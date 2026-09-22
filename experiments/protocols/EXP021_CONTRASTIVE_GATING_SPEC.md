# EXP021 Protocol Specification: Contrastive Relative-Evidence Gating

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP013–EXP020  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Context & Scientific Hypothesis

EXP020 demonstrated that feature projection energy $\|V^\top h_t\|_2$ is **not a sufficient selective criterion**:
- High projection energy tokens naturally encode general syntactic structure, punctuation, and salient semantic context alongside distractor bias.
- When intervention is concentrated on high-$e_t$ tokens to match linear corrective force, representation disruption worsens ($\Delta_{\mathrm{KL}}$ rose from $0.0971 \to 0.2120$).

EXP021 evaluates **relative contrastive evidence**:
$$\boxed{\text{[HYPOTHESIS] Intervening selectively where distractor representation explicitly dominates target representation}}$$
$$\boxed{(d_t = \|V_-^\top h_t\|_2 - \|V_+^\top h_t\|_2 > 0) \text{ isolates distractor bias without damaging general syntactic functionality.}}$$

---

## 2. Oracle-Free Basis Construction Protocol

To prevent any post-hoc data leakage or evaluator outcome contamination (Law 7):
1. **Pre-Registered Semantic Decomposition:**
   In `BENCH-002-NL`, every instance has two deterministic prompt segments:
   - Premise segment $P$ (introducing target entity) $\implies$ token range $\mathcal{T}_{\mathrm{premise}}$
   - Distractor segment $D$ (introducing distractor entity) $\implies$ token range $\mathcal{T}_{\mathrm{distractor}}$
2. **Subspace Generation at Layer 8:**
   - **Target Subspace $V_+ \in \mathbb{R}^{d \times 2}$:** Formed by rank-2 SVD on Layer 8 hidden states of the premise tokens $H[\mathcal{T}_{\mathrm{premise}}]$.
   - **Distractor Subspace $V_- \in \mathbb{R}^{d \times 2}$:** Formed by rank-2 SVD on Layer 8 hidden states of the distractor tokens $H[\mathcal{T}_{\mathrm{distractor}}]$.
3. **Provenance & Independence:**
   Both $V_+$ and $V_-$ are derived strictly from fixed prompt token representations prior to any intervention, candidate selection, or evaluation.

---

## 3. Relative Contrastive Evidence & Exact Magnitude Matching

For each token representation $h_t \in \mathbb{R}^d$ ($t \in \{1, \dots, T\}$) at Layer 8:
- Distractor feature energy: $e_t^- = \|V_-^\top h_t\|_2$
- Target feature energy: $e_t^+ = \|V_+^\top h_t\|_2$
- Relative evidence difference:
  $$d_t = e_t^- - e_t^+$$

### Exact Realized Intervention Magnitude Matching:
Unlike mean-gate normalization ($\bar{g}=1.0$), which allows realized displacement to vary, EXP021 enforces **exact realized magnitude matching**:
$$h_t' = h_t - \alpha s g_t V_- V_-^\top h_t \quad (\alpha = 0.25)$$
where the instance-specific analytical scale $s$ is:
$$s = \frac{\sqrt{\sum_{t=1}^T \|V_-^\top h_t\|_2^2}}{\sqrt{\sum_{t=1}^T g_t^2 \|V_-^\top h_t\|_2^2}}$$
This guarantees that:
$$\frac{\|H_{\mathrm{gated}}' - H\|_F}{\|H\|_F} \equiv \frac{\|H_{\mathrm{linear}}' - H\|_F}{\|H\|_F} = A_{\mathrm{linear}} \quad \text{on EVERY forward pass.}$$

---

## 4. Operators Evaluated

1. **O0 (Uniform Linear Baseline Control):**
   $$g_t = 1.0 \implies s = 1.0 \implies h_t' = h_t - 0.25 V_- V_-^\top h_t$$
2. **O5 (Contrastive Hard Gate):**
   $$g_t = \mathbf{1}[d_t > 0] \implies h_t' = h_t - 0.25 s \cdot \mathbf{1}[d_t > 0] \cdot V_- V_-^\top h_t$$
   *(Intervenes strictly when distractor evidence strictly exceeds target evidence).*
3. **O6 (Contrastive Soft Sigmoid Gate — Primary Operator):**
   $$g_t = \sigma\left(\frac{d_t}{T_d}\right) \quad \text{with} \quad T_d = \operatorname{std}(d_t) + 10^{-8}$$
   $$h_t' = h_t - 0.25 s g_t V_- V_-^\top h_t$$

---

## 5. Diagnostic Suite

1. **Contrastive Selectivity:**
   - $D_{d^+}$: Relative displacement on tokens where $d_t > 0$
   - $D_{d^-}$: Relative displacement on tokens where $d_t \le 0$
   - Prediction: $D_{d^+} \gg D_{d^-}$
2. **Gate/Evidence Correlation:**
   $$\rho(g_t, d_t) = \frac{\operatorname{Cov}(g_t, d_t)}{\sigma_g \sigma_d}$$
3. **Realized Magnitude Verification:**
   Confirm $A_{\mathrm{O5}} \equiv A_{\mathrm{O6}} \equiv A_{\mathrm{O0}}$.
4. **Logit Preservation:** $\Delta_{\mathrm{KL}}$ and $\operatorname{Overlap}_{10}$.
5. **Target Log-Probability & Rank Shift:** $\Delta \log p(y_{\mathrm{correct}})$ and $\Delta \operatorname{rank}(y_{\mathrm{correct}})$.
6. **Task Performance:** $M_{\text{Oracle}}, M_{\text{RandCand}}, \text{Pref}_{\text{Oracle}}$.

---

## 6. Pre-Registered Decision Criteria

```text
EXP021: Contrastive Relative-Evidence Screen (N=20)
Linear (O0) vs. Contrastive Hard (O5) vs. Contrastive Soft (O6)
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
          Case A: Selective Gain        Case B: Selective Failure
          (M >= 0.80, KL <= KL_O0)      (M < 0.80 or KL > KL_O0)
                 │                             │
                 ▼                             ▼
          Relative evidence is the      Residual stream distractor
          correct selective filter;     cannot be isolated by linear
          lock O6 for Confirmatory      projections of token states;
          Benchmark (N=100).            investigate attention head intervention.
```
