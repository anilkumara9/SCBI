#!/usr/bin/env python3
"""EXP086 mock harness: full run_full_loop orchestration on synthetic
activation landscapes (zero torch, zero model passes, zero weights).

Drives run_exp086.run_full_loop with MockBackend through 13 Stage-B
scenarios (every §9 verdict row incl. all four INVALID rows, the V7b row,
and the V5-before-V7 precedence) plus the Stage-A advisory structural
checks (48 blocks, He in [0,1], verdict field None — Stage A cannot emit
a verdict by construction).

The mock's tables are wiring fixtures: they target verdict rows to exercise
the orchestration (guards, budget accounting, contrasts, Stage-2 gating,
adjudication). They never claim protocol-RNG status and are not scientific
results.

Run: python3 mock_harness.py — exit 0 iff all checks pass.
"""

import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import exp086_guards as G
import exp086_henrici as H
import exp086_statistics as S
import exp086_verdicts as V
import run_exp086 as RUN
from run_exp086 import Backend

N = 60


# ---------------------------------------------------------------------------
# Deterministic fixture builders
# ---------------------------------------------------------------------------

def build_tables(n10, n01, n00, n11, r10, r01, r00, r11, p10, p01, p00, p11):
    """Per-item arm correctness lists with a consistent v̂_1 margin.

    v1[i] = 1 for i < m1 where m1 = n10+n11 (= r10+r11 = p10+p11, asserted).
    vrand/v3/perm are assigned conditional on v1 to realize the three paired
    tables exactly.
    """
    m1 = n10 + n11
    assert r10 + r11 == m1 and p10 + p11 == m1, "v1 margin inconsistent"
    assert n01 + n00 == N - m1 and r01 + r00 == N - m1 and p01 + p00 == N - m1
    v1 = [i < m1 for i in range(N)]

    def cond(t10, t01):
        t = [None] * N
        ones = [i for i in range(N) if v1[i]]
        zeros = [i for i in range(N) if not v1[i]]
        for i in ones[:t10]:
            t[i] = False
        for i in ones[t10:]:
            t[i] = True
        for i in zeros[:t01]:
            t[i] = True
        for i in zeros[t01:]:
            t[i] = False
        return t

    return {"v1": v1, "vrand": cond(n10, n01), "v3": cond(r10, r01),
            "perm": cond(p10, p01)}


def make_spec(**kw):
    spec = {
        "base_wrong": 20,          # wrong-at-baseline count (first k items)
        "aborted": set(),          # aborted item indices
        "s_full": (3.0, 1.0, 0.8),  # sigma hats (non-aborted)
        "s_aborted": (1.0, 1.0, 1.0),
        "alpha": 0.4,              # |<v1,nhat>| (float or list)
        "dz": 0.01,                # ||Dz||_2 for vrand@0.45 (apparatus)
        "tamper": False,           # V1: mutate state dict post-snapshot
        "tables": None,            # build_tables(...) output
    }
    spec.update(kw)
    return spec


# ---------------------------------------------------------------------------
# Mock backend
# ---------------------------------------------------------------------------

class MockBackend(Backend):
    """Synthetic backend. Directions are tags; outcomes come from the spec."""

    def __init__(self, spec):
        self.spec = spec
        self._sd_calls = 0
        import numpy as np
        rng = np.random.default_rng(12345)
        self._sd = {"mock_layer": rng.standard_normal(64)}

    # -- Stage A / guard --
    def load_state_dict_readonly(self):
        self._sd_calls += 1
        import numpy as np
        if self.spec["tamper"] and self._sd_calls > 1:
            return {"mock_layer": self._sd["mock_layer"] + 1.0}  # V1 tamper
        return dict(self._sd)

    # -- Stage B --
    def build_probe(self, record, i):
        return {"i": i}

    def baseline_forward(self, probe):
        i = probe["i"]
        wrong = i < self.spec["base_wrong"]
        logits = [0.0, 1.0] if wrong else [1.0, 0.0]
        return (not wrong, logits, [0.0, 0.0, 0.0, 0.0])

    def power_iteration(self, probe, h):
        i = probe["i"]
        s = self.spec["s_aborted"] if i in self.spec["aborted"] \
            else self.spec["s_full"]
        return {"v": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
                "s": list(s),
                "rayleigh": [[s[0]] * 12, [s[1]] * 12, [s[2]] * 12],
                "n_iters": [12, 12, 12]}

    def decision_normal_vjp(self, probe, h):
        i = probe["i"]
        a = self.spec["alpha"]
        a = a[i] if isinstance(a, list) else a
        return [a, math.sqrt(max(0.0, 1 - a * a)), 0.0, 0.0]

    def apply_sign_rule(self, item_idx, n_hat):
        # Mock: directions are spec-table tags; the sign flip is a no-op for
        # outcomes, but we mirror the real path and return signed v̂_1 for
        # the ĉ diagnostic (F1 fix).
        v1 = [1.0, 0.0, 0.0, 0.0]
        s = 1.0 if sum(a * b for a, b in zip(v1, n_hat)) >= 0 else -1.0
        return [s * x for x in v1]

    def _arm_correct(self, probe_i, direction, eps_frac):
        k = 0 if abs(eps_frac - 0.15) < 1e-9 else 1
        t = self.spec["tables"]
        if isinstance(direction, tuple) and direction[0] == "permuted":
            return t["perm"][probe_i] if k == 0 else t["perm"][probe_i]
        if direction in ("v1", "v2", "v3", "bagg"):
            return t[direction][probe_i] if direction in t else \
                (probe_i >= self.spec["base_wrong"])
        if direction.startswith("vrand"):
            return t["vrand"][probe_i]
        raise ValueError(f"mock: unknown direction {direction!r}")

    def inject_and_eval(self, probe, h, direction, eps_frac):
        i = probe["i"]
        correct = self._arm_correct(i, direction, eps_frac)
        k = 0 if abs(eps_frac - 0.15) < 1e-9 else 1
        is_vrand = (not isinstance(direction, tuple)
                    and direction.startswith("vrand"))
        if is_vrand and k == 1:
            logits = [1.0 + self.spec["dz"], 0.0]  # apparatus movement
        else:
            logits = [1.0, 0.0]
        return bool(correct), logits

    def stage2_derangement(self, n):
        return [(i + 1) % n for i in range(n)]  # cyclic shift: der(i) != i


