# PARADIGM-BREAK SPRINT — think differently (LOG-4693)

*Deep-strategy sprint lane: LOG-4693 (pre-assigned). $0 CPU, strategy
dossier only. No experiment numbers minted, no signed protocol touched,
no GPU contact, no execution licensed, nothing committed. Every family
below requires its own worth-it gate + signed pre-registration +
independent Law #14 review before any execution (launch chain).*

**Read:** `research/benchmarks/FRONTIER_SCOREBOARD.md` (v3.1),
`research/analysis_plans/G1_REPORT_2026-09-23.md`,
`research/innovation/SPRINT_2026-09-29_SUMMIT.md`,
`research/strategy/INNOVATION_DESIGN_SESSION_POST_EXP123_2026-09-29.md`,
`research/innovation/SPRINT_2026-09-25_SUMMIT.md` (TGA pilot, ranked #2,
never executed).

**Founder directive (2026-09-29):** the current paradigm has hit a wall;
think fundamentally differently, not more variants of the same
instruments. This dossier is the answer.

---

## 1. The paradigm that died, and why

**Name: the static-snapshot instrument paradigm.** Every family in the
RUN-INVALID/KILL columns shares one unexamined move: measure or
manipulate a *frozen activation snapshot* — one layer, one token
position, one forward pass — and treat the number as a fact about the
model's cognition. Probes decode the snapshot. Bridges add a fixed
direction to the snapshot. Logit readouts score the snapshot. Dose
sweeps scale the snapshot's perturbation. Plan compositions bolt text
onto the snapshot's prompt. The transformer is treated as a fixed-point
map f(x) = y, and the research program spent six months instrumenting y.

**Why it died — the mechanism of death, not just the tally.** The
negative is clean and replicated because the *object* is wrong, not
because the instruments were sloppy:

- The instruments worked: decodability hit 6.7× chance (EXP105),
  27/30 with position decorrelated (EXP122), guards passed on every
  KILL (EXP125, EXP126).
- The causal channel never opened: ΔM = 0 at L20 (EXP077) and L11
  (EXP094); the shared task direction is inert (EXP093); per-arm
  effects ≥ 4.87% are dead (S5-2); eight decode-probe variants found
  never-decodable rooms, not decodable-yet-inert (S5-3).
- Every "number that went up" was manufactured by the instrument, not
  found in the model: bridges were label-informed (LOG-204), the
  60/60 trained-head transfer was a template artifact (EXP107), the
  three-bench decodability CONTINUEs were domain-set detectors
  (EXP126), the honesty readout was a one-bench phenomenon (EXP125),
  entity-name "generation" was regurgitation (EXP124's 60/60
  hallucinated premises).

[INTERPRETATION] A transformer is not a map from snapshots to
decisions. It is a **dynamical system**: a residual stream evolving
over 24 layers and over generation steps. Information lives in the
*trajectory*; the static paradigm measured *cross-sections* and then
was surprised the cross-sections don't steer the trajectory. The
program's own unfollowed measurement says this in numbers: EXP086
Stage A measured Henrici non-normality **He = 0.7332–0.8343 (mean
0.7689) across all 48 attention blocks** — the layer dynamics are
strongly non-normal, i.e., the dynamics are *not* diagonalizable into
independent modes, perturbations do *not* evolve along the directions
we inject them, and eigenvalue-style (static-geometry) analysis
*cannot* see the amplification structure. We measured the reason the
static paradigm fails, filed it as "advisory," and went back to
probing snapshots.

**What the negative licenses:** boundary-science claims with exact
bounds — per-arm ≤ 4.87% static effects dead at two layers (S5-2);
never-decodable rooms exist (S5-3); the boundary is precision-
certified under INT8 fake-quantization (EXP110); head readouts are
characterized as domain-set detectors (EXP126); honesty readouts are
tagged bench-specific (EXP125). These are real, publishable, falsified
facts about a 410M frozen model.

