# EXP046: Prospective Failure Mode Diagnosis & Adaptive Computation Allocation Protocol Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP046`
- **Date:** 2026-09-12
- **Lead Roles:**
  - **Research Theorist / Scientific Strategist / Skeptical Reviewer:** Formulates hypotheses, derives mathematical questions, challenges conclusions, sets falsification thresholds.
  - **Experimental Scientist / Research Engineer (Antigravity):** Implements pre-registered protocols, writes modular verified code, runs experiments, analyzes raw outputs with statistical sobriety, guarantees $\Delta\theta \equiv 0$, identifies implementation phenomena.
- **Governing Standard:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (specifically Law 2: Never Invent Results, Law 4: Never Silently Shift Hypotheses, Law 6: Frozen Backbone $\Delta\theta \equiv 0$, Law 7: Zero Data Leakage, Law 9: No Cherry-Picking, Law 10: Never Claim Premature Novelty, Law 13: Deterministic Reproducibility, Law 14: Challenge Rather Than Defend).
- **Codification Anchor:** [`theory/README.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/theory/README.md) §104–§105.
- **Core Scientific Question:**
  $$\boxed{\textbf{Can a frozen model predict whether internal representation reorganization is likely to be useful before selecting a computational action?}}$$

---

## 2. Methodological Safeguards: Rigorous Resolution of the Five Reviewer Critiques

### Safeguard 1: Explicit Technical Specification of the Retrieval Action ($\mathcal{S}$)
The external retrieval action is formally specified prior to execution to prevent ambiguity:
- **Retrieval Mechanism ($\mathcal{S}$):** Fixed BM25 lexical retriever operating over a pre-indexed corpus $\mathcal{K}$.
- **Corpus $\mathcal{K}$:** A knowledge base of $K=500$ factual reference passages spanning all relational domains in `BENCH-002` and `BENCH-004`, plus $400$ distractors and encyclopedic trivia passages.
- **Passage Budget:** Top-$k = 1$ retrieved passage.
- **Context Injection Policy:** The retrieved passage is prefixed to the prompt context:
  $$\tilde{x} = \text{"[Reference: "} + \mathcal{S}(x) + \text{"]\n"} + x$$
- **Evaluation Pass:** Exactly 1 forward pass through the frozen model over the augmented prompt $\tilde{x}$.
- **Compute Cost Accounting:** $C(\mathcal{S}) = 2.00$ normalized compute units (1.0 index query FLOP equivalent + 1.0 longer-context forward pass).

### Safeguard 2: Complete Temporal & Epistemic Separation of Dataset Splits
To guarantee that the diagnostic classifier $D_\phi$ cannot overfit or access held-out test data:
$$\boxed{\mathcal{D}_{\mathrm{calib}} \ (N=30) \longrightarrow \text{Fit & Freeze } D_\phi \longrightarrow \mathcal{D}_{\mathrm{test}} \ (N=100)}$$
1. **$\mathcal{D}_{\mathrm{calib}}$ ($N=30$, Seed 123 for `BENCH-002`, Seed 250 for `BENCH-004`):**
   Used exclusively to compute label-free pre-intervention observables $\mathcal{O}_M(x)$ and fit the diagnostic scoring model $\hat{p}(\text{useful} \mid \mathcal{O}_M(x))$.
   - **FREEZE LOCK:** The parameters $\phi$ and decision thresholds of $D_\phi$ are hashed and cryptographically locked before $\mathcal{D}_{\mathrm{test}}$ is loaded.
2. **$\mathcal{D}_{\mathrm{test}}$ ($N=100$, Seed 84 for `BENCH-002`, Seed 350 for `BENCH-004`):**
   Held-out confirmatory benchmark. Never observed by $D_\phi$ during calibration.

### Safeguard 3: Pre-Registered, Numerically Fixed Utility Equation
The net utility function is locked prior to running test instances:
$$\boxed{U(a \mid x) = \operatorname{Correct}(a \mid x) - \lambda \cdot C(a) - \gamma \cdot \mathbf{1}[\text{Corrupted}(a \mid x)]}$$
where:
- $\operatorname{Correct}(a \mid x) \in \{0, 1\}$: Discrete task correctness indicator.
- $\mathbf{1}[\text{Corrupted}(a \mid x)] \in \{0, 1\}$: $1$ if baseline unsteered model was correct on $x$ and action $a$ induces an incorrect prediction ($c=1$), else $0$.
- **Normalized Compute Costs:**
  - $C(\emptyset) = 1.00$ (Direct unsteered baseline pass).
  - $C(\mathcal{R}) = 1.05$ (1 forward pass + lightweight linear projection at Layer 8).
  - $C(\mathcal{S}) = 2.00$ (BM25 retrieval + augmented context forward pass).
- **Locked Lagrange Multipliers:**
  - $\lambda = 0.05$ (Compute penalty: retrieval must produce $>+5\%$ accuracy gain to break even on compute).
  - $\gamma = 1.00$ (Corruption penalty: any corruption zeroes the reward).
- **Net Relative Utility over Baseline:**
  $$\Delta U(a \mid x) = U(a \mid x) - U(\emptyset \mid x)$$

### Safeguard 4: Operational Definition of Computational Regimes
Regimes are defined strictly by operational utility under the tested action set, not ontological assumptions about "world knowledge":
- **Regime A ($\mathcal{R}$-Viable / Representation Conflict):** Instances where internal representation reorganization provides positive net utility ($U_{\mathcal{R}} > U_{\emptyset}$ and $c=0$).
- **Regime B ($\mathcal{S}$-Viable / External Retrieval Needed):** Instances where internal representation reorganization fails ($U_{\mathcal{R}} \le U_{\emptyset}$), but external retrieval provides positive net utility ($U_{\mathcal{S}} > U_{\emptyset}$).
- **Regime C ($\emptyset$-Optimal / Action Unavailable / Ambiguous):** Instances where neither internal reorganization nor retrieval provides positive net utility over baseline ($\max(U_{\mathcal{R}}, U_{\mathcal{S}}) \le U_{\emptyset}$). Action $\emptyset$ (abstention) is the optimal decision.

The retrospective Oracle action is defined as:
$$a^*(x) = \arg\max_{a \in \{\mathcal{R}, \mathcal{S}, \emptyset\}} U(a \mid x)$$

### Safeguard 5: Feature Ablation Hierarchy
The diagnostic system is evaluated under a strict ablation hierarchy:
1. **Full Diagnostic ($D_{\mathrm{full}}$):** All features ($\Delta z_{\mathrm{top2}}, H_{\mathrm{vocab}}, \sigma_H(A_8), \mathrm{PR}_{\min}, d_{\mathrm{drift}}$).
2. **Output-Only ($D_{\mathrm{output}}$):** Logit gap $\Delta z_{\mathrm{top2}}$ and vocabulary predictive entropy $H_{\mathrm{vocab}}$.
3. **Geometry-Only ($D_{\mathrm{geom}}$):** Participation ratio $\mathrm{PR}_{\min}$ and residual directional drift $d_{\mathrm{drift}}$.
4. **Attention-Only ($D_{\mathrm{attn}}$):** Attention head entropy dispersion $\sigma_H(A_8)$.

---

## 3. Evaluated Policies on Held-Out Mixed Benchmark ($N_{\mathrm{test}} = 100$)

1. **$\pi_{\mathrm{always}\text{-}\emptyset}$:** Always executes direct unsteered forward pass ($B_{\mathrm{eval}} = 1.00$).
2. **$\pi_{\mathrm{always}\text{-}\mathcal{R}}$:** Always executes internal representation reorganization.
3. **$\pi_{\mathrm{always}\text{-}\mathcal{S}}$:** Always executes external retrieval.
4. **$\pi_{\mathrm{diagnostic}}$:** Evaluates pre-intervention observables $\mathcal{O}_M(x)$ using frozen $D_\phi$ and selects:
   $$a^* = \arg\max_{a \in \{\mathcal{R}, \mathcal{S}, \emptyset\}} \hat{U}(a \mid x)$$
5. **$\pi_{\mathrm{oracle}}$:** Retrospective instance-optimal allocation using measured outcomes.

---

## 4. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Superiority of Diagnostic Allocation ($H_{\mathrm{utility}}$)
$$\bar{U}(\pi_{\mathrm{diagnostic}}) > \max\big(\bar{U}(\pi_{\mathrm{always}\text{-}\mathcal{R}}), \bar{U}(\pi_{\mathrm{always}\text{-}\mathcal{S}}), \bar{U}(\pi_{\mathrm{always}\text{-}\emptyset})\big)$$
- **Prediction:** The diagnostic policy achieves higher net expected utility than any static blind policy by selectively assigning $\mathcal{R}$ to representation-conflict instances, $\mathcal{S}$ to retrieval-viable instances, and $\emptyset$ to ambiguous instances, avoiding corruptions ($c=0$).
- **Falsification Criterion:** If $\bar{U}(\pi_{\mathrm{diagnostic}}) \le \max(\bar{U}_{\mathrm{blind}})$, the hypothesis that prospective failure mode diagnosis improves computational utility is **falsified**.

### Hypothesis 2: Discrimination of $\mathcal{R}$-Viability ($H_{\mathrm{ROC}}$)
- **Prediction:** Pre-intervention observables predict whether an instance has $U_{\mathcal{R}} > U_{\emptyset}$ with $\mathrm{ROC}\text{-}\mathrm{AUC} \ge 0.75$ on the held-out test split ($N=100$).
- **Falsification Criterion:** If $\mathrm{ROC}\text{-}\mathrm{AUC} < 0.65$, prospective diagnostic discrimination from unsteered internal observables is judged unviable.

---

## 5. Execution Protocol & Invariance Audit

1. **Step 1: Calibration & Frozen Diagnostic Fitting on $\mathcal{D}_{\mathrm{calib}}$ ($N=30$, Seed 123/250):**
   - Extract label-free observables $\mathcal{O}_M(x)$ on $15$ `BENCH-002` and $15$ `BENCH-004` calibration instances.
   - Fit logistic scoring function $\hat{p}(\mathcal{R} \mid \mathcal{O}_M(x))$ without test label access.
   - Freeze decision rule:
     - Predict $\mathcal{R}$ if $\hat{p}(\mathcal{R} \mid \mathcal{O}_M(x)) \ge 0.60$.
     - Predict $\mathcal{S}$ if $\hat{p}(\mathcal{R} \mid \mathcal{O}_M(x)) \le 0.30$ and $H_{\mathrm{vocab}} > 2.5$.
     - Predict $\emptyset$ otherwise.
   - **FREEZE DIAGNOSTIC MODEL:** Record SHA-256 hash of weights and threshold rules.
2. **Step 2: Held-Out Confirmatory Evaluation on $\mathcal{D}_{\mathrm{test}}$ ($N=100$, Seed 84/350):**
   - Verify model parameter hash: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).
   - Run all four policies across all 100 instances.
   - Compute counterfactual action matrix: $U(\mathcal{R}), U(\mathcal{S}), U(\emptyset)$ for every instance.
   - Verify post-experiment parameter SHA-256 hash identical ($\Delta\theta \equiv 0$).
   - Compute exact net utility, costs, corruptions, and ROC-AUC under the feature ablation hierarchy.
