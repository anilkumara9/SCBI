# EXP027: Cross-Architecture Failure Decomposition Protocol Specification

**Status:** Pre-Registered Experimental Specification  
**Governing Laws:** [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) Laws 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14  
**Target Architectures:** `EleutherAI/pythia-160m` (160M, 12 layers, $d_{\mathrm{model}}=768$, RoPE + parallel Attention/MLP) vs. `gpt2` (124M, 12 layers, $d_{\mathrm{model}}=768$, sequential Attention/MLP)  
**Evaluation Benchmark:** `BENCH-002-NL` Confirmatory Set ($N=100$, Seed 84)  
**Execution Script:** `experiments/scripts/run_exp027_failure_decomposition.py`  
**Output Location:** `experiments/runs/EXP027_decomposition/exp027_decomposition_results.json`  

---

## 1. Scientific Context & Motivation

In EXP026, the frozen SCBI pipeline ($G4_{\text{sparse}}, E_{CF}, O5, r=2, \alpha=0.25, \lambda=0.667$) exhibited divergent cross-architecture behaviors:
1. **Intra-Family Scale Transfer (GPT-2 Medium):** Baseline competence was high ($M_I = 0.7800$); SCBI captured 100% of available Oracle headroom ($\eta_{\mathrm{HR}} = 100\%$) with positive target-token probability boost ($\Delta \log p = +0.0696, CI > 0$), but Top-1 confirmation was inconclusive ($p=0.5000$) due to ceiling compression.
2. **Cross-Family Architecture Transfer (Pythia-160M):** Oracle headroom was identically zero ($M_{\mathrm{Oracle}} = M_I = 0.5900$), and autonomous SCBI yielded $\Delta M = -0.0200$.

### The Critical Methodological Mandate:
As established by scientific review:
$$\text{Pythia failure} \neq \text{proof that RoPE caused failure}$$
Pythia differs from GPT-2 simultaneously across:
- Rotary Position Embeddings (RoPE) vs. absolute learned position embeddings,
- GPT-NeoX parallel Attention/MLP execution vs. sequential execution,
- Tokenizer vocabulary and byte-level segmentation,
- Normalization placements and weight parameterization,
- Functional depth: $\lambda = 8/12$ may not map to the same semantic representation stage.

Furthermore, RoPE acts on attention query/key coordinates ($q_t, k_t$), whereas SCBI intervenes in the **residual stream** ($h_t$). Residual representations are not identical to the RoPE-rotated coordinate frame.

**Objective of EXP027:** Execute a diagnostic decomposition across the pipeline:
$$\mathcal{G} \longrightarrow E_{CF} \longrightarrow O5$$
and test the functional depth profile to causally localize the exact failure point without ad-hoc operator tuning.

---

## 2. Inviolable Governance & Protocol Locks

1. `[LAW 6]` **Frozen Parameter Invariant ($\Delta\theta \equiv 0$):** Pre/post execution SHA-256 parameter hashes must match identically. No weights, biases, or normalization buffers may be updated.
2. `[LAW 7]` **Zero Data Leakage:** Target labels $y_{\mathrm{correct}}$ must never be exposed to candidate generation $\mathcal{G}$ or unsupervised evaluator $E_{CF}$.
3. `[LAW 10 & 14]` **Anti-Optimization Mandate:** No ad-hoc RoPE-aware operator or hyperparameter searching may be introduced to "fix" Pythia. The protocol is strictly diagnostic.
4. `[LAW 13]` **Deterministic Reproducibility:** Fixed seeds, pinned tokenizers, explicit device precision (`float32`), and instance-level logging.

---

## 3. Five Diagnostic Modules

### Module A: Candidate Quality Spread Audit ($\mathcal{G}$)
Evaluates whether SVD on prompt token representations produces any viable candidate directions in Pythia:
$$\Delta_{\mathrm{spread}} = M_{\mathrm{Oracle}} - M_{\mathrm{Random}}$$
- Compute accuracy for each individual candidate $k \in \{0, 1, 2, 3\}$.
- Compute mean target log-probability change $\Delta \log p_k(y_{\mathrm{correct}})$ for each candidate.
- **Diagnostic Criterion:** If $\Delta_{\mathrm{spread}} \approx 0$, candidate generation $\mathcal{G}$ fails to isolate constructive directions in Pythia's residual space. If $\Delta_{\mathrm{spread}} > 0$, viable candidates exist but downstream components fail to exploit them.

### Module B: Contrastive Evidence Separability Audit
Audits whether the contrastive evidence metric $d_t$ cleanly segments distractor tokens from premise/query tokens in Pythia's residual stream.
For prompt token representations $h_t \in \mathbb{R}^d$:
$$e_t^- = \|V_-^\top h_t\|_2, \qquad e_t^+ = \|V_+^\top h_t\|_2, \qquad d_t = e_t^- - e_t^+$$
Segment the prompt into three non-overlapping token regions:
1. Premise tokens: $\mathcal{T}_{\mathrm{premise}}$
2. Distractor tokens: $\mathcal{T}_{\mathrm{distractor}}$
3. Question tokens: $\mathcal{T}_{\mathrm{question}}$

