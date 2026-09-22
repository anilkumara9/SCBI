"""
EXP017-A: Coordinated Multi-Layer SCBI Development Screen
Evaluates distributed weak interventions across multiple depths ({6,8}, {8,10}, {4,8}, {4,6,8,10})
under conserved budget A_total = 0.25 (alpha_l = 0.25 / n).
Compares:
  - M1: Independent Bases (generated from unperturbed trajectory)
  - M2: Sequential Adaptive Bases (iteratively generated from transformed representations)
Elevated metrics:
  - Top-1 Accuracy M and Delta M
  - Cross-layer synergy: Delta M_combined - sum(Delta M_l)
  - Probability Margin Delta: Delta Margin = [p(target) - p(distractor)]_SCBI - [p(target) - p(distractor)]_I
  - Log-Probability Delta: Delta log p(target)
  - Target Token Rank Shift: Delta rank(target)
  - Output logit KL divergence and Top-10 vocabulary overlap
Model: Frozen GPT-2 (124M, Delta_theta = 0)
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
    parser.add_argument("--total_budget", type=float, default=0.25, help="Conserved total intervention budget")
    args = parser.parse_args()

    print("=" * 105)
    print("EXP017-A: COORDINATED MULTI-LAYER SCBI DEVELOPMENT SCREEN & SYNERGY AUDIT")
    print(f"Model: Frozen GPT-2 (124M) | Budget A_total = {args.total_budget} (alpha_l = 0.25/n) | N_dev={args.n_dev}, Seed={args.dev_seed}")
    print("Candidate Generator: Native G4_sparse | Mechanisms: M1 (Independent) vs. M2 (Sequential Adaptive)")
    print("=" * 105)

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

    # Configurations to test
    configs = {
        "6_8": [6, 8],
        "8_10": [8, 10],
        "4_8": [4, 8],
        "4_6_8_10": [4, 6, 8, 10]
    }
    mechanisms = ["M1_independent", "M2_sequential"]
    rank = 2
    K = 4

    # Single-layer baseline deltas from EXP016-A for synergy computation
    single_layer_deltas = {4: 0.0000, 6: 0.0500, 8: 0.1500, 10: 0.1000}

    # Tracking containers
    results_matrix = {
        f"{cfg_name}_{mech}": {
            "layers": layers,
            "mechanism": mech,
            "alpha_l": args.total_budget / len(layers),
            "oracle_corr": [],
            "rand_cand_corr": [],
            "oracle_pref": [],
            "delta_margins": [],
            "delta_logps": [],
            "rank_shifts": [],
            "displacements": [],
            "kl_divs": [],
            "overlaps": []
        }
        for cfg_name, layers in configs.items()
        for mech in mechanisms
    }

    identity_correct = []
    identity_pref = []
    total_forwards = 0

    print(f"\nExecuting multi-layer screen across {len(dataset)} development instances...")

    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]

        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]
        inputs_base = tokenizer(base_text, return_tensors="pt")

        # 1. Baseline Forward Pass
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
        
        # Rank of target token (1-indexed)
        sorted_indices = torch.argsort(base_logits, descending=True)
        base_rank = (sorted_indices == target_id).nonzero().item() + 1

        identity_correct.append(base_corr)
        identity_pref.append(base_pr)

        # Precompute unperturbed native bases for all layers (for M1)
        native_bases_unperturbed = {}
        for l in [4, 6, 8, 10]:
            h_l = out_base.hidden_states[l][0]
            native_bases_unperturbed[l] = generate_g4_sparse(h_l, rank=rank, K=K)

        # 2. Iterate over configurations and mechanisms
        for cfg_name, layers in configs.items():
            n_layers = len(layers)
            alpha_l = args.total_budget / n_layers

            # ---- Mechanism 1: Independent Bases ----
            m1_key = f"{cfg_name}_M1_independent"
            m1_cand_corrs = []
            m1_cand_prefs = []
            m1_cand_margins = []
            m1_cand_logps = []
            m1_cand_ranks = []
            m1_cand_disps = []
            m1_cand_kls = []
            m1_cand_overlaps = []

            for k in range(K):
                # Register simultaneous hooks at all layers in configuration
                handles = []
                cum_disp = 0.0
                for l in layers:
                    block_idx = l - 1
                    V = native_bases_unperturbed[l][k]
                    h_l = out_base.hidden_states[l][0]
                    proj_norm = torch.norm(torch.matmul(h_l, V)).item()
                    cum_disp += alpha_l * (proj_norm / max(torch.norm(h_l).item(), 1e-8))

                    def make_hook(v_mat, a_val):
                        def hook(module, input, output):
                            h = output[0].clone()
                            h_proj = h - a_val * torch.matmul(torch.matmul(h, v_mat), v_mat.T)
                            return (h_proj, *output[1:])
                        return hook

                    handle = model.transformer.h[block_idx].register_forward_hook(make_hook(V, alpha_l))
                    handles.append(handle)

                with torch.no_grad():
                    o_cand = model(**inputs_base)
                    total_forwards += 1

                for h in handles:
                    h.remove()

                c_logits = o_cand.logits[0, -1]
                c_probs = F.softmax(c_logits, dim=-1)
                c_pred_id = torch.argmax(c_logits).item()
                c_corr = (c_pred_id == target_id)
                c_pref = (c_probs[target_id].item() > c_probs[dist_id].item())
                c_margin = c_probs[target_id].item() - c_probs[dist_id].item()
                c_logp = float(torch.log(c_probs[target_id] + 1e-12).item())

                c_sorted = torch.argsort(c_logits, descending=True)
                c_rank = (c_sorted == target_id).nonzero().item() + 1

                m1_cand_corrs.append(c_corr)
                m1_cand_prefs.append(c_pref)
                m1_cand_margins.append(c_margin - base_margin)
                m1_cand_logps.append(c_logp - base_logp)
                m1_cand_ranks.append(base_rank - c_rank)  # positive means improved rank
                m1_cand_disps.append(cum_disp / n_layers)
                m1_cand_kls.append(compute_kl_divergence(base_logits, c_logits))
                m1_cand_overlaps.append(compute_topk_overlap(base_logits, c_logits, k=10))

            results_matrix[m1_key]["oracle_corr"].append(any(m1_cand_corrs))
            rk = np.random.randint(0, len(m1_cand_corrs))
            results_matrix[m1_key]["rand_cand_corr"].append(m1_cand_corrs[rk])
            results_matrix[m1_key]["oracle_pref"].append(any(m1_cand_prefs))
            results_matrix[m1_key]["delta_margins"].append(float(np.mean(m1_cand_margins)))
            results_matrix[m1_key]["delta_logps"].append(float(np.mean(m1_cand_logps)))
            results_matrix[m1_key]["rank_shifts"].append(float(np.mean(m1_cand_ranks)))
            results_matrix[m1_key]["displacements"].append(float(np.mean(m1_cand_disps)))
            results_matrix[m1_key]["kl_divs"].append(float(np.mean(m1_cand_kls)))
            results_matrix[m1_key]["overlaps"].append(float(np.mean(m1_cand_overlaps)))

            # ---- Mechanism 2: Sequential Adaptive Bases ----
            m2_key = f"{cfg_name}_M2_sequential"
            m2_cand_corrs = []
            m2_cand_prefs = []
            m2_cand_margins = []
            m2_cand_logps = []
            m2_cand_ranks = []
            m2_cand_disps = []
            m2_cand_kls = []
            m2_cand_overlaps = []

            for k in range(K):
                # Sequential progression:
                # Start with basis at first layer l_1
                current_handles = []
                cum_disp = 0.0

                first_layer = layers[0]
                V_first = native_bases_unperturbed[first_layer][k]

                def make_hook(v_mat, a_val):
                    def hook(module, input, output):
                        h = output[0].clone()
                        h_proj = h - a_val * torch.matmul(torch.matmul(h, v_mat), v_mat.T)
                        return (h_proj, *output[1:])
                    return hook

                h1 = model.transformer.h[first_layer - 1].register_forward_hook(make_hook(V_first, alpha_l))
                current_handles.append(h1)

                # For subsequent layers, propagate forward under current hooks, extract adapted hidden states
                for i in range(1, len(layers)):
                    next_layer = layers[i]
                    with torch.no_grad():
                        out_intermediate = model(**inputs_base, output_hidden_states=True)
                        total_forwards += 1
                    
                    h_next = out_intermediate.hidden_states[next_layer][0]
                    # Generate adapted basis from this transformed representation state
                    adapted_bases = generate_g4_sparse(h_next, rank=rank, K=K)
                    V_next = adapted_bases[k]

                    h_next_hook = model.transformer.h[next_layer - 1].register_forward_hook(make_hook(V_next, alpha_l))
                    current_handles.append(h_next_hook)

                # Final forward pass under all adapted hooks
                with torch.no_grad():
                    o_m2 = model(**inputs_base)
                    total_forwards += 1

                for h in current_handles:
                    h.remove()

                m2_logits = o_m2.logits[0, -1]
                m2_probs = F.softmax(m2_logits, dim=-1)
                m2_pred_id = torch.argmax(m2_logits).item()
                m2_corr = (m2_pred_id == target_id)
                m2_pref = (m2_probs[target_id].item() > m2_probs[dist_id].item())
                m2_margin = m2_probs[target_id].item() - m2_probs[dist_id].item()
                m2_logp = float(torch.log(m2_probs[target_id] + 1e-12).item())

                m2_sorted = torch.argsort(m2_logits, descending=True)
                m2_rank = (m2_sorted == target_id).nonzero().item() + 1

                m2_cand_corrs.append(m2_corr)
                m2_cand_prefs.append(m2_pref)
                m2_cand_margins.append(m2_margin - base_margin)
                m2_cand_logps.append(m2_logp - base_logp)
                m2_cand_ranks.append(base_rank - m2_rank)
                m2_cand_kls.append(compute_kl_divergence(base_logits, m2_logits))
                m2_cand_overlaps.append(compute_topk_overlap(base_logits, m2_logits, k=10))

            results_matrix[m2_key]["oracle_corr"].append(any(m2_cand_corrs))
            rk2 = np.random.randint(0, len(m2_cand_corrs))
            results_matrix[m2_key]["rand_cand_corr"].append(m2_cand_corrs[rk2])
            results_matrix[m2_key]["oracle_pref"].append(any(m2_cand_prefs))
            results_matrix[m2_key]["delta_margins"].append(float(np.mean(m2_cand_margins)))
            results_matrix[m2_key]["delta_logps"].append(float(np.mean(m2_cand_logps)))
            results_matrix[m2_key]["rank_shifts"].append(float(np.mean(m2_cand_ranks)))
            results_matrix[m2_key]["displacements"].append(0.0) # Tracked qualitatively
            results_matrix[m2_key]["kl_divs"].append(float(np.mean(m2_cand_kls)))
            results_matrix[m2_key]["overlaps"].append(float(np.mean(m2_cand_overlaps)))

        if (idx + 1) % 5 == 0 or (idx + 1) == len(dataset):
            print(f"  Processed {idx + 1}/{len(dataset)} development instances...")

    elapsed_time = time.time() - start_time
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "CRITICAL: Model parameter hash changed during evaluation!"

    m_identity = float(np.mean(identity_correct))
    pref_identity = float(np.mean(identity_pref))

    summary_results = {
        "metadata": {
            "experiment": "EXP017-A",
            "model": "gpt2 (124M)",
            "generator": "G4_sparse",
            "total_budget": args.total_budget,
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
        "configurations": {}
    }

    print("\n" + "=" * 115)
    print(f"EXP017-A RESULTS: COORDINATED MULTI-LAYER SCBI SCREEN (M_Identity = {m_identity:.4f}, Pref_Identity = {pref_identity:.4f})")
    print("=" * 115)
    print(f"{'Config':<18} | {'Mech':<12} | {'M_Oracle':<8} | {'Delta_M':<8} | {'Synergy':<8} | {'Pref_Or':<8} | {'Delta_Marg':<10} | {'Delta_logp':<10} | {'Rank_Shift':<10} | {'Overlap_10':<10}")
    print("-" * 115)

    for key, data in results_matrix.items():
        layers = data["layers"]
        mech = data["mechanism"]
        m_oracle = float(np.mean(data["oracle_corr"]))
        delta_m = m_oracle - m_identity
        sum_delta_l = sum(single_layer_deltas[l] for l in layers)
        synergy = delta_m - sum_delta_l
        pref_or = float(np.mean(data["oracle_pref"]))
        d_margin = float(np.mean(data["delta_margins"]))
        d_logp = float(np.mean(data["delta_logps"]))
        r_shift = float(np.mean(data["rank_shifts"]))
        ov = float(np.mean(data["overlaps"]))
        kl = float(np.mean(data["kl_divs"]))

        cfg_label = f"{{{','.join(map(str, layers))}}}"
        mech_short = "M1-Indep" if "M1" in mech else "M2-SeqAdapt"

        summary_results["configurations"][key] = {
            "layers": layers,
            "mechanism": mech,
            "alpha_per_layer": round(data["alpha_l"], 4),
            "M_Oracle": round(m_oracle, 4),
            "Delta_M": round(delta_m, 4),
            "Sum_Single_Delta": round(sum_delta_l, 4),
            "Cross_Layer_Synergy": round(synergy, 4),
            "Pref_Oracle": round(pref_or, 4),
            "Delta_Margin": round(d_margin, 4),
            "Delta_Logp": round(d_logp, 4),
            "Target_Rank_Shift": round(r_shift, 4),
            "Mean_KL": round(kl, 4),
            "Mean_Top10_Overlap": round(ov, 4)
        }

        print(f"{cfg_label:<18} | {mech_short:<12} | {m_oracle:<8.4f} | {delta_m:<+8.4f} | {synergy:<+8.4f} | {pref_or:<8.4f} | {d_margin:<+10.4f} | {d_logp:<+10.4f} | {r_shift:<+10.4f} | {ov:<10.4f}")

    print("=" * 115)
    print(f"[REPRODUCIBILITY] SHA-256 pre == post: {pre_hash == post_hash} (Parameter immutability verified)")
    print(f"[RUNTIME] Completed {total_forwards} forward passes in {elapsed_time:.2f}s.")

    out_dir = "experiments/runs/EXP017_multilayer_coordination"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp017a_screen_results.json")
    with open(out_path, "w") as f:
        json.dump(summary_results, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
