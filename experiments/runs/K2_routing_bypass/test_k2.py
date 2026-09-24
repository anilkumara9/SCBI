"""K2 routing-vs-bypass — evaluator tests (LOG-226, Law #15).

Seeded, deterministic, CPU-runnable (stdlib only; scipy cross-checks are
conditional on scipy being importable). Covers:

  1. endpoint arithmetic: McNemar exact p, Tango (score) CI on the paired
     contrast (properties + Monte-Carlo coverage + archive cross-check),
  2. kill bars L > 0.05 / U < 0.05,
  3. verdict-table cell mapping (all six rows: 1, 2, 2r, 3, 4, 5),
  4. G10 exclusion-floor logic,
  5. pre-execution gates' pass/fail criteria (gate A, checklist B, G1/G3/G4/G5).

Run:  python3 test_k2.py   (from the K2_routing_bypass directory)
Exit 0 + ALL TESTS PASSED iff every test passes.
"""

import os
import sys
import json
import math
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2_endpoints import (paired_table, paired_contrast_stats, mcnemar_exact_p,
                          tango_ci, tango_score_z, tango_one_sided_upper,
                          adjudicate_verdict, _z_for_alpha)
from k2_guards import (g1_norm_check, g1_invalid_check, g4_pass_count_check,
                       g5_c_gate_check, g10_exclusion_floor_check,
                       gate_a_evaluate, checklist_b_record,
                       g3_delta_theta_check, guards_evaluate,
                       C_GATE_MDE_B, NORM_REL_TOL, DELTA_MIN)

HERE = os.path.dirname(os.path.abspath(__file__))
ARCH_RECORDS = os.path.normpath(os.path.join(
    HERE, "..", "EXP077_cone_vs_line", "exp077_instance_records.json"))

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"  [{PASS if cond else FAIL}] {name}" + (f" — {detail}" if detail and not cond else ""))


# ---------------------------------------------------------------- 1. McNemar
def test_mcnemar():
    # The archived smoke bridge_gate anchor: b=14, c=0 -> p=0.0001220703125 [FACT].
    check("mcnemar: b=14,c=0 reproduces archived p=0.0001220703125",
          mcnemar_exact_p(14, 0) == 0.0001220703125,
          f"got {mcnemar_exact_p(14, 0)}")
    check("mcnemar: b=c=0 -> 1.0 (M5.1)", mcnemar_exact_p(0, 0) == 1.0)
    check("mcnemar: b=6,c=0 -> 0.03125 (L1 MDE bar)",
          mcnemar_exact_p(6, 0) == 0.03125, f"got {mcnemar_exact_p(6, 0)}")
    check("mcnemar: symmetric in (b,c)",
          mcnemar_exact_p(3, 9) == mcnemar_exact_p(9, 3))
    try:
        from scipy.stats import binomtest
        ok = True
        for (b, c) in [(14, 0), (6, 0), (3, 9), (0, 5), (11, 4), (1, 1)]:
            s = b + c
            ref = binomtest(min(b, c), s, 0.5, alternative="two-sided").pvalue
            if abs(mcnemar_exact_p(b, c) - ref) > 1e-15:
                ok = False
        check("mcnemar: matches scipy binomtest two-sided (6 cases)", ok)
    except ImportError:
        check("mcnemar: scipy cross-check skipped (scipy absent)", True)


