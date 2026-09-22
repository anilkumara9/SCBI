# EXP064 Protocol Specification: Lexical-Invariant Internal-State Basis Construction

**Status:** PRE-REGISTERED (Confirmatory Protocol)  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP062 (Output-Space Boundary), EXP063 (Internal-State Localization)  
**Lead Agents:** Research Manager, Theory Agent, Experiment Agent, Adversarial Reviewer  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws, esp. Law 6: Frozen Backbone, Law 7: Zero Data Leakage) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Epistemic Frontier

EXP063 demonstrated that an internal hidden-state direction ($B_{\text{centroid}}$ at Layer 10) can causally alter model behavior on unseen held-out instances within a familiar entity vocabulary ($+16.7\text{ pp}, b=5, c=0$). However, this basis exhibited strictly zero causal transfer to a disjoint entity vocabulary ($\Delta M = 0.0\text{ pp}, p = 1.0000$), demonstrating that single-vocabulary basis extraction remains trapped by lexical-coordinate dependence.

EXP064 targets this bottleneck directly:
$$\boxed{\textbf{Can SCBI construct an internal basis from multiple lexical realizations of the same computation such that the resulting basis transfers to an unseen vocabulary?}}$$

The operational paradigm transitions:
$$\text{Single-Vocabulary Basis} \longrightarrow \text{Multi-Vocabulary Aggregation} \longrightarrow \text{Disjoint-Vocabulary Causal Transfer}$$

---

## 2. The Central Hypothesis

- **Hypothesis $H_{\text{cancel}}$ (Lexical Cancellation / Common Subspace):**
  When internal counterfactual state differences ($\Delta h_{i,k} = h(x_{i,k}^{\text{rel}}) - h(x_{i,k}^{\text{neutral}})$) are aggregated across $K$ independently renamed lexical realizations, instance-specific and token-specific coordinates vary orthogonally and cancel, concentrating energy along the shared relational computation:
  $$\Delta M(B_{\text{multi}}) > 0 \quad \text{AND} \quad \Delta M(B_{\text{multi}}) > \Delta M(B_{\text{single}}) \quad \text{on unseen novel vocabulary}.$$
- **Hypothesis $H_{\text{disjoint}}$ (Independent Coordinate Subspaces):**
  Different entity vocabularies recruit disjoint, unaligned activation coordinates ($\cos(v_k, v_j) \approx 0$). In this regime, linear pooling averages out signal, yielding $\Delta M(B_{\text{multi}}) \approx 0$, proving that a static linear subspace cannot bridge vocabularies without an explicit temporary coordinate transformation.

---

## 3. Power Analysis & Pre-Registered Sample Size Rationale

In EXP063, a sample size of $N=30$ resulted in borderline statistical significance ($b=5, c=0 \implies p = 0.0625$), creating ambiguity. 

### Pre-Registered Statistical Calibration:
- **Target Effect Size:** Minimum scientifically meaningful transfer effect $\Delta M \ge +12.5\text{ pp}$ with low corruption rate ($c \le 1$).
- **Sample Size Setting:** We set the held-out confirmatory sample size to **$N_{\text{conf}} = 60$ independent instances** on a completely unseen vocabulary (e.g., Greek letter entities / astronomical bodies).
- **Exact Binomial Power:**
  - With $N = 60$, an observed net shift of $+15.0\text{ pp}$ (e.g., $b = 10, c = 1$) yields an exact McNemar $p = 0.0117$, comfortably surpassing the $p < 0.05$ threshold.
- **Effective-Unit Accounting Rule (Mandatory):**
  The $K$ renamed realizations used in the support set are structured augmentations, **not independent samples**. The effective degrees of freedom remain anchored strictly to the base instances ($N_{\text{base}} = 60$).

---

## 4. Multi-Vocabulary Support Construction

