"""
EXP075 decision-tree evaluator (protocol §7, pre-registered, SIGNED).

Reads exp075_results.json and outputs the pre-registered ruling branch VERBATIM.
No new statistics are invented: McNemar exact p, (b, c), ΔM, the energy gate,
rank diagnostics, and halt flags are read from the artifact. Margin shifts are
never confirmatory (audit Finding 3 / O5) and are not consulted here.

Precedence (protocol §7.1):
    (a) energy-gate halt -> (b) headroom halt -> (c) invalid run ->
    (d) [supersedes (e)-(i)] -> (e)/(f)/(g) -> (h)/(i) conditional on (g).
The rank-guard halt (§3.1) is not lettered in §7.1 (it fires before any
condition runs); it is reported as branch (a') with the §3.1/§7.2 halt text.

Conservative readings (documented, mirroring run_exp075.py):
    - (f) is TERMINAL per §7.0 (the "single source of truth" canonical
      criterion): the exact-kill cell (C4 b=c=0, C3 valid, C2 null) returns
      "f" (H_sub FALSIFIED). (h)/(i) are supplementary localization NOTES
      in report() for the (f) region, not branch replacements.
    - (g) conditional partition: C5 significant positive -> (h) ("upgrades
      it toward (f)" -- unchanged); otherwise -> (i) ("neither (e) nor (f)
      fires" -- literally true for the (g) sub-case only).
    - (e) + C5-also-rescues: branch stays (e) ((h) is conditional on (f)/(g)
      only); the C5 rescue is an informational note, no branch change.

Usage:
    python evaluate_exp075.py [path/to/exp075_results.json]
"""

import os
import sys
import json
import argparse

HISTORICAL_BASELINES = {"EXP065": 0.6833, "EXP066": 0.5667}
# Artifact-verified (research_log.md spot-check); also carried in the results
# artifact under "historical_baselines" for the branch-(d) comparability rider.

