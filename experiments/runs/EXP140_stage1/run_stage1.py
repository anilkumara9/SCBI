#!/usr/bin/env python3
"""EXP140 Stage-1: S4-5 free-energy branch selection CPU pilot.
Executes EXACTLY per research/prereg/EXP_S45_prereg_DRAFT_2026-10-03.md (SIGNED, LOG-4887).
CEO venue approval: Stage-1 CPU pilot only (240 generations + 240 scoring passes). $0 compute.
Exit codes: 0 = clean completion; 44 = RUN-INVALID (validity gate trip).

Pre-reg interpretation notes (documented, not improvised):
- Readout: the pre-reg writes argmax over {tok1("A"), tok1("C")}. Per the binding
  EXP139 execution precedent (run_stage1.py line 217: yhat_of(logits, tok1(v["A"]),
  tok1(v["C"]))), the program's pre-reg notation tok1("A") denotes the single token
  of the bench's "A" field value (the correct entity name), i.e. tok1(v["A"]).
  This matches the design's unquoted tok1(A)/tok1(C), EXP135's baseline
  (run_exp135.py:290), and the pre-reg's own "same 2-token forced-choice readout
  as the EXP135 baseline" claim. Correct iff argmax == tok1(v["A"]).
- B1: "the two option texts exchanged in place" = swap X/Y in the question's
  "X or Y" only; premise untouched (swapping premise facts would flip the correct
  entity and break "correctness remains (a_k == tok1('A'))"). Verified involutive.
- B2/B3 seeds: torch.manual_seed(S_Bx) before each stochastic generation
  (transformers 5.17 generate() accepts no `generator` kwarg); deterministic per
  (item, branch), order-independent.
- Random-branch: torch.Generator().manual_seed(20261003); per item (bench order
  0..59) draw randint(0,4). If drawn branch degenerate (unspecified edge case),
  re-draw until non-degenerate; documented in RUN_REPORT.
- SC ties: toward B0's answer (pre-reg); if B0 degenerate, lowest-index
  non-degenerate branch (unspecified edge case, documented).
"""
import hashlib, json, math, os, sys, time
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from scipy import stats as scipy_stats

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(RUN_DIR, exist_ok=True)
LOGF = open(os.path.join(RUN_DIR, "stage1_run_log.txt"), "w")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOGF.write(line + "\n"); LOGF.flush()

# ============ pre-reg §2 pinned constants ============
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df"
HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
MODEL_ID = "EleutherAI/pythia-410m"
R_MAX = 48
S_B2, S_B3 = 20261004, 20261005
S_PERM_C2 = 20261006
S_RANDOM = 20261003
N_ITEMS = 60
N_BRANCHES = 4

torch.manual_seed(20261003)
torch.set_num_threads(max(1, (os.cpu_count() or 4) - 1))
log("threads=%d" % torch.get_num_threads())

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

def run_invalid(reason):
    log("RUN-INVALID: %s" % reason)
    json.dump({"verdict": "RUN-INVALID", "reason": reason,
               "forwards": FWD_COUNT[0], "generations": GEN_COUNT[0]},
              open(os.path.join(RUN_DIR, "stage1_verdict.json"), "w"), indent=1)
    LOGF.close()
    sys.exit(44)

# ============ model (pre-reg §2 verbatim) ============
log("loading model %s rev %s (float32, cpu, local_files_only)" % (MODEL_ID, HF_REVISION))
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=HF_REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, revision=HF_REVISION, local_files_only=True,
    torch_dtype=torch.float32, device_map="cpu")
model.eval()
pre_hash = sha256_state_dict(model)
log("backbone pre-hash: %s" % pre_hash)
if pre_hash != BACKBONE_PIN:
    run_invalid("(b) backbone pre-hash mismatch: got %s" % pre_hash)
log("(b) backbone pin PASS")

def tok1(s):
    ids = tokenizer.encode(" " + s)
    assert len(ids) == 1, "multi-token: %r -> %r" % (s, ids)
    return ids[0]

