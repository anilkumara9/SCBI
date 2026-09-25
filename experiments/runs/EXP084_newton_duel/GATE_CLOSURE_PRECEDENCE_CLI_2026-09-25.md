# Gate-closure record — EXP084 decision-tree precedence + CLI + GPU-fatal scan (2026-09-25)

GPU-queue readiness lane, 30-day campaign. All inspections executed on the
CPU build machine ($0, no weights touched, stdlib-only). The signed protocol
(`EXP084_R2_NEWTON_DUEL_PREREG_SIGNED.md`, digest
`811a390cf248922837ee6ee36f315ef29ecba40df63f38b60e51b14ebd8ef003`,
recomputed this wave — match) was not modified. Bundle is git-tracked
(the LOG-328 gap is closed for EXP084).

## Gate 1 — signed protocol + bundle test suites: CLOSED

| Suite | Result (re-run this wave) |
|---|---|
| `test_exp084.py` evaluator | **74/74 PASS** (exit 0; run as `python3 test_exp084.py` — the file is a script-style `check()` harness, not a unittest module; `python3 -m unittest` collides with the runner's argparse) |
| `smoke_test.py` startup smoke | **40 SMOKE-OK checks, `SMOKE RESULT: PASS`** |
| `mock_harness.py` end-to-end | **17/17 scenarios PASS** |

## Gate 2 — verdict precedence inspection: CLOSED (conforming)

Inspected `run_exp084.py::adjudicate` against the signed protocol §7
(precedence: INVALID(i)→(iv) → CONTINUE → HELD(win-not-curv) →
HELD(step-noise) → KILL → HELD(straddle); narrow-KILL as secondary,
LOG-266 Fix 2). 10 adversarial probes executed against the real code path:

| Probe | Expected (protocol §7) | Observed |
|---|---|---|
| n_defined=5 + all conjuncts fire | INVALID/UNDEFINED-LANDSCAPE preempts | INVALID/UNDEFINED-LANDSCAPE |
| sens_p=0.5 + all conjuncts fire | INVALID/UNINFORMATIVE-PROXY preempts | INVALID/UNINFORMATIVE-PROXY |
| a∧b∧c∧d∧e | CONTINUE | CONTINUE |
| a∧b∧c∧d ∧ ¬e | HELD(win-not-curvature-explained) | HELD(win-not-curvature-explained) |
| a ∧ ¬b | HELD(step-noise) | HELD(step-noise) |
| a ∧ ¬d | HELD(step-noise) | HELD(step-noise) |
| med≤0, HL-upper<0.01, no conjuncts | KILL(flagship, cost-fair) | KILL(flagship, cost-fair) |
| narrow-KILL criteria met, flagship straddles | HELD(straddle) + narrow secondary | HELD(straddle), secondary=`KILL(directional, narrow)` |
| no rows fire | HELD(straddle) | HELD(straddle) |
| KILL bar boundary: hl_hi=0.01 exactly | HELD(straddle) (strict <) | HELD(straddle) |

`KILL_BAR = 0.01` verified in `exp084_statistics.py` (strict `<`,
protocol-literal). INVALID(i)/(ii) are run-halting exceptions raised
before `adjudicate` — "no verdict," protocol-faithful.

**Observation O1 (not a defect, for the reviewer):** the KILL row does not
re-check conjunct (a); the code is protocol-literal (§7 lists only
"CONTINUE not met and median ≤ 0 and HL-upper < 0.01"). A pathological
corner (Wilcoxon one-sided p≤0.05 with sample-median ≤ 0 and HL-upper <
0.01) could fire KILL while (a) holds — mathematically possible
(e.g. 12 small negatives + 12 large positives). Protocol governs.

## Gate 3 — statistical protocol references: CLOSED

`experiments/protocols/STATISTICAL_PROTOCOL_V02.md` EXISTS (2517 bytes,
2026-09-11; the EXP083 E1 "missing" claim was retracted). EXP084's
statistics are pinned self-contained in the signed protocol §5 (exact
Wilcoxon, Hodges–Lehmann 95% CI, exact Spearman permutation via
precomputed nulls) — no missing statistical doc blocks this bundle.

## Gate 4 — CLI verification: CLOSED

`run_exp084.py` exit codes verified (genuine `$?`, no pipes):

| Invocation | Output | Exit |
|---|---|---|
| `--smoke` | `SMOKE RESULT: PASS` (40 checks) | 0 |
| `--run` (no clearance) | `REFUSED: --run requires --ceo-gpu-clearance ...` | 2 |
| `--run --ceo-gpu-clearance` (no signoff) | `REFUSED: --run requires --stage2-review-signoff ...` | 2 |
| `--run --ceo-gpu-clearance --stage2-review-signoff` (no torch) | `REFUSED: torch is not installed; the model loop needs the GPU node.` | 2 |
| (no args) | `RuntimeError: GPU execution not licensed in this bundle stage. ...` | 1 |
| `--bogus` | argparse error | 2 |

Refusal posture is fail-safe on every path. Note: no-args raises (exit 1)
rather than EXP083's help+exit-2 — cosmetic; nothing executes.

## Gate 5 — GPU-fatal scan: CLOSED

- **torch imports:** all three are function-local (`run_exp084.py:89`
  SHA-hash helper, `:424` TorchBackend constructor, `:815` CLI torch
  probe). No top-level torch import anywhere in the bundle; CPU build
  machine runs stdlib-only per `requirements.txt`.
- **Hardcoded paths:** none (`/home/`, `/Users/`, `/tmp/` — zero hits in
  non-test code).
- **Spearman tables:** n=1..19 present in `exp084_spearman_tables/`
  (19/19). n=20–24 are GPU-node build artifacts
  (`tools/build_spearman_tables_gpu.py`, NTT+Ryser); missing tables →
  `MissingSpearmanTableError` loud halt, no verdict (verified live for
  n=20 this wave; the error message names the builder).
- **Budget enforcement:** 240 fwd + 72 bwd accepted; pass 241 and bwd
  pass 73 both REFUSED (live in the 74/74 suite).
- **Fail-safe defaults:** `RECORDS_REL` resolves to the pinned archive
  (LOG-269 F2 regression test asserts the R5d SHA on the default path).

## Remaining

Gate 6 (independent Law #14 bundle review) — commissioned separately;
its verdict is binding and outside this lane's authority.

*— GPU-queue readiness lane, 30-day campaign, 2026-09-25.*
