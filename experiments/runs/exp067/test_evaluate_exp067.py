"""Regression tests for evaluate_exp067.py (Law #14: tooling must not break on
pre-registered outcomes).

Covers:
  1. HALT_STAGE_A payload (no stage_B_conditions, no baseline_accuracy) -> branch (a), no crash.
  2. HALT_HEADROOM payload (has baseline_accuracy, no stage_B_conditions) -> headroom branch, no crash.
  3. OUT-OF-SCOPE completed run -> raw stats + NO PROTOCOL RULING banner, no branch text.
  4. IN-SCOPE completed run -> full branch ruling (gate does not over-fire).
  5. --historical dry-runs on EXP065/066 artifacts -> H1_FALSIFIED, artifact-exact numbers.

Run:  python test_evaluate_exp067.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.join(HERE, "evaluate_exp067.py")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def make_halt_payload(outcome, extra, scope="IN-SCOPE (pythia-410m, layer 20)"):
    """Mimics save_halt() in run_exp067.py exactly (key set)."""
    payload = {
        "experiment": "EXP067",
        "model": "EleutherAI/pythia-410m",
        "protocol_scope": scope,
        "outcome": outcome,
        "halt_reason": "synthetic test halt",
        "pre_hash": "abc",
        "post_hash": "abc",
        "target_layer": 20,
        "hidden_dim": 1024,
        "num_heads": 16,
        "alpha": 0.50,
        "stage_A_heads": [],
        "env_manifest": {},
    }
    payload.update(extra)
    return payload


def run_eval_on_dict(payload):
    path = os.path.join(HERE, "_test_payload_tmp.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    try:
        r = subprocess.run([sys.executable, EVAL, path],
                           capture_output=True, text=True, timeout=60)
    finally:
        if os.path.exists(path):
            os.remove(path)
    return r


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" -- {detail}" if detail and not cond else ""))
    return cond


def main():
    ok = True

    # 1. HALT_STAGE_A: must not crash; must print branch (a) verbatim.
    r = run_eval_on_dict(make_halt_payload("HALT_STAGE_A", {}))
    ok &= check("HALT_STAGE_A: no crash", r.returncode == 0, r.stderr[-500:])
    ok &= check("HALT_STAGE_A: branch (a)", "BRANCH: STAGE_A_HALT" in r.stdout)
    ok &= check("HALT_STAGE_A: baseline n/a", "Baseline acc: n/a" in r.stdout)

    # 2. HALT_HEADROOM: must not crash; must print headroom branch.
    r = run_eval_on_dict(make_halt_payload("HALT_HEADROOM", {"baseline_accuracy": 0.95}))
    ok &= check("HALT_HEADROOM: no crash", r.returncode == 0, r.stderr[-500:])
    ok &= check("HALT_HEADROOM: headroom branch", "BRANCH: HEADROOM_HALT" in r.stdout)
    ok &= check("HALT_HEADROOM: baseline shown", "Baseline acc: 95.00%" in r.stdout)

    # 3. OUT-OF-SCOPE completed run: banner, no branch text.
    oos = {
        "experiment": "EXP067",
        "model": "EleutherAI/pythia-160m",
        "protocol_scope": "OUT-OF-SCOPE (pre-registration fixes pythia-410m)",
        "outcome": "COMPLETED",
        "baseline_accuracy": 0.60,
        "stage_B_conditions": {
            "C3_Aligned_Dynamic_Basis": {"delta_m": 0.0, "rescues_b": 0,
                                        "corruptions_c": 0, "exact_p": 1.0},
            "C4_Output_Bridge": {"delta_m": 0.1333, "rescues_b": 8,
                                 "corruptions_c": 0, "exact_p": 0.0078},
        },
    }
    r = run_eval_on_dict(oos)
    ok &= check("OOS: no crash", r.returncode == 0, r.stderr[-500:])
    ok &= check("OOS: banner present",
                "NO PROTOCOL RULING -- OUT-OF-SCOPE PILOT" in r.stdout)
    ok &= check("OOS: no branch text", "BRANCH:" not in r.stdout)
    ok &= check("OOS: raw stats present", "b=8" in r.stdout)

    # 4. IN-SCOPE completed run: full ruling (gate must not over-fire).
    ins = dict(oos)
    ins["protocol_scope"] = "IN-SCOPE (pythia-410m, layer 20)"
    r = run_eval_on_dict(ins)
    ok &= check("IN-SCOPE: no crash", r.returncode == 0, r.stderr[-500:])
    ok &= check("IN-SCOPE: branch (d)", "BRANCH: H1_FALSIFIED" in r.stdout)

    # 5. Historical dry-runs: artifact-exact H1_FALSIFIED.
    hist = [
        ("experiments/runs/EXP065_coordinate_alignment/exp065_results.json",
         {"b4": 10, "p4": 0.0020}),
        ("experiments/runs/EXP066_pythia410m_replication/exp066_replication_results.json",
         {"b4": 8, "p4": 0.0078}),
    ]
    for rel, exp in hist:
        p = os.path.join(REPO, rel)
        r = subprocess.run([sys.executable, EVAL, "--historical", p],
                           capture_output=True, text=True, timeout=60)
        ok &= check(f"historical {os.path.basename(p)}: no crash",
                    r.returncode == 0, r.stderr[-500:])
        ok &= check(f"historical {os.path.basename(p)}: H1_FALSIFIED",
                    "BRANCH: H1_FALSIFIED" in r.stdout)
        ok &= check(f"historical {os.path.basename(p)}: C4 b={exp['b4']}",
                    f"b={exp['b4']}" in r.stdout)

    print("=" * 60)
    print("ALL TESTS PASSED" if ok else "SOME TESTS FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
