# Independent Exact-Artifact Verdict Review — EXP120 (H15/LFH-GEN2)

**Lane:** LOG-4634 (independent Law #14-style exact-artifact verdict review; independent of the LOG-4633 execution lane).
**Date:** 2026-09-29
**Target:** `~/workspace/SCBI/research/experiments/EXP120_LFHGEN2_REPORT_2026-09-29.md` (registered verdict: CONTINUE)
**Pre-registration:** `~/workspace/SCBI/research/prereg/EXP_PREREG_H15_LFHGEN2_2026-09-29.md` (LOG-4631 draft → LOG-4632 SIGN, zero fixes)
**Gate memo:** `~/workspace/SCBI/research/strategy/H15_GATE_2026-09-29.md` (LOG-4630 PASS)

## Verdict

**QUALIFY — the registered CONTINUE stands. One factual caveat: the report's descriptive
one-sided binomial p-value ("≈0.0009" for 25/30, report §7) is incorrect. The exact value is
0.00016 (one-sided) / 0.00032 (two-sided). The error understates the evidence and cannot
have manufactured the verdict: the registered bar is count-based (≥20/30 with G<0.30), and
the bar's own licensed p-values (20/30 → 0.0494, 19/30 → 0.1002, 18/30 → 0.1808) are exact.
Recommendation: an append-only erratum on the report correcting the descriptive p to the
exact 0.00016 — never a silent edit.**

## What was independently verified (all from the raw artifacts, no trust in the report's text)

### 1. Head-test accuracy, recomputed from scratch
From `exp120_embeddings.npz` (60×1024 float32, ids byte-match per-item records 60/60),
`exp120_head_params.npz` (`coef_`, `intercept_`), and `exp120_test_ids.json`, with labels taken
directly from the per-item `y` field (not inferred): logistic decision `sign(w·x + b)` on the
30 held-out test items → **25/30 correct**. Label distribution on test: 15 positive / 30 (balanced).
- Per-cell (phrasing × flipped), test split: A-first/original **4/8**, A-first/flipped **7/7**,
  C-first/original **7/7**, C-first/flipped **7/8** — matches the report exactly.
- One-sided exact binomial P(X≥25 | 30, 0.5) = 174437 / 2³⁰ = **0.0001624** (report says ≈0.0009 —
  the caveat above; the normal-with-continuity value 0.0009 corresponds to 24/30, not the observed 25/30).

### 2. G metric
acc(F=flipped-False) = 11/15 = 0.7333; acc(T=flipped-True) = 14/15 = 0.9333; **G = −0.2000 < 0.30** ✓.
N_F = N_T = 15 ✓. The G≥0.30 template-detector bar is 2.5 items of margin away on the signed side.

### 3. Bars applied per §4
≥20/30 with G<0.30 → CONTINUE ✓. The falsification branch "construction gates pass → hash OK →
split disjoint → determinism OK → artifact gate OK → evaluate → CONTINUE" matches the pre-reg's
§4/§6 tree. No other branch is licensed; none was taken.

### 4. Construction gates (Stage A — the breaking point; all passed, verified from `exp120_result.json` + builder)
- Design-time assertions: 60 items, phrasing 30/30, four 15-item cells (15/15/15/15), flipped items
  use the opposite verb family, extraction contract, `exp120_*` ID namespace disjoint from bench 1,
  label pin per-item — all pass. Bench-2 canonical pin `1d7d22c0…82fb2eee` identical across
  worksheet, stdout, and report; deterministic re-parse ×2 byte-identical.
- **G-C1** pure-template detector: 30/60 ≤ 36/60 ✓ (chance-level, by construction).
- **G-C2** |Pearson| = 0.0475 ≤ 0.10 ✓ — and the implementation reads only bench-1 builder
  records (`TRIPLES`/`QUADS` entity-index sequences via importlib) as a design check: **no bench-1
  labels or embeddings enter the analysis** — the Law #13 fence is real, not decorative.
- **G-C3** template-decomposition pin: QUESTION_SUFFIX byte-exact + deterministic rebuild ✓.
- Template-vocabulary decorrelation independently confirmed from the canonical JSON: no bench-2
  premise contains bench-1's verb families — " outranks " and " is lower than " are absent 0/60
  (bench-1's families verified against `build_exp107_bench.py` lines 14–21); bench-2 uses the new
  "surpasses"/"is below" families; entity sets are new (rivers: Nile/Amazon/Yangtze/Ganges/Thames;
  trees: Oak/Pine/Birch/Cedar/Maple), all 10 confirmed present across bench-2 premises.

### 5. H5 protocol pinned verbatim
Seed 20260929; `train_test_split(test_size=0.5, random_state=20260929, stratify="{phrasing}_{flipped}")`;
train 30 / test 30, **ID overlap 0**; per-cell test 8/7/7/8 ✓; `LogisticRegression(penalty='l2', C=1.0,
solver='lbfgs', max_iter=1000, random_state=20260929)`; no tuning, no re-seeds ✓.
- Determinism re-fit: byte-identical test predictions ✓ (logged in stdout, not just claimed).
- Stratification key includes phrasing (which determines y): standard balanced stratified split,
  same as the pinned H5 discipline — test labels never touched in training. No Law #7 issue.
- FIX-1 label-pin discipline honored prospectively: the builder's module docstring cites the
  meaning-preserving construction ("the ranking meaning (A > B > C [> D]) ... preserved") plus
  an independent per-item assertion — never a truncated comment.

### 6. Pins and Δθ=0
Backbone LOG-331 hash `ec276abe3902fab0…38e0ed` verified **before AND after** all 60 extractions
(stdout log) — match both times (Δθ=0). Environment pins: torch 2.14.0+cpu, transformers 5.17.0,
sklearn 1.9.1, numpy 2.5.3, threads 2/2, `device_map='cpu'` accepted at load. Extraction site:
`hidden_states[20]`, final token, premise-only (no question, no option list — the EXP107 discipline).

### 7. Record-keeping gate (§3.7 — the EXP119 lesson, applied)
All seven artifacts hash-pinned in the worksheet **before** the verdict line: builder script
`52ceca4e…`, canonical JSON, per-item JSON, embeddings npz, train IDs, test IDs, head params.
The run-1 crash is exactly as disclosed: verdict CONTINUE was printed, then `json.dump` failed at
line 269 on tuple keys (TypeError, exit 1). The repair (string-keyed gate record) was followed by a
**full deterministic re-run** — byte-identical artifact hashes and byte-identical verdict across runs;
both logs preserved (`exp120_stdout_run1.log`, `exp120_stdout.log`). The disclosure is honest and
the evidentiary chain is intact.

### 8. Law #9 / Law #7 / Law #4 / Law #8 / Law #11 fences
- Law #9: primary metric (test accuracy) and bars were registered in the pre-reg §4 before any
  output was inspected; per-cell values are reported as descriptive only.
- Law #7: labels pinned independently at construction (FIX-1 discipline); head fit on train split only.
- Law #4: the §4 bars are the gate memo's bars verbatim; no post-hoc bar movement.
- Law #8: EXP111's bench-1 observation is restated, never re-adjudicated.
- Law #11: the verdict concerns only the generality hypothesis (two-bench observation).

### 9. The unlicensed fence
Pre-reg §2/§7.1 explicitly un-licenses post-hoc cross-bench effect-size comparisons (no t-test
between bench-1 and bench-2 accuracies). The report states each bench's own numbers descriptively
(24/30 & G=0.0000 bench-1; 25/30 & G=−0.2000 bench-2) and **performs no statistical comparison**
— compliant. §8's "does NOT claim" fences (no generality beyond the two benches/layer/model; no
capability claims without downstream causal tests; no re-licensing of H1/H4 or closed families;
N1 — Known Combination) are all present and correctly scoped.

## Caveat (the QUALIFY item — documentation-precision, verdict-immaterial)

Report §7 says "one-sided binomial p ≈ 0.0009 vs chance" for the observed 25/30. The exact value is
**0.0001624** (one-sided; two-sided 0.0003249). The executor never computed a p-value (the script
prints no p; the ≈0.0009 was hand-written by the execution lane). The error is in the conservative
direction — it understates the evidence — so it cannot have licensed the CONTINUE: the registered
bar (≥20/30, exact p=0.0494) is cleared by the count alone. Recommended follow-up (not by this lane):
append-only erratum on the report correcting the descriptive p to exact 0.00016; never a silent edit.

## What this verdict licenses and does not claim (binding)

- **Licenses:** EXP111's trained-head signal (24/30, G=0.0000, bench 1) replicates at 25/30 with
  G=−0.2000 on an independently constructed, template-decorrelated second bench. The output-side
  readout room's single positive is no longer a one-bench observation — it is a two-bench
  observation of the same trained-readout signal.
- **Does NOT license:** anything beyond a correlation at layer 20 on two benches. The narrow
  reading stands: the head extracts the subject-position cue on a second bench — a legitimate
  frozen-backbone signal, not steering, not decision-flip, not capability. The label-free race
  remains tied at zero; EXP112's HELD is untouched.

## Lane boundaries

$0 CPU (read-only verification; one sklearn import attempt failed on a pandas binary mismatch in
this environment — all recomputation was done with numpy only, which is sufficient for the
linear-decision check). No signed artifact modified; no data invented; no follow-ups dispatched;
no push; no credentials, weights, or GPU contact. Single-lane fence held: review only.
