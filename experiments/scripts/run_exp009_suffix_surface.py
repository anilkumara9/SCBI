"""
EXP009: Suffix Response Surface & Information Localization Execution Harness.

Tests:
1. Label-free output-distribution statistics Z across candidate pool.
2. Layer-wise information localization (Layer l -> Layer l+1 -> Layer l+2 -> Output q).
3. Diagnostic Information Classifier Test with Leave-One-Instance-Out (LOIO) Cross-Validation.
4. Cluster-aware bootstrapping and within-instance permutation tests.
"""

import json
import os
import sys
import time
from typing import Any, Dict, List, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import numpy as np
import scipy.stats as stats
import torch
import torch.nn.functional as F

from scbi.core.frozen_model import FrozenModelWrapper
from scbi.core.basis import SubspaceProjector, generate_candidate_subspaces, compute_subspace_distance
from experiments.benchmarks.synthetic_disentanglement import (
    generate_benchmark_dataset,
    SyntheticTaskModel
)


def compute_js_divergence_pair(p: torch.Tensor, q: torch.Tensor) -> float:
    """JS divergence between two categorical distributions (C,)."""
    m = 0.5 * (p + q)
    kl_p = torch.sum(p * (torch.log(p + 1e-9) - torch.log(m + 1e-9)))
    kl_q = torch.sum(q * (torch.log(q + 1e-9) - torch.log(m + 1e-9)))
    return float(0.5 * (kl_p + kl_q).item())


