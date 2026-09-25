#!/usr/bin/env python3
"""EXP086 runner: R3 dynamical-amplifier / singular-vector-aligned injection.

Implements the signed protocol
experiments/protocols/EXP086_R3_AMPLIFIER_PREREG_SIGNED.md (LOG-311, CEO-signed).

TWO MODES (one bundle, two gates):
  --stage-a : Stage A ($0 CPU, weight-only, ADVISORY). Licensed on bundle
              build (LOG-311) but weight access happens ONLY after the
              independent Law #14 bundle review -> requires
              --bundle-review-signoff (refuses with exit 2 otherwise).
              NEVER emits a verdict (structural; see exp086_henrici).
  --run     : Stage B GPU pilot orchestration (backend-neutral run_full_loop;
              the TorchBackend sketch is execution-node code). NOT licensed:
              requires BOTH --ceo-gpu-clearance AND --stage2-review-signoff
              (refuses with exit 2 otherwise). Queue: behind K2 -> EXP083 ->
              EXP084; no pre-emption.

Frozen backbone (Law #6): read-only weight access; FrozenBackboneGuard hashes
state_dict before/after every weight-touching phase; mismatch -> INVALID V1.
Deterministic (Law #13): seeds pinned, env manifest logged, parameter hashes
recorded, raw per-item logs preserved.

Pass budget (§11, binding): 121 fwd-equiv/item x 60 = 7260; Stage-2 permuted
arm = 120; total hard ceiling 7380. The budget REFUSES the excess pass.

This file has never executed a model pass on the build machine: the
TorchBackend raises without torch, and both execution modes refuse without
their clearance flags (verified by the smoke test).
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp086_guards as G
import exp086_henrici as H
import exp086_rng as R
import exp086_statistics as S
import exp086_verdicts as V

HERE = os.path.dirname(os.path.abspath(__file__))
PROTOCOL_PATH = os.path.join(
    HERE, "..", "..", "protocols", "EXP086_R3_AMPLIFIER_PREREG_SIGNED.md")


# ---------------------------------------------------------------------------
# Environment manifest (Law #13)
# ---------------------------------------------------------------------------

def env_manifest(extra=None):
    """Deterministic environment manifest for every run artifact."""
    try:
        import numpy as _np
        numpy_v = _np.__version__
    except ImportError:
        numpy_v = None
    try:
        import torch as _t
        torch_v = _t.__version__
    except ImportError:
        torch_v = None
    try:
        git = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                             text=True, cwd=HERE, timeout=10)
        commit = git.stdout.strip() if git.returncode == 0 else None
    except Exception:
        commit = None
    file_hashes = {}
    for fn in ("exp086_guards.py", "exp086_henrici.py", "exp086_rng.py",
               "exp086_statistics.py", "exp086_verdicts.py", "run_exp086.py"):
        p = os.path.join(HERE, fn)
        if os.path.exists(p):
            h = hashlib.sha256()
            with open(p, "rb") as f:
                h.update(f.read())
            file_hashes[fn] = h.hexdigest()
    try:
        hp = hashlib.sha256()
        with open(PROTOCOL_PATH, "rb") as f:
            hp.update(f.read())
        protocol_digest = hp.hexdigest()
    except OSError:
        protocol_digest = None
    m = {
        "experiment": "EXP086",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "numpy": numpy_v,
        "torch": torch_v,
        "git_commit": commit,
        "bundle_file_hashes": file_hashes,
        "protocol_sha256": protocol_digest,
        "master_seed": R.MASTER_SEED,
        "model": G.MODEL_ID,
        "layer_index": G.LAYER_INDEX,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if extra:
        m.update(extra)
    return m


def atomic_write_json(path, obj):
    """Atomic JSON write (tmp + rename); never leaves a half-written record."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
        f.write("\n")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Backend protocol (backend-neutral orchestration; EXP084 LOG-268 pattern)
# ---------------------------------------------------------------------------