Support instances ($N_{\text{base}} = 30$, 15 2-hop, 15 3-hop) are evaluated under $K=5$ disjoint lexical vocabularies $\mathcal{V}_1, \dots, \mathcal{V}_5$:
- $\mathcal{V}_1$: Anglo Names (`Alice`, `Bob`, `Charlie`, `David`, `Emma`)
- $\mathcal{V}_2$: Biblical / Historical (`Aaron`, `Caleb`, `Gideon`, `Miriam`, `Reuben`)
- $\mathcal{V}_3$: Classical Greek (`Hector`, `Jason`, `Nestor`, `Paris`, `Priam`)
- $\mathcal{V}_4$: Roman / Latin (`Marcus`, `Lucius`, `Titus`, `Felix`, `Silas`)
- $\mathcal{V}_5$: Modern International (`Liam`, `Noah`, `Sora`, `Maya`, `Leila`)

For every instance $i \in \{1 \dots N_{\text{base}}\}$ and vocabulary $k \in \{1 \dots K\}$, we construct matched counterfactual pairs:
- $x_{i,k}^{\text{rel}}$: Comparative relation prompt holding relational semantics constant.
- $x_{i,k}^{\text{neutral}}$: Structurally matched neutral context (`"is next to"`) preserving identical token length, entity names, query options, and answer tokens.

Extract internal contrast vectors at Layer 10 (prospectively validated in EXP063):
$$\Delta h_{i,k} = h^{(10)}(x_{i,k}^{\text{rel}}) - h^{(10)}(x_{i,k}^{\text{neutral}}) \in \mathbb{R}^{768}$$

---

## 5. Candidate Internal Basis Constructions

EXP064 compares three candidate basis constructions against each other and against matched controls:

### A. Single-Vocabulary Baseline ($B_{\text{single}}$)
- SVD applied exclusively to vocabulary $\mathcal{V}_1$:
  $$B_{\text{single}} = \operatorname{SVD}_1\left([\Delta h_{1,1}, \dots, \Delta h_{N,1}]\right)$$

### B. Pooled Multi-Vocabulary Basis ($B_{\text{pool}}$)
- SVD applied to the pooled set of all $N \times K = 150$ contrast vectors:
  $$B_{\text{pool}} = \operatorname{SVD}_1\left([\Delta h_{1,1}, \dots, \Delta h_{N,K}]\right)$$

### C. Normalized Per-Vocabulary Aggregation ($v_{\text{agg}}$)
- First compute the mean normalized direction per vocabulary:
  $$v_k = \frac{1}{N} \sum_{i=1}^N \frac{\Delta h_{i,k}}{\|\Delta h_{i,k}\|_2}, \quad \hat{v}_k = \frac{v_k}{\|v_k\|_2}$$
- Aggregate across all $K$ vocabularies:
  $$v_{\text{agg}} = \frac{\sum_{k=1}^K \hat{v}_k}{\|\sum_{k=1}^K \hat{v}_k\|_2}, \quad B_{\text{agg}} = v_{\text{agg}}$$

---

## 6. Pre-Intervention Diagnostic: Cross-Vocabulary Representation Alignment

Before conducting behavioral interventions, EXP064 measures pairwise cosine similarities:
$$S_{j,k} = \cos(\hat{v}_j, \hat{v}_k) \quad \forall j \ne k \in \{1 \dots K\}$$
against the empirical random null distribution ($S_{\text{rand}} = \mathcal{N}(0, 1/d_{\text{model}})$).

### Pre-Intervention Alignment Thresholds:
1. **Strong Alignment ($S_{j,k} \ge 0.40$):** Indicates a robust shared coordinate across vocabularies.
2. **Moderate Alignment ($0.15 \le S_{j,k} < 0.40$):** Indicates partial overlap; aggregation may filter noise.
3. **Orthogonal Disconnect ($S_{j,k} < 0.10$):** Proves that representations are coordinate-disjoint, indicating that linear pooling will cancel both signal and noise.

---

## 7. Confirmatory Evaluation on Unseen Novel Vocabulary ($\mathcal{V}_{\text{novel}}$, $N=60$)

The evaluation set $\mathcal{D}_{\text{test}}$ ($N=60$ independent instances) uses **completely unseen entities** never present in any support set:
- $\mathcal{V}_{\text{novel}}$: Planetary / Astronomical (`Mars`, `Venus`, `Jupiter`, `Saturn`, `Mercury`) and Elemental (`Iron`, `Gold`, `Silver`, `Bronze`, `Steel`).

