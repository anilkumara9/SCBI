# EXP149 — Design Draft: EXP148 follow-ups (hop dose-response; cross-family generality within the EXP145 bound) — 2026-10-09

**Status: DESIGN DRAFT — NOT SIGNED. NOT EXECUTED.** Awaits independent Law #14 review + CEO sign + execution authorization. No forwards run. $0.

**Drafting lane:** EXP149 innovation-sprint design, 2026-10-09. **Experiment number EXP149 minted by the CEO** (LOG-4967) — new operationalization = new number per the single-lane fence; EXP148's CONTINUE verdict stands untouched.

**Parent context [FACT]:** EXP148 (S7-1 follow-up, J7) CONTINUE ADOPTED (LOG-4958/4959; independent verdict review ADOPT, LOG-4960): on frozen Pythia-410m, WRITE/READ prompting discipline beat budget-matched CoT by net +22.2pp (b=52, c=12, one-sided McNemar p=2.2833e-07, 95% Wald CI (0.1414, 0.3031)), with discipline verified delivered and budget-match verified. Mandatory caveats carried: S vs B net −0.2500 (direct answering still beats WRITE/READ); the gain is prompting discipline, not autonomous steering; single model, single bench. The Friday cull (LOG-4965) recorded the death-debt: EXP148's CONTINUE owes exactly two follow-up candidates — (a) hop dose-response, (b) cross-family generality within the EXP145 bound — new experiment number by CEO mint only.

**Governing laws:** Law #2 (every constant below is pinned, computed, or carried from a signed artifact — never improvised), Law #4 (no post-hoc hypothesis shifts; descriptive EXP148 stratum data is motivation, not a test target), Law #6 (Δθ=0), Law #7 (bench golds never touch prompts), Law #9 (primary registered here, before any new output is inspected — stratum breakdowns descriptive only), Law #11 (labels throughout), Law #13 (determinism), Law #14 (this draft awaits independent review — the review lane is separate), Law #15 (worth-it gate §1 of the pre-reg draft).

**Epistemological labels** per `~/workspace/SCBI/AGENTS.md` §5 are load-bearing below. [NOTE] and [CAVEAT] mark operational clarifications.

---

## 0. Licensed scope [DEFINITION]

EXP149 tests exactly the two death-debt candidates from LOG-4965:

- **(a) Hop dose-response:** does the WRITE/READ vs budget-matched CoT gain grow with hop count (2-hop vs 3-hop)?
- **(b) Cross-family generality within the EXP145 bound:** does the prompting-discipline gain replicate on frozen GPT-2-small?

**What EXP149 does not do:** it does not re-litigate EXP148 (the parent CONTINUE stands regardless of what fires here — a KILL here *scopes* the parent verdict, never overturns it); it does not re-open EXP145's KILL/PIVOT (the shared-direction decodability instrument stays dead); it licenses no Gap-generality claim, no autonomous-steering claim, no claim about other families or scales; it does not touch the paper.

---

## 1. The EXP145 bound (one paragraph) [FACT]

EXP145's KILL/PIVOT (LOG-4925/4926) bounded the *Decodability Gap's shared-direction instrument* to Pythia-scale: on frozen GPT-2-small, the decodability instrument decoded (D1 PASS — layers 8 and 10 significant) but the shared-direction instrument failed (D2: mean shared-direction cosine −0.4587 vs the 0.70 bar), so the decode+ precondition is absent in GPT-2-small; the outcome cannot separate an architecture effect from scale/bench-fit, and the dissociation itself remains untested in that family. EXP149 tests a **different object** — an inference-time prompting-discipline *capability gain*, not a decodability direction — so it re-opens nothing: candidate (b)'s generality claim is scoped to the WRITE/READ discipline effect and stands or falls on its own pre-registered bars, with EXP144's bench-portability lesson enforced by a binding Step-0 portability gate (§5.4 of the pre-reg). No Gap-generality claim is licensed by anything in EXP149.

---

## 2. Candidate (a): hop dose-response

**[HYPOTHESIS]** The WRITE/READ discipline advantage over budget-matched CoT scales with reasoning depth: net(S−C) at 3-hop exceeds net(S−C) at 2-hop — δ̂_3 − δ̂_2 > 0.

**Why this is risky [INTERPRETATION]:** EXP148's descriptive stratum nets point the *other* way — compositional-2hop +0.4667 vs 3-hop +0.1333; transitive-2hop +0.2444 vs 3-hop +0.0444 — so a monotone-increasing dose-response is not what the prior data suggests. That is the point: a risky pre-registered directional prediction that can die cleanly. If the gain is headroom-driven (largest where the B baseline is weakest) rather than depth-driven, the breaking point should fire.

