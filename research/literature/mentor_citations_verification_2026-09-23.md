# Verification of Mentor-Supplied Citations (LOG-158 Review §1) — LOG-185

**Track:** Literature | **Date:** 2026-09-23 | **Analyst:** Literature Track
**Mandate:** Law #3 (never fabricate citations; unverified = UNVERIFIED).
Epistemic status of every entry below is [FACT — fetched and quoted]; only the
mentor's original claim column is [INTERPRETATION — reviewer-supplied].
Nothing enters the novelty map except VERIFIED records. The revised synthesis
may cite a VERIFIED record as an adjacent/precedent paper; UNVERIFIED or
PARTIALLY VERIFIED records must carry their qualifications.

**Verdict summary:** 5 VERIFIED, 2 PARTIALLY VERIFIED (both partial only on
venue-status sub-claims — the mechanisms themselves are real papers with the
claimed mechanisms), 0 UNVERIFIED.

| # | Citation | Verdict |
|---|----------|---------|
| 1 | LTPO (arXiv:2510.04182) | **VERIFIED** |
| 2 | Meta-Reasoner (arXiv:2502.19918; Findings of ACL 2026) | **VERIFIED** |
| 3 | LatentMAS (arXiv:2511.20639; ICML 2026) | **VERIFIED** |
| 4 | NoisyCoconut (arXiv:2605.08221) | **PARTIALLY VERIFIED** — mechanism verified; "TMLR June 2026 publication" sub-claim false as stated (under review, decision pending) |
| 5 | RISER (2026.findings-acl.226) | **VERIFIED** |
| 6 | ∇-Reasoner (arXiv:2603.04948; ICLR 2026) | **VERIFIED** |
| 7 | Activation-LQR (arXiv:2604.19018; ICML 2026 listing confirmed) | **VERIFIED** |

Two material corrections to the mentor's claims that the revised synthesis must
respect: (a) NoisyCoconut must be cited as an **arXiv preprint under review at
TMLR**, not as a published TMLR paper; (b) ∇-Reasoner's venue is confirmed
(ICLR 2026) and its 80.4% MATH-500 figure is confirmed in the paper text
(Qwen-2.5-7B-Instruct); RISER's trained component is a lightweight external
router while the LLM backbone is frozen — the review's "violates Δθ=0" framing
needs the nuance stated in §5.

---

## 1. LTPO — Latent Thought Policy Optimization

