#!/usr/bin/env python3
"""EXP084 mock-model end-to-end harness (CPU, zero weights, zero torch).

Runs the ENTIRE run_exp084.run_full_loop orchestration on synthetic
activation landscapes — the full arm wiring, guard logic, pass-budget
accounting, tie validation, table gate, and verdict adjudication — with
no model, no GPU, and no torch.

Per-item synthetic profile (dim 8):
    M(o) = M0 + L*t + C2*t^2 - q*t^3,   t = (u . o)
with deterministic per-item (L, C2, q, u) and deterministic
pseudo-isotropic random directions from a pure-Python LCG. The mock never
claims to be the protocol RNG (torch-exclusive on the GPU node); it is a
wiring fixture whose scenarios are VERIFIED by execution below.

Scenarios (each exercised through run_full_loop; per the LOG-269 D2
binding, every scenario runs the GPU-node two-invocation pattern:
invocation 1 = P0 pre-pass, which MUST archive + halt verdict-clean with
BaselinePrepassHalt; invocation 2 = full loop, replaying the archive with
INVALID(ii) enforced bit-for-bit):
  continue  - Newton wins every conjunct            -> CONTINUE
  kill      - Newton loses to GD-costfair           -> KILL(flagship, cost-fair)
  f2fail    - apparatus dead (gradient dir worst)   -> INVALID/UNINFORMATIVE-PROXY
  few       - n_defined=8                           -> INVALID/UNDEFINED-LANDSCAPE
  ties      - engineered |d| tie                     -> NonTestableDataError (loud)
  tablegate - n_defined=20 (no exact table)         -> MissingSpearmanTableError
  tamper    - state_hash != guard                    -> InvalidRunError("i")
  baseline  - first run: archives + halts verdict-clean (pre-pass,
              BaselinePrepassHalt, LOG-269 D2); identical rerun replays
              the archive and completes the full loop; shifted M0 rerun
              -> InvalidRunError("ii")

run_all(workdir) executes every scenario and returns [(name, ok, detail)].
Exit 0 iff all pass when run as a script.
"""

import hashlib
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run_exp084 as RUN
import exp084_statistics as S
import exp084_spearman as SP

MASTER_SEED = 20260924
N_ITEMS = 24
DIM = 8


# --- deterministic pure-python primitives ------------------------------------
def _lcg_stream(seed):
    s = seed & 0x7FFFFFFF
    while True:
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        yield s


def _gaussians(seed, n):
    """Box-Muller normals from the LCG stream. Deterministic."""
    out = []
    st = _lcg_stream(seed)
    while len(out) < n:
        u1 = (next(st) + 1) / 0x80000001
        u2 = (next(st) + 1) / 0x80000001
        r = math.sqrt(-2.0 * math.log(u1))
        out.append(r * math.cos(2.0 * math.pi * u2))
        if len(out) < n:
            out.append(r * math.sin(2.0 * math.pi * u2))
    return out[:n]


def _unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return tuple(x / n for x in v)


def _derangement(n, seed):
    """Fisher-Yates derangement from the LCG (mock-only; the protocol
    derangement is torch-based on the GPU node)."""
    st = _lcg_stream(seed)
    while True:
        perm = list(range(n))
        for i in range(n - 1, 0, -1):
            j = next(st) % (i + 1)
            perm[i], perm[j] = perm[j], perm[i]
        if all(p != i for i, p in enumerate(perm)):
            return perm


