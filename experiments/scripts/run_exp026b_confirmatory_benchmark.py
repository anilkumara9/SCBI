"""
EXP026-B: Cross-Architecture Confirmatory Benchmark.

Evaluates the frozen, autonomous SCBI pipeline across distinct foundation models on BENCH-002-NL (N=100, Seed 84):
1. Reference: GPT-2 Small (124M, 12 layers, d_model=768) at Layer 8 (lambda = 8/12 = 0.667)
2. Regime 1 (Scale Transfer): GPT-2 Medium (355M, 24 layers, d_model=1024) at Layer 16 (lambda = 16/24 = 0.667)
3. Regime 2 (Architecture Transfer): Pythia-160m (160M, 12 layers, d_model=768, RoPE + parallel attention/MLP) at Layer 8 (lambda = 8/12 = 0.667)

Frozen Pipeline Invariants (Zero Modifications):
- r = 2, alpha = 0.25
- Operator: Contrastive Hard Gate O5 (g_t = 1[d_t > 0]) with Frobenius matching scale factor s
- Candidate Generator: Native G4_sparse (K=4)
- Evaluator: Frozen E_CF (d_pos - 0.5 * d_neg)
- Pre-declared normalized depth: lambda = l / L_blocks = 0.667
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

def js_divergence(p, q):
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

def evaluate_architecture(model_name, model_type, target_layer, n_instances=100, seed=84, alpha=0.25, rank=2, K=4):
    print(f"\n" + "=" * 100)
    print(f"EVALUATING ARCHITECTURE: {model_name} (Layer {target_layer}, alpha={alpha}, N={n_instances}, Seed={seed})")
    print(f"=" * 100)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run SHA-256 Parameter Hash: {pre_hash}")

    block_idx = target_layer - 1
    dataset = generate_bench_002_nl(n_instances=n_instances, seed=seed)
    print(f"[DATASET] Loaded {len(dataset)} confirmatory instances.")

    records = {
        "identity_corr": [],
        "fixed_v0_corr": [],
        "rand_cand_corr": [],
        "rand_ortho_corr": [],
        "ecf_corr": [],
        "oracle_corr": [],
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

    start_time = time.time()
    total_forwards = 0

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
        base_logp = float(torch.log(base_probs[target_id] + 1e-12).item())
        base_margin = base_probs[target_id].item() - base_probs[dist_id].item()

        sorted_base = torch.argsort(base_logits, descending=True)
        base_rank = (sorted_base == target_id).nonzero().item() + 1

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
        records["comp_identity"].append(comp_id)

        h_l = out_base.hidden_states[target_layer][0]
        d_model = h_l.shape[-1]

        idx_dist_str = base_text.index(" Distractor:")
        idx_query_str = base_text.index(" Question:")
        text_prem = base_text[:idx_dist_str]
        text_dist = base_text[idx_dist_str:idx_query_str]

        len_prem = len(tokenizer.encode(text_prem))
        len_dist = len(tokenizer.encode(text_dist))

        h_premise = h_l[:len_prem]
        h_dist = h_l[len_prem : len_prem + len_dist]

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
                    else:
                        return h_mod.unsqueeze(0)
                return hook_fn

            target_module = get_hook_target(model, model_type, block_idx)
            hook = target_module.register_forward_hook(make_hook(V_minus, V_plus, alpha))

            with torch.no_grad():
                out_b = model(**inputs_base)
                out_p = model(**inputs_pos)
                out_n = model(**inputs_neg)
                total_forwards += 3

            hook.remove()

            q_b_logits = out_b.logits[0, -1]
            q_b_probs = F.softmax(q_b_logits, dim=-1)
            q_p_probs = F.softmax(out_p.logits[0, -1], dim=-1)
            q_n_probs = F.softmax(out_n.logits[0, -1], dim=-1)

            d_pos = js_divergence(q_b_probs, q_p_probs)
            d_neg = js_divergence(q_b_probs, q_n_probs)
            e_cf = d_pos - 0.5 * d_neg

            cand_pred_id = torch.argmax(q_b_logits).item()
            cand_corr = (cand_pred_id == target_id)
            cand_margin = q_b_probs[target_id].item() - q_b_probs[dist_id].item()
            cand_logp = float(torch.log(q_b_probs[target_id] + 1e-12).item())
            cand_kl = compute_kl_divergence(base_logits, q_b_logits)
            cand_overlap = compute_topk_overlap(base_logits, q_b_logits, k=10)

            sorted_cand = torch.argsort(q_b_logits, descending=True)
            cand_rank = (sorted_cand == target_id).nonzero().item() + 1
            cand_rank_shift = base_rank - cand_rank

            cand_results.append({
                "k": k_idx,
                "e_cf": e_cf,
                "corr": cand_corr,
                "margin": cand_margin,
                "logp": cand_logp,
                "delta_logp": cand_logp - base_logp,
                "delta_margin": cand_margin - base_margin,
                "rank_shift": cand_rank_shift,
                "kl": cand_kl,
                "overlap": cand_overlap,
                "probs": q_b_probs
            })

        # Controls & Selection
        fixed_v0 = cand_results[0]
        records["fixed_v0_corr"].append(fixed_v0["corr"])

        rng_c = random.Random(idx + 2000)
        rand_k = rng_c.randint(0, K - 1)
        rand_cand = cand_results[rand_k]
        records["rand_cand_corr"].append(rand_cand["corr"])

        best_ecf = min(cand_results, key=lambda c: c["e_cf"])
        records["ecf_corr"].append(best_ecf["corr"])
        records["delta_logp_ecf"].append(best_ecf["delta_logp"])
        records["delta_margin_ecf"].append(best_ecf["delta_margin"])
        records["rank_shift_ecf"].append(best_ecf["rank_shift"])
        records["kl_ecf"].append(best_ecf["kl"])
        records["overlap_ecf"].append(best_ecf["overlap"])
        records["selected_k_dist"][best_ecf["k"]] += 1

        probs_ecf = best_ecf["probs"]
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

        oracle_cands = [c for c in cand_results if c["corr"]]
        best_oracle = max(oracle_cands, key=lambda c: c["margin"]) if oracle_cands else cand_results[0]
        records["oracle_corr"].append(best_oracle["corr"])

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

        records["ecf_oracle_agreement"].append(best_ecf["k"] == best_oracle["k"])

        # Evaluator correlations
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

        # Haar-Random Orthogonal Control
        rng_ortho = np.random.RandomState(idx + 7000)
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

        hook_rand = target_module.register_forward_hook(make_ortho_hook(V_ortho, alpha))
        with torch.no_grad():
            out_rand = model(**inputs_base)
            total_forwards += 1
        hook_rand.remove()
        records["rand_ortho_corr"].append(torch.argmax(out_rand.logits[0, -1]).item() == target_id)

    elapsed = time.time() - start_time
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "CRITICAL ERROR: Parameter hash mismatch!"

    m_id = float(np.mean(records["identity_corr"]))
    m_ecf = float(np.mean(records["ecf_corr"]))
    m_v0 = float(np.mean(records["fixed_v0_corr"]))
    m_rand = float(np.mean(records["rand_cand_corr"]))
    m_ortho = float(np.mean(records["rand_ortho_corr"]))
    m_orc = float(np.mean(records["oracle_corr"]))

    delta_m = m_ecf - m_id
    delta_headroom = m_orc - m_id
    eta_hr = (delta_m / delta_headroom) if delta_headroom > 0 else 0.0

    a = sum(1 for i in range(len(dataset)) if records["identity_corr"][i] and records["ecf_corr"][i])
    b = sum(1 for i in range(len(dataset)) if not records["identity_corr"][i] and records["ecf_corr"][i])
    c = sum(1 for i in range(len(dataset)) if records["identity_corr"][i] and not records["ecf_corr"][i])
    d = sum(1 for i in range(len(dataset)) if not records["identity_corr"][i] and not records["ecf_corr"][i])
    n_disc = b + c

    p_one_sided = float(binom.sf(b - 1, n_disc, 0.5)) if n_disc > 0 else 1.0
    p_two_sided = float(min(1.0, 2 * p_one_sided))

    bs_rng = np.random.RandomState(42)
    bs_deltas = []
    for _ in range(10000):
        idx_s = bs_rng.randint(0, len(dataset), len(dataset))
        id_bs = np.array(records["identity_corr"])[idx_s]
        ecf_bs = np.array(records["ecf_corr"])[idx_s]
        bs_deltas.append(float(np.mean(ecf_bs) - np.mean(id_bs)))
    ci_low, ci_high = np.percentile(bs_deltas, [2.5, 97.5])

    bs_logp = []
    for _ in range(10000):
        idx_s = bs_rng.randint(0, len(dataset), len(dataset))
        bs_logp.append(float(np.mean(np.array(records["delta_logp_ecf"])[idx_s])))
    ci_logp_low, ci_logp_high = np.percentile(bs_logp, [2.5, 97.5])

    comp_id_counts = {k: records["comp_identity"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}
    comp_ecf_counts = {k: records["comp_ecf"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}
    comp_orc_counts = {k: records["comp_oracle"].count(k) for k in ["clean_win", "distractor_bias", "third_token_intrusion"]}

    summary = {
        "model_name": model_name,
        "model_type": model_type,
        "d_model": d_model,
        "target_layer": target_layer,
        "normalized_depth": target_layer / (24 if "medium" in model_name else 12),
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "m_identity": m_id,
        "m_fixed_v0": m_v0,
        "m_rand_ortho": m_ortho,
        "m_rand_cand": m_rand,
        "m_ecf": m_ecf,
        "m_oracle": m_orc,
        "delta_m": delta_m,
        "eta_hr": eta_hr,
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
        }
    }

    print(f"\n--- RESULTS SUMMARY FOR {model_name} ---")
    print(f"Identity (M_I):             {m_id:.4f} ({int(m_id*n_instances)}/{n_instances})")
    print(f"Fixed Top Cand (V_0):       {m_v0:.4f}")
    print(f"Rand Ortho Control:         {m_ortho:.4f}")
    print(f"Random Candidate:           {m_rand:.4f}")
    print(f"Autonomous SCBI (M_E_CF):   {m_ecf:.4f} ({int(m_ecf*n_instances)}/{n_instances})")
    print(f"Oracle Upper Bound:         {m_orc:.4f} ({int(m_orc*n_instances)}/{n_instances})")
    print(f"Delta M:                    {delta_m:+.4f} (Headroom Recovery eta_HR: {eta_hr*100:.1f}%)")
    print(f"Contingency Table:          a={a}, b(wins)={b}, c(losses)={c}, d={d}")
    print(f"McNemar Exact p (1-sided):  {p_one_sided:.5f}")
    print(f"Bootstrap 95% CI:           [{ci_low:+.4f}, {ci_high:+.4f}]")
    print(f"Mean Delta log p:           {summary['mean_delta_logp']:+.4f} (CI: [{ci_logp_low:+.4f}, {ci_logp_high:+.4f}])")
    print(f"Candidate Distribution:     {records['selected_k_dist']}")
    print(f"Distractor Bias Drop:       {comp_id_counts['distractor_bias']} -> {comp_ecf_counts['distractor_bias']}")
    print(f"Third Token Intrusion:      {comp_id_counts['third_token_intrusion']} -> {comp_ecf_counts['third_token_intrusion']}")

    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_instances", type=int, default=100, help="Number of confirmatory instances")
    parser.add_argument("--seed", type=int, default=84, help="Confirmatory seed")
    parser.add_argument("--alpha", type=float, default=0.25, help="Locked operator strength")
    args = parser.parse_args()

    print("=" * 115)
    print("EXP026-B: CROSS-ARCHITECTURE CONFIRMATORY BENCHMARK")
    print(f"BENCH-002-NL (N={args.n_instances}, Seed={args.seed}) | Invariant Normalized Depth: lambda = 0.667")
    print("Zero Retuning Rule: G4_sparse, E_CF, O5 Contrastive Hard Gate, alpha=0.25, rank=2")
    print("=" * 115)

    architectures = [
        # 1. Baseline Reference: GPT-2 Small
        {"name": "gpt2", "type": "gpt2", "layer": 8},
        # 2. Regime 1: GPT-2 Medium (Scale Transfer: 24 layers, d_model=1024)
        {"name": "gpt2-medium", "type": "gpt2", "layer": 16},
        # 3. Regime 2: Pythia-160m (Architecture Family Transfer: RoPE + parallel attention/MLP)
        {"name": "EleutherAI/pythia-160m", "type": "pythia", "layer": 8}
    ]

    all_summaries = {}
    for arch in architectures:
        summary = evaluate_architecture(
            model_name=arch["name"],
            model_type=arch["type"],
            target_layer=arch["layer"],
            n_instances=args.n_instances,
            seed=args.seed,
            alpha=args.alpha
        )
        all_summaries[arch["name"]] = summary

    # Synthesis Table
    print("\n" + "=" * 115)
    print("EXP026-B CROSS-ARCHITECTURE CONFIRMATORY SYNTHESIS (BENCH-002-NL, N=100, Seed 84)")
    print("=" * 115)
    print(f"{'Architecture':<25} | {'Layers':<6} | {'d_model':<8} | {'M_I':<6} | {'M_SCBI':<7} | {'M_Oracle':<8} | {'Delta M':<8} | {'eta_HR':<8} | {'Exact p':<8} | {'95% CI':<16}")
    print("-" * 115)
    for name, s in all_summaries.items():
        ci_str = f"[{s['ci_95_delta_m'][0]:+.2f}, {s['ci_95_delta_m'][1]:+.2f}]"
        print(f"{name:<25} | {s['target_layer']:<6} | {s['d_model']:<8} | {s['m_identity']:<6.3f} | {s['m_ecf']:<7.3f} | {s['m_oracle']:<8.3f} | {s['delta_m']:<+8.3f} | {s['eta_hr']*100:<7.1f}% | {s['mcnemar_exact_p_one_sided']:<8.4f} | {ci_str:<16}")
    print("=" * 115)

    # Persist JSON artifacts
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP026_architecture"))
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "exp026_architecture_results.json")

    with open(out_file, "w") as f:
        json.dump(all_summaries, f, indent=2)
    print(f"\n[ARTIFACT] Saved full EXP026 cross-architecture confirmatory results to: {out_file}")

if __name__ == "__main__":
    main()
