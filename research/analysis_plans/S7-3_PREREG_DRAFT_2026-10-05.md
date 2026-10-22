# ERRATUM — LOG-4914 (2026-10-05) — appended; the signed plan body below is byte-unchanged

**[FACT]** The bench-sha256 pin in §2 (line 50) and Step 0.3 (line 90) contains a single-hex-digit transcription error at hex position 14: the plan pins `eb304fa65a60b55ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`; the committed EXP135 run's own report (`experiments/runs/EXP135_eval/out/exp135_report.json`, field `bench_sha256`, written by the runner itself) is `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`, and an independent verbatim replication of `build_bench` reproduces that value exactly. The pin is wrong; the bench identity is verified.

**Correction:** wherever the plan pins the bench sha256, read **`eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`**. All thresholds, signals, seeds, screening targets, and the §5 decision rule are unchanged — this is a typo fix to a data pin, not a design change, so the Law #14 SIGN stands.

**[INTERPRETATION]** The Step 0.3 abort worked exactly as pre-registered (exit 44, zero analysis executed) — the fence caught the typo before any number was computed. Review-process lesson: Law #14 reviews must verify long hex pins character-by-character against the committed run report, not trust the drafter's transcription.

---

# S7-3 Pre-registration — Label-free signal inventory (selection-bottleneck screen)

**Status:** DRAFT for independent Law #14 review. Born at the Monday idea session, LOG-4911 (2026-10-05).
**No experiment number minted** (the CEO assigns numbers; this plan mints none).
**Cost:** $0 CPU, **zero new forward passes** — archived per-item records only. Read-only on all data files.

---

## 1. Precise question (Law #15 Q1)

**Question:** After EXP135 (E-step dead), EXP140 (free-energy dead), EXP141 (self-model dead), and TESTA (margin anti-calibrated, ρ=−0.3958): does ANY cheap label-free signal correlate with correctness on this bench family?

**Measurand:** For each of six pre-registered label-free signals S1–S6 (§4), the Spearman rank correlation ρ between the signal (computed with zero label access) and per-item correctness (labels used label-informed for screening only, per Law #7 — §5).

**Endpoint registered:** Per-signal two-sided permutation p (100,000 permutations, seed `20261005`), Bonferroni-corrected over the six tests (α = 0.05/6 ≈ 0.008333). See §7 for the binding decision thresholds.

## Why it matters (Law #15 Q2 — the decision this changes)

Exactly one decision: **KILL or CONTINUE the selection program's founding premise** — that some cheap label-free signal of correctness exists in frozen-model outputs on this bench family. The label-free selection program is the only honest race left and it is tied at zero: every licensed selector to date (E-step, free-energy, self-model, margin) is dead or inverted. This inventory is the cheapest possible decisive test — zero forwards — that either kills the premise outright or licenses the next selector. Downstream: a KILL closes the label-free selection line on this bench family (the program's summit path must then come from architecture, not selection); a LICENSE (any signal passing §7) becomes the next licensed selector candidate with a full pre-registration of its own.

## Why this is the cheapest possible way (Law #15 Q3)

There is no cheaper decision: 0 forward passes, $0, CPU-only re-analysis of already-paid-for records. A weight-only analysis cannot answer it (the question is about output-side scalar signals, not weights); a closed-form bound cannot answer it (no theorem predicts these correlations); new data collection is strictly dominated (the archived records contain every needed field — verified in §3).

## Mathematical license (Law #15 Q4)

**License: [CONJECTURE].** The killed selectors (E-step, free-energy, self-model, margin) are not an exhaustive enumeration of the cheap label-free signal space. If frozen-model outputs carry any correctness information in scalar summaries beyond the mean margin — e.g., in output stability across prompt views (self-consistency literature) or in generation diversity (free-energy spread) — then at least one of S1–S6 will show |ρ|≥0.3 at n=60.

**Quantitative prediction:** Under the conjecture, ≥1 of 6 signals clears |ρ|≥0.3 with p<0.05/6. Under the null (no signal), all six are null after correction.

**Breaking point (where the license fails):** TESTA's anti-calibration (ρ=−0.3958) suggests this bench's position-bias structure may *invert* every scalar signal — if the bench punishes the model's confident answers systematically, then no scalar summary of the same outputs can be positively calibrated, and the battery's modal outcome is six nulls (or further inversions). The license therefore predicts its own most likely death, which is what makes this a falsification-first plan rather than a fishing expedition.

