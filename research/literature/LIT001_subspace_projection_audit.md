# LIT001: Literature Audit & Equivalence Analysis — Subspace Projection & Activation Steering

**Audit ID:** LIT001  
**Target Mechanism:** Inference-Time Multi-Candidate Subspace Projection with Unsupervised Self-Consistency  
**Authoring Agent:** [`literature-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/literature-agent.md)  
**Adversarial Auditor:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rule:** [`.agents/rules/01-literature.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/01-literature.md)  
**Date:** 2026-09-11  

---

## 1. Literature Screening Record

| Field | Details |
| :--- | :--- |
| **Paper 1** | *Representation Engineering: A Top-Down Approach to AI Transparency* (Zou et al., 2023) |
| **Venue / URL** | arXiv:2310.01405 |
| **Method Mechanism** | Reads activation differences on contrastive prompt pairs offline; applies fixed steering vector $h \leftarrow h + \alpha v$ during inference. |
| **Backbone Frozen?** | **Yes** ($\Delta\theta = 0$). |
| **Dynamic per Instance?** | **No.** The steering vector $v$ is computed globally offline across a training set. |
| **Objective Evaluator $\mathcal{E}$?** | **None.** Applied statically without internal consistency evaluation. |
| **Equivalence to SCBI:** | `[DISTINCT]` — RepE uses static, globally pre-computed vectors. SCBI invents candidate coordinate frames $B_{t,k}$ dynamically per instance $x$ and evaluates them via $\mathcal{E}$. |

---

| Field | Details |
| :--- | :--- |
| **Paper 2** | *Learning to (Learn at Test Time): RNNs with Expressive Hidden States* (Sun et al., 2024 / TTT) |
| **Venue / URL** | arXiv:2407.04620 |
| **Method Mechanism** | Formulates test-time training by taking gradient steps on model parameters/weights in an inner loop using a self-supervised reconstruction loss. |
| **Backbone Frozen?** | **No.** TTT explicitly updates hidden state weights $W_K$ at test time ($\Delta\theta \ne 0$). |
| **Dynamic per Instance?** | **Yes.** |
| **Equivalence to SCBI:** | `[DIFFERENT_INVARIANT: PARAMETER_UPDATE]` — Violates the core SCBI invariant $\Delta\theta_t = 0$. SCBI proves or disproves whether representation adaptation alone suffices without parameter training. |

---

| Field | Details |
| :--- | :--- |
| **Paper 3** | *Activation Addition: Steering Language Models Without Optimization* (Turner et al., 2023) |
| **Venue / URL** | arXiv:2308.10248 |
| **Method Mechanism** | Injects an activation vector $h + (v_{\text{pos}} - v_{\text{neg}})$ into the forward pass. |
| **Backbone Frozen?** | **Yes** ($\Delta\theta = 0$). |
| **Dynamic per Instance?** | **No.** Fixed steering vector derived offline. |
| **Equivalence to SCBI:** | `[DISTINCT]` — SCBI constructs candidate projection bases $P_k = I - V_k V_k^\top$ dynamically per test instance and selects them via an unsupervised self-consistency objective $\mathcal{E}$. |

---

## 2. Formal Equivalence Matrix

| Method | Backbone Frozen? ($\Delta\theta=0$) | Dynamic Basis per Instance? | Transient State Wiped? | Internal Self-Consistency Objective? | Relationship to SCBI |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Tent (Wang et al. 2021)** | No (updates BN) | Yes | No (state drifts) | Entropy minimization | `[DISTINCT]` |
| **TTT (Sun et al. 2024)** | No (updates $W_K$) | Yes | Yes | Reconstruction loss | `[DISTINCT]` |
| **RepE (Zou et al. 2023)** | Yes | No (static offline) | No | None | `[DISTINCT]` |
| **ActAdd (Turner et al. 2023)** | Yes | No (static offline) | No | None | `[DISTINCT]` |
| **Self-Consistency (Wang et al. 2022)** | Yes | No (token-level) | Yes | Token majority voting | `[ORTHOGONAL]` (Compute baseline) |
| **SCBI (Formulation D+C)** | **Yes** | **Yes** | **Yes** | **$\mathcal{L}_{\text{cycle}} + \lambda \mathcal{H}$** | **Target Research Subject** |

---

## 3. Formulated Research Gap

> *While prior representation engineering methods rely on globally pre-computed static vectors, and test-time training methods rely on gradient updates to model weights ($\Delta\theta \ne 0$), the mathematical and empirical viability of dynamically constructing, self-evaluating, and selecting temporary coordinate frames in internal activation space under a strictly frozen backbone ($\Delta\theta = 0$) remains uncharacterized in machine learning literature.*
