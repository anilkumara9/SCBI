"""EXP148 Step-0 dry-run gate — J7 first-token scoring repair (signed pre-reg LOG-4955,
independent verification SIGN LOG-4956, CEO execution authorization for Step-0 only).

Order per §5.4: (u0) scoring-pipeline unit test (zero forwards) -> (b) revision ->
load -> (a) pre-hash -> (h) throughput probe -> (c) bench pin -> exemplar/Law#7 ->
20-item dry-run subset (seed 148000, != 7101), B arm only, T_B=15, greedy,
first-token scoring -> guard (d) -> (a) post-hash.

Pass: B first-token accuracy in [0.2, 0.8] -> full run licensable (NOT executed here).
Fail: EXP148 STOPS at design cost. No verdict.
$0 CPU. ~300 generation forwards + 50-step probe (excluded from bench).
"""
import hashlib
import json
import os
import random
import re
import string
import sys
import time

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(RUN_DIR, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))
from reference_implementation import bench_sha256  # noqa: E402 (canonical pin fn)

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "EleutherAI/pythia-410m"
EXPECTED_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "2b055b53127a241b72338a82373c3efc7b666256e25d8c584d45989278c14dcf"
BENCH_PATH = os.path.expanduser(
    "~/workspace/SCBI/research/analysis_plans/S7-1_BENCH_2026-10-05.json")
PROMPTS_PATH = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP147/S7-1_PROMPTS_2026-10-05.json")

SUBSET_SEED = 148000  # registered at execution; != bench-construction seed 7101
TORCH_SEED = 148001
N_DRYRUN = 20

STEP0_JSON = os.path.join(RUN_DIR, "exp148_step0_dryrun_2026-10-06.json")
LOG_TXT = os.path.join(RUN_DIR, "exp148_step0_dryrun_2026-10-06.log")
JSONL = os.path.join(RUN_DIR, "exp148_dryrun_per_item.jsonl")

ANSWER_RE = re.compile(r"answer:", re.IGNORECASE)


def log(msg):
    line = "[step0] %s" % msg
    print(line, flush=True)
    with open(LOG_TXT, "a") as f:
        f.write(line + "\n")


def normalize(s):
    s = s.lower()
    s = s.translate(str.maketrans("", "", string.punctuation))
    return " ".join(s.split())


def score_b(generation, gold):
    """First-token scoring, B arm (§5.3.1)."""
    toks = normalize(generation).split()
    first = toks[0] if toks else ""
    return (1 if first == normalize(gold) else 0), first


def score_cs(generation, gold):
    """First-token scoring, C/S arms (§5.3.2): first token after LAST answer marker."""
    matches = list(ANSWER_RE.finditer(generation))
    if not matches:
        return 0, ""
    after = generation[matches[-1].end():]
    toks = normalize(after).split()
    first = toks[0] if toks else ""
    return (1 if first == normalize(gold) else 0), first


def unit_test_u0():
    """(u0) zero-forward scoring-pipeline unit test — 5 synthetic cases + B-arm sanity."""
    cases = [
        # (fn, generation, gold, expect_correct, expect_first, label)
        (score_cs, "Some reasoning here. ANSWER: Alice", "Alice", 1, "alice",
         "cs-a standard ANSWER:"),
        (score_cs, "Some reasoning. answer: Bob", "Bob", 1, "bob",
         "cs-b lowercase answer:"),
        (score_cs, "First ANSWER: wrong. Second ANSWER: Carol", "Carol", 1,
         "carol", "cs-c multiple markers last-wins"),
        (score_cs, "Reasoning. ANSWER: Dave and then he went home", "Dave", 1,
         "dave", "cs-d trailing ramble"),
        (score_cs, "Just some text without any marker", "Eve", 0, "",
         "cs-e missing marker -> 0"),
        (score_cs, "ANSWER: Frank", "Grace", 0, "frank",
         "cs-f wrong name -> 0"),
        (score_b, "Alice went to the store", "Alice", 1, "alice",
         "b-a first token match"),
        (score_b, "The answer is Alice", "Alice", 0, "the",
         "b-b first token mismatch"),
        (score_b, "", "Alice", 0, "", "b-c empty generation -> 0"),
    ]
    failures = []
    for fn, gen, gold, exp_c, exp_f, label in cases:
        got_c, got_f = fn(gen, gold)
        if (got_c, got_f) != (exp_c, exp_f):
            failures.append(
                {"case": label, "expected": (exp_c, exp_f),
                 "got": (got_c, got_f)})
    return failures


def sha256_state_dict(model):
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu()
        if t.dtype != torch.float32:
            t = t.float()
        h.update(t.numpy().tobytes())
    return h.hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def build_prompt(prompts, arm, item):
    t = prompts["arms"][arm]["template"]
    shots = "".join(prompts["shots"][arm])
    facts = " ".join(item["facts"])
    return t.replace("{shots}", shots).replace("{facts}", facts).replace(
        "{question}", item["question"])


