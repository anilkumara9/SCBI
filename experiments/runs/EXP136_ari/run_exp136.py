#!/usr/bin/env python3
"""EXP136 (B4/ARI) execution: Attention-Routing Intervention.
Executes EXACTLY per research/prereg/EXP136_PREREG_ARI_2026-09-30.md
(repaired: F1 direction-appropriate McNemar, F2 Phase-2 T1 delivery;
 advisories A1 output-propagation, A2 C-flat resolution applied;
 fix-verification LOG-4851 PASS, no amendments).
$0 CPU. No verdict interpretation — raw results only.
Exit codes: 0 = clean completion; 44 = RUN-INVALID (breaking point trip).
"""
import csv
import hashlib
import json
import math
import os
import re
import sys
import time

import numpy as np
import torch

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(RUN_DIR, "out")
os.makedirs(OUT, exist_ok=True)
LOGF = open(os.path.join(OUT, "exp136_run_log.txt"), "w")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOGF.write(line + "\n"); LOGF.flush()

# ============ §3.1 pinned constants ============
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
MODEL_ID = "EleutherAI/pythia-410m"
LAYER = 20
N_BENCH = 60
D_MAX_EXCL = 6
SEED_TORCH = 136013
BETA_T1 = 3.0
N_H = 2  # probe forwards: one T2 + one T1

torch.manual_seed(SEED_TORCH)
torch.set_num_threads(2)
log("torch %s | transformers pinned 5.17.0 | threads=%d | seed=%d"
    % (torch.__version__, torch.get_num_threads(), SEED_TORCH))
log("numpy %s" % np.__version__)

FWD_COUNT = [0]
def count_fwd(n=1):
    FWD_COUNT[0] += n

class RunInvalid(Exception):
    pass

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
    rec = {"verdict": "RUN-INVALID", "reason": reason,
           "forwards": FWD_COUNT[0], "exit_code": 44}
    json.dump(rec, open(os.path.join(OUT, "exp136_verdict.json"), "w"), indent=1)
    LOGF.close()
    sys.exit(44)

# ============ model ============
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers.models.gpt_neox.modeling_gpt_neox as m_gn

log("loading model %s rev %s (eager)" % (MODEL_ID, HF_REVISION))
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=HF_REVISION,
                                          local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, revision=HF_REVISION, local_files_only=True,
    torch_dtype=torch.float32, device_map="cpu", attn_implementation="eager")
model.eval()
pre_hash = sha256_state_dict(model)
log("backbone pre-hash: %s" % pre_hash)
if pre_hash != BACKBONE_PIN:
    run_invalid("(a) Δθ=0 pre-hash mismatch: got %s expected %s"
                % (pre_hash, BACKBONE_PIN))
log("(a) Δθ=0 pre-hash PASS")
L20_ATTN = model.gpt_neox.layers[LAYER].attention
log("L20 attention module: %s" % type(L20_ATTN).__name__)

# ============ bench (EXP092-B, licensed) ============
REPO_ROOT = os.path.abspath(os.path.join(RUN_DIR, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))
from reference_implementation import build_bench, bench_sha256  # noqa: E402

BENCH_PIN = "9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4"
bench = build_bench()
if len(bench) != N_BENCH:
    run_invalid("(c) bench len %d != 60" % len(bench))
bh = bench_sha256(bench)
log("(c) bench sha256=%s" % bh)
if bh != BENCH_PIN:
    run_invalid("(c) bench pin mismatch: got %s expected %s" % (bh, BENCH_PIN))
log("(c) bench pin PASS")

# ============ entity-span derivation (EXP101/EXP102 licensed pattern) ============
def _word_pattern(name):
    return re.compile(r"\b" + re.escape(name) + r"\b")

def entity_span_token_idx(prompt, a_name, c_name):
    spans = []
    for name in (a_name, c_name):
        for m in _word_pattern(name).finditer(prompt):
            spans.append(m.span())
    enc = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    offs = [(int(s), int(e)) for s, e in enc["offset_mapping"]]
    span_idx = sorted({t for (s0, s1) in spans
                       for t, (c0, c1) in enumerate(offs)
                       if c0 <= s0 and c1 >= s1})
    return span_idx, offs

