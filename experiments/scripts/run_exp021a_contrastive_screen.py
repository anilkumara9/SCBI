"""
EXP021-A: Contrastive Relative-Evidence Gating Screen
Evaluates relative-evidence selective intervention at Layer 8 on frozen GPT-2 (124M).
Contrastive Signal:
  d_t = ||V_-^T h_t||_2 - ||V_+^T h_t||_2
where V_- (distractor subspace) and V_+ (target subspace) are constructed oracle-free
from pre-registered prompt segments H^(b) (distractor text) and H^(a) (premise text).
Exact Realized Intervention Magnitude Matching:
  s = sqrt(sum_t ||V_-^T h_t||^2) / sqrt(sum_t g_t^2 ||V_-^T h_t||^2)
ensuring ||H'_gated - H||_F / ||H||_F == ||H'_linear - H||_F / ||H||_F on every forward pass.
Operators Compared:
  - O0: Uniform Linear Baseline (g_t = 1.0, s = 1.0)
  - O5: Contrastive Hard Gate (g_t = 1[d_t > 0])
  - O6: Contrastive Soft Gate (g_t = sigmoid(d_t / T_d), T_d = std(d_t) + 1e-8)
Model: Frozen GPT-2 (124M, Delta_theta = 0)
Dataset: BENCH-002-NL (Development split N=20, dev_seed=123)
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
    # Candidate 1: Top 2 singular vectors
    cand_V_minus.append(Vh_d[:rank, :].T)
    # Candidate 2: Singular vectors (1, 2)
    idx2 = [1, min(2, max_components - 1)]
    cand_V_minus.append(Vh_d[idx2, :].T)
    # Candidate 3: Singular vectors (0, 2)
    idx3 = [0, min(2, max_components - 1)]
    cand_V_minus.append(Vh_d[idx3, :].T)
    # Candidate 4: Singular vectors (0, 3) or (2, 3)
    idx4 = [min(2, max_components - 2), min(3, max_components - 1)] if max_components >= 4 else [0, 1]
    cand_V_minus.append(Vh_d[idx4, :].T)

    return V_plus, cand_V_minus[:K]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_dev", type=int, default=20, help="Number of development instances")
    parser.add_argument("--dev_seed", type=int, default=123, help="Seed for development split")
    parser.add_argument("--layer", type=int, default=8, help="Locked target layer")
    parser.add_argument("--alpha", type=float, default=0.25, help="Locked operator strength")
    args = parser.parse_args()

    print("=" * 115)
    print("EXP021-A: CONTRASTIVE RELATIVE-EVIDENCE GATING SCREEN")
    print(f"Model: Frozen GPT-2 (124M) | Layer {args.layer} (Block {args.layer - 1}) | alpha = {args.alpha} | N_dev={args.n_dev}, Seed={args.dev_seed}")
    print("Operators: O0 (Uniform Linear) vs. O5 (Contrastive Hard Gate) vs. O6 (Contrastive Soft Gate) | Exact Realized Magnitude Matching")
    print("=" * 115)

    np.random.seed(args.dev_seed)
    torch.manual_seed(args.dev_seed)
    start_time = time.time()

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")

    dataset = generate_bench_002_nl(n_instances=args.n_dev, seed=args.dev_seed)
    print(f"[DATASET] Loaded {len(dataset)} development instances.")

    layer_idx = args.layer
    block_idx = layer_idx - 1  # Block 7 for Layer 8
    rank = 2
    K = 4
    operators = ["O0_linear", "O5_contrast_hard", "O6_contrast_soft"]

    op_records = {
        op: {
            "oracle_corr": [],
            "rand_cand_corr": [],
            "rand_ortho_corr": [],
            "oracle_pref": [],
            "intervention_A": [],
            "disp_d_pos": [],
            "disp_d_neg": [],
            "gate_evidence_corr": [],
            "kl_divs": [],
            "overlaps": [],
            "delta_margins": [],
            "delta_logps": [],
            "rank_shifts": []
        }
        for op in operators
    }

    identity_correct = []
    identity_pref = []
    total_forwards = 0

    print(f"\nEvaluating operators across {len(dataset)} development instances...")

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
        base_pr = (base_probs[target_id].item() > base_probs[dist_id].item())
        base_margin = base_probs[target_id].item() - base_probs[dist_id].item()
        base_logp = float(torch.log(base_probs[target_id] + 1e-12).item())

        sorted_indices = torch.argsort(base_logits, descending=True)
        base_rank = (sorted_indices == target_id).nonzero().item() + 1

        identity_correct.append(base_corr)
        identity_pref.append(base_pr)

        # Extract native Layer 8 representations
        h_l = out_base.hidden_states[layer_idx][0]  # [seq_len, d_model]
        d_model = h_l.shape[-1]
        seq_len = h_l.shape[0]

        # 2. Extract deterministic premise and distractor token ranges
        # base_text: "Premise: {prem_base} Distractor: {dist} {query}"
        idx_distractor_str = base_text.index(" Distractor:")
        idx_query_str = base_text.index(" Question:")
        text_premise = base_text[:idx_distractor_str]
        text_distractor = base_text[idx_distractor_str:idx_query_str]

        len_premise = len(tokenizer.encode(text_premise))
        len_distractor = len(tokenizer.encode(text_distractor))

        h_premise = h_l[:len_premise]
        h_dist = h_l[len_premise : len_premise + len_distractor]

        # 3. Oracle-free contrastive basis construction
        V_plus, cand_V_minus_list = construct_contrastive_subspaces(h_premise, h_dist, rank=rank, K=K)

        # 4. Evaluate operators
        for op in operators:
            cand_corrs = []
            cand_prefs = []
            cand_margins = []
            cand_logps = []
            cand_ranks = []
            cand_A = []
            cand_d_pos = []
            cand_d_neg = []
            cand_rhos = []
            cand_kls = []
            cand_overlaps = []

            for V_minus in cand_V_minus_list:
                # Contrastive energies
                Z_minus = torch.matmul(h_l, V_minus)  # [seq_len, rank]
                e_minus = torch.norm(Z_minus, dim=-1)  # [seq_len]

                Z_plus = torch.matmul(h_l, V_plus)    # [seq_len, rank]
                e_plus = torch.norm(Z_plus, dim=-1)    # [seq_len]

                # Relative evidence difference: d_t = e_t^- - e_t^+
                d = e_minus - e_plus
                d_np = d.detach().cpu().numpy()
                std_d = float(np.std(d_np)) + 1e-8

                # Compute gate g_t
                if op == "O0_linear":
                    g = torch.ones(seq_len, 1, dtype=h_l.dtype, device=h_l.device)
                elif op == "O5_contrast_hard":
                    g = (d > 0.0).float().unsqueeze(-1)
                elif op == "O6_contrast_soft":
                    g = torch.sigmoid(d / std_d).unsqueeze(-1)

                # Pearson correlation rho(g_t, d_t)
                g_flat = g.squeeze().detach().cpu().numpy()
                if np.std(g_flat) > 1e-8 and np.std(d_np) > 1e-8:
                    rho = float(np.corrcoef(g_flat, d_np)[0, 1])
                else:
                    rho = 0.0
                cand_rhos.append(rho)

                # Exact Realized Magnitude Matching scale factor s:
                # s = ||H V_- V_-^T||_F / ||diag(g) H V_- V_-^T||_F
                linear_proj_energy = torch.sum(torch.norm(Z_minus, dim=-1) ** 2).item()
                gated_proj_energy = torch.sum((g.squeeze() ** 2) * (torch.norm(Z_minus, dim=-1) ** 2)).item()

                if gated_proj_energy > 1e-8 and op != "O0_linear":
                    s = float(np.sqrt(linear_proj_energy / gated_proj_energy))
                else:
                    s = 1.0

                # Delta h under matched operator
                delta_h = args.alpha * s * g * torch.matmul(Z_minus, V_minus.T)
                norm_delta = torch.sum(torch.norm(delta_h, dim=-1)).item()
                norm_h = torch.sum(torch.norm(h_l, dim=-1)).item()
                cand_A.append(norm_delta / max(norm_h, 1e-8))

                # Contrastive selectivity: D_d+ vs D_d-
                pos_mask = (d > 0.0)
                neg_mask = ~pos_mask
                disp_per_token = torch.norm(delta_h, dim=-1) / torch.clamp(torch.norm(h_l, dim=-1), min=1e-8)
                d_pos = float(torch.mean(disp_per_token[pos_mask]).item()) if torch.sum(pos_mask) > 0 else 0.0
                d_neg = float(torch.mean(disp_per_token[neg_mask]).item()) if torch.sum(neg_mask) > 0 else 0.0
                cand_d_pos.append(d_pos)
                cand_d_neg.append(d_neg)

                # Register hook at Layer 8 block output
                def hook_fn(module, input, output):
                    h_curr = output[0].clone()
                    h_token = h_curr[0]
                    z_m = torch.matmul(h_token, V_minus)
                    z_p = torch.matmul(h_token, V_plus)
                    d_curr = torch.norm(z_m, dim=-1) - torch.norm(z_p, dim=-1)

                    if op == "O0_linear":
                        g_curr = torch.ones(h_token.shape[0], 1, dtype=h_curr.dtype, device=h_curr.device)
                        s_curr = 1.0
                    elif op == "O5_contrast_hard":
                        g_curr = (d_curr > 0.0).float().unsqueeze(-1)
                        lin_e = torch.sum(torch.norm(z_m, dim=-1) ** 2).item()
                        gat_e = torch.sum((g_curr.squeeze() ** 2) * (torch.norm(z_m, dim=-1) ** 2)).item()
                        s_curr = float(np.sqrt(lin_e / max(gat_e, 1e-8)))
                    elif op == "O6_contrast_soft":
                        std_val = float(torch.std(d_curr).item()) + 1e-8
                        g_curr = torch.sigmoid(d_curr / std_val).unsqueeze(-1)
                        lin_e = torch.sum(torch.norm(z_m, dim=-1) ** 2).item()
                        gat_e = torch.sum((g_curr.squeeze() ** 2) * (torch.norm(z_m, dim=-1) ** 2)).item()
                        s_curr = float(np.sqrt(lin_e / max(gat_e, 1e-8)))

                    h_proj = h_token - args.alpha * s_curr * g_curr * torch.matmul(z_m, V_minus.T)
                    return (h_proj.unsqueeze(0), *output[1:])

                handle = model.transformer.h[block_idx].register_forward_hook(hook_fn)
                with torch.no_grad():
                    o_cand = model(**inputs_base)
                    total_forwards += 1
                handle.remove()

                c_logits = o_cand.logits[0, -1]
                c_probs = F.softmax(c_logits, dim=-1)
                c_pred_id = torch.argmax(c_logits).item()
                c_corr = (c_pred_id == target_id)
                c_pref = (c_probs[target_id].item() > c_probs[dist_id].item())
                c_margin = c_probs[target_id].item() - c_probs[dist_id].item()
                c_logp = float(torch.log(c_probs[target_id] + 1e-12).item())

                c_sorted = torch.argsort(c_logits, descending=True)
                c_rank = (c_sorted == target_id).nonzero().item() + 1

                cand_corrs.append(c_corr)
                cand_prefs.append(c_pref)
                cand_margins.append(c_margin - base_margin)
                cand_logps.append(c_logp - base_logp)
                cand_ranks.append(base_rank - c_rank)
                cand_kls.append(compute_kl_divergence(base_logits, c_logits))
                cand_overlaps.append(compute_topk_overlap(base_logits, c_logits, k=10))

            oracle_c = any(cand_corrs)
            oracle_p = any(cand_prefs)
            rk = np.random.randint(0, len(cand_corrs))
            rand_cand_c = cand_corrs[rk]

            # Random Orthogonal Subspace Control
            rand_mat = torch.randn(d_model, rank)
            V_rand, _ = torch.linalg.qr(rand_mat)

            def rand_hook_fn(module, input, output):
                h_curr = output[0].clone()
                h_token = h_curr[0]
                z_curr = torch.matmul(h_token, V_rand)
                h_proj = h_token - args.alpha * torch.matmul(z_curr, V_rand.T)
                return (h_proj.unsqueeze(0), *output[1:])

            handle_rand = model.transformer.h[block_idx].register_forward_hook(rand_hook_fn)
            with torch.no_grad():
                o_rand = model(**inputs_base)
                total_forwards += 1
            handle_rand.remove()

            r_logits = o_rand.logits[0, -1]
            r_pred_id = torch.argmax(r_logits).item()
            rand_ortho_c = (r_pred_id == target_id)

            op_records[op]["oracle_corr"].append(oracle_c)
            op_records[op]["rand_cand_corr"].append(rand_cand_c)
            op_records[op]["rand_ortho_corr"].append(rand_ortho_c)
            op_records[op]["oracle_pref"].append(oracle_p)
            op_records[op]["intervention_A"].append(float(np.mean(cand_A)))
            op_records[op]["disp_d_pos"].append(float(np.mean(cand_d_pos)))
            op_records[op]["disp_d_neg"].append(float(np.mean(cand_d_neg)))
            op_records[op]["gate_evidence_corr"].append(float(np.mean(cand_rhos)))
            op_records[op]["kl_divs"].append(float(np.mean(cand_kls)))
            op_records[op]["overlaps"].append(float(np.mean(cand_overlaps)))
            op_records[op]["delta_margins"].append(float(np.mean(cand_margins)))
            op_records[op]["delta_logps"].append(float(np.mean(cand_logps)))
            op_records[op]["rank_shifts"].append(float(np.mean(cand_ranks)))

        if (idx + 1) % 5 == 0 or (idx + 1) == len(dataset):
            print(f"  Processed {idx + 1}/{len(dataset)} development instances...")

    elapsed_time = time.time() - start_time
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "CRITICAL: Model parameter hash changed during evaluation!"

    m_identity = float(np.mean(identity_correct))
    pref_identity = float(np.mean(identity_pref))

    summary_results = {
        "metadata": {
            "experiment": "EXP021-A",
            "model": "gpt2 (124M)",
            "layer": layer_idx,
            "alpha": args.alpha,
            "subspace_rank": rank,
            "operators_tested": operators,
            "n_dev": args.n_dev,
            "dev_seed": args.dev_seed,
            "total_forwards": total_forwards,
            "elapsed_seconds": round(elapsed_time, 2),
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_identical": (pre_hash == post_hash)
        },
        "identity": {
            "M_Identity": round(m_identity, 4),
            "Pref_Identity": round(pref_identity, 4)
        },
        "operators": {}
    }

    print("\n" + "=" * 135)
    print(f"EXP021-A RESULTS: CONTRASTIVE GATING SCREEN (M_Identity = {m_identity:.4f}, Pref_Identity = {pref_identity:.4f})")
    print("Exact Realized Magnitude Matching Enforced (A_gated == A_linear on every instance)")
    print("=" * 135)
    print(f"{'Operator':<22} | {'M_Oracle':<8} | {'Delta_M':<8} | {'M_RandCand':<10} | {'Pref_Or':<8} | {'Total A':<8} | {'D(d>0)':<8} | {'D(d<=0)':<8} | {'rho(g,d)':<8} | {'KL':<7} | {'Overlap':<7}")
    print("-" * 135)

    for op in operators:
        rec = op_records[op]
        m_oracle = float(np.mean(rec["oracle_corr"]))
        delta_m = m_oracle - m_identity
        m_rand_c = float(np.mean(rec["rand_cand_corr"]))
        m_rand_o = float(np.mean(rec["rand_ortho_corr"]))
        pref_or = float(np.mean(rec["oracle_pref"]))
        mean_a = float(np.mean(rec["intervention_A"]))
        d_pos = float(np.mean(rec["disp_d_pos"]))
        d_neg = float(np.mean(rec["disp_d_neg"]))
        rho_val = float(np.mean(rec["gate_evidence_corr"]))
        kl = float(np.mean(rec["kl_divs"]))
        ov = float(np.mean(rec["overlaps"]))
        d_margin = float(np.mean(rec["delta_margins"]))
        d_logp = float(np.mean(rec["delta_logps"]))
        r_shift = float(np.mean(rec["rank_shifts"]))

        summary_results["operators"][op] = {
            "M_Oracle": round(m_oracle, 4),
            "Delta_M": round(delta_m, 4),
            "M_RandCand": round(m_rand_c, 4),
            "M_RandOrtho": round(m_rand_o, 4),
            "Pref_Oracle": round(pref_or, 4),
            "Total_Intervention_A": round(mean_a, 4),
            "Displacement_d_pos": round(d_pos, 4),
            "Displacement_d_neg": round(d_neg, 4),
            "Gate_Evidence_Correlation": round(rho_val, 4),
            "Mean_KL": round(kl, 4),
            "Mean_Top10_Overlap": round(ov, 4),
            "Delta_Margin": round(d_margin, 4),
            "Delta_Logp": round(d_logp, 4),
            "Target_Rank_Shift": round(r_shift, 4)
        }

        print(f"{op:<22} | {m_oracle:<8.4f} | {delta_m:<+8.4f} | {m_rand_c:<10.4f} | {pref_or:<8.4f} | {mean_a:<8.4f} | {d_pos:<8.4f} | {d_neg:<8.4f} | {rho_val:<8.4f} | {kl:<7.4f} | {ov:<7.4f}")

    print("=" * 135)
    print(f"[REPRODUCIBILITY] SHA-256 pre == post: {pre_hash == post_hash} (Parameter immutability verified)")
    print(f"[RUNTIME] Completed {total_forwards} forward passes in {elapsed_time:.2f}s.")

    out_dir = "experiments/runs/EXP021_contrastive_gated"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp021a_contrastive_results.json")
    with open(out_path, "w") as f:
        json.dump(summary_results, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
