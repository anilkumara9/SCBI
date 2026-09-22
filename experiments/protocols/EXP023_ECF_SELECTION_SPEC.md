# EXP023 Protocol Specification: Counterfactual Evaluator Candidate Selection (End-to-End SCBI)

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team & ChatGPT (Independent Reviewer)  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP013 (Evaluator Diagnostic), EXP021 (Contrastive Gating), EXP022 (Verified Magnitude Confirmation)  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Purpose

EXP022 demonstrated that contrastive hard gating ($O5$) with verified Frobenius magnitude matching produces statistically significant confirmatory headroom under Oracle selection:
$$M_{\mathrm{Identity}} = 0.6500 \longrightarrow M_{O5,\mathrm{Oracle}} = 0.7800 \quad (\Delta M = +0.1300, p = 0.00012, CI_{95\%} = [+0.07, +0.20])$$
with positive target log-probability change ($\Delta \log p = +0.0468, CI > 0$).

However, Oracle candidate selection relies on outcome knowledge. The fundamental question of Self-Consistent Basis Invention (SCBI) is:
$$\boxed{\text{Can a frozen model autonomously discover and select a beneficial subspace without ground-truth outcome knowledge?}}$$

EXP023 integrates the confirmed $O5$ contrastive operator with the previously validated counterfactual evaluator $E_{CF}^{\mathrm{frozen}}$ to execute the **first true end-to-end test of autonomous SCBI**:
$$H \longrightarrow \mathcal{G} \longrightarrow \{V_0, V_1, V_2, V_3\} \longrightarrow E_{CF}^{\mathrm{frozen}} \longrightarrow V^* \longrightarrow O5 \longrightarrow q$$

---

## 2. Invariant Components & Leakage Protection Locks

| Component | Protocol Lock | Epistemological Status |
| :--- | :--- | :--- |
| **Model** | Frozen HuggingFace `gpt2` (124M parameters, 12 layers) | `[FACT]` Pre/post SHA-256 parameter hash verification ($\Delta\theta = 0$) |
| **Target Layer** | **Layer 8** (Block 7 output) | `[DEFINITION]` Optimal depth established across EXP016–EXP022 |
| **Operator** | **Contrastive Hard Gate ($O5$)** | `[DEFINITION]` $g_t = \mathbf{1}[d_t > 0]$ with exact Frobenius norm matching scale factor $s$ |
| **Subspace Rank** | **$r = 2$** | `[DEFINITION]` Optimal linear dimensionality established in EXP018 |
| **Operator Strength** | **$\alpha = 0.25$** | `[DEFINITION]` Optimal softening established across EXP014–EXP022 |
| **Candidate Generator** | **Oracle-free SVD** on premise $H^{(a)}$ and distractor $H^{(b)}$ | `[DEFINITION]` $K=4$ distractor candidates $V_{-,0}, V_{-,1}, V_{-,2}, V_{-,3}$ |
| **Evaluator $E_{CF}$** | **Frozen $E_{CF}$ (Zero Tuning)** | `[FACT]` Fixed formula: $e_{\mathrm{cf}}(V_k) = \mathrm{JS}(q_b, q_p) - 0.5 \cdot \mathrm{JS}(q_b, q_n)$ |
| **Confirmatory Seed** | **Seed 84 (Fresh unseen split)** | `[FACT]` Prevents post-hoc data reuse or overfitting to Seed 42 |

---

## 3. Autonomous Pipeline Formulation

For each instance $i$:
1. **Unperturbed Forward Pass:** Obtain Layer 8 hidden states $H_i$.
2. **Oracle-Free Candidate Generation:**
   - Target Subspace $V_+ \in \mathbb{R}^{d \times 2}$ from premise tokens $H[\mathcal{T}_{\mathrm{premise}}]$.
   - Distractor Subspaces $V_{-,k} \in \mathbb{R}^{d \times 2}$ ($k \in \{0, 1, 2, 3\}$) from distractor tokens $H[\mathcal{T}_{\mathrm{distractor}}]$.
