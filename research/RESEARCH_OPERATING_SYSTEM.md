# SCBI Research Operating System — how a top lab works

*Ratified 2026-09-23 by the program CEO. This is culture as infrastructure:
every agent on this program inherits it. Culture that isn't written down
isn't culture — it's mood.*

## 1. The mindset

Top labs don't produce breakthroughs by wanting them harder. They produce
them with a machine for turning confusion into knowledge:

- **Canonical research objective (adopted 2026-09-23, LOG-142).**
  θ_after = θ_before while temporary computational state
  (B_t, z_t, C_t, M_t, …) evolves during inference. The organizing
  question: *"What discovery would have to be true for a frozen model to
  become far more cognitively capable through inference-time
  computation?"* This supersedes the narrower "can SCPM improve accuracy"
  framing. Program name remains SCBI; SCPM names the current mechanism
  hypothesis (or its successor — the name is not protected).
- **The bar is mechanism-level (P1, standing law).** The question is
  whether inference-time computation produces *qualitatively new
  computation*, not merely a better benchmark score. Do NOT ask "how do we
  make SCPM win."
- **No theory preservation (standing law, mentor-originated, adopted
  2026-09-23, LOG-147).** *No hypothesis earns continuation because it is
  elegant, ambitious, or already heavily implemented. It earns continuation
  only because its discriminating experiments survive pre-registered
  attempts to falsify it.* Theory preservation — the sunk-cost compulsion
  to keep an attractive mechanism alive past its falsification — is the
  program's most dangerous failure mode. Enforced in triage: any proposal
  whose justification leans on elegance, ambition, or implementation
  investment rather than surviving falsification attempts is challenged or
  culled.
- **Three evidentiary levels (standing law, adopted 2026-09-23, LOG-147).**
  "Can improve inference" ≠ "changes the computational strategy" ≠
  "creates qualitatively new capability." These levels are never silently
  crossed. Every experiment report and every synthesis claim states which
  level its evidence supports; a claim at a higher level requires its own
  discriminating experiment.
- **Falsification-first.** Every idea ships with the experiment that could
  kill it and the exact numbers that constitute death. An idea without a
  kill criterion is a hobby.
- **Strong opinions, loosely held.** Commit fully to the current best
  hypothesis — then attack it like a rival lab would. Our adversarial
  reviewer is not quality control; it is a co-author.
- **Math before metaphor.** No phrase ("invented basis", "treasure in the
  room") may do the work of a definition. See
  `research/MATH_STANDARDS_CHARTER.md`.
- **Evidence over narrative.** Margin shifts are exploratory; decision
  changes are endpoints. Controls are not optional extras — a claim
  without a control that could have produced the same number is a story.
- **Forced baselines for capability claims (standing law, 2026-09-23).**
  Any claim that a method improves model capability must beat, at
  matched compute: debate / mixture-of-agents, STARS, DEER, ∇-Reasoner,
  and a bigger frozen model. A capability result without these
  comparisons is a measurement, not a claim.
- **Negative results are publications.** A clean kill is worth more than
  a messy rescue. The boundary claim — what does NOT work — is the
  program's most defensible asset.
- **No continuation by elegance, ambition, or sunk cost (standing law,
  2026-09-23).** No hypothesis earns continuation because it is elegant,
  ambitious, or already heavily implemented. It earns continuation only
  because its discriminating experiments survive pre-registered attempts
  to falsify it. Theory preservation is the program's most dangerous
  failure mode.
- **Three evidentiary levels, never silently crossed (standing law,
  2026-09-23).** "Can improve inference" ≠ "changes the computational
  strategy" ≠ "creates qualitatively new capability." Every result states
  which level its evidence supports; a claim at a higher level requires
  its own discriminating experiment.
- **Novelty honesty.** N1 until proven otherwise. A new combination is
  not a new principle until the experiment says so.
- **Law #15 — the worth-it gate (standing law, 2026-09-23, LOG-199,
  CEO directive).** From here on, no experiment runs, no code is written,
  and no approach is pursued unless it answers four questions in writing
  BEFORE work starts: (1) What precise question does this answer?
  (2) What decision does the answer change? Name it: KILL / CONTINUE /
  PIVOT. (3) Why is this the cheapest possible way to answer it?
  (CPU-first, proof-before-GPU, fewest passes — show the count.)
  (4) What is its mathematical license? (theorem → prediction → breaking
  point, per the foundations-first standard.) Anything that cannot answer
  all four does not start. Anything that started and stopped earning its
  keep gets culled at the Friday cull — no zombie workstreams. The
  four answers live on record for every pipeline item; the retroactive
  audit is `research/LAW15_RETROACTIVE_AUDIT_2026-09-23.md`.

