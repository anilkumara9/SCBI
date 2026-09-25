#!/usr/bin/env python3
"""Build exact Spearman null tables for n=20..24 on the GPU node (NTT+Ryser).

Binding pre-execution condition (LOG-266 Fix 3): tables n=20..24 MUST be
built via this path BEFORE any EXP084 execution. The GPU node does table
lookup only (no recomputation). tools/build_spearman_tables.py OOMs for
n>=20 and must NOT be used.

Kaggle-side command (run from the EXP084_newton_duel bundle directory):
    !python3 tools/build_spearman_tables_gpu.py --n 20 21 22 23 24 \\
        --out exp084_spearman_tables/

Requires: torch with CUDA (CPU fallback works but is much slower; the
script prints a time estimate and proceeds only with --device cpu given
explicitly... actually CPU is allowed via --device cpu).

Method (exact, no Monte Carlo):
  We need c_s = #{pi in S_n : sum_i i*pi_i = s} for
  s in [s_min, s_max], s_min = n(n+1)(n+2)/6, s_max = n(n+1)(2n+1)/6.
  D = sum_i (i - pi_i)^2 = 2*(s_max - s), so the D-distribution follows.

  Let P(u) = sum_s c_s u^s = perm(A), A[i][j] = u^{i*j} (1-indexed).
  Ryser: P(u) = sum_{S subset [n]} (-1)^{n-|S|} prod_{i=1}^n (sum_{j in S} u^{ij}).
  Put Q(u) = u^{-s_min} P(u) = sum_{w=0}^{W} c_{s_min+w} u^w, W = n(n^2-1)/6
  (deg Q <= 2300 for n=24). With M = 4096 > W and primitive M-th root z in
  F_p: Qhat[k] = z^{-k s_min} sum_S (-1)^{n-|S|} prod_i (sum_{j in S} z^{kij}).
  One inverse NTT (size M) recovers the coefficients mod p.

  Exactness: each coefficient <= 24! < 2^79.3. We run the whole pipeline mod
  three NTT primes p1=998244353, p2=1004535809, p3=104857601
  (p1*p2*p3 > 24!) and combine by CRT (Garner) to the exact integer.
  All modular products are < p^2 < 2^60, exact in int64. Subset sums are
  accumulated unreduced (< n*p < 2^35) and reduced once per tile.

  Tiling: masks in batches of --batch-masks (default 16384), k in chunks of
  --k-chunk (default 512); subset sums via a single dense einsum
  F[b,i,k] = sum_j bits[b,j] * z^{k*i*j}.

Integrity checks per n (all must pass or the table is NOT written):
  sum == n!; counts[0] == 1 (D=0 <-> identity); counts[d] == counts[dmax-d];
  odd d -> 0; dmax == n(n^2-1)/3.

Output JSON schema (identical to tools/build_spearman_tables.py):
  {"n": n, "d_max": Dmax, "counts": [c0, c1, ..., c_Dmax]}

Self-test (validates the full pipeline incl. CRT on this machine):
    python3 tools/build_spearman_tables_gpu.py --selftest
  Runs n=1..8 through the torch pipeline and cross-checks every count
  against itertools.permutations brute force, plus an NTT roundtrip check.
"""

import argparse
import json
import math
import os
import sys
import time

# NTT primes: each = 1 mod 4096; product > 24!
PRIMES = (998244353, 1004535809, 104857601)
M = 4096  # NTT size; must exceed W = n(n^2-1)/6 (2300 at n=24)


def check_ntt_size(n):
    w = n * (n * n - 1) // 6
    if w >= M:
        raise ValueError(f"n={n}: W={w} >= NTT size {M}; increase M")
    return w


def primitive_root(p):
    """Smallest primitive root of prime p (p-1 factored by trial division)."""
    phi = p - 1
    factors = set()
    d = phi
    f = 2
    while f * f <= d:
        if d % f == 0:
            factors.add(f)
            while d % f == 0:
                d //= f
        f += 1 if f == 2 else 2
    if d > 1:
        factors.add(d)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    raise RuntimeError(f"no primitive root found for {p}")


