# H12 (HDI-FLIP) — Kill Recommendation (LOG-4613, 2026-09-29)

**Lane:** worth-it-gate + pre-registration drafting lane, LOG-4613 pre-assigned. $0 CPU.
**Recommendation: KILL the H12 experiment proposal. Do not draft a pre-registration. Do not mint an experiment number.**

## The proposal

H12 would test whether EXP112's descriptive flipped-vs-original fidelity asymmetry (flipped 24/30 vs original 17/30) is a real effect, reusing H6's zero-generation logit-readout apparatus on the EXP107 decorrelated bench.

## Stage 1 — worth-it gate (the six elements)

1. **Exact question:** Does the honesty logit-readout's fidelity concentrate in the flipped-word cells (24/30 vs 17/30)?
2. **Decision changed:** CONTINUE → stratify future honesty designs by word-family; KILL → the observation is noise.
3. **Cheapest test:** Fisher's exact two-sided on the archived 2×2 table `[[24,6],[17,13]]` — one Python call, $0 CPU, read-only on archived data.
4. **Mathematical license:** exact hypergeometric null; no asymptotic approximation. The EXP112 apparatus is deterministic (greedy, zero generation, fixed prompts) — the per-item decisions are already fixed and archived, so this test is decisive and final: no new measurement on this bench can change the table.
5. **Quantitative prediction (computed at gating):** OR = 3.06, **two-sided p = 0.0946** > 0.05 → the test KILLS the question.
6. **Breaking point:** the test fails to reject at α=0.05. A new experiment number adds nothing — the numbers are fixed.

## Why the gate FAILS (three independent grounds)

**G1 — The test is already decisive, and it says noise.** Two-sided Fisher's exact p = 0.0946. The per-15-cell splits are weaker still (A-first 12/15 vs 8/15: p = 0.2451; C-first 12/15 vs 9/15: p = 0.4270). The one-sided p = 0.0473 is explicitly declined: the direction was selected *after* seeing the observation, and using it would be post-hoc direction selection barred by Law #4/Law #9. The pre-registered question would have to be two-sided, and the two-sided answer is noise.

**G2 — No cross-experiment consistency.** EXP111's trained-head readout on the same bench shows acc(flipped=True) = 12/15 vs acc(flipped=False) = 12/15, G = 0.0000 — exactly zero asymmetry. The EXP112 cell difference appears only in the logit-readout apparatus, on fixed data, at p = 0.0946. There is no second signal to corroborate.

**G3 — A new experiment number would be theater.** EXP112's decisions are deterministic and archived (`exp112_per_item.json`). Re-running H6's apparatus reproduces the identical table. H12 as an experiment would pre-register bars against data that already exist and are already known — a Law #9 violation in spirit (metrics registered after output inspection). The honest object is not a new experiment but this gate analysis itself.

## What this kills and does not kill

- **KILLS:** the H12 experiment proposal and the flipped-cell concentration question on this bench. No experiment number is minted. No pre-registration is drafted.
- **Does NOT kill:** EXP112's HELD (41/60) stands unchanged; the 24/30 vs 17/30 split remains a registered descriptive [OBSERVATION] in EXP112's report §9 (p = 0.0946 two-sided, now recorded here as a post-hoc exact test — descriptive only, no verdict).
- **Does NOT license:** any stratified-by-word-family design, any re-read, any "larger-N" rescue of the cell question.

## Residual note

If a future bench (new items, new ids) ever exists, a flipped-vs-original moderation hypothesis could be pre-registered there with a two-sided Fisher bar — that would be a new hypothesis on new data, not H12. Nothing in the current program licenses building such a bench for this question alone.
