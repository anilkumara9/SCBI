# EXP105 — Intervention Battery Report (cloze format) — 2026-09-28

**LOG-4491. Verdict (binding, pre-registered decision table v3 §3, first-match order): KILL (nonspecific), step 9.**
*Maps to: Refuted (the autonomous target-free selection-repair claim is not supported on this bench).*

## What was run

The S4-8′ battery arms (S4-8 v3 §2.3, carried over verbatim into S4-8′ v2, SIGNED at LOG-4488), applied as logit-level operators to the recorded Tier-0 8-candidate logit vectors. Masking sets one candidate's logit to −1e9 before argmax (ascending-token-id tie-break on float32 exact ties — 0/60 tie events). **No model contact was made in the battery; Δθ=0 by construction.** $0 CPU.

- **B:** none (Tier-0 baseline decisions, recomputed from logits — 60/60 match the recorded top-1, sanity check PASS).
- **T:** mask baseline top-1 token, re-argmax over 7.
- **F:** mask the structural foil's token (transferred MC-bench designation, blinded at build time), re-argmax.
- **R:** mask a uniformly random candidate among the k−2 excluding baseline top-1 AND correct; seed pinned at **20260928** before any battery computation.

**Primary population:** Tier-0 population = 28 failed items ∩ correct-rank ≤ 5 → **n_pop = 21**. Full-bench (60) secondary.

## Results (primary, Tier-0 population)

| Arm | ΔM (vs B) | Rescues (of 21) |
|---|---|---|
| T | **+0.2381** | 5 |
| F | +0.1429 | 3 |
| R | 0.0000 | 0 |

| Contrast | b | c | McNemar-exact p | Tango 95% CI |
|---|---|---|---|---|
| **T-vs-R (PRIMARY, binding, α=0.05)** | 5 | 0 | **0.0625** | (0.047, 0.451) |
| T-vs-B | 5 | 0 | 0.0625 | (0.047, 0.451) |
| F-vs-B | 3 | 0 | 0.25 | (−0.034, 0.346) |
| R-vs-B | 0 | 0 | 1.0 | (−0.155, 0.155) |
| T-vs-F | 2 | 0 | 0.5 | (−0.074, 0.289) |

**Foil–top-1 overlap O = 12/21 = 0.571 > 0.5** → the F arm is non-diagnostic per the pre-registered overlap stratum (it duplicates the T arm on a majority of Tier-0-pop items); F results are descriptive only.

## Decision-table walk (binding order)

1. G1: PASS (carried from Tier-0, 480/480). 2. Premise: median rank 4.0 ≤ 5, pass. 3. Power: n_pop=21 ≥ 12, pass (feasibility recorded: b=6,c=0 → p=0.03125 reachable; max ΔM=1.0 ≥ DELTA_BAR). 4. Sanity: baseline 0.5333 ∈ [0.25,0.75], pass. 5. Tie-guard: 0.0 ≤ 0.25, pass.
6. PIVOT-diagnostic: ΔM_T > 0 → condition False. 7. CONTINUE: ΔM_T=0.2381 > 0.10 ✓, |ΔM_R|=0 < 0.05 ✓, **T-vs-R p=0.0625 ≥ 0.05 ✗ → False**. 8. PIVOT-foil: F-vs-B p=0.25 ≥ 0.0125, O > 0.5 → False. **9. KILL (nonspecific): ΔM_T > 0 ✓ and T-vs-R p ≥ 0.05 ✓ → FIRES.**

## Reading (observation vs interpretation)

- [OBSERVATION] Top-1 masking rescued 5/21 Tier-0-pop items (+0.2381); random masking rescued 0/21. The observed direction is specific, not generic.
- [OBSERVATION] At n_pop=21 the binding test cannot certify that direction: McNemar-exact needs 6 unidirectional flips for p<0.05; the battery produced 5. The margin is exactly one rescue.
- [INTERPRETATION] The pre-registered routing is mechanical and was followed: step 9 fires, verdict KILL (nonspecific) — "random masking matches — generic perturbation, not selection repair" is the table's wording, but on the observed numbers the more precise statement is: **the rescue direction is clean (R perfectly flat) while the binding significance bar was missed by one flip.** The verdict is Refuted; it is not evidence that masking is generic — it is evidence the licensed test could not certify specificity at n_pop=21.
- [FACT] No re-run, no larger-population variant, and no third readout may be commissioned from this outcome — the verdict discipline (v3 §3, "exactly one step is earned") and the S4-8′ LINE-CLOSED stop rule close the I2′ battery line on this bench.

## Artifacts

- `battery_worksheet_exp105.json` — bars, contrasts, CIs, decision walk, feasibility.
- `per_item_records_battery.json` / `.csv` — 240 arm decisions (60 × B/T/F/R) with masked indices.
- `run_battery_exp105.py` — the battery executor (deterministic; R seed pinned).
- Lineage: Tier-0 bundle `../EXP105_cloze_Tier0/` (per_item_records.json, cloze_bench_manifest.json); pre-reg `research/innovation/S4-8_PRIME_PREREG_DRAFT_v2_2026-09-28.md` (LOG-4488 SIGN); decision table from `S4-8_PREREG_DRAFT_v3_2026-09-28.md` (LOG-4480 SIGN).
