"""EXP093 unit tests — numpy-only (+ fake model pieces). No torch, no weights.

Covers: direction construction (incl. the v0.1 degeneracy regression),
registered measurements on the real archived .npz (read-only), McNemar exact
values, the §5 TOTAL decision tree on all six verdict scenarios, the tie
rule, G5 mock verification (+ misplacement failure), the PENDING-SIGNATURE
launch-chain gate, forbidden flags, and the --mock end-to-end path.

NOTE: torch-requiring tests live in test_exp093_hook_order.py (LOG-4349
regression). This module must stay torch-free: test_mock_end_to-end asserts
the mock path never imports torch.
"""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr

import numpy as np

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
sys.path.append(os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))

import protocol_pin as pin
import reference_implementation as ref
from direction_builder import build_directions, REGISTERED
from direction_builder import RunInvalid as BuilderRunInvalid
from inject import (MockCausalModel, verify_g5, verify_g5_mock, ALPHA,
                    G5_REL_TOL, G5_ABS_TOL)
from inject import RunInvalid as InjectRunInvalid
from score_exp093 import (mcnemar_exact_p, score_conditions,
                          RunInvalid as ScorerRunInvalid)
import run_exp093


def margins_from_correct(correct):
    return np.where(np.asarray(correct, dtype=bool), 1.0, -1.0)


def phrasing_30_30():
    return np.array(["A-first"] * 30 + ["C-first"] * 30)


def synthetic_class_data(seed=7, n=60, dim=1024, nclass=20):
    rng = np.random.default_rng(seed)
    labels = [f"cls{k % nclass}" for k in range(n)]
    means = {f"cls{k}": rng.normal(size=dim) for k in range(nclass)}
    X = np.stack([means[labels[i]] + 0.3 * rng.normal(size=dim)
                  for i in range(n)]).astype(np.float32)
    return X, labels


class TestDirectionBuilder(unittest.TestCase):
    def test_construction_synthetic(self):
        X, labels = synthetic_class_data()
        d = build_directions(X, labels)
        self.assertTrue(np.all(d["r_norms"] > 1e-9))
        self.assertTrue(d["all_unit_norm"])
        self.assertTrue(d["r4_not_bit_identical"])
        self.assertIn("mean_pairwise_cosine_u", d)
        self.assertLessEqual(d["prenorm_min"], d["prenorm_max"])

    def test_v01_degeneracy_regression(self):
        """The v0.1 formula (mean of UNNORMALIZED residuals) is identically
        zero — the LOG-4340 defect. The v0.2 construction must be
        non-degenerate on the same data (error-preservation standard)."""
        X, labels = synthetic_class_data()
        X64 = X.astype(np.float64)
        lab = np.array(labels)
        max_norm = 0.0
        for i in range(60):
            tot = np.zeros(X64.shape[1])
            for j in range(60):
                if j == i:
                    continue
                mask = (lab == lab[j])
                mask[i] = False
                mask[j] = False
                c = X64[mask].mean(axis=0)
                tot += c - X64[j]
            max_norm = max(max_norm, float(np.linalg.norm(tot / 59)))
        self.assertLess(max_norm, 1e-9,
                        "v0.1 construction is NOT degenerate here — "
                        "regression test premise broken")
        d = build_directions(X, labels)
        self.assertGreater(d["min_r_norm"], 1e-9)

    def test_registered_measurements_real_npz(self):
        """Reviewer-verified numbers on the archived .npz (read-only)."""
        z = np.load(pin.npz_path(), allow_pickle=True)
        bench = ref.build_bench()
        d = build_directions(z["layers"][11], z["labels"],
                             [b["ent"] for b in bench])
        self.assertAlmostEqual(d["min_r_norm"], REGISTERED["min_r_norm"],
                               places=3)
        self.assertAlmostEqual(d["mean_pairwise_cosine_u"],
                               REGISTERED["mean_pairwise_cosine_u"], places=3)
        self.assertAlmostEqual(d["prenorm_min"], REGISTERED["prenorm_min"],
                               places=3)
        self.assertAlmostEqual(d["prenorm_max"], REGISTERED["prenorm_max"],
                               places=3)
        self.assertAlmostEqual(d["max_pairwise_cosine_v"],
                               REGISTERED["max_pairwise_cosine_v"], places=3)

    def test_label_mismatch_runinvalid(self):
        X, labels = synthetic_class_data()
        bad = list(labels)
        bad[0], bad[1] = bad[1], bad[0]
        with self.assertRaises(BuilderRunInvalid):
            build_directions(X, labels, bad)

    def test_degenerate_r_runinvalid(self):
        X = np.zeros((60, 1024), dtype=np.float32)  # all coincide w/ prototype
        labels = [f"cls{k % 20}" for k in range(60)]
        with self.assertRaises(BuilderRunInvalid):
            build_directions(X, labels)


