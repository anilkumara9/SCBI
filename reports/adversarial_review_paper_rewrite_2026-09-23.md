# Adversarial Review — Paper Mechanism Rewrite (LOG-145 dispatch, LOG-155 landing)

**Reviewer:** Law #14 adversarial reviewer (LOG-156). Verdict answers to the CEO; no softening instructed or honored.
**Scope:** `reports/paper_draft.md` rewritten §7 (+ §§8–12, abstract, data statement). Analysis only — no GPU, no experiments.
**Verdict: SIGN-WITH-FIXES** — the draft clears for external use once the enumerated fixes below (all wording-level, no re-computation required) are applied. Venue decision remains user-reserved.

---

## 1. Number integrity (Law #2) — PASS

Every re-verified number was recomputed against its primary artifact. All match.

**G1** (`research/analysis_plans/G1_RESULTS_2026-09-23.json`):
- Ē_QK(B_agg) = 0.3899846… → paper 0.389985 ✓; Ē_QK(b_mean) = 0.3561852… → 0.356185 ✓
- Null (100 draws, seed 20260923): q05 = 0.3410994… → 0.341099 ✓; q95 = 0.3617300… → 0.361730 ✓; mean = 0.3523329… → 0.352333 ✓
- p_low(B_agg) = 1.0 ✓ (every null draw below B_agg — independently re-verified from the 100-draw sample); p_high(b_mean) = 0.227722… → 0.2277 ✓
- "B_agg beats the bridge in 35 of 48 heads" — recomputed from `per_head`: 35/48 ✓; cross-head r = 0.27 — recomputed ✓. Both also appear in `G1_REPORT_2026-09-23.md` (ll.65–66), so the paper introduces no new empirical claim.
- OV: B_agg = 0.4067585… → 0.406759 ✓; b_mean = 0.3533082… → 0.353308 ✓; null band q05 = 0.3466 / q95 = 0.3590 ✓
- s_j companion: median 0.3562008… → 0.356201 ✓; s̄ = 0.3670994… → 0.367099 ✓
- B_wrong QK = 0.4884746… → 0.488475 ✓
- Kill-rule fidelity: G1_PLAN.md §7 states "KILL — if A ≥ B"; the paper's table states the same pre-registered rule (Ē_QK(B_agg) ≥ Ē_QK(b_mean) → KILL) and it fired. ✓

**EXP077 GPU vs CPU-smoke provenance — PASS, never conflated:**
- Paper cites the GPU ruling from the LOG-128 record: branch (c) NEITHER, baseline 0.5667, radial all ΔM=0.00pp p=1.0 Holm-adjusted S_H=∅, angular/control/offset/replication b=c=0 p=1.0, bridge gate +10pp b=6 c=0 p=0.03125 — all match LOG-128 verbatim. ✓
- Paper cites the in-repo archive `experiments/runs/EXP077_cone_vs_line/exp077_results.json` explicitly as **the CPU-smoke run**: baseline 0.6 ✓, bridge +23.33pp b=14 c=0 p=0.000122 ✓ (recomputed from the JSON). The smoke provenance is labeled at every mention. ✓

**EXP067** (`reports/research_log.md` LOG-130): rank=33 (required ≥64), gap=1.59e-08 vs smoke 1.44e-08, head 0 V1→V2_Biblical, 70.79s, `exp067_results.json` (4bef6dc6…, 924 B), `exp067_run_log.txt` (118c9c4f…, 2139 B), sanity hash 4c242d9a…5ed48dd — all match. ✓

**EXP065/066 bridges:** EXP065 Same_Layer_Output_Bridge: +16.67pp, 10 rescues, exact_p=0.001953125 → paper p=0.0020 ✓; EXP066: +13.33pp, 8 rescues, exact_p=0.0078125 → paper p=0.0078 ✓; baselines 68.33%/56.67%, 19/26 rescuable errors ✓. Static conditions ΔM=0, b=c=0, p=1.0 ✓.

**Data statement:** lists the CPU-smoke archive as the EXP077 in-repo artifact and routes the GPU outcome through the LOG-128 log record — honest given the GPU files were produced on the execution machine; no number is cited that lacks a trace. ✓

