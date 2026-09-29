# EXP120 (H15/LFH-GEN2) Run Report — 2026-09-29

**Status:** EXP120 executed per signed pre-registration `EXP_PREREG_H15_LFHGEN2_2026-09-29.md` (LOG-4631 draft → LOG-4632 SIGN, zero fixes → CEO launch as EXP120).

## Verdict

**CONTINUE** — overall test accuracy **25/30 = 0.8333** with **G = −0.2000** (< 0.30). The generality hypothesis CONTINUES: the trained L2-logistic head extracts a template-invariant feature on a second, independently constructed template-decorrelated bench.

## 1. Stage A — bench-2 construction (the breaking point; passed)

[OBSERVATION] Bench 2 was independently authored (`build_exp120_bench.py`): two new 5-entity named sets in new domains (rivers: Nile/Amazon/Yangtze/Ganges/Thames; trees: Oak/Pine/Birch/Cedar/Maple), disjoint from the EXP107 bench's planets/elements; new verb families (family-1 "surpasses", family-2 "is below"); no bench-2 premise contains `" outranks "` or `" is lower than "`. Structure parallel to bench 1: 60 items, 2-hop/3-hop premises, `tuple[0]` = the highest-ranked entity A on all 60 items (the builder's meaning-preserving construction docstring plus the independent per-item assertion — the EXP119 FIX-1 discipline), `phrasing` 30/30, deterministic meaning-preserving flip within each phrasing group (even sorted positions) → four balanced 15-item cells, ID namespace `exp120_*` disjoint from bench 1.

