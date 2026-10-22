"""EXP098 executor — S6-2 multi-layer composition (L11+L20 co-injection).

Licensed protocol: research/innovation/S6-2_PREREG_DRAFT_v2_2026-09-28.md
(binding Law #14 ACCEPT-WITH-FIXES: LOG-4418; v2 repair: LOG-4419;
independent delta re-verification SIGN: LOG-4420; CEO execution clearance:
LOG-4421; S6-2 minted as EXP098). This executor follows the licensed
protocol EXACTLY; any deviation is a STOP + new experiment number.

Design (licensed protocol §2):
  60 EXP092-B items x 5 arms (B, L11-only, L20-only, Joint, W-joint) =
  300 passes (+ 60 reference = 360 expected, 500 HARD CAP), CPU, $0.
  Per-layer ratio 0.38 (alpha = 8.0 equivalent; executor ratio parameter
  0.38 directly). UNGATED.
  Arms:
    B        : no injection (single run per item; S5-1 v2 F2 precedent)
    L11-only : d_i^(11) @ 0.38*||h_i^(11,B)||_2  (premise check)
    L20-only : d_i^(20) @ 0.38*||h_i^(20,B)||_2  (premise + novel L20 test)
    Joint    : d_i^(11) @ L11 AND d_i^(20) @ L20 in ONE forward pass
               (L11 injected; layers 12-19 transform; L20 injected)
    W-joint  : g_i^(11) @ L11 AND g_i^(20) @ L20 in one pass, per-layer
               norm-tied to the Joint arm's components (120 assertions)
  {d_i^(11)}: frozen EXP094 constructor (hash pin below), ratio 0.38.
  {d_i^(20)}: the IDENTICAL contrast procedure (frozen constructor module
              C.build_per_item_direction, unmodified) run on L20 residual
              activations; anchored to the BASELINE L20 norm ||h_i^(20,B)||
              (never the perturbed norm). Degeneracy gate >= 0.95 and the
              >2 zero-norm HOLD path are pre-registered (§2.1, §3 step 2).
  {g_i^(.)}: pinned RNG (R_SEED=94094), item-major draw order (per item:
             L11 draw then L20 draw), each normalized and scaled to the
             per-layer Joint norm. Documented in the manifest.

Binding execution order (licensed protocol §3, first match wins):
  0. Foundation gates FIRST: constructor re-hash vs pin; G0 bench;
     thread pin; Δθ=0 pre; G5 placement probes for layers 11 AND 20
     (frozen verify_g5 core); B-arm zero-variance -> HOLD; per-item B
     agreement 60/60 vs archived EXP094 -> HOLD; degeneracy sanity on
     {d_i^(11)} vs 0.7923 (tol 0.05) -> HOLD.
  1. Delivery probe on the six injected (layer, arm) cells:
     (11,L11-only),(20,L20-only),(11,Joint),(20,Joint),
     (11,W-joint),(20,W-joint); perturbation_ratio in [0.285, 0.475].
     Non-injected cells are UNDEFINED and never probed (F3).
     <=2 rows out of band per (layer, arm) -> excluded from that arm's
     contrasts; >2 rows, or ANY zero-norm direction -> HOLD + diagnose.
  2. Degeneracy: mean|cos| over {d_i^(20)} >= 0.95 -> HALT (HOLD with
     facts; the verdict lane rules Underdetermined per the pre-registered
     HOLD path). {d_i^(11)} >= 0.95 -> same.
  Regime routing (machine-written, §3 step 3): W-joint flips >= 1 -> LIVE;
  W-joint = 0 AND joint = 0 (delivery confirmed) -> FROZEN ->
  Underdetermined (verdict lane); W-joint = 0 with joint >= 1 -> LIVE
  (asymmetric rule). Sanity gates route per-arm RUN-INVALID where they
  fire (zero-variance; ties_arm/300 > 5% literal reading).
  Steps 4-8 = VERDICT LANE (separate). This executor is MECHANICAL ONLY.

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


pin = _load_module("exp098_protocol_pin",
                   os.path.join(EXP093_DIR, "protocol_pin.py"))
import reference_implementation as ref
import g1prime
from inject import verify_g5, RunInvalid as InjectRunInvalid
from test_g7_audit import sha256_file

score098 = _load_module("exp098_scorer",
                        os.path.join(BUNDLE_DIR, "score_exp098.py"))

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
DEGENERACY_SANITY_REF = 0.7923   # EXP094's archived value (L11)
DEGENERACY_SANITY_TOL = 0.05
TIE_DENOMINATOR = 300             # protocol §2.4 fixed denominator
TIE_RATE_BAR = 0.05
HARD_CAP_PASSES = 500
EXPECTED_PASSES = 368             # 60 B + 60 Ref + 8 G5 probes + 240 sweep
LAYERS = (11, 20)
# The six injected (layer, arm) cells (§3 step 1, F3). Non-injected cells
# are undefined and never probed.
INJECTED_CELLS = [(11, "L11"), (20, "L20"), (11, "J"), (20, "J"),
                  (11, "W"), (20, "W")]

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


class LayerInjectionHook:
    """Forward hook adding alpha*v at the final position of a given layer's
    post-block residual. attach()/detach(); enable()/disable().

    This is the frozen TorchInjectionHook's mechanics (identical _hook_fn,
    identical G5 criteria) generalized to an explicit layer index — the
    protocol requires co-injection at layers 11 AND 20 in one forward pass,
    which the frozen single-layer class cannot express. Misplacement is
    caught by the frozen verify_g5 core, not by trust.
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
    core (identical criteria i/ii/iii)."""
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


def nearly_moved(dm, mB):
    """§2.5 classifier (descriptive only; frozen definition)."""
    dm = float(dm)
    mB = float(mB)
    if mB == 0.0:
        return bool(abs(dm) > 0.0)
    return bool((np.sign(dm) == -np.sign(mB)) and
                (abs(dm) >= 0.5 * abs(mB)))


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

    # ---- G5 placement probes are foundation gates but run AFTER construction,
    # using the ACTUAL constructed item-0 directions as probe vectors (EXP094
    # precedent: run_exp094.py L277-278). A norm-0.38-absolute random probe
    # fails criterion (i) at 1e-6 on this model because the float32 hook
    # arithmetic's rounding (~6e-8 * ||clean||) exceeds 1e-6 * ||v|| when
    # ||clean||/||v|| >> 1/0.38; the constructed d_0 has ||d_0|| = 0.38 *
    # ||clean||, so the probe exercises the true operating ratio. The probes
    # are placed here (step 0, before the sweep) — see below after the
    # B-agreement check.

    p0_ids = tokenizer.encode(C.P0_TEXT, add_special_tokens=False)
    prompts = [tokenizer.encode(b["prompt"], add_special_tokens=False)
               for b in bench]

    cap11 = LayerCapture(model, 11)
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

    a11, a20, h11_norms, h20_norms = [], [], [], []
    mB = np.zeros(N_ITEMS)
    try:
        # ---- B arm (60 items; doubles as constructor Pass A) ----
        for i in range(N_ITEMS):
            logits = forward_ids(prompts[i])
            r11 = cap11.captured[-1, :].copy()
            r20 = cap20.captured[-1, :].copy()
            a11.append(r11)
            a20.append(r20)
            h11_norms.append(float(np.linalg.norm(r11)))
            h20_norms.append(float(np.linalg.norm(r20)))
            a_id, c_id = opt_ids[i]
            mB[i] = float(logits[-1, a_id] - logits[-1, c_id])
        log(f"[run] B arm complete: 60 passes; B accuracy "
            f"{int((mB > 0).sum())}/60.")

        if bool((mB == mB[0]).all()):
            raise Hold(
                "STEP-0 HOLD: B-arm decisions zero-variance — the bench "
                "itself broke — HOLD + diagnose.")

        # ---- Reference passes (constructor Pass B: P0 + prompt) ----
        b11, b20 = [], []
        for i in range(N_ITEMS):
            forward_ids(p0_ids + prompts[i])
            b11.append(cap11.captured[-1, :].copy())
            b20.append(cap20.captured[-1, :].copy())
        log("[run] reference passes complete: 60 passes.")

        # ---- Construction (frozen C-1 procedure on L11 AND L20) ----
        d11, d20 = [], []
        info11, info20 = [], []
        for i in range(N_ITEMS):
            d, info = C.build_per_item_direction(
                a11[i], b11[i], h11_norms[i], ratio=RATIO)
            if info["degenerate_zero"]:
                raise Hold(
                    f"STEP-1 HOLD: zero-norm d_i^(11) on item {i} — "
                    "common-cause delivery failure — HOLD + diagnose.")
            d11.append(d)
            info11.append(info)
            d, info = C.build_per_item_direction(
                a20[i], b20[i], h20_norms[i], ratio=RATIO)
            if info["degenerate_zero"]:
                raise Hold(
                    f"STEP-1 HOLD: zero-norm d_i^(20) on item {i} — the "
                    "L20 contrast failed to separate — HOLD + diagnose "
                    "(§2.1 HOLD path).")
            d20.append(d)
            info20.append(info)
        log("[run] construction complete: 60 d_i^(11) + 60 d_i^(20) at "
            f"ratio {RATIO} (frozen C-1 procedure, L20 anchored to "
            "baseline L20 norms).")

        # ---- W-joint draws: pinned RNG, item-major (L11 then L20/item) ----
        # Documented choice: each (item, layer) gets its own isotropic draw
        # from the single R_SEED stream (the natural two-layer extension of
        # the R-arm precedent). Independent per layer = the isotropic-noise
        # model the control is named for.
        dim = a11[0].shape[0]
        rng = np.random.default_rng(C.R_SEED)
        g11, g20 = [], []
        for i in range(N_ITEMS):
            for layer_vecs, d_vecs in (("L11", d11), ("L20", d20)):
                z = np.asarray(rng.normal(size=dim), dtype=np.float64)
                z_norm = float(np.linalg.norm(z))
                if z_norm == 0.0:
                    raise Hold("STEP-1 HOLD: isotropic draw exactly zero.")
                z = z / z_norm
                g = z * float(np.linalg.norm(d_vecs[i]))
                (g11 if layer_vecs == "L11" else g20).append(g)
        log(f"[run] W-joint draws complete: 120 isotropic draws "
            f"(R_SEED={C.R_SEED}, item-major L11-then-L20 per item).")

        # ---- Norm-tie assertions: 120 per-layer ties (EXP096 bug class) --
        for i in range(N_ITEMS):
            for tag, gv, dv in (("L11", g11[i], d11[i]),
                                ("L20", g20[i], d20[i])):
                nt = float(np.linalg.norm(dv))
                nw = float(np.linalg.norm(gv))
                if abs(nt - nw) > 1e-9 * max(nt, 1e-300):
                    raise Hold(
                        f"STEP-1 HOLD: norm-tie broken on item {i} layer "
                        f"{tag}: ||T||={nt:.6f} vs ||W||={nw:.6f} — "
                        "HOLD + diagnose.")
        log("[run] norm-tie check: 120/120 per-layer ties hold "
            "(||g_i^(L)|| == ||d_i^(L)||).")

        # ---- STEP-0(iii): degeneracy sanity on {d_i^(11)} vs 0.7923 ----
        u11 = np.stack([d / float(np.linalg.norm(d)) for d in d11])
        mean_abs_cos_11 = mean_pairwise_abs_cosine(u11)
        if abs(mean_abs_cos_11 - DEGENERACY_SANITY_REF) > DEGENERACY_SANITY_TOL:
            raise Hold(
                f"STEP-0 HOLD: regenerated L11 mean|cos|={mean_abs_cos_11:.4f} "
                f"vs archived {DEGENERACY_SANITY_REF} — HOLD + diagnose.")
        log(f"[run] L11 degeneracy sanity: mean|cos|={mean_abs_cos_11:.4f} "
            f"(vs 0.7923 OK; bar {DEGENERACY_BAR}).")

        # ---- STEP-2 input: degeneracy gate on {d_i^(20)} ----
        u20 = np.stack([d / float(np.linalg.norm(d)) for d in d20])
        mean_abs_cos_20 = mean_pairwise_abs_cosine(u20)
        log(f"[run] L20 degeneracy: mean|cos|={mean_abs_cos_20:.4f} "
            f"(gate {DEGENERACY_BAR}).")
        if mean_abs_cos_20 >= DEGENERACY_BAR:
            raise Hold(
                f"STEP-2 HALT: L20 direction set degenerate "
                f"(mean|cos|={mean_abs_cos_20:.4f} >= {DEGENERACY_BAR}) — "
                "the L20 contrast failed to separate — HALT per the §2.1 "
                "HOLD path (verdict lane rules Underdetermined). Facts "
                "logged; no sweep on a degenerate direction.")

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
        # ---- item-0 directions (EXP094 precedent; see note at model load) --
        for layer_idx, d0 in ((11, d11[0]), (20, d20[0])):
            res = verify_g5_layer_real(model, tokenizer, bench[0]["prompt"],
                                       d0, layer_idx)
            passes[0] += 4  # ref + disabled + clean + injected
            if passes[0] > HARD_CAP_PASSES:
                raise RunInvalid("budget FAIL: hard cap exceeded — "
                                 "RUN-INVALID.")
            log(f"[run] G5 layer-{layer_idx} execution probe: PASS "
                f"(rel_err={res['criterion_i_rel_err']:.2e}, "
                f"other={res['criterion_ii_max_abs_change']:.2e}).")

        # ---- STEP-1 delivery probe on the six injected cells ----
        # (11,Joint) duplicates (11,L11-only); (20,Joint) duplicates
        # (20,L20-only) — the Joint arm injects the same per-layer vectors.
        lo, hi = G5_BAND
        cell_ratios = {
            (11, "L11"): [float(np.linalg.norm(d11[i]) / h11_norms[i])
                          for i in range(N_ITEMS)],
            (20, "L20"): [float(np.linalg.norm(d20[i]) / h20_norms[i])
                          for i in range(N_ITEMS)],
            (11, "J"): [float(np.linalg.norm(d11[i]) / h11_norms[i])
                        for i in range(N_ITEMS)],
            (20, "J"): [float(np.linalg.norm(d20[i]) / h20_norms[i])
                        for i in range(N_ITEMS)],
            (11, "W"): [float(np.linalg.norm(g11[i]) / h11_norms[i])
                        for i in range(N_ITEMS)],
            (20, "W"): [float(np.linalg.norm(g20[i]) / h20_norms[i])
                        for i in range(N_ITEMS)],
        }
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
        log(f"[run] STEP-1 delivery: 360/360 cell-rows computed; "
            f"{360 - n_oob}/360 in band [{lo}, {hi}]; exclusions: "
            + ", ".join(f"{c}={len(v)}" for c, v in excluded.items()) + ".")
        # Arm masks: an arm's contrasts use the intersection of its cells.
        mask = {
            "L11": np.array([i not in excluded[(11, "L11")]
                             for i in range(N_ITEMS)]),
            "L20": np.array([i not in excluded[(20, "L20")]
                             for i in range(N_ITEMS)]),
            "J": np.array([i not in excluded[(11, "J")] and
                           i not in excluded[(20, "J")]
                           for i in range(N_ITEMS)]),
            "W": np.array([i not in excluded[(11, "W")] and
                           i not in excluded[(20, "W")]
                           for i in range(N_ITEMS)]),
        }

        # ---- The sweep ----
        hook11 = LayerInjectionHook(layer_index=11, alpha=1.0)
        hook20 = LayerInjectionHook(layer_index=20, alpha=1.0)

        def single_pass(ids, layer_idx, vec):
            hook = hook11 if layer_idx == 11 else hook20
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
            return lg

        def joint_pass(ids, v11, v20, capture_realized):
            """Co-injection in one forward pass. If capture_realized, a
            capture hook registered BEFORE the L20 injection hook records
            the pre-injection (L11-perturbed) L20 residual for the
            realized-ratio diagnostic."""
            cap_pre = LayerCapture(model, 20) if capture_realized else None
            hook11.attach(model, v11)
            hook20.attach(model, v20)
            hook11.enable()
            hook20.enable()
            try:
                ids_t = torch.tensor([ids], dtype=torch.long)
                with torch.no_grad():
                    lg = model(ids_t).logits[0].detach().cpu().to(
                        torch.float64).numpy()
                h20_pre = (cap_pre.captured[-1, :].copy()
                           if cap_pre is not None else None)
            finally:
                hook11.detach()
                hook20.detach()
                if cap_pre is not None:
                    cap_pre.remove()
            passes[0] += 1
            if passes[0] > HARD_CAP_PASSES:
                raise RunInvalid("budget FAIL: hard cap exceeded — "
                                 "RUN-INVALID.")
            return lg, h20_pre

        margins = {}
        realized_J, realized_W = [], []
        # L11-only (60)
        m = np.full(N_ITEMS, np.nan)
        for i in range(N_ITEMS):
            lg = single_pass(prompts[i], 11, d11[i])
            a_id, c_id = opt_ids[i]
            m[i] = float(lg[-1, a_id] - lg[-1, c_id])
        margins["L11"] = m
        log("[run] sweep L11-only: 60/60 passes complete.")
        # L20-only (60)
        m = np.full(N_ITEMS, np.nan)
        for i in range(N_ITEMS):
            lg = single_pass(prompts[i], 20, d20[i])
            a_id, c_id = opt_ids[i]
            m[i] = float(lg[-1, a_id] - lg[-1, c_id])
        margins["L20"] = m
        log("[run] sweep L20-only: 60/60 passes complete.")
        # Joint (60) — co-injection, one pass per item
        m = np.full(N_ITEMS, np.nan)
        for i in range(N_ITEMS):
            lg, h20_pre = joint_pass(prompts[i], d11[i], d20[i],
                                     capture_realized=True)
            a_id, c_id = opt_ids[i]
            m[i] = float(lg[-1, a_id] - lg[-1, c_id])
            realized_J.append(float(np.linalg.norm(d20[i]) /
                                    np.linalg.norm(h20_pre)))
        margins["J"] = m
        log("[run] sweep Joint: 60/60 co-injection passes complete.")
        # W-joint (60) — co-injection of the norm-tied random pair
        m = np.full(N_ITEMS, np.nan)
        for i in range(N_ITEMS):
            lg, h20_pre = joint_pass(prompts[i], g11[i], g20[i],
                                     capture_realized=True)
            a_id, c_id = opt_ids[i]
            m[i] = float(lg[-1, a_id] - lg[-1, c_id])
            realized_W.append(float(np.linalg.norm(g20[i]) /
                                    np.linalg.norm(h20_pre)))
        margins["W"] = m
        log("[run] sweep W-joint: 60/60 co-injection passes complete.")
        log(f"[run] sweep complete. Total passes: {passes[0]} "
            f"(expected {EXPECTED_PASSES}, cap {HARD_CAP_PASSES}).")
    finally:
        cap11.remove()
        cap20.remove()

    # Δθ=0 (post)
    post = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if post != pin.WEIGHTS_PIN:
        raise RunInvalid("Δθ=0 FAIL (post): state_dict changed — RUN-INVALID.")
    log("[run] Δθ=0 post-run hash OK (Δθ=0 verified).")

    # ---- Mechanical scoring (no verdict) ----
    table, sec = score098.score_all(
        mB, margins["L11"], margins["L20"], margins["J"], margins["W"],
        phrasing, mask["L11"], mask["L20"], mask["J"], mask["W"])
    log(f"[run] scoring complete: {len(table)} stratum cells "
        f"(3 strata x 5 contrasts).")

    # ---- Regime routing (machine-written, §3 step 3) ----
    w_flips = sec["flips_vs_B"]["W"]
    j_flips = sec["flips_vs_B"]["J"]
    if w_flips >= 1:
        route, why = "LIVE", f"W-joint flips = {w_flips} >= 1"
    elif j_flips == 0:
        route, why = ("FROZEN",
                      "W-joint = 0 and joint = 0 (delivery confirmed)")
    else:
        route, why = ("LIVE",
                      f"W-joint = 0 with joint = {j_flips} >= 1 "
                      "(asymmetric liveness rule)")
    routing = {
        "routing": route,
        "routing_reason": why,
        "evidence": {
            "W_joint_flips_vs_B": w_flips,
            "joint_flips_vs_B": j_flips,
            "delivery_confirmed": True,
            "tie_counts": sec["tie_counts"],
            "tie_gate_arms": sec["tie_gate_arms"],
            "zero_variance": sec["zero_variance"],
            "coherence_arms": sec["coherence_arms"],
            "n_included": sec["n_included"],
        },
    }
    log(f"[run] regime routing: {route} ({why}).")

    # ---- Margin-shift ledger (§2.5; descriptive only) ----
    dm = {k: margins[k] - mB for k in ("L11", "L20", "J", "W")}
    dm_add = dm["L11"] + dm["L20"]
    dm_int = dm["J"] - dm_add
    nm_L11 = np.array([nearly_moved(dm["L11"][i], mB[i])
                       for i in range(N_ITEMS)])
    nm_L20 = np.array([nearly_moved(dm["L20"][i], mB[i])
                       for i in range(N_ITEMS)])
    cB = mB > 0.0
    cJ = margins["J"] > 0.0
    jmask = mask["J"]
    ledger = []
    for i in range(N_ITEMS):
        joint_flip = bool(cJ[i] != cB[i]) and bool(jmask[i])
        if joint_flip:
            cls = ("additive-explained" if (nm_L11[i] or nm_L20[i])
                   else "interaction-candidate")
        else:
            cls = "no-joint-flip"
        ledger.append({
            "item": i,
            "item_id": item_ids[i],
            "stratum": phrasing[i],
            "dM_11": float(dm["L11"][i]),
            "dM_20": float(dm["L20"][i]),
            "dM_joint": float(dm["J"][i]),
            "dM_W": float(dm["W"][i]),
            "dM_add": float(dm_add[i]),
            "dM_int": float(dm_int[i]),
            "nearly_moved_L11": bool(nm_L11[i]),
            "nearly_moved_L20": bool(nm_L20[i]),
            "joint_flip_vs_B": joint_flip,
            "joint_flip_class": cls,
            "excluded_J": bool(not jmask[i]),
            "excluded_W": bool(not mask["W"][i]),
        })
    n_add = sum(1 for r in ledger if r["joint_flip_class"] == "additive-explained")
    n_int = sum(1 for r in ledger
                if r["joint_flip_class"] == "interaction-candidate")
    log(f"[run] margin-shift ledger: {len(ledger)} rows; joint-flip classes "
        f"among included items: additive-explained={n_add}, "
        f"interaction-candidate={n_int}.")

    # ---- Persist (§5 instrumentation spec, append-only) ----
    arm_names = {"B": "B", "L11": "L11-only", "L20": "L20-only",
                 "J": "Joint", "W": "W-joint"}
    with open(os.path.join(out_dir, "per_item_records.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "stratum", "arm", "correct_top1", "margin",
                    "margin_shift_vs_B"])
        all_m = {"B": mB, **margins}
        for key in ("B", "L11", "L20", "J", "W"):
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
                    "norm_target", "in_band", "excluded_from_contrasts"])
        arm_of = {"L11": "L11-only", "L20": "L20-only", "J": "Joint",
                  "W": "W-joint"}
        for (layer, akey), ratios in cell_ratios.items():
            src = {"L11": d11, "L20": d20, "J": (d11 if layer == 11 else d20),
                   "W": (g11 if layer == 11 else g20)}[akey]
            for i, iid in enumerate(item_ids):
                nt = float(np.linalg.norm(src[i]))
                w.writerow([iid, arm_of[akey], layer, f"{ratios[i]:.10f}",
                            f"{nt:.10f}",
                            "y" if lo <= ratios[i] <= hi else "n",
                            "y" if i in excluded[(layer, akey)] else "n"])

    ctor_manifest = {
        "constructor_sha256": CONSTRUCTOR_PIN,
        "constructor_sha256_live": sha256_file(
            os.path.join(EXP094_DIR, "constructor.py")),
        "P0_sha256": manifest["P0_sha256"],
        "NORM_RATIO": C.NORM_RATIO,
        "RATIO": RATIO,
        "G5_BAND": list(G5_BAND),
        "R_SEED": C.R_SEED,
        "g7_carryover": "EXP094 constructor_manifest.json (audit PASS)",
        "L11_direction_note": "frozen C-1 on L11 residuals (Pass A vs P0)",
        "L20_direction_note": "IDENTICAL C-1 procedure on L20 residuals "
                              "(Pass A vs P0); anchored to BASELINE L20 "
                              "norms; not a transported L11 vector",
        "W_draw_order": "item-major: per item i in 0..59, draw z_i^(11) "
                        "then z_i^(20) from the single R_SEED stream; each "
                        "normalized and per-layer norm-tied to the Joint "
                        "arm's component",
        "norm_tie_assertions": "120/120 pass (||g_i^(L)|| == ||d_i^(L)||)",
        "L20_degeneracy": {
            "mean_pairwise_abs_cosine": mean_abs_cos_20,
            "bar": DEGENERACY_BAR,
            "gate_fired": bool(mean_abs_cos_20 >= DEGENERACY_BAR),
        },
        "L11_degeneracy_sanity": {
            "archived_ref": DEGENERACY_SANITY_REF,
            "recomputed": mean_abs_cos_11,
            "tol": DEGENERACY_SANITY_TOL,
            "pass": True,
        },
        "per_item": [
            {"item": i, "item_id": item_ids[i],
             "d11_norm": float(np.linalg.norm(d11[i])),
             "d20_norm": float(np.linalg.norm(d20[i])),
             "g11_norm": float(np.linalg.norm(g11[i])),
             "g20_norm": float(np.linalg.norm(g20[i])),
             "h11_norm_B": h11_norms[i],
             "h20_norm_B": h20_norms[i]}
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
        "seeds": {"R_SEED": C.R_SEED, "G5_probe_seed": 31337},
        "single_environment_F5": "all passes in this environment; "
                                 "no mid-run rebuild",
        "n_passes": passes[0],
        "expected_passes": EXPECTED_PASSES,
        "hard_cap": HARD_CAP_PASSES,
    }
    with open(os.path.join(out_dir, "env_manifest.json"), "w") as f:
        json.dump(env_manifest, f, indent=2)

    with open(os.path.join(out_dir, "delivery_probe_log.json"), "w") as f:
        json.dump({
            "band": list(G5_BAND),
            "n_cell_rows": 360,
            "in_band": 360 - n_oob,
            "out_of_band": n_oob,
            "exclusions": {f"({c[0]},{c[1]})": v
                           for c, v in excluded.items()},
            "per_cell_ratios": {
                f"({c[0]},{c[1]})": [round(x, 10) for x in cell_ratios[c]]
                for c in INJECTED_CELLS},
            "L20_realized_vs_perturbed_norm": {
                "joint": [round(x, 10) for x in realized_J],
                "W_joint": [round(x, 10) for x in realized_W],
                "note": "diagnostic only (§0.1): ||d_i^(20)|| / "
                        "||h_i^(20, L11-perturbed, pre-injection)||_2",
            },
        }, f, indent=2)

    with open(os.path.join(out_dir, "regime_routing.json"), "w") as f:
        json.dump(routing, f, indent=2)

    with open(os.path.join(out_dir, "stratum_table.json"), "w") as f:
        json.dump(table, f, indent=2)

    with open(os.path.join(out_dir, "margin_shift_ledger.json"), "w") as f:
        json.dump({"rows": ledger,
                   "additive_explained": n_add,
                   "interaction_candidate": n_int,
                   "note": "descriptive only (§2.5); alters no verdict"},
                  f, indent=2)

    # Mechanical read-out (UNINTERPRETED — verdict lane walks §3 steps 4-8).
    readout = {"status": "UNINTERPRETED_MECHANICAL_READOUT",
               "experiment": "EXP098"}
    agg = {c: table[f"agg__{c}"] for c in
           ("JB", "L11B", "L20B", "WB", "JW")}
    readout["routing"] = routing["routing"]
    readout["n_correct"] = sec["n_correct"]
    readout["flips_vs_B"] = sec["flips_vs_B"]
    readout["flips_J_vs_W"] = sec["flips_J_vs_W"]
    readout["delta_M"] = {c: agg[c]["delta"] for c in agg}
    readout["mcnemar"] = {c: {"b": agg[c]["mcnemar_b"],
                              "c": agg[c]["mcnemar_c"],
                              "p": agg[c]["mcnemar_p"]} for c in agg}
    readout["strata"] = {
        s: {c: {"delta": table[f"{s}__{c}"]["delta"],
                "b": table[f"{s}__{c}"]["mcnemar_b"],
                "c": table[f"{s}__{c}"]["mcnemar_c"],
                "p": table[f"{s}__{c}"]["mcnemar_p"]}
            for c in ("JB", "L11B", "L20B", "WB")} for s in ("agg", "A", "C")}
    readout["decision_worksheet_steps_0_2"] = [
        {"step": 0, "condition": "foundation gates",
         "evidence": {
             "constructor_rehash": "match frozen pin",
             "G5_layer_11": "PASS (frozen verify_g5 core, d_0^(11) probe)",
             "G5_layer_20": "PASS (frozen verify_g5 core, d_0^(20) probe)",
             "B_agreement": "60/60 per-item vs archived EXP094 baseline",
             "L11_degeneracy_sanity": "within 0.05 of 0.7923"}},
        {"step": 1, "condition": "delivery (360 cell-rows in band)",
         "evidence": {"in_band": 360 - n_oob,
                      "exclusions": {f"({c[0]},{c[1]})": v
                                     for c, v in excluded.items()}}},
        {"step": 2, "condition": "degeneracy gate input (L20)",
         "evidence": {"mean_abs_cosine_20": mean_abs_cos_20,
                      "bar": DEGENERACY_BAR,
                      "gate_fired": bool(mean_abs_cos_20 >= DEGENERACY_BAR)}},
        {"step": 3, "condition": "regime routing (machine-written)",
         "evidence": routing},
        {"step": "4-8", "condition": "VERDICT LANE (not executor)",
         "evidence": "contrast statistics in stratum_table.json; "
                     "decomposition inputs in margin_shift_ledger.json"},
    ]
    with open(os.path.join(out_dir, "mechanical_readout.json"), "w") as f:
        json.dump(readout, f, indent=2)

    artifact_hashes = {}
    for fname in ("per_item_records.csv", "per_layer_delivery.csv",
                  "constructor_manifest.json", "env_manifest.json",
                  "delivery_probe_log.json", "regime_routing.json",
                  "stratum_table.json", "margin_shift_ledger.json",
                  "mechanical_readout.json"):
        artifact_hashes[fname] = sha256_file(os.path.join(out_dir, fname))
    with open(os.path.join(out_dir, "artifact_hashes.txt"), "w") as f:
        for k, v in artifact_hashes.items():
            f.write(f"{v}  {k}\n")

    report = {
        "experiment": "EXP098",
        "mode": "real",
        "layers": list(LAYERS),
        "ratio": RATIO,
        "exclusions": {f"({c[0]},{c[1]})": v for c, v in excluded.items()},
        "routing": routing["routing"],
        "guards": {
            "G0": "pass (bench pin)",
            "G1'": "pass (real-tokenizer cover re-executed)",
            "Δθ=0": "pass (pre/post LOG-331 hash)",
            "G7": f"pass (constructor {CONSTRUCTOR_PIN[:16]}…, audit PASS)",
            "G5-L11": "pass (frozen verify_g5 core, d_0^(11) execution probe)",
            "G5-L20": "pass (frozen verify_g5 core, d_0^(20) execution probe)",
            "STEP-0": "pass (60/60 B agreement; L11 sanity OK)",
            "STEP-1": f"{360 - n_oob}/360 in band",
            "STEP-2": f"L20 mean|cos|={mean_abs_cos_20:.4f} "
                      f"(bar {DEGENERACY_BAR})",
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
    ap = argparse.ArgumentParser(description="EXP098 executor")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ceo-clearance", action="store_true")
    ap.add_argument("--snapshot", default=None)
    args = ap.parse_args(argv)

    if not args.ceo_clearance:
        print("REFUSAL: real execution requires --ceo-clearance (LOG-4421).",
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
        with open(os.path.join(args.out_dir, "exp098_run_log.txt"), "w") as f:
            f.write("\n".join(log_lines) + "\n")
        print(f"HOLD: {e}", file=sys.stderr)
        return 4
    except (RunInvalid, InjectRunInvalid, score098.RunInvalid) as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    with open(os.path.join(args.out_dir, "exp098_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(args.out_dir, "exp098_run_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print("[run] EXP098 records complete (UNINTERPRETED — verdict lane next).")
    print(f"[run] report: {os.path.join(args.out_dir, 'exp098_report.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