def tok1(s):
    ids = tokenizer.encode(" " + s, add_special_tokens=False)
    assert len(ids) == 1, "multi-token entity: %s -> %s" % (s, ids)
    return ids[0]

excluded = []
included = []
for it in bench:
    try:
        sidx, offs = entity_span_token_idx(it["prompt"], it["A"], it["C"])
        N_i = len(offs)
        E_i = len(sidx)
        ok = (E_i >= 1 and E_i < N_i and (E_i / N_i) <= 0.5
              and (not sidx or max(sidx) < N_i - 1))
        # single-token coverage check (mirrors G1')
        for t in sidx:
            c0, c1 = offs[t]
            assert any(c0 <= s0 and c1 >= s1 for (s0, s1) in
                       [m.span() for name in (it["A"], it["C"])
                        for m in _word_pattern(name).finditer(it["prompt"])])
        if not ok or not sidx:
            raise ValueError("span operating-condition violation: E=%d N=%d" % (E_i, N_i))
        it["_span"] = sidx
        it["_E"] = E_i
        it["_N"] = N_i
        it["_tA"] = tok1(it["A"])
        it["_tC"] = tok1(it["C"])
        included.append(it)
    except Exception as ex:
        excluded.append((it["id"], str(ex)))
        log("excluded %s: %s" % (it["id"], ex))

e = len(excluded)
log("span derivation: excluded=%d" % e)
if e > D_MAX_EXCL:
    run_invalid("(c) exclusions %d > 6" % e)
n = N_BENCH - e
log("n = %d included items" % n)

# ============ archived EXP094 B vector (guard (b)) ============
archived = {}
arch_path = os.path.join(REPO_ROOT, "experiments", "runs", "EXP094_peritem_l11",
                         "out", "per_item_records.csv")
with open(arch_path, newline="") as f:
    for row in csv.DictReader(f):
        if row["arm"] == "B":
            archived[row["item_id"]] = (row["stratum"], int(row["correct_top1"]))
if len(archived) != N_BENCH:
    run_invalid("(b) archived B vector has %d items, expected 60" % len(archived))
arch_acc = sum(v[1] for v in archived.values())
log("(b) archived B vector loaded: 60 items, acc=%d/60" % arch_acc)

# ============ attention-weight patch (the intervention) ============
ORIG_EAGER = m_gn.eager_attention_forward
PATCH = {"active": False, "mode": None, "span": None, "q": None}

def apply_reweight(w, mode, span, q):
    """w: (1,H,Q,K) post-softmax. Returns w' with row q reweighted."""
    wp = w.clone()
    H = w.shape[1]
    T = w.shape[3]
    if mode == "T1":
        for h in range(H):
            row = wp[0, h, q, :].clone()
            for t in span:
                row[t] = BETA_T1 * row[t]
            s = row.sum()
            if not torch.isfinite(s) or float(s) <= 0:
                raise RunInvalid("(e) T1 renormalization degenerate")
            wp[0, h, q, :] = row / s
    elif mode == "T2":
        for h in range(H):
            row = wp[0, h, q, :].clone()
            for t in span:
                row[t] = 0.0
            s = row.sum()
            if not torch.isfinite(s) or float(s) <= 0:
                raise RunInvalid("(e) T2 renormalization degenerate")
            wp[0, h, q, :] = row / s
    elif mode == "C":
        for h in range(H):
            wp[0, h, q, :] = 1.0 / T
    else:
        raise RunInvalid("unknown patch mode %s" % mode)
    # guard (e): renormalization + finiteness on the hooked row
    prow = wp[0, :, q, :]
    if not torch.isfinite(prow).all():
        raise RunInvalid("(e) non-finite weights after reweight")
    if float((prow.sum(dim=-1) - 1.0).abs().max()) > 1e-5:
        raise RunInvalid("(e) renormalization violated: max |sum-1| = %g"
                         % float((prow.sum(dim=-1) - 1.0).abs().max()))
    return wp

