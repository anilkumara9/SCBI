#!/usr/bin/env python3
"""EXP129 (CLP) — Closed-Loop Adaptive Pursuit, LOG-4715 execution lane.

$0 CPU. Delta-theta = 0 by construction: pure forwards through a frozen
Pythia-410m in eval mode + exact autograd JVP/VJP sensing at frozen weights
(EXP127's Law-#14-licensed apparatus); no optimizer, no loss, no backward
pass into parameters; all parameter tensors carry requires_grad=False.

Law #9 order: guards -> backbone pin -> forward batches ->
validity-check evaluation (norm-budget audit + sensing-discipline assert +
correction-rule pin) -> backbone re-pin -> raw-record hash-pin ->
displacement metric -> decision.

Readout-site reading (documented, §3.1 ambiguity note): the pre-registration
defines x_{24,last} with a "(post-final-LayerNorm)" parenthetical but its
entire design — v1 re-pinned from EXP127's artifact, M as "the exact
L20->L24 Jacobian", the deflated power iteration on M^T M, the adjoint
correction w = M^T d1_hat / ||M^T d1_hat|| — references EXP127's propagator
(block-23 output, pre-final-LayerNorm, final token). The only internally
consistent executable reading is EXP127's map; the parenthetical is treated
as a drafting slip and this choice is disclosed for the independent review.
"""
import hashlib
import json
import math
import os
import re
import sys
import time

import numpy as np
import torch
import torch.nn.functional as F
import transformers

# ---------------- Law #13 pins ----------------
PROTOCOL = os.path.expanduser(
    "~/workspace/SCBI/research/prereg/EXP_PREREG_CLP_ADAPTIVEPURSUIT_2026-09-29.md")
PROTOCOL_PIN = "8eea9f0d659501885cbe7e30657824a372495fda9ecc130c8cc4a0cabeee5ba7"
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
V1_NPZ = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP127_tga/out/exp127_vectors.npz")
V1_NPZ_PIN = "9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc"
SNAP = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
EXP107DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl")
RUNDIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP129_clp")
OUTDIR = os.path.join(RUNDIR, "out")
os.makedirs(OUTDIR, exist_ok=True)
LOGF = open(os.path.join(OUTDIR, "exp129_console.log"), "a")
STDOUTF = open(os.path.join(OUTDIR, "exp129_stdout.log"), "a")


def log(s):
    print(s, flush=True)
    STDOUTF.write(str(s) + "\n"); STDOUTF.flush()
    LOGF.write(str(s) + "\n"); LOGF.flush()


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
log("== EXP129 (CLP) execution lane LOG-4715 ==")
h_proto = sha256_file(PROTOCOL)
log("protocol sha256: %s" % h_proto)
if h_proto != PROTOCOL_PIN:
    log("HALT: protocol hash mismatch. Tree terminates before any forward is minted.")
    sys.exit(42)
log("protocol pin OK (post-erratum LOG-4714 revision)")

# ---------------- 1. prompts ----------------
sys.path.insert(0, EXP107DIR)
from build_exp107_bench import build_bench  # noqa: E402

bench = build_bench()
assert len(bench) == 60, "EXP107 bench len != 60"
prompts = bench[:10]
prompt_ids = [b["id"] for b in prompts]
prompt_texts = [b["prompt"] for b in prompts]
pat = re.compile(r"^exp107_(flip|ctrl)_exp077_planet_2hop_[0-9]$")
assert all(pat.match(i) for i in prompt_ids), "prompt id pattern mismatch"
log("prompts: canonical-order first 10 of verbatim EXP107 bench (ids pinned)")

# ---------------- 2. environment ----------------
torch.manual_seed(20260929)
torch.set_num_threads(2)
threads = torch.get_num_threads()
assert threads == 2, "thread read-back != 2"
log("torch %s | transformers %s | numpy %s | threads=%d (read back)"
    % (torch.__version__, transformers.__version__, np.__version__, threads))
