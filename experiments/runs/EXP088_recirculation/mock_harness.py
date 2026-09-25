#!/usr/bin/env python3
"""EXP088 mock-model end-to-end harness (CPU, zero weights, zero torch).

Runs the ENTIRE run_exp088.run_full_loop orchestration on synthetic
fixtures — the Stage-A screen + F7 INVALID gate, the F2 RAND-vector
once-per-run draw, the Stage-B discrimination loop, the DeltaTheta pre/post
guard, pass-budget accounting, and verdict adjudication — with no model,
no GPU, and no torch.

Synthetic fixtures (deterministic, pure Python):
  Stage A: per-token NLLs. Baseline NLL = BASE_NLL for every token; a
      recirculated block for pair (s, d) returns BASE_NLL - shift[(s,d)].
      The runner's DeltaPPL = mean(exp(base) - exp(rec)) then has the
      scripted sign/ordering. Baseline repeat 1 uses BASE_NLL; repeat 2
      uses BASE_NLL - repeat_shift (0 by default -> identical repeats ->
      eps = 0).
  Stage B: scripted per-arm correctness lists. probe_answer_logits returns
      (2.0, 1.0) for a correct item, (1.0, 2.0) otherwise; the runner's
      EXP077 section-4 decision rule turns those into the scripted booleans.

The mock never claims to be the protocol RNG or the F8 ramping applier
(torch-exclusive on the GPU node); it is a wiring fixture whose scenarios
are VERIFIED by execution below.

Scenarios (each through run_full_loop with blocks_override + the REAL
pinned probe records, so the F11 preflight + EXP084-D1 deviation path are
exercised too):
  stageA_invalid    - all pair shifts <= 0             -> StageAInvalid; no
                      Stage-B calls; INVALID record written via the shared
                      write_invalid_record path
  stageA_noisefloor - repeat_shift > 0 gives eps > 0; small positive pair
                      shifts below eps                 -> StageAInvalid via
                      the noise-floor rule (not via negativity)
  stageA_tie        - two pairs tie for argmax         -> ValueError (loud)
  continue          - primary Supported, D->S > RAND   -> CONTINUE
  kill_dead         - primary contrast dead (U < 0.05) -> KILL
  kill_rand         - primary inconclusive, D->S <= RAND on the point
                                                       -> KILL (secondary)
  pivot_helps       - primary inconclusive, an arm beats baseline
                                                       -> PIVOT
  held              - primary inconclusive, nothing beats baseline -> HELD
  b2_override       - primary Supported but monotone gain curve
                                                       -> PIVOT (B2)
  b4_tension        - primary d_hat <= 0 yet U >= 0.05 (wide CI),
                      D->S > RAND on the point, no arm beats baseline
                                                       -> HELD (documents
                      the B4-vs-F5 reconciliation: not KILL)
  tamper            - state_hash changes mid-run       -> DeltaThetaError
  wiring/*          - leak-spec threading, RAND drawn exactly once, exact
                      call accounting (1640), Stage-B geometries

run_all(workdir) executes every scenario and returns [(name, ok, detail)].
Exit 0 iff all pass when run as a script.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run_exp088 as RUN  # noqa: E402

BASE_NLL = 2.5
MOCK_BLOCKS = [[101, 202, 303, 404, 505, 606, 707, 808,
                909, 1010, 1111, 1212, 1313, 1414, 1515, 1616]] * 4
N_BLOCKS = len(MOCK_BLOCKS)
RECORDS_PATH = os.path.join(HERE, "..", "EXP077_cone_vs_line",
                            "exp077_instance_records.json")

GRID = [(d + off, d) for d in (4, 6, 8) for off in (4, 6, 8)]  # (s, d)
ALPHAS = (0.07, 0.10, 0.15)


def _bits(on):
    """60-item correctness list with True at the given indices."""
    on = set(on)
    return [i in on for i in range(60)]


class MockBackend:
    """Synthetic backend. The scenario dict controls Stage-A shifts,
    Stage-B correctness, baseline-repeat noise, and tampering."""

    def __init__(self, budget, scenario):
        self.budget = budget
        self.sc = scenario
        self._hash_calls = 0
        self._rand_draws = 0
        self._base_block_calls = 0
        self._pos = {}
        self.leak_specs_seen = []
        self.stage_b_calls = 0

    # -- backend interface (mirrors TorchBackend) --
    def state_hash(self):
        self._hash_calls += 1
        if self.sc.get("tamper") and self._hash_calls > 1:
            return "mockhash-tampered"
        return "mockhash"

    def rand_unit_vector(self):
        self._rand_draws += 1
        return ("mock-rand-vector",)

    def corpus_block_nlls(self, token_ids, leak_spec):
        if leak_spec is None:
            self.budget.charge(1)
            self._base_block_calls += 1
            # Baseline repeat 2 = block-calls [N_BLOCKS, 2*N_BLOCKS).
            shift = (self.sc.get("repeat_shift", 0.0)
                     if self._base_block_calls > N_BLOCKS else 0.0)
            return [BASE_NLL - shift] * (len(token_ids) - 1)
        self.budget.charge(2)
        self.leak_specs_seen.append(dict(leak_spec))
        shift = self.sc.get("pair_shifts", {}).get(
            (leak_spec["s"], leak_spec["d"]), 0.0)
        return [BASE_NLL - shift] * (len(token_ids) - 1)

    def probe_answer_logits(self, item, leak_spec):
        self.stage_b_calls += 1
        if leak_spec is None:
            self.budget.charge(1)
            key = None
        else:
            self.budget.charge(2)
            self.leak_specs_seen.append(dict(leak_spec))
            key = (leak_spec["kind"], leak_spec["alpha"])
        pos = self._pos.get(key, 0)
        self._pos[key] = pos + 1
        return (2.0, 1.0) if self.sc["arms_correct"][key][pos] else (1.0, 2.0)


def _scenario_arms(base_on, arms):
    d = {None: _bits(base_on)}
    for k, on in arms.items():
        d[k] = _bits(on)
    return d


def _run_one(workdir, name, scenario, expect):
    """Run one scenario through the full orchestration."""
    logs = []

    def log(m):
        logs.append(m)

    budget = RUN.PassBudget()
    backend = MockBackend(budget, scenario)
    try:
        rec = RUN.run_full_loop(backend, budget, workdir, log, None,
                                RECORDS_PATH,
                                blocks_override=MOCK_BLOCKS)
        outcome = ("verdict", rec["verdict"]["label"])
    except RUN.StageAInvalid as e:
        # exercise the shared INVALID-record path (same code as cmd_run)
        rec = RUN.write_invalid_record(backend, budget, workdir, log, e)
        outcome = ("invalid", rec["verdict"]["label"])
    except Exception as e:  # noqa: BLE001 - scenarios assert on the type
        outcome = ("raised", type(e).__name__)
    ok = (outcome == expect)
    return (name, ok, f"outcome={outcome} expect={expect}")


def _scenarios():
    """(name, scenario, expected-outcome) list."""
    win = {p: (-0.01 if p != (10, 6) else 0.05) for p in GRID}
    base30 = list(range(30))

    # continue: primary b=14,c=2 (d_hat=0.20, Tango L>0.05 verified below),
    # D->S (48/60) > RAND (40/60) on the point.
    both = set(range(34))
    d2s_idx = sorted(both | set(range(34, 48)))
    s2d_idx = sorted(both | {48, 49})
    rand_idx = sorted(both | set(range(34, 40)))
    arms_c = {}
    for a in ALPHAS:
        arms_c[("D2S", a)] = d2s_idx
        arms_c[("S2D", a)] = s2d_idx
        arms_c[("RAND", a)] = rand_idx

    # kill_dead: b=2, c=12 -> d_hat=-1/6, Tango U < 0.05.
    arms_k = {}
    for a in ALPHAS:
        arms_k[("D2S", a)] = sorted(set(range(28)) | {50, 51})
        arms_k[("S2D", a)] = sorted(set(range(28)) | set(range(40, 52)))
        arms_k[("RAND", a)] = sorted(set(range(20)))

    # kill_rand: primary inconclusive (b=6,c=4), D->S (42) <= RAND (45) pt.
    arms_r = {}
    for a in ALPHAS:
        arms_r[("D2S", a)] = sorted(set(range(36)) | set(range(40, 46)))
        arms_r[("S2D", a)] = sorted(set(range(36)) | set(range(52, 56)))
        arms_r[("RAND", a)] = sorted(set(range(45)))

    # pivot_helps: primary inconclusive (b=6,c=4: D->S-only {24..29},
    # S->D-only {50..53}); D->S (44) > RAND (38) pt; D->S beats baseline
    # (20 -> 44, discordant b=26,c=2).
    d2s_p = sorted(set(range(20)) | set(range(24, 48)))
    s2d_p = sorted((set(d2s_p) - {24, 25, 26, 27, 28, 29}) | {50, 51, 52, 53})
    arms_p = {}
    for a in ALPHAS:
        arms_p[("D2S", a)] = d2s_p
        arms_p[("S2D", a)] = s2d_p
        arms_p[("RAND", a)] = sorted(set(range(38)))

    # held: primary inconclusive (b=4,c=2), D->S (34) > RAND (30) pt,
    # no arm beats baseline (baseline 32, arms ~32-34, discordant p>0.05).
    base_h = sorted(set(range(32)))
    d2s_h = sorted((set(base_h) - {0, 1}) | {40, 41, 42, 43})
    s2d_h = sorted((set(base_h) - {2, 3}) | {44, 45})
    arms_h = {}
    for a in ALPHAS:
        arms_h[("D2S", a)] = d2s_h
        arms_h[("S2D", a)] = s2d_h
        arms_h[("RAND", a)] = sorted(set(range(30)))

    # b2_override: primary Supported at alpha=0.10 (D->S 39/60, S->D 30/60,
    # S->D correct subset of D->S -> b=9,c=0, d_hat=0.15) but gains grow
    # monotonically with alpha (0.05, 0.15, 0.25) -> PIVOT (B2).
    gains = {0.07: 0.05, 0.10: 0.15, 0.15: 0.25}
    arms_b2 = {}
    for a, gv in gains.items():
        n_d = 30 + int(round(gv * 60))
        arms_b2[("D2S", a)] = sorted(set(range(n_d)))
        arms_b2[("S2D", a)] = sorted(set(range(30)))
        arms_b2[("RAND", a)] = sorted(set(range(n_d - 4)))

    # b4_tension: primary d_hat<=0 (b=4,c=6, a=24) but Tango U>=0.05
    # (wide CI -> Inconclusive, NOT dead), D->S (28) > RAND (20) pt, no arm
    # beats baseline (D->S identical to baseline; S->D discordance 6v4 ->
    # p~0.38) -> HELD. This documents the B4-vs-F5 reconciliation:
    # literal B4 would KILL; binding F5 holds.
    d2s_t = sorted(set(range(28)))                       # 0..27
    s2d_t = sorted(set(range(24)) | set(range(28, 34)))   # 0..23, 28..33
    arms_t = {}
    for a in ALPHAS:
        arms_t[("D2S", a)] = d2s_t
        arms_t[("S2D", a)] = s2d_t
        arms_t[("RAND", a)] = sorted(set(range(20)))

    return [
        ("stageA_invalid",
         {"pair_shifts": {p: -0.01 for p in GRID},
          "arms_correct": _scenario_arms([], {})},
         ("invalid", "INVALID")),
        ("stageA_noisefloor",
         {"pair_shifts": {p: 0.001 for p in GRID},
          "repeat_shift": 0.002,
          "arms_correct": _scenario_arms([], {})},
         ("invalid", "INVALID")),
        ("stageA_tie",
         {"pair_shifts": {p: (0.05 if p in [(10, 6), (12, 8)] else -0.01)
                          for p in GRID},
          "arms_correct": _scenario_arms([], {})},
         ("raised", "ValueError")),
        ("continue",
         {"pair_shifts": win,
          "arms_correct": _scenario_arms(base30, arms_c)},
         ("verdict", "CONTINUE")),
        ("kill_dead",
         {"pair_shifts": win,
          "arms_correct": _scenario_arms(sorted(set(range(25))), arms_k)},
         ("verdict", "KILL")),
        ("kill_rand",
         {"pair_shifts": win,
          "arms_correct": _scenario_arms(base30, arms_r)},
         ("verdict", "KILL")),
        ("pivot_helps",
         {"pair_shifts": win,
          "arms_correct": _scenario_arms(sorted(set(range(20))), arms_p)},
         ("verdict", "PIVOT")),
        ("held",
         {"pair_shifts": win,
          "arms_correct": _scenario_arms(base_h, arms_h)},
         ("verdict", "HELD")),
        ("b2_override",
         {"pair_shifts": win,
          "arms_correct": _scenario_arms(sorted(set(range(25))), arms_b2)},
         ("verdict", "PIVOT")),
        ("b4_tension",
         {"pair_shifts": win,
          "arms_correct": _scenario_arms(sorted(set(range(28))), arms_t)},
         ("verdict", "HELD")),
        ("tamper",
         {"pair_shifts": win, "tamper": True,
          "arms_correct": _scenario_arms(base30, arms_c)},
         ("raised", "DeltaThetaError")),
    ]


def _wiring_checks(workdir):
    """Call-order-level assertions on a fresh full run."""
    logs = []

    def log(m):
        logs.append(m)

    win = {p: (-0.01 if p != (10, 6) else 0.05) for p in GRID}
    arms_correct = {None: _bits(range(30))}
    for a in ALPHAS:
        arms_correct[("D2S", a)] = _bits(range(48))
        arms_correct[("S2D", a)] = _bits(range(36))
        arms_correct[("RAND", a)] = _bits(range(40))
    budget = RUN.PassBudget()
    backend = MockBackend(budget, {"pair_shifts": win,
                                   "arms_correct": arms_correct})
    RUN.run_full_loop(backend, budget, workdir, log, None, RECORDS_PATH,
                      blocks_override=MOCK_BLOCKS)
    specs = backend.leak_specs_seen
    # Call order: Stage-A specs come first (9 pairs x N_BLOCKS), then Stage B.
    stage_a = specs[:9 * N_BLOCKS]
    stage_b = specs[9 * N_BLOCKS:]
    d2s_b = [s for s in stage_b if s["kind"] == "D2S"]
    s2d = [s for s in stage_b if s["kind"] == "S2D"]
    rnd = [s for s in stage_b if s["kind"] == "RAND"]
    seen = {(s["kind"], s["alpha"]) for s in stage_b}
    want = {(k, a) for k in ("D2S", "S2D", "RAND") for a in ALPHAS}
    # Mock budget arithmetic (N_BLOCKS mock blocks; the real corpus has 25):
    # Stage A: 2 repeats x N_BLOCKS x 1 call + 9 pairs x N_BLOCKS x 2 calls.
    # Stage B: 60 baseline x 1 + 9 arms x 60 x 2.
    expected_calls = (2 * N_BLOCKS + 18 * N_BLOCKS) + (60 + 9 * 120)
    # LOG-320 F2 gate (a): full-scale budget guard. The mock only exercises
    # N_BLOCKS synthetic blocks; the REAL run uses 25 corpus blocks
    # (ceil(50000/2048)). Re-derive the true call total from the protocol's
    # own pass structure and require it to equal AND fit the hard ceiling —
    # this is the check that would have caught the 25-call shortfall.
    real_blocks = (RUN.CORPUS_N_TOKENS + RUN.CORPUS_BLOCK - 1) // RUN.CORPUS_BLOCK
    stage_a_true = 2 * real_blocks * 1 + 9 * real_blocks * 2
    stage_b_true = 60 * 1 + 9 * 60 * 2
    true_total = stage_a_true + stage_b_true
    gate_a = (real_blocks == 25 and stage_a_true == RUN.STAGE_A_CALLS
              and stage_b_true == RUN.STAGE_B_CALLS
              and true_total == RUN.FWD_BUDGET == 1640
              and true_total <= budget.limit)
    gate_a_detail = (f"25 blocks -> true total {true_total} "
                     f"(A={stage_a_true}, B={stage_b_true}) vs constants "
                     f"(A={RUN.STAGE_A_CALLS}, B={RUN.STAGE_B_CALLS}) "
                     f"vs ceiling {budget.limit}")
    # LOG-320 F1 gate (b): per-arm layer-wiring check. Spec dicts alone are
    # correct; this asserts the (capture_src, capture_dst, hook_layer)
    # mapping TorchBackend._leak_layers actually applies — the S2D swap
    # this review caught. (_leak_layers uses no torch state; the mock
    # exercises it directly with a dummy self.)
    s_star, d_star = 10, 6  # mock Stage-A winner: deep s*=10, shallow d*=6
    arm_specs = {"D2S": {"kind": "D2S", "s": s_star, "d": d_star, "alpha": 0.10},
                 "S2D": {"kind": "S2D", "s": d_star, "d": s_star, "alpha": 0.10},
                 "RAND": {"kind": "RAND", "s": None, "d": d_star, "alpha": 0.10}}
    # (capture_src_layer, capture_dst_layer, hook_layer):
    # D2S: capture deep src, hook at shallow dst; S2D: capture shallow src,
    # hook at deep dst; RAND: no src capture, hook at dst.
    want_wiring = {"D2S": (s_star, d_star, d_star),
                   "S2D": (d_star, s_star, s_star),
                   "RAND": (None, d_star, d_star)}
    layer_wiring = []
    for kind, spec in arm_specs.items():
        RUN._check_leak_geometry(spec)
        src, dst = RUN.TorchBackend._leak_layers(None, spec)
        hook = RUN.leak_destination_layer(spec)
        layer_wiring.append((kind, (src, dst, hook) == want_wiring[kind],
                             (src, dst, hook)))
    gate_b = all(ok for _, ok, _ in layer_wiring)
    return [
        ("wiring/rand-drawn-once", backend._rand_draws == 1,
         f"draws={backend._rand_draws}"),
        ("wiring/all-kind-alpha-seen", want <= seen,
         f"missing={sorted(want - seen)}"),
        ("wiring/stageA-9-pairs-x-N_BLOCKS", len(stage_a) == 9 * N_BLOCKS,
         f"got {len(stage_a)}"),
        ("wiring/stageA-alpha-pinned-0.10",
         all(s["alpha"] == 0.10 for s in stage_a),
         f"alphas={sorted({s['alpha'] for s in stage_a})}"),
        ("wiring/stageB-D2S-geometry",
         all(s["s"] == 10 and s["d"] == 6 for s in d2s_b), f"n={len(d2s_b)}"),
        ("wiring/stageB-S2D-swapped",
         all(s["s"] == 6 and s["d"] == 10 for s in s2d),
         f"sample={s2d[0] if s2d else None}"),
        ("wiring/stageB-RAND-destination",
         all(s["d"] == 6 and s["s"] is None for s in rnd),
         f"sample={rnd[0] if rnd else None}"),
        ("wiring/exact-call-accounting", budget.used == expected_calls,
         f"used={budget.used} expected={expected_calls}"),
        ("wiring/budget-limit-pinned-1640", budget.limit == 1640,
         f"limit={budget.limit}"),
        ("wiring/full-scale-budget-guard", gate_a, gate_a_detail),
        ("wiring/leak-layer-mapping-per-arm", gate_b,
         "; ".join(f"{k}={m}" for k, _, m in layer_wiring)),
    ]


def run_all(workdir):
    out = [_run_one(workdir, n, s, e) for n, s, e in _scenarios()]
    out.extend(_wiring_checks(workdir))
    return out


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        res = run_all(td)
    n_ok = sum(1 for _, ok, _ in res if ok)
    for name, ok, detail in res:
        print(("PASS " if ok else "FAIL ") + name + " :: " + detail)
    print(f"{n_ok}/{len(res)} harness checks pass")
    sys.exit(0 if n_ok == len(res) else 1)
