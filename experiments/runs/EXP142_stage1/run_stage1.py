#!/usr/bin/env python3
"""EXP142 Stage-1: S4-7 spectral phase transition (RMT lens) CPU observational pilot.
Executes EXACTLY per research/prereg/EXP_S47_prereg_DRAFT_2026-10-03.md (SIGNED, LOG-4891).
CEO venue approval: Stage-1 CPU pilot only (60 passes + hidden states). $0 compute.
OBSERVATIONAL ONLY: no intervention, no selection, no steering.
Exit codes: 0 = clean completion; 44 = RUN-INVALID (validity gate trip).

Pre-reg interpretation notes (documented, not improvised):
- Baseline correctness from committed EXP140 B0 records (branch 0 'correct' bool),
  id-aligned 60/60, no regeneration — the pre-reg's pinned baseline-source decision.
  Labels define the correct/failed groups in the primary permutation test only
  (Law #7); the sigma-hat estimator, MP edge, s_{i,l} counts, and s_i are all
  computed label-blind. The permutation seed is fixed, not chosen at runtime.
- MP median equation implemented verbatim from pre-reg §2: m solves F(m) =
  1 - 1/(2*gamma), where F is the full MP CDF (atom at 0 of mass 1-1/gamma plus
  the continuous part), gamma_i = 1024/n_i. Computed by numerical integration
  of the closed-form MP density with sigma^2=1 on [lambda_-, lambda_+].
- Max-inside-permutation: s_i = max_l s_{i,l} is a pre-registered per-item
  statistic computed once; the permutation shuffles ONLY the correct/failed
  labels, so the max is applied identically in every permutation.
- n_i = number of input token positions (no padding; single-item batches).
"""
import hashlib, json, math, os, sys, time
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(RUN_DIR, exist_ok=True)
LOGF = open(os.path.join(RUN_DIR, "stage1_run_log.txt"), "w")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOGF.write(line + "\n"); LOGF.flush()

# ============ pre-reg pinned constants ============
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df"
HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
MODEL_ID = "EleutherAI/pythia-410m"
S_PERM = 20261010
N_PERM = 100000
N_ITEMS = 60
N_LAYERS = 24
D_MODEL = 1024
N_MIN = 40          # C2 guard: items with n_i < 40 excluded
N_KEEP_MIN = 30     # C2 guard: <30 remaining -> HELD with reason
P_BAR = 0.05
DELTA_S_BAR = 2
KS_FLAG = 0.15      # bulk-fit diagnostic flag (reported, not binding)

torch.manual_seed(20261010)
torch.set_num_threads(max(1, (os.cpu_count() or 4) - 1))
log("threads=%d" % torch.get_num_threads())

FWD_COUNT = [0]
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
               "forwards": FWD_COUNT[0]},
              open(os.path.join(RUN_DIR, "stage1_verdict.json"), "w"), indent=1)
    LOGF.close()
    sys.exit(44)

# ============ model load + backbone pin ============
log("loading tokenizer + model (float32, cpu, local_files_only)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=HF_REVISION,
                                          local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, revision=HF_REVISION, local_files_only=True,
    torch_dtype=torch.float32, device_map="cpu")
model.eval()
log("model loaded")

pre_hash = sha256_state_dict(model)
log("backbone pre-hash: %s" % pre_hash)
if pre_hash != BACKBONE_PIN:
    run_invalid("(b) backbone pre-hash mismatch: got %s" % pre_hash)
log("(b) backbone pin PASS")

# ============ bench reconstruction (inlined from run_exp135.py) ============
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

bench = build_bench()
assert len(bench) == 60, "bench len %d != 60" % len(bench)
bench_hash = hashlib.sha256(json.dumps(
    [{k: bench[i][k] for k in ("id", "prompt", "A", "C")} for i in range(len(bench))],
    sort_keys=True).encode()).hexdigest()
log("(a) bench len=60; bench sha256=%s" % bench_hash)
if bench_hash != BENCH_PIN:
    run_invalid("(a) bench sha256 mismatch: got %s" % bench_hash)
log("(a) bench pin PASS")

# view 0 for all 60 items (pre-reg §2)
items_v0 = [make_views(it, novel_src(it))[0] for it in bench]

# ============ baseline correctness from committed EXP140 B0 records ============
EXP140_REC = "/home/hatch/workspace/SCBI/experiments/runs/EXP140_stage1/stage1_records.json"
with open(EXP140_REC) as f:
    exp140 = json.load(f)
