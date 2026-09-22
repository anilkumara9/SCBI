"""
Automated Execution Harness for EXP001–EXP006.

Executes:
- EXP001: Frozen Baseline
- EXP002: Fixed Projection
- EXP003: Random Selection
- EXP004: SCBI Evaluator Selection (IASP)
- EXP005: Oracle Selection & Selection Regret
- EXP006: Evaluator Predictiveness Analysis
"""

import json
import os
import sys
import time
from typing import Any, Dict, List

# Ensure workspace root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import numpy as np
import scipy.stats as stats
import torch

from scbi.core.frozen_model import FrozenModelWrapper
from scbi.core.basis import SubspaceProjector, generate_candidate_subspaces, compute_candidate_pool_diversity
from scbi.core.engine import SCBIEngine
from scbi.baselines.matched_baseline import ComputeMatchedBaseline
from experiments.benchmarks.synthetic_disentanglement import (
    generate_benchmark_dataset,
    SyntheticTaskModel
)


def bootstrap_ci(diffs: np.ndarray, n_boot: int = 1000, ci: float = 0.95) -> List[float]:
    """Computes 95% bootstrap confidence interval."""
    if len(diffs) == 0:
        return [0.0, 0.0]
    boot_means = [float(np.mean(np.random.choice(diffs, size=len(diffs), replace=True))) for _ in range(n_boot)]
    alpha = (1.0 - ci) / 2.0
    return [float(np.percentile(boot_means, 100 * alpha)), float(np.percentile(boot_means, 100 * (1 - alpha)))]


