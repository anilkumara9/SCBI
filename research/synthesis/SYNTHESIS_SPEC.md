# A–J Synthesis — Commissioned Spec (LOG-140)

*Commissioned 2026-09-23 by the CEO, mentorship-directive implementation.
Authority: `research/CHATGPT_MENTORSHIP_DIRECTIVE.md` (LOG-139) incl. the
mentor's second message (P1–P4), the standing law against theory preservation,
and the deliverable expectation. A synthesizer agent will assemble the final
document from three track-cluster reports; the mentor adversarially reviews
the result. The killer experiment (G) and the failure experiment (H) become
pre-registered program-level gates once defined here.*

## 1. The organizing question (P1 — mechanism-level bar)

**"What discovery would have to be true for a frozen model to become far more
cognitively capable through inference-time computation?"**

The canonical objective: θ_after = θ_before while temporary computational
state (B_t, z_t, C_t, M_t, …) evolves during inference. The bar is
**qualitatively new computation, not benchmark scores.** Do NOT ask "how do we
make SCPM win." Score gains are level-1 evidence; the question is whether the
computation itself is new (level 3), or a new strategy for allocating
computation (level 2).

## 2. Honest evidence base — FACTS the synthesis must respect

Every claim below is [FACT — computed/observed]; the synthesis may reinterpret
them ([INTERPRETATION]) but may not soften them.

- **G1 (LOG-134, CPU, $0 GPU): KILL.** Ē_QK(B_agg)=0.389985 ≥
  Ē_QK(b_mean)=0.356185; random-unit null (100 draws, seed 20260923):
  q05=0.341099, q95=0.361730, mean=0.352333. B_agg sits ABOVE the null 95th
  percentile (p_low=1.0 — all 100 draws lower); the bridge sits mid-null
  (p_high=0.2277). The handover's "Core Causal Null-Space Theorem" (§3.3
  central sentence) is **false as a QK-subspace claim** — the exact inversion
  of the sentence. OV corroborates (0.406759 vs 0.353308, null band
  0.3466–0.3590; non-decision per plan). Companion s_j: median 0.356201 ≥
  bridge (fires by +0.000016), aggregation-matched s̄=0.367099 ≥ bridge →
  "maximize QK-projection energy" REJECTED as a sufficient-condition design
  objective. B_wrong=0.4885 QK with ΔM=0 (visible ≠ causal — second
  dissociation). Sensitivity with L20 heads: 0.387411 vs 0.357586 — ordering
  preserved. Boundary claim I1 survives (rests on endpoints, not mechanism);
  paper mechanism → readout-misalignment-or-unknown; QK-subspace operator
  program stood down before further GPU spend.
- **EXP077 (GPU, 2×T4): branch (c) NEITHER.** Radial α∈{0.25,0.5,1.0,2.0}:
  all ΔM=0, p=1.0. Cone-vs-line: b=0,c=0,p=1.0; cone-vs-control: b=0,c=0,p=1.0;
  offset: b=0,c=0,p=1.0; replication: b=0,c=0,p=1.0. Official GPU bridge rescue
  +10pp (56.67%→66.67%, b=6,c=0,p=0.03125); local smoke artifact +23.33pp
  (b=14,c=0,p=0.000122). Licensed kill is NARROW: unconditional ρ=30° cone
  and α=1.0 offset at Pythia-410m/L20. Gated and conditional variants survive.
- **EXP070 (GPU): branch (c2) UNINFORMATIVE_PROBE.** Baseline 68.33%
  (41/60). C2 static +0.00pp p=1.0; C3 oracle-selected +0.00pp p=1.0;
  C7 output bridge +16.67pp p=0.001953. The probe carried no transferable
  signal — no ceiling measured; EXP068 NOT cancelled (pool-homogeneity
  reading).
- **EXP078 (GPU): branch (a) ENERGY_GATE_HALT.** Median projected bridge
  energy 0.054399 < 0.10 — uninformative causal test, informative
  localization: the bridge's causal power lies mostly OUTSIDE the tested
  concept subspace.
