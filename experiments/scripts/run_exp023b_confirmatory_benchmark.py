"""
EXP023-B: Confirmatory End-to-End Autonomous SCBI Benchmark
Confirmatory evaluation of frozen E_CF candidate selection under O5 contrastive hard gating
on fresh, unseen benchmark split (BENCH-002-NL, N=100, Seed 84).

Autonomous Inference Pipeline (Zero Outcome Knowledge):
  H -> G -> {V_0, V_1, V_2, V_3} -> E_CF^frozen -> V* -> O5 -> q

Frozen Evaluator Formula (EXP013 Lock):
  d_pos = JS(q_b, q_p)
  d_neg = JS(q_b, q_n)
  e_cf = d_pos - 0.5 * d_neg
  k* = argmin_k e_cf(V_k)

Primary Confirmatory Endpoint:
  Delta M = M_ECF - M_Identity > 0, exact p < 0.05, 95% bootstrap CI > 0

Secondary Mechanistic Endpoint:
  H_mech: Delta log p(y_correct)_ECF > 0, 95% bootstrap CI > 0
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
    parser.add_argument("--n_conf", type=int, default=100, help="Number of confirmatory benchmark instances")
    parser.add_argument("--conf_seed", type=int, default=84, help="Fresh unseen seed for confirmatory dataset")
    parser.add_argument("--layer", type=int, default=8, help="Locked target layer")
    parser.add_argument("--alpha", type=float, default=0.25, help="Locked operator strength")
    args = parser.parse_args()

    print("=" * 115)
    print("EXP023-B: CONFIRMATORY END-TO-END AUTONOMOUS SCBI BENCHMARK")
    print(f"Model: Frozen GPT-2 (124M) | Layer {args.layer} (Block {args.layer - 1}) | alpha = {args.alpha} | N_conf={args.n_conf}, Seed={args.conf_seed} (FRESH UNSEEN)")
    print("Autonomous Candidate Selection: Frozen E_CF (d_pos - 0.5 * d_neg) under O5 Contrastive Hard Gate")
    print("=" * 115)

    np.random.seed(args.conf_seed)
    torch.manual_seed(args.conf_seed)
    start_time = time.time()

    # Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")

    dataset = generate_bench_002_nl(n_instances=args.n_conf, seed=args.conf_seed)
    print(f"[DATASET] Loaded {len(dataset)} confirmatory instances from fresh Seed {args.conf_seed}.")

    layer_idx = args.layer
    block_idx = layer_idx - 1
    rank = 2
    K = 4

    # Tracking lists
    records = {
        "identity_corr": [],
        "identity_pref": [],
        "fixed_v0_corr": [],
        "fixed_v0_pref": [],
        "rand_cand_corr": [],
        "rand_cand_pref": [],
        "ecf_corr": [],
        "ecf_pref": [],
        "oracle_corr": [],
        "oracle_pref": [],
        "rand_ortho_corr": [],
        "delta_logp_ecf": [],
        "delta_margin_ecf": [],
        "rank_shift_ecf": [],
        "kl_ecf": [],
        "overlap_ecf": [],
        "comp_identity": [],
        "comp_ecf": [],
        "comp_oracle": [],
        "ecf_oracle_agreement": [],
        "spearman_rho": [],
        "kendall_tau": [],
        "selected_k_dist": [0] * K
    }

    total_forwards = 0
    print(f"\nExecuting autonomous SCBI pipeline across {len(dataset)} confirmatory instances...")

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

        # 1. Identity Forward Pass
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

        sorted_base = torch.argsort(base_logits, descending=True)
        base_rank = (sorted_base == target_id).nonzero().item() + 1

        # Identity competition
        other_probs_id = base_probs.clone()
        other_probs_id[target_id] = -1.0
        other_probs_id[dist_id] = -1.0
        p_max_other_id = torch.max(other_probs_id).item()
        if base_probs[dist_id].item() > base_probs[target_id].item():
            comp_id = "distractor_bias"
        elif base_probs[target_id].item() > p_max_other_id:
            comp_id = "clean_win"
        else:
            comp_id = "third_token_intrusion"

        records["identity_corr"].append(base_corr)
        records["identity_pref"].append(base_pref)
        records["comp_identity"].append(comp_id)

        # Extract native Layer 8 representations
        h_l = out_base.hidden_states[layer_idx][0]
        d_model = h_l.shape[-1]

        # Extract premise & distractor token ranges
        idx_distractor_str = base_text.index(" Distractor:")
        idx_query_str = base_text.index(" Question:")
        text_premise = base_text[:idx_distractor_str]
        text_distractor = base_text[idx_distractor_str:idx_query_str]

        len_premise = len(tokenizer.encode(text_premise))
        len_distractor = len(tokenizer.encode(text_distractor))

        h_premise = h_l[:len_premise]
        h_dist = h_l[len_premise : len_premise + len_distractor]

        # 2. Oracle-Free Candidate Subspaces
        V_plus, cand_V_minus_list = construct_contrastive_subspaces(h_premise, h_dist, rank=rank, K=K)

        cand_results = []

        # 3. Evaluate each candidate under O5
        for k_idx, V_minus in enumerate(cand_V_minus_list):
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
            c_p_dist = probs_b[dist_id].item()
            c_margin = c_p_target - c_p_dist
            c_logp = float(torch.log(probs_b[target_id] + 1e-12).item())

            sorted_c = torch.argsort(logits_b, descending=True)
            c_rank = (sorted_c == target_id).nonzero().item() + 1

            # Output-space competition for candidate
            other_p = probs_b.clone()
            other_p[target_id] = -1.0
            other_p[dist_id] = -1.0
            c_p_max_other = torch.max(other_p).item()

            if c_p_dist > c_p_target:
                c_comp = "distractor_bias"
            elif c_p_target > c_p_max_other:
                c_comp = "clean_win"
            else:
                c_comp = "third_token_intrusion"

            # Counterfactual evaluator score e_cf = d_pos - 0.5 * d_neg
            d_pos = js_divergence(probs_b.unsqueeze(0), probs_p.unsqueeze(0))
            d_neg = js_divergence(probs_b.unsqueeze(0), probs_n.unsqueeze(0))
            e_cf = d_pos - 0.5 * d_neg

            cand_results.append({
                "k_idx": k_idx,
                "corr": c_corr,
                "pref": c_pref,
                "p_target": c_p_target,
                "p_dist": c_p_dist,
                "margin": c_margin,
                "logp": c_logp,
                "rank": c_rank,
                "comp": c_comp,
                "e_cf": e_cf,
                "kl": compute_kl_divergence(base_logits, logits_b),
                "overlap": compute_topk_overlap(base_logits, logits_b, k=10)
            })

        # Selection Rules:
        # A. Fixed Candidate (Candidate 0)
        c0 = cand_results[0]
        records["fixed_v0_corr"].append(c0["corr"])
        records["fixed_v0_pref"].append(c0["pref"])

        # B. Random Candidate (Uniform pseudo-random choice from {0..K-1})
        rk = np.random.randint(0, K)
        crand = cand_results[rk]
        records["rand_cand_corr"].append(crand["corr"])
        records["rand_cand_pref"].append(crand["pref"])

        # C. Autonomous Counterfactual Selection: argmin e_cf
        ecf_scores = [c["e_cf"] for c in cand_results]
        best_ecf_k = int(np.argmin(ecf_scores))
        records["selected_k_dist"][best_ecf_k] += 1
        cecf = cand_results[best_ecf_k]

        records["ecf_corr"].append(cecf["corr"])
        records["ecf_pref"].append(cecf["pref"])
        records["delta_logp_ecf"].append(cecf["logp"] - base_logp)
        records["delta_margin_ecf"].append(cecf["margin"] - base_margin)
        records["rank_shift_ecf"].append(base_rank - cecf["rank"])
        records["kl_ecf"].append(cecf["kl"])
        records["overlap_ecf"].append(cecf["overlap"])
        records["comp_ecf"].append(cecf["comp"])

        # D. Oracle Upper Bound: argmax p_target (or any correct)
        target_probs = [c["p_target"] for c in cand_results]
        best_oracle_k = int(np.argmax(target_probs))
        corrs = [c["corr"] for c in cand_results]
        oracle_c = any(corrs)
        oracle_p = any([c["pref"] for c in cand_results])
        records["oracle_corr"].append(oracle_c)
        records["oracle_pref"].append(oracle_p)

        # Oracle competition
        coracle = cand_results[best_oracle_k]
        records["comp_oracle"].append(coracle["comp"])

        # Agreement & Ranking correlation
        is_agreement = (best_ecf_k == best_oracle_k) or (cecf["corr"] and oracle_c)
        records["ecf_oracle_agreement"].append(is_agreement)

        ecf_ranks = stats.rankdata(ecf_scores)
        oracle_ranks = stats.rankdata([-p for p in target_probs])
        if np.std(ecf_ranks) > 1e-8 and np.std(oracle_ranks) > 1e-8:
            rho, _ = stats.spearmanr(ecf_ranks, oracle_ranks)
            tau, _ = stats.kendalltau(ecf_ranks, oracle_ranks)
            if not np.isnan(rho):
                records["spearman_rho"].append(float(rho))
            if not np.isnan(tau):
                records["kendall_tau"].append(float(tau))

        # E. Random Orthogonal Subspace Control
        rand_mat = torch.randn(d_model, rank)
        V_rand, _ = torch.linalg.qr(rand_mat)

        def rand_hook_fn(module, input, output):
            h_curr = output[0].clone()
            h_token = h_curr[0]
            z_r = torch.matmul(h_token, V_rand)
            h_proj = h_token - args.alpha * torch.matmul(z_r, V_rand.T)
            return (h_proj.unsqueeze(0), *output[1:])

        h_rand = model.transformer.h[block_idx].register_forward_hook(rand_hook_fn)
        with torch.no_grad():
            o_rand = model(**inputs_base)
            total_forwards += 1
        h_rand.remove()

        r_logits = o_rand.logits[0, -1]
        r_pred_id = torch.argmax(r_logits).item()
        records["rand_ortho_corr"].append(r_pred_id == target_id)

        if (idx + 1) % 20 == 0 or idx == len(dataset) - 1:
            print(f"  [Progress {idx + 1:3d}/{len(dataset)}] M_I={np.mean(records['identity_corr']):.3f} | "
                  f"M_V0={np.mean(records['fixed_v0_corr']):.3f} | "
                  f"M_Rand={np.mean(records['rand_cand_corr']):.3f} | "
                  f"M_ECF={np.mean(records['ecf_corr']):.3f} | "
                  f"M_Oracle={np.mean(records['oracle_corr']):.3f} | "
                  f"Agreement={np.mean(records['ecf_oracle_agreement']):.1%}")

    elapsed_time = time.time() - start_time
    post_hash = get_param_hash(model)
    print(f"\n[REPRODUCIBILITY] Post-run Parameter Hash (SHA-256): {post_hash}")
    assert pre_hash == post_hash, "Backbone weights modified!"

    # =========================================================================
    # STATISTICAL INFERENCE (CONFIRMATORY ENDPOINTS)
    # =========================================================================
    N = len(dataset)
    m_identity = float(np.mean(records["identity_corr"]))
    m_ecf = float(np.mean(records["ecf_corr"]))
    m_oracle = float(np.mean(records["oracle_corr"]))
    m_rand_cand = float(np.mean(records["rand_cand_corr"]))
    m_fixed_v0 = float(np.mean(records["fixed_v0_corr"]))
    m_rand_ortho = float(np.mean(records["rand_ortho_corr"]))

    p_identity = float(np.mean(records["identity_pref"]))
    p_ecf = float(np.mean(records["ecf_pref"]))
    p_oracle = float(np.mean(records["oracle_pref"]))

    delta_m_ecf = m_ecf - m_identity
    headroom_oracle = m_oracle - m_identity
    headroom_recovery_ratio = float(delta_m_ecf / max(headroom_oracle, 1e-8)) if headroom_oracle > 0 else 0.0

    # 1. Primary McNemar Paired Test (ECF vs Identity)
    id_arr = np.array(records["identity_corr"], dtype=bool)
    ecf_arr = np.array(records["ecf_corr"], dtype=bool)

    ties_a = int(np.sum(id_arr & ecf_arr))
    wins_b = int(np.sum((~id_arr) & ecf_arr))
    losses_c = int(np.sum(id_arr & (~ecf_arr)))
    ties_d = int(np.sum((~id_arr) & (~ecf_arr)))
    n_disc = wins_b + losses_c

    if n_disc > 0:
        p_exact_one_sided = float(stats.binomtest(wins_b, n_disc, 0.5, alternative="greater").pvalue)
        p_exact_two_sided = float(stats.binomtest(wins_b, n_disc, 0.5, alternative="two-sided").pvalue)
    else:
        p_exact_one_sided = 1.0
        p_exact_two_sided = 1.0

    # 10,000-Resample Bootstrap for Delta M
    n_boot = 10000
    boot_delta_m = []
    for _ in range(n_boot):
        b_idx = np.random.choice(N, size=N, replace=True)
        boot_delta_m.append(np.mean(ecf_arr[b_idx]) - np.mean(id_arr[b_idx]))
    ci_delta_m_lower = float(np.percentile(boot_delta_m, 2.5))
    ci_delta_m_upper = float(np.percentile(boot_delta_m, 97.5))

    primary_passed = bool((delta_m_ecf > 0) and (ci_delta_m_lower > 0) and (p_exact_one_sided < 0.05))

    # 2. Secondary Mechanistic Hypothesis H_mech: Delta log p(y_correct) > 0
    delta_logps = np.array(records["delta_logp_ecf"])
    mean_delta_logp = float(np.mean(delta_logps))
    boot_logp = []
    for _ in range(n_boot):
        b_idx = np.random.choice(N, size=N, replace=True)
        boot_logp.append(np.mean(delta_logps[b_idx]))
    ci_logp_lower = float(np.percentile(boot_logp, 2.5))
    ci_logp_upper = float(np.percentile(boot_logp, 97.5))
    h_mech_supported = bool((mean_delta_logp > 0) and (ci_logp_lower > 0))

    # 3. Secondary Margin
    delta_margins = np.array(records["delta_margin_ecf"])
    mean_delta_margin = float(np.mean(delta_margins))
    boot_margin = []
    for _ in range(n_boot):
        b_idx = np.random.choice(N, size=N, replace=True)
        boot_margin.append(np.mean(delta_margins[b_idx]))
    ci_margin_lower = float(np.percentile(boot_margin, 2.5))
    ci_margin_upper = float(np.percentile(boot_margin, 97.5))

    # Output-Space Competition Frequencies
    comp_counts_id = {k: records["comp_identity"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}
    comp_counts_ecf = {k: records["comp_ecf"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}
    comp_counts_oracle = {k: records["comp_oracle"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}

    mean_rho = float(np.mean(records["spearman_rho"])) if len(records["spearman_rho"]) > 0 else 0.0
    mean_tau = float(np.mean(records["kendall_tau"])) if len(records["kendall_tau"]) > 0 else 0.0
    agreement_rate = float(np.mean(records["ecf_oracle_agreement"]))

    results_payload = {
        "metadata": {
            "experiment": "EXP023-B",
            "model": "gpt2 (124M)",
            "benchmark": "BENCH-002-NL",
            "conf_seed": args.conf_seed,
            "n_conf": args.n_conf,
            "layer": layer_idx,
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
            "M_Identity": round(m_identity, 4),
            "M_Fixed_V0": round(m_fixed_v0, 4),
            "M_Random_Cand": round(m_rand_cand, 4),
            "M_ECF_Autonomous": round(m_ecf, 4),
            "M_Oracle_UpperBound": round(m_oracle, 4),
            "M_RandOrtho_Control": round(m_rand_ortho, 4),
            "Delta_M_ECF_vs_Identity": round(delta_m_ecf, 4),
            "Delta_M_ECF_vs_Random": round(m_ecf - m_rand_cand, 4),
            "Delta_M_ECF_vs_Fixed": round(m_ecf - m_fixed_v0, 4),
            "Headroom_Recovery_Ratio": round(headroom_recovery_ratio, 4),
            "Pref_Identity": round(p_identity, 4),
            "Pref_ECF": round(p_ecf, 4),
            "Pref_Oracle": round(p_oracle, 4),
            "Mean_Delta_logp_ECF": round(mean_delta_logp, 4),
            "Mean_Delta_Margin_ECF": round(mean_delta_margin, 4),
            "Mean_Rank_Shift_ECF": round(float(np.mean(records["rank_shift_ecf"])), 4),
            "Mean_KL_ECF": round(float(np.mean(records["kl_ecf"])), 4),
            "Top10_Overlap_ECF": round(float(np.mean(records["overlap_ecf"])), 4),
            "Selected_Candidate_Distribution": records["selected_k_dist"]
        },
        "statistical_inference": {
            "primary_endpoint_autonomous_scbi": {
                "metric": "Delta M (M_ECF - M_Identity)",
                "delta_m": round(delta_m_ecf, 4),
                "contingency_table": {
                    "ties_both_correct_a": ties_a,
                    "wins_ecf_only_b": wins_b,
                    "losses_identity_only_c": losses_c,
                    "ties_both_fail_d": ties_d,
                    "n_discordant": n_disc
                },
                "p_exact_one_sided": round(p_exact_one_sided, 5),
                "p_exact_two_sided": round(p_exact_two_sided, 5),
                "ci95_delta_m": [round(ci_delta_m_lower, 4), round(ci_delta_m_upper, 4)],
                "autonomous_scbi_confirmed": primary_passed
            },
            "secondary_mechanistic_h_mech": {
                "hypothesis": "H_mech: Delta log p(y_correct)_ECF > 0",
                "mean_delta_logp": round(mean_delta_logp, 4),
                "ci95_delta_logp": [round(ci_logp_lower, 4), round(ci_logp_upper, 4)],
                "ci_excludes_zero": bool(ci_logp_lower > 0),
                "h_mech_supported": h_mech_supported
            },
            "secondary_margin": {
                "mean_delta_margin": round(mean_delta_margin, 4),
                "ci95_delta_margin": [round(ci_margin_lower, 4), round(ci_margin_upper, 4)]
            }
        },
        "evaluator_diagnostics": {
            "mean_spearman_rho": round(mean_rho, 4),
            "mean_kendall_tau": round(mean_tau, 4),
            "oracle_candidate_agreement": round(agreement_rate, 4),
            "positive_correlation_fraction": round(float(np.mean([r > 0 for r in records["spearman_rho"]])), 4) if len(records["spearman_rho"]) > 0 else 0.0
        },
        "output_space_competition_diagnostic": {
            "proportions": {
                "Identity": {k: round(v / N, 4) for k, v in comp_counts_id.items()},
                "ECF_Autonomous": {k: round(v / N, 4) for k, v in comp_counts_ecf.items()},
                "Oracle_UpperBound": {k: round(v / N, 4) for k, v in comp_counts_oracle.items()}
            }
        }
    }

    print("\n" + "=" * 115)
    print("EXP023-B CONFIRMATORY END-TO-END RESULTS SUMMARY (FRESH SEED 84, N=100)")
    print("=" * 115)
    print(f"  M_Identity:              {m_identity:.4f} ({int(m_identity*N)}/{N}) | Pref: {p_identity:.4f}")
    print(f"  M_Fixed_V0:              {m_fixed_v0:.4f} | RandCand: {m_rand_cand:.4f} | RandOrtho: {m_rand_ortho:.4f}")
    print(f"  M_ECF (Autonomous SCBI): {m_ecf:.4f} ({int(m_ecf*N)}/{N}) | Pref: {p_ecf:.4f}")
    print(f"  M_Oracle (Upper Bound):  {m_oracle:.4f} ({int(m_oracle*N)}/{N}) | Pref: {p_oracle:.4f}")
    print(f"  Headroom Recovery:       {headroom_recovery_ratio*100:.1f}% (Delta M_ECF: {delta_m_ecf:+.4f})")
    print("-" * 115)
    print("STATISTICAL INFERENCE:")
    print(f"  Primary Autonomous Delta M:     Delta M = {delta_m_ecf:+.4f}, 95% CI [{ci_delta_m_lower:+.4f}, {ci_delta_m_upper:+.4f}]")
    print(f"  McNemar Exact Binomial:         Wins b={wins_b}, Losses c={losses_c} (n_disc={n_disc}) | p_exact={p_exact_one_sided:.5f}")
    print(f"  Autonomous SCBI Status:         {'PASSED (AUTONOMOUS SCBI CONFIRMED)' if primary_passed else 'FAILED'}")
    print(f"  Secondary H_mech (Delta log p): Mean = {mean_delta_logp:+.4f}, 95% CI [{ci_logp_lower:+.4f}, {ci_logp_upper:+.4f}]")
    print(f"  H_mech Confirmation Status:     {'CONFIRMED' if h_mech_supported else 'NOT CONFIRMED'}")
    print(f"  Secondary Delta Margin:         Mean = {mean_delta_margin:+.4f}, 95% CI [{ci_margin_lower:+.4f}, {ci_margin_upper:+.4f}]")
    print("-" * 115)
    print("EVALUATOR CANDIDATE RANKING DIAGNOSTICS:")
    print(f"  Spearman rho: {mean_rho:+.4f} | Kendall tau: {mean_tau:+.4f} | Oracle Agreement: {agreement_rate*100:.1f}%")
    print(f"  Candidate Distribution (k=0..3): {records['selected_k_dist']}")
    print("-" * 115)
    print("OUTPUT-SPACE COMPETITION DIAGNOSTIC:")
    print(f"  Identity:        Clean Win: {comp_counts_id['clean_win']/N:.2f} | Distractor Bias: {comp_counts_id['distractor_bias']/N:.2f} | Third-Token Intrusion: {comp_counts_id['third_token_intrusion']/N:.2f}")
    print(f"  ECF Autonomous:  Clean Win: {comp_counts_ecf['clean_win']/N:.2f} | Distractor Bias: {comp_counts_ecf['distractor_bias']/N:.2f} | Third-Token Intrusion: {comp_counts_ecf['third_token_intrusion']/N:.2f}")
    print(f"  Oracle Upper:    Clean Win: {comp_counts_oracle['clean_win']/N:.2f} | Distractor Bias: {comp_counts_oracle['distractor_bias']/N:.2f} | Third-Token Intrusion: {comp_counts_oracle['third_token_intrusion']/N:.2f}")
    print("=" * 115)
    print(f"[REPRODUCIBILITY] Pre-run SHA-256 == Post-run SHA-256: {pre_hash == post_hash} (Weight Invariance Guaranteed)")
    print(f"[RUNTIME] Completed {total_forwards} forward passes in {elapsed_time:.2f}s.")

    out_dir = "experiments/runs/EXP023_ecf_selection"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp023b_confirmatory_results.json")
    with open(out_path, "w") as f:
        json.dump(results_payload, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
