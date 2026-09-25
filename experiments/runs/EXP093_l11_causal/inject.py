"""EXP093 injection mechanics + G5 injection-site verification.

Draft §3.2: inject h <- h + alpha * v^(-i) at the layer-11 post-block
residual stream, final token position only, alpha = 1.0.

G5 (registered acceptance criteria, draft F5):
  (i)   single-item probe: hooked final-position residual == unhooked value
        + alpha*v^(-i) within relative 1e-6;
  (ii)  all other positions change by < 1e-9 absolute;
  (iii) condition B (hook disabled) logits bit-match a hook-free reference run.

Misplacement -> RUN-INVALID.

The verification core (verify_g5) is backend-agnostic: it takes callables so
the same logic is executed against the numpy MockModel (build-time / smoke
tests) and the real torch model (real mode). No torch import at module top
level — the real backend imports torch lazily inside functions.
"""

import numpy as np

ALPHA = 1.0          # registered injection magnitude (draft §3.2)
LAYER_INDEX = 11     # Pythia/GPTNeoX: gpt_neox.layers[11]
G5_REL_TOL = 1e-6    # criterion (i)
G5_ABS_TOL = 1e-9    # criterion (ii)


class RunInvalid(Exception):
    """Guard failure -> RUN-INVALID (withheld, never a verdict)."""


# ---------------------------------------------------------------------------
# Mock backend (numpy only, no weights) — pipeline testing, never a verdict.
# ---------------------------------------------------------------------------

class MockCausalModel:
    """Synthetic causal model with a genuine linear readout.

    Residual stream: per-item (T, 1024) arrays. Layer-11 final-token residual
    h_i is class-structured; the decision margin is margin_i = <w, h_final>
    + b, so injection genuinely moves margins by alpha*<w, v>. The readout
    is fixed (seeded); margins are calibrated so the clean baseline lands
    near 36/60 correct.
    """

    DIM = 1024
    N_CLASSES = 20

    def __init__(self, seed=93093, n_items=60, seq_len=24):
        rng = np.random.default_rng(seed)
        self.seq_len = seq_len
        self.w = rng.normal(size=self.DIM)
        self.w /= np.linalg.norm(self.w)
        # class means + per-item residuals
        self.class_mean = rng.normal(size=(self.N_CLASSES, self.DIM))
        self.h = np.zeros((n_items, self.DIM))
        self.target_ids = np.zeros(n_items, dtype=int)
        self.foil_ids = np.zeros(n_items, dtype=int) + 1
        for i in range(n_items):
            c = i % self.N_CLASSES
            self.h[i] = self.class_mean[c] + 0.5 * rng.normal(size=self.DIM)
        # calibrate b so ~60% of items are correct at baseline
        m0 = self.h @ self.w
        self.b = -float(np.quantile(m0, 0.40))
        # full residual stream: other positions are filler
        self.stream = rng.normal(size=(n_items, seq_len, self.DIM)) * 0.1
        for i in range(n_items):
            self.stream[i, -1, :] = self.h[i]

    def layer11_residual(self, item_idx, inject=None):
        """Return the (T, DIM) layer-11 post-block residual for an item.

        inject: None (clean) or (v, alpha) to add alpha*v at final position.
        """
        r = self.stream[item_idx].copy()
        if inject is not None:
            v, alpha = inject
            r[-1, :] = r[-1, :] + alpha * np.asarray(v, dtype=np.float64)
        return r

    def forward_logits(self, item_idx, inject=None):
        """Return (logit_target, logit_foil) for the item under a condition."""
        r = self.layer11_residual(item_idx, inject=inject)
        margin = float(r[-1, :] @ self.w + self.b)
        # tie-breaking noise is zero: ties are exact and therefore testable
        return np.array([margin / 2.0, -margin / 2.0])


# ---------------------------------------------------------------------------
# G5 verification core (backend-agnostic)
# ---------------------------------------------------------------------------

def verify_g5(get_resid_clean, get_resid_injected,
             get_logits_hooked_disabled, get_logits_free,
             v, alpha, label=""):
    """Execute the three G5 acceptance criteria.

    All callables are zero-arg thunks for the SAME probe item.
    v: the unit direction used for the probe (alpha*v injected).
    Returns a dict of the measured deviations. Raises RunInvalid on failure.
    """
    tag = f" [{label}]" if label else ""
    resid_clean = np.asarray(get_resid_clean(), dtype=np.float64)
    resid_inj = np.asarray(get_resid_injected(), dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)

    if resid_clean.shape != resid_inj.shape:
        raise RunInvalid(
            f"G5 FAIL{tag}: residual shape mismatch "
            f"{resid_clean.shape} vs {resid_inj.shape} — RUN-INVALID.")
    if resid_clean.ndim != 2:
        raise RunInvalid(
            f"G5 FAIL{tag}: expected (T, D) residuals, got "
            f"{resid_clean.shape} — RUN-INVALID.")

    # (i) final position == clean + alpha*v within relative 1e-6
    expected = resid_clean[-1, :] + alpha * v
    denom = np.linalg.norm(alpha * v)
    rel_err = (np.linalg.norm(resid_inj[-1, :] - expected)
               / denom if denom > 0 else float("inf"))
    if rel_err > G5_REL_TOL:
        raise RunInvalid(
            f"G5 FAIL{tag}: criterion (i) — hooked final-position residual "
            f"differs from clean + alpha*v by rel {rel_err:.3e} > "
            f"{G5_REL_TOL:.0e} — RUN-INVALID (injection misplaced).")

    # (ii) all other positions change by < 1e-9 absolute
    other = np.abs(resid_inj[:-1, :] - resid_clean[:-1, :]).max() \
        if resid_inj.shape[0] > 1 else 0.0
    if other >= G5_ABS_TOL:
        raise RunInvalid(
            f"G5 FAIL{tag}: criterion (ii) — non-final positions changed by "
            f"{other:.3e} >= {G5_ABS_TOL:.0e} — RUN-INVALID (injection "
            f"leaked beyond the final position).")

    # (iii) hook-disabled logits bit-match hook-free reference logits
    l_dis = np.asarray(get_logits_hooked_disabled())
    l_free = np.asarray(get_logits_free())
    if l_dis.shape != l_free.shape or not np.array_equal(l_dis, l_free):
        raise RunInvalid(
            f"G5 FAIL{tag}: criterion (iii) — condition-B (hook disabled) "
            f"logits do not bit-match the hook-free reference run — "
            f"RUN-INVALID.")

    return {
        "criterion_i_rel_err": float(rel_err),
        "criterion_ii_max_abs_change": float(other),
        "criterion_iii_bit_match": True,
        "gate": "PASS",
    }


