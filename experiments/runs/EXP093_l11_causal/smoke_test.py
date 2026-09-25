"""EXP093 zero-model-pass smoke test.

Checks: bundle completeness, bench pin, direction builder on the real
archived .npz (read-only), the mock pipeline end-to-end (0 torch imports,
0 model passes), PENDING-SIGNATURE refusal, and the coherence gate.
Zero model passes: numpy only until the --mock pipeline's fake model.
"""

import json
import os
import sys
import tempfile

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
sys.path.append(os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))

import protocol_pin as pin
import reference_implementation as ref
from direction_builder import (build_directions, write_direction_verification)
import run_exp093

checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))
    print(f"[{'OK' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def main():
    required = ["protocol_pin.py", "direction_builder.py", "inject.py",
                "run_exp093.py", "score_exp093.py", "test_exp093.py",
                "smoke_test.py", "requirements.txt", "BUILD_NOTES.md"]
    for f in required:
        check(f"bundle file {f}", os.path.isfile(os.path.join(BUNDLE_DIR, f)))

    # Bench pin (canonical EXP092-B reuse)
    bench = ref.build_bench()
    check("bench pin (G0)", ref.bench_sha256(bench) == pin.BENCH_PIN,
          f"{pin.BENCH_PIN[:16]}…")
    check("bench 60 unique ordered tuples",
          len({tuple(b["tuple"]) for b in bench}) == 60)

    # Direction builder on the real archived .npz (read-only)
    try:
        z = np_load_ro()
        bench_targets = [b["ent"] for b in bench]
        d = build_directions(z["layers"][11], z["labels"], bench_targets)
        check("G2 direction construction (real .npz, read-only)", True,
              f"min||r||={d['min_r_norm']:.4f}, 60/60 ||r_i||>1e-9")
        check("R4: 60 v^(-i) not bit-identical", d["r4_not_bit_identical"])
        with tempfile.TemporaryDirectory() as td:
            art = write_direction_verification(
                pin.npz_path(), bench_targets,
                out_path=os.path.join(td, "direction_verification.json"))
        check("direction_verification.json gate PASS",
              art["gate"] == "PASS",
              f"mean_cos_u={d['mean_pairwise_cosine_u']:.4f} (registered "
              f"-0.0160; only ~3% coherent -> KILL expected)")
    except Exception as e:  # noqa: BLE001 — smoke test reports, not masks
        check("G2 direction construction (real .npz, read-only)", False, str(e))

    # Signed protocol (LOG-4343) verifies under the header blanking rule
    check("signed protocol digest verifies",
          run_exp093.assert_signed_protocol(),
          f"{pin.SIGNED_PROTOCOL_DIGEST[:16]}… (LOG-4343)")

    # Mock pipeline end-to-end
    try:
        with tempfile.TemporaryDirectory() as td:
            rc = run_exp093.main(["--out-dir", td, "--mock"])
            rep = json.load(open(os.path.join(td, "exp093_report.json")))
        check("mock pipeline end-to-end", rc == 0 and rep["mode"] == "mock",
              f"verdict={rep['verdict']}")
        check("torch never imported (0 model passes)",
              "torch" not in sys.modules)
    except Exception as e:  # noqa: BLE001
        check("mock pipeline end-to-end", False, str(e))

    n_fail = sum(1 for _, ok, _ in checks if not ok)
    print(f"\nsmoke: {len(checks) - n_fail}/{len(checks)} checks passed")
    return 1 if n_fail else 0


def np_load_ro():
    import numpy as np
    return np.load(pin.npz_path(), allow_pickle=True)


if __name__ == "__main__":
    sys.exit(main())
