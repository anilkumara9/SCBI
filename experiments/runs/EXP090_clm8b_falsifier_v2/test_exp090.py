"""EXP090 unit tests — ALL must pass. Synthetic/mock only; no weights touched.

Covers: §6 bench contract (deterministic builder output + archive provenance
pin; the STRUCK byte-reproduction guard is absent), verdict-boundary cases
(38/60, 37/60, 39/60), split-tie PIVOT, opposite-tilt PIVOT, G4
deaf-instrument RUN-INVALID, tie-breaking, G1/G2/G3 guard logic, binomial
exactness, runner refusal rules, and the signed-protocol digest guard.
numpy-only (no torch required).
"""

import json
import math
import os
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import benchmark_exp090
from benchmark_exp090 import (
    ARCHIVE_PROVENANCE_HASH, artifacts_dir, assert_archive_hash,
    assert_phrasing_balance, build_benchmark, state_text_of,
)
from extract_state_embeddings import (
    RunInvalid as ExtractRunInvalid,
    check_single_token_entity, compute_state_dict_hash, guard_state_dict_hash,
    extract_mock,
)
import extract_state_embeddings as ext_mod
from score_exp090 import (
    RunInvalid as ScoreRunInvalid,
    adjudicate, decide_from_embeddings, exact_binomial_upper_tail,
    main as score_main,
)
import run_exp090
run_main = run_exp090.main


def _synthetic_case(n_correct_a, n_correct_c):
    """Build (correct_mask, phrasing, cosines) with n_correct_a/30 on the
    A-first split and n_correct_c/30 on the C-first split.

    correct item → cosA=0.9, cosC=0.1; incorrect → cosA=0.1, cosC=0.9.
    """
    correct, phrasing, cos = [], [], []
    for split, n_ok in (("A-first", n_correct_a), ("C-first", n_correct_c)):
        for j in range(30):
            ok = j < n_ok
            correct.append(ok)
            phrasing.append(split)
            cos.extend([0.9, 0.1] if ok else [0.1, 0.9])
    return correct, phrasing, np.array(cos)


class TestBenchContract(unittest.TestCase):
    """§6: the repaired bench contract (the single design change vs EXP089)."""

    def test_length_60(self):
        self.assertEqual(len(build_benchmark()), 60)

    def test_bench_matches_exp089_builder_byte_identical(self):
        # The signed protocol §6 registers this builder as the LOG-345-verified
        # verbatim port of the repaired EXP077 benchmark block (EXP089's
        # builder, the reviewed artifact). Any drift in items/prompts/phrasing
        # breaks the registration — pin byte-identity here.
        sib = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "EXP089_clm8b_falsifier")
        if not os.path.isdir(sib):
            self.skipTest("EXP089 bundle not present alongside this bundle")
        sys.path.insert(0, os.path.abspath(sib))
        try:
            import benchmark_exp089 as b89
            a = json.dumps(b89.build_benchmark(), sort_keys=True)
        finally:
            sys.path.remove(os.path.abspath(sib))
        b = json.dumps(build_benchmark(), sort_keys=True)
        self.assertEqual(a, b)

    def test_bench_deterministic_two_builds_identical(self):
        # The registered bench is the deterministic builder output: two
        # independent builds must be byte-identical.
        b1 = json.dumps(build_benchmark(), sort_keys=True)
        b2 = json.dumps(build_benchmark(), sort_keys=True)
        self.assertEqual(b1, b2)

    def test_struck_guard_absent(self):
        # The EXP089 byte-for-value (ent,typ) reproduction guard is STRUCK as
        # unsatisfiable (LOG-344/345) — it must not exist in EXP090.
        self.assertFalse(
            hasattr(benchmark_exp090, "verify_against_instance_records"),
            "struck guard resurrected in EXP090")

    def test_archive_pin_passes_on_real_archive(self):
        # The real archive's hash matches the §6-recorded provenance hash.
        got = assert_archive_hash()
        self.assertEqual(got, ARCHIVE_PROVENANCE_HASH)
        self.assertEqual(
            got,
            "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585")

    def test_archive_pin_refuses_on_tampered_archive(self):
        # Tampered archive → RUN-INVALID, never a verdict.
        with tempfile.TemporaryDirectory() as d:
            tampered = os.path.join(d, "exp077_instance_records.json")
            with open(tampered, "w") as f:
                json.dump([{"ent": "X", "typ": "planet"}], f)
            old = benchmark_exp090.artifacts_dir
            benchmark_exp090.artifacts_dir = lambda: d
            try:
                with self.assertRaises(benchmark_exp090.RunInvalid):
                    assert_archive_hash()
            finally:
                benchmark_exp090.artifacts_dir = old

    def test_provenance_pin_fires_in_mock_pipeline(self):
        # The §6 pin guards even the mock pipeline: a tampered archive
        # aborts extraction before any embedding is written.
        with tempfile.TemporaryDirectory() as d:
            tampered = os.path.join(d, "exp077_instance_records.json")
            with open(tampered, "w") as f:
                json.dump([{"ent": "X", "typ": "planet"}], f)
            old = benchmark_exp090.artifacts_dir
            benchmark_exp090.artifacts_dir = lambda: d
            try:
                with tempfile.TemporaryDirectory() as out:
                    with self.assertRaises(ExtractRunInvalid):
                        extract_mock(out)
                    self.assertFalse(
                        os.path.exists(os.path.join(out, "exp090_embeddings.npz")),
                        "embeddings written despite provenance-pin failure")
            finally:
                benchmark_exp090.artifacts_dir = old

    def test_phrasing_balance_30_30(self):
        n_a, n_c = assert_phrasing_balance(build_benchmark())
        self.assertEqual((n_a, n_c), (30, 30))

    def test_state_text_excludes_question(self):
        for b in build_benchmark():
            s = state_text_of(b["prompt"])
            self.assertTrue(s.startswith("Premise:"))
            self.assertNotIn("Question:", s)
            self.assertNotIn("Answer:", s)


