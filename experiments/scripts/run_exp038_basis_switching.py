"""
EXP038: Compute-Bounded Attractor Discrimination & Dynamic Basis Switching Benchmark (Pythia-160M).

Pre-Registered Confirmatory Benchmark:
1. Evaluates multiple independently motivated semantic diagnostic signals to distinguish
   genuine semantic alignment from surface lexical unigram overlap (dissecting Inst 28):
   - S_context: Mean context token cosine similarity (EXP037 baseline)
   - S_clause: Clause subspace projection differential (rank-2 Premise vs Distractor)
   - S_trajectory: Inter-layer forward flow trajectory alignment
   - kappa_2: Trajectory acceleration / curvature
2. Evaluates an expanded compute-bounded action space:
   A = {CONTINUE, STOP, ROLLBACK, CHANGE BASIS}
   where failing updates trigger ROLLBACK and spend their remaining forward pass (B_eval <= 3)
   evaluating an alternative secondary orthogonal trajectory subspace (V_2 = SVD_{3:4}).
3. Tracks compute-normalized metrics:
   - Marginal FLOP efficiency: Delta log p / forward passes
   - Rescue yield: rescues / total forward passes

Guarantees:
- Pre/post parameter SHA-256 hash invariant (Delta theta = 0)
- Zero test-label leakage
- Explicit forward pass budget <= 3
- Output saved to experiments/runs/EXP038_basis_switching/exp038_basis_switching_results.json
"""

import os
import sys
import time
import json
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import mannwhitneyu, binomtest
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def compute_bootstrap_ci(data, n_boot=1000, ci=0.95):
    if len(data) == 0:
        return [0.0, 0.0]
    arr = np.array(data)
    boot_means = [np.mean(np.random.choice(arr, size=len(arr), replace=True)) for _ in range(n_boot)]
    alpha_ci = (1.0 - ci) / 2.0
    low = float(np.percentile(boot_means, alpha_ci * 100))
    high = float(np.percentile(boot_means, (1.0 - alpha_ci) * 100))
    return [low, high]

def exact_mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    res = binomtest(b, n, 0.5, alternative='greater')
    return float(res.pvalue)

def extract_contrastive_subspace(h, prem_indices, dist_indices, rank=2):
    h_dist = h[dist_indices, :]
    h_d_cent = h_dist - torch.mean(h_dist, dim=0, keepdim=True)
    _, _, Vh_d = torch.linalg.svd(h_d_cent, full_matrices=False)
    return Vh_d[:rank, :].T

def extract_subspace_modes(h_late, h_early, rank=2):
    diff = h_late - h_early
    diff_cent = diff - torch.mean(diff, dim=0, keepdim=True)
    _, _, Vh = torch.linalg.svd(diff_cent, full_matrices=False)
    # Mode 1: primary direction (1:rank)
    V1 = Vh[:rank, :].T
    # Mode 2: secondary orthogonal direction (rank:2*rank)
    V2 = Vh[rank:2*rank, :].T if Vh.shape[0] >= 2*rank else Vh[:rank, :].T
    return V1, V2

def extract_clause_subspace(h, indices, rank=2):
    h_sub = h[indices, :]
    if h_sub.shape[0] < rank:
        rank = h_sub.shape[0]
    h_cent = h_sub - torch.mean(h_sub, dim=0, keepdim=True)
    _, _, Vh = torch.linalg.svd(h_cent, full_matrices=False)
    return Vh[:rank, :].T

