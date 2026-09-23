"""
EXP070 decision-tree evaluator (protocol §8, pre-registered).

Reads exp070_results.json and outputs the pre-registered ruling branch VERBATIM.
No new statistics are invented: McNemar exact p, (b, c), ΔM, the probe-signal
gate, and halt flags are read from the artifact. Margin shifts are never
confirmatory (audit Finding 3 / O5) and are not consulted here.

Precedence (protocol §8, m8 review):
    (a) halts -> (b) invalid run -> (f) [before (c1)/(c3)/(d)/(e);
    a fired (f) suspends their selection licenses, but NOT (c2)'s probe
    logic] -> kill/comparison branches.

The probe-signal gate (§8) is evaluated on entering branch (c), BEFORE any
(c1)/(c2) ruling: it is read from results.json["probe_gate"] (computed by
run_exp070.py per §6), never recomputed here.

Usage:
    python evaluate_exp070.py [path/to/exp070_results.json]
"""

import os
import sys
import json
import argparse

WORTH_CHASING_BAR = 0.12   # +12pp [ARBITRARY -- sensitivity analysis required]
SENSITIVITY_BANDS = [0.12, 0.16, 0.20]

RULINGS = {
    "a": ("Branch (a): readiness/headroom gate halted. RULING: reportable halt, not a "
          "result about selection. LICENSES: 'the benchmark/probe preconditions for the "
          "ceiling measurement are not met.' DOES NOT LICENSE: anything about H_loop."),
    "b": ("Branch (b): C7 positive control FAILED (bridge: ΔM <= 0 or p >= 0.05). RULING: "
          "invalid run -- setup broken or benchmark drifted. NO conclusion about "
          "H_ceiling or H_loop may be drawn; do not interpret C3 in an invalid run."),
    "c1": ("Branch (c1) -- CANONICAL KILL (probe-gated): C3 vs C2 shows no statistically "
          "significant gain (p >= 0.05), and the probe-signal gate PASSED. RULING: "
          "justification WITHDRAWN -- EXP068 is cancelled in its current form. LICENSES: "
          "'No label-informed selection over this pool beats static injection here; the "
          "ceiling was measured, not merely unmeasured; therefore no target-free evaluator "
          "over the same pool can justify the loop's cost.' DOES NOT LICENSE: falsification "
          "of H_loop (never tested); 'representation-level adaptation is impossible in "
          "general' (family-, model-, benchmark-restricted); 'the loop's evaluator would "
          "fail'; 'steering is impossible'; anything about directions outside the pool "
          "(A-pool, protocol §7)."),
    "c2": ("Branch (c2): C3 vs C2 shows no gain as in (c1), but the probe-signal gate "
          "FAILED. RULING: ceiling UNMEASURED -- EXP068 is explicitly NOT cancelled. "
          "LICENSES: 'The probe carried no transferable signal, so no ceiling was measured.' "
          "Required next step: re-register with a better probe (next free number); never a "
          "silent re-run under EXP070. DOES NOT LICENSE: any statement about the pool's "
          "ceiling; EXP068 cancellation."),
    "c3": ("Branch (c3): C3 vs C2 significant (p < 0.05) with ΔM_oracle - ΔM_static < 0. "
          "RULING: justification WITHDRAWN -- EXP068 is cancelled in its current form "
          "(stronger than (c1)). LICENSES: 'Per-instance selection over this pool actively "
          "hurts vs static.' Ungated: a significant negative is itself a measured effect. "
          "DOES NOT LICENSE: anything in the (c1) DOES-NOT-LICENSE column."),
    "d": ("Branch (d): C3 beats C2 significantly (p < 0.05) but the margin is below the "
          "+12pp worth-chasing bar [ARBITRARY]. RULING: ambiguous -- EXP068 NOT justified. "
          "LICENSES: 'a selection signal exists but is below the worth-chasing bar.' "
          "DOES NOT LICENSE: EXP068 justification; H_loop confirmation."),
    "e": ("Branch (e): C3 beats C2 by >= +12pp [ARBITRARY] with p < 0.05. RULING: EXP068 "
          "JUSTIFIED -- explicitly NOT validated. LICENSES: 'a per-instance selection prize "
          "exists; the oracle-static gap quantifies the verifier's worth; proceed to build "
          "the loop.' DOES NOT LICENSE: 'the loop will work'; 'a target-free evaluator can "
          "recover the gap'; any novelty-tier movement (N1 stands); 'invention' beyond "
          "selection among support-derived candidates."),
    "f": ("Branch (f): no selection signal -- C4 (random) >= C3, or C3 ~= C4 while both "
          "beat C2. RULING: do not kill or justify on selection grounds. LICENSES: 'the "
          "pool helps but selection doesn't -- or the oracle methodology is uninformative.' "
          "Diagnose probe leakage/noise via §6 diagnostics before any re-registration. A C4 > "
          "C2 finding alone is a pool-quality result, not a loop justification. (A fired (f) "
          "suspends the selection licenses of (c1)/(c3)/(d)/(e).)"),
    "unclassified": ("No pre-registered branch matches this outcome. RULING: report raw statistics "
          "only; DO NOT interpret. (Fail-safe: the protocol's tree should be exhaustive; "
          "an unclassified outcome indicates a schema or logic error -- investigate.)"),
}

