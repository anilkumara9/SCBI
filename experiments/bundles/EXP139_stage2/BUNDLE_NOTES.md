# EXP139 Stage-2 Bundle — Apparatus Audit Notes

**Lane:** apparatus audit + bundle build, 2026-10-03 (founder order: close the EXP139
Stage-2 Kaggle bundle gap).
**Protocol:** `research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4885).
**Stage-1 precedent:** `experiments/runs/EXP139_stage1/` (LOG-4885→4886; κ̂=0.955971<1).

## (a) What existed before this lane

**Nothing.** Workspace-wide search found no Stage-2 bundle, Kaggle notebook, or GPU
execution package for EXP139:
- `experiments/bundles/` contained only `exp131_v1inj/` (a different experiment).
- No file matching `*stage2*`/`*stage_2*` exists anywhere under `~/workspace/SCBI`.
- EXP139 mentions in `goals/scbi-research-program/hidden_files/` are watermarks,
  the push-readiness report, and `active_lanes.txt` — no bundle.
- The 2026-10-03 checkpoint's required "built and independently reviewed Stage-2
  execution bundle" was never produced. **Gap confirmed.**

## (b) What was built

`experiments/bundles/EXP139_stage2/`:
- `exp139_stage2_lib.py` — pure-Python (stdlib only, no torch): all §2 pins,
  verbatim bench reconstruction (ported from `run_stage1.py`), §7 Newcombe/Wilson
  implementation, McNemar-exact secondary, trajectory diagnostic, §6 branch reporter.
- `run_stage2.py` — GPU executor (imports the lib; torch required). Implements §5
  exactly: 60 baselines + 480 R-evaluations (T=8), decode at t=8, paired table vs
  committed baseline, Newcombe interval, trajectory backstop, validity gates
  (a)/(b)/(c), forward-budget assert, Δθ=0 post-hash, RUN-INVALID (exit 44) on any
  gate trip. Single source of truth for T/N/budget via the lib.
- `data/committed_baseline_view0.json` — 60 committed view-0 yhat values copied
  from `experiments/runs/EXP135_eval/out/exp135_records.json` (integrity-tested).
- `tests/test_bundle_cpu.py` — 67 structural tests, CPU-only, no GPU, no downloads
  (60 original + 7 repair-lane regression/static tests: F1×4, F2×2, F4+1; the two
  `~/workspace/...` provenance checks SKIP gracefully when the workspace tree is
  absent, e.g. on Kaggle).
- `requirements.txt` — torch 2.10.0+cu128 / transformers 5.17.0 / numpy (pin basis:
  EXP131's GPU execution record on Tesla T4 with this backbone pin).
- `README.md` — exact founder Kaggle steps.

Nothing signed was modified: the pre-registration and Stage-1 records are untouched.

## (c) Test results (after LOG-4896 repair lane)

`python tests/test_bundle_cpu.py` — **67/67 PASS** (run 2026-10-03, stdlib only):
- bench reconstruction → BENCH_PIN `eb304fa6…` match;
- all three pins found verbatim in the signed pre-registration text;
- Newcombe vs hand-computed reference (n=60,b=10,c=2): L=0.024446, U=0.249518 ✓;
- Wilson symmetry/clipping; McNemar-exact doubling value ✓; trajectory strictness
  (incl. tie rejection) ✓;
- verdict-tree branches CONTINUE/PIVOT/HELD(c)/HELD(d) trip correctly; the
  ΔM≤0 path emits HELD(f) unambiguously per the binding adjudication (LOG-4896),
  with no conflict and no KILL reading ✓;
- committed data file: 60 items, ids match bench, values match EXP135 source ✓;
- executor static scan: no training calls (`.backward`/optim/`.train()`/
  `requires_grad_(True)`/`zero_grad` absent), `torch.no_grad()`/`model.eval()`/
  `local_files_only=True`/pins/artifacts present, T from lib (no hardcoded 8) ✓;
- requirements parse; lib has no torch/network imports ✓;
- F1 regression: the executor's exact `yhat_of` call path operates on a
  stubbed 50304-vector (target and foil branches), the two decode call sites
  carry no `[0]` reduction, and the old scalar-reduction defect is shown to
  crash — the defect class is covered ✓;
- F2: post-hash mismatch segment trips `run_invalid`; `backbone_post` is
  written to both `stage2_records.json` and `stage2_verdict.json` ✓.

Kaggle simulation (workspace tree absent): **61/67 passed, 6 skipped, 0 FAIL** —
the 5 pre-reg provenance checks and the EXP135-source check SKIP gracefully.

## (d) Open ambiguities (REPORTED, not resolved — for the Law #14 reviewer)

- **AMBIGUITY-1 (pass accounting):** pre-reg §5 says "480 R-evaluations + 40
  additional baseline passes = 520 passes". Stage-1 archived only h_i *norms*,
  not the 20 h_i vectors, so items 0–19 cannot be reused on the founder's machine.
  The bundle recomputes all 60 baselines → **540 passes**, asserted in-script and
  documented. The science is identical (deterministic recomputation per machine;
  cross-machine equivalence is anchored by validity gates (a)–(c), not by a
  bitwise claim); only the cost line differs.
- **AMBIGUITY-2 (readout convention):** pre-reg §2 text says "argmax over the full
  vocab"; the signed Stage-1 implementation and the committed EXP135 records use
  the two-way candidate comparison (`tA` wins iff `lv[tA] >= lv[tC]`). The bundle
  follows the Stage-1/committed convention — the paired table is only well-defined
  that way (baseline correctness derives from committed yhat). Diverges from the
  §2 text only when a third token would be the full-vocab argmax.
- **AMBIGUITY-3 (McNemar convention, secondary only):** pre-reg §7 names
  "McNemar-exact two-sided p" without a two-sided convention; the bundle uses the
  doubling method. Reported, not binding.
- **AMBIGUITY-4 (verdict conflict, ADJUDICATED — binding, Law #14 apparatus review
  LOG-4896):** pre-reg §0 breaking points and §5 bars assign Stage-2
  ΔM_attractor ≤ 0 → **KILL**; the §6 falsification table assigns κ̂<1 with
  ΔM_attractor ≤ 0 → **HELD(f)** ("converges to nothing useful"). **Ruling: the
  §6 table governs; the §0/§5 KILL lines are superseded as drafting defects.**
  For κ̂<1 and ΔM_attractor ≤ 0 the executor emits HELD(f) unambiguously (no
  conflict, no KILL reading). This is a pre-execution disambiguation of a
  drafting defect, not a post-hoc bar shift (Law #4): HELD(f) licenses nothing
  and kills nothing. Implemented in `stage2_branch_report`, the executor
  docstring/report template, README, and tests.

## (e) Trajectory aggregation (m3, conservative reading)

The pre-reg's trajectory backstop is unaggregated ("must be strictly
decreasing"). The bundle implements the conservative aggregation: the 8
diff-norms ‖h^(t+1)−h^(t)‖₂ (t=0..7) must be strictly decreasing **on all 60
items** (a single non-decreasing item or a tie fails the backstop). This is the
strictest reading consistent with the text; the per-item vectors are persisted
in `stage2_records.json` so any weaker aggregation can be recomputed
post-hoc without re-running.

## (f) Repair lane (LOG-4896 required fixes, applied 2026-10-03)

Mechanical repair only — no protocol changes, no new science. Nothing signed
was modified (pre-registration and `APPARATUS_REVIEW_2026-10-03.md` untouched).

- **F1 (critical):** dropped the erroneous `[0]` at both attractor-decode call
  sites in `run_stage2.py` (`readout_yhat` already returns the full (50304,)
  vector); added 4 CPU regression tests (exact `yhat_of` call path on a stubbed
  50304-vector, call-site static guard, old-bug crash proof).
- **F2:** backbone post-hash mismatch now trips RUN-INVALID (exit 44) per Law #6
  (post-hash moved before the artifact writes); `backbone_post` persisted in
  `stage2_records.json` and `stage2_verdict.json`; 2 static tests.
- **F3:** the two `~/workspace/...` provenance checks SKIP gracefully when the
  files are absent (verified in a Kaggle simulation: 61/67 passed, 6 skipped,
  0 FAIL); README step 5 reworded ("zero FAILs; SKIPs expected on Kaggle").
- **F4:** AMBIGUITY-4 adjudication implemented in code, docs, and tests
  (HELD(f) governs; §0/§5 KILL lines superseded); +1 test (traj-fail case).
- **m1:** this document's stale "40 tests" count → 67.
- **m2:** "bitwise-deterministic" softened to per-machine determinism with
  cross-machine equivalence anchored by gates (a)–(c) (executor docstring,
  README, and §(d) above).
- **m3:** trajectory aggregation documented in §(e) above and README.

Pending: follow-up Law #14 verification review of the repaired bundle
(no LOG entry written by this lane — the verification review logs).

## Review pointers

1. Verify the bench port is byte-faithful to `run_stage1.py` (the test only checks
   the hash, which transitively verifies it).
2. Rule on AMBIGUITY-1 (accept 540), AMBIGUITY-2 (two-way readout), AMBIGUITY-4
   (KILL vs HELD(f) for ΔM≤0).
3. Confirm the gate-(c)-to-60/60 extension is an acceptable analog of §3(c).
4. Confirm no GPU was touched in bundle construction (true: torch is not even
   installed in the build environment; tests are stdlib-only).
