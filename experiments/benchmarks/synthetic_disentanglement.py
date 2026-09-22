"""
Synthetic Linear Disentanglement & Distractor Interference (SLD-DI) Benchmark.

Implements BENCH-001 per Reviewer V0.2 Section 10.
"""

from dataclasses import dataclass
from typing import List, Tuple
import torch
import torch.nn as nn


@dataclass
class BenchmarkDataset:
    inputs: torch.Tensor          # (N, seq_len, hidden_dim)
    labels: torch.Tensor          # (N,)
    distractor_subspace: torch.Tensor  # (hidden_dim, distractor_rank)


def generate_benchmark_dataset(
    num_samples: int = 100,
    seq_len: int = 8,
    hidden_dim: int = 32,
    num_classes: int = 4,
    distractor_rank: int = 2,
    distractor_scale: float = 1.5,
    seed: int = 42
) -> BenchmarkDataset:
    """
    Generates synthetic instances where distractor tokens corrupt the query subspace.
    """
    gen = torch.Generator().manual_seed(seed)
    
    # 1. Define orthogonal target prototypes for each class
    prototypes = torch.randn(num_classes, hidden_dim, generator=gen)
    prototypes, _ = torch.linalg.qr(prototypes.t())
    prototypes = prototypes.t() # (num_classes, hidden_dim)
    
    # 2. Define fixed distractor subspace orthogonal to prototypes
    distractor_raw = torch.randn(hidden_dim, distractor_rank, generator=gen)
    distractor_subspace, _ = torch.linalg.qr(distractor_raw) # (hidden_dim, distractor_rank)
    
    # 3. Sample instances
    labels = torch.randint(0, num_classes, (num_samples,), generator=gen)
    inputs = torch.zeros(num_samples, seq_len, hidden_dim)
    
    for i in range(num_samples):
        cls_idx = labels[i].item()
        target_vec = prototypes[cls_idx]
        
        # Tokens 0..3: Premise tokens carrying target information + small noise
        for s in range(4):
            inputs[i, s] = target_vec + 0.1 * torch.randn(hidden_dim, generator=gen)
            
        # Tokens 4..5: Distractor tokens projecting strongly onto distractor subspace
        for s in range(4, 6):
            coeffs = torch.randn(distractor_rank, generator=gen) * distractor_scale
            distractor_vec = torch.matmul(distractor_subspace, coeffs)
            inputs[i, s] = distractor_vec + 0.1 * torch.randn(hidden_dim, generator=gen)
            
        # Tokens 6..7: Query tokens
        for s in range(6, seq_len):
            inputs[i, s] = target_vec * 0.5 + 0.1 * torch.randn(hidden_dim, generator=gen)
            
    return BenchmarkDataset(
        inputs=inputs,
        labels=labels,
        distractor_subspace=distractor_subspace
    )


class SyntheticTaskModel(nn.Module):
    """
    Model with prefix layers (1..l) and suffix readout layers (l+1..L)
    to test internal representation intervention (Case A).
    """
    def __init__(self, hidden_dim: int = 32, num_classes: int = 4):
        super().__init__()
        # Prefix encoder layers
        self.layer_prefix = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU()
        )
        # Suffix readout layers
        self.layer_suffix = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward_prefix(self, x: torch.Tensor) -> torch.Tensor:
        """Executes Layers 1..l, outputting h_0."""
        return self.layer_prefix(x)

    def forward_suffix(self, h: torch.Tensor) -> torch.Tensor:
        """Executes Layers l+1..L, outputting logits over classes."""
        # Mean pool over sequence tokens then classify
        pooled = torch.mean(h, dim=-2)
        logits = self.layer_suffix(pooled)
        return logits

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Standard full forward pass."""
        h = self.forward_prefix(x)
        return self.forward_suffix(h)