# --- scenario parameter sets: (L, C2, q, M0) per item ------------------------
# kappa_hat_dir = 2*C2 exactly (odd cubic terms cancel in central differences).
def _scenario_params(scenario):
    if scenario in ("continue", "ties"):
        params, j = [], 0
        for i in range(18):  # Newton-defined: L=4c => Newton edge = c, dose up
            c = (1.0, 2.0, 4.0, 8.0)[i % 4] * (1.0 + 0.01 * j)
            j += 1
            params.append((4.0 * c, -c, 0.0, 0.5 + 0.01 * i))
        for i in range(18, 24):  # convex-undefined (F2 support)
            params.append((1.0, 1.0, 0.0, 0.5 + 0.01 * i))
        if scenario == "ties":
            params[1] = params[0]  # identical twins -> engineered tie
        return params
    if scenario == "kill":
        # Cubic punishes Newton's long step; GD-1 stays healthy (F2 passes).
        params = [(2.2, -0.3 * (1.0 + 0.001 * i), 0.5, 0.5 + 0.01 * i)
                  for i in range(18)]
        params += [(1.0, 1.0, 0.0, 0.5 + 0.01 * i) for i in range(18, 24)]
        return params
    if scenario == "f2fail":
        # Defined: f(1) is the unique global min on [-1,1] -> gradient dir
        # worst -> d_i < 0. Undefined (convex-uphill): f(t)=t+t^2-3t^3 also
        # has d_i <= 0 (max at t_r=1). All d_i <= 0 -> F2 p = 1.0 -> dead.
        params = [(1.0, -0.5, 1.5, 0.5 + 0.01 * i) for i in range(12)]
        params += [(1.0, 1.0, 3.0, 0.5 + 0.01 * i) for i in range(12, 24)]
        return params
    if scenario == "few":
        params = [(1.0, -0.5, 0.0, 0.5 + 0.01 * i) for i in range(8)]
        params += [(1.0, 1.0, 0.0, 0.5 + 0.01 * i) for i in range(8, 24)]
        return params
    if scenario == "tablegate":
        params = []
        for i in range(20):
            c = (1.0, 2.0, 4.0, 8.0)[i % 4] * (1.0 + 0.01 * i)
            params.append((4.0 * c, -c, 0.0, 0.5 + 0.01 * i))
        params += [(1.0, 1.0, 0.0, 0.5 + 0.01 * i) for i in range(20, 24)]
        return params
    raise ValueError(f"unknown scenario {scenario!r}")


# --- mock backend -------------------------------------------------------------
class MockBackend:
    """Synthetic activation backend implementing the run_full_loop interface."""

    def __init__(self, scenario, budget, log, tamper=False, m0_shift=0.0):
        self.scenario = scenario
        self.budget = budget
        self.log = log
        self.tamper = tamper
        params = _scenario_params(scenario)
        self.coef = [(L, C2, q) for (L, C2, q, _) in params]
        self.M0 = [m0 + m0_shift for (_, _, _, m0) in params]
        self.u = [_unit(_gaussians(MASTER_SEED + 1000 + i, DIM))
                  for i in range(N_ITEMS)]
        self.rhat = [_unit(_gaussians(MASTER_SEED + i, DIM))
                     for i in range(N_ITEMS)]
        if scenario == "ties":
            self.rhat[1] = self.rhat[0]
        self._der = _derangement(N_ITEMS, MASTER_SEED)

    # -- interface --
    def set_prompts(self, prompts):
        pass

    def state_hash(self):
        h = hashlib.sha256()
        for (L, C2, q), m0, u in zip(self.coef, self.M0, self.u):
            h.update(repr((round(L, 12), round(C2, 12), round(q, 12),
                           round(m0, 12))).encode())
            h.update(repr(tuple(round(x, 12) for x in u)).encode())
        d = h.hexdigest()
        if self.tamper:
            d = ("0" if d[0] != "0" else "1") + d[1:]
        return d

    def _t(self, i, off):
        return sum(a * b for a, b in zip(self.u[i], off))

    def _M(self, i, off):
        L, C2, q = self.coef[i]
        t = self._t(i, off)
        return self.M0[i] + L * t + C2 * t * t - q * t ** 3

    def _grad(self, i, off):
        L, C2, q = self.coef[i]
        t = self._t(i, off)
        s = L + 2 * C2 * t - 3 * q * t * t
        return tuple(s * x for x in self.u[i])

    def p0(self, i):
        self.budget.charge_fwd()
        return self.M0[i], (i, (0.0,) * DIM)

    def grad_from_ctx(self, ctx):
        self.budget.charge_bwd()
        i, off = ctx
        return self._grad(i, off)

    def eval_margin(self, i, off):
        self.budget.charge_fwd()
        return self._M(i, off)

    def eval_margin_and_grad(self, i, offset):
        self.budget.charge_fwd()
        self.budget.charge_bwd()
        return self._M(i, offset), self._grad(i, offset)

    def random_direction(self, i):
        return self.rhat[i]

    def derangement(self):
        return list(self._der)

    # -- vector ops on tuples --
    @staticmethod
    def vadd(a, b):
        return tuple(x + y for x, y in zip(a, b))

    @staticmethod
    def vscale(a, c):
        return tuple(x * c for x in a)

    @staticmethod
    def vneg(a):
        return tuple(-x for x in a)

    @staticmethod
    def vnorm(a):
        return math.sqrt(sum(x * x for x in a))