# ---------------------------------------------------------------------------
# Scenarios: one per verdict row (+ precedence + tamper)
# ---------------------------------------------------------------------------

def scenario_continue():
    t = build_tables(16, 2, 10, 32,   # primary: strong win
                     12, 3, 9, 36,    # rank: gradient win
                     10, 2, 10, 38)   # permuted: item-specific win
    return make_spec(tables=t), "CONTINUE", 7380


def scenario_kill_v5():
    # ĉ kill-first preempts an otherwise-winning primary (precedence test)
    t = build_tables(16, 2, 10, 32, 12, 3, 9, 36, 10, 2, 10, 38)
    alphas = [0.5] + [0.02] * 59  # ĉ=0.028<0.1, E=1/60<10%
    return make_spec(tables=t, alpha=alphas), "KILL", 7380


def scenario_kill_v6():
    # primary (2,8,25,25): Tango UCI < 0.05 (gain excluded); m1=27 consistent
    t = build_tables(2, 8, 25, 25, 5, 6, 27, 22, 4, 5, 28, 23)
    return make_spec(tables=t), "KILL", 7260


def scenario_pivot_v8():
    t = build_tables(16, 2, 10, 32,   # primary wins
                     2, 5, 7, 46,     # rank: CI below +0.05, point<0 (excluded)
                     4, 4, 8, 44)     # permuted: moot (rank fails first)
    return make_spec(tables=t), "PIVOT", 7380


def scenario_held_v9():
    t = build_tables(16, 2, 10, 32,   # primary wins
                     6, 5, 7, 42,     # rank straddles 0
                     10, 2, 10, 38)   # permuted wins (rank fails first)
    return make_spec(tables=t), "HELD", 7380


def scenario_held_v7b():
    t = build_tables(16, 2, 10, 32,   # primary wins
                     12, 3, 9, 36,    # rank wins
                     4, 5, 7, 44)     # permuted FAILS -> V7b
    return make_spec(tables=t), "HELD", 7380


def scenario_held_v10():
    t = build_tables(5, 3, 22, 30,    # primary straddles (no win)
                     4, 5, 20, 31, 3, 4, 21, 32)
    alphas = [0.3] * 12 + [0.02] * 48  # ĉ=0.076<0.1, E=0.20≥10%
    return make_spec(tables=t, alpha=alphas), "HELD", 7260


def scenario_held_v11():
    t = build_tables(16, 2, 10, 32, 12, 3, 9, 36, 4, 4, 8, 44)
    # s1/s2=1.15 (no abort) but s1/s3=1.15 < 1.2 (rank undefined)
    return make_spec(tables=t, s_full=(1.15, 1.0, 1.0)), "HELD", 7380


def scenario_held_v12():
    t = build_tables(5, 3, 22, 30,    # primary straddles +0.05
                     4, 5, 20, 31, 3, 4, 21, 32)
    return make_spec(tables=t), "HELD", 7260


def scenario_invalid_v2():
    t = build_tables(16, 2, 10, 32, 12, 3, 9, 36, 10, 2, 10, 38)
    return make_spec(tables=t, base_wrong=10), "INVALID", 60


def scenario_invalid_v3():
    t = build_tables(16, 2, 10, 32, 12, 3, 9, 36, 10, 2, 10, 38)
    return make_spec(tables=t, aborted=set(range(40))), "INVALID", 6860


def scenario_invalid_v4():
    t = build_tables(16, 2, 10, 32, 12, 3, 9, 36, 10, 2, 10, 38)
    return make_spec(tables=t, dz=0.0), "INVALID", 7260


