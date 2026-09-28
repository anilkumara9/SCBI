# Law #14 Adversarial Review — S6-1 Pre-registration DRAFT (Threshold-Account Breaking Point)

*Reviewer: Independent Scientific Mentor & Adversarial Reviewer (standing role; reports to the founder; binding verdict authority).*
*Date: 2026-09-28. Review lane is read-only: no edits to the draft, $0 compute, no model executed.*
*Target: `research/innovation/S6-1_PREREG_DRAFT_2026-09-28.md` (DRAFT, UNSIGNED; logged LOG-4410).*
*Licensing chain reviewed: LOG-4391 (breaking-point license) → LOG-4400 (EXP095 REFUTED) → LOG-4407 (EXP096 REFUTED, >0.4740 fenced untested) → LOG-4408 (sprint; S6-1 ranked #1, green-lit).*

## Verdict: ACCEPT-WITH-FIXES (binding)

The draft is licensable. Its central honesty treatment (§0.1) survives the primary attack; the decision table is fully pre-mapped with no unmapped outcome; the liveness instrument and coherence gate fail safe; the scope fences hold. Five localized fixes are required before SIGN — one corrects a false justification in the degeneracy analysis (F1), one corrects a misattributed ratio (F2), two tighten verdict language against overclaiming (F3, F4), one closes a single-B design gap (F5). None is structural. No fatal defect; not REJECT.

**Decisive reason:** the draft's hardest problem — testing beyond the linear license without smuggling it — is solved honestly (pure empirical probe on the threshold account's own terms, no margin-shift predictions, coherence boundary operationalized with a tripwire plus a pre-registered weakened-form KILL). The flaws found are all in justification language and fence precision, not in the decision machinery. The table itself routes every reachable outcome to exactly one verdict and cannot be gamed in either direction (verified below).

---

## 1. Primary attack: §0.1's "pure empirical probe" — legitimate or license-free curve-fitting?

**Attack as run:** without the linear license, the draft has no mathematical license for any quantitative prediction. Is "the account predicts decisions move once ‖δ‖ dominates ‖r‖" a testable hypothesis or an unfalsifiable gesture? A critic could argue the draft substitutes rhetoric ("on the account's own terms") for a license.

**Finding — HOLDS.** Three properties make the probe legitimate rather than curve-fitting:
1. The hypothesis is the threshold account's *own* prediction, quoted from the program's license (LOG-4391: "breaking point ‖δ‖/‖r‖>1"). Testing a claim on its own terms is the falsificationist core, not a dodge.
2. Every reachable outcome is pre-mapped to exactly one of five permitted verdicts (§3 steps 0–7 + per-ratio routing). There is no unmapped region where the drafter could improvise — the "weirdest outcomes" (frozen regime, zero-variance, ties, sign-heterogeneous movement, wrong-direction steering) each have a named step. Curve-fitting requires degrees of freedom; the table leaves none.
3. Nothing quantitative is smuggled: the draft explicitly disavows margin-shift predictions and reach-scaling extrapolation at these ratios. The bars (≥6 flips, p<0.01, B_wrong flat, all-strata ΔM_T>0) are disclosed program conventions, not derivations — and the asymmetry (strong conjunction for CONTINUE, flatness-at-live-ratios for KILL) is the standard falsificationist one.

**No fix required.** The "License verdict: HOLDS for a test, not a conclusion" (§1) is the correct epistemic stance and is honestly labeled.

## 2. Coherence boundary — is ratio 3.0 already representation-replacement?

**Attack as run:** the draft defines "coherent" operationally (zero-variance → RUN-INVALID) but 3.0's status as "maximum coherent strength" is stipulated (risk 7 admits: "This is a definitional fence"). Replacement can be subtler than zero-variance — decisions vary, yet are δ-artifacts. The drafter's counter is that norm-matched B_wrong controls "δ-driven but content-free" changes. Is the counter sufficient?

**Finding — HOLDS, with the counter verified adequate.** The design distinguishes the three cases exhaustively:
- Both arms move ≥6 → step-5a PIVOT (fragility — nonspecific, never CONTINUE). The δ-artifact case is correctly routed *away* from a false positive.
- B_wrong ≥6 with T<6 → step-4 KILL fires (first-match-wins), strengthened: the regime is live and flippable, yet the task direction does not move it. Correct.
- T ≥6/p<0.01 with B_wrong flat → step-6 CONTINUE: directional movement where matched-norm random injection moves nothing. The chance-alignment objection (a δ-artifact accidentally aligning with d_i) is priced out by the conjunction (60 items, all-strata ΔM_T>0 strict, p<0.01).

