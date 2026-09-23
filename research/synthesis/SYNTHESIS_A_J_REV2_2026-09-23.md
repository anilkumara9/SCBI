# A–J Synthesis — Revised 2 (LOG-191)

**Commission:** LOG-140 (CEO) · **Assembly:** LOG-158 (synthesis assembler) · **Targeted revision:** LOG-187 (revision drafter, mentor-ordered) · **Targeted patch:** LOG-191 (patch drafter, mentor-ordered — this file)
**Date:** 2026-09-23 · **Patches:** `research/synthesis/SYNTHESIS_A_J_REV_2026-09-23.md` (LOG-187 — immutable, untouched by this patch) · **Revision chain:** LOG-158 (immutable) → LOG-187 (immutable) → this file (LOG-191)
**Spec:** `research/synthesis/SYNTHESIS_SPEC.md` (binding, §§1–10) · `research/synthesis/REVISION_EDIT_SPEC_2026-09-23.md` (E1–E12, binding) · `research/synthesis/STATS_REVISION_DRAFT_2026-09-23.md` (binding, §§1–4)
**Inputs:** LOG-187 revision (source text, copied verbatim then patched) · LOG-190 (mentor's second review — 9-criterion audit, five required fixes) · LOG-193 (mentor's final adoption-gate criteria — the five defects to be CLOSED, not discussed) · Appendix V (fresh-object Law #3 verification, 2026-09-23 — authoritative for every load-bearing citation in this file; supersedes LOG-185's literature record wherever statuses changed)
**Analysis/writing only.** No GPU used. No experiments run. No signed protocol, primary artifact, or the mentor review file modified. Δθ=0 throughout.
**Status:** targeted patch draft for Law #14 review (LOG-192, pre-assigned) before program adoption; G/H pre-registration triggers on this patch landing (spec §4). The mentor re-reads this file as a fresh object.

**Knowledge-protocol discharge.** Read before writing, in the mandated order:
`SYNTHESIS_SPEC.md` (full) → `CLUSTER_A_2026-09-23.md` (full) →
`CLUSTER_B_2026-09-23.md` (full) → `CLUSTER_C_2026-09-23.md` (full), plus the
repo `AGENTS.md` (14 laws, 10-label standard), plus the five revision inputs
above in full (LOG-158 original; LOG-185; LOG-186 ruling as issued;
STATS_REVISION_DRAFT; REVISION_EDIT_SPEC). Cluster A/B/C each discharged
their own reading protocols (their §0 records); this synthesis does not
re-audit their sources and cites their FACTS as given, reinterpreting only
where marked.

**Labeling convention** [DEFINITION]: every load-bearing claim carries the
canonical pair (FACT / INFERENCE / HYPOTHESIS / SPECULATION) **and** the repo
10-label, e.g. `[FACT]/[OBSERVATION]`. Mapping: FACT → `[FACT]`/`[THEOREM]`/
`[OBSERVATION]`; INFERENCE → `[INTERPRETATION]`/`[PROPOSITION]`; HYPOTHESIS →
`[HYPOTHESIS]`; SPECULATION → `[CONJECTURE]`/`[OPEN]`. Every claim states its
evidentiary level: **L1** = can improve inference ≠ **L2** = changes the
computational strategy ≠ **L3** = creates qualitatively new capability — no
silent crossing. Verdicts use ONLY: Supported / Not supported / Inconclusive /
Underdetermined / Refuted. The words "interesting," "promising," "elegant,"
"worth another experiment" never appear as verdicts.
**Statistical decision protocol (binding, findings #2/#3):** every primary
comparison reports Δ̂M with the exact two-sided 95% confidence interval for
the paired difference; δ_min = 0.05 (5pp); verdicts follow the four-cell
mapping (L > δ_min → Supported; U < 0 → Not supported; U < δ_min →
Not supported via equivalence-to-null; otherwise Inconclusive — held, never
culled). The string "p ≥ 0.05" never appears as evidence against a candidate.
Box-1 "p<0.05" gates throughout §§E–H are read as "p<0.05 AND lower 95% CI >
δ_min". Full protocol: §G1b (universal CI+margin rule, negative-control rule,
hierarchical alpha budget).

**Organizing question (P1, mechanism-level)** [DEFINITION]: *What discovery
would have to be true for a frozen model to become far more cognitively
capable through inference-time computation?* Canonical objective:
θ_after = θ_before; temporary computational state (B_t, z_t, C_t, M_t, …)
evolves during inference. The bar is qualitatively new computation, not
benchmark scores.

---

# A. Strongest current interpretation of SCPM evidence

*Grounded in SYNTHESIS_SPEC §2 FACTS and Cluster B's evidence audit. Each
interpretation states its level.*

## A1. The boundary I1 — the best-evidenced proposition in the corpus

[FACT]/[OBSERVATION]: Raw cross-vocabulary cosine of relational contrast
directions is +0.7186 (EXP065, pythia-160m) and +0.6852 (EXP066, pythia-410m)
with no alignment; static injection of the aggregated basis B_agg yields
ΔM = 0.0pp (b=c=0, McNemar p=1.0) with verified headroom (19 and 26 rescuable
errors). **Verdict: Supported** — the rescue is ruled out (exact-zero paired
difference, b=c=0 in both experiments: the equivalence-to-null cell at the
practical margin) while raw geometric similarity ≈0.7 is observed; the
dissociation as a boundary proposition is Supported. Level: a *constraint*
on L1 claims — it is below L1, a boundary claim, not a capability.
[INFERENCE]/[INTERPRETATION]: raw geometric similarity (≈0.7 cosine) is
**observed**; semantic common structure is **not established** until
anisotropy-controlled nulls support it (cf. §B1: anisotropy inflates cosine
similarity — the two statements cannot both carry strength, and the
anisotropy caveat wins). The licensed dissociation is narrower: geometric
similarity without causal transfer under static injection. No mechanism
claim above L1 is licensed by the cosine value.

## A2. The dynamic-Procrustes conditions tested a scrambled basis — Inconclusive, not Not supported

[FACT]/[OBSERVATION]: recomputation shows the EXP065/066 Procrustes step
reduced cross-vocabulary cosine to +0.0032/−0.0118 (Δcos = −0.7154/−0.6971);
the operator was a rank-≤2 unembedding-space fit applied to full-rank
hidden-state directions — mathematically unsound (rank-deficiency Lemma,
[THEOREM] per the independent math audit). EXP067 halted at Stage A
(rank 33/64, gap 1.59e-08 < 1e-6 — full-rank Procrustes underdetermined).
**Verdicts:** "aligned-basis injection fails to rescue": **Inconclusive**
(never tested); "sound dynamic alignment rescues": **Inconclusive** (no sound
operator has been tested). The synthesis does not collapse these into
"Not supported" — the distinction licenses EXP067's scope. Level: below L1.

## A3. The output bridge rescues decisions — readout-path steerability, label-informed in every demonstration

[FACT]/[OBSERVATION]: same-layer unembedding-derived direction rescues
(exact-score (Tango) two-sided 95% CIs for the paired difference, re-analysis
of the stated (b, c, N); δ_min = 0.05):
EXP064 +5.0pp (b=3, c=0, N=60; CI [−0.0132, +0.1370]);
EXP065 +16.67pp (b=10, c=0, N=60; CI [+0.0931, +0.2803]);
EXP066 +13.33pp (b=8, c=0, N=60; CI [+0.0651, +0.2417]);
EXP077 GPU official +10pp (56.67%→66.67%, b=6, c=0, N=60; CI [+0.0338, +0.2015]);
EXP077 smoke +23.33pp (b=14, c=0, N=60; CI [+0.1444, +0.3544]);
EXP070 C7 +16.67pp (b=10, c=0, N=60; CI [+0.0931, +0.2803]).
**Verdict: Supported** — the option-informed construction repeatedly produces
causal decision changes: strong evidence of **steerability of the readout
path**. Level: L1. Margin-clearing (lower CI > δ_min): EXP065, EXP066, EXP070 C7,
EXP077 smoke clear the practical margin; EXP077 official is directional (CI excludes 0) but does not clear δ_min — held as directional
steerability evidence, not a margin-clearing demonstration; EXP064 is
underpowered (CI includes 0) — held, not killed.
**Validity notes the synthesis carries (Cluster B audit):** (i) EXP077's
+10pp does not clear δ_min at 95% confidence (L=+0.0338 < 0.05) and does not
survive the Level-2 multiplicity budget (two-sided p=0.03125 > α₂=0.00714) —
a directional positive control, not a margin-clearing demonstration;
(ii) EXP066's lower CI (+0.0651) clears δ_min — a fourth margin-clearing demonstration; (iii) the smoke-vs-official magnitude gap (+23.33pp local vs
+10pp official GPU) is a reproducibility red flag on *magnitude* — the
direction replicates, the size does not; no pp number is cited as a stable
quantity.
[INFERENCE]/[INTERPRETATION]: the target layer's readout is causally
accessible to this construction. The rescue *mechanism* (readout bypass vs
attention re-routing) is [CONJECTURE]/[OPEN] — asserted by the forensic audit
(Finding 4) but never discriminated. Crucially (reframing, finding #4): these
are repeated demonstrations of **one** option-informed construction
(normalize(E[target]−E[foil])), not independent confirmations of an
autonomous output-side cognitive mechanism — they share one construction
confound, the exact confound K1/K3 are designed to expose. Per track-2
charter duty, the bridge is currently best described as *a steering direction
coupled to the readout*, not a demonstrated causal representation of
relational content.
**Law #7 caveat (Cluster A CHALLENGE, binding on §C/§H):**
[FACT]/[OBSERVATION]: every bridge construction in the corpus uses candidate
option tokens (normalize(E[target] − E[foil])). On the letter of Law #7,
the rescues prove "the readout is causally accessible to an option-informed
direction" — the step to "a label-free autonomous system can exploit the
output side" is [CONJECTURE]/[OPEN] without a license. The corpus contains
neither a demonstrated causal representation nor a demonstrated autonomous
mechanism; it contains a steering direction and a boundary. That is the
honest L1 picture.

## A4. G1 killed the §3.3 null-space sentence as a QK-subspace claim

[FACT]/[OBSERVATION]: Ē_QK(B_agg)=0.389985 ≥ null 95th percentile (0.361730),
p_low=1.0; Ē_QK(bridge)=0.356185, mid-null (p_high=0.2277); OV corroborates
(0.406759 vs 0.353308, null band 0.3466–0.3590); B_wrong=0.4885 QK with
ΔM=0 (visible ≠ causal — second dissociation); "maximize QK-projection
energy" rejected as a design objective (aggregation-matched s̄=0.367099 ≥
bridge; the s_j median guardrail fired by only +0.000016 — razor-thin, not
leaned on); L20 sensitivity preserves ordering. **Verdict: Refuted** (the
specific claim that downstream heads project the failed direction into their
null space while the bridge enjoys privileged QK access). Mechanism status:
readout-misalignment-or-unknown [CONJECTURE]/[OPEN]. The QK-subspace operator
program is stood down — correctly. Level: below L1 (a refutation).

## A5. EXP077: five static-geometry rooms dead, under a narrow license

[FACT]/[OBSERVATION]: radial α∈{0.25,0.5,1.0,2.0}, cone-vs-line,
cone-vs-control, offset, replication — all ΔM=0 (b=c=0, N=60 per room);
branch (c) NEITHER. Per-room exact 95% upper bound on any rescue: 0.0602
(a single room alone cannot rule out the margin); pooled across the five
rooms (300 items, zero discordant pairs) the exact 95% CI for the paired
difference is [−0.0126, +0.0126] — U=0.0126 < δ_min = 0.05.
**Verdict: Not supported** (static geometric variants rescue decisions) —
via the equivalence-to-null cell on the joint evidence — *within the
licensed bounds* (unconditional ρ=30° cone, α=1.0 offset,
Pythia-410m/L20). Gated and conditional variants survive — the kill is
narrow by design.

## A6. EXP070 and EXP079: the loop's ceiling was never measured

[FACT]/[OBSERVATION]: EXP070 branch (c2) UNINFORMATIVE_PROBE — baseline
68.33% (41/60); C2 static +0.00pp; C3 oracle-selected +0.00pp; C7 bridge
+16.67pp (p=0.001953). The probe carried no transferable signal — no ceiling
measured. EXP068 survives (pool-homogeneity reading). EXP079: signed probe
rule infeasible by construction (max N_final=46<50 over ALL valid 75/75
splits) — a process failure (probe-feasibility algebra never computed), now
a standing pre-registration gate. **Verdict on "an oracle ceiling exists for
the loop": Inconclusive.** Nothing in the corpus licenses an L2 claim for
any SCPM mechanism. The per-instance G/E/S/T loop — the only formulation
distinction SCPM has over CAA — has never faced a discriminating test; its
E-validity remains [CONJECTURE]/[OPEN].

## A7. EXP078 localizes the bridge's power outside the concept subspace — a clue, not a demonstration

[FACT]/[OBSERVATION]: median projected bridge energy 0.054399 < 0.10 —
ENERGY_GATE_HALT. [INFERENCE]/[INTERPRETATION]: fifth demonstration that the
option-informed construction's causal power localizes outside the tested
concept subspace — a localization clue for readout-path steerability (still
Underdetermined as a causal demonstration), compatible with the alternative
"the subspace/projection metric is wrong" — hence **Underdetermined** as a
causal demonstration.

## A8. Handover-era score gains are P2-observations, not identity

[FACT]/[OBSERVATION — numbers verified 2026-09-23 against primary repo
artifacts, Appendix V; these are P2 score observations on Pythia-160m,
not capability claims]:

- EXP048 (regression lock): baseline 0.60 → intervention 0.74,
  ΔM=+14pp, b=7, c=0, McNemar p=0.0078125
  (`experiments/runs/EXP048_regression_lock/exp048_regression_results.json`).
- EXP049 (multi-seed invariance): pooled baseline 0.60 → intervention 0.67,
  ΔM=+7pp, b=17, c=3, p=0.0012884, 95% CI [0.03, 0.115]; per-seed
  significance fails on at least one seed (seed 42: p=0.363);
  metadata verdict FALSIFIED_OR_WEAK
  (`experiments/runs/EXP049_multi_seed_invariance/exp049_multi_seed_results.json`).
- EXP056 (autonomous lifecycle): unsupervised-selected 0.64 vs baseline
  0.60 (+4pp autonomous; oracle span 0.74); b=2, c=0, exact McNemar
  p=0.25 one-sided (0.50 two-sided) — **not statistically significant**;
  verdict SELECTION_BOTTLENECK_ACTIVE
  (`experiments/runs/EXP056_autonomous_lifecycle/exp056_autonomous_results.json`).
  The +4pp belongs to EXP056, not EXP057.
- EXP057 (blind discovery): blind autonomous 0.4083 vs baseline 0.45
  (−4.2pp); verdict DISCOVERY_BOTTLENECK_PERSISTS
  (`experiments/runs/EXP057_blind_discovery/exp057_discovery_results.json`).
- EXP058 (basis transfer): matched causal→causal transfer 0.5333 vs
  baseline 0.60 (−6.7pp); verdict TRANSFER_WEAK_OR_SPECIFIC
  (`experiments/runs/EXP058_basis_transfer/exp058_transfer_results.json`).

Level: L1 score gains; forced baselines (debate/MoA, STARS, DEER,
∇-Reasoner, bigger frozen model at matched compute) were never run — they
are measurements, not capability claims. Selection context is unverified
and matched compute was not enforced; whether the +14pp/+7pp survive a
modern audit (decision endpoints, matched compute, forced baselines) is
[OPEN]/[OPEN].
**Constraint:** the synthesis may cite Layer-8 linear SCBI +14.0pp only as
"per EXP048 primary artifact, selection context unverified, matched compute
not enforced" — a measurement awaiting audit, never stacked with other
results.

## A9. Margin endpoints are inadmissible; only decision changes count

[FACT]/[OBSERVATION]: B_wrong moves margins with p=1.2e-08 while b=c=0;
the "aligned" intervention shifted margins negatively (−0.041, p=1.6e-11)
with ΔM=0. Margin-shift significance ≠ causal evidence. Standing audit rule:
only McNemar decision-flip endpoints count.

## A10. EXP023 — lineage ruling applied (LOG-186)

[FACT]/[OBSERVATION]: per the LOG-186 lineage audit, the "configuration
grid" never existed — L∈{2,4,6,8,10} was EXP013's configuration and the
45-condition factorial was EXP030's. EXP023 was seed-123 dev selection →
one pinned config (G4, E_CF, O5, L=8, r=2, α=0.25) → seed-84 confirmatory.
No Bonferroni precommit was made. The reported result: Seed 84 +7.0pp,
N=100, CI [+0.0300,+0.1200]; Seed 168 +6.0pp; pooled b=14, c=1, p=0.000488.
**Verdict: Supported (L1, selection-optimism caveat).** The caveat, precisely:
the pooled p=0.000488 is reported with the pre-specification caveat —
winner's-curse optimism from the seed-123 dev-selection step is unquantified — the mechanism was selected among 5 on N=20 dev, and L=8 was inherited from EXP013's grid —
(the dev audit that froze the config is not a pre-registered confirmatory
design); the "AUTONOMOUS SCBI CONFIRMED" wording is not licensed; any L1
claim built on EXP023/024 requires fresh confirmatory replication with the
config frozen before data contact; no L2 license flows from this result
under the §G1b decision framework. Level: L1.

## Strongest interpretation, synthesized (tracks 1+2+3+4+8)

[INFERENCE]/[INTERPRETATION]: the evidence describes a frozen transformer
with two causally distinct regions at the intervention layer: **(i)** a
readout path that is causally accessible to one option-informed construction
(normalize(E[target]−E[foil])) — demonstrated repeatedly (A3), but the
demonstrations share one construction confound and do not independently
confirm an autonomous output-side cognitive mechanism; the mechanism
(readout bypass vs attention re-routing) is undiscriminated and the Law-#7
license is absent, so the interpretive stack above "steerability" rests
entirely on K1/K3 (§H6); **(ii)** an internal relational geometry (raw
cosine ≈0.7, structurally real — though the semantic reading of the cosine
value is suspended pending anisotropy-controlled nulls) that is causally
inert under every static additive intervention tried, for reasons unknown
(the QK null-space account is refuted; alternatives are open conjectures).
The *inert* half is the better-evidenced half. No result in the corpus
reaches L2 or L3. The program's live dynamic-loop bet (EXP068, signed) is
the only surviving empirical path to L2; its load-bearing assumption is
E-transfer (the §4b transfer-probe lesson: E-validity that doesn't transfer
is an instrument verdict, not a loop verdict).

---

# B. Strongest arguments SCPM is NOT fundamentally novel

*Cluster A attacks; Cluster B maps. Equivalence claims are
[INFERENCE]/[INTERPRETATION] per Cluster B's verified audit unless marked.*

## B1. The static mechanism is operator-equivalent to CAA / Activation Addition — total equivalence, N0

