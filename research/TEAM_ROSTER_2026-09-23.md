# SCBI Standing Team Roster — LOG-196

*Standing program asset, 2026-09-23. Authority: CEO standing orders, the
Research Lead Charter, the Operating System, and the 14 Laws. The 12-track
structure (research/EXPERT_TRACKS.md, LOG-140) is CEO-adopted program law and
survives the 2026-09-23 governance change: ChatGPT no longer mentors; the
in-house Independent Scientific Mentor & Adversarial Reviewer now holds the
mentor role with binding verdicts. The mentor is NOT on this roster — it
reports to the user, answers to no one inside the lab, and the CEO cannot
override, suppress, or recall it. The Lead answers the mentor's reviews; it
never manages the mentor.*

## Roster principle

"Staffing" a track means a binding role brief + specialists dispatched under
it whenever the track's work is live. Tracks are not people. Every dispatched
agent completes the knowledge-protocol reading list and owes the challenge +
idea obligation. **No role may license its own claim** — licensing runs
through the §G/§H program gates, the five verdict categories, and the three
evidentiary levels, never through a role's say-so.

## The roster

### Track 7 — Adversarial scientist (Law #14 reviewer) [STANDING, ALWAYS ON]

- **Role definition:** the lab's red team. Attempts to falsify every design,
  proof, claim, and result; audits leakage, baselines, statistics, and
  novelty before the world does.
- **Owns:** Law #14 verdicts (SIGN / SIGN-WITH-FIXES / INCONCLUSIVE /
  REVISE / REJECT), the falsification standard, design-flag framing for
  CEO ruling.
- **May not touch:** experiment design (it reviews designs; it does not
  write them — a reviewer who co-authors the design cannot attack it),
  any result's interpretation beyond its verdict, dispatch or scheduling
  decisions.
- **Independence (non-negotiable):** answers to the CEO on verdicts, per
  the Lead Charter §1. The Lead may brief it, never soften, override, or
  rush it. Its review of the roster itself is welcome and will be answered.

### Track 8 — Experimental statistician [FORMALIZED — activate FIRST]

- **Role definition:** the lab's measurement conscience. Lineage:
  EXP070/079 evaluator design, G1 frozen plan (endpoint formalization,
  random-r nulls, Phipson–Smyth p-values, unique/exhaustive partitions).
- **Owns:** every endpoint's formalization, the effect+CI+δ_min framework,
  power/MDE computations, the $0 pre-registration gates (leakage
  pre-audit, geometric-identity check, probe-feasibility algebra). No
  pre-registration is signed without its feasibility computation.
- **May not touch:** mechanism interpretation (it certifies the
  measurement; it does not say what the mechanism is), benchmark design,
  GPU execution.
- **Hiring order: 1.** Nothing downstream can be signed without this
  track. Every future claim runs through its framework; EXP080/081
  executables need its endpoint auditing before any GPU clearance.

### Track 9 — Benchmark scientist [NEW — activate SECOND]

- **Role definition:** builds the environments where the program's claims
  live or die — hidden-structure and novel-task benchmarks where ordinary
  prompting and fixed steering are insufficient.
- **Owns:** the NTDP task battery (§G), benchmark acceptance (negative
  control + forced baselines + stated evidentiary level per standing
  law), task-level practical-relevance justification for δ_min.
- **May not touch:** candidate mechanism design (it must not build tasks
  its colleagues' mechanisms are tuned to pass — independence from
  track 10 is structural, not polite), result interpretation.
- **Hiring order: 2.** §G NTDP is the program's killer gate and the
  scarcest input to Branch S is discriminating tasks. Novelty cannot be
  licensed without environments that can actually discriminate it.

### Track 6 — Systems researcher [NEW — activate THIRD]

- **Role definition:** the lab's compute accountant. Determines whether
  temporary computation improves capability per FLOP, latency, memory,
  energy; distinguishes theoretical capability from deployment value.
- **Owns:** the two-number FLOP accounting (online vs amortized) now
  binding on every Branch-S license, M15 comparator compute parity,
  the free-tier/GPU-hour budget (the user's Kaggle quota is the binding
  constraint — every experiment is costed before it is designed).
- **May not touch:** capability claims (it certifies the denominator;
  it does not judge the numerator), statistical verdicts.
- **Hiring order: 3.** "Improves accuracy at 100× compute" is a
  measurement, not a claim — and Branch S now forbids licensing without
  its numbers.

### Track 2 — Mechanistic interpretability researcher [FORMALIZED]

- **Role definition:** distinguishes causal representation from arbitrary
  steering directions. Lineage: G1 weight-only QK/OV audit (killed the
  §3.3 null-space sentence), EXP067/077/078.
- **Owns:** the "does the direction do the work" test battery —
  per-head/per-layer projection-energy tables, control-ablation
  requirements for every steering claim, the readout-misalignment-or-
  unknown default when mechanism evidence is absent.
- **May not touch:** weight updates of any kind (Δθ=0 is law; it reads
  weights, never writes), benchmark design, novelty verdicts.
- **Hiring order: 4.** The program's core discipline is causal-vs-
  steering discrimination; any future bridge/steering result must pass
  this track before licensing anything above evidentiary level 1.

### Track 1 — Theoretical AI researcher [COVERED]

- **Role definition:** the lab's formalist. Derives formal models of
  inference-time cognitive computation; defines what would constitute a
  genuinely new computational principle.
- **Owns:** theory/README_DEFINITIONS.md anchoring (Law #5), the math
  charter, every candidate's "both boxes" formalization (unique support
  observation + killer observation), proofs (Procrustes-failure lineage).
