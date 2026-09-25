#!/usr/bin/env python3
"""EXP084 runner: R2 Newton-vs-gradient duel (GPU node only).

Implements the signed protocol
experiments/protocols/EXP084_R2_NEWTON_DUEL_PREREG_SIGNED.md
(Law #14 final SIGN LOG-264).

Five arms (§4): (a) GD-1, (b) Newton (natural length, defined iff
κ̂_dir < −κ_floor), (c) random, (d) re-linearized 3-step GD (cost-fair),
(e) permuted-Newton. Label-free top-2 margin proxy only (§2).

Pass budget (§6, binding): 240 forward + 72 backward = 384 fwd-equiv.
The runner counts every pass and REFUSES pass 385 (hard stop).

Verdict precedence (§7, binding):
  INVALID(i)-(iv) -> sensitivity -> CONTINUE -> HELD(win-not-curv)
  -> HELD(step-noise) -> KILL -> HELD(straddle).

GPU-NODE ONLY: requires torch + transformers + the pinned model weights.
Does NOT run on the CPU build machine (raises RuntimeError without torch).
No weights are modified (Δθ ≡ 0; SHA-256 pre/post guard, §1).
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

# --- Signed pins (§1, §4) ---------------------------------------------------
MODEL_ID = "EleutherAI/pythia-410m"
PINNED_SHA256 = "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd"
LAYER_INDEX = 20          # 0-indexed residual stream (EXP077 site)
RHO = 1.0                 # GD step norm (§4)
DELTA = 0.1               # curvature probe spacing (§3)
N_ITEMS = 24
MASTER_SEED = 20260924

# Pass budget (§6): per item 10 fwd + 3 bwd; N=24 -> 240 fwd + 72 bwd.
FWD_BUDGET = 240
BWD_BUDGET = 72

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp084_guards as G
import exp084_rng as R
import exp084_statistics as S
import exp084_spearman as SP


class PassBudget:
    """Hard pass counter. Refuses to exceed the signed ceiling."""

    def __init__(self, fwd=FWD_BUDGET, bwd=BWD_BUDGET):
        self.fwd_limit = fwd
        self.bwd_limit = bwd
        self.fwd = 0
        self.bwd = 0

    def charge_fwd(self, n=1):
        if self.fwd + n > self.fwd_limit:
            raise RuntimeError(
                f"PASS CEILING REFUSED: forward {self.fwd}+{n} > {self.fwd_limit}. "
                "Signed budget is 240 forward passes; pass 241 is refused."
            )
        self.fwd += n

    def charge_bwd(self, n=1):
        if self.bwd + n > self.bwd_limit:
            raise RuntimeError(
                f"PASS CEILING REFUSED: backward {self.bwd}+{n} > {self.bwd_limit}. "
                "Signed budget is 72 backward passes; pass 73 is refused."
            )
        self.bwd += n

    def fwd_equiv(self):
        return self.fwd + 2 * self.bwd


def sha256_state_dict(model):
    """SHA-256 over state_dict tensors (sorted keys, CPU, float32 bytes).

    Byte convention: tensors ONLY (no key names) — matches the historical
    EXP077 hashing code (run_exp077.py: sha.update(tensor.float32.bytes)),
    which produced the pinned hash 4c242d9a…48dd. Hashing key names as well
    would NOT reproduce the pin.
    """
    import torch
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu().to(torch.float32)
        h.update(t.numpy().tobytes())
    return h.hexdigest()


def margin_from_logits(logits):
    """Top-2 margin proxy M(h) = z1 - z2 (§2). No labels involved."""
    top2 = sorted(logits, reverse=True)[:2]
    return top2[0] - top2[1]


def adjudicate(results):
    """Apply the §7 verdict table in fixed precedence order.

    results dict carries: n_defined, sens_p (F2), wilcoxon p-values for
    (a)-(d), spearman p (e), median_b_minus_d, hl_hi (flagship KILL prongs),
    median_b_minus_a, hl_hi_b_minus_a (narrow-KILL prongs on ΔM_b − ΔM_a),
    exclusion split.
    Returns (verdict_label, evidentiary, detail, secondary), where secondary
    is None or the dict {"verdict": "KILL(directional, narrow)",
    "evidentiary": "Not supported", "detail": ...}.

    The §7 "KILL (directional, narrow)" row (same criteria on ΔM_b − ΔM_a,
    "reported secondary") is evaluated at its §7 row position — after the
    flagship KILL check, before the HELD(straddle) fall-through — and is
    reported as a secondary kill alongside the primary verdict. It never
    replaces the primary verdict (LOG-266 Fix 2): a firing narrow kill can
    no longer be misreported as HELD(straddle). INVALID rows preempt all
    scientific rows, so no secondary is reported on INVALID.
    """
    # INVALID (iii): defined < 12
    if G.check_invalid_iii(results["n_defined"]):
        return ("INVALID/UNDEFINED-LANDSCAPE", "Underdetermined",
                f"arm (b) defined (κ̂_dir < −κ_floor) on "
                f"{results['n_defined']} of 24 items (< 12)",
                None)
    # INVALID (iv): F2 sensitivity precondition fails
    if results["sens_p"] > 0.10:
        return ("INVALID/UNINFORMATIVE-PROXY", "Underdetermined",
                f"F2 sensitivity p={results['sens_p']:.4f} > 0.10; apparatus dead",
                None)
    a = results["p_newton_vs_gdcostfair"] <= 0.05
    b = results["p_newton_vs_random"] <= 0.05
    c = results["p_newton_vs_gd1"] <= 0.05
    d = results["p_newton_vs_permuted"] <= 0.05
    e = results["spearman_p"] <= 0.10
    if a and b and c and d and e:
        return ("CONTINUE", "Inconclusive",
                "all conjuncts (a)-(e) hold; licenses curvature-spectrum study (≤660 passes)",
                None)
    if a and b and c and d and not e:
        return ("HELD(win-not-curvature-explained)", "Inconclusive",
                "(a)-(d) hold but dose-response (e) fails: win not curvature-explained",
                None)
    if a and (not b or not d):
        return ("HELD(step-noise)", "Inconclusive",
                "(a) holds but (b) or (d) fails: step-noise / non-item-specific",
                None)
    med = results["median_b_minus_d"]
    hi = results["hl_hi"]
    if med <= 0 and hi < S.KILL_BAR:
        primary = ("KILL(flagship, cost-fair)", "Not supported",
                   f"median(ΔM_b−ΔM_d)={med:.4f} ≤ 0 and HL95 upper={hi:.4f} < 0.01")
    else:
        primary = ("HELD(straddle)", "Inconclusive",
                   "none of the above (incl. HL CI straddling +0.01)")
    # KILL (directional, narrow), §7: same criteria on ΔM_b − ΔM_a.
    # Reported secondary alongside the primary verdict; never shadows it.
    med_a = results["median_b_minus_a"]
    hi_a = results["hl_hi_b_minus_a"]
    secondary = None
    if med_a <= 0 and hi_a < S.KILL_BAR:
        secondary = {
            "verdict": "KILL(directional, narrow)",
            "evidentiary": "Not supported",
            "detail": (f"median(ΔM_b−ΔM_a)={med_a:.4f} ≤ 0 and HL95 upper={hi_a:.4f} < 0.01; "
                       "kills only the per-step-quality claim (§7, reported secondary)"),
        }
    return primary + (secondary,)


# --- Run-halting errors ---------------------------------------------------
class InvalidRunError(RuntimeError):
    """INVALID(i)/(ii): apparatus failure — no verdict is produced.

    invalid_row: "i" (SHA-256 pre/post mismatch, or pre-run != pinned guard)
                 or "ii" (P0 identity mismatch vs archived baseline).
    Per §7 both halt before any scientific verdict is emitted.
    """
    def __init__(self, invalid_row, msg):
        super().__init__(f"INVALID({invalid_row}): {msg}")
        self.invalid_row = invalid_row


class BaselinePrepassHalt(RuntimeError):
    """Verdict-clean pre-pass halt: P0 baseline archived on the first run.

    Binding per LOG-269 D2: when no baseline archive exists, check_identity
    archives M0 and raises this — NO scientific arms, NO verdict — so the
    binding §7 INVALID(ii) row stays a live guard on the only run that
    counts (the re-run replays the archive and enforces bit-for-bit
    identity). Nothing is invalid on the first run, hence this is NOT an
    InvalidRunError. The message carries the re-run instruction; cmd_run
    catches it separately to print the re-run directive.
    """


class ApparatusError(RuntimeError):
    """Apparatus failure outside the §7 INVALID rows (fail loud, no verdict).

    Used for protocol-silence cases where construction is impossible:
    missing/unverifiable probe-set records file, zero gradient (unit
    gradient undefined), etc. Never silently worked around.
    """


# --- Probe-set benchmark: verbatim port of the EXP077 §3 bench builder -----
# Source: experiments/runs/exp077/run_exp077.py (N_BENCH=60 block), itself
# ported verbatim from experiments/runs/exp078/run_exp078.py §2 (Law #9: no
# new benchmark construction). Constants and all four loops reproduced
# exactly. Item dicts keep ent/typ for the archive-alignment audit.
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


def build_benchmark():
    """Rebuild the 60 EXP077 bench prompts verbatim (K2 precedent).

    Returns 60 dicts {id, prompt, ent, typ}. The margin proxy is label-free,
    so only the prompt STRINGS matter for bit-identity with the EXP077 site;
    ent/typ are kept for the archive-alignment audit.
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
                      "ent": A, "typ": "planet"})
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
                      "ent": A, "typ": "planet"})
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
                      "ent": A, "typ": "element"})
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
                      "ent": A, "typ": "element"})
    assert len(bench) == 60, f"expected 60 bench items, got {len(bench)}"
    return bench