# ---------------------------------------------------------------- 2. Tango CI
def test_tango_properties():
    check("z(0.05) == 1.959964 (tol 1e-6)",
          abs(_z_for_alpha(0.05) - 1.959963984540054) < 1e-6)
    # Score statistic reduces to McNemar's score at delta=0.
    for (n11, n12, n21, n22) in [(36, 14, 0, 10), (20, 8, 3, 29), (0, 6, 0, 54)]:
        z0 = tango_score_z(n11, n12, n21, n22, 0.0)
        mcn = (n12 - n21) / math.sqrt(n12 + n21)
        check(f"tango Z(0)==McNemar score for {(n11,n12,n21,n22)}",
              abs(z0 - mcn) < 1e-12, f"z0={z0}, mcnemar={mcn}")
    # CI contains the point estimate; arm-swap symmetry.
    rng = random.Random(20260923)
    sym_ok, contain_ok = True, True
    for _ in range(25):
        cells = [rng.randint(0, 30) for _ in range(4)]
        n11, n12, n21, n22 = cells
        L, U = tango_ci(n11, n12, n21, n22)
        d = (n12 - n21) / sum(cells)
        if not (L - 1e-12 <= d <= U + 1e-12):
            contain_ok = False
        Ls, Us = tango_ci(n11, n21, n12, n22)  # swap arms -> -delta
        if not (abs(L + Us) < 1e-9 and abs(U + Ls) < 1e-9):
            sym_ok = False
    check("tango: CI contains the point estimate (25 random tables)", contain_ok)
    check("tango: arm-swap symmetry CI(y,x) == -CI(x,y) (25 tables)", sym_ok)
    # Degenerate: no discordant pairs -> narrow symmetric CI around 0.
    L, U = tango_ci(36, 0, 0, 24)
    check("tango: zero-discordant CI contains 0 and is narrow",
          L < 0 < U and (U - L) < 0.15, f"({L:.4f},{U:.4f})")
    # All-concordant table -> approx +/- z^2/n.
    L, U = tango_ci(60, 0, 0, 0)
    z2n = (1.959963984540054 ** 2) / 60
    check("tango: all-concordant CI ~= +/- z^2/n",
          abs(U - z2n) < 0.005 and abs(L + z2n) < 0.005, f"({L:.4f},{U:.4f})")
    # Determinism: identical across repeated calls.
    r1 = tango_ci(36, 14, 0, 10)
    r2 = tango_ci(36, 14, 0, 10)
    check("tango: deterministic (repeat identical)", r1 == r2)
    # Monotonicity of Z in delta over a battery of tables.
    mono_ok = True
    for (n11, n12, n21, n22) in [(36, 14, 0, 10), (20, 8, 3, 29), (0, 6, 0, 54),
                                 (30, 0, 0, 30), (10, 10, 10, 30), (0, 0, 14, 46),
                                 (59, 1, 0, 0), (5, 25, 5, 25)]:
        prev = None
        for k in range(401):
            d_ = -0.999 + k * (1.998 / 400)
            z_ = tango_score_z(n11, n12, n21, n22, d_)
            if prev is not None and z_ > prev + 1e-9:
                mono_ok = False
            prev = z_
    check("tango: Z(delta) monotone decreasing (8 tables x 401 grid)", mono_ok)


def test_tango_anchor_and_coverage():
    # Archive cross-check: the smoke C8-vs-C1 table from the real records.
    with open(ARCH_RECORDS, encoding="utf-8") as f:
        recs = json.load(f)
    c1 = [bool(r["correct"]["C1"]) for r in recs]
    c8 = [bool(r["correct"]["C8_bridge"]) for r in recs]
    st = paired_contrast_stats(c1, c8, label="c8_vs_c1")
    check("archive: C8 vs C1 reproduces b=14, c=0", st["b"] == 14 and st["c"] == 0,
          f"b={st['b']}, c={st['c']}")
    check("archive: C8 vs C1 reproduces p=0.0001220703125",
          st["mcnemar_p"] == 0.0001220703125, f"p={st['mcnemar_p']}")
    check("archive: C8 vs C1 reproduces dM=+0.233333",
          abs(st["d_hat"] - 0.23333333333333334) < 1e-12, f"d={st['d_hat']}")
    check("archive: Tango CI lower bound > 0 (consistent with the rescue)",
          st["tango_L"] > 0.0, f"CI=({st['tango_L']:.4f},{st['tango_U']:.4f})")
    # Monte-Carlo coverage of the Tango 95% CI (seeded).
    for (p11, p12, p21, p22, n, seed) in [(0.50, 0.20, 0.10, 0.20, 60, 111),
                                          (0.80, 0.10, 0.05, 0.05, 60, 222)]:
        delta_true = p12 - p21
        r = random.Random(seed)
        hits = 0
        nsim = 1000
        probs = [p11, p12, p21, p22]
        for _ in range(nsim):
            counts = [0, 0, 0, 0]
            for _ in range(n):
                u = r.random()
                cum = 0.0
                for k, p_ in enumerate(probs):
                    cum += p_
                    if u < cum:
                        counts[k] += 1
                        break
            L, U = tango_ci(*counts)
            if L <= delta_true <= U:
                hits += 1
        cov = hits / nsim
        check(f"tango: 95% CI Monte-Carlo coverage ~= 0.95 "
              f"(p=({p11},{p12},{p21},{p22}), cov={cov:.3f})",
              0.925 <= cov <= 0.975, f"cov={cov:.3f}")


