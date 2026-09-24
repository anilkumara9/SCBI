"""K2 routing-vs-bypass — authoritative evaluator (LOG-226).

Reads k2_results.json (+ k2_instance_records.json) and re-derives the
pre-registered ruling from the archived per-item outcomes, independently
of the runner's display verdict. The evaluator is authoritative; the
runner's verdict is display only.

Usage:
    python3 evaluate_k2.py [--results k2_results.json] [--records k2_instance_records.json]

Exit codes: 0 = ruling derived (any verdict incl. Underdetermined);
            2 = artifact problem (missing/inconsistent records).
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2_endpoints import adjudicate_verdict
from k2_guards import guards_evaluate, g10_exclusion_floor_check, DELTA_MIN


def main():
    ap = argparse.ArgumentParser(description="K2 authoritative evaluator")
    ap.add_argument("--results", default="k2_results.json")
    ap.add_argument("--records", default="k2_instance_records.json")
    args = ap.parse_args()

    for p in (args.results, args.records):
        if not os.path.isfile(p):
            print(f"EVALUATOR FATAL: artifact missing: {p}")
            return 2
    with open(args.results, encoding="utf-8") as f:
        res = json.load(f)
    with open(args.records, encoding="utf-8") as f:
        recs = json.load(f)

    included = [r for r in recs if not r.get("excluded")]
    base = [bool(r["baseline_C1"]) for r in included]
    a = [bool(r["correct"]["a"]) for r in included]
    b = [bool(r["correct"]["b"]) for r in included]
    c = [bool(r["correct"]["c"]) for r in included]
    exclusions = res.get("exclusions", [])

    # Row-5 pre-adjudication from the runner's guard record (re-checked here).
    guard_record = {
        "g1_invalid": res.get("g1_invalid", False),
        "g3_pre_post_match": res.get("g3_pre_post_match", False),
        "g4_pass_count_ok": res.get("g4", {}).get("ok", False),
        "g4_expected": res.get("g4", {}).get("expected"),
        "g4_got": res.get("g4", {}).get("got"),
        "g5_c_gate_passed": res.get("g5_c_gate", {}).get("passed", False),
        "b_c": res.get("g5_c_gate", {}).get("b_c"),
        "records_missing": False,
        "exclusions": exclusions,
    }
    underdet, cause = guards_evaluate(guard_record)
    if underdet:
        ruling = {"row": 5, "verdict_routing": "Underdetermined",
                  "verdict_final_position_local": "Underdetermined",
                  "cause": cause}
    else:
        v = adjudicate_verdict(base, a, b, c, exclusions,
                               c_gate_passed=guard_record["g5_c_gate_passed"])
        ruling = {"row": v["row"],
                  "verdict_routing": v["verdict_routing"],
                  "verdict_final_position_local": v["verdict_final_position_local"],
                  "consequence": v["consequence"],
                  "n_actual": v["n_actual"],
                  "row3_reason": v.get("row3_reason"),
                  "contrast": {"d_hat": v["contrast_b_vs_a"]["d_hat"],
                               "tango_L": v["contrast_b_vs_a"]["tango_L"],
                               "tango_U": v["contrast_b_vs_a"]["tango_U"],
                               "b": v["contrast_b_vs_a"]["b"],
                               "c": v["contrast_b_vs_a"]["c"]},
                  "arm_a": {"d_hat": v["arm_a"]["d_hat"], "b": v["arm_a"]["b"],
                            "c": v["arm_a"]["c"], "tango_L": v["arm_a"]["tango_L"],
                            "tango_U": v["arm_a"]["tango_U"],
                            "tango_U_1s": v["arm_a"]["tango_U_1s"],
                            "mcnemar_p": v["arm_a"]["mcnemar_p"]},
                  "arm_b": {"d_hat": v["arm_b"]["d_hat"], "b": v["arm_b"]["b"],
                            "c": v["arm_b"]["c"], "tango_L": v["arm_b"]["tango_L"],
                            "tango_U": v["arm_b"]["tango_U"],
                            "mcnemar_p": v["arm_b"]["mcnemar_p"]},
                  "arm_c": {"d_hat": v["arm_c"]["d_hat"], "b": v["arm_c"]["b"],
                            "c": v["arm_c"]["c"]}}

    # Consistency check vs the runner's display verdict (informational).
    disp = res.get("verdict", {})
    consistent = (disp.get("row") == ruling["row"] and
                  disp.get("verdict_routing") == ruling["verdict_routing"])
    ruling["runner_display_consistent"] = bool(consistent)

    print("=" * 78)
    print("K2 AUTHORITATIVE RULING (evaluate_k2.py)")
    print("=" * 78)
    print(f"row: {ruling['row']}")
    print(f"routing: {ruling['verdict_routing']}")
    print(f"final-position-local: {ruling['verdict_final_position_local']}")
    if "consequence" in ruling:
        print(f"consequence: {ruling['consequence']}")
    if "arm_a" in ruling:
        print(f"arm_a flatness bar: U_1s(dM_a)={ruling['arm_a']['tango_U_1s']:.4f} "
              f"({'< 0.05 row-1 flatness CLEARS' if ruling['arm_a']['tango_U_1s'] < 0.05 else '>= 0.05 row-1 flatness FAILS'})")
    if "cause" in ruling:
        print(f"cause: {ruling['cause']}")
    print(f"runner display consistent: {ruling['runner_display_consistent']}")
    if ruling["row"] in (2, "2r"):
        print("NOTE: a cell-2 verdict is provisional-pending the official-bench "
              "replication (REV2 §7) before the P2 pivot is treated as settled.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
