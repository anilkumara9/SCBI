"""EXP093 G5 hook-ordering regression tests (LOG-4349) — torch required.

Separated from test_exp093.py because that module must stay torch-free
(test_mock_end_to_end asserts the mock path never imports torch).

LOG-4349: verify_g5_real registered the capture hook BEFORE the injection
hook's re-attach. PyTorch runs forward hooks in registration order with
chaining (each hook receives the previous hook's output), so the capture
always recorded the pre-injection residual and criterion (i) measured
rel_err == 1.0 exactly — the algebraic signature of a no-op capture, not a
misplaced injection.

The first test runs the REAL probe function (inject.verify_g5_real) against
a toy torch model (random init, no pretrained weights, no weight files):
it FAILS on the pre-LOG-4349 code and PASSES on the fixed code. The second
test pins the defect mechanism directly by replicating the old registration
order on a toy layer.
"""

import os
import sys
import unittest

import numpy as np

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)

import torch  # noqa: E402  (this module requires torch by design)

from inject import verify_g5_real, ALPHA, G5_REL_TOL, G5_ABS_TOL
from inject import RunInvalid as InjectRunInvalid


def _toy_model():
    from types import SimpleNamespace

    class ToyNeoX(torch.nn.Module):
        """Fake GPTNeoX: 12 linear 'layers' under gpt_neox.layers."""

        def __init__(self):
            super().__init__()
            self.gpt_neox = torch.nn.Module()
            self.gpt_neox.layers = torch.nn.ModuleList(
                [torch.nn.Linear(32, 32) for _ in range(12)])
            self.embed = torch.nn.Embedding(64, 32)
            self.readout = torch.nn.Linear(32, 64, bias=False)

        def forward(self, ids):
            h = self.embed(ids)
            for lyr in self.gpt_neox.layers:
                h = lyr(h)
            return SimpleNamespace(logits=self.readout(h))

    class FakeTokenizer:
        def encode(self, text, add_special_tokens=False):
            return [1, 2, 3, 4, 5]

    return ToyNeoX().eval(), FakeTokenizer()


class TestG5HookOrdering(unittest.TestCase):
    def test_verify_g5_real_observes_post_injection_residual(self):
        """The real probe passes on the fixed hook order (capture registered
        after the injection hook). Fails on the pre-LOG-4349 order."""
        model, tok = _toy_model()
        rng = np.random.default_rng(9349)
        v = rng.normal(size=32)
        v /= np.linalg.norm(v)
        g5 = verify_g5_real(model, tok, "toy prompt", v, ALPHA)
        self.assertEqual(g5["gate"], "PASS")
        self.assertLessEqual(g5["criterion_i_rel_err"], G5_REL_TOL)
        self.assertLess(g5["criterion_ii_max_abs_change"], G5_ABS_TOL)
        self.assertTrue(g5["criterion_iii_bit_match"])

    def test_capture_first_ordering_is_provably_blind(self):
        """Replicates the pre-LOG-4349 registration order (capture hook
        registered before the injection hook) on a toy layer and proves the
        defect mechanism: capture records the pre-injection residual, so
        criterion (i) yields rel_err == 1.0 exactly.

        Single-item batch (like the real probe): with batch B the no-op
        signature is sqrt(B); B=1 gives exactly 1.0.
        """
        torch.manual_seed(0)
        layer = torch.nn.Linear(32, 32).eval()
        v = torch.randn(32)
        alpha = 1.0
        captured = {}
        state = {"enabled": False}

        def inject_hook(module, inputs, output):
            if not state["enabled"]:
                return output
            out = output.clone()
            out[:, -1, :] = out[:, -1, :] + alpha * v
            return out

        def capture_hook(module, inputs, output):
            captured["r"] = output.detach().clone()

        x = torch.randn(1, 5, 32)  # single item, like the real probe
        cap_h = layer.register_forward_hook(capture_hook)  # OLD (buggy) order
        inj_h = layer.register_forward_hook(inject_hook)
        try:
            with torch.no_grad():
                layer(x)
                clean = captured["r"].clone()
                state["enabled"] = True
                layer(x)
                inj = captured["r"].clone()
        finally:
            cap_h.remove()
            inj_h.remove()
        expected = clean[:, -1, :] + alpha * v
        rel = float(torch.linalg.vector_norm(inj[:, -1, :] - expected)
                    / torch.linalg.vector_norm(alpha * v))
        self.assertAlmostEqual(rel, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
