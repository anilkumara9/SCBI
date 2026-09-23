# MATH STANDARDS CHARTER — SCBI Research Program

**Status:** Standing law. Effective 2026-09-23. Inherits authority from `AGENTS.md` Laws #5
(anchored definitions), #11 (observation/interpretation separation), #13 (reproducibility), and
#14 (challenge rather than defend). Every agent that states, uses, or reviews a mathematical
claim in this program is bound by it. Violations are adversarial-review findings, not style notes.

**Why this exists:** On 2026-09-23 this program retracted a published-style claim
($\Delta\cos \approx +0.13 \to +0.79$) whose primary artifacts showed $\Delta\cos \approx -0.70$.
The failure was mathematical, not experimental: a rank-2 orthogonal Procrustes fit was applied
as a full-dimensional rotation across two different vector spaces. The program's math must be
top-lab grade because its conclusions are only as sound as its derivations. This charter is the
mechanism.

---

## M1. Definitions before theorems

**M1.1.** No lemma, proposition, theorem, or "it can be shown that" may appear before every
symbol it uses is defined or cited to its definition. Definitions live in
`theory/README_DEFINITIONS.md` (§96+) or in a `Notation context` block at the top of the
document; document-local notation **MUST** state its scope ("In *this* document, $R$ denotes…").

**M1.2.** Any term with a prior meaning in the program ($R$ = representation update vs Procrustes
factor; $r$ = rank vs vector; "basis", "alignment", "transfer") **MUST** be disambiguated at
first use in each document. Reuse of a symbol with a different meaning without a scope note is
a **MAJOR** finding.

