"""EXP084 Spearman dose-response: exact one-sided permutation p-value.

Signed §5, conjunct (e) (R2): Spearman rank correlation between |κ̂_dir|
and (ΔM_b − ΔM_d), computed over the DEFINED item set (κ̂_dir < −κ_floor),
one-sided > 0 at pilot bar p ≤ 0.10. p by TRUE EXACT permutation (not
Monte Carlo): the full null distribution of D = Σ(rx_i − ry_i)² over S_n
is tabulated in ../exp084_spearman_tables/spearman_null_n{n}.json
(n<=19: tools/gen_spearman_null.c + tools/build_spearman_tables.py;
n=20..24: GPU-node tools/build_spearman_tables_gpu.py (NTT+Ryser) —
see BUILD_NOTES.md). For untied ranks, rho = 1 − 6D/(n(n²−1)), so
P_null(Rho ≥ rho_obs) = P_null(D ≤ d_obs).

Ties: the exact D-distribution assumes untied ranks. If ties are detected
in either variable, ValueError is raised (the protocol's dose-response uses
continuous |κ̂_dir| and margin gains; ties are measure-zero).
"""

import json
import math
import os

TABLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "exp084_spearman_tables")

# Kaggle/GPU-node command that builds the n=20..24 tables (NTT+Ryser).
# tools/build_spearman_tables.py OOMs for n>=20 and must NOT be used there.
GPU_TABLE_BUILD_CMD = (
    "python3 tools/build_spearman_tables_gpu.py --n 20 21 22 23 24 "
    "--out exp084_spearman_tables/"
)

_tables_cache = {}


class MissingSpearmanTableError(FileNotFoundError):
    """Loud pre-execution halt: exact Spearman null table missing for n.

    Law #4-clean resolution (LOG-266 Fix 3): tables n=20..24 are GPU-node
    build artifacts (NTT+Ryser, tools/build_spearman_tables_gpu.py) that must
    exist BEFORE any EXP084 execution — the GPU node does lookup only. If the
    defined set lands at n >= 20 without tables, the runner loud-halts here:
    no verdict, no CONTINUE, no KILL, no HELD. This is NOT an INVALID row —
    the signed protocol has no missing-table row, so no scientific verdict is
    emitted (verdict-clean). It subclasses FileNotFoundError (a table file is
    genuinely absent) but carries the actionable GPU-node build path.
    """


def require_spearman_table(n):
    """Pre-execution gate: the exact null table for defined-set size n must exist.

    Returns the table path after verifying integrity (n matches, d_max equals
    n(n^2-1)/3, counts sum to n!). Raises MissingSpearmanTableError (loud,
    verdict-clean) if the table is missing or corrupt.

    Binding pre-execution condition (LOG-266 Fix 3): the stage-2 model loop
    must call this at startup for the defined-set size BEFORE any verdict
    machinery runs.
    """
    path = os.path.join(TABLES_DIR, f"spearman_null_n{n}.json")
    if not os.path.exists(path):
        raise MissingSpearmanTableError(
            f"Exact Spearman null table missing for n={n}: {path}. "
            f"Tables n=20..24 are GPU-node build artifacts and must be built "
            f"BEFORE any EXP084 execution via the NTT+Ryser path:\n"
            f"  {GPU_TABLE_BUILD_CMD}\n"
            f"(run from the EXP084_newton_duel bundle directory on the GPU node; "
            f"tools/build_spearman_tables.py OOMs for n>=20 and must NOT be used.) "
            f"Loud halt: no verdict emitted (LOG-266 Fix 3; Law #4-clean)."
        )
    with open(path) as f:
        rec = json.load(f)
    dmax = n * (n * n - 1) // 3
    if (rec.get("n") != n or rec.get("d_max") != dmax
            or sum(rec.get("counts", [])) != math.factorial(n)):
        raise MissingSpearmanTableError(
            f"Exact Spearman null table CORRUPT for n={n}: {path} "
            f"(n/d_max/sum!=n! check failed). Rebuild via:\n"
            f"  {GPU_TABLE_BUILD_CMD}"
        )
    return path


def _load_table(n):
    if n not in _tables_cache:
        path = require_spearman_table(n)
        with open(path) as f:
            rec = json.load(f)
        _tables_cache[n] = rec["counts"]
    return _tables_cache[n]


def rankdata(a):
    """1-indexed ranks with average for ties. Returns (ranks, n_ties)."""
    n = len(a)
    order = sorted(range(n), key=lambda i: a[i])
    ranks = [0.0] * n
    n_ties = 0
    i = 0
    while i < n:
        j = i
        while j + 1 < n and a[order[j + 1]] == a[order[i]]:
            j += 1
        avg = (i + 1 + j + 1) / 2.0  # 1-indexed average rank
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        if j > i:
            n_ties += (j - i + 1)
        i = j + 1
    return ranks, n_ties


def spearman_rho(x, y):
    """Spearman rank correlation (Pearson on ranks; handles ties)."""
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    if n < 3:
        raise ValueError(f"n={n} < 3: Spearman undefined")
    rx, _ = rankdata(x)
    ry, _ = rankdata(y)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) *
                    sum((b - my) ** 2 for b in ry))
    if den == 0:
        raise ValueError("zero rank variance (constant input)")
    return num / den


def spearman_exact_p_greater(x, y):
    """Exact one-sided p-value for H1: Spearman rho > 0.

    Uses the tabulated full null distribution of D (sum of squared rank
    differences) for n = len(x). Returns (p_value, rho_obs, d_obs, n).

    p = P_null(D ≤ d_obs) = Σ_{d ≤ d_obs} count[d] / n!, where
    d_obs = Σ(rx_i − ry_i)² (integer when untied).

    Raises:
        ValueError: if ties detected, n < 3, or n > 24.
        MissingSpearmanTableError: if the null table for n is missing or
            corrupt — loud pre-execution halt, no verdict (LOG-266 Fix 3).
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    if n < 3:
        raise ValueError(f"n={n} < 3")
    if n > 24:
        raise ValueError(f"n={n} > 24: no exact table (protocol N=24 max)")
    rx, tx = rankdata(x)
    ry, ty = rankdata(y)
    if tx > 0 or ty > 0:
        raise ValueError(
            f"ties detected (x: {tx}, y: {ty}); exact D-distribution requires "
            "untied ranks"
        )
    d_obs = int(round(sum((a - b) ** 2 for a, b in zip(rx, ry))))
    counts = _load_table(n)
    total = math.factorial(n)
    # sanity: table sums to n!
    assert sum(counts) == total, f"table n={n} corrupt"
    p = sum(counts[d] for d in range(d_obs + 1)) / total
    rho_obs = 1.0 - 6.0 * d_obs / (n * (n * n - 1))
    return p, rho_obs, d_obs, n
