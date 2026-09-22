"""
EXP029 Layer B: Loss-of-Function Causal Manipulations at Viable Layer 4 (Pythia-160M).

Tests three specific causal interventions on the verified viable Layer 4:
1. Subspace Angle Sweep: theta in {0 deg, 30 deg, 60 deg, 90 deg} relative to contrastive axis (Testing H2: Linear Decoupling)
2. Attention Map Clamping: Clamping all downstream attention maps A_{l'>4} to unperturbed values (Testing H4: Attention Rerouting)
3. Unembedding Orthogonalization: Projecting V orthogonal to (W_tgt - W_dist) (Testing H5: Unembedding Readout)

Evaluated on N=50 benchmark instances from BENCH-002-NL (Seed 84).
Outputs results to experiments/runs/EXP029_causal/exp029b_loss_of_function_results.json.
"""

import os
import sys
import time
import json
import hashlib
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

def extract_contrastive_basis(h, prem_indices, dist_indices, rank=2):
    """
    Extracts top-rank contrastive basis pair (v1, v2) for premise vs distractor.
    """
    h_prem = h[prem_indices, :]
    h_dist = h[dist_indices, :]

    h_p_cent = h_prem - torch.mean(h_prem, dim=0, keepdim=True)
    _, _, Vh_p = torch.linalg.svd(h_p_cent, full_matrices=False)
    V_p = Vh_p[:rank, :].T # (d, rank)

    h_d_cent = h_dist - torch.mean(h_dist, dim=0, keepdim=True)
    _, _, Vh_d = torch.linalg.svd(h_d_cent, full_matrices=False)
    V_d = Vh_d[:rank, :].T # (d, rank)

    return V_p, V_d