assert exp140["pins"]["backbone_pre"] == BACKBONE_PIN, "EXP140 backbone pin drift"
assert exp140["pins"]["bench"] == BENCH_PIN, "EXP140 bench pin drift"
e140_items = exp140["items"]
assert len(e140_items) == 60, "EXP140 items %d != 60" % len(e140_items)
for i, (b, e) in enumerate(zip(bench, e140_items)):
    assert b["id"] == e["id"], "id mismatch at %d: %s vs %s" % (i, b["id"], e["id"])
log("(c) EXP140 record id alignment 60/60 PASS")

# correctness labels: branch-0 'correct' bool. Law #7: labels define the groups
# in the primary permutation test only (pre-reg §5).
b0_correct = []
for i in range(N_ITEMS):
    br0 = e140_items[i]["branches"][0]
    assert br0["k"] == 0
    b0_correct.append(1 if bool(br0["correct"]) else 0)
log("B0 baseline accuracy: %.4f" % (sum(b0_correct) / N_ITEMS))

# ============ Marchenko-Pastur construction (pre-reg §2, verbatim) ============
# MP density (sigma^2=1): f(x) = sqrt((l+ - x)(x - l-)) / (2*pi*gamma*x),
# on [l-, l+], l+ = (1+sqrt(g))^2, l- = (1-sqrt(g))^2.
# Full MP CDF (gamma > 1): F(x) = (1 - 1/g) + integral_{l-}^{x} f(t) dt for x>=0
# (atom at 0 of mass 1 - 1/g; continuous part has total mass 1/g).
# Theoretical median of the NONZERO spectrum: m solves F(m) = 1 - 1/(2g).

_MP_CACHE = {}

def _mp_unit_grid(gamma, npts=200000):
    """CDF grid for the full MP law with sigma^2=1, cached per gamma."""
    key = round(gamma, 12)
    if key in _MP_CACHE:
        return _MP_CACHE[key]
    sq = math.sqrt(gamma)
    lp = (1.0 + sq) ** 2
    lm = (1.0 - sq) ** 2
    xs = np.linspace(lm, lp, npts)
    # density; guard endpoints (sqrt of ~0)
    inner = np.clip((lp - xs) * (xs - lm), 0.0, None)
    f = np.sqrt(inner) / (2.0 * math.pi * gamma * xs)
    dx = xs[1] - xs[0]
    cum = np.cumsum(f) * dx          # integral_{lm}^{x} f
    atom = 1.0 - 1.0 / gamma
    F = atom + cum                    # full CDF
    _MP_CACHE[key] = (xs, F, lp, lm)
    return _MP_CACHE[key]

def mp_median(gamma):
    """Theoretical median m of the nonzero MP spectrum: F(m) = 1 - 1/(2g)."""
    xs, F, lp, lm = _mp_unit_grid(gamma)
    target = 1.0 - 1.0 / (2.0 * gamma)
    idx = int(np.searchsorted(F, target))
    idx = min(max(idx, 1), len(xs) - 1)
    # linear interpolation between grid points
    x0, x1 = xs[idx - 1], xs[idx]
    f0, f1 = F[idx - 1], F[idx]
    if f1 == f0:
        return x1
    return x0 + (target - f0) * (x1 - x0) / (f1 - f0)

def mp_cdf_fit(x, gamma, sigma2):
    """Fitted full MP CDF at x (scalar or array), with noise variance sigma2."""
    xs, F, lp, lm = _mp_unit_grid(gamma)
    x = np.asarray(x, dtype=float)
    # scale: F(x; s2) = F_unit(x / s2)
    xscl = x / sigma2
    out = np.where(xscl < lm, 1.0 - 1.0 / gamma,
           np.where(xscl >= lp, 1.0, np.interp(xscl, xs, F)))
    return out

def spectral_counts(eigvals, n_i, d_model=1024):
    """Per pre-reg §2: sigma2-hat via bulk-median fit; s = #{lambda > edge}.
    Returns (s_count, sigma2_hat, edge, ks)."""
    gamma = d_model / n_i
    med = float(np.median(eigvals))
    m_mp = mp_median(gamma)
    sigma2 = med / m_mp
    edge = sigma2 * (1.0 + math.sqrt(gamma)) ** 2
    s = int(np.sum(eigvals > edge))
    # bulk-fit diagnostic: KS between the empirical CDF of the NONZERO eigenvalues
    # and the fitted MP CDF over the bulk (continuous part renormalized:
    # F_bulk(x) = gamma * (F_full(x) - (1 - 1/gamma)) on [l-, l+]).
    ev = np.sort(eigvals)
    n = len(ev)
    F_emp = np.arange(1, n + 1) / n
    F_full = mp_cdf_fit(ev, gamma, sigma2)
    F_bulk = gamma * np.clip(F_full - (1.0 - 1.0 / gamma), 0.0, 1.0 / gamma)
    ks = float(np.max(np.abs(F_emp - F_bulk)))
    return s, sigma2, edge, ks

