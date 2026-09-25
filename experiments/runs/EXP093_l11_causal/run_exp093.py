"""EXP093 runner — Layer-11 Causal Transfer.

Draft: experiments/protocols/EXP093_L11_CAUSAL_PREREG_DRAFT.md (v0.2, UNSIGNED).
Independent Law #14 SIGN: LOG-4342 (bundle build cleared; execution NOT cleared).

Launch chain: draft v0.2 (LOG-4341) → Law #14 SIGN (LOG-4342) → bundle build
(this) → independent bundle review → CEO signing ceremony (SIGNED protocol +
digest stamp) → CEO execution clearance → execution.

Refusal rules:
  - PENDING-SIGNATURE: SIGNED_PROTOCOL_DIGEST is "PENDING-SIGNATURE" until
    the CEO signing ceremony stamps it. REAL execution is refused (exit 2)
    until then. Mock mode is unaffected.
  - Real execution requires --ceo-clearance (EXP092 FIX 1 discipline); the
    check fires before any guard and before any weight access.
  - Forbidden flags (training/GPU/weight mutation) -> exit 2.

Modes:
  --mock           synthetic pipeline (numpy only): synthetic embeddings for
                   G2, MockCausalModel for G5 + the 180-pass decision loop.
                   Never touches weights. For smoke tests and CI.
  --ceo-clearance  REAL execution: frozen LOG-331 snapshot, CPU, read-only.
                   180 forward passes + G5 probe. Refused while unsigned.

Exit codes: 0 = ran (verdict in report); 2 = refused; 3 = RUN-INVALID.

Guards (draft §6):
  G0  bench SHA-256 == BENCH_PIN (byte-identical EXP092-B reuse)
  G1  Δθ=0: state_dict SHA-256 == WEIGHTS_PIN pre- AND post-run
  G1' inherited via bench-pin byte-identity (no new text); in real mode the
      real-tokenizer offset-mapping cover check re-runs (also recovering the
      option token IDs from the offset mapping — never bare-word tokenization)
  G2  direction provenance: .npz (24,60,1024) float32, read-only; label
      vector == bench target sequence; recompute {r_i},{u_i},{v^(-i)} from
      the .npz (no cached directions); assert ||r_i|| > 1e-9 ∀i;
      assert ||v^(-i)|| = 1; R4 not-bit-identical; coherence reported
  G3  mode stamp ∈ {mock, real} on every artifact
  G4  clean baseline reproduces S2: 36/60 correct, mean margin within 1e-4
      of -0.0018 (torch intra-op threads pinned to THREAD_PIN, asserted)
  G5  injection-site verification (probe): (i) rel 1e-6, (ii) abs 1e-9,
      (iii) hook-disabled logits bit-match hook-free reference
"""

import argparse
import hashlib
import json
import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)  # own protocol_pin takes precedence
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
EXP092_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl")
sys.path.append(EXP092_DIR)  # EXP092's reference_implementation + g1prime

import numpy as np

import protocol_pin as pin
import reference_implementation as ref  # EXP092's canonical bench builder
import g1prime                          # EXP092's G1' helper (same BENCH_PIN)
from direction_builder import build_directions
from direction_builder import RunInvalid as BuilderRunInvalid
from inject import (ALPHA, LAYER_INDEX, MockCausalModel, TorchInjectionHook,
                    verify_g5_mock, verify_g5_real, RunInvalid)
from score_exp093 import score_conditions, RunInvalid as ScorerRunInvalid

FORBIDDEN_FLAGS = (
    "--train", "--training", "--finetune", "--fine-tune", "--lr",
    "--learning-rate", "--gpu", "--cuda", "--gpus",
    "--mutate-weights", "--update-weights",
)

N_ITEMS = 60
G4_N_CORRECT = 36
G4_MARGIN_REF = -0.0018
G4_MARGIN_TOL = 1e-4


# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------

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


