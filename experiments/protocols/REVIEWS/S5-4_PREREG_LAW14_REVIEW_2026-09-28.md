# Law #14 Adversarial Review — S5-4 Pre-registration DRAFT (LOG-4401)

*Reviewer: Independent Scientific Mentor & Adversarial Reviewer (standing role; binding authority; did not write the draft). Read-only review: no draft text altered, $0 compute, no model executed, no weights touched.*
*Verdict: **ACCEPT-WITH-FIXES** (binding). No fatal defect → not REJECT. Three binding fixes below (F1–F3); none touch the design's feasibility.*

---

## 1. What I attacked (in order)

### 1.1 The reach lemma — HELD (verified, not trusted)

The draft's forcing claim: the backlog's letter (gated injection at α=1.0) is infeasible by construction, forcing α=8.0. I recomputed everything from the frozen primaries:

| Claim (draft) | My recomputation | Result |
|---|---|---|
| EXP094 max\|shift\| at α=1.0 = 0.090155 | 0.090155 from `per_item_records.csv` (T arm) | ✓ exact |
| \|G₁\| = 1 (`exp092_planetary_3hop_7`) | 1, that item | ✓ exact |
| Strict per-item gate empty | 0 items satisfy sign(s_i)=−sign(m_B) ∧ \|s_i\|≥\|m_B\| | ✓ proven |
| max\|shift\|/α ∈ {0.0933, 0.0922, 0.0902, 0.0973, 0.1122} | {0.0933, 0.0922, 0.0902, 0.0973, 0.1122} | ✓ exact |
| max\|shift(4.0)\| = 0.4488 → τ_8 = 0.8976 ≈ 0.90 | 0.4488; 2×0.4488 = 0.8976 | ✓ exact |
| \|G\| = 21; Appendix A matches member-for-member | 21; sorted recomputation == Appendix A list | ✓ exact |
| 5 wrong / 16 right; 13 A-first / 8 C-first | 5 / 16; 13 / 8 | ✓ exact |
| Appendix A margins transcribe the archive | 5/5 spot checks (incl. ± signs) | ✓ exact |
| Archive SHA-256 pin `9ada6ef9…b366d149` | `sha256sum` matches | ✓ exact |
| Gate cleanliness | max in-gate \|m_B\| = 0.8904 < 0.90; min excluded = 1.0442 | ✓ no boundary ambiguity |

**Ruling:** the α=1.0→8.0 move is genuinely forced, not scope creep. The backlog's literal design (|G₁|=1 < 6 = minimum significant table) is infeasible by construction — the EXP079 lesson working as intended. The concept (inject only within-reach items, gate from archived margins) is preserved; the draft deviates from the backlog's *letter* while honoring its *license*, and documents the deviation as forced. The single-α, conditionality-first framing keeps it out of EXP095's barred "further strength experiments" territory.

### 1.2 The τ extrapolation — ACCEPTABLE with F2

