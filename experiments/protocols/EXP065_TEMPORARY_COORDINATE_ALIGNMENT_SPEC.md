# EXP065 Protocol Specification: Temporary Coordinate Alignment Operator

**Status:** PRE-REGISTERED (Confirmatory Protocol)  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP062 (Output-Space Boundary), EXP063 (Internal-State Steering), EXP064 (Multi-Vocabulary Linear Aggregation Boundary)  
**Lead Agents:** Research Manager, Theory Agent, Experiment Agent, Adversarial Reviewer  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws, esp. Law 6: Frozen Backbone, Law 7: Zero Data Leakage) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Epistemic Pivot

EXP064 established a decisive empirical boundary:
$$\boxed{\textbf{Representational similarity is not causal interchangeability.}}$$

Specifically:
1. **Geometric Alignment Observed (Level A Passed):** Internal counterfactual contrast directions ($\Delta h = h(x^{\text{rel}}) - h(x^{\text{neutral}})$) across five independently renamed support vocabularies exhibited strong descriptive geometric alignment ($\bar{S} = +0.7927 \pm 0.0618$).
2. **Static Causal Transfer Failed (Level B Failed):** Injected as a static linear vector, the aggregated basis $B_{\text{agg}}$ produced strictly zero causal transfer to unseen novel vocabularies ($\Delta M = 0.0\text{ pp}, p = 1.0000$), with a negligible decision-margin shift ($\Delta \text{Margin} = -0.0118$). In contrast, the same-layer output bridge control at Layer 10 shifted the margin by $+0.7619$ (100% accuracy).