def main():
    rec = {"guards": {}, "experiment": "EXP148", "lane": "step0-dryrun",
           "log": "LOG-4957"}
    torch.manual_seed(TORCH_SEED)

    # ---- (u0) scoring-pipeline unit test: ZERO forwards ----
    failures = unit_test_u0()
    rec["u0_failures"] = failures
    rec["guards"]["u0_scoring_pipeline"] = (len(failures) == 0)
    log(f"(u0) unit test: {9 - len(failures)}/9 cases pass")
    if failures:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "guard (u0): scoring-pipeline unit test failed"
        for fl in failures:
            log(f"(u0) FAIL {fl['case']}: expected {fl['expected']} "
                f"got {fl['got']}")
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: guard (u0) — STOP, no forwards run")
        sys.exit(2)
    log("(u0) PASS — scoring pipeline sound, proceeding")

    # ---- (b) model revision: resolve programmatically from the HF cache ----
    snap_dir = os.path.expanduser(
        "~/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots")
    revs = sorted(os.listdir(snap_dir))
    assert len(revs) == 1, f"expected 1 cached snapshot, got {revs}"
    actual_rev = revs[0]
    rec["model_revision_actual"] = actual_rev
    rec["model_revision_expected"] = EXPECTED_REVISION
    rec["guards"]["b_revision_match"] = (actual_rev == EXPECTED_REVISION)
    log(f"(b) revision actual={actual_rev} match={rec['guards']['b_revision_match']}")
    if not rec["guards"]["b_revision_match"]:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "guard (b): revision mismatch"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: guard (b)")
        sys.exit(2)

    # ---- load ----
    log("loading tokenizer + model (eager, fp32, cpu)")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=actual_rev, local_files_only=True,
        trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, revision=actual_rev, local_files_only=True,
        torch_dtype=torch.float32, device_map="cpu",
        attn_implementation="eager", trust_remote_code=False)
    model.eval()
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    rec["torch"] = torch.__version__
    import transformers as _tf
    rec["transformers"] = _tf.__version__
    import numpy as _np
    rec["numpy"] = _np.__version__
    rec["threads"] = torch.get_num_threads()
    log(f"env: torch={rec['torch']} transformers={rec['transformers']} "
        f"numpy={rec['numpy']} threads={rec['threads']}")

    # ---- (a) Δθ=0 pre-hash ----
    pre_hash = sha256_state_dict(model)
    rec["backbone_pre_hash"] = pre_hash
    rec["guards"]["a_prehash_match"] = (pre_hash == BACKBONE_PIN)
    log(f"(a) pre-hash={pre_hash} match={rec['guards']['a_prehash_match']}")
    if not rec["guards"]["a_prehash_match"]:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "guard (a): pre-hash mismatch"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: guard (a)")
        sys.exit(2)

    # ---- (h) throughput probe: 50 generation steps, fixed dummy prompt ----
    dummy = ("The quick brown fox jumps over the lazy dog. " * 6).strip()
    inp = tokenizer(dummy, return_tensors="pt")
    n_steps = 50
    t0 = time.time()
    with torch.no_grad():
        out = model.generate(inp["input_ids"], max_new_tokens=n_steps,
                             do_sample=False,
                             pad_token_id=tokenizer.eos_token_id)
    dt = time.time() - t0
    new_toks = out.shape[1] - inp["input_ids"].shape[1]
    tok_s = new_toks / dt
    projected_h = (46000 / tok_s) / 3600
    rec["throughput_probe"] = {
        "dummy_new_tokens": new_toks, "seconds": round(dt, 2),
        "tok_per_s": round(tok_s, 3),
        "projected_hours_46k": round(projected_h, 2),
    }
    rec["guards"]["h_compute_feasible"] = projected_h <= 72
    log(f"(h) probe: {new_toks} toks in {dt:.1f}s = {tok_s:.2f} tok/s; "
        f"46k projected {projected_h:.2f}h (cap 72h) "
        f"feasible={rec['guards']['h_compute_feasible']}")
    if not rec["guards"]["h_compute_feasible"]:
        rec["outcome"] = "INCONCLUSIVE"
        rec["reason"] = "guard (h): projected > 72h (compute-infeasible)"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("INCONCLUSIVE: guard (h) — STOP, no GPU escalation")
        sys.exit(3)

    # ---- (c) bench pin: recompute character-identical ----
    with open(BENCH_PATH) as f:
        bench = json.load(f)
    pin = bench_sha256(bench)
    char_match = len(pin) == 64 and all(a == b for a, b in zip(pin, BENCH_PIN))
    rec["bench_pin_recomputed"] = pin
    rec["guards"]["c_bench_pin_match"] = (pin == BENCH_PIN and char_match)
    log(f"(c) bench pin recomputed={pin} match={rec['guards']['c_bench_pin_match']}")
    if not rec["guards"]["c_bench_pin_match"]:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "guard (c): bench pin mismatch"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: guard (c)")
        sys.exit(2)

    # ---- exemplars: reuse EXP147's Step-0-pinned file byte-identical ----
    assert os.path.exists(PROMPTS_PATH), f"prompts file missing: {PROMPTS_PATH}"
    rec["prompts_sha256"] = sha256_file(PROMPTS_PATH)
    with open(PROMPTS_PATH) as f:
        prompts = json.load(f)
    log(f"exemplars: reusing {PROMPTS_PATH} "
        f"(sha256={rec['prompts_sha256'][:16]}...)")

    # Law #7: exemplar entities disjoint from bench entities (re-assert)
    bench_ents = set()
    for it in bench:
        for f_ in it["facts"]:
            bench_ents.update(w.strip(string.punctuation) for w in f_.split())
    ex_ents = set(prompts["exemplar_entities"])
    law7_ok = not (bench_ents & ex_ents)
    rec["guards"]["law7_disjoint"] = law7_ok
    log(f"Law #7 exemplar/bench entity disjointness "
        f"{'PASS' if law7_ok else 'FAIL'}")
    if not law7_ok:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "Law #7: exemplar/bench entity overlap"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: Law #7")
        sys.exit(2)

    # ---- dry-run subset: fresh 20 items, seed 148000 (!= 7101) ----
    assert SUBSET_SEED != 7101
    rng = random.Random(SUBSET_SEED)
    subset = rng.sample(bench, N_DRYRUN)
    rec["subset_seed"] = SUBSET_SEED
    rec["subset_ids"] = [it["id"] for it in subset]
    rec["subset_strata"] = [it["stratum"] for it in subset]
    log(f"dry-run subset: seed={SUBSET_SEED}, n={N_DRYRUN}, "
        f"ids={rec['subset_ids']}")

    # ---- B arm only, T_B=15, greedy, first-token scoring ----
    budget = prompts["arms"]["B"]["budget_tokens"]
    assert budget == 15, f"B budget changed: {budget}"
    t_start = time.time()
    n_correct = 0
    total_new_tokens = 0
    with open(JSONL, "w") as jf:
        for it in subset:
            prompt = build_prompt(prompts, "B", it)
            inp2 = tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                out2 = model.generate(
                    inp2["input_ids"], max_new_tokens=budget,
                    do_sample=False, pad_token_id=tokenizer.eos_token_id)
            new_ids = out2[0][inp2["input_ids"].shape[1]:]
            generation = tokenizer.decode(new_ids, skip_special_tokens=True)
            correct, first_tok = score_b(generation, it["gold"])
            n_correct += correct
            total_new_tokens += int(len(new_ids))
            jrec = {
                "item_id": it["id"], "stratum": it["stratum"], "arm": "B",
                "gold": it["gold"], "generation": generation,
                "first_token": first_tok, "correct": correct,
                "n_new_tokens": int(len(new_ids)),
                "n_prompt_tokens": int(inp2["input_ids"].shape[1]),
            }
            jf.write(json.dumps(jrec) + "\n")
            jf.flush()
            os.fsync(jf.fileno())
    rec["dryrun_seconds"] = round(time.time() - t_start, 1)
    rec["dryrun_generation_forwards"] = total_new_tokens
    log(f"dry-run: 20 B-arm items complete, "
        f"{total_new_tokens} generation forwards in {rec['dryrun_seconds']}s")

    # ---- guard (d): first-token B accuracy in [0.2, 0.8] ----
    b_acc = n_correct / N_DRYRUN
    rec["b_first_token_accuracy"] = round(b_acc, 4)
    rec["b_correct"] = n_correct
    rec["guards"]["d_calibration"] = (0.2 <= b_acc <= 0.8)
    log(f"guard (d): B first-token accuracy = {n_correct}/{N_DRYRUN} = "
        f"{b_acc:.4f} (bar [0.2, 0.8]) "
        f"-> {'PASS' if rec['guards']['d_calibration'] else 'FAIL'}")

    # ---- (a) post-hash ----
    post_hash = sha256_state_dict(model)
    rec["backbone_post_hash"] = post_hash
    rec["guards"]["a_posthash_match"] = (post_hash == BACKBONE_PIN)
    log(f"(a) post-hash match: {rec['guards']['a_posthash_match']}")
    if not rec["guards"]["a_posthash_match"]:
        rec["outcome"] = "RUN-INVALID"
        rec["reason"] = "guard (a): post-hash mismatch (Δθ≠0)"
        json.dump(rec, open(STEP0_JSON, "w"), indent=1)
        log("RUN-INVALID: guard (a) post-hash")
        sys.exit(2)

    # ---- gate verdict ----
    if rec["guards"]["d_calibration"]:
        rec["outcome"] = "DRYRUN_PASS"
        rec["consequence"] = ("Full EXP148 run licensable (pending CEO "
                              "execution authorization as a separate lane). "
                              "This lane does NOT execute it.")
    else:
        rec["outcome"] = "DRYRUN_FAIL_STOP"
        rec["consequence"] = ("EXP148 STOPS at design cost. No full run, "
                              "no verdict. Repair (c) (instruct-tuned model) "
                              "becomes the next candidate proposal.")
    rec["total_forwards"] = total_new_tokens + 50  # dry-run + probe
    json.dump(rec, open(STEP0_JSON, "w"), indent=1)
    log(f"dry-run complete: outcome={rec['outcome']} "
        f"accuracy={b_acc:.4f} forwards~{rec['total_forwards']}")


if __name__ == "__main__":
    main()
