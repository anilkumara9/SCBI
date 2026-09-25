#!/usr/bin/env python3
"""EXP086 Stage A — $0 CPU advisory weight-only screen (§5 of the signed protocol).

PINNED OBJECT (§5, G1): He_affine per layer-block computed from the frozen
weight matrices ALONE, restricted to the SQUARE blocks only — the attention
O/V projections (d x d). The rectangular MLP up/down projections (d x 4d /
4d x d) are EXCLUDED because lambda_i is undefined for rectangular matrices.

    He = (||W||_F^2 - sum_i |lambda_i|^2)^{1/2} / ||W||_F

computed via CPU eigendecomposition of each square block.

STATUS (signed, non-negotiable): explicitly APPROXIMATE, ADVISORY,
NON-BINDING. It CANNOT KILL the family alone; it is a prior-strength
modifier recorded before Stage B. This module is structurally incapable of
emitting a KILL/CONTINUE/HELD/PIVOT verdict — `stage_a_screen()` returns an
ADVISORY report only. Any caller that wants a verdict from Stage A is
defective by construction (G1 precedent).

Block registry (Pythia-410m = GPTNeoXForCausalLM, 24 layers, d = 1024):
  - INCLUDED: `gpt_neox.layers.{i}.attention.dense` (O projection, 1024x1024,
    read directly) and the V projection, which in GPTNeoX is FUSED inside
    `gpt_neox.layers.{i}.attention.query_key_value` (3072x1024). The fused
    weight is laid out PER-HEAD as [q_h, k_h, v_h] with head_dim = 64
    (16 heads), so V is the interleaved rows {r : (r mod 192) >= 128} —
    1024 rows total. The contiguous [2048:3072] slice assumed at build
    (LOG-315) was WRONG for GPT-NeoX (caught by independent review,
    LOG-326 F1: slice mean 206.2 vs true-V mean 300.0 on a synthetic
    fused weight) and was rewired to the interleaved layout at LOG-327.
    The fused QKV block itself is rectangular -> excluded by the G1
    square-only rule.
  - EXCLUDED: fused QKV (3072x1024), MLP dense_h_to_4h (4096x1024),
    MLP dense_4h_to_h (1024x4096), embeddings, unembedding, biases, norms.
  - Q and K projections: square (1024x1024 as slices) but NOT named in the
    signed §5 pinned object ("the attention O/V projections") -> EXCLUDED
    (faithful to the named set; see BUILD_NOTES §5 ambiguity A2).

Read-only: the runner loads weights through a loader that must not mutate
parameters; the FrozenBackboneGuard (exp086_guards) hashes state_dict
before/after Stage A (Law #6/Law #13).
"""

import math

import exp086_guards as G

N_LAYERS = 24  # Pythia-410m depth (program-standard site: layer 20 of 0..23)

# Per-head interleaved V layout of GPT-NeoX fused QKV (LOG-327 repair of
# LOG-326 F1). The fused weight is (3d, d) = (3072, 1024), laid out per-head
# as [q_h, k_h, v_h] with head_dim = 64 (16 heads x 64 = 1024). V rows are
# {r : (r mod 3*head_dim) >= 2*head_dim} = {r : (r mod 192) >= 128}.
QKV_FUSED_ROWS = 3072
HEAD_DIM = 64
V_ROWS = tuple(r for r in range(QKV_FUSED_ROWS)
               if (r % (3 * HEAD_DIM)) >= 2 * HEAD_DIM)
assert len(V_ROWS) == 1024, f"V_ROWS has {len(V_ROWS)} rows, expected 1024"

