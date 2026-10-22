#!/usr/bin/env python3
"""EXP109 (H4/PTTSC) execution — CPU pilot, verbatim per pre-registration
research/prereg/EXP_PREREG_H4_PTTSC_2026-09-29.md (LOG-4547..4550, CEO launch LOG-4551).

Phase 1 (generation): planner + executor + baseline generations, labels NEVER used.
Phase 2 (analysis): RUN-INVALID gates first; scoring only if gates pass (labels at metric time only).

Output: out/exp109_raw.json (raw logs), out/exp109_analysis.json, console log.
"""
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

# ---------------------------------------------------------------- pins
WEIGHTS = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
OUT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/out"
os.makedirs(OUT_DIR, exist_ok=True)

BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
PROVENANCE_PIN = "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585"
PROVENANCE_FILE = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json")

PLANNER_TAIL = ("\n\nPlan: Before answering, write 4 distinct numbered solution outlines "
                "(1. 2. 3. 4.), each a different approach to answering the question. "
                "Each outline must be 40 words or fewer. Do not give the final answer yet.")
EXECUTOR_TAIL = ("\n\nDevelop the outline above into a final answer. "
                 "Reply with the name of the higher-ranked entity and nothing else.")
BASELINE_TAIL = ("\n\nAnswer the question above. "
                 "Reply with the name of the higher-ranked entity and nothing else.")
TRAIL_PUNCT = ".,;:!?"


def log(msg):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}Z] {msg}", flush=True)


def sha256_state_dict(state_dict):
    """Exact EXP077/EXP084 convention: tensor bytes ONLY, sorted keys, float32."""
    h = hashlib.sha256()
    for k in sorted(state_dict.keys()):
        t = state_dict[k]
        if hasattr(t, "detach"):
            arr = t.detach().cpu().to(torch.float32).numpy()
        else:
            arr = np.asarray(t, dtype=np.float32)
        h.update(arr.tobytes())
    return h.hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_outlines(text):
    """Pinned §3.3: first-occurrence markers '1.'..'4.', preamble discarded,
    missing marker -> empty, drop empties + exact dups. Returns list of
    (marker_number, outline_text) in marker order after dedup."""
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


def parse_vote(gen_text, name_a, name_c):
    """Pinned §3.5: strip whitespace + trailing punctuation, case-insensitive
    exact match vs the two entity names; else None (UNPARSEABLE)."""
    s = gen_text.strip().rstrip(TRAIL_PUNCT).strip()
    if s.lower() == name_a.lower():
        return name_a
    if s.lower() == name_c.lower():
        return name_c
    return None


