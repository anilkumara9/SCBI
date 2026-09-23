# Adversarial Review — 7 New Sprint Proposals (2026-09-23)

**Reviewer:** Adversarial Reviewer
**Status:** REVIEW COMPLETE — 2026-09-23
**Scope:** the 7 proposals appended to `research/innovation/SPRINT_2026-09-23.md` under
`## New proposals (2026-09-23) — PENDING ADVERSARIAL REVIEW`, synthesized from the
Sept 2026 field sweep (`~/workspace/research_notes/llm-inference-control-2026-update-20260922-2118/`).
**Method:** per-proposal check on (1) five-element completeness (Research Operating
System §2 Monday standard), (2) duplication vs the 8 existing ideas + EXP067/068/070/075,
(3) novelty honesty (N1; P1's N2 candidacy), (4) kill-criterion teeth, (5) sweep
fidelity (verified against the sweep report + notes, not on trust), (6) sequencing.
Sprint file NOT edited. No subagents spawned.

## Sweep fidelity — verified, not trusted

All five arXiv IDs verified verbatim in the sweep report:
- `2602.01654` — SVF (Li et al., Feb 2026, `verified live`) ✓
- `2604.19018` — A-LQR (Skifstad, Yang & Chou, submitted 21 Apr 2026, `verified live` abstract) ✓
- `2505.22637` — Braun et al. (ICLR 2025 Workshop, `verified live` abstract) ✓
- `2407.12404` — Tan et al. (cited 2025 in SVF, `index`) ✓
- `2512.05534` — SDL unified theory (Dec 2025, `index`) ✓

Load-bearing details match the sweep notes verbatim: SVF KNN (K=64 centroid of nearest
target-bank neighbors, Model-Written-Evals, Llama-2-7b-Chat layer 15, beats CAA on
Corrigible/Coordinate, Narcissism unsteerable even under KNN); Braun (36 binary-choice
datasets, 7 prompt types, layer 13, all net-positive but high variance, directional
distinctness across prompt types); Tan (anti-steerable fraction 3–50%, avg ~1/3, 36
datasets); refusal-cone (algoverse-bias-steering, Aug 2026, LOW-confidence secondary;
QCRI ~11 flavors; ACE — qualifier preserved, not laundered); CAST (Lee & Padhi, ICLR
2025, arXiv:2409.05907v3, `index`); A-LQR (locally-linear LTV dynamics, layer-wise
Jacobians, semantic setpoints, tracking-error bounds); NLA
(transformer-circuits.pub/2026/nla, `verified live`); Gemma Scope 2 (Dec 2025, `index`);
Maar et al. negative cross-model evidence (arXiv:2601.20164, low-confidence secondary
via candle-mi README — matches the cut list). HyperSteer correctly tagged `UNVERIFIED`
per Law #3. **Not re-verified in this pass:** two specific performance figures (WAS
~89% refusal with benchmark preservation; EAGER −65% tokens / +37% Pass@k) — recommend
the integrator spot-check these against the sweep notes before preregistration.

## P1 — Online search vs the learned vector field (SVF head-to-head)

**Completeness:** 5/5 ✓ (question, dated sweep citation, cheapest falsifying experiment,
kill criterion with exact numbers, credible cost <30 min T4).
**Duplication:** none — retrieval-based steering baseline is new to the program.
**Novelty:** the N1-until-mechanism framing is sound; the N2 bid is correctly deferred
to mechanism identification per the revolution test. The "principle vs combination"
argument does not overclaim *as written in the N1-framing paragraph*.
**Sequencing:** runs after EXP070/068 with oracle fallback — sane.

**Findings (all require fixes):**
- **[F1 — framing mismatch]** The title says "Online search vs the *learned vector
  field*" but the experiment implements SVF's *KNN baseline* (training-free retrieval),
  never the learned MLP field. The operative comparison is KNN-retrieval vs
  loop-selection — two training-free adaptive methods. Fix: retitle/restate the
  comparison honestly; the offline-learned field is cited, not run.
