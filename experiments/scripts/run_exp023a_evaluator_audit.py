"""
EXP023-A: Counterfactual Evaluator Candidate Selection Audit (Development Screen)
Evaluates whether frozen E_CF can rank and select distractor candidates V_- autonomously
without ground-truth outcome knowledge under O5 contrastive hard gating at Layer 8.

Pipeline:
  H -> G -> {V_0, V_1, V_2, V_3} -> E_CF^frozen -> V* -> O5 -> q

Evaluator E_CF (Frozen from EXP013):
  d_pos = JS(q_b, q_p)
  d_neg = JS(q_b, q_n)
  e_cf = d_pos - 0.5 * d_neg
  k* = argmin_k e_cf(V_k)

Baselines Compared:
  - Identity (I)
  - Fixed Candidate (V_0: top SVD singular vectors)
  - Random Candidate (uniform random from {0, 1, 2, 3})
  - E_CF Selected Candidate
  - Oracle Upper Bound (outcome-selected candidate)

Dataset: BENCH-002-NL (Development Split N=20, dev_seed=123)
Model: Frozen GPT-2 (124M, Delta_theta = 0)
"""

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["USE_TF"] = "0"

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

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def js_divergence(p, q):
    """Calculates Jensen-Shannon divergence across vocabulary."""
    m = 0.5 * (p + q)
    kl_pm = F.kl_div(torch.log(torch.clamp(m, min=1e-12)), torch.clamp(p, min=1e-12), reduction="batchmean")
    kl_qm = F.kl_div(torch.log(torch.clamp(m, min=1e-12)), torch.clamp(q, min=1e-12), reduction="batchmean")
    return float((0.5 * (kl_pm + kl_qm)).item())

