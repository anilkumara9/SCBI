#!/usr/bin/env python3
"""
Law #14-adjacent unit tests for the EXP077 pre-registered evaluator.

Tests the pure decision logic (Holm step-down, radial shape classifier,
5-branch precedence) -- not the runner's model code.
"""

import io
import json
import math
import os
import sys
import tempfile
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evaluate_exp077 as ev

try:
    import run_exp077 as runner  # module-level is side-effect-free (constants + defs)
    HAS_RUNNER = True
except Exception:
    HAS_RUNNER = False

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (f" -- {detail}" if detail and not cond else ""))


def base_norm():
    """A minimal, fully-null norm dict (flat zero, COMPLETED)."""
    return {
        "outcome": "COMPLETED",
        "baseline_accuracy": 0.6833,
        "angular": {"b": 0, "c": 0, "delta_m": 0.0, "p": 1.0},
        "control": {"b": 0, "c": 0, "delta_m": 0.0, "p": 1.0},
        "offset": {"b": 0, "c": 0, "delta_m": 0.0, "p": 1.0},
        "replication": {"b": 0, "c": 0, "delta_m": 0.0, "p": 1.0},
        "radial": {"alphas": [0.25, 0.50, 1.00, 2.00],
                   "p_values": [1.0, 1.0, 1.0, 1.0],
                   "delta_ms": [0.0, 0.0, 0.0, 0.0]},
    }


# ---------------- Holm step-down (protocol §6, §8) ----------------
check("holm: first-only rejected",
      ev.holm_reject([0.0078, 0.02, 0.03, 0.5]) == {0})
check("holm: all rejected at strong signal",
      ev.holm_reject([0.0078, 0.0078, 0.0078, 0.0078]) == {0, 1, 2, 3})
check("holm: strict inequality at the boundary (0.0125 not < 0.0125)",
      ev.holm_reject([0.0125, 0.5, 0.5, 0.5]) == set())
check("holm: 7-0 split (p=0.0156) does not reject -- the A-headroom caveat (§6)",
      ev.holm_reject([0.0156, 0.5, 0.5, 0.5]) == set())
check("holm: empty input -> empty set", ev.holm_reject([]) == set())

# ---------------- radial_shape (§6, §8) ----------------
A = [0.25, 0.50, 1.00, 2.00]
shape, S_H = ev.radial_shape(A, [0.0078, 0.5, 0.5, 0.5], [0.1, 0, 0, 0])
check("radial: singleton {0.25} is non-upper", shape == "non-upper" and S_H == [0.25])
shape, S_H = ev.radial_shape(A, [0.5, 0.5, 0.0078, 0.0078], [0, 0, 0.1, 0.1])
check("radial: {1.0, 2.0} is upper", shape == "upper" and S_H == [1.0, 2.0])
shape, S_H = ev.radial_shape(A, [0.0078, 0.0078, 0.5, 0.5], [0.1, 0.1, 0, 0])
check("radial: {0.25, 0.5} is non-upper", shape == "non-upper" and S_H == [0.25, 0.5])
shape, S_H = ev.radial_shape(A, [0.0078, 0.5, 0.5, 0.5], [-0.1, 0, 0, 0])
check("radial: Holm-rejected but delta_m<0 is ignored -> empty",
      shape == "empty" and S_H == [])
shape, S_H = ev.radial_shape(A, [0.5, 0.5, 0.5, 0.5], [0, 0, 0, 0])
check("radial: all null -> empty", shape == "empty" and S_H == [])
shape, S_H = ev.radial_shape(A, [0.5, 0.5, 0.5, 0.0078], [0, 0, 0, 0.1])
check("radial: singleton {2.0} is upper", shape == "upper" and S_H == [2.0])
shape, S_H = ev.radial_shape(A, [0.0078] * 4, [0.1] * 4)
check("radial: all alphas positive -> upper", shape == "upper" and S_H == A)

