# Law #14 Second Review of the Revised A–J Synthesis (LOG-187) — Mentor Review, 2026-09-23

**Reviewer:** ChatGPT, acting as independent scientific mentor / adversarial reviewer
**Target:** `research/synthesis/SYNTHESIS_A_J_REV_2026-09-23.md` (LOG-187)
**Verdict: Inconclusive for program adoption. Not adopted.**

> LOG-187 is substantially stronger than LOG-158. The statistical framework is
> much safer, the novelty map is materially narrower, the bridge evidence is
> properly downgraded, TTPS now has an interpreter-sufficiency control, and the
> theory-preservation kill license remains intact. But the revision does not
> clear the acceptance gate yet. Several defects are still structural rather
> than cosmetic.

Epistemic status: reviewer [INTERPRETATION]; reviewer-supplied citations must
be verified by the literature track (Law #3) before entering the record —
including the NoisyCoconut status correction, which must be re-checked against
the *current* TMLR index, not inherited from any earlier verification
timestamp.

---

## Acceptance-gate audit

| Criterion | Verdict | Finding |
| --------- | ------- | ------- |
| 1. Fresh-object re-verification | **Not supported** | The carried-forward B1/B4/B5 literature remains load-bearing but was not fully re-verified. Disclosure is honest, but the fresh-object rule requires verification or removal/narrowing of those claims. |
| 2. Current prior-art map | **Inconclusive** | The major new occupants were incorporated, but one bibliographic status is already stale: the current TMLR index lists NoisyCoconut as a June 2026 TMLR paper, while LOG-187 still calls it an arXiv preprint under review. |
| 3. Novelty boundary | **Not supported** | M15 was correctly added, but Branch S does **not require beating M15**. Therefore the new "must not be explained by newer prior art" burden is not actually enforced by the killer gate. |
| 4. Statistical framework | **Supported with one required correction** | The CI/δ-min framework, underpowered→Inconclusive rule, anti-recycling rule, and Bonferroni candidate gate are materially better. But δ_min=5pp still needs an independent practical justification rather than being anchored to previously observed bridge effects. |
| 5. Evidence interpretation | **Supported** | A1/A3/A7 are substantially more honest. The bridge is correctly treated as one option-informed steerability construction, not independent convergent evidence. |
| 6. Candidate mechanism isolation | **Not supported** | ASR is explicitly `[INCOMPLETE]`, yet §E/checklist still says 8/8 candidates have both boxes answered. That is internally contradictory. C5 also lacks a communication-bandwidth control. |
| 7. External-computation boundaries | **Supported** | TTPS is materially improved. The interpreter-only control correctly prevents external computation from being silently credited to the frozen model. |
| 8. Compute comparability | **Inconclusive** | Online/amortized FLOP separation is good, but the newly required prior-art comparators are specified only as "LTPO-style," "Meta-Reasoner-style," etc.; their exact frozen protocols/configurations are not yet fixed. |
| 9. Kill/hold architecture | **Not supported** | The kill license is strong, but there is no explicit program-level **Hold** branch for the case where candidates remain Inconclusive/blocked. More importantly, M15 can currently be beaten by a candidate's apparent Branch-S result without actually being a Branch-S requirement. |

The revision clears the **epistemic direction** of the gate, but not the **formal acceptance** of the protocol.

---

## The most important defect: M15 is not actually load-bearing

LOG-187 correctly says the next experiment does not merely demonstrate that
one of the eight mechanisms works. It adds M15 (LTPO-style for C1/DPRS;
Meta-Reasoner-style for ASR; LatentMAS-style for LCMIC; NoisyCoconut-style for
CLB) — exactly what the previous review required. But G4 Branch S still
requires only beating M2–M8. M15 is absent from the killer-success
conjunction. That creates a direct logical contradiction: **D2 says newer
prior art must be ruled out. G3 includes newer prior art. G4 can nevertheless
license novelty without beating it.** That is an adoption blocker.

**Required correction:** for every candidate with an M15 comparator, Branch S
requires beating its candidate-specific M15 comparator at the same Level-2
standard, or otherwise demonstrating a pre-registered structural distinction
that makes direct superiority scientifically inapplicable. The latter should be
rare. "Different architecture" is not sufficient. For C6, for example, a CLB
result cannot become a novelty result merely because NoisyCoconut uses a
different branch construction. The experiment has to establish what the
difference does that the prior method cannot.

---

## C1 contains an internal prior-art contradiction

CLLC's Box 1 currently says: "No competitor predicts bound-holding feedback
beating its own open-loop ablation." But the synthesis itself identifies
**Activation-LQR** as the direct prior for closed-loop feedback control,
including local linearization, Jacobian-based feedback, and tracking-error
bounds. So this cannot be a unique-support condition. The valid surviving
distinction is narrower: **relational-task control + observer/controller/plant
separation + the particular setpoint construction + whatever mechanism-level
result differentiates CLLC from A-LQR.** The Box-1 wording must not pretend
the core closed-loop-vs-open-loop observation is unoccupied.

---

## C2 still overclaims the absence of prior art

ELM says: "No competitor has cross-pass accumulating state." That is too
broad. LTPO explicitly iteratively maintains and optimizes latent thought
vectors at test time on a frozen model. LatentMAS also explicitly transfers
latent working memory between agents. The defensible claim is narrower:
**among the reviewed comparators, no identified method uses the specific
fixed-slot, externally addressable runtime scratch-buffer protocol proposed by
ELM.** That is an auditable claim. "No competitor" is not.

---

## C5 has a bandwidth confound

The LCMIC comparison uses same roles / rounds / token budget / FLOPs. But a
mid-layer residual tensor can carry vastly more raw numerical payload than a
text message with the same token count. So if LCMIC beats text debate, the
result could mean "the latent channel has much higher communication
bandwidth" rather than "latent communication is a superior computational
mechanism." LatentMAS itself demonstrates training-free latent collaboration
and shared latent working memory, so this is not a hypothetical concern.

**Required correction:** F3 needs a **communication-capacity-matched
control**, e.g. `latent full-bandwidth` vs `latent compressed to
text-equivalent payload` vs `text channel` vs `LatentMAS-style`. Otherwise the
causal claim about the *channel representation* is not isolated. This is
exactly the sort of confound Law #14 should catch before GPU.

---

## C6 is now conceptually much better

The CLB narrowing is good (intra-layer latent branching + a genuinely
non-selection merge operator). NoisyCoconut's paper is now listed in the TMLR
paper index as a June 2026 publication, so the draft's bibliographic status
must be corrected. The scientific distinction can therefore remain only at the
**merge operator** level. But the Box-1 wording contains a duplicate
("merge-vs-select ablation favors the merge operator" appears twice). More
importantly, "No competitor branches inside the pass and merges
non-selectively" is too absolute unless the literature audit actually
establishes that — replace with a reviewed-literature scope statement.

---

## ASR cannot simultaneously be incomplete and counted as accepted

LOG-187 explicitly says `policy scope [INCOMPLETE]` and "may not enter §F
culling or §G NTDP runs." But §E says "8/8 mechanism candidates ... both
answered" and the standing checklist says every H1–H5 candidate has both boxes
answered. Those statements cannot coexist. ASR is currently **not a complete
candidate specification.** The synthesis should say: **7 complete candidates +
1 pending candidate (ASR), not eligible for experimental triage until policy
scope is frozen.** A mechanical consistency requirement, not a scientific
preference.

---

## The statistical framework is substantially improved — but δ_min needs one more justification

The move from `p ≥ .05 → kill` to `effect + exact CI + practical margin →
Supported / Not supported / Inconclusive` is correct, and holding underpowered
evidence (rather than converting it into a negative result) is the crucial
improvement. The 99.375% candidate-level interval makes the candidate-level
false-positive control explicit. However, the stated reason for δ_min=5pp
includes "below the smallest bridge rescue ever observed (+10pp)" — that risks
making the practical margin depend on the corpus being tested. A defensible
δ_min should be justified **independently of observed treatment effects**,
ideally by task-level practical relevance or a fixed decision-theoretic
criterion. A sensitivity table for 2pp / 5pp / 10pp may be reported, but **one
value must be frozen before NTDP data contact.** A protocol refinement, not a
reason to redesign the experiment.

---

## The fresh-object rule is still not discharged

This is the second major blocker. The carried-forward base was correctly
disclosed as not re-verified. The reviewer's own spot verification confirms
several inherited claims are genuine: CAA is genuinely prior art for
mean-difference residual-stream steering during inference; PPLM is genuinely
inference-time latent activation steering of a frozen pretrained LM using
external attribute controllers; Self-Refine really is training-free iterative
self-feedback/refinement, reporting diminishing marginal improvement with
additional iterations plus failures driven largely by erroneous feedback; DEER
really is training-free dynamic early exit based on trial-answer confidence;
STARS really does report gain-then-collapse behavior in looped latent
reasoning and proposes training-time stabilization against it — so its use as
an excluded-by-Δθ=0 but still predictive constraint is reasonable. So the
disclosed defect does **not** mean the inherited claims are false. It means
the **Law #3 verification record is incomplete.** The clean resolution is
either: **A. verify every load-bearing inherited citation**, or **B.
remove/narrow each inherited citation whose verification is not recorded.** No
GPU required.

---

## One more current-status correction

LOG-187 says NoisyCoconut is "an arXiv preprint under review at TMLR." The
current TMLR paper index lists **NoisyCoconut: Counterfactual Consensus via
Latent Space Reasoning — Michael M. Jerge, David Evans — June 2026** alongside
its OpenReview/PDF/code links. So the revision's own literature-status
correction is now stale. LatentMAS's ICML 2026 spotlight status is
independently corroborated. Meta-Reasoner is indeed a Findings of ACL 2026
paper using contextual multi-armed bandits for adaptive inference-time
strategy selection. ∇-Reasoner is a published ICLR 2026 paper using test-time
gradient optimization of latent textual representations. This reinforces the
Law #3 rule: **bibliographic verification must be current, not merely
inherited from a previous verification timestamp.**

---

## What to preserve unchanged

A1's narrowed dissociation (raw cosine no longer treated as semantic
evidence); A3's bridge downgrade (steerability evidence from one
option-informed construction); A5's pooled equivalence reasoning; A6's refusal
to manufacture an oracle ceiling; A9's decision-flip endpoint rule; D2's five
novelty conditions; F1's conditionality requirement; H3's actual kill license;
§I's separation of L1/L2/L3. Most importantly, the revision did **not** rescue
the old theory by weakening the falsification standard.

---

## Final disposition

**LOG-187: Inconclusive for program adoption.** The revision is not rejected
scientifically. Its central framework is substantially improved. But adoption
would currently institutionalize four contradictions the nine-criterion gate is
supposed to prevent: (1) M15 is present but not enforced by Branch S; (2) ASR
is incomplete but counted as complete; (3) C5 lacks bandwidth-matched causal
isolation; (4) the fresh-object citation audit is incomplete, and
NoisyCoconut's publication status is already stale. Plus a fifth, smaller
correction: (5) CLLC's uniqueness claim must be rewritten because A-LQR
already occupies the feedback-vs-open-loop mechanism space. None of these
requires new experimental machinery. They are precisely the kind of
**map/protocol corrections** the CEO instructed the Lead to make. The lab
should remain GPU-dark. The correct next revision is not another research
program — it is a **targeted text-and-citation patch** that closes those
defects, after which the synthesis can come back for a final adoption gate.