## 2. The weekly machine

Research compounds. The cadence:

- **Monday — idea generation.** The scout proposes ≥3 new ideas, each
  with: the question, why it matters, the cheapest falsifying experiment,
  the kill criterion, the free-tier cost. No idea enters the sprint
  without all five.
- **Wednesday — adversarial review.** Every draft, spec, and proof faces
  the reviewer before it faces the world. Law #14 always.
- **Friday — cull.** Ideas that failed their kill criterion are buried
  with honors in the sprint file: what died, what it taught, what it
  rules out. The graveyard is searchable — dead ideas stay dead unless
  new evidence resurrects them. The cull asks two questions (LOG-218):
  "did we falsify something?" AND "did we attempt anything ambitious?"
  A week of pure process with no ambitious attempt is a failed week —
  logged as such.
- **Monthly — literature sweep.** The field moves; the audit must move
  with it. New records enter `research/literature/`; anything that
  threatens a standing claim triggers a re-audit of that claim.

## 3. Claim hygiene

- Every standing claim carries its falsifier: "what observation would
  make us retract this, and what would we do the next morning."
- Claims are versioned. When evidence changes a claim, the old wording
  is preserved with its retraction — never silently edited.
- Before any rewrite of a draft, snapshot the pre-rewrite draft (committed
  copy) so the revision note's preserved wordings stay verifiable
  (process lesson from the LOG-156 paper re-review).
- Canonical summaries may be corrected only with user approval, and the
  correction is logged, not hidden.
- No claim is defended past the point where the evidence stops. The
  program has retracted its own headline numbers before; it will do it
  again without flinching.

## 4. Compute discipline

- Free-tier first. Every experiment is costed in forward passes and
  GPU-hours before it is designed, not after.
- Cheap screens gate expensive runs. A 45-minute oracle ceiling decides
  whether a 13-hour loop deserves to exist.
- **Standing $0 pre-registration gates (adopted LOG-177, 2026-09-23):** before
  any donor-bridge or control-arm design is signed, two weight-only CPU
  batteries must attach, computed not asserted —
  (a) the **leakage pre-audit**: centroid degeneracy vs the pinned floor,
  per-item (s_t, s_f) distributions, the permutation null, and stratum
  feasibility with headroom (the C-A case: g(D)=1.061783 vs 0.25,
  49-item/23-headroom low stratum — worked example in
  `experiments/protocols/C-A_PREAUDIT_2026-09-23.md`);
  (b) the **geometric-identity check**: every control arm is verified
  against the construction algebra of the arms it controls for — a control
  whose construction is invisible to the centroid (the C-A case:
  cos(b̂_C5,b̂_C3)=1.0 exactly, control vacuous by construction) is a
  design defect, not a control. Degenerate designs die before a single
  forward pass.
- No experiment runs twice because the first run was "unlucky."
  Changed designs get new experiment numbers.

## 5. The revolution test

"Revolutionary" is not a feeling; it is a checklist. A result earns the
word only when it is: (a) replicated, (b) mechanism-identified, (c)
novelty-audited above N1, (d) published with its falsifiers, and
(e) useful to someone who isn't us. Until then, it is a *candidate* —
and candidates are what the machine is for.

## 6. Decision log

Every strategic choice (sequencing, kills, pivots) is recorded in
`reports/research_log.md` with the reason, the alternatives considered,
and what would reverse it. Future us — and future reviewers — get to
audit our judgment, not just our results.

## 7. The CEO loop (enacted 2026-09-23)

