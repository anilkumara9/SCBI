# Adversarial Review — Wave 2: Literature Audit & Theory Deliverables

**Role:** Adversarial Reviewer (red-team; challenge, don't defend)
**Date:** 2026-09-23
**Scope:** `research/literature/audit_2026-09-23.md`, `reports/novelty_report.md`,
`theory/BOUNDARY_CLAIM_FORMALIZATION.md`, `theory/proofs/procrustes_failure_analysis.md`,
`experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md`
**Method:** Independent citation spot-checks via live web search (6 queries); line-level
mathematical verification of the Lemma and Proposition proofs; design audit of the EXP067
protocol against the defects it claims to fix; cross-agent consistency check.
**Standing:** This report does not edit the reviewed files. Required fixes are listed per
deliverable; nothing is accepted until fixes land and this reviewer re-signs.

---

## 0. Executive verdicts

| Deliverable | Verdict |
|---|---|
| Literature audit (`research/literature/audit_2026-09-23.md`) | **ACCEPT WITH CORRECTIONS** (major: missing priors) |
| Novelty report (`reports/novelty_report.md`) | **ACCEPT WITH CORRECTIONS** (inherits audit fixes) |
| Boundary formalization (`theory/BOUNDARY_CLAIM_FORMALIZATION.md`) | **ACCEPT WITH MINOR CORRECTIONS** |
| Procrustes proof (`theory/proofs/procrustes_failure_analysis.md`) | **ACCEPT WITH CORRECTIONS** (math verified; empirical grounding required) |
| EXP067 protocol (`experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md`) | **ACCEPT WITH CORRECTIONS** (major: incomplete falsification logic; program-level contradiction — see §5) |

No deliverable is **REJECTED**. The N1 verdict **stands** and is strengthened by this review.

---

## 1. Literature audit — citation verification

Spot-checked 6 records against the live web; all exist and are substantially as characterized:

1. **Braun et al., 2505.22637** — REAL. One correction: venue is the **ICLR 2025 Workshop on
   Foundation Models in the Wild**, not merely "arXiv preprint" (audit §2.10). Characterization
   confirmed by the abstract: steering "unreliable when the target behavior is not represented
   by a coherent direction" — this directly supports the audit's use of it against SCBI.
2. **Tan et al., 2407.12404** — REAL, NeurIPS 2024, authors/venue as stated. An independent
   secondary source confirms the audit's key claim: "many behaviors turn out to be unsteerable"
   for CAA specifically. Characterization stands.
3. **Rimsky et al. (CAA), 2312.06681** — REAL, **ACL 2024** confirmed by multiple independent
   sources. Method characterization verified against the abstract: mean difference of residual
   stream activations between contrastive pairs, added during inference. The audit's
   [EQUIVALENT] rating for the tested mechanism is **mathematically sound**: SCBI's
   $B_{agg} = \mathrm{normalize}(\sum_k \hat{v}_k)$ with per-instance-normalized contrast means,
   applied as $h \leftarrow h + \alpha u$ ($\alpha = 0.50$), is the same operator class as CAA's
   $v = \bar{h}_+ - \bar{h}_-$, $h \leftarrow h + c\,v$. Per-instance normalization, 5-vocabulary
   aggregation, fixed coefficient, and single-layer application are preprocessing/hyperparameter
   choices, not a new operator. The audit is correct to rate these as non-distinguishing.
4. **Dathathri et al. (PPLM), 1912.02164, ICLR 2020** — REAL, and **missing from the audit**
   (see objection L-1).
5. **Madaan et al. (Self-Refine), 2303.17651, NeurIPS 2023** — REAL, and **missing from the
   audit** (see objection L-2).
6. **Geiger et al. (DAS)** — the audit's "CLeaR 2024" venue with the v236 proceedings URL is
   plausible and consistent with the paper's publication history (original preprint 2023,
   arXiv:2303.02536). Not flagged as fabrication. Minor: the record should also cite the 2023
   preprint for completeness.

No fabricated citations found. The search log (§1) is credible.

