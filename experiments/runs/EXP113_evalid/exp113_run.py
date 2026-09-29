#!/usr/bin/env python3
"""EXP113 — H7/EVALID execution lane (LOG-4584).

Executes the signed pre-registration EXP_PREREG_H7_EVALID_2026-09-29.md EXACTLY:
  600 generations = 5 protocols x 2 tasks x 60 items, greedy, no early abandonment.
Mechanical parse scripts (T1 first-alpha rule = EXP108's rule;
T2 extract_outlines = EXP109's planner-valid rule, ported verbatim).
Deterministic re-parse x2 with byte-identical assertion.
Decision bars applied verbatim from pre-reg section 4.
"""
import hashlib
import json
import os
import sys
import time
import traceback

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ---------------------------------------------------------------- pins
WEIGHTS = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
PROVENANCE_FILE = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json")
PROVENANCE_PIN = "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585"
BACKBONE_PIN = ("ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed")
BENCH_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP089_clm8b_falsifier")
RUN_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP113_evalid")
OUT_DIR = os.path.join(RUN_DIR, "out")
SEED = 0

# ---------------------------------------------------------------- logging
os.makedirs(OUT_DIR, exist_ok=True)
LOG_PATH = os.path.join(OUT_DIR, "exp113_execution_log.txt")
_log_fh = open(LOG_PATH, "a", buffering=1)


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    _log_fh.write(line + "\n")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_state_dict(state_dict):
    """EXP077/EXP084/EXP108 canonical convention: tensor bytes ONLY, sorted keys, float32."""
    h = hashlib.sha256()
    for k in sorted(state_dict.keys()):
        t = state_dict[k]
        arr = t.detach().cpu().to(torch.float32).numpy()
        h.update(arr.tobytes())
    return h.hexdigest()


# ---------------------------------------------------------------- bench (pinned verbatim builder)
sys.path.insert(0, BENCH_DIR)
from benchmark_exp089 import build_benchmark  # noqa: E402

# ---------------------------------------------------------------- templates (pinned verbatim from pre-reg)
T1_P1_TAIL = ("\n\nQuestion: Which option did you choose \u2014 A or C? "
              "Reply with a single letter and nothing else.")
T1_P3_TAIL = ("\n\nQuestion: Which option did you choose? "
              "Answer with exactly one letter, A or C:")
T1_P5_TAIL = ("\n\nQuestion: Which option did you choose \u2014 A or C? "
              "Reply with a single letter and nothing else."
              "\n\nThe single-letter answer is:")
T2_P1_TAIL = ("\n\nPlan: Before answering, write 4 distinct numbered solution outlines "
              "(1. 2. 3. 4.), each a different approach to answering the question. "
              "Each outline must be 40 words or fewer. Do not give the final answer yet.")
T2_P3_TAIL = ("\n\nPlan: Before answering, write exactly 2 distinct numbered solution outlines "
              "(1. 2.), each a different approach to answering the question. "
              "Each outline must be 40 words or fewer. Stop after outline 2. "
              "Do not give the final answer yet.")
T2_P5_TAIL = ("\n\nPlan: Before answering, write 4 distinct numbered solution outlines, "
              "each a different approach to answering the question. "
              "Each outline must be 40 words or fewer. Do not give the final answer yet."
              "\n\n1.")
EXEMPLAR_OUTLINES = (
    "1. Restate the question's ordering constraint in my own words.\n"
    "2. Check each premise statement against the two candidate entities.\n"
    "3. Eliminate the entity contradicted by any premise.\n"
    "4. Name the remaining entity as the answer.")


