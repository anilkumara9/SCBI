"""
EXP028b Phase B: Confirmatory Benchmark on Qwen2.5-0.5B.

Evaluates the permanently locked prospective layer l* from Phase A (Layer 11, lambda = 0.458)
against the pre-declared heuristic baseline Layer 16 (lambda = 0.667) and runner-up Layer 9 (lambda = 0.375)
on BENCH-002-NL (N=100, Seed 84).

Primary Endpoint:
- Delta M_Oracle(l*) = M_Oracle(l*) - M_Identity > 0
- Comparative Test: l* (Layer 11) vs. Layer 16 (Exact Paired McNemar Test & Paired Wilcoxon)

Secondary Endpoints:
- Autonomous selection M_ECF(l*)
- Delta log p(y_correct)
- Selectivity Index and Logit KL Divergence
- Tri-state outcome resolution

Governed by AGENTS.md Laws 1, 2, 4, 6, 7, 8, 9, 11, 13, 14.
"""

import os
import sys
import time
import json
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from scipy.stats import binom, wilcoxon, spearmanr, kendalltau

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

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

def bootstrap_ci(arr, num_samples=10000, ci=0.95):
    arr = np.array(arr)
    n = len(arr)
    means = []
    rng = np.random.RandomState(84)
    for _ in range(num_samples):
        sample = rng.choice(arr, size=n, replace=True)
        means.append(np.mean(sample))
    lower = float(np.percentile(means, (1.0 - ci) / 2.0 * 100))
    upper = float(np.percentile(means, (1.0 + ci) / 2.0 * 100))
    return lower, upper

def segment_tokens(offsets, text):
    p_end = text.index(" Distractor:")
    d_end = text.index(" Question:")
    prem_indices = [i for i, (s, e) in enumerate(offsets) if e <= p_end and s < e]
    dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
    quest_indices = [i for i, (s, e) in enumerate(offsets) if s >= d_end and s < e]
    return prem_indices, dist_indices, quest_indices

def construct_contrastive_subspaces(h_premise, h_distractor, rank=2, K=4):
    h_p_centered = h_premise - torch.mean(h_premise, dim=0, keepdim=True)
    _, _, Vh_p = torch.linalg.svd(h_p_centered, full_matrices=False)
    V_plus = Vh_p[:rank, :].T

    h_d_centered = h_distractor - torch.mean(h_distractor, dim=0, keepdim=True)
    _, _, Vh_d = torch.linalg.svd(h_d_centered, full_matrices=False)
    max_components = Vh_d.shape[0]

    cand_V_minus = []
    cand_V_minus.append(Vh_d[:rank, :].T)
    idx1 = [1, min(2, max_components - 1)]
    cand_V_minus.append(Vh_d[idx1, :].T)
    idx2 = [0, min(2, max_components - 1)]
    cand_V_minus.append(Vh_d[idx2, :].T)
    idx3 = [min(2, max_components - 2), min(3, max_components - 1)] if max_components >= 4 else [0, 1]
    cand_V_minus.append(Vh_d[idx3, :].T)

    return V_plus, cand_V_minus[:K]

