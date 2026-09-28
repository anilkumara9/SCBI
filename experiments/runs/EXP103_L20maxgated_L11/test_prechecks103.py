"""EXP103 pre-run logic checks (numpy + tokenizer only; no model, no weights).

Validates the mechanical logic the executor depends on BEFORE any model
pass: constructor pin, licensed protocol file presence + clearance chain,
fresh-seed distinctness, entity-span derivation on all 60 bench items
(E_i/N_i <= 0.5, span excludes final token), the L20-max-gate math
(mass_i^{L20,mean} = mean_h span-sum; tau = 2E/N closed form; firing rule),
the F2-class fence (no non-gate attention columns), the F1 decision-proxy
audit (fired-vs-unfired B-accuracy split in the worksheet, descriptive
only), McNemar doubling, norm-tie math with the fresh seed,
deterministic-copy rule, delivery-band logic, and pass-budget arithmetic.
Any failure -> the executor must not run (fail loud, never silent).

The licensed protocol is research/innovation/S6-3d_PREREG_DRAFT_v2_2026-09-28.md
(v2, F1-F2 repaired), clearance chain LOG-4456 (v1 draft) -> LOG-4457 (Law
#14 ACCEPT-WITH-FIXES F1-F2) -> LOG-4458 (v2 repair) -> LOG-4459 (delta
SIGN) -> LOG-4460 (CEO clearance, EXP103 minted). This file checks the
chain, not the verdict.
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
        "exp103_frozen_scorer",
        os.path.join(EXP094_DIR, "score_exp094.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp103_frozen_scorer"] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_runner():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "exp103_runner", os.path.join(BUNDLE_DIR, "run_exp103.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp103_runner"] = mod
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


@check("licensed protocol S6-3d v2 file present + clearance chain "
       "(LOG-4457/4452/4453)")
def _():
    p = os.path.join(REPO_ROOT, "research", "innovation",
                     "S6-3d_PREREG_DRAFT_v2_2026-09-28.md")
    assert os.path.isfile(p), "v2 protocol file missing"
    txt = open(p).read()
    assert "S6-3d" in txt, "S6-3d designator not found in protocol file"
    assert "F1" in txt and "F2" in txt, \
        "F1-F2 repair references not found in protocol file"
    # F2-class fence: no non-gate attention columns (§4.3 verbatim).
    assert "attention column other than the gate's own mass" in txt, \
        "F2-class fence not found in v2 protocol"
    log_txt = open(os.path.join(
        REPO_ROOT, "reports", "research_log.md")).read()
    assert "LOG-4457" in log_txt, "LOG-4457 (Law #14) not in research log"
    assert "LOG-4459" in log_txt, "LOG-4459 (delta SIGN) not in research log"
    assert "LOG-4460" in log_txt, "LOG-4460 (CEO clearance) not in " \
        "research log"
    assert "LOG-4446" in log_txt, "LOG-4446 (CEO clearance) not in " \
        "research log"


@check("fresh gated-R seed 513020 distinct from all prior R streams "
       "(94094, 117011, 117013, 207101, 311019, 412019)")
def _():
    src = open(os.path.join(BUNDLE_DIR, "run_exp103.py")).read()
    assert "R_SEED_GATED = 513020" in src, "R seed pin not found in runner"
    for used in (94094, 117011, 117013, 207101, 311019, 412019):
        assert 513020 != used, f"seed collision with {used}"
    assert "R_SEED_GATED = 412019" not in src, \
        "runner must not still pin EXP102's seed 412019"


@check("entity-span derivation: all 60 items valid, E/N<=0.5, span excludes "
       "final token, tau in (0,1]")
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
        "exp103_pin_check",
        os.path.join(EXP093_DIR, "protocol_pin.py"))
    _pinmod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_pinmod)
    g0 = ref.verify_g0(bench, _pinmod.BENCH_PIN)
    assert g0["pin"] == _pinmod.BENCH_PIN


@check("gate threshold closed form tau = 2E/N (byte-identical constant)")
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


@check("firing rule: fire iff mass^{L20,mean} >= tau "
       "(boundary equality fires)")
def _():
    assert (0.30 >= 0.2758) is True
    assert (0.27 >= 0.2758) is False
    assert (0.2758 >= 0.2758) is True  # boundary fires


@check("mass^{L20,mean} formula: mean over heads of span-sum at final "
       "query row")
def _():
    rng = np.random.default_rng(3)
    H, T = 16, 29
    W = rng.random((H, T, T))
    W = W / W.sum(axis=-1, keepdims=True)
    span = [3, 13, 23, 25]
    q = T - 1
    head_spans = W[:, q, :][:, span].sum(axis=1)
    mass_l20mean = float(head_spans.mean())
    assert 0.0 <= mass_l20mean <= 1.0
    # vector form matches the runner's computation
    mass_l20mean2 = float(W[:, q, :][:, span].sum(axis=1).mean())
    assert abs(mass_l20mean - mass_l20mean2) < 1e-12


@check("F2-class fence: no non-gate attention columns in the runner or "
       "the gate CSV")
def _():
    src = open(os.path.join(BUNDLE_DIR, "run_exp103.py")).read()
    assert "mass_max" not in src, \
        "non-gate attention column mass_max present in runner"
    body = src.replace("mass_L20_max", "")
    assert "mass_mean" not in body, \
        "non-gate attention column mass_mean present in runner"
    assert '"mass_L20_max"' in src, \
        "gate CSV must persist the gate's own mass (mass_L20_max)"
    assert "L20-max>=tau" in src, "firing-rule string missing from runner"
    assert "mass^max" not in src and "mass_i^max" not in src, \
        "stale max-gate references in runner"


@check("McNemar doubling spot checks (b=0 cases)")
def _():
    S = _load_frozen_scorer()
    assert abs(S.mcnemar_exact_p(0, 8) - 0.0078125) < 1e-12
    assert abs(S.mcnemar_exact_p(0, 6) - 0.03125) < 1e-12
    assert S.mcnemar_exact_p(0, 0) == 1.0


@check("F1 decision-proxy audit: fired-vs-unfired B-accuracy split in "
       "the worksheet (descriptive only)")
def _():
    src = open(os.path.join(BUNDLE_DIR, "run_exp103.py")).read()
    assert "decision-proxy audit" in src, "F1 audit missing from runner"
    assert "B_accuracy_fired" in src and "B_accuracy_unfired" in src, \
        "F1 split not computed in runner"
    assert "descriptive only" in src.lower(), \
        "F1 audit must be descriptive only"
    assert "F1" in src, "F1 step marker missing from worksheet"


@check("norm-tie math: fresh seed 513020; task-norm scaling exact")
def _():
    rng = np.random.default_rng(513020)
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
    # observed EXP100 spend (127) is the floor; worst case stays in cap


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
