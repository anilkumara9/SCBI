# Law #14 Follow-up Verification Review — EXP139 Stage-2 Bundle Repair

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (binding verdict; the CEO cannot override).
**Date:** 2026-10-03.
**Scope:** verification that the repair lane applied the LOG-4896 required fixes (F1–F4 + m1–m3) — NOT a re-review of apparatus substance. The signed pre-registration (`research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md`) and the LOG-4896 review were not modified by this lane.
**Compute:** $0; zero GPU contact; no weight downloads; no git branch/checkout/push. Bundle and pre-registration not modified — this addendum and the LOG-4897 entry are the only writes.

## 1. F1 (critical: `[0]` scalar-reduction at both decode call sites) — VERIFIED

- `run_stage2.py` now reads `lv_attr = readout_yhat(traj[L.T_STEPS])` and `lv_t = readout_yhat(traj[t])` — both `[0]` reductions are gone; `yhat_of` receives the full `(50304,)` vector, matching the pre-fix contract the review described.
- Four regression tests added, all passing on this reviewer's independent re-run:
  - `f1_decode_operates_on_vector` / `f1_decode_foil_path`: extract the executor's **actual** `yhat_of` via AST and drive it with a stubbed 50304-length vector through both the target and foil branches — the exact call path, no torch needed. Genuine (fails if the indexing contract is ever re-broken).
  - `f1_no_scalar_reduction_at_callsites`: asserts the exact pre-fix strings `readout_yhat(traj[L.T_STEPS])[0]` and `readout_yhat(traj[t])[0]` are absent — **fails against the old code** (both strings were present there). This is the true defect-class guard.
  - `f1_old_bug_would_have_crashed`: proves the harness detects the crash mode (scalar fed to `yhat_of` raises), i.e. the regression tests are not vacuous.
- No test in the suite is vacuous: every new check was traced to a condition that fails on the pre-repair code or on a plausible re-introduction of the defect.

## 2. F2 (backbone post-hash must trip RUN-INVALID; persist `backbone_post`) — VERIFIED

