#!/usr/bin/env python3
"""EXP143: S5-inverted selector held-out validation (CPU pilot).
Executes EXACTLY per research/analysis_plans/S5-INV_PREREG_DRAFT_2026-10-05.md
(SIGNED, Law #14 SIGN, LOG-4916). Minted by CEO, LOG-4916.
Protocol: verbatim Stage-1 (EXP140_stage1/run_stage1.py) on the pinned held-out
bench (60 view-1 V2_Biblical items). 240 generations + 240 scoring forwards, CPU.
Exit codes: 0 = clean completion (verdict per frozen decision table);
44 = INCONCLUSIVE (Step-0 abort).
"""
import hashlib, json, math, os, sys, time
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from scipy import stats as scipy_stats

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(RUN_DIR, exist_ok=True)
LOGF = open(os.path.join(RUN_DIR, "exp143_run_log.txt"), "w")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOGF.write(line + "\n"); LOGF.flush()

# ============ S5-INV plan §10 pins ============
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
HELD_PIN = "779202d6f8297e70319c7e18e0ccf190c70488ef5c2082501cfb727dc91d1e55"
DISCOVERY_PIN = "eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df"
HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
MODEL_ID = "EleutherAI/pythia-410m"
R_MAX = 48
S_B2, S_B3 = 20261004, 20261005
S_PERM = 20261006
N_ITEMS = 60
N_BRANCHES = 4
N_PERM = 100000

torch.manual_seed(20261003)
torch.set_num_threads(max(1, (os.cpu_count() or 4) - 1))
log("threads=%d numpy=%s scipy=%s" % (torch.get_num_threads(),
      np.__version__, scipy_stats.__version__ if hasattr(scipy_stats, "__version__") else "?"))
import scipy
log("scipy=%s" % scipy.__version__)

FWD_COUNT = [0]
GEN_COUNT = [0]
def count_fwd(n=1):
    FWD_COUNT[0] += n

def sha256_state_dict(model):
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu()
        if t.dtype != torch.float32:
            t = t.float()
        h.update(t.numpy().tobytes())
    return h.hexdigest()

def inconclusive(reason):
    log("INCONCLUSIVE: %s" % reason)
    json.dump({"experiment": "EXP143", "verdict": "INCONCLUSIVE", "reason": reason,
               "forwards": FWD_COUNT[0], "generations": GEN_COUNT[0]},
              open(os.path.join(RUN_DIR, "exp143_verdict.json"), "w"), indent=1)
    LOGF.close()
    sys.exit(44)

# ============ model (plan §10 verbatim) ============
log("loading model %s rev %s (float32, cpu, local_files_only)" % (MODEL_ID, HF_REVISION))
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=HF_REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, revision=HF_REVISION, local_files_only=True,
    torch_dtype=torch.float32, device_map="cpu")
model.eval()
pre_hash = sha256_state_dict(model)
log("backbone pre-hash: %s" % pre_hash)
if pre_hash != BACKBONE_PIN:
    inconclusive("Step 0.2 backbone pre-hash mismatch: got %s" % pre_hash)
log("Step 0.2 backbone pre-hash PASS (Δθ=0 pre)")

def tok1(s):
    ids = tokenizer.encode(" " + s)
    assert len(ids) == 1, "multi-token: %r -> %r" % (s, ids)
    return ids[0]

# ============ Step 0.1: held-out bench pin (full 64-hex, canonical recipe) ============
HELD_PATH = os.path.expanduser(
    "~/workspace/SCBI/research/analysis_plans/S5-INV_HELDBENCH_2026-10-05.json")
held = json.load(open(HELD_PATH))
items = held["bench"]
assert len(items) == 60, "held-out bench len %d != 60" % len(items)
# canonical sha recipe (reviewer R2): sha256 over [{id,prompt,A,C}] sort_keys=True
held_hash = hashlib.sha256(json.dumps(
    [{k: it[k] for k in ("id", "prompt", "A", "C")} for it in items],
    sort_keys=True).encode()).hexdigest()
log("Step 0.1 held-out bench sha256 (full 64-hex): %s" % held_hash)
if held_hash != HELD_PIN:
    inconclusive("Step 0.1 held-out bench sha256 mismatch: got %s" % held_hash)
