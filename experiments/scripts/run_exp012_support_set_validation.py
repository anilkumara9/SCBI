"""
EXP012: Hierarchical Support-Set Relational Validation Study.

Evaluates the complete hierarchical ladder on independent held-out data:
Level 0: Random Selection (Null Reference)
Level 1: E_single (V0.1 Intrinsic Energy)
Level 2: E_CF (Single-Instance Counterfactual Consistency)
Level 3: E_support (Multi-Instance Support-Set Relational Consistency)
Ceiling: Oracle Selection (Empirical Ceiling)
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
from scbi.core.basis import SubspaceProjector, generate_candidate_subspaces
from experiments.benchmarks.synthetic_disentanglement import (
    generate_benchmark_dataset,
    SyntheticTaskModel
)


def compute_js_divergence_pair(p: torch.Tensor, q: torch.Tensor) -> float:
    m = 0.5 * (p + q)
    kl_p = torch.sum(p * (torch.log(p + 1e-9) - torch.log(m + 1e-9)))
    kl_q = torch.sum(q * (torch.log(q + 1e-9) - torch.log(m + 1e-9)))
    return float(0.5 * (kl_p + kl_q).item())


def bootstrap_ci(arr: np.ndarray, n_boot: int = 10000, ci: float = 0.95) -> List[float]:
    if len(arr) == 0:
        return [0.0, 0.0]
    boot_means = [float(np.mean(np.random.choice(arr, size=len(arr), replace=True))) for _ in range(n_boot)]
    alpha = (1.0 - ci) / 2.0
    return [float(np.percentile(boot_means, 100 * alpha)), float(np.percentile(boot_means, 100 * (1 - alpha)))]


def run_exp012_support_set(
    num_samples: int = 100,
    seq_len: int = 8,
    hidden_dim: int = 32,
    num_classes: int = 4,
    candidate_count: int = 4,
    subspace_rank: int = 2,
    # Strictly independent seeds
    dataset_seed: int = 555,
    candidate_seed: int = 333,
    experiment_seed: int = 32768,
    alpha: float = 0.5,
    support_size: int = 4,
    output_dir: str = "experiments/runs/EXP012_support_set"
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
    
    evaluators = ["Random", "E_single", "E_CF", "E_support", "Oracle"]
    instance_accuracies: Dict[str, List[float]] = {e: [] for e in evaluators}
    
    discriminatory_instances = []
    start_time = time.perf_counter()
    
    for i in range(num_samples):
        x_i = dataset.inputs[i:i+1] # (1, seq_len, hidden_dim)
        y_true = dataset.labels[i].item()
        
        # Support Set S_i: m other unlabeled instances
        support_indices = [(i + 1 + j) % num_samples for j in range(support_size)]
        support_q_base = []
        for s_idx in support_indices:
            h_s = model.forward_prefix(dataset.inputs[s_idx:s_idx+1])
            q_s = F.softmax(model.forward_suffix(h_s), dim=-1).squeeze(0)
            support_q_base.append(q_s)
            
        # Counterfactual Views for E_CF:
        x_plus = x_i + 0.05 * torch.randn_like(x_i)
        x_minus = x_i.clone()
        corrupt_indices = torch.randperm(seq_len)[:(seq_len // 2)]
        x_minus[0, corrupt_indices] = torch.randn(len(corrupt_indices), hidden_dim)
        
        h_0 = model.forward_prefix(x_i)
        h_plus = model.forward_prefix(x_plus)
        h_minus = model.forward_prefix(x_minus)
        h_s = h_0.squeeze(0)
        
        cands = generate_candidate_subspaces(
            h_s,
            candidate_count=candidate_count,
            subspace_rank=subspace_rank,
            seed=candidate_seed + i
        )
        
        cand_task_scores = []
        cand_eval_scores: Dict[str, List[float]] = {
            "E_single": [],
            "E_CF": [],
            "E_support": []
        }
        cand_diagnostics = []
        
        for k, cand in enumerate(cands):
            h_proj = cand.project(h_0)
            q0 = F.softmax(model.forward_suffix(h_proj), dim=-1).squeeze(0)
            qp = F.softmax(model.forward_suffix(cand.project(h_plus)), dim=-1).squeeze(0)
            qm = F.softmax(model.forward_suffix(cand.project(h_minus)), dim=-1).squeeze(0)
            
            pred_k = int(torch.argmax(q0).item())
            is_correct = 1 if pred_k == y_true else 0
            cand_task_scores.append(is_correct)
            
            # --- 1. E_single (V0.1 Intrinsic Energy) ---
            norm_diff = torch.norm(h_0 - h_proj, p="fro") / (torch.norm(h_0, p="fro") + 1e-8)
            probs = F.softmax(torch.mean(torch.abs(h_proj), dim=1), dim=-1)
            entropy = -torch.sum(probs * torch.log(probs + 1e-9))
            score_single = norm_diff.item() + 0.1 * entropy.item()
            cand_eval_scores["E_single"].append(score_single)
            
            # --- 2. E_CF (Single-Instance Counterfactual) ---
            d_pos = compute_js_divergence_pair(q0, qp)
            d_neg = compute_js_divergence_pair(q0, qm)
            score_cf = d_pos - alpha * d_neg
            cand_eval_scores["E_CF"].append(score_cf)
            
            # --- 3. E_support (Multi-Instance Support-Set Relational) ---
            d_support = float(np.mean([compute_js_divergence_pair(q0, qs) for qs in support_q_base]))
            score_support = d_pos - alpha * d_support
            cand_eval_scores["E_support"].append(score_support)
            
            cand_diagnostics.append({
                "is_correct": is_correct,
                "d_pos": d_pos,
                "d_neg": d_neg,
                "d_support": d_support
            })
            
        corr_count = sum(cand_task_scores)
        if 1 <= corr_count <= (candidate_count - 1):
            discriminatory_instances.append({
                "cand_diagnostics": cand_diagnostics,
                "cand_eval_scores": cand_eval_scores
            })
            
        # Selection
        # 1. Random
        k_rnd = int(torch.randint(0, candidate_count, (1,)).item())
        instance_accuracies["Random"].append(float(cand_task_scores[k_rnd]))
        
        # 2. Oracle
        k_orc = int(np.argmax(cand_task_scores))
        instance_accuracies["Oracle"].append(float(cand_task_scores[k_orc]))
        
        # 3. Evaluators (argmin)
        for e in ["E_single", "E_CF", "E_support"]:
            k_best = int(np.argmin(cand_eval_scores[e]))
            instance_accuracies[e].append(float(cand_task_scores[k_best]))
            
    elapsed = time.perf_counter() - start_time
    wrapper.verify_frozen()
    param_hash_after, buf_hash_after = wrapper.compute_hashes()
    assert param_hash_before == param_hash_after
    
    # Statistical Analysis
    random_accs = np.array(instance_accuracies["Random"])
    oracle_accs = np.array(instance_accuracies["Oracle"])
    
    m_random = float(np.mean(random_accs))
    m_oracle = float(np.mean(oracle_accs))
    oracle_opportunity = m_oracle - m_random
    
    evaluator_results = {}
    for e in evaluators:
        acc_arr = np.array(instance_accuracies[e])
        mean_acc = float(np.mean(acc_arr))
        acc_ci = bootstrap_ci(acc_arr)
        
        diff_vs_rnd = acc_arr - random_accs
        delta_rnd = float(np.mean(diff_vs_rnd))
        ci_delta = bootstrap_ci(diff_vs_rnd)
        
        try:
            p_val = float(stats.wilcoxon(diff_vs_rnd).pvalue) if not np.all(diff_vs_rnd == 0) else 1.0
        except Exception:
            p_val = 1.0
            
        recovery = float(delta_rnd / oracle_opportunity) if oracle_opportunity > 0 else 0.0
        
        evaluator_results[e] = {
            "mean_accuracy": round(mean_acc, 4),
            "accuracy_ci95": [round(acc_ci[0], 4), round(acc_ci[1], 4)],
            "delta_vs_random": round(delta_rnd, 4),
            "ci95_delta_vs_random": [round(ci_delta[0], 4), round(ci_delta[1], 4)],
            "wilcoxon_p_vs_random": round(p_val, 4),
            "oracle_recovery_ratio_RE": round(recovery, 4)
        }
        
    # Cluster-aware pairwise ranking on discriminatory instances
    num_disc = len(discriminatory_instances)
    pairwise_rankings = {}
    for e in ["E_single", "E_CF", "E_support"]:
        r_i_list = []
        for inst in discriminatory_instances:
            corr_indices = [idx for idx, d in enumerate(inst["cand_diagnostics"]) if d["is_correct"] == 1]
            inc_indices = [idx for idx, d in enumerate(inst["cand_diagnostics"]) if d["is_correct"] == 0]
            n_p = len(corr_indices) * len(inc_indices)
            
            c_cnt = 0.0
            scores = inst["cand_eval_scores"][e]
            for ci in corr_indices:
                for inc_i in inc_indices:
                    if scores[ci] < scores[inc_i]:
                        c_cnt += 1.0
                    elif scores[ci] == scores[inc_i]:
                        c_cnt += 0.5
            r_i_list.append(c_cnt / n_p)
            
        r_arr = np.array(r_i_list)
        mean_R = float(np.mean(r_arr))
        boot_R = bootstrap_ci(r_arr)
        
        perm_means = []
        for _ in range(5000):
            perm_r_inst = []
            for inst in discriminatory_instances:
                obs_corr = [d["is_correct"] for d in inst["cand_diagnostics"]]
                perm_labels = np.random.permutation(obs_corr)
                c_idx = [idx for idx, lab in enumerate(perm_labels) if lab == 1]
                inc_idx = [idx for idx, lab in enumerate(perm_labels) if lab == 0]
                n_p = len(c_idx) * len(inc_idx)
                
                c_cnt = 0.0
                scores = inst["cand_eval_scores"][e]
                for ci in c_idx:
                    for inc_i in inc_idx:
                        if scores[ci] < scores[inc_i]:
                            c_cnt += 1.0
                        elif scores[ci] == scores[inc_i]:
                            c_cnt += 0.5
                perm_r_inst.append(c_cnt / n_p)
            perm_means.append(float(np.mean(perm_r_inst)))
            
        p_perm = float(np.mean([abs(pm - 0.50) >= abs(mean_R - 0.50) for pm in perm_means]))
        pairwise_rankings[e] = {
            "mean_R_instance": round(mean_R, 4),
            "ci95_cluster_bootstrap": [round(boot_R[0], 4), round(boot_R[1], 4)],
            "within_instance_perm_p": round(p_perm, 4)
        }
        
    final_output = {
        "metadata": {
            "experiment_id": "EXP012",
            "num_samples": num_samples,
            "num_discriminatory_instances": num_disc,
            "dataset_seed": dataset_seed,
            "candidate_seed": candidate_seed,
            "alpha": alpha,
            "support_size": support_size,
            "wall_clock_time_seconds": round(elapsed, 4),
            "checksums_match": True,
            "strictly_independent_instances": True
        },
        "selection_performance_ladder": evaluator_results,
        "cluster_aware_pairwise_ranking": pairwise_rankings
    }
    
    save_path = os.path.join(output_dir, "support_set_results.json")
    with open(save_path, "w", encoding="utf-8") as fh:
        json.dump(final_output, fh, indent=4)
        
    print("\n=== EXP012 SUPPORT-SET RELATIONAL STUDY COMPLETE ===")
    print(json.dumps(final_output, indent=2))
    return final_output


if __name__ == "__main__":
    run_exp012_support_set()
