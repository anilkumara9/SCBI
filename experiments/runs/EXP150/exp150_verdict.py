"""EXP150 verdict — fills the registered §4 decision table (sole binding
verdict machinery per Fix E4) from the per-item records.

Reads exp150_per_item.jsonl + exp150_run_summary.json (guards). Writes the
§4 table outcome into the summary. Run only after the run script reports
PROCEED_TO_VERDICT (or HELD/RUN-INVALID — then the table is moot and the
script records that plainly).

Statistics: paired McNemar on (S,C) and (S,B) correctness pairs per level;
one-sided exact binomial p (H1: S>C / S>B); Wald 95% CIs per the S7-1 §2.2
convention (SE = sqrt((d - delta^2)/n)); theta = delta_T3 - delta_T2 with
SE(theta) = sqrt(SE_T3^2 + SE_T2^2).
"""
import json
import math
import os
import sys

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
JSONL = os.path.join(RUN_DIR, "exp150_per_item.jsonl")
SUMMARY = os.path.join(RUN_DIR, "exp150_run_summary.json")
LEVELS = ["transitive-2hop", "transitive-3hop"]
Z95 = 1.96


def binom_upper_tail(n, k):
    """P(X >= k), X ~ Bin(n, 0.5); exact via math.comb. n=0 -> 1.0."""
    if n == 0:
        return 1.0
    return sum(math.comb(n, j) for j in range(k, n + 1)) / 2.0 ** n


def paired_stats(pairs):
    """pairs: list of (s_correct, c_correct). Returns McNemar/Wald stats."""
    b = sum(1 for s, c in pairs if s == 1 and c == 0)
    c = sum(1 for s, c in pairs if s == 0 and c == 1)
    n = len(pairs)
    delta = (b - c) / n
    d = (b + c) / n
    se = math.sqrt(max(d - delta ** 2, 0.0) / n)
    lo, hi = delta - Z95 * se, delta + Z95 * se
    p_one = binom_upper_tail(b + c, b)  # H1: S>C (first > second)
    return {"b": b, "c": c, "n": n, "delta": delta, "d": d, "se": se,
            "ci95": [lo, hi], "p_one_sided": p_one}