RULINGS = {
    "a": ("Branch (a): energy gate failed (median e < 0.10). RULING: HALT -- "
          "uninformative causal test, informative localization measurement. The "
          "low e IS the localization evidence: the bridge's causal power lies "
          "almost entirely outside S. What is uninformative is specifically "
          "C4's causal test (a renormalized-noise injection cannot support a "
          "direction verdict). The e distribution is evidentially non-empty. "
          "Re-design required (not a re-run under EXP075)."),
    "a_rank": ("Branch (a') [spec §3.1, not lettered in §7.1]: rank guard "
          "failed (sigma_min/sigma_max <= 1e-6) -- S is degenerate. RULING: "
          "HALT -- a degenerate (effectively lower-dimensional) S would make "
          "the test uninformative, and silently proceeding would be "
          "p-hacking-adjacent. Reportable per §7.2; re-design required (not a "
          "re-run under EXP075)."),
    "b": ("Branch (b): headroom gate failed (baseline outside [40%, 70%]). "
          "RULING: HALT -- benchmark miscalibrated. Reportable; no conclusions."),
    "c": ("Branch (c): C3 positive control FAILED (bridge: ΔM <= 0 or p >= "
          "0.05). RULING: invalid run -- the load-bearing control did not "
          "replicate; NO conclusion about H_sub may be drawn. Diagnose (model "
          "hash, benchmark integrity, hook lifecycle) before any re-registration. "
          "Do not interpret C4/C5 in an invalid run."),
    "d": ("Branch (d): C2 RESCUES (ΔM > 0, p < 0.05) -- supersedes (e)-(i). "
          "RULING: boundary revision. The EXP065/066 static null failed to "
          "replicate. Report as a revision of the program's central boundary "
          "claim with full statistics, including the historical EXP065/066 "
          "baseline accuracy alongside this run's baseline accuracy. "
          "Comparability rider: the headroom band [40%,70%] is wide enough to "
          "admit incomparable runs -- if the baselines differ substantially, "
          "the 'boundary revision' reading is qualified accordingly (the "
          "numbers, not the adjective, carry the claim). The 'direction "
          "within S' interpretation is moot if the mean direction in S works."),
    "e": ("Branch (e): C4 ΔM > 0, p < 0.05 (C3 valid, energy gate passed). "
          "RULING: H_sub SUPPORTED -- strongest loop motivation. LICENSES: "
          "'for rescued items, S contains an item-specific direction, "
          "constructible with label information, that rescues at the decision "
          "endpoint; the EXP068 loop's per-instance search-within-S problem is "
          "non-vacuous in this oracle sense (EXP068's G1 candidates are "
          "aggregates of the same v_hat_k, hence elements of S by "
          "construction). Mechanism (relational vs. logit-steering) "
          "unidentified -- the energy gate guards null-interpretability only "
          "(§3.4). Label-free findability not established: contingent on "
          "EXP070's ceiling verdict and EXP068's own ρ-gate.' DOES NOT "
          "LICENSE: loop validation (no search was performed); that a "
          "label-free search can find such directions (EXP068's own question; "
          "contingent on EXP070's ceiling verdict and EXP068's ρ-gate); a "
          "single global rescuing direction in S; novelty claims (N1 holds); "
          "the identity of the best direction in S; any claim about other "
          "subspaces."),
    "f": ("Branch (f): C4 ΔM ≡ 0 (b = c = 0), C3 valid. RULING: H_sub "
          "FALSIFIED (kill). LICENSES: 'S, as constructed, is causally "
          "irrelevant as a search space; the EXP068 loop would be searching "
          "an empty room in this operationalization.' DOES NOT LICENSE: 'no "
          "subspace works' (only this S tested); 'the loop is dead in all "
          "forms' (a loop searching a different candidate family is a new "
          "pre-registration); any claim about S's geometric (non-causal) "
          "properties."),
    "g": ("Branch (g): C4 partial (b > 0 but p >= 0.05; or ΔM < 0). RULING: "
          "mixed -- neither support nor kill. Report exact (b, c, p, ΔM). No "
          "motivation claim, no kill claim."),
    "h": ("Branch (h): C5 RESCUES (ΔM > 0, p < 0.05) while C4 is (f)/(g). "
          "RULING: discriminant -- wrong room. The bridge's causal power is "
          "not in the contrast subspace. Strengthens (f)'s interpretation; if "
          "attached to (g), upgrades it toward (f). LICENSES: 'the bridge's "
          "causal power is not in the contrast subspace.'"),
    "i": ("Branch (i): C4 and C5 both null, C3 valid. RULING: non-localizable. "
          "The bridge's causal power requires components in both S and "
          "S^perp jointly (or neither separately at unit-norm). Report as a "
          "localization limit; neither (e) nor (f) fires."),
    "unclassified": ("No pre-registered branch matches this outcome. RULING: "
          "report raw statistics only; DO NOT interpret. (Fail-safe: the "
          "protocol's tree should be exhaustive; an unclassified outcome "
          "indicates a schema or logic error -- investigate.)"),
}

BRANCH_NAMES = {
    "a": "ENERGY_GATE_HALT",
    "a_rank": "RANK_GUARD_HALT",
    "b": "HEADROOM_HALT",
    "c": "INVALID_RUN",
    "d": "BOUNDARY_REVISION",
    "e": "HSUB_SUPPORTED",
    "f": "HSUB_FALSIFIED_KILL",
    "g": "MIXED",
    "h": "DISCRIMINANT_WRONG_ROOM",
    "i": "NON_LOCALIZABLE",
    "unclassified": "UNCLASSIFIED",
}


def sig_positive(s):
    return (s["delta_m"] > 0) and (s["p"] < 0.05)


def evaluate(norm):
    """Pure decision-tree function.

    norm keys: outcome, C2/C3/C4/C5 {delta_m,b,c,p}.
    Returns the branch letter ("a","a_rank","b".."i"/"unclassified").
    """
    try:
        outcome = norm.get("outcome", "COMPLETED")
        if outcome == "MALFORMED_PAYLOAD":
            return "unclassified"
        if outcome == "HALT_RANK":
            return "a_rank"
        if outcome == "HALT_ENERGY":
            return "a"
        if outcome == "HALT_HEADROOM":
            return "b"

        c3 = norm["C3"]
        if not sig_positive(c3):
            return "c"

        c2 = norm["C2"]
        if sig_positive(c2):
            return "d"   # supersedes (e)-(i)

        c4 = norm["C4"]
        if sig_positive(c4):
            return "e"
        if c4["b"] == 0 and c4["c"] == 0:
            return "f"   # F1: §7.0 canonical kill -- terminal; (h)/(i) are
                         # report-level supplementary notes, not replacements
        c5 = norm["C5"]
        if sig_positive(c5):
            return "h"   # "upgrades it toward (f)" -- the (g) sub-case
        return "i"        # "neither (e) nor (f) fires" -- literally true here
    except (KeyError, TypeError):
        return "unclassified"