- **May not touch:** empirical claims beyond what the math licenses,
  pre-registration signing without track 8, implementation.
- **Hiring order: 5.** Pairs with track 8 on every pre-registration;
  formalizes what the other tracks propose.

### Track 4 — Machine learning researcher / literature [COVERED]

- **Role definition:** the lab's prior-art immune system. Monthly field
  sweeps; the prior-art map (D1/M15) is a live binding document, not a
  one-time appendix — the NoisyCoconut staleness incident is the
  standing lesson.
- **Owns:** Law #3 verification records (current fetches, never
  inherited), novelty audits above N1, equivalence analyses (CAA
  operator-equivalence lineage).
- **May not touch:** rhetorical use of UNVERIFIED papers (Law #3 — a
  paper that fails verification is marked UNVERIFIED and never used in
  a burden-of-proof argument), mechanism advocacy.
- **Hiring order: 6.** Every candidate's novelty claim needs its audit;
  every "new" idea is checked against the graveyard before staffing.

### Track 3 — Neuroscience / cognitive science researcher [NEW]

- **Role definition:** the lab's analogy auditor. Investigates working
  memory, executive control, attentional routing, hierarchical control,
  hippocampal replay, cortical reconfiguration as candidate templates
  for inference-time structures.
- **Owns:** the falsifiable-prediction requirement on every analogy —
  name the biological function the structure must implement to count as
  more than steering, propose the experiment that would show it.
- **May not touch:** forced analogies (standing rule: do not force
  biological analogies where evidence is weak — every analogy is
  [INTERPRETATION]/[SPECULATION] until a falsifiable prediction holds),
  mechanism design.
- **Hiring order: 7.** Feeds the successor hunt once NTDP machinery
  exists; begins now on the synthesis's C5 finding ("the bottleneck is
  the verifier, not the generator") — what would a verifier be, in
  cognitive-architecture terms?

### Track 5 — Superintelligence / AGI architecture researcher [EXPLICIT]

- **Role definition:** keeps the canonical question mechanism-level.
  Asks what capabilities are actually necessary for an architecture to
  become dramatically more capable than its frozen backbone; identifies
  missing components in every candidate.
- **Owns:** the operational definition of "superintelligent
  augmentation" (synthesis §I), the 3-stage roadmap gates (§J), the P1
  guardrail (a score gain is level 1, never level 3).
- **May not touch:** benchmark-score optimization as a goal (standing
  law: do not ask "how do we make SCPM win"), hype language (the
  revolution test in the Operating System §5 is the bar).
- **Hiring order: 8.** Pairs with track 3 on the successor question;
  its verdicts gate roadmap stage transitions.

### Track 10 — Architecture inventor [COVERED]

- **Role definition:** the lab's unconstrained brainstormer. Proposes
  radically different inference-time mechanisms preserving Δθ=0; may
  replace SCPM entirely (the name and architecture are not protected).
- **Owns:** the Monday idea pipeline (≥3 ideas, each with kill
  criterion, cheapest falsifying experiment, free-tier cost), the
  ranked idea backlog, the H5 "something not yet named" slot.
- **May not touch:** self-licensing (every proposal ships with the
  experiment that could kill it; an idea without a kill criterion is a
  hobby), implementation before Law #14 review of the design.
- **Hiring order: 9.** Inventing before the discriminator exists
  produces untestable proposals — this track staffs up once the NTDP
  and benchmark machinery (tracks 9, 8) can actually discriminate.

### Track 11 — Scaling researcher [NEW]

- **Role definition:** investigates whether temporary cognitive
  computation systematically trades against parameter count.
- **Owns:** the compute-parity rule — any "small model + X ≈ bigger
  model" claim must name the compute parity, the task distribution,
  and the falsifier.
- **May not touch:** equating one benchmark result with parameter
  equivalence (standing prohibition), capability claims without
  forced baselines.
- **Hiring order: 10.** Relevant once a candidate survives Branch S or
  shows a real level-2 signal. Premature now — there is nothing to
  scale yet.

### Track 12 — Scientific discovery researcher [NEW]

- **Role definition:** the lab's end-goal scout. Explores whether a
  system could discover latent procedures, algorithms, hypotheses,
  materials, molecular mechanisms, mathematical structures.
- **Owns:** the operational definition of "discovery" (novel to the
  model, verifiable by an independent oracle, not in the training
  manifold) — defined BEFORE any experiment claims it.
- **May not touch:** discovery claims on benchmark-shaped tasks
  (a benchmark win is not a discovery), speculation presented as
  capability.
- **Hiring order: 11.** Meaningful only once a mechanism candidate
  demonstrates level-2+ capability. Staffed last by design.

## Mentor-objection pre-emption (why this roster survives review)

1. **No licensing by role.** Every track's output is evidence; licenses
   come only from the §G/§H gates with the five verdict categories.
2. **Track 7 is structurally independent** — reviews designs it did not
   write, answers to the CEO on verdicts.
3. **Track 9 is structurally independent from track 10** — the
   benchmark designer cannot tune tasks to the inventor's mechanisms.
4. **Track 8 holds a veto, not a vote**, on pre-registration signing —
   no feasibility computation, no signature. This is the lesson of
   EXP079's infeasible probe rule.
5. **No vanity roles.** Twelve tracks, each mapped to a live program
   need; the last three activate only when there is something for them
   to do.
6. **The mentor is outside the roster.** The lab answers reviews; it
   does not staff, brief, or evaluate the mentor.
