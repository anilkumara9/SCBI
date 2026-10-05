"""EXP145 injection mechanics + G5 injection-site verification (GPT-2-small).

Port of the committed EXP093 `inject.py` real-backend logic, adapted:
  - hook point: output of `transformer.h[l*]` (the sequential-block analogue
    of the NeoX `gpt_neox.layers[11]` tap — S7-2 D4);
  - layer index parameterized (not hardcoded 11);
  - injection magnitude α calibrated (not 1.0);
  - G5 per S7-2 §3.4.4: (i) hooked final-position residual == clean + αv
    within rel ≤ 1e-6; (ii) hook-disabled logits bit-match hook-free
    reference; (iii) max-abs deviation sane. Any failure → RUN-INVALID.

The EXP093 RUN-INVALID lesson is baked in: the capture hook is registered
AFTER the injection hook is re-attached, and the registration order is
explicitly asserted (otherwise capture records the pre-injection residual
and criterion (i) measures rel_err = 1.0 — the algebraic signature of a
no-op capture).
"""

import numpy as np


class RunInvalid(Exception):
    """Guard failure -> RUN-INVALID (withheld, never a verdict)."""


G5_REL_TOL = 1e-6      # criterion (i)
G5_OTHER_ABS_TOL = 1e-9  # non-final positions (carried from EXP093 G5)


class GPT2InjectionHook:
    """Forward hook adding alpha*v at the final position of the
    transformer.h[l*] output residual. attach()/detach(); enable()/disable()."""

    def __init__(self, layer_index, alpha):
        self.layer_index = layer_index
        self.alpha = alpha
        self.v_t = None
        self.enabled = False
        self._handle = None
        self._module_path = None

    def resolve_module(self, model):
        try:
            layer = model.transformer.h[self.layer_index]
            return layer, f"transformer.h[{self.layer_index}]"
        except (AttributeError, IndexError, TypeError):
            raise RunInvalid(
                f"G5 FAIL: could not resolve transformer.h[{self.layer_index}] "
                f"— RUN-INVALID.")

    def _hook_fn(self, module, inputs, output):
        if not self.enabled or self.v_t is None:
            return output
        is_tuple = isinstance(output, tuple)
        out = output[0] if is_tuple else output
        import torch
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


def verify_g5_real(model, tokenizer, prompt_text, v, alpha, layer_index):
    """G5 against the real torch model. Single-item probe.

    torch/transformers imported lazily. Returns the criterion measurements.
    Raises RunInvalid on failure.
    """
    import torch
    v = np.asarray(v, dtype=np.float64)
    hook = GPT2InjectionHook(layer_index, alpha)
    path = hook.attach(model, v)
    ids = torch.tensor([tokenizer.encode(prompt_text, add_special_tokens=False)],
                       dtype=torch.long)

    captured = {}

    def _capture(module, inputs, output):
        out = output[0] if isinstance(output, tuple) else output
        captured["resid"] = out[0].detach().cpu().to(torch.float64).numpy()

    layer, _ = hook.resolve_module(model)
    cap_handle = None
    try:
        with torch.no_grad():
            # hook-free reference logits (injection hook detached)
            hook.detach()
            ref_logits = model(ids).logits[0].detach().cpu()
            # Re-attach the injection hook FIRST, then register the capture
            # hook AFTER it (registration-order chaining: the capture hook
            # must observe the post-injection residual).
            hook.attach(model, v)
            cap_handle = layer.register_forward_hook(_capture)
            _order = list(layer._forward_hooks)
            if _order.index(hook._handle.id) > _order.index(cap_handle.id):
                raise RunInvalid(
                    "G5 FAIL: probe internal error — capture hook registered "
                    "before the injection hook; capture would record the "
                    "pre-injection residual — RUN-INVALID.")
            # (ii) hook-disabled logits bit-match hook-free reference
            hook.disable()
            logits_disabled = model(ids).logits[0].detach().cpu()
            if logits_disabled.shape != ref_logits.shape or not torch.equal(
                    logits_disabled, ref_logits):
                raise RunInvalid(
                    "G5 FAIL: criterion (ii) — condition-B (hook disabled) "
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
        if cap_handle is not None:
            cap_handle.remove()
        hook.detach()

    if resid_clean.shape != resid_inj.shape or resid_clean.ndim != 2:
        raise RunInvalid(
            f"G5 FAIL: residual capture shape {resid_clean.shape} vs "
            f"{resid_inj.shape} — RUN-INVALID.")

    # (i) final position == clean + alpha*v within relative 1e-6
    expected = resid_clean[-1, :] + alpha * v
    denom = np.linalg.norm(alpha * v)
    rel_err = (np.linalg.norm(resid_inj[-1, :] - expected)
               / denom if denom > 0 else float("inf"))
    if rel_err > G5_REL_TOL:
        raise RunInvalid(
            f"G5 FAIL [real probe ({path})]: criterion (i) — hooked "
            f"final-position residual differs from clean + alpha*v by rel "
            f"{rel_err:.3e} > {G5_REL_TOL:.0e} — RUN-INVALID (misplaced).")

    # non-final positions unchanged (EXP093 G5 carried check)
    other = np.abs(resid_inj[:-1, :] - resid_clean[:-1, :]).max() \
        if resid_inj.shape[0] > 1 else 0.0
    if other >= G5_OTHER_ABS_TOL:
        raise RunInvalid(
            f"G5 FAIL [real probe ({path})]: non-final positions changed by "
            f"{other:.3e} >= {G5_OTHER_ABS_TOL:.0e} — RUN-INVALID (leak).")

    # (iii) max-abs deviation sane: achieved |αv| within [0.5, 2]x expected
    dev = float(np.abs(resid_inj[-1, :] - resid_clean[-1, :]).max())
    exp_dev = float(np.abs(alpha * v).max())
    sane = (0.5 * exp_dev <= dev <= 2.0 * exp_dev)
    if not sane:
        raise RunInvalid(
            f"G5 FAIL [real probe ({path})]: criterion (iii) — max-abs "
            f"deviation {dev:.3e} not sane vs expected {exp_dev:.3e} — "
            f"RUN-INVALID.")

    return {
        "hook_path": path,
        "criterion_i_rel_err": float(rel_err),
        "nonfinal_max_abs_change": float(other),
        "criterion_ii_bit_match": True,
        "criterion_iii_dev": dev,
        "criterion_iii_expected": exp_dev,
        "criterion_iii_sane": sane,
        "gate": "PASS",
    }
