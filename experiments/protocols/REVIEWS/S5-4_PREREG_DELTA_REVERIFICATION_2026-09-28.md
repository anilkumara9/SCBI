# Law #14 Delta Re-verification — S5-4 Pre-registration DRAFT v2 (LOG-4403)

*Reviewer: Independent Scientific Mentor & Adversarial Reviewer (standing role; binding authority). FRESH — did not write the v1 draft, the v1 review, or the v2 repair. Read-only: no draft text altered, $0 compute, no model executed, no weights touched.*
*Date: 2026-09-28.*
*Verdict: **SIGN** (binding). Zero defects in delta scope — no third repair lane needed.*

---

## 1. Scope

Law #14's binding review (LOG-4402) returned ACCEPT-WITH-FIXES (F1–F3) on the S5-4 pre-reg v1 draft (LOG-4401). The repair lane applied all three in `research/innovation/S5-4_PREREG_DRAFT_v2_2026-09-28.md` (LOG-4403). The review flagged F2 as needing substantive re-verification; F1/F3 as verifiable by inspection. This report verifies all three independently, plus diff integrity.

Inputs read: v2 draft (full), v1 draft (full), binding v1 review (full), repo `AGENTS.md` house rules.

## 2. F2 — substantive re-verification: the symmetric over-coverage rule

**The rule as written (v2 §2.4):** "if realized max|shift(8.0)| < 0.5 × τ_8 = 0.45, the reach overshot — the step-3 KILL verdict must then carry the 'low-margin-items form' fence inline (the strict-reach form softens to 'even at maximum leverage on low-margin items, nothing moved'), with the realized reach reported."

**Arithmetic recomputed from frozen primaries (trusted nothing from the repair lane):**
- τ_8 = 2 × max|shift(α=4.0)| = 2 × 0.4488 = 0.8976 ≈ 0.90 ✓ (matches the v1 review's archive-verified value).
- 0.5 × 0.90 = **0.45** ✓ exact.
- 1.25 × 0.90 = **1.125** ✓ exact (under-coverage tripwire, unchanged).

**Mirror-symmetry check:** the rule structurally mirrors the under-coverage tripwire (threshold + pre-registered consequence + reporting requirement). The multiplier asymmetry (1.25 vs 0.5) is principled, not a gap: under-coverage is the KILL-invalidating direction (the gate may have missed flippable items — the "rescue's best shot" premise is at risk), while over-coverage is KILL-safe (the gate was generous — the KILL stands, only its phrasing softens from strict-reach form to low-margin-items form). No sharpness weasel-wording: the threshold (0.45), the trigger (realized max|shift(8.0)|), and the consequence (fenced KILL language with the softened form quoted verbatim) are all exact.

**Routing into §3:** the rule does not change which step fires — it amends the step-3 KILL's reported form. Unambiguous: the executor computes realized max|shift(8.0)|, compares to 0.45, and if below, the verdict report carries the fenced form inline. The softened wording is quoted verbatim, so a verdict lane cannot improvise it.

**HELD.** F2 is correctly applied, arithmetically sound, and unambiguous in routing.

## 3. F1 — inspection: the joint requirement

Two restatements, both verified against the binding §3 table:

- **§2.1.1 flatness bullet:** "step-4 PIVOT (fragility) fires only on gated T(8.0) movement ≥ 6 **and** gated B_wrong movement ≥ 6 — if T < 6 while B_wrong moves, step-3 KILL fires first (first-match-wins), and B_wrong movement on fragile items strengthens that KILL." ✓ Matches §3 step 4 ("Gated T(8.0) movement ≥ 6 AND: (a) gated B_wrong moves ≥ 6") and the first-match-wins order (step 3 precedes step 4).
- **§6 item 3:** "step-4 PIVOT (fragility) requires gated T(8.0) movement ≥ 6 **and** B_wrong ≥ 6 jointly — B_wrong ≥ 6 with T < 6 fires step-3 KILL (first-match-wins) and strengthens it." ✓ No drift between the two restatements or the table.
- The §0 summary line "PIVOT (fragility) if the gated B_wrong arm moves with T" reads jointly ("moves with T") and does not contradict the table; the binding table governs. No drift.

**HELD.** F1 is correctly applied in both locations.

## 4. F3 — inspection: the "conditionally" qualifier

Grep of v2 for "family" (5 hits): errata line (quotes the old text being replaced), §0 (now "the program's first mechanism family closed, conditionally — within the linear license up to ratio 0.38"), §0 belief line (no closure claim), §3 step 3 ("the static per-item family is closed conditionally too"). Grep for "fully closed": appears only inside the errata's quoted old-text — no surviving unqualified occurrence.

**HELD.** F3 is correctly applied everywhere it is needed.

## 5. Diff integrity

The v1↔v2 diff (34 lines total) contains exactly: the title bump, the dated append-only errata block, and the four intended text changes (F1 in §2.1.1 + §6 item 3; F2 in §2.4; F3 in §0). The reach lemma (§0.1), the α=8.0/τ_8=0.90/|G|=21 design, the frozen Appendix A member list, the KILL-only structure with its counterfactual, the 162/400 budget, and all guards are byte-untouched. v1 is preserved unedited.

## 6. Non-blocking observation (not a defect)

§5 instrumentation item 4's parenthetical names only the 1.125 under-coverage tripwire; the over-coverage rule (0.45) is pre-registered in §2.4 and the realized max|shift(8.0)| value it needs is logged by the same item, so the check is fully computable by the verdict lane. A future errata could name both tripwires in item 4 for tidiness; it does not affect licensability or routing.

## 7. Verdict

**SIGN (binding).** All three fixes verified — F2 arithmetically and structurally sound, F1/F3 textually exact against the binding decision table. Zero defects in delta scope. The S5-4 pre-registration v2 draft is authorized for **CEO execution clearance**. The pilot remains unauthorized until the CEO clears it; the draft is still UNSIGNED (signing/minting the experiment number is the CEO's act).

*Report: `experiments/protocols/REVIEWS/S5-4_PREREG_DELTA_REVERIFICATION_2026-09-28.md`. Logged as LOG-4404.*
