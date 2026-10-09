# EXP150 Design — DRAFT: EXP149a bench-repair re-attempt — stratified dry-run gate + hardened compositional template — 2026-10-09

**Status: DRAFT — NOT SIGNED. NOT EXECUTED.** This document designs the licensed bench-repair re-attempt of EXP149a (the hop dose-response study) for the CEO-minted experiment number EXP150 (LOG-4971). It awaits independent Law #14 review and CEO sign + execution authorization. No forwards have been run under this number.

**Drafting lane:** EXP150 innovation-sprint design, 2026-10-09. **Experiment number EXP150 minted by the CEO** (LOG-4971) — new operationalization = new number per the single-lane fence; EXP149's HELD verdict stands untouched (a HELD scopes nothing and overturns nothing).

---

## 1. Parent context [FACT]

EXP149 (LOG-4967/4968/4969; Law #14 SIGN-WITH-FIXES repaired; CEO sign LOG-4968): the two EXP148 death-debt candidates both **HELD at registered Step-0 gates** — no full runs, no verdicts.

**Study (a) — hop dose-response (Pythia-410m): HELD at the dry-run gate.** Fresh 760-item bench built (seed 149001, pin `a4275c8c7996006096c715c5399d0019844ded8aaff663c0359ead202bc27f67`, strata exact 190×4, golds ≥2×). Dry run: B accuracy 0.90 on the pooled 20-item subset (seed 149002) ∉ [0.2, 0.8] → STOP at design cost (~300 forwards), logged HELD.

**Apparatus finding [OBSERVATION] (diagnostic, not a verdict input — EXP149 log):** a post-stop B-arm sweep of the full 760-item bench shows violent stratum heterogeneity — compositional-2hop B = 0.9895, compositional-3hop B = 0.9316 (at/near ceiling), transitive-2hop B = 0.3105, transitive-3hop B = 0.3316. The dry-run subset drew 12/20 compositional-2hop items — **the gate tripped on subset composition, not bench-wide degeneracy** (full-bench B = 0.6408). The gate outcome stands as registered (no re-draw; Law #4).

**Licensed repair proposal (LOG-4969, the entire license for this lane):** any EXP149a re-attempt needs
(i) a **stratified dry-run gate** (per-stratum [0.2, 0.8] checks, not one pooled 20-item draw), and
(ii) a **hardened compositional template** (compositional B was 0.9895/0.9316 — at/near ceiling, no headroom to measure a gain) **or** a **transitive-only dose-response**.

**What the current compositional template is [FACT]:** possessive-chain facts ("Crun's hat is Blix.", "Blix's friend is Krad."), question spells the chain ("Who is Crun's hat's friend?" → "Krad"). The question's possessive chain is a literal substring map onto the fact chain — solvable by greedy entity-chain following with zero relation composition. That is the mechanism of the ceiling.

---

## 2. Design verdict: transitive-only dose-response as the verdict-bearing primary; hardened compositional as a registered pilot secondary

**Recommendation (primary): transitive-only hop dose-response.** The transitive strata have *verified* headroom (B = 0.3105/0.3316 — squarely measurable) and need no template redesign. The dose-response question is asked and answered on data where a gain is in principle measurable. The compositional question is unanswerable on the current template — that is a registered bench finding, not a design flaw to patch by fiat.

**The hardened compositional template is still built and registered — as a pilot secondary, descriptive-only.** The hardening mechanism is principled (distractor chains force relation-specified chain following; §6), but its achieved difficulty is *unverified until built* — registering a verdict on it would risk a second HELD on an untested instrument. It therefore gets its own per-stratum Step-0 gate and descriptive reporting (nets + CIs, no decision table). If it passes its gate and shows headroom, it becomes evidence for a future numbered experiment; it does not speak in this one.

**What this does not do:** it does not re-litigate EXP149 (HELD stands); it does not re-draw or reinterpret EXP149's gate outcome (Law #4); it does not change the models, arms, prompts, budgets, or scoring; it does not license execution (independent review SIGN + CEO authorization still required).

---

## 3. The questions

**Primary — transitive-only hop dose-response [HYPOTHESIS]:** The WRITE/READ discipline advantage over budget-matched CoT grows with reasoning depth on the transitive strata: net(S−C) at transitive-3hop exceeds net(S−C) at transitive-2hop — δ̂_T3 − δ̂_T2 > 0, on frozen Pythia-410m, fresh bench.

**Breaking point (primary):** 95% CI for (δ̂_T3 − δ̂_T2) entirely ≤ 0, with per-level guards (d_s),(e),(f),(f′) PASS → **KILL** the depth-dependence claim on transitive strata (the gain does not grow with hops there; EXP148's CONTINUE stands as a pooled effect, not a depth effect).

**Scope note [DEFINITION]:** this is a deliberately *narrowed* hypothesis relative to EXP149's. The narrowing is registered here, in a new numbered experiment, with the stated reason (compositional strata at ceiling — §1) — not a post-hoc shift of any prior hypothesis (Law #4 is satisfied by construction: EXP149 asked the unscoped question and HELD; EXP150 asks the scoped question fresh).

**Secondary — hardened compositional pilot [OBSERVATION target]:** descriptive S−C nets and CIs per hardened-compositional level, *if* its per-stratum gate passes. No decision table. No verdict.

---

## 4. Stratified dry-run gate (licensed repair (i)) — binding, precedes the full run

**Registered subset:** 20 fresh items per stratum × 4 strata = 80 items (subset seeds registered at execution, ≠ construction seed, ≠ each other), B arm only, T_B=15, greedy, §5.3 scoring of the EXP149 pre-reg (carried verbatim). Computable before any full-run forward. Uses no test labels in prompts (Law #7 — golds touch scoring only).

**Trip table (registered — a computation, not a choice):**

| Gate | Check | Trip condition | Registered outcome |
|---|---|---|---|
| (d-T2) | transitive-2hop B accuracy | ∉ [0.2, 0.8] | Study STOPS at design cost, logged HELD — the primary is unmeasurable |
| (d-T3) | transitive-3hop B accuracy | ∉ [0.2, 0.8] | Study STOPS at design cost, logged HELD — the primary is unmeasurable |
| (d-HC2) | hardened-compositional-2hop B accuracy | ∉ [0.2, 0.8] | HC2 stratum excluded from the secondary (logged descriptively); primary proceeds |
| (d-HC3) | hardened-compositional-3hop B accuracy | ∉ [0.2, 0.8] | HC3 stratum excluded from the secondary (logged descriptively); primary proceeds |

**Why asymmetric:** the primary's verdict machinery needs both transitive levels measurable; the secondary is an instrument test — a failed instrument is dropped, not a verdict. The exclusion is a registered branch (Law #4), never a post-hoc data selection.

**Pooled-computation exclusion [DEFINITION] (Advisory A3, Law #14 review 2026-10-09):** items from any (d-HC*)-dropped stratum are excluded from all full-run pooled computations; the secondary is per-stratum descriptive only, so no pooled secondary statistic is registered.

**Leakage audit:** the gate consumes only B-arm generations and golds-at-scoring. No S/C/WRITE information enters the bench; no item's gold touches any prompt. The gate cannot inflate or deflate the S−C nets — it can only stop the study or drop a secondary stratum.

**Cost:** 80 × 15 = 1,200 forwards. Design cost: 193,800 (generation) + 1,200 (stratified dry run) + 4,800 (C+S pilot, §5.4) = **199,800 ≤ guard (g) 200k** [registered].

---

## 5. Hardened compositional template (licensed repair (ii)) — registered construction procedure

**Hardening mechanism [INTERPRETATION]:** convert "follow the entity chain" into "follow the *relation-specified* chain" by adding distractor chains that share the head entity but differ in the first relation. The model must attend to the relation sequence, not just entity adjacency.

**Registered construction procedure (mechanical — the execution lane builds exactly this):**

1. **Head entity:** sample H from the 40-entity pool.
2. **Queried chain:** sample a relation sequence R_1…R_h (h = 2 or 3), relations from {hat, friend, pet, car, book}, with R_1 fixed distinct from the distractor chain's first relation (constraint 4).
3. **Distractor chain:** shares head H; first relation R′_1 ≠ R_1; remaining relations sampled; length = h.
4. **Entities:** sample distinct entity names for every chain node (≠ H, no reuse within an item, ≠ exemplar entities — Law #7).
5. **Facts:** emit "X's R is Y." per link for both chains; **shuffle fact order** with the registered construction seed (positional reading fails).
6. **Question:** "Who is H's R_1's R_2's …?" following the queried chain.
7. **Gold:** terminal entity of the queried chain.

**Registered validity constraints (construction-time assertions, zero forwards):**
- (v1) Queried-chain terminal ≠ distractor-chain terminal (no ambiguity).
- (v2) Every gold is a single token under the Pythia tokenizer — checkable offline with the tokenizer, a computation not a forward; the EXP149 (p1) lesson applied at construction.
- (v3) Distractor chains terminate unambiguously at their own distinct entities (the item is fully determined; no second reading yields the gold).
- (v4) Entity pool closed (40); exemplars entity-disjoint; golds ≥2× per the EXP148 §5.1 recipe (carried).

**Why this preserves validity:** the gold is still a single entity name; the question still has exactly one correct answer; the queried relation sequence is stated in the question. What changes is that entity-adjacency alone no longer suffices — the relation words must be composed. The difficulty is *unverified until built* — hence the per-stratum gate (d-HC2)/(d-HC3) and the descriptive-only status.

**Example (2-hop):** Facts (shuffled): ["Crun's car is Zib.", "Blix's friend is Krad.", "Crun's hat is Blix.", "Zib's friend is Dax."] Question: "Who is Crun's hat's friend?" → gold "Krad" (distractor terminal "Dax" ≠ "Krad" ✓).

---

## 6. Power and decision machinery (carried from the signed EXP149 pre-reg)

**Primary statistic:** θ = δ̂_T3 − δ̂_T2 (transitive strata only), Wald SE(θ) = √[SE(δ̂_T3)² + SE(δ̂_T2)²], SE(δ̂_h) = √[(d_h − δ̂_h²)/n_h] (S7-1 §2.2 convention, carried).

**Design value:** n_T2 = n_T3 = 190 per hop level, fixed by the registered bench (4 strata × 190 items). EXP149's power table (n=380) does not transfer. Recomputed (independent Law #14 recomputation, this review): at d = 0.30–0.36, SE(θ) = 0.0523–0.0580, **power 0.53–0.64** for δ = +0.10, one-sided α = 0.05 — the registered true-power band is [0.53, 0.64] [Fix E1]. The transitive discordant-pair rate is not pre-known — the **registered Step-0 bench-size rule** (CEO disposition E3; no n-raise — the bench is fixed, so no larger n exists): compute registered Wald-formula power Φ(0.10/SE(θ) − 1.645), SE(θ) = √[(d_src − 0.10²)(2/190)], from the 20-item C+S pilot rate d_pilot at the bench's fixed n=190; if the Step-0 registered power < 0.53 (band floor), the study STOPS at design cost — logged HELD — a computation, not a choice. The achieved power governs CONTINUE probability, not KILL validity (false-KILL 0.025 under δ=0, fails safe to HELD) [Fix E3].

**KILL/HELD machinery (carried, transitive-scoped):**
- KILL: 95% CI for (δ̂_T3 − δ̂_T2) entirely ≤ 0, with per-level guards (d_s),(e),(f),(f′) PASS. Operating characteristics carried: false-KILL 0.025 under δ=0 (remainder HELD — fails safe); false-KILL < 1e-4 under δ=+0.10; P(KILL fires) ≈ 0.41–0.48 under δ=−0.10 (recomputed at n=190) [Fix E2].
- CONTINUE: CI entirely above 0 AND transitive-3hop S−C one-sided p < 0.05.
- PIVOT: KILL fires AND transitive-3hop S vs B one-sided p < 0.05 (carried verbatim per the registered carry rule; CEO disposition A1/LOG-4968 applies).
- HELD: anything else. RUN-INVALID: apparatus guard trip — never a verdict.

**4-hop trigger:** NOT re-registered. EXP149's trigger existed for the unscoped design; with the narrowed primary and the guard-(g) headroom failure observed (4-hop would have breached 200k), a third level is out of scope. If the CEO wants it later, it is a new numbered experiment, not a quiet addition.

---

## 7. Feasibility

**$0 CPU.** (a) ≈ 193.8k generation + 1,200 stratified dry-run + 4,800 C+S pilot = **199.8k ≤ guard (g) 200k**. Wall ≈ 9h at EXP148 rates — re-gated at Step 0 (guard (h) ≤ 72h). Frozen backbone Δθ=0 throughout; greedy; local caches only (Pythia-410m in `~/.cache/huggingface` — verified present for EXP149; re-verified at Step 0, no HF Hub contact). No fine-tuning. No GPU contact. Margin note [NOTE]: design cost sits at 99.9% of the 200k cap (200 forwards of headroom) — razor-thin by construction; the bench-size STOP rule and Step-0 re-assertion cover overruns. [Advisory A1 noted, Law #14 review 2026-10-09.]

**Env:** the EXP149 lane restored the EXP148 CPU stack family in `~/workspace/.exp149-venv` (torch 2.14.x+cpu, transformers 5.17.0, numpy) — the execution lane re-verifies and records its own manifest (Law #13), reusing the venv if intact.

---

## 8. Open items for the independent Law #14 reviewer

1. **Hardened-template validity:** does the distractor-chain procedure (§5) preserve the bench's validity conditions (unambiguous gold, single entity name) while genuinely changing the measured skill? Any construction constraint missing?
2. **Gate asymmetry:** is the (d-T*)-STOP vs (d-HC*)-drop asymmetry the right registered branch, or should a hardened-compositional trip also STOP the study?
3. **Descriptive-only secondary:** is withholding a decision table from the secondary the right Law #9 discipline, or does it under-serve a clean secondary result?
4. **Transitive-scope narrowing:** is the narrowed hypothesis (EXP149's unscoped question → EXP150's transitive-scoped question) a clean new-registration, or does anything in it re-litigate EXP149's HELD?
5. **d-range for transitive power:** EXP149's power table spans d = 0.30–0.36. If the Step-0 pilot finds transitive d outside this band, the registered n-raise rule covers it — but should the pre-reg additionally register an MDE table for the transitive range? [Adjudicated by the Law #14 review — the n-raise rule is superseded by the registered bench-size rule (Fix E3); the power table is recomputed for n=190 (Fix E1). Repair lane annotation, 2026-10-09.]

---

*Design draft finalized 2026-10-09 (LOG-4971). Status: DRAFT — NOT SIGNED. NOT EXECUTED. No forwards run. Companion: `EXP150_PREREG_DRAFT_2026-10-09.md`. Awaited: independent Law #14 review of both drafts → CEO sign → execution authorization (Step-0 gates first). Execution NOT licensed by this document.*

---

## Fixes applied (Law #14 review repair lane, 2026-10-09)

- **E1:** §6 design value corrected to the registered bench (n_T2 = n_T3 = 190): power recomputed to **0.53–0.64** for δ=+0.10, one-sided α=0.05 (SE(θ) = 0.0523–0.0580 at d=0.30–0.36) — registered true-power band [0.53, 0.64]; all n=380-carried figures corrected. (Independently re-verified this lane.)
- **E2:** reverse dose-response P(KILL fires) ≈0.77 → **≈0.41–0.48** at n=190. (Independently re-verified this lane.)
- **E3:** the 0.80-bar n-raise rule is superseded — no n-raise is registered (bench fixed at 190/stratum). Registered Step-0 bench-size rule: registered Wald-formula power at n=190 from d_pilot; if < 0.53 (band floor) the study STOPS at design cost, logged HELD (computation, not choice). Achieved power governs CONTINUE probability, not KILL validity (false-KILL 0.025 under δ=0 intact, fails safe). CEO disposition: the 0.80 bar is unsatisfiable; the true-power bar is accepted.
- **E4:** pre-reg-only fix (registered composition rule at the top of the pre-reg's §4 — §4's table is the sole binding verdict machinery); this draft's carried machinery (§6) is unchanged.
- **A1:** razor-thin guard-(g) margin (199.8k/200k) registered explicitly in §7.
- **A2:** noted — registered seed-derivation rule for future pre-regs; no change in this draft.
- **A3:** (d-HC*)-dropped stratum items explicitly excluded from all full-run pooled computations (§4).
- **A4:** PIVOT carry consistent with CEO disposition A1/LOG-4968; noted, not objected — no change.
- **A5:** Law #15 worth-it at ≈0.53–0.64 power flagged for the CEO's call — not a repair-lane decision; the band is registered honestly in §§6–7.

**Status after repair: repaired per the independent review's exact prescriptions (`EXP150_LAW14_REVIEW_2026-10-09.md`). STILL NOT SIGNED — signing is the CEO's act after diff-level re-verification. NOT EXECUTED. No hypothesis, guard, or decision-bar change was made; all fixes are numeric/expositional plus the registered E3/E4 rule registrations.**