2× from the nearest measured anchor (α=4.0, ratio 0.1122 — the most local of the five anchors). The extrapolation direction is generous to the rescue (wider gate = the rescue's best shot), which is the correct asymmetry for a falsification instrument. The mild upward drift in the ratios (0.0902→0.1122) is a linearity flag the draft discloses, and the in-run under-coverage tripwire (1.125 = 1.25×τ_8) is sharp and pre-registered. **Gap:** no pre-registered rule for substantial *over*-coverage (realized reach ≪ τ_8), which would soften the KILL from strict-reach form to low-margin form. → **F2**.

### 1.3 No CONTINUE branch — LICENSABLE (the honest core holds)

- b_max = 5 (exactly 5 gated items wrong at baseline — verified) → min McNemar-exact (doubling) p = 2·2⁻⁵ = **0.0625** > 0.05. Recomputed, not trusted. The directional positive is unreachable by construction. ✓
- The infeasibility is proven from frozen archives, not chosen for convenience; the counterfactual CONTINUE (standard bars, had b_max ≥ 6) is stated, so the bars cannot be accused of being rigged. Genuine, not theater. ✓
- The statistic choice is not hiding a feasible positive: flips are the program's decision currency, and a margin-shift-based positive would contradict the program's own LOG-4391 breaking point ("margin shifts without flips"). ✓
- A KILL-only design is licensable in a falsification-first program: the existential rescue claim ("there exists a headroom regime where the direction works") IS falsifiable at its best shot, and the KILL (closing the last static variant — the program's first fully closed mechanism family, conditionally) is the valuable product. The step-5 suggestive PIVOT (2–5 flips, all wrong→right, B_wrong flat) preserves the upside honestly — even a perfect 5-0 table is reported as signal-motivating-follow-up rather than buried.
- The declined α=16 variant (k=35, 9 wrong → min p = 2·2⁻⁹ = 0.0039, positive feasible — verified) is correctly declined *as the first step*: at ratio 0.76 the B_wrong-fragility PIVOT is the likely outcome (no closure), while α=8.0 can deliver a clean KILL. Correct sequencing; α=16 preserved as conditional follow-up. The decline is not an evasion of a feasible positive — it is the less informative experiment first.

### 1.4 B_wrong fragility PIVOT — risk framing BROKE in part (→ F1), design HELD

§6 item 3 states that B_wrong flipping ≥6/21 "→ step-4 PIVOT, which closes nothing." Under the binding decision table this is wrong: step 4 requires **gated T movement ≥ 6 AND** B_wrong ≥ 6. If T < 6 while B_wrong moves, **step 3 fires first** (first-match-wins) → KILL — and B_wrong movement on fragile items *strengthens* that KILL (the items are flippable by large nudges, yet the task direction specifically doesn't move them). The table is correctly ordered; the risk section misstates it. The worth-it gate passes: the likely outcome (KILL on a flat T) is the valuable one, and no B_wrong behavior can poison it. → **F1** (documentation fix; the design needs no change).

### 1.5 Own hunt

- **Feasibility algebra:** b=21,c=0 → p ≈ 9.5×10⁻⁷ ✓ (2/2097152); budget 102+60=162 ≤ 400 hard cap ✓; delivery band [0.2844, 0.4740] = 0.3792×[0.75,1.25] ✓; tie gate ties/42 > 5% sharp ✓; step-1 ≤2-rows-excluded rule reasonable ✓.
- **Degeneracy analysis:** gate on degenerate archives (τ_8=0 → G empty) → feasibility check fails → no verdict, never a positive ✓; the gate only selects rows, cannot manufacture flips ✓; McNemar/ΔM fail safe ✓; suggestive branch cannot fire on 0–1 flips (falls to step 6, correctly) ✓; zero-norm d_i → step-1 HOLD before any division ✓.
- **In-run tripwire:** under-coverage rule sharp (threshold + disclosed consequence + non-decision diagnostic specified) ✓; over-coverage side missing → F2.
- **Scope fences:** step-3 KILL language fenced to "the licensed reach-calibrated set at α=8.0" ✓; "falsified within the linear license up to ratio 0.38" consistent with the 0.3792 target ✓; >0.4740 regime, non-static conditional mechanisms, other benches/models/layers all fenced to EXP096+ ✓. Language precision: §0's parenthetical "(the program's first mechanism family fully closed)" drops the "conditionally" qualifier the binding step-3 language carries → **F3**.
- **Counterfactual CONTINUE:** genuine constraint on goalpost-moving, not theater ✓.
- **Law #9:** T-vs-B_wrong labeled diagnostic-only in §2.4 ✓ (S5-1 v2 F13 precedent honored).
- **Stratum relaxation** (heterogeneity veto instead of strict all-strata consistency): disclosed (§0.1 Gap 3, §5); acceptable — the KILL doesn't depend on strata, and step 5 licenses nothing, so the follow-up design (not this one) carries the stratum bars.
- **60 B passes:** justified as the determinism self-check + replication anchor (F2 precedent from S5-1) ✓.
- **Sign-corrected variant** (§6 item 8): correctly killed by the reach lemma (empty strict gate) — no need to re-derive ✓.
- **Licensing citations:** LOG-4391 S5-4 packet and LOG-4400 successor-lane wording verified against the log — the draft cites both accurately ✓.

---

## 2. Binding fix list

- **F1 (§6 item 3 — re-verify by inspection):** restate the fragility-PIVOT risk with the joint requirement: step 4 fires only on gated T movement ≥ 6 **and** B_wrong ≥ 6. State explicitly that B_wrong ≥ 6 with T < 6 fires step-3 KILL (first-match-wins) and strengthens it. The current text contradicts the binding table.
- **F2 (§2.4 — re-verify):** add the symmetric over-coverage rule: if realized max\|shift(8.0)\| < 0.5×τ_8 (= 0.45), the step-3 KILL verdict must carry the "low-margin-items form" fence inline (strict-reach form softened), with the realized reach reported. The under-coverage tripwire (>1.125) is the model.
- **F3 (§0 — inspection):** keep the "conditionally" qualifier attached to every "family closed" claim — change "(the program's first mechanism family fully closed)" to "(the program's first mechanism family closed, conditionally — within the linear license up to ratio 0.38)". The binding step-3 language already carries it; the §0 parenthetical must not outrun it.

No fix touches the design's feasibility, the gate, the bars, or the budget. F2 is a new pre-registered rule → needs delta re-verification; F1/F3 are language fixes verifiable by inspection.

---

## 3. Verdict

**ACCEPT-WITH-FIXES.** The reach lemma is verified proof, not framing; the redesign is forced; the KILL-only asymmetry is honest and licensable; the decision table is correctly ordered; the worth-it gate passes. Apply F1–F3 in a new draft version (append-only errata, v1 preserved) → delta re-verification of F2 → SIGN → CEO execution clearance.

*Report: `experiments/protocols/REVIEWS/S5-4_PREREG_LAW14_REVIEW_2026-09-28.md`. Logged as LOG-4402.*