### Objection L-1 [MAJOR]: Missing prior — Plug and Play Language Models (PPLM)
Dathathri et al., ICLR 2020 (arXiv:1912.02164): **per-instance, inference-time gradient-based
updates to hidden states of a frozen LM**, guided by an external attribute classifier
(evaluator) with KL regularization to stay on-manifold. This is the closest published prior to
"dynamic representation intervention with an evaluator at inference time, $\Delta\theta = 0$."
It belongs in the taxonomy (Family C, or a new slot: gradient-guided hidden-state search) and
weakens the audit's "no exact prior" hedge for the dynamic loop. The remaining distinction —
SCBI's evaluator is supposed to be *internal* (self-consistency) rather than an external
classifier, and the search object a *basis* rather than a hidden-state trajectory — is a
combination of PPLM's intervention locus with ToT's self-evaluation. That sentence is the
definition of N1. **Required fix:** add a full §5-format record for PPLM; update §3.3, §7, and
the novelty report's "exact-prior statement" to the qualified form: "no verified paper
demonstrates the complete loop with a *self-consistency* evaluator over *bases*; the closest
dynamic-intervention prior (PPLM) uses an external evaluator over hidden states."

### Objection L-2 [MAJOR]: Missing prior — Self-Refine (Madaan et al., NeurIPS 2023)
Generate → self-critique → refine loop with a single frozen LLM, no training, ~20% absolute
gains. This is a second independent G/E/S-loop prior over outputs, alongside ToT and
self-consistency, and its documented limitation (gains plateau; self-critique has blind spots)
is directly relevant to SCBI's unvalidated $\mathcal{E}$. **Required fix:** add the record to
Family C; cite its blind-spot finding as an additional falsifier-risk for SCBI's evaluator.

### Objection L-3 [MINOR]: Braun venue correction
§2.10: venue is ICLR 2025 Workshop on Foundation Models in the Wild, not "arXiv preprint."

### Objection L-4 [MINOR]: KV-cache steering record (§2.22) is below the bar
Cited from a paper-aggregation page with self-flagged low confidence. Either verify it against
the primary source or drop it to an [OPEN] follow-up line. A low-confidence record inside an
otherwise high-confidence audit is a needless attack surface.

### Objection L-5 [MINOR]: Drop "N2-aspirational" phrasing
Novelty report §1 and audit §7 describe the untested loop as "N1 with an untested
N2-aspirational component." An untested formulation with zero empirical support cannot be
"N2-aspirational" — that smuggles a higher tier in through adjectives. Per protocol §13 it is
unscored conjecture. **Required fix:** replace with "unvalidated formulation distinction;
unscored pending demonstration."

**Net:** the audit's N1 verdict survives all attacks and is *strengthened* by L-1/L-2. The
tested mechanism remains N0; the loop remains an unscored conjecture with *stronger* priors
than the audit listed.

---

## 2. Theory — Procrustes failure analysis (proof verification)

I re-derived the Lemma and Proposition from scratch. **The mathematics is correct.**

- **Lemma (non-uniqueness):** the $\mathrm{tr}(Z\Sigma)$ maximization argument is airtight.
  The step "orthogonal $Z$ with $z_{ii} = 1$ for $i \le r$ forces $Z = \mathrm{diag}(I_r, Z_0)$"
  holds: a unit-norm row with a $+1$ entry is exactly $e_i^T$, and likewise for columns.
  Rating [THEOREM] is **justified**. No correction.
- **Proposition (scramble bound):** the Haar-invariance + Schur's lemma derivation of
  $\mathbb{E}[Q_0 c c^T Q_0^T] = \frac{\|c\|^2}{d-r}I$ is correct; the $a^2$ + cross-term
  expansion is correct; the deterministic corollary
  $\mathbb{E}[(w^T R v)^2] \le \|P_S v\|^2 + \frac{1}{d-r}$ is correct; the Jensen step is correct.
  The A-comp assumption is **explicitly labeled and self-flagged in §6** — this is exactly what
  honest labeling looks like. No mathematical correction needed.

