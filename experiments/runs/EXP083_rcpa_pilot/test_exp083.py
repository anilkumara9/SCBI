"""EXP083 (R1 RCPA kill pilot) — evaluator tests (LOG-258, Law #15).

Seeded, deterministic, CPU-runnable (stdlib only; the numpy cross-check for
the G-norm interpolation is conditional on numpy being importable).
Covers:

  1. the canonical Tango table (§13.2 / §8 F1 correction), computed from
     the protocol's own specified computation (constrained-MLE score,
     Tango 1998) — no trusted library values smuggled in:
       one-sided 95% upper  0.043147 at N=60 (flat b=c=0)
       two-sided 95%        [-0.0602, +0.0602] at N=60
       one-sided 95% upper  0.045315 at N_final=57 (KILL_flat canonical, R1)
       two-sided 95%        [-0.0631, +0.0631] at N_final=57
       0.056902 (b=c=1 boundary check)
       exact one-sided McNemar p 0.015625 at b=6, c=0 (MDE anchor)
  2. McNemar one-sided exactness (integer arithmetic vs Fraction) +
     directionality;
  3. Tango score properties (z anchors, McNemar reduction at delta=0,
     arm-swap symmetry, containment, determinism, monotonicity);
  4. the §8 verdict table: RE-SKIN / KILL_gross / KILL_flat / CONTINUE /
     HELD (straddle, underpowered-flat, sub-claim) / INVALID precedence;
  5. G-norm: type-7 interpolation pinned (numpy cross-check), strictly-
     below semantics, deterministic N_final=57, tie edge case, fault;
  6. G-static: 0.5 bar, chance anchor, fault modes;
  7. G-curve: report-only rescaling fraction;
  8. budget: pass-193 hard stop, 192 inventory encoded;
  9. position rule (§3.3): anchor search, char->token mapping, faults;
 10. seed scheme (20260924+i), torch-exclusivity (R5), archive anchor
     (EXP077 C1 accuracy 0.60, headroom gate).

Run:  python3 test_exp083.py   (from the EXP083_rcpa_pilot directory)
Exit 0 + ALL TESTS PASSED iff every test passes.
"""

import os
import sys
import json
import math
import random
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp083_endpoints import (flip_indicators, paired_flip_table,
                              mcnemar_one_sided_p, tango_score_z, tango_ci,
                              tango_one_sided_upper, flip_contrast_stats,
                              adjudicate_verdict, _z_for_alpha, _phi_inv)
from exp083_guards import (PassCounter, PassBudgetExceeded, MAX_PASSES,
                           HARD_STOP, EXPECTED_SHA256, sha_prerun_check,
                           identity_check, percentile_type7, g_norm_floor,
                           g_static_check, g_curve_rescale, D_MODEL,
                           N_ITEMS, STATIC_COS_BAR)
from exp083_position import q_char_offset, char_offset_to_token, locate_positions
from exp083_random import g_hat_seed, g_hat_seeds, generate_g_hat

HERE = os.path.dirname(os.path.abspath(__file__))
ARCH_RECORDS = os.path.normpath(os.path.join(
    HERE, "..", "EXP077_cone_vs_line", "exp077_instance_records.json"))

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"  [{PASS if cond else FAIL}] {name}" + (f" — {detail}" if detail and not cond else ""))


