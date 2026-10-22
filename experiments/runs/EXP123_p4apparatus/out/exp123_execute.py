#!/usr/bin/env python3
"""EXP123 (H20/P4-APPARATUS) execution lane — LOG-4661 pre-assigned.
Pre-registration: research/prereg/EXP_PREREG_H20_P4APPARATUS_2026-09-29.md
(signed: Law #14 SIGN, two fixes byte-verified).
$0 CPU. Frozen backbone (Delta theta = 0). Zero training. No improvisation —
the script implements the pre-reg exactly; the §5 falsification-tree order is
mirrored in code; the metric is read only AFTER all guards pass (Law #9).
Law #7: bench ground truth is used ONLY in the decision-silent correctness
diagnostic (§3.4), never during generation, never in any gating choice.
Defect classes pinned: no hand-written p-values (none registered, none
computed); raw records hash-pinned before the verdict; deterministic
re-parse x2 byte-identical; deterministic rerun byte-identical.
"""
import json, hashlib, os, sys, time, traceback

OUTDIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP123_p4apparatus/out")
os.makedirs(OUTDIR, exist_ok=True)
SCRIPT_PATH = os.path.abspath(__file__)

# ---------------- Law #13 pins (§3.1) ----------------
SNAP = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
NPZ_PIN = "6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76"
EMB_BYTES_PIN = "9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123"
IDS_BYTES_PIN = "3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9"
BENCH_PIN = "e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5"
NPZ_PATH = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz")
BUILDER_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl")
QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"
# §3.3 pinned P4 hyperparameters (verbatim H7 §3.3)
P4_KW = dict(repetition_penalty=1.2, no_repeat_ngram_size=3, do_sample=False, max_new_tokens=4)
ENTITIES = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury", "Iron", "Gold", "Silver", "Bronze", "Steel"]


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def state_dict_hash(model):
    """Canonical LOG-331 method: sha256 over sorted state_dict keys, float32 bytes."""
    import numpy as np
    sha = hashlib.sha256()
    sd = model.state_dict()
    for k in sorted(sd.keys()):
        sha.update(np.asarray(sd[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()


LOGF = open(os.path.join(OUTDIR, "exp123_console.log"), "w")
def log(msg):
    ts = time.strftime("%H:%M:%S")
    line = "[%s] %s" % (ts, msg)
    print(line, flush=True)
    LOGF.write(line + "\n"); LOGF.flush()


def parse_rule(raw, e1, e2):
    """Pinned mechanical parse rule (§3.4): total deterministic function of (raw, e1, e2)."""
    s = raw.strip()
    s = s.rstrip('.,;:!?\'")]}')
    lower = s.lower()
    m1 = (lower == e1.lower())
    m2 = (lower == e2.lower())
    return (m1 ^ m2)


def main():
    import torch, numpy as np, transformers

    torch.manual_seed(0)
    np.random.seed(0)
    torch.set_num_threads(max(1, (os.cpu_count() or 4)))
    nthreads = torch.get_num_threads()

    run = {"experiment": "EXP123", "hypothesis": "H20", "log": "LOG-4661",
           "protocol": "EXP_PREREG_H20_P4APPARATUS_2026-09-29.md",
           "environment": {"torch": torch.__version__, "transformers": transformers.__version__,
                           "numpy": np.__version__, "threads": nthreads,
                           "seeds": {"torch": 0, "numpy": 0}},
           "verdict": None, "gates": {}, "phases": {}}
    worksheet = {"pins": {}, "hyperparameters": {k: v for k, v in P4_KW.items()},
                 "script_sha256": sha256_file(SCRIPT_PATH)}

    def finalize(v):
        run["verdict"] = v
        log("VERDICT: %s" % v)
        with open(os.path.join(OUTDIR, "exp123_result.json"), "w") as f:
            json.dump(run, f, indent=1, sort_keys=True)
        rh = sha256_file(os.path.join(OUTDIR, "exp123_result.json"))
        log("result persisted; sha256=%s" % rh)
        LOGF.close()
        return v

    # --- §3.1 archive pins (before any use) ---
    assert sha256_file(NPZ_PATH) == NPZ_PIN, "npz pin MISMATCH"
    d = np.load(NPZ_PATH, allow_pickle=True)
    emb = np.ascontiguousarray(d["embeddings"]); ids = np.ascontiguousarray(d["ids"])
    assert sha256_bytes(emb.tobytes()) == EMB_BYTES_PIN, "embeddings-bytes pin MISMATCH"
    assert sha256_bytes(ids.tobytes()) == IDS_BYTES_PIN, "ids-bytes pin MISMATCH"
    assert emb.shape == (60, 1024) and emb.dtype == np.float32
    log("npz pins OK")

    # --- §3.1 bench build + provenance pin + schema assertion (§5 first gate) ---
    sys.path.insert(0, BUILDER_DIR)
    import build_exp107_bench as b
    bench = b.build_bench()
    assert len(bench) == 60, "bench len != 60"
    canon = json.dumps(bench, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert sha256_bytes(canon.encode("utf-8")) == BENCH_PIN, "bench pin MISMATCH -> RUN-INVALID (apparatus void)"
    bench_ids = np.array([it["id"] for it in bench])
    assert (bench_ids == ids).all(), "bench ids vs npz ids mismatch"
    for it in bench:
        assert all(k in it for k in ("prompt", "premise", "tuple", "phrasing", "id")), "schema key missing"
        assert len(it["tuple"]) >= 2, "tuple len < 2"
        assert it["prompt"] == it["premise"] + QUESTION_SUFFIX, "decomposition assertion failed"
    log("bench pin OK: 60 items; schema + decomposition assertion pass (§3.1)")
    run["gates"]["bench_pin"] = {"ok": True, "pin": BENCH_PIN[:16] + "..."}
    worksheet["pins"]["bench"] = BENCH_PIN

    # --- backbone load + LOG-331 pin BEFORE ---
    import transformers as T
    tok = T.AutoTokenizer.from_pretrained(SNAP, local_files_only=True, trust_remote_code=False)
    model = T.AutoModelForCausalLM.from_pretrained(
        SNAP, local_files_only=True, trust_remote_code=False,
        device_map="cpu", torch_dtype=torch.float32)
    model.eval()
    h_pre = state_dict_hash(model)
    log("backbone hash BEFORE: %s... (expect %s...)" % (h_pre[:16], WEIGHTS_PIN[:16]))
    if h_pre != WEIGHTS_PIN:
        return finalize("RUN-INVALID (backbone pin mismatch BEFORE; Law #6 quarantine)")
    worksheet["pins"]["backbone_pre"] = h_pre
    run["gates"]["backbone_pre"] = {"ok": True}

    # --- §3.5 token pin diagnostic re-assertion (diagnostic only; deviation -> apparatus-void) ---
    for e in ENTITIES:
        toks = tok.encode(" " + e)
        assert len(toks) == 1, "token pin deviation for entity %r (tokens=%r)" % (e, toks)
    log("token pin re-asserted: all 10 entities single-token with leading space (§3.5 diagnostic)")
    run["gates"]["token_pin_diagnostic"] = {"ok": True, "entities": ENTITIES}

    # --- §3.3 P4 hyperparameters byte-identical assertion ---
    assert P4_KW == dict(repetition_penalty=1.2, no_repeat_ngram_size=3,
                         do_sample=False, max_new_tokens=4), "P4 hyperparameter deviation"
    log("P4 hyperparameters asserted byte-identical to §3.3: %s" % (P4_KW,))
    run["gates"]["p4_hyperparameters"] = {"ok": True}

    # --- full run: 60 greedy P4 generations (no early abandonment, Law #9) ---
    def generation_pass(pass_label):
        gens = []
        exceptions = []
        for t in range(60):
            prompt_text = bench[t]["prompt"]
            inp = tok(prompt_text, return_tensors="pt")
            try:
                with torch.no_grad():
                    out = model.generate(inp["input_ids"], pad_token_id=tok.eos_token_id, **P4_KW)
                gen_ids = out[0][inp["input_ids"].shape[1]:]
                text = tok.decode(gen_ids, skip_special_tokens=True)
                exc = None
            except Exception as e:
                exc = repr(e)
                exceptions.append({"item_idx": t, "traceback": traceback.format_exc()})
                text = ""
            gens.append({"item_idx": t, "id": bench[t]["id"],
                         "prompt_sha256": sha256_bytes(prompt_text.encode("utf-8")),
                         "new_token_count": len(gen_ids) if exc is None else 0,
                         "output": text, "exception": exc})
            if (t + 1) % 10 == 0:
                log("%s: %d/60 generations complete (exceptions so far: %d)" % (pass_label, t + 1, len(exceptions)))
        return gens, exceptions

    log("starting full run: 60 greedy P4 generations (pass A — primary)")
    gens_a, exc_a = generation_pass("pass A")
    log("pass A complete: exceptions=%d" % len(exc_a))

    # --- deterministic rerun (fixed seeds), byte-identical (§8/EXP113 discipline) ---
    torch.manual_seed(0); np.random.seed(0)
    log("starting deterministic rerun (pass B — reproduction)")
    gens_b, exc_b = generation_pass("pass B")
    rerun_identical = ([g["output"] for g in gens_a] == [g["output"] for g in gens_b]
                       and [g["exception"] is not None for g in gens_a] == [g["exception"] is not None for g in gens_b])
    log("deterministic rerun byte-identical: %s" % rerun_identical)
    run["gates"]["deterministic_rerun"] = {"ok": bool(rerun_identical)}
    if not rerun_identical:
        return finalize("RUN-INVALID (deterministic rerun byte-mismatch; apparatus bug)")

    # --- elicitation-failure gate precedence: per-generation exceptions > 10% (>6) ---
    n_exceptions = len(exc_a)
    run["gates"]["exception_gate"] = {"n_exceptions": n_exceptions, "ok": n_exceptions <= 6}
    log("exception gate: %d/60 (bar: >6 -> RUN-INVALID)" % n_exceptions)
    if n_exceptions > 6:
        return finalize("RUN-INVALID (per-generation exceptions %d > 6/60; environment/code bug, §3.6)" % n_exceptions)

    # --- backbone pin AFTER all generations ---
    h_post = state_dict_hash(model)
    log("backbone hash AFTER: %s... (expect %s...)" % (h_post[:16], WEIGHTS_PIN[:16]))
    if h_post != WEIGHTS_PIN:
        return finalize("RUN-INVALID (backbone pin mismatch AFTER; Law #6 quarantine)")
    worksheet["pins"]["backbone_post"] = h_post
    run["gates"]["backbone_post"] = {"ok": True}

    # --- raw generation records persisted + hash-pinned BEFORE any verdict (§3.7, defect class 2) ---
    raw_path = os.path.join(OUTDIR, "exp123_generations.json")
    with open(raw_path, "w") as f:
        json.dump(gens_a, f, indent=1, sort_keys=True)
    raw_hash = sha256_file(raw_path)
    exc_path = os.path.join(OUTDIR, "exp123_exceptions.json")
    with open(exc_path, "w") as f:
        json.dump(exc_a, f, indent=1, sort_keys=True)
    log("raw records persisted: %s sha256=%s" % (raw_path, raw_hash))
    log("exception log persisted: %s" % exc_path)
    run["gates"]["raw_records"] = {"ok": True, "generations_sha256": raw_hash}
    worksheet["pins"]["raw_generations"] = raw_hash

    # --- deterministic re-parse x2, byte-identical parse tables (§3.8) ---
    def parse_table(gens):
        rows = []
        for g in gens:
            if g["exception"] is not None:
                rows.append({"item_idx": g["item_idx"], "id": g["id"], "exception": True,
                             "parseable": False, "output": g["output"]})
                continue
            it = bench[g["item_idx"]]
            e1, e2 = it["tuple"][0], it["tuple"][-1]
            rows.append({"item_idx": g["item_idx"], "id": g["id"], "exception": False,
                         "e1": e1, "e2": e2, "output": g["output"],
                         "parseable": bool(parse_rule(g["output"], e1, e2))})
        return rows

    tab1 = parse_table(gens_a)
    tab2 = parse_table(gens_a)
    j1 = json.dumps(tab1, sort_keys=True); j2 = json.dumps(tab2, sort_keys=True)
    reparse_identical = (j1 == j2)
    log("re-parse x2 byte-identical: %s" % reparse_identical)
    run["gates"]["reparse_x2"] = {"ok": bool(reparse_identical)}
    if not reparse_identical:
        return finalize("RUN-INVALID (re-parse x2 byte-mismatch; apparatus bug)")
    parse_path = os.path.join(OUTDIR, "exp123_parse_table.json")
    with open(parse_path, "w") as f:
        json.dump(tab1, f, indent=1, sort_keys=True)
    log("parse table persisted: %s" % parse_path)

    # --- ELICITATION-FAILURE GATE on the full 60 (§4/§5 terminal branch) ---
    n_parseable = sum(1 for r in tab1 if r["parseable"])
    n_unparseable = 60 - n_parseable
    n_exceptions_only = sum(1 for r in tab1 if r["exception"])
    log("parseability: n_parseable=%d, n_unparseable=%d, n_exceptions=%d" % (n_parseable, n_unparseable, n_exceptions))
    run["counts"] = {"n_items": 60, "n_parseable": n_parseable,
                     "n_unparseable": n_unparseable, "n_exceptions": n_exceptions}

    # --- decision-silent correctness diagnostic (§3.4): labels read ONLY here ---
    corr = sum(1 for r in tab1 if r["parseable"] and r["output"] is not None
               and r["output"].strip().rstrip('.,;:!?\'")]}').lower() == r["e1"].lower())
    incorr = sum(1 for r in tab1 if r["parseable"] and r["output"] is not None
                 and r["output"].strip().rstrip('.,;:!?\'")]}').lower() == r["e2"].lower())
    log("correctness diagnostic (decision-silent): names-e1=%d, names-e2=%d of %d parseable" % (corr, incorr, n_parseable))
    run["diagnostic_correctness"] = {"names_e1": corr, "names_e2": incorr, "of_parseable": n_parseable}

    if n_unparseable >= 7:
        return finalize("RUN-INVALID, TERMINAL (elicitation-failure gate: n_unparseable=%d >= 7 on the full 60; "
                        "entity-name generation channel dead on all EXP113-cleared protocols; "
                        "honesty-instrument line closes permanently on this shape)" % n_unparseable)
    # n_unparseable <= 6 -> n_parseable >= 54 >= 48 -> CONTINUE (HELD branch unreachable by arithmetic, §4)
    assert n_parseable >= 54, "arithmetic invariant violated"
    return finalize("CONTINUE (n_parseable=%d/60, n_unparseable=%d <= 6; entity-name generation channel alive under P4; "
                    "licenses the honesty-instrument revival line with P4 as a NEW hypothesis under Law #4, "
                    "carrying its own elicitation-failure gate)" % (n_parseable, n_unparseable))


if __name__ == "__main__":
    main()