def guard_g1prime_inherited():
    """G1' inherited via bench-pin byte-identity (no new text introduced).

    The bench pin match (G0) proves byte-identity with EXP092-B, whose
    real-tokenizer offset-mapping cover (240/240) was verified at LOG-4325
    extraction and re-verified at LOG-4339 (erratum C1). Asserted, not assumed.
    """
    return ("inherited (bench-pin byte-identity with EXP092-B; EXP092 "
            "real-tokenizer cover 240/240 stands)")


def guard_g2_directions(npz_path, bench_targets, synthetic=None):
    """G2: direction provenance. synthetic=(layer11, labels) for mock mode."""
    if synthetic is not None:
        layer11, labels = synthetic
    else:
        if not os.path.isfile(npz_path):
            raise RunInvalid(
                f"G2 FAIL: archived .npz not found at {npz_path} — RUN-INVALID.")
        z = np.load(npz_path, allow_pickle=True)  # read-only open
        if z["layers"].shape != (24, 60, 1024) or z["layers"].dtype != np.float32:
            raise RunInvalid(
                f"G2 FAIL: .npz shape {z['layers'].shape} dtype "
                f"{z['layers'].dtype} != (24, 60, 1024) float32 — RUN-INVALID.")
        layer11, labels = z["layers"][LAYER_INDEX], z["labels"]
    d = build_directions(layer11, labels, bench_targets)  # asserts inside
    return d


def synthetic_layer11(bench, seed=93093):
    """Mock-mode G2 input: class-structured synthetic (60, 1024) embeddings."""
    rng = np.random.default_rng(seed)
    targets = sorted({b["ent"] for b in bench})
    means = {t: rng.normal(size=1024) for t in targets}
    H = np.stack([means[b["ent"]] + 0.5 * rng.normal(size=1024)
                  for b in bench]).astype(np.float32)
    return H, [b["ent"] for b in bench]


# ---------------------------------------------------------------------------
# Decision loops
# ---------------------------------------------------------------------------

def run_conditions_mock(bench, directions):
    """Mock decision loop: MockCausalModel, numpy only, 0 model passes."""
    model = MockCausalModel()
    v = directions["v"].astype(np.float64)
    # G5 on the mock backend (probe item 0)
    g5 = verify_g5_mock(model, 0, v[0], ALPHA)
    mB = np.zeros(N_ITEMS)
    mP = np.zeros(N_ITEMS)
    mN = np.zeros(N_ITEMS)
    for i in range(N_ITEMS):
        mB[i] = float(model.forward_logits(i, inject=None)[0]
                      - model.forward_logits(i, inject=None)[1])
        lp = model.forward_logits(i, inject=(v[i], ALPHA))
        mP[i] = float(lp[0] - lp[1])
        ln = model.forward_logits(i, inject=(-v[i], ALPHA))
        mN[i] = float(ln[0] - ln[1])
    return mB, mP, mN, g5


