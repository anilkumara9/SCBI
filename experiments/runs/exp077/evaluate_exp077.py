#!/usr/bin/env python3
"""
EXP077 branch evaluator -- pure, deterministic, no model needed.

Applies the pre-registered 5-branch decision tree (protocol §8) to
exp077_results.json. Branch precedence (protocol §8):

    (d) INVALID  >  (r) BOUNDARY-NULL REPLICATION FAILURE
    >  (a) CONE-WINS  >  (b) LINE-WINS  >  (c) NEITHER

All sub-evidence uses Holm-adjusted p-values across the four alpha tests
(protocol §6, §8). A radial test counts as positive only if its
Holm-adjusted decision is significant AND delta_m > 0; an "upper set" is
{alpha in S_H : alpha >= min(S_H)} with exact float keys.

Usage: python3 evaluate_exp077.py <path-to-exp077_results.json>
"""

import argparse
import json
import math
import sys

P_PRIMARY = 0.05
ALPHAS = [0.25, 0.50, 1.00, 2.00]

HALT_OUTCOMES = {"HALT_HEADROOM", "HALT_BRIDGE", "HALT_CONTINUITY", "HALT_ANTICHEAT"}

BRANCH_NAMES = {
    "d": "INVALID",
    "r": "BOUNDARY-NULL REPLICATION FAILURE",
    "a": "CONE-WINS",
    "b": "LINE-WINS",
    "c": "NEITHER",
    "unclassified": "UNCLASSIFIED",
}


def isclose(a, b):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-12)


def holm_reject(p_values, alpha=P_PRIMARY):
    """Holm step-down rejection set (strict: reject iff p < alpha/(m-rank)).

    p_values: list of floats in a fixed order; returns set of rejected indices.
    """
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    rejected = set()
    for rank, i in enumerate(order):
        if p_values[i] < alpha / (m - rank):
            rejected.add(i)
        else:
            break
    return rejected


def radial_shape(alphas, p_values, delta_ms, alpha=P_PRIMARY):
    """Classify the Holm-significant positive radial set (§6, §8).

    Returns (shape, S_H) with shape in {"empty", "upper", "non-upper"}.
    A test is positive iff Holm-rejected AND delta_m > 0.
    S_H is an upper set iff every alpha >= min(S_H) is in S_H (exact float
    comparison, no tolerance).
    """
    rejected = holm_reject(p_values, alpha)
    S_H = sorted([alphas[i] for i in rejected if delta_ms[i] > 0])
    if not S_H:
        return "empty", []
    amin = min(S_H)
    if all(any(isclose(a, s) for s in S_H) for a in alphas if a >= amin - 1e-12):
        return "upper", S_H
    return "non-upper", S_H


def _ang(p, b, c, dm):
    """Angular-endpoint predicates (§8): strict p < 0.05 (M5.1)."""
    return {"sig_pos": bool(p < P_PRIMARY and b > c),
            "sig_neg": bool(p < P_PRIMARY and c > b),
            "sig_any": bool(p < P_PRIMARY and b != c),
            "null": not bool(p < P_PRIMARY and b != c)}


def classify(norm):
    """Apply the §8 tree. Returns (branch, trigger_detail)."""
    outcome = norm.get("outcome", "COMPLETED")

    # (d) INVALID -- any gate fired.
    if outcome in HALT_OUTCOMES:
        return "d", f"gate fired: {outcome}"
    if outcome == "MALFORMED_PAYLOAD":
        return "unclassified", "payload missing required fields"
    if outcome != "COMPLETED":
        return "unclassified", f"unexpected outcome value: {outcome!r}"

    # (r) REPLICATION FAILURE -- rescue or corruption at alpha=0.50 (§8,
    # M5.1 boundary: strict p < 0.05).
    rep = norm["replication"]
    if rep["p"] < P_PRIMARY and rep["delta_m"] != 0:
        kind = "rescue" if rep["delta_m"] > 0 else "corruption"
        return "r", f"C3 vs C1 significant ({kind}): b={rep['b']}, c={rep['c']}, p={rep['p']}"

    # (a) CONE-WINS -- any one of the three triggers.
    ang = _ang(norm["angular"]["p"], norm["angular"]["b"],
               norm["angular"]["c"], norm["angular"]["delta_m"])
    ctrl = _ang(norm["control"]["p"], norm["control"]["b"],
                norm["control"]["c"], norm["control"]["delta_m"])
    rad = norm["radial"]
    shape, S_H = radial_shape(rad["alphas"], rad["p_values"], rad["delta_ms"])
    off = norm["offset"]
    if ang["sig_pos"] and ctrl["sig_pos"]:
        return "a", (f"angular (cone vs line, §3.6): delta_m={norm['angular']['delta_m']*100:+.2f}pp "
                     f"(b={norm['angular']['b']}, c={norm['angular']['c']}, p={norm['angular']['p']:.6f}) "
                     f"+ control (cone vs control, §3.6) sig positive "
                     f"(b={norm['control']['b']}, c={norm['control']['c']}, p={norm['control']['p']:.6f})")
    if shape == "non-upper":
        return "a", f"radial: S_H={S_H} is a non-upper set"
    if off["p"] < P_PRIMARY and off["delta_m"] > 0:
        return "a", (f"affine: offset delta_m={off['delta_m']*100:+.2f}pp "
                     f"(b={off['b']}, c={off['c']}, p={off['p']:.6f})")

    # (b) LINE-WINS.
    if ang["sig_neg"]:
        return "b", (f"angular (cone vs line, §3.6): line beats cone "
                     f"(b={norm['angular']['b']}, c={norm['angular']['c']}, p={norm['angular']['p']:.6f})")
    if shape == "upper":
        return "b", f"radial-upper: S_H={S_H} is a non-empty upper set"

    # (c) NEITHER -- residual.
    if ang["sig_pos"]:
        return "c", ("attempts-alone: angular (cone vs line, §3.6) significant but the "
                     "cone-vs-control conjunct failed -- geometric signal without "
                     "cone-vs-control specificity")
    return "c", "flat-zero: no significant positive geometric signal"


