"""
EXP007 Evaluator Diagnostic Matrix Execution Harness.

Evaluates 8 competing evaluators across the exact same frozen candidate pool:
1. V0.1 (Reconstruction + Entropy)
2. Random Selection
3. E1-oracle (Privileged Segment Mask)
4. E1-unsupervised (Variance-Segmented Mask)
5. E2 (Query-Context Geometric Alignment)
6. E3 (Downstream Logit Margin - Confidence)
7. E4 (Candidate-to-Candidate Self-Consistency under Perturbations)
8. Oracle Selection (Empirical Upper Bound)
"""

import json
import os
import sys
import time
from typing import Any, Dict, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import numpy as np
import scipy.stats as stats
import torch
import torch.nn.functional as F

from scbi.core.frozen_model import FrozenModelWrapper
from scbi.core.basis import SubspaceProjector, generate_candidate_subspaces, compute_candidate_pool_diversity
from experiments.benchmarks.synthetic_disentanglement import (
    generate_benchmark_dataset,
    SyntheticTaskModel
)


def bootstrap_ci(diffs: np.ndarray, n_boot: int = 1000, ci: float = 0.95) -> List[float]:
    if len(diffs) == 0:
        return [0.0, 0.0]
    boot_means = [float(np.mean(np.random.choice(diffs, size=len(diffs), replace=True))) for _ in range(n_boot)]
    alpha = (1.0 - ci) / 2.0
    return [float(np.percentile(boot_means, 100 * alpha)), float(np.percentile(boot_means, 100 * (1 - alpha)))]


def compute_js_divergence(probs: torch.Tensor) -> float:
    """Computes mean Jensen-Shannon divergence across J probability distributions (J, C)."""
    mean_p = torch.mean(probs, dim=0, keepdim=True)
    kl = torch.sum(probs * (torch.log(probs + 1e-9) - torch.log(mean_p + 1e-9)), dim=-1)
    return float(torch.mean(kl).item())


