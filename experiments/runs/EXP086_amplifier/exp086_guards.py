#!/usr/bin/env python3
"""EXP086 guards: signed pins, startup crash-guard, frozen-backbone guard,
Stage-B preflight guards (headroom, convergence, apparatus), pass budget.

Implements the signed protocol
experiments/protocols/EXP086_R3_AMPLIFIER_PREREG_SIGNED.md (LOG-311).

All thresholds below are pre-registered pins copied verbatim from the
protocol (§1, §4, §5, §6, §9, §11, §14 G1-G4). Changing any pin is a design
change -> new experiment number (Law #4). It is NOT an edit.

Stage A (weight-only, $0 CPU, advisory) and Stage B (GPU pilot) guards live
here side by side; the runner selects by CLI mode. The crash-guard runs
BEFORE any weight access in every mode (fail fast and loud).
"""

import hashlib
import json
import os
import sys

# ---------------------------------------------------------------------------
# Signed pins (protocol §1, §4, §6, §11)
# ---------------------------------------------------------------------------

MODEL_ID = "EleutherAI/pythia-410m"
LAYER_INDEX = 20            # 0-indexed residual stream (program-standard site)
D_MODEL = 1024              # Pythia-410m hidden size (D1)
N_ITEMS = 60                # fixed probe-set size (§6.1)
MASTER_SEED = 20260924      # v_rand draws + Stage-2 derangement (§4, §13)

# Norms: eps in {0.15, 0.45} x ||h_l(x_i)||_2, per item. [ARBITRARY] (§4 F11)
EPS_NORMS = (0.15, 0.45)
PRIMARY_NORM = 0.15         # primary regime (T1 linearization most defensible)

# Deflated power iteration: ranks {1,2,3}, 12-iteration cap per vector (§4)
RANK_SET = (1, 2, 3)
POWER_ITER_CAP = 12
STALL_TOL = 1e-3            # Rayleigh-quotient relative-change stall tol (§4)

# Convergence guards (§6.4): abort item's direction arms if sigma1/sigma2 < 1.1;
# >50% of items aborted -> INVALID (UNDEFINED-LANDSCAPE)
SIGMA_RATIO_ABORT = 1.1
MAX_ABORT_FRAC = 0.5

# Rank-test validity (§6.4): require sigma1/sigma3 >= 1.2 else UNDEFINED -> HELD
SIGMA_RATIO_RANK_VALID = 1.2

# Headroom gate (§6.2): >= 15 wrong-at-baseline among the 60, else INVALID
HEADROOM_MIN = 15

# Apparatus check (§6.5): random delta at 0.45||h|| must move ||Dz||_2 above
# the 1e-4 noise floor on >= 80% of items, else INVALID (proxy-unresponsive)
APPARATUS_NOISE_FLOOR = 1e-4
APPARATUS_MIN_FRAC = 0.8

# ĉ kill-first diagnostic (§7 V5 / §9): ĉ < 0.1 AND exceedance < 10% -> KILL
CHAT_BAR = 0.1
EXCEEDANCE_BAR = 0.10

# Primary binding bar (§7, §9 V6/V7/V12): difference form, delta_min = 0.05
DELTA_MIN = 0.05
MCNEMAR_ALPHA = 0.05

# Budget (§11): 121 fwd-equiv/item x 60 = 7260; Stage-2 permuted = 120
FWD_EQUIV_PER_ITEM = 121
N_ITEMS_BUDGET = N_ITEMS * FWD_EQUIV_PER_ITEM          # 7260
STAGE2_FWD_EQUIV = 120
TOTAL_FWD_EQUIV_BUDGET = N_ITEMS_BUDGET + STAGE2_FWD_EQUIV  # 7380

# Deflated power iteration (§4): 12-iteration cap per vector; converged when
# the Rayleigh quotient's relative change < 1e-3 for 3 consecutive iterations.
PI_MAX_ITER = 12
PI_STALL_TOL = 1e-3
PI_STALL_WINDOW = 3

