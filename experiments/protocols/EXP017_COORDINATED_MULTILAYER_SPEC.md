# EXP017 Protocol Specification: Coordinated Multi-Layer SCBI

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP013 (Evaluator signal), EXP014 (Operator sweep), EXP015 (Generator characterization), EXP016 (Layer localization & confirmatory single-layer benchmark)  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Context & Research Question

Across four independent confirmatory benchmarks on `BENCH-002-NL` ($N=100$, Seed 42), every single-layer rank-2 continuous linear intervention at Layers 8 and 10 converged to an invariant empirical ceiling of $M_{\mathrm{Oracle}} \approx 0.7000 - 0.7100$ ($p \approx 0.09 - 0.11$, 95% bootstrap CIs spanning zero).

Crucially, contrastive preference climbed from $0.7900 \to 0.9100$, revealing that:
$$\boxed{\text{[OBSERVATION] The intervention alters internal representations in the intended direction,}}$$
$$\boxed{\text{but Top-1 generation does not reliably convert that representational change into the correct token.}}$$

EXP017 tests the coordinated multi-layer hypothesis:
$$\boxed{\text{[HYPOTHESIS] Can weak interventions distributed across multiple depths outperform the single-layer }0.71\text{ plateau?}}$$

---

## 2. Invariant Components & Protocol Locks

| Component | Protocol Lock | Epistemological Status |
| :--- | :--- | :--- |
| **Model** | Frozen HuggingFace `gpt2` (124M parameters, 12 layers) | `[FACT]` Pre-run & post-run SHA-256 parameter hash verification ($\Delta\theta = 0$) |
| **Dataset** | `BENCH-002-NL` ($N_{\mathrm{dev}}=20$, seed 123; $N_{\mathrm{conf}}=100$, seed 42) | `[FACT]` Fixed distractor suppression benchmark |
| **Generator** | Native $G4_{\mathrm{sparse}}$ Dictionary Atoms ($K=4, \text{rank}=2$) | `[DEFINITION]` Extracted from layer-specific representations |
| **Operator** | Continuous projector: $P_{\alpha_l} = I - \alpha_l V_l V_l^\top$ | `[DEFINITION]` Fluency-preserving contraction operator |
| **Budget Conservation** | **$A_{\mathrm{total}} = 0.25 \implies \alpha_l = \frac{0.25}{n}$** | `[ASSUMPTION]` Controls cumulative perturbation energy |
| **Scope** | All-token residual stream | `[DEFINITION]` Uniform sequence intervention |
| **Evaluator** | $E_{\mathrm{CF}}$ (Counterfactual consistency) | `[ASSUMPTION]` Sequestered until Gate 1 Oracle headroom is statistically demonstrated |
| **Baseline** | Identity ($\alpha = 0 \implies P = I, M_I = 0.6500$) | `[FACT]` Unperturbed foundation model performance |

### Conserved Intervention Budget Schedule:
- $n = 2$ layers: $\alpha_l = 0.1250$
- $n = 4$ layers: $\alpha_l = 0.0625$

---

## 3. Configurations & Mechanisms Evaluated (Phase A, $N_{\mathrm{dev}} = 20$)

### Depth Configurations:
1. $\{6, 8\}$ ($n=2, \alpha_l = 0.1250$)
2. $\{8, 10\}$ ($n=2, \alpha_l = 0.1250$)
3. $\{4, 8\}$ ($n=2, \alpha_l = 0.1250$)
4. $\{4, 6, 8, 10\}$ ($n=4, \alpha_l = 0.0625$)

### Coordination Mechanisms:
- **Mechanism 1 (M1 — Independent-Coordinate Intervention):**
  Bases $V_l = \mathcal{G}(H_l)$ are generated independently from the unperturbed forward pass activations at each depth. Projections are applied simultaneously across all layers in the configuration.
- **Mechanism 2 (M2 — Sequential Adaptive Intervention):**
  Activations are transformed sequentially:
  $$H_{l_1}' = P_{l_1} H_{l_1} \quad \longrightarrow \quad H_{l_2} = F^{l_1 \to l_2}(H_{l_1}') \quad \longrightarrow \quad V_{l_2} = \mathcal{G}(H_{l_2}) \quad \longrightarrow \quad H_{l_2}' = P_{l_2} H_{l_2} \dots$$
  Each subsequent candidate basis is fitted to the currently transformed representation state.

---

## 4. Elevated Diagnostic Suite

1. **Cross-Layer Synergy ($\Delta M_{\mathrm{synergy}}$):**
   $$\Delta M_{\mathrm{synergy}} = \Delta M_{\mathrm{combined}} - \sum_{l} \Delta M_l$$
   - $> 0$: Super-additive cross-layer synergy.
   - $\approx 0$: Independent additive corrections.
   - $< 0$: Destructive cross-layer interference.
2. **Probability Margin ($\Delta \mathrm{Margin}$):**
   $$\Delta \mathrm{Margin} = [p(y_{\mathrm{correct}}) - p(y_{\mathrm{distractor}})]_{\mathrm{SCBI}} - [p(y_{\mathrm{correct}}) - p(y_{\mathrm{distractor}})]_{\mathrm{Identity}}$$
3. **Correct Token Log-Probability Delta ($\Delta \log p$):**
   $$\Delta \log p(y_{\mathrm{correct}}) = \log p(y_{\mathrm{correct}})_{\mathrm{SCBI}} - \log p(y_{\mathrm{correct}})_{\mathrm{Identity}}$$
4. **Token Rank Shift ($\Delta \mathrm{rank}$):**
   $$\Delta \mathrm{rank}(y_{\mathrm{correct}}) = \operatorname{rank}(y_{\mathrm{correct}})_{\mathrm{Identity}} - \operatorname{rank}(y_{\mathrm{correct}})_{\mathrm{SCBI}}$$
5. **Residual Fluency Diagnostics:**
   Cumulative displacement $D_{\mathrm{cum}}$, output logit divergence $\Delta_{\mathrm{KL}}$, and top-10 vocabulary overlap $\operatorname{Overlap}_{10}$.

---

## 5. Decision Tree & Progression Rules

- **Phase A Screen ($N_{\mathrm{dev}} = 20$):**
  If any configuration and mechanism achieves $M_{\mathrm{Oracle}} \ge 0.75$ with positive cross-layer synergy ($\Delta M_{\mathrm{synergy}} > 0$) and stable logit preservation ($\operatorname{Overlap}_{10} \ge 0.75$), lock that single configuration for **Phase B Confirmatory Benchmark ($N=100$)**.
- **Negative Outcome Pathway:**
  If all multi-layer configurations remain bounded at $M_{\mathrm{Oracle}} \le 0.70$ without exceeding the single-layer plateau, conclude that linear multi-layer coordination is insufficient, directing research to nonlinear operators or higher-rank representations.
