"""EXP102 executor — S6-3c L20 mean-gated attention injection at L11.

Licensed protocol: research/innovation/S6-3c_PREREG_DRAFT_v2_2026-09-28.md
(v2, F1-F2 repaired; binding chain: LOG-4449 (S6-3c v1 draft) ->
LOG-4450 (Law #14 ACCEPT-WITH-FIXES, F1 decision-proxy fence + F2 prose
off-by-one) -> LOG-4451 (v2 repair) -> LOG-4452 (independent delta
re-verification: SIGN) -> LOG-4453 (CEO clearance; S6-3c minted as EXP102).
This executor follows the licensed protocol EXACTLY; any deviation is a
STOP + new experiment number.

Design (licensed protocol §2 — the ONE design change vs EXP101):
  60 EXP092-B items x 3 arms (B, gated-T, gated-R); INJECTION LAYER = 11
  (unchanged); ratio 0.38. The ONLY change vs EXP101: the relevance READ
  moved to L20 (mean-over-heads at L20).
  B        : no injection; read-only L20 attention observation on this pass.
  gated-T  : frozen EXP094 per-item L11 task direction d_i^(11) @ 0.38, but
             ONLY on items where the L20-mean gate fires; unfired items
             copy B.
  gated-R  : fresh matched random direction g_i^(11) under the IDENTICAL
             live L20-mean gate, per-item norm-tied (||g_i|| == ||d_i||);
             unfired items copy B.
  Gate (per item i, derived from the B pass ONLY):
    mass_i^{L20,mean} = mean_h sum_{t in span_i} A^{(20,h)}_i[q_i -> t]
                 (mean over heads at L20 — readout-adjacent relevance).
    E_i    = number of entity-span token positions (union).
    N_i    = prompt token count.
    tau_i  = 2 * E_i / N_i — UNCHANGED, byte-identical adjudicated constant.
    fired_i = (mass_i^{L20,mean} >= tau_i).
    Assert E_i / N_i <= 0.5 for every item (violation -> HOLD, §3 step 0iii).
  Attention read: the model's attention backend is SDPA, which cannot emit
    attention weights (output_attentions unsupported). The B pass therefore
    runs the bit-identical code path to EXP094-101 (SDPA, read-only hooks
    only); a read-only pre-hook captures the L20 block INPUT on the B pass
    only, and the weights are recomputed offline in torch from the model's
    own submodules (input_layernorm, query_key_value, rotary_emb,
    apply_rotary_pos_emb) with an explicit causal softmax — the settled
    EXP100/101 preflight procedure, re-run in full in this lane for the L20
    math: within-backend eager bit-exactness proof (the eager model's own
    captured block-20 input through its own submodules vs its own emitted
    weights; max abs diff < 1e-5). Cross-backend comparison is invalid
    (SDPA-vs-eager block inputs already differ ~1e-5 from layers-0-19
    backend divergence — diagnosed 2026-09-28 on the EXP101 precedent).
    The 60/60 B agreement gate remains the empirical non-perturbation
    proof. The hooks also capture L11 post-block residuals on B (direction
    construction machinery) and the G5 execution probe verifies the L11
    injection placement — both frozen EXP094-101 procedures.
  F2-class fence (S6-3c §4.3, §5 item 2): NO non-gate attention columns are
    persisted — the gate's own mass_i^{L20,mean} ONLY appears in
    per_item_gate.csv. No other attention quantity is computed, persisted,
    or cited anywhere.
  {d_i^(11)}: frozen EXP094 procedure (identical C-1 on L11 residuals,
    Pass A vs P0), constructor code hash-pinned
    5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361;
    pre-run re-hash, mismatch -> HOLD. Degeneracy-signature check:
    |recomputed mean|cos| - 0.7923| <= 0.05, else HOLD (§3 step 0iv).
    The INJECTED direction is L11's — this check is unchanged.
  {g_i^(11)}: per-item isotropic Gaussian directions, normalized and
    norm-tied (||g_i|| == ||d_i|| — 60 assertions). Fresh pre-registered
    seed R_SEED_GATED = 412019 — distinct from every prior R stream
    (94094, 117011, 117013, 207101 [EXP100's], 311019 [EXP101's]).
    Item-major draw order (i = 0..59).

Binding execution order (licensed protocol §3, first match wins):
  0. Foundation gates FIRST: constructor re-hash vs pin; G0 bench; G1';
     thread pin; Δθ=0 pre; entity-span derivation + E_i/N_i <= 0.5
     assertions (0iii); attention-math validation (eager ground truth,
     L20 math); B-arm zero-variance -> HOLD; per-item B agreement 60/60 vs
     archived EXP094 baseline (36/60) -> HOLD; L11 degeneracy-signature
     |recomputed - 0.7923| <= 0.05 -> HOLD; G5 execution probe for layer 11
     (frozen verify_g5 core, EXP098 machinery).
  1. Delivery probe on the two injected arms (fired rows only):
     perturbation_ratio = ||δ|| / ||h_i^(11,B)|| in [0.285, 0.475].
     Unfired rows are UNDEFINED and never probed (no injection, no ratio).
     <=2 fired rows out of band per arm -> excluded from that arm's
     contrasts (count-bars apply to the post-exclusion paired set);
     >2 rows, or ANY zero-norm direction -> HOLD + diagnose.
  2. Gate integrity: (a) firing vector derived from the B pass only
     (asserted: captures counted, arm-tagged); E_i/N_i <= 0.5 all items.
     (b) Coverage tripwire (<10% -> verdict lane PIVOT-untestable; the
     executor records it only). (c) Vacuous-gate flag recorded (100% ->
     recorded caveat; the verdict lane walks it). Fired⟺L20-mean≥τ
     consistency on all 60 rows (F2-class fence: no other attention column
     anywhere).
  3. Regime routing (machine-written): (gated-T flips >= 1) OR
     (gated-R flips >= 1) -> LIVE; both 0 with coverage >= 10% -> FROZEN
     (verdict lane -> Underdetermined); asymmetric rule — a moving test
     arm routes LIVE. Coverage < 10% with both 0 is pre-empted by step 2b.
     Sanity gates route per-arm RUN-INVALID where they fire
     (zero-variance; ties_arm/60 > 5%).
  F1 decision-proxy audit (descriptive ONLY — no routing consequence):
     B-arm accuracy on fired items vs unfired items, reported in the
     worksheet (§5 item 8).
  Steps 2b, 2c, 4-7 = VERDICT LANE (separate). This executor is MECHANICAL
  ONLY: it executes, persists, and reports facts; it does not walk the
  decision table.

F5 (binding, Law #14 via S6-1 v2): ALL passes in ONE pinned environment —
no mid-run rebuilds; the env manifest attests it; a change voids the run
(Law #13).

Exit codes: 0 = ran (records verdict-ready); 2 = refused; 3 = RUN-INVALID;
4 = HOLD (guard fired; diagnosis facts logged, never re-run).
"""


import argparse
import csv
import hashlib
import json
import os
import re
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
EXP094_DIR = os.path.join(os.path.dirname(BUNDLE_DIR), "EXP094_peritem_l11")
sys.path.insert(0, BUNDLE_DIR)
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
EXP092_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl")
EXP093_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP093_l11_causal")
sys.path.append(EXP092_DIR)
sys.path.append(EXP093_DIR)
sys.path.append(EXP094_DIR)

import numpy as np

import constructor as C  # noqa: E402  (EXP094's frozen constructor module)


