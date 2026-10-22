#!/usr/bin/env python3
"""EXP139 Stage-2 bundle structural tests — CPU only.

NO GPU contact. NO model/weight downloads. NO network.
Covers: config parsing, hash/pin checks, protocol-fidelity checks.
Run: python tests/test_bundle_cpu.py   (from the bundle directory)
"""
import json
import math
import os
import re
import sys

BUNDLE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BUNDLE_DIR)
import exp139_stage2_lib as L  # noqa: E402

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"
results = []


def check(name, cond, detail=""):
    results.append((name, PASS if cond else FAIL, detail))
    print("[%s] %s %s" % (PASS if cond else FAIL, name, detail))


def skip(name, detail=""):
    results.append((name, SKIP, detail))
    print("[SKIP] %s %s" % (name, detail))


PREREG = os.path.expanduser(
    "~/workspace/SCBI/research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md")

# ---- 1. bench reconstruction matches the signed pin (pure Python) ----
bench = L.build_bench()
check("bench_len_60", len(bench) == 60, "got %d" % len(bench))
check("bench_sha256_pin", L.bench_sha256(bench) == L.BENCH_PIN,
      L.bench_sha256(bench)[:16] + "...")

# ---- 2. pinned constants match the signed pre-registration text ----
# Build-machine provenance check: SKIPs gracefully on Kaggle where the
# workspace tree is absent (verified at build time, by the apparatus review).
if os.path.exists(PREREG):
    prereg_text = open(PREREG).read()
    for label, val in [("BACKBONE_PIN", L.BACKBONE_PIN),
                       ("BENCH_PIN", L.BENCH_PIN),
                       ("HF_REVISION", L.HF_REVISION)]:
        check("pin_in_prereg_%s" % label, val in prereg_text)
    check("model_id_in_prereg", L.MODEL_ID in prereg_text)
    check("t8_in_prereg", re.search(r"T\s*=\s*8", prereg_text) is not None)
else:
    for name in ["pin_in_prereg_BACKBONE_PIN", "pin_in_prereg_BENCH_PIN",
                 "pin_in_prereg_HF_REVISION", "model_id_in_prereg",
                 "t8_in_prereg"]:
        skip(name, "pre-reg text absent on this machine (build-time provenance)")
check("d_hid_1024", L.D_HID == 1024)

# ---- 3. protocol constants ----
check("n_items_60", L.N_ITEMS == 60)
check("t_steps_8", L.T_STEPS == 8)
check("r_passes_480", L.R_PASSES == 60 * 8)
check("expected_forwards_540_documented",
      L.EXPECTED_FORWARDS == 540 and "520" in open(
          os.path.join(BUNDLE_DIR, "run_stage2.py")).read(),
      "AMBIGUITY-1: 540 executed vs pre-reg 520, documented in executor")
check("bars", L.BAR_DELTA_PP == 0.08 and L.BAR_LCI == 0.05 and L.WILSON_Z == 1.96)

# ---- 4. Newcombe implementation vs hand-computed reference ----
# n=60, b=10, c=2 → dhat=8/60; Wilson(10/60)=(0.093139,0.280315);
# Wilson(2/60)=(0.009184,0.113644); L=0.024446; U=0.249518 (hand-derived)
nc = L.newcombe_paired(10, 2, 60)
check("newcombe_dhat", abs(nc["dhat"] - 8 / 60) < 1e-12, "%.6f" % nc["dhat"])
check("newcombe_L", abs(nc["L"] - 0.024446) < 1e-4, "%.6f" % nc["L"])
check("newcombe_U", abs(nc["U"] - 0.249518) < 1e-4, "%.6f" % nc["U"])
check("newcombe_bar_not_met", not (nc["dhat"] >= 0.08 and nc["L"] > 0.05))
# edge: b=c=0
nc0 = L.newcombe_paired(0, 0, 60)
check("newcombe_zero_zero", nc0["dhat"] == 0.0 and nc0["L"] < 0.0,
      "L=%.4f" % nc0["L"])
