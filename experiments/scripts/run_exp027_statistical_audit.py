"""
EXP027 Statistical Robustness and Layer Disparity Audit.

Computes:
1. Bootstrap 95% Confidence Intervals (10,000 resamples) for Oracle Headroom, Selectivity Index, and Delta log p across Pythia layers.
2. Exact paired McNemar test comparing Layer 4 vs. Layer 8 Oracle predictions.
3. Paired Wilcoxon test comparing Layer 4 vs. Layer 8 target log-probability gains.
"""

import os
import sys
import json
import random
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from scipy.stats import binom, wilcoxon

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

def bootstrap_ci(arr, num_samples=10000, ci=0.95):
    arr = np.array(arr)
    n = len(arr)
    means = []
    rng = np.random.RandomState(84)
    for _ in range(num_samples):
        boot_idx = rng.randint(0, n, n)
        means.append(np.mean(arr[boot_idx]))
    alpha = (1.0 - ci) / 2.0
    low = np.percentile(means, 100 * alpha)
    high = np.percentile(means, 100 * (1.0 - alpha))
    return float(low), float(high)

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

def segment_tokens(offsets, text):
    p_end = text.index(" Distractor:")
    d_end = text.index(" Question:")
    prem_indices = [i for i, (s, e) in enumerate(offsets) if e <= p_end and s < e]
    dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
    quest_indices = [i for i, (s, e) in enumerate(offsets) if s >= d_end and s < e]
    return prem_indices, dist_indices, quest_indices

