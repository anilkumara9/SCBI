# G1 probe: real-tokenizer verification of all 480 option strings (EXP090 lesson).
# Operationalization: the scored token is the next token after "Answer:", i.e. the
# option string with a leading space. Single-token check on (" " + option).
import json, sys, hashlib
sys.path.insert(0, "/home/hatch/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen")
from bench_spec import ITEMS, BACKUP_ITEMS, TEMPLATE

from transformers import AutoTokenizer

TOK_ID = "EleutherAI/gpt-neox-20b"
SNAP = "/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
# Provenance [FACT, verified 2026-09-28]: the hub copy of the gpt-neox-20b
# tokenizer.json (main branch) is BYTE-IDENTICAL (sha256 c24618a1...) to the
# tokenizer.json bundled in the frozen pythia-410m snapshot. Loading the local
# snapshot copy; the hub fetch of the repo id fails on config resolution in this
# environment, but the artifact bytes are the pinned gpt-neox-20b artifact.
tok = AutoTokenizer.from_pretrained(SNAP, trust_remote_code=False)
src = "local:pythia-410m snapshot tokenizer.json == hub EleutherAI/gpt-neox-20b tokenizer.json (byte-identical)"
file_sha = hashlib.sha256(open(SNAP + "/tokenizer.json", "rb").read()).hexdigest()
rev = "tokenizer.json sha256=" + file_sha + " (== hub gpt-neox-20b main-branch copy, verified 2026-09-28)"

def tok_id(s):
    ids = tok(" " + s, add_special_tokens=False)["input_ids"]
    return ids

fails = []
per_item = []
all_opts = []
for i, (q, c, d, f, r) in enumerate(ITEMS):
    opts = [c] + d
    ids = [tok_id(o) for o in opts]
    multi = [(o, x) for o, x in zip(opts, ids) if len(x) != 1]
    flat = [x[0] for x in ids if len(x) == 1]
    dup = len(flat) != len(set(flat))
    if multi or dup:
        fails.append({"item": i, "question": q, "multi_token": [(o, x) for o, x in multi],
                      "collision": dup})
    per_item.append({"item": i, "single_token_all": not multi, "distinct": not dup})
    all_opts += opts

print("tokenizer source:", src)
print("tokenizer revision:", rev)
print("vocab size:", tok.vocab_size)
print("items:", len(ITEMS), "options:", len(all_opts))
print("G1 FAILURES:", len(fails))
for fl in fails:
    print(" item", fl["item"], fl["question"][:60])
    for o, x in fl["multi_token"]:
        print("   MULTI:", repr(o), "->", x, [tok.decode([t]) for t in x])
    if fl["collision"]:
        print("   COLLISION within item")

# template hash
th = hashlib.sha256(TEMPLATE.encode()).hexdigest()
print("template_sha256:", th)

json.dump({"tokenizer_id": TOK_ID, "tokenizer_source": src, "tokenizer_revision": rev,
           "vocab_size": tok.vocab_size, "template_sha256": th,
           "n_items": len(ITEMS), "n_options": len(all_opts),
           "n_failures": len(fails), "failures": fails},
          open("/home/hatch/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen/g1_probe.json", "w"), indent=1)
print("G1 probe ->", "PASS" if not fails else "FAIL")
