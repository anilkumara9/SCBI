# V83 Change Plan — Independent Review + Ranked Plan
**Date:** 2026-09-28 · **Lane:** V83 CHANGE-PLAN (analysis only; v82 frozen, untouched; no experiment number minted) · **$0 compute**
**Inputs:** [LEGENDARY_GAP_ANALYSIS_2026-09-28.md](sandbox://workspace/SCBI-worktrees/sync-log4393-4465/research/strategy/LEGENDARY_GAP_ANALYSIS_2026-09-28.md) (LOG-4465) · `~/workspace/scbi-paper/v82/paper.tex` (754 lines, read-only; line numbers below are from that file) · `~/workspace/SCBI/reports/research_log.md`
**Epistemology:** Law #11 labels throughout — [FACT] (verifiable from v82's text or the log), [OBSERVATION] (reviewer's reading), [INTERPRETATION] (judgment).

---

## PART 1 — Independent review of the gap analysis (LOG-4465)

I re-read all 754 lines of v82 and checked every fix against the source and the log. Verdicts:

| Fix | Grounded in v82? | Honest? | Actionable? | Verdict |
|---|---|---|---|---|
| 1. Viral number | ✓ — abstract L143 says "more than six times chance"; intro L152, hero caption, results say "33.33%" — four phrasings, zero repetition | ✓ — 33.33/5 = **6.667 → 6.7×** is exact arithmetic, not rounding games | ✓ | **ADOPT as-is** |
| 2. One name for the finding | ✓ — intro L152 mixes "Decodability Gap," "decodability without causal steerability," "static null," "the boundary," "the dissociation" | ✓ | ✓ | **ADOPT** |
| 3. Named enemy in abstract | ✓ — abstract L143 opens with a fact ("cheapest way to control"), no overturned belief | ✓ | ✓ | **ADOPT** |
| 4. Item-33 vignette | ✓ — Discussion L391 has the material | ⚠ **with correction** (see Overstatement O1) | ✓ | **ADOPT after artifact verification** |
| 5. One number per figure caption | ✓ — 7 figures; hero caption leads with the name, not the number | ✓ | ✓ | **ADOPT** |
| 6. Abstract/intro restructure | ✓ — intro fronts C1–C5 + "Law #14"/"kill criteria" before the finding | ✓ | ✓ | **ADOPT** |
| 7. Name the dilution law | ✓ — L270 buries "one-thousandth (1/1022) of its squared alignment"; already called a "dilution law" once in the Fig-4 caption | ✓ | ✓ | **ADOPT** |
| 8. Limitations as thesis | ✓ — "Narrow by design; the narrowness is what makes it true" exists at L381; "a null the rig is proven capable of breaking" at L391 | ✓ | ✓ | **ADOPT** |
| 9. Reproduce-the-hero box | ✓ — master table maps claims→artifacts, no run-this-see-that path | ✓ | ⚠ commands must be real/tested | **ADOPT with verification** |
| 10. Compress §sec:future | ✓ — L502 "industry thesis" paragraph + L504 five-stage prose exist as described | ⚠ **conflicts with founder preference** (see Tension T1) | ✓ | **ADOPT as compression, not deletion — founder call** |

### Overstatements caught in the gap analysis (independent review)

**O1 — Fix 4 invents Item-33 margin numbers.** [FACT] The gap analysis prescribes the vignette as: *"Item 33: decodes with margin 1.013 (2nd of 60) → injection moved its margin by +0.010/−0.004 → decision unchanged."* But v82 L391 says: *"the mean injection margin shift is only +0.0059 / −0.0076 **across items**"* — the mean over all 60 items, not Item 33's own shift. The figures +0.010/−0.004 do not appear anywhere in v82. [INTERPRETATION] This is exactly the defect class this program exists to catch: numbers that look artifact-verified but aren't. **v83 must not print the gap analysis's Item-33 numbers.** The change plan below requires the item-level shift for item 33 to be recomputed from the EXP093 primary artifacts before it goes in the hero figure. If it cannot be recomputed, the vignette carries the mean-across-items numbers labeled as such, or ships without the margin arrow.

**O2 — Gap 1 ("missing dose-response") is partially stale.** [FACT] The gap analysis states: *"EXP093 tests exactly one (layer, α) point… Missing: an α-sweep dose-response (≥5 magnitudes)."* But EXP095 (LOG-4399/4400) ran a licensed 5-point α dose-response, α ∈ {0.25, 0.5, 1.0, 2.0, 4.0} (16× strength range), 660 injection rows: flips {0,0,0,1,1}, all McNemar p=1.0 — **REFUTED**, "the inertness is not a strength artifact." What remains genuinely unmeasured is the dose-response **for the hero shared-direction claim** (EXP092×EXP093 at layer 11): EXP095 tested the *per-item* family, and its scope fence explicitly bars "all strengths" claims and the ‖δ‖/‖r‖>1 threshold account. Additionally, Gap 1's framing ("EXP093's own margin data suggests a threshold structure") predates EXP097 (LOG-4416: threshold account NOT SUPPORTED — PIVOT-fragility). [INTERPRETATION] The honest v83 disclosure is a three-part dose-response statement, not a "missing experiment" line (see Change #3 below).

**O3 — Fix 5's hedge is resolved clean.** The gap analysis hedged "check the two `_superseded` entries are not compiled." [FACT] `figs/_superseded/` is a directory; `paper.tex` references 7 tikz figures, none superseded; the string "superseded" appears 0 times in the source. No action needed.

### Tension T1 — Fix 10 vs. the founder's standing preference
[FACT] The founder's standing paper preference (2026-09-26): *"Present the full vision (math, algorithm, benchmarks) without an in-flight 'currently working on it' narrative."* Fix 10 proposes cutting the five-stage "path to superhuman" (L504) and the industry thesis (L502) because they read as "a pitch deck inside a boundary-science paper." [INTERPRETATION] Both are right about different things: the credibility of a boundary paper benefits from a short future section; the founder's vision benefits from keeping the staged horizon. The plan below implements Fix 10 as **compression into a boxed three-bet + staged-horizon summary with falsifiers intact**, not deletion — and flags the depth of the cut as a founder decision (see approval brief).

---

## PART 2 — Ranked v83 change plan

Ranking criterion: citation impact per unit of claim risk. Each change names the exact v82 location, the edit, the evidence LOG, the predicted reader-perception effect, and the guardrail risk.

### Change #1 — THE viral number, byte-identical everywhere (Fix 1) · Impact: highest
- **v82 locations:** abstract L143 ("more than six times chance… changes zero decisions"); intro L152 ("more than six times chance is causally inert"); hero caption L158–161 ("20/60 = 33.33% (p = 0.000999…)"); results lead §sec:results; conclusion L508.
- **Change:** Replace all four phrasings with one line, printed identically in all five positions: **"Decodes at 6.7× chance; steers zero decisions."** Keep the p-value and N=60 in the caption as supporting detail, not as the lead.
- **Why [FACT]:** 33.33/5 = 6.667 → 6.7× is exact (EXP092, master table app:master, p=0.000999). Zero flips at α=1.0 (EXP093, McNemar b=c=0, p=1.0).
- **Predicted effect:** Memorability is citation infrastructure — people cite what they can recite. This is the paper's "175B parameters" line.
- **Risk (guardrail check):** "Steers zero decisions" must never be read as metaphysical zero — it is *observed* 0 flips on N=60 (rules out flip rates >~5%, L381). Pair with Change #3's dose-response disclosure in the same section. No new claim; risk LOW.

### Change #2 — Boundary-map expansion: EXP094–103 + S6-5 + stand-down (the best no-compute evidence delta) · Impact: highest
- **v82 locations:** kill ledger §sec:kills (L367); C1 in intro; phase diagram §sec:phasediagram (L376) + Fig. 6 caption; master table app:master (L530).
- **Change:** Extend the ledger with ten rows and the pooled bound; redraw the phase diagram's sideline as the closed {mean,max}×{L11,L20} gate family; add the family-pooled 95% upper bound 2.74% (S6-5) to C1's "flip rates above ~5% ruled out" — which becomes "above ~3% family-pooled (5/381, one-sided 95% UB 2.74%; per-cell 4.87% stands as declared)."
- **Why [FACT]:** EXP094 Refuted 0/120 (LOG-4377) · EXP095 α-grid REFUTED, 16× range, flat (LOG-4400) · EXP096 REFUTED (LOG-4407) · EXP097/099 PIVOT-fragility (LOG-4416/4434) · EXP098 PIVOT-premise (LOG-4423) · EXP100/102 PIVOT-untestable at 0/60 and 1/60 coverage (LOG-4441/4455) · EXP101/103 Refuted (LOG-4448/4462, UB 5.3%) · S6-5 pooled 5/381 → 2.74% (LOG-4409) · S6 stand-down (LOG-4463/4464).
- **Predicted effect:** Converts "a boundary finding" into "the boundary map" — ten experiments, ~2,000 CPU passes, $0 — closed by binding verdicts. This is the Chinchilla-grade density move: authority by complete closure of a space, not by a bigger number.
- **Risk:** Keep verdict wording binding and exact: PIVOT-untestable is not Refuted; do not soften the N1 novelty admission or the retraction (they are the credibility engine). Risk MEDIUM — reviewer lanes must walk every new row against its verdict doc. The S6 stand-down sentence ("the direction is the problem, not the gate," LOG-4464) must carry its scope fence (killed per-item L11 direction, frozen Pythia-410m, EXP092-B only).

### Change #3 — Honest dose-response disclosure (corrects Gap 1 per O2) · Impact: high
- **v82 locations:** Discussion A4 paragraph L391 ("EXP093 tests one (layer, α) point"); licensed claim L381; Limitation 6 (L394).
- **Change:** Replace "EXP093 tests one (layer, α) point" with the three-part statement: (1) the *per-item* family has a measured 5-point dose-response, α ∈ {0.25,…,4.0}, flat (EXP095, LOG-4400, REFUTED); (2) the *hero shared-direction* dose-response is unmeasured; (3) the threshold-account breaking point (‖δ‖/‖r‖>1) is untested and the S6 stand-down (LOG-4464) currently bars the CPU path to it. Add the EXP095 scope fence verbatim ("no 'all strengths' claim") to Limitation 6.
- **Why [FACT]:** LOG-4399/4400 (flat dose-response), LOG-4416 (threshold account NOT SUPPORTED), LOG-4464 (stand-down).
- **Predicted effect:** A reader who knows EXP095 exists will trust the paper more for stating it; a reader who doesn't will learn the wall is bigger than the hero figure alone.
- **Risk:** Do not cite EXP095 against the >1 threshold account (its own verdict forbids it). Risk LOW if the scope fence is quoted.

### Change #4 — Name the dilution law (Fix 7) · Impact: high
- **v82 locations:** theory L270 ("keeps roughly one-thousandth (1/1022)…"); Fig. 4 caption ("Read Eq. (3) as a dilution law"); discussion L391; conclusion L508.
- **Change:** Box it as **"The 1/(d−r) Dilution Law"** in the theory section; reference it by name in the retraction, discussion, and conclusion.
- **Why [FACT]:** Proposition 1 proves it; the number 1/1022 (d=1024, r=2) is already in v82.
- **Predicted effect:** Gives the theorem independent citability — the paper's best shot at legendary life that doesn't depend on the experiments (gap analysis §3a).
- **Risk:** Naming is presentation, not a new claim; the cross-space caveat (L270: "a cross-space transfer that was never validated") must travel with the name. Risk LOW.

### Change #5 — Named enemy in the abstract (Fix 3) · Impact: medium-high
- **v82 location:** abstract L143, first sentence.
- **Change:** Add one sentence up front: the field's working assumption is that decodability is a proxy for steerability — if a direction carries task information, adding it back should move decisions. This paper breaks that proxy.
- **Why [INTERPRETATION]:** GPT-3 named fine-tuning; Chinchilla named Kaplan's ratio. A paper without a named antithesis is a report; with one, an argument. Arguments get cited.
- **Risk:** None to guardrails — it sharpens, not extends, the claim. Risk NONE.

### Change #6 — Item-33 hero vignette (Fix 4, corrected per O1) · Impact: medium-high
- **v82 location:** Discussion L391 → add boxed callout to Fig. 1 (fig_hero.tikz).
- **Change:** Add the worked-example strip: "Item 33: decodes with margin 1.013 (2nd of 60) → decision unchanged under injection." **Required precondition:** recompute Item 33's *item-level* injection margin shift from the EXP093 primary artifacts before any per-item number goes in the figure. Do NOT use the gap analysis's +0.010/−0.004 (not in v82, unverified). If recomputation is infeasible, use v82's mean-across-items numbers labeled as such, or ship the vignette without the margin arrow.
- **Why [FACT]:** L391 establishes the decode margin and the unchanged decision; the per-item shift is the only unverified piece.
- **Predicted effect:** The CoT-Figure-1 move — the screenshot that travels on social media.
- **Risk:** Fabrication risk if O1's numbers are used — the precondition closes it. Risk MEDIUM until the artifact recomputation lands.

### Change #7 — Term discipline (Fix 2) · Impact: medium
- **v82 location:** intro L152 ff.; C2 claim text.
- **Change:** "Decodability Gap" becomes the only proper name for the central finding; "decodability without causal steerability" demoted to the definitional gloss; "static null"/"boundary"/"dissociation" get mechanism-scoped qualifiers.
- **Risk:** Mechanical edit; must not silently alter claim scope (Law #5). Risk LOW.

### Change #8 — Abstract/intro restructure (Fix 6) · Impact: medium
- **v82 locations:** abstract L143; intro L152–end; C1–C5 itemize.
- **Change:** Abstract arc → problem → adjudication procedure → the number (Change #1) → what it changes (Change #5) → honest boundary. Move the C1–C5 enumeration to a "Checkable claims" box in §sec:pipeline; strip "Law #14"/"kill criteria" machinery from the intro (GPT-3's abstract never mentioned OpenAI's internal process).
- **Risk:** C-number text must stay byte-identical when moved (Law #5). Risk LOW.

### Change #9 — Limitations as thesis (Fix 8) · Impact: medium
- **v82 location:** limitations L394.
- **Change:** Preface with L381's "Narrow by design; the narrowness is what makes it true" and L391's "a null the rig is proven capable of breaking" in the header.
- **Risk:** Pure framing; owns the #1 reviewer attack. Risk NONE.

### Change #10 — Caption audit (Fix 5) · Impact: low-medium
- **v82 locations:** 7 figure captions (hero, rig, machine, retraction, pipeline, phase diagram, bets).
- **Change:** First sentence of every caption becomes the quantitative takeaway. (_superseded/ confirmed not compiled — no action.)
- **Risk:** Mechanical. Risk NONE.

### Change #11 — "Reproduce the hero figure" box (Fix 9) · Impact: low-medium
- **v82 location:** new box, §sec:pipeline or Appendix app:repro.
- **Change:** Entry-point commands + expected outputs reproducing Fig. 1 end-to-end from named primary artifacts.
- **Risk:** Commands must be real and tested against the artifacts; a broken reproduce box is worse than none. Risk MEDIUM — gate on a tested run.

### Change #12 — Compress §sec:future (Fix 10, with T1 compromise) · Impact: low
- **v82 locations:** L502 (industry thesis), L504 (five-stage path).
- **Change:** Compress to a boxed three-bet summary with the "dies if…" falsifiers intact, plus the staged horizon kept as falsifiable one-liners (Stages 1–5 keep their killers). Do NOT delete the full vision — see T1.
- **Risk:** Over-cutting conflicts with the founder's standing full-vision preference. The depth of the cut is a founder decision (approval brief below). Risk LOW if boxed.

---

## PART 3 — Founder-approval brief

**Approving v83 authorizes:** building one new paper version (v83) from frozen v82 with Changes #1–12 above, preserving v82 byte-identically and carrying forward every binding verdict, the Procrustes retraction, the N1 novelty admission, and the closing line "The transfer is not a map; it is a draw." verbatim; Law #14 review of the v83 diff before any external use.

**Approving v83 does NOT authorize:** any new experiment or compute; any change to a signed protocol, verdict, or primary artifact; any softening of limitations or novelty; any "all strengths"/"all layers" generalization; arXiv submission or public posting (still founder-reserved); or filling the dose-response gap by violating the S6 stand-down (LOG-4464).

**Two founder decisions needed at approval time:** (a) Change #6's precondition — accept the artifact-recomputation requirement or drop the margin arrow; (b) Change #12's cut depth — boxed compression vs. full retention of the staged vision.

---

*Lane complete 2026-09-28. Analysis only; v82 untouched; no experiment number minted; $0 compute.*
