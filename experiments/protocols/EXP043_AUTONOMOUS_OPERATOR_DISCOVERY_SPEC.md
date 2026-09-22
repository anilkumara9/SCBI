# EXP043: Automated Model-Specific Operator Discovery Protocol Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP043`
- **Date:** 2026-09-12
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (specifically Law 2: Never Invent Results, Law 4: Never Silently Shift Hypotheses, Law 6: Frozen Backbone, Law 7: Zero Data Leakage, Law 9: No Cherry-Picking, Law 10: Never Claim Premature Novelty, Law 13: Deterministic Reproducibility, Law 14: Challenge Rather Than Defend).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark testing whether an automated calibration protocol can probe a model's internal causal properties, synthesize candidate representation operators, audit their causal stability on unlabeled calibration data, and assemble a model-specific toolbox $\mathcal{G}_M$ that eliminates cross-architecture corruptions on GPT-2 124M while preserving capability amplification on Pythia-160M under single-pass inference ($B_{\mathrm{eval}} = 1.00$, $\Delta\theta \equiv 0$).
- **Core Scientific Question:**
  $$\boxed{\textbf{Can a model autonomously construct its own useful operator toolbox without hand-coded architectural heuristics?}}$$

---

## 2. Theoretical Motivation: Beyond Hand-Crafted Operators

EXP041 and EXP042 proved that:
1. Representation operators do not possess architecture-invariant semantics; an operator's causal effect is conditioned by the downstream residual dynamics $\mathcal{D}_M$.
2. Input feature normalization cannot fix operator-level causal mismatch; an operator that destabilizes Post-LN normalization will cause corruptions regardless of input Z-scoring or rank scaling.

The next evolutionary step of SCBI is:
$$\boxed{\text{Fixed Hand-Authored Operators} \quad \longrightarrow \quad \textbf{Autonomous Model-Specific Operator Discovery}}$$

Rather than hand-coding operators based on human architectural knowledge (e.g., *"GPT-2 is Post-LN, Pythia is Parallel Rotary"*), the discovery protocol must measure internal computational properties:
$$\mathcal{O}_M = f(\text{residual geometry}, \text{normalization sensitivity}, \text{attention entropy}, \text{trajectory stability})$$
and synthesize, audit, and filter candidate operators purely through measured empirical causal response.

---

## 3. The 4-Stage Discovery Protocol Pipeline

```text
                                  MODEL M (Frozen, Δθ = 0)
                                            │
                                            ▼
                    STAGE 1: UNLABELED CALIBRATION PROBING (N_probe = 20)
                    - Measure inter-layer norm growth ||h_{l+1}|| / ||h_l||
                    - Measure LayerNorm perturbation sensitivity
                    - Measure attention entropy and head specialization
                    - Measure trajectory flow angle and acceleration
                                            │
                                            ▼
                    STAGE 2: CANDIDATE OPERATOR SYNTHESIS
                    Synthesize 5 mathematically distinct candidate families:
                    - G_traj: Inter-layer velocity flow
                    - G_norm_contrast: Norm-compensated counterfactual
                    - G_attn_rel: Head-contrast weighted projection
                    - G_ortho_diff: Early-stage orthogonalized flow
                    - G_token_gate: Feature-norm selective hard gate
                                            │
                                            ▼
                    STAGE 3: CAUSAL RESPONSE AUDIT (N_audit = 15)
                    Evaluate each candidate operator for:
                    - Attractor Stability: Does it cause output logit collapse?
                    - Directional Gain: Does it shift probability towards target?
                    - Filtering Rule: Retain in G_M iff c_audit == 0 and Δlog p_audit > 0
                                            │
                                            ▼
                    STAGE 4: ASSEMBLE MODEL TOOLBOX G_M & RUNTIME CONTROL
                    Evaluate locked G_M on Held-Out Confirmatory Split (N=50, B_eval=1.00)
```

---

## 4. Evaluated Backbones & Confirmatory Test Splits

1. **Architecture A (`EleutherAI/pythia-160m`):**
   - Calibration Split: `BENCH-002-NL` ($N=20$, Seed 123, unlabeled) for probing & causal audit.
   - Held-Out Confirmatory Split: `BENCH-002-NL` ($N=50$, Seed 84).
2. **Architecture B (`gpt2`, 124M):**
   - Calibration Split: `BENCH-002-NL` ($N=20$, Seed 123, unlabeled) for probing & causal audit.
   - Held-Out Confirmatory Split: `BENCH-002-NL` ($N=50$, Seed 84).

---

## 5. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Autonomous Corruption Elimination on GPT-2 ($H_{\mathrm{gpt2\_audit}}$)
$$\text{On GPT-2}, \quad c(\mathcal{G}_{\mathrm{discovered}}) \le 1 \quad \text{and} \quad M(\mathcal{G}_{\mathrm{discovered}}) \ge 0.6400$$
- **Prediction:** The causal audit detects that un-normalized trajectory flow ($G_{\mathrm{traj}}$) causes residual collapse on GPT-2, pruning it from $\mathcal{G}_{\mathrm{GPT2}}$ and retaining only stable operators (e.g., norm-compensated contrast or attention routing). This eliminates the $c=5$ corruptions observed in EXP041/EXP042, bringing accuracy to $\ge 64.0\%$ (baseline) or achieving positive headroom ($68.0\%$).
- **Falsification Criterion:** If the autonomously discovered toolbox on GPT-2 still produces $\ge 4$ corruptions or drops accuracy below $60.0\%$, the hypothesis that automated causal auditing builds a safe operator library is rejected.

### Hypothesis 2: Headroom Preservation on Pythia-160M ($H_{\mathrm{pythia\_retain}}$)
$$\text{On Pythia-160M}, \quad M(\mathcal{G}_{\mathrm{discovered}}) \ge 0.6600 \quad \text{and} \quad c = 0$$
- **Prediction:** On Pythia-160M, the causal audit confirms that trajectory flow and attention routing are safe ($c_{\mathrm{audit}} = 0$), retaining them into $\mathcal{G}_{\mathrm{Pythia}}$ and replicating positive headroom without human intervention.
- **Falsification Criterion:** If the autonomous protocol discards viable operators on Pythia and drops accuracy below $62.0\%$, the discovery mechanism is falsified.

---

## 6. Reproducibility & Ledger Output
- Parameter hashes verified invariant for Pythia-160M and GPT-2 124M ($\Delta\theta \equiv 0$).
- Zero outcome labels exposed during Stage 1 probing and Stage 2 synthesis.
- Exactly $1.00$ forward pass per instance during final evaluation ($B_{\mathrm{eval}} = 1.00$).
- Output data saved to `experiments/runs/EXP043_operator_discovery/exp043_operator_discovery_results.json`.
