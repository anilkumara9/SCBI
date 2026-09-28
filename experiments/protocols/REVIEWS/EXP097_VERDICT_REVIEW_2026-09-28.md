# EXP097 Verdict Review — Threshold-Account Breaking Point (2026-09-28)

**Verdict: PIVOT (fragility) — NOT SUPPORTED for the directional claim. Binding.**

The threshold account predicted that once ‖δ‖ dominates ‖r‖, the per-item L11 task direction becomes causal. At ratios 1.5 and 3.0 the task direction does move decisions — but the norm-matched random direction moves *more*. The movement is nonspecific δ-driven decision noise, not task geometry. The >1 regime is fragility, not a mechanism.

## 1. Independently recomputed numbers (from `per_item_records.csv`, 300 rows — zero discrepancies on counts)

Convention: b = wrong→right (improvements), c = right→wrong (degradations) — EXP096's convention. McNemar exact, doubling. ΔM = EXP093 logit-margin paired difference (see §5 for a labeling correction).

| ratio | contrast | flips | b | c | p (exact) | ΔM (margin) |
|---|---|---|---|---|---|---|
| 1.5 | T-vs-B | 7 | 1 | 6 | 0.125 | +0.0643 |
| 1.5 | B_wrong-vs-B | 11 | 4 | 7 | 0.5488 | −0.0573 |
| 3.0 | T-vs-B | 10 | 2 | 8 | 0.109375 | +0.1103 |
| 3.0 | B_wrong-vs-B | 15 | 7 | 8 | 1.0000 | +0.2704 |

Strata (T-vs-B): 1.5 → A: 1 flip, b=1, c=0, p=1.0, ΔM=+2.236 / C: 6 flips, b=0, c=6, p=0.03125, ΔM=−2.108. 3.0 → A: 2 flips, b=1, c=1, p=1.0, ΔM=+3.039 / C: 8 flips, b=1, c=7, p=0.0703125, ΔM=−2.818.

n_correct: B=36/60 both ratios; T=31/60 (1.5), 30/60 (3.0); B_wrong=33/60 (1.5), 35/60 (3.0). Stratum balance 30/30 confirmed. Zero exclusions (0/240). Ties 0/180 per ratio (no zero margins on any injection row).

## 2. Foundation verification (each independently recomputed)

- **Step 0(i):** constructor re-hash `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361` — matches frozen pin. ✓
- **Step 0(ii):** B agreement vs archived EXP094 B vector recomputed item-by-item from `experiments/runs/EXP094_peritem_l11/out/per_item_records.csv`: **60/60** (stratum + decision), B accuracy 36/60 both. ✓
- **Step 0(iii):** degeneracy sanity: recomputed mean|cos| = 0.7922606322936264; |0.7923 − 0.7923| < 0.05. ✓
- **Δθ=0:** pre and post hash = LOG-331 pin `ec276abe…`. ✓ (run log)
- **Norm-tie:** ‖B_wrong‖ == ‖T‖ verified on all 120 (item, ratio) pairs (perturbation_ratio equality). ✓
- **Single environment (F5):** no mid-run rebuilds; 360 passes ≤ 600 cap. ✓

## 3. Decision-table walk (first match wins)

- **Step 0 — Foundation gates:** all pass, no HOLD.
- **Step 1 — Delivery:** 240/240 injection rows in band ([1.125,1.875] at 1.5 — all exactly 1.5000; [2.25,3.75] at 3.0 — all exactly 3.0000); 0 rows out of band → 0 exclusions. No HOLD.
- **Step 2 — Degeneracy:** mean|cos| = 0.7923 < 0.95 → does not fire.
- **Step 3 — Powerless test:** B_wrong flips = 11 (1.5) and 15 (3.0), both ≥ 1 → **both ratios LIVE**. Does not fire.
- **Step 4 — Threshold KILL:** requires T-vs-B < 6 at *every* LIVE ratio. T flips = 7 (1.5), 10 (3.0). **Does not fire** (weakened form moot — no non-live ratio).
- **Step 5 — Specificity PIVOT:** at LIVE ratio 1.5, T movement 7 ≥ 6 **and** B_wrong movement 11 ≥ 6 → **(a) FIRES: PIVOT (fragility)**. (Also true at 3.0: 10 ≥ 6 and 15 ≥ 6.)
- Steps 6–7 not reached (first-match-wins).

**Binding conclusion:** the threshold account is **not supported**. The >1 regime moves decisions, but nonspecifically: a random direction at matched norm flips more decisions than the task direction at both ratios (11 > 7; 15 > 10). The account's core assertion — that dominance of the residual makes the *task geometry* causal — is contradicted on its own terms. The C-first stratum at 1.5 also sits in the pre-registered near-miss band (p=0.03125 ∈ [0.01,0.05)), independently consistent with PIVOT, never CONTINUE.

## 4. Scoring-convention deviation (disclosed; verdict-robust)

The executor's mechanical readout (LOG-4415) labels as "ΔM" what is actually **accuracy-delta** (mean change in correct_top1): e.g. T(1.5) −0.0833 = (31−36)/60. The true EXP093 logit-margin ΔM recomputed above: T(1.5)=+0.0643, T(3.0)=+0.1103, B_wrong(1.5)=−0.0573, B_wrong(3.0)=+0.2704. The CSV primary is correct; only the readout's labels are wrong. **This does not change the verdict:** step 5a fires on flip counts alone; step 6 fails on p ≥ 0.01 under both conventions (and on strata under both); step 7b fails on p < 0.01 under both. The deviation is recorded here so no downstream work cites the mislabeled values.

## 5. Supporting observation (not verdict-altering)

Striking stratum asymmetry in the true margin shifts: under T, A-first margins rise (+2.24 at 1.5, +3.04 at 3.0) while C-first margins fall (−2.11, −2.82). The injection systematically boosts A-first items and hurts C-first ones — the perturbation interacts with answer phrasing, consistent with nonspecific large-nudge fragility rather than task-direction causality. This is reported as an observation; the verdict machinery needed none of it.

## 6. Binding scope

Fenced to **static per-item L11 injection at coherent tested strengths on EXP092-B** — enumerated battery: 0.01185, 0.0237, 0.0474, 0.0948, 0.1896, 0.3792 (delivery max 0.4740), 1.5, 3.0. No interpolation. Dynamic/gated mechanisms, multi-layer compositions, other layers/benches/models remain untested and are EXP097+ material. The >3.0 regime is replacement by definition, not tested strength. No EXP094/095/096 claim is altered: EXP095/096 killed the sub-license and gated rescues; EXP097 removes the threshold account as the last coherent static rescue — the static per-item family's inertness is now structural from 0.01185 through 3.0, with the >1 regime characterized as fragility, not a missed mechanism.

*Review lane: independent verdict reviewer (LOG-4416). Protocol: S6-1 v2 (LOG-4412), licensed by CEO clearance LOG-4414. Records: `experiments/runs/EXP097_threshold_breaking_point/out/`. $0 compute; no model executed; no signed artifact touched.*
