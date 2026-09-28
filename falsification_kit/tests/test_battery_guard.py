"""Decodability Gap falsification kit — F1 guard tests (LOG-4501).

Regression tests for the LOG-4500 review finding F1: battery.py used to
silently emit KILL (step 10) on an empty population when input records
lacked `correct_rank`. It must now HALT (non-zero exit, no verdict) instead.

Run:  python tests/test_battery_guard.py     (from the kit root)
      python -m pytest tests/                (if pytest is installed)
"""
import json
import os
import subprocess
import sys
import tempfile

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []


def check(name, cond, detail=""):
    results.append({"test": name, "pass": bool(cond), "detail": detail})
    print(("PASS" if cond else "FAIL"), name, detail, flush=True)
    if not cond:
        raise SystemExit("UNIT TEST FAILED: %s — HALT" % name)


def make_bare_records(n, with_rank):
    """Well-formed bare records like the LOG-4500 reviewer's empirical probe:
    8-candidate logit vectors, token ids, correct/foil/top1 indices — with
    or without the required `correct_rank` field."""
    recs = []
    for i in range(n):
        rec = {
            "item_id": i,
            "candidate_logits": [5.0 - j * 0.5 for j in range(8)],
            "candidate_token_ids": [1000 + j for j in range(8)],
            "correct_idx": 3,
            "foil_idx": 5,
            "top1_idx": 0,
        }
        if with_rank:
            rec["correct_rank"] = 4  # failed item, rank within pop band
        recs.append(rec)
    return recs


def run_battery(records):
    with tempfile.TemporaryDirectory() as td:
        rec_path = os.path.join(td, "records.json")
        out_path = os.path.join(td, "out", "battery.json")
        with open(rec_path, "w") as f:
            json.dump(records, f)
        proc = subprocess.run(
            [sys.executable, os.path.join(KIT_ROOT, "battery.py"),
             "--records", rec_path, "--out", out_path],
            cwd=KIT_ROOT, capture_output=True, text=True)
        return proc


# F1: 60 well-formed bare records WITHOUT correct_rank must HALT —
# never silently emit KILL step 10.
proc = run_battery(make_bare_records(60, with_rank=False))
combined = proc.stdout + proc.stderr
check("(F1) bare records w/o correct_rank -> non-zero exit",
      proc.returncode != 0, "returncode=%s" % proc.returncode)
check("(F1) bare records w/o correct_rank -> HALT message",
      "HALT" in combined and "correct_rank" in combined)
check("(F1) bare records w/o correct_rank -> NO verdict emitted",
      "BATTERY VERDICT" not in proc.stdout)

# Positive control: the same records WITH correct_rank run to a verdict.
proc = run_battery(make_bare_records(60, with_rank=True))
check("(F1-pos) records WITH correct_rank -> clean exit",
      proc.returncode == 0, "returncode=%s" % proc.returncode)
check("(F1-pos) records WITH correct_rank -> verdict emitted",
      "BATTERY VERDICT" in proc.stdout)

print("\nALL %d F1 GUARD TESTS PASSED" % len(results), flush=True)
