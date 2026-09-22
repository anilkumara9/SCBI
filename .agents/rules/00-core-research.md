# Rule 00: Core Research Principles & Scientific Integrity

**Applies to:** All research tasks, agents, prompts, implementations, experiments, and writing across the SCBI project.  
**Foundational Documents:**
- [`documentation/researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) (Highest-level research specification, scope, and guiding principles)
- [`documentation/theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) (Mathematical research specification and epistemological labels)
- [`documentation/README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md) (Formal vocabulary source of truth)

---

## 1. Central Research Mandate

All activities in this repository exist to investigate the central research question:

> **"Can a frozen foundation model improve its inference behavior by dynamically constructing and selecting temporary representations during inference, without changing its underlying parameters?"**  
> *(Ref: [`researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) §3)*

Every hypothesis, proof, experiment, code implementation, and literature audit must directly tie back to this question or a clearly derived, mathematically bounded sub-question.

---

## 2. Epistemological Status Labels (Mandatory)

To eliminate ambiguity and prevent speculation from masquerading as fact, **every significant claim, specification line, and analytical statement must be labeled** using the standard defined in [`theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §2:

| Label | Meaning | Operational Constraint |
| :--- | :--- | :--- |
| `[FACT]` | Established mathematical or computational fact | Must cite source, standard theorem, or formal proof. |
| `[DEFINITION]` | Formal definition adopted by this project | Source of truth is [`README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md). |
| `[HYPOTHESIS]` | Empirical proposition to be tested | Must be accompanied by falsification criteria. |
| `[CONJECTURE]` | Plausible but currently unsupported proposition | Must never be treated as proven or assumed in proofs. |
| `[ASSUMPTION]` | Condition imposed for a specific analysis | Must be explicitly stated and tested for realism. |
| `[PROPOSITION]`| Statement intended for formal proof | Requires derivation steps before promotion. |
| `[THEOREM]` | Formally proven mathematical result | Proof must be verified by Theory Agent & Adversarial Reviewer. |
| `[OBSERVATION]`| Empirical result obtained experimentally | Must reference recorded seed, config, and artifact log. |
| `[INTERPRETATION]` | Researcher's interpretation of evidence | Must be clearly separated from the raw `[OBSERVATION]`. |
| `[OPEN]` | Unresolved problem or question | Must outline what data/proof would close the question. |

**Strict Prohibition:** An `[HYPOTHESIS]`, `[CONJECTURE]`, or `[INTERPRETATION]` must **never** be presented as a mathematical fact or proven truth.

---

## 3. The 8 Conceptual SCBI Invariants

Every agent and workflow must preserve the clean separation between the 8 core conceptual components established in [`researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) §2:

1. **Frozen foundation model** ($f_\theta$, parameters $\theta_0$ fixed for all $t$)
2. **Temporary inference state** ($z_t \in \mathcal{Z}$, transient within episode)
3. **Candidate representation / basis** ($B_t \in \mathcal{B}$)
4. **Candidate generation mechanism** ($\mathcal{G}: (x, z_t, \theta) \to \{B_{t,k}\}$)
5. **Candidate evaluation objective** ($\mathcal{E}: (B_{t,k}, x, z_t, \theta) \to \mathbb{R}$)
6. **Candidate selection rule** ($\mathcal{S}: (\{B_{t,k}\}, \{\mathcal{E}_k\}) \to B_t^*$)
7. **State evolution transition** ($\mathcal{T}: (z_t, B_t^*, x, \theta) \to z_{t+1}$)
8. **Final inference output** ($\hat{y} = f_\theta(x; z_T, B_T^*)$)

Agents must never blur candidate generation with candidate evaluation, nor confuse temporary inference state with model weights.

---

## 4. Scientific Honesty & Negative Results

1. **Acceptance of Non-Novelty:** A finding that SCBI is mathematically or empirically equivalent to prior art (e.g., test-time adaptation, dynamic prompting, prompt tuning, subspace projection) is a valid, high-value scientific result. Agents must never distort definitions to fabricate novelty.
2. **Acceptance of Falsification:** If controlled experiments show $\Delta M = M(\text{SCBI}) - M(\text{baseline}) \le 0$ under equalized compute/latency budgets, the hypothesis is falsified for that domain. Negative results must be reported with the same rigor and prominence as positive results.
3. **No Goalpost Moving:** Hypotheses, metrics, baselines, and evaluation protocols must be registered *before* running experiments. Adjusting benchmarks post-hoc to show an advantage is strictly forbidden.
4. **No Metric Cherry-Picking:** All standard evaluation metrics (accuracy, latency, memory footprint, FLOPs, failure rate) must be reported in full.

---

## 5. Decision & Revision Protocols

- Terminology and definitions cannot be altered ad-hoc. All changes must follow the **Definition Change Protocol** in [`README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md).
- Any deviations from the core frozen-parameter constraint must be segregated and explicitly designated as a **Variant** (e.g., `SCBI-PT`, `SCBI-Adapter`), never core SCBI.
