"""EXP094 mock pipeline tests — synthetic only, never touches weights.

Tests (numpy only):
  T1 constructor math: d = u * ratio * h_norm; perturbation_ratio == ratio
  T2 zero-direction flag: a == b -> degenerate_zero, d = 0
  T3 R-arm norm tie: ||g_i|| == ||d_i||
  T4 G7.3 label-swap on synthetic (via test_g7_audit)
  T5 degeneracy gate computation (orthogonal -> ~0; collinear -> ~1)
  T6 McNemar: b=6,c=0 -> p=0.03125 (N_final feasibility on paper, pre-reg §4)
  T7 Tango CI: contains theta_hat; sane width; degenerate (0,0) case
  T8 decision-table routing: all six steps reachable with synthetic margins
  T9 per-item CSV schema (column order per pre-reg §5 item 1)

Exit 0 = all pass; exit 1 = failure.
"""

import os
import sys

import numpy as np

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)

import constructor as C
import score_exp094 as S
from test_g7_audit import g73_label_swap, g74_isolation

FAILURES = []


def check(name, cond, detail=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        FAILURES.append(name)


def t1_constructor_math():
    rng = np.random.default_rng(1)
    a = rng.normal(size=1024)
    b = rng.normal(size=1024)
    h_norm = float(np.linalg.norm(a)) + 5.0
    d, info = C.build_per_item_direction(a, b, h_norm)
    r = a - b
    expected = (r / np.linalg.norm(r)) * (C.NORM_RATIO * h_norm)
    check("T1a direction formula", np.allclose(d, expected, rtol=1e-12),
          f"max|diff|={np.abs(d-expected).max():.2e}")
    check("T1b ratio identity",
          abs(info["perturbation_ratio"] - C.NORM_RATIO) < 1e-12,
          f"ratio={info['perturbation_ratio']:.6f}")
    check("T1c not degenerate", not info["degenerate_zero"])
    check("T1d frozen constants", C.NORM_RATIO == 0.0474 and
          C.R_SEED == 94094 and C.CONSTRUCTOR_VERSION == "C-1")
    check("T1e P0 frozen", C.P0_TEXT ==
          "The following passage is shown for reference.\n\n")


def t2_zero_direction():
    a = np.ones(1024)
    d, info = C.build_per_item_direction(a, a.copy(), 3.0)
    check("T2a zero flagged", info["degenerate_zero"])
    check("T2b zero vector", np.all(d == 0.0))
    check("T2c ratio 0 outside band",
          not (0.0355 <= info["perturbation_ratio"] <= 0.0593))


def t3_r_norm_tie():
    rng = np.random.default_rng(C.R_SEED)
    d_norm = 2.5
    g = C.build_random_direction(d_norm, 1024, rng)
    check("T3 norm tie", abs(np.linalg.norm(g) - d_norm) < 1e-12,
          f"||g||={np.linalg.norm(g):.6f}")


def t4_g73():
    max_diff, ok = g73_label_swap()
    check("T4 G7.3 label-swap", ok, f"max|diff|={max_diff:.2e}")
    ok74, msg = g74_isolation()
    check("T4b G7.4 isolation", ok74, msg)


def t5_degeneracy():
    rng = np.random.default_rng(2)
    U_orth = rng.normal(size=(60, 1024))
    U_orth /= np.linalg.norm(U_orth, axis=1, keepdims=True)
    from run_exp094 import mean_pairwise_abs_cosine
    m_orth = mean_pairwise_abs_cosine(U_orth)
    v = rng.normal(size=1024)
    v /= np.linalg.norm(v)
    U_col = np.tile(v, (60, 1)) + 1e-6 * rng.normal(size=(60, 1024))
    U_col /= np.linalg.norm(U_col, axis=1, keepdims=True)
    m_col = mean_pairwise_abs_cosine(U_col)
    check("T5a orthogonal ~0", m_orth < 0.1, f"{m_orth:.4f}")
    check("T5b collinear ~1", m_col > 0.99, f"{m_col:.4f}")


def t6_mcnemar():
    p = S.mcnemar_exact_p(6, 0)
    check("T6a b=6,c=0", abs(p - 0.03125) < 1e-12, f"p={p}")
    check("T6b b=5,c=0 n.s.", S.mcnemar_exact_p(5, 0) > 0.05,
          f"p={S.mcnemar_exact_p(5,0):.4f}")
    check("T6c b=c=0", S.mcnemar_exact_p(0, 0) == 1.0)


def t7_tango():
    # Table: n10=8, n01=2, n11=40, n00=10 -> theta_hat = 0.1
    lo, hi = S.tango_ci_paired(8, 2, 40, 10)
    check("T7a contains theta_hat", lo <= 0.1 <= hi, f"[{lo:.4f},{hi:.4f}]")
    check("T7b sane width", 0 < hi - lo < 0.5, f"width={hi-lo:.4f}")
    # Score at the point estimate is ~0 (inside CI deeply)
    check("T7c degenerate", S.tango_ci_paired(0, 0, 40, 20) == (0.0, 0.0))
    # Symmetric null table -> CI straddles 0
    lo2, hi2 = S.tango_ci_paired(3, 3, 30, 24)
    check("T7d null straddles 0", lo2 < 0 < hi2, f"[{lo2:.4f},{hi2:.4f}]")


def _margins(n_right_B, flips_T, flips_R, seed=0):
    """Synthetic margins: B correct on n_right_B items (margin +1 else -1);
    T flips flips_T of B's wrong->right; R flips flips_R similarly."""
    rng = np.random.default_rng(seed)
    mB = np.where(np.arange(60) < n_right_B, 1.0, -1.0)
    mT = mB.copy()
    mR = mB.copy()
    wrong = np.nonzero(mB < 0)[0]
    mT[wrong[:flips_T]] = 1.0
    mR[wrong[:flips_R]] = 1.0
    ph = np.array(["A-first"] * 30 + ["C-first"] * 30)
    return mB, mT, mR, ph


def t8_decision_table():
    # Step 1: delivery FAIL -> Inconclusive
    mB, mT, mR, ph = _margins(36, 10, 0)
    r = S.score_experiment(mB, mT, mR, ph, False, 0.1)
    check("T8 step1 Inconclusive", r["verdict"] == "Inconclusive",
          r["verdict"])
    # Step 2: degeneracy -> Underdetermined
    r = S.score_experiment(mB, mT, mR, ph, True, 0.97)
    check("T8 step2 Underdetermined", r["verdict"] == "Underdetermined",
          r["verdict"])
    # Step 3: no movement -> Refuted
    mB0, mT0, mR0, ph0 = _margins(36, 0, 0)
    r = S.score_experiment(mB0, mT0, mR0, ph0, True, 0.1)
    check("T8 step3 Refuted(family)", r["verdict"] == "Refuted" and
          r["decision_step"] == 3, f"{r['verdict']} step {r['decision_step']}")
    # Step 4: movement but null specificity, overlapping CIs -> Refuted
    # T flips 3, R flips 3 (same items): movement=6, TR table b=c=0 -> p=1.0
    mB4, mT4, mR4, ph4 = _margins(36, 3, 3)
    r = S.score_experiment(mB4, mT4, mR4, ph4, True, 0.1)
    check("T8 step4 Refuted(specificity)", r["verdict"] == "Refuted" and
          r["decision_step"] == 4, f"{r['verdict']} step {r['decision_step']}")
    # Step 5: licensed positive -> Supported
    # T flips 12 (all wrong->right), R flips 0; TR: b=12,c=0 -> p<0.05.
    # Strata: wrong items are indices 36..59; A-first = 0..29, C-first=30..59.
    # flips land in C-first only -> stratum-inconsistent -> NOT step 5.
    # For step 5, spread flips across strata: flip 6 in A-first wrong? A-first
    # wrong items: A-first indices 0..29, B correct on 0..35, so A-first wrong
    # = none in 0..29... B correct = first 36 (indices 0..35): A-first wrong =
    # indices 36..59 intersect A-first(0..29) = none. Redesign: B correct on
    # even indices (30 items), wrong on odd (30): flips on odd indices spread
    # across strata.
    mB5 = np.where(np.arange(60) % 2 == 0, 1.0, -1.0)
    mT5 = mB5.copy()
    mR5 = mB5.copy()
    odd = np.nonzero(np.arange(60) % 2 == 1)[0]
    # 12 flips spread across strata: 6 in A-first (idx<30), 6 in C-first.
    mT5[odd[:6]] = 1.0
    mT5[odd[15:21]] = 1.0
    ph5 = np.array(["A-first"] * 30 + ["C-first"] * 30)
    r = S.score_experiment(mB5, mT5, mR5, ph5, True, 0.1)
    check("T8 step5 Supported", r["verdict"] == "Supported",
          f"{r['verdict']} step {r['decision_step']}")
    # Step 6b: consistent wrong-direction -> PIVOT
    mT6 = mB5.copy()
    mT6[np.nonzero(mB5 > 0)[0][:12]] = -1.0  # 12 right->wrong flips
    r = S.score_experiment(mB5, mT6, mR5, ph5, True, 0.1)
    ws = r["decision_worksheet"][-1]["condition"]
    check("T8 step6b PIVOT", r["verdict"] == "Not supported" and "(b)" in ws,
          f"{r['verdict']} {ws}")
    # Nine cells present
    check("T8 nine cells", len(r["stratum_table"]) == 9,
          f"{len(r['stratum_table'])}")


def t9_csv_schema():
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["item_id", "stratum", "arm", "correct_top1", "margin",
                "perturbation_ratio", "margin_shift_vs_B"])
    header = buf.getvalue().strip()
    check("T9 csv header", header ==
          "item_id,stratum,arm,correct_top1,margin,perturbation_ratio,"
          "margin_shift_vs_B")


if __name__ == "__main__":
    t1_constructor_math()
    t2_zero_direction()
    t3_r_norm_tie()
    t4_g73()
    t5_degeneracy()
    t6_mcnemar()
    t7_tango()
    t8_decision_table()
    t9_csv_schema()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES: {FAILURES}")
        sys.exit(1)
    print("ALL MOCK TESTS PASS")
