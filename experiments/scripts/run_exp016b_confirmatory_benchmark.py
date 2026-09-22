"""
EXP016-B: Confirmatory Single-Layer Benchmark (Layer 8)
Confirmatory evaluation of native G4_sparse dictionary candidates under P_0.25 at Layer 8.
Model: Frozen GPT-2 (124M, Delta_theta = 0)
Dataset: BENCH-002-NL (Confirmatory split N=100, seed=42)
Single Pre-Registered Confirmatory Hypothesis:
  H1: Delta M = M_Oracle,L8 - M_Identity > 0, with CI_95% > 0 and exact p < 0.05.
"""

import os
import sys
import time
import json
import hashlib
import argparse
import numpy as np
from scipy import stats
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl
from scbi.generators.activation_cluster import (
    generate_g4_sparse,
    compute_candidate_quality
)

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def compute_kl_divergence(p_logits, q_logits):
    p_probs = F.softmax(p_logits, dim=-1)
    q_probs = F.softmax(q_logits, dim=-1)
    q_probs = torch.clamp(q_probs, min=1e-12)
    p_probs = torch.clamp(p_probs, min=1e-12)
    return float(torch.sum(p_probs * (torch.log(p_probs) - torch.log(q_probs))).item())

def compute_topk_overlap(p_logits, q_logits, k=10):
    topk_p = set(torch.topk(p_logits, k=k).indices.tolist())
    topk_q = set(torch.topk(q_logits, k=k).indices.tolist())
    return len(topk_p.intersection(topk_q)) / float(k)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_instances", type=int, default=100, help="Number of benchmark instances")
    parser.add_argument("--seed", type=int, default=42, help="Seed for benchmark dataset")
    parser.add_argument("--layer", type=int, default=8, help="Locked target layer")
    parser.add_argument("--alpha", type=float, default=0.25, help="Locked operator strength")
    args = parser.parse_args()

    print("=" * 95)
    print("EXP016-B: CONFIRMATORY SINGLE-LAYER BENCHMARK (LAYER 8)")
    print(f"Model: Frozen GPT-2 (124M) | Layer {args.layer} (Block {args.layer - 1}) | P_0.25 | N={args.n_instances}, Seed={args.seed}")
    print("Candidate Generator: Native G4_sparse (K=4, rank=2) | Single Pre-Registered Confirmatory Test")
    print("=" * 95)

    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    start_time = time.time()

    # 1. Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")

    # 2. Load BENCH-002-NL Confirmatory Dataset (Seed 42)
    dataset = generate_bench_002_nl(n_instances=args.n_instances, seed=args.seed)
    print(f"[DATASET] Loaded {len(dataset)} confirmatory benchmark instances.")

    layer_idx = args.layer
    block_idx = layer_idx - 1  # Block 7 for Layer 8
    rank = 2
    K = 4

    # Containers for instance-level tracking
    identity_correct = []
    identity_prefs = []

    oracle_correct = []
    oracle_prefs = []

    rand_cand_correct = []
    rand_cand_prefs = []

    rand_ortho_correct = []
    rand_ortho_prefs = []

    instance_displacements = []
    instance_kls = []
    instance_overlaps = []

    locality_records = []
    diversity_records = []
    stability_records = []

    total_forwards = 0

    print(f"\nStarting confirmatory execution across N={len(dataset)} instances...")

    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]

        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]
        inputs_base = tokenizer(base_text, return_tensors="pt")

        # 1. Identity Baseline Forward Pass
        with torch.no_grad():
            out_base = model(**inputs_base, output_hidden_states=True)
            total_forwards += 1

        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred_id = torch.argmax(base_logits).item()
        base_corr = (base_pred_id == target_id)
        base_pref = (base_probs[target_id].item() > base_probs[dist_id].item())

        identity_correct.append(base_corr)
        identity_prefs.append(base_pref)

        # 2. Extract Native Layer 8 Hidden State
        h_l = out_base.hidden_states[layer_idx][0]  # [seq_len, d_model]
        h_l_norm = torch.norm(h_l).item()

        # Generate Native G4 Sparse Candidates
        cand_V_list = generate_g4_sparse(h_l, rank=rank, K=K)
        q_metrics = compute_candidate_quality(h_l, cand_V_list, rank=rank)

        locality_records.append(q_metrics["locality"])
        diversity_records.append(q_metrics["diversity"])
        stability_records.append(q_metrics["stability"])

        cand_corrs = []
        cand_prefs = []
        cand_disps = []
        cand_kls = []
        cand_overlaps = []

        # 3. Evaluate Each Candidate Subspace
        for V in cand_V_list:
            proj_norm = torch.norm(torch.matmul(h_l, V)).item()
            disp = args.alpha * (proj_norm / max(h_l_norm, 1e-8))
            cand_disps.append(disp)

            def hook_fn(module, input, output):
                h = output[0].clone()
                h_proj = h - args.alpha * torch.matmul(torch.matmul(h, V), V.T)
                return (h_proj, *output[1:])

            handle = model.transformer.h[block_idx].register_forward_hook(hook_fn)
            with torch.no_grad():
                o_cand = model(**inputs_base)
                total_forwards += 1
            handle.remove()

            c_logits = o_cand.logits[0, -1]
            c_probs = F.softmax(c_logits, dim=-1)
            c_pred_id = torch.argmax(c_logits).item()
            cand_corrs.append(c_pred_id == target_id)
            cand_prefs.append(c_probs[target_id].item() > c_probs[dist_id].item())

            kl = compute_kl_divergence(base_logits, c_logits)
            overlap = compute_topk_overlap(base_logits, c_logits, k=10)
            cand_kls.append(kl)
            cand_overlaps.append(overlap)

        oracle_c = any(cand_corrs)
        oracle_p = any(cand_prefs)
        oracle_correct.append(oracle_c)
        oracle_prefs.append(oracle_p)

        # Random candidate selection from pool
        rk = np.random.randint(0, len(cand_corrs))
        rand_cand_correct.append(cand_corrs[rk])
        rand_cand_prefs.append(cand_prefs[rk])

        # Random Orthogonal Subspace Control
        d_model = h_l.shape[-1]
        rand_mat = torch.randn(d_model, rank)
        V_rand, _ = torch.linalg.qr(rand_mat)

        def rand_hook_fn(module, input, output):
            h = output[0].clone()
            h_proj = h - args.alpha * torch.matmul(torch.matmul(h, V_rand), V_rand.T)
            return (h_proj, *output[1:])

        handle_rand = model.transformer.h[block_idx].register_forward_hook(rand_hook_fn)
        with torch.no_grad():
            o_rand = model(**inputs_base)
            total_forwards += 1
        handle_rand.remove()

        r_logits = o_rand.logits[0, -1]
        r_probs = F.softmax(r_logits, dim=-1)
        r_pred_id = torch.argmax(r_logits).item()
        rand_ortho_correct.append(r_pred_id == target_id)
        rand_ortho_prefs.append(r_probs[target_id].item() > r_probs[dist_id].item())

        instance_displacements.append(float(np.mean(cand_disps)))
        instance_kls.append(float(np.mean(cand_kls)))
        instance_overlaps.append(float(np.mean(cand_overlaps)))

        if (idx + 1) % 10 == 0 or (idx + 1) == len(dataset):
            print(f"  Processed {idx + 1}/{len(dataset)} instances...")

    elapsed_time = time.time() - start_time
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "CRITICAL: Model parameter hash changed during evaluation!"

    # 4. Statistical Analysis
    m_identity = float(np.mean(identity_correct))
    m_oracle = float(np.mean(oracle_correct))
    m_rand_cand = float(np.mean(rand_cand_correct))
    m_rand_ortho = float(np.mean(rand_ortho_correct))

    pref_identity = float(np.mean(identity_prefs))
    pref_oracle = float(np.mean(oracle_prefs))
    pref_rand_cand = float(np.mean(rand_cand_prefs))
    pref_rand_ortho = float(np.mean(rand_ortho_prefs))

    delta_m_oracle = m_oracle - m_identity
    delta_m_rand = m_rand_cand - m_identity
    spread_oracle_rand = m_oracle - m_rand_cand

    # Paired Contingency Table: Identity vs. Oracle
    # b: Identity=0, Oracle=1 (wins)
    # c: Identity=1, Oracle=0 (losses)
    wins_b = sum(1 for i, o in zip(identity_correct, oracle_correct) if (not i and o))
    losses_c = sum(1 for i, o in zip(identity_correct, oracle_correct) if (i and not o))
    ties_a = sum(1 for i, o in zip(identity_correct, oracle_correct) if (i and o))
    ties_d = sum(1 for i, o in zip(identity_correct, oracle_correct) if (not i and not o))
    n_disc = wins_b + losses_c

    # Exact paired binomial test
    if n_disc > 0:
        p_exact_one_sided = float(stats.binomtest(wins_b, n_disc, 0.5, alternative="greater").pvalue)
        p_exact_two_sided = float(stats.binomtest(wins_b, n_disc, 0.5, alternative="two-sided").pvalue)
    else:
        p_exact_one_sided = 1.0
        p_exact_two_sided = 1.0

    # 10,000 Bootstrap Resamples for CI
    n_boot = 10000
    boot_diffs = []
    id_arr = np.array(identity_correct, dtype=float)
    or_arr = np.array(oracle_correct, dtype=float)
    n_samples = len(dataset)

    for _ in range(n_boot):
        b_idx = np.random.choice(n_samples, size=n_samples, replace=True)
        boot_diffs.append(np.mean(or_arr[b_idx]) - np.mean(id_arr[b_idx]))

    ci_lower = float(np.percentile(boot_diffs, 2.5))
    ci_upper = float(np.percentile(boot_diffs, 97.5))

    # Diagnostics Aggregates
    mean_displacement = float(np.mean(instance_displacements))
    mean_kl = float(np.mean(instance_kls))
    mean_overlap = float(np.mean(instance_overlaps))
    mean_locality = float(np.mean(locality_records))
    mean_diversity = float(np.mean(diversity_records))
    mean_stability = float(np.mean(stability_records))

    # Confirmatory Gate Decision
    gate1_passed = (delta_m_oracle > 0) and (ci_lower > 0) and (p_exact_one_sided < 0.05)

    results_payload = {
        "metadata": {
            "experiment": "EXP016-B",
            "model": "gpt2 (124M)",
            "layer": layer_idx,
            "block_idx": block_idx,
            "operator": "P_0.25",
            "generator": "G4_sparse (native)",
            "n_instances": args.n_instances,
            "seed": args.seed,
            "total_forwards": total_forwards,
            "elapsed_seconds": round(elapsed_time, 2),
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_identical": (pre_hash == post_hash)
        },
        "performance": {
            "M_Identity": round(m_identity, 4),
            "M_Oracle": round(m_oracle, 4),
            "Delta_M_Oracle": round(delta_m_oracle, 4),
            "M_RandCand": round(m_rand_cand, 4),
            "Delta_M_RandCand": round(delta_m_rand, 4),
            "M_RandOrtho": round(m_rand_ortho, 4),
            "Spread_Oracle_RandCand": round(spread_oracle_rand, 4),
            "Pref_Identity": round(pref_identity, 4),
            "Pref_Oracle": round(pref_oracle, 4),
            "Pref_RandCand": round(pref_rand_cand, 4),
            "Pref_RandOrtho": round(pref_rand_ortho, 4)
        },
        "statistical_inference": {
            "contingency_table": {
                "ties_both_correct_a": ties_a,
                "wins_oracle_only_b": wins_b,
                "losses_identity_only_c": losses_c,
                "ties_both_fail_d": ties_d,
                "n_discordant": n_disc
            },
            "p_exact_one_sided": round(p_exact_one_sided, 5),
            "p_exact_two_sided": round(p_exact_two_sided, 5),
            "ci95_delta_m": [round(ci_lower, 4), round(ci_upper, 4)],
            "gate1_passed": gate1_passed
        },
        "diagnostics": {
            "mean_displacement": round(mean_displacement, 4),
            "mean_kl_divergence": round(mean_kl, 4),
            "mean_top10_overlap": round(mean_overlap, 4),
            "mean_locality": round(mean_locality, 4),
            "mean_diversity": round(mean_diversity, 4),
            "mean_stability": round(mean_stability, 4)
        }
    }

    print("\n" + "=" * 95)
    print("EXP016-B CONFIRMATORY RESULTS: LAYER 8 BENCHMARK")
    print("=" * 95)
    print(f"  M_Identity:              {m_identity:.4f} ({int(m_identity * args.n_instances)}/{args.n_instances})")
    print(f"  M_Oracle (Layer 8):      {m_oracle:.4f} ({int(m_oracle * args.n_instances)}/{args.n_instances})")
    print(f"  Delta M_Oracle:          {delta_m_oracle:+.4f}")
    print(f"  M_RandCand:              {m_rand_cand:.4f} (Delta: {delta_m_rand:+.4f})")
    print(f"  M_RandOrtho:             {m_rand_ortho:.4f}")
    print(f"  Oracle-Random Spread:    {spread_oracle_rand:+.4f}")
    print(f"  Pref_Oracle vs Identity: {pref_oracle:.4f} vs. {pref_identity:.4f}")
    print("-" * 95)
    print(f"  Contingency Table (b/c): Wins b={wins_b}, Losses c={losses_c} (n_disc={n_disc})")
    print(f"  Exact Binomial p (one):  {p_exact_one_sided:.5f} (two-sided: {p_exact_two_sided:.5f})")
    print(f"  95% Bootstrap CI:        [{ci_lower:+.4f}, {ci_upper:+.4f}]")
    print(f"  Mean Displacement (D_8): {mean_displacement:.4f}")
    print(f"  Mean KL Divergence:      {mean_kl:.4f}")
    print(f"  Mean Top-10 Overlap:     {mean_overlap:.4f}")
    print(f"  Gate 1 Headroom Status:  {'PASSED' if gate1_passed else 'FAILED'}")
    print("=" * 95)
    print(f"[REPRODUCIBILITY] Pre-run SHA-256 == Post-run SHA-256: {pre_hash == post_hash} (Weight Invariance Guaranteed)")
    print(f"[RUNTIME] Completed {total_forwards} forward passes in {elapsed_time:.2f}s.")

    out_dir = "experiments/runs/EXP016_layer_localization"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp016b_confirmatory_results.json")
    with open(out_path, "w") as f:
        json.dump(results_payload, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
