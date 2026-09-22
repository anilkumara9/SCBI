# EXP044: Cross-Task Autonomous Operator Discovery & Synthesis Protocol Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP044`
- **Date:** 2026-09-12
- **Governing Standard:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (specifically Law 2: Never Invent Results, Law 4: Never Silently Shift Hypotheses, Law 6: Frozen Backbone $\Delta\theta \equiv 0$, Law 7: Zero Data Leakage, Law 9: No Cherry-Picking, Law 10: Never Claim Premature Novelty, Law 13: Deterministic Reproducibility, Law 14: Challenge Rather Than Defend).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark testing whether an automated operator discovery protocol can overcome the **Generator Existence Boundary** on cross-task transfer (`BENCH-004-TRANSFER`).
- **Core Scientific Question:**
  $$\boxed{\textbf{Can a model autonomously synthesize useful representation operators for unseen task domains, breaking the generator existence ceiling?}}$$

---

## 2. Theoretical Motivation: The Decoupled Inference Triad

EXP041 through EXP043 established that inference-time representation control decomposes into three distinct requirements:
$$\boxed{
\text{Existence}
\longrightarrow
\text{Applicability}
\longrightarrow
\text{Selection}
}$$

1. **Existence:** $\mathcal{G}_M$ must contain an operator that spans task contrast.
   - On `BENCH-004-TRANSFER`, the original static operator library had $M_{\mathrm{Oracle}} = M_I = 52.0\%$ (zero headroom, $b=0, c=0$).
   - When no viable operator exists in $\mathcal{G}_M$, neither routing nor applicability filtering can rescue instances.
2. **Applicability:** An operator must be computationally safe for the model's downstream dynamics $\mathcal{D}_M$.
   - Solved in EXP043: Causal response audits autonomously prune destabilizing operators ($G_1$ on GPT-2, $G_3$ on Pythia), eliminating corruptions ($c=0$).
3. **Selection:** The runtime controller must select the appropriate operator for the current input state $h_0$.
   - Solved in EXP040/EXP043: Prospective routing recovers $80\%$ of Oracle headroom under an exact 1-pass budget ($B_{\mathrm{eval}} = 1.00$).

**The Frontier in EXP044:** Can the discovery pipeline synthesize candidate operators conditioned on measured target task geometry $\mathcal{O}_{\mathrm{task}}$, audit them on unlabeled calibration prompts, and build a task-specific toolbox $\mathcal{G}^*_{\mathrm{task}}$ that creates positive Oracle headroom ($M_{\mathrm{Oracle}} > 52.0\%$) and delivers autonomous capability gains without labels?

---

## 3. The 4-Stage Task Discovery Architecture

```text
                        TARGET TASK DOMAIN (BENCH-004-TRANSFER)
                                       │
                                       ▼
               STAGE 1: UNLABELED PROBING & GEOMETRY PROFILING (N_calib = 15, Seed 250)
               - Measure inter-layer acceleration: ||(h_{l+2} - h_{l+1}) - (h_{l+1} - h_l)||
               - Profile layer-wise participation ratio PR(l)
               - Profile attention entropy & salience distribution
               - Measure punctuation/clause boundary subspace variance
                                       │
                                       ▼
               STAGE 2: TASK-CONDITIONED CANDIDATE SYNTHESIS
               Synthesize 5 candidate operator families:
               - G_accel: Inter-layer acceleration / curvature flow
               - G_salience: High-salience attention source divergence
               - G_clause: Sentence boundary subspace projection
               - G_ortho_flow: Orthogonalized inter-layer residual velocity
               - G_norm_ctx: Layer-normalized contextual perturbation
                                       │
                                       ▼
               STAGE 3: CAUSAL RESPONSE AUDIT (N_calib = 15, Seed 250)
               Evaluate each candidate operator without ground-truth labels:
               - Pruning rule: Remove G_i if c_audit > 0 or Δlog p_audit < 0
               - Retain audited toolbox: G*_task = {G_i | c_audit == 0 and Δlog p_audit > 0}
                                       │
                                       ▼
               STAGE 4: CONFIRMATORY EVALUATION (N_test = 50, Seed 350, B_eval = 1.00)
               Evaluate G*_task on held-out test split under exact 1.00 forward pass budget
```

---

## 4. Evaluated Backbone & Benchmark Configuration

- **Backbone Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision: `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark Suite:** `BENCH-004-TRANSFER` across 5 unseen relational domains:
  1. Corporate Ownership & Subsidiaries
  2. Historical Imperial Capitols & Seats of Rule
  3. Biochemical Enzymes & Specific Substrates
  4. Material Craft & Artisan Media
  5. Athletic Tournaments & Championship Awards
- **Calibration Split (Phase A):** $N_{\mathrm{calib}} = 15$ prompts (Seed 250, zero ground-truth labels exposed).
- **Confirmatory Split (Phase B):** $N_{\mathrm{test}} = 50$ benchmark instances (Seed 350).
- **Baseline Accuracy:** $M_I = 0.5200$ (26/50 correct).

---

## 5. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Autonomous Existence Recovery ($H_{\mathrm{exist}}$)
$$\text{On } \text{BENCH-004-TRANSFER}, \quad M_{\mathrm{Oracle}}(\mathcal{G}^*_{\mathrm{task}}) \ge 0.5800 \quad (+6.0\text{ pp})$$
- **Prediction:** Conditioning operator synthesis on measured task geometry $\mathcal{O}_{\mathrm{task}}$ discovers at least one viable operator family that produces failure rescues on `BENCH-004`, breaking the $52.0\%$ Oracle ceiling from EXP041/EXP042 ($b \ge 3$).
- **Falsification Criterion:** If $M_{\mathrm{Oracle}}(\mathcal{G}^*_{\mathrm{task}}) \le 0.5200$ ($b=0$), the hypothesis that automated discovery overcomes the generator existence boundary on this domain is **falsified**.

### Hypothesis 2: Zero-Corruption Autonomous Execution ($H_{\mathrm{safe}}$)
$$\text{On } \text{BENCH-004-TRANSFER}, \quad c = 0 \quad \text{and} \quad \Delta M \ge +4.0\text{ pp} \quad \text{under } B_{\mathrm{eval}} = 1.00$$
- **Prediction:** The causal response audit filters out destructive operators, allowing the audited toolbox to deliver positive headroom ($\Delta M \ge +4.0$ pp, $M \ge 0.5600$) with zero corruptions ($c=0$) under an exact $1.00$ forward pass budget.
- **Falsification Criterion:** If the audited toolbox produces $\ge 2$ corruptions ($c \ge 2$) or degrades accuracy below baseline ($M < 0.5200$), the discovery and pruning protocol is judged insufficient for safe out-of-domain transfer.

---

## 6. Reproducibility & Ledger Output

- Pre/post SHA-256 parameter hash verification: $\text{hash}_{\mathrm{pre}} == \text{hash}_{\mathrm{post}}$ ($\Delta\theta \equiv 0$).
- Exactly $1.00$ forward pass per instance during Phase B confirmatory evaluation ($B_{\mathrm{eval}} = 1.00$).
- Ledger output sealed at `experiments/runs/EXP044_cross_task_discovery/exp044_cross_task_results.json`.