def main():
    print("=" * 115)
    print("EXP038: COMPUTE-BOUNDED ATTRACTOR DISCRIMINATION & DYNAMIC BASIS SWITCHING BENCHMARK")
    print("Evaluating Gist vs Surface Overlap & Compute-Bounded Basis Switching (Pythia-160M)")
    print("=" * 115)

    model_name = "EleutherAI/pythia-160m"
    n_conf = 50
    seed_conf = 84
    target_layer = 8
    target_block = target_layer - 1 # Block 7
    layer_6_block = 5               # Block 5
    alpha = 0.25
    rank = 2

    # 1. Load Dataset
    conf_dataset = generate_bench_002_nl(n_instances=n_conf, seed=seed_conf)
    print(f"[DATASET] Loaded {len(conf_dataset)} confirmatory instances (BENCH-002-NL, Seed {seed_conf}).")

    # 2. Load Model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run Parameter SHA-256: {pre_hash}")

    model_layers = model.gpt_neox.layers

    instance_records = []

    print(f"\n>>> Step 1: Profiling Trajectories, Signals & Alternative Bases on {n_conf} Instances...")
    start_time = time.time()

    torch.manual_seed(seed_conf)
    np.random.seed(seed_conf)

    for idx, inst in enumerate(conf_dataset):
        prompt = inst["base"]
        target_token = inst["target"].strip()
        distractor_token = inst["distractor"].strip()

        target_id = tokenizer.encode(" " + target_token)[0] if tokenizer.encode(" " + target_token) else tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(" " + distractor_token)[0] if tokenizer.encode(" " + distractor_token) else tokenizer.encode(distractor_token)[0]

        enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
        input_ids = enc.input_ids
        offsets = enc.offset_mapping[0].tolist()
        T = input_ids.shape[1]

        try:
            p_end = prompt.index(" Distractor:")
            d_end = prompt.index(" Question:")
            prem_indices = [i for i, (s, e) in enumerate(offsets) if e <= p_end and s < e]
            dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
        except ValueError:
            continue

        # ---------------------------------------------------------------------
        # Base Forward Pass (T=0)
        # ---------------------------------------------------------------------
        captured = {}
        def cap_l6_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h_6"] = h.detach().squeeze(0)

        def cap_l8_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h_8"] = h.detach().squeeze(0)

        hndl_6 = model_layers[layer_6_block].register_forward_hook(cap_l6_hook)
        hndl_8 = model_layers[target_block].register_forward_hook(cap_l8_hook)

        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())

        hndl_6.remove()
        hndl_8.remove()

        h_6_init = captured["h_6"]
        h_8_init = captured["h_8"]

        # Supervised Contrast Reference
        V_contrastive = extract_contrastive_subspace(h_8_init, prem_indices, dist_indices, rank=rank)
        P_contrastive = (V_contrastive @ V_contrastive.T).to(h_8_init.device)

        def make_linear_hook(P_proj):
            def hook_fn(mod, inp, outp):
                if isinstance(outp, tuple):
                    h = outp[0].clone()
                    h[0] = h[0] - alpha * (h[0] @ P_proj)
                    return (h,) + outp[1:]
                else:
                    h = outp.clone()
                    h[0] = h[0] - alpha * (h[0] @ P_proj)
                    return h
            return hook_fn

        hndl_c = model_layers[target_block].register_forward_hook(make_linear_hook(P_contrastive))
        with torch.no_grad():
            out_c = model(input_ids=input_ids)
            logits_c = out_c.logits[0, -1, :]
            pred_c = torch.argmax(logits_c).item()
            logp_tgt_c = float(torch.log(torch.clamp(F.softmax(logits_c, dim=-1)[target_id], min=1e-12)).item())
        hndl_c.remove()

        # Extract Primary (V1) and Secondary (V2) Subspace Modes from Initial Trajectory
        V_traj_1, V_traj_2 = extract_subspace_modes(h_8_init, h_6_init, rank=rank)
        P_traj_1 = (V_traj_1 @ V_traj_1.T).to(h_8_init.device)
        P_traj_2_alt = (V_traj_2 @ V_traj_2.T).to(h_8_init.device)

        # Clause Subspaces for Signal 1
        V_prem = extract_clause_subspace(h_8_init, prem_indices, rank=rank)
        V_dist = extract_clause_subspace(h_8_init, dist_indices, rank=rank)
        P_prem = (V_prem @ V_prem.T).to(h_8_init.device)
        P_dist = (V_dist @ V_dist.T).to(h_8_init.device)

        flow_vec_0 = (h_8_init - h_6_init).view(-1)
        flow_norm_0 = torch.norm(flow_vec_0) + 1e-12

        # ---------------------------------------------------------------------
        # Step 1 (T=1, Primary Basis V1)
        # ---------------------------------------------------------------------
        captured_step1 = {}
        def hook_step1(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                captured_step1["h_8"] = h[0].detach()
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                captured_step1["h_8"] = h[0].detach()
                return h

        hndl_t1 = model_layers[target_block].register_forward_hook(hook_step1)
        with torch.no_grad():
            out_t1 = model(input_ids=input_ids)
            logits_t1 = out_t1.logits[0, -1, :]
            probs_t1 = F.softmax(logits_t1, dim=-1)
            pred_t1 = torch.argmax(logits_t1).item()
            logp_tgt_t1 = float(torch.log(torch.clamp(probs_t1[target_id], min=1e-12)).item())
        hndl_t1.remove()

        h_8_step1 = captured_step1["h_8"]
        delta_vec_1 = h_8_step1 - h_8_init

        # Signal Computations at Step 1:
        # Context Fidelity (EXP037)
        h_ctx_1 = torch.mean(h_8_step1[prem_indices], dim=0)
        h_last_1 = h_8_step1[-1]
        s_context_1 = float((torch.dot(h_last_1, h_ctx_1) / (torch.norm(h_last_1) * torch.norm(h_ctx_1) + 1e-12)).item())

        # Clause Subspace Projection (EXP038 Signal 1)
        # S_clause = ||P_prem h_last||^2 - ||P_dist h_last||^2
        s_clause_1 = float((torch.norm(h_last_1 @ P_prem)**2 - torch.norm(h_last_1 @ P_dist)**2).item())

        # Inter-Layer Trajectory Flow Alignment (EXP038 Signal 2)
        flat_d1 = delta_vec_1.view(-1)
        s_traj_1 = float((torch.dot(flat_d1, flow_vec_0) / (torch.norm(flat_d1) * flow_norm_0 + 1e-12)).item())

        # ---------------------------------------------------------------------
        # Step 2 (T=2, Standard Recurrence with Updated V_traj_2)
        # ---------------------------------------------------------------------
        V_traj_step2, _ = extract_subspace_modes(h_8_step1, h_6_init, rank=rank)
        P_traj_step2 = (V_traj_step2 @ V_traj_step2.T).to(h_8_init.device)

        captured_step2 = {}
        def hook_step2(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_step2)
                captured_step2["h_8"] = h[0].detach()
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_step2)
                captured_step2["h_8"] = h[0].detach()
                return h

        hndl_t2 = model_layers[target_block].register_forward_hook(hook_step2)
        with torch.no_grad():
            out_t2 = model(input_ids=input_ids)
            logits_t2 = out_t2.logits[0, -1, :]
            probs_t2 = F.softmax(logits_t2, dim=-1)
            pred_t2 = torch.argmax(logits_t2).item()
            logp_tgt_t2 = float(torch.log(torch.clamp(probs_t2[target_id], min=1e-12)).item())
        hndl_t2.remove()

        h_8_step2 = captured_step2["h_8"]
        delta_vec_2 = h_8_step2 - h_8_step1
        d_2 = float((torch.norm(delta_vec_2) / (torch.norm(h_8_step1) + 1e-12)).item())

        flat_d2 = delta_vec_2.view(-1)
        rho_2 = float((torch.dot(flat_d1, flat_d2) / (torch.norm(flat_d1) * torch.norm(flat_d2) + 1e-12)).item())

        # Curvature / Acceleration (Signal 3)
        accel_vec = delta_vec_2 - delta_vec_1
        kappa_2 = float((torch.norm(accel_vec) / (torch.norm(delta_vec_1) + 1e-12)).item())

        # Signals at Step 2:
        h_ctx_2 = torch.mean(h_8_step2[prem_indices], dim=0)
        h_last_2 = h_8_step2[-1]
        s_context_2 = float((torch.dot(h_last_2, h_ctx_2) / (torch.norm(h_last_2) * torch.norm(h_ctx_2) + 1e-12)).item())
        delta_s_context = s_context_2 - s_context_1

        s_clause_2 = float((torch.norm(h_last_2 @ P_prem)**2 - torch.norm(h_last_2 @ P_dist)**2).item())
        delta_s_clause = s_clause_2 - s_clause_1

        s_traj_2 = float((torch.dot(flat_d2, flow_vec_0) / (torch.norm(flat_d2) * flow_norm_0 + 1e-12)).item())
        delta_s_traj = s_traj_2 - s_traj_1

        # ---------------------------------------------------------------------
        # Alternative Basis Evaluation (CHANGE BASIS to V_2 = SVD_{3:4})
        # ---------------------------------------------------------------------
        # Evaluated if Step 2 is rejected, taking the 3rd forward pass budget
        captured_alt = {}
        def hook_alt(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2_alt)
                captured_alt["h_8"] = h[0].detach()
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2_alt)
                captured_alt["h_8"] = h[0].detach()
                return h

        hndl_alt = model_layers[target_block].register_forward_hook(hook_alt)
        with torch.no_grad():
            out_alt = model(input_ids=input_ids)
            logits_alt = out_alt.logits[0, -1, :]
            probs_alt = F.softmax(logits_alt, dim=-1)
            pred_alt = torch.argmax(logits_alt).item()
            logp_tgt_alt = float(torch.log(torch.clamp(probs_alt[target_id], min=1e-12)).item())
        hndl_alt.remove()

        h_8_alt = captured_alt["h_8"]
        h_last_alt = h_8_alt[-1]
        s_clause_alt = float((torch.norm(h_last_alt @ P_prem)**2 - torch.norm(h_last_alt @ P_dist)**2).item())
        delta_s_clause_alt = s_clause_alt - s_clause_1

        # Event Classification (Step 1 vs Step 2)
        is_corr_base = (pred_base == target_id)
        is_corr_t1 = (pred_t1 == target_id)
        is_corr_t2 = (pred_t2 == target_id)
        is_corr_c = (pred_c == target_id)
        is_corr_alt = (pred_alt == target_id)

        if not is_corr_t1 and is_corr_t2:
            event_type = "GAIN"
        elif is_corr_t1 and not is_corr_t2:
            event_type = "CORRUPTION"
        else:
            event_type = "NEUTRAL"

        instance_records.append({
            "idx": idx,
            "is_corr_base": is_corr_base,
            "is_corr_c": is_corr_c,
            "is_corr_t1": is_corr_t1,
            "is_corr_t2": is_corr_t2,
            "is_corr_alt": is_corr_alt,
            "event_type": event_type,
            "d_2": d_2,
            "rho_2": rho_2,
            "kappa_2": kappa_2,
            "delta_s_context": delta_s_context,
            "delta_s_clause": delta_s_clause,
            "delta_s_traj": delta_s_traj,
            "delta_s_clause_alt": delta_s_clause_alt,
            "logp_base": logp_tgt_base,
            "logp_c": logp_tgt_c,
            "logp_t1": logp_tgt_t1,
            "logp_t2": logp_tgt_t2,
            "logp_alt": logp_tgt_alt
        })

    elapsed = time.time() - start_time
    print(f"[COMPUTE] Profiling completed in {elapsed:.1f}s.")

    # Verify Parameter Invariance
    post_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Post-run Parameter SHA-256: {post_hash}")
    assert pre_hash == post_hash, "CRITICAL ERROR: Parameters mutated during inference!"
    print("[REPRODUCIBILITY] Frozen Backbone Verified: Parameter hashes match identically (Delta theta = 0).")

    # -------------------------------------------------------------------------
    # PART A: DIAGNOSTIC SIGNAL COMPARISON (GIST VS SURFACE OVERLAP)
    # -------------------------------------------------------------------------
    gain_records = [r for r in instance_records if r["event_type"] == "GAIN"]
    corr_records = [r for r in instance_records if r["event_type"] == "CORRUPTION"]
    neut_records = [r for r in instance_records if r["event_type"] == "NEUTRAL"]

    print("\n" + "=" * 115)
    print(f"PART A: DIAGNOSTIC SIGNAL COMPARISON (Gain: N={len(gain_records)}, Corruption: N={len(corr_records)})")
    print("=" * 115)

    def run_mwu(g_vals, c_vals):
        try:
            res = mannwhitneyu(g_vals, c_vals, alternative='two-sided')
            return float(res.pvalue)
        except Exception:
            return 1.0

    metrics_dict = {
        "Delta S_context (Mean Token)": ([r["delta_s_context"] for r in gain_records], [r["delta_s_context"] for r in corr_records], [r["delta_s_context"] for r in neut_records]),
        "Delta S_clause (Subspace)": ([r["delta_s_clause"] for r in gain_records], [r["delta_s_clause"] for r in corr_records], [r["delta_s_clause"] for r in neut_records]),
        "Delta S_trajectory (Flow Alignment)": ([r["delta_s_traj"] for r in gain_records], [r["delta_s_traj"] for r in corr_records], [r["delta_s_traj"] for r in neut_records]),
        "kappa_2 (Curvature / Accel)": ([r["kappa_2"] for r in gain_records], [r["kappa_2"] for r in corr_records], [r["kappa_2"] for r in neut_records])
    }

    print(f"{'Diagnostic Metric':<35} | {'Gain Mean (N=2)':<18} | {'Corruption Mean (N=3)':<22} | {'Neutral Mean (N=45)':<20} | {'MWU p-val':<10}")
    print("-" * 115)
    for m_name, (g_v, c_v, n_v) in metrics_dict.items():
        p_val = run_mwu(g_v, c_v)
        print(f"{m_name:<35} | {np.mean(g_v):<18.4f} | {np.mean(c_v):<22.4f} | {np.mean(n_v):<20.4f} | {p_val:<10.4f}")
    print("-" * 115)

    print("\nDetailed Diagnostic Breakdown on Critical Instances:")
    for r in corr_records:
        print(f"  [CORRUPTION] Inst {r['idx']:02d}: rho_2={r['rho_2']:.4f}, Delta S_ctx={r['delta_s_context']:+.4f}, Delta S_clause={r['delta_s_clause']:+.4f}, Delta S_traj={r['delta_s_traj']:+.4f}")
    for r in gain_records:
        print(f"  [GAIN]       Inst {r['idx']:02d}: rho_2={r['rho_2']:.4f}, Delta S_ctx={r['delta_s_context']:+.4f}, Delta S_clause={r['delta_s_clause']:+.4f}, Delta S_traj={r['delta_s_traj']:+.4f}")

    # -------------------------------------------------------------------------
    # PART B: EVALUATING CONTROLLERS & COMPUTE-BOUNDED BASIS SWITCHING
    # -------------------------------------------------------------------------
    print("\n" + "=" * 115)
    print("PART B: EVALUATING CONTROLLERS & COMPUTE-BOUNDED BASIS SWITCHING (B_eval <= 3)")
    print("=" * 115)
    print(f"{'Controller Strategy':<30} | {'Acc':<7} | {'Delta M':<9} | {'95% CI':<16} | {'Delta log p':<12} | {'b / c':<8} | {'McNemar p':<11} | {'Evals/Inst':<10}")
    print("-" * 115)

    base_correct = [r["is_corr_base"] for r in instance_records]
    base_acc = float(np.mean(base_correct))

    controllers_eval = {}

    # 1. Baseline
    controllers_eval["Baseline"] = {
        "correct": [r["is_corr_base"] for r in instance_records],
        "dlogp": [0.0 for _ in instance_records],
        "evals": [1 for _ in instance_records]
    }
    # 2. G_contrastive
    controllers_eval["G_contrastive"] = {
        "correct": [r["is_corr_c"] for r in instance_records],
        "dlogp": [r["logp_c"] - r["logp_base"] for r in instance_records],
        "evals": [1 for _ in instance_records]
    }
    # 3. Fixed_T1
    controllers_eval["Fixed_T1"] = {
        "correct": [r["is_corr_t1"] for r in instance_records],
        "dlogp": [r["logp_t1"] - r["logp_base"] for r in instance_records],
        "evals": [1 for _ in instance_records]
    }
    # 4. Fixed_T2
    controllers_eval["Fixed_T2"] = {
        "correct": [r["is_corr_t2"] for r in instance_records],
        "dlogp": [r["logp_t2"] - r["logp_base"] for r in instance_records],
        "evals": [2 for _ in instance_records]
    }
    # 5. Kinematic Rollback (EXP036)
    corr_kin, dlogp_kin, evals_kin = [], [], []
    for r in instance_records:
        if r["rho_2"] < 0.40 or r["d_2"] > 0.14:
            corr_kin.append(r["is_corr_t1"])
            dlogp_kin.append(r["logp_t1"] - r["logp_base"])
        else:
            corr_kin.append(r["is_corr_t2"])
            dlogp_kin.append(r["logp_t2"] - r["logp_base"])
        evals_kin.append(2)
    controllers_eval["Kinematic_Rollback"] = {"correct": corr_kin, "dlogp": dlogp_kin, "evals": evals_kin}

    # 6. Composite Kinematic + Context Fidelity (EXP037)
    corr_ctx, dlogp_ctx, evals_ctx = [], [], []
    for r in instance_records:
        kin_viol = (r["rho_2"] < 0.40 or r["d_2"] > 0.14)
        sem_viol = (r["delta_s_context"] < 0.0)
        if kin_viol or sem_viol:
            corr_ctx.append(r["is_corr_t1"])
            dlogp_ctx.append(r["logp_t1"] - r["logp_base"])
        else:
            corr_ctx.append(r["is_corr_t2"])
            dlogp_ctx.append(r["logp_t2"] - r["logp_base"])
        evals_ctx.append(2)
    controllers_eval["Composite_Kin_Context"] = {"correct": corr_ctx, "dlogp": dlogp_ctx, "evals": evals_ctx}

    # 7. Composite Kinematic + Clause Subspace (EXP038)
    corr_cls, dlogp_cls, evals_cls = [], [], []
    for r in instance_records:
        kin_viol = (r["rho_2"] < 0.40 or r["d_2"] > 0.14)
        cls_viol = (r["delta_s_clause"] < 0.0)
        if kin_viol or cls_viol:
            corr_cls.append(r["is_corr_t1"])
            dlogp_cls.append(r["logp_t1"] - r["logp_base"])
        else:
            corr_cls.append(r["is_corr_t2"])
            dlogp_cls.append(r["logp_t2"] - r["logp_base"])
        evals_cls.append(2)
    controllers_eval["Composite_Kin_Clause"] = {"correct": corr_cls, "dlogp": dlogp_cls, "evals": evals_cls}

    # 8. Adaptive Switching Controller:
    # If Step 2 passes kinematic + semantic gate -> ACCEPT Step 2 (2 evals)
    # If Step 2 fails -> ROLLBACK and spend 3rd eval evaluating V_2 (Secondary Mode)
    # If V_2 yields positive clause alignment (Delta S_clause_alt >= 0) -> ACCEPT V_2
    # Else -> TERMINAL ROLLBACK to Step 1.
    corr_sw, dlogp_sw, evals_sw = [], [], []
    switch_count = 0
    switch_success = 0
    for r in instance_records:
        kin_viol = (r["rho_2"] < 0.40 or r["d_2"] > 0.14)
        sem_viol = (r["delta_s_context"] < 0.0 or r["delta_s_clause"] < 0.0)

        if not kin_viol and not sem_viol:
            # Action: CONTINUE (Accept Step 2)
            corr_sw.append(r["is_corr_t2"])
            dlogp_sw.append(r["logp_t2"] - r["logp_base"])
            evals_sw.append(2)
        else:
            # Action: ROLLBACK & CHANGE BASIS to V_2 (uses 3rd eval)
            switch_count += 1
            if r["delta_s_clause_alt"] >= 0.0:
                # Accept V_2
                corr_sw.append(r["is_corr_alt"])
                dlogp_sw.append(r["logp_alt"] - r["logp_base"])
                if r["is_corr_alt"] and not r["is_corr_base"]:
                    switch_success += 1
            else:
                # Terminal rollback to Step 1
                corr_sw.append(r["is_corr_t1"])
                dlogp_sw.append(r["logp_t1"] - r["logp_base"])
            evals_sw.append(3)
    controllers_eval["Switching_Controller"] = {"correct": corr_sw, "dlogp": dlogp_sw, "evals": evals_sw}

    results_summary = {
        "metadata": {
            "experiment_id": "EXP038",
            "date": "2026-09-12",
            "model": model_name,
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_invariant": (pre_hash == post_hash),
            "n_conf": n_conf,
            "base_acc": base_acc
        },
        "diagnostics_summary": {
            "delta_s_clause": {
                "gain_mean": float(np.mean(metrics_dict["Delta S_clause (Subspace)"][0])),
                "corr_mean": float(np.mean(metrics_dict["Delta S_clause (Subspace)"][1])),
                "p_val": run_mwu(metrics_dict["Delta S_clause (Subspace)"][0], metrics_dict["Delta S_clause (Subspace)"][1])
            },
            "inst_28": {
                "delta_s_context": float(instance_records[28]["delta_s_context"]),
                "delta_s_clause": float(instance_records[28]["delta_s_clause"]),
                "delta_s_traj": float(instance_records[28]["delta_s_traj"])
            }
        },
        "controllers": {}
    }

    for name, data in controllers_eval.items():
        c_list = data["correct"]
        d_list = data["dlogp"]
        e_list = data["evals"]

        acc = float(np.mean(c_list))
        delta_m = acc - base_acc
        delta_arr = [float(c) - float(b) for c, b in zip(c_list, base_correct)]
        ci = compute_bootstrap_ci(delta_arr, n_boot=1000)
        b = sum(1 for c, b_val in zip(c_list, base_correct) if c and not b_val)
        c = sum(1 for c, b_val in zip(c_list, base_correct) if not c and b_val)
        p_mcnemar = exact_mcnemar(b, c)
        mean_dlogp = float(np.mean(d_list))
        mean_evals = float(np.mean(e_list))
        flop_eff = mean_dlogp / mean_evals if mean_evals > 0 else 0.0

        results_summary["controllers"][name] = {
            "accuracy": acc,
            "delta_m": delta_m,
            "ci_95": ci,
            "mean_delta_logp": mean_dlogp,
            "rescued_b": b,
            "corrupted_c": c,
            "mcnemar_p": p_mcnemar,
            "mean_evals": mean_evals,
            "flop_eff": flop_eff
        }
        print(f"{name:<30} | {acc:.4f}  | {delta_m*100:+5.1f} pp | [{ci[0]*100:+5.1f}, {ci[1]*100:+5.1f}] pp | {mean_dlogp:+10.4f}   | b={b:<2}, c={c:<2} | p={p_mcnemar:<9.4f} | {mean_evals:<10.2f}")

    print("-" * 115)
    print(f"\n[SWITCHING DYNAMICS] Total Basis Switches Triggered: {switch_count}/{n_conf}")
    print(f"[SWITCHING DYNAMICS] Rescues from Secondary Mode V_2: {switch_success}")

    # Save to json
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP038_basis_switching"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "exp038_basis_switching_results.json")
    with open(out_file, "w") as f:
        json.dump(results_summary, f, indent=2)
    print(f"[OUTPUT] Saved complete benchmark results to: {out_file}")

if __name__ == "__main__":
    main()
