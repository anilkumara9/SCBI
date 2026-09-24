# MATHEMATICAL LICENSE STANDARD — Foundations-First Protocol Gate

**LOG-200 · Theory Track (Track 1) · 2026-09-23 · CPU/$0, docs only, no code, no GPU**

**Status:** Binding standard on CEO ratification. This document is the "foundations-first
standard" referenced by Law #15 Q4 (`research/RESEARCH_OPERATING_SYSTEM.md` §8).

**Authority:** Law #15 (the worth-it gate); `research/MATH_STANDARDS_CHARTER.md` M8
(falsification checklist for mathematical claims); `AGENTS.md` Laws #2 (never invent results),
#3 (never fabricate citations), #5 (anchored definitions), #11 (observation/interpretation
separation), #14 (challenge rather than defend).

**Labeling:** every load-bearing claim below carries an epistemic label per `AGENTS.md` §5
(`[FACT]`/`[THEOREM]`/`[PROPOSITION]`/`[CONJECTURE]`/`[HYPOTHESIS]`/`[ASSUMPTION]`/
`[DEFINITION]`/`[OBSERVATION]`/`[INTERPRETATION]`/`[OPEN]`) and, where the claim crosses the
fact/inference line, the FACT/INFERENCE/HYPOTHESIS/SPECULATION layer. External citations used
here were verified by live fetch on 2026-09-23 (arXiv identifiers confirmed); any citation not
so verified is tagged `UNVERIFIED`.

---

## Law #15 answers for this dispatch (binding, on record)

- **Q1 — What precise question does this answer?** Two deliverables: (A) a binding
  "Mathematical License" section template that every future experiment protocol must carry
  (theorem/lemma/proposition/conjecture → quantitative prediction → exact breaking point),
  with a worked example from the LOG-197 Law #7 bridge audit and a transition rule for
  queued protocols; (B) the opening memo for the theory track's standing question —
  *"Under Δθ=0, what is provably possible for inference-time computation to add?"*
- **Q2 — What decision does the answer change?** **CONTINUE** — this standard, once ratified,
  unblocks the foundations-first licensing regime for all future protocols. No protocol
  advances to Law #14 review without a license section graded at or above
  CONJECTURE-UNDER-TEST; INTUITION-graded designs do not start.
- **Q3 — Why is this the cheapest possible way to answer it?** CPU/$0 pure theory. One
  document, one agent, no code, no GPU, no credentials, no forward passes. There is no
  cheaper decision procedure than writing the standard before the protocols that must obey it.
- **Q4 — What is its mathematical license?** This dispatch *is* the Q4 instrument: Part A
  defines the license regime itself; Part B surveys the theorems that currently license (or
  fail to license) the standing question. The license for writing a standard is definitional
  work, not empirical — its breaking point is named in §A.7.

---

# PART A — The Mathematical License Protocol Section (binding template)

## A.1 Why this exists

[INFERENCE] The program's most expensive failure mode to date (the retracted
Δcos ≈ +0.13 → +0.79 claim, 2026-09-23) was mathematical, not experimental: an operator was
fit in one space and applied in another with no transfer assumption stated. The standing law
against theory preservation (no hypothesis continues on elegance, ambition, or sunk cost)
needs a positive instrument, not just a prohibition. The Mathematical License is that
instrument: **no design draws on mathematics it cannot name, quantify, and break.**

[DEFINITION] A *mathematical license* is a signed, reviewable statement in an experiment
protocol that names the exact mathematical result authorizing the design, states the
result's quantitative prediction for the protocol's primary endpoint, and names the exact
observation at which the mathematics says the mechanism breaks.

## A.2 The four required fields

Every protocol's license section carries exactly these fields, in this order:

1. **Authorizing result.** The theorem, lemma, proposition, or conjecture the design rests
   on — stated *exactly* (full statement, all quantifiers, all premises), with its source:
   proven in-house (cite the proof document and its adversarial-review record),
   cited (cite the paper with verified identifier — Law #3), or labeled `CONJECTURE`
   (the experiment is then explicitly the conjecture's falsification attempt).
   Per Math Charter M2.4, conditional results name their condition in every citation.
2. **Quantitative prediction.** What the result predicts for the protocol's *primary
   endpoint* — numbers, tolerances, coverage ("for all N items", "with probability ≥ …"),
   not adjectives. A prediction without a number is not a prediction; it is a hope with
   LaTeX.
3. **Breaking point.** The exact point where the mathematics says the mechanism should
   break: the falsifying observation, named in advance, with the decision it triggers
   (KILL / CONTINUE / PIVOT per Law #15 Q2). Must satisfy Math Charter M8 Q1 ("what would
   prove it false?") and M5.2 (the breaking point must partition the outcome space — no
   outcome lands in "we'll decide later").
4. **Assumption inventory.** Every undischarged assumption the result carries, labeled per
   Math Charter M2.2, with a discharge plan (proof, measurement, or adversarial review).
   If the list is empty, say so and say why. An assumption discovered later demotes the
   license grade automatically (Charter M2.3).

## A.3 License-grade rubric

| Grade | Meaning | What it authorizes |
|---|---|---|
| **PROVEN-LEMMA** | In-house lemma/proposition with complete proof; all assumptions discharged; proof survived adversarial review that attacked each step (Charter M2.2). | May authorize a full-budget run. |
| **CITED-THEOREM** | Published result, Law-#3-verified (fetched, read, version pinned; applicability conditions checked against the protocol's setting — the M4 space/shape/rank/unit checks apply to *imported* theorems too). | May authorize a full-budget run, conditional on the applicability check being on record. |
| **IN-HOUSE-PROOF** | Proven in-house, proof complete, but not yet through adversarial review. Provisional. | May authorize a pilot or scale-gated run only. Full run requires promotion via Law #14 review of the proof. |
| **CONJECTURE-UNDER-TEST** | No proof; the protocol *is* the falsification attempt. The conjecture is stated exactly, the kill observation is pre-registered, and Law #15 Q3 (cheapest falsifying experiment) gates the budget. | May authorize the cheapest discriminating experiment only. |
| **INTUITION** | Metaphor, elegance, "it feels like the model should…", appeal to ambition or prior investment. | **Disqualifying. The protocol does not start.** Returned for rewrite. Per Charter M7, metaphor may motivate but never licenses. |

**Grade discipline:**
- The grade is assigned by the protocol author and *verified* by the Law #14 reviewer, who
  applies Charter M1–M8 to the license section. A finding cites the rubric, e.g.:
  "A.3-grade violation: license claimed as PROVEN-LEMMA with no adversarial-review record —
  demoted to IN-HOUSE-PROOF; full-budget run not authorized."
- Upgrading a grade mid-protocol is a new license, not an edit: it is appended, dated, and
  re-reviewed. Downgrades are automatic on discovery of an undischarged assumption
  (Charter M2.3) and are logged in `reports/research_log.md`.
- A protocol may carry *multiple* licenses (one per design element); the *weakest* grade
  among load-bearing licenses sets the authorization ceiling for the run.

## A.4 The template (copy verbatim into protocols)

```markdown
## Mathematical License (binding — Law #15 Q4; see research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md)

**License grade:** [PROVEN-LEMMA / CITED-THEOREM / IN-HOUSE-PROOF / CONJECTURE-UNDER-TEST]
(INTUITION is disqualifying — a protocol citing it does not start.)

### L1. Authorizing result
- **Statement (exact):** [full statement with all quantifiers and premises]
- **Source:** [in-house proof document + adversarial-review record | verified citation
  (identifier, version, retrieval date) + applicability check | CONJECTURE (this protocol
  is its falsification attempt)]
- **Epistemic label:** [THEOREM / PROPOSITION / CONJECTURE per Charter M2]

### L2. Quantitative prediction for the primary endpoint
- **Endpoint:** [the protocol's registered primary endpoint, verbatim]
- **Prediction:** [numbers: value or bound, tolerance, coverage — e.g. "|cos| ≥ 1−ε for
  all 60 items, ε = 1e-6 [ARBITRARY — rationale stated]"]
- **Derivation:** [one line: how the prediction follows from L1 — the algebra, or "see
  proof document §N"]

### L3. Breaking point
- **Falsifying observation:** [the exact measurement that kills the licensed claim]
- **Decision on break:** [KILL / CONTINUE / PIVOT — and which downstream workstream it moves]
- **Outcome partition:** [confirmation that every cell of the endpoint's outcome space
  lands in exactly one branch — Charter M5.2]

### L4. Assumption inventory
- [A1 … : assumption, justification, discharge plan] — or "none; [why the list is empty]"
- **Promotion path (if grade < PROVEN-LEMMA):** [what review/measurement promotes it]

**Signed:** [author] · [date] · **Law #14 review:** [reviewer, verdict, date]
```

## A.5 Worked example — the LOG-197 Law #7 bridge audit

[FACT] This example is drawn from the signed audit plan
(`research/analysis_plans/LAW7_BRIDGE_AUDIT_PLAN_LOG197_2026-09-23.md`, Law #14 SIGN).
It licenses an *audit*, not a capability claim — the license must match the question asked.

### L1. Authorizing result

- **Statement (exact):** For each evaluated item in each of the four runs
  (EXP065/066/070/077), the per-item bridge vector constructed by the executed code path
  satisfies b_code = α · normalize(E[tt] − E[ft]), where E is the frozen unembedding weight
  matrix, tt/ft are the token indices of the item's own target/foil option-token strings
  as encoded by the run's code, and α is the run's recorded injection scale (EXP065/066:
  α=1; EXP070/077: α=0.50). Provenance is a two-link chain: (E1) the executor's
  weight-only reconstruction matches the documented code formula; (E2) the documented
  code path is the path that executed (pinned file:line table + grep for alternative
  construction paths). Neither link alone suffices.
- **Source:** in-house, `research/analysis_plans/LAW7_BRIDGE_AUDIT_PLAN_LOG197_2026-09-23.md`
  §§2–3. The plan passed Law #14 review (SIGN, LOG-197 sub-entry 4).
- **Epistemic label:** [PROPOSITION] under labeled assumptions — graded **IN-HOUSE-PROOF**:
  the identity is exact algebra on pinned source lines, but the claim that it describes
  the *executed* vectors becomes [THEOREM]-grade only after E1 confirms it on all
  60 items × 4 runs and the execution report survives Law #14 review. Promotion path is
  named, not assumed.
- **Companion criterion (Law #7 compliance):** [DEFINITION] from the Law #7 protocol via
  the audit plan §5 — a reconstruction is Law-#7-compliant iff every construction source
  is one of: frozen model weights, item-unspecific constants, or support/premise material
  provably carrying no per-item target information (e.g., entity-disjoint donor banks with
  the disjointness proof attached). Any reconstruction encoding the item's own
  target/foil option tokens is non-compliant *by definition*, regardless of downstream
  performance.

### L2. Quantitative prediction for the primary endpoint

- **Endpoint:** E1 — construction-algebra identity (deterministic).
- **Prediction:** |cos(b_reconstructed, b_codeform)| ≥ 1 − ε for **all 60 items in each of
  the 4 runs**, with **ε = 1e-6** [ARBITRARY — tagged honestly in the plan: the
  construction is float32 linear algebra; 1e-6 is three orders of magnitude above float32
  unit roundoff (~1.2e-7 per op on unit vectors) and tight enough that no materially
  different direction can pass]. Scale check: ‖b‖ equals the run's recorded injection
  norm (EXP065/066: 1; EXP070/077: 0.50), relative error ≤ 1e-5.
- **Derivation:** direct — the prediction *is* the identity restated as a measurement
  (cosine of the two constructions; norm of the reconstruction vs the recorded scale).

### L3. Breaking point

- **Falsifying observation (identity):** any single item in any run with
  |cos(b_reconstructed, b_codeform)| < 1 − 1e-6. The audit's H0 (a different operator
  was used) wins; the "bridge is built from the answer key" claim dies for that run,
  and the §5 compliance verdict cannot be drawn. Decision: **PIVOT** — the audit's Q1
  answer flips and the §H7 positive-control recommendation is recomputed from the
  surviving runs only.
- **Falsifying observation (compliance):** Q1 = Supported ⇒ the audited construction is
  **non-compliant with Law #7 on the letter** (it encodes the item's own target/foil
  option tokens per item). [INFERENCE] over E1/E2 [OBSERVATION]s. Consequence, pre-named
  in the plan (§I condition 5): such a construction cannot support an *autonomous*
  mechanism claim — recorded "rescues" are label-assisted readout artifacts unless K1/K2
  rule otherwise. Decision: **KILL** for any autonomous-steerability reading of the
  bridge rescues; the bridge's positive-control status goes to the CEO under §H7.
- **Falsifying observation (license itself):** E2 finds an executed label-free
  construction path (the grep was the guard). Then the license was misgraded — the
  executor's reconstruction targeted the wrong code — and the audit restarts at E2.
  The license names its own failure mode; that is the point.
- **Outcome partition:** E1 pass/fail × E2 label-path/label-free × E3 consistent/
  contradictory × E4 attribution bins — the plan's §8 maps every cell to a
  recommendation; no cell defers to executor discretion (Charter M5.2).

### L4. Assumption inventory

- **A1:** the pinned source lines are the code that executed (no unrecorded
  monkey-patching between the repo snapshot and the run). Justification: run
  scripts are the archived execution artifacts; discharge: E2's line-table +
  the Δθ=0/parameter-hash guard (§6) — a hash mismatch is FATAL, results not reported.
- **A2:** float32 determinism of the reconstruction (same op order → same bits).
  Justification: CPU linear algebra on fixed inputs; discharge: the ε=1e-6 tolerance
  absorbs it, tagged [ARBITRARY] with rationale.
- **A3:** EXP070's vectors are UNVERIFIED from the repo (no byte-identical mirror;
  LOG-110) — where no record exists the endpoint is **Underdetermined**, never filled
  by assumption (plan §2 E3 honest boundary).

[INTERPRETATION] This example shows the license regime doing its real job: it forces the
audit to say *in advance* that a Supported Q1 is a compliance failure, not a success —
the breaking point cuts against the author's hopes, which is how you know it is honest.

> **[CORRECTION ADDENDUM 2026-09-23 — Law #14 review LOG-203, fixes F-200-1 and
> F-200-2.]** (a) The L2 paragraph above states "1e-6 is three orders of magnitude
> above float32 unit roundoff (~1.2e-7 per op on unit vectors)." This is
> arithmetically wrong: 1e-6 / 1.2e-7 ≈ 8.4× — less than one order of magnitude,
> not 10³×. The phrasing is quoted faithfully from the signed LOG-197 plan; the
> plan's arithmetic was wrong, not the quote. The tolerance choice itself (ε=1e-6,
> passed 240/240) is unaffected — only the "three orders of magnitude" gloss is
> retracted. A foundations standard cannot carry a false orders-of-magnitude claim.
> (b) L1's "E is the frozen unembedding weight matrix" must be read run-pinned:
> **E = the run's pinned model's unembedding matrix — `EleutherAI/pythia-160m` for
> EXP065/EXP070, `pythia-410m` for EXP066/EXP077** (per the executed audit report's
> E2 model-pin table). E1's first link is therefore 410m-matrix self-consistency
> for EXP065/070, not byte-copies of the executed 160m numerics; the two-link
> chain (E1+E2) remains honest as written. Future licenses must name the run pin
> in L1's statement. [FACT — corrections, not reinterpretations]

