#!/usr/bin/env python3
"""EXP084 evaluator test suite (CPU, synthetic fixtures).

Tests the protocol statistics from scratch and exercises dead-apparatus
refusal. GPU-node paths (torch, model weights) are NOT executed here.
All tests are deterministic; no randomness beyond pinned seeds.

Run: python3 test_exp084.py
Exit 0 iff all tests pass. Prints TAP-like lines.
"""

import math
import os
import sys
import hashlib
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import exp084_guards as G
import exp084_rng as R
import exp084_statistics as S
import exp084_spearman as SP
from run_exp084 import PassBudget, adjudicate

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"ok - {name}")
    else:
        FAIL += 1
        print(f"FAIL - {name} {detail}")


# --- 1. Guards (§3) ---------------------------------------------------------
check("guard: defined iff kappa < -1e-6",
      G.is_newton_defined(-2e-6) and not G.is_newton_defined(-1e-6)
      and not G.is_newton_defined(0.0) and not G.is_newton_defined(5e-6))
check("guard: exclusion split convex-uphill",
      G.classify_exclusion(3e-6) == "convex-uphill")
check("guard: exclusion split too-flat (interval)",
      G.classify_exclusion(-5e-7) == "too-flat"
      and G.classify_exclusion(0.0) == "too-flat"
      and G.classify_exclusion(9e-7) == "too-flat")
try:
    G.classify_exclusion(-2e-6)
    check("guard: classify_exclusion raises on defined", False)
except ValueError:
    check("guard: classify_exclusion raises on defined", True)
check("guard: INVALID(iii) at 11/24",
      G.check_invalid_iii(11) is True)
check("guard: INVALID(iii) clears at 12/24",
      G.check_invalid_iii(12) is False)
check("guard: newton_step_length = ||g||/|k|",
      abs(G.newton_step_length(2.0, -0.5) - 4.0) < 1e-12)
try:
    G.newton_step_length(1.0, -5e-7)
    check("guard: step raises when undefined", False)
except ValueError:
    check("guard: step raises when undefined", True)

# --- 2. Wilcoxon exact (§5) --------------------------------------------------
# Fixture: strong positive shift, n=10, no ties (distinct |d_i|).
xc = [0.1 * i for i in range(10)]
xa = [c + 0.5 + 0.01 * i for i, c in enumerate(xc)]  # diffs 0.5..0.59 distinct
p, w, n = S.wilcoxon_signed_rank_greater(xa, xc)
# All diffs > 0 -> W+ = 55 (max), p = 1/1024
check("wilcoxon: all-positive gives W+=55, p=1/1024",
      w == 55 and abs(p - 1 / 1024) < 1e-12, f"w={w} p={p}")
# Symmetric null-ish data: p should be large (distinct |d_i|)
y1 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
y2 = [1.11, 1.87, 3.23, 3.71, 5.15, 5.83]  # diffs: -0.11,+0.13,-0.23,+0.29,-0.15,+0.17
p2, _, _ = S.wilcoxon_signed_rank_greater(y1, y2)
check("wilcoxon: null-ish data p > 0.10", p2 > 0.10, f"p={p2}")
# Brute-force cross-check on a small fixture (n=7, distinct |d_i|)
import itertools
xb = [0.3, -0.11, 0.5, 0.2, -0.4, 0.6, 0.1]
yb = [0.0] * 7
pb, wb, nb = S.wilcoxon_signed_rank_greater(xb, yb)
diffs = [a - b for a, b in zip(xb, yb)]
ranks = sorted(range(7), key=lambda i: abs(diffs[i]))
w_obs = sum(r + 1 for r in range(7) if diffs[ranks[r]] > 0)
cnt = sum(1 for s in itertools.product([-1, 1], repeat=7)
          if sum((r + 1) for r in range(7) if s[r] > 0) >= w_obs)
p_brute = cnt / 128
check("wilcoxon: matches brute force (n=7)",
      abs(pb - p_brute) < 1e-12 and wb == w_obs, f"{pb} vs {p_brute}")