def _load_module(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pin = _load_module("exp102_protocol_pin",
                   os.path.join(EXP093_DIR, "protocol_pin.py"))
import reference_implementation as ref
import g1prime
from inject import verify_g5, RunInvalid as InjectRunInvalid
from test_g7_audit import sha256_file

score102 = _load_module("exp102_scorer",
                        os.path.join(BUNDLE_DIR, "score_exp102.py"))

FORBIDDEN_FLAGS = (
    "--train", "--training", "--finetune", "--fine-tune", "--lr",
    "--learning-rate", "--gpu", "--cuda", "--gpus",
    "--mutate-weights", "--update-weights",
)

N_ITEMS = 60
LAYER = 11  # injection layer (unchanged; §2.1)
GATE_LAYER = 20  # attention read layer (the S6-3c design change)
RATIO = 0.38                      # construction setpoint (§2.2)
G5_BAND = (0.285, 0.475)          # protocol literals, not float products
G5_MAX_EXCLUDED = 2               # <=2 fired rows OOB -> excluded; >2 -> HOLD
DEGENERACY_SIGNATURE_REF = 0.7923  # EXP094's archived L11 value
DEGENERACY_SIGNATURE_TOL = 0.05
TIE_DENOMINATOR = 60              # protocol §2.5 literal: ties/60 > 5%
TIE_RATE_BAR = 0.05
COVERAGE_FLOOR = 0.10
ATTN_VAL_TOL = 1e-5               # eager ground-truth validation tolerance
HARD_CAP_PASSES = 500
# 60 B + 60 construction-ref + 4 G5 execution probes + 3 eager-validation
# passes + <=120 sweep (fired items only). v2 §2.4's "180 maximum" counts
# the (item, arm) experiment passes (60 B + <=60 gated-T + <=60 gated-R)
# and 60 reserve; the construction ref passes, G5 probes, and
# attention-math validation passes are licensed executor machinery
# (EXP098 precedent: 368 under the same budget structure). The binding
# constraint is the 500 HARD CAP (not waivable).
EXPECTED_PASSES = 247

# Fresh pre-registered gated-R seed — distinct from every prior R
# stream (94094, 117011, 117013, 207101 [EXP100's], 311019 [EXP101's]).
R_SEED_GATED = 412019

CONSTRUCTOR_PIN = ("5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa"
                   "81917f361")
ARCHIVED_CSV = os.path.join(EXP094_DIR, "out", "per_item_records.csv")


class Hold(Exception):
    """Foundation guard fired -> HOLD (diagnose, never silent re-run)."""


class RunInvalid(Exception):
    """Guard failure -> RUN-INVALID (withheld, never a verdict)."""


def compute_state_dict_hash(state_dict):
    sha = hashlib.sha256()
    for key in sorted(state_dict.keys()):
        sha.update(np.asarray(state_dict[key], dtype=np.float32).tobytes())
    return sha.hexdigest()


def guard_g71_constructor():
    """G7.1: frozen constructor re-hash vs pin; audit PASS; P0 match."""
    ctor_path = os.path.join(EXP094_DIR, "constructor.py")
    live = sha256_file(ctor_path)
    if live != CONSTRUCTOR_PIN:
        raise Hold(
            f"STEP-0 HOLD: constructor.py hash {live[:16]}… != frozen pin "
            f"{CONSTRUCTOR_PIN[:16]}… — HOLD (diagnose, never proceed).")
    manifest = json.load(open(os.path.join(EXP094_DIR,
                                           "constructor_manifest.json")))
    if manifest.get("g7_verdict") != "PASS":
        raise Hold("STEP-0 HOLD: constructor audit verdict != PASS.")
    if manifest.get("P0_TEXT") != C.P0_TEXT:
        raise Hold("STEP-0 HOLD: P0_TEXT != frozen manifest.")
    return manifest


def guard_g0_bench():
    bench = ref.build_bench()
    try:
        g0 = ref.verify_g0(bench, pin.BENCH_PIN)
    except ref.BenchInvalid as e:
        raise RunInvalid(f"G0 FAIL: {e} — RUN-INVALID.")
    return bench, g0


def _word_pattern(name):
    return re.compile(r"\b" + re.escape(name) + r"\b")


def entity_span_token_idx(tokenizer, prompt, a_name, c_name):
    """EXP101 entity-span derivation (G1'-verified A/C occurrence tokens).

    Character spans: every \\b<A>\\b and \\b<C>\\b occurrence in the prompt
    (the same occurrence definition G1' verifies). Token positions: token
    indices whose token fully covers an occurrence char span. G1' has
    already verified each occurrence is single-token, so containment and
    overlap coincide; containment is used (exact).
    """
    spans = []
    for name in (a_name, c_name):
        for m in _word_pattern(name).finditer(prompt):
            spans.append(m.span())
    enc = tokenizer(prompt, add_special_tokens=False,
                    return_offsets_mapping=True)
    offs = [(int(s), int(e)) for s, e in enc["offset_mapping"]]
    # single-token coverage (G1' semantics): the token CONTAINS the
    # occurrence char span.
    span_idx = sorted({t for (s0, s1) in spans
                       for t, (c0, c1) in enumerate(offs)
                       if c0 <= s0 and c1 >= s1})
    if not span_idx:
        raise RunInvalid("entity span empty — RUN-INVALID.")
    for t in span_idx:  # single-token coverage check (mirrors G1')
        c0, c1 = offs[t]
        if not any(c0 <= s0 and c1 >= s1 for (s0, s1) in spans):
            raise RunInvalid(
                f"entity-span token {t} not covered by any occurrence — "
                "RUN-INVALID.")
    return span_idx


class LayerInjectionHook:
    """Forward hook adding alpha*v at the final position of a given layer's
    post-block residual. attach()/detach(); enable()/disable().

    Frozen TorchInjectionHook mechanics (identical _hook_fn, identical G5
    criteria) generalized to an explicit layer index — EXP098 machinery.
    Misplacement is caught by the frozen verify_g5 core, not by trust.
    """

    def __init__(self, layer_index, alpha=1.0):
        self.layer_index = int(layer_index)
        self.alpha = alpha
        self.v_t = None
        self.enabled = False
        self._handle = None
        self._module_path = None

    @staticmethod
    def resolve_module(model, layer_index):
        """Resolve the block module for an explicit layer index."""
        for path in ("gpt_neox.layers", "transformer.h"):
            obj = model
            try:
                for part in path.split("."):
                    obj = getattr(obj, part)
                layer = obj[int(layer_index)]
                return layer, f"{path}[{layer_index}]"
            except (AttributeError, IndexError, TypeError):
                continue
        raise RunInvalid(
            f"G5 FAIL: could not resolve the layer-{layer_index} block "
            "module — RUN-INVALID.")

    def _hook_fn(self, module, inputs, output):
        if not self.enabled or self.v_t is None:
            return output
        is_tuple = isinstance(output, tuple)
        out = output[0] if is_tuple else output
        delta = (self.alpha * self.v_t).to(dtype=out.dtype,
                                           device=out.device)
        out = out.clone()
        out[:, -1, :] = out[:, -1, :] + delta
        return (out,) + output[1:] if is_tuple else out

    def attach(self, model, v):
        import torch
        layer, path = self.resolve_module(model, self.layer_index)
        self.v_t = torch.as_tensor(np.asarray(v, dtype=np.float32))
        self._module_path = path
        self._handle = layer.register_forward_hook(self._hook_fn)
        return path

    def detach(self):
        if self._handle is not None:
            self._handle.remove()
            self._handle = None

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


class LayerCapture:
    """Capture a layer's post-block residual (full (T, D)) on forward."""

    def __init__(self, model, layer_index):
        import torch
        self._torch = torch
        layer, self.path = LayerInjectionHook.resolve_module(
            model, layer_index)
        self.captured = None

        def _cap(module, inputs, output):
            out = output[0] if isinstance(output, tuple) else output
            self.captured = out[0].detach().cpu().to(
                torch.float64).numpy()

        self._handle = layer.register_forward_hook(_cap)

    def remove(self):
        self._handle.remove()


class BlockInputCapture:
    """Read-only pre-hook capturing a layer block's INPUT on forward.

    Returns None (never modifies inputs). Attached ONLY during the B arm;
    the gate-source assertion counts captures and arm-tags them.
    """

    def __init__(self, model, layer_index):
        layer, self.path = LayerInjectionHook.resolve_module(
            model, layer_index)
        self.captured = []
        self.arm_tag = None

        def _pre(module, inputs):
            import torch
            self.captured.append((self.arm_tag, inputs[0][0].detach().cpu()
                                  .to(torch.float64).numpy()))
            return None  # read-only: inputs unmodified

        self._handle = layer.register_forward_pre_hook(_pre)

    def remove(self):
        self._handle.remove()


def verify_g5_layer_real(model, tokenizer, prompt_text, v, layer_index,
                         alpha=1.0):
    """G5 placement probe for an explicit layer, via the frozen verify_g5
    core (identical criteria i/ii/iii). EXP098 machinery."""
    import torch
    v = np.asarray(v, dtype=np.float64)
    hook = LayerInjectionHook(layer_index=layer_index, alpha=alpha)
    hook.attach(model, v)
    ids = torch.tensor([tokenizer.encode(prompt_text, add_special_tokens=False)],
                       dtype=torch.long)

    captured = {}

    def _capture(module, inputs, output):
        out = output[0] if isinstance(output, tuple) else output
        captured["resid"] = out[0].detach().cpu().to(torch.float64).numpy()

    layer, _ = LayerInjectionHook.resolve_module(model, layer_index)
    cap_handle = None
    try:
        with torch.no_grad():
            hook.detach()
            ref_logits = model(ids).logits[0].detach().cpu()
            # Re-attach injection FIRST, then register capture AFTER it
            # (LOG-4349: capture-after-injection observes post-injection).
            hook.attach(model, v)
            cap_handle = layer.register_forward_hook(_capture)
            _order = list(layer._forward_hooks)
            if _order.index(hook._handle.id) > _order.index(cap_handle.id):
                raise RunInvalid(
                    "G5 FAIL: probe internal error — capture hook registered "
                    "before the injection hook — RUN-INVALID.")
            hook.disable()
            logits_disabled = model(ids).logits[0].detach().cpu()
            if logits_disabled.shape != ref_logits.shape or not torch.equal(
                    logits_disabled, ref_logits):
                raise RunInvalid(
                    "G5 FAIL: criterion (iii) — condition-B bit-match failed "
                    "— RUN-INVALID.")
            hook.disable()
            model(ids)
            resid_clean = captured["resid"].copy()
            hook.enable()
            model(ids)
            resid_inj = captured["resid"].copy()
    finally:
        if cap_handle is not None:
            cap_handle.remove()
        hook.detach()

    return verify_g5(
        lambda: resid_clean,
        lambda: resid_inj,
        lambda: logits_disabled.numpy(),
        lambda: ref_logits.numpy(),
        v, alpha, label=f"real probe layer-{layer_index}")


def layer_attention_weights(model, layer_idx, x_block_input):
    """Recompute a layer's attention weights offline from a captured block
    input.

    Uses the model's OWN submodules (input_layernorm, query_key_value,
    rotary_emb, apply_rotary_pos_emb) with an explicit causal softmax —
    the exact eager attention math. x_block_input: torch tensor (1,T,1024).
    Returns numpy (H, T, T) float64.
    """
    import torch
    from transformers.models.gpt_neox.modeling_gpt_neox import (
        apply_rotary_pos_emb)
    layer = model.gpt_neox.layers[layer_idx]
    attn = layer.attention
    H = attn.config.num_attention_heads
    hs = attn.head_size
    with torch.no_grad():
        xn = layer.input_layernorm(x_block_input)
        T = xn.shape[1]
        qkv = attn.query_key_value(xn).view(1, T, H, 3 * hs).transpose(1, 2)
        q, k, _v = qkv.chunk(3, dim=-1)
        position_ids = torch.arange(T, dtype=torch.long).unsqueeze(0)
        cos, sin = model.gpt_neox.rotary_emb(xn, position_ids)
        q, k = apply_rotary_pos_emb(q, k, cos, sin)
        scores = torch.matmul(q, k.transpose(-2, -1)) * attn.scaling
        causal = torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)
        scores = scores.masked_fill(causal, float("-inf"))
        w = torch.softmax(scores, dim=-1, dtype=torch.float32)
    return w[0].detach().cpu().to(torch.float64).numpy()


