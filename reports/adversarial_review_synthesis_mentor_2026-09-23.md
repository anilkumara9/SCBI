# Law #14 Adversarial Review of LOG-158 (A–J Synthesis) — Mentor Review, 2026-09-23

**Reviewer:** ChatGPT, acting as independent scientific mentor / adversarial reviewer
**Target:** `research/synthesis/SYNTHESIS_A_J_2026-09-23.md` (LOG-158)
**Disposition: Inconclusive for program adoption until the synthesis receives a targeted revision.**

> Not because the central research question has failed. Because the synthesis is
> now strong enough that its remaining weaknesses are mostly formal ones — exactly
> the weaknesses that could later permit an apparently positive result to survive
> on a technicality.

Epistemic status of this document: reviewer [INTERPRETATION] and reviewer-supplied
citations. Every cited paper must be independently verified by the literature
track (Law #3) before entering the novelty map. Nothing in this review is [FACT]
until verified.

---

## 1. The prior-art map is materially incomplete

Four current papers directly overlap candidate mechanisms that §D/E currently treats as unoccupied.

| LOG-158 candidate | Current conflict | Consequence |
| ----------------- | ---------------- | ----------- |
| **H1 / DPRS** | **LTPO** is parameter-free, test-time optimization of latent thought vectors on a frozen LLM, using an intrinsic confidence reward in an online loop. ([arXiv](https://arxiv.org/abs/2510.04182)) | DPRS can no longer claim that the general "frozen model + per-instance latent optimization + internal signal" slot is unoccupied. Its claim must be narrowed to **readout-space perturbation search** specifically. |
| **H4 / ASR** | **Meta-Reasoner** already dynamically changes reasoning strategy at inference time using contextual multi-armed bandits and reports improvements under the same-compute setting. ([ACL Anthology](https://aclanthology.org/people/yuan-sui/)) | "Test-time-discovered strategy routing" is not an empty slot. ASR needs a stricter distinction than adaptive routing. |
| **H5a / LCMIC** | **LatentMAS** is explicitly training-free latent collaboration with shared latent working memory between agents. It is an ICML 2026 paper and directly occupies latent inter-agent communication. ([arXiv](https://arxiv.org/abs/2511.20639)) | The sentence "No competitor uses inter-instance latent exchange" is false. This candidate's novelty claim must be rewritten. |
| **H5b / CLB** | **NoisyCoconut** is a training-free inference-time method that injects noise into latent trajectories, produces multiple latent paths, and aggregates them. It is listed by TMLR in June 2026. ([TMLR](https://jmlr.org/tmlr/papers/)) | "Latent branching + aggregation" is occupied. CLB can only claim a narrower distinction such as **intra-layer fork with a genuinely non-selection merge operator**. |

There is also **RISER**, published in Findings of ACL 2026, which performs adaptive activation steering with a dynamically selected/composed vector library. It uses a trained RL router, so it violates the Δθ=0 boundary and is therefore **not an equivalence threat**. But it absolutely belongs in the novelty map as an adjacent excluded method. ([ACL Anthology](https://aclanthology.org/2026.findings-acl.226/))

By contrast, the two strongest "adjacent possible" citations check out: **∇-Reasoner** is an ICLR 2026 paper using test-time gradient optimization of latent/textual representations, and **Activation-LQR** is an ICML 2026 paper implementing closed-loop activation control with layer-wise Jacobians. ([arXiv](https://arxiv.org/abs/2603.04948))

So §D1's statement

> "The only unoccupied sub-slot is C′"

is now too strong. It should become something like:

> **Within the reviewed literature, the remaining potentially distinct slot is a narrowly defined combination of per-instance activation-operator construction, transfer-validated internal evaluation, conditional computation, and Δθ=0 — not generic latent optimization, routing, cooperation, or branching.**

That is much harder to attack.

## 2. The statistical protocol contains a real inconsistency

The synthesis correctly says verdicts must distinguish Not supported from Inconclusive. But several gates later effectively use **p ≥ 0.05 ⇒ candidate loses / Not supported**. That is not statistically valid by itself. For example, G4 F1 says: C* ≤ best of M2–M8 ... all p≥0.05 → Not supported. A nonsignificant positive estimate is **not evidence that the candidate is beaten** — the experiment may simply be underpowered. The same issue appears in F1 where candidates are culled on observed `Δ ≤ 0` rather than a confidence-bound/equivalence rule.

**Required correction:** every primary comparison needs effect estimate + confidence interval + pre-registered practical margin + significance rule. For example: `ΔM > δ_min` with lower CI > `δ_min` → Supported; CI overlaps the meaningful region → Inconclusive; upper CI < `δ_min` → Not supported; genuinely negative effect with sufficient precision → Not supported. This is especially important with **N=80**, where McNemar's exact test is discrete and modest decision deltas may be impossible to distinguish from zero. The protocol should also preregister the **minimum detectable effect and power** before NTDP.

## 3. Program-level multiplicity needs an explicit law

The synthesis has eight candidate mechanisms, multiple ablations, several baseline comparisons, three task families, and a program-level rule that allows **any candidate** to produce Branch S. You cannot simply use `α=.05` independently throughout and rely on the eventual conjunction to make everything safe. The correct solution isn't necessarily crude Bonferroni everywhere. A much better design is a **hierarchical testing plan**: `program gate → candidate gate → mechanism fingerprint → secondary analyses` with a fixed alpha budget. For example, the program could reserve the primary α for the candidate-level NTDP claims and treat exploratory mechanism diagnostics separately. The critical thing is that **candidate selection cannot silently recycle significance**.

## 4. A1/A3/A7 still overstate the bridge evidence

A1 says raw cosine ≈ 0.7 shows shared structure, not noise. But B1 simultaneously notes that anisotropy can inflate cosine similarity. Those two statements cannot both carry the current strength. The defensible statement: **raw geometric similarity is observed; semantic common structure is not established until anisotropy-controlled nulls support it.** Likewise, the "five experiments converging on the output-side reading" should be treated very cautiously — they are not five independent pieces of evidence. The bridge construction repeatedly uses `normalize(E[target] − E[foil])`, so the experiments share the exact confound that K1/K3 are designed to expose. The proper interpretation: **the same option-informed construction repeatedly produces causal decision changes** — strong evidence of **steerability of the readout path**, but not five independent confirmations of an autonomous output-side cognitive mechanism. This actually strengthens the logic of H6: K1/K3 aren't minor diagnostics; they can collapse the entire interpretive stack.

## 5. C5 is no longer a live novelty candidate in its current form

The sentence "No competitor uses inter-instance latent exchange" is now directly contradicted by LatentMAS ([arXiv](https://arxiv.org/abs/2511.20639)). Therefore **LCMIC as "latent-channel cooperation" = prior art family.** It can survive only if narrowed to something materially different, e.g. `same frozen backbone + causal residual exchange + verifier/arbiter separation + relational-task intervention` — and even then the claim is formulation-level, not "latent cooperation is new." The Box 1 statement "no competitor uses inter-instance latent exchange" must be removed. That is precisely the sort of sentence Law #14 should kill before it reaches a paper.

## 6. C6 also needs to be narrowed

NoisyCoconut already has frozen model, inference-time latent perturbation, multiple latent trajectories, path-diversity measurement, aggregation/consensus, no retraining. ([TMLR](https://jmlr.org/tmlr/papers/)) The scientific distinction cannot simply be "CLB branches in latent space and merges trajectories" — that space is occupied. The surviving hypothesis is narrower: **intra-forward/intra-layer latent branching followed by a merge operator that computes something irreducible to candidate selection.** The decisive test becomes `merge ≠ argmax/selection`, but the baseline must now include **NoisyCoconut-style latent branching/consensus**, not just Best-of-4.

## 7. H3 has a credit-assignment problem

TTPS says the deterministic interpreter executes external computation and therefore potentially crosses directly into L3. That inference is too quick: an external interpreter can perform arbitrary computation that the transformer itself did not possess. The question becomes: did the frozen model acquire a capability, or did we give the model access to a programmable computer? For TTPS, the interpreter needs an explicit capability boundary: **fixed instruction set → bounded operation count → no external data → no task solver hidden in primitives → interpreter-only control cannot solve the task.** An **interpreter-only baseline** is also needed. Otherwise a sufficiently expressive DSL makes L3 almost tautological. "New computation" ≠ "new capability of the frozen model."

## 8. C4 has a second problem besides prior art

ASR says the test-time bandit discovers the strategy policy. But where does the bandit learn? If it learns across multiple test examples, the protocol has **cross-instance state** and needs a formal online adaptation boundary. If it learns separately within one problem, there may not be enough reward observations for meaningful bandit learning. Preregistration must explicitly specify `policy scope = per-instance / per-episode / test-stream` and whether information from example `i` may affect example `i+1`. Without that, ASR's claimed adaptivity is underspecified. And because Meta-Reasoner already occupies dynamic strategy selection, ASR must beat or structurally differ from it. ([ACL Anthology](https://aclanthology.org/people/yuan-sui/))

## 9. Compute matching is not yet actually closed

"Matched FLOPs" is the right principle, but the system boundary needs to be defined. This matters for A-LQR Jacobian computation, ∇-Reasoner backward passes, reward models, TTPS interpreter operations, bandit updates, latent memory movement, latent-agent communication. The protocol needs two numbers — **online inference FLOPs** and **one-time/amortized preparation FLOPs** — defined consistently across every baseline. Otherwise "matched compute" can become a hidden accounting choice. (∇-Reasoner explicitly uses gradients from model likelihood and a reward model ([arXiv](https://arxiv.org/abs/2603.04948)); A-LQR explicitly uses layer-wise Jacobians and control computation ([arXiv](https://arxiv.org/abs/2604.19018)).)

## 10. EXP023's proposed selection-bias audit may itself be statistically wrong

The proposal "enumerate the configuration grid and Bonferroni/max-T adjust the EXP023 test" is necessary **only if the confirmatory result was affected by that selection process**. If `dev set → select configuration → untouched independent test set → one confirmatory test`, then searching the dev grid does **not automatically require Bonferroni correction of the independent test p-value**. The correct Law #14 audit question: **was the Seed-84/168 confirmatory data completely untouched by configuration selection, threshold selection, benchmark choice, and interpretation choice?** If yes, the main concern is generalization/selection optimism, not test-set familywise Type-I inflation. If no, multiplicity correction becomes appropriate. A10 should not precommit to Bonferroni before the data lineage is reconstructed. An adversarial audit should correct the proposed falsifier itself if necessary.

## 11. The strongest part of LOG-158 should remain

Despite the above, one part of the synthesis is genuinely strong: **the program now has a falsification architecture rather than a sequence of increasingly elaborate hypotheses.** The strongest sections: **A4** (explicit mechanism refutation rather than reinterpretation); **A5** (narrow licensing of negative results); **A6** (refusing to manufacture an oracle ceiling that was never measured); **A9** (decision-flip endpoints over margin movement); **D2** (explicit novelty boundary); **F1** (matched-compute adaptive ablations); **H3** (an actual license to kill the entire family); **I** (separating L1, L2, L3 instead of calling every score increase "capability"). That last one is particularly important: the synthesis explicitly acknowledges that the current corpus does **not** establish its own ultimate objective. That is scientifically healthy.

---

## Required pre-adoption changes

| Area | Required change |
| ---- | --------------- |
| Literature | Add LTPO, LatentMAS, NoisyCoconut, Meta-Reasoner; retain RISER as Δθ=0-excluded adjacent art |
| Novelty | Replace "only unoccupied C′" with a narrower reviewed-literature claim |
| H1 | Add LTPO as a forced baseline / novelty comparator |
| H4 | Add Meta-Reasoner as a forced baseline / comparator |
| H5a | Rewrite LCMIC; remove the false "no competitor" claim |
| H5b | Add NoisyCoconut and narrow CLB to intra-layer merge-specific novelty |
| Statistics | Introduce hierarchical alpha control and effect-size/CI rules |
| F1/G4 | Stop equating `p≥.05` with evidence against the candidate |
| A1 | Downgrade the raw-cosine "shared structure" inference until anisotropy control |
| A3/A7 | Stop treating repeated option-informed bridge tests as independent convergent evidence |
| TTPS | Bound external computation and add interpreter-only control |
| Compute | Formalize online vs amortized FLOPs across all baselines |
| EXP023 | Determine data lineage before deciding whether multiplicity adjustment is required |

One especially important current-literature update: **Activation-LQR is now listed in ICML 2026's proceedings**, so §B5 can accurately describe it as a published 2026 result rather than merely an under-review preprint. ([ICML](https://icml.cc/Downloads/2026))

The new prior-art findings change the burden of proof materially: **the next experiment should not merely demonstrate that one of the eight mechanisms works. It must demonstrate that what works is not already explained by this newer prior art.**
