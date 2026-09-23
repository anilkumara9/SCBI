# Revision Edit Spec — LOG-158 Targeted Revision (Lead-authored)

**For the revision drafter (LOG-187).** Implements mentor findings #1, #4, #5,
#6, #7, #8, #9, #10 (finding #11 = preserve; #2/#3 are in
STATS_REVISION_DRAFT_2026-09-23.md; EXP023 in LOG-186). The literature
verification report (LOG-185, pending at writing time) is authoritative for
citation text — any paper it marks UNVERIFIED or PARTIALLY VERIFIED is handled
per its report, never on the mentor review's word alone.

**Output:** a NEW dated file `research/synthesis/SYNTHESIS_A_J_REV_2026-09-23.md`.
Do NOT modify the LOG-158 original or any signed artifact.

---

## E1. §D1 — narrow the novelty claim; rebuild the map (finding #1)

**Replace** the sentence "The only unoccupied sub-slot is **C′: per-instance
basis-valued search with an internal self-consistency evaluator,
transfer-validated, Δθ=0.**" with:

> **Within the reviewed literature, the remaining potentially distinct slot is
> a narrowly defined combination of per-instance activation-operator
> construction, transfer-validated internal evaluation, conditional
> computation, and Δθ=0 — not generic latent optimization, routing,
> cooperation, or branching.**

**Map additions** (use LOG-185 verified citation text; drop any UNVERIFIED
paper from the map with an explicit "not placed — unverified" note):

- **LTPO** → Family C/D-adjacent, "test-time latent optimization (frozen)":
  parameter-free test-time optimization of latent thought vectors on a frozen
  LLM (verify details against LOG-185). Occupies the *general*
  "frozen model + per-instance latent optimization + internal signal" slot.
- **Meta-Reasoner** → Family C-adjacent, "test-time strategy routing":
  dynamic reasoning-strategy selection at inference time via contextual
  multi-armed bandits (verify). Occupies "test-time-discovered strategy
  routing" as a general slot.
- **LatentMAS** → new Family I, "training-free latent multi-agent
  collaboration": shared latent working memory between agents (verify; ICML
  2026). Occupies "inter-instance latent exchange" generally.
- **NoisyCoconut** → Family C/D-adjacent, "training-free latent
  branching + consensus": inference-time noise injection into latent
  trajectories, multiple latent paths, aggregation/consensus (verify; TMLR
  June 2026). Occupies "latent branching + aggregation" generally.
- **RISER** → adjacent EXCLUDED art: adaptive activation steering with a
  dynamically selected/composed vector library via a *trained RL router* —
  violates Δθ=0, therefore not an equivalence threat; retained in the map as
  adjacent excluded method (Findings of ACL 2026 — verify).
- **∇-Reasoner:** confirm ICLR 2026 venue from LOG-185; keep Family D.
- **Activation-LQR:** update venue to **ICML 2026** (the mentor states it is
  now in the proceedings — confirm via LOG-185; if the proceedings listing
  does not verify, keep "arXiv Apr 2026" and tag the ICML claim UNVERIFIED).
  §B5's phrasing "published 2026 result" replaces any "under-review preprint"
  language only if verified.

**§B4/B5/B6 consistency:** anywhere the synthesis treats H1/DPRS, H4/ASR,
H5a/LCMIC, H5b/CLB slots as "unoccupied," narrow per E2–E5 below.

## E2. H1/DPRS — narrow; add LTPO comparator (findings #1, #6-table)

- **Novelty paragraph:** DPRS's claim is narrowed from "no competitor searches
  readout space dynamically" to "**readout-space perturbation search
  specifically**": discrete perturbation search over the model's own top-k
  confusion pairs with an internal evaluator and the §F1 conditionality
  check. LTPO (verify) occupies general per-instance latent optimization;
  the surviving distinction is readout-space discreteness × internal
  evaluator × conditionality.
- **Forced comparator:** add LTPO as a required comparator for H1-family
  candidates (C1, DPRS) at matched compute in §G — as a named forced
  baseline for the H1 instantiations (not necessarily a full M-condition for
  all candidates; the drafter places it as M15-or-named-comparator with the
  FLOP-accounting rules of E8).
- **Box 1:** append "…and beats LTPO-style latent optimization at matched
  compute on the relational task (the general slot is occupied; the
  readout-space-specific claim must beat its occupant)."

## E3. H4/ASR — Meta-Reasoner comparator; policy-scope specification (findings #1, #8)