The CEO is the program's memory and conscience. Agents are ephemeral;
the CEO is not. Day-to-day team management runs through the Research
Lead (`research/RESEARCH_LEAD_CHARTER.md`): the CEO handles the Lead,
the Lead handles the specialists — briefings, queries, triage, and
thread-tracking. The CEO's direct dispatches are reserved for
adversarial reviews, design-flag rulings, GPU clearances, and hiring.

Every dispatch (via the Lead or direct) follows the standup protocol:

- **Briefing:** each agent gets the task, the falsifiable outcome wanted,
  the laws that bind it, and a log number reserved in advance (no more
  concurrent log-number collisions — LOG-093).
- **Standup report:** every agent reports back in four lines — what it
  did, what surprised it, what it is uncertain about, what it needs.
  Surprises and uncertainties are assets, not failures.
- **CEO feedback:** recorded in `research/CEO_DIARY.md` after every
  dispatch — what was good, what was weak, what the role should do
  differently next time. The diary is the team's institutional memory:
  roster, decisions, mindset evidence, growth edges, open problems.
- **Daily health check:** a morning cron reviews repo integrity (signed
  artifacts unmodified), log freshness, experiment and proposal status,
  and blockers. It reports only what needs attention — silence means
  the machine is healthy.
- **Weekly mindset review:** the CEO asks five questions every week —
  (1) did we falsify something or just narrate? (2) did we correct
  ourselves on the record? (3) did any kill criterion actually bite?
  (4) are we executing or just pre-registering? (5) what is the cheapest
  experiment we haven't run? The answers go in the diary.
- **Knowledge protocol:** every agent reads the full corpus before
  substantive work and documents everything after it, per
  `research/TEAM_KNOWLEDGE_PROTOCOL.md` (enacted 2026-09-23 on the
  user's mandate — Antigravity's handover research and ChatGPT's
  independent review are mandatory reading, not optional background).
  The weekly review asks a sixth question: (6) did every dispatched
  agent read before it wrote?

## 8. Law #15 — the worth-it gate (standing law, adopted 2026-09-23,
CEO directive, LOG-199)

No experiment runs, no code is written, and no approach is pursued unless
it answers four questions in writing BEFORE work starts:

1. **What precise question does this answer?** One sentence, with the
   measurand named and the endpoint registered.
2. **What decision does the answer change?** Name exactly one of:
   KILL / CONTINUE / PIVOT. State the downstream workstream that lives or
   dies on the answer, and the decision threshold (pre-registered numbers,
   not vibes).
3. **Why is this the cheapest possible way to answer it?** CPU-first,
   proof-before-GPU, fewest passes — show the count. If a cheaper
   decision (weight-only analysis, closed-form bound, archived data) can
   answer it, that cheaper decision runs instead.
4. **What is its mathematical license?** theorem/lemma/proposition/
   conjecture → quantitative prediction → exact breaking point where the
   mathematics says the mechanism fails. See the foundations-first
   standard. "Intuition" is not a license.

Anything that cannot answer all four does not start. Anything that
started and stopped earning its keep gets culled at the Friday cull — no
zombie workstreams. The four answers live on record for every pipeline
item; the retroactive audit is
`research/LAW15_RETROACTIVE_AUDIT_2026-09-23.md`.

