"""
EXP067 decision-tree evaluator (protocol §7.1, pre-registered).

Reads a results.json and outputs the pre-registered ruling branch VERBATIM.
No new statistics are invented: McNemar exact p, (b, c), ΔM, headroom and halt
flags are read from the artifact. Margin shifts are never confirmatory
(audit Finding 3) and are not consulted here.

Usage:
    python evaluate_exp067.py [path/to/exp067_results.json]
    python evaluate_exp067.py --historical path/to/exp065_results.json
    python evaluate_exp067.py --historical path/to/exp066_replication_results.json

The --historical mode maps the EXP065/066 schemas onto the C3/C4 roles for a
dry-run sanity check of this evaluator. Historical runs used the UNSOUND
operator, so their ruling is illustrative, not a protocol outcome.

M1: halt payloads (HALT_STAGE_A / HALT_HEADROOM) are handled without crashing:
outcome is checked first, missing stage_B_conditions/baseline_accuracy tolerated,
and the pre-registered §7.2 ruling prints verbatim.

M2 scope gate: for real runs whose protocol_scope starts with "OUT-OF-SCOPE",
the evaluator prints raw statistics plus "NO PROTOCOL RULING -- OUT-OF-SCOPE
PILOT" INSTEAD of branch text, so no ruling can be quoted without its qualifier.
"""

import os
import sys
import json
import argparse

# ----------------------------------------------------------------------------
# Pre-registered rulings, protocol §7.1 (single source of truth: §7.0 box)
# ----------------------------------------------------------------------------
RULINGS = {
    "a": ("STAGE_A_HALT",
          "Branch (a): Stage A gate halted (no head with g_h > 0, or rank/spectral "
          "guard aborted). RULING: A-anchor/A-uniform rejected on support data. H1 is "
          "untestable under this operationalization — neither falsified nor confirmed. "
          "I1 (the boundary claim) stands unchallenged by this experiment."),
    "headroom": ("HEADROOM_HALT",
          "Protocol §7.2: headroom gate halted (baseline outside [40%, 70%]). RULING: "
          "reportable outcome — benchmark miscalibrated. Any recalibration requires a "
          "new pre-registration; no tweak-and-rerun under the EXP067 label."),
    "b": ("INVALID_RUN",
          "Branch (b): C4 positive control FAILED (bridge did not replicate: ΔM <= 0 "
          "or p >= 0.05). RULING: invalid run. Setup broken or benchmark drifted; NO "
          "conclusion about H1 may be drawn. Diagnose (model hash, benchmark integrity, "
          "hook lifecycle) before any re-registration. Do not interpret C3 in an invalid run."),
    "d": ("H1_FALSIFIED",
          "Branch (d) — CANONICAL: C3 yielded ΔM = 0 (McNemar p >= 0.05, b = 0) while C4 "
          "yielded ΔM > 0 (p < 0.05, >= 5 rescues). RULING: H1 is FALSIFIED. The "
          "representational–causal dissociation is a structural property of the "
          "architecture at this scale, not an artifact of alignment-operator quality; "
          "the program pivots to characterizing WHERE the causal chain breaks (QK "
          "routing vs OV transport vs MLP readout) rather than HOW to align better."),
    "e": ("H1_CONFIRMED",
          "Branch (e): C3 yielded ΔM > 0 AND McNemar p < 0.05 (with C4 valid). RULING: "
          "H1 confirmed — the boundary claim reopens for revision. §1.1 scope applies: "
          "a positive C3 is a better-executed N0 mechanism (CAA-equivalent), not a "
          "novelty result."),
    "c1": ("MIXED_C1",
          "Branch (c1): C3 mixed — b > 0 but p >= 0.05. RULING: H1 NOT confirmed. "
          "Report as weak/partial evidence with exact statistics (b, c, p, ΔM); no "
          "success claim."),
    "c2": ("MIXED_C2",
          "Branch (c2): C3 mixed — ΔM < 0. RULING: report as a NEGATIVE result per Law #8 "
          "with full statistics. H1 not confirmed."),
    "c3": ("MIXED_C3",
          "Branch (c3): C3 mixed — b > 0 and c > 0. RULING: report net ΔM with both "
          "counts; H1 NOT confirmed (success requires ΔM > 0, p < 0.05)."),
    "unclassified": ("UNCLASSIFIED",
          "No pre-registered branch matches this outcome. RULING: report raw statistics "
          "only; DO NOT interpret. (Fail-safe: the protocol's tree should be exhaustive; "
          "an unclassified outcome indicates a schema or logic error — investigate.)"),
}


