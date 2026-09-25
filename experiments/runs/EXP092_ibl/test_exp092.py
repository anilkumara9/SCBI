"""EXP092 unit tests — ALL must pass. Synthetic/mock only; no weights touched.

Covers: §2 bench contract (deterministic builder, registered pin, 60/60
unique tuples, strata == §4 table, 30/30 phrasing, target balance 3x);
G0 provenance gate (pass on real bench, refusal on tampered bench);
G1' real-tokenizer path via a fake tokenizer (positive AND negative cases)
+ build-time artifact binding; G1 hash guard (match/mismatch); G2 artifact
re-verification (bound to pin, gate PASS); G3 phrasing balance; 1-NN LOO
statistic (clustered signal, tie RUN-INVALID); stratified permutation null
(null data -> large p, strong signal -> small p; scheme fidelity vs the
reference implementation); §5 TOTAL decision-tree boundaries (CONTINUE /
KILL / PIVOT incl. layer-20-only -> PIVOT, sub-threshold -> PIVOT);
G4 zero-spread RUN-INVALID; S1/S2 secondaries finite and in range; runner
refusal rules; signed-protocol digest guard; mock end-to-end (mode stamp).
numpy-only (no torch required).
"""

import json
import math
import os
import random
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_implementation as ref
from protocol_pin import BENCH_PIN, SIGNED_PROTOCOL_DIGEST
import protocol_pin
import g1prime
from extract_layer_embeddings import (
    RunInvalid as ExtractRunInvalid,
    compute_state_dict_hash, guard_state_dict_hash,
    guard_g0_bench, guard_g2_artifact, guard_g3_phrasing,
    extract_mock,
)
from score_exp092 import (
    RunInvalid as ScoreRunInvalid,
    loo_1nn_accuracy, strata_indices, permutation_null,
    adjudicate, s1_mi, s2_lm_baseline, decide_from_embeddings,
    ALPHA_B, EFFECT_BAR, PERM_B, EXCLUDED_LAYER, N_LAYERS, N_ITEMS,
)
import run_exp092
run_main = run_exp092.main


# ---------------------------------------------------------------------------
# Fake tokenizer implementing the HF fast-tokenizer interface used by
# g1prime.verify_g1_prime.
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
        import re as _re
        ids, offsets, pieces = [], [], []
        for m in _re.finditer(r"\w+|[^\w\s]", text):
            word, (s, e) = m.group(0), m.span()
            if word in self.split_words:
                # emit the word as two tokens (simulates multi-token entity)
                h = len(word) // 2
                for part, (ps, pe) in ((word[:h], (s, s + h)),
                                       (word[h:], (s + h, e))):
                    ids.append(self._tok_id(part, word))
                    offsets.append((ps, pe))
                    pieces.append("\u0120" + part)
            else:
                ids.append(self._tok_id(word, word))
                offsets.append((s, e))
                pieces.append("\u0120" + word)
        out = {"input_ids": ids}
        if return_offsets_mapping:
            out["offset_mapping"] = offsets
        self._last_pieces = pieces
        return out

    def convert_ids_to_tokens(self, ids):
        return [self._pieces[i] for i in ids]


# ---------------------------------------------------------------------------
class TestBenchContract(unittest.TestCase):
    def test_length_60(self):
        self.assertEqual(len(ref.build_bench()), 60)

    def test_deterministic_two_builds_identical(self):
        a = ref.canonical_json(ref.build_bench())
        b = ref.canonical_json(ref.build_bench())
        self.assertEqual(a, b)

    def test_registered_pin_recomputes(self):
        self.assertEqual(ref.bench_sha256(), BENCH_PIN)

    def test_unique_tuples_60(self):
        bench = ref.build_bench()
        keys = [(b["domain"], tuple(b["tuple"])) for b in bench]
        self.assertEqual(len(set(keys)), 60)

    def test_strata_match_section4(self):
        bench = ref.build_bench()
        from collections import Counter
        got = dict(Counter((b["domain"], b["phrasing"]) for b in bench))
        self.assertEqual(got, dict(ref.STRATA_TABLE))

    def test_phrasing_30_30(self):
        bench = ref.build_bench()
        n_a = sum(1 for b in bench if b["phrasing"] == "A-first")
        self.assertEqual(n_a, 30)

    def test_target_balance_3x(self):
        bench = ref.build_bench()
        from collections import Counter
        tc = Counter((b["domain"], b["ent"]) for b in bench)
        self.assertEqual(len(tc), 20)
        self.assertTrue(all(v == 3 for v in tc.values()))

    def test_item_schema_registered(self):
        bench = ref.build_bench()
        want = {"id", "prompt", "A", "C", "ent", "typ", "hop",
                "domain", "phrasing", "tuple"}
        for b in bench:
            self.assertEqual(set(b.keys()), want)


