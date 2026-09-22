"""
EXP028b Phase A: Prospective Stage Prediction on Qwen2.5-0.5B.

Executes strict prediction-before-outcome protocol:
1. Loads model: Qwen/Qwen2.5-0.5B.
2. Audits model commit hash, tokenizer info, and computes pre-inference parameter SHA-256.
3. Evaluates prospective representation statistics across all 24 layers (0 to 23)
   using ONLY unlabeled prompt representations from N_calib = 20 calibration prompts (Seed 123).
   ZERO access to task labels or targets.
4. Computes:
   - S_representation(l) = SI_rep(l) * O_subspace(l)
   - S_intervention(l) = SI(l) / (1 + KL(l))
5. Identifies:
   - Predicted l* = argmax S_representation(l)
   - Runner-up layer
   - Margin Delta S
6. Saves immutable JSON lock file with SHA-256 checksum BEFORE Phase B confirmatory evaluation.

Governed by AGENTS.md Laws 1, 2, 4, 6, 7, 8, 9, 10, 11, 13, 14.
"""

import os
import sys
import time
import json
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

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

def construct_contrastive_subspaces(h_premise, h_distractor, rank=2):
    h_p_centered = h_premise - torch.mean(h_premise, dim=0, keepdim=True)
    _, _, Vh_p = torch.linalg.svd(h_p_centered, full_matrices=False)
    V_plus = Vh_p[:rank, :].T

    h_d_centered = h_distractor - torch.mean(h_distractor, dim=0, keepdim=True)
    _, _, Vh_d = torch.linalg.svd(h_d_centered, full_matrices=False)
    V_minus = Vh_d[:rank, :].T

    return V_plus, V_minus

def segment_tokens(offsets, text):
    p_end = text.index(" Distractor:")
    d_end = text.index(" Question:")
    prem_indices = [i for i, (s, e) in enumerate(offsets) if e <= p_end and s < e]
    dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
    quest_indices = [i for i, (s, e) in enumerate(offsets) if s >= d_end and s < e]
    return prem_indices, dist_indices, quest_indices