# ================================================================ 1. canonical table
def test_canonical_table():
    # One-sided 95% Tango upper at the flat table, N=60: 0.043147 (§8, N=60 reference).
    u60 = tango_one_sided_upper(60, 0, 0, 0)
    check("canonical: one-sided 95% upper at N=60 (flat) == 0.043147 (6dp)",
          abs(u60 - 0.043147) < 5e-7, f"got {u60:.6f}")
    check("canonical: one-sided 95% upper at N=60 == 0.0431 (4dp form)",
          round(u60, 4) == 0.0431, f"got {u60:.6f}")
    # Two-sided 95% at N=60: [-0.0602, +0.0602].
    L60, U60 = tango_ci(60, 0, 0, 0)
    check("canonical: two-sided 95% CI at N=60 == [-0.0602, +0.0602] (4dp)",
          round(L60, 4) == -0.0602 and round(U60, 4) == 0.0602,
          f"got ({L60:.6f}, {U60:.6f})")
    # One-sided 95% upper at N_final=57: 0.045315 (KILL_flat canonical, R1).
    u57 = tango_one_sided_upper(57, 0, 0, 0)
    check("canonical: one-sided 95% upper at N_final=57 (flat) == 0.045315 (6dp)",
          abs(u57 - 0.045315) < 5e-7, f"got {u57:.6f}")
    # Two-sided 95% at N_final=57: [-0.0631, +0.0631].
    L57, U57 = tango_ci(57, 0, 0, 0)
    check("canonical: two-sided 95% CI at N_final=57 == [-0.0631, +0.0631] (4dp)",
          round(L57, 4) == -0.0631 and round(U57, 4) == 0.0631,
          f"got ({L57:.6f}, {U57:.6f})")
    # 0.056902: the b=c=1 boundary check (one-sided upper).
    u11 = tango_one_sided_upper(58, 1, 1, 0)
    check("canonical: one-sided 95% upper at b=c=1 (N=60) == 0.056902 (6dp)",
          abs(u11 - 0.056902) < 5e-7, f"got {u11:.6f}")
    # MDE anchor: exact one-sided McNemar p = 0.015625 at b=6, c=0.
    check("canonical: one-sided McNemar p at b=6,c=0 == 0.015625 (exact)",
          mcnemar_one_sided_p(6, 0) == 0.015625,
          f"got {mcnemar_one_sided_p(6, 0)}")
    # Tie edge case (§5 G-norm): N_final=58 flat -> 0.044568 < 0.05.
    u58 = tango_one_sided_upper(58, 0, 0, 0)
    check("canonical: one-sided 95% upper at N_final=58 (flat) == 0.044568 (6dp)",
          abs(u58 - 0.044568) < 5e-7, f"got {u58:.6f}")
    # Monotone tightening with N at the flat table.
    check("canonical: flat one-sided upper tightens with N (52..60)",
          all(tango_one_sided_upper(n, 0, 0, 0) > tango_one_sided_upper(n + 1, 0, 0, 0)
              for n in range(52, 60)))
    # Firing boundary: N_final >= 52 fires KILL_flat; N_final = 51 holds.
    check("canonical: flat bar fires at N_final=52",
          tango_one_sided_upper(52, 0, 0, 0) < 0.05,
          f"got {tango_one_sided_upper(52, 0, 0, 0):.6f}")
    check("canonical: flat bar holds at N_final=51 (underpowered)",
          tango_one_sided_upper(51, 0, 0, 0) >= 0.05,
          f"got {tango_one_sided_upper(51, 0, 0, 0):.6f}")


# ================================================================ 2. McNemar one-sided
def test_mcnemar_one_sided():
    # Integer-exactness: compare against Fraction arithmetic.
    for (b, c) in [(6, 0), (0, 6), (3, 9), (9, 3), (1, 1), (14, 0), (5, 5)]:
        s = b + c
        ref = float(sum(Fraction(math.comb(s, k), 2 ** s) for k in range(b, s + 1)))
        check(f"mcnemar-1s: integer-exact at b={b},c={c}",
              mcnemar_one_sided_p(b, c) == ref,
              f"got {mcnemar_one_sided_p(b, c)}, ref {ref}")
    check("mcnemar-1s: b=c=0 -> 1.0 (no discordant evidence)", mcnemar_one_sided_p(0, 0) == 1.0)
    # Directionality: evidence against A_r gives a large one-sided p.
    check("mcnemar-1s: b=0,c=6 -> 1.0 (effect in the wrong direction)",
          mcnemar_one_sided_p(0, 6) == 1.0)
    check("mcnemar-1s: monotone decreasing in b at fixed s",
          all(mcnemar_one_sided_p(b, 6 - b) >= mcnemar_one_sided_p(b + 1, 5 - b)
              for b in range(6)))
    # The reviewer's two-sided 0.03125 is exactly twice the pinned one-sided value.
    check("mcnemar-1s: 0.015625 is half the two-sided 0.03125 (F1 correction)",
          abs(mcnemar_one_sided_p(6, 0) * 2 - 0.03125) < 1e-15)