# ============ forward passes with hidden-state capture ============
def forward_hidden(prompt_text):
    input_ids = tokenizer.encode(prompt_text, return_tensors="pt")
    n_i = input_ids.shape[1]
    with torch.no_grad():
        out = model(input_ids=input_ids, output_hidden_states=True)
    count_fwd(1)
    # hidden_states[0] = embeddings; [1..24] = 24 block outputs
    hs = out.hidden_states
    assert len(hs) == N_LAYERS + 1, "hidden states %d != 25" % len(hs)
    return n_i, [hs[l + 1][0].detach().cpu() for l in range(N_LAYERS)]

# per-item spectral computation; returns dict with all pre-reg quantities
def item_spectrum(n_i, layer_tensors):
    s_il = []
    sig2_il = []
    ks_il = []
    eig_store = []  # for determinism spot-check
    for H in layer_tensors:
        # center per dimension; Gram; eigendecompose
        X = H - H.mean(dim=0, keepdim=True)
        G = (X @ X.T) / n_i
        ev = torch.linalg.eigvalsh(G).numpy().astype(np.float64)
        ev = np.sort(ev)[::-1]  # descending, matching lambda_1 >= ...
        s, sig2, edge, ks = spectral_counts(np.sort(ev), n_i)  # ascending for median
        s_il.append(s); sig2_il.append(sig2); ks_il.append(ks)
        eig_store.append(ev.copy())
        del H, X, G, ev
    s_i = int(max(s_il))
    return {"n_i": n_i, "s_il": s_il, "s_i": s_i,
            "sigma2_il": sig2_il, "ks_il": ks_il, "eig": eig_store}

t0 = time.time()
items = []
n_i_list = []
failed = 0
for i in range(N_ITEMS):
    n_i, hts = forward_hidden(items_v0[i]["prompt"])
    try:
        rec = item_spectrum(n_i, hts)
    except Exception as ex:
        log("spectral computation failed on item %d: %s" % (i, ex))
        failed += 1
        continue
    rec["id"] = bench[i]["id"]
    rec["correct"] = b0_correct[i]
    items.append(rec)
    n_i_list.append(n_i)
    del hts
    if (i + 1) % 10 == 0:
        log("passes %d/60 (%.1fs)" % (i + 1, time.time() - t0))
if failed:
    run_invalid("(d) %d spectral computations failed" % failed)
if FWD_COUNT[0] != 60:
    run_invalid("(d) forward count %d != 60" % FWD_COUNT[0])
log("(d) 60/60 passes complete PASS (%.1fs)" % (time.time() - t0))

# ============ validity gate (e): determinism spot-check ============
for i in (0, 29, 59):
    n2, hts2 = forward_hidden(items_v0[i]["prompt"])
    rec2 = item_spectrum(n2, hts2)
    assert n2 == items[i]["n_i"], "n_i changed on re-run"
    for l in range(N_LAYERS):
        if not np.array_equal(rec2["eig"][l], items[i]["eig"][l]):
            run_invalid("(e) determinism: item %d layer %d eigenvalues differ" % (i, l))
    del hts2
log("(e) determinism spot-check 3/3 byte-identical PASS")
# the 3 re-run forwards don't count toward the 60-pass budget; note them
log("note: 3 determinism re-run forwards excluded from the 60-pass count")

# ============ backbone post-hash (Delta theta = 0) ============
post_hash = sha256_state_dict(model)
log("backbone post-hash: %s" % post_hash)
if post_hash != BACKBONE_PIN:
    run_invalid("(c) backbone post-hash mismatch (Delta theta != 0)")
log("(c) Delta theta = 0 PASS")

# ============ C2 measurement-validity guard ============
n_i_arr = np.array(n_i_list)
ni_med = float(np.median(n_i_arr))
ni_q1, ni_q3 = float(np.percentile(n_i_arr, 25)), float(np.percentile(n_i_arr, 75))
ni_min, ni_max = int(n_i_arr.min()), int(n_i_arr.max())
below_floor = int(np.sum(n_i_arr < N_MIN))
log("n_i distribution: median=%.1f IQR=[%.1f,%.1f] range=[%d,%d] below-floor(%d)=%d"
    % (ni_med, ni_q1, ni_q3, ni_min, ni_max, N_MIN, below_floor))