# Ties raise
try:
    S.wilcoxon_signed_rank_greater([1.0, 1.0, 2.0, 3.0, 4.0, 5.0],
                                   [0.0] * 6)
    check("wilcoxon: ties raise ValueError", False)
except ValueError:
    check("wilcoxon: ties raise ValueError", True)
# n_eff < 6 raises
try:
    S.wilcoxon_signed_rank_greater([1.0, 2.0], [0.0, 0.0])
    check("wilcoxon: n_eff<6 raises", False)
except ValueError:
    check("wilcoxon: n_eff<6 raises", True)

# --- 3b. HL CI exactness vs independent test-inversion (LOG-266 Fix 1) --------
# Clear positive shift: CI should lie above 0
lo, hi, hl = S.hodges_lehmann_ci(xa, xc)
check("HL: positive shift CI above 0", lo > 0, f"[{lo}, {hi}]")
# The old code returned [walsh[c+1], walsh[m-c-2]] (one order statistic too
# narrow per side). This test compares the reported endpoints against an
# INDEPENDENT exact test-inversion: theta is accepted iff neither one-sided
# exact Wilcoxon tail rejects at alpha/2. Verified during development that
# this test FAILS on the old indices (old lo-eps stays accepted).
xd8 = [0.50, 0.61, 0.72, 0.83, 0.94, 1.05, 1.16, 1.27]
lo8, hi8, _ = S.hodges_lehmann_ci(xd8, [0.0] * 8)


def _accept_shift(theta, xs, alpha=0.05):
    d = [x - theta for x in xs]
    pg, _, _ = S.wilcoxon_signed_rank_greater(d, [0.0] * len(d))
    pl, _, _ = S.wilcoxon_signed_rank_greater([-v for v in d], [0.0] * len(d))
    return min(pg, pl) > alpha / 2


_eps8 = 1e-4
_inv = {
    "lo+eps": _accept_shift(lo8 + _eps8, xd8),
    "lo-eps": _accept_shift(lo8 - _eps8, xd8),
    "hi-eps": _accept_shift(hi8 - _eps8, xd8),
    "hi+eps": _accept_shift(hi8 + _eps8, xd8),
    "interior": _accept_shift(lo8 + 0.37 * (hi8 - lo8), xd8),
}
check("HL: endpoints match exact test-inversion",
      _inv == {"lo+eps": True, "lo-eps": False, "hi-eps": True,
               "hi+eps": False, "interior": True},
      str(_inv))
# KILL prong: fires only when upper < 0.01
xb2 = [0.001 * i for i in range(12)]
yb2 = [0.001 * i + 0.0005 + 0.00001 * i for i in range(12)]  # diffs distinct, negative
fires, clo, chi = S.kill_effect_prong(xb2, yb2)
check("KILL prong: fires on negative diff with tight CI",
      fires and chi < 0.01, f"fires={fires} hi={chi}")

# --- 4. Spearman exact (§5 conjunct e) ---------------------------------------
# Perfect positive correlation, n=12: D=0, p = 1/12!
x12 = list(range(12))
y12 = list(range(12))
p_sp, rho_sp, d_sp, n_sp = SP.spearman_exact_p_greater(x12, y12)
check("spearman: perfect rho=1, D=0",
      abs(rho_sp - 1.0) < 1e-12 and d_sp == 0)
check("spearman: p = 1/12!",
      abs(p_sp - 1 / math.factorial(12)) < 1e-18, f"p={p_sp}")
# Perfect negative: D=Dmax, p = 1.0 (P(D <= Dmax))
y12r = list(reversed(range(12)))
p_spr, rho_spr, d_spr, _ = SP.spearman_exact_p_greater(x12, y12r)
check("spearman: perfect negative rho=-1, p=1.0",
      abs(rho_spr + 1.0) < 1e-12 and abs(p_spr - 1.0) < 1e-12)
