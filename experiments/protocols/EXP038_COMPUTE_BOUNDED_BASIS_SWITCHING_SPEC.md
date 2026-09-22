# EXP038: Compute-Bounded Attractor Discrimination & Dynamic Basis Switching Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP038`
- **Date:** 2026-09-12
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark testing whether an internal controller can distinguish true semantic alignment from surface lexical overlap, and whether an expanded action space containing compute-bounded dynamic basis switching (`CHANGE BASIS`) can convert rolled-back failures into rescues without parameter modification ($\Delta\theta \equiv 0$).
- **Evaluated Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N = 50$ confirmatory instances, Seed 84).
- **Frozen Backbone Invariance:** Pre/post parameter SHA-256 hash verified invariant: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936`.

---

## 2. Theoretical Motivation & The Principle of Inadequate Scalars

Experiments EXP032 through EXP037 have systematically eliminated naive control observables:
1. **Static Covariance Refuted (EXP032):** $\text{Variance} \neq \text{Semantic Contrast}$ ($\Delta\log p \le -0.0145$).
2. **Output Readout Margin Refuted (EXP035):** $\text{Output Confidence} \neq \text{Latent State Integrity}$ ($c=3$ corruptions remained).
3. **Trajectory Smoothness Refuted (EXP036):** $\text{Kinematic Stability} \neq \text{Semantic Correctness}$ (Inst 22 & 28 converged smoothly at $\rho \approx 0.94$ into the wrong attractor).
4. **Perturbation Energy Refuted (EXP037):** $\text{Perturbation Resistance } (E_{\mathrm{CF}}) \neq \text{Truth}$ ($p=0.80$, perturbation resistance measures attractor basin depth, not semantic validity).

EXP037 established operational progress:
$$\boxed{\text{Kinematics } + \text{ Context Fidelity} > \text{Kinematics Alone}}$$
reducing corruptions from $c=3 \to 2 \to 1$ while retaining all $b=5$ rescues ($M=0.6800, p=0.1094$).

However, **Instance 28** leaked through because the distractor shared surface lexical unigrams with the premise, yielding a false-positive token-level context fidelity reading ($\Delta S_{\mathrm{context}} = +0.0006$).

Therefore, EXP038 addresses two critical, decoupled research questions:

$$\boxed{\textbf{Question 1: Can an internal controller distinguish semantic alignment from surface/token overlap?}}$$

$$\boxed{\textbf{Question 2: Can a model autonomously decide when its current basis is inadequate, switch to an alternative basis, and recover performance under an explicit compute budget?}}$$

---

## 3. Investigated Semantic Diagnostic Signals (Separating Gist from Surface Overlap)

To avoid manually tailoring a single metric, EXP038 compares four independently formulated internal signals:

### Signal 1: Clause Subspace Projection Differential ($S_{\mathrm{clause}}$)
Instead of averaging token vectors, extract the rank-2 principal subspace of the premise clause representations $\mathcal{V}_{\mathrm{prem}}$ and distractor clause representations $\mathcal{V}_{\mathrm{dist}}$:
$$S_{\mathrm{clause}}^{(t)} = \|P_{\mathcal{V}_{\mathrm{prem}}} h_8^{(t)}[-1]\|_2^2 - \|P_{\mathcal{V}_{\mathrm{dist}}} h_8^{(t)}[-1]\|_2^2$$
Differential: $\Delta S_{\mathrm{clause}} = S_{\mathrm{clause}}^{(2)} - S_{\mathrm{clause}}^{(1)}$.
*Mechanistic Rationale:* Clause subspace projection isolates multi-token semantic structure from individual unigram token overlaps.

### Signal 2: Inter-Layer Trajectory Alignment ($S_{\mathrm{trajectory}}$)
Cosine alignment between the current residual update $\Delta h_8^{(t)}$ and the unperturbed inter-layer forward flow vector $(h_8^{(0)} - h_6^{(0)})$ across the full sequence:
$$S_{\mathrm{trajectory}}^{(t)} = \frac{\langle \Delta h_8^{(t)}, h_8^{(0)} - h_6^{(0)} \rangle}{\|\Delta h_8^{(t)}\| \|h_8^{(0)} - h_6^{(0)}\|}$$

### Signal 3: Trajectory Acceleration / Curvature ($\kappa_t$)
The geometric acceleration norm between consecutive step updates:
$$\kappa_2 = \frac{\|\Delta h_8^{(2)} - \Delta h_8^{(1)}\|}{\|\Delta h_8^{(1)}\|}$$
*Mechanistic Rationale:* Detecting whether the representation is bending sharply toward an off-manifold distractor basin even if instantaneous step displacement appears normal.

### Signal 4: Baseline Context Representation Fidelity ($S_{\mathrm{context}}$ from EXP037)
Standard mean-context cosine similarity (serving as the control baseline).

---

## 4. Compute-Bounded Action Space & Alternative Basis Generation

The controller policy $\pi_t$ operates over the expanded action space:
$$\mathcal{A} = \{\text{CONTINUE}, \text{STOP}, \text{ROLLBACK}, \text{CHANGE BASIS}\}$$

### Explicit Forward-Pass Compute Budget ($B_{\mathrm{eval}} \le 3$)
To prevent unconstrained search where rollback simply tries random bases until something hits:
- Every instance begins with a budget of at most **$3$ total forward passes** (including base forward pass $T=0$).
- Step 1 uses primary relational trajectory basis $V_1 = \operatorname{SVD}(h_8 - h_6)_{1:2}$.
- If Step 1 triggers `ROLLBACK` (due to kinematic violation or semantic collapse):
  - Rather than passively terminating at Step 1, the controller spends its final forward pass on `CHANGE BASIS`.
  - Alternative candidate basis: **Secondary Orthogonal Trajectory Subspace** $V_2 = \operatorname{SVD}(h_8 - h_6)_{3:4}$ (the principal orthogonal complement to the primary direction).
  - If the alternative basis satisfies controller criteria, it is accepted; otherwise, the controller performs final terminal rollback to Step 1.

---

## 5. Compute-Normalized Performance Metrics

In addition to discrete Top-1 accuracy and exact paired McNemar tests, EXP038 tracks compute-normalized efficiency:

1. **Marginal FLOP Efficiency:**
   $$\eta_{\mathrm{compute}} = \frac{\Delta\log p_{\mathrm{target}}}{\text{Total Forward Passes}}$$
2. **Rescue Yield per Evaluation:**
   $$Y_{\mathrm{rescue}} = \frac{b}{\sum \text{Forward Passes}}$$
3. **Discrete Accuracy Scorecard:**
   - Accuracy $M$, Headroom $\Delta M$ vs. $M_I$, Discordant pairs $(b, c)$, Paired McNemar $p$-value, 95% Bootstrap CI.

---

## 6. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Surface Overlap Disentanglement ($H_{\mathrm{overlap}}$)
At least one candidate semantic signal ($S_{\mathrm{clause}}$ or $S_{\mathrm{trajectory}}$) correctly discriminates Instance 28 as a corrupting update ($\Delta S < 0$) while retaining positive scores on genuine rescues (Inst 30 & 35).

### Hypothesis 2: Compute-Bounded Basis Switching Efficacy ($H_{\mathrm{switch}}$)
$$\Delta M(\pi_{\mathrm{switch}}) \ge +8.0\text{ pp} \quad \text{with} \quad c = 0 \quad \text{under} \quad B_{\mathrm{eval}} \le 3$$
- **Predicted Outcome:** The dynamic switching controller recovers at least one previously rolled-back failure instance via the secondary basis $V_2$ without corrupting any baseline-correct instances ($c=0$), lifting accuracy while strictly respecting $B_{\mathrm{eval}} \le 3$.
- **Falsification Criterion:** If switching to $V_2$ produces net zero additional rescues or introduces new corruptions ($c \ge 1$), the hypothesis that secondary subspace switching provides autonomous recovery under frozen weights is rejected.

---

## 7. Statistical & Reproducibility Protocol
- Target Model: `EleutherAI/pythia-160m`, Seed 84, $N=50$ confirmatory instances.
- Parameter immutability guarantee: Pre-run SHA-256 == Post-run SHA-256 ($\Delta\theta \equiv 0$).
- Results saved to: `experiments/runs/EXP038_basis_switching/exp038_basis_switching_results.json`.
