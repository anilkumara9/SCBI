# Adversarial Review — Phase 2 (Manuscript + Loop Spec)

**Reviewer role:** Adversarial Reviewer (red-team; challenge, don't defend)
**Date:** 2026-09-23
**Governing:** `AGENTS.md` (14 laws), `.agents/agents/adversarial-reviewer.md`, `.agents/rules/00-core-research.md`
**Deliverables under review:**
- D1: `reports/paper_draft.md` (5,243 words, NeurIPS-style boundary/negative-result manuscript)
- D2: `theory/LOOP_SPEC_DRAFT.md` (337 lines, first operational G/E/S/T spec)
**Method:** hostile NeurIPS reviewer + scientific-integrity auditor for D1 (10+ quantitative claims recomputed from primary JSONs this session); specification attacker for D2 (implementability, validity architecture, leakage).

---

## PART A — Manuscript (`reports/paper_draft.md`)

### A1. Number-vs-artifact verification (recomputed 2026-09-23 from primary JSONs)

Every value below was recomputed from the unmodified primary artifacts. **Zero mismatches found.**

| # | Claim in draft | Artifact source | Artifact value | Match |
|---|---|---|---|---|
| 1 | EXP065 Stage A per-vocab table (raw/aligned/Δ) | `exp065_results.json` → `stage_A_alignment_discovery` | V2: 0.7379/−0.0640/−0.8019; V3: 0.7144/0.0217/−0.6927; V4: 0.6996/0.0023/−0.6973; V5: 0.7224/0.0527/−0.6697 | ✅ exact |
| 2 | EXP065 means: raw +0.7186, aligned +0.0032, Δ −0.7154 | recomputed from (1) | 0.71858 / 0.00318 / −0.71541 | ✅ |
| 3 | EXP066 Stage A: raw +0.6852 → aligned −0.0118, Δ −0.6971 | `exp066_replication_results.json` → `stage_A_summary` | 0.68524207 / −0.01181473 / −0.69705680 | ✅ exact |
| 4 | EXP064 Level A `mean_off_diagonal` = 0.7927 | `exp064_results.json` → `pre_intervention_alignment` | 0.79266537 | ✅ |
| 5 | EXP065 static: ΔM 0.0, b=0, c=0, p=1.0, KL 0.00028 | `stage_B_confirmatory_results.Static_B_agg` | 0.0 / 0 / 0 / 1.0 / 0.00027742 | ✅ |
| 6 | EXP065 bridge: +16.67pp, 10/19, p=0.0020, KL 0.0118 | `...Same_Layer_Output_Bridge` | ΔM 0.166667, b=10, c=0, p=0.001953125, KL 0.01180088 | ✅ |
| 7 | EXP066 static: ΔM 0.0, b=0, c=0, p=1.0, KL 0.00017 | `stage_B_conditions.Static_B_agg` | 0.0 / 0 / 0 / 1.0 / 0.00017211 | ✅ |
| 8 | EXP066 bridge: +13.33pp, 8/26, p=0.0078, KL 0.0283 | `...Same_Layer_Output_Bridge` | ΔM 0.133333, b=8, c=0, p=0.0078125, KL 0.02827699 | ✅ |
| 9 | EXP066 Wilcoxon table (5 rows) | `wilcoxon_p` + `delta_margin` fields | static 0.04143/+0.00903; aligned 1.63e−11/−0.04062; bridge 1.63e−11/+0.74921; B⊥ 0.21076/+0.00307; B_wrong 1.21e−08/−0.02050 | ✅ all match |
| 10 | EXP064: 7 basis conditions ΔM=0, b=c=0, p=1.0; bridge +5.0pp, 3 rescues, p=0.25 | `condition_results` | all 7 basis: ΔM 0.0, p 1.0; bridge: ΔM 0.05, b=3, p=0.25 | ✅ |
| 11 | Baselines 68.33% / 56.67%; 19 / 26 rescuable | `baseline_accuracy` fields | 0.683333 / 0.566667; 60×(1−acc) = 19 / 26 | ✅ |
| 12 | McNemar exact p values (two-sided: 2·0.5^b) | b=10→0.001953125; b=8→0.0078125 | matches JSON `exact_p` | ✅ |

**Headroom-window check:** the draft's "40–70% headroom window" claim was suspected of error, then cleared — the program's own EXP067 protocol §5 defines the gate as *baseline accuracy ∈ [40%, 70%]*; 68.33% and 56.67% are both inside. The draft is consistent with the program's definition. (A reader unfamiliar with the convention could misread "headroom" as error rate; the draft's parenthetical "19 and 26 rescuable errors" disambiguates adequately.)

