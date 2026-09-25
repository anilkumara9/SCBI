#!/usr/bin/env python3
"""EXP086 evaluator test suite (CPU, synthetic fixtures).

Tests the protocol decision logic from scratch: guards/pins, Henrici index
vs a closed-form 2x2 reference, the seed contract, exact McNemar, the Tango
95% CI (constrained-MLE derivation cross-checked against an independent
dense-grid argmax + score-inversion self-consistency), ĉ/exceedance, the
signed ledger, the full §9 verdict table incl. precedence, runner refusals,
and the crash-guard.

GPU-node paths (torch, model weights) are NOT executed here. All tests are
deterministic; no randomness beyond pinned seeds.

Run: python3 test_exp086.py
Exit 0 iff all tests pass. Prints TAP-like lines.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import exp086_guards as G
import exp086_henrici as H
import exp086_rng as R
import exp086_statistics as S
import exp086_verdicts as V
import run_exp086 as RUN

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


# ---------------------------------------------------------------------------
# 1. Signed pins (§1, §4, §6, §11)
# ---------------------------------------------------------------------------
check("pin MODEL_ID", G.MODEL_ID == "EleutherAI/pythia-410m")
check("pin LAYER_INDEX=20", G.LAYER_INDEX == 20)
check("pin D_MODEL=1024", G.D_MODEL == 1024)
check("pin N_ITEMS=60", G.N_ITEMS == 60)
check("pin MASTER_SEED=20260924", G.MASTER_SEED == 20260924 == R.MASTER_SEED)
check("pin EPS_NORMS=(0.15,0.45)", G.EPS_NORMS == (0.15, 0.45))
check("pin RANK_SET=(1,2,3)", G.RANK_SET == (1, 2, 3))
check("pin POWER_ITER_CAP=12", G.POWER_ITER_CAP == 12)
check("pin STALL_TOL=1e-3", G.STALL_TOL == 1e-3)
check("pin SIGMA_RATIO_ABORT=1.1", G.SIGMA_RATIO_ABORT == 1.1)
check("pin SIGMA_RATIO_RANK_VALID=1.2", G.SIGMA_RATIO_RANK_VALID == 1.2)
check("pin HEADROOM_MIN=15", G.HEADROOM_MIN == 15)
check("pin APPARATUS_NOISE_FLOOR=1e-4", G.APPARATUS_NOISE_FLOOR == 1e-4)
check("pin APPARATUS_MIN_FRAC=0.8", G.APPARATUS_MIN_FRAC == 0.8)
check("pin CHAT_BAR=0.1", G.CHAT_BAR == 0.1)
check("pin EXCEEDANCE_BAR=0.10", G.EXCEEDANCE_BAR == 0.10)
check("pin DELTA_MIN=0.05", G.DELTA_MIN == 0.05)
check("pin MCNEMAR_ALPHA=0.05", G.MCNEMAR_ALPHA == 0.05)
check("pin budget 7260+120=7380",
      G.N_ITEMS_BUDGET == 7260 and G.STAGE2_FWD_EQUIV == 120
      and G.TOTAL_FWD_EQUIV_BUDGET == 7380)
check("pin RECORDS_SHA256",
      G.RECORDS_SHA256 == "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585")

# ---------------------------------------------------------------------------
# 2. Guards (§6)
# ---------------------------------------------------------------------------
check("guard: abort iff s1/s2 < 1.1",
      G.should_abort_item(1.09, 1.0) and not G.should_abort_item(1.1, 1.0)
      and not G.should_abort_item(3.0, 1.0))
def _raises_v3(n_aborted):
    try:
        G.check_abort_frac(n_aborted)
        return False
    except G.InvalidRunError:
        return True


check("guard: INVALID V3 at 31/60 aborted", _raises_v3(31) is True)
check("guard: V3 clears at 30/60 aborted", _raises_v3(30) is False)
check("guard: rank valid iff s1/s3 >= 1.2",
      G.rank_test_valid(1.2, 1.0) and not G.rank_test_valid(1.19, 1.0)
      and not G.rank_test_valid(1.0, 0.0) and not G.rank_test_valid(1.0, None))


def _raises_headroom(n):
    try:
        G.check_headroom(n)
        return False
    except G.InvalidRunError:
        return True


check("guard: INVALID V2 at 14 wrong", _raises_headroom(14) is True)
check("guard: V2 clears at 15 wrong", _raises_headroom(15) is False)


def _raises_apparatus(f):
    try:
        G.check_apparatus(f)
        return False
    except G.InvalidRunError:
        return True


check("guard: INVALID V4 at 0.79 moved", _raises_apparatus(0.79) is True)
check("guard: V4 clears at 0.80 moved", _raises_apparatus(0.80) is False)

# Pass budget ceiling
b = G.PassBudget()
b.charge(7380)
try:
    b.charge(1, "one too many")
    check("budget: refuses pass 7381", False)
except RuntimeError as e:
    check("budget: refuses pass 7381", "7380" in str(e), str(e)[:80])
check("budget: remaining == 0 after full charge", b.remaining() == 0)

# Frozen-backbone guard
import numpy as _np
_sd = {"a": _np.ones(8), "b": _np.zeros(4)}
guard = G.FrozenBackboneGuard()
h0 = guard.snapshot_before(_sd)
check("guard: identical dict re-hashes equal",
      guard.verify_after(dict(_sd)) == h0)
_tampered = {"a": _np.ones(8) * 2.0, "b": _np.zeros(4)}
try:
    guard.verify_after(_tampered)
    check("guard: tamper -> INVALID V1", False)
except G.InvalidRunError as e:
    check("guard: tamper -> INVALID V1", "V1" in str(e), str(e)[:80])
check("guard: sha256_state_dict is key-order invariant",
      G.sha256_state_dict({"b": _np.zeros(4), "a": _np.ones(8)}) == h0)
try:
    G.FrozenBackboneGuard().verify_after(_sd)
    check("guard: verify-before-snapshot raises", False)
except G.CrashGuardError:
    check("guard: verify-before-snapshot raises", True)

# crash-guard: smoke mode passes on this bundle; stage-b verifies the archive
try:
    G.crash_guard("smoke")
    check("crash-guard: smoke mode passes", True)
except G.CrashGuardError as e:
    check("crash-guard: smoke mode passes", False, str(e)[:100])
try:
    G.crash_guard("stage-b")
    check("crash-guard: stage-b archive pin verified", True)
except G.CrashGuardError as e:
    check("crash-guard: stage-b archive pin verified", False, str(e)[:100])
import tempfile as _tf
with _tf.TemporaryDirectory() as _td:
    # archive missing under a foreign bundle dir -> loud refusal
    try:
        G.crash_guard("stage-b", bundle_dir=_td)
        check("crash-guard: missing archive refuses", False)
    except G.CrashGuardError:
        check("crash-guard: missing archive refuses", True)
    # corrupt archive (wrong bytes) -> sha mismatch refusal
    _arch = os.path.join(_td, "..", "EXP077_cone_vs_line",
                         "exp077_instance_records.json")
    os.makedirs(os.path.dirname(os.path.abspath(_arch)), exist_ok=True)
    with open(os.path.abspath(_arch), "w") as f:
        f.write('[{"corrupt": true}]')
    try:
        G.crash_guard("stage-b", bundle_dir=_td)
        check("crash-guard: corrupt archive refuses", False)
    except G.CrashGuardError as e:
        check("crash-guard: corrupt archive refuses",
              "mismatch" in str(e), str(e)[:80])


# ---------------------------------------------------------------------------
# 3. Henrici index vs closed-form 2x2 reference (pure python, no numpy)
# ---------------------------------------------------------------------------

def _he_2x2_closed(a, b, c, d):
    """He for [[a,b],[c,d]] via the quadratic formula (independent reference).

    eig = (tr ± sqrt(tr² − 4 det)) / 2, possibly complex; |λ|² = λ·conj(λ).
    """
    tr = a + d
    det = a * d - b * c
    disc = tr * tr - 4 * det
    if disc >= 0:
        l1 = (tr + math.sqrt(disc)) / 2
        l2 = (tr - math.sqrt(disc)) / 2
        lam2 = l1 * l1 + l2 * l2
    else:
        re = tr / 2
        im = math.sqrt(-disc) / 2
        lam2 = 2 * (re * re + im * im)
    frob2 = a * a + b * b + c * c + d * d
    return math.sqrt(max(0.0, frob2 - lam2)) / math.sqrt(frob2)


import numpy as _np2

_HE_FIXTURES = [
    (1.0, 0.0, 0.0, 1.0),     # identity: normal -> He = 0
    (0.0, 1.0, 0.0, 0.0),     # Jordan block: maximally non-normal -> He = 1
    (0.0, -2.0, 2.0, 0.0),    # skew-symmetric: normal -> He = 0
    (3.0, 1.0, 0.5, -1.0),    # generic real spectrum
    (1.0, 5.0, -0.2, 2.0),    # generic complex spectrum
    (0.7, -1.3, 2.1, -0.4),
]
_he_ok = True
for (_a, _b, _c, _d) in _HE_FIXTURES:
    _W = _np2.array([[_a, _b], [_c, _d]])
    _got, _info = H.henrici_index(_W, name="fixture-2x2")
    _want = _he_2x2_closed(_a, _b, _c, _d)
    if abs(_got - _want) > 1e-9:
        _he_ok = False
        print(f"   2x2 mismatch: got {_got}, want {_want}")
check("henrici: 6 fixtures match closed-form 2x2 reference", _he_ok)
check("henrici: identity He == 0",
      H.henrici_index(_np2.eye(3), name="eye")[0] < 1e-12)
_j = _np2.array([[0.0, 1.0], [0.0, 0.0]])
check("henrici: Jordan block He == 1",
      abs(H.henrici_index(_j, name="jordan")[0] - 1.0) < 1e-12)
try:
    H.henrici_index(_np2.zeros((4, 12)), name="rect")
    check("henrici: rectangular raises BlockSelectionError", False)
except G.BlockSelectionError:
    check("henrici: rectangular raises BlockSelectionError", True)
try:
    H.henrici_index(_np2.zeros((3, 3)), name="zero")
    check("henrici: zero matrix raises", False)
except G.BundleError:
    check("henrici: zero matrix raises", True)
# registry: 48 blocks, O direct + V fused-interleaved, unique keys, d=1024
check("registry: 48 blocks", len(H.BLOCKS) == 48)
check("registry: 24 O (direct) + 24 V (fused-interleaved)",
      sum(1 for s in H.BLOCKS if s["kind"] == "direct") == 24
      and sum(1 for s in H.BLOCKS if s["kind"] == "fused-interleaved") == 24)
check("registry: V rows are the per-head interleaved set {r:(r mod 192)>=128}",
      all(tuple(s["row_idx"]) == H.V_ROWS for s in H.BLOCKS
          if s["kind"] == "fused-interleaved"))
check("registry: V_ROWS has 1024 rows, none in contiguous [2048:3072] order",
      len(H.V_ROWS) == 1024
      and H.V_ROWS != tuple(range(2048, 3072))
      and set(H.V_ROWS) == {r for r in range(3072) if (r % 192) >= 128})
check("registry: keys unique, d=1024",
      len({s["key"] for s in H.BLOCKS}) == 48
      and all(s["d"] == 1024 for s in H.BLOCKS))
# extract_block: V interleaved-row selection + loud provenance (custom spec
# sized to double). Test double: (12,4) fused with interleave period 6 —
# V rows are {r : (r mod 6) >= 4} = {4, 5, 10, 11}.
_spec = {"name": "test.V", "key": "qkv", "kind": "fused-interleaved",
         "row_idx": (4, 5, 10, 11),
         "slice_note": "interleaved in test double", "d": 4}
_sd3 = {"qkv": _np2.arange(48).reshape(12, 4).astype(float)}
_nm, _Wv, _note = H.extract_block(_sd3, _spec)
check("extract_block: V is 4x4 from interleaved rows {4,5,10,11}",
      _Wv.shape == (4, 4) and _Wv[0, 0] == 16.0 and _Wv[3, 3] == 47.0,
      f"shape={_Wv.shape}")
check("extract_block: provenance names interleaved rows + fused key",
      "interleaved" in _note and "qkv" in _note, _note[:80])
# retired kind is dead: raises loudly, never silently slices
_legacy = {"name": "test.V.legacy", "key": "qkv", "kind": "fused-slice",
           "slice_rows": (8, 12), "slice_note": "retired", "d": 4}
try:
    H.extract_block(_sd3, _legacy)
    check("extract_block: retired 'fused-slice' kind raises", False)
except G.BundleError:
    check("extract_block: retired 'fused-slice' kind raises", True)
try:
    H.extract_block({}, _spec)
    check("extract_block: missing key raises", False)
except G.BundleError:
    check("extract_block: missing key raises", True)

# ---------------------------------------------------------------------------
# 4. RNG contract (§4, §13)
# ---------------------------------------------------------------------------
_sched = R.seed_schedule()
check("rng: 120 seeds pairwise distinct", len(set(_sched)) == 120)
check("rng: item_norm_seed pins",
      R.item_norm_seed(0, 0) == 20260924 and R.item_norm_seed(0, 1) == 20260925
      and R.item_norm_seed(1, 0) == 20261924)
try:
    R.item_norm_seed(60, 0)
    check("rng: item index range enforced", False)
except ValueError:
    check("rng: item index range enforced", True)
try:
    R.item_norm_seed(0, 2)
    check("rng: norm index range enforced", False)
except ValueError:
    check("rng: norm index range enforced", True)
try:
    R.generate_v_rand(0, 0)
    check("rng: generate_v_rand raises without torch", False)
except RuntimeError as e:
    check("rng: generate_v_rand raises without torch",
          "torch" in str(e), str(e)[:70])
try:
    R.derangement(60)
    check("rng: derangement raises without torch", False)
except RuntimeError:
    check("rng: derangement raises without torch", True)
_rng_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "exp086_rng.py")).read()
check("rng: numpy never imported for random directions",
      "import numpy" not in _rng_src and "np." not in _rng_src)

# ---------------------------------------------------------------------------
# 5. Exact one-sided McNemar (§7)
# ---------------------------------------------------------------------------
check("mcnemar: (10,0) -> 2^-10",
      abs(S.mcnemar_exact_one_sided(10, 0) - 2.0 ** -10) < 1e-15)


def _mcnemar_recurrence(n10, n01):
    """Independent cross-check: iterative binomial recurrence (no math.comb)."""
    n = n10 + n01
    # P(X = n10) via recurrence from P(X=0) = 2^-n
    p_k = 2.0 ** -n
    for k in range(1, n10 + 1):
        p_k = p_k * (n - k + 1) / k
    tail = p_k
    for k in range(n10 + 1, n + 1):
        p_k = p_k * (n - k + 1) / k
        tail += p_k
    return min(1.0, tail)


_mcn_ok = True
for (_a, _b) in [(16, 2), (3, 4), (5, 3), (0, 7), (12, 12), (1, 1)]:
    if abs(S.mcnemar_exact_one_sided(_a, _b)
           - _mcnemar_recurrence(_a, _b)) > 1e-12:
        _mcn_ok = False
check("mcnemar: 6 fixtures match recurrence cross-check", _mcn_ok)
check("mcnemar: symmetric data p > 0.5 for (12,12)",
      S.mcnemar_exact_one_sided(12, 12) > 0.5)
try:
    S.mcnemar_exact_one_sided(0, 0)
    check("mcnemar: (0,0) raises NonTestableDataError", False)
except G.NonTestableDataError:
    check("mcnemar: (0,0) raises NonTestableDataError", True)

# ---------------------------------------------------------------------------
# 6. Tango 95% CI (§7) — derivation cross-check + inversion self-consistency
# ---------------------------------------------------------------------------

def _mle_grid(n10, n01, nc, u, step=2e-4):
    """Independent reference: dense-grid argmax of the constrained loglik."""
    best_t, best_l = None, -1e300
    t = 1e-6
    while t < 1.0 - 1e-6:
        p10, p01, pc = t + u, t, 1 - 2 * t - u
        if p10 > 0 and p01 > 0 and pc > 0:
            l = (n10 * math.log(p10) + n01 * math.log(p01)
                 + nc * math.log(pc))
            if l > best_l:
                best_l, best_t = l, t
        t += step
    return best_t, best_t + u


_mle_ok = True
for (_u, _tab) in [(0.0, (16, 2, 42)), (0.2, (16, 2, 42)),
                   (-0.1, (3, 4, 53)), (0.05, (5, 3, 52))]:
    _n10, _n01, _nc = _tab
    _p10q, _p01q = S._constrained_mle(_u, _n10, _n01, _nc)
    _t, _p10g = _mle_grid(_n10, _n01, _nc, _u)
    _p01g = _t
    if abs(_p10q - _p10g) > 5e-4 or abs(_p01q - _p01g) > 5e-4:
        _mle_ok = False
        print(f"   mle mismatch at u={_u}: quad={(_p10q,_p01q)} grid={(_p10g,_p01g)}")
check("tango: constrained MLE matches dense-grid argmax (4 cases)", _mle_ok)


def _tango_selfcheck(n10, n01, n00, n11):
    lo, hi = S.tango_ci(n10, n01, n00, n11)
    n = n10 + n01 + n00 + n11
    ph = n10 / n - n01 / n
    tlo = S._tango_score(lo, n10, n01, n00, n11)
    thi = S._tango_score(hi, n10, n01, n00, n11)
    return (lo, hi, ph, abs(tlo - S.Z95) < 1e-6 and abs(thi + S.Z95) < 1e-6
            and lo < ph < hi)


_tci_ok = True
for _tab in [(16, 2, 10, 32), (3, 4, 25, 28), (5, 3, 22, 30),
             (12, 3, 9, 36), (0, 5, 30, 25), (20, 1, 15, 24)]:
    _lo, _hi, _ph, _ok = _tango_selfcheck(*_tab)
    if not _ok:
        _tci_ok = False
        print(f"   tango selfcheck failed on {_tab}: lo={_lo} hi={_hi}")
check("tango: inversion self-consistent on 6 tables (|T|=z, contains ph)",
      _tci_ok)
# score monotonicity on a grid (decreasing in delta0)
_mono_ok = True
for _tab in [(16, 2, 10, 32), (3, 4, 25, 28)]:
    _ts = [S._tango_score(-0.9 + 0.1 * k, *_tab) for k in range(19)]
    if any(_ts[k] < _ts[k + 1] - 1e-9 for k in range(18)):
        _mono_ok = False
check("tango: score statistic monotone decreasing", _mono_ok)
_lo, _hi, _, _ = _tango_selfcheck(16, 2, 10, 32)
check("tango: CONTINUE-scenario primary LCI > 0.05", _lo > 0.05,
      f"LCI={_lo:.4f}")
_lo6, _hi6, _, _ = _tango_selfcheck(2, 8, 25, 25)
check("tango: KILL-scenario primary UCI < 0.05", _hi6 < 0.05,
      f"UCI={_hi6:.4f}")
_lo9, _hi9, _, _ = _tango_selfcheck(6, 5, 7, 42)
check("tango: HELD-V9 rank CI crosses 0", _lo9 <= 0 <= _hi9,
      f"({_lo9:.4f},{_hi9:.4f})")
try:
    S.tango_ci(0, 0, 30, 30)
    check("tango: zero discordant raises NonTestableDataError", False)
except G.NonTestableDataError:
    check("tango: zero discordant raises NonTestableDataError", True)

# ---------------------------------------------------------------------------
# 7. ĉ / exceedance (§2 D6) and signed ledger (§7 P3)
# ---------------------------------------------------------------------------
check("c_hat: mean of |.|",
      abs(S.c_hat([0.5, -0.3, 0.1]) - 0.3) < 1e-12)
check("exceedance: fraction above 0.1",
      abs(S.exceedance([0.5, 0.09, 0.11, -0.2]) - 0.75) < 1e-12)
try:
    S.c_hat([])
    check("c_hat: empty raises", False)
except G.NonTestableDataError:
    check("c_hat: empty raises", True)
_led = S.signed_ledger([0, 0, 1, 1, 0, 1], [1, 0, 1, 0, 1, 1])
check("ledger: b=2 (wrong->right), c=1 (right->wrong)",
      _led["b_wrong_to_right"] == 2 and _led["c_right_to_wrong"] == 1,
      f"{_led}")
check("ledger: anti-steerable frac = 1/3 > 0.2 -> flagged (reporting)",
      abs(_led["anti_steerable_frac"] - 1 / 3) < 1e-12
      and _led["flagged"] is True)
_led2 = S.signed_ledger([0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0])  # b=4, c=1
check("ledger: frac = 0.2 exactly -> not flagged",
      abs(_led2["anti_steerable_frac"] - 0.2) < 1e-12
      and _led2["flagged"] is False)
_led3 = S.signed_ledger([1, 1], [1, 1])
check("ledger: no changes -> frac None, not flagged",
      _led3["anti_steerable_frac"] is None and _led3["flagged"] is False)
try:
    S.signed_ledger([1, 0], [1])
    check("ledger: length mismatch raises", False)
except ValueError:
    check("ledger: length mismatch raises", True)

# ---------------------------------------------------------------------------
# 8. Verdict table §9 (exact order) — every row + precedence
# ---------------------------------------------------------------------------

def _base_results(**kw):
    """Benign base: would CONTINUE (all conjuncts) unless overridden."""
    r = {
        "delta_theta_ok": True,
        "n_wrong_baseline": 20,
        "frac_aborted": 0.0,
        "apparatus_ok": True,
        "c_hat": 0.40,
        "exceedance": 0.50,
        "delta_lci": 0.10, "delta_uci": 0.30, "delta_point": 0.20,
        "mcnemar_p": 0.001,
        "rank_valid": True,
        "delta_rank_lci": 0.05, "delta_rank_uci": 0.25,
        "delta_rank_point": 0.15,
        "stage2_ran": True,
        "delta_perm_lci": 0.04,
    }
    r.update(kw)
    return r


_v, _e, _d = V.adjudicate(_base_results())
check("verdict V7: full conjuncts -> CONTINUE",
      _v == "CONTINUE" and _e == "Supported", f"{_v}/{_e}: {_d[:60]}")

# INVALID rows preempt everything
_v, _e, _d = V.adjudicate(_base_results(delta_theta_ok=False))
check("verdict V1: Δθ≠0 -> INVALID", _v == "INVALID" and "V1" in _d)
_v, _e, _d = V.adjudicate(_base_results(n_wrong_baseline=14))
check("verdict V2: <15 wrong -> INVALID", _v == "INVALID" and "V2" in _d)
_v, _e, _d = V.adjudicate(_base_results(frac_aborted=0.51))
check("verdict V3: >50% abort -> INVALID", _v == "INVALID" and "V3" in _d)
_v, _e, _d = V.adjudicate(_base_results(apparatus_ok=False))
check("verdict V4: apparatus fail -> INVALID", _v == "INVALID" and "V4" in _d)
check("verdict: INVALID evidentiary is Underdetermined",
      V.adjudicate(_base_results(apparatus_ok=False))[1] == "Underdetermined")

# V5 kill-first (ĉ) preempts a primary win -> KILL (precedence test)
_v, _e, _d = V.adjudicate(_base_results(c_hat=0.02, exceedance=0.01))
check("verdict V5: ĉ<0.1 & E<10% -> KILL (preempts V7)",
      _v == "KILL" and _e == "Refuted" and "V5" in _d, f"{_v}: {_d[:60]}")
# V5 boundary: E == 10% exactly does NOT kill (primary win -> V7 CONTINUE)
_v, _e, _d = V.adjudicate(_base_results(c_hat=0.02, exceedance=0.10))
check("verdict: c_hat<0.1 & E=10% -> V5 does not fire (V7 CONTINUE)",
      _v == "CONTINUE" and "V5" not in _d, f"{_v}: {_d[:60]}")
# V6: primary gain excluded -> KILL (even with rank undefined — precedence)
_v, _e, _d = V.adjudicate(_base_results(
    delta_lci=-0.10, delta_uci=0.04, delta_point=-0.02, mcnemar_p=0.9,
    rank_valid=False))
check("verdict V6: CI(Δ) entirely below +0.05 -> KILL (preempts V11)",
      _v == "KILL" and "V6" in _d, f"{_v}: {_d[:60]}")
# V6 boundary: UCI == 0.05 exactly is not "entirely below"
_v, _e, _d = V.adjudicate(_base_results(
    delta_lci=-0.10, delta_uci=0.05, delta_point=0.0, mcnemar_p=0.9,
    c_hat=0.4, exceedance=0.5))
check("verdict: UCI==0.05 -> not V6 (falls to V12/HELD)",
      _v == "HELD" and "V12" in _d, f"{_v}: {_d[:60]}")

# V7b: primary win + rank win + permuted fail -> HELD (not CONTINUE)
_v, _e, _d = V.adjudicate(_base_results(delta_perm_lci=-0.02))
check("verdict V7b: permuted fail -> HELD",
      _v == "HELD" and _e == "Inconclusive" and "V7b" in _d, f"{_v}: {_d[:60]}")

# V8: primary win + rank excluded (CI below +0.05, point ≤ 0) -> PIVOT
_v, _e, _d = V.adjudicate(_base_results(
    delta_rank_lci=-0.10, delta_rank_uci=0.03, delta_rank_point=-0.02,
    stage2_ran=True, delta_perm_lci=0.04))
check("verdict V8: rank gradient excluded -> PIVOT",
      _v == "PIVOT" and _e == "Not supported" and "V8" in _d, f"{_v}: {_d[:60]}")
# V8 boundary: point > 0 with CI below +0.05 is NOT V8 (straddle -> V9)
_v, _e, _d = V.adjudicate(_base_results(
    delta_rank_lci=-0.02, delta_rank_uci=0.04, delta_rank_point=0.01))
check("verdict: rank CI crosses 0, point>0 -> V9 not V8",
      _v == "HELD" and "V9" in _d, f"{_v}: {_d[:60]}")

# V9: primary win + rank straddles -> HELD
_v, _e, _d = V.adjudicate(_base_results(
    delta_rank_lci=-0.05, delta_rank_uci=0.15, delta_rank_point=0.05))
check("verdict V9: rank straddles -> HELD",
      _v == "HELD" and "V9" in _d, f"{_v}: {_d[:60]}")

# V10: ĉ<0.1 with E≥10% (no primary win) -> HELD
_v, _e, _d = V.adjudicate(_base_results(
    c_hat=0.07, exceedance=0.20, delta_lci=-0.05, delta_uci=0.10,
    delta_point=0.02, mcnemar_p=0.4))
check("verdict V10: ĉ<0.1, E≥10% -> HELD",
      _v == "HELD" and "V10" in _d, f"{_v}: {_d[:60]}")

# V11: rank undefined (no primary-gain exclusion) -> HELD, never KILL
_v, _e, _d = V.adjudicate(_base_results(rank_valid=False))
check("verdict V11: rank undefined -> HELD (fail-safe)",
      _v == "HELD" and "V11" in _d, f"{_v}: {_d[:60]}")

# V12: primary straddles +0.05 -> HELD
_v, _e, _d = V.adjudicate(_base_results(
    delta_lci=-0.02, delta_uci=0.12, delta_point=0.05, mcnemar_p=0.3))
check("verdict V12: primary straddles -> HELD",
      _v == "HELD" and "V12" in _d, f"{_v}: {_d[:60]}")

# Fall-through: primary win on LCI but McNemar p > 0.05, rank CI in (0, 0.05)
_v, _e, _d = V.adjudicate(_base_results(
    delta_lci=0.06, delta_uci=0.20, delta_point=0.13, mcnemar_p=0.10,
    delta_rank_lci=0.01, delta_rank_uci=0.04, delta_rank_point=0.025))
check("verdict: unlisted combination -> HELD/UNCLASSIFIED (never silent)",
      _v == "HELD" and "UNCLASSIFIED" in _d, f"{_v}: {_d[:60]}")

# Stage-2 process gate: primary win + rank win but stage-2 not run -> loud halt
try:
    V.adjudicate(_base_results(stage2_ran=False, delta_perm_lci=None))
    check("verdict: missing stage-2 on primary win -> loud halt", False)
except G.InvalidRunError:
    check("verdict: missing stage-2 on primary win -> loud halt", True)

# Missing keys -> loud KeyError
try:
    V.adjudicate({"delta_theta_ok": True})
    check("verdict: missing keys raise KeyError", False)
except KeyError:
    check("verdict: missing keys raise KeyError", True)

# _paired_table: pairwise deletion on aborted items
_items = [
    {"aborted": False,
     "arms": {("v1", 0): {"correct": True}, ("vrand", 0): {"correct": False}}},
    {"aborted": False,
     "arms": {("v1", 0): {"correct": False}, ("vrand", 0): {"correct": True}}},
    {"aborted": True, "arms": {("vrand", 0): {"correct": True}}},
]
_tab, _n = RUN._paired_table(_items, "v1", "vrand", 0)
check("paired table: (1,1,0,0) with aborted item deleted",
      _tab == (1, 1, 0, 0) and _n == 2, f"{_tab} n={_n}")

# ---------------------------------------------------------------------------
# 9. Runner refusals (no clearance -> exit 2, before any weight access)
# ---------------------------------------------------------------------------

def _exit_code(argv):
    try:
        rc = RUN.main(argv)
        return 0 if rc is None else rc
    except SystemExit as e:
        return e.code


check("runner: --run without clearance -> exit 2",
      _exit_code(["--run"]) == 2)
check("runner: --run with only one clearance -> exit 2",
      _exit_code(["--run", "--ceo-gpu-clearance"]) == 2)
check("runner: --stage-a without bundle-review-signoff -> exit 2",
      _exit_code(["--stage-a"]) == 2)
check("runner: no args -> exit 2", _exit_code([]) == 2)
# TorchBackend raises loudly without torch (never silently degrades)
try:
    RUN.TorchBackend("/nonexistent/weights")
    check("runner: TorchBackend raises without torch", False)
except RuntimeError as e:
    check("runner: TorchBackend raises without torch", "torch" in str(e))

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print(f"\n{PASS} passed, {FAIL} failed out of {PASS + FAIL} evaluator tests")
sys.exit(0 if FAIL == 0 else 1)
