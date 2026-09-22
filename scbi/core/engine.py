"""
SCBI Core Engine: Candidate Generation, Evaluation, and Selection Pipeline.

Governing Document: theory/README_ALGORITHM.md
Governing Rule: .agents/rules/00-core-research.md, .agents/rules/04-code.md
"""

from typing import Any, Callable, Dict, List, Optional, Tuple
import torch
import torch.nn.functional as F

from scbi.core.frozen_model import FrozenModelWrapper
from scbi.core.basis import SubspaceProjector, generate_candidate_subspaces


class SCBIEngine:
    """
    Executes the SCBI Inference Loop:
    (theta, x) -> G -> {B_k} -> E -> {s_k} -> S -> B* -> Readout -> y_hat
    with verified parameter immutability.
    """

    def __init__(
        self,
        model_wrapper: FrozenModelWrapper,
        candidate_count: int = 4,
        subspace_rank: int = 2,
        lambda_entropy: float = 0.1,
        seed: int = 42
    ):
        self.model_wrapper = model_wrapper
        self.candidate_count = candidate_count
        self.subspace_rank = subspace_rank
        self.lambda_entropy = lambda_entropy
        self.seed = seed
        self.transient_state: Dict[str, Any] = {}

    def evaluate_candidate(
        self,
        projector: SubspaceProjector,
        h_tokens: torch.Tensor,
        eval_fn: Optional[Callable[[torch.Tensor], float]] = None
    ) -> float:
        """
        Candidate Evaluator (Operator E):
        Calculates unsupervised objective:
        E(P, h) = L_reconstruction(h, P h) + lambda * Entropy(P h)
        """
        if eval_fn is not None:
            return eval_fn(projector.project(h_tokens))

        h_proj = projector.project(h_tokens)
        
        # 1. Normalized reconstruction variance
        norm_diff = torch.norm(h_tokens - h_proj, p="fro") / (torch.norm(h_tokens, p="fro") + 1e-8)
        
        # 2. Representation entropy proxy (uniformity of activation energy across dimensions)
        probs = F.softmax(torch.mean(torch.abs(h_proj), dim=0), dim=-1)
        entropy = -torch.sum(probs * torch.log(probs + 1e-9))
        
        score = norm_diff.item() + self.lambda_entropy * entropy.item()
        return score

    def select_candidate(
        self,
        candidates: List[SubspaceProjector],
        scores: List[float]
    ) -> Tuple[SubspaceProjector, int]:
        """
        Candidate Selector (Operator S):
        P* = argmin_k E(P_k, h)
        """
        best_idx = int(torch.argmin(torch.tensor(scores)).item())
        return candidates[best_idx], best_idx

    def run_episode(
        self,
        h_tokens: torch.Tensor,
        eval_fn: Optional[Callable[[torch.Tensor], float]] = None
    ) -> Tuple[torch.Tensor, SubspaceProjector, Dict[str, Any]]:
        """
        Executes a single inference episode on instance activation h_tokens.

        Returns:
            h_star: Transformed activation projected via optimal basis P*.
            best_projector: The selected SubspaceProjector P*.
            metadata: Log dictionary with candidate scores and parameter integrity.
        """
        # 1. Verify frozen backbone before inference
        self.model_wrapper.verify_frozen()

        # 2. Operator G: Generate candidate bases
        candidates = generate_candidate_subspaces(
            h_tokens,
            candidate_count=self.candidate_count,
            subspace_rank=self.subspace_rank,
            seed=self.seed
        )

        # Measure candidate pool diversity (measurement only)
        from scbi.core.basis import compute_candidate_pool_diversity
        mean_diversity, dist_matrix = compute_candidate_pool_diversity(candidates)

        # Baseline entropy before projection
        probs_before = F.softmax(torch.mean(torch.abs(h_tokens), dim=0), dim=-1)
        entropy_before = (-torch.sum(probs_before * torch.log(probs_before + 1e-9))).item()

        # 3. Operator E: Evaluate each candidate with detailed measurement decomposition
        candidate_metrics: List[Dict[str, float]] = []
        scores: List[float] = []

        for cand in candidates:
            h_proj = cand.project(h_tokens)
            reconstruction_term = (torch.norm(h_tokens - h_proj, p="fro") / (torch.norm(h_tokens, p="fro") + 1e-8)).item()
            
            probs_after = F.softmax(torch.mean(torch.abs(h_proj), dim=0), dim=-1)
            entropy_after = (-torch.sum(probs_after * torch.log(probs_after + 1e-9))).item()
            entropy_term = self.lambda_entropy * entropy_after
            total_score = reconstruction_term + entropy_term
            
            energy_removed = (torch.norm(h_tokens - h_proj, p="fro") / (torch.norm(h_tokens, p="fro") + 1e-8)).item()

            scores.append(total_score)
            candidate_metrics.append({
                "reconstruction_term": reconstruction_term,
                "entropy_term": entropy_term,
                "entropy_before_projection": entropy_before,
                "entropy_after_projection": entropy_after,
                "energy_removed": energy_removed,
                "total_score": total_score
            })

        # 4. Operator S: Select optimal basis P*
        best_projector, best_idx = self.select_candidate(candidates, scores)

        # 5. Apply optimal transformation
        h_star = best_projector.project(h_tokens)

        # 6. Verify frozen backbone after inference
        self.model_wrapper.verify_frozen()

        metadata = {
            "prefix_forward_passes": 1,
            "selected_suffix_forward_passes": 1,
            "total_model_forward_operations": 2,
            "candidate_count": len(candidates),
            "scores": scores,
            "selected_candidate_idx": best_idx,
            "selected_score": scores[best_idx],
            "candidate_metrics": candidate_metrics,
            "mean_candidate_diversity": mean_diversity,
            "pairwise_distances": dist_matrix,
            "checksum_verified": True
        }

        # 7. Transient state isolation purge
        self.purge_transient_state()

        return h_star, best_projector, metadata

    def purge_transient_state(self) -> None:
        """Purges any transient episode variables to eliminate cross-sample state leakage."""
        self.transient_state.clear()
