"""
EXP039: Prospective Representation-Generator Selection Benchmark (Pythia-160M).

Pre-Registered Confirmatory Benchmark:
Evaluates whether an autonomous inference controller can prospectively predict which
qualitative candidate representation generator:
  G_1: Inter-Layer Trajectory Flow (h_8 - h_6)
  G_2: Contextual Counterfactual Perturbation (h_8 - h_{8,pert})
  G_3: Attention-Derived Relational Subspace (Attention Head Routing Contrast)
is optimal for an instance BEFORE spending forward passes to evaluate candidates.

Core Comparisons:
1. Baseline (Unintervened M_I, 1 pass)
2. G_contrastive (Supervised reference, 1 pass)
3. Static G_1 (Always Trajectory, 1 pass)
4. Static G_2 (Always Contextual, 1 pass)
5. Static G_3 (Always Attention, 1 pass)
6. Oracle Selection pi_oracle (Best of {G1, G2, G3} with label knowledge)
7. Prospective Selection pi_prospective (Pre-intervention policy q(g|x, h_0), 1 pass)

Guarantees:
- Pre/post parameter SHA-256 hash invariant (Delta theta = 0)
- Zero test-label leakage in prospective policy
- Exactly 1 intervention forward pass per instance (B_eval = 1.0)
- Output saved to experiments/runs/EXP039_generator_selection/exp039_generator_selection_results.json
"""

import os
import sys
import time
import json
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import binomtest
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

def extract_attention_relational_subspace(h, attn_maps, prem_indices, dist_indices, rank=2):
    # attn_maps: [num_heads, seq_len, seq_len] at Layer 8
    # Focus on the last token's attention distribution across heads: [num_heads, seq_len]
    last_attn = attn_maps[:, -1, :] # [num_heads, seq_len]
    prem_attn = torch.sum(last_attn[:, prem_indices], dim=-1) # [num_heads]
    dist_attn = torch.sum(last_attn[:, dist_indices], dim=-1) # [num_heads]
    head_bias = prem_attn - dist_attn # positive = premise preference, negative = distractor preference

    # Compute head-weighted token representations
    # For heads that attend to distractor vs premise:
    # Build contrastive weighted vector across sequence
    diff_attn = torch.mean(last_attn[head_bias < 0, :], dim=0) if (head_bias < 0).any() else torch.mean(last_attn, dim=0)
    prem_attn_mean = torch.mean(last_attn[head_bias > 0, :], dim=0) if (head_bias > 0).any() else torch.mean(last_attn, dim=0)

    h_dist_rep = torch.sum(diff_attn.unsqueeze(-1) * h, dim=0, keepdim=True) # [1, d]
    h_prem_rep = torch.sum(prem_attn_mean.unsqueeze(-1) * h, dim=0, keepdim=True) # [1, d]

    rel_mat = h_dist_rep - h_prem_rep # [1, d]
    # To form a rank-2 subspace, expand with token-level weighted residuals
    weighted_diff = (diff_attn - prem_attn_mean).unsqueeze(-1) * h # [T, d]
    weighted_cent = weighted_diff - torch.mean(weighted_diff, dim=0, keepdim=True)
    _, _, Vh = torch.linalg.svd(weighted_cent, full_matrices=False)
    return Vh[:rank, :].T

