"""
EXP029 Layer A: Observational Profiler of Stage Viability (Pythia-160M).

Computes full 12-layer profile of:
1. Participation Ratio PR(l) [Intrinsic dimensionality of residual stream]
2. Downstream Jacobian Receptivity J(l) [Logit sensitivity to residual perturbation]
3. Downstream Attention Sensitivity Delta_A(l) [Shift in downstream attention weights]
4. Empirical Representation Score S_rep(l) [EXP028 baseline predictor]
5. Direct Unembedding Alignment rho_U(l) [Cosine similarity to W_tgt - W_dist]
6. Linear Fisher Contrastive Margin F(l) [Post-hoc target/distractor separation]

Compares known viable layer (Layer 4, Delta M = +12%) vs. known failed layer (Layer 8, Delta M = 0%).
Outputs results to experiments/runs/EXP029_causal/exp029a_observational_profiles.json.
"""

import os
import sys
import time
import json
import hashlib
from datetime import datetime, timezone
import numpy as np
import torch
import torch.nn.functional as F
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

def compute_participation_ratio(activations):
    """
    activations: Tensor of shape (N, d)
    PR = (Tr(Sigma))^2 / Tr(Sigma^2) = (sum sigma_i)^2 / sum(sigma_i^2)
    """
    act_centered = activations - torch.mean(activations, dim=0, keepdim=True)
    # Use SVD of data matrix (N, d)
    # singular values s_i relates to eigenvalues lambda_i of Sigma by lambda_i = s_i^2 / (N - 1)
    _, s, _ = torch.linalg.svd(act_centered, full_matrices=False)
    lambdas = (s ** 2) / max(1, activations.shape[0] - 1)
    sum_lambda = torch.sum(lambdas).item()
    sum_lambda_sq = torch.sum(lambdas ** 2).item()
    if sum_lambda_sq == 0:
        return 1.0
    return float((sum_lambda ** 2) / sum_lambda_sq)