kept = [r for r in items if r["n_i"] >= N_MIN]
n_kept = len(kept)
log("items kept after C2 guard: %d/60" % n_kept)
guard_fired = n_kept < N_KEEP_MIN

# ============ primary inference ============
s_vals = np.array([r["s_i"] for r in kept])
y_vals = np.array([r["correct"] for r in kept])
s_c = s_vals[y_vals == 1]
s_f = s_vals[y_vals == 0]
delta_s_obs = float(np.median(s_c) - np.median(s_f))
log("s_correct: n=%d median=%.1f | s_failed: n=%d median=%.1f | Delta_s_obs=%.2f"
    % (len(s_c), float(np.median(s_c)), len(s_f), float(np.median(s_f)), delta_s_obs))

rng = np.random.default_rng(S_PERM)
ge = 0
for p in range(N_PERM):
    yp = rng.permutation(y_vals)
    d = float(np.median(s_vals[yp == 1]) - np.median(s_vals[yp == 0]))
    if d >= delta_s_obs:
        ge += 1
p_val = ge / N_PERM
log("permutation test: %d perms, seed=%d, p=%.5f" % (N_PERM, S_PERM, p_val))

# bulk-fit diagnostic (median KS across all item-layer pairs)
all_ks = [k for r in items for k in r["ks_il"]]
ks_med = float(np.median(all_ks))
ks_flag = ks_med > KS_FLAG
log("bulk-fit diagnostic: median KS=%.4f (flag threshold %.2f) -> %s"
    % (ks_med, KS_FLAG, "POOR-FIT FLAGGED" if ks_flag else "ok"))

# ============ secondary diagnostics (reported, not binding) ============
# (a) l_c transition rule: >=3 new outliers sustained 2 layers
def find_lc(s_il):
    for l in range(1, N_LAYERS - 1):
        if (s_il[l] - s_il[l - 1] >= 3) and (s_il[l + 1] - s_il[l - 1] >= 3):
            return l + 1  # 1-indexed layer
    return None
lc_vals = [find_lc(r["s_il"]) for r in kept]
lc_present = [v is not None for v in lc_vals]
log("l_c: present on %d/%d items" % (sum(lc_present), len(lc_vals)))
# (b) per-layer version of the primary test
per_layer_p = []
for l in range(N_LAYERS):
    sl = np.array([r["s_il"][l] for r in kept])
    d_obs = float(np.median(sl[y_vals == 1]) - np.median(sl[y_vals == 0]))
    g2 = 0
    for p in range(20000):
        yp = rng.permutation(y_vals)
        if float(np.median(sl[yp == 1]) - np.median(sl[yp == 0])) >= d_obs:
            g2 += 1
    per_layer_p.append(g2 / 20000)
sig_layers = [l + 1 for l, pv in enumerate(per_layer_p) if pv < 0.05]
log("per-layer test (20k perms): significant layers (p<0.05): %s" % sig_layers)
# (c) mean-difference version
d_mean = float(np.mean(s_c) - np.mean(s_f))
gm = 0
for p in range(N_PERM):
    yp = rng.permutation(y_vals)
    if float(np.mean(s_vals[yp == 1]) - np.mean(s_vals[yp == 0])) >= d_mean:
        gm += 1
p_mean = gm / N_PERM
log("mean-difference version: Delta_mean=%.2f p=%.5f" % (d_mean, p_mean))

# ============ falsification tree (binding) ============
if guard_fired:
    verdict, reason = "HELD", "C2 guard fired: %d items with n_i>=%d (<30) - insufficient positions for stable spectra" % (n_kept, N_MIN)
elif p_val >= P_BAR:
    verdict, reason = "KILL", "p=%.5f >= 0.05 - the RMT lens sees nothing; intervention never attempted" % p_val
elif delta_s_obs >= DELTA_S_BAR:
    verdict, reason = "CONTINUE", "p=%.5f < 0.05 and Delta_s=%.2f >= 2 - licenses a NEW worth-it gate for spectral intervention only" % (p_val, delta_s_obs)
else:
    verdict, reason = "HELD", "p=%.5f < 0.05 but Delta_s=%.2f < 2 - significant but below magnitude bar" % (p_val, delta_s_obs)
log("VERDICT: %s - %s" % (verdict, reason))