**Lemma proof-sketch check (§6.1):** the "unit-norm row with a +1 entry is exactly eᵢᵀ ⇒ block-diagonal" step is sound. The scramble-bound arithmetic (§6.2: √(3/768)=0.0625, √(3/1024)≈0.0541) recomputes correctly. T-1 caveat is present and honest.

### A2. N1-position consistency — HOLDS

Checked abstract ("assessed novelty tier is N1 — Known Combination (tested mechanism N0)... this paper therefore makes no methods claim"), §1 ("Why a boundary paper"), §2.3 (loop distinction "[CONJECTURE]... unscored pending demonstration, not 'N2-aspirational'"), §7 ("boundary science, not novelty science... cannot move the novelty needle in either direction"), §9 ("What cannot make the program interesting: a positive EXP067 C3 presented as a novel method"), §10 ("we claim no novelty for it"). No methods-language creep detected. The word "novel" appears only in negations and the N1 tier name.

### A3. Retraction prominence — SUFFICIENT

§4 is a full dedicated section (not an appendix footnote) with the per-vocabulary table, the sign-flip stated in bold-adjacent language ("The claim is **retracted**"), the +0.79 misattribution traced, and the +0.1290 provenance recorded as *unresolved* rather than invented. An independent reader cannot miss it. "A paper that hides its own retraction is fraud; we publish ours." — this sentence is a hostage to fortune in the best way: it binds the program publicly.

### A4. Related-work fairness — FAIR, one labeling gap