- **EXP067 (GPU): branch (a) STAGE_A_HALT.** Rank 33/64, gap 1.59e-08 < 1e-6 —
  the full-rank Procrustes operationalization is underdetermined; H1
  untestable under it; boundary claim I1 unchallenged.
- **EXP079 (CPU-accepted halt): branch (a) READINESS_HEADROOM_HALT.**
  N_final=26<50; max N_final=46<50 over ALL valid 75/75 splits — the signed
  probe rule was infeasible BY CONSTRUCTION, not bad luck. Bundle deviations
  F1–F4 logged. No ceiling measured; EXP068 survives; next step is a
  pool-diversity diagnostic under a new design.
- **EXP065/066 retraction.** Raw cosine +0.7186/+0.6852 → post-Procrustes
  +0.0032/−0.0118; Δcos −0.7154/−0.6971. Defensible boundary: raw
  cross-vocabulary geometric similarity (~0.7) does not yield causal transfer
  under static injection.
- **Handover-era evidence (ledger — verify, don't trust on retelling):**
  +14pp/+7pp findings, autonomous +4pp, EXP057 failure, EXP058 transfer
  failure. **P2: these are observations that constrain the theory, not
  identity.** Sunk-cost bias is disallowed: the synthesis is LICENSED to
  propose a successor architecture that resembles nothing of current SCPM.
- **Forced baselines (standing law).** Any capability claim must beat, at
  matched compute: debate/MoA, STARS, DEER, ∇-Reasoner, a bigger frozen
  model. A capability result without these is a measurement, not a claim.
- **Novelty:** N1 (Known Combination) across the static mechanism family
  until an experiment says otherwise.

## 3. P2 — evidence, not identity

SCPM is one mechanism hypothesis, possibly a precursor, possibly a dead end.
The synthesis must treat the bridge rescues (+10/+16.67/+23.33pp) as
observations needing a mechanism, and the five dead static-geometry rooms as
constraints on where the mechanism ISN'T. The minimal-new-mechanism question
is mandatory: "What is the minimal new mechanism that would make SCPM a
fundamentally different kind of inference system?"

## 4. P3 — the kill experiment is a first-class gate

Deliverable H must define a result that would make the program say "this
mechanism family is not worth pursuing," with an EXPLICIT LICENSE TO KILL.
G (killer) and H (failure) are pre-registered as program-level gates once
defined — the pre-registration is triggered by this synthesis landing, not by
a second commissioning.

## 5. P4 — end with competing hypotheses, not one grand narrative

The synthesis MUST end with H1–H5:
- H1 = dynamic representation control
- H2 = ephemeral computational workspace
- H3 = test-time program synthesis
- H4 = adaptive cognitive routing
- H5 = something not yet named (the synthesis's own invention)

**Boxed standard (every candidate, no exceptions):**
> What observation would uniquely support this hypothesis over its competitors?
> What observation would kill it?

A candidate submitted without BOTH boxes answered is incomplete — the
synthesizer rejects it, the mentor will apply this standard on review, and
commissioning applies it now.

## 6. Deliverable form (what the mentor expects)

Not an executive summary. The final document must contain:
1. **The competing mechanisms** (E: ≥5 radically different candidate
   architectures for inference-time cognitive augmentation), each with both
   boxes from §5.
2. **The prior-art boundary** (D: map of adjacent prior art and exactly where
   the novelty boundary would have to be).
3. **The killer experiment** (G: success = convincing evidence for a new
   inference-time cognitive mechanism).
4. **The kill experiment** (H: result = justified abandonment of the
   mechanism family, with explicit license to kill).
5. **The reasoning behind WHY each experiment discriminates** — which
   hypotheses it separates, which predictions differ, what each outcome
   licenses. This is the most important part.

## 7. Section-by-section requirements (A–J)

- **A. Strongest current interpretation of SCPM evidence.** Grounded in §2
  FACTS. State the evidentiary level of each interpretation
  (improve-inference / change-strategy / new-capability).
- **B. Strongest arguments SCPM is not fundamentally novel.** Operator
  equivalence to CAA (Rimsky et al.), PPLM, Self-Refine, activation steering,
  ∇-Reasoner, STARS, DEER, debate/MoA — with exact equivalence claims and
  where they break. Track 4 + track 7 co-own this.
- **C. Strongest arguments a genuinely new direction exists.** What the
  negatives leave open — the output-side room (bridge rescues + EXP078
  localization), the per-head G1 table, anything the static program could
  not see.
- **D. Prior-art map + novelty boundary.** Where exactly the boundary would
  have to be; what experiment would cross it.
- **E. ≥5 radically different candidate architectures** preserving Δθ=0.
  Each with both §5 boxes. None assumed correct.
- **F. The 3 most scientifically important discriminating experiments.**
- **G. The killer experiment.** Pre-registrable spec sketch: hypothesis,
  conditions, decision tree, kill/survive criteria, budget.
- **H. The failure experiment.** Same spec sketch + explicit license to kill
  the mechanism family.
- **I. Operational definition of "superintelligent augmentation"** — no hype.
  Mechanism-level, falsifiable.
- **J. 3-stage roadmap.** Stage 1 prove/disprove the mechanism; Stage 2
  cross-task/general transfer; Stage 3 qualitatively new capabilities. Each
  stage gated by pre-registered criteria.

## 8. Standing laws the synthesis must obey

- **No theory preservation.** No hypothesis earns continuation by elegance,
  ambition, or sunk cost — only by discriminating experiments surviving
  pre-registered falsification attempts. Theory preservation is the
  program's most dangerous failure mode.
- **Three evidentiary levels, no silent crossing.** "Can improve inference" ≠
  "changes the computational strategy" ≠ "creates qualitatively new
  capability." Every claim states its level.
- **Epistemic double-labeling.** Every load-bearing claim: FACT / INFERENCE /
  HYPOTHESIS / SPECULATION + the repo 10-label mapping (EXPERT_TRACKS.md).
- **Mentor role:** independent scientific mentor / adversarial reviewer — not
  manager, not decision-maker. Plan for adversarial review of the final
  document.

## 9. Commissioning decomposition

Three track-cluster agents produce cluster reports; a synthesizer assembles
A–J. Clusters: (A) foundations — tracks 1,2,5,7 → §§A–C, E-input, I-input;
(B) evidence & validity — tracks 3,4,8,12 → §§A,B,D, the evidence audit,
discovery criterion; (C) futures — tracks 6,9,10,11 → §§E–H,J. All under
LOG-140. Cluster reports: `research/synthesis/CLUSTER_{A,B,C}_2026-09-23.md`.
Final assembly: `research/synthesis/SYNTHESIS_A_J_2026-09-23.md` (+ Law #14
review before program adoption).

## 10. Evidentiary verdict standard (binding on the H1–H5 synthesis)

The ONLY permitted verdict categories for a hypothesis against a
pre-registered falsification criterion:

- **Supported:** evidence directly survives the pre-registered falsification
  criterion.
- **Not supported:** the criterion was tested and the evidence failed it.
- **Inconclusive:** the experiment did not provide a valid discrimination.
- **Underdetermined:** multiple explanations remain compatible with the
  observations.
- **Refuted:** a decisive observation contradicts the hypothesis under the
  stated conditions.

"Interesting," "promising," "mechanistically elegant," and "worth another
experiment" are **NOT evidentiary categories** and may not appear as
verdicts. They may appear, labeled as [INTERPRETATION], only alongside a
verdict from the five above. The synthesizer rejects any H1–H5 candidate
assessment whose conclusion is one of the four banned phrases without a
verdict. The mentor will treat H1–H5 results as evidence first and theory
second, without rescuing SCBI if the data do not support it.
