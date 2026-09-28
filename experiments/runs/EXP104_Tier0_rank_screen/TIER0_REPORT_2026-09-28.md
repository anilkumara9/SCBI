# EXP104 — Tier-0 Correct-Rank Screen Report (2026-09-28)

**Experiment:** EXP104 (minted LOG-4481). **Lane:** Tier-0 execution (CEO clearance LOG-4482, SIGNED S4-8 pre-reg v3, LOG-4480).
**Verdict: HOLD (bench sanity) → maps to Inconclusive.** Battery NOT licensed.

## What was built
- 60-item k=8 2-hop bench (10 templates × 6: landmarks, products, films, rivers, museums→city, novels, founders, events, treaties, paintings), correct-position shuffled (seed 20260928, no fixed pattern), frozen prompt template (sha256 `b4f68516…`), pinned readout = next-token position after terminal `Answer:`.
- **G1 real-tokenizer gate (EXP090 lesson):** first bench draft had **58/480 option strings multi-token** under the real pinned tokenizer — the EXP090 failure mode reproduced and caught pre-run. Bench rebuilt around G1-verified single-token pools (75 countries, 52 cities, 8 elements, 27 states screened). Final G1: **0 failures / 480**.
- Tokenizer artifact: `EleutherAI/gpt-neox-20b`; file sha256 `c24618a1b3e6a38167beff1c72cffd126c3a66254347304b50547d12c5f25624` (hub main-branch copy byte-identical to the frozen pythia-410m snapshot's bundled tokenizer, verified 2026-09-28).
- **Independent checker lane:** 64/66 VERIFIED. 2 FLAGGED, both replaced/removed before any model contact: (1) PlayStation item — SIE HQ is San Mateo, USA, so "Japan" was ambiguous → replaced with the checker-VERIFIED Corolla→Japan backup; (2) Sunflowers backup — non-unique (Amsterdam and London both hold canonical canvases) → dropped. Final bench = 59 VERIFIED primaries + 1 VERIFIED backup. Blindness attestation: no model-output artifacts existed at check time.
- **Six §4 degeneracy unit tests:** all PASS on synthetic data (tie-break, mask no-op/promote, b=c=0→p=1.0, vacuous→KILL-premise, McNemar-exact 0 mismatches vs hand recurrence on full (b,c) grid, anchors b6c0=0.03125 / b5c0=0.0625).

## The run
- Frozen Pythia-410m, CPU float32, `torch.no_grad`, eval mode. **60/60 passes in 58.7 s** (≤120 budget). Δθ=0: weight-file sha256 identical pre/post (`3e090016…be27511b`).
- Deterministic, seed-pinned; per-item records persisted (item, arm B, top-1, correct-rank, 8 logits, tie flag).

## Tier-0 numbers [OBSERVATION]
| Statistic | Value | Pre-registered bar |
|---|---|---|
| Baseline accuracy | 11/60 = **0.1833** | sanity band [0.25, 0.75] |
| Failed items | 49 | — |
| Median correct-rank (failed) | **4** | kill if > 5 |
| n_pop (failed ∧ rank ≤ 5) | **33** | underdetermined if < 12 |
| Tie-guard rate | 0/33 = **0.0** | hold if > 0.25 |

## Binding evaluation (§3 order, first match wins)
1. G1: PASS. 2. Premise: median 4 ≤ 5 — no kill. 3. Power: n_pop 33 ≥ 12 — no underdetermined. **4. Sanity: 0.1833 < 0.25 → HOLD** — bench miscalibrated (model near-chance on this word-scored 8-option bench), not a verdict on the mechanism. Maps to **Inconclusive**.

The premise/power bars themselves were satisfied (median 4, n_pop 33): had the bench been calibrated, Tier-0 would have passed. The failure is bench calibration, not the selection-failure premise. Re-running on a rebuilt bench is a **new proposal**, not a repair (pre-reg §6 risk 6).

## Battery status
**NOT licensed, NOT run.** The HOLD verdict gates it per the signed decision table.

## Lineage
- Scripts: run_tier0.py `94a3bd91…`, build_bench.py `6bfd7563…`, bench_spec.py `8514bd86…`, unit_tests.py `c1a8863c…`, g1_probe.py `5fc022af…`
- Data: bench_manifest.json `c8934b1aafa54c41`, per_item_records.json `45198fffff62037d`, tier0_worksheet.json `9a8865e25a3f168a`
- Bundle: `~/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen/`
- Log: LOG-4481
