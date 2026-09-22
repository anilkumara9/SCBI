# SCBI Multi-Agent Research System Index

This document maps the foundational research files in `documentation/` to the operational rules, agents, and skills defined in `.agents/`.

---

## 1. Grounding Matrix: Documentation to Agents System

Every rule, agent, and skill in `.agents/` is directly anchored in the specifications defined in this documentation directory:

| Documentation File | Core Subject & Authority | Grounded Rules (`.agents/rules/`) | Grounded Agents (`.agents/agents/`) | Grounded Skills (`.agents/skills/`) |
| :--- | :--- | :--- | :--- | :--- |
| [`researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) | Highest-level specification, central question, 8 SCBI components, scope | [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md) | [`research-manager.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/research-manager.md)<br>[`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md) | [`hypothesis-testing`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/skills/hypothesis-testing/SKILL.md)<br>[`paper-writing`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/skills/paper-writing/SKILL.md) |
| [`theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) | Epistemological status labels, mathematical universe ($\Theta,\mathcal{X},\mathcal{Y},\mathcal{H},\mathcal{Z},\mathcal{B}$), $\Delta\theta=0$ invariant | [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md)<br>[`02-theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/02-theory.md) | [`theory-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/theory-agent.md)<br>[`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md) | [`hypothesis-testing`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/skills/hypothesis-testing/SKILL.md) |
| [`math.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/math.md) | Operational tuple $(\mathcal{G}, \mathcal{E}, \mathcal{S}, \mathcal{T})$, inference budgets, baseline comparisons, ablations | [`02-theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/02-theory.md)<br>[`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md) | [`theory-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/theory-agent.md)<br>[`experiment-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/experiment-agent.md) | [`experiment-design`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/skills/experiment-design/SKILL.md) |
| [`README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md) | Formal source of truth for terminology, fixed vs working status, change protocol | [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md)<br>[`02-theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/02-theory.md) | All Agents | All Skills |
| [`README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_LITERATURE.md) | Prior-art search protocol across 6 domains, equivalence criteria, non-novelty acceptance | [`01-literature.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/01-literature.md) | [`literature-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/literature-agent.md)<br>[`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md) | [`literature-review`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/skills/literature-review/SKILL.md) |

---

## 2. System Architecture

```text
.agents/
├── rules/
│   ├── 00-core-research.md          # Scientific integrity & status labels ([FACT], [HYPOTHESIS], etc.)
│   ├── 01-literature.md             # Prior-art cross-vocabulary audit & equivalence protocols
│   ├── 02-theory.md                 # Frozen backbone invariant (\Delta\theta=0) & decomposition rules
│   ├── 03-experiments.md            # Compute-matched baselines & 5 mandatory ablations
│   └── 04-code.md                   # Runtime guards, transient state isolation & reproducible seeds
│
├── agents/
│   ├── literature-agent.md          # Prior-art auditor, taxonomy architect, related-work investigator
│   ├── theory-agent.md              # Mathematical formalist, theoretical proof architect
│   ├── experiment-agent.md          # Benchmark architect, compute-budget enforcer
│   ├── implementation-agent.md      # Invariant enforcement engineer, pipeline implementer
│   ├── adversarial-reviewer.md      # Scientific red-teamer, rigor auditor, anti-hype guardian
│   └── research-manager.md          # Program director, orchestrator, handoff coordinator
│
└── skills/
    ├── literature-review/SKILL.md   # Systematic search, equivalence matrices, gap formulation
    ├── hypothesis-testing/SKILL.md  # Falsifiability protocols, null hypothesis setup
    ├── experiment-design/SKILL.md   # Compute-matched benchmarking, 5 mandatory ablations
    ├── statistical-analysis/SKILL.md# Multi-seed aggregation, bootstrap CIs, Wilcoxon tests, failure taxonomy
    ├── reproducibility/SKILL.md     # Deterministic seeding, parameter hash audits, environment manifests
    └── paper-writing/SKILL.md       # Scholarly drafting, anti-hype tone, status-tagged reporting
```