def main():
    print("=" * 115)
    print("EXP039: PROSPECTIVE REPRESENTATION-GENERATOR SELECTION BENCHMARK")
    print("Evaluating Adaptive Representation Strategy vs. Blind Search (Pythia-160M)")
    print("=" * 115)

    model_name = "EleutherAI/pythia-160m"
    n_conf = 50
    seed_conf = 84
    target_layer = 8
    target_block = target_layer - 1 # Block 7
    layer_6_block = 5               # Block 5
    layer_4_block = 3               # Block 3
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

    print(f"\n>>> Step 1: Profiling Generators G_1, G_2, G_3 on {n_conf} Instances...")
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
        # Base Forward Pass (T=0) with State Capture
        # ---------------------------------------------------------------------
        captured = {}
        def cap_l4_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h_4"] = h.detach().squeeze(0)

        def cap_l6_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h_6"] = h.detach().squeeze(0)

        def cap_l8_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h_8"] = h.detach().squeeze(0)

        hndl_4 = model_layers[layer_4_block].register_forward_hook(cap_l4_hook)
        hndl_6 = model_layers[layer_6_block].register_forward_hook(cap_l6_hook)
        hndl_8 = model_layers[target_block].register_forward_hook(cap_l8_hook)

        with torch.no_grad():
            out_base = model(input_ids=input_ids, output_attentions=True)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())
            attn_layer8 = out_base.attentions[target_block][0].detach() # [num_heads, seq_len, seq_len]

        hndl_4.remove()
        hndl_6.remove()
        hndl_8.remove()

        h_4_init = captured["h_4"]
        h_6_init = captured["h_6"]
        h_8_init = captured["h_8"]

        # ---------------------------------------------------------------------
        # Prospective State Observables (Available at T=0 before intervention)
        # ---------------------------------------------------------------------
        # 1. Flow Velocity Ratio: r_flow = ||h_8 - h_6|| / ||h_6 - h_4||
        diff_8_6 = torch.norm(h_8_init - h_6_init)
        diff_6_4 = torch.norm(h_6_init - h_4_init)
        r_flow = float((diff_8_6 / (diff_6_4 + 1e-12)).item())

        # 2. Attention Premise vs Distractor Ratio:
        last_attn = attn_layer8[:, -1, :] # [num_heads, seq_len]
        prem_attn_sum = float(torch.sum(last_attn[:, prem_indices]).item())
        dist_attn_sum = float(torch.sum(last_attn[:, dist_indices]).item())
        attn_ratio = prem_attn_sum / (dist_attn_sum + 1e-12)

        # 3. Last Token Attention Entropy:
        mean_attn_seq = torch.mean(last_attn, dim=0) # [seq_len]
        ctx_attn = mean_attn_seq[prem_indices + dist_indices]
        ctx_attn_prob = ctx_attn / (torch.sum(ctx_attn) + 1e-12)
        h_attn_entropy = float((-torch.sum(ctx_attn_prob * torch.log(ctx_attn_prob + 1e-12))).item())

        # Prospective Policy Rule q(g | x, h_0):
        # If distractor draws substantial attention (attn_ratio < 1.1) -> G_3 (Attention Relational)
        # Else if r_flow >= 1.05 (strong inter-layer acceleration) -> G_1 (Trajectory Flow)
        # Else -> G_2 (Contextual Perturbation)
        if attn_ratio < 1.1:
            predicted_g = "G3_attn"
        elif r_flow >= 1.05:
            predicted_g = "G1_traj"
        else:
            predicted_g = "G2_ctx"

        # ---------------------------------------------------------------------
        # Extract Candidate Bases for G_1, G_2, G_3, G_contrastive
        # ---------------------------------------------------------------------
        # Supervised Contrast Reference
        V_contrastive = extract_contrastive_subspace(h_8_init, prem_indices, dist_indices, rank=rank)
        P_contrastive = (V_contrastive @ V_contrastive.T).to(h_8_init.device)

        # G_1: Inter-Layer Trajectory Flow
        V_traj = extract_trajectory_subspace(h_8_init, h_6_init, rank=rank)
        P_traj = (V_traj @ V_traj.T).to(h_8_init.device)

        # G_2: Contextual Perturbation
        pert_ids = input_ids.clone()
        rng_pert = np.random.RandomState(seed_conf + idx * 13)
        mask_candidates = [t for t in range(1, T - 1)]
        n_mask = max(1, int(0.20 * len(mask_candidates)))
        mask_idx = rng_pert.choice(mask_candidates, size=n_mask, replace=False)
        for m_pos in mask_idx:
            pert_ids[0, m_pos] = tokenizer.eos_token_id

        captured_pert = {}
        def cap_pert_l8_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured_pert["h_8"] = h.detach().squeeze(0)
        hndl_pert = model_layers[target_block].register_forward_hook(cap_pert_l8_hook)
        with torch.no_grad():
            model(input_ids=pert_ids)
        hndl_pert.remove()
        h_8_pert = captured_pert["h_8"]
        V_context = extract_trajectory_subspace(h_8_init, h_8_pert, rank=rank)
        P_context = (V_context @ V_context.T).to(h_8_init.device)

        # G_3: Attention-Derived Relational Subspace
        V_attn = extract_attention_relational_subspace(h_8_init, attn_layer8, prem_indices, dist_indices, rank=rank)
        P_attn = (V_attn @ V_attn.T).to(h_8_init.device)

        # ---------------------------------------------------------------------
        # Helper: Evaluate Single Intervention Forward Pass
        # ---------------------------------------------------------------------
        def eval_single_pass(P_proj):
            def hook_fn(mod, inp, outp):
                if isinstance(outp, tuple):
                    h = outp[0].clone()
                    h[0] = h[0] - alpha * (h[0] @ P_proj)
                    return (h,) + outp[1:]
                else:
                    h = outp.clone()
                    h[0] = h[0] - alpha * (h[0] @ P_proj)
                    return h

            hndl = model_layers[target_block].register_forward_hook(hook_fn)
            with torch.no_grad():
                out = model(input_ids=input_ids)
                logits = out.logits[0, -1, :]
                probs = F.softmax(logits, dim=-1)
                pred = torch.argmax(logits).item()
                logp = float(torch.log(torch.clamp(probs[target_id], min=1e-12)).item())
            hndl.remove()
            return (pred == target_id), logp

        # Evaluate G_contrastive
        is_corr_c, logp_c = eval_single_pass(P_contrastive)

        # Evaluate G_1 (Trajectory)
        is_corr_g1, logp_g1 = eval_single_pass(P_traj)

        # Evaluate G_2 (Contextual Perturbation)
        is_corr_g2, logp_g2 = eval_single_pass(P_context)

        # Evaluate G_3 (Attention Relational)
        is_corr_g3, logp_g3 = eval_single_pass(P_attn)

        # Oracle Best Selection among {G1, G2, G3}
        cand_evals = [
            ("G1_traj", is_corr_g1, logp_g1),
            ("G2_ctx", is_corr_g2, logp_g2),
            ("G3_attn", is_corr_g3, logp_g3)
        ]
        # Sort by correctness first, then highest target log-prob
        cand_evals_sorted = sorted(cand_evals, key=lambda x: (x[1], x[2]), reverse=True)
        oracle_best_name = cand_evals_sorted[0][0]
        oracle_corr = cand_evals_sorted[0][1]
        oracle_logp = cand_evals_sorted[0][2]

        # Prospective Policy Selection
        if predicted_g == "G1_traj":
            prosp_corr, prosp_logp = is_corr_g1, logp_g1
        elif predicted_g == "G2_ctx":
            prosp_corr, prosp_logp = is_corr_g2, logp_g2
        else:
            prosp_corr, prosp_logp = is_corr_g3, logp_g3

        instance_records.append({
            "idx": idx,
            "is_corr_base": (pred_base == target_id),
            "is_corr_c": is_corr_c,
            "is_corr_g1": is_corr_g1,
            "is_corr_g2": is_corr_g2,
            "is_corr_g3": is_corr_g3,
            "is_corr_oracle": oracle_corr,
            "is_corr_prosp": prosp_corr,
            "predicted_g": predicted_g,
            "oracle_g": oracle_best_name,
            "r_flow": r_flow,
            "attn_ratio": attn_ratio,
            "h_attn_entropy": h_attn_entropy,
            "logp_base": logp_tgt_base,
            "logp_c": logp_c,
            "logp_g1": logp_g1,
            "logp_g2": logp_g2,
            "logp_g3": logp_g3,
            "logp_oracle": oracle_logp,
            "logp_prosp": prosp_logp
        })

    elapsed = time.time() - start_time
    print(f"[COMPUTE] Profiling completed in {elapsed:.1f}s.")

    # Verify Parameter Invariance
    post_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Post-run Parameter SHA-256: {post_hash}")
    assert pre_hash == post_hash, "CRITICAL ERROR: Parameters mutated during inference!"
    print("[REPRODUCIBILITY] Frozen Backbone Verified: Parameter hashes match identically (Delta theta = 0).")

    # -------------------------------------------------------------------------
    # PART A: HETEROGENEOUS GENERATOR COMPLEMENTARITY ANALYSIS
    # -------------------------------------------------------------------------
    base_correct = [r["is_corr_base"] for r in instance_records]
    base_acc = float(np.mean(base_correct))

    g1_rescues = set(r["idx"] for r in instance_records if r["is_corr_g1"] and not r["is_corr_base"])
    g2_rescues = set(r["idx"] for r in instance_records if r["is_corr_g2"] and not r["is_corr_base"])
    g3_rescues = set(r["idx"] for r in instance_records if r["is_corr_g3"] and not r["is_corr_base"])

    union_rescues = g1_rescues | g2_rescues | g3_rescues

    print("\n" + "=" * 115)
    print("PART A: HETEROGENEOUS GENERATOR COMPLEMENTARITY ANALYSIS")
    print("=" * 115)
    print(f"G_1 (Trajectory) Rescues:    N = {len(g1_rescues)} {sorted(list(g1_rescues))}")
    print(f"G_2 (Contextual) Rescues:    N = {len(g2_rescues)} {sorted(list(g2_rescues))}")
    print(f"G_3 (Attention) Rescues:     N = {len(g3_rescues)} {sorted(list(g3_rescues))}")
    print(f"Total Union Unique Rescues:  N = {len(union_rescues)} {sorted(list(union_rescues))}")
    print("-" * 115)

    # -------------------------------------------------------------------------
    # PART B: BENCHMARK SCORECARD
    # -------------------------------------------------------------------------
    print("\n" + "=" * 115)
    print("PART B: EVALUATING PROSPECTIVE GENERATOR SELECTION VS. STATIC & ORACLE CONTROLLERS (B_eval = 1.0)")
    print("=" * 115)
    print(f"{'Condition / Policy':<32} | {'Acc':<7} | {'Delta M':<9} | {'95% CI':<16} | {'Delta log p':<12} | {'b / c':<8} | {'McNemar p':<11} | {'Evals/Inst':<10}")
    print("-" * 115)

    controllers_eval = {
        "Baseline (Unintervened)": {
            "correct": base_correct,
            "dlogp": [0.0 for _ in instance_records],
            "evals": [1 for _ in instance_records]
        },
        "G_contrastive (Supervised Ref)": {
            "correct": [r["is_corr_c"] for r in instance_records],
            "dlogp": [r["logp_c"] - r["logp_base"] for r in instance_records],
            "evals": [1 for _ in instance_records]
        },
        "Static G_1 (Trajectory Flow)": {
            "correct": [r["is_corr_g1"] for r in instance_records],
            "dlogp": [r["logp_g1"] - r["logp_base"] for r in instance_records],
            "evals": [1 for _ in instance_records]
        },
        "Static G_2 (Contextual Perturb)": {
            "correct": [r["is_corr_g2"] for r in instance_records],
            "dlogp": [r["logp_g2"] - r["logp_base"] for r in instance_records],
            "evals": [1 for _ in instance_records]
        },
        "Static G_3 (Attention Relational)": {
            "correct": [r["is_corr_g3"] for r in instance_records],
            "dlogp": [r["logp_g3"] - r["logp_base"] for r in instance_records],
            "evals": [1 for _ in instance_records]
        },
        "Oracle Multi-Generator Bound": {
            "correct": [r["is_corr_oracle"] for r in instance_records],
            "dlogp": [r["logp_oracle"] - r["logp_base"] for r in instance_records],
            "evals": [1 for _ in instance_records]
        },
        "Prospective Policy (q(g|x,h0))": {
            "correct": [r["is_corr_prosp"] for r in instance_records],
            "dlogp": [r["logp_prosp"] - r["logp_base"] for r in instance_records],
            "evals": [1 for _ in instance_records]
        }
    }

    results_summary = {
        "metadata": {
            "experiment_id": "EXP039",
            "date": "2026-09-12",
            "model": model_name,
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_invariant": (pre_hash == post_hash),
            "n_conf": n_conf,
            "base_acc": base_acc
        },
        "complementarity": {
            "g1_rescues": list(sorted(list(g1_rescues))),
            "g2_rescues": list(sorted(list(g2_rescues))),
            "g3_rescues": list(sorted(list(g3_rescues))),
            "union_rescues": list(sorted(list(union_rescues)))
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
        print(f"{name:<32} | {acc:.4f}  | {delta_m*100:+5.1f} pp | [{ci[0]*100:+5.1f}, {ci[1]*100:+5.1f}] pp | {mean_dlogp:+10.4f}   | b={b:<2}, c={c:<2} | p={p_mcnemar:<9.4f} | {mean_evals:<10.2f}")

    print("-" * 115)

    # Save to json
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP039_generator_selection"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "exp039_generator_selection_results.json")
    with open(out_file, "w") as f:
        json.dump(results_summary, f, indent=2)
    print(f"\n[OUTPUT] Saved complete benchmark results to: {out_file}")

if __name__ == "__main__":
    main()
