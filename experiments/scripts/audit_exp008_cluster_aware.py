"""
EXP008 Cluster-Aware Statistical Audit Script.

Computes:
1. Per-instance ranking accuracy R_i and mean R_bar = mean(R_i).
2. Cluster bootstrap over the 35 discriminatory instances (10,000 replicates).
3. Exact within-instance label permutation test (preserving candidate counts per instance).
4. Clustered test on candidate geometry Delta_D = D(corr, inc) - D(corr, corr).
5. Explicit separation of pre-registered R_pre vs. retrospectively oriented R_post.
"""

import json
import os
import sys
import numpy as np
from scipy import stats
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scbi.core.basis import generate_candidate_subspaces, compute_subspace_distance
from experiments.benchmarks.synthetic_disentanglement import generate_benchmark_dataset, SyntheticTaskModel


def compute_effective_rank(tensor: torch.Tensor) -> float:
    try:
        _, s, _ = torch.linalg.svd(tensor, full_matrices=False)
        p = s / (torch.sum(s) + 1e-9)
        entropy = -torch.sum(p * torch.log(p + 1e-9)).item()
        return float(np.exp(entropy))
    except Exception:
        return 1.0


def compute_token_uniformity(tensor: torch.Tensor) -> float:
    normed = F.normalize(tensor, p=2, dim=-1)
    sim_matrix = torch.matmul(normed, normed.t())
    seq_len = tensor.size(0)
    mask = ~torch.eye(seq_len, dtype=torch.bool, device=tensor.device)
    return float(torch.mean(sim_matrix[mask]).item())