## A.6 Transition rule — queued protocols EXP080 and EXP081

**Recommendation to the CEO: license *addenda*, not re-registration. Ratify or amend.**

**The rule:** protocols already signed and queued (EXP080, EXP081) receive a one-page
Mathematical License addendum each — appended, dated, signed, Law-#14-reviewed —
before they can be cleared for GPU. The signed protocol text is never edited
(standing law: corrections are proposed, never silently applied). From EXP082 onward,
the license section is mandatory at draft stage and is checked by the Law #14 reviewer
under Charter M1–M8.

**Reasoning:**

1. **No silent edits.** Both protocols are signed artifacts. Rewriting them to insert a
   license section would violate the corrections discipline the program adopted after
   its own retraction. An addendum preserves the signature chain; a rewrite breaks it.
2. **The licenses already exist — the addendum is honest paperwork, not a rescue.**
   Recovered from signed text (no new claims invented):
   - *EXP080 (G2 oracle ceiling, LOG-172):* Lemma L1 — the oracle-ceiling lemma, proof
     verified airtight under the determinism pin at LOG-166/171/172 (grade
     IN-HOUSE-PROOF, promotion-ready). **L2 prediction:** pool-oracle accuracy ≥
     single-pass accuracy on the N=60 items — a ceiling is an upper bound by
     construction. **L3 breaking point:** bin(ii) (non-bridge pool ceiling) = 0 ⇒ the
     (d)/(e) "output room" licenses collapse to "bridge ceiling, not pool ceiling"
     reporting only; kill branch (c) stands per m7. The Law #7 dependency is already
     explicit in the spec — the addendum makes it a license field rather than prose.
   - *EXP081 (C-A donor transfer v2, LOG-182):* the §4.1 regrouping identity
     Σ_d(W_U[t_d]−W_U[f_d]) = Σ_y W_U[y]·(n_t(y)−n_f(y)) — re-derived by the reviewer
     from the pinned formula, JSON corroboration cos = 0.9999999999999998 (grade
     IN-HOUSE-PROOF). **L2 prediction:** identical per-token (n_t−n_f) ⟹ identical
     centroid; the three-desiderata unsatisfiability follows algebraically. **L3 breaking
     point:** distinct-content alternate agreement < ⌈5n_d/6⌉ ⇒ the C-A transfer claim
     is dead (F1 fix, LOG-182). [FACT — both predictions and breaking points are
     verbatim recoverable from the signed specs; nothing is added.]