[FACT]/[OBSERVATION] (verified audit): v = h̄₊ − h̄₋, h ← h + c·v, frozen
backbone, inference-time. Contrastive Activation Addition (Rimsky et al.,
ACL 2024; arXiv:2312.06681) and Activation Addition (Turner et al., 2023;
arXiv:2308.10248) are the same operator; SCBI's B_agg is a mean contrast
direction applied additively — aggregation over instances and vocabulary
mapping are preprocessing, not a new operator. **This is the killing attack:**
the EXP059–066 static program is a Known Combination (N1 overall, **N0 for
the tested mechanism**). The dynamic-Procrustes conditions cannot rescue it —
the operator was unsound (A2). Supporting fire: SCBI omitted anisotropy
correction (Jorgensen et al., 2023; Ethayarajh, 2019 — the ~0.7 cosine likely
inflates the bias direction: a methodological *deficit* vs prior art, and the
caveat that wins over the cosine's semantic reading in §A1); its
nulls were predicted by the steering literature (Tan et al., NeurIPS 2024;
Braun et al., 2025); alignment ≠ causal transfer was already established
(model stitching, Bansal et al., 2021); the Procrustes recipe is 2013/2017
math (Mikolov; Smith et al.), and SCBI's instance was defective.

## B2. Per-instance adaptivity is a searched cluster, not a new principle

[INFERENCE]/[INTERPRETATION]: even a *sound* R(x) would be "fit a coordinate
transform from premise embeddings at test time, apply to a steering
direction" — inside search clusters C (coordinate transforms, adaptive
bases) and D (hidden-state intervention) of the literature README. The
per-instance adaptivity is SCPM's only candidate formulation distinction
over CAA, and it is [CONJECTURE]/[OPEN] — never a discriminating positive.

## B3. G/E/S/T is search-based inference with an unsupervised selector — Family C

[INFERENCE]/[INTERPRETATION]: candidate generation + self-supervised
evaluation + selection + injection = literature cluster E (inference-time
search) composed with cluster F (self-consistency decoding). Best-of-K with
an unsupervised selector is a Known Combination. The 2026-09-11
falsification criterion #3 (a forward-pass-matched sampling baseline beating
the loop) was pre-registered and **never run** — EXP070 returned
UNINFORMATIVE_PROBE. A novelty claim for the loop with zero discriminating
evidence is theory preservation, not science.

## B4. Self-Refine maps onto G/E/S/T; PPLM occupies the dynamic-intervention slot since 2020

Self-Refine (Madaan et al., NeurIPS 2023; verified 2026-09-23 from the
NeurIPS abstract, Appendix V): frozen model, generate → self-critique →
refine at inference — the same LLM serves as generator, feedback provider,
and refiner; no supervised training data, no additional training, no
reinforcement learning; outputs preferred over one-step generation by
humans and automatic metrics across 7 tasks (~20% absolute average gain),
at test time with one model.
**Breaks at:** search object is text y, not bases B; refinement, not
selection. **Falsifier-risk note (not a verified limitation):** the LOG-158
text asserted Self-Refine's gains plateau after 2–3 iterations and that
self-critique has blind spots — neither claim appears in the verified
abstract and neither was verified against the primary source on 2026-09-23.
Those sentences are withdrawn as factual claims. The residual
falsifier-risk is restated honestly as [HYPOTHESIS]: *if* a self-critique
mechanism cannot see its own errors, an internal evaluator E built on the
same principle cannot select better bases — the risk stands as a hypothesis
under test (EXP068), not as a cited limitation.
PPLM (Dathathri et al., ICLR 2020; verified 2026-09-23, Appendix V): frozen
LM, per-instance inference-time updates to hidden activations
ΔH_t guided by an evaluator, Δθ=0. **Breaks at:** external label-trained
evaluator (vs claimed internal self-consistency); trajectory vs basis
search object; gradient steps vs generate–evaluate–select. "Per-instance
inference-time representation intervention of a frozen model guided by an
evaluator" has been occupied since 2020; the remaining distinction (internal
evaluator × basis-valued object) is [CONJECTURE]/[OPEN] under its first
test (EXP068), not a result. Tree of Thoughts (Yao et al., 2023) is
algorithmically isomorphic to G/E/S over bases — domain shift (y → B) does
not clear N1.

## B5. The field has shipped the adjacent possible — ∇-Reasoner, Activation-LQR, DEER, STARS

**∇-Reasoner (Wang et al., ICLR 2026; arXiv:2603.04948)** [FACT]/[OBSERVATION,
mechanism claims verified 2026-09-23 from the arXiv abstract (Appendix V);
the 80.4%/MATH-500/Qwen-2.5-7B-Instruct/GRPO figures below rest on the
LOG-185 web-search verification and were not re-checked against the full
text today]: test-time gradient descent on token *logits* (Differentiable
Textual Optimization), frozen model, iterative refinement of the model's own
output representations, no weight updates; 80.4% on MATH-500
(Qwen-2.5-7B-Instruct, up from 71.2% greedy); matches GRPO at 10–40% fewer
model calls than Best-of-N. The program's own evidence says causal power lives
output-side — **and that room already has a 2026 occupant that works**,
gradient-based with a reward model, more compute-efficient than sampling
baselines. Any SCBI output-side loop must beat ∇-Reasoner at matched compute
(standing law) and explain why gradient-free self-consistency would beat
gradient-based optimization with a reward model. The burden is on SCBI, not
the field.
**Activation-LQR — "Local Linearity of LLMs Enables Activation Steering via
Model-Based Linear Optimal Control" (Skifstad, Yang & Chou, ICML 2026;
arXiv:2604.19018)** [FACT]/[OBSERVATION, mechanism claims verified
2026-09-23 from the arXiv abstract (Appendix V); ICML 2026 venue per the
LOG-185 proceedings-listing check (entry 3288)]: layer-wise Jacobians linearize
transformer dynamics (LTV); LQR feedback controllers drive activations toward
semantic setpoints in *closed loop* with formal tracking-error bounds, no
fine-tuning, no parameter updates. This is the field's existence proof that
dynamic closed-loop representation control of a frozen model works with
guarantees — it occupies H1's slot with stronger validation than anything in
SCBI. It (a) validates the adaptive-loop *bet* (closed-loop > open-loop
steering); (b) sets the bar — SCBI's loop must beat or clearly differ from
A-LQR at matched compute, or its H1 candidacy is "closed-loop control, but
open-loop-evaluated and unbounded" — strictly weaker than the art.
**DEER (Yang et al., 2025; arXiv:2504.15895)** [FACT]/[OBSERVATION, verified
2026-09-23 per Appendix V]:
training-free, confidence-gated early exit; 19–80% shorter CoTs, +0.3–5.0%
accuracy, 11 models / 10 benchmarks. It allocates compute (exit/stop), not
representations — and it is **L2 evidence already demonstrated by the field
without any representation construction**. It is a forced baseline with
teeth: any SCBI claim to L2 must show a strategy change DEER-style routing
cannot already deliver at matched compute. **STARS (Yang et al., 2026;
arXiv:2605.26733)** [FACT]/[OBSERVATION, verified 2026-09-23 from the arXiv
abstract (Appendix V)]: a *training* framework (violates Δθ=0) that
constrains looped-LM latent states toward asymptotically stable fixed points
via efficient Jacobian Spectral Radius Regularization with random loop
sampling — motivated precisely by the observation that looped-LM performance
peaks at some iteration depth and then *collapses* with further recurrence.
It is no equivalence threat (training required, hence excluded from the
Δθ=0 core) but a *constraint*: it predicts frozen iterative latent loops
degrade without stabilization ("gain-then-collapse") — a falsifiable
prediction for EXP068-class loops: non-monotonic gains with iteration depth
unless a stabilizer is present.

## B6. The field has moved past open-loop additive steering

[INFERENCE]/[INTERPRETATION]: Activation-LQR (ICML 2026) moves steering to
closed-loop feedback control with tracking-error bounds; static CAA is the
field's *ablation baseline*. A program testing CAA-equivalent mechanisms in
late 2026 is behind the frontier. (Cluster A flag carried: Steering Vector
Fields (Feb 2026) is named per the internal Sept-2026 sweep note only —
**UNVERIFIED**, primary source not retrieved; the literature program must
verify it before the synthesis cites its content. No content claim about
SVF is made here; it is not placed in the §D1 map.)

## B7. No capability claim exists at all

[FACT]/[OBSERVATION]: every positive number in the corpus is L1, and none
beat the forced baselines — because those comparisons were never run. A
capability result without them is a measurement, not a claim (standing law).
There is therefore no *capability* for a novelty claim to attach to.

## Track-7 verdict on "SCPM is fundamentally novel"

- Static family (EXP059–066 + EXP077 static rooms): **Refuted** as novel
  (operator equivalence B1 + killed mechanisms A4 + five dead rooms A5).
- Per-instance G/E/S/T loop formulation: **Inconclusive** (never
  discriminatingly tested; E-validity [CONJECTURE]).
- Per P2, the synthesis is licensed to conclude SCPM is a dead end as a
  mechanism program. **The strongest honest statement for §B:
  SCBI's tested mechanism is prior art; its claimed mechanism is a
  conjecture in a field that has meanwhile produced working instances of
  the adjacent possible.** The one live thread — the loop's formulation
  distinction — survives only as an untested [HYPOTHESIS].
- **Where the attack breaks (honesty):** if E-validity were demonstrated —
  a label-free evaluator selecting activation-space candidates above
  chance-matched baselines at matched compute — the loop would be an
  N2-candidate formulation distinction (self-consistency selects over
  *outputs*; the loop would select over *activation operators* — a real
  structural difference). That experiment has never been run.

---

# C. Strongest arguments a genuinely new research direction exists

*What the negatives leave open. Highest licensed claim: L1 with paths to L2
tests. No L3 evidence anywhere — stated explicitly.*

## C1. The output-side room is real, unfalsified — and carries a Law #7 caveat that gates everything

[INFERENCE]/[INTERPRETATION]: the bridge demonstrations (A3) repeatedly show
causal decision changes with c=0 — but under the §A3 reframing these are
repeated demonstrations of one option-informed construction's readout-path
steerability, not independent confirmations of an autonomous output-side
mechanism. EXP078 localization puts the construction's causal power outside
the tested concept subspace (A7). The negatives killed *concept-geometry
steering*, not *output-coupled steering*. What is genuinely new is not the
bridge (logit steering is old) but the program the corpus has not run:
inventing output-coupled directions **without label access** —
donor-bridge transfer (§E candidate E8), pending the H6 battery.
**Load-bearing (strengthening, finding #4):** this reframing *raises* the
weight of K1/K3 — they are not minor diagnostics; a K1 tilt-verdict collapses
the entire output-side interpretive stack (§H6). The bridge is no longer
double-counted as converging evidence for an output-side mechanism; it is
one confounded construction awaiting adjudication.
**Caveat (binding):** every bridge demonstration is option-informed (A3).
Until the §H K3 Law-#7 audit clears a compliant construction, the
"output-side room" as an *autonomous mechanism* program is
[HYPOTHESIS]/[HYPOTHESIS], not evidence. Level: L1 path.

## C2. The G1 per-head table is a new instrument

[FACT]/[OBSERVATION]: 48 downstream heads measured weight-only, zero forward
passes — B_agg beats the bridge on QK energy in 35/48 heads; cross-head
correlation 0.27 (the two directions are visible to *different* heads, not
scaled versions of one profile). [INFERENCE]/[INTERPRETATION]: the program's
first *measurement-pruned* search-space reduction from the model's own
weights rather than geometry hypotheses. Honest restatement required: G1
refuted the QK-visibility premise, so the pruning hypothesis must be
restated around readout-coupled (OV/unembedding) heads. Level: method (L1
enabler). (Folded into §E as the E3 pruning operator — see reconciliation
appendix R(b).)

## C3. The boundary I1 is a diagnostic instrument

[INFERENCE]/[INTERPRETATION]: the dissociation is not just a result but a
*test* — any future mechanism can be run through "raw geometric similarity
vs. causal transfer" to separate geometric structure from causal structure.
A successor mechanism that *passes* the boundary test (high similarity AND
causal transfer under a sound operator) would be, by construction, doing
something no tested mechanism does.

## C4. Feedback control reframes the loop as a different kind of computation

[HYPOTHESIS]/[HYPOTHESIS]: Activation-LQR (ICML 2026) shows layer-wise
transformer dynamics are locally linear and controllable in closed loop
with setpoints and tracking-error bounds. Reframing G/E/S/T from open-loop
candidate search to closed-loop feedback control changes the *kind* of
computation from feedforward search to feedback regulation — the most
credible path in the corpus from L1 to L2, because the difference (feedback
vs. feedforward) is architectural, not incremental. The discriminating
question is mechanism-level: does closed-loop beat matched-compute open-loop
best-of-K? (§E candidate C1.)

## C5. The bottleneck is the verifier, not the generator — and no verifier has been built

[INFERENCE]/[INTERPRETATION]: EXP070's design, the oracle-vs-autonomous gap,
and the 2026-09-11 falsification criteria all point at *selection* as the
unsolved piece; candidate generation is cheap. A frozen-model verifier that
counterfactually tests candidate interventions without labels
(verifier/controller separation) is a genuinely open architectural question —
the corpus contains no such component (E-validity [CONJECTURE]). The
minimal-new-mechanism answer to the spec's mandatory question:
**"SCPM + a working verifier" is a different kind of inference system than
"SCPM + a better direction."** Level: [HYPOTHESIS].

## C6. The static program's comprehensiveness is a map, not just a graveyard

[INFERENCE]/[INTERPRETATION]: five dead rooms under narrow, honest licenses
(A5) + the G1 kill (A4) + the Procrustes unsoundness proof (A2) jointly say
*where the mechanism isn't* with unusual precision. A successor that avoids
all five rooms (no unconditional static geometry, no QK-subspace operators,
no unsound cross-space fits) starts from a constrained design space — which
is [INTERPRETATION] the evidentiary basis for keeping C1, C4, C5 in the
falsification funnel rather than selecting candidates at random.
Gated/conditional
variants survived EXP077's narrow kill; multi-layer coordination is untested.

---

# D. Prior-art map + novelty boundary

## D1. Map (families; SCBI's position marked)

- **Family A — diff-in-means steering (static):** ActAdd, CAA, RepE-control,
  ITI, Arditi refusal-direction, Subramani latent vectors, Jorgensen
  mean-centring. *SCBI-tested lives here (N0).*
- **Family B — linear cross-space alignment:** Mikolov (2013), Smith (2017),
  model stitching, DAS. *SCBI Stage-A mapping lived here (defective instance).*
- **Family C — inference-time search + self-evaluation:** self-consistency,
  ToT, Self-Refine, LLM-Monkeys, rStar-Math (MCTS+PRM), PPLM
  (gradient-guided hidden-state search, external evaluator).
  **LTPO** (Ye, Liang & Shan, arXiv:2510.04182 — arXiv preprint, no venue):
  parameter-free test-time optimization of latent thought vectors on a frozen
  LLM; online policy gradient guided by an intrinsic confidence reward
  computed from the frozen LLM's own output distributions; no parameter
  updates, no external supervision. Occupies the general "frozen model +
  per-instance latent optimization + internal signal" slot.
  **NoisyCoconut: Counterfactual Consensus via Latent Space Reasoning**
  (Jerge & Evans, TMLR June 2026 — published; status and mechanism verified
  2026-09-23, Appendix V): inference-time method operating directly on model
  representations, no retraining; controlled noise injected into latent
  trajectories to generate diverse reasoning paths; agreement among paths is
  a confidence signal enabling abstention under uncertainty (unanimous
  agreement drives error rates below 15% on math reasoning via selective
  abstention). The pinned comparator (§G3 M15-NoisyCoconut) fixes K=5,
  σ=0.1, abstention removed — program [PINNED-CHOICE]s, not paper claims.
  Occupies "latent branching + aggregation/consensus" generally.
  **Meta-Reasoner** (Sui et al., Findings of ACL 2026; arXiv:2502.19918):
  contextual multi-armed bandits learn an adaptive policy over reasoning
  strategies (backtrack / change decomposition / restart) from a compact
  progress report on the LLM's reasoning state, at inference time; 9–12%
  accuracy gains and 28–35% inference-time reduction under the same compute
  budget. Occupies "test-time-discovered strategy routing" generally.
  *SCBI-claimed loop lives here (conjectured sub-slot, narrowed — see below).*
- **Family D — output-side dynamic optimization (frozen):** ∇-Reasoner
  (Wang et al., ICLR 2026; arXiv:2603.04948 — venue and 80.4% MATH-500
  confirmed per LOG-185): test-time gradient descent on token logits
  (Differentiable Textual Optimization), frozen model, reward-guided.
  *Adjacent; occupied 2026.*
- **Family E — closed-loop representation control (frozen):**
  Activation-LQR — "Local Linearity of LLMs Enables Activation Steering via
  Model-Based Linear Optimal Control" (Skifstad, Yang & Chou, ICML 2026;
  arXiv:2604.19018 — proceedings listing confirmed per LOG-185): layer-wise
  Jacobian linearization (LTV), LQR feedback controllers steering activations
  toward semantic setpoints in closed loop, derived tracking-error bounds,
  no offline training. *Adjacent; occupied 2026.*
- **Family F — adaptive compute routing (frozen, training-free):** DEER
  (confidence-gated early exit). *Forced baseline; L2 already demonstrated
  by the field.*
- **Family G — frozen-backbone representation editing with learning:**
  ReFT/LoReFT, DAS. *Excluded from core SCBI by Law #6 (learned parameters).*
- **Family H — test-time weight adaptation:** TTT and descendants. *Excluded
  by the Δθ=0 boundary.*
- **Family I — training-free latent multi-agent collaboration (new):**
  **LatentMAS** (Zou et al., ICML 2026 spotlight; arXiv:2511.20639):
  end-to-end training-free framework for pure latent collaboration among LLM
  agents — autoregressive latent-thought generation through last-layer hidden
  embeddings, then a shared latent working memory preserving and transferring
  each agent's internal representations and latent thoughts, lossless
  information exchange without re-encoding and without text mediation.
  Occupies inter-instance latent exchange generally.
- **Adjacent excluded — trained-component steering:** **RISER** (Ye et al.,
  Findings of ACL 2026; 2026.findings-acl.226): plug-and-play adaptive
  activation steering — a library of reusable reasoning vectors dynamically
  composed per input by a lightweight Router optimized via reinforcement
  learning under task-level rewards (3.4–6.5% average zero-shot accuracy
  gains). The trained object is the *external router*, not the LLM backbone
  (whose weights are not described as updated) — excluded from core SCBI
  because any trained component violates Law #6, not because the backbone is
  fine-tuned. Not an equivalence threat; retained as adjacent art: dynamic
  vector composition is publishable steering research, and any Δθ=0-
  respecting variant must identify exactly what the trained router
  contributes that a parameter-free mechanism cannot.
- **Not placed — unverified:** Steering Vector Fields (Feb 2026, named per
  the internal Sept-2026 sweep note only): primary source not retrieved; the
  literature program must verify it before the synthesis cites its content.
  No content claim is made.

[INFERENCE]/[INTERPRETATION]: no SCBI component sits outside known families.
**Within the reviewed literature, the remaining potentially distinct slot is
a narrowly defined combination of per-instance activation-operator
construction, transfer-validated internal evaluation, conditional
computation, and Δθ=0 — not generic latent optimization, routing,
cooperation, or branching.**