def run_cluster_audit(
    dataset_seed: int = 42,
    candidate_seed: int = 137,
    experiment_seed: int = 4096,
    num_samples: int = 100,
    candidate_count: int = 4,
    subspace_rank: int = 2
):
    torch.manual_seed(experiment_seed)
    np.random.seed(experiment_seed)
    
    dataset = generate_benchmark_dataset(
        num_samples=num_samples,
        seq_len=8,
        hidden_dim=32,
        num_classes=4,
        distractor_rank=subspace_rank,
        distractor_scale=1.5,
        seed=dataset_seed
    )
    model = SyntheticTaskModel(hidden_dim=32, num_classes=4)
    
    discriminatory_instances = []
    
    for i in range(num_samples):
        x_i = dataset.inputs[i:i+1]
        y_true = dataset.labels[i].item()
        
        h_0 = model.forward_prefix(x_i)
        h_s = h_0.squeeze(0)
        hp, hd = h_s[:4], h_s[4:6]
        
        cands = generate_candidate_subspaces(
            h_s,
            candidate_count=candidate_count,
            subspace_rank=subspace_rank,
            seed=candidate_seed + i
        )
        
        cand_records = []
        for k, cand in enumerate(cands):
            h_proj = cand.project(h_0)
            logits_k = model.forward_suffix(h_proj)
            pred_k = int(torch.argmax(logits_k, dim=-1).item())
            is_correct = 1 if pred_k == y_true else 0
            
            norm_orig = torch.norm(h_0, p="fro").item() + 1e-8
            retained_energy = torch.norm(h_proj, p="fro").item() / norm_orig
            removed_energy = torch.norm(h_0 - h_proj, p="fro").item() / norm_orig
            eff_rank = compute_effective_rank(h_proj.squeeze(0))
            rep_var = float(torch.var(h_proj, dim=-1).mean().item())
            token_unif = compute_token_uniformity(h_proj.squeeze(0))
            
            other_cands = [c for idx, c in enumerate(cands) if idx != k]
            mean_dist_to_peers = float(np.mean([compute_subspace_distance(cand, oc) for oc in other_cands]))
            
            # Privileged
            hp_proj = cand.project(hp)
            hd_proj = cand.project(hd)
            distractor_removed = torch.norm(hd - hd_proj, p="fro").item() / (torch.norm(hd, p="fro").item() + 1e-8)
            premise_retained = torch.norm(hp_proj, p="fro").item() / (torch.norm(hp, p="fro").item() + 1e-8)
            sdr = (torch.norm(hp_proj, p="fro").item()) / (torch.norm(hd_proj, p="fro").item() + 1e-8)
            
            correct_logit = float(logits_k[0, y_true].item())
            all_other_logits = [logits_k[0, c].item() for c in range(4) if c != y_true]
            margin_to_incorrect = correct_logit - float(max(all_other_logits))
            
            cand_records.append({
                "cand_idx": k,
                "is_correct": is_correct,
                "projector": cand,
                "features": {
                    "retained_energy": retained_energy,
                    "removed_energy": removed_energy,
                    "effective_rank": eff_rank,
                    "representation_variance": rep_var,
                    "token_uniformity": token_unif,
                    "mean_distance_to_peers": mean_dist_to_peers,
                    "distractor_energy_removed": distractor_removed,
                    "premise_energy_retained": premise_retained,
                    "signal_to_distractor_ratio": sdr,
                    "correct_logit": correct_logit,
                    "margin_to_incorrect": margin_to_incorrect
                }
            })
            
        corr_count = sum(c["is_correct"] for c in cand_records)
        if 1 <= corr_count <= 3:
            discriminatory_instances.append(cand_records)
            
    num_disc = len(discriminatory_instances)
    features = list(discriminatory_instances[0][0]["features"].keys())
    
    # Pre-registered hypothesized directions (1 if higher feature is hypothesized correct, -1 if lower)
    # e.g., retained_energy (+), removed_energy (-), effective_rank (+), representation_variance (+), token_uniformity (-), peer_distance (+)
    preregistered_directions = {
        "retained_energy": +1,
        "removed_energy": -1,
        "effective_rank": +1,
        "representation_variance": +1,
        "token_uniformity": -1,
        "mean_distance_to_peers": +1,
        "distractor_energy_removed": +1,
        "premise_energy_retained": +1,
        "signal_to_distractor_ratio": +1,
        "correct_logit": +1,
        "margin_to_incorrect": +1
    }
    
    # 1. Compute R_i for each instance i, for each feature
    # R_i = (# of correct pairs) / (total pairs in instance i)
    instance_R: dict[str, list[float]] = {f: [] for f in features}
    
    for inst in discriminatory_instances:
        correct_c = [c for c in inst if c["is_correct"] == 1]
        incorrect_c = [c for c in inst if c["is_correct"] == 0]
        n_pairs = len(correct_c) * len(incorrect_c)
        
        for f in features:
            dir_sign = preregistered_directions[f]
            corr_pairs_count = 0.0
            for c in correct_c:
                for inc in incorrect_c:
                    diff = (c["features"][f] - inc["features"][f]) * dir_sign
                    if diff > 0:
                        corr_pairs_count += 1.0
                    elif diff == 0:
                        corr_pairs_count += 0.5
            instance_R[f].append(corr_pairs_count / n_pairs)
            
    # Cluster Bootstrap over the 35 instances (10,000 replicates)
    n_replicates = 10000
    results_matrix = {}
    
    for f in features:
        r_arr = np.array(instance_R[f])
        mean_R = float(np.mean(r_arr))
        
        # Cluster bootstrap CI
        boot_means = [float(np.mean(np.random.choice(r_arr, size=num_disc, replace=True))) for _ in range(n_replicates)]
        ci_cluster = [float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))]
        
        # Exact within-instance permutation test:
        # Under H0, permute is_correct within each instance across the 4 candidates
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
            
        # Two-sided permutation p-value vs null 0.50
        obs_dev = abs(mean_R - 0.50)
        p_within_perm = float(np.mean([abs(pm - 0.50) >= obs_dev for pm in perm_means]))
        
        # Post-hoc oriented R
        post_oriented_R = mean_R if mean_R >= 0.50 else (1.0 - mean_R)
        
        results_matrix[f] = {
            "is_unsupervised": f not in ["distractor_energy_removed", "premise_energy_retained", "signal_to_distractor_ratio", "correct_logit", "margin_to_incorrect"],
            "R_pre_registered": round(mean_R, 4),
            "R_post_oriented": round(post_oriented_R, 4),
            "ci95_cluster_bootstrap": [round(ci_cluster[0], 4), round(ci_cluster[1], 4)],
            "within_instance_perm_p": round(p_within_perm, 4),
            "preregistered_direction": ("+" if preregistered_directions[f] > 0 else "-")
        }
        
    # --- Clustered Subspace Geometry Test ---
    # For instances with >= 2 correct candidates, compute Delta_D_i = mean(D(corr, inc)) - mean(D(corr, corr))
    delta_D_instances = []
    for inst in discriminatory_instances:
        correct_c = [c for c in inst if c["is_correct"] == 1]
        incorrect_c = [c for c in inst if c["is_correct"] == 0]
        if len(correct_c) >= 2:
            d_corr_corr = []
            for i1 in range(len(correct_c)):
                for i2 in range(i1 + 1, len(correct_c)):
                    d_corr_corr.append(compute_subspace_distance(correct_c[i1]["projector"], correct_c[i2]["projector"]))
            d_corr_inc = []
            for c in correct_c:
                for inc in incorrect_c:
                    d_corr_inc.append(compute_subspace_distance(c["projector"], inc["projector"]))
            delta_D_instances.append(float(np.mean(d_corr_inc) - np.mean(d_corr_corr)))
            
    delta_D_arr = np.array(delta_D_instances)
    mean_delta_D = float(np.mean(delta_D_arr))
    boot_delta_D = [float(np.mean(np.random.choice(delta_D_arr, size=len(delta_D_arr), replace=True))) for _ in range(n_replicates)]
    ci_delta_D = [float(np.percentile(boot_delta_D, 2.5)), float(np.percentile(boot_delta_D, 97.5))]
    
    # Wilcoxon signed rank test on delta_D
    try:
        w_p = float(stats.wilcoxon(delta_D_arr).pvalue)
    except Exception:
        w_p = 1.0
        
    geom_results = {
        "n_instances_with_multiple_correct": len(delta_D_instances),
        "mean_Delta_D": round(mean_delta_D, 4),
        "ci95_Delta_D_cluster": [round(ci_delta_D[0], 4), round(ci_delta_D[1], 4)],
        "wilcoxon_p": round(w_p, 4)
    }
    
    out = {
        "cluster_audited_features": results_matrix,
        "clustered_geometry_test": geom_results
    }
    
    with open("experiments/runs/EXP008_identifiability/cluster_audit_results.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=4)
        
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run_cluster_audit()