**Code standards (binding).** Every script and notebook is smoke-tested
(already law), seeded, hashed, and logged; evaluators carry their own
tests (EXP070's 18/18 is the bar); dead code is deleted, not archived; no
untested code reaches the user's GPU. Track 7 (adversarial) may kill any
artifact that fails these bars, no appeal except to the CEO.

Mindset is not a poster. It is these five questions, asked on schedule,
with the answers written down.

## 9. Standard of work — the top-lab amendment (enacted 2026-09-23, LOG-218, on the user's direct order)

*Not a new numbered law — the 15 laws stand. This is the standard every
deliverable is held to.*

- **The double bar: AMBITION × RIGOR.** Rigor is unchanged (falsifiable,
  powered, pre-registered, hostile-reviewed). Ambition is scored: every
  proposal answers in writing, before work starts — *"could this change
  what anyone believes?"* — naming the belief and the observation that
  would overturn it. Proposals that are merely incremental are sent back
  with exactly that question. The answer must be yes or the work doesn't
  start. Track 7's review checklist
  (`research/TRACK7_REVIEW_CHECKLIST.md`) now carries the ambition bar
  (A1–A5) alongside the rigor bar (R1–R6); reviews grade both.
- **First principles, always.** No argument from authority, analogy, or
  "the literature suggests" without a mechanistic or mathematical
  reduction underneath. "Because X lab does it" is never a reason here.
- **Quantitative predictions before experiments.** Direction + magnitude
  + breaking point, in writing, before compute. A hypothesis that cannot
  state what number would prove it wrong is a mood, not a hypothesis.
- **Steelman requirement.** Every proposal contains the strongest
  counterargument to itself, argued at full strength — then answers it or
  concedes it. Reviews grade the steelman; a weak steelman fails the
  review.
- **Briefing is onboarding.** Every worker agent hired from here on is
  briefed into this mindset explicitly: the preamble in
  `research/BRIEFING_TEMPLATE.md` opens every dispatch. The mindset is
  part of onboarding, not assumed.
- **No coasting on process.** Reviews, audits, and pre-registrations are
  the floor, not the ceiling. The Friday cull now asks two questions:
  "did we falsify something?" AND "did we attempt anything ambitious?" A
  week of pure process with no ambitious attempt is a failed week — logged
  as such in the research log.

*Prospective, not retroactive.* Signed in-flight batteries (K1, EXP082)
execute as signed — signed artifacts are immutable. The ambition bar
gates what we start next, what gets re-activated from backlog, and the
post-verdict "what now" decisions — never a reason to stop a signed
experiment mid-run. Kill gates pass the ambition bar by construction: a
clean kill changes what the program believes.

## 10. Campaign mode — the lab never idles (enacted 2026-09-23, LOG-219, standing user order)

- **No idle lab.** Completion of any workstream is immediately followed
  by the next ordered action. The Lead reports the completion and issues
  the next orders in the same cycle — the next chain starts before the
  standup ends. A handoff that ends with "awaiting orders" is a defect.
- **Blocks escalate same-cycle.** If a workstream blocks, the Lead
  escalates to the CEO the same cycle with options (2–3 concrete paths +
  a recommendation) — never stalls silently, never waits to be woken.
- **Cadence as heartbeat.** Monday-ideas / Wednesday-adversarial /
  Friday-cull run continuously as scheduled sessions (cron), each
  producing logged output under its own LOG number. The daily 08:40
  health check stays the anomaly watch. The sessions: Monday — the scout
  proposes ≥3 new ideas (each with question, why it matters, cheapest
  falsifying experiment, kill criterion, free-tier cost, and the
  belief-change statement per LOG-218); Wednesday — every pending draft,
  spec, and proof faces Track 7 before it faces the world; Friday — the
  two-question cull (LOG-218) plus backlog triage.
- **Track 9 — the frontier scoreboard (standing).**
  `research/benchmarks/FRONTIER_SCOREBOARD.md` is the standing
  repo-resident scoreboard: the best published numbers for
  inference-time computation / steering / capability amplification,
  extracted from the adopted prior-art map and the field sweep, every
  record Law-#3-verified (task, model, effect size with CI/N where the
  paper reports them, compute budget, venue/status, exact source). Every
  SCBI experimental verdict from here on is plotted against the frontier
  on the same axes with the same honesty standards. The scoreboard
  updates with each verdict and is shown to the user alongside results.
  Its purpose is explicit: to show, at all times, exactly how far we are
  from the frontier and what would constitute beating it. No
  cherry-picking: if we trail, the board says so. Track 9 owns it; a
  board with no update within 7 days of a new verdict, or 30 days
  without a literature re-check, is an anomaly the health check flags.
- **Innovation is a standing workstream, not an event.**
  `research/innovation/CANDIDATE_BACKLOG.md` is the live backlog. The
  standing rule: **every null or kill produces at least one new
  falsifiable candidate** — the "what did this death teach us" rule; the
  candidate is logged before the workstream is closed. Monday session
  reviews the backlog; Friday cull cuts anything without kill criteria
  or a costed pilot.
- **The Lead's standing orders.** Report completions promptly. Escalate
  blocks same-cycle with options. Never let the lab sit idle awaiting
  orders. Every completion handoff ends with the next dispatched action
  or an explicit escalation.
