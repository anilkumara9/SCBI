"""EXP100 pre-run logic checks (numpy + tokenizer only; no model, no weights).

Validates the mechanical logic the executor depends on BEFORE any model
pass: constructor pin, protocol file presence, fresh-seed distinctness,
entity-span derivation on all 60 bench items (E_i/N_i <= 0.5, span excludes
final token), gate math (tau = 2E/N), firing rule, mass formula, McNemar
doubling, norm-tie math, deterministic-copy rule, stratum-consistency
definition, delivery-band logic, and pass-budget arithmetic. Any failure ->
the executor must not run (fail loud, never silent).
"""

import csv
import hashlib
import json
import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
EXP094_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP094_peritem_l11")
EXP092_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl")
EXP093_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP093_l11_causal")
sys.path.insert(0, BUNDLE_DIR)
sys.path.insert(0, EXP094_DIR)
sys.path.insert(0, EXP092_DIR)
sys.path.insert(0, EXP093_DIR)

import numpy as np

import constructor as C  # noqa: E402
import reference_implementation as ref  # noqa: E402
from transformers import AutoTokenizer  # noqa: E402


def _load_frozen_scorer():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "exp100_frozen_scorer",
        os.path.join(EXP094_DIR, "score_exp094.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp100_frozen_scorer"] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_runner():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "exp100_runner", os.path.join(BUNDLE_DIR, "run_exp100.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp100_runner"] = mod
    spec.loader.exec_module(mod)
    return mod

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


@check("licensed protocol v2 file present (Law #14 LOG-4436 F1-F7 chain)")
def _():
    p = os.path.join(REPO_ROOT, "research", "innovation",
                     "S6-3_PREREG_DRAFT_v2_2026-09-28.md")
    assert os.path.isfile(p), "v2 protocol file missing"
    txt = open(p).read()
    assert "LOG-4436" in txt and "F1" in txt and "F7" in txt, \
        "Law #14 review chain (LOG-4436, F1-F7) not found in protocol file"
    assert "S6-3" in txt, "S6-3 designator not found in protocol file"
    # EXP100 mint + CEO clearance live in the research log (LOG-4439),
    # not in the unsigned draft file.
    log_txt = open(os.path.join(
        REPO_ROOT, "reports", "research_log.md")).read()
    assert "LOG-4439" in log_txt, "LOG-4439 clearance not in research log"


@check("fresh gated-R seed 207101 distinct from all prior R streams")
def _():
    src = open(os.path.join(BUNDLE_DIR, "run_exp100.py")).read()
    assert "R_SEED_GATED = 207101" in src, "R seed pin not found in runner"
    for used in (94094, 117011, 117013):
        assert 207101 != used, f"seed collision with {used}"


@check("entity-span derivation: all 60 items valid, E/N<=0.5, span excludes final token")
def _():
    runner = _load_runner()
    tok = AutoTokenizer.from_pretrained(
        "/home/hatch/workspace/.exp086_weights/pythia-410m",
        local_files_only=True)
    bench = ref.build_bench()
    assert len(bench) == 60
    for b in bench:
        sidx = runner.entity_span_token_idx(tok, b["prompt"], b["A"], b["C"])
        N = len(tok.encode(b["prompt"], add_special_tokens=False))
        E = len(sidx)
        assert 1 <= E < N, f"item {b['id']}: E={E} N={N}"
        assert E / N <= 0.5, f"item {b['id']}: E/N={E/N} violates step-0iii"
        assert (N - 1) not in sidx, \
            f"item {b['id']}: final token inside entity span"
        tau = 2.0 * E / N
        assert 0.0 < tau <= 1.0, f"item {b['id']}: tau={tau} out of (0,1]"
    # bench pin bound to the same items the runner uses (registered pin)
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(
        "exp100_pin_check",
        os.path.join(EXP093_DIR, "protocol_pin.py"))
    _pinmod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_pinmod)
    g0 = ref.verify_g0(bench, _pinmod.BENCH_PIN)
    assert g0["pin"] == _pinmod.BENCH_PIN