def patched_eager(module, query, key, value, attention_mask,
                  scaling=None, dropout=0.0, **kwargs):
    attn_output, attn_weights = ORIG_EAGER(
        module, query, key, value, attention_mask,
        scaling=scaling, dropout=dropout, **kwargs)
    if PATCH["active"] and module is L20_ATTN:
        w_prime = apply_reweight(attn_weights, PATCH["mode"],
                                 PATCH["span"], PATCH["q"])
        out = torch.matmul(w_prime.to(value.dtype), value)
        out = out.transpose(1, 2).contiguous()
        return out, w_prime
    return attn_output, attn_weights

m_gn.eager_attention_forward = patched_eager
log("eager_attention_forward patched (module-global default path)")

# submodule-output capture hook (read-only) for the (h) A1 asserts
CAP = {}
def _cap_hook(module, inp, out):
    CAP["o"] = out[0].detach().cpu()  # post-dense attention-submodule output
cap_handle = L20_ATTN.register_forward_hook(_cap_hook)

def base_forward(input_ids, want_attn=False):
    with torch.no_grad():
        out = model(input_ids=input_ids, output_attentions=want_attn)
    count_fwd(1)
    return out

def decide(logits, tA, tC):
    lv = logits[0, -1, :]
    return "A" if float(lv[tA]) >= float(lv[tC]) else "C"

# ============ B pass (guard (b) + w_base/o_base for (h)) ============
log("B pass: %d items (eager, no hook)" % n)
PATCH["active"] = False
b_decisions = []
b_correct = []
w_base = None
o_base = None
q0 = None
for ii, it in enumerate(included):
    ids = tokenizer(it["prompt"], add_special_tokens=False,
                    return_tensors="pt")["input_ids"]
    T_i = ids.shape[1]
    q_i = T_i - 1
    want = (ii == 0)
    out = base_forward(ids, want_attn=want)
    yhat = decide(out.logits, it["_tA"], it["_tC"])
    b_decisions.append(yhat)
    b_correct.append(1 if yhat == "A" else 0)
    if want:
        w_base = out.attentions[LAYER][0, :, q_i, :].detach().cpu()  # (H,K)
        o_base = CAP["o"].clone()
        q0 = q_i
        log("captured w_base/o_base on item 0 (q=%d, T=%d)" % (q_i, T_i))

# guard (b): 60/60 agreement vs archived EXP094 B vector
dis = []
for it, yh, yc in zip(included, b_decisions, b_correct):
    arch_stratum, arch_correct = archived[it["id"]]
    if yc != arch_correct:
        dis.append(it["id"])
if dis:
    run_invalid("(b) B-decision agreement: %d disagreements vs archived "
                "(e.g. %s)" % (len(dis), dis[:3]))
log("(b) B-decision agreement 60/60 PASS (acc=%d/60)" % sum(b_correct))

# ============ (h) hook-delivery control: Phase 1 (T2) ============
log("(h) Phase 1: T2 span-ablate hook delivery")
it0 = included[0]
span0 = it0["_span"]
try:
    PATCH.update({"active": True, "mode": "T2", "span": span0, "q": q0})
    ids0 = tokenizer(it0["prompt"], add_special_tokens=False,
                     return_tensors="pt")["input_ids"]
    out = base_forward(ids0, want_attn=True)
    w = out.attentions[LAYER][0, :, q0, :].detach().cpu()  # (H,K)
    o = CAP["o"].clone()
    H = w.shape[0]
    # assert 2: span ablated in every head
    m1 = float(w[:, span0].sum(dim=-1).max())
    assert m1 < 1e-6, "P1 assert2: max_h span mass = %g" % m1
    # assert 3: renormalization
    m2 = float((w.sum(dim=-1) - 1.0).abs().max())
    assert m2 < 1e-5, "P1 assert3: max |sum-1| = %g" % m2
    # assert 4: finiteness
    assert torch.isfinite(w).all(), "P1 assert4: non-finite weights"
    # assert 5: hook active (L1 vs base)
    m3 = float((w - w_base).abs().sum(dim=-1).mean())
    assert m3 > 0.01, "P1 assert5: mean L1 = %g" % m3
    # assert 6 (A1): output propagation
    m4 = float((o - o_base).norm())
    assert m4 > 1e-6, "P1 assert6: ||o-o_base|| = %g" % m4
    log("(h) Phase 1 PASS: spanmass=%.2e renorm=%.2e L1=%.4f dOut=%.2e"
        % (m1, m2, m3, m4))
