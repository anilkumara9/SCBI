"""
EXP020-A: Budget-Matched Feature-Dependent Operator Screen
Evaluates budget-normalized conditional token gating at Layer 8 using native G4 sparse dictionary bases (r=2).
Normalizes the token gate so the mean sequence intervention budget matches the linear baseline:
  g_tilde_t = g_t / (1/T * sum_t g_t)  =>  mean(g_tilde_t) = 1.0
Operators Compared:
  - O0: Uniform Linear Baseline (g_tilde_t = 1.0)
  - O3: Budget-Normalized Hard Gate (g_t = 1[e_t > P75(e)], g_tilde_t = g_t / mean(g_t))
  - O4: Budget-Normalized Soft Sigmoid Gate (g_t = sigmoid((e_hat_t - P75(e_hat)) / 1.0), g_tilde_t = g_t / mean(g_t))
Model: Frozen GPT-2 (124M, Delta_theta = 0)
Dataset: BENCH-002-NL (Development split N=20, dev_seed=123)
Diagnostics:
  - Gate budget B = mean(g_tilde_t) = 1.0 (verified matched)
  - Total intervention magnitude A = sum(||h' - h||) / sum(||h||)
  - Partitioned displacements: D_high (on e_t > P75) vs. D_low (on e_t <= P75)
  - Sequence energy concentration: Shannon entropy H(q), H_ratio = H(q)/log(T), N_eff = 1/sum(q^2), N_eff/T
  - Downstream causal propagation at Layer 12: Delta_prop = ||h_12' - h_12||_F / ||h_12||_F
  - Output logit KL divergence and Top-10 vocabulary overlap
  - Margin delta, correct token log-probability delta, and target token rank shift
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
from scbi.generators.activation_cluster import generate_g4_sparse

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

    print("=" * 115)
    print("EXP020-A: BUDGET-MATCHED FEATURE-DEPENDENT OPERATOR SCREEN")
    print(f"Model: Frozen GPT-2 (124M) | Layer {args.layer} (Block {args.layer - 1}) | alpha = {args.alpha} | N_dev={args.n_dev}, Seed={args.dev_seed}")
    print("Operators: O0 (Uniform Linear) vs. O3 (Budget-Norm Hard Gate) vs. O4 (Budget-Norm Soft Gate) | Native G4_sparse (r=2)")
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
    operators = ["O0_linear", "O3_norm_hard_gate", "O4_norm_soft_sigmoid"]

    op_records = {
        op: {
            "oracle_corr": [],
            "rand_cand_corr": [],
            "rand_ortho_corr": [],
            "oracle_pref": [],
            "gate_budget_B": [],
            "intervention_A": [],
            "disp_high": [],
            "disp_low": [],
            "downstream_prop": [],
            "kl_divs": [],
            "overlaps": [],
            "delta_margins": [],
            "delta_logps": [],
            "rank_shifts": []
        }
        for op in operators
    }

    # Concentration records
    energy_entropies = []
    energy_entropy_ratios = []
    energy_n_effs = []
    energy_n_eff_ratios = []

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

        # Native representations
        h_l = out_base.hidden_states[layer_idx][0]  # [seq_len, d_model]
        h_12_base = out_base.hidden_states[12][0]   # [seq_len, d_model] Layer 12 output
        h_12_base_frob = torch.norm(h_12_base).item()
        d_model = h_l.shape[-1]
        seq_len = h_l.shape[0]

        # Generate native G4 sparse candidates (rank=2, K=4)
        cand_V_list = generate_g4_sparse(h_l, rank=rank, K=K)

        # Measure energy concentration metrics across candidate directions
        inst_entropies = []
        inst_entropy_ratios = []
        inst_n_effs = []
        inst_n_eff_ratios = []

        for V in cand_V_list:
            Z = torch.matmul(h_l, V)
            e = torch.norm(Z, dim=-1)
            sum_e = torch.sum(e).item()
            if sum_e > 1e-8:
                q = (e / sum_e).detach().cpu().numpy()
                entropy = -float(np.sum(q * np.log(q + 1e-12)))
                max_entropy = float(np.log(seq_len))
                ent_ratio = entropy / max_entropy if max_entropy > 0 else 1.0
                n_eff = float(1.0 / np.sum(q ** 2))
                n_eff_ratio = n_eff / float(seq_len)
            else:
                entropy = float(np.log(seq_len))
                ent_ratio = 1.0
                n_eff = float(seq_len)
                n_eff_ratio = 1.0

            inst_entropies.append(entropy)
            inst_entropy_ratios.append(ent_ratio)
            inst_n_effs.append(n_eff)
            inst_n_eff_ratios.append(n_eff_ratio)

        energy_entropies.append(float(np.mean(inst_entropies)))
        energy_entropy_ratios.append(float(np.mean(inst_entropy_ratios)))
        energy_n_effs.append(float(np.mean(inst_n_effs)))
        energy_n_eff_ratios.append(float(np.mean(inst_n_eff_ratios)))

        # 2. Evaluate Operators
        for op in operators:
            cand_corrs = []
            cand_prefs = []
            cand_margins = []
            cand_logps = []
            cand_ranks = []
            cand_B = []
            cand_A = []
            cand_d_high = []
            cand_d_low = []
            cand_props = []
            cand_kls = []
            cand_overlaps = []

            for V in cand_V_list:
                # Compute feature activation energy e_t = ||V^T h_t||_2 for t=1..T
                Z = torch.matmul(h_l, V)  # [seq_len, rank]
                e = torch.norm(Z, dim=-1)  # [seq_len]
                e_np = e.detach().cpu().numpy()
                p75_val = float(np.percentile(e_np, 75))

                # Standardized energy for soft sigmoid
                mu_e = float(np.mean(e_np))
                sigma_e = float(np.std(e_np)) + 1e-8
                e_hat = (e - mu_e) / sigma_e
                e_hat_np = e_hat.detach().cpu().numpy()
                tau_soft = float(np.percentile(e_hat_np, 75))

                # Define unnormalized gate g_t
                if op == "O0_linear":
                    g = torch.ones(seq_len, 1, dtype=h_l.dtype, device=h_l.device)
                elif op == "O3_norm_hard_gate":
                    mask = (e > p75_val).float().unsqueeze(-1)
                    g = mask
                elif op == "O4_norm_soft_sigmoid":
                    g = torch.sigmoid((e_hat - tau_soft) / 1.0).unsqueeze(-1)

                # Budget-normalization: g_tilde = g / mean(g)
                mean_g = torch.mean(g).item()
                g_tilde = g / max(mean_g, 1e-8)

                cand_B.append(float(torch.mean(g_tilde).item()))

                # Total intervention magnitude A
                delta_h = args.alpha * g_tilde * torch.matmul(Z, V.T)
                norm_delta = torch.sum(torch.norm(delta_h, dim=-1)).item()
                norm_h = torch.sum(torch.norm(h_l, dim=-1)).item()
                cand_A.append(norm_delta / max(norm_h, 1e-8))

                # Partitioned displacements: D_high vs D_low
                high_mask = (e > p75_val)
                low_mask = ~high_mask
                disp_per_token = torch.norm(delta_h, dim=-1) / torch.clamp(torch.norm(h_l, dim=-1), min=1e-8)
                d_high = float(torch.mean(disp_per_token[high_mask]).item()) if torch.sum(high_mask) > 0 else 0.0
                d_low = float(torch.mean(disp_per_token[low_mask]).item()) if torch.sum(low_mask) > 0 else 0.0
                cand_d_high.append(d_high)
                cand_d_low.append(d_low)

                # Register hook at Layer 8 block output
                def hook_fn(module, input, output):
                    h_curr = output[0].clone()
                    h_token = h_curr[0]
                    z_curr = torch.matmul(h_token, V)
                    e_curr = torch.norm(z_curr, dim=-1)

                    if op == "O0_linear":
                        g_curr = torch.ones(h_token.shape[0], 1, dtype=h_curr.dtype, device=h_curr.device)
                    elif op == "O3_norm_hard_gate":
                        thresh = float(np.percentile(e_curr.detach().cpu().numpy(), 75))
                        g_raw = (e_curr > thresh).float().unsqueeze(-1)
                        g_curr = g_raw / max(float(torch.mean(g_raw).item()), 1e-8)
                    elif op == "O4_norm_soft_sigmoid":
                        e_curr_np = e_curr.detach().cpu().numpy()
                        mu = float(np.mean(e_curr_np))
                        sig = float(np.std(e_curr_np)) + 1e-8
                        e_hat_curr = (e_curr - mu) / sig
                        thresh_soft = float(np.percentile(e_hat_curr.detach().cpu().numpy(), 75))
                        g_raw = torch.sigmoid((e_hat_curr - thresh_soft) / 1.0).unsqueeze(-1)
                        g_curr = g_raw / max(float(torch.mean(g_raw).item()), 1e-8)

                    h_proj = h_token - args.alpha * g_curr * torch.matmul(z_curr, V.T)
                    return (h_proj.unsqueeze(0), *output[1:])

                handle = model.transformer.h[block_idx].register_forward_hook(hook_fn)
                with torch.no_grad():
                    o_cand = model(**inputs_base, output_hidden_states=True)
                    total_forwards += 1
                handle.remove()

                # Downstream causal propagation to Layer 12
                h_12_cand = o_cand.hidden_states[12][0]
                delta_h12 = torch.norm(h_12_cand - h_12_base).item()
                cand_props.append(delta_h12 / max(h_12_base_frob, 1e-8))

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

            # Random Orthogonal Subspace Control under this budget-normalized operator
            rand_mat = torch.randn(d_model, rank)
            V_rand, _ = torch.linalg.qr(rand_mat)

            def rand_hook_fn(module, input, output):
                h_curr = output[0].clone()
                h_token = h_curr[0]
                z_curr = torch.matmul(h_token, V_rand)
                e_curr = torch.norm(z_curr, dim=-1)

                if op == "O0_linear":
                    g_curr = torch.ones(h_token.shape[0], 1, dtype=h_curr.dtype, device=h_curr.device)
                elif op == "O3_norm_hard_gate":
                    thresh = float(np.percentile(e_curr.detach().cpu().numpy(), 75))
                    g_raw = (e_curr > thresh).float().unsqueeze(-1)
                    g_curr = g_raw / max(float(torch.mean(g_raw).item()), 1e-8)
                elif op == "O4_norm_soft_sigmoid":
                    e_curr_np = e_curr.detach().cpu().numpy()
                    mu = float(np.mean(e_curr_np))
                    sig = float(np.std(e_curr_np)) + 1e-8
                    e_hat_curr = (e_curr - mu) / sig
                    thresh_soft = float(np.percentile(e_hat_curr.detach().cpu().numpy(), 75))
                    g_raw = torch.sigmoid((e_hat_curr - thresh_soft) / 1.0).unsqueeze(-1)
                    g_curr = g_raw / max(float(torch.mean(g_raw).item()), 1e-8)

                h_proj = h_token - args.alpha * g_curr * torch.matmul(z_curr, V_rand.T)
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
            op_records[op]["gate_budget_B"].append(float(np.mean(cand_B)))
            op_records[op]["intervention_A"].append(float(np.mean(cand_A)))
            op_records[op]["disp_high"].append(float(np.mean(cand_d_high)))
            op_records[op]["disp_low"].append(float(np.mean(cand_d_low)))
            op_records[op]["downstream_prop"].append(float(np.mean(cand_props)))
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
            "experiment": "EXP020-A",
            "model": "gpt2 (124M)",
            "layer": layer_idx,
            "alpha": args.alpha,
            "subspace_rank": rank,
            "generator": "G4_sparse",
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
        "energy_concentration": {
            "mean_entropy_H": round(float(np.mean(energy_entropies)), 4),
            "mean_entropy_ratio": round(float(np.mean(energy_entropy_ratios)), 4),
            "mean_n_eff": round(float(np.mean(energy_n_effs)), 4),
            "mean_n_eff_ratio": round(float(np.mean(energy_n_eff_ratios)), 4)
        },
        "operators": {}
    }

    print("\n" + "=" * 135)
    print(f"EXP020-A RESULTS: BUDGET-MATCHED OPERATOR SCREEN (M_Identity = {m_identity:.4f}, Pref_Identity = {pref_identity:.4f})")
    print(f"Sequence Energy Concentration: Mean H(q) = {summary_results['energy_concentration']['mean_entropy_H']:.4f} "
          f"({summary_results['energy_concentration']['mean_entropy_ratio']*100:.1f}% max) | "
          f"N_eff = {summary_results['energy_concentration']['mean_n_eff']:.2f} tokens "
          f"({summary_results['energy_concentration']['mean_n_eff_ratio']*100:.1f}% sequence)")
    print("=" * 135)
    print(f"{'Operator':<22} | {'M_Oracle':<8} | {'Delta_M':<8} | {'M_RandCand':<10} | {'Pref_Or':<8} | {'Budget B':<8} | {'D_high':<8} | {'D_low':<8} | {'L12 Prop':<8} | {'KL':<7} | {'Overlap':<7}")
    print("-" * 135)

    for op in operators:
        rec = op_records[op]
        m_oracle = float(np.mean(rec["oracle_corr"]))
        delta_m = m_oracle - m_identity
        m_rand_c = float(np.mean(rec["rand_cand_corr"]))
        m_rand_o = float(np.mean(rec["rand_ortho_corr"]))
        pref_or = float(np.mean(rec["oracle_pref"]))
        mean_b = float(np.mean(rec["gate_budget_B"]))
        mean_a = float(np.mean(rec["intervention_A"]))
        d_high = float(np.mean(rec["disp_high"]))
        d_low = float(np.mean(rec["disp_low"]))
        d_prop = float(np.mean(rec["downstream_prop"]))
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
            "Mean_Gate_Budget_B": round(mean_b, 4),
            "Total_Intervention_A": round(mean_a, 4),
            "Displacement_High": round(d_high, 4),
            "Displacement_Low": round(d_low, 4),
            "Downstream_Prop_L12": round(d_prop, 4),
            "Mean_KL": round(kl, 4),
            "Mean_Top10_Overlap": round(ov, 4),
            "Delta_Margin": round(d_margin, 4),
            "Delta_Logp": round(d_logp, 4),
            "Target_Rank_Shift": round(r_shift, 4)
        }

        print(f"{op:<22} | {m_oracle:<8.4f} | {delta_m:<+8.4f} | {m_rand_c:<10.4f} | {pref_or:<8.4f} | {mean_b:<8.4f} | {d_high:<8.4f} | {d_low:<8.4f} | {d_prop:<8.4f} | {kl:<7.4f} | {ov:<7.4f}")

    print("=" * 135)
    print(f"[REPRODUCIBILITY] SHA-256 pre == post: {pre_hash == post_hash} (Parameter immutability verified)")
    print(f"[RUNTIME] Completed {total_forwards} forward passes in {elapsed_time:.2f}s.")

    out_dir = "experiments/runs/EXP020_budget_matched"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp020a_budget_matched_results.json")
    with open(out_path, "w") as f:
        json.dump(summary_results, f, indent=2)
    print(f"[PERSISTENCE] Results saved to {out_path}")

if __name__ == "__main__":
    main()
