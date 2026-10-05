#!/usr/bin/env python3
"""S7-3 analysis EXECUTION — label-free signal inventory battery.

Executes EXACTLY per research/analysis_plans/S7-3_PREREG_DRAFT_2026-10-05.md
(Law #14 SIGN, LOG-4912). $0 CPU, ZERO new forward passes, all archives read-only.
Abort conditions from Step 0 are binding: any trip -> INCONCLUSIVE, no workaround.
"""
import hashlib, json, math, os, sys, warnings
import numpy as np
from scipy.stats import spearmanr, rankdata, norm

os.environ["HF_HUB_OFFLINE"] = "1"
from transformers import AutoTokenizer  # tokenizer load only: integer tok1 mapping, no forwards

REPO = os.path.expanduser("~/workspace/SCBI")
D1_PATH = os.path.join(REPO, "experiments/runs/EXP135_eval/out/exp135_records.json")
D2_PATH = os.path.join(REPO, "experiments/runs/EXP140_stage1/stage1_records.json")
BENCH_SHA_EXPECTED = "eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df"  # ERRATUM LOG-4914: was ...b55a... (typo); corrected per committed exp135_report.json
PERM_SEED = 20261005
N_PERM = 100000
ALPHA = 0.05 / 6.0
RHO_FLOOR = 0.3
CONDS = ["C1","C2","C3","C4","C5","C6","C7","C8","C9","cache_unintervened"]

def abort(reason):
    print("ABORT (Step 0): %s" % reason, flush=True)
    rec = {"verdict": "INCONCLUSIVE", "abort_reason": reason}
    json.dump(rec, open(os.path.join(REPO, "research/analysis_plans/S7-3_RESULTS_2026-10-05.json"), "w"), indent=1)
    sys.exit(44)

# ---------- §8 pinned unit check: spearmanr tie behavior ----------
s1 = spearmanr([1,2,3,4,5],[1,2,3,4,5]).statistic
s2 = spearmanr([1,2,2,4,5],[1,2,3,4,5]).statistic
assert abs(s1 - 1.0) < 1e-9, "toy perfect-correlation check failed: %r" % s1
assert abs(s2 - 0.9746794344808963) < 1e-12, "toy tie-handling check failed: %r" % s2
print("toy-vector unit check PASS (spearmanr tie behavior pinned)", flush=True)

# ---------- verbatim bench/view replication (no torch; string ops only) ----------
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

def item_signature(it):
    parts = it["id"].split("_")
    domain, hop, i = parts[1], int(parts[2][0]), int(parts[3])
    vocab = NOVEL_VOCAB_PLANET if domain == "planet" else NOVEL_VOCAB_ELEMENT
    idx = it["idx"]
    ents = [vocab[k] for k in idx]
    slot = "planet" if domain == "planet" else "element"
    return {"template": it["variant"] + "_%dhop" % hop, "ents": ents,
            "slots": [slot] * len(ents), "domain": domain, "hop": hop}

bench = build_bench()
assert len(bench) == 60, "bench len %d != 60" % len(bench)
bench_hash = hashlib.sha256(json.dumps(
    [{k: bench[i][k] for k in ("id", "prompt", "A", "C")} for i in range(len(bench))],
    sort_keys=True).encode()).hexdigest()
if bench_hash != BENCH_SHA_EXPECTED:
    abort("bench sha256 mismatch: got %s expected %s" % (bench_hash, BENCH_SHA_EXPECTED))
print("Step 0: bench sha256 PASS (%s...)" % bench_hash[:12], flush=True)

# exclusion check (view precondition); D1 indexes included_items in order -> need e=0
excluded = 0
for it in bench:
    try:
        sig = item_signature(it)
        assert all(e in it["prompt"] for e in sig["ents"])
    except Exception:
        excluded += 1
if excluded != 0:
    abort("view-precondition exclusions=%d != 0; record/item alignment unverifiable" % excluded)

# ---------- Step 0.1/0.2: load + structural asserts ----------
d1 = json.load(open(D1_PATH))
assert set(d1.keys()) == set(CONDS), "D1 condition keys mismatch: %s" % sorted(d1.keys())
for c in CONDS:
    assert len(d1[c]) == 60, "D1 %s: %d items" % (c, len(d1[c]))
    for ii, views in enumerate(d1[c]):
        assert len(views) == 5, "D1 %s item %d: %d views" % (c, ii, len(views))
        for j, v in enumerate(views):
            assert set(v.keys()) == {"yhat", "margin"}, "D1 %s/%d/%d keys %s" % (c, ii, j, v.keys())
            m = v["margin"]
            assert m is not None and not (isinstance(m, float) and math.isnan(m)), "D1 NaN margin"
            assert isinstance(v["yhat"], int), "D1 non-int yhat"
print("Step 0.1 PASS: D1 = 10 conditions x 60 items x 5 views, all {yhat, margin}, no NaN/None", flush=True)