**Honest prior-data statement [OBSERVATION]:** the EXP148 stratum pattern is prior *descriptive* data (never a guard, never a verdict input). Candidate (a) runs on a **fresh bench** built by the same templatic procedure, so there is no post-hoc stratum fishing (Law #9). The stratum numbers motivated the question; they are not the test.

**Breaking point:** δ̂_3 − δ̂_2 ≤ 0 with both per-level apparatuses powered and delivered → **KILL** the dose-response claim (the discipline gain does not grow with hops; EXP148's CONTINUE stands as a pooled effect, not a depth effect).

**Design:**
- Fresh bench, same templatic construction procedure as EXP147/148 (§5.1 of the EXP148 pre-reg: 40-name entity pool, templatic items, every gold a single entity token appearing ≥2×, exemplar entity-disjointness), new construction seed registered at execution (≠ 7101). Bench pin recomputed character-identical at Step 0 (guard (c)).
- Two hop levels (2-hop, 3-hop), each with two strata (transitive, compositional) like the parent bench: **n = 380 per hop level** (2 strata × 190).
- Arms: B (direct-answer, T_B=15), C (budget-matched CoT, T=120), S (WRITE/READ, T=120) — prompts and exemplar rules carried verbatim from the EXP148 pre-reg §5.2 (exemplars: reuse EXP148's Step-0-pinned exemplar file byte-identical; else rebuild by S7-1 §5.2 and record the new pin).
- Scoring: first-token scoring, EXP148 pre-reg §5.3 verbatim (C/S: first normalized token after the last `ANSWER:`; no `ANSWER:` → 0; no LLM judge).
- 4-hop: **exploratory only**, admitted solely if the pre-registered Step-0 throughput trigger is met (guard (h) at Step 0 projects the 2-level run at ≤ 48h wall [ASSUMPTION — registered]) [Fixes D4, A2]; then analyzed with the pre-registered Jonckheere–Terpstra trend test over {2,3,4} (4-hop stratum breakdowns descriptive only, Law #9 [Fix A5]). If the trigger is not met, 4-hop is neither built nor analyzed — the omission is logged, not revisited.

**Power (pre-registered, computation at Step 0):** primary statistic is the difference of two independent S−C nets. Under the S7-1/EXP148 Wald convention, per-level SE ≈ √[(d − net²)/n]; EXP148 realized SE = 0.0412 at n=180 (b=52, c=12). SE(δ̂_3 − δ̂_2) ≈ √[(d−net²)(1/n_3 + 1/n_2)]. At d ≈ 0.30–0.36 and n = 380/level: SE_diff ≈ 0.0370–0.0410 (recomputed from the formula; full table in the pre-reg draft §2.1 [Fix D1]). Detecting δ = +0.10 at one-sided α = 0.05 needs z ≥ 2.487 (1.645 + 0.842) → **≈0.83–0.86 power at d ≤ 0.32**, ≈0.79 at d = 0.36 [INTERPRETATION]. **Pre-registered power rule:** the execution lane computes registered Wald-formula power at Step 0 from the registered discordant-pair rate (20-item C+S pilot rate; see pre-reg §2.1); if registered power < 0.80 for δ = +0.10, n per level is raised by the registered formula (n = smallest even integer with registered power ≥ 0.80), and the raised n re-asserts guards (g)/(h) — STOP/HELD at design cost if breached [Fixes D5, D8]. A computation, not a choice (Law #2). **KILL-bar operating characteristic:** under δ = 0, P(CI entirely ≤ 0) = 0.025 (design fails safe: the remaining ~97.5% is HELD, never false-CONTINUE); under true δ = +0.10, false-KILL < 1e-4; under true δ = −0.10 (reverse dose-response), P(KILL fires) ≈ 0.77 [Fix D2].

**Decision table, candidate (a) (binding). Precedence: RUN-INVALID > HELD > KILL > CONTINUE:**

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | 95% CI for (δ̂_3 − δ̂_2) entirely above 0 AND 3-hop S−C one-sided McNemar (H1: S>C) p < 0.05 | Dose-response supported: the discipline gain grows with reasoning depth |
| KILL | 95% CI for (δ̂_3 − δ̂_2) entirely ≤ 0, with per-level guards (d),(e),(f),(f′) PASS | Dose-response dead: the gain does not grow with hops; it is pooled/headroom-driven. EXP148's CONTINUE stands — as a pooled effect, not a depth effect |
| HELD | Anything else (CI too wide, any per-level guard (d) or (f′) trips) | Inconclusive — licenses nothing, kills nothing |
| RUN-INVALID | Any apparatus guard (a)/(c)/(e)/(f)/(g)/(h) trips (per-level) | Apparatus failure — never a verdict |

Stratum (transitive/compositional) breakdowns inside a level are **descriptive only** (Law #9 — no post-hoc fishing); no stratum is promoted to a decision.

---

## 3. Candidate (b): cross-family generality within the EXP145 bound

**[HYPOTHESIS]** The WRITE/READ discipline advantage over budget-matched CoT is not Pythia-specific: on frozen GPT-2-small, S vs C one-sided McNemar (H1: S>C) p < 0.05 AND net δ̂ ≥ +0.10 → CONTINUE (generality supported, scoped to these two families).

**Breaking point:** the EXP148 KILL conjunction mirrored on GPT-2-small — (i) one-sided p ≥ 0.1 AND (ii) two-sided p ≥ 0.1 AND (iii) 95% CI upper < +0.10, with guards (d),(e),(f′) PASS → **KILL** the generality claim: the discipline gain does not transfer to GPT-2-small; EXP148's capability entry stands as Pythia-scale.

**Scope fence [DEFINITION]:** candidate (b) tests prompting-discipline generality **only**. It re-opens nothing from EXP145, licenses no Gap claim, no steering claim, no claim about other families or scales. [CAVEAT]: a KILL here does not say *why* the gain failed to transfer (architecture vs scale vs bench-fit — the EXP145 §1 steelman applies symmetrically); it only records the scoped non-transfer.

**Apparatus risk — the EXP144 lesson [ASSUMPTION]:** GPT-2 BPE may split gold entity tokens (the bench was built under Pythia tokenization), and GPT-2-small's format-following may degrade WRITE-span delivery. → **Binding Step-0 portability gate** (precedes the full run for (b)):
- **(p1) Tokenizer portability:** fraction of bench golds that are single tokens under GPT-2 BPE ≥ 0.95 [ASSUMPTION — registered] → else STOP.
- **(p2) Calibration portability:** B-arm first-token accuracy on a fresh 20-item subset ∈ [0.2, 0.8] [ASSUMPTION — registered] → else STOP.
- **(p3) Delivery portability:** WRITE-span regex rate on a 20-item S-arm pilot ≥ 0.50 [ASSUMPTION — registered] → else STOP.

Failing (p1)/(p2)/(p3) → candidate (b) **STOPS at design cost (~2,700 forwards: 20×15 B-pilot + 20×120 S-pilot [Fix D3]), logged HELD** — a measurement boundary (EXP147 precedent), which licenses nothing and kills nothing. A portability failure is never relabeled as a KILL.

**Bench:** the EXP148 bench byte-identical (pin `2b055b53127a241b72338a82373c3efc7b666256e25d8c584d45989278c14dcf`, recomputed 64/64 at Step 0) **if** (p1) passes. If (p1) fails, the execution lane rebuilds the bench by the EXP147 §5.1 procedure with a GPT-2-BPE-safe entity pool (single-token golds under GPT-2 BPE by construction), new seed registered at execution, new pin recorded — pre-registered here as the (p1)-fail branch, not a choice.

**n:** 180 items (45 × 4 strata, mirror of EXP148) — same scoring, same test, so the S7-1/EXP148 power license transfers unchanged (MDE80 ≈ +10pp at d ≤ 0.30; KILL fires 65–88% under null; false-KILL < 3% at +10pp; false-CONTINUE ≤ 0.035). Guards (a),(d),(e),(f),(f′),(g),(h),(u0) mirror EXP148 §5.4. Model revision resolved programmatically at Step 0 from the local cache — EXP145's carried pin `607a30d783dfa663caf39e06633721c8d4cfcd7e` is the expectation, re-resolved not transcribed (Law #2).

---

## 4. Feasibility analysis — CPU vs gated [FACT for cache state; wall-time figures are [INTERPRETATION] projections, re-gated at Step 0 per guard (h)]

- **No downloads, no HF contact at execution:** Pythia-410m cached at `~/.cache/huggingface` (1.3G; EXP148 ran from it, no run-local cache). GPT-2-small cached at `experiments/runs/EXP145/hf_cache` (5.3G; EXP145 ran it on CPU). Model revisions pinned at Step 0 from cache.
- **Candidate (a):** 760 items × 3 arms = 2,280 arm-records ≈ 193.8k generation forwards + ≈ 300 B dry-run + 4,800 C+S pilot = 198.9k → guard (g) ≤ 200k forwards (pre-registered; vs EXP148's 50k) [Fix D8]. At EXP148's rate (~13.9 s/arm-record on 2 threads): **≈ 8.8h CPU** — under guard (h) ≤ 72h. **Not GPU-gated.**
- **Candidate (b):** 540 arm-records ≈ 45.9k forwards + ≈ 2.7k portability pilots = 48.6k → guard (g) ≤ 50k [Fix D3]. **≈ 2.1h CPU.** **Not GPU-gated.**
- **Δθ=0 throughout; no fine-tuning; no new families beyond GPT-2-small for (b); no new scales for (a) (Pythia-410m only).** Both candidates are CPU-executable at $0. Nothing in EXP149 touches the GPU queue.

---

## 5. Falsification-first summary [INTERPRETATION]

The two riskiest pre-registered claims are deliberately the licensed ones: (a) a monotone dose-response that the prior descriptive data leans *against*; (b) generality to GPT-2-small that the EXP145 bound and EXP144's portability lesson lean *against*. A KILL on either is a sharp, informative boundary — it would show the discipline gain is pooled (not depth-driven) or Pythia-scale (not family-general) — while a CONTINUE would extend the program's first capability entry in a real, risky direction. Both candidates carry honest HELD outcomes for apparatus/measurement failure, so a bad bench can never be laundered into a verdict. EXP148's CONTINUE is not re-litigated: whatever fires in EXP149 *scopes* it; nothing overturns it.

---

## 6. Open items for the independent Law #14 review

1. Power rule: is the Step-0 exact-power recomputation + registered n-raise rule (candidate (a)) sufficiently mechanical to satisfy Law #2?
2. The (p1)/(p2)/(p3) portability gate for (b): are the three trip conditions (0.95 / [0.2,0.8] / 0.50) registered assumptions, or do any need justification?
3. The 4-hop exploratory trigger (≤48h projection at Step 0): acceptable as a pre-registered apparatus trigger, or does it invite fishing?
4. Cross-family claim scope: does the §1 bound statement adequately fence candidate (b) from re-opening EXP145?
5. The §2 KILL-bar: is "CI entirely ≤ 0" the right bar for killing a *growth* claim, or should the review demand a two-sided equivalence band?

---

*Design draft completed 2026-10-09. Status: DESIGN DRAFT — REPAIRED PER LAW #14 REVIEW, STILL NOT SIGNED. NOT EXECUTED. No forwards run. Companions: `EXP149_PREREG_DRAFT_2026-10-09.md` (pre-registration draft in program format). Independent Law #14 review completed 2026-10-09 (SIGN-WITH-FIXES on both drafts); 7 binding defects repaired by the repair lane; awaited: CEO sign → execution authorization (dry runs first).*

---

## Fixes applied — Law #14 review repair lane, 2026-10-09

**Status after repair: repaired per the independent review's exact prescriptions (`EXP149_LAW14_REVIEW_2026-10-09.md`). STILL NOT SIGNED — signing is the CEO's act after diff-level re-verification. NOT EXECUTED. No design, hypothesis, guard, or decision-bar change was made; all fixes are numeric/expositional.**

- **D1:** §2 power narrative corrected from the formula SE(δ̂_3−δ̂_2) ≈ √[(d−net²)(1/n_3+1/n_2)] — SE_diff ≈ 0.0370–0.0410; ≈0.83–0.86 power at d ≤ 0.32, ≈0.79 at d = 0.36; power rule updated to the registered Wald-formula power (pre-reg §2.1). (Independently re-verified this lane.)
- **D2:** reverse dose-response P(KILL fires) added as ≈0.77 (was unstated in this draft). (Independently re-verified this lane.)
- **D3:** study (b) portability-pilot cost ≈600 → **≈2,700** forwards; guard (g) margin re-asserted (48.6k ≤ 50k). (Independently re-verified this lane.)
- **D4:** 4-hop trigger reconciled to the pre-reg's registered wording (guard (h) at Step 0 projects the 2-level run at ≤ 48h wall).
- **D5:** pre-reg rule cross-referenced — any n-raise re-asserts guards (g)/(h), STOP/HELD at design cost if breached.
- **D8:** power rule cross-references the pre-reg's pinned method (20-item C+S pilot d_pilot; EXP148 d = 0.3556 first-block keying); study (a) design cost updated (198.9k ≤ guard (g) 200k).
- **D9:** n/a — this draft has no (p1)-fail branch text of its own; the pre-reg's branch now registers the re-verification.
- **A2:** [ASSUMPTION — registered] tags added to the (p1)/(p2)/(p3) trip thresholds and the 48h guard.
- **A3:** §4 header label corrected — [FACT] retained for cache state; wall-time figures are now explicitly [INTERPRETATION] projections, re-gated at Step 0 per guard (h).
- **A5:** 4-hop stratum descriptive-only rule carried explicitly (Law #9).
- **A1, A4:** advisory notes only — no changes made (A1's PIVOT reading is carried verbatim from EXP148's pre-reg §3 per the registered carry rule; A4 is registered and was noted, not objected). Both flagged for CEO discretion.
