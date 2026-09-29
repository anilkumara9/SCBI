#!/usr/bin/env python3
"""EXP131: TGA v_1 Injection Test — dynamics-matched injection in the frozen Pythia-410m.

Pre-registered protocol (signed, Law #14 SIGN-WITH-FIXES LOG-4725,
six fixes byte-verified LOG-4726):
    research/prereg/EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md

GPU-GATED bundle: runs on the founder's hardware (Kaggle/Colab T4).
This lane builds and smoke-tests the bundle only; execution is founder-gated.

$0 CPU at build. Delta-theta = 0 by construction: pure forwards through
a frozen model in eval mode; no optimizer, no loss, no backward pass
into weights; parameter tensors carry requires_grad=False. (The c-hat
gate uses exact autograd VJPs through the frozen graph — a backward
through the graph, never into weights — per breaking point (f).)

Falsification-tree order (Law #9, protocol §5):
guards -> backbone pin -> artifact re-pins (v1/v2/B_agg) ->
budget computation and record -> c-hat gate -> forward batches
(injections, any batch order) -> validity-check evaluation
(norm audit + B_agg null-control + re-pin) -> raw-record
hash-pin -> metric (median r, DeltaM, McNemar, rank trend) -> decision.

Exit codes: 0 = verdict reached; 42 = protocol/pin guard failure;
43 = B_agg null-control fired (RUN-INVALID, apparatus drift);
44 = apparatus-void (breaking-point miss, hypothesis UNTESTED).
"""
import argparse
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
PROTOCOL_PIN = "d85205f4ce2b1aadd2b2bda64397f7523e15958cf4fd8d903acccf0fd7f8bf52"
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
V1_NPZ_PIN = "9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc"
BENCH_PIN = "e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5"
SITE = 20  # program-standard site: input of block 20 = hidden_states[20]
MODEL_NAME = "EleutherAI/pythia-410m"

# Paths: resolve relative to the bundle dir so Kaggle upload just works.
BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BUNDLE_DIR, "out")
os.makedirs(OUTDIR, exist_ok=True)
LOGF = open(os.path.join(OUTDIR, "exp131_console.log"), "a")