# Brute-force cross-check n=6
import itertools as it
x6 = [3, 1, 4, 1.5, 5, 2]
y6 = [2, 3, 1, 5, 4, 1.5]
# (no ties by construction)
p6, rho6, d6, _ = SP.spearman_exact_p_greater(x6, y6)
rx = SP.rankdata(x6)[0]
ry = SP.rankdata(y6)[0]
d_brute = sum((a - b) ** 2 for a, b in zip(rx, ry))
cnt6 = 0
for perm in it.permutations(range(1, 7)):
    dd = sum((a - b) ** 2 for a, b in zip(rx, perm))
    if dd <= d_brute:
        cnt6 += 1
p6_brute = cnt6 / math.factorial(6)
check("spearman: matches brute force (n=6)",
      abs(p6 - p6_brute) < 1e-12 and d6 == int(round(d_brute)),
      f"{p6} vs {p6_brute}")
# Ties raise
try:
    SP.spearman_exact_p_greater([1, 2, 2, 3], [1, 2, 3, 4])
    check("spearman: ties raise ValueError", False)
except ValueError:
    check("spearman: ties raise ValueError", True)
# Table integrity: n=12 sums to 12!
import json
tbl = json.load(open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "exp084_spearman_tables", "spearman_null_n12.json")))
check("spearman table n=12: sums to 12!",
      sum(tbl["counts"]) == math.factorial(12))

# --- 4b. Table-presence gate (LOG-266 Fix 3) ----------------------------------
# require_spearman_table: present table passes with integrity verified.
p12 = SP.require_spearman_table(12)
check("table gate: n=12 present and valid",
      p12.endswith("spearman_null_n12.json"), p12)
# Missing table (n=20..24 not precomputed): LOUD halt, no bare abort.
try:
    SP.require_spearman_table(20)
    check("table gate: n=20 missing raises loudly", False)
except SP.MissingSpearmanTableError as e:
    msg = str(e)
    check("table gate: n=20 missing raises loudly",
          "build_spearman_tables_gpu.py" in msg and "NTT+Ryser" in msg
          and "no verdict" in msg, msg[:80])
# The loud error keeps FileNotFoundError semantics (a table file is absent).
try:
    SP.require_spearman_table(21)
    check("table gate: keeps FileNotFoundError lineage", False)
except FileNotFoundError:
    check("table gate: keeps FileNotFoundError lineage", True)
# The exact-p path surfaces the same loud halt (not a bare abort).
try:
    SP.spearman_exact_p_greater(list(range(20)), list(range(20)))
    check("table gate: exact-p path loud-halts at n=20", False)
except SP.MissingSpearmanTableError as e:
    check("table gate: exact-p path loud-halts at n=20",
          "build_spearman_tables_gpu.py" in str(e))

# --- 5. RNG contract (§4, F8) -------------------------------------------------
check("rng: master seed pinned", R.MASTER_SEED == 20260924)
seeds = R.item_seeds(24)
check("rng: 24 distinct per-item seeds",
      len(set(seeds)) == 24 and seeds[0] == 20260924)
try:
    R.item_seed(24)
    check("rng: item_seed(24) raises", False)
except ValueError:
    check("rng: item_seed(24) raises", True)
# torch-exclusivity: module source must not import numpy
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "exp084_rng.py")).read()
check("rng: no numpy import (torch-exclusive)",
      "import numpy" not in src and "from numpy" not in src)
# generate_r_hat raises clearly without torch
try:
    R.generate_r_hat(0)
    # torch may exist; if it returns, check unit norm contract instead
    check("rng: generate_r_hat without torch raises (or torch present)",
          True)
except RuntimeError as e:
    check("rng: generate_r_hat without torch raises (or torch present)",
          "torch" in str(e).lower())

# --- 6. Verdict precedence (§7) -----------------------------------------------
base = dict(n_defined=20, sens_p=0.01,
            p_newton_vs_gdcostfair=0.01, p_newton_vs_random=0.01,
            p_newton_vs_gd1=0.01, p_newton_vs_permuted=0.01,
            spearman_p=0.05, median_b_minus_d=0.02, hl_hi=0.03,
            median_b_minus_a=0.02, hl_hi_b_minus_a=0.03)
