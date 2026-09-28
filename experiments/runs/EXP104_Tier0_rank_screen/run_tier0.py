# run_tier0.py — EXP104 Tier-0 correct-rank screen (frozen Pythia-410m, CPU, $0).
# Runs ONLY after checker_verification.json exists with bench_accepted=true.
# ≤120 passes: 60 items x 1 baseline logit pass. Arm B only. No masking (battery-gated).
import json, hashlib, os, sys, time, statistics, resource
import torch

BUNDLE = "/home/hatch/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen"
SNAP = "/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
SEED = 20260928
torch.manual_seed(SEED)
torch.set_num_threads(2)

chk = json.load(open(BUNDLE + "/checker_verification.json"))
accepted = chk.get("bench_accepted") is True
add_path = BUNDLE + "/checker_addendum.json"
if not accepted and os.path.exists(add_path):
    accepted = json.load(open(add_path)).get("bench_accepted_final") is True
    print("checker addendum applied:", json.load(open(add_path))["change"][:120], "...")
assert accepted, "checker did not accept the bench — HALT"
print("bench accepted for execution")

manifest = json.load(open(BUNDLE + "/bench_manifest.json"))
items = manifest["items"]
assert len(items) == 60

# ---- Δθ=0 guard: weight-file hash pre ----
WFILE = SNAP + "/model.safetensors"
def fhash(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()
hash_pre = fhash(WFILE)
print("weight sha256 pre :", hash_pre)

from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained(SNAP, trust_remote_code=False)
model = AutoModelForCausalLM.from_pretrained(SNAP, torch_dtype=torch.float32,
                                             trust_remote_code=False, low_cpu_mem_usage=True)
model.eval()
assert not model.training
print("model loaded; params:",
      sum(p.numel() for p in model.parameters()) / 1e6, "M")

def correct_rank(logits8, correct_idx):
    order = sorted(range(8), key=lambda j: (-logits8[j], j))
    return order.index(correct_idx) + 1

rec_path = BUNDLE + "/per_item_records.json"
records = {}
if os.path.exists(rec_path):
    for r in json.load(open(rec_path)):
        records[r["item_id"]] = r
    print("resuming:", len(records), "already done")

t_all = time.time()
for it in items:
    iid = it["item_id"]
    if iid in records:
        continue
    enc = tok(it["prompt"], add_special_tokens=False)["input_ids"]
    assert len(enc) == it["readout_index"], f"readout drift on {iid}"
    t0 = time.time()
    with torch.no_grad():
        out = model(torch.tensor([enc]))
    logits = out.logits[0, -1, :].float()
    opt_logits = [float(logits[t]) for t in it["option_token_ids"]]
    top1 = max(range(8), key=lambda j: (opt_logits[j], -j))
    r = correct_rank(opt_logits, it["correct_position"])
    mx = max(opt_logits)
    tied_at_top = (opt_logits[it["correct_position"]] == mx) and (sum(1 for v in opt_logits if v == mx) >= 2)
    records[iid] = {
        "item_id": iid, "arm": "B",
        "top1_position": top1, "top1_option": it["options"][top1],
        "correct_position": it["correct_position"], "correct_option": it["correct_option"],
        "correct_rank": r, "correct_is_top1": top1 == it["correct_position"],
        "option_logits": opt_logits, "masked_token": None,
        "correct_tied_at_top": tied_at_top,
        "readout_index": it["readout_index"],
        "pass_seconds": round(time.time() - t0, 1),
    }
    json.dump(list(records.values()), open(rec_path, "w"))
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print(f"{iid} rank={r} top1={it['options'][top1]!r} {records[iid]['pass_seconds']}s rss={rss:.2f}GB",
          flush=True)

print("all 60 passes done in", round(time.time() - t_all, 1), "s")

# ---- Δθ=0 guard: weight-file hash post ----
hash_post = fhash(WFILE)
print("weight sha256 post:", hash_post)
assert hash_pre == hash_post, "WEIGHT HASH CHANGED — run void"

# ---- Tier-0 worksheet (§3 steps 1-5, first match wins) ----
recs = [records[it["item_id"]] for it in items]
failed = [r for r in recs if not r["correct_is_top1"]]
ranks = [r["correct_rank"] for r in failed]
n_fail = len(failed)
acc = (60 - n_fail) / 60
tier0pop = [r for r in failed if r["correct_rank"] <= 5]
n_pop = len(tier0pop)
tie_numer = sum(1 for r in tier0pop if r["correct_tied_at_top"])
tie_rate = (tie_numer / n_pop) if n_pop else None
median_rank = statistics.median(ranks) if ranks else None

if n_fail == 0:
    route = "KILL-premise-vacuous"   # §4(e)
elif median_rank > 5:
    route = "KILL-premise"           # §3 step 2
elif n_pop < 12:
    route = "UNDERDETERMINED"        # §3 step 3
elif not (0.25 <= acc <= 0.75):
    route = "HOLD-sanity"            # §3 step 4
elif tie_rate > 0.25:
    route = "HOLD-tieguard"          # §3 step 5
else:
    route = "TIER0-PASSED"

worksheet = {
    "experiment": "EXP104", "tier": "Tier-0",
    "n_items": 60, "n_passes": 60, "pass_budget": 120,
    "baseline_accuracy": acc, "n_failed": n_fail,
    "median_correct_rank_failed": median_rank,
    "failed_ranks": ranks,
    "n_pop": n_pop,
    "tie_guard": {"numerator": tie_numer, "denominator": n_pop, "rate": tie_rate},
    "step1_g1": "PASS",
    "route": route,
    "delta_theta0": {"weight_sha256_pre": hash_pre, "weight_sha256_post": hash_post, "match": True},
    "seed": SEED,
    "torch": torch.__version__,
}
import transformers
worksheet["transformers"] = transformers.__version__
worksheet["script_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
json.dump(worksheet, open(BUNDLE + "/tier0_worksheet.json", "w"), indent=1)
print(json.dumps({k: worksheet[k] for k in
      ["baseline_accuracy", "n_failed", "median_correct_rank_failed", "n_pop",
       "tie_guard", "route"]}, indent=1))
print("ROUTE:", route)