### Objection T-1 [MAJOR]: The "typical $v$" numerics must be grounded in measured quantities
The headline numerics (bound 0.0625/0.0541 vs observed 0.0032/−0.0118) rest on the genericity
assumption $\mathbb{E}\|P_S \hat{v}\|^2 = r/d$. But $\|P_S \hat{v}_k\|$ — the projection of the
*actual* contrast directions onto the *actual* 2D anchor subspace — is **computable from the
primary artifacts** (the $E_k$ anchor stacks and $\hat{v}_k$ vectors exist in the run scripts'
provenance). **Required fix:** compute $\|P_S \hat{v}_k\|$ per vocabulary from the stored
artifacts and report it in the proof document. If $\|P_S \hat{v}_k\| \approx \sqrt{2/d}$, the
genericity assumption is *measured*, and the bound graduates from illustrative to
data-grounded. If it is large, the scramble story needs revision — which is exactly the kind of
check that separates a proof sketch from a result. Until then, the numerics table must carry an
explicit "illustrative scale; genericity unmeasured" caveat.

### Objection T-2 [MINOR]: State the charitable rescue of A-cross explicitly
§4 marks A-cross "unsupported and, in this operationalization, contradicted." A hostile reader
could call this a strawman: nobody would defend fitting on token-identity geometry to rotate
relational directions *once stated plainly*. The charitable rescue — fit the map on
same-space, same-object correspondences — is precisely the EXP067 design. **Required fix:** add
one paragraph stating the rescue explicitly ("A-cross's salvageable core is the uniformity
claim tested by EXP067's Stage A gate"), so the document cannot be accused of defeating only
the weakest version of the assumption.

### Objection T-3 [MINOR]: A-comp determinism wording
§6 correctly notes torch's SVD completion is deterministic-but-arbitrary. Strengthen one
sentence: the Proposition's expectation is over the *design space* of completions, not a
sampling distribution governing the observed run — the observed cosine is one draw from an
unknown deterministic rule, and the Lemma (not the Proposition) is what makes that draw
task-arbitrary. The document already says this; make it unmissable.

**Net:** proof stands; Lemma promoted without reservation; Proposition correctly rated.
T-1 is the only fix that touches evidence rather than prose.

---

## 3. Theory — Boundary claim formalization

Careful, well-labeled, with explicit non-claims (§3.5) — including the notable "not a claim
about superhuman capabilities," which correctly holds the line against the program's ambient
hype pressure.

### Objection B-1 [MINOR]: O1's evidential weight
O1 ($\approx 0.7$ raw cosine) is listed as an [OBSERVATION] — correct — but the document should
cross-reference, at O1 itself rather than only in Q2, that Ethayarajh (2019) anisotropy and the
missing Jorgensen (2023) mean-centring control mean this number cannot be read as "shared
relational geometry" without further controls. Q2 raises it; O1 should carry a one-line
pointer so a careless reader cannot lift O1 out of context.

### Objection B-2 [MINOR]: H1's falsification criterion lives in two places
H1 (§3.3) states the falsification criterion; the EXP067 spec (§7) states it slightly
differently. After the EXP067 fixes in §4 below land, reconcile the two wordings to a single
canonical statement and cross-reference it. Two sources of truth for one criterion is a
future inconsistency bug.

**Net:** accept with minor corrections.

---

## 4. EXP067 protocol — design audit

This is a strong pre-registration: same-space fit, full-rank guards, explicit identity lift,
support-data-only head selection, 7 conditions, headroom gate, SHA-256 guard, margins demoted
to exploratory. The D1–D4 traceability table is exactly what a protocol should contain. The
following are required before execution.

### Objection E-1 [MAJOR]: The falsification criterion is incomplete — the decision tree has holes
§7 covers exactly one outcome: (C3 null ∧ C4 positive) → H1 falsified. Unspecified:
- **(a) Stage A gate halts** (no head with $g_h > 0$, or rank/spectral guard aborts): H1 is
  then *untestable under this operationalization*, not falsified and not confirmed. The verdict
  must be pre-registered: "A-anchor rejected on support data; H1 remains [OPEN]; the boundary
  claim I1 stands unchallenged by this experiment."
- **(b) C4 positive control fails** (bridge does not replicate): the experiment is
  *uninformative* — setup broken or benchmark drifted — and no conclusion about H1 may be
  drawn. Pre-register: "invalid run; diagnose before any re-registration."
- **(c) C3 mixed outcome** ($b > 0$ but $p \ge 0.05$; or $\Delta M < 0$; or $b > 0, c > 0$):
  pre-register the reading (e.g., "directionally positive but non-significant → H1 not
  confirmed; report as weak/partial evidence with exact statistics," and "$\Delta M < 0$ →
  report as negative result per Law #8").
**Required fix:** replace the single criterion with the full pre-registered decision tree. A
falsification criterion that only binds on one branch is not binding.

### Objection E-2 [MAJOR]: Halt gates must be pre-registered as *reportable outcomes*, not off-ramps
The protocol has three halts (Stage A gate, rank/spectral guard, headroom gate). If a halt is
treated as "tweak and rerun," the gates become p-hacking-adjacent. **Required fix:**
pre-register that *any halt IS the published outcome of EXP067* — with the full diagnostic
table ($g_h$ per head, rank/spectral values, baseline accuracy) written to the run directory
and reported. A halted EXP067 is a result (A-anchor rejected / benchmark miscalibrated), not a
non-result. Explicitly forbid re-running with adjusted anchors, $K$, or templates under the
EXP067 label; any adjusted design is EXP068 with a new pre-registration.

### Objection E-3 [MINOR]: Name the uniformity assumption explicitly
The rotation is **fit** on entity-frame anchors (role-matched head outputs) but **applied** to
the relational basis $B_{agg}$. Same-space fixed the *space* defect; the *object* mismatch
(fit object ≠ apply object) is the surviving cousin of A-cross. The protocol's saving grace is
real: the Stage A gate computes $g_h$ on the **relational** directions $\tilde{v}_k^{(h)}$, so
it *validates* the uniformity assumption on held-out support data rather than assuming it.
**Required fix:** name it — [ASSUMPTION] A-uniform: "the vocabulary-renaming rotation estimated
from entity-frame anchors acts uniformly on relational directions in $S_h$" — and state that
the Stage A gate is its empirical test. Do not repeat A-cross's original sin (unstated
assumption).

### Objection E-4 [MINOR]: SHA-256 expected value is environment-sensitive
The pre-registered hash `4c24…de936` was computed in one environment; safetensors weight bytes
should be deterministic, but tokenizer/config handling may differ across machines. **Required
fix:** make the *binding* guard the runtime pre/post match (computed in the execution
environment); the registered value is a sanity check, not an independent abort trigger.

### Objection E-5 [MINOR]: C2 is not EXP066's static condition
C2 (head-projected static, $\sum_h Q_h Q_h^T B_{agg}$) differs from the historical static
condition (full $B_{agg}$). The C2-vs-C3 contrast cleanly isolates the rotation effect *within
head subspaces* — good design — but any comparison of C2 against the EXP066 static null must
note the changed intervention. One sentence in §3.4.

**Net:** the protocol is execution-ready once E-1 and E-2 land. E-3 should land with them; E-4
and E-5 are one-line fixes.

---

## 5. Cross-cutting objection [FATAL to program coherence, not to any single document]

**The two agents' deliverables contradict each other on what EXP067 should be.**

- The literature audit (and novelty report §4): *"EXP067 must test the loop, not the static
  vector."* — i.e., the only novelty-relevant experiment is a per-instance
  $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ demonstration.
- The EXP067 protocol: tests a **static per-vocabulary-pair aligned vector** — explicitly
  *not* per-instance ("per-instance dynamic rotations deliberately removed," §9), and
  explicitly *not* the loop.

Both positions are defensible in isolation; together they are incoherent. If the program
executes the protocol as written while its own literature review declares that experiment
off-mission, the left hand does not know what the right hand is doing — and Law #4
(hypothesis/scope discipline) is violated in spirit.

**Resolution (required before execution):**
1. **Reframe EXP067 explicitly as a boundary-characterization experiment**, not a novelty
   experiment. Its research question — "does operator soundness change the Stage B null?" —
   is legitimate *boundary science*: it determines whether the I1 dissociation survives a fair
   test. Its outcome **cannot move the novelty needle in either direction**: a positive C3
   result would be a better-executed instance of an N0 mechanism (CAA-equivalent); a null
   result confirms the boundary. The protocol's §1 and the novelty report must say this
   plainly.
2. **Spin the loop test out as a separate future protocol** (EXP068 candidate) — but it may
   not be pre-registered until an **operational $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$
   specification exists on paper**. There is currently no implementable loop design in the repo;
   demanding an experiment for an unspecified mechanism is how the next forensic audit gets
   written. The Theory Agent's next assignment is that spec, with PPLM/ToT/Self-Refine as the
   explicit design priors it must distinguish itself from.
3. **Paper framing follows the science, not the ambition:** the honest manuscript this program
   can currently write is a *boundary/negative-result characterization* paper ("geometric
   similarity without causal transfer; alignment quality does not rescue it"), not a methods
   paper. NeurIPS publishes careful boundary work — but only with the novelty section written
   at the level of honesty this review demands.

---

## 6. Required-fix checklist (acceptance gates)

**Literature Agent:**
- [ ] L-1: add PPLM record; qualify the exact-prior statement
- [ ] L-2: add Self-Refine record to Family C
- [ ] L-3: Braun venue → ICLR 2025 Workshop
- [ ] L-4: verify or drop the KV-cache steering record
- [ ] L-5: drop "N2-aspirational"; unscored conjecture stays unscored

**Theory Agent:**
- [ ] T-1: compute $\|P_S \hat{v}_k\|$ from primary artifacts; caveat the numerics until then
- [ ] T-2: state the charitable rescue of A-cross
- [ ] T-3: harden A-comp determinism wording
- [ ] B-1: anisotropy/mean-centring pointer at O1
- [ ] B-2: single canonical falsification statement, cross-referenced
- [ ] E-1: full pre-registered decision tree (halt / invalid / mixed outcomes)
- [ ] E-2: halts are reportable outcomes; no rerun under the EXP067 label
- [ ] E-3: name [ASSUMPTION] A-uniform; identify the Stage A gate as its test
- [ ] E-4: SHA-256 binding guard = runtime pre/post match
- [ ] E-5: note C2 ≠ historical static condition

**Research Manager / CEO:**
- [ ] §5: resolve the EXP067 scope contradiction in writing before execution; reframe EXP067
  as boundary science; commission the operational $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$
  spec as the prerequisite for any loop experiment

---

## 7. What could still make this program interesting (adversarial reviewer's honest answer)

1. **A clean EXP067 null** (sound alignment, still zero transfer, bridge positive) would be a
   genuinely informative boundary result: it would show the representational–causal
   dissociation is *structural* at this scale, not an artifact — a real, publishable
   negative result that the steering literature (Tan, Braun) predicts but has not shown in
   this exact form.
2. **An operational, demonstrated $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop**
   that beats compute-matched baselines (self-consistency, Best-of-N, ToT) on reasoning tasks
   with $\Delta\theta = 0$ — the only path to a novelty claim, and it does not exist yet even
   as a spec.
3. **Locating the break** (QK routing vs OV transport vs MLP readout, cf. formalization Q3) —
   mechanistic follow-up science if EXP067 nulls.

What *cannot* make it interesting: a positive EXP067 C3 result presented as a novel method
(it would be well-executed CAA), or any manuscript containing the words "invented,"
"novel mechanism," or "superhuman" adjacent to the tested static mechanism.

---

*Adversarial Reviewer sign-off on the literature audit and theory deliverables is **WITHHELD**
pending the fixes in §6. The N1 verdict is endorsed. No primary artifacts were modified in
this review.*

---

## 8. Wave 2 Re-verification — 2026-09-23 (Adversarial Reviewer, re-sign pass)

The corrections integrator applied the §6 checklist. This reviewer re-verified every item
against the corrected documents and spot-checked the three new citations against the live
web. Method: line-level grep verification of each fix marker, cross-document consistency
check of the canonical falsification criterion, live web verification of PPLM / Self-Refine /
Belitsky et al., and a frozen-record audit of the surviving "must test the loop" phrasing.

### 8.1 Per-item verification

**Literature Agent:**
- [x] **L-1 CONFIRMED.** PPLM added as audit §2.23 (Dathathri et al., ICLR 2020,
  arXiv:1912.02164, 8 authors listed); exact-prior statement qualified to the required
  form in audit §7 and novelty report §4/Challenge 3; Family C taxonomy gains a
  "gradient-guided hidden-state search" slot; ranked work #6. Live-web spot-check:
  REAL — "Plug and Play Language Models," published as ICLR 2020, abstract confirms
  frozen LM + gradients from attribute model pushing hidden activations. Characterization
  stands.
- [x] **L-2 CONFIRMED.** Self-Refine added as audit §2.24 (Madaan et al., NeurIPS 2023,
  arXiv:2303.17651, 17 authors listed); Family C; plateau/blind-spot finding recorded as
  falsifier-risk for SCBI's unvalidated ℰ; ranked work #7. Live-web spot-check: REAL —
  arXiv abstract confirms single-LLM generate→feedback→refine loop, ~20% absolute gains,
  no additional training. Characterization stands.
- [x] **L-3 CONFIRMED.** Braun §2.10 venue now reads "ICLR 2025 Workshop on Foundation
  Models in the Wild," with a dated correction note (verified via arXiv comments and the
  author's publication page).
- [x] **L-4 CONFIRMED.** KV-cache steering is now a primary-source record: §2.22,
  Belitsky et al., arXiv:2507.08799, 7 authors listed. Live-web spot-check: REAL —
  "KV Cache Steering for Controlling Frozen LLMs," one-shot KV-cache intervention on
  frozen models. Low-confidence aggregation-source record eliminated.
- [x] **L-5 CONFIRMED.** Zero residual occurrences of "N2-aspirational" (grep count = 0).
  Both documents now read "unvalidated formulation distinction; unscored pending
  demonstration," with the dated removal note.

**Theory Agent:**
- [~] **T-1 PARTIAL-BY-BLOCKAGE, accepted with caveat.** The integrator attempted the
  computation honestly and documented the block: stored JSONs hold only scalar
  summaries; no vector dumps exist; recomputation needs unavailable model execution.
  The numerics table now carries the explicit "illustrative scale; genericity
  unmeasured" caveat, and the Law #13 implication (future runs must archive
  intervention vectors) is recorded. This is exactly the fallback this review
  authorized ("Until then, the numerics table must carry an explicit caveat"). The
  deterministic bound ‖P_S v‖² + 1/(d−r) is unaffected. T-1 graduates to data-grounded
  only when a future run archives raw vectors; until then the caveat is the honest
  state of the document. **Signable on this basis.**
- [x] **T-2 CONFIRMED.** "Charitable rescue of A-cross (T-2)" paragraph present (§5 of
  the proof): salvageable core stated as the uniformity claim tested by EXP067's
  Stage A gate. The strawman objection is foreclosed.
- [x] **T-3 CONFIRMED.** A-comp determinism wording hardened: the Proposition's
  expectation is over the design space of completions; the Lemma, not the Proposition,
  makes the observed draw task-arbitrary. Unmissable as required.
- [x] **B-1 CONFIRMED.** O1 carries the [NOTE — B-1] anisotropy/mean-centring pointer
  (Ethayarajh 2019; missing Jorgensen 2023 control) at the observation itself. A
  careless reader can no longer lift O1 out of context.
- [x] **B-2 CONFIRMED.** Single canonical falsification criterion in a boxed statement,
  byte-identical in the formalization (§3.3) and the EXP067 protocol (§7.0), with
  explicit cross-references in both directions. One source of truth; no inconsistency
  bug.

**EXP067 protocol:**
- [x] **E-1 CONFIRMED.** §7 replaced with a full pre-registered decision tree covering
  all required branches: (a) Stage A halt → untestable, not falsified; (b) C4 failure
  → invalid run, no conclusion; (c1–c3) mixed C3 outcomes → not confirmed, with exact
  rulings including the Law #8 negative-result branch; (d) canonical falsification
  branch; (e) C3 success branch with §1.1 novelty scope. The criterion now binds on
  every branch.
- [x] **E-2 CONFIRMED.** New §7.2: any halt IS the published outcome of EXP067, with
  full diagnostics written to the run directory; tweak-and-rerun under the EXP067
  label explicitly forbidden; any adjusted design is EXP068 with a new
  pre-registration. The Stage A gate (§3.5) and headroom gate (§5) both reference §7.2.
- [x] **E-3 CONFIRMED.** [ASSUMPTION] A-uniform named in §3.2 ("the vocabulary-renaming
  rotation estimated from entity-frame anchors acts uniformly on relational directions
  in S_h"); the Stage A gate explicitly identified as its empirical test. A-cross's
  original sin is not repeated.
- [x] **E-4 CONFIRMED.** Binding guard is the runtime pre/post match; the registered
  hash demoted to sanity check, with the environment-sensitivity rationale stated.
- [x] **E-5 CONFIRMED.** §3.4 notes C2 is head-projected and therefore not EXP066's
  historical static condition; comparisons against the historical null must note the
  changed intervention.

**CEO / §5 resolution:**
- [x] **CONFIRMED.** Protocol §1.1 reframes EXP067 as a boundary-characterization
  experiment whose outcome "cannot move the novelty needle in either direction"
  (positive C3 = well-executed CAA, i.e., N0). Protocol §9 spins the loop test out as
  a future EXP068-candidate protocol contingent on an operational
  𝒢/ℰ/𝒮/𝒯 spec — explicitly noting none exists — and requiring PPLM/ToT/Self-Refine
  as design priors and compute-matched baselines. Novelty report §4 is consistent
  with this framing. The three surviving "EXP067 must test the loop" occurrences are
  confirmed to live only in frozen historical records (two research-log entries,
  2026-09-23, and this report's own §5); the live documents carry the resolution.
  No audit-trail falsification.

### 8.2 Score: 15/15 applicable items confirmed (14 full + T-1 partial-by-blockage with authorized caveat)

No item is NOT DONE. No new objections raised by the corrections; the integrator did not
weaken any honest negative statement (spot-checked: "well-executed CAA" language intact,
N1 verdict unchanged and strengthened, N2-aspirational fully purged).

### 8.3 Sign-off

The verdicts of §0 stand. The required corrections have landed and are verified.

- Literature audit (`research/literature/audit_2026-09-23.md`, 24 verified records) —
  **ACCEPT, SIGNED 2026-09-23.**
- Novelty report (`reports/novelty_report.md`, N1 endorsed and strengthened) —
  **ACCEPT, SIGNED 2026-09-23** (adversarial signature line updated from WITHHELD).
- Boundary formalization (`theory/BOUNDARY_CLAIM_FORMALIZATION.md`) —
  **ACCEPT, SIGNED 2026-09-23.**
- Procrustes proof (`theory/proofs/procrustes_failure_analysis.md`) —
  **ACCEPT, SIGNED 2026-09-23**, with the recorded T-1 caveat: numerics illustrative
  until a future run archives raw vectors.
- EXP067 protocol (`experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md`) —
  **ACCEPT, SIGNED 2026-09-23** as a boundary-characterization pre-registration.
  Execution-ready on paper; the program-level scope resolution (§5) is in force:
  EXP067 tests the boundary, not novelty; the loop experiment awaits an operational
  𝒢/ℰ/𝒮/𝒯 spec that does not yet exist.

Residual open items (honest, not blocking): (1) T-1 full data-grounding awaits a future
compute run with vector archiving; (2) no loop spec exists yet — the Theory Agent's next
assignment per §5(2). Neither is a sign-off blocker; both are recorded as open work.

*Adversarial Reviewer — 2026-09-23. Re-verification complete. All §6 gates satisfied
(15/15). Sign-off granted. No primary artifacts were modified in this review.*