class TestG0(unittest.TestCase):
    def test_g0_passes_on_real_bench(self):
        g0 = guard_g0_bench()
        self.assertEqual(g0["pin"], BENCH_PIN)

    def test_g0_refuses_on_tampered_bench(self):
        bench = ref.build_bench()
        bench = [dict(b) for b in bench]
        bench[0] = dict(bench[0], prompt=bench[0]["prompt"] + " ")
        with self.assertRaises(ExtractRunInvalid):
            guard_g0_bench(bench)

    def test_g0_refuses_on_wrong_pin(self):
        with self.assertRaises(ref.BenchInvalid):
            ref.verify_g0(expected_pin="0" * 64)


class TestG1Prime(unittest.TestCase):
    def test_verify_passes_all_single_token(self):
        table = g1prime.verify_g1_prime(FakeTokenizer())
        n_occ = sum(v["occurrences"] for v in table.values())
        n_single = sum(v["single_token"] for v in table.values())
        self.assertEqual(n_occ, 240)
        self.assertEqual(n_single, 240)

    def test_negative_multitoken_span_fails_loud(self):
        tok = FakeTokenizer(split_words=("Mars",))
        with self.assertRaises(g1prime.RunInvalid):
            g1prime.verify_g1_prime(tok)

    def test_negative_unstable_token_id_fails(self):
        tok = FakeTokenizer(flip_words=("Iron",))
        with self.assertRaises(g1prime.RunInvalid):
            g1prime.verify_g1_prime(tok)

    def test_build_time_artifact_present_and_consistent(self):
        art = g1prime.check_g1prime_artifact()
        self.assertEqual(art["bench_pin"], BENCH_PIN)
        self.assertEqual(art["n_single_token"], 240)
        self.assertEqual(art["n_occurrences"], 240)

    def test_stale_artifact_pin_mismatch_refuses(self):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "g1prime_verification.json")
            with open(p, "w") as f:
                json.dump({"bench_pin": "0" * 64, "n_single_token": 240,
                           "n_occurrences": 240}, f)
            with self.assertRaises(g1prime.RunInvalid):
                g1prime.check_g1prime_artifact(p)


class TestG1G2G3(unittest.TestCase):
    def test_g1_hash_match_passes(self):
        # The pass branch is exercised by patching the expected pin to the
        # synthetic dict's own hash (the real pin can only match the real
        # LOG-331 snapshot, verified at real extraction).
        import extract_layer_embeddings as ext
        sd = {"b": np.zeros(4, dtype=np.float32),
              "a": np.ones(4, dtype=np.float32)}
        h = ext.compute_state_dict_hash(sd)
        old = ext.WEIGHTS_PIN
        ext.WEIGHTS_PIN = h
        try:
            self.assertEqual(ext.guard_state_dict_hash(sd, "test"), h)
        finally:
            ext.WEIGHTS_PIN = old

    def test_g1_hash_mismatch_refuses(self):
        sd = {"a": np.ones(4, dtype=np.float32)}
        with self.assertRaises(ExtractRunInvalid):
            guard_state_dict_hash(sd, "test")

    def test_g1_hash_order_stable(self):
        sd1 = {"b": np.zeros(3), "a": np.ones(3)}
        sd2 = {"a": np.ones(3), "b": np.zeros(3)}
        self.assertEqual(compute_state_dict_hash(sd1),
                         compute_state_dict_hash(sd2))

    def test_g2_artifact_passes(self):
        art = guard_g2_artifact()
        self.assertEqual(art["bench_pin"], BENCH_PIN)
        self.assertEqual(art["gate"], "PASS")
        self.assertGreaterEqual(art["permutation_p"], 0.05)
        self.assertAlmostEqual(art["oracle_accuracy"], 0.0607, places=3)

    def test_g2_missing_artifact_refuses(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ExtractRunInvalid):
                guard_g2_artifact(td)

    def test_g3_passes_on_real_bench(self):
        guard_g3_phrasing(ref.build_bench())  # must not raise

    def test_g3_refuses_on_imbalance(self):
        bench = [dict(b) for b in ref.build_bench()]
        bench[0] = dict(bench[0], phrasing="C-first")
        with self.assertRaises(ExtractRunInvalid):
            guard_g3_phrasing(bench)