The 3.0 cutoff's stipulative character is disclosed, backstopped by the empirical zero-variance tripwire, and fenced by the pre-registered weakened-form KILL (§3 step 4). A post-null demand for ratio 5.0 would be goalpost-moving; the pre-registration correctly blocks it. **No fix required** beyond F4's language tightening (range notation).

## 3. Drafter's risk 1 — representation-replacement at 3.0 (the counter)

Covered in §2 above. The counter is sufficient because the decision table routes every (T-moves, B_wrong-moves) combination to a distinct, honest verdict. **No fix.**

## 4. Drafter's risk 2 — the ≥1-flip liveness bar

**Attack as run:** a single B_wrong flip unlocks the KILL (§4.1 item 4 discloses the asymmetry). Does noise license a strong conclusion?

**Finding — the worry dissolves under the draft's own determinism premise; no fix, disclosure affirmed.** The forward passes are deterministic (pinned threads §4/G4, pinned seeds, Δθ=0; EXP095 demonstrated 60/60 bit-reproduction across a rebuilt environment). In a deterministic system there is no sampling noise in the flip count: a B_wrong flip *is* a genuine causal effect of the injection, i.e., proof the regime can move. The bar's function is only to distinguish "nothing can move" (→ Underdetermined, never KILL) from "something moved" (→ evaluate). The KILL's evidential weight then comes from T's flatness across 120 item-arms, as the draft states. The ≥1 bar is principled, not merely weak; the disclosure (§4.1 item 4) is honest and stays.

## 5. Drafter's risk 3 — OOD-strawman and KILL-language fencing

**Attack as run:** read every KILL statement for scope leakage, including the headline.

**Finding — fenced, with one language fix (F4).** Audit:
- §0: "inertness is deeper than strength at *every coherent strength*" — fenced to coherent strengths. ✓
- §0.1: "What it does NOT mean: anything about dynamic, gated, multi-layer, or other-layer mechanisms" ✓; "anything about the direction's decodability" ✓.
- §3 step-4 weakened form: fence inline in the verdict language, "never dropped in retelling" ✓.
- §3 scope fence: dynamic/gated/multi-layer/other-layer → EXP097+; "never to 'all mechanisms' or 'all strengths'" ✓ (explicitly disavowed).
- §7: no claim beyond the tested ratios/mechanisms ✓.
- The OOD-strawman objection itself is correctly dismissed: the account is a claim *about* the >1 regime; testing it there is not a strawman.

**Fix F4** (below) tightens the "0.01185–3.0" range notation, which a careless reader could read as a continuous claim despite §2.2's "no interpolation" rule.

## 6. Step-4 weakened-form KILL — principled or hedge?

**Finding — principled, but incomplete (fix F3).** If 3.0 is RUN-INVALID while 1.5 is LIVE with T<6, the weakened form reports exactly what was earned ("dead at every coherent strength tested (ratio 1.5); ratio 3.0 crosses into representation-replacement and is untestable by static injection") and refuses to claim 3.0. That is anti-hedge machinery: it *prevents* overclaiming. However, the draft pre-registers the weakened form only for 3.0-RUN-INVALID, not for 3.0-FROZEN. If 3.0 is FROZEN (B_wrong=0, T=0) while 1.5 is LIVE with T<6, the full-strength KILL language ("dead at every coherent static-injection strength") would rest on 1.5 alone — a slight overclaim, since 3.0 contributed no test. **Fix F3** extends the weakened form to any non-live 3.0.

## 7. Step-3 Underdetermined routing — gameability audit

