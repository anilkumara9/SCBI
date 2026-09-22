# EXP025: Cross-Template & Cross-Task Generalization Benchmark Specification

- **Experiment ID:** `EXP025`
- **Governing Rules:** [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (Laws 1–14), [`.agents/rules/00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`.agents/rules/03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md).
- **Core Research Question:** Does the frozen, autonomous SCBI pipeline ($G4, E_{CF}, O5, L=8, r=2, \alpha=0.25$) transfer out-of-distribution to permuted surface orders, diverse lexical framings, and entirely unseen task domains without hyperparameter retuning or parameter updates?

---

## 1. Scientific Hypotheses & Falsification Criteria

### Primary Hypothesis 1 (Template Transfer & Order Invariance):
$$\mathbf{H_{\mathrm{gen,template}}}: \quad \Delta M_{\mathrm{templates}} = M_{E_{CF}}(\mathrm{BENCH\text{-}003}) - M_{\mathrm{Identity}}(\mathrm{BENCH\text{-}003}) > 0$$
- **Pre-Registered Falsification Criteria:**
  - $p_{\mathrm{exact,one-sided}} \ge 0.05$ on paired McNemar test across $N=100$.
  - 10,000-resample Bootstrap 95% Confidence Interval spans or falls below 0: $\min CI_{95\%}(\Delta M) \le 0$.
  - Disparity between Target-First ($n=50$) and Distractor-First ($n=50$) subgroups reveals failure on permuted order ($\Delta M_{\mathrm{distractor\_first}} \le 0$).

### Primary Hypothesis 2 (Cross-Task & Domain Generalization):
$$\mathbf{H_{\mathrm{gen,task}}}: \quad \Delta M_{\mathrm{transfer}} = M_{E_{CF}}(\mathrm{BENCH\text{-}004}) - M_{\mathrm{Identity}}(\mathrm{BENCH\text{-}004}) > 0$$
- **Pre-Registered Falsification Criteria:**
  - $p_{\mathrm{exact,one-sided}} \ge 0.05$ on paired McNemar test across $N=100$.
  - 10,000-resample Bootstrap 95% Confidence Interval spans or falls below 0: $\min CI_{95\%}(\Delta M) \le 0$.

### Secondary Mechanistic Endpoint:
$$\mathbf{H_{\mathrm{mech}}}: \quad \mathbb{E}[\Delta \log p(y_{\mathrm{correct}})_{E_{CF}}] > 0$$
- Evaluated via bootstrap 95% confidence interval on correct-token log-probability deltas across both test suites.

---

## 2. Invariant Pipeline Locks (Zero Modifications Rule)

The autonomous pipeline is strictly locked to the exact implementation established in EXP023 and EXP024:

| Component | Locked Configuration | Status |
| :--- | :--- | :---: |
| **Foundation Model** | Frozen HuggingFace `gpt2` (124M) | SHA-256 Checksum Verified Pre/Post |
| **Model Weights** | $\theta_t \equiv \theta_0$, $\Delta\theta = 0$ | Strictly Enforced |
| **Target Depth** | Layer 8 (Block 7 output) | Fixed |
| **Subspace Rank** | $r = 2$ | Fixed |
| **Operator Strength** | $\alpha = 0.25$ | Fixed |
| **Operator Class** | Contrastive Hard Gate $O5$ ($g_t = \mathbf{1}[d_t > 0]$) with exact Frobenius norm matching scale factor $s$ | Fixed |
| **Candidate Generator** | Native $G4_{\text{sparse}}$ ($K=4$) from target-source ($H^{(a)}$) and distractor-source ($H^{(b)}$) | Fixed |
| **Evaluator** | Frozen $E_{CF}$ ($e_{\mathrm{cf}}(V_k) = \mathrm{JS}(q_b, q_p) - 0.5 \cdot \mathrm{JS}(q_b, q_n)$) | Fixed |
| **Data Leakage** | Zero target-token or label access | Zero Leakage Standard |

---

## 3. Benchmark Specifications

### Suite A: `BENCH-003-TEMPLATES` ($N=100$, Seed 250)
- Tests template invariance and positional robustness:
  - **Surface Order:**
    - 50% Target-First: `[Target Evidence] -> [Distractor Evidence] -> [Query]`
    - 50% Distractor-First: `[Distractor Evidence] -> [Target Evidence] -> [Query]`
  - **Lexical Markers:**
    - `Fact / Note`
    - `Context / Meanwhile`
    - `Record / Incident`
    - `Natural Prose` (Zero artificial headers)

### Suite B: `BENCH-004-TRANSFER` ($N=100$, Seed 350)
- Tests zero-shot task transfer across 5 completely new domains:
  1. *Corporate Ownership:* Acme Corp $\to$ subsidiary of Alphabet vs. Beta LLC acquired by Apple
  2. *Historical Imperial Capital:* Emperor Marcus ruled from Rome vs. General Claudius outpost in Carthage
  3. *Biochemical Substrate:* Amylase hydrolyzes starch vs. pepsin degrades protein
  4. *Material Craft:* Porcelain handcrafted from clay vs. industrial packaging from cardboard
  5. *Championship Award:* Championship team hoisted the trophy vs. runner-up received a ribbon

---

## 4. Evaluation & Statistical Testing Protocol

1. **Paired Comparisons:**
   - Identity ($I$) vs. Autonomous SCBI ($E_{CF}$)
   - Fixed Candidate ($V_0$) vs. Autonomous SCBI ($E_{CF}$)
   - Random Candidate ($V_{\mathrm{rand}}$) vs. Autonomous SCBI ($E_{CF}$)
   - Oracle Upper Bound ($V_{\mathrm{oracle}}$) vs. Autonomous SCBI ($E_{CF}$)
2. **Subgroup Analysis:**
   - Stratified breakdown by Surface Order: $\Delta M_{\mathrm{target\_first}}$ vs. $\Delta M_{\mathrm{distractor\_first}}$
   - Stratified breakdown by Domain Category (1 to 5)
3. **Output-Space Competition Diagnostic:**
   - Classification into Clean Win ($p_t > p_d \land p_t > p_{\max,\mathrm{other}}$), Distractor Bias ($p_d > p_t$), and Third-Token Intrusion ($p_t > p_d \land p_{\max,\mathrm{other}} > p_t$).
4. **Reproducibility Manifest:**
   - SHA-256 pre-run and post-run parameter verification.
   - Seed pinning and logging to JSON.
