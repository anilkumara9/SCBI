# Independent Law #14 Review — H4 (PTTSC) Pre-registration

**Lane:** LOG-4548 (independent review only — this lane did not draft the document)
**Date:** 2026-09-29
**Document under exact-version review:** `research/prereg/EXP_PREREG_H4_PTTSC_2026-09-29.md`
**Dossier reference:** `research/innovation/SPRINT_2026-09-29_SUMMIT.md` §H4
**Verdict: SIGN-WITH-FIXES** (5 required fixes, each verifiable; all required before execution; plus 2 recommendations)

This lane reviewed only. It does not fix the draft, does not approve execution, does not mint an experiment number, and dispatches no follow-ups. Execution requires the fixed exact version to pass a re-review/fix-verification lane (program precedent: H1 LOG-4542 → LOG-4544).

---

## Headline finding [INTERPRETATION]

The design's statistics, gates, budget logic, and falsification structure are sound — but the **answer-elicitation protocol is construct-invalid as written** (FIX-1). The prompt asks the model to "Reply with a single letter, A or C" while the question presents entity names ("Who is higher in rank, Mars or Venus?") and never establishes what A/C denote. Independently verified against the bench builder (`benchmark_exp089.py: build_benchmark()`): every one of the 60 items asks "who is **higher** in rank" with the target entity always highest, so the ground-truth label is **constant ("A" = target) across all items**. The model cannot map its reasoning to the letters because the mapping is never communicated — a human subject given this prompt would ask "what do A and C refer to?" As operationalized, "accuracy" = P(emit "A"), not decision capability. A CONTINUE would then be driven by a first-token bias shift, not better decisions (false positive for the coordinator program); a KILL would rest on a broken instrument, violating the program's own "a KILL must mean the instrument worked" principle (cf. H1 §3.3 G4 rationale). The fix is small and preserves the entire statistical apparatus (FIX-1).

Note on precedent: H1's review (LOG-4542) accepted the same letter convention, but H1's metric never depended on letter votes (its decision statistic was the cosine argmax; the self-report channel went RUN-INVALID on elicitation failure before any metric). H4's metric depends *entirely* on the letter votes, so the hole is load-bearing here.

---

## 1. The three dossier deviations — adjudicated [FACT + INTERPRETATION]

The draft's §8 header says "**two** deviations," but there are **three** substantive deviations from the dossier (the third is documented in §3.2/§7, not §8 — see FIX-4):

**(a) Budget redefined as identical *executor* budget, planner pass as treatment — CORRECT reading.** The dossier's "identical generation budget" is ambiguous; the draft pins 4×48-token executor developments vs 4×48-token baseline samples (identical sampling spec) with the ≤160-token planner pass as the marginal treatment. This is the right reading: the dossier's own theory (PTTS pays off via the planner overhead) and its CONTINUE decision ("planner-executor pattern enters the adaptive-loop designs") both concern the *marginal value* of the planner pass. Matching the planner pass away (e.g., 3 developments vs 4) would test a different question (fixed-total-budget reallocation). Bias-toward-CONTINUE check: the planner arm does consume ~40% more total tokens (≤544 vs ≤384/item), but the CONTINUE bar requires a one-sided McNemar p ≤ 0.05 with minimum (b,c)=(5,0) — five one-directional flips with zero reversals. Random prompt noise does not produce (5,0); the bar, not the budget, carries the license. The draft states the marginal-value framing explicitly (§3.7). **Pass, no fix.** (A CONTINUE therefore means "planning is worth the extra ~160 tokens," which is what the draft claims.)

**(b) "+8pp → CONTINUE" replaced by McNemar p ≤ 0.05 — SOUND and required.** Independently recomputed (exact binomial, `math.comb`): all seven table values match exactly — (5,0)→0.0312, (6,0)→0.0156, (6,1)→0.0625, (7,1)→0.0352, (7,2)→0.0898, (8,2)→0.0547, (9,2)→0.0327. The dossier's +8pp at n=20 is ≈1.6 items: even (b,c)=(2,0) gives p=0.25, and the draft's own example (net +5/20 as (6,1) → p=0.0625, fails) is correct. A raw +8pp bar at n=20 has no statistical license — the draft's claim that it is "not statistically meaningful" is **verified true**. Minimum CONTINUE configuration is indeed (5,0) (net +5, zero compensating flips); (4,0)→0.0625 fails. One-sidedness is pre-registered and directional (hypothesis: planning helps); a strongly negative outcome ((0,5)) routes to KILL via net ≤ 0, correctly. The HELD zone (0 < net, p > 0.05) is the honest receptacle for the underpowered middle — it licenses nothing. **Pass, no fix.**

