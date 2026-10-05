# S5-Inverted Selector Pre-registration — Held-out validation of the free-energy-spread anti-calibration (DRAFT)

**Status:** DRAFT for independent Law #14 review. Born from the S7-3 verdict (LOG-4915, 2026-10-05), per the signed S7-3 plan's §5 mandate: *"a full fresh pre-registration (including a held-out validation design) required before any selection experiment."*
**No experiment number minted** (the CEO assigns numbers; this plan mints none).
**Cost:** $0. This document is planning only — zero new model forward passes. The validation run it specifies is a CPU pilot (Stage-1 precedent: 240 generations + 240 scoring passes); its execution needs its own lane authorization and will mint its experiment number then.

---

## 1. Worth-it gate

- **Exact question [HYPOTHESIS]:** Does the S5 free-energy-spread anti-calibration discovered on EXP140 Stage-1 (view-0) items replicate on held-out items, and does the median-split low-spread selector built on it actually gain accuracy?
- **Decision it changes:** KILL / CONTINUE the S5-inverted selector candidate. S7-3's CONTINUE is provisional on this validation — a KILL here overturns it for this candidate, leaving the label-free selection line on this bench family with no surviving candidate.
- **Cheapest test:** 60 held-out items × 4 branches on CPU, verbatim Stage-1 protocol (240 generations + 240 scoring forwards, $0 — Stage-1 already proved CPU feasibility). No GPU needed; no new bench engineering (held-out items are derived from the pinned discovery bench, §4).
- **Mathematical license:** Spearman rank correlation is distribution-free; the permutation tests are exact with guaranteed Type-I control; the one-sided direction (negative) is licensed by the discovery result; the selector rule is a deterministic function of label-free inputs (Law #7 — labels touch only the scoring targets, §5).
- **Quantitative prediction:** held-out Spearman(spread, mean branch correctness) ρ ≤ −0.3 with one-sided permutation p < 0.025; median-split selection gain Δ ≥ 0.10 with one-sided permutation p < 0.025.
- **Breaking point:** if the held-out |ρ| < 0.3 in the licensed direction, the candidate dies — no post-hoc rescue via the secondary, no re-tuning of the rule, no new thresholds.

## 2. Discovery recap — the licensed fact base [FACT]

- S7-3 (LOG-4915): on EXP140 Stage-1 records (60 items × 4 branches, view-0 prompts), S5 = per-item `spread` = max(F_k) − min(F_k) over the 4 branches' primary free energy (nats/token) is anti-calibrated with mean branch correctness: Spearman ρ = **−0.4899**, two-sided permutation p = **0.000060** (100k perms, seed 20261005), 95% CI **[−0.6615, −0.2695]**, n=60. |ρ| = 0.4899 exceeds the 80%-power MDE of 0.4308 — above the power floor, not an underpowered fluke.
- The other five S7-3 signals failed (S1 ρ=−0.1925 p=0.14; S4 ρ=−0.2873 p=0.026; S2/S3/S6 degenerate). S5 is the only surviving label-free candidate on this bench family.
- EXP140 G3 tested *selection by* free energy (min_F / F̄ decision rule) — null, HELD. S5 tests spread *calibration* — a different estimand (S7-3 §2, Law #14-confirmed, no double-dipping). This pre-reg does not re-test G3's decision rule.
- Bench-inversion theme [OBSERVATION]: TESTA margin anti-calibration ρ=−0.3958; S4 ρ=−0.2873; now S5 ρ=−0.4899 — this bench family inverts naive confidence heuristics. The candidate is therefore an **inverted** selector, flagged as bench-inversion evidence, not a positive capability claim.

## 3. The candidate — precise selector rule [DEFINITION]

For each held-out item i (protocol identical to Stage-1, §4):
- Generate 4 branches per `generate_rationale` (B0/B1 greedy; B2/B3 τ=0.7 sampled, seeds pinned §10); score each per `score_branch` → primary free energy F_k (mean rationale-token NLL, nats/token), answer a_k, correctness c_k = 1[a_k == t_A].
- **spread_i** = max_k(F_k) − min_k(F_k) (primary F only, not F_full — matching discovery).
- **SELECT rule (frozen):** sort the 60 held-out items by (spread_i, id) ascending; SELECT the first 30; ABSTAIN on the remaining 30. The rule uses zero label access (Law #7): spreads, the median split, and the tie-break are all label-free.
- **Claim [HYPOTHESIS]:** mean branch correctness on SELECTED items exceeds that on UNSELECTED items — i.e., preferring low-spread items is a useful label-free selection policy on this bench family.

## 4. Held-out design [FACT]

- **Discovery items:** the 60 EXP140 Stage-1 items = view-0 (V1_Anglo) surface forms of the pinned bench (`eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`).
- **Held-out items:** the same 60 logical items rendered in **view 1 (V2_Biblical)** via the committed `make_views` — fresh surface strings (Aaron/Joel/Gideon/Ruth/Abel), **zero prompt overlap** with view-0 (verified by construction, §10). Branch generations and F scores for these prompts do not exist anywhere: `generate_rationale` appears in no other run script. The (spread, correctness) pairs are unobserved; the rule and thresholds below were frozen before they exist.
- **Why view-1 (not new entities):** the index space is exhausted (all 15 triples + 15 quads used in discovery), and the model only ever sees support-vocabulary surface forms — new "entities" would collapse to the same substituted prompts. View-1 keeps the logical-item distribution identical to discovery while guaranteeing fresh prompts and fresh model outputs. [ASSUMPTION] Surface-form novelty suffices for held-outness of the (spread, correctness) estimand; a cross-domain (new-entity) replication would be stronger and is noted as future work (§7.4), not smuggled into this verdict.
- **Frozen-branch firewall:** Δθ=0 throughout (Law #6); EXP135's view-1 forward passes changed no weights, so no contamination.
- The held-out bench is pinned: `research/analysis_plans/S5-INV_HELDBENCH_2026-10-05.json`, sha256 `779202d6f8297e70319c7e18e0ccf190c70488ef5c2082501cfb727dc91d1e55` (60 items, ids `s5inv_held_00`–`s5inv_held_59`, derived 2026-10-05 by CPU-only string construction — no model contact).
- **Protocol (verbatim Stage-1, pinned §10):** branch prompts (B0 = prompt + TEMPLATE; B1 = question-swapped + TEMPLATE, involution-verified; B2/B3 = B0's prompt, sampled), R_MAX=48, S_B2=20261004, S_B3=20261005, `score_branch` teacher-forced F, t_A/t_C = tok1(view-1 A/C) — all five Biblical names verified single-token under the exact `tok1` definition (`" "+s`).

## 5. Analysis steps (frozen)

**Step 0 — Integrity aborts (any failure → INCONCLUSIVE, exit before analysis):**
0.1 Held-out bench sha256 == `779202d6…1e55`; derivation-base (discovery) bench sha == `eb304fa6…89df`.
0.2 Backbone pre-hash and post-hash == `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (Δθ=0, Law #6); model `EleutherAI/pythia-410m@9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`.
0.3 All 240 branches present; every branch F non-null or counted degenerate; every a_k ∈ {t_A, t_C}; branch prompts match the §4 recipe byte-for-byte for all 60 items.
0.4 **Degeneracy pre-check (S7-3 lesson):** spread must be able to vary *in principle* — assert std(spreads) > 0 AND median(spread) ≥ 0.05 (Stage-1 G2 bar; Stage-1 observed 1.29), else INCONCLUSIVE. Assert mean branch correctness varies across items (else ρ undefined → INCONCLUSIVE).
0.5 Missing data: >6 items (>10%) with any missing branch field → INCONCLUSIVE (mirrors S7-3's untestable rule).

**Step 1 — Signals (label-free):** spread_i per §3 for all available items. No labels touched.

**Step 2 — Targets (Law #7 firewall — labels enter only here):** per-item correctness ȳ_i = mean_k(c_k) (the discovery target, graded). The SELECT/UNSELECT partition from §3 is computed from spreads alone, before targets are touched.

**Step 3 — Tests (exact):**
- **Primary (replication):** Spearman ρ(spread, ȳ) on all available held-out items. One-sided permutation test, H1: ρ<0 (direction licensed by discovery): p = (#{perm ρ ≤ observed ρ}+1)/100001, 100,000 perms, seed **20261006**. PASS iff ρ ≤ −0.3 AND p < 0.025. Report also: two-sided p (diagnostic), 95% CI (Fisher z), and the Step-3.4-style minimum-detectable-effect report at 80% power.
- **Secondary (decision rule):** Δ = mean(ȳ | SELECTED) − mean(ȳ | UNSELECTED), SELECTED = first floor(n/2) by (spread, id). One-sided permutation test relabeling SELECTED/UNSELECTED (100k perms, seed 20261006): p = (#{perm Δ ≥ observed Δ}+1)/100001. PASS iff Δ ≥ 0.10 AND p < 0.025. Hierarchical: interpreted only for the CONTINUE sub-qualifier (§6); it cannot rescue a primary FAIL.

**Step 4 — Decision (§6).** No other reading is licensed.

## 6. Decision table (fixed before analysis)

| Primary | Secondary | Verdict |
|---|---|---|
| PASS (ρ ≤ −0.3, p < 0.025) | PASS (Δ ≥ 0.10, p < 0.025) | **CONTINUE (SELECTION-READY)** — inverted selector licensed for a selection experiment (new experiment number + its own pre-reg at that time) |
| PASS | FAIL | **CONTINUE (SIGNAL-ONLY)** — anti-calibration replicates; the median-split rule is not useful; no selection experiment licensed; further selector design needs a new pre-reg |
| FAIL (ρ > −0.3 or p ≥ 0.025) | — | **KILL** — the S5-inverted candidate is dead on held-out data; S7-3's CONTINUE is overturned for this candidate |
| any Step-0 abort | — | **INCONCLUSIVE** — instrument/run failure, not a verdict on the candidate |

KILL is worded as "no |ρ|≥0.3 anti-calibration detectable at n=60 on held-out items" — never as proof of absence. A significantly *positive* held-out ρ fails the bar identically (KILL); it is reported as a further inversion-theme data point, not re-interpreted.

## 7. Falsification self-check (pre-mortem)

1. **Winner's curse.** Discovery |ρ|=0.49 is plausibly inflated; at true |ρ|=0.30 the primary is only ~65% powered — the single most likely embarrassment is a null that reflects inflation-plus-noise, not absence. **Why the plan survives it:** the power table is pre-registered (§8), every ρ carries a 95% CI plus an MDE report, and KILL is worded as detectability-at-n=60, which the plan cannot be embarrassed by.
2. **Secondary underpowered for moderate effects** (§8: 60% power at Δ=0.20) — a secondary FAIL with primary PASS is SIGNAL-ONLY, never KILL. Stated upfront so a FAIL can't be misread as refutation.
3. **Sampling artifact.** RUN_REPORT notes τ=0.7 sampling inflates B2/B3 F *by construction* — spread may track a sampling artifact rather than model uncertainty. **Consequence pre-registered:** no mechanistic claim is licensed by any outcome; the candidate is instrumental (a label-free predictive rule) full stop.
4. **"Not fully held-out" objection.** The held-out items share logical content with discovery (new surface forms only). **Conceded:** a cross-domain replication would be stronger. It is future work, not part of this verdict — the (spread, correctness) pairs tested here are unobserved and the rule predates them, which is what held-outness means for this estimand.

## 8. Power analysis (pre-registered; n=60, one-sided α=0.025, Fisher-z)

| true \|ρ\| | 0.49 (discovery) | 0.45 | 0.40 | 0.35 | 0.30 (floor) |
|---|---|---|---|---|---|
| power | 0.98 | 0.96 | 0.89 | 0.79 | 0.65 |

80%-power MDE ≈ **0.355**. The |ρ|≥0.3 floor sits below the MDE — the design is well-powered (≥79%) for |ρ|≥0.35 and ~65% at the floor; the CI+MDE reporting (§5, Step 3) prevents misreading a null. The secondary is a large-effect usefulness gate (30-vs-30; ~60% power at Δ=0.20, ~79% at Δ=0.25 assuming per-item correctness sd≈0.35) — deliberately coarse: it licenses a selection experiment only if the selector is *clearly* useful.

## 9. Epistemological labeling (per `AGENTS.md` §5)

- [FACT]: discovery numbers (LOG-4915), bench shas, protocol code lines, power arithmetic, view-1 zero-overlap.
- [DEFINITION]: the SELECT rule (§3), spread, the decision table (§6).
- [HYPOTHESIS]: the candidate's claim — awaiting this held-out falsification.
- [CONJECTURE]: that the anti-calibration will replicate (winner's curse says discount it).
- [ASSUMPTION]: surface-form novelty suffices for held-outness (§4); CPU vehicle reproduces Stage-1 numerics.
- [OBSERVATION]: the future (ρ, p, Δ) triple — not yet existent.
- [INTERPRETATION]: the §6 readings, bound by the frozen thresholds — no post-hoc re-reading licensed.

## 10. Pins and provenance

- Discovery bench sha256: `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` (= committed EXP135/EXP140 pin).
- Held-out bench: `research/analysis_plans/S5-INV_HELDBENCH_2026-10-05.json`, sha256 `779202d6f8297e70319c7e18e0ccf190c70488ef5c2082501cfb727dc91d1e55` (60 items, view-1 V2_Biblical, derived 2026-10-05 CPU-only; derivation script `research/analysis_plans/S5-INV_build_heldbench_2026-10-05.py` — replicate-before-trust).
- Model: `EleutherAI/pythia-410m`, revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`; backbone hash `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (Δθ=0).
- Protocol pins (verbatim `run_stage1.py`): R_MAX=48, N_BRANCHES=4, S_B2=20261004, S_B3=20261005, τ=0.7, TEMPLATE=`" Reason step by step, then answer:"`, SUFFIX=`"\nAnswer:"`, greedy B0/B1, `score_branch` teacher-forced F, spread=max−min primary F.
- Analysis pins: 100,000 permutations, seed **20261006** (fresh — discovery used 20261005), numpy/scipy per executor environment (logged, not aborting).
- Compute budget (execution lane): 240 generations + 240 scoring forwards + ≤3 determinism spot-check re-runs, CPU (Stage-1 precedent); GPU only if the CEO re-licenses the vehicle.
- Belief-change statement (LOG-218): current belief [CONJECTURE] — S5's anti-calibration is a 60-item discovery result, plausibly inflated; the inverted selector is untested. After CONTINUE: [OBSERVATION]-backed — the first held-out-validated label-free signal on this bench family (instrumental reading only, §7.3). After KILL: S7-3's CONTINUE overturned for this candidate; no surviving label-free candidate on this bench family.
