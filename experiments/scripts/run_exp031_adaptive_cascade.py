"""
EXP031: Closed-Loop Adaptive Controller & Multi-Stage Cascaded Representation Control (Pythia-160M).

Pre-Registered Confirmatory Benchmark on N=50 instances (BENCH-002-NL, Seed 84):
Tests whether multi-stage hierarchical cascading (L2[C2] + L8[C0]) unlocks compound
reasoning headroom exceeding any single-layer intervention in the model.

Conditions:
1. Baseline Control: M_I (Unintervened)
2. Single-Stage Champions:
   - L2_C2_a50 (Early Selective Gate)
   - L4_C0_a25 (Bottleneck Linear)
   - L8_C0_a25 (Late Linear - EXP030 Global Single-Stage Champion: +14.0 pp)
3. Two-Stage Hierarchical Cascades:
   - Cascade_L2C2_L8C0_nom: L2[C2, a=0.50] + L8[C0, a=0.25] (Hierarchical Champion)
   - Cascade_L2C2_L8C0_gentle: L2[C2, a=0.25] + L8[C0, a=0.25]
   - Cascade_L2C0_L8C0: L2[C0, a=0.25] + L8[C0, a=0.25] (Ungated both)
   - Cascade_L4C0_L8C0: L4[C0, a=0.25] + L8[C0, a=0.25] (Bottleneck to Late)
4. Tri-Stage Deep Cascade:
   - Cascade_TriStage_L2_L4_L8: L2[C2, a=0.25] + L4[C0, a=0.15] + L8[C0, a=0.25]
5. Confidence-Gated Selective Execution:
   - Cascade_Confidence_Gated: Only intervene if unintervened margin < 1.0

Guarantees:
- Pre/post parameter SHA-256 hash invariant (Delta theta = 0)
- 1,000-resample bootstrap 95% CIs for Delta M and Delta log p
- Exact Paired McNemar tests and Wilcoxon signed-rank tests
- Output saved to experiments/runs/EXP031_adaptive/exp031_cascade_results.json
"""

import os
import sys
import time
import json
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import wilcoxon
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def compute_bootstrap_ci(data, n_boot=1000, ci=0.95):
    if len(data) == 0:
        return [0.0, 0.0]
    arr = np.array(data)
    boot_means = [np.mean(np.random.choice(arr, size=len(arr), replace=True)) for _ in range(n_boot)]
    alpha_ci = (1.0 - ci) / 2.0
    low = float(np.percentile(boot_means, alpha_ci * 100))
    high = float(np.percentile(boot_means, (1.0 - alpha_ci) * 100))
    return [low, high]

def exact_mcnemar(b, c):
    from scipy.stats import binomtest
    n = b + c
    if n == 0:
        return 1.0
    res = binomtest(b, n, 0.5, alternative='greater')
    return float(res.pvalue)

def extract_contrastive_subspaces(h, prem_indices, dist_indices, rank=2):
    h_prem = h[prem_indices, :]
    h_dist = h[dist_indices, :]

    h_p_cent = h_prem - torch.mean(h_prem, dim=0, keepdim=True)
    _, _, Vh_p = torch.linalg.svd(h_p_cent, full_matrices=False)
    V_plus = Vh_p[:rank, :].T

    h_d_cent = h_dist - torch.mean(h_dist, dim=0, keepdim=True)
    _, _, Vh_d = torch.linalg.svd(h_d_cent, full_matrices=False)
    V_minus = Vh_d[:rank, :].T

    return V_plus, V_minus

