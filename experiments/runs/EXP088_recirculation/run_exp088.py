#!/usr/bin/env python3
"""EXP088 runner: recirculation directional-leak discrimination (GPU node only).

Implements the signed protocol
experiments/protocols/EXP088_RECIRCULATION_PREREG_SIGNED.md
(Law #14 final SIGN LOG-310; CEO signing LOG-312).

Stage A — (s, d) perplexity screen: 9 pairs (d in {4,6,8}, s = d + {4,6,8}),
alpha = 0.10, convex norm-matched leak (paper Eq. 2) with the pinned F8
ramping schedule, on the pinned ~50k-token corpus. F7 INVALID gate: no pair
with strictly-positive mean perplexity reduction beyond the corpus noise
floor (two no-recirculation repeat runs; pinned default eps = 0 if
unmeasurable) -> INVALID verdict, do not proceed.

Stage B — directional discrimination at (s*, d*): alpha in {0.07, 0.10,
0.15}, leak directions {D->S, S->D, RAND (F2 compute-matched: destination
pin d*, fixed random unit vector drawn once per run with pinned seed,
scaled to destination norm, same rerun span d*+1..L as D->S)} +
no-recirculation baseline, on the fixed N=60 probe set (F11). Primary
contrast (F4): paired D->S-vs-S->D correctness at alpha = 0.10 — McNemar
exact one-sided (p <= 0.05) + two-sided 95% Tango CI. Verdict precedence in
exp088_endpoints.adjudicate (binding section-G1b mapping; B2/F6 curve
override; the B4-vs-F5 tension is flagged, not silently resolved).

Frozen backbone (Laws #6/#13): SHA-256 over state_dict tensors (sorted
keys, CPU, float32 bytes — the EXP077/EXP084 tensor-bytes-only convention)
before the first pass and after the last pass; mismatch -> DeltaThetaError
(verdict-clean halt). All parameters requires_grad_(False); no optimizer
exists anywhere in this file.

Pass budget (binding): 1640 forward calls total —
  Stage A: 20 corpus-passes x 25 blocks = 500 calls
           (2 baseline repeats for the F7 noise floor + 9 pairs x
           (capture + inject) recirculated passes)
  Stage B: 60 baseline + 540 recirculated evaluations x 2 = 1140 calls
           (3 alphas x 3 directions x 60 items x 2 passes + 60 baseline)
The runner REFUSES call 1641 (hard stop). No backward passes anywhere.

GPU-NODE ONLY: requires torch + transformers + CUDA + the pinned corpus
artifact + the pinned probe records. Does NOT run on the CPU build machine
(raises/refuses without torch). The --run path additionally requires BOTH
--ceo-gpu-clearance AND --bundle-review-signoff (exit 2 otherwise).
"""

import argparse
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import time

# --- Signed pins -------------------------------------------------------------
MODEL_ID = "EleutherAI/pythia-410m"
N_LAYERS = 24            # Pythia-410m depth (0-indexed layers 0..23)
HIDDEN = 1024            # Pythia-410m hidden size

# Stage A grid (signed section 5): d in {4,6,8}, s = d + {4,6,8}.
D_GRID = (4, 6, 8)
S_OFFSETS = (4, 6, 8)
ALPHA_STAGE_A = 0.10

# Stage B (signed section 5).
STAGE_B_ALPHAS = (0.07, 0.10, 0.15)
ALPHA_LEAK = 0.10        # pinned primary leak coefficient (F4)
N_ITEMS = 60

# Corpus (pinned at build).
CORPUS_N_TOKENS = 50000
CORPUS_BLOCK = 2048      # -> 25 blocks (last partial)
# SHA-256 of the pinned token-id sequence (comma-joined ASCII ids), recorded
# by tools/build_stageA_corpus.py and transcribed here at build. The startup
# preflight refuses to run if the artifact's ids do not hash to this pin.
# Build 2026-09-24: wikitext/wikitext-103-raw-v1/validation (first 50,000 of
# 250,011 tokens from 3,760 rows), Pythia-410m tokenizer.
CORPUS_TOKEN_IDS_SHA256 = (
    "4206c056e87b209c1f47d3230138e5e2ce7b79697a8fa2a03a6a7442ff4bada7")

# Pass budget: forward CALLS (one block-forward or one item-forward each).
# Stage A: 20 corpus-passes x 25 blocks = 500; Stage B: 1140. Total 1640.
# (2 baseline repeats x 25 x 1 + 9 pairs x 25 x 2 capture/inject passes.)
STAGE_A_CALLS = 20 * 25
STAGE_B_CALLS = 60 + 540 * 2
FWD_BUDGET = STAGE_A_CALLS + STAGE_B_CALLS
assert FWD_BUDGET == 1640

# Program master seed (Law #13); F2 RAND vector draw seed.
MASTER_SEED = 20260924
RAND_SEED = 20260924