# Pinned probe-set records file (protocol R5d).
RECORDS_REL = os.path.join("..", "EXP077_cone_vs_line",
                            "exp077_instance_records.json")
RECORDS_SHA256 = ("47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585")
BASELINE_FILENAME = "exp084_baseline_margins.json"


def load_probe_set(records_path, log):
    """Probe-set preflight (§2, R5d).

    Verifies the pinned EXP077 instance-records file (sha256 vs the R5d pin
    — binding integrity check), rebuilds the 60 bench prompts verbatim, and
    returns the fixed 24-item probe set (rebuilt indices 0..23).

    PROTOCOL GAP — stage-2 review (binding): the literal "items 0–23 in
    archived order" cannot be implemented as written: the pinned records
    file carries no prompt strings, and its array order does not match this
    builder's order (audit count logged below; the archive is entity-grouped
    six-per-entity, which no in-repo builder produces, and correctness
    signatures are non-unique so signature-matching is impossible). The
    adopted reading preserves the protocol's intent — a FIXED probe set
    with NO outcome conditioning (LOG-262): verbatim EXP077 §3 rebuild,
    indices 0..23. Recorded here and in the run manifest; NOT silently
    reinterpreted. The stage-2 Law #14 review adjudicates this reading.
    """
    if not os.path.exists(records_path):
        raise ApparatusError(
            f"probe-set records file missing: {records_path} "
            "(R5d pin cannot be verified; fail loud)")
    with open(records_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    if sha != RECORDS_SHA256:
        raise ApparatusError(
            f"probe-set records sha256 {sha} != R5d pin {RECORDS_SHA256}")
    records = json.load(open(records_path))
    bench = build_benchmark()

    def _align(lo, hi):
        return sum(1 for i in range(lo, hi)
                   if i < len(records)
                   and records[i].get("ent") == bench[i]["ent"]
                   and records[i].get("typ") == bench[i]["typ"])
    a24, a60 = _align(0, N_ITEMS), _align(0, 60)
    log(f"probe-set records sha256 verified vs R5d pin ({sha[:16]}…)")
    log(f"PROBE-SET DEVIATION (stage-2 review): rebuilt (ent,typ) matches "
        f"archived records at {a24}/24 probe indices ({a60}/60 overall); "
        "the archive carries no prompt strings, so literal 'items 0–23 in "
        "archived order' is unimplementable — adopted reading: verbatim "
        "EXP077 §3 rebuild, fixed indices 0..23 (outcome-independent).")
    return {"prompts": [b["prompt"] for b in bench[:N_ITEMS]],
            "alignment_24": a24, "alignment_60": a60,
            "records_sha": sha}


def check_identity(M0, baseline_path, log):
    """INVALID(ii): P0 identity arm — bit-for-bit vs archived baseline.

    Runs AFTER all 24 P0 forwards and BEFORE any scientific arm (§7 order).
    First run (no archive exists): archives M0 (identity arm $0 by archive;
    EXP083 precedent) then raises BaselinePrepassHalt — a verdict-clean
    pre-pass halt (LOG-269 D2 binding): no scientific arms, no verdict.
    The re-run replays the archive and enforces INVALID(ii) bit-for-bit,
    keeping the binding §7 row a live guard on the only run that counts
    (the archive-and-continue self-certifying guard is forbidden).
    Later runs: exact float equality — JSON round-trips float64 bit-exactly
    via repr, so == is a bit-for-bit comparison. Mismatch -> INVALID(ii),
    no verdict.
    """
    M0 = [float(m) for m in M0]
    if not os.path.exists(baseline_path):
        payload = {
            "model_id": MODEL_ID,
            "n_items": N_ITEMS,
            "m0": M0,
            "note": ("EXP084 P0 baseline margins (identity arm archive). "
                     "Established by the verdict-clean pre-pass run "
                     "(LOG-269 D2 binding); the loop halted verdict-clean "
                     "after archiving. Later runs replay this archive and "
                     "must match bit-for-bit (INVALID(ii) otherwise)."),
        }
        tmp = baseline_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(payload, f)
        os.replace(tmp, baseline_path)
        log(f"P0 identity: no archive found — archived {N_ITEMS} M0 values "
            f"(first run; identity arm $0 by archive); halting verdict-clean")
        raise BaselinePrepassHalt(
            f"P0 baseline archived ({N_ITEMS} M0 values to {baseline_path}) "
            "— pre-pass complete; re-run the loop for the full execution "
            "(INVALID(ii) will be enforced bit-for-bit on the replay)")
    rec = json.load(open(baseline_path))
    if rec.get("m0") != M0:
        bad = sum(1 for a, b in zip(rec.get("m0", []), M0) if a != b)
        raise InvalidRunError(
            "ii",
            f"P0 identity mismatch vs archived baseline: {bad}/{N_ITEMS} "
            f"margins differ bit-for-bit; session invalid, no verdict")
    log(f"P0 identity: {N_ITEMS}/{N_ITEMS} M0 bit-for-bit match vs archive")


# --- Backend interface -------------------------------------------------------
# A backend implements:
#   set_prompts(prompts24)
#   state_hash() -> hex str                      (no pass charged)
#   p0(i) -> (m0: float, ctx)                    (charges 1 fwd, grad on)
#   grad_from_ctx(ctx) -> vec                     (charges 1 bwd)
#   eval_margin(i, offset) -> float               (charges 1 fwd, no grad)
#   eval_margin_and_grad(i, offset) -> (float, vec)  (charges 1 fwd + 1 bwd)
#   random_direction(i) -> vec                    (deterministic; no pass)
#   derangement() -> [der(i)]                     (fixed; no pass)
#   vadd(a,b), vscale(a,c), vneg(a), vnorm(a) -> float
# vecs are opaque (torch tensors live, tuples in the mock).
# Greedy decoding throughout: no sampling randomness in any forward pass.


class TorchBackend:
    """Live Pythia-410m backend (GPU node only).

    Layer-20 answer-position residual hook on model.gpt_neox.layers[20]
    (the EXP077 boundary-null site); the answer position is the last prompt
    token. Gradients are activation-leaf readouts via torch.autograd.grad —
    no optimizer exists anywhere in this file, and every parameter has
    requires_grad_(False), so weight gradients are impossible by
    construction (Δθ≡0 beyond the SHA-256 pre/post guard). Every forward
    and backward charges the PassBudget (hard refusal at 241/73).
    """

    HIDDEN = 1024  # Pythia-410m hidden size (protocol §1)

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
        layer = self.model.gpt_neox.layers[LAYER_INDEX]
        self._offset = None
        self._captured = None
        layer.register_forward_hook(self._hook)
        self._prompts = None
        log("model loaded on cuda; params frozen (requires_grad_(False)); "
            "eval mode; deterministic algorithms on")

    # -- hook --
    def _hook(self, module, inputs, output):
        x = output[0] if isinstance(output, tuple) else output
        x = x.clone()
        if self._offset is not None:
            x[:, -1, :] = x[:, -1, :] + self._offset
        self._captured = x[:, -1, :]
        if isinstance(output, tuple):
            return (x,) + tuple(output[1:])
        return x

    def set_prompts(self, prompts):
        self._prompts = list(prompts)

    def state_hash(self):
        return sha256_state_dict(self.model)

    # -- vector ops (torch tensors) --
    def vadd(self, a, b):
        return a + b

    def vscale(self, a, c):
        return a * c

    def vneg(self, a):
        return -a

    def vnorm(self, a):
        return float(self.torch.linalg.vector_norm(a))

    def random_direction(self, i):
        return R.generate_r_hat(i).to(self.device)

    def derangement(self):
        return R.derangement(N_ITEMS)

    # -- pass primitives --
    def _forward(self, i, offset, need_grad):
        torch = self.torch
        self._offset = offset
        self._captured = None
        ids = self.tok(self._prompts[i], return_tensors="pt").to(self.device)
        ctx = torch.enable_grad() if need_grad else torch.no_grad()
        with ctx:
            out = self.model(**ids)
            last = out.logits[0, -1, :]
            top2 = torch.topk(last, 2).values
            M = top2[0] - top2[1]  # z1 - z2, label-free (§2)
        h = self._captured
        self.budget.charge_fwd()  # hard refusal at 241
        return M, h

    def p0(self, i):
        """Clean baseline forward (grad enabled); returns (M0, ctx)."""
        M, h = self._forward(i, None, True)
        return float(M.detach()), {"M": M, "h": h}

    def grad_from_ctx(self, ctx):
        """One backward: ∇M w.r.t. the captured activation leaf."""
        g = self.torch.autograd.grad(ctx["M"], ctx["h"])[0]
        self.budget.charge_bwd()  # hard refusal at 73
        return g.reshape(-1).detach()

    def eval_margin(self, i, offset):
        M, _ = self._forward(i, offset, False)
        return float(M)

    def eval_margin_and_grad(self, i, offset):
        M, h = self._forward(i, offset, True)
        g = self.torch.autograd.grad(M, h)[0]
        self.budget.charge_bwd()
        return float(M.detach()), g.reshape(-1).detach()


# --- Orchestration -----------------------------------------------------------
def _unit(backend, g, i, where):
    n = backend.vnorm(g)
    if n == 0.0:
        raise ApparatusError(
            f"item {i}: zero gradient at {where} — unit vector undefined; "
            "apparatus degenerate, no verdict")
    return backend.vscale(g, 1.0 / n), n


def _paired_diffs(x, y, label):
    if len(x) != len(y):
        raise ApparatusError(f"{label}: unpaired inputs ({len(x)} vs {len(y)})")
    diffs = [xi - yi for xi, yi in zip(x, y)]
    S.assert_testable_differences(diffs, label)
    return diffs


def run_full_loop(backend, budget, out_dir, log, records_path, baseline_path,
                  pinned_sha256=PINNED_SHA256):
    """Backend-agnostic EXP084 model loop (§1–§7).

    Phase order (binding): 0. INVALID(i) pre-run SHA vs guard — before any
    pass. 1. Probe-set preflight (R5d archive pin + verbatim rebuild;
    skipped when records_path is None — mock-harness only). 2. P0 identity
    arm: 24 clean forwards + 24 gradient readouts. 3. INVALID(ii) identity
    — before ANY scientific arm. 4. Scientific arms: per item, curvature
    probes, GD-1, re-linearized 3-step GD (g0 sunk/shared per R5c), Newton
    (if defined), random; then Phase B permuted-Newton once all donor steps
    exist. 5. Post-run SHA (Δθ≡0) — before any verdict. 6. Tie/statistics
    validation (fail loud) + require_spearman_table(n_defined) gate before
    conjunct (e). 7. §7 adjudication. 8. Atomic artifact write.

    Returns the run record dict. Raises InvalidRunError("i"/"ii"),
    ApparatusError, S.NonTestableDataError, or BaselinePrepassHalt (first-run
    P0 archive, verdict-clean pre-pass per LOG-269 D2) — all verdict-clean
    halts (no verdict is emitted on any of these paths).
    """
    t0 = time.time()
    # Phase 0 — INVALID(i): SHA guard BEFORE any model pass.
    pre_hash = backend.state_hash()
    log(f"[0] pre-run state SHA-256: {pre_hash}")
    if pre_hash != pinned_sha256:
        raise InvalidRunError(
            "i",
            f"pre-run SHA-256 {pre_hash[:16]}… != guard {pinned_sha256[:16]}…; "
            "no model pass executed")
    # Phase 1 — probe-set preflight.
    if records_path is None:
        ps = {"prompts": None, "alignment_24": None, "alignment_60": None,
              "records_sha": None,
              "note": "probe-set preflight skipped (mock harness)"}
        log("[1] probe-set preflight SKIPPED (mock harness; prompts preset)")
    else:
        ps = load_probe_set(records_path, log)
        backend.set_prompts(ps["prompts"])
    der = backend.derangement()
    if len(der) != N_ITEMS or any(d == i for i, d in enumerate(der)):
        raise ApparatusError("arm (e) derangement invalid (must fix no item)")
    log(f"[1] arm (e) derangement fixed from master seed {R.MASTER_SEED}")
    # Phase 2 — P0 identity arm: 24 clean forwards (+24 activation readouts).
    M0, G0 = [], []
    for i in range(N_ITEMS):
        m0, ctx = backend.p0(i)          # 1 fwd (grad enabled)
        g0 = backend.grad_from_ctx(ctx)  # 1 bwd (activation leaf only)
        ghat, n0 = _unit(backend, g0, i, "clean point")
        M0.append(m0)
        G0.append((g0, ghat, n0))
        log(f"[P0] item {i}: M0={m0:.6f} ||g0||={n0:.6f}")
    # Phase 3 — INVALID(ii): identity BEFORE any scientific arm.
    check_identity(M0, baseline_path, log)
    # Phase 4 — scientific arms.
    per = []
    for i in range(N_ITEMS):
        g0, ghat, n0 = G0[i]
        Mp = backend.eval_margin(i, backend.vscale(ghat, DELTA))    # probe +
        Mm = backend.eval_margin(i, backend.vscale(ghat, -DELTA))   # probe −
        kappa = (Mp - 2.0 * M0[i] + Mm) / (DELTA ** 2)
        defined = G.is_newton_defined(kappa)
        excl = None if defined else G.classify_exclusion(kappa)
        Ma = backend.eval_margin(i, backend.vscale(ghat, RHO))      # arm (a)
        # Arm (d): 3 re-linearized steps, norm RHO/3 each; step 1 reuses the
        # sunk g0 (R5c: arm (d) costs exactly 3 fwd + 2 bwd).
        step = RHO / 3.0
        p = backend.vscale(ghat, step)                              # p1
        _, g1 = backend.eval_margin_and_grad(i, p)                  # 1f + 1b
        g1hat, _ = _unit(backend, g1, i, "arm (d) step 1")
        p = backend.vadd(p, backend.vscale(g1hat, step))            # p2
        _, g2 = backend.eval_margin_and_grad(i, p)                  # 1f + 1b
        g2hat, _ = _unit(backend, g2, i, "arm (d) step 2")
        p = backend.vadd(p, backend.vscale(g2hat, step))            # p3
        Md = backend.eval_margin(i, p)                             # 3rd readout
        # Arm (b): Newton, natural length (no rescaling), if defined.
        Mb, sN, sN_norm = None, None, None
        if defined:
            sN = backend.vscale(ghat, G.newton_step_length(n0, kappa))
            sN_norm = backend.vnorm(sN)
            Mb = backend.eval_margin(i, sN)
        # Arm (c): random direction, norm RHO.
        Mc = backend.eval_margin(
            i, backend.vscale(backend.random_direction(i), RHO))
        per.append({"kappa": kappa, "defined": defined, "exclusion": excl,
                    "Ma": Ma, "Mb": Mb, "Mc": Mc, "Md": Md,
                    "sN": sN, "sN_norm": sN_norm, "Me": None})
        log(f"[arm] item {i}: k̂={kappa:.6f} defined={defined} "
            f"ΔMa={Ma - M0[i]:+.6f} ΔMd={Md - M0[i]:+.6f} "
            f"ΔMb={'n/a' if Mb is None else f'{Mb - M0[i]:+.6f}'} "
            f"ΔMc={Mc - M0[i]:+.6f}")
    # Phase B — arm (e): donor der(i)'s Newton step on item i (all donor
    # steps exist now). Donor-undefined -> Me None -> pairwise deletion in
    # contrast (d); protocol-silent, documented, never imputed.
    for i in range(N_ITEMS):
        sN_donor = per[der[i]]["sN"]
        if sN_donor is not None:
            per[i]["Me"] = backend.eval_margin(i, sN_donor)
    # Phase 5 — post-run SHA-256 (Δθ≡0 binding guard), before any verdict.
    post_hash = backend.state_hash()
    if post_hash != pre_hash:
        raise InvalidRunError("i", "post-run SHA-256 != pre-run (Δθ≠0)")
    log(f"[post] SHA-256 post==pre ({post_hash[:16]}…); Δθ≡0 confirmed; "
        f"passes used: {budget.fwd} fwd + {budget.bwd} bwd "
        f"(={budget.fwd_equiv()} fwd-equiv)")
    # Phase 6–8 — statistics, adjudication, artifact write.
    return compute_statistics(per, M0, der, budget, out_dir, log,
                              pre_hash, ps, t0, pinned_sha256)


def compute_statistics(per, M0, der, budget, out_dir, log,
                       pre_hash, ps, t0, pinned_sha256):
    """Statistics stage: tie validation, table gate, contrasts, verdict."""
    defined_idx = [i for i, p in enumerate(per) if p["defined"]]
    n_defined = len(defined_idx)
    excl_split = {}
    for p in per:
        if not p["defined"]:
            excl_split[p["exclusion"]] = excl_split.get(p["exclusion"], 0) + 1
    log(f"[stats] Newton defined on {n_defined}/24; exclusions={excl_split}")
    # INVALID(iii) preempts the Spearman-table gate (no scientific
    # machinery runs at all on the UNDEFINED-LANDSCAPE path).
    if G.check_invalid_iii(n_defined):
        results = {"n_defined": n_defined, "sens_p": None,
                   "p_newton_vs_gdcostfair": None, "p_newton_vs_random": None,
                   "p_newton_vs_gd1": None, "p_newton_vs_permuted": None,
                   "spearman_p": None, "median_b_minus_d": None,
                   "hl_hi": None, "median_b_minus_a": None,
                   "hl_hi_b_minus_a": None,
                   "exclusion_split": excl_split, "n_e_contrast": 0}
        verdict = adjudicate(results)
        return finish_run(per, M0, der, budget, out_dir, log, pre_hash, ps,
                          t0, pinned_sha256, verdict, results, None)
    # Binding gate BEFORE conjunct (e) and all verdict machinery (LOG-266).
    table_path = SP.require_spearman_table(n_defined)
    log(f"[stats] exact Spearman table n={n_defined} present: {table_path}")
    Mb = [per[i]["Mb"] for i in defined_idx]
    Md = [per[i]["Md"] for i in defined_idx]
    Mc_d = [per[i]["Mc"] for i in defined_idx]
    Ma_d = [per[i]["Ma"] for i in defined_idx]
    Ma_all = [per[i]["Ma"] for i in range(N_ITEMS)]
    Mc_all = [per[i]["Mc"] for i in range(N_ITEMS)]
    # F2 precondition over ALL 24 items (protocol-silent choice, documented:
    # the sensitivity check tests the apparatus/proxy, not the duel subset).
    d_ac = _paired_diffs(Ma_all, Mc_all, "F2: ΔM_a − ΔM_c (n=24)")
    sens_p, w_f2, _ = S.wilcoxon_signed_rank_greater(Ma_all, Mc_all)
    log(f"[stats] F2 sensitivity: p={sens_p:.6f} (W+={w_f2})")
    # INVALID(iv) preempts the scientific contrasts (§7 precedence): on a
    # dead apparatus the duel rows are not computed at all.
    if sens_p > 0.10:
        results = {"n_defined": n_defined, "sens_p": sens_p,
                   "p_newton_vs_gdcostfair": None, "p_newton_vs_random": None,
                   "p_newton_vs_gd1": None, "p_newton_vs_permuted": None,
                   "spearman_p": None, "median_b_minus_d": None,
                   "hl_hi": None, "median_b_minus_a": None,
                   "hl_hi_b_minus_a": None,
                   "exclusion_split": excl_split, "n_e_contrast": 0}
        verdict = adjudicate(results)
        return finish_run(per, M0, der, budget, out_dir, log, pre_hash, ps,
                          t0, pinned_sha256, verdict, results, None)
    # Primary contrasts over the defined set.
    d_bd = _paired_diffs(Mb, Md, "(a) ΔM_b − ΔM_d")
    d_bc = _paired_diffs(Mb, Mc_d, "(b) ΔM_b − ΔM_c")
    d_ba = _paired_diffs(Mb, Ma_d, "(c) ΔM_b − ΔM_a")
    e_idx = [i for i in defined_idx if per[i]["Me"] is not None]
    Me = [per[i]["Me"] for i in e_idx]
    Mb_e = [per[i]["Mb"] for i in e_idx]
    # n_e_contrast: paired set for conjunct (d) (recipient AND donor defined).
    # n_e_evaluated: arm-(e) forwards actually spent (donor defined; the §6
    # per-item inventory counts 1/item, recipient-definedness not conditioned).
    n_e_eval = sum(1 for i in range(24) if per[i]["Me"] is not None)
    d_be = _paired_diffs(Mb_e, Me, "(d) ΔM_b − ΔM_e")
    p_a, _, _ = S.wilcoxon_signed_rank_greater(Mb, Md)
    p_b, _, _ = S.wilcoxon_signed_rank_greater(Mb, Mc_d)
    p_c, _, _ = S.wilcoxon_signed_rank_greater(Mb, Ma_d)
    p_d, _, _ = S.wilcoxon_signed_rank_greater(Mb_e, Me)
    med_bd = S.median(d_bd)
    _, hi_bd, _ = S.hodges_lehmann_ci(Mb, Md)
    med_ba = S.median(d_ba)
    _, hi_ba, _ = S.hodges_lehmann_ci(Mb, Ma_d)
    # Dose-response (e): Spearman(|κ̂_dir|, ΔM_b − ΔM_d), defined set.
    kappas = [abs(per[i]["kappa"]) for i in defined_idx]
    S.assert_no_ties(kappas, "|κ̂_dir| (defined set)")
    S.assert_no_ties(d_bd, "ΔM_b − ΔM_d (defined set)")
    spear_p, _, _, _ = SP.spearman_exact_p_greater(kappas, d_bd)
    log(f"[stats] (a)p={p_a:.6f} (b)p={p_b:.6f} (c)p={p_c:.6f} "
        f"(d)p={p_d:.6f} (n_e={len(e_idx)}) (e)p={spear_p:.6f}")
    log(f"[stats] median(ΔM_b−ΔM_d)={med_bd:.6f} HL95-hi={hi_bd:.6f}; "
        f"median(ΔM_b−ΔM_a)={med_ba:.6f} HL95-hi={hi_ba:.6f}")
    results = {"n_defined": n_defined, "sens_p": sens_p,
               "p_newton_vs_gdcostfair": p_a, "p_newton_vs_random": p_b,
               "p_newton_vs_gd1": p_c, "p_newton_vs_permuted": p_d,
               "spearman_p": spear_p, "median_b_minus_d": med_bd,
               "hl_hi": hi_bd, "median_b_minus_a": med_ba,
               "hl_hi_b_minus_a": hi_ba,
               "exclusion_split": excl_split, "n_e_contrast": len(e_idx),
               "n_e_evaluated": n_e_eval}
    verdict = adjudicate(results)
    return finish_run(per, M0, der, budget, out_dir, log, pre_hash, ps,
                      t0, pinned_sha256, verdict, results, None)


def finish_run(per, M0, der, budget, out_dir, log, pre_hash, ps, t0,
               pinned_sha256, verdict, results, _unused):
    """Write the run manifest + results atomically; log the verdict."""
    verdict_label, evidentiary, detail, secondary = verdict
    items = []
    for i, p in enumerate(per):
        items.append({
            "item": i, "M0": float(M0[i]), "kappa_dir": float(p["kappa"]),
            "newton_defined": p["defined"], "exclusion": p["exclusion"],
            "dM_a": float(p["Ma"] - M0[i]),
            "dM_b": None if p["Mb"] is None else float(p["Mb"] - M0[i]),
            "dM_c": float(p["Mc"] - M0[i]),
            "dM_d": float(p["Md"] - M0[i]),
            "dM_e": None if p["Me"] is None else float(p["Me"] - M0[i]),
            "newton_step_norm": p["sN_norm"],
            "donor": int(der[i]),
        })
    record = {
        "experiment": "EXP084",
        "protocol": ("experiments/protocols/"
                     "EXP084_R2_NEWTON_DUEL_PREREG_SIGNED.md"),
        "model_id": MODEL_ID,
        "pre_sha256": pre_hash,
        "post_sha256": pre_hash,
        "guard_sha256": pinned_sha256,
        "delta_theta": "0 (SHA pre==post)",
        "probe_set": {
            "records_sha256": ps["records_sha"],
            "alignment_24": ps["alignment_24"],
            "alignment_60": ps["alignment_60"],
            "note": ps.get("note") or (
                "verbatim EXP077 §3 rebuild, fixed indices 0..23; "
                "see load_probe_set docstring — stage-2 review adjudicates"),
        },
        "seeds": {"master": R.MASTER_SEED, "item": "20260924+i",
                  "decoding": "greedy (no sampling)"},
        "budget": {"fwd_used": budget.fwd, "bwd_used": budget.bwd,
                   "fwd_limit": budget.fwd_limit,
                   "bwd_limit": budget.bwd_limit,
                   "fwd_equiv": budget.fwd_equiv()},
        "items": items,
        "results": results,
        "verdict": {"label": verdict_label, "evidentiary": evidentiary,
                    "detail": detail, "secondary": secondary},
        "elapsed_s": round(time.time() - t0, 1),
    }
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "exp084_results.json")
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(record, f, indent=1)
    os.replace(tmp, out_path)
    log(f"[done] results -> {out_path}")
    log(f"VERDICT: {verdict_label} [{evidentiary}] :: {detail}")
    if secondary:
        log(f"SECONDARY: {secondary['verdict']} [{secondary['evidentiary']}] "
            f":: {secondary['detail']}")
    return record