**Finding — cannot be gamed in either direction. HOLDS.**
- Toward a false KILL: KILL requires a LIVE ratio (B_wrong ≥1). A frozen regime (B_wrong=0, T=0) routes to Underdetermined by construction; the machine-written routing log (§5.5) is computed before the global table is walked, so no post-hoc re-routing is possible.
- Toward hiding a positive: any ratio with T≥1 is LIVE by the asymmetric rule (B_wrong=0, T≥1 → LIVE), so a moving T can never hide in Underdetermined.
- Toward a false CONTINUE via dead instrument: B_wrong=0 with significant directional T routes LIVE and CONTINUE fires — correctly, since task-direction-specific movement where random injection moves nothing is the *strongest* evidence for the account, not a confound (see F1's corrected analysis).

## 8. Feasibility algebra — independent recomputation

Recomputed from first principles ($0, no model):
- McNemar exact (doubling): b=8,c=0 → p = 2·(1/2)⁸ = 2/256 = **0.0078125** < 0.01 ✓. b=7,c=0 → 2/128 = **0.015625**, n.s. ✓. The draft's "discovery bar needs ≥8 directional flips" is correct (at c=0); the ≥6-flip movement gate is necessary-but-insufficient ✓ (6–7 flips → step-5 PIVOT, never CONTINUE).
- Family-wise: 2 ratios × 0.01 → 1 − 0.99² = 1 − 0.9801 = **0.0199 ≈ 0.02** ✓ as disclosed.
- α→ratio factor cross-check: 4.0 × 0.0474 = **0.1896** (EXP095 max, §0) ✓; 8.0 × 0.0474 = **0.3792** (EXP096 ratio, §1) ✓; 1.5/0.0474 ≈ **31.65**, 3.0/0.0474 ≈ **63.29** ✓.
- Delivery bands: 1.5 ± 25% = **[1.125, 1.875]** ✓; 3.0 ± 25% = **[2.25, 3.75]** ✓.
- Budget: 300 + 90 = **390** ≤ 600 hard cap ✓.
- **Caught (fix F2):** the draft writes "ratio 0.01185 (EXP094)" (§3 step 4) and "ratios 0.01185–3.0" (§3 fence). 0.01185 = 0.0474 × 0.25 = **EXP095's α=0.25 point**; EXP094 ran α=1.0 → 0.0474. Misattribution — the battery minimum belongs to EXP095, not EXP094.
- KILL feasibility (T<6 at every live ratio — satisfiable, null predicts ~0–2) ✓; liveness feasibility (B_wrong ≥1 — S5-4 moved 3/21 at ratio 0.38; satisfiable a fortiori at 1.5/3.0) ✓; coherence-gate computability (deterministic property of the 60-vector) ✓. No EXP079-style structural infeasibility.

## 9. Degeneracy analysis (§4.1) — fail-safe audit

Items 1–6 verified sound: McNemar on b=c=0 → p=1.0 (cannot manufacture CONTINUE) ✓; ΔM zero-variance → 0, cannot clear 0.10 ✓; flip-rate → 0 ✓; liveness instrument's two degenerate cases route correctly (truly-frozen → Underdetermined; the "noise-unlock" case is dissolved by determinism — §4 above) ✓; coherence gate cannot fire on the KILL's evidence (inert T inherits B's variance, 36/60) ✓; zero-norm d_i → delivery HOLD before the degeneracy gate is ever computed (no division by zero) ✓.

**Item 7 is defective (fix F1):** it claims "a dead instrument simultaneously returns T p = 1.0, failing the T-significance conjunct" — i.e., that B_wrong-flatness can never coincide with a licensable CONTINUE. This is false as a general claim and **contradicts the draft's own §2.4 liveness rule** ("B_wrong = 0 with T ≥ 1 → ratio is LIVE … evaluate normally"). A dead B_wrong (0 flips) with significant directional T (≥6, p<0.01, all-strata ΔM_T>0) routes LIVE and CONTINUE fires — and fires *correctly*, since task-direction-specific movement where matched-norm random injection moves nothing is stronger evidence for the account, not a confound. The real neutralization path is narrower: a *truly frozen regime* gives T=0 as well, and then the T-significance conjunct fails. The item's justification must be rewritten; the decision table itself is unaffected (it already handles the case correctly).

## 10. Budget deviation (390 vs packet's 360)

**HOLDS.** The deviation is disclosed in three places (§2.1 with the S5-1 v2 F2 precedent, §2.3, §6 risk 8 with attack/counter). The packet is a proposal, not a signed protocol; deviation with documented justification is legitimate. The determinism premise (EXP095's 60/60 bit-reproduction) justifies the single-B design. **Fix F5** adds the one missing guard: the single-B premise requires all 300 passes in a single pinned environment (no mid-run rebuilds) — currently punted to "executor-scheduling" in risk 8's counter.

## 11. Law #9 contrast hygiene

**HOLDS.** Three contrasts per ratio are computed; only T-vs-B and B_wrong-vs-B enter the decision steps; T-vs-B_wrong is labeled diagnostic-only (§2.4, cf. S5-1 v2 F13) and correctly excluded from every gate. Step-7a's mention of "null T-vs-B_wrong specificity" is a *reporting descriptor* for the otherwise-PIVOT sub-case, not a decision input — the step fires regardless (observation, not a fix).

## 12. Scope fences

Present and adequate (§0.1, §3 end, §7): the KILL is fenced to static per-item L11 injection at coherent tested strengths; dynamic/gated/multi-layer/other-layer/other-bench are EXP097+ material; "all strengths" and "all mechanisms" are explicitly disavowed. **Fix F4** sharpens the fence's ratio notation.

## 13. Chain-of-license check (does S6-1 violate LOG-4407's "no further static per-item L11 experiments are licensed"?)

**No.** LOG-4407's closure was explicitly scoped: "within the linear license up to ratio 0.38" / "the >0.4740-ratio regime … remain EXP097+ material — untouched." S6-1 tests ratios 1.5/3.0 — outside the killed scope, inside the fenced-untouched territory — and LOG-4408 explicitly green-lit its preregistration as "EXP096+ material." This is a new experiment in untested territory, not a resurrection of a killed family. The draft's §1 death-debt framing ("not a revival or an edit") is accurate.

---

## Required fixes (binding — SIGN only after all five are applied in a new draft version)

**F1 — Rewrite §4.1 item 7 (B_wrong flatness).** The current neutralization claim ("a dead instrument simultaneously returns T p = 1.0") is false and contradicts §2.4's liveness rule. Replace with the correct analysis: (a) a truly frozen regime yields T=0 as well, so the T-significance conjunct fails — that is the actual neutralization path; (b) B_wrong=0 with significant directional T routes LIVE per §2.4 and a CONTINUE there is valid — indeed the strongest task-direction-specific evidence. Location: §4.1 item 7.

**F2 — Correct the ratio attribution.** "Ratio 0.01185 (EXP094)" is wrong: 0.01185 = 0.0474×0.25 is EXP095's α=0.25 point; EXP094's α=1.0 point is 0.0474. Correct the parenthetical and the battery-minimum attribution. Locations: §3 step 4 ("from ratio 0.01185 (EXP094)"), §3 scope fence ("ratios 0.01185–3.0" attribution).

**F3 — Extend the weakened-form KILL to 3.0-FROZEN.** Step 4's weakened form covers 3.0-RUN-INVALID but not 3.0-FROZEN. If 3.0 is FROZEN while 1.5 is LIVE with T<6, the full KILL language would rest on 1.5 alone. Extend the weakened form to *any* non-live 3.0 (FROZEN or RUN-INVALID), or fence step-4's KILL to name the live ratio set explicitly. Location: §3 step 4.

**F4 — Replace range notation with the tested-point enumeration in the scope fence.** "Ratios 0.01185–3.0" reads as a continuous claim and tensions with §2.2's "no interpolation" rule. Enumerate the battery's tested points (0.01185 [EXP095 α=0.25], 0.0474 [EXP094 α=1.0], …, 0.4740 [EXP096 max band], 1.5, 3.0 [S6-1]) with "no interpolation" restated. Locations: §3 step 4, §3 scope fence.

**F5 — Pre-register single-environment execution for the single-B design.** The determinism premise behind running B once must be guarded: all 300 passes in one pinned environment, no mid-run rebuilds or library changes (the §5.3 manifest attests the environment; the draft must forbid changing it mid-run). One line in §2.3 or §5. Location: §2.3 (budget) or §5 (instrumentation spec).

---

## Observations (not fixes; for the record)

- **O1.** The drafter's top-3 risks were genuine and fairly stated; the review attacked each and an additional battery (F3's gap, F1's contradiction, F2's misattribution) beyond them. The falsification-first posture of the draft is real.
- **O2.** The "maximum coherent strength" 3.0 cutoff remains stipulative (risk 7), but disclosed + tripwired + weakened-form-fenced — acceptable as a pre-registered definitional fence.
- **O3.** The draft's single weakest *rhetorical* point — "pure empirical probe" sounding like license-free testing — is its strongest *methodological* point once the decision table is inspected: the table is where the license lives.
- **O4.** No number in the draft was found invented; every cited value traces to LOG-4391/4400/4407/4408, the verdict reviews, or the frozen archives, except the flagged F2 attribution (a citation error, not an invention).

---

## Next steps per the program's pipeline

Repair lane applies F1–F5 → new draft version (v1 preserved unedited; dated append-only errata) → independent delta re-verification of the five fixes → CEO execution clearance → experiment number minted → run (CPU, ≤390 expected, 600 hard cap). Pilot NOT authorized until all complete. No GPU contact under any circumstance.