# ================================================================ 3. Tango properties
def test_tango_properties():
    check("z two-sided(0.05) == 1.959964 (tol 1e-6)",
          abs(_z_for_alpha(0.05) - 1.959963984540054) < 1e-6)
    check("z one-sided(0.95) == 1.6449 (tol 1e-3)",
          abs(_phi_inv(0.95) - 1.6449) < 1e-3, f"got {_phi_inv(0.95):.6f}")
    # Score statistic reduces to McNemar's score at delta=0.
    for (n11, n12, n21, n22) in [(36, 14, 0, 10), (20, 8, 3, 29), (0, 6, 0, 54)]:
        z0 = tango_score_z(n11, n12, n21, n22, 0.0)
        mcn = (n12 - n21) / math.sqrt(n12 + n21)
        check(f"tango Z(0)==McNemar score for {(n11,n12,n21,n22)}",
              abs(z0 - mcn) < 1e-12)
    # CI contains the point estimate; arm-swap symmetry.
    rng = random.Random(20260924)
    sym_ok, contain_ok = True, True
    for _ in range(25):
        cells = [rng.randint(0, 30) for _ in range(4)]
        n11, n12, n21, n22 = cells
        L, U = tango_ci(n11, n12, n21, n22)
        d = (n12 - n21) / sum(cells)
        if not (L - 1e-12 <= d <= U + 1e-12):
            contain_ok = False
        Ls, Us = tango_ci(n11, n21, n12, n22)
        if not (abs(L + Us) < 1e-9 and abs(U + Ls) < 1e-9):
            sym_ok = False
    check("tango: CI contains the point estimate (25 random tables)", contain_ok)
    check("tango: arm-swap symmetry (25 tables)", sym_ok)
    check("tango: deterministic (repeat identical)",
          tango_ci(36, 14, 0, 10) == tango_ci(36, 14, 0, 10)
          and tango_one_sided_upper(60, 0, 0, 0) == tango_one_sided_upper(60, 0, 0, 0))
    # One-sided upper is strictly below the two-sided upper (directional bar).
    check("one-sided U_1s < two-sided U for every canonical table",
          all(tango_one_sided_upper(*c) < tango_ci(*c)[1]
              for c in [(60, 0, 0, 0), (57, 0, 0, 0), (58, 1, 1, 0), (0, 6, 0, 51)]))
    # Monotonicity of Z in delta.
    mono_ok = True
    for (n11, n12, n21, n22) in [(36, 14, 0, 10), (0, 6, 0, 54), (30, 0, 0, 30)]:
        prev = None
        for k in range(401):
            d_ = -0.999 + k * (1.998 / 400)
            z_ = tango_score_z(n11, n12, n21, n22, d_)
            if prev is not None and z_ > prev + 1e-9:
                mono_ok = False
            prev = z_
    check("tango: Z(delta) monotone decreasing (3 tables x 401 grid)", mono_ok)


# ================================================================ 4. verdict table
def _base_args(**kw):
    d = dict(sha_prerun_ok=True, identity_ok=True, guard_fault=None,
             g_static_fired=False, g_static_value=0.02,
             g_norm_n_excluded=3, g_norm_floor=0.965,
             g_flips=[], r_flips=[])
    d.update(kw)
    return d


def test_verdict_kill_flat():
    # Flat world at canonical N_final=57 -> KILL_flat (one-sided bar).
    rec = adjudicate_verdict(**_base_args(g_flips=[0] * 57, r_flips=[0] * 57))
    check("verdict KILL_flat: b=c=0 at N_final=57 -> KILL",
          rec["row"] == "KILL" and "KILL_flat" in rec["row_detail"]
          and rec["verdict"] == "Not supported", rec["row_detail"])
    check("verdict KILL_flat: canonical upper 0.045315 recorded",
          abs(rec["contrast"]["tango_U_1s"] - 0.045315) < 5e-7)
    # Flat at N=60 reference -> KILL_flat with 0.043147.
    rec60 = adjudicate_verdict(**_base_args(g_flips=[0] * 60, r_flips=[0] * 60))
    check("verdict KILL_flat: b=c=0 at N=60 -> KILL (0.043147 reference)",
          rec60["row"] == "KILL" and abs(rec60["contrast"]["tango_U_1s"] - 0.043147) < 5e-7)
    # The F1 correction: the two-sided CI does NOT fire KILL_gross on the flat.
    L, U = rec["contrast"]["tango_L"], rec["contrast"]["tango_U"]
    check("verdict F1 correction: flat two-sided CI straddles (KILL_gross must not fire)",
          L <= 0.05 <= U, f"CI=({L:.4f},{U:.4f})")