# ---------------------------------------------------------------- 3. kill bars
def test_kill_bars():
    # L > 0.05 fires the routing bar; U < 0.05 fires the flat bar — on the
    # actual Tango CI, not on invented numbers.
    L, U = tango_ci(30, 18, 2, 10)   # strong (b)-side table
    check("kill bar: strong table has L > 0.05", L > 0.05, f"L={L:.4f}")
    # REGRESSION PROPERTY of the two-sided Tango family (retained; D1 RESOLVED
    # by REV3 per LOG-227, corrected per LOG-228/229): the two-sided bar is no
    # longer the row-1 instrument. At N=60 the Tango 95% CI's upper bound is
    # minimized at zero discordant pairs, where U = z^2/(n+z^2) = 0.0602 >
    # delta_min = 0.05. The repaired row-1 flatness conjunct is the true
    # one-sided 95% Tango upper (z=1.6449), pinned by test_rev4_flatness_bar.
    min_U = min(tango_ci(n11, 0, 0, 60 - n11)[1] for n11 in range(61))
    check("tango: min upper bound at N=60 is 0.0602 > 0.05 (no flat arm clears it)",
          abs(min_U - 0.0602) < 0.001 and min_U > 0.05, f"min U={min_U:.4f}")
    L3, U3 = tango_ci(25, 6, 4, 25)  # straddle table
    check("kill bar: straddle table has L <= 0.05 (routing bar not met)",
          not (L3 > 0.05), f"L={L3:.4f}")


# ---------------------------------------------------------------- 4. verdicts
def _lists(n, idx_right):
    v = [False] * n
    for i in idx_right:
        v[i] = True
    return v


