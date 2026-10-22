"""EXP099 executor — S6-4 causal layer sweep (L8 / L20).

Licensed protocol: research/innovation/S6-4_PREREG_DRAFT_v2_2026-09-28.md
(binding chain: LOG-4424 (v1) -> LOG-4425 (Law #14 ACCEPT-WITH-FIXES, F1-F9)
-> LOG-4426 (v2 repair) -> LOG-4427 (delta SIGN) -> LOG-4428 (CEO clearance;
S6-4 minted as EXP099). This executor follows the licensed protocol EXACTLY;
any deviation is a STOP + new experiment number.

Design (licensed protocol §2):
  60 EXP092-B items x 5 arms (B, L20-only, L8-only, W20, W8) = 300
  experiment passes (+ construction machinery; 500 HARD CAP), CPU, $0.
  Per-layer ratio 0.38. UNGATED.
  Arms (all single-injection; one forward pass per (item, arm)):
    B        : no injection (single run per item; S5-1 v2 F2 precedent)
    L20-only : d_i^(20) @ 0.38*||h_i^(20,B)||_2  (consistency anchor —
               expected to reproduce EXP098's 6-flip set; NOT a discovery
               test, §0.1)
    L8-only  : d_i^(8) @ 0.38*||h_i^(8,B)||_2    (discovery test)
    W20      : g_i^(20), per-item norm-tied to L20-only (fresh seed)
    W8       : g_i^(8), per-item norm-tied to L8-only (fresh seed)
  {d_i^(20)}: regenerated from the frozen EXP098 procedure — identical C-1
              task-contrast on L20 residuals (Pass A vs P0), anchored to
              BASELINE L20 norms ||h_i^(20,B)|| (never the perturbed norm);
              constructor code hash-pinned
              5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361;
              pre-run re-hash, mismatch -> HOLD. Degeneracy-signature check:
              |recomputed mean|cos| - 0.6639| <= 0.05, else HOLD (§3 step 0).
  {d_i^(8)} : the IDENTICAL C-1 procedure run on L8 residual-stream
              activations (per-item direction from the same contrast, not a
              transported vector), ratio 0.38, anchored to BASELINE L8
              norms. New construction per §2.1; manifest required.
              Degeneracy gate (§3 step 2): mean|cos| >= 0.95 -> HOLD
              (executor; verdict lane maps per the pre-registered HOLD
              path). ANY zero-norm direction -> HOLD + diagnose (§3 step 1,
              F5 — a broken constructor is a setup defect, never silently
              substituted).
  {g_i^(20)}, {g_i^(8)}: per-item isotropic Gaussian directions, normalized
              and per-layer norm-tied (||g_i^(L)|| == ||d_i^(L)|| — 120
              assertions; the EXP096 double-scale bug class, guarded
              per-layer). Fresh pre-registered seeds R_SEED_W20 = 117011,
              R_SEED_W8 = 117013 — distinct from EXP098's R_SEED = 94094
              stream. Per-layer stream, item-major draw order (i = 0..59).

Binding execution order (licensed protocol §3, first match wins):
  0. Foundation gates FIRST: constructor re-hash vs pin; G0 bench;
     thread pin; Δθ=0 pre; G5 execution probes for layers 8 AND 20
     (frozen verify_g5 core, EXP098 machinery); B-arm zero-variance -> HOLD;
     per-item B agreement 60/60 vs archived EXP094 baseline (36/60) -> HOLD;
     L20 degeneracy-signature |recomputed - 0.6639| <= 0.05 -> HOLD.
  1. Delivery probe on the four injected (layer, arm) cells:
     (20, L20-only), (20, W20), (8, L8-only), (8, W8);
     perturbation_ratio = ||δ|| / ||h_i^(layer,B)|| in [0.285, 0.475].
     Non-injected cells are UNDEFINED and never probed (S6-2 v2 F3
     precedent). <=2 rows out of band per (layer, arm) -> excluded from
     that arm's contrasts (count-bars apply to the post-exclusion paired
     set, F4); >2 rows, or ANY zero-norm direction -> HOLD + diagnose.
  2. Degeneracy (L8 void logic): mean|cos| over {d_i^(8)} >= 0.95 -> HOLD
     (executor; the verdict lane rules per the pre-registered step-2 HOLD
     path — L8 void routes to PIVOT (step 8b, incomplete sweep)).
  3. Regime routing (machine-written): anchor COUNT first — L20-only flips
     != 6 -> HOLD (diagnosis lane; step-4 set-equality then runs in the
     diagnosis lane). Then: (W20 >= 1) OR (W8 >= 1) -> LIVE;
     (W20 = 0) AND (W8 = 0) AND (L8-only = 0) with anchor count verified
     = 6 -> FROZEN -> Underdetermined (verdict lane); asymmetric rule —
     a moving test arm routes LIVE. Sanity gates route per-arm
     RUN-INVALID where they fire (zero-variance; ties_arm/300 > 5%).
  4. Consistency anchor: L20-only flip SET must equal EXP098's L20-only
     flip set (the same 6 items; b=0, c=6 expected). Equality -> setup
     validated. Any difference -> HOLD (diagnose, never verdict).
  Steps 5-8 = VERDICT LANE (separate). This executor is MECHANICAL ONLY.

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


pin = _load_module("exp099_protocol_pin",
                   os.path.join(EXP093_DIR, "protocol_pin.py"))
import reference_implementation as ref
import g1prime
from inject import verify_g5, RunInvalid as InjectRunInvalid
from test_g7_audit import sha256_file

score099 = _load_module("exp099_scorer",
                        os.path.join(BUNDLE_DIR, "score_exp099.py"))

FORBIDDEN_FLAGS = (
    "--train", "--training", "--finetune", "--fine-tune", "--lr",
    "--learning-rate", "--gpu", "--cuda", "--gpus",
    "--mutate-weights", "--update-weights",
)

N_ITEMS = 60
RATIO = 0.38                      # per-layer construction setpoint (§2.2)
G5_BAND = (0.285, 0.475)          # protocol literals, not float products
G5_MAX_EXCLUDED = 2               # <=2 rows OOB -> excluded; >2 -> HOLD
DEGENERACY_BAR = 0.95
DEGENERACY_SIGNATURE_REF = 0.6639  # EXP098's archived L20 value
DEGENERACY_SIGNATURE_TOL = 0.05
TIE_DENOMINATOR = 300             # protocol §2.4 fixed denominator
TIE_RATE_BAR = 0.05
HARD_CAP_PASSES = 500
# 60 B + 60 construction-ref + 8 G5 execution probes + 240 sweep.
# v2 §2.3's "360 expected" counts the 300 (item, arm) experiment passes +
# 60 reserve; the construction ref passes and G5 probes are licensed
# executor machinery (EXP098 precedent: 368 under the same budget
# structure). The binding constraint is the 500 HARD CAP (not waivable).
EXPECTED_PASSES = 368
LAYERS = (8, 20)
# The four injected (layer, arm) cells (§3 step 1). Non-injected cells are
# undefined and never probed.
INJECTED_CELLS = [(20, "L20"), (20, "W20"), (8, "L8"), (8, "W8")]

# Fresh pre-registered R-arm seeds — distinct from EXP098's R_SEED = 94094.
R_SEED_W20 = 117011
R_SEED_W8 = 117013

CONSTRUCTOR_PIN = ("5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa"
                   "81917f361")
ARCHIVED_CSV = os.path.join(EXP094_DIR, "out", "per_item_records.csv")

# EXP098's L20-only flip set (derived from
# EXP098_multilayer_composition/out/per_item_records.csv: L20-only-vs-B,
# 6 flips, b=0, c=6 — all right->wrong). The step-4 set-equality check
# compares against these item ids.
EXP098_ANCHOR_SET = frozenset([
    "exp092_elemental_2hop_0",
    "exp092_elemental_2hop_10",
    "exp092_elemental_3hop_1",
    "exp092_planetary_2hop_11",
    "exp092_planetary_2hop_5",
    "exp092_planetary_2hop_7",
])


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

    cap8 = LayerCapture(model, 8)
    cap20 = LayerCapture(model, 20)

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

    a8, a20, h8_norms, h20_norms = [], [], [], []
    mB = np.zeros(N_ITEMS)
    rider = []  # S3-7 rider rows: per (item, arm) top-5
    baseline_top1 = []
    try:
        # ---- B arm (60 items; doubles as constructor Pass A) ----
        for i in range(N_ITEMS):
            logits = forward_ids(prompts[i])
            r8 = cap8.captured[-1, :].copy()
            r20 = cap20.captured[-1, :].copy()
            a8.append(r8)
            a20.append(r20)
            h8_norms.append(float(np.linalg.norm(r8)))
            h20_norms.append(float(np.linalg.norm(r20)))
            a_id, c_id = opt_ids[i]
            mB[i] = float(logits[-1, a_id] - logits[-1, c_id])
            t5 = top5_info(logits[-1], tokenizer)
            rider.append({"item_id": item_ids[i], "arm": "B", **t5})
            baseline_top1.append({"item_id": item_ids[i],
                                  "top1_id": t5["ids"][0],
                                  "top1_str": t5["strs"][0]})
        log(f"[run] B arm complete: 60 passes; B accuracy "
            f"{int((mB > 0).sum())}/60.")

        if bool((mB == mB[0]).all()):
            raise Hold(
                "STEP-0 HOLD: B-arm decisions zero-variance — the bench "
                "itself broke — HOLD + diagnose.")

        # ---- Reference passes (constructor Pass B: P0 + prompt) ----
        b8, b20 = [], []
        for i in range(N_ITEMS):
            forward_ids(p0_ids + prompts[i])
            b8.append(cap8.captured[-1, :].copy())
            b20.append(cap20.captured[-1, :].copy())
        log("[run] reference passes complete: 60 passes.")

        # ---- Construction: {d_i^(20)} (frozen regen) + {d_i^(8)} (new) ----
        # The IDENTICAL C-1 procedure (frozen constructor module, unmodified)
        # run on L20 residuals (regeneration, EXP098 procedure) and on L8
        # residuals (new construction, S6-4 v2 §2.1). Both anchored to
        # BASELINE per-layer norms (never the perturbed norm).
        d20, d8 = [], []
        for i in range(N_ITEMS):
            d, info = C.build_per_item_direction(
                a20[i], b20[i], h20_norms[i], ratio=RATIO)
            if info["degenerate_zero"]:
                raise Hold(
                    f"STEP-1 HOLD: zero-norm d_i^(20) on item {i} — "
                    "common-cause delivery failure — HOLD + diagnose.")
            d20.append(d)
            d, info = C.build_per_item_direction(
                a8[i], b8[i], h8_norms[i], ratio=RATIO)
            if info["degenerate_zero"]:
                raise Hold(
                    f"STEP-1 HOLD: zero-norm d_i^(8) on item {i} — the L8 "
                    "contrast failed to separate — HOLD + diagnose "
                    "(§2.1 HOLD path, F5).")
            d8.append(d)
        log("[run] construction complete: 60 d_i^(20) (frozen regen) + "
            f"60 d_i^(8) (new C-1 on L8 residuals) at ratio {RATIO}.")

        # ---- W-arm draws: fresh seeds, per-layer stream, item-major ----
        # g_i^(20) ~ rng(117011), g_i^(8) ~ rng(117013); each normalized
        # and per-layer norm-tied to the test arm's component.
        dim = a20[0].shape[0]
        g20, g8 = [], []
        for seed, d_vecs, g_vecs, tag in (
                (R_SEED_W20, d20, g20, "W20"),
                (R_SEED_W8, d8, g8, "W8")):
            rng = np.random.default_rng(seed)
            for i in range(N_ITEMS):
                z = np.asarray(rng.normal(size=dim), dtype=np.float64)
                z_norm = float(np.linalg.norm(z))
                if z_norm == 0.0:
                    raise Hold(f"STEP-1 HOLD: isotropic draw exactly zero "
                               f"({tag}, item {i}).")
                g_vecs.append((z / z_norm)
                              * float(np.linalg.norm(d_vecs[i])))
        log(f"[run] W draws complete: 60 g_i^(20) (seed {R_SEED_W20}) + "
            f"60 g_i^(8) (seed {R_SEED_W8}), item-major per stream.")

        # ---- Norm-tie assertions: 120 per-layer ties (EXP096 bug class) --
        tie_ok = {}  # (item, layer) -> bool
        for i in range(N_ITEMS):
            for tag, layer, gv, dv in (("W20", 20, g20[i], d20[i]),
                                       ("W8", 8, g8[i], d8[i])):
                nt = float(np.linalg.norm(dv))
                nw = float(np.linalg.norm(gv))
                ok = abs(nt - nw) <= 1e-9 * max(nt, 1e-300)
                tie_ok[(i, layer)] = bool(ok)
                if not ok:
                    raise Hold(
                        f"STEP-1 HOLD: norm-tie broken on item {i} arm "
                        f"{tag}: ||T||={nt:.6f} vs ||W||={nw:.6f} — "
                        "HOLD + diagnose.")
        log("[run] norm-tie check: 120/120 per-layer ties hold "
            "(||g_i^(L)|| == ||d_i^(L)||).")

        # ---- STEP-0(iii): L20 degeneracy signature vs 0.6639 (±0.05) ----
        u20 = np.stack([d / float(np.linalg.norm(d)) for d in d20])
        mean_abs_cos_20 = mean_pairwise_abs_cosine(u20)
        if abs(mean_abs_cos_20 - DEGENERACY_SIGNATURE_REF) > \
                DEGENERACY_SIGNATURE_TOL:
            raise Hold(
                f"STEP-0 HOLD: regenerated L20 mean|cos|={mean_abs_cos_20:.4f} "
                f"vs archived {DEGENERACY_SIGNATURE_REF} "
                f"(tol {DEGENERACY_SIGNATURE_TOL}) — HOLD + diagnose.")
        log(f"[run] L20 degeneracy signature: mean|cos|={mean_abs_cos_20:.4f} "
            f"(vs {DEGENERACY_SIGNATURE_REF} OK; gate {DEGENERACY_BAR}).")

        # ---- STEP-2 input: degeneracy gate on the NEW {d_i^(8)} set ----
        u8 = np.stack([d / float(np.linalg.norm(d)) for d in d8])
        mean_abs_cos_8 = mean_pairwise_abs_cosine(u8)
        log(f"[run] L8 degeneracy: mean|cos|={mean_abs_cos_8:.4f} "
            f"(gate {DEGENERACY_BAR}).")
        if mean_abs_cos_8 >= DEGENERACY_BAR:
            raise Hold(
                f"STEP-2 HOLD: L8 direction set degenerate "
                f"(mean|cos|={mean_abs_cos_8:.4f} >= {DEGENERACY_BAR}) — "
                "the L8 contrast failed to separate — HOLD per the §3 "
                "step-2 path (verdict lane rules per the pre-registered "
                "HOLD mapping). Facts logged; no sweep on a degenerate "
                "direction.")

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

        # ---- STEP-0 (cont.): G5 execution probes with the constructed ----
        # ---- item-0 directions (EXP098 machinery; layers 8 and 20) -------
        for layer_idx, d0 in ((8, d8[0]), (20, d20[0])):
            res = verify_g5_layer_real(model, tokenizer, bench[0]["prompt"],
                                       d0, layer_idx)
            passes[0] += 4  # ref + disabled + clean + injected
            if passes[0] > HARD_CAP_PASSES:
                raise RunInvalid("budget FAIL: hard cap exceeded — "
                                 "RUN-INVALID.")
            log(f"[run] G5 layer-{layer_idx} execution probe: PASS "
                f"(rel_err={res['criterion_i_rel_err']:.2e}, "
                f"other={res['criterion_ii_max_abs_change']:.2e}).")

        # ---- STEP-1 delivery probe on the four injected cells ----
        lo, hi = G5_BAND
        d_src = {"L20": d20, "W20": g20, "L8": d8, "W8": g8}
        h_src = {20: h20_norms, 8: h8_norms}
        cell_ratios = {}
        for layer, akey in INJECTED_CELLS:
            cell_ratios[(layer, akey)] = [
                float(np.linalg.norm(d_src[akey][i]) / h_src[layer][i])
                for i in range(N_ITEMS)]
        excluded = {}  # (layer, arm) -> sorted list of item indices
        for cell in INJECTED_CELLS:
            oob = sorted(k for k, r in enumerate(cell_ratios[cell])
                         if not (lo <= r <= hi))
            if len(oob) > G5_MAX_EXCLUDED:
                raise Hold(
                    f"STEP-1 HOLD: {len(oob)} rows out of band on cell "
                    f"{cell} (>{G5_MAX_EXCLUDED}) — HOLD + diagnose.")
            excluded[cell] = oob
        n_oob = sum(len(v) for v in excluded.values())
        log(f"[run] STEP-1 delivery: 240/240 cell-rows computed; "
            f"{240 - n_oob}/240 in band [{lo}, {hi}]; exclusions: "
            + ", ".join(f"{c}={len(v)}" for c, v in excluded.items()) + ".")
        mask = {
            "L20": np.array([i not in excluded[(20, "L20")]
                             for i in range(N_ITEMS)]),
            "W20": np.array([i not in excluded[(20, "W20")]
                             for i in range(N_ITEMS)]),
            "L8": np.array([i not in excluded[(8, "L8")]
                            for i in range(N_ITEMS)]),
            "W8": np.array([i not in excluded[(8, "W8")]
                            for i in range(N_ITEMS)]),
        }

        # ---- The sweep (single-injection arms) ----
        hook8 = LayerInjectionHook(layer_index=8, alpha=1.0)
        hook20 = LayerInjectionHook(layer_index=20, alpha=1.0)

        def single_pass(ids, layer_idx, vec, item_id, arm_name):
            hook = hook8 if layer_idx == 8 else hook20
            hook.attach(model, vec)
            hook.enable()
            try:
                ids_t = torch.tensor([ids], dtype=torch.long)
                with torch.no_grad():
                    lg = model(ids_t).logits[0].detach().cpu().to(
                        torch.float64).numpy()
            finally:
                hook.detach()
            passes[0] += 1
            if passes[0] > HARD_CAP_PASSES:
                raise RunInvalid("budget FAIL: hard cap exceeded — "
                                 "RUN-INVALID.")
            rider.append({"item_id": item_id, "arm": arm_name,
                          **top5_info(lg[-1], tokenizer)})
            return lg

        margins = {}
        arm_spec = [("L20", 20, d20, "L20-only"),
                    ("L8", 8, d8, "L8-only"),
                    ("W20", 20, g20, "W20"),
                    ("W8", 8, g8, "W8")]
        for key, layer_idx, vecs, arm_name in arm_spec:
            m = np.full(N_ITEMS, np.nan)
            for i in range(N_ITEMS):
                lg = single_pass(prompts[i], layer_idx, vecs[i],
                                 item_ids[i], arm_name)
                a_id, c_id = opt_ids[i]
                m[i] = float(lg[-1, a_id] - lg[-1, c_id])
            margins[key] = m
            log(f"[run] sweep {arm_name}: 60/60 passes complete.")
        log(f"[run] sweep complete. Total passes: {passes[0]} "
            f"(expected {EXPECTED_PASSES}, cap {HARD_CAP_PASSES}).")
    finally:
        cap8.remove()
        cap20.remove()

    # Δθ=0 (post)
    post = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if post != pin.WEIGHTS_PIN:
        raise RunInvalid("Δθ=0 FAIL (post): state_dict changed — RUN-INVALID.")
    log("[run] Δθ=0 post-run hash OK (Δθ=0 verified).")

    # ---- Mechanical scoring (no verdict) ----
    table, sec = score099.score_all(
        mB, margins["L20"], margins["L8"], margins["W20"], margins["W8"],
        phrasing, mask["L20"], mask["L8"], mask["W20"], mask["W8"])
    log(f"[run] scoring complete: {len(table)} stratum cells "
        f"(3 strata x 5 contrasts).")

    # ---- STEP-3 (F2): anchor COUNT before regime routing ----
    l20_flips = sec["flips_vs_B"]["L20"]
    anchor_log = {
        "step": 4,
        "expected_set": sorted(EXP098_ANCHOR_SET),
        "expected_count": 6,
        "expected_b": 0,
        "expected_c": 6,
        "observed_count": l20_flips,
        "observed_b": int(table["agg__L20B"]["mcnemar_b"]),
        "observed_c": int(table["agg__L20B"]["mcnemar_c"]),
        "note": "setup validation, not a verdict step",
    }
    if l20_flips != 6:
        # HOLD before routing; set-equality runs inside the diagnosis lane.
        observed_ids = sorted(
            item_ids[i] for i in
            (sec["flip_ledgers"]["L20"]["x_to_right"]
             + sec["flip_ledgers"]["L20"]["x_to_wrong"]))
        anchor_log["observed_set"] = observed_ids
        anchor_log["set_equality"] = "deferred to diagnosis lane"
        with open(os.path.join(out_dir, "consistency_anchor.json"),
                  "w") as f:
            json.dump(anchor_log, f, indent=2)
        raise Hold(
            f"STEP-3 HOLD (F2): L20-only flips = {l20_flips} != 6 — the "
            "frozen pipeline changed — HOLD + diagnose (step-4 set-equality "
            "runs inside the diagnosis lane).")
    log(f"[run] anchor count check: L20-only flips = {l20_flips} == 6 — "
        "proceed to regime routing.")

    # ---- Regime routing (machine-written, §3 step 3 as repaired) ----
    w20_flips = sec["flips_vs_B"]["W20"]
    w8_flips = sec["flips_vs_B"]["W8"]
    l8_flips = sec["flips_vs_B"]["L8"]
    if w20_flips >= 1 or w8_flips >= 1:
        route, why = ("LIVE",
                      f"(W20={w20_flips} >= 1) OR (W8={w8_flips} >= 1)")
    elif l8_flips >= 1:
        route, why = ("LIVE",
                      f"W20 = 0 and W8 = 0 with L8-only = {l8_flips} >= 1 "
                      "(asymmetric liveness rule: a moving test arm "
                      "routes LIVE)")
    else:
        route, why = ("FROZEN",
                      "W20 = 0 and W8 = 0 and L8-only = 0 with the anchor "
                      "count verified = 6 (delivery confirmed)")
    routing = {
        "routing": route,
        "routing_reason": why,
        "anchor_count_verified": 6,
        "evidence": {
            "L20_flips_vs_B": l20_flips,
            "L8_flips_vs_B": l8_flips,
            "W20_flips_vs_B": w20_flips,
            "W8_flips_vs_B": w8_flips,
            "delivery_confirmed": True,
            "tie_counts": sec["tie_counts"],
            "tie_gate_arms": sec["tie_gate_arms"],
            "zero_variance": sec["zero_variance"],
            "coherence_arms": sec["coherence_arms"],
            "n_included": sec["n_included"],
        },
        "note": "machine-written before the table walk; "
                "per-arm RUN-INVALID routed where sanity gates fire",
    }
    log(f"[run] regime routing: {route} ({why}).")

    # ---- STEP-4: consistency anchor set-equality ----
    observed_ids = sorted(
        item_ids[i] for i in
        (sec["flip_ledgers"]["L20"]["x_to_right"]
         + sec["flip_ledgers"]["L20"]["x_to_wrong"]))
    anchor_log["observed_set"] = observed_ids
    anchor_log["set_equality"] = (set(observed_ids) == EXP098_ANCHOR_SET)
    with open(os.path.join(out_dir, "consistency_anchor.json"), "w") as f:
        json.dump(anchor_log, f, indent=2)
    if set(observed_ids) != EXP098_ANCHOR_SET:
        raise Hold(
            "STEP-4 HOLD: L20-only flip set != EXP098's L20-only flip set — "
            "the frozen pipeline changed — HOLD + diagnose (never verdict).")
    log("[run] consistency anchor: L20-only flip set == EXP098's 6-item "
        "set — setup validated.")

    # ---- Margin-shift ledger (descriptive only; no classifier licensed) --
    dm = {k: margins[k] - mB for k in ("L20", "L8", "W20", "W8")}
    ledger = []
    for i in range(N_ITEMS):
        ledger.append({
            "item": i,
            "item_id": item_ids[i],
            "stratum": phrasing[i],
            "dM_L20": float(dm["L20"][i]),
            "dM_L8": float(dm["L8"][i]),
            "dM_W20": float(dm["W20"][i]),
            "dM_W8": float(dm["W8"][i]),
        })
    desc = {}
    for k in ("L20", "L8", "W20", "W8"):
        v = dm[k]
        desc[k] = {"mean": float(v.mean()), "std": float(v.std()),
                   "min": float(v.min()), "max": float(v.max()),
                   "n_nonzero": int((v != 0.0).sum())}
    log("[run] margin-shift ledger: 60 rows; descriptive aggregates "
        "computed.")

    # ---- Persist (§5 instrumentation spec, append-only) ----
    arm_names = {"B": "B", "L20": "L20-only", "L8": "L8-only",
                 "W20": "W20", "W8": "W8"}
    with open(os.path.join(out_dir, "per_item_records.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "stratum", "arm", "correct_top1", "margin",
                    "margin_shift_vs_B"])
        all_m = {"B": mB, **margins}
        for key in ("B", "L20", "L8", "W20", "W8"):
            mm = all_m[key]
            for i, iid in enumerate(item_ids):
                w.writerow([iid, phrasing[i], arm_names[key],
                            int(mm[i] > 0.0), f"{mm[i]:.10f}",
                            f"{(mm[i] - mB[i]):.10f}" if key != "B"
                            else "0.0000000000"])

    with open(os.path.join(out_dir, "per_layer_delivery.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "arm", "layer", "perturbation_ratio",
                    "norm_target", "h_norm_B", "in_band",
                    "excluded_from_contrasts", "norm_tie_ok"])
        for (layer, akey), ratios in cell_ratios.items():
            src = d_src[akey]
            is_w_arm = akey in ("W20", "W8")
            for i, iid in enumerate(item_ids):
                nt = float(np.linalg.norm(src[i]))
                tie_cell = ("y" if tie_ok[(i, layer)] else "n") \
                    if is_w_arm else "na"
                w.writerow([iid, arm_names[akey], layer, f"{ratios[i]:.10f}",
                            f"{nt:.10f}", f"{h_src[layer][i]:.10f}",
                            "y" if lo <= ratios[i] <= hi else "n",
                            "y" if i in excluded[(layer, akey)] else "n",
                            tie_cell])

    ctor_manifest = {
        "constructor_sha256": CONSTRUCTOR_PIN,
        "constructor_sha256_live": sha256_file(
            os.path.join(EXP094_DIR, "constructor.py")),
        "P0_sha256": manifest["P0_sha256"],
        "NORM_RATIO": C.NORM_RATIO,
        "RATIO": RATIO,
        "G5_BAND": list(G5_BAND),
        "R_SEED_W20": R_SEED_W20,
        "R_SEED_W8": R_SEED_W8,
        "R_seed_note": "fresh pre-registered seeds, distinct from EXP098's "
                       "R_SEED=94094 stream; per-layer stream, item-major "
                       "draw order (i = 0..59)",
        "g7_carryover": "EXP094 constructor_manifest.json (audit PASS)",
        "L20_direction_note": "frozen C-1 procedure (identical code, "
                              "hash-pinned) on L20 residuals (Pass A vs "
                              "P0); anchored to BASELINE L20 norms; "
                              "regeneration of the EXP098 procedure",
        "L8_direction_note": "IDENTICAL C-1 procedure on L8 residuals "
                             "(Pass A vs P0); anchored to BASELINE L8 "
                             "norms; new construction per S6-4 v2 §2.1 "
                             "(procedure hash = constructor_sha256)",
        "W_draw_order": "per-layer stream: for i in 0..59, draw "
                        "z_i^(layer) ~ N(0, I) from "
                        "np.random.default_rng(R_SEED_W{layer}); each "
                        "normalized and per-layer norm-tied to the test "
                        "arm's component",
        "norm_tie_assertions": "120/120 pass (||g_i^(L)|| == ||d_i^(L)||)",
        "L20_degeneracy_signature": {
            "archived_ref": DEGENERACY_SIGNATURE_REF,
            "recomputed": mean_abs_cos_20,
            "tol": DEGENERACY_SIGNATURE_TOL,
            "pass": True,
        },
        "L8_degeneracy_gate": {
            "mean_pairwise_abs_cosine": mean_abs_cos_8,
            "bar": DEGENERACY_BAR,
            "gate_fired": bool(mean_abs_cos_8 >= DEGENERACY_BAR),
        },
        "per_item": [
            {"item": i, "item_id": item_ids[i],
             "d20_norm": float(np.linalg.norm(d20[i])),
             "d8_norm": float(np.linalg.norm(d8[i])),
             "g20_norm": float(np.linalg.norm(g20[i])),
             "g8_norm": float(np.linalg.norm(g8[i])),
             "h20_norm_B": h20_norms[i],
             "h8_norm_B": h8_norms[i],
             "norm_tie_ok_L20": tie_ok[(i, 20)],
             "norm_tie_ok_L8": tie_ok[(i, 8)]}
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
        "seeds": {"R_SEED_W20": R_SEED_W20, "R_SEED_W8": R_SEED_W8,
                  "G5_probe_seed": 31337},
        "single_environment_F5": "all passes in this environment; "
                                 "no mid-run rebuild",
        "n_passes": passes[0],
        "expected_passes": EXPECTED_PASSES,
        "hard_cap": HARD_CAP_PASSES,
        "budget_note": "360 expected per v2 §2.3 counts the 300 (item, "
                       "arm) experiment passes + 60 reserve; the 60 "
                       "construction-ref passes and 8 G5 execution probes "
                       "are licensed executor machinery (EXP098 precedent: "
                       "368 under the same budget structure); the binding "
                       "constraint is the 500 HARD CAP (not waivable)",
    }
    with open(os.path.join(out_dir, "env_manifest.json"), "w") as f:
        json.dump(env_manifest, f, indent=2)

    with open(os.path.join(out_dir, "delivery_probe_log.json"), "w") as f:
        json.dump({
            "band": list(G5_BAND),
            "n_cell_rows": 240,
            "in_band": 240 - n_oob,
            "out_of_band": n_oob,
            "exclusions": {f"({c[0]},{c[1]})": v
                           for c, v in excluded.items()},
            "per_cell_PASS_FAIL": {
                f"({c[0]},{c[1]})":
                ("PASS" if len(excluded[c]) <= G5_MAX_EXCLUDED else "FAIL")
                for c in INJECTED_CELLS},
            "per_cell_ratios": {
                f"({c[0]},{c[1]})": [round(x, 10) for x in cell_ratios[c]]
                for c in INJECTED_CELLS},
            "realized_vs_perturbed_note": "all four arms are "
                "single-injection (no co-injection cascade); the hook adds "
                "δ directly to the post-block residual at the final "
                "position, so the realized injection ratio == the analytic "
                "perturbation_ratio by construction; placement validated "
                "by the G5 execution probes (frozen verify_g5 core, "
                "criterion i) at both layers",
        }, f, indent=2)

    with open(os.path.join(out_dir, "regime_routing.json"), "w") as f:
        json.dump(routing, f, indent=2)

    with open(os.path.join(out_dir, "stratum_table.json"), "w") as f:
        json.dump(table, f, indent=2)

    with open(os.path.join(out_dir, "margin_shift_ledger.json"), "w") as f:
        json.dump({"rows": ledger, "descriptive": desc,
                   "note": "descriptive only; alters no verdict"}, f, indent=2)

    # S3-7 instrumentation rider (no analysis pre-registered).
    with open(os.path.join(out_dir, "s3_7_rider.json"), "w") as f:
        json.dump({
            "rows": [{"item_id": r["item_id"], "arm": r["arm"],
                      "top5": [{"id": r["ids"][k], "str": r["strs"][k],
                                "logit": r["logits"][k]} for k in range(5)]}
                     for r in rider],
            "baseline_top1": baseline_top1,
            "note": "rider only (LOG-4408 watchlist); no analysis "
                    "pre-registered",
        }, f, indent=2)

    # Decision-table worksheet: the §3 step walk is BLANK for the verdict
    # lane (this executor does not walk it); evidence cells are recorded.
    contrasts = ("L20B", "L8B", "W20B", "W8B", "L8W8")
    agg_evidence = {
        c: {"n": table[f"agg__{c}"]["n"],
            "delta": table[f"agg__{c}"]["delta"],
            "b": table[f"agg__{c}"]["mcnemar_b"],
            "c": table[f"agg__{c}"]["mcnemar_c"],
            "p": table[f"agg__{c}"]["mcnemar_p"]}
        for c in contrasts}
    worksheet = [
        {"step": 0, "condition": "foundation gates",
         "evidence": {
             "constructor_rehash": "match frozen pin",
             "G5_layer_8": "PASS (frozen verify_g5 core, d_0^(8) probe)",
             "G5_layer_20": "PASS (frozen verify_g5 core, d_0^(20) probe)",
             "B_agreement": "60/60 per-item vs archived EXP094 baseline",
             "B_accuracy": int((mB > 0).sum()),
             "L20_degeneracy_signature":
                 f"{mean_abs_cos_20:.4f} vs {DEGENERACY_SIGNATURE_REF} "
                 f"(tol {DEGENERACY_SIGNATURE_TOL}) — PASS"},
         "walk": "BLANK — verdict lane"},
        {"step": 1, "condition": "delivery (240 cell-rows in band)",
         "evidence": {"in_band": 240 - n_oob, "out_of_band": n_oob,
                      "exclusions": {f"({c[0]},{c[1]})": v
                                     for c, v in excluded.items()},
                      "zero_norm_directions": 0},
         "walk": "BLANK — verdict lane"},
        {"step": 2, "condition": "degeneracy gate input (L8)",
         "evidence": {"mean_abs_cosine_8": mean_abs_cos_8,
                      "bar": DEGENERACY_BAR,
                      "gate_fired": bool(mean_abs_cos_8 >= DEGENERACY_BAR)},
         "walk": "BLANK — verdict lane"},
        {"step": 3, "condition": "regime routing (machine-written)",
         "evidence": routing, "walk": "BLANK — verdict lane"},
        {"step": 4, "condition": "consistency anchor (set-equality)",
         "evidence": anchor_log, "walk": "BLANK — verdict lane"},
        {"step": 5, "condition": "fragility PIVOT (first-match-wins)",
         "evidence": {"aggregate_contrasts": agg_evidence,
                      "note": "step-5 disjuncts evaluated by the verdict "
                              "lane from these numbers"},
         "walk": "BLANK — verdict lane"},
        {"step": 6, "condition": "licensed positive (L8)",
         "evidence": {"aggregate_contrasts": agg_evidence,
                      "stratum_cells": "stratum_table.json (A__L8B, C__L8B)",
                      "note": "full conjunction evaluated by the verdict "
                              "lane"},
         "walk": "BLANK — verdict lane"},
        {"step": "6-caveat", "condition": "post-step-6 L20-fragility caveat",
         "evidence": {"W20_flips": w20_flips,
                      "aggregate_contrasts": agg_evidence},
         "walk": "BLANK — verdict lane"},
        {"step": 7, "condition": "sweep KILL",
         "evidence": {"aggregate_contrasts": agg_evidence,
                      "regime": routing["routing"],
                      "note": "KILL requires regime LIVE with L8-liveness "
                              "(F3)"},
         "walk": "BLANK — verdict lane"},
        {"step": 8, "condition": "otherwise -> PIVOT (named sub-cases)",
         "evidence": {"aggregate_contrasts": agg_evidence},
         "walk": "BLANK — verdict lane"},
    ]
    with open(os.path.join(out_dir, "decision_table_worksheet.json"),
              "w") as f:
        json.dump(worksheet, f, indent=2)

    # Mechanical read-out (UNINTERPRETED — verdict lane walks §3 steps 5-8).
    readout = {"status": "UNINTERPRETED_MECHANICAL_READOUT",
               "experiment": "EXP099"}
    readout["routing"] = routing["routing"]
    readout["routing_reason"] = routing["routing_reason"]
    readout["anchor"] = {"count": l20_flips, "expected": 6,
                         "set_equal": anchor_log["set_equality"]}
    readout["n_correct"] = sec["n_correct"]
    readout["n_included"] = sec["n_included"]
    readout["flips_vs_B"] = sec["flips_vs_B"]
    readout["flip_ledgers_vs_B"] = {
        k: {"n_to_right": len(v["x_to_right"]),
            "n_to_wrong": len(v["x_to_wrong"])}
        for k, v in sec["flip_ledgers"].items()}
    readout["delta_M"] = {c: table[f"agg__{c}"]["delta"] for c in contrasts}
    readout["mcnemar"] = {
        c: {"b": table[f"agg__{c}"]["mcnemar_b"],
            "c": table[f"agg__{c}"]["mcnemar_c"],
            "p": table[f"agg__{c}"]["mcnemar_p"]} for c in contrasts}
    readout["strata"] = {
        s: {c: {"n": table[f"{s}__{c}"]["n"],
                "delta": table[f"{s}__{c}"]["delta"],
                "b": table[f"{s}__{c}"]["mcnemar_b"],
                "c": table[f"{s}__{c}"]["mcnemar_c"],
                "p": table[f"{s}__{c}"]["mcnemar_p"]}
            for c in contrasts} for s in ("agg", "A", "C")}
    readout["margin_shift_descriptive"] = desc
    readout["delivery"] = {"in_band": 240 - n_oob, "out_of_band": n_oob,
                           "exclusions": {f"({c[0]},{c[1]})": v
                                          for c, v in excluded.items()}}
    readout["delta_theta"] = {"pre": pre, "post": post,
                              "pin": pin.WEIGHTS_PIN,
                              "verified": pre == post == pin.WEIGHTS_PIN}
    readout["passes"] = {"total": passes[0], "expected": EXPECTED_PASSES,
                         "hard_cap": HARD_CAP_PASSES}
    readout["sanity_gates"] = {"tie_gate_arms": sec["tie_gate_arms"],
                               "coherence_arms": sec["coherence_arms"],
                               "tie_counts": sec["tie_counts"]}
    with open(os.path.join(out_dir, "mechanical_readout.json"), "w") as f:
        json.dump(readout, f, indent=2)

    artifact_hashes = {}
    for fname in ("per_item_records.csv", "per_layer_delivery.csv",
                  "constructor_manifest.json", "env_manifest.json",
                  "delivery_probe_log.json", "regime_routing.json",
                  "consistency_anchor.json", "stratum_table.json",
                  "margin_shift_ledger.json", "s3_7_rider.json",
                  "decision_table_worksheet.json", "mechanical_readout.json"):
        artifact_hashes[fname] = sha256_file(os.path.join(out_dir, fname))
    with open(os.path.join(out_dir, "artifact_hashes.txt"), "w") as f:
        for k, v in artifact_hashes.items():
            f.write(f"{v}  {k}\n")

    report = {
        "experiment": "EXP099",
        "mode": "real",
        "layers": list(LAYERS),
        "ratio": RATIO,
        "exclusions": {f"({c[0]},{c[1]})": v for c, v in excluded.items()},
        "routing": routing["routing"],
        "anchor": {"count": l20_flips, "set_equal": anchor_log["set_equality"]},
        "guards": {
            "G0": "pass (bench pin)",
            "G1'": "pass (real-tokenizer cover re-executed)",
            "Δθ=0": "pass (pre/post LOG-331 hash)",
            "G7": f"pass (constructor {CONSTRUCTOR_PIN[:16]}…, audit PASS)",
            "G5-L8": "pass (frozen verify_g5 core, d_0^(8) execution probe)",
            "G5-L20": "pass (frozen verify_g5 core, d_0^(20) execution probe)",
            "STEP-0": "pass (60/60 B agreement; L20 signature OK)",
            "STEP-1": f"{240 - n_oob}/240 in band; 0 zero-norm directions",
            "STEP-2": f"L8 mean|cos|={mean_abs_cos_8:.4f} "
                      f"(bar {DEGENERACY_BAR})",
            "STEP-3": f"anchor count {l20_flips}/6; routing {routing['routing']}",
            "STEP-4": "anchor set-equality PASS",
            "norm_ties": "120/120",
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
    ap = argparse.ArgumentParser(description="EXP099 executor")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ceo-clearance", action="store_true")
    ap.add_argument("--snapshot", default=None)
    args = ap.parse_args(argv)

    if not args.ceo_clearance:
        print("REFUSAL: real execution requires --ceo-clearance (LOG-4428).",
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
        with open(os.path.join(args.out_dir, "exp099_run_log.txt"), "w") as f:
            f.write("\n".join(log_lines) + "\n")
        print(f"HOLD: {e}", file=sys.stderr)
        return 4
    except (RunInvalid, InjectRunInvalid, score099.RunInvalid) as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    with open(os.path.join(args.out_dir, "exp099_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(args.out_dir, "exp099_run_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print("[run] EXP099 records complete (UNINTERPRETED — verdict lane next).")
    print(f"[run] report: {os.path.join(args.out_dir, 'exp099_report.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
