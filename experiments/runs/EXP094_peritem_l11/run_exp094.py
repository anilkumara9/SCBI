"""EXP094 executor — S4-9 per-item layer-11 task-direction causal test.

Signed pre-reg: research/innovation/S4-9_PREREG_DRAFT_2026-09-27.md (binding
SIGN LOG-4371). CEO execution clearance: LOG-4372 (CPU lane only, <0.005
T4-h, $0, Δθ=0). This executor follows the pre-reg EXACTLY; any deviation is
a STOP + new experiment number.

Arms (pre-reg §2.1): B baseline (no injection; doubles as constructor Pass A),
T per-item task direction d_i at matched norm, R norm-matched per-item random
direction g_i (specificity control).

Passes per item (4 x 60 = 240; hard cap 400):
  B:   prompt -> capture L11 residual at readout anchor (a_i, ||h_i^B||) +
       decision margin mB[i].
  Ref: P0 + prompt -> capture L11 residual at readout anchor (b_i).
  T:   prompt, inject d_i at L11 readout anchor -> margin mT[i].
  R:   prompt, inject g_i at L11 readout anchor -> margin mR[i].

Refusal rules:
  - G7.1: constructor.py SHA-256 must equal the frozen manifest hash; the
    manifest must carry g7_verdict == "PASS". Else exit 2.
  - Real execution requires --ceo-clearance (LOG-4372). Else exit 2.
  - Forbidden flags (training/GPU/weight mutation) -> exit 2.
  - Guard failure -> exit 3 (RUN-INVALID).

Guards (pre-reg §4):
  G0 bench pin; Δθ=0 (state-dict hash pre/post == LOG-331 pin);
  G1' real-tokenizer cover re-run (option IDs from offset mapping);
  G7 frozen constructor + audit; G5-style delivery probe (per-item ratio band
  0.0355–0.0593, ≥58/60 PASS + execution probe on item 0); per-item margin
  CSV (Law #13); full-pairing arm routing (§3); N_final feasibility on paper;
  degeneracy gate (mean pairwise |cosine| >= 0.95 -> Underdetermined).

Exit codes: 0 = ran (verdict in report); 2 = refused; 3 = RUN-INVALID.
"""

import argparse
import csv
import hashlib
import json
import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
EXP092_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl")
EXP093_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP093_l11_causal")
sys.path.append(EXP092_DIR)
sys.path.append(EXP093_DIR)

import numpy as np

import constructor as C