**(c) Scope cut n=60 → 20-item pilot — licensed as a pilot, with two caveats.** "First 20 in build order" is a mechanical rule pinned before any treatment data exists, so cherry-picking a favorable subset for the *paired difference* is impossible — **provably cherry-pick-free** in the Law #9 sense. **However:** (i) the first 20 are 15 planet-2hop + 5 planet-3hop, **0% elemental** (verified by building the bench) — the pilot is unrepresentative of the 60-item bench; (ii) the draft fences CONTINUE to "this scale on this bench" but lets KILL retire "the TTS axis for this task class" — an overclaim for a planet-only pilot. See FIX-4 (fence the KILL) and R1 (stratify). The draft's CPU-honesty justification for the cut (n=60 ≈ 32,640 tokens ≈ 4.5–9+ h, beyond the practical envelope) is checkable and honest. A full-n=60 run is correctly fenced as a separate pre-registered lane, not a re-run. **Pass with fixes.**

---

## 2. Is planning the ONLY cross-arm difference? [INTERPRETATION] — Pass

Executor and baseline share the **identical** sampling spec (temperature=0.7, top_p=0.9, max_new_tokens=48, pinned per-(item,index) seeds; seed streams 2000+10i+k vs 3000+10i+k are disjoint — no collision). The draft explicitly bars the greedy-executor-vs-sampled-baseline confound. The planner's greediness affects only outline *content* — it never touches the baseline arm, so it cannot confound the paired comparison; the planner's decoding choice is part of the treatment definition (and greedy is the lower-variance choice for a fixed treatment). The vote rule (majority of parseable votes, ties → C/foil) is applied identically per item per arm (§3.6). The planner arm's longer prompt context (outline text) is inherent to plan-conditioning — it *is* the treatment, as in the PTTS literature. **Pass, no fix.**

---

## 3. Generation-degeneracy defenses (the EXP108 lesson) [INTERPRETATION] — Pass with pinning fixes

