# EXP148 Step-0 Dry-Run Report — 2026-10-06

**Outcome: DRYRUN_PASS** — the first-token scoring repair holds. Full EXP148 run is licensable (pending CEO execution authorization as a separate lane; NOT executed here).

## Gate result

| Check | Result |
|---|---|
| B first-token accuracy | **14/20 = 0.7000** |
| Calibration band | [0.2, 0.8] |
| Guard (d) | **PASS** |

The repaired baseline sits comfortably inside the measurable band — close to the n=180 descriptive estimate (0.6611), confirming transfer to fresh 20-item subsets.

## Guards (all PASS)

| Guard | Check | Result |
|---|---|---|
| (u0) | Scoring-pipeline unit test (9 synthetic cases, 0 forwards) | PASS |
| (b) | Model revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` | match |
| (a) | Δθ=0 pre/post state-dict hash `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` | match/match |
| (h) | Throughput 7.46 tok/s → 46k projected 1.71h (cap 72h) | feasible |
| (c) | Bench pin `2b055b53127a241b72338a82373c3efc7b666256e25d8c584d45989278c14dcf` | 64/64 |
| Law #7 | Exemplar/bench entity disjointness | PASS |

## Execution record

- **Subset seed:** 148000 (registered at execution; ≠ bench-construction seed 7101)
- **Torch seed:** 148001; greedy decoding
- **Items:** 20 fresh (S71-165, S71-085, S71-090, S71-170, S71-083, S71-020, S71-163, S71-069, S71-161, S71-140, S71-019, S71-022, S71-082, S71-077, S71-094, S71-157, S71-016, S71-178, S71-127, S71-025)
- **Arm:** B only, 2-shot direct-answer, T_B=15
- **Forwards:** 300 generation + 50 probe = ~350 total; $0 CPU
- **Wall time:** 67.9s for the 20 generations
- **Environment (re-recorded):** torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, 2 threads, eager attention, fp32 CPU
- **Exemplars:** reused EXP147's `S7-1_PROMPTS_2026-10-05.json` byte-identical (sha256 `e46211620ffaa496…`)

## Per-stratum accuracy (descriptive, n=20 — not a guard)

| Stratum | n | Correct |
|---|---|---|
| compositional-2hop | 2 | 2 |
| compositional-3hop | 7 | 7 |
| transitive-2hop | 5 | 0 |
| transitive-3hop | 6 | 5 |

See `exp148_dryrun_per_item.jsonl` for per-item generations, first tokens, and correctness.

## Consequence

Per the binding dry-run gate (§5.4): **PASS → full EXP148 run licensable.** Execution of the full run (n=180 × 3 arms, ≈46k forwards) requires CEO execution authorization as a separate lane. This lane ran nothing beyond Step 0.

*Run directory: `experiments/runs/EXP148/`. Machine-readable summary: `exp148_step0_dryrun_2026-10-06.json`. Log: `exp148_step0_dryrun_2026-10-06.log`.*