**(a) The review's claim (verbatim):** "LTPO is parameter-free, test-time
optimization of latent thought vectors on a frozen LLM, using an intrinsic
confidence reward in an online loop. ([arXiv](https://arxiv.org/abs/2510.04182))"

**(b) What was found.**
- **Title:** Thinking on the Fly: Test-Time Reasoning Enhancement via Latent
  Thought Policy Optimization
- **Authors:** Wengao Ye, Yan Liang, Lianlei Shan
- **arXiv:** 2510.04182 (cs.CL); submitted 5 Oct 2025, v4 last revised 26 Jan 2026.
  No conference venue listed on the arXiv page — cite as arXiv preprint.
- **Abstract mechanism (quoted verbatim):** "we introduce Latent Thought Policy
  Optimization (LTPO), a **parameter-free framework that enhances LLM reasoning
  entirely at test time, without requiring model parameter updates. LTPO treats
  intermediate latent 'thought' vectors as dynamic parameters that are actively
  optimized for each problem instance. It employs an online policy gradient
  method guided by an intrinsic, confidence-based reward signal computed directly
  from the frozen LLM's own output distributions**, eliminating the need for
  external supervision or expensive text generation during optimization."

**(c) Verdict: VERIFIED.** Every sub-claim checks out: parameter-free,
test-time, per-instance optimization of latent thought vectors, frozen LLM,
intrinsic confidence reward, online loop (online policy gradient).

**(d) Overlap with our candidates (own words from the abstract):** LTPO
occupies the mechanism family "frozen model + per-instance optimization of a
continuous latent representation + intrinsic/internal evaluation signal +
online update loop." Our H1/DPRS (dynamic per-instance representation search)
shares this exact signature: the only structural difference visible at the
abstract level is that LTPO's optimized object is a latent *thought vector*
optimized by policy gradient, while DPRS's claimed object is an
activation-space basis/perturbation operator found by search. The mentor's
prescription stands: DPRS must be narrowed to readout-space perturbation
search (or another specific distinction) and cannot claim the general slot.

**(e) Suggested citation text for the revised synthesis:**
> Latent Thought Policy Optimization (LTPO) (Ye, Liang & Shan, arXiv
> 2510.04182, 2025) demonstrates that intermediate latent "thought" vectors
> can be optimized per problem instance at test time, with an online policy
> gradient guided by an intrinsic confidence signal from the frozen LLM's own
> output distributions, requiring no model parameter updates. LTPO therefore
> occupies the general slot of per-instance latent optimization under a frozen
> backbone with an internal signal; any DPRS novelty claim must be narrowed to
> a distinction the paper does not cover, such as readout-space perturbation
> search specifically.

---

## 2. Meta-Reasoner — Dynamic Guidance for Optimized Inference-time Reasoning

**(a) The review's claim (verbatim):** "Meta-Reasoner already dynamically
changes reasoning strategy at inference time using contextual multi-armed
bandits and reports improvements under the same-compute setting.
([ACL Anthology](https://aclanthology.org/people/yuan-sui/))"

**(b) What was found.** The review supplied only an author page; the paper was
located independently via web search.
- **Title:** Meta-Reasoner: Dynamic Guidance for Optimized Inference-time
  Reasoning in Large Language Models
- **Authors:** Yuan Sui, Yufei He, Tri Cao, Simeng Han, Yulin Chen, Bryan Hooi
  (National University of Singapore; Yale University)
- **arXiv:** 2502.19918 (cs.AI/cs.LG); submitted 27 Feb 2025, v6 last revised
  7 May 2026. arXiv page comments: "Accepted by ACL'2026".
- **Venue (independently confirmed):** Findings of the Association for
  Computational Linguistics: ACL 2026 — https://aclanthology.org/2026.findings-acl.649/
  (pages 13268–13286, San Diego, July 2026), DOI 10.18653/v1/2026.findings-acl.649.
  The first author's own site (yuan-sui.com) lists it as "ACL Findings, 2026".
- **Abstract mechanism (quoted verbatim):** "It optimizes the inference process
  by **dynamically adapting reasoning strategies in real-time. Our approach
  employs contextual multi-armed bandits (CMABs) to learn an adaptive policy.**
  It learns to evaluate the current state of LLM's reasoning and determine
  optimal strategy that is most likely to lead to a successful outcome during
  inference, like **whether to backtrack, switch to a new approach, or restart
  the problem-solving process**." — "Results show that our method outperform
  previous SOTA methods by 9-12% in accuracy, while **reducing inference time by
  28-35% under the same compute budget**."

**(c) Verdict: VERIFIED.** Dynamic strategy change at inference time ✓;
contextual multi-armed bandits ✓; improvements under same-compute budget ✓
(abstract's phrasing: 28–35% inference-time reduction under the same compute
budget, 9–12% accuracy over previous SOTA).

**(d) Overlap with our candidates (own words from the abstract):** Meta-Reasoner
occupies "test-time-discovered strategy routing": a CMAB learns an adaptive
policy from the LLM's current reasoning state (compact progress report) and
selects high-level strategies (backtrack / change decomposition / restart)
during inference. Our H4/ASR (adaptive strategy routing via a test-time bandit
that discovers the strategy policy) is the same mechanism family. The
surviving ASR distinction must therefore be structural (e.g., per-instance
closed policy scope with no cross-instance learning, or a mechanism-level
difference such as activation-space rather than CoT-step routing) — and it
must beat or structurally differ from Meta-Reasoner, as the review requires.
Also directly relevant to the review's finding §8: the bandit's learning scope
(where the bandit learns) is a pre-registration question Meta-Reasoner forces
on ASR — policy scope must be pinned as per-instance / per-episode / test-stream.

**(e) Suggested citation text for the revised synthesis:**
> Meta-Reasoner (Sui et al., Findings of ACL 2026) implements test-time
> strategy routing: a contextual multi-armed bandit observes a compact progress
> report on the LLM's current reasoning state and selects high-level strategies
> (backtrack, change decomposition scheme, restart), reporting 9–12% accuracy
> gains and 28–35% inference-time reduction under the same compute budget.
> Adaptive strategy selection at inference time is therefore an occupied slot;
> ASR must be licensed only against a stricter, pre-registered distinction
> (mechanism-level difference and explicit per-instance/per-episode/test-stream
> policy scope), not against adaptive routing in general.

---

## 3. LatentMAS — Latent Collaboration in Multi-Agent Systems

**(a) The review's claim (verbatim):** "LatentMAS is explicitly training-free
latent collaboration with shared latent working memory between agents. It is
an ICML 2026 paper and directly occupies latent inter-agent communication.
([arXiv](https://arxiv.org/abs/2511.20639))"

**(b) What was found.**
- **Title:** Latent Collaboration in Multi-Agent Systems
- **Authors:** Jiaru Zou, Ruizhong Qiu, Gaotang Li, Xiyuan Yang, Katherine
  Tieu, Pan Lu, Ke Shen, Hanghang Tong, Yejin Choi, Jingrui He, James Zou,
  Mengdi Wang, Ling Yang
- **arXiv:** 2511.20639 (cs.CL); submitted 25 Nov 2025, v4 last revised 3 Aug 2026.
- **Venue (independently confirmed):** ICML 2026 — the authors' official
  repository (github.com/Gen-Verse/LatentMAS) announces acceptance as an
  **ICML 2026 spotlight** on 2026-05-01; the paper is entry 3017 in the ICML
  2026 Downloads/proceedings listing at https://icml.cc/Downloads/2026.
- **Abstract mechanism (quoted verbatim):** "we introduce LatentMAS, an
  **end-to-end training-free framework that enables pure latent collaboration
  among LLM agents**. In LatentMAS, **each agent first performs auto-regressive
  latent thoughts generation through last-layer hidden embeddings instead of
  text. Then, a shared latent working memory preserves and transfers each
  agent's internal representations and latent thoughts, ensuring lossless
  information exchange without re-encoding.**"

**(c) Verdict: VERIFIED.** Training-free ✓; latent collaboration ✓; shared
latent working memory between agents ✓; ICML 2026 (spotlight) ✓.

**(d) Overlap with our candidates (own words from the abstract):** LatentMAS
directly occupies inter-agent latent exchange: agents generate latent thoughts
from last-layer hidden embeddings and pass internal representations through a
shared latent working memory — without text mediation and without training.
Our H5a/LCMIC ("latent-channel multi-instance cooperation") claims
inter-instance latent exchange; the synthesis's sentence "No competitor uses
inter-instance latent exchange" is false as written and must be removed, as
the mentor rules. Any surviving LCMIC claim must be formulation-level (e.g.,
same frozen backbone + causal residual exchange + verifier/arbiter separation
+ relational-task intervention), and "latent cooperation" as such belongs to
prior art.

**(e) Suggested citation text for the revised synthesis:**
> LatentMAS (Zou et al., ICML 2026 spotlight) is a training-free multi-agent
> framework in which agents generate autoregressive latent thoughts from
> last-layer hidden embeddings and exchange internal representations through a
> shared latent working memory — pure latent collaboration with no text
> mediation. Latent inter-agent communication is therefore prior art, and the
> "no competitor uses inter-instance latent exchange" claim is retracted.
> LCMIC survives only as a formulation-level claim (e.g., same frozen backbone
> with causal residual exchange plus verifier/arbiter separation on
> relational tasks), to be adjudicated as a meaningful formulation difference,
> not as a new capability.

---

## 4. NoisyCoconut — Counterfactual Consensus via Latent Space Reasoning

**(a) The review's claim (verbatim):** "NoisyCoconut is a training-free
inference-time method that injects noise into latent trajectories, produces
multiple latent paths, and aggregates them. It is listed by TMLR in June 2026.
([TMLR](https://jmlr.org/tmlr/papers/))"

**(b) What was found.** The review supplied only the TMLR index; the paper was
located independently via web search.
- **Title:** NoisyCoconut: Counterfactual Consensus via Latent Space Reasoning
- **Authors:** Michael Jerge, David Evans (University of Virginia)
- **arXiv:** 2605.08221 (cs.LG); submitted 6 May 2026. (Note: an OpenReview
  record also references arXiv ID 2507.06203 — an unresolved discrepancy in
  that secondary index; the canonical current record is 2605.08221.)
- **Venue status (checked against primary sources):** the OpenReview TMLR
  submissions page lists it as **"Under review for TMLR" / "Decision pending
  for TMLR"** (TMLR Paper7067; submitted 19 Jan 2026, modified 09 May 2026);
  the author's own repository (github.com/mmjerge/noisycoconut) links the
  OpenReview forum (id=5aatZPiCv8, under review) alongside the arXiv preprint.
  The direct forum page could not be loaded (Cloudflare verification wall).
  **It is NOT a published TMLR paper.**
- **Abstract mechanism (quoted verbatim):** "a **novel inference-time method**
  that enhances large language model (LLM) reliability by manipulating internal
  representations. **Unlike fine-tuning methods that require extensive
  retraining, NOISYCOCONUT operates directly on model representations during
  inference and requires no retraining. Rather than training models to reason in
  latent space, we inject controlled noise into latent trajectories to generate
  diverse reasoning paths. Agreement among these paths provides a confidence
  signal**, enabling models to abstain when uncertain." The author's repo
  documents the mechanism: per-branch Gaussian noise added to the initial
  hidden state (K perturbed branches), latent reasoning per branch, a pairwise
  trajectory-diversity metric D_K, and output aggregation by majority or
  logit-probability-mass (confidence-weighted) voting.

**(c) Verdict: PARTIALLY VERIFIED.** Mechanism verified in full: training-free,
inference-time, noise injection into latent trajectories, multiple latent
paths, diversity measurement, aggregation/consensus ✓. **The venue sub-claim
is wrong as stated:** "listed by TMLR in June 2026" implies a published TMLR
paper; the primary record shows the paper is **under review / decision
pending at TMLR**, i.e., an arXiv preprint under review. Cite it as such —
never as a published TMLR 2026 paper unless and until its acceptance is
verified.

**(d) Overlap with our candidates (own words from the abstract):** NoisyCoconut
occupies frozen-model inference-time latent perturbation, multiple latent
trajectories with a measured path-diversity statistic, and consensus
aggregation — no retraining, no training-data access, no parameter
modification. Our H5b/CLB claims "latent branching + merge": that space is
occupied. The surviving CLB claim, per the mentor's narrowing, must be the
intra-layer fork with a genuinely non-selection merge operator — and, critically,
the paper's own aggregation modes are *selection-adjacent* (majority voting,
confidence-weighted voting), so the decisive discriminator is whether our
merge computes something irreducible to candidate selection. NoisyCoconut-style
branching/consensus must now be a baseline, not just Best-of-4.

**(e) Suggested citation text for the revised synthesis:**
> NoisyCoconut (Jerge & Evans, arXiv 2605.08221, 2026; under review at TMLR —
> **not** a published TMLR paper) injects controlled Gaussian noise into latent
> trajectories at inference time to generate K diverse reasoning paths from a
> common initial hidden state, measures pairwise trajectory diversity, and
> aggregates via majority or confidence-weighted voting, with no retraining or
> parameter modification. Frozen-model latent branching with aggregation is
> therefore occupied prior art. CLB's surviving novelty is narrowed to an
> intra-layer latent fork whose merge operator is provably irreducible to
> candidate selection, with NoisyCoconut-style branching/consensus as a forced
> baseline.

---

## 5. RISER — Orchestrating Latent Reasoning Skills for Adaptive Activation Steering

**(a) The review's claim (verbatim):** "There is also RISER, published in
Findings of ACL 2026, which performs adaptive activation steering with a
dynamically selected/composed vector library. It uses a trained RL router, so
it violates the Δθ=0 boundary and is therefore not an equivalence threat. But
it absolutely belongs in the novelty map as an adjacent excluded method.
([ACL Anthology](https://aclanthology.org/2026.findings-acl.226/))"

**(b) What was found.**
- **Title:** RISER: Orchestrating Latent Reasoning Skills for Adaptive
  Activation Steering (acronym expands to "Router-based Intervention for
  Steerable Enhancement of Reasoning")
- **Authors:** Wencheng Ye, Xiaoyang Yuan, Yi Bin, Hengyu Jin, Liang Peng,
  Pengpeng Zeng, Heng Tao Shen
- **Venue (confirmed):** Findings of the Association for Computational
  Linguistics: ACL 2026 — https://aclanthology.org/2026.findings-acl.226/
  (pages 4627–4644, San Diego, July 2026), DOI 10.18653/v1/2026.findings-acl.226.
- **Abstract mechanism (quoted verbatim):** "we propose RISER ..., a
  **plug-and-play intervention framework that adaptively steers LLM reasoning
  in activation space. RISER builds a library of reusable reasoning vectors
  and employs a lightweight Router to dynamically compose these vectors for
  each input. The Router is optimized via reinforcement learning under
  task-level rewards**, enabling the emergent and compositional activation of
  latent cognitive primitives."

**(c) Verdict: VERIFIED.** Venue ✓; adaptive activation steering with a
dynamically composed vector library ✓; trained RL router ✓. **Boundary
nuance the revised synthesis should state precisely:** the abstract describes
RISER as "plug-and-play" with a *lightweight* router that steers a base model —
the trained object is the router, not the LLM backbone (whose weights are not
described as updated). The review's "violates the Δθ=0 boundary" holds under
the program's Law #6 reading (no adapters/external trained weights in core
SCBI), but the honest record is: RISER trains an *external router module* over
a frozen backbone, not the backbone itself. It is excluded adjacent art
because any trained component violates the program's standing law, not
because the LLM weights are fine-tuned.

**(d) Overlap with our candidates:** RISER is adjacent, not overlapping: it is
the closest published analog of *adaptive activation steering with a
dynamically composed intervention* — the "dynamic selection/composition"
mechanism ASR-adjacent work must distinguish itself from — while remaining
outside the Δθ=0 boundary because of its trained router. It anchors the
novelty map's excluded-adjacent column.

**(e) Suggested citation text for the revised synthesis:**
> RISER (Ye et al., Findings of ACL 2026) is the closest adjacent method:
> a plug-and-play framework that builds a library of reusable reasoning
> vectors and uses a lightweight Router — optimized via reinforcement learning
> under task-level rewards — to dynamically compose them per input, steering
> LLM reasoning in activation space (3.4–6.5% average zero-shot accuracy gains).
> Because its router is trained, RISER is excluded from the Δθ=0 program
> boundary and is retained in the map strictly as adjacent art: it shows that
> dynamic vector composition is publishable steering research, and any
> Δθ=0-respecting variant must identify exactly what the trained router
> contributes that a parameter-free mechanism cannot.

---

## 6. ∇-Reasoner — Test-Time Gradient Descent in Latent Space

**(a) The review's claim (verbatim):** "the two strongest 'adjacent possible'
citations check out: ∇-Reasoner is an ICLR 2026 paper using test-time gradient
optimization of latent/textual representations ... test-time gradient descent
on token logits (Differentiable Textual Optimization), frozen model, reward
model; 80.4% MATH-500. ([arXiv](https://arxiv.org/abs/2603.04948))"

**(b) What was found.**
- **Title:** ∇-Reasoner: LLM Reasoning via Test-Time Gradient Descent in
  Latent Space
- **Authors:** Peihao Wang, Ruisi Cai, Zhen Wang, Hongyuan Mei, Qiang Liu,
  Pan Li, Zhangyang Wang
- **arXiv:** 2603.04948 (cs.LG); submitted 5 Mar 2026. (The arXiv page itself
  carries no venue; the venue is corroborated below.)
- **Venue (independently confirmed):** ICLR 2026 — the OpenReview listing
  carries the header "Published as a conference paper at ICLR 2026"; mirrored
  in an independent workshop PDF (pml4sc.github.io, June 2026) and a secondary
  explainer (toknow.ai, March 2026). Three independent sources agree.
- **Abstract mechanism (quoted verbatim):** "we propose ∇-Reasoner, an
  iterative generation framework that **integrates differentiable optimization
  over token logits into the decoding loop to refine the policy on the fly**.
  Our core component, **Differentiable Textual Optimization (DTO), leverages
  gradient signals from both the LLM's likelihood and a reward model to refine
  textual representations**." — "Theoretically, we show that performing
  inference-time gradient descent in the sample space to maximize reward is
  **dual to aligning an LLM policy via KL-regularized reinforcement
  learning**."
- **80.4% figure (verified in the paper text):** "on Qwen-2.5-7B-Instruct, our
  method scores **80.4% on MATH-500** and 56.8% on AMC" (vs 71.2% greedy
  decoding baseline). The reward models used are Skywork-Reward-V2-Qwen3
  (4B/8B); the method requires a reward model and model-likelihood gradients.

**(c) Verdict: VERIFIED.** ICLR 2026 venue ✓ (three independent corroborations);
test-time gradient descent on token logits via DTO ✓; frozen model (inference
only, no training) ✓; reward model ✓; 80.4% MATH-500 ✓ (on
Qwen-2.5-7B-Instruct, Nmax=8).

**(d) Overlap with our candidates:** ∇-Reasoner is the strongest "adjacent
possible" precedent for first-order inference-time optimization of internal
representations under a frozen backbone — directly relevant to the adaptive-loop
program (EXP068/EXP070): it shows test-time gradient-based representation
refinement is real, published, and effective (over 20% gains on math
reasoning). It differs structurally from our loop candidates by operating on
token logits in the decoding loop with an external reward model (and it uses
backward passes through the frozen model — a compute-accounting point for the
online-vs-amortized FLOPs formalism the review requires).

**(e) Suggested citation text for the revised synthesis:**
> ∇-Reasoner (Wang et al., ICLR 2026) applies differentiable optimization to
> token logits inside the decoding loop — Differentiable Textual Optimization
> (DTO) refines textual representations using gradient signals from the LLM's
> likelihood and a reward model, shown to be dual to KL-regularized RL
> alignment, reaching 80.4% on MATH-500 with Qwen-2.5-7B-Instruct (vs 71.2%
> greedy). It is the strongest published precedent for first-order
> representation optimization at inference time under a frozen model, and
> stands as the forced comparator for any adaptive-loop candidate: the loop
> must show what it achieves that per-instance gradient optimization of logits
> does not, under matched online compute.

---

## 7. Activation-LQR — Closed-Loop Activation Control via Layer-wise Jacobians

**(a) The review's claim (verbatim):** "Activation-LQR is an ICML 2026 paper
implementing closed-loop activation control with layer-wise Jacobians."
Plus §9: "A-LQR explicitly uses layer-wise Jacobians and control computation
([arXiv](https://arxiv.org/abs/2604.19018))." Plus the closing update:
"**Activation-LQR is now listed in ICML 2026's proceedings**, so §B5 can
accurately describe it as a published 2026 result rather than merely an
under-review preprint. ([ICML](https://icml.cc/Downloads/2026))"

**(b) What was found.**
- **Title:** Local Linearity of LLMs Enables Activation Steering via
  Model-Based Linear Optimal Control ("Activation-LQR" is the review's
  shorthand; the actual title does not contain "LQR" — note for citation hygiene.)
- **Authors:** Julian Skifstad, Xinyue Annie Yang, Glen Chou
- **arXiv:** 2604.19018 (cs.LG/cs.AI/cs.SY); submitted 21 Apr 2026.
- **Abstract mechanism (quoted verbatim):** "we show empirically that, despite
  the nonlinear structure of transformer blocks, **layer-wise dynamics across
  multiple LLM architectures and scales are well-approximated by
  locally-linear models**. Exploiting this property, we **model LLM inference
  as a linear time-varying dynamical system and adapt the classical linear
  quadratic regulator to compute feedback controllers using layer-wise
  Jacobians, steering activations toward desired semantic setpoints in
  closed-loop with minimal computational overhead and no offline training. We
  also derive theoretical bounds on setpoint tracking error**, enabling formal
  guarantees on steering performance."
- **ICML 2026 listing (verified directly):** the paper appears as entry 3288
  in the official ICML 2026 Downloads/proceedings listing at
  https://icml.cc/Downloads/2026 (title match, located via page find). The
  review's claim is confirmed.

**(c) Verdict: VERIFIED.** Layer-wise Jacobian linearization of transformer
dynamics (LTV model) ✓; LQR feedback controllers ✓; closed-loop steering toward
setpoints ✓; tracking-error bounds ✓; no fine-tuning / no offline training ✓;
ICML 2026 proceedings listing ✓ (verified on icml.cc/Downloads/2026).

**(d) Overlap with our candidates:** Activation-LQR is the strongest published
precedent for the **adaptive-loop** family the program is now betting on
(EXP068/EXP070): model-based, closed-loop, per-step control of activations
using locally-linear dynamics — i.e., an online feedback loop over internal
representations with formal guarantees. It differs from our candidates by
operating layer-wise with Jacobian-computed LQR controllers rather than
per-instance operator construction, and by targeting semantic setpoints for
behavior control (toxicity, truthfulness, refusal) rather than task-cognitive
improvement. Any adaptive-loop claim must discriminate against this paper:
what our loop does that closed-loop LQR steering on the same compute does not.

**(e) Suggested citation text for the revised synthesis:**
> Skifstad, Yang & Chou (ICML 2026; arXiv 2604.19018) show that transformer
> layer dynamics are locally linear, model inference as a linear time-varying
> system, and apply linear-quadratic-regulator feedback control using
> layer-wise Jacobians to steer activations toward semantic setpoints in
> closed loop — with derived tracking-error bounds and no offline training.
> This is the closest published realization of closed-loop activation control,
> and it validates the adaptive-loop bet while constraining it: our loop
> candidates must demonstrate, under matched online compute, a capability
> beyond Jacobian-linearized setpoint tracking.

---

## Notes on verification method (Law #3 compliance)

- Every title, author list, date, venue, and abstract sentence above was copied
  from a fetched primary page (arXiv abs, ACL Anthology, icml.cc, OpenReview
  submissions index, or the authors' own repository), not from the review.
- Where the review supplied only an author page (Meta-Reasoner) or a journal
  index (NoisyCoconut), the actual papers were located independently via web
  search.
- The one page that could not be fetched directly was the NoisyCoconut
  OpenReview forum (Cloudflare verification wall); its status was instead
  established from the OpenReview TMLR submissions index and the author's
  repository, both of which say "under review / decision pending," not
  published. Reported exactly as attempted.
- The arXiv-ID discrepancy in the NoisyCoconut OpenReview record (2507.06203
  vs the canonical 2605.08221) is flagged as an unresolved secondary-index
  oddity; the canonical citation is arXiv:2605.08221.
- Venue labels "spotlight" (LatentMAS) and "Accepted by ACL'2026" (Meta-Reasoner)
  come from the authors' own repositories/arXiv comments; the ACL Anthology
  page confirms Meta-Reasoner as Findings of ACL 2026 (2026.findings-acl.649).

**What remains uncertain / follow-ups for the Research Lead:**
1. LatentMAS's ICML-2026-spotlight status rests on the authors' GitHub
   announcement plus the icml.cc listing — not yet on an ICML proceedings page
   with page numbers (acceptable for the map; revisit if the synthesis needs
   page-level citation).
2. RISER's exact training setup (whether any backbone weights move during
   router RL) was not read from the paper body — only the abstract. The
   Δθ=0-exclusion rationale should be re-checked against the full paper before
   the synthesis asserts "violates Δθ=0" rather than "excluded because it
   trains any component."
3. LTPO has no listed venue (arXiv preprint only) — the synthesis should not
   attach a venue to it.
4. NoisyCoconut's TMLR status should be re-checked before any future draft
   that wants to cite it as published.