def main():
    with open(SUMMARY) as f:
        summary = json.load(f)

    run_outcome = summary.get("outcome")
    if run_outcome != "PROCEED_TO_VERDICT":
        summary["verdict"] = {
            "table": "§4 (binding)",
            "outcome": run_outcome,
            "reason": (f"run stopped before the verdict phase: "
                       f"{summary.get('reason', run_outcome)} — the §4 "
                       f"decision table is moot; no verdict is licensed."),
        }
        with open(SUMMARY, "w") as f:
            json.dump(summary, f, indent=1)
            f.write("\n")
        print(f"verdict: {run_outcome} (pre-verdict stop) — "
              f"{summary['verdict']['reason']}")
        return

    recs = [json.loads(l) for l in open(JSONL) if l.strip()]
    by_level_arm = {}
    for r in recs:
        by_level_arm.setdefault(r["stratum"], {}).setdefault(
            r["arm"], {})[r["item_id"]] = r["correct"]

    sc, sb = {}, {}
    for lvl in LEVELS:
        arms = by_level_arm[lvl]
        ids = set(arms["S"]) & set(arms["C"]) & set(arms["B"])
        assert len(ids) == 190, f"{lvl}: {len(ids)} complete triples"
        sc[lvl] = paired_stats([(arms["S"][i], arms["C"][i]) for i in ids])
        sb[lvl] = paired_stats([(arms["S"][i], arms["B"][i]) for i in ids])

    d2, d3 = sc["transitive-2hop"], sc["transitive-3hop"]
    theta = d3["delta"] - d2["delta"]
    se_theta = math.sqrt(d2["se"] ** 2 + d3["se"] ** 2)
    ci_theta = [theta - Z95 * se_theta, theta + Z95 * se_theta]

    g = summary["guards"]
    guards_pass = bool(g.get("ds_stratified_gate") and
                       g.get("e_discipline_pass") and
                       g.get("f_compute_delivered") and
                       g.get("fp_budget_matched_per_level"))

    ci_above_0 = ci_theta[0] > 0
    ci_below_eq_0 = ci_theta[1] <= 0
    t3_sc_p = d3["p_one_sided"]
    t3_sb_p = sb["transitive-3hop"]["p_one_sided"]

    kill_fires = ci_below_eq_0 and guards_pass
    cont_fires = ci_above_0 and (t3_sc_p < 0.05)
    pivot_fires = kill_fires and (t3_sb_p < 0.05)

    # Precedence: RUN-INVALID > HELD > KILL > CONTINUE (run script already
    # settled RUN-INVALID/HELD pre-verdict stops; here: KILL vs CONTINUE vs
    # HELD per the §4 rows).
    if cont_fires and kill_fires:
        # logically impossible (CI cannot be both entirely >0 and ≤0);
        # guard against arithmetic pathology -> HELD.
        verdict, reading = "HELD", ("pathology guard: CI both above 0 and "
                                    "<= 0 — HELD, reported for audit")
    elif cont_fires:
        verdict = "CONTINUE"
        reading = ("Dose-response supported on transitive strata: the "
                   "discipline gain grows with reasoning depth; the "
                   "capability entry gains a (transitive-scoped) depth axis")
    elif kill_fires:
        verdict = "KILL"
        reading = ("Dose-response dead on transitive strata: the gain does "
                   "not grow with hops there — it is pooled/headroom-driven. "
                   "EXP148's CONTINUE stands as a pooled effect, not a "
                   "depth effect")
    else:
        verdict = "HELD"
        reading = ("Inconclusive — licenses nothing, kills nothing "
                   "(CI too wide, or a per-level guard (d_s)/(f') tripped)")

    summary["verdict"] = {
        "table": "§4 (binding; sole verdict machinery per Fix E4)",
        "outcome": verdict,
        "reading": reading,
        "theta_delta_T3_minus_T2": round(theta, 4),
        "se_theta": round(se_theta, 4),
        "ci95_theta": [round(ci_theta[0], 4), round(ci_theta[1], 4)],
        "per_level_S_vs_C": {
            lvl: {k: (round(v, 4) if isinstance(v, float) else v)
                  for k, v in sc[lvl].items()
                  if k != "ci95"} | {"ci95": [round(sc[lvl]["ci95"][0], 4),
                                              round(sc[lvl]["ci95"][1], 4)]}
            for lvl in LEVELS},
        "per_level_S_vs_B": {
            lvl: {"b": sb[lvl]["b"], "c": sb[lvl]["c"], "n": sb[lvl]["n"],
                  "delta": round(sb[lvl]["delta"], 4),
                  "p_one_sided_S_gt_B": round(sb[lvl]["p_one_sided"], 6)}
            for lvl in LEVELS},
        "guards_for_table": {
            "ds_stratified_gate": g.get("ds_stratified_gate"),
            "e_discipline_pass": g.get("e_discipline_pass"),
            "f_compute_delivered": g.get("f_compute_delivered"),
            "fp_budget_matched_per_level": g.get(
                "fp_budget_matched_per_level"),
            "all_pass": guards_pass},
        "pivot": {"fires": pivot_fires,
                  "t3_S_vs_B_p_one_sided": round(t3_sb_p, 6),
                  "reading": ("Test-time compute helps at depth but "
                              "discipline doesn't — pivot to "
                              "test-time-compute scaling") if pivot_fires
                  else None},
        "mandatory_caveats": [
            "S vs B: direct answering beat WRITE/READ in EXP148 "
            "(net -0.2500); prompting discipline, not autonomous steering.",
            "Single model (Pythia-410m), single bench family.",
            "No consciousness / superhuman claim.",
        ],
    }
    with open(SUMMARY, "w") as f:
        json.dump(summary, f, indent=1)
        f.write("\n")

    print(f"verdict: {verdict}")
    print(f"  theta (dT3-dT2) = {theta:+.4f}, SE = {se_theta:.4f}, "
          f"95% CI [{ci_theta[0]:+.4f}, {ci_theta[1]:+.4f}]")
    print(f"  T2 S-C: delta={d2['delta']:+.4f} CI[{d2['ci95'][0]:+.4f},"
          f"{d2['ci95'][1]:+.4f}] p1={d2['p_one_sided']:.4g} (b={d2['b']},c={d2['c']})")
    print(f"  T3 S-C: delta={d3['delta']:+.4f} CI[{d3['ci95'][0]:+.4f},"
          f"{d3['ci95'][1]:+.4f}] p1={d3['p_one_sided']:.4g} (b={d3['b']},c={d3['c']})")
    print(f"  T3 S-B one-sided p = {t3_sb_p:.4g} -> "
          f"PIVOT {'FIRES' if pivot_fires else 'no'}")
    print(f"  guards for table: {guards_pass}")
    print(f"  reading: {reading}")


if __name__ == "__main__":
    main()