3. **Counterfactual Forward Evaluations:**
   For each candidate $k \in \{0, 1, 2, 3\}$, execute forward passes under operator $O5(V_{-,k})$ on:
   - Base input $x \implies q_b(V_{-,k})$
   - Positive counterfactual input $x^+ \implies q_p(V_{-,k})$ (paraphrase of premise, same target)
   - Negative counterfactual input $x^- \implies q_n(V_{-,k})$ (entity replacement, distinct target)
4. **Frozen Evaluator Scoring:**
   $$d_{\mathrm{pos}}(V_{-,k}) = \mathrm{JS}(q_b, q_p)$$
   $$d_{\mathrm{neg}}(V_{-,k}) = \mathrm{JS}(q_b, q_n)$$
   $$e_{\mathrm{cf}}(V_{-,k}) = d_{\mathrm{pos}}(V_{-,k}) - 0.5 \cdot d_{\mathrm{neg}}(V_{-,k})$$
5. **Autonomous Candidate Selection:**
   $$k^* = \arg\min_{k \in \{0, 1, 2, 3\}} e_{\mathrm{cf}}(V_{-,k})$$
   Select optimal projector $V^* = V_{-,k^*}$ with zero outcome knowledge.
6. **Inference Execution:**
   Apply $O5(V^*)$ to generate the final autonomous output token prediction.

---

## 4. Two-Stage Experimental Design

### Stage 1: EXP023-A — Development Audit ($N_{\mathrm{dev}} = 20$, Seed 123)
Compare:
- Identity Baseline: $M_{\mathrm{Identity}}$
- Fixed Candidate Baseline: $M_{V_0}$ (Candidate 0, top singular vectors)
- Random Candidate Baseline: $M_{\mathrm{Random}}$ (Uniform random choice from $\{0, 1, 2, 3\}$)
- Counterfactual Selection: $M_{E_{CF}}$
- Oracle Upper Bound: $M_{\mathrm{Oracle}}$

**Audit Diagnostic Metrics:**
1. Headroom Recovery Ratio: $\frac{M_{E_{CF}} - M_I}{M_{\mathrm{Oracle}} - M_I}$
2. Exact Agreement: $\Pr(V_{ECF} = V_{\mathrm{Oracle}})$
3. Margins over Baselines: $M_{E_{CF}} - M_{\mathrm{Random}}$ and $M_{E_{CF}} - M_{V_0}$
4. Candidate Ranking Correlation: Mean Spearman rank correlation $\rho(R_{ECF}, R_{\mathrm{Oracle}})$ and Kendall's $\tau$ across the 4 candidate scores.

### Stage 2: EXP023-B — Confirmatory End-to-End Benchmark ($N_{\mathrm{conf}} = 100$, Seed 84)
- Benchmark: `BENCH-002-NL` on fresh unseen **Seed 84**.
- Primary End-to-End Endpoint:
  $$\Delta M_{\mathrm{autonomous}} = M_{O5,E_{CF}} - M_{\mathrm{Identity}}$$
- Pre-registered Confirmatory Criteria:
  $$\Delta M_{\mathrm{autonomous}} > 0 \quad \land \quad CI_{95\%}(\Delta M_{\mathrm{autonomous}}) > 0 \quad \land \quad p_{\mathrm{exact,one-sided}} < 0.05$$
  evaluated via exact paired binomial McNemar test and 10,000 bootstrap resamples.
- Secondary Mechanistic Hypothesis:
  $$H_{\mathrm{mech}}: \Delta \log p(y_{\mathrm{correct}})_{E_{CF}} > 0 \quad \text{with } CI_{95\%} > 0$$
- Output-Space Competition Diagnostic:
  Breakdown into Clean Win, Distractor Bias, and Third-Token Intrusion for $E_{CF}$.

---

## 5. Pre-Registered Decision Branches

```text
EXP023: End-to-End SCBI Benchmark (Identity vs. E_CF Autonomous Selection)
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
        Delta M > 0 &                     Delta M <= 0 or
        p_exact < 0.05                    p_exact >= 0.05
                 │                               │
                 ▼                               ▼
       END-TO-END SCBI                   EVALUATOR BOTTLENECK
       CONFIRMED                         ISOLATED
                 │                               │
                 ▼                               ▼
       Autonomous discovery             Operator headroom exists
       succeeds without                 (EXP022), but E_CF ranking
       labels on fresh data             accuracy requires refinement
```
