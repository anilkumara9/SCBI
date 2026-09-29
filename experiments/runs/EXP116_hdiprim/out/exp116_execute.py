#!/usr/bin/env python3
"""EXP116 (H10/HDI-PRIM) executor — executes EXACTLY per
research/prereg/EXP_PREREG_H10_HDIPRIM_2026-09-29.md (Law #14 SIGN, LOG-4601).

$0 CPU. Read-only on signed artifacts. No push, no GPU, no weights touched.
Any HALT / RUN-INVALID precondition -> STOP, report evidence, no metric read.
"""
import hashlib, json, os, sys, time, traceback

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ------------------------------------------------------------ pins ----
PIN_BENCH = "e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5"
PIN_DECISIONS = "f8133f1f4dc6f302cb7fdbe4dee248f9eb5ab97afab00c7fbc7b331e1a804625"
PIN_BACKBONE = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
SNAPSHOT = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
RUNS = os.path.expanduser("~/workspace/SCBI/experiments/runs")
OUTDIR = os.path.join(RUNS, "EXP116_hdiprim", "out")
N = 60
G1_BAR = 7
G4_FLOOR = 1e-4
MAX_NEW = 8
TAIL = "The entity higher in rank is:"

os.makedirs(OUTDIR, exist_ok=True)
log_lines = []
def log(msg):
    line = f"[exp116] {msg}"
    print(line, flush=True)
    log_lines.append(line)

class RunInvalid(Exception): pass
class Halt(Exception): pass

def sha256_state_dict(state_dict):
    h = hashlib.sha256()
    for k in sorted(state_dict.keys()):
        t = state_dict[k]
        arr = t.detach().cpu().to(torch.float32).numpy() if hasattr(t, "detach") else np.asarray(t, dtype=np.float32)
        h.update(arr.tobytes())
    return h.hexdigest()

def parse_record(gen_text, E1, E2):
    """Pinned §3.4 parse rule: first occurrence (case-insensitive) in generated text."""
    assert E1.lower() not in E2.lower() and E2.lower() not in E1.lower(), "substring overlap"
    g = gen_text.lower()
    p1 = g.find(E1.lower()); p2 = g.find(E2.lower())
    if p1 < 0 and p2 < 0:
        return "UNPARSEABLE"
    return "E1" if (p1 >= 0 and (p2 < 0 or p1 < p2)) else "E2"

