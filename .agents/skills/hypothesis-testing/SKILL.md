---
name: hypothesis-testing
description: Playbook for translating informal research intuitions into falsifiable mathematical hypotheses, defining null hypotheses, establishing explicit falsification criteria, and pre-registering evaluation protocols.
---

# Hypothesis Testing Skill

This skill guides researchers and agents in transforming qualitative research ideas into formally testable, mathematically bounded, and rigorously falsifiable scientific hypotheses for **Self-Consistent Basis Invention (SCBI)**.

**Foundational Documents:**
- [`documentation/researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) §3, §4 (Central research question & core hypothesis)
- [`documentation/theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §2, §4 (Scientific status labeling and core requirements)
- [`documentation/README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md) §2 (Fixed vs working definitions)

---

## When to Use This Skill

Activate this skill whenever:
- Proposing a new capability, dynamic operator, or algorithmic variant of SCBI.
- Formulating a theorem or empirical proposition for experimental verification.
- Designing an experiment to ensure that results can unambiguously confirm or falsify a claim.
- Red-teaming an existing claim to determine if it is mathematically falsifiable.

---

## The 4 Essential Requirements of an SCBI Hypothesis

Per [`theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §4, every valid SCBI hypothesis must explicitly satisfy:

1. **Frozen Parameters:** The foundation model parameters remain strictly invariant ($\Delta\theta = 0$).
2. **Inference-Time Dynamics:** The mechanism operates during inference on an instance $x$.
3. **Transient Representation/State:** Adaptation is mediated by temporary state $z_t$ and basis $B_t$ that are discarded post-inference.
4. **Objective Selection:** The representation $B_t^*$ is selected via an explicit objective function $\mathcal{E}$, not random or oracle heuristics.

---

## Step-by-Step Hypothesis Construction Protocol

### Step 1: Formal Mathematical Statement

State the proposition using formal symbols:
- Let $x \in \mathcal{X}$ be an input, $\theta_0$ the frozen parameters, and $M: \mathcal{Y} \times \mathcal{Y} \to \mathbb{R}$ the evaluation metric.
- Define the alternative hypothesis $H_1$ and the null hypothesis $H_0$:

$$H_0: \mathbb{E}_{x \sim \mathcal{D}}\left[ M(f_{\theta_0}(x; z_T, B_T^*)) - M(f_{\theta_0}(x; \text{baseline})) \right] \le 0$$
$$H_1: \mathbb{E}_{x \sim \mathcal{D}}\left[ M(f_{\theta_0}(x; z_T, B_T^*)) - M(f_{\theta_0}(x; \text{baseline})) \right] > \epsilon \quad (\epsilon > 0)$$

*Crucial requirement:* The baseline must be matched on total compute budget (FLOPs, latency, forward passes).

---

### Step 2: Explicit Boundary Assumptions (`[ASSUMPTION]`)

Enumerate every boundary condition under which the hypothesis is asserted to hold:
- **Model Class Assumption:** (e.g., autoregressive decoder-only transformers with hidden dimension $d \ge 512$).
- **Data Distribution Assumption:** (e.g., out-of-distribution reasoning tasks requiring compositionality).
- **Compute Budget Assumption:** (e.g., maximum iterations $T \le 10$, candidate pool size $K \le 16$).

---

### Step 3: Falsification Criteria (Pre-Registration)

Define precisely what empirical findings will count as **immediate falsification**:
1. If $\Delta M \le 0$ on $\ge 50\%$ of evaluated benchmark splits.
2. If the performance gain $\Delta M$ vanishes when comparing against a compute-matched Best-of-$N$ baseline.
3. If Ablation 1 (random selection) matches or outperforms candidate selection $\mathcal{S}$ via objective $\mathcal{E}$, indicating that $\mathcal{E}$ provides zero useful signal.
4. If candidate basis invention introduces computational latency exceeding full fine-tuning without superior out-of-distribution generalization.

---

### Step 4: Standard Hypothesis Specification Template

```markdown
### Hypothesis Specification: [ID-Title]
- **Status:** `[HYPOTHESIS]`
- **Authoring Agent:** Theory Agent
- **Target Mechanism:** [e.g., Residual Stream Subspace Rotation via Self-Consistency Loss]

#### 1. Mathematical Formulation
- Objective: \mathcal{E}(B) = ...
- Update Rule: z_{t+1} = \mathcal{T}(z_t, B_t^*)
- Prediction: \hat{y} = f_{\theta_0}(x; z_T, B_T^*)

#### 2. Statistical Hypotheses
- H_0: \mathbb{E}[\Delta M] \le 0 under compute-matched forward-pass baseline.
- H_1: \mathbb{E}[\Delta M] > 0 with p < 0.01 across 5 random seeds.

#### 3. Scope & Assumptions
- [ASSUMPTION 1]: Frozen backbone weights \theta_t = \theta_0.
- [ASSUMPTION 2]: No test-label leakage during candidate evaluation.

#### 4. Falsification Protocol
- Falsified if: Ablation 1 (random basis) yields \Delta M \ge \Delta M_{\text{SCBI}}.
- Falsified if: Compute-matched self-consistency achieves equal accuracy at lower latency.
```