def cond_stats(d):
    return {"delta_m": float(d["delta_m"]), "b": int(d["rescues_b"]),
            "c": int(d["corruptions_c"]), "p": float(d["exact_p"])}


def normalize_exp075(payload):
    # Halt payloads (rank / energy / headroom gates) carry no
    # stage_B_conditions: check `outcome` FIRST (M1 lesson from EXP067/070).
    outcome = payload.get("outcome", "COMPLETED")
    if outcome in ("HALT_RANK", "HALT_ENERGY", "HALT_HEADROOM"):
        # F8: halt payloads (save_halt) write diagnostics at TOP LEVEL:
        # e_median / e_distribution / e_sensitivity / energy_bar for
        # HALT_ENERGY and HALT_HEADROOM; rank_ratio / singular_values for
        # HALT_RANK. Rebuild the display dicts so report() surfaces the
        # values protocol §7.1(a) requires to be reported.
        energy_gate = payload.get("energy_gate")
        if energy_gate is None:
            eg = {}
            for _k in ("e_median", "e_distribution", "energy_bar"):
                if payload.get(_k) is not None:
                    eg[_k] = payload[_k]
            if payload.get("e_sensitivity") is not None:
                eg["sensitivity"] = payload["e_sensitivity"]
            if payload.get("e_median") is not None:
                eg["passed"] = bool(payload["e_median"] >= 0.10)
            energy_gate = eg or None
        subspace = payload.get("subspace")
        if subspace is None:
            sub = {}
            if payload.get("rank_ratio") is not None:
                sub["rank"] = None  # rank unknown; guard failed => < 5
                sub["rank_ratio_sigma_min_over_max"] = payload["rank_ratio"]
            if payload.get("singular_values") is not None:
                sub["singular_values"] = payload["singular_values"]
            subspace = sub or None
        return {
            "outcome": outcome,
            "scope": payload.get("protocol_scope", "unknown"),
            "baseline_acc": (float(payload["baseline_accuracy"])
                             if payload.get("baseline_accuracy") is not None else None),
            "halt_reason": payload.get("halt_reason", ""),
            "C2": None, "C3": None, "C4": None, "C5": None,
            "energy_gate": energy_gate,
            "subspace": subspace,
        }
    # F9: a malformed non-halt payload (missing/incomplete
    # stage_B_conditions) must normalize to the "unclassified" fail-safe,
    # not crash with KeyError. Loud-but-structured: evaluate() returns
    # "unclassified" and the ruling text says the schema is wrong.
    conds = payload.get("stage_B_conditions")
    required = ("C1_Unintervened_Baseline", "C2_Static_B_agg", "C3_Full_Bridge",
                "C4_Subspace_Bridge", "C5_Complement_Bridge",
                "C6_Static_B_perp", "C7_Static_B_wrong")
    if not isinstance(conds, dict) or not all(k in conds for k in required):
        return {
            "outcome": "MALFORMED_PAYLOAD",
            "scope": payload.get("protocol_scope", "unknown"),
            "baseline_acc": None,
            "halt_reason": ("malformed results payload: stage_B_conditions "
                            "missing or incomplete (expected the 7 condition "
                            "records); no branch may be ruled"),
            "C2": None, "C3": None, "C4": None, "C5": None,
            "energy_gate": payload.get("energy_gate"),
            "subspace": payload.get("subspace"),
        }
    return {
        "outcome": outcome,
        "scope": payload.get("protocol_scope", "unknown"),
        "baseline_acc": float(payload["baseline_accuracy"]),
        "halt_reason": "",
        "N": 60,
        "C1": cond_stats(conds["C1_Unintervened_Baseline"]),
        "C2": cond_stats(conds["C2_Static_B_agg"]),
        "C3": cond_stats(conds["C3_Full_Bridge"]),
        "C4": cond_stats(conds["C4_Subspace_Bridge"]),
        "C5": cond_stats(conds["C5_Complement_Bridge"]),
        "C6": cond_stats(conds["C6_Static_B_perp"]),
        "C7": cond_stats(conds["C7_Static_B_wrong"]),
        "kl_flags": {k: bool(v.get("kl_guardrail_exceeded", False))
                     for k, v in conds.items() if k != "C1_Unintervened_Baseline"},
        "energy_gate": payload.get("energy_gate"),
        "subspace": payload.get("subspace"),
        "historical_baselines": payload.get("historical_baselines", HISTORICAL_BASELINES),
        "pre_hash": payload.get("pre_hash"),
        "post_hash": payload.get("post_hash"),
    }