finally:
    PATCH["active"] = False

# ============ (h) hook-delivery control: Phase 2 (T1) ============
log("(h) Phase 2: T1 span-boost hook delivery")
try:
    PATCH.update({"active": True, "mode": "T1", "span": span0, "q": q0})
    out = base_forward(ids0, want_attn=True)
    w = out.attentions[LAYER][0, :, q0, :].detach().cpu()
    o = CAP["o"].clone()
    # assert 8: L1 activity
    m8 = float((w - w_base).abs().sum(dim=-1).mean())
    assert m8 > 0.01, "P2 assert8: mean L1 = %g" % m8
    # assert 9: boost direction (strict increase of span mass)
    mb_new = float(w[:, span0].sum(dim=-1).mean())
    mb_old = float(w_base[:, span0].sum(dim=-1).mean())
    assert mb_new > mb_old, "P2 assert9: %.6f not > %.6f" % (mb_new, mb_old)
    # assert 10: non-trivial mass floor
    assert mb_new > 1e-3, "P2 assert10: boosted span mass = %g" % mb_new
    # assert 11: renormalization
    m11 = float((w.sum(dim=-1) - 1.0).abs().max())
    assert m11 < 1e-5, "P2 assert11: max |sum-1| = %g" % m11
    # assert 12: finiteness
    assert torch.isfinite(w).all(), "P2 assert12: non-finite weights"
    # assert 13 (A1): output propagation
    m13 = float((o - o_base).norm())
    assert m13 > 1e-6, "P2 assert13: ||o-o_base|| = %g" % m13
    log("(h) Phase 2 PASS: L1=%.4f spanmass %.4f>%.4f floor-ok renorm=%.2e dOut=%.2e"
        % (m8, mb_new, mb_old, m11, m13))
finally:
    PATCH["active"] = False
log("(h) hook-delivery PASS on both hooks")

# ============ decision passes: T1, T2, C ============
def arm_pass(mode):
    log("%s pass: %d items" % (mode, n))
    PATCH.update({"active": True, "mode": mode, "span": None, "q": None})
    dec, cor = [], []
    try:
        for it in included:
            ids = tokenizer(it["prompt"], add_special_tokens=False,
                            return_tensors="pt")["input_ids"]
            q_i = ids.shape[1] - 1
            PATCH["span"] = it["_span"]
            PATCH["q"] = q_i
            out = base_forward(ids, want_attn=False)
            yhat = decide(out.logits, it["_tA"], it["_tC"])
            dec.append(yhat)
            cor.append(1 if yhat == "A" else 0)
    finally:
        PATCH["active"] = False
    return dec, cor

t1_dec, t1_cor = arm_pass("T1")
t2_dec, t2_cor = arm_pass("T2")
c_dec, c_cor = arm_pass("C")

# ============ endpoint: ΔM + McNemar (F1 direction-appropriate) ============
def mcnemar_p(b, c, alternative):
    n_ = b + c
    if n_ == 0:
        return 1.0
    if alternative == "greater":  # H1: b > c
        return sum(math.comb(n_, k) for k in range(b, n_ + 1)) / 2**n_
    if alternative == "less":  # H1: c > b
        return sum(math.comb(n_, k) for k in range(c, n_ + 1)) / 2**n_
    # two-sided
    p = 2 * sum(math.comb(n_, k) for k in range(max(b, c), n_ + 1)) / 2**n_
    return min(p, 1.0)

