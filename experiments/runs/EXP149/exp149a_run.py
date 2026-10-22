"""EXP149 study (a) full run — hop dose-response on frozen Pythia-410m.

Signed pre-reg EXP149_PREREG_DRAFT_2026-10-09.md (Law #14 SIGN-WITH-FIXES
repaired; CEO sign + execution authorization LOG-4968). Fresh bench
(EXP149A_BENCH_2026-10-09.json, pin a4275c8c7996006096c715c5399d0019844ded8aaff663c0359ead202bc27f67).

Sequence: (u0) -> revision/hash/pin -> throughput probe (h) + 4-hop trigger ->
B dry run (d-gate) -> C+S pilot (power rule, n-raise) -> full run (d_block1
keying) -> guards -> verdict per §4a. Greedy, Δθ=0, $0 CPU. Resumable JSONL.
"""
import hashlib
import json
import math
import os
import random
import re
import string
import sys
import time

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(RUN_DIR, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))
from reference_implementation import bench_sha256  # noqa: E402

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "EleutherAI/pythia-410m"
CACHE_DIR = os.path.expanduser("~/.cache/huggingface")
REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "a4275c8c7996006096c715c5399d0019844ded8aaff663c0359ead202bc27f67"

BENCH_PATH = os.path.join(RUN_DIR, "EXP149A_BENCH_2026-10-09.json")
PROMPTS_PATH = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP147/S7-1_PROMPTS_2026-10-05.json")
JSONL = os.path.join(RUN_DIR, "exp149a_per_item.jsonl")
RUNLOG = os.path.join(RUN_DIR, "exp149a_run.log")
SUMMARY = os.path.join(RUN_DIR, "exp149a_run_summary.json")

TORCH_SEED = 149004  # registered at execution
DRYRUN_SEED = 149002  # B dry-run 20-item subset (≠ construction 149001)
PILOT_SEED = 149003  # C+S pilot 20-item subset (≠ 149001, ≠ 149002)
REBUILD4HOP_SEED = 149009  # 4-hop bench construction seed (if trigger fires)

DESIGN_N = 380  # per hop level
WRITE_RE = re.compile(r'WRITE\(fact\d+,')
ANSWER_RE = re.compile(r"answer:", re.IGNORECASE)


def log(msg):
    line = "[run-a] %s" % msg
    print(line, flush=True)
    with open(RUNLOG, "a") as f:
        f.write(line + "\n")


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


def normalize(s):
    s = s.lower()
    s = s.translate(str.maketrans("", "", string.punctuation))
    return " ".join(s.split())


def score_b(generation, gold):
    toks = normalize(generation).split()
    first = toks[0] if toks else ""
    return (1 if first == normalize(gold) else 0), first


def score_cs(generation, gold):
    matches = list(ANSWER_RE.finditer(generation))
    if not matches:
        return 0, ""
    after = generation[matches[-1].end():]
    toks = normalize(after).split()
    first = toks[0] if toks else ""
    return (1 if first == normalize(gold) else 0), first


def unit_test_u0():
    cases = [
        (score_cs, "Some reasoning here. ANSWER: Zorp", "Zorp", 1, "zorp",
         "cs-a standard ANSWER:"),
        (score_cs, "Some reasoning. answer: Blip", "Blip", 1, "blip",
         "cs-b lowercase answer:"),
        (score_cs, "First ANSWER: wrong. Second ANSWER: Fweep", "Fweep", 1,
         "fweep", "cs-c multiple markers last-wins"),
        (score_cs, "Reasoning. ANSWER: Quix and then more", "Quix", 1,
         "quix", "cs-d trailing ramble"),
        (score_cs, "Just some text without any marker", "Vorn", 0, "",
         "cs-e missing marker -> 0"),
        (score_cs, "ANSWER: Jalp", "Trun", 0, "jalp",
         "cs-f wrong name -> 0"),
        (score_b, "Zorp went home", "Zorp", 1, "zorp",
         "b-a first token match"),
        (score_b, "The answer is Blip", "Blip", 0, "the",
         "b-b first token mismatch"),
        (score_b, "", "Fweep", 0, "", "b-c empty generation -> 0"),
    ]
    failures = []
    for fn, gen, gold, exp_c, exp_f, label in cases:
        got_c, got_f = fn(gen, gold)
        if (got_c, got_f) != (exp_c, exp_f):
            failures.append({"case": label, "expected": (exp_c, exp_f),
                             "got": (got_c, got_f)})
    return failures