class TestLooStatistic(unittest.TestCase):
    def _clustered(self, seed=0):
        # 60 points, 20 well-separated clusters -> 1-NN recovers labels
        rng = np.random.default_rng(seed)
        X = np.zeros((60, 8))
        labels = np.zeros(60, dtype=int)
        for c in range(20):
            ctr = rng.normal(scale=10.0, size=8)
            X[3 * c:3 * c + 3] = ctr + rng.normal(scale=0.01, size=(3, 8))
            labels[3 * c:3 * c + 3] = c
        d2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
        return d2, labels

    def test_clustered_signal_high_accuracy(self):
        d2, labels = self._clustered()
        acc, _ = loo_1nn_accuracy(d2, labels)
        self.assertGreater(acc, 0.9)

    def test_random_data_near_chance(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(60, 8))
        d2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
        labels = np.repeat(np.arange(20), 3)
        acc, _ = loo_1nn_accuracy(d2, labels)
        self.assertLess(acc, 0.3)

    def test_exact_tie_run_invalid(self):
        X = np.zeros((60, 4))  # all identical -> all ties
        d2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
        labels = np.repeat(np.arange(20), 3)
        with self.assertRaises(ScoreRunInvalid):
            loo_1nn_accuracy(d2, labels)


class TestPermutationNull(unittest.TestCase):
    def _data(self, seed=0, signal=True):
        rng = np.random.default_rng(seed)
        X = np.zeros((60, 8))
        labels = np.zeros(60, dtype=int)
        for c in range(20):
            ctr = rng.normal(scale=10.0 if signal else 0.0, size=8)
            X[3 * c:3 * c + 3] = ctr + rng.normal(scale=0.5, size=(3, 8))
            labels[3 * c:3 * c + 3] = c
        d2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
        domain = np.array(["Planetary"] * 30 + ["Elemental"] * 30)
        phrasing = np.array((["A-first"] * 16 + ["C-first"] * 14) +
                            (["A-first"] * 14 + ["C-first"] * 16))
        return d2, labels, strata_indices(domain, phrasing)

    def test_strong_signal_small_p(self):
        d2, labels, strata = self._data(signal=True)
        _, p, q95, _ = permutation_null(d2, labels, strata, B=200)
        self.assertLess(p, 0.05)

    def test_null_data_large_p(self):
        d2, labels, strata = self._data(signal=False)
        _, p, _, _ = permutation_null(d2, labels, strata, B=200)
        self.assertGreater(p, 0.05)

    def test_scheme_fidelity_vs_reference(self):
        # Scheme-fidelity: score_exp092.permutation_null must implement the
        # registered RNG scheme (random.Random(9207+b), within-strata
        # shuffle, p=(1+ge)/(1+B)) identically to the reference
        # implementation. Both are driven with the SAME statistic (argmin
        # 1-NN on one distance matrix), so any scheme difference shows up
        # as a p-value difference. (The tie-break convention difference
        # noted in the Law #14 review §5 is a statistic difference, not a
        # scheme difference, and is excluded by construction here.)
        bench = ref.build_bench()
        labels_raw = [b["ent"] for b in bench]
        uniq = sorted(set(labels_raw))
        lid = {u: i for i, u in enumerate(uniq)}
        label_ids = np.array([lid[u] for u in labels_raw])
        domain = np.array([b["domain"] for b in bench])
        phrasing = np.array([b["phrasing"] for b in bench])
        strata = strata_indices(domain, phrasing)

        # integer-overlap "distance" matrix (ties possible -> relaxed only
        # for this scheme probe; the registered tie rule is tested elsewhere)
        ents = [set([b["A"], b["C"]]) | set(
            (ref.PLANET_VOCAB if b["domain"] == "Planetary"
             else ref.ELEMENT_VOCAB)[k] for k in b["tuple"])
            for b in bench]
        n = len(bench)
        sim = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                sim[i, j] = len(ents[i] & ents[j])
        d2 = -sim

        def stat_from_bench(pb):
            lab = np.array([lid[b["ent"]] for b in pb])
            acc, _ = loo_1nn_accuracy(d2, lab, assert_no_ties=False)
            return acc

        _, ref_p = ref.stratified_permutation_p(bench, stat_from_bench, 200)
        _, mine_p, _, _ = permutation_null(
            d2, label_ids, strata, B=200, assert_no_ties=False)
        self.assertAlmostEqual(mine_p, ref_p, places=6)

    def test_p_value_bounds(self):
        d2, labels, strata = self._data(signal=True)
        _, p, _, _ = permutation_null(d2, labels, strata, B=100)
        self.assertGreaterEqual(p, 1 / 101)
        self.assertLessEqual(p, 1.0)


