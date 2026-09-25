# EXP093 — Layer-11 Causal Transfer: Bundle Build Notes

**Status: bundle built against the SIGNED protocol (LOG-4343). No real
execution has occurred.**

## Protocol state (as of 2026-09-25)

- Design: `experiments/protocols/EXP093_L11_CAUSAL_PREREG_DRAFT.md` v0.2 —
  UNSIGNED draft (kept as the pre-signature record). The v0.1 construction was
  killed by Law #14 at LOG-4340 for algebraic degeneracy; v0.2 (LOO
  maximum-average-cosine shared correction) received the binding SIGN at
  LOG-4342.
- Signing ceremony completed at **LOG-4343** (concurrent lane, CEO office):
  `experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`, body
  byte-identical to the reviewed draft. Signed digest
  `3e0f269b9f2c5170d2b6ed37b2bd03f39f8eeb344914e8bb1f904709ad13db93`
  (SHA-256 over the signed file with the 64-char digest value blanked —
  self-referential digest convention, signature-block rule).
- The bundle build **independently re-verified both digests before stamping**:
  signed-digest MATCH (blanking rule), and SHA-256(reviewed draft content) ==
  `33434fe34e8f56512dbbf5b9339509736e60462a94a1a96a10f0b90b5fae7378`
  (cross-check against the draft, untouched since `ca88c95`).
- `protocol_pin.py` stamps the signed digest; the runner verifies it with the
  blanking rule (a literal hash of the raw file cannot reproduce a
  self-referential digest). A one-byte tamper test is in the unit suite.