# ---------------- discordant_stats (§3.6, MAJOR-2 regression) ----------------
# The registered comparisons are cone-vs-LINE and cone-vs-CONTROL discordant
# counts -- (b,c) = (ΣK(1−L), ΣL(1−K)). These tests pin the formula so the
# inverted cone-vs-baseline construction cannot return silently.
if HAS_RUNNER:
    ds = runner.discordant_stats
    K = [1, 1, 1, 0, 0]
    L = [0, 1, 0, 1, 0]
    r = ds(K, L)
    check("discordant: (b,c) = (ΣK(1−L), ΣL(1−K))", r["b"] == 2 and r["c"] == 1,
          f"b={r['b']}, c={r['c']}")
    check("discordant: delta_m = (b-c)/n", abs(r["delta_m"] - 1/5) < 1e-12)
    r = ds([0, 0, 0], [0, 0, 0])
    check("discordant: b=c=0 -> p=1.0 [M5.1]", r["b"] == 0 and r["c"] == 0 and r["p"] == 1.0)
    r = ds([1]*9 + [0]*51, [0]*60)
    check("discordant: 9-0 split -> b=9, c=0, p=0.0039",
          r["b"] == 9 and r["c"] == 0 and abs(r["p"] - 0.00390625) < 1e-9, f"p={r['p']}")
    # The inversion bug fed correctness lists (cone vs baseline): discordant
    # counts on indicator lists are NOT reproducible from correctness pairs --
    # a 9-0 rescue-vs-baseline split is a different comparison.
    r = ds([1, 1, 0, 0], [1, 0, 1, 0])
    check("discordant: ignores concordant pairs", r["b"] == 1 and r["c"] == 1,
          f"b={r['b']}, c={r['c']}")
else:
    check("discordant: runner import available (skipped -- torch/transformers missing)", False)

# ---------------- branch (d) INVALID ----------------
for halt in ["HALT_HEADROOM", "HALT_BRIDGE", "HALT_CONTINUITY", "HALT_ANTICHEAT"]:
    n = {"outcome": halt}
    br, trig = ev.classify(n)
    check(f"(d): {halt} -> INVALID", br == "d" and halt in trig, trig)

# ---------------- unclassified ----------------
br, trig = ev.classify({"outcome": "MALFORMED_PAYLOAD"})
check("unclassified: MALFORMED_PAYLOAD", br == "unclassified")
try:
    ev.classify({"outcome": "COMPLETED"})  # missing required fields downstream
    check("classify: incomplete COMPLETED payload raises (missing keys)", False)
except KeyError:
    check("classify: incomplete COMPLETED payload raises (missing keys)", True)
br, trig = ev.classify(base_norm())
check("(c): flat-zero base -> NEITHER", br == "c" and trig.startswith("flat-zero"), trig)