- **Novelty paragraph:** "test-time-discovered strategy routing" is not an
  empty slot (Meta-Reasoner, verify). ASR's surviving distinction must be
  stated strictly: a *test-time-learned allocation policy* (bandit over
  strategies with an internal target-free reward) vs Meta-Reasoner's
  contextual bandit over a strategy menu — and ASR must beat or structurally
  differ from Meta-Reasoner, not reimplement it with a different menu.
- **Forced comparator:** Meta-Reasoner added as a required comparator for
  ASR at matched compute.
- **Policy-scope specification (new, pre-registered):** ASR must declare
  `policy scope ∈ {per-instance, per-episode, test-stream}`; state explicitly
  whether information from example i may affect example i+1; if any
  cross-instance state exists, define the formal online-adaptation boundary
  (what carries over, what resets per instance/episode, and the Law-#7
  audit of carried state). Without this declaration the adaptivity claim is
  inadmissible — mark the current ASR spec [INCOMPLETE] on this point until
  declared.
- **Box 1:** append the Meta-Reasoner-beats-or-differs condition.

## E4. H5a/LCMIC — rewrite; remove the false sentence (findings #1, #5)

- **DELETE** the Box-1 sentence "No competitor uses inter-instance latent
  exchange" and the §E summary/Box 1 statement to the same effect. This is
  the Law-#14 kill the mentor ordered — it must not survive in any
  paraphrase.
- **Rewrite the novelty paragraph:** "LCMIC as 'latent-channel cooperation'
  is a prior-art family after LatentMAS (verify). The surviving hypothesis is
  formulation-level, not 'latent cooperation is new': **same frozen backbone
  + causal residual exchange + verifier/arbiter separation +
  relational-task intervention**. The claim is that *this formulation* beats
  text-channel debate/MoA and LatentMAS-style shared-memory collaboration at
  matched compute on the relational task — not that latent cooperation is
  novel."
- **Box 1:** rewrite the unique-support observation so it is not predicted by
  LatentMAS: latent-channel beats text-only AND beats a LatentMAS-style
  shared-latent-memory ablation (same roles/rounds/budget) AND the critic's
  latent doubt predicts proposer errors above chance. If the LatentMAS-style
  ablation matches, LCMIC reduces to prior art — culled.
- **Forced comparator:** LatentMAS-style collaboration added as a required
  comparator arm for C5 (or as the §F3 fourth arm).

## E5. H5b/CLB — narrow; NoisyCoconut baseline (findings #1, #6)

- **Novelty paragraph:** "CLB branches in latent space and merges
  trajectories" is occupied (NoisyCoconut, verify). The surviving hypothesis:
  "**intra-forward/intra-layer latent branching followed by a merge operator
  that computes something irreducible to candidate selection.**"
- **Baseline:** the discriminating test's baseline becomes
  **NoisyCoconut-style latent branching/consensus**, not just Best-of-4.
  Box 1's "~2F beats Best-of-4 at 4F" becomes "~2F beats Best-of-4 at 4F AND
  beats NoisyCoconut-style branching/consensus at matched compute AND the
  merge-vs-select ablation favors the merge operator (merge ≠ argmax/
  selection — the decisive test)."
- **Box 2:** add "or the merge operator's advantage vanishes against the
  NoisyCoconut-style baseline → the operator adds nothing over occupied art;
  withdrawn."

## E6. A1 — downgrade the cosine inference (finding #4)

**Replace** "[INFERENCE]/[INTERPRETATION]: ≈0.7 raw cosine shows the contrast
directions encode something shared across disjoint vocabularies (not noise),
but that shared structure is causally inert under static additive steering."
with:

> [INFERENCE]/[INTERPRETATION]: raw geometric similarity (≈0.7 cosine) is
> **observed**; semantic common structure is **not established** until
> anisotropy-controlled nulls support it (cf. §B1: anisotropy inflates
> cosine similarity — the two statements cannot both carry strength, and the
> anisotropy caveat wins). The licensed dissociation is narrower: geometric
> similarity without causal transfer under static injection. No mechanism
> claim above L1 is licensed by the cosine value.

The [FACT]/[OBSERVATION] sentence (the numbers) is untouched.

## E7. A3/A7/C1 — reframe as readout-path steerability (finding #4)

- **A3:** the "verified four times" framing stays as [FACT], but the
  interpretation is reframed: "the same option-informed construction
  (normalize(E[target]−E[foil])) repeatedly produces causal decision changes
  — strong evidence of **steerability of the readout path**, not independent
  confirmations of an autonomous output-side cognitive mechanism. The five
  demonstrations share one construction confound — the exact confound K1/K3
  are designed to expose."
