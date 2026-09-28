# run_tier0_exp105.py — EXP105 cloze Tier-0 execution (frozen Pythia-410m, CPU, $0).
# Signed S4-8' v2 protocol; CEO execution clearance granted. Runs Tier-0 ONLY.
# Binding bar order: baseline<0.25 -> LINE-CLOSED; empty failed -> KILL;
# median failed rank>5 -> KILL; n_pop<12 -> UNDERDETERMINED;
# baseline>0.75 or tie-guard>0.25 -> HOLD; else TIER-0 PASSED.
import json, hashlib, os, sys, time, statistics, resource
import torch

sys.path.insert(0, "/home/hatch/workspace/SCBI/experiments/runs/EXP105_cloze_Tier0")
from exp105_lib import (correct_rank, top1_decision, token_id_rank_of_correct,
                        tier0_verdict)

BUNDLE = "/home/hatch/workspace/SCBI/experiments/runs/EXP105_cloze_Tier0"
SNAP = "/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
TOKFILE = BUNDLE + "/tokenizer_artifact/tokenizer.json"
SEED = 20260928
CUE = "The answer is"
ALT_CUE = "Answer:"
torch.manual_seed(SEED)
torch.set_num_threads(2)

manifest = json.load(open(BUNDLE + "/cloze_bench_manifest.json"))
items = manifest["items"]
assert len(items) == 60

# ---- G1 GATE: re-attestation against the pinned gpt-neox-20b artifact ----
# Provenance: the pinned artifact is the gpt-neox-20b main-branch tokenizer.json
# (sha256 c24618a1...), verified at run time byte-identical to the copy bundled
# in the frozen pythia-410m snapshot (SNAP/tokenizer.json). The tokenizer is
# loaded via AutoTokenizer.from_pretrained(SNAP) — the EXACT loading path used
# by EXP104's G1 probe and bench builder — because the snapshot's
# tokenizer_config.json (prefix-space handling etc.) is part of the scoring
# instrument. A bare tokenizer.json load without that config tokenizes
# differently and is NOT the instrument; using it would score with a different
# tokenizer than the manifest pools were built for.
from transformers import AutoTokenizer
exp_tok_sha = manifest["tokenizer_file_sha256"]
act_tok_sha = hashlib.sha256(open(TOKFILE, "rb").read()).hexdigest()
snap_tok_sha = hashlib.sha256(open(SNAP + "/tokenizer.json", "rb").read()).hexdigest()
assert act_tok_sha == exp_tok_sha, f"bundle tokenizer artifact drift: {act_tok_sha}"
assert snap_tok_sha == exp_tok_sha, f"snapshot tokenizer.json drift: {snap_tok_sha}"
tok = AutoTokenizer.from_pretrained(SNAP, trust_remote_code=False)
n_checked = 0
for it in items:
    tids = it["option_token_ids"]
    assert len(set(tids)) == 8, f"intra-item token collision on {it['item_id']}"
    for s, t in zip(it["options"], tids):
        # Leading-space operationalization (carried over from EXP104's G1 probe):
        # the scored token is the NEXT token after the cue, i.e. the completion
        # token with its leading space ("The answer is" + " France"). The
        # manifest pools were built as tok(" " + option).
        enc = tok(" " + s, add_special_tokens=False)["input_ids"]
        assert len(enc) == 1 and enc[0] == t, \
            f"G1 FAIL on {it['item_id']} {s!r}: {enc} vs {t}"
        n_checked += 1
print(f"G1 gate PASS: {n_checked}/480 single-token, ids match manifest, intra-item distinct")
g1_attestation = {
    "status": "PASS",
    "tokenizer_artifact": "EleutherAI/gpt-neox-20b",
    "tokenizer_revision": "main",
    "tokenizer_file_sha256": act_tok_sha,
    "tokenizer_load_path": "AutoTokenizer.from_pretrained(pythia-410m snapshot) — identical to EXP104 G1/bench loading path",
    "snapshot_tokenizer_json_sha256": snap_tok_sha,
    "n_strings": n_checked,
    "note": ("artifact fetched from hub at run time; byte-identical to pythia-410m "
             "snapshot copy (verified pre-run). Loading config comes from the "
             "snapshot's tokenizer_config.json, as in EXP104. Leading-space "
             "operationalization carried over from EXP104's G1 probe: the scored "
             "token is the next token after the cue, i.e. tok(' ' + option)."),
}

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

