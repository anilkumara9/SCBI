# EXP055 Protocol Specification: Specialization Substitution & Plasticity Test

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP048, EXP054  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Mandate

The secondary pillar of the substitution frontier is:
> **Can temporary cognitive computation substitute for permanent specialization (parameter fine-tuning)?**

Standard adaptation requires fine-tuning weights (LoRA or full SFT), which incurs three critical costs:
1. Catastrophic forgetting / capability degradation on un-targeted domains.
2. Parameter storage explosion (maintaining distinct adapters $\Delta\theta$ per task).
3. Inability to switch tasks dynamically within a single prompt.

SCPM hypothesizes that temporary basis invention ($M_\theta + B_t$) provides task specialization while preserving $\Delta\theta = 0$ and completely eliminating catastrophic forgetting.

$$\boxed{\text{Does temporary basis invention match LoRA task performance while achieving zero catastrophic forgetting?}}$$

---

## 2. Experimental Conditions

| Condition | Adaptation Mode | Weight Status | Domain Transfer / Retention |
| :--- | :--- | :--- | :--- |
| **C0: Frozen Base** | Zero-shot | $\Delta\theta = 0$ | Baseline retention |
| **C1: LoRA Fine-Tuned** | Permanent adapter ($r=2$) | $\Delta\theta \ne 0$ | Evaluated on target + general suite |
| **C2: SCPM ($B_t$)** | Transient subspace ($r=2$) | $\Delta\theta = 0$ | Evaluated on target + general suite |

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 Specialization Parity on Target Task:
On target benchmark (`BENCH-002-NL`):
$$M(M_\theta + B_t) \ge 0.85 \times M(M_{\theta + \Delta\theta_{\text{LoRA}}})$$
Temporary basis invention must recover at least $85\%$ of the headroom achieved by permanent LoRA weight modification.

### 3.2 Zero Catastrophic Forgetting Invariant:
On a diverse retention suite of general NLP tasks (Lambada completion, WinoGrande reasoning, and in-domain perplexity):
$$\Delta M_{\text{general}}(M_\theta + B_t) = 0.00\% \quad (\text{exact invariance via } \Delta\theta = 0 \text{ when } B_t \text{ is discarded})$$
whereas LoRA exhibits statistically significant degradation:
$$\Delta M_{\text{general}}(M_{\theta + \Delta\theta_{\text{LoRA}}}) \le -2.5\text{ pp} \quad (p < 0.01)$$

---

## 4. Pre-Registered Falsification Criteria

Specialization substitution is **falsified** if:
1. LoRA achieves overwhelming superiority ($M_{\text{LoRA}} - M_{B_t} > 20\text{ pp}$), indicating that linear subspace projection cannot approximate non-linear parameter adaptation.
2. Applying $B_t$ causes uncontrolled damage to off-target tokens within the same sequence, producing syntax breakdown.

---

## 5. Epistemological Interpretation Matrix

| Outcome | Epistemological Status | Interpretation |
| :--- | :--- | :--- |
| **Both criteria passed** | `[OBSERVATION]` | Temporary cognitive computation successfully substitutes for permanent weight specialization, delivering zero-forgetting task versatility without storing separate parameter checkpoints. |
| **Temporary basis falls short** | `[OBSERVATION]` | Permanent weight optimization alters internal manifold geometry in fundamental non-linear ways that transient subspace interventions cannot replicate. |
