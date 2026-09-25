#!/usr/bin/env python3
"""EXP088 smoke test (CPU only, zero model passes, zero torch).

Run directly, or via:  python3 run_exp088.py --smoke

Verifies, without touching any model weight:
  1. All bundle modules import with no torch installed.
  2. Startup refusal: --run without both sign-off flags -> exit 2,
     no artifact written.
  3. Crash guard: _startup_preflight raises ApparatusError on a missing
     corpus BEFORE any model construction is possible.
  4. Preflight passes on the real pinned artifacts (CPU smoke mode).
  5. The pinned Stage-A corpus artifact exists and matches the runner pin.
  6. The full evaluator suite passes (24/24).
  7. The mock-model end-to-end harness passes (22/22) — the entire
     orchestration (Stage-A gate, F2 RAND draw, Stage-B loop, DeltaTheta
     guard, budget accounting, verdicts, full-scale budget gate,
     per-arm leak-layer wiring) on synthetic fixtures.

Exit 0 iff every gate passes. Any failure is loud (nonzero exit).
"""

import argparse
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

RESULTS = []


def gate(name, fn):
    try:
        detail = fn()
        print(f"SMOKE-PASS {name} :: {detail}")
        RESULTS.append(True)
    except Exception as e:  # noqa: BLE001 - loud, keep going
        print(f"SMOKE-FAIL {name} :: {type(e).__name__}: {e}")
        RESULTS.append(False)


def g1_imports():
    assert "torch" not in sys.modules, "torch must not be imported"
    import exp088_endpoints, exp088_probeset, exp088_ramping  # noqa: F401
    import exp088_rng, run_exp088  # noqa: F401
    return "5 modules import clean, torch absent"


def g2_clearance_refusal():
    import run_exp088 as RUN
    with tempfile.TemporaryDirectory() as td:
        ns = argparse.Namespace(ceo_gpu_clearance=False,
                                bundle_review_signoff=False,
                                out=td, corpus=None, records=None)
        rc = RUN.cmd_run(ns)
        assert rc == 2, f"expected 2, got {rc}"
        assert not os.path.exists(os.path.join(td, "exp088_results.json"))
        assert not os.path.exists(os.path.join(td, "exp088_run_log.txt")), \
            "no log may be written on refusal"
    return "exit 2, no artifact, no log"


def g3_preflight_crash_guard():
    import run_exp088 as RUN
    logs = []
    with tempfile.TemporaryDirectory() as td:
        ns = argparse.Namespace(
            corpus=os.path.join(td, "missing.json"), records=None, out=td)
        try:
            RUN._startup_preflight(ns, logs.append, check_gpu=False)
        except RUN.ApparatusError as e:
            assert "corpus" in str(e).lower()
            return f"ApparatusError before any weight access: {e}"
        raise AssertionError("preflight did not halt on missing corpus")


def g4_preflight_on_pinned_artifacts():
    import run_exp088 as RUN
    logs = []
    ns = argparse.Namespace(corpus=None, records=None, out=None)
    RUN._startup_preflight(ns, logs.append, check_gpu=False)
    assert any("ALL CHECKS PASS" in m for m in logs)
    return "corpus + records + geometry + outdir verified"


def g5_corpus_pin():
    import json
    import hashlib
    import run_exp088 as RUN
    art = json.load(open(os.path.join(HERE, "stageA_corpus.json")))
    ids = art["token_ids"]
    assert len(ids) == 50000, len(ids)
    sha = hashlib.sha256(b",".join(str(i).encode() for i in ids)).hexdigest()
    assert sha == art["token_ids_sha256"] == RUN.CORPUS_TOKEN_IDS_SHA256, \
        "artifact sha != runner pin"
    return f"50,000 tokens, sha {sha[:16]}... == runner pin"


def g6_evaluator_suite():
    import test_exp088
    # run the suite's checks without its __main__ summary path
    passed, failed = 0, []
    for name, fn in test_exp088.CHECKS:
        try:
            fn()
            passed += 1
        except Exception as e:  # noqa: BLE001
            failed.append(f"{name}: {e}")
    assert not failed, f"{len(failed)} evaluator checks failed: {failed[:3]}"
    return f"{passed}/{len(test_exp088.CHECKS)} evaluator checks pass"


def g7_mock_harness():
    import mock_harness
    with tempfile.TemporaryDirectory() as td:
        res = mock_harness.run_all(td)
    failed = [f"{n}: {d}" for n, ok, d in res if not ok]
    assert not failed, f"{len(failed)} harness checks failed: {failed[:3]}"
    return f"{len(res)}/{len(res)} mock-harness checks pass (zero model passes)"


def main():
    gate("imports-without-torch", g1_imports)
    gate("clearance-refusal", g2_clearance_refusal)
    gate("preflight-crash-guard", g3_preflight_crash_guard)
    gate("preflight-on-pinned-artifacts", g4_preflight_on_pinned_artifacts)
    gate("corpus-artifact-pin", g5_corpus_pin)
    gate("evaluator-suite", g6_evaluator_suite)
    gate("mock-harness-end-to-end", g7_mock_harness)
    n_ok = sum(RESULTS)
    print(f"SMOKE {n_ok}/{len(RESULTS)} gates pass")
    return 0 if n_ok == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
