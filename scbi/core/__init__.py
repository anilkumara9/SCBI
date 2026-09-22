"""
SCBI Core Module Package.
"""

from scbi.core.frozen_model import FrozenModelWrapper, FrozenModelGuardError
from scbi.core.basis import SubspaceProjector, generate_candidate_subspaces
from scbi.core.engine import SCBIEngine

__all__ = [
    "FrozenModelWrapper",
    "FrozenModelGuardError",
    "SubspaceProjector",
    "generate_candidate_subspaces",
    "SCBIEngine"
]
