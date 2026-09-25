# Law #14 — Independent re-verification of the EXP093 G5 probe repair

**Verdict: SIGN (binding)** — the repair is verified. The bundle is cleared to seek fresh CEO CPU execution clearance for the real EXP093 re-execution.

- **Target:** commit `b5da3c5` — "EXP093 G5 probe repair (LOG-4350)"
- **Reviewer:** Independent Law #14 reviewer (reports to the founder; binding, non-overridable)
- **Date:** 2026-09-25
- **Context:** LOG-4349 RUN-INVALID — `inject.py::verify_g5_real` registered the capture hook before re-attaching the injection hook, so the probe measured the pre-injection residual (criterion (i) rel_err = 1.0 exactly). The layer-11 causal question was never tested.

This review re-ran everything itself. Nothing below is taken on the repair agent's word.

---

## 1. Diff audit — the fix is minimal and correctly scoped

`git diff b5da3c5^ b5da3c5` touches exactly 7 files:

| File | Change | Assessment |
|---|---|---|
| `experiments/runs/EXP093_l11_causal/inject.py` | +25/−3, confined to `verify_g5_real` | The only production-code change |
| `test_exp093_hook_order.py` | New, 122 lines | 2 torch regression tests |
| `test_exp093.py` | +4 docstring lines only | No behavioral change; torch-free invariant kept |
| `BUILD_NOTES.md` | +46 doc lines | Repair documentation |
| `out/g5_repair_probe_2026-09-25.{py,log}` | New | Repair agent's probe script + log (artifacts) |
| `reports/research_log.md` | +20 lines | LOG-4350 entry |

**Byte-identical (empty diff):** `score_exp093.py`, `run_exp093.py` (decision-loop injection), `direction_builder.py`, and every file under `experiments/protocols/` including all signed protocols.

The fix itself, read line by line:

1. `cap_handle = layer.register_forward_hook(_capture)` moved from *before* `hook.detach()` to *after* `hook.attach(model, v)` — the capture hook now observes the post-injection residual. This is the correct minimal correction for the diagnosed defect (PyTorch executes forward hooks in registration order with chaining).
2. An explicit order assertion was added: the injection handle's id must precede the capture handle's id in the module's ordered `_forward_hooks` registry, else `RunInvalid`. A future reordering silently reintroducing the LOG-4349 defect now fails loudly as RUN-INVALID rather than producing a false measurement.
3. The `finally` block is null-safe (`if cap_handle is not None`), and the hook-free reference run is now genuinely hook-free (previously the capture hook was registered during the "hook-free" reference — harmless there, but sloppy; now clean).

No change to the intervention semantics: `ALPHA = 1.0`, `G5_REL_TOL = 1e-6`, `G5_ABS_TOL = 1e-9`, and the three criteria in `verify_g5` are untouched. The registered G5 acceptance criteria are exactly as signed.

## 2. Independent real-path G5 reproduction — PASS

Independently written probe script (`/tmp/law14_g5_repro.py`, fresh process, nothing reused from the repair agent's script), pinned environment `~/workspace/.venvs/exp093` (torch 2.14.0+cpu, transformers 5.17.0), frozen LOG-331 snapshot, read-only weights, `torch.no_grad`, thread pin 2:

- **G1 pre-hash:** `ec276abe3902fab0…` == `pin.WEIGHTS_PIN` — MATCH (Law #6 / Law #13)
- **G5 gate=PASS** — criterion (i) rel_err = **4.295e-07 ≤ 1e-6** ✓; criterion (ii) max abs change = **0.000e+00** ✓; criterion (iii) bit-match = **True** ✓
- **G1 post-hash == pre-hash** — Δθ=0 confirmed ✓

The rel_err value (4.295e-07) reproduces the repair agent's claimed value exactly — expected under deterministic pinned execution, and it corroborates rather than duplicates their run since the script, process, and hash assertions are mine.

Environment pin honored: transformers 5.17.0 used as required. The G1 pin reproduced on first attempt; no library substitution was needed or performed.

## 3. Suites — all green, regression test proven genuine

Re-ran in the pinned venv:

- **Unit:** 21/21 OK (`test_exp093.py`, torch-free)
- **Hook-order regression:** 2/2 OK (`test_exp093_hook_order.py`)
- **Smoke:** 17/17 checks passed (`smoke_test.py`)

**The regression test genuinely guards the defect:** I checked the pre-fix `inject.py` (from `b5da3c5^`) into a scratch dir and ran `test_verify_g5_real_observes_post_injection_residual` against it — it FAILS with `RunInvalid: criterion (i) … rel 1.000e+00 > 1e-06`, the exact algebraic signature recorded at LOG-4349. On the fixed code it passes. The second test pins the mechanism directly (old registration order provably yields rel == 1.0 on a toy layer). This is a real regression test, not a tautology.

## 4. Signed protocol digest — intact

Recomputed SHA-256 over `experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md` with the 64-char self-digest value blanked (the header's signature-block rule, same rule the runner enforces): `3e0f269b9f2c5170d2b6ed37b2bd03f39f8eeb344914e8bb1f904709ad13db93` — **exact match**. No signed file was touched by the repair. The signed protocol, its decision tree, and its registered bars stand unchanged.

---

## Verdict rationale

The repair does exactly what the authorized repair lane permitted and nothing more: a minimal, correctly reasoned correction to the G5 verification probe's hook ordering, guarded against recurrence by an explicit order assertion. The decision-loop injection, scoring, and all signed artifacts are byte-identical. The real-path proof (criterion (i) ≤ 1e-6 on the frozen snapshot with Δθ=0) was reproduced independently. The regression tests fail on the defect and pass on the fix.

**Binding verdict: SIGN.** The EXP093 bundle's G5 probe is repaired and verified. Re-execution still requires fresh CEO CPU execution clearance per the launch chain — this SIGN covers the repair only, not the experiment's eventual verdict. KILL remains the registered prior for the re-run.

## Adversarial notes (for the record)

- The order assertion reads `layer._forward_hooks`, a private PyTorch API. It is used read-only (key order inspection), which is stable across the pinned torch 2.14.0 and the mechanism it guards is version-independent (registration-order chaining). Acceptable; not a defect.
- The repair agent's probe log and my independent reproduction agree to the digit (4.295e-07). Deterministic, pinned, expected — noted, not suspicious.
- Nothing in this review licenses any change to the signed protocol. Any future design change remains a new experiment number.