def arm_stats(name, cor_arm, dec_arm, alternative):
    b = sum(1 for ca, cb in zip(cor_arm, b_correct) if ca and not cb)
    c = sum(1 for ca, cb in zip(cor_arm, b_correct) if not ca and cb)
    flips = sum(1 for da, db in zip(dec_arm, b_decisions) if da != db)
    dM = flips / n
    p = mcnemar_p(b, c, alternative)
    return {"arm": name, "n": n, "b": b, "c": c, "flips": flips,
            "deltaM": dM, "p": p, "alternative": alternative,
            "acc_arm": sum(cor_arm), "acc_base": sum(b_correct)}

res = {
    "T1": arm_stats("T1", t1_cor, t1_dec, "greater"),
    "T2": arm_stats("T2", t2_cor, t2_dec, "less"),
    "C": arm_stats("C", c_cor, c_dec, "two-sided"),
}
for k, v in res.items():
    log("%s: flips=%d/%d ΔM=%.4f b=%d c=%d p=%.6f (%s) acc=%d/60 base=%d/60"
        % (k, v["flips"], n, v["deltaM"], v["b"], v["c"], v["p"],
           v["alternative"], v["acc_arm"], v["acc_base"]))

# ============ guards: post-hash + budget audit ============
cap_handle.remove()
m_gn.eager_attention_forward = ORIG_EAGER
post_hash = sha256_state_dict(model)
log("backbone post-hash: %s" % post_hash)
if post_hash != BACKBONE_PIN:
    run_invalid("(a) Δθ=0 post-hash mismatch")

expected_fwd = 4 * n + N_H
if FWD_COUNT[0] != expected_fwd:
    run_invalid("(f) budget audit: %d forwards != %d expected"
                % (FWD_COUNT[0], expected_fwd))
log("(f) budget audit PASS: %d forwards = 4*%d + %d" % (FWD_COUNT[0], n, N_H))

# ============ artifacts (Law #8) ============
per_item = []
for ii, it in enumerate(included):
    per_item.append({
        "item_id": it["id"], "stratum": it["phrasing"],
        "E": it["_E"], "N": it["_N"],
        "yhat_B": b_decisions[ii], "correct_B": b_correct[ii],
        "yhat_T1": t1_dec[ii], "correct_T1": t1_cor[ii],
        "yhat_T2": t2_dec[ii], "correct_T2": t2_cor[ii],
        "yhat_C": c_dec[ii], "correct_C": c_cor[ii],
    })
with open(os.path.join(OUT, "exp136_per_item.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(per_item[0].keys()))
    w.writeheader(); w.writerows(per_item)

records = {
    "experiment": "EXP136",
    "design": "B4/ARI attention-routing intervention",
    "prereg": "research/prereg/EXP136_PREREG_ARI_2026-09-30.md",
    "n": n, "excluded": excluded,
    "backbone_pin": BACKBONE_PIN, "pre_hash": pre_hash, "post_hash": post_hash,
    "bench_pin": bh, "hf_revision": HF_REVISION,
    "env": {"torch": torch.__version__, "numpy": np.__version__,
            "transformers": "5.17.0", "threads": torch.get_num_threads(),
            "seed": SEED_TORCH, "attn": "eager", "device": "cpu",
            "dtype": "float32"},
    "arms": res,
    "forwards": FWD_COUNT[0],
    "guards": {"a_dtheta": "PASS", "b_agreement": "PASS 60/60",
               "c_bench_span": "PASS", "d_hook_delivery": "PASS (2 phases)",
               "e_renorm": "PASS (per-forward)", "f_budget": "PASS"},
    "verdict": "RAW RESULTS ONLY — no interpretation (independent review lane decides)",
}
json.dump(records, open(os.path.join(OUT, "exp136_records.json"), "w"), indent=1)
rh = hashlib.sha256(open(os.path.join(OUT, "exp136_records.json"), "rb").read()).hexdigest()
log("records sha256: %s" % rh)
json.dump({"verdict": "RAW", "records_sha256": rh, "exit_code": 0},
          open(os.path.join(OUT, "exp136_verdict.json"), "w"), indent=1)
log("EXP136 execution complete: exit 0")
LOGF.close()
