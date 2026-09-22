# EXP015 Protocol: Representational Locality & Candidate Generator Redesign

**Protocol ID:** `EXP015`  
**Status:** Pre-Registered (Joint Collaboration: Antigravity & ChatGPT)  
**Date:** 2026-09-11  
**Lead Implementer:** [`implementation-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/implementation-agent.md)  
**Independent Reviewer:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rules:** [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  
**Preceding Protocols:** [`EXP013_PRETRAINED_TRANSFORMER_SPEC.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/experiments/protocols/EXP013_PRETRAINED_TRANSFORMER_SPEC.md), [`EXP014_LESS_DESTRUCTIVE_OPERATORS_SPEC.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/experiments/protocols/EXP014_LESS_DESTRUCTIVE_OPERATORS_SPEC.md)

---

## 1. Scientific Objective & The Core Paradigm Shift

In EXP014, testing less-destructive continuous operators ($P_\alpha = I - \alpha V V^\top$) revealed that softening to $\alpha = 0.25$ lifted nominal Oracle accuracy to $0.710$ ($+6\%$ over baseline, with $11$ wins vs. $5$ regressions), but failed confirmatory FWER significance ($p^{\text{Holm}} = 1.00$, bootstrap CI $[-0.01, +0.14]$).

This localized the fundamental bottleneck:
$$\boxed{\text{EXP013: Evaluator Works}} \quad \longrightarrow \quad \boxed{\text{EXP014: Operator } P_{0.25} \text{ Preserves Fluency}} \quad \longrightarrow \quad \boxed{\text{EXP015: Candidate Generator } \mathcal{G} \text{ is the Bottleneck}}$$

Arbitrary temporal quartiles $B_k = [(k-1)T/4 : kT/4]$ assume that *tokens occurring at similar positions represent the same semantic feature*. In pretrained language models, this assumption fails: temporal slicing extracts directions that entangle task distractors with base grammatical fluency.

**Core Research Hypothesis ($H_1$):**
$$\boxed{\textbf{Candidate directions localized by representational geometry / feature activity rather than arbitrary temporal position will produce greater Oracle headroom than temporal-quartile SVD.}}$$

---

## 2. Inviolable Governance & Experimental Invariants

To guarantee rigorous causal attribution ($\mathcal{G}_{\text{old}} \to \mathcal{G}_{\text{new}}$), all other pipeline elements remain strictly frozen:
1. **Frozen Foundation Model ($\Delta\theta = 0$):**
   HuggingFace `gpt2` (124M parameters, 12 layers, $d_{\text{model}} = 768$). Parameter checksum audited via SHA-256 pre- and post-run:
   `6c12f993878ad39ba4aa3b0ab58a7466f5a62651cda94464dab438339008ba1d`.
2. **Fixed Intervention Operator:**
   $P_\alpha = I - \alpha V V^\top$ locked at $\mathbf{\alpha = 0.25}$ across all candidates.
3. **Fixed Intervention Scope & Location:**
   All residual-stream token states at Layer 10 block output (`model.transformer.h[9]`).
4. **Reference Baseline Control:**
   Identity ($\alpha = 0 \equiv I$, $M_{\text{Identity}} = 0.650$).
5. **Sequestered Evaluator Guarantee:**
   Evaluator $E_{\text{CF}}$ is strictly sequestered until Gate 1 Oracle headroom is statistically proven.
6. **Benchmark Dataset:**
   `BENCH-002-NL` (controlled natural-language distractor benchmark).

---

## 3. Candidate Generator Families Under Evaluation

For an instance with hidden sequence states $H_l = [h_1, \dots, h_T]^\top \in \mathbb{R}^{T \times d}$:

### G0 (Baseline Control — Temporal Quartiles):
Divided into 4 equal sequence quartiles $B_k = [(k-1)T/4 : kT/4]$, with $V_k \in \mathbb{R}^{d \times 2}$ spanning top 2 singular vectors of $B_k$.

### G1 (Primary Candidate — Activation-Clustered Subspaces):
Clusters tokens by representational similarity:
1. Normalized representations: $\tilde{h}_t = h_t / \|h_t\|_2$ for $t \in \{1, \dots, T\}$.
2. Cluster into $K=4$ clusters $\{C_1, C_2, C_3, C_4\}$ via cosine distance clustering.
3. For each cluster $k$, extract centered top-2 singular vectors:
   $$V_k = \text{SVD}_{r=2}\left(\{h_t - \mu_k : t \in C_k\}\right)$$
   where $\mu_k = \frac{1}{|C_k|} \sum_{t \in C_k} h_t$. (If $|C_k| < 2$, pad with orthogonal random vectors).

### G2 (Principal Covariance / Global PCA Directions):
Extracts directions of maximum global representation variance:
1. Centered sample covariance: $\Sigma = \frac{1}{T-1} \sum_{t=1}^T (h_t - \bar{h})(h_t - \bar{h})^\top$.
2. Spectral decomposition $\Sigma = U \Lambda U^\top$.
3. Subspaces from consecutive principal pairs: $V_k = [u_{2k-1}, u_{2k}] \in \mathbb{R}^{d \times 2}$ for $k \in \{1, 2, 3, 4\}$.

### G4 (Sparse Feature Dictionary Decomposition):
Decomposes hidden states into sparse latent dictionary atoms:
1. Dictionary learning over instance representations: $H \approx Z D$ with $D \in \mathbb{R}^{m \times d}$ and sparse $Z$.
2. Candidate subspaces constructed from leading dictionary atom pairs.

---

## 4. Candidate-Quality Metrics Suite

Before evaluating downstream Top-1 accuracy, each candidate pool is characterized across:
1. **Locality ($L$):** Activation energy concentration:
   $$L(V_k) = \frac{\|H V_k\|_F^2}{\|H\|_F^2}$$
2. **Orthogonality / Diversity ($\bar{D}$):** Normalized Grassmanian distance:
   $$\bar{D} = \frac{1}{\binom{K}{2}} \sum_{i < j} \sqrt{1 - \frac{1}{r} \|V_i^\top V_j\|_F^2} \in [0, 1]$$
3. **Subspace Stability ($\operatorname{Sim}$):** Principal-angle similarity across bootstrap token resamples within the prompt:
   $$\operatorname{Sim}(V, V') = \frac{1}{r} \|V^\top V'\|_F^2 \in [0, 1]$$

---

## 5. Two-Stage Execution Workflow

### Phase EXP015-A (Diagnostic Development Pass):
- Evaluate G0, G1, G2, G4 on $N_{\text{dev}} = 20$ development instances.
- Compute candidate-quality metrics, descriptive Oracle headroom ($M_{\text{Oracle}} - M_{\text{Identity}}$), and the Oracle-vs-Random spread ($M_{\text{Oracle}} - M_{\text{Random}}$).
- Lock the single most promising generator family.

### Phase EXP015-B (Confirmatory Benchmark):
- Freeze the locked generator from Phase A.
- Execute full confirmatory run on $N=100$ instances of `BENCH-002-NL`.
- Primary confirmatory endpoint:
  $$\boxed{\text{PASS} \iff \Delta M_{\text{Oracle}} > 0 \land \text{CI}_{95\%} > 0 \land p_{\text{exact}} < 0.05 \land (M_{\text{Oracle}} - M_{\text{Random}} > 0)}$$
- If Gate 1 passes with statistical significance, advance to testing $E_{\text{CF}}$ selection on the winning pool.