### The 8 Mandatory Comparative Conditions ($N=60$):
1. **$B_{\text{single-SVD}}$ (Single-Vocab SVD):** SVD applied to single vocabulary $\mathcal{V}_1$.
2. **$B_{\text{single-centroid}}$ (EXP063 Internal Centroid Basis):** Exact winning basis from EXP063 ($\hat{v}_1 = \operatorname{normalize}(\sum_i \Delta h_{i,1} / \|\Delta h_{i,1}\|)$).
3. **$B_{\text{pool}}$ (Pooled Multi-Vocab SVD):** SVD on all pooled support contrasts across $K=5$ vocabularies.
4. **$B_{\text{agg}}$ (Normalized Multi-Vocab Aggregation):** Per-vocabulary normalized aggregation $v_{\text{agg}}$.
5. **$B_{\text{random}}$ (Norm-Matched Random Subspace):** 5-seed random null distribution with median energy calibration.
6. **$B_{\perp}$ (Orthogonal Complement):** Orthonormal vector in $\operatorname{ker}(B_{\text{agg}}^T)$.
7. **$B_{\text{wrong-task}}$:** Internal basis extracted from unrelated Level 0 lexical recall.
8. **Same-Layer Output Bridge ($v_{\text{output}}^{(10)}$):**
   - Output unembedding contrast vector $W_U[t] - W_U[f]$ evaluated at the **exact same layer** (Layer 10) to eliminate cross-layer depth confounds.

---

## 8. Epistemological Classification Ladder (Levels A, B, C)

To avoid premature claims of "invariance," experimental results are classified into three strict levels:

- **Level A — Cross-Vocabulary Alignment:**
  Satisfied if $\operatorname{mean}_{j \ne k} \cos(\hat{v}_j, \hat{v}_k) > 0.20$ ($p < 0.001$ vs. random null).
- **Level B — Cross-Vocabulary Causal Transfer:**
  Satisfied if:
  $$\Delta M(B_{\text{agg}}) > 0 \quad (p < 0.05) \quad \text{AND} \quad \Delta M(B_{\text{agg}}) > \Delta M(B_{\text{single}})$$
  on the unseen held-out vocabulary $\mathcal{D}_{\text{test}}$.
- **Level C — Lexically Invariant Computational Control:**
  Satisfied if Level B holds **AND** the basis survives EXP062/063 counterfactual controls (reversal deficit reduction $\ge 15\text{ pp}$, correct polarity inversion, and performance exceeding the same-layer output bridge control $v_{\text{output}}^{(10)}$).

*Constraint:* Only **Level C** justifies the term *"transferable relational representation"*.

---

## 9. Pre-Registered Scientific Fork (The Decision Tree)

$$\begin{array}{c}
\textbf{EXP064 Multi-Vocabulary Execution} \\
\Downarrow \\
\begin{array}{c|c}
\textbf{Outcome 1: Level B/C Transfer Succeeded} & \textbf{Outcome 2: Level B Transfer Failed} \\
\Delta M(B_{\text{agg}}) > \Delta M(B_{\text{single}}) \quad (p < 0.05) & \Delta M(B_{\text{agg}}) \approx 0.0\text{ pp} \quad (p \ge 0.05) \\
\Downarrow & \Downarrow \\
\textbf{EXP065: Specificity \& Robustness} & \textbf{EXP065: Temporary Coordinate Alignment} \\
\text{Stress-test circuit repairs, multi-hop depth,} & \text{Formalize local alignment operator } A_k: \\
\text{and cross-architecture scaling.} & h_k \xrightarrow{A_k} \tilde{h}_k \xrightarrow{B} \dots \text{ (True SCBI Lifecycle).}
\end{array}
\end{array}$$

---

## 10. Invariance Verification

- Target model: Frozen `EleutherAI/pythia-160m` ($\Delta\theta \equiv 0$).
- Immutability guarantee: Pre/post parameter SHA-256 verified invariant:
  `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936`.
