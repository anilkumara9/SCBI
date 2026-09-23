"""
EXP079 evaluator branch tests + calibrated null-bar tests.

Pure synthetic tests of evaluate() covering every branch of the pre-registered
decision tree (§8), plus the adversarially-reviewed edge cases:
  (1) (f)+(c2*) co-fire: gate failed AND C4 >= C3 -> (f) must take precedence
      and subsume (c2*) (table-row reading, LOG-121).
  (2) (f)+(e) co-fire: C3 significant AND >= +12pp vs C2, while C4 >= C3
      -> (f) must take precedence and suspend (e)'s license.
  (3) Exact bar boundaries: dm = +12pp exactly with p < 0.05 -> (e);
      dm just below -> (d); p = 0.05 exactly -> not significant -> (c1*)/(c2*).
  (4) Historical falling-through cell b=5, c=0, +8.3pp, p=0.0625
      (EXP065 bridge) -> must route to (c1*) (gate passed) or (c2*)
      (gate failed), never fall through.
  (5) All three halt outcomes -> (a).
  (6) The calibrated H_sel null bar (runner function): N=60 -> 0.150,
      N=50 -> 0.160 (spec [FACT -- computed], seed 7979, 100k draws).
Usage:
    python test_evaluate_exp079.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evaluate_exp079 import evaluate, WORTH_CHASING_BAR
from run_exp079 import compute_hsel_null_bar


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

    # (a) halts (all three halt outcomes)
    ok &= expect("a: HALT_PROBE", {"outcome": "HALT_PROBE"}, "a")
    ok &= expect("a: HALT_HEADROOM", {"outcome": "HALT_HEADROOM"}, "a")
    ok &= expect("a: HALT_DEGENERACY", {"outcome": "HALT_DEGENERACY"}, "a")

    # (b) invalid run: C7 does not rescue (also when p >= 0.05 with delta>0)
    ok &= expect("b: C7 no rescue",
                 base_norm(C7=_cond(0.0, p=1.0)), "b")
    ok &= expect("b: C7 delta>0 but p>=0.05",
                 base_norm(C7=_cond(0.02, p=0.30)), "b")

    # (c1*) canonical kill (calibrated-probe-gated): no sig gain, gate passed.
    # C3 > C4 on delta vs baseline so (f) clause 1 does not fire; clause 2
    # needs both beating C2 significantly, which is absent.
    ok &= expect("c1*: no sig gain + gate passed",
                 base_norm(C3=_cond(0.02, b=3, c=2, p=0.50),
                           cmp_C3_C2=_cmp(0.02, b=3, c=2, exact_p=0.50)), "c1*")

    # (c2*) still-uninformative probe: no sig gain, gate failed.
    # C3's ΔM vs baseline (0.02) strictly exceeds C4's (0.0) so (f) clause 1
    # does not fire; clause 2 needs significant positives, absent.
    ok &= expect("c2*: no sig gain + gate failed",
                 base_norm(C3=_cond(0.02, b=3, c=2, p=0.50),
                           cmp_C3_C2=_cmp(0.02, b=3, c=2, exact_p=0.50),
                           gate_passed=False), "c2*")

    # (c3*) oracle significantly worse than static (ungated by the probe gate).
    # (f) clause 1 must not fire: C4's delta vs baseline is BELOW C3's;
    # clause 2 needs sig-positive vs C2, absent.
    ok &= expect("c3*: C3 significantly worse than C2",
                 base_norm(C3=_cond(-0.05, b=1, c=7, p=0.01),
                           C4=_cond(-0.10, b=0, c=6, p=0.03),
                           cmp_C3_C2=_cmp(-0.10, b=1, c=7, exact_p=0.0156)),
                 "c3*")
    # (c3*) fires even when the gate FAILED (ungated significant negative).
    ok &= expect("c3*: significant negative, gate failed (ungated)",
                 base_norm(C3=_cond(-0.05, b=1, c=7, p=0.01),
                           C4=_cond(-0.10, b=0, c=6, p=0.03),
                           cmp_C3_C2=_cmp(-0.10, b=1, c=7, exact_p=0.0156),
                           gate_passed=False), "c3*")

    # (d) oracle wins small: significant positive below the +12pp bar.
    # (f) clause 1 must not fire: C4's delta vs baseline (0.0) is below C3's.
    ok &= expect("d: sig positive below +12pp",
                 base_norm(C3=_cond(0.10, b=8, c=2, p=0.02),
                           cmp_C3_C2=_cmp(0.10, b=8, c=2, exact_p=0.02)), "d")
    ok &= expect("d: dm just below bar (0.1199)",
                 base_norm(C3=_cond(0.1199, b=8, c=0, p=0.0078),
                           cmp_C3_C2=_cmp(0.1199, b=8, c=0, exact_p=0.0078)), "d")

    # (e) oracle wins big: >= +12pp [ARBITRARY] with p < 0.05.
    ok &= expect("e: dm exactly +12pp, p<0.05",
                 base_norm(C3=_cond(0.12, b=9, c=1, p=0.01),
                           cmp_C3_C2=_cmp(0.12, b=9, c=1, exact_p=0.01)), "e")
    ok &= expect("e: dm +16.7pp, p<0.05",
                 base_norm(C3=_cond(0.1667, b=10, c=0, p=0.002),
                           cmp_C3_C2=_cmp(0.1667, b=10, c=0, exact_p=0.002)), "e")

    # p = 0.05 exactly is NOT significant -> (c1*)/(c2*), never (d)/(e).
    ok &= expect("p=0.05 exactly + gate passed -> c1*",
                 base_norm(C3=_cond(0.13, b=8, c=1, p=0.05),
                           cmp_C3_C2=_cmp(0.13, b=8, c=1, exact_p=0.05)), "c1*")
    ok &= expect("p=0.05 exactly + gate failed -> c2*",
                 base_norm(C3=_cond(0.13, b=8, c=1, p=0.05),
                           cmp_C3_C2=_cmp(0.13, b=8, c=1, exact_p=0.05),
                           gate_passed=False), "c2*")

    # (f) clause 1: C4 (random) >= C3 on ΔM vs baseline.
    ok &= expect("f: clause 1 (C4 >= C3), gate passed",
                 base_norm(C4=_cond(0.06, b=5, c=1, p=0.08),
                           C3=_cond(0.05, b=4, c=1, p=0.10),
                           cmp_C3_C2=_cmp(0.05, b=4, c=1, exact_p=0.10),
                           gate_passed=True), "f")
    # (f) clause 2: C3 ~= C4 while both beat C2.
    ok &= expect("f: clause 2 (both beat C2, indistinguishable)",
                 base_norm(C3=_cond(0.10, b=8, c=2, p=0.02),
                           C4=_cond(0.10, b=8, c=2, p=0.02),
                           cmp_C3_C2=_cmp(0.10, b=8, c=2, exact_p=0.02),
                           cmp_C4_C2=_cmp(0.10, b=8, c=2, exact_p=0.02),
                           cmp_C3_C4=_cmp(0.0, b=2, c=2, exact_p=1.0)), "f")

    # Edge (1): (f)+(c2*) co-fire -> (f) dominates (table-row reading, LOG-121).
    ok &= expect("f-fires + c2* conditions: (f), not (c2*)",
                 base_norm(C4=_cond(0.06, b=5, c=1, p=0.08),
                           C3=_cond(0.05, b=4, c=1, p=0.10),
                           cmp_C3_C2=_cmp(0.05, b=4, c=1, exact_p=0.10),
                           gate_passed=False), "f")

    # Edge (2): (f)+(e) co-fire -> (f) suspends (e)'s license.
    ok &= expect("f-fires + e conditions: (f), not (e)",
                 base_norm(C3=_cond(0.15, b=10, c=1, p=0.01),
                           C4=_cond(0.16, b=11, c=1, p=0.006),
                           cmp_C3_C2=_cmp(0.15, b=10, c=1, exact_p=0.01)), "f")

    # Edge (4): historical falling-through cell (EXP065 bridge): b=5, c=0,
    # +8.3pp, p=0.0625 -> (c1*) or (c2*), never fall through.
    ok &= expect("historical cell + gate passed -> c1*",
                 base_norm(C3=_cond(0.083, b=5, c=0, p=0.0625),
                           cmp_C3_C2=_cmp(0.083, b=5, c=0, exact_p=0.0625),
                           gate_passed=True), "c1*")
    ok &= expect("historical cell + gate failed -> c2*",
                 base_norm(C3=_cond(0.083, b=5, c=0, p=0.0625),
                           cmp_C3_C2=_cmp(0.083, b=5, c=0, exact_p=0.0625),
                           gate_passed=False), "c2*")

    # Edge (6): calibrated H_sel null bar (spec §8 [FACT -- computed]).
    bar60 = compute_hsel_null_bar(60)
    bar50 = compute_hsel_null_bar(50)
    b60_ok = abs(bar60 - 0.150) < 1e-9
    b50_ok = abs(bar50 - 0.160) < 1e-9
    print(f"[{'PASS' if b60_ok else 'FAIL'}] null bar N=60: expected 0.150, got {bar60:.6f}")
    print(f"[{'PASS' if b50_ok else 'FAIL'}] null bar N=50: expected 0.160, got {bar50:.6f}")
    ok &= b60_ok and b50_ok
    # Bar must adapt to N_final: smaller N -> higher bar (sanity of monotonicity).
    mono_ok = compute_hsel_null_bar(55) > bar60
    print(f"[{'PASS' if mono_ok else 'FAIL'}] null bar monotonic in N (bar55 > bar60)")
    ok &= mono_ok

    print()
    if ok:
        print("ALL EXP079 EVALUATOR BRANCH TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