v, ev, _, sec = adjudicate(base)
check("verdict: full conjuncts -> CONTINUE", v == "CONTINUE", v)
check("verdict: CONTINUE carries no narrow secondary", sec is None, str(sec))
b2 = dict(base, spearman_p=0.50)
v, ev, _, sec = adjudicate(b2)
check("verdict: (e) fails -> HELD(win-not-curvature-explained)",
      v == "HELD(win-not-curvature-explained)", v)
b3 = dict(base, p_newton_vs_random=0.50)
v, ev, _, sec = adjudicate(b3)
check("verdict: (b) fails -> HELD(step-noise)",
      v == "HELD(step-noise)", v)
b4 = dict(base, n_defined=11)
v, ev, _, sec = adjudicate(b4)
check("verdict: INVALID(iii) preempts all",
      v == "INVALID/UNDEFINED-LANDSCAPE", v)
b5 = dict(base, sens_p=0.50, n_defined=20)
v, ev, _, sec = adjudicate(b5)
check("verdict: INVALID(iv) sensitivity preempts scientific rows",
      v == "INVALID/UNINFORMATIVE-PROXY", v)
b6 = dict(base, p_newton_vs_gdcostfair=0.60, spearman_p=0.60,
          median_b_minus_d=-0.005, hl_hi=0.004)
v, ev, _, sec = adjudicate(b6)
check("verdict: KILL fires on median<=0 and HL upper<0.01",
      v == "KILL(flagship, cost-fair)", v)
b7 = dict(base, p_newton_vs_gdcostfair=0.60, spearman_p=0.60,
          median_b_minus_d=0.02, hl_hi=0.05)
v, ev, _, sec = adjudicate(b7)
check("verdict: straddle -> HELD(straddle)",
      v == "HELD(straddle)", v)
check("verdict: straddle carries no narrow secondary when narrow idle",
      sec is None, str(sec))

# --- 6b. Narrow KILL row (§7 "KILL (directional, narrow)", LOG-266 Fix 2) ----
# Fires: narrow criteria hold on ΔM_b − ΔM_a while primary is straddle —
# previously misreported as bare HELD(straddle).
bn = dict(base, p_newton_vs_gdcostfair=0.60, spearman_p=0.60,
          median_b_minus_d=0.02, hl_hi=0.05,
          median_b_minus_a=-0.004, hl_hi_b_minus_a=0.003)
v, ev, _, sec = adjudicate(bn)
check("verdict: narrow KILL fires alongside HELD(straddle)",
      v == "HELD(straddle)" and sec is not None
      and sec["verdict"] == "KILL(directional, narrow)", f"{v} {sec}")
# Does-not-fire: narrow criteria not met.
bn2 = dict(bn, median_b_minus_a=0.02, hl_hi_b_minus_a=0.05)
v, ev, _, sec = adjudicate(bn2)
check("verdict: narrow KILL silent when its criteria fail",
      sec is None, str(sec))
# Does not shadow the primary KILL row: flagship fires AND narrow fires.
bn3 = dict(base, p_newton_vs_gdcostfair=0.60, spearman_p=0.60,
           median_b_minus_d=-0.005, hl_hi=0.004,
           median_b_minus_a=-0.004, hl_hi_b_minus_a=0.003)
v, ev, _, sec = adjudicate(bn3)
check("verdict: narrow KILL does not shadow flagship KILL",
      v == "KILL(flagship, cost-fair)" and sec is not None
      and sec["verdict"] == "KILL(directional, narrow)", f"{v} {sec}")
# Disjointness from CONTINUE conjunct (c): when (c) holds, CONTINUE (or an
# earlier HELD) fires first per §7 precedence, so no narrow secondary is
# ever reported — the narrow row cannot contradict a Newton>GD-1 win.
bn4 = dict(base)  # all conjuncts hold incl. (c); narrow prongs forced hot
bn4.update(median_b_minus_a=-0.004, hl_hi_b_minus_a=0.003)
v, ev, _, sec = adjudicate(bn4)
check("verdict: narrow secondary disjoint from CONTINUE conjunct (c)",
      v == "CONTINUE" and sec is None, f"{v} {sec}")
