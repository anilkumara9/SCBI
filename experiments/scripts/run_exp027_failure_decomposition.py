"""
EXP027: Cross-Architecture Failure Decomposition.

Performs a systematic diagnostic decomposition of the failure of frozen SCBI on EleutherAI/pythia-160m:
Does the failure occur at:
1. Component A: Candidate Quality Spread (G audit: M_Oracle - M_Random)
2. Component B: Contrastive Evidence Separability (e_t^-, e_t^+, d_t on Premise vs Distractor vs Question)
3. Component C: Operator Displacement & Representation Impact (Frobenius displacement, logit KL, top-10 overlap)
4. Component D: Evaluator Calibration (E_CF Spearman rho and Kendall tau vs true utility)
5. Component E: Functional Depth Sensitivity Profile (evaluating Pythia across layers l in {2, 4, 6, 8, 10, 11})

Governing laws: AGENTS.md Laws 1, 2, 4, 6, 7, 8, 9, 10, 11, 13, 14.
"""

import os
import sys
import time
import json
import random
import hashlib
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from scipy.stats import spearmanr, kendalltau, binom

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

def get_hook_target(model, model_type, block_idx):
    if model_type == "gpt2":
        return model.transformer.h[block_idx]
    elif model_type == "pythia":
        return model.gpt_neox.layers[block_idx]
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def segment_tokens(offsets, text):
    p_end = text.index(" Distractor:")
    d_end = text.index(" Question:")
    prem_indices = [i for i, (s, e) in enumerate(offsets) if e <= p_end and s < e]
    dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
    quest_indices = [i for i, (s, e) in enumerate(offsets) if s >= d_end and s < e]
    return prem_indices, dist_indices, quest_indices

