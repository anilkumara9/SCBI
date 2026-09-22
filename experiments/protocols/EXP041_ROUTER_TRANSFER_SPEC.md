# EXP041: Cross-Task & Cross-Architecture Router Transfer Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP041`
- **Date:** 2026-09-12
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (specifically Law 4: Never Silently Shift Hypotheses, Law 6: Frozen Backbone, Law 7: Zero Data Leakage, Law 9: No Cherry-Picking, Law 10: Never Claim Premature Novelty, Law 13: Deterministic Reproducibility, Law 14: Challenge Rather Than Defend).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark testing whether the prospective router parameters $\phi^*$—calibrated strictly on Pythia-160M on `BENCH-002-NL` (Seed 123) in EXP040—can transfer **without any retraining or adaptation** ($\Delta\phi \equiv 0$) to:
  1. **Cross-Task / Cross-Domain Transfer:** An unseen 5-domain benchmark (`BENCH-004-TRANSFER`, $N=50$) with novel entity types, relational predicates, and vocabulary tokens.
  2. **Cross-Architecture Transfer:** A structurally distinct transformer backbone (`gpt2`, 124M, $L=12, d=768$, Post-LN architecture vs. Pythia's Parallel Rotary architecture).
- **Core Scientific Question:**
  $$\boxed{\textbf{Does state-to-generator routing capture a transferable computational principle, or is it an in-distribution artifact?}}$$

---

## 2. Theoretical Motivation: The Threshold of Generalization

EXP040 proved that pre-intervention internal state observables $\mathbf{s}(h_0) \in \mathbb{R}^6$ allow a prospective router to recover $80\%$ of the Oracle multi-generator headroom within the training distribution without label leakage.

However, within-distribution transfer cannot distinguish between two fundamentally different scientific realities:
1. **Narrow Hypothesis:** The router has learned specific idiosyncratic geometric correlations of the `BENCH-002-NL` prompt templates on Pythia-160M.
2. **Transferable Principle Hypothesis:** The router has learned a domain-invariant relationship between pre-intervention computation diagnostics (velocity, attention entropy, clause contrast) and the required representation mode (trajectory correction $G_1$, contextual reinterpretation $G_2$, attention rerouting $G_3$).

EXP041 establishes the definitive empirical test: **the router $\phi^*$ is locked, frozen, and evaluated zero-shot.**

---

## 3. Evaluated Transfer Dimensions

```text
                               EXP040 FROZEN ROUTER φ*
                       (Trained on Pythia-160M, BENCH-002-NL)
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        PART 1: CROSS-TASK TRANSFER            PART 2: CROSS-ARCHITECTURE
             (Pythia-160M)                               (GPT-2 124M)
                   │                                           │
         BENCH-004-TRANSFER (N=50)                   BENCH-002-NL (N=50)
         - Corporate Ownership                       - Different Attention & LN
         - Imperial Capitols                         - Different Parameter Space
         - Biochemical Enzymes                       - Completely Unseen Weights
         - Material Craft
         - Athletic Awards
```

---

## 4. Benchmark Protocols & Conditions

### Part 1: Cross-Task Transfer on Pythia-160M (`BENCH-004-TRANSFER`, $N=50$, Seed 350)
1. **Condition 1.1 (Baseline $M_I$):** Unintervened single-pass baseline on transfer domains.
2. **Condition 1.2 ($G_{\mathrm{contrastive}}$):** Supervised reference baseline.
3. **Condition 1.3 (Static $G_1$):** Trajectory flow correction.
4. **Condition 1.4 (Static $G_2$):** Contextual perturbation.
5. **Condition 1.5 (Static $G_3$):** Attention relational routing.
6. **Condition 1.6 (Oracle Bound):** Hindsight best of $\{G_1, G_2, G_3\}$ on transfer tasks.
7. **Condition 1.7 (Frozen Router $\pi_{\phi^*}$):** Zero-shot application of EXP040 router $\phi^*$ without retraining.

### Part 2: Cross-Architecture Transfer on GPT-2 124M (`BENCH-002-NL`, $N=50$, Seed 84)
1. **Condition 2.1 (Baseline $M_I$):** Unintervened single pass on GPT-2.
2. **Condition 2.2 ($G_{\mathrm{contrastive}}$):** Supervised reference on GPT-2.
3. **Condition 2.3 (Static $G_1$):** Trajectory flow on GPT-2.
4. **Condition 2.4 (Static $G_2$):** Contextual perturbation on GPT-2.
5. **Condition 2.5 (Static $G_3$):** Attention relational routing on GPT-2.
6. **Condition 2.6 (Oracle Bound):** Hindsight best of $\{G_1, G_2, G_3\}$ on GPT-2.
7. **Condition 2.7 (Frozen Router $\pi_{\phi^*}$):** Zero-shot application of EXP040 router $\phi^*$ directly to GPT-2 pre-intervention features $\mathbf{s}(h_0)$.

---

## 5. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Cross-Task Invariance ($H_{\mathrm{cross\_task}}$)
$$M(\pi_{\phi^*} \mid \text{BENCH-004}) > M_I(\text{BENCH-004}) \quad \text{and} \quad c \le 1$$
- **Prediction:** The frozen router achieves positive headroom ($\Delta M \ge +4.0$ pp, $c \le 1$) across unseen semantic domains without parameter adaptation.
- **Falsification Criterion:** If $\Delta M \le 0$ or regressions occur ($c \ge 3$), the hypothesis that the routing policy generalizes across semantic tasks is rejected.

### Hypothesis 2: Cross-Architecture Invariance ($H_{\mathrm{cross\_arch}}$)
$$M(\pi_{\phi^*} \mid \text{GPT-2}) > M_I(\text{GPT-2}) \quad \text{and} \quad c \le 1$$
- **Prediction:** The standardized feature vector $\mathbf{s}(h_0)$ allows the router to select effective computational modes on GPT-2 without architecture-specific retraining.
- **Falsification Criterion:** If the router produces zero or negative headroom on GPT-2, architecture-invariance of representation diagnostics is falsified.

---

## 6. Reproducibility & Integrity Standards
- Parameter hashes verified invariant for Pythia-160M and GPT-2 pre- and post-run ($\Delta\theta \equiv 0$).
- Exactly $1.00$ forward pass per instance ($B_{\mathrm{eval}} = 1.00$).
- Router parameters $\phi^*$ locked identically to EXP040 values.
- Complete output saved to `experiments/runs/EXP041_router_transfer/exp041_router_transfer_results.json`.
