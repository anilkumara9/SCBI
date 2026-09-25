#!/usr/bin/env python3
"""EXP088 pinned RNG (F2 compute-matched RAND control).

Torch-exclusive (no numpy import; asserted in tests) — mirrors the
exp084_rng.py precedent. The F2 RAND control needs a FIXED random unit
vector drawn ONCE per run with a pinned seed, scaled to the destination
norm ||h_d|| at injection time (the scaling happens in the runner's leak
operator, not here — this module only draws the unit vector).

GPU-node only: raises RuntimeError without torch. The CPU mock harness
uses its own pure-Python LCG fixture and never claims protocol-RNG status.
"""

# Pinned seeds (Law #13) ------------------------------------------------------
MASTER_SEED = 20260924   # program master-seed convention (EXP084 precedent)
RAND_SEED = 20260924     # F2: the fixed random unit vector's draw seed
                         # (drawn once per run; recorded in the manifest)


def draw_rand_unit_vector(dim, seed=RAND_SEED):
    """Draw the F2 fixed random unit vector (GPU node only).

    Standard-normal entries from a torch.Generator seeded ONCE per run with
    the pinned RAND_SEED, normalized to unit L2 norm. Deterministic given
    (dim, seed); the runner calls this exactly once per run and reuses the
    vector for every item and every token position (F2: "drawn once per
    run").

    Raises RuntimeError without torch (the build machine has no torch —
    the mock harness supplies its own fixture).
    """
    try:
        import torch
    except ImportError as e:
        raise RuntimeError(
            "draw_rand_unit_vector requires torch (GPU node only)") from e
    if dim < 1:
        raise ValueError(f"dim must be >= 1; got {dim}")
    g = torch.Generator().manual_seed(seed)
    v = torch.randn(dim, generator=g)
    n = v.norm().item()
    if n == 0.0:
        raise RuntimeError("F2 RNG drew a zero vector (measure-zero event); "
                           "halting loud rather than injecting a no-op")
    return v / n
