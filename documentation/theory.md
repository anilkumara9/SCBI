# SCBI Mathematical Research Specification

**Project:** Self-Consistent Basis Invention (SCBI)
**Document:** `theory/README.md`
**Status:** Research specification — provisional where explicitly marked
**Purpose:** Define the mathematical structure of SCBI before implementation and experimentation.

---

## 1. Purpose

This document provides the mathematical research specification for **Self-Consistent Basis Invention (SCBI)**.

It exists to ensure that:

1. the implementation follows the research hypothesis;
2. mathematical assumptions are explicit;
3. the frozen-backbone constraint is never accidentally violated;
4. temporary inference-time state is distinguished from persistent model parameters;
5. the representation mechanism is precisely specified;
6. candidate generation and evaluation are separated;
7. "self-consistency" is not left as an informal intuition;
8. experiments can be reproduced from the mathematical specification;
9. alternative formulations can be compared without silently changing SCBI;
10. Antigravity agents cannot redefine the research concept while implementing it.

This document is **not** a claim that the proposed formulation is mathematically proven, novel, or empirically effective.

---

# 2. Scientific Status

Every important statement in this document must be interpreted according to its status.

| Label              | Meaning                                         |
| ------------------ | ----------------------------------------------- |
| `[FACT]`           | Established mathematical/computational fact     |
| `[DEFINITION]`     | Definition adopted by this project              |
| `[HYPOTHESIS]`     | Empirical proposition to be tested              |
| `[CONJECTURE]`     | Plausible but currently unsupported proposition |
| `[ASSUMPTION]`     | Condition imposed for a particular analysis     |
| `[PROPOSITION]`    | Statement intended for proof                    |
| `[THEOREM]`        | Formally proven result                          |
| `[OBSERVATION]`    | Result obtained experimentally                  |
| `[INTERPRETATION]` | Researcher's interpretation of evidence         |
| `[OPEN]`           | Not yet resolved                                |

**Rule:** An `[HYPOTHESIS]`, `[CONJECTURE]`, or `[INTERPRETATION]` must never be presented as a mathematical fact.

---

# 3. Core Research Question

The central question is:

> **Can a frozen foundation model improve its inference behavior by dynamically constructing and selecting temporary representations during inference, without changing its underlying parameters?**

The word **improve** must always be operationalized using a predefined evaluation metric.

For example:

$$
\Delta M =
M(\text{SCBI}) -
M(\text{baseline})
$$

where \(M\) is a predefined evaluation metric.

An observed positive \(\Delta M\) is evidence of improvement under that evaluation protocol, not automatically evidence that the SCBI mechanism caused the improvement.

---

# 4. Core Hypothesis & Decomposition

### `[HYPOTHESIS]`

A frozen foundation model may improve inference performance when it is allowed to construct, evaluate, and temporarily use representations adapted to the current inference problem.

The hypothesis contains four essential requirements:

1. the backbone parameters remain frozen ($\Delta\theta = 0$);
2. adaptation occurs during inference;
3. adaptation operates through temporary representation/state;
4. the representation is selected using a predefined objective.

If one of these requirements is removed, the experiment may no longer constitute a core SCBI experiment.

---

## 4.1 Decomposition: Two Independent Hypotheses

Theoretical analysis and empirical results from EXP001–EXP013 demonstrate that end-to-end SCBI requires the conjunction of two mathematically independent sub-hypotheses:

### 1. Hypothesis $H_A$: Candidate Identifiability
$$\boxed{\exists E \in \mathcal{E}: \quad M_E > M_{\mathrm{Random}}}$$
*Statement:* Given an admissible candidate pool $\mathcal{G}(x)$, there exists a label-free evaluator $E$ that reliably ranks and selects superior candidates over uniform random choice.

### 2. Hypothesis $H_B$: Candidate Usefulness (Headroom)
$$\boxed{\exists P \in \mathcal{G}(x): \quad M_P > M_{\mathrm{Identity}}}$$
*Statement:* The candidate generator $\mathcal{G}(x)$ constructs an intervention pool containing at least one representation transformation that strictly outperforms the unmodified frozen backbone model.

### 3. End-to-End SCBI Requirement
$$\boxed{\exists E \in \mathcal{E}, \quad \exists P \in \mathcal{G}(x): \quad M_E > M_{\mathrm{Random}} \quad \text{and} \quad M_E > M_{\mathrm{Identity}}}$$

---

## 4.2 Epistemological Distinction: Relative Selection vs. Absolute Usefulness

An empirical finding that an evaluator solves $H_A$ does **not** imply that it satisfies end-to-end SCBI:

$$\boxed{\text{Relative Selection Ability} \neq \text{Absolute Intervention Usefulness}}$$

- If a candidate pool contains only destructive interventions (e.g., $M \in \{0.02, 0.05, 0.10, 0.16\}$ while $M_{\mathrm{Identity}} = 0.65$), an evaluator $E$ that consistently selects candidate $0.16$ rather than $0.02$ possesses **genuine relative ranking ability** ($H_A$ holds).
- However, because the entire candidate pool is destructive relative to the unmodified model, the selected intervention has **no absolute usefulness** for the foundation model ($H_B$ fails, Gate 1 fails).
- Conversely, in synthetic benchmarks (`EXP001`–`EXP012`), $H_B$ held ($M_{\mathrm{Oracle}} \approx 0.53 > M_{\mathrm{Identity}} \approx 0.28$), but all tested evaluators failed $H_A$ ($M_E \le M_{\mathrm{Random}}$).
- In pretrained language models (`EXP013`), $H_A$ held ($R_E = +64.71\%$, $M_{E_{\mathrm{CF}}} > M_{\mathrm{Random}}$), but $H_B$ failed for all-token hard rank-2 projection.

---

## 4.3 Dual-Channel Evaluation Standard

To prevent confounding task-specific discrimination with general model fluency, evaluation must decouple two distinct behavioral channels:

1. **General Language Modeling Metric ($M_{\mathrm{LM}}$):**  
   Measures greedy next-token prediction exact match across the entire vocabulary, reflecting base model fluency, syntax preservation, and unconstrained task performance.
2. **Contrastive Preference Metric ($M_{\mathrm{contrast}}$):**  
   Measures targeted distractor suppression:
   $$M_{\mathrm{contrast}} = \mathbb{I}\left[P(y_{\mathrm{target}} \mid x, P) > P(y_{\mathrm{distractor}} \mid x, P)\right]$$
   An intervention may enhance $M_{\mathrm{contrast}}$ (e.g., $0.79 \to 0.82$) while simultaneously disrupting $M_{\mathrm{LM}}$ ($0.65 \to 0.16$). They must never be conflated into a single monolithic metric.

