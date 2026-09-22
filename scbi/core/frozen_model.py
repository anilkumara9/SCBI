"""
Frozen Foundation Model Wrapper with Automated Runtime Invariant Guards.

Governing Constitution: AGENTS.md Law 6 (Preserve the Frozen Backbone)
Governing Rule: .agents/rules/04-code.md
"""

import hashlib
from typing import Any, Callable, Dict, Optional, Tuple
import torch
import torch.nn as nn


class FrozenModelGuardError(RuntimeError):
    """Raised when an inference step violates the frozen backbone invariant."""
    pass


class FrozenModelWrapper:
    """
    Wraps a PyTorch neural network to guarantee and verify that Delta_theta = 0
    throughout inference.
    """

    def __init__(self, model: nn.Module):
        self.model = model
        self.freeze_backbone()
        self._initial_checksum = self.compute_parameter_checksum()

    def freeze_backbone(self) -> None:
        """Sets eval mode and requires_grad=False on all parameters."""
        self.model.eval()
        for name, param in self.model.named_parameters():
            param.requires_grad = False

    def compute_hashes(self) -> Tuple[str, str]:
        """Computes separate SHA-256 hashes for parameters and buffers."""
        param_hasher = hashlib.sha256()
        for name, param in sorted(self.model.named_parameters()):
            param_hasher.update(name.encode("utf-8"))
            param_hasher.update(param.detach().cpu().numpy().tobytes())
            
        buf_hasher = hashlib.sha256()
        for name, buf in sorted(self.model.named_buffers()):
            buf_hasher.update(name.encode("utf-8"))
            buf_hasher.update(buf.detach().cpu().numpy().tobytes())
            
        return param_hasher.hexdigest(), buf_hasher.hexdigest()

    def compute_parameter_checksum(self) -> str:
        """Computes combined SHA-256 hash across all model parameters and buffers."""
        p_hash, b_hash = self.compute_hashes()
        return hashlib.sha256((p_hash + b_hash).encode("utf-8")).hexdigest()

    def verify_frozen(self) -> None:
        """
        Verifies that no inference operation has modified model weights or buffers,
        and confirms model is in eval mode with requires_grad=False.
        """
        if self.model.training:
            raise FrozenModelGuardError("INVARIANT VIOLATION: Model is in training mode (model.training == True)!")

        for name, param in self.model.named_parameters():
            if param.requires_grad:
                raise FrozenModelGuardError(f"INVARIANT VIOLATION: Parameter {name} has requires_grad=True!")

        current_checksum = self.compute_parameter_checksum()
        if current_checksum != self._initial_checksum:
            raise FrozenModelGuardError(
                f"INVARIANT VIOLATION: Model parameter hash changed! "
                f"Initial: {self._initial_checksum}, Current: {current_checksum}. "
                f"Delta_theta = 0 invariant violated."
            )

    def forward(self, *args: Any, **kwargs: Any) -> Any:
        """Safe forward pass ensuring no gradient tracking."""
        with torch.no_grad():
            return self.model(*args, **kwargs)
