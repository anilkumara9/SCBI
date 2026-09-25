"""EXP084 guards: Newton definedness, exclusion classification, INVALID checks.

Implements the signed protocol §3 (corrected Newton-definedness guard) and
§7 INVALID rows (i)-(iv). All thresholds are pre-registered pins.

- KAPPA_FLOOR = 1e-6 (LOG-262 adjudicated CONFIRM, sign-corrected).
- Newton arm (b) is DEFINED iff kappa_dir < -KAPPA_FLOOR (concave regime
  for the maximization objective). Excluded iff kappa_dir >= -KAPPA_FLOOR.
- Exclusion split (R3a, §7 F7 attribution):
    convex-uphill: kappa_dir >= +KAPPA_FLOOR
    too-flat:      -KAPPA_FLOOR <= kappa_dir < +KAPPA_FLOOR
- INVALID(iii): arm (b) defined on < 12 of 24 items -> UNDEFINED-LANDSCAPE.
"""

KAPPA_FLOOR = 1e-6
MIN_DEFINED_ITEMS = 12
N_ITEMS = 24


def is_newton_defined(kappa_dir: float) -> bool:
    """True iff the scalar-curvature Newton step is defined for maximization.

    Definedness guard (signed §3, corrected per R1/LOG-262): the 1-D quadratic
    model along ĝ is concave (a maximizer exists) iff kappa_dir < -KAPPA_FLOOR.
    """
    return kappa_dir < -KAPPA_FLOOR


def classify_exclusion(kappa_dir: float) -> str:
    """Classify an excluded item into the §7 F7 attribution split.

    Returns "convex-uphill" if kappa_dir >= +KAPPA_FLOOR (Newton-for-
    maximization undefined; model unbounded above along +ĝ), else
    "too-flat" for -KAPPA_FLOOR <= kappa_dir < +KAPPA_FLOOR (LOG-248 κR²
    regime: second order provably negligible at this scale).

    Raises ValueError if called on a defined item (kappa_dir < -KAPPA_FLOOR).
    """
    if is_newton_defined(kappa_dir):
        raise ValueError(
            "classify_exclusion called on a defined item "
            f"(kappa_dir={kappa_dir} < -KAPPA_FLOOR)"
        )
    if kappa_dir >= KAPPA_FLOOR:
        return "convex-uphill"
    return "too-flat"


def check_invalid_iii(n_defined: int, n_total: int = N_ITEMS) -> bool:
    """INVALID(iii): True iff arm (b) is defined on < 12 of 24 items.

    Returns True when the run is INVALID/UNDEFINED-LANDSCAPE (the duel
    cannot run; not a family kill). n_total is pinned at 24 by the protocol.
    """
    if n_total != N_ITEMS:
        raise ValueError(f"n_total={n_total} != pinned N_ITEMS={N_ITEMS}")
    return n_defined < MIN_DEFINED_ITEMS


def newton_step_length(grad_norm: float, kappa_dir: float) -> float:
    """Natural Newton step length alpha* = ||g|| / |kappa_dir|.

    Valid only where defined (kappa_dir < -KAPPA_FLOOR); raises ValueError
    otherwise. No cap, no rescaling (F1 repair (a)).
    """
    if not is_newton_defined(kappa_dir):
        raise ValueError(
            "Newton step undefined: kappa_dir must be < -KAPPA_FLOOR "
            f"(got {kappa_dir})"
        )
    if grad_norm < 0:
        raise ValueError(f"grad_norm must be non-negative (got {grad_norm})")
    return grad_norm / abs(kappa_dir)
