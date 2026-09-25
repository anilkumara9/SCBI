#!/usr/bin/env python3
"""EXP088 evaluator test suite (CPU, zero model passes, zero torch).

Synthetic fixtures only. Every numeric claim is checked against an
independent brute-force or algebraic reference computed in this file —
never against the module under test.

Groups:
  A. McNemar exact one-sided p vs brute-force binomial tails.
  B. Tango CI: containment of d_hat, swap-symmetry, degenerate tables,
     width shrinks with n.
  C. Section-G1b mapping boundaries (F5).
  D. F6 gain-curve classification (all five classes).
  E. F7 Stage-A gate: strict > eps, argmax, margin, tie loud-halt.
  F. Verdict adjudication: all four labels + the B2 override.
  G. Probe set: 60-item rebuild, decision rule, pinned-archive preflight.
  H. F8 ramping: pinned schedule values + loud input validation.
  I. RNG pins + torch-exclusivity + no-numpy contract.
  J. Runner: clearance refusal, budget ceiling, startup preflight before
     any model construction (defect-#6 regression), geometry-drift halt.

Exit 0 iff every check passes. Prints PASS/FAIL per check and a summary.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import exp088_endpoints as E
import exp088_probeset as P
import exp088_ramping as RP
import exp088_rng as R
import run_exp088 as RUN

CHECKS = []


def check(name):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


def brute_mcnemar_greater(b, c):
    """Independent reference: P(Bin(b+c, 1/2) >= b); b=c=0 -> 1.0."""
    s = b + c
    if s == 0:
        return 1.0
    return sum(math.comb(s, k) for k in range(b, s + 1)) / 2.0 ** s


def bits(n, on):
    on = set(on)
    return [i in on for i in range(n)]


# ---------------------------------------------------------------- A. McNemar
@check("mcnemar/brute-force-agreement")
def _():
    rng = random.Random(20260924)
    worst = 0.0
    for _ in range(300):
        b = rng.randint(0, 60)
        c = rng.randint(0, 60)
        got = E.mcnemar_exact_one_sided_greater(b, c)
        want = brute_mcnemar_greater(b, c)
        worst = max(worst, abs(got - want))
        assert got == want, f"b={b} c={c}: {got} != {want}"
    assert worst == 0.0
    return f"300 random (b,c) agree exactly; degenerate b=c=0 -> {E.mcnemar_exact_one_sided_greater(0, 0)}"


@check("mcnemar/one-sided-orientation")
def _():
    # y clearly better: small p; x clearly better: p near 1.
    assert E.mcnemar_exact_one_sided_greater(14, 2) < 0.01
    assert E.mcnemar_exact_one_sided_greater(2, 14) > 0.99
    p = E.mcnemar_exact_one_sided_greater(6, 4)
    assert abs(p - brute_mcnemar_greater(6, 4)) == 0.0
    return f"p(14,2)={E.mcnemar_exact_one_sided_greater(14,2):.5f} p(2,14)={E.mcnemar_exact_one_sided_greater(2,14):.5f}"


# ---------------------------------------------------------------- B. Tango
@check("tango/contains-dhat")
def _():
    rng = random.Random(7)
    for _ in range(200):
        n11 = rng.randint(0, 40)
        n12 = rng.randint(0, 40)
        n21 = rng.randint(0, 40)
        n22 = rng.randint(0, 40)
        n = n11 + n12 + n21 + n22
        if n == 0:
            continue
        d = (n12 - n21) / n
        L, U = E.tango_ci(n11, n12, n21, n22)
        assert L - 1e-9 <= d <= U + 1e-9, (
            f"d_hat={d} outside [{L},{U}] for {(n11,n12,n21,n22)}")
        assert L <= U
    return "200 random tables: d_hat inside [L,U], L<=U"


@check("tango/swap-symmetry")
def _():
    rng = random.Random(11)
    worst = 0.0
    for _ in range(100):
        a = [rng.randint(0, 30) for _ in range(4)]
        if sum(a) == 0:
            continue
        n11, n12, n21, n22 = a
        L1, U1 = E.tango_ci(n11, n12, n21, n22)
        L2, U2 = E.tango_ci(n11, n21, n12, n22)  # arms swapped
        worst = max(worst, abs(L2 + U1), abs(U2 + L1))
        assert abs(L2 + U1) < 1e-6 and abs(U2 + L1) < 1e-6, (
            f"asymmetry: [{L1},{U1}] vs [{L2},{U2}]")
    return f"100 tables: CI(y-x) == -CI(x-y), worst |err|={worst:.2e}"


@check("tango/degenerate-tables")
def _():
    # No discordant pairs: the Tango score interval does NOT collapse to a
    # point (the concordant cells still carry marginal uncertainty); it is
    # symmetric about 0 and narrow.
    L, U = E.tango_ci(30, 0, 0, 30)
    assert abs(L + U) < 1e-9 and (U - L) < 0.15, f"[{L},{U}]"
    # One-sided discordance: CI hugs the correct side, contains d_hat.
    L, U = E.tango_ci(20, 9, 0, 31)
    d = 9 / 60
    assert L <= d <= U and L >= -1e-9, f"[{L},{U}] d={d}"
    L, U = E.tango_ci(20, 0, 9, 31)
    d = -9 / 60
    assert L <= d <= U and U <= 1e-9, f"[{L},{U}] d={d}"
    return "b=c=0 -> symmetric narrow interval about 0; one-sided stays put"


@check("tango/width-shrinks-with-n")
def _():
    def width(scale):
        n11, n12, n21, n22 = (20 * scale, 14 * scale,
                              2 * scale, 24 * scale)
        L, U = E.tango_ci(n11, n12, n21, n22)
        return U - L
    w1, w2, w4 = width(1), width(2), width(4)
    assert w4 < w2 < w1, f"{w1} {w2} {w4}"
    return f"widths at 1x/2x/4x n: {w1:.4f} > {w2:.4f} > {w4:.4f}"


# ---------------------------------------------------------------- C. G1b
@check("g1b/boundaries")
def _():
    assert E.g1b_map(0.0500001, 0.2) == "Supported"
    assert E.g1b_map(0.05, 0.2) == "Inconclusive"      # L > 0.05 strict
    assert E.g1b_map(-0.1, 0.0499999) == "Not supported"
    assert E.g1b_map(-0.1, 0.05) == "Inconclusive"     # U < 0.05 strict
    assert E.g1b_map(-0.02, 0.08) == "Inconclusive"    # straddle
    assert E.g1b_map(0.06, 0.09) == "Supported"
    return "strict inequalities at exactly 0.05 verified"


# ---------------------------------------------------------------- D. F6
@check("f6/curve-classes")
def _():
    assert E.gain_curve_class(0.05, 0.15, 0.25) == "monotone_increasing"
    assert E.gain_curve_class(0.10, 0.10, 0.10) == "flat"
    assert E.gain_curve_class(0.05, 0.15, 0.08) == "cap_supports"
    assert E.gain_curve_class(0.02, 0.10, -0.03) == "cap_supports"  # harms-helps
    assert E.gain_curve_class(0.15, 0.05, 0.10) == "other"
    assert E.gain_curve_class(0.05, 0.05, 0.15) != "monotone_increasing"  # strict
    return "monotone/flat/cap/harms-helps/other all classified"


# ---------------------------------------------------------------- E. F7
@check("f7/strict-gate-and-argmax")
def _():
    deltas = {(10, 6): 0.60, (12, 6): 0.40, (8, 4): 0.05}
    ok, sel, margin, passing = E.stage_a_gate(deltas, eps=0.05)
    assert ok and sel == (10, 6), f"{ok} {sel}"
    assert (10, 6) in passing and (8, 4) not in passing  # strict: 0.05 !> 0.05
    assert abs(margin - 0.20) < 1e-12, margin
    ok, _, _, _ = E.stage_a_gate(deltas, eps=0.60)
    assert not ok  # nothing strictly above
    ok, _, _, _ = E.stage_a_gate({(8, 4): -0.1}, eps=0.0)
    assert not ok
    return f"argmax (10,6), margin 0.20, strict->eps boundary respected"


@check("f7/tie-halts-loud")
def _():
    try:
        E.stage_a_gate({(10, 6): 0.5, (12, 8): 0.5, (8, 4): 0.1}, eps=0.0)
    except ValueError as e:
        assert "tie" in str(e).lower()
        return f"ValueError: {e}"
    raise AssertionError("tie did not halt")


@check("f7/single-passer-margin")
def _():
    ok, sel, margin, _ = E.stage_a_gate({(10, 6): 0.3, (8, 4): -0.2}, 0.0)
    assert ok and sel == (10, 6) and abs(margin - 0.3) < 1e-12
    return "lone passer: margin == its own delta"


# ---------------------------------------------------------------- F. verdict
def _stats(b, c, n=60):
    a = n - b - c
    assert a >= 0
    x = bits(n, range(a + c))          # x correct on a+c items
    y = bits(n, list(range(a)) + list(range(a + c, a + c + b)))
    return E.paired_contrast_stats(x, y)


@check("verdict/all-cells")
def _():
    base = {"D->S": False, "S->D": False, "RAND": False}
    # CONTINUE: Supported primary (b=14,c=2 -> L>0.05 verified), RAND beaten.
    prim = _stats(14, 2)
    assert E.g1b_map(prim["tango_L"], prim["tango_U"]) == "Supported"
    sec = dict(prim); sec["d_hat"] = 8 / 60
    v = E.adjudicate(prim, sec, dict(base), "flat")
    assert v[0] == "CONTINUE", v
    # KILL via dead contrast.
    prim = _stats(2, 12)
    assert E.g1b_map(prim["tango_L"], prim["tango_U"]) == "Not supported"
    sec = dict(prim); sec["d_hat"] = 1 / 60
    v = E.adjudicate(prim, sec, dict(base), "flat")
    assert v[0] == "KILL" and v[1] == "Not supported", v
    # KILL via RAND (primary inconclusive, D->S <= RAND on the point).
    prim = _stats(6, 4)
    assert E.g1b_map(prim["tango_L"], prim["tango_U"]) == "Inconclusive"
    sec = dict(prim); sec["d_hat"] = -1 / 60
    v = E.adjudicate(prim, sec, dict(base), "flat")
    assert v[0] == "KILL", v
    # PIVOT via B2 override (Supported primary + monotone curve).
    prim = _stats(14, 2)
    sec = dict(prim); sec["d_hat"] = 8 / 60
    v = E.adjudicate(prim, sec, dict(base), "monotone_increasing")
    assert v[0] == "PIVOT", v
    # PIVOT via helps-but-direction-unresolved.
    prim = _stats(6, 4)
    sec = dict(prim); sec["d_hat"] = 2 / 60
    beat = dict(base); beat["RAND"] = True
    v = E.adjudicate(prim, sec, beat, "flat")
    assert v[0] == "PIVOT", v
    # HELD.
    v = E.adjudicate(prim, sec, dict(base), "flat")
    assert v[0] == "HELD" and v[1] == "Inconclusive", v
    return "CONTINUE / KILLx2 / PIVOTx2 / HELD all adjudicated"


@check("verdict/b4-tension-held-not-killed")
def _():
    # d_hat <= 0 but CI reaches 0.05 -> Inconclusive -> HELD (never KILL).
    prim = _stats(4, 6)
    assert prim["d_hat"] <= 0
    assert E.g1b_map(prim["tango_L"], prim["tango_U"]) == "Inconclusive"
    sec = dict(prim); sec["d_hat"] = 2 / 60
    v = E.adjudicate(prim, sec,
                     {"D->S": False, "S->D": False, "RAND": False}, "flat")
    assert v[0] == "HELD", v
    return f"d_hat={prim['d_hat']:+.3f} CI=[{prim['tango_L']:+.3f},{prim['tango_U']:+.3f}] -> HELD"


# ---------------------------------------------------------------- G. probeset
@check("probeset/60-item-rebuild")
def _():
    bench = P.build_benchmark()
    assert len(bench) == 60
    for i, it in enumerate(bench):
        assert it["A"] and it["C"] and it["A"] != it["C"], i
        assert it["prompt"].endswith("Answer:"), i
    ids = [it["id"] for it in bench]
    assert len(set(ids)) == 60
    return "60 unique items, A/C fields present, prompts well-formed"


@check("probeset/decision-rule")
def _():
    chosen, ok = P.decide_from_logits(2.0, 1.0, "Mars", "Venus")
    assert (chosen, ok) == ("Mars", True)
    chosen, ok = P.decide_from_logits(1.0, 2.0, "Mars", "Venus")
    assert (chosen, ok) == ("Venus", False)
    chosen, ok = P.decide_from_logits(1.5, 1.5, "Mars", "Venus")
    assert (chosen, ok) == ("Venus", False)  # tie -> foil (EXP077 convention)
    return "A-wins / C-wins / tie->foil verified"


@check("probeset/pinned-archive-preflight")
def _():
    logs = []
    path = os.path.join(HERE, "..", "EXP077_cone_vs_line",
                        "exp077_instance_records.json")
    ps = P.load_probe_set(path, logs.append)
    assert len(ps["items"]) == 60
    assert ps["records_sha"] == P.RECORDS_SHA256
    assert any("DEVIATION" in m for m in logs), "D1 deviation not logged"
    return f"sha verified, alignment {ps['alignment_60']}/60, deviation logged"


# ---------------------------------------------------------------- H. ramping
@check("ramping/pinned-schedule")
def _():
    def close(x, y):
        return abs(x - y) < 1e-12
    assert RP.RAMP_SCHEDULE_ID == "F8-linear-10"
    a = 0.10
    assert close(RP.alpha_eff(a, 1), a * 0.1)
    assert close(RP.alpha_eff(a, 5), a * 0.5)
    assert RP.alpha_eff(a, 10) == a
    assert RP.alpha_eff(a, 11) == a
    assert RP.alpha_eff(a, 2048) == a
    assert RP.alpha_eff(0.0, 7) == 0.0
    v = RP.ramp_vector(0.10, 12)
    assert len(v) == 12 and close(v[0], 0.01)
    assert close(v[9], 0.10) and v[10] == v[11] == 0.10
    assert all(v[i] <= v[i + 1] + 1e-15 for i in range(11))  # monotone ramp
    return "t=1..10 linear ramp, t>=10 full, monotone"


@check("ramping/loud-validation")
def _():
    for args in [(0.1, 0), (0.1, -3), (-0.1, 5), (1.5, 5)]:
        try:
            RP.alpha_eff(*args)
        except ValueError:
            pass
        else:
            raise AssertionError(f"alpha_eff{args} did not raise")
    try:
        RP.ramp_vector(0.1, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("ramp_vector n=0 did not raise")
    return "t<1 / alpha outside [0,1] / n<1 all raise ValueError"


# ---------------------------------------------------------------- I. RNG
@check("rng/pins-and-contract")
def _():
    assert R.MASTER_SEED == 20260924 == R.RAND_SEED
    src = open(os.path.join(HERE, "exp088_rng.py")).read()
    assert "import numpy" not in src, "torch-exclusive contract broken"
    try:
        R.draw_rand_unit_vector(16)
    except RuntimeError as e:
        assert "torch" in str(e).lower()
        return f"pins 20260924; no-torch -> RuntimeError ({e})"
    raise AssertionError("draw did not raise without torch")


# ---------------------------------------------------------------- J. runner
@check("runner/refuses-without-clearance")
def _():
    import argparse
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        ns = argparse.Namespace(ceo_gpu_clearance=False,
                                bundle_review_signoff=False,
                                out=td, corpus=None, records=None)
        assert RUN.cmd_run(ns) == 2
        ns = argparse.Namespace(ceo_gpu_clearance=True,
                                bundle_review_signoff=False,
                                out=td, corpus=None, records=None)
        assert RUN.cmd_run(ns) == 2
        assert not os.path.exists(os.path.join(td, "exp088_results.json"))
    try:
        RUN.main([])
    except RuntimeError as e:
        assert "not licensed" in str(e)
        return "both flags required; bare main() raises; no artifact written"
    raise AssertionError("main([]) did not raise")


@check("runner/budget-ceiling")
def _():
    b = RUN.PassBudget(limit=5)
    b.charge(3); b.charge(2)
    assert b.used == 5
    try:
        b.charge(1)
    except RuntimeError as e:
        assert "PASS CEILING REFUSED" in str(e)
    else:
        raise AssertionError("ceiling not enforced")
    assert RUN.FWD_BUDGET == 1640 == RUN.STAGE_A_CALLS + RUN.STAGE_B_CALLS
    assert RUN.STAGE_A_CALLS == 20 * 25 and RUN.STAGE_B_CALLS == 60 + 540 * 2
    return "ceiling refuses call 6/5; FWD_BUDGET=1640 arithmetic pinned"


@check("runner/preflight-before-model-construction")
def _():
    import argparse
    import tempfile
    logs = []
    with tempfile.TemporaryDirectory() as td:
        # Missing corpus -> ApparatusError, before any torch/weight touch.
        ns = argparse.Namespace(corpus=os.path.join(td, "nope.json"),
                                records=None, out=td)
        try:
            RUN._startup_preflight(ns, logs.append, check_gpu=False)
        except RUN.ApparatusError as e:
            assert "corpus" in str(e).lower()
        else:
            raise AssertionError("missing corpus did not halt")
        # Corrupt corpus JSON -> ApparatusError.
        bad = os.path.join(td, "bad.json")
        open(bad, "w").write("{not json")
        ns = argparse.Namespace(corpus=bad, records=None, out=td)
        try:
            RUN._startup_preflight(ns, logs.append, check_gpu=False)
        except RUN.ApparatusError as e:
            assert "json" in str(e).lower()
        else:
            raise AssertionError("corrupt corpus did not halt")
    return "missing/corrupt corpus halts in preflight (no model built)"


@check("runner/preflight-passes-on-pinned-artifacts")
def _():
    import argparse
    logs = []
    ns = argparse.Namespace(corpus=None, records=None, out=None)
    try:
        RUN._startup_preflight(ns, logs.append, check_gpu=False)
    except RUN.ApparatusError as e:
        raise AssertionError(f"preflight failed on pinned artifacts: {e}")
    assert any("ALL CHECKS PASS" in m for m in logs)
    return "corpus+records+geometry+outdir verified (CPU smoke mode)"


@check("runner/geometry-drift-halts")
def _():
    import argparse
    logs = []
    ns = argparse.Namespace(corpus=None, records=None, out=None)
    old = RUN.N_LAYERS
    RUN.N_LAYERS = 25
    try:
        RUN._startup_preflight(ns, logs.append, check_gpu=False)
    except RUN.ApparatusError as e:
        assert "N_LAYERS" in str(e)
        return f"drift detected: {e}"
    finally:
        RUN.N_LAYERS = old
    raise AssertionError("geometry drift did not halt")


def main():
    passed, failed = 0, []
    for name, fn in CHECKS:
        try:
            detail = fn()
            print(f"PASS {name} :: {detail}")
            passed += 1
        except Exception as e:  # noqa: BLE001 - report, don't crash
            print(f"FAIL {name} :: {type(e).__name__}: {e}")
            failed.append(name)
    print(f"{passed}/{len(CHECKS)} evaluator checks pass")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