from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(SNAP, torch_dtype=torch.float32,
                                             trust_remote_code=False, low_cpu_mem_usage=True)
model.eval()
assert not model.training
print("model loaded; params:", sum(p.numel() for p in model.parameters()) / 1e6, "M")


def run_pass(prompt):
    enc = tok(prompt, add_special_tokens=False)["input_ids"]
    readout_index = len(enc)
    t0 = time.time()
    with torch.no_grad():
        out = model(torch.tensor([enc]))
    logits = out.logits[0, -1, :].float()  # float32; callers index only the 8 candidates
    return readout_index, logits, round(time.time() - t0, 1)


def candidate_logits8(logits_tensor, token_ids8):
    # float32 -> Python float widens without changing exact-equality relations
    return [float(logits_tensor[t]) for t in token_ids8]


def score_item(it, logits_tensor, readout_index, pass_seconds):
    tids = it["option_token_ids"]
    opts8 = candidate_logits8(logits_tensor, tids)
    top1 = top1_decision(opts8, tids)
    ci = it["correct_position"]
    r = correct_rank(opts8, ci, tids)
    mx = max(opts8)
    tied_at_top = (opts8[ci] == mx) and (sum(1 for v in opts8 if v == mx) >= 2)
    return {
        "item_id": it["item_id"], "arm": "B",
        "prompt_cue": CUE,
        "top1_idx": top1, "top1_option": it["options"][top1],
        "top1_token_id": tids[top1],
        "correct_position": ci, "correct_option": it["correct_option"],
        "correct_is_top1": top1 == ci,
        "correct_rank": r,
        "candidate_logits": opts8,
        "masked_token": None,
        "top1_minus_correct_margin": max(opts8) - opts8[ci],
        "correct_tied_at_top": tied_at_top,
        "token_id_rank_of_correct": token_id_rank_of_correct(ci, tids),
        "readout_index": readout_index,
        "pass_seconds": pass_seconds,
    }


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
    ri, cand_logits, secs = run_pass(it["prompt"])
    records[iid] = score_item(it, cand_logits, ri, secs)
    json.dump(list(records.values()), open(rec_path, "w"))
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    r = records[iid]
    print(f"{iid} rank={r['correct_rank']} top1={r['top1_option']!r} "
          f"{secs}s rss={rss:.2f}GB", flush=True)
print("all 60 cloze passes done in", round(time.time() - t_all, 1), "s")

# ---- Δθ=0 guard: weight-file hash post ----
hash_post = fhash(WFILE)
print("weight sha256 post:", hash_post)
assert hash_pre == hash_post, "WEIGHT HASH CHANGED — run void"


def evaluate(recs):
    failed = [r for r in recs if not r["correct_is_top1"]]
    ranks = [r["correct_rank"] for r in failed]
    n_pop = sum(1 for r in ranks if r <= 5)
    tie_numer = sum(1 for r in failed
                    if r["correct_rank"] <= 5 and r["correct_tied_at_top"])
    tie_rate = (tie_numer / n_pop) if n_pop else None
    acc = (60 - len(failed)) / 60
    verdict = tier0_verdict(acc, ranks, tie_rate if tie_rate is not None else 0.0)
    return {
        "baseline_accuracy": acc, "n_failed": len(failed),
        "median_correct_rank_failed": statistics.median(ranks) if ranks else None,
        "failed_ranks": ranks, "n_pop": n_pop,
        "tie_guard": {"numerator": tie_numer, "denominator": n_pop, "rate": tie_rate},
        "route": verdict,
    }


recs = [records[it["item_id"]] for it in items]
w = evaluate(recs)

# ---- Descriptive diagnostics (v2 sec 9 item 3) ----
# Per-template block table: manifest carries no explicit template labels;
# items are 10 consecutive 6-item stem-pattern blocks (derived, descriptive only).
blocks = {}
for i, it in enumerate(items):
    b = i // 6
    stem = it["question"].split("?", 1)[0][-60:]
    blocks.setdefault(b, {"stem_tail": stem, "n": 0, "correct": 0})
    blocks[b]["n"] += 1
    if records[it["item_id"]]["correct_is_top1"]:
        blocks[b]["correct"] += 1