---

## 4.4 Coordinate Transformations vs. Orthogonal Projections

Core SCBI initially framed representation adaptation as orthogonal projection onto a basis ($P^2 = P, P^\top = P$). However, continuous attenuation operators:
$$P_\alpha = I - \alpha V V^\top, \quad \alpha \in (0, 1)$$
are non-idempotent ($P_\alpha^2 \neq P_\alpha$). They are symmetric contraction operators that dynamically suppress targeted subspace energy without destroying fluency. SCBI is therefore properly generalized as:
$$\boxed{\text{Inference-time temporary coordinate transformations / representation operators, not strictly orthogonal projections.}}$$


---

# 5. Mathematical Universe

Define:

$$
\Theta
$$

as the parameter space of the foundation model.

$$
\mathcal{X}
$$

as the input space.

$$
\mathcal{Y}
$$

as the target/output space.

$$
\mathcal{H}
$$

as the representation/hidden-state space.

$$
\mathcal{Z}
$$

as the temporary inference-state space.

$$
\mathcal{B}
$$

as the space of admissible temporary representation objects.

A single inference episode operates on:

$$
x \in \mathcal{X}
$$

with optional target:

$$
y \in \mathcal{Y}.
$$

---

# 6. Frozen Foundation Model

Let the foundation model be:

$$
f_\theta:\mathcal{X}\rightarrow\mathcal{Y}
$$

where:

$$
\theta\in\Theta.
$$

The initial model parameters are:

$$
\theta_0.
$$

For core SCBI:

$$
\boxed{\theta_t=\theta_0\quad\forall t}
$$

and therefore:

$$
\boxed{\Delta\theta_t=0}.
$$

This is a mandatory constraint.

---

# 7. Frozen-Parameter Constraint

Core SCBI must not update:

* neural-network weights;
* biases;
* LoRA parameters;
* adapters;
* prompt parameters learned through optimization;
* normalization parameters;
* embeddings stored as persistent parameters;
* optimizer state that changes model behavior across episodes;
* any other persistent trainable model parameter.

Formally:

$$
\theta_{t+1}=\theta_t.
$$

Therefore:

$$
\theta_T=\theta_0.
$$

Any experiment that changes \(\theta\) must be explicitly labeled as a **variant**.

---

# 8. Model Decomposition

For mathematical analysis, decompose the model into representation and prediction functions:

$$
h_\theta(x)=f_\theta^{(h)}(x)
$$

and:

$$
\hat y=f_\theta^{(y)}(h).
$$

Thus:

$$
f_\theta(x)
=
f_\theta^{(y)}
\left(
f_\theta^{(h)}(x)
\right).
$$

The representation:

$$
h_0=h_{\theta_0}(x)
$$

is the initial model representation.

This decomposition is conceptual and may differ from the exact implementation architecture.

---

# 9. Temporary Inference State

SCBI introduces:

$$
z_t\in\mathcal{Z}.
$$

The state may contain temporary information such as:

* candidate representations;
* statistics;
* temporary transformations;
* intermediate evaluations;
* candidate scores;
* search history;
* accepted/rejected candidate information;
* temporary memory.

The state must not become persistent model parameters in the core formulation.

Initial state:

$$
z_0=I_z(x)
$$

where \(I_z\) is the predefined initialization mechanism.

---

# 10. Temporary Representation

SCBI introduces:

$$
B_t\in\mathcal{B}.
$$

`B` is intentionally treated as a general mathematical object until the research establishes a narrower interpretation.

Possible interpretations include:

* linear basis;
* coordinate system;
* subspace;
* projection;
* transformation;
* feature dictionary;
* latent representation;
* learned temporary feature vectors;
* activation-space transformation;
* low-dimensional coordinate system.

The actual interpretation must be explicitly selected for each experiment.

---

# 11. Strict Mathematical Basis

If SCBI eventually uses the word **basis** in the strict linear-algebraic sense, then for a vector space \(V\):

$$
B=\{b_1,\ldots,b_k\}
$$

must satisfy the appropriate basis conditions.

For example, a basis must provide:

1. linear independence;
2. spanning of the relevant vector space/subspace.

Until such properties are formally established, `basis` should be interpreted as:

> **temporary candidate representation / coordinate system**

rather than automatically assuming a strict linear basis.

---

# 12. Representation Transformation

A temporary representation must have an actual computational role.

Define:

$$
T_{B_t}:
(\mathcal{H},\mathcal{Z},\mathcal{X})
\rightarrow
\mathcal{H}'.
$$

Then:

$$
h'_t
=
T_{B_t}(h_t,z_t,x).
$$

The prediction becomes:

