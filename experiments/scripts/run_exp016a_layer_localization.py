"""
EXP016-A: Four-Layer Localization Screen & Residual Diagnostics
Isolates depth (L in {4, 6, 8, 10}) using native G4 sparse dictionary candidate bases.
Model: Frozen GPT-2 (124M, Delta_theta = 0)
Operator: P_0.25 = I - 0.25 * V * V^T (all-token scope)
Dataset: BENCH-002-NL (Development split N=20, dev_seed=123)
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
    """
    Computes D_KL(p || q) at the final sequence position.
    p = baseline (Identity) distribution, q = perturbed (SCBI) distribution.
    """
    p_probs = F.softmax(p_logits, dim=-1)
    q_probs = F.softmax(q_logits, dim=-1)
    # Clip for numerical stability
    q_probs = torch.clamp(q_probs, min=1e-12)
    p_probs = torch.clamp(p_probs, min=1e-12)
    kl = torch.sum(p_probs * (torch.log(p_probs) - torch.log(q_probs))).item()
    return float(kl)

def compute_topk_overlap(p_logits, q_logits, k=10):
    """
    Computes top-k vocabulary token overlap between baseline and perturbed predictions.
    """
    topk_p = set(torch.topk(p_logits, k=k).indices.tolist())
    topk_q = set(torch.topk(q_logits, k=k).indices.tolist())
    return len(topk_p.intersection(topk_q)) / float(k)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_dev", type=int, default=20, help="Number of development instances")
    parser.add_argument("--dev_seed", type=int, default=123, help="Seed for development split")
    parser.add_argument("--alpha", type=float, default=0.25, help="Single-layer continuous operator strength")
    args = parser.parse_args()

    print("=" * 95)
    print("EXP016-A: FOUR-LAYER LOCALIZATION SCREEN & RESIDUAL TRAJECTORY AUDIT")
    print(f"Model: Frozen GPT-2 (124M) | Layers L in {{4, 6, 8, 10}} | N_dev={args.n_dev}, Seed={args.dev_seed}")
    print(f"Candidate Generator: Native G4_sparse | Operator: P_alpha (alpha={args.alpha}) | All-Token")
    print("=" * 95)

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

    target_layers = [4, 6, 8, 10]
    rank = 2
    K = 4

    # Containers for metrics per layer
    layer_records = {
        l: {
            "oracle_corr": [],
            "rand_cand_corr": [],
            "rand_ortho_corr": [],
            "displacements": [],
            "kl_divs": [],
            "top10_overlaps": [],
            "locality": [],
            "diversity": [],
            "stability": []
        }
        for l in target_layers
    }

    identity_correct = []
    total_forwards = 0

    print(f"\nScreening layers {target_layers} natively across {len(dataset)} instances...")

    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]

        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]
        inputs_base = tokenizer(base_text, return_tensors="pt")

        # 1. Unperturbed Baseline Forward Pass
        with torch.no_grad():
            out_base = model(**inputs_base, output_hidden_states=True)
            total_forwards += 1

        base_logits = out_base.logits[0, -1]
        base_pred_id = torch.argmax(base_logits).item()
        base_corr = (base_pred_id == target_id)
        identity_correct.append(base_corr)

        # 2. Iterate over each layer
        for l in target_layers:
            block_idx = l - 1  # 0-indexed block
            h_l = out_base.hidden_states[l][0]  # [seq_len, d_model]
            h_l_norm = torch.norm(h_l).item()

            # Generate NATIVE candidate basis for layer l
            cand_V_list = generate_g4_sparse(h_l, rank=rank, K=K)
            q_metrics = compute_candidate_quality(h_l, cand_V_list, rank=rank)

            layer_records[l]["locality"].append(q_metrics["locality"])
            layer_records[l]["diversity"].append(q_metrics["diversity"])
            layer_records[l]["stability"].append(q_metrics["stability"])

            cand_corrs = []
            cand_disps = []
            cand_kls = []
            cand_overlaps = []

            for V in cand_V_list:
                # Displacement: D_l = alpha * ||h_l V||_F / ||h_l||_F
                proj_norm = torch.norm(torch.matmul(h_l, V)).item()
                disp = args.alpha * (proj_norm / max(h_l_norm, 1e-8))
                cand_disps.append(disp)

                # Hook at layer block output
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
                c_pred_id = torch.argmax(c_logits).item()
                cand_corrs.append(c_pred_id == target_id)

                # Diagnostics
                kl = compute_kl_divergence(base_logits, c_logits)
                overlap = compute_topk_overlap(base_logits, c_logits, k=10)
                cand_kls.append(kl)
                cand_overlaps.append(overlap)

            oracle_c = any(cand_corrs)
            # Random selection from candidate pool
            rk = np.random.randint(0, len(cand_corrs))
            rand_cand_c = cand_corrs[rk]

            # Random Orthogonal Subspace Control at layer l
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
            r_pred_id = torch.argmax(r_logits).item()
            rand_ortho_c = (r_pred_id == target_id)

            # Record per-instance metrics
            layer_records[l]["oracle_corr"].append(oracle_c)
            layer_records[l]["rand_cand_corr"].append(rand_cand_c)
            layer_records[l]["rand_ortho_corr"].append(rand_ortho_c)
            layer_records[l]["displacements"].append(float(np.mean(cand_disps)))
            layer_records[l]["kl_divs"].append(float(np.mean(cand_kls)))
            layer_records[l]["top10_overlaps"].append(float(np.mean(cand_overlaps)))

        if (idx + 1) % 5 == 0 or (idx + 1) == len(dataset):
            print(f"  Processed {idx + 1}/{len(dataset)} instances...")

    elapsed_time = time.time() - start_time
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "CRITICAL: Model parameter hash changed during evaluation!"

    # Aggregate Analysis
    m_identity = float(np.mean(identity_correct))

    summary_results = {
        "metadata": {
            "experiment": "EXP016-A",
            "model": "gpt2 (124M)",
            "generator": "G4_sparse",
            "operator": "P_0.25",
            "n_dev": args.n_dev,
            "dev_seed": args.dev_seed,
            "total_forwards": total_forwards,
            "elapsed_seconds": round(elapsed_time, 2),
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_identical": (pre_hash == post_hash)
        },
        "identity_accuracy": m_identity,
        "layers": {}
    }

    print("\n" + "=" * 95)
    print(f"EXP016-A RESULTS: FOUR-LAYER LOCALIZATION SCREEN (M_Identity = {m_identity:.4f})")
    print("=" * 95)
    print(f"{'Layer':<7} | {'M_Oracle':<9} | {'Delta_M':<8} | {'M_RandCand':<10} | {'M_RandOrtho':<11} | {'Spread':<8} | {'Disp (D_l)':<10} | {'KL (Delta)':<10} | {'Overlap_10':<10}")
    print("-" * 95)

    for l in target_layers:
        rec = layer_records[l]
        m_oracle = float(np.mean(rec["oracle_corr"]))
        delta_m = m_oracle - m_identity
        m_rand_c = float(np.mean(rec["rand_cand_corr"]))
        m_rand_o = float(np.mean(rec["rand_ortho_corr"]))
        spread = m_oracle - m_rand_c
        mean_disp = float(np.mean(rec["displacements"]))
        mean_kl = float(np.mean(rec["kl_divs"]))
        mean_ov = float(np.mean(rec["top10_overlaps"]))

        summary_results["layers"][str(l)] = {
            "M_Oracle": round(m_oracle, 4),
            "Delta_M": round(delta_m, 4),
            "M_RandCand": round(m_rand_c, 4),
            "M_RandOrtho": round(m_rand_o, 4),
            "Spread_Cand": round(spread, 4),
            "Spread_Ortho": round(m_oracle - m_rand_o, 4),
            "Mean_Displacement": round(mean_disp, 4),
            "Mean_KL": round(mean_kl, 4),
            "Mean_Top10_Overlap": round(mean_ov, 4),
            "Locality": round(float(np.mean(rec["locality"])), 4),
            "Diversity": round(float(np.mean(rec["diversity"])), 4),
            "Stability": round(float(np.mean(rec["stability"])), 4)
        }

        print(f"Layer {l:<2} | {m_oracle:<9.4f} | {delta_m:<+8.4f} | {m_rand_c:<10.4f} | {m_rand_o:<11.4f} | {spread:<+8.4f} | {mean_disp:<10.4f} | {mean_kl:<10.4f} | {mean_ov:<10.4f}")

    print("=" * 95)
    print(f"[HASH CHECK] SHA-256 pre == post: {pre_hash == post_hash} (Weight immutability verified)")
    print(f"[RUNTIME] Completed {total_forwards} forward passes in {elapsed_time:.2f}s.")

    # Save results to runs directory
    output_dir = "experiments/runs/EXP016_layer_localization"
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "exp016a_localization_results.json")
    with open(out_path, "w") as f:
        json.dump(summary_results, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
