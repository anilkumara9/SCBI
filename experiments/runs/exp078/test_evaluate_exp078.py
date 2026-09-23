"""
EXP078 evaluator branch tests.

Pure synthetic tests of evaluate() covering every branch of the pre-registered
decision tree (protocol §7), including the adversarially-reviewed edge cases:
  (1) (d) supersession: C2 rescues while C4 also rescues -> (d), not (e).
  (2) (e) + C5-also-rescues: branch stays (e); (h) does not fire alongside (e).
  (3) (f) is TERMINAL per §7.0 (canonical kill): the exact-kill cell
      (C4 b=c=0, C3 valid) -> (f), never (g)/(i); (h)/(i) are report-level
      supplementary localization notes for the (f) region, not replacements.
  (4) (g) conditional partition: C5 rescues -> (h) ("upgrades it toward (f)");
      C5 null -> (i) ("neither (e) nor (f) fires" -- literally true here).
  (5) Exact p=0.05 boundary: strict p < 0.05, so p=0.05 never counts as
      significant (C4 p=0.05 -> (g)->(i); C3 p=0.05 -> (c) invalid).
  (6) Malformed non-halt payloads normalize to "unclassified", not KeyError.
Usage:
    python test_evaluate_exp078.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evaluate_exp078 import evaluate, normalize_exp078, report


def _cond(delta_m, b=0, c=0, p=1.0):
    return {"delta_m": delta_m, "b": b, "c": c, "p": p}


def base_norm(**over):
    n = {
        "outcome": "COMPLETED",
        # C3 valid: the historical EXP066 bridge cell (8/26, +13.3pp, p=0.0078)
        "C3": _cond(0.133, b=8, c=0, p=0.0078),
        "C2": _cond(0.0),
        "C4": _cond(0.0),
        "C5": _cond(0.0),
    }
    n.update(over)
    return n


def expect(name, norm, want_branch):
    got = evaluate(norm)
    status = "PASS" if got == want_branch else "FAIL"
    print(f"[{status}] {name}: expected ({want_branch}), got ({got})")
    return got == want_branch


def report_norm(**over):
    # Minimal norm dict shaped for report() (report-level supplement tests).
    n = {
        "outcome": "COMPLETED",
        "scope": "IN-SCOPE (pythia-410m, layer 20)",
        "baseline_acc": 0.5667,
        "halt_reason": "",
        "N": 60,
        "C1": _cond(0.0), "C2": _cond(0.0),
        "C3": _cond(0.133, b=8, c=0, p=0.0078),
        "C4": _cond(0.0), "C5": _cond(0.0),
        "C6": _cond(0.0), "C7": _cond(0.0),
        "kl_flags": {}, "energy_gate": None, "subspace": None,
        "historical_baselines": {"EXP065": 0.6833, "EXP066": 0.5667},
    }
    n.update(over)
    return n


def expect_report_contains(name, norm, branch, fragments):
    txt = report(norm, branch)
    ok = all(f in txt for f in fragments)
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    return ok


def main():
    ok = True

    # (a) halts
    ok &= expect("a: HALT_ENERGY", {"outcome": "HALT_ENERGY"}, "a")
    ok &= expect("a': HALT_RANK", {"outcome": "HALT_RANK"}, "a_rank")
    ok &= expect("b: HALT_HEADROOM", {"outcome": "HALT_HEADROOM"}, "b")

    # (c) invalid run: C3 does not replicate (two variants)
    ok &= expect("c: C3 no rescue",
                 base_norm(C3=_cond(0.0, p=1.0)), "c")
    ok &= expect("c: C3 delta>0 but p>=0.05",
                 base_norm(C3=_cond(0.05, b=4, c=1, p=0.20)), "c")

    # (d) C2 rescues (ΔM>0, p<0.05); supersedes (e): C4 also rescues -> (d)
    ok &= expect("d: C2 rescues",
                 base_norm(C2=_cond(0.10, b=7, c=1, p=0.03)), "d")
    ok &= expect("d: C2 rescues while C4 also rescues -> (d) supersedes (e)",
                 base_norm(C2=_cond(0.10, b=7, c=1, p=0.03),
                           C4=_cond(0.15, b=10, c=1, p=0.01)), "d")

    # (e) C4 significant positive, C3 valid, C2 null
    ok &= expect("e: C4 rescues significantly",
                 base_norm(C4=_cond(0.133, b=8, c=0, p=0.0078)), "e")
    # (e) + C5-also-rescues: branch stays (e); (h) is conditional on (f)/(g)
    ok &= expect("e: C4 rescues, C5 also rescues -> still (e)",
                 base_norm(C4=_cond(0.133, b=8, c=0, p=0.0078),
                           C5=_cond(0.10, b=7, c=1, p=0.03)), "e")

    # (f) exact kill cell: C4 b=c=0 (ΔM≡0), C3 valid, C2 null -> (f) TERMINAL
    # per §7.0 canonical criterion (not (g), not (i)).
    ok &= expect("f: C4 b=c=0, C5 null -> (f) terminal",
                 base_norm(), "f")
    # (f) + C5 rescues: branch stays (f); (h) is a report-level supplement.
    ok &= expect("f: C4 b=c=0, C5 rescues -> still (f), (h) as report-level note",
                 base_norm(C5=_cond(0.10, b=7, c=1, p=0.03)), "f")
    # F1: report()-level supplementary localization notes for the (f) region.
    ok &= expect_report_contains(
        "f report: C5 null -> localization-limit supplement",
        report_norm(), "f",
        ["BRANCH: (f) HSUB_FALSIFIED_KILL",
         "SUPPLEMENTARY LOCALIZATION NOTE (report-level; branch unchanged)",
         "neither S nor S^perp alone rescued at unit-norm"])
    ok &= expect_report_contains(
        "f report: C5 rescues -> (h) wrong-room supplement",
        report_norm(C5=_cond(0.10, b=7, c=1, p=0.03)), "f",
        ["BRANCH: (f) HSUB_FALSIFIED_KILL",
         "SUPPLEMENTARY LOCALIZATION NOTE (report-level; branch unchanged)",
         "wrong room", "strengthens (f)'s interpretation"])

    # (g) partial: C4 b>0, p>=0.05 -> (g); C5 null -> (i)
    ok &= expect("g: C4 partial (b=5, p>=0.05), C5 null -> (i)",
                 base_norm(C4=_cond(0.083, b=5, c=0, p=0.0625)), "i")
    # (g)->(h): C4 partial, C5 rescues -> (h)
    ok &= expect("h: C4 partial, C5 rescues -> (h)",
                 base_norm(C4=_cond(0.083, b=5, c=0, p=0.0625),
                           C5=_cond(0.10, b=7, c=1, p=0.03)), "h")
    # (g) negative: C4 ΔM<0 -> (g), not (f); C5 null -> (i)
    ok &= expect("g: C4 negative delta -> (g)->(i)",
                 base_norm(C4=_cond(-0.05, b=1, c=4, p=0.20)), "i")

    # F5: exact p=0.05 boundary -- strict p < 0.05, so p=0.05 is never
    # significant. (C4 p=0.05 paths through (g), then (i) with C5 null.)
    ok &= expect("boundary: C4 ΔM>0, p=0.05 -> (g), not (e)",
                 base_norm(C4=_cond(0.10, b=6, c=0, p=0.05)), "i")
    ok &= expect("boundary: C3 ΔM>0, p=0.05 -> (c) invalid",
                 base_norm(C3=_cond(0.10, b=6, c=0, p=0.05)), "c")

    # unclassified: malformed norm (missing conditions) -> fail-safe
    ok &= expect("unclassified: missing conditions",
                 {"outcome": "COMPLETED"}, "unclassified")

    # F8: halt payloads carry diagnostics at top level (save_halt format);
    # normalize() must rebuild the display dicts so report() surfaces the
    # values §7.1(a) requires (§7.1(a): e distribution evidentially non-empty).
    _halt_energy = normalize_exp078({
        "experiment": "EXP078", "outcome": "HALT_ENERGY",
        "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
        "halt_reason": "energy gate failed",
        "e_median": 0.03,
        "e_distribution": {"min": 0.01, "median": 0.03, "max": 0.09},
        "e_sensitivity": {"0.05": False, "0.10": False, "0.15": False},
        "energy_bar": 0.10})
    ok &= expect("a: HALT_ENERGY branch", _halt_energy, "a")
    ok &= expect_report_contains(
        "a report: top-level halt diagnostics surface e values",
        _halt_energy, "a",
        ["e_median = 0.03", "bar = 0.1", "passed = False"])
    _halt_rank = normalize_exp078({
        "experiment": "EXP078", "outcome": "HALT_RANK",
        "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
        "halt_reason": "rank guard failed",
        "rank_ratio": 5e-8, "singular_values": [3.1, 2.2, 1.0, 0.5, 1e-7]})
    ok &= expect("a': HALT_RANK branch", _halt_rank, "a_rank")
    ok &= expect_report_contains(
        "a' report: top-level halt diagnostics surface rank diagnostics",
        _halt_rank, "a_rank",
        ["sigma_min/sigma_max = 5e-08"])

    # F9: malformed non-halt PAYLOAD (through normalize_exp078) -> the
    # "unclassified" fail-safe, not a KeyError crash; report() stays intact.
    _malformed = normalize_exp078({"experiment": "EXP078", "outcome": "COMPLETED",
                                   "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
                                   "baseline_accuracy": 0.5667})
    ok &= expect("unclassified: malformed payload (no stage_B_conditions)",
                 _malformed, "unclassified")
    ok &= expect_report_contains(
        "unclassified report: malformed payload renders without crashing",
        _malformed, "unclassified",
        ["BRANCH: (unclassified) UNCLASSIFIED",
         "malformed results payload"])

    print()
    if ok:
        print("ALL EXP078 EVALUATOR BRANCH TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
