# EXP066 Protocol Specification: Cross-Scale Replication on Pythia-410M

**Status:** PRE-REGISTERED (Replication Protocol)  
**Date:** 2026-09-23  
**Predecessor Experiments:** EXP063 (Internal-State Basis), EXP064 (Multi-Vocabulary Aggregation Boundary), EXP065 (Temporary Coordinate Alignment Operator)  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws, esp. Law 1: Read Before Modifying, Law 6: Frozen Backbone, Law 7: Zero Data Leakage, Law 10: Premature Novelty, Law 13: Deterministic Reproducibility) & `STATISTICAL_PROTOCOL_V02.md`  
**Execution Rule:** Strictly confirmatory replication. No retuning of EXP065 mechanism or intervention hyperparameters ($\alpha = 0.50$) prior to primary evaluation.

---

## 1. Research Question and Replication Hypothesis

### 1.1 Central Scientific Question
$$\boxed{\textbf{Does the EXP063–EXP065 representational–causal boundary replicate at a larger frozen Pythia scale?}}$$

In EXP065 (`pythia-160m`, $d=768$, 12 layers), we established strong boundary evidence:
- Support representations from independent vocabularies exhibit geometric alignment under closed-form orthogonal Procrustes rotation ($\Delta \cos \approx +0.13$).
- However, injecting the dynamic coordinate-aligned internal basis into the residual stream at Layer 10 yielded **strictly zero behavioral rescue** ($\Delta M = 0.0\text{ pp}, p = 1.0000; 0/19\text{ rescues}, 0/19\text{ corruptions}$) on a difficulty-calibrated benchmark with 68.3% baseline accuracy.
- In contrast, the same-layer output bridge control produced $+16.7\text{ pp}$ accuracy gain ($p = 0.0020; 10/19\text{ rescues}$), proving that the intermediate representation layer had unblocked causal access to the language modeling head.

EXP066 tests whether this dissociation between representational alignment and causal interchangeability is an artifact of the 160M parameter scale or reflects a robust architectural boundary preserved across model scaling.

### 1.2 Formal Hypotheses
- **Null Hypothesis ($H_0$):**
  $$\Delta M(\text{Dynamic Coordinate-Aligned Internal Basis}) = 0$$
  The dynamically aligned internal basis produces no statistically significant net rescue over the frozen unintervened baseline ($p \ge 0.05$), while the same-layer output bridge achieves $\Delta M > 0$ ($p < 0.05$).
- **Alternative Hypothesis ($H_1$ — Emergence of Causal Interchangeability):**
  $$\Delta M(\text{Dynamic Coordinate-Aligned Internal Basis}) > 0 \quad (p < 0.05)$$
  At 410M parameter scale, internal coordinate-aligned states acquire causal efficacy across disjoint vocabularies, significantly exceeding both the static basis and random orthogonal rotations.

---

## 2. Frozen Model and SHA-256 Verification

- **Model Identifier:** `EleutherAI/pythia-410m`
- **Tokenizer Identifier:** `EleutherAI/pythia-410m`
- **Architecture:** GPT-NeoX Transformer (Rotary Position Embeddings, Parallel Attention/MLP, Untied Output Embeddings)
- **Parameters:** $405{,}081{,}600$
- **Hidden Dimension ($d$):** $1024$
- **Number of Hidden Layers:** $24$
- **Attention Heads:** $16$
- **Intermediate Dimension:** $4096$
- **Weight Hash Standard:**
  Before and after all interventions, the exact SHA-256 hash of all model tensor parameters must match:
  $$\boxed{\text{SHA-256: } \texttt{4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd}}$$
- **Immutability Mandate:** $\Delta \theta \equiv 0$. No weights, biases, layernorms, or buffers may be updated during any stage of execution.

---

## 3. Exact Benchmark and Headroom Criterion

### 3.1 Benchmark Instance Structure ($N=60$)
The benchmark is identically ported from EXP065 to eliminate confounders:
- **Disjoint Novel Domains:**
  1. Planetary domain ($N=30$): `Mars`, `Venus`, `Jupiter`, `Saturn`, `Mercury`
  2. Elemental domain ($N=30$): `Iron`, `Gold`, `Silver`, `Bronze`, `Steel`
