# EXP063 Protocol Specification: Internal-State Basis Construction & Causal Transfer Ladder

**Status:** REVISED PRE-REGISTRATION (Amended with Hierarchical Counterfactual Controls)  
**Date:** 2026-09-21  
**Predecessor Boundary Series:** EXP059, EXP060, EXP061, EXP062 (Formally Frozen as Output-Space Boundary)  
**Lead Agents:** Research Manager, Theory Agent, Experiment Agent, Adversarial Reviewer  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws, esp. Law 6: Frozen Backbone, Law 7: Zero Data Leakage) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Core Pivot

The Output-Space Boundary Series (EXP059–EXP062) established that linear interventions derived from output unembeddings ($W_U[t] - W_U[f]$) manipulate decision margins with high mechanistic specificity ($D_{\text{KL}} \le 0.0014$), but achieve zero structural transfer across disjoint vocabularies ($\Delta M = 0.0\text{ pp}$) and collapse under query or premise inversion.

This established the foundational lesson of Phase I:
$$\boxed{\textbf{Controlling a model's answer is not the same as controlling the computation that produces the answer.}}$$

**Phase II** pivots from output-space steering to **Internal-State Basis Construction**.

### Core Research Question
$$\boxed{\textbf{Can SCBI discover a temporary internal basis whose intervention transfers across instances while preserving the computation it is intended to control?}}$$

*Conceptual Discipline:* We do **not** define "internal-state basis" as automatically meaning "computational representation." State-space correlation must be empirically distinguished from causal computational reuse. The research trajectory advances through four strictly separated stages:
$$\text{Output Control} \longrightarrow \text{Internal-State Control} \longrightarrow \text{Reusable Internal Control} \longrightarrow \text{Computational Control}$$

---

## 2. The Revised Six-Level Evaluation Ladder (R1 to R6)

To prevent premature claims of "reasoning discovery," EXP063 establishes an amended, non-circular evaluation hierarchy:

| Level | Capability Target | Empirical Falsification Criterion | Prerequisite |
| :--- | :--- | :--- | :---: |
| **R1 — Causal State Localization** | Does a task-relevant direction exist in internal hidden states? | $\Delta M(B_{\text{true}}) > \Delta M(B_{\text{controls}})$ ($p < 0.05$) **AND** state-level displacement $\Delta H(B_{\text{true}}) > \Delta H(B_{\text{controls}})$. | None |
| **R2 — Instance Transfer** | Does an internal basis discovered on $\mathcal{D}_{\text{support}}$ improve unseen validation instances $\mathcal{D}_{\text{val}}$? | $\Delta M_{\text{transfer}}(\mathcal{D}_{\text{val}}) > 0$ with $b > c$ ($p < 0.05$) without seeing test answers. | **R1** |
| **R3 — Vocabulary Transfer** | Does the internal basis transfer to instances with disjoint entity names? | $\Delta M_{\text{transfer}}(\text{Novel Entities}) > 0$ ($p < 0.05$). | **R2** |
| **R4 — Structural Transfer** | Does the basis survive controlled syntax, wording, and clause order changes? | $\Delta M_{\text{transfer}}(\text{Permuted Surface}) > 0$ under relation-preserving transformations. | **R3** |
| **R5 — Computational Specificity** | Does the basis alter the internal relational computation rather than merely the output answer? | Demonstrates superiority over the output bridge control $v_{\text{output}}$, rescues premise reversal ($C < B < A$), and inverts correctly under query polarity reversal. | **R4** |
| **R6 — Autonomous Basis Discovery** | Can SCBI discover and select this basis without ground-truth labels? | Autonomous evaluator selection achieves statistically significant improvement over random selection on held-out test data. | **R5** |

*Inviolable Rule:* Levels R1–R3 are strict prerequisites before investigating R4–R5. Level R6 is deferred until R1–R5 are empirically established.

---

## 3. Strict Three-Way Data Partitioning (Pre-Registered Layer Protocol)

To eliminate retrospective layer cherry-picking and guarantee zero data leakage:
1. **Support Set ($\mathcal{D}_{\text{support}}$, $N=30$):** Used strictly for extracting internal hidden states and constructing candidate bases.
2. **Validation Set ($\mathcal{D}_{\text{val}}$, $N=30$):** Used strictly for screening candidate layers $L \in \{2, 5, 7, 10\}$ and operators (O1 vs. O2). The single best (layer, operator) configuration is prospectively locked based on $\mathcal{D}_{\text{val}}$.
3. **Confirmatory Held-Out Set ($\mathcal{D}_{\text{heldout}}$, $N=30$):** The prospectively locked configuration is evaluated once on unseen held-out instances.
4. **Absolute Blinding (AGENTS.md Law 7):** Basis construction algorithms receive only activations from $\mathcal{D}_{\text{support}}$. Under no circumstances are validation or held-out prompt strings, target tokens, or evaluation labels exposed during basis construction.
5. **Backbone Immutability (AGENTS.md Law 6):** Pre- and post-run parameter SHA-256 hashes must match identically:
   `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).

---

## 4. Candidate Internal-State Basis Families

EXP063 evaluates three mathematically distinct internal basis families from internal hidden states $h_i^{(l)} \in \mathbb{R}^{d_{\text{model}}}$ ($d_{\text{model}}=768$):

### Family 1: Matched Counterfactual State Difference Subspace ($B_{\text{diff}}$)
To eliminate lexical, length, and positional confounds, $B_{\text{diff}}$ is constructed exclusively from **strictly matched counterfactual pairs**:
- Relational Prompt $x_{\text{rel}}$: `"Premise: Alice outranks Bob. Bob outranks Charlie. Question: Who is higher in rank, Alice or Charlie? Answer:"`
- Matched Neutral Prompt $x_{\text{neutral}}$: `"Premise: Alice is next to Bob. Bob is next to Charlie. Question: Who is higher in rank, Alice or Charlie? Answer:"`
- Both prompts possess identical token length, identical entity names, identical query format, and identical target/foil vocabulary. The difference:
  $$\Delta h_i^{(l)} = h_i^{(l)}(x_{\text{rel}}) - h_i^{(l)}(x_{\text{neutral}})$$
  $$B_{\text{diff}} = \operatorname{SVD}_{k}\left([\Delta h_1^{(l)}, \dots, \Delta h_N^{(l)}]\right)$$
  isolates the minimal relation-bearing transformation while holding surface geometry constant.

### Family 2: High-Variance Activation Subspace ($B_{\text{var}}$, explicitly designated Variance Basis)
- Top-$k$ principal components of internal states during relational prompt processing:
  $$C = \frac{1}{N} \sum_{i=1}^N (h_i^{(l)} - \bar{h})(h_i^{(l)} - \bar{h})^T, \quad B_{\text{var}} = \operatorname{TopK-Eigenvectors}(C)$$
  *Epistemological Label:* This is explicitly labeled a **Variance Basis**, recognizing that variance directions can capture syntax, token identity, and positional encodings rather than relational deduction.

### Family 3: Relational Centroid Displacement ($B_{\text{centroid}}$)
- Direction connecting class centroids of high-rank vs. low-rank comparative states:
  $$v_{\text{centroid}} = \frac{\bar{h}_{\text{high}} - \bar{h}_{\text{low}}}{\|\bar{h}_{\text{high}} - \bar{h}_{\text{low}}\|_2}$$

---

## 5. Decoupled Intervention Operators: O1 vs. O2

To separate component amplification from external basis injection, EXP063 registers two distinct operators:

### Operator 1 (O1) — Projection Amplification:
$$h_{\text{new}}^{(l)} = h^{(l)} + \alpha P_B h^{(l)} = h^{(l)} + \alpha B B^T h^{(l)}$$
- *Causal Hypothesis Tested:* "Amplifying the component of the model's existing internal state already lying within subspace $B$ enhances task computation."

### Operator 2 (O2) — Basis Injection:
$$h_{\text{new}}^{(l)} = h^{(l)} + \alpha b$$
where $b \in \operatorname{span}(B)$ is a unit vector constructed exclusively from the support set $\mathcal{D}_{\text{support}}$.
- *Causal Hypothesis Tested:* "Injecting an externally discovered coordinate direction into the hidden state enables/restores task computation."

---

## 6. Rigorous Matched Controls & The Output Bridge Control

For every true candidate basis $B_{\text{true}}$ (rank $k$), EXP063 evaluates six mandatory controls:

1. **Random Subspace Distribution ($B_{\text{rand}}^{(1 \dots K)}$, $K=5$ seeds):**
   - Orthonormal basis drawn from $\mathcal{N}(0, I_d)$ strictly matched in dimension: $\dim(B_{\text{rand}}) = \dim(B_{\text{true}})$.
   - **Norm-Matched Scaling:** The intervention energy is scaled to match the true projection norm:
     $$\mathbb{E}[\|P_{B_{\text{rand}}} h\|_2] \approx \|P_{B_{\text{true}}} h\|_2$$
     preventing true bases from appearing superior merely due to larger effective perturbation magnitude.
2. **Dimension-Shuffled Basis ($B_{\text{shuff}}$):**
   - Randomized coordinate permutation of the true basis vectors within $\mathbb{R}^{d_{\text{model}}}$.
3. **Strict Orthogonal Complement Subspace ($B_{\perp}$):**
   - An orthonormal basis drawn strictly from the orthogonal complement of the true basis:
     $$B_{\perp} \subset \operatorname{ker}(B_{\text{true}}^T), \quad \operatorname{span}(B_{\perp}) \perp \operatorname{span}(B_{\text{true}})$$
     with dimension and projection energy norm matched to $B_{\text{true}}$.
4. **Wrong-Task Internal Basis ($B_{\text{wrong-task}}$):**
   - Internal basis extracted from an unrelated non-relational task (Level 0 lexical dictionary recall).
5. **Relation-Inverted Counterfactual Basis ($B_{\text{inv}}$):**
   - Internal basis extracted from reversed premises ($C < B < A$).
6. **The Output-Direction Bridge Control ($v_{\text{output}}$):**
   - The normalized unembedding contrast vector from EXP061/062:
     $$v_{\text{output}} = \frac{W_U[t] - W_U[f]}{\|W_U[t] - W_U[f]\|_2}$$
   - *Diagnostic Mandate:* Resolves directly whether the internal-state basis provides computational leverage that cannot be explained by simple output-facing decision steering.

---

## 7. Preregistered Superiority & Screening Criteria

### 7.1 R1 Screening Criterion (Causal Localization)
A candidate basis $B$ passes Level R1 if and only if:
$$\Delta M(B) > \max_{k \in \{1 \dots 5\}} \Delta M(B_{\text{rand}}^{(k)}) \quad (p < 0.05)$$
$$\text{AND} \quad \Delta H(B) > \max_{k \in \{1 \dots 5\}} \Delta H(B_{\text{rand}}^{(k)})$$
where $\Delta H = \|h_{\text{mod}}^{(l)} - h_{\text{base}}^{(l)}\|_2$ measures state-level displacement at the intervened layer.

### 7.2 R5 Computational Specificity Criterion
A candidate basis passes Level R5 if and only if:
1. **Superiority over Output Bridge:** $\Delta M(B) > \Delta M(v_{\text{output}})$ on premise-reversed instances ($p < 0.05$).
2. **Reversal Deficit Amelioration:** Reduces the Premise Reversal Gap ($A > B > C$ vs. $C < B < A$) by at least 15 percentage points without corrupting canonical instances ($b > c$).
3. **Polarity Sensitivity:** Reverses effect direction appropriately when query polarity is inverted ("Who is lower?").