**What the negative forbids:** any claim that decodability implies
steerability (the program's own headline kills it); any capability
claim from a label-informed construction; any new static-injection
lane at any strength, layer, gating, or dose (EXP094–097 + S6 wave +
S5-2 bound fence it); any "one more bench" whose purpose is another
decodability number; any resurrection of KILLED hypotheses (H22
generality, H23 identity interpretation, entity-name generation,
bench-2 logit reuse, QK-subspace operators).

---

## 2. The one unfollowed lead, stated plainly

EXP086 Stage A (CPU, read-only, Δθ=0 verified, LOG-331): the attention
blocks' Jacobians are strongly non-normal. In non-normal dynamics,
perturbations can be **transiently amplified by factors ≫ 1 over a
finite layer span even when every eigenvalue is stable**
([THEOREM] Kreiss Matrix Theorem; Trefethen & Embree). The static
program injected along *semantic* directions (concept vectors, bridge
directions, task normals) — directions the model's *dynamics* were
never consulted about. The dynamics' own maximally-amplified direction
is the leading right singular vector v_1 of the layer-to-layer
propagator M = Π J_t, and **no static injection in the program's
history has ever been along v_1**. We spent a year pushing the model
along directions it damps, and filed the damping as a boundary.

The 2026-09-25 summit sprint ranked the TGA pilot #2 (randomized power
iteration + Hutchinson, ~1 CPU-hour, kill rule pre-drafted: gain ratio
< 2 kills the dynamics-matched program pre-GPU). It was never
executed. The 2026-09-28 sprint absorbed the team's bandwidth into the
S6 wave and never re-ranked it. **This is the lead this dossier
engages first.**

---

## 3. Candidate families — each with the six worth-it items

Forbidden by §1 are excluded a priori: no new bench for a decodability
number, no probe/head/readout as steering, no layer/strength/gating
sweep of injection, no plan-text-near-prompt composition without a
generation-construct-validity gate (defect class 8).

### Family A — TGA: transient-growth amplification along the dynamics' own leading direction (the unfollowed lead)

**Mechanism sketch.** Compute the leading right singular vector v_1 of
the frozen L20→L24 (or full-depth) residual-stream propagator via
randomized power iteration on autograd Jacobians — $0 CPU, no training,
Law #7 clean (no labels anywhere). The pilot's discriminant is the
gain ratio R = σ_max/σ̄ (maximal vs mean directional gain). If R ≥ 3,
the dynamics contain a usable directional amplifier and the program
has its first *dynamics-matched* intervention direction — inject the
task signal along v_1 vs matched-norm random directions vs the dead
semantic B_agg (the EXP077 direction, ΔM=0) on the EXP107 bench. If
R < 2, He≈0.77 was a red herring and the dynamics-matched program
stands down before a single GPU minute.

1. *Exact question:* Does the frozen model's layer propagator contain
   a distinguished amplified direction (R ≥ 3), and does injecting
   along it move decisions where semantic-direction injection moved
   nothing?