def test_verdict_kill_gross():
    # Negative table: CI entirely below +0.05 -> KILL_gross.
    g = [1] * 8 + [0] * 49
    r = [1] * 2 + [0] * 55  # first two overlap -> b=0, c=6
    rec = adjudicate_verdict(**_base_args(g_flips=g, r_flips=r))
    st = rec["contrast"]
    check("verdict KILL_gross: CI entirely below +0.05 -> KILL",
          rec["row"] == "KILL" and "KILL_gross" in rec["row_detail"]
          and st["tango_U"] < 0.05, rec["row_detail"])


def test_verdict_continue_mde_anchor():
    # MDE anchor: b=6, c=0 at N_final=57 -> CONTINUE (Delta=6/57, p=0.015625).
    g = [0] * 57
    r = [1] * 6 + [0] * 51
    rec = adjudicate_verdict(**_base_args(g_flips=g, r_flips=r))
    st = rec["contrast"]
    check("verdict CONTINUE: MDE anchor b=6,c=0 at N_final=57 -> CONTINUE",
          rec["row"] == "CONTINUE", rec["row_detail"])
    check("verdict CONTINUE: Delta=6/57 >= 0.05, p=0.015625 <= 0.05",
          abs(st["d_hat"] - 6 / 57) < 1e-12 and st["mcnemar_p_1s"] == 0.015625
          and st["b"] == 6 and st["c"] == 0)
    check("verdict CONTINUE: evidentiary verdict is Inconclusive (never a claim)",
          rec["verdict"] == "Inconclusive" and "never a capability claim" in rec["license"])
    # CONTINUE requires the p conjunct: Delta >= 0.05 but p > 0.05 -> not CONTINUE.
    g2 = [0] * 57
    r2 = [1] * 4 + [0] * 53  # b=4, c=0: p = 1/16 = 0.0625 > 0.05
    rec2 = adjudicate_verdict(**_base_args(g_flips=g2, r_flips=r2))
    check("verdict: Delta>=0.05 but p=0.0625>0.05 -> not CONTINUE",
          rec2["row"] != "CONTINUE", f"row={rec2['row']}")


def test_verdict_held():
    # Straddle: b=2, c=0 at N=57 -> CI straddles +0.05 -> HELD.
    g = [0] * 57
    r = [1] * 2 + [0] * 55
    rec = adjudicate_verdict(**_base_args(g_flips=g, r_flips=r))
    st = rec["contrast"]
    check("verdict HELD: straddle table -> HELD (Inconclusive)",
          rec["row"] == "HELD" and rec["verdict"] == "Inconclusive"
          and st["tango_L"] <= 0.05 <= st["tango_U"],
          f"row={rec['row']}, CI=({st['tango_L']:.4f},{st['tango_U']:.4f})")
    check("verdict HELD: never CONTINUE",
          "never CONTINUE" in rec["license"])
    # Underpowered flat: b=c=0 at N_final=51 -> HELD (not KILL_flat).
    rec51 = adjudicate_verdict(**_base_args(g_flips=[0] * 51, r_flips=[0] * 51))
    check("verdict HELD: b=c=0 at N_final=51 -> HELD (underpowered flat)",
          rec51["row"] == "HELD" and "underpowered" in rec51["row_detail"],
          rec51["row_detail"])


def test_verdict_reskin():
    # G-static fires on a validated apparatus -> RE-SKIN KILL, even with
    # strong flip data (flip arms would not have run; the adjudicator
    # still preempts).
    g = [0] * 57
    r = [1] * 6 + [0] * 51
    rec = adjudicate_verdict(**_base_args(g_flips=g, r_flips=r,
                                          g_static_fired=True, g_static_value=0.72))
    check("verdict RE-SKIN: G-static fires on validated apparatus -> RE-SKIN KILL",
          rec["row"] == "RE-SKIN KILL" and rec["verdict"] == "Not supported",
          rec["row_detail"])
    # RE-SKIN never fires on a broken apparatus (M1): SHA failure preempts.
    rec2 = adjudicate_verdict(**_base_args(sha_prerun_ok=False,
                                           g_static_fired=True, g_static_value=0.72,
                                           g_flips=g, r_flips=r))
    check("verdict M1: broken apparatus can never record RE-SKIN KILL",
          rec2["row"] == "INVALID" and "INVALID(i)" in rec2["row_detail"])