class TestVerdictBoundaries(unittest.TestCase):
    def test_continue_38_clean(self):
        # 38/60 = 20/30 + 18/30, both splits > 0.5 → CONTINUE
        r = adjudicate(*_synthetic_case(20, 18))
        self.assertEqual(r["verdict"], "CONTINUE")
        self.assertEqual(r["n_correct"], 38)

    def test_continue_39(self):
        r = adjudicate(*_synthetic_case(20, 19))
        self.assertEqual(r["verdict"], "CONTINUE")

    def test_continue_60(self):
        r = adjudicate(*_synthetic_case(30, 30))
        self.assertEqual(r["verdict"], "CONTINUE")

    def test_kill_37(self):
        # 37/60 = 19/30 + 18/30 → KILL regardless of splits
        r = adjudicate(*_synthetic_case(19, 18))
        self.assertEqual(r["verdict"], "KILL")

    def test_kill_0(self):
        r = adjudicate(*_synthetic_case(0, 0))
        self.assertEqual(r["verdict"], "KILL")

    def test_kill_30(self):
        r = adjudicate(*_synthetic_case(15, 15))
        self.assertEqual(r["verdict"], "KILL")

    def test_pivot_split_exactly_half(self):
        # 38/60 but A-first exactly 15/30 = 0.5 → PIVOT (F2 boundary rule)
        r = adjudicate(*_synthetic_case(15, 23))
        self.assertEqual(r["n_correct"], 38)
        self.assertEqual(r["verdict"], "PIVOT")

    def test_pivot_opposite_tilts(self):
        # 38/60 with opposite tilts (12/30 vs 26/30) → PIVOT
        r = adjudicate(*_synthetic_case(12, 26))
        self.assertEqual(r["verdict"], "PIVOT")

    def test_pivot_one_split_below_half(self):
        # 40/60 but A-first 14/30 < 0.5 → PIVOT, CONTINUE withheld
        r = adjudicate(*_synthetic_case(14, 26))
        self.assertEqual(r["n_correct"], 40)
        self.assertEqual(r["verdict"], "PIVOT")

    def test_bar_sharpness_registered_values(self):
        # Signed protocol §7 registers P(X≥38)=0.0260 (3dp, exact computation);
        # the full-precision value is 0.0259469… → 0.0259 at 4dp.
        # P(X≥37)=0.0462 > α — the bar is sharp.
        p38 = exact_binomial_upper_tail(38)
        self.assertEqual(round(p38, 3), 0.026)
        self.assertEqual(round(p38, 4), 0.0259)
        self.assertEqual(round(exact_binomial_upper_tail(37), 4), 0.0462)
        # Independent recomputation (not via the module under test).
        p = sum(math.comb(60, k) for k in range(38, 61)) / 2 ** 60
        self.assertAlmostEqual(p38, p, places=12)