# --- scenario execution -------------------------------------------------------
def run_scenario(scenario, workdir, tamper=False, m0_shift=0.0,
                 pinned_sha256=None, log=None):
    """Run ONE invocation of run_full_loop on a mock scenario.

    A single invocation. On the first invocation (no baseline archive in
    `workdir`), check_identity archives M0 and raises BaselinePrepassHalt
    (LOG-269 D2 binding: verdict-clean pre-pass, no scientific arms). A
    second invocation replays the archive and runs the full loop.
    Returns (record, budget, log_lines)."""
    logs = []
    _log = log or logs.append
    budget = RUN.PassBudget()
    backend = MockBackend(scenario, budget, _log,
                          tamper=tamper, m0_shift=m0_shift)
    pin = pinned_sha256 if pinned_sha256 is not None else backend.state_hash()
    base = os.path.join(workdir, f"baseline_{scenario}.json")
    record = RUN.run_full_loop(backend, budget, workdir, _log,
                               records_path=None, baseline_path=base,
                               pinned_sha256=pin)
    return record, budget, logs


def run_scenario_full(scenario, workdir, **kw):
    """Two-invocation mock run: the GPU-node pre-pass pattern.

    Invocation 1: P0 pre-pass — archives the baseline and MUST halt
    verdict-clean with BaselinePrepassHalt (LOG-269 D2). Invocation 2:
    replays the archive, INVALID(ii) enforced bit-for-bit, full loop to
    its verdict or loud halt. Raises AssertionError if invocation 1 does
    not halt (the guard must be live, never vacuous).
    Returns (record, budget, log_lines) from invocation 2."""
    try:
        run_scenario(scenario, workdir, **kw)
    except RUN.BaselinePrepassHalt:
        pass
    else:
        raise AssertionError(
            f"{scenario}: pre-pass invocation did not halt verdict-clean "
            "(BaselinePrepassHalt expected)")
    return run_scenario(scenario, workdir, **kw)