def construct_contrastive_subspaces(h_premise, h_distractor, rank=2, K=4):
    """
    Oracle-free construction of V_+ (target) and V_- candidates (distractor)
    from premise and distractor representation segments at Layer 8.
    """
    # 1. Target Subspace V_+ from premise representations
    h_p_centered = h_premise - torch.mean(h_premise, dim=0, keepdim=True)
    _, _, Vh_p = torch.linalg.svd(h_p_centered, full_matrices=False)
    V_plus = Vh_p[:rank, :].T  # [d_model, rank]

    # 2. Distractor Subspaces V_- from distractor representations
    h_d_centered = h_distractor - torch.mean(h_distractor, dim=0, keepdim=True)
    _, _, Vh_d = torch.linalg.svd(h_d_centered, full_matrices=False)
    max_components = Vh_d.shape[0]

    cand_V_minus = []
    # Candidate 0: Top 2 singular vectors
    cand_V_minus.append(Vh_d[:rank, :].T)
    # Candidate 1: Singular vectors (1, 2)
    idx1 = [1, min(2, max_components - 1)]
    cand_V_minus.append(Vh_d[idx1, :].T)
    # Candidate 2: Singular vectors (0, 2)
    idx2 = [0, min(2, max_components - 1)]
    cand_V_minus.append(Vh_d[idx2, :].T)
    # Candidate 3: Singular vectors (0, 3) or (2, 3)
    idx3 = [min(2, max_components - 2), min(3, max_components - 1)] if max_components >= 4 else [0, 1]
    cand_V_minus.append(Vh_d[idx3, :].T)

    return V_plus, cand_V_minus[:K]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_dev", type=int, default=20, help="Number of development instances")
    parser.add_argument("--dev_seed", type=int, default=123, help="Seed for development dataset")
    parser.add_argument("--layer", type=int, default=8, help="Locked target layer")
    parser.add_argument("--alpha", type=float, default=0.25, help="Locked operator strength")
    args = parser.parse_args()

    print("=" * 115)
    print("EXP023-A: COUNTERFACTUAL EVALUATOR CANDIDATE SELECTION AUDIT")
    print(f"Model: Frozen GPT-2 (124M) | Layer {args.layer} (Block {args.layer - 1}) | alpha = {args.alpha} | N_dev={args.n_dev}, Seed={args.dev_seed}")
    print("Selection: Frozen E_CF (d_pos - 0.5 * d_neg) vs. Random vs. Fixed (V_0) vs. Oracle Upper Bound")
    print("=" * 115)

    np.random.seed(args.dev_seed)
    torch.manual_seed(args.dev_seed)
    start_time = time.time()

    # Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")

    dataset = generate_bench_002_nl(n_instances=args.n_dev, seed=args.dev_seed)
    print(f"[DATASET] Loaded {len(dataset)} development instances.")

    layer_idx = args.layer
    block_idx = layer_idx - 1
    rank = 2
    K = 4

    # Result trackers
    m_identity = []
    m_fixed_v0 = []
    m_random = []
    m_ecf = []
    m_oracle = []

    pref_identity = []
    pref_fixed_v0 = []
    pref_random = []
    pref_ecf = []
    pref_oracle = []

    delta_logp_ecf = []
    delta_margin_ecf = []

    ecf_oracle_agreements = []
    spearman_rhos = []
    kendall_taus = []

    total_forwards = 0
    print(f"\nEvaluating candidate ranking & selection across {len(dataset)} instances...")

    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        pos_text = inst["pos"]
        neg_text = inst["neg"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]

        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]

        inputs_base = tokenizer(base_text, return_tensors="pt")
        inputs_pos = tokenizer(pos_text, return_tensors="pt")
        inputs_neg = tokenizer(neg_text, return_tensors="pt")

        # 1. Identity Forward Pass on Base
        with torch.no_grad():
            out_base = model(**inputs_base, output_hidden_states=True)
            total_forwards += 1

        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred_id = torch.argmax(base_logits).item()
        base_corr = (base_pred_id == target_id)
        base_pref = (base_probs[target_id].item() > base_probs[dist_id].item())
        base_logp = float(torch.log(base_probs[target_id] + 1e-12).item())
        base_margin = base_probs[target_id].item() - base_probs[dist_id].item()

        m_identity.append(base_corr)
        pref_identity.append(base_pref)

        # Extract native Layer 8 representations
        h_l = out_base.hidden_states[layer_idx][0]  # [seq_len, d_model]
        seq_len = h_l.shape[0]

        # Extract premise & distractor tokens
        idx_distractor_str = base_text.index(" Distractor:")
        idx_query_str = base_text.index(" Question:")
        text_premise = base_text[:idx_distractor_str]
        text_distractor = base_text[idx_distractor_str:idx_query_str]

        len_premise = len(tokenizer.encode(text_premise))
        len_distractor = len(tokenizer.encode(text_distractor))

        h_premise = h_l[:len_premise]
        h_dist = h_l[len_premise : len_premise + len_distractor]

        # Oracle-Free candidate generation
        V_plus, cand_V_minus_list = construct_contrastive_subspaces(h_premise, h_dist, rank=rank, K=K)

        cand_results = []

        # Evaluate each candidate under O5
        for k_idx, V_minus in enumerate(cand_V_minus_list):
            # Define dynamic hook for candidate k (handles variable sequence lengths)
            def hook_fn(module, input, output, V_m=V_minus, V_p=V_plus):
                h_curr = output[0].clone()
                h_token = h_curr[0]
                z_m = torch.matmul(h_token, V_m)
                z_p = torch.matmul(h_token, V_p)
                d_curr = torch.norm(z_m, dim=-1) - torch.norm(z_p, dim=-1)
                g_curr = (d_curr > 0.0).float().unsqueeze(-1)
                lin_e = torch.sum(torch.norm(z_m, dim=-1) ** 2).item()
                gat_e = torch.sum((g_curr.squeeze() ** 2) * (torch.norm(z_m, dim=-1) ** 2)).item()
                s_curr = float(np.sqrt(lin_e / max(gat_e, 1e-8)))
                h_proj = h_token - args.alpha * s_curr * g_curr * torch.matmul(z_m, V_m.T)
                return (h_proj.unsqueeze(0), *output[1:])

            # Forward passes on base, pos, neg
            handle = model.transformer.h[block_idx].register_forward_hook(hook_fn)
            with torch.no_grad():
                out_b = model(**inputs_base)
                out_p = model(**inputs_pos)
                out_n = model(**inputs_neg)
                total_forwards += 3
            handle.remove()

            logits_b = out_b.logits[0, -1]
            logits_p = out_p.logits[0, -1]
            logits_n = out_n.logits[0, -1]

            probs_b = F.softmax(logits_b, dim=-1)
            probs_p = F.softmax(logits_p, dim=-1)
            probs_n = F.softmax(logits_n, dim=-1)

            pred_id_b = torch.argmax(logits_b).item()
            c_corr = (pred_id_b == target_id)
            c_pref = (probs_b[target_id].item() > probs_b[dist_id].item())
            c_p_target = probs_b[target_id].item()
            c_margin = probs_b[target_id].item() - probs_b[dist_id].item()
            c_logp = float(torch.log(probs_b[target_id] + 1e-12).item())

            # Counterfactual evaluator score e_cf = d_pos - 0.5 * d_neg
            d_pos = js_divergence(probs_b.unsqueeze(0), probs_p.unsqueeze(0))
            d_neg = js_divergence(probs_b.unsqueeze(0), probs_n.unsqueeze(0))
            e_cf = d_pos - 0.5 * d_neg

            cand_results.append({
                "k_idx": k_idx,
                "corr": c_corr,
                "pref": c_pref,
                "p_target": c_p_target,
                "margin": c_margin,
                "logp": c_logp,
                "e_cf": e_cf,
                "d_pos": d_pos,
                "d_neg": d_neg
            })

        # Selection rules:
        # 1. Fixed Candidate (k=0)
        res_v0 = cand_results[0]
        m_fixed_v0.append(res_v0["corr"])
        pref_fixed_v0.append(res_v0["pref"])

        # 2. Random Candidate (random k in {0..K-1})
        rand_k = np.random.randint(0, K)
        res_rand = cand_results[rand_k]
        m_random.append(res_rand["corr"])
        pref_random.append(res_rand["pref"])

        # 3. Counterfactual Evaluator Selection: argmin e_cf
        ecf_scores = [c["e_cf"] for c in cand_results]
        best_ecf_k = int(np.argmin(ecf_scores))
        res_ecf = cand_results[best_ecf_k]
        m_ecf.append(res_ecf["corr"])
        pref_ecf.append(res_ecf["pref"])
        delta_logp_ecf.append(res_ecf["logp"] - base_logp)
        delta_margin_ecf.append(res_ecf["margin"] - base_margin)

        # 4. Oracle Upper Bound: argmax p_target (or any correct)
        target_probs = [c["p_target"] for c in cand_results]
        best_oracle_k = int(np.argmax(target_probs))
        oracle_any_corr = any([c["corr"] for c in cand_results])
        oracle_any_pref = any([c["pref"] for c in cand_results])
        m_oracle.append(oracle_any_corr)
        pref_oracle.append(oracle_any_pref)

        # Agreement & Ranking metrics
        is_exact_agreement = (best_ecf_k == best_oracle_k) or (res_ecf["corr"] and any([c["corr"] for c in cand_results]))
        ecf_oracle_agreements.append(is_exact_agreement)

        # Ranking correlation:
        # e_cf ranking (lowest e_cf is best -> rank 1)
        ecf_ranks = stats.rankdata(ecf_scores)  # smallest is 1
        # Oracle ranking (highest p_target is best -> rank 1)
        oracle_ranks = stats.rankdata([-p for p in target_probs])  # largest is 1

        if np.std(ecf_ranks) > 1e-8 and np.std(oracle_ranks) > 1e-8:
            rho, _ = stats.spearmanr(ecf_ranks, oracle_ranks)
            tau, _ = stats.kendalltau(ecf_ranks, oracle_ranks)
            if not np.isnan(rho):
                spearman_rhos.append(float(rho))
            if not np.isnan(tau):
                kendall_taus.append(float(tau))

        if (idx + 1) % 5 == 0 or idx == len(dataset) - 1:
            print(f"  [Progress {idx + 1:2d}/{len(dataset)}] M_I={np.mean(m_identity):.2f} | "
                  f"M_V0={np.mean(m_fixed_v0):.2f} | M_Rand={np.mean(m_random):.2f} | "
                  f"M_ECF={np.mean(m_ecf):.2f} | M_Oracle={np.mean(m_oracle):.2f}")

    elapsed_time = time.time() - start_time
    post_hash = get_param_hash(model)
    print(f"\n[REPRODUCIBILITY] Post-run Parameter Hash: {post_hash}")
    assert pre_hash == post_hash, "Backbone weights modified!"

    # Aggregate Statistics
    acc_identity = float(np.mean(m_identity))
    acc_v0 = float(np.mean(m_fixed_v0))
    acc_rand = float(np.mean(m_random))
    acc_ecf = float(np.mean(m_ecf))
    acc_oracle = float(np.mean(m_oracle))

    p_identity = float(np.mean(pref_identity))
    p_v0 = float(np.mean(pref_fixed_v0))
    p_rand = float(np.mean(pref_random))
    p_ecf = float(np.mean(pref_ecf))
    p_oracle = float(np.mean(pref_oracle))

    headroom_ecf = acc_ecf - acc_identity
    headroom_oracle = acc_oracle - acc_identity
    recovery_ratio = float(headroom_ecf / max(headroom_oracle, 1e-8)) if headroom_oracle > 0 else 0.0

    mean_rho = float(np.mean(spearman_rhos)) if len(spearman_rhos) > 0 else 0.0
    mean_tau = float(np.mean(kendall_taus)) if len(kendall_taus) > 0 else 0.0
    agreement_rate = float(np.mean(ecf_oracle_agreements))
    mean_delta_logp = float(np.mean(delta_logp_ecf))
    mean_delta_margin = float(np.mean(delta_margin_ecf))

    audit_payload = {
        "metadata": {
            "experiment": "EXP023-A",
            "n_dev": args.n_dev,
            "seed": args.dev_seed,
            "layer": args.layer,
            "alpha": args.alpha,
            "rank": rank,
            "candidate_count": K,
            "total_forwards": total_forwards,
            "elapsed_seconds": round(elapsed_time, 2),
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_identical": (pre_hash == post_hash)
        },
        "performance_comparison": {
            "M_Identity": round(acc_identity, 4),
            "M_Fixed_V0": round(acc_v0, 4),
            "M_Random": round(acc_rand, 4),
            "M_ECF_Autonomous": round(acc_ecf, 4),
            "M_Oracle_UpperBound": round(acc_oracle, 4),
            "Delta_M_ECF_vs_Identity": round(headroom_ecf, 4),
            "Delta_M_ECF_vs_Random": round(acc_ecf - acc_rand, 4),
            "Delta_M_ECF_vs_Fixed": round(acc_ecf - acc_v0, 4),
            "Headroom_Recovery_Ratio": round(recovery_ratio, 4),
            "Pref_Identity": round(p_identity, 4),
            "Pref_Fixed_V0": round(p_v0, 4),
            "Pref_Random": round(p_rand, 4),
            "Pref_ECF": round(p_ecf, 4),
            "Pref_Oracle": round(p_oracle, 4),
            "Mean_Delta_logp_ECF": round(mean_delta_logp, 4),
            "Mean_Delta_Margin_ECF": round(mean_delta_margin, 4)
        },
        "evaluator_ranking_diagnostics": {
            "mean_spearman_rho": round(mean_rho, 4),
            "mean_kendall_tau": round(mean_tau, 4),
            "oracle_agreement_rate": round(agreement_rate, 4),
            "positive_correlation_fraction": round(float(np.mean([r > 0 for r in spearman_rhos])), 4) if len(spearman_rhos) > 0 else 0.0
        }
    }

    print("\n" + "=" * 115)
    print("EXP023-A DEVELOPMENT AUDIT SUMMARY")
    print("=" * 115)
    print(f"  M_Identity:              {acc_identity:.4f} | Pref: {p_identity:.4f}")
    print(f"  M_Fixed_V0:              {acc_v0:.4f} | Pref: {p_v0:.4f}")
    print(f"  M_Random:                {acc_rand:.4f} | Pref: {p_rand:.4f}")
    print(f"  M_ECF (Autonomous):      {acc_ecf:.4f} | Pref: {p_ecf:.4f} | Delta M vs I: {headroom_ecf:+.4f}")
    print(f"  M_Oracle (Upper Bound):  {acc_oracle:.4f} | Pref: {p_oracle:.4f} | Headroom Recovery: {recovery_ratio*100:.1f}%")
    print("-" * 115)
    print(f"  Candidate Ranking Spearman rho: {mean_rho:+.4f}")
    print(f"  Candidate Ranking Kendall tau:  {mean_tau:+.4f}")
    print(f"  Oracle Candidate Agreement:     {agreement_rate*100:.1f}%")
    print(f"  Mean Delta log p (ECF):         {mean_delta_logp:+.4f}")
    print(f"  Mean Delta Margin (ECF):        {mean_delta_margin:+.4f}")
    print("=" * 115)

    out_dir = "experiments/runs/EXP023_ecf_selection"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp023a_evaluator_audit_results.json")
    with open(out_path, "w") as f:
        json.dump(audit_payload, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