def test_verdict_invalid_precedence():
    g = [0] * 57
    r = [1] * 6 + [0] * 51
    rec = adjudicate_verdict(**_base_args(sha_prerun_ok=False, identity_ok=False,
                                          guard_fault="g-norm fault",
                                          g_static_fired=True, g_static_value=0.9,
                                          g_flips=g, r_flips=r))
    check("INVALID precedence: (i) preempts (ii), (iii), RE-SKIN, flip rows",
          rec["row"] == "INVALID" and "INVALID(i)" in rec["row_detail"]
          and rec["verdict"] == "Underdetermined", rec["row_detail"])
    rec = adjudicate_verdict(**_base_args(identity_ok=False, guard_fault="x",
                                          g_flips=g, r_flips=r))
    check("INVALID precedence: (ii) preempts (iii)",
          "INVALID(ii)" in rec["row_detail"], rec["row_detail"])
    rec = adjudicate_verdict(**_base_args(guard_fault="g-static fault",
                                          g_flips=g, r_flips=r))
    check("INVALID precedence: (iii) preempts flip rows",
          rec["row"] == "INVALID" and "INVALID(iii)" in rec["row_detail"])


# ================================================================ 5. G-norm
def test_g_norm():
    # Fixture: 3 small norms + 57 large -> interpolated floor excludes exactly 3.
    norms = [0.10, 0.20, 0.30] + [1.00 + 0.01 * i for i in range(57)]
    floor, excluded, n_final = g_norm_floor(norms)
    exp_floor = 0.30 + 0.95 * (1.00 - 0.30)  # position (60-1)*0.05 = 2.95
    check("G-norm: linear-interpolation floor (type 7, pos 2.95)",
          abs(floor - exp_floor) < 1e-12, f"floor={floor}, expected={exp_floor}")
    check("G-norm: strictly-below exclusion -> exactly 3 excluded, N_final=57",
          excluded == [0, 1, 2] and n_final == 57,
          f"excluded={excluded}, n_final={n_final}")
    try:
        import numpy as np
        check("G-norm: matches numpy.percentile default (type 7)",
              abs(floor - float(np.percentile(norms, 5))) < 1e-12,
              f"numpy={float(np.percentile(norms, 5))}")
    except ImportError:
        check("G-norm: numpy cross-check skipped (numpy absent)", True)
    # Strictly-below, not <=: a value exactly AT the floor is included.
    norms2 = list(norms)
    norms2[3] = floor  # the smallest large value sits exactly on the floor
    _, excluded2, n_final2 = g_norm_floor(norms2)
    check("G-norm: value exactly at floor is NOT excluded (<, not <=)",
          excluded2 == [0, 1, 2] and n_final2 == 57)
    # Computation fault: non-finite norm -> ValueError (INVALID(iii) upstream).
    bad = list(norms)
    bad[7] = float("nan")
    fault = False
    try:
        g_norm_floor(bad)
    except ValueError:
        fault = True
    check("G-norm: non-finite norm raises (computation fault)", fault)
    # Wrong count -> ValueError.
    fault2 = False
    try:
        g_norm_floor([1.0] * 59)
    except ValueError:
        fault2 = True
    check("G-norm: != 60 norms raises", fault2)


# ================================================================ 6. G-static
def _unit(i, d=D_MODEL):
    v = [0.0] * d
    v[i % d] = 1.0
    return v


def test_g_static():
    # Identical directions -> mean cos = 1.0 > 0.5 -> fires.
    fired, mc = g_static_check([_unit(0)] * 10)
    check("G-static: identical unit vectors fire (mean cos = 1.0)",
          fired and abs(mc - 1.0) < 1e-12, f"mean_cos={mc}")
    # Orthogonal directions -> mean cos = 0 -> does not fire.
    fired2, mc2 = g_static_check([_unit(i) for i in range(10)])
    check("G-static: orthogonal vectors do not fire (mean cos = 0)",
          (not fired2) and abs(mc2) < 1e-12, f"mean_cos={mc2}")
    # Chance anchor: |cos| ~ 0.1 is already far above chance for d=1024 —
    # the 0.5 bar is far above the chance scale.
    check("G-static: bar 0.5 >> chance scale 1/sqrt(1024)",
          STATIC_COS_BAR > 10 / math.sqrt(D_MODEL))
    # Faults: non-unit input, wrong dim, < 2 items.
    for name, vecs in [("non-unit", [[2.0] + [0.0] * (D_MODEL - 1)] * 3),
                       ("wrong dim", [[1.0] * 512] * 3),
                       ("<2 items", [_unit(0)])]:
        fault = False
        try:
            g_static_check(vecs)
        except ValueError:
            fault = True
        check(f"G-static: {name} raises (computation fault)", fault)