# --- CLI ---------------------------------------------------------------------
def cmd_run(args):
    here = os.path.dirname(os.path.abspath(__file__))
    if not args.ceo_gpu_clearance:
        print("REFUSED: --run requires --ceo-gpu-clearance "
              "(CEO GPU clearance for EXP084).")
        return 2
    if not args.stage2_review_signoff:
        print("REFUSED: --run requires --stage2-review-signoff (the separate "
              "stage-2 Law #14 review sign-off of the model loop).")
        return 2
    try:
        import torch  # noqa: F401
    except ImportError:
        print("REFUSED: torch is not installed; the model loop needs the "
              "GPU node.")
        return 2
    out_dir = args.out or here
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp084_run_log.txt")

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        with open(log_path, "a") as f:
            f.write(line + "\n")

    budget = PassBudget()
    records_path = (args.records or os.path.join(here, RECORDS_REL))
    baseline_path = os.path.join(out_dir, BASELINE_FILENAME)
    try:
        backend = TorchBackend(budget, log)
        run_full_loop(backend, budget, out_dir, log,
                       records_path, baseline_path)
    except BaselinePrepassHalt as e:
        # LOG-269 D2: first run archived the P0 baseline and halted
        # verdict-clean — no scientific arms ran, no verdict emitted.
        log(f"HALT (verdict-clean pre-pass): {type(e).__name__}: {e}")
        log("Re-run the same command for the full loop; the archived "
            "baseline will be replayed and INVALID(ii) enforced bit-for-bit.")
        return 3
    except (InvalidRunError, ApparatusError, S.NonTestableDataError) as e:
        log(f"HALT (verdict-clean): {type(e).__name__}: {e}")
        return 3
    except Exception as e:  # unexpected: loud, no verdict
        log(f"HALT (unexpected {type(e).__name__}): {e}")
        return 4
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="EXP084 Newton-duel model loop (signed protocol).")
    ap.add_argument("--smoke", action="store_true",
                    help="CPU-only: smoke suite incl. the mock-model "
                         "end-to-end harness (zero model passes).")
    ap.add_argument("--run", action="store_true",
                    help="GPU-node model loop (needs both sign-off flags).")
    ap.add_argument("--ceo-gpu-clearance", action="store_true",
                    help="CEO GPU clearance for the EXP084 run.")
    ap.add_argument("--stage2-review-signoff", action="store_true",
                    help="Separate stage-2 Law #14 review sign-off of the "
                         "model loop.")
    ap.add_argument("--out", default=None,
                    help="Run output directory (default: bundle dir).")
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
        "--stage2-review-signoff on the GPU node."
    )


if __name__ == "__main__":
    sys.exit(main())