class TestInstrumentGate(unittest.TestCase):
    def test_g4_deaf_instrument_run_invalid(self):
        # All 120 cosines identical → spread 0 < 1e-4 → RUN-INVALID, never KILL.
        correct = [False] * 60
        phrasing = ["A-first"] * 30 + ["C-first"] * 30
        cosines = np.full(120, 0.5)
        with self.assertRaises(ScoreRunInvalid):
            adjudicate(correct, phrasing, cosines)

    def test_g4_healthy_instrument_passes(self):
        correct, phrasing, cos = _synthetic_case(20, 18)  # spread 0.8
        r = adjudicate(correct, phrasing, cos)
        self.assertEqual(r["verdict"], "CONTINUE")

    def test_tie_breaks_toward_foil(self):
        # Exact float tie → C (foil) chosen, counted as incorrect + tie count.
        n = 60
        state = np.eye(3, dtype=np.float32)
        s = np.tile(state[0], (n, 1))
        a = np.tile(state[1], (n, 1))
        c = np.tile(state[1], (n, 1))  # actC == actA → exact ties everywhere
        phrasing = np.array(["A-first"] * 30 + ["C-first"] * 30)
        ids = np.array([f"item_{i}" for i in range(n)])
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.npz")
            np.savez(p, state=s, actA=a, actC=c, ids=ids, phrasing=phrasing)
            # Ties everywhere → spread 0 → G4 fires first (RUN-INVALID).
            with self.assertRaises(ScoreRunInvalid):
                decide_from_embeddings(p)

    def test_tie_counted_when_instrument_healthy(self):
        # One exact tie amid healthy spread: tie → incorrect, tie counted.
        n = 60
        rng = np.random.default_rng(7)
        s = rng.normal(size=(n, 8)).astype(np.float32)
        a = rng.normal(size=(n, 8)).astype(np.float32)
        c = rng.normal(size=(n, 8)).astype(np.float32)
        a[0] = c[0]  # exact tie on item 0
        phrasing = np.array(["A-first"] * 30 + ["C-first"] * 30)
        ids = np.array([f"item_{i}" for i in range(n)])
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.npz")
            np.savez(p, state=s, actA=a, actC=c, ids=ids, phrasing=phrasing)
            try:
                r = decide_from_embeddings(p)
            except ScoreRunInvalid:
                self.skipTest("random draw hit G4 deafness (astronomically "
                              "unlikely; rng seed issue)")
            self.assertGreaterEqual(r["ties_broken_toward_foil"], 1)
            self.assertFalse(r["per_item"][0]["correct"])  # tie → foil


class TestGuards(unittest.TestCase):
    def test_g1_multitoken_refuses(self):
        with self.assertRaises(ExtractRunInvalid):
            check_single_token_entity(lambda t: [1, 2], "Mars", "target")

    def test_g1_singletoken_passes(self):
        self.assertEqual(
            check_single_token_entity(lambda t: [42], "Mars", "target"), 42)

    def test_g2_hash_mismatch_refuses(self):
        fake = {"w": np.ones((4, 4), dtype=np.float32)}
        with self.assertRaises(ExtractRunInvalid):
            guard_state_dict_hash(fake, "test")  # never equals the real hash

    def test_g2_hash_match_passes(self):
        fake = {"a": np.ones((2, 2), dtype=np.float32),
                "b": np.zeros(3, dtype=np.float32)}
        want = compute_state_dict_hash(fake)
        old = ext_mod.EXPECTED_STATE_DICT_HASH
        ext_mod.EXPECTED_STATE_DICT_HASH = want
        try:
            self.assertEqual(guard_state_dict_hash(fake, "test"), want)
        finally:
            ext_mod.EXPECTED_STATE_DICT_HASH = old

    def test_g2_hash_deterministic_and_order_stable(self):
        d1 = {"b": np.ones(3), "a": np.ones((2, 2))}
        d2 = {"a": np.ones((2, 2)), "b": np.ones(3)}
        self.assertEqual(compute_state_dict_hash(d1), compute_state_dict_hash(d2))
        d3 = {"a": np.ones((2, 2)) * 2, "b": np.ones(3)}
        self.assertNotEqual(compute_state_dict_hash(d1), compute_state_dict_hash(d3))


