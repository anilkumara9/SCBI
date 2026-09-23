"""
EXP070 evaluator branch tests.

Pure synthetic tests of evaluate() covering every branch of the pre-registered
decision tree (§8), plus the two adversarially-reviewed edge cases:
  (1) (f)+(e) co-fire: C3 significant AND >= +12pp vs C2, while C4 >= C3
      -> (f) must take precedence and suspend (e)'s license.
  (2) Historical falling-through cell b=5, c=0, +8.3pp, p=0.0625
      (EXP065 bridge) -> must route to (c1) (gate passed) or (c2)
      (gate failed), never fall through.
Usage:
    python test_evaluate_exp070.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evaluate_exp070 import evaluate, WORTH_CHASING_BAR


def _cond(delta_m, b=0, c=0, p=1.0):
    return {"delta_m": delta_m, "b": b, "c": c, "p": p}


def _cmp(delta_m, b=0, c=0, exact_p=1.0):
    return {"delta_m": delta_m, "b": b, "c": c, "exact_p": exact_p}


def base_norm(**over):
    n = {
        "outcome": "COMPLETED",
        "C7": _cond(0.1667, b=10, c=0, p=0.002),
        "C3": _cond(0.0),
        "C4": _cond(0.0),
        "cmp_C3_C2": _cmp(0.0),
        "cmp_C3_C4": _cmp(0.0),
        "cmp_C4_C2": _cmp(0.0),
        "gate_passed": True,
    }
    n.update(over)
    return n


def expect(name, norm, want_branch):
    got = evaluate(norm)
    status = "PASS" if got == want_branch else "FAIL"
    print(f"[{status}] {name}: expected ({want_branch}), got ({got})")
    return got == want_branch


def main():
    ok = True

    # (a) halts (both halt outcomes)
    ok &= expect("a: HALT_PROBE", {"outcome": "HALT_PROBE"}, "a")
    ok &= expect("a: HALT_HEADROOM", {"outcome": "HALT_HEADROOM"}, "a")

    # (b) invalid run: C7 does not rescue (also when p >= 0.05 with delta>0)
    ok &= expect("b: C7 no rescue",
                 base_norm(C7=_cond(0.0, p=1.0)), "b")
    ok &= expect("b: C7 delta>0 but p>=0.05",
                 base_norm(C7=_cond(0.02, p=0.30)), "b")

    # (c1) canonical kill: no sig gain, gate passed. C3 > C4 on delta vs
    # baseline so (f) clause 1 does not fire (0.02 > 0.0); clause 2 needs both
    # beating C2 significantly, which is absent.
    ok &= expect("c1: no sig gain + gate passed",
                 base_norm(C3=_cond(0.02, b=3, c=2, p=0.50),
                           cmp_C3_C2=_cmp(0.02, b=3, c=2, exact_p=0.50)), "c1")

    # (c2) uninformative probe: no sig gain, gate failed
    ok &= expect("c2: no sig gain + gate failed",
                 base_norm(gate_passed=False), "c2")

    # (c3) oracle significantly worse than static (ungated by the probe gate).
    # (f) clause 1 must not fire: C4's delta vs baseline is BELOW C3's
    # (-0.10 < -0.05); clause 2 needs sig-positive vs C2, absent.
    ok &= expect("c3: C3 significantly worse than C2",
                 base_norm(C3=_cond(-0.05, b=1, c=7, p=0.01),
                           C4=_cond(-0.10, b=0, c=8, p=0.01),
                           cmp_C3_C2=_cmp(-0.05, b=1, c=7, exact_p=0.01),
                           gate_passed=False),
                 "c3")

    # (d) significant positive but below +12pp
    ok &= expect("d: sig +8.3pp < +12pp",
                 base_norm(C3=_cond(0.083, b=8, c=3, p=0.01),
                           cmp_C3_C2=_cmp(0.083, b=8, c=3, exact_p=0.01),
                           cmp_C4_C2=_cmp(0.0)), "d")

    # (e) significant positive >= +12pp
    ok &= expect("e: sig +15pp >= +12pp",
                 base_norm(C3=_cond(0.15, b=10, c=1, p=0.01),
                           cmp_C3_C2=_cmp(0.15, b=10, c=1, exact_p=0.01)), "e")

    # (e) boundary: exactly +12pp clears the bar (protocol: >= +12pp)
    ok &= expect("e: exactly +12pp clears bar",
                 base_norm(C3=_cond(WORTH_CHASING_BAR, b=9, c=2, p=0.02),
                           cmp_C3_C2=_cmp(WORTH_CHASING_BAR, b=9, c=2, exact_p=0.02)), "e")

    # (d) boundary: +12pp - epsilon routes to (d)
    ok &= expect("d: +12pp-epsilon routes to d",
                 base_norm(C3=_cond(0.1199, b=9, c=2, p=0.02),
                           cmp_C3_C2=_cmp(0.1199, b=9, c=2, exact_p=0.02)), "d")

    # (f) clause 1: C4 >= C3 on delta vs baseline (C4 >= C3 fires even when
    # C3_vs_C2 is non-significant)
    ok &= expect("f: C4 >= C3 clause 1",
                 base_norm(C3=_cond(0.05, b=4, c=1, p=0.10),
                           C4=_cond(0.06, b=5, c=1, p=0.08),
                           cmp_C3_C2=_cmp(0.05, b=4, c=1, exact_p=0.10)), "f")

    # (f) clause 2: C3 ~= C4 while both beat C2 (operationalization:
    # both sig positive vs C2, head-to-head indistinguishable). Set C4's delta
    # vs baseline below C3's so clause 1 does NOT fire; clause 2 must fire.
    ok &= expect("f: clause 2, both beat C2, C3~=C4",
                 base_norm(C3=_cond(0.05, b=4, c=1, p=0.10),
                           C4=_cond(0.04, b=3, c=1, p=0.15),
                           cmp_C3_C2=_cmp(0.15, b=10, c=1, exact_p=0.01),
                           cmp_C4_C2=_cmp(0.13, b=9, c=1, exact_p=0.02),
                           cmp_C3_C4=_cmp(0.01, b=2, c=1, exact_p=0.60)), "f")

    # Edge case 1: (f)+(e) co-fire -- (f) must take precedence and suspend (e).
    # C3 sig >= +12pp vs C2, but C4's delta vs baseline >= C3's.
    ok &= expect("f+e co-fire: (f) precedence suspends (e)",
                 base_norm(C3=_cond(0.15, b=10, c=1, p=0.01),
                           C4=_cond(0.16, b=11, c=1, p=0.005),
                           cmp_C3_C2=_cmp(0.15, b=10, c=1, exact_p=0.01)), "f")

    # Edge case 2: historical falling-through cell b=5, c=0, +8.3pp, p=0.0625
    # (EXP065 bridge result; p >= 0.05 -> not significant). The synthetic norm
    # is made self-consistent: C3 delta vs baseline = +8.3pp (> C4's 0.0) so
    # (f) clause 1 does not fire, and neither clause 2 condition holds.
    ok &= expect("historical cell + gate passed -> c1",
                 base_norm(C3=_cond(0.083, b=5, c=0, p=0.0625),
                           cmp_C3_C2=_cmp(0.083, b=5, c=0, exact_p=0.0625)), "c1")
    ok &= expect("historical cell + gate failed -> c2",
                 base_norm(C3=_cond(0.083, b=5, c=0, p=0.0625),
                           cmp_C3_C2=_cmp(0.083, b=5, c=0, exact_p=0.0625),
                           gate_passed=False), "c2")

    # (f) clause 1 with gate failed and p >= 0.05: (c2) probe logic preserved
    # (m8 review): (f) suspends (c1)/(c3)/(d)/(e), NOT (c2).
    ok &= expect("f-fires + c2 conditions: (c2) preserved",
                 base_norm(C4=_cond(0.06, b=5, c=1, p=0.08),
                           C3=_cond(0.05, b=4, c=1, p=0.10),
                           cmp_C3_C2=_cmp(0.05, b=4, c=1, exact_p=0.10),
                           gate_passed=False), "c2")

    # (f) clause 1 with gate PASSED and p >= 0.05: (f), not (c1).
    ok &= expect("f-fires + c1 conditions: (f), not (c1)",
                 base_norm(C4=_cond(0.06, b=5, c=1, p=0.08),
                           C3=_cond(0.05, b=4, c=1, p=0.10),
                           cmp_C3_C2=_cmp(0.05, b=4, c=1, exact_p=0.10),
                           gate_passed=True), "f")

    print()
    if ok:
        print("ALL EXP070 EVALUATOR BRANCH TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