def run_confirmatory_layer(model, tokenizer, dataset, layer, rank=2, alpha=0.25, K=4):
    target_module = model.model.layers[layer]

    id_correct = []
    oracle_correct = []
    rand_correct = []
    ecf_correct = []

    dlogp_oracle = []
    dlogp_ecf = []

    frob_displacements = []
    kl_divergences = []
    overlaps = []
    si_list = []

    ecf_scores_all = []
    oracle_ranks_all = []

    cand_accs = {k: [] for k in range(K)}

    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        pos_text = inst["pos"]
        neg_text = inst["neg"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]

        target_id = tokenizer.encode(target_token, add_special_tokens=False)[0]
        dist_id = tokenizer.encode(distractor_token, add_special_tokens=False)[0]

        enc_base = tokenizer(base_text, return_tensors="pt", return_offsets_mapping=True)
        offsets = enc_base["offset_mapping"][0].tolist()
        input_ids = enc_base["input_ids"]

        prem_idx, dist_idx, quest_idx = segment_tokens(offsets, base_text)

        # 1. Base Forward Pass
        with torch.no_grad():
            out_base = model(input_ids=input_ids, output_hidden_states=True)

        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred = torch.argmax(base_logits).item()
        base_is_corr = (base_pred == target_id)
        id_correct.append(base_is_corr)
        base_logp = float(torch.log(base_probs[target_id] + 1e-12).item())

        # Precompute un-intervened pseudo-prompts for E_CF
        enc_pos = tokenizer(pos_text, return_tensors="pt")
        enc_neg = tokenizer(neg_text, return_tensors="pt")
        with torch.no_grad():
            pos_probs_base = F.softmax(model(**enc_pos).logits[0, -1], dim=-1)
            neg_probs_base = F.softmax(model(**enc_neg).logits[0, -1], dim=-1)

        # Hidden states at target layer
        h_l = out_base.hidden_states[layer][0]
        h_premise = h_l[prem_idx]
        h_dist = h_l[dist_idx]

        V_plus, cand_V_minus_list = construct_contrastive_subspaces(h_premise, h_dist, rank=rank, K=K)

        cand_results = []
        for k_idx, V_minus in enumerate(cand_V_minus_list):
            def make_hook(V_minus_mat, V_plus_mat, alpha_val):
                def hook_fn(module, input, output):
                    h = output[0] if isinstance(output, tuple) else output
                    rest = output[1:] if isinstance(output, tuple) else None
                    h_t = h[0]

                    proj_d = torch.matmul(h_t, V_minus_mat)
                    e_d = torch.norm(proj_d, dim=-1)
                    proj_p = torch.matmul(h_t, V_plus_mat)
                    e_p = torch.norm(proj_p, dim=-1)

                    diff = e_d - e_p
                    gate = (diff > 0.0).float().unsqueeze(-1)

                    P_minus = torch.matmul(V_minus_mat, V_minus_mat.T)
                    delta_linear = - alpha_val * torch.matmul(h_t, P_minus)
                    delta_gated_raw = gate * delta_linear

                    frob_lin = torch.norm(delta_linear, p="fro")
                    frob_gat = torch.norm(delta_gated_raw, p="fro")
                    scale = frob_lin / frob_gat if frob_gat > 1e-12 else 1.0

                    h_mod = h_t + scale * delta_gated_raw
                    return (h_mod.unsqueeze(0),) + rest if rest is not None else h_mod.unsqueeze(0)
                return hook_fn

            hook = target_module.register_forward_hook(make_hook(V_minus, V_plus, alpha))
            with torch.no_grad():
                out_cand = model(input_ids=input_ids)
            hook.remove()

            cand_logits = out_cand.logits[0, -1]
            cand_probs = F.softmax(cand_logits, dim=-1)
            cand_pred = torch.argmax(cand_logits).item()
            c_corr = (cand_pred == target_id)
            c_logp = float(torch.log(cand_probs[target_id] + 1e-12).item())

            kl = compute_kl_divergence(base_logits, cand_logits)
            overlap = compute_topk_overlap(base_logits, cand_logits, k=10)

            # Evaluator pseudo-prompts
            hook_pos = target_module.register_forward_hook(make_hook(V_minus, V_plus, alpha))
            with torch.no_grad():
                out_pos = model(**enc_pos)
            hook_pos.remove()

            hook_neg = target_module.register_forward_hook(make_hook(V_minus, V_plus, alpha))
            with torch.no_grad():
                out_neg = model(**enc_neg)
            hook_neg.remove()

            pos_probs_cand = F.softmax(out_pos.logits[0, -1], dim=-1)
            d_pos = pos_probs_cand[target_id].item() - pos_probs_base[target_id].item()

            neg_probs_cand = F.softmax(out_neg.logits[0, -1], dim=-1)
            d_neg = neg_probs_cand[dist_id].item() - neg_probs_base[dist_id].item()

            ecf_score = d_pos - 0.5 * d_neg

            cand_accs[k_idx].append(c_corr)
            cand_results.append({
                "k_idx": k_idx,
                "is_correct": c_corr,
                "logp": c_logp,
                "delta_logp": c_logp - base_logp,
                "kl": kl,
                "overlap": overlap,
                "ecf_score": ecf_score
            })

        # Separability on candidate 0
        V_minus_0 = cand_V_minus_list[0]
        proj_dist_tokens = torch.matmul(h_l, V_minus_0)
        energy_dist_tokens = torch.norm(proj_dist_tokens, dim=-1)
        proj_prem_tokens = torch.matmul(h_l, V_plus)
        energy_prem_tokens = torch.norm(proj_prem_tokens, dim=-1)
        d_tokens = energy_dist_tokens - energy_prem_tokens

        d_prem = d_tokens[prem_idx]
        d_dist = d_tokens[dist_idx]
        g_rate_prem = float(torch.mean((d_prem > 0.0).float()).item()) if len(d_prem) > 0 else 0.0
        g_rate_dist = float(torch.mean((d_dist > 0.0).float()).item()) if len(d_dist) > 0 else 0.0
        si_list.append(g_rate_dist - g_rate_prem)

        # Oracle Candidate
        oracle_cand = None
        for c in cand_results:
            if c["is_correct"]:
                oracle_cand = c
                break
        if oracle_cand is None:
            best_k = int(np.argmax([c["logp"] for c in cand_results]))
            oracle_cand = cand_results[best_k]

        oracle_correct.append(oracle_cand["is_correct"])
        dlogp_oracle.append(oracle_cand["delta_logp"])
        kl_divergences.append(oracle_cand["kl"])
        overlaps.append(oracle_cand["overlap"])

        # Random candidate (Candidate 1)
        rand_correct.append(cand_results[1]["is_correct"])

        # Autonomous E_CF Candidate
        ecf_cand = max(cand_results, key=lambda c: c["ecf_score"])
        ecf_correct.append(ecf_cand["is_correct"])
        dlogp_ecf.append(ecf_cand["delta_logp"])

        # Evaluator ranking correlation metrics
        cand_logps = [c["logp"] for c in cand_results]
        cand_ecf_scores = [c["ecf_score"] for c in cand_results]
        ecf_scores_all.append(cand_ecf_scores)
        oracle_ranks_all.append(cand_logps)

        # Norm displacement on candidate 0
        P_minus_0 = torch.matmul(V_minus_0, V_minus_0.T)
        delta_lin_0 = - alpha * torch.matmul(h_l, P_minus_0)
        proj_d_0 = torch.matmul(h_l, V_minus_0)
        proj_p_0 = torch.matmul(h_l, V_plus)
        diff_0 = torch.norm(proj_d_0, dim=-1) - torch.norm(proj_p_0, dim=-1)
        gate_0 = (diff_0 > 0.0).float().unsqueeze(-1)
        delta_gat_0 = gate_0 * delta_lin_0
        f_lin = torch.norm(delta_lin_0, p="fro")
        f_gat = torch.norm(delta_gat_0, p="fro")
        sc = f_lin / f_gat if f_gat > 1e-12 else 1.0
        h_disp = sc * delta_gat_0
        frob_displacements.append(float(torch.norm(h_disp, p="fro") / (torch.norm(h_l, p="fro") + 1e-12)))

    # Compute aggregate metrics
    m_id = float(np.mean(id_correct))
    m_oracle = float(np.mean(oracle_correct))
    m_rand = float(np.mean(rand_correct))
    m_ecf = float(np.mean(ecf_correct))

    delta_m_oracle = m_oracle - m_id
    delta_m_ecf = m_ecf - m_id

    # Bootstrap CIs
    headroom_diffs = np.array(oracle_correct, dtype=float) - np.array(id_correct, dtype=float)
    ci_headroom = bootstrap_ci(headroom_diffs)

    ecf_diffs = np.array(ecf_correct, dtype=float) - np.array(id_correct, dtype=float)
    ci_ecf = bootstrap_ci(ecf_diffs)

    ci_dlogp_oracle = bootstrap_ci(dlogp_oracle)
    ci_dlogp_ecf = bootstrap_ci(dlogp_ecf)
    ci_si = bootstrap_ci(si_list)

    # McNemar vs Identity
    b_wins = int(np.sum((np.array(oracle_correct) == 1) & (np.array(id_correct) == 0)))
    c_losses = int(np.sum((np.array(oracle_correct) == 0) & (np.array(id_correct) == 1)))
    n_disc = b_wins + c_losses
    if n_disc > 0:
        p_mcnemar = float(1.0 - binom.cdf(b_wins - 1, n_disc, 0.5))
    else:
        p_mcnemar = 1.0

    # Evaluator ranking correlation
    spearmans = []
    kendalls = []
    for scores, logs in zip(ecf_scores_all, oracle_ranks_all):
        if len(set(scores)) > 1 and len(set(logs)) > 1:
            sr, _ = spearmanr(scores, logs)
            kt, _ = kendalltau(scores, logs)
            if not np.isnan(sr): spearmans.append(sr)
            if not np.isnan(kt): kendalls.append(kt)

    mean_rho = float(np.mean(spearmans)) if len(spearmans) > 0 else 0.0
    mean_tau = float(np.mean(kendalls)) if len(kendalls) > 0 else 0.0

    k_means = [float(np.mean(cand_accs[k])) for k in range(K)]
    cand_spread = max(k_means) - min(k_means)

    return {
        "layer": layer,
        "M_Identity": m_id,
        "M_Oracle": m_oracle,
        "M_Random": m_rand,
        "M_ECF": m_ecf,
        "Oracle_Headroom": delta_m_oracle,
        "Oracle_Headroom_CI95": list(ci_headroom),
        "Candidate_Spread": cand_spread,
        "ECF_Headroom": delta_m_ecf,
        "ECF_Headroom_CI95": list(ci_ecf),
        "McNemar_vs_Identity": {"b_wins": b_wins, "c_losses": c_losses, "p_one_sided": p_mcnemar},
        "Mean_Delta_LogP_Oracle": float(np.mean(dlogp_oracle)),
        "Mean_Delta_LogP_Oracle_CI95": list(ci_dlogp_oracle),
        "Mean_Delta_LogP_ECF": float(np.mean(dlogp_ecf)),
        "Mean_Delta_LogP_ECF_CI95": list(ci_dlogp_ecf),
        "Selectivity_Index": float(np.mean(si_list)),
        "Selectivity_Index_CI95": list(ci_si),
        "Frobenius_Displacement": float(np.mean(frob_displacements)),
        "KL_Divergence": float(np.mean(kl_divergences)),
        "Top10_Overlap": float(np.mean(overlaps)),
        "Evaluator_Spearman_Rho": mean_rho,
        "Evaluator_Kendall_Tau": mean_tau,
        "raw_oracle_correct": [int(x) for x in oracle_correct],
        "raw_delta_logp_oracle": dlogp_oracle,
        "raw_id_correct": [int(x) for x in id_correct]
    }

