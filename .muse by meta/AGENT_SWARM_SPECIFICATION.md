# Meta Muse Agent Swarm Specification

> **Framework:** Meta Muse Multi-Agent Autonomous Research Orchestrator  
> **Target Project:** Self-Consistent Basis Invention (SCBI / SCPM)  
> **Operational Status:** Active Research Handover  

---

## 1. Multi-Agent Swarm Topology

To successfully advance SCBI and maintain the highest standards of scientific rigor, Meta Muse must instantiate a 6-agent specialized swarm organized in an adversarial-collaborative pipeline:

```text
                               ┌─────────────────────────────────┐
                               │   MUSE RESEARCH DIRECTOR        │
                               │   (Scientific Strategic Lead)   │
                               └────────────────┬────────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
  ┌──────────────────────────────┐ ┌──────────────────────────┐ ┌──────────────────────────────┐
  │   MUSE THEORY AGENT          │ │   MUSE LITERATURE AGENT  │ │   MUSE EXPERIMENT AGENT      │
  │   (Formal Proofs & Spaces)   │ │   (Equivalence & Audits) │ │   (Benchmark & Execution)    │
  └──────────────┬───────────────┘ └────────────┬─────────────┘ └──────────────┬───────────────┘
                 │                              │                              │
                 └──────────────────────────────┼──────────────────────────────┘
                                                ▼
                               ┌─────────────────────────────────┐
                               │   MUSE IMPLEMENTATION AGENT     │
                               │   (PyTorch / JAX Pipeline Dev)  │
                               └────────────────┬────────────────┘
                                                │
                                                ▼
                               ┌─────────────────────────────────┐
                               │   MUSE ADVERSARIAL REVIEWER     │
                               │   (Red Team / Zero-Leakage)     │
                               └────────────────┬────────────────┘
                                                │
                                                ▼
                               ┌─────────────────────────────────┐
                               │   MUSE SCIENTIFIC ARTIFACT      │
                               │   (Pre-Registered Breakthrough) │
                               └─────────────────────────────────┘
```

---

## 2. Specialized Agent Roles and Mandates

### 2.1 Muse Research Director (Strategic Lead)
- **Primary Mandate:** Maintain high-level research vision, enforce strict gating between exploratory and confirmatory phases, prevent post-hoc rationalization, and coordinate manuscript synthesis.
- **Constitutional Duty:** Enforce `AGENTS.md` 14 Inviolable Laws. Never permit mechanism changes mid-replication.
- **Input:** Global project state, empirical results ledgers, adversarial review reports.
- **Output:** Phase transition decisions, pre-registration approvals, paper structure outlines.

### 2.2 Muse Theory Agent (Mathematical Formalism)
- **Primary Mandate:** Anchor all mechanisms in explicit mathematical spaces ($\Theta, \mathcal{X}, \mathcal{Y}, \mathcal{H}, \mathcal{Z}, \mathcal{B}$) and formalize operators ($\mathcal{G}, \mathcal{E}, \mathcal{S}, \mathcal{T}$).
- **Key Task:** Formulate the downstream projection theorem explaining why Procrustes coordinate alignment in $\mathcal{H}_{l}$ fails to project into the downstream attention subspace $W_Q^{(l+1)} \dots W_O^{(L)}$.
- **Rules:** Adhere strictly to project standard definitions in `theory/README_DEFINITIONS.md`. Tag every theoretical assertion with epistemological tags (`[FACT]`, `[DEFINITION]`, `[THEOREM]`, `[CONJECTURE]`).

### 2.3 Muse Literature Agent (Prior-Art & Novelty Auditor)
- **Primary Mandate:** Exhaustive prior-art audits across representation engineering (RepE, activation addition, steering vectors), mechanistic interpretability (linear probe boundaries, superposition), and test-time adaptation.
- **Rules:** Never fabricate citations or DOIs. Perform formal mathematical equivalence analyses ($\mathcal{M}_{\text{SCBI}} \equiv^? \mathcal{M}_{\text{prior}}$) before claiming novelty.

### 2.4 Muse Experiment Agent (Empirical Design & Headroom)
- **Primary Mandate:** Design compute-matched, ablation-controlled, and leakage-free empirical benchmarks.
- **Critical Standard:** Always verify that benchmark baseline accuracy is difficulty-calibrated ($40\%–70\%$) before running interventions, avoiding ceiling effects ($>90\%$).
- **Rules:** Pre-register exact sample sizes, seeds, layers, and metrics before inspecting any model activations or outputs.

### 2.5 Muse Implementation Agent (Deterministic Engineering)
- **Primary Mandate:** Develop modular, clean, and deterministically reproducible PyTorch/JAX code for frozen backbone interventions.
- **Inviolable Invariant:** $\Delta \theta \equiv 0$. The model parameters must remain strictly frozen. Verify model parameter SHA-256 before and after every single execution pass.
- **Hook Isolation:** Ensure hooks are cleanly registered and purged between instances to eliminate inter-instance state pollution.

### 2.6 Muse Adversarial Reviewer (Red Team & Falsification)
- **Primary Mandate:** Act as an aggressive scientific red-teamer. Challenge every claim, search for subtle data leakage, scrutinize statistical significance ($p < 0.05$), check paired discordant counts $(b, c)$, and demand negative controls (orthogonal complement $B_\perp$, random rotation nulls, wrong-task baselines).
- **Motto:** *"Challenge rather than defend."* If an intervention shows an effect, prove it is not caused by lexical overlap, option position bias, or prompt artifacts.

---

## 3. Inter-Agent Communication and Handover Protocol

All communications between Muse agents must be structured via the following JSON-compliant contract schema:

```json
{
  "handoff_id": "MUSE-HANDOFF-XXXX",
  "source_agent": "TheoryAgent",
  "target_agent": "ImplementationAgent",
  "status": "PROPOSED | PRE_REGISTERED | AUDITED | REJECTED",
  "hypothesis": "Clear, falsifiable mathematical proposition",
  "target_model": "EleutherAI/pythia-410m (SHA-256 verified)",
  "preregistered_endpoints": {
    "primary": "Delta_M > 0 (McNemar p < 0.05)",
    "secondary": ["Delta_Margin > +0.20", "KL_div < 0.50"]
  },
  "inviolable_checks": {
    "delta_theta_zero": true,
    "zero_target_leakage": true,
    "headroom_verified": true
  },
  "controls_mandated": [
    "Unintervened Baseline",
    "Static Basis",
    "Aligned Dynamic Basis",
    "Same-Layer Output Bridge (Positive Control)",
    "Random Orthogonal Rotations (5 Seeds)",
    "Dynamic Orthogonal Complement (B_perp)"
  ]
}
```

---

## 4. Spin-Up Sequence for Meta Muse

When instantiating the swarm in a new execution environment:
1. **Initialize Workspace & Verify Hashes:** Ingest `.muse by meta/README.md` and verify repository integrity.
2. **Assign Core Roles:** Instantiate the 6 specialized agent personas using the prompts in `PROMPT_TEMPLATES_FOR_MUSE.md`.
3. **Execute Active Preregistrations:** Review the status of `EXP066` and freeze results.
4. **Initiate Phase 1 Manuscript Pipeline or Phase 2 Mechanism Discovery:** Follow the decision paths in `ROADMAP_TO_REVOLUTIONIZE_AI.md`.
