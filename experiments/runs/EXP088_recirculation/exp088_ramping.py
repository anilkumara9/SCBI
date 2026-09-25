#!/usr/bin/env python3
"""EXP088 ramping schedule (F8, pinned at build).

Signed protocol F8: the leak coefficient alpha is attenuated for the first
~10 token positions (paper section 4.3: 1B-scale models show early-token
recirculation harm — little state to propagate, OOD cost dominates):

    alpha_eff(t) = alpha * (t / 10)   for token positions t = 1..10
    alpha_eff(t) = alpha              for t >= 11

Token positions are 1-indexed. At t = 10 the ramp reaches full alpha
(alpha * 10/10); t = 11 onward is unattenuated. The schedule is FIXED for
all runs (Stage A screen and every Stage-B arm) — recorded at build, never
tuned.

Pure standard library. CPU-testable. The GPU-node TorchBackend applies
alpha_eff per position inside the layer-destination hook.
"""

# Pinned F8 constants ---------------------------------------------------------
RAMP_TOKENS = 10          # linear ramp length (token positions)
RAMP_SCHEDULE_ID = "F8-linear-10"   # manifest/schedule identifier


def alpha_eff(alpha, t):
    """Effective leak coefficient at 1-indexed token position t.

    Args:
        alpha: the nominal leak coefficient (Stage A: 0.10;
               Stage B: one of {0.07, 0.10, 0.15}).
        t: 1-indexed token position (t >= 1).

    Returns:
        alpha * min(t / RAMP_TOKENS, 1.0).

    Raises:
        ValueError: on non-positive position or negative alpha (fail loud;
        the schedule is pinned — out-of-range inputs are caller bugs).
    """
    if t < 1:
        raise ValueError(f"token position t is 1-indexed; got t={t}")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError(f"alpha must be in [0,1]; got {alpha}")
    return alpha * min(t / RAMP_TOKENS, 1.0)


def ramp_vector(alpha, n_tokens):
    """Per-position effective alphas for a block of n_tokens tokens.

    Returns [alpha_eff(alpha, 1), ..., alpha_eff(alpha, n_tokens)].
    Deterministic; used by the GPU-node hook to build the position-wise
    multiplier in one vectorized multiply.
    """
    if n_tokens < 1:
        raise ValueError(f"n_tokens must be >= 1; got {n_tokens}")
    return [alpha_eff(alpha, t) for t in range(1, n_tokens + 1)]


def describe_schedule():
    """One-line pinned schedule description for run manifests."""
    return (f"{RAMP_SCHEDULE_ID}: alpha_eff(t) = alpha*min(t/{RAMP_TOKENS},1), "
            "t 1-indexed; full alpha from t=11 (t=10 already reaches alpha)")
