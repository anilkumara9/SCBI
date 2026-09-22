"""
EXP008: Candidate Mechanism Decomposition & Identifiability Study.

Tests Hypothesis H8: Whether correct and incorrect candidates within discriminatory
instances possess measurable, information-valid differences in pre-selection statistics.
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


def compute_effective_rank(tensor: torch.Tensor) -> float:
    """Computes exponential of spectral entropy: exp(-sum p_j ln p_j)."""
    # tensor is (seq_len, hidden_dim)
    try:
        _, s, _ = torch.linalg.svd(tensor, full_matrices=False)
        p = s / (torch.sum(s) + 1e-9)
        entropy = -torch.sum(p * torch.log(p + 1e-9)).item()
        return float(np.exp(entropy))
    except Exception:
        return 1.0


def compute_token_uniformity(tensor: torch.Tensor) -> float:
    """Mean pairwise cosine similarity across tokens."""
    # (seq_len, hidden_dim)
    normed = F.normalize(tensor, p=2, dim=-1)
    sim_matrix = torch.matmul(normed, normed.t())
    seq_len = tensor.size(0)
    # Exclude diagonal
    mask = ~torch.eye(seq_len, dtype=torch.bool, device=tensor.device)
    return float(torch.mean(sim_matrix[mask]).item())


def permutation_test_pairwise(diffs: np.ndarray, n_permutations: int = 2000) -> float:
    """
    Tests whether the pairwise differences D = f(correct) - f(incorrect)
    have a mean significantly different from 0 under random sign flips (null R = 0.5).
    """
    observed_t = np.mean(diffs)
    if len(diffs) == 0:
        return 1.0
    abs_observed = abs(observed_t)
    
    count = 0
    for _ in range(n_permutations):
        signs = np.random.choice([-1.0, 1.0], size=len(diffs))
        perm_mean = np.mean(diffs * signs)
        if abs(perm_mean) >= abs_observed:
            count += 1
    return float(count / n_permutations)


def run_exp008_identifiability(
    num_samples: int = 100,
    seq_len: int = 8,
    hidden_dim: int = 32,
    num_classes: int = 4,
    candidate_count: int = 4,
    subspace_rank: int = 2,
    dataset_seed: int = 42,
    candidate_seed: int = 137,
    experiment_seed: int = 4096,
    output_dir: str = "experiments/runs/EXP008_identifiability"
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
    
    # Store candidates and features across all instances
    all_instances_data = []
    discriminatory_instances = []
    
    start_time = time.perf_counter()
    
    for i in range(num_samples):
        x_i = dataset.inputs[i:i+1]
        y_true = dataset.labels[i].item()
        
        h_0 = model.forward_prefix(x_i) # (1, seq_len, hidden_dim)
        h_s = h_0.squeeze(0) # (seq_len, hidden_dim)
        
        # Ground truth token slices
        hp = h_s[:4] # Premise tokens
        hd = h_s[4:6] # Distractor tokens
        hq = h_s[6:] # Query tokens
        
        cands = generate_candidate_subspaces(
            h_s,
            candidate_count=candidate_count,
            subspace_rank=subspace_rank,
            seed=candidate_seed + i
        )
        
        instance_record = {
            "instance_idx": i,
            "y_true": y_true,
            "candidates": []
        }
        
        for k, cand in enumerate(cands):
            h_proj = cand.project(h_0)
            logits_k = model.forward_suffix(h_proj)
            pred_k = int(torch.argmax(logits_k, dim=-1).item())
            is_correct = 1 if pred_k == y_true else 0
            
            # --- Pre-Selection Representation Statistics (Label-Free / Unsupervised) ---
            norm_orig = torch.norm(h_0, p="fro").item() + 1e-8
            retained_energy = torch.norm(h_proj, p="fro").item() / norm_orig
            removed_energy = torch.norm(h_0 - h_proj, p="fro").item() / norm_orig
            eff_rank = compute_effective_rank(h_proj.squeeze(0))
            rep_var = float(torch.var(h_proj, dim=-1).mean().item())
            token_unif = compute_token_uniformity(h_proj.squeeze(0))
            
            # Subspace distance to other candidates in pool
            other_cands = [c for idx, c in enumerate(cands) if idx != k]
            mean_dist_to_peers = float(np.mean([compute_subspace_distance(cand, oc) for oc in other_cands]))
            
            # --- Privileged Diagnostic Features (Benchmark Ground-Truth) ---
            hp_proj = cand.project(hp)
            hd_proj = cand.project(hd)
            distractor_removed = torch.norm(hd - hd_proj, p="fro").item() / (torch.norm(hd, p="fro").item() + 1e-8)
            premise_retained = torch.norm(hp_proj, p="fro").item() / (torch.norm(hp, p="fro").item() + 1e-8)
            sdr = (torch.norm(hp_proj, p="fro").item()) / (torch.norm(hd_proj, p="fro").item() + 1e-8)
            
            correct_logit = float(logits_k[0, y_true].item())
            all_other_logits = [logits_k[0, c].item() for c in range(num_classes) if c != y_true]
            max_incorrect_logit = float(max(all_other_logits))
            margin_to_incorrect = correct_logit - max_incorrect_logit
            
            cand_features = {
                "cand_idx": k,
                "is_correct": is_correct,
                "projector": cand,
                # Unsupervised
                "retained_energy": retained_energy,
                "removed_energy": removed_energy,
                "effective_rank": eff_rank,
                "representation_variance": rep_var,
                "token_uniformity": token_unif,
                "mean_distance_to_peers": mean_dist_to_peers,
                # Privileged Diagnostic
                "distractor_energy_removed": distractor_removed,
                "premise_energy_retained": premise_retained,
                "signal_to_distractor_ratio": sdr,
                "correct_logit": correct_logit,
                "margin_to_incorrect": margin_to_incorrect
            }
            instance_record["candidates"].append(cand_features)
            
        all_instances_data.append(instance_record)
        
        correct_count = sum(c["is_correct"] for c in instance_record["candidates"])
        if 1 <= correct_count <= (candidate_count - 1):
            discriminatory_instances.append(instance_record)
            
    elapsed = time.perf_counter() - start_time
    
    wrapper.verify_frozen()
    param_hash_after, buf_hash_after = wrapper.compute_hashes()
    assert param_hash_before == param_hash_after
    
    # Analyze Within-Instance Feature Predictiveness on Discriminatory Instances
    unsupervised_features = [
        "retained_energy",
        "removed_energy",
        "effective_rank",
        "representation_variance",
        "token_uniformity",
        "mean_distance_to_peers"
    ]
    
    privileged_features = [
        "distractor_energy_removed",
        "premise_energy_retained",
        "signal_to_distractor_ratio",
        "correct_logit",
        "margin_to_incorrect"
    ]
    
    all_features = unsupervised_features + privileged_features
    feature_evaluations: Dict[str, Any] = {}
    
    # Extract pairwise comparisons
    pairwise_diffs: Dict[str, List[float]] = {f: [] for f in all_features}
    pairwise_ranking_acc: Dict[str, List[float]] = {f: [] for f in all_features}
    
    for inst in discriminatory_instances:
        correct_cands = [c for c in inst["candidates"] if c["is_correct"] == 1]
        incorrect_cands = [c for c in inst["candidates"] if c["is_correct"] == 0]
        
        for c in correct_cands:
            for inc in incorrect_cands:
                for f in all_features:
                    val_c = c[f]
                    val_inc = inc[f]
                    diff = val_c - val_inc
                    pairwise_diffs[f].append(diff)
                    
                    # Higher is hypothesized to be correct
                    if diff > 0:
                        pairwise_ranking_acc[f].append(1.0)
                    elif diff == 0:
                        pairwise_ranking_acc[f].append(0.5)
                    else:
                        pairwise_ranking_acc[f].append(0.0)
                        
    num_pairs = len(pairwise_diffs["retained_energy"])
    
    for f in all_features:
        diff_arr = np.array(pairwise_diffs[f])
        rank_acc_arr = np.array(pairwise_ranking_acc[f])
        
        mean_r = float(np.mean(rank_acc_arr))
        # If mean_r < 0.5, check if lower value indicates correctness
        # We report both raw R and oriented R (max(R, 1-R))
        oriented_r = mean_r if mean_r >= 0.5 else (1.0 - mean_r)
        
        # Permutation p-value
        perm_p = permutation_test_pairwise(diff_arr, n_permutations=2000)
        
        # Within-instance effect size (Cohen's d_z)
        mean_diff = float(np.mean(diff_arr))
        std_diff = float(np.std(diff_arr, ddof=1)) + 1e-8
        cohens_dz = float(mean_diff / std_diff)
        
        # Bootstrap CI for pairwise accuracy
        boot_rs = [float(np.mean(np.random.choice(rank_acc_arr, size=num_pairs, replace=True))) for _ in range(1000)]
        ci95 = [float(np.percentile(boot_rs, 2.5)), float(np.percentile(boot_rs, 97.5))]
        
        feature_evaluations[f] = {
            "is_unsupervised": (f in unsupervised_features),
            "pairwise_ranking_accuracy_R": round(mean_r, 4),
            "oriented_ranking_accuracy": round(oriented_r, 4),
            "ci95_R": [round(ci95[0], 4), round(ci95[1], 4)],
            "permutation_p_value": round(perm_p, 4),
            "within_instance_effect_size_dz": round(cohens_dz, 4),
            "mean_pairwise_diff": round(mean_diff, 4)
        }
        
    # --- Candidate Geometry Analysis ---
    # Compare within-instance subspace distances:
    # 1. D(correct, correct) when >= 2 correct candidates exist
    # 2. D(correct, incorrect)
    # 3. D(incorrect, incorrect) when >= 2 incorrect candidates exist
    d_c_c = []
    d_c_inc = []
    d_inc_inc = []
    
    for inst in discriminatory_instances:
        correct_cands = [c for c in inst["candidates"] if c["is_correct"] == 1]
        incorrect_cands = [c for c in inst["candidates"] if c["is_correct"] == 0]
        
        # D(correct, incorrect)
        for c in correct_cands:
            for inc in incorrect_cands:
                d_c_inc.append(compute_subspace_distance(c["projector"], inc["projector"]))
                
        # D(correct, correct)
        if len(correct_cands) >= 2:
            for i1 in range(len(correct_cands)):
                for i2 in range(i1 + 1, len(correct_cands)):
                    d_c_c.append(compute_subspace_distance(correct_cands[i1]["projector"], correct_cands[i2]["projector"]))
                    
        # D(incorrect, incorrect)
        if len(incorrect_cands) >= 2:
            for i1 in range(len(incorrect_cands)):
                for i2 in range(i1 + 1, len(incorrect_cands)):
                    d_inc_inc.append(compute_subspace_distance(incorrect_cands[i1]["projector"], incorrect_cands[i2]["projector"]))
                    
    geometry_analysis = {
        "mean_dist_correct_to_correct": round(float(np.mean(d_c_c)), 4) if len(d_c_c) > 0 else None,
        "mean_dist_correct_to_incorrect": round(float(np.mean(d_c_inc)), 4) if len(d_c_inc) > 0 else None,
        "mean_dist_incorrect_to_incorrect": round(float(np.mean(d_inc_inc)), 4) if len(d_inc_inc) > 0 else None,
        "n_pairs_correct_correct": len(d_c_c),
        "n_pairs_correct_incorrect": len(d_c_inc),
        "n_pairs_incorrect_incorrect": len(d_inc_inc)
    }
    
    final_output = {
        "metadata": {
            "experiment_id": "EXP008",
            "num_samples": num_samples,
            "num_discriminatory_instances": len(discriminatory_instances),
            "num_pairwise_comparisons": num_pairs,
            "wall_clock_time_seconds": round(elapsed, 4),
            "checksums_match": True
        },
        "feature_identifiability_matrix": feature_evaluations,
        "subspace_geometry_analysis": geometry_analysis
    }
    
    save_path = os.path.join(output_dir, "identifiability_results.json")
    with open(save_path, "w", encoding="utf-8") as fh:
        json.dump(final_output, fh, indent=4)
        
    print("\n=== EXP008 CANDIDATE IDENTIFIABILITY STUDY COMPLETE ===")
    print(f"Discriminatory instances: {len(discriminatory_instances)} | Pairs: {num_pairs}")
    print("\nFeature Identifiability Matrix:")
    for f, res in feature_evaluations.items():
        status = "[UNSUPERVISED]" if res["is_unsupervised"] else "[PRIVILEGED]"
        print(f"{status:15} {f:30}: R = {res['pairwise_ranking_accuracy_R']:.4f} (p = {res['permutation_p_value']:.4f}, dz = {res['within_instance_effect_size_dz']:.4f})")
    print(f"\nSubspace Geometry Analysis:\n{json.dumps(geometry_analysis, indent=4)}")
    print(f"Results saved to: {save_path}\n")
    return final_output


if __name__ == "__main__":
    run_exp008_identifiability()