class TestRunnerRefusals(unittest.TestCase):
    def test_refuses_without_clearance(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run_exp090.main(["--out-dir", d]), 2)

    def test_refuses_forbidden_flags(self):
        with tempfile.TemporaryDirectory() as d:
            for flag in ("--gpu", "--train", "--cuda", "--finetune"):
                self.assertEqual(
                    run_exp090.main(["--out-dir", d, "--mock", flag]), 2,
                    f"flag {flag} was not refused")

    def test_signed_protocol_digest_guard_passes(self):
        self.assertTrue(run_exp090.assert_signed_protocol())

    def test_mock_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            rc = run_exp090.main(["--out-dir", d, "--mock"])
            self.assertEqual(rc, 0)
            rp = os.path.join(d, "exp090_report.json")
            self.assertTrue(os.path.isfile(rp))
            with open(rp) as f:
                report = json.load(f)
            self.assertIn(report["verdict"], ("CONTINUE", "KILL", "PIVOT"))
            self.assertEqual(report["n_total"], 60)
            self.assertTrue(os.path.isfile(
                os.path.join(d, "exp090_embeddings.npz")))


class TestScorerEndToEnd(unittest.TestCase):
    def test_all_correct_continue(self):
        n = 60
        s = np.tile(np.array([1.0, 0.0], dtype=np.float32), (n, 1))
        a = np.tile(np.array([1.0, 0.1], dtype=np.float32), (n, 1))
        c = np.tile(np.array([0.0, 1.0], dtype=np.float32), (n, 1))
        phrasing = np.array(["A-first"] * 30 + ["C-first"] * 30)
        ids = np.array([f"item_{i}" for i in range(n)])
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.npz")
            np.savez(p, state=s, actA=a, actC=c, ids=ids, phrasing=phrasing)
            r = decide_from_embeddings(p)
        self.assertEqual(r["n_correct"], 60)
        self.assertEqual(r["verdict"], "CONTINUE")
        self.assertEqual(len(r["per_item"]), 60)


class TestModeStamp(unittest.TestCase):
    """F1 (Law #14 LOG-345, carried forward): the verdict artifact must carry
    its mode."""

    def _bundle(self, d, mode=None):
        n = 60
        s = np.tile(np.array([1.0, 0.0], dtype=np.float32), (n, 1))
        a = np.tile(np.array([1.0, 0.1], dtype=np.float32), (n, 1))
        c = np.tile(np.array([0.0, 1.0], dtype=np.float32), (n, 1))
        phrasing = np.array(["A-first"] * 30 + ["C-first"] * 30)
        ids = np.array([f"item_{i}" for i in range(n)])
        p = os.path.join(d, "exp090_embeddings.npz")
        np.savez(p, state=s, actA=a, actC=c, ids=ids, phrasing=phrasing)
        if mode is not None:
            with open(os.path.join(d, "exp090_extraction_meta.json"), "w") as f:
                json.dump({"mode": mode}, f)
        return p

    def test_scorer_main_stamps_mock_mode(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._bundle(d, mode="mock")
            out = os.path.join(d, "out")
            rc = score_main(["--embeddings", p, "--out-dir", out])
            self.assertEqual(rc, 0)
            with open(os.path.join(out, "exp090_report.json")) as f:
                rep = json.load(f)
            self.assertEqual(rep["mode"], "mock")

    def test_scorer_main_stamps_unknown_without_meta(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._bundle(d, mode=None)
            out = os.path.join(d, "out")
            rc = score_main(["--embeddings", p, "--out-dir", out])
            self.assertEqual(rc, 0)
            with open(os.path.join(out, "exp090_report.json")) as f:
                rep = json.load(f)
            self.assertEqual(rep["mode"], "unknown")

    def test_runner_mock_stamps_mock_mode(self):
        with tempfile.TemporaryDirectory() as d:
            rc = run_main(["--out-dir", d, "--mock"])
            self.assertEqual(rc, 0)
            with open(os.path.join(d, "exp090_report.json")) as f:
                rep = json.load(f)
            self.assertEqual(rep["mode"], "mock")


if __name__ == "__main__":
    unittest.main(verbosity=2)