def run_layer_diagnostic(model, tokenizer, model_type, dataset, layer, alpha=0.25, rank=2, K=4, include_evaluator=True):
    block_idx = layer - 1
    target_module = get_hook_target(model, model_type, block_idx)

    # Aggregators
    n_instances = len(dataset)
    id_correct = []
    oracle_correct = []
    random_correct = []
    cand_correct = [[] for _ in range(K)]
    cand_delta_logp = [[] for _ in range(K)]

    # Separability metrics across instances
    mean_d_prem_list = []
    mean_d_dist_list = []
    mean_d_quest_list = []
    gate_rate_prem_list = []
    gate_rate_dist_list = []
    gate_rate_quest_list = []
    selectivity_index_list = []

    # Operator displacement metrics
    disp_list = []
    kl_list = []
    overlap_list = []
    delta_logp_list = []
    delta_margin_list = []

    # Evaluator metrics
    ecf_correct = []
    spearman_rho_list = []
    kendall_tau_list = []
    ecf_oracle_agreements = []

    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        pos_text = inst["pos"]
        neg_text = inst["neg"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]

        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]

        enc_base = tokenizer(base_text, return_tensors="pt", return_offsets_mapping=True)
        offsets = enc_base["offset_mapping"][0].tolist()
        input_ids = enc_base["input_ids"]

        prem_idx, dist_idx, quest_idx = segment_tokens(offsets, base_text)

        # 1. Identity Forward Pass
        with torch.no_grad():
            out_base = model(input_ids=input_ids, output_hidden_states=True)

        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred = torch.argmax(base_logits).item()
        base_is_corr = (base_pred == target_id)
        id_correct.append(base_is_corr)

        base_logp = float(torch.log(base_probs[target_id] + 1e-12).item())
        base_dist_logp = float(torch.log(base_probs[dist_id] + 1e-12).item())
        base_margin = base_probs[target_id].item() - base_probs[dist_id].item()

        # Precompute un-intervened pseudo-prompts if evaluating E_CF
        if include_evaluator:
            enc_pos = tokenizer(pos_text, return_tensors="pt")
            enc_neg = tokenizer(neg_text, return_tensors="pt")
            with torch.no_grad():
                pos_logits_base = model(**enc_pos).logits[0, -1]
                neg_logits_base = model(**enc_neg).logits[0, -1]
            pos_probs_base = F.softmax(pos_logits_base, dim=-1)
            neg_probs_base = F.softmax(neg_logits_base, dim=-1)

        # Hidden state at target layer
        h_l = out_base.hidden_states[layer][0] # shape [T, d]
        h_premise = h_l[prem_idx]
        h_dist = h_l[dist_idx]

        V_plus, cand_V_minus_list = construct_contrastive_subspaces(h_premise, h_dist, rank=rank, K=K)

        cand_results = []
        for k_idx, V_minus in enumerate(cand_V_minus_list):
            def make_hook(V_minus_mat, V_plus_mat, alpha_val):
                def hook_fn(module, input, output):
                    if isinstance(output, tuple):
                        h = output[0]
                        rest = output[1:]
                    else:
                        h = output
                        rest = None

                    h_t = h[0]
                    proj_dist = torch.matmul(h_t, V_minus_mat)
                    energy_dist = torch.norm(proj_dist, dim=-1)
                    proj_prem = torch.matmul(h_t, V_plus_mat)
                    energy_prem = torch.norm(proj_prem, dim=-1)

                    diff = energy_dist - energy_prem
                    gate = (diff > 0.0).float().unsqueeze(-1)

                    P_minus = torch.matmul(V_minus_mat, V_minus_mat.T)
                    delta_linear = - alpha_val * torch.matmul(h_t, P_minus)
                    delta_gated_raw = gate * delta_linear

                    frob_linear = torch.norm(delta_linear, p="fro")
                    frob_gated = torch.norm(delta_gated_raw, p="fro")

                    if frob_gated > 1e-12:
                        scale = frob_linear / frob_gated
                    else:
                        scale = 1.0

                    delta_h = scale * delta_gated_raw
                    h_mod = h_t + delta_h

                    if rest is not None:
                        return (h_mod.unsqueeze(0),) + rest
                    return h_mod.unsqueeze(0)
                return hook_fn

            hook = target_module.register_forward_hook(make_hook(V_minus, V_plus, alpha))
            with torch.no_grad():
                out_cand = model(input_ids=input_ids)
            hook.remove()

            cand_logits = out_cand.logits[0, -1]
            cand_probs = F.softmax(cand_logits, dim=-1)
            cand_pred = torch.argmax(cand_logits).item()
            cand_is_corr = (cand_pred == target_id)
            cand_logp = float(torch.log(cand_probs[target_id] + 1e-12).item())
            cand_dist_logp = float(torch.log(cand_probs[dist_id] + 1e-12).item())
            cand_margin = cand_probs[target_id].item() - cand_probs[dist_id].item()

            kl = compute_kl_divergence(base_logits, cand_logits)
            overlap = compute_topk_overlap(base_logits, cand_logits, k=10)

            # Evaluator score on pseudo-prompts
            if include_evaluator:
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
            else:
                ecf_score = 0.0

            cand_correct[k_idx].append(cand_is_corr)
            cand_delta_logp[k_idx].append(cand_logp - base_logp)

            cand_results.append({
                "k_idx": k_idx,
                "is_correct": cand_is_corr,
                "cand_logp": cand_logp,
                "delta_logp": cand_logp - base_logp,
                "delta_margin": cand_margin - base_margin,
                "kl": kl,
                "overlap": overlap,
                "ecf_score": ecf_score,
                "V_minus": V_minus
            })

        # Measure token-level separability on candidate 0 (primary SVD direction)
        V_minus_0 = cand_V_minus_list[0]
        proj_dist_tokens = torch.matmul(h_l, V_minus_0)
        energy_dist_tokens = torch.norm(proj_dist_tokens, dim=-1)
        proj_prem_tokens = torch.matmul(h_l, V_plus)
        energy_prem_tokens = torch.norm(proj_prem_tokens, dim=-1)
        d_tokens = energy_dist_tokens - energy_prem_tokens

        d_prem = d_tokens[prem_idx]
        d_dist = d_tokens[dist_idx]
        d_quest = d_tokens[quest_idx]

        m_d_prem = float(torch.mean(d_prem).item()) if len(d_prem) > 0 else 0.0
        m_d_dist = float(torch.mean(d_dist).item()) if len(d_dist) > 0 else 0.0
        m_d_quest = float(torch.mean(d_quest).item()) if len(d_quest) > 0 else 0.0

        g_rate_prem = float(torch.mean((d_prem > 0.0).float()).item()) if len(d_prem) > 0 else 0.0
        g_rate_dist = float(torch.mean((d_dist > 0.0).float()).item()) if len(d_dist) > 0 else 0.0
        g_rate_quest = float(torch.mean((d_quest > 0.0).float()).item()) if len(d_quest) > 0 else 0.0

        mean_d_prem_list.append(m_d_prem)
        mean_d_dist_list.append(m_d_dist)
        mean_d_quest_list.append(m_d_quest)
        gate_rate_prem_list.append(g_rate_prem)
        gate_rate_dist_list.append(g_rate_dist)
        gate_rate_quest_list.append(g_rate_quest)
        selectivity_index_list.append(g_rate_dist - g_rate_prem)

        # Oracle Candidate
        oracle_cand = None
        for c in cand_results:
            if c["is_correct"]:
                oracle_cand = c
                break
        if oracle_cand is None:
            oracle_cand = cand_results[0]
        oracle_correct.append(oracle_cand["is_correct"])

        # Random Candidate (seed-consistent for instance)
        rng = random.Random(84000 + idx)
        rand_idx = rng.randint(0, K - 1)
        random_correct.append(cand_results[rand_idx]["is_correct"])

        # Counterfactual Selected Candidate
        sorted_by_ecf = sorted(cand_results, key=lambda c: c["ecf_score"], reverse=True)
        selected_cand = sorted_by_ecf[0]
        ecf_correct.append(selected_cand["is_correct"])
        ecf_oracle_agreements.append(selected_cand["k_idx"] == oracle_cand["k_idx"])

        # Operator displacement metrics from candidate 0
        cand_0 = cand_results[0]
        # Realized Frobenius displacement
        P_minus_0 = torch.matmul(V_minus_0, V_minus_0.T)
        delta_lin = - alpha * torch.matmul(h_l, P_minus_0)
        gate_0 = (d_tokens > 0.0).float().unsqueeze(-1)
        delta_gated = gate_0 * delta_lin
        frob_lin = torch.norm(delta_lin, p="fro")
        frob_gat = torch.norm(delta_gated, p="fro")
        scale_0 = frob_lin / frob_gat if frob_gat > 1e-12 else 1.0
        delta_realized = scale_0 * delta_gated
        disp = float((torch.norm(delta_realized, p="fro") / (torch.norm(h_l, p="fro") + 1e-12)).item())

        disp_list.append(disp)
        kl_list.append(cand_0["kl"])
        overlap_list.append(cand_0["overlap"])
        delta_logp_list.append(cand_0["delta_logp"])
        delta_margin_list.append(cand_0["delta_margin"])

        # Evaluator Correlation on this instance across K candidates
        ecf_scores = [c["ecf_score"] for c in cand_results]
        true_utilities = [c["delta_logp"] for c in cand_results]
        if len(set(ecf_scores)) > 1 and len(set(true_utilities)) > 1:
            rho, _ = spearmanr(ecf_scores, true_utilities)
            tau, _ = kendalltau(ecf_scores, true_utilities)
            if not np.isnan(rho):
                spearman_rho_list.append(rho)
            if not np.isnan(tau):
                kendall_tau_list.append(tau)

    # Compute Aggregate Summary for Layer
    res = {
        "layer": layer,
        "n_instances": n_instances,
        "M_Identity": float(np.mean(id_correct)),
        "M_Oracle": float(np.mean(oracle_correct)),
        "M_Random": float(np.mean(random_correct)),
        "M_ECF": float(np.mean(ecf_correct)),
        "Oracle_Headroom": float(np.mean(oracle_correct) - np.mean(id_correct)),
        "Candidate_Spread": float(np.mean(oracle_correct) - np.mean(random_correct)),
        "Selection_Regret": float(np.mean(oracle_correct) - np.mean(ecf_correct)),
        "ECF_Oracle_Agreement": float(np.mean(ecf_oracle_agreements)),
        "Candidate_Accuracies": [float(np.mean(c)) for c in cand_correct],
        "Candidate_Mean_Delta_LogP": [float(np.mean(c)) for c in cand_delta_logp],
        # Separability
        "Separability": {
            "mean_d_premise": float(np.mean(mean_d_prem_list)),
            "mean_d_distractor": float(np.mean(mean_d_dist_list)),
            "mean_d_question": float(np.mean(mean_d_quest_list)),
            "gate_rate_premise": float(np.mean(gate_rate_prem_list)),
            "gate_rate_distractor": float(np.mean(gate_rate_dist_list)),
            "gate_rate_question": float(np.mean(gate_rate_quest_list)),
            "selectivity_index": float(np.mean(selectivity_index_list)),
        },
        # Operator
        "Operator": {
            "mean_frobenius_displacement": float(np.mean(disp_list)),
            "mean_kl_divergence": float(np.mean(kl_list)),
            "mean_top10_overlap": float(np.mean(overlap_list)),
            "mean_delta_logp": float(np.mean(delta_logp_list)),
            "mean_delta_margin": float(np.mean(delta_margin_list)),
        },
        # Evaluator
        "Evaluator": {
            "spearman_rho": float(np.mean(spearman_rho_list)) if spearman_rho_list else 0.0,
            "kendall_tau": float(np.mean(kendall_tau_list)) if kendall_tau_list else 0.0,
        }
    }
    return res

