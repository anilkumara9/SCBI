#!/usr/bin/env python3
"""EXP127 (TGA) executor — LOG-4698.

Transient-Growth Amplification of the frozen Pythia-410m L20->L24
residual-stream propagator M = d x_{24,last} / d x_{20,last}
(clamped-context final-token map, all KVs clamped to base-pass values).

$0 CPU. Delta-theta = 0 by construction: pure autograd JVPs/VJPs through
a frozen model in eval mode; no optimizer, no loss, no backward pass
into weights; all parameter tensors carry requires_grad=False.

Falsification-tree order (Law #9): guards -> backbone pin -> convergence
-> null arms -> raw records hash-pinned -> re-pin -> R -> decision.
"""
import hashlib
import json
import math
import os
import sys
import time

import numpy as np
import torch
import torch.nn.functional as F
import transformers

# ---------------- Law #13 pins ----------------
PROTOCOL = os.path.expanduser(
    "~/workspace/SCBI/research/prereg/EXP_PREREG_TGA_TRANSIENTGROWTH_2026-09-29.md")
PROTOCOL_PIN = "5dea0d419794fe6aa1fce056b9225625aa6ec3b55c57fab39bb7cb9e7d6e2882"
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
SNAP = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
EXP107DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl")
OUTDIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP127_tga/out")
os.makedirs(OUTDIR, exist_ok=True)
LOGF = open(os.path.join(OUTDIR, "exp127_console.log"), "a")


