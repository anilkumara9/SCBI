"""EXP096 executor — S5-4 headroom-gated injection of the killed per-item L11 direction.

Signed pre-reg: research/innovation/S5-4_PREREG_DRAFT_v2_2026-09-28.md
(binding SIGN: LOG-4404 Law #14 delta re-verification; CEO execution
clearance: LOG-4405; S5-4 minted as EXP096). This executor follows the signed
protocol EXACTLY; any deviation is a STOP + new experiment number.

Design (signed pre-reg §2):
  Single strength alpha=8.0 on the frozen gated set G (|G|=21 — the 21
  EXP092-B items with |m_i^B| <= tau_8 = 0.90, Appendix A, frozen).
  Arms: B (all 60 items), T(8.0) = per-item task direction d_i at norm
        8*0.0474*||h_i^B||_2 = 0.3792*||h_i^B||_2 (gated items only),
        B_wrong(8.0) = per-item isotropic random g_i (EXP094's frozen R-arm
        constructor, pinned seed -> identical {g_i}) scaled to norm 8*||d_i||
        (gated items only).
  Budget: 162 passes expected (60 B + 60 Ref + 21 T + 21 B_wrong), hard cap 400.

Binding execution order (signed pre-reg §3):
  0. Foundation gates FIRST: constructor re-hash vs pin; B agreement vs
     archived EXP094 B vector (60/60 required); gate-manifest reproduction
     (recomputed G from the pinned archive must equal Appendix A exactly,
     member-for-member); degeneracy sanity vs 0.7923. ANY failure -> HOLD,
     never silent re-run.
  1. Delivery probe on the 42 gated injection rows: perturbation_ratio within
     [0.2844, 0.4740]; <=2 rows out of band -> excluded from all contrasts;
     >2 rows out of band, or any zero-norm d_i -> HOLD + diagnose.
  2. Degeneracy gate input on regenerated {d_i} (mean|cos| < 0.95 to proceed).
  Sweep: frozen routing — T/B_wrong exactly on Appendix A, paired vs B.
  In-run reach verification (§2.4): realized max|shift(8.0)| over gated T rows
  vs the 1.125 under-coverage tripwire and the 0.45 over-coverage tripwire.

This executor is MECHANICAL ONLY: it produces records + an UNINTERPRETED
read-out. It does NOT walk the §3 decision table (steps 3-6 = verdict lane).

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


pin = _load_module("exp096_protocol_pin",
                   os.path.join(EXP093_DIR, "protocol_pin.py"))
import reference_implementation as ref
import g1prime
from inject import TorchInjectionHook, RunInvalid as InjectRunInvalid
from test_g7_audit import sha256_file

score096 = _load_module("exp096_scorer",
                        os.path.join(BUNDLE_DIR, "score_exp096.py"))

FORBIDDEN_FLAGS = (
    "--train", "--training", "--finetune", "--fine-tune", "--lr",
    "--learning-rate", "--gpu", "--cuda", "--gpus",
    "--mutate-weights", "--update-weights",
)

N_ITEMS = 60
LAYER_INDEX = 11
ALPHA = 8.0
# §2.2 G5-style band (±25% around 8*0.0474 = 0.3792).
G5_BAND = (0.2844, 0.4740)
G5_MAX_EXCLUDED = 2  # <=2 rows out of band -> excluded; >2 -> HOLD.
# §2.4 in-run reach-verification tripwires (pre-registered).
TAU_8 = 0.90
REACH_UNDER_TRIP = 1.125   # = 1.25 * tau_8
REACH_OVER_TRIP = 0.45     # = 0.5 * tau_8
DEGENERACY_BAR = 0.95
DEGENERACY_SANITY_REF = 0.7923   # EXP094's archived value
DEGENERACY_SANITY_TOL = 0.05
HARD_CAP_PASSES = 400
EXPECTED_PASSES = 162  # 60 B + 60 Ref + 21 T(8.0) + 21 B_wrong(8.0)

CONSTRUCTOR_PIN = ("5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa"
                   "81917f361")
ARCHIVED_CSV = os.path.join(EXP094_DIR, "out", "per_item_records.csv")
ARCHIVED_CSV_PIN = ("9ada6ef9d489aee959b56160053cbe7bdb7024e6c593cbf3a9ffbfd9b366d149")

# Frozen Appendix A member list (§2.1.1; |G|=21; 13 A-first / 8 C-first;
# 5 wrong / 16 right at baseline). Recomputed-G must equal this exactly.
APPENDIX_A = [
    "exp092_elemental_2hop_0",
    "exp092_elemental_2hop_10",
    "exp092_elemental_2hop_11",
    "exp092_elemental_2hop_2",
    "exp092_elemental_2hop_5",
    "exp092_elemental_2hop_9",
    "exp092_elemental_3hop_0",
    "exp092_elemental_3hop_1",
    "exp092_elemental_3hop_11",
    "exp092_elemental_3hop_13",
    "exp092_elemental_3hop_3",
    "exp092_planetary_2hop_0",
    "exp092_planetary_2hop_1",
    "exp092_planetary_2hop_12",
    "exp092_planetary_2hop_13",
    "exp092_planetary_2hop_2",
    "exp092_planetary_2hop_8",
    "exp092_planetary_2hop_9",
    "exp092_planetary_3hop_0",
    "exp092_planetary_3hop_10",
    "exp092_planetary_3hop_7",
]


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


def guard_gate_recompute():
    """§3 step-0(iii): recompute G from the PINNED archive; must equal
    Appendix A exactly (member-for-member)."""
    live = sha256_file(ARCHIVED_CSV)
    if live != ARCHIVED_CSV_PIN:
        raise Hold(
            f"STEP-0 HOLD: EXP094 archive hash {live[:16]}… != frozen pin "
            f"{ARCHIVED_CSV_PIN[:16]}… — archive drift — HOLD "
            "(re-verify archive SHA-256, never silent re-gating).")
    margins_B = {}
    with open(ARCHIVED_CSV, newline="") as f:
        for row in csv.DictReader(f):
            if row["arm"] == "B":
                margins_B[row["item_id"]] = float(row["margin"])
    if len(margins_B) != N_ITEMS:
        raise Hold(
            f"STEP-0 HOLD: archived B vector has {len(margins_B)} items, "
            f"expected {N_ITEMS} — cannot run the gate-manifest gate — HOLD.")
    recomputed = sorted(i for i, m in margins_B.items() if abs(m) <= TAU_8)
    if recomputed != sorted(APPENDIX_A):
        missing = sorted(set(APPENDIX_A) - set(recomputed))
        extra = sorted(set(recomputed) - set(APPENDIX_A))
        raise Hold(
            f"STEP-0 HOLD: recomputed gate ({len(recomputed)} items) != "
            f"Appendix A ({len(APPENDIX_A)} items) — missing={missing} "
            f"extra={extra} — HOLD (archive drift; never a silent re-gate).")
    return margins_B


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


def run_real(bench, manifest, archived_margins_B, snapshot, log, out_dir):
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
    id_to_idx = {iid: i for i, iid in enumerate(item_ids)}

    # Frozen gated index set (Appendix A order = injection order).
    gated_idx = [id_to_idx[iid] for iid in APPENDIX_A]
    assert len(gated_idx) == 21 and len(set(gated_idx)) == 21
    log(f"[run] gated set: 21 items (Appendix A order); "
        f"A-first={sum(1 for i in gated_idx if phrasing[i]=='A-first')}, "
        f"C-first={sum(1 for i in gated_idx if phrasing[i]=='C-first')}.")

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
        # ---- B arm (all 60 items; doubles as constructor Pass A) ----
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

        # ---- Reference passes (constructor Pass B: P0 + prompt) ----
        for i in range(N_ITEMS):
            logits = forward_ids(p0_ids + prompts[i])
            b_vecs.append(cap.captured[-1, :].copy())
        log("[run] reference passes complete: 60 passes.")

        # ---- Construction (frozen C-1) at alpha=8.0 + R-arm (pinned seed) ----
        rng = np.random.default_rng(C.R_SEED)
        d8_vecs, g_vecs, ctor_rows = [], [], []
        for i in range(N_ITEMS):
            d, info = C.build_per_item_direction(
                a_vecs[i], b_vecs[i], h_norms[i],
                ratio=ALPHA * C.NORM_RATIO)
            if info["degenerate_zero"]:
                raise Hold(
                    f"STEP-1 HOLD (F7): zero-norm d_{i} — common-cause "
                    "delivery failure — HOLD + diagnose.")
            d8_vecs.append(d)
            g_vecs.append(C.build_random_direction(info["d_norm"],
                                                   d.shape[0], rng))
            ctor_rows.append({
                "item": i,
                "item_id": item_ids[i],
                "r_norm": info["r_norm"],
                "degenerate_zero": info["degenerate_zero"],
                "d_norm_alpha8": info["d_norm"],
                "perturbation_ratio_alpha8": info["perturbation_ratio"],
            })
        log(f"[run] construction complete: 60 d_i at alpha=8.0, 60 g_i "
            f"(R seed {C.R_SEED}).")

        # Norm-tie assertion (protocol §2.1: B_wrong norm targets T(8.0)'s
        # per-item norm). Fails loud — the delivery probe is the backstop.
        for i in gated_idx:
            nt = float(np.linalg.norm(d8_vecs[i]))
            nw = float(np.linalg.norm(g_vecs[i]))
            if abs(nt - nw) > 1e-9 * max(nt, 1e-300):
                raise Hold(
                    f"STEP-1 HOLD: norm-tie broken on gated item {i}: "
                    f"||T||={nt:.6f} vs ||B_wrong||={nw:.6f} — HOLD + "
                    "diagnose.")
        log("[run] norm-tie check: ||B_wrong_i|| == ||T(8.0)_i|| on all 21 "
            "gated items.")

        # ---- STEP-0(iv): degeneracy gate input + sanity vs EXP094's 0.7923 --
        norms = np.array([r["d_norm_alpha8"] for r in ctor_rows])
        unit = np.stack([d / n for d, n in zip(d8_vecs, norms)])
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
            "archived EXP094 baseline.")

        # ---- STEP-1 delivery probe on the 42 gated injection rows ----
        lo, hi = G5_BAND
        ratios_T, ratios_W = [], []
        for i in gated_idx:
            ratios_T.append(float(np.linalg.norm(d8_vecs[i]) / h_norms[i]))
            # g_i norm == d_norm_alpha8 (targets T(8.0)'s per-item norm).
            ratios_W.append(float(np.linalg.norm(g_vecs[i]) / h_norms[i]))
        out_of_band = [k for k, r in enumerate(ratios_T + ratios_W)
                       if not (lo <= r <= hi)]
        log(f"[run] STEP-1 delivery: 42/42 ratios computed; "
            f"{42 - len(out_of_band)}/42 in [{lo}, {hi}].")
        if len(out_of_band) > G5_MAX_EXCLUDED:
            raise Hold(
                f"STEP-1 HOLD: {len(out_of_band)} gated rows out of band "
                f"(>{G5_MAX_EXCLUDED}) — common-cause suspected — HOLD "
                "+ diagnose.")
        excluded_g = sorted(out_of_band)
        if excluded_g:
            log(f"[run] STEP-1: {len(excluded_g)} gated rows excluded from "
                f"all contrasts (indices {excluded_g}).")
        live_g = [k for k in range(21) if k not in excluded_g]

        # ---- The sweep: T(8.0), B_wrong(8.0) on gated items ----
        # B_wrong norm targets T(8.0)'s per-item norm: g_i already has
        # norm d_norm_alpha8 (== ||T(8.0)_i||), so it is injected AS-IS
        # (no extra alpha scaling — that was the diagnosed double-scale bug).
        mT = np.full(21, np.nan)
        mW = np.full(21, np.nan)
        for k, i in enumerate(gated_idx):
            if k in excluded_g:
                continue
            lg = inject_pass(prompts[i], d8_vecs[i])
            a_id, c_id = opt_ids[i]
            mT[k] = float(lg[-1, a_id] - lg[-1, c_id])
        log(f"[run] sweep T(8.0): {len(live_g)}/21 gated passes complete.")
        for k, i in enumerate(gated_idx):
            if k in excluded_g:
                continue
            lg = inject_pass(prompts[i], g_vecs[i])
            a_id, c_id = opt_ids[i]
            mW[k] = float(lg[-1, a_id] - lg[-1, c_id])
        log(f"[run] sweep B_wrong(8.0): {len(live_g)}/21 gated passes "
            "complete.")
        log(f"[run] sweep complete. Total passes: {passes[0]} "
            f"(expected {EXPECTED_PASSES}, cap {HARD_CAP_PASSES}).")

        # ---- §2.4 in-run reach verification ----
        mB_g = mB[gated_idx]
        shift_T = mT - mB_g
        realized_reach = float(np.nanmax(np.abs(shift_T)))
        under = realized_reach > REACH_UNDER_TRIP
        over = realized_reach < REACH_OVER_TRIP
        log(f"[run] reach verification: realized max|shift(8.0)|="
            f"{realized_reach:.4f} vs under-trip {REACH_UNDER_TRIP} "
            f"({'TRIPPED — under-coverage disclosed' if under else 'ok'}) / "
            f"over-trip {REACH_OVER_TRIP} "
            f"({'TRIPPED — KILL carries low-margin-items fence' if over else 'ok'}).")
    finally:
        cap.remove()
        inj.detach()

    # Δθ=0 (post)
    post = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if post != pin.WEIGHTS_PIN:
        raise RunInvalid("Δθ=0 FAIL (post): state_dict changed — RUN-INVALID.")
    log("[run] Δθ=0 post-run hash OK (Δθ=0 verified).")

    # ---- Scoring over the gated set (mechanical; tie gate on 42 rows) ----
    phrasing_g = [phrasing[i] for i in gated_idx]
    try:
        table_27, sec = score096.score_gated(mB[gated_idx], mT, mW,
                                             phrasing_g)
    except score096.RunInvalid as e:
        log(f"[run] {e} — no verdict licensed on any contrast.")
        raise
    log(f"[run] scoring complete: 27 cells; ties={sec['tie_count']}/42 "
        f"(rate {sec['tie_rate']:.3f}).")

    # ---- Persist (§5 instrumentation spec, append-only) ----
    csv_path = os.path.join(out_dir, "per_item_records.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "stratum", "arm", "gate_member",
                    "correct_top1", "margin", "perturbation_ratio",
                    "margin_shift_vs_B"])
        for i, iid in enumerate(item_ids):
            gm = "y" if iid in APPENDIX_A else "n"
            w.writerow([iid, phrasing[i], "B", gm, int(mB[i] > 0.0),
                        f"{mB[i]:.10f}", "0.0000000000", "0.0000000000"])
        for k, i in enumerate(gated_idx):
            iid = item_ids[i]
            w.writerow([iid, phrasing[i], "T(8.0)", "y",
                        int(mT[k] > 0.0), f"{mT[k]:.10f}",
                        f"{ratios_T[k]:.10f}",
                        f"{(mT[k] - mB_g[k]):.10f}"])
            w.writerow([iid, phrasing[i], "B_wrong(8.0)", "y",
                        int(mW[k] > 0.0), f"{mW[k]:.10f}",
                        f"{ratios_W[k]:.10f}",
                        f"{(mW[k] - mB_g[k]):.10f}"])
    log(f"[run] per-item CSV written: {csv_path} "
        f"({60 + 2 * 21} rows).")

    gate_manifest = {
        "tau_8": TAU_8,
        "tau_8_derivation": "2 * 0.4488 (nearest-anchor extrapolation of the "
                            "measured reach scaling law, protocol §0.1)",
        "archive_sha256": ARCHIVED_CSV_PIN,
        "archive_sha256_live": sha256_file(ARCHIVED_CSV),
        "appendix_A": APPENDIX_A,
        "recomputed_gate": sorted(APPENDIX_A),
        "gate_agreement": "21/21 member-for-member vs Appendix A",
        "baseline_composition": {
            "A_first": sum(1 for i in gated_idx
                           if phrasing[i] == "A-first"),
            "C_first": sum(1 for i in gated_idx
                           if phrasing[i] == "C-first"),
        },
    }
    with open(os.path.join(out_dir, "gate_manifest.json"), "w") as f:
        json.dump(gate_manifest, f, indent=2)

    ctor_run = {
        "constructor_sha256": CONSTRUCTOR_PIN,
        "constructor_sha256_live": sha256_file(
            os.path.join(EXP094_DIR, "constructor.py")),
        "P0_sha256": manifest["P0_sha256"],
        "NORM_RATIO": C.NORM_RATIO,
        "ALPHA": ALPHA,
        "RATIO_ALPHA8": ALPHA * C.NORM_RATIO,
        "R_SEED": C.R_SEED,
        "g7_carryover": "EXP094 constructor_manifest.json (audit PASS)",
        "per_item": [
            {"item": i, "item_id": item_ids[i],
             "gate_member": item_ids[i] in APPENDIX_A,
             "d_norm_alpha8": float(np.linalg.norm(d8_vecs[i])),
             "g_norm_alpha8": float(np.linalg.norm(g_vecs[i])),
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
        "n_passes": passes[0],
        "expected_passes": EXPECTED_PASSES,
        "hard_cap": HARD_CAP_PASSES,
    }
    with open(os.path.join(out_dir, "env_manifest.json"), "w") as f:
        json.dump(env_manifest, f, indent=2)

    reach_log = {
        "realized_max_abs_shift_alpha8": realized_reach,
        "under_coverage_tripwire": REACH_UNDER_TRIP,
        "under_coverage_tripped": under,
        "over_coverage_tripwire": REACH_OVER_TRIP,
        "over_coverage_tripped": over,
        "routing": ("under-coverage: KILL reported with under-coverage "
                    "disclosed + flips on the tau=1.125 superset as "
                    "non-decision diagnostic"
                    if under else
                    "over-coverage: step-3 KILL carries the "
                    "'low-margin-items form' fence inline"
                    if over else
                    "no tripwire fired: reach as calibrated"),
    }
    with open(os.path.join(out_dir, "delivery_probe_log.json"), "w") as f:
        json.dump({
            "band": list(G5_BAND),
            "n_gated_rows": 42,
            "in_band": 42 - len(out_of_band),
            "out_of_band": len(out_of_band),
            "excluded_gated_indices": excluded_g,
            "per_row_ratios_T": ratios_T,
            "per_row_ratios_W": ratios_W,
            "reach_verification": reach_log,
        }, f, indent=2)

    with open(os.path.join(out_dir, "stratum_table_27.json"), "w") as f:
        json.dump(table_27, f, indent=2)

    # Mechanical read-out (UNINTERPRETED — verdict lane walks §3 steps 3-6).
    tb = table_27["agg__TB"]
    wb = table_27["agg__WB"]
    readout = {
        "status": "UNINTERPRETED_MECHANICAL_READOUT",
        "alpha": ALPHA,
        "n_correct": {"B_gated": sec["n_B_correct"],
                      "T": sec["n_T_correct"],
                      "B_wrong": sec["n_W_correct"]},
        "flips_vs_B": {"T": tb["mcnemar_b"] + tb["mcnemar_c"],
                       "B_wrong": wb["mcnemar_b"] + wb["mcnemar_c"]},
        "delta_M": {"T": tb["delta"], "B_wrong": wb["delta"]},
        "mcnemar_T_vs_B": {"b": tb["mcnemar_b"], "c": tb["mcnemar_c"],
                           "p": tb["mcnemar_p"]},
        "mcnemar_W_vs_B": {"b": wb["mcnemar_b"], "c": wb["mcnemar_c"],
                           "p": wb["mcnemar_p"]},
        "flip_ledger_TB": sec["flip_ledger_TB"],
        "flip_ledger_WB": sec["flip_ledger_WB"],
        "ties": sec["tie_count"],
        "reach_verification": reach_log,
        "strata": {k: {"T_delta": v["delta"],
                       "T_b": v["mcnemar_b"], "T_c": v["mcnemar_c"],
                       "T_p": v["mcnemar_p"]}
                  for k, v in table_27.items() if k.endswith("__TB")},
    }
    worksheet = [
        {"step": 0, "condition": "foundation gates",
         "evidence": {
             "constructor_rehash": "match frozen pin",
             "B_agreement": "60/60 per-item vs archived EXP094 baseline",
             "gate_manifest": "21/21 member-for-member vs Appendix A",
             "degeneracy_sanity": "within 0.05 of 0.7923"}},
        {"step": 1, "condition": "delivery (42 gated rows in band)",
         "evidence": {"in_band": 42 - len(out_of_band),
                      "excluded": excluded_g}},
        {"step": 2, "condition": "degeneracy gate input",
         "evidence": {"mean_abs_cosine": mean_abs_cos,
                      "bar": DEGENERACY_BAR}},
        {"step": "reach", "condition": "in-run reach verification",
         "evidence": reach_log},
        {"step": "3-6", "condition": "VERDICT LANE (not executor)",
         "evidence": "gated contrast statistics in stratum_table_27.json"},
    ]
    readout["decision_worksheet_steps_0_2"] = worksheet
    with open(os.path.join(out_dir, "mechanical_readout.json"), "w") as f:
        json.dump(readout, f, indent=2)

    report = {
        "experiment": "EXP096",
        "mode": "real",
        "layer": LAYER_INDEX,
        "alpha": ALPHA,
        "gate": {"tau_8": TAU_8, "n": 21, "agreement": "21/21"},
        "excluded_gated_indices": excluded_g,
        "reach": reach_log,
        "guards": {
            "G0": "pass (bench pin)",
            "G1'": "pass (real-tokenizer cover re-executed)",
            "Δθ=0": "pass (pre/post LOG-331 hash)",
            "G7": f"pass (constructor {CONSTRUCTOR_PIN[:16]}…, audit PASS)",
            "STEP-0": "pass (60/60 B agreement; gate 21/21; sanity OK)",
            "STEP-1": f"{42 - len(out_of_band)}/42 in band "
                      f"({len(excluded_g)} excluded)",
            "STEP-2": f"mean|cos|={mean_abs_cos:.4f} (sanity vs 0.7923 OK)",
            "reach": reach_log["routing"],
            "thread_pin": n_threads,
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
    ap = argparse.ArgumentParser(description="EXP096 executor")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ceo-clearance", action="store_true")
    ap.add_argument("--snapshot", default=None)
    ap.add_argument("--manifest", default=None)
    args = ap.parse_args(argv)

    if not args.ceo_clearance:
        print("REFUSAL: real execution requires --ceo-clearance (LOG-4405).",
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
        # §3 step-0(iii): gate-manifest reproduction BEFORE bench/model.
        archived_margins_B = guard_gate_recompute()
        log("[g0] gate-manifest pass: recomputed G == Appendix A (21/21, "
            "member-for-member); archive hash matches frozen pin.")
        bench, g0 = guard_g0_bench()
        log(f"[g0] G0 pass: bench pin {g0['pin'][:16]}…, 60 items.")
        report, _ = run_real(bench, manifest, archived_margins_B,
                             args.snapshot or pin.SNAPSHOT_DIR, log,
                             args.out_dir)
    except Hold as e:
        with open(os.path.join(args.out_dir, "HOLD.txt"), "w") as f:
            f.write(str(e) + "\n")
        with open(os.path.join(args.out_dir, "exp096_run_log.txt"), "w") as f:
            f.write("\n".join(log_lines) + "\n")
        print(f"HOLD: {e}", file=sys.stderr)
        return 4
    except (RunInvalid, InjectRunInvalid, score096.RunInvalid) as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    with open(os.path.join(args.out_dir, "exp096_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(args.out_dir, "exp096_run_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print("[run] EXP096 records complete (UNINTERPRETED — verdict lane next).")
    print(f"[run] report: {os.path.join(args.out_dir, 'exp096_report.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
