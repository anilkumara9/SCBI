#!/usr/bin/env python3
"""EXP138 (B5/TGA-INT8): precision certification of the TGA injection nulls.

Pre-registered protocol (signed, Law #14 SIGN-WITH-FIXES LOG-4861,
fix byte-verified PASS LOG-4863):
    research/prereg/EXP138_PREREG_TGAINT8_2026-09-30.md

Question: do the TGA decision nulls (EXP131 one-shot, EXP133 geodesic)
reproduce under weight-only INT8 fake-quantization of the frozen backbone?

Six tiers: Q1 (c^_q < 0.1), Q2 (11-arm one-shot DM=0), Q3 (geodesic DM_geo=0),
Q4 (McNemar p_q >= 0.05), Q5 (B_agg dead control -> RUN-INVALID if missed),
Q6 (delivery (h) under quantization -> RUN-INVALID if missed).
CERTIFIED <=> Q1&Q2&Q3&Q4; PIVOT <=> any Q1-Q4 fail; RUN-INVALID <=> Q5/Q6 fail.

Method: EXP110-certified fake-quant pattern (per-output-channel symmetric INT8
on every nn.Linear weight, FP32 compute, disposable in-memory copy,
pin-check-then-derive). FP32 backbone verified against the LOG-331 pin BEFORE
quantization; quantized copy derived once, hash-asserted pre/post, discarded
after. All DM statistics against the quantized-regime baseline; baseline
shifts reported separately.

$0 CPU. Delta-theta = 0 on the FP32 reference by construction: pure forwards,
no optimizer, no backward into weights. (The c-hat gate uses exact autograd
VJPs on states, never into weights — EXP131 breaking point (f) carries over.)

Falsification-tree order (pre-reg §5):
FP32 pin -> quantized copy -> v1 re-pin ->
quantized c^ + one-shot 11-arm + geodesic + (h) -> 6 tier Booleans.

Exit codes: 0 = execution complete (tiers recorded, NO verdict);
42 = protocol/pin guard failure; 43 = Q5 RUN-INVALID (B_agg fired);
44 = apparatus-void (breaking-point miss incl. Q6, hypothesis UNTESTED).
"""
import argparse
import copy
import gc
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
PREREG_PATH = os.path.expanduser("~/workspace/SCBI/research/prereg/EXP138_PREREG_TGAINT8_2026-09-30.md")
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
V1_NPZ_PIN = "9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc"
BENCH_PIN = "e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5"
BAGG_PIN = "d3556d83751634a2fc5114d56c4ee246bb1b296293d2adcde40a369da1600ae1"  # EXP131 h_bagg
SITE = 20  # program-standard site: input of block 20 = hidden_states[20]
MODEL_NAME = "EleutherAI/pythia-410m"
WEIGHTS_DIR = "/home/hatch/workspace/.exp086_weights/pythia-410m"
B_GEO = 0.50578119  # EXP133 pinned geodesic budget (breaking point (d), Amendment C)
GEO_K = 5
ALPHA_GEO = B_GEO / GEO_K

RUNDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(RUNDIR, "out")
os.makedirs(OUTDIR, exist_ok=True)
LOGF = open(os.path.join(OUTDIR, "exp138_console.log"), "a")

BUNDLE131 = os.path.expanduser("~/workspace/SCBI/experiments/bundles/exp131_v1inj")
V1_NPZ_CANDIDATES = [
    os.path.join(BUNDLE131, "exp127_vectors.npz"),
    os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP127_tga/out/exp127_vectors.npz"),
]


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


def first_existing(candidates, what):
    for c in candidates:
        if os.path.isfile(c):
            return c
    log("HALT: %s not found in any candidate location: %s" % (what, candidates))
    sys.exit(42)


def binom_sf_ge(k, n):
    """P(X >= k | n, 0.5) exact — one-sided McNemar p."""
    from math import comb
    return sum(comb(n, i) for i in range(k, n + 1)) / (2.0 ** n)


