# EXP014 Protocol: Less-Destructive Representation Transformation Operators (Stage 1: Headroom Sweep)

**Protocol ID:** `EXP014`  
**Phase:** Stage 1 Confirmatory Headroom Sweep  
**Status:** Authorized by Peer Reviewer (Antigravity & ChatGPT Consensus)  
**Date:** 2026-09-11  
**Lead Implementer:** [`implementation-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/implementation-agent.md)  
**Independent Reviewer:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rules:** [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  
**Preceding Protocol:** [`EXP013_PRETRAINED_TRANSFORMER_SPEC.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/experiments/protocols/EXP013_PRETRAINED_TRANSFORMER_SPEC.md)

---

## 1. Scientific Objective & The Stage 1 Principle

EXP013 confirmed that the relational counterfactual evaluator $E_{\text{CF}}$ possesses statistically significant relative ranking ability on GPT-2 ($p = 0.0156$ under exact McNemar paired test, $R_E = +64.71\%$). However, the hard rank-2 all-token projection family possessed zero positive headroom over the unmodified model ($M_{\text{Oracle}} = 0.190 \ll M_{\text{Identity}} = 0.650$).

The research bottleneck has moved from the evaluator to the intervention generator:
$$\boxed{\text{EXP001–012: Evaluator Bottleneck}} \quad \Longrightarrow \quad \boxed{\text{EXP013: Intervention Generator Bottleneck}}$$

**Stage 1 Scientific Objective:**
$$\boxed{\textbf{Determine whether softening or localizing the intervention operator produces positive Oracle candidate headroom above Identity } (M_{\text{Oracle}} > M_{\text{Identity}} = 0.650).}$$

### The Strict Two-Stage Progression Principle:
$$\boxed{\text{Stage 1: Headroom Sweep (Oracle vs. Identity)}} \quad \longrightarrow \quad \boxed{\text{Stage 2: Relational Evaluator Selection (Only if Stage 1 Passes)}}$$
Evaluator $E_{\text{CF}}$ is **strictly sequestered** during Stage 1. No evaluation of candidate-selection mechanisms will be conducted unless and until an intervention configuration demonstrates statistically validated Oracle headroom above the frozen foundation model.

---

## 2. Inviolable Governance & Protocol Locks

1. **Fixed Backbone & Immutability:**
   - Model: HuggingFace `gpt2` (124M parameters, 12 layers, $d_{\text{model}} = 768$).
   - Parameter checksum verified via SHA-256 pre- and post-run:
     `6c12f993878ad39ba4aa3b0ab58a7466f5a62651cda94464dab438339008ba1d` ($\Delta\theta = 0$).
2. **Fixed Benchmark & Dataset:**
   - `BENCH-002-NL` ($N=100$ instances, seed 42, identical to EXP013).
3. **Fixed Candidate Construction:**
   - Candidates are generated from Layer 10 hidden states ($h_{10}$ at output of transformer block 9) via $K=4$ programmatic temporal quartiles:
     $$B_k = \left[ \left\lfloor \frac{(k-1)T}{4} \right\rfloor : \left\lfloor \frac{kT}{4} \right\rfloor \right], \quad k \in \{1, 2, 3, 4\}$$
   - Rank $r=2$ singular vectors $V_k \in \mathbb{R}^{d \times 2}$ ($V_k^\top V_k = I_2$).
   - Completely unchanged from EXP013. Only the operator and scope are varied.
4. **Exact Causal Graph & Computational Hook:**
   - Hook location: Output of transformer block $l-1 = 9$ (corresponding to Layer 10 residual stream).
   - Causal Graph:
     $$H_l \longrightarrow \begin{cases} h_{l, -1}' = P_\alpha h_{l, -1} & \text{Query-Token Only } (\mathcal{S}_{\text{query}}) \\ H_l' = P_\alpha H_l & \text{All-Token } (\mathcal{S}_{\text{all}}) \end{cases} \longrightarrow F_{\theta}^{>l} \longrightarrow q$$
   - In $\mathcal{S}_{\text{query}}$, all prefix token states $t < T-1$ remain completely unmodified.
   - Non-materialized contraction operator:
     $$h' = P_\alpha h = h - \alpha (h V) V^\top$$
     For $0 < \alpha < 1$, $P_\alpha^2 \neq P_\alpha$. The operator is a symmetric contraction along subspace $V$, scaling energy in $V$ by $(1-\alpha)$ while leaving $V^\perp$ invariant.

---

## 3. Pre-Registered $2 \times 5$ Multiplicity Family

The experiment tests exactly $J = 10$ non-trivial intervention configurations:

### Scopes ($\mathcal{S}$):
1. **$\mathcal{S}_{\text{query}}$ (Query-Token Only):** Only final token $h_{l, -1}$ modified.
2. **$\mathcal{S}_{\text{all}}$ (All-Token):** Entire residual stream $H_l$ modified.

### Contraction Strengths ($\alpha$):
- $\alpha \in \{0.05, 0.10, 0.25, 0.50, 1.00\}$

### Baseline Control ($\alpha = 0$):
$$\boxed{\alpha = 0 \equiv \text{Identity Baseline } (I)}$$
Unmodified forward pass ($M_{\text{Identity}} = 0.650$). $\alpha = 0$ is the reference control and is **not** counted in the multiplicity family.

---

## 4. Pre-Registered Multiplicity-Controlled Decision Rule

For each configuration $j \in \{1, \dots, 10\}$:
1. **Paired Contingency Counts vs. Identity:**
   $$b_j = \#(\text{Oracle}_j = 1, \text{Identity} = 0)$$
   $$c_j = \#(\text{Oracle}_j = 0, \text{Identity} = 1)$$
2. **Exact Paired Binomial Test:**
   $$p_j = \text{scipy.stats.binomtest}(b_j, b_j + c_j, p=0.5, \text{alternative}='greater')$$
3. **Family-Wise Error Rate (FWER) Multiplicity Control:**
   Apply Holm step-down adjustment across the 10 tests:
   $$p_j^{\text{Holm}} = \text{Holm-adjusted } p_j$$
4. **Effect Size & Bootstrap CI:**
   $$\Delta M_{\text{Oracle}, j} = M_{\text{Oracle}, j} - M_{\text{Identity}}$$
   with 95% bootstrap confidence interval $\text{CI}_j$.

### Formal Stage 1 Gate 1 Decision Rule:
$$\boxed{\text{Stage 1 PASS} \iff \exists j \in \{1, \dots, 10\}: \left[ \Delta M_{\text{Oracle}, j} > 0 \land \text{CI}_j \text{ excludes } 0 \land p_j^{\text{Holm}} < 0.05 \right]}$$

- **If Stage 1 Passes:** Advance the winning configuration(s) to Stage 2 to test whether $E_{\text{CF}}$ can reliably select the winning representations without labels.
- **If Stage 1 Fails:** Conclude that the temporal-quartile SVD candidate generator does not produce Top-1 improvements over frozen GPT-2 even under localized or continuous attenuation, directing future research to candidate generation rather than evaluator design.

---

## 5. Secondary Diagnostics
1. **Uninformed Cost Curve:** Track $M_{\text{Random}}(\alpha)$ for both scopes to map base fluency preservation.
2. **Degradation Response Surface:** Plot $\alpha \mapsto M_{\text{Oracle}}(\alpha)$ to measure the nonlinear intervention-strength tradeoff.
3. **Contrastive Distractor Margin:** Measure $\text{Pref}_{\text{Oracle}}(\alpha)$ and $\text{Pref}_{\text{Random}}(\alpha)$ to verify that distractor suppression operates across $\alpha$.