# Missing narrow keys fail loud (binding extended results dict) — fixture
# reaches the narrow row's §7 position (primary straddle).
try:
    bad = {k: v for k, v in bn2.items() if k != "median_b_minus_a"}
    adjudicate(bad)
    check("verdict: missing narrow keys raise", False)
except KeyError:
    check("verdict: missing narrow keys raise", True)

# --- 7. Pass budget (§6) -------------------------------------------------------
pb = PassBudget()
for _ in range(240):
    pb.charge_fwd()
for _ in range(72):
    pb.charge_bwd()
check("budget: 240 fwd + 72 bwd accepted", pb.fwd_equiv() == 384)
try:
    pb.charge_fwd()
    check("budget: pass 241 REFUSED", False)
except RuntimeError as e:
    check("budget: pass 241 REFUSED", "241" in str(e))
pb2 = PassBudget()
for _ in range(72):
    pb2.charge_bwd()
try:
    pb2.charge_bwd()
    check("budget: bwd pass 73 REFUSED", False)
except RuntimeError:
    check("budget: bwd pass 73 REFUSED", True)

# --- 8. Runner refuses execution (no GPU clearance) ---------------------------
import run_exp084
try:
    run_exp084.main()
    check("runner: refuses execution without clearance", False)
except RuntimeError as e:
    check("runner: refuses execution without clearance",
          "not licensed" in str(e).lower() or "torch" in str(e).lower())

# --- 9. Model-loop construction: statistics + orchestration ------------------
# median
check("stats: median odd", S.median([3.0, 1.0, 2.0]) == 2.0)
check("stats: median even", S.median([4.0, 1.0, 3.0, 2.0]) == 2.5)
try:
    S.median([])
    check("stats: median empty raises", False)
except ValueError:
    check("stats: median empty raises", True)
# tie/zero loud halt (LOG-266 binding: never silently drop, never tie-break)
check("stats: NonTestableDataError is ValueError",
      issubclass(S.NonTestableDataError, ValueError))
check("stats: clean diffs pass",
      S.assert_testable_differences([0.1, -0.2, 0.3], "t") == 3)
try:
    S.assert_testable_differences([0.1, 0.0, 0.3], "t")
    check("stats: zero diff halts loud", False)
except S.NonTestableDataError:
    check("stats: zero diff halts loud", True)
try:
    S.assert_testable_differences([0.1, -0.1, 0.3], "t")
    check("stats: |d| tie halts loud", False)
except S.NonTestableDataError:
    check("stats: |d| tie halts loud", True)
check("stats: assert_no_ties clean", S.assert_no_ties([1.0, 2.0], "t") == 2)
try:
    S.assert_no_ties([1.0, 1.0], "t")
    check("stats: tie halts loud", False)
except S.NonTestableDataError:
    check("stats: tie halts loud", True)
# benchmark verbatim rebuild
bench = run_exp084.build_benchmark()
check("bench: 60 items", len(bench) == 60)
check("bench: item0 bit-exact",
      bench[0]["prompt"] == "Premise: Mars outranks Venus. Venus outranks "
      "Jupiter. Question: Who is higher in rank, Jupiter or Mars? Answer:"
      and bench[0]["ent"] == "Mars" and bench[0]["typ"] == "planet")
check("bench: item15 is planet 3-hop",
      bench[15]["id"] == "exp077_planet_3hop_0" and bench[15]["typ"] == "planet")
check("bench: item30 is element 2-hop",
      bench[30]["id"] == "exp077_element_2hop_0" and bench[30]["typ"] == "element")
# run-halting error taxonomy
try:
    raise run_exp084.InvalidRunError("ii", "x")
except run_exp084.InvalidRunError as e:
    check("loop: InvalidRunError carries row",
          e.invalid_row == "ii" and isinstance(e, RuntimeError))
