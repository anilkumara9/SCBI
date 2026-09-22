# EXP020 Protocol Specification: Budget-Matched Feature-Dependent Operator

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP013–EXP019  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Context & Scientific Hypothesis

EXP019 demonstrated that token-level activation gating significantly improves representation preservation ($\Delta_{\mathrm{KL}}$ reduced by up to 55%, from $0.0971 \to 0.0433$; Top-10 vocabulary overlap rose from $85.25\% \to 89.87\%$). However, under unnormalized gating, the effective sequence intervention budget dropped to $B_{O1} = 0.2535$ and $B_{O2} = 0.4986$ (vs. $B_{O0} = 1.0$), attenuating the total corrective force and reducing Oracle accuracy from $0.8000 \to 0.7000$.

EXP020 addresses this causal ambiguity by testing **budget-matched selective intervention**:
$$\boxed{\text{[HYPOTHESIS] Normalizing the token gate so that the sequence mean intervention budget matches linear } (\bar{g}=1.0)}$$
$$\boxed{\text{will restore Oracle headroom while preserving the logit selectivity advantages of gating.}}$$

---

## 2. Invariant Components & Protocol Locks

| Component | Protocol Lock | Epistemological Status |
| :--- | :--- | :--- |
| **Model** | Frozen HuggingFace `gpt2` (124M parameters, 12 layers) | `[FACT]` Pre-run & post-run SHA-256 parameter hash verification ($\Delta\theta = 0$) |
| **Benchmark** | `BENCH-002-NL` ($N_{\mathrm{dev}}=20$, seed 123; $N_{\mathrm{conf}}=100$, seed 42) | `[FACT]` Fixed distractor suppression benchmark |
| **Layer** | **Layer 8** (Block 7 output) | `[DEFINITION]` Optimal single-layer depth |
| **Generator** | Native $G4_{\mathrm{sparse}}$ Dictionary Atoms ($K=4$) | `[DEFINITION]` $n_{\mathrm{atoms}} = 8$ atoms learned per layer |
| **Subspace Rank** | **$r = 2$** | `[DEFINITION]` Optimal linear dimensionality |
| **Base Strength** | **$\alpha = 0.25$** | `[DEFINITION]` Optimal continuous intervention strength |
| **Scope** | All-token residual stream (modulated by normalized gate $\tilde{g}_t$) | `[DEFINITION]` Sequence-normalized token gating |
| **Evaluator** | $E_{\mathrm{CF}}$ (Counterfactual consistency) | `[ASSUMPTION]` Sequestered until Gate 1 Oracle headroom is demonstrated |
| **Baseline** | Identity ($\alpha = 0 \implies P = I, M_I = 0.6500, \text{Pref}_I = 0.9000$) | `[FACT]` Unperturbed foundation model performance |

---

## 3. Operator Formulations: Budget Normalization

For sequence token representations $h_t \in \mathbb{R}^d$ ($t \in \{1, \dots, T\}$) at Layer 8:
- Feature projection: $z_t = V^\top h_t \in \mathbb{R}^2$.
- Feature activation energy: $e_t = \|z_t\|_2 = \|V^\top h_t\|_2$.
- Standardized prompt energy: $\hat{e}_t = \frac{e_t - \mu_e}{\sigma_e + \epsilon}$.

### Operators Compared:
1. **O0 (Uniform Linear Baseline Control):**
   $$g_t = 1.0 \implies \tilde{g}_t = 1.0 \implies h_t' = h_t - 0.25 V V^\top h_t$$
   $$\bar{g} = \frac{1}{T} \sum_{t=1}^T g_t = 1.0$$
2. **O3 (Budget-Normalized Hard Gate):**
   $$g_t = \mathbf{1}[e_t > P_{75}(e)]$$
   $$\tilde{g}_t = \frac{g_t}{\bar{g}} \quad \text{where} \quad \bar{g} = \frac{1}{T}\sum_{t=1}^T g_t$$
   $$h_t' = h_t - 0.25 \tilde{g}_t V V^\top h_t$$
   *(Note: Since $\bar{g} \approx 0.25$, active tokens receive $\tilde{g}_t \approx 4.0 \implies \alpha_{\mathrm{eff}} \approx 1.0$, while inactive tokens receive $0$).*
