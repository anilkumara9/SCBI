#!/usr/bin/env python3
"""Decodability Gap falsification kit — Tier-0 runner (model-agnostic).

Scores the 60-item cloze bench on any HuggingFace causal LM and applies the
binding Tier-0 bar order. Deterministic and seed-pinned; the model is frozen
(weight hash asserted identical before and after — the Delta-theta=0 guard).

Usage:
    python tier0.py --model-id EleutherAI/pythia-410m --out results/tier0.json
    python tier0.py --model-id meta-llama/Llama-2-7b-hf --device cuda \
        --dtype float16 --out results/tier0_llama2.json

Output JSON: per-item records with the 8 candidate logits, token ids,
top-1/correct rank, plus a Tier-0 worksheet (verdict, bars, G1 gate).

G1 gate (single-token candidate pools): every candidate string must encode
to exactly ONE token under the model's tokenizer. Items that fail are
excluded and reported — the bench is only licensed on items that pass the
gate. This is the model-agnostic generalization of the EXP105 G1 attestation.

Requires: torch, transformers, numpy.
"""
import argparse
import hashlib
import json
import os
import sys
import time

KIT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT_ROOT)

from core.scoring import correct_rank, top1_decision, tier0_verdict

SEED = 20260928


def weight_hash(model):
    """Streaming SHA-256 over all parameters (fp32 view)."""
    import torch
    h = hashlib.sha256()
    with torch.no_grad():
        for p in model.parameters():
            h.update(p.detach().to(torch.float32).cpu().numpy().tobytes())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Decodability Gap Tier-0 runner")
    ap.add_argument("--model-id", required=True,
                    help="HuggingFace causal-LM id, e.g. EleutherAI/pythia-410m")
    ap.add_argument("--bench", default=os.path.join(KIT_ROOT, "bench",
                                                    "cloze_bench.json"))
    ap.add_argument("--out", required=True, help="output per-item JSON path")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--dtype", default="float32",
                    choices=["float32", "float16", "bfloat16"])
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    torch.manual_seed(args.seed)
    dtype = {"float32": torch.float32, "float16": torch.float16,
             "bfloat16": torch.bfloat16}[args.dtype]

    bench = json.load(open(args.bench))
    items = bench["items"]
    assert len(items) == 60, "bench must carry 60 items"

    print("loading %s ..." % args.model_id, flush=True)
    tok = AutoTokenizer.from_pretrained(args.model_id, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_id, torch_dtype=dtype).to(args.device)
    model.eval()

    hash_before = weight_hash(model)

    # ---- G1 gate: candidate strings must be single tokens ----
    gate_failures = []
    item_pools = []
    for it in items:
        tids = []
        ok = True
        for cand in it["candidates"]:
            # leading-space convention: the cloze cue ends without a space,
            # the candidate is the next token; encode with the space the
            # tokenizer would see at the completion position.
            ids = tok.encode(" " + cand, add_special_tokens=False)
            if len(ids) != 1:
                ok = False
                break
            tids.append(ids[0])
        if not ok or len(set(tids)) != 8:
            gate_failures.append(it["item_id"])
        else:
            item_pools.append((it, tids))
    print("G1 gate: %d/60 items passed single-token attestation"
          % len(item_pools), flush=True)
    if gate_failures:
        print("G1 failures (excluded, listed): %s"
              % ",".join(gate_failures), flush=True)
    if not item_pools:
        raise SystemExit("G1 gate: 0 items passed — HALT, bench not licensed "
                         "on this tokenizer")

    records = []
    n_correct = 0
    failed_ranks = []
    tie_hits = 0
    for it, tids in item_pools:
        enc = tok(it["prompt"], return_tensors="pt")
        input_ids = enc["input_ids"].to(args.device)
        t0 = time.time()
        with torch.no_grad():
            logits = model(input_ids).logits[0, -1, :].to(torch.float32)
        dt = time.time() - t0
        cand_logits = [float(logits[t]) for t in tids]
        top1 = top1_decision(cand_logits, tids)
        rank = correct_rank(cand_logits, it["correct_idx"], tids)
        # tie-guard: exact float32 tie at the top involving >1 candidate
        top_logit = max(cand_logits)
        n_tied = sum(1 for v in cand_logits if v == top_logit)
        tied = n_tied > 1
        tie_hits += 1 if tied else 0
        ok_item = (top1 == it["correct_idx"])
        n_correct += 1 if ok_item else 0
        if not ok_item:
            failed_ranks.append(rank)
        records.append({
            "item_id": it["item_id"],
            "correct_idx": it["correct_idx"],
            "foil_idx": it["foil_idx"],
            "top1_idx": top1,
            "top1_is_correct": ok_item,
            "correct_rank": rank,
            "candidate_logits": cand_logits,
            "candidate_token_ids": tids,
            "top1_tied": tied,
            "pass_seconds": round(dt, 2),
        })
        print("%s rank=%d top1=%s %.1fs" % (
            it["item_id"], rank, it["candidates"][top1], dt), flush=True)

    hash_after = weight_hash(model)
    assert hash_before == hash_after, "WEIGHT DRIFT — Delta-theta=0 violated"
    print("Delta-theta=0 guard: weight hash identical pre/post", flush=True)

    n = len(item_pools)
    baseline_acc = n_correct / n
    tie_rate = tie_hits / n
    verdict = tier0_verdict(baseline_acc, failed_ranks, tie_rate)

    worksheet = {
        "kit": "decodability-gap-falsification-kit",
        "phase": "tier0",
        "model_id": args.model_id,
        "device": args.device,
        "dtype": args.dtype,
        "seed": args.seed,
        "n_items_gated": n,
        "g1_failures": gate_failures,
        "baseline_acc": baseline_acc,
        "n_failed": len(failed_ranks),
        "median_failed_correct_rank":
            float(__import__("statistics").median(failed_ranks))
            if failed_ranks else None,
        "n_pop": sum(1 for r in failed_ranks if r <= 5),
        "tie_rate": tie_rate,
        "weight_sha256": hash_before,
        "verdict": verdict,
    }
    out = {"worksheet": worksheet, "records": records}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(out, open(args.out, "w"), indent=1)
    print("\nTIER-0 VERDICT: %s  (acc=%.4f, failed=%d, tie_rate=%.3f)"
          % (verdict, baseline_acc, len(failed_ranks), tie_rate), flush=True)
    print("wrote %s" % args.out, flush=True)


if __name__ == "__main__":
    main()