def main():
    t0 = time.time()
    torch.manual_seed(0)
    np.random.seed(0)
    torch.set_num_threads(2)
    threads = torch.get_num_threads()

    # ---- Phase 0a: bench provenance pin ----
    sys.path.insert(0, os.path.join(RUNS, "EXP107_templatectrl"))
    from build_exp107_bench import build_bench, canonical_json
    bench = build_bench()
    assert len(bench) == N, f"bench length {len(bench)} != 60"
    bench_hash = hashlib.sha256(canonical_json(bench)).hexdigest()
    if bench_hash != PIN_BENCH:
        raise Halt(f"HALT: bench canonical-JSON sha256 mismatch (got {bench_hash[:16]}...).")
    log(f"bench pin OK: {bench_hash[:16]}... n=60")

    # ---- Phase 0b: archived decisions provenance pin + G4 ----
    dec_path = os.path.join(RUNS, "EXP112_hdildr", "out", "exp112_per_item.json")
    with open(dec_path, "rb") as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != PIN_DECISIONS:
        raise Halt("HALT: exp112_per_item.json sha256 mismatch (archive drift).")
    records = json.loads(raw)
    assert len(records) == N
    # alignment: id + E1/E2 convention check against bench build order
    for i, (b, r) in enumerate(zip(bench, records)):
        assert r["id"] == b["id"], f"record/bench id mismatch at {i}: {r['id']} vs {b['id']}"
        assert r["E1"] == b["tuple"][0] and r["E2"] == b["tuple"][-1], f"E1/E2 convention mismatch at {i}"
        assert r["decision"] in ("E1", "E2"), f"bad decision at {i}"
    vals = [r["cos_E1"] for r in records] + [r["cos_E2"] for r in records]
    g4 = max(vals) - min(vals)
    if g4 < G4_FLOOR:
        raise Halt(f"HALT: archived G4 re-check {g4} < 1e-4 (archive drift).")
    log(f"decisions pin OK; alignment 60/60; archived G4 max-min={g4:.6f}")

    # ---- Phase 1: load frozen backbone, pre-hash ----
    # accelerate is unavailable in the env (per EXP115 note); the machine is CPU-only,
    # so a plain from_pretrained load lands on CPU — equivalent to device_map="cpu".
    tokenizer = AutoTokenizer.from_pretrained(SNAPSHOT, local_files_only=True)
    import importlib.util as _iu
    if _iu.find_spec("accelerate") is not None:
        model = AutoModelForCausalLM.from_pretrained(SNAPSHOT, local_files_only=True,
                                                     torch_dtype=torch.float32, device_map="cpu")
        dm = "cpu"
    else:
        log("accelerate unavailable; loading without device_map (CPU-only machine)")
        model = AutoModelForCausalLM.from_pretrained(SNAPSHOT, local_files_only=True,
                                                     torch_dtype=torch.float32)
        dm = "default-cpu"
    model.eval()
    h_before = sha256_state_dict(model.state_dict())
    if h_before != PIN_BACKBONE:
        raise RunInvalid(f"RUN-INVALID: backbone hash mismatch before (got {h_before}). Quarantine.")
    log(f"backbone pre-hash OK: {h_before[:16]}... (Δθ=0), device_map={dm}")

    # ---- Phase 2: build 60 pinned priming prompts (§3.3 verbatim) ----
    prompts = []
    for i, b in enumerate(bench):
        full = b["prompt"] + "\n\n" + TAIL
        prompts.append(full)
    # binding checks: single block, ends mid-sentence with "is:", no exemplar blocks
    for j, full in enumerate(prompts):
        assert full.endswith("is:"), f"prompt {j} must end mid-sentence with 'is:'"
        assert full.count("Premise:") == 1, f"prompt {j} must contain exactly one 'Premise:'"
    log("60 priming prompts built per §3.3 (single target block, unfinished copula tail)")

    # ---- Phase 3: generate (greedy, max_new_tokens=8), no early abandonment ----
    pad_id = tokenizer.eos_token_id
    records_out = []
    exceptions = 0
    tgen = time.time()
    with torch.no_grad():
        for i, (b, full) in enumerate(zip(bench, prompts)):
            rec = {"bench_index": i, "id": b["id"], "E1": b["tuple"][0], "E2": b["tuple"][-1]}
            try:
                enc = tokenizer(full, return_tensors="pt")
                out = model.generate(enc["input_ids"], max_new_tokens=MAX_NEW,
                                     do_sample=False, pad_token_id=pad_id)
                new_toks = out[0][enc["input_ids"].shape[1]:]
                gen_text = tokenizer.decode(new_toks, skip_special_tokens=True)
                rec["generation"] = gen_text
            except Exception:
                exceptions += 1
                rec["generation"] = ""
                rec["exception"] = traceback.format_exc(limit=3)
            records_out.append(rec)
            if (i + 1) % 20 == 0:
                log(f"progress: {i+1}/60 generations, {time.time()-tgen:.1f}s elapsed, exceptions={exceptions}")
    log(f"generations done: 60/60, exceptions={exceptions}, {time.time()-tgen:.1f}s")

    # ---- Phase 4: backbone post-hash ----
    h_after = sha256_state_dict(model.state_dict())
    if h_after != PIN_BACKBONE:
        raise RunInvalid("RUN-INVALID: backbone hash mismatch after (Δθ≠0). Quarantine.")
    log(f"backbone post-hash OK (Δθ=0)")

    # ---- Phase 5: deterministic re-parse ×2 ----
    def parse_all():
        table = {}
        for rec in records_out:
            table[rec["id"]] = parse_record(rec["generation"], rec["E1"], rec["E2"])
        return table
    t1, t2 = parse_all(), parse_all()
    assert t1 == t2, "re-parse mismatch"
    for rec in records_out:
        rec["parsed"] = t1[rec["id"]]
    log("re-parse ×2 byte-identical")

    # ---- Phase 6: gates BEFORE any metric ----
    n_unparseable = sum(1 for r in records_out if r["parsed"] == "UNPARSEABLE")
    from collections import Counter
    c = Counter(r["parsed"] for r in records_out)
    nonnull = {k: v for k, v in c.items() if k != "UNPARSEABLE"}
    n_distinct = len(nonnull)
    minority = min(nonnull.values()) if nonnull else 0
    log(f"G1: n_unparseable={n_unparseable}/60 (bar: >=7 -> RUN-INVALID)")
    log(f"G2: distinct(non-null)={n_distinct}, minority={minority} (need >=2 distinct, minority>=3)")
    log(f"parse distribution (incl. UNPARSEABLE): {dict(c)}")
    if n_unparseable >= G1_BAR:
        verdict = "RUN-INVALID"; reason = "G1 elicitation-failure gate fired"
    elif n_distinct < 2 or minority < 3:
        verdict = "RUN-INVALID"; reason = "G2 variation guard fired"
    else:
        verdict = None; reason = None

    # ---- Phase 7: metric (only if gates pass) — §4 bars at n=60 verbatim ----
    fidelity = None; n_match = None; bars_result = None
    if verdict is None:
        n_match = sum(1 for r in records_out if r["parsed"] == records[r["bench_index"]]["decision"])
        fidelity = n_match / 60
        if n_match >= 59: verdict = "KILL"; reason = "fidelity >= 59/60: perfect within noise, no gap"
        elif n_match == 58: verdict = "HELD"; reason = "58/60: gap too small to instrument"
        elif n_match >= 42: verdict = "CONTINUE"; reason = "42-57/60: real signal and real gap"
        elif n_match >= 34: verdict = "HELD"; reason = "34-41/60: weak signal, below decisive bar"
        else: verdict = "KILL"; reason = "fidelity <= 33/60: no signal at emitted-answer level"
        bars_result = {"n": 60, "n_match": n_match, "fidelity": fidelity}

    # per-cell descriptive (no decision branch reads it)
    cells = {}
    for r in records_out:
        b = bench[r["bench_index"]]
        key = f"{b['phrasing']}|{'flipped' if b['flipped'] else 'original'}"
        match = None
        if verdict is not None and "RUN-INVALID" not in verdict:
            match = 1 if r["parsed"] == records[r["bench_index"]]["decision"] else 0
        cells.setdefault(key, []).append({"id": r["id"], "parsed": r["parsed"],
                                          "decision": records[r["bench_index"]]["decision"], "match": match})

    result = {
        "experiment": "EXP116_HDI-PRIM", "lane": "LOG-4602",
        "pins": {"bench": bench_hash, "decisions": PIN_DECISIONS, "backbone_before": h_before, "backbone_after": h_after, "delta_theta": 0},
        "env": {"torch": torch.__version__, "transformers": __import__("transformers").__version__,
                "numpy": np.__version__, "accelerate": "unavailable", "device_map": dm,
                "threads_set": 2, "threads_read": threads,
                "seed_torch": 0, "seed_numpy": 0, "device": "cpu", "dtype": "float32",
                "decoding": "greedy", "max_new_tokens": MAX_NEW, "priming_tail": TAIL},
        "gates": {"G1_n_unparseable_60": n_unparseable, "G2_distinct": n_distinct, "G2_minority": minority},
        "exceptions": exceptions,
        "fidelity_result": bars_result,
        "verdict": verdict, "verdict_reason": reason,
        "per_cell": {k: {"n": len(v), "matches": [x["match"] for x in v]} for k, v in cells.items()},
        "systematic_misreporting_signature": (n_match is not None and n_match <= 22),
        "elapsed_min": (time.time() - t0) / 60,
    }
    json.dump(records_out, open(os.path.join(OUTDIR, "exp116_generations.json"), "w"), indent=1)
    json.dump(result, open(os.path.join(OUTDIR, "exp116_result.json"), "w"), indent=1)
    with open(os.path.join(OUTDIR, "exp116_stdout.log"), "w") as f:
        f.write("\n".join(log_lines))
    log(f"VERDICT={verdict} ({reason}); artifacts written")
    return verdict

if __name__ == "__main__":
    try:
        v = main()
    except (RunInvalid, Halt) as e:
        print(f"[exp116] {e}", flush=True)
        with open(os.path.join(OUTDIR, "exp116_terminated.txt"), "w") as f:
            f.write(str(e))
        raise SystemExit(2)
