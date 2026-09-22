"""
EXP035: Adaptive Gated Latent Deliberation Benchmark (Pythia-160M).

Pre-Registered Confirmatory Benchmark:
Evaluates whether an instance-level Adaptive Stopping Gate (S_margin) based on
decision margin m^(1) = z_(1)^(1) - z_(2)^(1) can resolve the Over-Steering Dilemma
identified in EXP034, halting deliberation upon attractor stabilization to retain
failure rescues (b=5) while eliminating representation corruption (c <= 1).

Evaluated Conditions:
1. Baseline (Unintervened control M_I, 1 pass)
2. G_contrastive (Supervised reference, 1 pass)
3. Fixed_T1 (1-step relational trajectory steering)
4. Fixed_T2 (2-step blind recurrence)
5. Fixed_T3 (3-step blind recurrence)
6. Gated_Margin_0.5 (Halt at T=1 if m^(1) >= 0.5, else advance to T=2)
7. Gated_Margin_1.0 (Halt at T=1 if m^(1) >= 1.0, else advance to T=2)
8. Gated_Margin_1.5 (Halt at T=1 if m^(1) >= 1.5, else advance to T=2)
9. Gated_Margin_2.0 (Halt at T=1 if m^(1) >= 2.0, else advance to T=2)

Guarantees:
- Pre/post parameter SHA-256 hash invariant (Delta theta = 0)
- Zero test-label leakage
- 1,000-resample bootstrap 95% CIs
- Instance-level tracking of rescued (b) and corrupted (c) predictions
- Output saved to experiments/runs/EXP035_adaptive_deliberation/exp035_adaptive_deliberation_results.json
"""

import os
import sys
import time
import json
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import wilcoxon, binomtest
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
    n = b + c
    if n == 0:
        return 1.0
    res = binomtest(b, n, 0.5, alternative='greater')
    return float(res.pvalue)

def extract_contrastive_subspace(h, prem_indices, dist_indices, rank=2):
    h_dist = h[dist_indices, :]
    h_d_cent = h_dist - torch.mean(h_dist, dim=0, keepdim=True)
    _, _, Vh_d = torch.linalg.svd(h_d_cent, full_matrices=False)
    return Vh_d[:rank, :].T

def extract_trajectory_subspace(h_late, h_early, rank=2):
    diff = h_late - h_early
    diff_cent = diff - torch.mean(diff, dim=0, keepdim=True)
    _, _, Vh = torch.linalg.svd(diff_cent, full_matrices=False)
    return Vh[:rank, :].T

