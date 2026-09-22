# EXP022 Protocol Specification: Verified-Magnitude Contrastive Confirmation

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP013–EXP021  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Purpose

In EXP021-A, contrastive relative-evidence gating demonstrated a qualitatively distinct mechanistic signal:
- For the first time, target token log-probability increased over Identity on the development split ($\Delta \log p(y_{\mathrm{correct}}) = +0.0882 > 0$).
- Contrastive preference reached 100% ($\text{Pref} = 1.0000$), and non-distractor tokens experienced zero displacement ($D_{d \le 0} = 0.0000$).

However:
1. An implementation audit revealed that realized perturbation must be audited and matched strictly via the **matrix Frobenius norm** $\frac{\|\Delta H\|_F}{\|H\|_F}$ to guarantee that O5 does not benefit from lower total displacement.
2. Top-1 exact match accuracy remained plateaued at $0.7000$ on the development split.

EXP022 executes a formal confirmatory benchmark on **$N=100$ (Seed 42)** to test whether O5 achieves statistically significant representation-level gain and to diagnose the exact output-space competition structure governing the remaining errors.

---

## 2. Invariant Components & Protocol Locks

| Component | Protocol Lock | Epistemological Status |
| :--- | :--- | :--- |
| **Model** | Frozen HuggingFace `gpt2` (124M parameters, 12 layers) | `[FACT]` Pre-run & post-run SHA-256 parameter hash verification ($\Delta\theta = 0$) |
| **Benchmark** | `BENCH-002-NL` Confirmatory Split ($N_{\mathrm{conf}}=100$, seed 42) | `[FACT]` Pre-registered distractor suppression benchmark |
| **Layer** | **Layer 8** (Block 7 output) | `[DEFINITION]` Optimal single-layer depth |
| **Subspace Rank** | **$r = 2$** | `[DEFINITION]` Optimal linear dimensionality |
| **Base Strength** | **$\alpha = 0.25$** | `[DEFINITION]` Optimal continuous intervention strength |
| **Scope** | All-token residual stream (modulated by contrastive gate $g_t$ and exact scale $s$) | `[DEFINITION]` Token-level contrastive intervention |
| **Baseline** | Identity ($\alpha = 0 \implies P = I, M_I = 0.6500$) | `[FACT]` Unperturbed foundation model reference |

---

## 3. Operators Compared & Exact Magnitude Matching

For each instance in `BENCH-002-NL`:
1. **Oracle-Free Contrastive Basis Construction:**
   - Target Subspace $V_+ \in \mathbb{R}^{d \times 2}$: SVD on premise tokens $H[\mathcal{T}_{\mathrm{premise}}]$.
   - Distractor Subspace $V_- \in \mathbb{R}^{d \times 2}$: SVD on distractor tokens $H[\mathcal{T}_{\mathrm{distractor}}]$.
2. **Relative Evidence Difference:**
   $$d_t = \|V_-^\top h_t\|_2 - \|V_+^\top h_t\|_2$$
3. **Exact Realized Frobenius Magnitude Matching:**
   $$s = \frac{\|H V_- V_-^\top\|_F}{\|\operatorname{diag}(g) H V_- V_-^\top\|_F} = \frac{\sqrt{\sum_{t=1}^T \|V_-^\top h_t\|_2^2}}{\sqrt{\sum_{t=1}^T g_t^2 \|V_-^\top h_t\|_2^2}}$$
   $$\text{Audit Requirement: } \max_{i=1}^{100} \left| \frac{\|\Delta H_{\mathrm{O5},i}\|_F}{\|H_i\|_F} - \frac{\|\Delta H_{\mathrm{O0},i}\|_F}{\|H_i\|_F} \right| < 10^{-7}$$

### Operators:
- **Identity ($I$):** $h_t' = h_t$
- **O0 (Uniform Linear Baseline):** $g_t = 1.0, s = 1.0 \implies h_t' = h_t - 0.25 V_- V_-^\top h_t$
- **O5 (Contrastive Hard Gate):** $g_t = \mathbf{1}[d_t > 0] \implies h_t' = h_t - 0.25 s \cdot \mathbf{1}[d_t > 0] \cdot V_- V_-^\top h_t$

---

## 4. Pre-Registered Endpoints & Decision Criteria

1. **Primary Top-1 Endpoint:**
   $$\Delta M = M_{\mathrm{O5}} - M_{\mathrm{Identity}}$$
   - Pre-registered confirmation criterion: $\Delta M > 0$, $CI_{95\%}(\Delta M) > 0$, and exact paired McNemar $p < 0.05$.
2. **Secondary Mechanistic Hypothesis ($H_{\mathrm{mech}}$):**
   $$\boxed{H_{\mathrm{mech}}: \Delta \log p(y_{\mathrm{correct}}) > 0}$$
   - Evaluated via 95% bootstrap confidence interval. Supported if $CI_{95\%}(\Delta \log p)$ strictly excludes zero.
3. **Secondary Margin Hypothesis:**
   $$\Delta \mathrm{Margin} = [p(y_{\mathrm{target}}) - p(y_{\mathrm{distractor}})]_{\mathrm{O5}} - [p(y_{\mathrm{target}}) - p(y_{\mathrm{distractor}})]_{\mathrm{Identity}} > 0$$

---

## 5. Output-Space Competition Diagnostic

To explain why contrastive preference reaches 100% while Top-1 exact match remains around $\sim 0.70$, every instance $i \in \{1, \dots, 100\}$ will record the tripartite output probability competition:
- $p_i(y_{\mathrm{target}})$
- $p_i(y_{\mathrm{distractor}})$
- $p_{i,\max,\mathrm{other}} = \max_{y \notin \{y_{\mathrm{target}}, y_{\mathrm{distractor}}\}} p_i(y)$

### Three Mutually Exclusive Outcome Categories:
1. **Clean Win (Target Dominance):**
   $$p(y_{\mathrm{target}}) > p(y_{\mathrm{distractor}}) \quad \land \quad p(y_{\mathrm{target}}) > p_{\max,\mathrm{other}} \implies \text{Top-1 Correct}$$
2. **Distractor Bias (Distractor Dominance):**
   $$p(y_{\mathrm{distractor}}) > p(y_{\mathrm{target}}) \implies \text{Distractor Error}$$
3. **Third-Token Intrusion (The Competition Failure Mode):**
   $$p(y_{\mathrm{target}}) > p(y_{\mathrm{distractor}}) \quad \land \quad p_{\max,\mathrm{other}} > p(y_{\mathrm{target}})$$
   *(Distractor was successfully suppressed below target, but an unrelated third vocabulary token won greedy selection).*

---

## 6. Pre-Registered Decision Branches

```text
EXP022: Verified-Magnitude Contrastive Confirmation (N=100)
Identity vs. Uniform Linear (O0) vs. Contrastive Hard Gate (O5)
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
          Delta M > 0 &                 Delta M ~ 0, but
          p_exact < 0.05                H_mech confirmed
                 │                             │
                 ▼                             ▼
          Full SCBI End-to-End          Analyze Output-Space
          Confirmation Passed           Competition Diagnostic
                 │                             │
                 ▼                             ▼
          Prepare Paper Section         Isolate Third-Token
          on Confirmed SCBI             Intrusion Frequency
```