if held.get("sha256") != HELD_PIN:
    inconclusive("Step 0.1 stored sha256 field mismatch: %s" % held.get("sha256"))
if held.get("derived_from_bench_sha") != DISCOVERY_PIN:
    inconclusive("Step 0.1 derived_from_bench_sha mismatch: %s" % held.get("derived_from_bench_sha"))
log("Step 0.1 held-out pin PASS (recomputed == stored == plan pin; derived_from == corrected discovery pin)")

# single-token assertion for all view-1 A/C names (plan §4)
for ii, v in enumerate(items):
    tok1(v["A"]); tok1(v["C"])
log("tok1 single-token assertion PASS for all 60 view-1 A/C names")

# ============ branch prompts (verbatim Stage-1 recipe, plan §4) ============
TEMPLATE = " Reason step by step, then answer:"
SUFFIX = "\nAnswer:"

def b1_swap_question(view_prompt, A_text, C_text, ii):
    qi = view_prompt.index("Question:")
    head, tail = view_prompt[:qi], view_prompt[qi:]
    pat_AC = "%s or %s" % (A_text, C_text)
    pat_CA = "%s or %s" % (C_text, A_text)
    if pat_AC in tail and pat_CA not in tail:
        tail = tail.replace(pat_AC, pat_CA)
    elif pat_CA in tail and pat_AC not in tail:
        tail = tail.replace(pat_CA, pat_AC)
    else:
        inconclusive("Step 0.3 B1 swap ambiguous on item %d" % ii)
    return head + tail

branch_prompts = []
for ii, v in enumerate(items):
    p0 = v["prompt"] + TEMPLATE
    p1 = b1_swap_question(v["prompt"], v["A"], v["C"], ii) + TEMPLATE
    qi = v["prompt"].index("Question:")
    assert p1[:qi] == v["prompt"][:qi], "B1 premise changed on item %d" % ii
    assert b1_swap_question(p1[:len(p1)-len(TEMPLATE)], v["A"], v["C"], ii) == v["prompt"], \
        "B1 not involutive on item %d" % ii
    branch_prompts.append([p0, p1, p0, p0])
log("branch prompts built (B1 swap verified involutive, premise-unchanged, all 60)")

# Step 0.3 (prompt part): byte-for-byte recipe check on all 240 prompts
for ii, v in enumerate(items):
    assert branch_prompts[ii][0] == v["prompt"] + TEMPLATE
    assert branch_prompts[ii][2] == branch_prompts[ii][0]
    assert branch_prompts[ii][3] == branch_prompts[ii][0]
log("Step 0.3 prompt byte-for-byte recipe PASS (240/240)")

t_A_list = [tok1(v["A"]) for v in items]
t_C_list = [tok1(v["C"]) for v in items]
suffix_ids = tokenizer.encode(SUFFIX)

# ============ generation (verbatim Stage-1) ============
def generate_rationale(prompt, branch):
    inputs = tokenizer(prompt, return_tensors="pt")
    prompt_ids = inputs["input_ids"][0].tolist()
    gen_kwargs = dict(max_new_tokens=R_MAX, pad_token_id=tokenizer.eos_token_id)
    if branch in (2, 3):
        torch.manual_seed(S_B2 if branch == 2 else S_B3)
        gen_kwargs.update(do_sample=True, temperature=0.7)
    else:
        gen_kwargs.update(do_sample=False)
    with torch.no_grad():
        out = model.generate(**inputs, **gen_kwargs)
    GEN_COUNT[0] += 1
    prompt_len = inputs["input_ids"].shape[1]
    return prompt_ids, out[0][prompt_len:].tolist()

# ============ scoring (verbatim Stage-1: folded teacher-forced pass) ============
def score_branch(prompt_ids, rationale_ids, t_A, t_C):
    if len(rationale_ids) == 0:
        return None, None, None
    full = prompt_ids + rationale_ids + suffix_ids
    input_ids = torch.tensor([full])
    with torch.no_grad():
        out = model(input_ids=input_ids)
    count_fwd(1)
    logits = out.logits[0]
    logprobs = torch.log_softmax(logits.float(), dim=-1)
    nlls = []
    for i, tok in enumerate(rationale_ids):
        j = len(prompt_ids) + i
        nlls.append(float(-logprobs[j - 1, tok]))
    F_k = sum(nlls) / len(nlls)
    final_logits = logits[-1]
    a_k = t_A if float(final_logits[t_A]) >= float(final_logits[t_C]) else t_C
    ans_nll = float(-logprobs[-1, a_k])
    F_full = (sum(nlls) + ans_nll) / (len(nlls) + 1)
    return F_k, F_full, a_k