- **Hop Depths:**
  - $30$ 2-hop instances ($15$ Planetary, $15$ Elemental)
  - $30$ 3-hop instances ($15$ Planetary, $15$ Elemental)
- **Symmetry Controls:**
  - Premise reversal: Exactly $50\%$ canonical (`outranks`) and $50\%$ reversed (`is lower than`).
  - Foil positioning: Exactly $50\%$ target-first (`A or C`) and $50\%$ target-second (`C or A`).
  - Option balancing: Both target and foil are verified single-token entities in the Pythia vocabulary.

### 3.2 Pre-Registered Headroom Criterion
- The benchmark baseline accuracy must fall strictly within the pre-registered **40%–70%** window to ensure sufficient error instances ($18 \le \text{errors} \le 36$) for measuring rescue capacity.
- **Empirical Baseline Pre-Screening (Blind to Interventions):**
  $$\text{Unintervened Baseline Accuracy} = 34 / 60 = \mathbf{56.67\%}$$
  Available errors for causal rescue: $\mathbf{26 \text{ instances}}$ ($43.33\%$).
- The headroom criterion is **fully met**; no ceiling effect exists.

---

## 4. Fixed Intervention and Configuration Inherited from EXP065

To preserve strict replication validity, no hyperparameter search or mechanism retuning is permitted.

### 4.1 Target Layer Selection
- In EXP065 (`pythia-160m`, 12 layers), interventions were targeted at Layer 10 (relative depth $10/12 \approx 83.33\%$).
- In EXP066 (`pythia-410m`, 24 layers), interventions are targeted at proportional depth:
  $$\text{Target Layer} = \text{round}\left(24 \times \frac{10}{12}\right) = \mathbf{\text{Layer } 20} \quad (\text{Index } 20 \text{ in } 0\dots 23)$$
- Module: `model.gpt_neox.layers[20]`
- Intervention Site: Layer output residual stream before input to Layer 21.

### 4.2 Support Basis Construction ($B_{\text{agg}} \in \mathbb{R}^{1024}$)
- Evaluated across $K=5$ disjoint support vocabularies:
  - $\mathcal{V}_1$ (Anglo): `Alice`, `Bob`, `Charlie`, `David`, `Emma`
  - $\mathcal{V}_2$ (Biblical): `Aaron`, `Caleb`, `Gideon`, `Miriam`, `Reuben`
  - $\mathcal{V}_3$ (Greek): `Hector`, `Jason`, `Nestor`, `Paris`, `Priam`
  - $\mathcal{V}_4$ (Roman): `Marcus`, `Lucius`, `Titus`, `Felix`, `Silas`
  - $\mathcal{V}_5$ (Modern): `Liam`, `Noah`, `Sora`, `Maya`, `Leila`
- Per-vocabulary contrast direction at Layer 20:
  $$\Delta h(x) = h_{20}(x^{\text{rel}}) - h_{20}(x^{\text{neutral}})$$
  $$\hat{v}_k = \frac{\frac{1}{M}\sum_{i=1}^M \frac{\Delta h_i}{\|\Delta h_i\|_2}}{\left\|\frac{1}{M}\sum_{i=1}^M \frac{\Delta h_i}{\|\Delta h_i\|_2}\right\|_2}$$
- Aggregated basis:
  $$B_{\text{agg}} = \frac{\sum_{k=1}^K \hat{v}_k}{\left\|\sum_{k=1}^K \hat{v}_k\right\|_2} \in \mathbb{R}^{1024}$$

### 4.3 Dynamic Role-Procrustes Operator $R(x) \in O(1024)$
- Reference support frames (Canonical Anglo entities: Alice, Charlie, David):
  $$E_0^{(2\text{-hop})} = \left[ w(\text{" Alice"}), w(\text{" Charlie"}) \right]^T \in \mathbb{R}^{2 \times 1024}$$
  $$E_0^{(3\text{-hop})} = \left[ w(\text{" Alice"}), w(\text{" David"}) \right]^T \in \mathbb{R}^{2 \times 1024}$$
- Target instance premise role embeddings:
  $$E(x) = \left[ w(e_{\text{head}}(x)), w(e_{\text{tail}}(x)) \right]^T \in \mathbb{R}^{2 \times 1024}$$