assert torch.__version__ == "2.14.0+cpu", "torch version pin"
assert transformers.__version__ == "5.17.0", "transformers version pin"
assert np.__version__ == "2.5.3", "numpy version pin"

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
    log("RUN-INVALID: backbone hash mismatch before first forward (Law #6). Quarantine. No ratio exists.")
    sys.exit(42)
log("backbone pin OK. Delta-theta guard armed.")
tokenizer = transformers.AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
cfg = model.config
H, NH, HD = cfg.hidden_size, cfg.num_attention_heads, cfg.hidden_size // cfg.num_attention_heads
assert (H, NH, HD) == (1024, 16, 64)
LN_EPS = cfg.layer_norm_eps
RND = 16
assert cfg.use_parallel_residual, "expected parallel-residual Pythia block"
layers = model.gpt_neox.layers
inv_freq = model.gpt_neox.rotary_emb.inv_freq.detach().clone()
SCALE = 1.0 / math.sqrt(HD)

# ---------------- 4. v1 re-pin (FIX-5) ----------------
h_npz = sha256_file(V1_NPZ)
log("v1 artifact sha256: %s" % h_npz)
if h_npz != V1_NPZ_PIN:
    log("apparatus-void: v1 artifact hash mismatch.")
    sys.exit(44)
npz = np.load(V1_NPZ)
missing = ["v1__" + pid for pid in prompt_ids if "v1__" + pid not in npz.files]
if missing:
    log("apparatus-void: v1 id misalignment, missing keys: %s" % missing)
    sys.exit(44)
v1 = {pid: torch.from_numpy(npz["v1__" + pid]).float() for pid in prompt_ids}
for pid in prompt_ids:
    assert v1[pid].shape == (H,) and v1[pid].dtype == torch.float32
    assert abs(float(v1[pid].norm().item()) - 1.0) < 1e-6, "v1 not unit norm"
log("v1 re-pinned: hash OK + all 10 decision-set ids aligned (v1__<prompt_id>)")

# ---------------- 5. EXP127 JVP/VJP apparatus (Law-#14-licensed) ----------------
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


