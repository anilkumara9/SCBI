"""EXP089 runner — CLI entry point.

Launch-chain position (signed protocol §12): signed pre-registration (LOG-338)
→ bundle build (this bundle) → independent bundle review → CEO execution
clearance → execution.

Refusal rules (signed protocol §8):
  - MUST refuse any run while the protocol is unsigned → enforced by
    assert_signed_protocol() (SIGNED file must exist with the recorded digest).
  - MUST refuse any flag requesting training, GPU execution, or weight
    mutation → FORBIDDEN_FLAGS below.
  - Real execution requires --ceo-clearance. Without it (and without --mock),
    the runner prints the clearance requirement and exits 2.

Modes:
  --mock           synthetic embeddings (seeded, numpy only); never touches
                   weights. For smoke tests and CI.
  --ceo-clearance  REAL execution: frozen snapshot extraction (CPU, read-only)
                   + scoring. Requires torch + transformers installed.

Exit codes: 0 = ran (verdict in report); 2 = refused (no clearance / forbidden
flag / unsigned protocol); 3 = RUN-INVALID (a guard fired).
"""

import argparse
import hashlib
import os
import sys

from benchmark_exp089 import SIGNED_PROTOCOL_DIGEST, signed_protocol_path

FORBIDDEN_FLAGS = (
    "--train", "--training", "--finetune", "--fine-tune", "--lr",
    "--learning-rate", "--gpu", "--cuda", "--gpus",
    "--mutate-weights", "--update-weights",
)


def assert_signed_protocol():
    """Refuse unless the SIGNED protocol exists with the recorded digest."""
    path = signed_protocol_path()
    if not os.path.isfile(path):
        print("REFUSAL: signed protocol not found — the protocol is unsigned; "
              "nothing is licensed.", file=sys.stderr)
        return False
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            sha.update(chunk)
    if sha.hexdigest() != SIGNED_PROTOCOL_DIGEST:
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
                  f"no training, no GPU execution, no weight mutation (§8).",
                  file=sys.stderr)
            return 2
    ap = argparse.ArgumentParser(description="EXP089 runner")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--mock", action="store_true",
                    help="synthetic run; never touches weights")
    ap.add_argument("--ceo-clearance", action="store_true",
                    help="CEO execution clearance for the REAL run")
    args = ap.parse_args(argv)

    if not assert_signed_protocol():
        return 2
    if not args.mock and not args.ceo_clearance:
        print("REFUSAL: real execution requires --ceo-clearance (CEO). "
              "Use --mock for synthetic tests.", file=sys.stderr)
        return 2

    os.makedirs(args.out_dir, exist_ok=True)
    # Local imports: extraction module imports torch/transformers lazily.
    from extract_state_embeddings import extract_mock, extract_real, RunInvalid
    from score_exp089 import decide_from_embeddings

    try:
        if args.mock:
            print("[run] MOCK mode: synthetic embeddings, no weights touched.")
            emb_path, meta = extract_mock(args.out_dir)
        else:
            print("[run] REAL mode: frozen LOG-331 snapshot, CPU, read-only.")
            emb_path, meta = extract_real(args.out_dir)
        report = decide_from_embeddings(emb_path)
        # F1 (Law #14 LOG-345): stamp execution mode into the authoritative
        # verdict artifact — a mock-run KILL must be distinguishable on disk
        # from a real-run KILL.
        report["mode"] = meta.get("mode", "unknown")
    except RunInvalid as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3

    import json
    out_path = os.path.join(args.out_dir, "exp089_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    r = report
    print(f"[run] n_correct={r['n_correct']}/60  acc={r['accuracy']:.4f}  "
          f"acc_Afirst={r['acc_Afirst']:.4f}  acc_Cfirst={r['acc_Cfirst']:.4f}  "
          f"p_upper={r['binomial_p_upper_tail']:.6f}")
    print(f"[run] AUTHORITATIVE VERDICT: {r['verdict']}")
    print(f"[run] report: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