def log(s):
    print(s, flush=True)
    LOGF.write(str(s) + "\n")
    LOGF.flush()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def state_dict_hash(model):
    """Canonical LOG-331 method: sha256 over sorted state_dict keys, float32 bytes."""
    sha = hashlib.sha256()
    sd = model.state_dict()
    for k in sorted(sd.keys()):
        sha.update(np.asarray(sd[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()


# ---------------- 0. protocol hash before anything ----------------
log("== EXP127 (TGA) execution lane LOG-4698 ==")
h_proto = sha256_file(PROTOCOL)
log("protocol sha256: %s" % h_proto)
if h_proto != PROTOCOL_PIN:
    log("HALT: protocol hash mismatch. Tree terminates before any R is minted.")
    sys.exit(42)
log("protocol pin OK (post-fix LOG-4697 revision)")

# ---------------- 1. prompts: verbatim EXP107 bench, canonical first 10 ----------------
sys.path.insert(0, EXP107DIR)
from build_exp107_bench import build_bench  # noqa: E402

bench = build_bench()
assert len(bench) == 60, "EXP107 bench len != 60"
prompts = bench[:10]
prompt_ids = [b["id"] for b in prompts]
prompt_texts = [b["prompt"] for b in prompts]
log("prompts: canonical-order first 10 of verbatim EXP107 bench")
for i, pid in enumerate(prompt_ids):
    log("  [%d] %s" % (i, pid))

# ---------------- 2. environment ----------------
torch.manual_seed(20260929)
torch.set_num_threads(2)
threads = torch.get_num_threads()
assert threads == 2, "thread read-back != 2"
log("torch %s | transformers %s | numpy %s | threads=%d (read back)"
    % (torch.__version__, transformers.__version__, np.__version__, threads))

# ---------------- 3. frozen backbone ----------------
model = transformers.AutoModelForCausalLM.from_pretrained(
    SNAP, local_files_only=True, trust_remote_code=False,
    device_map="cpu", torch_dtype=torch.float32,
    output_hidden_states=True, output_attentions=False)
model.eval()
for p in model.parameters():
    p.requires_grad_(False)
h_pre = state_dict_hash(model)
log("backbone LOG-331 pin (pre): %s" % h_pre)
if h_pre != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash mismatch before first JVP (Law #6). Quarantine. No R exists.")
    sys.exit(42)
log("backbone pin OK. Delta-theta guard armed.")

tokenizer = transformers.AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
cfg = model.config
H, NH, HD = cfg.hidden_size, cfg.num_attention_heads, cfg.hidden_size // cfg.num_attention_heads
assert (H, NH, HD) == (1024, 16, 64)
LN_EPS = cfg.layer_norm_eps
RND = 16  # rotary_ndims = head_dim * rotary_pct
assert cfg.use_parallel_residual, "expected parallel-residual Pythia block"
log("model: H=%d NH=%d HD=%d rotary_ndims=%d parallel_residual=%s ln_eps=%g"
    % (H, NH, HD, RND, cfg.use_parallel_residual, LN_EPS))

# ---------------- 4. weight views (detached constants) ----------------
layers = model.gpt_neox.layers
inv_freq = model.gpt_neox.rotary_emb.inv_freq.detach().clone()  # (8,)
assert inv_freq.numel() == RND // 2
W = {"ln1w": [], "ln1b": [], "ln2w": [], "ln2b": [],
     "qkv": [], "qkvb": [], "dense": [], "denseb": [],
     "h4": [], "h4b": [], "o4": [], "o4b": []}
for L in range(20, 24):
    ly = layers[L]
    W["ln1w"].append(ly.input_layernorm.weight.detach())
    W["ln1b"].append(ly.input_layernorm.bias.detach())
    W["ln2w"].append(ly.post_attention_layernorm.weight.detach())
    W["ln2b"].append(ly.post_attention_layernorm.bias.detach())
    W["qkv"].append(ly.attention.query_key_value.weight.detach())
    W["qkvb"].append(ly.attention.query_key_value.bias.detach())
    W["dense"].append(ly.attention.dense.weight.detach())
    W["denseb"].append(ly.attention.dense.bias.detach())
    W["h4"].append(ly.mlp.dense_h_to_4h.weight.detach())
    W["h4b"].append(ly.mlp.dense_h_to_4h.bias.detach())
    W["o4"].append(ly.mlp.dense_4h_to_h.weight.detach())
    W["o4b"].append(ly.mlp.dense_4h_to_h.bias.detach())
SCALE = NH ** 0  # placeholder replaced below
SCALE = (1.0 / math.sqrt(HD))
log("weight views gathered for layers 20-23; attention scale=%g" % SCALE)


def rotate_vec(r, pos):
    """GPT-NeoX rotary on the first RND dims of a (...,64) tensor.
    pos: scalar int or (T,) tensor of positions."""
    ang = torch.as_tensor(pos).reshape(-1, 1) * inv_freq.reshape(1, -1)  # (T,8) or (1,8)
    c = torch.cat([ang.cos(), ang.cos()], dim=-1)  # (T,16)
    s = torch.cat([ang.sin(), ang.sin()], dim=-1)
    r_rot = r[..., :RND]
    while c.dim() < r_rot.dim():
        c = c.unsqueeze(0)
        s = s.unsqueeze(0)
    r1, r2 = r_rot[..., :RND // 2], r_rot[..., RND // 2:]
    rh = torch.cat([-r2, r1], dim=-1)
    return torch.cat([r_rot * c + rh * s, r[..., RND:]], dim=-1)


# per-head q/k/v weight views: rows [h*192:h*192+64] = q_h, [+64:+128] = k_h, [+128:+192] = v_h
QW, QB, KW, KB, VW, VB = [], [], [], [], [], []
for L in range(20, 24):
    qw, qb, kw, kb, vw, vb = [], [], [], [], [], []
    Wqkv, Bqkv = W["qkv"][L - 20], W["qkvb"][L - 20]
    for hd in range(NH):
        o = hd * 3 * HD
        qw.append(Wqkv[o:o + HD]);        qb.append(Bqkv[o:o + HD])
        kw.append(Wqkv[o + HD:o + 2 * HD]); kb.append(Bqkv[o + HD:o + 2 * HD])
        vw.append(Wqkv[o + 2 * HD:o + 3 * HD]); vb.append(Bqkv[o + 2 * HD:o + 3 * HD])
    QW.append(qw); QB.append(qb); KW.append(kw); KB.append(kb); VW.append(vw); VB.append(vb)
log("per-head q/k/v views built (interleaved layout verified against module)")


def build_clamped_kv(h_base, li):
    """h_base: (T,1024) layer-input hidden states from the base pass (detached).
    li: span-layer index 0..3 (layer 20+li). Returns K,V: (NH, T, HD) with rotary on K."""
    u = F.layer_norm(h_base, (H,), W["ln1w"][li], W["ln1b"][li], LN_EPS)
    T = h_base.shape[0]
    K = torch.empty(NH, T, HD)
    V = torch.empty(NH, T, HD)
    pos = torch.arange(T)
    for hd in range(NH):
        k = u @ KW[li][hd].T + KB[li][hd]
        v = u @ VW[li][hd].T + VB[li][hd]
        K[hd] = rotate_vec(k, pos)
        V[hd] = v
    return K, V


def make_f(Kc, Vc, T):
    """Clamped-context final-token map f: R^1024 -> R^1024.
    Kc,Vc: lists over the 4 span layers of (NH,T,HD) clamped K/V.
    Only the block-20 input residual at the last token varies."""
    def f(z):
        h = z
        for li in range(4):
            # attention branch (Q free, K/V clamped)
            u = F.layer_norm(h, (H,), W["ln1w"][li], W["ln1b"][li], LN_EPS)
            q = torch.stack([u @ QW[li][hd].T + QB[li][hd] for hd in range(NH)])
            q = rotate_vec(q, T - 1)
            scores = (q.unsqueeze(-2) @ Kc[li].transpose(-1, -2)).squeeze(-2) * SCALE  # (NH, T)
            att = torch.softmax(scores, dim=-1)
            o = (att.unsqueeze(-2) @ Vc[li]).squeeze(-2).reshape(H)
            ao = o @ W["dense"][li].T + W["denseb"][li]
            # mlp branch (parallel residual)
            m = F.layer_norm(h, (H,), W["ln2w"][li], W["ln2b"][li], LN_EPS)
            mo = F.gelu(m @ W["h4"][li].T + W["h4b"][li]) @ W["o4"][li].T + W["o4b"][li]
            h = h + ao + mo
        return h
    return f


def jvp(f, z, v):
    return torch.autograd.functional.jvp(f, (z,), (v,))[1]


def vjp(f, z, w):
    # torch>=2.x: vjp(f, inputs, v) returns (output, vjp_result) directly
    return torch.autograd.functional.vjp(f, (z,), (w,))[1][0]


def power_iteration(f, z, gen, tol, min_iter, max_iter, v1=None, label="s1"):
    """Randomized power iteration on M^T M (deflated against v1 if given).
    Returns (sigma, v, iters, trace, converged, products)."""
    products = 0
    v = torch.randn(H, generator=gen)
    if v1 is not None:
        v = v - (v1 @ v) * v1
    v = v / v.norm()
    rho_prev, consec, it, trace = None, 0, 0, []
    while True:
        w = jvp(f, z, v)
        products += 1
        t = vjp(f, z, w)
        products += 1
        if v1 is not None:
            t = t - (v1 @ t) * v1
        v = t / t.norm()
        rho = float((w.norm() ** 2).item())
        it += 1
        trace.append(rho)
        if rho_prev is not None and rho_prev > 0:
            rel = abs(rho - rho_prev) / rho_prev
            consec = consec + 1 if rel < tol else 0
        rho_prev = rho
        if it >= min_iter and consec >= 5:
            return math.sqrt(rho), v.detach(), it, trace, True, products
        if it >= max_iter:
            return math.sqrt(rho), v.detach(), it, trace, False, products


log("executor defined; entering per-prompt measurement")

# ---------------- 5. per-prompt measurement ----------------
K_HUTCH, K_DIRECT = 64, 64
BUDGET_CAP = 700
SMOKE = os.environ.get("EXP127_SMOKE") == "1"
if SMOKE:
    log("!! SMOKE MODE: machinery validation only — no numbers minted, no verdict !!")
    prompts = prompts[:1]
    prompt_ids = prompt_ids[:1]
    prompt_texts = prompt_texts[:1]
results = []
v1_store, urand_store = {}, {}

for pi in range(len(prompts)):
    t0 = time.time()
    pid, text = prompt_ids[pi], prompt_texts[pi]
    log("--- prompt %d/%d: %s" % (pi + 1, len(prompts), pid))
    gen = torch.Generator()
    gen.manual_seed(20260929 + pi)

    toks = tokenizer(text, return_tensors="pt")
    T = toks["input_ids"].shape[1]
    with torch.no_grad():
        out = model(**toks)
    hs = out.hidden_states
    assert len(hs) == 25
    h20_in = hs[20][0].detach()          # input of block 20, all positions
    # NOTE (transformers 5.x @capture_outputs): hs[24] is the FINAL-LAYER-NORM
    # output, not block 23's output. The protocol's x_{24} = output of block 23
    # (pre-norm) is obtained from the real layer-23 module (exact: verified
    # fln(module(hs[23])) == hs[24] to 0.0).
    with torch.no_grad():
        pos_emb = model.gpt_neox.rotary_emb(
            hs[23], position_ids=torch.arange(T).unsqueeze(0))
        x24_base = layers[23](hs[23], attention_mask=None,
                              position_embeddings=pos_emb)[0, -1].detach()
    z0 = h20_in[-1].detach()

    # clamped K/V per span layer from base-pass hidden states
    Kc, Vc = [], []
    for li in range(4):
        K, V = build_clamped_kv(hs[20 + li][0].detach(), li)
        Kc.append(K)
        Vc.append(V)
    f = make_f(Kc, Vc, T)

    # sanity: manual span must reproduce the real model at the base point (diagnostic)
    with torch.no_grad():
        fz0 = f(z0)
    sanity = float((fz0 - x24_base).abs().max().item())
    log("  T=%d | sanity max|f(z0)-x24_base| = %.3e" % (T, sanity))

    z = z0.clone().requires_grad_(True)
    counts = {}

    # σ1 power iteration
    s1, v1, it1, tr1, conv1, c1 = power_iteration(
        f, z, gen, tol=1e-6, min_iter=20, max_iter=200)
    counts["sigma1"] = c1
    log("  sigma1=%.6f iters=%d converged=%s products=%d" % (s1, it1, conv1, c1))
    if SMOKE:
        # machinery validation: one extra JVP+VJP pair, then stop
        w = jvp(f, z, v1)
        t = vjp(f, z, w)
        log("  SMOKE: extra JVP/VJP ok | ||Mv1||=%.6f ||Mt||=%.6f" % (w.norm().item(), t.norm().item()))
        log("  SMOKE complete — exiting before any verdict machinery")
        sys.exit(0)

    # deflated σ2
    s2, v2, it2, tr2, conv2, c2 = power_iteration(
        f, z, gen, tol=1e-4, min_iter=10, max_iter=200, v1=v1)
    counts["sigma2"] = c2
    log("  sigma2=%.6f iters=%d converged=%s products=%d | s1/s2=%.4f"
        % (s2, it2, conv2, c2, s1 / s2 if s2 > 0 else float("nan")))

    # Hutchinson arm (K=64 Rademacher, same M, same budget)
    c3 = 0
    acc = 0.0
    for _ in range(K_HUTCH):
        r = (torch.randint(0, 2, (H,), generator=gen).float() * 2 - 1)
        w = jvp(f, z, r)
        c3 += 1
        t = vjp(f, z, w)
        c3 += 1
        acc += float((r @ t).item())
    counts["hutchinson"] = c3
    tr_est = acc / K_HUTCH
    sbar = math.sqrt(tr_est / H)
    log("  hutchinson: Tr(MTM)=%.6f sigma_bar=%.6f products=%d" % (tr_est, sbar, c3))

    # direct random-direction arm (K=64 isotropic, median ||Mu||)
    c4 = 0
    norms = []
    us = []
    for _ in range(K_DIRECT):
        u = torch.randn(H, generator=gen)
        u = u / u.norm()
        us.append(u.detach().numpy().astype(np.float32))
        w = jvp(f, z, u)
        c4 += 1
        norms.append(float(w.norm().item()))
    counts["direct"] = c4
    direct_med = float(np.median(np.array(norms)))
    log("  direct: median||Mu||=%.6f products=%d" % (direct_med, c4))

    total = sum(counts.values())
    log("  products total=%d (cap %d)" % (total, BUDGET_CAP))
    assert total <= BUDGET_CAP, "budget cap exceeded"

    trip = abs(direct_med - sbar) / sbar if sbar > 0 else float("nan")
    log("  direct-vs-hutchinson agreement trip: |med-sbar|/sbar = %.4f (diagnostic, <=0.15)"
        % trip)

    R = s1 / sbar if sbar > 0 else float("nan")
    results.append({
        "prompt_id": pid, "prompt": text, "T": T,
        "sanity_max_abs": sanity,
        "sigma1": s1, "sigma1_iters": it1, "sigma1_converged": conv1,
        "sigma1_trace": tr1,
        "sigma2": s2, "sigma2_iters": it2, "sigma2_converged": conv2,
        "sigma2_trace": tr2,
        "sigma1_over_sigma2": (s1 / s2) if s2 > 0 else None,
        "hutchinson_trace": tr_est, "sigma_bar": sbar,
        "direct_median": direct_med, "direct_norms": norms,
        "direct_trip": trip,
        "R": R,
        "products": counts, "products_total": total,
        "seconds": time.time() - t0,
    })
    v1_store[pid] = v1.detach().numpy().astype(np.float32)
    urand_store[pid] = np.stack(us)

# ---------------- 6. raw records hash-pinned BEFORE any verdict ----------------
log("== hash-pinning raw records (Law #9: before R is read) ==")
per_prompt_path = os.path.join(OUTDIR, "exp127_per_prompt.json")
with open(per_prompt_path, "w") as fh:
    json.dump(results, fh, indent=1)
vec_path = os.path.join(OUTDIR, "exp127_vectors.npz")
np.savez_compressed(vec_path,
                    **{"v1__" + pid: v1_store[pid] for pid in prompt_ids},
                    **{"urand__" + pid: urand_store[pid] for pid in prompt_ids})
manifest = {
    "experiment": "EXP127_TGA", "log": "LOG-4698",
    "protocol_sha256": PROTOCOL_PIN,
    "weights_snap": SNAP,
    "backbone_pin_pre": h_pre,
    "prompt_ids": prompt_ids,
    "seeds": [20260929 + i for i in range(10)],
    "env": {"torch": torch.__version__, "transformers": transformers.__version__,
            "numpy": np.__version__, "threads": threads, "dtype": "float32",
            "device": "cpu", "model": "pythia-410m-local"},
    "budget_cap_per_prompt": BUDGET_CAP,
    "arms": {"sigma1": "power iteration 1e-6/5it/>=20",
             "sigma2": "deflated power iteration 1e-4/5it/>=10",
             "hutchinson": "K=64 Rademacher", "direct": "K=64 isotropic median"},
}
manifest_path = os.path.join(OUTDIR, "exp127_worksheet.json")
with open(manifest_path, "w") as fh:
    json.dump(manifest, fh, indent=1)
# validate the manifest round-trips (EXP126 worksheet-truncation lesson)
with open(manifest_path) as fh:
    assert json.load(fh)["backbone_pin_pre"] == h_pre

pins = {p: sha256_file(p) for p in (per_prompt_path, vec_path, manifest_path)}
log("pinned: per_prompt=%s" % pins[per_prompt_path])
log("pinned: vectors   =%s" % pins[vec_path])
log("pinned: worksheet =%s" % pins[manifest_path])

# ---------------- 7. backbone re-pin (Delta theta = 0) ----------------
h_post = state_dict_hash(model)
log("backbone LOG-331 pin (post): %s" % h_post)
if h_post != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash changed during JVPs. Quarantine. No R is read.")
    sys.exit(43)
log("backbone pin identical after all JVPs: Delta theta = 0")

# ---------------- 8. decision set, medians, verdict (Law #9: only now) ----------------
decision = [r for r in results if r["sigma1_converged"] and r["sigma2_converged"]]
n_d = len(decision)
log("decision set: %d/10 prompts (both sigma1 and sigma2 converged)" % n_d)
if n_d < 8:
    verdict = "APPARATUS-VOID"
    log("VERDICT: APPARATUS-VOID — fewer than 8/10 prompts converged. No R minted.")
    med_R = None
    med_ratio = None
else:
    Rs = sorted(r["R"] for r in decision)
    ratios = sorted(r["sigma1_over_sigma2"] for r in decision)
    if n_d % 2 == 1:
        med_R = Rs[n_d // 2]
        med_ratio = ratios[n_d // 2]
    else:
        med_R = (Rs[n_d // 2 - 1] + Rs[n_d // 2]) / 2
        med_ratio = (ratios[n_d // 2 - 1] + ratios[n_d // 2]) / 2
    log("median R = %.6f | median sigma1/sigma2 = %.6f" % (med_R, med_ratio))
    if med_R >= 3 and med_ratio >= 1.5:
        verdict = "CONTINUE"
    elif med_R >= 3 and med_ratio < 1.5:
        verdict = "KILL"
    elif 2 <= med_R < 3:
        verdict = "HELD"
    else:
        verdict = "KILL"
    log("VERDICT: %s" % verdict)

final = {
    "verdict": verdict, "n_d": n_d,
    "median_R": med_R, "median_sigma1_over_sigma2": med_ratio,
    "Rs_sorted": sorted(r["R"] for r in decision) if n_d else [],
    "ratios_sorted": sorted(r["sigma1_over_sigma2"] for r in decision) if n_d else [],
    "backbone_pin_post": h_post,
    "artifact_pins": pins,
}
with open(manifest_path, "w") as fh:
    json.dump({**manifest, "final": final}, fh, indent=1)
with open(manifest_path) as fh:
    assert json.load(fh)["final"]["verdict"] == verdict
log("worksheet finalized and re-validated")
log("== EXP127 execution complete: %s ==" % verdict)