- SVD factorization:
  $$E(x)^T E_0 = U \Sigma V^T \implies R(x) = U V^T \in O(1024)$$
- Dynamic basis vector:
  $$b_{\text{dynamic}}(x) = R(x) B_{\text{agg}}$$
- Fixed intervention strength:
  $$\alpha = 0.50 \quad \text{(locked)}$$
  $$h'_{20}(x) = h_{20}(x) + \alpha \cdot b_{\text{dynamic}}(x)$$

---

## 5. Same-Layer Output Bridge (Positive Control)

The causal-access benchmark is defined at Layer 20 identically to EXP065:
$$v_{\text{output}}^{(20)}(x) = \frac{w(e_{\text{target}}) - w(e_{\text{foil}})}{\|w(e_{\text{target}}) - w(e_{\text{foil}})\|_2} \in \mathbb{R}^{1024}$$
$$h'_{20}(x) = h_{20}(x) + \alpha \cdot v_{\text{output}}^{(20)}(x)$$

**Purpose:** Confirms whether Layer 20 possesses linear readout causal access to the decision logits. If the output bridge achieves $\Delta M > 0$, any failure of $b_{\text{dynamic}}$ cannot be attributed to layer disconnectivity or logit masking.

---

## 6. Controls and Normalization

EXP066 tests 6 standardized conditions under identical hook geometry:

| Condition # | Condition Name | Mathematical Definition | Role |
| :---: | :--- | :--- | :--- |
| **0** | **Unintervened Baseline** | $h'_{20} = h_{20}$ | Benchmark baseline ($56.67\%$) |
| **1** | **Static Basis Baseline** | $h'_{20} = h_{20} + \alpha B_{\text{agg}}$ | Test static representation transfer |
| **2** | **Aligned Dynamic Basis** | $h'_{20} = h_{20} + \alpha R(x) B_{\text{agg}}$ | **Primary Confirmatory Condition** |
| **3** | **Output Bridge Control** | $h'_{20} = h_{20} + \alpha v_{\text{output}}^{(20)}$ | Positive control for Layer 20 causal access |
| **4** | **Random Rotation Control** | $h'_{20} = h_{20} + \alpha R_{\text{rand}} B_{\text{agg}}$ | Null distribution (5 orthogonal seeds: 7000, 7053, 7106, 7159, 7212) |
| **5** | **Dynamic $B_\perp$ Control** | $h'_{20} = h_{20} + \alpha R(x) B_\perp$ | Task subspace selectivity ($B_\perp \perp B_{\text{agg}}$, Seed 9876) |
| **6** | **Dynamic $B_{\text{wrong}}$ Control** | $h'_{20} = h_{20} + \alpha R(x) B_{\text{wrong}}$ | Semantic content specificity (factual capital-city contrast) |

---

## 7. No-Leakage Rules (Constitutional Compliance)

In strict adherence to Law 7 (Zero Data Leakage):
1. **Answer Blindness:** $E(x)$ is extracted exclusively from premise entity tokens ($e_{\text{head}}, e_{\text{tail}}$).
2. **Option Isolation:** The query string (`Question: Who is higher in rank, A or B?`), candidate options, and target answer are strictly barred from the computation of $R(x)$ and $b_{\text{dynamic}}(x)$.
3. **No Dynamic Optimization:** $R(x)$ is closed-form SVD on the input embeddings; no test-time gradients or loss calculations are performed.
4. **State Purification:** All PyTorch hooks are removed and PyTorch caches flushed between instances.

---

## 8. Primary Endpoint

The central pre-registered confirmatory test:
$$\boxed{\Delta M_{\text{dynamic internal}} = \frac{b - c}{N} = \frac{\text{Rescues} - \text{Corruptions}}{60} \stackrel{?}{>} 0}$$
where:
- $b$: Number of instances where baseline was incorrect ($y_{\text{base}} = 0$) and intervened model was correct ($y_{\text{mod}} = 1$).
- $c$: Number of instances where baseline was correct ($y_{\text{base}} = 1$) and intervened model was incorrect ($y_{\text{mod}} = 0$).

---

## 9. Secondary Mechanistic Endpoints

1. **Logit Margin Shift:**
   $$\Delta \text{Margin} = \frac{1}{N}\sum_{i=1}^N \left[ (z_i^{\text{target}} - z_i^{\text{foil}})_{\text{intervened}} - (z_i^{\text{target}} - z_i^{\text{foil}})_{\text{baseline}} \right]$$