def run_all(workdir):
    """Execute every mock scenario. Returns [(name, ok, detail)]."""
    out = []

    def rec(name, ok, detail=""):
        out.append((name, bool(ok), str(detail)))

    # 1. continue -> CONTINUE, exact budget accounting
    try:
        r, b, _ = run_scenario_full("continue", workdir)
        v = r["verdict"]["label"]
        rec("continue: verdict CONTINUE", v == "CONTINUE", f"got {v}")
        rec("continue: bwd == 72", b.bwd == 72, f"bwd={b.bwd}")
        rec("continue: fwd <= 240", b.fwd <= 240, f"fwd={b.fwd}")
        # exact budget model: 24*8 base + 18 Newton + 18 permuted (donor-defined)
        rec("continue: fwd == 228 (exact budget model)", b.fwd == 228,
            f"fwd={b.fwd}")
        rec("continue: n_e_contrast == 13 (paired set)",
            r["results"]["n_e_contrast"] == 13,
            f"n_e={r['results']['n_e_contrast']}")
        rec("continue: n_e_evaluated == 18 (arm spend)",
            r["results"]["n_e_evaluated"] == 18,
            f"n_eval={r['results']['n_e_evaluated']}")
        rec("continue: n_defined=18", r["results"]["n_defined"] == 18,
            f"n={r['results']['n_defined']}")
    except Exception as e:
        rec("continue: verdict CONTINUE", False, f"{type(e).__name__}: {e}")

    # 2. kill -> KILL(flagship, cost-fair)
    try:
        r, b, _ = run_scenario_full("kill", workdir)
        v = r["verdict"]["label"]
        rec("kill: verdict KILL(flagship, cost-fair)",
            v == "KILL(flagship, cost-fair)", f"got {v}")
    except Exception as e:
        rec("kill: verdict KILL(flagship, cost-fair)", False,
            f"{type(e).__name__}: {e}")

    # 3. f2fail -> INVALID/UNINFORMATIVE-PROXY
    try:
        r, _, _ = run_scenario_full("f2fail", workdir)
        v = r["verdict"]["label"]
        rec("f2fail: verdict INVALID/UNINFORMATIVE-PROXY",
            v == "INVALID/UNINFORMATIVE-PROXY", f"got {v}")
    except Exception as e:
        rec("f2fail: verdict INVALID/UNINFORMATIVE-PROXY", False,
            f"{type(e).__name__}: {e}")

    # 4. few -> INVALID/UNDEFINED-LANDSCAPE
    try:
        r, _, _ = run_scenario_full("few", workdir)
        v = r["verdict"]["label"]
        rec("few: verdict INVALID/UNDEFINED-LANDSCAPE",
            v == "INVALID/UNDEFINED-LANDSCAPE", f"got {v}")
    except Exception as e:
        rec("few: verdict INVALID/UNDEFINED-LANDSCAPE", False,
            f"{type(e).__name__}: {e}")

    # 5. ties -> loud halt (no silent drop, no tie-break)
    try:
        run_scenario_full("ties", workdir)
        rec("ties: loud halt", False, "no exception raised")
    except S.NonTestableDataError as e:
        rec("ties: loud halt", True, f"NonTestableDataError: {e}")
    except Exception as e:
        rec("ties: loud halt", False,
            f"wrong exception {type(e).__name__}: {e}")

    # 6. tablegate -> loud halt before verdict machinery
    try:
        run_scenario_full("tablegate", workdir)
        rec("tablegate: loud halt", False, "no exception raised")
    except SP.MissingSpearmanTableError as e:
        rec("tablegate: loud halt", True, "MissingSpearmanTableError")
    except Exception as e:
        rec("tablegate: loud halt", False,
            f"wrong exception {type(e).__name__}: {e}")

    # 7. tamper -> INVALID(i) before any pass
    try:
        clean = MockBackend("continue", RUN.PassBudget(), lambda m: None)
        run_scenario("continue", workdir, tamper=True,
                     pinned_sha256=clean.state_hash())
        rec("tamper: INVALID(i)", False, "no exception raised")
    except RUN.InvalidRunError as e:
        rec("tamper: INVALID(i)", e.invalid_row == "i",
            f"row={e.invalid_row}")
    except Exception as e:
        rec("tamper: INVALID(i)", False,
            f"wrong exception {type(e).__name__}: {e}")

    # 8. baseline (LOG-269 D2 binding): first run archives M0 then halts
    #    verdict-clean (pre-pass — no scientific arms, no verdict);
    #    identical re-run replays the archive and completes the full loop;
    #    shifted-M0 re-run -> INVALID(ii)
    bdir = os.path.join(workdir, "baseline_test")
    os.makedirs(bdir, exist_ok=True)
    arch = os.path.join(bdir, "baseline_continue.json")
    try:
        run_scenario("continue", bdir)  # first run: archive + halt
        rec("baseline: first run archives + halts verdict-clean "
            "(BaselinePrepassHalt)", False, "no exception raised")
        _first_ok = False
    except RUN.BaselinePrepassHalt as e:
        _first_ok = True
        rec("baseline: first run archives + halts verdict-clean "
            "(BaselinePrepassHalt)",
            os.path.isfile(arch) and "re-run" in str(e).lower(),
            str(e)[:80])
        rec("baseline: pre-pass halt is verdict-clean, not INVALID",
            not isinstance(e, RUN.InvalidRunError),
            type(e).__name__)
    except Exception as e:
        _first_ok = False
        rec("baseline: first run archives + halts verdict-clean "
            "(BaselinePrepassHalt)", False,
            f"wrong exception {type(e).__name__}: {e}")
    if _first_ok:
        try:
            r, _, _ = run_scenario("continue", bdir)  # re-run: replay
            rec("baseline: identical re-run completes full loop "
                "(identity enforced)",
                r["verdict"]["label"] == "CONTINUE",
                f"got {r['verdict']['label']}")
        except Exception as e:
            rec("baseline: identical re-run completes full loop "
                "(identity enforced)", False,
                f"{type(e).__name__}: {e}")
        try:
            shifted = MockBackend("continue", RUN.PassBudget(),
                                  lambda m: None, m0_shift=0.001)
            run_scenario("continue", bdir, m0_shift=0.001,
                         pinned_sha256=shifted.state_hash())
            rec("baseline: shifted rerun INVALID(ii)", False, "no exception")
        except RUN.InvalidRunError as e:
            rec("baseline: shifted rerun INVALID(ii)", e.invalid_row == "ii",
                f"row={e.invalid_row}")
        except Exception as e:
            rec("baseline: shifted rerun INVALID(ii)", False,
                f"wrong exception {type(e).__name__}: {e}")

    return out


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        results = run_all(td)
    n_ok = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(("ok   " if ok else "FAIL ") + name
              + ("" if ok else f" :: {detail}"))
    print(f"\n{n_ok}/{len(results)} mock scenarios pass")
    sys.exit(0 if n_ok == len(results) else 1)