- The LOG-4343 SIGN **does not clear execution**. Remaining chain:
  independent bundle review (Law #14) → CEO CPU clearance → execution.

## What was built

`experiments/runs/EXP093_l11_causal/`:

| File | Purpose |
|---|---|
| `requirements.txt` | numpy (+ torch/transformers listed for the real path) |
| `protocol_pin.py` | bench pin `9be81626…`, weights pin, PENDING-SIGNATURE digest, `THREAD_PIN = 2` |
| `direction_builder.py` | G2: registered LOO construction from the archived `.npz` (numpy-only, read-only); CLI writes `direction_verification.json` |
| `inject.py` | backend-agnostic G5 verifier, numpy `MockCausalModel`, real torch `TorchInjectionHook` (lazy imports) |
| `run_exp093.py` | entry point; `--mock` (synthetic) vs `--ceo-clearance` (real); launch-chain gates fire before any guard/weight access |
| `score_exp093.py` | McNemar exact test + the §5 TOTAL decision tree (CONTINUE→PIVOT(c)→PIVOT(a)→PIVOT(b)→KILL) |
| `test_exp093.py` | 19 unit tests, numpy-only |
| `smoke_test.py` | zero-model-pass pipeline check |
| `build_artifacts/direction_verification.json` | G2 build artifact on the real archived `.npz` |

## What was executed (build-time only, 2026-09-25)

- `direction_builder.py --out-dir build_artifacts`: gate PASS — reproduced all
  registered measurements (min ‖r‖=1.3352, mean cos u=−0.0160, prenorm
  [0.0246, 0.0444], max cos v=0.9554), 60/60 ‖r_i‖>1e-9, 60/60 unit-norm,
  R4 not-bit-identical.
- `python3 -m unittest test_exp093`: **19/19 pass** (McNemar hand values,
  decision-tree scenarios for all six routes, tie rule, tie-rate RUN-INVALID,
  G5 mock pass + misplaced-injection RUN-INVALID, v0.1 degeneracy regression,
  PENDING-SIGNATURE refusal, forbidden flags, mock end-to-end with zero torch
  imports).
- `smoke_test.py`: all checks pass (bundle files, bench pin, G2 artifact,
  unsigned refusal, mock pipeline, torch never imported).
- **No real execution occurred**: no weight access, no forward passes on the
  frozen model. The only real-data contact was the read-only `.npz` read in
  the direction builder (no torch, no weights touched).

## Launch chain for the real run

1. CEO signing ceremony: sign protocol, stamp `SIGNED_PROTOCOL_DIGEST`.
2. Independent bundle review (Law #14): this bundle + build artifacts.
3. CEO CPU clearance for the 180 forward passes.
4. Real execution: `python3 run_exp093.py --out-dir <dir> --ceo-clearance`.

## Reviewer notes (flagged for the independent review)

- **THREAD_PIN = 2** is an assumption, not a measurement: EXP092 extraction had
  no explicit thread metadata; 2 was chosen because the build host reports
  `nproc=2`. The runner pins and asserts `torch.get_num_threads() == 2`
  before condition B (draft F8); on a different host this is RUN-INVALID until
  re-pinned to the documented extraction value.
- G4 is evaluated after the 60 condition-B passes and **before** P/N — an
  implementation choice to fail fast on pipeline drift (draft §6 does not
  order B vs P/N within item).
- The G5 probe runs once, on item 0, before the 180-pass loop (draft F6):
  post-loop probe omitted to avoid 181st-pass contamination questions.
- The scoring tie rule uses strict inequality (margin > 0); tie rate > 5% of
  the 180 item-conditions → RUN-INVALID.
- Decision-tree evaluation order follows the draft: CONTINUE → PIVOT(c) →
  PIVOT(a) → PIVOT(b) → KILL (F3/F4).
- Mock-mode margins are arbitrary synthetic values; the mock verdict
  (KILL on the seeded synthetic data) is a pipeline artifact, not a result.

---

## Repair note — G5 probe hook-ordering defect (LOG-4349 → repair lane, 2026-09-25)

**Defect:** `inject.py::verify_g5_real` registered the capture hook *before*
re-attaching the injection hook. PyTorch runs forward hooks in registration
order with chaining, so the capture recorded the pre-injection residual and
criterion (i) measured rel_err = 1.000e+00 exactly — the algebraic signature
of a no-op capture. The real execution aborted RUN-INVALID at G5 (LOG-4349);
the decision-loop injection (single hook per item in `run_exp093.py`) was
never defective.

**Fix (minimal, `inject.py` only):** the capture hook is now registered
*after* the injection hook's re-attach, and the probe asserts the order
explicitly via the module's ordered hook registry
(`_forward_hooks`: injection handle id must precede capture handle id; a
violated order raises RunInvalid). The `finally` block is null-safe for the
capture handle. No change to the decision-loop injection, scoring, or any
signed file.

**Regression tests** (`test_exp093_hook_order.py`, torch-only, kept out of
`test_exp093.py` so that module's torch-free invariant stands):
- `test_verify_g5_real_observes_post_injection_residual` — runs the real
  `verify_g5_real` against a toy torch model; FAILS on the pre-fix code
  (RunInvalid, rel 1.0), PASSES on the fixed code.
- `test_capture_first_ordering_is_provably_blind` — replicates the old
  registration order on a toy layer; proves the mechanism (rel == 1.0).

**Re-verification required before any re-run:** the fixed probe must
demonstrate criterion (i) rel_err ≤ 1e-6 on the real model path (read-only
weights, Δθ=0), plus green suites (21/21 unit, 2/2 hook-order, 17/17 smoke),
plus independent Law #14 re-verification of the repair. Re-execution needs
fresh CEO clearance — this repair lane does not re-run the experiment.

**Re-verification result (repair lane, same day):** the fixed probe was
executed against the frozen LOG-331 snapshot (venv torch 2.14.0+cpu,
transformers 5.17.0 — the LOG-8436 pin; transformers 4.x loads hash to a
different value, 2ca7f6bf…, due to a state-dict conversion change, so 5.17.0
is required for the G1 guard): G1 pre-hash `ec276abe…` MATCH,
criterion (i) rel_err = **4.295e-07 ≤ 1e-6** PASS,
criterion (ii) 0.0 PASS, criterion (iii) bit-match PASS,
G1 post-hash unchanged (Δθ=0). Suites: 21/21 unit (torch-free),
2/2 hook-order regression, 17/17 smoke. Probe script + log preserved in
`out/g5_repair_probe_2026-09-25.{py,log}`. Awaiting independent Law #14
re-verification of the repair + fresh CEO clearance before any re-run.
