"""EXP092 smoke test — 0 model passes.

Verifies, without touching weights: module imports, CLI parsing, refusal
behaviors (exit 2 paths), the signed-protocol digest guard, bench integrity,
guard artifacts, and a fast mock extraction + scoring pass (seeded numpy
only). Exit 0 = PASS, 1 = FAIL.
"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CHECKS = []


def check(name, fn):
    try:
        fn()
        CHECKS.append((name, True, ""))
    except Exception as e:  # noqa: BLE001 - smoke test must report, not crash
        CHECKS.append((name, False, f"{type(e).__name__}: {e}"))


def main():
    import reference_implementation as ref
    import protocol_pin
    import g1prime
    import extract_layer_embeddings as ext
    import score_exp092 as score
    import run_exp092

    check("import reference_implementation",
          lambda: ref.build_bench())
    check("bench pin registered",
          lambda: (_ for _ in ()).throw(
              AssertionError("pin mismatch")) if ref.bench_sha256()
          != protocol_pin.BENCH_PIN else None)
    check("bench 60 items / 60 unique tuples",
          lambda: (_ for _ in ()).throw(AssertionError()) if not (
              len(ref.build_bench()) == 60 and
              len({(b["domain"], tuple(b["tuple"]))
                   for b in ref.build_bench()}) == 60) else None)
    check("signed-protocol digest guard",
          lambda: (_ for _ in ()).throw(
              AssertionError("digest guard failed"))
          if not run_exp092.assert_signed_protocol() else None)
    check("G0 passes", lambda: ext.guard_g0_bench())
    check("G2 artifact passes", lambda: ext.guard_g2_artifact())
    check("G1' artifact passes", lambda: g1prime.check_g1prime_artifact())
    check("runner refuses without clearance",
          lambda: (_ for _ in ()).throw(AssertionError("rc!=2"))
          if run_exp092.main(["--out-dir", tempfile.mkdtemp()]) != 2
          else None)
    check("runner refuses --gpu",
          lambda: (_ for _ in ()).throw(AssertionError("rc!=2"))
          if run_exp092.main(["--out-dir", tempfile.mkdtemp(),
                              "--mock", "--gpu"]) != 2 else None)
    # Fast mock extraction + scoring (seeded numpy; no weights).
    def _mock_pipeline():
        with tempfile.TemporaryDirectory() as td:
            emb_path, meta = ext.extract_mock(td)
            assert meta["mode"] == "mock"
            rep = score.decide_from_embeddings(emb_path, perm_b=20)
            assert rep["verdict"] in ("CONTINUE", "KILL", "PIVOT")
            assert len(rep["layers"]) == 24
    check("mock extraction + scoring (perm_b=20)", _mock_pipeline)

    # G4 sanity: zero-spread instrument refuses.
    def _g4():
        import numpy as np
        bench = ref.build_bench()
        layers = np.zeros((24, 60, 8), dtype=np.float32)
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "e.npz")
            np.savez(p, layers=layers,
                     opt_logits=np.zeros((60, 2), dtype=np.float32),
                     ids=np.array([b["id"] for b in bench]),
                     labels=np.array([b["ent"] for b in bench]),
                     phrasing=np.array([b["phrasing"] for b in bench]),
                     domain=np.array([b["domain"] for b in bench]))
            try:
                score.decide_from_embeddings(p, perm_b=10)
            except score.RunInvalid:
                return
            raise AssertionError("G4 did not fire")
    check("G4 zero-spread refuses", _g4)

    failed = [c for c in CHECKS if not c[1]]
    print(f"smoke: {len(CHECKS) - len(failed)}/{len(CHECKS)} checks passed")
    for name, ok, err in CHECKS:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}"
              + (f" — {err}" if err else ""))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