# binding bar met case: b=14, c=1 → dhat=13/60=0.2167
nc1 = L.newcombe_paired(14, 1, 60)
check("newcombe_bar_met_case", nc1["dhat"] >= 0.08 and nc1["L"] > 0.05,
      "dhat=%.4f L=%.4f" % (nc1["dhat"], nc1["L"]))

# ---- 5. Wilson interval properties ----
lb, ub = L.wilson_interval(0.5, 60)
check("wilson_symmetric", abs((lb + ub) / 2 - 0.5) < 1e-9)
check("wilson_clipped", 0.0 <= lb and ub <= 1.0)

# ---- 6. McNemar exact (doubling method): b=10,c=2 → 2*(79/4096)=0.038574 ----
p = L.mcnemar_exact_twosided(10, 2)
check("mcnemar_value", abs(p - 0.038574) < 1e-4, "%.6f" % p)
check("mcnemar_degenerate", L.mcnemar_exact_twosided(0, 0) == 1.0)

# ---- 7. trajectory diagnostic ----
check("traj_strict", L.trajectory_strictly_decreasing([3.0, 2.0, 1.0]))
check("traj_nonmonotone", not L.trajectory_strictly_decreasing([3.0, 2.5, 2.6]))
check("traj_tie_not_strict", not L.trajectory_strictly_decreasing([3.0, 2.0, 2.0]))

# ---- 8. verdict-tree reporter ----
r = L.stage2_branch_report(0.10, 0.06, 0.15, True)
check("verdict_continue",
      any(n == "CONTINUE" for n, _ in r["branches"]) and not r["conflicts"])
r = L.stage2_branch_report(0.10, 0.06, 0.15, False)
check("verdict_pivot", any(n == "PIVOT" for n, _ in r["branches"]))
r = L.stage2_branch_report(0.03, 0.01, 0.05, True)
check("verdict_held_c", any(n == "HELD(c)" for n, _ in r["branches"]))
r = L.stage2_branch_report(0.03, 0.01, 0.05, False)
check("verdict_held_d", any(n == "HELD(d)" for n, _ in r["branches"]))
r = L.stage2_branch_report(-0.02, -0.05, 0.01, True)
check("verdict_held_f_adjudicated",
      len(r["conflicts"]) == 0
      and any(n == "HELD(f)" for n, _ in r["branches"])
      and not any("KILL" in n for n, _ in r["branches"]),
      "LOG-4896: §6 governs; §0/§5 KILL lines superseded")
r = L.stage2_branch_report(0.0, -0.03, 0.03, False)
check("verdict_held_f_adjudicated_traj_fail",
      len(r["conflicts"]) == 0
      and any(n == "HELD(f)" for n, _ in r["branches"])
      and not any("KILL" in n for n, _ in r["branches"]),
      "HELD(f) governs for ΔM≤0 regardless of trajectory")

# ---- 9. committed baseline data file integrity ----
data = json.load(open(os.path.join(BUNDLE_DIR, "data",
                                   "committed_baseline_view0.json")))
check("data_n60", data["n_items"] == 60 and len(data["items"]) == 60)
check("data_ids_match_bench",
      [it["id"] for it in data["items"]] == [b["id"] for b in bench])
check("data_yhat_ints",
      all(isinstance(it["committed_yhat"], int) for it in data["items"]))
src = None
EXP135_SRC = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP135_eval/out/exp135_records.json")
if os.path.exists(EXP135_SRC):
    src = json.load(open(EXP135_SRC))
    src_yhat = [src["cache_unintervened"][i][0]["yhat"] for i in range(60)]
    check("data_matches_committed_source",
          [it["committed_yhat"] for it in data["items"]] == src_yhat)
else:
    skip("data_matches_committed_source",
         "EXP135 source absent on this machine (build-time provenance)")

# ---- 10. executor protocol-fidelity (static scan; executor not executed) ----
exe = open(os.path.join(BUNDLE_DIR, "run_stage2.py")).read()
for pat in [r"\.backward\s*\(", r"torch\.optim", r"\.train\s*\(",
            r"requires_grad_\(\s*True", r"zero_grad\s*\("]:
    check("executor_no_%s" % pat[:12], re.search(pat, exe) is None)
