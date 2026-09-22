"""
EXP030: Controller vs. Stage Viability Landscape Matrix (Pythia-160M).

Factorial 5 Depths x 3 Controllers x 3 Strengths (45 conditions) on N=50 instances:
- Depths: l in {2, 4, 6, 8, 10}
- Controllers: C0 (Ungated Linear), C1 (Soft Sigmoid), C2 (Contrastive Hard Gate O5)
- Strengths: alpha in {0.10, 0.25, 0.50}

Tracks:
- Delta M(l, g, alpha) with 1,000-resample bootstrap 95% CI
- Mean Delta log p(y_correct) with 1,000-resample bootstrap 95% CI
- Viability sets V(l) and failure boundaries

Saves full landscape to experiments/runs/EXP030_landscape/exp030_landscape_results.json.
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

def compute_bootstrap_ci(data, n_boot=1000, ci=0.95):
    if len(data) == 0:
        return [0.0, 0.0]
    arr = np.array(data)
    boot_means = [np.mean(np.random.choice(arr, size=len(arr), replace=True)) for _ in range(n_boot)]
    alpha_ci = (1.0 - ci) / 2.0
    low = float(np.percentile(boot_means, alpha_ci * 100))
    high = float(np.percentile(boot_means, (1.0 - alpha_ci) * 100))
    return [low, high]

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
    print("=" * 100)
    print("EXP030: CONTROLLER VS. STAGE VIABILITY LANDSCAPE MATRIX (Pythia-160M)")
    print("Factorial 5 Depths x 3 Controllers x 3 Strengths (45 Conditions)")
    print("=" * 100)

    model_name = "EleutherAI/pythia-160m"
    n_instances = 50
    seed = 84

    # 1. Configuration Grids
    layers_to_test = [2, 4, 6, 8, 10]
    controllers = ["C0_ungated", "C1_soft", "C2_hard"]
    alphas = [0.10, 0.25, 0.50]
    rank = 2

    # 2. Load Dataset
    dataset = generate_bench_002_nl(n_instances=n_instances, seed=seed)
    print(f"[DATASET] Loaded {len(dataset)} confirmatory instances (Seed {seed}).")

    # 3. Load Model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run Parameter SHA-256: {pre_hash}")

    model_layers = model.gpt_neox.layers
    num_layers = len(model_layers)

    # Pre-allocate results matrix
    # cell: (l, ctrl, alpha) -> {correct: [], delta_logp: []}
    grid_results = {}
    for l in layers_to_test:
        for ctrl in controllers:
            for a in alphas:
                key = f"L{l}_{ctrl}_a{int(a*100):02d}"
                grid_results[key] = {
                    "layer": l,
                    "controller": ctrl,
                    "alpha": a,
                    "correct": [],
                    "delta_logp": []
                }

    base_correct_list = []
    base_logp_list = []

    print(f"\n>>> Running Factorial Grid across {n_instances} instances...")
    start_time = time.time()

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
        # Base Forward Pass: Captures Baseline and Layer Representations
        # ---------------------------------------------------------------------
        captured_layers = {}
        def make_capture_hook(l_idx):
            def hook_fn(module, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                captured_layers[l_idx] = h.detach()
            return hook_fn

        cap_handles = [model_layers[l - 1].register_forward_hook(make_capture_hook(l)) for l in layers_to_test]
        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            logits_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(logits_base, dim=-1)
            pred_base = torch.argmax(logits_base).item()
            logp_tgt_base = float(torch.log(torch.clamp(probs_base[target_id], min=1e-12)).item())

        for h in cap_handles:
            h.remove()

        base_is_corr = (pred_base == target_id)
        base_correct_list.append(base_is_corr)
        base_logp_list.append(logp_tgt_base)

        # Precompute Subspaces and Gating Values for each layer
        layer_subspaces = {}
        for l in layers_to_test:
            h_l = captured_layers[l].squeeze(0) # [T, d]
            V_p, V_m = extract_contrastive_subspaces(h_l, prem_indices, dist_indices, rank=rank)
            P_m = V_m @ V_m.T
            P_p = V_p @ V_p.T

            # Token differential: d_t = energy_dist - energy_prem
            proj_m = h_l @ P_m
            proj_p = h_l @ P_p
            d_tokens = torch.norm(proj_m, dim=-1) - torch.norm(proj_p, dim=-1)

            layer_subspaces[l] = {
                "P_m": P_m,
                "d_tokens": d_tokens
            }

        # ---------------------------------------------------------------------
        # Run 45 Cell Interventions for this instance
        # ---------------------------------------------------------------------
        for l in layers_to_test:
            block_idx = l - 1
            P_m = layer_subspaces[l]["P_m"]
            d_tokens = layer_subspaces[l]["d_tokens"]

            for ctrl in controllers:
                # Compute token gate g_t
                if ctrl == "C0_ungated":
                    gate = torch.ones_like(d_tokens).unsqueeze(-1) # [T, 1]
                elif ctrl == "C1_soft":
                    tau = torch.median(d_tokens)
                    tau_scale = torch.std(d_tokens) + 1e-6
                    gate = torch.sigmoid((d_tokens - tau) / tau_scale).unsqueeze(-1) # [T, 1]
                elif ctrl == "C2_hard":
                    gate = (d_tokens > 0.0).float().unsqueeze(-1) # [T, 1]

                for a in alphas:
                    key = f"L{l}_{ctrl}_a{int(a*100):02d}"

                    def make_intervention_hook(P_mat, gate_tensor, alpha_val):
                        def hook_fn(module, inp, outp):
                            if isinstance(outp, tuple):
                                h = outp[0].clone()
                                # h shape: [1, T, d]
                                delta = alpha_val * (h[0] @ P_mat) * gate_tensor.to(h.device)
                                h[0] = h[0] - delta
                                return (h,) + outp[1:]
                            else:
                                h = outp.clone()
                                delta = alpha_val * (h[0] @ P_mat) * gate_tensor.to(h.device)
                                h[0] = h[0] - delta
                                return h
                        return hook_fn

                    hook = model_layers[block_idx].register_forward_hook(make_intervention_hook(P_m, gate, a))
                    with torch.no_grad():
                        out_cell = model(input_ids=input_ids)
                        logits_cell = out_cell.logits[0, -1, :]
                        probs_cell = F.softmax(logits_cell, dim=-1)
                        pred_cell = torch.argmax(logits_cell).item()
                        logp_tgt_cell = float(torch.log(torch.clamp(probs_cell[target_id], min=1e-12)).item())
                    hook.remove()

                    grid_results[key]["correct"].append(pred_cell == target_id)
                    grid_results[key]["delta_logp"].append(logp_tgt_cell - logp_tgt_base)

        if (idx + 1) % 10 == 0 or idx == n_instances - 1:
            print(f"  Processed {idx+1}/{n_instances} instances... [Base: {sum(base_correct_list)}/{idx+1}]")

    elapsed = time.time() - start_time
    print(f"[COMPUTE] Factorial sweep completed in {elapsed:.1f}s.")

    # 4. Parameter Invariance Verification
    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "Parameter mutation detected!"
    print(f"[REPRODUCIBILITY] Post-run Parameter SHA-256 verified invariant: {post_hash}")

    # 5. Statistical Aggregation
    m_base = float(np.mean(base_correct_list))
    print("\n" + "=" * 115)
    print(f"EXP030 CONTROLLER VS. STAGE VIABILITY LANDSCAPE SCORECARD (Base Accuracy M_I = {m_base:6.4f})")
    print("=" * 115)
    print(f"{'Cell Key':<18} | {'Depth l':<8} | {'Controller':<12} | {'Alpha':<6} | {'Accuracy':<8} | {'Delta M (pp)':<14} | {'95% CI (M)':<15} | {'Delta logP':<10} | {'Viable?':<8}")
    print("-" * 115)

    landscape_output = {
        "metadata": {
            "experiment": "EXP030",
            "model_name": model_name,
            "parameter_sha256": post_hash,
            "n_instances": n_instances,
            "seed": seed,
            "baseline_accuracy": m_base
        },
        "cells": {},
        "viability_sets": {l: [] for l in layers_to_test}
    }

    for l in layers_to_test:
        for ctrl in controllers:
            for a in alphas:
                key = f"L{l}_{ctrl}_a{int(a*100):02d}"
                corr_list = grid_results[key]["correct"]
                dlp_list = grid_results[key]["delta_logp"]

                acc = float(np.mean(corr_list))
                delta_m_pp = (acc - m_base) * 100.0
                ci_m = compute_bootstrap_ci([(c - b) for c, b in zip(corr_list, base_correct_list)])
                ci_m_pp = [ci_m[0] * 100.0, ci_m[1] * 100.0]

                mean_dlp = float(np.mean(dlp_list))
                ci_dlp = compute_bootstrap_ci(dlp_list)

                # Pre-registered viability criterion: Delta M > 0 and Delta logP > 0
                is_viable = (delta_m_pp > 0.0 and mean_dlp > 0.0)
                if is_viable:
                    landscape_output["viability_sets"][l].append({
                        "controller": ctrl,
                        "alpha": a,
                        "delta_m_pp": delta_m_pp,
                        "mean_dlp": mean_dlp
                    })

                viab_str = "YES" if is_viable else "no"

                ci_str = f"[{ci_m_pp[0]:+4.1f}, {ci_m_pp[1]:+4.1f}]"
                print(f"{key:<18} | L{l:<7d} | {ctrl:<12} | {a:<6.2f} | {acc:<8.4f} | {delta_m_pp:+6.1f} pp     | {ci_str:<15} | {mean_dlp:+7.4f}    | {viab_str:<8}")

                landscape_output["cells"][key] = {
                    "layer": l,
                    "controller": ctrl,
                    "alpha": a,
                    "accuracy": acc,
                    "delta_m_pp": delta_m_pp,
                    "delta_m_ci95_pp": ci_m_pp,
                    "mean_delta_logp": mean_dlp,
                    "delta_logp_ci95": ci_dlp,
                    "is_viable": is_viable
                }

    print("=" * 115)

    # 6. Viability Landscape Synthesis Across Depths
    print("\nVIABILITY LANDSCAPE SUMMARY BY LAYER V(l):")
    for l in layers_to_test:
        v_cells = landscape_output["viability_sets"][l]
        if v_cells:
            best_cell = max(v_cells, key=lambda x: x["delta_m_pp"])
            print(f"  Layer {l:2d}: VIABLE ({len(v_cells)}/9 cells). Best: {best_cell['controller']} (alpha={best_cell['alpha']}) -> Delta M = {best_cell['delta_m_pp']:+5.1f} pp, Delta logP = {best_cell['mean_dlp']:+6.4f}")
        else:
            print(f"  Layer {l:2d}: EMPTY V(l) = 0/9 viable cells (Failure boundary across all controllers)")

    # 7. Tri-State Outcome Determination
    viable_layers = [l for l in layers_to_test if len(landscape_output["viability_sets"][l]) > 0]
    n_viable_layers = len(viable_layers)

    if n_viable_layers >= 4:
        outcome = "OUTCOME_A_BROAD_VIABILITY"
        desc = "Broad multi-layer viability confirmed across >= 4 layers under adaptive controller policies. Pure depth constraint falsified; Tri-Partite Model strongly supported."
    elif n_viable_layers <= 2:
        outcome = "OUTCOME_B_NARROW_DEPTH_PRIMACY"
        desc = "Narrow depth constraint confirmed; viable cells restricted to isolated layer region. Stage selection remains fundamental."
    else:
        outcome = "OUTCOME_C_STRUCTURED_INTERACTION"
        desc = "Structured controller-depth interaction observed across 3 intermediate layers."

    print(f"\n[TRI-STATE OUTCOME RESOLUTION]: {outcome}")
    print(f"[DESCRIPTION]: {desc}")

    landscape_output["tri_state_outcome"] = {
        "status": outcome,
        "description": desc,
        "viable_layers": viable_layers,
        "n_viable_layers": n_viable_layers
    }

    # Save to disk
    os.makedirs("experiments/runs/EXP030_landscape", exist_ok=True)
    out_path = "experiments/runs/EXP030_landscape/exp030_landscape_results.json"
    with open(out_path, "w") as f:
        json.dump(landscape_output, f, indent=2)
    print(f"\n[OUTPUT] Landscape results successfully saved to: {out_path}")

if __name__ == "__main__":
    main()