[OBSERVATION] All construction gates passed — no gate fired:
- Design-time assertions (60 items, phrasing 30/30, four 15-item cells, flipped items use the OPPOSITE verb family from originals, extraction contract `premise == prompt[:prompt.index(' Question:')]`, ID-namespace disjointness, label check `tuple[0]` in first premise sentence iff A-first): **pass**.
- **G-C1** pure-template detector: **30/60** ≤ 36/60 — pass (by construction).
- **G-C2** entity-rank correlation vs EXP107 builder records: **−0.0475**, |·| = 0.0475 ≤ 0.10 — pass (design check only; fed no bench-1 labels or embeddings into the analysis — Law #13 fence).
- **G-C3** template-decomposition pin: QUESTION_SUFFIX byte-exact, deterministic rebuild — pass.
- Bench-2 canonical pin: `1d7d22c0…82fb2eee`; deterministic re-parse ×2 byte-identical — pass.

## 2. Stage B — embedding extraction (pre-reg §3.3 — all pins verified)

[OBSERVATION]
- Environment: torch=2.14.0+cpu, transformers=5.17.0, sklearn=1.9.1, numpy=2.5.3; threads set=2, read-back=2; torch/numpy seeds=0.
- `device_map='cpu'` accepted at load (logged).
- Backbone LOG-331 pin `ec276abe3902fab0…38e0ed` verified **before AND after** all 60 extractions — match both times (**Δθ=0**).
- 60 forward passes on bench-2 premises only (no question, no option list — the EXP107 extraction discipline), `hidden_states[20]`, final token, float32, CPU, `model.eval()`, `torch.no_grad()`.
- Embeddings (60, 1024) float32, all finite; npz ids byte-match the bench-2 per-item records (60/60).

## 3. Split (H5 §3.3 pinned verbatim)

[OBSERVATION] sklearn==1.9.1, numpy==2.5.3, seed **20260929**, `train_test_split(test_size=0.5, random_state=20260929, stratify=f"{phrasing}_{flipped}")`. Train n=30, test n=30, **ID overlap = 0** (disjointness asserted). Per-cell test counts: A-first_False 8, A-first_True 7, C-first_False 7, C-first_True 8 — the pinned 8/7/7/8 encoding. N_F=15 (flipped=False test), N_T=15 (flipped=True test) — both denominators as pinned.

## 4. Head training (pinned spec, Law #7 — no tuning)

[OBSERVATION] `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)` on the 30-item train split. No L2-C sweep, no layer choice, no solver choice, no seed re-rolls.

- Determinism pass: re-fit from the same npz → **byte-identical test predictions** (pass).
- Head weight hash: `203809e8…729b92`; weight L2 norm 1.756494.
- Train accuracy (sanity): 1.0000.

## 5. Record-keeping gate (§3.7 — passed before the verdict)

[OBSERVATION] All seven artifacts were present and hash-pinned before the verdict was computed: builder script, bench-2 canonical JSON, per-item JSON records, embedding npz, train/test ID lists, head parameters. Missing artifact → RUN-INVALID did not fire. A mechanical serialization defect (tuple-keyed gate dict in the first worksheet write, run 1) was repaired by converting the gate record to string keys; the full script was re-run deterministically (same builder, same seeds, same model) — byte-identical artifact hashes and byte-identical verdict across runs. Both run logs are preserved (`exp120_stdout_run1.log`, `exp120_stdout.log`).

## 6. Test evaluation (n=30)

| Metric | Value |
|---|---|
| Overall accuracy | 25/30 = 0.8333 |
| acc(flipped=False, N_F=15) | 0.7333 (11/15) |
| acc(flipped=True, N_T=15) | 0.9333 (14/15) |
| **G** = acc(F) − acc(T) | **−0.2000** |

Per-cell descriptives: A-first/original 0.5000 (4/8); A-first/flipped 1.0000 (7/7); C-first/original 1.0000 (7/7); C-first/flipped 0.8750 (7/8).

## 7. Decision bars applied (pre-reg §4 verbatim)

- G ≥ 0.30 (template-detector signature)? **No** (G=−0.2000 — negative, i.e., the head did *better* on flipped-word items; no template-detection signature in either direction).
- Overall ≥ 20/30 with G < 0.30? **Yes** (25/30; one-sided binomial p ≈ 0.0009 vs chance).
- **→ CONTINUE.** Falsification-tree branch: construction gates pass → hash OK → split disjoint → determinism OK → artifact gate OK → evaluate → G<0.30 and overall ≥20/30 → CONTINUE.

## 8. What this verdict licenses and does NOT claim

**Licenses:** the generality hypothesis CONTINUES — EXP111's trained-head signal (24/30, G=0.0000 on bench 1) replicates at 25/30 with G=−0.2000 on an independently constructed, template-decorrelated second bench. The output-side readout room's single positive result is no longer a one-bench observation.

**Does NOT claim** (§8 fences): this is a correlation at one layer (20) on two benches — not consciousness, not generality beyond the benches, not superhuman cognition. Capability claims require downstream causal tests (steering, decision-flip). The bench-2 labels encode the subject-position cue (A-first → y=1), so a CONTINUE means the head extracts *position* on a second bench — a legitimate frozen-backbone signal but a narrow one. Does not re-license H1/H4, static-injection lines, or any closed family. No cross-bench effect-size comparison was performed (unlicensed). Novelty N1 — Known Combination.

## 9. Files

- Report: this file (`EXP120_LFHGEN2_REPORT_2026-09-29.md`)
- Raw logs: `~/workspace/SCBI/experiments/runs/EXP120_lfhgen2/out/` — `exp120_execute.py`, `exp120_result.json` (worksheet: all raw records), `exp120_stdout.log` (+ `_run1.log`), `exp120_console.log` (+ `_run1.log`), `exp120_bench2_canonical.json`, `exp120_per_item.json`, `exp120_embeddings.npz`, `exp120_train_ids.json`, `exp120_test_ids.json`, `exp120_head_params.npz`
- Builder: `~/workspace/SCBI/experiments/runs/EXP120_lfhgen2/build_exp120_bench.py`

No data invented. Falsification-tree branch: CONTINUE. Lane stops here.

## 10. Erratum (LOG-4635, 2026-09-29)

Report §7 states 'one-sided binomial p ≈ 0.0009 vs chance' for the 25/30 test accuracy. This is incorrect: exact one-sided P(X≥25|30,0.5) = 174437/2³⁰ = 0.0001624 (two-sided 0.0003249). The executor never computed a p-value (the script prints none); the ≈0.0009 was hand-written and matches the normal-approximation value for 24/30, not the observed 25/30. The error understates the evidence and cannot have licensed the CONTINUE: the registered bar (≥20/30, exact p=0.0494) is cleared by the count alone. The descriptive p-value is corrected to exact 0.00016 (one-sided) / 0.00032 (two-sided). No verdict change: EXP120 CONTINUE stands. — Independent exact-artifact review, LOG-4634 (VERDICTREVIEW_EXP120_2026-09-29.md).