Metrics:
- Mean $d_t$ in each region: $\bar{d}_{\mathrm{prem}}, \bar{d}_{\mathrm{dist}}, \bar{d}_{\mathrm{quest}}$.
- Gating activation frequency:
  $$P(g_t = 1 \mid t \in \mathcal{T}_{\mathrm{distractor}}), \qquad P(g_t = 1 \mid t \in \mathcal{T}_{\mathrm{premise}})$$
- Contrastive Selectivity Index:
  $$\mathrm{SI} = P(g_t = 1 \mid \mathcal{T}_{\mathrm{distractor}}) - P(g_t = 1 \mid \mathcal{T}_{\mathrm{premise}})$$
- **Diagnostic Criterion:** In GPT-2, $\mathrm{SI} > 0.85$ (cleanly gating distractor tokens while sparing premise). If Pythia shows $\mathrm{SI} \approx 0$ or $d_t \le 0$ globally, residual-space contrastive separability has failed.

### Module C: Operator Displacement & Representation Impact ($O5$)
Audits whether realized operator displacement at the target layer preserves or disrupts downstream representations:
- Realized Frobenius displacement:
  $$\mathrm{Disp} = \frac{\|\Delta H\|_F}{\|H\|_F}$$
- Output logit KL divergence: $\mathrm{KL}(p_{\mathrm{Identity}} \,\|\, p_{O5})$.
- Output Top-10 logit overlap: $\mathrm{Overlap}_{10}(p_{\mathrm{Identity}}, p_{O5})$.
- Margin impact: $\Delta \mathrm{Margin} = \Delta [p(y_{\mathrm{correct}}) - p(y_{\mathrm{distractor}})]$.
- **Diagnostic Criterion:** Determines whether the operator is under-displacing (inert) or over-displacing (catastrophic representational disruption).

### Module D: Evaluator Calibration ($E_{CF}$)
Audits whether the unsupervised counterfactual score $e_{\mathrm{cf}}(k) = d_{\mathrm{pos}}(k) - 0.5 \cdot d_{\mathrm{neg}}(k)$ accurately ranks candidate quality without labels:
- True utility: continuous target log-prob change $\Delta \log p_k(y_{\mathrm{correct}})$.
- Spearman rank correlation $\rho(E_{CF}, \Delta \log p)$ and Kendall $\tau$.
- Selection Regret: $M_{\mathrm{Oracle}} - M_{E_{CF}}$.
- **Diagnostic Criterion:** In GPT-2, $\rho \approx +0.4920$. If Pythia's $\rho \le 0$ despite viable candidates existing ($\Delta_{\mathrm{spread}} > 0$), the failure is causally attributed to evaluator geometry mismatch.

### Module E: Functional Depth Sensitivity Profile
Tests whether the failure at Layer 8 was caused by the normalized-depth heuristic $\lambda = 8/12 \approx 0.667$ failing to align with functional semantic processing stages across different architectures:
- Evaluate Pythia-160m across layers:
  $$l \in \{2, 4, 6, 8, 10, 11\}$$
- For each layer $l$, measure:
  - Baseline $M_I(l)$
  - Oracle accuracy $M_{\mathrm{Oracle}}(l)$
  - Headroom $\Delta M_{\mathrm{Oracle}}(l) = M_{\mathrm{Oracle}}(l) - M_I(l)$
  - Contrastive Selectivity Index $\mathrm{SI}(l)$
  - Realized displacement $\mathrm{Disp}(l)$ and output KL divergence $\mathrm{KL}(l)$.
- **Diagnostic Criterion:** If $\Delta M_{\mathrm{Oracle}} > 0$ at an alternative depth, the failure is localized to cross-architecture depth alignment.

---

## 4. Pre-Registered Causal Attribution Matrix

| Diagnostic Observation | Scientific Causal Attribution |
| :--- | :--- |
| Candidate spread collapses across all tested configurations ($\Delta_{\mathrm{spread}} \approx 0$) | **Generator Failure ($\mathcal{G}$):** SVD on token hidden slices does not isolate separable distractor subspaces in Pythia. |
| Contrastive separability collapses ($\mathrm{SI} \approx 0$) | **Evidence Metric Failure ($d_t$):** Residual stream does not exhibit differential projection energy between target and distractor subspaces. |
| Candidate spread exists ($\Delta_{\mathrm{spread}} > 0$), but evaluator correlation collapses ($\rho \le 0$) | **Evaluator Failure ($E_{CF}$):** Contrastive pseudo-prompts do not produce valid proxy signals in Pythia. |
| Operator produces extreme KL or destroys top-10 overlap ($\mathrm{Overlap} < 0.50$) | **Operator Distortion ($O5$):** Linear projection destroys residual stream invariants under parallel block execution. |
| Operator succeeds at another depth ($l \neq 8$), but fails at $\lambda = 0.667$ | **Functional Depth Mismatch:** Normalized depth rule $\lambda = l/L$ does not map to equivalent semantic abstraction stages across models. |
| Residual intervention fails across all depths, but attention query/key intervention succeeds | **RoPE / Attention Coordinate Constraint:** Coordinate frame is localized to attention mechanisms and not accessible via residual stream linear projections. |

---

## 5. Artifacts & Reproducibility Requirements

- All outputs written to `experiments/runs/EXP027_decomposition/exp027_decomposition_results.json`.
- Complete timing and parameter hashes recorded.
- Findings incorporated into `reports/experiment_report.md` Section 23 and `reports/research_log.md` LOG-030.
