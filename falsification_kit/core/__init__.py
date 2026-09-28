"""Decodability Gap falsification kit — core machinery."""
from .scoring import (
    correct_rank, top1_decision, masked_argmax, mcnemar_exact, tango_ci,
    token_id_rank_of_correct, tier0_verdict, battery_arms, battery_decision,
    K, R_SEED,
)

__all__ = [
    "correct_rank", "top1_decision", "masked_argmax", "mcnemar_exact",
    "tango_ci", "token_id_rank_of_correct", "tier0_verdict",
    "battery_arms", "battery_decision", "K", "R_SEED",
]