**Steelman (argued at full strength):** The bench family is narrow (60 two-choice items, one model, one task shape); an all-null battery kills the premise *here*, not label-free selection in general — a skeptic will rightly note that six nulls on 60 items is evidence about this bench, not about selection as a program. Conceded in advance: the KILL verdict is explicitly scoped to "this bench family" (§7), and the plan does not generalize beyond it. A second steelman: with n=60 and α=0.00833, the |ρ|≥0.3 bar is only ≈35–40% powered (two-sided; Fisher-z ≈ 0.38 at true |ρ|=0.3, Spearman slightly lower) — a null could be underpowering, not absence. Conceded and handled: every ρ is reported with a 95% CI, and a null is read as "no signal ≥0.3 detectable at n=60," never as "no signal exists" (§9).

---

## 2. Data sources — exact files and columns, verified on disk

All paths below were verified to exist on 2026-10-05 (read-only inspection; no file was opened for writing, no analysis executed).

### Primary sources (battery inputs)

| # | File | Structure (verified) | Columns/fields consumed |
|---|---|---|---|
| D1 | `experiments/runs/EXP135_eval/out/exp135_records.json` | 60 items × 10 conditions (`C1`–`C9`, `cache_unintervened`) × 5 views; every view is exactly `{yhat, margin}` | `yhat` (predicted token id), `margin` (top1−top2 logit gap at the answer position) |
| D2 | `experiments/runs/EXP140_stage1/stage1_records.json` | 60 items, each with 4 branches; no missing `spread`/`acc` (verified 0/60 missing) | `spread` (F-spread, nats/token), `branches[].correct` (bool), `branches[].degenerate` (bool), `acc` (integrity cross-check only — see Step 0) |

### Bench-label reconstruction (screening targets only — Law #7)

- D1's screening target reuses **TESTA's documented convention** (`research/innovation/TESTA_CALIBRATION_2026-10-03.md`): per-view correctness = (`yhat` == `tok1(A)`), item target = 1 if ≥3/5 views correct else 0. Bench reconstructed deterministically from `experiments/runs/EXP135_eval/run_exp135.py` (`build_bench`, `make_views`, `tok1`); bench sha256 `eb304fa65a60b55ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` (matches the committed run). Labels touch only the screening correlation — never any signal definition.
- D2's screening target is self-contained: per-item mean branch correctness = mean(`branches[].correct`) ∈ {0, 0.25, 0.5, 0.75, 1}. No bench reconstruction needed.

### Explicitly excluded sources (with reason — no silent narrowing)

