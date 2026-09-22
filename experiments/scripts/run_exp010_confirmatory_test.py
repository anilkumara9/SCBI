"""
EXP010: Confirmatory Post-Nonlinear Variance Selection Study.

Strictly tests Hypothesis H1_EXP010 on genuinely independent, held-out instances:
D_discovery (seeds 42, 137, 4096) disjoint from D_EXP010 (dataset_seed 999, candidate_seed 777).

Evaluates complete ladder:
1. Random Selection (Null)
2. V0.1 (Energy Re-construction)
3. E_var (Primary Confirmatory: Post-GELU Variance)
4. E_norm (Ablation: Post-GELU Norm)
5. E_var_norm (Combined Ablation)
6. Oracle Selection (Ceiling)
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


def compute_effective_rank(tensor: torch.Tensor) -> float:
    try:
        _, s, _ = torch.linalg.svd(tensor, full_matrices=False)
        p = s / (torch.sum(s) + 1e-9)
        entropy = -torch.sum(p * torch.log(p + 1e-9)).item()
        return float(np.exp(entropy))
    except Exception:
        return 1.0


def bootstrap_ci(arr: np.ndarray, n_boot: int = 10000, ci: float = 0.95) -> List[float]:
    if len(arr) == 0:
        return [0.0, 0.0]
    boot_means = [float(np.mean(np.random.choice(arr, size=len(arr), replace=True))) for _ in range(n_boot)]
    alpha = (1.0 - ci) / 2.0
    return [float(np.percentile(boot_means, 100 * alpha)), float(np.percentile(boot_means, 100 * (1 - alpha)))]


def run_exp010_confirmation(
    num_samples: int = 100,
    seq_len: int = 8,
    hidden_dim: int = 32,
    num_classes: int = 4,
    candidate_count: int = 4,
    subspace_rank: int = 2,
    # Strictly disjoint seeds from EXP001-EXP009
    dataset_seed: int = 999,
    candidate_seed: int = 777,
    experiment_seed: int = 8192,
    output_dir: str = "experiments/runs/EXP010_confirmation"
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
    
    evaluators = ["Random", "V0.1", "E_var", "E_norm", "E_var_norm", "Oracle"]
    instance_accuracies: Dict[str, List[float]] = {e: [] for e in evaluators}
    selected_anti_collapse: Dict[str, Dict[str, List[float]]] = {
        e: {"var_l1": [], "norm_l1": [], "eff_rank": []} for e in evaluators
    }
    
    # Store discriminatory instances for within-instance R_i
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
        
        cand_task_scores = []
        cand_eval_scores: Dict[str, List[float]] = {
            "V0.1": [],
            "E_var": [],
            "E_norm": [],
            "E_var_norm": []
        }
        cand_diagnostics = []
        
        for k, cand in enumerate(cands):
            h_proj = cand.project(h_0)
            z0 = torch.mean(h_proj, dim=-2)
            
            # Intermediate representation at layer l+1
            z_lin = model.layer_suffix[0](z0)
            z_ln = model.layer_suffix[1](z_lin)
            z_l1 = model.layer_suffix[2](z_ln) # post-GELU
            
            logits = model.layer_suffix[3](z_l1)
            pred_k = int(torch.argmax(logits, dim=-1).item())
            is_correct = 1 if pred_k == y_true else 0
            cand_task_scores.append(is_correct)
            
            var_val = float(torch.var(z_l1).item())
            norm_val = float(torch.norm(z_l1, p=2).item())
            erank_val = compute_effective_rank(h_proj.squeeze(0))
            
            cand_diagnostics.append({
                "is_correct": is_correct,
                "var_l1": var_val,
                "norm_l1": norm_val,
                "eff_rank": erank_val
            })
            
            # --- Evaluator Scores (Minimization convention) ---
            # 1. V0.1
            norm_diff = torch.norm(h_0 - h_proj, p="fro") / (torch.norm(h_0, p="fro") + 1e-8)
            probs = F.softmax(torch.mean(torch.abs(h_proj), dim=1), dim=-1)
            entropy = -torch.sum(probs * torch.log(probs + 1e-9))
            score_v01 = norm_diff.item() + 0.1 * entropy.item()
            cand_eval_scores["V0.1"].append(score_v01)
            
            # 2. E_var: -Var(z_l1)
            cand_eval_scores["E_var"].append(-var_val)
            
            # 3. E_norm: -Norm(z_l1)
            cand_eval_scores["E_norm"].append(-norm_val)
            
            # 4. E_var_norm: -(Var + 0.1 Norm)
            cand_eval_scores["E_var_norm"].append(-(var_val + 0.1 * norm_val))
            
        corr_count = sum(cand_task_scores)
        if 1 <= corr_count <= (candidate_count - 1):
            discriminatory_instances.append({
                "cand_diagnostics": cand_diagnostics,
                "cand_eval_scores": cand_eval_scores
            })
            
        # --- Perform Selection for each condition ---
        # 1. Random Selection
        k_rnd = int(torch.randint(0, candidate_count, (1,)).item())
        instance_accuracies["Random"].append(float(cand_task_scores[k_rnd]))
        selected_anti_collapse["Random"]["var_l1"].append(cand_diagnostics[k_rnd]["var_l1"])
        selected_anti_collapse["Random"]["norm_l1"].append(cand_diagnostics[k_rnd]["norm_l1"])
        selected_anti_collapse["Random"]["eff_rank"].append(cand_diagnostics[k_rnd]["eff_rank"])
        
        # 2. Oracle Selection
        k_orc = int(np.argmax(cand_task_scores))
        instance_accuracies["Oracle"].append(float(cand_task_scores[k_orc]))
        selected_anti_collapse["Oracle"]["var_l1"].append(cand_diagnostics[k_orc]["var_l1"])
        selected_anti_collapse["Oracle"]["norm_l1"].append(cand_diagnostics[k_orc]["norm_l1"])
        selected_anti_collapse["Oracle"]["eff_rank"].append(cand_diagnostics[k_orc]["eff_rank"])
        
        # 3. Evaluators (argmin)
        for e in ["V0.1", "E_var", "E_norm", "E_var_norm"]:
            k_best = int(np.argmin(cand_eval_scores[e]))
            instance_accuracies[e].append(float(cand_task_scores[k_best]))
            selected_anti_collapse[e]["var_l1"].append(cand_diagnostics[k_best]["var_l1"])
            selected_anti_collapse[e]["norm_l1"].append(cand_diagnostics[k_best]["norm_l1"])
            selected_anti_collapse[e]["eff_rank"].append(cand_diagnostics[k_best]["eff_rank"])
            
    elapsed = time.perf_counter() - start_time
    wrapper.verify_frozen()
    param_hash_after, buf_hash_after = wrapper.compute_hashes()
    assert param_hash_before == param_hash_after
    
    # --- Statistical Analysis ---
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
        
        # Anti-collapse means
        mean_var = float(np.mean(selected_anti_collapse[e]["var_l1"]))
        mean_norm = float(np.mean(selected_anti_collapse[e]["norm_l1"]))
        mean_erank = float(np.mean(selected_anti_collapse[e]["eff_rank"]))
        
        evaluator_results[e] = {
            "mean_accuracy": round(mean_acc, 4),
            "accuracy_ci95": [round(acc_ci[0], 4), round(acc_ci[1], 4)],
            "delta_vs_random": round(delta_rnd, 4),
            "ci95_delta_vs_random": [round(ci_delta[0], 4), round(ci_delta[1], 4)],
            "wilcoxon_p_vs_random": round(p_val, 4),
            "oracle_recovery_ratio_RE": round(recovery, 4),
            "anti_collapse_stats": {
                "mean_var_l1": round(mean_var, 4),
                "mean_norm_l1": round(mean_norm, 4),
                "mean_effective_rank": round(mean_erank, 4)
            }
        }
        
    # --- Cluster-Aware Pairwise Ranking Accuracy R_i on Discriminatory Instances ---
    num_disc = len(discriminatory_instances)
    pairwise_rankings = {}
    for e in ["V0.1", "E_var", "E_norm", "E_var_norm"]:
        r_i_list = []
        for inst in discriminatory_instances:
            corr_indices = [idx for idx, d in enumerate(inst["cand_diagnostics"]) if d["is_correct"] == 1]
            inc_indices = [idx for idx, d in enumerate(inst["cand_diagnostics"]) if d["is_correct"] == 0]
            n_p = len(corr_indices) * len(inc_indices)
            
            c_cnt = 0.0
            scores = inst["cand_eval_scores"][e]
            for ci in corr_indices:
                for inc_i in inc_indices:
                    # Minimization: lower is better
                    if scores[ci] < scores[inc_i]:
                        c_cnt += 1.0
                    elif scores[ci] == scores[inc_i]:
                        c_cnt += 0.5
            r_i_list.append(c_cnt / n_p)
            
        r_arr = np.array(r_i_list)
        mean_R = float(np.mean(r_arr))
        boot_R = bootstrap_ci(r_arr)
        
        # Within-instance permutation p-value
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
            "experiment_id": "EXP010",
            "num_samples": num_samples,
            "num_discriminatory_instances": num_disc,
            "dataset_seed": dataset_seed,
            "candidate_seed": candidate_seed,
            "wall_clock_time_seconds": round(elapsed, 4),
            "checksums_match": True,
            "disjoint_from_discovery": True
        },
        "selection_performance_ladder": evaluator_results,
        "cluster_aware_pairwise_ranking": pairwise_rankings
    }
    
    save_path = os.path.join(output_dir, "confirmation_results.json")
    with open(save_path, "w", encoding="utf-8") as fh:
        json.dump(final_output, fh, indent=4)
        
    print("\n=== EXP010 CONFIRMATORY STUDY COMPLETE ===")
    print(json.dumps(final_output, indent=2))
    return final_output


if __name__ == "__main__":
    run_exp010_confirmation()