EXP065 transitions from static linear basis aggregation to the true **Self-Consistent Basis Invention (SCBI) dynamic lifecycle**:
$$\boxed{h(x) \xrightarrow{A(x)} \tilde{h}(x) \xrightarrow{B} \text{common relational coordinate} \xrightarrow{A(x)^{-1}} h'(x)}$$

---

## 2. Inviolable Governance on the Alignment Operator $A(x)$

To prevent manufacturing artificial transfer through arbitrary learned mappings, the alignment operator $A(x)$ must strictly satisfy five constitutional constraints:

1. **Inference-Time Discovery:** $A(x)$ is computed on-the-fly for instance $x$ and purged immediately after the forward pass.
2. **Strictly Parameter-Free:** No backpropagation, no gradient optimization, no trained neural adapters, and no fine-tuned projection matrices.
3. **Zero Target-Answer Leakage (Label-Free on Target Instance):**
   $A(x)$ must be constructed **exclusively from premise context tokens** (entity tokens and structural cues present in the input prompt). The target label, query foil, candidate options, and correct answer must never enter the construction of $A(x)$.
4. **Support-Identified Reference Frame:**
   The reference subspace is anchored to the support set's canonical relational coordinate frame.
5. **Invertible and Norm-Controlled (Orthogonal / Unitary):**
   $A(x)$ must be an orthogonal transformation ($A(x)^T A(x) = I$), ensuring that representation norms, energy, and inner products are strictly preserved without distorting the residual stream geometry:
   $$A(x)^{-1} = A(x)^T$$

---

## 3. Mathematical Formulation: Subspace-Preserving Role-Procrustes Alignment

For a target instance $x$, the relational chain in the premise defines distinct structural roles:
- $\text{Role}_{\text{head}}$: The head entity of the transitive chain (e.g. $e_{\text{head}}$).
- $\text{Role}_{\text{tail}}$: The tail entity of the transitive chain (e.g. $e_{\text{tail}}$).
These roles are parsed **strictly from premise syntax** (e.g., `Premise: A outranks B. B outranks C` $\implies e_{\text{head}} = A, e_{\text{tail}} = C$), completely blind to the question options and the correct answer.

In the canonical support set, the corresponding canonical entities define the support reference frame:
$$E_0 = \left[ w(e_{\text{head}}^{(0)}), w(e_{\text{tail}}^{(0)}) \right]^T \in \mathbb{R}^{2 \times d}$$
For target instance $x$, the target entity frame is:
$$E(x) = \left[ w(e_{\text{head}}), w(e_{\text{tail}}) \right]^T \in \mathbb{R}^{2 \times d}$$

### Subspace-Preserving Orthogonal Rotation:
1. Compute the SVD of the cross-role covariance:
   $$E(x)^T E_0 = U \Sigma V^T \in \mathbb{R}^{d \times d}$$
2. The closed-form Procrustes rotation $R(x) = U V^T \in O(d)$ aligns the support role basis with the target role basis.
3. Because $R(x) \in O(d)$, it is strictly norm-preserving ($\|R(x) v\|_2 = \|v\|_2$) and orthogonal ($R(x)^{-1} = R(x)^T$).
4. The dynamic inference-time relational direction is:
   $$b_{\text{dynamic}}(x) = R(x) B_{\text{agg}}$$
   where $B_{\text{agg}}$ is the multi-vocabulary support relational basis, and $b_{\text{dynamic}}(x)$ is dynamically rotated into the instance's specific entity coordinate frame.
5. Injected forward state at Layer 10:
   $$h'(x) = h(x) + \alpha \cdot b_{\text{dynamic}}(x)$$

---

## 4. Benchmark Calibration: Eliminating the 95% Baseline Ceiling

EXP064 evaluated a benchmark with a 95.0% baseline accuracy, leaving only 3 error instances out of 60 ($0/3$ rescues), severely constraining the accuracy endpoint.

### Confirmatory Benchmark Calibration for EXP065:
- **Target Baseline Accuracy Window:** Calibrated to **40%–70%** baseline accuracy on frozen `pythia-160m`.
- **Structural Challenge:**
  - 3-hop and 4-hop transitive reasoning chains.
  - Distractor-interleaved relational premises.
  - Premise clause permutations.
- **Novel Entity Vocabularies ($N=60$ Independent Instances):**
  - Completely unseen disjoint entity domains (e.g. Mythological deities, Astronomical entities, Elemental materials), verified single-token in Pythia tokenizer.
  - Generates substantial error headroom (expected 20–35 baseline errors out of 60).

---

## 5. The Three-Stage Experimental Architecture

### Stage A — Alignment Discovery in Support Space
- Test whether independently renamed support vocabularies ($\mathcal{V}_1 \dots \mathcal{V}_5$) exhibit coordinate rotation deficits.
- Compute the cross-vocabulary alignment under the Orthogonal Procrustes operator $R_{j \to k}$:
  $$S_{\text{aligned}}(j, k) = \cos(R_{j \to k} \hat{v}_j, \hat{v}_k)$$
- Compare against unaligned baseline cosines $S_{\text{raw}}(j, k)$ to quantify the geometric headroom recovered by coordinate transformation.

### Stage B — Blind Target Inference on Calibrated Benchmark ($N=60$)
- For each target instance $x \in \mathcal{D}_{\text{test}}$, infer $R(x)$ **blind to the target answer**.
- Evaluate candidate conditions under Operator O2 at Layer 10 ($\alpha = 0.50$):
  1. **Unintervened Baseline:** Frozen model accuracy on difficulty-calibrated benchmark.
  2. **Static Basis Baseline ($B_{\text{agg}}$):** Unaligned linear aggregate from EXP064.
  3. **Aligned Dynamic Basis ($b_{\text{dynamic}}(x) = R(x)^T B_{\text{agg}}$):** The Procrustes-aligned dynamic direction.
  4. **Same-Layer Output Bridge ($v_{\text{output}}^{(10)}$):** Diagnostic benchmark at Layer 10.
  5. **Norm-Matched Random Rotations ($R_{\text{rand}}^T B_{\text{agg}}$):** 5-seed random orthogonal matrices $R_{\text{rand}} \in O(d)$ to verify that alignment specificity—not arbitrary rotation—drives the effect.
  6. **Orthogonal Complement ($R(x)^T B_\perp$):** Rotated vector from $\operatorname{ker}(B_{\text{agg}}^T)$.

### Stage C — Computational Specificity & Robustness
If Stage B demonstrates statistically significant transfer ($\Delta M > 0, p < 0.05$):
- Premise Reversal ($C < B < A$): Must reduce reversal deficit.
- Query Polarity Reversal ("Who is lower in rank?"): Must invert behavioral steering.
- Syntax / Synonym Transfer: Must remain invariant to relation phrase substitution.

---

## 6. Pre-Registered Confirmatory Success Criteria

1. **Criterion 1 (Causal Transfer via Alignment):**
   $$\Delta M(B_{\text{aligned}}) > 0 \quad (p < 0.05) \quad \text{AND} \quad \Delta M(B_{\text{aligned}}) > \Delta M(B_{\text{static}})$$
   on the difficulty-calibrated novel-vocabulary benchmark.
2. **Criterion 2 (Rotation Specificity vs. Random Null):**
   $$\Delta M(B_{\text{aligned}}) > \Delta M(B_{\text{random-rotation}}) \quad (p < 0.05)$$
   confirming that the Procrustes mapping $R(x)$, not generic orthogonal disruption, produces the gain.
3. **Criterion 3 (Decision Margin Leverage):**
   $$\Delta \text{Margin}(B_{\text{aligned}}) > +0.20 \quad \text{on novel instances (exceeding static } B_{\text{agg}}\text{)}.$$

---

## 7. Model Invariance Guarantee

- Target model: Frozen `EleutherAI/pythia-160m` ($\Delta\theta \equiv 0$).
- Parameter SHA-256 hash verified invariant before and after execution:
  `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936`.