2. *Decision changed:* CPU pilot R ≥ 3 → CONTINUE to a GPU injection
   test with a real license (the first licensed injection direction
   since the static family closed); R < 2 → KILL the dynamics-matched
   injection program pre-GPU (§2's lead retired honestly).
3. *Cheapest test:* randomized power iteration + Hutchinson estimator
   on autograd Jacobians of the frozen propagator, CPU, ~1h, $0. No
   forwards beyond the Jacobian-vector products; no labels.
4. *Mathematical license:* [THEOREM] Kreiss Matrix Theorem —
   sup_k ‖A^k‖ ≥ ρ_ε(A)/ε for non-normal A, so transient growth ≫ 1
   is possible with all eigenvalues stable; [THEOREM] SVD/power
   iteration — v̂_1 maximizes ‖J·u‖, so downstream logit displacement
   σ_1·ε is maximal over unit directions; EXP086's measured He≈0.77
   is the existence condition (a near-normal network would have no
   such direction to find).
5. *Quantitative prediction:* R ≥ 3 on the L20→L24 propagator (bar set
   below the ×1.8 precedent in the 9-24 ambition packet to be fair);
   gain rank-orders with singular rank in the injection stage.
6. *Breaking point:* R < 2 → KILL (pre-GPU); flat gain across singular
   ranks (p ≥ 0.1 for rank trend) → KILL; ĉ < 0.1 (gain is
   decision-orthogonal) → KILL; σ_1/σ_2 ≈ 1 (no distinguished
   direction) → KILL.

*What kills it:* the CPU pilot's own ratio — no GPU needed to kill.
*What constrains it:* S5-2's 4.87% bound covers *semantic/static*
directions; v_1 is a new direction class under Law #4, not a dose
tweak. G1's QK-subspace kill constrains mechanism *accounts*, not
this measurement (the propagator is the full residual update, not the
QK projector).

### Family B — DSF: dynamical sensitivity-field mapping (derived — the map the loop needs)

**Mechanism sketch.** The program has measured *information*
(decodability) and *influence* (flips) but never *sensitivity* — the
third quantity a dynamical view needs first. Freeze the prefix,
generate two completions under a counterfactual prompt perturbation,
and measure S = ‖trajectory(x+δ) − trajectory(x)‖ / ‖δ‖ in residual
space across all 24 layers: a sensitivity field over (layer,
position, context). No semantic direction, no label, no probe, no
head — Law #7 clean by construction. This is generation-as-
intervention, not generation-as-measurement (EXP123's terminal rule
covers elicitation-as-readout; this elicits nothing, it perturbs and
measures divergence). The field tells Family A *where the amplifier
is* and Family C *where to close the loop*.

1. *Exact question:* Is the frozen model's dynamical sensitivity
   field structured (concentrated, layer/position-dependent) or
   uniform — i.e., does the computation have soft spots a
   dynamics-first intervention could exploit?
2. *Decision changed:* structured field with layer-concentrated
   sensitivity (top-3 layers carry ≥ 50% of total S) → CONTINUE as
   the targeting map for Families A/C; uniform field (Gini < 0.2
   across layers) → KILL the "soft spot" premise — the model is
   dynamically homogeneous and dynamics-matched targeting has
   nothing to aim at.
3. *Cheapest test:* 20 item pairs × {unperturbed, δ-perturbed}
   completions × 24 layers of residual norms, frozen Pythia-410m
   CPU, ~1–2h, $0. δ is a fixed meaningless token swap (no semantic
   content — the perturbation must carry no task signal, or the
   field confounds with content).
4. *Mathematical license:* [THEOREM] finite-difference sensitivity is
   the model-free estimator of the propagator norm field;
   [OBSERVATION] EXP086's He≈0.77 guarantees the field is not
   trivially flat *if* the non-normality is load-bearing rather
   than decorative — this family is the test of exactly that.
5. *Quantitative prediction:* under load-bearing non-normality,
   layer-Gini ≥ 0.4 with sensitivity concentrated mid-to-late
   (L14–L22); under decorative non-normality, Gini < 0.2.
6. *Breaking point:* Gini < 0.2 → KILL; sensitivity concentrated
   only at the final layer (already instrumented — adds nothing) →
   KILL as independent family (folds into A as a targeting note).

*What kills it:* its own uniformity statistic — no downstream
experiment needed. *What constrains it:* the generation channel is
dead *as a measurement of content* (EXP115/116/123) — this family
never reads content, only trajectory norms, so the terminal rule
does not touch it; Law #14 must rule on that distinction at
pre-registration.

### Family C — CLP: closed-loop adaptive pursuit (CLLC narrowed, never tested)

**Mechanism sketch.** Every dead injection was open-loop: add δ once
at layer L, hope. The frontier's working form (Activation-LQR) is
closed-loop: u_t = −Kx_t, recomputed from the evolving state. The $0
shadow: two-step Newton-on-the-residual — inject δ_1 at L20, read the
residual displacement at L24, re-target δ_2 = δ_1 + correction from
the measured displacement, vs fixed-δ and vs δ_1+δ_2 open-loop sum.
The differentiator from the killed EXP095 dose-response is that the
*direction adapts to state*; it is not a bigger α. This is the
honest CPU pilot of the GPU-gated CLLC/EXP086-B line.

1. *Exact question:* Does state-feedback re-targeting of an injection
   move the residual (and the decision statistic) further per unit
   norm than any open-loop injection the program has tried?
2. *Decision changed:* two-step closed-loop displacement-per-norm ≥
   2× the best open-loop arm (paired, McNemar-registered on the
   decision statistic) → CONTINUE to the GPU closed-loop line;
   ≤ 1.2× → KILL the adaptive-pursuit premise on $0 (the loop adds
   nothing the push didn't already do).
3. *Cheapest test:* 60 items × {closed-loop 2-step, open-loop 2-step
   sum, single δ_1} displacement norms + decision-statistic flips,
   CPU, ~2h, $0. The correction rule is frozen in the pre-reg (no
   adaptive tuning of the tuner — Law #4).
4. *Mathematical license:* [THEOREM] Newton-type iteration converges
   quadratically near a root where fixed-point iteration converges
   linearly — *if* the residual map is locally smooth; the pilot is
   the test of whether that "if" holds in the residual stream.
   Frontier existence proof: Activation-LQR's tracking-error bounds
   (no training).
5. *Quantitative prediction:* closed-loop ≥ 2× open-loop
   displacement-per-norm; decision-statistic flip rate separates
   (the open-loop arms are expected at ~0 per EXP094).
6. *Breaking point:* ratio ≤ 1.2 → KILL; displacement saturates with
   the correction (EXP096/097 saturation territory) → KILL;
   Law-#14 rules it a dose tweak rather than a new channel → the
   family never launches (pre-launch kill, recorded).

*What kills it:* its own ratio — $0. *What constrains it:* EXP095's
dose-response kill and EXP097's threshold kill fence the "bigger push"
reading; the pre-reg must carry the proof that direction-adaptation ≠
dose. The GPU queue (EXP083 R1, EXP084 R2, EXP088) already holds the
relational/dynamical GPU program — this family is its $0 gate, not a
competitor.

### Family D — TTS: discriminating test-time scaling (budget-matched, pre-registered)

**Mechanism sketch.** The frontier's numbers live on this axis
(∇-Reasoner 71.2→80.4%, Meta-Reasoner +9–12% at −28–35% time,
self-consistency +17.9pp, ToT 4%→74%). The program's one attempt
(EXP056: +4pp, p=0.25, n.s.) was unpowered and unregistered. The
honest version: greedy vs best-of-N with the *frozen model's own
margin* as the verifier, N set by power analysis for a 10pp effect,
McNemar-registered, breaking point pre-registered. If the curve is
flat, the bench class is saturated and the program stops spending
thought on this axis for this task class.

1. *Exact question:* At matched generation budget, does
   margin-verified best-of-N beat greedy by a registered margin on
   the relational bench class?
2. *Decision changed:* best-of-N ≥ greedy + 10pp (paired p < 0.05) →
   CONTINUE the TTS axis (the program's first capability-positive
   $0 result); flat curve (Δ < 4pp at N=16) → KILL the axis for this
   bench class — stop proposing TTS pilots here.
3. *Cheapest test:* 60 items × {greedy + N=16 samples}, margin
   verifier = the registered cosine decision statistic (no new
   verifier trained — Law #7 clean), CPU, ~3–4h, $0.
4. *Mathematical license:* [OBSERVATION] the frontier's scaling laws
   (LLM-Monkeys log-linear coverage; self-consistency +17.9pp);
   [THEOREM] best-of-N with a calibrated verifier dominates greedy
   in expectation — the pilot tests whether our margin *is* a
   calibrated verifier.
5. *Quantitative prediction:* +8–12pp at N=16 under a working
   verifier; ~0 under a miscalibrated one (the informative outcome
   either way — it characterizes the margin, not just the method).
6. *Breaking point:* Δ < 4pp at N=16 → KILL for this bench class;
   verifier calibration check fails (margin uncorrelated with
   correctness on the greedy arm) → RUN-INVALID (the test measured
   the wrong thing — the verifier, not the scaling).

*What kills it:* its own flat curve. *What constrains it:* EXP056's
+4pp n.s. is the fence — this family must beat it by *registration*,
not by repetition; the H4/PTTSC pilot was never executed, so this is
not a resurrection, but the pre-reg must differentiate from it
(budget-matched verifier design vs planner-executor design).

---

## 4. Ranked recommendation

| Rank | Family | Cost to gate | Kill buys | Continue buys |
|---|---|---|---|---|
| **1** | **A — TGA** | ~1h CPU, $0 | Retires the whole dynamics-matched program pre-GPU (the He number was decorative) | First licensed injection direction since the static family closed; gates the GPU dynamics queue |
| 2 | B — DSF | ~1–2h CPU, $0 | Kills the "soft spot" premise (model is dynamically homogeneous) | The targeting map every closed-loop design needs; a new measured quantity either way |
| 3 | C — CLP | ~2h CPU, $0 | Kills adaptive pursuit on $0 | $0 gate for the GPU closed-loop line (CLLC/EXP086-B) |
| 4 | D — TTS | ~3–4h CPU, $0 | Kills the axis for this bench class (stops the proposals) | First capability-positive $0 result; characterizes the margin verifier |

**Why A first:** it is the cheapest (~1h), its kill rule was pre-
drafted in the 2026-09-25 sprint (ratio < 2 → stand down), it engages
the single measured-but-unfollowed lead in the program's history
(He≈0.77), and its outcome gates everything downstream — if the
dynamics have no distinguished amplified direction, Families B and C
lose their targeting premise and the program learns that the non-
normality is decorative, which is itself a publishable boundary fact.
No other family offers a $0, 1-hour, pre-registered kill of an entire
research direction.

**Why the others wait:** B's map is most valuable *after* A says the
amplifier exists (a map of a homogeneous field is a null with less
downstream use); C needs the GPU queue regardless and its Law-#4
channel-vs-dose adjudication is cleaner once A has established that
direction-classes matter; D is the frontier's game, CPU-expensive,
and EXP056-adjacent — it waits until the $0 dynamics answers are in,
because a dynamics-matched verifier would change D's design.

## 5. What the program should STOP doing (explicit)

1. **Stop instrumenting snapshots.** No new probe, bridge, logit
   readout, or trained head whose purpose is a decodability number.
   The static-snapshot paradigm is closed; its questions are
   answered.
2. **Stop sweeping injection.** No per-layer, per-strength,
   per-gating, per-dose lane. The 4.87% bound (S5-2) and the
   never-decodable PIVOT (S5-3) fence this space completely.
3. **Stop building benches for readout.** A new bench is licensed
   only if its breaking point is about *dynamics* (Family B's
   perturbation pairs) or *trajectories* (Family D's budget-
   matched scaling) — never for another fidelity/accuracy number
   on a snapshot instrument.
4. **Stop composing plan text near decision prompts** without a
   generation-construct-validity gate (defect class 8, EXP124).
   H11's planning question stays alive but unlicensed until a
   genuinely new instrument class is proposed — and "genuinely new"
   now means *dynamical or trajectory-level*, not another phrasing
   trick.
5. **Stop re-testing KILLED hypotheses.** H22 generality, H23
   identity interpretation, entity-name generation, bench-2 logit
   reuse, QK-subspace operators — dead means dead (Law #8 stands,
   Law #11 tags stand).
6. **Stop proposing without a kill.** Any future proposal whose
   dossier cannot name the $0 observation that would retire its
   whole direction is busywork, however summit-flavored its
   language. The six worth-it items are now seven: the seventh is
   *"what existing SCBI kill constrains this, and why is it not a
   resurrection."*

---

## 6. Session notes

- Summit filter applied honestly: Families A–C are mechanism-first
  (they ask how the frozen computer *moves*, not what its snapshots
  *contain*); D is capability-positive on the axis where the
  frontier's numbers actually live. None claims consciousness,
  superhuman achievement, or generality beyond its registered bars.
- The deep cut this dossier makes: **the program's 120-experiment
  negative is not "frozen models can't be steered." It is "frozen
  models can't be steered *by snapshot instruments*."** The dynamical
  system was never addressed — its amplifier never found (A), its
  sensitivity never mapped (B), its loop never closed (C), its
  trajectory never budgeted (D). That is the wall, and the four
  families are the four ways through it.
- No experiments executed in this sprint ($0 CPU, proposals only).
  Next step per family: worth-it gate → signed pre-registration →
  independent Law #14 review (launch chain). This dossier is a
  proposal record, not a license. No experiment numbers minted.
- Frontier inputs incorporated: ∇-Reasoner / Meta-Reasoner / DEER /
  LLM-Monkeys / ToT / self-consistency (D); Activation-LQR (C);
  JEV-27B discipline noted and not reused (the trained-head line is
  closed by EXP126); Astra shelving noted (oversight remains the
  field's binding constraint — a dynamics-first honesty instrument
  is a possible future family, not proposed here).
- Differentiation audit: A extends the 9-25 TGA pilot (ranked #2,
  never executed — unfollowed, not killed); B is new to the corpus;
  C is the $0 gate of the GPU-resident CLLC/EXP086-B line (narrowed,
  never tested); D differentiates from the unexecuted H4/PTTSC pilot
  (verifier design vs planner-executor design) and from EXP056 (by
  registration and power).

*Single-lane fence applies to each family's launch chain:
worth-it-gate lane → pre-registration draft → independent Law #14
review → fix-verification → CEO launch decision → execution under a
minted number. No lane may advance itself.*
