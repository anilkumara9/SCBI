"""EXP097 executor — S6-1 threshold-account breaking point.

Licensed protocol: research/innovation/S6-1_PREREG_DRAFT_v2_2026-09-28.md
(binding Law #14 ACCEPT-WITH-FIXES: LOG-4411; v2 repair: LOG-4412;
independent delta re-verification SIGN: LOG-4413; CEO execution clearance:
LOG-4414; S6-1 minted as EXP097). This executor follows the licensed
protocol EXACTLY; any deviation is a STOP + new experiment number.

Design (licensed protocol §2):
  Two super-license ratios {1.5, 3.0} on the 60 EXP092-B items, UNGATED
  (the threshold account is about push-dominance, not headroom — gating
  would conflate two rescues; protocol §2.2).
  Arms: B (60 items, single run), T(1.5)/T(3.0) = per-item task direction
        d_i scaled to norm ratio*||h_i^B||_2 (executor alpha = ratio/0.0474
        ≈ 31.65 / 63.29; the frozen constructor takes the ratio directly),
        B_wrong(1.5)/B_wrong(3.0) = per-item isotropic random direction g_i
        (EXP094's frozen R-arm constructor, pinned seed R_SEED -> one draw
        per item, identical {g_i} across ratios) scaled to norm targeting
        T(ratio)'s per-item norm (norm-tie asserted per item per ratio;
        injected AS-IS — no extra alpha scaling: the diagnosed EXP096
        attempt-1 double-scale bug must not recur).
  Budget: 300 passes (60 B + 120 T + 120 B_wrong) + 60 Ref + 90 reserve =
          390 expected; 600 HARD CAP (not waivable).

Binding execution order (licensed protocol §3):
  0. Foundation gates FIRST: constructor re-hash vs pin; B-arm zero-variance
     check (bench broke -> HOLD); per-item B-decision agreement vs archived
     EXP094 B vector (60/60 required); degeneracy sanity vs 0.7923.
     ANY failure -> HOLD, never silent re-run.
  1. Delivery probe on the 240 injection rows: per (ratio, arm),
     perturbation_ratio within the §2.2 band ([1.125, 1.875] /
     [2.25, 3.75]); <=2 rows out of band -> those items excluded from that
     arm's contrasts; >2 rows out of band, or any zero-norm d_i -> HOLD +
     diagnose.
  2. Degeneracy gate input on regenerated {d_i} (mean|cos| < 0.95 to
     proceed; verdict lane).
  Per-ratio regime routing (machine-written, §5 item 5): RUN-INVALID_r if
  the coherence gate (zero-variance injection-arm decisions) or tie gate
  (ties/180 > 5%) fires; else FROZEN_r if B_wrong flips = 0 AND T flips = 0
  (delivery confirmed); else LIVE_r (incl. the asymmetric B_wrong=0/T>=1
  case). Routing is recorded, never walked into a verdict here.
  Steps 3-7 = VERDICT LANE (separate). This executor is MECHANICAL ONLY.

F5 (binding, Law #14): ALL passes in ONE pinned environment — no mid-run
rebuilds; the env manifest attests it; a change voids the run (Law #13).

Exit codes: 0 = ran (records verdict-ready); 2 = refused; 3 = RUN-INVALID;
4 = HOLD (foundation guard fired; diagnosis facts logged, never re-run).
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


pin = _load_module("exp097_protocol_pin",
                   os.path.join(EXP093_DIR, "protocol_pin.py"))
import reference_implementation as ref
import g1prime
from inject import TorchInjectionHook, RunInvalid as InjectRunInvalid
from test_g7_audit import sha256_file

score097 = _load_module("exp097_scorer",
                        os.path.join(BUNDLE_DIR, "score_exp097.py"))

FORBIDDEN_FLAGS = (
    "--train", "--training", "--finetune", "--fine-tune", "--lr",
    "--learning-rate", "--gpu", "--cuda", "--gpus",
    "--mutate-weights", "--update-weights",
)

N_ITEMS = 60
LAYER_INDEX = 11
RATIOS = {"1.5": 1.5, "3.0": 3.0}
# §2.2 G5-style bands (±25% around each ratio).
G5_BANDS = {"1.5": (1.125, 1.875), "3.0": (2.25, 3.75)}
G5_MAX_EXCLUDED = 2  # <=2 rows out of band -> excluded; >2 -> HOLD.
DEGENERACY_BAR = 0.95
DEGENERACY_SANITY_REF = 0.7923   # EXP094's archived value
DEGENERACY_SANITY_TOL = 0.05
TIE_DENOMINATOR = 180  # 60 items x 3 arms per ratio
TIE_RATE_BAR = 0.05
HARD_CAP_PASSES = 600
EXPECTED_PASSES = 390  # 300 (60 B + 120 T + 120 B_wrong) + 90 reserve
MODEL_PASSES_PLANNED = 360  # 60 B + 60 Ref + 240 injection

CONSTRUCTOR_PIN = ("5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa"
                   "81917f361")
ARCHIVED_CSV = os.path.join(EXP094_DIR, "out", "per_item_records.csv")
ARCHIVED_CSV_PIN = ("9ada6ef9d489aee959b56160053cbe7bdb7024e6c593cbf3a9ffbfd9b366d149")


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
            f"{CONSTRUCTOR_PIN[:16]}… — the foundation is not EXP094's — "
            "HOLD (diagnose, never proceed).")
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


class CaptureHook:
    def __init__(self, model):
        layer, self.path = TorchInjectionHook.resolve_module(model)
        self.captured = None

        def _cap(module, inputs, output):
            out = output[0] if isinstance(output, tuple) else output
            import torch
            self.captured = out[0].detach().cpu().to(
                torch.float64).numpy()

        self._handle = layer.register_forward_hook(_cap)

    def remove(self):
        self._handle.remove()


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
            f"{N_ITEMS} — cannot run the per-item agreement gate — HOLD.")
    return out


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

    cap = CaptureHook(model)
    inj = TorchInjectionHook(alpha=1.0)

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

    def inject_pass(ids, vec):
        ids_t = torch.tensor([ids], dtype=torch.long)
        inj.attach(model, vec)
        inj.enable()
        try:
            with torch.no_grad():
                lg = model(ids_t).logits[0].detach().cpu().to(
                    torch.float64).numpy()
        finally:
            inj.detach()
        passes[0] += 1
        if passes[0] > HARD_CAP_PASSES:
            raise RunInvalid("budget FAIL: hard cap exceeded — RUN-INVALID.")
        return lg

    a_vecs, b_vecs, h_norms = [], [], []
    mB = np.zeros(N_ITEMS)
    prompts = []
    try:
        # ---- B arm (60 items; doubles as constructor Pass A) ----
        for i, b in enumerate(bench):
            ids = tokenizer.encode(b["prompt"], add_special_tokens=False)
            prompts.append(ids)
            logits = forward_ids(ids)
            resid = cap.captured
            a_vecs.append(resid[-1, :].copy())
            h_norms.append(float(np.linalg.norm(resid[-1, :])))
            a_id, c_id = opt_ids[i]
            mB[i] = float(logits[-1, a_id] - logits[-1, c_id])
        log(f"[run] B arm complete: 60 passes; B accuracy "
            f"{int((mB > 0).sum())}/60.")

        # B-arm zero-variance -> the bench itself broke -> HOLD.
        if bool((mB == mB[0]).all()):
            raise Hold(
                "STEP-0 HOLD: B-arm decisions zero-variance across all 60 "
                "items — the bench itself broke — HOLD + diagnose.")

        # ---- Reference passes (constructor Pass B: P0 + prompt) ----
        for i in range(N_ITEMS):
            logits = forward_ids(p0_ids + prompts[i])
            b_vecs.append(cap.captured[-1, :].copy())
        log("[run] reference passes complete: 60 passes.")

        # ---- Construction (frozen C-1) at ratios 1.5 and 3.0 ----
        # One isotropic draw per item (item order 0..59 — same draw sequence
        # as EXP094/095/096's R-arm), unit-normalized, then scaled to each
        # ratio's T norm. The {g_i} directions are thus identical across
        # ratios (protocol §2.1: "per-item random direction g_i ...
        # identical {g_i}"), differing only in norm.
        dim = a_vecs[0].shape[0]
        rng = np.random.default_rng(C.R_SEED)
        d_vecs = {"1.5": [], "3.0": []}
        g_vecs = {"1.5": [], "3.0": []}
        ctor_rows = []
        for i in range(N_ITEMS):
            infos = {}
            for rlabel, ratio in RATIOS.items():
                d, info = C.build_per_item_direction(
                    a_vecs[i], b_vecs[i], h_norms[i], ratio=ratio)
                if info["degenerate_zero"]:
                    raise Hold(
                        f"STEP-1 HOLD (F7): zero-norm d_{i} at ratio "
                        f"{rlabel} — common-cause delivery failure — HOLD "
                        "+ diagnose.")
                d_vecs[rlabel].append(d)
                infos[rlabel] = info
            z = np.asarray(rng.normal(size=dim), dtype=np.float64)
            z_norm = float(np.linalg.norm(z))
            if z_norm == 0.0:
                raise Hold("STEP-1 HOLD: isotropic draw exactly zero.")
            z = z / z_norm
            for rlabel in RATIOS:
                g_vecs[rlabel].append(
                    z * float(np.linalg.norm(d_vecs[rlabel][i])))
            ctor_rows.append({
                "item": i,
                "item_id": item_ids[i],
                "r_norm": infos["1.5"]["r_norm"],
                "degenerate_zero": False,
                "d_norm_r15": infos["1.5"]["d_norm"],
                "d_norm_r30": infos["3.0"]["d_norm"],
                "perturbation_ratio_r15": infos["1.5"]["perturbation_ratio"],
                "perturbation_ratio_r30": infos["3.0"]["perturbation_ratio"],
            })
        log(f"[run] construction complete: 60 d_i at ratio 1.5, 60 at 3.0; "
            f"60 g_i unit directions (R seed {C.R_SEED}), scaled per ratio.")

        # Norm-tie assertion (protocol §2.1: B_wrong norm targets T(ratio)'s
        # per-item norm). Fails loud — the delivery probe is the backstop.
        # This is the EXP096 attempt-1 lesson: g_i is injected AS-IS.
        for rlabel in RATIOS:
            for i in range(N_ITEMS):
                nt = float(np.linalg.norm(d_vecs[rlabel][i]))
                nw = float(np.linalg.norm(g_vecs[rlabel][i]))
                if abs(nt - nw) > 1e-9 * max(nt, 1e-300):
                    raise Hold(
                        f"STEP-1 HOLD: norm-tie broken on item {i} at ratio "
                        f"{rlabel}: ||T||={nt:.6f} vs ||B_wrong||={nw:.6f} — "
                        "HOLD + diagnose.")
        log("[run] norm-tie check: ||B_wrong_i(r)|| == ||T_i(r)|| on all "
            "60 items x 2 ratios.")

        # ---- STEP-0(iv): degeneracy gate input + sanity vs EXP094's 0.7923 --
        # The unit task directions u_i are ratio-independent (d = u*r*||h||),
        # so the degeneracy input is computed once.
        norms15 = np.array([r["d_norm_r15"] for r in ctor_rows])
        unit = np.stack([d / n for d, n in zip(d_vecs["1.5"], norms15)])
        mean_abs_cos = mean_pairwise_abs_cosine(unit)
        if abs(mean_abs_cos - DEGENERACY_SANITY_REF) > DEGENERACY_SANITY_TOL:
            raise Hold(
                f"STEP-0 HOLD: regenerated mean|cos|={mean_abs_cos:.4f} vs "
                f"archived {DEGENERACY_SANITY_REF} (tol {DEGENERACY_SANITY_TOL})"
                " — constructor regeneration broken — HOLD + diagnose.")
        log(f"[run] degeneracy: mean|cos|={mean_abs_cos:.4f} "
            f"(sanity vs 0.7923 OK; bar {DEGENERACY_BAR}).")
        if mean_abs_cos >= DEGENERACY_BAR:
            log(f"[run] STEP-2: mean|cos| >= {DEGENERACY_BAR} — "
                "Underdetermined (verdict lane).")

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
                f"{len(disagreements)} items (e.g. {disagreements[:5]}) vs "
                "archived EXP094 baseline — HOLD + diagnose (re-hash "
                "weights, verify thread pinning, byte-compare prompts).")
        log("[run] STEP-0 B agreement: 60/60 per-item decisions match the "
            "archived EXP094 baseline (determinism self-check OK).")

        # ---- STEP-1 delivery probe on the 240 injection rows ----
        # Per (ratio, arm): <=2 rows out of band -> excluded from that arm's
        # contrasts; >2 -> HOLD.
        ratios_probe = {}  # (rlabel, arm) -> list of 60 ratios
        for rlabel, ratio in RATIOS.items():
            lo, hi = G5_BANDS[rlabel]
            rT = [float(np.linalg.norm(d_vecs[rlabel][i]) / h_norms[i])
                  for i in range(N_ITEMS)]
            rW = [float(np.linalg.norm(g_vecs[rlabel][i]) / h_norms[i])
                  for i in range(N_ITEMS)]
            ratios_probe[(rlabel, "T")] = (rT, lo, hi)
            ratios_probe[(rlabel, "W")] = (rW, lo, hi)
        excluded = {}  # (rlabel, arm) -> sorted list of item indices
        for (rlabel, arm), (rvals, lo, hi) in ratios_probe.items():
            oob = sorted(k for k, r in enumerate(rvals) if not (lo <= r <= hi))
            if len(oob) > G5_MAX_EXCLUDED:
                raise Hold(
                    f"STEP-1 HOLD: {len(oob)} rows out of band on "
                    f"({rlabel}, {arm}) (>{G5_MAX_EXCLUDED}) — common-cause "
                    "suspected — HOLD + diagnose.")
            excluded[(rlabel, arm)] = oob
        n_oob = sum(len(v) for v in excluded.values())
        log(f"[run] STEP-1 delivery: 240/240 ratios computed; "
            f"{240 - n_oob}/240 in band; exclusions per (ratio, arm): "
            + ", ".join(f"{k}={len(v)}" for k, v in excluded.items()) + ".")
        mask_T = {r: np.array([i not in excluded[(r, "T")]
                               for i in range(N_ITEMS)])
                  for r in RATIOS}
        mask_W = {r: np.array([i not in excluded[(r, "W")]
                               for i in range(N_ITEMS)])
                  for r in RATIOS}

        # ---- The sweep: T(1.5), T(3.0), B_wrong(1.5), B_wrong(3.0) ----
        # Vectors carry their full target norms already (constructor ratio
        # parameter); injected AS-IS — no extra scaling (EXP096 lesson).
        margins = {}
        for rlabel in RATIOS:
            for arm, vecs in (("T", d_vecs[rlabel]),
                              ("B_wrong", g_vecs[rlabel])):
                m = np.full(N_ITEMS, np.nan)
                for i in range(N_ITEMS):
                    lg = inject_pass(prompts[i], vecs[i])
                    a_id, c_id = opt_ids[i]
                    m[i] = float(lg[-1, a_id] - lg[-1, c_id])
                margins[(rlabel, arm)] = m
                log(f"[run] sweep {arm}({rlabel}): 60/60 passes complete.")
        log(f"[run] sweep complete. Total passes: {passes[0]} "
            f"(planned {MODEL_PASSES_PLANNED}, expected {EXPECTED_PASSES}, "
            f"cap {HARD_CAP_PASSES}).")
    finally:
        cap.remove()
        inj.detach()

    # Δθ=0 (post)
    post = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if post != pin.WEIGHTS_PIN:
        raise RunInvalid("Δθ=0 FAIL (post): state_dict changed — RUN-INVALID.")
    log("[run] Δθ=0 post-run hash OK (Δθ=0 verified).")

    # ---- Per-ratio scoring + machine-written regime routing ----
    tables, secs, routing = {}, {}, {}
    for rlabel in RATIOS:
        tbl, sec = score097.score_ratio(
            rlabel, mB, margins[(rlabel, "T")], margins[(rlabel, "B_wrong")],
            phrasing, mask_T[rlabel], mask_W[rlabel])
        tables[rlabel] = tbl
        secs[rlabel] = sec
        if sec["tie_gate_fires"] or sec["coherence_gate_fires"]:
            route = "RUN-INVALID"
            why = ("tie gate" if sec["tie_gate_fires"] else "") + (
                "+coherence gate" if sec["tie_gate_fires"] and
                sec["coherence_gate_fires"] else
                ("coherence gate" if sec["coherence_gate_fires"] else ""))
        elif sec["flips_W_vs_B"] == 0 and sec["flips_T_vs_B"] == 0:
            route = "FROZEN"
            why = "B_wrong=0 and T=0 (delivery confirmed)"
        else:
            route = "LIVE"
            why = ("B_wrong>=1 flip" if sec["flips_W_vs_B"] >= 1 else
                   "T>=1 flip with B_wrong=0 (asymmetric liveness rule)")
        routing[rlabel] = {
            "routing": route,
            "routing_reason": why,
            "evidence": {
                "tie_rate": sec["tie_rate"],
                "tie_count": sec["tie_count"],
                "zero_variance_T": sec["zero_variance_T"],
                "zero_variance_W": sec["zero_variance_W"],
                "flips_T_vs_B": sec["flips_T_vs_B"],
                "flips_W_vs_B": sec["flips_W_vs_B"],
                "delivery_confirmed": True,
                "n_included_T": sec["n_included_T"],
                "n_included_W": sec["n_included_W"],
            },
        }
        log(f"[run] routing ratio {rlabel}: {route} ({why}); "
            f"ties={sec['tie_count']}/180; flips T={sec['flips_T_vs_B']}, "
            f"W={sec['flips_W_vs_B']}.")
    n_cells = sum(len(t) for t in tables.values())
    log(f"[run] scoring complete: {n_cells} stratum cells "
        f"(protocol '54 cells' = 18 contrast cells x 3 stats).")

    # ---- Persist (§5 instrumentation spec, append-only) ----
    csv_path = os.path.join(out_dir, "per_item_records.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "stratum", "ratio", "arm", "correct_top1",
                    "margin", "perturbation_ratio", "margin_shift_vs_B",
                    "delivery_in_band", "excluded_from_contrasts"])
        for i, iid in enumerate(item_ids):
            w.writerow([iid, phrasing[i], "NA", "B", int(mB[i] > 0.0),
                        f"{mB[i]:.10f}", "0.0000000000", "0.0000000000",
                        "NA", "n"])
        for rlabel in RATIOS:
            for arm, akey in (("T", "T"), ("B_wrong", "W")):
                m = margins[(rlabel, arm)]
                rvals, lo, hi = ratios_probe[(rlabel, akey)]
                for i, iid in enumerate(item_ids):
                    in_band = lo <= rvals[i] <= hi
                    w.writerow([iid, phrasing[i], rlabel, arm,
                                int(m[i] > 0.0), f"{m[i]:.10f}",
                                f"{rvals[i]:.10f}",
                                f"{(m[i] - mB[i]):.10f}",
                                "y" if in_band else "n",
                                "y" if i in excluded[(rlabel, akey)] else "n"])
    log(f"[run] per-item CSV written: {csv_path} (300 rows).")

    ctor_run = {
        "constructor_sha256": CONSTRUCTOR_PIN,
        "constructor_sha256_live": sha256_file(
            os.path.join(EXP094_DIR, "constructor.py")),
        "P0_sha256": manifest["P0_sha256"],
        "NORM_RATIO": C.NORM_RATIO,
        "RATIOS": {k: v for k, v in RATIOS.items()},
        "executor_alpha": {k: v / C.NORM_RATIO for k, v in RATIOS.items()},
        "G5_BANDS": {k: list(v) for k, v in G5_BANDS.items()},
        "R_SEED": C.R_SEED,
        "g7_carryover": "EXP094 constructor_manifest.json (audit PASS)",
        "g_direction_note": "one isotropic draw per item (item order 0..59, "
                            "R_SEED) — {g_i} directions identical across "
                            "ratios; norm scaled to T(ratio)'s per-item norm",
        "per_item": [
            {"item": i, "item_id": item_ids[i],
             "d_norm_r15": float(np.linalg.norm(d_vecs["1.5"][i])),
             "d_norm_r30": float(np.linalg.norm(d_vecs["3.0"][i])),
             "g_norm_r15": float(np.linalg.norm(g_vecs["1.5"][i])),
             "g_norm_r30": float(np.linalg.norm(g_vecs["3.0"][i])),
             "h_norm_B": h_norms[i]}
            for i in range(N_ITEMS)],
        "mean_pairwise_abs_cosine": mean_abs_cos,
        "degeneracy_sanity": {
            "archived_ref": DEGENERACY_SANITY_REF,
            "recomputed": mean_abs_cos,
            "tol": DEGENERACY_SANITY_TOL,
            "pass": True,
        },
    }
    with open(os.path.join(out_dir, "constructor_manifest.json"), "w") as f:
        json.dump(ctor_run, f, indent=2)

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
        "seeds": {"R_SEED": C.R_SEED},
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
            "bands": {k: list(v) for k, v in G5_BANDS.items()},
            "n_injection_rows": 240,
            "in_band": 240 - n_oob,
            "out_of_band": n_oob,
            "exclusions": {f"{k[0]}/{k[1]}": v
                           for k, v in excluded.items()},
            "per_row_ratios": {
                f"{r}/{a}": [round(x, 10) for x in ratios_probe[(r, a)][0]]
                for r in RATIOS for a in ("T", "W")},
        }, f, indent=2)

    with open(os.path.join(out_dir, "regime_routing.json"), "w") as f:
        json.dump(routing, f, indent=2)

    stratum_table = {}
    for rlabel in RATIOS:
        for cell, st in tables[rlabel].items():
            stratum_table[f"{cell}__r{rlabel}"] = st
    with open(os.path.join(out_dir, "stratum_table_54.json"), "w") as f:
        json.dump(stratum_table, f, indent=2)

    # Mechanical read-out (UNINTERPRETED — verdict lane walks §3 steps 3-7).
    readout = {"status": "UNINTERPRETED_MECHANICAL_READOUT",
               "experiment": "EXP097", "ratios": {}}
    for rlabel in RATIOS:
        agg_tb = tables[rlabel]["agg__TB"]
        agg_wb = tables[rlabel]["agg__WB"]
        sec = secs[rlabel]
        readout["ratios"][rlabel] = {
            "routing": routing[rlabel]["routing"],
            "n_correct": {"B": sec["n_B_correct"], "T": sec["n_T_correct"],
                          "B_wrong": sec["n_W_correct"]},
            "flips_vs_B": {"T": sec["flips_T_vs_B"],
                           "B_wrong": sec["flips_W_vs_B"]},
            "delta_M": {"T": agg_tb["delta"], "B_wrong": agg_wb["delta"]},
            "mcnemar_T_vs_B": {"b": agg_tb["mcnemar_b"],
                               "c": agg_tb["mcnemar_c"],
                               "p": agg_tb["mcnemar_p"]},
            "mcnemar_W_vs_B": {"b": agg_wb["mcnemar_b"],
                               "c": agg_wb["mcnemar_c"],
                               "p": agg_wb["mcnemar_p"]},
            "flip_ledger_TB": sec["flip_ledger_TB"],
            "flip_ledger_WB": sec["flip_ledger_WB"],
            "ties": sec["tie_count"],
            "strata": {
                s: {"T_delta": tables[rlabel][f"{s}__TB"]["delta"],
                    "T_b": tables[rlabel][f"{s}__TB"]["mcnemar_b"],
                    "T_c": tables[rlabel][f"{s}__TB"]["mcnemar_c"],
                    "T_p": tables[rlabel][f"{s}__TB"]["mcnemar_p"],
                    "W_delta": tables[rlabel][f"{s}__WB"]["delta"]}
                for s in ("agg", "A", "C")},
        }
    worksheet = [
        {"step": 0, "condition": "foundation gates",
         "evidence": {
             "constructor_rehash": "match frozen pin",
             "B_agreement": "60/60 per-item vs archived EXP094 baseline",
             "degeneracy_sanity": "within 0.05 of 0.7923"}},
        {"step": 1, "condition": "delivery (240 injection rows in band)",
         "evidence": {"in_band": 240 - n_oob,
                      "exclusions": {f"{k[0]}/{k[1]}": v
                                     for k, v in excluded.items()}}},
        {"step": 2, "condition": "degeneracy gate input",
         "evidence": {"mean_abs_cosine": mean_abs_cos,
                      "bar": DEGENERACY_BAR}},
        {"step": "routing", "condition": "per-ratio regime routing",
         "evidence": routing},
        {"step": "3-7", "condition": "VERDICT LANE (not executor)",
         "evidence": "per-ratio contrast statistics in "
                     "stratum_table_54.json"},
    ]
    readout["decision_worksheet_steps_0_2"] = worksheet
    with open(os.path.join(out_dir, "mechanical_readout.json"), "w") as f:
        json.dump(readout, f, indent=2)

    artifact_hashes = {}
    for fname in ("per_item_records.csv", "constructor_manifest.json",
                  "env_manifest.json", "delivery_probe_log.json",
                  "regime_routing.json", "stratum_table_54.json",
                  "mechanical_readout.json"):
        artifact_hashes[fname] = sha256_file(os.path.join(out_dir, fname))
    with open(os.path.join(out_dir, "artifact_hashes.txt"), "w") as f:
        for k, v in artifact_hashes.items():
            f.write(f"{v}  {k}\n")

    report = {
        "experiment": "EXP097",
        "mode": "real",
        "layer": LAYER_INDEX,
        "ratios": {k: v for k, v in RATIOS.items()},
        "exclusions": {f"{k[0]}/{k[1]}": v for k, v in excluded.items()},
        "routing": {k: v["routing"] for k, v in routing.items()},
        "guards": {
            "G0": "pass (bench pin)",
            "G1'": "pass (real-tokenizer cover re-executed)",
            "Δθ=0": "pass (pre/post LOG-331 hash)",
            "G7": f"pass (constructor {CONSTRUCTOR_PIN[:16]}…, audit PASS)",
            "STEP-0": "pass (60/60 B agreement; sanity OK)",
            "STEP-1": f"{240 - n_oob}/240 in band",
            "STEP-2": f"mean|cos|={mean_abs_cos:.4f} (sanity vs 0.7923 OK)",
            "thread_pin": n_threads,
            "F5": "single environment (no mid-run rebuild)",
        },
        "run_meta": env_manifest,
    }
    return report, log


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for flag in FORBIDDEN_FLAGS:
        if any(a == flag or a.startswith(flag + "=") for a in argv):
            print(f"REFUSAL: forbidden flag {flag}.", file=sys.stderr)
            return 2
    ap = argparse.ArgumentParser(description="EXP097 executor")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ceo-clearance", action="store_true")
    ap.add_argument("--snapshot", default=None)
    args = ap.parse_args(argv)

    if not args.ceo_clearance:
        print("REFUSAL: real execution requires --ceo-clearance (LOG-4414).",
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
        report, _ = run_real(bench, manifest,
                             args.snapshot or pin.SNAPSHOT_DIR, log,
                             args.out_dir)
    except Hold as e:
        with open(os.path.join(args.out_dir, "HOLD.txt"), "w") as f:
            f.write(str(e) + "\n")
        with open(os.path.join(args.out_dir, "exp097_run_log.txt"), "w") as f:
            f.write("\n".join(log_lines) + "\n")
        print(f"HOLD: {e}", file=sys.stderr)
        return 4
    except (RunInvalid, InjectRunInvalid, score097.RunInvalid) as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    with open(os.path.join(args.out_dir, "exp097_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(args.out_dir, "exp097_run_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print("[run] EXP097 records complete (UNINTERPRETED — verdict lane next).")
    print(f"[run] report: {os.path.join(args.out_dir, 'exp097_report.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
