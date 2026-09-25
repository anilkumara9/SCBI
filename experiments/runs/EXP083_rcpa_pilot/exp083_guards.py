"""EXP083 (R1 RCPA kill pilot) — guard predicates and budget enforcement.

Pure standard library. CPU. Deterministic. Implements EXP083 §2 (SHA guard),
§3.2 (identity arm), §5 (G-norm / G-static / G-curve), and §6 (pass budget).

Guard inventory (protocol numbering):
  SHA-prerun  §2/R3: pre-run SHA-256 == pinned expected hash, else INVALID(i)
  IDENTITY    §3.2: identity arm == archived C1 bit-for-bit, else INVALID(ii)
  G-norm      §5/F6: 5th-percentile floor (linear interpolation, type 7),
              strictly-below exclusion, pre-flip-test; computation fault ->
              INVALID(iii)
  G-static    §5/F5: mean pairwise cos(r_i, r_j) > 0.5 -> RE-SKIN KILL
              (fires only on a validated apparatus — precedence in the
              adjudicator); computation fault -> INVALID(iii)
  G-curve     §5/F9: report-only mean<r_i, h_a,i> (rescaling fraction)
  BUDGET      §6/F3: 180 + <=12 smoke + $0 identity = <=192; the runner
              REFUSES pass 193 (hard stop). The inventory is ENCODED in
              PassCounter, not just documented.
"""

import math

# ----------------------------------------------------------------------------
# Pre-registered constants (EXP083 §2/§4/§5/§6)
# ----------------------------------------------------------------------------
EXPECTED_SHA256 = ("4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd")
N_ITEMS = 60
MASTER_SEED = 20260924          # S0 (§4 A_g)
ALPHA = 1.0                     # pinned injection norm (§2, F2)
D_MODEL = 1024                  # Pythia-410m residual width
DELTA_MIN = 0.05                # the packet's claimed effect (Q4)
STATIC_COS_BAR = 0.5            # G-static RE-SKIN bar (§5, F5)
RESCALE_FRAC = 0.5              # G-curve powered-stage trigger (§5, F9)

# Pass inventory (§6): the hard stop is encoded, not documented.
SMOKE_MAX = 12                  # startup smoke: 3 items x {clean, A_r, A_g} = 9 (+3 spare)
CLEAN_READ = 60                 # r computation (+ G-norm/G-static/G-curve on CPU)
ARM_R = 60                      # A_r injection arm (skipped if G-static fires)
ARM_G = 60                      # A_g random-direction arm (skipped if G-static fires)
ARM_0 = 0                       # A_0 identity: $0 by reuse of clean-read decisions (R4)
MAX_PASSES = SMOKE_MAX + CLEAN_READ + ARM_R + ARM_G + ARM_0   # 192
HARD_STOP = MAX_PASSES + 1      # 193 — the runner REFUSES this pass (§A.4 guard)


class PassBudgetExceeded(Exception):
    """Raised when a pass allocation would reach or exceed the hard stop."""


class PassCounter:
    """Enforces the §6 pass inventory at runtime.

    `use(n, label)` allocates n passes; raises PassBudgetExceeded if the
    allocation would take the total past MAX_PASSES (i.e. refuses pass 193).
    `inventory()` returns the licensed block table for the run manifest.
    """

    def __init__(self):
        self.total = 0
        self.blocks = []

    def use(self, n, label):
        if n < 0:
            raise ValueError("cannot allocate negative passes")
        if self.total + n > MAX_PASSES:
            raise PassBudgetExceeded(
                "REFUSED: allocating %d passes for '%s' would take the run to "
                "%d > %d (MAX_PASSES); pass %d is the hard stop — no "
                "unlicensed passes (§6, F3-TIER-EXCEPTION binds at 192)."
                % (n, label, self.total + n, MAX_PASSES, HARD_STOP))
        self.total += n
        self.blocks.append({"label": label, "passes": n,
                            "running_total": self.total})
        return self.total

    def inventory(self):
        return {"blocks": list(self.blocks), "total": self.total,
                "max_passes": MAX_PASSES, "hard_stop": HARD_STOP,
                "licensed": {"smoke_max": SMOKE_MAX, "clean_read": CLEAN_READ,
                             "arm_r": ARM_R, "arm_g": ARM_G, "arm_0": ARM_0}}


# ----------------------------------------------------------------------------
# SHA-256 guard (§2, R3)
# ----------------------------------------------------------------------------

def sha_prerun_check(actual_hash, expected=EXPECTED_SHA256):
    """Pre-run SHA-256 vs the pinned expected hash.

    Returns (ok, cause). Mismatch -> INVALID(i): the binding pre/post match
    alone would let a wrong-model download slip through (R3).
    """
    if actual_hash == expected and actual_hash:
        return True, "pre-run SHA-256 matches the pinned expected hash"
    return False, ("INVALID(i): pre-run SHA-256 != expected pinned hash "
                   "4c242d...dd — wrong model downloaded (R3)")


def sha_pre_post_check(pre_hash, post_hash):
    """Binding guard: SHA-256 over state_dict() pre-run == post-run.

    Mismatch -> frozen-backbone violation (AGENTS.md Law #6); results are
    NOT reported. (Precedence: evaluated inside the run; the pre-run
    expected-hash check is INVALID(i) at startup.)
    """
    match = (pre_hash == post_hash) and bool(pre_hash)
    return match, ("Delta theta = 0 holds (pre==post)" if match
                   else "FATAL: pre/post parameter hash mismatch — "
                        "frozen-backbone violation (Law #6)")


