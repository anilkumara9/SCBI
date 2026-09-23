# Adversarial Review — EXP067 Execution Bundle (Spec-Faithfulness Audit)

**Date:** 2026-09-23
**Reviewer role:** Adversarial Reviewer (`.agents/agents/adversarial-reviewer.md`)
**Gate:** Law #14 — bundle must be reviewed for spec-faithfulness BEFORE GPU hours are spent
**Scope document (signed):** `experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md`
**Bundle under review:** `experiments/runs/exp067/` — `run_exp067.py`, `evaluate_exp067.py`,
`RUNBOOK.md`, `UNTESTED_ASSUMPTIONS.md`, `requirements.txt`
**Method:** line-by-line code audit against the signed protocol; independent re-derivation of
the decision tree on 10 synthetic cases + both historical artifacts; crash-testing the
evaluator on halt payloads; cross-checking EXP066 conventions in
`experiments/scripts/run_exp066_pythia410m_replication.py`.

---

## VERDICT: **DO-NOT-EXECUTE**

One FATAL spec-faithfulness bug (silent zero-vector C2 control) plus one MAJOR evaluator
crash on halt payloads. Executing the bundle as-is would waste GPU hours and — worse —
produce a corrupted C2 column that looks like a clean null. All fixes are small and
paper-/code-local; re-review of the diff is required before execution (no full re-audit).

---

## FATAL (must fix before any execution)

### F1 — C2 "static basis" control is a ZERO vector (silent no-op)

**Location:** `run_exp067.py`, `head_projected_sum()` + `C2_vec = head_projected_sum(B_agg)`.

**Protocol §3.4 requires:** C2: `h ← h + α Σ_{h∈H*} Q_h Q_h^T B_agg` (head-projected, no rotation).

**Code does:**
```python
def head_projected_sum(basis_vec, R_by_head=None):
    ...
    Rh = R_by_head[h] if R_by_head is not None else I64
    total += Q_heads[h] @ ((Rh - I64) @ qb[h])   # Rh=I64 → (I64−I64) = 0
    return ALPHA * total
C2_vec = head_projected_sum(B_agg)   # = 0 vector
```
With `R_by_head=None`, `Rh − I64 = 0`, so **C2_vec ≡ 0**. The "static basis" condition
would add nothing to the residual stream — it is C1 wearing a C2 label. The ledger would
show a pristine null row (ΔM=0, KL≈0.0000, ‖ΔH‖≈0) that a reader interprets as "the static
basis was tested and did nothing," when in fact no static basis was ever injected.

**Why this is fatal, not cosmetic:** protocol E-5 defines the entire purpose of C2 as
"the C2-vs-C3 contrast cleanly isolates the rotation effect *within head subspaces*."
With C2=0 that contrast is C3-vs-nothing. If C3 later shows ΔM>0, the program could claim
"rotation enables transfer where the static basis fails" — a corrupted conclusion built on
an untested control. The bug is silent: no crash, no warning, clean-looking numbers.

**Fix (one line):** `C2_vec = ALPHA * Σ_{h∈H*} Q_heads[h] @ (Q_heads[h].T @ B_agg)`
(the head-projected basis, no `(R−I)` delta form — that form is correct only for C3/C5/C6/C7).

---

## MAJOR (fix before execution)

### M1 — `evaluate_exp067.py` CRASHES on halt payloads (KeyError)

**Reproduced:** built a minimal `HALT_STAGE_A` payload exactly as `save_halt()` writes it;
the evaluator died with `KeyError: 'stage_B_conditions'`.

**Root cause:** `normalize_exp067()` reads `payload["stage_B_conditions"]` *before*
checking `payload["outcome"]`. Halt payloads (Stage A and headroom) contain no
`stage_B_conditions` key — and Stage A halts additionally lack `baseline_accuracy`.