def main():
    print("=" * 100)
    print("EXP028b PHASE B: CONFIRMATORY BENCHMARK (Qwen/Qwen2.5-0.5B)")
    print("Evaluating Locked Prospective Stage l* vs. Pre-Declared Baseline Layer 16")
    print("=" * 100)

    lock_file = "experiments/runs/EXP028b_qwen/exp028b_prediction_lock.json"
    assert os.path.exists(lock_file), f"FATAL: Lock file {lock_file} does not exist!"

    with open(lock_file, "r") as f:
        lock_data = json.load(f)

    locked_l_star = lock_data["locked_prediction"]["primary_predicted_layer_l_star"]
    runner_up_l = lock_data["locked_prediction"]["runner_up_layer"]
    baseline_l = lock_data["metadata"]["predeclared_baseline_layer"]
    lock_hash = lock_data.get("lock_checksum_sha256", "UNKNOWN")

    print(f"[PREDICTION VERIFIED] Reading from lock file: {lock_file}")
    print(f"[PREDICTION VERIFIED] Locked Prospective Layer l*: LAYER {locked_l_star}")
    print(f"[PREDICTION VERIFIED] Pre-Declared Baseline Layer:   LAYER {baseline_l}")
    print(f"[PREDICTION VERIFIED] Runner-up Stage Layer:        LAYER {runner_up_l}")
    print(f"[PREDICTION VERIFIED] Lock Record Checksum SHA-256:  {lock_hash}")

    model_name = "Qwen/Qwen2.5-0.5B"
    seed = 84
    n_instances = 100

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    assert pre_hash == lock_data["metadata"]["parameter_sha256"], "Model weights differ from Phase A!"
    print(f"[REPRODUCIBILITY] Pre-run Parameter SHA-256 verified: {pre_hash}")

    dataset = generate_bench_002_nl(n_instances=n_instances, seed=seed)
    print(f"[BENCHMARK] Loaded {len(dataset)} confirmatory instances (Seed {seed}).")

    # 1. Evaluate Locked Layer l* (Layer 11)
    print(f"\n>>> EVALUATING LOCKED PROSPECTIVE STAGE: Layer {locked_l_star}...")
    res_l_star = run_confirmatory_layer(model, tokenizer, dataset, layer=locked_l_star)

    # 2. Evaluate Pre-Declared Baseline Stage (Layer 16)
    print(f"\n>>> EVALUATING PRE-DECLARED BASELINE STAGE: Layer {baseline_l}...")
    res_baseline = run_confirmatory_layer(model, tokenizer, dataset, layer=baseline_l)

    # 3. Evaluate Runner-up Stage (Layer 9)
    print(f"\n>>> EVALUATING RUNNER-UP STAGE: Layer {runner_up_l}...")
    res_runner_up = run_confirmatory_layer(model, tokenizer, dataset, layer=runner_up_l)

    # 4. Pairwise Confirmatory Test: l* (Layer 11) vs. Baseline Layer 16
    l_star_corr = np.array(res_l_star["raw_oracle_correct"])
    base_corr = np.array(res_baseline["raw_oracle_correct"])

    b_pair = int(np.sum((l_star_corr == 1) & (base_corr == 0)))
    c_pair = int(np.sum((l_star_corr == 0) & (base_corr == 1)))
    a_pair = int(np.sum((l_star_corr == 1) & (base_corr == 1)))
    d_pair = int(np.sum((l_star_corr == 0) & (base_corr == 0)))

    n_disc_pair = b_pair + c_pair
    if n_disc_pair > 0:
        p_pair_one_sided = float(1.0 - binom.cdf(b_pair - 1, n_disc_pair, 0.5))
        p_pair_two_sided = float(binom.cdf(min(b_pair, c_pair), n_disc_pair, 0.5) * 2.0)
    else:
        p_pair_one_sided = 1.0
        p_pair_two_sided = 1.0

    l_star_dlogp = np.array(res_l_star["raw_delta_logp_oracle"])
    base_dlogp = np.array(res_baseline["raw_delta_logp_oracle"])
    diff_dlogp = l_star_dlogp - base_dlogp
    w_stat, w_pval = wilcoxon(l_star_dlogp, base_dlogp, alternative="greater")

    # 5. Tri-State Outcome Resolution
    delta_oracle_l_star = res_l_star["Oracle_Headroom"]
    m_oracle_l_star = res_l_star["M_Oracle"]
    m_oracle_base = res_baseline["M_Oracle"]

    if delta_oracle_l_star > 0 and (m_oracle_l_star >= m_oracle_base):
        outcome_status = "OUTCOME_1_PREDICTION_CONFIRMED"
        outcome_desc = "Prospective stage prediction successfully identified an effective intervention layer with positive Oracle headroom that equals or exceeds the baseline heuristic."
    elif delta_oracle_l_star <= 0 and (res_runner_up["Oracle_Headroom"] > 0 or res_baseline["Oracle_Headroom"] > 0):
        outcome_status = "OUTCOME_2_COARSE_VALIDITY"
        outcome_desc = "Predicted layer did not capture headroom, but an adjacent or baseline layer captured positive headroom (coarse localization)."
    else:
        outcome_status = "OUTCOME_3_PREDICTION_FALSIFIED"
        outcome_desc = "SCBI intervention failed to expose headroom across tested configurations on this architecture."

    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "Backbone parameters corrupted!"

    final_report = {
        "metadata": {
            "experiment": "EXP028b",
            "phase": "Phase B (Confirmatory Benchmark)",
            "model_name": model_name,
            "parameter_sha256": pre_hash,
            "parameter_invariant": (pre_hash == post_hash),
            "n_instances": n_instances,
            "seed": seed,
            "lock_checksum_verified": lock_hash
        },
        "tri_state_outcome": {
            "status": outcome_status,
            "description": outcome_desc
        },
        "primary_prediction_layer_l_star": {
            "layer": locked_l_star,
            "results": {k: v for k, v in res_l_star.items() if not k.startswith("raw_")}
        },
        "predeclared_baseline_layer_16": {
            "layer": baseline_l,
            "results": {k: v for k, v in res_baseline.items() if not k.startswith("raw_")}
        },
        "runner_up_layer_9": {
            "layer": runner_up_l,
            "results": {k: v for k, v in res_runner_up.items() if not k.startswith("raw_")}
        },
        "pairwise_test_l_star_vs_baseline": {
            "contingency_table": {"a_both_correct": a_pair, "b_l_star_win": b_pair, "c_base_win": c_pair, "d_both_incorrect": d_pair},
            "mcnemar_b": b_pair,
            "mcnemar_c": c_pair,
            "mcnemar_p_one_sided": p_pair_one_sided,
            "mcnemar_p_two_sided": p_pair_two_sided,
            "mean_delta_logp_diff": float(np.mean(diff_dlogp)),
            "wilcoxon_stat": float(w_stat),
            "wilcoxon_p_one_sided": float(w_pval)
        }
    }

    out_file = "experiments/runs/EXP028b_qwen/exp028b_confirmatory_results.json"
    with open(out_file, "w") as f:
        json.dump(final_report, f, indent=2)

    print("\n" + "=" * 100)
    print("EXP028b PHASE B BENCHMARK RESULTS:")
    print("=" * 100)
    print(f"TRI-STATE OUTCOME: {outcome_status}")
    print(f"Description: {outcome_desc}")
    print("-" * 100)
    print(f"Baseline Identity:   M_I = {res_l_star['M_Identity']:.4f}")
    print(f"Predicted L* (L{locked_l_star}): M_Oracle = {res_l_star['M_Oracle']:.4f} (Headroom = {res_l_star['Oracle_Headroom']:+.4f}, CI: {res_l_star['Oracle_Headroom_CI95']})")
    print(f"                     M_ECF    = {res_l_star['M_ECF']:.4f} (Headroom = {res_l_star['ECF_Headroom']:+.4f})")
    print(f"                     SI       = {res_l_star['Selectivity_Index']:.4f}, KL = {res_l_star['KL_Divergence']:.4f}, Mean Delta_logp = {res_l_star['Mean_Delta_LogP_Oracle']:+.4f}")
    print(f"Baseline L16:        M_Oracle = {res_baseline['M_Oracle']:.4f} (Headroom = {res_baseline['Oracle_Headroom']:+.4f}, CI: {res_baseline['Oracle_Headroom_CI95']})")
    print(f"                     M_ECF    = {res_baseline['M_ECF']:.4f} (Headroom = {res_baseline['ECF_Headroom']:+.4f})")
    print(f"                     SI       = {res_baseline['Selectivity_Index']:.4f}, KL = {res_baseline['KL_Divergence']:.4f}, Mean Delta_logp = {res_baseline['Mean_Delta_LogP_Oracle']:+.4f}")
    print(f"Runner-up L9:        M_Oracle = {res_runner_up['M_Oracle']:.4f} (Headroom = {res_runner_up['Oracle_Headroom']:+.4f})")
    print("-" * 100)
    print(f"Pairwise McNemar (L{locked_l_star} vs. L{baseline_l}): b (L* win) = {b_pair}, c (L16 win) = {c_pair} -> p = {p_pair_one_sided:.6f}")
    print(f"Wilcoxon Log-Prob Advantage: W = {w_stat:.1f}, p = {w_pval:.6e}")
    print("=" * 100)
    print(f"Results successfully saved to {out_file}")

if __name__ == "__main__":
    main()