def test_verdict_rows():
    n = 60
    # Row 1 (REV4 headline, repaired bar): arm-(a) FLAT at 0/60 -> the true
    # one-sided 95% Tango upper U_1s = 0.043147 < 0.05 FIRES; (b) rescues
    # strongly (b_b = 20 >= 6); contrast L > 0.05. Routing Supported.
    base = _lists(n, list(range(36)))          # baseline 36/60 right
    a1 = list(base)                            # (a): flat, s = 0
    b1 = _lists(n, list(range(56)))            # (b): 20 rescues, 0 flips
    c1 = _lists(n, list(range(56)))
    v1 = adjudicate_verdict(base, a1, b1, c1, [], c_gate_passed=True)
    check("verdict row 1: routing Supported / local Not supported (flat arm-(a))",
          v1["row"] == 1 and v1["verdict_routing"] == "Supported"
          and v1["verdict_final_position_local"] == "Not supported",
          f"row={v1['row']}")
    check("verdict row 1: kill bars hold (L_contrast>0.05, b_b>=6, U_1s(a)<0.05)",
          v1["contrast_b_vs_a"]["tango_L"] > 0.05 and v1["arm_b"]["b"] >= 6
          and v1["arm_a"]["tango_U_1s"] < 0.05,
          f"L={v1['contrast_b_vs_a']['tango_L']:.4f}, b_b={v1['arm_b']['b']}, "
          f"U_1s={v1['arm_a']['tango_U_1s']:.4f}")
    check("verdict row 1: arm-(a) is flat (dM_a=0, s=0) — headline case",
          v1["arm_a"]["d_hat"] == 0.0 and v1["arm_a"]["b"] == 0 and v1["arm_a"]["c"] == 0)
    # A materially negative arm-(a) also satisfies the directional conjunct.
    a1neg = _lists(n, list(range(6, 36)))      # (a): 6 flips, 0 rescues
    v1neg = adjudicate_verdict(base, a1neg, b1, c1, [], c_gate_passed=True)
    check("verdict row 1: negative arm-(a) still fires (directional conjunct)",
          v1neg["row"] == 1 and v1neg["arm_a"]["tango_U_1s"] < 0.05,
          f"row={v1neg['row']}")
    # Row 2: (a) rescues, (b) weak-but-nonzero, contrast U < 0.05.
    base2 = _lists(n, list(range(36)))
    a2 = _lists(n, list(range(50)))            # (a): 14 rescues, 0 flips
    b2 = _lists(n, list(range(36)) + [50, 51])  # (b): 2 rescues, 0 flips
    c2 = _lists(n, list(range(50)))
    v2 = adjudicate_verdict(base2, a2, b2, c2, [], c_gate_passed=True)
    check("verdict row 2: routing Not supported / local Supported",
          v2["row"] == 2 and v2["verdict_routing"] == "Not supported"
          and v2["verdict_final_position_local"] == "Supported",
          f"row={v2['row']}")
    # Row 2r: row-2 pattern with (b) flat-zero and L_a > 0.05.
    b2r = _lists(n, list(range(36)))           # (b): identical to baseline
    v2r = adjudicate_verdict(base2, a2, b2r, c2, [], c_gate_passed=True)
    check("verdict row 2r: routing Refuted / local Supported",
          v2r["row"] == "2r" and v2r["verdict_routing"] == "Refuted"
          and v2r["verdict_final_position_local"] == "Supported",
          f"row={v2r['row']}")
    # Row 3: contrast CI straddles.
    a3 = _lists(n, list(range(44)))            # (a): 8 rescues
    b3 = _lists(n, list(range(40)) + list(range(44, 50)))  # (b): 10 rescues, overlap 4
    c3 = _lists(n, list(range(50)))
    v3 = adjudicate_verdict(base2, a3, b3, c3, [], c_gate_passed=True)
    check("verdict row 3: Inconclusive / Inconclusive (straddle)",
          v3["row"] == 3 and v3["verdict_routing"] == "Inconclusive"
          and v3["verdict_final_position_local"] == "Inconclusive",
          f"row={v3['row']}")
    # Row 4: both arms flat, (c) passes G5.
    z = _lists(n, list(range(36)))
    cz = _lists(n, list(range(50)))
    v4 = adjudicate_verdict(base2, z, z, cz, [], c_gate_passed=True)
    check("verdict row 4: Inconclusive / Inconclusive (both flat, c passes)",
          v4["row"] == 4 and v4["verdict_routing"] == "Inconclusive",
          f"row={v4['row']}")
    # Row 5 is decided by guards_evaluate (FATAL) — see test_guards_row5.
    # Actual-N accounting: exclusions shrink N; bars still apply.
    excl = [{"item": i, "cause": "G10 test"} for i in range(6)]
    vN = adjudicate_verdict(base[:54], a1[:54], b1[:54], c1[:54], excl,
                            c_gate_passed=True)
    check("verdict: actual-N accounting (N=54 recorded)",
          vN["n_actual"] == 54 and vN["n_excluded"] == 6 and vN["row"] == 1,
          f"row={vN['row']}, N={vN['n_actual']}")


