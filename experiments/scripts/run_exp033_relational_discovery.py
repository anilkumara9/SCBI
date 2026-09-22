"""
EXP033: Autonomous Relational Basis Discovery Benchmark (Pythia-160M).

Pre-Registered Confirmatory Benchmark:
Evaluates whether internal relational geometry (attention divergence, competing hypotheses,
contextual perturbation, and inter-layer trajectory) can discover task-relevant intervention
directions without human semantic token tags.

Generators Evaluated at Layer 8 (C0 Ungated Linear, alpha=0.25, rank=2):
1. G_contrastive: Supervised token-contrast reference (EXP026/027/030/031/032 reference)
2. G_attention_relational: Relational difference between high-attention and low-attention token representations
3. G_hypothesis_contrast: Relational conflict between top-2 competing unembedding hypotheses (W_U[y1] - W_U[y2])
4. G_latent_counterfactual: Relational divergence under contextual prompt perturbation (h_orig - h_perturbed)
5. G_trajectory_difference: Inter-layer computation trajectory acceleration (h_8 - h_6)
6. G_random: Uniformly sampled orthonormal Grassmannian subspace (Null control)

Guarantees:
- Pre/post parameter SHA-256 hash invariant (Delta theta = 0)
- Zero test-label leakage during calibration/basis generation
- 1,000-resample bootstrap 95% CIs
- Output saved to experiments/runs/EXP033_relational/exp033_relational_results.json
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

def main():
    print("=" * 110)
    print("EXP033: AUTONOMOUS RELATIONAL BASIS DISCOVERY BENCHMARK")
    print("Evaluating Relational Generators vs. Contrastive Supervision (Pythia-160M, Layer 8, alpha=0.25, rank=2)")
    print("=" * 110)

    model_name = "EleutherAI/pythia-160m"
    n_conf = 50
    seed_conf = 84
    target_layer = 8
    target_block = target_layer - 1 # Block 7 is Layer 8 (0-indexed)
    layer_6_block = 5               # Block 5 is Layer 6 (0-indexed)
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
    embed_out_w = model.embed_out.weight.detach() # [V, d]

    generators = [
        "G_contrastive",
        "G_attention_relational",
        "G_hypothesis_contrast",
        "G_latent_counterfactual",
        "G_trajectory_difference",
        "G_random"
    ]

    results = {g: {"correct": [], "delta_logp": []} for g in generators}
    base_correct_list = []
    base_logp_list = []

    print(f"\n>>> Evaluating {len(generators)} Candidate Generators on {n_conf} Confirmatory Instances...")
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
        # Step 1: Base Forward Pass (Capturing L6, L8, Attention, and Logits)
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
            out_base = model(input_ids=input_ids, output_attentions=True)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())
            attentions_all = out_base.attentions

        hndl_6.remove()
        hndl_8.remove()

        base_is_corr = (pred_base == target_id)
        base_correct_list.append(base_is_corr)
        base_logp_list.append(logp_tgt_base)

        h_8 = captured["h_8"] # [T, d]
        h_6 = captured["h_6"] # [T, d]
        d_dim = h_8.shape[-1]

        # ---------------------------------------------------------------------
        # Step 2: Construct Candidate Subspaces for each Relational Generator
        # ---------------------------------------------------------------------
        gen_subspaces = {}

        # 1. G_contrastive (Supervised Ground Truth Reference)
        V_contrastive = extract_contrastive_subspace(h_8, prem_indices, dist_indices, rank=rank)
        gen_subspaces["G_contrastive"] = V_contrastive

        # 2. G_attention_relational (Attention-Weighted High- vs Low-Attention Difference)
        # Use attention at block 6 (Layer 7), from last token to previous tokens across heads
        attn_layer7 = attentions_all[layer_6_block + 1][0] # [num_heads, T, T]
        last_tok_attn = attn_layer7[:, -1, :T-1].mean(dim=0) # [T-1]
        k_attn = max(2, int(0.20 * (T - 1)))
        top_attn_idx = torch.topk(last_tok_attn, k_attn).indices
        bot_attn_idx = torch.topk(last_tok_attn, k_attn, largest=False).indices

        h_high = h_8[top_attn_idx] # [k, d]
        h_low = h_8[bot_attn_idx]   # [k, d]
        diff_attn_mean = torch.mean(h_high, dim=0) - torch.mean(h_low, dim=0)
        u1_attn = diff_attn_mean / (torch.norm(diff_attn_mean) + 1e-12)

        # Compute second orthogonal principal component from high-attention token spread
        h_high_proj = h_high - torch.mean(h_high, dim=0, keepdim=True)
        _, _, Vh_high = torch.linalg.svd(h_high_proj, full_matrices=False)
        u2_cand = Vh_high[0, :]
        u2_attn = u2_cand - torch.dot(u2_cand, u1_attn) * u1_attn
        u2_attn = u2_attn / (torch.norm(u2_attn) + 1e-12)
        gen_subspaces["G_attention_relational"] = torch.stack([u1_attn, u2_attn], dim=1)

        # 3. G_hypothesis_contrast (Top-2 Competing Unembedding Conflict)
        # Identify top-2 predictions under base forward pass
        top_preds = torch.topk(logits_base, 3).indices
        y_1 = top_preds[0].item()
        y_2 = top_preds[1].item()
        y_3 = top_preds[2].item()

        w_1 = embed_out_w[y_1] # [d]
        w_2 = embed_out_w[y_2] # [d]
        w_3 = embed_out_w[y_3] # [d]

        diff_w12 = w_1 - w_2
        u1_hyp = diff_w12 / (torch.norm(diff_w12) + 1e-12)

        diff_w13 = w_1 - w_3
        u2_cand = diff_w13 - torch.dot(diff_w13, u1_hyp) * u1_hyp
        u2_hyp = u2_cand / (torch.norm(u2_cand) + 1e-12)
        gen_subspaces["G_hypothesis_contrast"] = torch.stack([u1_hyp, u2_hyp], dim=1)

        # 4. G_latent_counterfactual (Contextual Prompt Perturbation Difference)
        # Create perturbed input: mask 20% of context tokens with eos_token_id
        pert_ids = input_ids.clone()
        rng_pert = np.random.RandomState(seed_conf + idx * 7)
        mask_candidates = [t for t in range(1, T - 1)] # avoid first token and last token
        n_mask = max(1, int(0.20 * len(mask_candidates)))
        mask_idx = rng_pert.choice(mask_candidates, size=n_mask, replace=False)
        for m_pos in mask_idx:
            pert_ids[0, m_pos] = tokenizer.eos_token_id

        captured_pert = {}
        def cap_pert_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured_pert["h_pert"] = h.detach().squeeze(0)

        hndl_pert = model_layers[target_block].register_forward_hook(cap_pert_hook)
        with torch.no_grad():
            model(input_ids=pert_ids)
        hndl_pert.remove()

        h_pert = captured_pert["h_pert"] # [T, d]
        diff_pert = h_8 - h_pert        # [T, d]
        diff_pert_cent = diff_pert - torch.mean(diff_pert, dim=0, keepdim=True)
        _, _, Vh_pert = torch.linalg.svd(diff_pert_cent, full_matrices=False)
        gen_subspaces["G_latent_counterfactual"] = Vh_pert[:rank, :].T

        # 5. G_trajectory_difference (Inter-Layer Acceleration h_8 - h_6)
        diff_traj = h_8 - h_6 # [T, d]
        diff_traj_cent = diff_traj - torch.mean(diff_traj, dim=0, keepdim=True)
        _, _, Vh_traj = torch.linalg.svd(diff_traj_cent, full_matrices=False)
        gen_subspaces["G_trajectory_difference"] = Vh_traj[:rank, :].T

        # 6. G_random (Grassmannian Uniform Null Baseline)
        rng_rand = np.random.RandomState(seed_conf + idx * 100)
        rand_mat = rng_rand.randn(d_dim, rank)
        Q, _ = np.linalg.qr(rand_mat)
        gen_subspaces["G_random"] = torch.tensor(Q, dtype=torch.float32)

        # ---------------------------------------------------------------------
        # Step 3: Evaluate Each Generator at Layer 8 (alpha=0.25)
        # ---------------------------------------------------------------------
        for g_name in generators:
            V = gen_subspaces[g_name].to(h_8.device)
            P_mat = V @ V.T

            def make_hook(P_proj):
                def hook_fn(module, inp, outp):
                    if isinstance(outp, tuple):
                        h = outp[0].clone()
                        delta = alpha * (h[0] @ P_proj)
                        h[0] = h[0] - delta
                        return (h,) + outp[1:]
                    else:
                        h = outp.clone()
                        delta = alpha * (h[0] @ P_proj)
                        h[0] = h[0] - delta
                        return h
                return hook_fn

            hook = model_layers[target_block].register_forward_hook(make_hook(P_mat))
            with torch.no_grad():
                out_g = model(input_ids=input_ids)
                logits_g = out_g.logits[0, -1, :]
                probs_g = F.softmax(logits_g, dim=-1)
                pred_g = torch.argmax(logits_g).item()
                logp_tgt_g = float(torch.log(torch.clamp(probs_g[target_id], min=1e-12)).item())
            hook.remove()

            results[g_name]["correct"].append(pred_g == target_id)
            results[g_name]["delta_logp"].append(logp_tgt_g - logp_tgt_base)

        if (idx + 1) % 10 == 0 or idx == n_conf - 1:
            print(f"  Processed {idx+1}/{n_conf} instances... [Base Accuracy: {sum(base_correct_list)}/{idx+1}]")

    elapsed = time.time() - start_time
    print(f"[COMPUTE] Evaluation completed in {elapsed:.1f}s.")

    # -------------------------------------------------------------------------
    # Step 4: Verify Post-Run Parameter Hash
    # -------------------------------------------------------------------------
    post_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Post-run Parameter SHA-256: {post_hash}")
    assert pre_hash == post_hash, "CRITICAL ERROR: Model parameters mutated during inference!"
    print("[REPRODUCIBILITY] Frozen Backbone Verified: Parameter hashes match identically (Delta theta = 0).")

    # -------------------------------------------------------------------------
    # Step 5: Compute Statistical Metrics
    # -------------------------------------------------------------------------
    base_acc = float(np.mean(base_correct_list))
    print("\n" + "=" * 110)
    print(f"EMPIRICAL RESULTS: Base Unintervened Accuracy M_I = {base_acc:.4f} ({sum(base_correct_list)}/{n_conf})")
    print("=" * 110)
    print(f"{'Generator':<26} | {'Acc':<7} | {'Delta M':<9} | {'95% CI':<16} | {'Delta log p':<12} | {'McNemar (vs Base)':<20} | {'McNemar (vs Rand)':<20}")
    print("-" * 110)

    summary = {
        "metadata": {
            "experiment_id": "EXP033",
            "date": "2026-09-11",
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
        "generators": {}
    }

    rand_correct = results["G_random"]["correct"]

    for g_name in generators:
        corr = results[g_name]["correct"]
        d_logp = results[g_name]["delta_logp"]

        acc = float(np.mean(corr))
        delta_m = acc - base_acc
        delta_arr = [float(c) - float(b) for c, b in zip(corr, base_correct_list)]
        ci = compute_bootstrap_ci(delta_arr, n_boot=1000)
        mean_d_logp = float(np.mean(d_logp))

        # McNemar vs Base
        b = sum(1 for c, b_val in zip(corr, base_correct_list) if c and not b_val)
        c = sum(1 for c, b_val in zip(corr, base_correct_list) if not c and b_val)
        p_mcnemar_base = exact_mcnemar(b, c)

        # McNemar vs Random
        b_r = sum(1 for c, r_val in zip(corr, rand_correct) if c and not r_val)
        c_r = sum(1 for c, r_val in zip(corr, rand_correct) if not c and r_val)
        p_mcnemar_rand = exact_mcnemar(b_r, c_r)

        # Wilcoxon on delta_logp vs 0
        try:
            w_stat, w_pval = wilcoxon(d_logp, alternative='greater')
            w_pval = float(w_pval)
        except Exception:
            w_pval = 1.0

        summary["generators"][g_name] = {
            "accuracy": acc,
            "delta_m": delta_m,
            "ci_95": ci,
            "mean_delta_logp": mean_d_logp,
            "wilcoxon_logp_pval": w_pval,
            "mcnemar_vs_base": {"b": b, "c": c, "p_value": p_mcnemar_base},
            "mcnemar_vs_random": {"b": b_r, "c": c_r, "p_value": p_mcnemar_rand}
        }

        print(f"{g_name:<26} | {acc:.4f}  | {delta_m*100:+5.1f} pp | [{ci[0]*100:+5.1f}, {ci[1]*100:+5.1f}] pp | {mean_d_logp:+10.4f}   | b={b}, c={c}, p={p_mcnemar_base:.4f}     | b={b_r}, c={c_r}, p={p_mcnemar_rand:.4f}")

    print("-" * 110)

    # Save to json
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP033_relational"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "exp033_relational_results.json")
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n[OUTPUT] Saved complete benchmark results to: {out_file}")

if __name__ == "__main__":
    main()