- `run_stage2.py`: `if post_hash != L.BACKBONE_PIN: run_invalid("(post) backbone post-hash mismatch: got %s" % post_hash)` — mismatch now exits 44, never 0. The check sits before the artifact writes, so no hypothesis verdict can be emitted from a mutated-weights run (Law #6).
- `backbone_post` is persisted in **both** `stage2_records.json` and `stage2_verdict.json` (2 occurrences confirmed).
- Static tests `f2_posthash_mismatch_trips_runinvalid` and `f2_backbone_post_persisted` pass; both fail against the pre-repair code (which logged "MISMATCH" and exited 0 with no `backbone_post` recorded).

## 3. F3 (Kaggle-SKIP grace; README step 5) — VERIFIED

- The six `~/workspace/...`-dependent checks (5 pre-reg provenance + 1 EXP135 source) now SKIP gracefully when the files are absent.
- This reviewer ran a Kaggle simulation (provenance paths redirected to `/nonexistent` in a `/tmp` copy — the bundle itself untouched): **61/67 passed, 6 skipped, 0 FAIL** — exactly matching the repair lane's reported figure.
- README step 5 now reads "zero FAILs required (SKIP lines are expected on Kaggle — provenance checks verify build-machine files)". Exact and achievable.

## 4. F4 (AMBIGUITY-4 adjudication: κ̂<1 & ΔM≤0 → HELD(f)) — VERIFIED

Matches the binding LOG-4896 ruling exactly, in all four places:
- `exp139_stage2_lib.py::stage2_branch_report`: `dhat <= 0` emits `("HELD(f)", ...)` — **no conflict reported, no KILL reading emitted**; the superseded §0/§5 KILL lines are cited as drafting defects with the LOG-4896 reference.
- `run_stage2.py`: module docstring carries the adjudication; the RUN_REPORT.md template documents it; the conflicts loop is retained as a defensive tripwire that now expects the list to be empty.
- `README.md`: "If Δ̂ ≤ 0 the report emits **HELD(f)** ... per the binding Law #14 apparatus-review adjudication (LOG-4896)". The old "both readings" paragraph is gone.
- `BUNDLE_NOTES.md` §(d): adjudication recorded with the same wording.
- Tests: `verdict_held_f_adjudicated` and `verdict_held_f_adjudicated_traj_fail` assert empty conflicts + HELD(f) present + no "KILL" in any branch name (including the trajectory-fail case, per the ruling's unqualified scope). Both pass.

## 5. Minors m1–m3 — VERIFIED

- m1: the stale "40 tests" count now reads 67 (BUNDLE_NOTES §(b)/(c)).
- m2: no "bitwise-deterministic" claim remains; executor docstring, README, and BUNDLE_NOTES state per-machine determinism with cross-machine equivalence anchored by gates (a)–(c).
- m3: the all-60-items-strict trajectory aggregation is documented in BUNDLE_NOTES §(e) and README.

## 6. CPU test suite — re-run by this reviewer: 67/67 PASS, 0 skipped

Count reconciles: 60 (LOG-4896) − 1 (removed dual-report conflict test) + 8 (F1×4, F2×2, F4 net +1) = 67. Vacuity spot-check: the negative-pattern scans, pin-vs-prereg checks, hash checks, and the new F1/F2/F4 tests each fail against the pre-repair code or a plausible regression — none is a tautology.

## 7. No protocol drift; nothing else changed

- Pins, bars (`BAR_DELTA_PP=0.08`, `BAR_LCI=0.05`), bench reconstruction, Newcombe/Wilson/McNemar implementations, trajectory diagnostic, requirements pins: all byte-identical in behavior to the LOG-4896-reviewed state.
- Signed pre-registration untouched (tracked file clean in working tree; this lane wrote nothing to it).
- `data/committed_baseline_view0.json` and `requirements.txt` unchanged (integrity and pin tests still pass).
- Changes are confined to F1–F4, m1–m3, and their documentation/tests.

## 8. Founder README — exact, complete, safe, with ONE residual (R1)

Steps 1–7 remain exact and safe: Kaggle T4 + Internet ON, bundle upload, public pinned model download (no login), pinned requirements, CPU tests with the corrected step-5 wording, `run_stage2.py`, the four `out/` files back. No credentials, no weight exfiltration, correct model pin, exit-44 semantics accurate.

**R1 (residual, mechanical):** the README status line still reads "independent Law #14 apparatus review PENDING — do not run until the review signs." The apparatus review is complete (LOG-4896, SIGN-WITH-FIXES); post-verification this line wrongly instructs the founder not to run, contradicting the licensed state. Required replacement (verbatim):

`**Status:** bundle built and CPU-tested 2026-10-03; Law #14 apparatus review (LOG-4896) and follow-up repair verification (LOG-4897) complete — founder GPU execution licensed.`

## 9. Hygiene observation (non-blocking)

`__pycache__/` dirs ship inside the bundle. Harmless: `exp139_stage2_lib`'s `.pyc` is newer than its source (consistent), and CPython never consults a cached `.pyc` for the `__main__` script (`run_stage2.py`). Optional: exclude `__pycache__` from the founder upload.

## Binding verdict: SIGN-WITH-FIXES

The LOG-4896 repairs are verified as implemented — F1–F4 and m1–m3 all check out, the suite is 67/67 on independent re-run, no test is vacuous, no protocol drift, pre-registration untouched. One mechanical residual remains: **R1**, the stale README status line (§8 above).

**Founder contact is not licensed until R1 is applied.** Per the LOG-4895 precedent for mechanical residuals: once R1 is applied verbatim and a diff confirms only that line changed, the bundle may be treated as signed and founder GPU execution licensed — no further re-review required.
