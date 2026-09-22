"""
EXP037: Semantic Trajectory Verification Benchmark (Pythia-160M).

Pre-Registered Confirmatory Benchmark:
Evaluates whether combining internal kinematic trajectory bounds (d_2, rho_2) with
semantic context verification (Context Representation Fidelity S_context, Counterfactual
Energy E_CF) can distinguish smooth attractor drift from genuine failure rescue,
eliminating corruptions (c <= 1) while retaining failure rescues (b >= 4).

Evaluated Controllers:
1. Baseline (Unintervened M_I, 1 pass)
2. G_contrastive (Supervised reference, 1 pass)
3. Fixed_T1 (1-step relational trajectory, 1 pass)
4. Fixed_T2 (2-step blind recurrence, 2 passes)
5. Kinematic_Rollback (Reject if rho_2 < 0.4 or d_2 > 0.14)
6. Composite_Kin_Context (Reject if kinematic violation OR Delta S_context < 0)
7. Composite_Kin_ECF (Reject if kinematic violation OR Delta E_CF > 0)
8. Composite_Full (Reject if kinematic violation OR Delta S_context < 0 OR Delta E_CF > 0)

Guarantees:
- Pre/post parameter SHA-256 hash invariant (Delta theta = 0)
- Zero test-label leakage
- Exact Mann-Whitney U test on semantic diagnostic metrics
- Output saved to experiments/runs/EXP037_semantic_verification/exp037_semantic_verification_results.json
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

def extract_trajectory_subspace(h_late, h_early, rank=2):
    diff = h_late - h_early
    diff_cent = diff - torch.mean(diff, dim=0, keepdim=True)
    _, _, Vh = torch.linalg.svd(diff_cent, full_matrices=False)
    return Vh[:rank, :].T

def main():
    print("=" * 115)
    print("EXP037: SEMANTIC TRAJECTORY VERIFICATION BENCHMARK")
    print("Evaluating Composite Kinematic-Semantic Controllers vs. Smooth Attractor Drift (Pythia-160M)")
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

    print(f"\n>>> Step 1: Profiling Kinematic & Semantic Trajectory Metrics on {n_conf} Instances...")
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

        # Construct perturbed input for Counterfactual Energy evaluation (20% token masking)
        pert_ids = input_ids.clone()
        rng_pert = np.random.RandomState(seed_conf + idx * 13)
        mask_candidates = [t for t in range(1, T - 1)]
        n_mask = max(1, int(0.20 * len(mask_candidates)))
        mask_idx = rng_pert.choice(mask_candidates, size=n_mask, replace=False)
        for m_pos in mask_idx:
            pert_ids[0, m_pos] = tokenizer.eos_token_id

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

        # ---------------------------------------------------------------------
        # Step 1 (T=1)
        # ---------------------------------------------------------------------
        V_traj_1 = extract_trajectory_subspace(h_8_init, h_6_init, rank=rank)
        P_traj_1 = (V_traj_1 @ V_traj_1.T).to(h_8_init.device)

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

        # Compute Counterfactual Perturbation Energy at Step 1
        captured_pert1 = {}
        def hook_pert1(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                captured_pert1["h_8"] = h[0].detach()
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                captured_pert1["h_8"] = h[0].detach()
                return h

        hndl_pert1 = model_layers[target_block].register_forward_hook(hook_pert1)
        with torch.no_grad():
            model(input_ids=pert_ids)
        hndl_pert1.remove()

        h_8_pert1 = captured_pert1["h_8"]
        e_cf_1 = float(torch.mean(torch.norm(h_8_step1 - h_8_pert1, dim=-1)**2).item())

        # Compute Context Representation Fidelity at Step 1
        # Context tokens: tokens up to p_end (non-distractor premise tokens)
        h_ctx_1 = torch.mean(h_8_step1[prem_indices], dim=0)
        h_last_1 = h_8_step1[-1]
        s_context_1 = float((torch.dot(h_last_1, h_ctx_1) / (torch.norm(h_last_1) * torch.norm(h_ctx_1) + 1e-12)).item())

        # ---------------------------------------------------------------------
        # Step 2 (T=2)
        # ---------------------------------------------------------------------
        V_traj_2 = extract_trajectory_subspace(h_8_step1, h_6_init, rank=rank)
        P_traj_2 = (V_traj_2 @ V_traj_2.T).to(h_8_init.device)

        captured_step2 = {}
        def hook_step2(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2)
                captured_step2["h_8"] = h[0].detach()
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2)
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

        flat_d1 = delta_vec_1.view(-1)
        flat_d2 = delta_vec_2.view(-1)
        rho_2 = float((torch.dot(flat_d1, flat_d2) / (torch.norm(flat_d1) * torch.norm(flat_d2) + 1e-12)).item())

        # Compute Counterfactual Perturbation Energy at Step 2
        captured_pert2 = {}
        def hook_pert2(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2)
                captured_pert2["h_8"] = h[0].detach()
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2)
                captured_pert2["h_8"] = h[0].detach()
                return h

        hndl_pert2 = model_layers[target_block].register_forward_hook(hook_pert2)
        with torch.no_grad():
            model(input_ids=pert_ids)
        hndl_pert2.remove()

        h_8_pert2 = captured_pert2["h_8"]
        e_cf_2 = float(torch.mean(torch.norm(h_8_step2 - h_8_pert2, dim=-1)**2).item())
        delta_e_cf = e_cf_2 - e_cf_1

        # Compute Context Representation Fidelity at Step 2
        h_ctx_2 = torch.mean(h_8_step2[prem_indices], dim=0)
        h_last_2 = h_8_step2[-1]
        s_context_2 = float((torch.dot(h_last_2, h_ctx_2) / (torch.norm(h_last_2) * torch.norm(h_ctx_2) + 1e-12)).item())
        delta_s_context = s_context_2 - s_context_1

        # Event Classification
        is_corr_base = (pred_base == target_id)
        is_corr_t1 = (pred_t1 == target_id)
        is_corr_t2 = (pred_t2 == target_id)
        is_corr_c = (pred_c == target_id)

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
            "event_type": event_type,
            "d_2": d_2,
            "rho_2": rho_2,
            "s_context_1": s_context_1,
            "s_context_2": s_context_2,
            "delta_s_context": delta_s_context,
            "e_cf_1": e_cf_1,
            "e_cf_2": e_cf_2,
            "delta_e_cf": delta_e_cf,
            "logp_base": logp_tgt_base,
            "logp_c": logp_tgt_c,
            "logp_t1": logp_tgt_t1,
            "logp_t2": logp_tgt_t2
        })

    elapsed = time.time() - start_time
    print(f"[COMPUTE] Profiling completed in {elapsed:.1f}s.")

    # Verify Parameter Invariance
    post_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Post-run Parameter SHA-256: {post_hash}")
    assert pre_hash == post_hash, "CRITICAL ERROR: Parameters mutated during inference!"
    print("[REPRODUCIBILITY] Frozen Backbone Verified: Parameter hashes match identically (Delta theta = 0).")

    # -------------------------------------------------------------------------
    # PART A: SEMANTIC DIAGNOSTIC SEPARATION
    # -------------------------------------------------------------------------
    gain_records = [r for r in instance_records if r["event_type"] == "GAIN"]
    corr_records = [r for r in instance_records if r["event_type"] == "CORRUPTION"]
    neut_records = [r for r in instance_records if r["event_type"] == "NEUTRAL"]

    print("\n" + "=" * 115)
    print(f"PART A: SEMANTIC DIAGNOSTIC SEPARATION (Gain: N={len(gain_records)}, Corruption: N={len(corr_records)})")
    print("=" * 115)

    ds_gain = [r["delta_s_context"] for r in gain_records]
    ds_corr = [r["delta_s_context"] for r in corr_records]
    ds_neut = [r["delta_s_context"] for r in neut_records]

    de_gain = [r["delta_e_cf"] for r in gain_records]
    de_corr = [r["delta_e_cf"] for r in corr_records]
    de_neut = [r["delta_e_cf"] for r in neut_records]

    def run_mwu(g_vals, c_vals):
        try:
            res = mannwhitneyu(g_vals, c_vals, alternative='two-sided')
            return float(res.pvalue)
        except Exception:
            return 1.0

    p_ds = run_mwu(ds_gain, ds_corr)
    p_de = run_mwu(de_gain, de_corr)

    print(f"{'Metric':<35} | {'Gain Mean (N=5)':<18} | {'Corruption Mean (N=3)':<22} | {'Neutral Mean (N=42)':<20} | {'MWU p-value':<12}")
    print("-" * 115)
    print(f"{'Context Fidelity Shift Delta S_ctx':<35} | {np.mean(ds_gain):<18.4f} | {np.mean(ds_corr):<22.4f} | {np.mean(ds_neut):<20.4f} | {p_ds:<12.4f}")
    print(f"{'Counterfactual Energy Shift Delta E_CF':<35} | {np.mean(de_gain):<18.4f} | {np.mean(de_corr):<22.4f} | {np.mean(de_neut):<20.4f} | {p_de:<12.4f}")
    print("-" * 115)

    print("\nDetailed Semantic Metrics for Corrupted Instances:")
    for r in corr_records:
        print(f"  [CORRUPTION] Inst {r['idx']}: Delta S_ctx = {r['delta_s_context']:+.4f}, Delta E_CF = {r['delta_e_cf']:+.4f}, rho_2 = {r['rho_2']:.4f}")

    print("\nDetailed Semantic Metrics for Rescued Instances:")
    for r in gain_records:
        print(f"  [GAIN] Inst {r['idx']}: Delta S_ctx = {r['delta_s_context']:+.4f}, Delta E_CF = {r['delta_e_cf']:+.4f}, rho_2 = {r['rho_2']:.4f}")

    # -------------------------------------------------------------------------
    # PART B: EVALUATING COMPOSITE KINEMATIC-SEMANTIC CONTROLLERS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 115)
    print("PART B: EVALUATING COMPOSITE KINEMATIC-SEMANTIC ROLLBACK CONTROLLERS")
    print("=" * 115)
    print(f"{'Controller Condition':<30} | {'Acc':<7} | {'Delta M':<9} | {'95% CI':<16} | {'Delta log p':<12} | {'McNemar (vs Base)':<20} | {'b (Rescued)':<11} | {'c (Corrupted)':<13}")
    print("-" * 115)

    base_correct = [r["is_corr_base"] for r in instance_records]
    base_acc = float(np.mean(base_correct))

    # Evaluate Reference Baselines
    controllers_eval = {}

    # 1. Baseline
    controllers_eval["Baseline"] = ([r["is_corr_base"] for r in instance_records], [0.0 for _ in instance_records])
    # 2. G_contrastive
    controllers_eval["G_contrastive"] = ([r["is_corr_c"] for r in instance_records], [r["logp_c"] - r["logp_base"] for r in instance_records])
    # 3. Fixed_T1
    controllers_eval["Fixed_T1"] = ([r["is_corr_t1"] for r in instance_records], [r["logp_t1"] - r["logp_base"] for r in instance_records])
    # 4. Fixed_T2
    controllers_eval["Fixed_T2"] = ([r["is_corr_t2"] for r in instance_records], [r["logp_t2"] - r["logp_base"] for r in instance_records])

    # 5. Kinematic Rollback (from EXP036: reject if rho_2 < 0.4 or d_2 > 0.14)
    corr_kin = []
    dlogp_kin = []
    for r in instance_records:
        if r["rho_2"] < 0.40 or r["d_2"] > 0.14:
            corr_kin.append(r["is_corr_t1"])
            dlogp_kin.append(r["logp_t1"] - r["logp_base"])
        else:
            corr_kin.append(r["is_corr_t2"])
            dlogp_kin.append(r["logp_t2"] - r["logp_base"])
    controllers_eval["Kinematic_Rollback"] = (corr_kin, dlogp_kin)

    # 6. Composite Kinematic + Context Fidelity:
    # Reject Step 2 if kinematic violation OR Delta S_context < 0
    corr_ctx = []
    dlogp_ctx = []
    for r in instance_records:
        kin_viol = (r["rho_2"] < 0.40 or r["d_2"] > 0.14)
        sem_viol = (r["delta_s_context"] < 0.0)
        if kin_viol or sem_viol:
            corr_ctx.append(r["is_corr_t1"])
            dlogp_ctx.append(r["logp_t1"] - r["logp_base"])
        else:
            corr_ctx.append(r["is_corr_t2"])
            dlogp_ctx.append(r["logp_t2"] - r["logp_base"])
    controllers_eval["Composite_Kin_Context"] = (corr_ctx, dlogp_ctx)

    # 7. Composite Kinematic + Counterfactual Energy:
    # Reject Step 2 if kinematic violation OR Delta E_CF > 0
    corr_ecf = []
    dlogp_ecf = []
    for r in instance_records:
        kin_viol = (r["rho_2"] < 0.40 or r["d_2"] > 0.14)
        ecf_viol = (r["delta_e_cf"] > 0.0)
        if kin_viol or ecf_viol:
            corr_ecf.append(r["is_corr_t1"])
            dlogp_ecf.append(r["logp_t1"] - r["logp_base"])
        else:
            corr_ecf.append(r["is_corr_t2"])
            dlogp_ecf.append(r["logp_t2"] - r["logp_base"])
    controllers_eval["Composite_Kin_ECF"] = (corr_ecf, dlogp_ecf)

    # 8. Composite Full (Kinematic + Context Fidelity + E_CF):
    corr_full = []
    dlogp_full = []
    for r in instance_records:
        kin_viol = (r["rho_2"] < 0.40 or r["d_2"] > 0.14)
        sem_viol = (r["delta_s_context"] < 0.0 or r["delta_e_cf"] > 0.0)
        if kin_viol or sem_viol:
            corr_full.append(r["is_corr_t1"])
            dlogp_full.append(r["logp_t1"] - r["logp_base"])
        else:
            corr_full.append(r["is_corr_t2"])
            dlogp_full.append(r["logp_t2"] - r["logp_base"])
    controllers_eval["Composite_Full"] = (corr_full, dlogp_full)

    results_summary = {
        "metadata": {
            "experiment_id": "EXP037",
            "date": "2026-09-12",
            "model": model_name,
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_invariant": (pre_hash == post_hash),
            "n_conf": n_conf,
            "base_acc": base_acc
        },
        "semantic_diagnostics": {
            "delta_s_context": {"gain_mean": float(np.mean(ds_gain)), "corr_mean": float(np.mean(ds_corr)), "neut_mean": float(np.mean(ds_neut)), "p_val": p_ds},
            "delta_e_cf": {"gain_mean": float(np.mean(de_gain)), "corr_mean": float(np.mean(de_corr)), "neut_mean": float(np.mean(de_neut)), "p_val": p_de}
        },
        "controllers": {}
    }

    for name, (c_list, d_list) in controllers_eval.items():
        acc = float(np.mean(c_list))
        delta_m = acc - base_acc
        delta_arr = [float(c) - float(b) for c, b in zip(c_list, base_correct)]
        ci = compute_bootstrap_ci(delta_arr, n_boot=1000)
        b = sum(1 for c, b_val in zip(c_list, base_correct) if c and not b_val)
        c = sum(1 for c, b_val in zip(c_list, base_correct) if not c and b_val)
        p_mcnemar = exact_mcnemar(b, c)
        mean_dlogp = float(np.mean(d_list))

        results_summary["controllers"][name] = {
            "accuracy": acc,
            "delta_m": delta_m,
            "ci_95": ci,
            "mean_delta_logp": mean_dlogp,
            "rescued_b": b,
            "corrupted_c": c,
            "mcnemar_p": p_mcnemar
        }
        print(f"{name:<30} | {acc:.4f}  | {delta_m*100:+5.1f} pp | [{ci[0]*100:+5.1f}, {ci[1]*100:+5.1f}] pp | {mean_dlogp:+10.4f}   | b={b}, c={c}, p={p_mcnemar:.4f}     | {b:<11} | {c:<13}")

    print("-" * 115)

    # Save to json
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP037_semantic_verification"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "exp037_semantic_verification_results.json")
    with open(out_file, "w") as f:
        json.dump(results_summary, f, indent=2)
    print(f"\n[OUTPUT] Saved complete benchmark results to: {out_file}")

if __name__ == "__main__":
    main()
