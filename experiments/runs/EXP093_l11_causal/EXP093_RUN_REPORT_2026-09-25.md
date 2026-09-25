# EXP093 — Layer-11 Causal Transfer: Execution Report (real run, 2026-09-25)

**Outcome: RUN-INVALID** — guard G5 (injection-site verification) failed on the
real model before any decision-loop forward pass. **No verdict was produced.
No statistics were computed. The hypothesis is untested, not falsified.**

**Mode:** real (`--ceo-clearance`). **Clearance:** CEO CPU execution clearance
issued on the binding LOG-4348 SIGN. **Compute:** CPU only, $0.
**Weights:** read-only throughout; Δθ = 0 asserted pre-run (G1 pre-hash OK);
no mutation path executed (see §4).

---

## 1. Pre-run verification (all green)

| Check | Result |
|---|---|
| Unit suite `test_exp093.py` | **21/21 pass** |
| `smoke_test.py` | **17/17 pass**, torch never imported |
| Signed-protocol digest (blanking rule) | `3e0f269b…` MATCH (LOG-4343) |
| Draft byte-identity | `33434fe3…` MATCH |
| Bundle commit | `fa3fa3e` (LOG-4348 SIGN) on `main` |

## 2. Real-run guard sequence (from `out/exp093_real_stdout.log`)

| Step | Result |
|---|---|
| Launch gates (signed digest + `--ceo-clearance`) | pass |
| G0 bench pin `9be81626…` | pass — 60/60 unique tuples, strata match §2 |
| G1′ inherited (bench-pin byte-identity) | pass |
| G2 direction provenance (real archived `.npz`, read-only) | pass — 60/60 ‖r_i‖ > 1e-9 (min 1.3352), 60/60 v unit-norm, mean_cos_u = −0.0160, prenorm [0.0246, 0.0444] |
| Thread pin | 2, asserted |
| G1′ real-tokenizer cover (offset mapping, never bare-word) | pass — 240/240 in-prompt occurrences single-token |
| Model load (frozen LOG-331 snapshot, CPU, float32) | ok |
| G1 pre-run state-dict hash | **OK** — `ec276abe3902fab0…` == LOG-331 pin |
| G5 criterion (iii) — hook-disabled logits bit-match hook-free reference | **pass** |
| G5 criterion (i) — hooked final-position residual == clean + αv (rel ≤ 1e-6) | **FAIL** — rel_err = **1.000e+00** |

Exact failure line:

```text
RUN-INVALID: G5 FAIL [real probe (gpt_neox.layers[11])]: criterion (i) — hooked final-position residual differs from clean + alpha*v by rel 1.000e+00 > 1e-06 — RUN-INVALID (injection misplaced).
```

Runner exit code 3 (RUN-INVALID). The decision loop (conditions B/P/N) never
started: G4 was never evaluated, no verdict, no `exp093_report.json`.

## 3. Diagnosis: probe defect in `verify_g5_real` (bundle bug, not a measurement)

**Root cause — forward-hook registration order** in `inject.py::verify_g5_real`:

1. The injection hook is attached, then **detached** for the hook-free
   reference run.
2. The capture hook `_capture` is registered on the layer module.
3. The injection hook is **re-attached** — now *after* the capture hook in
   registration order.
4. PyTorch executes forward hooks **in registration order, each receiving the
   previous hook's output**. The capture hook therefore always records the
   **pre-injection** residual, even when the injection hook is enabled.

Consequence: `resid_inj` is byte-identical to `resid_clean`, so criterion (i)
computes ‖−αv‖ / ‖αv‖ = **1.000e+00 exactly** — the observed value is the
algebraic signature of a no-op capture, not of a misplaced injection.

**Confirmation:** a `/tmp` probe on a toy `nn.Linear` (no weights, no model
data involved) verified the ordering semantics: hooks run in registration
order and each sees the previous hook's modified output
(`output[0,0] = 104.0 = 4.0 + 100.0`). The mock-backend G5 passed because the
mock path calls the residual functions directly — the ordering defect exists
only on the real torch path, which no test or smoke check ever executed
before this run.

**Scope of the defect:** the decision-loop injection in `run_exp093.py`
(`run_conditions_real`) is **unaffected** — it attaches a single hook per
item, so the injection genuinely reaches the logits. Only the G5 *probe* is
defective. The scientific hypothesis (layer-11 causal transfer) remains
untested.

## 4. Weight integrity

- `model.eval()` + `requires_grad_(False)` set on all parameters.
- All forward passes under `torch.no_grad()`; no optimizer, no backward, no
  training flag.
- G1 pre-run hash matched the LOG-331 pin; the run aborted at G5 before any
  code path capable of parameter mutation.
- **Δθ = 0 stands.** (G1 post-hash was not reached — the run aborted before
  the decision loop — but no executed statement could modify parameters.)

## 5. Why the execution agent did not fix this

The task license covers execution and reporting, not bundle repair. The G5
failure is a genuine bundle defect of the same class as the F1 defect
(LOG-4345/4346): it requires a repair lane **plus independent re-verification
by execution on the real model** before any re-run — the separation of duties
that caught the v0.1 degeneracy and F1. A silent in-place fix by the executor
would collapse that separation.

**Recommended repair (for the CEO's repair lane):** in `verify_g5_real`,
register the capture hook **after** attaching the injection hook (or capture
the post-injection output by chaining), so `_capture` records the injected
residual. Then re-verify G5 by execution on the real model (criterion (i) rel
≤ 1e-6 must be demonstrated, not asserted), re-run the 21/21 + 17/17 suites,
and re-run the real execution. No protocol change is needed — the registered
G5 criteria are correct; the probe implementation was wrong.

## 6. Artifacts (preserved, Law #8)

- `out/exp093_real_stdout.log` — full real-run stdout (guard sequence,
  G1 pre-hash, G5 failure line).
- No `exp093_report.json` was written (RUN-INVALID exits before scoring).
- This report: `EXP093_RUN_REPORT_2026-09-25.md`.

## 7. Registered implication

**None on the science.** A RUN-INVALID is withheld, never a verdict (§5).
The EXP092 CONTINUE stands; the layer-11 causal question is still open;
KILL remains the registered prior for the re-run. The only licensed claim
from this run: *the EXP093 bundle's real-path G5 probe cannot pass as
written (hook-ordering defect); the real execution is blocked until the probe
is repaired and re-verified.*