## D2. Exactly where the novelty boundary would have to be

[INFERENCE]/[PROPOSITION]: a result crosses from N1 to a genuine novelty
claim **iff** it simultaneously demonstrates, pre-registered:

1. **Per-instance construction** — the applied intervention varies
   non-trivially across instances (falsifier: if selected bases collapse to
   a near-constant direction, it is steering with extra steps — Family A,
   not C′).
2. **Transfer-validated internal evaluator** — E's scores track rescue on a
   *held-out distribution* (vocabulary/task), not just the gate distribution
   (the EXP068 §4b lesson: E-validity that doesn't transfer is an instrument
   verdict, not a loop verdict).
3. **Matched-compute superiority over Family C/D/E/F baselines** — beats
   ToT-style search, best-of-N, ∇-Reasoner, A-LQR-style closed-loop, DEER,
   debate/MoA at equal forward-pass budget (standing law; no exceptions) —
   **plus candidate-specific forced comparators at matched compute** (the
   pinned §G3 M15 protocols, executable as written): M15-LTPO (H1-family:
   C1, DPRS), M15-MetaReasoner (H4: ASR — activated only when ASR's policy
   scope is frozen), M15-LatentMAS (H5a: LCMIC), M15-NoisyCoconut (H5b: CLB).
4. **Conditional computation (the track-3 bar)** — the loop's gain depends on
   intermediate computed quantities within the episode: randomizing E's
   measurements (or the feedback signal) must kill the gain. Open-loop
   selection from precomputed candidates does not cross. **This is the P1
   mechanism-level bar operationalized** — it is what makes the computation
   *new* rather than *more*.
5. **Specificity** — the selected intervention passes a specificity-gap test
   against matched structural controls (the EXP059 lesson): Δ_valid −
   Δ_control > 0, pre-registered.

Conditions 1–5 are individually necessary and jointly sufficient for the
boundary crossing. EXP068 (signed) tests 1–3 partially (ρ-gate + §4b
transfer probe + kill criteria F1–F5) but not 4 (conditionality) or 5
(specificity).