d2 = json.load(open(D2_PATH))["items"]
assert len(d2) == 60
for ii, it in enumerate(d2):
    assert len(it["branches"]) == 4, "D2 item %d: %d branches" % (ii, len(it["branches"]))
    assert it["spread"] is not None and math.isfinite(it["spread"]), "D2 bad spread item %d" % ii
    assert it["acc"] is not None, "D2 null acc item %d" % ii
    mean_c = sum(1 for b in it["branches"] if b["correct"]) / 4.0
    if abs(it["acc"] - mean_c) > 1e-9:
        abort("D2 item %d acc cross-check failed: acc=%r mean(correct)=%r" % (ii, it["acc"], mean_c))
print("Step 0.2 PASS: D2 = 60 items x 4 branches, spread/acc present, acc==mean(correct) all items", flush=True)

# ---------- Step 0.3: tok1 mapping (tokenizer load only, zero forwards) + yhat check ----------
tokenizer = AutoTokenizer.from_pretrained(
    "EleutherAI/pythia-410m", revision="9879c9b5f8bea9051dcb0e68dff21493d67e9d4f",
    local_files_only=True)

def tok1(s):
    ids = tokenizer.encode(" " + s)
    assert len(ids) == 1, "multi-token entity: %s" % s
    return ids[0]

def novel_src(it):
    base = NOVEL_VOCAB_PLANET if it["typ"] == "planet" else NOVEL_VOCAB_ELEMENT
    return [base[k] for k in it["idx"]]

view_tok = []  # per item: per view: (tA, tC)
for it in bench:
    src_ents = novel_src(it)
    vt = []
    for vk in VOCAB_KEYS:
        sub = dict(zip(src_ents, [SUPPORT_VOCABULARIES[vk][k] for k in it["idx"]]))
        vt.append((tok1(sub[it["A"]]), tok1(sub[it["C"]])))
    view_tok.append(vt)

mism = 0
for c in CONDS:
    for ii in range(60):
        for j in range(5):
            y = d1[c][ii][j]["yhat"]
            tA, tC = view_tok[ii][j]
            if y != tA and y != tC:
                mism += 1
if mism != 0:
    abort("yhat membership check: %d mismatches (allowed 0)" % mism)
print("Step 0.3 PASS: all 3000 D1 yhat in {tok1(A), tok1(C)} per (item, view), 0 mismatches", flush=True)

# ---------- Step 1: signal computation ----------
cache = d1["cache_unintervened"]
def modal_agree(yhats):
    counts = {}
    for y in yhats:
        counts[y] = counts.get(y, 0) + 1
    top = max(counts.values())
    mode = min(y for y, n in counts.items() if n == top)  # pre-registered tie-break: smallest token id
    return sum(1 for y in yhats if y == mode) / len(yhats)

S = {k: [] for k in ["S1","S2","S3","S4","S5","S6"]}
for ii in range(60):
    margins_cache = [v["margin"] for v in cache[ii]]
    yhats_cache = [v["yhat"] for v in cache[ii]]
    S["S1"].append(float(np.std(margins_cache, ddof=1)))
    S["S2"].append(modal_agree(yhats_cache))
    agrees = [modal_agree([v["yhat"] for v in d1[c][ii]]) for c in CONDS]
    S["S3"].append(float(np.mean(agrees)))
    m45 = [v["margin"] for c in CONDS[:9] for v in d1[c][ii]]
    assert len(m45) == 45
    S["S4"].append(float(np.mean(m45)))
for it in d2:
    S["S5"].append(float(it["spread"]))
    S["S6"].append(sum(1 for b in it["branches"] if b["degenerate"]) / 4.0)

# Step 0.4 missing-data rule (pre-registered; expected vacuous)
untestable = []
for k in S:
    arr = np.array(S[k], dtype=float)
    miss = np.isnan(arr).sum()
    if miss > 6:
        untestable.append(k)
print("Step 1 PASS: 60x6 signal matrix computed; missing/item: all 0; untestable: %s" % untestable, flush=True)

# ---------- Step 2: screening targets (Law #7: labels enter ONLY here) ----------
T1 = []  # TESTA majority-correct partition on cache views
for ii in range(60):
    ncorr = sum(1 for j in range(5) if cache[ii][j]["yhat"] == view_tok[ii][j][0])
    T1.append(1 if ncorr >= 3 else 0)
T2 = [sum(1 for b in it["branches"] if b["correct"]) / 4.0 for it in d2]
print("Step 2 PASS: T1 ones=%d/60 (TESTA convention), T2 graded target computed" % sum(T1), flush=True)
TARGET = {"S1": T1, "S2": T1, "S3": T1, "S4": T1, "S5": T2, "S6": T2}

# ---------- Step 3: statistics ----------
def fisher_ci(rho, n, zcrit=1.959963984540054):
    if not math.isfinite(rho) or abs(rho) >= 1.0:
        return (float("nan"), float("nan"))
    z = math.atanh(rho)
    se = 1.0 / math.sqrt(n - 3)
    return (math.tanh(z - zcrit * se), math.tanh(z + zcrit * se))

