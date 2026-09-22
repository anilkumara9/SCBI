# EXP050 Protocol Specification: Cross-Task & Generalization Transfer Battery

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP048, EXP049  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Mandate

A central requirement of Hypothesis A (General Cognitive Control) is that transient representation construction operates as a general inferential mechanism, not merely a syntax-cancellation patch for distractor-token spans.

**EXP050 evaluates temporary representation modulation across 4 distinct cognitive task paradigms:**
1. **Task T1 (Distractor Interference / BENCH-002-NL):** Suppressing misleading context spans.
2. **Task T2 (Relational Binding / BENCH-003):** Multi-hop relational predicate-argument binding.
3. **Task T3 (Counterfactual Premise Override / BENCH-005):** Overriding world knowledge priors with explicit counterfactual premises.
4. **Task T4 (Variable Binding / Induction / BENCH-004):** Maintaining sequential token-to-variable bindings.

$$\boxed{\text{Does temporary basis construction modulate diverse reasoning paradigms or only distractor spans?}}$$

---

## 2. Invariant Protocol Locks

| Parameter | Protocol Lock | Epistemological Basis |
| :--- | :--- | :--- |
| **Model** | `EleutherAI/pythia-160m` | `[FACT]` Pre/post SHA-256 hash invariant ($\Delta\theta = 0$) |
| **Target Layer** | Layer 7 (0-indexed = Block 7) | `[DEFINITION]` Middle representational depth |
| **Subspace Rank** | $r = 2$ | `[DEFINITION]` Subspace dimensionality |
| **Operator Strength** | $\alpha = 0.25$ | `[DEFINITION]` Standard attenuation coefficient |
| **Sample Size** | $N = 50$ instances per task paradigm | `[FACT]` Fixed evaluation set |
| **Basis Construction** | Contrastive SVD on task-specific functional spans | `[DEFINITION]` Identical algebraic operator across tasks |

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 Primary Multi-Task Endpoint:
Across the 4 task paradigms $\{T_1, T_2, T_3, T_4\}$:
- Headroom recovery:
  $$\eta(T) = \frac{M_{G}(T) - M_{\text{base}}(T)}{M_{\text{oracle}}(T) - M_{\text{base}}(T)}$$
- Success threshold:
  $$\text{Mean}(\Delta M) > +5.0\text{ pp} \quad \land \quad \Delta M(T) > 0 \text{ on } \ge 3/4 \text{ tasks}$$
  with family-wise error rate controlled at $\alpha_{\text{FWER}} = 0.05$ via Holm-Bonferroni correction.

### 3.2 Non-Destructive Side-Effect Invariant:
On a held-out standard language modeling evaluation (Lambada perplexity or next-token cross-entropy):
$$\Delta \text{Loss}_{\text{general}} \le +0.02 \text{ nats}$$
The temporary basis must not cause global representational collapse.

---

## 4. Pre-Registered Falsification Criteria

Hypothesis A (General Cognitive Control) is **falsified** in favor of Hypothesis B (Task-Specific Activation Intervention) if:
1. $\Delta M \le 0$ on all tasks other than T1 (Distractor Interference).
2. The intervention causes catastrophic collapse ($\Delta M \le -10\text{ pp}$) on relational binding (T2) or counterfactual override (T3).
3. Random subspace ablation matches or outperforms task-directed basis construction across the multi-task suite.

---

## 5. Epistemological Interpretation Matrix

| Outcome | Epistemological Status | Interpretation |
| :--- | :--- | :--- |
| **Gains replicate across $\ge 3/4$ tasks** | `[OBSERVATION]` | Strongly supports Hypothesis A: Temporary subspace invention serves as a general inference-time cognitive control mechanism for modulating latent circuits. |
| **Gains strictly confined to T1** | `[OBSERVATION]` | Decisively establishes Hypothesis B: The effect is an idiosyncratic artifact of distractor-token suppression, not a general cognitive mechanism. |