The three-layer defense (per-arm ≥3 parseable votes; 20−n_valid ≥ 3 → RUN-INVALID; ≥50% unparseable vote-generations → RUN-INVALID) is sufficient against the EXP108 echo mode: the echo (`"\n\nQuestion:"` → first-alpha 'Q') is caught by the parse rule by construction, and 60/60-echo-scale failure trips the 50% wire. Four *identical* outlines are caught: dedup → 1 distinct < 2 → planner-invalid → item invalid → counted toward the elicitation gate. (Four distinct-but-vacuous outlines are a *weak* planner, not a degenerate one — measuring actual planner quality is the experiment's job, not a defect.)

Two pinning holes require fixes: the outline-extraction rule is ambiguous for preambles, repeated markers, and in-text "1." occurrences (FIX-2), and the parse rule doesn't pin "newly generated tokens only" (FIX-3). The EXP108 convention (parse new tokens only) exists in-program but is not stated. With those pinned, the defense is airtight. Note: base Pythia-410m is not instruction-tuned, so RUN-INVALID (apparatus failure) remains the modally likely outcome — the draft is honest that this is non-evidence, consistent with H1's handling. **Pass with fixes.**

---

## 4. Statistical honesty — is the pilot theater? [FACT] — No, but name the power honestly

Independent power simulation (20 items; (B,C) ~ independent binomials on discordant-pair rates; 20k trials per cell):

| True effect (per-item P(planner-only-right), P(baseline-only-right)) | P(CONTINUE) | P(HELD) | P(KILL) |
|---|---|---|---|
| null (0.05, 0.05) | 0.001 | 0.348 | 0.651 |
| large clean (0.30, 0.02) | **0.622** | 0.372 | 0.006 |
| moderate (0.15, 0.05) | 0.072 | 0.720 | 0.208 |
| small (0.10, 0.05) | 0.017 | 0.594 | 0.389 |

The pilot is a **big-effect-or-nothing screen**: it can CONTINUE (62% power on a large clean effect — not theater), is underpowered for moderate effects (which land honestly in HELD), and controls type-I error at ≈0.001 under the null (conservative by discreteness). The draft should state plainly that only large, clean effects (net ≥ +5/20 with zero reversals, i.e., ≥ +25pp one-directional) can CONTINUE — the HELD zone is doing real work here, not hedging. **Pass** — recommend adding the one-line power characterization to §4 (R3 below is not added; folded here as text the drafter may adopt verbatim).

---

## 5. Degrees of freedom — complete modulo the pinning fixes [INTERPRETATION]

The §5 registry covers bench/builder/provenance, n=20, both prompt templates (verbatim in §§3.3–3.5), planner generation spec, extraction rule, sampling spec + seeds, parse rule, arm-valid rule, vote rule + tie-break, budget definition, item-valid rule, global tripwire, backbone hash pin, determinism pins, metric, bars, and label hygiene. Missing or underspecified (all covered by FIX-1–FIX-3): the answer-to-option mapping (unstatable as written — FIX-1), the exact extraction algorithm (FIX-2), the new-tokens-only parse scope (FIX-3). The 2–3-outline executor behavior ("develop exactly those") is pinned in §3.4 body but absent from the table — add a row. **Pass with fixes.**

---

## 6. Laws audit [FACT]

- **Law #6 (frozen backbone):** hash pin `ec276abe…0ed` (LOG-331) recorded before/after; mismatch → RUN-INVALID + quarantine + no metric read. **Clean.**
- **Law #7 (zero leakage):** labels used only at metric time; planner/executor/baseline never see labels; the "first 20" rule is label-independent. **Clean by construction.** (Note: the prompts contain both entity names — that is task input, not label information; the *correct* name is never indicated.)
- **Law #9 (no cherry-picking):** pilot rule mechanical and pre-treatment-data; bench rebuilt verbatim via the signed builder; no new benchmark construction. **Clean.**
- **Law #13 (reproducibility):** seeds pinned per (item, index) on disjoint streams; determinism pins (eval/no_grad/cpu/float32) present; backbone hash pinned. **Clean modulo FIX-2/FIX-3** (extraction and parse scope must be deterministic as written).
- **Law #4 (no silent shifts):** post-hoc rewording → BARRED; no rescue runs; full-n=60 fenced as separate lane. **Clean.**
- **Law #10 (novelty):** N1 — Known Combination claimed with prior art cited. The PTTS citation (arXiv:2609.27374, Wu et al.) was **independently verified to exist** via arXiv: "Planned Test-Time Scaling with Coordinated Reasoning Paths," PTTS-ZS +6.7pp pass@64, planner-writes-outlines-in-one-pass with frozen executor — matching the dossier's description. The Meta FAIR 2609.26704 citation is dossier-carried, not independently verified by this lane. No fabrication found. **Pass.**
- **Law #14:** this review is the independent lane; the draft correctly states it is unsigned pending this lane. **Satisfied by this document.**

---

## 7. Overclaim guards [INTERPRETATION] — Pass with the KILL fence (FIX-4)

§8 correctly scopes CONTINUE (planning premium at this scale/bench only; not superintelligence/consciousness/generality; mechanism reading is interpretation), HELD (licenses nothing), template-generality (explicitly not claimed — the EXP107 lesson applied), and novelty (N1). The KILL reading ("the TTS axis is dead for this task class") needs the pilot-scope fence — FIX-4. **Pass with fix.**

---

## 8. Feasibility [FACT] — Pass

Arithmetic verified: per-item ceiling 160 + 4×48 + 4×48 = **544** tokens; 20 items → **10,880** tokens max; 9 generations/item × 20 = **180** generations. At the stated 0.5–1 s/token (stated explicitly as a checkable assumption for 410M-param fp32 CPU forward passes — credible, arguably conservative), wall time ≈ 1.5–3.0 h; the draft's "~1.5–3.5 hours" is consistent. $0, no GPU contact, no signed artifacts touched. **Pass.**

---

## Required fixes (all verifiable by exact quoted text in the repaired file)

**FIX-1 (substantive — construct validity of the answer protocol).** The prompt must communicate the response-to-option mapping to the model. Recommended repair: change the executor and baseline closing instruction to "Reply with the name of the higher-ranked entity and nothing else." and replace the parse rule with: "Decode the newly generated tokens only; strip whitespace and trailing punctuation (.,;:!?); case-insensitive compare against the item's two bench entity names (bench keys "A" and "C"): exact match → that entity is the vote; otherwise UNPARSEABLE." Labels become the target entity name (bench "A" key). The vote rule, McNemar machinery, (b,c) table, and all bars are unchanged; ties → foil entity. *Verification:* the repaired file's §§3.4–3.5 show the entity-name instruction and entity-name parse rule verbatim; no "single letter, A or C" instruction remains. (Alternative acceptable repair: letter-label the options in the question, e.g. "Who is higher in rank, (A) Mars or (C) Jupiter?" — but this amends the "{PROMPT} verbatim" pin and is the inferior option; the entity-name repair keeps {PROMPT} truly verbatim.)

**FIX-2 (required — deterministic outline extraction).** Replace the extraction rule with an exact algorithm, e.g.: "Scan the planner output left to right; record the first occurrence position of each literal marker `1.`, `2.`, `3.`, `4.`; for k=1..4, outline_k = the substring from the end of marker `k.` to the start of the next marker occurrence in position order (or end of output), stripped; text before the first marker (preamble) is discarded; a missing marker yields an empty outline; then drop empties and exact duplicates; planner-valid iff ≥ 2 distinct non-empty outlines remain; outline_idx for seeding is the 0-based position in the post-dedup list." *Verification:* §3.3 contains a rule covering preamble, repeated/in-text markers, and seed indexing with no residual ambiguity.

**FIX-3 (required — parse scope).** Pin: "The parse rule applies to newly generated tokens only (prompt tokens excluded), matching the EXP108 convention." Clarify the §3.8 tripwire denominator: "≥ 50% of executor + baseline vote-generations UNPARSEABLE" (planner generations are covered by the planner-valid rule, not the parse rule). *Verification:* §§3.5/3.8 state the new-tokens-only scope and the tripwire denominator explicitly.

**FIX-4 (editorial — deviation count).** §8 header says "two deviations"; there are three (budget clarification §3.7; decision-bar replacement §4; n=60→n=20 pilot scope §3.2/§7). Correct the header to three and list all three. *Verification:* §8 header reads "three deviations" with all three named.

**FIX-5 (required — KILL scope fence).** The KILL interpretation ("Planning adds nothing. The TTS axis is dead for this task class.") overclaims for a 20-item planet-only pilot. Fence it to the piloted scope, e.g.: "Planning adds nothing *at this pilot scale on this pilot bench*; the coordinator axis is retired for the piloted scope (a full-bench test remains a separate, unlicensed lane)." Apply identically in §4 and §6. *Verification:* the KILL rows in §§4/6 carry the pilot-scope fence; no unqualified "dead for this task class" remains.

## Recommendations (not required for SIGN)

**R1.** Stratify the pilot: "first 5 items of each of the 4 build blocks in build order" (planet-2hop, planet-3hop, element-2hop, element-3hop) — still mechanical and cherry-pick-free, but representative of the bench, unlike the current first-20 (15 planet-2hop + 5 planet-3hop, 0% elemental).

**R2.** Planner token budget: 4 outlines × ≤40 words ≈ 200+ tokens > max_new_tokens=160, so the planner will routinely truncate (likely losing outline 4 and inflating planner-invalid items). Either raise the cap (~220) or tighten the instruction (e.g., "30 words or fewer").

**R3 (text the drafter may adopt).** Add to §4: "Power characterization: the pilot is a big-effect-or-nothing screen — only large, clean effects (net ≥ +5/20 with zero compensating flips) can CONTINUE; moderate effects land in HELD by design."

---

## Boundary

This lane reviewed only. It does not fix the draft, approve execution, mint an experiment number, or dispatch follow-ups. The five required fixes must be applied by a repair lane and the fixed exact version must pass a re-review/fix-verification lane before any CEO launch decision. This lane stops here.