---

## 2. Retraction completeness — PASS

Full-paper search for null-space / downstream-filtering / null space language: every occurrence sits inside an explicit retraction context — abstract (falsified prior), §7.1 (quoted theorem + "RETRACTED" + Refuted-with-scope), §9.8 (scope), §11 (retraction summary), §12 (superseded-wording ledger). The only other "null-space" is §6.1 "LAPACK's null-space completion" — SVD terminology, not mechanism language. No surviving endorsement outside retraction text.

---

## 3. I1's scope — PASS with one qualifier (see F2)

§5.6 I1 and §7.2 state the Supported verdict strictly on endpoints (raw cosine ≈0.7 + zero decision flips at headroom + bridge rescues), with §5.6 I3 fixing the scope conditions. "Causal transfer / causal interchangeability" language describes endpoint behavior, not mechanism attribution — permitted. The single spot where mechanism leaks into a control claim is §5.4's "legitimate 'causal access exists at this layer' control" (F2 below).

---

## 4. The Underdetermined bridge — PASS

Three hypotheses honestly labeled ([HYPOTHESIS] readout bypass; [HYPOTHESIS] different direction family; [CONJECTURE] LayerNorm/softmax/value-path attenuation); the operative verdict is stated as **[INTERPRETATION]: Underdetermined; this paper claims no mechanism.** No hypothesis is promoted to interpretation of a fact. The closest thing to a tilt is the §7 title's "Readout-Misalignment-or-Unknown" giving rhetorical primacy to H1 — non-blocking, because the operative text explicitly demotes it to [HYPOTHESIS] ("Untested by intervention"). No fix required.

---

## 5. The §7.3 standing caveat — INADEQUATE AS WRITTEN → F1, F2

The paper's caveat names only the LOG-144 entity-similarity-leak review, and describes it as "currently testing" — but the LOG-144 review has **landed** (LOG-149: REVISE, nine binding requirements; C-A pre-reg drafting queued under LOG-150). Worse, two **later, independent** challenges now attack the positive control itself, not just the mechanism of its rescue, and the paper names neither:

- **Cluster A (LOG-153):** the bridge is constructed from target/foil option-token unembedding rows — on the letter of Law #7 (zero data leakage) this is option-information leakage; every rescue (EXP077 +10pp, EXP070 C7 +16.67pp, smoke +23.33pp) may be a label-assisted readout artifact; the corpus never audited its own positive control against its own law. CEO ruling requested.
- **Cluster C (LOG-154):** independent convergence — "output bridge may be readout tilt, not a mechanism," with a $0 label-shuffle falsification proposed; may demote the bridge's positive-control status across the signed EXP065/066/070/077 protocols.

The current caveat ("the bridge's rescue licenses only the empirical observation, not any of the three hypotheses") answers the mechanism question but not the validity question: if Cluster A is right, the bridge cannot be invoked as a "legitimate 'causal access exists at this layer' control" (§5.4) at all — the rescue may not demonstrate legitimate causal access. The caveat must be strengthened to name both challenges and qualify the control claim. Required sentence changes (F1, F2).

---

## 6. No new empirical claims; no synthesis scope creep — PASS

No number in §7–§8 lacks an artifact trace (all derive from G1 JSON, LOG-128/130 records, or the smoke archive; the 35/48 and r=0.27 figures live in the G1 report). The A–J synthesis is never invoked; the paper cites only program-internal standing reviews (LOG-144/149).

---

## 7. Retraction culture (§12) — PASS, with a verification limit noted

