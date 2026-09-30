#!/usr/bin/env python3
"""EXP133: GEOSTEER geodesic multistep steering along the TGA v1 direction (CPU pilot).

Pre-registration (CEO-SIGNED, LOG-4798):
    research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md
as amended by Amendment B (Law #14 SIGN, LOG-4801; CEO re-clearance LOG-4802)
    research/prereg/EXP133_AMENDMENT_B_2026-09-30.md
and Amendment C (Law #14 SIGN, LOG-4805; CEO re-clearance LOG-4806):
    research/prereg/EXP133_AMENDMENT_C_2026-09-30.md
(Amendment C: breaking point (d) tolerance 1e-6 -> 1e-4 relative for the
cross-device equality check only; injected dose still verbatim B per Law #2.)

Question: at fixed total norm budget B=0.50578119, can a K=5 geodesic multistep
path (sphere retraction + parallel transport) along TGA v1 move decisions where
EXP131's one-shot Euclidean injection moved none?

Executor derivation: copied from the Law-#14-reviewed EXP131 executor
(experiments/bundles/exp131_v1inj/run_exp131.py); the ONLY scientific delta is
the injection arm (one-shot -> K=5 geodesic micro-steps + sphere retraction,
pre-reg section 3.4 as repaired). Bench, backbone pinning, v1 re-pin, v2
derivation (LOG-4714 erratum parameters, run TWICE per Amendment B), B_agg
reconstruction (EXP077 support set), budget computation, option embeddings,
and the H1/H6 section 3.3 decision readout are byte-identical logic.

$0 CPU. Delta-theta = 0 by construction: pure forwards through a frozen model
in eval mode; no optimizer, no loss, no backward pass into weights; parameter
tensors carry requires_grad=False. (The c-hat computations use exact autograd
VJPs through the frozen graph — a backward through the graph, never into
weights — per breaking point (f).)

Falsification-tree order (Law #9, protocol section 5):
guards -> backbone pin -> artifact re-pins (v1 / v2-x2 / B_agg) ->
budget computation and record -> endpoint-c-hat gate -> forward batches
(geodesic injection paths, any batch order) -> validity-check evaluation
(per-step norm audit + retraction bound + B_agg-path null-control + re-pin) ->
raw-record hash-pin -> metric (c_geo, DeltaM_geo, McNemar, rank trend,
midpoint c) -> decision (section 2 table, KILL-first, DEFAULT->INCONCLUSIVE).

Exit codes: 0 = verdict reached; 42 = protocol/pin guard failure;
43 = B_agg-path null-control fired (RUN-INVALID, apparatus drift);
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
PROTOCOL_PIN = "ad2158bbdec7e86bd925031fad94fa3ce6a12dc5debe86d49edeec05a25ac8a3"  # signed pre-reg (LOG-4798)
AMENDMENT_PIN = "e4a7633584b76fc8274d13935f980010e3a2cd91db814a682c7f4707796c58ef"  # Amendment B (LOG-4801)
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
V1_NPZ_PIN = "9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc"
BENCH_PIN = "e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5"
BAGG_PIN = "d3556d83751634a2fc5114d56c4ee246bb1b296293d2adcde40a369da1600ae1"  # EXP131 pins.bagg_reconstruction
BUDGET_B = 0.50578119  # copied verbatim from LOG-4766 (Law #2); independently recomputed + asserted in §5
GEO_K = 5  # geodesic micro-steps
SITE = 20  # program-standard site: input of block 20 = hidden_states[20]
MODEL_NAME = "EleutherAI/pythia-410m"

# Paths: the executor lives in the EXP133 run dir; support modules are reused
# from the EXP131 bundle (only the injection arm changes).
RUN_DIR = os.path.dirname(os.path.abspath(__file__))
BUNDLE_DIR = os.path.expanduser("~/workspace/SCBI/experiments/bundles/exp131_v1inj")
OUTDIR = os.path.join(RUN_DIR, "out")
os.makedirs(OUTDIR, exist_ok=True)
LOGF = open(os.path.join(OUTDIR, "exp133_console.log"), "a")

PROTOCOL_CANDIDATES = [
    os.path.expanduser("~/workspace/SCBI/research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md"),
]
AMENDMENT_CANDIDATES = [
    os.path.expanduser("~/workspace/SCBI/research/prereg/EXP133_AMENDMENT_B_2026-09-30.md"),
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
    """EXP133 §2 decision table in §4 evaluation order.

    KILL branches precede CONTINUE bars (EXP129 FIX-1). First firing verdict wins.
    Verdicts: CONTINUE / KILL / PIVOT / INCONCLUSIVE / RUN-INVALID / APPARATUS-VOID.
    """
    vi = verdict_inputs
    if vi.get("apparatus_void"):
        return ("APPARATUS-VOID", vi["apparatus_void"])
    if vi["dm_bagg"] != 0:
        return ("RUN-INVALID", "B_agg-path null-control fired: DM_Bagg=%d != 0 (apparatus drift, breaking point (e))" % vi["dm_bagg"])
    if vi["dm_geo"] == 0:
        # Midpoint-PIVOT check fires BEFORE the endpoint-null KILL (§4, A3).
        if vi["n_pivot_prompts"] >= 2:
            return ("PIVOT", "endpoints null BUT %d prompts show midpoint c^>=0.1 on the v1 geodesic — "
                    "path-midpoint targeting: curvature exists mid-path but washes out at the endpoint; "
                    "a new matched-budget design may be drafted (never a dose increase)" % vi["n_pivot_prompts"])
        if vi["c_geo_mean"] < 0.1:
            return ("KILL", "decision-orthogonal geodesic null: DM_geo=0 and mean c_geo=%.4f < 0.1 "
                    "(§0 gate, F3 conditional on the endpoint null)" % vi["c_geo_mean"])
        return ("KILL", "geodesic v1 endpoint null: DM_geo=0; the kill stands on the decision question "
                "without the orthogonality characterization (c_geo=%.4f >= 0.1, F3)" % vi["c_geo_mean"])
    # DM_geo > 0 branch — KILL branches first (FIX-1).
    if vi["path_noise"]:
        return ("KILL", "path-noise: geodesic v1 moves decisions only where a matched random path "
                "also does — the effect is path-noise, not the amplifier's")
    if (vi["mcnemar_p"] is not None and vi["mcnemar_p"] <= 0.05 and vi["rank_trend"]
            and vi["outmoves_best_random"] and vi["dm_bagg"] == 0):
        return ("CONTINUE", "first bound positive steering signal in program history: DM_geo=%d, "
                "McNemar(geo,base) one-sided p=%.4f<=0.05, rank-trend holds (%d/10), geodesic v1 "
                "out-moves the best random path, B_agg-path null — multistep-geodesic is a licensed "
                "instrument class on Pythia-410m L20, the 10 pinned prompts, matched budget" % (
                    vi["dm_geo"], vi["mcnemar_p"], vi["trend_hits"]))
    if (vi["mcnemar_p"] is not None and vi["mcnemar_p"] <= 0.05
            and vi["random_null_holding"] and not vi["rank_trend"]):
        return ("KILL", "rank-trend gate: DM_geo=%d with McNemar p=%.4f<=0.05 but rank trend flat/inverted "
                "(%d/10 < 8) — the effect is not the amplifier's" % (
                    vi["dm_geo"], vi["mcnemar_p"], vi["trend_hits"]))
    if vi["mcnemar_p"] is not None and vi["mcnemar_p"] > 0.05 and vi["random_null_holding"]:
        return ("INCONCLUSIVE", "DM_geo=%d > 0 but McNemar(geo,base) n.s. (p=%.4f), random-null holding — "
                "insufficient power at N=%d pinned prompts; hypothesis UNTESTED, licenses no follow-up" % (
                    vi["dm_geo"], vi["mcnemar_p"], vi["n_prompts"]))
    # B2 repair: any measured outcome matching no row above.
    return ("INCONCLUSIVE", "DEFAULT (B2): measured outcome matches no CONTINUE/PIVOT/RUN-INVALID/"
            "apparatus-void conjunct — hypothesis UNTESTED; licenses nothing; no CONTINUE/PIVOT claim "
            "may be read from this corner (Law #4)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="smoke mode: 1 prompt, full pipeline end-to-end (norm-audit check)")
    ap.add_argument("--weights", default=None,
                    help="local weights dir (default: HF download at runtime)")
    args = ap.parse_args()
    SMOKE = args.smoke
    N_PROMPTS = 1 if SMOKE else 10
    K_RAND = 2  # pre-reg §3.5: two matched-norm random-path geodesics (fixed, both modes)
    log("== EXP133 (GEOSTEER geodesic multistep, K=%d) execution lane ==" % GEO_K)
    log("mode: %s" % ("SMOKE (1 prompt, K=2 random paths)" if SMOKE else "FULL (10 prompts, K=2 random paths)"))

    # ---------------- 0. protocol hashes before anything ----------------
    proto = first_existing(PROTOCOL_CANDIDATES, "protocol")
    h_proto = sha256_file(proto)
    log("protocol sha256: %s" % h_proto)
    if h_proto != PROTOCOL_PIN:
        log("HALT: protocol hash mismatch. Tree terminates before any forward is minted.")
        sys.exit(42)
    amend = first_existing(AMENDMENT_CANDIDATES, "amendment")
    h_amend = sha256_file(amend)
    log("amendment sha256: %s" % h_amend)
    if h_amend != AMENDMENT_PIN:
        log("HALT: amendment hash mismatch. Tree terminates before any forward is minted.")
        sys.exit(42)
    log("protocol + amendment pins OK (signed pre-reg LOG-4798 as amended LOG-4801/4802)")

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
    torch.use_deterministic_algorithms(True)  # pre-reg §3.2: deterministic-algorithms flag set
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
    if h_bagg != BAGG_PIN:
        log("apparatus-void: B_agg reconstruction hash mismatch (breaking point (b3)). "
            "Expected %s, got %s." % (BAGG_PIN, h_bagg))
        sys.exit(44)
    log("B_agg hash gate PASS (breaking point (b3)): matches EXP131 pins.bagg_reconstruction")
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
    # Breaking point (d): independent recompute must equal the LOG-4766 verbatim value (Law #2).
    # The equality assert is meaningful only on the full 10-prompt bench (the verbatim value is a
    # 10-prompt median); in smoke mode (1 prompt) it is logged but not asserted.
    if N_PROMPTS == 10:
        if abs(B - BUDGET_B) / BUDGET_B > 1e-4:
            log("apparatus-void: recomputed B=%.8f != verbatim %.8f (rel %.3e) — bench/backbone drift." % (
                B, BUDGET_B, abs(B - BUDGET_B) / BUDGET_B))
            sys.exit(44)
        log("budget pin OK: recomputed B matches %.8f within 1e-4 rel (breaking point (d), Amendment C)" % BUDGET_B)
    else:
        log("smoke mode: 1-prompt recompute (%.8f) logged; verbatim-equality assert deferred to the full run" % B)
    B = BUDGET_B  # use the verbatim registered value downstream
    ALPHA = B / GEO_K

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

    def sensing_discipline_assert():
        used = set(SENSING_OPS)
        bad = used - {"exact-jvp", "exact-vjp"}
        assert not bad, "apparatus-void: BLACKLISTED sensing op used: %s" % sorted(bad)
        log("sensing-discipline assert PASS: ops=%s (whitelist: exact JVP/VJP only; blacklist: finite-difference gain ratios)" % sorted(used))

    K_V2 = 40  # fixed iteration count, same for every prompt (FIX-4)

    def derive_v2():
        """EXP131 §7 v2 derivation, byte-identical logic (LOG-4714 erratum parameters).

        Seeded deflated power iteration: generator seed 20260929_4714, K=40 fixed
        iterations per prompt, exact JVP/VJP sensing on the frozen L20→L24
        propagator, orthogonalization against the re-pinned v1 at every step.
        """
        gen = torch.Generator()
        gen.manual_seed(20260929_4714)
        out = {}
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
            v1d = v1[pid].to(device)
            q = torch.randn(H, generator=gen).to(device)
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
            out[pid] = v2i
            log("v2 %d/%d %s: K=%d |v2.v1|=%.3e OK" % (pi + 1, N_PROMPTS, pid, K_V2, ortho))
        return out

    # Amendment B §3.1: licensed deterministic reproduction, executed TWICE.
    v2_run1 = derive_v2()
    v2_run2 = derive_v2()

    def _v2_sha(v2d):
        blob = np.concatenate([v2d[pid].detach().cpu().numpy().astype(np.float32)
                               for pid in prompt_ids]).tobytes()
        return hashlib.sha256(blob).hexdigest()

    h_v2_1, h_v2_2 = _v2_sha(v2_run1), _v2_sha(v2_run2)
    log("v2 run-twice SHA-256: run1=%s" % h_v2_1)
    log("v2 run-twice SHA-256: run2=%s" % h_v2_2)
    if h_v2_1 != h_v2_2:
        log("apparatus-void: v2 run-twice bit-identity FAILED — nondeterminism, "
            "the LOG-4714 determinism assertion fails.")
        sys.exit(44)
    log("v2 run-twice bit-identity PASS")
    v2 = v2_run1
    for pid in prompt_ids:  # definitional asserts: unit norm (orthogonality asserted per-run above)
        n2 = float(v2[pid].norm().item())
        if abs(n2 - 1.0) > 1e-6:
            log("apparatus-void: v2 unit-norm assert failed on %s (|v2|=%.9f)." % (pid, n2))
            sys.exit(44)
        o2 = abs(float((v2[pid].to(torch.float64) @ v1[pid].to(torch.float64)).item()))
        if o2 >= 1e-6:
            log("apparatus-void: v2 orthogonality re-assert failed on %s (|v2.v1|=%.3e)." % (pid, o2))
            sys.exit(44)
    log("v2 definitional asserts PASS: ||v2||=1±1e-6, |v2.v1|<1e-6 on all %d prompts" % N_PROMPTS)
    sensing_discipline_assert()  # breaking point (c): no finite-difference sensing anywhere

    # ---------------- 8. geodesic walks + endpoint-c-hat gate (exact VJP at x_K) ----------------
    # Pure vector arithmetic (float64) on x_0 = x_{20,last}; no model contact.
    # Pre-reg §3.4 as repaired (F1): tangent injection t_k = alpha * d_k with
    # ||t_k|| = alpha audited per step; sphere retraction; parallel transport
    # by tangent-space projection + renormalization (the specified stepwise
    # procedure — NOT a single great-circle arc, N4).
    cur_id = [None]

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
            t = ALPHA * d
            tn = float(np.linalg.norm(t))
            if abs(tn - ALPHA) / ALPHA > 1e-6:  # breaking point (d): tangent audit
                log("apparatus-void: tangent step norm %.9f != alpha %.9f (rel %.3e)." % (
                    tn, ALPHA, abs(tn - ALPHA) / ALPHA))
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
        lo = B * (1.0 - ALPHA ** 2 / (2.0 * r0 ** 2)) - 1e-6 * B
        if not (lo <= s_dlt <= B + 1e-6 * B):  # F1 one-sided retraction bound
            log("apparatus-void: retracted total %.9f outside [%.9f, %.9f]." % (s_dlt, lo, B + 1e-6 * B))
            sys.exit(44)
        return {"xs": xs, "ds": ds, "t_norms": t_norms, "dlt_norms": dlt_norms,
                "xK": xs[-1], "dK": ds[-1], "x0_norm": r0}

    def chat_at(x_64, d_64, e1_64, e2_64):
        """| <d_unit, grad_x margin> | at state x — exact autograd VJP (float64),
        breaking point (f) apparatus. Returns None if ||g|| < 1e-12."""
        z = torch.from_numpy(np.ascontiguousarray(x_64)).clone().requires_grad_(True)
        e1 = torch.from_numpy(np.ascontiguousarray(e1_64))
        e2 = torch.from_numpy(np.ascontiguousarray(e2_64))
        c1 = torch.dot(z, e1) / (z.norm() * e1.norm())
        c2 = torch.dot(z, e2) / (z.norm() * e2.norm())
        margin = torch.abs(c1 - c2)
        g = torch.autograd.grad(margin, z, retain_graph=False)[0]
        if float(g.norm().item()) < 1e-12:
            return None
        g_hat = g / g.norm()
        return abs(float(torch.dot(torch.from_numpy(np.ascontiguousarray(d_64)), g_hat).item()))

    walks = {}  # walks[pid][arm] -> walk dict
    c_geos, c_oneshots, c_excl, mid_cs = [], [], [], {}
    gen_r = torch.Generator()
    for pi, pid in enumerate(prompt_ids):
        cur_id[0] = pid
        x0_64 = base_states[pi].detach().cpu().numpy().astype(np.float64)
        v1_64 = v1[pid].detach().cpu().numpy().astype(np.float64)
        v2_64 = v2[pid].detach().cpu().numpy().astype(np.float64)
        ba_64 = b_agg.detach().cpu().numpy().astype(np.float64)
        gen_r.manual_seed(20260929_4724 + pi * 100)  # pinned seed stream (EXP131 convention)
        rand_dirs = []
        for j in range(K_RAND):
            u = torch.randn(H, generator=gen_r)
            rand_dirs.append((u / u.norm()).numpy().astype(np.float64))
        dirs = {"geo_v1": v1_64, "geo_v2": v2_64, "geo_bagg": ba_64,
                **{"geo_rand%d" % j: rand_dirs[j] for j in range(K_RAND)}}
        w = {an: geodesic_walk(x0_64, u) for an, u in dirs.items()}
        walks[pid] = w
        e1 = option_embs[(pid, "E1")].numpy().astype(np.float64)
        e2 = option_embs[(pid, "E2")].numpy().astype(np.float64)
        cg = chat_at(w["geo_v1"]["xK"], w["geo_v1"]["dK"], e1, e2)  # [DEFINITION] c^_geo,i
        if cg is None:
            c_excl.append(pid)
        else:
            c_geos.append(cg)
        co = chat_at(x0_64 + B * v1_64, v1_64, e1, e2)  # one-shot endpoint c^ (diagnostic, §3.5 count)
        c_oneshots.append(co)
        m2 = chat_at(w["geo_v1"]["xs"][2], w["geo_v1"]["ds"][2], e1, e2)  # PIVOT diagnostic
        m3 = chat_at(w["geo_v1"]["xs"][3], w["geo_v1"]["ds"][3], e1, e2)
        mid_cs[pid] = {"k2": m2, "k3": m3}
        log("walk %d/%d %s: x0_norm=%.4f sum_t=%.6f sum_dlt=%.6f c_geo=%s c_oneshot=%s mid=(%s,%s)" % (
            pi + 1, N_PROMPTS, pid, w["geo_v1"]["x0_norm"],
            float(np.sum(w["geo_v1"]["t_norms"])), float(np.sum(w["geo_v1"]["dlt_norms"])),
            ("%.4f" % cg) if cg is not None else "EXCL",
            ("%.4f" % co) if co is not None else "nan",
            ("%.4f" % m2) if m2 is not None else "nan",
            ("%.4f" % m3) if m3 is not None else "nan"))
    if len(c_excl) >= 3:
        log("apparatus-void: >=3 degenerate ||g|| exclusions in endpoint c-hat gate.")
        sys.exit(44)
    c_geo_mean = float(np.mean(c_geos)) if c_geos else 0.0
    log("endpoint c-hat gate: mean c_geo=%.4f over %d prompts (%d exclusions)" % (
        c_geo_mean, len(c_geos), len(c_excl)))

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
    arm_names = ["base", "oneshot_v1", "geo_v1", "geo_v2", "geo_rand0", "geo_rand1", "geo_bagg"]
    path_arms = ["geo_v1", "geo_v2", "geo_bagg", "geo_rand0", "geo_rand1"]
    for pi, pid in enumerate(prompt_ids):
        cur_id[0] = pid
        x0_64 = base_states[pi].detach().cpu().numpy().astype(np.float64)
        w = walks[pid]
        # Injection deltas (float32, additive hook byte-identical to EXP131's).
        # One-shot arm: the EXP131 baseline re-measured on CPU (N3 contingency).
        # Geodesic arms: the retracted endpoint displacement x_K - x_0.
        v1_64 = v1[pid].detach().cpu().numpy().astype(np.float64)
        deltas = {"oneshot_v1": B * v1_64}
        for an in path_arms:
            deltas[an] = w[an]["xK"] - x0_64
        rec = {"id": pid, "arms": {}, "x0_norm": w["geo_v1"]["x0_norm"]}
        base_dec = base_mar = None
        for an in arm_names:
            if an == "base":
                st = base_states[pi].to(torch.float64)
                inj_norm = 0.0
            else:
                delta = torch.from_numpy(
                    np.ascontiguousarray(deltas[an].astype(np.float32))).to(device)
                st = inject_forward(input_ids_list[pi], delta)
                inj_norm = float(delta.norm().item())
                if an == "oneshot_v1":
                    # norm-budget audit: one-shot arm spends exactly B (breaking point (d))
                    rel = abs(inj_norm - B) / B
                    norm_audit.append(rel <= 1e-6)
                    if rel > 1e-6:
                        log("apparatus-void: one-shot arm norm %.8f != B %.8f (rel %.3e)." % (
                            inj_norm, B, rel))
                        sys.exit(44)
            dec, c1, c2, mar = readout(st.numpy() if isinstance(st, torch.Tensor) else st)
            arm_rec = {"decision": dec, "cos_E1": c1, "cos_E2": c2,
                       "margin": mar, "injected_norm": inj_norm}
            if an in path_arms:  # §3.8 per-step path records
                arm_rec["t_norms"] = w[an]["t_norms"]
                arm_rec["dlt_norms"] = w[an]["dlt_norms"]
                arm_rec["sum_t"] = float(np.sum(w[an]["t_norms"]))
                arm_rec["sum_dlt"] = float(np.sum(w[an]["dlt_norms"]))
                arm_rec["xK_checksum"] = hashlib.sha256(
                    w[an]["xK"].astype(np.float32).tobytes()).hexdigest()
            rec["arms"][an] = arm_rec
            if an == "base":
                base_dec, base_mar = dec, mar
        rec["dm"] = {an: (1 if rec["arms"][an]["decision"] != base_dec else 0)
                     for an in arm_names if an != "base"}
        rec["margin_disp"] = {an: abs(rec["arms"][an]["margin"] - base_mar)
                              for an in arm_names if an != "base"}
        gd = rec["arms"]["geo_v1"]["decision"]
        rec["flip_dir"] = ("E1->E2" if (base_dec, gd) == ("E1", "E2")
                           else "E2->E1" if (base_dec, gd) == ("E2", "E1") else None)
        per_item.append(rec)
        log("item %d/%d %s: base=%s margin=%.4f | dm: %s" % (
            pi + 1, N_PROMPTS, pid, base_dec, base_mar,
            {an: rec["dm"][an] for an in rec["dm"]}))
    log("forward batches complete: %d prompts x %d forwards "
        "(+1 support pass, option forwards, v2 JVPs, c-hat VJPs)" % (N_PROMPTS, len(arm_names)))

    # ---------------- 10. validity-check evaluation ----------------
    # Tangent-step norms were audited per step inside geodesic_walk (breaking point (d));
    # the retracted totals were checked against the F1 one-sided bound there as well.
    n_tangent_audits = N_PROMPTS * len(path_arms) * GEO_K
    if not all(norm_audit):
        log("apparatus-void: one-shot norm-budget audit failed (breaking point (d)).")
        sys.exit(44)
    log("norm-budget audit PASS: %d tangent steps at alpha±1e-6 rel + %d one-shot arms at B±1e-6 rel" % (
        n_tangent_audits, len(norm_audit)))
    h_post = state_dict_hash(model)
    log("backbone LOG-331 pin (post): %s" % h_post)
    if h_post != WEIGHTS_PIN:
        log("apparatus-void: backbone hash mismatch after forwards.")
        sys.exit(44)

    dm_bagg = sum(r["dm"]["geo_bagg"] for r in per_item)
    if dm_bagg != 0:
        log("RUN-INVALID: B_agg-path null-control fired (DM_Bagg=%d != 0 — apparatus drift, breaking point (e)). Hypothesis UNTESTED." % dm_bagg)
        _write_records(per_item, env, h_pre, h_post, B, c_geos, c_excl, c_oneshots, mid_cs,
                       h_bagg, h_npz, h_v2_1, h_v2_2, h_proto, h_amend,
                       {"verdict": "RUN-INVALID", "reason": "B_agg-path null-control fired"})
        sys.exit(43)

    # ---------------- 11. raw-record hash-pin (BEFORE any metric) ----------------
    pin = _write_records(per_item, env, h_pre, h_post, B, c_geos, c_excl, c_oneshots, mid_cs,
                         h_bagg, h_npz, h_v2_1, h_v2_2, h_proto, h_amend,
                         {"verdict": "PENDING-METRIC"})
    log("raw-record hash-pin: %s (minted before any decision statistic)" % pin)

    # ---------------- 12. metrics ----------------
    # (a) decision flips on the geodesic v1 endpoint arm
    dm_geo = sum(r["dm"]["geo_v1"] for r in per_item)
    dm_oneshot = sum(r["dm"]["oneshot_v1"] for r in per_item)
    # (b) directional McNemar (geodesic v1 vs base), one-sided in the majority-flip
    # direction. Operationalization note: the pre-reg registers "one-sided" without a
    # pre-specified flip direction (the hypothesis is unsigned); the test is therefore
    # run in the direction of the observed majority discordance, with b/c/n and the
    # majority direction recorded verbatim. The two-sided p is recorded alongside.
    b_dir = sum(1 for r in per_item if r["flip_dir"] == "E1->E2")
    c_dir = sum(1 for r in per_item if r["flip_dir"] == "E2->E1")
    n_dir = b_dir + c_dir
    maj_dir = "E1->E2" if b_dir >= c_dir else "E2->E1"
    p_geo_base = binom_sf_ge(max(b_dir, c_dir), n_dir) if n_dir > 0 else 1.0
    p_geo_base_twosided = min(1.0, 2.0 * p_geo_base) if n_dir > 0 else 1.0
    # (c) reference McNemar (geodesic v1 vs one-shot v1), EXP131 paired-flip convention
    b_ref = sum(1 for r in per_item if r["dm"]["geo_v1"] == 1 and r["dm"]["oneshot_v1"] == 0)
    c_ref = sum(1 for r in per_item if r["dm"]["oneshot_v1"] == 1 and r["dm"]["geo_v1"] == 0)
    n_ref = b_ref + c_ref
    p_geo_one = binom_sf_ge(b_ref, n_ref) if n_ref > 0 else 1.0
    # (d) rank-trend gate (§3.7/F4 single quantified definition):
    # margin_disp(geo_v1) >= margin_disp(geo_v2) on >= 8/10 prompts
    trend_hits = sum(1 for r in per_item
                     if r["margin_disp"]["geo_v1"] >= r["margin_disp"]["geo_v2"])
    trend_bar = 8 if N_PROMPTS == 10 else 1
    rank_trend = trend_hits >= trend_bar
    # (e) best-random-path (pinned before inspection: argmax flips, tie -> lowest index)
    rand_flips = {"geo_rand0": sum(r["dm"]["geo_rand0"] for r in per_item),
                  "geo_rand1": sum(r["dm"]["geo_rand1"] for r in per_item)}
    j_star = min([a for a in rand_flips if rand_flips[a] == max(rand_flips.values())])
    outmoves = dm_geo > rand_flips[j_star]
    # (f) path-noise: every geodesic-v1 flip is matched by a random path
    flip_geo = {r["id"] for r in per_item if r["dm"]["geo_v1"] == 1}
    flip_rand = {r["id"] for r in per_item
                 if r["dm"]["geo_rand0"] == 1 or r["dm"]["geo_rand1"] == 1}
    path_noise = dm_geo > 0 and flip_geo <= flip_rand
    random_null_holding = not path_noise
    # (g) PIVOT diagnostic: prompts with midpoint c^ (k in {2,3}) >= 0.1 on the v1 geodesic
    n_pivot = sum(1 for pid in prompt_ids
                  if max([c for c in (mid_cs[pid]["k2"], mid_cs[pid]["k3"])
                          if c is not None] or [-1.0]) >= 0.1)
    log("metrics: DM_geo=%d DM_oneshot=%d | McNemar(geo,base) (%s %d/%d) p_one=%.6f p_two=%.6f | "
        "McNemar(geo,oneshot) (b,c)=(%d,%d) p=%.6f" % (
            dm_geo, dm_oneshot, maj_dir, max(b_dir, c_dir), n_dir,
            p_geo_base, p_geo_base_twosided, b_ref, c_ref, p_geo_one))
    log("metrics: rank-trend %d/%d (bar %d) %s | best-random=%s (flips=%d) outmoves=%s | "
        "path_noise=%s | pivot_prompts=%d | c_geo_mean=%.4f" % (
            trend_hits, N_PROMPTS, trend_bar, "PASS" if rank_trend else "FAIL",
            j_star, rand_flips[j_star], outmoves, path_noise, n_pivot, c_geo_mean))

    # ---------------- 13. decision (§2 table, §4 order; KILL branches first per FIX-1) ----------------
    vi = {"c_geo_mean": c_geo_mean, "dm_geo": dm_geo, "mcnemar_p": p_geo_base,
          "rank_trend": rank_trend, "trend_hits": trend_hits,
          "outmoves_best_random": outmoves, "path_noise": path_noise,
          "random_null_holding": random_null_holding, "n_pivot_prompts": n_pivot,
          "dm_bagg": dm_bagg, "n_prompts": N_PROMPTS, "apparatus_void": None}
    verdict, reason = decision_tree(vi)
    log("=" * 70)
    log("VERDICT: %s" % verdict)
    log("reason: %s" % reason)
    log("=" * 70)

    _write_report(per_item, env, h_pre, h_post, B, c_geos, c_excl, c_oneshots, mid_cs,
                  h_bagg, h_npz, h_v2_1, h_v2_2, h_proto, h_amend, pin,
                  dm_geo, dm_oneshot, b_dir, c_dir, n_dir, maj_dir,
                  p_geo_base, p_geo_base_twosided, b_ref, c_ref, n_ref, p_geo_one,
                  trend_hits, trend_bar, rank_trend, j_star, rand_flips, outmoves,
                  path_noise, random_null_holding, n_pivot, c_geo_mean, dm_bagg,
                  verdict, reason)
    log("report written to out/exp133_report.json")
    log("raw records: out/exp133_records.json (+ .sha256 pin)")


def _write_records(per_item, env, h_pre, h_post, B, c_geos, c_excl, c_oneshots, mid_cs,
                   h_bagg, h_npz, h_v2_1, h_v2_2, h_proto, h_amend, meta):
    rec = {
        "experiment": "EXP133", "env": env,
        "pins": {"protocol": h_proto, "amendment": h_amend,
                 "weights_pre": h_pre, "weights_post": h_post,
                 "v1_npz": h_npz, "v2_run1": h_v2_1, "v2_run2": h_v2_2,
                 "bagg_reconstruction": h_bagg, "bench": BENCH_PIN},
        "budget_B": B, "alpha": B / GEO_K, "geodesic_K": GEO_K,
        "c_geo_per_prompt": c_geos, "c_geo_exclusions": c_excl,
        "c_oneshot_per_prompt_diagnostic": c_oneshots,
        "midpoint_c_per_prompt": mid_cs,
        "per_item": per_item, "meta": meta,
    }
    path = os.path.join(OUTDIR, "exp133_records.json")
    with open(path, "w") as fh:
        json.dump(rec, fh, indent=1, default=str)
    pin = sha256_file(path)
    with open(path + ".sha256", "w") as fh:
        fh.write(pin + "\n")
    return pin


def _write_report(per_item, env, h_pre, h_post, B, c_geos, c_excl, c_oneshots, mid_cs,
                  h_bagg, h_npz, h_v2_1, h_v2_2, h_proto, h_amend, pin,
                  dm_geo, dm_oneshot, b_dir, c_dir, n_dir, maj_dir,
                  p_geo_base, p_geo_base_twosided, b_ref, c_ref, n_ref, p_geo_one,
                  trend_hits, trend_bar, rank_trend, j_star, rand_flips, outmoves,
                  path_noise, random_null_holding, n_pivot, c_geo_mean, dm_bagg,
                  verdict, reason):
    rep = {
        "experiment": "EXP133", "verdict": verdict, "reason": reason,
        "metrics": {
            "dm_geo": dm_geo, "dm_oneshot_v1": dm_oneshot,
            "mcnemar_geo_base": {"b_E1toE2": b_dir, "c_E2toE1": c_dir, "n": n_dir,
                                 "majority_direction": maj_dir,
                                 "p_one_sided_majority": p_geo_base,
                                 "p_two_sided": p_geo_base_twosided},
            "mcnemar_geo_oneshot_ref": {"b": b_ref, "c": c_ref, "n": n_ref,
                                        "p_one_sided": p_geo_one},
            "rank_trend_hits": trend_hits, "rank_trend_bar": trend_bar,
            "rank_trend": rank_trend,
            "best_random_arm": j_star, "random_flips": rand_flips,
            "outmoves_best_random": outmoves,
            "path_noise": path_noise, "random_null_holding": random_null_holding,
            "pivot_prompts": n_pivot,
            "c_geo_mean": c_geo_mean, "c_geo_exclusions": c_excl,
            "dm_bagg_path": dm_bagg,
            "budget_B": B, "alpha": B / GEO_K, "geodesic_K": GEO_K,
        },
        "pins": {"protocol": h_proto, "amendment": h_amend,
                 "weights_pre": h_pre, "weights_post": h_post,
                 "v1_npz": h_npz, "v2_run1": h_v2_1, "v2_run2": h_v2_2,
                 "bagg_reconstruction": h_bagg, "bench": BENCH_PIN},
        "records_pin": pin, "env": env,
    }
    with open(os.path.join(OUTDIR, "exp133_report.json"), "w") as fh:
        json.dump(rep, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
