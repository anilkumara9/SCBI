# Law #14 Independent Review — S4-8′ Cloze-Format Pre-registration Draft (LOG-4484)

**Reviewer lane:** Law #14 INDEPENDENT REVIEW. **Verdict: SIGN-WITH-FIXES.**
**Review completed:** 2026-09-28. **Review log:** LOG-4485.
**Scope:** Review ONLY. The draft was not edited, nothing was executed. $0 CPU.
**Inputs:** `research/innovation/S4-8_PRIME_PREREG_DRAFT_2026-09-28.md` (LOG-4484); the draft's six ranked §6 risks; `research/analysis_plans/EXP104_BENCH_AUTOPSY_2026-09-28.md` (LOG-4483); AGENTS.md Laws #4, #9, #13, #14, #15.

**Binding statement:** This review's SIGN-WITH-FIXES clears the draft for CEO signing consideration ONLY after all four defects below are repaired verbatim (or to the reviewer's equivalent). No experiment number is minted here; no run is authorized.

---

## Per-element scores

### 1. Prior-vehicle removal + tie-break vehicle — PASS (with MINOR fix)

**Does cloze genuinely remove the measured position-A prior vehicle?** Yes. The autopsy measured 30/60 top-1 picks at position 0 (p=2.02e-12) as a format-driven artifact of the `A)…H)` enumeration + terminal `Answer:`. The draft removes the enumeration, the letters, and the `Answer:` terminal entirely; there is no prompt-side ordering variable left to carry a position prior. The shuffle control is dropped *because positions no longer exist*, not replaced — the correct reasoning. No candidate order appears in the prompt, so no order parameter needs pinning or randomization.

**Is the ascending-token-id tie-break a new prior vehicle?** No, on the stated mechanism: it fires only on float32 exact-equality ties of candidate logits, which are measure-zero events (MC bench: 0/60; tie-guard 0.0). A tie-break cannot be a bias vehicle when it never binds; when it does bind, the per-item tie event is logged in the worksheet and the tie-guard (>0.25 → HOLD) adjudicates the degraded-instrument case. The token-id↔correctness correlation the task asks about is unmeasurable through this path. However, the draft never pre-registers the uniformity diagnostic, so a future tie cluster would have no recorded baseline — hence MINOR defect D3 below.

### 2. LINE-CLOSED bar — PASS

The baseline < 0.25 → LINE-CLOSED rule is a legitimate pre-registered stop, not an escape hatch. An escape hatch evades a damaging verdict; this rule *imposes* terminality on the line itself (mapped explicitly to "Inconclusive-for-the-line, terminal" — no verdict on the mechanism, no third readout, no further S4-8′ work on this model). The "no third readout" justification is sound: two distinct $0 readouts (word-scored MC, cloze) both exhausted means the next instrument proposal would be shopping for a passable number — the v3 §6 risk-6 backdoor warning, honored here as a pre-registered stop rather than circumvented. The asymmetry with the upper edge (>0.75 → HOLD, repairable miscalibration) is justified in-text: the lower edge is the autopsy's second-HOLD stop rule (verdict (b): untestable on Pythia-410m at $0). The breaking point is sharp, pre-registered, and adversarial against the proposal's own survival.

### 3. Tier-0 bars carried over — PASS (with MAJOR fix D1)

