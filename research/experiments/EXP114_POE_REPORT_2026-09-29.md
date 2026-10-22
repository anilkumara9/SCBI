# EXP114 (H8/POE) Execution Report — Positional-Order Ensembling

**Experiment:** EXP114 · **Hypothesis:** H8/POE · **Log:** LOG-4591 (2026-09-29)
**Pre-registration:** `research/prereg/EXP_PREREG_H8_POE_2026-09-29.md` (clean Law #14 SIGN, zero fixes — LOG-4589; CEO launch LOG-4590)
**Verdict: KILL** — net (b − c) = −3 ≤ 0 → the positional-order-ensembling TTA axis is dead for this task class.

## 1. Result (binding)

| Metric | Value |
|---|---|
| Ensemble accuracy (K=5 order-averaged) | 38/60 = **0.6333** |
| Baseline accuracy (canonical order) | 41/60 = **0.6833** |
| McNemar table | **b = 2** (baseline wrong, ensemble right), **c = 5** (baseline right, ensemble wrong), n = 7 |
| One-sided exact McNemar p | **0.9375** (= P(X ≥ 2 \| 7, 0.5)) |
| Net (b − c) | **−3** |

**Falsification-tree branch taken:** `b − c ≤ 0 → KILL` (net = −3 ≤ 0). [FACT] The registered CONTINUE branch required p ≤ 0.05 with b > c; the HELD branch required net > 0. Neither condition obtained.

[OBSERVATION] The ensemble did not merely fail to improve — it scored 5pp *below* the canonical-order baseline. Order averaging over a single nuisance permutation hurt the registered decision on this bench.

Per-cell descriptive (no decision branch reads these): A-first/flipped acc_ens=0.40/acc_base=0.60; A-first/original 0.533/0.667; C-first/original 1.000/0.933; C-first/flipped 0.600/0.533.

## 2. Falsification-tree gates (all passed)

| Gate | Result |
|---|---|
| npz archive pin (`6cf4a8a7…af6a76`) | ✔ recomputed, match |
| embeddings-array bytes pin (`9b6e8afb…923`) | ✔ recomputed, match |
| ids-array bytes pin (`3669e102…5075cb9`) | ✔ recomputed, match |
| Bench canonical-JSON pin (`e91b302f…4f5`), 60 items | ✔ match; bench ids == npz ids 60/60 |
| QUESTION_SUFFIX byte-exact | ✔ |
| Backbone LOG-331 pin before first forward | ✔ `ec276abe…38e0ed` |
| Single-token BPE assertion (120 entity texts) | ✔ 120/120, zero failures |
| Backbone LOG-331 pin after last forward | ✔ identical — Δθ=0 |

No RUN-INVALID branch fired. No gate was skipped or substituted.

*Note on a lane-instruction label:* the pre-reg's tree labels bench-pin mismatch as HALT; the CEO launch lane (LOG-4590) directed RUN-INVALID for any pin mismatch. Both mean "no metric exists." Mismatch never occurred, so the label distinction is moot.

## 3. Method as executed (per §3.2–3.5, §3.8)

- Bench: 60-item EXP107 template-decorrelated bench rebuilt deterministically via `build_exp107_bench.build_bench()` (no model calls, no RNG).
- Prompt construction (pinned byte-exact): `premise_i + " Options: " + first + ", " + second + "." + " Question: Who is higher in rank? Answer:"`; no letters anywhere (EXP109 lesson).
- Orders: K=5 i.i.d. bits per item from a single `random.Random(20260929)` instance, sequential draws in canonical bench order; per-item patterns logged in `exp114_worksheet.json`; degenerate 5–0 compositions: 3/60 (≈6% expected).
- Forwards: 360 total (300 ensemble + 60 canonical-order baseline), frozen Pythia-410m, CPU, float32, `torch.no_grad()`, **zero generation**. Completed in 296s.
- Readout: argmax over the two pinned single-token entity-name ids (`tok.encode(" "+E)[0]`); tie-break → E2 applied identically to both arms.
- Ensemble prediction: argmax over mean-of-5 logits; baseline: argmax over single-order logits. Labels: y=1 iff A-first; prediction maps to 1 if `tuple[0]` else 0.

## 4. Environment manifest (Law #13)

torch **2.14.0+cpu**, transformers **5.17.0**, numpy 2.5.3, accelerate 1.15.0; torch threads 2 set / 2 read back; seeds torch=0, numpy=0; device cpu, dtype float32; snapshot `~/workspace/.exp086_weights/pythia-410m`; order seed 20260929, K=5.

## 5. What this does and does not claim

1. The KILL retires only the positional-order-ensembling axis **for this task class** — not test-time scaling in general, not the adaptive-loop program (§7.3).
2. An ensembling loss is a decision-accuracy comparison on one bench — not evidence about reasoning, consciousness, or capability (§7.1). It is variance change over a presentation nuisance variable, and here the variance change was negative.
3. Single bench (60 items), single model, K=5, pinned seed — no generality beyond.
4. Novelty: **N1 — Known Combination**.

## 6. Files

- Report: this file — `research/experiments/EXP114_POE_REPORT_2026-09-29.md`
- Execution script: `experiments/runs/EXP114_poe/out/exp114_execute.py`
- Raw: `experiments/runs/EXP114_poe/out/exp114_result.json` (per-item records), `exp114_worksheet.json` (order patterns, pins), `exp114_stdout.log`
- Verdict recomputed independently from the raw per-item records: b=2, c=5, p=0.9375 — matches.

No data invented. No follow-ups dispatched. Lane stops here.
