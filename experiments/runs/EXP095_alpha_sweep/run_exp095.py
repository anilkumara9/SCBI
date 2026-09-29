"""EXP095 executor — S5-1 alpha-sweep dose-response on the killed per-item L11 direction.

Signed pre-reg: research/innovation/S5-1_PREREG_DRAFT_v2_2026-09-28.md
(binding SIGN: LOG-4397 Law #14 delta re-verification; CEO execution
clearance: LOG-4398; S5-1 minted as EXP095). This executor follows the signed
protocol EXACTLY; any deviation is a STOP + new experiment number.

Design (signed pre-reg §2):
  Grid: alpha in {0.25, 0.5, 1.0, 2.0, 4.0} on the 60 EXP092-B items.
  Arms: B (single baseline run per item), T(alpha) = per-item task direction
        d_i at norm alpha*0.0474*||h_i^B||_2, B_wrong(alpha) = per-item
        isotropic random g_i (EXP094's frozen R-arm constructor, pinned seed
        -> identical {g_i}) at norm alpha*||d_i||_2.
  Budget: 724 passes expected (660 injection + 60 construction Ref + 4 G5
        execution probe), 150 reserve, 1300 HARD CAP.

Binding execution order (signed pre-reg §3):
  0. Replication gate FIRST: constructor re-hash vs pin; regenerate {d_i},
     {g_i}; B agreement vs archived EXP094 baseline (per-item; aggregate
     fallback if archived absent); T(1.0) flip count with foundation-wobble
     flag. ANY foundation wobble -> HOLD, never silent re-run.
  1. Delivery probe per (alpha,i): perturbation_ratio within §2.2 bands;
     >=58/60 per alpha or that alpha excluded; common-cause -> HOLD.
  2. Degeneracy gate input on regenerated {d_i} (+ sanity vs 0.7923).
  Sweep: full within-(alpha,item) pairing; tie gate per alpha (>5%/180 ->
     that alpha RUN-INVALID).

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


pin = _load_module("exp095_protocol_pin",
                   os.path.join(EXP093_DIR, "protocol_pin.py"))
import reference_implementation as ref
import g1prime
from inject import TorchInjectionHook, verify_g5_real, RunInvalid as InjectRunInvalid
from test_g7_audit import sha256_file

score095 = _load_module("exp095_scorer",
                        os.path.join(BUNDLE_DIR, "score_exp095.py"))

FORBIDDEN_FLAGS = (
    "--train", "--training", "--finetune", "--fine-tune", "--lr",
    "--learning-rate", "--gpu", "--cuda", "--gpus",
    "--mutate-weights", "--update-weights",
)

N_ITEMS = 60
LAYER_INDEX = 11
ALPHAS = (0.25, 0.5, 1.0, 2.0, 4.0)
# §2.2 G5-style per-alpha bands (±25% around alpha*0.0474).
G5_BANDS = {
    0.25: (0.00889, 0.01481),
    0.5: (0.01778, 0.02963),
    1.0: (0.0355, 0.0593),
    2.0: (0.0711, 0.1185),
    4.0: (0.1422, 0.2370),
}
G5_MIN_ITEMS = 58
DEGENERACY_BAR = 0.95
DEGENERACY_SANITY_REF = 0.7923   # EXP094's archived value
DEGENERACY_SANITY_TOL = 0.05
HARD_CAP_PASSES = 1300
EXPECTED_PASSES = 724  # 60 B + 60 Ref + 60 T(1.0) + 240 T + 300 B_wrong + 4 G5

CONSTRUCTOR_PIN = ("5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa"
                   "81917f361")
ARCHIVED_CSV = os.path.join(EXP094_DIR, "out", "per_item_records.csv")
ARCHIVED_MANIFEST = os.path.join(EXP094_DIR, "out",
                                 "constructor_manifest_run.json")


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
        # ---- B arm (single run per item; doubles as constructor Pass A) ----
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

        # ---- Construction (frozen C-1) + R-arm sampling (pinned seed) ----
        rng = np.random.default_rng(C.R_SEED)
        d1_vecs, g_vecs, ctor_rows = [], [], []
        for i in range(N_ITEMS):
            d, info = C.build_per_item_direction(a_vecs[i], b_vecs[i],
                                                 h_norms[i])
            if info["degenerate_zero"]:
                raise Hold(
                    f"STEP-1 HOLD (F7): zero-norm d_{i} — common-cause "
                    "delivery failure — HOLD + diagnose.")
            d1_vecs.append(d)
            g_vecs.append(C.build_random_direction(info["d_norm"],
                                                   d.shape[0], rng))
            ctor_rows.append({
                "item": i,
                "item_id": item_ids[i],
                "r_norm": info["r_norm"],
                "degenerate_zero": info["degenerate_zero"],
                "d_norm": info["d_norm"],
                "perturbation_ratio": info["perturbation_ratio"],
            })
        log("[run] construction complete: 60 d_i, 60 g_i "
            f"(R seed {C.R_SEED}).")

        # ---- Degeneracy gate input + sanity vs EXP094's 0.7923 ----
        norms = np.array([r["d_norm"] for r in ctor_rows])
        unit = np.stack([d / n for d, n in zip(d1_vecs, norms)])
        mean_abs_cos = mean_pairwise_abs_cosine(unit)
        if abs(mean_abs_cos - DEGENERACY_SANITY_REF) > DEGENERACY_SANITY_TOL:
            raise Hold(
                f"STEP-2 HOLD: regenerated mean|cos|={mean_abs_cos:.4f} vs "
                f"archived {DEGENERACY_SANITY_REF} (tol {DEGENERACY_SANITY_TOL})"
                " — constructor regeneration broken — HOLD + diagnose.")
        log(f"[run] degeneracy: mean|cos|={mean_abs_cos:.4f} "
            f"(sanity vs 0.7923 OK; bar {DEGENERACY_BAR}).")

        # ---- STEP-0 replication gate: per-item B agreement ----
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

        # ---- STEP-0: T(1.0) replication ----
        mT1 = np.zeros(N_ITEMS)
        for i in range(N_ITEMS):
            lg = inject_pass(prompts[i], d1_vecs[i])
            a_id, c_id = opt_ids[i]
            mT1[i] = float(lg[-1, a_id] - lg[-1, c_id])
        cB = mB > 0.0
        cT1 = mT1 > 0.0
        flips_T1 = int(((cT1 & ~cB) | (~cT1 & cB)).sum())
        wobble = 0 < flips_T1 < 6
        if flips_T1 >= 6:
            raise Hold(
                f"STEP-0 HOLD: T(1.0)-vs-B flips={flips_T1} >= 6 — EXP094 "
                "non-replication; the kill's foundation is unstable — HOLD.")
        log(f"[run] STEP-0 T(1.0): flips vs B = {flips_T1} "
            f"{'(FOUNDATION-WOBBLE FLAG — disclosed, sweep proceeds)' if wobble else '(clean replication)'}.")

        # ---- G5 execution probe at alpha=1.0, item 0 ----
        g5 = verify_g5_real(model, tokenizer, bench[0]["prompt"],
                            d1_vecs[0], alpha=1.0)
        passes[0] += 4
        log(f"[run] G5 execution probe (a=1.0, item 0): "
            f"rel_err={g5['criterion_i_rel_err']:.2e}, "
            f"other-pos={g5['criterion_ii_max_abs_change']:.2e}, "
            f"bit_match={g5['criterion_iii_bit_match']} -> {g5['gate']}.")

        # ---- STEP-1 delivery probe per alpha (measured ratios) ----
        d_alpha = {}   # alpha -> list of T vectors
        for alpha in ALPHAS:
            vecs = []
            for i in range(N_ITEMS):
                d, info = C.build_per_item_direction(
                    a_vecs[i], b_vecs[i], h_norms[i],
                    ratio=alpha * C.NORM_RATIO)
                vecs.append(d)
            d_alpha[alpha] = vecs
        delivery = {}
        for alpha in ALPHAS:
            lo, hi = G5_BANDS[alpha]
            in_band = 0
            ratios = []
            for i in range(N_ITEMS):
                r = float(np.linalg.norm(d_alpha[alpha][i]) / h_norms[i])
                ratios.append(r)
                if lo <= r <= hi:
                    in_band += 1
            ok = in_band >= G5_MIN_ITEMS
            delivery[alpha] = {"in_band": in_band, "pass": ok,
                               "band": [lo, hi]}
            log(f"[run] STEP-1 delivery a={alpha}: {in_band}/60 in "
                f"[{lo}, {hi}] -> {'PASS' if ok else 'EXCLUDED'}.")
            if not ok:
                # F7: isolated per-alpha failure -> exclude that alpha.
                # A common-cause pattern (all alpha fail) -> HOLD.
                pass
        if all(not delivery[a]["pass"] for a in ALPHAS):
            raise Hold("STEP-1 HOLD (F7): delivery failed at ALL alpha — "
                       "common-cause failure — HOLD + diagnose.")
        live_alphas = [a for a in ALPHAS if delivery[a]["pass"]]

        # ---- The sweep: T(alpha), B_wrong(alpha) ----
        mT = {1.0: mT1}
        mW = {}
        margin_shift_T = {1.0: mT1 - mB}
        margin_shift_W = {}
        for alpha in live_alphas:
            if alpha == 1.0:
                mT_a = mT1
            else:
                mT_a = np.zeros(N_ITEMS)
                for i in range(N_ITEMS):
                    lg = inject_pass(prompts[i], d_alpha[alpha][i])
                    a_id, c_id = opt_ids[i]
                    mT_a[i] = float(lg[-1, a_id] - lg[-1, c_id])
                mT[alpha] = mT_a
                margin_shift_T[alpha] = mT_a - mB
            mW_a = np.zeros(N_ITEMS)
            for i in range(N_ITEMS):
                lg = inject_pass(prompts[i], alpha * g_vecs[i])
                a_id, c_id = opt_ids[i]
                mW_a[i] = float(lg[-1, a_id] - lg[-1, c_id])
            mW[alpha] = mW_a
            margin_shift_W[alpha] = mW_a - mB
            log(f"[run] sweep a={alpha}: T {60 if alpha != 1.0 else 0} + "
                f"B_wrong 60 passes complete.")
        log(f"[run] sweep complete. Total passes: {passes[0]} "
            f"(expected {EXPECTED_PASSES}, cap {HARD_CAP_PASSES}).")
    finally:
        cap.remove()
        inj.detach()

    # Δθ=0 (post)
    post = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if post != pin.WEIGHTS_PIN:
        raise RunInvalid("Δθ=0 FAIL (post): state_dict changed — RUN-INVALID.")
    log("[run] Δθ=0 post-run hash OK (Δθ=0 verified).")

    # ---- Scoring per alpha (mechanical; tie gate per alpha) ----
    stratum_table, secondaries, excluded = {}, {}, []
    for alpha in live_alphas:
        try:
            tbl, sec = score095.score_alpha(mB, mT[alpha], mW[alpha],
                                            phrasing, alpha)
        except score095.RunInvalid as e:
            log(f"[run] {e} — alpha={alpha} excluded from records.")
            excluded.append(alpha)
            continue
        for k, v in tbl.items():
            stratum_table[f"a{alpha}__{k}"] = v
        secondaries[f"a{alpha}"] = sec

    # ---- Persist (§5 instrumentation spec, append-only) ----
    csv_path = os.path.join(out_dir, "per_item_records.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "stratum", "alpha", "arm", "correct_top1",
                    "margin", "perturbation_ratio", "margin_shift_vs_B"])
        for i, iid in enumerate(item_ids):
            w.writerow([iid, phrasing[i], "n/a", "B", int(mB[i] > 0.0),
                        f"{mB[i]:.10f}", "0.0000000000", "0.0000000000"])
            for alpha in live_alphas:
                if alpha in excluded:
                    continue
                rT = float(np.linalg.norm(d_alpha[alpha][i]) / h_norms[i])
                w.writerow([iid, phrasing[i], alpha, "T",
                            int(mT[alpha][i] > 0.0),
                            f"{mT[alpha][i]:.10f}", f"{rT:.10f}",
                            f"{margin_shift_T[alpha][i]:.10f}"])
                rW = float(np.linalg.norm(alpha * g_vecs[i]) / h_norms[i])
                w.writerow([iid, phrasing[i], alpha, "B_wrong",
                            int(mW[alpha][i] > 0.0),
                            f"{mW[alpha][i]:.10f}", f"{rW:.10f}",
                            f"{margin_shift_W[alpha][i]:.10f}"])
    log(f"[run] per-item CSV written: {csv_path}.")

    ctor_run = {
        "constructor_sha256": CONSTRUCTOR_PIN,
        "constructor_sha256_live": sha256_file(
            os.path.join(EXP094_DIR, "constructor.py")),
        "P0_sha256": manifest["P0_sha256"],
        "NORM_RATIO": C.NORM_RATIO,
        "R_SEED": C.R_SEED,
        "g7_carryover": "EXP094 constructor_manifest.json (audit PASS)",
        "per_item": [
            {"item": i, "item_id": item_ids[i],
             "d_norm_alpha1": float(np.linalg.norm(d1_vecs[i])),
             "g_norm_alpha1": float(np.linalg.norm(g_vecs[i])),
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

    with open(os.path.join(out_dir, "delivery_probe_log.json"), "w") as f:
        json.dump({"bands": {str(a): list(G5_BANDS[a]) for a in ALPHAS},
                   "per_alpha": delivery,
                   "live_alphas": live_alphas,
                   "excluded_alphas": excluded,
                   "g5_execution_probe_alpha1": g5}, f, indent=2)

    with open(os.path.join(out_dir, "stratum_table_135.json"), "w") as f:
        json.dump(stratum_table, f, indent=2)

    # Mechanical read-out (UNINTERPRETED — verdict lane walks §3 steps 3-6).
    readout = {"status": "UNINTERPRETED_MECHANICAL_READOUT",
               "per_alpha": {}}
    for alpha in live_alphas:
        if alpha in excluded:
            continue
        sec = secondaries[f"a{alpha}"]
        tb = stratum_table[f"a{alpha}__agg__TB"]
        wb = stratum_table[f"a{alpha}__agg__WB"]
        readout["per_alpha"][str(alpha)] = {
            "n_correct": {"B": sec["n_B_correct"], "T": sec["n_T_correct"],
                          "B_wrong": sec["n_W_correct"]},
            "flips_vs_B": {"T": tb["mcnemar_b"] + tb["mcnemar_c"],
                           "B_wrong": wb["mcnemar_b"] + wb["mcnemar_c"]},
            "delta_M": {"T": tb["delta"], "B_wrong": wb["delta"]},
            "mcnemar_T_vs_B": {"b": tb["mcnemar_b"], "c": tb["mcnemar_c"],
                               "p": tb["mcnemar_p"]},
            "mcnemar_W_vs_B": {"b": wb["mcnemar_b"], "c": wb["mcnemar_c"],
                               "p": wb["mcnemar_p"]},
            "ties": sec["tie_count"],
        }
    worksheet = [
        {"step": 0, "condition": "replication anchor",
         "evidence": {
             "B_agreement": "60/60 per-item vs archived EXP094 baseline",
             "T1_flips_vs_B": flips_T1,
             "foundation_wobble": wobble}},
        {"step": 1, "condition": "delivery per alpha (>=58/60 in band)",
         "evidence": {str(a): delivery[a] for a in ALPHAS}},
        {"step": 2, "condition": "degeneracy gate input + sanity",
         "evidence": {"mean_abs_cosine": mean_abs_cos,
                      "sanity_ref": DEGENERACY_SANITY_REF,
                      "sanity_tol": DEGENERACY_SANITY_TOL}},
        {"step": "3-6", "condition": "VERDICT LANE (not executor)",
         "evidence": "per-alpha contrast statistics in stratum_table_135.json"},
    ]
    readout["decision_worksheet_steps_0_2"] = worksheet
    with open(os.path.join(out_dir, "mechanical_readout.json"), "w") as f:
        json.dump(readout, f, indent=2)

    report = {
        "experiment": "EXP095",
        "mode": "real",
        "layer": LAYER_INDEX,
        "alphas": live_alphas,
        "excluded_alphas": excluded,
        "foundation_wobble": wobble,
        "guards": {
            "G0": "pass (bench pin)",
            "G1'": "pass (real-tokenizer cover re-executed)",
            "Δθ=0": "pass (pre/post LOG-331 hash)",
            "G7": f"pass (constructor {CONSTRUCTOR_PIN[:16]}…, audit PASS)",
            "STEP-0": "pass (60/60 B agreement; T(1.0) replication)",
            "STEP-1": {str(a): ("PASS" if delivery[a]["pass"] else "EXCLUDED")
                       for a in ALPHAS},
            "STEP-2": f"mean|cos|={mean_abs_cos:.4f} (sanity vs 0.7923 OK)",
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
    ap = argparse.ArgumentParser(description="EXP095 executor")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ceo-clearance", action="store_true")
    ap.add_argument("--snapshot", default=None)
    ap.add_argument("--manifest", default=None)
    args = ap.parse_args(argv)

    if not args.ceo_clearance:
        print("REFUSAL: real execution requires --ceo-clearance (LOG-4398).",
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
        with open(os.path.join(args.out_dir, "exp095_run_log.txt"), "w") as f:
            f.write("\n".join(log_lines) + "\n")
        print(f"HOLD: {e}", file=sys.stderr)
        return 4
    except (RunInvalid, InjectRunInvalid, score095.RunInvalid) as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    with open(os.path.join(args.out_dir, "exp095_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(args.out_dir, "exp095_run_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print("[run] EXP095 records complete (UNINTERPRETED — verdict lane next).")
    print(f"[run] report: {os.path.join(args.out_dir, 'exp095_report.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
