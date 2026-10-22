"""EXP091 unit tests — ALL must pass. Synthetic/mock only; no weights touched.

Covers: §6 bench contract (deterministic builder output + archive provenance
pin; the STRUCK byte-reproduction guard is absent), G1' in-context
single-token verification (the design change vs EXP090 — real-tokenizer
execution path via a fake tokenizer implementing the HF interface, positive
AND negative cases, build-time artifact binding), action-text coupling
(" "+A / " "+C), verdict-boundary cases (38/60, 37/60, 39/60), split-tie
PIVOT, opposite-tilt PIVOT, G4 deaf-instrument RUN-INVALID, tie-breaking,
G1-legacy/G2/G3 guard logic, binomial exactness, runner refusal rules, and
the signed-protocol digest guard.
numpy-only (no torch required).
"""

import json
import math
import os
import re
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import benchmark_exp091
from benchmark_exp091 import (
    ALL_ENTITIES, ARCHIVE_PROVENANCE_HASH, action_text_of, artifacts_dir,
    assert_archive_hash, assert_phrasing_balance, bench_sha256,
    build_benchmark, check_g1prime_artifact, state_text_of,
    verify_g1_prime,
)
from extract_state_embeddings import (
    RunInvalid as ExtractRunInvalid,
    check_single_token_entity, compute_state_dict_hash, guard_state_dict_hash,
    extract_mock, guard_g1_prime_action_texts,
)
import extract_state_embeddings as ext_mod
from score_exp091 import (
    RunInvalid as ScoreRunInvalid,
    adjudicate, decide_from_embeddings, exact_binomial_upper_tail,
    main as score_main,
)
import run_exp091
run_main = run_exp091.main


