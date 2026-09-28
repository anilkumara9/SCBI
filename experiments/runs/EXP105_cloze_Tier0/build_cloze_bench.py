# build_cloze_bench.py — EXP105 cloze bench manifest builder (no model contact).
# Carries over from EXP104's bench_manifest.json: the SAME 60 item ids, question
# texts, 8 candidate option strings, token pools, and structural-foil
# designations (D3 blindness transferred — no re-designation). The ONLY change
# is the prompt: the lettered enumeration and "Answer:" terminal are removed and
# replaced with the pinned completion cue "The answer is" (S4-8' v2 sec 2.2).
# Template literal: "<question text verbatim> The answer is"
import json
import hashlib

EXP104 = "/home/hatch/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen"
BUNDLE = "/home/hatch/workspace/SCBI/experiments/runs/EXP105_cloze_Tier0"
CUE = "The answer is"

mc = json.load(open(EXP104 + "/bench_manifest.json"))
assert mc["n_items"] == 60 and mc["k"] == 8

template_literal = "<question text verbatim> The answer is"
template_sha256 = hashlib.sha256(
    ("CUE_LITERAL=" + CUE + "\nASSEMBLY=question + ' ' + CUE\n" +
     "READOUT=next-token logits at position len(input_ids)\n" +
     "TIER0_CUE=" + CUE).encode()).hexdigest()

items = []
for it in mc["items"]:
    prompt = it["question"] + " " + CUE
    items.append({
        "item_id": it["item_id"],
        "question": it["question"],
        "question_sha256": hashlib.sha256(it["question"].encode()).hexdigest(),
        "options": it["options"],                      # scoring set, not displayed
        "option_token_ids": it["option_token_ids"],    # G1 pool (re-attested at run)
        "correct_option": it["correct_option"],
        "correct_position": it["correct_position"],
        "structural_foil": it["structural_foil"],      # D3 designation transferred
        "foil_rationale": it["foil_rationale"],
        "prompt": prompt,
    })

# Integrity: question text byte-identical to the MC stem (no rewording).
for new, old in zip(items, mc["items"]):
    assert new["question"] == old["question"], "stem drift on " + new["item_id"]
    assert new["options"] == old["options"], "pool drift on " + new["item_id"]
    assert new["option_token_ids"] == old["option_token_ids"], "token drift on " + new["item_id"]

manifest = {
    "experiment": "EXP105",
    "tier": "Tier-0",
    "bench_format": "cloze",
    "cue_literal": CUE,
    "template_literal": template_literal,
    "template_sha256": template_sha256,
    "n_items": 60,
    "k": 8,
    "tokenizer_artifact": "EleutherAI/gpt-neox-20b",
    "tokenizer_revision": "main",
    "tokenizer_file_sha256": "c24618a1b3e6a38167beff1c72cffd126c3a66254347304b50547d12c5f25624",
    "g1_attestation": "PENDING — re-confirmed by run_tier0_exp105.py before passes",
    "d3_blindness": ("transferred from EXP104 bench_manifest.json: structural-foil "
                     "designations fixed at bench-build time before any model contact "
                     "on S4-8 bench items; checker-verified (checker_verification.json "
                     "+ checker_addendum.json in the EXP104 bundle). No re-designation "
                     "for cloze re-prompting; any post-hoc foil change = disqualification."),
    "lineage": "items/pools/foils carried over from " + EXP104 + "/bench_manifest.json; "
               "EXP104 MC measurements NOT reused (fresh cloze passes).",
    "items": items,
}
json.dump(manifest, open(BUNDLE + "/cloze_bench_manifest.json", "w"), indent=1)
print("cloze bench manifest written: 60 items, cue=%r, template_sha256=%s"
      % (CUE, template_sha256[:16]))
