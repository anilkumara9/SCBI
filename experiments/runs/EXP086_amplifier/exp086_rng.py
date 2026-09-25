"""EXP086 RNG: torch-exclusive random directions + seed-pinned Stage-2 derangement.

PROTOCOL PINS (§4, §13):
- Master seed 20260924; v̂_rand = fresh uniform unit vector per item per norm
  (seeded); Stage-2 permuted arm uses a fixed derangement (seeded).
- torch is the SOLE random-direction library (EXP083/EXP084 R5 precedent;
  Law #13). numpy is never used for random directions.

torch is available on the execution node, not on the CPU build machine. The
seed-scheme contract (pure, testable here) is separated from the
torch-dependent generation (execution-node only): the torch functions raise
a clear RuntimeError when torch is absent — never silently fall back to
another library.
"""

MASTER_SEED = 20260924
D_MODEL = 1024  # Pythia-410m hidden size (protocol D1)
N_ITEMS = 60
N_NORMS = 2     # {0.15, 0.45} x ||h||


def item_norm_seed(i, norm_idx):
    """Seed for v̂_rand on item i, norm index norm_idx in {0,1}.

    Schedule: MASTER_SEED + 1000*i + norm_idx — pairwise distinct across
    items and norms, deterministic, documented in the env manifest.
    """
    if not (0 <= i < N_ITEMS):
        raise ValueError(f"item index {i} out of range [0, {N_ITEMS})")
    if norm_idx not in (0, 1):
        raise ValueError(f"norm_idx {norm_idx} not in {{0, 1}}")
    return MASTER_SEED + 1000 * i + norm_idx


def seed_schedule(n_items=N_ITEMS):
    """Full (item, norm) seed schedule. Deterministic; pairwise distinct."""
    seeds = [item_norm_seed(i, k) for i in range(n_items) for k in (0, 1)]
    if len(set(seeds)) != len(seeds):
        raise AssertionError("seed schedule collision (impossible by construction)")
    return seeds


def generate_v_rand(i, norm_idx):
    """Draw the isotropic unit random direction for item i, norm norm_idx.

    Execution-node only: requires torch. Raises RuntimeError with a clear
    message when torch is unavailable (CPU build machine) — never silently
    falls back to another library.
    """
    try:
        import torch
    except ImportError:
        raise RuntimeError(
            "generate_v_rand requires torch (torch-exclusive per §4/F8); "
            "torch is not installed on this machine. Run on the execution node."
        )
    g = torch.Generator()
    g.manual_seed(item_norm_seed(i, norm_idx))
    v = torch.randn(D_MODEL, generator=g)
    return v / v.norm(p=2)


def derangement(n_items=N_ITEMS, seed=MASTER_SEED):
    """Fixed derangement for the Stage-2 permuted-v̂_1 arm: der(i) != i.

    Fisher-Yates shuffle with a torch Generator seeded by the master seed;
    rejection-resamples (re-shuffles) until der(i) != i for all i.
    Deterministic given the seed. Execution-node only (requires torch).
    """
    try:
        import torch
    except ImportError:
        raise RuntimeError(
            "derangement requires torch; not installed on this machine. "
            "Run on the execution node."
        )
    if n_items < 2:
        raise ValueError("derangement needs n_items >= 2")
    g = torch.Generator()
    g.manual_seed(seed)
    while True:
        perm = torch.randperm(n_items, generator=g).tolist()
        if all(p != i for i, p in enumerate(perm)):
            return perm