def run_conditions_real(bench, directions, snapshot, log):
    """Real decision loop: frozen LOG-331 snapshot, CPU, read-only."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    v = directions["v"].astype(np.float64)
    phrasing = [b["phrasing"] for b in bench]

    # Thread pin (draft F8): pin to the EXP092 extraction value, assert it.
    torch.set_num_threads(pin.THREAD_PIN)
    n_threads = torch.get_num_threads()
    if n_threads != pin.THREAD_PIN:
        raise RunInvalid(
            f"G4 FAIL: torch intra-op threads = {n_threads} != pinned "
            f"{pin.THREAD_PIN} — RUN-INVALID.")
    log(f"[run] torch intra-op threads pinned: {n_threads}")

    if not os.path.isdir(snapshot):
        raise RunInvalid(f"snapshot directory not found: {snapshot}")
    log(f"[run] loading tokenizer: {snapshot}")
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)

    # G1' real-tokenizer cover check BEFORE any weight access; option token
    # IDs recovered from the offset mapping (never bare-word tokenization).
    table = g1prime.verify_g1_prime(tokenizer, bench)
    n_occ = sum(x["occurrences"] for x in table.values())
    log(f"[run] G1' pass: {n_occ}/240 in-prompt occurrences single-token "
        f"(real tokenizer, offset-mapping cover check).")
    opt_ids = [(table[b["A"]]["token_id"], table[b["C"]]["token_id"])
               for b in bench]

    log(f"[run] loading frozen model: {snapshot}")
    model = AutoModelForCausalLM.from_pretrained(
        snapshot, local_files_only=True, torch_dtype=torch.float32,
        device_map="cpu")
    model.eval()
    model.requires_grad_(False)
    log("[run] model.eval() set; requires_grad_(False) on all parameters.")

    # G1 (pre)
    pre = compute_state_dict_hash(
        {k: v_.detach().cpu() for k, v_ in model.state_dict().items()})
    if pre != pin.WEIGHTS_PIN:
        raise RunInvalid(
            f"G1 FAIL (pre): state_dict SHA-256 {pre} != LOG-331 "
            f"{pin.WEIGHTS_PIN} — Δθ=0 NOT verified — RUN-INVALID.")
    log(f"[run] G1 pre-run hash OK: {pre[:16]}…")

    # G5 injection-site verification (single-item probe, before the run)
    g5 = verify_g5_real(model, tokenizer, bench[0]["prompt"], v[0], ALPHA)
    log(f"[run] G5 pass: (i) rel_err={g5['criterion_i_rel_err']:.2e}, "
        f"(ii) max_abs={g5['criterion_ii_max_abs_change']:.2e}, "
        f"(iii) bit_match={g5['criterion_iii_bit_match']}")

    hook = TorchInjectionHook(alpha=ALPHA)
    mB = np.zeros(N_ITEMS)
    mP = np.zeros(N_ITEMS)
    mN = np.zeros(N_ITEMS)

    def _margins(logits_t, a_id, c_id):
        lg = logits_t.detach().cpu().to(torch.float64).numpy()
        return float(lg[a_id] - lg[c_id])

    with torch.no_grad():
        # Condition B first for all items: G4 must pass before P/N run.
        for i, b in enumerate(bench):
            ids = torch.tensor(
                [tokenizer.encode(b["prompt"], add_special_tokens=False)],
                dtype=torch.long)
            hook.attach(model, v[i])
            hook.disable()
            a_id, c_id = opt_ids[i]
            mB[i] = _margins(model(ids).logits[0, -1, :], a_id, c_id)
            hook.detach()
        # G4: exact S2 baseline reproduction (deterministic model,
        # byte-identical prompts, pinned threads).
        n_b = int((mB > 0.0).sum())
        mean_m = float(mB.mean())
        if n_b != G4_N_CORRECT or abs(mean_m - G4_MARGIN_REF) > G4_MARGIN_TOL:
            raise RunInvalid(
                f"G4 FAIL: clean baseline {n_b}/60 correct (expected "
                f"{G4_N_CORRECT}/60), mean margin {mean_m:.6f} (ref "
                f"{G4_MARGIN_REF}, tol {G4_MARGIN_TOL}) — decision pipeline "
                f"drifted — RUN-INVALID.")
        log(f"[run] G4 pass: clean baseline {n_b}/60, mean margin "
            f"{mean_m:.6f} (ref {G4_MARGIN_REF}).")
        # Conditions P / N.
        for i, b in enumerate(bench):
            ids = torch.tensor(
                [tokenizer.encode(b["prompt"], add_special_tokens=False)],
                dtype=torch.long)
            a_id, c_id = opt_ids[i]
            hook.attach(model, v[i])
            hook.enable()
            mP[i] = _margins(model(ids).logits[0, -1, :], a_id, c_id)
            hook.detach()
            hook.attach(model, -v[i])
            hook.enable()
            mN[i] = _margins(model(ids).logits[0, -1, :], a_id, c_id)
            hook.detach()
    log("[run] 180 forward passes complete (60 B + 60 P + 60 N).")

    # G1 (post): Δθ=0
    post = compute_state_dict_hash(
        {k: v_.detach().cpu() for k, v_ in model.state_dict().items()})
    if post != pin.WEIGHTS_PIN:
        raise RunInvalid(
            f"G1 FAIL (post): state_dict SHA-256 changed during the run — "
            f"Δθ=0 VIOLATED — RUN-INVALID.")
    log(f"[run] G1 post-run hash OK: {post[:16]}… (Δθ=0 verified)")
    return mB, mP, mN, g5, n_threads


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def assert_signed_protocol():
    """Refuse unless the SIGNED protocol exists and verifies under the
    header's self-referential digest rule (LOG-4343).

    Verification rule (from the signature block): recompute SHA-256 over the
    signed file with the 64-character digest value itself blanked (the value
    sits between backticks after the marker ``**SHA-256 (this signed file):** ``).
    A literal hash of the raw file cannot reproduce a self-referential digest.
    Any other byte change breaks the match.
    """
    if pin.SIGNED_PROTOCOL_DIGEST == "PENDING-SIGNATURE":
        print("REFUSAL: protocol unsigned (PENDING-SIGNATURE) — the signing "
              "ceremony (hash + SIGN record) is a separate CEO step; real "
              "execution is not licensed. Use --mock for synthetic tests.",
              file=sys.stderr)
        return False
    path = pin.signed_protocol_path()
    if not os.path.isfile(path):
        print("REFUSAL: signed protocol not found — the protocol is "
              "unsigned; nothing is licensed.", file=sys.stderr)
        return False
    marker = b"**SHA-256 (this signed file):** `"
    raw = open(path, "rb").read()
    i = raw.find(marker)
    if i == -1:
        print("REFUSAL: signed protocol missing its digest marker — "
              "verification rule absent; nothing is licensed.",
              file=sys.stderr)
        return False
    s = i + len(marker)
    if raw[s + 64:s + 65] != b"`":
        print("REFUSAL: signed protocol digest marker malformed — "
              "verification rule absent; nothing is licensed.",
              file=sys.stderr)
        return False
    blanked = raw[:s] + raw[s + 64:]  # blank the 64-char self-digest value
    if hashlib.sha256(blanked).hexdigest() != pin.SIGNED_PROTOCOL_DIGEST:
        print("REFUSAL: signed-protocol digest mismatch — the protocol file "
              "differs from the signed version; nothing is licensed.",
              file=sys.stderr)
        return False
    return True


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for flag in FORBIDDEN_FLAGS:
        if any(a == flag or a.startswith(flag + "=") for a in argv):
            print(f"REFUSAL: forbidden flag {flag} — this protocol licenses "
                  f"no training, no GPU execution, no weight mutation.",
                  file=sys.stderr)
            return 2
    ap = argparse.ArgumentParser(description="EXP093 runner")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--mock", action="store_true",
                    help="synthetic run; never touches weights")
    ap.add_argument("--ceo-clearance", action="store_true",
                    help="CEO execution clearance for the REAL run")
    ap.add_argument("--snapshot", default=None,
                    help="override snapshot dir (default: LOG-331 snapshot)")
    args = ap.parse_args(argv)

    # Launch-chain gates FIRST: signature, then clearance — before any guard,
    # before any weight access (EXP092 FIX 1 discipline).
    if not args.mock:
        if not assert_signed_protocol():
            return 2
        if not args.ceo_clearance:
            print("REFUSAL: real execution requires --ceo-clearance (CEO). "
                  "Use --mock for synthetic tests.", file=sys.stderr)
            return 2

    os.makedirs(args.out_dir, exist_ok=True)
    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print(msg, flush=True)

    mode = "mock" if args.mock else "real"
    try:
        # G0
        bench, g0 = guard_g0_bench()
        log(f"[run] G0 pass: bench pin {g0['pin'][:16]}…, 60/60 unique "
            f"tuples, strata match §2.")
        bench_targets = [b["ent"] for b in bench]
        phrasing = [b["phrasing"] for b in bench]
        # G1' (inherited)
        g1p = guard_g1prime_inherited()
        log(f"[run] G1' {g1p}.")
        # G2
        if args.mock:
            synth = synthetic_layer11(bench)
            d = guard_g2_directions(None, bench_targets, synthetic=synth)
            g2_src = "synthetic (mock)"
        else:
            d = guard_g2_directions(pin.npz_path(), bench_targets)
            g2_src = "archived .npz (read-only)"
        log(f"[run] G2 pass ({g2_src}): 60/60 ||r_i|| > 1e-9 "
            f"(min={d['min_r_norm']:.4f}), 60/60 v unit-norm, "
            f"coherence mean_cos_u={d['mean_pairwise_cosine_u']:.4f}, "
            f"prenorm=[{d['prenorm_min']:.4f},{d['prenorm_max']:.4f}].")
        # Conditions
        if args.mock:
            mB, mP, mN, g5 = run_conditions_mock(bench, d)
            threads = "n/a (mock)"
            log("[run] MOCK mode: 180 synthetic condition passes, "
                "no weights touched.")
        else:
            mB, mP, mN, g5, threads = run_conditions_real(
                bench, d, args.snapshot or pin.SNAPSHOT_DIR, log)
            log("[run] REAL mode: frozen LOG-331 snapshot, CPU, read-only.")
        # Scoring (tie rule inside; >5% ties -> RUN-INVALID)
        report = score_conditions(mB, mP, mN, phrasing)
        report["mode"] = mode  # G3 mode stamp
        # Non-binding diagnostic (§3.2): ||alpha*v|| / median(||h_11||)
        if not args.mock:
            z = np.load(pin.npz_path(), allow_pickle=True)
            h11 = z["layers"][LAYER_INDEX].astype(np.float64)
            med_h = float(np.median(np.linalg.norm(h11, axis=1)))
            report["perturbation_ratio"] = float(ALPHA / med_h)
        report["guards"] = {
            "G0": f"pass (bench pin {g0['pin'][:16]}…)",
            "G1": "pass (pre/post LOG-331 hash)" if not args.mock
                  else "skipped (no weights in mock mode)",
            "G1'": g1p if args.mock else
                   "inherited + real-tokenizer cover re-executed (240/240)",
            "G2": (f"pass (60/60 ||r_i||>1e-9, min={d['min_r_norm']:.4f}, "
                   f"60/60 unit-norm, R4 ok)"),
            "G3": f"mode={mode}",
            "G4": ("pass (36/60, margin tol 1e-4)" if not args.mock
                   else "n/a (mock)"),
            "G5": (f"pass (i rel_err={g5['criterion_i_rel_err']:.2e}, "
                   f"ii max_abs={g5['criterion_ii_max_abs_change']:.2e}, "
                   f"iii bit_match)"),
        }
        report["coherence"] = {
            "mean_pairwise_cosine_u": d["mean_pairwise_cosine_u"],
            "prenorm_norm_range": [d["prenorm_min"], d["prenorm_max"]],
            "max_pairwise_cosine_v": d["max_pairwise_cosine_v"],
            "min_r_norm": d["min_r_norm"],
        }
        report["run_meta"] = {
            "mode": mode,
            "alpha": ALPHA,
            "layer": LAYER_INDEX,
            "n_conditions": 3,
            "n_passes": 180,
            "torch_threads": threads,
            "protocol_digest": pin.SIGNED_PROTOCOL_DIGEST,
            "bench_pin": pin.BENCH_PIN,
        }
    except (RunInvalid, BuilderRunInvalid, ScorerRunInvalid) as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    out_path = os.path.join(args.out_dir, "exp093_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(args.out_dir, "exp093_run_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    r = report["verdict_detail"]["aggregate"]
    print(f"[run] Δ={r['delta']:+.4f} McNemar p={r['mcnemar_p']:.4g} "
          f"monotone={r['monotone']}")
    print(f"[run] Δ_A={report['verdict_detail']['A_first']['delta']:+.4f} "
          f"Δ_C={report['verdict_detail']['C_first']['delta']:+.4f}")
    print(f"[run] AUTHORITATIVE VERDICT: {report['verdict']}")
    print(f"[run] report: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
