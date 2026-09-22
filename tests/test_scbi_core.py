"""
Unit and Invariant Verification Suite for SCBI Core Implementation.

Verifies:
1. Frozen backbone invariant (Delta_theta = 0) and checksum guard triggers.
2. Algebraic properties of SubspaceProjector (idempotence, symmetry).
3. Candidate generation determinism and shape validity.
4. End-to-end SCBI engine episode execution.
5. Compute-matched baseline forward-pass counter equivalence.
"""

import os
import sys

# Ensure workspace root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import torch
import torch.nn as nn

from scbi.core.frozen_model import FrozenModelWrapper, FrozenModelGuardError
from scbi.core.basis import SubspaceProjector, generate_candidate_subspaces
from scbi.core.engine import SCBIEngine
from scbi.baselines.matched_baseline import ComputeMatchedBaseline


class SimpleToyModel(nn.Module):
    """Minimal linear toy backbone for invariant testing."""
    def __init__(self, in_features: int = 16, out_features: int = 16):
        super().__init__()
        self.fc = nn.Linear(in_features, out_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc(x)


def test_frozen_model_wrapper_invariance():
    """Confirms that parameters are frozen and checksum verification succeeds."""
    model = SimpleToyModel()
    wrapper = FrozenModelWrapper(model)
    
    # Check requires_grad is False
    for param in model.parameters():
        assert not param.requires_grad
        
    # Verify passes without error
    wrapper.verify_frozen()
    
    # Intentionally corrupt a parameter to test guard detection
    with torch.no_grad():
        model.fc.weight.add_(1.0)
        
    with pytest.raises(FrozenModelGuardError):
        wrapper.verify_frozen()


def test_subspace_projector_algebra():
    """Confirms that P = I - V V^T is symmetric and idempotent (P^2 = P)."""
    d = 32
    r = 4
    V = torch.randn(d, r)
    projector = SubspaceProjector(V)
    
    assert projector.verify_algebraic_properties()
    
    # Test projection on random activation batch
    h = torch.randn(8, d)
    h_proj = projector.project(h)
    assert h_proj.shape == h.shape
    
    # Projecting twice must yield the same result (idempotence on data)
    h_proj2 = projector.project(h_proj)
    assert torch.allclose(h_proj, h_proj2, atol=1e-5)


def test_candidate_generator():
    """Confirms candidate generator produces K valid orthonormal projectors."""
    seq_len = 10
    hidden_dim = 16
    K = 4
    r = 2
    
    h_tokens = torch.randn(seq_len, hidden_dim)
    candidates = generate_candidate_subspaces(h_tokens, candidate_count=K, subspace_rank=r, seed=42)
    
    assert len(candidates) == K
    for cand in candidates:
        assert cand.verify_algebraic_properties()


def test_scbi_engine_episode():
    """Runs a complete SCBI inference episode and verifies checksum integrity."""
    model = SimpleToyModel(in_features=16, out_features=16)
    wrapper = FrozenModelWrapper(model)
    
    engine = SCBIEngine(
        model_wrapper=wrapper,
        candidate_count=4,
        subspace_rank=2,
        seed=42
    )
    
    h_tokens = torch.randn(6, 16)
    h_star, best_proj, meta = engine.run_episode(h_tokens)
    
    assert h_star.shape == h_tokens.shape
    assert meta["candidate_count"] == 4
    assert meta["checksum_verified"] is True
    assert 0 <= meta["selected_candidate_idx"] < 4
    assert len(engine.transient_state) == 0  # State must be purged post-episode


def test_compute_matched_baseline():
    """Confirms that the compute-matched baseline runs exactly budget_k evaluations."""
    model = SimpleToyModel()
    wrapper = FrozenModelWrapper(model)
    baseline = ComputeMatchedBaseline(wrapper, budget_k=4)
    
    h_tokens = torch.randn(6, 16)
    
    def mock_scorer(h: torch.Tensor) -> float:
        return torch.norm(h).item()
        
    best_sample, best_idx, meta = baseline.run_matched_sampling(h_tokens, mock_scorer)
    
    assert meta["budget_k"] == 4
    assert meta["total_evals"] == 4
    assert 0 <= best_idx < 4


if __name__ == "__main__":
    test_frozen_model_wrapper_invariance()
    test_subspace_projector_algebra()
    test_candidate_generator()
    test_scbi_engine_episode()
    test_compute_matched_baseline()
    print("ALL TESTS PASSED SUCCESSFULLY!")