- **A7:** replace "Fifth experiment converging on the output-side reading"
  with "Fifth demonstration that the option-informed construction's causal
  power localizes outside the tested concept subspace — a localization clue
  for readout-path steerability (still Underdetermined as a causal
  demonstration)."
- **C1:** replace "five experiments converge on 'the transferable direction
  lives output-side'" with the steerability framing above.
- **Add (strengthening, per the mentor):** state explicitly that this
  reframing *raises* the load-bearing weight of K1/K3 — they are not minor
  diagnostics; a K1 tilt-verdict collapses the entire output-side
  interpretive stack. (The current §H6 says this; the revision makes §C
  consistent with it instead of double-counting the bridge as converging
  evidence.)

## E8. H3/TTPS — interpreter capability boundary + interpreter-only baseline (finding #7)

Add a pre-registered **interpreter capability boundary** to C3/TTPS:

- Fixed instruction set (enumerated in the pre-registration) →
- bounded operation count per item (pre-registered cap) →
- no external data at execution time →
- no task solver hidden in primitives (each primitive's capability
  documented; a primitive that alone solves the task class is forbidden) →
- **interpreter-only control cannot solve the task** (pre-registered check).

Add an **interpreter-only baseline** arm: the interpreter executing a
degenerate/fixed program (or the DSL's primitives composed without model
synthesis) at matched operation budget. **Decision rule:** L3 is licensed
only if the interpreter-only control fails the task while TTPS succeeds;
if the interpreter alone succeeds, the "new capability" belongs to the
interpreter (a programmable computer the model was given), not to the
frozen model — verdict Not supported for L3 ("new computation" ≠ "new
capability of the frozen model"). Box 1 gains the interpreter-only-control
condition; Box 2 gains the interpreter-sufficiency kill.

## E9. FLOP accounting — online vs amortized (finding #9)

Add to §G2/G3 a **compute-accounting specification** (binding on all
baselines and candidates):

- Every condition reports two numbers: **(a) online inference FLOPs per
  item** (everything executed after the test item is observed) and
  **(b) one-time/amortized preparation FLOPs** (A-LQR Jacobian computation,
  ∇-Reasoner backward passes, reward-model training/inference, TTPS
  interpreter operations, bandit updates, latent-memory movement,
  latent-agent communication, cached-gain construction).
- "Matched compute" = matched **(a) online inference FLOPs per item**;
  **(b)** is reported separately, amortized over the evaluation set with the
  amortization denominator stated — never hidden, never mixed into (a).
- Track-11's bigger-frozen-model rule is restated under this accounting:
  both frames (training FLOPs amortized vs excluded) reported, neither
  hidden — already in §G2; the revision makes the two-number rule universal.

## E10. Standing burden-of-proof note (new; mentor's main finding)

Add a boxed standing note in §D (after D2), recorded as program guidance:

> **Changed burden of proof (standing):** the next experiment does not merely
> demonstrate that one of the eight mechanisms works. It must demonstrate
> that what works is **not already explained by the newer prior art**
> (LTPO, LatentMAS, NoisyCoconut, Meta-Reasoner — LOG-185 verified). A
> positive result that a 2026 occupant predicts at matched compute is a
> replication of prior art, not a novelty result — verdict Not supported for
> the novelty claim (engineering value assessed separately under the
> demote-to-engineering logic).

## E11. Preserved sections (finding #11 — DO NOT WEAKEN)

A4, A5, A6, A9, D2 (all five boundary conditions), F1's structure, H3's
license, §I's definition and grades. The revision narrows claims and
corrects decision rules; it never softens a kill, a narrow license, or a
falsifier. In particular: the §B track-7 verdict ("licensed to conclude
SCPM is a dead end as a mechanism program") stays at full strength; the
§H3 kill trigger stays executable without re-approval; §I's "rules out the
entire current corpus" note stays.

## E12. Mechanical consistency pass

- The §E summary table: update the H5a/H5b "Distinctive computation" cells
  to the narrowed formulations; add the new forced comparators to the
  relevant rows.
- §D2 condition 3's baseline list: add LTPO (for H1-family), Meta-Reasoner
  (for H4), LatentMAS-style collaboration (for H5a), NoisyCoconut-style
  branching/consensus (for H5b) as candidate-specific forced comparators.
- Appendix R: add R(h) recording this revision — what the mentor's review
  changed and why, per finding, with the LOG-185 verification outcomes.
- The standing-law compliance checklist: add items for the hierarchical
  alpha budget, the CI+margin rule, and the changed burden of proof; leave
  unchecked for the mentor.
- Epistemic double-labeling and verdict-category discipline continue
  unchanged throughout.