def run_exp009_suffix_diagnostic(
    num_samples: int = 100,
    seq_len: int = 8,
    hidden_dim: int = 32,
    num_classes: int = 4,
    candidate_count: int = 4,
    subspace_rank: int = 2,
    dataset_seed: int = 42,
    candidate_seed: int = 137,
    experiment_seed: int = 4096,
    output_dir: str = "experiments/runs/EXP009_suffix_surface"
) -> Dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)
    
    torch.manual_seed(experiment_seed)
    np.random.seed(experiment_seed)
    
    dataset = generate_benchmark_dataset(
        num_samples=num_samples,
        seq_len=seq_len,
        hidden_dim=hidden_dim,
        num_classes=num_classes,
        distractor_rank=subspace_rank,
        distractor_scale=1.5,
        seed=dataset_seed
    )
    
    model = SyntheticTaskModel(hidden_dim=hidden_dim, num_classes=num_classes)
    wrapper = FrozenModelWrapper(model)
    param_hash_before, buf_hash_before = wrapper.compute_hashes()
    
    discriminatory_instances = []
    start_time = time.perf_counter()
    
    for i in range(num_samples):
        x_i = dataset.inputs[i:i+1]
        y_true = dataset.labels[i].item()
        
        h_0 = model.forward_prefix(x_i)
        h_s = h_0.squeeze(0)
        
        cands = generate_candidate_subspaces(
            h_s,
            candidate_count=candidate_count,
            subspace_rank=subspace_rank,
            seed=candidate_seed + i
        )
        
        # Precompute projected forward trajectories
        cand_outputs = []
        for k, cand in enumerate(cands):
            h_proj = cand.project(h_0) # (1, seq_len, hidden_dim)
            pooled_0 = torch.mean(h_proj, dim=-2) # (1, hidden_dim) - Layer l
            
            # Sub-layers of suffix
            # layer_suffix[0]: Linear(32, 32)
            # layer_suffix[1]: LayerNorm(32)
            # layer_suffix[2]: GELU()
            # layer_suffix[3]: Linear(32, 4)
            h_l1 = model.layer_suffix[2](model.layer_suffix[1](model.layer_suffix[0](pooled_0))) # Layer l+1
            logits = model.layer_suffix[3](h_l1) # Layer l+2
            probs = F.softmax(logits, dim=-1).squeeze(0) # Output q
            
            pred_k = int(torch.argmax(logits, dim=-1).item())
            is_correct = 1 if pred_k == y_true else 0
            
            cand_outputs.append({
                "cand_idx": k,
                "is_correct": is_correct,
                "h_proj": h_proj,
                "pooled_l0": pooled_0.squeeze(0),
                "h_l1": h_l1.squeeze(0),
                "logits": logits.squeeze(0),
                "probs": probs,
                "projector": cand
            })
            
        corr_count = sum(c["is_correct"] for c in cand_outputs)
        if 1 <= corr_count <= (candidate_count - 1):
            # Compute ensemble probability distribution across the 4 candidates
            all_probs = torch.stack([c["probs"] for c in cand_outputs], dim=0) # (4, C)
            mean_ensemble_prob = torch.mean(all_probs, dim=0) # (C,)
            
            instance_cands = []
            for k, c in enumerate(cand_outputs):
                probs_k = c["probs"]
                logits_k = c["logits"]
                
                # Suffix Output Features Z
                entropy_q = -torch.sum(probs_k * torch.log(probs_k + 1e-9)).item()
                top2_q = torch.topk(probs_k, k=2).values
                margin_q = (top2_q[0] - top2_q[1]).item()
                logit_norm = torch.norm(logits_k, p=2).item()
                logit_var = torch.var(logits_k).item()
                
                # Consensus features
                js_to_ensemble = compute_js_divergence_pair(probs_k, mean_ensemble_prob)
                peer_js_list = [compute_js_divergence_pair(probs_k, cand_outputs[j]["probs"]) for j in range(candidate_count) if j != k]
                mean_peer_js = float(np.mean(peer_js_list))
                
                # View consistency (output curvature)
                # Apply small perturbations at h_0, pass through suffix, measure JS divergence
                views = [c["h_proj"] + torch.randn_like(c["h_proj"]) * 0.05 for _ in range(3)]
                vprobs = [F.softmax(model.forward_suffix(v), dim=-1).squeeze(0) for v in views]
                curvatures = [compute_js_divergence_pair(probs_k, vp) for vp in vprobs]
                view_curvature = float(np.mean(curvatures))
                
                # Intermediate features X
                norm_orig = torch.norm(h_0, p="fro").item() + 1e-8
                retained_energy = torch.norm(c["h_proj"], p="fro").item() / norm_orig
                removed_energy = torch.norm(h_0 - c["h_proj"], p="fro").item() / norm_orig
                rep_var = float(torch.var(c["h_proj"], dim=-1).mean().item())
                
                # Layer-wise norms and variances
                norm_l0 = torch.norm(c["pooled_l0"], p=2).item()
                norm_l1 = torch.norm(c["h_l1"], p=2).item()
                var_l0 = torch.var(c["pooled_l0"]).item()
                var_l1 = torch.var(c["h_l1"]).item()
                
                features = {
                    # Suffix Output Features Z
                    "suffix_entropy": entropy_q,
                    "suffix_prob_margin": margin_q,
                    "suffix_logit_norm": logit_norm,
                    "suffix_logit_variance": logit_var,
                    "suffix_js_to_ensemble": js_to_ensemble,
                    "suffix_mean_peer_js": mean_peer_js,
                    "suffix_view_curvature": view_curvature,
                    # Layer-wise representations
                    "norm_layer_l0": norm_l0,
                    "norm_layer_l1": norm_l1,
                    "var_layer_l0": var_l0,
                    "var_layer_l1": var_l1,
                    # Intermediate features X
                    "retained_energy": retained_energy,
                    "removed_energy": removed_energy,
                    "representation_variance": rep_var
                }
                
                instance_cands.append({
                    "cand_idx": k,
                    "is_correct": c["is_correct"],
                    "features": features
                })
                
            discriminatory_instances.append(instance_cands)
            
    elapsed = time.perf_counter() - start_time
    wrapper.verify_frozen()
    param_hash_after, buf_hash_after = wrapper.compute_hashes()
    assert param_hash_before == param_hash_after
    
    num_disc = len(discriminatory_instances)
    feature_names = list(discriminatory_instances[0][0]["features"].keys())
    
    # Pre-registered hypothesized directions
    # e.g., entropy (-), margin (+), logit_norm (+), consensus js (-), curvature (-)
    preregistered_directions = {
        "suffix_entropy": -1,
        "suffix_prob_margin": +1,
        "suffix_logit_norm": +1,
        "suffix_logit_variance": +1,
        "suffix_js_to_ensemble": -1,
        "suffix_mean_peer_js": -1,
        "suffix_view_curvature": -1,
        "norm_layer_l0": +1,
        "norm_layer_l1": +1,
        "var_layer_l0": +1,
        "var_layer_l1": +1,
        "retained_energy": +1,
        "removed_energy": -1,
        "representation_variance": +1
    }
    
    # 1. Cluster-Aware Per-Instance Ranking R_i
    instance_R = {f: [] for f in feature_names}
    for inst in discriminatory_instances:
        correct_c = [c for c in inst if c["is_correct"] == 1]
        incorrect_c = [c for c in inst if c["is_correct"] == 0]
        n_pairs = len(correct_c) * len(incorrect_c)
        
        for f in feature_names:
            dir_sign = preregistered_directions[f]
            c_count = 0.0
            for c in correct_c:
                for inc in incorrect_c:
                    diff = (c["features"][f] - inc["features"][f]) * dir_sign
                    if diff > 0:
                        c_count += 1.0
                    elif diff == 0:
                        c_count += 0.5
            instance_R[f].append(c_count / n_pairs)
            
    # Cluster bootstrap (10,000 replicates) & within-instance permutations
    n_replicates = 5000
    feature_report = {}
    
    for f in feature_names:
        r_arr = np.array(instance_R[f])
        mean_R = float(np.mean(r_arr))
        
        boot_means = [float(np.mean(np.random.choice(r_arr, size=num_disc, replace=True))) for _ in range(n_replicates)]
        ci_cluster = [float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))]
        
        perm_means = []
        for _ in range(n_replicates):
            perm_r_inst = []
            for inst in discriminatory_instances:
                observed_correct = [c["is_correct"] for c in inst]
                perm_labels = np.random.permutation(observed_correct)
                c_cands = [inst[idx] for idx, lab in enumerate(perm_labels) if lab == 1]
                inc_cands = [inst[idx] for idx, lab in enumerate(perm_labels) if lab == 0]
                n_p = len(c_cands) * len(inc_cands)
                
                dir_sign = preregistered_directions[f]
                c_count = 0.0
                for c in c_cands:
                    for inc in inc_cands:
                        diff = (c["features"][f] - inc["features"][f]) * dir_sign
                        if diff > 0:
                            c_count += 1.0
                        elif diff == 0:
                            c_count += 0.5
                perm_r_inst.append(c_count / n_p)
            perm_means.append(float(np.mean(perm_r_inst)))
            
        obs_dev = abs(mean_R - 0.50)
        p_within_perm = float(np.mean([abs(pm - 0.50) >= obs_dev for pm in perm_means]))
        
        feature_report[f] = {
            "mean_R_instance": round(mean_R, 4),
            "ci95_cluster_bootstrap": [round(ci_cluster[0], 4), round(ci_cluster[1], 4)],
            "within_instance_perm_p": round(p_within_perm, 4),
            "direction": ("+" if preregistered_directions[f] > 0 else "-")
        }
        
    # 2. Diagnostic Information Classifier Test (Leave-One-Instance-Out Cross-Validation)
    # Prepare datasets
    X_intermediate_keys = ["retained_energy", "removed_energy", "representation_variance"]
    Z_suffix_keys = ["suffix_entropy", "suffix_prob_margin", "suffix_logit_norm", "suffix_logit_variance", "suffix_js_to_ensemble", "suffix_mean_peer_js", "suffix_view_curvature"]
    All_keys = X_intermediate_keys + Z_suffix_keys
    
    def evaluate_loio_classifier(keys_subset: List[str]) -> Tuple[float, List[float]]:
        oof_instance_R = []
        for test_idx in range(num_disc):
            # Train set = all instances except test_idx
            train_X, train_Y = [], []
            for idx in range(num_disc):
                if idx == test_idx:
                    continue
                for c in discriminatory_instances[idx]:
                    train_X.append([c["features"][k] for k in keys_subset])
                    train_Y.append(c["is_correct"])
                    
            train_X = np.array(train_X)
            train_Y = np.array(train_Y)
            
            # Standardize
            mu = np.mean(train_X, axis=0, keepdims=True)
            sigma = np.std(train_X, axis=0, keepdims=True) + 1e-8
            train_X_norm = (train_X - mu) / sigma
            
            # Simple Ridge Logistic Regression / Linear Discriminant
            # W = (X^T X + lambda I)^-1 X^T Y
            X_b = np.column_stack([train_X_norm, np.ones(len(train_X_norm))])
            reg = 1.0 * np.eye(X_b.shape[1])
            reg[-1, -1] = 0.0 # Don't regularize bias
            w = np.linalg.solve(X_b.T @ X_b + reg, X_b.T @ (train_Y - 0.5))
            
            # Predict on test instance
            test_inst = discriminatory_instances[test_idx]
            test_cands_X = np.array([[c["features"][k] for k in keys_subset] for c in test_inst])
            test_cands_X_norm = (test_cands_X - mu) / sigma
            test_X_b = np.column_stack([test_cands_X_norm, np.ones(len(test_cands_X_norm))])
            scores = test_X_b @ w
            
            correct_c = [idx for idx, c in enumerate(test_inst) if c["is_correct"] == 1]
            incorrect_c = [idx for idx, c in enumerate(test_inst) if c["is_correct"] == 0]
            n_p = len(correct_c) * len(incorrect_c)
            
            c_cnt = 0.0
            for ci in correct_c:
                for inc_i in incorrect_c:
                    if scores[ci] > scores[inc_i]:
                        c_cnt += 1.0
                    elif scores[ci] == scores[inc_i]:
                        c_cnt += 0.5
            oof_instance_R.append(c_cnt / n_p)
            
        r_oof = float(np.mean(oof_instance_R))
        boot_oof = [float(np.mean(np.random.choice(oof_instance_R, size=num_disc, replace=True))) for _ in range(2000)]
        ci_oof = [float(np.percentile(boot_oof, 2.5)), float(np.percentile(boot_oof, 97.5))]
        return round(r_oof, 4), [round(ci_oof[0], 4), round(ci_oof[1], 4)]
        
    r_oof_x, ci_oof_x = evaluate_loio_classifier(X_intermediate_keys)
    r_oof_z, ci_oof_z = evaluate_loio_classifier(Z_suffix_keys)
    r_oof_all, ci_oof_all = evaluate_loio_classifier(All_keys)
    
    loio_results = {
        "model_X_intermediate_only": {
            "features": X_intermediate_keys,
            "out_of_fold_ranking_R": r_oof_x,
            "ci95_cluster_bootstrap": ci_oof_x
        },
        "model_Z_suffix_output_only": {
            "features": Z_suffix_keys,
            "out_of_fold_ranking_R": r_oof_z,
            "ci95_cluster_bootstrap": ci_oof_z
        },
        "model_combined_X_and_Z": {
            "features": All_keys,
            "out_of_fold_ranking_R": r_oof_all,
            "ci95_cluster_bootstrap": ci_oof_all
        }
    }
    
    final_output = {
        "metadata": {
            "experiment_id": "EXP009",
            "num_samples": num_samples,
            "num_discriminatory_instances": num_disc,
            "wall_clock_time_seconds": round(elapsed, 4),
            "checksums_match": True
        },
        "suffix_response_surface_features": feature_report,
        "diagnostic_information_classifier_loio": loio_results
    }
    
    save_path = os.path.join(output_dir, "suffix_diagnostic_results.json")
    with open(save_path, "w", encoding="utf-8") as fh:
        json.dump(final_output, fh, indent=4)
        
    print("\n=== EXP009 SUFFIX RESPONSE SURFACE COMPLETE ===")
    print(json.dumps(final_output, indent=2))
    return final_output


if __name__ == "__main__":
    run_exp009_suffix_diagnostic()
