# EXP037: Semantic Trajectory Verification Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP037`
- **Date:** 2026-09-12
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark evaluating whether internal semantic consistency metrics—evaluated in combination with kinematic bounds—can prospectively predict whether a recurrence step is beneficial ($b$-event) or harmful ($c$-event), enabling an autonomous controller to retain failure rescues ($b=5$) while eliminating smooth representation corruption ($c \to 0$).
- **Evaluated Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N = 50$ confirmatory instances, Seed 84).
- **Frozen Backbone Guarantee:** Parameter SHA-256 hash verified invariant before and after inference: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).

---

## 2. Theoretical Motivation: Beyond Kinematic Smoothness

EXP036 produced a critical conceptual distinction:
$$\boxed{\text{Kinematic Smoothness } (\rho \approx 1) \neq \text{ Semantic Correctness}}$$

While kinematic bounding caught geometric collapse (Inst 39: $d_2 = 0.1628, \rho_2 = 0.3984$), it failed to catch **smooth attractor drift** (Inst 22 & 28: $\rho_2 > 0.94, \Delta H < 0$), where the representation moved smoothly and confidently into the distractor basin.

To safely govern recurrence, the inference controller cannot rely on kinematic observables alone ($K_t$). It requires a **Semantic State Evaluator ($S_t$)**:
$$\boxed{\pi_t = f(K_t, S_t) \longrightarrow \{\text{ACCEPT Step 2}, \text{ROLLBACK to Step 1}\}}$$

$$\boxed{\textbf{Central Question: Can Internal Semantic Consistency Detect Smooth Attractor Drift and Eliminate Corruptions Without Sacrificing Rescues?}}$$

---

## 3. Candidate Semantic Trajectory Signals ($S_t$)

All candidate signals are computed using internal activations available *before* Step 2 is accepted, without exposing ground-truth targets:

### Signal 1: Context Representation Fidelity ($S_{\mathrm{context}}$)
Cosine similarity between the final-token representation $h_8^{(t)}[-1]$ and the prompt's context representation $\bar{h}_{\mathrm{context}}$ (mean across non-distractor context tokens):
$$S_{\mathrm{context}}^{(t)} = \frac{\langle h_8^{(t)}[-1], \bar{h}_{\mathrm{context}} \rangle}{\|h_8^{(t)}[-1]\| \|\bar{h}_{\mathrm{context}}\|}$$
Differential: $\Delta S_{\mathrm{context}} = S_{\mathrm{context}}^{(2)} - S_{\mathrm{context}}^{(1)}$.
*Hypothesis:* Smooth drift into the distractor attractor pulls representation away from the context premise ($\Delta S_{\mathrm{context}} < 0$).

### Signal 2: Counterfactual Perturbation Energy ($E_{\mathrm{CF}}$)
Compute residual divergence under 20% prompt token masking:
$$E_{\mathrm{CF}}^{(t)} = \frac{1}{T} \sum_{i=1}^T \|h_8^{(t)}[i] - h_{8,\mathrm{pert}}^{(t)}[i]\|_2^2$$
Differential: $\Delta E_{\mathrm{CF}} = E_{\mathrm{CF}}^{(2)} - E_{\mathrm{CF}}^{(1)}$.
*Hypothesis:* True failure rescues stabilize the attractor against contextual perturbation ($\Delta E_{\mathrm{CF}} \le 0$), whereas distractor capture increases sensitivity.

### Signal 3: Prompt Instruction Alignment ($S_{\mathrm{instr}}$)
Cosine similarity to the instruction/question prefix tokens.

---

## 4. Evaluated Controllers in EXP037

1. **Baseline ($M_I$):** Unintervened single pass ($M_I = 0.6000$).
2. **Supervised Reference ($G_{\mathrm{contrastive}}$):** Gold-standard token contrast ($+14.0$ pp, $p=0.0078$).
3. **Fixed $T=1$ Deliberation:** Single-step trajectory ($+6.0$ pp, $b=3, c=0$).
4. **Fixed $T=2$ Deliberation:** Blind 2-step recurrence ($+4.0$ pp, $b=5, c=3$).
5. **Kinematic-Only Rollback (EXP036 champion):** Rollback if $\rho_2 < 0.4$ or $d_2 > 0.14$ ($+6.0$ pp, $b=5, c=2$).
6. **Composite Controller 1 ($\pi_{K + S_{\mathrm{context}}}$):**
   Accept Step 2 if kinematic bounds hold AND $\Delta S_{\mathrm{context}} \ge 0$; else rollback to Step 1.
7. **Composite Controller 2 ($\pi_{K + E_{\mathrm{CF}}}$):**
   Accept Step 2 if kinematic bounds hold AND $\Delta E_{\mathrm{CF}} \le 0$; else rollback to Step 1.
8. **Composite Controller 3 ($\pi_{\mathrm{full}}$):**
   Accept Step 2 if kinematic bounds hold AND both $\Delta S_{\mathrm{context}} \ge 0$ and $\Delta E_{\mathrm{CF}} \le 0$; else rollback to Step 1.

---

## 5. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Semantic Corruption Discrimination ($H_{\mathrm{semantic\_sep}}$)
At least one semantic trajectory signal ($\Delta S_{\mathrm{context}}$ or $\Delta E_{\mathrm{CF}}$) shows statistically significant separation between Gain events ($N=5$) and smooth corruption events ($N=2$) (Mann-Whitney $U$, $p < 0.05$).

### Hypothesis 2: Autonomous Headroom Recovery ($H_{\mathrm{recovery}}$)
$$\Delta M(\pi^*) \ge +10.0\text{ pp} \quad \text{AND} \quad c \le 1 \quad \text{AND} \quad p < 0.05 \text{ vs. } M_I$$
- **Predicted Outcome:** The composite controller eliminates smooth corruptions ($c \le 1$) while preserving at least 4 of the 5 rescues ($b \ge 4$), yielding $\ge +10.0$ pp net headroom ($70.0\%+$ accuracy) autonomously without labels.
- **Falsification Criterion:** If all composite controllers fail to reduce corruptions below $c=2$ or sacrifice rescues such that $\Delta M \le +6.0$ pp, the hypothesis that semantic context metrics solve smooth attractor drift is rejected.

---

## 6. Statistical Protocol
- Pre/post parameter SHA-256 hash verified invariant ($\Delta\theta \equiv 0$).
- 1,000-resample bootstrap 95% confidence intervals for $\Delta M$.
- Exact Paired McNemar tests vs. $M_I$ and vs. Fixed $T=1$.
- Output saved to `experiments/runs/EXP037_semantic_verification/exp037_semantic_verification_results.json`.