$$
\hat y_t
=
f_{\theta_0}^{(y)}(h'_t).
$$

Therefore, the temporary representation can affect the computation without modifying:

$$
\theta_0.
$$

---

# 13. General SCBI Computation

A general SCBI inference episode can be written:

$$
x
\rightarrow
h_0
\rightarrow
z_0
\rightarrow
B_0
\rightarrow
\text{candidate generation}
\rightarrow
\text{candidate evaluation}
\rightarrow
\text{selection}
\rightarrow
\text{state update}
\rightarrow
B_1,z_1
\rightarrow\cdots
\rightarrow
B_T,z_T
\rightarrow
\hat y.
$$

The backbone remains:

$$
\theta_0.
$$

---

# 14. Candidate Generation

At iteration \(t\), SCBI generates one or more candidate representations.

Define:

$$
G_t:
(\theta_0,x,h_t,z_t,B_t)
\rightarrow
\mathcal{C}_t
$$

where:

$$
\mathcal{C}_t
=
\{
B_t^{(1)},
B_t^{(2)},
\ldots,
B_t^{(K_t)}
\}.
$$

Each:

$$
B_t^{(i)}\in\mathcal{B}.
$$

Candidate generation may be:

* deterministic;
* stochastic;
* search-based;
* optimization-based;
* model-generated;
* analytically constructed;
* gradient-based with respect to temporary variables;
* gradient-free.

The specific mechanism must be declared by the experiment.

---

# 15. Candidate Generation Must Not Change the Backbone

Even if candidate generation uses gradients, those gradients must not update:

$$
\theta_0.
$$

For example, if:

$$
\nabla_{B}J
$$

is computed, this does not imply:

$$
\nabla_\theta J
$$

is used to modify \(\theta\).

The optimization variable must remain temporary.

---

# 16. Candidate Evaluation

Every candidate requires a predefined evaluation mechanism.

Define:

$$
S(B,x,z)
\rightarrow
\mathbb{R}.
$$

Higher or lower values must be explicitly defined.

For a loss:

$$
L(B,x,y,z)
$$

lower is better.

For a score:

$$
S(B,x,y,z)
$$

higher may be better.

The direction must never be ambiguous.

---

# 17. Objective Function

A general objective can be written:

$$
J(B,z;x,y)
=
L_{\text{task}}
+
\lambda_1L_{\text{consistency}}
+
\lambda_2L_{\text{representation}}
+
\lambda_3C_{\text{compute}}
+
\lambda_4R_{\text{complexity}}.
$$

This is a general template, not the final SCBI objective.

The actual objective must specify:

* each term;
* units;
* normalization;
* weighting;
* optimization direction;
* availability of labels;
* computational cost;
* whether the term is train-time or inference-time.

No term may be added after seeing test results merely to improve the outcome.

---

# 18. Supervised and Unsupervised Evaluation

SCBI may operate under different information settings.

### Setting A — Label available during inference

$$
J(B,z;x,y).
$$

This must be explicitly identified as supervised/test-time adaptation.

### Setting B — No ground-truth label available

$$
J(B,z;x).
$$

Evaluation must then use an objective available without the ground-truth answer.

### Setting C — External evaluator

$$
E(B,x)
\rightarrow
s.
$$

The evaluator may be:

* another frozen model;
* deterministic program;
* reward model;
* verifier;
* symbolic checker;
* human evaluator.

External evaluators must be explicitly reported because they change the information and compute budget.

---

# 19. Information Boundary

Every SCBI experiment must define its information boundary.

Let:

$$
I_t
$$

denote all information available to SCBI at iteration \(t\).

Then:

$$
I_t=
I_{\text{input}}
\cup
I_{\text{model}}
\cup
I_{\text{state}}
\cup
I_{\text{external}}.
$$

The experiment must specify which components exist.

---

# 20. Ground-Truth Leakage

SCBI must not use:

$$
y
$$

during inference unless the experiment is explicitly designed as a supervised adaptation experiment.

For standard inference:

$$
y\notin I_t.
$$

Using the test answer directly or indirectly to construct the representation constitutes leakage.

Any leakage must invalidate that experiment as a standard inference comparison.

---

# 21. External Information

If SCBI uses:

* retrieval;
* web search;
* databases;
* external models;
* tools;
* human feedback;

then the experiment must explicitly declare this.

External information must not be silently treated as part of SCBI itself.

---

# 22. Self-Consistency

### `[OPEN DEFINITION]`

The term **self-consistency** is currently not considered mathematically finalized.

A candidate formulation is:

$$
C(B;x,z)
=
\operatorname{Consistency}
\left(
\mathcal{P}_1(B,x,z),
\ldots,
\mathcal{P}_m(B,x,z)
\right)
$$

where:

$$
\mathcal{P}_i
$$

represents a defined prediction, representation, reasoning, transformation, or evaluation under condition \(i\).

However, this formulation is only a candidate.

The project must determine:

1. What exactly is compared?
2. Why should agreement indicate quality?
3. Can incorrect outputs remain consistent?
4. Can correct outputs be inconsistent?
5. Is ground truth required?
6. Is consistency predictive of correctness?
7. Does the mechanism overlap with existing self-consistency methods?
8. What additional capability does representation adaptation provide?

Until resolved, self-consistency must remain marked `[OPEN]`.

---

# 23. Candidate Selection

Define:

$$
A_t:
(B_t^{(1)},\ldots,B_t^{(K)})
\rightarrow
B_t^\star.
$$

For minimization:

$$
B_t^\star
=
\arg\min_{B\in\mathcal{C}_t}
J(B,z_t;x,y).
$$

For maximization:

$$
B_t^\star
=
\arg\max_{B\in\mathcal{C}_t}
S(B,x,z_t).
$$

The selection rule must be fixed before evaluation on the final test set.

---

# 24. Acceptance and Rejection

Not every candidate must be accepted.

Define:

$$
A_{\text{accept}}
(B_t^\star,B_t,z_t)
\in
\{0,1\}.
$$

If accepted:

$$
B_{t+1}=R_B(B_t,B_t^\star,z_t).
$$

If rejected:

$$
B_{t+1}=B_t
$$

unless the experiment explicitly defines another update rule.

Rejection must be recorded rather than discarded from the research history.

---

# 25. State Update

Define:

$$
U:
(B_t,z_t,B_t^\star,s_t)
\rightarrow
z_{t+1}.
$$

Thus:

$$
z_{t+1}
=
U(B_t,z_t,B_t^\star,s_t).
$$

The state update must not implicitly modify:

$$
\theta_0.
$$

---

# 26. General SCBI Transition

The complete transition is:

$$
(B_t,z_t)
\xrightarrow{G_t}
\mathcal{C}_t
\xrightarrow{S,C}
\text{candidate scores}
\xrightarrow{A_t}
B_t^\star
\xrightarrow{R,U}
(B_{t+1},z_{t+1}).
$$

This transition repeats until the termination condition is satisfied.

---

# 27. Inference Iteration

At iteration \(t\):

### Step 1 — Construct representation

$$
h_t=f_{\theta_0}^{(h)}(x)
$$

or the representation resulting from the previous temporary state.

### Step 2 — Generate candidates

$$
\mathcal{C}_t=G_t(x,h_t,z_t,B_t).
$$

### Step 3 — Evaluate candidates

$$
s_t^{(i)}
=
S(B_t^{(i)},x,z_t).
$$

### Step 4 — Select

$$
B_t^\star=A_t(\mathcal{C}_t,s_t).
$$

### Step 5 — Accept/reject

$$
a_t\in\{0,1\}.
$$

### Step 6 — Update temporary state

$$
z_{t+1}=U(z_t,B_t^\star,a_t).
$$

### Step 7 — Continue or terminate.

---

# 28. Termination

Define:

$$
T_{\max}
$$

as the maximum number of inference iterations.

Possible termination conditions include:

$$
t=T_{\max}
$$

or:

$$
\left|
J_{t}-J_{t-1}
\right|
<\epsilon
$$

or:

$$
B_{t+1}=B_t
$$

for a predefined number of iterations.

Termination rules must be defined before final evaluation.

---

# 29. Final Representation

After termination:

$$
B^\star=B_T.
$$

Final state:

$$
z^\star=z_T.
$$

Final representation:

$$
h^\star
=
T_{B^\star}(h_T,z^\star,x).
$$

Final prediction:

$$
\boxed{
\hat y
=
f_{\theta_0}^{(y)}(h^\star)
}
$$

subject to the exact architecture implemented by the experiment.

---

# 30. SCBI as an Inference-Time Optimization Problem

A generalized formulation is:

$$
B^\star,z^\star
=
\operatorname*{argmin}_{B,z}
J(B,z;x)
$$

subject to:

$$
\theta=\theta_0.
$$

Therefore, the optimization variables are temporary quantities:

$$
(B,z),
$$

not the foundation-model parameters.

This distinguishes core SCBI from ordinary fine-tuning.

---

# 31. Constrained Formulation

A more explicit formulation is:

$$
\begin{aligned}
\min_{B,z}\quad
&
J(B,z;x)
\\
\text{subject to}\quad
&
\theta=\theta_0,
\\
&
B\in\mathcal{B},
\\
&
z\in\mathcal{Z},
\\
&
C_{\text{compute}}\leq C_{\max},
\\
&
I_t\subseteq I_{\max}.
\end{aligned}
$$

Here:

* \(J\) = predefined objective;
* \(\theta_0\) = frozen backbone;
* \(\mathcal{B}\) = admissible representations;
* \(\mathcal{Z}\) = admissible temporary states;
* \(C_{\max}\) = inference-compute budget;
* \(I_{\max}\) = allowed information boundary.

---

# 32. Baseline Function

Let:

$$
f_{\theta_0}(x)
$$

be the frozen-model baseline.

SCBI produces:

$$
f_{\theta_0}^{SCBI}(x).
$$

The baseline must use the same:

* backbone;
* dataset;
* preprocessing;
* evaluation set;
* output requirements;
* hardware where practical;
* information budget where applicable.

---

# 33. Performance Difference

Define:

$$
M_{\text{base}}
$$

as baseline performance and:

$$
M_{\text{SCBI}}
$$

as SCBI performance.

Then:

$$
\Delta M
=
M_{\text{SCBI}}
-
M_{\text{base}}.
$$

A positive value indicates observed improvement according to metric \(M\).

It does **not** by itself prove that the representation mechanism caused the improvement.

---

# 34. Causal Interpretation

The causal question is:

> Does the temporary representation mechanism itself produce the observed improvement?

This requires controlled comparisons.

At minimum, consider:

$$
\text{Baseline}
$$

versus:

$$
\text{SCBI}.
$$

Stronger controls may include:

* equal-compute random representation;
* random search;
* fixed transformation;
* candidate generation without selection;
* selection without representation changes;
* representation changes without self-consistency;
* extra inference steps without SCBI;
* equivalent search over unrelated variables.

---

# 35. Compute Budget

Let:

$$
C_{\text{base}}
$$

be baseline inference cost.

Let:

$$
C_{\text{SCBI}}
$$

be SCBI inference cost.

SCBI should report:

$$
C_{\text{SCBI}}/C_{\text{base}}.
$$

Improved accuracy at arbitrarily greater computation is not automatically evidence of an efficient method.

Therefore, experiments should include compute-matched comparisons where practical.

---

# 36. Information-Matched Comparison

Let:

$$
I_{\text{base}}
$$

and:

$$
I_{\text{SCBI}}
$$

represent the information available to each method.

Comparisons should clearly state whether:

$$
I_{\text{SCBI}}=I_{\text{base}}
$$

or whether SCBI receives additional information.

Additional information must not be attributed solely to the representation mechanism.

---

# 37. Search Budget

Let:

$$
K_t=|\mathcal{C}_t|
$$

be the number of candidates generated at iteration \(t\).

Total candidate evaluations:

$$
K_{\text{total}}
=
\sum_{t=0}^{T-1}K_t.
$$

This quantity must be reported.

---

# 38. Search Efficiency

A method that evaluates many candidates may achieve higher performance simply through more search.

Therefore define:

$$
\text{Efficiency}
=
\frac{\text{performance gain}}
{\text{additional compute}}
$$

or another predefined efficiency metric.

The exact metric must be fixed in the evaluation specification.

---

# 39. Representation Complexity

A representation should have a measurable complexity where practical.

Possible measures include:

* dimensionality;
* number of basis vectors;
* transformation rank;
* parameter count;
* memory footprint;
* number of operations;
* number of candidate representations.

Let:

$$
C_B(B)
$$

denote representation complexity.

Then a regularized objective may be:

$$
J(B,z;x)
=
L(B,z;x)
+
\lambda_B C_B(B).
$$

This is optional and must be experimentally justified.

---

# 40. Stability

Let:

$$
B^\star(x)
$$

be the selected representation for input \(x\).

Stability may measure whether small perturbations:

$$
x'
=
x+\delta
$$

produce similar representations:

$$
d_B(B^\star(x),B^\star(x'))
$$

for small \(\delta\).

Stability is an evaluation question, not an assumed property.

---

# 41. Robustness

SCBI should be tested under controlled perturbations such as:

* input noise;
* formatting changes;
* irrelevant context;
* semantic-preserving transformations;
* adversarial or difficult examples where appropriate.

A robust SCBI mechanism should not merely exploit superficial features.

This is an empirical question.

---

# 42. Generalization

SCBI must distinguish:

### Per-example adaptation

$$
B^\star_i
$$

is constructed independently for each input.

### Task-level adaptation

$$
B^\star_{\text{task}}
$$

is constructed for a task.

### Batch-level adaptation

$$
B^\star_{\text{batch}}
$$

is constructed from a group of examples.

These settings must never be mixed without explicit labeling.

---

# 43. Persistent vs Temporary Learning

Core SCBI is temporary.

For inference episode \(i\):

$$
(B_i,z_i)
$$

may change.

But after the episode:

$$
\theta_{i+1}=\theta_i.
$$

A persistent change such as:

$$
\theta_{i+1}\neq\theta_i
$$

is outside the core formulation.

---

# 44. Memory Across Episodes

Cross-example memory is not automatically permitted.

If:

$$
z^{(i+1)}_0
$$

depends on:

$$
z^{(i)}
$$

then the experiment contains persistent or cross-example adaptation.

This must be explicitly declared.

The default core setting is:

$$
z^{(i+1)}_0=I_z(x_{i+1})
$$

independent of previous examples unless the experiment is specifically designed to test cross-example adaptation.

---

# 45. Randomness

If candidate generation is stochastic:

$$
B_t^{(i)}
\sim
G_t(\cdot\mid x,z_t).
$$

Experiments must record:

* random seed;
* number of samples;
* sampling method;
* temperature or equivalent parameters;
* candidate count.

Repeated runs should be used where stochasticity materially affects conclusions.

---

# 46. Deterministic Form

A deterministic SCBI instance may be represented as:

$$
B_t^{(i)}
=
G_t^{(i)}(x,z_t).
$$

This may simplify reproducibility and initial debugging.

The deterministic version does not automatically represent the full research hypothesis.

---

# 47. Gradient-Based Temporary Optimization

A possible SCBI variant is:

$$
B_{t+1}
=
B_t
-
\eta
\nabla_B J(B_t,z_t;x).
$$

This is permissible only if:

$$
\nabla_\theta J
$$

does not update \(\theta\).

The resulting method should be described as **inference-time optimization of temporary representation variables**.

Whether such an approach constitutes the most meaningful form of SCBI is an open research question.

---

# 48. Gradient-Free Search

Another possible formulation is:

$$
\mathcal{C}_t
=
G_t(B_t,z_t,x)
$$

followed by evaluation and selection.

Examples include:

* random search;
* evolutionary search;
* beam search;
* discrete candidate enumeration;
* model-generated candidates.

The search mechanism must be treated as part of the algorithm specification.

---

# 49. Candidate Generator as a Learned Model

If a second model generates candidates:

$$
G_\phi(x,z_t)
\rightarrow
\mathcal{C}_t,
$$

then \(\phi\) must be explicitly reported.

Questions include:

* Is \(\phi\) frozen?
* Was it trained?
* On what data?
* Does it contain task information?
* Does it create an unfair information advantage?
* Does it make SCBI equivalent to another existing method?

A learned generator must not be hidden inside the term "SCBI."

---

# 50. Oracle Components

An oracle is any component with information unavailable to the baseline.

Examples:

* ground-truth answer;
* test labels;
* human feedback unavailable to baseline;
* future information;
* privileged metadata.

Oracle use is permitted only in explicitly labeled experiments.

---

# 51. Algorithmic Equivalence

Two implementations may appear different but perform the same computation.

If:

$$
F_1(x)=F_2(x)
$$

for all relevant inputs, they may be computationally equivalent despite different code structures.

Therefore, novelty cannot be established by implementation differences alone.

---

# 52. Representation Equivalence

Two representation mechanisms may also be equivalent under a transformation:

$$
B_2=T(B_1).
$$

The research must distinguish:

* genuinely different mechanisms;
* reparameterizations;
* coordinate changes;
* implementation variants.

This is especially important because SCBI uses the term "basis."

---

# 53. Core SCBI Tuple

The minimum mathematical description of an SCBI system is:

$$
\boxed{
S=
(
f_\theta,
x,
z_0,
B_0,
G,
S,
C,
A,
R,
U,
T
)
}
$$

subject to:

$$
\boxed{\theta_t=\theta_0\quad\forall t}.
$$

Where:

| Symbol       | Meaning                                  |
| ------------ | ---------------------------------------- |
| \(f_\theta\) | frozen foundation model                  |
| \(x\)        | input                                    |
| \(z_0\)      | initial temporary state                  |
| \(B_0\)      | initial representation                   |
| \(G\)        | candidate-generation mechanism           |
| \(S\)        | evaluation/scoring mechanism             |
| \(C\)        | consistency mechanism                    |
| \(A\)        | candidate-selection/acceptance mechanism |
| \(R\)        | representation update                    |
| \(U\)        | state update                             |
| \(T\)        | termination rule                         |

This tuple is the minimum structural representation of the current SCBI concept.

---

# 54. Core Transition Equation

The central transition is:

$$
\boxed{
(B_t,z_t)
\rightarrow
G
\rightarrow
\mathcal{C}_t
\rightarrow
(S,C)
\rightarrow
B_t^\star
\rightarrow
(A)
\rightarrow
(R,U)
\rightarrow
(B_{t+1},z_{t+1})
}
$$

with:

$$
\theta_{t+1}=\theta_t.
$$

---

# 55. Final Inference Equation

After \(T\) iterations:

$$
B^\star=B_T
$$

and:

$$
z^\star=z_T.
$$

The final representation is:

$$
h^\star
=
T_{B^\star}(h_T,z^\star,x).
$$

Prediction:

$$
\boxed{
\hat y
=
f_{\theta_0}^{(y)}(h^\star)
}
$$

This is the conceptual core of SCBI.

---

# 56. What Counts as Core SCBI?

An experiment is a candidate **core SCBI experiment** only if:

1. the backbone is frozen;
2. temporary inference-time state exists;
3. temporary representation adaptation occurs;
4. candidates can be generated or constructed;
5. candidates are evaluated using a predefined mechanism;
6. selection/update is explicit;
7. the representation affects computation;
8. the procedure terminates under a predefined rule;
9. the evaluation protocol is fixed;
10. information leakage is controlled.

Failure of one or more conditions requires the experiment to be labeled appropriately rather than silently called SCBI.

---

# 57. What Does Not Automatically Count as SCBI?

The following should not automatically be labeled SCBI:

### Ordinary fine-tuning

$$
\theta\leftarrow\theta-\eta\nabla_\theta L.
$$

This violates the frozen-backbone constraint.

### LoRA / adapters

If their parameters are optimized during the experiment, this is parameter adaptation rather than core SCBI.

### Prompt engineering

Changing a manually written prompt is not automatically temporary representation adaptation.

### Retrieval

RAG provides external information but does not itself constitute basis invention.

### Chain-of-thought

Reasoning traces are not automatically temporary representations.

### Self-consistency decoding

Sampling multiple answers and selecting a majority answer is not automatically SCBI.

### Test-time training

If model parameters are updated, it must be distinguished from core SCBI.

These methods may be baselines or related approaches.

---

# 58. SCBI Variants

Possible variants include:

### SCBI-G

Gradient-based temporary representation optimization.

### SCBI-R

Random/search-based candidate representation selection.

### SCBI-E

Evolutionary candidate search.

### SCBI-M

Model-generated candidate representations.

### SCBI-X

External-evaluator-based selection.

These names are provisional and should not be used in papers until formally adopted.

---

# 59. Ablation Variables

Important ablations include:

### No representation adaptation

$$
B_t=B_0.
$$

### No candidate selection

Use the first candidate.

### No consistency term

$$
\lambda_C=0.
$$

### No state update

$$
z_{t+1}=z_t.
$$

### Single iteration

$$
T=1.
$$

### Multiple iterations

$$
T>1.
$$

### Random representation

Replace learned/selected representation with random candidate.

### Compute-matched search

Give baseline equivalent inference computation.

These ablations help determine which component causes observed behavior.

---

# 60. Falsification Conditions

The hypothesis should be considered weakened or rejected if repeated controlled experiments show that:

1. SCBI provides no meaningful improvement;
2. improvement disappears under compute matching;
3. improvement disappears under stronger baselines;
4. random representations perform similarly;
5. representation selection contributes nothing;
6. the effect is entirely explained by extra inference computation;
7. the mechanism depends on leakage;
8. performance gains fail to generalize;
9. the proposed representation mechanism is equivalent to an existing method;
10. the claimed mechanism does not explain the observed improvement.

Negative results are valid research outcomes.

---

# 61. Strong Evidence Hierarchy

Evidence should be interpreted approximately in this order:

### Level 1 — Implementation correctness

Does the code actually implement the mathematical specification?

### Level 2 — Reproducibility

Can independent runs reproduce the observation?

### Level 3 — Baseline comparison

Does SCBI outperform appropriate baselines?

### Level 4 — Ablation evidence

Does the proposed mechanism matter?

### Level 5 — Compute-controlled evidence

Does the improvement remain after accounting for additional inference computation?

### Level 6 — Robustness

Does the effect survive perturbations and dataset changes?

### Level 7 — Mechanistic evidence

Can the internal behavior explain the improvement?

### Level 8 — Prior-art comparison

Is the method distinguishable from existing methods?

### Level 9 — Generalization

Does the result hold beyond the initial benchmark?

No lower level automatically proves a higher level.

---

# 62. Statistical Evaluation

For stochastic experiments, report:

* number of runs;
* random seeds;
* mean;
* standard deviation;
* confidence intervals where appropriate;
* per-example results where useful;
* effect size;
* statistical test when justified.

A single successful run is insufficient evidence for a general claim.

---

# 63. Practical Significance

Statistical significance is not equivalent to practical significance.

Define:

$$
\Delta M=M_{\text{SCBI}}-M_{\text{baseline}}.
$$

The research should determine whether:

$$
|\Delta M|
$$

is practically meaningful relative to:

* variance;
* compute cost;
* latency;
* memory;
* implementation complexity.

---

# 64. Convergence

SCBI must not assume convergence.

A sequence:

$$
(B_0,z_0),
(B_1,z_1),
\ldots
$$

may:

* converge;
* oscillate;
* diverge;
* collapse;
* repeatedly select the same candidate;
* terminate due to budget.

Convergence claims require mathematical or empirical evidence.

---

# 65. Representation Collapse

A failure mode occurs if candidate representations become indistinguishable:

$$
d_B(B_i,B_j)\approx0
$$

for many candidates.

This may indicate:

* insufficient candidate diversity;
* generator collapse;
* redundant transformations;
* ineffective search.

It should be measured where possible.

---

# 66. Search Redundancy

If:

$$
B_t^{(i)}
\approx
B_t^{(j)}
$$

for many candidate pairs, candidate evaluation may waste computation.

Define an appropriate representation-distance measure:

$$
d_B(B_i,B_j).
$$

The specific distance must match the representation type.

---

# 67. Information-Theoretic Interpretation

A future formulation may analyze:

$$
I(B;Y\mid X)
$$

or related quantities.

However, no information-theoretic interpretation should be assumed to prove SCBI effectiveness.

Such analyses are optional theoretical directions.

---

# 68. Optimization Interpretation

SCBI may be interpreted as inference-time optimization over a temporary search space:

$$
\mathcal{B}\times\mathcal{Z}.
$$

The frozen model defines the computational substrate while temporary variables define an episode-specific adaptation space.

This is a research interpretation and must be distinguished from an established theoretical result.

---

# 69. Search-Space Interpretation

Define:

$$
\mathcal{S}_{SCBI}
=
\mathcal{B}\times\mathcal{Z}.
$$

The research question can then be expressed as:

> Does searching over an episode-specific temporary representation/state space improve the solution produced by a frozen foundation model sufficiently to justify the additional computation?

This formulation allows comparison with other inference-time optimization methods.

---

# 70. Important Confound

A major confound is:

$$
\text{more computation}
\Rightarrow
\text{better result}.
$$

Therefore:

$$
\text{SCBI improvement}
\neq
\text{SCBI mechanism improvement}
$$

unless appropriate controls are performed.

---

# 71. Another Major Confound

Candidate generation may itself contain substantial intelligence.

If:

$$
G
$$

is a powerful learned model, observed improvement could result primarily from \(G\), rather than the basis-selection mechanism.

Therefore experiments must isolate:

$$
G
$$

from:

$$
A,R,U.
$$

---

# 72. Another Major Confound: Evaluator Quality

If candidate selection uses an evaluator:

$$
E(B,x),
$$

then performance depends on evaluator quality.

A strong evaluator may select better candidates regardless of whether the representation mechanism is meaningful.

Therefore evaluator-only baselines may be required.

---

# 73. Another Major Confound: Search Size

If SCBI evaluates:

$$
K=1000
$$

candidates while a baseline evaluates:

$$
K=1,
$$

the comparison is not computationally matched.

Search-budget controls are therefore required.

---

# 74. Another Major Confound: Hidden Parameter Updates

The implementation must verify that:

$$
\theta_T=\theta_0.
$$

It is not sufficient to assume that the optimizer is not intentionally updating weights.

The implementation should verify:

* parameter checksums;
* gradient state;
* optimizer state;
* train/eval mode;
* adapter state;
* checkpoint differences.

---

# 75. Formal Frozen-Parameter Test

Before and after every core experiment:

$$
H(\theta_0)
$$

and:

$$
H(\theta_T)
$$

should be compared using an appropriate hash/checksum or exact parameter comparison.

Require:

$$
H(\theta_0)=H(\theta_T)
$$

for deterministic parameter storage.

If numerical transformations can alter representation without parameter modification, the exact validation method must be documented.

---

# 76. Experiment Record

Every experiment should store:

$$
E=
(
\text{code version},
\text{model},
\text{dataset},
\text{seed},
\text{configuration},
\text{information boundary},
\text{compute budget},
\text{results}
).
$$

No result should exist without enough metadata to reproduce it.

---

# 77. Hyperparameters

Examples include:

$$
\eta
$$

learning rate for temporary optimization,

$$
K
$$

candidate count,

$$
T
$$

number of iterations,

$$
\lambda
$$

objective weights,

$$
\epsilon
$$

termination threshold.

Hyperparameters must be selected using a predefined protocol.

Test-set tuning is prohibited unless explicitly labeled.

---

# 78. Train / Validation / Test Separation

If hyperparameters are tuned:

$$
D_{\text{train}}
\rightarrow
\text{development}
\rightarrow
D_{\text{validation}}
\rightarrow
\text{final test}.
$$

The final test set should not be used repeatedly for design decisions.

Otherwise the reported test performance may be biased.

---

# 79. Minimum Experimental Comparison

The first useful experiment should compare:

$$
\boxed{\text{Frozen Baseline}}
$$

against:

$$
\boxed{\text{Minimal SCBI}}
$$

under the same task and controlled information boundary.

Then progressively add:

1. stronger baselines;
2. compute matching;
3. ablations;
4. robustness;
5. multiple datasets;
6. mechanistic analysis.

---

# 80. Minimum Viable SCBI

A minimal implementation should contain:

$$
f_{\theta_0}
$$

a frozen model,

$$
B_0
$$

an initial representation,

$$
G
$$

candidate generation,

$$
S
$$

candidate evaluation,

$$
A
$$

candidate selection,

$$
U
$$

temporary state update,

and:

$$
T
$$

termination.

The first implementation should be intentionally small.

Do not build a complex system before verifying the fundamental mechanism.

---

# 81. Research Progression

The recommended progression is:

```text
Mathematical definition
        ↓
Prior-art analysis
        ↓
Minimal falsifiable formulation
        ↓
Minimal implementation
        ↓
Frozen-backbone verification
        ↓
Baseline
        ↓
Minimal SCBI experiment
        ↓
Ablations
        ↓
Compute controls
        ↓
Robustness
        ↓
Mechanistic analysis
        ↓
Broader evaluation
        ↓
Scientific conclusion
```

---

# 82. Mathematical Questions Still Open

The following must not be silently resolved by implementation:

1. What is the strict mathematical definition of \(B_t\)?
2. What exactly constitutes a "basis"?
3. What is the final definition of self-consistency?
4. What objective should select representations?
5. Which representation spaces are theoretically useful?
6. Under what conditions can temporary representation adaptation improve prediction?
7. Can improvement be theoretically bounded?
8. Can convergence be established?
9. What causes representation collapse?
10. When is SCBI computationally worthwhile?
11. Which existing methods are mathematically equivalent?
12. What properties distinguish SCBI from test-time adaptation?
13. What is the smallest sufficient SCBI formulation?

These are research questions, not implementation details.

---

# 83. Required Proof Discipline

No statement may be labeled:

* theorem;
* guarantee;
* proof;
* convergence guarantee;
* optimality guarantee;

without a valid mathematical derivation.

If a proof is incomplete, label the statement:

`[CONJECTURE]`

or:

`[OPEN]`.

---

# 84. Required Empirical Discipline

No statement may be labeled:

* demonstrated;
* validated;
* consistently improves;
* state-of-the-art;
* superior;
* robust;

unless supported by the corresponding experiments.

One successful example should be labeled:

`[OBSERVATION]`

rather than generalized into a broad claim.

---

# 85. Novelty

Novelty is deliberately excluded from the mathematical definition.

The following implication is invalid:

$$
\text{new name}
\Rightarrow
\text{new method}.
$$

Likewise:

$$
\text{different implementation}
\Rightarrow
\text{novel algorithm}.
$$

Novelty requires prior-art analysis.

The literature specification is responsible for determining whether the formulation overlaps existing work.

---

# 86. Relationship to Prior Work

Before claiming that SCBI is different from:

* test-time adaptation;
* test-time training;
* inference-time optimization;
* latent optimization;
* representation editing;
* activation steering;
* self-consistency;
* iterative refinement;
* search-based inference;
* meta-learning;
* prompt optimization;
* adaptive computation;

the project must perform explicit literature analysis.

The mathematical formulation must then be compared mechanism-by-mechanism.

---

# 87. Core Scientific Distinction

The intended distinguishing constraint is:

$$
\boxed{
\text{Persistent model parameters remain frozen}
}
$$

while:

$$
\boxed{
\text{temporary representation/state may adapt during inference}
}
$$

and:

$$
\boxed{
\text{the adapted representation participates directly in inference}
}
$$

This is the central structural property being investigated.

It is **not yet a novelty claim**.

---

# 88. Research Decision Tree

For every proposed implementation, ask:

### Question 1

Does it modify \(\theta\)?

If yes:

> Not core SCBI.

### Question 2

Does it create temporary inference-time state?

If no:

> Insufficient evidence that it implements SCBI.

### Question 3

Does a temporary representation affect computation?

If no:

> It may only be search/state adaptation.

### Question 4

Is the representation selected or constructed using a defined mechanism?

If no:

> SCBI mechanism is underspecified.

### Question 5

Is the selection objective predefined?

If no:

> Experiment is scientifically underdetermined.

### Question 6

Is the information boundary explicit?

If no:

> Experiment is not ready for evaluation.

---

# 89. Implementation-to-Theory Traceability

Every implementation component must map to a mathematical component.

Example:

| Implementation        | Mathematical object |
| --------------------- | ------------------- |
| Frozen model          | \(f_{\theta_0}\)    |
| Hidden activation     | \(h_t\)             |
| Temporary memory      | \(z_t\)             |
| Candidate basis       | \(B_t^{(i)}\)       |
| Candidate generator   | \(G_t\)             |
| Score function        | \(S\)               |
| Consistency function  | \(C\)               |
| Selector              | \(A_t\)             |
| Representation update | \(R\)               |
| State update          | \(U\)               |
| Stop condition        | \(T\)               |

If an implementation component has no mathematical role, its purpose must be documented.

If a mathematical component has no implementation, the implementation is incomplete.

---

# 90. Theory-to-Experiment Traceability

Every experiment must identify:

$$
\text{Hypothesis}
\rightarrow
\text{Mathematical mechanism}
\rightarrow
\text{Implementation}
\rightarrow
\text{Metric}
\rightarrow
\text{Result}.
$$

This prevents experiments from becoming disconnected from the research question.

---

# 91. Theory Change Protocol

If the mathematical formulation changes, create a change record containing:

```text
Definition/Formulation ID:
Previous formulation:
New formulation:
Reason for change:
Evidence:
Affected experiments:
Affected implementation:
Affected documentation:
Date:
Status:
```

Do not silently replace mathematical definitions.

---

# 92. Forbidden Theory Drift

Antigravity must not silently:

* redefine \(B_t\);
* redefine \(z_t\);
* redefine self-consistency;
* introduce trainable parameters;
* change the information boundary;
* add external models;
* add retrieval;
* change the objective;
* change the stopping rule;
* change the hypothesis;
* call a variant "core SCBI."

Any such change requires explicit documentation.

---

# 93. Minimum Formal Specification

Before implementation begins, the following must be specified:

$$
\boxed{
\begin{aligned}
&f_{\theta_0}\\
&x\\
&z_0\\
&B_0\\
&G\\
&S\\
&C\\
&A\\
&R\\
&U\\
&T
\end{aligned}
}
$$

with:

$$
\boxed{\theta_t=\theta_0}.
$$

If any of these are undefined, the algorithm remains incomplete.

---

# 94. Current Mathematical Status

| Component                        | Status                 |
| -------------------------------- | ---------------------- |
| Frozen backbone                  | `[FIXED]`              |
| Input \(x\)                      | `[FIXED]`              |
| Target \(y\)                     | `[FIXED]`              |
| Model parameters \(\theta\)      | `[FIXED]`              |
| Hidden representation \(h_t\)    | `[WORKING DEFINITION]` |
| Temporary state \(z_t\)          | `[WORKING DEFINITION]` |
| Temporary representation \(B_t\) | `[WORKING/OPEN]`       |
| Candidate generation \(G\)       | `[OPEN/WORKING]`       |
| Evaluation \(S\)                 | `[OPEN/WORKING]`       |
| Self-consistency \(C\)           | `[OPEN]`               |
| Acceptance \(A\)                 | `[WORKING]`            |
| Representation update \(R\)      | `[WORKING]`            |
| State update \(U\)               | `[WORKING]`            |
| Termination \(T\)                | `[WORKING]`            |
| Final objective \(J\)            | `[OPEN]`               |
| Theoretical guarantees           | `[OPEN]`               |
| Empirical effectiveness          | `[UNKNOWN]`            |
| Novelty                          | `[UNKNOWN]`            |

---

# 95. What Antigravity Must Do With This Document

Antigravity agents must treat this document as a **research specification**, not as permission to invent missing details.

When an unresolved component is encountered:

1. identify it;
2. label it `[OPEN]`;
3. research prior work where appropriate;
4. propose candidate formulations;
5. compare alternatives;
6. document the decision;
7. obtain explicit research-level approval before treating it as fixed.

The agent must never silently select a convenient implementation and redefine the science around it.

---

# 96. Required Agent Behavior

When implementing SCBI, agents must ask:

> "Does this implementation preserve the mathematical hypothesis?"

rather than:

> "What implementation is easiest?"

When evaluating SCBI, agents must ask:

> "What alternative explanation could produce this result?"

rather than:

> "How can we make the result positive?"

When reviewing the research, agents must ask:

> "What evidence would falsify this hypothesis?"

rather than:

> "How can we prove the hypothesis?"

---

# 97. Scientific Interpretation Rule

The correct logical chain is:

$$
\text{Implementation}
\rightarrow
\text{Experiment}
\rightarrow
\text{Observation}
\rightarrow
\text{Analysis}
\rightarrow
\text{Conclusion}.
$$

Never reverse this:

$$
\text{Desired conclusion}
\rightarrow
\text{experiment selection}.
$$

The experiment must be capable of producing a negative result.

---

# 98. Final Research Principle

SCBI should not be judged by whether the implementation looks sophisticated.

It should be judged by whether a controlled experiment can answer:

> **Does temporary inference-time representation construction and selection provide a measurable capability advantage for a frozen foundation model, beyond what can be explained by extra computation, stronger auxiliary components, leakage, search, or existing methods?**

That is the scientific question this specification exists to preserve.

---

# 99. Source of Truth

For terminology:

```text
theory/README_DEFINITIONS.md
```

For mathematical formulation:

```text
theory/README.md
```

For prior art:

```text
research/README_LITERATURE.md
```

For implementation:

```text
scbi/README.md
```

For experiments:

```text
experiments/README.md
```

For evaluation:

```text
evaluation/README.md
```

If documents conflict, the conflict must be explicitly reported and resolved.

No agent may silently choose one interpretation.

---

# 100. Final Constraint

The core SCBI research specification can be summarized as:

$$
\boxed{
\begin{aligned}
&\theta_t=\theta_0
\\[2mm]
&z_t\in\mathcal{Z}
\\[2mm]
&B_t\in\mathcal{B}
\\[2mm]
&\mathcal{C}_t=G_t(x,h_t,z_t,B_t)
\\[2mm]
&B_t^\star=A_t(\mathcal{C}_t,S,C)
\\[2mm]
&(B_{t+1},z_{t+1})
=
(R,U)(B_t^\star,z_t)
\\[2mm]
&\hat y
=
f_{\theta_0}^{(y)}
\left(
T_{B^\star}(h_T,z^\star,x)
\right)
\end{aligned}
}
$$

with the critical scientific condition:

$$
\boxed{
\textbf{The foundation-model parameters remain frozen throughout the core inference episode.}
}
$$

Everything beyond this equation remains subject to formal definition, prior-art analysis, implementation verification, experimentation, and falsification.

---

## Document Status

**Current status:** Provisional mathematical research specification.

**Not yet established:**

* final definition of "basis";
* final definition of self-consistency;
* final objective function;
* theoretical guarantees;
* empirical effectiveness;
* computational advantage;
* novelty.

**Established project constraint:**

$$
\boxed{\theta_t=\theta_0}
$$

for all core SCBI experiments.

**Scientific standard:**

> Do not let implementation convenience determine the mathematical definition. Do not let positive experimental results determine the hypothesis. Do not let the name determine novelty. Let definitions, controlled experiments, prior art, and evidence determine what SCBI actually is.