# Block registry with provenance. kind "direct" = square weight read as-is;
# kind "fused-interleaved" = square sub-block formed by per-head interleaved
# row selection from a rectangular fused block (the selected block is
# weight-only; provenance is logged loudly).
# RETIRED kind "fused-slice" (contiguous rows [2048:3072]): assumed a Q;K;V
# stacked layout GPT-NeoX does not use. Kept as a loud dead branch in
# extract_block below — it raises, never slices.
BLOCKS = []
for _i in range(N_LAYERS):
    BLOCKS.append({
        "name": f"layer{_i}.attn.O",
        "key": f"gpt_neox.layers.{_i}.attention.dense.weight",
        "kind": "direct",
        "d": 1024,
    })
    BLOCKS.append({
        "name": f"layer{_i}.attn.V",
        "key": f"gpt_neox.layers.{_i}.attention.query_key_value.weight",
        "kind": "fused-interleaved",
        "row_idx": V_ROWS,   # per-head interleaved V rows (LOG-327)
        "slice_note": ("V is fused in QKV (3072x1024, rectangular -> excluded "
                       "as a whole); V read as the per-head interleaved rows "
                       "{r : (r mod 192) >= 128} (1024x1024), weight-only, "
                       "provenance logged. The contiguous [2048:3072] slice "
                       "assumed at build was WRONG (LOG-326 F1, repaired "
                       "LOG-327)."),
        "d": 1024,
    })


def assert_square_block(W, name="<block>"):
    """G1 square-only rule: raise BlockSelectionError on rectangular input.

    W: 2-D array-like with .shape. The rule is enforced at the point of use,
    not trusted from the registry.
    """
    shape = getattr(W, "shape", None)
    if shape is None:
        raise G.BlockSelectionError(
            f"Stage A: block '{name}' has no .shape — cannot verify squareness"
        )
    if len(shape) != 2 or shape[0] != shape[1]:
        raise G.BlockSelectionError(
            f"Stage A: block '{name}' is {tuple(shape)} — rectangular blocks "
            "are EXCLUDED by the signed §5/G1 square-only rule (lambda_i "
            "undefined for rectangular matrices)."
        )
    if shape[0] == 0:
        raise G.BlockSelectionError(f"Stage A: block '{name}' is empty")
    return shape[0]


def eigendecompose(W):
    """CPU eigendecomposition backend: numpy first, torch fallback.

    Returns eigenvalues as a 1-D complex array-like. Raises
    G.BundleError loudly if neither backend is importable — never silently
    substitutes an approximation.
    """
    try:
        import numpy as np
        return np.linalg.eigvals(np.asarray(W, dtype=np.complex128))
    except ImportError:
        pass
    try:
        import torch
        Wt = torch.as_tensor(W, dtype=torch.complex128)
        return torch.linalg.eigvals(Wt).cpu().numpy()
    except ImportError:
        pass
    raise G.BundleError(
        "Stage A: no eigendecomposition backend available (need numpy or "
        "torch). Refusing to approximate."
    )


def henrici_index(W, eigvals=None, name="<block>"):
    """Henrici non-normality index of a SQUARE block.

        He = (||W||_F^2 - sum_i |lambda_i|^2)^{1/2} / ||W||_F

    W: 2-D square array-like. eigvals: optional precomputed eigenvalues
    (same backend convention); if None, eigendecompose(W) is used.
    Returns (He, info dict). He in [0, 1] up to floating error; tiny
    negative radicands from rounding are clamped to 0 (logged).

    [FACT] Schur: sum |lambda_i|^2 <= ||W||_F^2, so He in [0,1]; He = 0 iff
    W is normal.
    """
    d = assert_square_block(W, name)
    if eigvals is None:
        eigvals = eigendecompose(W)
    try:
        import numpy as np
        Wf = np.asarray(W, dtype=np.float64)
        frob2 = float(np.sum(Wf * Wf))
        lam2 = float(np.sum(np.abs(np.asarray(eigvals)) ** 2))
    except ImportError:  # pragma: no cover — numpy always present on build box
        frob2 = sum(float(x) * float(x) for row in W for x in row)
        lam2 = sum(abs(complex(l)) ** 2 for l in eigvals)
    if not (frob2 > 0):
        raise G.BundleError(
            f"Stage A: block '{name}' has zero Frobenius norm — He undefined"
        )
    radicand = frob2 - lam2
    clamped = False
    if radicand < 0:
        if radicand < -1e-9 * frob2:
            raise G.BundleError(
                f"Stage A: block '{name}': sum|lambda|^2 exceeds ||W||_F^2 by "
                f"{-radicand:.3e} (Schur violation — backend suspect)"
            )
        radicand = 0.0
        clamped = True
    he = math.sqrt(radicand) / math.sqrt(frob2)
    return he, {
        "name": name, "d": d,
        "frob": math.sqrt(frob2), "sum_abs_lambda2": lam2,
        "radicand_clamped": clamped,
    }


