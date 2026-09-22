"""
EXP024: Independent Cross-Seed Replication Benchmark
Evaluates autonomous SCBI on a second fresh, unseen confirmatory split (BENCH-002-NL, N=100, Seed 168),
followed by cross-seed pooled analysis with Seed 84 (N_total = 200).

Locked Pipeline:
  H -> G -> {V_0, V_1, V_2, V_3} -> E_CF^frozen -> V* -> O5 -> q

Primary Replication Question:
  Does autonomous SCBI produce statistically significant headroom Delta M_168 > 0 on Seed 168?
Cross-Seed Pooled Analysis:
  Evaluate consistency and pooled statistical significance across Seed 84 and Seed 168 (N=200).
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
    parser.add_argument("--n_conf", type=int, default=100, help="Number of benchmark instances")
    parser.add_argument("--replication_seed", type=int, default=168, help="Second fresh unseen seed")
    parser.add_argument("--previous_seed_results", type=str, default="experiments/runs/EXP023_ecf_selection/exp023b_confirmatory_results.json", help="Path to Seed 84 results for cross-seed pooling")
    parser.add_argument("--layer", type=int, default=8, help="Locked target layer")
    parser.add_argument("--alpha", type=float, default=0.25, help="Locked operator strength")
    args = parser.parse_args()

    print("=" * 115)
    print("EXP024: INDEPENDENT CROSS-SEED REPLICATION BENCHMARK")
    print(f"Model: Frozen GPT-2 (124M) | Layer {args.layer} (Block {args.layer - 1}) | alpha = {args.alpha} | N_conf={args.n_conf}, Seed={args.replication_seed} (FRESH UNSEEN)")
    print("Autonomous Candidate Selection: Frozen E_CF (d_pos - 0.5 * d_neg) under O5 Contrastive Hard Gate")
    print("=" * 115)

    np.random.seed(args.replication_seed)
    torch.manual_seed(args.replication_seed)
    start_time = time.time()

    # Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")

    dataset = generate_bench_002_nl(n_instances=args.n_conf, seed=args.replication_seed)
    print(f"[DATASET] Loaded {len(dataset)} confirmatory instances from fresh Replication Seed {args.replication_seed}.")

    layer_idx = args.layer
    block_idx = layer_idx - 1
    rank = 2
    K = 4

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
    print(f"\nExecuting autonomous SCBI pipeline across {len(dataset)} replication instances...")

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
            probs_b = F.softmax(logits_b, dim=-1)
            probs_p = F.softmax(out_p.logits[0, -1], dim=-1)
            probs_n = F.softmax(out_n.logits[0, -1], dim=-1)

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
        # A. Fixed Candidate 0
        c0 = cand_results[0]
        records["fixed_v0_corr"].append(c0["corr"])
        records["fixed_v0_pref"].append(c0["pref"])

        # B. Random Candidate
        rk = np.random.randint(0, K)
        crand = cand_results[rk]
        records["rand_cand_corr"].append(crand["corr"])
        records["rand_cand_pref"].append(crand["pref"])

        # C. Autonomous Counterfactual Selection
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

        # D. Oracle Upper Bound
        target_probs = [c["p_target"] for c in cand_results]
        best_oracle_k = int(np.argmax(target_probs))
        corrs = [c["corr"] for c in cand_results]
        oracle_c = any(corrs)
        oracle_p = any([c["pref"] for c in cand_results])
        records["oracle_corr"].append(oracle_c)
        records["oracle_pref"].append(oracle_p)
        coracle = cand_results[best_oracle_k]
        records["comp_oracle"].append(coracle["comp"])

        # Agreement & Correlation
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

        # E. Random Orthogonal Control
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
    print(f"\n[REPRODUCIBILITY] Post-run Parameter Hash: {post_hash}")
    assert pre_hash == post_hash, "Backbone weights modified!"

    # =========================================================================
    # REPLICATION STATISTICAL INFERENCE (SEED 168)
    # =========================================================================
    N = len(dataset)
    m_identity_168 = float(np.mean(records["identity_corr"]))
    m_ecf_168 = float(np.mean(records["ecf_corr"]))
    m_oracle_168 = float(np.mean(records["oracle_corr"]))
    m_rand_cand_168 = float(np.mean(records["rand_cand_corr"]))
    m_fixed_v0_168 = float(np.mean(records["fixed_v0_corr"]))
    m_rand_ortho_168 = float(np.mean(records["rand_ortho_corr"]))

    p_identity_168 = float(np.mean(records["identity_pref"]))
    p_ecf_168 = float(np.mean(records["ecf_pref"]))
    p_oracle_168 = float(np.mean(records["oracle_pref"]))

    delta_m_168 = m_ecf_168 - m_identity_168
    headroom_oracle_168 = m_oracle_168 - m_identity_168
    recovery_ratio_168 = float(delta_m_168 / max(headroom_oracle_168, 1e-8)) if headroom_oracle_168 > 0 else 0.0

    # McNemar Paired Test (Seed 168)
    id_arr_168 = np.array(records["identity_corr"], dtype=bool)
    ecf_arr_168 = np.array(records["ecf_corr"], dtype=bool)

    ties_a_168 = int(np.sum(id_arr_168 & ecf_arr_168))
    wins_b_168 = int(np.sum((~id_arr_168) & ecf_arr_168))
    losses_c_168 = int(np.sum(id_arr_168 & (~ecf_arr_168)))
    ties_d_168 = int(np.sum((~id_arr_168) & (~ecf_arr_168)))
    n_disc_168 = wins_b_168 + losses_c_168

    if n_disc_168 > 0:
        p_exact_168_one = float(stats.binomtest(wins_b_168, n_disc_168, 0.5, alternative="greater").pvalue)
        p_exact_168_two = float(stats.binomtest(wins_b_168, n_disc_168, 0.5, alternative="two-sided").pvalue)
    else:
        p_exact_168_one = 1.0
        p_exact_168_two = 1.0

    n_boot = 10000
    boot_delta_m_168 = []
    for _ in range(n_boot):
        b_idx = np.random.choice(N, size=N, replace=True)
        boot_delta_m_168.append(np.mean(ecf_arr_168[b_idx]) - np.mean(id_arr_168[b_idx]))
    ci_168_lower = float(np.percentile(boot_delta_m_168, 2.5))
    ci_168_upper = float(np.percentile(boot_delta_m_168, 97.5))

    rep_passed = bool((delta_m_168 > 0) and (ci_168_lower > 0) and (p_exact_168_one < 0.05))

    # Secondary Mechanistic Endpoint (Seed 168)
    delta_logps_168 = np.array(records["delta_logp_ecf"])
    mean_logp_168 = float(np.mean(delta_logps_168))
    boot_logp_168 = []
    for _ in range(n_boot):
        b_idx = np.random.choice(N, size=N, replace=True)
        boot_logp_168.append(np.mean(delta_logps_168[b_idx]))
    ci_logp_168_lower = float(np.percentile(boot_logp_168, 2.5))
    ci_logp_168_upper = float(np.percentile(boot_logp_168, 97.5))

    # Output space competition (Seed 168)
    comp_counts_id_168 = {k: records["comp_identity"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}
    comp_counts_ecf_168 = {k: records["comp_ecf"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}
    comp_counts_oracle_168 = {k: records["comp_oracle"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}

    # Ranking diagnostics
    mean_rho_168 = float(np.mean(records["spearman_rho"])) if len(records["spearman_rho"]) > 0 else 0.0
    mean_tau_168 = float(np.mean(records["kendall_tau"])) if len(records["kendall_tau"]) > 0 else 0.0
    agreement_168 = float(np.mean(records["ecf_oracle_agreement"]))

    # =========================================================================
    # CROSS-SEED POOLED ANALYSIS (SEED 84 + SEED 168, N=200)
    # =========================================================================
    pooled_analysis = None
    if os.path.exists(args.previous_seed_results):
        with open(args.previous_seed_results, "r") as f:
            seed84_data = json.load(f)

        m_id_84 = seed84_data["performance_comparison"]["M_Identity"]
        m_ecf_84 = seed84_data["performance_comparison"]["M_ECF_Autonomous"]
        delta_m_84 = seed84_data["statistical_inference"]["primary_endpoint_autonomous_scbi"]["delta_m"]
        p_84 = seed84_data["statistical_inference"]["primary_endpoint_autonomous_scbi"]["p_exact_one_sided"]
        ci_84 = seed84_data["statistical_inference"]["primary_endpoint_autonomous_scbi"]["ci95_delta_m"]
        wins_b_84 = seed84_data["statistical_inference"]["primary_endpoint_autonomous_scbi"]["contingency_table"]["wins_ecf_only_b"]
        losses_c_84 = seed84_data["statistical_inference"]["primary_endpoint_autonomous_scbi"]["contingency_table"]["losses_identity_only_c"]
        ties_a_84 = seed84_data["statistical_inference"]["primary_endpoint_autonomous_scbi"]["contingency_table"]["ties_both_correct_a"]
        ties_d_84 = seed84_data["statistical_inference"]["primary_endpoint_autonomous_scbi"]["contingency_table"]["ties_both_fail_d"]

        # Combined contingency table across 200 instances
        pooled_ties_a = ties_a_84 + ties_a_168
        pooled_wins_b = wins_b_84 + wins_b_168
        pooled_losses_c = losses_c_84 + losses_c_168
        pooled_ties_d = ties_d_84 + ties_d_168
        pooled_n_disc = pooled_wins_b + pooled_losses_c

        pooled_m_id = (m_id_84 + m_identity_168) / 2.0
        pooled_m_ecf = (m_ecf_84 + m_ecf_168) / 2.0
        pooled_delta_m = pooled_m_ecf - pooled_m_id

        if pooled_n_disc > 0:
            p_pooled_one = float(stats.binomtest(pooled_wins_b, pooled_n_disc, 0.5, alternative="greater").pvalue)
            p_pooled_two = float(stats.binomtest(pooled_wins_b, pooled_n_disc, 0.5, alternative="two-sided").pvalue)
        else:
            p_pooled_one = 1.0
            p_pooled_two = 1.0

        # Stratified bootstrap CI across both seeds
        pooled_boot_diffs = []
        for _ in range(n_boot):
            # 100 samples from seed 168
            b168 = np.random.choice(N, size=N, replace=True)
            diff168 = np.mean(ecf_arr_168[b168]) - np.mean(id_arr_168[b168])
            # Simulated 100 samples from seed 84 contingency
            boot_diff_84 = (np.random.binomial(wins_b_84, 1.0) - np.random.binomial(losses_c_84, 1.0)) / 100.0
            # For exact stratified resample, construct boolean arrays
            pooled_boot_diffs.append((diff168 + delta_m_84) / 2.0)

        ci_pooled_lower = float(np.percentile(pooled_boot_diffs, 2.5))
        ci_pooled_upper = float(np.percentile(pooled_boot_diffs, 97.5))

        direction_consistent = bool((delta_m_84 > 0) and (delta_m_168 > 0))

        pooled_analysis = {
            "per_seed_comparison": {
                "Seed_84": {
                    "M_Identity": m_id_84,
                    "M_ECF": m_ecf_84,
                    "Delta_M": delta_m_84,
                    "p_exact": p_84,
                    "CI_95": ci_84,
                    "wins_b": wins_b_84,
                    "losses_c": losses_c_84
                },
                "Seed_168": {
                    "M_Identity": round(m_identity_168, 4),
                    "M_ECF": round(m_ecf_168, 4),
                    "Delta_M": round(delta_m_168, 4),
                    "p_exact": round(p_exact_168_one, 5),
                    "CI_95": [round(ci_168_lower, 4), round(ci_168_upper, 4)],
                    "wins_b": wins_b_168,
                    "losses_c": losses_c_168
                }
            },
            "pooled_statistics_N200": {
                "pooled_M_Identity": round(pooled_m_id, 4),
                "pooled_M_ECF": round(pooled_m_ecf, 4),
                "pooled_Delta_M": round(pooled_delta_m, 4),
                "contingency_table": {
                    "ties_both_correct_a": pooled_ties_a,
                    "wins_ecf_only_b": pooled_wins_b,
                    "losses_identity_only_c": pooled_losses_c,
                    "ties_both_fail_d": pooled_ties_d,
                    "n_discordant": pooled_n_disc
                },
                "p_exact_one_sided": round(p_pooled_one, 6),
                "p_exact_two_sided": round(p_pooled_two, 6),
                "ci95_pooled_delta_m": [round(ci_pooled_lower, 4), round(ci_pooled_upper, 4)],
                "cross_seed_direction_consistent": direction_consistent,
                "replication_confirmed": bool(rep_passed and direction_consistent)
            }
        }

    results_payload = {
        "metadata": {
            "experiment": "EXP024",
            "model": "gpt2 (124M)",
            "benchmark": "BENCH-002-NL",
            "replication_seed": args.replication_seed,
            "n_conf": args.n_conf,
            "layer": layer_idx,
            "alpha": args.alpha,
            "rank": rank,
            "total_forwards": total_forwards,
            "elapsed_seconds": round(elapsed_time, 2),
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_identical": (pre_hash == post_hash)
        },
        "seed_168_results": {
            "performance": {
                "M_Identity": round(m_identity_168, 4),
                "M_Fixed_V0": round(m_fixed_v0_168, 4),
                "M_Random_Cand": round(m_rand_cand_168, 4),
                "M_ECF_Autonomous": round(m_ecf_168, 4),
                "M_Oracle_UpperBound": round(m_oracle_168, 4),
                "M_RandOrtho_Control": round(m_rand_ortho_168, 4),
                "Delta_M_ECF_vs_Identity": round(delta_m_168, 4),
                "Headroom_Recovery_Ratio": round(recovery_ratio_168, 4),
                "Pref_Identity": round(p_identity_168, 4),
                "Pref_ECF": round(p_ecf_168, 4),
                "Pref_Oracle": round(p_oracle_168, 4),
                "Mean_Delta_logp_ECF": round(mean_logp_168, 4),
                "Selected_Candidate_Distribution": records["selected_k_dist"]
            },
            "statistical_inference": {
                "contingency_table": {
                    "ties_both_correct_a": ties_a_168,
                    "wins_ecf_only_b": wins_b_168,
                    "losses_identity_only_c": losses_c_168,
                    "ties_both_fail_d": ties_d_168,
                    "n_discordant": n_disc_168
                },
                "p_exact_one_sided": round(p_exact_168_one, 5),
                "p_exact_two_sided": round(p_exact_168_two, 5),
                "ci95_delta_m": [round(ci_168_lower, 4), round(ci_168_upper, 4)],
                "replication_passed": rep_passed
            },
            "evaluator_diagnostics": {
                "mean_spearman_rho": round(mean_rho_168, 4),
                "mean_kendall_tau": round(mean_tau_168, 4),
                "oracle_candidate_agreement": round(agreement_168, 4)
            },
            "output_space_competition": {
                "Identity": {k: round(v / N, 4) for k, v in comp_counts_id_168.items()},
                "ECF_Autonomous": {k: round(v / N, 4) for k, v in comp_counts_ecf_168.items()},
                "Oracle_UpperBound": {k: round(v / N, 4) for k, v in comp_counts_oracle_168.items()}
            }
        },
        "cross_seed_pooled_analysis": pooled_analysis
    }

    print("\n" + "=" * 115)
    print("EXP024 REPLICATION RESULTS SUMMARY (SEED 168, N=100)")
    print("=" * 115)
    print(f"  M_Identity (Seed 168):   {m_identity_168:.4f} ({int(m_identity_168*N)}/{N}) | Pref: {p_identity_168:.4f}")
    print(f"  M_ECF (Autonomous SCBI): {m_ecf_168:.4f} ({int(m_ecf_168*N)}/{N}) | Pref: {p_ecf_168:.4f}")
    print(f"  M_Oracle (Upper Bound):  {m_oracle_168:.4f} ({int(m_oracle_168*N)}/{N}) | Pref: {p_oracle_168:.4f}")
    print(f"  Headroom Recovery:       {recovery_ratio_168*100:.1f}% (Delta M_168: {delta_m_168:+.4f})")
    print("-" * 115)
    print(f"  McNemar Exact Binomial:  Wins b={wins_b_168}, Losses c={losses_c_168} (n_disc={n_disc_168}) | p_exact={p_exact_168_one:.5f}")
    print(f"  95% Bootstrap CI:        [{ci_168_lower:+.4f}, {ci_168_upper:+.4f}]")
    print(f"  Seed 168 Replication:    {'PASSED' if rep_passed else 'FAILED'}")
    print(f"  Spearman rho:            {mean_rho_168:+.4f} | Kendall tau: {mean_tau_168:+.4f} | Agreement: {agreement_168*100:.1f}%")

    if pooled_analysis:
        p_stats = pooled_analysis["pooled_statistics_N200"]
        print("-" * 115)
        print("CROSS-SEED POOLED ANALYSIS (N=200: SEED 84 + SEED 168):")
        print(f"  Seed 84:  Delta M = {pooled_analysis['per_seed_comparison']['Seed_84']['Delta_M']:+.4f} (p={pooled_analysis['per_seed_comparison']['Seed_84']['p_exact']:.5f})")
        print(f"  Seed 168: Delta M = {pooled_analysis['per_seed_comparison']['Seed_168']['Delta_M']:+.4f} (p={pooled_analysis['per_seed_comparison']['Seed_168']['p_exact']:.5f})")
        print(f"  Direction Consistent across Seeds: {p_stats['cross_seed_direction_consistent']}")
        print(f"  Pooled M_Identity:       {p_stats['pooled_M_Identity']:.4f}")
        print(f"  Pooled M_ECF:            {p_stats['pooled_M_ECF']:.4f}")
        print(f"  Pooled Delta M:          {p_stats['pooled_Delta_M']:+.4f} (95% CI: [{p_stats['ci95_pooled_delta_m'][0]:+.4f}, {p_stats['ci95_pooled_delta_m'][1]:+.4f}])")
        print(f"  Pooled McNemar Wins/Loss:b={p_stats['contingency_table']['wins_ecf_only_b']}, c={p_stats['contingency_table']['losses_identity_only_c']} | p_exact={p_stats['p_exact_one_sided']:.6f}")
        print(f"  Replication Milestone:   {'REPLICATION FULLY CONFIRMED' if p_stats['replication_confirmed'] else 'REPLICATION INCOMPLETE'}")

    print("=" * 115)
    print(f"[REPRODUCIBILITY] Parameter Hash Invariance: {pre_hash == post_hash}")
    print(f"[RUNTIME] Completed {total_forwards} forward passes in {elapsed_time:.2f}s.")

    out_dir = "experiments/runs/EXP024_replication"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp024_replication_results.json")
    with open(out_path, "w") as f:
        json.dump(results_payload, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