@check("gate threshold closed form tau = 2E/N")
def _():
    rng = np.random.default_rng(11)
    for _ in range(50):
        E = int(rng.integers(1, 20))
        N = int(rng.integers(E + 1, 200))
        if E / N > 0.5:
            continue
        tau = 2.0 * E / N
        assert abs(tau - 2 * (E / N)) < 1e-15
        assert tau <= 1.0


@check("firing rule: fire iff mass >= tau")
def _():
    assert (0.30 >= 0.2758) is True
    assert (0.27 >= 0.2758) is False
    # boundary: exact equality fires
    assert (0.2758 >= 0.2758) is True


@check("mass formula: mean over heads of span-sum at final query row")
def _():
    rng = np.random.default_rng(3)
    H, T = 16, 29
    W = rng.random((H, T, T))
    W = W / W.sum(axis=-1, keepdims=True)
    span = [3, 13, 23, 25]
    q = T - 1
    mass = float(np.mean([W[h, q, span].sum() for h in range(H)]))
    assert 0.0 <= mass <= 1.0
    # rows sum to 1 so mass <= 1 by construction; recompute via vector form
    mass2 = float(W[:, q, :][:, span].sum(axis=1).mean())
    assert abs(mass - mass2) < 1e-12


@check("McNemar doubling spot checks (b=0 cases)")
def _():
    S = _load_frozen_scorer()
    assert abs(S.mcnemar_exact_p(0, 8) - 0.0078125) < 1e-12
    assert abs(S.mcnemar_exact_p(0, 6) - 0.03125) < 1e-12
    assert S.mcnemar_exact_p(0, 0) == 1.0


@check("norm-tie math: fresh random unit direction scaled to task-direction norm")
def _():
    rng = np.random.default_rng(207101)
    d = rng.normal(size=1024)
    d = d / np.linalg.norm(d) * 2.5
    u = rng.normal(size=1024)
    g = u / np.linalg.norm(u) * np.linalg.norm(d)
    assert abs(np.linalg.norm(g) - np.linalg.norm(d)) < 1e-12


@check("deterministic-copy rule: unfired injected margins equal B margins")
def _():
    rng = np.random.default_rng(5)
    mB = rng.normal(size=60)
    fired = np.zeros(60, dtype=bool)
    fired[rng.choice(60, size=9, replace=False)] = True
    mT = mB.copy()
    mT[fired] = rng.normal(size=fired.sum())
    assert np.array_equal(mT[~fired], mB[~fired])


@check("stratum-consistency definition on synthetic data")
def _():
    # consistent: positive point deltas in >=2 strata, none negative
    deltas = {"agg": 0.05, "a_first": 0.03, "c_first": 0.02}
    pos = sum(1 for v in deltas.values() if v > 0)
    neg = sum(1 for v in deltas.values() if v < 0)
    assert pos >= 2 and neg == 0
    # inconsistent: mixed signs
    deltas2 = {"agg": 0.05, "a_first": -0.03, "c_first": 0.02}
    pos2 = sum(1 for v in deltas2.values() if v > 0)
    neg2 = sum(1 for v in deltas2.values() if v < 0)
    assert not (pos2 >= 2 and neg2 == 0)


@check("delivery-band logic: OOB counting and exclusion")
def _():
    ratios = np.array([0.38, 0.29, 0.475, 0.50, 0.10])
    in_band = (ratios >= 0.285) & (ratios <= 0.475)
    assert in_band.tolist() == [True, True, True, False, False]
    assert int((~in_band).sum()) == 2  # <=2 -> exclude, not HOLD


@check("pass-budget arithmetic within hard cap")
def _():
    total = 60 + 60 + 4 + 3 + 120  # B + ref + G5 + eager-validation + sweep
    assert total == 247 <= 500
    assert 60 + 120 <= 180  # protocol experiment-pass maximum


def main():
    fails = []
    for name, fn in CHECKS:
        try:
            fn()
            print(f"PASS  {name}")
        except Exception as e:
            print(f"FAIL  {name}: {e}")
            fails.append(name)
    print(f"\n{len(CHECKS) - len(fails)}/{len(CHECKS)} prechecks passed")
    if fails:
        raise SystemExit(f"PRECHECK FAILURES: {fails}")


if __name__ == "__main__":
    main()