The four bars appear with identical thresholds and statistics to the v3 reference: median correct-rank over failed items ≤ 5 (premise, >5 → KILL), n_pop ≥ 12 (power, <12 → Underdetermined), tie-guard ≤ 0.25 (>0.25 → HOLD, float32 exact-equality definition), sanity band [0.25, 0.75] split into <0.25 → LINE-CLOSED (this draft's one named amendment) and >0.75 → HOLD. McNemar exact ALPHA=0.05 primary, Bonferroni 0.0125 others, Tango CIs, DELTA_BAR=0.10, D1/D2/N1 amendments, foil–top-1 overlap O ≤ 0.5 diagnostic stratum — all carried. The one amendment is named, not smuggled. **But** the carryover is anchored by reference to a draft the document elsewhere admits is unsigned (see D1) — the statistics themselves check out on paper; the anchoring does not.

### 4. Predicted band labeled as hypothesis — PASS

The [0.25, 0.45] band is tagged [HYPOTHESIS], explicitly "not a claim," anchored to the autopsy's non-pos0 subset measurement (0.233, prior only partially removed → "full removal should add points"), with the named alternative outcome (near chance 0.125 if the Cause-2 capability gradient dominates) and the explicit statement that Tier-0 adjudicates between them. Nothing is smuggled. The 0.233 anchor sits just below the 0.25 band edge — internally consistent with the "should add points" justification, and honestly presented.

### 5. Degeneracy analysis + constant-data unit tests — PASS (with MINOR fix D2)

All seven tests (a)–(g) are specified with assertions: constant-logit → tie-break path, mask-non-top-1 invariance, mask-top-1 promotion, b=c=0 → p=1.0 as valid null, empty failed set → vacuous → KILL, McNemar-exact cross-check on the full (b,c) grid pre-bench-contact, and the cloze-specific all-equal-logits tie-break-path exercise (g). The LOG-4338 lesson is honored on paper, and (g) genuinely exercises the generation-context path rather than assuming it. Test count is internally inconsistent between sections (see D2).

### 6. Scope fence / no MC↔cloze comparison as a finding — PASS

Risk 3 asks the reviewer to confirm the draft forbids MC↔cloze comparison explicitly — confirmed at §8: the 0.183 MC baseline is "calibration context (autopsy) only; it is not a primary, secondary, or descriptive result of any S4-8′ run. Violation = Law #9 breach." The position-A prior is recorded as an instrument confound, not a model property. No autonomy claim, no generality beyond the k=8 2-hop cloze bench / Pythia-410m / frozen backbone. The S6 stand-down and EXP085's kill are untouched; v3 is neither amended nor superseded. Law #9 (items/templates verbatim, no rewording on pilot accuracy, §2.1) and Law #4 (prompt freeze, §8) are pre-registered, not assumed.

### 7. Feasibility algebra — PASS

Correct-rank is measurable under cloze scoring: 8 G1-verified single-token candidates, one forward pass, extract logits at the pinned readout position, rank the correct token's logit among the 8. The McNemar feasibility figures are correct (b=6,c=0 → p=0.03125 < 0.05; b=5,c=0 → p=0.0625, n.s.), the n_pop ≥ 12 gate enforces the power requirement, and the DELTA_BAR=0.10 reachability computation is pre-registered as a hard gate before the battery (HOLD, not a silent edit, if unreachable). The 60-pass Tier-0 figure (~1 min CPU, $0, Δθ=0) is consistent with single-pass 8-logit extraction.

---

## Defects (4: 1 MAJOR, 3 MINOR)

### D1 — MAJOR: §1 anchors the carryover to "the signed v3 draft"; v3 is unsigned

**Location:** §1, first paragraph: "they transfer by reference to the signed v3 draft."
**Why it matters:** The draft's own header states v3 is "awaiting its own delta check" (LOG-4479/4480 line) — i.e., unsigned. Claiming a signed source is a false anchoring of the entire decision-table/battery-arms carryover, and it hides a real dependency: if v3's independent Law #14 review changes the decision table, the changes propagate here.
**Exact fix text (replace the sentence):** "The following are **not re-derived here** — they are carried over from the v3 draft (`S4-8_PREREG_DRAFT_v3_2026-09-28.md`, LOG-4479/4480 line, currently **unsigned**) and are restated here as this draft's own binding specification. If v3's independent Law #14 outcome alters any carried-over element, this draft must be re-reviewed before signing."

### D2 — MINOR: test-count inconsistency (§0 says six, §5 and §9 say seven)

**Location:** §0 ("The six §5 degeneracy unit tests re-run…").
**Why it matters:** §5 lists (a)–(g) = 7 tests; §9 item 5 says "the seven §5 tests." A reviewer or executor counting "six" will skip one test — likely the cloze-specific (g), the only one that exercises the new readout path.
**Exact fix text:** §0 → "The seven §5 degeneracy unit tests (a)–(g) re-run on the cloze rank function (same synthetic suite) before any bench contact."

### D3 — MINOR: no pre-registered token-id/correctness uniformity diagnostic

**Location:** §3 tie-break paragraph; §9 item 3 worksheet.
**Why it matters:** Element 1's second question (does token-id ordering correlate with correctness?) has no recorded baseline. The tie-break is harmless on the stated mechanism, but a future tie cluster would have nothing to check against.
**Exact fix text (append to §9 item 3):** "Descriptive diagnostic: per-item rank of the correct candidate's token id among the 8 candidate token ids (should be ~uniform over {1,…,8}); per-item tie-event flag (float32 exact equality). If tie events occur and correlate with token-id rank, the rank instrument is voided (HOLD) pending re-review."

### D4 — MINOR: cue-robustness sensitivity left as a §6 risk instead of pre-registered

**Location:** §6 risk 1 (completion-cue bias) and §2.3 item 3.
**Why it matters:** The draft already freezes the cue and bars post-Tier-0 cue changes (good), but leaves the descriptive cue sensitivity as a decision for later — exactly the kind of post-result design choice the LINE-CLOSED rule exists to prevent. Pre-registering it now as descriptive-only closes the backdoor tighter.
**Exact fix text (append to §2.3 item 3):** "Pre-registered descriptive sensitivity (NOT a second instrument): if Tier-0 passes its gates, the Tier-0 worksheet may include a re-run under the single named alternative cue `Answer:` + completion (one line in the worksheet, descriptive only, never a gate or a result). It may not be added, removed, or re-cued after any Tier-0 number is seen."

---

## Risk-by-risk confirmation (§6 agenda)

1. **Cue bias → D4** (tighten now, don't decide later).
2. **Candidate-absent frequency collapse → covered:** per-item top-1 distribution diagnostic is in the worksheet (§9 item 3) and the sanity band adjudicates; a collapsed sub-band readout closes the line via LINE-CLOSED, not a "better cue" repair. PASS.
3. **MC↔cloze comparison → forbidden at §8.** PASS.
4. **Rank-machinery generation-context → test (g) covers it; no MC constants leak** (120-pass budget and option-index tie-break are explicitly obsoleted in §3/§4). PASS.
5. **Tier-0 power under harder task → the 0.25 edge (= 2× chance 0.125) is the right sharp line**, and the draft is honest that the closure is irreversible. PASS.
6. **Single-cue rigidity → the LINE-CLOSED rule is the enforcement; D4 tightens the remaining backdoor.** PASS with D4.

---

## Verdict: SIGN-WITH-FIXES

The draft is a genuine pre-registration: hypotheses are tagged [HYPOTHESIS] and separated from [OBSERVATION]/[INTERPRETATION] per the 10-label standard; the six Law #15 packet elements (exact question, decision table, cheapest falsifying test, mathematical license, quantitative prediction, breaking point) are all present and sharp; it pre-registers its own line's death (LINE-CLOSED); it invents no numbers; it touches no signed protocol, no weights, no GPU. The four defects are textual repairs, not design flaws — none requires new analysis or a new experiment. Repair D1–D4 verbatim, then the draft is clear for CEO signing consideration.

**Not authorized by this review:** any run, any pilot, any experiment number, any protocol modification, any GPU contact. Sequencing remains: repair → re-review confirmation → SIGN → CEO clearance → cloze Tier-0.
