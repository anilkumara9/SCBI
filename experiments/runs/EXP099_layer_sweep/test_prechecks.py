"""EXP099 pre-run logic checks (numpy-only; no model, no weights).

Validates the mechanical logic the executor depends on BEFORE any model
pass: constructor pin, fresh-seed norm-tie math, degeneracy gate behavior,
McNemar machinery import, RNG stream determinism, anchor-set derivation,
and protocol-file presence. Any failure -> the executor must not run
(fail loud, never silent).
"""

import csv
import hashlib
import json
import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
EXP094_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP094_peritem_l11")
EXP098_OUT = os.path.join(REPO_ROOT, "experiments", "runs",
                          "EXP098_multilayer_composition", "out")
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


@check("licensed protocol file present (v2, LOG-4427 delta SIGN chain)")
def _():
    p = os.path.join(REPO_ROOT, "research", "innovation",
                     "S6-4_PREREG_DRAFT_v2_2026-09-28.md")
    assert os.path.isfile(p), "v2 protocol file missing"
    txt = open(p).read()
    assert "LOG-4425" in txt and "F1" in txt and "F9" in txt, \
        "v2 errata (Law #14 F1-F9, LOG-4425) not found in protocol file"


@check("fresh R-arm seeds distinct from EXP098's 94094")
def _():
    src = open(os.path.join(BUNDLE_DIR, "run_exp099.py")).read()
    assert "R_SEED_W20 = 117011" in src and "R_SEED_W8 = 117013" in src
    assert 117011 != 94094 and 117013 != 94094 and 117011 != 117013


@check("constructor direction math at ratio 0.38")
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
    dim = 1024
    for seed in (117011, 117013):
        rng = np.random.default_rng(seed)
        for i in range(60):
            d_norm = 0.38 * (0.5 + rng.random())
            z = rng.normal(size=dim)
            z = z / np.linalg.norm(z)
            g = z * d_norm
            assert abs(float(np.linalg.norm(g)) - d_norm) <= 1e-9 * d_norm


@check("RNG draw order deterministic (per-layer stream, item-major)")
def _():
    def draws(seed):
        rng = np.random.default_rng(seed)
        return [rng.normal(size=8) for _i in range(60)]
    for seed in (117011, 117013):
        a, b = draws(seed), draws(seed)
        assert all(np.array_equal(x, y) for x, y in zip(a, b))
        assert len(a) == 60
    # the two streams differ (independent seeds)
    assert not np.array_equal(draws(117011)[0], draws(117013)[0])


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


@check("McNemar doubling import + probe-feasibility algebra (§4.2)")
def _():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "s94", os.path.join(EXP094_DIR, "score_exp094.py"))
    s94 = importlib.util.module_from_spec(spec)
    sys.modules["s94"] = s94
    spec.loader.exec_module(s94)
    p = s94.mcnemar_exact_p(0, 9)
    assert abs(p - 0.00390625) < 1e-12, f"b=0,c=9 -> {p}"
    p2 = s94.mcnemar_exact_p(0, 8)
    assert abs(p2 - 0.0078125) < 1e-12, f"b=0,c=8 -> {p2}"
    p3 = s94.mcnemar_exact_p(0, 6)
    assert abs(p3 - 0.03125) < 1e-12, f"b=0,c=6 -> {p3} (anchor band)"
    assert hasattr(s94, "tango_ci_paired") and hasattr(s94, "contrast_stats")


@check("G5 band literals ([0.285, 0.475] contain 0.38)")
def _():
    lo, hi = 0.285, 0.475
    assert lo <= 0.38 <= hi
    assert abs(lo - 0.38 * 0.75) < 1e-12
    assert abs(hi - 0.38 * 1.25) < 1e-12


@check("G5 probes use constructed d_0 at layers 8 and 20")
def _():
    src = open(os.path.join(BUNDLE_DIR, "run_exp099.py")).read()
    assert "d8[0]" in src and "d20[0]" in src, \
        "G5 probes must use the constructed d_0 vectors"
    assert "(8, d8[0])" in src and "(20, d20[0])" in src, \
        "G5 probes must cover layers 8 and 20"
    assert "pv = pv / np.linalg.norm(pv) * 0.38" not in src, \
        "norm-0.38-absolute random probe must not be used"
    assert 6e-8 * (1 / 0.38) < 1e-6


@check("score_exp099 imports cleanly (numpy-only)")
def _():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "score_exp099",
        os.path.join(BUNDLE_DIR, "score_exp099.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["score_exp099"] = mod
    spec.loader.exec_module(mod)
    assert hasattr(mod, "score_all")


@check("EXP098 anchor set derivation (6 items, b=0, c=6)")
def _():
    B, L20 = {}, {}
    with open(os.path.join(EXP098_OUT, "per_item_records.csv")) as f:
        for row in csv.DictReader(f):
            if row["arm"] == "B":
                B[row["item_id"]] = int(row["correct_top1"])
            elif row["arm"] == "L20-only":
                L20[row["item_id"]] = int(row["correct_top1"])
    assert len(B) == 60 and len(L20) == 60
    flip = sorted(k for k in B if B[k] != L20[k])
    b = sum(1 for k in flip if B[k] == 0 and L20[k] == 1)
    c = sum(1 for k in flip if B[k] == 1 and L20[k] == 0)
    assert len(flip) == 6 and b == 0 and c == 6, \
        f"anchor derivation mismatch: flips={len(flip)}, b={b}, c={c}"
    # the executor's hardcoded set must equal the derived set
    src = open(os.path.join(BUNDLE_DIR, "run_exp099.py")).read()
    for k in flip:
        assert k in src, f"anchor item {k} missing from executor pin"


@check("executor pins the v2 decision constants")
def _():
    src = open(os.path.join(BUNDLE_DIR, "run_exp099.py")).read()
    assert "DEGENERACY_SIGNATURE_REF = 0.6639" in src
    assert "DEGENERACY_SIGNATURE_TOL = 0.05" in src
    assert "HARD_CAP_PASSES = 500" in src
    assert "(20, \"L20\"), (20, \"W20\"), (8, \"L8\"), (8, \"W8\")" in src


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
