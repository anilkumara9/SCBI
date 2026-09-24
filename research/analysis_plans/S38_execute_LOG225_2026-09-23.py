#!/usr/bin/env python3
"""S3-8 downstream-amplification test -- LOG-225.

Question: is the EXP065/066 bridge rescue fully explained by the direct L1
readout shift of the (t-f) direction, or does it require downstream layers
(attention re-routing) beyond that shift?

Per-item decomposition on rescued items:
  dm_hat_i = alpha * b_hat_i . (W_U[t_i] - W_U[f_i])   (L1-predicted margin shift)
  dm_i     = archived end-to-end margin shift (Same_Layer_Output_Bridge_margin_shift)
  residual_i = dm_i - dm_hat_i

Pre-registered reading (CANDIDATE_BACKLOG.md S3-8):
  residuals ~= 0 on rescued items -> downstream-amplification dead -> Not supported
     (K2's routing premise dissolves)
  large systematic residuals     -> downstream transformation real   -> Supported

Mechanistic note: the bridge is injected at layer-20 output (h + alpha*v via a
forward hook on gpt_neox.layers[20]); pythia-410m has 24 layers, so blocks
21/22/23 + final LayerNorm + unembedding sit downstream. Under the direct-
readout null the downstream map acts as identity on the injected direction and
dm_i == dm_hat_i up to compute noise.

Guards: $0 CPU. No forward passes (G5-style self-inspection below). Weights
read-only; Delta theta = 0 verified by reproducing the archived EXP066
pre_hash with the runner-verbatim params-order hash function before and after
reads (K1 G3 precedent). EXP065 has no per-item archive -> that run is
Underdetermined per the pre-registered contingency (never filled by assumption).
EXP077 has no per-item margin shifts -> out of scope.
"""

import hashlib
import json
import math
import os
import re
import sys

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# ---------------------------------------------------------------------------
# G5 self-inspection: no forward-pass invocation of the model on inputs.
# ---------------------------------------------------------------------------
_SRC = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
_BAD = []
for _ln, _line in enumerate(_SRC.splitlines(), 1):
    _code = _line.split("#", 1)[0]
    if re.search(r"(?<![\w\"'.])model\s*\(", _code):
        _BAD.append((_ln, _line.strip()))
assert not _BAD, f"G5 FATAL: model forward-pass call candidates found: {_BAD}"
print("[G5] self-inspection passed: no model forward-pass invocation present.", flush=True)

assert torch.__version__ == "2.14.0+cpu", f"torch version mismatch: {torch.__version__}"
assert np.__version__ == "2.5.3", f"numpy version mismatch: {np.__version__}"

SCBI = os.path.expanduser("~/workspace/SCBI")
SNAP_410M = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
ARCHIVED_EXP066_PRE_HASH = "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd"
ALPHA = 0.5  # [FACT] runner l.379: alpha_val = 0.50; archive top-level alpha 0.5

def get_hash_params_order(model):
    """Verbatim EXP066 runner get_hash (ll. 34-38): params() order, raw bytes."""
    sha = hashlib.sha256()
    for p in model.parameters():
        sha.update(p.detach().cpu().numpy().tobytes())
    return sha.hexdigest()

print("[LOAD] pythia-410m (read-only) ...", flush=True)
model = AutoModelForCausalLM.from_pretrained(
    "EleutherAI/pythia-410m", revision=SNAP_410M,
    local_files_only=True, trust_remote_code=False, torch_dtype=torch.float32)
model.eval()
tok = AutoTokenizer.from_pretrained(
    "EleutherAI/pythia-410m", revision=SNAP_410M,
    local_files_only=True, trust_remote_code=False)
assert model.config.num_hidden_layers == 24, "depth assumption violated"
print("[DEPTH] num_hidden_layers=24; injection at layer-20 output -> 3 blocks downstream (21,22,23).", flush=True)

pre = get_hash_params_order(model)
assert pre == ARCHIVED_EXP066_PRE_HASH, (
    f"G3 FATAL: weights differ from archived EXP066 run.\n  computed={pre}\n  archived={ARCHIVED_EXP066_PRE_HASH}")
print(f"[G3] params-order hash OK: {pre[:12]}... == archived EXP066 pre==post.", flush=True)

# ---------------------------------------------------------------------------
# Item construction: byte-verbatim port of EXP065/066 runners (K1 executor ll.106-345)
# ---------------------------------------------------------------------------
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

items = []
for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
    A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
    target_first = (i % 2 == 1)
    q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
    is_rev = (i >= 8)
    if not is_rev:
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
    else:
        p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
    items.append({"target_token": " " + A, "foil_token": " " + C, "prompt": p})
for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
    A, B, C, D = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                  NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
    target_first = (i % 2 == 1)
    q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
    is_rev = (i >= 8)
    if not is_rev:
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
    else:
        p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
    items.append({"target_token": " " + A, "foil_token": " " + D, "prompt": p})