def _load_module(name, path):
    """Load a module from an explicit file path (avoids sys.path collisions
    between EXP092_ibl/protocol_pin.py and EXP093_l11_causal/protocol_pin.py)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# EXP093's pins (bench, weights, snapshot, thread pin) — explicit path load.
pin = _load_module("exp093_protocol_pin",
                   os.path.join(EXP093_DIR, "protocol_pin.py"))
import reference_implementation as ref
import g1prime
from inject import TorchInjectionHook, verify_g5_real, RunInvalid as InjectRunInvalid
from score_exp094 import score_experiment, RunInvalid as ScorerRunInvalid
from test_g7_audit import sha256_file

FORBIDDEN_FLAGS = (
    "--train", "--training", "--finetune", "--fine-tune", "--lr",
    "--learning-rate", "--gpu", "--cuda", "--gpus",
    "--mutate-weights", "--update-weights",
)

N_ITEMS = 60
LAYER_INDEX = 11
G5_BAND = (0.0355, 0.0593)   # ±25% around 0.0474 (pre-reg §4)
G5_MIN_ITEMS = 58            # aggregation rule: ≥58/60 in band
DEGENERACY_BAR = 0.95        # pre-reg §4
TIE_RATE_BAR = 0.05
HARD_CAP_PASSES = 400


class RunInvalid(Exception):
    """Guard failure -> RUN-INVALID (withheld, never a verdict)."""


def compute_state_dict_hash(state_dict):
    """SHA-256 over sorted keys, CPU, float32 bytes (EXP077/EXP091/EXP092)."""
    sha = hashlib.sha256()
    for key in sorted(state_dict.keys()):
        sha.update(np.asarray(state_dict[key], dtype=np.float32).tobytes())
    return sha.hexdigest()


def guard_g0_bench():
    bench = ref.build_bench()
    try:
        g0 = ref.verify_g0(bench, pin.BENCH_PIN)
    except ref.BenchInvalid as e:
        raise RunInvalid(f"G0 FAIL: {e} — RUN-INVALID.")
    return bench, g0


def guard_g71_constructor(manifest_path):
    """G7.1: the frozen constructor hash must match; audit must be PASS."""
    if not os.path.isfile(manifest_path):
        raise RunInvalid(
            f"G7.1 FAIL: constructor manifest not found at {manifest_path} — "
            "the constructor is not frozen — RUN-INVALID.")
    manifest = json.load(open(manifest_path))
    ctor_path = os.path.join(BUNDLE_DIR, "constructor.py")
    live = sha256_file(ctor_path)
    if live != manifest["constructor_sha256"]:
        raise RunInvalid(
            f"G7.1 FAIL: constructor.py hash {live[:16]}… != frozen "
            f"{manifest['constructor_sha256'][:16]}… — code changed after "
            "freeze — RUN-INVALID (new experiment number required).")
    if manifest.get("g7_verdict") != "PASS":
        raise RunInvalid(
            f"G7.1 FAIL: constructor audit verdict is "
            f"{manifest.get('g7_verdict')!r}, not PASS — RUN-INVALID.")
    if manifest.get("P0_TEXT") != C.P0_TEXT:
        raise RunInvalid("G7.1 FAIL: P0_TEXT != frozen manifest — RUN-INVALID.")
    return manifest


class CaptureHook:
    """Forward hook capturing the layer-11 post-block residual (read-only)."""

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
    """Degeneracy gate input: mean |cosine| over pairs of unit vectors."""
    U = np.asarray(unit_vecs, dtype=np.float64)
    n = U.shape[0]
    if n < 2:
        return 0.0
    G = U @ U.T
    iu = np.triu_indices(n, k=1)
    return float(np.abs(G[iu]).mean())


def run_real(bench, manifest, snapshot, log, out_dir):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    passes = [0]

    torch.set_num_threads(pin.THREAD_PIN)
    n_threads = torch.get_num_threads()
    if n_threads != pin.THREAD_PIN:
        raise RunInvalid(
            f"thread-pin FAIL: torch intra-op threads = {n_threads} != "
            f"{pin.THREAD_PIN} — RUN-INVALID.")
    log(f"[run] torch intra-op threads pinned: {n_threads}")

    if not os.path.isdir(snapshot):
        raise RunInvalid(f"snapshot directory not found: {snapshot}")
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)

    # G1': real-tokenizer cover BEFORE any weight access; option token IDs
    # from the offset mapping (never bare-word tokenization).
    table = g1prime.verify_g1_prime(tokenizer, bench)
    n_occ = sum(x["occurrences"] for x in table.values())
    log(f"[run] G1' pass: {n_occ}/240 in-prompt occurrences single-token.")
    opt_ids = [(table[b["A"]]["token_id"], table[b["C"]]["token_id"])
               for b in bench]

    model = AutoModelForCausalLM.from_pretrained(
        snapshot, local_files_only=True, torch_dtype=torch.float32,
        device_map="cpu")
    model.eval()
    model.requires_grad_(False)
    log("[run] model.eval(); requires_grad_(False).")

    # Δθ=0 (pre)
    pre = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if pre != pin.WEIGHTS_PIN:
        raise RunInvalid(
            f"Δθ=0 FAIL (pre): state_dict SHA-256 {pre} != LOG-331 "
            f"{pin.WEIGHTS_PIN} — RUN-INVALID.")
    log(f"[run] Δθ=0 pre-run hash OK: {pre[:16]}…")

    p0_ids = tokenizer.encode(C.P0_TEXT, add_special_tokens=False)
    log(f"[run] P0 tokenized: {len(p0_ids)} tokens "
        f"(sha {manifest['P0_sha256'][:16]}…).")

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
                f"budget FAIL: exceeded hard cap {HARD_CAP_PASSES} passes — "
                "RUN-INVALID.")
        return logits

    a_vecs, b_vecs, h_norms = [], [], []
    mB = np.zeros(N_ITEMS)
    try:
        # ---- B arm (baseline; doubles as constructor Pass A) ----
        for i, b in enumerate(bench):
            ids = tokenizer.encode(b["prompt"], add_special_tokens=False)
            logits = forward_ids(ids)
            resid = cap.captured  # (T, D) float64
            a_vecs.append(resid[-1, :].copy())
            h_norms.append(float(np.linalg.norm(resid[-1, :])))
            a_id, c_id = opt_ids[i]
            mB[i] = float(logits[-1, a_id] - logits[-1, c_id])
        n_b = int((mB > 0.0).sum())
        log(f"[run] B arm complete: 60 passes; baseline accuracy "
            f"{n_b}/60 = {n_b/60:.4f} (S2 reference 36/60; reported, "
            f"not gated — pre-reg licenses no baseline gate).")

        # ---- Reference passes (constructor Pass B: P0 + prompt) ----
        for i, b in enumerate(bench):
            ids = tokenizer.encode(b["prompt"], add_special_tokens=False)
            logits = forward_ids(p0_ids + ids)
            resid = cap.captured
            b_vecs.append(resid[-1, :].copy())
        log("[run] reference passes complete: 60 passes.")

        # ---- Construction (frozen C-1) + R-arm sampling ----
        rng = np.random.default_rng(C.R_SEED)
        d_vecs, g_vecs, ctor_rows = [], [], []
        for i in range(N_ITEMS):
            d, info = C.build_per_item_direction(a_vecs[i], b_vecs[i],
                                                 h_norms[i])
            d_vecs.append(d)
            g = C.build_random_direction(info["d_norm"], d.shape[0], rng)
            g_vecs.append(g)
            ctor_rows.append({
                "item": i,
                "r_norm": info["r_norm"],
                "degenerate_zero": info["degenerate_zero"],
                "d_norm": info["d_norm"],
                "perturbation_ratio": info["perturbation_ratio"],
            })
        n_zero = sum(r["degenerate_zero"] for r in ctor_rows)
        log(f"[run] construction complete: 60 d_i, 60 g_i "
            f"(R seed {C.R_SEED}); zero-direction items: {n_zero}.")

        # ---- G5-style delivery probe ----
        # (a) per-item band: ratio in [0.0355, 0.0593], ≥58/60 PASS.
        in_band = [r for r in ctor_rows
                   if G5_BAND[0] <= r["perturbation_ratio"] <= G5_BAND[1]]
        # (b) execution probe on item 0 with d_0 (pre-reg §4 G5-style).
        g5 = verify_g5_real(model, tokenizer, bench[0]["prompt"],
                            d_vecs[0], alpha=1.0)
        passes[0] += 4  # verify_g5_real runs ref + disabled + clean + injected
        delivery_pass = (len(in_band) >= G5_MIN_ITEMS and
                         g5["gate"] == "PASS")
        log(f"[run] G5 probe: per-item band {len(in_band)}/60 in "
            f"[{G5_BAND[0]}, {G5_BAND[1]}] (need ≥{G5_MIN_ITEMS}); "
            f"execution probe rel_err={g5['criterion_i_rel_err']:.2e}, "
            f"other-pos={g5['criterion_ii_max_abs_change']:.2e}, "
            f"bit_match={g5['criterion_iii_bit_match']} -> "
            f"{'PASS' if delivery_pass else 'FAIL'}.")

        # ---- Degeneracy gate input ----
        norms = np.array([r["d_norm"] for r in ctor_rows])
        unit = np.stack([
            d / n if n > 0 else d
            for d, n in zip(d_vecs, norms)])
        mean_abs_cos = mean_pairwise_abs_cosine(unit)
        log(f"[run] degeneracy gate: mean pairwise |cosine| = "
            f"{mean_abs_cos:.4f} (bar {DEGENERACY_BAR}).")

        # ---- T / R arms ----
        mT = np.zeros(N_ITEMS)
        mR = np.zeros(N_ITEMS)
        for i, b in enumerate(bench):
            ids = tokenizer.encode(b["prompt"], add_special_tokens=False)
            ids_t = torch.tensor([ids], dtype=torch.long)
            a_id, c_id = opt_ids[i]
            inj.attach(model, d_vecs[i])
            inj.enable()
            with torch.no_grad():
                lg = model(ids_t).logits[0].detach().cpu().to(
                    torch.float64).numpy()
            passes[0] += 1
            mT[i] = float(lg[-1, a_id] - lg[-1, c_id])
            inj.detach()
            inj.attach(model, g_vecs[i])
            inj.enable()
            with torch.no_grad():
                lg = model(ids_t).logits[0].detach().cpu().to(
                    torch.float64).numpy()
            passes[0] += 1
            mR[i] = float(lg[-1, a_id] - lg[-1, c_id])
            inj.detach()
        log(f"[run] T/R arms complete: 120 passes. Total passes: {passes[0]}.")
    finally:
        cap.remove()
        inj.detach()

    # Δθ=0 (post)
    post = compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if post != pin.WEIGHTS_PIN:
        raise RunInvalid("Δθ=0 FAIL (post): state_dict changed — RUN-INVALID.")
    log(f"[run] Δθ=0 post-run hash OK (Δθ=0 verified).")

    # ---- Persist per-item records (Law #13, pre-reg §5 item 1) ----
    csv_path = os.path.join(out_dir, "per_item_records.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "stratum", "arm", "correct_top1", "margin",
                    "perturbation_ratio", "margin_shift_vs_B"])
        for i, b in enumerate(bench):
            stratum = b["phrasing"]
            row = ctor_rows[i]
            for arm, m, dm, ratio in (
                    ("B", mB[i], 0.0, 0.0),
                    ("T", mT[i], mT[i] - mB[i], row["perturbation_ratio"]),
                    ("R", mR[i], mR[i] - mB[i], row["perturbation_ratio"])):
                w.writerow([b["id"], stratum, arm, int(m > 0.0),
                            f"{m:.10f}", f"{ratio:.10f}", f"{dm:.10f}"])
    log(f"[run] per-item CSV written: {csv_path} (180 rows).")

    with open(os.path.join(out_dir, "constructor_manifest_run.json"),
              "w") as f:
        json.dump({"frozen_manifest": manifest, "per_item": ctor_rows,
                   "g5_band": list(G5_BAND), "g5_n_in_band": len(in_band),
                   "g5_execution": g5, "delivery_pass": delivery_pass,
                   "mean_pairwise_abs_cosine": mean_abs_cos}, f, indent=2)

    phrasing = [b["phrasing"] for b in bench]
    report = score_experiment(mB, mT, mR, phrasing, delivery_pass,
                              mean_abs_cosine)
    report["mode"] = "real"
    report["guards"] = {
        "G0": "pass (bench pin)",
        "G1'": "pass (real-tokenizer cover re-executed)",
        "Δθ=0": "pass (pre/post LOG-331 hash)",
        "G7": f"pass (constructor {manifest['constructor_sha256'][:16]}…, "
               "audit PASS)",
        "G5": f"{'pass' if delivery_pass else 'FAIL'} "
               f"({len(in_band)}/60 in band; execution probe "
               f"{g5['gate']})",
        "thread_pin": n_threads,
    }
    report["run_meta"] = {
        "mode": "real",
        "layer": LAYER_INDEX,
        "n_passes": passes[0],
        "constructor_sha256": manifest["constructor_sha256"],
        "bench_pin": pin.BENCH_PIN,
        "weights_pin": pin.WEIGHTS_PIN,
        "P0_sha256": manifest["P0_sha256"],
        "R_SEED": C.R_SEED,
    }
    return report, log


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for flag in FORBIDDEN_FLAGS:
        if any(a == flag or a.startswith(flag + "=") for a in argv):
            print(f"REFUSAL: forbidden flag {flag}.", file=sys.stderr)
            return 2
    ap = argparse.ArgumentParser(description="EXP094 executor")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--ceo-clearance", action="store_true")
    ap.add_argument("--snapshot", default=None)
    ap.add_argument("--manifest", default=None,
                    help="constructor manifest path "
                         "(default: <bundle>/constructor_manifest.json)")
    args = ap.parse_args(argv)

    if not args.mock and not args.ceo_clearance:
        print("REFUSAL: real execution requires --ceo-clearance (LOG-4372). "
              "Use --mock for synthetic tests.", file=sys.stderr)
        return 2

    os.makedirs(args.out_dir, exist_ok=True)
    manifest_path = (args.manifest or
                     os.path.join(BUNDLE_DIR, "constructor_manifest.json"))
    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print(msg, flush=True)

    try:
        # G7.1 FIRST: frozen constructor + audit PASS — before any guard,
        # before any weight access.
        manifest = guard_g71_constructor(manifest_path)
        log(f"[g7] G7.1 pass: constructor {manifest['constructor_sha256'][:16]}… "
            f"frozen, audit PASS.")
        bench, g0 = guard_g0_bench()
        log(f"[g0] G0 pass: bench pin {g0['pin'][:16]}…, 60 items.")
        if args.mock:
            print("MOCK mode is not implemented in this executor: use "
                  "test_exp094_mock.py for synthetic pipeline tests. Real "
                  "execution requires --ceo-clearance.", file=sys.stderr)
            return 2
        report, _ = run_real(bench, manifest,
                             args.snapshot or pin.SNAPSHOT_DIR, log,
                             args.out_dir)
    except (RunInvalid, InjectRunInvalid, ScorerRunInvalid) as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    out_path = os.path.join(args.out_dir, "exp094_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(args.out_dir, "exp094_run_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    agg = report["stratum_table"]["agg__TB"]
    print(f"[run] ΔM_T={agg['delta']:+.4f} "
          f"T-vs-R p={report['stratum_table']['agg__TR']['mcnemar_p']:.4g}")
    print(f"[run] AUTHORITATIVE VERDICT: {report['verdict']} "
          f"(decision step {report['decision_step']})")
    print(f"[run] report: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
