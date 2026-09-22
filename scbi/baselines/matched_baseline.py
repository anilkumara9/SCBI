"""
Compute-Matched Baseline Suite.

Governing Constitution: AGENTS.md Law 9, Law 14
Governing Rule: .agents/rules/03-experiments.md
"""

from typing import Any, Callable, Dict, List, Tuple
import torch

from scbi.core.frozen_model import FrozenModelWrapper


class ComputeMatchedBaseline:
    """
    Executes compute-matched baselines (Best-of-N, temperature sampling)
    that consume exactly the same number of evaluations as SCBI candidate count K.
    """

    def __init__(self, model_wrapper: FrozenModelWrapper, budget_k: int = 4):
        self.model_wrapper = model_wrapper
        self.budget_k = budget_k
        self.eval_counter = 0

    def run_matched_sampling(
        self,
        h_tokens: torch.Tensor,
        sample_scoring_fn: Callable[[torch.Tensor], float],
        temperature: float = 0.7
    ) -> Tuple[torch.Tensor, int, Dict[str, Any]]:
        """
        Runs exactly budget_k candidate forward passes / perturbations,
        evaluates each with sample_scoring_fn, and selects the best sample.
        """
        self.model_wrapper.verify_frozen()
        
        candidates: List[torch.Tensor] = []
        scores: List[float] = []

        for i in range(self.budget_k):
            self.eval_counter += 1
            # Add stochastic perturbation matched to temperature sampling
            noise = torch.randn_like(h_tokens) * (temperature * 0.05)
            h_perturbed = h_tokens + noise
            score = sample_scoring_fn(h_perturbed)
            candidates.append(h_perturbed)
            scores.append(score)

        best_idx = int(torch.argmin(torch.tensor(scores)).item())
        
        self.model_wrapper.verify_frozen()

        metadata = {
            "budget_k": self.budget_k,
            "total_evals": self.eval_counter,
            "scores": scores,
            "selected_idx": best_idx
        }

        return candidates[best_idx], best_idx, metadata
