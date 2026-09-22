# EXP013 Protocol: Pretrained Transformer Representation Search & Evaluator Transfer Study

**Protocol ID:** `EXP013`  
**Status:** Pre-Registered (Joint Collaboration: Antigravity & ChatGPT)  
**Date:** 2026-09-11  
**Lead Implementer:** [`implementation-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/implementation-agent.md)  
**Independent Reviewer:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rules:** [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  

---

## 1. Scientific Objective & Context

**Primary Research Question:**
$$\boxed{\textbf{Does a pretrained frozen transformer provide sufficiently rich relational response signals to make temporary candidate representations identifiable without labels?}}$$

Across EXP001–EXP012 on `BENCH-001`, two empirical realities were established:
1. **Candidate Generation and Candidate Identification are Separable Scientific Problems:** Under `BENCH-001`, the candidate generator reliably produced a pool containing task-improving interventions ($M_{\text{oracle}} \approx 50\% - 55\%$ vs. $M_{\text{baseline}} \approx 24\% - 28\%$, $p < 0.0001$).
2. **The Tested Classes of Label-Free Evidence Failed on BENCH-001:** Across intrinsic, local-counterfactual, and support-set evaluators, the synthetic architecture produced a weak counterfactual response channel ($D_{\text{JS}} \sim 10^{-3} - 10^{-2}$), preventing label-free evaluators from reliably selecting useful candidates.

EXP013 transitions to a pretrained language model (`GPT-2 124M`) to determine whether a rich linguistic representation space provides the response channel necessary for relational candidate evaluation.

---

## 2. Inviolable Governance & Protocol Safeguards

1. **Frozen Foundation Model ($\Delta\theta = 0$):**
   - Base model: HuggingFace `gpt2` (124M parameters, 12 layers, $d_{\text{model}} = 768$).
   - Parameter checksum verified via SHA-256 before and after execution:
     `6c12f993878ad39ba4aa3b0ab58a7466f5a62651cda94464dab438339008ba1d`.
2. **Controlled Task Benchmark (`BENCH-002-NL`):**
   - 100 instances across 5 balanced relational domains (Spatial, Travel, Temporal, Professional, Attributes).
   - Preserves exact causal topology of BENCH-001 with zero arithmetic or parsing confounds.
3. **Pre-Registered Semantic Perturbation Rules:**
   - **Semantic Paraphrase ($x^+$):** A predefined, meaning-preserving predicate paraphrase using synonymous relations. Distractor and query remain byte-for-byte identical.
   - **Semantic Counterfactual ($x^-$):** An orthogonal entity substitution in the premise predicate. Distractor and query remain byte-for-byte identical.
4. **Strict Zero-Label Leakage & Label-Free Candidate Generation:**
   - Candidate generator receives solely raw hidden states $H_l \in \mathbb{R}^{T \times d}$. It has ZERO access to semantic labels, entity spans, premise/distractor masks, or prompt syntax.
   - Slices hidden states into $K=4$ equal temporal quartiles:
     $$B_k = \left[ \left\lfloor \frac{(k-1)T}{4} \right\rfloor : \left\lfloor \frac{kT}{4} \right\rfloor \right], \quad k \in \{1, 2, 3, 4\}$$
   - Evaluator $E_{\text{CF}}$ uses *strictly* unlabeled model responses: $q_k(x)$, $q_k(x^+)$, $q_k(x^-)$. Ground-truth label $y$ is reserved exclusively for the downstream Oracle ceiling.
5. **Exact Residual-Stream Hook Location & Non-Materialized Operator:**
   - Explicit Layer Mapping: Layer index $l \in \{2, 4, 6, 8, 10\}$ corresponds to output of transformer block $b = l-1$ (`model.transformer.h[b]`), matching `hidden_states[l]` (where `hidden_states[0]` is the embedding).
   - Primary Intervention Scope: All residual-stream token states at the selected layer:
     $$H_l' = H_l - (H_l V) V^\top$$
     where $V \in \mathbb{R}^{d \times r}$ ($r=2$) is orthonormal.
   - Algebraic properties mathematically verified: $P^\top = P$ ($< 10^{-12}$), $P^2 = P$ ($< 10^{-12}$).
6. **Pre-Registered Layer Strategy:**
   - **Primary Analysis (Design A - Layer-Independent):** Evaluate candidates independently within each pre-registered layer:
     $$L \in \{2, 4, 6, 8, 10\}$$
   - **Secondary Analysis (Design B - Model-Level Search):** The search space is $\mathcal{C} = \{(l, k) : l \in L, k \in \{1,\dots,K\}\}$ ($|\mathcal{C}| = 20$). Random, $E_{\text{CF}}$, and Oracle search over the *exact same* layer $\times$ candidate space.

---

## 3. Candidate Generator Controls & Diversity Metrics

For each instance and layer $l$, the candidate pool includes:
1. **Control 0 (Identity Baseline):** $P_0 = I$ (unmodified residual stream).
2. **Control 1 (Matched Random Orthogonal Projection):** $V_{\text{rand}} \in \text{Stiefel}(d, 2)$ via QR decomposition of Gaussian matrix, matched in layer and rank.
3. **Control 2 (Fixed Candidate Baseline):** $k=1$ (first temporal quartile candidate) to diagnose candidate-ordering artifacts.
4. **Candidates (Temporal Quartile SVD Subspaces):** $V_k \in \mathbb{R}^{d \times 2}$ ($k \in \{1, 2, 3, 4\}$) spanning top 2 singular vectors of quartile slices $B_k$.
5. **Normalized Candidate Diversity Metric:**
   Record normalized pairwise subspace distance:
   $$D(P_i, P_j) = \frac{\|P_i - P_j\|_F}{\sqrt{2r}} = \sqrt{1 - \frac{1}{r} \|V_i^\top V_j\|_F^2} \in [0, 1]$$
   Logging mean, minimum, and maximum candidate diversity.

---

## 4. Evaluation Ladder & Evaluator Definitions

Across the matched candidate pool, evaluate:
1. **Identity Baseline:** $\hat{y}_{\text{id}} = \arg\max_w q_0(w \mid x)$
2. **Fixed Candidate Control:** $\hat{y}_{k=1} = \arg\max_w q_{k=1}(w \mid x)$
3. **Random Selection:** $P^*_{\text{random}} \sim \text{Uniform}(\{P_k\})$
4. **Intrinsic Energy Selection ($E_{\text{energy}}$):** $\arg\min_k \|H_l V_k\|_F / \|H_l\|_F$
5. **Counterfactual Consistency ($E_{\text{CF}}$):**
   $$E_{\text{CF}}(P_k) = D_{\text{JS}}(q_k(x), q_k(x^+)) - 0.5 \cdot D_{\text{JS}}(q_k(x), q_k(x^-))$$
   where $D_{\text{JS}}$ is the full vocabulary Jensen-Shannon divergence in nats.
6. **Directional NLL Diagnostic (Secondary Metric):**
   $$\Delta\text{NLL}_+(P_k) = \text{NLL}(y \mid x^+, P_k) - \text{NLL}(y \mid x, P_k)$$
   $$\Delta\text{NLL}_-(P_k) = \text{NLL}(y \mid x^-, P_k) - \text{NLL}(y \mid x, P_k)$$
7. **Oracle Upper Bound:**
   $$P^*_{\text{oracle}} = \arg\max_k \mathbf{1}[\hat{y}_k = y_{\text{true}}]$$
   with identically matched search space to Random and $E_{\text{CF}}$.

---

## 5. Pre-Registered Hypotheses & Status

- **Hypothesis H13-A (Response-Channel Dynamic Range):**  
  *Status:* **Pilot-supported** ($D_{\text{neg}}/D_{\text{pos}} = 4.00\times$, Wilcoxon $p = 0.0186$ on $n=10$), awaiting full benchmark confirmation.
- **Hypothesis H13-B (Candidate Selection Transfer):**  
  *Status:* **Untested — Confirmatory Phase B.**  
  $$\boxed{M(E_{\text{CF}}) > M(\text{Random})}$$
  Evaluated with cluster-aware 95% bootstrap confidence intervals and paired permutation tests.

---

## 6. Rigorous Compute Accounting

For every evaluation run, log:
- $N_{\text{forward}}$ (total forward model evaluations)
- $N_{\text{tokens}}$ (total processed tokens)
- Number of candidate evaluations
- Wall-clock time (seconds)
- Peak VRAM / Host RAM usage.
