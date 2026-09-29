#!/usr/bin/env python3
"""EXP132 (DGF) executor — LOG-4743.

Directional-gain field: exact-JVP (forward-mode AD) directional gain of the
frozen Pythia-410m full layer-to-readout map along a fixed semantic probe and
K=8 seeded isotropic controls, all 24 layers, 10 pinned prompts.

$0 CPU. Delta-theta = 0 by construction: pure autograd JVPs through a frozen
model in eval mode; no optimizer, no loss, no backward pass into weights;
all parameter tensors carry requires_grad=False.

ZERO finite differences in any sensing primitive or verdict-bearing quantity.
The sole epsilon-bearing computation is the verdict-immaterial multi-epsilon
convergence diagnostic (gates the decision set only).

Falsification-tree order (Law #9): guards -> backbone pin -> probe/hash pins
-> convergence diagnostic -> JVP batches -> validity checks -> backbone
re-pin -> raw-record hash-pin -> metric (median DeltaGini) -> decision.

Exit codes: 0 = verdict reached; 42 = guard/pin failure (apparatus-void).
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
import transformers

# ---------------- Law #13 pins ----------------
PROTOCOL_PIN = "6963043b8bed628646520bf3a2eb15389c2740eb4b85d913a8a7bcf2202ec6cf"
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
BENCH_PIN = "e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5"
SITE = 21  # EXP077 support space: hidden_states[21] = output of block 20
WEIGHTS_DIR = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
BUNDLE_DIR = os.path.expanduser("~/workspace/SCBI/experiments/bundles/exp131_v1inj")
RUN_DIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(RUN_DIR, "out")
os.makedirs(OUTDIR, exist_ok=True)
LOGF = open(os.path.join(OUTDIR, "exp132_console.log"), "a")

PROTOCOL_CANDIDATES = [
    os.path.expanduser("~/workspace/SCBI/research/prereg/EXP_PREREG_DGF_GAINFIELD_2026-09-29.md"),
]

N_PROMPTS = 10
N_LAYERS = 24
K_ISO = 8
SEED_BASE = 20260929
DIAG_LAYERS = [0, 11, 23]
DIAG_EPS = [1e-6, 1e-7, 1e-8]
DIAG_TOL = 0.25
NORM_TOL = 1e-6
CAP_PER_PROMPT = 1000
CAP_TOTAL = 40000


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
    sha = hashlib.sha256()
    sd = model.state_dict()
    for k in sorted(sd.keys()):
        sha.update(np.asarray(sd[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()


def gini(xs):
    """Standard Gini coefficient over non-negative values (executor-computed)."""
    xs = np.asarray(xs, dtype=np.float64)
    n = len(xs)
    m = xs.mean()
    if m == 0.0:
        return None  # degenerate: caller routes to apparatus-void for that prompt
    xs = np.sort(xs)
    idx = np.arange(1, n + 1)
    return float((2.0 * np.sum(idx * xs)) / (n * np.sum(xs)) - (n + 1.0) / n)


def median_executor(vals):
    s = sorted(vals)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="code-path test only: 1 prompt, 3 layers, no verdict")
    args = ap.parse_args()
    SMOKE = args.smoke
    t0 = time.time()

    # ---------------- 0. guards: protocol pin ----------------
    proto = next((c for c in PROTOCOL_CANDIDATES if os.path.isfile(c)), None)
    if proto is None:
        log("HALT: protocol file not found.")
        sys.exit(42)
    h_proto = sha256_file(proto)
    if h_proto != PROTOCOL_PIN:
        log("HALT: protocol hash mismatch: %s" % h_proto)
        sys.exit(42)
    log("protocol pin OK (post-fix LOG-4740 revision)")

    sys.path.insert(0, BUNDLE_DIR)
    from build_exp107_bench import build_bench, bench_sha256  # noqa: E402
    from exp077_support import support_prompts, build_candidate_directions, VOCAB_KEYS  # noqa: E402

    # ---------------- 1. prompts: bench build + pin, pinned 10 ids ----------------
    bench = build_bench()
    assert len(bench) == 60
    h_bench = bench_sha256(bench)
    log("bench sha256: %s" % h_bench)
    if h_bench != BENCH_PIN:
        log("HALT: bench hash mismatch.")
        sys.exit(42)
    EXPECTED_IDS = [
        "exp107_flip_exp077_planet_2hop_0", "exp107_ctrl_exp077_planet_2hop_1",
        "exp107_flip_exp077_planet_2hop_2", "exp107_ctrl_exp077_planet_2hop_3",
        "exp107_flip_exp077_planet_2hop_4", "exp107_ctrl_exp077_planet_2hop_5",
        "exp107_flip_exp077_planet_2hop_6", "exp107_ctrl_exp077_planet_2hop_7",
        "exp107_ctrl_exp077_planet_2hop_8", "exp107_flip_exp077_planet_2hop_9",
    ]
    prompts = bench[:N_PROMPTS]
    prompt_ids = [b["id"] for b in prompts]
    if prompt_ids != EXPECTED_IDS:
        log("HALT: prompt id list mismatch vs protocol §3.1: %s" % prompt_ids)
        sys.exit(42)
    log("prompts: 10 pinned ids verified (protocol §3.1)")

    # ---------------- 2. environment ----------------
    torch.manual_seed(SEED_BASE)
    np.random.seed(SEED_BASE)
    env = {"torch": torch.__version__, "transformers": transformers.__version__,
           "numpy": np.__version__, "device": "cpu", "threads": torch.get_num_threads(),
           "smoke": SMOKE, "protocol_pin": h_proto, "bench_pin": h_bench}
    log("env: %s" % json.dumps(env))

    # ---------------- 3. frozen backbone ----------------
    model = transformers.AutoModelForCausalLM.from_pretrained(
        WEIGHTS_DIR, local_files_only=True, trust_remote_code=False,
        torch_dtype=torch.float32, output_hidden_states=True, output_attentions=False,
        attn_implementation="eager")  # eager: the CPU sdpa/flash backend has no backward
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)
    blocks = model.gpt_neox.layers
    final_ln = model.gpt_neox.final_layer_norm
    rotary_emb = model.gpt_neox.rotary_emb
    cfg = model.config
    assert len(blocks) == 24
    # readout site (protocol §3.3, FIX-6): x_{24,last}, the final-token residual
    # at the input to the unembedding (post-final-LayerNorm) — EXP128's
    # registered readout site (its pre-reg §3.1; executor's double-norm was
    # a latent bug, the registered object is the single-norm tensor).
    h_pre = state_dict_hash(model)
    log("backbone LOG-331 pin (pre): %s" % h_pre)
    if h_pre != WEIGHTS_PIN:
        log("RUN-INVALID: backbone hash mismatch before first forward. No metric exists.")
        sys.exit(42)
    log("backbone pin OK. Delta-theta guard armed.")
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        WEIGHTS_DIR, local_files_only=True, trust_remote_code=False)

    # ---------------- 4. semantic probe: deterministic EXP077 support-set derivation ----------------
    sup_items = list(support_prompts())
    delta_h_by_vocab = {vk: [] for vk in VOCAB_KEYS}
    h_all = []
    with torch.no_grad():
        for sid, p_rel, p_neu in sup_items:
            ids_rel = tokenizer.encode(p_rel, return_tensors="pt")
            ids_neu = tokenizer.encode(p_neu, return_tensors="pt")
            o_rel = model(input_ids=ids_rel, output_hidden_states=True)
            o_neu = model(input_ids=ids_neu, output_hidden_states=True)
            h_rel = o_rel.hidden_states[SITE][0, -1, :].detach().cpu()
            h_neu = o_neu.hidden_states[SITE][0, -1, :].detach().cpu()
            vk = next(k for k in VOCAB_KEYS if sid.startswith("sup_" + k + "_"))
            delta_h_by_vocab[vk].append(h_rel - h_neu)
            h_all.extend([h_rel, h_neu])
    for vk in VOCAB_KEYS:
        delta_h_by_vocab[vk] = torch.stack(delta_h_by_vocab[vk])
    assert len(h_all) == 300, "expected 300 support presentations, got %d" % len(h_all)
    cand = build_candidate_directions(delta_h_by_vocab, h_all)
    u_sem = cand["v_hat"].detach().float()
    assert u_sem.shape == (1024,)
    h_probe = hashlib.sha256(u_sem.numpy().astype(np.float32).tobytes()).hexdigest()
    log("semantic probe derived (EXP077 support-set recipe); sha256: %s" % h_probe)
    log("support continuity diagnostic mean_cos_v1=%.4f" % cand["mean_cos_v1"])
    del h_all, delta_h_by_vocab

    # ---------------- 5. base forwards (capture full-sequence layer inputs) ----------------
    seq_states = []  # per prompt: list of 25 hidden-state tensors [1,seq,1024]
    with torch.no_grad():
        for b in prompts:
            ids = tokenizer.encode(b["prompt"], return_tensors="pt")
            o = model(input_ids=ids, output_hidden_states=True)
            seq_states.append([h.detach() for h in o.hidden_states])
    assert all(len(hs) == 25 for hs in seq_states)
    log("base forwards complete: %d prompts" % len(prompts))

    # ---------------- 5b. validity check (a): probe unit-norm audit (pre-JVP) ----------------
    def unit_audit(v, name):
        d = abs(float(v.norm().item()) - 1.0)
        if d > NORM_TOL:
            log("apparatus-void: unit-norm audit failed for %s (|n|-1|=%.2e)" % (name, d))
            sys.exit(42)

    unit_audit(u_sem, "semantic probe")
    iso_probes = []
    for pi in range(N_PROMPTS):
        g = torch.Generator().manual_seed(SEED_BASE + pi)
        probes = []
        for j in range(K_ISO):
            v = torch.randn(1024, generator=g)
            v = v / (v.norm() + 1e-12)
            unit_audit(v, "iso probe p%d j%d" % (pi, j))
            probes.append(v)
        iso_probes.append(probes)
    log("validity check (a): unit-norm audit passed (1 semantic + %d iso probes)" % (N_PROMPTS * K_ISO))

    from transformers.cache_utils import DynamicCache  # noqa: E402
    from transformers.masking_utils import create_causal_mask  # noqa: E402

    rotary_emb = model.gpt_neox.rotary_emb

    def model_mask(h):
        """The model's own mask construction (GPTNeoXModel.forward): a fresh
        DynamicCache (use_cache default) materializes the 4D causal mask;
        passing it explicitly keeps eager attention causal."""
        return create_causal_mask(
            config=cfg, inputs_embeds=h, attention_mask=None,
            past_key_values=DynamicCache(config=cfg),
            position_ids=torch.arange(h.shape[1]).unsqueeze(0).to(h.device))

    def make_g(seq_l, l):
        """g_l: final-token residual at layer l -> readout x_{24,last}
        (post-final-LayerNorm input to the unembedding — protocol §3.3).
        Attention recomputed, context unclamped."""
        prefix = seq_l[:, :-1, :].detach()
        seq_len = seq_l.shape[1]
        position_ids = torch.arange(seq_len).unsqueeze(0)

        def g(y):
            h = torch.cat([prefix, y.unsqueeze(0).unsqueeze(0)], dim=1)
            h = h.to(dtype=seq_l.dtype)
            pos_emb = rotary_emb(h, position_ids=position_ids.to(h.device))
            mask = model_mask(h)
            for blk in blocks[l:]:
                h = blk(h, attention_mask=mask, position_ids=position_ids.to(h.device),
                        position_embeddings=pos_emb)
            h = final_ln(h)
            return h[0, -1, :]

        return g

    n_products = 0
    diag_records = []  # verdict-immaterial instrument-health records

    # ---------------- 6. multi-epsilon convergence diagnostic (float64, verdict-immaterial) ----------------
    log("converting model to float64 for the convergence diagnostic...")
    model.double()
    diag_pass = []
    layers_diag = DIAG_LAYERS if not SMOKE else [0]
    for pi, b in enumerate(prompts):
        if SMOKE and pi > 0:
            break
        seq64 = [h.double() for h in seq_states[pi]]
        probes_all = [("sem", u_sem.double())] + [("iso%d" % j, iso_probes[pi][j].double())
                                                  for j in range(K_ISO)]
        ok = True
        for pname, u in probes_all:
            for l in layers_diag:
                g = make_g(seq64[l], l)
                y_l = seq64[l][0, -1, :]
                with torch.enable_grad():
                    _, jv = torch.autograd.functional.jvp(g, (y_l,), (u,))
                jvp_norm = float(jv.norm().item())
                n_products += 1
                for eps in DIAG_EPS:
                    with torch.no_grad():
                        fwd_p = g(y_l + eps * u)
                        fwd_0 = g(y_l)
                    f_eps = float((fwd_p - fwd_0).norm().item()) / eps
                    rel = abs(f_eps - jvp_norm) / (jvp_norm + 1e-30)
                    n_products += 1.5
                    diag_records.append({"prompt": b["id"], "probe": pname, "layer": l,
                                         "eps": eps, "F": f_eps, "JVP": jvp_norm, "rel": rel})
                    if rel > DIAG_TOL:
                        ok = False
        diag_pass.append(ok)
        log("diagnostic prompt %s: %s" % (b["id"], "PASS" if ok else "FAIL (excluded)"))
    model.float()
    h_mid = state_dict_hash(model)
    if h_mid != WEIGHTS_PIN:
        log("RUN-INVALID: backbone hash mismatch after float64 round-trip.")
        sys.exit(42)
    log("model restored to float32; backbone hash re-verified after round-trip.")

    decision_idx = [i for i, ok in enumerate(diag_pass) if ok]
    n_d = len(decision_idx)
    log("decision set: %d/%d prompts passed the diagnostic" % (n_d, N_PROMPTS))
    if n_d < 8 and not SMOKE:
        log("apparatus-void: fewer than 8 diagnostic-passing prompts. Hypothesis UNTESTED.")
        sys.exit(42)

    # ---------------- 7. JVP batches: exact directional-gain field ----------------
    # S_l^*(u) = || Dg_l(y_l) . u ||_2, float32, forward-mode AD only.
    field = {}  # (pi, probe_name) -> [24 floats]
    layers_all = list(range(N_LAYERS)) if not SMOKE else [0, 11, 23]
    for pi in decision_idx:
        b = prompts[pi]
        probes_all = [("sem", u_sem)] + [("iso%d" % j, iso_probes[pi][j]) for j in range(K_ISO)]
        for pname, u in probes_all:
            vals = []
            for l in layers_all:
                g = make_g(seq_states[pi][l], l)
                y_l = seq_states[pi][l][0, -1, :]
                with torch.enable_grad():
                    _, jv = torch.autograd.functional.jvp(g, (y_l,), (u,))
                s = float(jv.norm().item())
                vals.append(s)
                n_products += 1
                if not math.isfinite(s):
                    log("apparatus-void: non-finite JVP output (prompt %s, probe %s, layer %d)"
                        % (b["id"], pname, l))
                    sys.exit(42)
            field[(pi, pname)] = vals
        # degenerate-field check: all-zero field -> apparatus-void for that prompt
        for pname, _ in probes_all:
            if all(v == 0.0 for v in field[(pi, pname)]):
                log("apparatus-void: degenerate all-zero field (prompt %s, probe %s)"
                    % (b["id"], pname))
                sys.exit(42)
    log("JVP batches complete: %d prompts x %d layers x 9 probes" % (n_d, len(layers_all)))

    # ---------------- 7b. validity check (c): seed/pin audit ----------------
    assert h_probe == hashlib.sha256(u_sem.numpy().astype(np.float32).tobytes()).hexdigest()
    log("validity check (c): probe pin matches manifest; seeds = %d + prompt index" % SEED_BASE)

    # ---------------- 8. backbone re-pin (post) ----------------
    h_post = state_dict_hash(model)
    log("backbone LOG-331 pin (post): %s" % h_post)
    if h_post != WEIGHTS_PIN:
        log("RUN-INVALID: backbone hash mismatch after last forward. No metric exists.")
        sys.exit(42)

    # ---------------- 9. metric ----------------
    gini_sem, gini_iso_med, delta = [], [], []
    for pi in decision_idx:
        gs = gini(field[(pi, "sem")])
        assert gs is not None
        gisos = [gini(field[(pi, "iso%d" % j)]) for j in range(K_ISO)]
        assert all(x is not None for x in gisos)
        gi_med = median_executor(gisos)
        gini_sem.append(gs)
        gini_iso_med.append(gi_med)
        delta.append(gs - gi_med)
    med_delta = median_executor(delta)
    med_giso = median_executor(gini_iso_med)
    log("median DeltaGini = %.6f ; median Gini_iso = %.6f (n_d=%d)" % (med_delta, med_giso, n_d))

    # ---------------- 10. raw-record hash-pin (BEFORE decision read... records written now) ----------------
    records = {
        "experiment": "EXP132", "lane": "LOG-4743",
        "protocol_pin": h_proto, "backbone_pre": h_pre, "backbone_post": h_post,
        "bench_pin": h_bench, "prompt_ids": [prompts[i]["id"] for i in decision_idx],
        "probe_sha256": h_probe, "probe_kind": "EXP077 support-set v_hat (Law #2-honest recipe)",
        "env": env,
        "diagnostic": {"layers": layers_diag, "eps": DIAG_EPS, "tol": DIAG_TOL,
                       "pass": [prompts[i]["id"] for i in decision_idx],
                       "fail": [prompts[i]["id"] for i in range(len(diag_pass)) if i not in decision_idx],
                       "records": diag_records},
        "field": {prompts[pi]["id"] + "/" + pn: vals for (pi, pn), vals in field.items()},
        "gini_sem": gini_sem, "gini_iso_med": gini_iso_med, "delta_gini": delta,
        "median_delta_gini": med_delta, "median_gini_iso": med_giso, "n_d": n_d,
        "n_products": n_products,
        "budget": {"per_prompt_cap": CAP_PER_PROMPT, "total_cap": CAP_TOTAL},
    }
    rec_path = os.path.join(OUTDIR, "exp132_records.json")
    with open(rec_path, "w") as fh:
        json.dump(records, fh, sort_keys=True)
    pin = sha256_file(rec_path)
    with open(rec_path + ".sha256", "w") as fh:
        fh.write(pin + "\n")
    log("raw-record hash-pin: %s (minted before the decision read)" % pin)
    if n_products > CAP_TOTAL:
        log("apparatus-void: total budget cap exceeded (%d > %d)" % (n_products, CAP_TOTAL))
        sys.exit(42)

    # ---------------- 11. decision (bars verbatim from the pre-reg §4) ----------------
    verdict = None
    if med_delta >= 0.2 and med_giso < 0.4:
        verdict = "CONTINUE"
    elif med_delta <= 0:
        verdict = "KILL"
    elif med_giso >= 0.4:
        verdict = "KILL-as-premise"
    elif 0 < med_delta < 0.2 and med_giso < 0.4:
        verdict = "HELD"
    else:
        verdict = "UNDECIDED-TREE-GAP"
    log("VERDICT: %s" % verdict)

    # ---------------- 12. report ----------------
    rep_path = os.path.expanduser(
        "~/workspace/SCBI/research/experiments/EXP132_DGF_GAINFIELD_REPORT_2026-09-29.md")
    with open(rep_path, "w") as fh:
        fh.write("# Execution Report: EXP132 — ε-Free Directional-Gain Field\n\n")
        fh.write("**Lane:** LOG-4743. **License:** CEO launch decision LOG-4741; ")
        fh.write("pre-reg post-fix sha256 `%s`.\n\n" % PROTOCOL_PIN)
        fh.write("## Verdict\n\n**%s**\n\n" % verdict)
        fh.write("| Statistic | Executor-computed value |\n|---|---|\n")
        fh.write("| median ΔGini (decision set) | %.6f |\n" % med_delta)
        fh.write("| median Ḡini_iso (decision set) | %.6f |\n" % med_giso)
        fh.write("| decision-set size n_d | %d |\n" % n_d)
        fh.write("| per-prompt ΔGini | %s |\n" % ", ".join("%.4f" % d for d in delta))
        fh.write("| per-prompt Ḡini_iso | %s |\n" % ", ".join("%.4f" % x for x in gini_iso_med))
        fh.write("| raw-record SHA-256 pin | `%s` |\n" % pin)
        fh.write("| autograd product-equivalents | %d (cap %d/prompt, %d total) |\n"
                 % (n_products, CAP_PER_PROMPT, CAP_TOTAL))
        fh.write("| diagnostic pass | %d/%d prompts (tol %.2f) |\n" % (n_d, N_PROMPTS, DIAG_TOL))
        fh.write("\n## Decision-tree walk (code order)\n\n")
        fh.write("1. Backbone LOG-331 pin (pre): `%s` — MATCH.\n" % h_pre)
        fh.write("2. Prompt set: 10 pinned ids — PASS.\n")
        fh.write("3. Probe provenance: EXP077 support-set recipe, SHA-256 `%s` recorded pre-JVP — PASS.\n" % h_probe)
        fh.write("4. Multi-ε convergence diagnostic: %d/10 prompts passed (≥8 required) — %s.\n"
                 % (n_d, "PASS" if n_d >= 8 else "apparatus-void"))
        fh.write("5. Isotropic controls (K=8, seeded): present on every decision-set prompt — PASS.\n")
        fh.write("6. JVP batches (24 layers × 9 probes × %d prompts): present — PASS.\n" % n_d)
        fh.write("7. Backbone LOG-331 pin (post): `%s` — MATCH.\n" % h_post)
        fh.write("8. Raw records hash-pinned: `%s` — PASS.\n" % pin)
        fh.write("9. median ΔGini = %.6f; median Ḡini_iso = %.6f — §4 bars → **%s**.\n"
                 % (med_delta, med_giso, verdict))
        fh.write("\n## Honest frame\n\n")
        fh.write("- [CHARACTERIZATION ONLY] This experiment measures the infinitesimal ")
        fh.write("directional-gain field (regime ~3 orders of magnitude below feasible injection ")
        fh.write("budgets). No targeting claim is licensed; Family B's targeting mission stays UNTESTED.\n")
        fh.write("- One semantic probe direction tested (EXP077's v_hat); the KILL license is qualified ")
        fh.write("to the registered probe direction.\n")
        fh.write("- A CONTINUE licenses further characterization only — not a steering claim; the ")
        fh.write("capability scoreboard stays at zero positive signals for autonomous steering.\n")
        fh.write("- No generality beyond Pythia-410m, the full-map linearization, and the 10 pinned prompts.\n")
        fh.write("- Δθ=0 verified by LOG-331 pre/post pins; no labels anywhere (Law #7 clean).\n")
    log("report: %s" % rep_path)
    log("elapsed: %.1f min" % ((time.time() - t0) / 60.0))
    return verdict, med_delta


if __name__ == "__main__":
    main()