w["per_template_blocks"] = {str(b): {"stem_tail": v["stem_tail"],
    "accuracy": v["correct"] / v["n"]} for b, v in blocks.items()}
# Top-1 collapse diagnostic: distribution of top-1 candidate token ids.
top1_counts = {}
for r in recs:
    top1_counts[r["top1_token_id"]] = top1_counts.get(r["top1_token_id"], 0) + 1
w["top1_token_distribution"] = {str(k): v for k, v in sorted(top1_counts.items())}
w["top1_distinct_tokens"] = len(top1_counts)
# Token-id-rank uniformity of the correct candidate (should be ~uniform 1..8).
tidr = [r["token_id_rank_of_correct"] for r in recs]
w["correct_token_id_rank_dist"] = {str(k): tidr.count(k) for k in range(1, 9)}
# Tie-event flags (float32 exact equality).
w["n_tie_events_all_items"] = sum(1 for r in recs if r["correct_tied_at_top"])
w["tie_events_correlate_with_token_id_rank"] = "n/a (0 events)" \
    if w["n_tie_events_all_items"] == 0 else "CHECK"

# ---- Pre-registered descriptive sensitivity: alt cue "Answer:" (v2 sec 2.3) ----
# Licensed ONLY if Tier-0 passes its gates. One line, descriptive, never a gate.
w["alt_cue_sensitivity"] = None
if w["route"] == "TIER-0 PASSED":
    alt_correct = 0
    for it in items:
        ri, logits_tensor, _ = run_pass(it["question"] + " " + ALT_CUE)
        tids = it["option_token_ids"]
        opts8 = candidate_logits8(logits_tensor, tids)
        if top1_decision(opts8, tids) == it["correct_position"]:
            alt_correct += 1
    w["alt_cue_sensitivity"] = {
        "cue": ALT_CUE,
        "baseline_accuracy": alt_correct / 60,
        "role": "descriptive only — not a gate, not a result",
    }
    print("alt-cue descriptive baseline:", w["alt_cue_sensitivity"]["baseline_accuracy"])

hash_post2 = fhash(WFILE)
assert hash_pre == hash_post2, "WEIGHT HASH CHANGED during alt-cue — void"

worksheet = {
    "experiment": "EXP105", "tier": "Tier-0", "format": "cloze",
    "cue_literal": CUE, "template_sha256": manifest["template_sha256"],
    "n_items": 60, "n_passes": 60,
    "g1_attestation": g1_attestation,
    "d3_blindness": manifest["d3_blindness"],
    **w,
    "delta_theta0": {"weight_sha256_pre": hash_pre,
                     "weight_sha256_post": hash_post2, "match": True},
    "seed": SEED,
    "torch": torch.__version__,
}
import transformers
worksheet["transformers"] = transformers.__version__
worksheet["script_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
json.dump(worksheet, open(BUNDLE + "/tier0_worksheet_exp105.json", "w"), indent=1)

# per_item_records.csv (v2 sec 9 item 1 — Tier-0 arm-B fields)
import csv
with open(BUNDLE + "/per_item_records.csv", "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["item_id", "arm", "cue", "top1_option", "top1_token_id",
                 "correct_option", "correct_is_top1", "correct_rank",
                 "top1_minus_correct_margin", "correct_tied_at_top",
                 "token_id_rank_of_correct", "readout_index", "pass_seconds"])
    for r in recs:
        wr.writerow([r["item_id"], r["arm"], r["prompt_cue"], r["top1_option"],
                     r["top1_token_id"], r["correct_option"], r["correct_is_top1"],
                     r["correct_rank"], round(r["top1_minus_correct_margin"], 6),
                     r["correct_tied_at_top"], r["token_id_rank_of_correct"],
                     r["readout_index"], r["pass_seconds"]])

print(json.dumps({k: w[k] for k in
      ["baseline_accuracy", "n_failed", "median_correct_rank_failed", "n_pop",
       "tie_guard", "route"]}, indent=1))
print("ROUTE:", w["route"])