# probe-set preflight against the real pinned archive
import tempfile
_logs = []
try:
    ps = run_exp084.load_probe_set(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "EXP077_cone_vs_line",
                     "exp077_instance_records.json"), _logs.append)
    check("loop: probe preflight sha ok",
          ps["records_sha"] == run_exp084.RECORDS_SHA256
          and len(ps["prompts"]) == 24)
    check("loop: probe deviation recorded (6/24)",
          ps["alignment_24"] == 6 and any("DEVIATION" in m for m in _logs))
except run_exp084.ApparatusError as e:
    check("loop: probe preflight sha ok", False, str(e))
# missing records file -> loud halt
try:
    run_exp084.load_probe_set("/nonexistent/records.json", _logs.append)
    check("loop: missing records halts loud", False)
except run_exp084.ApparatusError:
    check("loop: missing records halts loud", True)

# --- 10. First-run P0 baseline: archive-then-halt (LOG-269 D2 binding) -----
# Direct unit tests of check_identity: first run must archive M0 and halt
# verdict-clean (BaselinePrepassHalt, NOT InvalidRunError); the re-run
# replays the archive and enforces INVALID(ii) bit-for-bit.
_tmp = tempfile.mkdtemp(prefix="exp084_d2_")
_bpath = os.path.join(_tmp, "exp084_baseline_margins.json")
_m0 = [0.5 + 0.01 * i for i in range(24)]
_logs3 = []
try:
    run_exp084.check_identity(_m0, _bpath, _logs3.append)
    check("loop: first run archives + halts verdict-clean (BaselinePrepassHalt)",
          False, "no exception raised")
except run_exp084.BaselinePrepassHalt as e:
    check("loop: first run archives + halts verdict-clean (BaselinePrepassHalt)",
          "re-run" in str(e).lower(), str(e)[:80])
    check("loop: pre-pass halt is not INVALID (nothing invalid)",
          not isinstance(e, run_exp084.InvalidRunError))
    check("loop: baseline archive written on first run",
          os.path.isfile(_bpath))
    _arch = json.load(open(_bpath))["m0"] if os.path.isfile(_bpath) else None
    check("loop: archive stores bit-exact M0",
          _arch == [float(x) for x in _m0])
except Exception as e:
    check("loop: first run archives + halts verdict-clean (BaselinePrepassHalt)",
          False, f"{type(e).__name__}: {e}")
# re-run: identical M0 replays the archive — no halt, full loop may proceed
try:
    run_exp084.check_identity(_m0, _bpath, _logs3.append)
    check("loop: re-run replays archive (identity enforced)", True)
except Exception as e:
    check("loop: re-run replays archive (identity enforced)", False,
          f"{type(e).__name__}: {e}")
# re-run: shifted M0 -> INVALID(ii)
try:
    run_exp084.check_identity([x + 0.001 for x in _m0], _bpath, _logs3.append)
    check("loop: re-run M0 mismatch -> INVALID(ii)", False, "no exception")
except run_exp084.InvalidRunError as e:
    check("loop: re-run M0 mismatch -> INVALID(ii)", e.invalid_row == "ii")

# --- 11. Default RECORDS_REL resolves to the pinned archive (LOG-269 F2) ---
# Regression test for the untested-default class of bug: this resolves the
# DEFAULT path the runner actually uses (not an explicitly correct one)
# and asserts it hits the pinned archive with the R5d SHA.
_bundle = os.path.dirname(os.path.abspath(__file__))
_default_records = os.path.join(_bundle, run_exp084.RECORDS_REL)
check("loop: default RECORDS_REL exists on disk",
      os.path.isfile(_default_records), run_exp084.RECORDS_REL)
try:
    _sha = hashlib.sha256(open(_default_records, "rb").read()).hexdigest()
except FileNotFoundError:
    _sha = ""
check("loop: default RECORDS_REL sha256 == R5d pin",
      _sha == run_exp084.RECORDS_SHA256, run_exp084.RECORDS_REL)

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