def report(norm, branch_letter):
    bid, bname, text = branch_letter, BRANCH_NAMES[branch_letter], RULINGS[branch_letter]
    lines = []
    lines.append("=" * 80)
    lines.append("EXP075 DECISION-TREE RULING (protocol §7, pre-registered)")
    lines.append("=" * 80)
    lines.append(f"Run outcome : {norm['outcome']}")
    lines.append(f"Scope       : {norm['scope']}")
    if norm.get("baseline_acc") is not None:
        lines.append(f"Baseline acc: {norm['baseline_acc']*100:.2f}%")
    else:
        lines.append("Baseline acc: n/a (halted before baseline evaluation)")
    if norm.get("halt_reason"):
        lines.append(f"Halt reason : {norm['halt_reason']}")
    sub = norm.get("subspace")
    if sub:
        lines.append(f"Subspace S  : rank {sub.get('rank')}; "
                     f"sigma_min/sigma_max = {sub.get('rank_ratio_sigma_min_over_max')}")
    eg = norm.get("energy_gate")
    if eg:
        sens = eg.get("sensitivity", {})
        lines.append(f"Energy gate : e_median = {eg.get('e_median')}; bar = {eg.get('energy_bar')}; "
                     f"passed = {eg.get('passed')}; sensitivity "
                     + ", ".join(f"{k}: {'PASS' if v else 'FAIL'}" for k, v in sens.items()))
    for role in ("C1", "C2", "C3", "C4", "C5", "C6", "C7"):
        s = norm.get(role)
        if s is not None:
            lines.append(f"{role}: ΔM(vs C1)={s['delta_m']*100:+.2f}pp  b={s['b']}  c={s['c']}  p={s['p']:.6f}")
    kf = norm.get("kl_flags")
    if kf:
        over = [k for k, v in kf.items() if v]
        lines.append("KL guardrail (0.50, exploratory): " +
                     ("exceeded by " + ", ".join(over) if over else "no condition exceeded"))
    hb = norm.get("historical_baselines")
    if hb and bid == "d":
        lines.append("Comparability rider (M3): historical baselines "
                     f"EXP065={hb.get('EXP065', 0)*100:.2f}% / EXP066={hb.get('EXP066', 0)*100:.2f}% "
                     f"vs this run {norm.get('baseline_acc', 0)*100:.2f}% -- the numbers, not the "
                     "adjective, carry the claim.")
    # Informational note (no branch change): C5 rescues alongside (e).
    if bid == "e" and norm.get("C5") is not None and sig_positive(norm["C5"]):
        lines.append("NOTE (informational; branch unchanged): C5 also rescued significantly. "
                     "Branch (h) is conditional on (f)/(g) only -- it does not fire alongside (e).")
    # F1: (h)/(i) are supplementary localization notes for the (f) region --
    # the branch is (f) either way (§7.0 canonical kill).
    if bid == "f":
        c5 = norm.get("C5")
        if c5 is not None and sig_positive(c5):
            lines.append("SUPPLEMENTARY LOCALIZATION NOTE (report-level; branch unchanged): "
                         "the (h) content applies -- the bridge's causal power is not in "
                         "the contrast subspace ('wrong room'); this strengthens (f)'s "
                         "interpretation.")
        else:
            lines.append("SUPPLEMENTARY LOCALIZATION NOTE (report-level; branch unchanged): "
                         "C5 did not rescue significantly either -- neither S nor S^perp "
                         "alone rescued at unit-norm (localization limit; (f) still fired).")
    lines.append("-" * 80)
    lines.append(f"BRANCH: ({bid}) {bname}")
    lines.append(text)
    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="EXP075 pre-registered decision-tree evaluator")
    ap.add_argument("results", nargs="?", default=None,
                    help="path to exp075_results.json (default: experiments/runs/EXP075_subspace_bridge/exp075_results.json)")
    args = ap.parse_args()
    path = args.results or os.path.join("experiments", "runs",
                                         "EXP075_subspace_bridge",
                                         "exp075_results.json")
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    norm = normalize_exp075(payload)
    branch = evaluate(norm)
    print(report(norm, branch))


if __name__ == "__main__":
    main()