results = {}
for k in ["S1","S2","S3","S4","S5","S6"]:
    sig = np.array(S[k], dtype=float)
    tgt = np.array(TARGET[k], dtype=float)
    if np.std(sig) < 1e-12:  # tolerance-based: S2/S3 are constant 0.2 by construction (views use disjoint vocabs -> modal raw-id agreement always 1/5); fp noise made std ~8e-17, not exactly 0.0
        results[k] = {"rho": None, "p": None, "ci95": [None, None],
                      "note": "DEGENERATE: zero signal variance across 60 items (constant); rho undefined",
                      "significant": False}
        print("%s: DEGENERATE (constant signal) -> fails bar" % k, flush=True)
        continue
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rho = float(spearmanr(sig, tgt).statistic)
    rs = rankdata(sig)
    rt = rankdata(tgt)
    rng = np.random.default_rng(PERM_SEED)  # fresh identical stream per signal (plan: identical procedure)
    perms = np.stack([rng.permutation(60) for _ in range(N_PERM)])
    rt_p = rt[perms]
    rs_c = rs - rs.mean()
    rt_c = rt_p - rt_p.mean(axis=1, keepdims=True)
    denom = math.sqrt(float((rs_c ** 2).sum())) * np.sqrt((rt_c ** 2).sum(axis=1))
    rho_p = (rs_c @ rt_c.T) / denom
    # self-check: vectorized observed |rho| must match scipy
    rho_obs_vec = abs(float((rs_c @ (rt - rt.mean())) /
                            (math.sqrt(float((rs_c ** 2).sum())) * math.sqrt(float(((rt - rt.mean()) ** 2).sum())))))
    assert abs(rho_obs_vec - abs(rho)) < 1e-9, "%s vectorized/scipy rho mismatch" % k
    ge = int((np.abs(rho_p) >= abs(rho)).sum())
    p = (ge + 1) / (N_PERM + 1)
    lo, hi = fisher_ci(rho, 60)
    sig_bar = (p < ALPHA) and (abs(rho) >= RHO_FLOOR)
    results[k] = {"rho": rho, "p": p, "ci95": [lo, hi],
                  "n_perm_ge": ge, "significant": bool(sig_bar)}
    print("%s: rho=%+.4f p=%.6f CI=[%+.4f,%+.4f] %s" %
          (k, rho, p, lo, hi, "PASS-BAR" if sig_bar else "fail-bar"), flush=True)

# Step 3.4: minimum detectable |rho| at 80% power, n=60, alpha=0.00833 (two-sided, Fisher-z closed form)
mde = math.tanh((norm.ppf(1 - ALPHA / 2) + norm.ppf(0.8)) / math.sqrt(57))
print("Step 3.4 MDE: min |rho| at 80%% power (n=60, alpha=%.6f) = %.4f" % (ALPHA, mde), flush=True)

# ---------- Step 4: decision (§5) ----------
testable = [k for k in results if k not in untestable and results[k]["rho"] is not None]
hits = [k for k in testable if results[k]["significant"]]
if len(untestable) >= 2:
    verdict = "INCONCLUSIVE"
    reason = ">=2 signals UNTESTABLE per Step 0.4"
elif hits:
    verdict = "CONTINUE"
    reason = "signal(s) %s meet the bar (|rho|>=0.3 and p<0.008333)" % hits
else:
    verdict = "KILL"
    reason = ("all six signals fail the bar on this 60-item bench family; "
              "scoped reading: no signal >=0.3 detectable at n=60; no generalization beyond this bench family")

out = {
    "analysis": "S7-3", "plan": "research/analysis_plans/S7-3_PREREG_DRAFT_2026-10-05.md",
    "date": "2026-10-05", "verdict": verdict, "verdict_reason": reason,
    "thresholds": {"p_bar": ALPHA, "rho_floor": RHO_FLOOR, "n_perm": N_PERM, "perm_seed": PERM_SEED},
    "signals": {k: S[k] for k in S},
    "targets": {"T1_binary": T1, "T2_graded": T2},
    "per_signal": results,
    "untestable": untestable,
    "mde_80pct": mde,
    "pins": {"python": "3.12", "numpy": "2.5.3", "scipy": "1.18.1",
             "bench_sha256": BENCH_SHA_EXPECTED,
             "tokenizer": "EleutherAI/pythia-410m@9879c9b5f8bea9051dcb0e68dff21493d67e9d4f (tok1 mapping only, zero forwards)"},
    "provenance": {"D1": D1_PATH, "D2": D2_PATH, "read_only": True, "new_forward_passes": 0,
                   "experiment_number_minted": None},
}
json.dump(out, open(os.path.join(REPO, "research/analysis_plans/S7-3_RESULTS_2026-10-05.json"), "w"), indent=1)
print("VERDICT: %s — %s" % (verdict, reason), flush=True)
print("results written: research/analysis_plans/S7-3_RESULTS_2026-10-05.json", flush=True)