def run_evaluator_diagnostic(
    num_samples: int = 100,
    seq_len: int = 8,
    hidden_dim: int = 32,
    num_classes: int = 4,
    candidate_count: int = 4,
    subspace_rank: int = 2,
    dataset_seed: int = 42,
    candidate_seed: int = 137,
    experiment_seed: int = 4096,
    output_dir: str = "experiments/runs/EXP007_diagnostic"
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
    
    evaluators = ["V0.1", "Random", "E1_oracle", "E1_unsup", "E2_align", "E3_margin", "E4_self_consistency", "Oracle"]
    
    # Store instance-level binary task accuracies
    instance_accuracies: Dict[str, List[float]] = {e: [] for e in evaluators}
    
    # Store candidate-level (E_score, is_correct) pairs for global Spearman rho
    candidate_scores: Dict[str, List[float]] = {e: [] for e in evaluators if e not in ["Random", "Oracle"]}
    candidate_correctness: List[int] = []
    
    start_time = time.perf_counter()
    
    for i in range(num_samples):
        x_i = dataset.inputs[i:i+1] # (1, seq_len, hidden_dim)
        y_true = dataset.labels[i].item()
        
        # Prefix pass to get h_0
        h_0 = model.forward_prefix(x_i) # (1, seq_len, hidden_dim)
        h_s = h_0.squeeze(0) # (seq_len, hidden_dim)
        
        # Unmodified Baseline
        pred_base = int(torch.argmax(model.forward_suffix(h_0), dim=-1).item())
        
        # Generate Candidates G
        candidates = generate_candidate_subspaces(
            h_s,
            candidate_count=candidate_count,
            subspace_rank=subspace_rank,
            seed=candidate_seed + i
        )
        
        cand_task_scores = []
        cand_scores_dict: Dict[str, List[float]] = {e: [] for e in candidate_scores}
        
        for k, cand in enumerate(candidates):
            h_proj = cand.project(h_0)
            logits_k = model.forward_suffix(h_proj)
            pred_k = int(torch.argmax(logits_k, dim=-1).item())
            is_correct = 1 if pred_k == y_true else 0
            cand_task_scores.append(is_correct)
            candidate_correctness.append(is_correct)
            
            # --- 1. V0.1 ---
            norm_diff = torch.norm(h_0 - h_proj, p="fro") / (torch.norm(h_0, p="fro") + 1e-8)
            probs = F.softmax(torch.mean(torch.abs(h_proj), dim=1), dim=-1)
            entropy = -torch.sum(probs * torch.log(probs + 1e-9))
            score_v01 = norm_diff.item() + 0.1 * entropy.item()
            cand_scores_dict["V0.1"].append(score_v01)
            
            # --- 2. E1-oracle (Privileged Segment Mask) ---
            hp = h_s[:4]
            hd = h_s[4:6]
            rec_p = (torch.norm(hp - cand.project(hp), p="fro") / (torch.norm(hp, p="fro") + 1e-8)).item()
            rec_d = (torch.norm(hd - cand.project(hd), p="fro") / (torch.norm(hd, p="fro") + 1e-8)).item()
            score_e1_oracle = rec_p - 0.5 * rec_d
            cand_scores_dict["E1_oracle"].append(score_e1_oracle)
            
            # --- 3. E1-unsup (Variance-Segmented Token Mask) ---
            token_vars = torch.var(h_s, dim=-1) # (seq_len,)
            med_var = torch.median(token_vars)
            h_low_var = h_s[token_vars <= med_var]
            h_high_var = h_s[token_vars > med_var]
            rec_low = (torch.norm(h_low_var - cand.project(h_low_var), p="fro") / (torch.norm(h_low_var, p="fro") + 1e-8)).item()
            rec_high = (torch.norm(h_high_var - cand.project(h_high_var), p="fro") / (torch.norm(h_high_var, p="fro") + 1e-8)).item()
            score_e1_unsup = rec_low - 0.5 * rec_high
            cand_scores_dict["E1_unsup"].append(score_e1_unsup)
            
            # --- 4. E2 (Query-Context Alignment) ---
            h_ctx = torch.mean(h_s[:6], dim=0, keepdim=True)
            h_qry = torch.mean(h_s[6:], dim=0, keepdim=True)
            proj_ctx = cand.project(h_ctx)
            proj_qry = cand.project(h_qry)
            cos_sim = F.cosine_similarity(proj_ctx, proj_qry).item()
            score_e2 = -cos_sim
            cand_scores_dict["E2_align"].append(score_e2)
            
            # --- 5. E3 (Logit Margin - Confidence) ---
            top2_logits = torch.topk(logits_k.squeeze(0), k=2).values
            margin = (top2_logits[0] - top2_logits[1]).item()
            score_e3 = -margin
            cand_scores_dict["E3_margin"].append(score_e3)
            
            # --- 6. E4 (Candidate Self-Consistency across Perturbations) ---
            # Generate 3 independent stochastic views of h_0
            perturbed_views = [h_0 + torch.randn_like(h_0) * 0.05 for _ in range(3)]
            view_probs = [F.softmax(model.forward_suffix(cand.project(v)), dim=-1) for v in perturbed_views]
            score_e4 = compute_js_divergence(torch.cat(view_probs, dim=0))
            cand_scores_dict["E4_self_consistency"].append(score_e4)
            
        for e in candidate_scores:
            candidate_scores[e].extend(cand_scores_dict[e])
            
        # Select winner for each evaluator
        # Random
        k_rnd = int(torch.randint(0, candidate_count, (1,)).item())
        instance_accuracies["Random"].append(float(cand_task_scores[k_rnd]))
        
        # Oracle
        k_orc = int(np.argmax(cand_task_scores))
        instance_accuracies["Oracle"].append(float(cand_task_scores[k_orc]))
        
        # Evaluators (argmin of score)
        for e in candidate_scores:
            k_best = int(np.argmin(cand_scores_dict[e]))
            instance_accuracies[e].append(float(cand_task_scores[k_best]))
            
    elapsed = time.perf_counter() - start_time
    
    wrapper.verify_frozen()
    param_hash_after, buf_hash_after = wrapper.compute_hashes()
    assert param_hash_before == param_hash_after
    
    # Compute Statistics for each evaluator
    diagnostic_report: Dict[str, Any] = {}
    random_accs = np.array(instance_accuracies["Random"])
    oracle_accs = np.array(instance_accuracies["Oracle"])
    
    for e in evaluators:
        acc_arr = np.array(instance_accuracies[e])
        mean_acc = float(np.mean(acc_arr))
        regret = float(np.mean(oracle_accs - acc_arr))
        
        # Paired difference vs Random
        diff_vs_rnd = acc_arr - random_accs
        delta_rnd = float(np.mean(diff_vs_rnd))
        ci_rnd = bootstrap_ci(diff_vs_rnd)
        
        try:
            p_val = float(stats.wilcoxon(diff_vs_rnd).pvalue)
        except Exception:
            p_val = 1.0
            
        # Spearman correlation (candidate-level predictiveness)
        if e in candidate_scores:
            # We negate score because lower score is hypothesized to predict correctness=1
            neg_scores = [-s for s in candidate_scores[e]]
            rho, p_rho = stats.spearmanr(neg_scores, candidate_correctness)
            rho_val = float(rho) if not np.isnan(rho) else 0.0
            p_rho_val = float(p_rho) if not np.isnan(p_rho) else 1.0
        else:
            rho_val = 0.0
            p_rho_val = 1.0
            
        diagnostic_report[e] = {
            "mean_accuracy": round(mean_acc, 4),
            "selection_regret": round(regret, 4),
            "delta_vs_random": round(delta_rnd, 4),
            "ci95_vs_random": [round(ci_rnd[0], 4), round(ci_rnd[1], 4)],
            "wilcoxon_p_vs_random": round(p_val, 4),
            "candidate_spearman_rho": round(rho_val, 4),
            "spearman_p_value": round(p_rho_val, 4)
        }
        
    final_output = {
        "metadata": {
            "num_samples": num_samples,
            "total_candidate_evaluations": num_samples * candidate_count,
            "wall_clock_time_seconds": round(elapsed, 4),
            "checksums_match": True
        },
        "diagnostic_matrix": diagnostic_report
    }
    
    save_path = os.path.join(output_dir, "diagnostic_results.json")
    with open(save_path, "w", encoding="utf-8") as fh:
        json.dump(final_output, fh, indent=4)
        
    print("\n=== EXP007 EVALUATOR DIAGNOSTIC MATRIX COMPLETE ===")
    print(json.dumps(diagnostic_report, indent=4))
    print(f"Results saved to: {save_path}\n")
    return final_output


if __name__ == "__main__":
    run_evaluator_diagnostic()