# ---------------------------------------------------------------- 4b. REV4 bite table
def test_rev4_flatness_bar():
    # Signed canonical values (REV4 §3.4/§6; LOG-228 interval-identity ruling;
    # LOG-229 0.056902 correction): the TRUE one-sided 95% Tango upper bound
    # for Δ̂M_a (z=1.6449, constrained-MLE variance) from the K1-validated
    # tango_ci code path — one interval family, not two (the q-pinned score
    # form is rejected by name). Independently reproduced to 6dp (LOG-229).
    check("one-sided z(0.95) == 1.6449 (tol 1e-3)",
          abs(_z_for_alpha(0.10) - 1.6449) < 1e-3,
          f"got {_z_for_alpha(0.10):.6f}")
    for cells, exact6, form4 in [((60, 0, 0, 0), 0.043147, 0.0431),
                                 ((58, 1, 1, 0), 0.056902, 0.0569),
                                 ((56, 2, 2, 0), 0.067926, 0.0679),
                                 ((54, 0, 0, 0), 0.047712, 0.0477)]:
        u = tango_one_sided_upper(*cells)
        check(f"bite table: {cells} -> {exact6} (6dp)",
              abs(u - exact6) < 5e-7, f"got {u:.6f}")
        check(f"bite table: {cells} -> {form4} (4dp form)",
              round(u, 4) == form4, f"got {u:.6f}")
    # (i) HEADLINE: flat arm-(a) at 0/60 fires row 1.
    n = 60
    base = _lists(n, list(range(36)))
    a_flat = list(base)
    b_strong = _lists(n, list(range(56)))
    c_strong = _lists(n, list(range(56)))
    v = adjudicate_verdict(base, a_flat, b_strong, c_strong, [], c_gate_passed=True)
    check("bite (i): flat arm-(a) 0/60 -> U_1s=0.0431 < 0.05, b_b>=6, contrast L>0.05",
          round(v["arm_a"]["tango_U_1s"], 4) == 0.0431
          and v["arm_a"]["tango_U_1s"] < 0.05 and v["arm_b"]["b"] >= 6
          and v["contrast_b_vs_a"]["tango_L"] > 0.05,
          f"U_1s={v['arm_a']['tango_U_1s']:.4f}, b_b={v['arm_b']['b']}, "
          f"L={v['contrast_b_vs_a']['tango_L']:.4f}")
    check("bite (i): row 1 fires (routing Supported / local Not supported)",
          v["row"] == 1 and v["verdict_routing"] == "Supported"
          and v["verdict_final_position_local"] == "Not supported",
          f"row={v['row']}")
    # (ii) b_a = c_a = 1 does NOT fire row 1 (U_1s=0.0569 >= 0.05).
    a11 = list(base)
    a11[35] = False   # one flip  (c_a = 1)
    a11[40] = True    # one rescue (b_a = 1)
    v11 = adjudicate_verdict(base, a11, b_strong, c_strong, [], c_gate_passed=True)
    check("bite (ii): b=c=1 -> U_1s=0.0569 >= 0.05 (bar fails)",
          round(v11["arm_a"]["tango_U_1s"], 4) == 0.0569
          and v11["arm_a"]["tango_U_1s"] >= 0.05,
          f"U_1s={v11['arm_a']['tango_U_1s']:.4f}")
    check("bite (ii): row 1 does NOT fire",
          v11["row"] != 1, f"row={v11['row']}")
    # (iv) ROW-3 CATCH-ALL: contrast clears but the flatness conjunct fails
    # (here b_a = c_a = 2 -> U_1s = 0.0679) -> Inconclusive, reason recorded.
    a22 = list(base)
    a22[34] = False
    a22[35] = False   # two flips  (c_a = 2)
    a22[40] = True
    a22[41] = True    # two rescues (b_a = 2)
    v22 = adjudicate_verdict(base, a22, b_strong, c_strong, [], c_gate_passed=True)
    check("bite (iv): b=c=2 -> U_1s=0.0679 >= 0.05 (flatness fails)",
          round(v22["arm_a"]["tango_U_1s"], 4) == 0.0679
          and v22["arm_a"]["tango_U_1s"] >= 0.05,
          f"U_1s={v22['arm_a']['tango_U_1s']:.4f}")
    check("bite (iv): catch-all fires (row 3, Inconclusive / Inconclusive)",
          v22["row"] == 3 and v22["verdict_routing"] == "Inconclusive"
          and v22["verdict_final_position_local"] == "Inconclusive",
          f"row={v22['row']}")
    check("bite (iv): catch-all reason names the failed flatness conjunct",
          v22["row3_reason"] is not None
          and v22["row3_reason"].startswith("contrast_clears_row1_flatness_fails"),
          v22["row3_reason"])
    check("bite (ii): the b=c=1 world is the same catch-all branch",
          v11["row"] == 3 and v11["row3_reason"].startswith("contrast_clears_row1_flatness_fails"),
          f"row={v11['row']}, reason={v11['row3_reason']}")
    # (v) N=54 G10-exclusion floor: flat arm-(a) fires row 1 (U_1s=0.0477).
    n54 = 54
    base54 = _lists(n54, list(range(36)))
    a54 = list(base54)
    b54 = _lists(n54, list(range(51)))   # 15 rescues, b_b = 15 >= 6
    c54 = _lists(n54, list(range(51)))
    excl = [{"item": i, "cause": "G10 test"} for i in range(6)]
    v54 = adjudicate_verdict(base54, a54, b54, c54, excl, c_gate_passed=True)
    check("bite (v): N=54 flat -> U_1s=0.0477 < 0.05, b_b>=6, contrast L>0.05",
          round(v54["arm_a"]["tango_U_1s"], 4) == 0.0477
          and v54["arm_a"]["tango_U_1s"] < 0.05 and v54["arm_b"]["b"] >= 6
          and v54["contrast_b_vs_a"]["tango_L"] > 0.05 and v54["n_actual"] == 54,
          f"U_1s={v54['arm_a']['tango_U_1s']:.4f}, L={v54['contrast_b_vs_a']['tango_L']:.4f}, "
          f"N={v54['n_actual']}")
    check("bite (v): row 1 fires at the G10 floor",
          v54["row"] == 1 and v54["verdict_routing"] == "Supported",
          f"row={v54['row']}")
    # One-sided upper is strictly below the two-sided upper (directional bar).
    check("one-sided U_1s < two-sided U for every canonical table",
          all(tango_one_sided_upper(*c) < tango_ci(*c)[1]
              for c in [(60, 0, 0, 0), (58, 1, 1, 0), (56, 2, 2, 0), (54, 0, 0, 0)]))
    # (iii) all six rows fire on synthetic data: rows 1/2/2r/3/4 through the
    # adjudicator (re-built here) and row 5 through the guard record.
    rows = {1: v["row"], 11: v11["row"], 22: v22["row"], 54: v54["row"]}
    b2 = _lists(n, list(range(36)) + [50, 51])     # (b): 2 rescues
    a2 = _lists(n, list(range(50)))                 # (a): 14 rescues
    r2 = adjudicate_verdict(base, a2, b2, c_strong, [], c_gate_passed=True)
    rows["r2"] = r2["row"]
    b2r = list(base)                                # (b) flat-zero
    r2r = adjudicate_verdict(base, a2, b2r, c_strong, [], c_gate_passed=True)
    rows["r2r"] = r2r["row"]
    a3 = _lists(n, list(range(44)))
    b3 = _lists(n, list(range(40)) + list(range(44, 50)))
    r3 = adjudicate_verdict(base, a3, b3, c_strong, [], c_gate_passed=True)
    rows["r3"] = r3["row"]
    z = list(base)
    r4 = adjudicate_verdict(base, z, z, c_strong, [], c_gate_passed=True)
    rows["r4"] = r4["row"]
    check("bite (iii): all six rows fire on synthetic data",
          rows[1] == 1 and rows["r2"] == 2 and rows["r2r"] == "2r"
          and rows["r3"] == 3 and rows[22] == 3 and rows["r4"] == 4,
          f"rows={rows}")


