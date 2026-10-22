# Independent Delta Re-verification — S6-4 Preregistration DRAFT v2 (2026-09-28)

**Verifier:** independent delta lane (fresh; did not draft v1, did not Law #14-review it at LOG-4425, did not repair it at LOG-4426).
**Target:** `research/innovation/S6-4_PREREG_DRAFT_v2_2026-09-28.md` (md5 `6ffdb61da2938565df99322bc4b92938`) vs
`research/innovation/S6-4_PREREG_DRAFT_2026-09-28.md` (v1, md5 below).
**Binding fix list:** `experiments/protocols/REVIEWS/S6-4_DRAFT_v1_LAW14_REVIEW_2026-09-28.md` §2 (F1–F9).
**Repair report:** LOG-4426 (claims: all nine fixes applied; diff touches only F1–F9 sites + three coherence edits; no bar/gate/verdict-mapping/§4.2 figure altered).
**Verdict: SIGN — the delta is verified.** Every diff hunk maps to an authorized fix; no undeclared change; no unauthorized numeric change.

## (a) Verdict

**SIGN (delta verified).** The v2 file contains exactly the nine Law #14 fixes (F1–F9) plus the declared coherence/status additions, with byte-identical v1 preserved. No bar, gate value, verdict mapping, or §4.2 power figure was altered. Next: CEO execution clearance.

## (b) v1 hash check [FACT]

```
md5sum research/innovation/S6-4_PREREG_DRAFT_2026-09-28.md
545cc691048a4319f04b83acbd124c64   ← matches the expected hash exactly; v1 untouched
```

v1 was not edited during this verification (read-only + diff only; re-verified hash after all reads — unchanged).

## (c) Hunk-by-hunk table

Full diff (`diff -u`): 8 hunks, saved for reference at `/tmp/s64_delta.diff`. Each hunk's authorizing fix:

| # | Hunk (v1→v2 lines) | Site | Authorizing fix | Substance check vs LOG-4425 prescription |
|---|---|---|---|---|
| 1 | `@@ -1,9 +1,25` | Header | **Errata-section addition + status block + licensing chain** (all declared) | Title v1→v2; append-only errata lists F1–F9 each with the review's wording, plus §6-risk-4 resolution note and the v1-preservation citation (md5 `545cc691…124c64`); status reads DRAFT v2 — UNSIGNED with "Law #14 review: ACCEPT-WITH-FIXES (LOG-4425)"; licensing chain extended through LOG-4425; header pilot paragraph updated to "independent delta re-verification of this v2 (separate lane), then CEO execution clearance" — status coherence, same content as the authorized §8 update. |
| 2 | `@@ -62,7 +78,7` | §2.1 `{d_i^(8)}` | **F5** | "any zero-norm direction → HOLD + diagnose per §3 step 1 (a broken constructor is a setup defect, not a degeneracy; never silently substituted)"; void path restricted to "mean pairwise \|cosine\| ≥ 0.95". Matches §4.1 item 6, as prescribed. |
| 3 | `@@ -83,7 +99,7` | §2.4 statistics | **F8** | "Two discovery contrasts" → "**One** discovery contrast (L8-only-vs-B; the L20 anchor is explicitly NOT a discovery contrast). The per-layer 0.005 bar holds the discovery family-wise rate at ≤0.01 (Bonferroni over the 2 swept layers — conservative, since only one layer carries a discovery contrast)." Verbatim per prescription. |
| 4 | `@@ -98,14 +114,16` | §3 steps 1, 2, 3, 5, post-step-6 caveat, 7, 8 | **F1 + F2 + F3 + F4 + F7 + F9** | Step 1 (F4): "the count-bars (≥6, ≥9) apply to the post-exclusion paired set (excluded items do not count toward any bar; §4.2 reports the realized N)". Step 2 (F7): void path "live only for {d_i^(8)}"; L20-void marked unreachable with the review's arithmetic (0.95 − 0.6639 = 0.2861 ≫ 0.05); "L8-void → step 6 is unavailable; the anchor (step 4) still validates the setup, and the sweep routes to PIVOT (step 8b, incomplete sweep) — the KILL is downgraded as stated". Step 3 (F2): "First check the anchor count: if L20-only flips ≠ 6 → HOLD (the frozen pipeline changed; step 4's set-equality check then runs inside the diagnosis lane)"; FROZEN → Underdetermined requires "(W20 = 0) AND (W8 = 0) AND (L8-only = 0) with the anchor count verified = 6". Step 5 (F1+F9): first-match-wins over (a) matched-control fragility "(L8-only ≥ 6 AND W8 ≥ 6) → PIVOT (fragility — nonspecific δ-driven movement at L8)" and (b) control-outmoves-task "(L8-only < 6 AND (W8 ≥ 6 OR W20 ≥ 6)) → PIVOT (fragility — control-outmoves-task / fragile regime, naming the layer)"; unmatched W20 ≥ 6-alone clause removed from step 5, handled by the binding post-step-6 caveat: "step 6's conjunct is evaluated first — if it holds → CONTINUE with a named 'L20 fragile-regime caveat' (W20 ≥ 6 — the L20 layer is in the fragility regime; the anchor's sub-bar status is uninterpretable as mechanism evidence); if step 6's conjunct fails and W20 ≥ 6 → PIVOT (fragility), naming L20". F1/F9 coherence explicit: "F9's step-5b covers L8-only < 6; F1's post-step-6 caveat covers L8-only ≥ 6-but-sub-bar". Step 7 (F3+F9): KILL requires "Regime LIVE with L8-liveness — (W8 ≥ 1) OR (L8-only ≥ 1)"; "controls sub-threshold"; "Global-LIVE via W20 only (W8 = 0 AND L8-only = 0) → not a KILL; routes to step 8(d)". Step 8 (F3): new sub-case (d) "incomplete sweep — L8-regime unproven-live (global liveness via W20 only: W8 = 0 and L8-only = 0 — the sweep KILL is not licensed at a layer whose perturbations demonstrably reach no decision)". |
| 5 | `@@ -129,7 +147,7` | §4.1 item 4(b) | **Declared §4.1-item-4(b) coherence parenthetical** | "step-7 KILL fires (only where step 7's L8-liveness condition holds — a W20-only unlocked regime routes to step 8(d), not KILL)". Declared by the repair lane; pure coherence, no number changed. |
| 6 | `@@ -138,13 +156,13` | §4.2 (three lines) | **F8 (§4.2) + F4 (§4.2) + F6 (§4.2)** | Bonferroni line: "1 discovery contrast … at family-wise 0.01 → per-contrast 0.005 — Bonferroni is computed over the 2 swept layers (conservative, since only one layer carries a discovery contrast)" (F8). Sensitivity floor line: "Post-exclusion N: the count-bars (≥6, ≥9) apply to the post-exclusion paired set (§3 step 1) — the verdict lane recomputes and reports the realized N and the sensitivity floor (9/N_realized; e.g. 9/58 ≈ 0.155)" (F4). Pricing line: "660 recorded rows (the '724 passes' executor narration double-counts T(1.0) — EXP095 verdict review)" (F6). |
| 7 | `@@ -178,7 +196,7` | §6 risk 4 | **Declared §6-risk-4 update** | "tripwire question now resolved (F5, LOG-4425)"; confirmed routing — any zero-norm direction → HOLD + diagnose per §3 step 1; §3-step-2 void path covers only the ≥0.95 mean-|cosine| case (§4.1 item 6). Declared by the repair lane. |
| 8 | `@@ -198,8 +216,8` | §8 + closing line | **Declared §8 next-steps update + status block** | "Independent delta re-verification of this v2 against the F1–F9 fix list (separate lane, fresh to the repair) → CEO execution clearance … Law #14's v1 review (LOG-4425, ACCEPT-WITH-FIXES) is satisfied by the append-only errata at the top; no re-review of the design is needed. Pilot NOT authorized until all complete." Closing line: "Draft v2 prepared 2026-09-28 by the S6-4 pre-registration repair lane (fresh lane — did not draft v1, did not review it). DRAFT, UNSIGNED — Law #14 review: ACCEPT-WITH-FIXES (LOG-4425)…". Declared by the repair lane. |