# ================================================================ 7. G-curve
def test_g_curve():
    # r = h_a exactly -> rescaling fraction 1.0; r orthogonal -> 0.0.
    h = [_unit(0), _unit(1)]
    f1 = g_curve_rescale([_unit(0), _unit(1)], h)
    check("G-curve: r=h_a -> fraction 1.0 (report-only)", abs(f1 - 1.0) < 1e-12)
    f0 = g_curve_rescale([_unit(2), _unit(3)], h)
    check("G-curve: r orthogonal to h_a -> fraction 0.0", abs(f0) < 1e-12)
    # Length mismatch -> fault.
    fault = False
    try:
        g_curve_rescale([_unit(0)], h)
    except ValueError:
        fault = True
    check("G-curve: length mismatch raises", fault)


# ================================================================ 8. budget
def test_budget():
    check("budget: MAX_PASSES == 192 (180 + <=12 smoke + $0 identity)",
          MAX_PASSES == 192)
    check("budget: HARD_STOP == 193", HARD_STOP == 193)
    pc = PassCounter()
    pc.use(12, "smoke")
    pc.use(60, "clean-read")
    pc.use(60, "A_r")
    pc.use(48, "A_g partial")
    check("budget: licensed blocks accumulate (12+60+60+48=180)",
          pc.total == 180, f"total={pc.total}")
    refused = False
    try:
        pc.use(13, "would exceed")
    except PassBudgetExceeded:
        refused = True
    check("budget: allocation past 192 refused", refused)
    pc2 = PassCounter()
    pc2.use(192, "full inventory")
    refused2 = False
    try:
        pc2.use(1, "pass 193")
    except PassBudgetExceeded:
        refused2 = True
    check("budget: pass 193 refused (hard stop)", refused2)
    neg = False
    try:
        PassCounter().use(-1, "negative")
    except ValueError:
        neg = True
    check("budget: negative allocation rejected", neg)
    inv = pc2.inventory()
    check("budget: inventory encodes the licensed block table",
          inv["licensed"] == {"smoke_max": 12, "clean_read": 60,
                              "arm_r": 60, "arm_g": 60, "arm_0": 0}
          and inv["hard_stop"] == 193)


# ================================================================ 9. position rule
def test_position_rule():
    prompt = ("Premise: A outranks B. B outranks C. "
              "Question: Who is higher in rank, A or C? Answer:")
    idx = q_char_offset(prompt)
    check("position: q_char_offset finds the '?' of '? Answer:'",
          prompt[idx] == "?" and prompt[idx:idx + 9] == "? Answer:",
          f"idx={idx}")
    # Synthetic whitespace-token spans.
    spans, s = [], 0
    for tok in prompt.split(" "):
        st = prompt.find(tok, s)
        spans.append((st, st + len(tok)))
        s = st + len(tok)
    q_tok = char_offset_to_token(idx, spans)
    check("position: char offset maps to the '?' token",
          "?" in prompt[spans[q_tok][0]:spans[q_tok][1]], f"tok={q_tok}")
    ans_pos, q_pos = locate_positions(prompt, spans)
    check("position: ans_pos = T-1, q_pos strictly before ans_pos",
          ans_pos == len(spans) - 1 and 0 <= q_pos < ans_pos,
          f"ans={ans_pos}, q={q_pos}")
    # Faults: anchor absent; offset uncovered.
    fault = False
    try:
        q_char_offset("no anchor here")
    except ValueError:
        fault = True
    check("position: missing '? Answer:' anchor raises (no silent default)", fault)
    fault2 = False
    try:
        char_offset_to_token(10 ** 9, spans)
    except ValueError:
        fault2 = True
    check("position: uncovered char offset raises", fault2)