def main():
    parser = argparse.ArgumentParser(description="EXP027: Failure Decomposition")
    parser.add_argument("--n_instances", type=int, default=100, help="Number of instances")
    parser.add_argument("--seed", type=int, default=84, help="Dataset seed")
    parser.add_argument("--alpha", type=float, default=0.25, help="Operator strength")
    parser.add_argument("--rank", type=int, default=2, help="Subspace rank")
    parser.add_argument("--dev", action="store_true", help="Quick dev run")
    args = parser.parse_args()

    n_instances = 10 if args.dev else args.n_instances
    seed = args.seed
    alpha = args.alpha
    rank = args.rank

    print("=" * 100)
    print(f"STARTING EXP027: CROSS-ARCHITECTURE FAILURE DECOMPOSITION")
    print(f"N = {n_instances}, Seed = {seed}, alpha = {alpha}, rank = {rank}")
    print("=" * 100)

    dataset = generate_bench_002_nl(n_instances=n_instances, seed=seed)
    out_dir = "experiments/runs/EXP027_decomposition"
    os.makedirs(out_dir, exist_ok=True)

    results = {
        "metadata": {
            "experiment": "EXP027",
            "date": "2026-09-11",
            "n_instances": n_instances,
            "seed": seed,
            "alpha": alpha,
            "rank": rank,
            "dev_mode": args.dev
        },
        "gpt2_reference": None,
        "pythia_reference_layer8": None,
        "pythia_depth_profile": {}
    }

    # -------------------------------------------------------------
    # 1. GPT-2 Small Reference (Layer 8, lambda = 0.667)
    # -------------------------------------------------------------
    print("\n>>> AUDITING REFERENCE: GPT-2 Small (Layer 8, lambda = 8/12 = 0.667)")
    tok_gpt2 = AutoTokenizer.from_pretrained("gpt2")
    model_gpt2 = AutoModelForCausalLM.from_pretrained("gpt2")
    model_gpt2.eval()
    pre_hash_gpt2 = get_param_hash(model_gpt2)

    res_gpt2 = run_layer_diagnostic(model_gpt2, tok_gpt2, "gpt2", dataset, layer=8, alpha=alpha, rank=rank)
    post_hash_gpt2 = get_param_hash(model_gpt2)
    assert pre_hash_gpt2 == post_hash_gpt2, "GPT-2 backbone parameter hash corrupted!"
    res_gpt2["param_hash"] = pre_hash_gpt2
    results["gpt2_reference"] = res_gpt2

    print(f"[GPT-2 Layer 8] M_I={res_gpt2['M_Identity']:.4f}, M_Oracle={res_gpt2['M_Oracle']:.4f}, Headroom={res_gpt2['Oracle_Headroom']:.4f}, Spread={res_gpt2['Candidate_Spread']:.4f}")
    print(f"[GPT-2 Layer 8] Selectivity Index={res_gpt2['Separability']['selectivity_index']:.4f}, Mean d_dist={res_gpt2['Separability']['mean_d_distractor']:.4f}, Mean d_prem={res_gpt2['Separability']['mean_d_premise']:.4f}")
    print(f"[GPT-2 Layer 8] Disp={res_gpt2['Operator']['mean_frobenius_displacement']:.4f}, KL={res_gpt2['Operator']['mean_kl_divergence']:.4f}, Evaluator rho={res_gpt2['Evaluator']['spearman_rho']:.4f}")

    del model_gpt2
    del tok_gpt2

    # -------------------------------------------------------------
    # 2. Pythia-160M Reference (Layer 8, lambda = 0.667)
    # -------------------------------------------------------------
    print("\n>>> AUDITING TARGET: EleutherAI/pythia-160m (Layer 8, lambda = 8/12 = 0.667)")
    tok_pythia = AutoTokenizer.from_pretrained("EleutherAI/pythia-160m")
    model_pythia = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-160m")
    model_pythia.eval()
    pre_hash_pythia = get_param_hash(model_pythia)

    res_pythia_8 = run_layer_diagnostic(model_pythia, tok_pythia, "pythia", dataset, layer=8, alpha=alpha, rank=rank)
    results["pythia_reference_layer8"] = res_pythia_8

    print(f"[Pythia Layer 8] M_I={res_pythia_8['M_Identity']:.4f}, M_Oracle={res_pythia_8['M_Oracle']:.4f}, Headroom={res_pythia_8['Oracle_Headroom']:.4f}, Spread={res_pythia_8['Candidate_Spread']:.4f}")
    print(f"[Pythia Layer 8] Selectivity Index={res_pythia_8['Separability']['selectivity_index']:.4f}, Mean d_dist={res_pythia_8['Separability']['mean_d_distractor']:.4f}, Mean d_prem={res_pythia_8['Separability']['mean_d_premise']:.4f}")
    print(f"[Pythia Layer 8] Disp={res_pythia_8['Operator']['mean_frobenius_displacement']:.4f}, KL={res_pythia_8['Operator']['mean_kl_divergence']:.4f}, Evaluator rho={res_pythia_8['Evaluator']['spearman_rho']:.4f}")

    # -------------------------------------------------------------
    # 3. Component E: Functional Depth Sensitivity Profile for Pythia-160m
    # Test layers l in {2, 4, 6, 10, 11}
    # -------------------------------------------------------------
    layers_to_test = [2, 4, 6, 10, 11]
    print(f"\n>>> AUDITING FUNCTIONAL DEPTH PROFILE: Pythia-160m across layers {layers_to_test}")
    for l in layers_to_test:
        print(f"\nEvaluating Pythia-160m at Layer {l}...")
        res_l = run_layer_diagnostic(model_pythia, tok_pythia, "pythia", dataset, layer=l, alpha=alpha, rank=rank, include_evaluator=False)
        results["pythia_depth_profile"][f"layer_{l}"] = res_l
        print(f"[Pythia Layer {l}] M_I={res_l['M_Identity']:.4f}, M_Oracle={res_l['M_Oracle']:.4f}, Headroom={res_l['Oracle_Headroom']:.4f}, Spread={res_l['Candidate_Spread']:.4f}, SI={res_l['Separability']['selectivity_index']:.4f}, Disp={res_l['Operator']['mean_frobenius_displacement']:.4f}")

    post_hash_pythia = get_param_hash(model_pythia)
    assert pre_hash_pythia == post_hash_pythia, "Pythia backbone parameter hash corrupted!"
    results["pythia_param_hash"] = pre_hash_pythia

    out_file = os.path.join(out_dir, "exp027_decomposition_results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 100)
    print(f"EXP027 COMPLETED SUCCESSFULLY. Results saved to: {out_file}")
    print("=" * 100)

if __name__ == "__main__":
    main()