for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
    A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
    target_first = (i % 2 == 0)
    q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
    is_rev = (i >= 7)
    if not is_rev:
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
    else:
        p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
    items.append({"target_token": " " + A, "foil_token": " " + C, "prompt": p})
for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
    A, B, C, D = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                  NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
    target_first = (i % 2 == 0)
    q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
    is_rev = (i >= 7)
    if not is_rev:
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
    else:
        p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
    items.append({"target_token": " " + A, "foil_token": " " + D, "prompt": p})
assert len(items) == 60

# ---- G2: prompt byte-identity vs archived per-item records ----
rec = json.load(open(os.path.join(
    SCBI, "experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json")))
assert len(rec) == 60
ordered = ([f"pythia410m_planet_2hop_{i}" for i in range(15)] +
           [f"pythia410m_planet_3hop_{i}" for i in range(15)] +
           [f"pythia410m_element_2hop_{i}" for i in range(15)] +
           [f"pythia410m_element_3hop_{i}" for i in range(15)])
for idx, key in enumerate(ordered):
    assert rec[key]["prompt"] == items[idx]["prompt"], f"G2 FATAL: prompt mismatch at {key}"
print("[G2] 60/60 prompts byte-consistent with archived EXP066 per-item records.", flush=True)

ids = [(tok.encode(it["target_token"])[0], tok.encode(it["foil_token"])[0]) for it in items]
for i, (t, f) in enumerate(ids):
    assert t != f, f"item {i}: target==foil"

E = model.get_output_embeddings().weight.detach().cpu()  # == model.embed_out.weight (runner)
assert E.shape[1] == 1024

# ---------------------------------------------------------------------------
# Per-item decomposition
# dm_hat_i = alpha * b_hat_i . (E[t_i] - E[f_i]) = alpha * ||E[t_i]-E[f_i]||
#   (b_hat_i = normalize(E[t_i]-E[f_i]) is the runner's verbatim make_bridge_vec,
#    K1 G1 verified |cos| >= 1-1e-6)
# dm_i = archived Same_Layer_Output_Bridge_margin_shift
#      = (t_l_m - f_l_m) - (t_l_b - f_l_b)  (runner l.449, verbatim)
# ---------------------------------------------------------------------------
rows = []
for idx, key in enumerate(ordered):
    t_id, f_id = ids[idx]
    diff = E[t_id, :] - E[f_id, :]
    nd = float(torch.norm(diff).item())
    assert nd > 0
    b_hat = diff / nd
    dm_hat = ALPHA * float((b_hat @ diff).item())  # == ALPHA * nd
    dm_arch = float(rec[key]["Same_Layer_Output_Bridge_margin_shift"])
    base_c = bool(rec[key]["base_correct"])
    mod_c = bool(rec[key]["Same_Layer_Output_Bridge_correct"])
    rows.append({"key": key, "t_id": t_id, "f_id": f_id, "norm_diff": nd,
                 "dm_hat": dm_hat, "dm_archived": dm_arch,
                 "residual": dm_arch - dm_hat,
                 "base_correct": base_c, "mod_correct": mod_c,
                 "rescued": (not base_c) and mod_c,
                 "corrupted": base_c and (not mod_c)})

# Post-read hash (Delta theta = 0)
post = get_hash_params_order(model)
assert post == pre, "G3 FATAL: weights changed during read-only analysis"
print("[G3] post-hash matches pre-hash: Delta theta = 0 confirmed.", flush=True)

b = sum(r["rescued"] for r in rows)
c = sum(r["corrupted"] for r in rows)
print(f"[B] rescued b={b}, corrupted c={c} (archived: 8, 0).", flush=True)
assert (b, c) == (8, 0), "rescue-set identity mismatch vs archived (b,c)=(8,0)"

arch = json.load(open(os.path.join(
    SCBI, "experiments/runs/EXP066_pythia410m_replication/exp066_replication_results.json")))
sb = arch["stage_B_conditions"]["Same_Layer_Output_Bridge"]
mean_dm_hat = float(np.mean([r["dm_hat"] for r in rows]))
mean_dm_arch = float(np.mean([r["dm_archived"] for r in rows]))
print(f"[SANITY] mean(dm_hat)={mean_dm_hat:.6f} vs archived delta_margin={sb['delta_margin']:.6f} "
      f"(diff={mean_dm_hat - sb['delta_margin']:+.2e})", flush=True)
print(f"[SANITY] archived dL_t - dL_f = {sb['delta_logit_target'] - sb['delta_logit_foil']:.6f} "
      f"(== delta_margin by margin identity)", flush=True)

# ---------------------------------------------------------------------------
# Residual statistics
# ---------------------------------------------------------------------------
EPS = 1e-4  # [ASSUMPTION] measurement-noise floor: ~100x float32 ulp on O(10)
            # logit quantities; disclosed, does not drive the verdict.

