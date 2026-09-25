"""EXP083 (R1 RCPA kill pilot) — ĝ_i null-control generator (§4 A_g, R5).

PROTOCOL PIN (R5): **torch is the sole ĝ_i generator library** — numpy is
not used for ĝ_i (Law #13). Per-item construction:

    g_i = torch.Generator(); g_i.manual_seed(20260924 + i)
    v   = torch.randn(1024, generator=g_i)
    ĝ_i = v / ||v||_2

Master seed S0 = 20260924; per-item seed = S0 + i. Greedy decoding.
Matched norm by construction (||ĝ_i||_2 = 1 = ||r̂_i||_2).

torch is available on the GPU node, not on the CPU build machine. The
seed-scheme contract (pure, testable here) is separated from the
torch-dependent generation (GPU-node only): generate_g_hat raises a clear
error when torch is absent, and the evaluator test suite asserts that this
module never imports numpy (R5 exclusivity check).
"""

MASTER_SEED = 20260924
D_MODEL = 1024


def g_hat_seed(i):
    """Per-item seed for the ĝ_i generator: 20260924 + i (§4, R5)."""
    if i < 0:
        raise ValueError("item index must be non-negative")
    return MASTER_SEED + i


def g_hat_seeds(n_items):
    """The full per-item seed schedule. Deterministic; pairwise distinct."""
    return [g_hat_seed(i) for i in range(n_items)]


def generate_g_hat(i):
    """Draw the unit-norm isotropic Gaussian direction ĝ_i for item i.

    GPU-node only: requires torch. Raises RuntimeError with a clear message
    when torch is unavailable (CPU build machine) — never silently falls
    back to another library (R5).
    """
    try:
        import torch
    except ImportError:
        raise RuntimeError(
            "generate_g_hat requires torch (R5: torch is the sole ĝ_i "
            "generator library); torch is not installed on this machine. "
            "Run on the GPU node.")
    g = torch.Generator()
    g.manual_seed(g_hat_seed(i))
    v = torch.randn(D_MODEL, generator=g)
    return v / v.norm(p=2)


def check_unit_norm(vec, tol=1e-6):
    """Contract check: ||ĝ_i||_2 == 1 (matched norm by construction, §4)."""
    import math
    n = math.sqrt(sum(float(x) * float(x) for x in vec))
    return abs(n - 1.0) <= tol