PROTOCOL_CANDIDATES = [
    os.path.join(BUNDLE_DIR, "EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md"),
    os.path.expanduser("~/workspace/SCBI/research/prereg/EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md"),
]
V1_NPZ_CANDIDATES = [
    os.path.join(BUNDLE_DIR, "exp127_vectors.npz"),
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


def decision_tree(verdict_inputs):
    """Pure decision-tree logic (protocol §2 + §4, KILL branches first per FIX-1).

    verdict_inputs: dict with keys
      c_hat (float), dm_v1 (int), mcnemar_p (float or None), rank_trend (bool),
      median_r (float), dm_bagg (int), apparatus_void (str|None)
    Returns (verdict, reason). Verdicts: CONTINUE / KILL / HELD /
    RUN-INVALID / APPARATUS-VOID.
    """
    vi = verdict_inputs
    if vi.get("apparatus_void"):
        return ("APPARATUS-VOID", vi["apparatus_void"])
    if vi["dm_bagg"] != 0:
        return ("RUN-INVALID", "B_agg null-control fired: DM_Bagg=%d != 0 (apparatus drift, breaking point (e))" % vi["dm_bagg"])
    # KILL branches evaluated FIRST (EXP129 FIX-1 precedence discipline).
    # NOTE on the protocol table's overlap: "DeltaM_v1 = 0 -> KILL" and
    # "median r >= 2 but DeltaM_v1 = 0 -> HELD" are both rows. The coherent
    # reading (documented, conservative): the KILL branch is INERTNESS
    # (no margin gain either); margin gain without flips is HELD.
    if vi["c_hat"] < 0.1:
        return ("KILL", "decision-orthogonal amplifier: c_hat=%.4f < 0.1" % vi["c_hat"])
    if vi["dm_v1"] == 0 and vi["median_r"] < 2.0:
        return ("KILL", "v1 inert: DM_v1=0 with no margin gain (median r=%.4f < 2)" % vi["median_r"])
    if vi["dm_v1"] == 0 and vi["median_r"] >= 2.0:
        return ("HELD", "amplifier moves the residual but not the decision (median r=%.4f >= 2, DM_v1=0)" % vi["median_r"])
    if not vi["rank_trend"]:
        return ("KILL", "flat rank trend: injection effect does not rank-order with singular rank")
    # CONTINUE: all conjunctive bars.
    if (vi["c_hat"] >= 0.1 and vi["median_r"] >= 2.0 and vi["dm_v1"] > 0
            and vi["mcnemar_p"] is not None and vi["mcnemar_p"] <= 0.05
            and vi["rank_trend"] and vi["dm_bagg"] == 0):
        return ("CONTINUE", "first bound positive steering signal: c_hat>=0.1, median r>=2, DM_v1>0 with McNemar p<=0.05, rank trend holds, B_agg null")
    # Residual: hypothesis's quantitative core (>=2x paired gain) unmet.
    return ("KILL", "CONTINUE conjunctive bar unmet (median r=%.4f, McNemar p=%s); the >=2x paired-gain hypothesis is falsified" % (vi["median_r"], vi["mcnemar_p"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="smoke mode: 1 prompt, K=1 random arm, full pipeline end-to-end")
    ap.add_argument("--weights", default=None,
                    help="local weights dir (default: HF download at runtime)")
    args = ap.parse_args()
    SMOKE = args.smoke
    N_PROMPTS = 1 if SMOKE else 10
    K_RAND = 1 if SMOKE else 8
    log("== EXP131 (v1 injection test) execution lane ==")
    log("mode: %s" % ("SMOKE (1 prompt, K=1 random)" if SMOKE else "FULL (10 prompts, K=8 randoms)"))

    # ---------------- 0. protocol hash before anything ----------------
    proto = first_existing(PROTOCOL_CANDIDATES, "protocol")
    h_proto = sha256_file(proto)
    log("protocol sha256: %s" % h_proto)
    if h_proto != PROTOCOL_PIN:
        log("HALT: protocol hash mismatch. Tree terminates before any forward is minted.")
        sys.exit(42)
    log("protocol pin OK (post-fix LOG-4726 revision)")

    # ---------------- 1. prompts: bench build + pin, canonical first N ----------------
    sys.path.insert(0, BUNDLE_DIR)
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
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(20260929)
    env = {
        "torch": torch.__version__, "transformers": transformers.__version__,
        "numpy": np.__version__, "device": str(device),
        "cuda": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "smoke": SMOKE,
    }
    log("env: %s" % json.dumps(env))

    # ---------------- 3. frozen backbone ----------------
    snap = args.weights or MODEL_NAME
    model = transformers.AutoModelForCausalLM.from_pretrained(
        snap, local_files_only=args.weights is not None, trust_remote_code=False,
        torch_dtype=torch.float32, output_hidden_states=True, output_attentions=False)
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)
    model.to(device)
    h_pre = state_dict_hash(model)
    log("backbone LOG-331 pin (pre): %s" % h_pre)
    if h_pre != WEIGHTS_PIN:
        log("RUN-INVALID: backbone hash mismatch before first forward (Law #6). Quarantine. No metric exists.")
        sys.exit(42)
    log("backbone pin OK. Delta-theta guard armed.")
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        snap, local_files_only=args.weights is not None, trust_remote_code=False)
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

    # ---- B_agg: deterministic reconstruction from the EXP077 archived support set ----
    from exp077_support import support_prompts, build_candidate_directions, VOCAB_KEYS  # noqa: E402
    sup_items = list(support_prompts())
    log("support set: %d contrast pairs (300 presentations, verbatim EXP077 construction)" % len(sup_items))
    delta_h_by_vocab = {vk: [] for vk in VOCAB_KEYS}
    h_all = []
    with torch.no_grad():
        for sid, p_rel, p_neu in sup_items:
            ids_rel = tokenizer.encode(p_rel, return_tensors="pt").to(device)
            ids_neu = tokenizer.encode(p_neu, return_tensors="pt").to(device)
            o_rel = model(input_ids=ids_rel, output_hidden_states=True)
            o_neu = model(input_ids=ids_neu, output_hidden_states=True)
            h_rel = o_rel.hidden_states[SITE + 1][0, -1, :].detach().cpu()  # output of block 20 (EXP077 space)
            h_neu = o_neu.hidden_states[SITE + 1][0, -1, :].detach().cpu()
            vk = next(k for k in VOCAB_KEYS if sid.startswith("sup_" + k + "_"))
            assert vk in delta_h_by_vocab, "support id vocab mismatch: %s" % sid
            delta_h_by_vocab[vk].append(h_rel - h_neu)
            h_all.extend([h_rel, h_neu])
    for vk in VOCAB_KEYS:
        delta_h_by_vocab[vk] = torch.stack(delta_h_by_vocab[vk])
    assert len(h_all) == 300, "expected 300 support presentations, got %d" % len(h_all)
    cand = build_candidate_directions(delta_h_by_vocab, h_all)
    b_agg = cand["v_hat"].detach()
    assert b_agg.shape == (H,)
    h_bagg = hashlib.sha256(b_agg.numpy().astype(np.float32).tobytes()).hexdigest()
    log("B_agg re-derived deterministically from EXP077 support set; reconstruction sha256: %s" % h_bagg)
    log("support continuity diagnostic mean_cos_v1=%.4f" % cand["mean_cos_v1"])
    del h_all, delta_h_by_vocab  # free memory before the injection phase

    # ---------------- 5. base forwards + budget B (recorded BEFORE first injection forward) ----------------
    input_ids_list = [tokenizer.encode(t, return_tensors="pt").to(device) for t in [p["prompt"] for p in prompts]]
    y20_norms, base_states, base_hs_all = [], [], []
    with torch.no_grad():
        for pi in range(N_PROMPTS):
            out = model(input_ids=input_ids_list[pi], output_hidden_states=True)
            hs = out.hidden_states
            y20 = hs[SITE][0, -1, :].detach()
            y20_norms.append(float(y20.norm().item()))
            base_states.append(y20.cpu())
            base_hs_all.append([h.detach() for h in hs])
    B = 0.01 * float(np.median(np.array(y20_norms)))
    assert B > 0 and math.isfinite(B)
    log("budget B = 0.01 * median||y20|| = %.8f  (recorded BEFORE first injection forward)" % B)

    # ---------------- 6. option embeddings (fresh forwards, no injection) + single-token assert ----------------
    option_embs = {}
    for pi, p in enumerate(prompts):
        E1, E2 = p["tuple"][0], p["tuple"][-1]
        assert E1 != E2
        for side, E in (("E1", E1), ("E2", E2)):
            ids = tokenizer.encode(" " + E, add_special_tokens=False)
            if len(ids) != 1:
                log("RUN-INVALID: single-token assertion failed at execution on item %s: ' %s'->%s. Items NOT silently dropped." % (p["id"], E, ids))
                sys.exit(43)
            with torch.no_grad():
                out = model(input_ids=tokenizer.encode(" " + E, return_tensors="pt").to(device),
                            output_hidden_states=True)
            option_embs[(p["id"], side)] = out.hidden_states[SITE][0, -1, :].detach().cpu().to(torch.float64)
    log("option forwards complete; single-token assert passed on all %d option texts" % (2 * N_PROMPTS))

    def cos_np(a, v):
        return float(np.dot(a, v) / (np.linalg.norm(a) * np.linalg.norm(v)))

    def readout(state64):
        c1 = cos_np(state64, option_embs[(cur_id[0], "E1")])
        c2 = cos_np(state64, option_embs[(cur_id[0], "E2")])
        dec = "E2" if c1 == c2 else ("E1" if c1 > c2 else "E2")
        return dec, c1, c2, abs(c1 - c2)

    # ---------------- 7. v2 derivation (LOG-4714 erratum: K=40, seed pinned, exact JVP/VJP) ----------------
    # EXP127 clamped-context apparatus (Law-#14-licensed, EXP127/EXP129).
    LN_EPS = cfg.layer_norm_eps
    RND = 16
    inv_freq = model.gpt_neox.rotary_emb.inv_freq.detach().clone()
    SCALE = 1.0 / math.sqrt(HD)
    W = {"ln1w": [], "ln1b": [], "ln2w": [], "ln2b": [], "qkv": [], "qkvb": [],
         "dense": [], "denseb": [], "h4": [], "h4b": [], "o4": [], "o4b": []}
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

    def sensing_discipline_assert():
        used = set(SENSING_OPS)
        bad = used - {"exact-jvp", "exact-vjp"}
        assert not bad, "apparatus-void: BLACKLISTED sensing op used: %s" % sorted(bad)
        log("sensing-discipline assert PASS: ops=%s (whitelist: exact JVP/VJP only; blacklist: finite-difference gain ratios)" % sorted(used))

    K_V2 = 40  # fixed iteration count, same for every prompt (FIX-4)
    gen_v2 = torch.Generator()
    gen_v2.manual_seed(20260929_4714)
    v2 = {}
    for pi, pid in enumerate(prompt_ids):
        hs = base_hs_all[pi]
        T = input_ids_list[pi].shape[1]
        Kc, Vc = [], []
        for li in range(4):
            K, V = build_clamped_kv(hs[SITE + li][0].detach(), li)
            Kc.append(K); Vc.append(V)
        f = make_f(Kc, Vc, T)
        z0 = hs[SITE][0, -1].detach()
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
        if ortho >= 1e-6:
            log("apparatus-void: v2 orthogonality assert failed (|v2.v1|=%.3e)." % ortho)
            sys.exit(44)
        v2[pid] = v2i
        log("v2 %d/%d %s: K=%d |v2.v1|=%.3e OK" % (pi + 1, N_PROMPTS, pid, K_V2, ortho))
    sensing_discipline_assert()  # breaking point (c): no finite-difference sensing anywhere

    # ---------------- 8. c-hat gate (exact VJP on the BASE forward, before any injection) ----------------
    cur_id = [None]
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
        log("apparatus-void: >=3 degenerate ||g|| exclusions in c-hat gate.")
        sys.exit(44)
    c_hat = float(np.mean(c_hats)) if c_hats else 0.0
    log("c-hat gate: mean=%.4f over %d prompts (%d exclusions)" % (c_hat, len(c_hats), len(c_excl)))

    # ---------------- 9. injection forwards (Law #9: forward batches) ----------------
    CAP = {}

    def inject_forward(input_ids, delta):
        def hook_fn(_m, _inp, outp):
            o = outp.clone()
            o[:, -1, :] = o[:, -1, :] + delta
            return o
        h_inj = layers[19].register_forward_hook(hook_fn)  # input of block 20
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
        gen_r.manual_seed(20260929_4724 + pi * 100)
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
                # norm-budget audit: every arm spends exactly B (breaking point (d))
                rel = abs(inj_norm - B) / B
                norm_audit.append(rel <= 1e-6)
                if rel > 1e-6:
                    log("apparatus-void: arm %s norm %.8f != B %.8f (rel %.3e)." % (an, inj_norm, B, rel))
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
        log("item %d/%d %s: base=%s margin=%.4f | dm: %s" % (
            pi + 1, N_PROMPTS, pid, base_dec, base_mar,
            {an: rec["dm"][an] for an in rec["dm"]}))
    log("forward batches complete: %d prompts x %d forwards (+1 support pass, option forwards, v2 JVPs)" % (N_PROMPTS, len(arm_names)))

    # ---------------- 10. validity-check evaluation ----------------
    if not all(norm_audit):
        log("apparatus-void: norm-budget audit failed (breaking point (d)).")
        sys.exit(44)
    log("norm-budget audit PASS: all %d injection arms within 1e-6 rel of B" % len(norm_audit))
    h_post = state_dict_hash(model)
    log("backbone LOG-331 pin (post): %s" % h_post)
    if h_post != WEIGHTS_PIN:
        log("apparatus-void: backbone hash mismatch after forwards.")
        sys.exit(44)

    dm_bagg = sum(r["dm"]["bagg"] for r in per_item)
    if dm_bagg != 0:
        log("RUN-INVALID: B_agg null-control fired (DM_Bagg=%d != 0 — apparatus drift, breaking point (e)). Hypothesis UNTESTED." % dm_bagg)
        _write_records(per_item, env, h_pre, h_post, B, c_hats, c_excl, h_bagg, h_npz,
                       {"verdict": "RUN-INVALID", "reason": "B_agg null-control fired"})
        sys.exit(43)

    # ---------------- 11. raw-record hash-pin (BEFORE any metric) ----------------
    pin = _write_records(per_item, env, h_pre, h_post, B, c_hats, c_excl, h_bagg, h_npz,
                         {"verdict": "PENDING-METRIC"})
    log("raw-record hash-pin: %s (minted before any decision statistic)" % pin)

    # ---------------- 12. metrics ----------------
    # (a) median margin-displacement ratio r (FIX-2 zero-denominator branch)
    rs = []
    for r in per_item:
        num = r["margin_disp"]["v1"]
        den = max(r["margin_disp"]["rand%d" % j] for j in range(K_RAND))
        if den == 0.0:
            rs.append(1.0 if num == 0.0 else float("inf"))
        else:
            rs.append(num / den)
    rs_fin = [x for x in rs if math.isfinite(x)]
    median_r = float(np.median(rs_fin)) if rs_fin else float("inf")
    # (b) decision flips + McNemar v1 vs best-random (FIX-1: global-best arm)
    rand_flips = {j: sum(r["dm"]["rand%d" % j] for r in per_item) for j in range(K_RAND)}
    j_star = min([j for j in rand_flips if rand_flips[j] == max(rand_flips.values())])
    dm_v1 = sum(r["dm"]["v1"] for r in per_item)
    b_mc = sum(1 for r in per_item if r["dm"]["v1"] == 1 and r["dm"]["rand%d" % j_star] == 0)
    c_mc = sum(1 for r in per_item if r["dm"]["v1"] == 0 and r["dm"]["rand%d" % j_star] == 1)
    n_mc = b_mc + c_mc
    p_mc = binom_sf_ge(b_mc, n_mc) if n_mc > 0 else 1.0
    # (c) singular-rank trend gate
    trend_hits = sum(1 for r in per_item
                     if r["margin_disp"]["v1"] > r["margin_disp"]["v2"]
                     > np.median([r["margin_disp"]["rand%d" % j] for j in range(K_RAND)]))
    rank_trend = trend_hits >= 8 if N_PROMPTS == 10 else (trend_hits >= 1)
    log("metrics: median r=%.6f | DM_v1=%d | best-random=j%d (flips=%d) | McNemar (b,c)=(%d,%d) n=%d p=%.6f | rank-trend %d/%d %s" % (
        median_r, dm_v1, j_star, rand_flips[j_star], b_mc, c_mc, n_mc, p_mc,
        trend_hits, N_PROMPTS, "PASS" if rank_trend else "FAIL"))

    # ---------------- 13. decision (KILL branches first per FIX-1) ----------------
    vi = {"c_hat": c_hat, "dm_v1": dm_v1, "mcnemar_p": p_mc,
          "rank_trend": rank_trend, "median_r": median_r, "dm_bagg": dm_bagg,
          "apparatus_void": None}
    verdict, reason = decision_tree(vi)
    log("=" * 70)
    log("VERDICT: %s" % verdict)
    log("reason: %s" % reason)
    log("=" * 70)

    _write_report(per_item, env, h_pre, h_post, B, c_hats, c_excl, h_bagg, h_npz,
                  pin, median_r, dm_v1, j_star, rand_flips, b_mc, c_mc, n_mc, p_mc,
                  trend_hits, rank_trend, verdict, reason, rs)
    log("report written to out/exp131_report.json")
    log("raw records: out/exp131_records.json (+ .sha256 pin)")


def _write_records(per_item, env, h_pre, h_post, B, c_hats, c_excl, h_bagg, h_npz, meta):
    rec = {
        "experiment": "EXP131", "env": env,
        "pins": {"protocol": PROTOCOL_PIN, "weights_pre": h_pre, "weights_post": h_post,
                 "v1_npz": h_npz, "bagg_reconstruction": h_bagg, "bench": BENCH_PIN},
        "budget_B": B, "c_hat_per_prompt": c_hats, "c_hat_exclusions": c_excl,
        "per_item": per_item, "meta": meta,
    }
    path = os.path.join(OUTDIR, "exp131_records.json")
    with open(path, "w") as fh:
        json.dump(rec, fh, indent=1, default=str)
    pin = sha256_file(path)
    with open(path + ".sha256", "w") as fh:
        fh.write(pin + "\n")
    return pin


def _write_report(per_item, env, h_pre, h_post, B, c_hats, c_excl, h_bagg, h_npz,
                  pin, median_r, dm_v1, j_star, rand_flips, b_mc, c_mc, n_mc, p_mc,
                  trend_hits, rank_trend, verdict, reason, rs):
    rep = {
        "experiment": "EXP131", "verdict": verdict, "reason": reason,
        "metrics": {
            "median_r": median_r, "r_per_item": rs,
            "dm_v1": dm_v1, "best_random_arm": j_star,
            "random_flips": rand_flips,
            "mcnemar_b": b_mc, "mcnemar_c": c_mc, "mcnemar_n": n_mc,
            "mcnemar_p_onesided": p_mc,
            "rank_trend_hits": trend_hits, "rank_trend": rank_trend,
            "c_hat_mean": float(np.mean(c_hats)) if c_hats else 0.0,
            "c_hat_exclusions": c_excl,
            "dm_bagg": sum(r["dm"]["bagg"] for r in per_item),
            "budget_B": B,
        },
        "records_pin": pin, "env": env,
    }
    with open(os.path.join(OUTDIR, "exp131_report.json"), "w") as fh:
        json.dump(rep, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