def build_prompts(bench):
    """Return dict: (task, protocol) -> list of 60 prompt strings (build order)."""
    # True label determination (Law #7): bench ground-truth labels are A=target
    # (H1 pre-reg). ent is always field "A", so the single-letter answer is "A"
    # for every item. Deterministic; cannot inflate parseability.
    t1p2_parts = []
    for ei in (0, 1, 2):
        it = bench[ei]
        assert it["ent"] == it["A"], "ent != A: label assumption violated"
        t1p2_parts.append("Q: " + it["prompt"] + T1_P1_TAIL + "\nA: A")
    t2p2_parts = []
    for ei in (3, 4):
        t2p2_parts.append(bench[ei]["prompt"] + T2_P1_TAIL + "\n" + EXEMPLAR_OUTLINES)

    prompts = {}
    for i in range(60):
        p = bench[i]["prompt"]
        prompts.setdefault(("T1", "P1"), []).append(p + T1_P1_TAIL)
        prompts.setdefault(("T1", "P2"), []).append(
            "\n".join(t1p2_parts) + "\nQ: " + p + T1_P1_TAIL + "\nA:")
        prompts.setdefault(("T1", "P3"), []).append(p + T1_P3_TAIL)
        prompts.setdefault(("T1", "P4"), []).append(p + T1_P1_TAIL)
        prompts.setdefault(("T1", "P5"), []).append(p + T1_P5_TAIL)
        prompts.setdefault(("T2", "P1"), []).append(p + T2_P1_TAIL)
        prompts.setdefault(("T2", "P2"), []).append(
            "\n\n".join(t2p2_parts) + "\n\n" + p + T2_P1_TAIL)
        prompts.setdefault(("T2", "P3"), []).append(p + T2_P3_TAIL)
        prompts.setdefault(("T2", "P4"), []).append(p + T2_P1_TAIL)
        prompts.setdefault(("T2", "P5"), []).append(p + T2_P5_TAIL)
    return prompts


# ---------------------------------------------------------------- parse rules (mechanical, pinned)
def parse_t1(text):
    """EXP108's rule: strip; first alphabetic char; uppercase; in {A, C}."""
    s = text.strip()
    for ch in s:
        if ch.isalpha():
            c = ch.upper()
            return (c in ("A", "C")), c
    return False, None


def extract_outlines(text):
    """EXP109's planner-valid rule, ported verbatim: first-occurrence markers
    '1.'..'4.', preamble discarded, missing marker -> empty, drop empties +
    exact dups. Returns list of (marker_number, outline_text) in marker order."""
    markers = {}
    for k in (1, 2, 3, 4):
        pos = text.find(f"{k}.")
        if pos != -1:
            markers[k] = pos
    if not markers:
        return []
    ordered = sorted(markers.items(), key=lambda kv: kv[1])  # (k, pos) by position
    spans = []
    for idx, (k, pos) in enumerate(ordered):
        start = pos + 2  # end of marker "k."
        end = ordered[idx + 1][1] if idx + 1 < len(ordered) else len(text)
        spans.append((k, text[start:end].strip()))
    # drop empties and exact duplicates (keep first in marker-number order)
    seen = set()
    outlines = []
    for k, t in sorted(spans, key=lambda kv: kv[0]):
        if not t or t in seen:
            continue
        seen.add(t)
        outlines.append((k, t))
    return outlines


def parse_t2(text):
    outlines = extract_outlines(text)
    return len(outlines) >= 2, outlines