def stats(rs, name):
    r = np.array([x["residual"] for x in rs])
    dmh = np.array([x["dm_hat"] for x in rs])
    n = len(r)
    out = {
        "n": n,
        "mean_residual": float(np.mean(r)),
        "std_residual": float(np.std(r)),
        "min_residual": float(np.min(r)),
        "max_residual": float(np.max(r)),
        "mean_abs_residual": float(np.mean(np.abs(r))),
        "max_abs_residual": float(np.max(np.abs(r))),
        "mean_abs_dm_hat": float(np.mean(np.abs(dmh))),
        "rel_mean_abs": float(np.mean(np.abs(r)) / np.mean(np.abs(dmh))),
        "frac_within_eps": float(np.mean(np.abs(r) <= EPS)),
        "frac_within_10pct": float(np.mean(np.abs(r) <= 0.10 * np.abs(dmh))),
        "pos_frac": float(np.mean(r > 0)),
    }
    print(f"[{name}] n={n} mean_res={out['mean_residual']:+.6f} std={out['std_residual']:.6f} "
          f"min={out['min_residual']:+.6f} max={out['max_residual']:+.6f} "
          f"mean|res|={out['mean_abs_residual']:.6f} mean|dm_hat|={out['mean_abs_dm_hat']:.6f} "
          f"rel={out['rel_mean_abs']:.4f} frac|res|<=1e-4={out['frac_within_eps']:.3f} "
          f"frac|res|<=10%|dm_hat|={out['frac_within_10pct']:.3f} pos_frac={out['pos_frac']:.3f}", flush=True)
    return out

rescued = [r for r in rows if r["rescued"]]
others = [r for r in rows if not r["rescued"]]
st_all = stats(rows, "ALL")
st_res = stats(rescued, "RESCUED")
st_oth = stats(others, "OTHER")

# Per-item rescued table
print("--- rescued items (per-item) ---", flush=True)
for r in rescued:
    print(f"  {r['key']}: dm_hat={r['dm_hat']:+.6f} dm_arch={r['dm_archived']:+.6f} "
          f"res={r['residual']:+.6f} |res|/|dm_hat|={abs(r['residual'])/abs(r['dm_hat']):.4f}", flush=True)

# Correlation checks: does the residual carry signal about rescue status?
res_all = np.array([r["residual"] for r in rows])
lab_all = np.array([1.0 if r["rescued"] else 0.0 for r in rows])
dmh_all = np.array([r["dm_hat"] for r in rows])
def pearson(x, y):
    x = x - x.mean(); y = y - y.mean()
    return float((x @ y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-300))
corr_res_rescue = pearson(res_all, lab_all)
corr_res_dmhat = pearson(res_all, dmh_all)
print(f"[CORR] corr(residual, rescued)={corr_res_rescue:+.4f}; corr(residual, dm_hat)={corr_res_dmhat:+.4f}", flush=True)

twin = {
    "log": "LOG-225",
    "run": "EXP066_pythia410m_replication",
    "n_items": 60, "n_rescued": b, "n_corrupted": c,
    "alpha": ALPHA, "target_layer": 20, "downstream_blocks": [21, 22, 23],
    "delta_theta_0": {"pre_hash_params_order": pre, "post_hash": post, "match": True},
    "guards": {"G2_prompt_identity": "60/60 byte-consistent",
               "G3_delta_theta": "PASS", "G5_no_forward_pass": "PASS (self-inspection)"},
    "epsilon_noise_floor_assumption": EPS,
    "sanity": {"mean_dm_hat": mean_dm_hat,
               "archived_delta_margin": sb["delta_margin"],
               "archived_dL_t": sb["delta_logit_target"],
               "archived_dL_f": sb["delta_logit_foil"]},
    "stats_all": st_all, "stats_rescued": st_res, "stats_other": st_oth,
    "corr_residual_rescued": corr_res_rescue,
    "corr_residual_dmhat": corr_res_dmhat,
    "rescued_items": [{"key": r["key"], "t_id": r["t_id"], "f_id": r["f_id"],
                       "dm_hat": r["dm_hat"], "dm_archived": r["dm_archived"],
                       "residual": r["residual"]} for r in rescued],
    "exp065": "Underdetermined: no per-item logit/margin archive exists (aggregates only)",
    "exp077": "not decomposable: exp077_instance_records.json carries correctness only, "
              "no per-item logit/margin shifts",
}
out = os.path.join(SCBI, "research/analysis_plans/S38_DOWNSTREAM_RESULTS_LOG225_2026-09-23.json")
json.dump(twin, open(out, "w"), indent=2)
print(f"[OUT] wrote {out}", flush=True)
print("=" * 78)
print("S3-8 DECOMPOSITION COMPLETE")
print("=" * 78)