def verify_g5_mock(mock_model, item_idx, v, alpha=ALPHA):
    """G5 against the numpy MockModel (build-time / smoke tests)."""
    v = np.asarray(v, dtype=np.float64)
    return verify_g5(
        lambda: mock_model.layer11_residual(item_idx),
        lambda: mock_model.layer11_residual(item_idx, inject=(v, alpha)),
        lambda: mock_model.forward_logits(item_idx, inject=None),
        lambda: mock_model.forward_logits(item_idx, inject=None),
        v, alpha, label=f"mock item {item_idx}")


# ---------------------------------------------------------------------------
# Real backend (torch) — lazy imports only.
# ---------------------------------------------------------------------------

class TorchInjectionHook:
    """Forward hook adding alpha*v at the final position of the layer-11
    post-block residual. attach()/detach(); enable()/disable().

    Misplacement is caught by G5, not by trust.
    """

    def __init__(self, alpha=ALPHA):
        self.alpha = alpha
        self.v_t = None
        self.enabled = False
        self._handle = None
        self._module_path = None

    @staticmethod
    def resolve_module(model):
        """Resolve the layer-11 block module. Raises RunInvalid if unresolvable."""
        for path in ("gpt_neox.layers", "transformer.h"):
            obj = model
            try:
                for part in path.split("."):
                    obj = getattr(obj, part)
                layer = obj[LAYER_INDEX]
                return layer, f"{path}[{LAYER_INDEX}]"
            except (AttributeError, IndexError, TypeError):
                continue
        raise RunInvalid(
            "G5 FAIL: could not resolve the layer-11 block module "
            "(tried gpt_neox.layers[11], transformer.h[11]) — RUN-INVALID.")

    def _hook_fn(self, module, inputs, output):
        if not self.enabled or self.v_t is None:
            return output
        # GPTNeoXLayer returns a tensor (or a 1-tuple); the post-block
        # residual is the first element.
        is_tuple = isinstance(output, tuple)
        out = output[0] if is_tuple else output
        delta = (self.alpha * self.v_t).to(dtype=out.dtype, device=out.device)
        out = out.clone()
        out[:, -1, :] = out[:, -1, :] + delta
        return (out,) + output[1:] if is_tuple else out

    def attach(self, model, v):
        import torch
        layer, path = self.resolve_module(model)
        self.v_t = torch.as_tensor(np.asarray(v, dtype=np.float32))
        self._module_path = path
        self._handle = layer.register_forward_hook(self._hook_fn)
        return path

    def detach(self):
        if self._handle is not None:
            self._handle.remove()
            self._handle = None

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


def verify_g5_real(model, tokenizer, prompt_text, v, alpha=ALPHA):
    """G5 against the real torch model (real mode). Single-item probe.

    Returns the criterion measurements dict. Raises RunInvalid on failure.
    torch/transformers are imported here (lazy) — this function never runs in
    mock mode.
    """
    import torch
    v = np.asarray(v, dtype=np.float64)
    hook = TorchInjectionHook(alpha=alpha)
    path = hook.attach(model, v)
    ids = torch.tensor([tokenizer.encode(prompt_text, add_special_tokens=False)],
                       dtype=torch.long)

    captured = {}

    def _capture(module, inputs, output):
        out = output[0] if isinstance(output, tuple) else output
        captured["resid"] = out[0].detach().cpu().to(torch.float64).numpy()

    layer, _ = TorchInjectionHook.resolve_module(model)
    cap_handle = layer.register_forward_hook(_capture)
    try:
        with torch.no_grad():
            # hook-free reference logits
            hook.detach()
            ref_logits = model(ids).logits[0].detach().cpu()
            # re-attach for the disabled/enabled runs
            hook.attach(model, v)
            hook.disable()
            logits_disabled = model(ids).logits[0].detach().cpu()
            # (iii) bit-match BEFORE any injection run
            if logits_disabled.shape != ref_logits.shape or not torch.equal(
                    logits_disabled, ref_logits):
                raise RunInvalid(
                    "G5 FAIL: criterion (iii) — condition-B (hook disabled) "
                    "logits do not bit-match the hook-free reference run — "
                    "RUN-INVALID.")
            # clean residual capture
            hook.disable()
            model(ids)
            resid_clean = captured["resid"].copy()
            # injected residual capture
            hook.enable()
            model(ids)
            resid_inj = captured["resid"].copy()
    finally:
        cap_handle.remove()
        hook.detach()

    return verify_g5(
        lambda: resid_clean,
        lambda: resid_inj,
        lambda: logits_disabled.numpy(),
        lambda: ref_logits.numpy(),
        v, alpha, label=f"real probe ({path})")