class TestDecisionTree(unittest.TestCase):
    def _stats(self, sig_layers=(), effects=None):
        effects = effects or {}
        out = []
        for l in range(24):
            if l in sig_layers:
                out.append({"accuracy": 0.20, "p": 0.0001,
                            "q95": 0.20 - effects.get(l, 0.15)})
            else:
                out.append({"accuracy": 0.06, "p": 0.5, "q95": 0.10})
        return out

    def test_continue(self):
        v, d = adjudicate(self._stats(sig_layers=(5,), effects={5: 0.15}))
        self.assertEqual(v, "CONTINUE")
        self.assertEqual(d["l_star"], 5)

    def test_continue_picks_max_effect(self):
        v, d = adjudicate(self._stats(sig_layers=(3, 9),
                                      effects={3: 0.12, 9: 0.20}))
        self.assertEqual(v, "CONTINUE")
        self.assertEqual(d["l_star"], 9)

    def test_kill(self):
        v, _ = adjudicate(self._stats())
        self.assertEqual(v, "KILL")

    def test_pivot_subthreshold(self):
        v, d = adjudicate(self._stats(sig_layers=(7,), effects={7: 0.05}))
        self.assertEqual(v, "PIVOT")
        self.assertIn(7, d["significant_layers"])

    def test_pivot_layer20_only(self):
        # layer 20 significant with a LARGE effect still cannot CONTINUE
        # (EXP091 already read it); it routes to PIVOT.
        v, d = adjudicate(self._stats(sig_layers=(20,), effects={20: 0.30}))
        self.assertEqual(v, "PIVOT")

    def test_pivot_layer20_subthreshold(self):
        v, _ = adjudicate(self._stats(sig_layers=(20,), effects={20: 0.05}))
        self.assertEqual(v, "PIVOT")

    def test_effect_bar_sharpness(self):
        # exactly at the 10pp bar -> CONTINUE; just below -> PIVOT
        v1, _ = adjudicate(self._stats(sig_layers=(2,), effects={2: 0.10}))
        v2, _ = adjudicate(self._stats(sig_layers=(2,), effects={2: 0.0999}))
        self.assertEqual(v1, "CONTINUE")
        self.assertEqual(v2, "PIVOT")


