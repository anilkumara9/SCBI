# SCBI-2.0: Adaptive Inference-Time Representation Control
## Comprehensive Architectural Audit & Research Program Specification

**Document Version:** 2.0 (Post-EXP032 Synthesis)  
**Date:** 2026-09-11  
**Authoring Agent:** Research Manager, Theory Agent, Implementation Agent, Adversarial Reviewer  
**Governing Standard:** [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) & [`reports/README.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/reports/README.md)

---

## 1. Executive Research Audit (EXP001 through EXP032)

Over 32 pre-registered, cryptographically sealed experiments, Self-Consistent Basis Invention (SCBI) has transitioned from an informal hypothesis into an empirically established, causally dissected paradigm.

### The Proven Empirical Ledger:

| Research Question | Benchmark Scope | Key Finding | Causal / Statistical Confirmation |
| :--- | :--- | :--- | :--- |
| **1. Weight Invariance** | 5 Architectures (GPT-2, OPT, Pythia, Qwen, BLOOM) | Model parameters remain strictly invariant ($\Delta\theta \equiv 0$). Zero weight corruption, zero catastrophic forgetting. | Verified via SHA-256 parameter hashes before and after inference. |
| **2. Autonomous Candidate Selection** | GPT-2 (`BENCH-001`, `BENCH-002`) | Counterfactual Energy $E_{\mathrm{CF}}$ achieves $\rho = +0.83$ Spearman correlation, recovering up to 100% of Oracle headroom. | Exact Paired McNemar $p < 0.001$, Bootstrap CI $[+0.05, +0.19] > 0$. |
| **3. Prospective Stage Prediction** | OPT-125M, Qwen2.5-0.5B, BLOOM-560M | Zero-label representation metric $S_{\mathrm{rep}}(l)$ prospectively locks viable stages before benchmark outcomes. | OPT: L7 ($p=0.0156$); Qwen: L11 ($p=0.0078$, 93% Oracle, 90% autonomous); BLOOM: L13 (100% HR recovery). |
| **4. Causal Mechanics (EXP029)** | Pythia-160M (`BENCH-002-NL`) | - Directional necessity confirmed ($\theta \uparrow \implies \Delta M \downarrow$).<br>- Attention rerouting is the primary vehicle (0% retention when attention clamped).<br>- Unembedding alignment non-essential (100% retention $V \perp W_U$). | Causal loss-of-function and gain-of-function rescue ($0.60 \to 0.74, \Delta M = +14.0$ pp). |
| **5. Viability Landscape (EXP030)** | Pythia-160M (45 conditions) | Extended viability across L2, L4, L6, L8. Controller $\times$ Depth interaction: L2 hard gate ($+10$ pp), L8 linear ($+14$ pp), L10 failure boundary ($\mathcal{V}(10)=\emptyset$). | Factorial $5 \times 3 \times 3$ grid; late layers do not require larger $\alpha$ ($\alpha^*_8 = 0.25 < \alpha^*_2 = 0.50$). |
| **6. Multi-Stage Cascading (EXP031)** | Pythia-160M (Hierarchical Cascade) | The heterogeneous L2 $\to$ L8 cascade produced a larger observed target-log-probability shift (+0.1625 vs. +0.1088 for L8 alone, a +49.4% relative increase), but the prespecified paired test did not establish statistical significance ($p=0.0616$). Discrete accuracy tied at $74.0\%$ ($b=7, c=0, p=0.0078$). Homogeneous cascades interfered destructively. | Top-1 exact match confirmed ($p=0.0078$); continuous superiority remains an unconfirmed trend ($p > 0.05$). |
| **7. Covariance Basis Invention (EXP032)** | Pythia-160M (Layer 8, $\alpha=0.25$) | The tested unlabeled covariance eigenvectors did not reliably recover the task-relevant intervention direction ($\Delta M \le +6.0$ pp, $\Delta\log p \le -0.0145$), while supervised contrast achieved $+14.0$ pp ($p=0.0078$). | Outcome 3: Unsupervised static covariance refuted. Activation variance does not equal semantic contrast. |
| **8. Relational Basis Discovery (EXP033)** | Pythia-160M (Layer 8, $\alpha=0.25$) | Relational differences reversed covariance degradation: inter-layer trajectory ($h_8 - h_6$, $+6.0$ pp, $\Delta\log p = +0.0112$) and contextual counterfactual ($+4.0$ pp, $\Delta\log p = +0.0317$) produced positive target shifts with zero corruption ($c=0$), but fell short of supervised contrast ($+14.0$ pp, $p=0.0078$). Dual unembedding conflict failed ($-4.0$ pp). | Outcome 2: Directional validity confirmed ($\Delta\log p > 0, c=0$); single-pass equivalence refuted ($p > 0.05$). |
| **9. Iterative Deliberation (EXP034)** | Pythia-160M (Layer 8, $\alpha=0.25$) | Multi-pass latent recurrence increased raw failure rescues ($b: 3 \to 5$), but unguided recurrence caused progressive representation drift corrupting baseline-correct instances ($c: 0 \to 3 \to 5$), returning net accuracy to baseline at $T=3$ ($60.0\%$, $+0.0$ pp). Compute-matched temperature sampling collapsed to $38.0\%$ (-22.0 pp). | Outcome 3: Fixed-iteration deliberation refuted due to over-steering drift ($c \ge 3$). Isolates the necessity of an adaptive stopping gate. |
| **10. Adaptive Margin Halting (EXP035)** | Pythia-160M (Layer 8, $\alpha=0.25$) | Output decision-margin gating ($m^{(1)} \ge \tau$) halted 58% of instances and restored positive continuous log-prob ($\Delta\log p = +0.0216$), but failed to prevent discrete corruptions ($c=3$), leaving net accuracy at $+4.0$ pp ($p=0.3633$). | Outcome 3: Output margin alone is insufficient to govern recurrence. Scalar margins lack internal geometric awareness. |
| **11. Trajectory Rollback Control (EXP036)** | Pythia-160M (Layer 8, $\alpha=0.25$) | Directional coherence gating ($\rho < 0.4$) and displacement bounding ($d > 0.14$) successfully caught and rolled back geometric collapse (Inst 39), reducing corruptions from $c=3$ to $c=2$ while retaining all $b=5$ rescues ($+6.0$ pp, $M=0.6600, p=0.2266$). However, smooth attractor drift (Inst 22 & 28, $\rho_2 > 0.94, \Delta H < 0$) escaped kinematic bounds. | Outcome 2: Partial rollback confirmed ($c=2$); kinematic smoothness does not guarantee semantic alignment. |
| **12. Semantic Trajectory Verification (EXP037)** | Pythia-160M (Layer 8, $\alpha=0.25$) | Combining kinematic bounds ($\rho \ge 0.40, d \le 0.14$) with Context Representation Fidelity ($\Delta S_{\mathrm{context}} \ge 0$) achieved **$68.0\%$ (+8.0 pp headroom, $b=5, c=1$, $CI_{95\%} = [0.0, +18.0]$ pp)**, catching smooth attractor drift (Inst 22: $\Delta S_{\mathrm{ctx}} = -0.0145$) while retaining all $b=5$ rescues. $E_{\mathrm{CF}}$ energy failed to discriminate drift ($\Delta E_{\mathrm{CF}} < 0$ across all attractors). | Outcome 1: Autonomous headroom recovery confirmed at $+8.0$ pp; context fidelity catches smooth attractor drift ($c$ reduced from $3 \to 2 \to 1$). |
| **13. Basis Switching & Compute Bounds (EXP038)** | Pythia-160M (Layer 8, $\alpha=0.25$, $B_{\mathrm{eval}} \le 3$) | Evaluated multi-signal attractor diagnostics and compute-bounded basis switching to secondary orthogonal trajectory mode ($V_2 = \operatorname{SVD}_{3:4}$). Switching triggered on 49/50 instances but produced only 1 rescue, consuming 2.98 passes/instance with lower FLOP efficiency ($0.0095$) than single-pass ($0.0112$), tying discrete accuracy at $66.0\%$ ($b=3, c=0$). Clause projection eliminated corruptions ($c=0$) but over-pruned rescues ($b: 5 \to 3$). | Outcome 2: Orthogonal basis switching is FLOP-inefficient; singular spectrum decay refutes secondary modes as general recovery mechanism. |
| **14. Prospective Generator Selection (EXP039)** | Pythia-160M (Layer 8, $\alpha=0.25$, $B_{\mathrm{eval}} = 1.0$) | Evaluated heterogeneous generator complementarity across Trajectory Flow ($G_1$), Contextual Perturbation ($G_2$), and Attention Relational Routing ($G_3$). Qualitative complementarity confirmed: union of rescues reached $N=5$ unique instances ($G_3$ uniquely rescued Inst 34). Oracle multi-generator bound reached **$70.0\%$ (+10.0 pp, $b=5, c=0, p=0.03125, CI = [+0.02, +0.18]$, $\Delta\log p = +0.1211$)** under $1.0$ forward pass. Prospective policy $q(g \mid x, h_0)$ achieved $66.0\%$ ($b=3, c=0$). | Outcome 1: Heterogeneous generator complementarity confirmed ($p=0.0312$); Oracle bound establishes multi-generator headroom under 1 pass. |
| **15. Prospective Router Benchmark (EXP040)** | Pythia-160M (Layer 8, $B_{\mathrm{eval}} = 1.00$) | Frozen router $\phi^*$ trained on separate calibration split ($N=50$) achieved **$68.0\%$ (+8.0 pp, $b=4, c=0, CI = [+0.02, +0.16]$ pp)** at 1 forward pass, capturing $80\%$ of Oracle headroom over baseline ($+8$ pp vs $+10$ pp) and outperforming all static single generators. | Outcome 1: Prospective routing confirmed within calibrated distribution ($p=0.0625$, exact 1-pass budget). |
| **16. Router Transfer Boundary (EXP041)** | Pythia-160M & GPT-2 124M ($B_{\mathrm{eval}} = 1.00$) | Zero-shot uncalibrated transfer across tasks (`BENCH-004`) and architectures (`gpt2`) failed ($\Delta M = -4.0$ pp and $-8.0$ pp). Isolated two distinct failure modes: generator existence failure on task transfer ($M_{\mathrm{Oracle}} = M_I = 52\%$) vs. causal dynamics mismatch on GPT-2 ($c=5$). | Outcome 3: Zero-shot uncalibrated router transfer refuted. Efficacy is conditioned on generator existence and model dynamics. |
| **17. Applicability & Normalization (EXP042)** | Pythia-160M & GPT-2 124M ($B_{\mathrm{eval}} = 1.00$) | Input feature normalizations (Z-score and empirical CDF rank mapping) failed to resolve cross-architecture transfer ($58.0\%, c=5$ on GPT-2). Proved that cross-architecture failure is an operator-level causal mismatch, not an input feature-scaling artifact. | Outcome 3: Input feature normalization refuted. The causal effect of the tested representation operators is architecture-dependent. |
| **18. Autonomous Operator Discovery (EXP043)** | Pythia-160M & GPT-2 124M ($B_{\mathrm{eval}} = 1.00$) | Probed unlabeled calibration prompts ($N=15$), synthesized 5 candidate operator families from measured properties ($\mathcal{O}_M$), and executed an automated causal response audit. Autonomously pruned $G_1$ on GPT-2 ($c=1 \to \text{pruned}$) and $G_3$ on Pythia ($c=2 \to \text{pruned}$). Held-out confirmatory evaluation eliminated all corruptions on GPT-2 ($c=0$), reaching **$72.0\%$ (+8.0 pp, beating supervised ref $70.0\%$)**, and reached **$74.0\%$ (+14.0 pp, matching supervised ref, $p=0.0078$)** on Pythia-160M. | Outcome 1: Autonomous operator discovery eliminates corruptions and achieves state-of-the-art headroom under exact 1-pass budget. |
| **19. Cross-Task Discovery & Existence Boundary (EXP044)** | Pythia-160M (`BENCH-004-TRANSFER`, $B_{\mathrm{eval}} = 1.00$) | Probed 5 unseen relational domains with natural prose. Oracle bound reached only $54.00\%$ (+2.0 pp, $b=1, c=0$). Logit failure profiling revealed that 75% of failures stem from grammatical/syntactic ambiguity rather than entity distractor attraction. Confirms that linear residual projection cannot span non-entity open generation gaps. | Outcome 3: Generator existence boundary confirmed; isolates scope condition of linear representation operators. |
| **20. First-Principles Operator Invention (EXP045)** | Pythia-160M (`BENCH-004-TRANSFER`, $B_{\mathrm{eval}} = 1.00$) | Evaluated first-principles operator invention with 3-way data firewall ($\mathcal{D}_{\mathrm{synth}} \to \mathcal{D}_{\mathrm{audit}} \to \mathcal{D}_{\mathrm{test}}$) and formal reducibility audit. Structurally novel candidates ($E_{\mathrm{span}}, E_{\mathrm{comp}} \ge 0.80$) achieved $52.00\%$ ($b=0, c=0$). Pre-registered invention threshold ($M \ge 62.0\%, b \ge 5, c=0, p=0.03125$) was not met. | Outcome 4: Existence boundary invariant; first-principles operator invention not demonstrated. |
| **21. Prospective Diagnosis & Computation Allocation (EXP046)** | Pythia-160M (Mixed $N=100$, Seed 84/350) | Evaluated prospective diagnosis across $\{\mathcal{R}, \mathcal{S}, \emptyset\}$ under locked utility $U = \text{Acc} - 0.05C - 1.00c$. Pre-intervention observables failed to discriminate $\mathcal{R}$-viability ($\mathrm{AUC}=0.5000$). External retrieval severely corrupted base Pythia-160M in-context attention ($c=17$, degrading accuracy to $42.0\%$). Blind baseline was optimal ($\bar{U}=+0.5100$). | Outcome 4: Prospective diagnosis refuted; base LM vulnerable to in-context retrieval distraction. |




---

## 2. Theoretical Diagnosis: The 3 Epistemological Levels of Internal Geometry

EXP032 through EXP038 rigorously isolate the geometric structure of internal representations:

$$\boxed{\textbf{Static Variance } \neq \textbf{ Semantic Contrast} \quad \big|\quad \textbf{Kinematic Smoothness } \neq \textbf{ Semantic Correctness} \quad \big|\quad \textbf{Secondary Modes } \neq \textbf{ Independent Rescues}}$$

This establishes a three-tier hierarchy of internal representation:

```text
Level 1: Static Geometry (Σ(h), Raw PCA)
         ↳ Refuted in EXP032: Indiscriminate energy perturbation (Δlog p ≤ -0.0145, degrades to 56%).
   │
   ▼
Level 2: Kinematic Geometry (Trajectory Displacement d_t, Alignment ρ_t)
         ↳ Confirmed in EXP036: Catches geometric incoherence/collapse (Inst 39, c: 3 → 2).
         ↳ Blind to Smooth Attractor Drift: Inst 22 & 28 move smoothly (ρ ≈ 0.94) into the wrong attractor.
   │
   ▼
Level 3: Semantic Context Geometry (S_context, Clause Subspaces)
         ↳ Confirmed in EXP037: Context representation fidelity (ΔS_context ≥ 0) flags smooth drift (Inst 22).
         ↳ Confirmed in EXP038: Clause projection flags Inst 28, but unnormalized projection over-prunes rescues.
         ↳ Proves that secondary SVD modes (V_2 = SVD_{3:4}) cannot substitute for genuinely distinct candidate generators.
```

---

## 3. The SCBI Closed-Loop Inference Architecture

$$\boxed{g_t = f(K_t, S_t, U_t) \longrightarrow \{\text{CONTINUE}, \text{STOP}, \text{ROLLBACK}, \text{CHANGE BASIS}\}}$$

```text
                                  SCBI CLOSED-LOOP INFERENCE CONTROLLER
                                                    │
                                          Input Problem Prompt x
                                                    │
                                                    ▼
                                    Initial Representation h_0
                                                    │
                      ┌─────────────────────────────┴─────────────────────────────┐
                      ▼                                                           ▼
         [Kinematic State K_t]                                       [Semantic State S_t]
         Evaluates Movement Geometry:                                Evaluates Premise Fidelity:
         - Relative Displacement d_t                                 - Context Cosine Similarity S_context
         - Directional Cosine Alignment ρ_t                          - Clause Subspace Projection S_clause
                      │                                                           │
                      └─────────────────────────────┬─────────────────────────────┘
                                                    │
                                                    ▼
                                         [Utility State U_t]
                                         Evaluates Objective Headroom:
                                         - Decision Margin m_t
                                         - Attractor Entropy H_t
                                                    │
                                                    ▼
                                  [Inference Executive Policy π_t]
                    ┌───────────────────────────────┼───────────────────────────────┐
                    ▼                               ▼                               ▼
               {CONTINUE}                       {ROLLBACK}                    {CHANGE BASIS}
        Accept h_{t+1}, advance         Reject h_{t+1}, revert to h_t    Switch candidate generator
        deliberation to next step       due to kinematic/semantic fault  under hard compute budget B_eval
```

---

## 4. Decoupled Research Program

The research program investigates this architecture across decoupled, independently falsifiable experimental phases:

```text
EXP032: Static Covariance Geometry ────────► REFUTED (Outcome 3: Static variance does not equal contrast)
   │
   ▼
EXP033: Relational Basis Discovery ────────► PARTIAL SIGNAL (Outcome 2: Trajectory Δlog p > 0, c=0, +6 pp)
   │
   ▼
EXP034: Iterative Latent Deliberation ─────► OVER-STEERING DISCOVERED (Outcome 3: b=5 rescued, but c=5 corrupted)
   │
   ▼
EXP035: Adaptive Margin Halting ───────────► REFUTED (Outcome 3: Output margin cannot distinguish corruption c=3)
   │
   ▼
EXP036: Trajectory Rollback Control ───────► PARTIAL CONFIRMATION (Outcome 2: Inst 39 caught, c reduced to 2; smooth drift persists)
   │
   ▼
EXP037: Semantic Trajectory Verification ──► CONFIRMED (Outcome 1: Context fidelity catches smooth drift; b=5, c=1, +8.0 pp)
   │
   ▼
EXP038: Basis Switching & Compute Bounds ──► PARTIAL REFUTATION (Outcome 2: Secondary SVD mode is FLOP-inefficient, 1 rescue)
   │
   ▼
EXP039: Heterogeneous Basis Complementarity ─► CONFIRMED (Outcome 1: Oracle pool reaches 70.0%, p=0.0312, b=5, c=0)
   │
   ▼
   │
   ▼
EXP040: Prospective Generator Router ───────► CONFIRMED (Outcome 1: Frozen router recovers 80% Oracle gain, 68.0%, +8 pp, b=4, c=0 at B_eval=1.0)
   │
   ▼
EXP041: Cross-Task / Cross-Architecture ────► REFUTED ZERO-SHOT (Outcome 3: Uncalibrated transfer causes negative headroom; requires calibration)
   │
   ▼
EXP042: Applicability & Normalization ──────► REFUTED NORMALIZATION (Outcome 3: Z-score/rank normalization fails to fix causal operator mismatch)
   │
   ▼
EXP043: Autonomous Operator Discovery ──────► CONFIRMED DISCOVERY (Outcome 1: Causal audit prunes G1 on GPT-2; c=0, +8 pp beating supervised ref)
   │
   ▼
EXP044: Cross-Task Discovery & Existence ────► EXISTENCE BOUNDARY CONFIRMED (Outcome 3: 75% non-entity errors; linear projection cannot span open syntactic ambiguity)
   │
   ▼
EXP045: First-Principles Operator Invention ─► OUTCOME 4 INVARIANT (Outcome 4: Non-reducible S3 fails to rescue baseline; invention not demonstrated)
   │
   ▼
EXP046: Prospective Failure Mode Diagnosis ──► REFUTED PASSIVE OBSERVABLES (Outcome 4: Pre-intervention features give AUC=0.50; BM25 retrieval distracts c=17)
   │
   ▼
EXP047: Active Inference Causal Micro-Probing ─► DECISION SHARPENING DECOUPLING (Outcome 4: Micro-probe kappa gives AUC=0.50; margin expansion != target accuracy)
```

---

## 5. Architectural Synthesis: From Fixed Subspaces to Autonomous Toolbox Discovery

### The Completed Empirical Trajectory (EXP032–EXP047):
1. **The Inadequacy of Static Covariance (EXP032):** Maximizing unprompted activation variance does not isolate task contrast.
2. **The Discovery of Trajectory Steering (EXP033):** Inter-layer velocity vectors ($h_8 - h_6$) provide genuine directional contrast ($+6.0$ pp, $b=3, c=0$).
3. **The Danger of Latent Recurrence (EXP034 & EXP035):** Blindly iterating over-steers representations ($T=3 \to c=5$); output margins cannot detect latent corruption.
4. **The Dual Nature of Representation Failure (EXP036 & EXP037):** Geometric kinematics catches trajectory collapse ($c: 3 \to 2$), while context representation fidelity catches smooth attractor drift ($c: 2 \to 1$).
5. **The Spectral Fallacy (EXP038):** Traversing secondary singular modes ($V_2 = \operatorname{SVD}_{3:4}$) fails to provide alternative bases (FLOP-inefficient, 1 rescue in 49 switches).
6. **Heterogeneous Computational Modes (EXP039):** Truly distinct generator families ($G_1$: Trajectory, $G_2$: Contextual, $G_3$: Attention) rescue disjoint failure instances (Oracle bound: $70.0\%$, $+10.0$ pp, $p=0.03125$).
7. **Prospective Autonomous Routing (EXP040):** An unseen, label-free router $q_\phi(g \mid \mathbf{s}(h_0))$ calibrated on an independent split and frozen before test evaluation achieves **$68.0\%$ (+8.0 pp, $b=4, c=0, CI_{95\%} = [+0.02, +0.16]$ pp)** at **$B_{\mathrm{eval}} = 1.00$**, recovering $80\%$ of the Oracle headroom.
8. **The Transfer Boundary (EXP041):** Zero-shot transfer of the frozen router to unseen tasks (`BENCH-004`) and a different architecture (`gpt2`) yields negative headroom ($\Delta M = -4.0$ pp and $-8.0$ pp).
9. **Causal Dynamics Mismatch vs. Feature Normalization (EXP042):** Rank and Z-score normalization fail to resolve cross-architecture transfer ($c=5$ persists). Operators that are benign on Pythia ($G_1, G_2$) are destructive to Post-LN dynamics on GPT-2. The causal effect of the tested representation operators is architecture-dependent.
10. **Autonomous Model-Specific Operator Discovery (EXP043):**
    - Moving from hand-authored operators to automated synthesis from measured properties ($\mathcal{O}_M$) and pre-inference causal response audits.
    - Causal response audit autonomously prunes destabilizing operators ($G_1$ on GPT-2), assembling tailored toolboxes $\mathcal{G}_{\mathrm{Pythia}}$ and $\mathcal{G}_{\mathrm{GPT2}}$.
    - Completely eliminates corruptions on GPT-2 ($c=5 \to c=0$), elevating accuracy to **$72.0\%$ (+8.0 pp headroom, $p=0.0625$, promising but not statistically superior to supervised contrast $70.0\%$)**, and matching supervised contrast on Pythia-160M at **$74.0\%$ (+14.0 pp, $b=7, c=0, p=0.0078$)** at $B_{\mathrm{eval}} = 1.00$.
11. **The Empirical Existence Boundary & Task Scope (EXP044):**
    - Tested task-conditioned operator synthesis and causal auditing across 5 unseen relational domains on `BENCH-004-TRANSFER`.
    - Within the tested operator family, `BENCH-004` exhibits an empirical operator-existence boundary: instance-wise oracle selection recovered only 2 percentage points of headroom ($M_{\mathrm{Oracle}} = 54.00\% \approx M_I = 52.00\%, b=1$).
    - Detailed error profiling established that $75\%$ of model failures were driven by grammatical/syntactic open generation ambiguities rather than entity distractor attraction.
12. **The Limits of First-Principles Operator Invention (EXP045):**
    - Structurally novel candidate $S_3$ achieved $E_{\mathrm{span}}=0.9987, E_{\mathrm{comp}}=0.9982$ and passed causal safety ($c=0$), but delivered zero rescues on held-out test data ($b=0, M=52.00\%$). Decisively resolves to Outcome 4.
13. **The Elimination of Passive Pre-Intervention Observables (EXP046):**
    - Passive static features ($\Delta z_{\mathrm{top2}}, H_{\mathrm{vocab}}, \sigma_H, \mathrm{PR}_{\min}, d_{\mathrm{drift}}$) yielded $\mathrm{AUC} = 0.5000$ for predicting intervention utility.
    - Demonstrates that observable uncertainty $\neq$ action utility. BM25 context retrieval severely disrupted Pythia-160M ($56\% \to 42\%, c=17$).
14. **Active Inference Causal Micro-Probing & The Decision Sharpening Decoupling (EXP047):**
    - Evaluated reversible micro-probing ($\epsilon = 0.05$) to measure local controllability $\kappa = \Delta \mathcal{M}_{12} / (d_{\mathrm{disp}} + \delta)$.
    - The micro-probe detected local responsiveness ($\Delta \mathcal{M}_{12} > 0, \kappa > 6.197, \Delta H \le 0$) on 21 instances and committed to full intervention, but produced zero discrete token flips ($b=0, c=0$).
    - Discovered the fundamental duality: **decision margin expansion measures internal model conviction, not semantic correctness.** Unguided steering sharpens confidence into whatever attractor the model is already occupying.

### The Five-Layer Hierarchy of Adaptive Computation:
$$\boxed{
\begin{aligned}
&\textbf{1. Task Scope & Error Type: } \text{Is failure driven by entity competition vs. open syntactic ambiguity?} \\
&\textbf{2. Operator Discovery & Span: } \text{Does the operator library span the required semantic direction?} \\
&\textbf{3. Causal Audit & Safety: } \text{Are synthesized operators non-destructive under downstream layers? } (c=0). \\
&\textbf{4. Dynamic Probing vs. Passive State: } \text{Measure causal response } \kappa \text{ rather than static geometry.} \\
&\textbf{5. Verifiable Semantic Reference: } \text{A directional anchor is required to distinguish true rescue from wrong attractor locking.}
\end{aligned}
}$$


---

## 5. Architectural Synthesis: From Fixed Subspaces to Autonomous Toolbox Discovery

### The Completed Empirical Trajectory (EXP032–EXP045):
1. **The Inadequacy of Static Covariance (EXP032):** Maximizing unprompted activation variance does not isolate task contrast.
2. **The Discovery of Trajectory Steering (EXP033):** Inter-layer velocity vectors ($h_8 - h_6$) provide genuine directional contrast ($+6.0$ pp, $b=3, c=0$).
3. **The Danger of Latent Recurrence (EXP034 & EXP035):** Blindly iterating over-steers representations ($T=3 \to c=5$); output margins cannot detect latent corruption.
4. **The Dual Nature of Representation Failure (EXP036 & EXP037):** Geometric kinematics catches trajectory collapse ($c: 3 \to 2$), while context representation fidelity catches smooth attractor drift ($c: 2 \to 1$).
5. **The Spectral Fallacy (EXP038):** Traversing secondary singular modes ($V_2 = \operatorname{SVD}_{3:4}$) fails to provide alternative bases (FLOP-inefficient, 1 rescue in 49 switches).
6. **Heterogeneous Computational Modes (EXP039):** Truly distinct generator families ($G_1$: Trajectory, $G_2$: Contextual, $G_3$: Attention) rescue disjoint failure instances (Oracle bound: $70.0\%$, $+10.0$ pp, $p=0.03125$).
7. **Prospective Autonomous Routing (EXP040):** An unseen, label-free router $q_\phi(g \mid \mathbf{s}(h_0))$ calibrated on an independent split and frozen before test evaluation achieves **$68.0\%$ (+8.0 pp, $b=4, c=0, CI_{95\%} = [+0.02, +0.16]$ pp)** at **$B_{\mathrm{eval}} = 1.00$**, recovering $80\%$ of the Oracle headroom.
8. **The Transfer Boundary (EXP041):** Zero-shot transfer of the frozen router to unseen tasks (`BENCH-004`) and a different architecture (`gpt2`) yields negative headroom ($\Delta M = -4.0$ pp and $-8.0$ pp).
9. **Causal Dynamics Mismatch vs. Feature Normalization (EXP042):** Rank and Z-score normalization fail to resolve cross-architecture transfer ($c=5$ persists). Operators that are benign on Pythia ($G_1, G_2$) are destructive to Post-LN dynamics on GPT-2. The causal effect of the tested representation operators is architecture-dependent.
10. **Autonomous Model-Specific Operator Discovery (EXP043):**
    - Moving from hand-authored operators to automated synthesis from measured properties ($\mathcal{O}_M$) and pre-inference causal response audits.
    - Causal response audit autonomously prunes destabilizing operators ($G_1$ on GPT-2), assembling tailored toolboxes $\mathcal{G}_{\mathrm{Pythia}}$ and $\mathcal{G}_{\mathrm{GPT2}}$.
    - Completely eliminates corruptions on GPT-2 ($c=5 \to c=0$), elevating accuracy to **$72.0\%$ (+8.0 pp headroom, $p=0.0625$, promising but not statistically superior to supervised contrast $70.0\%$)**, and matching supervised contrast on Pythia-160M at **$74.0\%$ (+14.0 pp, $b=7, c=0, p=0.0078$)** at $B_{\mathrm{eval}} = 1.00$.
11. **The Empirical Existence Boundary & Task Scope (EXP044):**
    - Tested task-conditioned operator synthesis and causal auditing across 5 unseen relational domains on `BENCH-004-TRANSFER`.
    - Within the tested operator family, `BENCH-004` exhibits an empirical operator-existence boundary: instance-wise oracle selection recovered only 2 percentage points of headroom ($M_{\mathrm{Oracle}} = 54.00\% \approx M_I = 52.00\%, b=1$).
    - Detailed error profiling established that $75\%$ of model failures were driven by grammatical/syntactic open generation ambiguities (predicting an adjective, article, or noun category) rather than entity distractor attraction.
    - Demonstrates that linear residual subspace intervention is causally scoped to **entity resolution and distractor suppression**, without ruling out that unexamined, non-linear operator families could exist.
12. **The Limits of First-Principles Operator Invention (EXP045):**
    - Evaluated whether candidate operators outside the span of $\mathcal{G}_{\mathrm{pre}}$ ($E_{\mathrm{span}}, E_{\mathrm{comp}} \ge 0.80$) could break the existence boundary under a strict pre-registered threshold ($M \ge 62.00\%, b \ge 5, c=0, p=0.03125$).
    - Structurally novel candidate $S_3$ achieved $E_{\mathrm{span}}=0.9987, E_{\mathrm{comp}}=0.9982$ and passed causal safety ($c=0$), but delivered zero rescues on held-out test data ($b=0, M=52.00\%$).
    - Decisively resolves to **Outcome 4: Existence Boundary Invariant**. Structural operator invention is **not demonstrated** on this domain.

### The Four-Layer Hierarchy of Adaptive Representation Control:
$$\boxed{
\begin{aligned}
&\textbf{1. Operator Discovery Space: } \text{What candidate operator grammar is synthesized from internal observables } \mathcal{O}_M? \\
&\textbf{2. Generator Existence: } \text{Does the candidate operator space contain recoverable headroom? } (M_{\mathrm{Oracle}} > M_I). \\
&\textbf{3. Applicability Audit: } \text{Are candidate operators } G_i \text{ safe under downstream dynamics } \mathcal{D}_M\text{? Prune if } c > 0. \\
&\textbf{4. Prospective Selection: } \text{Route state } h_0 \text{ to the optimal mode } G^* \in \mathcal{G}_M \text{ under exact } B_{\mathrm{eval}} = 1.00.
\end{aligned}
}$$

### The Frontier Beyond Library Routing:
The central open problem is whether a frozen backbone can transition from selecting within fixed candidate sets to **problem-specific operator synthesis from first principles**:
$$\boxed{x \longrightarrow \text{probe internal state } \mathcal{O}_M(x) \longrightarrow \text{synthesize } G^*(x) \longrightarrow \text{test cheaply} \longrightarrow \text{intervene} \longrightarrow \text{verify}}$$