def main():
    print("=" * 100)
    print("EXP028b PHASE A: PROSPECTIVE STAGE PREDICTION (Qwen/Qwen2.5-0.5B)")
    print("Strict Prediction-Before-Outcome Protocol (Zero Task Labels Exposed)")
    print("=" * 100)

    model_name = "Qwen/Qwen2.5-0.5B"
    calib_seed = 123
    n_calib = 20
    rank = 2
    alpha = 0.25

    print(f"Loading model config, tokenizer, and weights for {model_name}...")
    config = AutoConfig.from_pretrained(model_name)
    commit_hash = getattr(config, "_commit_hash", "060db6499f32faf8b98477b0a26969ef7d8b9987")
    num_layers = config.num_hidden_layers
    hidden_size = config.hidden_size

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tok_commit_hash = getattr(tokenizer, "_commit_hash", "unknown")
    tok_vocab_size = len(tokenizer)

    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    print(f"Model commit hash:     {commit_hash}")
    print(f"Tokenizer vocab size:  {tok_vocab_size}")
    print(f"Parameter SHA-256:     {pre_hash}")
    print(f"Total hidden layers:   {num_layers} (hidden_size: {hidden_size})")

    # Load unlabelled calibration dataset
    full_calib_dataset = generate_bench_002_nl(n_instances=n_calib, seed=calib_seed)
    calibration_prompts = [inst["base"] for inst in full_calib_dataset]
    print(f"Generated {len(calibration_prompts)} unlabelled calibration prompts (Seed {calib_seed}).")

    candidate_layers = list(range(num_layers))
    stage_profiles = {}

    print("\nEvaluating prospective representation and intervention metrics across candidate layers...")

    for layer in candidate_layers:
        target_module = model.model.layers[layer]
        si_list = []
        ortho_list = []
        kl_list = []
        d_dist_mean_list = []
        d_prem_mean_list = []

        for prompt_text in calibration_prompts:
            enc = tokenizer(prompt_text, return_tensors="pt", return_offsets_mapping=True)
            offsets = enc["offset_mapping"][0].tolist()
            input_ids = enc["input_ids"]

            prem_idx, dist_idx, quest_idx = segment_tokens(offsets, prompt_text)
            if len(prem_idx) == 0 or len(dist_idx) == 0:
                continue

            # Base Forward Pass (No Intervention)
            with torch.no_grad():
                out_base = model(input_ids=input_ids, output_hidden_states=True)

            base_logits = out_base.logits[0, -1]
            h_l = out_base.hidden_states[layer][0]
            h_premise = h_l[prem_idx]
            h_dist = h_l[dist_idx]

            V_plus, V_minus = construct_contrastive_subspaces(h_premise, h_dist, rank=rank)

            # Metric 1a: Token Contrastive Evidence d_t
            proj_dist = torch.matmul(h_l, V_minus)
            energy_dist = torch.norm(proj_dist, dim=-1)
            proj_prem = torch.matmul(h_l, V_plus)
            energy_prem = torch.norm(proj_prem, dim=-1)
            d_tokens = energy_dist - energy_prem

            d_prem = d_tokens[prem_idx]
            d_dist = d_tokens[dist_idx]

            g_prem = float(torch.mean((d_prem > 0.0).float()).item()) if len(d_prem) > 0 else 0.0
            g_dist = float(torch.mean((d_dist > 0.0).float()).item()) if len(d_dist) > 0 else 0.0
            si = g_dist - g_prem

            si_list.append(si)
            d_dist_mean_list.append(float(torch.mean(d_dist).item()) if len(d_dist) > 0 else 0.0)
            d_prem_mean_list.append(float(torch.mean(d_prem).item()) if len(d_prem) > 0 else 0.0)

            # Metric 1b: Grassmann Subspace Orthogonality
            cross_proj = torch.matmul(V_plus.T, V_minus)
            frob_overlap = float(torch.norm(cross_proj, p="fro").item())
            ortho = 1.0 - (frob_overlap / np.sqrt(rank))
            ortho_list.append(ortho)

            # Metric 2: Pre-Outcome Intervention Diagnostic (Downstream Logit KL)
            def make_hook(V_minus_mat, V_plus_mat, alpha_val):
                def hook_fn(module, input, output):
                    h = output[0] if isinstance(output, tuple) else output
                    rest = output[1:] if isinstance(output, tuple) else None
                    h_t = h[0]

                    proj_d = torch.matmul(h_t, V_minus_mat)
                    e_d = torch.norm(proj_d, dim=-1)
                    proj_p = torch.matmul(h_t, V_plus_mat)
                    e_p = torch.norm(proj_p, dim=-1)

                    diff = e_d - e_p
                    gate = (diff > 0.0).float().unsqueeze(-1)

                    P_minus = torch.matmul(V_minus_mat, V_minus_mat.T)
                    delta_linear = - alpha_val * torch.matmul(h_t, P_minus)
                    delta_gated_raw = gate * delta_linear

                    frob_lin = torch.norm(delta_linear, p="fro")
                    frob_gat = torch.norm(delta_gated_raw, p="fro")
                    scale = frob_lin / frob_gat if frob_gat > 1e-12 else 1.0

                    h_mod = h_t + scale * delta_gated_raw
                    return (h_mod.unsqueeze(0),) + rest if rest is not None else h_mod.unsqueeze(0)
                return hook_fn

            hook = target_module.register_forward_hook(make_hook(V_minus, V_plus, alpha))
            with torch.no_grad():
                out_cand = model(input_ids=input_ids)
            hook.remove()

            cand_logits = out_cand.logits[0, -1]
            kl = compute_kl_divergence(base_logits, cand_logits)
            kl_list.append(kl)

        mean_si = float(np.mean(si_list))
        mean_ortho = float(np.mean(ortho_list))
        mean_kl = float(np.mean(kl_list))

        # Intrinsic Representation Score: S_rep(l) = SI(l) * Ortho(l)
        s_rep = float(max(0.0, mean_si) * max(0.0, mean_ortho))

        # Pre-Outcome Intervention Diagnostic: S_interv(l) = SI(l) / (1 + KL(l))
        s_interv = float(mean_si / (1.0 + mean_kl))

        norm_depth = float(layer) / float(num_layers)

        stage_profiles[str(layer)] = {
            "layer": layer,
            "normalized_depth": norm_depth,
            "S_representation": s_rep,
            "S_intervention": s_interv,
            "selectivity_index": mean_si,
            "subspace_orthogonality": mean_ortho,
            "kl_divergence": mean_kl,
            "mean_d_dist": float(np.mean(d_dist_mean_list)),
            "mean_d_prem": float(np.mean(d_prem_mean_list))
        }

        print(f"Layer {layer:2d} (lambda={norm_depth:.3f}): S_rep={s_rep:.4f} | S_interv={s_interv:.4f} | SI={mean_si:.4f} | Ortho={mean_ortho:.4f} | KL={mean_kl:.4f}")

    # Rank candidate layers by prospective representation score S_representation
    sorted_by_s_rep = sorted(stage_profiles.values(), key=lambda x: x["S_representation"], reverse=True)
    predicted_l_star = sorted_by_s_rep[0]["layer"]
    runner_up_layer = sorted_by_s_rep[1]["layer"]
    margin = sorted_by_s_rep[0]["S_representation"] - sorted_by_s_rep[1]["S_representation"]

    # Also record rank by intervention diagnostic
    sorted_by_s_interv = sorted(stage_profiles.values(), key=lambda x: x["S_intervention"], reverse=True)
    interv_top_l = sorted_by_s_interv[0]["layer"]

    post_hash = get_param_hash(model)
    assert pre_hash == post_hash, "Backbone parameters corrupted during prediction!"

    lock_record = {
        "metadata": {
            "experiment": "EXP028b",
            "phase": "Phase A (Stage Prediction)",
            "model_name": model_name,
            "model_commit_hash": commit_hash,
            "tokenizer_commit_hash": tok_commit_hash,
            "tokenizer_vocab_size": tok_vocab_size,
            "parameter_sha256": pre_hash,
            "parameter_invariant": (pre_hash == post_hash),
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "calibration_seed": calib_seed,
            "calibration_instances_count": n_calib,
            "predeclared_baseline_layer": 16,
            "predeclared_baseline_norm_depth": 16.0 / num_layers
        },
        "locked_prediction": {
            "primary_predicted_layer_l_star": predicted_l_star,
            "primary_predicted_norm_depth": float(predicted_l_star) / float(num_layers),
            "primary_metric": "S_representation = SI_rep * Ortho",
            "score_l_star": sorted_by_s_rep[0]["S_representation"],
            "runner_up_layer": runner_up_layer,
            "runner_up_score": sorted_by_s_rep[1]["S_representation"],
            "first_to_second_margin": margin,
            "pre_outcome_intervention_top_layer": interv_top_l,
            "pre_outcome_intervention_score": sorted_by_s_interv[0]["S_intervention"]
        },
        "all_layer_profiles": stage_profiles,
        "calibration_prompts": calibration_prompts
    }

    os.makedirs("experiments/runs/EXP028b_qwen", exist_ok=True)
    lock_file = "experiments/runs/EXP028b_qwen/exp028b_prediction_lock.json"

    # Compute hash of the formatted JSON string to seal it
    json_str = json.dumps(lock_record, indent=2)
    record_hash = hashlib.sha256(json_str.encode("utf-8")).hexdigest()
    lock_record["lock_checksum_sha256"] = record_hash

    with open(lock_file, "w") as f:
        json.dump(lock_record, f, indent=2)

    print("\n" + "=" * 100)
    print("EXP028b PROSPECTIVE PREDICTION LOCKED AND SEALED:")
    print("=" * 100)
    print(f"Model:                          {model_name} (Commit: {commit_hash[:10]}...)")
    print(f"Parameter SHA-256:              {pre_hash}")
    print(f"LOCKED PROSPECTIVE LAYER (l*):  LAYER {predicted_l_star} (lambda = {predicted_l_star / num_layers:.3f})")
    print(f"S_representation(l*):           {sorted_by_s_rep[0]['S_representation']:.4f}")
    print(f"RUNNER-UP LAYER:                LAYER {runner_up_layer} (lambda = {runner_up_layer / num_layers:.3f})")
    print(f"Runner-up Score:                {sorted_by_s_rep[1]['S_representation']:.4f}")
    print(f"First-to-Second Margin:         {margin:.4f}")
    print(f"Intervention Diagnostic Top:    LAYER {interv_top_l} (S_interv = {sorted_by_s_interv[0]['S_intervention']:.4f})")
    print(f"Pre-Declared Baseline:          LAYER 16 (lambda = {16.0 / num_layers:.3f})")
    print(f"Lock File Path:                 {lock_file}")
    print(f"Lock File Checksum (SHA-256):   {record_hash}")
    print("=" * 100)

if __name__ == "__main__":
    main()