3. **Cheapest (Law #15 Q3).** Two one-page addenda (hours of CPU-only doc work) versus
   re-drafting and re-reviewing two signed protocols through full Law #14 cycles
   (weeks, for zero scientific gain). The addendum is the cheapest decision that
   satisfies Q4.
4. **The addendum rides the existing gate.** Both experiments are already gated on the
   Law #7 bridge audit + CEO GPU clearance. The signed addendum becomes a clearance
   precondition — no new process, no parallel track.
5. **The transition is a finding generator, not a rubber stamp.** If writing an addendum
   reveals that a queued protocol's best honest grade is CONJECTURE-UNDER-TEST (or that
   no license above INTUITION exists), the addendum *reports that to the CEO before
   clearance*. [HYPOTHESIS] For EXP080/081 the recovered licenses are IN-HOUSE-PROOF —
   the transition should confirm, not embarrass. But the rule must be stated for the
   case where it does embarrass, or it is not a rule.

## A.7 Breaking point of this standard itself

Per Charter M8 Q1, the standard names what would kill it: **if a protocol carrying a
PROVEN-LEMMA-grade license, whose prediction and breaking point were both honored,
produces a primary-endpoint result that is later retracted for a mathematical error the
license section should have caught** — then this standard failed at its sole job, and it
is demoted to a guideline pending a post-mortem logged in `reports/research_log.md`.
A standard that cannot state its own death condition is a slogan. This one can.

