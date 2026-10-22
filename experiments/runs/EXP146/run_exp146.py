#!/usr/bin/env python3
"""EXP146 (S7-4) execution: powered follow-up to EXP136 (attention-routing).

Executes EXACTLY per research/analysis_plans/S7-4_PREREG_DRAFT_2026-10-05.md
(Status: SIGNED, LOG-4937; Law #14 SIGN-WITH-FIXES + fix-verification PASS).
Identical EXP136 protocol (B4/ARI, Pythia-410m, arms B/T1/T2/C, seeds
discipline, guards) on TWO fresh 60-item benches (seeds 7401/7402).
$0 CPU. Frozen backbone. Exit codes: 0 = clean completion (verdict per §4);
44 = RUN-INVALID (guard trip, never a verdict).
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
LOGF = open(os.path.join(OUT, "exp146_run_log.txt"), "w")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOGF.write(line + "\n"); LOGF.flush()

# ============ §5.1 pinned constants (identical to EXP136) ============
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
MODEL_ID = "EleutherAI/pythia-410m"
LAYER = 20
D_MAX_EXCL = 6          # pooled across both benches (§5.7c)
SEED_TORCH = 136013
BETA_T1 = 3.0
N_H = 2                # (h) probes: one T2 + one T1
BENCH1_PIN = "83af7daa5596f351f0412ab4938ec4d3eb70477aad12915de6b7851b73a05eb5"
BENCH2_PIN = "c7d280ebc9a0eb6d6c761b91557570159671a842754792355b013ec0f695048b"
PLAN_DIR = os.path.abspath(os.path.join(RUN_DIR, "..", "..", "..", "research",
                                        "analysis_plans"))

torch.manual_seed(SEED_TORCH)
torch.set_num_threads(2)
log("torch %s | transformers %s | numpy %s | threads=%d | seed=%d"
    % (torch.__version__, __import__("transformers").__version__,
       np.__version__, torch.get_num_threads(), SEED_TORCH))

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
    rec = {"experiment": "EXP146", "verdict": "RUN-INVALID", "reason": reason,
           "forwards": FWD_COUNT[0], "exit_code": 44}
    json.dump(rec, open(os.path.join(OUT, "exp146_verdict.json"), "w"), indent=1)
    LOGF.close()
    sys.exit(44)

# ============ incremental per-item records (EXP143 VM-restart-drain lesson) ==
JSONL = os.path.join(OUT, "exp146_per_item.jsonl")
def write_record(rec):
    with open(JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")
        f.flush()
        os.fsync(f.fileno())

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

# ============ benches (S7-4 fresh, pinned JSONs; Step 0 / guard (c)) =========
REPO_ROOT = os.path.abspath(os.path.join(RUN_DIR, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))
from reference_implementation import bench_sha256  # noqa: E402 (canonical pin fn)

def load_bench(fname, pin, tag):
    path = os.path.join(PLAN_DIR, fname)
    with open(path) as f:
        bench = json.load(f)
    if len(bench) != 60:
        run_invalid("(c) %s len %d != 60" % (tag, len(bench)))
    bh = bench_sha256(bench)
    log("(c) %s sha256=%s" % (tag, bh))
    if bh != pin:
        run_invalid("(c) %s pin mismatch: got %s expected %s" % (tag, bh, pin))
    log("(c) %s pin PASS" % tag)
    return bench, bh

bench1, bh1 = load_bench("S7-4_BENCH1_2026-10-05.json", BENCH1_PIN, "Bench1")
bench2, bh2 = load_bench("S7-4_BENCH2_2026-10-05.json", BENCH2_PIN, "Bench2")
for b, tag in ((bench1, "Bench1"), (bench2, "Bench2")):
    for it in b:
        it["_bench"] = tag

# ============ entity-span derivation (committed EXP136 procedure, verbatim) ==
# Copied verbatim from experiments/runs/EXP136_ari/run_exp136.py
# (entity_span_token_idx, tok1, _word_pattern). NOT imported: importing that
# module would execute the EXP136 experiment. Read-only reuse of the committed
# procedure per S7-4 §5.2.
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
included1, included2 = [], []
for bench, included, tag in ((bench1, included1, "Bench1"),
                             (bench2, included2, "Bench2")):
    for it in bench:
        try:
            sidx, offs = entity_span_token_idx(it["prompt"], it["A"], it["C"])
            N_i = len(offs)
            E_i = len(sidx)
            ok = (E_i >= 1 and E_i < N_i and (E_i / N_i) <= 0.5
                  and (not sidx or max(sidx) < N_i - 1))
            for t in sidx:
                c0, c1 = offs[t]
                assert any(c0 <= s0 and c1 >= s1 for (s0, s1) in
                           [m.span() for name in (it["A"], it["C"])
                            for m in _word_pattern(name).finditer(it["prompt"])])
            if not ok or not sidx:
                raise ValueError("span operating-condition violation: E=%d N=%d"
                                 % (E_i, N_i))
            it["_span"] = sidx
            it["_E"] = E_i
            it["_N"] = N_i
            it["_tA"] = tok1(it["A"])
            it["_tC"] = tok1(it["C"])
            included.append(it)
        except Exception as ex:
            excluded.append((tag, it["id"], str(ex)))
            log("excluded %s %s: %s" % (tag, it["id"], ex))

e = len(excluded)
log("span derivation: excluded=%d pooled" % e)
if e > D_MAX_EXCL:
    run_invalid("(c) exclusions %d > 6 pooled" % e)
n1, n2 = len(included1), len(included2)
log("n1=%d (Bench1) n2=%d (Bench2) pooled n=%d" % (n1, n2, n1 + n2))

# ============ attention-weight patch (identical to EXP136) ===================
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

CAP = {}
def _cap_hook(module, inp, out):
    CAP["o"] = out[0].detach().cpu()
cap_handle = L20_ATTN.register_forward_hook(_cap_hook)

def base_forward(input_ids, want_attn=False):
    with torch.no_grad():
        out = model(input_ids=input_ids, output_attentions=want_attn)
    count_fwd(1)
    return out

def decide(logits, tA, tC):
    if not torch.isfinite(logits).all():
        raise RunInvalid("(b) non-finite logits")
    lv = logits[0, -1, :]
    return "A" if float(lv[tA]) >= float(lv[tC]) else "C"

# ============ B passes (guard (b): archive + non-degeneracy) ================
log("B pass Bench1: %d items (eager, no hook)" % n1)
PATCH["active"] = False
B1, B1c, B1ids = [], [], []
w_base = o_base = q0 = None
for ii, it in enumerate(included1):
    ids = tokenizer(it["prompt"], add_special_tokens=False,
                    return_tensors="pt")["input_ids"]
    q_i = ids.shape[1] - 1
    out = base_forward(ids, want_attn=(ii == 0))
    yhat = decide(out.logits, it["_tA"], it["_tC"])
    B1.append(yhat); B1c.append(1 if yhat == "A" else 0); B1ids.append(it["id"])
    if ii == 0:
        w_base = out.attentions[LAYER][0, :, q_i, :].detach().cpu()
        o_base = CAP["o"].clone()
        q0 = q_i
        log("captured w_base/o_base on Bench1 item 0 (q=%d)" % q_i)

log("B pass Bench2: %d items (eager, no hook)" % n2)
B2, B2c, B2ids = [], [], []
for it in included2:
    ids = tokenizer(it["prompt"], add_special_tokens=False,
                    return_tensors="pt")["input_ids"]
    out = base_forward(ids, want_attn=False)
    yhat = decide(out.logits, it["_tA"], it["_tC"])
    B2.append(yhat); B2c.append(1 if yhat == "A" else 0); B2ids.append(it["id"])

# guard (b): non-degeneracy across pooled n=120 (EXP094-B check retired, §5.7b)
pooled_B = B1 + B2
if not (any(d == "A" for d in pooled_B) and any(d == "C" for d in pooled_B)):
    run_invalid("(b) B decisions degenerate across pooled n=%d" % len(pooled_B))
log("(b) B-decision archive recorded (%d items); non-degeneracy PASS "
    "(A=%d C=%d pooled)" % (len(pooled_B), sum(1 for d in pooled_B if d == "A"),
                            sum(1 for d in pooled_B if d == "C")))
for tag, ids_l, dec_l, cor_l in (("Bench1", B1ids, B1, B1c),
                                  ("Bench2", B2ids, B2, B2c)):
    for iid, yh, yc in zip(ids_l, dec_l, cor_l):
        write_record({"phase": "B", "bench": tag, "item_id": iid,
                      "yhat": yh, "correct": yc})

# ============ (h) hook-delivery control (mandatory, §5.6) ====================
log("(h) Phase 1: T2 span-ablate hook delivery (Bench1 item 0)")
it0 = included1[0]
span0 = it0["_span"]
try:
    PATCH.update({"active": True, "mode": "T2", "span": span0, "q": q0})
    ids0 = tokenizer(it0["prompt"], add_special_tokens=False,
                     return_tensors="pt")["input_ids"]
    out = base_forward(ids0, want_attn=True)
    w = out.attentions[LAYER][0, :, q0, :].detach().cpu()
    o = CAP["o"].clone()
    m1 = float(w[:, span0].sum(dim=-1).max())
    assert m1 < 1e-6, "P1 assert2: max_h span mass = %g" % m1
    m2 = float((w.sum(dim=-1) - 1.0).abs().max())
    assert m2 < 1e-5, "P1 assert3: max |sum-1| = %g" % m2
    assert torch.isfinite(w).all(), "P1 assert4: non-finite weights"
    m3 = float((w - w_base).abs().sum(dim=-1).mean())
    assert m3 > 0.01, "P1 assert5: mean L1 = %g" % m3
    m4 = float((o - o_base).norm())
    assert m4 > 1e-6, "P1 assert6: ||o-o_base|| = %g" % m4
    log("(h) Phase 1 PASS: spanmass=%.2e renorm=%.2e L1=%.4f dOut=%.2e"
        % (m1, m2, m3, m4))
finally:
    PATCH["active"] = False

log("(h) Phase 2: T1 span-boost hook delivery (Bench1 item 0)")
try:
    PATCH.update({"active": True, "mode": "T1", "span": span0, "q": q0})
    out = base_forward(ids0, want_attn=True)
    w = out.attentions[LAYER][0, :, q0, :].detach().cpu()
    o = CAP["o"].clone()
    m8 = float((w - w_base).abs().sum(dim=-1).mean())
    assert m8 > 0.01, "P2 assert8: mean L1 = %g" % m8
    mb_new = float(w[:, span0].sum(dim=-1).mean())
    mb_old = float(w_base[:, span0].sum(dim=-1).mean())
    assert mb_new > mb_old, "P2 assert9: %.6f not > %.6f" % (mb_new, mb_old)
    assert mb_new > 1e-3, "P2 assert10: boosted span mass = %g" % mb_new
    m11 = float((w.sum(dim=-1) - 1.0).abs().max())
    assert m11 < 1e-5, "P2 assert11: max |sum-1| = %g" % m11
    assert torch.isfinite(w).all(), "P2 assert12: non-finite weights"
    m13 = float((o - o_base).norm())
    assert m13 > 1e-6, "P2 assert13: ||o-o_base|| = %g" % m13
    log("(h) Phase 2 PASS: L1=%.4f spanmass %.4f>%.4f floor-ok renorm=%.2e dOut=%.2e"
        % (m8, mb_new, mb_old, m11, m13))
finally:
    PATCH["active"] = False
log("(h) hook-delivery PASS on both hooks")

# ============ decision passes: T1, T2, C on both benches =====================
def arm_pass(mode, included, tag):
    log("%s pass %s: %d items" % (mode, tag, len(included)))
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
            write_record({"phase": mode, "bench": tag, "item_id": it["id"],
                          "yhat": yhat, "correct": cor[-1]})
    finally:
        PATCH["active"] = False
    return dec, cor

T1a, T1ac = arm_pass("T1", included1, "Bench1")
T2a, T2ac = arm_pass("T2", included1, "Bench1")
Ca, Cac = arm_pass("C", included1, "Bench1")
T1b, T1bc = arm_pass("T1", included2, "Bench2")
T2b, T2bc = arm_pass("T2", included2, "Bench2")
Cb, Cbc = arm_pass("C", included2, "Bench2")

# ============ guards: post-hash + budget audit ===============================
cap_handle.remove()
m_gn.eager_attention_forward = ORIG_EAGER
post_hash = sha256_state_dict(model)
log("backbone post-hash: %s" % post_hash)
if post_hash != BACKBONE_PIN:
    run_invalid("(a) Δθ=0 post-hash mismatch")

n = n1 + n2
expected_fwd = 4 * n + N_H
if FWD_COUNT[0] != expected_fwd:
    run_invalid("(f) budget audit: %d forwards != %d expected"
                % (FWD_COUNT[0], expected_fwd))
log("(f) budget audit PASS: %d forwards = 4*%d + %d" % (FWD_COUNT[0], n, N_H))

# ============ endpoint statistics (Law #9, §5.5 / frozen §3 bars) ============
def mcnemar_p(b, c, alternative):
    n_ = b + c
    if n_ == 0:
        return 1.0
    if alternative == "greater":
        return sum(math.comb(n_, k) for k in range(b, n_ + 1)) / 2**n_
    if alternative == "less":
        return sum(math.comb(n_, k) for k in range(c, n_ + 1)) / 2**n_
    p = 2 * sum(math.comb(n_, k) for k in range(max(b, c), n_ + 1)) / 2**n_
    return min(p, 1.0)

def bc(cor_arm, cor_base):
    b = sum(1 for ca, cb in zip(cor_arm, cor_base) if ca and not cb)
    c = sum(1 for ca, cb in zip(cor_arm, cor_base) if not ca and cb)
    return b, c

def wald_ci_upper(b, c, n_, direction):
    # direction: +1 -> (b-c)/n ; -1 -> (c-b)/n ; §3: SE=√[(b+c)−(b−c)²/n]/n
    delta = direction * (b - c) / n_
    se = math.sqrt(max((b + c) - (b - c) ** 2 / n_, 0.0)) / n_
    return delta + 1.96 * se, delta, se

def arm_block(name, cor_b1, base_b1, cor_b2, base_b2, alt_dir, ci_dir):
    b1, c1 = bc(cor_b1, base_b1)
    b2, c2 = bc(cor_b2, base_b2)
    b, c = b1 + b2, c1 + c2
    n_ = len(cor_b1) + len(cor_b2)
    flips = sum(1 for ca, cb in zip(cor_b1 + cor_b2, base_b1 + base_b2)
                if ca != cb)
    if alt_dir == "greater":
        p_dir = mcnemar_p(b, c, "greater")
    elif alt_dir == "less":
        p_dir = mcnemar_p(b, c, "less")
    else:
        p_dir = mcnemar_p(b, c, "two-sided")
    p_two = mcnemar_p(b, c, "two-sided")
    ci_up, delta, se = wald_ci_upper(b, c, n_, ci_dir)
    # per-bench one-sided p in predicted and anti directions (diagnostic)
    if alt_dir == "greater":
        p_b1 = mcnemar_p(b1, c1, "greater"); p_b2 = mcnemar_p(b2, c2, "greater")
        p_b1_anti = mcnemar_p(b1, c1, "less"); p_b2_anti = mcnemar_p(b2, c2, "less")
        repl = (b1 > c1) and (b2 > c2)
    elif alt_dir == "less":
        p_b1 = mcnemar_p(b1, c1, "less"); p_b2 = mcnemar_p(b2, c2, "less")
        p_b1_anti = mcnemar_p(b1, c1, "greater"); p_b2_anti = mcnemar_p(b2, c2, "greater")
        repl = (c1 > b1) and (c2 > b2)
    else:
        p_b1 = mcnemar_p(b1, c1, "two-sided"); p_b2 = mcnemar_p(b2, c2, "two-sided")
        p_b1_anti = p_b1; p_b2_anti = p_b2
        repl = None
    return {"arm": name, "n": n_, "n1": len(cor_b1), "n2": len(cor_b2),
            "b": b, "c": c, "b1": b1, "c1": c1, "b2": b2, "c2": c2,
            "flips": flips, "deltaM": flips / n_,
            "p_directional": p_dir, "p_twosided": p_two,
            "p_b1": p_b1, "p_b2": p_b2,
            "p_b1_anti": p_b1_anti, "p_b2_anti": p_b2_anti,
            "ci_delta": delta, "ci_se": se, "ci_upper": ci_up,
            "replication_sign": repl,
            "acc_arm": sum(cor_b1) + sum(cor_b2),
            "acc_base": sum(base_b1) + sum(base_b2)}

T1 = arm_block("T1", T1ac, B1c, T1bc, B2c, "greater", +1)
T2 = arm_block("T2", T2ac, B1c, T2bc, B2c, "less", -1)
C = arm_block("C", Cac, B1c, Cbc, B2c, "two-sided", +1)
for v in (T1, T2, C):
    log("%(arm)s pooled n=%(n)d: flips=%(flips)d ΔM=%(deltaM).4f b=%(b)d c=%(c)d "
        "p_dir=%(p_directional).6f p_2s=%(p_twosided).6f CI_up=%(ci_upper).4f "
        "[b1=%(b1)d c1=%(c1)d p1=%(p_b1).4f | b2=%(b2)d c2=%(c2)d p2=%(p_b2).4f] "
        "repl=%(replication_sign)s" % v)

# ============ §4 decision table (precedence RUN-INVALID > HELD > KILL > CONTINUE)
T1_sig = T1["p_directional"] < 0.05
T2_sig = T2["p_directional"] < 0.05
C_sig = C["p_twosided"] <= 0.05
C_null = C["p_twosided"] > 0.05

def kill_conj(v):
    return (v["p_directional"] >= 0.1 and v["p_twosided"] >= 0.1
            and v["ci_upper"] < 0.10)

hetero = (T1["p_b1_anti"] < 0.05 or T1["p_b2_anti"] < 0.05
          or T2["p_b1_anti"] < 0.05 or T2["p_b2_anti"] < 0.05)

verdict = None
verdict_cell = None
if (T1_sig or T2_sig) and C_sig:
    verdict, verdict_cell = "HELD", "unattributable (routing arm + C significant)"
elif ((T1_sig and T1["replication_sign"]) or
      (T2_sig and T2["replication_sign"])) and C_null:
    verdict, verdict_cell = "CONTINUE", "directional replication + null control"
elif kill_conj(T1) and kill_conj(T2) and not hetero:
    verdict, verdict_cell = ("KILL",
        "powered null both arms; ≥10pp excluded; (h) PASS")
else:
    verdict, verdict_cell = "HELD", "meets neither CONTINUE nor KILL"
log("VERDICT per §4: %s — %s" % (verdict, verdict_cell))

# ============ artifacts (Law #8) ============================================
records = {
    "experiment": "EXP146",
    "design": "S7-4 powered follow-up to EXP136 (B4/ARI attention-routing)",
    "prereg": "research/analysis_plans/S7-4_PREREG_DRAFT_2026-10-05.md",
    "n1": n1, "n2": n2, "n_pooled": n, "excluded": excluded,
    "backbone_pin": BACKBONE_PIN, "pre_hash": pre_hash, "post_hash": post_hash,
    "bench1_pin": bh1, "bench2_pin": bh2, "hf_revision": HF_REVISION,
    "env": {"torch": torch.__version__, "numpy": np.__version__,
            "transformers": __import__("transformers").__version__,
            "threads": torch.get_num_threads(), "seed": SEED_TORCH,
            "attn": "eager", "device": "cpu", "dtype": "float32"},
    "arms": {"T1": T1, "T2": T2, "C": C},
    "forwards": FWD_COUNT[0],
    "guards": {"a_dtheta": "PASS", "b_archive_nondeg": "PASS",
               "c_bench_span": "PASS (excluded=%d)" % e,
               "d_hook_delivery": "PASS (2 phases)", "e_renorm": "PASS",
               "f_budget": "PASS %d" % FWD_COUNT[0]},
    "verdict": verdict, "verdict_cell": verdict_cell,
}
json.dump(records, open(os.path.join(OUT, "exp146_records.json"), "w"), indent=1)
rh = hashlib.sha256(open(os.path.join(OUT, "exp146_records.json"), "rb").read()
                    ).hexdigest()
log("records sha256: %s" % rh)
json.dump({"experiment": "EXP146", "verdict": verdict,
           "verdict_cell": verdict_cell, "records_sha256": rh, "exit_code": 0},
          open(os.path.join(OUT, "exp146_verdict.json"), "w"), indent=1)
log("EXP146 execution complete: exit 0")
LOGF.close()