def scenario_invalid_v1():
    t = build_tables(16, 2, 10, 32, 12, 3, 9, 36, 10, 2, 10, 38)
    return make_spec(tables=t, tamper=True), "INVALID", None


SCENARIOS = [
    ("continue/V7", scenario_continue),
    ("kill/V5-preempts-V7", scenario_kill_v5),
    ("kill/V6", scenario_kill_v6),
    ("pivot/V8", scenario_pivot_v8),
    ("held/V9", scenario_held_v9),
    ("held/V7b", scenario_held_v7b),
    ("held/V10", scenario_held_v10),
    ("held/V11", scenario_held_v11),
    ("held/V12", scenario_held_v12),
    ("invalid/V2-headroom", scenario_invalid_v2),
    ("invalid/V3-abortfrac", scenario_invalid_v3),
    ("invalid/V4-apparatus", scenario_invalid_v4),
    ("invalid/V1-tamper", scenario_invalid_v1),
]


def run_all(out_dir):
    checks = []

    def check(name, cond, detail=""):
        checks.append((name, bool(cond), detail))

    for name, builder in SCENARIOS:
        spec, expect_verdict, expect_used = builder()
        backend = MockBackend(spec)
        budget = G.PassBudget()
        logs = []
        try:
            with tempfile.TemporaryDirectory() as td:
                results, (verdict, evidentiary, detail) = RUN.run_full_loop(
                    backend, budget, td, log=logs.append)
            got = verdict
            used_ok = (expect_used is None) or (budget.used == expect_used)
            check(f"mock/{name}: verdict={verdict}",
                  got == expect_verdict,
                  f"expected {expect_verdict}, got {got}; {detail[:120]}")
            if expect_used is not None:
                check(f"mock/{name}: budget used={budget.used}",
                      used_ok, f"expected {expect_used}, got {budget.used}")
        except G.InvalidRunError as e:
            check(f"mock/{name}: verdict=INVALID",
                  expect_verdict == "INVALID",
                  f"InvalidRunError: {e}")
            if expect_used is not None:
                check(f"mock/{name}: budget used={budget.used}",
                      budget.used == expect_used,
                      f"expected {expect_used}, got {budget.used}")
        except Exception as e:
            check(f"mock/{name}: no unexpected exception", False,
                  f"{type(e).__name__}: {e}")

    # ---- Stage-A structural checks (synthetic 48-block state dict) ----
    try:
        import numpy as np
        rng = np.random.default_rng(777)
        sd = {}
        for i in range(24):
            sd[f"gpt_neox.layers.{i}.attention.dense.weight"] = \
                rng.standard_normal((1024, 1024))
            qkv = rng.standard_normal((3072, 1024))
            sd[f"gpt_neox.layers.{i}.attention.query_key_value.weight"] = qkv
        t0ok = True
        rep = H.stage_a_screen(sd)
        hes = [b["He"] for b in rep["blocks"]]
        check("mock/stage-a: 48 blocks screened", rep["n_blocks"] == 48,
              f"got {rep['n_blocks']}")
        check("mock/stage-a: all He in [0,1]",
              all(0.0 <= h <= 1.0 for h in hes),
              f"He range ({min(hes):.4f},{max(hes):.4f})")
        check("mock/stage-a: verdict field is None (no verdict by design)",
              rep["verdict"] is None, f"verdict={rep['verdict']!r}")
        check("mock/stage-a: status is ADVISORY",
              "ADVISORY" in rep["status"], rep["status"][:60])
        kinds = {b["kind"] for b in rep["blocks"]}
        check("mock/stage-a: O direct + V fused-interleaved provenance",
              kinds == {"direct", "fused-interleaved"}, f"kinds={kinds}")
        # rectangular block must be refused loudly (G1)
        try:
            H.henrici_index(rng.standard_normal((4, 12)), name="rect-test")
            check("mock/stage-a: rectangular refused", False, "no raise")
        except G.BlockSelectionError:
            check("mock/stage-a: rectangular refused", True)
        # frozen-backbone guard around Stage A on the synthetic dict
        guard = G.FrozenBackboneGuard()
        h0 = guard.snapshot_before(sd)
        H.stage_a_screen(sd)
        h1 = guard.verify_after(sd)
        check("mock/stage-a: Δθ=0 guard passes on read-only screen",
              h0 == h1, f"{h0[:12]} vs {h1[:12]}")
    except Exception as e:
        check("mock/stage-a: no unexpected exception", False,
              f"{type(e).__name__}: {e}")

    return checks


def main():
    with tempfile.TemporaryDirectory() as td:
        checks = run_all(td)
    npass = sum(1 for _, ok, _ in checks if ok)
    nfail = len(checks) - npass
    for name, ok, detail in checks:
        print(("ok - " if ok else "FAIL - ") + name +
              ("" if ok else f" :: {detail}"))
    print(f"mock harness: {npass}/{len(checks)} checks pass")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
