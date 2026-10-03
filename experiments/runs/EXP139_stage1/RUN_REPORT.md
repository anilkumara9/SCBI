# EXP139 Stage-1 Run Report (κ̂ contraction screen)

**Pre-reg:** `research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4885). CEO venue approval: Stage-1 CPU only.

## Validity gates
- (a) bench sha256: `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` — PASS
- (b) backbone pre-hash: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — PASS
- (c) baseline yhat fidelity: 20/20 — PASS

## Results
- κ̂ (max of 20 local + 190 cross ratios): **0.955971**
- median: 0.734152, IQR: [0.685572, 0.783381]
- local ratios range: [0.334814, 0.955971]
- cross ratios range: [0.570595, 0.932439]
- forwards: 60 (budget 60)

## Bar comparison (pre-reg §3, §6 — quoted, not decided)
- κ̂ < 1 → contraction license SURVIVES → Stage-2 gate opens (needs CEO venue approval + founder GPU)
- κ̂ ≥ 1 → contraction license LOST → Stage 2 does NOT run → Stage-1b (venue per §4 pilot rule; NOT approved in this lane)
