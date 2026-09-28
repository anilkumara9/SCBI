# S4-8 Pre-registration DRAFT — Independent Law #14 Review (LOG-4476)

*Status: REVIEW — binding. This document reviews; it does not edit the draft, authorize a run, or mint an experiment number.*
*Reviewer: independent Law #14 lane (pre-assigned LOG-4476), first-touch — this reviewer has not touched the S4-8 draft, its backlog row, or the EXP085 chain before this review.*
*Inputs read in full before judging: `research/innovation/S4-8_PREREG_DRAFT_2026-09-28.md` (LOG-4475); LOG-323 (EXP085 KILL record, binding); `experiments/protocols/EXP085_I2_RUNNERUP_SUPPRESSION_PREREG_DRAFT.md` §2 (Law #15 gate card) and its kill grounds; repo `AGENTS.md` (14 laws); Law #15 gate-card convention; LOG-4338 degeneracy lesson; LOG-219 death-debt rule; LOG-4353 (S4-8 birth).*
*Compute: $0 CPU. No model runs, no weights touched, no signed artifact modified. The draft was NOT edited.*

---

## 0. Executive summary

The draft is the strongest fresh-proposal pre-registration this reviewer has seen in the I2 family: the EXP085 escape is genuine (verified line by line below), the G1 gate is correctly placed first in the binding order, the Tier-0 screen is a real $0 gate, multiplicity is handled with a single binding test, and the scope fence is airtight. **It is not yet signable.** Five MAJOR defects — all in the decision table's interaction with the foil arm and in the bench-build specification — would let the binding machinery misroute real outcome patterns or rest on unauditable bench construction. None is structural; all are fixable by pre-registered text. No redesign is required.

**Binding verdict: SIGN-WITH-FIXES.** The five MAJOR fixes (§3, D1–D5) are mandatory before CEO signing. The three MINORs (§3, m1–m3) are required before execution clearance. After the repair wave, an independent delta re-verification lane must confirm each fix is present verbatim before signing.

---

## 1. Per-element scores

### Element 1 — Rank measurability / genuine escape from the EXP085 algebraic collapse: **PASS**

Verified line by line against LOG-323's kill grounds:

1. *EXP085's collapse:* at k=2, correct-rank r_i ∈ {1,2} with r_i = 2 ⟺ wrong, so ΔM_C2 ≡ 2·(N_f/60)−1 — a deterministic relabeling of baseline accuracy. **Confirmed** from the killed draft's §2 and LOG-323.
2. *The k=8 construct:* r_i ∈ {1,…,8} is not a deterministic function of correctness — a wrong item can hold the correct option at any rank 2–8. ΔM_T on the Tier-0 population = (# rescued)/n_pop, which depends on the empirical rank profile and the masking counterfactual, not on baseline accuracy alone. **No relabeling exists.** The draft's claim "ΔM is not a function of N_f" checks.
3. *C3 vacuity:* at k=2 the mask set was the whole option set (masks {m₁,m₂} = O(x)); at k=8, T masks exactly 1 of 8 and re-argmaxes over 7 — a well-defined operator. **Confirmed well-defined.**
4. *Tier-0 gate vacuity:* at k=2 every failed item has r_i = 2, so any median-based screen always opens (Type-I = 1.00). At k=8 the median-over-failed-items > 5 kill bar is a genuine statistical property of the rank distribution (uniform null median = 4.5; the bar sits above it). **Genuine gate.**
5. *T never masks the correct option on Tier-0 items:* top-1 ≠ correct by population construction, so the test arm cannot corrupt by masking the answer. **True by construction;** the draft states it and the R-arm symmetry argument (§2.3) is the correct consequence.

The license verdict "HOLDS for a test, not a conclusion" is the honest scope. **The escape is real — this is a different experiment, not a revival, per LOG-323's routing.**

### Element 2 — G1 real-tokenizer gate (EXP090 lesson): **NEEDS-FIX**

What is right: the gate is structurally present, correctly specified as RUN-INVALID (not a verdict), and correctly placed **first** in the binding evaluation order (§3 step 1) — before the Tier-0 premise kill. The attestation format is auditable per-string (§5 item 2: per-string token counts + intra-item distinctness), which is exactly what risk 1 demanded. The "asserted satisfiability is worth nothing" lesson is internalized.

What is missing: **the tokenizer is never identified.** "The REAL tokenizer (the production tokenizer of the frozen model)" names a role, not an artifact. The scope fence names Pythia-410m, but the tokenizer name + revision/hash is not pinned anywhere in the draft. A gate whose instrument is unnamed is not auditable — the repair lane must pin it (e.g., EleutherAI/gpt-neox-20b, revision hash) in §2.1/§4. **→ MAJOR D5-family fix D4 (see §3, D4 item e).**

### Element 3 — Falsification bars (statistics, thresholds, multiplicity): **NEEDS-FIX**

What is right: exactly one binding test (T-vs-R McNemar, α = 0.05), all other contrasts at Bonferroni α = 0.0125 and explicitly descriptive — Law #9 satisfied, no post-hoc promotion possible. DELTA_BAR = 0.10, flat band |ΔM| < 0.05, Tango CIs, breaking points sharp (ΔM_T ≤ 0.05 → PIVOT-or-KILL; T-vs-R n.s. with ΔM_T > 0 → KILL nonspecific; n_pop < 12 → Underdetermined). The McNemar feasibility numbers check: b=6,c=0 → p = 2/64 = 0.03125 < 0.05; b=5,c=0 → p = 0.0625, n.s.

What is broken — **two decision-table defects:**

- **D1 (MAJOR):** Step 8 (KILL nonspecific) misroutes the pattern {ΔM_T > 0, T-vs-R p ≥ 0.05, ΔM_F > 0 significant}. Step 8 fires → verdict "Refuted" with rationale "random masking matches — generic perturbation" — but in this corner the *structural foil* mask rescued, not (only) the random mask. The rationale misdescribes the evidence, and the interference-positive pattern is buried under a Refuted verdict. The F-significant pattern must be evaluated before step 8.
- **D2 (MAJOR):** The CONTINUE conjunct |ΔM_F| < 0.05 is unreachable in the plausible foil–top-1 overlap world. The structural foil is "the distractor judged most confusable" — on failed items the baseline top-1 is the model's most-confused-about distractor, so foil == top-1 on a large fraction of Tier-0 items is the *expected* case, not a corner. Where they coincide, the F arm duplicates the T arm and ΔM_F ≈ ΔM_T > 0.10, so CONTINUE can never fire; the outcome routes to step 10 PIVOT ("Not supported") — a genuine autonomous rescue mislabeled. Step 10's parenthetical ("F's rescue is then a mechanism note, checked descriptively against top-1/foil overlap") contradicts the binding table: the table gives the overlap check no adjudicating role. The overlap must be pre-registered as a stratum, not a parenthetical.

### Element 4 — Cheapest falsifying test + Tier-0 quantitative kill bar: **PASS**

The Tier-0 screen (≤120-pass logit rebuild, $0 CPU) genuinely precedes the battery; the kill bar (median correct-rank > 5 on failed items) is quantitative and the battery never runs when it fires. The draft honestly retires the "$0 screen" label per LOG-284 (archives carry decisions only) and prices the rebuild instead of hiding it. The power gate (n_pop ≥ 12 → Underdetermined, R4: never KILL on a powerless test) is the correct conservatism. Risk 3's conservatism (partial R rescue → KILL nonspecific, never "trending") is acceptable and pre-registered.

### Element 5 — Degeneracy analysis + constant-data unit tests (LOG-4338): **PASS**

§4 pre-registers all five before any bench contact: (a) constant-logit → option-index tie-break asserted; (b) masking a non-top-1 token never changes argmax on fixed logits; (c) masking top-1 promotes the runner-up on fixed logits; (d) b=c=0 → McNemar p=1.0 is a valid null, not an error; (e) empty failed set → Tier-0 vacuous. The masking unit-test log is a persisted instrument (§5 item 5). This is exactly what LOG-4338 demands (degeneracy analysis + constant-data unit test before pre-registration). **MINOR m3:** the list should additionally require the McNemar-exact implementation to cross-check against a reference (hand recurrence or scipy) on the (b,c) grid — the implementation review will need it.

### Element 6 — Scope fence (no autonomy/general claims): **PASS**

Airtight: EXP085's kill explicitly untouched; masking declared executor-applied ("must never be described as an autonomy result"); no generality beyond the k=8 2-hop bench, Pythia-410m, frozen; CONTINUE licenses only the operationalized claim ("target-free top-1 masking rescues decisions on this bench"); five permitted verdicts, no banned language; the S6 L11 stand-down acknowledged as a separate lane. The summit-filter caveat is preserved, not buried.

### Element 7 — Feasibility algebra (EXP079 lesson): **PASS**

The §4 N_pop computation is the EXP079 lesson applied correctly: n_pop and minimum-flips-for-significance computed from Tier-0 *before* the battery; max achievable ΔM = 1.0 ≥ DELTA_BAR = 0.10 (no hidden structural cap — the draft states the cap analysis explicitly, unlike EXP079's split-limited probe); rank threshold contentful at k=8; "if the computation shows the bar unreachable, the battery does not run (HOLD, not a silent edit)". Budget arithmetic checks: 120 + (240 + probes ≈ 360) = 480 ≤ 500 hard cap. The battery runs all 60 items × 4 arms with the primary on the Tier-0 population and full-bench ΔM secondary — consistent with §2.3's endpoint definition.

---

## 2. Law-by-law check (AGENTS.md #4, #9, #13, #14, #15)

- **Law #4 (no silent hypothesis/design shift):** §0's Law #15 block and the §3 decision table are consistent KILL/CONTINUE/PIVOT mappings (premise↔step 2, nonspecific↔step 8, null↔step 9, CONTINUE↔step 7, diagnostic-PIVOT↔step 6). **Holds**, subject to D1/D2 repairs.
- **Law #9 (no post-hoc metric cherry-picking):** single binding test pre-registered; Bonferroni for the rest; "never trending" conservatism explicit. **Holds.**
- **Law #13 (deterministic reproducibility):** R-arm seed pinned, Δθ=0 hash pre/post, environment + seed manifest, per-item records (LOG-284 aggregate-only gap explicitly not repeated). **Holds**, subject to D4 (prompt template + readout position pinning).
- **Law #14 (adversarial review):** this document. **Discharged.**
- **Law #15 (gate card):** all six present — precise question, decision it changes, cheapest falsifying test, mathematical license, quantitative prediction with bars, sharp breaking point. **Holds.**
- **Law #2 (never invent):** no empirical numbers invented; all values cite the backlog row or LOG-323; the new construct is specified, not measured. **Holds.**
- **Law #7 (zero leakage):** foil-build blindness guard present (see D3 for the operationalization gap). The R arm's correct-option exclusion uses the label in *control construction*, never exposes it to the model, is documented with rationale, and is conservative (it strengthens the control, making T-vs-R harder to win). **Holds as designed;** the draft must never describe R as "label-free" (it does not).
- **Law #8 (never delete failures):** EXP085's killed draft retained/banne
...[truncated 10000 chars]