- `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` (60 items; per-arm binary `correct.{C1..C10}`, `rescue_indicators`): contains **no model-output scalars** beyond correctness itself — no label-free signal is derivable from it. Role in this plan: item-set alignment reference only. (Its CPU-smoke-vs-official-GPU provenance caveat, documented in the TESTA record, does not apply here because no correctness value from this file enters any computation.)
- `experiments/runs/EXP094_peritem_l11/out/per_item_records.csv` (180 rows: `item_id, stratum, arm, correct_top1, margin, perturbation_ratio, margin_shift_vs_B`): its bench namespace (`exp092_planetary_2hop_*`, built from EXP093's bench pins) is **not verified identical** to D1's A-vs-C bench (`exp077_planet_2hop_*`). Including it would require a bench-identity verification that is itself un-pre-registered. Excluded from this battery; the verification path is documented as a follow-up battery, not smuggled into this one.
- The candidate record's aspirational signals **entropy, top-2 gap (beyond margin), and attention-entropy proxy are NOT computable from any archived record** (no full per-token distributions, no attention weights archived anywhere in `experiments/runs/`). They are excluded with this reason stated, not silently dropped. The battery below is the six-signal set that is both computable and never tested.

### Grandfathered priors (reported, not re-tested — no double-dipping)

- **TESTA (2026-10-03):** unintervened mean margin m̄⁰ vs correctness on D1's cache — Spearman ρ=−0.3958, p=0.0017, significantly *anti*-calibrated. The battery does **not** re-test unintervened mean margin. S4 below uses *intervention-condition* margins (C1–C9), which TESTA never touched.
- **EXP140 G3:** free-energy calibration screen (min_F / F_bar selection, Spearman + TESTA-style partition) — null, gate reading HELD. The battery does **not** re-test min_F/F_bar calibration. S5 (spread) was used by G2 only as a variance gate, never as a calibration signal; S6 (degenerate-branch fraction) was never tested at all.

---

## 3. The battery — six pre-registered signals (all label-free, all never tested)

All signals are pure functions of model outputs. None accesses labels.

| ID | Name | Definition (exact) | Source |
|---|---|---|---|
| S1 | Margin dispersion | Per-item **std of `margin` across the 5 `cache_unintervened` views** (ddof=1) | D1 |
| S2 | Cross-view agreement | Per item: fraction of the 5 `cache_unintervened` views whose `yhat` equals the **modal** `yhat` across those views (ties in the mode → use the smallest token id; pre-registered tie-break) | D1 |
| S3 | Cross-condition agreement | Per item, per condition (10: `C1`–`C9` + `cache_unintervened`): modal-agreement fraction over its 5 views (same tie-break as S2); signal = **mean over the 10 conditions** | D1 |
| S4 | Intervention-mean margin | Per-item **mean of `margin` over `C1`–`C9` × 5 views** (45 values) | D1 |
| S5 | Free-energy spread | Per-item `spread` field as archived | D2 |
| S6 | Degenerate-branch fraction | Per item: (# branches with `degenerate`=true) / 4 | D2 |

Screening targets: S1–S4 → TESTA's majority-correct partition (1 if ≥3/5 cache views correct else 0); S5–S6 → mean(`branches[].correct`).

---

## 4. Analysis steps — exact, ordered, reproducible

A reviewer with this plan, the two data files, and Python 3.12 + numpy/scipy must be able to reproduce every number. **Zero new forward passes. No data file is modified at any step.**

**Step 0 — Integrity pre-checks (abort conditions pre-registered).**
1. Assert D1 loads with exactly the structure verified above: 10 named conditions × 60 items × 5 views, every view exactly `{yhat, margin}`, no NaN/None margins.
2. Assert D2 loads with 60 items × 4 branches, `spread`/`acc` non-null for all items; assert per-item `acc` == mean(`branches[].correct`) within 1e-9 (cross-check; mismatch → abort, do not proceed).
3. Reconstruct the bench per TESTA's documented method; assert rebuilt bench sha256 == `eb304fa65a60b55ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`; assert every D1 `yhat` ∈ {`tok1(A)`, `tok1(C)`} for its (item, view) — 0 mismatches allowed (abort otherwise).
4. Missing-data rule: any signal undefined for an item (cannot occur per the verified schema, but pre-registered anyway) → pairwise deletion for that signal; if >6/60 items (>10%) are missing for any signal, that signal is reported **UNTESTABLE** (not null) and excluded from the KILL reading.

**Step 1 — Signal computation.** Compute S1–S6 per §3, exactly as defined (S2/S3 tie-break: smallest token id). Write the 60×6 signal matrix to a new results file (never into the archives).

**Step 2 — Screening targets.** Compute the S1–S4 binary target (≥3/5 views correct) and the S5–S6 graded target (mean branch correctness), per §2. Law #7 firewall: labels enter only here.

**Step 3 — Statistics (per signal, identical procedure).**
1. Spearman rank correlation ρ between the signal vector and the target vector (n=60; scipy `spearmanr`, default tie handling).
2. Two-sided permutation p: 100,000 permutations of the target vector, seed `20261005` (numpy `default_rng(20261005)`), test statistic |ρ|; p = (# permuted |ρ| ≥ observed |ρ| + 1) / (100001).
3. 95% CI on ρ via Fisher z-transform (reported for every signal, null or not).
4. Achieved-power statement: report the minimum |ρ| detectable at 80% power given n=60 and α=0.00833 (closed-form approximation, pre-registered as a reporting requirement, not a decision input).

**Step 4 — Decision.** Apply §7's binding thresholds to the six (ρ, p) pairs. Write the full results (signals, targets, ρ, p, CIs, power note, decision) to `research/analysis_plans/S7-3_RESULTS_YYYY-MM-DD.json` + a one-page verdict memo. Log the outcome as the next LOG entry; mint no experiment number from this plan alone.

---

## 5. Decision rule — quantitative, falsifiable, fixed before any analysis

**Significance bar (pre-registered):** a signal is *significant* iff two-sided permutation p < 0.05/6 ≈ 0.008333 **and** |ρ| ≥ 0.3 (effect-size floor; a significant-but-tiny ρ licenses nothing).

- **KILL:** all six signals fail the bar (every p ≥ 0.008333, or |ρ| < 0.3 wherever p passes) → **KILL the premise** "a cheap label-free correctness signal exists on this bench family." Scoped reading (pre-registered): the kill covers the inventoried signal space on this 60-item bench family; it does not generalize beyond it (steelman conceded in §1). The grandfathered inverse-margin (TESTA) stands as prior evidence of bench inversion, not as a surviving selector — consistent with EXP141's G3 logic (inverted → KILL the family).
- **LICENSE/CONTINUE:** any signal S_i meets the bar (|ρ| ≥ 0.3 **and** p < 0.008333) → **CONTINUE**: S_i is licensed as the next selector candidate, with a full fresh pre-registration (including a held-out validation design) required before any selection experiment. A negative ρ licenses only an *inverted* selector candidate, flagged as bench-inversion evidence.
- **UNTESTABLE** (Step 0.4) for any signal removes that signal from the KILL reading; if ≥2 signals are untestable, the battery as a whole is reported INCONCLUSIVE (not KILL).

No other outcome is licensed. In particular: p < 0.05 uncorrected, |ρ| ≥ 0.3 without significance, or any post-hoc signal discovered during analysis **cannot** trigger CONTINUE — those go to a new pre-registration.

---

## 6. LOG-218 belief-change statement

**Belief:** "Some label-free signal of correctness must exist in frozen-model outputs — the selection program's founding bet."

**Overturning observation (pre-registered):** a six-signal battery (S1–S6), each a cheap label-free scalar never before tested, all null after Bonferroni correction at n=60 — i.e., the KILL outcome of §5. That observation would overturn the belief on this bench family and close the label-free selection line here.

---

## 7. Falsification-first self-check

**What result would embarrass this plan?** Three, in increasing order of damage:

1. *An all-null battery that is really underpowering.* With n=60 and α=0.00833, the |ρ|≥0.3 bar is only ≈35–40% powered (two-sided, true |ρ|=0.3) — the single most likely embarrassment is a null that reflects sample size, not absence. **Why the plan survives it:** the underpowering is conceded in the license itself (§1 steelman), every ρ carries a pre-registered 95% CI, Step 3.4 forces a minimum-detectable-effect statement, and the KILL verdict is worded as "no signal ≥0.3 detectable at n=60" — the plan cannot be embarrassed by an objection it pre-registered.
2. *A "hit" that is really the bench's position-bias structure again.* TESTA showed this bench inverts margin; any margin-derived signal (S4) could inherit the inversion and pass |ρ|≥0.3 for the wrong reason. **Why the plan survives it:** the decision rule is direction-agnostic (|ρ|) and a negative ρ licenses only an inverted candidate explicitly flagged as bench-inversion evidence — the plan cannot launder an inversion into a positive selector.
3. *A hit on S5/S6 that EXP140's G3 already implicitly killed.* If spread or degenerate-fraction correlates with correctness, G3's null (on min_F/F_bar) looks inconsistent. **Why the plan survives it:** G3 tested *selection by* free energy (a decision rule), not *calibration of* spread/degeneracy (a screening correlation) — different estimands, no contradiction; the plan states this distinction in §2 so a reviewer cannot claim double-counting in either direction.

The plan's deepest honesty: its own license (§1 breaking point) predicts the modal outcome is six nulls. A plan that pre-registers its own most likely death is doing falsification-first correctly.

---

## 8. Reproducibility pins

- Seeds: permutation seed `20261005` (this battery); TESTA's seed `20261003` is **not** reused.
- Libraries: Python 3.12, numpy 2.5.3, scipy (any ≥1.14; `spearmanr` tie behavior is version-stable and asserted in Step 0 by a pinned unit check on a 5-point toy vector — executor includes the check).
- Data: D1, D2 as archived (read-only; executor asserts the Step-0 integrity checks before computing anything).
- No GPU, no model loads, no tokenizer loads beyond the integer `tok1` mapping already documented in the TESTA record (no forward passes — mapping only).
- Executor script (to be written at execution time, after Law #14 SIGN): `research/analysis_plans/s73_execute_YYYYMMDD.py`, seeded, with the Step-0 toy-vector unit check; results JSON + verdict memo as named in Step 4.

## 9. Epistemological labeling (per `AGENTS.md` §5)

- [FACT]: file paths, structures, and column contents in §2 (verified on disk 2026-10-05); TESTA's reported ρ=−0.3958, p=0.0017; EXP135's ρ̄*=−0.0042; EXP140 G3's null gate reading; the 100k-permutation / seed conventions quoted from the TESTA and EXP141 records.
- [CONJECTURE]: the Law #15 license (§1) — the killed selectors are not exhaustive of the cheap label-free signal space.
- [ASSUMPTION]: the Step-0 integrity checks pass (abort otherwise); bench reconstruction reproduces the committed sha (verified by TESTA, re-asserted here).
- [HYPOTHESIS]: "a cheap label-free correctness signal exists on this bench family" — the proposition this battery is built to falsify.
- [OBSERVATION] vs [INTERPRETATION]: the six (ρ, p) pairs the executor will produce are future [OBSERVATION]s; the KILL/CONTINUE readings in §5 are [INTERPRETATION]s bound by the pre-registered thresholds — no post-hoc re-reading is licensed.

---

*Draft prepared 2026-10-05 for independent Law #14 review. Ambiguities resolved from the LOG-4911 / CANDIDATE_BACKLOG records are listed in the drafting agent's handoff report.*