BRANCH_NAMES = {
    "a": "READINESS_HEADROOM_HALT",
    "b": "INVALID_RUN",
    "c1": "CANONICAL_KILL",
    "c2": "UNINFORMATIVE_PROBE",
    "c3": "ORACLE_WORSE_THAN_STATIC",
    "d": "ORACLE_WINS_SMALL",
    "e": "ORACLE_WINS_BIG",
    "f": "NO_SELECTION_SIGNAL",
    "unclassified": "UNCLASSIFIED",
}


def sig_positive(cmp):
    return (cmp["delta_m"] > 0) and (cmp["exact_p"] < 0.05)


def evaluate(norm):
    """Pure decision-tree function.

    norm keys: outcome, C7 {delta_m,p}, C3 {delta_m}, C4 {delta_m},
    cmp_C3_C2/cmp_C3_C4/cmp_C4_C2 {delta_m,b,c,exact_p}, gate_passed (bool|None).
    Returns the branch letter ("a".."f"/"unclassified").
    """
    outcome = norm.get("outcome", "COMPLETED")
    if outcome in ("HALT_PROBE", "HALT_HEADROOM"):
        return "a"

    c7 = norm["C7"]
    if not ((c7["delta_m"] > 0) and (c7["p"] < 0.05)):
        return "b"

    c3c2 = norm["cmp_C3_C2"]
    c3c4 = norm["cmp_C3_C4"]
    c4c2 = norm["cmp_C4_C2"]

    # (f) precedence: evaluated before (c1)/(c3)/(d)/(e). Clause 1: random >=
    # oracle on ΔM vs baseline. Clause 2 (conservative operationalization of
    # "C3 ~= C4 while both beat C2"): both beat static significantly and the
    # head-to-head is indistinguishable.
    f_fires = (norm["C4"]["delta_m"] >= norm["C3"]["delta_m"]) or (
        sig_positive(c3c2) and sig_positive(c4c2) and (c3c4["exact_p"] >= 0.05))
    if f_fires:
        # (f) suspends the selection licenses of (c1)/(c3)/(d)/(e), but NOT
        # (c2)'s probe logic: an uninformative probe is still reported as such.
        if (c3c2["exact_p"] >= 0.05) and (norm["gate_passed"] is False):
            return "c2"
        return "f"

    p, dm = c3c2["exact_p"], c3c2["delta_m"]
    if p < 0.05 and dm < 0:
        return "c3"
    if p < 0.05 and dm >= WORTH_CHASING_BAR:
        return "e"
    if p < 0.05 and dm > 0:
        return "d"
    # p >= 0.05: the probe-signal gate (evaluated on entering branch (c),
    # BEFORE any kill ruling) decides (c1) vs (c2).
    if norm["gate_passed"] is True:
        return "c1"
    if norm["gate_passed"] is False:
        return "c2"
    return "unclassified"


def cond_stats(d):
    return {"delta_m": float(d["delta_m"]), "b": int(d["rescues_b"]),
            "c": int(d["corruptions_c"]), "p": float(d["exact_p"])}


def cmp_stats(d):
    return {"delta_m": float(d["delta_m"]), "b": int(d["b"]),
            "c": int(d["c"]), "exact_p": float(d["exact_p"])}