# ---------------------------------------------------------------------------
# Fake tokenizer implementing the HF fast-tokenizer interface used by
# verify_g1_prime: tokenizer(text, add_special_tokens=False,
# return_offsets_mapping=True) -> {"input_ids", "offset_mapping"};
# tokenizer.convert_ids_to_tokens(ids) -> [str].
# Splits text into word/punctuation tokens with character-accurate offsets.
# split_words: words emitted as TWO tokens (simulates a multi-token entity).
# flip_words: words whose token id alternates across occurrences (simulates
#             an unstable tokenization).
# ---------------------------------------------------------------------------
class FakeTokenizer:
    def __init__(self, split_words=(), flip_words=()):
        self.split_words = set(split_words)
        self.flip_words = set(flip_words)
        self._vocab = {}
        self._counter = 1000
        self._pieces = {}
        self._flip_state = {}

    def _tok_id(self, piece, word):
        if word in self.flip_words:
            self._flip_state[word] = not self._flip_state.get(word, False)
            key = (piece, self._flip_state[word])
        else:
            key = (piece, None)
        if key not in self._vocab:
            self._counter += 1
            self._vocab[key] = self._counter
        tid = self._vocab[key]
        self._pieces[tid] = piece
        return tid

    def __call__(self, text, add_special_tokens=False,
                 return_offsets_mapping=False):
        ids, offsets = [], []
        for m in re.finditer(r"[A-Za-z]+|[^A-Za-z\s]", text):
            word = m.group()
            s, e = m.span()
            if word in self.split_words:
                mid = s + max(1, (e - s) // 2)
                for (a, b) in ((s, mid), (mid, e)):
                    piece = text[a:b]
                    ids.append(self._tok_id(piece, word))
                    offsets.append((a, b))
            else:
                piece = "Ġ" + word
                ids.append(self._tok_id(piece, word))
                offsets.append((s, e))
        out = {"input_ids": ids}
        if return_offsets_mapping:
            out["offset_mapping"] = offsets
        return out

    def convert_ids_to_tokens(self, ids):
        return [self._pieces[i] for i in ids]

    def encode(self, text, add_special_tokens=False):
        return self(text, add_special_tokens=add_special_tokens)["input_ids"]


# Registered G1' per-entity table (signed protocol §6 — drafter-executed with
# the real Pythia tokenizer, 2026-09-25; build-time artifact re-verified).
REGISTERED_G1PRIME_COUNTS = {
    "Mars": 42, "Venus": 14, "Jupiter": 8, "Saturn": 16, "Mercury": 40,
    "Iron": 42, "Gold": 14, "Silver": 8, "Bronze": 16, "Steel": 40,
}
REGISTERED_G1PRIME_IDS = {
    "Mars": 13648, "Venus": 36210, "Jupiter": 34434, "Saturn": 38876,
    "Mercury": 36091, "Iron": 17826, "Gold": 7284, "Silver": 16309,
    "Bronze": 49134, "Steel": 19727,
}


class TestBenchContract(unittest.TestCase):
    """§6: the bench contract (carried from EXP090 — construction unchanged)."""

    def test_length_60(self):
        self.assertEqual(len(build_benchmark()), 60)

    def test_bench_matches_exp089_builder_byte_identical(self):
        # The signed protocol §6 registers this builder as the LOG-345-verified
        # verbatim port of the repaired EXP077 benchmark block (EXP089's
        # builder, the reviewed artifact). Any drift in items/prompts/phrasing
        # breaks the registration — pin byte-identity here. (The G1' change
        # does not touch the builder output.)
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
        b1 = json.dumps(build_benchmark(), sort_keys=True)
        b2 = json.dumps(build_benchmark(), sort_keys=True)
        self.assertEqual(b1, b2)

    def test_struck_guard_absent(self):
        self.assertFalse(
            hasattr(benchmark_exp091, "verify_against_instance_records"),
            "struck guard resurrected in EXP091")

    def test_archive_pin_passes_on_real_archive(self):
        got = assert_archive_hash()
        self.assertEqual(got, ARCHIVE_PROVENANCE_HASH)
        self.assertEqual(
            got,
            "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585")

    def test_archive_pin_refuses_on_tampered_archive(self):
        with tempfile.TemporaryDirectory() as d:
            tampered = os.path.join(d, "exp077_instance_records.json")
            with open(tampered, "w") as f:
                json.dump([{"ent": "X", "typ": "planet"}], f)
            old = benchmark_exp091.artifacts_dir
            benchmark_exp091.artifacts_dir = lambda: d
            try:
                with self.assertRaises(benchmark_exp091.RunInvalid):
                    assert_archive_hash()
            finally:
                benchmark_exp091.artifacts_dir = old

    def test_provenance_pin_fires_in_mock_pipeline(self):
        with tempfile.TemporaryDirectory() as d:
            tampered = os.path.join(d, "exp077_instance_records.json")
            with open(tampered, "w") as f:
                json.dump([{"ent": "X", "typ": "planet"}], f)
            old = benchmark_exp091.artifacts_dir
            benchmark_exp091.artifacts_dir = lambda: d
            try:
                with tempfile.TemporaryDirectory() as out:
                    with self.assertRaises(ExtractRunInvalid):
                        extract_mock(out)
                    self.assertFalse(
                        os.path.exists(os.path.join(out, "exp091_embeddings.npz")),
                        "embeddings written despite provenance-pin failure")
            finally:
                benchmark_exp091.artifacts_dir = old

    def test_phrasing_balance_30_30(self):
        n_a, n_c = assert_phrasing_balance(build_benchmark())
        self.assertEqual((n_a, n_c), (30, 30))

    def test_state_text_excludes_question(self):
        for b in build_benchmark():
            s = state_text_of(b["prompt"])
            self.assertTrue(s.startswith("Premise:"))
            self.assertNotIn("Question:", s)
            self.assertNotIn("Answer:", s)


class TestG1Prime(unittest.TestCase):
    """G1' — in-context single-token verification (THE design change vs EXP090).

    verify_g1_prime EXECUTES a tokenizer (never word-commonness reasoning).
    Here the HF interface is implemented by FakeTokenizer (numpy-only); the
    real-tokenizer execution is recorded in g1prime_verification.json at build
    time and re-verified below.
    """

    def test_verify_passes_all_single_token(self):
        table = verify_g1_prime(FakeTokenizer())
        total_occ = sum(v["occurrences"] for v in table.values())
        total_single = sum(v["single_token"] for v in table.values())
        self.assertEqual(total_occ, 240)
        self.assertEqual(total_single, 240)

    def test_per_entity_counts_match_registered_table(self):
        # Pins the signed-protocol §6 table in code: any bench drift changes
        # these counts and breaks the registration.
        table = verify_g1_prime(FakeTokenizer())
        for name, want in REGISTERED_G1PRIME_COUNTS.items():
            self.assertEqual(table[name]["occurrences"], want, name)
            self.assertEqual(table[name]["single_token"], want, name)

    def test_negative_multitoken_span_fails_loud(self):
        # A multi-token entity span in-prompt → RUN-INVALID (never silent).
        with self.assertRaises(benchmark_exp091.RunInvalid) as cm:
            verify_g1_prime(FakeTokenizer(split_words=("Mars",)))
        self.assertIn("G1' FAIL", str(cm.exception))

    def test_negative_unstable_token_id_fails(self):
        # Same surface form mapping to different token ids → RUN-INVALID.
        with self.assertRaises(benchmark_exp091.RunInvalid):
            verify_g1_prime(FakeTokenizer(flip_words=("Steel",)))

    def test_action_text_of_is_spaced_form(self):
        self.assertEqual(action_text_of("Mars"), " Mars")
        self.assertEqual(action_text_of("Steel"), " Steel")

    def test_action_texts_single_token_assert_passes(self):
        ids = guard_g1_prime_action_texts(FakeTokenizer().encode)
        self.assertEqual(len(ids), 10)
        self.assertEqual(set(ids.keys()), set(ALL_ENTITIES))

    def test_action_texts_multitoken_assert_fails(self):
        def bad_encode(t):
            return [1, 2] if t.strip() == "Mars" else [1]
        with self.assertRaises(ExtractRunInvalid) as cm:
            guard_g1_prime_action_texts(bad_encode)
        self.assertIn("G1' FAIL", str(cm.exception))

    def test_build_time_artifact_present_and_consistent(self):
        # The real-tokenizer build-time execution is recorded and bound to
        # the current bench: 240/240, verdict SATISFIED, hash matches.
        artifact = check_g1prime_artifact()
        self.assertEqual(artifact["occurrences_total"], 240)
        self.assertEqual(artifact["occurrences_single_token"], 240)
        self.assertEqual(artifact["verdict"], "G1' SATISFIED")
        self.assertEqual(artifact["bench_sha256"], bench_sha256())
        for name, want_id in REGISTERED_G1PRIME_IDS.items():
            self.assertEqual(
                artifact["per_entity"][name]["token_id"], want_id, name)

    def test_tampered_artifact_refuses(self):
        with tempfile.TemporaryDirectory() as d:
            bad = os.path.join(d, "g1prime_verification.json")
            with open(bad, "w") as f:
                json.dump({"occurrences_total": 240,
                           "occurrences_single_token": 239,
                           "verdict": "G1' SATISFIED",
                           "bench_sha256": bench_sha256()}, f)
            with self.assertRaises(benchmark_exp091.RunInvalid):
                check_g1prime_artifact(path=bad)

    def test_stale_artifact_bench_mismatch_refuses(self):
        with tempfile.TemporaryDirectory() as d:
            stale = os.path.join(d, "g1prime_verification.json")
            with open(stale, "w") as f:
                json.dump({"occurrences_total": 240,
                           "occurrences_single_token": 240,
                           "verdict": "G1' SATISFIED",
                           "bench_sha256": "0" * 64}, f)
            with self.assertRaises(benchmark_exp091.RunInvalid):
                check_g1prime_artifact(path=stale)

    def test_mock_requires_valid_g1prime_artifact(self):
        # --mock re-verifies the build-time artifact: a tampered artifact
        # aborts extraction before any embedding is written.
        with tempfile.TemporaryDirectory() as d:
            bad = os.path.join(d, "g1prime_verification.json")
            with open(bad, "w") as f:
                json.dump({"occurrences_total": 240,
                           "occurrences_single_token": 239,
                           "verdict": "G1' SATISFIED",
                           "bench_sha256": bench_sha256()}, f)
            old = benchmark_exp091._bundle_dir
            benchmark_exp091._bundle_dir = lambda: d
            try:
                with tempfile.TemporaryDirectory() as out:
                    with self.assertRaises(ExtractRunInvalid):
                        extract_mock(out)
                    self.assertFalse(
                        os.path.exists(
                            os.path.join(out, "exp091_embeddings.npz")),
                        "embeddings written despite G1' artifact failure")
            finally:
                benchmark_exp091._bundle_dir = old


class TestVerdictBoundaries(unittest.TestCase):
    def test_continue_38_clean(self):
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
        r = adjudicate(*_synthetic_case(19, 18))
        self.assertEqual(r["verdict"], "KILL")

    def test_kill_0(self):
        r = adjudicate(*_synthetic_case(0, 0))
        self.assertEqual(r["verdict"], "KILL")

    def test_kill_30(self):
        r = adjudicate(*_synthetic_case(15, 15))
        self.assertEqual(r["verdict"], "KILL")

    def test_pivot_split_exactly_half(self):
        r = adjudicate(*_synthetic_case(15, 23))
        self.assertEqual(r["n_correct"], 38)
        self.assertEqual(r["verdict"], "PIVOT")

    def test_pivot_opposite_tilts(self):
        r = adjudicate(*_synthetic_case(12, 26))
        self.assertEqual(r["verdict"], "PIVOT")

    def test_pivot_one_split_below_half(self):
        r = adjudicate(*_synthetic_case(14, 26))
        self.assertEqual(r["n_correct"], 40)
        self.assertEqual(r["verdict"], "PIVOT")

    def test_bar_sharpness_registered_values(self):
        p38 = exact_binomial_upper_tail(38)
        self.assertEqual(round(p38, 3), 0.026)
        self.assertEqual(round(p38, 4), 0.0259)
        self.assertEqual(round(exact_binomial_upper_tail(37), 4), 0.0462)
        p = sum(math.comb(60, k) for k in range(38, 61)) / 2 ** 60
        self.assertAlmostEqual(p38, p, places=12)


class TestInstrumentGate(unittest.TestCase):
    def test_g4_deaf_instrument_run_invalid(self):
        correct = [False] * 60
        phrasing = ["A-first"] * 30 + ["C-first"] * 30
        cosines = np.full(120, 0.5)
        with self.assertRaises(ScoreRunInvalid):
            adjudicate(correct, phrasing, cosines)

    def test_g4_healthy_instrument_passes(self):
        correct, phrasing, cos = _synthetic_case(20, 18)
        r = adjudicate(correct, phrasing, cos)
        self.assertEqual(r["verdict"], "CONTINUE")

    def test_tie_breaks_toward_foil(self):
        n = 60
        state = np.eye(3, dtype=np.float32)
        s = np.tile(state[0], (n, 1))
        a = np.tile(state[1], (n, 1))
        c = np.tile(state[1], (n, 1))
        phrasing = np.array(["A-first"] * 30 + ["C-first"] * 30)
        ids = np.array([f"item_{i}" for i in range(n)])
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.npz")
            np.savez(p, state=s, actA=a, actC=c, ids=ids, phrasing=phrasing)
            with self.assertRaises(ScoreRunInvalid):
                decide_from_embeddings(p)

    def test_tie_counted_when_instrument_healthy(self):
        n = 60
        rng = np.random.default_rng(7)
        s = rng.normal(size=(n, 8)).astype(np.float32)
        a = rng.normal(size=(n, 8)).astype(np.float32)
        c = rng.normal(size=(n, 8)).astype(np.float32)
        a[0] = c[0]
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
            self.assertFalse(r["per_item"][0]["correct"])


class TestGuards(unittest.TestCase):
    def test_g1_legacy_multitoken_refuses(self):
        with self.assertRaises(ExtractRunInvalid):
            check_single_token_entity(lambda t: [1, 2], "Mars", "target")

    def test_g1_legacy_singletoken_passes(self):
        self.assertEqual(
            check_single_token_entity(lambda t: [42], "Mars", "target"), 42)

    def test_g2_hash_mismatch_refuses(self):
        fake = {"w": np.ones((4, 4), dtype=np.float32)}
        with self.assertRaises(ExtractRunInvalid):
            guard_state_dict_hash(fake, "test")

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
            self.assertEqual(run_exp091.main(["--out-dir", d]), 2)

    def test_refuses_forbidden_flags(self):
        with tempfile.TemporaryDirectory() as d:
            for flag in ("--gpu", "--train", "--cuda", "--finetune"):
                self.assertEqual(
                    run_exp091.main(["--out-dir", d, "--mock", flag]), 2,
                    f"flag {flag} was not refused")

    def test_signed_protocol_digest_guard_passes(self):
        self.assertTrue(run_exp091.assert_signed_protocol())

    def test_mock_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            rc = run_exp091.main(["--out-dir", d, "--mock"])
            self.assertEqual(rc, 0)
            rp = os.path.join(d, "exp091_report.json")
            self.assertTrue(os.path.isfile(rp))
            with open(rp) as f:
                report = json.load(f)
            self.assertIn(report["verdict"], ("CONTINUE", "KILL", "PIVOT"))
            self.assertEqual(report["n_total"], 60)
            self.assertTrue(os.path.isfile(
                os.path.join(d, "exp091_embeddings.npz")))


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
        p = os.path.join(d, "exp091_embeddings.npz")
        np.savez(p, state=s, actA=a, actC=c, ids=ids, phrasing=phrasing)
        if mode is not None:
            with open(os.path.join(d, "exp091_extraction_meta.json"), "w") as f:
                json.dump({"mode": mode}, f)
        return p

    def test_scorer_main_stamps_mock_mode(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._bundle(d, mode="mock")
            out = os.path.join(d, "out")
            rc = score_main(["--embeddings", p, "--out-dir", out])
            self.assertEqual(rc, 0)
            with open(os.path.join(out, "exp091_report.json")) as f:
                rep = json.load(f)
            self.assertEqual(rep["mode"], "mock")

    def test_scorer_main_stamps_unknown_without_meta(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._bundle(d, mode=None)
            out = os.path.join(d, "out")
            rc = score_main(["--embeddings", p, "--out-dir", out])
            self.assertEqual(rc, 0)
            with open(os.path.join(out, "exp091_report.json")) as f:
                rep = json.load(f)
            self.assertEqual(rep["mode"], "unknown")

    def test_runner_mock_stamps_mock_mode(self):
        with tempfile.TemporaryDirectory() as d:
            rc = run_main(["--out-dir", d, "--mock"])
            self.assertEqual(rc, 0)
            with open(os.path.join(d, "exp091_report.json")) as f:
                rep = json.load(f)
            self.assertEqual(rep["mode"], "mock")


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
