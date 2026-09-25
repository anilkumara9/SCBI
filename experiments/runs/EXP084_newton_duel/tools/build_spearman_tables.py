#!/usr/bin/env python3
"""Generate exact Spearman null tables for n=1..19.

Uses tools/gen_spearman_null (C, subset DP, exact __int128 counts).
D-chunking does NOT reduce peak memory for n >= 20 (the DP must track
[0, d_hi]; n=20 needs 7.8GB at d_hi=1330) — n >= 20 tables are built on
the GPU node via tools/build_spearman_tables_gpu.py (NTT+Ryser), NOT here.
Verifies: sum == n!, symmetry count[d]==count[Dmax-d], D even-only support.
Writes: exp084_spearman_tables/spearman_null_n{n}.json

Each JSON: {"n": n, "d_max": Dmax, "counts": [c0, c1, ..., c_Dmax]}
(counts are Python ints; JSON stores them as numbers.)

Usage: python3 build_spearman_tables.py [n_start] [n_end]
"""
import json
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = HERE
TABLES = os.path.join(HERE, "..", "exp084_spearman_tables")
BIN = os.path.join(TOOLS, "gen_spearman_null")

DMAX = lambda n: n * (n * n - 1) // 3
MEM_TARGET_BYTES = 1_000_000_000  # ~1GB peak per run (conservative; OOM at 2GB)


def binom(n, k):
    return math.comb(n, k)


def chunk_size_for(n):
    """Largest D-chunk such that peak 2-layer memory fits MEM_TARGET."""
    peak_masks = binom(n, n // 2)
    # peak bytes ~= 2 layers * peak_masks * (chunk+1) * 16
    chunk = MEM_TARGET_BYTES // (2 * peak_masks * 16) - 1
    return max(32, min(chunk, DMAX(n)))


def gen_table(n):
    dmax = DMAX(n)
    chunk = chunk_size_for(n)
    print(f"[n={n}] Dmax={dmax}, chunk={chunk}", flush=True)
    counts = [0] * (dmax + 1)
    # symmetry: only need d <= dmax//2; mirror the rest
    need = dmax // 2
    d_lo = 0
    t0 = time.time()
    while d_lo <= need:
        d_hi = min(d_lo + chunk - 1, need)
        # run C program with d_hi (it computes 0..d_hi); take [d_lo..d_hi]
        out = subprocess.run(
            [BIN, str(n), str(d_hi)],
            capture_output=True, text=True, check=True,
        ).stdout.strip().split("\n")
        assert len(out) == d_hi + 1, f"n={n}: got {len(out)} lines, want {d_hi+1}"
        for d in range(d_lo, d_hi + 1):
            counts[d] = int(out[d])
        d_lo = d_hi + 1
    # mirror via symmetry count[d] == count[dmax-d]
    for d in range(need + 1, dmax + 1):
        counts[d] = counts[dmax - d]
    dt = time.time() - t0
    # verify
    total = sum(counts)
    assert total == math.factorial(n), f"n={n}: sum={total} != {math.factorial(n)}"
    assert all(counts[d] == counts[dmax - d] for d in range(dmax + 1)), "symmetry"
    # D is always even: odd counts must be 0
    assert all(counts[d] == 0 for d in range(1, dmax + 1, 2)), "odd D nonzero"
    print(f"[n={n}] OK sum={total} time={dt:.1f}s", flush=True)
    return counts


def main():
    os.makedirs(TABLES, exist_ok=True)
    ns = range(int(sys.argv[1]) if len(sys.argv) > 1 else 1,
               (int(sys.argv[2]) if len(sys.argv) > 2 else 24) + 1)
    for n in ns:
        path = os.path.join(TABLES, f"spearman_null_n{n}.json")
        if os.path.exists(path):
            print(f"[n={n}] exists, skipping", flush=True)
            continue
        counts = gen_table(n)
        with open(path, "w") as f:
            json.dump({"n": n, "d_max": DMAX(n), "counts": counts}, f)
        print(f"[n={n}] wrote {path}", flush=True)


if __name__ == "__main__":
    main()