# ============ main loop ============
records = []
degenerate_pairs = 0
# incremental per-item records (flush after each item; survives interruption)
INCR = open(os.path.join(RUN_DIR, "exp143_items_incremental.jsonl"), "w")
t0 = time.time()
for ii in range(N_ITEMS):
    v = items[ii]
    t_A, t_C = t_A_list[ii], t_C_list[ii]
    branches = []
    for k in range(N_BRANCHES):
        prompt_ids, rat = generate_rationale(branch_prompts[ii][k], k)
        F_k, F_full, a_k = score_branch(prompt_ids, rat, t_A, t_C)
        deg = (F_k is None)
        if deg:
            degenerate_pairs += 1
        else:
            if a_k not in (t_A, t_C):
                inconclusive("Step 0.3 answer not in {t_A,t_C} on item %d branch %d" % (ii, k))
        branches.append({"k": k, "n_rat": len(rat),
                         "F": F_k, "F_full": F_full, "a": a_k,
                         "correct": (a_k == t_A) if not deg else None,
                         "degenerate": deg,
                         "rationale_ids": rat,
                         "rationale_text": tokenizer.decode(rat)})
    records.append({"item": ii, "id": v["id"], "src_id": v.get("src_id"),
                    "t_A": t_A, "t_C": t_C, "branches": branches})
    INCR.write(json.dumps(records[-1]) + "\n")
    INCR.flush()
    if (ii + 1) % 10 == 0:
        log("items %d/60; gens=%d fwds=%d; %.1fs elapsed" %
            (ii + 1, GEN_COUNT[0], FWD_COUNT[0], time.time() - t0))
INCR.close()
log("generation+scoring complete: gens=%d fwds=%d degenerate_pairs=%d" %
    (GEN_COUNT[0], FWD_COUNT[0], degenerate_pairs))

if GEN_COUNT[0] != 240 or FWD_COUNT[0] != 240:
    inconclusive("Step 0.3 pass count mismatch: gens=%d fwds=%d (expected 240/240)" %
                 (GEN_COUNT[0], FWD_COUNT[0]))
log("Step 0.3 pass counts 240/240 PASS")

# determinism spot-check (plan compute budget: <=3 re-runs; Stage-1 gate (c))
for ii in (0, 30, 59):
    _, rat2 = generate_rationale(branch_prompts[ii][0], 0)
    GEN_COUNT[0] += 1
    if rat2 != records[ii]["branches"][0]["rationale_ids"]:
        inconclusive("Step 0 determinism spot-check failed on item %d" % ii)
log("Step 0 determinism spot-check PASS (items 0, 30, 59 byte-identical)")

# Step 0.2 (post): backbone hash (Δθ=0)
post_hash = sha256_state_dict(model)
log("backbone post-hash: %s" % post_hash)
if post_hash != BACKBONE_PIN:
    inconclusive("Step 0.2 backbone post-hash mismatch: Δθ != 0")
log("Step 0.2 Δθ=0 PASS")

# ============ per-item aggregates ============
missing_items = 0
for rec in records:
    valid = [b for b in rec["branches"] if not b["degenerate"]]
    if len(valid) == 0:
        missing_items += 1
        rec["spread"] = None
        rec["acc"] = None
        continue
    Fs = [b["F"] for b in valid]
    rec["spread"] = max(Fs) - min(Fs)
    rec["acc"] = sum(1 for b in valid if b["correct"]) / len(valid)

# Step 0.5: missing-data rule (>6 items = >10% -> INCONCLUSIVE)
if missing_items > 6:
    inconclusive("Step 0.5 missing-data: %d items fully degenerate (>6)" % missing_items)
log("Step 0.5 missing-data PASS (%d fully-degenerate items)" % missing_items)