# Probe-set pin (§6.1, G4): EXP077 60-record archive, sha256 verified on disk
# 2026-09-24 (matches the EXP084 signed protocol's recorded pin)
RECORDS_REL = ("..", "EXP077_cone_vs_line", "exp077_instance_records.json")
RECORDS_SHA256 = ("47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585")

# B_agg historical anchor: archived EXP077 static-semantic direction.
BAGG_REL = ("..", "EXP077_cone_vs_line", "exp077_vectors.pt")

# Tango 95% CI z (two-sided 95% -> 1.959963984540054)
Z_95 = 1.959963984540054


# ---------------------------------------------------------------------------
# Error taxonomy (loud halts, never silent passes)
# ---------------------------------------------------------------------------

class BundleError(RuntimeError):
    """Base: bundle-level loud halt."""


class CrashGuardError(BundleError):
    """Startup crash-guard refusal (before any weight access)."""


class InvalidRunError(BundleError):
    """Pre-registered INVALID row fired (§9 V1-V4)."""


class NonTestableDataError(ValueError):
    """Statistic is not testable on this data (loud, never silent drop)."""


class BlockSelectionError(BundleError):
    """Stage-A block-registry violation (e.g. rectangular block)."""


# ---------------------------------------------------------------------------
# Startup crash-guard (fail fast and loud BEFORE touching weights)
# ---------------------------------------------------------------------------

REQUIRED_MODULES = (
    "exp086_guards",
    "exp086_henrici",
    "exp086_rng",
    "exp086_statistics",
    "exp086_verdicts",
    "run_exp086",
)