> **Changed burden of proof (standing — the mentor review's closing burden note, unnumbered):** the next experiment
> does not merely demonstrate that one of the seven complete mechanisms works. It must
> demonstrate that what works is **not already explained by the newer prior
> art** (LTPO, LatentMAS, NoisyCoconut, Meta-Reasoner — LOG-185 verified). A
> positive result that a 2026 occupant predicts at matched compute is a
> replication of prior art, not a novelty result — verdict Not supported for
> the novelty claim (engineering value assessed separately under the
> demote-to-engineering logic).

## D3. The experiment that would cross it — EXP068 + the conditionality probe, absorbed into §F1

[HYPOTHESIS]/[PROPOSITION]: after the loop runs, re-run with E's
per-instance measurements replaced by randomly permuted measurements (same
marginal distribution, broken instance-linkage). Pre-registered decision
rule (stats revision, finding #2): report Δ̂ = ΔM_loop − ΔM_permuted-E with
the exact two-sided 95% CI; if the CI rules out a δ_min strategy
contribution (U < δ_min = 0.05), the loop's gain does not depend on its
computed quantities — verdict **Not supported** for L2 (it is open-loop
selection). If the CI overlaps δ_min → **Inconclusive** (the ablation is
underpowered) — the candidate is held for a powered re-test, never culled
on this cell. If the gain survives only with true E (lower CI > δ_min) and
beats the Family C/D/E/F battery at matched compute, with a positive
specificity gap — the boundary is crossed. Either outcome is first-class
science; the probe is cheap (a re-run arm, no new bundle). This design is
preserved as the **named EXP068 instantiation of §F1's adaptive-ablation** —
see reconciliation appendix R(d) for the merge (decision rule updated per
the binding stats revision; see R(h)).

---

# E. Candidate architectures for inference-time cognitive augmentation

*All preserve Δθ=0 by construction (no optimizer, no gradient-applied
parameter update; argument per candidate). All target the organizing question
at the mechanism level (P1). Cost unit: 1F = one forward pass per instance;
ℓ = wall latency; A = activation memory; weights W shared, already loaded.
Derived numbers are [ILLUSTRATIVE] (math charter M3.1) with derivations
shown; regime: pythia-410m-class, single T4. None is assumed correct; none
is [Supported] — all await falsification attempts. FLOP accounting follows
the §G1b two-number rule (online vs amortized); the 1F unit below is online
inference FLOPs per item.*
*Box-1 "p<0.05" gates below are read as "p<0.05 AND lower 95% CI >
δ_min = 0.05" (binding stats revision, finding #2) — no Supported verdict on
significance alone.*

**H1–H5 mapping:** C1→H1 (dynamic representation control, feedback-control
instantiation) · E7/DPRS→H1 (dynamic representation control,
readout-search instantiation) · C2→H2 (ephemeral computational workspace) ·
C3→H3 (test-time program synthesis) · C4→H4 (adaptive cognitive routing) ·
C5→H5a (cooperation, not yet named) · C6→H5b (counterfactual branching, not
yet named) · E8→H5c (donor transfer, not yet named — **conditional** on the
§H bridge battery).

---

## H1 — Dynamic representation control

### C1. Closed-Loop Latent Control (CLLC)

**Mechanism** [HYPOTHESIS]/[HYPOTHESIS]: treat the residual stream as a
dynamical plant steered with *feedback*. Two frozen roles: a **plant**
forward pass generates the trajectory; an **observer** role (same weights,
different prompt-role) reads mid-layer residuals and a **controller**
computes correction u_t = −K·(h_t − h\*) toward a reference state h\*
(pre-registered: the output-bridge direction's induced state OR the mean
correct-answer state — the second option must be used if the §H battery
confirms readout bias; setpoint label-informed only at definition time,
never per test item). Gains K come from layer-wise Jacobians (A-LQR
lineage) computed once per task and cached. Verifier/controller separation
made literal: the controller never generates content; the plant never
evaluates itself.
**Δθ=0** [FACT]/[PROPOSITION]: Jacobians via autograd, gradients wrt
activations only, parameters under no-grad on the update path; all mutations
target activations h_t or the temporary gain cache (discarded); θ_t = θ_0 ∀t.
**Novelty** [INFERENCE]/[INTERPRETATION]: A-LQR (ICML 2026) is the direct
prior: feedback control of activations. CLLC's bid is the
observer–controller–plant separation with cached gains and a pre-registered
error bound evaluated on a *relational* task (A-LQR's bounds were shown on
toxicity/truthfulness-style steering). LTPO (arXiv:2510.04182) occupies the
general per-instance latent-optimization slot; CLLC's surviving distinction
is the feedback-control formulation with an error bound — and the pinned
M15-LTPO comparator (§G3) is the forced H1-family comparator at matched
compute. Honest tier: N1 until the bound holds
on relational reasoning — then N2-adjacent on formulation, operator credit
remaining A-LQR's. **Systems:** per item (uncached) ≈ 4–6F, (cached) ≈ 2F;
latency ≈ 2 sequential forwards + JVP; memory ≈ 2A; pre-registered cost
falsifier: Jacobian conditioning κ > κ_max → no control authority → halt.
> **Box 1 — unique support:** measured setpoint-tracking error stays within
> the pre-registered bound's order of magnitude on the relational task AND
> CLLC rescues items (ΔM>0, lower 95% CI > δ_min) where open-loop injection
> of the *same final correction* (no feedback) does not. Activation-LQR is
> the direct prior for feedback-vs-open-loop control — the claim "no
> competitor predicts bound-holding feedback beating its own open-loop
> ablation" is withdrawn (A-LQR occupies exactly that comparison). The
> surviving distinction is explicitly narrower: the observer/controller/plant
> separation with cached gains, the pre-registered setpoint construction on
> the relational task, and a measured bound-holding result that A-LQR's
> formulation (setpoints on toxicity/truthfulness-style steering) does not
> predict — the mechanism-level differentiation from A-LQR. (C2/C3/C6 have no
> feedback; C4 routes but does not control; C5 debates but does not track —
> none of which distinguishes CLLC from its direct prior.)
>
> **Box 2 — kill:** the A-LQR "faithful-but-inert" cell: ΔM_CLLC = 0 while
> tracking-error bounds hold, OR bounds violated by >1 order of magnitude
> with ΔM = 0. Either way the controller formulation is withdrawn for
> relational reasoning — feedback control is not the missing mechanism.
**Evidentiary target:** L2 (open-loop → closed-loop); L1 gains alone do not
license C1.

### E7. Dynamic Per-Instance Readout-Space Search (DPRS) [from Cluster B IDEA]

**Mechanism** [HYPOTHESIS]/[HYPOTHESIS]: the corpus never tested a dynamic
per-instance loop in *readout space* — EXP068 tests the loop geometry-side,
where the evidence says causality isn't. Per instance x: G — candidate
readout perturbations {δ_j}: sparse logit biases on the model's own top-k
confusion pairs from frozen logits (±β on ordered pairs), |{δ_j}| ≤ 8,
pre-registered, label-free. E — frozen self-consistency over perturbed
rollouts evaluated on a held-out paraphrase x′ of x (paraphrase from the
frozen model; E never sees the test decision). S — δ\* = argmax E. T —
apply δ\* to x. The loop's decisions are conditional on per-instance
computed quantities (the track-3 §4.4 bar): E-scores measured within the
episode.
**Δθ=0** [FACT]/[PROPOSITION]: perturbations are activation/logit edits at
inference; no parameter mutation.
**Novelty** [INFERENCE]/[INTERPRETATION]: N1 — Family-C loop in readout
space. LTPO (Ye, Liang & Shan, arXiv:2510.04182) occupies the general
"frozen model + per-instance latent optimization + internal signal" slot —
DPRS cannot claim that slot. The surviving distinction is narrowed to
**readout-space perturbation search specifically**: discrete perturbation
search over the model's own top-k confusion pairs with an internal evaluator
and the §F1 conditionality check. Adjacent art: ∇-Reasoner (ICLR 2026;
gradient-based logit refinement, external reward model — DPRS differs:
gradient-free, internal evaluator, discrete candidates), PPLM (per-instance
hidden-state updates), Self-Refine (output loop). Cited with evidence; no
N2 claim. **Systems:** ~60 × 8 × 2 forward passes on Pythia-410m for the
cheapest falsifying pilot — minutes on 2×T4.
> **Box 1 — unique support:** DPRS ΔM exceeds the static bridge ΔM at
> matched forward-pass budget AND beats the matched-compute
> random-perturbation control (p<0.05 AND lower 95% CI > δ_min), AND the §F1
> conditionality check holds (permuted E kills the gain), AND DPRS beats
> the pinned M15-LTPO comparator at matched compute on the relational task
> (the general slot is occupied; the readout-space-specific claim must beat
> its occupant). No competitor searches readout space dynamically — C1
> controls hidden activations, C5 parallelizes instances, C6 branches within
> the pass.
>
> **Box 2 — kill:** the 95% CI for DPRS ΔM rules out δ_min (U < 0.05), OR
> DPRS does not beat the random-perturbation control → the idea is dead: the
> output-side room contains only label-informed existence proofs, not a
> discoverable dynamic mechanism.
**Evidentiary target:** L2 (new strategy for allocating inference
computation); L3 requires D1–D4 (§5/J).

**H1 discrimination note** [INFERENCE]/[INTERPRETATION]: C1 and DPRS are
mechanism-distinct instantiations of the same hypothesis — continuous
feedback control with an error bound (C1) vs discrete per-instance
readout search with an internal evaluator (DPRS). §F1's adaptive-ablation
separates them (C1: open-loop ablation; DPRS: random-perturbation control);
A-LQR is the forced Family-E baseline for both at matched compute, and
the pinned M15-LTPO protocol is the forced H1-family comparator (§G3).

---

## H2 — Ephemeral computational workspace

### C2. Ephemeral Latent Memory (ELM)

**Mechanism** [HYPOTHESIS]/[HYPOTHESIS]: a runtime RAM outside θ — fixed
scratch buffer M_t of S slots (e.g. S=128, d=1024 → ~0.5MB
[ILLUSTRATIVE]), read/written across T sequential forward passes via
model-generated keys. Pass t emits (key_t, write_t); a fixed addressing
operator (no learned parameters — dot-product attention over slots) routes
write_t into M_t and returns read_t as additional input to pass t+1. θ
untouched; only M_t evolves. Latent workspace construction made
addressable: unlike chain-of-thought (text tokens, no algebra), slots
support compositional operators (slot-add for evidence accumulation,
slot-compare for consistency). **Track-3 constraint (binding):** any H2
candidate must pre-register which of the working-memory criteria it
implements — (a) maintenance over delays with interference/decay,
(b) manipulation not just storage, (c) capacity limits,
(d) content-addressability — and the measurement for each; otherwise
"ephemeral workspace" is a metaphor, not a mechanism.
**Δθ=0** [FACT]/[PROPOSITION]: M_t is a runtime buffer (like a KV-cache);
writes are activation copies, never gradient updates.
**Novelty** [INFERENCE]/[INTERPRETATION]: DNC/NTM (Graves et al.) are the
priors — but those *train* the controller. ELM's bid: training-free
addressing with a frozen controller — memory as *protocol*, not learned
skill. Honest tier: N1 until the read-attention diagnostic shows the model
actually uses slots non-trivially across passes. **Systems:** ≈ T·F,
T ∈ {3..8} pre-registered; latency T sequential passes (binding cost);
memory +0.5MB; cost falsifier: read-attention mass ≈ uniform over slots
→ T·F buys nothing; halt.
> **Box 1 — unique support:** ablating the buffer (T=1, no carryover) at
> matched total FLOPs removes ≥50% of the gain (pre-registered), AND
> read-attention over slots is significantly non-uniform (p<0.05 AND lower
> 95% CI > δ_min vs uniform), AND banked content is causally implicated
> (corrupting a banked slot flips the decision). Among the reviewed
> comparators, no identified method uses ELM's specific fixed-slot,
> externally addressable runtime scratch-buffer protocol — C1/C4/C5/C6
> recompute every pass; C3's "memory" is the synthesized program text, not a
> latent buffer.
>
> **Box 2 — kill:** read-attention ≈ uniform (memory unused) with ΔM = 0,
> OR buffer-ablation at matched FLOPs leaves the gain unchanged (the gain
> was the extra passes, not the memory). Then ELM is "T forward passes with
> extra steps" — withdrawn.
**Evidentiary target:** L2 (accumulate-then-compose vs single-pass); L3
only if banked structures compose *novel* procedures (Stage 3 bar, §J).

---

## H3 — Test-time program synthesis

### C3. Test-Time Program Synthesis with Compiled Execution (TTPS)

**Mechanism** [HYPOTHESIS]/[HYPOTHESIS]: split cognition into *invention*
and *execution* on different substrates. The frozen model **synthesizes** a
short program in a constrained DSL whose primitives are frozen-model calls
(attend-to(span), retrieve(), compare(a,b), compose(f,g),
branch-on(uncertainty)); a **deterministic interpreter** (plain code, ~0F)
*executes* the program, invoking the model only at primitive call sites.
The executed computation is the synthesized program's control flow, not the
transformer's forward pass — "cognitive compilation" literalized. A verifier
role (same weights, separate instance) test-runs candidate programs on
support items and keeps the best rescue-rate-per-primitive-call.
**Δθ=0** [FACT]/[PROPOSITION]: the interpreter is external code; primitive
calls are ordinary forward passes; synthesis is generation. No parameter
mutation anywhere.
**Interpreter capability boundary (pre-registered, finding #7):** the DSL's
instruction set is fixed and enumerated in the pre-registration; bounded
operation count per item (pre-registered cap); no external data at execution
time; no task solver hidden in primitives — each primitive's capability is
documented, and a primitive that alone solves the task class is forbidden;
Operational check: each primitive executed standalone (degenerate single-primitive program) on the NTDP task must yield ΔM with U < δ_min (cannot rescue alone); a primitive violating this is removed from the DSL before TTPS runs;
and the **interpreter-only control cannot solve the task** (pre-registered
check). **Interpreter-only baseline arm:** the interpreter executing a
degenerate/fixed program (or the DSL's primitives composed without model
synthesis) at matched operation budget. **Decision rule:** L3 is licensed
only if the interpreter-only control fails the task while TTPS succeeds; if
the interpreter alone succeeds, the "new capability" belongs to the
interpreter (a programmable computer the model was given), not to the frozen
model — verdict Not supported for L3. "New computation" ≠ "new capability
of the frozen model."
**Novelty** [INFERENCE]/[INTERPRETATION]: program-synthesis priors
(DreamCoder, LEAP) all *train*. Test-time priors: PAL/PoT (single-shot
Python for arithmetic, no search, no DSL over latent primitives). TTPS's
bid: searched, verified programs over *latent* primitives with compiled
execution. Honest tier: N1 (combination) until the complexity audit shows
non-trivial control flow doing causal work. **Systems:** ≈ (K+V)·F ≈ 8F for
K=V=4 [ILLUSTRATIVE]; cost falsifier: program-complexity audit — if ≥70% of
winning programs are straight-line (no branch/recursion/loop) → compiled
execution buys nothing over direct generation; halt.
> **Box 1 — unique support:** the complexity audit shows winning programs
> use branching/recursion/looping on ≥30% of items (pre-registered bar) AND
> replacing compiled execution with "model emits the program's final answer
> directly" (same synthesis FLOPs) removes the gain AND the interpreter-only
> control fails the task while TTPS succeeds (the capability is the model's
> synthesis, not the interpreter's). No competitor executes a
> non-transformer computation — C1/C2/C4/C5/C6 all ultimately run
> transformer forward passes.
>
> **Box 2 — kill:** winning programs are straight-line paraphrases of
> single-pass inference (audit fails the bar) OR direct-emission matches
> compiled execution (the program adds nothing) OR the interpreter-only
> control succeeds (interpreter-sufficiency — the "new capability" belongs to
> the interpreter, not the frozen model). Then TTPS is "expensive
> chain-of-thought" — withdrawn.
**Evidentiary target:** L3 directly (new computation: the interpreter's
control flow) — but L3 is licensed ONLY if the complexity audit passes AND
the interpreter-only control fails; otherwise any gain is L1.

---

## H4 — Adaptive cognitive routing

### C4. Adaptive Strategy Routing (ASR)

**Mechanism** [HYPOTHESIS]/[HYPOTHESIS]: a meta-level router (frozen model in
a probe role: one cheap draft forward; answer-token entropy + self-margin
as difficulty signals) assigns each instance a *computational strategy*
from a pre-registered menu {direct answer (1F), latent search (~2F),
memory-augmented (~4F), verify-heavy (~6F)} — and the routing *policy*
itself is discovered at test time by a bandit over strategies with an
internal reward (agreement + margin, target-free), not fixed by entropy
thresholds. "Cognitive resource allocation" with a learned-at-test-time
allocator.
**Δθ=0** [FACT]/[PROPOSITION]: the bandit's policy is a temporary count
table (part of z_t, discarded); strategies are forward-pass patterns.
**Policy-scope specification (pre-registered, finding #8):** ASR must declare
`policy scope ∈ {per-instance, per-episode, test-stream}`; state explicitly
whether information from example i may affect example i+1; if any
cross-instance state exists, define the formal online-adaptation boundary
(what carries over, what resets per instance/episode, and the Law-#7 audit
of carried state). Without this declaration the adaptivity claim is
inadmissible — the current ASR spec is marked **[INCOMPLETE]** on this point
until the declaration is made. C4/ASR may not enter §F culling or §G NTDP runs — and no Box-1/Box-2 verdict for ASR is licensable — until the policy-scope declaration is pre-registered.
**Novelty** [INFERENCE]/[INTERPRETATION]: EAGER (entropy-gated compute),
mixture-of-depths, early-exit gate *depth/tokens* with fixed rules.
Meta-Reasoner (Sui et al., Findings of ACL 2026) occupies
test-time-discovered strategy routing generally: a contextual bandit over a
strategy menu (backtrack / change decomposition / restart) with 9–12%
accuracy gains at the same compute budget. ASR's surviving distinction is
structural, not "adaptive routing is new": a *test-time-learned allocation
policy* (bandit over strategies with an internal target-free reward) vs
Meta-Reasoner's contextual bandit over a strategy menu — and ASR must beat
or structurally differ from Meta-Reasoner, not reimplement it with a
different menu. Honest tier: N1; the experiment that matters is the
allocative-efficiency comparison (§F1). **Systems:** router probe 1F +
routed strategy; expected ≈ 3.2F at p_h=0.3 heavy-rate [ILLUSTRATIVE]; claim
is *capability per FLOP*; direct falsifier: pre-register total-FLOP parity
vs uniform-heavy — if uniform wins, routing buys nothing.
> **Box 1 — unique support:** the strategy-shift assay (§F1): disabling the
> router (uniform strategy) at *matched total FLOPs* removes the gain
> (Δ>0, p<0.05 AND lower 95% CI > δ_min) AND the router's difficulty
> predictions correlate with actual instance difficulty (AUC > 0.6
> pre-registered) AND the test-time bandit policy clears the pinned
> M15-MetaReasoner comparator at matched compute (Level-2 standard, or the
> §G4 structural-comparison path is licensed). No competitor
> learns an allocation policy of this form — C1 controls, C2 remembers, C3
> compiles, C5 cooperates, C6 branches, all at fixed budgets.
>
> **Box 2 — kill:** router AUC ≤ 0.5 (chance) → pure overhead, withdrawn;
> OR the CI for (ΔM_routed − ΔM_uniform-heavy) rules out δ_min (U < 0.05)
> → allocation buys nothing, withdrawn; CI overlapping δ_min →
> Inconclusive (underpowered), held.
**Evidentiary target:** L2 (new strategy: difficulty-contingent
computation); the capability-per-FLOP framing keeps it honest at L2 even
with large L1 gains.

---

## H5 — Something not yet named

*Two distinct inventions, each independently passing the boxed standard —
both kept (see reconciliation appendix R(b)).*

### C5 → H5a. Latent-Channel Multi-Instance Cooperation (LCMIC)

**Mechanism** [HYPOTHESIS]/[HYPOTHESIS]: R frozen instances in fixed roles
— **proposer** (generates), **critic** (reads the proposer's *mid-layer
residuals*, not its output tokens; emits a latent critique = direction +
scalar doubt), **arbiter** (reads both residual streams, issues the
decision) — communicating through a *latent channel* (activation tensors
exchanged between roles' forward passes) over D rounds, not through text.
The claim: mid-layer residual exchange carries more task-relevant bandwidth
per FLOP than text debate (the critic sees *why* the proposer is leaning,
not just *what* it said). The entire bid is the channel — §F3 isolates it,
including the bandwidth control (arm (e)), which separates the
channel-representation claim from raw channel capacity.
**Δθ=0** [FACT]/[PROPOSITION]: roles are prompt-role framings; exchanged
tensors are activations.
**Novelty** [INFERENCE]/[INTERPRETATION]: Debate (Irving et al.), MoA
(Wang et al.) are text-channel forced baselines. LatentMAS (Zou et al.,
ICML 2026 spotlight) is a training-free multi-agent framework with shared
latent working memory — "latent-channel cooperation" as such is a prior-art
family, and the claim that no competitor uses inter-instance latent exchange
is retracted (it was false). LCMIC's surviving hypothesis is
formulation-level, not "latent cooperation is new": **same frozen backbone
+ causal residual exchange + verifier/arbiter separation + relational-task
intervention**. The claim is that *this formulation* beats text-channel
debate/MoA and the pinned M15-LatentMAS collaboration protocol at matched
compute on the relational task — not that latent cooperation is novel.
Honest tier: N1 (multi-agent inference is well-trod); the F3 ablation is the
experiment that could promote the *channel* claim. **Systems:** R·D·F = 6F
for R=3, D=2 [ILLUSTRATIVE]; latency D sequential rounds; cost falsifier
(§F3): text-only ablation at matched token budget matches latent-channel
performance → the channel buys nothing; it's just debate.
> **Box 1 — unique support:** the §F3 ablation — latent-channel beats
> text-only (same roles/rounds/token budget; lower 95% CI > δ_min) AND beats
> the §F3 arm-(d) M15-LatentMAS ablation (same roles/rounds/budget;
> lower 95% CI > δ_min) AND the bandwidth-isolation arm (e) matches full
> latent (a) at the practical margin (U_(a−e) < δ_min — the raw-capacity
> account is ruled out; §F3 licensing rule) AND text-only ≈ debate/MoA
> forced baseline (the roles add nothing by themselves) AND the critic's
> latent doubt scalar predicts proposer errors above chance (the channel
> carries signal, not noise). If the M15-LatentMAS ablation matches, LCMIC
> reduces to prior art — culled. If full latent (a) beats the
> payload-compressed arm (e) (L_(a−e) > δ_min), the channel advantage is raw
> capacity, not mechanism — the channel-representation claim is withdrawn.
>
> **Box 2 — kill:** the CI for (ΔM_latent − ΔM_text) rules out δ_min
> (U < 0.05) → the channel is decorative; LCMIC reduces to debate and is
> culled (N1, no further spend); CI overlapping δ_min → Inconclusive, held.
**Evidentiary target:** L2 (new strategy: latent-bandwidth cooperation);
L1 gains without the ablation win are just "more agents."

### C6 → H5b. Counterfactual Latent Branching (CLB)

**Mechanism** [HYPOTHESIS]/[HYPOTHESIS]: inside *one* forward pass, fork the
residual stream at layer l\* into K counterfactual branches — each branch
continues through the remaining layers conditioned on a different
hypothesized world-state (e.g. different relational hypotheses, injected as
branch-specific bias vectors that are themselves generated, not hand-set) —
then a **merge operator** (not selection: e.g. consistency-weighted averaging
of branch logits, or minimum-description-length arbitration over branch
trajectories) produces the decision. Unlike Best-of-N (K full passes +
pick-a-winner) the prefix is shared and branches are *latent* (never
decoded); unlike Tree-of-Thoughts there is no text. The merge operator —
arbitration over counterfactual trajectories rather than selection among
finished outputs — is the claimed new computation.
**Δθ=0** [FACT]/[PROPOSITION]: forking duplicates activations, not
parameters; branch biases are activation edits (hook pattern, cf. loop spec
§2.2).
**Novelty** [INFERENCE]/[INTERPRETATION]: Best-of-N / self-consistency
(output-level), ToT (text-level branching). NoisyCoconut (Jerge & Evans,
TMLR June 2026 — published; verified 2026-09-23, Appendix V) occupies
frozen-model latent branching with aggregation: noise-injected latent
trajectories, path agreement as a confidence signal, consensus with
selective abstention. CLB's surviving hypothesis is narrowed: **intra-forward/
intra-layer latent branching followed by a merge operator that computes
something irreducible to candidate selection** (NoisyCoconut's own
aggregation modes are selection-adjacent — majority voting,
confidence-weighted voting — so the decisive discriminator is whether the
merge computes something selection cannot). Honest tier: N1 until the
merge-vs-select ablation shows the operator does work selection cannot.
**Systems:** shared prefix (1−φ)·F + K branches × φ·F + merge ≈
(1+(K−1)φ)·F ≈ 2F for K=4, φ=1/3 [ILLUSTRATIVE]; branches batch in the batch
dim → ≈1× wall-clock given VRAM; memory K·A (binding — pre-register the
VRAM gate: reduce K if OOM rather than silently shrinking φ); cost
falsifier: branches collapse (mean pairwise cos → 1) → parallelism buys
nothing; or merge ≡ argmax → the operator is Best-of-N in disguise.
> **Box 1 — unique support:** branch diversity holds (mean pairwise cos <
> 0.9 pre-registered) AND CLB at ~2F beats Best-of-4 at 4F (more
> capability per FLOP) AND beats the pinned M15-NoisyCoconut comparator at
> matched compute (§G3) AND the merge-vs-select ablation favors the merge
> operator (lower 95% CI > δ_min; merge ≠ argmax/selection — the decisive
> test). Among the reviewed comparators, no identified method performs
> intra-forward-pass latent branching followed by a non-selection merge
> operator — C4 routes between whole strategies, C5 parallelizes instances,
> C2/C3 serialize passes; the merge-vs-select ablation remains the decisive
> discriminator.
>
> **Box 2 — kill:** branches collapse (diversity guard fails) OR merge ≡
> argmax (operator reduces to selection) OR the merge operator's advantage
> vanishes against the pinned M15-NoisyCoconut comparator (§G3) → the operator adds
> nothing over occupied art; withdrawn.
**Evidentiary target:** L2 (new strategy: intra-pass counterfactual
arbitration); L3 only if the merge operator is shown to compute something
no selection can (Stage 3 bar, §J).

### E8 → H5c. Donor-bridge transfer (C-A lineage) — CONDITIONAL candidate

**Mechanism** [HYPOTHESIS]/[HYPOTHESIS]: construct steering directions from
*other items'* unembedding geometry (donor items), restricted to the
output-coupled direction family; zero target-option information at eval
time (strict Law #7 compliance by construction). If donor geometry rescues
held-out items under the entity-similarity-leak control, the mechanism is
"cross-item donor transfer" — not steering, not CAA. **This candidate is
gated:** it becomes a live mechanism program only if the §H bridge battery
leaves an output-side room (i.e., the bridge survives K1 readout-tilt and
K3 Law-#7 audit admits a compliant construction). Until then it is a
pre-registered conditional design, not an active bet.
**Δθ=0** [FACT]/[PROPOSITION]: donor directions are activation/unembedding
constructions; no parameter mutation.
**Novelty** [INFERENCE]/[INTERPRETATION]: logit steering is old; the bid is
*transfer* of output-coupled geometry across items without option
information. Honest tier: N1 until a rescue under strict Law #7 compliance.
> **Box 1 — unique support:** Law-#7-compliant donor bridges rescue
> held-out items with c≈0 at matched compute (lower 95% CI > δ_min) while
> the entity-similarity-leak control does not (pre-registered; LOG-144 review
> scope — the entity-similarity-leak adversarial review per Cluster A). No competitor predicts cross-item donor transfer — C1–C6 are
> per-instance dynamics, not cross-item transfer.
>
> **Box 2 — kill:** donor ΔM ≤ 0 while the self-bridge rescues, OR the
> effect collapses to the similarity control → it is logit steering, not
> transfer; withdrawn.
**Evidentiary target:** L1 (rescue); L2 only if donor transfer beats
per-instance steering at matched compute with conditionality.

## E summary — boxed-standard compliance

| Candidate | H-map | Distinctive computation | Systems signature | Boxes |
|---|---|---|---|---|
| C1 CLLC | H1 | feedback control w/ error bound | 2–6F, 2A | both answered |
| E7 DPRS | H1 | dynamic readout-space search (narrowed; pinned M15-LTPO forced comparator) | pilot ~960F total | both answered |
| C2 ELM | H2 | cross-pass addressable latent RAM | T·F, +0.5MB | both answered |
| C3 TTPS | H3 | synthesized program, compiled exec (interpreter boundary + interpreter-only baseline) | ~8F | both answered |
| C4 ASR | H4 | test-time-learned strategy routing (pinned M15-MetaReasoner forced comparator, dormant until activation; policy scope [INCOMPLETE]) | ~3.2F | **pending — boxes answered but [INCOMPLETE]: not eligible for §F/§G until policy scope is frozen** |
| C5 LCMIC | H5a | formulation-level latent-channel cooperation (same backbone + residual exchange + verifier/arbiter split); pinned M15-LatentMAS forced comparator (§F3 arm (d)) + bandwidth-isolation arm (e) | 6F | both answered |
| C6 CLB | H5b | intra-pass latent branching + non-selection merge operator; pinned M15-NoisyCoconut forced comparator (§G3) | ~2F, K·A | both answered |
| E8 donor-bridge | H5c | cross-item donor transfer | per-item ≤1F | both answered, conditional on §H6 |

[INFERENCE]/[INTERPRETATION]: the seven complete candidates (C1, E7, C2, C3,
C5, C6, plus E8 conditional on §H6) are pairwise mechanism-distinct —
no candidate's Box-1 observation is predicted by any other candidate's
mechanism; that is the discrimination structure §F exploits. C4/ASR's
mechanism-distinctness claim is held pending its policy-scope declaration:
**7 complete candidates + 1 pending candidate (ASR), not eligible for
experimental triage until policy scope is frozen** — stated identically in
§E, the standing-law checklist, and §§G/H. All Box-2 kills are
pre-registrable as written. The six §F1 adaptive ablations (C1, E7, C2, C3,
C5, C6 — C4 excluded until its scope is frozen) are pairwise
distinct (no candidate's ablation is another's mechanism).

---

# F. The three most scientifically important discriminating experiments

*Why these three* [INFERENCE]/[INTERPRETATION]: each separates *families*
of candidates (not candidates from baselines — that is §G's job), each
targets L2+ evidence, each has a pre-registered cell in which a whole
family is culled. Ordered by information value.

## F1 — The strategy-shift assay (adaptive-ablation at matched FLOPs)

**Discriminates:** adaptive families (C1, C4) vs structural families
(C2, C3, C6) vs "extra compute in disguise" (all). **Question:** does the
gain come from a *new strategy* (L2) or from *more FLOPs* (L1)?
**Design** [HYPOTHESIS]/[HYPOTHESIS]: for each eligible candidate (C4/ASR
excluded — [INCOMPLETE], not eligible for §F triage until its policy scope is
frozen; its ablation below is specified prospectively only), run (a) full
mechanism and (b) the *adaptive-ablation*: identical total FLOPs, adaptive
component disabled — C1: inject the final control open-loop (no feedback);
C4: uniform-heavy strategy at matched expected FLOPs (prospective); C2: T passes with the
buffer zeroed (recompute, no carryover); C3: same synthesis FLOPs, direct
emission instead of compiled execution; C5: same roles/rounds, text channel;
C6: K independent full passes + argmax (the Best-of-K it claims to beat);
E7/DPRS: matched-compute random-perturbation control. Pre-registered
statistic: adaptive-ablation Δ = ΔM_full − ΔM_ablated with the exact
two-sided 95% CI; McNemar on the paired difference. Decision per the §G1b
four-cell mapping: demote (Not supported for L2; may survive as L1
engineering) iff the adaptive-ablation difference CI rules out a δ_min
strategy contribution (U_abl < 0.05). CI overlapping δ_min → Inconclusive
(the ablation is underpowered) — candidate held, not demoted.
**Named instantiation — the conditionality probe (Cluster B §3.3/§4.4,
merged):** for EXP068-class loops, (b) is the permutation arm — E's
per-instance measurements replaced by randomly permuted measurements (same
marginals, broken instance-linkage). Pre-registered rule: report
Δ̂ = ΔM_loop − ΔM_permuted-E with the exact two-sided 95% CI; if the CI rules
out a δ_min strategy contribution (U < δ_min), the gain does not depend on
its computed quantities — verdict **Not supported** for L2 (open-loop
selection). If the CI overlaps δ_min → **Inconclusive** — held for a powered
re-test, never culled on this cell. This is the track-3 operational form of
P1: the intervention at stage t+1 must be a load-bearing function of a
quantity measured at stage t within the same episode — otherwise it is bias,
not control.
**Why it discriminates** [INFERENCE]/[INTERPRETATION]: a positive Δ with
FLOPs identical *proves the strategy did the work* — the only L2-licensed
inference available. A zero Δ demotes the candidate to L1 ("more compute
helped") regardless of headline gains — no silent level-crossing.
**Culls:** any candidate whose adaptive-ablation CI rules out a δ_min
strategy contribution is demoted out of the "new mechanism" race (may
survive as L1 engineering only).

## F2 — Cross-family transfer under frozen protocol (generality assay)

**Discriminates:** general architectures (C2, C3, C6 claim generality) from
task-bound steering (C1 as specified, C5 as instantiated). **Question:** is
the candidate a *cognitive architecture* or a *task-specific trick*?
**Design** [HYPOTHESIS]/[HYPOTHESIS]: the identical mechanism protocol —
hyperparameters frozen, only task-specific support data permitted per the
information boundary — applied to three pre-registered task families:
(i) relational 2-hop (home), (ii) algorithmic (multi-step symbolic with
hidden intermediates), (iii) planning (hidden-structure navigation). Each
family carries its own forced baselines and negative controls (§G
conditions, per family). Transfer criterion (pre-registered): beats
compute-matched best fixed baseline on ≥2/3 families (each "beats" read
under the §G1b CI+δ_min rule: lower 95% CI > δ_min) AND passes its Box-1
fingerprint on each winning family.
**Why it discriminates** [INFERENCE]/[INTERPRETATION]: the synthesis asks
for a *successor architecture*, not a benchmark-specific hack. A mechanism
that wins only at home is task-specific steering — valuable (L1) but not the
program's objective. **Culls:** candidates winning <2 families are re-scoped
to "task-specific method," removed from the Stage-3 track (§J).

## F3 — The latent-channel ablation (C5 vs debate/MoA vs M15-LatentMAS vs bandwidth control)

**Discriminates:** C5's channel claim from the forced text-debate baseline,
from the pinned M15-LatentMAS collaboration protocol, and — via the
bandwidth control — from raw channel capacity; secondarily tests
whether *any* multi-instance candidate needs its exotic channel.
**Design** [HYPOTHESIS]/[HYPOTHESIS]: five arms at matched token budget and
matched FLOPs on the NTDP task (§G): (a) C5 full (latent exchange),
(b) C5-text (identical roles/rounds, text-only communication), (c)
debate/MoA forced baseline, (d) M15-LatentMAS (§G3: same roles/rounds/budget,
shared latent working memory), (e) **bandwidth control** — identical
roles/rounds, latent channel compressed to text-equivalent payload: the
exchanged latent tensor is projected/quantized so its total payload in bits
≤ the text channel's token budget in arm (b) (pre-registered compression:
top-k principal components of the exchanged activation, k fixed on the pilot
so payload_bits(e) ≤ payload_bits(b); the compression is frozen before NTDP
data contact). Pre-registered predictions: (a)>(b) with lower 95% CI >
δ_min, AND (b)≈(c) demonstrated by equivalence (95% CI for (b−c) within
±δ_min), AND (a)>(d) with lower 95% CI > δ_min ⇒ the latent channel — in
LCMIC's formulation — is the mechanism; (a)≈(b) with the CI for (a−b) ruling
out δ_min ⇒ C5 reduces to debate (culled, N1); (a)≈(d) with the CI ruling
out δ_min ⇒ C5 reduces to prior art (culled, N1); equivalence not
demonstrable (CI too wide) ⇒ Inconclusive (held, not culled).
**Bandwidth-isolation rule (binding licensing condition, not an appendix
note):** the channel-*representation* causal claim additionally requires the
(a) vs (e) comparison. If L_(a−e) > δ_min (full latent beats
payload-compressed latent by a meaningful margin), the (a)>(b) advantage is
attributable to raw channel capacity, not to the latent mechanism — the
channel-representation claim is **Not supported** and C5's Branch S is
BLOCKED (§G4 condition (v)). If U_(a−e) < δ_min (payload-compressed latent
matches full latent at the practical margin), the raw-capacity account is
ruled out and the representation claim survives this control. If the (a−e)
CI overlaps δ_min ⇒ Inconclusive for the isolation question — C5 is held
(Branch S blocked) pending a powered isolation re-test. Without arm (e),
the latent-vs-text comparison cannot attribute raw channel capacity to the
mechanism. Secondary: critic's latent doubt scalar predicts proposer errors
above chance (AUC>0.55) — the channel carries signal.
**Why it discriminates** [INFERENCE]/[INTERPRETATION]: the cheapest
family-killing experiment in the set (~6F/item × 5 arms, one task family);
it adjudicates the entire "cooperation" direction: if latent bandwidth adds
nothing over text, over the pinned M15-LatentMAS protocol, or over a
capacity-matched control, the H5-cooperation branch of the design space is
closed without further spend.

---

# G. The killer experiment — Novel-Task Discovery Protocol (NTDP), spec sketch

*Pre-registered program-level gate on this synthesis landing (spec §4).
Success = convincing evidence for a new inference-time cognitive mechanism
(L2 required; L3 claimed only if the L3 sub-bars pass).*

## G1. Hypothesis

**H_G** [HYPOTHESIS]/[HYPOTHESIS]: *A frozen model (θ_after=θ_before)
equipped with candidate mechanism C\* discovers and executes a
task-appropriate computational procedure on a novel task family —
constructed after mechanism freeze, with hidden structure no
fixed-inference method exploits — achieving decision accuracy no
FLOPs-matched fixed method achieves, with pre-registered evidence that the
*strategy* (not just the score) is new.*

## G1b. Statistical decision protocol (binding — findings #2/#3)

**Scope:** every primary comparison in §§E/F/G/H that licenses or kills a
mechanism claim. Endpoint is always the decision-change difference ΔM with
the exact McNemar paired test.

**Universal primary-comparison rule.** Every primary comparison reports Δ̂M
with an exact two-sided 95% confidence interval [L, U] for the paired
difference. A p-value alone never licenses a verdict. **Pre-registered
practical margin:** δ_min = 0.05 (5pp), frozen before NTDP data contact and
held constant across all comparisons — margin-shopping after data contact is
forbidden. Justification (treatment-independent): δ_min is a
decision-theoretic practical-relevance margin, not an empirical anchor. On
the NTDP decision-change endpoint, a 5pp absolute decision-accuracy gain is
the smallest effect that would change the program's resource decision —
below 5pp, an inference-time mechanism's win is not worth its forward-pass
cost, its engineering complexity, or its claim on the program's Stage-2
budget; at or above 5pp it is. The value is fixed from task-level practical
relevance and the standing cost structure of inference-time computation
(§G5: every candidate costs ≥2F/item against fixed-method baselines) — no
observed effect size, bridge or otherwise, enters the justification.
(LOG-191 correction: the LOG-187 wording anchored δ_min to the observed
+10pp bridge rescue — that corpus-dependent reasoning is removed and
replaced by this treatment-independent criterion.) With N=80 the two-sided
exact McNemar MDE is ≈7.5pp at c=0, so δ_min lies just below typical
detectability — the Inconclusive cell absorbs that gap instead of converting
underpower into a kill.

**Sensitivity to δ_min (pre-registered reporting; exactly one frozen value).**
The primary margin is 5pp and no verdict in §§E–H is licensed at any other
margin. The table below is reported for transparency, not used for
verdict-shopping: it shows how the retrospective §A3 margin-clearing
adjudications respond to δ_min ∈ {2pp, 5pp, 10pp}.

| Case | 95% CI for ΔM | 2pp | 5pp (frozen) | 10pp |
|---|---|---|---|---|
| EXP065 bridge | [+0.0931, +0.2803] | clears | clears | does not clear |
| EXP066 bridge | [+0.0651, +0.2417] | clears | clears | does not clear |
| EXP070 C7 bridge | [+0.0931, +0.2803] | clears | clears | does not clear |
| EXP077 official bridge | [+0.0338, +0.2015] | clears | directional only | directional only |
| EXP077 smoke bridge | [+0.1444, +0.3544] | clears | clears | clears |
| EXP064 bridge | [−0.0132, +0.1370] | underpowered | underpowered | underpowered |
| A5 pooled static rooms | [−0.0126, +0.0126] | equivalence | equivalence | equivalence |

"clears" = lower CI > δ_min (margin-clearing); "directional only" = CI
excludes 0 but not δ_min; "underpowered" = CI includes 0;
"equivalence" = U < δ_min (equivalence-to-null). Reading: the A5
Not-supported verdict is robust to all three margins; the EXP077-official
directional reading is margin-sensitive (margin-clearing only at 2pp); the
smoke-vs-official magnitude gap (§A3) persists at every margin. The §G1b
prospective rule is evaluated only at the frozen 5pp.

**Verdict mapping (exhaustive).** For a superiority claim "X beats Y by a
meaningful amount": (1) **L > δ_min → Supported** — meaningful improvement
established (significance is necessary but NOT sufficient: p<0.05 with
L ≤ δ_min is not Supported); (2) **U < 0 → Not supported** — genuinely
negative effect with precision; (3) **U < δ_min (with U ≥ 0) → Not
supported** — the CI rules out a meaningful improvement
(equivalence-to-null at the practical margin; TOST logic). This is the only
way a null result becomes "Not supported." (4) **Otherwise (CI overlaps
δ_min, or covers 0 too widely to rule out δ_min) → Inconclusive** — the
comparison is underpowered. The candidate is HELD for a powered re-test,
never culled on this cell.

**Standing ban:** the string "p ≥ 0.05" never appears as evidence against a
candidate anywhere in this synthesis.

**Negative-control rule.** A negative control (B_perp, B_wrong,
shuffled-label, random-perturbation) is "null" iff its 95% CI rules out a
meaningful rescue **in the rescue direction** (U_ctrl < δ_min). If a
control's CI cannot rule out δ_min, the control is **uninformative** — any
Branch-S licensing that depends on it is BLOCKED (verdict Inconclusive),
never licensed. An uninformative control is a property of the experiment,
not evidence for the candidate.

**Hierarchical alpha budget.** Error is controlled hierarchically across four levels: Level 2 controls family-wise error at 0.05 across the 7 complete candidates (Bonferroni; C4/ASR is [INCOMPLETE] and excluded from the NTDP and from this budget until its policy scope is frozen under a fresh pre-registration — see §E/ASR accounting); Level 1's α₁=0.05 governs the single pre-registered program-gate conjunction; Level 3 uses per-check α₃=0.05 for interpretation only. No level borrows from another.
- **Level 1 — Program gate (H3 kill trigger / Survive).** α₁ = 0.05. A single
  family-level conjunction (kill requires ALL candidates to fail; Survive
  requires ≥1 Level-2-licensed Branch S). No multiplicity: it is one
  pre-registered conjunction.
- **Level 2 — Candidate gate (Branch-S licensing, per candidate).**
  α₂ = 0.05/7 = 0.00714 two-sided (Bonferroni over the 7 complete candidates), applied
  to the primary superiority gate (conditions (i), (ii), and (vii) jointly: vs M1 AND vs
  best of M2–M8 AND vs the candidate-specific M15 comparator (or the pre-registered
  structural-comparison path) — the gate passes only if ALL clear δ_min at α₂, using the
  CI rule above; CIs at Level 2 are 1−α₂ = 99.286% exact two-sided
  intervals, the four-cell mapping applying with δ_min unchanged). Secondary Branch-S conditions (controls, fingerprint,
  harm) are reported at Level 3 and cannot license Branch S alone. E8's conditional
  activation does not reclaim budget: if the §H6 battery never activates E8, the 7-way
  division stands (conservative — the budget is pre-registered, not re-divided after data contact).
- **Level 3 — Mechanism fingerprint (Box-1 checks) and control validation.**
  α₃ = 0.05 per check, reported without cross-candidate adjustment. Gates
  *interpretation* of a Level-2 pass; cannot advance a candidate alone.
- **Level 4 — Secondary / exploratory.** Unadjusted p-values, labeled
  exploratory, cannot move any verdict.

**Anti-recycling rule (binding):** candidate selection cannot silently recycle
significance. A candidate failing Level 2 on NTDP data may not be re-tested
on the same data with a new analysis to manufacture a pass. Re-tests require
fresh task-family construction (track-9) and re-consume Level-2 budget. Budget is per-experiment: FWER is controlled within each NTDP run, not across sequential re-tests.
"The winner" is selected only from Level-2-adjusted results.

**Power honesty (pre-registered):** Level-2 Bonferroni is conservative at
N=80. Before the NTDP, the protocol pre-registers N=80, δ_min=0.05,
α₂=0.00714 (two-sided testing), the MDE computed under the pilot-estimated
discordant-pair count (N=20 pilot), and the adaptation rule: if estimated
MDE > 2·δ_min, the candidate is held (Inconclusive) — no N increase is pre-registered in this protocol; any N increase requires a new pre-registration with its own MDE computation —
the Inconclusive cell is the honest container for underpowered comparisons,
never converted to Not supported. McNemar exact is discrete at N=80: modest
decision deltas may be indistinguishable from zero, which the four-cell
mapping already handles.

**Compute-accounting specification (binding on all baselines and candidates —
finding #9).** Every condition reports two numbers: **(a) online inference
FLOPs per item** (everything executed after the test item is observed) and
**(b) one-time/amortized preparation FLOPs** (A-LQR Jacobian computation,
∇-Reasoner backward passes, reward-model training/inference, TTPS
interpreter operations, bandit updates, latent-memory movement, latent-agent
communication, cached-gain construction). "Matched compute" = matched **(a)**
online inference FLOPs per item; **(b)** is reported separately, amortized
over the evaluation set with the amortization denominator stated — never
hidden, never mixed into (a). Track-11's bigger-frozen-model rule: both
frames (training FLOPs amortized vs excluded) reported, neither hidden.

## G2. Benchmark conditions (track-9 duty)

- **Task construction:** the benchmark scientist constructs the task family
  *after* all candidate mechanisms are frozen (constructor independence).
  Hidden compositional / hidden-structure design (ordinary prompting and
  fixed steering insufficient *by construction*). N ≥ 80 items; 40–70%
  headroom on the frozen backbone verified *before* mechanism evaluation
  (Law #9); items without verified headroom excluded and logged.
- **Negative controls (every run):** unintervened backbone; B_perp (random
  orthogonal direction, norm-matched); B_wrong (distractor direction);
  **shuffled-label control** (swap target/foil roles — a true mechanism must
  not "rescue" toward the wrong label; catches readout-bias artifacts);
  random-selection ablation of the candidate's search component. Nullness
  per the §G1b negative-control rule (U_ctrl < δ_min in the rescue
  direction).
- **Forced baselines — all at matched (a) online inference FLOPs per item**
  (FLOPs counted per the two-number rule, not passes assumed): best fixed
  prompt + CoT; static CAA; Best-of-N / self-consistency over outputs; text
  debate / MoA; STARS; DEER; ∇-Reasoner; **next-scale frozen model**
  (e.g. pythia-410m vs 160m) with compute-parity accounting stated in the
  pre-registration (track-11 rule: both accounting frames — training FLOPs
  amortized vs excluded — reported, neither hidden).
- **Evidentiary level:** L2 required for "survive"; L3 additionally requires
  the L3 sub-bars (G4). A bare L1 win is Branch F2, not success — no silent
  crossing.

## G3. Conditions (per candidate C\*)

M1 unintervened · M2 best fixed prompt+CoT · M3 static CAA · M4 Best-of-N
(FLOP-matched) · M5 debate/MoA (FLOP-matched) · M6 STARS · M7 DEER ·
M8 ∇-Reasoner · M9 next-scale frozen model · M10 C\* full · M11 C\*
adaptive-ablation (§F1) · M12–M14 negative controls (B_perp, B_wrong,
shuffled-label) · **M15 candidate-specific forced comparator** (pinned
executable protocols below — per-candidate: M15-LTPO for H1-family C1/DPRS;
M15-MetaReasoner for H4/ASR, activated only when ASR's policy scope is
frozen; M15-LatentMAS for C5/LCMIC, run as §F3's arm (d);
M15-NoisyCoconut for C6/CLB), at matched (a) online inference FLOPs per item
with (b) amortized FLOPs reported separately. **M15 protocol-pinning rule
(binding):** each M15 comparator below is an executable protocol — frozen
model, exact configuration, task construction, and two-number FLOP
accounting are all fixed here, before NTDP data contact. These are the
program's pre-registered operationalizations of the cited mechanisms
(faithful to each paper as verified in Appendix V); where a paper leaves a
hyperparameter free, the program pins a value marked [PINNED-CHOICE] — a
program decision, not a claim about the paper. If any M15 protocol below
cannot be executed as written, it is marked [INCOMPLETE], and per §G4
condition (vii) the associated candidate's Branch S is BLOCKED
(Inconclusive) — incompleteness is never read as clearance.

- **M15-LTPO (for C1, DPRS).** Paper: LTPO (Ye, Liang & Shan,
  arXiv:2510.04182 — parameter-free test-time optimization of latent thought
  vectors on a frozen LLM; online policy gradient guided by an intrinsic
  confidence reward from the frozen LLM's own output distributions; verified
  2026-09-23, Appendix V). Frozen model: the NTDP backbone (the same
  SHA-256-verified checkpoint as every arm; Δθ=0 — no parameter update
  anywhere). Configuration: per instance, T=8 online optimization steps
  [PINNED-CHOICE] over
  the latent thought vector (initialized from the model's own hidden state
  at the intervention layer); each step is a policy-gradient update on the
  latent vector under the intrinsic confidence reward = negative entropy of
  the frozen LLM's output distribution over the answer options
  ([PINNED-CHOICE] operationalization of the paper's
  "intrinsic confidence reward computed from the frozen LLM's own output
  distributions"); step size η=0.1 [PINNED-CHOICE]; no external supervision,
  no reward model, no parameter updates. Task construction: the NTDP task
  (§G2), identical items. FLOP accounting: (a) online = T forward passes +
  T activation-gradient passes per item, counted exactly on the pilot, not
  assumed; (b) amortized = 0 (no preparation). Matched compute: the
  candidate arm's pass budget is set to the measured M15-LTPO (a) cost on
  the pilot — the candidate does not get extra FLOPs because the comparator
  is expensive.
- **M15-MetaReasoner (for C4/ASR; dormant until ASR activates).** Paper:
  Meta-Reasoner (Sui et al., arXiv:2502.19918 — contextual multi-armed
  bandits learn an adaptive policy over reasoning strategies at inference
  time; 9–12% accuracy gains, 28–35% inference-time reduction under the same
  compute budget; verified 2026-09-23, Appendix V). Frozen
  model: the NTDP backbone. Configuration: contextual bandit over the
  strategy menu {backtrack, change decomposition, restart} (the paper's
  menu); context = the compact progress report on the LLM's reasoning state
  (answer-token entropy + self-margin over a 1F draft — the same difficulty
  signals ASR uses, so the comparison isolates the learned policy, not the
  signals); internal reward = agreement + margin (target-free)
  [PINNED-CHOICE]; UCB bandit
  [PINNED-CHOICE]; policy updates use within-episode data only, no
  cross-episode state [PINNED-CHOICE, matching the paper's inference-time
  description]. Task construction: the NTDP task (§G2). FLOP accounting:
  (a) online = 1F draft + routed-strategy passes per item, counted; (b)
  amortized = 0 (bandit table is temporary state, discarded).
- **M15-LatentMAS (for C5/LCMIC; identical to §F3 arm (d)).** Paper:
  LatentMAS (Zou et al., arXiv:2511.20639 — training-free pure latent
  collaboration among LLM agents; autoregressive latent-thought generation
  through last-layer hidden embeddings; shared latent working memory
  transferring internal representations without text mediation; verified
  2026-09-23, Appendix V). Frozen model:
  the NTDP backbone. Configuration: R=3 latent agents in the same fixed
  role framings as C5's arms (a)/(b) (proposer/critic/arbiter [PINNED-CHOICE]
  — the comparison isolates the collaboration protocol, not the roles); D=2
  rounds [PINNED-CHOICE]; R=3 agents [PINNED-CHOICE]; agents communicate by
  appending last-layer hidden embeddings to a
  shared latent working memory (the paper's "shared latent working memory
  preserving and transferring each agent's internal representations and
  latent thoughts"); no re-encoding to text; the arbiter issues the decision
  from the shared memory. Task construction: the NTDP task (§G2). FLOP
  accounting: (a) online = R·D forward passes + memory-move FLOPs, counted;
  (b) amortized = 0.
- **M15-NoisyCoconut (for C6/CLB).** Paper: NoisyCoconut (Jerge & Evans,
  TMLR June 2026, arXiv:2605.08221 — inference-time noise injection into
  latent trajectories generating diverse reasoning paths; path agreement as
  a confidence signal with selective abstention; verified 2026-09-23,
  Appendix V). Frozen model: the NTDP backbone.
  Configuration: K=5 noise-perturbed latent trajectories from the same
  initial hidden state [PINNED-CHOICE] (operationalizing the paper's
  "diverse reasoning paths" from controlled noise injection); Gaussian
  noise σ=0.1 injected into the latent trajectory
  at the branch layer [PINNED-CHOICE]; path diversity measured by mean
  pairwise cosine distance [PINNED-CHOICE operationalization — the abstract
  does not specify a diversity metric]; aggregation = majority vote
  (primary), confidence-weighted voting as the pre-registered secondary
  [PINNED-CHOICE operationalizations of the paper's "agreement among paths"
  consensus — the paper's own mechanism couples agreement to abstention];
  unanimous-agreement abstention is NOT used — the NTDP requires a decision on every item, and abstention would
  change the endpoint (deviation pre-registered here). Task construction:
  the NTDP task (§G2). FLOP accounting: (a) online = K trajectory passes per
  item, counted; (b) amortized = 0. Primary endpoint: ΔM decision changes, exact McNemar with
the §G1b CI+δ_min rule; secondary: per-sample harm ledger
(anti-steerable fraction), Box-1 fingerprint check (per-candidate, §E),
per-item two-number FLOP accounting.

## G4. Decision tree (exhaustive; verdicts per the binding standard)

- **Branch S — KILLER SUCCESS.** ALL hold: (i) ΔM_C\* > 0 vs M1, with lower
  99.286% CI (1−α₂) > δ_min = 0.05; (ii) C\* beats EACH of M2–M8 at matched FLOPs, each
  with lower 99.286% CI (1−α₂) > δ_min = 0.05; (iii) M9 does not beat C\* beyond the
  pre-registered parameter-equivalence margin (else Branch F3); (iv) all
  negative controls null — each negative control's 95% CI rules out a
  δ_min rescue in the rescue direction (U_ctrl < 0.05) — §G1b; a control
  that cannot rule out δ_min blocks Branch S (Inconclusive); (v) Box-1
  fingerprint check passes — for C5/LCMIC this includes the §F3
  bandwidth-isolation arm: the payload-compressed latent arm (e) must match
  full latent (a) at the practical margin (U_(a−e) < δ_min); if L_(a−e) >
  δ_min (full latent beats payload-compressed latent), the channel advantage
  is attributable to raw capacity and Branch S is BLOCKED for C5 (§F3
  licensing rule); (vi) per-sample harm ledger: anti-steerable
  fraction < 15% (else Branch F4); (vii) the candidate-specific M15
  comparator (§G3) is cleared — C\* beats M15 at matched (a) online inference
  FLOPs with lower 99.286% CI (1−α₂) > δ_min = 0.05, OR the pre-registered
  structural-comparison path below is licensed. M15 is not optional: a
  Branch-S license that skips the newer-prior-art comparator is invalid. If
  the M15 protocol is marked [INCOMPLETE] (no pinned executable protocol),
  condition (vii) cannot be evaluated and Branch S is BLOCKED for that
  candidate (verdict Inconclusive) — incompleteness is never read as
  clearance. → **Verdict: Supported** (L2 licensed).
  Significance alone does not license Supported. **L3 additionally** iff:
  (a) M2–M9 all ≈ chance-class performance on a pre-registered *hard
  subset* (items the constructor certifies require structure discovery)
  while C\* succeeds reliably there; (b) the track-12 discovery criterion
  is met (procedure novel to the model per held-out-family
  operationalization, verified by independent oracle). → L3 licensed;
  program advances to §J Stage 2.
- **Branch HOLD — program-level hold (neither kill nor license).** A
  candidate enters HOLD (not F1–F5) when: (a) its primary comparison is
  Inconclusive under the §G1b four-cell mapping (including the pre-registered
  power rule: estimated MDE > 2·δ_min with no N increase pre-registered);
  (b) a licensing control is uninformative (per the §G1b negative-control
  rule) or a required comparator/ablation is [INCOMPLETE]; (c) the candidate
  itself is [INCOMPLETE] (C4/ASR until its policy scope is frozen). HOLD
  neither kills nor licenses: the candidate's mechanism claim stays exactly
  where the evidence left it (normally Inconclusive), with no Stage-2
  advancement and no engineering demotion. Release from HOLD requires a
  fresh pre-registration — fresh task-family construction per the
  anti-recycling rule, re-consumed Level-2 budget, the blocking defect
  explicitly repaired; a held candidate never re-enters on the same data or
  by re-analysis. A candidate that exhausts its pre-registered re-test path
  without clearing the block exits HOLD to the applicable F-branch verdict
  (F1/F2/F4 as the evidence dictates) — never to Branch S by attrition.
  HOLD is not a rescue path: §H3's kill trigger still fires over candidates
  with no active pre-registered re-test path (see §H3 condition 1). The
  structural-comparison path (below) never places a candidate in HOLD to
  evade condition (vii) — it is an alternative licensing route with its own
  trigger conditions, not a deferral.
- **Structural-comparison rule (pre-registered; not an escape hatch).**
  Direct superiority over M15 is scientifically inapplicable — and the
  structural path may be used instead of condition (vii)'s superiority test
  — ONLY IF all three trigger conditions hold: (a) the structural
  distinction is pre-registered as an observable mechanism property
  independent of the measured gain — stated as a property of the candidate's
  construction (e.g., CLLC's observer/controller/plant separation with a
  derived tracking-error bound; CLB's merge operator computing arbitration
  irreducible to selection) that can be verified without reference to ΔM,
  with a pre-registered operational check for its presence; "different
  architecture" as a redescription of the mechanism, without an independent
  operational check, never qualifies; (b) the distinction is experimentally
  established on the NTDP (the operational check passes at its
  pre-registered bar); (c) M15 is still run as a control arm on the same
  NTDP and its outcome reported at Level 3 (interpretation), with a
  pre-registered prediction of M15's failure mode under the structural
  claim. The structural path licenses Branch S only if (a)–(c) all hold AND
  conditions (i)–(vi) hold AND M15 does not beat C\* at the Level-2 standard
  — if M15 clears δ_min over C\* at α₂, the structural claim is Not
  supported (the structural difference did not do work the prior method
  cannot do). The structural path is rare by design and its invocation is
  logged as a protocol event.
- **Branch F1 — beaten by fixed methods.** For the best forced baseline, the
  95% CI for (ΔM_C\* − ΔM_baseline) at matched FLOPs rules out a δ_min
  advantage (U < 0.05) → **Not supported** (beaten-or-equivalent
  demonstrated). If the CI overlaps δ_min → **Inconclusive** (underpowered
  comparison) — the candidate is held for a powered re-test, never culled
  on this cell. → Feeds experiment H.
- **Branch F2 — gain without strategy.** (i)–(iv) hold but (v) fingerprint
  fails. → **Underdetermined** (L1 gain, mechanism unproven). C\* continues
  ONLY as L1 engineering; the "new mechanism" claim is not licensed.
- **Branch F3 — parameter substitution.** M9 (bigger frozen model) beats C\*
  at matched inference FLOPs beyond the margin. → **Inconclusive** for
  novelty: the capability exists in weights; C\* is not licensed as *new
  computation*. (Track-11 rule: not a failure of C\* as engineering — a
  failure of the novelty claim.)
- **Branch F4 — harm.** Anti-steerable fraction ≥ 15% with net ΔM>0. →
  **Not supported** as a cognitive mechanism ("wins on average while
  harming a sixth of instances" is inadmissible); returns for re-design,
  not advancement.
- **Branch F5 — Contaminated.** (i)–(iii), (v), (vi) hold but (iv) fails —
  a negative control also fires (readout-bias artifact signature: the
  rescue is real but a control that should be null is not). →
  **Not supported** as a mechanism; the artifact routes to the §H6 battery
  for adjudication rather than being scored as a mechanism failure.
- **Degenerate cells.** Zero variance → statistic undefined →
  **Inconclusive**, task re-constructed. b=c=0 throughout ⇒ p=1.0 exactly
  (vacuous significance cell impossible).

## G5. Forward-pass budget (pre-registered cap)

Per item per candidate: F_C\* ≤ 8F (hard cap; candidates declaring above
8F/item are inadmissible for G). Total per candidate: N=80 × 15 conditions
× ≤8F ≈ ≤ 9,600F [ILLUSTRATIVE]; at ~0.5 s/pass (410m-class, T4) ≈ **3–5 h
T4 per candidate** — schedulable across Kaggle sessions on the free tier.
Pilot: 20 items × full conditions first; full run only if no degenerate cell
fires on the pilot. (FLOP counts per the §G1b two-number rule.)

---

# H. The failure experiment — explicit license to kill the mechanism family

*Pre-registered program-level gate with **explicit license to kill** (spec
§4; mentor P3). H runs the *family-level* adjudication: G tests candidates;
H tests whether the family deserves to exist.*

## H1. Hypothesis (the family claim)

**H_H** [HYPOTHESIS]/[HYPOTHESIS]: *There exists a temporary-computation
mechanism (any of C1, E7, C2, C3, C5, C6, E8-conditional, or a pre-registered
composition of at most two; C4/ASR is [INCOMPLETE] and excluded from H until
its policy scope is frozen) that changes the computational strategy (L2) or
creates qualitatively new capability (L3) on the NTDP at matched inference
FLOPs vs the forced-baseline set.*

## H2. Design

All surviving candidates (post-§F culling) run the full NTDP (§G1b–G3) with
one addition: the **family-ablation arm** — the *best* fixed method per item
(post-hoc oracle over M2–M8, labels used only for this ceiling measurement,
cf. EXP070 precedent): if no candidate beats even the oracle-fixed ceiling,
the family cannot claim headroom exists. Benchmark conditions, negative
controls, forced baselines, harm ledgers: identical to §G2. All verdicts per
the §G1b decision protocol.

## H3. The kill trigger — READ THIS AS LICENSE

**KILL TRIGGER (pre-registered):** the mechanism family is **Refuted** as a
cognitive-augmentation program iff ALL of the following hold on the NTDP:
1. Every eligible candidate lands in G-Branch F1, F2, F3, or F4 (no Branch S anywhere);
   candidates in HOLD with an active pre-registered re-test path suspend the family
   verdict to Inconclusive (family held, not killed, not surviving) until the re-test
   resolves — HOLD with no remaining re-test path does not block this condition;
2. No candidate passes its Box-1 fingerprint check (no L2 evidence for any
   mechanism — gains, if any, are L1-only);
3. The per-sample harm ledgers show no rescuable subset (gains
   unconcentrated — there is no "it works on a discoverable subset"
   retreat);
4. The oracle-fixed ceiling (H2 addition) is not beaten by any candidate
   (no headroom for *any* fixed-computation selector to exploit).
**THE LICENSE:** if the kill trigger fires, the program **closes the
temporary-computation mechanism arm**: no new C-variants, no rescues by
re-tuning, no "one more architecture." The A–J "new mechanism" claim is
withdrawn in writing. Remaining resources redirect to (a) publishing the
negative result — *why* temporary computation cannot add capability under
Δθ=0 is itself a boundary claim of publishable value (the program's most
defensible asset class, per the kill culture of G1/EXP079); (b)
mechanistic understanding of the boundary. **This license is pre-registered
and executes without re-approval.** Theory preservation — keeping the
family alive for elegance, ambition, or sunk cost — is the named forbidden
move, and this paragraph is its antidote.

## H4. Survive / demote branches (exhaustive)

- **Survive:** any candidate hits G-Branch S (L2+) → family survives
  **narrowed** to the surviving mechanism(s); all others culled. Candidates in
  HOLD are neither culled nor advanced — they retain their hold status and
  pre-registered re-test path. Program advances to §J Stage 2 with the survivor(s) only.
- **Demote (partial):** ≥1 candidate shows replicable L1 gains (Branch F2,
  fingerprint failed) with harm < 15% → the family survives ONLY as an
  **inference-improvement engineering program**, explicitly demoted from
  the superintelligence objective. The L2/L3 claim is withdrawn; no Stage
  2/3. [INFERENCE]/[INTERPRETATION]: this is the "useful but not new" cell
  — honest, publishable, and not the program's organizing question.
- **Substitution (all-F3):** every candidate lands in G-Branch F3 (M9 beats
  each at matched inference FLOPs beyond the margin) → the family's
  *novelty* claim has failed everywhere, even where engineering value
  survives. The family is **Not supported** as *new computation*; surviving
  L1 value, if any, is handled under the demote-to-engineering logic
  (track-11: "not a failure of C* as engineering — a failure of the novelty
  claim"). No Stage 2/3.
- **Degenerate:** NTDP itself fails construction (no headroom achievable, or
  all forced baselines ≈ chance AND all candidates ≈ chance — the task is
  broken, not the family) → **Inconclusive**; track 9 reconstructs; H
  re-runs once. A second consecutive degenerate construction retires H in
  favor of a redesigned gate (logged, Law #8 — never silently dropped).

## H5. Forward-pass budget

Shared NTDP infrastructure with G (constructor, headroom verification,
baselines M1–M9 run once, reused): marginal cost per additional candidate
≈ N=80 × 4 arms (M10/M11/M12–14 subset) × ≤8F ≈ 2,500F ≈ **~1 h T4**
[ILLUSTRATIVE]. The family-level verdict is therefore *cheaper* than any
single candidate's G run — killing is economical, which is the point.

## H6. The bridge-evidence battery (twin challenges + diagnostic)

*The H1–H5 family gate above adjudicates candidates. This battery
adjudicates the program's positive-evidence base — the bridge rescues that
§C reads as the "output-side room." It is an evidence-gate, not the family
gate; its outcomes feed H3 (a confirmed readout-bias verdict removes the
premise of the conditional E8 candidate and forces C1's setpoint
re-specification). Order is binding on *interpretation* — no K2/K3 verdict
is drawn before K1 rules — but parallel *preparation* (K2's pilot run,
K3's Law-#7-compliant constructions) is explicitly permitted and encouraged
so benchwork does not idle; each step is pre-registrable. All verdicts per
the §G1b decision protocol.*

**K1 — Readout-tilt falsification (Cluster C CHALLENGE). FIRST.**
[INFERENCE]/[INTERPRETATION]: an unembedding-space direction injected at
the answer position is mathematically adjacent to adding a constant logit
bias toward the target token. Tests ($0, archived EXP065/066/077
artifacts): (a) cos(bridge direction, unembedding row of t_target) — if cos ≥ 0.9 (pre-registered),
it is a target boost, full stop; (b) correct-item flip analysis —
**diagnostic readout** (not a standalone kill): symmetric correct→wrong
flips (bias) vs only wrong→correct (rescue); pre-registered reading —
count correct→wrong flips f and wrong→correct rescues r: f ≥ r/2
strengthens a tilt verdict, f ≈ 0 with r > 0 (lower 95% CI > δ_min)
weakens it, reported as [OBSERVATION] feeding the K1 verdict; (c)
**label-shuffle test** — re-score archived items with target/foil roles
swapped: a true relational mechanism must now *hurt*; a readout tilt still
"helps" toward the original target token. **Kill criterion:** (a) cos ≥ 0.9 OR
(c) shows rescue-persistence under label shuffling (read under the §G1b
CI+δ_min rule) → the bridge is readout bias; the "output-side mechanism"
reading is withdrawn; the bridge's positive-control status is revoked to
*rescue* control, not *mechanism* control.
**Why the mentor gets this falsification first:** (i) it is $0 —
re-analysis of archived artifacts, no new compute, fastest to a verdict;
(ii) it is logically prior — a readout-bias verdict dissolves the Law #7
question (there is no autonomous mechanism left to audit for label
compliance); only a *survival* verdict licenses the K3 audit to bite;
(iii) it is designed to lose cleanly — if (a)–(c) all favor a true
mechanism, the output-side lead stands strengthened, which is also
information.

**K2 — Bypass-vs-routing discriminator (Cluster A IDEA). SECOND.**
[CONJECTURE]/[OPEN] in the corpus: is the bridge's rescue *readout bypass*
(direct logit tilting through the residual→unembedding path, no attention
mediation) or *computational re-routing* (the bridge changes what downstream
attention heads compute)? The corpus asserts bypass (forensic audit Finding
4) but never discriminated it. **Cheapest falsifying experiment**
(60 items × 3 conditions ≈ 180 forward passes — minutes on a T4): inject
the archived b_mean at (a) final-token position only, (b) premise-entity
positions only (current standard), (c) all positions, on the signed
EXP077/078 benchmark (decision-change endpoints, McNemar, §G1b CI+δ_min
rule). **Kill criterion:** if (a) final-token-only rescues ≥ (b)
premise-position (ΔM_a ≥ ΔM_b, and the exact two-sided 95% CI for (ΔM_b − ΔM_a) rules out a δ_min advantage of (b) over (a) (U < 0.05)), the bypass account is
**Supported** and the routing account **Not supported** — the bridge does
not engage attention computation; the "output-side mechanism" is logit
steering, period. If (a) fails while (b) rescues (the CI for
(ΔM_b − ΔM_a) clears δ_min, L > 0.05), bypass is **Not supported** — the
bridge demonstrably routes through upstream computation. Ordered after K1
because it needs a pilot run while K1 needs none; a K1 tilt-verdict + K2
bypass-verdict jointly close the output-side room as a mechanism program.

**K3 — Law #7 compliance audit of the bridge (Cluster A CHALLENGE). THIRD.**
[FACT]/[OBSERVATION]: every bridge in the corpus is constructed as
normalize(E[target] − E[foil]) — from candidate option tokens. **Falsifier
(pre-registerable):** construct the bridge under strict Law #7 compliance —
from premise-entity tokens only, or from donor items (C-A) with the
entity-similarity-leak control — and test rescue on the signed benchmark.
**Kill criterion:** if the Law-#7-compliant bridge yields ΔM = 0 while the
option-informed bridge rescues, then the "output-side room" as an
*autonomous mechanism* hypothesis is **Not supported**: the rescues are a
label-assisted readout-steering artifact, and the output-side program is
re-scoped to "label-assisted steering" (N0 vs CAA with a known-answer
direction — the §B attack applies to it too). Ordered third because it
bites only on a mechanism that survives K1 — auditing the label compliance
of a confirmed readout tilt is wasted motion.

## H7. UNRESOLVED — CEO decision required (not decided here)

[OPEN]/[OPEN]: **if K1 confirms readout bias, does the bridge's
positive-control status get demoted across all signed protocols that used
it (EXP065/066/070/077)?** Cluster C flagged this as "flagged, not decided
here"; this synthesis does not decide it silently. The decision (revoke vs
retain-with-relabeling, and whether signed-protocol corrections require
user sign-off per the repo's correction law) is reserved for the CEO and
must be logged explicitly when taken. Until decided, the synthesis cites
the bridge as "Supported (L1, mechanism [CONJECTURE], readout-bias audit
pending)."

---

# I. Operational definition of "superintelligent augmentation"

*Cluster A's track-5 input is authoritative (reconciliation appendix R(a)).
"Superintelligent" is a measurement protocol below, not an adjective.*

**Definition** [INFERENCE]/[PROPOSITION] (track 5): a frozen model M
(Δθ=0, SHA-256-verified pre/post) is *superintelligently augmented* by an
inference-time procedure P iff all of the following hold on a
pre-registered task family T:

1. **Capability delta at matched compute.** M+P exceeds every forced
   baseline at ≤ matched inference FLOPs — unaugmented M, debate/MoA,
   STARS, DEER, ∇-Reasoner, a bigger frozen model — on decision-change
   endpoints with pre-registered statistics.
2. **Strategy change (L2).** P's internal compute allocation depends on the
   input: per-item compute spend correlates with item difficulty/uncertainty
   at fixed total budget; ablating the adaptivity (fixed-budget P) destroys
   the gain.
3. **New capability (L3).** There exists a task family T_new
   (hidden-structure / novel-task) on which M and all forced baselines
   perform at chance while M+P performs significantly above chance,
   **and** the capability transfers to a second task family not used in P's
   development (Stage-2 gate).
4. **Mechanism ablation.** Removing P's claimed novel component (verifier,
   controller, workspace) at matched compute destroys the capability. No
   ablation, no mechanism claim.
5. **No label leakage.** P's construction uses no test labels, target
   answers, or candidate-option tokens (Law #7); verified by construction
   audit.

**Kill criterion** [INFERENCE]/[PROPOSITION]: if M+P's only demonstrations
are score gains on benchmarks where a forced baseline at matched compute
matches or exceeds it, "superintelligent augmentation" is **Refuted** for
P; the claim downgrades to L1 ("can improve inference") or to a
measurement.

**Grades (bound to the three evidentiary levels):** (a) *inference
improvement* (L1 — score gain at matched compute); (b) *strategy change*
(L2 — adaptive compute allocation verified); (c) *new capability* (L3 —
chance-to-above-chance on hidden-structure tasks with transfer). The term
"superintelligent augmentation" is reserved for (c); (a) and (b) are named
as what they are.

[INFERENCE]/[INTERPRETATION]: this definition rules out the entire current
corpus — the bridge rescues are L1 at best (option-informed construction
fails condition 5 for autonomous claims; forced baselines never run fails
condition 1 as a claim). That is the definition working as intended: it is
a bar, not a celebration.

**Operationalization notes (reconciled with Cluster C's provisional
definition — differences flagged in R(a)):** condition 1–2 are
operationalized by G-Branch S (L2+ on the NTDP: beats every forced
baseline at matched FLOPs + Box-1 fingerprint); condition 3's transfer
clause is operationalized by §F2 (≥2/3 families — retained as the stricter
quantitative bar); condition 3's new-capability clause by the G4 L3
sub-bars (chance-bar + track-12 discovery bar); condition 4 by the §F1
adaptive-ablation + per-candidate ablation arms; condition 5 by the H6-K3
audit and the track-9 constructor-independence rule.

---

# J. Three-stage roadmap

*Gated by the §I definition (authoritative) and the track-12 discovery
criterion (Cluster B §5). No hype terms appear in any gate criterion.*

## Stage 1 — Prove/disprove the mechanism

**Work:** §F culling (F1–F3) → G (NTDP per surviving candidate) → H (family
adjudication). **Pre-registered gate:** advance iff ≥1 G-Branch S (L2+);
close iff H kill trigger (§H3); demote iff H-Demote branch; hold (family
verdict Inconclusive, not killed, not advanced) iff ≥1 candidate sits in
§G4 Branch HOLD with an active pre-registered re-test path. **No candidate
reaches Stage 2 on L1 gains.** [INFERENCE]/[INTERPRETATION]: Stage 1 is the
falsification funnel; its output is at most two surviving mechanisms, more
likely zero. **Recommended cull order if compute binds:** F3 first (cheapest
family-kill), then F1 (demotes L1-disguised candidates), then G pilots.

## Stage 2 — Cross-task / general transfer

**Work:** survivor(s) run §F2 across ≥3 pre-registered task families
(relational, algorithmic, planning + one track-9-constructed
hidden-structure family), each with own forced baselines, negative
controls, harm ledgers. **Pre-registered gate:** transfer bar = beats
compute-matched best fixed baseline on ≥2/3 families AND Box-1 fingerprint
passes on each winning family AND harm < 15% throughout. **Fail:**
mechanism re-scoped to "task-specific method" (honest, publishable);
program does not advance it. **Pass:** Stage 3.

## Stage 3 — Qualitatively new capabilities

**Work:** the L3 sub-bars, pre-registered per mechanism: (a) **chance-bar:**
task class where backbone + all fixed methods ≈ chance (pre-registered
chance baseline + margin) but the mechanism succeeds reliably (replicated,
N≥80); (b) **discovery bar** (track 12): the mechanism outputs a
procedure/algorithm/hypothesis operationally novel to the model
(held-out-family test) and verified by an independent oracle; (c) **scaling
bar** (track 11): capability-vs-inference-FLOPs curve for the mechanism vs
parameter scaling, with the compute-parity falsifier named — the mechanism
must show a regime where inference-FLOPs beat parameter-FLOPs or the "new
capability" claim is not licensed as *efficient*. **Gate:** all three
sub-bars, or the L3 claim is not made.
**Discovery criterion (track 12, binding on Stage 3)** —
[INFERENCE]/[PROPOSITION]: no "discovery" claim without all of D1–D4
pre-registered and satisfied. **D1 — Novelty-to-model (behavioral):** the
artifact is not in the frozen model's elicitable repertoire without P
(operational test: *elicitation control* — the same frozen model at matched
compute, given the task directly, fails to produce A at comparable
quality/rate). **D2 — Independent oracle:** A's correctness verified by a
process causally independent of the model's own judgment (formal proof
checker, held-out tests, physical experiment, or an independently-validated
different model family); the model's self-evaluation can never be the
oracle. **D3 — Outside the training manifold:** at least one pre-registered
proxy — temporal novelty, combinatorial novelty, or canary ablation.
**D4 — Capability bite:** A enables decisions/actions the model could not
otherwise take — measured as new task success under D1's elicitation
control, not score gains on solved tasks. **Credit assignment:** discovery
credit accrues to the *model* only to the extent P is task-general; report
P's scaffolding-specificity alongside D1–D4. Current status: no SCBI result
satisfies even D1 — Stage 3 is *ungated aspiration*, not a plan, until an
L2 mechanism exists.
[OPEN]/[OPEN]: Stage 3 may require compute beyond free-tier VRAM for larger
backbones — flagged honestly; Stage 1–2 fit the free tier per §G5/H5.

---

# Appendix R. Reconciliation decisions (a)–(h)

*Every decision below records what was kept, cut, or merged, and why. The
boxed standard was applied to every H1–H5 candidate; any candidate lacking
either box would have been rejected — none was. R(a)–R(g) are the LOG-158
assembly record, carried forward verbatim; R(h) records the LOG-187
revision.*

## R(a). §I — one operational definition

**Kept as authoritative:** Cluster A's track-5 five-condition definition
(capability delta at matched compute; strategy change; new capability with
second-family transfer; mechanism ablation; no label leakage), its kill
criterion, and its L1/L2/L3 grades. **Reconciled against:** Cluster C's
provisional §J definition. **Differences found and flagged:** (1) the
provisional definition omits mechanism ablation (track-5 condition 4) —
adopted, now required; (2) it omits no-label-leakage (track-5 condition 5) —
adopted, now required, and it is the condition that currently rules out the
entire corpus; (3) its "≥3 task families" is a stricter quantitative form
of track-5's second-family transfer clause — kept as the operational bar
(§F2); (4) its "passes G-Branch S (L2+)" operationalizes track-5 conditions
1–2 on the NTDP — kept as operationalization, not as replacement;
(5) its L3 sub-bars operationalize condition 3's new-capability clause —
kept. **Cut:** nothing from track-5; the provisional definition's
standalone status (it was labeled [SPECULATION]/[CONJECTURE] pending
reconciliation). **Result:** one definition (§I), with the provisional's
operational elements folded in as measurement procedures under track-5's
conditions.

## R(b). H5 — two candidates kept, third conditional

**Cluster C offered C5 (LCMIC) and C6 (CLB) as H5 candidates.** Each was
tested against the boxed standard independently: C5 Box 1 (latent > text at
matched budget AND text-only ≈ debate/MoA AND critic doubt predicts errors)
and Box 2 (latent ≈ text → culled as debate) are both answered and
pre-registrable. C6 Box 1 (branch diversity + merge-vs-select favors merge
+ ~2F beats Best-of-4 at 4F) and Box 2 (collapse or merge ≡ argmax →
withdrawn) are both answered and pre-registrable. **Both pass; both kept**
as H5a (cooperation) and H5b (counterfactual branching) — they are
mechanism-distinct (inter-instance latent exchange vs intra-pass
counterfactual arbitration), and no candidate's Box-1 observation is
predicted by the other's mechanism. **Cut:** neither. **Added from Cluster
A's E-input:** E2 (donor-bridge transfer) as H5c — **conditional** on the
§H bridge battery leaving an output-side room; its boxes were expanded from
Cluster A's compressed pair. **Merged (not dropped):** Cluster A's E3
(measurement-pruned head-targeted search) — folded as a pruning *operator*
applicable to search candidates (restated around readout-coupled
OV/unembedding heads per G1's honest caveat), not a standalone H candidate,
because its box pair is a design-objective claim ("maximize QK-projection
energy" was already refuted as sufficient by G1) rather than a mechanism;
E4 (verifier/controller separation) — absorbed into C1's
observer/controller/plant hierarchy and DPRS's E component. **Added from
Cluster B's IDEA:** DPRS as a second H1 instantiation (E7) — Cluster C's
six contained no readout-space dynamic loop, and the evidence says causality
lives output-side; it does not duplicate any C-candidate (C1 controls hidden
activations; DPRS searches readout perturbations).

## R(c). The twin bridge challenges — ordering and the open CEO decision

**Both represented in §H6's kill battery.** K1 = Cluster C's readout-tilt
falsification (cos vs unembedding row of t_target; correct-item flip
analysis; label-shuffle test). K3 = Cluster A's Law #7 compliance audit
(premise-entity-token or donor-item bridge; kill criterion: compliant ΔM=0
while option-informed rescues → autonomous output-side hypothesis Not
supported). K2 = Cluster A's bypass-vs-routing IDEA sits between them as
the mechanism diagnostic. **The mentor gets K1 first because:** (i) it is
$0 — pure re-analysis of archived artifacts, no new compute, fastest
verdict; (ii) it is logically prior — a confirmed readout-bias verdict
dissolves the Law #7 question (no autonomous mechanism remains to audit);
only a survival verdict licenses K3 to bite; (iii) it is designed to lose
cleanly — a negative result strengthens the output-side program. K2 is
ordered second (needs a ~180-pass pilot; converts a K1 tilt-verdict into a
bypass-vs-routing mechanism verdict); K3 third (bites only on a surviving
output-side mechanism). **Explicitly unresolved (§H7):** whether a confirmed
readout-bias verdict demotes the bridge's positive-control status across
all signed protocols (EXP065/066/070/077) — reserved for the CEO, to be
logged explicitly when decided; the synthesis does not assume an answer.

## R(d). Crossing experiment — one experiment set, merged with attribution

**Cluster B's "EXP068 + conditionality probe" (§3.3, with track-3's §4.4
conditional-routing criterion) and Cluster C's §F/§G designs genuinely
overlap:** the conditionality probe (permuted-E arm) is the EXP068-geometry-
loop instantiation of §F1's adaptive-ablation (identical FLOPs, adaptive
component disabled). **Merged, not duplicated:** §F1 is the general
family-level discriminating experiment (per-candidate ablations C1–C6/E7);
the conditionality probe is preserved as its **named EXP068 instantiation**,
with attribution to Cluster B §3.3 and track-3 §4.4 (the P1
operationalization: gain must depend on within-episode computed quantities).
What F1 adds beyond B's probe: coverage of all candidates, not just the
geometry loop — that is the genuine difference, stated in §F1. Cluster B's
D3-adjacent §3.3 decision rule is preserved inside F1 and §D3, with the
decision rule updated to the binding CI+δ_min formulation per the stats
revision (see R(h)).

## R(e). EXP023 lineage — discharged per LOG-186

The LOG-158-era selection-bias challenge is closed. Per the LOG-186 lineage
audit: the "configuration grid" never existed — L∈{2,4,6,8,10} was EXP013's
configuration and the 45-condition factorial was EXP030's. EXP023 was
seed-123 dev selection → one pinned config (G4, E_CF, O5, L=8, r=2, α=0.25)
→ seed-84 confirmatory. No Bonferroni precommit was made. The reported
result (Seed 84 +7.0pp, N=100, CI [+0.0300,+0.1200]; Seed 168 +6.0pp;
pooled b=14, c=1, p=0.000488) is reported with the pre-specification caveat:
winner's-curse optimism from the dev-selection step is unquantified; the
revised verdict is **Supported (L1, selection-optimism caveat)** (§A10); no
L2 license flows from this result; any L1 claim built on it requires fresh
confirmatory replication with the config frozen before data contact.

## R(f). The "adjacent possible already shipped" line — not softened

**§B5 carries Cluster B's surprise at full strength:** ∇-Reasoner (ICLR
2026) occupies the output-side dynamic room with working results (80.4%
MATH-500, GRPO-matching at 10–40% fewer calls than Best-of-N) — the burden
is now on SCBI to explain why gradient-free self-consistency would beat
gradient-based optimization with a reward model at matched compute; and
Activation-LQR (ICML 2026) occupies H1's slot with formal tracking-error
bounds — SCBI's H1 candidacy is "closed-loop control, but open-loop-
evaluated and unbounded," strictly weaker than the art until proven
otherwise. DEER is stated as L2 evidence already demonstrated by the field
without any representation construction. Steering Vector Fields (Feb 2026)
is cited as **UNVERIFIED** (Cluster B could not retrieve the primary
source) — the literature program must verify before the synthesis is cited
on it. Nothing here is softened into "SCBI was early" or "the field
validates us." *(LOG-187 note: the LOG-158-era venue labels in this
paragraph are superseded by the LOG-185 corrections recorded in R(h) —
Activation-LQR's ICML 2026 listing is confirmed and its actual title is used
in §§B5/D1; ∇-Reasoner's ICLR 2026 venue and 80.4% figure are confirmed.)*

## R(g). Additional merge/cut ledger (completeness)

- **Cluster A §B attack claims** (CAA operator equivalence, etc.) were
  [INFERENCE]/[INTERPRETATION] pending Cluster B's audit — the audit
  verified them; §B cites them as verified. No unverified equivalence claim
  is cited as fact.
- **Cluster A A2 verdict distinction** (dynamic alignment Inconclusive, not
  Not supported) preserved in §A2 — collapsing it would mislicense EXP067.
- **Cluster B's seven non-softenable constraints** enforced: (1) Wilcoxon
  margins inadmissible (§A9); (2) bridges are label-informed existence
  proofs (§A3); (3) EXP077 +10pp not margin-clearing, magnitudes
  environment-sensitive (§A3); (4) EXP057 is a benchmark-validity finding
  (§A8); (5) G1 kill scoped to the QK-subspace claim, not the bridges or I1
  (§A4); (6) N1 across the static family, tested mechanism N0 (§B1);
  (7) forced baselines explicitly include ∇-Reasoner and Activation-LQR at
  matched compute (standing law, §§G2/G3).
- **Cluster B's D1–D4 discovery criterion** constrains §J Stage 3 verbatim;
  Stage 3 is stated as ungated aspiration until an L2 mechanism exists.
- **Cluster A's track-5 note** that the definition rules out the current
  corpus is preserved in §I (the definition working as a bar, not a
  celebration).
- **Cut as standalone items:** Cluster C's provisional §J operational
  definition (folded into §I per R(a)); Cluster A's E1/E5/E6 (superseded by
  the fully-developed C1/C2/C4 — the E-input was scaffolding per Cluster A's
  own handoff note); Cluster B's IDEA DPRS is kept, not cut (E7). Nothing
  with a live falsifier was dropped.

## R(h). LOG-187 revision record — per-finding changes (mentor-ordered)

**Finding #1 (literature map).** §D1 rebuilt per LOG-185 (nothing cited from
the mentor review's wording): **LTPO** (Ye, Liang & Shan, arXiv:2510.04182 —
arXiv preprint, no venue) placed in Family C as "test-time latent
optimization (frozen)"; **Meta-Reasoner** (Sui et al., arXiv:2502.19918,
Findings of ACL 2026) in Family C as "test-time strategy routing";
**LatentMAS** (Zou et al., arXiv:2511.20639, ICML 2026 spotlight) as new
Family I "training-free latent multi-agent collaboration"; **NoisyCoconut**
(Jerge & Evans, arXiv:2605.08221) in Family C as "training-free latent
branching + consensus" — cited strictly as an **arXiv preprint under review
at TMLR**, never as a published TMLR paper (LOG-185 correction applied;
overrides the edit spec's "TMLR June 2026" phrasing wherever it appeared);
**RISER** (Ye et al., Findings of ACL 2026) as adjacent excluded art with
the boundary nuance stated precisely (trained *external router* over a
frozen backbone — excluded because any trained component violates Law #6,
not because the backbone is fine-tuned); **∇-Reasoner** venue confirmed
ICLR 2026 with the 80.4% MATH-500 figure confirmed; **Activation-LQR**
confirmed as ICML 2026 proceedings listing (entry 3288) and cited under its
actual title "Local Linearity of LLMs Enables Activation Steering via
Model-Based Linear Optimal Control". Steering Vector Fields: not placed —
unverified. The "only unoccupied sub-slot" sentence was narrowed per E1.
Forced comparators added: LTPO-style (H1-family, §G3 M15), Meta-Reasoner-style
(H4, §G3 M15 + §C4 Box 1), LatentMAS-style collaboration (H5a, §F3 fourth
arm + §C5 Box 1), NoisyCoconut-style branching/consensus (H5b, §G3 M15 +
§C6 Boxes).
**Finding #2 (statistics).** Binding decision framework installed: §G1b
(universal CI+δ_min rule, four-cell verdict mapping, negative-control rule,
standing ban on "p ≥ 0.05" as evidence against a candidate); Box-1 gates
read as "p<0.05 AND lower CI > δ_min"; per-site replacements applied exactly
(G4 Branch S (i)/(ii)/(iv)/F1, F1 cull rule, DPRS Box 2, C4 Box 2, C5 Box 2,
F3 predictions, D3 conditionality rule). Retrospective §A sites restated in
CI language (A3 per-demonstration CIs with margin-clearing adjudication;
A5 pooled equivalence-to-null bound; A10 per LOG-186).
**Finding #3 (multiplicity).** Four-level hierarchical alpha budget stated in
§G1b (α₁=0.05 program gate; α₂=0.00625 Bonferroni over 8 candidates at the
Branch-S gate; α₃=0.05 per fingerprint/control check; Level 4 exploratory),
plus the anti-recycling rule and pre-registered power honesty.
**Finding #4 (bridge evidence).** A1's cosine inference downgraded
(anisotropy caveat wins; licensed dissociation narrowed); A3/A7/C1 reframed
as readout-path steerability (one confounded construction, not converging
confirmations); K1/K3 load-bearing weight raised explicitly in §C1.
**Findings #5/#6 (H5a/H5b).** The false "no competitor uses inter-instance
latent exchange" sentence deleted (verified: no occurrence or paraphrase
survives); LCMIC rewritten as formulation-level with LatentMAS-style
forced comparator; CLB narrowed to intra-layer branching + non-selection
merge with NoisyCoconut-style forced baseline.
**Finding #7 (TTPS).** Interpreter capability boundary + interpreter-only
baseline + decision rule installed in §C3 ("new computation" ≠ "new
capability of the frozen model"; interpreter-sufficiency → Not supported
for L3).
**Finding #8 (ASR).** Policy-scope declaration required
(per-instance/per-episode/test-stream + cross-instance-state boundary +
Law-#7 audit of carried state); current spec marked [INCOMPLETE]; Box 1
gains the Meta-Reasoner-beats-or-differs condition.
**Finding #9 (FLOP accounting).** Dual online/amortized accounting installed
in §G1b and applied in §§G2/G3/G5; "matched compute" = matched (a) online
inference FLOPs per item.
**Finding #10 (EXP023).** §A10 and R(e) replaced wholesale per the LOG-186
ruling as issued (seed-123 dev selection → pinned config → seed-84
confirmatory; no Bonferroni precommit; "Supported (L1, selection-optimism
caveat)" + pooled p=0.000488 with pre-specification caveat). Note: the
LOG-186 ruling's record is the research_log.md entry (line 3578); applied
exactly as issued.
**Burden of proof (mentor review's closing note, unnumbered).** Boxed standing note installed after §D2:
the next experiment must show what works is not already explained by the
newer prior art; a positive result a 2026 occupant predicts is Not supported
for the novelty claim.
**Finding #11 (preservation).** A4, A5, A6, A9, D2 (all five conditions),
F1's structure, H3's license, §I's definition and grades, the §B track-7
verdict, and the §I "rules out the entire corpus" note are unsoftened —
verified section by section (A5's Not supported now rests on the pooled
equivalence-to-null bound, a stronger footing, not a weaker one).

## R(i). LOG-191 patch record — per-defect changes (mentor-ordered, LOG-190/LOG-193)

**Defect 1 — M15 load-bearing (adoption blocker).** §G4 Branch S gains
condition (vii): the candidate-specific M15 comparator must be cleared at
the Level-2 standard (lower 99.286% CI > δ_min), or the pre-registered
structural-comparison path with all three trigger conditions met; an
[INCOMPLETE] M15 blocks Branch S (Inconclusive) — incompleteness is never
clearance. §G3's M15 line is replaced by four pinned executable protocols
(M15-LTPO, M15-MetaReasoner, M15-LatentMAS, M15-NoisyCoconut) with frozen
model, exact configuration, task construction, and two-number FLOP
accounting fixed before NTDP data contact; paper-free hyperparameters are
marked [PINNED-CHOICE] (program decisions, not claims about the papers).
The structural-comparison rule states its trigger conditions precisely
((a) pre-registered observable mechanism property independent of the gain
with an operational check; (b) established on the NTDP; (c) M15 still run
as a Level-3 control with a pre-registered failure-mode prediction) — and
M15 beating C\* at the Level-2 standard under the structural path renders
the structural claim Not supported. "Different architecture" alone never
qualifies. §D2 condition 3 now references the pinned protocols.
**Defect 2 — ASR consistency.** Every candidate-counting site now reads
**7 complete candidates + 1 pending candidate (ASR), not eligible for
experimental triage until policy scope is frozen**: §E summary table (C4
row), §E summary paragraph, §F1 (C4 excluded; its ablation specified
prospectively only), §G1b Level-2 budget (Bonferroni over 7: α₂=0.05/7=
0.00714, 99.286% CIs — corrected for the eligible set, not a weakening),
§§H1/H3/H4, §J Stage 1, the checklist. ASR's boxes remain answered; its
policy-scope declaration remains [INCOMPLETE] and gates all experimental
eligibility. E8 stays conditional (not incomplete). A held/ASR-pending
candidate never joins a running NTDP; admission requires a fresh
pre-registration with re-divided budget.
**Defect 3 — LCMIC bandwidth.** §F3 gains arm (e): latent channel compressed
to text-equivalent payload (pre-registered compression, frozen before data
contact). The bandwidth-isolation rule is a binding Branch-S licensing
condition (§G4 condition (v), §F3): L_(a−e) > δ_min → raw-capacity account,
channel-representation claim Not supported, Branch S BLOCKED; U_(a−e) <
δ_min → capacity account ruled out; CI overlap → Inconclusive, C5 held. C5's
Box 1 carries the (e) condition.
**Defect 4 — fresh-object audit.** New Appendix V (2026-09-23) records URL,
fetch date, exact supported claim, verdict, and textual consequence for
every load-bearing inherited citation (B1: CAA, Activation Addition; B4:
PPLM, Self-Refine; B5: DEER, STARS; A8: handover numbers via primary repo
artifacts). Anything not verified is narrowed or removed — nothing left
load-bearing. NoisyCoconut's bibliographic status re-checked against the
live TMLR index at patch time (see Appendix V); all body citations updated
to the current status.
**Defect 5 — CLLC corrected.** C1 Box 1's "no competitor predicts
bound-holding feedback beating its own open-loop ablation" is withdrawn;
Activation-LQR is named as the direct prior occupying exactly that
comparison; the surviving distinction is explicitly narrower
(observer/controller/plant separation + cached gains + pre-registered
relational-task setpoint construction + a measured bound-holding result
A-LQR's formulation does not predict).
**Also:** ELM's "no competitor has cross-pass accumulating state" narrowed to
the auditable fixed-slot scratch-buffer protocol claim (C2 Box 1); CLB's
duplicated merge-vs-select line removed and its "no competitor branches
inside the pass" absolute replaced with a reviewed-literature-scoped
statement (C6 Box 1); δ_min re-justified on treatment-independent
decision-theoretic grounds with the corpus-dependent anchoring removed and a
2/5/10pp sensitivity table reported (§G1b); §G4 Branch HOLD added
(program-level hold — neither kill nor license, release only via fresh
pre-registration); M15 structural-comparison rule installed (§G4).
**Preservation re-verified (mentor reads this file as a fresh object):** A1's
dissociation, A3's downgrade, A5's pooled equivalence, A6's no-oracle-ceiling,
A9's decision-flip rule, D2's five conditions (condition 3's comparator list
now points at the pinned §G3 protocols — same requirement, executable form),
F1's conditionality structure (C4's exclusion is an eligibility correction,
not a structural change), H3's kill license (conditions 1–4 unchanged in
substance; the HOLD-suspension clause makes explicit what "every candidate
lands in F1–F4" already entailed — a candidate with no verdict yet cannot
satisfy a condition about verdicts), and §I's L1/L2/L3 separation are
unweakened. The Level-2 re-division (8→7) follows ASR's exclusion from the
eligible set; E8's conditional activation does not reclaim budget
(conservative). R(h) is retained verbatim as the LOG-187 historical record;
where the live 2026-09-23 check changed a status R(h) records (NoisyCoconut),
the body is updated and the change is logged here, not back-edited into R(h).

---

## Standing-law compliance checklist (for the mentor's adversarial review)

- [ ] Epistemic double-labeling on every load-bearing claim — present
  throughout (canonical pair + 10-label).
- [ ] Evidentiary levels stated per claim, no silent crossing — L1/L2/L3
  tagged; §I grades bind the levels to named outcomes.
- [ ] Verdicts only from Supported / Not supported / Inconclusive /
  Underdetermined / Refuted — checked; the four banned phrases appear
  nowhere as verdicts.
- [ ] 7 complete candidates with both boxes answered (C1, E7, C2, C3, C5, C6,
  E8-conditional) + 1 pending candidate (C4/ASR, [INCOMPLETE] — not eligible
  for experimental triage until policy scope is frozen); see §E summary table.
- [ ] No theory preservation — §H3's license executes without re-approval;
  the demote branch is explicit; E8 is conditional rather than protected.
- [ ] P1 mechanism-level bar — §F1's conditionality criterion and §D2
  condition 4 operationalize it; score gains are never the success criterion
  (§G4 Branch F2).
- [ ] P2 evidence-not-identity — §A8; the synthesis is licensed to conclude
  SCPM is a dead end (§B track-7 verdict).
- [ ] P3 kill experiment as first-class gate — §H with explicit license.
- [ ] P4 competing hypotheses, not one grand narrative — §E's seven complete
  candidates (+ E8 conditional), pairwise mechanism-distinct; ASR pending —
  none assumed correct.
- [ ] Hierarchical alpha budget stated and binding — §G1b (finding #3).
- [ ] CI + δ_min decision rule applied at every primary comparison; the
  string "p ≥ 0.05" never used as evidence against a candidate (finding #2).
- [ ] Changed burden of proof installed as standing guidance — §D box
  (the mentor review's closing burden note, unnumbered).
- [ ] M15 genuinely load-bearing — Branch S condition (vii) requires clearing
  the pinned candidate-specific M15 comparator (§G3) at the Level-2 standard,
  or the pre-registered structural-comparison path with all three trigger
  conditions met; an [INCOMPLETE] M15 blocks Branch S (§G3/G4).
- [ ] Program-level Hold branch exists — §G4 Branch HOLD: neither kill nor
  license; release only via fresh pre-registration; never a rescue path.
- [ ] δ_min justified by treatment-independent practical relevance; exactly
  one value (5pp) frozen before NTDP data contact; 2/5/10pp sensitivity table
  reported (§G1b).
- [ ] Fresh-object citation audit complete — every load-bearing inherited
  citation carries a current (2026-09-23) Law #3 verification record in
  Appendix V; publication statuses current at patch time.
- [ ] LCMIC bandwidth isolation is a Branch-S licensing condition — §F3 arm
  (e) plus §G4 condition (v), not an appendix note.

---

## Appendix V. Fresh-object Law #3 verification record (LOG-191, 2026-09-23)

Every load-bearing inherited citation below was re-checked against its
primary source on 2026-09-23. Verdicts: VERIFIED (primary source supports
the exact claim as written), PARTIALLY VERIFIED (mechanism confirmed;
specific figures/venue rest on an earlier verification record, cited),
UNVERIFIED (not supported by the checked source — the claim is narrowed or
withdrawn, never left load-bearing). No GPU was used; all checks are
read-only fetches and repo artifact reads.

**V1. CAA — Rimsky et al.** Source:
https://arxiv.org/abs/2312.06681 and
https://aclanthology.org/2024.acl-long.828/ (checked 2026-09-23).
Verdict: VERIFIED. Supported claim: contrastive activation addition —
steering vectors computed from contrastive prompt pairs steer model
behavior without training. Consequence: B1's static-steering prior-art
claim stands.

**V2. Activation Addition — Turner et al.** Source:
https://arxiv.org/abs/2308.10248 (checked 2026-09-23). Verdict: VERIFIED.
Supported claim: activation addition at inference steers outputs without
weight updates. Consequence: B1 stands.

**V3. PPLM — Dathathri et al., ICLR 2020.** Source:
https://arxiv.org/abs/1912.02164 (checked 2026-09-23). Verdict: VERIFIED.
Supported claim: frozen LM with per-step inference-time updates to hidden
activations guided by an attribute evaluator, Δθ=0; the evaluator is an
external label-trained classifier. Consequence: B4's "per-instance
inference-time representation intervention of a frozen model guided by an
evaluator has been occupied since 2020" stands, with the external-evaluator
break as stated.

**V4. Self-Refine — Madaan et al., NeurIPS 2023.** Source: NeurIPS
proceedings abstract,
https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html
(checked 2026-09-23). Verdict: VERIFIED for the generate→feedback→refine
mapping. Supported claim: the same LLM serves as generator, feedback
provider, and refiner, iteratively; no supervised training data, no
additional training, no reinforcement learning; outputs preferred over
one-step generation across 7 tasks (~20% absolute average gain), at test
time with one model. UNVERIFIED: "gains plateau after 2–3 iterations" and
"self-critique has blind spots" — neither appears in the checked source.
Consequence: B4 rewritten — the mapping is retained with the verification
tag; the plateau/blind-spot sentences are withdrawn as factual claims and
restated as an explicit [HYPOTHESIS].

**V5. DEER — Yang et al., 2025.** Source:
https://arxiv.org/abs/2504.15895 (checked 2026-09-23). Verdict: VERIFIED.
Supported claim: training-free, confidence-gated dynamic early exit of CoT
at reasoning transition points; 10 reasoning benchmarks, 11 reasoning
LLMs; CoT length reduced 19.1%–80.1%, accuracy improved 0.3%–5.0%.
Consequence: B5 stands.

**V6. STARS — Yang et al., 2026.** Source:
https://arxiv.org/abs/2605.26733 (checked 2026-09-23). Verdict: VERIFIED.
Supported claim: a *training* framework (STAbility-driven Recurrent
Scaling) constraining looped-LM latent states toward asymptotically stable
fixed points via efficient Jacobian Spectral Radius Regularization with
random loop sampling — motivated by the observed peak-then-collapse of
performance with further recurrence depth. Consequence: B5 stands; STARS is
excluded from the Δθ=0 core (training required) and used as a constraint
predicting gain-then-collapse for unstabilized frozen loops.

**V7. ∇-Reasoner — Wang et al., ICLR 2026.** Source:
https://arxiv.org/abs/2603.04948 (abstract checked 2026-09-23). Verdict:
PARTIALLY VERIFIED. Supported claim (abstract): Differentiable Textual
Optimization — test-time gradient descent on token logits in the decoding
loop; gradient signals from the LLM's likelihood and a reward model; over
20% accuracy improvement on a challenging math benchmark with ~10–40%
fewer model calls than strong baselines; no weight updates. The
80.4%-on-MATH-500 / Qwen-2.5-7B-Instruct / GRPO figures and the ICLR 2026
venue rest on the LOG-185 web-search/proceedings verification, not on
today's fetch. Consequence: B5 stands with the provenance split stated in
the tag.

**V8. Activation-LQR — Skifstad, Yang & Chou.** Source:
https://arxiv.org/abs/2604.19018 (abstract checked 2026-09-23). Verdict:
VERIFIED for the mechanism; venue per earlier record. Supported claim
(abstract): layer-wise transformer dynamics are well-approximated by
locally-linear models; inference modeled as a linear time-varying system;
LQR feedback controllers computed from layer-wise Jacobians steer
activations toward semantic setpoints in closed loop, with theoretical
tracking-error bounds, no offline training, no parameter updates. The ICML
2026 venue rests on the LOG-185 proceedings-listing check. Consequence: B5
stands; the CLLC correction (A-LQR as the direct prior) is verified.

**V9. Meta-Reasoner — Sui et al.** Source:
https://arxiv.org/abs/2502.19918 (abstract checked 2026-09-23). Verdict:
VERIFIED for the mechanism. Supported claim (abstract): contextual
multi-armed bandits learn an adaptive policy over reasoning strategies
(backtrack, change decomposition, restart) from the LLM's reasoning state
at inference time; 9–12% accuracy gains and 28–35% inference-time reduction
under the same compute budget. The Findings-of-ACL-2026 venue rests on the
LOG-185 record. Consequence: D1 and the M15-MetaReasoner protocol stand.

**V10. LTPO — Ye, Liang & Shan.** Source:
https://arxiv.org/abs/2510.04182 (abstract checked 2026-09-23; ICLR 2026
publication confirmed via the paper's published footer). Verdict:
VERIFIED. Supported claim: parameter-free, entirely test-time framework;
latent thought vectors treated as dynamic parameters optimized per problem
instance via online policy gradient guided by an intrinsic confidence
reward computed from the frozen LLM's own output distributions; no model
parameter updates, no external supervision. Consequence: D1 and the
M15-LTPO protocol stand; the reward operationalization in §G3 is marked
[PINNED-CHOICE] where it goes beyond the abstract.

**V11. LatentMAS — Zou et al.** Source:
https://arxiv.org/abs/2511.20639 (abstract checked 2026-09-23; ICML 2026
Spotlight per the paper's comments). Verdict: VERIFIED. Supported claim:
end-to-end training-free framework for pure latent collaboration among LLM
agents; autoregressive latent-thought generation through last-layer hidden
embeddings; a shared latent working memory preserving and transferring
each agent's internal representations and latent thoughts — lossless
information exchange without text mediation; 9 benchmarks, up to 14.6%
higher accuracy, 70.8%–83.7% token reduction. Consequence: D1's Family I
and the M15-LatentMAS protocol stand; this record confirms the LOG-187
retraction of the "no competitor uses inter-instance latent exchange"
sentence — LatentMAS is the prior-art family for H5a/LCMIC.

**V12. NoisyCoconut — Jerge & Evans, TMLR June 2026.** Sources: live TMLR
index https://www.jmlr.org/tmlr/papers/ (checked 2026-09-23 — entry
"NoisyCoconut: Counterfactual Consensus via Latent Space Reasoning,
Michael M. Jerge, David Evans, June 2026" present) and
https://arxiv.org/abs/2605.08221 (abstract checked 2026-09-23). Verdict:
VERIFIED. Supported claim: published at TMLR, June 2026 (the "under review
at TMLR" status is stale and withdrawn everywhere in the body); an
inference-time method operating directly on model representations with no
retraining; controlled noise injected into latent trajectories generates
diverse reasoning paths; agreement among paths is a confidence signal
enabling abstention under uncertainty (unanimous agreement drives error
rates below 15% on math reasoning via selective abstention). The abstract
does not specify K, σ, or a diversity metric — K=5, σ=0.1, and the cosine
diversity/aggregation choices in §G3 are marked [PINNED-CHOICE]
operationalizations. Consequence: D1, C6, and M15-NoisyCoconut updated to
published status; the mechanism description narrowed to abstract-verified
claims.

**V13–V17. A8 primary artifacts (repo-local).** Checked 2026-09-23 by
direct JSON reads under `experiments/runs/` (the `research/handover/` path
cited in earlier drafts does not exist). Verdict: VERIFIED.
- V13 EXP048 (`EXP048_regression_lock/exp048_regression_results.json`):
  baseline 0.60, intervention 0.74, ΔM=+0.14, b=7, c=0, McNemar
  p=0.0078125.
- V14 EXP049 (`EXP049_multi_seed_invariance/exp049_multi_seed_results.json`):
  pooled baseline 0.60, intervention 0.67, ΔM=+0.07, b=17, c=3,
  p=0.0012884, 95% CI [0.03, 0.115]; per-seed significance fails on seed 42
  (p=0.363); metadata verdict FALSIFIED_OR_WEAK.
- V15 EXP056 (`EXP056_autonomous_lifecycle/exp056_autonomous_results.json`):
  baseline 0.60, unsupervised-selected 0.64 (+4pp autonomous), oracle 0.74;
  b=2, c=0, exact McNemar p=0.25 one-sided (0.50 two-sided) — not
  significant; verdict SELECTION_BOTTLENECK_ACTIVE. The +4pp belongs to
  EXP056, not EXP057.
- V16 EXP057 (`EXP057_blind_discovery/exp057_discovery_results.json`): blind
  autonomous 0.4083 vs baseline 0.45 (−4.2pp); verdict
  DISCOVERY_BOTTLENECK_PERSISTS.
- V17 EXP058 (`EXP058_basis_transfer/exp058_transfer_results.json`):
  matched causal→causal transfer 0.5333 vs baseline 0.60 (−6.7pp); verdict
  TRANSFER_WEAK_OR_SPECIFIC.
Consequence: A8 rewritten with exact paths, numbers, and the stated
caveats (P2 score observations; no matched modern baselines; selection
context unverified).

**Not re-verified today (non-load-bearing inherited references).** RISER
(D1 adjacent-excluded), Tree of Thoughts (B4 comparative), and venue-only
claims for ∇-Reasoner / A-LQR / Meta-Reasoner (LOG-185) were not re-fetched
on 2026-09-23; they carry no synthesis verdict and are cited with their
original provenance. If any becomes load-bearing for a verdict, it must
earn a V-record first.

*End of revised synthesis. LOG-191 patch dispatch discharged. No GPU used;
no signed protocols, primary artifacts, or the mentor review file modified.
Fresh-object verification: Appendix V (2026-09-23). Awaits Law #14 review
(LOG-192) before program adoption; G/H pre-registration triggers
on landing.*