def build_prompt(prompts, arm, item):
    t = prompts["arms"][arm]["template"]
    shots = "".join(prompts["shots"][arm])
    facts = " ".join(item["facts"])
    return t.replace("{shots}", shots).replace("{facts}", facts).replace(
        "{question}", item["question"])


def load_done():
    done = set()
    if os.path.exists(JSONL):
        with open(JSONL) as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    done.add((r["item_id"], r["arm"]))
    return done


def fresh_subset(bench, k, seed):
    rng = random.Random(seed)
    idx = rng.sample(range(len(bench)), k)
    return [bench[i] for i in idx]


def wald_power(d, n):
    """Registered Wald-formula power for δ=+0.10, one-sided α=0.05."""
    se = math.sqrt(max(d - 0.01, 1e-9) * (2.0 / n))
    z = 0.10 / se - 1.645
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0))), se


def n_for_power(d, target=0.80):
    """Smallest even integer n with registered power ≥ target."""
    n = 2
    while n <= 2000:
        p, _ = wald_power(d, n)
        if p >= target:
            return n
        n += 2
    return None


def main():
    t_start = time.time()
    torch.manual_seed(TORCH_SEED)
    summary = {"experiment": "EXP149", "study": "a",
               "log": "LOG-4968", "torch_seed": TORCH_SEED, "guards": {},
               "dryrun_seed": DRYRUN_SEED, "pilot_seed": PILOT_SEED}

    # ---- (u0) ----
    failures = unit_test_u0()
    summary["guards"]["u0_scoring_pipeline"] = (len(failures) == 0)
    log(f"(u0) unit test: {9 - len(failures)}/9 pass")
    if failures:
        summary["outcome"] = "RUN-INVALID"
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        sys.exit(2)
    log("(u0) PASS")

    # ---- (b) revision ----
    snap_dir = os.path.join(CACHE_DIR, "hub",
                            "models--EleutherAI--pythia-410m", "snapshots")
    revs = sorted(os.listdir(snap_dir))
    assert len(revs) == 1, f"expected 1 cached snapshot, got {revs}"
    actual_rev = revs[0]
    summary["guards"]["b_revision_match"] = (actual_rev == REVISION)
    log(f"(b) revision match: {summary['guards']['b_revision_match']}")
    if not summary["guards"]["b_revision_match"]:
        summary["outcome"] = "RUN-INVALID"
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        sys.exit(2)

    # ---- load ----
    # Load directly from the verified snapshot directory (bypasses hub
    # resolution; the (b) guard above verified the snapshot dir == REVISION).
    SNAPSHOT_PATH = os.path.join(
        CACHE_DIR, "hub", "models--EleutherAI--pythia-410m", "snapshots",
        actual_rev)
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    log("loading Pythia-410m tokenizer + model (eager, fp32, cpu, local snapshot)")
    tokenizer = AutoTokenizer.from_pretrained(
        SNAPSHOT_PATH, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        SNAPSHOT_PATH, local_files_only=True,
        torch_dtype=torch.float32, device_map="cpu",
        attn_implementation="eager", trust_remote_code=False)
    model.eval()
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    import transformers as _tf
    import numpy as _np
    summary["env"] = {"torch": torch.__version__,
                      "transformers": _tf.__version__,
                      "numpy": _np.__version__,
                      "threads": torch.get_num_threads()}

    # ---- (a) pre-hash ----
    pre_hash = sha256_state_dict(model)
    summary["guards"]["a_prehash_match"] = (pre_hash == BACKBONE_PIN)
    log(f"(a) pre-hash match: {summary['guards']['a_prehash_match']}")
    assert summary["guards"]["a_prehash_match"], "(a) pre-hash mismatch"

    # ---- (c) bench pin ----
    with open(BENCH_PATH) as f:
        bench = json.load(f)
    pin = bench_sha256(bench)
    char_match = len(pin) == 64 and all(a == b for a, b in zip(pin, BENCH_PIN))
    summary["guards"]["c_bench_pin_match"] = (pin == BENCH_PIN and char_match)
    summary["bench_pin"] = pin
    log(f"(c) bench pin match: {summary['guards']['c_bench_pin_match']} "
        f"({len(bench)} items)")
    assert summary["guards"]["c_bench_pin_match"], "(c) bench pin mismatch"

    # ---- exemplars byte-identical; Law #7 ----
    assert os.path.exists(PROMPTS_PATH), f"prompts missing: {PROMPTS_PATH}"
    summary["prompts_sha256"] = sha256_file(PROMPTS_PATH)
    with open(PROMPTS_PATH) as f:
        prompts = json.load(f)
    bench_ents = set()
    for it in bench:
        for f_ in it["facts"]:
            bench_ents.update(w.strip(string.punctuation) for w in f_.split())
    ex_ents = set(prompts["exemplar_entities"])
    summary["guards"]["law7_disjoint"] = not (bench_ents & ex_ents)
    log(f"Law #7 disjointness: {summary['guards']['law7_disjoint']}")
    assert summary["guards"]["law7_disjoint"], "Law #7 overlap"

    def gen(item, arm, budget=None):
        b = budget if budget is not None else prompts["arms"][arm]["budget_tokens"]
        prompt = build_prompt(prompts, arm, item)
        inp = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            out = model.generate(
                inp["input_ids"], max_new_tokens=b,
                do_sample=False, pad_token_id=tokenizer.eos_token_id)
        new_ids = out[0][inp["input_ids"].shape[1]:]
        generation = tokenizer.decode(new_ids, skip_special_tokens=True)
        return generation, int(len(new_ids))

    # ---- (h) throughput probe: 50 generation steps, fixed dummy prompt ----
    probe_prompt = "The quick brown fox jumps over the lazy dog. " * 10
    inp = tokenizer(probe_prompt, return_tensors="pt")
    t0 = time.time()
    with torch.no_grad():
        out = model.generate(inp["input_ids"], max_new_tokens=50,
                             do_sample=False,
                             pad_token_id=tokenizer.eos_token_id)
    probe_secs = time.time() - t0
    sec_per_tok = probe_secs / 50.0
    # project the 2-level design run: 2*380 items x 3 arms
    design_new = 2 * DESIGN_N * (15 + 120 + 120)
    proj_h = design_new * sec_per_tok / 3600.0
    summary["throughput_probe"] = {"sec_per_token": round(sec_per_tok, 4),
                                   "projected_design_hours": round(proj_h, 2)}
    summary["guards"]["h_compute_gate"] = proj_h <= 72.0
    log(f"(h) probe: {sec_per_tok:.3f}s/tok; 2-level design projects "
        f"{proj_h:.2f}h (cap 72h) -> {'PASS' if proj_h <= 72 else 'INCONCLUSIVE'}")
    if proj_h > 72.0:
        summary["outcome"] = "INCONCLUSIVE"
        summary["reason"] = "guard (h): compute-infeasible"
        summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        log("INCONCLUSIVE: guard (h)")
        return

    # ---- 4-hop trigger: 2-level run ≤ 48h wall? AND guard (g) headroom? ----
    trigger_48h = proj_h <= 48.0
    # 4-hop would add 380 items x 255 = 96.9k; (g) is a hard cap on study (a)
    fourhop_new = DESIGN_N * (15 + 120 + 120)
    fourhop_ok_g = (198900 + fourhop_new) <= 200000
    admit_4hop = trigger_48h and fourhop_ok_g
    summary["fourhop_trigger"] = {"h48_pass": trigger_48h,
                                  "g_headroom_pass": fourhop_ok_g,
                                  "admitted": admit_4hop}
    log(f"4-hop trigger: (h)≤48h={trigger_48h}; (g) headroom={fourhop_ok_g} "
        f"-> {'ADMITTED' if admit_4hop else 'NOT BUILT (omission logged)'}")
    if trigger_48h and not fourhop_ok_g:
        log("4-hop NOT built: admitting it would breach guard (g) ≤ 200k "
            "(registered cap outranks the exploratory trigger)")

    # ---- (d) dry run: fresh 20-item subset, B arm only ----
    dry_items = fresh_subset(bench, 20, DRYRUN_SEED)
    dry_corr = 0
    dry_tok = 0
    for it in dry_items:
        generation, n_new = gen(it, "B")
        c, _ = score_b(generation, it["gold"])
        dry_corr += c
        dry_tok += n_new
    dry_acc = dry_corr / 20
    summary["dryrun"] = {"b_accuracy": round(dry_acc, 4),
                         "forwards": dry_tok}
    summary["guards"]["d_dryrun_pass"] = (0.2 <= dry_acc <= 0.8)
    log(f"(d) dry run B accuracy = {dry_acc:.4f} (bar [0.2,0.8]) -> "
        f"{'PASS' if 0.2 <= dry_acc <= 0.8 else 'STOP'}")
    if not (0.2 <= dry_acc <= 0.8):
        summary["outcome"] = "HELD"
        summary["reason"] = f"dry-run gate (d): B accuracy {dry_acc:.4f}"
        summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        log("HELD: dry-run gate")
        return

    # ---- C+S pilot: fresh 20-item subset (≠ dry-run), C and S arms ----
    pilot_items = fresh_subset(bench, 20, PILOT_SEED)
    pilot_ids = {it["id"] for it in pilot_items}
    assert not (pilot_ids & {it["id"] for it in dry_items}), "pilot/dry overlap"
    pilot_recs = []
    pilot_tok = 0
    for it in pilot_items:
        for arm in ("C", "S"):
            generation, n_new = gen(it, arm)
            c, _ = score_cs(generation, it["gold"])
            pilot_recs.append((it["id"], arm, c))
            pilot_tok += n_new
    by_id = {}
    for iid, arm, c in pilot_recs:
        by_id.setdefault(iid, {})[arm] = c
    b_p = sum(1 for v in by_id.values() if v["C"] != v["S"])
    d_pilot = b_p / 20.0
    summary["pilot"] = {"d_pilot": round(d_pilot, 4), "forwards": pilot_tok}
    log(f"C+S pilot: d_pilot = {d_pilot:.4f} (discordant {b_p}/20)")

    # ---- registered power rule + n-raise ----
    power, se = wald_power(d_pilot, DESIGN_N)
    n_level = DESIGN_N
    if power < 0.80:
        n_new = n_for_power(d_pilot)
        log(f"power {power:.3f} < 0.80 -> n-raise to {n_new} (pilot d={d_pilot:.4f})")
        n_level = n_new
    else:
        log(f"power {power:.3f} ≥ 0.80 -> n stays {DESIGN_N}")
    summary["power_rule"] = {"d_src": round(d_pilot, 4), "power": round(power, 4),
                             "n_per_level": n_level}
    # bench-size feasibility: bench has 380/level
    if n_level > 380:
        # re-assert (g)/(h) at raised n; bench cannot supply >380/level
        raise_new = 2 * n_level * 255
        raise_h = raise_new * sec_per_tok / 3600.0
        if raise_new > 200000 or raise_h > 72.0 or n_level > 380:
            summary["outcome"] = "HELD"
            summary["reason"] = (f"n-raise to {n_level}/level infeasible "
                                 f"(bench 380/level; (g)/(h) re-assertion) — "
                                 "STOP at design cost")
            summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
            json.dump(summary, open(SUMMARY, "w"), indent=1)
            log("HELD: n-raise infeasible (bench/(g)/(h))")
            return
    # n stays within bench: use first n_level items per level
    assert n_level <= 380
    log(f"n_per_level = {n_level} (bench supports 380)")

    # ---- full run, level by level, with d_block1 keying ----
    levels = {"2hop": [it for it in bench if "2hop" in it["stratum"]][:n_level],
              "3hop": [it for it in bench if "3hop" in it["stratum"]][:n_level]}
    assert all(len(v) == n_level for v in levels.values())
    done = load_done()
    log(f"resuming: {len(done)} (item, arm) pairs already done")

    def run_item_arm(it, arm):
        generation, n_tok = gen(it, arm)
        scorer = score_b if arm == "B" else score_cs
        correct, first_tok = scorer(generation, it["gold"])
        rec = {"item_id": it["id"], "stratum": it["stratum"], "arm": arm,
               "gold": it["gold"], "generation": generation,
               "first_token": first_tok, "correct": correct,
               "n_new_tokens": n_tok}
        with open(JSONL, "a") as f:
            f.write(json.dumps(rec) + "\n")
            f.flush()
            os.fsync(f.fileno())
        done.add((it["id"], arm))
        return n_tok

    # B arm first (per-level guard (d))
    for lvl, items in levels.items():
        for it in items:
            if (it["id"], "B") not in done:
                run_item_arm(it, "B")
        log(f"B arm complete for {lvl} ({n_level} items)")
    b_recs = {}
    for lvl in levels:
        ids = {it["id"] for it in levels[lvl]}
        rs = [json.loads(l) for l in open(JSONL)
              if json.loads(l)["arm"] == "B" and json.loads(l)["item_id"] in ids]
        assert len(rs) == n_level, f"B {lvl} incomplete: {len(rs)}/{n_level}"
        acc = sum(r["correct"] for r in rs) / len(rs)
        b_recs[lvl] = acc
    summary["b_accuracy_per_level"] = {k: round(v, 4) for k, v in b_recs.items()}
    d_pass = all(0.2 <= v <= 0.8 for v in b_recs.values())
    summary["guards"]["d_calibration_per_level"] = d_pass
    log(f"guard (d) per level: {summary['b_accuracy_per_level']} -> "
        f"{'PASS' if d_pass else 'HELD'}")
    if not d_pass:
        summary["outcome"] = "HELD"
        summary["reason"] = f"guard (d): per-level B accuracy {b_recs}"
        post_hash = sha256_state_dict(model)
        summary["guards"]["a_posthash_match"] = (post_hash == BACKBONE_PIN)
        summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        log("HELD: guard (d)")
        return

    # C+S block 1 per level (20 items each) for d_block1 keying
    block_recs = {}
    for lvl, items in levels.items():
        blk = items[:20]
        for it in blk:
            for arm in ("C", "S"):
                if (it["id"], arm) not in done:
                    run_item_arm(it, arm)
        cs = {}
        for it in blk:
            cs[it["id"]] = {}
        for line in open(JSONL):
            r = json.loads(line)
            if r["item_id"] in cs and r["arm"] in ("C", "S"):
                cs[r["item_id"]][r["arm"]] = r["correct"]
        b_h = sum(1 for v in cs.values()
                  if len(v) == 2 and v["C"] != v["S"])
        block_recs[lvl] = b_h / 20.0
        log(f"d_block1[{lvl}] = {block_recs[lvl]:.4f}")
    d_max = max(block_recs.values())
    n_blk = n_for_power(d_max)
    if n_blk > n_level:
        log(f"d_block1 keying: d_max={d_max:.4f} implies n={n_blk} > {n_level} "
            "-> raising (computation, not a choice)")
        n_level = n_blk
        # re-assert (g)/(h) and bench feasibility
        raise_new = 2 * n_level * 255
        raise_h = raise_new * sec_per_tok / 3600.0
        summary["block_keying"] = {"d_max": round(d_max, 4),
                                   "n_raised": n_level,
                                   "forwards": raise_new,
                                   "hours": round(raise_h, 2)}
        if raise_new > 200000 or raise_h > 72.0 or n_level > 380:
            summary["outcome"] = "HELD"
            summary["reason"] = (f"d_block1 n-raise to {n_level}/level infeasible "
                                 "— STOP at design cost")
            summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
            json.dump(summary, open(SUMMARY, "w"), indent=1)
            log("HELD: d_block1 n-raise infeasible")
            return
        # extend levels to raised n
        levels = {"2hop": [it for it in bench if "2hop" in it["stratum"]][:n_level],
                  "3hop": [it for it in bench if "3hop" in it["stratum"]][:n_level]}
    else:
        summary["block_keying"] = {"d_max": round(d_max, 4),
                                   "n_raised": None}
        log(f"d_block1 keying: d_max={d_max:.4f} implies n={n_blk} ≤ {n_level} "
            "-> no raise")
    summary["n_per_level_final"] = n_level

    # complete remaining C/S items
    for lvl, items in levels.items():
        for it in items:
            for arm in ("C", "S"):
                if (it["id"], arm) not in done:
                    run_item_arm(it, arm)
        log(f"C/S complete for {lvl} ({n_level} items)")

    # ---- guards (e), (f), (f'), (g); post-hash ----
    recs = [json.loads(l) for l in open(JSONL)]
    per_lvl = {}
    for lvl, items in levels.items():
        ids = {it["id"] for it in items}
        by_arm = {}
        for r in recs:
            if r["item_id"] in ids:
                by_arm.setdefault(r["arm"], []).append(r)
        for a in ("B", "C", "S"):
            assert len(by_arm.get(a, [])) == n_level, f"{lvl}/{a} incomplete"
        per_lvl[lvl] = by_arm
    mean_tok = {}
    e_rates = {}
    fp = {}
    for lvl, by_arm in per_lvl.items():
        mt = {a: sum(r["n_new_tokens"] for r in rs) / len(rs)
              for a, rs in by_arm.items()}
        mean_tok[lvl] = mt
        sw = sum(1 for r in by_arm["S"] if WRITE_RE.search(r["generation"]))
        e_rates[lvl] = sw / len(by_arm["S"])
        fp[lvl] = (mt["S"] / mt["C"]) if mt["C"] > 0 else float("inf")
    summary["mean_tokens_per_level"] = {
        k: {a: round(v, 2) for a, v in v.items()} for k, v in mean_tok.items()}
    summary["guards"]["e_discipline_rate"] = {k: round(v, 4)
                                              for k, v in e_rates.items()}
    e_pass = all(v >= 0.5 for v in e_rates.values())
    summary["guards"]["e_discipline_pass"] = e_pass
    f_pass = all(mt["C"] > 2 * mt["B"] and mt["S"] > 2 * mt["B"]
                 for mt in mean_tok.values())
    summary["guards"]["f_compute_delivered"] = f_pass
    fp_pass = all((2 / 3) <= r <= (3 / 2) for r in fp.values())
    summary["token_ratio_S_C"] = {k: round(v, 4) for k, v in fp.items()}
    summary["guards"]["fp_comparability_per_level"] = fp_pass

    total_gen = (sum(r["n_new_tokens"] for r in recs) + dry_tok + pilot_tok)
    summary["total_generation_forwards"] = total_gen
    summary["guards"]["g_budget"] = total_gen <= 200000
    log(f"guard (g): {total_gen} forwards (cap 200000, incl. dry-run+pilot)")

    post_hash = sha256_state_dict(model)
    summary["guards"]["a_posthash_match"] = (post_hash == BACKBONE_PIN)
    summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
    json.dump(summary, open(SUMMARY, "w"), indent=1)

    if not e_pass:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (e): discipline not delivered"
    elif not f_pass:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (f): compute not delivered"
    elif not summary["guards"]["g_budget"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (g): budget exceeded"
    elif not summary["guards"]["a_posthash_match"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (a): Δθ≠0"
    else:
        summary["outcome"] = "PROCEED_TO_VERDICT"
        if not fp_pass:
            summary["fp_note"] = "guard (f') tripped -> HELD (attribution compromised)"
    json.dump(summary, open(SUMMARY, "w"), indent=1)
    log(f"run complete: outcome={summary['outcome']} "
        f"elapsed={summary['elapsed_hours']}h forwards={total_gen}")


if __name__ == "__main__":
    main()