- Item 1 verified: the quoted "Core Causal Null-Space Theorem" matches `.muse by meta/THEORY_AND_MATHEMATICAL_FOUNDATIONS.md` §3.3 (l.112) verbatim, including the bolded QK-matrix clause. ✓
- Items 2–4 (prior §7 status line, pivot sentence, prior §9 items) are internally consistent with the LOG-145 dispatch and LOG-155 landing records, but **cannot be independently verified**: the pre-rewrite full draft was never committed (HEAD's `reports/paper_draft.md` is a 59-line stub), so the superseded draft wording has no version-controlled ancestor. No defect in the paper itself; recommendation to the program: keep a dated snapshot of any draft before a rewrite, so future §12 checks are independently verifiable.

---

## 8. Labeling and verdicts — PASS

Epistemic double-labeling is consistent throughout ([OBSERVATION]/[INTERPRETATION]/[HYPOTHESIS]/[CONJECTURE]/[ASSUMPTION]/[NOTE] + the fact/inference role). Verdicts used: Supported (I1), Refuted (§3.3 as a QK-subspace claim, with G1's pre-registered "KILL" separately rendered as Refuted), Underdetermined (bridge mechanism), Inconclusive (dynamic alignment, §5.6 I2 in substance). The three evidentiary levels are stated in §7.3 with the bridge capped at level 1. Banned verdict phrases ("promising", "worth another experiment", "interesting") do not appear as verdicts; the lone "interesting" (§10) is prose about the program, not a verdict.

---

## Required fixes (all wording-level; no re-computation)

**F1 — §7.3 standing [NOTE]: replace the stale single-challenge caveat.** The current note says the LOG-144 review "is currently testing" the confound. It must (a) record that the LOG-144 review **landed** (LOG-149: REVISE; nine binding requirements for the C-A pre-reg, drafting queued LOG-150), and (b) name the twin independent challenges that target the positive control itself: **Cluster A Law #7 option-leakage** (bridge built from test option-token rows; rescues may be label-assisted readout artifacts; the positive control was never audited against Law #7 — LOG-153, CEO ruling pending) and **Cluster C readout-tilt** ($0 label-shuffle falsification proposed; may demote the bridge's positive-control status across EXP065/066/070/077 — LOG-154). Close with: until these rule, the bridge's rescue licenses only the paired-decision numbers, not the three hypotheses *and not the claim that behavior is legitimately steerable at this layer*.

**F2 — §5.4: demote the "legitimate" control claim.** Change "This is a legitimate 'causal access exists at this layer' control — behavior *is* steerable at layer 20 via output-space directions" to the observation-only form: the bridge is the program's positive control that rescues behaviorally, but the Cluster A Law #7 and Cluster C readout-tilt challenges dispute whether the rescue demonstrates legitimate causal access; until they rule, the rescue is an [OBSERVATION] only. Cross-reference the updated F1 note.

**F3 — §7.2 smoke-archive wording (minor precision).** "The in-repo archive … (the CPU-smoke run) shows the same flat-zero pattern" is slightly stronger than the artifact: the smoke `angular` endpoint has b=2, c=1, p=1.0, ΔM=+0.0167pp (vs GPU b=c=0). Reword to "shows the same statistically-flat null pattern (every endpoint non-significant; smoke angular b=2, c=1, p=1.0 vs GPU b=c=0)". Provenance labeling itself is correct and must be kept.

---

## Standup (four lines)

- **Verdict: SIGN-WITH-FIXES.** All numbers re-verified against primary artifacts (G1 JSON, LOG-128/130, smoke archive, EXP065/066 JSONs); GPU/smoke provenance correctly labeled everywhere; retraction complete; I1 scoped to endpoints; bridge honestly Underdetermined; no synthesis creep; verdicts all from the permitted set.
- **Blocking the SIGN:** the §7.3 caveat is stale (LOG-144 review has landed, not "currently testing") and names only one of three standing attacks on the bridge — the Cluster A Law #7 option-leakage and Cluster C readout-tilt challenges, which dispute the positive control's validity itself, must be named and the §5.4 "legitimate causal access" claim demoted to observation-only (F1, F2).
- **Minor:** §7.2 "same flat-zero pattern" overstates the smoke archive (angular b=2, c=1, p=1.0) — reword to "statistically-flat null" (F3); §12 items 2–4 unverifiable against version control (paper_draft.md never committed pre-rewrite) — noted, program should snapshot drafts before rewrites.
- **Non-issues:** §7 title's H1 primacy is neutralized by the operative Underdetermined verdict; "(verbatim)" on the EXP077 ruling is accurate; the §10 "interesting" is prose, not a verdict.