# ---------------------------------------------------------------- setup
def main():
    t0 = time.time()
    log("EXP109 H4/PTTSC execution start")

    # Provenance gate (before any generation)
    prov = sha256_file(PROVENANCE_FILE)
    log(f"provenance sha256: {prov}")
    assert prov == PROVENANCE_PIN, f"PROVENANCE MISMATCH -> RUN-INVALID ({prov})"

    sys.path.insert(0, os.path.expanduser(
        "~/workspace/SCBI/experiments/runs/EXP089_clm8b_falsifier"))
    from benchmark_exp089 import build_benchmark
    bench = build_benchmark()
    assert len(bench) == 60, f"bench len {len(bench)} != 60"
    items = bench[0:20]
    assert len(items) == 20, "pilot scope must be exactly 20 items"
    log(f"bench rebuilt verbatim: n=60; pilot items 0..19; item0 id={items[0]['id']}")

    log("loading tokenizer + model (cpu, float32)...")
    tok = AutoTokenizer.from_pretrained(WEIGHTS, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        WEIGHTS, device_map="cpu", torch_dtype=torch.float32)
    model.eval()
    log(f"model: {model.__class__.__name__}; dtype={next(model.parameters()).dtype}; "
        f"threads={torch.get_num_threads()}")

    h_before = sha256_state_dict(model.state_dict())
    log(f"backbone hash BEFORE: {h_before}")
    assert h_before == BACKBONE_PIN, f"BACKBONE HASH MISMATCH (before) -> RUN-INVALID"

    # ---------------------------------------------------------------- phase 1: generation
    raw = {"exp": "EXP109", "backbone_hash_before": h_before,
           "provenance_sha256": prov, "items": []}
    total_gen = 0
    t_gen0 = time.time()

    with torch.no_grad():
        for i, it in enumerate(items):
            prompt = it["prompt"]
            name_a, name_c = it["A"], it["C"]
            rec = {"idx": i, "id": it["id"], "A": name_a, "C": name_c,
                   "phrasing": it.get("phrasing"), "hop": it.get("hop"),
                   "planner": None, "outlines": [], "planner_valid": False,
                   "executor_gens": [], "baseline_gens": []}

            # --- planner arm: one greedy pass
            planner_prompt = prompt + PLANNER_TAIL
            inp = tok(planner_prompt, return_tensors="pt")
            out = model.generate(**inp, do_sample=False, max_new_tokens=160,
                                 pad_token_id=tok.eos_token_id)
            gen_text = tok.decode(out[0][inp["input_ids"].shape[1]:],
                                  skip_special_tokens=True)
            total_gen += 1
            outlines = extract_outlines(gen_text)
            rec["planner"] = {"raw": gen_text,
                              "n_tokens": int((out[0].shape[0]
                                               - inp["input_ids"].shape[1]))}
            rec["outlines"] = [{"k": k, "text": t} for k, t in outlines]
            rec["planner_valid"] = len(outlines) >= 2

            # --- executor arm: develop exactly the extracted outlines
            votes = []
            for oi, (k, otext) in enumerate(outlines):
                ex_prompt = (prompt + f"\n\nOutline {k}: {otext}" + EXECUTOR_TAIL)
                seed = 2000 + 10 * i + oi
                set_seed(seed)
                torch.manual_seed(seed)
                inp2 = tok(ex_prompt, return_tensors="pt")
                out2 = model.generate(**inp2, temperature=0.7, top_p=0.9,
                                      max_new_tokens=48, do_sample=True,
                                      pad_token_id=tok.eos_token_id)
                g2 = tok.decode(out2[0][inp2["input_ids"].shape[1]:],
                                skip_special_tokens=True)
                total_gen += 1
                v = parse_vote(g2, name_a, name_c)
                votes.append({"outline_k": k, "outline_idx": oi, "seed": seed,
                              "raw": g2, "vote": v})
            rec["executor_gens"] = votes
            rec["executor_parseable"] = sum(1 for x in votes if x["vote"] is not None)

            # --- baseline arm: 4 independent samples, identical sampling spec
            bvotes = []
            for s in range(4):
                b_prompt = prompt + BASELINE_TAIL
                seed = 3000 + 10 * i + s
                set_seed(seed)
                torch.manual_seed(seed)
                inp3 = tok(b_prompt, return_tensors="pt")
                out3 = model.generate(**inp3, temperature=0.7, top_p=0.9,
                                      max_new_tokens=48, do_sample=True,
                                      pad_token_id=tok.eos_token_id)
                g3 = tok.decode(out3[0][inp3["input_ids"].shape[1]:],
                                skip_special_tokens=True)
                total_gen += 1
                v = parse_vote(g3, name_a, name_c)
                bvotes.append({"sample_idx": s, "seed": seed, "raw": g3, "vote": v})
            rec["baseline_gens"] = bvotes
            rec["baseline_parseable"] = sum(1 for x in bvotes if x["vote"] is not None)

            raw["items"].append(rec)
            if (i + 1) % 5 == 0 or i == 0:
                el = time.time() - t_gen0
                log(f"item {i+1}/20 done | planner_valid={rec['planner_valid']} "
                    f"({len(outlines)} outlines) | exec_parseable={rec['executor_parseable']}/"
                    f"{len(votes)} | base_parseable={rec['baseline_parseable']}/4 | "
                    f"{total_gen} gens, {el/60:.1f} min elapsed")

    h_after = sha256_state_dict(model.state_dict())
    log(f"backbone hash AFTER: {h_after}")
    gen_minutes = (time.time() - t_gen0) / 60

    raw["backbone_hash_after"] = h_after
    raw["generation_minutes"] = gen_minutes
    raw["total_generations"] = total_gen
    with open(f"{OUT_DIR}/exp109_raw.json", "w") as f:
        json.dump(raw, f)
    log(f"raw log saved: {OUT_DIR}/exp109_raw.json")

    # ---------------------------------------------------------------- phase 2: gates then scoring
    analysis = {"gates": {}, "run_invalid": None}

    if h_after != BACKBONE_PIN:
        analysis["run_invalid"] = (
            f"RUN-INVALID: backbone hash mismatch (Δθ≠0). before={h_before} after={h_after}")
    else:
        # per-item arm validity (labels NOT used)
        valid_items = []
        n_exec_unparse = 0
        n_exec_total = 0
        n_base_unparse = 0
        n_base_total = 0
        for rec in raw["items"]:
            ev = [x["vote"] for x in rec["executor_gens"] if x["vote"] is not None]
            bv = [x["vote"] for x in rec["baseline_gens"] if x["vote"] is not None]
            n_exec_unparse += len(rec["executor_gens"]) - len(ev)
            n_exec_total += len(rec["executor_gens"])
            n_base_unparse += len(rec["baseline_gens"]) - len(bv)
            n_base_total += len(rec["baseline_gens"])
            arm_ok = (rec["planner_valid"] and len(ev) >= 3 and len(bv) >= 3)
            rec["_ev"] = ev
            rec["_bv"] = bv
            rec["_arm_ok"] = arm_ok
            if arm_ok:
                valid_items.append(rec)

        n_valid = len(valid_items)
        analysis["gates"]["n_valid"] = n_valid
        analysis["gates"]["items_invalid"] = 20 - n_valid
        unparse_frac = ((n_exec_unparse + n_base_unparse)
                        / max(1, (n_exec_total + n_base_total)))
        analysis["gates"]["exec_unparseable"] = [n_exec_unparse, n_exec_total]
        analysis["gates"]["base_unparseable"] = [n_base_unparse, n_base_total]
        analysis["gates"]["unparseable_fraction"] = unparse_frac

        if 20 - n_valid >= 3:
            analysis["run_invalid"] = (
                f"RUN-INVALID: elicitation failure — 20−n_valid={20-n_valid} ≥ 3")
        elif unparse_frac >= 0.50:
            analysis["run_invalid"] = (
                f"RUN-INVALID: apparatus failure — {unparse_frac:.1%} of executor+baseline "
                f"vote-generations UNPARSEABLE (≥50% tripwire)")

    if analysis["run_invalid"]:
        log(analysis["run_invalid"])
        with open(f"{OUT_DIR}/exp109_analysis.json", "w") as f:
            json.dump(analysis, f, indent=1)
        log("STOPPED at RUN-INVALID gate. No metric read.")
        return

    # ---- scoring (metric time; labels used only here)
    per_item = []
    b = c = 0
    tie_exec = tie_base = 0
    acc_p = acc_b = 0
    for rec in valid_items:
        target, foil = rec["A"], rec["C"]
        ev, bv = rec["_ev"], rec["_bv"]

        def vote_of(votes):
            na = sum(1 for v in votes if v == target)
            nc = sum(1 for v in votes if v == foil)
            if na > nc:
                return target, False
            if nc > na:
                return foil, False
            return foil, True  # tie -> foil (pinned §3.6)

        pv, pt = vote_of(ev)
        bsv, bt = vote_of(bv)
        tie_exec += pt
        tie_base += bt
        p_ok = (pv == target)
        b_ok = (bsv == target)
        acc_p += p_ok
        acc_b += b_ok
        if p_ok and not b_ok:
            b += 1
        elif b_ok and not p_ok:
            c += 1
        per_item.append({"idx": rec["idx"], "id": rec["id"],
                         "n_outlines": len(rec["outlines"]),
                         "executor_votes": ev, "executor_majority": pv,
                         "executor_tie": pt, "executor_correct": p_ok,
                         "baseline_votes": bv, "baseline_majority": bsv,
                         "baseline_tie": bt, "baseline_correct": b_ok})

    n = n_valid
    net = (acc_p - acc_b) / n
    n_disc = b + c
    if n_disc == 0:
        p_one = 1.0
    else:
        p_one = sum(math.comb(n_disc, k) for k in range(b, n_disc + 1)) / (2 ** n_disc)
    analysis["scoring"] = {
        "n_valid": n, "b": b, "c": c, "net": net,
        "mcnemar_one_sided_p": p_one,
        "acc_planner": acc_p / n, "acc_baseline": acc_b / n,
        "ties_executor": tie_exec, "ties_baseline": tie_base,
        "per_item": per_item,
    }
    if p_one <= 0.05:
        verdict = "CONTINUE"
    elif net <= 0:
        verdict = "KILL"
    else:
        verdict = "HELD"
    analysis["verdict"] = verdict
    with open(f"{OUT_DIR}/exp109_analysis.json", "w") as f:
        json.dump(analysis, f, indent=1)

    log(f"SCORING: n_valid={n} b={b} c={c} net={net:+.3f} "
        f"McNemar one-sided p={p_one:.4f}")
    log(f"acc_planner={acc_p/n:.3f} acc_baseline={acc_b/n:.3f} "
        f"ties(exec/base)={tie_exec}/{tie_base}")
    log(f"VERDICT: {verdict}")
    log(f"total wall time: {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
