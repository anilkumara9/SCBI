#!/usr/bin/env python3
"""Decodability Gap falsification kit — intervention battery (model-agnostic).

Applies the four pre-registered logit-level masking arms to recorded Tier-0
8-candidate logit vectors and walks the binding decision table. Masking is a
pure logit operator (-1e9 before argmax): NO model contact is needed or
performed, so Delta-theta=0 holds by construction and the battery costs $0.

Input:  the JSON written by tier0.py ({"worksheet":..., "records":[...]}),
        or any JSON list of records with fields:
        item_id, candidate_logits[8], candidate_token_ids[8],
        correct_idx, foil_idx, top1_idx.
Usage:
    python battery.py --records results/tier0.json --out results/battery.json

Output: worksheet JSON with dM contrasts, McNemar-exact p-values, Tango 95%
CIs, foil-top1 overlap O, and the binding decision-table verdict.

Requires: numpy (scipy optional — Tango CIs fall back to Newcombe-Wilson).
"""
import argparse
import json
import os
import random
import sys

KIT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT_ROOT)

from core.scoring import (
    top1_decision, battery_arms, battery_decision, R_SEED,
)


def main():
    ap = argparse.ArgumentParser(description="Decodability Gap battery")
    ap.add_argument("--records", required=True,
                    help="tier0.py output JSON (or bare records list)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=R_SEED)
    args = ap.parse_args()

    data = json.load(open(args.records))
    records = data["records"] if isinstance(data, dict) else data
    assert records, "empty records"

    rng = random.Random(args.seed)  # pinned BEFORE any battery computation

    pop_records = []
    full_records = []
    for rec in records:
        logits = rec["candidate_logits"]
        tids = rec["candidate_token_ids"]
        top1 = rec["top1_idx"]
        correct = rec["correct_idx"]
        foil = rec["foil_idx"]
        arms, r_mask = battery_arms(logits, tids, top1, correct, foil, rng)
        arms_correct = {a: (idx == correct) for a, idx in arms.items()}
        rank_ok = rec.get("correct_rank")
        in_pop = (not arms_correct["B"]) and (
            rank_ok is not None and rank_ok <= 5)
        entry = {
            "item_id": rec["item_id"],
            "arms_correct": arms_correct,
            "foil_is_top1": (tids[foil] == tids[top1]),
            "r_mask_idx": r_mask,
            "in_tier0_pop": in_pop,
        }
        full_records.append(entry)
        if in_pop:
            pop_records.append(entry)

    verdict, step, evidence, contrasts = battery_decision(pop_records)

    worksheet = {
        "kit": "decodability-gap-falsification-kit",
        "phase": "battery",
        "seed": args.seed,
        "n_items": len(records),
        "n_pop": evidence["n_pop"],
        "dM_primary_tier0pop": {"T": evidence["dM_T"], "F": evidence["dM_F"],
                                "R": evidence["dM_R"]},
        "contrasts": {k: {"b": v["b"], "c": v["c"], "d": v["d"], "p": v["p"],
                          "tango95": list(v["tango95"])}
                       for k, v in contrasts.items()},
        "decision": {"verdict": verdict, "step": step, "evidence": evidence},
        "guards": {
            "model_contact": "none — logit-level operator; Delta-theta=0 by construction",
            "bars": "DELTA_BAR=0.10, flat band |dM|<0.05, "
                    "primary T-vs-R alpha=0.05, others Bonferroni 0.0125, "
                    "O_GATE=0.5",
        },
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump({"worksheet": worksheet, "records": full_records},
              open(args.out, "w"), indent=1)
    print("n_pop=%d dM_T=%.4f dM_F=%.4f dM_R=%.4f O=%.4f" % (
        evidence["n_pop"], evidence["dM_T"], evidence["dM_F"],
        evidence["dM_R"], evidence["O"]), flush=True)
    print("T-vs-R: b=%d c=%d p=%.4f" % (
        contrasts["T-vs-R"]["b"], contrasts["T-vs-R"]["c"],
        contrasts["T-vs-R"]["p"]), flush=True)
    print("\nBATTERY VERDICT: %s (step %d)" % (verdict, step), flush=True)
    print("wrote %s" % args.out, flush=True)


if __name__ == "__main__":
    main()