BLOCK_A = "\n\nQuestion:"
BLOCK_B = "Write a list of the possible answers"


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    log("EXP113 H7/EVALID execution start (LOG-4584)")

    # --- environment manifest (Law #13)
    import transformers
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    torch.set_num_threads(2)
    threads_set = 2
    threads_read = torch.get_num_threads()
    log(f"env: torch={torch.__version__} transformers={transformers.__version__} "
        f"numpy={np.__version__} threads_set={threads_set} threads_read={threads_read} "
        f"seed={SEED} device=cpu dtype=float32 greedy=True")

    # --- bench provenance (RUN-INVALID on mismatch)
    prov = sha256_file(PROVENANCE_FILE)
    log(f"bench provenance sha256: {prov}")
    assert prov == PROVENANCE_PIN, f"PROVENANCE MISMATCH -> RUN-INVALID ({prov})"
    bench = build_benchmark()
    assert len(bench) == 60, f"bench len {len(bench)} != 60 -> RUN-INVALID"
    log(f"bench rebuilt verbatim: n=60; item0 id={bench[0]['id']}; item59 id={bench[59]['id']}")

    # --- model
    log("loading tokenizer + model (cpu, float32)...")
    tok = AutoTokenizer.from_pretrained(WEIGHTS, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        WEIGHTS, device_map="cpu", torch_dtype=torch.float32)
    model.eval()
    log(f"model: {model.__class__.__name__}; dtype={next(model.parameters()).dtype}")

    h_before = sha256_state_dict(model.state_dict())
    log(f"backbone hash BEFORE: {h_before}")
    assert h_before == BACKBONE_PIN, "BACKBONE HASH MISMATCH (before) -> RUN-INVALID"

    prompts = build_prompts(bench)

    # --- generation (pinned order: P1->P5; within protocol T1 60 items then T2 60 items)
    GEN = {
        ("T1", "P1"): dict(max_new_tokens=4),
        ("T1", "P2"): dict(max_new_tokens=4),
        ("T1", "P3"): dict(max_new_tokens=1),
        ("T1", "P4"): dict(max_new_tokens=4, repetition_penalty=1.2, no_repeat_ngram_size=3),
        ("T1", "P5"): dict(max_new_tokens=4),
        ("T2", "P1"): dict(max_new_tokens=160),
        ("T2", "P2"): dict(max_new_tokens=160),
        ("T2", "P3"): dict(max_new_tokens=96),
        ("T2", "P4"): dict(max_new_tokens=160, repetition_penalty=1.2, no_repeat_ngram_size=3),
        ("T2", "P5"): dict(max_new_tokens=160),
    }

    raw = {"exp": "EXP113", "backbone_hash_before": h_before,
           "provenance_sha256": prov, "seed": SEED,
           "env": {"torch": torch.__version__, "transformers": transformers.__version__,
                   "numpy": np.__version__, "threads_set": threads_set,
                   "threads_read": threads_read},
           "records": []}
    n_exc = 0
    n_empty = 0
    total = 0
    t_gen0 = time.time()
    with torch.no_grad():
        for pnum in ("P1", "P2", "P3", "P4", "P5"):
            for task in ("T1", "T2"):
                key = (task, pnum)
                gkw = GEN[key]
                for i in range(60):
                    prompt = prompts[key][i]
                    total += 1
                    rec = {"task": task, "protocol": pnum, "idx": i,
                           "id": bench[i]["id"], "raw": None,
                           "n_new_tokens": None, "exception": None}
                    try:
                        inp = tok(prompt, return_tensors="pt")
                        out = model.generate(**inp, do_sample=False,
                                             pad_token_id=tok.eos_token_id, **gkw)
                        new_ids = out[0][inp["input_ids"].shape[1]:]
                        gen_text = tok.decode(new_ids, skip_special_tokens=True)
                        rec["raw"] = gen_text
                        rec["n_new_tokens"] = int(new_ids.shape[0])
                        if gen_text == "":
                            n_empty += 1
                    except Exception:
                        n_exc += 1
                        rec["exception"] = traceback.format_exc(limit=3)
                    raw["records"].append(rec)
                    if total % 60 == 0:
                        el = time.time() - t_gen0
                        log(f"progress: {total}/600 generations, {el/60:.1f} min elapsed, "
                            f"exceptions={n_exc}, empty={n_empty}")
                        # Crash-recovery checkpoint (write-only diagnostic; the
                        # registered procedure is unchanged — a crash still
                        # requires a fresh full re-run, never a partial resume).
                        try:
                            with open(os.path.join(
                                    OUT_DIR, "exp113_raw_partial.json"), "w") as pf:
                                json.dump({"records": raw["records"],
                                           "exceptions": n_exc,
                                           "empty": n_empty}, pf)
                        except Exception as cpe:
                            log(f"checkpoint write failed (non-fatal): {cpe}")
    log(f"generation complete: {total}/600, exceptions={n_exc}, empty={n_empty}, "
        f"gen_time_min={(time.time()-t_gen0)/60:.1f}")

    # --- apparatus RUN-INVALID branches
    if total and (n_empty / total > 0.90 or n_exc / total > 0.10):
        log(f"GLOBAL GENERATION FAILURE -> RUN-INVALID (empty={n_empty}, exc={n_exc})")
        raise SystemExit("RUN-INVALID")

    h_after = sha256_state_dict(model.state_dict())
    log(f"backbone hash AFTER: {h_after}")
    assert h_after == BACKBONE_PIN, "BACKBONE HASH MISMATCH (after) -> RUN-INVALID"
    raw["backbone_hash_after"] = h_after

    # --- mechanical parse, run twice (Law #14-grade anti-self-deception)
    def parse_all():
        table = {}
        for rec in raw["records"]:
            task, pnum, idx = rec["task"], rec["protocol"], rec["idx"]
            text = rec["raw"] if rec["raw"] is not None else ""
            if task == "T1":
                ok, detail = parse_t1(text)
                detail = {"first_alpha": detail}
            else:
                ok, outlines = parse_t2(text)
                detail = {"outlines": [{"k": k, "text": t} for k, t in outlines]}
            block_a = BLOCK_A in text
            block_b = BLOCK_B in text
            table[(task, pnum, idx)] = {"parseable": ok, "detail": detail,
                                        "block_a": block_a, "block_b": block_b}
        return table

    t1 = parse_all()
    t2 = parse_all()
    j1 = json.dumps({str(k): v for k, v in t1.items()}, sort_keys=True)
    j2 = json.dumps({str(k): v for k, v in t2.items()}, sort_keys=True)
    assert j1 == j2, "DETERMINISTIC RE-PARSE MISMATCH -> RUN-INVALID"
    log("deterministic re-parse: byte-identical (2 runs)")

    # --- counts + decision bars (pre-reg section 4, verbatim)
    r1, r2 = {}, {}
    for pnum in ("P1", "P2", "P3", "P4", "P5"):
        r1[pnum] = sum(1 for i in range(60) if t1[("T1", pnum, i)]["parseable"])
        r2[pnum] = sum(1 for i in range(60) if t2[("T2", pnum, i)]["parseable"])
    t1_clear = [p for p in r1 if r1[p] >= 48]
    t2_clear = [p for p in r2 if r2[p] >= 48]
    if t1_clear and t2_clear:
        verdict = "CONTINUE"
    elif t1_clear or t2_clear:
        verdict = "PIVOT"
    elif max(list(r1.values()) + list(r2.values())) <= 21:
        verdict = "KILL"
    else:
        verdict = "HELD"
    log(f"r1(T1)={r1} r2(T2)={r2}")
    log(f"T1-CLEAR={t1_clear} T2-CLEAR={t2_clear} -> verdict={verdict}")

    # --- descriptive blocklist diagnostic (no decision branch reads it)
    diag = {}
    for pnum in ("P1", "P2", "P3", "P4", "P5"):
        for task in ("T1", "T2"):
            n_a = sum(1 for i in range(60) if t1[(task, pnum, i)]["block_a"])
            n_b = sum(1 for i in range(60) if t1[(task, pnum, i)]["block_b"])
            diag[f"{task}-{pnum}"] = {"frac_block_a": n_a / 60, "frac_block_b": n_b / 60}
    log(f"blocklist diagnostic: {diag}")

    raw["parse_table_run1"] = {str(k): v for k, v in t1.items()}
    raw["counts"] = {"r1": r1, "r2": r2, "t1_clear": t1_clear,
                     "t2_clear": t2_clear, "verdict": verdict}
    raw["blocklist_diagnostic"] = diag
    raw["exceptions_total"] = n_exc
    raw["empty_total"] = n_empty

    with open(os.path.join(OUT_DIR, "exp113_raw.json"), "w") as f:
        json.dump(raw, f)
    log(f"raw records written: {len(raw['records'])}")
    log(f"EXP113 execution done in {(time.time()-t0)/60:.1f} min; verdict={verdict}")
    print(f"VERDICT={verdict}", flush=True)


if __name__ == "__main__":
    main()
