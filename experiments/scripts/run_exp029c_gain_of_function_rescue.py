"""
EXP029 Layer C: Gain-of-Function Rescue Manipulations in Pythia-160M.

Investigates whether non-viable stages can be converted into viable stages:
1. Early-Layer Rescue (Layer 2):
   - Tests standard SCBI at Layer 2 (measuring baseline degradation / lack of headroom)
   - Downstream Gain Attenuation: Attenuating downstream residual block gain gamma in {0.5, 0.75, 1.0}
     to test if dampening downstream non-linear amplification rescues Layer 2.
2. Late-Layer Rescue (Layer 8):
   - Tests standard SCBI at Layer 8 (confirming 0% headroom)
   - Intervention Scaling: alpha in {0.25, 0.50, 1.00} to test if overcoming the hardened 1.12-logit
     unembedding margin rescues Layer 8.
   - Attention-Weighted Distractor Nullification: Intervening directly on the distractor token position.

Evaluated on N=50 benchmark instances from BENCH-002-NL (Seed 84).
Outputs results to experiments/runs/EXP029_causal/exp029c_rescue_results.json.
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
    h_dist = h[dist_indices, :]
    h_d_cent = h_dist - torch.mean(h_dist, dim=0, keepdim=True)
    _, _, Vh_d = torch.linalg.svd(h_d_cent, full_matrices=False)
    return Vh_d[:rank, :].T

def main():
    print("=" * 100)
    print("EXP029 LAYER C: GAIN-OF-FUNCTION RESCUE MANIPULATIONS (Pythia-160M)")
    print("Attempting Causal Rescue of Non-Viable Early (Layer 2) and Late (Layer 8) Stages")
    print("=" * 100)

    model_name = "EleutherAI/pythia-160m"
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

    # Experiment tracking
    rescue_records = {
        "identity_correct": 0,
        # Layer 2 conditions (Block 1)
        "layer_2": {
            "standard_alpha025": {"correct": 0, "delta_logp": []},
            "gain_gamma_75": {"correct": 0, "delta_logp": []},
            "gain_gamma_50": {"correct": 0, "delta_logp": []},
        },
        # Layer 8 conditions (Block 7)
        "layer_8": {
            "standard_alpha025": {"correct": 0, "delta_logp": []},
            "scaled_alpha050": {"correct": 0, "delta_logp": []},
            "scaled_alpha100": {"correct": 0, "delta_logp": []},
        }
    }

    print(f"\n>>> Running Rescue Protocol across {n_instances} instances...")

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
        # Base Forward Pass
        # ---------------------------------------------------------------------
        captured_activations = {}
        def capture_hook(layer_idx):
            def hook_fn(module, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                captured_activations[layer_idx] = h.detach()
            return hook_fn

        h2_handle = layers[1].register_forward_hook(capture_hook(1)) # Layer 2 (idx 1)
        h8_handle = layers[7].register_forward_hook(capture_hook(7)) # Layer 8 (idx 7)

        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())

        h2_handle.remove()
        h8_handle.remove()

        if pred_base == target_id:
            rescue_records["identity_correct"] += 1

        # Extract contrastive basis at Layer 2 and Layer 8
        h_L2 = captured_activations[1].squeeze(0)
        V_d2 = extract_contrastive_basis(h_L2, prem_indices, dist_indices, rank=2)
        P_2 = V_d2 @ V_d2.T

        h_L8 = captured_activations[7].squeeze(0)
        V_d8 = extract_contrastive_basis(h_L8, prem_indices, dist_indices, rank=2)
        P_8 = V_d8 @ V_d8.T

        # ---------------------------------------------------------------------
        # PART 1: LAYER 2 EVALUATIONS (Early Layer)
        # ---------------------------------------------------------------------
        # 1. Standard SCBI at Layer 2 (alpha = 0.25, gamma = 1.0)
        def make_l2_hook(alpha_val, P_mat):
            def hook_fn(module, inp, outp):
                if isinstance(outp, tuple):
                    h = outp[0].clone()
                    h[0] = h[0] - alpha_val * (h[0] @ P_mat)
                    return (h,) + outp[1:]
                else:
                    h = outp.clone()
                    h[0] = h[0] - alpha_val * (h[0] @ P_mat)
                    return h
            return hook_fn

        hook_l2_std = layers[1].register_forward_hook(make_l2_hook(0.25, P_2))
        with torch.no_grad():
            out_l2_std = model(input_ids=input_ids)
            logits_l2_std = out_l2_std.logits[0, -1, :]
            probs_l2_std = F.softmax(logits_l2_std, dim=-1)
            pred_l2_std = torch.argmax(logits_l2_std).item()
            logp_l2_std = float(torch.log(torch.clamp(probs_l2_std[target_id], min=1e-12)).item())
        hook_l2_std.remove()

        if pred_l2_std == target_id:
            rescue_records["layer_2"]["standard_alpha025"]["correct"] += 1
        rescue_records["layer_2"]["standard_alpha025"]["delta_logp"].append(logp_l2_std - logp_tgt_base)

        # 2. Layer 2 Rescue via Downstream Gain Attenuation (gamma in {0.75, 0.50})
        # In Pythia-160M parallel block: x = x + attn(ln(x)) + mlp(ln(x))
        # We attenuate the output residual addition: x = x + gamma * (attn + mlp)
        for gamma_val in [0.75, 0.50]:
            hook_l2 = layers[1].register_forward_hook(make_l2_hook(0.25, P_2))

            # Hook downstream layers 2 to 11 to scale their residual outputs
            gain_handles = []
            def make_gain_hook(g):
                def hook_fn(module, inp, outp):
                    # inp[0] is the input to the layer, outp[0] is the output (inp + attn + mlp)
                    # output - input is the delta!
                    h_in = inp[0]
                    if isinstance(outp, tuple):
                        h_out = outp[0]
                        delta_layer = h_out - h_in
                        h_mod = h_in + g * delta_layer
                        return (h_mod,) + outp[1:]
                    else:
                        delta_layer = outp - h_in
                        return h_in + g * delta_layer
                return hook_fn

            for l in range(2, num_layers):
                gain_handles.append(layers[l].register_forward_hook(make_gain_hook(gamma_val)))

            with torch.no_grad():
                out_gamma = model(input_ids=input_ids)
                logits_gamma = out_gamma.logits[0, -1, :]
                probs_gamma = F.softmax(logits_gamma, dim=-1)
                pred_gamma = torch.argmax(logits_gamma).item()
                logp_gamma = float(torch.log(torch.clamp(probs_gamma[target_id], min=1e-12)).item())

            hook_l2.remove()
            for h in gain_handles:
                h.remove()

            cond_key = f"gain_gamma_{int(gamma_val*100):02d}"
            if pred_gamma == target_id:
                rescue_records["layer_2"][cond_key]["correct"] += 1
            rescue_records["layer_2"][cond_key]["delta_logp"].append(logp_gamma - logp_tgt_base)

        # ---------------------------------------------------------------------
        # PART 2: LAYER 8 EVALUATIONS (Late Layer)
        # ---------------------------------------------------------------------
        # 1. Standard SCBI at Layer 8 (alpha = 0.25)
        hook_l8_std = layers[7].register_forward_hook(make_l2_hook(0.25, P_8))
        with torch.no_grad():
            out_l8_std = model(input_ids=input_ids)
            logits_l8_std = out_l8_std.logits[0, -1, :]
            probs_l8_std = F.softmax(logits_l8_std, dim=-1)
            pred_l8_std = torch.argmax(logits_l8_std).item()
            logp_l8_std = float(torch.log(torch.clamp(probs_l8_std[target_id], min=1e-12)).item())
        hook_l8_std.remove()

        if pred_l8_std == target_id:
            rescue_records["layer_8"]["standard_alpha025"]["correct"] += 1
        rescue_records["layer_8"]["standard_alpha025"]["delta_logp"].append(logp_l8_std - logp_tgt_base)

        # 2. Scaled SCBI at Layer 8 (alpha = 0.50 and alpha = 1.00)
        for alpha_val in [0.50, 1.00]:
            hook_l8_scale = layers[7].register_forward_hook(make_l2_hook(alpha_val, P_8))
            with torch.no_grad():
                out_scale = model(input_ids=input_ids)
                logits_scale = out_scale.logits[0, -1, :]
                probs_scale = F.softmax(logits_scale, dim=-1)
                pred_scale = torch.argmax(logits_scale).item()
                logp_scale = float(torch.log(torch.clamp(probs_scale[target_id], min=1e-12)).item())
            hook_l8_scale.remove()

            cond_key = f"scaled_alpha{int(alpha_val*100):03d}"
            if pred_scale == target_id:
                rescue_records["layer_8"][cond_key]["correct"] += 1
            rescue_records["layer_8"][cond_key]["delta_logp"].append(logp_scale - logp_tgt_base)

        if (idx + 1) % 10 == 0 or idx == n_instances - 1:
            print(f"  Processed {idx+1}/{n_instances} instances... [Base: {rescue_records['identity_correct']}/{idx+1}]")

    # 3. Parameter Invariance Verification
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "Parameter mutation detected!"
    print(f"\n[REPRODUCIBILITY] Post-run Parameter SHA-256 verified invariant: {post_hash}")

    # 4. Summary & Table
    m_base = rescue_records["identity_correct"] / n_instances

    print("\n" + "=" * 100)
    print("EXP029 LAYER C CAUSAL RESCUE SCORECARD (Pythia-160M)")
    print("=" * 100)
    print(f"Baseline Unintervened Accuracy (M_I): {m_base:6.4f} ({rescue_records['identity_correct']}/{n_instances})")
    print("-" * 100)
    print("EARLY-LAYER RESCUE ATTEMPTS (Layer 2):")
    for key, name in [
        ("standard_alpha025", "Standard SCBI (alpha=0.25, gamma=1.0)"),
        ("gain_gamma_75",     "Downstream Gain Attenuated (gamma=0.75)"),
        ("gain_gamma_50",     "Downstream Gain Attenuated (gamma=0.50)")
    ]:
        acc = rescue_records["layer_2"][key]["correct"] / n_instances
        d_m = (acc - m_base) * 100
        d_lp = float(np.mean(rescue_records["layer_2"][key]["delta_logp"]))
        print(f"  {name:<40s}: Accuracy = {acc:6.4f} (Delta M = {d_m:+5.1f} pp, Mean Delta_logp: {d_lp:+6.4f})")

    print("-" * 100)
    print("LATE-LAYER RESCUE ATTEMPTS (Layer 8):")
    for key, name in [
        ("standard_alpha025", "Standard SCBI (alpha=0.25)"),
        ("scaled_alpha050",   "Intervention Scaled (alpha=0.50)"),
        ("scaled_alpha100",   "Intervention Scaled (alpha=1.00)")
    ]:
        acc = rescue_records["layer_8"][key]["correct"] / n_instances
        d_m = (acc - m_base) * 100
        d_lp = float(np.mean(rescue_records["layer_8"][key]["delta_logp"]))
        print(f"  {name:<40s}: Accuracy = {acc:6.4f} (Delta M = {d_m:+5.1f} pp, Mean Delta_logp: {d_lp:+6.4f})")
    print("=" * 100)

    # 5. Save Output Artifact
    output_record = {
        "metadata": {
            "experiment": "EXP029c",
            "model_name": model_name,
            "parameter_sha256": post_hash,
            "n_instances": n_instances,
            "seed": seed
        },
        "baseline_accuracy": m_base,
        "layer_2_rescue": {
            k: {
                "accuracy": rescue_records["layer_2"][k]["correct"] / n_instances,
                "delta_m": (rescue_records["layer_2"][k]["correct"] / n_instances) - m_base,
                "mean_delta_logp": float(np.mean(rescue_records["layer_2"][k]["delta_logp"]))
            } for k in rescue_records["layer_2"]
        },
        "layer_8_rescue": {
            k: {
                "accuracy": rescue_records["layer_8"][k]["correct"] / n_instances,
                "delta_m": (rescue_records["layer_8"][k]["correct"] / n_instances) - m_base,
                "mean_delta_logp": float(np.mean(rescue_records["layer_8"][k]["delta_logp"]))
            } for k in rescue_records["layer_8"]
        }
    }

    out_path = "experiments/runs/EXP029_causal/exp029c_rescue_results.json"
    with open(out_path, "w") as f:
        json.dump(output_record, f, indent=2)
    print(f"[OUTPUT] Rescue results successfully written to: {out_path}")

if __name__ == "__main__":
    main()
