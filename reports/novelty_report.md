# SCBI Novelty Assessment Report

**Document Status:** Post-Audit Verdict — 2026-09-23; Adversarial Review Wave 2 completed 2026-09-23 (ACCEPT WITH CORRECTIONS); corrections applied 2026-09-23 (Corrections Integrator); adversarial re-sign pending
**Governing Protocol:** [`research/README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/research/README_LITERATURE.md) §9, §10, §13
**Full Evidence:** [`research/literature/audit_2026-09-23.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/research/literature/audit_2026-09-23.md)
**Reviewing Agents:** [`literature-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/literature-agent.md), [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)

---

## 1. Candidate Novelty Classification

Per [`research/README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/research/README_LITERATURE.md) §9, claims must be assigned one of the five formal novelty tiers:
- **N0 — Clearly Existing:** The proposed mechanism already exists substantially unchanged.
- **N1 — Known Combination:** Existing mechanisms are combined differently.
- **N2 — Meaningful Formulation Difference:** The formulation differs in a technically meaningful way.
- **N3 — Strong Methodological Distinction:** The mechanism appears substantially different from prior work.
- **N4 — Potentially Novel:** Evidence of a new mechanism, requiring exhaustive adversarial verification.

**Current Project Status: `N1 — Known Combination`**

Component-level scoring (the audit scores the tested mechanism and the claimed loop separately, per AGENTS.md Laws #4 and #11):
- **Tested static mechanism** ($h \leftarrow h + B_{agg}$, EXP064–066 Stage A): **N0** — algorithmically equivalent to Contrastive Activation Addition / Activation Addition. The computation graph (contrast pair → mean difference → residual-stream addition → forward pass) duplicates prior art.
- **Procrustes cross-vocabulary alignment** (EXP065/066 Stage A): **N0** — a misapplied instance of Mikolov et al. (2013) / Smith et al. (2017); rank-2 unembedding-space fit applied to full-rank hidden-state directions.
- **Claimed full dynamic loop** ($\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ over per-instance bases): **unvalidated formulation distinction** — cannot be scored above N1 per protocol §13. Internally: unvalidated formulation distinction; unscored pending demonstration. *(Wave 2 review L-5: "N2-aspirational" phrasing removed.)*

Composition identity: SCBI = (Family A diff-in-means vector construction) + (Family B linear cross-space alignment) + (Family C inference-time generate–evaluate–select loop). That sentence is the definition of N1.

---

## 2. Closest Prior-Art Methods

### 2.1 Contrastive Activation Addition — Rimsky et al. (2023 / ACL 2024)
- **URL:** https://arxiv.org/abs/2312.06681v1
- **Mechanism Comparison:** CAA computes $v = \bar{h}_+ - \bar{h}_-$ over contrastive prompt pairs and applies $h \leftarrow h + c \cdot v$ during frozen-model inference. SCBI's $B_{agg}$ is a mean contrast direction applied additively to the residual stream. **Operationally identical.**
- **Mathematical Comparison:** Same linear operator; same frozen-backbone constraint; same inference-time application. Aggregation over instances and vocabulary mapping are preprocessing and do not change the applied operator. **[EQUIVALENT]**
- **Implementation Comparison:** CAA sweeps layers; SCBI fixes an aggregation. Both add one static vector per forward pass.
- **Remaining Distinction:** None for the tested mechanism. The dynamic loop is untested.
- **Confidence Level:** High. **This is the strongest prior-art threat.**

### 2.2 Activation Addition (ActAdd) — Turner et al. (2023)
- **URL:** https://arxiv.org/abs/2308.10248v2
- **Mechanism Comparison:** Canonical diff-in-means steering: $v = \overline{h}(p_+) - \overline{h}(p_-)$, $h \leftarrow h + c \cdot v$, no training. SCBI Stage A is an instance of this recipe.
- **Mathematical Comparison:** Identical operator class. **[EQUIVALENT]**
- **Implementation Comparison:** Same.
- **Remaining Distinction:** None for the tested mechanism.
- **Confidence Level:** High.

### 2.3 Tree of Thoughts — Yao et al. (NeurIPS 2023)
- **URL:** https://arxiv.org/abs/2305.10601v2
- **Mechanism Comparison:** Generate candidate thoughts → self-evaluate → BFS/DFS select with backtracking, frozen model, transient state. Algorithmically isomorphic to SCBI's proposed $\mathcal{G}/\mathcal{E}/\mathcal{S}$ loop.
- **Mathematical Comparison:** Not equivalent — ToT searches over token-level thoughts $y$; SCBI proposes searching over representation bases $B$. Change of search object, not of algorithm.
- **Implementation Comparison:** ToT's loop is demonstrated; SCBI's is not implemented or tested.
- **Remaining Distinction:** Search object ($B$ vs $y$) — a formulation-level difference with zero empirical support.
- **Confidence Level:** High.

### 2.4 Self-Consistency — Wang et al. (ICLR 2023)
- **URL:** https://arxiv.org/abs/2203.11171
- **Mechanism Comparison:** Sample diverse reasoning paths; select by majority vote (marginalize the path). Agreement-as-evidence is the philosophical core of SCBI's proposed $\mathcal{E}/\mathcal{S}$ operators.
- **Mathematical Comparison:** Selection over outputs $y$, not bases $B$. The "self-consistency" criterion itself is prior art.
- **Implementation Comparison:** Demonstrated on reasoning benchmarks; SCBI has no analogous demonstration.
- **Remaining Distinction:** Applying agreement-based selection to *bases* rather than *answers* — conjectured, untested.
- **Confidence Level:** High.

### 2.5 Orthogonal Procrustes cross-space alignment — Smith et al. (ICLR 2017)
- **URL:** https://arxiv.org/abs/1702.03859
- **Mechanism Comparison:** Orthogonal Procrustes alignment of vector spaces + retrieval evaluation. SCBI's Stage A alignment is this operator, misapplied.
- **Mathematical Comparison:** $\min_Q \|QA - B\|_F$ s.t. $Q^\top Q = I$ — same form as Mikolov et al. (2013), https://arxiv.org/abs/1309.4168, unconstrained variant.
- **Implementation Comparison:** Smith et al. align full embedding spaces and evaluate retrieval; SCBI fit rank-2 in unembedding space and applied to hidden states (forensically unsound).
- **Remaining Distinction:** None — a defective special case of a known recipe.
- **Confidence Level:** High.

### 2.6 Plug and Play Language Models — Dathathri et al. (ICLR 2020)
- **URL:** http://arxiv.org/abs/1912.02164
- **Mechanism Comparison:** At generation time, gradients from an external attribute model update the LM's past hidden activations with KL regularization; the LM is never trained. Per-instance, inference-time representation intervention of a frozen model guided by an evaluator — the closest published dynamic-intervention prior to SCBI's claimed loop (Wave 2 review L-1).
- **Mathematical Comparison:** Not equivalent — PPLM's evaluator is external (separately trained classifier) and its search object is the hidden-state trajectory, optimized by gradient steps; SCBI proposes an internal self-consistency evaluator over basis-valued objects via generate–evaluate–select. The remaining distinction is a conjecture with zero empirical support.
- **Implementation Comparison:** PPLM is demonstrated on controlled generation; SCBI's loop is not implemented.
- **Remaining Distinction:** Internal (self-consistency) evaluator + basis-valued search object — claimed, not demonstrated.
- **Confidence Level:** High.

### 2.7 Self-Refine — Madaan et al. (NeurIPS 2023)
- **URL:** https://arxiv.org/abs/2303.17651
- **Mechanism Comparison:** A single frozen LLM acts as generator, critic, and refiner in an iterative loop (generate → self-critique → refine), with ~20% absolute gains across 7 tasks. The second independent G/E/S-loop prior with an *internal* evaluator (alongside ToT and self-consistency) (Wave 2 review L-2).
- **Mathematical Comparison:** Not equivalent — the search object is text outputs $y$, refined rather than selected; no basis-valued search.
- **Implementation Comparison:** Demonstrated; gains plateau after 2–3 iterations and self-critique has documented blind spots.
- **Remaining Distinction:** Search object ($B$ vs $y$) — conjectured, untested. Its plateau/blind-spot limitation is a direct falsifier-risk for SCBI's unvalidated $\mathcal{E}$.
- **Confidence Level:** High.

---

## 3. Adversarial Red-Team Novelty Audit

*(Self-administered red-team challenge by the Literature Agent; independent Adversarial Reviewer sign-off still pending.)*

**Challenge 1 — "But the basis is aggregated across instances, not a single contrast pair."**
Rebuttal: Aggregation is preprocessing. CAA itself aggregates across many contrast pairs per behavior. The applied operator is unchanged. Fails.

**Challenge 2 — "But SCBI maps across vocabularies with Procrustes."**
Rebuttal: Cross-space linear mapping is Mikolov (2013) / Smith (2017). SCBI's instance was rank-deficient and misapplied — a broken instance of a known operator confers no novelty. Fails.

**Challenge 3 — "But the full dynamic loop has no exact prior."**
Rebuttal: True and weak. No verified paper formalizes the complete per-instance basis loop — but ToT provides the isomorphic loop structure and self-consistency provides the selection criterion. The closest dynamic-intervention prior is PPLM (per-instance inference-time hidden-state updates, external evaluator); the second G/E/S-loop prior is Self-Refine (internal evaluator over outputs, with documented plateau/blind-spot limitations that directly threaten SCBI's unvalidated $\mathcal{E}$). An untested domain-shifted composition is N1 by the protocol's own definition ("existing mechanisms combined differently"). The loop has additionally never been shown to work, so even its formulation-level distinction is a conjecture, not a result. Survives only as: "no *exact* prior found; closest structural and dynamic priors identified."

**Challenge 4 — "The frozen-backbone constraint is distinctive."**
Rebuttal: The entire steering literature (Families A–C) operates with $\Delta\theta = 0$. Only TTT updates weights, and TTT is thereby *excluded* from SCBI's class, not a competitor within it. Fails.

**Challenge 5 — "The ~0.7 raw cosine shows real geometric structure."**
Rebuttal: Ethayarajh (2019) establishes strong anisotropy in contextual representations — high raw cosine is expected and weak evidence. Jorgensen et al. (2023) show un-centred mean-difference vectors carry a non-informative global offset, which SCBI never removed. The cosine figure cannot bear the interpretive weight placed on it. Fails.

**Net red-team result:** Every distinctiveness claim except the untested loop formulation fails. The loop formulation survives as an open conjecture, not a novelty result.

---

## 4. Sign-Off & Verdict

- **Novelty tier: N1 — Known Combination** (tested components N0; dynamic loop unvalidated).
- **Strongest prior-art threat:** Contrastive Activation Addition (Rimsky et al., 2023/ACL 2024) — the tested SCBI mechanism is algorithmically equivalent to it.
- **Required reformulation:** Drop "invention"/"novel mechanism" language. Reframe as a test of whether per-instance basis search (ToT-style loop + CAA-style construction) over representation space transfers output-space search gains under frozen-backbone constraints. EXP067 is reframed as boundary-characterization science (Wave 2 review §5): it tests whether a *sound* alignment operator changes the Stage B null; its outcome cannot move the novelty needle either way (positive C3 = well-executed CAA, i.e. N0; null = boundary confirmed). The loop test is spun out as a separate future protocol contingent on an operational $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ spec, which does not currently exist.
- **Literature Agent Signature:** `SIGNED — 2026-09-23 (Nova, Literature Agent)`
- **Adversarial Reviewer Signature:** `SIGNED — 2026-09-23 (Nova, Adversarial Reviewer; Wave 2 re-verification §8: all §6 gates satisfied, 15/15)`
- **Research Manager Approval:** `PENDING`
