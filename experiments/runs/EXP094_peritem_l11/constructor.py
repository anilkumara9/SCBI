"""EXP094 frozen constructor C-1 — per-item task-direction construction.

Signed pre-reg: research/innovation/S4-9_PREREG_DRAFT_2026-09-27.md §2.1.1.
Binding SIGN: LOG-4371 (Law #14 delta re-verification). Frozen per G7.1 —
any change to this file is a new experiment number, never an edit.

ISOLATED FROM BENCH ANNOTATIONS BY CONSTRUCTION (G7.2): every function in
this module accepts only token-ID arrays and activation vectors. Only
token-ID arrays and activation vectors cross any function boundary here —
no annotation of any kind is named, read, or reasoned about. The G7.2 source
scan and the G7.3 swap test audit this mechanically.

DIMENSION NOTE (LOG-4373 erratum): the pre-reg text annotates the L11 space
as R^512; the licensed frozen model (Pythia-410m, LOG-331 pin) has
hidden_size=1024. No formula below hardcodes a dimension — D is read from the
activation vectors at runtime. All operations (subtraction, normalization,
cosine, norm-matching) are dimension-agnostic.
"""

import numpy as np

# Frozen neutral prefix P0 (pre-reg §2.1.1): a constant task-free string —
# never the bench prompt, never annotation-bearing text.
P0_TEXT = "The following passage is shown for reference.\n\n"

# Frozen construction constants (pre-reg §2.1.1, §2.1.2).
NORM_RATIO = 0.0474   # construction setpoint: ||d_i||_2 / ||h_i^B||_2
R_SEED = 94094        # pinned sampling seed for the R-arm directions

CONSTRUCTOR_VERSION = "C-1"


class ConstructionError(Exception):
    """Constructor defect -> construction refused (never a silent zero)."""


def _as_vector(v, name):
    """Coerce to float64 1-D. Rejects cross-item tensors (G7.4)."""
    v = np.asarray(v, dtype=np.float64)
    if v.ndim != 1:
        raise ConstructionError(
            f"{name} must be a single-item vector (ndim == 1); got shape "
            f"{v.shape} — batched/cross-item tensors are forbidden (G7.4).")
    if v.shape[0] == 0:
        raise ConstructionError(f"{name} is empty.")
    return v


def build_per_item_direction(a_vec, b_vec, h_norm_b, ratio=NORM_RATIO):
    """Within-item task-framing contrast direction (pre-reg §2.1.1).

    a_vec: L11 residual-stream activation at the readout-anchor position,
           item under the bench's task framing (Pass A == B-arm pass). (D,)
    b_vec: L11 residual-stream activation at the readout-anchor position,
           the SAME item text under the neutral prefix P0 (Pass B). (D,)
    h_norm_b: ||h_i^B||_2 — the L11 residual norm at the readout-anchor
              position on item i's B-arm pass. Must be > 0.
    ratio: construction setpoint for ||d_i||_2 / ||h_i^B||_2 (frozen 0.0474).

    Returns (d_vec, info) with d_vec = (r_i / ||r_i||_2) * ratio * h_norm_b,
    r_i = a_i - b_i. If ||r_i||_2 == 0 exactly, d_vec is the zero vector and
    info["degenerate_zero"] is True — the item is flagged in the constructor
    manifest and the G5 per-item band catches it downstream
    (perturbation_ratio = 0 sits outside 0.0355–0.0593).
    """
    a = _as_vector(a_vec, "a_vec")
    b = _as_vector(b_vec, "b_vec")
    if a.shape != b.shape:
        raise ConstructionError(
            f"a_vec shape {a.shape} != b_vec shape {b.shape} — the two "
            f"passes must read the same residual space.")
    h_norm_b = float(h_norm_b)
    if not (h_norm_b > 0.0):
        raise ConstructionError(
            f"h_norm_b must be > 0, got {h_norm_b}.")
    ratio = float(ratio)
    if not (ratio > 0.0):
        raise ConstructionError(f"ratio must be > 0, got {ratio}.")

    r = a - b
    r_norm = float(np.linalg.norm(r))
    if r_norm == 0.0:
        d = np.zeros_like(r)
        return d, {
            "r_norm": 0.0,
            "degenerate_zero": True,
            "d_norm": 0.0,
            "perturbation_ratio": 0.0,
            "constructor_version": CONSTRUCTOR_VERSION,
        }
    u = r / r_norm
    d = u * (ratio * h_norm_b)
    d_norm = float(np.linalg.norm(d))
    return d, {
        "r_norm": r_norm,
        "degenerate_zero": False,
        "d_norm": d_norm,
        # By construction == ratio up to float64 rounding; the G5 probe
        # verifies the injected delivery, not this identity.
        "perturbation_ratio": d_norm / h_norm_b,
        "constructor_version": CONSTRUCTOR_VERSION,
    }


def build_random_direction(d_norm, dim, rng):
    """Norm-matched isotropic random direction (pre-reg §2.1.2).

    g_i_raw ~ N(0, I_dim); normalized to unit norm, then scaled so
    ||g_i||_2 == ||d_i||_2 (the norm tie). Task-free by construction.
    rng: numpy Generator (seed pinned in the environment manifest).
    """
    d_norm = float(d_norm)
    if not (d_norm >= 0.0):
        raise ConstructionError(f"d_norm must be >= 0, got {d_norm}.")
    dim = int(dim)
    if dim <= 0:
        raise ConstructionError(f"dim must be > 0, got {dim}.")
    z = np.asarray(rng.normal(size=dim), dtype=np.float64)
    z_norm = float(np.linalg.norm(z))
    if z_norm == 0.0:  # probability-zero event; fail loud, never silent
        raise ConstructionError("isotropic draw was exactly zero.")
    return (z / z_norm) * d_norm
