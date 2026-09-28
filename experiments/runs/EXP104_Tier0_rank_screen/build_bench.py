# build_bench.py — freeze the EXP104 Tier-0 bench (post-G1, pre-checker).
# Bench-builder: EXP104 Tier-0 execution lane. Foil designations were made at
# bench-build time in bench_spec.py BEFORE any model contact (D3 blindness).
import json, hashlib, sys, random
sys.path.insert(0, "/home/hatch/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen")
from bench_spec import ITEMS, BACKUP_ITEMS, TEMPLATE
from transformers import AutoTokenizer

BUNDLE = "/home/hatch/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen"
SNAP = "/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
SHUFFLE_SEED = 20260928
TOK_NAME = "EleutherAI/gpt-neox-20b"
TOK_FILE_SHA = "c24618a1b3e6a38167beff1c72cffd126c3a66254347304b50547d12c5f25624"

tok = AutoTokenizer.from_pretrained(SNAP, trust_remote_code=False)
template_sha = hashlib.sha256(TEMPLATE.encode()).hexdigest()

def token_id(option):
    ids = tok(" " + option, add_special_tokens=False)["input_ids"]
    assert len(ids) == 1, f"G1 violated for {option!r}"
    return ids[0]

def build(items, seed):
    rng = random.Random(seed)
    out = []
    for i, (q, c, d, f, r) in enumerate(items):
        opts = [c] + d
        perm = list(range(8)); rng.shuffle(perm)
        shuffled = [opts[p] for p in perm]
        correct_pos = perm.index(0)
        token_ids = [token_id(o) for o in shuffled]
        assert len(set(token_ids)) == 8, f"intra-item collision in item {i}"
        prompt = TEMPLATE.format(question=q, o1=shuffled[0], o2=shuffled[1], o3=shuffled[2],
                                 o4=shuffled[3], o5=shuffled[4], o6=shuffled[5],
                                 o7=shuffled[6], o8=shuffled[7])
        enc = tok(prompt, add_special_tokens=False)["input_ids"]
        readout_index = len(enc)  # next-token position after the prompt
        out.append({
            "item_id": f"exp104_t0_{i:02d}",
            "question": q,
            "options": shuffled,
            "option_token_ids": token_ids,
            "correct_option": c,
            "correct_position": correct_pos,
            "structural_foil": f,
            "foil_rationale": r,
            "prompt": prompt,
            "readout_index": readout_index,
        })
    return out

bench = build(ITEMS, SHUFFLE_SEED)
backups = build(BACKUP_ITEMS, SHUFFLE_SEED + 1)

# G1 attestation: per-string evidence
att = []
for it in bench:
    for o, t in zip(it["options"], it["option_token_ids"]):
        att.append({"item_id": it["item_id"], "option": o, "n_tokens": 1, "token_id": t})

code_hash = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
spec_hash = hashlib.sha256(
    open(BUNDLE + "/bench_spec.py", "rb").read()).hexdigest()

manifest = {
    "experiment": "EXP104",
    "tier": "Tier-0",
    "bench_builder": "EXP104 Tier-0 execution lane (this lane), 2026-09-28",
    "d3_blindness_claim": "All structural-foil designations in bench_spec.py were made at bench-build time, "
                          "before any model contact on S4-8 bench items. Independent verification pending "
                          "(checker lane); see checker_verification.json when present.",
    "tokenizer_artifact": TOK_NAME,
    "tokenizer_file_sha256": TOK_FILE_SHA,
    "tokenizer_provenance": "hub EleutherAI/gpt-neox-20b main-branch tokenizer.json byte-identical to "
                            "pythia-410m snapshot copy (verified 2026-09-28)",
    "vocab_size": tok.vocab_size,
    "template_sha256": template_sha,
    "shuffle_seed": SHUFFLE_SEED,
    "n_items": len(bench),
    "k": 8,
    "g1_attestation": {
        "n_option_strings": len(att),
        "all_single_token": True,
        "all_intra_item_distinct": True,
        "per_string": att,
    },
    "bench_build_code_sha256": code_hash,
    "bench_spec_sha256": spec_hash,
    "items": bench,
}
json.dump(manifest, open(BUNDLE + "/bench_manifest.json", "w"), indent=1)
json.dump(backups, open(BUNDLE + "/bench_backups.json", "w"), indent=1)
print("bench frozen:", len(bench), "items; backups:", len(backups))
print("manifest sha256:", hashlib.sha256(open(BUNDLE + "/bench_manifest.json", "rb").read()).hexdigest())
# no fixed correct-position pattern check
from collections import Counter
print("correct-position histogram:", sorted(Counter(it["correct_position"] for it in bench).items()))