def run_experiment_suite(
    num_samples: int = 100,
    seq_len: int = 8,
    hidden_dim: int = 32,
    num_classes: int = 4,
    candidate_count: int = 4,
    subspace_rank: int = 2,
    lambda_entropy: float = 0.1,
    dataset_seed: int = 42,
    candidate_seed: int = 137,
    experiment_seed: int = 4096,
    output_dir: str = "experiments/runs/EXP001_to_EXP006"
) -> Dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Deterministic seeding
    torch.manual_seed(experiment_seed)
    np.random.seed(experiment_seed)
    
    # 2. Benchmark data generation
    dataset = generate_benchmark_dataset(
        num_samples=num_samples,
        seq_len=seq_len,
        hidden_dim=hidden_dim,
        num_classes=num_classes,
        distractor_rank=subspace_rank,
        distractor_scale=1.5,
        seed=dataset_seed
    )
    
    # 3. Model setup and frozen verification
    model = SyntheticTaskModel(hidden_dim=hidden_dim, num_classes=num_classes)
    wrapper = FrozenModelWrapper(model)
    
    param_hash_before, buf_hash_before = wrapper.compute_hashes()
    
    engine = SCBIEngine(
        model_wrapper=wrapper,
        candidate_count=candidate_count,
        subspace_rank=subspace_rank,
        lambda_entropy=lambda_entropy,
        seed=candidate_seed
    )
    
    # Metrics collection arrays
    scores_baseline = []
    scores_fixed = []
    scores_random = []
    scores_scbi = []
    scores_oracle = []
    scores_matched_baseline = []
    
    regrets_scbi = []
    regrets_random = []
    
    eval_reconstructions = []
    eval_entropies = []
    eval_totals = []
    pool_diversities = []
    
    evaluator_rank_correlations = []
    top1_agreement_count = 0
    
    start_time = time.perf_counter()
    
    for i in range(num_samples):
        x_i = dataset.inputs[i:i+1] # (1, seq_len, hidden_dim)
        y_true = dataset.labels[i].item()
        
        # --- EXP001: Frozen Baseline ---
        h_0 = model.forward_prefix(x_i) # (1, seq_len, hidden_dim)
        logits_base = model.forward_suffix(h_0)
        pred_base = int(torch.argmax(logits_base, dim=-1).item())
        m_base = 1.0 if pred_base == y_true else 0.0
        scores_baseline.append(m_base)
        
        # --- Generate Candidates G ---
        candidates = generate_candidate_subspaces(
            h_0.squeeze(0),
            candidate_count=candidate_count,
            subspace_rank=subspace_rank,
            seed=candidate_seed + i
        )
        diversity, _ = compute_candidate_pool_diversity(candidates)
        pool_diversities.append(diversity)
        
        # --- EXP002: Fixed Projection (Candidate 0 fixed) ---
        h_fixed = candidates[0].project(h_0)
        logits_fixed = model.forward_suffix(h_fixed)
        pred_fixed = int(torch.argmax(logits_fixed, dim=-1).item())
        m_fixed = 1.0 if pred_fixed == y_true else 0.0
        scores_fixed.append(m_fixed)
        
        # --- Evaluate all candidates in pool ---
        cand_scores = []
        cand_m_scores = []
        
        for k, cand in enumerate(candidates):
            h_proj = cand.project(h_0)
            score_E = engine.evaluate_candidate(cand, h_0.squeeze(0))
            cand_scores.append(score_E)
            
            # Ground truth task evaluation for Oracle & Predictiveness study
            logits_k = model.forward_suffix(h_proj)
            pred_k = int(torch.argmax(logits_k, dim=-1).item())
            m_k = 1.0 if pred_k == y_true else 0.0
            cand_m_scores.append(m_k)
            
        eval_totals.extend(cand_scores)
        
        # --- EXP003: Random Selection ---
        k_random = int(torch.randint(0, candidate_count, (1,)).item())
        m_random = cand_m_scores[k_random]
        scores_random.append(m_random)
        
        # --- EXP004: SCBI Evaluator Selection ---
        k_scbi = int(np.argmin(cand_scores))
        m_scbi = cand_m_scores[k_scbi]
        scores_scbi.append(m_scbi)
        
        # --- EXP005: Oracle Selection ---
        k_oracle = int(np.argmax(cand_m_scores))
        m_oracle = cand_m_scores[k_oracle]
        scores_oracle.append(m_oracle)
        
        # Selection Regret
        regrets_scbi.append(m_oracle - m_scbi)
        regrets_random.append(m_oracle - m_random)
        
        # --- EXP006: Evaluator Predictiveness ---
        # Top-1 agreement: did argmin E match an optimal candidate?
        if m_scbi == m_oracle:
            top1_agreement_count += 1
            
        # Spearman correlation (reverse cand_scores because lower E is hypothesized to be better)
        if len(set(cand_m_scores)) > 1 and len(set(cand_scores)) > 1:
            r, _ = stats.spearmanr([-s for s in cand_scores], cand_m_scores)
            if not np.isnan(r):
                evaluator_rank_correlations.append(r)
                
        # --- Forward-Pass Matched Baseline ---
        # Draw 4 stochastic perturbed samples, pick lowest logit entropy
        cand_base_h = [h_0 + torch.randn_like(h_0) * 0.05 for _ in range(candidate_count)]
        entropies = []
        base_preds = []
        for h_pert in cand_base_h:
            log_p = torch.log_softmax(model.forward_suffix(h_pert), dim=-1)
            p = torch.softmax(log_p, dim=-1)
            ent = (-torch.sum(p * log_p)).item()
            entropies.append(ent)
            base_preds.append(int(torch.argmax(p, dim=-1).item()))
        best_base_idx = int(np.argmin(entropies))
        scores_matched_baseline.append(1.0 if base_preds[best_base_idx] == y_true else 0.0)
        
    elapsed_time = time.perf_counter() - start_time
    
    # 4. Final verification of frozen state
    wrapper.verify_frozen()
    param_hash_after, buf_hash_after = wrapper.compute_hashes()
    
    assert param_hash_before == param_hash_after, "FATAL: Parameter hash mutated!"
    assert buf_hash_before == buf_hash_after, "FATAL: Buffer hash mutated!"
    
    # 5. Statistical Calculations
    arr_base = np.array(scores_baseline)
    arr_fixed = np.array(scores_fixed)
    arr_random = np.array(scores_random)
    arr_scbi = np.array(scores_scbi)
    arr_oracle = np.array(scores_oracle)
    arr_matched = np.array(scores_matched_baseline)
    
    diff_scbi_vs_random = arr_scbi - arr_random
    diff_scbi_vs_matched = arr_scbi - arr_matched
    
    # Wilcoxon signed-rank test
    try:
        w_res_random = stats.wilcoxon(diff_scbi_vs_random)
        wilcoxon_p_random = float(w_res_random.pvalue)
    except Exception:
        wilcoxon_p_random = 1.0
        
    try:
        w_res_matched = stats.wilcoxon(diff_scbi_vs_matched)
        wilcoxon_p_matched = float(w_res_matched.pvalue)
    except Exception:
        wilcoxon_p_matched = 1.0
        
    results: Dict[str, Any] = {
        "metadata": {
            "num_samples": num_samples,
            "hidden_dim": hidden_dim,
            "seq_len": seq_len,
            "candidate_count": candidate_count,
            "subspace_rank": subspace_rank,
            "lambda_entropy": lambda_entropy,
            "dataset_seed": dataset_seed,
            "candidate_seed": candidate_seed,
            "experiment_seed": experiment_seed,
            "wall_clock_time_seconds": round(elapsed_time, 4),
            "prefix_forward_passes_per_instance": 1,
            "selected_suffix_forward_passes_per_instance": 1,
            "total_model_forward_operations_per_instance": 2,
            "parameter_hash_before": param_hash_before,
            "parameter_hash_after": param_hash_after,
            "buffer_hash_before": buf_hash_before,
            "buffer_hash_after": buf_hash_after,
            "checksums_match": True,
            "requires_grad_all_false": True,
            "model_training_false": True
        },
        "metrics": {
            "EXP001_frozen_baseline_accuracy": float(np.mean(arr_base)),
            "EXP002_fixed_projection_accuracy": float(np.mean(arr_fixed)),
            "EXP003_random_selection_accuracy": float(np.mean(arr_random)),
            "EXP004_scbi_evaluator_accuracy": float(np.mean(arr_scbi)),
            "EXP005_oracle_selection_accuracy": float(np.mean(arr_oracle)),
            "matched_baseline_accuracy": float(np.mean(arr_matched)),
            
            "selection_regret_scbi": float(np.mean(regrets_scbi)),
            "selection_regret_random": float(np.mean(regrets_random)),
            "regret_difference": float(np.mean(regrets_random) - np.mean(regrets_scbi)),
            
            "mean_candidate_pool_diversity": float(np.mean(pool_diversities)),
            "evaluator_top1_agreement_rate": float(top1_agreement_count / num_samples),
            "mean_spearman_rank_correlation": float(np.mean(evaluator_rank_correlations)) if evaluator_rank_correlations else 0.0,
            
            "delta_scbi_vs_random": float(np.mean(diff_scbi_vs_random)),
            "ci95_scbi_vs_random": bootstrap_ci(diff_scbi_vs_random),
            "wilcoxon_p_scbi_vs_random": wilcoxon_p_random,
            
            "delta_scbi_vs_matched": float(np.mean(diff_scbi_vs_matched)),
            "ci95_scbi_vs_matched": bootstrap_ci(diff_scbi_vs_matched),
            "wilcoxon_p_scbi_vs_matched": wilcoxon_p_matched
        }
    }
    
    results_path = os.path.join(output_dir, "results.json")
    with open(results_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=4)
        
    print("\n=== EXP001–EXP006 EXECUTION COMPLETE ===")
    print(json.dumps(results["metrics"], indent=4))
    print(f"Results saved to: {results_path}\n")
    return results


if __name__ == "__main__":
    run_experiment_suite()