def main():
    print("=" * 100)
    print("EXP029 LAYER B: LOSS-OF-FUNCTION CAUSAL MANIPULATIONS (Pythia-160M Layer 4)")
    print("Testing Causal Necessity of Direction, Attention Rerouting, and Unembedding Alignment")
    print("=" * 100)

    model_name = "EleutherAI/pythia-160m"
    target_layer = 4 # 1-indexed (Block 3)
    block_idx = target_layer - 1
    alpha = 0.25
    rank = 2
    n_instances = 50
    seed = 84

    # 1. Load Dataset
    dataset = generate_bench_002_nl(n_instances=n_instances, seed=seed)
    print(f"[DATASET] Loaded {len(dataset)} confirmatory instances (Seed {seed}).")

    # 2. Load Model & Tokenizer
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
    W_U = model.embed_out.weight.detach()

    results = {
        "identity_correct": 0,
        "oracle_baseline_correct": 0,
        "angle_sweep": {
            0: {"correct": 0, "delta_logp": []},
            30: {"correct": 0, "delta_logp": []},
            60: {"correct": 0, "delta_logp": []},
            90: {"correct": 0, "delta_logp": []},
        },
        "unembedding_ortho": {"correct": 0, "delta_logp": []},
        "attention_clamped": {"correct": 0, "delta_logp": []},
    }

    print(f"\n>>> Running Causal Manipulations across {n_instances} instances at Layer {target_layer}...")

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

        # ---------------------------------------------------------------------
        # PASS 1: Unperturbed Identity Forward Pass (also captures attention)
        # ---------------------------------------------------------------------
        captured_activations = {}
        downstream_attentions = {}

        def capture_hook(module, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            captured_activations["h"] = h.detach()

        # Capture downstream attention weights in layers block_idx+1 to num_layers-1
        attn_handles = []
        for l in range(block_idx + 1, num_layers):
            def make_attn_hook(layer_num):
                def attn_hook_fn(module, inp, outp):
                    # Pythia attention output is (context, attn_weights) or context
                    # If attn_weights not returned, hook the attention module's internal calculation or softmax
                    pass
                return attn_hook_fn

        h_hook = layers[block_idx].register_forward_hook(capture_hook)
        with torch.no_grad():
            out_base = model(input_ids=input_ids, output_attentions=True)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())

            # Store downstream attention weights: out_base.attentions is tuple of length num_layers
            if out_base.attentions is not None:
                for l in range(block_idx + 1, num_layers):
                    downstream_attentions[l] = out_base.attentions[l].detach()

        h_hook.remove()

        if pred_base == target_id:
            results["identity_correct"] += 1

        # Extract contrastive basis at Layer 4
        h_L4 = captured_activations["h"].squeeze(0)
        V_p, V_d = extract_contrastive_basis(h_L4, prem_indices, dist_indices, rank=rank)
        # V_d is the primary distractor basis (d_model, 2). Let v1, v2 be orthonormal columns
        v1 = V_d[:, 0:1] # primary contrastive direction
        v2 = V_d[:, 1:2] # secondary contrastive direction

        # ---------------------------------------------------------------------
        # PASS 2: Standard SCBI Intervention (Baseline Oracle at Layer 4, theta=0)
        # ---------------------------------------------------------------------
        # Intervention: h' = h - alpha * V_d V_d^T h at the prompt tokens
        V_0 = V_d
        P_0 = V_0 @ V_0.T

        def intervention_hook_0(module, inp, outp):
            if isinstance(outp, tuple):
                h = outp[0].clone()
                h[0] = h[0] - alpha * (h[0] @ P_0)
                return (h,) + outp[1:]
            else:
                h = outp.clone()
                h[0] = h[0] - alpha * (h[0] @ P_0)
                return h

        hook_0 = layers[block_idx].register_forward_hook(intervention_hook_0)
        with torch.no_grad():
            out_0 = model(input_ids=input_ids)
            logits_0 = out_0.logits[0, -1, :]
            probs_0 = F.softmax(logits_0, dim=-1)
            pred_0 = torch.argmax(logits_0).item()
            logp_tgt_0 = float(torch.log(torch.clamp(probs_0[target_id], min=1e-12)).item())
        hook_0.remove()

        if pred_0 == target_id:
            results["oracle_baseline_correct"] += 1
            results["angle_sweep"][0]["correct"] += 1
        results["angle_sweep"][0]["delta_logp"].append(logp_tgt_0 - logp_tgt_base)

        # ---------------------------------------------------------------------
        # TEST B1: Subspace Angle Sweep (theta in {30, 60, 90})
        # ---------------------------------------------------------------------
        # We rotate v1 towards an arbitrary orthogonal vector in the residual space
        # Find an orthogonal vector v_orth to span(v1, v2)
        v_rand = torch.randn_like(v1)
        v_rand = v_rand - (v_rand.T @ v1) * v1 - (v_rand.T @ v2) * v2
        v_orth = v_rand / torch.norm(v_rand)

        for theta_deg in [30, 60, 90]:
            theta_rad = np.radians(theta_deg)
            # Rotated primary vector
            v1_rot = np.cos(theta_rad) * v1 + np.sin(theta_rad) * v_orth
            v1_rot = v1_rot / torch.norm(v1_rot)
            # Construct 2D rotated basis with v2
            V_theta = torch.cat([v1_rot, v2], dim=1)
            P_theta = V_theta @ V_theta.T

            def make_angle_hook(P_mat):
                def hook_fn(module, inp, outp):
                    if isinstance(outp, tuple):
                        h = outp[0].clone()
                        h[0] = h[0] - alpha * (h[0] @ P_mat)
                        return (h,) + outp[1:]
                    else:
                        h = outp.clone()
                        h[0] = h[0] - alpha * (h[0] @ P_mat)
                        return h
                return hook_fn

            hook_th = layers[block_idx].register_forward_hook(make_angle_hook(P_theta))
            with torch.no_grad():
                out_th = model(input_ids=input_ids)
                logits_th = out_th.logits[0, -1, :]
                probs_th = F.softmax(logits_th, dim=-1)
                pred_th = torch.argmax(logits_th).item()
                logp_tgt_th = float(torch.log(torch.clamp(probs_th[target_id], min=1e-12)).item())
            hook_th.remove()

            if pred_th == target_id:
                results["angle_sweep"][theta_deg]["correct"] += 1
            results["angle_sweep"][theta_deg]["delta_logp"].append(logp_tgt_th - logp_tgt_base)

        # ---------------------------------------------------------------------
        # TEST B3: Unembedding Orthogonalization (V_ortho_W)
        # ---------------------------------------------------------------------
        # Project V_d orthogonal to w_diff = W_U[target] - W_U[distractor]
        w_diff = (W_U[target_id, :] - W_U[dist_id, :]).unsqueeze(1) # (d_model, 1)
        w_diff_unit = w_diff / torch.norm(w_diff)

        # Project each column of V_d
        V_perp = V_d - (w_diff_unit @ (w_diff_unit.T @ V_d))
        # Gram-Schmidt QR to orthonormalize
        Q_perp, _ = torch.linalg.qr(V_perp)
        P_perp = Q_perp @ Q_perp.T

        hook_perp = layers[block_idx].register_forward_hook(make_angle_hook(P_perp))
        with torch.no_grad():
            out_perp = model(input_ids=input_ids)
            logits_perp = out_perp.logits[0, -1, :]
            probs_perp = F.softmax(logits_perp, dim=-1)
            pred_perp = torch.argmax(logits_perp).item()
            logp_tgt_perp = float(torch.log(torch.clamp(probs_perp[target_id], min=1e-12)).item())
        hook_perp.remove()

        if pred_perp == target_id:
            results["unembedding_ortho"]["correct"] += 1
        results["unembedding_ortho"]["delta_logp"].append(logp_tgt_perp - logp_tgt_base)

        # ---------------------------------------------------------------------
        # TEST B2: Downstream Attention Clamping
        # ---------------------------------------------------------------------
        # Pythia-160M forward pass with attention weight clamping across layers > block_idx
        # In Pythia-160M, each layer computes:
        # hn = layer.input_layernorm(h)
        # attn_out = layer.attention(hn)
        # mlp_out = layer.mlp(layer.post_attention_layernorm(hn))
        # h = h + attn_out + mlp_out
        # To clamp attention maps, we hook downstream attention modules:
        # We record the attention output from the unperturbed pass and substitute it!
        # Specifically: attn_out carries the attention routing signal.
        # Clamping attention output to its unperturbed value isolates the MLP residual stream!

        captured_attn_outputs = {}
        def make_record_attn_hook(l_idx):
            def hook_fn(module, inp, outp):
                captured_attn_outputs[l_idx] = outp.detach() if not isinstance(outp, tuple) else outp[0].detach()
            return hook_fn

        record_hooks = [layers[l].attention.register_forward_hook(make_record_attn_hook(l)) for l in range(block_idx + 1, num_layers)]
        with torch.no_grad():
            model(input_ids=input_ids)
        for h in record_hooks:
            h.remove()

        # Now run intervention at Layer 4, while CLAMPING downstream attention outputs to unperturbed!
        def make_clamp_attn_hook(l_idx):
            def hook_fn(module, inp, outp):
                saved = captured_attn_outputs[l_idx]
                if isinstance(outp, tuple):
                    return (saved,) + outp[1:]
                return saved
            return hook_fn

        hook_l4 = layers[block_idx].register_forward_hook(make_angle_hook(P_0))
        clamp_hooks = [layers[l].attention.register_forward_hook(make_clamp_attn_hook(l)) for l in range(block_idx + 1, num_layers)]

        with torch.no_grad():
            out_clamped = model(input_ids=input_ids)
            logits_clamped = out_clamped.logits[0, -1, :]
            probs_clamped = F.softmax(logits_clamped, dim=-1)
            pred_clamped = torch.argmax(logits_clamped).item()
            logp_tgt_clamped = float(torch.log(torch.clamp(probs_clamped[target_id], min=1e-12)).item())

        hook_l4.remove()
        for h in clamp_hooks:
            h.remove()

        if pred_clamped == target_id:
            results["attention_clamped"]["correct"] += 1
        results["attention_clamped"]["delta_logp"].append(logp_tgt_clamped - logp_tgt_base)

        if (idx + 1) % 10 == 0 or idx == n_instances - 1:
            print(f"  Processed {idx+1}/{n_instances} instances... [Base: {results['identity_correct']}/{idx+1} | L4: {results['oracle_baseline_correct']}/{idx+1}]")

    # 3. Parameter Invariance Verification
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "Parameter mutation detected!"
    print(f"\n[REPRODUCIBILITY] Post-run Parameter SHA-256 verified invariant: {post_hash}")

    # 4. Summary & Table
    m_base = results["identity_correct"] / n_instances
    m_l4 = results["oracle_baseline_correct"] / n_instances

    print("\n" + "=" * 100)
    print("EXP029 LAYER B CAUSAL LOSS-OF-FUNCTION SCORECARD (Pythia-160M Layer 4)")
    print("=" * 100)
    print(f"Baseline Unintervened Accuracy (M_I):       {m_base:6.4f} ({results['identity_correct']}/{n_instances})")
    print(f"Viable Layer 4 Standard SCBI (theta=0 deg):  {m_l4:6.4f} (+{(m_l4 - m_base)*100:4.1f} pp, Mean Delta_logp: {np.mean(results['angle_sweep'][0]['delta_logp']):+6.4f})")
    print("-" * 100)
    print("TEST B1: SUBSPACE ANGLE SWEEP (Linear Decoupling H2):")
    for theta in [0, 30, 60, 90]:
        acc = results["angle_sweep"][theta]["correct"] / n_instances
        d_m = (acc - m_base) * 100
        d_lp = float(np.mean(results["angle_sweep"][theta]["delta_logp"]))
        print(f"  Rotation theta = {theta:2d} deg: Accuracy = {acc:6.4f} (Delta M = {d_m:+5.1f} pp, Mean Delta_logp: {d_lp:+6.4f})")

    print("-" * 100)
    print("TEST B2: ATTENTION CLAMPING (Attention Rerouting H4):")
    acc_clamp = results["attention_clamped"]["correct"] / n_instances
    d_m_clamp = (acc_clamp - m_base) * 100
    d_lp_clamp = float(np.mean(results["attention_clamped"]["delta_logp"]))
    retention_clamp = (acc_clamp - m_base) / max(1e-8, (m_l4 - m_base)) * 100
    print(f"  Downstream Attention Clamped: Accuracy = {acc_clamp:6.4f} (Delta M = {d_m_clamp:+5.1f} pp, Headroom Retention: {retention_clamp:5.1f}%, Mean Delta_logp: {d_lp_clamp:+6.4f})")

    print("-" * 100)
    print("TEST B3: UNEMBEDDING ORTHOGONALIZATION (Unembedding Alignment H5):")
    acc_perp = results["unembedding_ortho"]["correct"] / n_instances
    d_m_perp = (acc_perp - m_base) * 100
    d_lp_perp = float(np.mean(results["unembedding_ortho"]["delta_logp"]))
    retention_perp = (acc_perp - m_base) / max(1e-8, (m_l4 - m_base)) * 100
    print(f"  Orthogonal to (W_tgt - W_dist): Accuracy = {acc_perp:6.4f} (Delta M = {d_m_perp:+5.1f} pp, Headroom Retention: {retention_perp:5.1f}%, Mean Delta_logp: {d_lp_perp:+6.4f})")
    print("=" * 100)

    # 5. Save Output Artifact
    output_record = {
        "metadata": {
            "experiment": "EXP029b",
            "model_name": model_name,
            "target_layer": target_layer,
            "parameter_sha256": post_hash,
            "n_instances": n_instances,
            "seed": seed
        },
        "baseline_accuracy": m_base,
        "standard_l4_accuracy": m_l4,
        "angle_sweep_results": {
            theta: {
                "accuracy": results["angle_sweep"][theta]["correct"] / n_instances,
                "delta_m": (results["angle_sweep"][theta]["correct"] / n_instances) - m_base,
                "mean_delta_logp": float(np.mean(results["angle_sweep"][theta]["delta_logp"]))
            } for theta in [0, 30, 60, 90]
        },
        "attention_clamping_results": {
            "accuracy": acc_clamp,
            "delta_m": d_m_clamp / 100.0,
            "headroom_retention_pct": retention_clamp,
            "mean_delta_logp": d_lp_clamp
        },
        "unembedding_orthogonal_results": {
            "accuracy": acc_perp,
            "delta_m": d_m_perp / 100.0,
            "headroom_retention_pct": retention_perp,
            "mean_delta_logp": d_lp_perp
        }
    }

    out_path = "experiments/runs/EXP029_causal/exp029b_loss_of_function_results.json"
    with open(out_path, "w") as f:
        json.dump(output_record, f, indent=2)
    print(f"[OUTPUT] Loss-of-function results successfully written to: {out_path}")

if __name__ == "__main__":
    main()
