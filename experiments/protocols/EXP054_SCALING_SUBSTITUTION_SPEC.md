# EXP054 Protocol Specification: Parameter Scaling Substitution Test

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP048, EXP051  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Mandate

The fundamental question of cognitive AI architectures is:
> **Can temporary cognitive computation substitute for some amount of permanent parameter scaling?**

Rather than continually scaling parameter count ($N \times$ weights, VRAM, and memory bandwidth), can a smaller model running transient basis invention ($M_{\theta_{\text{small}}} + B_t$) match or exceed the reasoning capability of a larger model ($M_{\theta_{\text{large}}}$) at matched total inference compute?

$$\boxed{\text{Does } M(\text{Pythia-160M} + B_t) \ge M(\text{Pythia-410M}) \text{ under matched inference FLOPs?}}$$

---

## 2. Invariant Protocol Locks & Compute Matching

| Model & Mode | Parameter Count | VRAM Footprint | Forward Passes | Relative FLOPs per query |
| :--- | :--- | :--- | :--- | :--- |
| **Pythia-160M (Greedy)** | 162M | ~650 MB | 1 | $1.0\times$ |
| **Pythia-160M + SCPM ($B_t, K=4$)** | 162M | ~650 MB | 4 | $4.0\times$ |
| **Pythia-410M (Greedy)** | 405M | ~1,620 MB | 1 | $2.5\times$ |
| **Pythia-1.4B (Greedy)** | 1,414M | ~5,650 MB | 1 | $8.7\times$ |

Under FLOP-matching:
- Pythia-160M running a 4-pass candidate basis evaluation consumes $\approx 4 \times 162\text{M} = 648\text{M}$ effective FLOP-parameters, which is comparable to Pythia-410M ($405\text{M}$ FLOP-parameters).
- The memory footprint of Pythia-160M remains **$2.5\times$ smaller** than Pythia-410M and **$8.7\times$ smaller** than Pythia-1.4B.

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 The Parameter Scaling Substitution Hypothesis ($H_{\text{scale-sub}}$):
On interference and relational reasoning benchmarks (`BENCH-002-NL` and `BENCH-003`):
$$M(f_{\text{Pythia-160M}}; B_t^*) \ge M(f_{\text{Pythia-410M}}; \text{greedy})$$
with $p_{\text{McNemar}} \ge 0.05$ (non-inferiority margin $\epsilon = -0.02$) and strictly smaller memory footprint.

### 3.2 Effective Scaling Factor ($S_{\text{param}}$):
Define the empirical parameter multiplier:
$$S_{\text{param}}(B_t) = \frac{\theta_{\text{equiv}}}{\theta_{\text{actual}}}$$
The success criterion is $S_{\text{param}}(B_t) \ge 2.5\times$, proving that temporary basis invention enables a smaller network to achieve the effective capability of a model at least $2.5\times$ its parameter size.

---

## 4. Pre-Registered Falsification Criteria

The Parameter Scaling Substitution Hypothesis is **falsified** if:
1. $M(f_{\text{Pythia-160M}}; B_t^*) < M(f_{\text{Pythia-410M}}; \text{greedy}) - 0.05$ ($p < 0.05$).
2. Larger models naturally resolve the interference without basis intervention, rendering $B_t$ ineffective or obsolete at larger scales.
3. Total wall-clock latency of $160\text{M} + B_t$ exceeds the latency of $410\text{M}$ by $> 3\times$ due to sequential overhead.

---

## 5. Epistemological Interpretation Matrix

| Outcome | Epistemological Status | Interpretation |
| :--- | :--- | :--- |
| **Substitution confirmed ($S_{\text{param}} \ge 2.5$)** | `[OBSERVATION]` | Breakthrough evidence: Temporary inference-time cognitive computation can substitute for permanent model scaling, unlocking high-capability reasoning on memory-constrained edge hardware. |
| **Scaling substitution fails** | `[OBSERVATION]` | Raw parameter scaling provides representational geometry that cannot be emulated by temporary subspace operations on smaller models. |
