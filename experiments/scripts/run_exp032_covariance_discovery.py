"""
EXP032: Autonomous Internal Basis Discovery from Activation Geometry (Pythia-160M).

Pre-Registered Confirmatory Benchmark:
Evaluates whether unlabeled internal activation geometry can discover useful SCBI
intervention directions without explicit premise/distractor token supervision.

Generators Evaluated at Layer 8 (C0 Ungated Linear, alpha=0.25):
1. G_contrastive: Supervised token-contrast baseline (EXP026/027 reference)
2. G_cov_token_top: Principal eigenvectors [u1, u2] of prompt token covariance Sigma_token
3. G_cov_token_mid: Sub-dominant eigenvectors [u3, u4] of Sigma_token
4. G_cov_token_tail: Tail eigenvectors [u5, u6] of Sigma_token
5. G_cov_prompt: Top eigenvectors of inter-prompt population covariance Sigma_prompt
6. G_cov_residual: Top eigenvectors of position-residualized covariance Sigma_residual
7. G_random: Random orthonormal Grassmannian subspace (Null control)

Guarantees:
- Pre/post parameter SHA-256 hash invariant (Delta theta = 0)
- Zero test-label leakage during calibration
- 1,000-resample bootstrap 95% CIs
- Output saved to experiments/runs/EXP032_covariance/exp032_covariance_results.json
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
    print("EXP032: AUTONOMOUS INTERNAL BASIS DISCOVERY FROM UNLABELED ACTIVATION GEOMETRY")
    print("Evaluating Covariance Generators vs. Contrastive Supervision (Pythia-160M, Layer 8, alpha=0.25)")
    print("=" * 110)

    model_name = "EleutherAI/pythia-160m"
    n_calib = 20
    n_conf = 50
    seed_calib = 123
    seed_conf = 84
    target_layer = 8
    target_block = target_layer - 1
    alpha = 0.25
    rank = 2

    # 1. Load Datasets
    calib_dataset = generate_bench_002_nl(n_instances=n_calib, seed=seed_calib)
    conf_dataset = generate_bench_002_nl(n_instances=n_conf, seed=seed_conf)
    print(f"[DATASET] Loaded {len(calib_dataset)} calibration prompts (Seed {seed_calib}) and {len(conf_dataset)} confirmatory instances (Seed {seed_conf}).")

    # 2. Load Model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run Parameter SHA-256: {pre_hash}")

    model_layers = model.gpt_neox.layers

    # -------------------------------------------------------------------------
    # PHASE A: Compute Calibration Statistics (Zero Labels Exposed)
    # -------------------------------------------------------------------------
    print("\n>>> Phase A: Computing Population and Positional Calibration Statistics...")
    calib_prompt_means = []
    calib_pos_tensors = {} # pos -> list of vectors

    for inst in calib_dataset:
        prompt = inst["base"]
        enc = tokenizer(prompt, return_tensors="pt")
        input_ids = enc.input_ids
        T = input_ids.shape[1]

        captured = {}
        def cap_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h"] = h.detach().squeeze(0) # [T, d]

        hndl = model_layers[target_block].register_forward_hook(cap_hook)
        with torch.no_grad():
            model(input_ids=input_ids)
        hndl.remove()

        h_calib = captured["h"]
        mean_p = torch.mean(h_calib, dim=0)
        calib_prompt_means.append(mean_p)

        for t in range(T):
            if t not in calib_pos_tensors:
                calib_pos_tensors[t] = []
            calib_pos_tensors[t].append(h_calib[t])

    # Compute Sigma_prompt
    all_means = torch.stack(calib_prompt_means, dim=0) # [P, d]
    all_means_cent = all_means - torch.mean(all_means, dim=0, keepdim=True)
    _, _, Vh_prompt = torch.linalg.svd(all_means_cent, full_matrices=False)
    V_cov_prompt = Vh_prompt[:rank, :].T # [d, r]

    # Compute mean representation per token position
    calib_pos_mean = {t: torch.mean(torch.stack(vecs, dim=0), dim=0) for t, vecs in calib_pos_tensors.items()}
    print(f"[PHASE A] Population Covariance computed across {n_calib} prompts. Sigma_prompt rank: {V_cov_prompt.shape}")

    # -------------------------------------------------------------------------
    # PHASE B: Confirmatory Evaluation Across 7 Candidate Generators
    # -------------------------------------------------------------------------
    generators = [
        "G_contrastive",
        "G_cov_token_top",
        "G_cov_token_mid",
        "G_cov_token_tail",
        "G_cov_prompt",
        "G_cov_residual",
        "G_random"
    ]

    results = {g: {"correct": [], "delta_logp": []} for g in generators}
    base_correct_list = []
    base_logp_list = []

    print(f"\n>>> Phase B: Evaluating {len(generators)} Generators on {n_conf} Confirmatory Instances...")
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

        # 1. Base Forward Pass
        captured = {}
        def cap_hook(mod, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured["h"] = h.detach().squeeze(0)

        hndl = model_layers[target_block].register_forward_hook(cap_hook)
        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())
        hndl.remove()

        base_is_corr = (pred_base == target_id)
        base_correct_list.append(base_is_corr)
        base_logp_list.append(logp_tgt_base)

        h_8 = captured["h"] # [T, d]
        d_dim = h_8.shape[-1]

        # 2. Construct Candidate Subspaces for each Generator
        gen_subspaces = {}

        # G1: Supervised Contrastive (Gold Standard Reference)
        V_contrastive = extract_contrastive_subspace(h_8, prem_indices, dist_indices, rank=rank)
        gen_subspaces["G_contrastive"] = V_contrastive

        # G2, G3, G4: Prompt Token Covariance Spectrum
        h_8_cent = h_8 - torch.mean(h_8, dim=0, keepdim=True)
        _, _, Vh_token = torch.linalg.svd(h_8_cent, full_matrices=False)
        gen_subspaces["G_cov_token_top"] = Vh_token[:2, :].T
        gen_subspaces["G_cov_token_mid"] = Vh_token[2:4, :].T if Vh_token.shape[0] >= 4 else Vh_token[:2, :].T
        gen_subspaces["G_cov_token_tail"] = Vh_token[4:6, :].T if Vh_token.shape[0] >= 6 else Vh_token[:2, :].T

        # G5: Population Context Covariance
        gen_subspaces["G_cov_prompt"] = V_cov_prompt

        # G6: Position-Residualized Token Covariance
        h_residual = h_8.clone()
        for t in range(T):
            if t in calib_pos_mean:
                h_residual[t] = h_residual[t] - calib_pos_mean[t]
        _, _, Vh_res = torch.linalg.svd(h_residual, full_matrices=False)
        gen_subspaces["G_cov_residual"] = Vh_res[:2, :].T

        # G7: Random Orthonormal Subspace (Null Control)
        # Sample using fixed seed per instance
        rng = np.random.RandomState(seed_conf + idx * 100)
        rand_mat = rng.randn(d_dim, rank)
        Q, _ = np.linalg.qr(rand_mat)
        gen_subspaces["G_random"] = torch.tensor(Q, dtype=torch.float32)

        # 3. Evaluate Each Generator
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

    # 4. Parameter Invariance Verification
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "Parameter mutation detected!"
    print(f"[REPRODUCIBILITY] Post-run Parameter SHA-256 verified invariant: {post_hash}")

    # 5. Statistical Scorecard
    m_base = float(np.mean(base_correct_list))
    print("\n" + "=" * 125)
    print(f"EXP032 SCORECARD: AUTONOMOUS ACTIVATION GEOMETRY GENERATORS (Base M_I = {m_base:6.4f})")
    print("=" * 125)
    print(f"{'Generator Key':<20} | {'Accuracy':<8} | {'Delta M (pp)':<14} | {'95% CI (Delta M)':<16} | {'Delta logP':<10} | {'McNemar vs Base':<16} | {'Spread vs Random'}")
    print("-" * 125)

    m_rand = float(np.mean(results["G_random"]["correct"]))

    output_data = {
        "metadata": {
            "experiment": "EXP032",
            "model_name": model_name,
            "parameter_sha256": post_hash,
            "target_layer": target_layer,
            "alpha": alpha,
            "n_instances": n_conf,
            "seed": seed_conf,
            "baseline_accuracy": m_base,
            "random_baseline_accuracy": m_rand
        },
        "generators": {}
    }

    for g_name in generators:
        corr = results[g_name]["correct"]
        dlp = results[g_name]["delta_logp"]

        acc = float(np.mean(corr))
        delta_m_pp = float((acc - m_base) * 100.0)
        ci_delta_m = compute_bootstrap_ci([(c - b) * 100.0 for c, b in zip(corr, base_correct_list)])
        mean_dlp = float(np.mean(dlp))

        b = sum(1 for c, b_i in zip(corr, base_correct_list) if c and not b_i)
        c = sum(1 for c, b_i in zip(corr, base_correct_list) if not c and b_i)
        p_mcnemar_base = exact_mcnemar(b, c)

        spread_vs_rand = float((acc - m_rand) * 100.0)

        print(f"{g_name:<20} | {acc:6.4f}   | {delta_m_pp:+6.1f} pp     | [{ci_delta_m[0]:+5.1f}, {ci_delta_m[1]:+5.1f}] pp | {mean_dlp:+8.4f}   | b={b}, c={c} (p={p_mcnemar_base:6.4f}) | {spread_vs_rand:+5.1f} pp")

        output_data["generators"][g_name] = {
            "accuracy": acc,
            "delta_m_pp": delta_m_pp,
            "delta_m_ci95_pp": ci_delta_m,
            "mean_delta_logp": mean_dlp,
            "mcnemar_vs_base": {"b": b, "c": c, "p_value": p_mcnemar_base},
            "spread_vs_random_pp": spread_vs_rand
        }

    # 6. Tri-State Resolution
    m_cov_token = output_data["generators"]["G_cov_token_top"]["delta_m_pp"]
    m_cov_res = output_data["generators"]["G_cov_residual"]["delta_m_pp"]

    if m_cov_token >= 8.0 and m_cov_token > (m_rand - m_base) * 100.0:
        outcome = "OUTCOME_1_AUTONOMOUS_RECOVERY_CONFIRMED"
        desc = "Unlabeled token covariance geometry autonomously discovers useful intervention directions without token supervision."
    elif m_cov_res >= 8.0 and m_cov_res > (m_rand - m_base) * 100.0:
        outcome = "OUTCOME_2_RESIDUALIZATION_SUPERIORITY"
        desc = "Token covariance requires position residualization to unlock autonomous intervention efficacy."
    else:
        outcome = "OUTCOME_3_UNSUPERVISED_GEOMETRY_REFUTED_OR_INSUFFICIENT"
        desc = "Unlabeled variance axes do not align with task-critical intervention directions; explicit semantic contrast remains necessary."

    output_data["tri_state_resolution"] = {
        "status": outcome,
        "description": desc
    }
    print("-" * 125)
    print(f"[TRI-STATE RESOLUTION]: {outcome}")
    print(f"[DESCRIPTION]: {desc}")

    # 7. Save JSON Ledger
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../runs/EXP032_covariance"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp032_covariance_results.json")
    with open(out_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n[OUTPUT] EXP032 results successfully saved to: {out_path}")

if __name__ == "__main__":
    main()
