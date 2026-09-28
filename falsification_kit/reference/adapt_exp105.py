#!/usr/bin/env python3
"""Adapt the committed EXP105 Tier-0 per-item records to the kit record format.

EXP105 records carry correct_position (not correct_idx) and no foil_idx /
candidate_token_ids array. Foil designations and the reference gpt-neox-20b
token-id pools come from the kit bench (bench/cloze_bench.json), which is
byte-identical in content to the EXP105 cloze_bench_manifest.json items.
"""
import json
import os
import sys

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP105_T0 = ("/home/hatch/workspace/SCBI/experiments/runs/"
             "EXP105_cloze_Tier0/per_item_records.json")


def main():
    bench = json.load(open(os.path.join(KIT_ROOT, "bench",
                                        "cloze_bench.json")))
    bmap = {it["item_id"]: it for it in bench["items"]}
    exp = json.load(open(EXP105_T0))
    out = []
    for rec in exp:
        b = bmap[rec["item_id"]]
        assert rec["correct_position"] == b["correct_idx"], "index drift"
        out.append({
            "item_id": rec["item_id"],
            "candidate_logits": rec["candidate_logits"],
            "candidate_token_ids": b["reference_token_ids_gpt_neox_20b"],
            "correct_idx": b["correct_idx"],
            "foil_idx": b["foil_idx"],
            "top1_idx": rec["top1_idx"],
            "correct_rank": rec["correct_rank"],
        })
    assert len(out) == 60
    dest = os.path.join(KIT_ROOT, "reference", "exp105_tier0_kitformat.json")
    json.dump(out, open(dest, "w"), indent=1)
    print("wrote %s (%d records)" % (dest, len(out)))


if __name__ == "__main__":
    main()
