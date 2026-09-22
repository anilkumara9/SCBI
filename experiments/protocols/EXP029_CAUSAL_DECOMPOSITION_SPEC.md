# EXP029: Causal Decomposition & Rescue of SCBI Intervention-Stage Viability in Pythia-160M

## 1. Executive Summary & Purpose

- **Experiment ID:** `EXP029`
- **Model:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision: `e72e396263595503028d71243171317d7ae65463`).
- **Core Motivation:** In EXP027, Pythia-160M exhibited an empirical contrast:
  - **Layer 4:** $M_I = 0.5900 \to M_{\mathrm{Oracle}} = 0.7100$ ($\Delta M = +0.1200, p = 0.000916$, McNemar $13/1$, Wilcoxon $p = 4.77 \times 10^{-10}$).
  - **Layer 8:** $M_I = 0.5900 \to M_{\mathrm{Oracle}} = 0.5900$ ($\Delta M = 0.0000, p = 1.0000$, complete failure).
  - In EXP028, the representation score $S_{\mathrm{representation}}(l)$ successfully located viable intervention regions across unseen architectures (OPT-125M, Qwen2.5-0.5B, BLOOM-560M).
- **Core Research Question:**
  > **What causal geometric or computational property makes an intermediate layer viable for frozen-backbone SCBI intervention, and can we experimentally demonstrate both loss-of-function (destroying efficacy at L4) and gain-of-function rescue (restoring efficacy at L2 or L8)?**
- **Epistemological Framing:** Causal decomposition across 5 non-mutually exclusive candidate mechanisms (H1: Downstream Receptivity, H2: Linear Decoupling, H3: Dimensional Bottleneck, H4: Attention Rerouting, H5: Unembedding Alignment).

---

## 2. Inviolable Governance Locks & Protocol Boundaries

1. **Law 1 & 6 (Frozen Backbone):** Model parameters $\theta_t \equiv \theta_0$ remain invariant throughout inference ($\Delta\theta = 0$). Parameter SHA-256 hash verified before and after all runs (`d359b8d0034a742880c5980757d54d24a66a1c1d8825c04ae1ad6b0c6dfec610`).
2. **Law 7 (Data Leakage & Diagnostic Separation):**
   - **Phase A (Label-Free Diagnostics):** Evaluated strictly on $N_{\mathrm{calib}}=20$ unlabeled prompt representations (Seed 123). Zero benchmark labels or target answers are revealed.
   - **Phase B (Mechanistic Probes):** Evaluated on $N=100$ instances of `BENCH-002-NL` (Seed 84) strictly *after* observational profiles are locked, used exclusively for causal intervention experiments.
3. **Preservation of Prior Evidence:** EXP028a, EXP028b, and EXP028c remain permanently frozen and unmodified.

---

## 3. Mathematical Definitions of Evaluated Properties

### 3.1 Label-Free Diagnostics (Phase A)

1. **Intrinsic Dimensionality via Participation Ratio ($\mathrm{PR}$):**
   For residual activations $h_l \in \mathbb{R}^{d}$ across prompt positions on unlabeled calibration prompts:
   $$\Sigma_l = \frac{1}{N}\sum_{i=1}^N (h_l^{(i)} - \bar{h}_l)(h_l^{(i)} - \bar{h}_l)^\top$$
   $$\mathrm{PR}(l) = \frac{\left(\operatorname{Tr}(\Sigma_l)\right)^2}{\operatorname{Tr}\left(\Sigma_l^2\right)} = \frac{\left(\sum_{k=1}^d \sigma_k\right)^2}{\sum_{k=1}^d \sigma_k^2} \in [1, d]$$
2. **Downstream Suffix Jacobian Receptivity ($\mathcal{J}$):**
   Sensitivity of final output logits to isotropic residual perturbations $\delta \sim \mathcal{N}(0, \sigma_h^2 I)$ at layer $l$:
   $$\mathcal{J}(l) = \mathbb{E}_{x, \delta}\left[ \frac{\|f^{>l}(h_l + \delta) - f^{>l}(h_l)\|_2}{\|\delta\|_2} \right]$$
