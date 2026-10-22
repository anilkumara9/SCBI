# verify_resume.py — one-pass determinism check across the VM restart:
# recompute item exp104_t0_00 and require EXACT float equality of the 8
# candidate logits vs the pre-restart stored record. Pass -> resume is valid.
import json, sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

BUNDLE = "/home/hatch/workspace/SCBI/experiments/runs/EXP105_cloze_Tier0"
SNAP = "/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
torch.manual_seed(20260928)
torch.set_num_threads(2)

manifest = json.load(open(BUNDLE + "/cloze_bench_manifest.json"))
it = manifest["items"][0]
assert it["item_id"] == "exp104_t0_00"
stored = {r["item_id"]: r for r in json.load(open(BUNDLE + "/per_item_records.json"))}["exp104_t0_00"]

tok = AutoTokenizer.from_pretrained(SNAP, trust_remote_code=False)
model = AutoModelForCausalLM.from_pretrained(SNAP, torch_dtype=torch.float32,
                                             trust_remote_code=False, low_cpu_mem_usage=True)
model.eval()
enc = tok(it["prompt"], add_special_tokens=False)["input_ids"]
with torch.no_grad():
    logits = model(torch.tensor([enc])).logits[0, -1, :].float()
fresh = [float(logits[t]) for t in it["option_token_ids"]]
old = stored["candidate_logits"]
match = all(a == b for a, b in zip(fresh, old))
print("fresh :", [round(x, 6) for x in fresh])
print("stored:", [round(x, 6) for x in old])
print("EXACT MATCH:", match)
sys.exit(0 if match else 1)