- **[F2 — overclaim]** "The program's loop is the first demonstration that search-time
  computation substitutes for training-time learning in representation control" — SVF's
  own KNN result (training-free retrieval beating CAA on Corrigible/Coordinate) is
  already that demonstration on behavior tasks. Fix: narrow to "on 2-hop relational
  reasoning" or "loop-selection matches retrieval-based adaptation."
- **[F3 — kill teeth]** The success condition uses bare non-significance ("ΔM_online ≥
  ΔM_SVF-KNN with p ≥ 0.05 for the paired difference → online matches"). Non-significance
  is not equivalence; an underpowered test manufactures "success" and hands the program
  a motivated-continuation hatch. Fix: pre-register a non-inferiority margin (e.g.,
  ΔM_online within −5pp of ΔM_SVF-KNN, [ARBITRARY] with sensitivity bands) or a
  TOST-style bound. The two-sided redirect (SVF-KNN fails to beat static → premise
  withdrawn) is good and must be kept.

**VERDICT: ACCEPT-WITH-FIXES (F1, F2, F3).**

## P2 — The loop as a closed-loop controller (A-LQR)

**Completeness:** 5/5 ✓ (cost tagged [CONJECTURE — log actuals] ✓; 160m pilot gates
410m ✓).
**Duplication:** none — control-theoretic formulation comparison is new.
**Novelty:** honest — "the program's contribution becomes the benchmark and the
formulation comparison, not the operator (that credit stays with A-LQR)" ✓.
**Sequencing:** loop arm needs EXP070/068 signal; the oracle fallback keeps it runnable.

**Findings (all require fixes):**
- **[F1 — unpinned primary]** Two setpoint candidates are offered (label-informed
  mean-of-correct-answers vs output bridge) but the formulation kill's meaning depends
  on which is primary. Fix: pre-register one primary setpoint (recommend the output
  bridge — the direction already known causal, keeping the label budget symmetric
  with the loop's oracle fallback); the other as a secondary arm.
- **[F2 — kill license depends on the arm]** The formulation kill ("A-LQR rescues while
  our loop-selected direction does not → G/E/S is the wrong architecture") is licensed
  on the loop-selected arm, but the experiment allows an oracle fallback — under which
  the kill would license only "feedback control beats oracle selection," a weaker and
  different claim. Fix: pre-register which arm the formulation kill is licensed on.
- **[F3 — minor partition gap]** (A-LQR ΔM=0, bounds hold) is unruled: the reframing
  kill requires bound-failure AND ΔM=0. Fix: name it — "controller implements
  faithfully but is relationally inert" → reframing neither killed nor adopted;
  report as a negative.

**VERDICT: ACCEPT-WITH-FIXES (F1, F2, F3).**

## P3 — Anti-steerability + coherence as mandatory pre-registration gates

**Completeness:** 5/5 ✓. **Cost:** $0 GPU — re-analysis of archived artifacts ✓.
**Duplication:** none — methodology, not a mechanism; the protocol-amendment
implication is a feature, not a bug.
**Sequencing note:** if the >15% branch fires, EXP068/070's *signed* evaluators need a
per-sample harm-ledger amendment → Law #14 re-review before execution. The proposal
should state this consequence.

**Findings (all require fixes):**
- **[F1 — partition gap, m7-style]** Branches: ≤5% + high coherence → premise withdrawn;
  >15% → gate adopted. The 5–15% band is unruled. Fix: define it (recommend: report
  the ledger, no protocol change, sensitivity bands retained).
- **[F2 — degenerate branch]** b=c=0 is already established for EXP065/066 static
  injection — the per-item signed ledger is therefore nearly guaranteed to return a 0%
  anti-steerable fraction, so the "premise withdrawn" branch fires trivially. This does
  not invalidate the proposal (the coherence diagnostics and the gate-adoption machinery
  are the real payload, and confirming the trivial zero is still a logged measurement),
  but the proposal must name the degenerate branch explicitly rather than presenting
  the fraction as an open empirical question on this artifact. The open question is
  coherence, not the fraction.
- **[F3 — feasibility assumption]** The proposal assumes per-instance signed outcome
  ledgers exist in the EXP065/066 archive. Fix: verify before scheduling — if only
  aggregate McNemar tables were archived, the fraction is uncomputable and the proposal
  reduces to coherence diagnostics on contrast pairs.

**VERDICT: ACCEPT-WITH-FIXES (F1, F2, F3).**

## P4 — Gemma 3 + Gemma Scope 2 (feature-level validation)

**Completeness:** 5/5 ✓; assumptions logged, not hidden (gated HF access = user action;
transcoder download staging) ✓.
**Duplication:** none; "port, not a backbone migration — the Pythia results stand on
their own" ✓. Minor: P1 calls SVF's cross-layer alignment space "the 2026 successor
to our Procrustes pillar" while P4 calls transcoders "the modern replacement for our
Procrustes-alignment pillar" — two heirs to one pillar. Fix: pick one framing
(recommend transcoders as the alignment successor, SVF as the adaptive-search prior)
or name both as candidate successors.
**Novelty:** "first N2-adjacent evidence — *if* the identifiability guard survives" is
conditional and sound; N2 candidacy is deferred to mechanism identification per the
revolution test ✓. The SDL tempering prior is carried honestly and the two-seed
replication guard is the right identifiability check ✓.

**Findings:**
- **[F1 — unruled invalid branch]** The kill requires "a feature-mapped output bridge
  rescues" as the positive control, but the branch where the feature-mapped bridge
  FAILS to rescue is not pre-registered — that outcome is uninformative (no positive
  control), not a kill. Fix: add the invalid-run branch (bridge fails → halt,
  re-design the feature mapping; not evidence for the boundary).

**VERDICT: ACCEPT-WITH-FIXES (F1 + dual-mantle wording).**

## P5 — The adaptivity tournament

**Completeness:** 5/5 ✓; cost <45 min T4 credible ✓.
**Duplication:** distinct from P1 — a 4-way adaptivity-*form* tournament vs a head-to-head;
the relationship to P1 (SVF-KNN arm) and P6 (CAST-style gate) is explicit ✓. WAS's
*trained* controller correctly excluded under Law #6; only training-free gating logic
admitted ✓. First Finish Search duplication correctly avoided (covered by EXP068's
output-level search comparison) ✓. The EAGER arm is explicitly a per-instance *budget*
port, audited by the per-instance α ledger — honest about what it is ✓.
**Novelty:** "the first head-to-head of adaptivity *forms* on one benchmark — an N1
experimental design, honestly labeled" ✓.

**Findings:**
- **[F1 — unruled tie]** "If exactly one form wins → winner becomes baseline, losers
  culled." The multiple-winner/tie case is unruled. Fix: pre-register a tie rule
  (e.g., joint winners survive to a pairwise runoff, or a stated priority order).

**VERDICT: ACCEPT-WITH-FIXES (F1).**

## P6 — Cone-vs-line geometry

**Completeness:** 5/5 ✓. **Sweep fidelity:** LOW-confidence provenance preserved
("carried in the protocol, not laundered out"; QCRI/ACE = practitioner-doc claims
only; dated Aug 2026 citation) ✓.
**Duplication:** none; overlap with old Idea 5's offset arm is explicit, joint-run,
cited ✓.
**Kill teeth:** the strongest in the set — two-way falsifiability: flat-zero across
the α grid kills the cone hypothesis; a peaked curve *withdraws the program's own
blanket null* and replaces it with a geometry-conditional claim. The α grid is
[ARBITRARY] and pre-registered with Law #9 cited against cherry-picking; the
response *curve* is the endpoint, correctly chosen ✓.
**Novelty:** N1, honestly labeled ✓.
**Sequencing:** joint with Idea 5 — sane.
No fixes required. Non-blocking note: the Anthropic circuit-tracing citation (Mar 2025)
is tagged `index` per sweep convention — carried as-is.

**VERDICT: ACCEPT.**

## P7 — NLA-derived directions as the loop's generator

**Completeness:** 5/5 ✓; the only pilot-gated proposal (1–2 h T4 [CONJECTURE]) ✓.
**Duplication:** none. Confabulation carried as the standing falsifier ✓; HyperSteer
tagged `UNVERIFIED` per Law #3 ✓.
**Novelty:** "A novelty bid requires the systematic comparison (NLA vs contrast as
generators) — not the direction itself" — sound ✓.

**Findings (all require fixes):**
- **[F1 — host-model feasibility hole, substantive]** "Take an open-model NLA (released
  by Anthropic)" — but our benchmark runs on Pythia-410m, and an NLA verbalizes a
  *specific* model's activations (the cited demonstration is on Opus 4.6). As written
  the experiment is infeasible: no NLA for Pythia-410m is named and no port plan is
  given. Fix: specify the host model for which a released NLA exists and port the
  2-hop benchmark to it (a P4-style port, stated and costed explicitly), or restrict
  the proposal to "if an NLA for our backbone exists." Without this the kill criterion
  cannot fire because the experiment cannot run.
- **[F2 — partition gap, m7-style]** The kill requires the conjunction (ΔM=0 AND
  cos(d_NLA, v̂)<0.3). The (no rescue, cos≥0.3) cell — the NLA captures the concept
  geometrically but it is not causal — is unruled. Fix: pre-register it (recommend:
  "geometric agreement without causal efficacy" — weakens the confabulation reading,
  does not cull; the generator question stays open pending a different edit strategy).
- **[F3 — minor]** The success branch ("d_NLA rescues → candidate generator for
  EXP068's G") does not compare against C2 B_agg — but the standing boundary null is
  ΔM_static=0, so any significant rescue beats static. Fix: state this anchoring
  explicitly so the success license is tied to the null it defeats.

**VERDICT: ACCEPT-WITH-FIXES (F1, F2, F3).**

## Verdict summary

| # | Proposal | Verdict |
|---|---|---|
| P1 | SVF head-to-head | ACCEPT-WITH-FIXES (title/framing honesty; narrow "first demonstration"; non-inferiority margin) |
| P2 | A-LQR | ACCEPT-WITH-FIXES (pin primary setpoint; pin kill's licensed arm; name the faithful-but-inert cell) |
| P3 | Anti-steerability gates | ACCEPT-WITH-FIXES (define 5–15% band; name degenerate branch; verify ledgers exist) |
| P4 | Gemma Scope 2 | ACCEPT-WITH-FIXES (invalid-run branch for failed feature bridge; one Procrustes-mantle framing) |
| P5 | Adaptivity tournament | ACCEPT-WITH-FIXES (tie rule) |
| P6 | Cone-vs-line | ACCEPT |
| P7 | NLA generator | ACCEPT-WITH-FIXES (host-model/port feasibility; partition the no-rescue/high-cos cell; anchor success to the null) |

**7 accepts (1 clean, 6 conditional), 0 rejects.** Every proposal has all five required
elements, decision-change endpoints, free-tier costing, preserved sweep confidence
qualifiers, and N1 framing. No proposal duplicates the existing 8 ideas or
EXP067/068/070/075. The cut list is sound: genuine duplicates folded (cross-model
transfer → ★; WAS-trained and TTRL cut on Law #6; Iterative Sparse Matrix Steering
and Steerling-8B cut on confidence), Dynamic Cheatsheet parked with a named
resurrection condition, many-shot TTA absorbed as a design warning, refusal-cone
correctly scoped to our task rather than refusal itself.

**Strongest and weakest, for the CEO's sequencing:** P6 is the cleanest proposal in the
set and the cheapest mechanism test available — it can narrow the program's own
headline null and should be preregistered early. P3 is the cheapest falsification in
the set ($0 GPU) and its >15% branch would amend signed protocols, so it should run
before any EXP068/070 execution. P7 is the least feasible as written (F1) and must
not be preregistered until the host-model question is answered.
