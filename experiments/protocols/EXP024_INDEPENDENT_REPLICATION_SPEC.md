# EXP024 Protocol Specification: Independent Cross-Seed Replication Benchmark

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team & ChatGPT (Independent Reviewer)  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP022 (Verified Magnitude Operator), EXP023 (Autonomous End-to-End SCBI)  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Purpose

In EXP023, autonomous Self-Consistent Basis Invention (SCBI) was demonstrated on a fresh unseen benchmark split (`BENCH-002-NL`, $N=100$, Seed 84):
$$M_{\mathrm{Identity}} = 0.6400 \longrightarrow M_{E_{CF}} = 0.7100 \quad (\Delta M = +0.0700, p_{\mathrm{exact}} = 0.00781, CI_{95\%} = [+0.0300, +0.1200])$$
recovering $87.5\%$ of available Oracle headroom autonomously with zero outcome label access.

To ensure that this finding is not an artifact of a single benchmark split or a statistical fluctuation on Seed 84, **EXP024 executes a strict independent replication on a second fresh confirmatory seed (Seed 168, $N=100$)** with all pipeline components held completely frozen:
$$\boxed{\text{Does the }+7\%\text{ autonomous SCBI headroom reproduce on a second independent benchmark split?}}$$

---

## 2. Invariant Pipeline Locks & Zero-Tuning Safeguards

Every component is locked to the exact implementation validated in EXP023:

| Component | Protocol Lock | Epistemological Basis |
| :--- | :--- | :--- |
| **Model** | Frozen HuggingFace `gpt2` (124M parameters, 12 layers) | `[FACT]` Pre/post SHA-256 parameter hash verification ($\Delta\theta = 0$) |
| **Target Layer** | **Layer 8** (Block 7 output) | `[DEFINITION]` Confirmed single-layer depth |
| **Operator** | **Contrastive Hard Gate ($O5$)** | `[DEFINITION]` $g_t = \mathbf{1}[d_t > 0]$ with exact Frobenius norm matching scale factor $s$ |
| **Subspace Rank** | **$r = 2$** | `[DEFINITION]` Subspace dimensionality |
| **Operator Strength** | **$\alpha = 0.25$** | `[DEFINITION]` Operator softening coefficient |
| **Candidate Generator** | **Oracle-free SVD** on premise $H^{(a)}$ and distractor $H^{(b)}$ | `[DEFINITION]` $K=4$ distractor candidates $V_{-,0}, V_{-,1}, V_{-,2}, V_{-,3}$ |
| **Evaluator $E_{CF}$** | **Frozen $E_{CF}$ (Zero Tuning)** | `[FACT]` Fixed formula: $e_{\mathrm{cf}}(V_k) = \mathrm{JS}(q_b, q_p) - 0.5 \cdot \mathrm{JS}(q_b, q_n)$ |
| **Confirmatory Seed** | **Seed 168 (Second fresh unseen split)** | `[FACT]` Strictly isolated from Seed 42 and Seed 84 |

---

## 3. Pre-Registered Endpoints & Cross-Seed Analysis Protocol

### 1. Primary Endpoint (Seed 168 Replication):
$$\Delta M_{168} = M_{E_{CF}, 168} - M_{\mathrm{Identity}, 168}$$
- Pre-registered replication criterion:
  $$\Delta M_{168} > 0 \quad \land \quad CI_{95\%}(\Delta M_{168}) > 0 \quad \land \quad p_{\mathrm{exact,one-sided}} < 0.05$$
  evaluated via exact paired binomial McNemar test and 10,000 bootstrap resamples.

### 2. Secondary Mechanistic Hypothesis:
$$H_{\mathrm{mech}}: \Delta \log p(y_{\mathrm{correct}})_{E_{CF}, 168} > 0 \quad \text{with } CI_{95\%} > 0$$

### 3. Cross-Seed Stratified & Pooled Analysis:
To prevent seed pooling from masking seed-specific variability, both per-seed and pooled statistics will be reported:
- **Per-Seed Reporting:**
  - Seed 84: $M_{I, 84}, M_{E_{CF}, 84}, \Delta M_{84}, p_{84}, CI_{95\%, 84}$
  - Seed 168: $M_{I, 168}, M_{E_{CF}, 168}, \Delta M_{168}, p_{168}, CI_{95\%, 168}$
- **Consistency Evaluation:** Check whether $\Delta M_s > 0$ across both seeds with overlapping confidence intervals.
- **Pooled Inference ($N_{\mathrm{total}} = 200$):**
  $$\Delta M_{\mathrm{pooled}} = \frac{M_{E_{CF}, 84} + M_{E_{CF}, 168}}{2} - \frac{M_{I, 84} + M_{I, 168}}{2}$$
  Exact paired McNemar test and stratified cluster bootstrap 95% CI on the pooled $N=200$ evaluation.

---

## 4. Pre-Registered Decision Branches

```text
EXP024: Independent Cross-Seed Replication Benchmark (Seed 168, N=100)
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
       Delta M_168 > 0 &               Delta M_168 <= 0 or
       p_exact < 0.05                  p_exact >= 0.05
                 │                               │
                 ▼                               ▼
       REPLICATION CONFIRMED           BENCHMARK VARIABILITY /
                 │                     MARGINAL HEADROOM
                 ▼                               │
       Autonomous SCBI is                        ▼
       robust across unseen            Analyze seed-level instance
       benchmark splits                distributions & third-token
                                       competition divergence
```