CAA/ActAdd equivalence is stated at the operator level with the preprocessing-vs-operator distinction made explicit (§2.1). PPLM is credited with Δθ=0 (the non-differentiator correction survived into the paper's §2.3 lineage). Tan/Braun are used as *predictors* of the result, not strawmen; Ethayarajh/Jorgensen are used to *weaken* the paper's own O1. This is the opposite of strawmanning. **Minor gap:** §2.3's "algorithmically isomorphic, differing only in search object: thoughts vs. bases" (ToT) carries no epistemological label though it is load-bearing for the N1 argument — tag it [INTERPRETATION].

### A5. Hype check — CLEAN

"superhuman" occurs only in explicit non-claims (§1, §8.4, §9). "Invented"/"novel mechanism" occur only in the §9 prohibition sentence. No "revolutionary"/"breakthrough"/"vastly outperforms". No journalist-quotable overclaim found; the most quotable line ("A paper that hides its own retraction is fraud") is a methodological boast, not a scientific one, and it is earned.

### A6. NeurIPS-style review (hostile)

> **Summary.** A negative-result paper: static contrast-direction injection (CAA-equivalent, N1 — stated up front) shows zero causal transfer at verified headroom while output-space controls work; the authors retract their own prior Procrustes claim inside the paper, prove why the operator scrambled, and pre-register the fair test (unexecuted).
>
> **Strengths.** (1) Admirable scientific hygiene: in-paper retraction with artifact-level forensics is rare and valuable. (2) The rank-deficiency lemma is a clean, correct, genuinely useful cautionary result for the steering literature. (3) Falsification discipline (decision trees, halt-as-outcome) exceeds the norm.
>
> **Weaknesses.** (1) The empirical core is thin: N=60, one benchmark family, two sub-1B models — small even for a boundary claim, and the headline result is *predicted* by the cited brittleness literature (Tan, Braun), shrinking the delta over prior work to "this exact controlled form." (2) The paper's answer to "is the dissociation structural or operator-quality?" is a pre-registration, i.e., a promise, not evidence — EXP067 unexecuted. A reviewer cannot evaluate a boundary the authors have not yet probed with a sound operator. (3) EXP064's seven null conditions sit at 95% baseline (3 rescuable errors); counting them alongside headroom-verified runs without annotation inflates the "eleven basis conditions" headline (see required fix M1).
>
> **Recommendation: Major revision, borderline reject for the main track.** The hygiene and the lemma deserve an audience, but the empirical contribution as it stands is a well-documented null on a tiny benchmark that prior work predicts. The paper becomes submittable when EXP067 is *executed* (either outcome is publishable under the pre-registration) — or, alternatively, reframed for a workshop where negative results and methodology are the point. Do not submit this version to the main track: Reviewer 2 will write exactly weakness (2), and Reviewer 2 will be right.

### A7. Manuscript verdict: **ACCEPT WITH CORRECTIONS**

**Required fixes:**
- **[M1 — MAJOR] EXP064 ceiling annotation.** §5.3's "eleven basis conditions: zero decision changes" must annotate that EXP064 ran at 95% baseline (3 rescuable errors; bridge 3/3, p=0.25 n.s.) — a null there is weak evidence. Either report the headroom-verified count separately (EXP065/066: 4 basis conditions, 2 runs, full headroom) or add the explicit caveat. Do not let the headline count mix ceiling-adjacent and headroom-verified nulls silently.
- **[m2 — minor] Counting transparency.** State the "eleven" denominator explicitly (7 EXP064 + 2 EXP065 + 2 EXP066 basis conditions) and note the exclusion rule for EXP064's three reversal/specificity conditions (one had b=1, n.s.) — one sentence suffices.
- **[m3 — minor] Label gap.** Tag the §2.3 ToT "algorithmically isomorphic" claim [INTERPRETATION].
- **[m4 — minor] Forward pointer.** §9's "the next forensic audit gets written" is cute but the paper should state plainly in §8 or §9 that main-track submission awaits EXP067 execution (per the review above) — bind the program to its own standard.

No fabrication, no number mismatch, no hype leakage, N1 held throughout. The draft is honest; with M1–m4 it is publishable-as-honest. Whether it is *NeurIPS-main-track* publishable awaits EXP067 data.

---

## PART B — Loop spec (`theory/LOOP_SPEC_DRAFT.md`)

### B1. What the spec gets right (acknowledged before attacking)

Δθ=0 proof-by-construction is checkable; Law #7 boundary is respected (no test labels in E; support labels confined to hyperparameter validity); compute-matching is addressed (F(x) budget, compute-matched Best-of-N/self-consistency baselines in the EXP068 checklist); falsifiers F1–F5 are pre-stated with a conjunctive positive criterion; blind-spot risk is named as [CONJECTURE] with a diagnostic rather than buried; the PPLM "Δθ=0 is not a differentiator" correction is stated as [FACT]. The honesty architecture is sound. The attacks below are on *implementability and validity mechanics*, not integrity.

### B2. Objections

- **[S1 — MAJOR] The initial incumbent B₀ is undefined, so the t=0 acceptance step is unimplementable as written.** §0's tuple includes B₀, but no section defines it. §2.3's acceptance rule `A(B_t^*, B_t) = 1 ⟺ S_E(B_t^*) > S_E(B_t) + δ` at t=0 requires S_E(B₀) — undefined. An implementer must invent B₀ (B_agg? unintervened "null direction" with S_E defined on unintervened decisions? random draw?). Each choice changes loop behavior. This is not a gap an implementer can fill "obviously" — it is a missing definition in the spec's core loop.
- **[S2 — MAJOR] View construction is underspecified at the point of maximum load.** §2.2: "the same relational query re-instantiated under each of the m=5 support entity vocabularies (entity-frame substitution; relation and template fixed)." No template grammar, no entity-slot mapping, no procedure for re-instantiating a *novel-entity* Planetary/Elemental test item under Anglo/Biblical/Greek/Roman/Modern vocabularies is given anywhere in the spec. C_cons — the heart of E — cannot be computed without it. An implementer must invent the substitution operator, which is a research contribution in itself, not an implementation detail.
- **[S3 — MAJOR] The ρ-gate double-dips on the support set.** Six hyperparameters (K, m, T_max, λ_c, λ_m, τ_min, δ, σ, D_min, α — §1) are "fixed on D_sup only," and the validity gate ρ = corr(S_E(B), 1[rescue]) is measured "on D_sup (labeled, disjoint from test)." Tuning S_E's weights on D_sup and then gating S_E's validity on the same D_sup makes the gate optimistic by construction. Required fix: split D_sup into disjoint tune/gate subsets, or fix (λ_c, λ_m) a priori and gate only the rest — and state which.
- **[S4 — MAJOR] No tuning objectives are stated for any hyperparameter.** "Fixed on support" appears eight times; *how* — by what objective, what criterion, what search — appears zero times. What objective sets σ (perturbation scale)? τ_min? D_min? δ? Two implementers following this spec will produce different loops. A spec that forces invention of six tuning protocols has not earned its implementability rating.
- **[S5 — MAJOR] §4.3(a) "decoupling" overstates the independence.** The mitigation claims the perturbation axes are "external to G's proposal distribution." But G₁ draws its candidates by aggregating contrast directions from *exactly the same five support vocabularies* that define E's views. The vocabularies are shared; only the representation (direction-space vs induced-decision-space) differs. If the support vocabularies share a systematic bias, G and E inherit it jointly — which is precisely the blind-spot failure mode (a) claims to mitigate. Restate honestly: representation-level separation with shared data dependence, not decoupling. The "partial" label is present but the prose still sells more independence than exists.
- **[S6 — minor]** z₀ is inferable ((0, {}) per §2.3's state update) but never stated; state it.
- **[S7 — minor, tension to acknowledge]** The program's own O5 invalidated margin shifts as task-relevant evidence, yet S_E leans on the self-margin term M̃. The spec's defense (the ρ-gate) is the right one — but it makes S3 load-bearing: a compromised ρ-gate plus a margin component is exactly how a confounded "valid" verdict gets manufactured. The spec should state this tension explicitly in §4.3.

**On the "MEDIUM implementability" self-rating:** not earned as written. S1 alone makes the t=0 step unimplementable without invention; S2 makes the core of E unimplementable without invention; S4 makes the hyperparameter configuration unimplementable without invention. Implementability is LOW as written, raisable to MEDIUM by fixing S1–S4 (all fixable on paper, none requiring new science).

**On OQ4 (candidate diversity):** the D(C_t) guard is defined and logged, which is good, but G₁ resamples the same 150 support contrast pairs that produced B_agg — the effective candidate count diagnostic (promised for EXP068) is doing real work here, and the spec is right to flag it as [OPEN]. No new objection beyond S4 (D_min's tuning objective is unstated).

**On the E-validity conjecture and the ρ-gate's testability:** ρ is computable in principle (support labels exist; "rescue" on support is well-defined), so the gate is *testable* — the problem is purely S3 (double-dipping), not untestability. OQ3 (fundamental blind-spot limit) is honestly framed and correctly routed to falsifier F4 with a diagnostic. No objection to the honesty; the objection is that the mechanism meant to *test* the conjecture is compromised.

### B3. Loop-spec verdict: **ACCEPT WITH CORRECTIONS**

Required fixes S1–S5 (major), S6–S7 (minor). Nothing here requires new science — all five majors are paper-fixable: define B₀, specify the substitution operator (or scope the spec to items for which it exists), split the support set, state tuning objectives, restate the decoupling honestly. After these, the spec earns MEDIUM and EXP068 pre-registration may proceed.

### B4. Single most dangerous objection

**The evaluator-validity architecture is circular and partially unimplementable as specified.** E's credibility rests on two pillars — the ρ-gate and the margin term — and both are compromised: the ρ-gate measures validity on the same support data used to fix E's hyperparameters (S3), the margin term is in tension with the program's own O5 invalidation (S7), and the loop cannot even execute its t=0 acceptance step because the incumbent B₀ is undefined (S1). An EXP068 run against this spec could return a "valid evaluator" verdict manufactured by double-dipping rather than discovered by measurement. Fix S1+S3 and the danger collapses to the honest, named scientific risk (OQ3/F4) — which is exactly where a pre-registration should leave it.

---

## Sign-off summary

| Deliverable | Verdict | Blocking items |
|---|---|---|
| D1 Manuscript (`reports/paper_draft.md`) | **ACCEPT WITH CORRECTIONS** | M1 (EXP064 ceiling annotation); m2–m4 (minor) |
| D2 Loop spec (`theory/LOOP_SPEC_DRAFT.md`) | **ACCEPT WITH CORRECTIONS** | S1–S5 (major, all paper-fixable); S6–S7 (minor) |

**Integrity statement:** 12 quantitative claims recomputed from primary artifacts — zero mismatches. No fabricated citations encountered in the draft's references (all match the signed 24-record audit). No hype leakage. Both deliverables' honesty architectures are sound; the objections are to evidence presentation (D1) and specification completeness (D2), not to integrity. Neither deliverable was edited; corrections are the authors' to make.

*End of Phase 2 adversarial review. Next gate: corrections integration, then re-verification before any external use of the manuscript (Law #14).*

---

## §8 — Phase 2 Re-verification & Sign-off (Adversarial Reviewer, 2026-09-23)

**Method.** Every fix (M1, m2–m4, S1–S7) checked against the corrected documents; the m2 deviation re-verified independently against primary JSONs; three adversarial probes re-run (M1 re-scoping integrity, S3 residual leakage, B₀ bias direction); implementability re-rating audited.

### 8.1 Per-fix confirmation

**Manuscript (`reports/paper_draft.md`) — 4/4 CONFIRMED.**
- **[M1] CONFIRMED.** §5.3 carries the [CORRECTION M1, 2026-09-23] annotation: 7 ceiling-adjacent (EXP064) + 4 headroom-verified (EXP065/066); the strong claim re-scoped; §10 conclusion updated ("4 headroom-verified, 7 ceiling-adjacent; see §5.3 annotation"). Artifact cross-check this session: EXP064's 7 basis conditions all at `acc_base=0.95`, ΔM=0, b=c=0, p=1.0 (`exp064_results.json` → `condition_results`); EXP065/066 `Static_B_agg` and `Aligned_Dynamic_Basis` all ΔM=0.0, b=c=0, p=1.0 at 68.33%/56.67% baselines. The evidential grades are now separated as required.
- **[m2] CONFIRMED.** Denominator stated ("7+2+2"); exclusion rule for the three reversal/specificity probes stated.
- **[m3] CONFIRMED.** ToT "algorithmically isomorphic" claim tagged [INTERPRETATION] in §2.3.
- **[m4] CONFIRMED.** §9 "Submission posture" binds the program in print (workshop-suitable as-is; main-track awaits EXP067 execution).

**Loop spec (`theory/LOOP_SPEC_DRAFT.md`) — 7/7 CONFIRMED.**
- **[S1] CONFIRMED.** `B₀ := B_agg` defined in §1 with justification; `S_E(B₀)` computed as for any candidate; unintervened model rejected as incumbent with reasoning.
- **[S2] CONFIRMED.** §2.2 specifies template τ(x), slot filling, slot-index-aligned map φ_j, view formula, plus an explicit benchmark precondition (items lacking slot signatures excluded and logged, never improvised; §8 checklist).
- **[S3] CONFIRMED.** §1 partitions D_sup → D_tune (100) + D_gate (50), fixed seed, stratified; all tuning on D_tune; ρ-gate on D_gate only. The tuning→gate double-dip is eliminated.
- **[S4] CONFIRMED.** §1.1 states objectives, grids, and deterministic selection rules for all ten hyperparameters (m fixed at 5 with justification).
- **[S5] CONFIRMED.** §4.3(a) rewritten as "representation-level separation with shared data dependence"; shared-data blindness explicitly assigned to F4.
- **[S6] CONFIRMED.** `z₀ := (0, {})` stated in §1.
- **[S7] CONFIRMED.** §4.3(d) states the O5-vs-margin-term tension explicitly; M̃ licensed only via the ρ-gate; S3 split named as prerequisite.

### 8.2 The m2 deviation — adjudicated: INTEGRATOR WAS CORRECT

The review's m2 parenthetical said "(one had b=1)". Recomputed from `exp064_results.json` this session: `B_agg_Premise_Reversal` (rescues_b=1, corruptions_c=0, exact_p=1.0) **and** `B_single_Premise_Reversal` (rescues_b=1, corruptions_c=0, exact_p=1.0); `B_agg_Polarity_Reversal` (b=0). The review text was wrong; the primary artifacts show two. Per Law #2 (artifacts outrank all derived text, including this reviewer's own), the integrator's deviation was correct and the manuscript's "two of them registered a single non-significant rescue each (b=1, c=0, p=1.0)" matches the artifacts exactly. This reviewer's error is recorded here, not erased.

### 8.3 Adversarial probes, second round

- **M1 re-scoping integrity.** The "4 headroom-verified" count is factually accurate (all four at 40–70% baselines, all null). Residual observation (non-blocking): the strict static-injection claim I1 rests on 2 static conditions; the other 2 are scrambled-dynamic nulls. The manuscript is transparent about this (§5.3 annotation + I2's "contributes no evidence for or against the boundary"), and M1-as-specified is satisfied — but a future revision should state "2 static + 2 scrambled-dynamic" explicitly rather than letting "4" do the work. Noted, not blocking.
- **S3 residual leakage.** The primary defect (tuning λ on the gate set) is fixed. Two second-order dependencies survive and are flagged as hardening items for EXP068 pre-registration (non-blocking): (i) G₁ resamples from all 150 support pairs, including D_gate's 50 — at ρ-gate time, candidates are built partly from gate items' own contrast vectors (dilution ~1/150 per item in a mean aggregate; negligible but unclean — G₁ should draw from D_tune only during gating); (ii) μ_M, σ_M (margin normalization) are computed on full D_sup rather than D_tune. Neither can manufacture a validity verdict the way the original double-dip could.
- **B₀ bias direction.** Initializing at B_agg makes acceptance *harder* (must beat static by δ) — the bias points toward null findings, which is the conservative, honest direction. F2 (cos(B*,B_agg)>0.95 on >80%) guards the collapse mode; G₁ fresh draws at t≥1 mitigate local-optimum trapping (OQ4). Justification sound.
- **Implementability re-rating.** S1–S4 closed the exact gaps cited: B₀ defined, view construction specified with a checkable precondition, tuning objectives stated, split defined. An implementer can now code every operator without inventing missing definitions. Residual risk is scientific (E-validity conjecture, OQ3/F4), not specification. **MEDIUM is earned.**

### 8.4 Sign-off

| Deliverable | Verdict |
|---|---|
| D1 Manuscript (`reports/paper_draft.md`) | **SIGNED for external use** — as an honest boundary/negative-result document under its own §9 submission posture (workshop-suitable as-is; main-track submission awaits EXP067 execution). 12/12 Phase-2 fixes confirmed; 12 quantitative claims re-verified against primary artifacts this session with zero mismatches; no hype leakage; N1 held throughout. |
| D2 Loop spec (`theory/LOOP_SPEC_DRAFT.md`) | **SIGNED as a specification** — cleared as the constraining basis for EXP068 pre-registration. 7/7 fixes confirmed; implementability MEDIUM earned. This sign-off covers the spec, not the method: E-validity remains [CONJECTURE], unscored pending the ρ-gate. |

**Integrity statement (final).** No primary artifact was modified at any point in Phase 2. Every number in both deliverables traces to a stored artifact or a labeled illustration. The one error found in this re-verification pass was in my own review text (m2's "one"), corrected against the artifacts per Law #2. Residual items above are recorded as hardening notes, not blockers.

*Phase 2 sign-off loop closed 2026-09-23. Phase 2 status: COMPLETE — manuscript signed, loop spec signed, both gated for their stated next steps (EXP067 execution; EXP068 pre-registration).*
