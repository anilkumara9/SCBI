"""
EXP025: Cross-Template and Cross-Task Generalization Benchmark for SCBI.

Evaluates the locked, autonomous SCBI pipeline across two orthogonal transfer tests:
1. Suite A: BENCH-003-TEMPLATES (N=100, Seed 250)
   - 50% Target-First vs. 50% Distractor-First surface order
   - Varied lexical framing (Fact/Note, Context/Meanwhile, Record/Incident, Natural Prose)
2. Suite B: BENCH-004-TRANSFER (N=100, Seed 350)
   - 5 unseen semantic domains (Corporate Ownership, Imperial Seat, Biochemical Substrate,
     Material Craft, Championship Award)

Pipeline Invariants (Zero Modifications):
- Model: Frozen GPT-2 (124M), Layer 8, r=2, alpha=0.25
- Operator: Contrastive Hard Gate O5 (g_t = 1[d_t > 0]) with Frobenius matching scale s
- Candidate Generator: Native G4_sparse (K=4) from target & distractor representations
- Evaluator: Frozen E_CF (d_pos - 0.5 * d_neg) with zero outcome leakage
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
from scipy.stats import spearmanr, kendalltau

# Ensure repository root is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_003_templates import generate_bench_003_templates
from experiments.benchmarks.bench_004_transfer import generate_bench_004_transfer

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

def get_token_span(offsets, start_char, end_char):
    """Finds token indices in offsets matching character range [start_char, end_char]."""
    token_indices = []
    for idx, (s, e) in enumerate(offsets):
        if s is None or e is None or s == e:
            continue
        if max(s, start_char) < min(e, end_char):
            token_indices.append(idx)
    return token_indices

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

def evaluate_suite(dataset, suite_name, model, tokenizer, layer_idx=8, alpha=0.25, rank=2, K=4):
    print(f"\n" + "=" * 90)
    print(f"RUNNING EVALUATION ON {suite_name} (N={len(dataset)})")
    print(f"=" * 90)

    block_idx = layer_idx - 1
    total_forwards = 0

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
        "selected_k_dist": [0] * K,
        "order": [],
        "domain": []
    }

    start_time = time.time()

    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        pos_text = inst["pos"]
        neg_text = inst["neg"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]
        target_evidence_text = inst["target_evidence_text"]
        distractor_evidence_text = inst["distractor_evidence_text"]

        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]

        enc_base = tokenizer(base_text, return_tensors="pt", return_offsets_mapping=True)
        inputs_base = {k: v for k, v in enc_base.items() if k != "offset_mapping"}
        offsets_base = enc_base.offset_mapping[0].tolist()

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
        records["order"].append(inst.get("order", "unknown"))
        records["domain"].append(inst.get("domain", 0))

        # Extract native Layer 8 representations
        h_l = out_base.hidden_states[layer_idx][0]
        d_model = h_l.shape[-1]

        # Extract premise & distractor token ranges using character offset mapping
        idx_target_start = base_text.index(target_evidence_text)
        idx_target_end = idx_target_start + len(target_evidence_text)
        idx_dist_start = base_text.index(distractor_evidence_text)
        idx_dist_end = idx_dist_start + len(distractor_evidence_text)

        target_token_indices = get_token_span(offsets_base, idx_target_start, idx_target_end)
        dist_token_indices = get_token_span(offsets_base, idx_dist_start, idx_dist_end)

        # Fallback safeguard in case of unexpected tokenization boundary
        if len(target_token_indices) == 0:
            target_token_indices = list(range(0, 5))
        if len(dist_token_indices) == 0:
            dist_token_indices = list(range(5, 10))

        h_premise = h_l[target_token_indices]
        h_dist = h_l[dist_token_indices]

        # 2. Oracle-Free Candidate Subspaces
        V_plus, cand_V_minus_list = construct_contrastive_subspaces(h_premise, h_dist, rank=rank, K=K)

        cand_results = []

        # 3. Evaluate each candidate under O5
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
                    else:
                        return h_mod.unsqueeze(0)
                return hook_fn

            hook = model.transformer.h[block_idx].register_forward_hook(make_hook(V_minus, V_plus, alpha))

            with torch.no_grad():
                out_base_cand = model(**inputs_base)
                out_pos_cand = model(**inputs_pos)
                out_neg_cand = model(**inputs_neg)
                total_forwards += 3

            hook.remove()

            q_b_logits = out_base_cand.logits[0, -1]
            q_b_probs = F.softmax(q_b_logits, dim=-1)
            q_p_logits = out_pos_cand.logits[0, -1]
            q_p_probs = F.softmax(q_p_logits, dim=-1)
            q_n_logits = out_neg_cand.logits[0, -1]
            q_n_probs = F.softmax(q_n_logits, dim=-1)

            d_pos = js_divergence(q_b_probs, q_p_probs)
            d_neg = js_divergence(q_b_probs, q_n_probs)
            e_cf_score = d_pos - 0.5 * d_neg

            cand_pred_id = torch.argmax(q_b_logits).item()
            cand_corr = (cand_pred_id == target_id)
            cand_pref = (q_b_probs[target_id].item() > q_b_probs[dist_id].item())
            cand_logp = float(torch.log(q_b_probs[target_id] + 1e-12).item())
            cand_margin = q_b_probs[target_id].item() - q_b_probs[dist_id].item()
            cand_kl = compute_kl_divergence(base_logits, q_b_logits)
            cand_overlap = compute_topk_overlap(base_logits, q_b_logits, k=10)

            sorted_cand = torch.argsort(q_b_logits, descending=True)
            cand_rank = (sorted_cand == target_id).nonzero().item() + 1
            cand_rank_shift = base_rank - cand_rank

            cand_results.append({
                "k": k_idx,
                "e_cf": e_cf_score,
                "corr": cand_corr,
                "pref": cand_pref,
                "logp": cand_logp,
                "delta_logp": cand_logp - base_logp,
                "margin": cand_margin,
                "delta_margin": cand_margin - base_margin,
                "rank_shift": cand_rank_shift,
                "kl": cand_kl,
                "overlap": cand_overlap,
                "probs": q_b_probs
            })

        # 4. Controls & Autonomous Selection
        fixed_v0 = cand_results[0]
        records["fixed_v0_corr"].append(fixed_v0["corr"])
        records["fixed_v0_pref"].append(fixed_v0["pref"])

        rng_cand = random.Random(idx + 1000)
        rand_k = rng_cand.randint(0, K - 1)
        rand_cand = cand_results[rand_k]
        records["rand_cand_corr"].append(rand_cand["corr"])
        records["rand_cand_pref"].append(rand_cand["pref"])

        best_ecf_cand = min(cand_results, key=lambda c: c["e_cf"])
        records["ecf_corr"].append(best_ecf_cand["corr"])
        records["ecf_pref"].append(best_ecf_cand["pref"])
        records["delta_logp_ecf"].append(best_ecf_cand["delta_logp"])
        records["delta_margin_ecf"].append(best_ecf_cand["delta_margin"])
        records["rank_shift_ecf"].append(best_ecf_cand["rank_shift"])
        records["kl_ecf"].append(best_ecf_cand["kl"])
        records["overlap_ecf"].append(best_ecf_cand["overlap"])
        records["selected_k_dist"][best_ecf_cand["k"]] += 1

        # Output competition for E_CF
        probs_ecf = best_ecf_cand["probs"]
        other_probs_ecf = probs_ecf.clone()
        other_probs_ecf[target_id] = -1.0
        other_probs_ecf[dist_id] = -1.0
        p_max_other_ecf = torch.max(other_probs_ecf).item()
        if probs_ecf[dist_id].item() > probs_ecf[target_id].item():
            comp_ecf = "distractor_bias"
        elif probs_ecf[target_id].item() > p_max_other_ecf:
            comp_ecf = "clean_win"
        else:
            comp_ecf = "third_token_intrusion"
        records["comp_ecf"].append(comp_ecf)

        # Oracle Candidate Selection
        oracle_cands = [c for c in cand_results if c["corr"]]
        if len(oracle_cands) > 0:
            best_oracle = max(oracle_cands, key=lambda c: c["margin"])
        else:
            best_oracle = max(cand_results, key=lambda c: c["margin"])
        records["oracle_corr"].append(best_oracle["corr"])
        records["oracle_pref"].append(best_oracle["pref"])

        probs_orc = best_oracle["probs"]
        other_probs_orc = probs_orc.clone()
        other_probs_orc[target_id] = -1.0
        other_probs_orc[dist_id] = -1.0
        p_max_other_orc = torch.max(other_probs_orc).item()
        if probs_orc[dist_id].item() > probs_orc[target_id].item():
            comp_orc = "distractor_bias"
        elif probs_orc[target_id].item() > p_max_other_orc:
            comp_orc = "clean_win"
        else:
            comp_orc = "third_token_intrusion"
        records["comp_oracle"].append(comp_orc)

        records["ecf_oracle_agreement"].append(best_ecf_cand["k"] == best_oracle["k"])

        # Evaluator Ranking Diagnostic
        rank_ecf = [c["e_cf"] for c in cand_results]
        utility_margin = [c["margin"] for c in cand_results]
        try:
            r_val, _ = spearmanr([-e for e in rank_ecf], utility_margin)
            records["spearman_rho"].append(0.0 if np.isnan(r_val) else float(r_val))
        except:
            records["spearman_rho"].append(0.0)

        try:
            t_val, _ = kendalltau([-e for e in rank_ecf], utility_margin)
            records["kendall_tau"].append(0.0 if np.isnan(t_val) else float(t_val))
        except:
            records["kendall_tau"].append(0.0)

        # 5. Haar-Random Orthogonal Subspace Control
        rng_ortho = np.random.RandomState(idx + 5000)
        M_rand = rng_ortho.randn(d_model, rank)
        Q_rand, _ = np.linalg.qr(M_rand)
        V_ortho = torch.tensor(Q_rand, dtype=torch.float32)

        def make_ortho_hook(V_mat, alpha_val):
            def hook_fn(module, input, output):
                if isinstance(output, tuple):
                    h = output[0]
                    rest = output[1:]
                else:
                    h = output
                    rest = None
                P = torch.matmul(V_mat, V_mat.T)
                delta_h = - alpha_val * torch.matmul(h[0], P)
                h_mod = h[0] + delta_h
                if rest is not None:
                    return (h_mod.unsqueeze(0),) + rest
                else:
                    return h_mod.unsqueeze(0)
            return hook_fn

        hook_rand = model.transformer.h[block_idx].register_forward_hook(make_ortho_hook(V_ortho, alpha))
        with torch.no_grad():
            out_rand = model(**inputs_base)
            total_forwards += 1
        hook_rand.remove()

        rand_pred_id = torch.argmax(out_rand.logits[0, -1]).item()
        records["rand_ortho_corr"].append(rand_pred_id == target_id)

    elapsed = time.time() - start_time
    print(f"Completed {total_forwards} forward passes in {elapsed:.2f}s ({elapsed/len(dataset):.3f}s per instance).")

    # Statistical Evaluation
    m_id = float(np.mean(records["identity_corr"]))
    m_ecf = float(np.mean(records["ecf_corr"]))
    m_v0 = float(np.mean(records["fixed_v0_corr"]))
    m_rand = float(np.mean(records["rand_cand_corr"]))
    m_ortho = float(np.mean(records["rand_ortho_corr"]))
    m_orc = float(np.mean(records["oracle_corr"]))

    delta_m = m_ecf - m_id
    delta_headroom = m_orc - m_id
    headroom_recovery = (delta_m / delta_headroom) if delta_headroom > 0 else 0.0

    # Paired McNemar Table
    a = sum(1 for i in range(len(dataset)) if records["identity_corr"][i] and records["ecf_corr"][i])
    b = sum(1 for i in range(len(dataset)) if not records["identity_corr"][i] and records["ecf_corr"][i])
    c = sum(1 for i in range(len(dataset)) if records["identity_corr"][i] and not records["ecf_corr"][i])
    d = sum(1 for i in range(len(dataset)) if not records["identity_corr"][i] and not records["ecf_corr"][i])
    n_disc = b + c

    if n_disc > 0:
        from scipy.stats import binom
        p_one_sided = float(binom.sf(b - 1, n_disc, 0.5))
        p_two_sided = float(min(1.0, 2 * p_one_sided))
    else:
        p_one_sided = 1.0
        p_two_sided = 1.0

    # 10,000-sample bootstrap for Delta M
    bs_rng = np.random.RandomState(42)
    bs_deltas = []
    for _ in range(10000):
        idx_sample = bs_rng.randint(0, len(dataset), len(dataset))
        id_bs = np.array(records["identity_corr"])[idx_sample]
        ecf_bs = np.array(records["ecf_corr"])[idx_sample]
        bs_deltas.append(float(np.mean(ecf_bs) - np.mean(id_bs)))
    ci_low, ci_high = np.percentile(bs_deltas, [2.5, 97.5])

    # 10,000-sample bootstrap for delta logp
    bs_logp = []
    for _ in range(10000):
        idx_sample = bs_rng.randint(0, len(dataset), len(dataset))
        bs_logp.append(float(np.mean(np.array(records["delta_logp_ecf"])[idx_sample])))
    ci_logp_low, ci_logp_high = np.percentile(bs_logp, [2.5, 97.5])

    # Output Competition Counts
    comp_id_counts = {k: records["comp_identity"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}
    comp_ecf_counts = {k: records["comp_ecf"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}
    comp_orc_counts = {k: records["comp_oracle"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}

    # Subgroup analysis by order
    orders = set(records["order"])
    subgroup_order = {}
    for o in orders:
        idxs = [i for i, ord_val in enumerate(records["order"]) if ord_val == o]
        if idxs:
            id_sub = np.mean([records["identity_corr"][i] for i in idxs])
            ecf_sub = np.mean([records["ecf_corr"][i] for i in idxs])
            b_sub = sum(1 for i in idxs if not records["identity_corr"][i] and records["ecf_corr"][i])
            c_sub = sum(1 for i in idxs if records["identity_corr"][i] and not records["ecf_corr"][i])
            subgroup_order[o] = {
                "n": len(idxs),
                "m_id": float(id_sub),
                "m_ecf": float(ecf_sub),
                "delta_m": float(ecf_sub - id_sub),
                "wins_b": b_sub,
                "losses_c": c_sub
            }

    # Subgroup analysis by domain
    subgroup_domain = {}
    for dom_id in range(5):
        idxs = [i for i, d_val in enumerate(records["domain"]) if d_val == dom_id]
        if idxs:
            id_dom = np.mean([records["identity_corr"][i] for i in idxs])
            ecf_dom = np.mean([records["ecf_corr"][i] for i in idxs])
            subgroup_domain[dom_id] = {
                "n": len(idxs),
                "m_id": float(id_dom),
                "m_ecf": float(ecf_dom),
                "delta_m": float(ecf_dom - id_dom)
            }

    summary = {
        "suite_name": suite_name,
        "n_instances": len(dataset),
        "total_forwards": total_forwards,
        "elapsed_seconds": elapsed,
        "m_identity": m_id,
        "m_fixed_v0": m_v0,
        "m_rand_ortho": m_ortho,
        "m_rand_cand": m_rand,
        "m_ecf": m_ecf,
        "m_oracle": m_orc,
        "delta_m": delta_m,
        "headroom_recovery_ratio": headroom_recovery,
        "contingency_table": {"a": a, "b": b, "c": c, "d": d, "n_disc": n_disc},
        "mcnemar_exact_p_one_sided": p_one_sided,
        "mcnemar_exact_p_two_sided": p_two_sided,
        "ci_95_delta_m": [float(ci_low), float(ci_high)],
        "mean_delta_logp": float(np.mean(records["delta_logp_ecf"])),
        "ci_95_delta_logp": [float(ci_logp_low), float(ci_logp_high)],
        "mean_delta_margin": float(np.mean(records["delta_margin_ecf"])),
        "mean_rank_shift": float(np.mean(records["rank_shift_ecf"])),
        "mean_kl": float(np.mean(records["kl_ecf"])),
        "mean_top10_overlap": float(np.mean(records["overlap_ecf"])),
        "oracle_agreement_rate": float(np.mean(records["ecf_oracle_agreement"])),
        "mean_spearman_rho": float(np.mean(records["spearman_rho"])),
        "mean_kendall_tau": float(np.mean(records["kendall_tau"])),
        "selected_k_dist": records["selected_k_dist"],
        "competition": {
            "identity": comp_id_counts,
            "ecf": comp_ecf_counts,
            "oracle": comp_orc_counts
        },
        "subgroup_order": subgroup_order,
        "subgroup_domain": subgroup_domain
    }

    print(f"\n--- {suite_name} RESULTS SUMMARY ---")
    print(f"Identity (M_I):             {m_id:.4f} ({int(m_id*len(dataset))}/{len(dataset)})")
    print(f"Fixed Top Cand (V_0):       {m_v0:.4f}")
    print(f"Rand Ortho Control:         {m_ortho:.4f}")
    print(f"Random Candidate:           {m_rand:.4f}")
    print(f"Autonomous SCBI (M_E_CF):   {m_ecf:.4f} ({int(m_ecf*len(dataset))}/{len(dataset)})")
    print(f"Oracle Upper Bound:         {m_orc:.4f} ({int(m_orc*len(dataset))}/{len(dataset)})")
    print(f"Delta M:                    {delta_m:+.4f} (Headroom Recovery: {headroom_recovery*100:.1f}%)")
    print(f"Contingency Table:          a={a}, b(wins)={b}, c(losses)={c}, d={d}")
    print(f"McNemar Exact p (1-sided):  {p_one_sided:.5f}")
    print(f"Bootstrap 95% CI:           [{ci_low:+.4f}, {ci_high:+.4f}]")
    print(f"Mean Delta log p:           {summary['mean_delta_logp']:+.4f} (CI: [{ci_logp_low:+.4f}, {ci_logp_high:+.4f}])")
    print(f"Candidate Distribution:     {records['selected_k_dist']}")
    print(f"Distractor Bias Drop:       {comp_id_counts['distractor_bias']} -> {comp_ecf_counts['distractor_bias']}")
    if subgroup_order:
        print("Subgroup by Order:")
        for o, sub in subgroup_order.items():
            print(f"  {o}: n={sub['n']}, M_I={sub['m_id']:.3f} -> M_SCBI={sub['m_ecf']:.3f}, Delta={sub['delta_m']:+.3f} (b={sub['wins_b']}, c={sub['losses_c']})")

    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_instances", type=int, default=100, help="Number of instances per suite")
    parser.add_argument("--seed_templates", type=int, default=250, help="Seed for BENCH-003-TEMPLATES")
    parser.add_argument("--seed_transfer", type=int, default=350, help="Seed for BENCH-004-TRANSFER")
    parser.add_argument("--layer", type=int, default=8, help="Locked target layer")
    parser.add_argument("--alpha", type=float, default=0.25, help="Locked operator strength")
    args = parser.parse_args()

    print("=" * 115)
    print("EXP025: CROSS-TEMPLATE AND CROSS-TASK GENERALIZATION BENCHMARK")
    print(f"Model: Frozen GPT-2 (124M) | Layer {args.layer} | alpha = {args.alpha} | N={args.n_instances} per suite")
    print("Zero Modifications Lock: G4_sparse, E_CF (d_pos - 0.5*d_neg), O5 Contrastive Hard Gate")
    print("=" * 115)

    # Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")

    # Generate Datasets
    bench_templates = generate_bench_003_templates(n_instances=args.n_instances, seed=args.seed_templates)
    bench_transfer = generate_bench_004_transfer(n_instances=args.n_instances, seed=args.seed_transfer)

    # Execute Suite A: BENCH-003-TEMPLATES
    summary_templates = evaluate_suite(
        dataset=bench_templates,
        suite_name="BENCH-003-TEMPLATES",
        model=model,
        tokenizer=tokenizer,
        layer_idx=args.layer,
        alpha=args.alpha
    )

    # Execute Suite B: BENCH-004-TRANSFER
    summary_transfer = evaluate_suite(
        dataset=bench_transfer,
        suite_name="BENCH-004-TRANSFER",
        model=model,
        tokenizer=tokenizer,
        layer_idx=args.layer,
        alpha=args.alpha
    )

    post_hash = get_param_hash(model)
    print(f"\n[REPRODUCIBILITY] Post-run GPT-2 Parameter Hash (SHA-256): {post_hash}")
    assert pre_hash == post_hash, "CRITICAL ERROR: Backbone weights modified during inference!"
    print("[REPRODUCIBILITY] Parameter Hash MATCH Confirmed. Frozen Backbone Integrity Verified (Delta theta == 0).")

    # Pooled Multi-Suite Synthesis (N_total = 200)
    pooled_id_corr = summary_templates["m_identity"] * 100 + summary_transfer["m_identity"] * 100
    pooled_ecf_corr = summary_templates["m_ecf"] * 100 + summary_transfer["m_ecf"] * 100
    pooled_m_id = pooled_id_corr / 200.0
    pooled_m_ecf = pooled_ecf_corr / 200.0
    pooled_delta_m = pooled_m_ecf - pooled_m_id
    pooled_b = summary_templates["contingency_table"]["b"] + summary_transfer["contingency_table"]["b"]
    pooled_c = summary_templates["contingency_table"]["c"] + summary_transfer["contingency_table"]["c"]
    pooled_disc = pooled_b + pooled_c

    from scipy.stats import binom
    pooled_p = float(binom.sf(pooled_b - 1, pooled_disc, 0.5)) if pooled_disc > 0 else 1.0

    print("\n" + "=" * 90)
    print("EXP025 OVERALL GENERALIZATION SYNTHESIS (N=200 TOTAL)")
    print("=" * 90)
    print(f"BENCH-003-TEMPLATES: M_I = {summary_templates['m_identity']:.4f} -> M_SCBI = {summary_templates['m_ecf']:.4f} (Delta M = {summary_templates['delta_m']:+.4f}, p = {summary_templates['mcnemar_exact_p_one_sided']:.5f}, b/c = {summary_templates['contingency_table']['b']}/{summary_templates['contingency_table']['c']})")
    print(f"BENCH-004-TRANSFER:  M_I = {summary_transfer['m_identity']:.4f} -> M_SCBI = {summary_transfer['m_ecf']:.4f} (Delta M = {summary_transfer['delta_m']:+.4f}, p = {summary_transfer['mcnemar_exact_p_one_sided']:.5f}, b/c = {summary_transfer['contingency_table']['b']}/{summary_transfer['contingency_table']['c']})")
    print(f"POOLED TRANSFER:     M_I = {pooled_m_id:.4f} -> M_SCBI = {pooled_m_ecf:.4f} (Delta M = {pooled_delta_m:+.4f}, p = {pooled_p:.6f}, b/c = {pooled_b}/{pooled_c})")
    print("=" * 90)

    # Persist JSON artifacts
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP025_generalization"))
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "exp025_generalization_results.json")

    results_data = {
        "metadata": {
            "experiment_id": "EXP025",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model_name": "gpt2",
            "layer": args.layer,
            "alpha": args.alpha,
            "rank": 2,
            "K": 4,
            "pre_param_hash": pre_hash,
            "post_param_hash": post_hash,
            "hash_match": (pre_hash == post_hash)
        },
        "suite_a_templates": summary_templates,
        "suite_b_transfer": summary_transfer,
        "pooled_synthesis": {
            "n_total": 200,
            "pooled_m_identity": pooled_m_id,
            "pooled_m_ecf": pooled_m_ecf,
            "pooled_delta_m": pooled_delta_m,
            "pooled_wins_b": pooled_b,
            "pooled_losses_c": pooled_c,
            "pooled_exact_p": pooled_p
        }
    }

    with open(out_file, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"\n[ARTIFACT] Saved full EXP025 generalization results to: {out_file}")

if __name__ == "__main__":
    main()