---

# PART B — Standing question memo (theory track opening memo)

**The question:** *Under Δθ=0, what is provably possible for inference-time computation
to add?*

**Status of this memo:** [INTERPRETATION]/survey — the opening position of the theory
track, not a result. Every claim below is labeled; the track's job is to promote the
[CONJECTURE]s and [PROPOSITION]s to [THEOREM]s or kill them.

## B.1 Formalization

[DEFINITION] **Frozen backbone.** Parameters θ ∈ Θ are fixed for the entire episode:
θ_t = θ_0, Δθ_t = 0 for all t (`AGENTS.md` Law #6). θ is the trained weight vector of a
fixed architecture (e.g., a decoder-only transformer).

[DEFINITION] **Temporary inference state.** During inference the procedure maintains
S_t = (B_t, z_t, C_t, M_t, …), where B_t ∈ ℝ^{d×k} is a temporary representation object
(`theory/README_DEFINITIONS.md` §15: a *candidate* representation with a defined
computational role), z_t ∈ 𝒵 is control/latent state, C_t is context/cache, M_t is
scratch memory. All components of S_t are functions of (θ, input history, randomness)
— nothing else exists to draw on.

[DEFINITION] **Inference-time procedure.** An algorithm P that issues a sequence of
**oracle queries** to the frozen map f_θ (one forward pass = one query: prompt →
distribution over continuations), updates S_{t+1} = U(S_t, queries, answers, r_t; θ)
for a computable update operator U built only from frozen θ (sampling, steering
interventions, search, selection, verifier scoring), and returns y = D(S_T) for a
decision rule D. **Budget:** N forward passes (FLOPs); N is the resource.

[INTERPRETATION] This framing reduces the standing question to the **oracle question**:
*with N-query oracle access to a fixed, finitely-representable function f_θ, what can P
compute that f_θ's single-query output cannot?* Everything the program means by
"inference-time computation" — self-consistency, verifier-gated search, adaptive loops,
steering, the G/E/S/T operators — is a choice of (U, D, N). The canonical research
objective (θ_after = θ_before; only S_t evolves) is exactly this formalism in program
language.

## B.2 What is already provable

**P1. Intermediate compute is a complexity resource — provably.** [FACT — CITED-THEOREM,
verified by live fetch 2026-09-23] Merrill & Sabharwal, "The Expressive Power of
Transformers with Chain of Thought," arXiv:2310.07923 (2023): for decoder-only
transformers, the number of intermediate decoding steps provably extends the
recognizable language class — logarithmic steps add little; linear steps (under
projected pre-norm) recognize all regular languages (under standard complexity
conjectures); polynomial steps recognize exactly P. **What this licenses:** inference-time
token budget is not "just sampling" — step count is a genuine computational resource
with class-separation consequences. **What it does not license** (category error to
avoid): the theorem is about *families* of transformers (∃θ recognizing a class), not
about a *fixed* θ gaining capability. "∃θ: CoT helps" does not imply "for our frozen θ,
N more steps add capability C." Any license section importing P1 must state this
limitation explicitly.

**P2. Without intermediate compute, fixed models are provably weak.** [FACT —
CITED-THEOREM, verified via bibliography fetch 2026-09-23] Saturated / log-precision
transformers that answer immediately are constant-depth threshold circuits (Merrill,
Sabharwal & Smith, TACL 2022; Merrill & Sabharwal, "The parallelism tradeoff,"
*TACL* 11:531–545, 2023). [INTERPRETATION] This is the floor that inference-time
compute provably escapes: the limitation P2 proves is exactly what P1's intermediate
steps overcome. Together P1+P2 license the *search space* (more steps can matter) while
saying nothing about whether they *will* matter for a given θ.

**P3. The oracle-information bound — true and nearly vacuous.** [THEOREM — in-house,
elementary] Let P issue N oracle queries to f_θ. Then P's output is measurable with
respect to the σ-algebra generated by (θ, input, the N answers). *No procedure
manufactures information about the target ex nihilo; N queries yield at most N answers'
worth of information.* Proof: three lines — the output is a deterministic (or
randomized, adding no information) function of the query answers. **Breaking point:**
none — it is information theory. Its weakness is vacuity (see B.3): it forbids only
information creation, while the live question is *recomposition*.

**P4. Amplification by resampling is real — empirically.** [OBSERVATION — cited,
verified by live fetch 2026-09-23] Wang et al., "Self-Consistency Improves Chain of
Thought Reasoning in Language Models," arXiv:2203.11171, ICLR 2023: replacing greedy
decoding with sample-then-majority-vote at fixed θ improves reasoning accuracy
(GSM8K +17.9pp, SVAMP +11.0pp, AQuA +12.2pp, StrategyQA +6.4pp). [INTERPRETATION] This
is the existence proof that recomposition produces behavior no single query exhibits
(the majority answer routinely differs from the greedy answer) — and it sits at
evidentiary Level 1 ("can improve inference"), not Level 3. The three evidentiary
levels are never silently crossed: P4 licenses Level-1 claims only.

**P5. Selection gains are bounded by error correlation — provable in principle.**
[PROPOSITION — track to prove as T2] For N-sample majority vote with per-draw
correctness p and exchangeable pairwise error correlation ρ, the N→∞ correctness has a
closed form; as ρ→1 the ceiling collapses to p (perfectly correlated errors make
voting provably inert). Elementary probability; the track's job is to write it cleanly
and turn it into a licensed quantitative prediction (see T2).

**P6. An information-free selector is provably inert.** [PROPOSITION — track to prove as
T1] If a verifier/scorer V is statistically independent of correctness given the
generator's draws (exchangeable scores under H0), then best-of-N selection by V has
*exactly* the single-draw success probability. Symmetry argument; the independence
condition is the falsifiable hinge. This is the sharpest existing discriminator between
"search works" and "search is theater."

## B.3 Honest admission — where the math is weaker than the ambition

[INTERPRETATION — the track's candid assessment, labeled as such:]

1. **The oracle bound (P3) is nearly vacuous against the real question.** It rules out
   only creation of information. But nobody's mechanism hypothesis claims to create
   information — they claim to *recompose* it (search, verify, select, iterate). P4 is
   the standing counterexample to any naive "nothing new is possible" reading: the
   majority-vote answer is genuinely new behavior from a fixed oracle. Any impossibility
   claim that P3 refutes was never a serious claim.
2. **"Qualitatively new capability" is undefined, so no impossibility proof is currently
   possible in principle.** This is the binding constraint. Until the track produces a
   formal capability-class definition with decidable membership (T3), every sentence of
   the form "X is provably impossible under Δθ=0" is either (a) secretly about a narrow,
   already-formalized class (fine — say which), or (b) metaphysics. The program's
   falsification discipline requires the same honesty about impossibility claims as
   about capability claims.
3. **P1/P2 are about ∃θ, not about our θ.** The expressivity literature bounds what
   intermediate compute can do *across weight settings*. It does not bound — in either
   direction — what N more queries add to *this* frozen model on *this* task. Importing
   "CoT makes transformers Turing-complete" as a license for "our loop will discover
   new cognition" is the category error the Math Charter's M4 (space check) exists to
   catch, applied to theorems instead of vectors.
4. **Test-time scaling behavior is description, not limitation.** Empirical scaling of
   accuracy with compute predicts returns; it does not bound what is achievable, and it
   certainly does not distinguish Level 2 ("changes the computational strategy") from
   Level 3 ("creates qualitatively new capability").
5. **Bottom line:** current mathematics licenses *search, verification, and
   recombination over a fixed oracle* as the only channels (Level 1 firmly, Level 2
   conditionally on the verifier carrying independent information per P6), says nothing
   yet that discriminates Level 3, and provides **no proven barrier to Level 3 and no
   proven path to it either**. The field is open. [INFERENCE] That openness is precisely
   why the instrument is the falsification program, not armchair proof: the math tells
   us where to dig (verifier information, error correlation, oracle ceilings) and
   refuses to tell us what we will find.

## B.4 What would constitute a proof — either direction

**Impossibility direction** would require, jointly: (i) a formal definition of
"qualitatively new capability under Δθ=0" as a capability class C with a decision
procedure for membership (this is T3); (ii) an information-theoretic lower bound —
e.g., any N-query oracle procedure entering C requires a verifier carrying ≥ k bits of
information independent of the generator (or ≥ poly(N) bits of independent oracle
information); (iii) a demonstration that the program's candidate mechanisms cannot
supply it. P6 (T1) is the first rung of this ladder: it proves the k=0 case.

**Possibility direction** would require: an explicit construction — an oracle procedure
P* plus a bounded-information verifier that *provably* solves a task class outside the
one-shot reachable set of f_θ — where "outside" is itself proven via a one-shot lower
bound on f_θ for that class. [INTERPRETATION] EXP080's oracle ceiling is the empirical
shadow of exactly this: it measures the gap between the pool-oracle and the single
pass. A proof would pin that gap from below instead of measuring it from above.

**What would not constitute a proof:** an asymptotic class-separation result about
∃θ (P1-style) cited as settling the fixed-θ question; a benchmark gain cited as a
capability-class separation; a bound whose breaking point was never named (Charter M8).

## B.5 Concrete proof targets for the theory track

**T1 — The inert-verifier lemma (no-free-lunch for selection).**
[PROPOSITION → THEOREM target] *Statement sketch:* let generator G produce i.i.d.
candidates c_1…c_N with single-draw success probability p; let scorer V assign scores
s_i = V(c_i); assume (s_1…s_N) is independent of (correct(c_1)…correct(c_N))
[ASSUMPTION — the hinge]. Then P(argmax_i s_i correct) = p exactly. *Proof idea:*
exchangeability — under the independence assumption the selected index is uniform and
independent of correctness. *Breaking point:* the lemma breaks exactly when V ⫫̸
correctness — i.e., selection gains *require* the verifier to carry independent
information, which converts every verifier-gated design's license question into "name
the independent information your verifier carries, in bits or in mechanism."
*Deliverable:* two pages under the Math Charter; on promotion to [THEOREM] it becomes
the standard license for all verifier-gated protocols (their L1 cites T1; their L2
names the verifier's independent information; their L3 is the independence test).

**T2 — Correlated-error ceiling for majority vote.**
[PROPOSITION → THEOREM target] *Statement sketch:* for N-sample majority vote with
per-draw correctness p and exchangeable pairwise error correlation ρ, derive the exact
N→∞ limiting correctness and a finite-N bound; show collapse to p as ρ→1 and
convergence to 1 as N→∞ when ρ<1 and p>1/2 (Condorcet regime). *Breaking point:* a
measured (p, ρ) pair whose observed majority-vote accuracy exceeds the bound kills the
exchangeability modeling assumption — the failure is informative (it localizes
non-exchangeable structure). *Deliverable:* closed-form bound + the prediction template
that turns P4 (self-consistency as observation) into licensed quantitative predictions
for any future voting/search protocol's L2 field.

**T3 — The capability-class boundary (definitions-first).**
[CONJECTURE → DEFINITION + THEOREM target — hardest, highest value] Draft a candidate
formal definition of "qualitatively new capability under Δθ=0" as a strict class
separation: task classes solvable by N-query oracle procedures but *provably not* by
1-query procedures *under the same verifier-information budget* (so the separation
cannot be smuggled in through the verifier). Then prove at least one separation
instance exists — candidate construction: an explicit toy f_θ (small, fully specified)
where bounded-step search provably decides a language outside the oracle's one-shot
image, with the one-shot lower bound proven, not asserted. *Breaking point / refutation
of usefulness:* if every candidate definition either collapses to Level 1
(re-labeling "improvement" as "new capability") or is undecidable in practice, the
definition is discarded and the failure is logged — a killed definition is progress,
per the program's cull discipline. *Deliverable:* the definition, the separation proof
(or the honest autopsy), and the decision procedure for class membership. Until T3
lands, the standing question remains open *by construction* — and the track says so
plainly.

---

## Reading guide & change protocol

- License grades and epistemic labels in this document follow `AGENTS.md` §5 and the
  Math Charter M2; the Charter's M1–M8 apply to every proof the track produces.
- This standard may only be weakened by the user's explicit instruction; any agent may
  propose strengthening it via `reports/research_log.md` (Charter enforcement clause).
- The worked example (§A.5) is pinned to the LOG-197 audit plan as signed on 2026-09-23;
  if the audit's execution changes any number, the example is amended by dated addendum,
  not silent edit.

*End of standard. Written LOG-200, 2026-09-23. Awaiting CEO ratification (§A.6).*
