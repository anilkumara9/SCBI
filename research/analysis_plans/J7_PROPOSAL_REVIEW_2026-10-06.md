# Independent Law #14 Review — J7 Proposal Draft (LOG-4954)

**Reviewer:** Independent Scientific Reviewer (Law #14), 2026-10-06.
**Artifact reviewed:** `research/analysis_plans/J7_PROPOSAL_DRAFT_2026-10-06.md` (DRAFT, LOG-4953).
**Review lane:** LOG-4954 (CEO pre-assigned). The reviewer did not draft the proposal and reports no one but the record.
**Verdict: SIGN.**

This review attempted to falsify the proposal's design. It could not. The proposal is sound and may proceed to the CEO for the minting decision (new experiment number, final pre-registration, execution authorization — all still CEO-gated, none licensed by this review).

---

## 1. Verification of pinned numbers [FACT]

Every quantitative claim in the draft was checked against the committed EXP147 artifacts:

| Draft claim | Committed source | Result |
|---|---|---|
| First-token B = 119/180 = 0.6611 | `EXP147_RESULTS_2026-10-05.json`: `descriptive_first_token_correct: 119`, `descriptive_first_token_accuracy: 0.6611` | ✅ exact |
| Compositional 2-hop 44/45 = 0.9778 | per-stratum `compositional-2hop: 0.9778` | ✅ exact |
| Compositional 3-hop 43/45 = 0.9556 | per-stratum `compositional-3hop: 0.9556` | ✅ exact |
| Transitive 2-hop 12/45 = 0.2667 | per-stratum `compositional-2hop` analog `transitive-2hop: 0.2667` | ✅ exact |
| Transitive 3-hop 20/45 = 0.4444 | per-stratum `transitive-3hop: 0.4444` | ✅ exact |
| Registered B = 0/180 = 0.0000 | `b_correct_registered: 0`, `b_accuracy_registered: 0.0` | ✅ exact |
| Bench pin `2b055b53…dcf` (64 hex) | `bench_pin` field, character-compared | ✅ identical |
| Guard (d) band [0.2, 0.8], tripped | `guard_d_band: [0.2, 0.8]`, `guard_d_tripped: true` | ✅ exact |
| Dry-run false-fail ≈ 5.5% | Independently recomputed: X ~ Bin(20, 0.6611), P(X≤3) ≈ 3.7e-6, P(X≥17) ≈ 0.0546, total ≈ 0.0546 | ✅ correct |
| Model revision `9879c9b5…e9d4f` | EXP147 verdict §5, 40-hex | ✅ matches |

No invented numbers. No transcription errors. Law #2 holds.

## 2. Worth-it gate — crisp and correctly gated

The KILL/CONTINUE/PIVOT/HELD table is inherited verbatim from the signed S7-1 plan (verified against `S7-1_PREREG_DRAFT_2026-10-05.md` §4 — no drift). The decision is crisp: a powered null kills J7; a ≥+10pp S−C effect with p < 0.05 continues it as the program's first capability entry.

The 20-item dry-run break point is the right gate, and it is correctly calibrated:
- It tests the actual repair (does first-token scoring produce a measurable baseline?), not a proxy.
- The 5.5% false-fail rate under the n=180 point estimate means it is a real apparatus check (catches scoring-pipeline bugs, which would produce systematically wrong scores) without being a gamble.
- It kills bad designs at ~300 forwards, not ~46k. This is the cheapest discriminative gate available.
- It does not kill good designs: a 94% pass rate under the estimate is an acceptable gate risk, and a fail is itself informative (it would indicate the n=180 descriptive estimate doesn't transfer to fresh subsets — a finding, not just a cost).

## 3. First-token scoring — valid repair, no smuggled confound

The reviewer's hardest challenge was here: does changing the scoring change what "beating CoT" means?

**Finding: no.** The J7 hypothesis (S7-1 §0) is about *reasoning capability* — whether WRITE/READ discipline grows multi-hop capability. The registered S7-1 scoring conflated two things: (a) did the model reason to the right answer, and (b) did it obey "answer with the name only." EXP147 proved (b) fails on base Pythia independently of (a) — the model emits the right name first, then rambles. First-token scoring isolates (a). This is a *cleaner* operationalization of the hypothesis, not a different hypothesis.

Symmetry holds: every arm is scored on "the answer the model committed to first" (B: first token of generation; C/S: first token after the last `ANSWER:`). The C/S arms do their reasoning before `ANSWER:`, so the scored token is post-reasoning in all arms. No arm gets a structural advantage from the scoring change.

The draft's rejection of (b) stop-sequence is correct (fragile on base LMs; 1-token truncation *is* first-token scoring — the drafter spotted the identity). The deferral of (c) instruct-tuned model is correct (breaks the comparability chain; properly held as the next proposal if (a) fails).

## 4. Power license — transfers honestly

McNemar power depends on discordant-pair parameters (q, r, d), not on marginal accuracy — the draft is correct that these are scoring-agnostic. The draft does not assume d; it spans d ∈ [0.20, 0.35] and states the residual uncertainty. This is the honest form of the license.

The draft discloses the compositional-stratum ceiling (0.96–0.98) and keeps the pooled primary (Law #9 — no post-hoc stratum fishing). The reviewer notes the ceiling makes the design *conservative*: if compositional items contribute ~0 discordant pairs, the S−C comparison is effectively powered on transitive items, widening CIs and biasing toward HELD rather than toward false KILL or false CONTINUE. A design that fails safe toward "licenses nothing" is acceptable in a falsification-first program. This is an advisory, not a defect — the draft already discloses the mechanism.

## 5. Law #9 — no cherry-picking

The repaired scoring is registered in this proposal *before any new model output is inspected*. The EXP147 descriptive first-token numbers are explicitly labeled as prior observations, not tuning targets — and indeed they cannot be tuning targets for C/S, because the C and S arms were never run in EXP147 (confirmed: `arms_not_run` in the committed results; the verdict's §2 states "Arms C and S not run"). There is no unrun data to peek at. The primary metric (pooled per-item correctness, McNemar on S−C) is fixed before the fact. Law #9 holds.

## 6. What the drafter got right that a weaker draft would have missed

- The bench pin is reused, not rebuilt — the bench is correctly identified as an asset, not part of the failure.
- The dry-run subset uses a fresh seed distinct from bench-construction seed 7101 — no overfitting to the specific 180.
- Guard (d) is re-applied to the *repaired* baseline, not waived — the calibration discipline survives the repair.
- The proposal does not touch the v102 paper, any killed lane, or EXP147's HELD verdict. New number at execution, per the single-lane fence.
- Open question #4 (T=120 tightness for 3-hop scratchpads) is inherited unresolved rather than silently fixed — honest.

## 7. Advisories (non-blocking)

These do not affect the SIGN verdict but should be considered at final pre-registration:

**(i) C/S scoring pipeline hardening.** The 20-item dry run is B-only, so it exercises the B scoring path ("first normalized token") but not the C/S path ("first normalized token after the last `ANSWER:`"). A bug in the `ANSWER:` parsing (case sensitivity, whitespace variants) would not be caught until the full run. Cheap fix at Step 0: a 5-line unit test asserting the C/S scoring function correctly extracts from a synthetic string containing `ANSWER:`. Cost: zero forwards.

**(ii) Exemplar pinning clarity.** §4 says "exemplars re-pinned at Step 0 by the same construction procedure." To avoid ambiguity between *reusing* EXP147's Step-0-pinned exemplars and *rebuilding* them, the final pre-registration should state explicitly: "reuse the EXP147 Step-0 exemplar file byte-identical; if unavailable, rebuild by the S7-1 §5.2 procedure and record the new pin."

**(iii) Effective-n disclosure.** At final pre-registration, consider adding one sentence to the power section noting that if compositional strata contribute ~0 discordant pairs under first-token scoring, the S−C comparison is effectively powered on the transitive strata, and the stated power figures are therefore upper bounds. The design remains valid (it fails safe toward HELD); this is documentation, not redesign.

## 8. Verdict

**SIGN.** The proposal is sound: numbers verified, math verified, decision bars crisp, worth-it gate correctly calibrated, Law #9 respected, honest caveats carried. The first-token scoring repair is a valid operationalization of the J7 hypothesis, not a confound. The dry-run gate kills bad designs cheaply without gambling good ones.

The proposal may proceed to the CEO for: (a) the minting decision (new experiment number), (b) final pre-registration (addressing advisories (i)–(iii) at the drafter's discretion), and (c) execution authorization. None of these are licensed by this review.

---

*Review conducted 2026-10-06 under Law #14 (Challenge Rather Than Defend). The reviewer examined the draft, the EXP147 verdict, the S7-1 signed plan, and the committed EXP147 results JSON, and recomputed the draft's binomial claim independently. No model forwards were run. No files were modified except this review and the LOG-4954 entry.*