**Undeclared changes: none.** All 8 hunks map to the authorized set {F1..F9, §6-risk-4 update, §8 next-steps update, §4.1-item-4(b) coherence parenthetical, errata/status/licensing-chain additions}. The repair lane's three declared coherence edits (hunks 5, 7, 8) are all present and declared; no fourth coherence edit exists.

**Substance notes (F1/F9 interplay, checked explicitly):** F9's step-5b covers L8-only < 6; F1's post-step-6 caveat covers L8-only ≥ 6-but-sub-bar with W20 ≥ 6 — both kept, first-match-wins, as the review requires. Step 5's matched disjunct keeps its PIVOT (fragility) mapping; step 7's KILL prose ("inertness generalizes…") is now unreachable in control-outmoves worlds (claimed by step 5b) and in W20-only-live worlds (routed to 8d) — the review's honesty condition is satisfied structurally. Verdict mappings unchanged: HOLD / Underdetermined / PIVOT / CONTINUE / Refuted each fire exactly as prescribed; no new verdict or mapping was introduced.

## (d) Numeric-invariance scan [FACT]

Compared the sorted unique numeric-token sets of v1 and v2. **Every decision value is unchanged:** 0.38 (ratio), [0.285, 0.475] (bands), 0.005 (per-layer α), 0.01 (family-wise), DELTA_BAR = 0.10, ≥6 / ≥9 bars, 0.95 (degeneracy gate), 300/360/500 (budget), 60 items, 36/60 B-agreement, constructor 0.6639 ± 0.05, 0.7923 L11 precedent, all McNemar figures (0.03125, 1.73×10⁻¹⁸, 0.0078125, 0.00390625), all §4.2 power figures (0.142, 0.823, 0.023, 0.415, 0.0091, 0.9909, [0.0376, 0.2051], θ≈0.15, 575 passes), 0.3792, 0.125, 0.109375, R_SEED=94094, 120 norm-tie assertions.

**Authorized new/altered numerics (each inside an F1–F9 prescription):**
- F4: `9/58 ≈ 0.155` example (the review's own example text).
- F6: `724 passes` → `660 recorded rows` (the "724" string remains only inside the quoted executor-narration phrase, as prescribed).
- F7: `0.2861` (0.95 − 0.6639 = 0.2861 ≫ 0.05 — the review's own arithmetic).
- F8: "Two" → "One"/"1" discovery contrast — wording, not a bar: per-contrast α = 0.005 and family-wise 0.01 both unchanged.
- Status/chain: LOG-4425 added to the licensing chain; the v1 md5 quoted in the errata.

**Result: no unauthorized numeric change.** No bar, gate value, verdict mapping, or §4.2 power figure was altered.

---

*Verification completed 2026-09-28 by the independent delta lane. Neither v1 nor v2 was edited. Next: CEO execution clearance per §8. No pilot authorized until then.*
