# J7 Follow-up — PROPOSAL DRAFT: First-token scoring repair for the writable-memory-in-context test (new experiment, not a repair of EXP147)

**Status: DRAFT — NOT SIGNED, NOT PRE-REGISTERED.** No independent Law #14 review commissioned. No experiment number minted. No execution licensed. This draft proposes; it does not authorize.

**Drafting lane:** J7 follow-up proposal, LOG-4953 (CEO pre-assigned, 2026-10-06). Licensed by EXP147's HELD verdict (LOG-4946/4947), which explicitly authorizes "a new proposal and experiment number using a repaired baseline measurement" — never a repair of EXP147.

**Parent context [FACT]:** EXP147 (S7-1, J7) HELD on 2026-10-05: guard (d) tripped — B-arm accuracy 0/180 = 0.0000 under the registered scoring (full generation → normalize → exact match), outside the [0.2, 0.8] calibration band. The verdict's descriptive diagnosis [OBSERVATION]: this is a **format-compliance floor, not a capability floor** — base Pythia-410m emits a candidate name as its first generated token, then rambles for the remaining budget (0/180 generations were short). First normalized token == gold on **119/180 = 0.6611** (compositional 2-hop 44/45 = 0.9778; compositional 3-hop 43/45 = 0.9556; transitive 2-hop 12/45 = 0.2667; transitive 3-hop 20/45 = 0.4444). The bench elicits the target reasoning; the **measurement apparatus** failed. Arms C and S were not run (~2,700 generation forwards spent, $0 CPU). The J7 hypothesis — whether WRITE/READ prompting beats budget-matched CoT — remains **untested, not killed**.

**Governing laws:** Law #2 (every constant below is pinned, computed, or carried from a signed artifact — never improvised), Law #4 (no post-hoc shifts — the S7-1 decision bars are inherited verbatim, not re-read), Law #6 (Δθ=0), Law #7 (bench golds never touch prompts), Law #9 (the repaired scoring below is registered here, before any new output is inspected — the EXP147 descriptive first-token numbers are prior observations, not a tuning target), Law #11 (labels throughout), Law #13 (determinism), Law #15 (worth-it gate §1).

**Epistemological labels** per `~/workspace/SCBI/AGENTS.md` §5 are load-bearing below.

---

## 0. The question (unchanged from S7-1)

**[HYPOTHESIS]** A standard frozen transformer can simulate writable key–value memory in context: explicit WRITE/READ prompting discipline lets it externalize intermediate deductions as discrete tokens and re-attend to them, growing multi-hop capability without new architecture — beating budget-matched chain-of-thought.

**Breaking point (inherited from S7-1 §0, unchanged):** On the powered design (n=180), the scratchpad arm shows no advantage over budget-matched CoT (one-sided McNemar p ≥ 0.1, 95% CI for the net rate excluding +10pp) with the discipline verified delivered (guard (e)) and the budget-match comparability verified (guard (f′)) → **KILL** the J7 hypothesis. The missing ingredient is architectural, not disciplinary.

---

## 1. The repair: evaluation of candidate baseline measurements

EXP147's failure was scoring-only: full-generation exact match on a base LM that does not respect "answer with the name only." Three candidate repairs evaluated:

### (a) First-token scoring [RECOMMENDED]

**Definition:** B arm — take the full generation, normalize (lowercase, strip punctuation, collapse whitespace, identical to S7-1 §5.3 step 2), take the FIRST whitespace-delimited token, exact match vs normalized gold → 1 else 0. C/S arms — take text after the LAST occurrence of `ANSWER:`, normalize, take the FIRST whitespace-delimited token, exact match vs gold → 1 else 0; no `ANSWER:` → 0 (unchanged from S7-1).