def report(norm, branch, trigger):
    """Print the pre-registered ruling. Returns the branch letter."""
    lines = []
    lines.append("=" * 80)
    lines.append("EXP077 RULING (pre-registered decision tree, protocol §8)")
    lines.append("=" * 80)
    lines.append(f"Branch: ({branch}) {BRANCH_NAMES[branch]}")
    lines.append(f"Trigger: {trigger}")
    lines.append("")
    lines.append(f"Outcome: {norm.get('outcome')}")
    lines.append(f"Baseline accuracy: {norm.get('baseline_accuracy')}")
    rad = norm["radial"]
    shape, S_H = radial_shape(rad["alphas"], rad["p_values"], rad["delta_ms"])
    lines.append("Radial family (Holm-adjusted, alpha=0.05):")
    rej = holm_reject(rad["p_values"])
    for i, a in enumerate(rad["alphas"]):
        lines.append(f"  alpha={a}: delta_m={rad['delta_ms'][i]*100:+.2f}pp, "
                     f"p={rad['p_values'][i]:.6f} "
                     f"{'REJECTED' if i in rej else 'not rejected'}")
    lines.append(f"  S_H={S_H}  shape={shape}")
    ang = norm["angular"]; ctrl = norm["control"]
    lines.append(f"Angular endpoint (cone vs line, §3.6): b={ang['b']}, c={ang['c']}, "
                 f"delta_m={ang['delta_m']*100:+.2f}pp, p={ang['p']:.6f}")
    lines.append(f"Control endpoint (cone vs control, §3.6): b={ctrl['b']}, c={ctrl['c']}, "
                 f"delta_m={ctrl['delta_m']*100:+.2f}pp, p={ctrl['p']:.6f}")
    off = norm["offset"]
    lines.append(f"Offset endpoint: b={off['b']}, c={off['c']}, "
                 f"delta_m={off['delta_m']*100:+.2f}pp, p={off['p']:.6f}")
    rep = norm["replication"]
    lines.append(f"Replication C3 vs C1: b={rep['b']}, c={rep['c']}, "
                 f"delta_m={rep['delta_m']*100:+.2f}pp, p={rep['p']:.6f}")
    lines.append("")
    lines.append(LICENSE_TEXT[branch])
    lines.append("=" * 80)
    text = "\n".join(lines)
    print(text, flush=True)
    return branch


LICENSE_TEXT = {
    "d": ("LICENSE (d) INVALID: no claim about geometry or about the v_hat/alpha=0.50 "
          "null may be made from this run. The halt report is the outcome."),
    "r": ("LICENSE (r) REPLICATION FAILURE: the boundary null (v_hat @ alpha=0.50) does "
          "NOT replicate; the flat-zero at alpha=0.50 was itself atypical. "
          "Re-scope under a new pre-registration before any cone-vs-line claim. "
          "The (r) branch does not itself resolve cone-vs-line."),
    "a": ("LICENSE (a) CONE-WINS: the cone geometry or offset direction produced a "
          "Holm-significant causal rescue; the blanket I1 null is withdrawn in favor of "
          "a geometry-conditional claim. Scope: the tested rho=30deg unconditional "
          "cone (or the alpha=1.0 offset direction) at pythia-410m/layer-20 only."),
    "b": ("LICENSE (b) LINE-WINS: angularly, the rescue is confined to the line "
          "(cone corrupts) or the peaked alpha-curve favors the line over the cone; "
          "the I1 line interpretation is strengthened. The rho=30deg unconditional "
          "cone hypothesis is killed; other radii/gated variants survive (§11/P5 residual)."),
    "c": ("LICENSE (c) NEITHER: the rho=30deg unconditional cone and alpha=1.0 offset "
          "hypotheses are killed at pythia-410m/layer-20; other radii, gated, and "
          "conditional (concept-projection) variants survive (§11/P5 residual)."),
    "unclassified": ("NO LICENSE: malformed payload -- no ruling may be stated."),
}


def load_results(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if raw.get("outcome") in HALT_OUTCOMES:
        return {"outcome": raw["outcome"]}
    required = ["outcome", "angular", "control", "offset", "replication", "radial",
                "baseline_accuracy"]
    missing = [k for k in required if k not in raw]
    if missing:
        return {"outcome": "MALFORMED_PAYLOAD", "missing": missing}
    # The evaluator needs only the decision-relevant fields; it normalizes to a
    # minimal dict so malformed-but-complete payloads evaluate deterministically.
    return {
        "outcome": raw["outcome"],
        "baseline_accuracy": raw["baseline_accuracy"],
        "angular": raw["angular"],
        "control": raw["control"],
        "offset": raw["offset"],
        "replication": raw["replication"],
        "radial": raw["radial"],
    }


def main():
    ap = argparse.ArgumentParser(description="EXP077 pre-registered branch evaluator")
    ap.add_argument("results_json", help="path to exp077_results.json")
    args = ap.parse_args()
    norm = load_results(args.results_json)
    branch, trigger = classify(norm)
    report(norm, branch, trigger)


if __name__ == "__main__":
    main()