def main():
    print("=" * 115)
    print("EXP035: ADAPTIVE GATED LATENT DELIBERATION BENCHMARK")
    print("Evaluating Margin-Based Halting Gates vs. Fixed Recurrence & Supervised Baselines (Pythia-160M)")
    print("=" * 115)

    model_name = "EleutherAI/pythia-160m"
    n_conf = 50
    seed_conf = 84
    target_layer = 8
    target_block = target_layer - 1 # Block 7
    layer_6_block = 5               # Block 5
    alpha = 0.25
    rank = 2

    # 1. Load Dataset
    conf_dataset = generate_bench_002_nl(n_instances=n_conf, seed=seed_conf)
    print(f"[DATASET] Loaded {len(conf_dataset)} confirmatory instances (BENCH-002-NL, Seed {seed_conf}).")

    # 2. Load Model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run Parameter SHA-256: {pre_hash}")

    model_layers = model.gpt_neox.layers

    thresholds = [0.5, 1.0, 1.5, 2.0]
    conditions = [
        "Baseline",
        "G_contrastive",
        "Fixed_T1",
        "Fixed_T2",
        "Fixed_T3"
    ] + [f"Gated_Margin_{t:.1f}" for t in thresholds]

    results = {c: {"correct": [], "delta_logp": []} for c in conditions}
    gated_stats = {f"Gated_Margin_{t:.1f}": {"halted_at_t1": 0, "advanced_to_t2": 0} for t in thresholds}

    print(f"\n>>> Running Evaluation across {len(conditions)} Conditions on {n_conf} Instances...")
    start_time = time.time()

    torch.manual_seed(seed_conf)
    np.random.seed(seed_conf)

    for idx, inst in enumerate(conf_dataset):
        prompt = inst["base"]
        target_token = inst["target"].strip()
        distractor_token = inst["distractor"].strip()

        target_id = tokenizer.encode(" " + target_token)[0] if tokenizer.encode(" " + target_token) else tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(" " + distractor_token)[0] if tokenizer.encode(" " + distractor_token) else tokenizer.encode(distractor_token)[0]

        enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
        input_ids = enc.input_ids
        offsets = enc.offset_mapping[0].tolist()
        T = input_ids.shape[1]

        try:
            p_end = prompt.index(" Distractor:")
            d_end = prompt.index(" Question:")
            prem_indices = [i for i, (s, e) in enumerate(offsets) if e <= p_end and s < e]
            dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
        except ValueError:
            continue

        # ---------------------------------------------------------------------
        # 1. Base Forward Pass (T=0)
        # ---------------------------------------------------------------------
        captured = {}
        def cap_l6_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h_6"] = h.detach().squeeze(0)

        def cap_l8_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h_8"] = h.detach().squeeze(0)

        hndl_6 = model_layers[layer_6_block].register_forward_hook(cap_l6_hook)
        hndl_8 = model_layers[target_block].register_forward_hook(cap_l8_hook)

        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())

        hndl_6.remove()
        hndl_8.remove()

        h_6_init = captured["h_6"]
        h_8_init = captured["h_8"]

        results["Baseline"]["correct"].append(pred_base == target_id)
        results["Baseline"]["delta_logp"].append(0.0)

        # ---------------------------------------------------------------------
        # 2. Supervised Reference (G_contrastive)
        # ---------------------------------------------------------------------
        V_contrastive = extract_contrastive_subspace(h_8_init, prem_indices, dist_indices, rank=rank)
        P_contrastive = (V_contrastive @ V_contrastive.T).to(h_8_init.device)

        def make_linear_hook(P_proj):
            def hook_fn(mod, inp, outp):
                if isinstance(outp, tuple):
                    h = outp[0].clone()
                    h[0] = h[0] - alpha * (h[0] @ P_proj)
                    return (h,) + outp[1:]
                else:
                    h = outp.clone()
                    h[0] = h[0] - alpha * (h[0] @ P_proj)
                    return h
            return hook_fn

        hndl_c = model_layers[target_block].register_forward_hook(make_linear_hook(P_contrastive))
        with torch.no_grad():
            out_c = model(input_ids=input_ids)
            logits_c = out_c.logits[0, -1, :]
            probs_c = F.softmax(logits_c, dim=-1)
            pred_c = torch.argmax(logits_c).item()
            logp_tgt_c = float(torch.log(torch.clamp(probs_c[target_id], min=1e-12)).item())
        hndl_c.remove()

        results["G_contrastive"]["correct"].append(pred_c == target_id)
        results["G_contrastive"]["delta_logp"].append(logp_tgt_c - logp_tgt_base)

        # ---------------------------------------------------------------------
        # 3. Recurrent Step 1 (T=1)
        # ---------------------------------------------------------------------
        V_traj_1 = extract_trajectory_subspace(h_8_init, h_6_init, rank=rank)
        P_traj_1 = (V_traj_1 @ V_traj_1.T).to(h_8_init.device)

        captured_step1 = {}
        def hook_step1(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                captured_step1["h_8"] = h[0].detach()
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                captured_step1["h_8"] = h[0].detach()
                return h

        hndl_t1 = model_layers[target_block].register_forward_hook(hook_step1)
        with torch.no_grad():
            out_t1 = model(input_ids=input_ids)
            logits_t1 = out_t1.logits[0, -1, :]
            probs_t1 = F.softmax(logits_t1, dim=-1)
            pred_t1 = torch.argmax(logits_t1).item()
            logp_tgt_t1 = float(torch.log(torch.clamp(probs_t1[target_id], min=1e-12)).item())
        hndl_t1.remove()

        h_8_step1 = captured_step1["h_8"]

        # Compute Step 1 Decision Margin m^(1) = top1 - runner_up
        top2_vals = torch.topk(logits_t1, 2).values
        margin_t1 = float((top2_vals[0] - top2_vals[1]).item())

        results["Fixed_T1"]["correct"].append(pred_t1 == target_id)
        results["Fixed_T1"]["delta_logp"].append(logp_tgt_t1 - logp_tgt_base)

        # ---------------------------------------------------------------------
        # 4. Recurrent Step 2 (T=2)
        # ---------------------------------------------------------------------
        V_traj_2 = extract_trajectory_subspace(h_8_step1, h_6_init, rank=rank)
        P_traj_2 = (V_traj_2 @ V_traj_2.T).to(h_8_init.device)

        captured_step2 = {}
        def hook_step2(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2)
                captured_step2["h_8"] = h[0].detach()
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2)
                captured_step2["h_8"] = h[0].detach()
                return h

        hndl_t2 = model_layers[target_block].register_forward_hook(hook_step2)
        with torch.no_grad():
            out_t2 = model(input_ids=input_ids)
            logits_t2 = out_t2.logits[0, -1, :]
            probs_t2 = F.softmax(logits_t2, dim=-1)
            pred_t2 = torch.argmax(logits_t2).item()
            logp_tgt_t2 = float(torch.log(torch.clamp(probs_t2[target_id], min=1e-12)).item())
        hndl_t2.remove()

        h_8_step2 = captured_step2["h_8"]

        results["Fixed_T2"]["correct"].append(pred_t2 == target_id)
        results["Fixed_T2"]["delta_logp"].append(logp_tgt_t2 - logp_tgt_base)

        # ---------------------------------------------------------------------
        # 5. Recurrent Step 3 (T=3)
        # ---------------------------------------------------------------------
        V_traj_3 = extract_trajectory_subspace(h_8_step2, h_6_init, rank=rank)
        P_traj_3 = (V_traj_3 @ V_traj_3.T).to(h_8_init.device)

        def hook_step3(mod, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2)
                h[0] = h[0] - alpha * (h[0] @ P_traj_3)
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_traj_1)
                h[0] = h[0] - alpha * (h[0] @ P_traj_2)
                h[0] = h[0] - alpha * (h[0] @ P_traj_3)
                return h

        hndl_t3 = model_layers[target_block].register_forward_hook(hook_step3)
        with torch.no_grad():
            out_t3 = model(input_ids=input_ids)
            logits_t3 = out_t3.logits[0, -1, :]
            probs_t3 = F.softmax(logits_t3, dim=-1)
            pred_t3 = torch.argmax(logits_t3).item()
            logp_tgt_t3 = float(torch.log(torch.clamp(probs_t3[target_id], min=1e-12)).item())
        hndl_t3.remove()

        results["Fixed_T3"]["correct"].append(pred_t3 == target_id)
        results["Fixed_T3"]["delta_logp"].append(logp_tgt_t3 - logp_tgt_base)

        # ---------------------------------------------------------------------
        # 6. Adaptive Gated Conditions (Decision Margin S_margin)
        # ---------------------------------------------------------------------
        for tau in thresholds:
            cond_key = f"Gated_Margin_{tau:.1f}"
            if margin_t1 >= tau:
                # Halt at Step 1
                gated_pred = pred_t1
                gated_logp = logp_tgt_t1
                gated_stats[cond_key]["halted_at_t1"] += 1
            else:
                # Advance to Step 2
                gated_pred = pred_t2
                gated_logp = logp_tgt_t2
                gated_stats[cond_key]["advanced_to_t2"] += 1

            results[cond_key]["correct"].append(gated_pred == target_id)
            results[cond_key]["delta_logp"].append(gated_logp - logp_tgt_base)

        if (idx + 1) % 10 == 0 or idx == n_conf - 1:
            print(f"  Processed {idx+1}/{n_conf} instances... [Base: {sum(results['Baseline']['correct'])}/{idx+1}, T1: {sum(results['Fixed_T1']['correct'])}/{idx+1}, T2: {sum(results['Fixed_T2']['correct'])}/{idx+1}]")

    elapsed = time.time() - start_time
    print(f"[COMPUTE] Benchmark completed in {elapsed:.1f}s.")

    # Verify Parameter Invariance
    post_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Post-run Parameter SHA-256: {post_hash}")
    assert pre_hash == post_hash, "CRITICAL ERROR: Parameters mutated during inference!"
    print("[REPRODUCIBILITY] Frozen Backbone Verified: Parameter hashes match identically (Delta theta = 0).")

    # -------------------------------------------------------------------------
    # Statistical Scorecard
    # -------------------------------------------------------------------------
    base_correct = results["Baseline"]["correct"]
    base_acc = float(np.mean(base_correct))

    print("\n" + "=" * 115)
    print(f"EMPIRICAL RESULTS: Base Unintervened Accuracy M_I = {base_acc:.4f} ({sum(base_correct)}/{n_conf})")
    print("=" * 115)
    print(f"{'Condition':<22} | {'Acc':<7} | {'Delta M':<9} | {'95% CI':<16} | {'Delta log p':<12} | {'McNemar (vs Base)':<20} | {'b (Rescued)':<11} | {'c (Corrupted)':<13}")
    print("-" * 115)

    summary = {
        "metadata": {
            "experiment_id": "EXP035",
            "date": "2026-09-12",
            "model": model_name,
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_invariant": (pre_hash == post_hash),
            "target_layer": target_layer,
            "alpha": alpha,
            "rank": rank,
            "n_conf": n_conf,
            "base_acc": base_acc,
            "elapsed_sec": elapsed
        },
        "conditions": {},
        "gated_stats": gated_stats
    }

    for c_name in conditions:
        corr = results[c_name]["correct"]
        d_logp = results[c_name]["delta_logp"]

        acc = float(np.mean(corr))
        delta_m = acc - base_acc
        delta_arr = [float(c) - float(b) for c, b in zip(corr, base_correct)]
        ci = compute_bootstrap_ci(delta_arr, n_boot=1000)
        mean_d_logp = float(np.mean(d_logp))

        b = sum(1 for c, b_val in zip(corr, base_correct) if c and not b_val)
        c = sum(1 for c, b_val in zip(corr, base_correct) if not c and b_val)
        p_mcnemar_base = exact_mcnemar(b, c)

        summary["conditions"][c_name] = {
            "accuracy": acc,
            "delta_m": delta_m,
            "ci_95": ci,
            "mean_delta_logp": mean_d_logp,
            "rescued_b": b,
            "corrupted_c": c,
            "mcnemar_vs_base": {"b": b, "c": c, "p_value": p_mcnemar_base}
        }

        print(f"{c_name:<22} | {acc:.4f}  | {delta_m*100:+5.1f} pp | [{ci[0]*100:+5.1f}, {ci[1]*100:+5.1f}] pp | {mean_d_logp:+10.4f}   | b={b}, c={c}, p={p_mcnemar_base:.4f}     | {b:<11} | {c:<13}")

    print("-" * 115)
    print("\n[GATED HALTING STATS]")
    for k, v in gated_stats.items():
        print(f"  {k}: Halted at T=1: {v['halted_at_t1']}/{n_conf} ({v['halted_at_t1']/n_conf*100:.1f}%), Advanced to T=2: {v['advanced_to_t2']}/{n_conf} ({v['advanced_to_t2']/n_conf*100:.1f}%)")

    # Save to json
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP035_adaptive_deliberation"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "exp035_adaptive_deliberation_results.json")
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n[OUTPUT] Saved complete benchmark results to: {out_file}")

if __name__ == "__main__":
    main()