# Step 1 — signals (label-free): spread_i
usable = [rec for rec in records if rec["spread"] is not None]
spreads = np.array([rec["spread"] for rec in usable])
n = len(usable)
log("Step 1: n=%d usable items with spread" % n)

# Step 0.4 — degeneracy pre-check (S7-3 lesson): must vary IN PRINCIPLE
if not (float(np.std(spreads, ddof=1)) > 0):
    inconclusive("Step 0.4 degeneracy: std(spreads)==0")
med_spread = float(np.median(spreads))
if not (med_spread >= 0.05):
    inconclusive("Step 0.4 degeneracy: median(spread)=%.6f < 0.05" % med_spread)
log("Step 0.4 degeneracy pre-check PASS (std=%.6f > 0, median=%.6f >= 0.05)" %
    (float(np.std(spreads, ddof=1)), med_spread))

# Step 2 — targets (Law #7 firewall: labels enter ONLY here)
ybar = np.array([rec["acc"] for rec in usable])
if float(np.std(ybar, ddof=1)) == 0:
    inconclusive("Step 0.4 degeneracy: mean branch correctness does not vary")
log("Step 2: targets built (mean branch correctness varies: std=%.4f)" %
    float(np.std(ybar, ddof=1)))

# SELECT/UNSELECT partition from spreads alone, BEFORE targets are touched (Law #7)
order = sorted(range(n), key=lambda i: (spreads[i], usable[i]["id"]))
sel_idx = order[:n // 2]
unsel_idx = order[n // 2:]
assert len(sel_idx) == 30 and len(unsel_idx) == 30
log("SELECT/UNSELECT partition frozen from spreads alone (30/30, Law #7)")

# ============ Step 3 — tests ============
def spearman_perm_p(x, y, n_perm, seed, side):
    """Exact one-sided permutation p for Spearman via rank-Pearson.
    side='neg': H1 rho<0 -> p = (#{perm r <= obs}+1)/(n_perm+1)
    side='pos': H1 rho>0 -> p = (#{perm r >= obs}+1)/(n_perm+1)"""
    rx = scipy_stats.rankdata(x)
    ry = scipy_stats.rankdata(y)
    rxc = rx - rx.mean()
    ryc = ry - ry.mean()
    denom = math.sqrt(float(np.sum(rxc ** 2)) * float(np.sum(ryc ** 2)))
    if denom == 0:
        return float("nan"), float("nan"), 0
    r_obs = float(np.dot(rxc, ryc) / denom)
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(n_perm):
        ryp = rng.permutation(ry)
        rypc = ryp - ryp.mean()
        r = float(np.dot(rxc, rypc) / denom)
        if side == "neg" and r <= r_obs:
            cnt += 1
        elif side == "pos" and r >= r_obs:
            cnt += 1
    return r_obs, (cnt + 1) / (n_perm + 1), cnt

# Primary (replication): Spearman(spread, ybar), one-sided H1: rho<0
rho_obs, p_one, n_le = spearman_perm_p(spreads, ybar, N_PERM, S_PERM, "neg")
# two-sided diagnostic: 2*min(one-sided tails)
_, p_pos, _ = spearman_perm_p(spreads, ybar, N_PERM, S_PERM + 778, "pos")
p_two = min(1.0, 2.0 * min(p_one, p_pos))
# 95% CI via Fisher z
z = math.atanh(max(-0.999999, min(0.999999, rho_obs)))
se = 1.0 / math.sqrt(n - 3)
ci_lo, ci_hi = math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)
# MDE at 80% power, one-sided alpha=0.025, n=60 (Fisher-z closed form)
z_alpha = scipy_stats.norm.ppf(0.975)
z_beta = scipy_stats.norm.ppf(0.80)
mde80 = math.tanh((z_alpha + z_beta) / math.sqrt(n - 3))
primary_pass = (rho_obs <= -0.3) and (p_one < 0.025)
log("PRIMARY: Spearman(spread, ybar) rho=%.6f one-sided p=%.8f (n_le=%d) "
    "two-sided p=%.8f 95%%CI=[%.4f, %.4f] MDE80=%.4f -> %s" %
    (rho_obs, p_one, n_le, p_two, ci_lo, ci_hi, mde80,
     "PASS" if primary_pass else "FAIL"))

# Secondary (hierarchical): median-split gain
delta_obs = float(ybar[sel_idx].mean() - ybar[unsel_idx].mean())
rng2 = np.random.default_rng(S_PERM)
ge = 0
idx_all = np.arange(n)
for _ in range(N_PERM):
    pidx = rng2.permutation(idx_all)
    d = float(ybar[pidx[:n // 2]].mean() - ybar[pidx[n // 2:]].mean())
    if d >= delta_obs:
        ge += 1
p_sec = (ge + 1) / (N_PERM + 1)
secondary_pass = (delta_obs >= 0.10) and (p_sec < 0.025)
log("SECONDARY: Delta=%.6f one-sided p=%.8f (n_ge=%d) -> %s%s" %
    (delta_obs, p_sec, ge, "PASS" if secondary_pass else "FAIL",
     " (hierarchical: evaluated)" if primary_pass else " (hierarchical: recorded only)"))

# ============ Step 4 — decision (§6, frozen) ============
if primary_pass and secondary_pass:
    verdict = "CONTINUE (SELECTION-READY)"
elif primary_pass and not secondary_pass:
    verdict = "CONTINUE (SIGNAL-ONLY)"
else:
    verdict = "KILL"
log("STEP 4 VERDICT: %s" % verdict)

# ============ records ============
serial = []
for rec in records:
    serial.append({
        "item": rec["item"], "id": rec["id"], "src_id": rec.get("src_id"),
        "spread": rec["spread"], "acc": rec["acc"],
        "branches": [{"k": b["k"], "n_rat": b["n_rat"], "F": b["F"],
                      "F_full": b["F_full"], "correct": b["correct"],
                      "degenerate": b["degenerate"],
                      "rationale_ids": b["rationale_ids"],
                      "rationale_text": b["rationale_text"]} for b in rec["branches"]],
    })
out = {
    "experiment": "EXP143",
    "prereg": "research/analysis_plans/S5-INV_PREREG_DRAFT_2026-10-05.md (SIGNED, Law #14 SIGN, LOG-4916)",
    "pins": {"backbone_pre": pre_hash, "backbone_post": post_hash,
             "held_bench": held_hash, "held_bench_plan": HELD_PIN,
             "derived_from": DISCOVERY_PIN,
             "hf_revision": HF_REVISION, "model": MODEL_ID, "dtype": "float32"},
    "seeds": {"S_B2": S_B2, "S_B3": S_B3, "S_PERM": S_PERM},
    "counts": {"generations": 240, "forwards": 240,
               "diagnostic_gens": GEN_COUNT[0] - 240,
               "degenerate_pairs": degenerate_pairs,
               "missing_items": missing_items, "n_usable": n},
    "step0": {"bench_sha_full": held_hash, "backbone_pre": pre_hash,
              "backbone_post": post_hash, "median_spread": med_spread,
              "std_spread": float(np.std(spreads, ddof=1))},
    "per_item": {"spreads": [float(s) for s in spreads],
                 "ybar": [float(y) for y in ybar],
                 "ids": [rec["id"] for rec in usable]},
    "primary": {"rho": float(rho_obs), "p_one_sided": float(p_one),
                "n_perm_le": int(n_le), "p_two_sided_diag": float(p_two),
                "ci95": [float(ci_lo), float(ci_hi)], "mde80": float(mde80),
                "n_perm": N_PERM, "seed": S_PERM,
                "pass": bool(primary_pass)},
    "secondary": {"delta": float(delta_obs), "p_one_sided": float(p_sec),
                  "n_perm_ge": int(ge), "n_perm": N_PERM, "seed": S_PERM,
                  "n_selected": len(sel_idx),
                  "pass": bool(secondary_pass)},
    "verdict": verdict,
    "items": serial,
}
json.dump(out, open(os.path.join(RUN_DIR, "exp143_records.json"), "w"), indent=1)
json.dump({"experiment": "EXP143", "verdict": verdict,
           "primary_rho": float(rho_obs), "primary_p": float(p_one),
           "secondary_delta": float(delta_obs), "secondary_p": float(p_sec),
           "forwards": FWD_COUNT[0], "generations": GEN_COUNT[0]},
          open(os.path.join(RUN_DIR, "exp143_verdict.json"), "w"), indent=1)
log("records written; DONE")
LOGF.close()