3. **O4 (Budget-Normalized Soft Sigmoid Gate):**
   $$g_t = \sigma\left(\frac{\hat{e}_t - \tau}{T_{\mathrm{temp}}}\right) \quad \text{with} \quad \tau = P_{75}(\hat{e}), \; T_{\mathrm{temp}} = 1.0$$
   $$\tilde{g}_t = \frac{g_t}{\bar{g}} \quad \text{where} \quad \bar{g} = \frac{1}{T}\sum_{t=1}^T g_t$$
   $$h_t' = h_t - 0.25 \tilde{g}_t V V^\top h_t$$

By construction:
$$\frac{1}{T} \sum_{t=1}^T \tilde{g}_t \equiv 1.0 \quad \text{for all operators (O0, O3, O4)}$$

---

## 4. Diagnostics & Explicit Energy Concentration Metrics

1. **Mean Gate Activation Budget ($B$):**
   $$B = \frac{1}{T} \sum_{t=1}^T \tilde{g}_t = 1.0000$$
2. **Total Intervention Magnitude ($A$):**
   $$A = \frac{\sum_t \|h_t' - h_t\|_2}{\sum_t \|h_t\|_2}$$
3. **Partitioned Selective Displacement ($D_{\mathrm{high}}$ vs. $D_{\mathrm{low}}$):**
   - High-energy tokens: $\mathcal{T}_{\mathrm{high}} = \{t : e_t > P_{75}(e)\} \implies D_{\mathrm{high}} = \frac{1}{|\mathcal{T}_{\mathrm{high}}|} \sum_{t \in \mathcal{T}_{\mathrm{high}}} \frac{\|h_t' - h_t\|_2}{\|h_t\|_2}$
   - Low-energy tokens: $\mathcal{T}_{\mathrm{low}} = \{t : e_t \le P_{75}(e)\} \implies D_{\mathrm{low}} = \frac{1}{|\mathcal{T}_{\mathrm{low}}|} \sum_{t \in \mathcal{T}_{\mathrm{low}}} \frac{\|h_t' - h_t\|_2}{\|h_t\|_2}$
4. **Energy Concentration Metrics Across Sequence:**
   - Probability distribution over sequence tokens:
     $$q_t = \frac{e_t}{\sum_{j=1}^T e_j}$$
   - Shannon entropy of energy distribution:
     $$H(q) = -\sum_{t=1}^T q_t \log q_t$$
   - Normalized entropy ratio: $H(q) / \log(T) \in [0, 1]$ (1.0 = completely uniform; 0.0 = completely localized).
   - Effective number of tokens expressing the feature:
     $$N_{\mathrm{eff}} = \frac{1}{\sum_{t=1}^T q_t^2}$$
   - Effective token support fraction: $N_{\mathrm{eff}} / T$.
5. **Causal Attention Propagation Diagnostic:**
   - Measure relative hidden state change at the final layer (Layer 12 output):
     $$\Delta_{\mathrm{prop}} = \frac{\|h_{12}' - h_{12}\|_F}{\|h_{12}\|_F}$$
6. **Logit Preservation Diagnostics:** $\Delta_{\mathrm{KL}}$ and $\operatorname{Overlap}_{10}$.
7. **Target Metrics:** $\Delta \mathrm{Margin}$, $\Delta \log p$, target rank shift.

---

## 5. Pre-Registered Decision Branches

```text
EXP020: Budget-Matched Feature-Dependent Screen (N=20)
Uniform (O0) vs. Budget-Normalized Hard (O3) vs. Budget-Normalized Soft (O4)
                               │
                ┌──────────────┴──────────────┐
                │                             │
          Case A: Headroom              Case B: Headroom
          Restored (M >= 0.80)          Stagnates (M <= 0.70)
                │                             │
                ▼                             ▼
          Budget deficiency             Feature energy (||V^T h||)
          was the limiting factor;      is NOT the right semantic gate;
          selectivity validated.        conflates syntax with distractor.
                │                             │
                ▼                             ▼
          Lock winning operator         Proceed to Contrastive Gating
          for Confirmatory (N=100)      g_t = sigma((e_t^- - e_t^+ - tau)/T)
```