# ============ records ============
records = {
    "experiment": "EXP142",
    "prereg": "research/prereg/EXP_S47_prereg_DRAFT_2026-10-03.md (SIGNED, LOG-4891)",
    "pins": {"backbone_pre": pre_hash, "backbone_post": post_hash,
             "bench": bench_hash, "hf_revision": HF_REVISION,
             "model": MODEL_ID, "dtype": "float32"},
    "seeds": {"S_PERM": S_PERM},
    "counts": {"forwards_budget": 60, "forwards_run": 60,
               "determinism_reruns": 3, "eigendecompositions": 60 * N_LAYERS},
    "guards": {"N_MIN": N_MIN, "n_i": {"median": ni_med, "iqr": [ni_q1, ni_q3],
               "range": [ni_min, ni_max], "below_floor": below_floor},
               "kept": n_kept, "guard_fired": guard_fired},
    "bulk_fit": {"median_ks": ks_med, "flag_threshold": KS_FLAG, "flagged": ks_flag},
    "primary": {"delta_s_obs": delta_s_obs, "p_value": p_val,
                "n_perm": N_PERM, "n_correct": int((y_vals == 1).sum()),
                "n_failed": int((y_vals == 0).sum()),
                "s_correct_median": float(np.median(s_c)),
                "s_failed_median": float(np.median(s_f))},
    "secondary": {"l_c_present": int(sum(lc_present)), "l_c_n": len(lc_vals),
                  "per_layer_p": per_layer_p,
                  "significant_layers": sig_layers,
                  "delta_mean": d_mean, "p_mean": p_mean},
    "verdict": verdict,
    "verdict_reason": reason,
    "items": [{"id": r["id"], "n_i": r["n_i"], "correct": r["correct"],
               "s_i": r["s_i"], "s_il": r["s_il"],
               "sigma2_med": float(np.median(r["sigma2_il"])),
               "ks_med": float(np.median(r["ks_il"]))} for r in items],
}
json.dump(records, open(os.path.join(RUN_DIR, "stage1_records.json"), "w"), indent=1)
json.dump({"verdict": verdict, "reason": reason, "delta_s": delta_s_obs,
           "p_value": p_val, "forwards": FWD_COUNT[0]},
          open(os.path.join(RUN_DIR, "stage1_verdict.json"), "w"), indent=1)
log("records written")

# ============ RUN_REPORT.md ============
with open(os.path.join(RUN_DIR, "RUN_REPORT.md"), "w") as f:
    f.write("# EXP142 Stage-1 RUN REPORT — S4-7 spectral phase transition (RMT lens)\n\n")
    f.write("**Protocol:** `research/prereg/EXP_S47_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4891).\n\n")
    f.write("## Validity gates\n\n")
    f.write("- bench sha256 `%s` — PASS\n" % bench_hash)
    f.write("- backbone pre/post hash `%s` — PASS (Delta theta = 0)\n" % pre_hash)
    f.write("- 60/60 passes complete — PASS (+3 determinism re-runs)\n")
    f.write("- determinism spot-check 3/3 byte-identical — PASS\n\n")
    f.write("## C2 guard\n\n")
    f.write("- n_i: median %.1f, IQR [%.1f, %.1f], range [%d, %d], below-floor(%d): %d\n"
            % (ni_med, ni_q1, ni_q3, ni_min, ni_max, N_MIN, below_floor))
    f.write("- items kept: %d/60; guard fired: %s\n\n" % (n_kept, guard_fired))
    f.write("## Primary test\n\n")
    f.write("- s_correct (n=%d): median %.1f; s_failed (n=%d): median %.1f\n"
            % (int((y_vals == 1).sum()), float(np.median(s_c)),
               int((y_vals == 0).sum()), float(np.median(s_f))))
    f.write("- Delta_s_obs = %.2f; one-sided permutation p = %.5f (100,000 perms, seed %d)\n"
            % (delta_s_obs, p_val, S_PERM))
    f.write("- bulk-fit diagnostic: median KS = %.4f (flag %.2f) — %s\n\n"
            % (ks_med, KS_FLAG, "FLAGGED" if ks_flag else "ok"))
    f.write("## Secondary diagnostics (not binding)\n\n")
    f.write("- l_c present on %d/%d items\n" % (sum(lc_present), len(lc_vals)))
    f.write("- per-layer significant layers (p<0.05, 20k perms): %s\n" % sig_layers)
    f.write("- mean-difference version: Delta_mean=%.2f, p=%.5f\n\n" % (d_mean, p_mean))
    f.write("## Verdict\n\n**%s** — %s\n" % (verdict, reason))
log("RUN_REPORT.md written")
LOGF.close()
print("DONE verdict=%s" % verdict, flush=True)
