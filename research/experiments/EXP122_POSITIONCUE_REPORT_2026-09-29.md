# EXP122 (H16/POSITION-CUE) Run Report — 2026-09-29

**Status:** EXP122 executed per signed pre-registration `EXP_PREREG_H16_POSITIONCUE_2026-09-29.md` (LOG-4650 draft → LOG-4651 Law #14 SIGN → LOG-4652 FIX-1–FIX-4 byte-verified → CEO launch as EXP122).

## Verdict

**CONTINUE** — overall test accuracy **27/30 = 0.9000** with **G = −0.0667** (< 0.30). The identity-readout hypothesis CONTINUES: the trained L2-logistic head extracts the target entity's domain-set identity (D1 animals vs D2 fruits) on a position-scrambled bench where the target's sentence position carries no label information.

## 1. Stage A — bench-3 construction (the breaking point; passed)

[OBSERVATION] Bench 3 was independently authored (`build_exp122_bench.py`): two new 5-entity named sets in fresh domains (D1 animals: Lion/Tiger/Bear/Wolf/Fox; D2 fruits: Apple/Mango/Cherry/Grape/Plum), disjoint from bench-1's planets/elements and bench-2's rivers/trees; new verb families (family-1 "ranks above"/"ranks below"; family-2 "dominates"/"is dominated by"); no bench-3 premise contains `" outranks "`, `" is lower than "`, `" surpasses "`, or `" is below "`. Structure: 60 items, 2-hop/3-hop premises, `tuple[0]` = the highest-ranked entity A on all 60 items (the builder's meaning-preserving construction docstring plus the independent per-item assertion `y == (tuple[0] in VOCAB_ANIMAL)` — the EXP119 FIX-1 discipline), mixed-domain non-target tuples (B, C, D drawn from both D1 and D2 by a label-independent parity pattern), `phrasing` 30/30 (target-first/target-last original groups), deterministic meaning-preserving flip within each phrasing group (even sorted positions) → four balanced 15-item cells. The flip moves the target to the opposite sentence end (final position = phrasing XOR flipped, verified per-item). Labels: y=1 iff tuple[0] ∈ D1 (animals), balanced 30/30; within each label class the target's final sentence position is balanced 15/15 (position-scrambled). ID namespace `exp122_*` disjoint from benches 1/2.

[OBSERVATION] All construction gates passed — no gate fired:
- Design-time assertions (60 items, phrasing 30/30, four 15-item cells, flipped items use family-2 vs originals' family-1, extraction contract `premise == prompt[:prompt.index(' Question:')]`, ID-namespace disjointness, label pin, position pin `final_first == (phrasing XOR flipped)`, entity distinctness, mixed-domain non-targets, hop×label balance): **pass**.
- **G-C1** pure-template detector: **32/60** ≤ 36/60 — pass (by construction).
- **Position-scramble gate** (new, discriminative): pure-position detector **30/60** ≤ 36/60 — pass (by construction; position carries no label information).
- **G-C2** entity-rank correlation vs EXP107 builder records: **−0.0322**, |·| = 0.0322 ≤ 0.10 — pass (design check only; fed no bench-1 labels or embeddings into the analysis — Law #13 fence). Canonical order for r3 is sorted-by-ID; the bench emission order's (2-hop, 3-hop) block layout spuriously aligns with bench-1's (triples, quads) layout (position-3 pad-structure r=+0.71), so sorted-by-ID is the documented canonical order.
- **G-C3** template-decomposition pin: QUESTION_SUFFIX byte-exact, deterministic rebuild — pass.
- Bench-3 canonical pin: `2b65f01e…82b165ca`; deterministic re-parse ×2 byte-identical — pass.

## 2. Stage B — embedding extraction (pre-reg §3.3 — all pins verified)

[OBSERVATION]
- Environment: torch=2.14.0+cpu, transformers=5.17.0, sklearn=1.9.1, numpy=2.5.3; threads set=2, read-back=2; torch/numpy seeds=0.
- `device_map='cpu'` accepted at load (logged).
- Backbone LOG-331 pin `ec276abe3902fab0…38e0ed` verified **before AND after** all 60 extractions — match both times (**Δθ=0**).
- 60 forward passes on bench-3 premises only (no question, no option list — the EXP107 extraction discipline), `hidden_states[20]`, final token, float32, CPU, `model.eval()`, `torch.no_grad()`.
- Embeddings (60, 1024) float32, all finite; npz ids byte-match the bench-3 per-item records (60/60).

## 3. Split (H5 §3.3 pinned verbatim)

[OBSERVATION] sklearn==1.9.1, numpy==2.5.3, seed **20260929**, `train_test_split(test_size=0.5, random_state=20260929, stratify=f"{phrasing}_{flipped}")`. Train n=30, test n=30, **ID overlap = 0** (disjointness asserted). Per-cell test counts: target-first_False 8, target-first_True 7, target-last_False 7, target-last_True 8 — the pinned 8/7/7/8 encoding. N_F=15 (flipped=False test), N_T=15 (flipped=True test) — both denominators as pinned.

## 4. Head training (pinned spec, Law #7 — no tuning)

[OBSERVATION] `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)` on the 30-item train split. No L2-C sweep, no layer choice, no solver choice, no seed re-rolls.

- Determinism pass: re-fit from the same npz → **byte-identical test predictions** (pass).
- Full deterministic rerun (fixed seeds, same builder, same model): **byte-identical metric** (27/30, G=−0.0667, CONTINUE), byte-identical head hash, byte-identical artifact hashes across runs. Both run logs preserved (`exp122_stdout_run1.log`, `exp122_stdout.log`, `exp122_console_run1.log`, `exp122_console.log`).
- Head weight hash: `5ac7b477…20aa4b`; weight L2 norm 1.555946.
- Train accuracy (sanity): 1.0000.

## 5. Record-keeping gate (§3.7 — passed before the verdict)

[OBSERVATION] All seven artifacts were present and hash-pinned before the verdict was computed: builder script, bench-3 canonical JSON, per-item JSON records, embedding npz, train/test ID lists, head parameters. Missing artifact → RUN-INVALID did not fire.

## 6. Test evaluation (n=30)

| Metric | Value |
|---|---|
| Overall accuracy | 27/30 = 0.9000 |
| acc(flipped=False, N_F=15) | 0.8667 (13/15) |
| acc(flipped=True, N_T=15) | 0.9333 (14/15) |
| **G** = acc(F) − acc(T) | **−0.0667** |
| Exact one-sided p (executor) | 0.0000042 |
| Exact two-sided p (executor) | 0.0000084 |

Per-cell descriptives: target-first/original 0.7500 (6/8); target-first/flipped 1.0000 (7/7); target-last/original 1.0000 (7/7); target-last/flipped 0.8750 (7/8).

## 7. Decision bars applied (pre-reg §4 verbatim)

- G ≥ 0.30 (word-family detector signature)? **No** (G=−0.0667 — negative; no template-detection signature in either direction).
- Overall ≥ 20/30 with G < 0.30? **Yes** (27/30; exact one-sided p=0.0000042 vs chance, executor-computed via math.comb — defect class (a) honored).
- **→ CONTINUE.** Falsification-tree branch: construction gates pass → hash OK → split disjoint → determinism OK → artifact gate OK → evaluate → G<0.30 and overall ≥20/30 → CONTINUE.

## 8. What this verdict licenses and does NOT claim

**Licenses:** the identity-readout hypothesis CONTINUES — the trained head extracts the target's domain-set identity (D1 vs D2) at 27/30 with G=−0.0667 on a position-scrambled bench where the target's sentence position is balanced 15/15 within each label class. The two-bench CONTINUE (EXP111 24/30, EXP120 25/30) gains a mechanistic foothold: the signal is not exhausted by a subject-position detector.

**Does NOT claim** (§8 fences): this is a correlation at one layer (20) on three benches — not consciousness, not generality beyond the benches, not superhuman cognition. **Decodability, not steering or capability** — the head extracts a domain-set property of the target at layer 20, nothing more. Capability claims require downstream causal tests (steering, decision-flip); the capability scoreboard stays at zero positive signals for autonomous steering. Does not re-license H1/H4, static-injection lines, or any closed family. No cross-bench effect-size comparison was performed (unlicensed). No re-reading of bench-1/2 data, no re-fitting, no re-cutting (Law #13 fence). Novelty N1 — Known Combination.

## 9. Files

- Report: this file (`EXP122_POSITIONCUE_REPORT_2026-09-29.md`)
- Raw logs: `~/workspace/SCBI/experiments/runs/EXP122_positioncue/out/` — `exp122_execute.py`, `exp122_result.json` (worksheet: all raw records), `exp122_stdout.log` (+ `_run1.log`), `exp122_console.log` (+ `_run1.log`), `exp122_bench3_canonical.json`, `exp122_per_item.json`, `exp122_embeddings.npz`, `exp122_train_ids.json`, `exp122_test_ids.json`, `exp122_head_params.npz`
- Builder: `~/workspace/SCBI/experiments/runs/EXP122_positioncue/build_exp122_bench.py`

No data invented. Falsification-tree branch: CONTINUE. Lane stops here.