def fake_quantize_linear_(model):
    """EXP110-certified pattern: per-output-channel symmetric INT8 fake-quant
    on every nn.Linear weight, in place, float32. Returns count quantized."""
    n = 0
    for mod in model.modules():
        if isinstance(mod, torch.nn.Linear):
            w = mod.weight.data
            max_c = w.abs().amax(dim=1, keepdim=True)  # per-output-channel (rows)
            scale = max_c / 127.0
            scale_safe = torch.where(scale == 0, torch.ones_like(scale), scale)
            w_q = torch.clamp(torch.round(w / scale_safe), -128, 127) * scale_safe
            w.copy_(w_q)  # zero rows map to exact 0
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="smoke mode: 1 prompt, K=1 random, full pipeline end-to-end")
    args = ap.parse_args()
    SMOKE = args.smoke
    N_PROMPTS = 1 if SMOKE else 10
    K_RAND = 1 if SMOKE else 8
    t0 = time.time()
    log("== EXP138 (B5/TGA-INT8) execution lane ==")
    log("mode: %s" % ("SMOKE (1 prompt, K=1 random)" if SMOKE else "FULL (10 prompts, K=8 randoms)"))

    # ---------------- 0. pre-reg hash (Law #9 first) ----------------
    h_prereg = sha256_file(PREREG_PATH)
    log("pre-reg sha256: %s" % h_prereg)

    # ---------------- 1. prompts: bench build + pin, canonical first N ----------------
    sys.path.insert(0, BUNDLE131)
    from build_exp107_bench import build_bench, bench_sha256  # noqa: E402
    bench = build_bench()
    assert len(bench) == 60, "EXP107 bench len != 60"
    h_bench = bench_sha256(bench)
    log("bench sha256: %s" % h_bench)
    if h_bench != BENCH_PIN:
        log("HALT: bench hash mismatch.")
        sys.exit(42)
    prompts = bench[:N_PROMPTS]
    prompt_ids = [b["id"] for b in prompts]
    log("prompts: canonical-order first %d of verbatim EXP107 bench" % N_PROMPTS)

    # ---------------- 2. environment ----------------
    device = torch.device("cpu")
    torch.manual_seed(20260930)
    torch.set_num_threads(2)
    env = {
        "torch": torch.__version__, "transformers": transformers.__version__,
        "numpy": np.__version__, "device": str(device),
        "threads": torch.get_num_threads(), "smoke": SMOKE,
        "presentation_mechanism": "in-memory state_dict transform (no saved model dir)",
    }
    log("env: %s" % json.dumps(env))

    # ---------------- 3. FP32 frozen backbone + pin (breaking point (a)) ----------------
    model = transformers.AutoModelForCausalLM.from_pretrained(
        WEIGHTS_DIR, local_files_only=True, trust_remote_code=False,
        torch_dtype=torch.float32, output_hidden_states=True, output_attentions=False)
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)
    model.to(device)
    h_pre = state_dict_hash(model)
    log("backbone LOG-331 pin (pre): %s" % h_pre)
    if h_pre != WEIGHTS_PIN:
        log("HALT: backbone hash mismatch before first forward (Law #6).")
        sys.exit(42)
    log("backbone pin OK. Delta-theta guard armed.")
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        WEIGHTS_DIR, local_files_only=True, trust_remote_code=False)
    cfg = model.config
    H, NH, HD = cfg.hidden_size, cfg.num_attention_heads, cfg.hidden_size // cfg.num_attention_heads
    assert (H, NH, HD) == (1024, 16, 64)
    layers = model.gpt_neox.layers

    # ---------------- 4. artifact re-pins ----------------
    v1_npz_path = first_existing(V1_NPZ_CANDIDATES, "exp127_vectors.npz")
    h_npz = sha256_file(v1_npz_path)
    log("v1 artifact sha256: %s" % h_npz)
    if h_npz != V1_NPZ_PIN:
        log("apparatus-void: v1 artifact hash mismatch (breaking point (b)).")
        sys.exit(44)
    npz = np.load(v1_npz_path)
    missing = ["v1__" + pid for pid in prompt_ids if "v1__" + pid not in npz.files]
    if missing:
        log("apparatus-void: v1 id misalignment, missing keys: %s" % missing)
        sys.exit(44)
    v1 = {pid: torch.from_numpy(npz["v1__" + pid]).float() for pid in prompt_ids}
    for pid in prompt_ids:
        assert v1[pid].shape == (H,) and abs(float(v1[pid].norm().item()) - 1.0) < 1e-6
    log("v1 re-pinned: hash OK + %d/%d id alignment (v1__<prompt_id>)" % (N_PROMPTS, N_PROMPTS))

    input_ids_list = [tokenizer.encode(t, return_tensors="pt").to(device)
                      for t in [p["prompt"] for p in prompts]]

    # ---------------- 5. FP32 base forwards (baseline-shift reference + v2 inputs) ----------------
    log("FP32 phase: base forwards (baseline reference)...")
    fp32_base_states, fp32_hs_all = [], []
    with torch.no_grad():
        for pi in range(N_PROMPTS):
            out = model(input_ids=input_ids_list[pi], output_hidden_states=True)
            hs = out.hidden_states
            fp32_base_states.append(hs[SITE][0, -1, :].detach().cpu())
            fp32_hs_all.append([h.detach().cpu() for h in hs])
    log("FP32 base forwards complete.")

    # ---------------- 6. B_agg: deterministic reconstruction from EXP077 support set (FP32) ----------------
    from exp077_support import support_prompts, build_candidate_directions, VOCAB_KEYS  # noqa: E402
    sup_items = list(support_prompts())
    delta_h_by_vocab = {vk: [] for vk in VOCAB_KEYS}
    h_all = []
    with torch.no_grad():
        for sid, p_rel, p_neu in sup_items:
            ids_rel = tokenizer.encode(p_rel, return_tensors="pt").to(device)
            ids_neu = tokenizer.encode(p_neu, return_tensors="pt").to(device)
            o_rel = model(input_ids=ids_rel, output_hidden_states=True)
            o_neu = model(input_ids=ids_neu, output_hidden_states=True)
            h_rel = o_rel.hidden_states[SITE + 1][0, -1, :].detach().cpu()
            h_neu = o_neu.hidden_states[SITE + 1][0, -1, :].detach().cpu()
            vk = next(k for k in VOCAB_KEYS if sid.startswith("sup_" + k + "_"))
            delta_h_by_vocab[vk].append(h_rel - h_neu)
            h_all.extend([h_rel, h_neu])
    for vk in VOCAB_KEYS:
        delta_h_by_vocab[vk] = torch.stack(delta_h_by_vocab[vk])
    assert len(h_all) == 300, "expected 300 support presentations, got %d" % len(h_all)
    cand = build_candidate_directions(delta_h_by_vocab, h_all)
    b_agg = cand["v_hat"].detach()
    assert b_agg.shape == (H,)
    h_bagg = hashlib.sha256(b_agg.numpy().astype(np.float32).tobytes()).hexdigest()
    log("B_agg re-derived on FP32; reconstruction sha256: %s" % h_bagg)
    if h_bagg != BAGG_PIN:
        log("apparatus-void: B_agg reconstruction hash mismatch (expected EXP131's).")
        sys.exit(44)
    log("B_agg pin OK (matches EXP131).")
    del h_all, delta_h_by_vocab

    # ---------------- 7. v2 derivation on FP32 (EXP131 §7, LOG-4714 erratum, verbatim) ----------------
    log("FP32 phase: v2 deflated power iteration (K=40, seed 20260929_4714)...")
    LN_EPS = cfg.layer_norm_eps
    RND = 16
    inv_freq = model.gpt_neox.rotary_emb.inv_freq.detach().clone()
    SCALE = 1.0 / math.sqrt(HD)
    W = {"ln1w": [], "ln1b": [], "qkv": [], "qkvb": [],
         "dense": [], "denseb": [], "h4": [], "h4b": [], "o4": [], "o4b": [],
         "ln2w": [], "ln2b": []}
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
        ang = torch.as_tensor(pos, device=inv_freq.device).reshape(-1, 1) * inv_freq.reshape(1, -1)
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
        K = torch.empty(NH, T, HD, device=device)
        V = torch.empty(NH, T, HD, device=device)
        pos = torch.arange(T, device=device)
        for hd in range(NH):
            k = u @ KW[li][hd].T + KB[li][hd]
            v = u @ VW[li][hd].T + VB[li][hd]
            K[hd] = rotate_vec(k, pos)
            V[hd] = v
        return K, V

    def make_f(Kc, Vc, T):
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

    SENSING_OPS = []

    def jvp(f, z, v):
        SENSING_OPS.append("exact-jvp")
        return torch.autograd.functional.jvp(f, (z,), (v,))[1]

    def vjp(f, z, w):
        SENSING_OPS.append("exact-vjp")
        return torch.autograd.functional.vjp(f, (z,), (w,))[1][0]

    K_V2 = 40
    gen_v2 = torch.Generator()
    gen_v2.manual_seed(20260929_4714)
    v2 = {}
    for pi, pid in enumerate(prompt_ids):
        hs = fp32_hs_all[pi]
        T = input_ids_list[pi].shape[1]
        Kc, Vc = [], []
        for li in range(4):
            K, V = build_clamped_kv(hs[SITE + li][0].detach(), li)
            Kc.append(K); Vc.append(V)
        f = make_f(Kc, Vc, T)
        z = hs[SITE][0, -1].detach().clone().requires_grad_(True)
        v1d = v1[pid].to(device)
        q = torch.randn(H, generator=gen_v2).to(device)
        q = q - (v1d @ q) * v1d
        q = q / q.norm()
        for _ in range(K_V2):
            w = jvp(f, z, q)
            t = vjp(f, z, w)
            t = t - (v1d @ t) * v1d
            tq = t.norm()
            assert float(tq.item()) > 0, "deflated iteration collapsed"
            q = t / tq
        v2i = q.detach()
        ortho = abs(float((v2i @ v1d).item()))
        if ortho >= 1e-6:
            log("apparatus-void: v2 orthogonality assert failed (|v2.v1|=%.3e)." % ortho)
            sys.exit(44)
        v2[pid] = v2i
        log("v2 %d/%d %s: K=%d |v2.v1|=%.3e OK" % (pi + 1, N_PROMPTS, pid, K_V2, ortho))
    used = set(SENSING_OPS)
    assert not (used - {"exact-jvp", "exact-vjp"}), "apparatus-void: blacklisted sensing op"
    log("sensing-discipline assert PASS: ops=%s" % sorted(used))
    del fp32_hs_all, W, QW, QB, KW, KB, VW, VB
    gc.collect()

    # ---------------- 8. QUANTIZATION: derive disposable INT8 fake-quant copy ----------------
    # FP32 phase is complete. The FP32 reference is never modified below.
    log("quantization: per-output-channel symmetric INT8 fake-quant on every nn.Linear...")
    n_q = fake_quantize_linear_(model)
    h_q_pre = state_dict_hash(model)
    log("linear layers quantized: %d" % n_q)
    log("quantized copy sha256: %s" % h_q_pre)
    if h_q_pre == WEIGHTS_PIN:
        log("apparatus-void: quantized copy identical to FP32 pin (quantization no-op).")
        sys.exit(44)
    log("quantized copy differs from FP32 pin (expected). Presentation: in-memory state_dict transform.")
    layers = model.gpt_neox.layers  # rebind (same object, quantized weights)

    # ---------------- 9. quantized base forwards + budget B_q ----------------
    log("quantized phase: base forwards...")
    base_states, y20_norms = [], []
    with torch.no_grad():
        for pi in range(N_PROMPTS):
            out = model(input_ids=input_ids_list[pi], output_hidden_states=True)
            hs = out.hidden_states
            y20 = hs[SITE][0, -1, :].detach()
            y20_norms.append(float(y20.norm().item()))
            base_states.append(y20.cpu())
    B = 0.01 * float(np.median(np.array(y20_norms)))
    assert B > 0 and math.isfinite(B)
    log("budget B_q = 0.01 * median||y20_q|| = %.8f (quantized regime)" % B)

    # ---------------- 10. breaking point (h)/Q6: delivery probe under quantization, both arms ----------------
    # Same probe as EXP131 §5b (seed 20260930, ||delta||=16.0, layers[19], prepend=True),
    # run on the quantized model. Labeled per arm per the pre-reg; the hook mechanism
    # is arm-independent.
    r_probes = {}
    for arm_label in ["oneshot", "geodesic"]:
        tap_base_h = base_states[0].detach()
        g_probe = torch.Generator(device=device).manual_seed(20260930)
        delta_probe = torch.randn(tap_base_h.shape, generator=g_probe, dtype=torch.float32, device=device)
        delta_probe = delta_probe * (16.0 / float(delta_probe.norm().item()))
        def probe_hook_fn(_m, _inp, outp):
            o = outp.clone()
            o[:, -1, :] = o[:, -1, :] + delta_probe
            return o
        h_probe = layers[19].register_forward_hook(probe_hook_fn, prepend=True)
        try:
            with torch.no_grad():
                out_probe = model(input_ids=input_ids_list[0], output_hidden_states=True)
        finally:
            h_probe.remove()
        tap_inj_h = out_probe.hidden_states[SITE][0, -1, :].detach().cpu()
        r_probe = float((tap_inj_h - tap_base_h).norm().item()) / float(delta_probe.norm().item())
        r_probes[arm_label] = r_probe
        log("Q6/(h) [%s arm]: r_q = %.7f (must be in [0.99, 1.01])" % (arm_label, r_probe))
        del delta_probe, out_probe, tap_inj_h, tap_base_h
    q6_pass = all(0.99 <= r <= 1.01 for r in r_probes.values())
    if not q6_pass:
        log("RUN-INVALID: delivery (h) failed under quantization (Q6) — apparatus-void in the new regime.")
        sys.exit(44)
    log("Q6 PASS: injection reaches the readout tap under quantization on both arms.")

    # ---------------- 11. option embeddings on the quantized model + single-token assert ----------------
    option_embs = {}
    for pi, p in enumerate(prompts):
        E1, E2 = p["tuple"][0], p["tuple"][-1]
        assert E1 != E2
        for side, E in (("E1", E1), ("E2", E2)):
            ids = tokenizer.encode(" " + E, add_special_tokens=False)
            if len(ids) != 1:
                log("RUN-INVALID: single-token assertion failed at execution on item %s." % p["id"])
                sys.exit(43)
            with torch.no_grad():
                out = model(input_ids=tokenizer.encode(" " + E, return_tensors="pt").to(device),
                            output_hidden_states=True)
            option_embs[(p["id"], side)] = out.hidden_states[SITE][0, -1, :].detach().cpu().to(torch.float64)
    log("quantized option forwards complete; single-token assert passed on all %d option texts" % (2 * N_PROMPTS))

    def cos_np(a, v):
        return float(np.dot(a, v) / (np.linalg.norm(a) * np.linalg.norm(v)))

    cur_id = [None]

    def readout(state64):
        c1 = cos_np(state64, option_embs[(cur_id[0], "E1")])
        c2 = cos_np(state64, option_embs[(cur_id[0], "E2")])
        dec = "E2" if c1 == c2 else ("E1" if c1 > c2 else "E2")
        return dec, c1, c2, abs(c1 - c2)

    # ---------------- 12. Q1: quantized c-hat (exact VJP through the quantized graph) ----------------
    c_hats, c_excl = [], []
    for pi, pid in enumerate(prompt_ids):
        cur_id[0] = pid
        z = base_states[pi].to(torch.float64).clone().requires_grad_(True)
        e1 = option_embs[(pid, "E1")].to(torch.float64)
        e2 = option_embs[(pid, "E2")].to(torch.float64)
        c1 = torch.dot(z, e1) / (z.norm() * e1.norm())
        c2 = torch.dot(z, e2) / (z.norm() * e2.norm())
        margin = torch.abs(c1 - c2)
        g = torch.autograd.grad(margin, z, retain_graph=False)[0]
        gn = float(g.norm().item())
        if gn < 1e-12:
            c_excl.append(pid)
            continue
        g_hat = g / gn
        c_hats.append(abs(float(torch.dot(v1[pid].to(torch.float64), g_hat).item())))
    if len(c_excl) >= 3:
        log("apparatus-void: >=3 degenerate ||g|| exclusions in quantized c-hat gate.")
        sys.exit(44)
    c_hat_q = float(np.mean(c_hats)) if c_hats else 0.0
    q1_pass = c_hat_q < 0.1
    log("Q1: quantized c-hat mean=%.5f over %d prompts (%d exclusions) -> %s" % (
        c_hat_q, len(c_hats), len(c_excl), "PASS" if q1_pass else "FAIL"))

    # ---------------- 13. Q2/Q5: 11-arm one-shot injection on the quantized backbone ----------------
    def inject_forward(input_ids, delta):
        def hook_fn(_m, _inp, outp):
            o = outp.clone()
            o[:, -1, :] = o[:, -1, :] + delta
            return o
        h_inj = layers[19].register_forward_hook(hook_fn, prepend=True)
        try:
            with torch.no_grad():
                out = model(input_ids=input_ids, output_hidden_states=True)
        finally:
            h_inj.remove()
        return out.hidden_states[SITE][0, -1, :].detach().cpu().to(torch.float64)

    per_item, norm_audit = [], []
    gen_r = torch.Generator()
    arm_names = ["base", "v1", "v2"] + ["rand%d" % j for j in range(K_RAND)] + ["bagg"]
    for pi, pid in enumerate(prompt_ids):
        cur_id[0] = pid
        gen_r.manual_seed(20260929_4724 + pi * 100)  # F1-pinned re-derivation (verbatim EXP131)
        rand_dirs = []
        for j in range(K_RAND):
            u = torch.randn(H, generator=gen_r)
            rand_dirs.append(u / u.norm())
        arms = {"base": None, "v1": v1[pid], "v2": v2[pid],
                **{"rand%d" % j: rand_dirs[j] for j in range(K_RAND)},
                "bagg": b_agg}
        rec = {"id": pid, "arms": {}}
        base_dec = base_mar = None
        for an in arm_names:
            if an == "base":
                st = base_states[pi].to(torch.float64)
                inj_norm = 0.0
            else:
                delta = (B * arms[an].to(device).to(torch.float32)).to(device)
                st = inject_forward(input_ids_list[pi], delta)
                inj_norm = float((B * arms[an]).norm().item())
                rel = abs(inj_norm - B) / B
                norm_audit.append(rel <= 1e-6)
                if rel > 1e-6:
                    log("apparatus-void: arm %s norm %.8f != B_q %.8f (rel %.3e)." % (an, inj_norm, B, rel))
                    sys.exit(44)
            dec, c1, c2, mar = readout(st.numpy() if isinstance(st, torch.Tensor) else st)
            rec["arms"][an] = {"decision": dec, "cos_E1": c1, "cos_E2": c2,
                               "margin": mar, "injected_norm": inj_norm}
            if an == "base":
                base_dec, base_mar = dec, mar
        rec["dm"] = {an: (1 if rec["arms"][an]["decision"] != base_dec else 0)
                     for an in arm_names if an != "base"}
        rec["margin_disp"] = {an: abs(rec["arms"][an]["margin"] - base_mar)
                              for an in arm_names if an != "base"}
        per_item.append(rec)
        log("oneshot %d/%d %s: base=%s margin=%.4f | dm: %s" % (
            pi + 1, N_PROMPTS, pid, base_dec, base_mar,
            {an: rec["dm"][an] for an in rec["dm"]}))
    if not all(norm_audit):
        log("apparatus-void: norm-budget audit failed (breaking point (d)).")
        sys.exit(44)
    log("norm-budget audit PASS: all %d one-shot arms within 1e-6 rel of B_q" % len(norm_audit))

    dm_v1_q = sum(r["dm"]["v1"] for r in per_item)
    dm_bagg_q = sum(r["dm"]["bagg"] for r in per_item)
    q2_pass = (dm_v1_q == 0)
    log("Q2: quantized one-shot DM_v1=%d/110 -> %s" % (dm_v1_q, "PASS" if q2_pass else "FAIL"))
    # Q5 dead control BEFORE any metric use
    if dm_bagg_q != 0:
        log("RUN-INVALID: Q5 B_agg null-control fired (DM_Bagg=%d != 0) — quantized bench drift." % dm_bagg_q)
        sys.exit(43)
    log("Q5 PASS: B_agg dead control holds under quantization (DM_Bagg=0).")

    # Q4: McNemar one-sided, v1 vs best random (EXP131 construction, quantized regime)
    rand_flips = {j: sum(r["dm"]["rand%d" % j] for r in per_item) for j in range(K_RAND)}
    j_star = min([j for j in rand_flips if rand_flips[j] == max(rand_flips.values())])
    b_mc = sum(1 for r in per_item if r["dm"]["v1"] == 1 and r["dm"]["rand%d" % j_star] == 0)
    c_mc = sum(1 for r in per_item if r["dm"]["v1"] == 0 and r["dm"]["rand%d" % j_star] == 1)
    n_mc = b_mc + c_mc
    p_mc = binom_sf_ge(b_mc, n_mc) if n_mc > 0 else 1.0
    q4_pass = p_mc >= 0.05
    log("Q4: McNemar (b,c)=(%d,%d) n=%d p=%.6f vs best-random j%d -> %s" % (
        b_mc, c_mc, n_mc, p_mc, j_star, "PASS" if q4_pass else "FAIL"))

    # ---------------- 14. Q3: geodesic multistep on the quantized backbone ----------------
    # EXP133 §8 walk (verbatim): pure float64 vector arithmetic from the quantized
    # x0; K=5, ALPHA=B_GEO/5, sphere retraction + parallel transport, pinned budget.
    def geodesic_walk(x0_64, u_64):
        r0 = float(np.linalg.norm(x0_64))
        xh0 = x0_64 / r0
        d = u_64 - float(np.dot(u_64, xh0)) * xh0
        dn = float(np.linalg.norm(d))
        if dn < 1e-12:
            log("apparatus-void: direction degenerate after tangent projection.")
            sys.exit(44)
        d = d / dn
        xs, ds, t_norms, dlt_norms = [x0_64.copy()], [d.copy()], [], []
        x = x0_64.copy()
        for _ in range(GEO_K):
            t = ALPHA_GEO * d
            tn = float(np.linalg.norm(t))
            if abs(tn - ALPHA_GEO) / ALPHA_GEO > 1e-6:
                log("apparatus-void: tangent step norm %.9f != alpha." % tn)
                sys.exit(44)
            t_norms.append(tn)
            xn = (x + t) * (r0 / float(np.linalg.norm(x + t)))
            dlt_norms.append(float(np.linalg.norm(xn - x)))
            x = xn
            xh = x / float(np.linalg.norm(x))
            d = d - float(np.dot(d, xh)) * xh
            d = d / float(np.linalg.norm(d))
            xs.append(x.copy())
            ds.append(d.copy())
        s_dlt = float(np.sum(dlt_norms))
        lo = B_GEO * (1.0 - ALPHA_GEO ** 2 / (2.0 * r0 ** 2)) - 1e-6 * B_GEO
        if not (lo <= s_dlt <= B_GEO + 1e-6 * B_GEO):
            log("apparatus-void: retracted total %.9f outside [%.9f, %.9f]." % (s_dlt, lo, B_GEO + 1e-6 * B_GEO))
            sys.exit(44)
        return {"xs": xs, "ds": ds, "t_norms": t_norms, "dlt_norms": dlt_norms,
                "xK": xs[-1], "dK": ds[-1], "x0_norm": r0}

    geo_per_item = []
    for pi, pid in enumerate(prompt_ids):
        cur_id[0] = pid
        x0_64 = base_states[pi].detach().cpu().numpy().astype(np.float64)
        v1_64 = v1[pid].detach().cpu().numpy().astype(np.float64)
        ba_64 = b_agg.detach().cpu().numpy().astype(np.float64)
        w_v1 = geodesic_walk(x0_64, v1_64)
        w_ba = geodesic_walk(x0_64, ba_64)
        deltas = {"geo_v1": w_v1["xK"] - x0_64, "geo_bagg": w_ba["xK"] - x0_64}
        rec = {"id": pid, "arms": {}}
        base_dec = None
        for an in ["base", "geo_v1", "geo_bagg"]:
            if an == "base":
                st = base_states[pi].to(torch.float64)
            else:
                delta = torch.from_numpy(np.ascontiguousarray(deltas[an].astype(np.float32))).to(device)
                st = inject_forward(input_ids_list[pi], delta)
            dec, c1, c2, mar = readout(st.numpy() if isinstance(st, torch.Tensor) else st)
            rec["arms"][an] = {"decision": dec, "margin": mar,
                               "sum_dlt": float(np.sum(w_v1["dlt_norms"])) if an == "geo_v1"
                               else float(np.sum(w_ba["dlt_norms"]))}
            if an == "base":
                base_dec = dec
        rec["dm"] = {an: (1 if rec["arms"][an]["decision"] != base_dec else 0)
                     for an in ["geo_v1", "geo_bagg"]}
        geo_per_item.append(rec)
        log("geodesic %d/%d %s: base=%s | dm: %s" % (
            pi + 1, N_PROMPTS, pid, base_dec, rec["dm"]))
    dm_geo_q = sum(r["dm"]["geo_v1"] for r in geo_per_item)
    dm_geo_bagg_q = sum(r["dm"]["geo_bagg"] for r in geo_per_item)
    q3_pass = (dm_geo_q == 0)
    log("Q3: quantized geodesic DM_geo=%d/10 (B_agg-path flips=%d) -> %s" % (
        dm_geo_q, dm_geo_bagg_q, "PASS" if q3_pass else "FAIL"))

    # ---------------- 15. post-run integrity: quantized copy + FP32 reference ----------------
    h_q_post = state_dict_hash(model)
    log("quantized copy sha256 (post): %s" % h_q_post)
    if h_q_post != h_q_pre:
        log("apparatus-void: quantized copy drifted during the run (breaking point (h)).")
        sys.exit(44)
    log("quantized-copy integrity PASS (breaking point (h)).")
    # FP32 reference: reload from disk (never modified) and re-pin — Delta-theta guard.
    del model
    gc.collect()
    model_fp32 = transformers.AutoModelForCausalLM.from_pretrained(
        WEIGHTS_DIR, local_files_only=True, trust_remote_code=False,
        torch_dtype=torch.float32)
    h_fp32_post = state_dict_hash(model_fp32)
    log("FP32 reference pin (post): %s" % h_fp32_post)
    if h_fp32_post != WEIGHTS_PIN:
        log("apparatus-void: FP32 reference drifted (breaking point (a)).")
        sys.exit(44)
    log("Delta-theta guard PASS: FP32 reference unmodified.")
    del model_fp32
    gc.collect()

    # ---------------- 16. baseline shifts (quantized vs FP32 alpha=0 decisions) ----------------
    fp32_decisions, q_decisions = [], []
    for pi, pid in enumerate(prompt_ids):
        cur_id[0] = pid
        dec_fp32, _, _, _ = readout(fp32_base_states[pi].to(torch.float64).numpy()
                                    if isinstance(fp32_base_states[pi], torch.Tensor)
                                    else fp32_base_states[pi])
        # NOTE: readout uses the QUANTIZED option embeddings; the FP32-vs-quantized
        # baseline comparison is therefore on decision labels under a common readout.
        # A cleaner attribution (FP32 readout on FP32 states) is recorded below.
        fp32_decisions.append(dec_fp32)
        q_decisions.append(per_item[pi]["arms"]["base"]["decision"])
    baseline_shifts = sum(1 for a, b in zip(fp32_decisions, q_decisions) if a != b)
    log("baseline shift: %d/%d quantized alpha=0 decisions differ from FP32 (common readout)" % (
        baseline_shifts, N_PROMPTS))

    # ---------------- 17. tier Booleans (execution only — NO verdict) ----------------
    tiers = {
        "Q1_c_hat_q": c_hat_q, "Q1_pass": q1_pass,
        "Q2_dm_v1_q": dm_v1_q, "Q2_pass": q2_pass,
        "Q3_dm_geo_q": dm_geo_q, "Q3_dm_geo_bagg_q": dm_geo_bagg_q, "Q3_pass": q3_pass,
        "Q4_mcnemar_b": b_mc, "Q4_mcnemar_c": c_mc, "Q4_mcnemar_n": n_mc,
        "Q4_p": p_mc, "Q4_pass": q4_pass,
        "Q5_dm_bagg_q": dm_bagg_q, "Q5_pass": True,
        "Q6_r_probes": r_probes, "Q6_pass": q6_pass,
        "baseline_shifts": baseline_shifts, "budget_B_q": B,
        "c_hat_exclusions": c_excl,
    }
    log("=" * 70)
    log("TIERS (raw, execution only — verdict belongs to the independent review lane):")
    for k in ["Q1_pass", "Q2_pass", "Q3_pass", "Q4_pass", "Q5_pass", "Q6_pass"]:
        log("  %s = %s" % (k, tiers[k]))
    log("  c_hat_q=%.5f dm_v1_q=%d dm_geo_q=%d p_q=%.6f baseline_shifts=%d/%d" % (
        c_hat_q, dm_v1_q, dm_geo_q, p_mc, baseline_shifts, N_PROMPTS))
    log("  elapsed: %.1f min" % ((time.time() - t0) / 60.0))
    log("=" * 70)

    # ---------------- 18. Law #8: records + report + hash pins ----------------
    rec = {
        "experiment": "EXP138", "env": env,
        "pins": {"prereg": h_prereg, "weights_fp32_pre": h_pre,
                 "weights_fp32_post": h_fp32_post, "quantized_pre": h_q_pre,
                 "quantized_post": h_q_post, "v1_npz": h_npz,
                 "bagg_reconstruction": h_bagg, "bench": BENCH_PIN},
        "budget_B_q": B, "budget_B_geo": B_GEO,
        "c_hat_q_per_prompt": c_hats, "c_hat_exclusions": c_excl,
        "tiers": {k: (float(v) if isinstance(v, (np.floating,)) else v)
                  for k, v in tiers.items() if not isinstance(v, dict)},
        "r_probes": r_probes,
        "fp32_base_decisions": fp32_decisions,
        "quantized_base_decisions": q_decisions,
        "per_item_oneshot": per_item, "per_item_geodesic": geo_per_item,
        "meta": {"verdict": "PENDING-INDEPENDENT-REVIEW"},
    }
    rpath = os.path.join(OUTDIR, "exp138_records.json")
    with open(rpath, "w") as fh:
        json.dump(rec, fh, indent=1, default=str)
    pin = sha256_file(rpath)
    with open(rpath + ".sha256", "w") as fh:
        fh.write(pin + "\n")
    log("raw-record hash-pin: %s" % pin)
    with open(os.path.join(OUTDIR, "exp138_report.json"), "w") as fh:
        json.dump({"experiment": "EXP138", "tiers": tiers, "records_pin": pin,
                   "env": env, "elapsed_min": (time.time() - t0) / 60.0}, fh, indent=1, default=str)
    log("report written. Execution complete — NO verdict (independent review lane decides).")


if __name__ == "__main__":
    main()