# ----------------------------------------------------------------------------
# Identity arm (§3.2) — $0 by reuse of the clean-read decisions (R4)
# ----------------------------------------------------------------------------

def identity_check(identity_decisions, archived_c1):
    """Bit-for-bit: identity arm == archived C1 decisions.

    Returns (ok, cause). Mismatch -> INVALID(ii): apparatus failure —
    no verdict about R1 is licensed.
    """
    if len(identity_decisions) != len(archived_c1):
        return False, ("INVALID(ii): identity/arm archive length mismatch "
                       "(%d vs %d)" % (len(identity_decisions), len(archived_c1)))
    mism = [i for i, (a, b) in enumerate(zip(identity_decisions, archived_c1))
            if bool(a) != bool(b)]
    if mism:
        return False, ("INVALID(ii): identity arm != archived C1 bit-for-bit — "
                       "%d mismatches (first: %s)" % (len(mism), mism[:5]))
    return True, "identity arm reproduces archived C1 bit-for-bit ($0 apparatus check)"


# ----------------------------------------------------------------------------
# G-norm (§5, F6 / R2): 5th-percentile floor, linear interpolation (type 7)
# ----------------------------------------------------------------------------

def percentile_type7(sorted_vals, p):
    """Linear-interpolation percentile (numpy.percentile default, type 7).

    position = (n - 1) * p between sorted values; pinned by R2.
    Nearest-rank interpolation is REJECTED by name (would give N_final=58).
    """
    n = len(sorted_vals)
    if n == 0:
        raise ValueError("empty values")
    if n == 1:
        return float(sorted_vals[0])
    pos = (n - 1) * p
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return float(sorted_vals[lo])
    frac = pos - lo
    return float(sorted_vals[lo] + frac * (sorted_vals[hi] - sorted_vals[lo]))


def g_norm_floor(r_norms, p=0.05):
    """G-norm floor + strictly-below exclusion (§5, F6, R2).

    Returns (floor, excluded_indices, n_final). Exclusion is STRICTLY below
    the floor (<, not <=). N_final is deterministic: exactly 3 items fall
    strictly below the interpolated floor -> N_final = 57 (verified
    arithmetically 2026-09-24). Tie edge case: if sorted ||r|| values tie
    at the interpolation point, N_final = 58 — the KILL_flat functional
    bar applies at the observed N_final either way.
    """
    if len(r_norms) != N_ITEMS:
        raise ValueError("G-norm expects %d norms, got %d" % (N_ITEMS, len(r_norms)))
    for i, v in enumerate(r_norms):
        if not (v >= 0.0) or math.isnan(v) or math.isinf(v):
            raise ValueError("G-norm computation fault: non-finite norm at item %d" % i)
    srt = sorted(r_norms)
    floor = percentile_type7(srt, p)
    excluded = [i for i, v in enumerate(r_norms) if v < floor]
    return floor, excluded, N_ITEMS - len(excluded)


# ----------------------------------------------------------------------------
# G-static (§5, F5): static-ness check — mean pairwise cosine
# ----------------------------------------------------------------------------

def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _norm(v):
    return math.sqrt(_dot(v, v))


def g_static_check(r_hat_list):
    """G-static: mean pairwise cos(r_i, r_j) over included items.

    Bar: > 0.5 -> RE-SKIN KILL (fires only on a validated apparatus —
    precedence is enforced by the adjudicator). Chance anchor: for random
    unit vectors in d=1024, pairwise cos ~ N(0, 1/1024), so |cos| ~= 0.1 is
    already far above chance; 0.5 means a dominant common component.

    Returns (fired, mean_cos). Computation fault (non-unit input,
    wrong dim) raises ValueError -> INVALID(iii) at the call site.
    """
    n = len(r_hat_list)
    if n < 2:
        raise ValueError("G-static computation fault: need >= 2 included items")
    for i, v in enumerate(r_hat_list):
        if len(v) != D_MODEL:
            raise ValueError("G-static computation fault: dim %d != %d at item %d"
                             % (len(v), D_MODEL, i))
        nv = _norm(v)
        if abs(nv - 1.0) > 1e-6:
            raise ValueError("G-static computation fault: r_hat not unit-norm "
                             "at item %d (||.||=%.6f)" % (i, nv))
    total, pairs = 0.0, 0
    for i in range(n):
        for j in range(i + 1, n):
            total += _dot(r_hat_list[i], r_hat_list[j])
            pairs += 1
    mean_cos = total / pairs
    return mean_cos > STATIC_COS_BAR, mean_cos


# ----------------------------------------------------------------------------
# G-curve (§5, F9): report-only rescaling fraction
# ----------------------------------------------------------------------------

def g_curve_rescale(r_hat_list, h_a_list):
    """$0 diagnostic: mean<r_i, h_a,i> over included items (rescaling fraction).

    Interpretation rule (pre-registered): if the verdict is CONTINUE and the
    rescaling fraction > 0.5, the powered pilot must include the
    scalar-rescale arm. Report-only in the kill pilot — never verdict-bearing.
    """
    if len(r_hat_list) != len(h_a_list):
        raise ValueError("G-curve: list length mismatch")
    fracs = []
    for r, h in zip(r_hat_list, h_a_list):
        nh = _norm(h)
        if nh == 0.0:
            raise ValueError("G-curve computation fault: zero h_a norm")
        fracs.append(_dot(r, h) / nh)
    return sum(fracs) / len(fracs)