# ---------------------------------------------------------------- 5. G10 floor
def test_g10_floor():
    s6, m6 = g10_exclusion_floor_check([{"item": i, "cause": "x"} for i in range(6)])
    check("G10: 6 exclusions -> proceed at actual N",
          s6 == "proceed" and "54" in m6, m6)
    s7, m7 = g10_exclusion_floor_check([{"item": i, "cause": "x"} for i in range(7)])
    check("G10: 7 exclusions -> Underdetermined",
          s7 == "Underdetermined", m7)
    s0, _ = g10_exclusion_floor_check([])
    check("G10: 0 exclusions -> proceed", s0 == "proceed")


# ---------------------------------------------------------------- 6. pre-exec gates
def test_gate_a():
    v, m = gate_a_evaluate(True, True, True)
    check("gate A: all pass -> PASS", v == "PASS", m)
    for name, args_ in [("byte-identity fail", (False, True, True)),
                        ("norm-compare fail", (True, False, True)),
                        ("tokenizer-log fail", (True, True, False))]:
        v, m = gate_a_evaluate(*args_)
        check(f"gate A: {name} -> FAIL blocks GPU clearance with cause",
              v == "FAIL" and "BLOCKED" in m, m)


def test_checklist_b():
    r = checklist_b_record("ab" * 32, "c" * 40)
    check("checklist B: checksum+revision -> complete", r["status"] == "complete")
    r = checklist_b_record(None, "c" * 40)
    check("checklist B: missing log -> recorded DEVIATION, not INVALID",
          r["status"] == "deviation_recorded" and "NOT an INVALID" in r["note"])
    r = checklist_b_record("ab" * 32, None)
    check("checklist B: missing revision -> recorded deviation",
          r["status"] == "deviation_recorded")