2. **Hidden State Displacement:**
   $$\Delta H = \frac{1}{N}\sum_{i=1}^N \|h'_{20}(x_i) - h_{20}(x_i)\|_2$$
3. **Distributional Divergence:**
   $$\text{KL}(p_{\text{base}} \,\|\, p_{\text{mod}})$$
4. **Vocabulary Stability:** Top-10 output token overlap percentage.

---

## 10. Exact Statistical Tests and Thresholds

1. **McNemar / Exact Binomial Test:**
   - Evaluated on discordant pairs $(b, c)$ with null parameter $\pi = 0.50$ via two-sided exact binomial test.
   - Significance threshold: $p < 0.05$.
2. **Wilcoxon Signed-Rank Test:**
   - Continuous test on paired margin deltas $\Delta \text{Margin}_i$.
   - Significance threshold: $p < 0.05$.
3. **Specificity Contrast:**
   - $\Delta M(b_{\text{dynamic}}) > \Delta M(R_{\text{rand}} B_{\text{agg}})$ ($p < 0.05$).

---

## 11. Replication and Falsification Criteria

### Outcome A — Direct Replication of Boundary (Expected)
- **Conditions:**
  $$\Delta M(\text{Aligned Dynamic Basis}) \approx 0 \quad (p \ge 0.05)$$
  $$\Delta M(\text{Same-Layer Output Bridge}) > 0 \quad (p < 0.05)$$
- **Scientific Interpretation:**
  $$\boxed{\textbf{The representational–causal dissociation replicates across Pythia scale (160M } \to \textbf{ 410M).}}$$
  Confirms that the inability of Procrustes coordinate alignment to induce causal steering is not an under-capacity artifact of 160M, but an inherent geometric-causal dissociation in transformer representations.

### Outcome B — Scale-Dependent Emergence of Causal Transfer (Divergence)
- **Conditions:**
  $$\Delta M(\text{Aligned Dynamic Basis}) > 0 \quad (p < 0.05)$$
  $$\Delta M(\text{Aligned Dynamic Basis}) > \Delta M(R_{\text{rand}} B_{\text{agg}}) \quad (p < 0.05)$$
- **Scientific Interpretation:**
  $$\boxed{\textbf{Scale-dependent emergence of causal interchangeability.}}$$
  Causal interchangeability is absent at 160M scale but emerges at 410M scale under identical mathematical operators.

---

## 12. Decision Tree for EXP067

```text
                               EXP066 Execution
                                      │
               ┌──────────────────────┴──────────────────────┐
               ▼                                             ▼
        [OUTCOME A: REPLICATION]                      [OUTCOME B: EMERGENCE]
      ΔM(dynamic) ≈ 0, Bridge > 0                   ΔM(dynamic) > 0, p < 0.05
               │                                             │
               ▼                                             ▼
  Representational-Causal Dissociation        Scale-Dependent Emergence Confirmed:
     Replicated Across Scale (160M & 410M)        Investigate Minimum Critical
               │                                   Scale & Head Attractor Dynamics
               ▼                                             │
  FREEZE EXPERIMENTAL ARC FOR PAPER                          ▼
  Proceed to Manuscript Package:              EXP067: Pythia-70M vs 1.4B Boundary
  "Representational Alignment is Not                  Cross-Scale Sweep
   Sufficient for Causal Transfer"
```

---

## 13. Artifact and Reproducibility Requirements

1. **Dedicated Run Directory:** `experiments/runs/EXP066_pythia410m_replication/`
2. **Execution Script:** `experiments/scripts/run_exp066_pythia410m_replication.py`
3. **Artifact Files Required:**
   - `exp066_run_log.txt`: Complete stdout log with timestamps and hash assertions.
   - `exp066_replication_results.json`: Full quantitative ledger including per-condition accuracy, margin shifts, McNemar $p$-values, KL divergences, and top-10 overlaps.
   - `exp066_instance_evaluations.json`: Instance-by-instance log ($N=60$) across all 6 conditions.
4. **Model Parameter Immutability Assertion:**
   - Pre-run SHA-256 == Post-run SHA-256 == `4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd`.