def evaluate(norm):
    """Pure decision-tree function. `norm` keys: outcome, C3 {delta_m,b,c,p}, C4 {...}."""
    outcome = norm.get("outcome", "COMPLETED")

    if outcome == "HALT_STAGE_A":
        return RULINGS["a"]
    if outcome == "HALT_HEADROOM":
        return RULINGS["headroom"]

    c3, c4 = norm["C3"], norm["C4"]
    c4_valid = (c4["delta_m"] > 0) and (c4["p"] < 0.05) and (c4["b"] >= 5)
    if not ((c4["delta_m"] > 0) and (c4["p"] < 0.05)):
        return RULINGS["b"]

    # Canonical (d) requires ΔM == 0 EXACTLY with b = 0 per the protocol's
    # parenthetical (b==0 and ΔM==0 jointly imply c==0). b==0 & p>=0.05 alone is
    # insufficient: b=0,c=2 gives ΔM<0, which is branch (c2), not (d).
    c3_null = (c3["b"] == 0) and (c3["c"] == 0)
    c3_success = (c3["delta_m"] > 0) and (c3["p"] < 0.05)
    if c3_null and c4_valid:
        return RULINGS["d"]
    if c3_success and c4_valid:
        return RULINGS["e"]
    if (c3["b"] > 0) and (c3["p"] >= 0.05):
        return RULINGS["c1"]
    if c3["delta_m"] < 0:
        return RULINGS["c2"]
    if (c3["b"] > 0) and (c3["c"] > 0):
        return RULINGS["c3"]
    return RULINGS["unclassified"]


def cond_stats(d):
    return {"delta_m": float(d["delta_m"]), "b": int(d["rescues_b"]),
            "c": int(d["corruptions_c"]), "p": float(d["exact_p"])}


def normalize_exp067(payload):
    # M1 fix: check `outcome` FIRST. Halt payloads (Stage A and headroom) carry
    # no `stage_B_conditions`, and Stage A halts additionally lack
    # `baseline_accuracy`. A halt is a first-class reportable outcome
    # (protocol §7.2); the evaluator must not crash on precisely the outcomes
    # the pre-registration was designed to produce.
    outcome = payload.get("outcome", "COMPLETED")
    if outcome in ("HALT_STAGE_A", "HALT_HEADROOM"):
        return {
            "outcome": outcome,
            "scope": payload.get("protocol_scope", "unknown"),
            "baseline_acc": (float(payload["baseline_accuracy"])
                             if payload.get("baseline_accuracy") is not None else None),
            "halt_reason": payload.get("halt_reason", ""),
            "C3": None,
            "C4": None,
        }
    conds = payload["stage_B_conditions"]
    return {
        "outcome": outcome,
        "scope": payload.get("protocol_scope", "unknown"),
        "baseline_acc": float(payload["baseline_accuracy"]),
        "halt_reason": "",
        "C3": cond_stats(conds["C3_Aligned_Dynamic_Basis"]),
        "C4": cond_stats(conds["C4_Output_Bridge"]),
    }


HISTORICAL_MAP = {
    # historical condition name -> decision-tree role
    "Aligned_Dynamic_Basis": "C3",
    "Same_Layer_Output_Bridge": "C4",
}


def normalize_historical(payload):
    """Map EXP065/066 schemas onto C3/C4 roles. Illustrative only: those runs used
    the unsound (rank-2, cross-space) operator, so no protocol ruling applies."""
    if "stage_B_conditions" in payload:
        conds = payload["stage_B_conditions"]
    elif "stage_B_confirmatory_results" in payload:
        conds = payload["stage_B_confirmatory_results"]
    else:
        raise ValueError("unrecognized historical schema")
    roles = {}
    for hname, role in HISTORICAL_MAP.items():
        if hname not in conds:
            raise ValueError(f"historical condition {hname} missing")
        roles[role] = cond_stats(conds[hname])
    return {
        "outcome": "COMPLETED",
        "scope": "HISTORICAL (pre-EXP067 protocol; unsound operator — illustrative only)",
        "baseline_acc": float(payload["baseline_accuracy"]),
        "C3": roles["C3"],
        "C4": roles["C4"],
    }