3. **Downstream Attention Sensitivity ($\Delta\mathcal{A}$):**
   Total variation shift in multi-head attention weight distributions across downstream layers $l' > l$ induced by residual shift:
   $$\Delta\mathcal{A}(l) = \frac{1}{L - 1 - l} \sum_{l'=l+1}^{L-1} \frac{1}{H}\sum_{h=1}^H \|A_{l', h}(h_l + \delta) - A_{l', h}(h_l)\|_{\mathrm{TV}}$$
4. **Empirical Representation Predictor ($S_{\mathrm{representation}}$):**
   $$S_{\mathrm{representation}}(l) = \mathrm{SI}_{\mathrm{rep}}(l) \times \mathcal{O}_{\mathrm{subspace}}(l)$$

### 3.2 Post-Hoc Mechanistic Probes (Phase B)

1. **Linear Fisher Contrastive Separation ($\mathcal{F}$):**
   $$\mathcal{F}(l) = \frac{\left(v_{\mathrm{diff}}^\top (\mu_{\mathrm{tgt}}^{(l)} - \mu_{\mathrm{dist}}^{(l)})\right)^2}{v_{\mathrm{diff}}^\top \left(\Sigma_{\mathrm{tgt}}^{(l)} + \Sigma_{\mathrm{dist}}^{(l)}\right) v_{\mathrm{diff}}}$$
2. **Direct Unembedding Alignment ($\rho_U$):**
   Cosine similarity between the candidate projection basis $V_l$ and the unembedding difference vector $w_{\mathrm{diff}} = W_U[\text{target}] - W_U[\text{distractor}]$:
   $$\rho_U(l) = \frac{\|V_l^\top w_{\mathrm{diff}}\|_2}{\|w_{\mathrm{diff}}\|_2}$$

---

## 4. Experimental Execution Architecture

### Layer A: Observational Profiling (Layers 0 to 11 in Pythia-160M)
- Compute full layer-wise profiles for $\mathrm{PR}(l)$, $\mathcal{J}(l)$, $\Delta\mathcal{A}(l)$, $S_{\mathrm{rep}}(l)$, and $\rho_U(l)$.
- Analyze contrast between known viable layer ($L4$) and known non-viable layer ($L8$).

### Layer B: Loss-of-Function Causal Manipulations (At Viable Layer 4)
1. **Subspace Angle Sweep (Testing H2):** Rotate candidate basis $V$ away from the contrastive direction:
   $$V(\theta) = \cos(\theta) v_{\parallel} + \sin(\theta) v_{\perp}, \quad \theta \in \{0^\circ, 30^\circ, 60^\circ, 90^\circ\}$$
   *Falsification Criterion:* If $\Delta M(90^\circ) \ge 0.80 \Delta M(0^\circ)$, H2 is falsified.
2. **Attention Map Clamping (Testing H4):** Inject standard SCBI at Layer 4, but clamp all downstream attention weights $A_{l'>4, h} \longleftarrow A_{l'>4, h}^{\mathrm{unperturbed}}$:
   *Falsification Criterion:* If clamping attention preserves $\ge 80\%$ of Oracle headroom, H4 (attention rerouting as primary vehicle) is ruled out as necessary.
3. **Unembedding Orthogonalization (Testing H5):** Project candidate basis $V$ orthogonal to $w_{\mathrm{diff}}$:
   $$V_{\perp} = \left(I - \frac{w_{\mathrm{diff}} w_{\mathrm{diff}}^\top}{\|w_{\mathrm{diff}}\|_2^2}\right) V$$
   *Falsification Criterion:* If $V_{\perp}$ preserves $\ge 80\%$ of Oracle headroom, H5 (direct unembedding readout) is ruled out as necessary.

### Layer C: Gain-of-Function Rescue Manipulations (At Non-Viable Layers 2 and 8)
1. **Early-Layer Rescue via Suffix Gain Attenuation (Layer 2):**
   Attenuate downstream residual gain $\gamma \in \{0.5, 0.75, 1.0\}$ in layers $l' \in [3, 11]$:
   $$h_{l'+1} = h_{l'} + \gamma \cdot \Delta h_{\mathrm{block}}(h_{l'})$$
   *Criterion:* Does reducing downstream chaotic amplification unmask positive intervention headroom at Layer 2?
2. **Late-Layer Rescue via Unembedding Realignment (Layer 8):**
   Explicitly orient intervention basis along the unembedding difference vector $w_{\mathrm{diff}}$ at Layer 8.
   *Criterion:* Does supplying direct readout leverage restore headroom at Layer 8?

---

## 5. Decision Tree & Scientific Falsification Rules

1. **If Test B1 shows monotonic drop to zero as $\theta \to 90^\circ$:** Linear Decoupling ($\mathcal{F}$) is a **necessary condition**.
2. **If Test B2 destroys headroom upon attention clamping:** Downstream Attention Rerouting is a **necessary vehicle**.
3. **If Test B3 preserves headroom when $V \perp w_{\mathrm{diff}}$:** Direct Unembedding Readout is **not necessary**; the intervention operates via non-linear suffix transformation.
4. **If Test C1 restores headroom at Layer 2:** Downstream suffix chaos is the **causal bottleneck** preventing early-layer viability.
5. **Abandonment Threshold:** If the causal angle sweep shows that arbitrary orthogonal directions in Layer 4 produce identical headroom, or if an alternative latent variable predicts stage efficacy with strictly higher fidelity than $S_{\mathrm{representation}}$, we will explicitly replace $S_{\mathrm{representation}}$ in the project ledger.
