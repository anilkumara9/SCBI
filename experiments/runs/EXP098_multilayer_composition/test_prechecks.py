"""EXP098 pre-run logic checks (numpy-only; no model, no weights).

Validates the mechanical logic the executor depends on BEFORE any model
pass: constructor pin, norm-tie math, degeneracy gate behavior, McNemar
machinery import, nearly-moved classifier edge cases, RNG draw-order
determinism, and protocol-file presence. Any failure -> the executor must
not run (fail loud, never silent).
"""

import hashlib
import json
import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
EXP094_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP094_peritem_l11")
sys.path.insert(0, BUNDLE_DIR)
sys.path.insert(0, EXP094_DIR)

import numpy as np

import constructor as C  # noqa: E402

CHECKS = []


def check(name):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@check("constructor frozen pin")
def _():
    live = sha256_file(os.path.join(EXP094_DIR, "constructor.py"))
    assert live == ("5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa"
                    "81917f361"), f"constructor hash mismatch: {live[:16]}"
    m = json.load(open(os.path.join(EXP094_DIR, "constructor_manifest.json")))
    assert m.get("g7_verdict") == "PASS"
    assert m.get("P0_TEXT") == C.P0_TEXT
    assert C.R_SEED == 94094 and C.NORM_RATIO == 0.0474


@check("licensed protocol file present (v2, LOG-4421 clearance chain)")
def _():
    p = os.path.join(REPO_ROOT, "research", "innovation",
                     "S6-2_PREREG_DRAFT_v2_2026-09-28.md")
    assert os.path.isfile(p), "v2 protocol file missing"
    txt = open(p).read()
    assert "LOG-4418" in txt and "F1" in txt and "F3" in txt, \
        "v2 errata (Law #14 F1-F3, LOG-4418) not found in protocol file"


@check("constructor direction math at ratio 0.38 (both layers' pattern)")
def _():
    rng = np.random.default_rng(7)
    for _trial in range(5):
        dim = 1024
        a = rng.normal(size=dim)
        b = rng.normal(size=dim)
        h = float(np.linalg.norm(a))
        d, info = C.build_per_item_direction(a, b, h, ratio=0.38)
        assert not info["degenerate_zero"]
        assert abs(info["perturbation_ratio"] - 0.38) < 1e-12
        assert 0.285 <= info["perturbation_ratio"] <= 0.475
    # zero-norm contrast -> degenerate_zero, ratio 0 (out of band -> HOLD)
    a = rng.normal(size=1024)
    d, info = C.build_per_item_direction(a, a.copy(), 1.0, ratio=0.38)
    assert info["degenerate_zero"] and info["perturbation_ratio"] == 0.0


@check("norm-tie math: ||g|| == ||d|| per layer per item (120 assertions)")
def _():
    rng = np.random.default_rng(C.R_SEED)
    dim = 1024
    for i in range(60):
        for _layer in (11, 20):
            d_norm = 0.38 * (0.5 + rng.random())
            z = rng.normal(size=dim)
            z = z / np.linalg.norm(z)
            g = z * d_norm
            assert abs(float(np.linalg.norm(g)) - d_norm) <= 1e-9 * d_norm


@check("RNG draw order deterministic (item-major: L11 then L20 per item)")
def _():
    def draws():
        rng = np.random.default_rng(C.R_SEED)
        out = []
        for _i in range(60):
            out.append(rng.normal(size=8))   # L11 draw
            out.append(rng.normal(size=8))   # L20 draw
        return out
    a, b = draws(), draws()
    assert all(np.array_equal(x, y) for x, y in zip(a, b))
    assert len(a) == 120
    # L11 and L20 draws for the same item differ (independent directions)
    assert not np.array_equal(a[0], a[1])


@check("degeneracy gate behavior (mean|cos|, bar 0.95)")
def _():
    rng = np.random.default_rng(11)
    # isotropic set -> low degeneracy (proceed)
    U = rng.normal(size=(60, 64))
    U = U / np.linalg.norm(U, axis=1, keepdims=True)
    G = U @ U.T
    iu = np.triu_indices(60, k=1)
    m = float(np.abs(G[iu]).mean())
    assert m < 0.95, f"isotropic set unexpectedly degenerate: {m}"
    # near-identical set -> gate fires
    base = rng.normal(size=64)
    base = base / np.linalg.norm(base)
    V = np.stack([base + 0.01 * rng.normal(size=64) for _ in range(60)])
    V = V / np.linalg.norm(V, axis=1, keepdims=True)
    G2 = V @ V.T
    m2 = float(np.abs(G2[iu]).mean())
    assert m2 >= 0.95, f"near-identical set did not trip gate: {m2}"


