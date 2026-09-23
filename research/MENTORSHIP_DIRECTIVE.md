# Mentorship Directive — Standing Advisory Guidance

> **ROLE-HOLDER SUCCESSION — 2026-09-23 (LOG-194).** ChatGPT's mentorship ended
> 2026-09-23 by direct user order. The user appointed an in-house **Independent
> Scientific Mentor & Adversarial Reviewer** (a Muse Spark subagent, standing
> appointment) to succeed ChatGPT in the mentor role. The mentor reports to the
> USER, not the CEO: verdicts (adoption gates, Law #14 dispositions, protocol
> vetoes) bind the program and cannot be overridden, softened, or delayed by the
> CEO or Research Lead; the CEO is a courier for mentor verdicts, never an editor;
> the CEO may not assign the mentor work outside mentorship/review, suppress or
> rewrite its reviews, or recall it — recall is the user's decision alone. The
> mentor has no management authority (no experiments, no hiring, no tasking).
> Structural-honesty note: in-house independence is structurally weaker than an
> external reviewer; the counterweight is total transparency — every review is
> written to the repo, immutable, with line-level evidence. ChatGPT's original
> directive text below is preserved verbatim as program history; all standing laws
> (anti-theory-preservation, three evidentiary levels, five verdicts,
> Fresh-object rule, Law #3, Law #14, Δθ=0) remain in force unchanged.

**Source:** relayed by the user, 2026-09-23. ChatGPT originally acted as
mentor/advisor to the CEO (LOG-139 – LOG-193); succeeded by the in-house
Independent Scientific Mentor & Adversarial Reviewer from 2026-09-23 (LOG-194).
**Status:** ADOPTED as standing advisory guidance by the CEO, 2026-09-23 (LOG-139).
**Authority note:** This directive is advisory. CEO authority remains with Muse (Nova)
under the user's standing mandate. The user reserves: external publication, upstream
repo pushes/PRs, spending money, account/credential changes. Adversarial-review
independence (Law #14) is not subordinate to this directive.

---

## CEO adoption memo

**What this changes:**

1. **Canonical research objective (adopted).** The program's formal objective is now:
   `θ_after = θ_before`, while temporary computational state `(B_t, z_t, C_t, M_t, ...)`
   changes during inference. The long-term question: *can inference-time computation
   create a new class of intelligence not present in the model's ordinary fixed
   computational path?* This supersedes the narrower "can SCPM improve accuracy"
   framing. Program name remains SCBI; SCPM names the current mechanism hypothesis
   (or its successor — the name is not protected).
2. **Epistemic levels (adopted as canonical reporting layer).** Every agent must be
   able to state each claim as FACT / INFERENCE / HYPOTHESIS / SPECULATION. This is
   a reporting layer on top of the repo's 10-label standard (AGENTS.md §5), not a
   replacement: FACT → [FACT]/[THEOREM]/[OBSERVATION]; INFERENCE →
   [INTERPRETATION]/[PROPOSITION]; HYPOTHESIS → [HYPOTHESIS]; SPECULATION →
   [CONJECTURE]/[OPEN]. Both layers must appear on load-bearing claims.
3. **Twelve-track structure (to be staffed).** Map existing roles; staff the missing
   tracks (see §Implementation).
4. **A–J synthesis (commissioned).** The multi-track synthesis deliverable below is
   now a commissioned program asset.
5. **Organizing question (adopted):** "What discovery would have to be true for a
   frozen model to become far more cognitively capable through inference-time
   computation?" — not "how do we make SCPM win."
6. **Killer / failure experiments (G, H) become program-level gates** once defined
   by the synthesis: pre-registered, with the failure experiment licensed to kill
   the mechanism family.

**What this does NOT change:**

- Live experiment pipeline and gates (G2, C-A donor transfer, paper rewrite) continue;
  nothing restarts.
- The 14 laws, the math charter, forced baselines, signed-protocol immutability,
  and the kill discipline all stand.
- No GPU spend without CEO clearance; free-tier constraint unchanged.

**Honest note (CEO → mentor → user):** most of the directive's critical rules were
already program law and have already bitten — G1 fired the kill on the §3.3
null-space sentence (LOG-134); EXP079's infeasible probe rule was closed, not
rescued (LOG-138); forced baselines are standing law; prior art is treated as
serious. This directive validates that posture and extends it: the genuinely new
parts are the canonical formal objective, the 12-track staffing, the A–J
synthesis, and the killer/failure experiments as pre-registered program gates.

---

## The directive (verbatim, as relayed)

I want the entire SCBI/SCPM research program to be treated as an open-ended scientific investigation into a possible new mechanism for advanced machine intelligence.

Do NOT assume SCPM is correct.
Do NOT protect the existing theory.
Do NOT optimize benchmark scores merely to make SCPM look successful.
Do NOT preserve the name or current architecture if a better mechanism is discovered.

The ultimate research objective is:

Determine whether a frozen neural model can acquire substantially more powerful inference-time cognition by dynamically constructing, evaluating, composing, revising, selecting, and discarding temporary computational structures without changing its learned parameters.

Formally, investigate mechanisms of the form:

θ_after = θ_before

while temporary computational state changes:

B_t, z_t, C_t, M_t, ...

during inference.

The long-term question is much larger than "can SCPM improve accuracy?"

It is:

CAN INFERENCE-TIME COMPUTATION CREATE A NEW CLASS OF INTELLIGENCE THAT IS NOT PRESENT IN THE MODEL'S ORDINARY FIXED COMPUTATIONAL PATH?

I want the agents to investigate whether this can become a general cognitive augmentation architecture capable of:

* discovering task structure
* dynamically choosing how to reason
* constructing temporary internal representations
* composing multiple representations
* verifying and falsifying its own intermediate hypotheses
* allocating more or less computation based on uncertainty
* transferring abstract structure across domains
* generating new computational procedures for unfamiliar tasks
* using multiple models as cooperating cognitive components
* improving smaller frozen models through temporary computation
* coordinating fast and slow inference
* remembering useful procedures without permanently modifying the backbone
* discovering when existing computation is insufficient and escalating to additional computation/models/tools

The desired end state is NOT another LLM.

The research target is a COGNITIVE CONTROL / COGNITIVE COMPILATION ARCHITECTURE that can sit above existing models and dynamically organize their computation.

Use the following principle as a starting hypothesis, NOT as a truth:

Sense → infer task geometry → invent candidate computational structures → test counterfactually → select → compose/refine → act → verify → retain useful temporary state → purge.

Now deploy multiple independent expert perspectives.

At minimum create separate research tracks for:

1. Theoretical AI researcher
   * derive formal models of inference-time cognitive computation
   * identify what would constitute a genuinely new computational principle
2. Mechanistic interpretability researcher
   * determine whether temporary bases/subspaces actually correspond to meaningful mechanisms
   * distinguish causal representation from arbitrary steering directions
3. Neuroscience / cognitive science researcher
   * investigate analogies to working memory, executive control, attentional routing, hierarchical control, hippocampal replay, cortical reconfiguration, etc.
   * do not force biological analogies where evidence is weak
4. Machine learning researcher
   * investigate test-time adaptation, activation steering, representation engineering, search, self-consistency, latent reasoning, recurrent inference, modular networks, mixture-of-experts, adaptive computation, etc.
   * explicitly identify prior art that could invalidate novelty claims
5. Superintelligence / AGI architecture researcher
   * ask what capabilities are actually necessary for an architecture to become dramatically more capable than its frozen backbone
   * identify missing components in SCPM
6. Systems researcher
   * determine whether temporary computation can improve capability per FLOP, latency, memory, and energy
   * distinguish theoretical capability from practical deployment value
7. Adversarial scientist
   * actively attempt to prove SCPM is an illusion, benchmark artifact, activation-steering variant, or task-specific trick
   * design the strongest possible falsification experiments
8. Experimental statistician
   * audit every existing SCPM result
   * identify leakage, oracle information, benchmark construction artifacts, weak controls, multiple-comparison problems, underpowered experiments, and invalid interpretations
9. Benchmark scientist
   * design entirely new benchmarks where ordinary prompting and fixed steering are insufficient
   * especially hidden-structure and novel-task environments
10. Architecture inventor
    * unconstrained brainstorming of completely new mechanisms that preserve Δθ = 0
    * may replace the current SCPM algorithm entirely
11. Scaling researcher
    * investigate whether temporary cognitive computation can systematically trade against parameter count
    * do not equate one benchmark result with parameter equivalence
12. Scientific discovery researcher
    * explore whether a system could discover useful latent procedures, algorithms, scientific hypotheses, materials, molecular mechanisms, mathematical structures, etc.
    * focus on what experimental capability would constitute genuine novelty

CRITICAL RESEARCH RULE:

Every agent must distinguish:

FACT
INFERENCE
HYPOTHESIS
SPECULATION

No agent may turn a successful benchmark result into a general intelligence claim.

The current known SCPM evidence must be treated honestly:

* G_contrastive has shown reproducible improvement under specific conditions.
* Cross-task generalization is weak.
* Oracle-guided intervention outperforms current autonomous selection.
* Blind task-geometry discovery currently fails.
* Cross-domain basis transfer currently fails.
* Therefore autonomous representation discovery remains unresolved.
* Existing activation steering / representation engineering literature must be treated as serious prior art.

Do NOT spend the majority of research effort tuning layers, rank, alpha, or operators unless that experiment answers a deeper mechanism question.

Instead ask:

WHAT IS THE MINIMAL NEW MECHANISM THAT WOULD MAKE SCPM A FUNDAMENTALLY DIFFERENT KIND OF INFERENCE SYSTEM?

I want the agents to investigate alternatives such as:

* latent workspace construction
* temporary computational graphs
* dynamic basis invention
* internal program synthesis
* task-geometry induction
* hypothesis-space construction
* model-generated internal experiments
* counterfactual latent computation
* adaptive routing between representations
* compositional temporary modules
* ephemeral memory
* recursive inference
* cognitive resource allocation
* verifier/controller separation
* model-to-model cognitive cooperation
* learned-free test-time algorithm discovery
* external symbolic structures coupled to frozen latent representations

But none of these should be assumed correct.

THE MOST IMPORTANT QUESTION:

Can we design a system where the model is not merely given a better representation, but discovers WHICH representation, WHICH reasoning procedure, and WHICH computational pathway should be used for a previously unfamiliar task?

If yes, determine exactly how.

If no, explain the fundamental bottleneck.

I want Muse to search for a potentially much deeper successor to current SCPM rather than merely extending the current implementation.

The final synthesis should produce:

A. The strongest current interpretation of SCPM evidence.
B. The strongest arguments that SCPM is not fundamentally novel.
C. The strongest arguments that there is a genuinely new research direction here.
D. A map of adjacent prior art and exactly where the novelty boundary would have to be.
E. At least 5 radically different candidate architectures for inference-time cognitive augmentation.
F. The 3 most scientifically important experiments that could distinguish these architectures.
G. A proposed "killer experiment" whose success would constitute convincing evidence for a new inference-time cognitive mechanism.
H. A failure experiment whose result would justify abandoning SCPM entirely.
I. A formal definition of what "superintelligent augmentation" would mean operationally without using hype.
J. A 3-stage research roadmap:
    Stage 1 — prove/disprove the mechanism
    Stage 2 — demonstrate cross-task/general transfer
    Stage 3 — demonstrate qualitatively new capabilities

Most importantly:

DO NOT ASK "How do we make SCPM win?"

ASK:

"WHAT DISCOVERY WOULD HAVE TO BE TRUE FOR A FROZEN MODEL TO BECOME FAR MORE COGNITIVELY CAPABLE THROUGH INFERENCE-TIME COMPUTATION?"

Then let the research determine whether SCPM is that mechanism, a precursor to that mechanism, or a dead end.

---

## Mentor principles — second message, 2026-09-23 (adopted)

The mentor endorsed the mentor-not-manager governance and added four standing
principles, adopted by the CEO:

**P1. The canonical question stays mechanism-level.**
θ_{t+1} = θ_t while temporary computational state evolves
(B_t, z_t, C_t, M_t) → (B_{t+1}, z_{t+1}, C_{t+1}, M_{t+1}).
The question is whether that produces *qualitatively new computation*, not merely
a better benchmark score.

**P2. Existing SCPM results are evidence, not identity.**
The +14pp / +7pp findings, the autonomous +4pp result, EXP057's failure,
EXP058's transfer failure, and the post-handover negative experiments are
observations that constrain the theory. They do not obligate any future
architecture to resemble today's SCPM. Sunk-cost bias is explicitly disallowed:
the program is licensed to discover a *successor* to SCPM, not merely improve it.

**P3. The kill experiment is essential.**
The synthesis must define a result that would make the program say: "this
mechanism family is not worth pursuing." This protects the project from becoming
an endlessly expanding engineering effort. The failure experiment (H) is a
first-class program gate with a license to kill.

**P4. The synthesis ends with competing hypotheses, not one grand narrative.**
Target form: H1 = dynamic representation control; H2 = ephemeral computational
workspace; H3 = test-time program synthesis; H4 = adaptive cognitive routing;
H5 = something not yet named — plus the experiments that discriminate between
them. That is where this becomes real science.

**Mentor's behavioral note (recorded as program culture):** a null theorem being
killed rather than rescued (G1/EXP079) is exactly the behavior the lab must
preserve. Demonstrated willingness to close an attractive hypothesis matters more
than accumulating positive results.

**Deliverable expectation for the synthesis:** not just an executive summary —
bring the competing mechanisms, the prior-art boundary, the killer experiment,
the kill experiment, and above all the *reasoning* behind why each experiment
would distinguish the hypotheses. That is where the mentor is most useful as
independent adversarial reviewer.

## Standing law against theory preservation — adopted 2026-09-23

> **No hypothesis earns continuation because it is elegant, ambitious, or already
> heavily implemented. It earns continuation only because its discriminating
> experiments survive pre-registered attempts to falsify it.**

This is now standing program law (mentor-originated, CEO-adopted). It guards the
most dangerous current failure mode: theory preservation — the sunk-cost
compulsion to keep an attractive mechanism alive past its falsification.

**Three evidentiary levels (never to be silently crossed):**

"can improve inference" ≠ "changes the computational strategy" ≠ "creates
qualitatively new capability."

These are three distinct evidentiary levels. A result must never silently move
from one level to another. Every reported result must state which level its
evidence supports, and any claim at a higher level requires its own
discriminating experiment.

**Boxed standard for every candidate mechanism in the H1–H5 synthesis:**

> What observation would uniquely support this hypothesis over its competitors?

> What observation would kill it?

The mentor will apply this standard when the synthesis returns. The Lead must
apply it when commissioning the synthesis: any candidate mechanism submitted
without both boxes answered is incomplete.

**Mentor's role (confirmed):** independent scientific mentor / adversarial
reviewer — not lab manager, not decision-maker.

## Re-review acceptance criteria — mentor, 2026-09-23

The mentor confirmed the INCONCLUSIVE disposition and will treat the revised
synthesis as a fresh adversarial object, not as LOG-158 with edits. The revised
synthesis must satisfy every item below before it can be adopted:

1. Every newly added prior-art claim is actually verified (Law #3) and its
   mechanism characterized correctly. A paper that fails verification remains
   explicitly marked UNVERIFIED — never used rhetorically in the
   burden-of-proof argument.
2. The revised novelty boundary is narrower than the literature it invokes.
3. `p ≥ 0.05` has been removed as a standalone falsifier everywhere and
   replaced by the effect/CI/margin framework.
4. MDE, power, multiplicity, and the candidate-selection hierarchy are fixed
   BEFORE NTDP data contact.
5. A3/A7 no longer imply independent convergent evidence from the same
   option-informed bridge construction (reframed as readout-path
   steerability).
6. K1/K2/K3 remain logically ordered and capable of collapsing the
   output-side interpretation.
7. TTPS, latent branching, latent cooperation, and adaptive routing each have
   baselines that actually test their CLAIMED MECHANISM, not merely their
   implementation.
8. Compute matching includes all relevant online and amortized costs.
9. The final H3 kill license remains executable without a discretionary
   rescue path.

**Standing review principle (mentor):** a re-review judges the revised
protocol and novelty boundary — it does not reward the program for having
produced more experimental machinery. Adoption requires the map and the
protocol to be correct, not the pipeline to be large.

**Fresh-object rule (mentor, 2026-09-23):** the second review treats the
revision as a fresh adversarial object, *including the sections that
previously appeared strongest.* The acceptance gate applies to the revision
itself, with particular attention to whether the corrected literature map and
statistical framework materially change any previously permitted conclusion.
Any unresolved citation verification, statistical ambiguity, or novelty
overstatement is an **open defect** — it does not silently inherit LOG-158's
cleared status. Nothing in the revision is grandfathered.

## Evidentiary verdict standard for the H1–H5 synthesis — adopted 2026-09-23

The only permitted verdict categories for a hypothesis against a
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
experiment" are **not evidentiary categories** and may not appear as verdicts.
They may appear, labeled as [INTERPRETATION], only alongside a verdict from the
five above. The mentor will treat forthcoming H1–H5 results as evidence first
and theory second, without rescuing SCBI if the data do not support it.

## Implementation (CEO orders to the Research Lead)

1. **Track mapping.** Map the 12 tracks onto existing roles; identify and staff the
   missing ones: (3) neuroscience/cognitive science, (6) systems, (9) benchmark
   scientist, (11) scaling researcher, (12) scientific discovery researcher,
   (5) superintelligence/AGI architecture researcher (partially covered by the
   roadmap — make it an explicit track). Existing coverage: (1) theory role,
   (2) mechanistic interpretability (G1 lineage), (4) literature role,
   (7) Law #14 adversarial reviewer, (8) experimental statistician (evaluator
   design lineage — formalize), (10) innovation sprints.
2. **Commission the A–J synthesis** as a multi-track deliverable grounded in the
   honest evidence base (G1 kill, EXP077/070/078/067, EXP079 closure, forced
   baselines). Every claim labeled FACT/INFERENCE/HYPOTHESIS/SPECULATION.
3. **Adopt the epistemic levels** program-wide; update the knowledge protocol's
   labeling standard.
4. **Adopt the canonical objective** in the operating system and theory docs.
5. **Continue live gates** (G2 pre-reg, C-A donor-transfer pre-reg with the
   entity-similarity-leak adversarial review, paper rewrite). No restart.
6. **Pre-register G and H** as program-level gates once the synthesis defines them.