# ================================================================ 10. seeds, torch, archive
def test_seeds_and_random():
    check("seeds: master seed S0 = 20260924", g_hat_seed(0) == 20260924)
    check("seeds: per-item seed = 20260924 + i",
          g_hat_seed(5) == 20260929 and g_hat_seed(59) == 20260983)
    seeds = g_hat_seeds(60)
    check("seeds: 60 pairwise-distinct seeds", len(set(seeds)) == 60)
    check("seeds: deterministic across calls", g_hat_seeds(60) == g_hat_seeds(60))
    # R5: torch is the sole ĝ_i generator — this module must not import numpy.
    # (Check import statements, not the substring: the docstring names numpy
    # only to record the exclusion.)
    import re as _re
    import exp083_random
    src = open(exp083_random.__file__, encoding="utf-8").read()
    check("R5: exp083_random never imports numpy (torch exclusivity)",
          not _re.search(r"^\s*(import|from)\s+numpy", src, _re.M))
    # torch absent on the CPU build machine -> clear error, never silent fallback.
    err = False
    try:
        generate_g_hat(0)
    except RuntimeError as e:
        err = "torch" in str(e)
    check("random: generate_g_hat refuses without torch (no silent fallback)", err)


def test_archive_anchor():
    with open(ARCH_RECORDS, encoding="utf-8") as f:
        recs = json.load(f)
    c1 = [bool(r["correct"]["C1"]) for r in recs]
    acc = sum(c1) / len(c1)
    check("archive: 60 EXP077 instance records", len(recs) == 60)
    check("archive: C1 accuracy = 0.60 (§3.2 baseline license)",
          abs(acc - 0.60) < 1e-12, f"acc={acc}")
    check("archive: headroom gate [40%, 70%] PASS", 0.40 <= acc <= 0.70)
    # flip_indicators: structural zeros for baseline-right items.
    fl = flip_indicators([True, False, False], [True, True, False])
    check("flip indicators: wrong-at-baseline AND right-under-arm (structural zeros)",
          fl == [0, 1, 0], f"got {fl}")
    t = paired_flip_table([0, 1, 0], [1, 1, 0])
    check("paired flip table: b=A_r-only, c=A_g-only, d_hat=(b-c)/n",
          t["b"] == 1 and t["c"] == 0 and abs(t["d_hat"] - 1 / 3) < 1e-12,
          f"b={t['b']}, c={t['c']}, d={t['d_hat']}")


def test_sha_and_identity_guards():
    ok, _ = sha_prerun_check(EXPECTED_SHA256)
    check("SHA: pinned expected hash passes", ok)
    ok2, cause2 = sha_prerun_check("ab" * 32)
    check("SHA: wrong pre-run hash -> INVALID(i)", (not ok2) and "INVALID(i)" in cause2)
    check("SHA: expected hash is the protocol-pinned 4c242d...dd",
          EXPECTED_SHA256 == "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd")
    ok3, _ = identity_check([True, False], [True, False])
    check("identity: bit-for-bit match -> ok", ok3)
    ok4, cause4 = identity_check([True, True], [True, False])
    check("identity: mismatch -> INVALID(ii)", (not ok4) and "INVALID(ii)" in cause4)


def main():
    print("EXP083 evaluator tests (LOG-258) — seeded, deterministic, CPU-only")
    print("-" * 70)
    test_canonical_table()
    test_mcnemar_one_sided()
    test_tango_properties()
    test_verdict_kill_flat()
    test_verdict_kill_gross()
    test_verdict_continue_mde_anchor()
    test_verdict_held()
    test_verdict_reskin()
    test_verdict_invalid_precedence()
    test_g_norm()
    test_g_static()
    test_g_curve()
    test_budget()
    test_position_rule()
    test_seeds_and_random()
    test_archive_anchor()
    test_sha_and_identity_guards()
    print("-" * 70)
    n_fail = sum(1 for _, ok, _ in results if not ok)
    print(f"{len(results) - n_fail}/{len(results)} tests passed")
    if n_fail:
        print("FAILURES:")
        for name, ok, detail in results:
            if not ok:
                print(f"  - {name}: {detail}")
        print("EXP083 EVALUATOR TESTS: FAILURES PRESENT")
        return 1
    print("ALL EXP083 EVALUATOR TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