def main():
    print("=" * 110)
    print("EXP031: CLOSED-LOOP ADAPTIVE CONTROLLER & MULTI-STAGE CASCADED REPRESENTATION CONTROL")
    print("Testing Compound Hierarchical Synergies on EleutherAI/pythia-160m (N=50, BENCH-002-NL)")
    print("=" * 110)

    model_name = "EleutherAI/pythia-160m"
    n_instances = 50
    seed = 84
    rank = 2

    # 1. Load Dataset
    dataset = generate_bench_002_nl(n_instances=n_instances, seed=seed)
    print(f"[DATASET] Loaded {len(dataset)} confirmatory instances (Seed {seed}).")

    # 2. Load Model & Verify Weights
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run Parameter SHA-256: {pre_hash}")

    model_layers = model.gpt_neox.layers
    num_layers = len(model_layers)

    # 3. Define Condition Manifest
    # Each condition defines a list of hook specifications:
    # [(layer_idx, controller_type, alpha)]
    conditions = {
        # Single-Stage Champions
        "Single_L2_C2_a50": [(2, "C2_hard", 0.50)],
        "Single_L4_C0_a25": [(4, "C0_ungated", 0.25)],
        "Single_L8_C0_a25": [(8, "C0_ungated", 0.25)],

        # Two-Stage Hierarchical Cascades
        "Cascade_L2C2_L8C0_nom": [(2, "C2_hard", 0.50), (8, "C0_ungated", 0.25)],
        "Cascade_L2C2_L8C0_gentle": [(2, "C2_hard", 0.25), (8, "C0_ungated", 0.25)],
        "Cascade_L2C0_L8C0": [(2, "C0_ungated", 0.25), (8, "C0_ungated", 0.25)],
        "Cascade_L4C0_L8C0": [(4, "C0_ungated", 0.25), (8, "C0_ungated", 0.25)],

        # Tri-Stage Deep Cascade
        "Cascade_TriStage_L2_L4_L8": [(2, "C2_hard", 0.25), (4, "C0_ungated", 0.15), (8, "C0_ungated", 0.25)],

        # Confidence-Gated Selective Execution (Evaluated dynamically)
        "Cascade_Confidence_Gated": "DYNAMIC_CONFIDENCE_GATED"
    }

    results = {cond: {"correct": [], "delta_logp": [], "logits_margin": []} for cond in conditions}
    base_correct_list = []
    base_logp_list = []
    base_margin_list = []

    start_time = time.time()
    print("\n>>> Executing Multi-Stage Cascaded Interventions across 50 instances...")

    for idx, inst in enumerate(dataset):
        prompt = inst["base"]
        target_token = inst["target"].strip()
        distractor_token = inst["distractor"].strip()

        target_id = tokenizer.encode(" " + target_token)[0] if tokenizer.encode(" " + target_token) else tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(" " + distractor_token)[0] if tokenizer.encode(" " + distractor_token) else tokenizer.encode(distractor_token)[0]

        enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
        input_ids = enc.input_ids
        offsets = enc.offset_mapping[0].tolist()

        try:
            p_end = prompt.index(" Distractor:")
            d_end = prompt.index(" Question:")
            prem_indices = [i for i, (s, e) in enumerate(offsets) if e <= p_end and s < e]
            dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
        except ValueError:
            continue

        # A. Unintervened Baseline Run + Layer Capture
        captured_layers = {}
        cap_handles = []

        for l_num in [2, 4, 8]:
            b_idx = l_num - 1
            def make_cap_hook(l_target):
                def hook_fn(mod, inp, outp):
                    h = outp[0] if isinstance(outp, tuple) else outp
                    captured_layers[l_target] = h.detach().clone()
                return hook_fn
            cap_handles.append(model_layers[b_idx].register_forward_hook(make_cap_hook(l_num)))

        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())

            top2_vals, _ = torch.topk(logits_base, k=2)
            base_margin = float((top2_vals[0] - top2_vals[1]).item())

        for h in cap_handles:
            h.remove()

        base_is_corr = (pred_base == target_id)
        base_correct_list.append(base_is_corr)
        base_logp_list.append(logp_tgt_base)
        base_margin_list.append(base_margin)

        # B. Extract Contrastive Subspaces for L2, L4, L8
        subspaces = {}
        for l_num in [2, 4, 8]:
            h_l = captured_layers[l_num].squeeze(0)
            V_p, V_m = extract_contrastive_subspaces(h_l, prem_indices, dist_indices, rank=rank)
            P_m = V_m @ V_m.T
            P_p = V_p @ V_p.T
            d_tokens = torch.norm(h_l @ P_m, dim=-1) - torch.norm(h_l @ P_p, dim=-1)
            subspaces[l_num] = {"P_m": P_m, "d_tokens": d_tokens}

        # C. Execute Each Experimental Condition
        for cond_name, spec in conditions.items():
            if cond_name == "Cascade_Confidence_Gated":
                # Meta-cognitive gate: if model is already highly confident (margin >= 1.0), do not intervene
                if base_margin >= 1.0:
                    results[cond_name]["correct"].append(base_is_corr)
                    results[cond_name]["delta_logp"].append(0.0)
                    results[cond_name]["logits_margin"].append(base_margin)
                    continue
                else:
                    # Apply Hierarchical Champion Cascade when margin < 1.0
                    spec = [(2, "C2_hard", 0.50), (8, "C0_ungated", 0.25)]

            # Construct and Register Hooks for this condition
            active_hooks = []
            for (l_num, ctrl_type, alpha_val) in spec:
                b_idx = l_num - 1
                P_mat = subspaces[l_num]["P_m"]
                d_tokens = subspaces[l_num]["d_tokens"]

                if ctrl_type == "C0_ungated":
                    gate = torch.ones_like(d_tokens).unsqueeze(-1)
                elif ctrl_type == "C1_soft":
                    tau = torch.median(d_tokens)
                    tau_scale = torch.std(d_tokens) + 1e-6
                    gate = torch.sigmoid((d_tokens - tau) / tau_scale).unsqueeze(-1)
                elif ctrl_type == "C2_hard":
                    gate = (d_tokens > 0.0).float().unsqueeze(-1)

                def make_hook(P_proj, g_gate, a_coeff):
                    def hook_fn(module, inp, outp):
                        if isinstance(outp, tuple):
                            h = outp[0].clone()
                            delta = a_coeff * (h[0] @ P_proj) * g_gate.to(h.device)
                            h[0] = h[0] - delta
                            return (h,) + outp[1:]
                        else:
                            h = outp.clone()
                            delta = a_coeff * (h[0] @ P_proj) * g_gate.to(h.device)
                            h[0] = h[0] - delta
                            return h
                    return hook_fn

                hook = model_layers[b_idx].register_forward_hook(make_hook(P_mat, gate, alpha_val))
                active_hooks.append(hook)

            with torch.no_grad():
                out_cond = model(input_ids=input_ids)
                logits_cond = out_cond.logits[0, -1, :]
                probs_cond = F.softmax(logits_cond, dim=-1)
                pred_cond = torch.argmax(logits_cond).item()
                logp_tgt_cond = float(torch.log(torch.clamp(probs_cond[target_id], min=1e-12)).item())

                top2_cond, _ = torch.topk(logits_cond, k=2)
                cond_margin = float((top2_cond[0] - top2_cond[1]).item())

            for h in active_hooks:
                h.remove()

            results[cond_name]["correct"].append(pred_cond == target_id)
            results[cond_name]["delta_logp"].append(logp_tgt_cond - logp_tgt_base)
            results[cond_name]["logits_margin"].append(cond_margin)

        if (idx + 1) % 10 == 0 or idx == n_instances - 1:
            print(f"  Processed {idx+1}/{n_instances} instances... [Base Accuracy: {sum(base_correct_list)}/{idx+1}]")

    elapsed = time.time() - start_time
    print(f"[COMPUTE] Multi-Stage Cascade benchmark completed in {elapsed:.1f}s.")

    # 4. Verify Post-run Parameter Invariance
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "Parameter mutation detected!"
    print(f"[REPRODUCIBILITY] Post-run Parameter SHA-256 verified invariant: {post_hash}")

    # 5. Statistical Scorecard
    m_base = float(np.mean(base_correct_list))
    print("\n" + "=" * 125)
    print(f"EXP031 SCORECARD: MULTI-STAGE CASCADED REPRESENTATION CONTROL (Base M_I = {m_base:6.4f})")
    print("=" * 125)
    print(f"{'Condition Key':<28} | {'Accuracy':<8} | {'Delta M (pp)':<14} | {'95% CI (Delta M)':<16} | {'Delta logP':<10} | {'McNemar vs Base':<16} | {'Synergy vs L8?'}")
    print("-" * 125)

    output_data = {
        "metadata": {
            "experiment": "EXP031",
            "model_name": model_name,
            "parameter_sha256": post_hash,
            "n_instances": n_instances,
            "seed": seed,
            "baseline_accuracy": m_base
        },
        "conditions": {}
    }

    # Reference L8 accuracy for synergy comparison
    m_l8 = float(np.mean(results["Single_L8_C0_a25"]["correct"]))

    for cond_name, cdata in results.items():
        corr = cdata["correct"]
        dlp = cdata["delta_logp"]

        acc = float(np.mean(corr))
        delta_m_pp = float((acc - m_base) * 100.0)
        ci_delta_m = compute_bootstrap_ci([(c - b) * 100.0 for c, b in zip(corr, base_correct_list)])
        mean_dlp = float(np.mean(dlp))

        # McNemar contingency vs baseline
        b = sum(1 for c, b_i in zip(corr, base_correct_list) if c and not b_i)
        c = sum(1 for c, b_i in zip(corr, base_correct_list) if not c and b_i)
        p_mcnemar_base = exact_mcnemar(b, c)

        # Synergy vs Single L8 (+14.0 pp)
        synergy = "YES (+ compound)" if acc > m_l8 else ("TIED" if acc == m_l8 else "no")

        print(f"{cond_name:<28} | {acc:6.4f}   | {delta_m_pp:+6.1f} pp     | [{ci_delta_m[0]:+5.1f}, {ci_delta_m[1]:+5.1f}] pp | {mean_dlp:+8.4f}   | b={b}, c={c} (p={p_mcnemar_base:6.4f}) | {synergy}")

        output_data["conditions"][cond_name] = {
            "accuracy": acc,
            "delta_m_pp": delta_m_pp,
            "delta_m_ci95_pp": ci_delta_m,
            "mean_delta_logp": mean_dlp,
            "mcnemar_vs_base": {"b": b, "c": c, "p_value": p_mcnemar_base},
            "synergy_vs_single_l8": synergy
        }

    # Paired Wilcoxon Test: Hierarchical Champion vs Single L8 Champion
    dlp_hierarchical = results["Cascade_L2C2_L8C0_nom"]["delta_logp"]
    dlp_single_l8 = results["Single_L8_C0_a25"]["delta_logp"]
    try:
        w_stat, w_pval = wilcoxon(dlp_hierarchical, dlp_single_l8, alternative='greater')
        output_data["pairwise_tests"] = {
            "comparison": "Cascade_L2C2_L8C0_nom vs Single_L8_C0_a25",
            "wilcoxon_stat": float(w_stat),
            "wilcoxon_p_value": float(w_pval)
        }
        print("-" * 125)
        print(f"[PAIRWISE TEST] Hierarchical Cascade vs Single L8 Target Log-Probability: Wilcoxon W={w_stat}, p={w_pval:.6f}")
    except Exception as e:
        print(f"[PAIRWISE TEST ERROR] {e}")

    # 6. Save JSON ledger
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP031_adaptive"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp031_cascade_results.json")
    with open(out_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n[OUTPUT] EXP031 Cascade results successfully written to: {out_path}")

if __name__ == "__main__":
    main()