# ---------------- branch (r) REPLICATION FAILURE ----------------
n = base_norm()
n["replication"] = {"b": 8, "c": 0, "delta_m": 8/60, "p": 0.0078}
br, trig = ev.classify(n)
check("(r): C3 rescue vs C1 -> REPLICATION FAILURE", br == "r", trig)
n = base_norm()
n["replication"] = {"b": 0, "c": 8, "delta_m": -8/60, "p": 0.0078}
br, trig = ev.classify(n)
check("(r): C3 corruption vs C1 -> REPLICATION FAILURE", br == "r", trig)
n = base_norm()
n["replication"] = {"b": 8, "c": 0, "delta_m": 8/60, "p": 0.05}  # strict boundary
br, trig = ev.classify(n)
check("(r): p=0.05 exactly is NOT (r) [M5.1 strict]", br == "c", f"got {br}")
n = base_norm()
n["replication"] = {"b": 8, "c": 0, "delta_m": 8/60, "p": 0.0078}
n["angular"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
n["control"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
br, trig = ev.classify(n)
check("precedence: (r) outranks (a)", br == "r", f"got {br}")

# ---------------- branch (a) CONE-WINS (§3.6 semantics) ----------------
# NOTE (MAJOR-2 repair): "angular" is the cone-vs-LINE discordant endpoint and
# "control" the cone-vs-CONTROL discordant endpoint (spec §3.6) -- NOT
# cone-vs-baseline / control-vs-baseline. The tests below assert the registered
# comparisons.
n = base_norm()
n["angular"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
n["control"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
br, trig = ev.classify(n)
check("(a)(i): cone beats line AND cone beats control -> CONE-WINS", br == "a", trig)

n = base_norm()
n["angular"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
n["control"] = {"b": 0, "c": 0, "delta_m": 0.0, "p": 0.5}
br, trig = ev.classify(n)
check("(c): attempts-alone (cone beats line, cone-vs-control failed) -> NEITHER",
      br == "c" and trig.startswith("attempts-alone"), trig)

n = base_norm()
n["radial"] = {"alphas": A, "p_values": [0.0078, 0.5, 0.5, 0.5], "delta_ms": [0.1, 0, 0, 0]}
br, trig = ev.classify(n)
check("(a)(ii): non-upper radial set {0.25} -> CONE-WINS", br == "a", trig)

n = base_norm()
n["radial"] = {"alphas": A, "p_values": [0.0078, 0.5, 0.5, 0.0078], "delta_ms": [0.1, 0, 0, 0.1]}
br, trig = ev.classify(n)
check("(a)(ii): non-upper radial set {0.25, 2.0} -> CONE-WINS", br == "a", trig)

n = base_norm()
n["offset"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
br, trig = ev.classify(n)
check("(a)(iii): offset sig positive -> CONE-WINS", br == "a", trig)

n = base_norm()
n["angular"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.05}  # strict boundary
n["control"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
br, trig = ev.classify(n)
check("(a)(i): angular p=0.05 exactly is null [M5.1 strict] -> not (a)", br == "c", f"got {br}")

# ---------------- branch (b) LINE-WINS (§3.6 semantics) ----------------
n = base_norm()
n["angular"] = {"b": 0, "c": 9, "delta_m": -9/60, "p": 0.004}
br, trig = ev.classify(n)
check("(b)(i): line beats cone -> LINE-WINS", br == "b", trig)

n = base_norm()
n["radial"] = {"alphas": A, "p_values": [0.5, 0.5, 0.0078, 0.0078], "delta_ms": [0, 0, 0.1, 0.1]}
br, trig = ev.classify(n)
check("(b)(ii): upper radial set {1.0, 2.0} -> LINE-WINS", br == "b", trig)

n = base_norm()
n["radial"] = {"alphas": A, "p_values": [0.5, 0.5, 0.5, 0.0078], "delta_ms": [0, 0, 0, 0.1]}
br, trig = ev.classify(n)
check("(b)(ii): singleton upper set {2.0} -> LINE-WINS", br == "b", trig)

n = base_norm()
n["angular"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
n["control"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
n["radial"] = {"alphas": A, "p_values": [0.5, 0.5, 0.0078, 0.0078], "delta_ms": [0, 0, 0.1, 0.1]}
br, trig = ev.classify(n)
check("precedence: (a)(i) outranks (b)(ii)", br == "a", f"got {br}")

# ---------------- report() rendering ----------------
n = base_norm()
n["angular"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
n["control"] = {"b": 9, "c": 0, "delta_m": 9/60, "p": 0.004}
br, trig = ev.classify(n)
buf = io.StringIO()
with redirect_stdout(buf):
    ev.report(n, br, trig)
txt = buf.getvalue()
check("report: contains 'Branch: (a) CONE-WINS'", "Branch: (a) CONE-WINS" in txt)
check("report: contains LICENSE (a)", "LICENSE (a)" in txt)

buf = io.StringIO()
with redirect_stdout(buf):
    ev.report(base_norm(), "c", "flat-zero")
check("report: (c) license names killed/surviving hypotheses",
      "killed" in buf.getvalue() and "survive" in buf.getvalue())

# ---------------- load_results() ----------------
good = base_norm()
good["extra_field"] = "ignored"
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(good, f)
    path = f.name
norm = ev.load_results(path)
os.unlink(path)
check("load_results: complete payload normalizes", norm["outcome"] == "COMPLETED" and norm["angular"]["b"] == 0)

bad = {"outcome": "COMPLETED", "angular": {}}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(bad, f)
    path = f.name
norm = ev.load_results(path)
os.unlink(path)
br, _ = ev.classify(norm)
check("load_results: missing keys -> MALFORMED_PAYLOAD -> unclassified",
      norm["outcome"] == "MALFORMED_PAYLOAD" and br == "unclassified")

halted = {"outcome": "HALT_BRIDGE"}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(halted, f)
    path = f.name
norm = ev.load_results(path)
os.unlink(path)
br, _ = ev.classify(norm)
check("load_results: halt payload -> (d)", norm["outcome"] == "HALT_BRIDGE" and br == "d")

print()
print(f"{len(PASS)} passed, {len(FAIL)} failed")
sys.exit(1 if FAIL else 0)
