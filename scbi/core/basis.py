"""
Subspace Representation Objects and Candidate Projection Basis.

Governing Document: theory/README_FORMULATION.md (Formulation D+C)
Governing Rule: .agents/rules/02-theory.md
"""

from typing import List, Tuple
import torch
import torch.nn as nn


class SubspaceProjector:
    """
    Represents an orthogonal subspace projector P = I - V V^T.
    Projects activations onto the orthogonal complement of subspace spanned by V.
    """

    def __init__(self, V: torch.Tensor):
        """
        Args:
            V: Orthonormal basis matrix of shape (d, r) where r is rank and d is hidden_dim.
        """
        if V.ndim != 2:
            raise ValueError(f"Basis tensor V must be 2D (d, r), got shape {V.shape}")
        
        self.d, self.r = V.shape
        # Ensure orthonormal basis via QR decomposition
        Q, _ = torch.linalg.qr(V)
        self.V = Q[:, :self.r]

    def project(self, h: torch.Tensor) -> torch.Tensor:
        """
        Applies projection P h = h - h V V^T to activation tensor h of shape (..., d).
        """
        # h @ V -> (..., r)
        # (h @ V) @ V^T -> (..., d)
        proj_component = torch.matmul(torch.matmul(h, self.V), self.V.t())
        return h - proj_component

    def verify_algebraic_properties(self, atol: float = 1e-5) -> bool:
        """
        Verifies idempotence (P^2 = P) and symmetry (P^T = P).
        """
        I = torch.eye(self.d, device=self.V.device, dtype=self.V.dtype)
        P = I - torch.matmul(self.V, self.V.t())
        
        # Check symmetry: P^T == P
        sym_diff = torch.max(torch.abs(P - P.t())).item()
        # Check idempotence: P @ P == P
        idem_diff = torch.max(torch.abs(torch.matmul(P, P) - P)).item()
        
        return sym_diff < atol and idem_diff < atol


def generate_candidate_subspaces(
    h_tokens: torch.Tensor,
    candidate_count: int = 4,
    subspace_rank: int = 2,
    seed: int = 42
) -> List[SubspaceProjector]:
    """
    Candidate Generator (Operator G):
    Constructs K candidate projection subspaces from prompt activation slices
    using SVD across distinct token subsets.

    Args:
        h_tokens: Tensor of shape (seq_len, hidden_dim).
        candidate_count: Number of candidate projectors to synthesize (K).
        subspace_rank: Rank r of the subspace to isolate.
        seed: Random seed for deterministic candidate partitioning.

    Returns:
        List of K SubspaceProjector instances.
    """
    seq_len, hidden_dim = h_tokens.shape
    candidates: List[SubspaceProjector] = []
    
    # Generate deterministic candidate slices
    gen = torch.Generator().manual_seed(seed)
    
    for k in range(candidate_count):
        # Candidate k: slice random subset or contrastive interval
        if seq_len > subspace_rank:
            indices = torch.randperm(seq_len, generator=gen)[:max(subspace_rank + 1, 3)]
            slice_h = h_tokens[indices]
            # SVD on slice to find principal directions
            _, _, Vh = torch.linalg.svd(slice_h, full_matrices=False)
            V_cand = Vh[:subspace_rank].t() # (hidden_dim, rank)
        else:
            # Fallback for very short sequences: orthogonal random directions
            rand_mat = torch.randn(hidden_dim, subspace_rank, generator=gen)
            V_cand, _ = torch.linalg.qr(rand_mat)
        
        candidates.append(SubspaceProjector(V_cand))
    
    return candidates


def compute_subspace_distance(P1: SubspaceProjector, P2: SubspaceProjector) -> float:
    """
    Computes normalized projection Frobenius distance between two projectors:
    D(P1, P2) = ||P1 - P2||_F / sqrt(2 * r)
    """
    I = torch.eye(P1.d, device=P1.V.device, dtype=P1.V.dtype)
    proj1 = I - torch.matmul(P1.V, P1.V.t())
    proj2 = I - torch.matmul(P2.V, P2.V.t())
    norm_diff = torch.norm(proj1 - proj2, p="fro").item()
    norm_denom = (2.0 * min(P1.r, P2.r)) ** 0.5
    return norm_diff / (norm_denom + 1e-8)


def compute_candidate_pool_diversity(candidates: List[SubspaceProjector]) -> Tuple[float, List[List[float]]]:
    """
    Measures pairwise projection distances across candidate pool.
    Returns (mean_pairwise_distance, distance_matrix).
    """
    K = len(candidates)
    if K <= 1:
        return 0.0, [[0.0]]
    
    dist_matrix = [[0.0] * K for _ in range(K)]
    total_dist = 0.0
    pairs_count = 0
    
    for i in range(K):
        for j in range(i + 1, K):
            d = compute_subspace_distance(candidates[i], candidates[j])
            dist_matrix[i][j] = d
            dist_matrix[j][i] = d
            total_dist += d
            pairs_count += 1
            
    mean_dist = total_dist / max(pairs_count, 1)
    return mean_dist, dist_matrix