def extract_block(state_dict, spec):
    """Read one registered block from a state_dict (read-only view).

    spec: registry entry. Returns (name, array, provenance_note).
    Raises BlockSelectionError if the fused slice would be non-square.
    """
    key = spec["key"]
    if key not in state_dict:
        raise G.BundleError(
            f"Stage A: weight key missing: '{key}' (block {spec['name']})"
        )
    W = state_dict[key]
    note = f"direct read of '{key}'"
    if spec["kind"] == "fused-slice":
        # RETIRED (LOG-327): the contiguous [2048:3072] slice assumed a
        # Q;K;V stacked layout that GPT-NeoX does not use (LOG-326 F1).
        # Any spec still carrying this kind is stale — refuse loudly, never
        # silently slice. Dead by design; tested dead in test_exp086.py.
        raise G.BundleError(
            f"Stage A: block '{spec['name']}' uses retired kind "
            "'fused-slice' (contiguous [2048:3072] assumption was wrong, "
            "LOG-326 F1). Use kind 'fused-interleaved'."
        )
    if spec["kind"] == "fused-interleaved":
        idx = list(spec["row_idx"])
        W = W[idx, :]
        note = (f"per-head interleaved V rows {{r : (r mod 192) >= 128}} of "
                f"fused '{key}' (GPT-NeoX [q_h,k_h,v_h] per-head layout, "
                f"head_dim=64); {spec['slice_note']}")
    return spec["name"], W, note


def stage_a_screen(state_dict, eig_fn=None):
    """Run the full Stage-A advisory screen. Returns the ADVISORY report.

    state_dict: mapping weight-name -> array (read-only; never mutated here).
    eig_fn: optional eigendecomposition callable (tests inject synthetic
    backends); default eigendecompose().

    The report dict carries per-block He values, provenance, the guard hashes
    (filled by the runner), and the advisory reading. It carries NO verdict
    field by design: `advisory_reading` is prose ("prior-strength modifier"),
    never one of KILL/CONTINUE/HELD/PIVOT. Structural guarantee: any attempt
    to derive a family verdict from this report must go through
    exp086_verdicts.adjudicate, which has no Stage-A input row.
    """
    per_block = []
    for spec in BLOCKS:
        name, W, note = extract_block(state_dict, spec)
        d = assert_square_block(W, name)  # G1 enforced at point of use
        eigvals = eig_fn(W) if eig_fn is not None else eigendecompose(W)
        he, info = henrici_index(W, eigvals=eigvals, name=name)
        per_block.append({
            "block": name,
            "key": spec["key"],
            "kind": spec["kind"],
            "d": d,
            "He": he,
            "frob": info["frob"],
            "sum_abs_lambda2": info["sum_abs_lambda2"],
            "radicand_clamped": info["radicand_clamped"],
            "provenance": note,
        })
    hes = [b["He"] for b in per_block]
    report = {
        "stage": "A",
        "status": "ADVISORY — explicitly approximate, non-binding; "
                  "CANNOT KILL the family alone (signed §5; G1 precedent)",
        "model": G.MODEL_ID,
        "n_blocks": len(per_block),
        "blocks": per_block,
        "He_min": min(hes),
        "He_max": max(hes),
        "He_mean": sum(hes) / len(hes),
        "advisory_reading": (
            "Prior-strength modifier recorded before Stage B. High He "
            "(strongly non-normal attention projections) is consistent with "
            "the dynamical-amplifier hypothesis' premise (transient growth "
            "without large eigenvalues); near-zero He everywhere weakens the "
            "prior but the pilot still runs — the rank arms test the actual "
            "claim (§5: the screen's weakness is declared, not hidden)."
        ),
        "verdict": None,  # structural: Stage A emits no verdict, ever
    }
    return report