# ============ bench (verbatim port of run_exp135.py via EXP139) ============
SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Joel", "Gideon", "Ruth", "Abel"],
    "V3_Greek": ["Ajax", "Jason", "Apollo", "Paris", "Atlas"],
    "V4_Roman": ["Marcus", "Julius", "Augustus", "Felix", "Diana"],
    "V5_Modern": ["Liam", "Noah", "Eli", "Maya", "Finn"],
}
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())
NOVEL_VOCAB_PLANET = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
NOVEL_VOCAB_ELEMENT = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
TRIPLES_INDICES = [
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
]
QUADS_INDICES = [
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
]
def build_bench():
    bench = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = "%s or %s" % (A, C) if target_first else "%s or %s" % (C, A)
        if i < 8:
            p = "Premise: %s outranks %s. %s outranks %s. Question: Who is higher in rank, %s? Answer:" % (A, B, B, C, q_opts)
        else:
            p = "Premise: %s is lower than %s. %s is lower than %s. Question: Who is higher in rank, %s? Answer:" % (C, B, B, A, q_opts)
        bench.append({"id": "exp077_planet_2hop_%d" % i, "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "planet", "hop": 2, "domain": "Planetary",
                      "idx": (iA, iB, iC), "tfirst": target_first, "variant": "outranks" if i < 8 else "lower"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                          NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        target_first = (i % 2 == 1)
        q_opts = "%s or %s" % (A, D_ent) if target_first else "%s or %s" % (D_ent, A)
        if i < 8:
            p = ("Premise: %s outranks %s. %s outranks %s. %s outranks %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (A, B, B, C, C, D_ent, q_opts)
        else:
            p = ("Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (D_ent, C, C, B, B, A, q_opts)
        bench.append({"id": "exp077_planet_3hop_%d" % i, "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "planet", "hop": 3, "domain": "Planetary",
                      "idx": (iA, iB, iC, iD), "tfirst": target_first, "variant": "outranks" if i < 8 else "lower"})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = "%s or %s" % (A, C) if target_first else "%s or %s" % (C, A)
        if i < 7:
            p = "Premise: %s outranks %s. %s outranks %s. Question: Who is higher in rank, %s? Answer:" % (A, B, B, C, q_opts)
        else:
            p = "Premise: %s is lower than %s. %s is lower than %s. Question: Who is higher in rank, %s? Answer:" % (C, B, B, A, q_opts)
        bench.append({"id": "exp077_element_2hop_%d" % i, "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "element", "hop": 2, "domain": "Elemental",
                      "idx": (iA, iB, iC), "tfirst": target_first, "variant": "outranks" if i < 7 else "lower"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                          NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        target_first = (i % 2 == 0)
        q_opts = "%s or %s" % (A, D_ent) if target_first else "%s or %s" % (D_ent, A)
        if i < 7:
            p = ("Premise: %s outranks %s. %s outranks %s. %s outranks %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (A, B, B, C, C, D_ent, q_opts)
        else:
            p = ("Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (D_ent, C, C, B, B, A, q_opts)
        bench.append({"id": "exp077_element_3hop_%d" % i, "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "element", "hop": 3, "domain": "Elemental",
                      "idx": (iA, iB, iC, iD), "tfirst": target_first, "variant": "outranks" if i < 7 else "lower"})
    return bench

bench = build_bench()
assert len(bench) == 60, "bench len %d != 60" % len(bench)
bench_hash = hashlib.sha256(json.dumps(
    [{k: bench[i][k] for k in ("id", "prompt", "A", "C")} for i in range(len(bench))],
    sort_keys=True).encode()).hexdigest()
log("(a) bench len=60; bench sha256=%s" % bench_hash)
if bench_hash != BENCH_PIN:
    run_invalid("(a) bench sha256 mismatch: got %s" % bench_hash)
log("(a) bench pin PASS")

def make_views(it, src_ents):
    views = []
    for vk in VOCAB_KEYS:
        sub = dict(zip(src_ents, [SUPPORT_VOCABULARIES[vk][k] for k in it["idx"]]))
        prompt = it["prompt"]
        for old, new in sub.items():
            assert old in prompt, "substitution source missing: %s" % old
            prompt = prompt.replace(old, new)
        views.append({"prompt": prompt, "vk": vk, "A": sub[it["A"]], "C": sub[it["C"]]})
    return views

def novel_src(it):
    base = NOVEL_VOCAB_PLANET if it["typ"] == "planet" else NOVEL_VOCAB_ELEMENT
    return [base[k] for k in it["idx"]]

# view 0 for all 60 items (pre-reg §2: "All 60 items in canonical bench order, view 0")
items = [make_views(it, novel_src(it))[0] for it in bench]

# single-token assertion for all entity names (view 0)
for ii, v in enumerate(items):
    tok1(v["A"]); tok1(v["C"])
log("tok1 single-token assertion PASS for all 60 view-0 A/C names")

# ============ branch prompts (pre-reg §2) ============
TEMPLATE = " Reason step by step, then answer:"
SUFFIX = "\nAnswer:"

def b1_swap_question(view_prompt, A_text, C_text):
    """Swap the two option texts in the question only (pre-reg §2, §10.7).
    Premise untouched: swapping premise facts would flip the correct entity."""
    qi = view_prompt.index("Question:")
    head, tail = view_prompt[:qi], view_prompt[qi:]
    pat_AC = "%s or %s" % (A_text, C_text)
    pat_CA = "%s or %s" % (C_text, A_text)
    if pat_AC in tail and pat_CA not in tail:
        tail = tail.replace(pat_AC, pat_CA)
    elif pat_CA in tail and pat_AC not in tail:
        tail = tail.replace(pat_CA, pat_AC)
    else:
        run_invalid("B1 swap ambiguous on item: %r" % view_prompt)
    return head + tail

branch_prompts = []  # per item: [P_B0, P_B1, P_B2, P_B3]
for ii, v in enumerate(items):
    p0 = v["prompt"] + TEMPLATE
    p1 = b1_swap_question(v["prompt"], v["A"], v["C"]) + TEMPLATE
    # verify: premise unchanged, swap involutive
    qi = v["prompt"].index("Question:")
    assert p1[:qi] == v["prompt"][:qi]
    assert b1_swap_question(p1[:len(p1)-len(TEMPLATE)], v["A"], v["C"]) == v["prompt"]
    branch_prompts.append([p0, p1, p0, p0])  # B2/B3 share B0's prompt, differ by sampling
log("branch prompts built (B1 swap verified involutive, premise-unchanged, all 60)")

t_A_list = [tok1(v["A"]) for v in items]
t_C_list = [tok1(v["C"]) for v in items]
suffix_ids = tokenizer.encode(SUFFIX)

# ============ generation (pre-reg §2) ============
def generate_rationale(prompt, branch):
    inputs = tokenizer(prompt, return_tensors="pt")
    prompt_ids = inputs["input_ids"][0].tolist()
    gen_kwargs = dict(max_new_tokens=R_MAX, pad_token_id=tokenizer.eos_token_id)
    if branch in (2, 3):
        # transformers 5.17 generate() takes no `generator` kwarg; seed the global
        # torch RNG to the pinned seed before each stochastic generation.
        # Deterministic per (item, branch): output depends only on the pinned seed
        # and the prompt, never on execution order. (Law #13: seeds pinned, C1.)
        torch.manual_seed(S_B2 if branch == 2 else S_B3)
        gen_kwargs.update(do_sample=True, temperature=0.7)
    else:
        gen_kwargs.update(do_sample=False)
    with torch.no_grad():
        out = model.generate(**inputs, **gen_kwargs)
    GEN_COUNT[0] += 1
    prompt_len = inputs["input_ids"].shape[1]
    return prompt_ids, out[0][prompt_len:].tolist()

# ============ scoring (pre-reg §2: folded teacher-forced pass) ============
def score_branch(prompt_ids, rationale_ids, t_A, t_C):
    """Returns (F_k, F_full_k, a_k). F_k=None iff rationale empty (degenerate)."""
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
records = []  # per item: {branches: [{F, F_full, a, n_rat, degenerate}], ...}
degenerate_pairs = 0
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
        branches.append({"k": k, "n_rat": len(rat),
                         "F": F_k, "F_full": F_full, "a": a_k,
                         "correct": (a_k == t_A) if not deg else None,
                         "degenerate": deg,
                         "rationale_ids": rat,
                         "rationale_text": tokenizer.decode(rat)})
    records.append({"item": ii, "id": bench[ii]["id"], "t_A": t_A, "t_C": t_C,
                    "branches": branches})
    if (ii + 1) % 10 == 0:
        log("items %d/60; gens=%d fwds=%d; %.1fs elapsed" %
            (ii + 1, GEN_COUNT[0], FWD_COUNT[0], time.time() - t0))
log("generation+scoring complete: gens=%d fwds=%d degenerate_pairs=%d" %
    (GEN_COUNT[0], FWD_COUNT[0], degenerate_pairs))

# validity: 240/240
if GEN_COUNT[0] != 240 or FWD_COUNT[0] != 240:
    run_invalid("pass count mismatch: gens=%d fwds=%d (expected 240/240)" %
                (GEN_COUNT[0], FWD_COUNT[0]))
log("pass counts 240/240 PASS")

# validity gate (c): determinism spot-check — re-run B0 on items 0, 30, 59
for ii in (0, 30, 59):
    _, rat2 = generate_rationale(branch_prompts[ii][0], 0)
    GEN_COUNT[0] += 1  # not counted in the 240 budget (diagnostic, pre-reg §3 gate (c))
    if rat2 != records[ii]["branches"][0]["rationale_ids"]:
        run_invalid("(c) determinism spot-check failed on item %d" % ii)
log("(c) determinism spot-check PASS (items 0, 30, 59 byte-identical)")

# validity gate (d): post-run backbone hash (Δθ=0)
post_hash = sha256_state_dict(model)
log("backbone post-hash: %s" % post_hash)
if post_hash != BACKBONE_PIN:
    run_invalid("(d) backbone post-hash mismatch: Δθ != 0")
log("(d) Δθ=0 PASS")

# ============ per-item aggregates ============
fully_degenerate_items = 0
for rec in records:
    valid = [b for b in rec["branches"] if not b["degenerate"]]
    if len(valid) == 0:
        fully_degenerate_items += 1
        rec["F_bar"] = None
        rec["acc"] = None
        rec["k_star"] = None
        continue
    Fs = [b["F"] for b in valid]
    rec["F_bar"] = sum(Fs) / len(Fs)
    rec["F_full_bar"] = sum(b["F_full"] for b in valid) / len(valid)
    rec["min_F"] = min(Fs)
    rec["min_F_full"] = min(b["F_full"] for b in valid)
    rec["acc"] = sum(1 for b in valid if b["correct"]) / len(valid)
    # selection: argmin F over non-degenerate, ties -> lowest index
    best = min(valid, key=lambda b: (b["F"], b["k"]))
    rec["k_star"] = best["k"]
    rec["spread"] = max(Fs) - min(Fs)

if fully_degenerate_items >= 3:
    run_invalid("pilot VOID: %d fully-degenerate items (>=3)" % fully_degenerate_items)
log("fully-degenerate items: %d" % fully_degenerate_items)

# ============ G1 diversity ============
g1_items = sum(1 for rec in records
               if rec["F_bar"] is not None and
               len(set(b["a"] for b in rec["branches"] if not b["degenerate"])) >= 2)
G1_PASS = g1_items >= 15
log("G1: %d/60 items with >=2 distinct answers (bar >=15) -> %s" %
    (g1_items, "PASS" if G1_PASS else "FAIL"))

# ============ G2 variance ============
spreads = [rec["spread"] for rec in records if rec["spread"] is not None]
median_spread = float(np.median(spreads))
G2_PASS = median_spread >= 0.05
log("G2: median F-spread = %.6f nats/token (bar >=0.05) -> %s" %
    (median_spread, "PASS" if G2_PASS else "FAIL"))

# ============ G3 calibration (Law #7: labels only in instrument) ============
g3_items = [rec for rec in records if rec["F_bar"] is not None]
F_bars = np.array([rec["F_bar"] for rec in g3_items])
accs = np.array([rec["acc"] for rec in g3_items])
min_Fs = np.array([rec["min_F"] for rec in g3_items])
n_g3 = len(g3_items)
log("G3 instrument: n=%d items" % n_g3)

# C1: Spearman(F_bar, acc), one-sided negative
rho, two_p = scipy_stats.spearmanr(F_bars, accs)
if rho < 0:
    p_lic_c1 = two_p / 2.0
    p_inv_c1 = 1.0 - two_p / 2.0
else:
    p_lic_c1 = 1.0 - two_p / 2.0
    p_inv_c1 = two_p / 2.0
C1_PASS = (rho < 0) and (p_lic_c1 < 0.05)
C1_INV = (rho > 0) and (p_inv_c1 < 0.05)
log("C1: Spearman(F_bar, acc) rho=%.4f one-sided p_lic=%.6f p_inv=%.6f -> %s" %
    (rho, p_lic_c1, p_inv_c1, "PASS" if C1_PASS else ("INVERTED" if C1_INV else "NULL")))

# C2: TESTA-style partition, permutation test, seed pinned
wrong_mask = accs <= 0.5
right_mask = accs >= 0.75
n_wrong, n_right = int(wrong_mask.sum()), int(right_mask.sum())
log("C2 partition: n_wrong=%d (acc<=0.5), n_right=%d (acc>=0.75)" % (n_wrong, n_right))
C2_PASS, C2_INV, p_lic_c2, p_inv_c2, D_obs = False, False, 1.0, 1.0, float("nan")
if n_wrong == 0 or n_right == 0:
    log("C2: UNDEFINED (empty group) -> treated as NULL per gate logic")
else:
    D_obs = float(F_bars[wrong_mask].mean() - F_bars[right_mask].mean())
    rng = np.random.default_rng(S_PERM_C2)
    pooled = F_bars
    labels = np.concatenate([np.ones(n_wrong), np.zeros(n_right)])
    # permute which F_bar values fall in the wrong group
    idx_wrong = np.where(wrong_mask)[0]
    idx_right = np.where(right_mask)[0]
    all_idx = np.concatenate([idx_wrong, idx_right])
    vals = F_bars[all_idx]
    n_perm = 100000
    ge = 0
    le = 0
    for _ in range(n_perm):
        perm = rng.permutation(vals)
        d = perm[:n_wrong].mean() - perm[n_wrong:].mean()
        if d >= D_obs:
            ge += 1
        if d <= D_obs:
            le += 1
    p_lic_c2 = ge / n_perm   # licensed direction: D > 0
    p_inv_c2 = le / n_perm   # inverted: D < 0
    C2_PASS = (D_obs > 0) and (p_lic_c2 < 0.05)
    C2_INV = (D_obs < 0) and (p_inv_c2 < 0.05)
    log("C2: D_obs=%.6f p_lic=%.6f p_inv=%.6f -> %s" %
        (D_obs, p_lic_c2, p_inv_c2, "PASS" if C2_PASS else ("INVERTED" if C2_INV else "NULL")))

G3_PASS = C1_PASS and C2_PASS
G3_INV = C1_INV or C2_INV
log("G3: C1=%s C2=%s -> %s" % (
    "PASS" if C1_PASS else ("INVERTED" if C1_INV else "NULL"),
    "PASS" if C2_PASS else ("INVERTED" if C2_INV else "NULL"),
    "PASS" if G3_PASS else ("INVERTED-KILL" if G3_INV else "FAIL-null")))

# ============ secondary diagnostic (C5): same on min_k F ============
rho_m, two_p_m = scipy_stats.spearmanr(min_Fs, accs)
if rho_m < 0:
    p_lic_m, p_inv_m = two_p_m / 2.0, 1.0 - two_p_m / 2.0
else:
    p_lic_m, p_inv_m = 1.0 - two_p_m / 2.0, two_p_m / 2.0
if n_wrong == 0 or n_right == 0:
    D_obs_m, p_lic_m2, p_inv_m2 = float("nan"), 1.0, 1.0
else:
    D_obs_m = float(min_Fs[wrong_mask].mean() - min_Fs[right_mask].mean())
    rng2 = np.random.default_rng(S_PERM_C2 + 1)  # distinct stream, documented
    vals_m = min_Fs[np.concatenate([np.where(wrong_mask)[0], np.where(right_mask)[0]])]
    ge = le = 0
    for _ in range(100000):
        perm = rng2.permutation(vals_m)
        d = perm[:n_wrong].mean() - perm[n_wrong:].mean()
        if d >= D_obs_m:
            ge += 1
        if d <= D_obs_m:
            le += 1
    p_lic_m2, p_inv_m2 = ge / 100000.0, le / 100000.0
min_inv = ((rho_m > 0) and (p_inv_m < 0.05)) or \
          ((n_wrong > 0 and n_right > 0) and (D_obs_m < 0) and (p_inv_m2 < 0.05))
log("secondary min-F: rho=%.4f p_lic=%.6f | D=%.6f p_lic=%.6f -> min-inverted=%s" %
    (rho_m, p_lic_m, D_obs_m, p_lic_m2, min_inv))

# ============ comparators (diagnostic; Stage-2 bars NOT applied) ============
# min-F selection accuracy
fe_correct = sum(1 for rec in records if rec["k_star"] is not None and
                 [b for b in rec["branches"] if b["k"] == rec["k_star"]][0]["correct"])
b0_correct = sum(1 for rec in records
                 if not rec["branches"][0]["degenerate"] and rec["branches"][0]["correct"])
n_scored = sum(1 for rec in records if rec["F_bar"] is not None)
acc_FE = fe_correct / n_scored
acc_B0 = b0_correct / n_scored
# random-branch
gr = torch.Generator().manual_seed(S_RANDOM)
rand_correct = 0
for rec in records:
    if rec["F_bar"] is None:
        continue
    valid_ks = [b["k"] for b in rec["branches"] if not b["degenerate"]]
    k = int(torch.randint(0, 4, (1,), generator=gr).item())
    while k not in valid_ks:  # degenerate re-draw (documented edge case)
        k = int(torch.randint(0, 4, (1,), generator=gr).item())
    b = [x for x in rec["branches"] if x["k"] == k][0]
    rand_correct += 1 if b["correct"] else 0
acc_rand = rand_correct / n_scored
# self-consistency
sc_correct = 0
for rec in records:
    if rec["F_bar"] is None:
        continue
    valid = [b for b in rec["branches"] if not b["degenerate"]]
    votes = sum(1 for b in valid if b["correct"])
    n_v = len(valid)
    if votes * 2 > n_v:
        sc_ans_correct = True
    elif votes * 2 < n_v:
        sc_ans_correct = False
    else:
        b0b = rec["branches"][0]
        sc_ans_correct = b0b["correct"] if not b0b["degenerate"] else valid[0]["correct"]
    sc_correct += 1 if sc_ans_correct else 0
acc_SC = sc_correct / n_scored
sel_freq = [sum(1 for rec in records if rec["k_star"] == k) for k in range(4)]
log("diagnostic acc: B0=%.4f FE=%.4f rand=%.4f SC=%.4f (n=%d)" %
    (acc_B0, acc_FE, acc_rand, acc_SC, n_scored))
log("selection frequency per branch: %s" % sel_freq)
log("dM_FE=%.4f dM_rand=%.4f dM_SC=%.4f (diagnostic only; Stage-2 bars NOT applied)" %
    (acc_FE - acc_B0, acc_rand - acc_B0, acc_SC - acc_B0))

# ============ gate verdict (Stage-1 only) ============
if G3_INV:
    gate_reading = "KILL-FAMILY (G3 inverted)"
elif not (G1_PASS and G2_PASS):
    gate_reading = "HELD (G1/G2 fail: %s%s)" % (
        "" if G1_PASS else "G1", "" if G2_PASS else "G2")
elif not G3_PASS:
    gate_reading = "HELD (G3 null: C1=%s C2=%s)" % (
        "pass" if C1_PASS else "null", "pass" if C2_PASS else "null")
else:
    gate_reading = "GATES-PASS (G1+G2+G3 in licensed direction; Stage-2 gate opens, needs CEO+GPU)"
log("STAGE-1 GATE READING: %s" % gate_reading)
if G3_PASS and min_inv:
    log("C5 NOTE: mean-F passes G3 but min-F inverts -> binding consequence is "
        "Stage-2 KILL-selector bar (dM_FE <= dM_random); mean-calibration is not a selection license")

# ============ records ============
serial = []
for rec in records:
    serial.append({
        "item": rec["item"], "id": rec["id"],
        "F_bar": rec["F_bar"], "F_full_bar": rec.get("F_full_bar"),
        "min_F": rec.get("min_F"), "min_F_full": rec.get("min_F_full"),
        "acc": rec["acc"], "k_star": rec["k_star"], "spread": rec.get("spread"),
        "branches": [{"k": b["k"], "n_rat": b["n_rat"], "F": b["F"],
                      "F_full": b["F_full"], "correct": b["correct"],
                      "degenerate": b["degenerate"],
                      "rationale_ids": b["rationale_ids"],
                      "rationale_text": b["rationale_text"]} for b in rec["branches"]],
    })
out = {
    "experiment": "EXP140",
    "prereg": "research/prereg/EXP_S45_prereg_DRAFT_2026-10-03.md (SIGNED, LOG-4887)",
    "pins": {"backbone_pre": pre_hash, "backbone_post": post_hash, "bench": bench_hash,
             "hf_revision": HF_REVISION, "model": MODEL_ID, "dtype": "float32"},
    "seeds": {"S_B2": S_B2, "S_B3": S_B3, "S_PERM_C2": S_PERM_C2, "S_RANDOM": S_RANDOM},
    "counts": {"generations": 240, "forwards": 240, "diagnostic_gens": GEN_COUNT[0] - 240,
               "degenerate_pairs": degenerate_pairs,
               "fully_degenerate_items": fully_degenerate_items},
    "gates": {
        "G1": {"items_ge2_answers": g1_items, "bar": 15, "pass": G1_PASS},
        "G2": {"median_spread": median_spread, "bar": 0.05, "pass": G2_PASS},
        "G3": {
            "n": n_g3,
            "C1": {"rho": float(rho), "p_lic": float(p_lic_c1), "p_inv": float(p_inv_c1),
                   "pass": bool(C1_PASS), "inverted": bool(C1_INV)},
            "C2": {"n_wrong": n_wrong, "n_right": n_right, "D_obs": float(D_obs),
                   "p_lic": float(p_lic_c2), "p_inv": float(p_inv_c2),
                   "pass": bool(C2_PASS), "inverted": bool(C2_INV)},
            "pass": bool(G3_PASS), "inverted": bool(G3_INV)},
        "secondary_minF": {"rho": float(rho_m), "p_lic": float(p_lic_m),
                           "D_obs": float(D_obs_m), "p_lic_c2": float(p_lic_m2),
                           "inverted": bool(min_inv)},
    },
    "diagnostic_acc": {"n": n_scored, "B0": acc_B0, "FE": acc_FE,
                       "random": acc_rand, "SC": acc_SC,
                       "dM_FE": acc_FE - acc_B0, "dM_rand": acc_rand - acc_B0,
                       "dM_SC": acc_SC - acc_B0,
                       "selection_freq": sel_freq},
    "gate_reading": gate_reading,
    "items": serial,
}
json.dump(out, open(os.path.join(RUN_DIR, "stage1_records.json"), "w"), indent=1)
json.dump({"experiment": "EXP140", "gate_reading": gate_reading,
           "G1": bool(G1_PASS), "G2": bool(G2_PASS),
           "G3": bool(G3_PASS), "G3_inverted": bool(G3_INV),
           "forwards": FWD_COUNT[0], "generations": GEN_COUNT[0]},
          open(os.path.join(RUN_DIR, "stage1_verdict.json"), "w"), indent=1)
log("records written; DONE")
LOGF.close()