**Evidence [OBSERVATION — from EXP147's committed per-item records, not new data]:** first-token B accuracy = 119/180 = 0.6611, inside the [0.2, 0.8] calibration band. Golds are single entity tokens from the closed 40-name pool [FACT — bench construction], so first-token comparison is well-defined.

**Why it wins:**
1. Empirically grounded on the actual bench and model — not a guess.
2. Minimal delta: same model, same bench (pin `2b055b53127a241b72338a82373c3efc7b666256e25d8c584d45989278c14dcf` reused — the bench is an asset, not part of the failure), same prompts, same budgets. Only the scoring function changes. The full Law #14 review investment in the S7-1 plan is preserved.
3. Symmetric across arms: every arm is scored on "the answer the model committed to first."
4. Measures the reasoning outcome, not format compliance — the J7 question is about reasoning.

**Honest caveat [INTERPRETATION]:** compositional strata sit at 0.96–0.98 under first-token scoring — near ceiling, little headroom for S/C gains there. The detectable J7 effect (if real) must come substantially from transitive strata (0.267, 0.444 — good headroom) or the pooled comparison. The PRIMARY verdict stays pooled (Law #9 — no post-hoc stratum fishing); stratum breakdowns are descriptive only. If the true effect is compositional-only, this design is underpowered for it — stated, not hidden.

### (b) Stop-sequence / truncation + exact match [REJECTED]

Strictly dominated by (a). Stop sequences are fragile on base LMs (EXP147: 0/180 generations were short; a `\n` stop may never fire, returning to full-generation scoring = 0/180). Truncation to 1 token **is** first-token scoring; truncation to 2–3 tokens reintroduces the rambling ("Fweep is" ≠ "Fweep"). More moving parts, more failure modes, zero additional information.

### (c) Instruct-tuned model instead of base Pythia-410m [DEFERRED]

Legitimate but heavier. It changes the model: breaks the comparability chain to EXP147's descriptive findings and the program's Pythia-410m kill boundary; requires re-pinning a new model revision and re-validating the bench. The J7 question ("can prompting discipline simulate writable memory in a frozen transformer") does not logically require a base model — Δθ=0 holds for a frozen instruct-tuned model too — but the minimal repair keeps the model fixed. **(c) becomes the licensed next proposal only if (a) fails the §2 dry run**, i.e., if the base LM proves unmeasurable for this question class even with repaired scoring.

---

## 2. Worth-it gate (Law #15)

1. **Exact question [HYPOTHESIS]:** §0 — does explicit in-context WRITE/READ discipline beat budget-matched CoT on multi-hop reasoning at Δθ=0, measured with a working baseline?
2. **Decision changed** (S7-1 §4 inherited verbatim):
   - **CONTINUE:** S vs C one-sided McNemar p < 0.05 AND net δ̂ ≥ +10pp → the program's first capability entry; writable-memory-in-context lives.
   - **KILL:** S vs C (i) one-sided p ≥ 0.1 AND (ii) two-sided p ≥ 0.1 AND (iii) 95% CI upper < +0.10, with guards (e) and (f′) PASS → discipline adds nothing; J7 dead; the Δθ=0 capability question pivots to architecture (Spotlight's direction).
   - **PIVOT:** KILL fires AND S vs B one-sided p < 0.05 → test-time compute helps, discipline doesn't.
   - **HELD:** anything else. **RUN-INVALID:** guard (a)/(c)/(e)/(f)/(g)/(h) trips.
3. **Cheapest test:** the S7-1 design with exactly one substantive change (the §1(a) scoring repair). n=180 × 3 arms (B: T=15; C, S: T=120 budget-matched), frozen Pythia-410m (`9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`), greedy, Δθ=0. Preceded by the §3 dry run.
4. **Cost:** $0 CPU. ≈46k generation forwards + 540 prompt encodings (guard (g) ≤ 50k, unchanged) + ≈300 dry-run forwards. Wall-time re-gated at Step 0 (guard (h) ≤ 72h).
5. **Mathematical license:** S7-1 §1.5(a)–(d) inherited unchanged (content-addressable attention [CONJECTURE]; WRITE/READ discipline definition; binding-degradation routing-around [CONJECTURE]; budget-matched CoT control [DEFINITION] with guard (f′) earning the "budget-matched" label).
6. **Quantitative prediction:** if J7 holds at decision-relevant scale: S − C ≥ +10pp net (one-sided McNemar p < 0.05 at n=180). If the breaking point holds: S − C ≈ 0 with discipline delivered. Power license transfers from S7-1 §2 (MDE80 ≈ +10pp at d ≤ 0.30; KILL fires 65–88% under null; false-KILL < 3% at +10pp) — stated in discordant-pair parameters (q, r, d), which are scoring-agnostic. [CAVEAT]: the true d under first-token scoring is unknown; the §2 table spans d ∈ [0.20, 0.35] rather than assuming it. If the dry run suggests extreme discordance, n is revisited — as a new proposal matter, not in this draft.
7. **Breaking point:** §0. Plus the **dry-run gate (§3)**: the proposal dies at design cost if the 20-item dry run does not lift the repaired baseline into [0.2, 0.8].

**Why this is worth doing [INTERPRETATION]:** the program's kills say static geometric injection does not steer standard frozen transformers; the open summit-adjacent question is whether the missing ingredient for Δθ=0 capability growth is architectural (Spotlight) or disciplinary (prompting). EXP147 left this untested. A clean KILL sharpens the boundary (discipline doesn't do it → architecture is the direction). A CONTINUE is the program's first capability entry. Both outcomes are informative; a second HELD would itself license the instruct-tuned-model proposal (repair (c)).

---

## 3. Dry-run break-point protocol (binding on the proposal)

Before any full run, a 20-item dry run: fresh random 20-item subset of the EXP147 bench (seed registered at execution, distinct from bench-construction seed 7101), B arm only, T_B=15, greedy, §1(a) first-token scoring.

- **Pass:** B accuracy ∈ [0.2, 0.8] → full run licensed (pending Law #14 review of the final pre-reg).
- **Fail:** → proposal dies at design cost (~300 forwards). No full run. The dry-run outcome is reported; repair (c) becomes the next candidate proposal.

[FACT — exact binomial]: under the n=180 point estimate (p=0.6611), P(20-item accuracy ∉ [0.2, 0.8]) = P(X ≤ 3) + P(X ≥ 17) ≈ 0 + 0.055 ≈ **5.5%** (X ~ Bin(20, 0.6611)). The gate is a real apparatus check (catches scoring-pipeline bugs, which would produce systematically wrong scores) without being a gamble — it passes ~94% of the time if the n=180 estimate holds.

---

## 4. Design deltas vs the signed S7-1 plan (complete list)

The ONLY substantive change is the scoring function (§1(a)). Everything else is carried forward unchanged: the bench (same pin), the three arms and prompt templates (S7-1 §5.2, exemplars re-pinned at Step 0 by the same construction procedure), all eight guards (a)–(h) with guard (d) now applied to first-token B accuracy, the decision table (§4), the power analysis (§2), the cost envelope, and the determinism requirements (Law #13).

## 5. What this proposal does not do

- It does not repair, reopen, or re-read EXP147 (HELD verdict stands; new number at execution authorization).
- It does not change the model, the bench, the prompts, the budgets, or the decision bars.
- It does not touch the v102 paper or any killed lane.
- It does not license execution — a Law #14 review of the final pre-registration and CEO execution authorization are still required.

## 6. Open questions for the Law #14 reviewer (when commissioned)

1. Is first-token scoring a faithful operationalization of "the model's answer," or does it smuggle in a capability assumption (that the first token is the committed answer)? The draft's position: EXP147's data (model "almost always emits a name first") supports it; the symmetric application across arms contains the risk.
2. Does the compositional-stratum ceiling (0.96–0.98) warrant a stratum-reweighted primary analysis? The draft's position: no — pooled primary stands (Law #9); the ceiling is disclosed, not designed around.
3. Is the 20-item dry run sufficient as the break point, or should it also check C-arm ANSWER:-format compliance descriptively? The draft runs B-only (cheapest); C/S format behavior is guarded at full-run Step 0 by (e)/(f)/(f′).
4. T=120 sufficiency for 3-hop scratchpads (S7-1 material uncertainty #4) is inherited unresolved.
