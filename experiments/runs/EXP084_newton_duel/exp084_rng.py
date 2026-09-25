"""EXP084 RNG: torch-exclusive random directions + seed-pinned derangement.

PROTOCOL PINS (§4, F8):
- Master seed 20260924; per-item torch Generator seeded 20260924+i.
- torch is the SOLE random-direction library (EXP083 R5 precedent; Law #13).
  numpy is never used for random directions.
- Arm (c) random: s = ρr̂, r̂ isotropic unit (torch.randn normalized).
- Arm (e) permuted-Newton: fixed derangement der(i) from the master seed
  (Fisher-Yates with the master generator); item i receives item der(i)'s s_N.
- Greedy decoding (no sampling randomness in the forward passes).

torch is available on the GPU node, not on the CPU build machine. The
seed-scheme contract (pure, testable here) is separated from the
torch-dependent generation (GPU-node only): generate_r_hat raises a clear
error when torch is absent, and the evaluator test suite asserts that this
module never imports numpy.
"""

MASTER_SEED = 20260924
D_MODEL = 1024  # Pythia-410m hidden size (protocol §1)
N_ITEMS = 24


def item_seed(i):
    """Per-item seed: 20260924 + i (§4, F8)."""
    if not (0 <= i < N_ITEMS):
        raise ValueError(f"item index {i} out of range [0, {N_ITEMS})")
    return MASTER_SEED + i


def item_seeds(n_items=N_ITEMS):
    """Full per-item seed schedule. Deterministic; pairwise distinct."""
    return [item_seed(i) for i in range(n_items)]


def generate_r_hat(i):
    """Draw the isotropic unit random direction r̂_i for arm (c), item i.

    GPU-node only: requires torch. Raises RuntimeError with a clear message
    when torch is unavailable (CPU build machine) — never silently falls
    back to another library.
    """
    try:
        import torch
    except ImportError:
        raise RuntimeError(
            "generate_r_hat requires torch (torch-exclusive per §4/F8); "
            "torch is not installed on this machine. Run on the GPU node."
        )
    g = torch.Generator()
    g.manual_seed(item_seed(i))
    v = torch.randn(D_MODEL, generator=g)
    return v / v.norm(p=2)


def derangement(n_items=N_ITEMS, seed=MASTER_SEED):
    """Fixed derangement for arm (e): der(i) != i for all i.

    Fisher-Yates shuffle with a torch Generator seeded by the master seed;
    rejection-resamples (re-shuffles) until der(i) != i for all i.
    Deterministic given the seed. GPU-node only (requires torch).
    """
    try:
        import torch
    except ImportError:
        raise RuntimeError(
            "derangement requires torch; not installed on this machine. "
            "Run on the GPU node."
        )
    if n_items < 2:
        raise ValueError("derangement needs n_items >= 2")
    g = torch.Generator()
    g.manual_seed(seed)
    while True:
        perm = torch.randperm(n_items, generator=g).tolist()
        if all(p != i for i, p in enumerate(perm)):
            return perm