def main():
    print("=" * 90)
    print("RUNNING EXP027 STATISTICAL ROBUSTNESS AUDIT (Pythia-160M Layer Profile)")
    print("=" * 90)

    n_instances = 100
    seed = 84
    dataset = generate_bench_002_nl(n_instances=n_instances, seed=seed)

    model_name = "EleutherAI/pythia-160m"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    layers_to_audit = [2, 4, 6, 8, 10, 11]
    layer_records = {l: {"oracle_corr": [], "delta_m": [], "si": [], "delta_logp": []} for l in layers_to_audit}

    base_corr_list = []

    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]

        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]

        enc_base = tokenizer(base_text, return_tensors="pt", return_offsets_mapping=True)
        offsets = enc_base["offset_mapping"][0].tolist()
        input_ids = enc_base["input_ids"]

        prem_idx, dist_idx, quest_idx = segment_tokens(offsets, base_text)

        with torch.no_grad():
            out_base = model(input_ids=input_ids, output_hidden_states=True)

        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred = torch.argmax(base_logits).item()
        base_is_corr = (base_pred == target_id)
        base_corr_list.append(base_is_corr)
        base_logp = float(torch.log(base_probs[target_id] + 1e-12).item())

        for layer in layers_to_audit:
            block_idx = layer - 1
            target_module = model.gpt_neox.layers[block_idx]

            h_l = out_base.hidden_states[layer][0]
            h_premise = h_l[prem_idx]
            h_dist = h_l[dist_idx]

            V_plus, cand_V_minus_list = construct_contrastive_subspaces(h_premise, h_dist, rank=2, K=4)

            cand_corrs = []
            cand_logps = []
            for V_minus in cand_V_minus_list:
                def make_hook(V_minus_mat, V_plus_mat, alpha_val=0.25):
                    def hook_fn(module, input, output):
                        h = output[0] if isinstance(output, tuple) else output
                        rest = output[1:] if isinstance(output, tuple) else None
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
                        scale = frob_linear / frob_gated if frob_gated > 1e-12 else 1.0

                        h_mod = h_t + scale * delta_gated_raw
                        return (h_mod.unsqueeze(0),) + rest if rest is not None else h_mod.unsqueeze(0)
                    return hook_fn

                hook = target_module.register_forward_hook(make_hook(V_minus, V_plus))
                with torch.no_grad():
                    out_cand = model(input_ids=input_ids)
                hook.remove()

                cand_logits = out_cand.logits[0, -1]
                cand_pred = torch.argmax(cand_logits).item()
                c_corr = (cand_pred == target_id)
                cand_probs = F.softmax(cand_logits, dim=-1)
                c_logp = float(torch.log(cand_probs[target_id] + 1e-12).item())

                cand_corrs.append(c_corr)
                cand_logps.append(c_logp)

            # Oracle candidate
            is_oracle_corr = any(cand_corrs)
            best_idx = np.argmax(cand_logps)
            oracle_delta_logp = cand_logps[best_idx] - base_logp

            # Separability
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
            si = g_rate_dist - g_rate_prem

            layer_records[layer]["oracle_corr"].append(int(is_oracle_corr))
            layer_records[layer]["delta_m"].append(int(is_oracle_corr) - int(base_is_corr))
            layer_records[layer]["si"].append(si)
            layer_records[layer]["delta_logp"].append(oracle_delta_logp)

    # 1. Compute layer statistics and bootstrap CIs
    report_stats = {}
    for l in layers_to_audit:
        rec = layer_records[l]
        dm_mean = np.mean(rec["delta_m"])
        dm_ci = bootstrap_ci(rec["delta_m"])

        si_mean = np.mean(rec["si"])
        si_ci = bootstrap_ci(rec["si"])

        dlogp_mean = np.mean(rec["delta_logp"])
        dlogp_ci = bootstrap_ci(rec["delta_logp"])

        report_stats[f"layer_{l}"] = {
            "layer": l,
            "oracle_acc": float(np.mean(rec["oracle_corr"])),
            "delta_m": float(dm_mean),
            "delta_m_ci95": list(dm_ci),
            "si": float(si_mean),
            "si_ci95": list(si_ci),
            "delta_logp": float(dlogp_mean),
            "delta_logp_ci95": list(dlogp_ci)
        }

    # 2. Pairwise Test: Layer 4 vs Layer 8
    l4_corr = np.array(layer_records[4]["oracle_corr"])
    l8_corr = np.array(layer_records[8]["oracle_corr"])

    # Contingency table
    # a: both 1, b: L4=1, L8=0 (L4 wins), c: L4=0, L8=1 (L8 wins), d: both 0
    a = int(np.sum((l4_corr == 1) & (l8_corr == 1)))
    b = int(np.sum((l4_corr == 1) & (l8_corr == 0)))
    c = int(np.sum((l4_corr == 0) & (l8_corr == 1)))
    d = int(np.sum((l4_corr == 0) & (l8_corr == 0)))

    n_discordant = b + c
    if n_discordant > 0:
        p_val_mcnemar = float(binom.cdf(min(b, c), n_discordant, 0.5) * 2.0)
        p_val_one_sided = float(1.0 - binom.cdf(b - 1, n_discordant, 0.5))
    else:
        p_val_mcnemar = 1.0
        p_val_one_sided = 1.0

    # Wilcoxon signed rank test on target delta_logp (L4 vs L8)
    l4_dlogp = np.array(layer_records[4]["delta_logp"])
    l8_dlogp = np.array(layer_records[8]["delta_logp"])
    diff_dlogp = l4_dlogp - l8_dlogp
    w_stat, w_pval = wilcoxon(l4_dlogp, l8_dlogp, alternative="greater")

    pairwise_res = {
        "comparison": "Layer 4 vs. Layer 8",
        "l4_oracle_acc": float(np.mean(l4_corr)),
        "l8_oracle_acc": float(np.mean(l8_corr)),
        "headroom_diff": float(np.mean(l4_corr) - np.mean(l8_corr)),
        "contingency_table": {"a_both_correct": a, "b_l4_win": b, "c_l8_win": c, "d_both_incorrect": d},
        "mcnemar_b": b,
        "mcnemar_c": c,
        "mcnemar_p_two_sided": float(p_val_mcnemar),
        "mcnemar_p_one_sided": float(p_val_one_sided),
        "mean_dlogp_diff": float(np.mean(diff_dlogp)),
        "wilcoxon_stat": float(w_stat),
        "wilcoxon_p_one_sided": float(w_pval)
    }

    final_results = {
        "layer_profiles": report_stats,
        "pairwise_l4_vs_l8": pairwise_res
    }

    out_file = "experiments/runs/EXP027_decomposition/exp027_statistical_robustness.json"
    with open(out_file, "w") as f:
        json.dump(final_results, f, indent=2)

    print("\n" + "=" * 90)
    print("EXP027 STATISTICAL ROBUSTNESS RESULTS:")
    print("=" * 90)
    for l in layers_to_audit:
        st = report_stats[f"layer_{l}"]
        print(f"Layer {l:2d}: Headroom={st['delta_m']:+.4f} (95% CI: [{st['delta_m_ci95'][0]:+.4f}, {st['delta_m_ci95'][1]:+.4f}]), "
              f"SI={st['si']:.4f} ([{st['si_ci95'][0]:.4f}, {st['si_ci95'][1]:.4f}]), "
              f"Δlogp={st['delta_logp']:+.4f} ([{st['delta_logp_ci95'][0]:+.4f}, {st['delta_logp_ci95'][1]:+.4f}])")

    print("-" * 90)
    print(f"PAIRWISE TEST (Layer 4 vs. Layer 8):")
    print(f"Contingency: b (L4 wins) = {b}, c (L8 wins) = {c} (Ratio {b}:{c})")
    print(f"Exact McNemar test (one-sided): p = {p_val_one_sided:.6f} ({p_val_one_sided < 0.001})")
    print(f"Exact McNemar test (two-sided): p = {p_val_mcnemar:.6f}")
    print(f"Mean Target Δlogp Difference (L4 - L8): {pairwise_res['mean_dlogp_diff']:+.4f}")
    print(f"Wilcoxon signed-rank test (one-sided): p = {w_pval:.8e}")
    print("=" * 90)

if __name__ == "__main__":
    main()
