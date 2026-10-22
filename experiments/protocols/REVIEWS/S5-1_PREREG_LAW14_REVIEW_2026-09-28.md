# Law #14 Adversarial Review — S5-1 Pre-registration DRAFT (LOG-4394)

*Reviewer: Independent Scientific Mentor & Adversarial Reviewer (standing role; reports to the founder; binding verdict authority).*
*Target: `research/innovation/S5-1_PREREG_DRAFT_2026-09-28.md` — DRAFT, UNSIGNED. Read-only review; no edit made to the draft.*
*Review date: 2026-09-28. Verdict: **ACCEPT-WITH-FIXES** (binding).*
*Licensing chain checked: LOG-4373–4377 (EXP094 Refuted/KILL) → LOG-4390 (gap review) → LOG-4391 (S5-1 PROPOSAL, Law-#15 packet) → LOG-4394 (this draft). All LOG numbers exist in `reports/research_log.md`.*

## Verdict

**ACCEPT-WITH-FIXES.** The design is scientifically coherent, falsification-first, and honest about its own risks — but it is not executable as drafted. Three binding defects (F1 multiplicity bar, F2 B-arm determinism incoherence, F3 wrong manifest filename) plus ten further required fixes must be repaired in a new draft version (append-only errata or v2 file; never silent edits). No defect is fatal to the design's logic → not REJECT. Fixes F1, F2, F4, F6, and the F12-4th-arm option (if taken) require independent delta re-verification; the rest do not.

**Decisive reason:** a CONTINUE here would *resurrect a bindingly killed family*. The draft's disclosed ~22.6% family-wise false-positive rate on the discovery claim is acceptable for an exploratory scan but not for a resurrection — the bar must be Bonferroni p<0.01 (F1). The remaining fixes close real holes (a guard pointing at a nonexistent file, an incoherent B-arm budget, scope-creep-prone KILL language) that would otherwise license ambiguous verdicts.

## What was attacked and what held

**Sources independently verified (no invented numbers):** EXP094's 36/60, nine contrasts (3 arm-pairs × 3 strata — the "nine" checks out), 0.7923 degeneracy statistic, and G5 band from `EXP094_VERDICT_REVIEW_2026-09-27.md` §2; the EXP093 "decisions are fragile / S2 mean margin −0.0018" quote and the logit-margin definition by reference from `EXP093_L11_CAUSAL_PREREG_SIGNED.md`; the constructor SHA-256 pin `5e03f206…` against the actual `experiments/runs/EXP094_peritem_l11/constructor.py` (matches byte-for-byte); the R_SEED and G7 attestation fields (`g72_attestation`, `g7_verdict`) in the manifest.

**1. Multiplicity — BROKE (F1).** The draft discloses 1−0.95⁵ ≈ 0.226 (arithmetic verified) and calls the conjunction "mitigation, not correction." Under the global null with stable decisions (EXP094 showed 0 flips/120 arms), the B_wrong-flat conjunct does almost no work against chance — P(B_wrong flat | null) ≈ 1 when the instrument is stable; its real power is against the strength-artifact *alternative*, not the global null. The stratum-consistency conjunct trims only ~3–8% at the minimum table. Realistic family-wise false-positive on the discovery claim: ~18–19%. For a resurrection claim that is too weak. **Ruling: the T(α)-vs-B(α) discovery McNemar is Bonferroni-corrected to p < 0.01 (5 tests).** Minimum significant table becomes b=8, c=0 (p = 2·2⁻⁸ = 0.0078125 < 0.01; b=7,c=0 gives 0.015625, n.s.). Adjacent-α replication is accepted as a *substitute* only if pre-registered as such. Mere disclosure is rejected — insufficient for overturning a binding KILL. The discriminant contrasts (B_wrong-vs-B, T-vs-B_wrong) stay at 0.05; they are guards, not discovery claims.

**2. Grid resolution vs KILL scope — HELD with language fix (F4).** The step-3 KILL is fenced to the grid, but the verdict line reads "Refuted (KILL family)" — "family" unqualified invites double-counting EXP094's already-killed family and scope creep in retelling. The killed object is the *magic-strength rescue*, not the family.

**3. B_wrong discriminant — RULED: accept with disclosure + fence (F12).** The isotropic random arm is the *correct* control for the live alternative in a strength sweep (strength-mediated nonspecific flips); replacing it with d_{π(i)} would lose that control. But a CONTINUE must not be readable as per-item specificity (this-item's-d_i vs any-task-direction needs the shuffled control). The 3-arm design stands; the CONTINUE language gets an interpretive fence. The drafter may alternatively add d_{π(i)} as a 4th arm within the 1300 cap (the F2 budget fix creates headroom) — that path requires full delta re-verification of the new decision rows.

**4. §6 items 4–6 — item 4 BROKE in part (F6), items 5–6 HELD.** Replication-gate brittleness: the draft keeps exact 36/60 with HOLD routing but never defines what a HOLD triggers, and gates on the aggregate (compensating per-item flips could pass it). Linearity diagnostic: the drafter's proposal (non-binding, interpretation-qualifying only) is correct — confirmed, add as specified. Threshold-account fence: airtight (§0, §3 step 3, scope fence all consistent) — confirmed.

**5. Own hunt:**
- **Degeneracy (§4.1) — HELD.** Every diagnostic fails safe on constant input; the zero-vector edge is routed to delivery-HOLD before the gate divides by zero; the dead-instrument/B_wrong-flat analysis is correct (the conjunction neutralizes it). Genuinely good.
- **Feasibility algebra (§4.2) — HELD, recomputed independently:** b=6,c=0 → 2·2⁻⁶ = 0.03125 < 0.05 ✓; b=5,c=0 → 0.0625 n.s. ✓; max flips 60 ≥ 6, max |ΔM| = 1.0 ≥ 0.10 ✓; no EXP079-style structural infeasibility ✓.
- **B-arm determinism — BROKE (F2).** The draft simultaneously asserts determinism ("deterministic CPU + byte-identical prompts + thread pinning *must reproduce*," step 0) and budgets "five independent baseline replications" (300 B passes). Under its own determinism premise the five B runs are byte-identical — not independent, and 240 passes are redundant. The draft must pick: (a) single B run, or (b) 5×B explicitly as a determinism diagnostic with a pre-registered divergence rule.
- **Manifest filename — BROKE (F3).** The draft cites `constructor_manifest_run.json` (2×); the file on disk is `constructor_manifest.json`. The executor's frozen-constructor guard points at a nonexistent file. (The G7 attestation fields do exist in the real file — verified.)
- **Step-4a α-index — ambiguous (F5).** "B_wrong(α) movement ≥ 6" must mean the *same* α (co-movement is the strength-artifact evidence).
- **Step-1 vs §4.1 zero-norm routing — inconsistent (F7).** Same event routed to HOLD (§4.1) and to per-α exclusion (§3 step 1).
- **"Two orders of magnitude" (§0) — false (F8).** The grid spans 16× = 1.2 orders, not two. §3's "16×" is correct; §0 overclaims.
- **§6 item 2 parenthetical — false (F9).** α=8.0 → ratio 0.3792 < 1 does *not* "exit the linear license" (boundary is >1).
- **"Exactly T(α)'s per-item norm" (§2.1.1) — imprecise (F10).** Exact only if regenerated ‖d_i‖₂ matches EXP094's 0.0474·‖h‖₂.
- **Doubling arithmetic (§4.1) — slip (F11).** b=60,c=0 → p ≈ 1.73×10⁻¹⁸ under doubling, not 8.7×10⁻¹⁹.
- **T-vs-B_wrong contrast has no decision role (F13).** It is computed (135-cell table) but step 3–6 never use it. Acceptable as diagnostic-only, but §2.4 must say so explicitly (Law #9 hygiene: no post-hoc role invention).

## Required fix list

| # | Fix | Sections | Re-verification? |
|---|---|---|---|
| F1 | CONTINUE's T-vs-B McNemar → p < 0.01 (Bonferroni, 5 α); minimum table b=8,c=0 (p=0.0078). Update §0 bars, §2.4 ALPHA (discovery contrast only), §4.2 algebra, and the "p ∈ [0.01,0.05) with caveat" sentence (such outcomes now fall to step 6 PIVOT). Note the ≥6-flip gate is dominated by p<0.01 for discovery but retained for B_wrong-flat/step-4a. Adjacent-α replication allowed only as a pre-registered substitute. | §0, §2.4, §3 steps 4–6, §4.2 | **Yes — delta** |
| F2 | Resolve B-arm determinism: (a) single B run (60 passes; budget 660 injection + 150 reserve = 810 expected; cap 1300 unchanged; pairing B(i) vs T(α,i)) — recommended; or (b) 5×B kept explicitly as a determinism diagnostic with pre-registered rule (any B(α,i)≠B(α′,i) → HOLD + diagnose nondeterminism source). | §2.3, §3 step 0 | **Yes — delta** |
| F3 | `constructor_manifest_run.json` → `constructor_manifest.json` (2×); pre-run checklist names the real file; confirm G7 fields present (verified: `g72_attestation`, `g7_verdict`). | §2, §5 item 2 | No |
| F4 | Step-3 verdict names the killed object: "the magic-strength rescue of the per-item static family is refuted *on the licensed five-point grid*" (never bare "KILL family"); carry the sub-grid-peak fence inline. Add B_wrong-moved sub-case: B_wrong(α)≥6 anywhere while all T(α)<6 → KILL stands, report must state nonspecific fragility was observed. | §3 step 3 | **Yes — delta** |
| F5 | Step 4a: B_wrong movement evaluated at the *same* α as the T(α) movement. | §3 step 4 | No |
| F6 | Step-0 gate: (i) per-item B-decision agreement with EXP094's archived B vector when archived (pre-run checklist: locate it; if absent, 36/60 aggregate with disclosed compensating-flip weakness); (ii) worksheet records the exact T(1.0)-vs-B(1.0) flip count; any nonzero <6 flagged as foundation wobble (sweep proceeds per the <6 standard); (iii) a step-0 HOLD triggers a pre-registered diagnosis lane (re-hash weights, verify thread pinning, byte-compare prompts) — never a silent re-run. | §3 step 0, §5 item 6 | **Yes — delta** |
| F7 | Zero-norm d_i or any common-cause-across-α delivery failure → HOLD + diagnose; isolated per-α delivery failures → exclude that α only. | §3 step 1, §4.1 item 4 | No |
| F8 | §0 "two orders of magnitude" → "16× (1.2 orders of magnitude)". | §0 | No |
| F9 | §6 item 2: α=8.0 → ratio 0.38 stays *inside* the ≲1 license; correct or delete the "exits the linear license" phrase. | §6 item 2 | No |
| F10 | B_wrong norm "targets (not 'exactly') T(α)'s per-item norm; exact when regenerated ‖d_i‖₂ matches EXP094's 0.0474·‖h‖₂; §3-step-1 probe is the enforcer. | §2.1.1 | No |
| F11 | §4.1: b=60,c=0 → p ≈ 1.73×10⁻¹⁸ under doubling. | §4.1 item 1 | No |
| F12 | Step-5 CONTINUE fence: licenses "a task-direction-shaped causal signal at the winning α on EXP092-B" — NOT per-item specificity (d_{π(i)} control is EXP095+ material). Optional: add d_{π(i)} 4th arm within the 1300 cap with pre-registered discriminant bars → then **delta re-verification required**. | §2.1.1, §3 step 5 | Fence: no; 4th-arm option: **yes** |
| F13 | §2.4 states the T(α)-vs-B_wrong(α) contrast is diagnostic-only with no decision role. | §2.4 | No |

## What held (no fix)

- All six drafter-flagged risks were honestly disclosed; the §6 attack lines were aimed at the right targets.
- §4.1 degeneracy analysis: complete and correct — constant-data unit tests, safe failure directions, zero-vector routing.
- §4.2 feasibility algebra: independently recomputed, all claims verify; no structural infeasibility.
- Cited facts: 36/60, nine contrasts, 0.7923, constructor pin, EXP093 quotes, margin definition by reference, LOG chain — all verified against primaries.
- Full within-(α,item) pairing with no post-hoc re-routing; step-6b wrong-direction handling ("never KILL" on a live causal channel) is correct.
- Law #11 labeling discipline observed throughout; Law #9 (no post-hoc metrics) and Law #4 (no silent hypothesis shifts) protected by the frozen decision table.
- The >1 threshold-account scope fence is airtight; the linearity diagnostic belongs non-binding as proposed.

## Review method

Read-only. No draft text altered; no model executed; no weights touched; $0 compute. Every number above was recomputed from the cited primaries or from first principles (binomial exact test); nothing invented. The draft remains DRAFT/UNSIGNED — this review does not sign it.

## Next steps

Repair lane addresses F1–F13 in a new draft version (or append-only errata) → independent delta re-verification of F1, F2, F4, F6 (and F12's 4th-arm option if taken) → SIGN → CEO execution clearance. Pilot remains unauthorized until all complete.