def rotate_vec(r, pos):
    ang = torch.as_tensor(pos).reshape(-1, 1) * inv_freq.reshape(1, -1)
    c = torch.cat([ang.cos(), ang.cos()], dim=-1)
    s = torch.cat([ang.sin(), ang.sin()], dim=-1)
    r_rot = r[..., :RND]
    while c.dim() < r_rot.dim():
        c = c.unsqueeze(0)
        s = s.unsqueeze(0)
    r1, r2 = r_rot[..., :RND // 2], r_rot[..., RND // 2:]
    rh = torch.cat([-r2, r1], dim=-1)
    return torch.cat([r_rot * c + rh * s, r[..., RND:]], dim=-1)


def build_clamped_kv(h_base, li):
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
    """Clamped-context final-token map f: R^1024 -> R^1024 (EXP127 apparatus)."""
    def f(z):
        h = z
        for li in range(4):
            u = F.layer_norm(h, (H,), W["ln1w"][li], W["ln1b"][li], LN_EPS)
            q = torch.stack([u @ QW[li][hd].T + QB[li][hd] for hd in range(NH)])
            q = rotate_vec(q, T - 1)
            scores = (q.unsqueeze(-2) @ Kc[li].transpose(-1, -2)).squeeze(-2) * SCALE
            att = torch.softmax(scores, dim=-1)
            o = (att.unsqueeze(-2) @ Vc[li]).squeeze(-2).reshape(H)
            ao = o @ W["dense"][li].T + W["denseb"][li]
            m = F.layer_norm(h, (H,), W["ln2w"][li], W["ln2b"][li], LN_EPS)
            mo = F.gelu(m @ W["h4"][li].T + W["h4b"][li]) @ W["o4"][li].T + W["o4b"][li]
            h = h + ao + mo
        return h
    return f


SENSING_OPS_USED = []


def jvp(f, z, v):
    SENSING_OPS_USED.append("exact-jvp")
    return torch.autograd.functional.jvp(f, (z,), (v,))[1]


def vjp(f, z, w):
    SENSING_OPS_USED.append("exact-vjp")
    return torch.autograd.functional.vjp(f, (z,), (w,))[1][0]


def sensing_discipline_assert():
    """FIX-3: mechanically checkable whitelist/blacklist assert (breaking point (c))."""
    used = set(SENSING_OPS_USED)
    bad = used - {"exact-jvp", "exact-vjp"}
    assert not bad, "apparatus-void: BLACKLISTED sensing op used: %s" % sorted(bad)
    assert used, "apparatus-void: no sensing performed"
    log("sensing-discipline assert PASS: ops=%s (whitelist: exact JVP/VJP only; "
        "blacklist: finite-difference gain ratios)" % sorted(used))


def correction_rule(d1, f, z, v1_ref):
    """§3.5 frozen correction rule — the ONLY rule; identical for all items (Law #4).
    Returns (w_hat, diagnostics). No finite-difference term exists anywhere."""
    d1n = float(d1.norm().item())
    assert d1n > 0, "zero measured displacement"
    d1_hat = d1 / d1n  # WHITELISTED: finite-displacement direction as feedback input
    Mt_d1hat = vjp(f, z, d1_hat)  # exact adjoint, no linear-regime assumption
    n = float(Mt_d1hat.norm().item())
    fallback = (n == 0.0)
    w_hat = v1_ref.clone() if fallback else Mt_d1hat / n
    return w_hat, {"Mt_d1_hat_norm": n, "fallback_to_v1": fallback}


RULE_ID = id(correction_rule)

# ---------------- 6. forward machinery: hook injection at L20, capture at block 23 ----------------
CAPTURE = {}


def _capture_hook(_m, _inp, outp):
    CAPTURE["x24"] = outp[:, -1, :].detach().clone().squeeze(0)


def forward_with_injection(input_ids, delta):
    """Real frozen forward with delta added to the final token at L20
    (output of block 19). Returns x24 (block-23 output, pre-norm, final token)."""
    def inject_hook(_m, _inp, outp):
        o = outp.clone()
        o[:, -1, :] = o[:, -1, :] + delta
        return o
    h_inj = layers[19].register_forward_hook(inject_hook)
    h_cap = layers[23].register_forward_hook(_capture_hook)
    try:
        with torch.no_grad():
            out = model(input_ids=input_ids)
    finally:
        h_inj.remove()
        h_cap.remove()
    return CAPTURE["x24"].clone(), out


def base_forward(input_ids):
    """Base forward: returns (x24, hs). x24 via capture hook (same path as arms)."""
    h_cap = layers[23].register_forward_hook(_capture_hook)
    try:
        with torch.no_grad():
            out = model(input_ids=input_ids)
    finally:
        h_cap.remove()
    return CAPTURE["x24"].clone(), out.hidden_states


# ---------------- 7. base forwards + budget B ----------------
input_ids_list = [tokenizer(t, return_tensors="pt")["input_ids"] for t in prompt_texts]
base_x24, base_hs, y20_norms, f_maps, z0s = [], [], [], [], []
n_fwd = 0
for pi, pid in enumerate(prompt_ids):
    x24, hs = base_forward(input_ids_list[pi])
    n_fwd += 1
    assert len(hs) == 25
    y20 = hs[20][0, -1].detach()  # input of block 20 = output of block 19
    y20_norms.append(float(y20.norm().item()))
    base_x24.append(x24)
    base_hs.append([h.detach() for h in hs])
    T = input_ids_list[pi].shape[1]
    Kc, Vc = [], []
    for li in range(4):
        K, V = build_clamped_kv(hs[20 + li][0].detach(), li)
        Kc.append(K); Vc.append(V)
    f_maps.append(make_f(Kc, Vc, T))
    z0s.append(y20.clone())
    # sanity: clamped map reproduces the real block-23 output at the base point
    with torch.no_grad():
        fz0 = f_maps[-1](z0s[-1])
    san = float((fz0 - x24).abs().max().item())
    log("base %d/%d %s: T=%d ||y20||=%.4f sanity max|f(z0)-x24|=%.3e"
        % (pi + 1, len(prompt_ids), pid, T, y20_norms[-1], san))

B = 0.01 * float(np.median(np.array(y20_norms)))
assert B > 0 and math.isfinite(B)
log("budget B = 0.01 * median||y20|| = %.8f  (recorded BEFORE first perturbed forward)" % B)

# ---------------- 8. v2 derivation (LOG-4714 erratum) ----------------
K_V2 = 40  # fixed iteration count, same for every prompt, recorded
gen_v2 = torch.Generator()
gen_v2.manual_seed(20260929_4714)
v2 = {}
for pi, pid in enumerate(prompt_ids):
    f, z0 = f_maps[pi], z0s[pi]
    z = z0.clone().requires_grad_(True)
    q = torch.randn(H, generator=gen_v2)
    q = q - (v1[pid] @ q) * v1[pid]
    q = q / q.norm()
    for _ in range(K_V2):
        w = jvp(f, z, q)
        t = vjp(f, z, w)
        t = t - (v1[pid] @ t) * v1[pid]
        tq = t.norm()
        assert float(tq.item()) > 0, "deflated iteration collapsed"
        q = t / tq
    v2i = q.detach()
    ortho = abs(float((v2i @ v1[pid]).item()))
    log("v2 %d/%d %s: K=%d |v2|=%.6f |v2.v1|=%.3e %s"
        % (pi + 1, len(prompt_ids), pid, K_V2, v2i.norm().item(), ortho,
           "OK" if ortho < 1e-6 else "FAIL"))
    if ortho >= 1e-6:
        log("apparatus-void: v2 orthogonality assert failed.")
        sys.exit(44)
    v2[pid] = v2i
log("v2 derived for all 10 prompts (seed 20260929_4714, K=%d, exact JVP/VJP)" % K_V2)

# ---------------- 9. arms (Law #9: forward batches) ----------------
TOL = 1e-5  # float32 component-structure tolerance (relative)
items = []
vec_store = {}
for pi, pid in enumerate(prompt_ids):
    t0 = time.time()
    f, z0 = f_maps[pi], z0s[pi]
    v1i, v2i = v1[pid], v2[pid]
    xb = base_x24[pi]
    delta1 = (B / 2) * v1i
    # --- loop arm, forward 1: sense ---
    x1, _ = forward_with_injection(input_ids_list[pi], delta1)
    n_fwd += 1
    d1 = (x1 - xb)
    assert float(d1.norm().item()) > 1e-12, "zero first-push displacement"
    # --- frozen correction rule (exact adjoint sensing) ---
    z = z0.clone().requires_grad_(True)
    w_hat, diag = correction_rule(d1, f, z, v1i)
    assert id(correction_rule) == RULE_ID, "correction rule identity changed"
    c = (B / 2) * w_hat
    # --- loop arm, forward 2: act (from the unperturbed base) ---
    delta2 = delta1 + c
    x2, _ = forward_with_injection(input_ids_list[pi], delta2)
    n_fwd += 1
    d2 = (x2 - xb)
    # --- open-loop sum arm ---
    delta_open = (B / 2) * v2i
    xs, _ = forward_with_injection(input_ids_list[pi], delta1 + delta_open)
    n_fwd += 1
    d_sum = (xs - xb)
    # --- single-shot arm ---
    delta_single = B * v1i
    xg, _ = forward_with_injection(input_ids_list[pi], delta_single)
    n_fwd += 1
    d_single = (xg - xb)
    # --- component norm audit (breaking point (b), FIX-4) ---
    aud = {
        "norm_delta1": float(delta1.norm().item()),
        "norm_c": float(c.norm().item()),
        "norm_delta_open": float(delta_open.norm().item()),
        "norm_delta_single": float(delta_single.norm().item()),
        "norm_delta2_injected": float(delta2.norm().item()),
        "norm_delta1_plus_open": float((delta1 + delta_open).norm().item()),
    }
    for key, target in (("norm_delta1", B / 2), ("norm_c", B / 2),
                        ("norm_delta_open", B / 2), ("norm_delta_single", B)):
        rel = abs(aud[key] - target) / target
        if rel > TOL:
            log("apparatus-void: component %s = %.8f vs target %.8f (rel %.3e > tol)"
                % (key, aud[key], target, rel))
            sys.exit(44)
    # triangle-inequality observation: the loop can never win on dose
    if aud["norm_delta2_injected"] > B * (1 + TOL):
        log("apparatus-void: injected loop norm exceeds budget B.")
        sys.exit(44)
    n1, n2, ns, ng = (float(d1.norm().item()), float(d2.norm().item()),
                      float(d_sum.norm().item()), float(d_single.norm().item()))
    assert ns > 1e-12 and ng > 1e-12, "zero open-loop displacement"
    r_i = n2 / max(ns, ng)
    sat_i = float(((d2 - d1).norm() / d1.norm()).item())
    dose_i = n2 / ns
    beat_single_i = n2 / ng
    items.append({
        "prompt_id": pid, "T": int(input_ids_list[pi].shape[1]),
        "norm_d1": n1, "norm_d2": n2, "norm_d_sum": ns, "norm_d_single": ng,
        "r": r_i, "saturation": sat_i, "dose_ratio": dose_i,
        "loop_beats_single": beat_single_i,
        "norm_audit": aud, "adjoint": diag, "rule_id_ok": True,
        "seconds": time.time() - t0,
    })
    for nm, vec in (("delta1", delta1), ("c", c), ("delta2", delta2),
                    ("delta_open", delta_open), ("delta_single", delta_single),
                    ("d1", d1), ("d2", d2), ("d_sum", d_sum), ("d_single", d_single)):
        vec_store["%s__%s" % (nm, pid)] = vec.detach().numpy().astype(np.float32)
    log("item %d/%d %s: ||d1||=%.4f ||d2||=%.4f ||d_sum||=%.4f ||d_single||=%.4f "
        "r=%.4f sat=%.4f dose=%.4f beat1=%.4f (%.1fs)"
        % (pi + 1, len(prompt_ids), pid, n1, n2, ns, ng, r_i, sat_i, dose_i,
           beat_single_i, time.time() - t0))
log("forward batches DONE: %d forwards (10 base + 40 arm)" % n_fwd)
assert n_fwd == 50, "forward count != 50 (protocol: 10x5)"

# ---------------- 10. validity-check evaluation ----------------
sensing_discipline_assert()  # breaking point (c), FIX-3
log("correction-rule pin PASS: single frozen §3.5 rule for all 10 items (breaking point (d))")

# ---------------- 11. backbone re-pin (Delta theta = 0) ----------------
h_post = state_dict_hash(model)
log("backbone LOG-331 pin (post): %s" % h_post)
if h_post != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash changed during execution. Quarantine. No ratio is read.")
    sys.exit(43)
log("backbone pin identical after all forwards/JVPs: Delta theta = 0")

# ---------------- 12. raw-record hash-pin BEFORE any decision (Law #9, §3.8) ----------------
per_item_path = os.path.join(OUTDIR, "exp129_per_item.json")
with open(per_item_path, "w") as fh:
    json.dump(items, fh, indent=1)
vec_path = os.path.join(OUTDIR, "exp129_vectors.npz")
np.savez_compressed(vec_path,
                    **{"v1__" + pid: v1[pid].detach().numpy().astype(np.float32)
                       for pid in prompt_ids},
                    **{"v2__" + pid: v2[pid].detach().numpy().astype(np.float32)
                       for pid in prompt_ids},
                    **vec_store)
manifest = {
    "experiment": "EXP129_CLP", "log": "LOG-4715",
    "protocol_sha256": PROTOCOL_PIN,
    "weights_snap": SNAP,
    "backbone_pin_pre": h_pre, "backbone_pin_post": h_post,
    "v1_artifact_sha256": h_npz,
    "v2_derivation": {"seed": 20260929_4714, "K": K_V2,
                      "recurrence": "q_{k+1} ~ (I - v1 v1^T) M^T M q_k",
                      "orthogonality_assert": "|v2.v1| < 1e-6"},
    "prompt_ids": prompt_ids,
    "budget_B": B, "budget_rule": "B = 0.01 * median||y20_last||",
    "y20_norms": y20_norms,
    "component_tolerance_rel": TOL,
    "sensing_ops": sorted(set(SENSING_OPS_USED)),
    "correction_rule": "w_hat = M^T d1_hat / ||M^T d1_hat|| (frozen, identical all items)",
    "readout_site": "block-23 output (pre-final-LayerNorm), final token "
                    "(EXP127 propagator map; §3.1 parenthetical disclosed in report)",
    "flips_observation": "not measured — no licensed decision-readout channel "
                         "(logits barred §6; generation/probe/head barred §3.7)",
    "env": {"torch": torch.__version__, "transformers": transformers.__version__,
            "numpy": np.__version__, "threads": threads, "dtype": "float32",
            "device": "cpu", "model": "pythia-410m-local"},
    "forwards": n_fwd,
}
manifest_path = os.path.join(OUTDIR, "exp129_worksheet.json")
with open(manifest_path, "w") as fh:
    json.dump(manifest, fh, indent=1)
with open(manifest_path) as fh:
    assert json.load(fh)["backbone_pin_pre"] == h_pre
console_path = os.path.join(OUTDIR, "exp129_console.log")
LOGF.flush()
pins = {p: sha256_file(p) for p in (per_item_path, vec_path, manifest_path, console_path)}
log("hash-pinned (before any decision statistic exists):")
for k, v in pins.items():
    log("  %s -> %s" % (os.path.basename(k), v))

# ---------------- 13. displacement metric + decision (FIX-1 precedence) ----------------
def med(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2

med_r = med([it["r"] for it in items])
med_sat = med([it["saturation"] for it in items])
med_dose = med([it["dose_ratio"] for it in items])
med_beat1 = med([it["loop_beats_single"] for it in items])
log("median r = %.6f | median saturation = %.6f | median dose = %.6f | "
    "median loop/single = %.6f" % (med_r, med_sat, med_dose, med_beat1))

if med_sat <= 0.1:
    verdict = "KILL"
    reason = ("saturation KILL (premise branch, evaluated first): median "
              "||d2-d1||/||d1|| = %.6f <= 0.1 — the correction buys no "
              "displacement regardless of rule" % med_sat)
elif med_dose <= 1.2 and med_beat1 > 1.2:
    verdict = "KILL"
    reason = ("dose-in-disguise KILL (premise branch, evaluated first): median "
              "||d2||/||d_sum|| = %.6f <= 1.2 while the loop beats the single "
              "shot (%.4f > 1.2) — the 'feedback' was a second push" % (med_dose, med_beat1))
elif med_r >= 2:
    verdict = "CONTINUE"
    reason = ("median r = %.6f >= 2 — feedback has causal value per unit norm; "
              "the $0 gate for the GPU closed-loop line passes" % med_r)
elif med_r <= 1.2:
    verdict = "KILL"
    reason = ("median r = %.6f <= 1.2 — the loop adds nothing the push didn't "
              "already do; the adaptive-pursuit premise on $0 is dead" % med_r)
else:
    verdict = "HELD"
    reason = ("median r = %.6f in (1.2, 2) — recorded, no re-test without a "
              "new gate" % med_r)
log("VERDICT: %s — %s" % (verdict, reason))

final = {
    "verdict": verdict, "reason": reason,
    "median_r": med_r, "median_saturation": med_sat,
    "median_dose_ratio": med_dose, "median_loop_beats_single": med_beat1,
    "r_sorted": sorted(it["r"] for it in items),
    "saturation_sorted": sorted(it["saturation"] for it in items),
    "dose_sorted": sorted(it["dose_ratio"] for it in items),
    "backbone_pin_post": h_post,
    "artifact_pins": pins,
}
with open(manifest_path, "w") as fh:
    json.dump({**manifest, "final": final}, fh, indent=1)
with open(manifest_path) as fh:
    assert json.load(fh)["final"]["verdict"] == verdict
log("worksheet finalized and re-validated")
log("== EXP129 execution complete: %s ==" % verdict)
LOGF.close(); STDOUTF.close()