**Why this matters:** the RUNBOOK explicitly instructs halted users to run the evaluator
for the pre-registered branch-(a)/(headroom) ruling ("it will print the branch-(a) ruling
verbatim"). Instead they get a Python traceback at the exact moment the protocol demands
a clean, reportable outcome. A halt is a first-class scientific result under §7.2; the
tooling must not break on precisely the outcomes the pre-registration was designed to produce.

**Fix:** check `outcome` first in `normalize_exp067()`; tolerate missing
`stage_B_conditions`/`baseline_accuracy`; make `report()` handle a `None` baseline.
Re-test with synthetic halt payloads for both halt types before sign-off.

### M2 — Default model is the OUT-OF-SCOPE pythia-160m; evaluator prints unqualified protocol rulings for out-of-scope runs

**Facts:** the signed protocol pre-registers **only** `pythia-410m`. The bundle defaults to
`--model pythia-160m`, and the RUNBOOK's primary command is the 160m run. The out-of-scope
labeling is honest and pervasive (docstring, config table, `results.json`
`protocol_scope`, evaluator scope line, runbook, `UNTESTED_ASSUMPTIONS.md` A1).

**The hazard:** the evaluator's ruling text carries no scope qualifier. For an out-of-scope
run it prints `Scope: OUT-OF-PROTOCOL-SCOPE ...` and then, verbatim,
`BRANCH: H1_FALSIFIED — ... RULING: H1 is FALSIFIED.` The branch text is quotable without
its scope line (exactly as happened in the `--historical` dry-runs, where "illustrative
only" sits above a full falsification ruling). A non-expert user following the RUNBOOK's
first command can produce, screenshot, and report "EXP067 falsified H1" from a run the
pre-registration does not cover — a protocol violation by accident, which is precisely what
Law #14 review exists to prevent. 410m is also free-tier feasible (≈1.7 GB fp32 on a
16 GB T4; tens of minutes ×2–4), so cost does not justify the out-of-scope default.

**Fix (either):**
- (a, preferred) Default to `--model pythia-410m` (the pre-registered configuration);
  keep 160m as an explicit `--pilot` smoke-test flag. The default should be the
  configuration whose results are scientifically reportable.
- (b) Keep the 160m default but scope-gate the evaluator: for out-of-scope runs, print
  raw statistics plus a banner `NO PROTOCOL RULING — OUT-OF-SCOPE PILOT` *instead of*
  the branch text, so no ruling can be quoted without its qualifier.

### M3 — RUNBOOK gaps that will fail a non-expert user

1. **Kaggle phone verification (most likely first-run failure):** new Kaggle accounts
   require phone-number verification to unlock GPU quota. The RUNBOOK's step 1
   ("sign in → Create → New Notebook → Accelerator: GPU T4 x2") will silently offer no
   GPU to an unverified account. Add an explicit step 0.
2. **No pre-flight GPU check + silent CPU fallback:** the script does
   `torch.device("cuda" if torch.cuda.is_available() else "cpu")` and would run the full
   ~2,100 forward passes on CPU for many hours (likely hitting session limits) without
   ever erroring. Add a pre-flight cell: `!nvidia-smi` and
   `python -c "import torch; assert torch.cuda.is_available()"`, with the instruction
   **stop if CPU** — do not run.
3. **Bundle-upload step lacks copy-paste commands:** the GitHub clone does not contain
   this local-only bundle; step 5's "upload via Add data → Upload or zip it and `!unzip`,
   then copy it over the cloned tree" is the most failure-prone step and needs exact
   commands (upload path `/kaggle/input/...`, `!cp -r` target). A non-expert will stall here.

---

## MINOR (fix opportunistically; not execution-blocking)

### m1 — Stage A `g_h` uses raw dot products, not true cosines (protocol §3.5 specifies cos)

`cos_al = dot(R_t @ v1, vkh)` where `ṽ = Q_h^T v̂` has norm `‖P_{S_h} v̂‖ ≤ 1` — these are
not unit vectors. **Impact analysis:** since `‖R_t v1‖ = ‖v1‖`, the sign of
`(dot_al − dot_raw)` equals the sign of `(cos_al − cos_raw)`, so the **halt/no-halt
decision is identical** under either definition. Only the top-K *ranking* among passing
heads can differ, and the diagnostics table mislabels the quantity. Fix: divide by norms
to match the protocol exactly.

### m2 — Per-instance records lack per-instance KL

Protocol §8 asks for per-instance records of "margin shift, KL"; the bundle records
per-instance correctness and margin shifts but only *aggregate* KL per condition.
Add per-instance KL (cheap — already computed in the loop).

### m3 — MIXED_C3 branch effectively unreachable (protocol-tree property, faithfully implemented)

With the documented c1→c2→c3 precedence: `b>0 ∧ c>0 ∧ p≥0.05` → MIXED_C1;
`b>0 ∧ c>0 ∧ p<0.05` → branch (e) or (c2) first. Both rulings say "H1 NOT confirmed,"
so no misclassification occurs — noted for the record, no code change needed.

---

## VERIFIED CLEAN (audited, no action required)

- **V1 — Stage A mechanism:** per-head OV-subspace (dim 64) full-rank Procrustes,
  m=80 same-space anchors (5 entities × 16 templates, subspace-projected both sides),
  rank==64 + spectral-gap>1e-6 guards aborting to HALT_STAGE_A, identity lift via the
  `(R̃−I)` delta form for C3/C5/C6/C7 — all match protocol §3.3/§3.4. D1–D4 fixes present.
- **V2 — Conservative readings C1–C5:** all genuinely conservative or neutral.
  C1 (V1_Anglo support frame) is the only natural reading (EXP065/066 E_0 convention).
  C2 (index-aligned pairing) is arbitrary but applied identically to every fit — and
  arbitrariness can only *weaken* fits, i.e., it errs toward the halt, not toward success.
  C3 (any-guard-violation → whole-run abort) is stricter than head-skipping. C4 (H* = all
  passing when <4) is forced by executability. C5 (templates frozen as constants) is an
  honest pre-registration; sensitivity unmeasured and disclosed.
- **V3 — Hook-point reasoning B1–B3:** the runtime self-check
  (`Σ_h o_h + bias == dense(merged)` to 1e-3, every anchor prompt) verifies the
  *algebraic* decomposition, which is all the downstream code needs. The head-permutation
  worry (B2) was independently re-derived, not taken on trust: under a permuted layout,
  the code's "head h" still computes a *genuine* head's output (both the z-slice and the
  W-block slice permute together), and fit/selection/intervention are all per-index
  consistent with no head-identity claims anywhere. **B2's "harmless by design" is TRUE.**
  fp16 false-failure would fail closed (loud abort), which is safe.
- **V4 — C4 bridge scaling:** cross-checked against EXP066 — there the hook applied
  `0.50 × v_vec` to all conditions including the bridge; here every vector is pre-scaled
  by `ALPHA=0.50` and the hook adds as-is. Net intervention identical; "identical to
  EXP066 `make_bridge_vec`" holds. No deviation.
- **V5 — C5 Haar sampling:** `U @ Vh` from SVD of a Gaussian is Haar-distributed on
  O(64) — correct. Seeds {11,22,33,44,55} match protocol §8.
- **V6 — Benchmark fidelity:** reversal thresholds (planet i≥8, elemental i≥7) and
  `target_first` parity (planet odd, elemental even) all match EXP066 line-for-line.
  "Identical N=60 suite" holds.
- **V7 — Evaluator tree on completed runs:** 10 synthetic cases all classify correctly,
  including branch-(b) precedence over (d), the fixed `b==0∧c==0` canonical logic
  (`b=0,c=2,ΔM<0` → MIXED_C2, not (d)), and both `--historical` dry-runs
  (EXP065 → H1_FALSIFIED with C3 ΔM=0 b=0 / C4 +16.67pp b=10 p=0.0020;
   EXP066 → H1_FALSIFIED with C3 ΔM=0 b=0 / C4 +13.33pp b=8 p=0.0078 —
   artifact-exact).
- **V8 — SHA-256 guard:** binding pre/post match with abort on drift; registered value
  sanity-check-only per protocol E-4. Correct.
- **V9 — Law #13 archive:** `exp067_vectors.pt` contains Q_heads, A_sub, T_sub,
  v_hat_by_vocab, v_tilde, all bases, R_domain, H_star, stage-A table, and metas —
  `‖P_S v̂_k‖` (the T-1 quantity) is recomputable. The T-1 lesson was learned.
- **V10 — Headroom gate, seeds, determinism, hook lifecycle:** all per protocol §5/§8.

---

## Answers to the review brief's specific questions

1. **Protocol fidelity:** faithful except F1 (C2 zero-vector) and m1/m2 (minor).
2. **Conservative readings C1–C5:** genuinely conservative; none smuggles advantage.
3. **Hook-point B1–B3:** self-check sufficient; permutation harmlessness independently
   verified TRUE. One residual: none — fail-closed on layout change.
4. **160m default:** labeling is honest, but the default should change to the in-scope
   410m (M2) — or the evaluator must be scope-gated. An out-of-scope default invites
   protocol-violation-by-accident.
5. **Evaluator:** correct on completed runs (V7); **crashes on halt payloads (M1)** —
   the exact outcomes the runbook sends users to evaluate. UNCLASSIFIED is a genuine
   fail-safe (verified unreachable on sane inputs; fires only on NaN/schema corruption).
6. **RUNBOOK:** would fail a non-expert at phone verification, bundle upload, and silent
   CPU fallback (M3). Fixable with ~15 lines of added instructions.

## Required fixes before execution (checklist)

- [ ] **F1:** C2_vec = `ALPHA * Σ_{h∈H*} Q_h (Q_h^T B_agg)` (one-line fix)
- [ ] **M1:** evaluator handles halt payloads (no KeyError); re-test both halt types
- [ ] **M2:** default 410m OR scope-gated evaluator rulings
- [ ] **M3:** runbook — phone verification, exact upload commands, GPU pre-flight check
- [ ] m1/m2: true-cosine g_h; per-instance KL (opportunistic)
- [ ] Re-review of the F1/M1/M2 diff before execution (Law #14)

*No primary artifacts were modified. No bundle files were edited. History appended, not rewritten.*

---

## RE-REVIEW: Post-Corrections Diff Audit — **VERDICT: EXECUTE**

**Date:** 2026-09-23
**Auditor method:** Independent re-read of every corrected region (not on trust);
ran `test_evaluate_exp067.py` myself; `py_compile` all bundle files; grepped all
assertion layers, callers, scope strings, and halt paths. No bundle files edited.

### F1 — VERIFIED FIXED, and the failure mode is now *impossible by assertion*

1. `C2_vec = ALPHA * sum(Q_heads[h] @ (Q_heads[h].T @ B_agg) for h in H_star)` —
   the protocol §3.4 direct form. Correct.
2. `head_projected_sum(basis_vec, R_by_head)` — the `R_by_head=None` signature default
   is **gone**. The silent-zero path cannot be invoked accidentally; any stale caller
   would fail loudly with TypeError. All 4 remaining callers (C3, C6, C7, C5-seed)
   pass `R_by_head` explicitly — verified by grep.
3. Three assertion layers, all confirmed present and on every execution path:
   - **Precompute block:** C2/C3/C6/C7 norms asserted `> 0` at build time.
   - **C5 per-seed:** each seed's vector asserted `> 0`, norm persisted.
   - **Per-instance arm:** `idx == 0` check inside `eval_test_condition` covers
     C4's per-instance bridge vectors.
   - All norms persisted to `results.json` as `injection_vector_norms` (line 900).
4. **Nuance (non-blocking):** the per-instance arm checks only the first instance.
   This is adequate, not a gap: C2/C3/C5/C6/C7 vectors are instance-invariant
   (precomputed), and C4's bridge vector is unit-normalized (`make_bridge_vec`
   divides by its norm + 1e-12), so a zero C4 vector is impossible by construction.
   Recorded for precision; no change required.

### M1 — VERIFIED FIXED

`normalize_exp067()` checks `outcome` FIRST; halt payloads tolerate missing
`stage_B_conditions`/`baseline_accuracy`; `report()` handles `None` baseline and
`None` C3/C4. The test suite's `make_halt_payload()` key set was cross-checked
against the real `save_halt()` in `run_exp067.py` (lines 469–487) — **identical**,
so the tests exercise reality, not fiction (both halt types, including the headroom
halt's `baseline_accuracy` extra).

Ran the suite myself: **18 assertions, ALL PASS** (the integrator's "19/19"
counts the final "ALL TESTS PASSED" summary line as the 19th PASS — cosmetic
reporting discrepancy, zero correctness impact).

### M2 — VERIFIED FIXED

- Default `--model` is now `pythia-410m` (line 226), the in-scope pre-registered config.
- `--model pythia-160m` prints an unmissable runtime banner (lines 256–265),
  carries `protocol_scope: "OUT-OF-SCOPE ..."` in results.json, and the evaluator
  prints raw stats + `NO PROTOCOL RULING -- OUT-OF-SCOPE PILOT` **instead of**
  branch text. Gate fires on `str(scope).startswith("OUT-OF-SCOPE")`; the in-scope
  string `"IN-SCOPE (pythia-410m, layer 20)"` cannot over-fire — confirmed, and
  test case 4 proves the in-scope run still gets its full ruling.

### M3 — VERIFIED FIXED

- CUDA FATAL: `SystemExit` with a diagnostic message when no GPU and no
  `--allow-cpu`; the override prints an explicit warning (and Law #8 is honored:
  a killed session is logged as data). No silent CPU fallback possible.
- RUNBOOK: step 0 (Kaggle phone verification), pre-flight `nvidia-smi` cell with
  `assert torch.cuda.is_available()` and a stop-if-CPU instruction, copy-paste
  upload commands with the `<dataset-slug>` placeholder plus an `ls` verification
  step. The 410m default is the primary command.

### Minors — VERIFIED FIXED

- **m1:** `g_h` now uses true normalized cosines (`cos_al`, `cos_raw` with
  `/(n1 * nkh)`, lines 458–459) per protocol §3.5.
- **m2:** per-instance KL recorded (`{cond}_kl_div` in instance records, line ~776).

### New-introduction risk scan — CLEAN

Re-scanned every touched region: no off-by-ones in the assertion layers, no
precedence change in the evaluator tree (halt → (b) → (d)/(e) → c1 → c2 → c3 →
unclassified, matching the signed decision tree), no banner logic that can suppress
an in-scope ruling. The CUDA FATAL closes `log_file` before `SystemExit` — clean.
`raise SystemExit(msg)` prints the diagnostic to stderr — correct behavior.

### Residuals (non-blocking, recorded for the record)

1. **`--historical` mode keeps full branch text.** The scope line reads
   "HISTORICAL (pre-EXP067 protocol; unsound operator — illustrative only)", and
   the mode requires an explicit developer flag outside the execution path, so the
   misquotation hazard is far lower than the original M2. Still, a screenshot of
   "RULING: H1 is FALSIFIED" without its scope line is possible. **Recommendation
   (non-blocking):** prepend `NO PROTOCOL RULING -- ILLUSTRATIVE DRY-RUN` above the
   branch text in historical mode, matching the spirit of M2. Acceptable to defer.
2. **30 UNTESTED_ASSUMPTIONS remain unverified without a GPU** — most notably
   runtime/VRAM estimates (unmeasured) and `gpt_neox`/`embed_out` geometry
   attributes on the HF checkpoint. Mitigation: every one of these fails CLOSED
   (shape asserts, the Σ_h self-check, the CUDA FATAL), so the worst case is a
   loud abort, not a corrupted result.

### Final verdict

**EXECUTE.** The bundle is cleared for Kaggle. The F1 silent-zero failure mode —
the single most dangerous spec-faithfulness issue found in this program — is now
impossible by three layers of runtime assertion with an audit trail, not merely
fixed by a code change. All Law #14 gate conditions satisfied.

*No primary artifacts modified. No bundle files edited by the reviewer. History
appended, not rewritten.*