# Historical program weight pin (EXP084 section 1, same model id). REFERENCE
# ONLY for EXP088 — the signed protocol requires pre/post logging (Law #13),
# not this pin. A mismatch vs the historical pin is LOUD-WARNED (different
# weight revision than the program's pinned one) but does not halt; the
# binding guard is pre == post (DeltaThetaError otherwise).
HISTORICAL_SHA256 = ("4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp088_endpoints as E
import exp088_probeset as P
import exp088_ramping as RP
import exp088_rng as R


class PassBudget:
    """Hard forward-call counter. Refuses to exceed the signed ceiling."""

    def __init__(self, limit=FWD_BUDGET):
        self.limit = limit
        self.used = 0

    def charge(self, n=1):
        if self.used + n > self.limit:
            raise RuntimeError(
                f"PASS CEILING REFUSED: forward calls {self.used}+{n} > "
                f"{self.limit}. Signed budget is {self.limit} forward calls; "
                f"call {self.limit + 1} is refused.")
        self.used += n


def sha256_state_dict(model):
    """SHA-256 over state_dict tensors (sorted keys, CPU, float32 bytes).

    Byte convention: tensors ONLY (no key names) — matches the historical
    EXP077/EXP084 hashing code, which produced the pinned hash
    4c242d9a...48dd. Hashing key names as well would NOT reproduce the pin.
    """
    import torch
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu().to(torch.float32)
        h.update(t.numpy().tobytes())
    return h.hexdigest()


class DeltaThetaError(RuntimeError):
    """Frozen-backbone violation: post-run hash != pre-run hash (Laws #6/#13).

    Verdict-clean halt: no verdict is emitted."""


class ApparatusError(RuntimeError):
    """Apparatus failure outside the verdict table (fail loud, no verdict).

    Used for protocol-silence cases where construction is impossible:
    missing/unverifiable corpus artifact, zero-norm source activation,
    invalid leak geometry, etc. Never silently worked around."""


# --- Leak specification --------------------------------------------------------
# A leak spec is a dict:
#   {"kind": "D2S"}            deep source s -> shallow destination d
#   {"kind": "S2D"}            shallow source d* -> deep destination s*
#   {"kind": "RAND"}           fixed random unit vector -> destination d*
# plus "s", "d", "alpha". For RAND, "s" is None (source replaced by the
# once-per-run fixed vector, scaled to ||h_d|| at injection time).
#
# The leak operator (paper Eq. 2, convex norm-matched mixture, D2):
#   h_dst^new(t) = a_t * (||h_dst(t)|| / ||h_src(t)||) * h_src(t)
#                  + (1 - a_t) * h_dst(t)
# with the F8 ramping schedule a_t = alpha_eff(alpha, t), t 1-indexed.
# RAND: h_src(t) is replaced by u (unit norm), so the norm-matching factor
# is 1 and the injection is a_t * ||h_dst(t)|| * u + (1 - a_t) * h_dst(t).
# One recirculation iteration = apply the leak at layer d, then run layers
# d+1..L a second time (two forward passes per recirculated evaluation).

def _check_leak_geometry(spec):
    kind, s, d = spec["kind"], spec.get("s"), spec["d"]
    if kind not in ("D2S", "S2D", "RAND"):
        raise ApparatusError(f"unknown leak kind {kind!r}")
    if not 0 <= d < N_LAYERS:
        raise ApparatusError(f"destination layer d={d} outside [0,{N_LAYERS})")
    if kind == "D2S":
        if not (s is not None and 0 <= s < N_LAYERS and s > d):
            raise ApparatusError(
                f"D2S needs a deep source s > d (got s={s}, d={d})")
    elif kind == "S2D":
        if not (s is not None and 0 <= s < N_LAYERS and s < d):
            raise ApparatusError(
                f"S2D needs a shallow source s < d (got s={s}, d={d})")
    # RAND: s is None by construction; destination d checked above.


def leak_destination_layer(spec):
    """Layer index where the leak is injected (the rerun starts after it)."""
    return spec["d"]


# --- Backend interface ---------------------------------------------------------
# A backend implements:
#   state_hash() -> hex str                                   (no pass charged)
#   corpus_block_nlls(token_ids, leak_spec)
#       -> list[float] per-token NLLs (tokens 1..T-1 predicted from 0..T-2).
#       leak_spec None: 1 forward call. Else: 2 forward calls.
#   probe_answer_logits(item, leak_spec) -> (logit_A, logit_C)
#       item: {prompt, A, C}. leak_spec None: 1 forward call. Else: 2.
#       Logits are the last-position logits at the first-token ids of
#       " "+A and " "+C (EXP077 section 4 decision rule; the runner applies
#       decide_from_logits).
#   rand_unit_vector() -> opaque vector, drawn ONCE per run (F2).
# The runner charges the PassBudget; backends must not double-charge.

class TorchBackend:
    """Live Pythia-410m backend (GPU node only).

    Residual-stream hooks on the source and destination layers. Pass 1
    captures h_src / h_dst at every position; pass 2 injects the leak at the
    destination layer (per-position F8 ramping) and runs layers d+1..L on the
    modified stream; readouts come from pass 2. No optimizer exists; every
    parameter has requires_grad_(False), so weight gradients are impossible
    by construction (DeltaTheta = 0 beyond the SHA-256 pre/post guard).
    Greedy/deterministic throughout: no sampling randomness in any forward.
    """

    def __init__(self, budget, log):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.budget = budget
        self.log = log
        torch.use_deterministic_algorithms(True)
        if not torch.cuda.is_available():
            raise ApparatusError(
                "TorchBackend requires CUDA (GPU-node only); refusing silent "
                "CPU execution")
        self.device = "cuda"
        log(f"loading {MODEL_ID} ...")
        self.tok = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
        self.model.to(self.device)
        self.model.eval()
        for p in self.model.parameters():
            p.requires_grad_(False)
        self._layers = self.model.gpt_neox.layers
        if len(self._layers) != N_LAYERS:
            raise ApparatusError(
                f"model has {len(self._layers)} layers, expected {N_LAYERS}")
        # Hook state (per forward call).
        self._cap_src = None
        self._cap_dst = None
        self._inject = None   # (dst_layer, src_tensor|None, dst_tensor|None, u|None, alphas)
        self._hook_handles = []
        self._rand_vec = None
        # Token ids for " A"/" C" first tokens are resolved per item.
        log("model loaded on cuda; params frozen (requires_grad_(False)); "
            "eval mode; deterministic algorithms on")

    # -- hooks --
    def _clear_hooks(self):
        for h in self._hook_handles:
            h.remove()
        self._hook_handles = []

    def _capture_hook(self, slot):
        def fn(module, inputs, output):
            x = output[0] if isinstance(output, tuple) else output
            if slot == "src":
                self._cap_src = x.detach()
            else:
                self._cap_dst = x.detach()
        return fn

    def _inject_hook(self, dst_layer, src, dst, u, alphas):
        torch = self.torch
        def fn(module, inputs, output):
            x = output[0] if isinstance(output, tuple) else output
            h = x.clone()
            T = h.shape[1]
            a = torch.tensor(alphas[:T], device=h.device, dtype=h.dtype
                             ).view(1, T, 1)
            hd = dst[:, :T, :] if dst is not None else h
            if u is not None:
                # RAND: norm-matched by construction (u unit norm).
                src_scaled = u.view(1, 1, -1).expand(1, T, -1) * \
                    hd.norm(dim=-1, keepdim=True)
            else:
                hs = src[:, :T, :]
                n_src = hs.norm(dim=-1, keepdim=True)
                n_dst = hd.norm(dim=-1, keepdim=True)
                if bool((n_src == 0).any()):
                    raise ApparatusError(
                        "zero-norm source activation at some position — "
                        "norm-matching undefined; halting loud")
                src_scaled = hs * (n_dst / n_src)
            h_new = a * src_scaled + (1.0 - a) * hd
            h = h.clone()
            h[:, :T, :] = h_new
            if isinstance(output, tuple):
                return (h,) + tuple(output[1:])
            return h
        return fn

    def _run_capture_pass(self, input_ids, src_layer, dst_layer):
        """Pass 1: capture residual streams at src and dst layers."""
        self._cap_src, self._cap_dst = None, None
        self._clear_hooks()
        self._hook_handles.append(
            self._layers[src_layer].register_forward_hook(
                self._capture_hook("src")))
        if dst_layer != src_layer:
            self._hook_handles.append(
                self._layers[dst_layer].register_forward_hook(
                    self._capture_hook("dst")))
        else:
            self._cap_dst = "alias"
        with self.torch.no_grad():
            out = self.model(input_ids=input_ids)
        self.budget.charge(1)
        src = self._cap_src
        dst = self._cap_dst if self._cap_dst != "alias" else self._cap_src
        self._clear_hooks()
        return out, src, dst

    def _run_inject_pass(self, input_ids, spec, src, dst):
        """Pass 2: inject the leak at the destination layer; read out."""
        torch = self.torch
        T = input_ids.shape[1]
        alphas = RP.ramp_vector(spec["alpha"], T)
        u = None
        src_t = src
        if spec["kind"] == "RAND":
            u = self.rand_unit_vector().to(self.device)
            src_t = None
        self._clear_hooks()
        self._hook_handles.append(
            self._layers[spec["d"]].register_forward_hook(
                self._inject_hook(spec["d"], src_t, dst, u, alphas)))
        with torch.no_grad():
            out = self.model(input_ids=input_ids)
        self.budget.charge(1)
        self._clear_hooks()
        return out

    # -- backend interface --
    def state_hash(self):
        return sha256_state_dict(self.model)

    def rand_unit_vector(self):
        if self._rand_vec is None:
            self._rand_vec = R.draw_rand_unit_vector(HIDDEN, seed=RAND_SEED)
            self.log(f"F2 RAND unit vector drawn once (seed={RAND_SEED}, "
                     f"dim={HIDDEN})")
        return self._rand_vec

    def _leak_layers(self, spec):
        """(capture_src_layer, destination_layer) for a leak spec."""
        if spec["kind"] == "D2S":
            return spec["s"], spec["d"]
        if spec["kind"] == "S2D":
            return spec["s"], spec["d"]   # shallow source, deep destination
        return None, spec["d"]            # RAND: destination only

    def corpus_block_nlls(self, token_ids, leak_spec):
        """Per-token NLLs for one corpus block (tokens[1:] from tokens[:-1])."""
        torch = self.torch
        ids = torch.tensor([token_ids], dtype=torch.long, device=self.device)
        if leak_spec is None:
            with torch.no_grad():
                out = self.model(input_ids=ids)
            self.budget.charge(1)
            logits = out.logits[0]
        else:
            _check_leak_geometry(leak_spec)
            src_layer, dst_layer = self._leak_layers(leak_spec)
            cap_src = src_layer if src_layer is not None else dst_layer
            _, src, dst = self._run_capture_pass(ids, cap_src, dst_layer)
            out = self._run_inject_pass(ids, leak_spec, src, dst)
            logits = out.logits[0]
        logp = torch.log_softmax(logits[:-1, :], dim=-1)
        tgt = torch.tensor(token_ids[1:], dtype=torch.long, device=self.device)
        nlls = (-logp[torch.arange(len(token_ids) - 1), tgt]).detach().cpu()
        return [float(v) for v in nlls]

    def probe_answer_logits(self, item, leak_spec):
        """(logit_A, logit_C) at the last position (EXP077 section 4 rule)."""
        torch = self.torch
        ids = self.tok(item["prompt"], return_tensors="pt").to(self.device)
        toks_A = self.tok.encode(" " + item["A"])[0]
        toks_C = self.tok.encode(" " + item["C"])[0]
        if leak_spec is None:
            with torch.no_grad():
                out = self.model(**ids)
            self.budget.charge(1)
            last = out.logits[0, -1, :]
        else:
            _check_leak_geometry(leak_spec)
            src_layer, dst_layer = self._leak_layers(leak_spec)
            cap_src = src_layer if src_layer is not None else dst_layer
            _, src, dst = self._run_capture_pass(ids["input_ids"],
                                                 cap_src, dst_layer)
            out = self._run_inject_pass(ids["input_ids"], leak_spec, src, dst)
            last = out.logits[0, -1, :]
        return float(last[toks_A]), float(last[toks_C])


# --- Corpus --------------------------------------------------------------------

def load_corpus(corpus_path, log):
    """Load + verify the pinned Stage-A corpus artifact (before weight access)."""
    if not os.path.exists(corpus_path):
        raise ApparatusError(
            f"Stage-A corpus artifact missing: {corpus_path} (pinned at "
            "build; fail loud)")
    with open(corpus_path, "rb") as f:
        raw = f.read()
    art = json.loads(raw)
    ids = art.get("token_ids", [])
    if len(ids) != CORPUS_N_TOKENS:
        raise ApparatusError(
            f"corpus holds {len(ids)} tokens, pinned {CORPUS_N_TOKENS}")
    id_bytes = b",".join(str(i).encode() for i in ids)
    sha = hashlib.sha256(id_bytes).hexdigest()
    if sha != art.get("token_ids_sha256"):
        raise ApparatusError("corpus token_ids sha256 mismatch vs artifact pin")
    blocks = [ids[i:i + CORPUS_BLOCK]
              for i in range(0, len(ids), CORPUS_BLOCK)]
    log(f"Stage-A corpus verified: {len(ids)} tokens in {len(blocks)} blocks "
        f"(sha256 {sha[:16]}...; provenance: "
        f"{art['provenance']['dataset']}/{art['provenance']['config']}/"
        f"{art['provenance']['split']})")
    return blocks


def _mean(xs):
    return sum(xs) / len(xs)


# --- Stage A ---------------------------------------------------------------------

def run_stage_a(backend, budget, blocks, log):
    """Stage-A (s, d) perplexity screen + F7 INVALID gate.

    Returns (s_star, d_star, margin, pair_deltas, eps) or raises
    StageAInvalid (verdict INVALID — do not proceed to Stage B).
    """
    # Two no-recirculation repeat runs (F7 noise floor). Deterministic
    # decoding -> identical repeats -> eps = 0 (the pinned default).
    def _baseline_ppls():
        ppls = []
        for b, blk in enumerate(blocks):
            nlls = backend.corpus_block_nlls(blk, None)
            ppls.extend(math.exp(v) for v in nlls)
            if b == 0:
                log(f"[A] block 0: {len(nlls)} NLLs, "
                    f"mean ppl={_mean(ppls):.4f}")
        return ppls

    log("[A] baseline repeat 1/2 ...")
    ppl_a = _baseline_ppls()
    log("[A] baseline repeat 2/2 ...")
    ppl_b = _baseline_ppls()
    eps = abs(_mean([x - y for x, y in zip(ppl_a, ppl_b)]))
    log(f"[A] corpus noise floor eps={eps:.6f} "
        f"({'pinned default 0: repeats identical' if eps == 0.0 else 'measured'})")

    pair_deltas = {}
    for d in D_GRID:
        for off in S_OFFSETS:
            s = d + off
            spec = {"kind": "D2S", "s": s, "d": d, "alpha": ALPHA_STAGE_A}
            _check_leak_geometry(spec)
            ppl_r = []
            for blk in blocks:
                nlls = backend.corpus_block_nlls(blk, spec)
                ppl_r.extend(math.exp(v) for v in nlls)
            delta = _mean([x - y for x, y in zip(ppl_a, ppl_r)])
            pair_deltas[(s, d)] = delta
            log(f"[A] pair (s={s},d={d}): mean Δppl={delta:+.6f} "
                f"(passes eps={eps:.6f}: {delta > eps})")
    ok, selected, margin, passing = E.stage_a_gate(pair_deltas, eps)
    if not ok:
        raise StageAInvalid(
            f"no pair shows strictly-positive mean Δppl beyond the corpus "
            f"noise floor (eps={eps:.6f}; best={max(pair_deltas.values()):+.6f}); "
            f"Pythia-410m may be unreceptive — INVALID, do not proceed")
    s_star, d_star = selected
    log(f"[A] selected (s*,d*)=({s_star},{d_star}) Δppl={pair_deltas[selected]:+.6f}, "
        f"margin over runner-up={margin:+.6f}")
    return s_star, d_star, margin, pair_deltas, eps


class StageAInvalid(RuntimeError):
    """F7 gate: Stage-A screen flat -> INVALID verdict (no Stage B).

    This is a VERDICT (the protocol's B1 breaking point), not an apparatus
    failure: the runner writes the INVALID run record and stops."""


# --- Stage B ---------------------------------------------------------------------

def run_stage_b(backend, budget, s_star, d_star, log, records_path):
    """Stage-B directional discrimination at (s*, d*).

    Returns the run-record results dict (statistics + verdict inputs).
    """
    ps = P.load_probe_set(records_path, log)
    items = ps["items"]

    def _leak(kind, alpha):
        if kind == "D2S":
            return {"kind": "D2S", "s": s_star, "d": d_star, "alpha": alpha}
        if kind == "S2D":
            # Shallow source (d*) leaked upward into the deep destination
            # (s*); rerun span s*+1..L. D2 with s<->d swapped (D4).
            return {"kind": "S2D", "s": d_star, "d": s_star, "alpha": alpha}
        # RAND: destination pin d*, fixed once-per-run unit vector scaled to
        # ||h_d||, rerun span d*+1..L — the same rerun span as D->S (F2).
        return {"kind": "RAND", "s": None, "d": d_star, "alpha": alpha}

    def _correctness(leak):
        out = []
        for it in items:
            la, lc = backend.probe_answer_logits(it, leak)
            _, ok = P.decide_from_logits(la, lc, it["A"], it["C"])
            out.append(ok)
        return out

    log("[B] no-recirculation baseline ...")
    base = _correctness(None)
    log(f"[B] baseline accuracy={sum(base)}/{len(base)}")
    arms = {}
    for alpha in STAGE_B_ALPHAS:
        for kind in ("D2S", "S2D", "RAND"):
            spec = _leak(kind, alpha)
            _check_leak_geometry(spec)
            log(f"[B] arm {kind} alpha={alpha} ...")
            corr = _correctness(spec)
            arms[(kind, alpha)] = corr
            log(f"[B]   accuracy={sum(corr)}/{len(corr)}")

    # Primary contrast (F4, pinned): D->S vs S->D at alpha = 0.10, N = 60.
    d2s = arms[("D2S", ALPHA_LEAK)]
    s2d = arms[("S2D", ALPHA_LEAK)]
    rnd = arms[("RAND", ALPHA_LEAK)]
    primary = E.paired_contrast_stats(s2d, d2s, alpha=E.ALPHA,
                                      label="D->S vs S->D @0.10")
    secondary = E.paired_contrast_stats(rnd, d2s, alpha=E.ALPHA,
                                        label="D->S vs RAND @0.10")
    beats = {}
    for kind in ("D2S", "S2D", "RAND"):
        st = E.paired_contrast_stats(base, arms[(kind, ALPHA_LEAK)],
                                     alpha=E.ALPHA,
                                     label=f"{kind} vs baseline @0.10")
        beats[kind] = st["mcnemar_p_one_sided"] <= E.ALPHA
    gains = {a: (sum(arms[("D2S", a)]) - sum(arms[("S2D", a)])) / N_ITEMS
             for a in STAGE_B_ALPHAS}
    curve = E.gain_curve_class(gains[0.07], gains[0.10], gains[0.15])
    verdict = E.adjudicate(primary, secondary, beats, curve)

    log(f"[B] primary: d_hat={primary['d_hat']:+.4f} "
        f"McNemar 1-sided p={primary['mcnemar_p_one_sided']:.6f} "
        f"Tango95=[{primary['tango_L']:.4f},{primary['tango_U']:.4f}] "
        f"-> {E.g1b_map(primary['tango_L'], primary['tango_U'])}")
    log(f"[B] secondary D->S vs RAND: d_hat={secondary['d_hat']:+.4f} "
        f"p={secondary['mcnemar_p_one_sided']:.6f}")
    log(f"[B] gain curve {gains} -> {curve}")
    log(f"[B] arms beating baseline @0.10: "
        f"{[k for k, v in beats.items() if v] or 'none'}")
    return {"probe_set": {"records_sha": ps["records_sha"],
                          "alignment_60": ps["alignment_60"]},
            "baseline_acc": sum(base) / len(base),
            "arms_acc": {f"{k}@{a}": sum(v) / len(v)
                         for (k, a), v in arms.items()},
            "primary": primary, "secondary": secondary,
            "arm_beats_baseline": beats, "gains": gains,
            "curve_class": curve,
            "verdict": {"label": verdict[0], "evidentiary": verdict[1],
                        "detail": verdict[2]}}


# --- Orchestration ---------------------------------------------------------------

def env_manifest():
    """Law #13 environment manifest (versions available on the node)."""
    man = {"python": platform.python_version(), "platform": platform.platform()}
    for mod in ("torch", "transformers", "tokenizers"):
        try:
            m = __import__(mod)
            man[mod] = getattr(m, "__version__", "unknown")
        except ImportError:
            man[mod] = "absent"
    try:
        man["cuda"] = __import__("torch").cuda.is_available()
    except ImportError:
        man["cuda"] = False
    try:
        repo_root = os.path.dirname(os.path.abspath(__file__))
        for _ in range(3):  # EXP088_recirculation -> runs -> experiments -> SCBI
            repo_root = os.path.dirname(repo_root)
        man["git_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root,
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        man["git_commit"] = "unknown"
    return man


def run_full_loop(backend, budget, out_dir, log, corpus_path, records_path,
                  blocks_override=None):
    """Backend-agnostic EXP088 model loop.

    Phase order: 0. pre-run SHA-256 (before any pass); 1. Stage-A screen +
    F7 gate (INVALID verdict short-circuits before Stage B); 2. F2 RAND
    vector draw (once per run); 3. Stage-B discrimination; 4. post-run SHA
    (DeltaTheta == 0) before any verdict is finalized; 5. atomic artifact
    write.

    blocks_override: TEST-ONLY (mock harness). When given, these token-id
    blocks are used for Stage A instead of loading the pinned corpus
    artifact. The GPU path never uses it.

    Returns the run record dict. Raises DeltaThetaError / ApparatusError
    (verdict-clean halts). StageAInvalid is caught by cmd_run and recorded
    as the INVALID verdict.
    """
    t0 = time.time()
    here = os.path.dirname(os.path.abspath(__file__))

    # Phase 0 — pre-run SHA BEFORE any model pass (Law #13).
    pre_hash = backend.state_hash()
    log(f"[0] pre-run state SHA-256: {pre_hash}")
    if pre_hash != HISTORICAL_SHA256:
        log(f"[0] WARNING: pre-run hash != program historical pin "
            f"{HISTORICAL_SHA256[:16]}... — weight revision differs from "
            f"EXP084's pinned revision; logged, not halting (the signed "
            f"protocol requires pre/post logging, not this pin)")
    else:
        log("[0] pre-run hash matches the program historical pin")

    # F2: draw the fixed random unit vector ONCE per run (pinned seed).
    u = backend.rand_unit_vector()
    log(f"[0] F2 RAND vector ready (pinned seed {RAND_SEED})")

    # Phase 1 — Stage A.
    if blocks_override is not None:
        blocks = blocks_override
        log(f"[A] TEST-ONLY blocks_override: {len(blocks)} synthetic blocks")
    else:
        blocks = load_corpus(corpus_path, log)
    s_star, d_star, margin, pair_deltas, eps = run_stage_a(
        backend, budget, blocks, log)

    # Phase 3 — Stage B.
    results = run_stage_b(backend, budget, s_star, d_star, log, records_path)

    # Phase 4 — post-run SHA (DeltaTheta == 0), before finalizing.
    post_hash = backend.state_hash()
    if post_hash != pre_hash:
        raise DeltaThetaError("post-run SHA-256 != pre-run (DeltaTheta != 0)")
    log(f"[post] SHA-256 post==pre ({post_hash[:16]}...); DeltaTheta==0 "
        f"confirmed; forward calls used: {budget.used}/{budget.limit}")

    return finish_run(results, budget, out_dir, log, pre_hash, post_hash,
                      t0, here, s_star, d_star, margin, pair_deltas, eps)


def finish_run(results, budget, out_dir, log, pre_hash, post_hash, t0, here,
               s_star, d_star, margin, pair_deltas, eps):
    """Write the run manifest + results atomically; log the verdict."""
    verdict = results["verdict"]
    record = {
        "experiment": "EXP088",
        "protocol": ("experiments/protocols/"
                     "EXP088_RECIRCULATION_PREREG_SIGNED.md"),
        "model_id": MODEL_ID,
        "pre_sha256": pre_hash,
        "post_sha256": post_hash,
        "historical_pin_sha256": HISTORICAL_SHA256,
        "delta_theta": "0 (SHA pre==post)",
        "env": env_manifest(),
        "stage_a": {
            "grid": {"d": list(D_GRID), "s_offsets": list(S_OFFSETS),
                     "alpha": ALPHA_STAGE_A},
            "corpus": {"n_tokens": CORPUS_N_TOKENS, "block": CORPUS_BLOCK,
                       "n_blocks": (CORPUS_N_TOKENS + CORPUS_BLOCK - 1) // CORPUS_BLOCK},
            "noise_floor_eps": eps,
            "pair_deltas": {f"s={s},d={d}": v
                            for (s, d), v in pair_deltas.items()},
            "selected": {"s_star": s_star, "d_star": d_star,
                         "margin_over_runner_up": margin},
            "ramping": RP.describe_schedule(),
        },
        "stage_b": results,
        "seeds": {"master": MASTER_SEED, "rand_vector": RAND_SEED,
                  "decoding": "greedy/deterministic (no sampling)"},
        "budget": {"fwd_calls_used": budget.used,
                   "fwd_calls_limit": budget.limit,
                   "stage_a_calls": STAGE_A_CALLS,
                   "stage_b_calls": STAGE_B_CALLS},
        "verdict": verdict,
        "elapsed_s": round(time.time() - t0, 1),
    }
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp088_results.json")
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(record, f, indent=1)
    os.replace(tmp, out_path)
    log(f"[done] results -> {out_path}")
    log(f"VERDICT: {verdict['label']} [{verdict['evidentiary']}] :: "
        f"{verdict['detail']}")
    return record


# --- CLI -------------------------------------------------------------------------

def _startup_preflight(args, log, check_gpu=True):
    """Fail-fast crash guard: verify everything that needs no weights BEFORE
    any weight access (TorchBackend construction).

    Order: corpus artifact -> probe records -> fixed geometry -> output-dir
    writability -> (check_gpu) torch/CUDA. Raises ApparatusError on any
    failure. check_gpu=False is for the CPU smoke test (exercises every
    non-GPU check against the real pinned artifacts without needing CUDA).
    """
    here = os.path.dirname(os.path.abspath(__file__))
    corpus_path = args.corpus or os.path.join(here, "stageA_corpus.json")
    records_path = args.records or os.path.join(here, P.RECORDS_REL)

    # 1. Corpus artifact.
    if not os.path.exists(corpus_path):
        raise ApparatusError(
            f"startup preflight: Stage-A corpus artifact missing: "
            f"{corpus_path}")
    with open(corpus_path, "rb") as f:
        raw = f.read()
    try:
        art = json.loads(raw)
    except ValueError as e:
        raise ApparatusError(
            f"startup preflight: corpus artifact is not valid JSON: {e}")
    ids = art.get("token_ids", [])
    if len(ids) != CORPUS_N_TOKENS:
        raise ApparatusError(
            f"startup preflight: corpus holds {len(ids)} tokens, pinned "
            f"{CORPUS_N_TOKENS}")
    if not all(isinstance(i, int) and i >= 0 for i in ids):
        raise ApparatusError(
            "startup preflight: corpus token_ids are not all non-neg ints")
    id_bytes = b",".join(str(i).encode() for i in ids)
    sha = hashlib.sha256(id_bytes).hexdigest()
    if sha != art.get("token_ids_sha256"):
        raise ApparatusError(
            "startup preflight: corpus token_ids sha256 mismatch vs the "
            "artifact's recorded pin (artifact tampered or truncated)")
    if CORPUS_TOKEN_IDS_SHA256 is None:
        raise ApparatusError(
            "startup preflight: CORPUS_TOKEN_IDS_SHA256 pin not transcribed "
            "at build (see BUILD_NOTES.md); refusing to run unpinned")
    if sha != CORPUS_TOKEN_IDS_SHA256:
        raise ApparatusError(
            f"startup preflight: corpus sha256 {sha} != build pin "
            f"{CORPUS_TOKEN_IDS_SHA256}")
    prov = art.get("provenance", {})
    for k in ("dataset", "config", "split", "source_sha256",
              "tokenizer_sha256"):
        if k not in prov:
            raise ApparatusError(
                f"startup preflight: corpus provenance missing key {k!r}")
    log(f"[preflight] corpus OK: {len(ids)} tokens, sha256 {sha[:16]}..., "
        f"{prov['dataset']}/{prov['config']}/{prov['split']}")

    # 2. Probe records (F11 pin).
    if not os.path.exists(records_path):
        raise ApparatusError(
            f"startup preflight: probe records missing: {records_path}")
    with open(records_path, "rb") as f:
        rsha = hashlib.sha256(f.read()).hexdigest()
    if rsha != P.RECORDS_SHA256:
        raise ApparatusError(
            f"startup preflight: records sha256 {rsha} != F11 pin "
            f"{P.RECORDS_SHA256}")
    records = json.loads(open(records_path).read())
    if len(records) != N_ITEMS:
        raise ApparatusError(
            f"startup preflight: records hold {len(records)} items, F11 "
            f"pins {N_ITEMS}")
    log(f"[preflight] probe records OK: {len(records)} items, sha256 "
        f"{rsha[:16]}...")

    # 3. Fixed configuration geometry (pinned; a drifted constant is a
    # protocol violation, not a runtime hiccup).
    geometry = {"MODEL_ID": (MODEL_ID, "EleutherAI/pythia-410m"),
                "N_LAYERS": (N_LAYERS, 24),
                "HIDDEN": (HIDDEN, 1024),
                "D_GRID": (D_GRID, (4, 6, 8)),
                "S_OFFSETS": (S_OFFSETS, (4, 6, 8)),
                "STAGE_B_ALPHAS": (STAGE_B_ALPHAS, (0.07, 0.10, 0.15)),
                "ALPHA_STAGE_A": (ALPHA_STAGE_A, 0.10),
                "FWD_BUDGET": (FWD_BUDGET, 1640)}
    for name, (got, want) in geometry.items():
        if got != want:
            raise ApparatusError(
                f"startup preflight: geometry drift: {name}={got!r} != "
                f"pinned {want!r}")
    log("[preflight] fixed geometry OK (24L/1024H, grid, alphas, budget 1640)")

    # 4. Output dir writability.
    out_dir = args.out or here
    os.makedirs(out_dir, exist_ok=True)
    probe = os.path.join(out_dir, ".exp088_write_probe")
    try:
        with open(probe, "w") as f:
            f.write("ok")
        os.remove(probe)
    except OSError as e:
        raise ApparatusError(
            f"startup preflight: output dir not writable: {out_dir} ({e})")
    log(f"[preflight] output dir writable: {out_dir}")

    # 5. GPU stack (last — closest to weight access).
    if check_gpu:
        try:
            import torch  # noqa: F401
        except ImportError as e:
            raise ApparatusError(
                "startup preflight: torch is not installed; the model loop "
                "needs the GPU node") from e
        import torch
        if not torch.cuda.is_available():
            raise ApparatusError(
                "startup preflight: torch installed but CUDA unavailable; "
                "EXP088 is GPU-licensed")
        log(f"[preflight] torch {torch.__version__} + CUDA OK")
    else:
        log("[preflight] GPU stack check skipped (CPU smoke mode)")
    log("[preflight] ALL CHECKS PASS — weights may now be accessed")


def cmd_run(args):
    here = os.path.dirname(os.path.abspath(__file__))
    if not args.ceo_gpu_clearance:
        print("REFUSED: --run requires --ceo-gpu-clearance "
              "(CEO GPU clearance for EXP088).")
        return 2
    if not args.bundle_review_signoff:
        print("REFUSED: --run requires --bundle-review-signoff (the "
              "independent Law #14 bundle review sign-off).")
        return 2
    out_dir = args.out or here
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp088_run_log.txt")

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        with open(log_path, "a") as f:
            f.write(line + "\n")

    # Startup preflight BEFORE any weight access (crash guard): corpus,
    # records, geometry, out-dir, torch/CUDA. Raises ApparatusError loud.
    try:
        _startup_preflight(args, log, check_gpu=True)
    except ApparatusError as e:
        log(f"PREFLIGHT HALT: {e}")
        return 3

    budget = PassBudget()
    corpus_path = args.corpus or os.path.join(here, "stageA_corpus.json")
    records_path = (args.records or os.path.join(here, P.RECORDS_REL))
    try:
        backend = TorchBackend(budget, log)
        run_full_loop(backend, budget, out_dir, log, corpus_path, records_path)
    except StageAInvalid as e:
        # F7/B1: the screen is flat -> INVALID verdict (no Stage B).
        # The protocol's B1 breaking point: INVALID, stop. The run record
        # carries the verdict; nothing scientific ran beyond the screen.
        write_invalid_record(backend, budget, out_dir, log, e)
        return 0
    except (DeltaThetaError, ApparatusError) as e:
        log(f"HALT (verdict-clean): {type(e).__name__}: {e}")
        return 3
    except Exception as e:  # unexpected: loud, no verdict
        log(f"HALT (unexpected {type(e).__name__}): {e}")
        return 4
    return 0


def write_invalid_record(backend, budget, out_dir, log, exc):
    """Write the F7/B1 INVALID run record (shared by cmd_run and tests)."""
    log(f"VERDICT: INVALID [Underdetermined] :: {exc}")
    pre = backend.state_hash()
    record = {
        "experiment": "EXP088",
        "protocol": ("experiments/protocols/"
                     "EXP088_RECIRCULATION_PREREG_SIGNED.md"),
        "model_id": MODEL_ID,
        "pre_sha256": pre, "post_sha256": pre,
        "delta_theta": "0 (SHA pre==post; Stage B never ran)",
        "env": env_manifest(),
        "stage_a": {"gate": "INVALID", "detail": str(exc)},
        "stage_b": None,
        "seeds": {"master": MASTER_SEED, "rand_vector": RAND_SEED},
        "budget": {"fwd_calls_used": budget.used,
                   "fwd_calls_limit": budget.limit},
        "verdict": {"label": "INVALID", "evidentiary": "Underdetermined",
                    "detail": str(exc)},
    }
    out_path = os.path.join(out_dir, "exp088_results.json")
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(record, f, indent=1)
    os.replace(tmp, out_path)
    log(f"[done] results -> {out_path}")
    return record


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="EXP088 recirculation model loop (signed protocol).")
    ap.add_argument("--smoke", action="store_true",
                    help="CPU-only: smoke suite incl. the mock-model "
                         "end-to-end harness (zero model passes).")
    ap.add_argument("--run", action="store_true",
                    help="GPU-node model loop (needs both sign-off flags).")
    ap.add_argument("--ceo-gpu-clearance", action="store_true",
                    help="CEO GPU clearance for the EXP088 run.")
    ap.add_argument("--bundle-review-signoff", action="store_true",
                    help="Independent Law #14 bundle review sign-off.")
    ap.add_argument("--out", default=None,
                    help="Run output directory (default: bundle dir).")
    ap.add_argument("--corpus", default=None,
                    help="Override path to the pinned Stage-A corpus artifact.")
    ap.add_argument("--records", default=None,
                    help="Override path to the pinned EXP077 records file.")
    args = ap.parse_args(argv)
    if args.smoke:
        smoke_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "smoke_test.py")
        return subprocess.call([sys.executable, smoke_path])
    if args.run:
        return cmd_run(args)
    raise RuntimeError(
        "GPU execution not licensed in this bundle stage. Use --smoke for "
        "the CPU harness, or --run with --ceo-gpu-clearance and "
        "--bundle-review-signoff on the GPU node."
    )


if __name__ == "__main__":
    sys.exit(main())