def crash_guard(mode, bundle_dir=None):
    """Run every startup check that can be run without touching weights.

    mode: "stage-a", "stage-b", or "smoke". Raises CrashGuardError on any
    failure. Checks:
      1. Python >= 3.10.
      2. All bundle modules import cleanly.
      3. numpy present (Stage-A eigendecomposition; lazy torch fallback ok).
      4. Stage B: probe archive present AND sha256 == signed pin.
      5. The signed pins are the signed values (anti-drift).
    Never touches model weights, never downloads, never allocates the model.
    """
    here = bundle_dir or os.path.dirname(os.path.abspath(__file__))

    # 1. interpreter
    if sys.version_info < (3, 10):
        raise CrashGuardError(
            f"crash-guard: Python >= 3.10 required, found {sys.version.split()[0]}"
        )

    # 2. imports
    saved = list(sys.path)
    try:
        sys.path.insert(0, here)
        for mod in REQUIRED_MODULES:
            try:
                __import__(mod)
            except Exception as e:
                raise CrashGuardError(
                    f"crash-guard: bundle module '{mod}' failed to import: "
                    f"{type(e).__name__}: {e}"
                )
    finally:
        sys.path[:] = saved

    # 3. numpy (Stage-A eig backend; torch fallback attempted at runtime)
    if mode == "stage-a":
        try:
            import numpy  # noqa: F401
        except ImportError:
            # torch.linalg.eig is the runtime fallback; flag only as warning
            # here — the Stage-A path loud-halts at runtime if NEITHER exists.
            pass

    # 4. Stage-B probe archive pin (weight-free; archive is data, not weights)
    if mode == "stage-b":
        records_path = os.path.join(here, *RECORDS_REL)
        if not os.path.exists(records_path):
            raise CrashGuardError(
                f"crash-guard: probe archive missing: {records_path}"
            )
        h = hashlib.sha256()
        with open(records_path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        digest = h.hexdigest()
        if digest != RECORDS_SHA256:
            raise CrashGuardError(
                f"crash-guard: probe archive sha256 mismatch: got {digest}, "
                f"signed pin {RECORDS_SHA256}"
            )
        # 4b. B_agg anchor archive present (content validated at backend init;
        # torch-free here, so existence only).
        bagg_path = os.path.join(here, *BAGG_REL)
        if not os.path.exists(bagg_path):
            raise CrashGuardError(
                f"crash-guard: B_agg anchor archive missing: {bagg_path}"
            )
        try:
            recs = json.load(open(records_path))
        except Exception as e:
            raise CrashGuardError(f"crash-guard: archive not valid JSON: {e}")
        if len(recs) != N_ITEMS:
            raise CrashGuardError(
                f"crash-guard: archive has {len(recs)} records, pin is "
                f"N_ITEMS={N_ITEMS}"
            )

    # 5. signed-pin anti-drift
    import exp086_guards as _G  # noqa: F401  (imported above; re-check values)
    pins = {
        "MODEL_ID": (MODEL_ID, "EleutherAI/pythia-410m"),
        "LAYER_INDEX": (LAYER_INDEX, 20),
        "D_MODEL": (D_MODEL, 1024),
        "N_ITEMS": (N_ITEMS, 60),
        "MASTER_SEED": (MASTER_SEED, 20260924),
        "EPS_NORMS": (EPS_NORMS, (0.15, 0.45)),
        "HEADROOM_MIN": (HEADROOM_MIN, 15),
        "SIGMA_RATIO_ABORT": (SIGMA_RATIO_ABORT, 1.1),
        "SIGMA_RATIO_RANK_VALID": (SIGMA_RATIO_RANK_VALID, 1.2),
        "CHAT_BAR": (CHAT_BAR, 0.1),
        "DELTA_MIN": (DELTA_MIN, 0.05),
        "PI_MAX_ITER": (PI_MAX_ITER, 12),
        "PI_STALL_TOL": (PI_STALL_TOL, 1e-3),
        "PI_STALL_WINDOW": (PI_STALL_WINDOW, 3),
    }
    for name, (got, want) in pins.items():
        if got != want:
            raise CrashGuardError(
                f"crash-guard: signed pin drift: {name}={got!r}, signed {want!r}"
            )
    return True


# ---------------------------------------------------------------------------
# Frozen-backbone guard (Law #6 / Law #13): Delta theta = 0
# ---------------------------------------------------------------------------

def sha256_state_dict(state_dict):
    """SHA-256 over a state_dict mapping name -> array-like.

    Byte convention: tensors/arrays ONLY (no key names), sorted keys,
    float32 bytes — matches the historical EXP077/EXP084 hashing convention
    (run_exp084.py sha256_state_dict). Works on torch tensors and numpy
    arrays (duck-typed); the caller passes the raw state_dict.
    """
    h = hashlib.sha256()
    for k in sorted(state_dict.keys()):
        t = state_dict[k]
        if hasattr(t, "detach"):          # torch tensor
            t = t.detach().cpu()
            import torch
            arr = t.to(torch.float32).numpy()
        else:                            # numpy array or array-like
            import numpy as _np
            arr = _np.asarray(t, dtype=_np.float32)
        h.update(arr.tobytes())
    return h.hexdigest()


class FrozenBackboneGuard:
    """Law #6 guard: asserts Delta theta = 0 around a weight-touching phase.

    Usage:
        guard = FrozenBackboneGuard()
        guard.snapshot_before(state_dict)   # hashes, keeps NO copies
        ... read-only computation ...
        guard.verify_after(state_dict)      # raises InvalidRunError on mismatch
    The guard never mutates the model; it only observes hashes. Any hash
    mismatch -> pre-registered INVALID V1 (protocol §9), never a verdict.
    """

    def __init__(self):
        self.hash_before = None

    def snapshot_before(self, state_dict):
        self.hash_before = sha256_state_dict(state_dict)
        return self.hash_before

    def verify_after(self, state_dict):
        if self.hash_before is None:
            raise CrashGuardError(
                "FrozenBackboneGuard: verify_after called before snapshot_before"
            )
        h_after = sha256_state_dict(state_dict)
        if h_after != self.hash_before:
            raise InvalidRunError(
                "INVALID V1: Delta theta != 0 — state_dict hash changed during "
                f"a read-only phase (before={self.hash_before}, "
                f"after={h_after})."
            )
        return h_after


# ---------------------------------------------------------------------------
# Stage-B preflight guards (§6)
# ---------------------------------------------------------------------------

def check_headroom(n_wrong_baseline, n_items=N_ITEMS):
    """§6.2 headroom gate: >= HEADROOM_MIN wrong-at-baseline else INVALID V2."""
    if n_items != N_ITEMS:
        raise ValueError(f"n_items={n_items} != pinned N_ITEMS={N_ITEMS}")
    if n_wrong_baseline < HEADROOM_MIN:
        raise InvalidRunError(
            f"INVALID V2: headroom gate — {n_wrong_baseline} wrong-at-baseline "
            f"< {HEADROOM_MIN} (infeasible probe — do not run)."
        )
    return True


def should_abort_item(sigma1, sigma2):
    """§6.4 per-item convergence guard: abort direction arms if s1/s2 < 1.1.

    (Baseline + random arm are kept.) sigma2 <= 0 -> abort (no distinguished
    max-gain direction; the arm would degenerate to random).
    """
    if sigma2 is None or sigma2 <= 0:
        return True
    return (sigma1 / sigma2) < SIGMA_RATIO_ABORT


def check_abort_frac(n_aborted, n_items=N_ITEMS):
    """>50% items aborted -> INVALID (UNDEFINED-LANDSCAPE) V3."""
    if n_items != N_ITEMS:
        raise ValueError(f"n_items={n_items} != pinned N_ITEMS={N_ITEMS}")
    if n_aborted / n_items > MAX_ABORT_FRAC:
        raise InvalidRunError(
            f"INVALID V3: {n_aborted}/{n_items} items power-iteration "
            "non-converged (>50%) — UNDEFINED-LANDSCAPE."
        )
    return True


def rank_test_valid(sigma1, sigma3):
    """§6.4: rank test defined iff sigma1/sigma3 >= 1.2, else UNDEFINED->HELD."""
    if sigma3 is None or sigma3 <= 0:
        return False
    return (sigma1 / sigma3) >= SIGMA_RATIO_RANK_VALID


def check_apparatus(frac_moved):
    """§6.5: random delta at 0.45||h|| must move margins on >= 80% of items.

    frac_moved = fraction of items with ||Dz||_2 above the 1e-4 noise floor.
    Else INVALID V4 (proxy-unresponsive apparatus).
    """
    if frac_moved < APPARATUS_MIN_FRAC:
        raise InvalidRunError(
            f"INVALID V4: apparatus check — only {frac_moved:.3f} of items "
            f"moved margins above the {APPARATUS_NOISE_FLOOR:g} noise floor "
            f"(need >= {APPARATUS_MIN_FRAC}); proxy-unresponsive apparatus."
        )
    return True


# ---------------------------------------------------------------------------
# Pass budget (§11): 7260 fwd-equiv (60 x 121) + 120 Stage-2 = 7380 hard ceiling
# ---------------------------------------------------------------------------

class PassBudget:
    """Hard forward-equivalent counter. Refuses to exceed the signed ceiling."""

    def __init__(self, limit=TOTAL_FWD_EQUIV_BUDGET):
        self.limit = limit
        self.used = 0

    def charge(self, n=1, what=""):
        if self.used + n > self.limit:
            raise RuntimeError(
                f"PASS CEILING REFUSED: fwd-equiv {self.used}+{n} > {self.limit} "
                f"({what}). Signed budget is {TOTAL_FWD_EQUIV_BUDGET} "
                "forward-equivalents (§11); the excess pass is refused."
            )
        self.used += n

    def remaining(self):
        return self.limit - self.used
