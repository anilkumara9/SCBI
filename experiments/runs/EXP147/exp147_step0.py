"""EXP147 Step 0 — model load + guards (a), (b), (c), (h).

Guards per the signed S7-1 plan §5.4. Order: (b) revision, (a) pre-hash,
(h) throughput probe, (c) bench pin. If (h) projects > 72h -> INCONCLUSIVE.
$0 CPU. No bench forwards.
"""
import hashlib
import json
import os
import sys
import time

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(RUN_DIR, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))
from reference_implementation import bench_sha256  # noqa: E402 (canonical pin fn)

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "EleutherAI/pythia-410m"
EXPECTED_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "2b055b53127a241b72338a82373c3efc7b666256e25d8c584d45989278c14dcf"
BENCH_PATH = os.path.expanduser(
    "~/workspace/SCBI/research/analysis_plans/S7-1_BENCH_2026-10-05.json")

STEP0_JSON = os.path.join(RUN_DIR, "exp147_step0_2026-10-05.json")
LOG_TXT = os.path.join(RUN_DIR, "exp147_step0_2026-10-05.log")


def log(msg):
    line = "[step0] %s" % msg
    print(line, flush=True)
    with open(LOG_TXT, "a") as f:
        f.write(line + "\n")


def sha256_state_dict(model):
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu()
        if t.dtype != torch.float32:
            t = t.float()
        h.update(t.numpy().tobytes())
    return h.hexdigest()


def main():
    rec = {"guards": {}}
    torch.manual_seed(147001)

    # ---- (b) model revision: resolve programmatically from the HF cache ----
    snap_dir = os.path.expanduser(
        "~/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots")
    revs = sorted(os.listdir(snap_dir))
    assert len(revs) == 1, f"expected 1 cached snapshot, got {revs}"
    actual_rev = revs[0]
    assert len(actual_rev) == 40 and all(c in "0123456789abcdef"
                                        for c in actual_rev)
    rec["model_revision_actual"] = actual_rev
    rec["model_revision_expected"] = EXPECTED_REVISION
    rec["guards"]["b_revision_match"] = (actual_rev == EXPECTED_REVISION)
    log(f"(b) revision actual={actual_rev} expected={EXPECTED_REVISION} "
        f"match={rec['guards']['b_revision_match']}")
    if not rec["guards"]["b_revision_match"]:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "guard (b): revision mismatch"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: guard (b)")
        sys.exit(2)

    # ---- load ----
    log("loading tokenizer + model (eager, fp32, cpu)")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=actual_rev, local_files_only=True,
        trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, revision=actual_rev, local_files_only=True,
        torch_dtype=torch.float32, device_map="cpu",
        attn_implementation="eager", trust_remote_code=False)
    model.eval()
    rec["torch"] = torch.__version__
    import transformers as _tf
    rec["transformers"] = _tf.__version__
    import numpy as _np
    rec["numpy"] = _np.__version__
    rec["threads"] = torch.get_num_threads()

    # ---- (a) Δθ=0 pre-hash ----
    pre_hash = sha256_state_dict(model)
    rec["backbone_pre_hash"] = pre_hash
    rec["guards"]["a_prehash_match"] = (pre_hash == BACKBONE_PIN)
    log(f"(a) pre-hash={pre_hash} match={rec['guards']['a_prehash_match']}")
    if not rec["guards"]["a_prehash_match"]:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "guard (a): pre-hash mismatch"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: guard (a)")
        sys.exit(2)

    # ---- (h) throughput probe: 50 generation steps, fixed dummy prompt ----
    dummy = ("The quick brown fox jumps over the lazy dog. " * 6).strip()
    inp = tokenizer(dummy, return_tensors="pt")
    n_steps = 50
    t0 = time.time()
    with torch.no_grad():
        out = model.generate(inp["input_ids"], max_new_tokens=n_steps,
                             do_sample=False,
                             pad_token_id=tokenizer.eos_token_id)
    dt = time.time() - t0
    new_toks = out.shape[1] - inp["input_ids"].shape[1]
    tok_s = new_toks / dt
    # Projected full run: ~47k generation tokens (46k + margin)
    projected_s = 47000 / tok_s
    projected_h = projected_s / 3600
    rec["throughput_probe"] = {
        "dummy_new_tokens": new_toks, "seconds": round(dt, 2),
        "tok_per_s": round(tok_s, 3),
        "projected_seconds_47k": round(projected_s, 1),
        "projected_hours_47k": round(projected_h, 2),
    }
    rec["guards"]["h_compute_feasible"] = projected_h <= 72
    log(f"(h) probe: {new_toks} toks in {dt:.1f}s = {tok_s:.2f} tok/s; "
        f"47k projected {projected_h:.2f}h (cap 72h) "
        f"feasible={rec['guards']['h_compute_feasible']}")
    if not rec["guards"]["h_compute_feasible"]:
        rec["outcome"] = "INCONCLUSIVE"
        rec["reason"] = "guard (h): projected > 72h (compute-infeasible)"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("INCONCLUSIVE: guard (h) — STOP, no GPU escalation")
        sys.exit(3)

    # ---- (c) bench pin: recompute character-identical ----
    with open(BENCH_PATH) as f:
        bench = json.load(f)
    pin = bench_sha256(bench)
    char_match = len(pin) == 64 and all(a == b for a, b in zip(pin, BENCH_PIN))
    rec["bench_pin_recomputed"] = pin
    rec["guards"]["c_bench_pin_match"] = (pin == BENCH_PIN and char_match)
    log(f"(c) bench pin recomputed={pin} match={rec['guards']['c_bench_pin_match']}")
    if not rec["guards"]["c_bench_pin_match"]:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "guard (c): bench pin mismatch"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: guard (c)")
        sys.exit(2)

    rec["outcome"] = "STEP0_PASS"
    json.dump(rec, open(STEP0_JSON, "w"), indent=1)
    log("STEP0_PASS — all of (a),(b),(c),(h) PASS")


if __name__ == "__main__":
    main()