def test_g1_g3_g4_g5():
    ok, per = g1_norm_check([0.5] * 60, [0.5] * 60)
    check("G1(b): exact norms match", ok and all(p["passed"] for p in per))
    ok, per = g1_norm_check([0.5] * 60, [0.50002] * 60)  # rel err 4e-5 > 1e-5
    check("G1(b): 4e-5 rel err fails the 1e-5 bar", not ok)
    ok, per = g1_norm_check([0.5], [0.0])
    check("G1(b): zero logged norm handled (no crash)", per[0]["rel_err"] == float("inf"))
    check("G1: 2 item failures -> not INVALID", not g1_invalid_check(2))
    check("G1: 3 item failures -> INVALID", g1_invalid_check(3))
    ok, exp = g4_pass_count_check(180, 60)
    check("G4: 180 passes at N=60 -> ok", ok and exp == 180)
    ok, _ = g4_pass_count_check(179, 60)
    check("G4: 179 passes -> violated", not ok)
    ok, exp = g4_pass_count_check(162, 54)
    check("G4: scales to actual N (162 = 3x54)", ok and exp == 162)
    check("G5: b_c=6 -> pass (L1 MDE floor)", g5_c_gate_check(6))
    check("G5: b_c=5 -> fail", not g5_c_gate_check(5))
    check("G5: b_c=14 (smoke anchor) -> pass", g5_c_gate_check(14))
    ok, _ = g3_delta_theta_check("abc", "abc")
    check("G3: pre==post -> holds", ok)
    ok, msg = g3_delta_theta_check("abc", "abd")
    check("G3: pre!=post -> FATAL", not ok and "FATAL" in msg)


def test_guards_row5():
    base_rec = {"g1_invalid": False, "g3_pre_post_match": True,
                "g4_pass_count_ok": True, "g4_expected": 180, "g4_got": 180,
                "g5_c_gate_passed": True, "b_c": 14,
                "records_missing": False, "exclusions": []}
    u, _ = guards_evaluate(dict(base_rec))
    check("row 5: clean record -> not Underdetermined", not u)
    for name, mut in [("G3 violated", {"g3_pre_post_match": False}),
                      ("G4 violated", {"g4_pass_count_ok": False}),
                      ("G1 INVALID", {"g1_invalid": True}),
                      ("G5 failed", {"g5_c_gate_passed": False}),
                      ("records missing", {"records_missing": True}),
                      ("G10 floor", {"exclusions": [{"item": i, "cause": "x"}
                                                    for i in range(7)]})]:
        rec = dict(base_rec)
        rec.update(mut)
        u, cause = guards_evaluate(rec)
        check(f"row 5: {name} -> Underdetermined",
              u and "Underdetermined" in cause, cause)


def main():
    print("K2 evaluator tests (LOG-226) — seeded, deterministic, CPU-only")
    print("-" * 70)
    test_mcnemar()
    test_tango_properties()
    test_tango_anchor_and_coverage()
    test_kill_bars()
    test_verdict_rows()
    test_rev4_flatness_bar()
    test_g10_floor()
    test_gate_a()
    test_checklist_b()
    test_g1_g3_g4_g5()
    test_guards_row5()
    print("-" * 70)
    n_fail = sum(1 for _, ok, _ in results if not ok)
    print(f"{len(results) - n_fail}/{len(results)} tests passed")
    if n_fail:
        print("FAILURES:")
        for name, ok, detail in results:
            if not ok:
                print(f"  - {name}: {detail}")
        print("K2 EVALUATOR TESTS: FAILURES PRESENT")
        return 1
    print("ALL K2 EVALUATOR TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
