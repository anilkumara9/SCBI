"""EXP145 G1' mismatch diagnostic — full per-entity cover table under GPT-2 BPE.

Runs the SAME offset-mapping cover logic as the committed g1prime module
but collects ALL failures per entity instead of raising. Diagnostic only:
no weights touched, no protocol changed.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp145_common as C  # noqa: E402


def main():
    from transformers import AutoTokenizer
    from huggingface_hub import snapshot_download

    with open(os.path.join(C.RUN_DIR, "exp145_manifest.json")) as f:
        manifest = json.load(f)
    rev = manifest["model_revision_40hex"]
    tok_dir = snapshot_download(
        manifest["repo_id"], revision=rev,
        allow_patterns=["*.json", "*.txt", "*.model"],
        cache_dir=os.path.join(C.RUN_DIR, "hf_cache"))
    tokenizer = AutoTokenizer.from_pretrained(tok_dir, local_files_only=True)
    bench = C.build_bench()
    entities = sorted({b["A"] for b in bench} | {b["C"] for b in bench})

    def word_pattern(name):
        return re.compile(r"\b" + re.escape(name) + r"\b")

    table = {}
    for name in entities:
        table[name] = {"occurrences": 0, "single_token": 0,
                       "token_ids_seen": set(), "failing_items": []}
    for b in bench:
        prompt = b["prompt"]
        enc = tokenizer(prompt, add_special_tokens=False,
                        return_offsets_mapping=True)
        ids = list(enc["input_ids"])
        offsets = [(int(s), int(e)) for s, e in enc["offset_mapping"]]
        pieces = tokenizer.convert_ids_to_tokens(ids)
        for role, name in (("target", b["A"]), ("foil", b["C"])):
            for m in word_pattern(name).finditer(prompt):
                s, e = m.span()
                table[name]["occurrences"] += 1
                covering = [i for i, (os_, oe_) in enumerate(offsets)
                            if os_ < e and oe_ > s]
                ok = False
                if len(covering) == 1:
                    i = covering[0]
                    os_, oe_ = offsets[i]
                    text = pieces[i].lstrip("Ġ").lstrip("▁").lstrip("Ġ")
                    # mirror the committed check: strip the BPE space marker
                    text = pieces[i].replace("Ġ", "").replace("▁", "")
                    if text == name and os_ <= s and oe_ >= e:
                        ok = True
                        table[name]["token_ids_seen"].add(int(ids[i]))
                if ok:
                    table[name]["single_token"] += 1
                else:
                    table[name]["failing_items"].append(
                        {"item": b["id"], "role": role,
                         "covering": [pieces[i] for i in covering]})

    summary = {}
    for name, t in table.items():
        summary[name] = {
            "occurrences": t["occurrences"],
            "single_token": t["single_token"],
            "token_ids": sorted(t["token_ids_seen"]),
            "n_failing_items": len({f["item"] for f in t["failing_items"]}),
            "example_covering": (t["failing_items"][0]["covering"]
                                 if t["failing_items"] else None),
        }
    n_occ = sum(t["occurrences"] for t in table.values())
    n_single = sum(t["single_token"] for t in table.values())
    out = {"n_occurrences": n_occ, "n_single_token": n_single,
           "expected": 240, "per_entity": summary}
    path = os.path.join(C.RUN_DIR, "exp145_g1prime_mismatch.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"occurrences={n_occ} single_token={n_single} (expected 240/240)")
    bad = [n for n, t in summary.items()
           if t["single_token"] < t["occurrences"]]
    print(f"failing entities: {bad}")
    for n in bad:
        print(f"  {n}: {summary[n]['single_token']}/"
              f"{summary[n]['occurrences']} single-token; covering="
              f"{summary[n]['example_covering']}")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