def main():
    print("=" * 100)
    print("EXP029 LAYER A: OBSERVATIONAL PROFILER (EleutherAI/pythia-160m)")
    print("Decomposing Geometric & Computational Properties of Stage Viability")
    print("=" * 100)

    model_name = "EleutherAI/pythia-160m"
    n_calib = 20
    seed_calib = 123
    n_probe = 50
    seed_probe = 84

    # 1. Load Datasets
    # Phase A: Unlabeled calibration prompts for label-free diagnostics
    calib_data = generate_bench_002_nl(n_instances=n_calib, seed=seed_calib)
    unlabeled_prompts = [inst["base"] for inst in calib_data]
    print(f"[FIREWALL] Loaded {len(unlabeled_prompts)} unlabeled calibration prompts.")

    # Phase B: Mechanistic probe instances for post-hoc validation
    probe_data = generate_bench_002_nl(n_instances=n_probe, seed=seed_probe)
    print(f"[PROBE] Loaded {len(probe_data)} mechanistic probe instances.")

    # 2. Load Model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run Parameter SHA-256: {pre_hash}")

    layers = model.gpt_neox.layers
    num_layers = len(layers)
    d_model = model.config.hidden_size
    print(f"[ARCHITECTURE] Pythia-160M: {num_layers} layers, d_model = {d_model}")

    # Unembedding matrix for W_U probes: shape (vocab_size, d_model)
    W_U = model.embed_out.weight.detach()

    # Dictionary to collect all layer metrics
    layer_profiles = {}

    # =========================================================================
    # STEP 1: Compute Participation Ratio PR(l) across layers on unlabeled data
    # =========================================================================
    print("\n>>> Step 1: Measuring Intrinsic Dimensionality (Participation Ratio) on Unlabeled Prompts...")
    layer_activations = {l: [] for l in range(num_layers)}

    for prompt in unlabeled_prompts:
        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            # Hook all layers to capture residual output
            captured = {}
            handles = []
            for l in range(num_layers):
                def make_hook(layer_idx):
                    def hook_fn(module, inp, outp):
                        h = outp[0] if isinstance(outp, tuple) else outp
                        captured[layer_idx] = h.detach()
                    return hook_fn
                handles.append(layers[l].register_forward_hook(make_hook(l)))

            model(**inputs)

            for h in handles:
                h.remove()

            for l in range(num_layers):
                # Token activations across all positions in the prompt
                layer_activations[l].append(captured[l].squeeze(0).cpu())

    pr_profile = {}
    for l in range(num_layers):
        all_tokens_l = torch.cat(layer_activations[l], dim=0) # shape (total_tokens, d_model)
        pr_val = compute_participation_ratio(all_tokens_l)
        pr_profile[l] = pr_val
        print(f"  Layer {l:2d}: Participation Ratio PR = {pr_val:6.2f} / {d_model}")

    # =========================================================================
    # STEP 2: Compute Downstream Suffix Jacobian Receptivity J(l)
    # =========================================================================
    print("\n>>> Step 2: Measuring Downstream Suffix Jacobian Receptivity J(l)...")
    jacobian_profile = {}
    sigma_perturb = 0.1

    for l in range(num_layers):
        jac_ratios = []
        for prompt in unlabeled_prompts[:10]: # 10 prompts for efficiency
            inputs = tokenizer(prompt, return_tensors="pt")
            # Unperturbed forward pass
            with torch.no_grad():
                out_base = model(**inputs)
                logits_base = out_base.logits[0, -1, :].detach()

            # Perturbed forward pass at layer l
            delta = torch.randn(1, 1, d_model) * sigma_perturb
            delta_norm = float(torch.norm(delta).item())

            def inject_perturbation(module, inp, outp):
                if isinstance(outp, tuple):
                    h = outp[0].clone()
                    h[:, -1:, :] += delta.to(h.device)
                    return (h,) + outp[1:]
                else:
                    h = outp.clone()
                    h[:, -1:, :] += delta.to(h.device)
                    return h

            handle = layers[l].register_forward_hook(inject_perturbation)
            with torch.no_grad():
                out_perturbed = model(**inputs)
                logits_perturbed = out_perturbed.logits[0, -1, :].detach()
            handle.remove()

            logit_diff_norm = float(torch.norm(logits_perturbed - logits_base).item())
            jac_ratios.append(logit_diff_norm / max(1e-8, delta_norm))

        mean_jac = float(np.mean(jac_ratios))
        jacobian_profile[l] = mean_jac
        print(f"  Layer {l:2d}: Downstream Receptivity J = {mean_jac:6.3f}")

    # =========================================================================
    # STEP 3: Compute Empirical Representation Score S_rep(l)
    # =========================================================================
    print("\n>>> Step 3: Measuring Empirical Representation Score S_rep(l)...")
    s_rep_profile = {}

    for l in range(num_layers):
        si_list = []
        ortho_list = []
        for prompt in unlabeled_prompts:
            text = prompt
            try:
                p_end = text.index(" Distractor:")
                d_end = text.index(" Question:")
            except ValueError:
                continue

            enc = tokenizer(text, return_offsets_mapping=True, return_tensors="pt")
            offsets = enc.offset_mapping[0].tolist()
            input_ids = enc.input_ids

            prem_indices = [i for i, (s, e) in enumerate(offsets) if e <= p_end and s < e]
            dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]

            if not prem_indices or not dist_indices:
                continue

            captured = {}
            def hook_fn(module, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                captured["h"] = h.detach()

            h_hook = layers[l].register_forward_hook(hook_fn)
            with torch.no_grad():
                model(input_ids=input_ids)
            h_hook.remove()

            h = captured["h"].squeeze(0)
            h_prem = h[prem_indices, :]
            h_dist = h[dist_indices, :]

            # SVD to get top-2 basis
            h_p_cent = h_prem - torch.mean(h_prem, dim=0, keepdim=True)
            _, _, Vh_p = torch.linalg.svd(h_p_cent, full_matrices=False)
            V_p = Vh_p[:2, :].T

            h_d_cent = h_dist - torch.mean(h_dist, dim=0, keepdim=True)
            _, _, Vh_d = torch.linalg.svd(h_d_cent, full_matrices=False)
            V_d = Vh_d[:2, :].T

            # Project distractor energy
            d_prem = torch.mean(torch.norm(h_dist @ V_p @ V_p.T, dim=-1)).item()
            d_dist = torch.mean(torch.norm(h_dist @ V_d @ V_d.T, dim=-1)).item()

            si = max(0.0, (d_dist - d_prem) / max(1e-8, d_dist))
            si_list.append(si)

            overlap = float(torch.norm(V_p.T @ V_d).item()) / np.sqrt(2.0)
            ortho = 1.0 - min(1.0, overlap)
            ortho_list.append(ortho)

        mean_si = float(np.mean(si_list)) if si_list else 0.0
        mean_ortho = float(np.mean(ortho_list)) if ortho_list else 0.0
        s_rep = mean_si * mean_ortho
        s_rep_profile[l] = s_rep
        print(f"  Layer {l:2d}: S_rep = {s_rep:6.4f} (SI = {mean_si:6.4f}, Ortho = {mean_ortho:6.4f})")

    # =========================================================================
    # STEP 4: Compute Direct Unembedding Alignment rho_U(l) & Fisher Margin F(l)
    # =========================================================================
    print("\n>>> Step 4: Measuring Mechanistic Probes: Unembedding Alignment rho_U(l) & Fisher Margin F(l)...")
    rho_u_profile = {}
    fisher_profile = {}

    for l in range(num_layers):
        rho_list = []
        fisher_list = []

        for inst in probe_data:
            target_token = inst["target"]
            distractor_token = inst["distractor"]

            # Token IDs
            target_id = tokenizer.encode(" " + target_token.strip())[0] if tokenizer.encode(" " + target_token.strip()) else tokenizer.encode(target_token.strip())[0]
            dist_id = tokenizer.encode(" " + distractor_token.strip())[0] if tokenizer.encode(" " + distractor_token.strip()) else tokenizer.encode(distractor_token.strip())[0]

            w_tgt = W_U[target_id, :]
            w_dst = W_U[dist_id, :]
            w_diff = (w_tgt - w_dst)
            w_diff_unit = w_diff / torch.norm(w_diff)

            # Capture layer representation
            captured = {}
            def hook_fn(module, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                captured["h"] = h.detach()

            h_hook = layers[l].register_forward_hook(hook_fn)
            with torch.no_grad():
                model(input_ids=tokenizer(inst["base"], return_tensors="pt").input_ids)
            h_hook.remove()

            h_last = captured["h"][0, -1, :] # final token representation

            # Unembedding cosine alignment: projection of h_last onto w_diff
            rho = float(torch.abs(torch.dot(h_last / torch.norm(h_last), w_diff_unit.to(h_last.device))).item())
            rho_list.append(rho)

            # Contrastive separation: difference between projection on w_tgt vs w_dst
            margin = float((torch.dot(h_last, w_tgt.to(h_last.device)) - torch.dot(h_last, w_dst.to(h_last.device))).item())
            fisher_list.append(margin)

        mean_rho = float(np.mean(rho_list))
        mean_fisher = float(np.mean(fisher_list))
        rho_u_profile[l] = mean_rho
        fisher_profile[l] = mean_fisher
        print(f"  Layer {l:2d}: Unembedding Align rho_U = {mean_rho:6.4f}, Unembedding Margin F = {mean_fisher:6.3f}")

    # =========================================================================
    # STEP 5: Consolidate & Analyze Layer 4 vs. Layer 8 Contrast
    # =========================================================================
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "Parameter mutation detected!"
    print(f"\n[REPRODUCIBILITY] Post-run Parameter SHA-256 verified invariant: {post_hash}")

    output_record = {
        "metadata": {
            "experiment": "EXP029a",
            "model_name": model_name,
            "parameter_sha256": post_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "n_calib": n_calib,
            "n_probe": n_probe
        },
        "profiles": {}
    }

    print("\n" + "=" * 100)
    print("EXP029a OBSERVATIONAL PROFILE SUMMARY TABLE (Pythia-160M)")
    print("=" * 100)
    print(f"{'Layer':<6} | {'Norm Depth':<10} | {'PR (dim)':<10} | {'Jacobian J':<11} | {'S_rep':<10} | {'rho_U (align)':<14} | {'Known Efficacy':<15}")
    print("-" * 100)

    for l in range(num_layers):
        lambda_val = l / num_layers
        pr = pr_profile[l]
        jac = jacobian_profile[l]
        s_rep = s_rep_profile[l]
        rho_u = rho_u_profile[l]

        known_str = "—"
        if l == 4:
            known_str = "L4: VIABLE (+12%)"
        elif l == 8:
            known_str = "L8: FAILED (0%)"

        print(f"{l:<6d} | {lambda_val:<10.3f} | {pr:<10.2f} | {jac:<11.3f} | {s_rep:<10.4f} | {rho_u:<14.4f} | {known_str:<15}")

        output_record["profiles"][l] = {
            "layer": l,
            "normalized_depth": lambda_val,
            "participation_ratio": pr,
            "jacobian_receptivity": jac,
            "s_representation": s_rep,
            "unembedding_alignment": rho_u,
            "unembedding_margin": fisher_profile[l]
        }

    os.makedirs("experiments/runs/EXP029_causal", exist_ok=True)
    out_path = "experiments/runs/EXP029_causal/exp029a_observational_profiles.json"
    with open(out_path, "w") as f:
        json.dump(output_record, f, indent=2)

    print(f"\n[OUTPUT] Full observational profile successfully written to: {out_path}")

if __name__ == "__main__":
    main()