def mean_pairwise_abs_cosine(unit_vecs):
    U = np.asarray(unit_vecs, dtype=np.float64)
    n = U.shape[0]
    if n < 2:
        return 0.0
    G = U @ U.T
    iu = np.triu_indices(n, k=1)
    return float(np.abs(G[iu]).mean())


def load_archived_B(csv_path):
    """Archived EXP094 per-item B decisions: item_id -> (stratum, correct)."""
    out = {}
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            if row["arm"] == "B":
                out[row["item_id"]] = (row["stratum"], int(row["correct_top1"]))
    if len(out) != N_ITEMS:
        raise Hold(
            f"STEP-0 HOLD: archived B vector has {len(out)} items, expected "
            f"{N_ITEMS} — HOLD.")
    return out


def top5_info(logits_final, tokenizer):
    """Top-5 token ids/strings/logits at the final position (S3-7 rider)."""
    lv = np.asarray(logits_final, dtype=np.float64)
    idx = np.argpartition(lv, -5)[-5:]
    idx = idx[np.argsort(lv[idx])[::-1]]
    ids = [int(i) for i in idx]
    return {
        "ids": ids,
        "strs": [tokenizer.decode([i]) for i in ids],
        "logits": [float(lv[i]) for i in ids],
    }


def top5_info_from_rider(rider, item_id, arm):
    for r in rider:
        if r["item_id"] == item_id and r["arm"] == arm:
            return {"ids": r["ids"], "strs": r["strs"],
                    "logits": r["logits"]}
    raise RunInvalid("rider lookup failed — RUN-INVALID.")