class TestMcNemar(unittest.TestCase):
    def test_hand_values(self):
        # b=10, c=2: tail=(1+12+66)/4096=79/4096; p=158/4096
        self.assertAlmostEqual(mcnemar_exact_p(10, 2), 158 / 4096, places=12)
        self.assertEqual(mcnemar_exact_p(0, 0), 1.0)
        self.assertEqual(mcnemar_exact_p(5, 5), 1.0)  # capped
        # b=7, c=0: tail=1/128; p=1/64
        self.assertAlmostEqual(mcnemar_exact_p(7, 0), 1 / 64, places=12)
        # symmetry
        self.assertEqual(mcnemar_exact_p(3, 8), mcnemar_exact_p(8, 3))


class TestDecisionTree(unittest.TestCase):
    def _score(self, cB, cP, cN):
        ph = phrasing_30_30()
        return score_conditions(margins_from_correct(cB),
                                margins_from_correct(cP),
                                margins_from_correct(cN), ph)

    def test_continue(self):
        cB = np.array([i < 30 for i in range(60)])
        cP = cB.copy()
        cP[0] = False; cP[1] = False          # c=2 reversals
        for i in range(30, 42):
            cP[i] = True                        # b=12 flips
        cN = np.array([i < 25 for i in range(60)])
        r = self._score(cB, cP, cN)
        self.assertEqual(r["verdict"], "CONTINUE")
        d = r["verdict_detail"]["aggregate"]
        self.assertGreaterEqual(d["delta"], 0.10)
        self.assertLess(d["mcnemar_p"], 0.05)
        self.assertTrue(d["monotone"])

    def test_kill(self):
        cB = np.array([i < 30 for i in range(60)])
        cP = cB.copy(); cP[0] = False; cP[30] = True   # b=1, c=1 -> p=1
        cN = cB.copy(); cN[29] = False                # N-vs-B p=1
        r = self._score(cB, cP, cN)
        self.assertEqual(r["verdict"], "KILL")

    def test_pivot_a(self):
        # A-first (0..29) meets all three bars; C-first does not; aggregate p fails
        cB = np.array([i < 15 or 30 <= i < 45 for i in range(60)])
        cP = cB.copy()
        cP[0] = False                                # A: c=1
        for i in range(15, 23):
            cP[i] = True                             # A: b=8 -> p~0.039
        cP[30] = False; cP[31] = False               # C: c=2
        cP[45] = True; cP[46] = True                 # C: b=2 -> p=1
        cN = np.array([i < 12 or 30 <= i < 44 for i in range(60)])
        r = self._score(cB, cP, cN)
        self.assertEqual(r["verdict"], "PIVOT(a)")
        self.assertTrue(r["verdict_detail"]["A_first"]["bars"])
        self.assertFalse(r["verdict_detail"]["C_first"]["bars"])

    def test_pivot_b(self):
        # significant (p<0.05) but monotonicity fails -> forensics, not CONTINUE
        cB = np.array([i < 30 for i in range(60)])
        cP = cB.copy()
        for i in range(30, 37):
            cP[i] = True                             # b=7, c=0 -> p~0.0156
        cN = cB.copy()
        for i in range(30, 35):
            cN[i] = True                             # N=35 > B=30: mono fails
        r = self._score(cB, cP, cN)
        self.assertEqual(r["verdict"], "PIVOT(b)")

    def test_pivot_c(self):
        # C-first meets all three bars; aggregate p fails -> forensics
        cB = np.array([i < 15 or 30 <= i < 45 for i in range(60)])
        cP = cB.copy()
        cP[0] = False; cP[30] = False; cP[45] = True     # A: b=1,c=1; C: b=1,c=1
        for i in range(46, 54):
            cP[i] = True                                 # C: b=8,c=1 -> p~0.039
        cN = np.array([i < 15 or 30 <= i < 42 for i in range(60)])
        r = self._score(cB, cP, cN)
        self.assertEqual(r["verdict"], "PIVOT(c)")
        self.assertTrue(r["verdict_detail"]["C_first"]["bars"])

    def test_tie_rule(self):
        # exact ties are scored INCORRECT (strict inequality); one tie on a
        # 180 item-condition basis stays under the 5% RUN-INVALID bar.
        mB = np.where(np.arange(60) < 30, 1.0, -1.0)
        mB[59] = 0.0   # exact tie -> scored incorrect
        mP = np.ones(60)
        mN = -np.ones(60)
        r = score_conditions(mB, mP, mN, phrasing_30_30())
        self.assertEqual(r["verdict_detail"]["aggregate"]["acc_B"], 30 / 60)
        self.assertEqual(r["secondaries"]["tie_count"], 1)

    def test_tie_rate_runinvalid(self):
        mB = np.zeros(60); mP = np.zeros(60); mN = np.zeros(60)
        with self.assertRaises(ScorerRunInvalid):
            score_conditions(mB, mP, mN, phrasing_30_30())