def ntt(a, invert, p, omega):
    """Iterative NTT over F_p (torch int64; products < p^2 < 2^63 stay exact).

    a: (M,) int64 tensor. omega: primitive M-th root mod p.
    """
    import torch
    n = a.numel()
    # bit-reversal permutation (CPU, tiny)
    rev = [0] * n
    bits = n.bit_length() - 1
    for i in range(n):
        r = 0
        x = i
        for _ in range(bits):
            r = (r << 1) | (x & 1)
            x >>= 1
        rev[i] = r
    a = a[torch.tensor(rev, dtype=torch.long, device=a.device)].clone()
    length = 2
    while length <= n:
        wlen = pow(omega, n // length, p)
        if invert:
            wlen = pow(wlen, p - 2, p)
        half = length // 2
        ws = torch.tensor([pow(wlen, j, p) for j in range(half)],
                          dtype=torch.int64, device=a.device)
        a = a.reshape(-1, length)
        u = a[:, :half]
        v = (a[:, half:] * ws) % p
        a = torch.cat([((u + v) % p), ((u - v + p) % p)], dim=1)
        a = a.reshape(n)
        length <<= 1
    if invert:
        a = (a * pow(n, p - 2, p)) % p
    return a


def qhat_mod_prime(n, p, s_min, device, batch_masks, k_chunk):
    """Compute Qhat[k] = Q(z^k) mod p for k=0..M-1 (Ryser, tiled, torch int64)."""
    import torch
    W = check_ntt_size(n)
    g = primitive_root(p)
    omega = pow(g, (p - 1) // M, p)
    assert pow(omega, M // 2, p) == p - 1, f"order check failed for p={p}"
    Ep = torch.tensor([pow(omega, e, p) for e in range(M)],
                      dtype=torch.int64, device=device)
    acc = torch.zeros(M, dtype=torch.int64, device=device)
    nmasks = 1 << n
    ii = torch.arange(1, n + 1, dtype=torch.int64, device=device)
    jj = torch.arange(1, n + 1, dtype=torch.int64, device=device)
    bitpos = torch.arange(n, dtype=torch.int64, device=device)
    n_batches = 0
    for b0 in range(0, nmasks, batch_masks):
        B = min(batch_masks, nmasks - b0)
        masks = torch.arange(b0, b0 + B, dtype=torch.int64, device=device)
        bits = ((masks[:, None] >> bitpos[None, :]) & 1)  # (B, n)
        # (-1)^{n-|S|}: +1 iff parity(|S|) == parity(n)
        sgn = torch.where((bits.sum(1) & 1) == (n & 1),
                          torch.ones(B, dtype=torch.int64, device=device),
                          -torch.ones(B, dtype=torch.int64, device=device))
        for kc0 in range(0, M, k_chunk):
            K = min(k_chunk, M - kc0)
            Kvec = torch.arange(kc0, kc0 + K, dtype=torch.int64, device=device)
            # C[j,i,k] = z^{k*i*j}; entries < p
            exp_idx = (Kvec[None, None, :] * ii[None, :, None]
                       * jj[:, None, None]) % M
            C = Ep[exp_idx]  # (n, n, K)
            F = torch.einsum('bj,jik->bik', bits, C)  # (B,n,K), < n*p
            F = F % p
            G = torch.ones(B, K, dtype=torch.int64, device=device)
            for i in range(n):
                G = (G * F[:, i, :]) % p  # products < p^2 < 2^63
            acc[kc0:kc0 + K] += (sgn[:, None] * G).sum(0)
        n_batches += 1
    kk = torch.arange(M, dtype=torch.int64, device=device)
    Qhat = (((acc % p) + p) % p) * Ep[((-kk * s_min) % M)] % p
    return Qhat, W


def crt3(r1, r2, r3, p1, p2, p3):
    """Exact CRT for three moduli (Python ints)."""
    t12 = ((r2 - r1) * pow(p1, p2 - 2, p2)) % p2
    x12 = r1 + p1 * t12
    t123 = ((r3 - x12) * pow((p1 * p2) % p3, p3 - 2, p3)) % p3
    return x12 + p1 * p2 * t123


def build_counts(n, device, batch_masks, k_chunk, verbose=True):
    """Exact D-distribution counts for S_n. Returns [c_0..c_dmax]."""
    import torch
    s_min = n * (n + 1) * (n + 2) // 6
    s_max = n * (n + 1) * (2 * n + 1) // 6
    W = s_max - s_min
    dmax = 2 * W
    assert dmax == n * (n * n - 1) // 3
    qmod = []
    for p in PRIMES:
        t0 = time.time()
        Qhat, _ = qhat_mod_prime(n, p, s_min, device, batch_masks, k_chunk)
        g = primitive_root(p)
        omega = pow(g, (p - 1) // M, p)
        q = ntt(Qhat, invert=True, p=p, omega=omega)
        qmod.append([int(v) for v in q[:W + 1].tolist()])
        if verbose:
            print(f"  [n={n}] prime {p}: {time.time()-t0:.1f}s", flush=True)
    p1, p2, p3 = PRIMES
    assert p1 * p2 * p3 > math.factorial(n), "CRT moduli too small"
    counts = [0] * (dmax + 1)
    for w in range(W + 1):
        qw = crt3(qmod[0][w], qmod[1][w], qmod[2][w], p1, p2, p3)
        s = s_min + w
        D = 2 * (s_max - s)
        counts[D] = qw
    return counts


def check_integrity(n, counts):
    """Integrity checks; raises AssertionError on failure."""
    dmax = n * (n * n - 1) // 3
    assert len(counts) == dmax + 1, f"len {len(counts)} != {dmax+1}"
    total = sum(counts)
    assert total == math.factorial(n), f"sum={total} != {n}!"
    assert counts[0] == 1, f"counts[0]={counts[0]} != 1 (D=0 <-> identity)"
    assert all(counts[d] == 0 for d in range(1, dmax + 1, 2)), "odd D nonzero"
    assert all(counts[d] == counts[dmax - d] for d in range(dmax + 1)), \
        "symmetry violated"
    return dmax


def brute_counts(n):
    """Reference: full enumeration over S_n (n<=8 only)."""
    import itertools
    dmax = n * (n * n - 1) // 3
    counts = [0] * (dmax + 1)
    for perm in itertools.permutations(range(1, n + 1)):
        D = sum((i + 1 - p) ** 2 for i, p in enumerate(perm))
        counts[D] += 1
    return counts


def selftest(device, batch_masks=1 << 10, k_chunk=512):
    """End-to-end validation: torch pipeline vs brute force for n=1..8."""
    import torch
    print("selftest: NTT roundtrip check", flush=True)
    p = PRIMES[0]
    g = primitive_root(p)
    omega = pow(g, (p - 1) // M, p)
    torch.manual_seed(0)
    a = torch.randint(0, p, (M,), dtype=torch.int64, device=device)
    b = ntt(ntt(a, False, p, omega), True, p, omega)
    assert torch.equal(a % p, b), "NTT roundtrip failed"
    print("selftest: NTT roundtrip OK", flush=True)
    for n in range(1, 9):
        t0 = time.time()
        counts = build_counts(n, device, batch_masks, k_chunk, verbose=False)
        ref = brute_counts(n)
        assert counts == ref, f"n={n}: pipeline != brute force"
        check_integrity(n, counts)
        print(f"selftest: n={n} OK ({time.time()-t0:.1f}s)", flush=True)
    print("SELFTEST PASS: torch NTT+Ryser pipeline matches brute force n=1..8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n", nargs="+", type=int, default=[],
                    help="n values to build (e.g. --n 20 21 22 23 24)")
    ap.add_argument("--out", default=None,
                    help="output dir (default: exp084_spearman_tables/ next to tools/)")
    ap.add_argument("--device", default="auto",
                    help="auto|cuda|cpu (auto uses cuda if available)")
    ap.add_argument("--batch-masks", type=int, default=1 << 14)
    ap.add_argument("--k-chunk", type=int, default=512)
    ap.add_argument("--selftest", action="store_true",
                    help="validate pipeline vs brute force (n=1..8), then exit")
    ap.add_argument("--skip-existing", action="store_true", default=True)
    ap.add_argument("--no-skip-existing", action="store_false",
                    dest="skip_existing")
    args = ap.parse_args()

    try:
        import torch
    except ImportError:
        sys.exit("FATAL: torch is required (GPU node). pip install torch "
                 "--index-url https://download.pytorch.org/whl/cu121")

    if args.device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device
    if device == "cpu":
        print("WARNING: CPU device — n>=20 will take hours; prefer a GPU node.",
              flush=True)

    if args.selftest:
        selftest(device)
        return

    if not args.n:
        sys.exit("nothing to do: pass --n values or --selftest")
    for n in args.n:
        if not 1 <= n <= 24:
            sys.exit(f"FATAL: n={n} out of supported range 1..24")

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = args.out or os.path.join(here, "..", "exp084_spearman_tables")
    os.makedirs(outdir, exist_ok=True)

    for n in args.n:
        path = os.path.join(outdir, f"spearman_null_n{n}.json")
        if args.skip_existing and os.path.exists(path):
            print(f"[n={n}] exists, skipping", flush=True)
            continue
        t0 = time.time()
        print(f"[n={n}] NTT+Ryser on {device} ...", flush=True)
        counts = build_counts(n, device, args.batch_masks, args.k_chunk)
        dmax = check_integrity(n, counts)
        with open(path, "w") as f:
            json.dump({"n": n, "d_max": dmax, "counts": counts}, f)
        print(f"[n={n}] OK sum={math.factorial(n)} dmax={dmax} "
              f"time={time.time()-t0:.1f}s wrote {path}", flush=True)


if __name__ == "__main__":
    main()