def report(norm, branch):
    bid, text = branch
    lines = []
    lines.append("=" * 80)
    lines.append("EXP067 DECISION-TREE RULING (protocol §7.1, pre-registered)")
    lines.append("=" * 80)
    lines.append(f"Run outcome : {norm['outcome']}")
    lines.append(f"Scope       : {norm['scope']}")
    if norm.get("baseline_acc") is not None:
        lines.append(f"Baseline acc: {norm['baseline_acc']*100:.2f}%")
    else:
        lines.append("Baseline acc: n/a (halted before baseline evaluation)")
    if norm.get("halt_reason"):
        lines.append(f"Halt reason : {norm['halt_reason']}")
    for role in ("C3", "C4"):
        s = norm.get(role)
        if s is not None:
            lines.append(f"{role}: ΔM={s['delta_m']*100:+.2f}pp  b={s['b']}  c={s['c']}  p={s['p']:.6f}")
    lines.append("-" * 80)
    lines.append(f"BRANCH: {bid}")
    lines.append(text)
    lines.append("=" * 80)
    return "\n".join(lines)


def report_out_of_scope(norm):
    """M2 scope gate: for OUT-OF-SCOPE runs, raw statistics only -- NO branch
    text, so no ruling can be quoted without its qualifier."""
    lines = []
    lines.append("=" * 80)
    lines.append("EXP067 EVALUATOR -- OUT-OF-PROTOCOL-SCOPE RUN")
    lines.append("=" * 80)
    lines.append("NO PROTOCOL RULING -- OUT-OF-SCOPE PILOT")
    lines.append("The signed protocol pre-registers pythia-410m only. This run used an")
    lines.append("out-of-scope configuration; NO pre-registered branch applies to it.")
    lines.append("Statistics below are reported raw and MUST NOT be quoted as a ruling.")
    lines.append("-" * 80)
    lines.append(f"Run outcome : {norm['outcome']}")
    lines.append(f"Scope       : {norm['scope']}")
    if norm.get("baseline_acc") is not None:
        lines.append(f"Baseline acc: {norm['baseline_acc']*100:.2f}%")
    else:
        lines.append("Baseline acc: n/a (halted before baseline evaluation)")
    if norm.get("halt_reason"):
        lines.append(f"Halt reason : {norm['halt_reason']}")
    for role in ("C3", "C4"):
        s = norm.get(role)
        if s is not None:
            lines.append(f"{role}: ΔM={s['delta_m']*100:+.2f}pp  b={s['b']}  c={s['c']}  p={s['p']:.6f}")
    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="EXP067 pre-registered decision-tree evaluator")
    ap.add_argument("results", nargs="?", default=None,
                    help="path to exp067_results.json (default: experiments/runs/EXP067_qkov_subspace_procrustes/exp067_results.json)")
    ap.add_argument("--historical", default=None,
                    help="dry-run mode: map an EXP065/066 results.json onto C3/C4 roles")
    args = ap.parse_args()

    if args.historical:
        with open(args.historical, encoding="utf-8") as f:
            payload = json.load(f)
        print(f"[dry-run] historical mapping used: {HISTORICAL_MAP}")
        norm = normalize_historical(payload)
    else:
        path = args.results or os.path.join("experiments", "runs",
                                             "EXP067_qkov_subspace_procrustes",
                                             "exp067_results.json")
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
        norm = normalize_exp067(payload)
        # M2 scope gate (real runs only; --historical dry-runs are explicitly
        # illustrative and keep their full ruling text).
        if str(norm["scope"]).startswith("OUT-OF-SCOPE"):
            print(report_out_of_scope(norm))
            return

    branch = evaluate(norm)
    print(report(norm, branch))


if __name__ == "__main__":
    main()