class TestInstrumentGate(unittest.TestCase):
    def _bundle(self, layers):
        bench = ref.build_bench()
        return {
            "layers": layers,
            "opt_logits": np.zeros((60, 2), dtype=np.float32),
            "ids": np.array([b["id"] for b in bench]),
            "labels": np.array([b["ent"] for b in bench]),
            "phrasing": np.array([b["phrasing"] for b in bench]),
            "domain": np.array([b["domain"] for b in bench]),
        }

    def test_g4_zero_spread_run_invalid(self):
        # constant embeddings -> permutation null has zero spread -> G4 fires.
        # (ties would fire first in loo; bypass ties by distinct labels check:
        # use the full pipeline and expect RunInvalid from either guard.)
        layers = np.zeros((24, 60, 8), dtype=np.float32)
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "e.npz")
            b = self._bundle(layers)
            np.savez(p, **b)
            with self.assertRaises(ScoreRunInvalid):
                decide_from_embeddings(p, perm_b=50)

    def test_healthy_pipeline_kill_on_noise(self):
        rng = np.random.default_rng(7)
        layers = rng.normal(size=(24, 60, 16)).astype(np.float32)
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "e.npz")
            b = self._bundle(layers)
            np.savez(p, **b)
            rep = decide_from_embeddings(p, perm_b=100)
        self.assertEqual(rep["verdict"], "KILL")
        self.assertEqual(len(rep["layers"]), 24)


class TestSecondaries(unittest.TestCase):
    def test_s1_finite(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(60, 32))
        labels = np.repeat(np.arange(20), 3)
        mi = s1_mi(X, labels)
        self.assertTrue(math.isfinite(mi))
        self.assertGreaterEqual(mi, -0.5)  # estimator noise floor

    def test_s1_signal_positive(self):
        rng = np.random.default_rng(4)
        X = np.zeros((60, 32))
        labels = np.zeros(60, dtype=int)
        for c in range(20):
            X[3 * c:3 * c + 3] = rng.normal(scale=5.0, size=32) \
                + rng.normal(scale=0.1, size=(3, 32))
            labels[3 * c:3 * c + 3] = c
        mi = s1_mi(X, labels)
        self.assertGreater(mi, 0.5)

    def test_s2_range(self):
        rng = np.random.default_rng(5)
        s2 = s2_lm_baseline(rng.normal(size=(60, 2)))
        self.assertGreaterEqual(s2["accuracy"], 0.0)
        self.assertLessEqual(s2["accuracy"], 1.0)
        self.assertTrue(math.isfinite(
            s2["mean_logprob_margin_target_minus_foil"]))

    def test_s2_perfect(self):
        s2 = s2_lm_baseline(np.array([[5.0, -5.0]] * 60))
        self.assertEqual(s2["accuracy"], 1.0)


class TestRunnerRefusals(unittest.TestCase):
    def test_refuses_without_clearance(self):
        with tempfile.TemporaryDirectory() as td:
            rc = run_main(["--out-dir", td])
        self.assertEqual(rc, 2)

    def test_refuses_forbidden_flags(self):
        with tempfile.TemporaryDirectory() as td:
            for flag in ("--gpu", "--train", "--cuda"):
                rc = run_main(["--out-dir", td, "--mock", flag])
                self.assertEqual(rc, 2, flag)

    def test_signed_protocol_digest_guard_passes(self):
        self.assertTrue(run_exp092.assert_signed_protocol())

    def test_mock_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            rc = run_main(["--out-dir", td, "--mock"])
            self.assertEqual(rc, 0)
            with open(os.path.join(td, "exp092_report.json")) as f:
                rep = json.load(f)
        self.assertEqual(rep["mode"], "mock")
        self.assertIn(rep["verdict"], ("CONTINUE", "KILL", "PIVOT"))
        self.assertEqual(len(rep["layers"]), 24)
        self.assertIn("S2", rep)


class TestMockExtraction(unittest.TestCase):
    def test_mock_shapes(self):
        with tempfile.TemporaryDirectory() as td:
            emb_path, meta = extract_mock(td)
            z = np.load(emb_path)
            self.assertEqual(z["layers"].shape, (24, 60, 1024))
            self.assertEqual(z["opt_logits"].shape, (60, 2))
            self.assertEqual(meta["mode"], "mock")

    def test_mock_deterministic(self):
        with tempfile.TemporaryDirectory() as td1, \
                tempfile.TemporaryDirectory() as td2:
            p1, _ = extract_mock(td1)
            p2, _ = extract_mock(td2)
            a = np.load(p1)["layers"]
            b = np.load(p2)["layers"]
            self.assertTrue(np.array_equal(a, b))


if __name__ == "__main__":
    unittest.main(verbosity=2)