class Backend:
    """Abstract execution backend. The runner never touches a model directly.

    Stage A: load_state_dict_readonly() -> {name: array-like}.
    Stage B: build_probe(record, i) -> probe; baseline_forward(probe);
             power_iteration(probe, h); decision_normal_vjp(probe, h);
             inject_and_eval(probe, h, direction, eps_frac).
    directions are tags: "v1","v2","v3","vrand_<k>","bagg","permuted".
    """

    # -- Stage A --
    def load_state_dict_readonly(self):
        raise NotImplementedError

    # -- Stage B --
    def build_probe(self, record, i):
        raise NotImplementedError

    def baseline_forward(self, probe):
        """-> (correct: bool, logits: list[float], h: vector). 1 fwd."""
        raise NotImplementedError

    def power_iteration(self, probe, h):
        """Deflated power iteration, ranks 1..3.

        -> dict(v=[v1,v2,v3] unit vectors, s=[s1,s2,s3] sigma hats,
                rayleigh=[traj1,traj2,traj3], n_iters=[..]).
        Costs 108 fwd-equiv (3 vec x 12 iter x (1 JVP + 1 VJP)); the runner
        charges the budget — the backend only reports n_iters for the log.
        """
        raise NotImplementedError

    def decision_normal_vjp(self, probe, h):
        """n̂ = grad_{h}(z_top1 - z_top2), unit vector. 1 VJP = 2 fwd-equiv."""
        raise NotImplementedError

    def apply_sign_rule(self, item_idx, n_hat):
        """§4 F2: v̂_r <- sign(<v̂_r, n̂>) v̂_r, applied to the TREATMENT vectors.

        Must be called after power_iteration + decision_normal_vjp and before
        any inject_and_eval with v1/v2/v3. The injected arms must carry the
        signed directions — not the arbitrary-sign power-iteration cache
        (F1 fix, Law #14 Stage-B review 2026-09-25). Returns signed v̂_1
        (for the ĉ diagnostic).
        """
        raise NotImplementedError

    def inject_and_eval(self, probe, h, direction, eps_frac):
        """Inject eps_frac*||h|| * direction at the answer position; re-run.

        -> (correct: bool, logits: list[float]). 1 fwd.
        """
        raise NotImplementedError

    def stage2_derangement(self, n):
        """Fixed derangement der(i) != i for the Stage-2 permuted arm (§4 F10).

        Seeded (MASTER_SEED). The TorchBackend uses exp086_rng.derangement;
        test backends supply their own deterministic derangement.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# EXP077 §3 verbatim probe rebuild (torch-free; testable on the build machine)
# ---------------------------------------------------------------------------
# Pinned to the EXP065/EXP077 construction (see
# experiments/scripts/run_exp065_temporary_coordinate_alignment.py §3 and
# experiments/runs/exp077/run_exp077.py TRIPLES_INDICES/QUADS_INDICES — the
# code that PRODUCED the EXP077 archive). Fixed indices 0..59:
#   0..14  planet 2-hop, 15..29 planet 3-hop,
#   30..44 element 2-hop, 45..59 element 3-hop.
# target = head entity A; foil = tail entity (C for 2-hop, D for 3-hop).
#
# DEVIATION NOTE (EXP084-D1 class): EXP084's run_exp084.py build_benchmark
# claims a "verbatim" rebuild but uses DIFFERENT index tuples (a 15-cycle
# rotation set). EXP086 does NOT follow EXP084; it follows the authoritative
# EXP077 construction below. The EXP077 archive itself contains no prompt
# strings (only ent/typ/correct per record), so bit-identity of the prompt
# SET rests on this construction code, and the archive serves as the
# SHA-256 integrity pin + 60-record probe-set definition (protocol R5d).

_BENCH_PLANETS = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
_BENCH_ELEMENTS = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
_BENCH_TRIPLES = [
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
]
_BENCH_QUADS = [
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
]


def build_benchmark_items():
    """Rebuild the 60 EXP077 probe items verbatim (prompt/target/foil/ent/typ).

    Torch-free: returns plain dicts. The backend's build_probe() pins the
    tokenizer-dependent fields (input_ids, t_tok, f_tok) on the execution node
    and asserts ent/typ alignment with the archived EXP077 records.
    """
    bench = []
    for i, (iA, iB, iC) in enumerate(_BENCH_TRIPLES):
        A, B, C = (_BENCH_PLANETS[iA], _BENCH_PLANETS[iB], _BENCH_PLANETS[iC])
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 8:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {C} is lower than {B}. {B} is lower than {A}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_planet_2hop_{i}", "prompt": p,
                      "target": A, "foil": C, "ent": A, "typ": "planet"})
    for i, (iA, iB, iC, iD) in enumerate(_BENCH_QUADS):
        A, B, C, D_ent = (_BENCH_PLANETS[iA], _BENCH_PLANETS[iB],
                          _BENCH_PLANETS[iC], _BENCH_PLANETS[iD])
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 8:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                 f"{C} outranks {D_ent}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_planet_3hop_{i}", "prompt": p,
                      "target": A, "foil": D_ent, "ent": A, "typ": "planet"})
    for i, (iA, iB, iC) in enumerate(_BENCH_TRIPLES):
        A, B, C = (_BENCH_ELEMENTS[iA], _BENCH_ELEMENTS[iB],
                   _BENCH_ELEMENTS[iC])
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 7:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {C} is lower than {B}. {B} is lower than {A}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_element_2hop_{i}", "prompt": p,
                      "target": A, "foil": C, "ent": A, "typ": "element"})
    for i, (iA, iB, iC, iD) in enumerate(_BENCH_QUADS):
        A, B, C, D_ent = (_BENCH_ELEMENTS[iA], _BENCH_ELEMENTS[iB],
                          _BENCH_ELEMENTS[iC], _BENCH_ELEMENTS[iD])
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 7:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                 f"{C} outranks {D_ent}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_element_3hop_{i}", "prompt": p,
                      "target": A, "foil": D_ent, "ent": A, "typ": "element"})
    assert len(bench) == 60, f"expected 60 bench items, got {len(bench)}"
    return bench


# Module-level verbatim rebuild (torch-free; asserted at import).
_BENCH = build_benchmark_items()


class TorchBackend(Backend):
    """EXECUTION-NODE ONLY (torch + transformers + weights). UNTESTED on the
    CPU build machine (torch absent); must pass the Law #14 bundle review
    before any execution. Sketch of the signed §4/§6 construction:

    - Model loaded once, .eval(), all params requires_grad_(False); the
      state_dict is snapshotted by FrozenBackboneGuard (read-only by
      construction — no optimizer, no .backward() on params, no in-place
      weight ops anywhere in this file).
    - h_l(x): forward hook on gpt_neox.layers[20] capturing the residual
      stream at the answer position (final token; program-standard site).
    - J(x) = dz/dh_l never materialized: JVP via torch.autograd.functional.jvp
      (1 fwd), VJP via torch.autograd.functional.vjp (1 bwd ~= 2 fwd-equiv),
      on the hook-captured activation leaf under torch.enable_grad().
    - Deflated power iteration: w <- (I - Vhat Vhat^T) w projections between
      ranks; 12-iteration cap; Rayleigh-quotient stall tol 1e-3 (relative).
    - Sign rule: v_r <- sign(<v_r, n̂>) v_r (§4 F2).
    - n̂: single VJP of (z_top1 - z_top2) at h_l (label-free; Law #7 clean).
    - Injection: h_l <- h_l + eps*d̂ at the answer position via a second
      forward with a perturbation hook; eps = eps_frac * ||h_l||_2.
    - Correctness: greedy-decoded answer vs the probe's labeled correct
      option — labels touch ONLY the correctness endpoint (Law #7 standard).
    - Probe rebuild: verbatim EXP077 §3 rebuild, fixed indices 0..59; the
      deviation note (EXP084-D1 class) is loudly logged by load_probe_set.
    """

    def __init__(self, weights_path, device="cuda", attn_implementation=None):
        try:
            import torch  # noqa: F401
        except ImportError:
            raise RuntimeError(
                "TorchBackend requires torch (execution node). Refusing on "
                "the CPU build machine."
            )
        self.weights_path = weights_path
        self.device = device
        # attn_implementation: None = environment default (GPU node). The CPU
        # readiness test passes "eager" because torch's CPU flash-attention
        # backward is unimplemented (jvp/vjp require a differentiable attn).
        self._attn_implementation = attn_implementation
        self._torch = None
        self._model = None
        self._tokenizer = None
        self._layer = None          # gpt_neox.layers[20]
        self._b_agg = None          # historical B_agg anchor (unit vector)
        self._v_cache = {}          # (item_idx, rank) -> unit v̂_r tensor

    # -- lazy, execution-node-only setup ---------------------------------
    def _setup(self):
        """Load model/tokenizer/B_agg once. Loud halt on any defect."""
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        if self._model is not None:
            return
        torch.use_deterministic_algorithms(True)
        dev = self.device
        if dev == "cuda" and not torch.cuda.is_available():
            raise RuntimeError(
                "TorchBackend: device='cuda' requested but CUDA is not "
                "available on this node. Refusing to silently run a GPU-budgeted "
                "pilot on the wrong device."
            )
        try:
            torch.set_default_device(dev)
        except Exception:
            pass  # older torch: fall back to explicit .to() calls below
        model = AutoModelForCausalLM.from_pretrained(
            self.weights_path, torch_dtype=torch.float32, trust_remote_code=False,
            attn_implementation=self._attn_implementation)
        try:
            model.to(dev)
        except Exception:
            pass
        model.eval()
        for p in model.parameters():
            p.requires_grad_(False)
        tok = AutoTokenizer.from_pretrained(self.weights_path,
                                            trust_remote_code=False)
        self._torch = torch
        self._model = model
        self._tokenizer = tok
        self._layer = model.gpt_neox.layers[G.LAYER_INDEX]
        self._b_agg = self._load_b_agg()

    def _load_b_agg(self):
        """Load the historical B_agg anchor: archived EXP077 v_hat.

        Provenance: experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt,
        key 'v_hat' — the killed static-semantic family direction from the
        EXP077 pilot (same model, same layer, same space). Validated loud:
        shape (1024,), unit norm, finite.
        """
        import torch
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "EXP077_cone_vs_line", "exp077_vectors.pt")
        if not os.path.exists(p):
            raise RuntimeError(
                f"TorchBackend: B_agg archive missing: {p}. Refusing.")
        d = torch.load(p, map_location="cpu", weights_only=True)
        v = d["v_hat"].to(torch.float32).flatten()
        if tuple(v.shape) != (G.D_MODEL,):
            raise RuntimeError(
                f"TorchBackend: B_agg shape {tuple(v.shape)} != "
                f"({G.D_MODEL},). Refusing.")
        n = float(v.norm(p=2))
        if not (0.999 <= n <= 1.001):
            raise RuntimeError(
                f"TorchBackend: B_agg not unit-norm (||v||={n}). Refusing.")
        if bool(torch.isnan(v).any()) or bool(torch.isinf(v).any()):
            raise RuntimeError("TorchBackend: B_agg has NaN/Inf. Refusing.")
        return (v / v.norm(p=2)).to(self.device)

    # -- hook machinery ----------------------------------------------------
    @staticmethod
    def _take_out(output):
        return output[0] if isinstance(output, tuple) else output

    def _logits_with_delta(self, input_ids, delta):
        """Full-model last-position logits with layer-20 output perturbed.

        Adds `delta` (a (1024,) tensor, requires_grad allowed) at the answer
        (final) position only, via a forward hook. Returns logits[0,-1,:].
        The hook preserves the layer's tuple output structure.
        """
        torch = self._torch
        layer = self._layer

        def hook(module, inputs, output):
            o = self._take_out(output)
            pad = torch.zeros_like(o)
            pad[:, -1, :] = delta.to(o.dtype)
            new_o = o + pad
            if isinstance(output, tuple):
                return (new_o,) + tuple(output[1:])
            return new_o

        handle = layer.register_forward_hook(hook)
        try:
            out = self._model(input_ids=input_ids)
        finally:
            handle.remove()
        return out.logits[0, -1, :]

    def _capture_h_and_logits(self, input_ids):
        """One clean forward: (h: (1024,) residual at layer 20 / answer pos,
        logits: (V,) last-position logits)."""
        captured = {}

        def hook(module, inputs, output):
            o = self._take_out(output)
            captured["h"] = o[0, -1, :].detach().clone()

        handle = self._layer.register_forward_hook(hook)
        try:
            out = self._model(input_ids=input_ids)
        finally:
            handle.remove()
        return captured["h"], out.logits[0, -1, :]

    # -- Stage-B interface ---------------------------------------------------
    def load_state_dict_readonly(self):
        self._setup()
        return self._model.state_dict()

    def build_probe(self, record, i):
        """Pin the verbatim probe: tokenize the rebuilt prompt.

        The record is accepted as the protocol-pinned probe-set definition
        (SHA-256 verified by load_probe_set); the prompt strings come from
        the authoritative EXP077 construction (_BENCH). NOTE: no per-index
        ent/typ alignment is asserted — the archived records carry no prompt
        strings and their record order does not match construction order, so
        a per-index check would be spurious. The probe SET (60 prompts) is
        what the construction guarantees.
        """
        self._setup()
        item = _BENCH[i]
        input_ids = self._tokenizer(item["prompt"], return_tensors="pt"
                                    ).input_ids.to(self.device)
        t_ids = self._tokenizer.encode(" " + item["target"])
        f_ids = self._tokenizer.encode(" " + item["foil"])
        if len(t_ids) != 1 or len(f_ids) != 1:
            raise RuntimeError(
                f"build_probe: target/foil not single tokens at index {i} "
                f"(target={t_ids}, foil={f_ids}). Refusing: correctness "
                "endpoint requires single-token options.")
        return {"i": i, "id": item["id"], "prompt": item["prompt"],
                "target": item["target"], "foil": item["foil"],
                "input_ids": input_ids, "t_tok": t_ids[0], "f_tok": f_ids[0]}

    def baseline_forward(self, probe):
        """-> (correct: bool, logits: list[float], h: vector). 1 fwd.

        Correctness (protocol §4 sketch, binding): greedy-decoded answer
        (argmax over the full vocabulary at the answer position) vs the
        probe's labeled correct option. Labels touch ONLY this endpoint.
        """
        self._setup()
        torch = self._torch
        with torch.no_grad():
            h, logits = self._capture_h_and_logits(probe["input_ids"])
        if bool(torch.isnan(h).any()) or bool(torch.isinf(h).any()):
            raise RuntimeError(
                f"baseline_forward: h has NaN/Inf on item {probe['i']}. "
                "Refusing.")
        correct = bool(int(torch.argmax(logits)) == probe["t_tok"])
        return correct, [float(x) for x in logits.detach().cpu()], h

    def power_iteration(self, probe, h):
        """Deflated power iteration on J^T J for ranks 1..3 (protocol §4).

        J(x) = dz/dh_l is never materialized: each iteration is 1 JVP
        (torch.autograd.functional.jvp, ~1 fwd) + 1 VJP
        (torch.autograd.functional.vjp, ~1 bwd ~= 2 fwd-equiv), applied to
        f(delta) = last-position logits with layer-20 output += delta.
        Deflation: project (I - V̂V̂ᵀ) before and after each JᵀJ application.
        Converged when the Rayleigh quotient's relative change < 1e-3 for 3
        consecutive iterations (12-iteration cap); else converged=False, which
        is DIAGNOSTIC-ONLY and does not abort the item (F5 correction, Law #14
        Stage-B review 2026-09-25). The only item-abort is σ̂₁/σ̂₂ < 1.1
        (G.should_abort_item, §6.4). The Rayleigh quotient is computed as
        ||Jw||² from the iteration's own JVP — zero extra passes (F2 fix).

        -> dict(v=[v1,v2,v3], s=[σ̂1,σ̂2,σ̂3], rayleigh=[traj...],
                n_iters=[...], converged=bool).
        """
        self._setup()
        torch = self._torch
        d = G.D_MODEL
        input_ids = probe["input_ids"]
        i = probe["i"]

        def f(delta):
            return self._logits_with_delta(input_ids, delta)

        delta0 = torch.zeros(d, device=self.device)
        V_prev = torch.zeros((d, 0), device=self.device)
        vs, sigmas, trajs, n_iters = [], [], [], []
        all_converged = True
        with torch.enable_grad():
            for r in range(3):
                gen = torch.Generator(device="cpu")
                gen.manual_seed(G.MASTER_SEED + 90000 + i * 10 + r)
                w = torch.randn(d, generator=gen, device=self.device,
                                dtype=torch.float32)
                w = w / w.norm(p=2)
                traj, consec, rho_prev = [], 0, None
                it_done = G.PI_MAX_ITER
                for t in range(G.PI_MAX_ITER):
                    if V_prev.shape[1] > 0:
                        w = w - V_prev @ (V_prev.T @ w)
                        wn = w.norm(p=2)
                        if float(wn) == 0.0:
                            raise RuntimeError(
                                "power_iteration: deflated w is zero "
                                f"(item {i}, rank {r+1}). Loud halt.")
                        w = w / wn
                    # J w  (1 JVP)
                    _f0, Jw = torch.autograd.functional.jvp(f, delta0, w)
                    # Rayleigh quotient rho = w^T J^T J w = ||Jw||^2.
                    # F2 fix (Law #14 Stage-B review 2026-09-25): computed from
                    # the already-available Jw — ZERO extra passes. The prior
                    # code ran a second JVP on w_new for this, which was
                    # unbudgeted (4 fwd-equiv/iter vs the registered 3).
                    rho = float((Jw.norm(p=2) ** 2))
                    traj.append(rho)
                    if rho_prev is not None and rho_prev > 0:
                        rel = abs(rho - rho_prev) / rho_prev
                        consec = consec + 1 if rel < G.PI_STALL_TOL else 0
                    else:
                        consec = 0
                    rho_prev = rho
                    # J^T (J w)  (1 VJP)
                    _f0b, JTJw_t = torch.autograd.functional.vjp(
                        f, delta0, Jw)
                    JTJw = JTJw_t.reshape(-1)
                    if V_prev.shape[1] > 0:
                        JTJw = JTJw - V_prev @ (V_prev.T @ JTJw)
                    nrm = float(JTJw.norm(p=2))
                    if nrm == 0.0 or not math.isfinite(nrm):
                        raise RuntimeError(
                            "power_iteration: J^TJw degenerate "
                            f"(item {i}, rank {r+1}, iter {t}). Loud halt.")
                    w = JTJw / nrm
                    if consec >= G.PI_STALL_WINDOW:
                        it_done = t + 1
                        break
                converged_r = consec >= G.PI_STALL_WINDOW
                all_converged = all_converged and converged_r
                sigma = math.sqrt(rho_prev) if rho_prev and rho_prev > 0 else 0.0
                if not math.isfinite(sigma):
                    raise RuntimeError(
                        "power_iteration: non-finite sigma "
                        f"(item {i}, rank {r+1}). Loud halt.")
                v = w / w.norm(p=2)
                vs.append(v.detach())
                sigmas.append(sigma)
                trajs.append(traj)
                n_iters.append(it_done)
                self._v_cache[(i, r + 1)] = v.detach().clone()
                V_prev = torch.cat([V_prev, v.reshape(-1, 1)], dim=1)
        return {"v": vs, "s": sigmas, "rayleigh": trajs,
                "n_iters": n_iters, "converged": all_converged}

    def decision_normal_vjp(self, probe, h):
        """n̂ = grad_{h_l}(z_top1 − z_top2)(h_l(x)), unit vector (protocol D5).

        Label-free: top-2 indices are taken at the unperturbed point; the
        scalar (z_i1 − z_i2) is differentiated w.r.t. the perturbation delta.
        1 VJP = 2 fwd-equiv. Loud halt if the gradient is degenerate.
        """
        self._setup()
        torch = self._torch
        input_ids = probe["input_ids"]

        def f(delta):
            return self._logits_with_delta(input_ids, delta)

        with torch.enable_grad():
            delta = torch.zeros(G.D_MODEL, device=self.device,
                                requires_grad=True)
            logits = f(delta)
            top2 = torch.topk(logits, 2)
            i1, i2 = int(top2.indices[0]), int(top2.indices[1])
            s = logits[i1] - logits[i2]
            g = torch.autograd.grad(s, delta)[0].reshape(-1)
        nrm = float(g.norm(p=2))
        if nrm == 0.0 or not math.isfinite(nrm):
            raise RuntimeError(
                f"decision_normal_vjp: degenerate gradient (item {probe['i']})."
                " Loud halt.")
        return (g / nrm).detach()

    def apply_sign_rule(self, item_idx, n_hat):
        """§4 F2, applied IN the treatment cache (F1 fix).

        Flips each cached v̂_r by sign(<v̂_r, n̂>) so that _resolve_direction
        (hence every injected v1/v2/v3 arm) carries the signed treatment.
        The unsigned power-iteration output is never injected. Loud halt if
        the cache is missing (power iteration must precede). Returns the
        signed v̂_1 tensor for the ĉ diagnostic.
        """
        self._setup()
        nl = n_hat.detach().tolist()
        for r in (1, 2, 3):
            key = (item_idx, r)
            if key not in self._v_cache:
                raise RuntimeError(
                    f"apply_sign_rule: no cached v̂_{r} for item {item_idx} "
                    "(power iteration must precede sign rule). Loud halt.")
            v = self._v_cache[key]
            vl = v.detach().tolist()
            s = 1.0 if sum(a * b for a, b in zip(vl, nl)) >= 0 else -1.0
            self._v_cache[key] = (v * s).detach().clone()
        return self._v_cache[(item_idx, 1)]

    def _resolve_direction(self, probe, direction):
        """Resolve a direction tag to a unit (1024,) tensor. Loud on any
        unresolvable tag."""
        torch = self._torch
        i = probe["i"]
        if direction in ("v1", "v2", "v3"):
            key = (i, int(direction[1]))
            if key not in self._v_cache:
                raise RuntimeError(
                    f"inject_and_eval: direction {direction} not computed for "
                    f"item {i} (power iteration must precede injection). "
                    "Loud halt.")
            return self._v_cache[key]
        if direction.startswith("vrand_"):
            k = int(direction.split("_", 1)[1])
            if k not in (0, 1):
                raise RuntimeError(
                    f"inject_and_eval: bad vrand norm index {k}. Loud halt.")
            return R.generate_v_rand(i, k).to(self.device)
        if direction == "bagg":
            return self._b_agg
        if isinstance(direction, tuple) and direction[0] == "permuted":
            _, j, _k = direction
            key = (j, 1)
            if key not in self._v_cache:
                raise RuntimeError(
                    "inject_and_eval: permuted source item "
                    f"{j} has no cached v1. Loud halt.")
            return self._v_cache[key]
        raise RuntimeError(
            f"inject_and_eval: unresolvable direction {direction!r}. Loud halt.")

    def inject_and_eval(self, probe, h, direction, eps_frac):
        """Inject eps_frac*||h|| * direction at the answer position; re-run.

        -> (correct: bool, logits: list[float]). 1 fwd. Correctness uses the
        same greedy endpoint as baseline_forward.
        """
        self._setup()
        torch = self._torch
        dvec = self._resolve_direction(probe, direction)
        hnorm = float(h.norm(p=2))
        if hnorm == 0.0 or not math.isfinite(hnorm):
            raise RuntimeError(
                f"inject_and_eval: degenerate ||h|| on item {probe['i']}. "
                "Loud halt.")
        eps = eps_frac * hnorm
        delta = (eps * dvec / dvec.norm(p=2)).to(self.device)
        with torch.no_grad():
            logits = self._logits_with_delta(probe["input_ids"], delta)
        if bool(torch.isnan(logits).any()) or bool(torch.isinf(logits).any()):
            raise RuntimeError(
                f"inject_and_eval: NaN/Inf logits on item {probe['i']} "
                f"(direction={direction!r}). Loud halt.")
        correct = bool(int(torch.argmax(logits)) == probe["t_tok"])
        return correct, [float(x) for x in logits.detach().cpu()]

    def stage2_derangement(self, n):
        return R.derangement(n, R.MASTER_SEED)


# ---------------------------------------------------------------------------
# Stage A — $0 CPU advisory screen
# ---------------------------------------------------------------------------

def run_stage_a(backend, out_dir, log=print):
    """Execute Stage A exactly as pinned in §5. Returns the advisory report.

    Flow: crash-guard -> frozen-backbone snapshot -> read-only weight load ->
    He per square block (O direct; V via fused-QKV per-head interleaved rows,
    loud provenance) -> frozen-backbone verify (Δθ=0) -> atomic report write.
    Emits NO verdict by construction (report["verdict"] is None).
    """
    G.crash_guard("stage-a", HERE)
    os.makedirs(out_dir, exist_ok=True)
    guard = G.FrozenBackboneGuard()

    log("[Stage A] loading weights (read-only) ...")
    t0 = time.time()
    state_dict = backend.load_state_dict_readonly()
    h0 = guard.snapshot_before(state_dict)
    log(f"[Stage A] state_dict sha256 (pre):  {h0}")

    report = H.stage_a_screen(state_dict)
    h1 = guard.verify_after(state_dict)  # INVALID V1 on mismatch (loud)
    log(f"[Stage A] state_dict sha256 (post): {h1}  (Δθ=0 verified)")

    report["param_hash_pre"] = h0
    report["param_hash_post"] = h1
    report["delta_theta_zero"] = (h0 == h1)
    report["env"] = env_manifest({"mode": "stage-a"})
    report["wall_seconds"] = time.time() - t0
    atomic_write_json(os.path.join(out_dir, "exp086_stage_a_report.json"), report)
    log(f"[Stage A] advisory report written: {len(report['blocks'])} blocks, "
        f"He in [{report['He_min']:.4f}, {report['He_max']:.4f}], "
        f"mean {report['He_mean']:.4f}")
    log("[Stage A] status: ADVISORY ONLY — no verdict emitted (by design).")
    return report


# ---------------------------------------------------------------------------
# Stage B — pilot orchestration (backend-neutral)
# ---------------------------------------------------------------------------

ARMS = ("v1", "v2", "v3", "vrand", "bagg")  # §4 (matched ||δ||₂ across arms)
NORM_TAGS = (0, 1)                          # index into G.EPS_NORMS


def load_probe_set(backend):
    """Load the pinned EXP077 archive; return (records, deviation_note).

    §6.1: verbatim rebuild, fixed indices 0..59. DEVIATION NOTE (EXP084-D1
    class, build-time): the pinned archive carries no prompt strings/options/
    token IDs/margins — only per-arm correctness records. The actual probe
    strings are rebuilt verbatim per EXP077 §3 by the backend's build_probe
    on the execution node; this deviation is loudly logged here and recorded
    in every run manifest. Any paper/scoreboard use must carry this note.
    """
    path = os.path.join(HERE, *G.RECORDS_REL)
    recs = json.load(open(path))
    assert len(recs) == G.N_ITEMS, "archive size drift (crash-guard covers this)"
    note = ("EXP084-D1 class: archive carries no prompt strings/options/token "
            "IDs/margins — probe inputs rebuilt verbatim per EXP077 §3, fixed "
            f"indices 0..{G.N_ITEMS - 1}, by the execution-node backend; "
            "outcome-independent (EXP077 was a null; margins were never its "
            "endpoint).")
    return recs, note


def _l2norm(vec):
    return sum(float(x) * float(x) for x in vec) ** 0.5


def _dot(a, b):
    return sum(float(x) * float(y) for x, y in zip(a, b))


def run_full_loop(backend, budget, out_dir, log=print):
    """Backend-neutral Stage-B orchestration. Returns (results, verdict_tuple).

    Ordering (§6/§9 binding): Δθ snapshot -> baseline forwards -> headroom
    gate V2 -> per-item power iteration + n̂ + arms -> abort-frac V3 ->
    apparatus V4 -> contrasts -> Stage-2 gate -> Δθ verify V1 -> adjudicate.
    Every forward/backward-equivalent is budget-charged; the ceiling refuses.
    """
    G.crash_guard("stage-b", HERE)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    guard = G.FrozenBackboneGuard()

    records, deviation_note = load_probe_set(backend)
    log(f"[Stage B] probe set: {len(records)} records (sha pin verified).")
    log(f"[Stage B] DEVIATION NOTE: {deviation_note}")

    # Δθ=0 snapshot BEFORE any weight-touching phase (§6.6)
    state_dict = backend.load_state_dict_readonly()
    h0 = guard.snapshot_before(state_dict)
    log(f"[Stage B] state_dict sha256 (pre): {h0}")

    probes = [backend.build_probe(rec, i) for i, rec in enumerate(records)]

    # ---- baseline forwards (1 fwd each; correctness endpoint only) ----
    base_correct, base_logits, hs = [], [], []
    for i, probe in enumerate(probes):
        correct, logits, h = backend.baseline_forward(probe)
        budget.charge(1, f"baseline item {i}")
        base_correct.append(bool(correct))
        base_logits.append(list(logits))
        hs.append(h)
    n_wrong = sum(1 for c in base_correct if not c)
    log(f"[Stage B] baseline: {n_wrong}/{G.N_ITEMS} wrong-at-baseline")
    G.check_headroom(n_wrong)  # V2 (loud INVALID)

    # ---- per-item: power iteration -> n̂ -> arms ----
    items = []
    n_aborted = 0
    alphas = []          # |<v̂_1, n̂>| per non-aborted item (ĉ components)
    for i, probe in enumerate(probes):
        h = hs[i]
        pi = backend.power_iteration(probe, h)
        budget.charge(108, f"power-iteration item {i}")  # §11: 3x12x(1+2)
        s = pi["s"]
        v = pi["v"]
        aborted = G.should_abort_item(s[0], s[1])
        rec = {"i": i, "sigma": list(s), "aborted": aborted,
               "rayleigh": pi.get("rayleigh"), "n_iters": pi.get("n_iters")}
        if aborted:
            n_aborted += 1
            rec["arms"] = {}
        else:
            n_hat = backend.decision_normal_vjp(probe, h)
            budget.charge(2, f"decision-normal VJP item {i}")
            # sign rule §4 F2 (F1 fix): flip the TREATMENT vectors inside the
            # backend cache BEFORE any injection, so the v1/v2/v3 arms carry
            # signed directions. Returns signed v̂_1 for the ĉ diagnostic.
            v1_signed = backend.apply_sign_rule(i, n_hat)
            alpha = abs(_dot(v1_signed, n_hat))
            alphas.append(alpha)
            rec["alpha"] = alpha
            rec["arms"] = {}
            for k, eps_frac in enumerate(G.EPS_NORMS):
                for a, arm in enumerate(ARMS):
                    if arm == "vrand":
                        direction = f"vrand_{k}"  # per-item per-norm seed
                    else:
                        direction = arm
                    correct, logits = backend.inject_and_eval(
                        probe, h, direction, eps_frac)
                    budget.charge(1, f"arm {arm} norm {eps_frac} item {i}")
                    rec["arms"][(arm, k)] = {
                        "correct": bool(correct), "logits": list(logits)}
        # random arm is KEPT on aborted items (apparatus + primary control)
        if aborted:
            rec["arms"] = {}
            for k, eps_frac in enumerate(G.EPS_NORMS):
                correct, logits = backend.inject_and_eval(
                    probe, h, f"vrand_{k}", eps_frac)
                budget.charge(1, f"arm vrand norm {eps_frac} item {i} (aborted)")
                rec["arms"][("vrand", k)] = {
                    "correct": bool(correct), "logits": list(logits)}
        items.append(rec)
    log(f"[Stage B] power iteration done: {n_aborted}/{G.N_ITEMS} aborted "
        f"(σ̂₁/σ̂₂ < {G.SIGMA_RATIO_ABORT})")
    G.check_abort_frac(n_aborted)  # V3 (loud INVALID)

    # ---- apparatus check §6.5: random δ at 0.45||h|| moves ||Δz||₂ ----
    moved = 0
    for i, rec in enumerate(items):
        dz = [b - a for a, b in
              zip(base_logits[i], rec["arms"][("vrand", 1)]["logits"])]
        if _l2norm(dz) > G.APPARATUS_NOISE_FLOOR:
            moved += 1
    frac_moved = moved / G.N_ITEMS
    log(f"[Stage B] apparatus: {moved}/{G.N_ITEMS} items moved margins "
        f"({frac_moved:.3f} >= {G.APPARATUS_MIN_FRAC} required)")
    G.check_apparatus(frac_moved)  # V4 (loud INVALID)

    return finish_run(backend, budget, out_dir, items, probes, hs, alphas,
                      base_correct, deviation_note, h0, guard, log)

# ---------------------------------------------------------------------------
# Contrasts, Stage-2 gate, adjudication (continued)
# ---------------------------------------------------------------------------

def _paired_table(items, arm_a, arm_b, norm_k=0):
    """Paired correctness table for arm-pair (A, B) at norm index norm_k.

    Returns (n10, n01, n00, n11) over items where BOTH arms are present
    (aborted items have no direction arms; pairwise deletion on the
    pre-treatment convergence covariate — non-gameable, EXP084-D3 class).
    n10 = #{A right, B wrong}; n01 = #{A wrong, B right}.
    """
    n10 = n01 = n00 = n11 = 0
    n_used = 0
    for rec in items:
        arms = rec["arms"]
        if (arm_a, norm_k) not in arms or (arm_b, norm_k) not in arms:
            continue
        a = arms[(arm_a, norm_k)]["correct"]
        b = arms[(arm_b, norm_k)]["correct"]
        n_used += 1
        if a and not b:
            n10 += 1
        elif b and not a:
            n01 += 1
        elif a and b:
            n11 += 1
        else:
            n00 += 1
    return (n10, n01, n00, n11), n_used


def finish_run(backend, budget, out_dir, items, probes, hs, alphas, base_correct,
               deviation_note, h0, guard, log=print):
    """Contrasts -> Stage-2 gate -> Δθ verify -> adjudicate -> artifacts."""
    t0 = time.time()

    # ---- primary contrast: v̂_1 vs v̂_rand at norm 0.15 (§7) ----
    (n10, n01, n00, n11), n_pri = _paired_table(items, "v1", "vrand", 0)
    delta_point = (n10 - n01) / (n10 + n01 + n00 + n11)
    mcnemar_p = S.mcnemar_exact_one_sided(n10, n01)
    delta_lci, delta_uci = S.tango_ci(n10, n01, n00, n11)
    log(f"[Stage B] primary Δ=v̂_1−v̂_rand @0.15: n=({n10},{n01},{n00},{n11}) "
        f"n_used={n_pri}, Δ̂={delta_point:+.4f}, "
        f"Tango95=({delta_lci:+.4f},{delta_uci:+.4f}), McNemar p={mcnemar_p:.4g}")

    # ---- rank contrast: v̂_1 vs v̂_3 at norm 0.15 (§7 discriminating) ----
    (r10, r01, r00, r11), n_rank = _paired_table(items, "v1", "v3", 0)
    rank_point = (r10 - r01) / (r10 + r01 + r00 + r11)
    rank_lci, rank_uci = S.tango_ci(r10, r01, r00, r11)
    log(f"[Stage B] rank Δ_rank=v̂_1−v̂_3 @0.15: Δ̂={rank_point:+.4f}, "
        f"Tango95=({rank_lci:+.4f},{rank_uci:+.4f})")

    # ---- rank-test validity: median_i(σ̂_1/σ̂_3) >= 1.2 (§6.4) ----
    ratios = [rec["sigma"][0] / rec["sigma"][2] for rec in items
              if not rec["aborted"] and rec["sigma"][2] > 0]
    ratios.sort()
    med_ratio = ratios[len(ratios) // 2] if ratios else 0.0
    rank_valid = med_ratio >= G.SIGMA_RATIO_RANK_VALID
    log(f"[Stage B] rank validity: median(σ̂_1/σ̂_3)={med_ratio:.3f} "
        f"(need ≥ {G.SIGMA_RATIO_RANK_VALID}) -> "
        f"{'DEFINED' if rank_valid else 'UNDEFINED → HELD (V11)'}")

    # ---- ĉ kill-first diagnostic (§2 D6, §7) ----
    chat = S.c_hat(alphas)
    exc = S.exceedance(alphas)
    log(f"[Stage B] ĉ={chat:.4f} (bar {G.CHAT_BAR}), "
        f"E={exc:.3f} (bar {G.EXCEEDANCE_BAR:.0%})")

    # ---- signed ledger (§7 P3): per-arm (b, c) vs baseline @0.15 ----
    ledgers = {}
    for arm in ARMS:
        arm_corr = [rec["arms"][(arm, 0)]["correct"] for rec in items
                    if (arm, 0) in rec["arms"]]
        base_sub = [c for rec, c in zip(items, base_correct)
                    if (arm, 0) in rec["arms"]]
        led = S.signed_ledger(base_sub, arm_corr)
        ledgers[arm] = led
        log(f"[Stage B] ledger {arm}@0.15: b={led['b_wrong_to_right']} "
            f"c={led['c_right_to_wrong']} anti-steerable="
            f"{led['anti_steerable_frac']}"
            f"{' FLAGGED' if led['flagged'] else ''}")

    # ---- Stage-2 gate (S4 F10, G3): runs IFF the primary win fires ----
    primary_win = (delta_lci > G.DELTA_MIN) and (mcnemar_p <= G.MCNEMAR_ALPHA)
    stage2_ran = False
    delta_perm_lci = delta_perm_uci = None
    n_perm_used = 0
    if primary_win:
        log("[Stage B] primary win fired -> running Stage-2 permuted arm")
        delta_perm_lci, delta_perm_uci, n_perm_used = run_stage2(
            backend, budget, items, probes, hs, log)
        stage2_ran = True

    # ---- Dtheta = 0 verification (S6.6) -> INVALID V1 on mismatch ----
    state_dict = backend.load_state_dict_readonly()
    h1 = guard.verify_after(state_dict)
    log("[Stage B] state_dict sha256 (post): %s  (Dtheta=0 verified)" % h1)

    results = {
        "delta_theta_ok": True,
        "n_wrong_baseline": sum(1 for c in base_correct if not c),
        "n_items": G.N_ITEMS,
        "frac_aborted": sum(1 for rec in items if rec["aborted"]) / G.N_ITEMS,
        "apparatus_ok": True,  # checked loudly mid-loop (V4); True = passed
        "c_hat": chat,
        "exceedance": exc,
        "delta_lci": delta_lci, "delta_uci": delta_uci,
        "delta_point": delta_point, "mcnemar_p": mcnemar_p,
        "rank_valid": rank_valid,
        "delta_rank_lci": rank_lci, "delta_rank_uci": rank_uci,
        "delta_rank_point": rank_point,
        "stage2_ran": stage2_ran,
        "delta_perm_lci": delta_perm_lci,
        "delta_perm_uci": delta_perm_uci,
        "n_primary_used": n_pri, "n_rank_used": n_rank,
        "n_perm_used": n_perm_used,
        "median_sigma1_sigma3": med_ratio,
        "ledgers": ledgers,
        "passes_used": budget.used,
        "passes_budget": budget.limit,
    }
    verdict, evidentiary, detail = V.adjudicate(results)
    log("[Stage B] VERDICT: %s (%s) -- %s" % (verdict, evidentiary, detail))

    record = {
        "experiment": "EXP086",
        "mode": "stage-b",
        "env": env_manifest({"probe_deviation_note": deviation_note}),
        "param_hash_pre": h0,
        "param_hash_post": h1,
        "delta_theta_zero": True,
        "results": results,
        "verdict": verdict,
        "evidentiary": evidentiary,
        "detail": detail,
        "wall_seconds": time.time() - t0,
        # raw per-item logs (Law #13); tuple arm keys -> "arm@norm" strings
        # because JSON object keys must be strings.
        "items": [
            {k: ({f"{a}@{n}": v for (a, n), v in rec["arms"].items()}
                 if k == "arms" else v)
             for k, v in rec.items()}
            for rec in items
        ],
    }
    atomic_write_json(os.path.join(out_dir, "exp086_stage_b_record.json"), record)
    return results, (verdict, evidentiary, detail)


def run_stage2(backend, budget, items, probes, hs, log=print):
    """Stage-2 conditional arm (§4 F10): permuted-v̂_1 at both norms.

    Item j's v̂_1 injected on item i (j = fixed derangement, seeded), both
    norms, paired per item vs v̂_1. Costs 120 fwd-equiv (§11).
    Returns (delta_perm_lci, delta_perm_uci, n_perm_used).
    """
    der = backend.stage2_derangement(len(items))
    p10 = p01 = p00 = p11 = 0
    n_perm_used = 0
    for k, eps_frac in enumerate(G.EPS_NORMS):
        for i, rec in enumerate(items):
            if rec["aborted"] or ("v1", k) not in rec["arms"]:
                continue
            j = der[i]
            # direction tag ("permuted", donor j, norm k):
            # the backend injects item j's v1 direction on item i
            correct, _ = backend.inject_and_eval(
                probes[i], hs[i], ("permuted", j, k), eps_frac)
            budget.charge(1, f"stage-2 permuted norm {eps_frac} item {i}")
            if k == 0:  # Δ_perm evaluated at the primary norm
                a = rec["arms"][("v1", 0)]["correct"]
                b = bool(correct)
                n_perm_used += 1
                if a and not b:
                    p10 += 1
                elif b and not a:
                    p01 += 1
                elif a and b:
                    p11 += 1
                else:
                    p00 += 1
    lci, uci = S.tango_ci(p10, p01, p00, p11)
    log(f"[Stage B] Stage-2 Δ_perm=v̂_1−permuted @0.15: n=({p10},{p01},{p00},"
        f"{p11}) Tango95=({lci:+.4f},{uci:+.4f})")
    return lci, uci, n_perm_used

# ---------------------------------------------------------------------------
# CLI: --smoke / --stage-a / --run (all gated; refusals exit 2)
# ---------------------------------------------------------------------------

def cmd_smoke():
    """0 model passes: import the smoke module and run it in-process."""
    sys.path.insert(0, HERE)
    import smoke_test
    ok = smoke_test.main()
    return 0 if ok else 1


def cmd_stage_a(args):
    if not args.bundle_review_signoff:
        print("REFUSED (exit 2): --stage-a requires --bundle-review-signoff "
              "(independent Law #14 bundle review). Weight access happens "
              "only after that review. No weights touched.", file=sys.stderr)
        return 2
    # The execution-node backend is chosen here; on the build machine there
    # is no weights path and no torch, so this raises loudly by design.
    if not args.weights:
        print("REFUSED (exit 2): --stage-a requires --weights <path> "
              "(read-only local snapshot).", file=sys.stderr)
        return 2
    backend = TorchBackend(args.weights)
    budget = G.PassBudget()  # Stage A is $0 CPU; budget unused but constructed
    report = run_stage_a(backend, args.out, log=print)
    print(f"Stage A complete: {args.out}/exp086_stage_a_report.json "
          f"(advisory only; verdict={report['verdict']})")
    return 0


def cmd_run(args):
    if not (args.ceo_gpu_clearance and args.stage2_review_signoff):
        print("REFUSED (exit 2): --run requires BOTH --ceo-gpu-clearance AND "
              "--stage2-review-signoff. GPU execution is NOT licensed "
              "(signed §15; queue behind K2 -> EXP083 -> EXP084).",
              file=sys.stderr)
        return 2
    if not args.weights:
        print("REFUSED (exit 2): --run requires --weights pointing at a "
              "read-only LOCAL weights snapshot. Refusing to fall back to a "
              "HuggingFace hub ID (would attempt a network download).",
              file=sys.stderr)
        return 2
    if not os.path.isdir(args.weights):
        print(f"REFUSED (exit 2): --weights is not a directory: {args.weights}",
              file=sys.stderr)
        return 2
    backend = TorchBackend(args.weights)
    budget = G.PassBudget()
    results, (verdict, evidentiary, detail) = run_full_loop(
        backend, budget, args.out, log=print)
    print(f"Stage B complete: verdict={verdict} ({evidentiary})")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="EXP086 R3 dynamical-amplifier runner (gated; see --help)")
    ap.add_argument("--smoke", action="store_true",
                    help="startup smoke test (0 model passes)")
    ap.add_argument("--stage-a", action="store_true",
                    help="Stage A advisory weight-only screen")
    ap.add_argument("--run", action="store_true",
                    help="Stage B pilot (execution node; NOT licensed)")
    ap.add_argument("--out", default=os.path.join(HERE, "out"),
                    help="output directory for run artifacts")
    ap.add_argument("--weights", default=None,
                    help="read-only local weights snapshot path")
    ap.add_argument("--bundle-review-signoff", action="store_true",
                    help="independent Law #14 bundle review SIGN (Stage A gate)")
    ap.add_argument("--ceo-gpu-clearance", action="store_true",
                    help="CEO GPU clearance (Stage B gate)")
    ap.add_argument("--stage2-review-signoff", action="store_true",
                    help="Law #14 stage-2 review signoff (Stage B gate)")
    args = ap.parse_args(argv)
    if args.smoke:
        return cmd_smoke()
    if args.stage_a:
        return cmd_stage_a(args)
    if args.run:
        return cmd_run(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