def run_real(bench, manifest, snapshot, log, out_dir):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    passes = [0]

    torch.set_num_threads(pin.THREAD_PIN)
    n_threads = torch.get_num_threads()
    if n_threads != pin.THREAD_PIN:
        raise RunInvalid(
            f"thread-pin FAIL: {n_threads} != {pin.THREAD_PIN} — RUN-INVALID.")
    log(f"[run] torch intra-op threads pinned: {n_threads}")

    if not os.path.isdir(snapshot):
        raise RunInvalid(f"snapshot directory not found: {snapshot}")
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)

    table = g1prime.verify_g1_prime(tokenizer, bench)
    n_occ = sum(x["occurrences"] for x in table.values())
    log(f"[run] G1' pass: {n_occ}/240 in-prompt occurrences single-token.")
    opt_ids = [(table[b["A"]]["token_id"], table[b["C"]]["token_id"])
               for b in bench]
    item_ids = [b["id"] for b in bench]
    phrasing = [b["phrasing"] for b in bench]
    assert len(set(item_ids)) == N_ITEMS

    # ---- STEP-0(iii): entity-span derivation + E_i/N_i <= 0.5 (pre-model) --
    span_idx_list, E_list, N_list, tau_list = [], [], [], []
    for b in bench:
        sidx = entity_span_token_idx(tokenizer, b["prompt"], b["A"], b["C"])
        toks = tokenizer.encode(b["prompt"], add_special_tokens=False)
        E, N = len(sidx), len(toks)
        if not (1 <= E < N):
            raise Hold(f"STEP-0 HOLD: item {b['id']}: E={E}, N={N} "
                       "violates 1<=E<N — HOLD + diagnose.")
        if E / N > 0.5:
            raise Hold(f"STEP-0 HOLD: item {b['id']}: E/N={E/N:.4f} > 0.5 "
                       "— HOLD + diagnose (§3 step 0iii).")
        if (N - 1) in sidx:
            raise Hold(f"STEP-0 HOLD: item {b['id']}: final prompt token "
                       "inside entity span — HOLD + diagnose.")
        span_idx_list.append(sidx)
        E_list.append(E)
        N_list.append(N)
        tau_list.append(2.0 * E / N)
    log(f"[run] STEP-0(iii): 60/60 items satisfy 1<=E<N, E/N<=0.5, final "
        f"token outside span. tau range "
        f"[{min(tau_list):.4f}, {max(tau_list):.4f}].")

    model = AutoModelForCausalLM.from_pretrained(
        snapshot, local_files_only=True, dtype=torch.float32)
    model.eval()
    model.requires_grad_(False)

    pre = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if pre != pin.WEIGHTS_PIN:
        raise RunInvalid(
            f"Δθ=0 FAIL (pre): {pre[:16]}… != LOG-331 pin — RUN-INVALID.")
    log(f"[run] Δθ=0 pre-run hash OK: {pre[:16]}…")

    p0_ids = tokenizer.encode(C.P0_TEXT, add_special_tokens=False)
    prompts = [tokenizer.encode(b["prompt"], add_special_tokens=False)
               for b in bench]

    # ---- attention-math validation: within-backend eager ground truth ----
    # SDPA cannot emit attention weights; the offline recomputation above
    # is validated once against a second model instance using the eager
    # backend (output_attentions=True), WITHIN-backend: the eager model's
    # own captured block-20 input is fed through the eager model's own
    # submodules and compared to its own emitted weights (the settled
    # EXP100/101 procedure, bit-exact in testing, 0.00e+00). Cross-backend
    # comparison is invalid (SDPA-vs-eager block-20 inputs already differ
    # ~1e-5 from layers-0-19 backend divergence — diagnosed 2026-09-28 on
    # the EXP101 precedent). 3 licensed machinery passes.
    model_eager = AutoModelForCausalLM.from_pretrained(
        snapshot, local_files_only=True, dtype=torch.float32,
        attn_implementation="eager")
    model_eager.eval()
    model_eager.requires_grad_(False)
    val_cap = BlockInputCapture(model_eager, GATE_LAYER)
    val_cap.arm_tag = "VALIDATION"
    attn_val_diffs = []
    eager_block_inputs = []
    with torch.no_grad():
        for i in range(3):
            ids_t = torch.tensor([prompts[i]], dtype=torch.long)
            out_e = model_eager(ids_t, output_attentions=True)
            passes[0] += 1
            if passes[0] > HARD_CAP_PASSES:
                raise RunInvalid("budget FAIL: hard cap — RUN-INVALID.")
            w_true = out_e.attentions[GATE_LAYER][0].detach().cpu().to(
                torch.float64).numpy()
            xb = val_cap.captured[-1][1]
            eager_block_inputs.append(xb.copy())
            x = torch.from_numpy(xb).to(torch.float32).unsqueeze(0)
            w_mine = layer_attention_weights(model_eager, GATE_LAYER, x)
            d = float(np.abs(w_true - w_mine).max())
            attn_val_diffs.append(d)
            if d > ATTN_VAL_TOL:
                raise Hold(
                    f"STEP-0 HOLD: attention-math validation failed on "
                    f"item {i}: max abs diff {d:.2e} > {ATTN_VAL_TOL:.0e} "
                    "vs within-backend eager ground truth — HOLD + diagnose.")
    val_cap.remove()
    log(f"[run] attention-math validation: 3/3 items within-backend, max "
        f"abs diff {max(attn_val_diffs):.2e} <= {ATTN_VAL_TOL:.0e} vs eager "
        "ground truth (L20 math) — PASS.")
    del model_eager

    cap11 = LayerCapture(model, LAYER)
    blk_in = BlockInputCapture(model, GATE_LAYER)
    blk_in.arm_tag = "B"

    def forward_ids(ids_list):
        ids = torch.tensor([ids_list], dtype=torch.long)
        with torch.no_grad():
            logits = model(ids).logits[0].detach().cpu().to(
                torch.float64).numpy()
        passes[0] += 1
        if passes[0] > HARD_CAP_PASSES:
            raise RunInvalid(
                f"budget FAIL: exceeded hard cap {HARD_CAP_PASSES} — "
                "RUN-INVALID.")
        return logits

    a11, h11_norms = [], []
    mB = np.zeros(N_ITEMS)
    rider = []  # S3-7 rider rows: per (item, arm) top-5
    baseline_top1 = []
    capture_tags = []  # arm tags of every block-input capture (gate source)
    try:
        # ---- B arm (60 items; doubles as constructor Pass A) ----
        for i in range(N_ITEMS):
            logits = forward_ids(prompts[i])
            r11 = cap11.captured[-1, :].copy()
            a11.append(r11)
            h11_norms.append(float(np.linalg.norm(r11)))
            a_id, c_id = opt_ids[i]
            mB[i] = float(logits[-1, a_id] - logits[-1, c_id])
            t5 = top5_info(logits[-1], tokenizer)
            rider.append({"item_id": item_ids[i], "arm": "B",
                          "source": "executed", **t5})
            baseline_top1.append({"item_id": item_ids[i],
                                  "top1_id": t5["ids"][0],
                                  "top1_str": t5["strs"][0]})
        # gate-source assertion: exactly 60 captures, all arm-tagged "B"
        # (the pre-hook was attached only for the B loop).
        block_inputs = [arr for tag, arr in blk_in.captured]
        capture_tags = [tag for tag, arr in blk_in.captured]
        if len(block_inputs) != N_ITEMS:
            raise Hold(
                f"STEP-2 HOLD: gate-source FAIL: {len(block_inputs)} "
                f"block-input captures, expected {N_ITEMS} — HOLD.")
        if any(t != "B" for t in capture_tags):
            raise Hold(
                "STEP-2 HOLD: gate-source FAIL: non-B capture in the gate "
                "source — HOLD + diagnose.")
        blk_in.remove()
        # backend-divergence diagnostic (attempt-1 HOLD diagnosis, logged
        # not gated): SDPA-vs-eager block-11 inputs already differ ~1e-5
        # from layers-0-10 backend divergence.
        be_div = max(float(np.abs(block_inputs[i] - eager_block_inputs[i])
                           .max()) for i in range(3))
        log(f"[run] diagnostic: SDPA-vs-eager block-20 input max abs "
            f"diff over 3 items = {be_div:.2e} (backend divergence, not "
            "gated).")
        log(f"[run] B arm complete: 60 passes; B accuracy "
            f"{int((mB > 0).sum())}/60.")

        if bool((mB == mB[0]).all()):
            raise Hold(
                "STEP-0 HOLD: B-arm decisions zero-variance — the bench "
                "itself broke — HOLD + diagnose.")

        # ---- Reference passes (constructor Pass B: P0 + prompt) ----
        b11 = []
        for i in range(N_ITEMS):
            forward_ids(p0_ids + prompts[i])
            b11.append(cap11.captured[-1, :].copy())
        log("[run] reference passes complete: 60 passes.")

        # ---- Construction: {d_i^(11)} (frozen EXP094 procedure) ----
        d11 = []
        for i in range(N_ITEMS):
            d, info = C.build_per_item_direction(
                a11[i], b11[i], h11_norms[i], ratio=RATIO)
            if info["degenerate_zero"]:
                raise Hold(
                    f"STEP-1 HOLD: zero-norm d_i^(11) on item {i} — "
                    "HOLD + diagnose.")
            d11.append(d)
        log(f"[run] construction complete: 60 d_i^(11) (frozen C-1) at "
            f"ratio {RATIO}.")

        # ---- gated-R draws: fresh seed, item-major, per-item norm-tied ----
        rng = np.random.default_rng(R_SEED_GATED)
        dim = a11[0].shape[0]
        g11 = []
        for i in range(N_ITEMS):
            z = np.asarray(rng.normal(size=dim), dtype=np.float64)
            z_norm = float(np.linalg.norm(z))
            if z_norm == 0.0:
                raise Hold("STEP-1 HOLD: isotropic draw exactly zero "
                           f"(item {i}).")
            g11.append((z / z_norm) * float(np.linalg.norm(d11[i])))
        log(f"[run] gated-R draws complete: 60 g_i^(11) (seed "
            f"{R_SEED_GATED}), item-major.")

        # ---- Norm-tie assertions: 60 (EXP096 bug class) ----
        tie_ok = {}
        for i in range(N_ITEMS):
            nt = float(np.linalg.norm(d11[i]))
            nw = float(np.linalg.norm(g11[i]))
            ok = abs(nt - nw) <= 1e-9 * max(nt, 1e-300)
            tie_ok[i] = bool(ok)
            if not ok:
                raise Hold(
                    f"STEP-1 HOLD: norm-tie broken on item {i}: "
                    f"||T||={nt:.6f} vs ||R||={nw:.6f} — HOLD + diagnose.")
        log("[run] norm-tie check: 60/60 pass (||g_i^(11)|| == ||d_i^(11)||).")

        # ---- STEP-0(iv): L11 degeneracy signature vs 0.7923 (±0.05) ----
        u11 = np.stack([d / float(np.linalg.norm(d)) for d in d11])
        mean_abs_cos_11 = mean_pairwise_abs_cosine(u11)
        if abs(mean_abs_cos_11 - DEGENERACY_SIGNATURE_REF) > \
                DEGENERACY_SIGNATURE_TOL:
            raise Hold(
                f"STEP-0 HOLD: L11 mean|cos|={mean_abs_cos_11:.4f} vs "
                f"archived {DEGENERACY_SIGNATURE_REF} "
                f"(tol {DEGENERACY_SIGNATURE_TOL}) — HOLD + diagnose.")
        log(f"[run] L11 degeneracy signature: mean|cos|={mean_abs_cos_11:.4f} "
            f"(vs {DEGENERACY_SIGNATURE_REF} OK).")

        # ---- STEP-0(ii): per-item B agreement (60/60 required) ----
        archived_B = load_archived_B(ARCHIVED_CSV)
        disagreements = []
        for i, iid in enumerate(item_ids):
            arch_stratum, arch_correct = archived_B[iid]
            live_correct = int(mB[i] > 0.0)
            if arch_correct != live_correct or arch_stratum != phrasing[i]:
                disagreements.append(iid)
        if disagreements:
            raise Hold(
                f"STEP-0 HOLD: per-item B-decision disagreement on "
                f"{len(disagreements)} items vs archived EXP094 baseline — "
                "HOLD + diagnose.")
        log("[run] STEP-0 B agreement: 60/60 per-item decisions match the "
            "archived EXP094 baseline.")

        # ---- STEP-0 (cont.): G5 execution probe, layer 11 ----
        res = verify_g5_layer_real(model, tokenizer, bench[0]["prompt"],
                                   d11[0], LAYER)
        passes[0] += 4  # ref + disabled + clean + injected
        if passes[0] > HARD_CAP_PASSES:
            raise RunInvalid("budget FAIL: hard cap exceeded — RUN-INVALID.")
        log(f"[run] G5 layer-{LAYER} execution probe: PASS "
            f"(rel_err={res['criterion_i_rel_err']:.2e}, "
            f"other={res['criterion_ii_max_abs_change']:.2e}).")

        # ---- STEP-2a: L20-MEAN-gate computation from B-pass captures ----
        # mass_i^{L20,mean} = mean over heads of the final-query-row span
        # mass at L20 (the S6-3c design change: readout-adjacent relevance
        # read; injection stays at L11). F2-class fence: NO non-gate
        # attention columns are persisted — the gate's own mass only.
        masses_L20mean = np.zeros(N_ITEMS)
        fired = np.zeros(N_ITEMS, dtype=bool)
        for i in range(N_ITEMS):
            x = torch.from_numpy(block_inputs[i]).to(
                torch.float32).unsqueeze(0)
            W = layer_attention_weights(model, GATE_LAYER, x)  # (H,T,T) f64
            q = N_list[i] - 1
            rowsum = float(np.abs(W[:, q, :].sum(axis=1) - 1.0).max())
            if rowsum > 1e-4:
                raise Hold(
                    f"STEP-2 HOLD: attention rows do not sum to 1 on item "
                    f"{i} (max dev {rowsum:.2e}) — HOLD + diagnose.")
            head_spans = W[:, q, :][:, span_idx_list[i]].sum(axis=1)
            masses_L20mean[i] = float(head_spans.mean())
            if not (0.0 <= masses_L20mean[i] <= 1.0):
                raise Hold(
                    f"STEP-2 HOLD: mass_i^{{L20,mean}}={masses_L20mean[i]:.4f} "
                    f"outside [0,1] on item {i} — HOLD + diagnose.")
            fired[i] = bool(masses_L20mean[i] >= tau_list[i])
        n_fired = int(fired.sum())
        coverage = n_fired / N_ITEMS
        # §5 item 2 audit: fired⟺mass^{L20,mean}≥τ on all 60 rows.
        audit_a = all(bool(fired[i]) == (masses_L20mean[i] >= tau_list[i])
                      for i in range(N_ITEMS))
        if not audit_a:
            raise Hold("STEP-2 HOLD: fired⟺L20-mean≥τ consistency violated "
                       "— HOLD + diagnose.")
        log(f"[run] gate (L20 mean-over-heads): fired {n_fired}/60 "
            f"(coverage {coverage:.3f}); mass_i^{{L20,mean}} range "
            f"[{masses_L20mean.min():.4f}, {masses_L20mean.max():.4f}]; "
            f"tau range [{min(tau_list):.4f}, {max(tau_list):.4f}]; "
            f"fired⟺L20-mean≥τ 60/60.")

        # ---- STEP-1 delivery probe on fired rows of the injected arms ----
        lo, hi = G5_BAND
        ratios_T = [float(np.linalg.norm(d11[i]) / h11_norms[i])
                    for i in range(N_ITEMS)]
        ratios_R = [float(np.linalg.norm(g11[i]) / h11_norms[i])
                    for i in range(N_ITEMS)]
        excluded = {"gated-T": sorted(
            i for i in range(N_ITEMS)
            if fired[i] and not (lo <= ratios_T[i] <= hi)),
            "gated-R": sorted(
            i for i in range(N_ITEMS)
            if fired[i] and not (lo <= ratios_R[i] <= hi))}
        for arm, oob in excluded.items():
            if len(oob) > G5_MAX_EXCLUDED:
                raise Hold(
                    f"STEP-1 HOLD: {len(oob)} fired rows out of band on "
                    f"{arm} (>{G5_MAX_EXCLUDED}) — HOLD + diagnose.")
        n_oob = sum(len(v) for v in excluded.values())
        log(f"[run] STEP-1 delivery: {2 * n_fired} fired cell-rows; "
            f"{2 * n_fired - n_oob} in band [{lo}, {hi}]; exclusions: "
            f"gated-T={excluded['gated-T']}, gated-R={excluded['gated-R']}.")
        mask_T = np.array([i not in excluded["gated-T"]
                           for i in range(N_ITEMS)])
        mask_R = np.array([i not in excluded["gated-R"]
                           for i in range(N_ITEMS)])

        # ---- The sweep (gated injection on fired items; copy otherwise) ----
        hook11 = LayerInjectionHook(layer_index=LAYER, alpha=1.0)

        def single_pass(ids, vec, item_id, arm_name):
            hook11.attach(model, vec)
            hook11.enable()
            try:
                ids_t = torch.tensor([ids], dtype=torch.long)
                with torch.no_grad():
                    lg = model(ids_t).logits[0].detach().cpu().to(
                        torch.float64).numpy()
            finally:
                hook11.detach()
            passes[0] += 1
            if passes[0] > HARD_CAP_PASSES:
                raise RunInvalid("budget FAIL: hard cap exceeded — "
                                 "RUN-INVALID.")
            rider.append({"item_id": item_id, "arm": arm_name,
                          "source": "executed", **top5_info(lg[-1],
                                                            tokenizer)})
            return lg

        mT = mB.copy()  # unfired items deterministically copy B
        mR = mB.copy()
        for i in range(N_ITEMS):
            if not fired[i]:
                t5b = top5_info_from_rider(rider, item_ids[i], "B")
                rider.append({"item_id": item_ids[i], "arm": "gated-T",
                              "source": "deterministic_copy", **t5b})
                rider.append({"item_id": item_ids[i], "arm": "gated-R",
                              "source": "deterministic_copy", **t5b})
                continue
            lg = single_pass(prompts[i], d11[i], item_ids[i], "gated-T")
            a_id, c_id = opt_ids[i]
            mT[i] = float(lg[-1, a_id] - lg[-1, c_id])
            lg = single_pass(prompts[i], g11[i], item_ids[i], "gated-R")
            mR[i] = float(lg[-1, a_id] - lg[-1, c_id])
        log(f"[run] sweep complete: {2 * n_fired} injection passes "
            f"({n_fired} fired items x 2 arms); {N_ITEMS - n_fired} unfired "
            f"items copied B. Total passes: {passes[0]} "
            f"(expected ≤ {EXPECTED_PASSES}, cap {HARD_CAP_PASSES}).")
    finally:
        cap11.remove()

    # Δθ=0 (post)
    post = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if post != pin.WEIGHTS_PIN:
        raise RunInvalid("Δθ=0 FAIL (post): state_dict changed — RUN-INVALID.")
    log("[run] Δθ=0 post-run hash OK (Δθ=0 verified).")

    # ---- Mechanical scoring (no verdict) ----
    arm_names = {"B": "B", "gated-T": "gated-T", "gated-R": "gated-R"}
    with open(os.path.join(out_dir, "per_item_records.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "stratum", "arm", "correct_top1", "margin",
                    "margin_shift_vs_B", "executed"])
        all_m = {"B": (mB, np.ones(N_ITEMS, dtype=bool)),
                 "gated-T": (mT, fired), "gated-R": (mR, fired)}
        for key in ("B", "gated-T", "gated-R"):
            mm, execv = all_m[key]
            for i, iid in enumerate(item_ids):
                w.writerow([iid, phrasing[i], arm_names[key],
                            int(mm[i] > 0.0), f"{mm[i]:.10f}",
                            f"{(mm[i] - mB[i]):.10f}" if key != "B"
                            else "0.0000000000",
                            "y" if (key == "B" or execv[i]) else "n"])

    # §5 item 2: the gate's own mass ONLY — NO non-gate attention columns
    # (F2-class fence). Round-trip verification of the written CSV happens
    # immediately after.
    with open(os.path.join(out_dir, "per_item_gate.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "E", "N", "mass_L20_mean", "tau",
                    "fired", "firing_rule", "gate_source"])
        for i, iid in enumerate(item_ids):
            w.writerow([iid, E_list[i], N_list[i],
                        f"{masses_L20mean[i]:.10f}",
                        f"{tau_list[i]:.10f}", "1" if fired[i] else "0",
                        "L20-mean>=tau", "B_pass"])

    # Gate-integrity round-trip audit on the PERSISTED csv (not the live
    # arrays): fired⟺mass_L20_mean≥τ on all 60 rows (F2-class fence: the
    # gate's own mass is the only attention column). Fails -> HOLD.
    gate_roundtrip = []
    with open(os.path.join(out_dir, "per_item_gate.csv"), newline="") as f:
        for r in csv.DictReader(f):
            mm, ta = float(r["mass_L20_mean"]), float(r["tau"])
            fr = r["fired"] == "1"
            gate_roundtrip.append(fr == (mm >= ta))
    n_audit_consistent = sum(1 for ok in gate_roundtrip if ok)
    if n_audit_consistent != N_ITEMS:
        raise Hold("STEP-2 HOLD: gate CSV round-trip audit failed "
                   f"(consistent={n_audit_consistent}/60) — HOLD + diagnose.")
    log(f"[run] gate CSV round-trip audit: fired⟺L20-mean≥τ "
        f"{n_audit_consistent}/60 — PASS.")

    with open(os.path.join(out_dir, "per_item_delivery.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "arm", "fired", "perturbation_ratio",
                    "norm_target", "h_norm_B", "in_band",
                    "excluded_from_contrasts", "norm_tie_ok"])
        for key, ratios in (("gated-T", ratios_T), ("gated-R", ratios_R)):
            for i, iid in enumerate(item_ids):
                nt = float(np.linalg.norm(
                    d11[i] if key == "gated-T" else g11[i]))
                if not fired[i]:
                    w.writerow([iid, key, "n", "undefined",
                                f"{nt:.10f}", f"{h11_norms[i]:.10f}",
                                "na", "n", "y" if tie_ok[i] else "n"])
                else:
                    r = ratios[i]
                    w.writerow([iid, key, "y", f"{r:.10f}",
                                f"{nt:.10f}", f"{h11_norms[i]:.10f}",
                                "y" if lo <= r <= hi else "n",
                                "y" if i in excluded[key] else "n",
                                "y" if tie_ok[i] else "n"])

    cells, readout = score102.compute(
        score102.load_csv(os.path.join(out_dir, "per_item_records.csv")),
        score102.load_csv(os.path.join(out_dir, "per_item_delivery.csv")),
        score102.load_csv(os.path.join(out_dir, "per_item_gate.csv")))
    log(f"[run] scoring complete: {len(cells)} stratum cells "
        f"(3 strata x 3 contrasts).")

    # ---- Regime routing (machine-written, §3 step 3) ----
    t_flips = readout["gated_T_flips_vs_B"]
    r_flips = readout["gated_R_flips_vs_B"]
    if t_flips >= 1 or r_flips >= 1:
        route, why = ("LIVE", f"(gated-T={t_flips} >= 1) OR "
                              f"(gated-R={r_flips} >= 1)")
    elif coverage >= COVERAGE_FLOOR:
        route, why = ("FROZEN", "gated-T = 0 and gated-R = 0 with coverage "
                                f"{coverage:.3f} >= {COVERAGE_FLOOR} "
                                "(verdict lane -> Underdetermined)")
    else:
        route, why = ("PREEMPTED_BY_STEP_2B",
                      f"gated-T = 0 and gated-R = 0 with coverage "
                      f"{coverage:.3f} < {COVERAGE_FLOOR} (step-2b "
                      "tripwire; verdict lane rules PIVOT)")
    routing = {
        "routing": route,
        "routing_reason": why,
        "coverage": coverage,
        "n_fired": n_fired,
        "evidence": {
            "gated_T_flips_vs_B": t_flips,
            "gated_R_flips_vs_B": r_flips,
            "delivery_confirmed": True,
            "sanity": readout["sanity"],
        },
        "note": "machine-written before the table walk; per-arm RUN-INVALID "
                "routed where sanity gates fire; steps 2b, 4-8 are the "
                "verdict lane's",
    }
    log(f"[run] regime routing: {route} ({why}).")

    # ---- Margin-shift ledger (descriptive only; no classifier licensed) --
    dmT, dmR = mT - mB, mR - mB
    ledger = [{"item": i, "item_id": item_ids[i], "stratum": phrasing[i],
               "fired": bool(fired[i]),
               "dM_gated_T": float(dmT[i]), "dM_gated_R": float(dmR[i])}
              for i in range(N_ITEMS)]
    desc = {}
    for k, v in (("gated-T", dmT), ("gated-R", dmR)):
        desc[k] = {"mean": float(v.mean()), "std": float(v.std()),
                   "min": float(v.min()), "max": float(v.max()),
                   "n_nonzero": int((v != 0.0).sum())}
    log("[run] margin-shift ledger: 60 rows; descriptive aggregates "
        "computed.")

    # ---- Gate-integrity log (§3 steps 0iii/2a; Law #14 adversarial input) --
    gate_integrity = {
        "gate_source": "B_pass_only",
        "gate_rule": "L20-mean>=tau (mass_i^{L20,mean} = mean_h span-sum at "
                     "L20; read-only block-input pre-hook on the B pass)",
        "n_block_input_captures": len(block_inputs),
        "capture_arm_tags": sorted(set(capture_tags)),
        "pre_hook_readonly": True,
        "coverage": coverage,
        "n_fired": n_fired,
        "mass_L20_mean_range": [float(masses_L20mean.min()),
                                float(masses_L20mean.max())],
        "tau_range": [float(min(tau_list)), float(max(tau_list))],
        "audit_fired_iff_L20mean_ge_tau": f"{n_audit_consistent}/{N_ITEMS}",
        "audit_note": "F2-class fence: NO non-gate attention columns are "
                      "persisted — the gate's own mass_i^{L20,mean} only "
                      "(§5 item 2; §4.3). No verdict, worksheet cell, or "
                      "report may cite any non-gate attention quantity.",
        "step_0iii": {"E_over_N_le_0.5": "60/60",
                      "one_le_E_lt_N": "60/60",
                      "final_token_outside_span": "60/60",
                      "tau_in_(0,1]": "60/60"},
        "step_2a": "firing vector derived from B-pass captures only; "
                   "injection-pass data never entered the gate computation",
        "attention_backend": "sdpa (default; B pass bit-identical code path "
                             "to EXP094-099)",
        "attention_math_validation": {
            "method": "WITHIN-backend eager ground truth: the eager model's "
                      "own captured block-20 input through its own "
                      "submodules vs its own output_attentions[20] weights "
                      "(separate model instance, output_attentions=True)",
            "n_items": 3,
            "max_abs_diff": max(attn_val_diffs),
            "tol": ATTN_VAL_TOL,
            "pass": True,
        },
        "backend_divergence_diagnostic": {
            "note": "EXP101 HOLD diagnosis (2026-09-28): cross-backend "
                    "comparison is invalid — SDPA-vs-eager block-20 inputs "
                    "already differ ~1e-5 from layers-0-19 backend "
                    "divergence; logged, not gated",
            "sdpa_vs_eager_block20_input_max_abs_diff_3_items": be_div,
        },
    }

    # ---- Persist (§5 instrumentation spec, append-only) ----
    ctor_manifest = {
        "constructor_sha256": CONSTRUCTOR_PIN,
        "constructor_sha256_live": sha256_file(
            os.path.join(EXP094_DIR, "constructor.py")),
        "P0_sha256": manifest["P0_sha256"],
        "NORM_RATIO": C.NORM_RATIO,
        "RATIO": RATIO,
        "G5_BAND": list(G5_BAND),
        "R_SEED_GATED": R_SEED_GATED,
        "R_seed_note": "fresh pre-registered seed, distinct from every "
                       "prior R stream (94094, 117011, 117013, 207101 "
                       "[EXP100's], 311019 [EXP101's]); item-major draw "
                       "order (i = 0..59)",
        "g7_carryover": "EXP094 constructor_manifest.json (audit PASS)",
        "direction_note": "frozen C-1 procedure (identical code, "
                          "hash-pinned) on L11 residuals (Pass A vs P0); "
                          "anchored to BASELINE L11 norms",
        "R_draw_order": "for i in 0..59, draw z_i ~ N(0, I) from "
                        "np.random.default_rng(412019); each normalized "
                        "and norm-tied to the task arm's component",
        "norm_tie_assertions": "60/60 pass (||g_i^(11)|| == ||d_i^(11)||)",
        "L11_degeneracy_signature": {
            "archived_ref": DEGENERACY_SIGNATURE_REF,
            "recomputed": mean_abs_cos_11,
            "tol": DEGENERACY_SIGNATURE_TOL,
            "pass": True,
        },
        "per_item": [
            {"item": i, "item_id": item_ids[i],
             "d11_norm": float(np.linalg.norm(d11[i])),
             "g11_norm": float(np.linalg.norm(g11[i])),
             "h11_norm_B": h11_norms[i],
             "norm_tie_ok": tie_ok[i]}
            for i in range(N_ITEMS)],
    }
    with open(os.path.join(out_dir, "constructor_manifest.json"), "w") as f:
        json.dump(ctor_manifest, f, indent=2)

    env_manifest = {
        "torch": __import__("torch").__version__,
        "transformers": __import__("transformers").__version__,
        "numpy": np.__version__,
        "python": sys.version.split()[0],
        "thread_pin": n_threads,
        "snapshot": snapshot,
        "weights_pin": pin.WEIGHTS_PIN,
        "weights_pre": pre,
        "weights_post": post,
        "bench_pin": pin.BENCH_PIN,
        "seeds": {"R_SEED_GATED": R_SEED_GATED, "G5_probe_seed": 31337},
        "single_environment_F5": "all passes in this environment; "
                                 "no mid-run rebuild",
        "n_passes": passes[0],
        "expected_passes": EXPECTED_PASSES,
        "hard_cap": HARD_CAP_PASSES,
        "budget_note": "180 maximum per v2 §2.4 counts the 60 B + <=60 "
                       "gated-T + <=60 gated-R experiment passes, plus 60 "
                       "reserve; the 60 construction-ref passes, 4 G5 "
                       "execution probes, and 3 eager attention-validation "
                       "passes are licensed executor machinery (EXP098 "
                       "precedent: 368 under the same budget structure); "
                       "the binding constraint is the 500 HARD CAP (not "
                       "waivable)",
    }
    with open(os.path.join(out_dir, "env_manifest.json"), "w") as f:
        json.dump(env_manifest, f, indent=2)

    with open(os.path.join(out_dir, "gate_integrity.json"), "w") as f:
        json.dump(gate_integrity, f, indent=2)

    with open(os.path.join(out_dir, "delivery_probe_log.json"), "w") as f:
        json.dump({
            "band": list(G5_BAND),
            "n_fired_cell_rows": 2 * n_fired,
            "in_band": 2 * n_fired - n_oob,
            "out_of_band": n_oob,
            "exclusions": excluded,
            "per_arm_PASS_FAIL": {
                arm: ("PASS" if len(oob) <= G5_MAX_EXCLUDED else "FAIL")
                for arm, oob in excluded.items()},
            "realized_vs_perturbed_note": "both arms are single-injection "
                "(no co-injection cascade); the hook adds δ directly to the "
                "post-block residual at the final position, so the realized "
                "injection ratio == the analytic perturbation_ratio by "
                "construction; placement validated by the G5 execution probe "
                "(frozen verify_g5 core, criterion i) at layer 11",
        }, f, indent=2)

    with open(os.path.join(out_dir, "regime_routing.json"), "w") as f:
        json.dump(routing, f, indent=2)

    with open(os.path.join(out_dir, "stratum_table.json"), "w") as f:
        json.dump(cells, f, indent=2)

    with open(os.path.join(out_dir, "margin_shift_ledger.json"), "w") as f:
        json.dump({"rows": ledger, "descriptive": desc,
                   "note": "descriptive only; alters no verdict"}, f, indent=2)

    # S3-7 instrumentation rider (no analysis pre-registered).
    with open(os.path.join(out_dir, "s3_7_rider.json"), "w") as f:
        json.dump({
            "rows": [{"item_id": r["item_id"], "arm": r["arm"],
                      "source": r["source"],
                      "top5": [{"id": r["ids"][k], "str": r["strs"][k],
                                "logit": r["logits"][k]} for k in range(5)]}
                     for r in rider],
            "baseline_top1": baseline_top1,
            "note": "rider only (LOG-4408 watchlist); deterministic_copy "
                    "rows reuse the B pass top-5; no analysis pre-registered",
        }, f, indent=2)

    # Decision-table worksheet: the §3 step walk is BLANK for the verdict
    # lane (this executor does not walk it); evidence cells are recorded.
    contrasts = ("gated-T_vs_B", "gated-R_vs_B", "gated-T_vs_gated-R")
    cell_of = {(c["contrast"], c["stratum"]): c for c in cells}
    agg_evidence = {
        c: {"n": cell_of[(c, "agg")]["n"],
            "delta": cell_of[(c, "agg")]["delta"],
            "b": cell_of[(c, "agg")]["mcnemar_b"],
            "c": cell_of[(c, "agg")]["mcnemar_c"],
            "p": cell_of[(c, "agg")]["mcnemar_p"]}
        for c in contrasts}
    # Decision-table worksheet: the §3 step walk is BLANK for the verdict
    # lane (this executor does not walk it); evidence cells are recorded.
    # Steps follow S6-3c v2 §3 exactly (0, 1, 2a, 2b, 2c, 3, 4, 5, 6, 7).
    # Plus the F1 decision-proxy audit (descriptive only; no routing).
    coverage_conditioned_floor_8F = (8 / n_fired if n_fired else None)
    # F1 decision-proxy audit (descriptive ONLY — no routing, bar, or
    # verdict consequence; §4.3): B-arm accuracy on fired vs unfired items.
    b_acc_fired = int((mB[fired] > 0).sum())
    b_acc_unfired = int((mB[~fired] > 0).sum())
    worksheet = [
        {"step": 0, "condition": "foundation gates",
         "evidence": {
             "constructor_rehash": "match frozen pin",
             "G5_layer_11": "PASS (frozen verify_g5 core, d_0^(11) probe)",
             "B_agreement": "60/60 per-item vs archived EXP094 baseline",
             "B_accuracy": int((mB > 0).sum()),
             "L11_degeneracy_signature":
                 f"{mean_abs_cos_11:.4f} vs {DEGENERACY_SIGNATURE_REF} "
                 f"(tol {DEGENERACY_SIGNATURE_TOL}) — PASS",
             "attention_math_validation":
                 f"max abs diff {max(attn_val_diffs):.2e} <= "
                 f"{ATTN_VAL_TOL:.0e} — PASS (L20 math)",
             "E_over_N": "60/60 <= 0.5"},
         "walk": "BLANK — verdict lane"},
        {"step": 1, "condition": "delivery (fired rows in band)",
         "evidence": {"n_fired_cell_rows": 2 * n_fired,
                      "in_band": 2 * n_fired - n_oob,
                      "out_of_band": n_oob, "exclusions": excluded,
                      "zero_norm_directions": 0},
         "walk": "BLANK — verdict lane"},
        {"step": "2a", "condition": "gate integrity",
         "evidence": gate_integrity, "walk": "BLANK — verdict lane"},
        {"step": "2b", "condition": "coverage tripwire",
         "evidence": {"coverage": coverage, "n_fired": n_fired,
                      "floor": COVERAGE_FLOOR,
                      "tripwire_fired": bool(coverage < COVERAGE_FLOOR),
                      "vacuous_gate": bool(n_fired == N_ITEMS)},
         "walk": "BLANK — verdict lane"},
        {"step": "2c", "condition": "vacuous-gate flag",
         "evidence": {"vacuous_gate": bool(n_fired == N_ITEMS),
                      "required_verbatim_caveat": "CONTINUE (directional "
                      "signal at ratio 0.38; gating unattributed — the "
                      "gate was vacuous)."},
         "walk": "BLANK — verdict lane"},
        {"step": 3, "condition": "regime routing (machine-written)",
         "evidence": routing, "walk": "BLANK — verdict lane"},
        {"step": "F1", "condition": "decision-proxy audit (descriptive ONLY; "
         "no routing, bar, or verdict consequence — §4.3)",
         "evidence": {"B_accuracy_fired": b_acc_fired,
                      "B_accuracy_unfired": b_acc_unfired,
                      "n_fired": n_fired, "n_unfired": N_ITEMS - n_fired,
                      "note": "descriptive only — the verdict lane may "
                              "state whether the gate behaved as a "
                              "near-decision proxy; it alters no step"},
         "walk": "BLANK — verdict lane (informational)"},
        {"step": 4, "condition": "fragility PIVOT (matched random, §3 step 4)",
         "evidence": {"aggregate_contrasts": agg_evidence,
                      "gated_R_flips_vs_B": r_flips,
                      "note": "fragility routes before directionality; "
                              "verdict lane applies the first-match rule"},
         "walk": "BLANK — verdict lane"},
        {"step": 5, "condition": "licensed positive (gated-T, §3 step 5)",
         "evidence": {"aggregate_contrasts": agg_evidence,
                      "stratum_cells": "stratum_table.json",
                      "sensitivity_floor_8_over_N_realized":
                          8 / int(mask_T.sum()) if int(mask_T.sum()) else None,
                      "sensitivity_floor_8_over_F":
                          coverage_conditioned_floor_8F,
                      "note": "full conjunction evaluated by the verdict "
                              "lane"},
         "walk": "BLANK — verdict lane"},
        {"step": 6, "condition": "gated KILL (§3 step 6)",
         "evidence": {"routing": routing["routing"],
                      "coverage": coverage, "n_fired": n_fired,
                      "aggregate_contrasts": agg_evidence,
                      "note": "verdict lane evaluates the step-6 conjunction "
                              "(LIVE, coverage≥10%, gated-T<6, gated-R "
                              "sub-threshold)"},
         "walk": "BLANK — verdict lane"},
        {"step": 7, "condition": "otherwise -> PIVOT (named sub-cases)",
         "evidence": {"aggregate_contrasts": agg_evidence},
         "walk": "BLANK — verdict lane"},
    ]
    with open(os.path.join(out_dir, "decision_table_worksheet.json"),
              "w") as f:
        json.dump(worksheet, f, indent=2)

    # Mechanical read-out (UNINTERPRETED — verdict lane walks §3 steps 2b-7).
    readout_doc = {"status": "UNINTERPRETED_MECHANICAL_READOUT",
                   "experiment": "EXP102"}
    readout_doc["routing"] = routing["routing"]
    readout_doc["routing_reason"] = routing["routing_reason"]
    readout_doc["coverage"] = coverage
    readout_doc["n_fired"] = n_fired
    readout_doc["mass_L20_mean_range"] = [float(masses_L20mean.min()),
                                         float(masses_L20mean.max())]
    readout_doc["tau_range"] = [float(min(tau_list)),
                                float(max(tau_list))]
    readout_doc["gate_integrity_audit"] = {
        "fired_iff_L20mean_ge_tau": f"{n_audit_consistent}/{N_ITEMS}",
    }
    readout_doc["decision_proxy_audit"] = {
        "B_accuracy_fired": b_acc_fired,
        "B_accuracy_unfired": b_acc_unfired,
        "n_fired": n_fired,
        "n_unfired": N_ITEMS - n_fired,
        "note": "descriptive only (F1); no routing consequence",
    }
    readout_doc["n_correct"] = {
        "B": int((mB > 0).sum()),
        "gated-T": int((mT[mask_T] > 0).sum()),
        "gated-R": int((mR[mask_R] > 0).sum()),
    }
    readout_doc["n_included"] = {"gated-T": int(mask_T.sum()),
                                 "gated-R": int(mask_R.sum())}
    readout_doc["flips_vs_B"] = {
        "gated-T": readout["gated_T_flips_vs_B"],
        "gated-R": readout["gated_R_flips_vs_B"],
    }
    readout_doc["flip_ids_vs_B"] = {
        "gated-T": readout["gated_T_flip_ids"],
        "gated-R": readout["gated_R_flip_ids"],
    }
    readout_doc["delta_M"] = {c: agg_evidence[c]["delta"] for c in contrasts}
    readout_doc["mcnemar"] = {
        c: {"b": agg_evidence[c]["b"], "c": agg_evidence[c]["c"],
            "p": agg_evidence[c]["p"]} for c in contrasts}
    readout_doc["strata"] = {
        s: {c: {"n": cell_of[(c, s)]["n"],
                "delta": cell_of[(c, s)]["delta"],
                "b": cell_of[(c, s)]["mcnemar_b"],
                "c": cell_of[(c, s)]["mcnemar_c"],
                "p": cell_of[(c, s)]["mcnemar_p"]}
            for c in contrasts} for s in ("agg", "a_first", "c_first")}
    readout_doc["margin_shift_descriptive"] = desc
    readout_doc["delivery"] = {"fired_cell_rows": 2 * n_fired,
                               "in_band": 2 * n_fired - n_oob,
                               "out_of_band": n_oob, "exclusions": excluded}
    readout_doc["delta_theta"] = {"pre": pre, "post": post,
                                  "pin": pin.WEIGHTS_PIN,
                                  "verified": pre == post == pin.WEIGHTS_PIN}
    readout_doc["passes"] = {"total": passes[0],
                             "expected_max": EXPECTED_PASSES,
                             "hard_cap": HARD_CAP_PASSES}
    readout_doc["sanity_gates"] = readout["sanity"]
    with open(os.path.join(out_dir, "mechanical_readout.json"), "w") as f:
        json.dump(readout_doc, f, indent=2)

    artifact_hashes = {}
    for fname in ("per_item_records.csv", "per_item_gate.csv",
                  "per_item_delivery.csv", "constructor_manifest.json",
                  "env_manifest.json", "gate_integrity.json",
                  "delivery_probe_log.json", "regime_routing.json",
                  "stratum_table.json", "margin_shift_ledger.json",
                  "s3_7_rider.json", "decision_table_worksheet.json",
                  "mechanical_readout.json"):
        artifact_hashes[fname] = sha256_file(os.path.join(out_dir, fname))
    with open(os.path.join(out_dir, "artifact_hashes.txt"), "w") as f:
        for k, v in artifact_hashes.items():
            f.write(f"{v}  {k}\n")

    report = {
        "experiment": "EXP102",
        "mode": "real",
        "layer": LAYER,
        "gate_layer": GATE_LAYER,
        "ratio": RATIO,
        "coverage": coverage,
        "n_fired": n_fired,
        "exclusions": excluded,
        "routing": routing["routing"],
        "guards": {
            "G0": "pass (bench pin)",
            "G1'": "pass (real-tokenizer cover re-executed)",
            "Δθ=0": "pass (pre/post LOG-331 hash)",
            "G7": f"pass (constructor {CONSTRUCTOR_PIN[:16]}…, audit PASS)",
            "G5-L11": "pass (frozen verify_g5 core, d_0^(11) execution probe)",
            "STEP-0": "pass (60/60 B agreement; L11 signature OK; "
                      "L20 attention-math validation PASS)",
            "STEP-0iii": "pass (60/60 E/N<=0.5)",
            "STEP-1": f"{2 * n_fired - n_oob}/{2 * n_fired} fired rows in "
                      "band; 0 zero-norm directions",
            "STEP-2a": "pass (gate from B-pass L20 captures only; "
                      "fired⟺L20-mean≥τ 60/60)",
            "gate_rule": "L20-mean>=tau (gate\u2019s own mass only — "
                      "F2-class fence, §4.3)",
            "norm_ties": "60/60",
            "thread_pin": n_threads,
            "F5": "single environment (no mid-run rebuild)",
        },
        "run_meta": env_manifest,
    }
    return report


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for flag in FORBIDDEN_FLAGS:
        if any(a == flag or a.startswith(flag + "=") for a in argv):
            print(f"REFUSAL: forbidden flag {flag}.", file=sys.stderr)
            return 2
    ap = argparse.ArgumentParser(description="EXP102 executor")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ceo-clearance", action="store_true")
    ap.add_argument("--snapshot", default=None)
    args = ap.parse_args(argv)

    if not args.ceo_clearance:
        print("REFUSAL: real execution requires --ceo-clearance (LOG-4453).",
              file=sys.stderr)
        return 2

    os.makedirs(args.out_dir, exist_ok=True)
    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print(msg, flush=True)

    try:
        # G7.1 FIRST — before any guard, before any weight access.
        manifest = guard_g71_constructor()
        log(f"[g7] G7.1 pass: constructor {CONSTRUCTOR_PIN[:16]}… frozen, "
            "audit PASS.")
        bench, g0 = guard_g0_bench()
        log(f"[g0] G0 pass: bench pin {g0['pin'][:16]}…, 60 items.")
        report = run_real(bench, manifest,
                          args.snapshot or pin.SNAPSHOT_DIR, log,
                          args.out_dir)
    except Hold as e:
        with open(os.path.join(args.out_dir, "HOLD.txt"), "w") as f:
            f.write(str(e) + "\n")
        with open(os.path.join(args.out_dir, "exp102_run_log.txt"), "w") as f:
            f.write("\n".join(log_lines) + "\n")
        print(f"HOLD: {e}", file=sys.stderr)
        return 4
    except (RunInvalid, InjectRunInvalid, score102.RunInvalid) as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    with open(os.path.join(args.out_dir, "exp102_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(args.out_dir, "exp102_run_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print("[run] EXP102 records complete (UNINTERPRETED — verdict lane next).")
    print(f"[run] report: {os.path.join(args.out_dir, 'exp102_report.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