class TestG5Mock(unittest.TestCase):
    def test_g5_mock_pass(self):
        model = MockCausalModel()
        v = np.random.default_rng(0).normal(size=1024)
        v /= np.linalg.norm(v)
        g5 = verify_g5_mock(model, 0, v, ALPHA)
        self.assertEqual(g5["gate"], "PASS")
        self.assertLessEqual(g5["criterion_i_rel_err"], G5_REL_TOL)
        self.assertLess(g5["criterion_ii_max_abs_change"], G5_ABS_TOL)
        self.assertTrue(g5["criterion_iii_bit_match"])

    def test_g5_misplaced_injection_fails(self):
        # inject at position 0 instead of the final position -> criterion (ii)
        model = MockCausalModel()
        v = np.random.default_rng(1).normal(size=1024)
        v /= np.linalg.norm(v)

        def resid_wrong_pos():
            r = model.layer11_residual(3)
            r[0, :] = r[0, :] + ALPHA * v   # WRONG position
            return r

        with self.assertRaises(InjectRunInvalid):
            verify_g5(lambda: model.layer11_residual(3),
                      resid_wrong_pos,
                      lambda: model.forward_logits(3, inject=None),
                      lambda: model.forward_logits(3, inject=None),
                      v, ALPHA, label="misplaced")


class TestLaunchChain(unittest.TestCase):
    def test_signed_protocol_verifies(self):
        """LOG-4343 signed digest verifies under the header's blanking rule."""
        self.assertNotEqual(pin.SIGNED_PROTOCOL_DIGEST, "PENDING-SIGNATURE")
        self.assertTrue(run_exp093.assert_signed_protocol())

    def test_tampered_signed_protocol_refused(self):
        """One flipped byte in the signed body breaks the digest -> refuse."""
        import shutil
        real_path = pin.signed_protocol_path()
        with tempfile.TemporaryDirectory() as td:
            copy = os.path.join(td, "signed_copy.md")
            shutil.copyfile(real_path, copy)
            with open(copy, "r+b") as f:
                f.seek(-100, 2)  # deep in the protocol body, not the header
                f.write(b"X" if f.read(1) != b"X" else b"Y")
            orig = pin.signed_protocol_path
            pin.signed_protocol_path = lambda: copy
            try:
                err = io.StringIO()
                with redirect_stderr(err):
                    self.assertFalse(run_exp093.assert_signed_protocol())
                self.assertIn("mismatch", err.getvalue().lower())
            finally:
                pin.signed_protocol_path = orig

    def test_clearance_still_required(self):
        """Signed, but real mode without --ceo-clearance -> exit 2, no guards."""
        with tempfile.TemporaryDirectory() as td:
            err = io.StringIO()
            with redirect_stderr(err):
                rc = run_exp093.main(["--out-dir", td])
            self.assertEqual(rc, 2)
            self.assertIn("--ceo-clearance", err.getvalue())

    def test_forbidden_flag_refused(self):
        with tempfile.TemporaryDirectory() as td:
            err = io.StringIO()
            with redirect_stderr(err):
                rc = run_exp093.main(["--out-dir", td, "--mock", "--gpu"])
            self.assertEqual(rc, 2)

    def test_mock_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            rc = run_exp093.main(["--out-dir", td, "--mock"])
            self.assertEqual(rc, 0)
            with open(os.path.join(td, "exp093_report.json")) as f:
                rep = json.load(f)
            self.assertEqual(rep["mode"], "mock")
            self.assertEqual(rep["run_meta"]["protocol_digest"],
                             pin.SIGNED_PROTOCOL_DIGEST)
            self.assertIn(rep["verdict"],
                          {"CONTINUE", "KILL", "PIVOT(a)", "PIVOT(b)",
                           "PIVOT(c)"})
            self.assertIn("G5", rep["guards"])
            self.assertIn("coherence", rep)
            self.assertTrue(os.path.isfile(
                os.path.join(td, "exp093_run_log.txt")))
        self.assertNotIn("torch", sys.modules,
                         "mock path must not import torch (0 model passes)")


class TestBenchReuse(unittest.TestCase):
    def test_bench_pin(self):
        bench = ref.build_bench()
        self.assertEqual(ref.bench_sha256(bench), pin.BENCH_PIN)
        self.assertEqual(len(bench), 60)


if __name__ == "__main__":
    unittest.main(verbosity=2)