def normalize_exp070(payload):
    # Halt payloads (probe-construction / headroom gates) carry no
    # stage_B_conditions: check `outcome` FIRST (M1 lesson from EXP067).
    outcome = payload.get("outcome", "COMPLETED")
    if outcome in ("HALT_PROBE", "HALT_HEADROOM"):
        return {
            "outcome": outcome,
            "scope": payload.get("protocol_scope", "unknown"),
            "baseline_acc": (float(payload["baseline_accuracy"])
                             if payload.get("baseline_accuracy") is not None else None),
            "halt_reason": payload.get("halt_reason", ""),
            "C7": None, "C3": None, "C4": None,
            "cmp_C3_C2": None, "cmp_C3_C4": None, "cmp_C4_C2": None,
            "gate_passed": None, "probe_gate": None,
            "consistency_g": None,
        }
    conds = payload["stage_B_conditions"]
    cmps = payload["comparisons"]
    gate = payload.get("probe_gate") or {}
    return {
        "outcome": outcome,
        "scope": payload.get("protocol_scope", "unknown"),
        "baseline_acc": float(payload["baseline_accuracy"]),
        "halt_reason": "",
        "N_final": int(payload.get("N_final", -1)),
        "C7": cond_stats(conds["C7_Output_Bridge"]),
        "C3": cond_stats(conds["C3_Oracle_Selected"]),
        "C4": cond_stats(conds["C4_Random_Selected"]),
        "C2": cond_stats(conds["C2_Static_B_agg"]),
        "cmp_C3_C2": cmp_stats(cmps["C3_vs_C2"]),
        "cmp_C3_C4": cmp_stats(cmps["C3_vs_C4"]),
        "cmp_C4_C2": cmp_stats(cmps["C4_vs_C2"]),
        "gate_passed": (bool(gate["passed"]) if gate.get("passed") is not None else None),
        "probe_gate": gate,
        "consistency_g": payload.get("consistency_check_g"),
    }


def band_clearance(delta_m):
    cleared = [b for b in SENSITIVITY_BANDS if delta_m >= b]
    missed = [b for b in SENSITIVITY_BANDS if delta_m < b]
    return cleared, missed


def report(norm, branch_letter):
    bid, bname, text = branch_letter, BRANCH_NAMES[branch_letter], RULINGS[branch_letter]
    lines = []
    lines.append("=" * 80)
    lines.append("EXP070 DECISION-TREE RULING (protocol §8, pre-registered)")
    lines.append("=" * 80)
    lines.append(f"Run outcome : {norm['outcome']}")
    lines.append(f"Scope       : {norm['scope']}")
    if norm.get("baseline_acc") is not None:
        lines.append(f"Baseline acc: {norm['baseline_acc']*100:.2f}%")
    else:
        lines.append("Baseline acc: n/a (halted before baseline evaluation)")
    if norm.get("N_final", -1) >= 0:
        lines.append(f"N_final     : {norm['N_final']}")
    if norm.get("halt_reason"):
        lines.append(f"Halt reason : {norm['halt_reason']}")
    for role in ("C2", "C3", "C4", "C7"):
        s = norm.get(role)
        if s is not None:
            lines.append(f"{role}: ΔM(vs C1)={s['delta_m']*100:+.2f}pp  b={s['b']}  c={s['c']}  p={s['p']:.6f}")
    c = norm.get("cmp_C3_C2")
    if c is not None:
        lines.append(f"C3_vs_C2 (kill comparison): ΔM={c['delta_m']*100:+.2f}pp  "
                     f"b={c['b']}  c={c['c']}  p={c['exact_p']:.6f}")
        cleared, missed = band_clearance(c["delta_m"])
        lines.append("Sensitivity bands (+12/+16/+20pp): cleared "
                     + (", ".join(f"+{int(b*100)}pp" for b in cleared) or "none")
                     + "; below " + (", ".join(f"+{int(b*100)}pp" for b in missed) or "none"))
    g = norm.get("probe_gate")
    if g:
        lines.append(f"Probe-signal gate: passed={g.get('passed')}  path={g.get('path')}  "
                     f"r_pb={g.get('r_pb')}  p={g.get('r_pb_one_sided_p')}  "
                     f"H_sel={g.get('H_sel')}")
    cg = norm.get("consistency_g")
    if cg:
        lines.append(f"(g) C2 replicates EXP065 null: {cg.get('C2_replicates_EXP065_null')}; "
                     f"C7 rescues: {cg.get('C7_rescues')}; "
                     f"C2 discrepancy flag: {cg.get('C2_discrepancy_flag')}")
    lines.append("-" * 80)
    lines.append(f"BRANCH: ({bid}) {bname}")
    lines.append(text)
    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="EXP070 pre-registered decision-tree evaluator")
    ap.add_argument("results", nargs="?", default=None,
                    help="path to exp070_results.json (default: experiments/runs/EXP070_oracle_ceiling/exp070_results.json)")
    args = ap.parse_args()
    path = args.results or os.path.join("experiments", "runs",
                                         "EXP070_oracle_ceiling",
                                         "exp070_results.json")
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    norm = normalize_exp070(payload)
    branch = evaluate(norm)
    print(report(norm, branch))


if __name__ == "__main__":
    main()
