"""
EXP018-A: Subspace Rank Capacity Screen (r in {2, 4, 8})
Isolates subspace rank capacity at Layer 8 using native G4 sparse dictionary bases.
Model: Frozen GPT-2 (124M, Delta_theta = 0)
Operator: P_0.25 = I - 0.25 * V_r * V_r^T (all-token scope, Layer 8)
Dataset: BENCH-002-NL (Development split N=20, dev_seed=123)
Diagnostics:
  - Displacement D_r = 0.25 * ||H V_r||_F / ||H||_F
  - Logit KL divergence D_KL(p_I || p_SCBI)
  - Top-10 vocabulary overlap Overlap_10
  - Probability margin Delta Margin
  - Target token log-probability delta Delta log p
  - Target token rank shift Delta rank
"""

import os
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
    parser.add_argument("--n_dev", type=int, default=20, help="Number of development instances")
    parser.add_argument("--dev_seed", type=int, default=123, help="Seed for development split")
    parser.add_argument("--layer", type=int, default=8, help="Locked target layer")
    parser.add_argument("--alpha", type=float, default=0.25, help="Locked operator strength")
    args = parser.parse_args()

    print("=" * 110)
    print("EXP018-A: SUBSPACE RANK CAPACITY SCREEN (r in {2, 4, 8})")
    print(f"Model: Frozen GPT-2 (124M) | Layer {args.layer} (Block {args.layer - 1}) | alpha = {args.alpha} | N_dev={args.n_dev}, Seed={args.dev_seed}")
    print("Candidate Generator: Native G4_sparse | All-Token Residual Projection")
    print("=" * 110)

    np.random.seed(args.dev_seed)
    torch.manual_seed(args.dev_seed)
    start_time = time.time()

    # 1. Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")

    # 2. Load BENCH-002-NL Development Dataset
    dataset = generate_bench_002_nl(n_instances=args.n_dev, seed=args.dev_seed)
    print(f"[DATASET] Loaded {len(dataset)} development instances.")

    layer_idx = args.layer
    block_idx = layer_idx - 1  # Block 7 for Layer 8
    ranks = [2, 4, 8]
    K = 4

    rank_records = {
        r: {
            "oracle_corr": [],
            "rand_cand_corr": [],
            "rand_ortho_corr": [],
            "oracle_pref": [],
            "displacements": [],
            "kl_divs": [],
            "overlaps": [],
            "delta_margins": [],
            "delta_logps": [],
            "rank_shifts": [],
            "locality": [],
            "diversity": [],
            "stability": []
        }
        for r in ranks
    }

    identity_correct = []
    identity_pref = []
    total_forwards = 0

    print(f"\nScreening ranks {ranks} across {len(dataset)} development instances...")

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

        # Extract native Layer 8 hidden states
        h_l = out_base.hidden_states[layer_idx][0]  # [seq_len, d_model]
        h_l_norm = torch.norm(h_l).item()
        d_model = h_l.shape[-1]

        # 2. Evaluate Each Subspace Rank
        for r in ranks:
            cand_V_list = generate_g4_sparse(h_l, rank=r, K=K)
            q_metrics = compute_candidate_quality(h_l, cand_V_list, rank=r)

            rank_records[r]["locality"].append(q_metrics["locality"])
            rank_records[r]["diversity"].append(q_metrics["diversity"])
            rank_records[r]["stability"].append(q_metrics["stability"])

            cand_corrs = []
            cand_prefs = []
            cand_margins = []
            cand_logps = []
            cand_ranks = []
            cand_disps = []
            cand_kls = []
            cand_overlaps = []

            for V in cand_V_list:
                # Displacement: D_r = alpha * ||H V_r||_F / ||H||_F
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

            # Random Orthogonal Subspace Control of rank r
            rand_mat = torch.randn(d_model, r)
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
            r_pred_id = torch.argmax(r_logits).item()
            rand_ortho_c = (r_pred_id == target_id)

            rank_records[r]["oracle_corr"].append(oracle_c)
            rank_records[r]["rand_cand_corr"].append(rand_cand_c)
            rank_records[r]["rand_ortho_corr"].append(rand_ortho_c)
            rank_records[r]["oracle_pref"].append(oracle_p)
            rank_records[r]["displacements"].append(float(np.mean(cand_disps)))
            rank_records[r]["kl_divs"].append(float(np.mean(cand_kls)))
            rank_records[r]["overlaps"].append(float(np.mean(cand_overlaps)))
            rank_records[r]["delta_margins"].append(float(np.mean(cand_margins)))
            rank_records[r]["delta_logps"].append(float(np.mean(cand_logps)))
            rank_records[r]["rank_shifts"].append(float(np.mean(cand_ranks)))

        if (idx + 1) % 5 == 0 or (idx + 1) == len(dataset):
            print(f"  Processed {idx + 1}/{len(dataset)} development instances...")

    elapsed_time = time.time() - start_time
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "CRITICAL: Model parameter hash changed during evaluation!"

    m_identity = float(np.mean(identity_correct))
    pref_identity = float(np.mean(identity_pref))

    summary_results = {
        "metadata": {
            "experiment": "EXP018-A",
            "model": "gpt2 (124M)",
            "layer": layer_idx,
            "alpha": args.alpha,
            "generator": "G4_sparse",
            "ranks_tested": ranks,
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
        "ranks": {}
    }

    print("\n" + "=" * 115)
    print(f"EXP018-A RESULTS: SUBSPACE RANK CAPACITY SCREEN (M_Identity = {m_identity:.4f}, Pref_Identity = {pref_identity:.4f})")
    print("=" * 115)
    print(f"{'Rank (r)':<9} | {'M_Oracle':<8} | {'Delta_M':<8} | {'M_RandCand':<10} | {'M_RandOrtho':<11} | {'Pref_Or':<8} | {'Disp (D_r)':<10} | {'KL (Delta)':<10} | {'Overlap_10':<10} | {'Delta_Marg':<10}")
    print("-" * 115)

    for r in ranks:
        rec = rank_records[r]
        m_oracle = float(np.mean(rec["oracle_corr"]))
        delta_m = m_oracle - m_identity
        m_rand_c = float(np.mean(rec["rand_cand_corr"]))
        m_rand_o = float(np.mean(rec["rand_ortho_corr"]))
        pref_or = float(np.mean(rec["oracle_pref"]))
        disp = float(np.mean(rec["displacements"]))
        kl = float(np.mean(rec["kl_divs"]))
        ov = float(np.mean(rec["overlaps"]))
        d_margin = float(np.mean(rec["delta_margins"]))
        d_logp = float(np.mean(rec["delta_logps"]))
        r_shift = float(np.mean(rec["rank_shifts"]))

        summary_results["ranks"][str(r)] = {
            "M_Oracle": round(m_oracle, 4),
            "Delta_M": round(delta_m, 4),
            "M_RandCand": round(m_rand_c, 4),
            "M_RandOrtho": round(m_rand_o, 4),
            "Spread_Cand": round(m_oracle - m_rand_c, 4),
            "Spread_Ortho": round(m_oracle - m_rand_o, 4),
            "Pref_Oracle": round(pref_or, 4),
            "Mean_Displacement": round(disp, 4),
            "Mean_KL": round(kl, 4),
            "Mean_Top10_Overlap": round(ov, 4),
            "Delta_Margin": round(d_margin, 4),
            "Delta_Logp": round(d_logp, 4),
            "Target_Rank_Shift": round(r_shift, 4),
            "Locality": round(float(np.mean(rec["locality"])), 4),
            "Diversity": round(float(np.mean(rec["diversity"])), 4),
            "Stability": round(float(np.mean(rec["stability"])), 4)
        }

        print(f"r = {r:<5} | {m_oracle:<8.4f} | {delta_m:<+8.4f} | {m_rand_c:<10.4f} | {m_rand_o:<11.4f} | {pref_or:<8.4f} | {disp:<10.4f} | {kl:<10.4f} | {ov:<10.4f} | {d_margin:<+10.4f}")

    print("=" * 115)
    print(f"[REPRODUCIBILITY] SHA-256 pre == post: {pre_hash == post_hash} (Parameter immutability verified)")
    print(f"[RUNTIME] Completed {total_forwards} forward passes in {elapsed_time:.2f}s.")

    out_dir = "experiments/runs/EXP018_rank_capacity"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp018a_rank_results.json")
    with open(out_path, "w") as f:
        json.dump(summary_results, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