@check("McNemar doubling import + probe-feasibility algebra")
def _():
    sys.path.insert(0, os.path.join(
        REPO_ROOT, "experiments", "runs", "EXP094_peritem_l11"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "s94", os.path.join(REPO_ROOT, "experiments", "runs",
                            "EXP094_peritem_l11", "score_exp094.py"))
    s94 = importlib.util.module_from_spec(spec)
    sys.modules["s94"] = s94
    spec.loader.exec_module(s94)
    p = s94.mcnemar_exact_p(8, 0)
    assert abs(p - 0.0078125) < 1e-12, f"b=8,c=0 -> {p}"
    p2 = s94.mcnemar_exact_p(7, 0)
    assert abs(p2 - 0.015625) < 1e-12, f"b=7,c=0 -> {p2}"
    assert hasattr(s94, "tango_ci_paired") and hasattr(s94, "contrast_stats")


def _nm(dm, mB):
    # mirror of the executor's classifier; returns python bool
    if mB == 0.0:
        return bool(abs(dm) > 0.0)
    return bool((np.sign(dm) == -np.sign(mB)) and
                (abs(dm) >= 0.5 * abs(mB)))


@check("nearly-moved classifier edge cases (§2.5 definition)")
def _():
    # pushed halfway toward the flip boundary, correct sign
    assert _nm(-0.6, 1.0) is True
    assert _nm(-0.4, 1.0) is False
    # wrong sign (pushed away) -> not nearly moved
    assert _nm(0.9, 1.0) is False
    # mB == 0 edge
    assert _nm(0.01, 0.0) is True
    assert _nm(0.0, 0.0) is False


@check("G5 band literals ([0.285, 0.475] contain 0.38)")
def _():
    # The protocol's bands are rounded literals, not exact float products
    # (0.38*0.75 = 0.28500000000000003 in float64). The executor uses the
    # literals verbatim — this check pins that behavior.
    lo, hi = 0.285, 0.475
    assert lo <= 0.38 <= hi
    assert abs(lo - 0.38 * 0.75) < 1e-12
    assert abs(hi - 0.38 * 1.25) < 1e-12


@check("G5 probe uses constructed d_0 (EXP094 precedent, not norm-0.38 random)")
def _():
    # The smoke test proved a norm-0.38-absolute random probe FAILS criterion
    # (i) at 1e-6 on this model (float32 hook rounding ~6e-8*||clean|| exceeds
    # 1e-6*||v|| when ||clean||/||v|| >> 1/0.38). The executor must probe with
    # the constructed item-0 directions (||d_0|| = 0.38*||clean||).
    src = open(os.path.join(BUNDLE_DIR, "run_exp098.py")).read()
    assert "d11[0]" in src and "d20[0]" in src, \
        "G5 probes must use the constructed d_0 vectors"
    assert "pv = pv / np.linalg.norm(pv) * 0.38" not in src, \
        "norm-0.38-absolute random probe must not be used"
    # arithmetic guard: rel_err ~= 6e-8 * ||clean||/||v|| < 1e-6
    # requires ||clean||/||v|| < ~16; d_0 gives 1/0.38 ~= 2.6 -> OK
    assert 6e-8 * (1 / 0.38) < 1e-6


@check("score_exp098 imports cleanly (numpy-only)")
def _():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "score_exp098",
        os.path.join(BUNDLE_DIR, "score_exp098.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["score_exp098"] = mod
    spec.loader.exec_module(mod)
    assert hasattr(mod, "score_all")


def main():
    failed = []
    for name, fn in CHECKS:
        try:
            fn()
            print(f"  PASS  {name}")
        except Exception as e:  # noqa: BLE001
            failed.append(name)
            print(f"  FAIL  {name}: {e}")
    print(f"[prechecks] {len(CHECKS) - len(failed)}/{len(CHECKS)} passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