for token in ["torch.no_grad()", "model.eval()", "local_files_only=True",
              "BACKBONE_PIN", "final_layer_norm", "EXPECTED_FORWARDS",
              "newcombe_paired", "stage2_branch_report", "T_STEPS",
              "stage2_run_log.txt", "stage2_records.json", "stage2_verdict.json"]:
    check("executor_has_%s" % token.replace(".", "_")[:28], token in exe)
check("executor_imports_lib", "import exp139_stage2_lib" in exe)
check("executor_no_hardcoded_T8",
      "range(8)" not in exe and "T = 8" not in exe,
      "T comes from lib.T_STEPS")
check("executor_exit44", "sys.exit(44)" in exe)

# ---- 10b. F2: backbone post-hash mismatch must trip RUN-INVALID (Law #6) ----
post_seg = exe[exe.index("post_hash = sha256_state_dict(model)"):
               exe.index("post_hash = sha256_state_dict(model)") + 500]
check("f2_posthash_mismatch_trips_runinvalid", "run_invalid" in post_seg,
      "mutated-weights run must exit 44, never exit 0")
check("f2_backbone_post_persisted", exe.count('"backbone_post"') >= 2,
      "persisted in stage2_records.json and stage2_verdict.json")

# ---- 10c. F1 regression: decode must operate on the full (50304,) readout vector ----
# readout_yhat(h) returns the full logit vector; the old bug applied [0] at the
# two call sites, reducing it to a 0-dim scalar so yhat_of crashed on the first
# decode. This test exercises the executor's EXACT yhat_of call path against a
# stubbed 50304-length vector (no torch needed).
import ast as _ast
_yhat_src = _ast.get_source_segment(
    exe, next(n for n in _ast.walk(_ast.parse(exe))
              if isinstance(n, _ast.FunctionDef) and n.name == "yhat_of"))
_ns = {}
exec(compile(_yhat_src, "run_stage2.py", "exec"), _ns)
_yhat_of = _ns["yhat_of"]
_VOCAB = 50304
_stub = [0.0] * _VOCAB             # stub mimicking the (50304,) readout vector
_tA, _tC = 1234, 5678
_stub[_tA], _stub[_tC] = 2.0, 1.0
check("f1_decode_operates_on_vector",
      _yhat_of(_stub, _tA, _tC) == _tA,
      "yhat_of indexes the full 50304-vector by token id")
_stub[_tC] = 3.0
check("f1_decode_foil_path",
      _yhat_of(_stub, _tA, _tC) == _tC,
      "foil branch of the same call path")
check("f1_no_scalar_reduction_at_callsites",
      "readout_yhat(traj[L.T_STEPS])[0]" not in exe
      and "readout_yhat(traj[t])[0]" not in exe,
      "executor must not reduce the readout vector with [0]")


def _old_bug_crashes():
    reduced = _stub[0]             # what the old [0] slip produced: a scalar
    try:
        _yhat_of(reduced, _tA, _tC)
    except TypeError:
        return True               # scalar is not subscriptable -> crash, as on torch
    return False
check("f1_old_bug_would_have_crashed", _old_bug_crashes(),
      "proves this regression test catches the F1 defect class")

# ---- 11. requirements parse ----
req = open(os.path.join(BUNDLE_DIR, "requirements.txt")).read()
check("req_transformers_pinned", "transformers==5.17.0" in req)
check("req_torch_cuda", "cu128" in req or "cu12" in req)
check("req_no_local_paths", "file://" not in req and "/home/" not in req)

# ---- 12. lib has no torch/GPU/network imports ----
lib_src = open(os.path.join(BUNDLE_DIR, "exp139_stage2_lib.py")).read()
check("lib_no_torch", "import torch" not in lib_src)
check("lib_no_network", "urllib" not in lib_src and "requests" not in lib_src
      and "huggingface_hub" not in lib_src)

n_fail = sum(1 for _, s, _ in results if s == FAIL)
n_skip = sum(1 for _, s, _ in results if s == SKIP)
print("\n%d/%d tests passed, %d skipped" % (len(results) - n_fail - n_skip,
                                           len(results), n_skip))
sys.exit(1 if n_fail else 0)