**M1.3.** Definitions are versioned. Changing a definition's meaning mid-program requires the
Definition Change Protocol (`AGENTS.md` Law #5); silently shifting a definition to rescue a
proof is fabrication-adjacent and treated as such.

## M2. The labeling law, with teeth

`AGENTS.md` §5 gives the labels. This charter gives the promotion rules — what evidence moves
a claim up the ladder, and what demotes it.

**M2.1. Ladder (bottom to top):** `[CONJECTURE]` → `[PROPOSITION]` (statement + complete proof
modulo explicitly labeled assumptions) → `[THEOREM]` (complete proof, all assumptions discharged
or universally accepted). `[ASSUMPTION]` is not a rung — it is a declared debt.

**M2.2. Promotion criteria (all must hold):**
- CONJECTURE → PROPOSITION: a proof exists in which *every* non-axiomatic step is either derived
  or delegated to an explicitly labeled `[ASSUMPTION]` with a stated justification and a stated
  plan to discharge it (measurement, experiment, or proof). The assumption's label must travel
  with every citation of the proposition.
- PROPOSITION → THEOREM: all labeled assumptions discharged by proof or by measurement from
  primary artifacts, AND the proof has survived one adversarial review that attempted to break
  each step (not merely read it).
- Nothing is promoted by vote, by elegance, or by matching intuition.

**M2.3. Demotion triggers (automatic):** a claim rated `[THEOREM]` is demoted to `[PROPOSITION]`
the moment an undischarged assumption is found hiding in its proof; to `[CONJECTURE]` if its
proof has a gap no assumption covers. The demotion is logged in `reports/research_log.md`
with the exact step that failed.

**M2.4. Conditional results MUST name their condition in every citation.** "The Proposition shows
scramble" is forbidden; "the Proposition shows scramble *in expectation under the Haar-completion
model A-comp*" is required. Dropping the condition when citing is a **MAJOR** finding
(condition-laundering).

**M2.5. Worked example (binding precedent):** `theory/proofs/procrustes_failure_analysis.md`
rates its rank-deficiency Lemma `[THEOREM]` (assumptions discharged, proof adversarially
self-reviewed) and its scramble result `[PROPOSITION]` under labeled `[ASSUMPTION]` A-comp,
with the unmeasured genericity flagged T-1 ("illustrative scale; genericity unmeasured").
This is the template. Note its imperfection is also precedent: §6 point 4 of that document
incorrectly claimed repeated singular values break the fit part's uniqueness — the Lemma's own
proof needs no distinctness. Even self-review sections are subject to M2.

## M3. Exact-vs-asymptotic honesty

**M3.1.** Every number in a proof or derivation is one of: `[EXACT]` (follows algebraically from
stated premises — show the algebra or cite the line), `[ASYMPTOTIC]` (holds in a stated limit —
state the limit and the regime you are actually in), or `[ILLUSTRATIVE]` (a scale example —
tagged as such, never cited as evidence).

**M3.2.** The symbol `≈` **MUST** be accompanied by what is being approximated, in which regime,
and the size of the error or a bound on it. Bare `≈` in a derivation is a **MINOR** finding;
bare `≈` in a *conclusion* is a **MAJOR** finding. `≲`/`≳` are allowed only with the same
disclosure.

**M3.3.** A bound is not a measurement. "Observed values lie inside the predicted band" licenses
consistency, not confirmation. Saying a bound is "confirmed" by data inside it is a **MAJOR**
finding (direction-of-fit error).

**M3.4.** Rounding: reported rounded values (`0.88`, `0.42`, `ρ̂ ≳ 0.235`) **MUST** have their
unrounded computed values recorded in the same document or a cited artifact
(`0.877555`, `0.417093`, `0.2353` via $t_{48,0.95}$). A reviewer must be able to recompute every
digit shown.

**M3.5. Precedent:** the scramble-bound numerics $\sqrt{3/768} = 0.0625$ were correctly derived
but initially presented without the genericity caveat; the T-1 corrections pass re-tagged them
`[ILLUSTRATIVE]`. The McNemar table ($(5,0)\to0.0625$, $(6,0)\to0.03125$, $(8,0)\to0.007812$,
$(8,1)\to0.039062$) recomputes exactly from the two-sided exact definition — this is the bar.

## M4. Dimensional and space-consistency checks (mandatory pre-proof steps)

No proof or operator analysis is reviewed until it passes these four checks. They are
**preconditions**, not appendix material.

**M4.1. Shape check.** Every matrix product, SVD, and application $R v$ **MUST** have its shapes
stated at first use ($E_k \in \mathbb{R}^{2 \times d}$, $M = E_k^T E_0 \in \mathbb{R}^{d \times d}$,
$R_k \in \mathbb{R}^{d \times d}$, $\hat{v} \in \mathbb{R}^d$). A shape mismatch is a **FATAL**
finding — the document stops there.

**M4.2. Space check.** Every vector and every operator's domain **MUST** name its space:
residual stream at layer $l^*$ vs unembedding rows vs attention OV subspace vs logit space.
An operator fit in space $A$ and applied in space $B \neq A$ **MUST** carry an explicit,
labeled transfer assumption (cf. A-cross, `procrustes_failure_analysis.md` §4) with its own
falsification criterion. Unstated cross-space application is a **FATAL** finding — this exact
failure cost the program its first central claim.

**M4.3. Rank check.** Any claim invoking a fitted operator **MUST** state the fit rank $r$,
the ambient dimension $d$, and what happens on the $(d-r)$-dimensional orthogonal complement.
"Rotation" applied to a vector with $\|P_S v\| \ll 1$ is scrambling until proven otherwise;
the burden of proof is on the claimant.

**M4.4. Unit/normalization check.** Every direction used in an intervention **MUST** state its
norm convention and where renormalization happens. Renormalizing a 10%-energy projection to
unit norm before injecting at fixed $\alpha$ amplifies it 10× — energy statements and
injection statements must never be mixed without the amplification factor shown.

## M5. Trivial-case and edge-case testing

**M5.1.** Every lemma/proposition **MUST** be evaluated on: the trivial case ($r = 0$, $n = 0$,
empty set, identity operator), the degenerate case (zero-variance input, constant labels,
$b = c = 0$), and the boundary case (threshold equality, e.g. $p = 0.05$ exactly, $\Delta M$
exactly at the bar).

**M5.2.** Decision procedures (gates, branches, trees) **MUST** have an exhaustive partition:
every cell of the outcome space lands in exactly one branch. A cell with no branch
(positive-but-nonsignificant outcomes; undefined test statistics) is a **MAJOR** finding —
*pre-registration's m7 precedent*: the fix is widening a trigger or adding a branch, never
executor discretion.

**M5.3.** Statistical tests **MUST** state: the exact null hypothesis, the exchangeability or
distributional justification (permutation tests: what is permuted, why it is valid under H0),
the handling of degenerate inputs (zero variance → statistic undefined → which branch?),
and all pinned parameters (number of permutations $B$, seed — `AGENTS.md` Law #13).
"Exact permutation $p$" with unpinned $B$ is not reproducible and is a **MINOR** finding;
an undefined statistic with no assigned branch is a **MAJOR** finding (*ρ-gate precedent,
2026-09-23*: the transfer probe received a degenerate-probe rule; the ρ-gate's own
zero-variance edge was left unruled — do not repeat this asymmetry).

**M5.4.** Every "impossible" cell in a partition table **MUST** carry its proof of impossibility
in one line (e.g. "$b = c \Rightarrow p = 1.0$ under exact McNemar, so $(\Delta M = 0, p < 0.05)$
is vacuous"). Unargued "impossible" is a **MINOR** finding.

## M6. Proof vs sketch vs hand-wave

**M6.1.** A **proof** shows every step; a step may cite a standard result by name
(Cauchy–Schwarz, Schur's lemma, cyclic property of trace) but the citation must be *correct* —
a misattributed or sloppy citation (e.g. invoking Schur's lemma where the equivariance argument
actually needed is sphere-uniformity) is a **MINOR** finding even when the result is right,
because the next reader will copy the argument, not the result.

**M6.2.** A **sketch** is labeled `[SKETCH]` and states which steps are omitted and why they are
routine. An unlabeled sketch presented as a proof is a hand-wave.

**M6.3.** A **hand-wave** ("it can be shown", "clearly", "by symmetry" doing real work,
"the general case follows") with no labeled assumption or citation is a **MAJOR** finding.
"By symmetry" is allowed only when the symmetry group and the invariant quantity are named
($Q_0 \stackrel{d}{=} -Q_0$ under Haar; $E\|P_S v\|^2 = r/d$ for $v$ uniform on the sphere with
$S$ fixed — the distribution of $v$ must be stated).

**M6.4.** The rank-deficiency Lemma's proof (`procrustes_failure_analysis.md` §2) is the
program's reference proof: hypotheses minimal, each implication shown, edge case ($r=0$)
covered by the same argument, no hand-waves. Match it.

## M7. No metaphor as definition

**M7.1.** Metaphors ("invented basis", "treasure in the room", "the room", "surgery",
"ceiling" as a noun doing causal work) **MUST NOT** appear in definitions, theorem statements,
or license text. They may appear in motivation sections only, and only already-qualified
("the treasure was found *with a map*").

**M7.2.** Any term that has done metaphorical duty in the program's history **MUST** be replaced
by its operational definition before reuse: not "alignment", but "orthogonal Procrustes fit of
$E_0^T$ to $E_k^T$ minimizing $\|RA - B\|_F$"; not "transfer", but "$\Delta M > 0$ with McNemar
$p < 0.05$ on the pre-registered benchmark".

**M7.3.** A proof or license whose key step, read literally, refers to the metaphor rather than
the definition is a **MAJOR** finding. If removing the metaphorical sentence removes content,
the content was never there.

## M8. Falsification checklist for mathematical claims

Before any mathematical claim is cited as `[THEOREM]`/`[PROPOSITION]` in a protocol, paper, or
review, the claimant **MUST** answer these in writing, in the document:

1. **What would prove it false?** (A counterexample schema, a violated assumption, a
   measurement that contradicts it. "Nothing — it's math" is disqualifying: state the
   assumption whose failure kills it.)
2. **Where is the assumption inventory?** (Every undischarged assumption listed with label,
   justification, and discharge plan. If the list is empty, say so and say why.)
3. **What did the adversary try?** (At least one concrete attack per proof step — wrong space,
   rank collapse, degenerate input, swapped quantifiers — and why it failed.)
4. **Do the numbers recompute?** (An independent recomputation of every displayed number from
   stated premises; record unrounded values per M3.4.)
5. **Does the label survive citation?** (Read the citing sentence: does it carry the condition?
   If not, fix the citation, not the label.)
6. **What is the smallest change that breaks it?** (Sensitivity: which premise is load-bearing?
   The Lemma's load-bearer is $\operatorname{rank}(M) = r < d$; the Proposition's is A-comp.
   Name yours.)

A claim that cannot answer (1) is not a claim — it is a slogan. A claim that cannot answer (4)
is not checked — it is trusted. This program does not trust; it verifies.

---

## Enforcement

- The Adversarial Reviewer **MUST** apply M1–M8 to every theory document and every mathematical
  passage of every pre-registration. Findings cite the violated section (e.g. "M4.2 FATAL:
  operator fit in unembedding space applied to residual-stream vectors without a transfer
  assumption").
- Severity: FATAL (work stops; document not cited until fixed) > MAJOR (must fix before the
  dependent experiment runs or the paper cites it) > MINOR (fix within one review cycle).
- This charter may only be weakened by the user's explicit instruction; any agent may propose
  strengthening it at any time via `reports/research_log.md`.
- Precedents cited above (Procrustes Lemma, A-comp/T-1, m7 partition gap, ρ-gate degeneracy
  asymmetry, §6-point-4 singular-value error) are binding interpretations, not anecdotes.

*First audit under this charter: Mathematics Auditor report, 2026-09-23
(`reports/research_log.md`). The Lemma passes; the program's math is strong but not flawless —
§6 point 4, the ρ-gate's unpinned permutations and unruled zero-variance edge, and one sloppy
Schur citation are the first entries in the correction ledger. That is the system working.*
