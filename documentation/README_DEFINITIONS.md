# SCBI Formal Definitions

## Self-Consistent Basis Invention (SCBI)

---

# 1. Purpose

This document defines the formal vocabulary and mathematical objects used throughout the SCBI research repository.

Its purpose is to prevent ambiguity, terminology drift, and implementation-driven redefinition of the research hypothesis.

The definitions in this document are the current **source of truth** for:

* the frozen foundation model,
* model parameters,
* inputs and targets,
* hidden representations,
* temporary inference state,
* temporary representations,
* candidate representations,
* candidate generation,
* candidate evaluation,
* self-consistency,
* acceptance/rejection,
* representation updates,
* state updates,
* inference iterations,
* inference budget,
* computational cost,
* and the distinction between core SCBI and variants.

These definitions are initially provisional.

A definition may be changed only through the **Definition Change Protocol** described later in this document.

---

# 2. Definition Status

Every definition belongs to one of four statuses.

## 2.1 Fixed

A definition is sufficiently precise and is not expected to change without strong evidence.

Example:

$$
\theta
$$

denotes the underlying model parameters.

---

## 2.2 Working Definition

A definition is currently being used for experiments but may change after theory or literature analysis.

Example:

$$
B_t
$$

as a temporary representation object.

---

## 2.3 Open Definition

The research question is not yet sufficiently resolved to provide one definitive mathematical definition.

Example:

The exact mathematical meaning of "self-consistency."

---

## 2.4 Variant Definition

A definition applies only to a particular experimental implementation.

Example:

A matrix-valued basis:

$$
B_t\in\mathbb{R}^{d\times k}.
$$

This must not automatically become the definition of SCBI itself.

---

# 3. Core Mathematical Universe

Define:

$$
\Theta
$$

as the parameter space of the foundation model.

Define:

$$
\mathcal{X}
$$

as the input space.

Define:

$$
\mathcal{Y}
$$

as the output/target space.

Define:

$$
\mathcal{H}
$$

as the relevant representation space.

Define:

$$
\mathcal{Z}
$$

as the temporary inference-state space.

Define:

$$
\mathcal{B}
$$

as the space of admissible temporary representation objects.

Thus:

$$
\theta\in\Theta
$$

$$
x\in\mathcal{X}
$$

$$
y\in\mathcal{Y}
$$

$$
h\in\mathcal{H}
$$

$$
z\in\mathcal{Z}
$$

$$
B\in\mathcal{B}.
$$

---

# 4. Foundation Model

The foundation model is represented by:

$$
f_\theta.
$$

Here:

$$
\theta\in\Theta
$$

is the complete set of persistent model parameters.

The model may be decomposed into layers:

$$
f_\theta
=
F_L\circ F_{L-1}\circ\cdots\circ F_1.
$$

with:

$$
\theta=
\{\theta_1,\theta_2,\ldots,\theta_L\}.
$$

---

# 5. Frozen Parameters

For core SCBI:

$$
\boxed{\theta_t=\theta_0}
$$

for every inference step \(t\).

Equivalently:

$$
\boxed{\Delta\theta_t=0}
$$

where:

$$
\Delta\theta_t
=
\theta_{t+1}-\theta_t.
$$

Therefore:

$$
\theta_0
=
\theta_1
=
\cdots
=
\theta_T.
$$

This is a **hard constraint** of core SCBI.

---

# 6. What "Frozen" Means

A model is considered frozen only if its persistent trainable parameters remain unchanged during the SCBI inference procedure.

The following are therefore prohibited in core SCBI:

* gradient updates to model parameters,
* optimizer updates to model parameters,
* parameter rewriting,
* LoRA updates,
* adapter-weight updates,
* bias updates,
* normalization-parameter updates,
* persistent weight modifications.

Temporary activations or inference state may change.

The distinction is:

```text
Persistent model parameters
        ↓
        MUST NOT CHANGE

Temporary inference state
        ↓
        MAY CHANGE
```

---

# 7. Input

The input is:

$$
x\in\mathcal{X}.
$$

Depending on the task, \(x\) may represent:

* text,
* an image,
* audio,
* video,
* structured data,
* multimodal data,
* a sequence,
* or another valid model input.

The exact input domain belongs to the experiment configuration.

---

# 8. Target

For supervised tasks:

$$
y\in\mathcal{Y}
$$

denotes the target.

For unsupervised or self-supervised tasks, a ground-truth \(y\) may not exist.

In that case, evaluation may use:

$$
\mathcal{L}_{self}
$$

or another predefined objective.

The absence of ground truth must not be interpreted as evidence that an arbitrary evaluator is valid.

---

# 9. Prediction

The model's prediction is:

$$
\hat{y}.
$$

At inference iteration \(t\):

$$
\hat{y}_t.
$$

The final prediction is:

$$
\hat{y}_T.
$$

The prediction may be:

* a class,
* probability distribution,
* generated sequence,
* embedding,
* structured output,
* numerical value,
* or another task-specific output.

---

# 10. Hidden Representation

Let:

$$
h_t\in\mathcal{H}
$$

denote a representation produced during inference.

For a conventional frozen model:

$$
h_0=f_\theta^{(h)}(x).
$$

The exact layer at which \(h_t\) is defined must be specified by the experiment.

A representation should not be called a "basis" merely because it is an internal activation.

---

# 11. Temporary Inference State

Define:

$$
\boxed{z_t\in\mathcal{Z}}
$$

as temporary state used during the inference procedure.

The state is:

* created or initialized during inference,
* potentially modified during inference,
* not part of the persistent model parameters,
* associated with the current inference process.

Examples may include:

* latent variables,
* optimization variables,
* temporary memory,
* candidate-selection state,
* task-specific state,
* intermediate representation information,
* search state.

The exact contents depend on the implementation.

---

# 12. Persistent vs Temporary State

The distinction is mandatory.

### Persistent state

Survives beyond the inference episode.

Examples:

* model weights,
* trained adapters,
* persistent databases,
* permanent memory.

### Temporary state

Exists only for the current inference procedure.

Examples:

$$
z_t
$$

and:

$$
B_t.
$$

Core SCBI primarily investigates temporary adaptation.

---

# 13. Inference Episode

An inference episode is the complete computation associated with one task/input instance.

Define:

$$
E(x)
$$

as an inference episode for input \(x\).

An episode may contain:

$$
E(x)
=
\{x,\theta,z_0,B_0,\ldots,z_T,B_T,\hat{y}\}.
$$

At the end of the episode, temporary state is normally discarded unless an experiment explicitly studies persistence.

---

# 14. Temporary Representation

The central SCBI object is:

$$
\boxed{B_t\in\mathcal{B}}
$$

where \(B_t\) denotes a temporary representation object used during inference.

The term "basis" is intentionally broader at this stage.

A valid \(B_t\) may eventually be shown to be one of:

* a linear basis,
* a coordinate system,
* a subspace,
* a projection,
* a transformation,
* a dictionary,
* a collection of feature vectors,
* a latent representation,
* an activation-space transformation,
* another mathematically defined representation object.

---

# 15. Necessary Condition for \(B_t\)

To qualify as an SCBI candidate representation, \(B_t\) must have a defined computational role.

There must exist a function:

$$
T_B
$$

such that:

$$
h'_t=T_{B_t}(h_t,z_t,x)
$$

or an equivalent intervention mechanism.

Therefore, merely storing arbitrary metadata in a variable named \(B_t\) does not qualify.

---

# 16. Representation Effect

A candidate representation should have a measurable effect on inference.

Define:

$$
h'_t=T(B_t,h_t,z_t,x).
$$

The model then produces:

$$
\hat{y}_t
=
f_\theta(x;B_t,z_t).
$$

The notation:

$$
f_\theta(x;B_t,z_t)
$$

is shorthand for inference under the temporary intervention.

It does **not** mean that \(B_t\) has been inserted into the model's persistent parameters.

---

# 17. Basis: Strict Interpretation

If the research eventually establishes that \(B_t\) is a mathematical basis, then:

$$
B_t
=
\{b_1,\ldots,b_k\}
$$

must satisfy the required properties of the relevant vector space.

For example, for a basis of a subspace \(\mathcal{S}\):

### Linear independence

$$
\sum_{i=1}^{k}a_i b_i=0
\Rightarrow
a_i=0\quad\forall i.
$$

### Spanning

$$
\forall v\in\mathcal{S},
\quad
v=\sum_{i=1}^{k}a_i b_i.
$$

Until this is established, use:

> temporary representation object

rather than assuming a strict linear basis.

---

# 18. Candidate Representation

At iteration \(t\), a candidate is:

$$
B_t^{(i)}
$$

where:

$$
i\in\{1,\ldots,K\}.
$$

The candidate set is:

$$
\mathcal{C}_t
=
\{B_t^{(1)},B_t^{(2)},\ldots,B_t^{(K)}\}.
$$

Candidates represent alternative temporary representations considered during inference.

---

# 19. Candidate Generation

Candidate generation is the process:

$$
G(x,z_t,B_t)
\rightarrow
\mathcal{C}_t.
$$

More generally:

$$
\mathcal{C}_t
=
G_\phi(x,z_t,B_t).
$$

The generator may be:

* deterministic,
* stochastic,
* gradient-based,
* gradient-free,
* learned,
* heuristic,
* search-based,
* externally proposed.

The generator itself is not automatically part of the novelty claim.

---

# 20. Candidate Diversity

Candidate generation may produce:

$$
K
$$

candidates.

Define candidate diversity as a measurable property:

$$
D(\mathcal{C}_t).
$$

Possible diversity measures include:

* pairwise distance,
* cosine distance,
* subspace angle,
* representation similarity,
* structural diversity.

The exact measure must depend on the representation.

---

# 21. Candidate Evaluation

Each candidate is evaluated using:

$$
S(B_t^{(i)};x,z_t).
$$

Higher score may represent better performance, depending on the definition.

Alternatively define a loss:

$$
\mathcal{L}(B_t^{(i)};x,z_t).
$$

Lower loss is preferred.

The evaluation mechanism must be explicitly defined.

---

# 22. Evaluation Must Be Predefined

The evaluation function cannot be chosen after seeing results.

For each experiment:

```text
Objective
↓
Evaluation metric
↓
Acceptance rule
```

must be specified before the primary result is analyzed.

This prevents post-hoc optimization.

---

# 23. Supervised Evaluation

If target \(y\) is available:

$$
\mathcal{L}
=
\mathcal{L}
\left(
f_\theta(x;B,z),y
\right).
$$

Examples include:

* cross-entropy,
* mean squared error,
* negative log likelihood,
* task-specific loss.

---

# 24. Self-Supervised Evaluation

If \(y\) is unavailable, define:

$$
\mathcal{L}_{self}
=
\mathcal{L}_{self}
(x,B,z).
$$

The objective must be independently justified.

An arbitrary confidence score is not automatically a valid proxy for correctness.

---

# 25. Self-Consistency

The term:

$$
\boxed{\text{self-consistency}}
$$

is an **open definition**.

It must not simply mean:

> the model agrees with itself.

A mathematical definition is required.

A candidate definition is:

$$
C(B;x,z)
=
\operatorname{Agreement}
\left(
\hat{y}^{(1)},
\hat{y}^{(2)},
\ldots,
\hat{y}^{(m)}
\right).
$$

However, the exact sources of the multiple predictions must be specified.

Possible consistency axes include:

* input perturbations,
* representation perturbations,
* stochastic forward passes,
* candidate representations,
* model layers,
* temporal inference steps,
* multiple views.

---

# 26. Self-Consistency Requirement

A valid self-consistency measure must answer:

1. What entities are being compared?
2. What constitutes agreement?
3. Why should agreement correlate with correctness or useful inference?
4. Can a wrong answer still be highly consistent?
5. Can a correct answer be inconsistent?
6. Is the criterion independent of the target?
7. Does the criterion introduce additional compute?
8. Does the criterion already exist in prior work?

These questions must be answered before using self-consistency as a central scientific claim.

---

# 27. Consistency Score

A generic notation is:

$$
C_t
=
C(B_t,z_t,x).
$$

A threshold-based criterion may be:

$$
C_t\geq\tau.
$$

where:

$$
\tau
$$

is predetermined.

The threshold must not be tuned on the test set.

---

# 28. Acceptance

Define:

$$
A(B_t^{(i)},B_t)
\in
\{0,1\}.
$$

A simple acceptance rule is:

$$
A=1
\iff
S(B_t^{(i)})>S(B_t).
$$

A consistency-constrained rule may be:

$$
A=1
\iff
S(B_t^{(i)})>S(B_t)
\land
C(B_t^{(i)})\geq\tau.
$$

This is only a candidate formulation.

---

# 29. Rejection

If:

$$
A=0,
$$

the candidate is rejected.

A simple update is:

$$
B_{t+1}=B_t.
$$

The rejected candidate should still be recorded for analysis.

Rejected candidates must never be silently deleted from research records.

---

# 30. Representation Update

Define:

$$
R:
\mathcal{B}\times\mathcal{B}\times\mathcal{Z}\times\mathcal{X}
\rightarrow
\mathcal{B}.
$$

Then:

$$
B_{t+1}
=
R(B_t,B_t^*,z_t,x).
$$

Possible implementations include:

### Replacement

$$
B_{t+1}=B_t^*
$$

### Interpolation

$$
B_{t+1}
=
(1-\alpha)B_t+\alpha B_t^*
$$

### Incremental modification

$$
B_{t+1}=B_t+\Delta B_t.
$$

The exact update defines part of the algorithm and must be recorded.

---

# 31. State Update

Define:

$$
U:
\mathcal{Z}\times\mathcal{B}\times\mathcal{X}
\rightarrow
\mathcal{Z}.
$$

Then:

$$
z_{t+1}
=
U(z_t,B_{t+1},x).
$$

State update may be:

$$
z_{t+1}=z_t
$$

if no temporary state adaptation is required.

---

# 32. Inference Iteration

One SCBI iteration consists conceptually of:

```text
Current state
      ↓
Candidate generation
      ↓
Candidate evaluation
      ↓
Consistency evaluation
      ↓
Candidate selection
      ↓
Accept/reject
      ↓
Representation update
      ↓
State update
```

This sequence defines an iteration:

$$
t\rightarrow t+1.
$$

---

# 33. Initial Representation

The initial representation is:

$$
B_0.
$$

It may be:

* empty,
* identity,
* model-derived,
* randomly initialized,
* task-derived,
* externally supplied.

The initialization must be explicitly specified.

---

# 34. Initial State

The initial state is:

$$
z_0.
$$

It must be generated using only information allowed by the experiment.

If:

$$
z_0
$$

contains target information during an evaluation that is supposed to be target-free, the experiment is invalid.

---

# 35. Information Boundary

At each inference step, define the information available to SCBI:

$$
I_t.
$$

Then:

$$
B_{t+1},z_{t+1}
=
F(I_t).
$$

The information boundary must specify whether SCBI can access:

* the input,
* previous activations,
* model outputs,
* external retrieval,
* ground truth,
* evaluation labels,
* additional examples,
* human feedback,
* external models.

---

# 36. Ground-Truth Leakage

Ground truth must not be used to construct or select \(B_t\) in experiments claiming target-free inference.

Invalid:

$$
B_t=G(x,y).
$$

Valid target-free form:

$$
B_t=G(x,\hat{y}_{<t},z_t).
$$

unless the experimental task explicitly permits target information.

---

# 37. External Information

External information is any information unavailable to the baseline under the chosen comparison protocol.

Examples:

* retrieval databases,
* external models,
* search engines,
* human feedback,
* additional labeled examples.

If used, it must be documented.

---

# 38. Inference-Time Learning

Inference-time learning means that some computational object changes as a consequence of information available during the inference episode.

For SCBI:

$$
B_t
$$

and/or:

$$
z_t
$$

may change.

This does not imply that:

$$
\theta
$$

changes.

---

# 39. Inference-Time Adaptation

Define inference-time adaptation as:

$$
\mathcal{A}(x):
\text{initial inference state}
\rightarrow
\text{adapted inference state}.
$$

SCBI is a candidate inference-time adaptation mechanism.

However, the term itself is broad and is heavily used in prior literature.

Therefore:

> inference-time adaptation ≠ SCBI

by definition.

---

# 40. Persistent Adaptation

An adaptation is persistent if:

$$
B^*
$$

or modified parameters are retained for future inference episodes.

Core SCBI should normally use:

$$
B^*\rightarrow\text{discard}
$$

after the episode.

Persistent variants must be separately labeled.

---

# 41. Temporary Adaptation

Temporary adaptation means:

$$
B_0
\rightarrow
B_1
\rightarrow
\cdots
\rightarrow
B_T
$$

within one inference episode, followed by disposal or reset.

This is the default SCBI interpretation.

---

# 42. Final Representation

After the final iteration:

$$
B^*=B_T.
$$

The final representation is used for final inference:

$$
\hat{y}
=
f_\theta(x;B^*,z_T).
$$

---

# 43. Final State

Similarly:

$$
z^*=z_T.
$$

The pair:

$$
(B^*,z^*)
$$

represents the final temporary inference configuration.

---

# 44. SCBI Trajectory

An inference episode may produce:

$$
\tau_{SCBI}
=
\{
(B_0,z_0),
(B_1,z_1),
\ldots,
(B_T,z_T)
\}.
$$

This trajectory can be analyzed for:

* convergence,
* stability,
* diversity,
* collapse,
* oscillation,
* computational cost.

---

# 45. Objective

Define a general objective:

$$
J(B,z;x)
$$

which may contain:

$$
J
=
\mathcal{L}_{task}
+
\lambda_c C_{consistency}
+
\lambda_r C_{representation}
+
\lambda_f C_{compute}.
$$

The exact objective must be specified by the experiment.

The existence of an objective does not establish novelty.

---

# 46. Task Loss

Define:

$$
\mathcal{L}_{task}
=
\mathcal{L}
(f_\theta(x;B,z),y)
$$

when \(y\) is available.

For target-free evaluation:

$$
\mathcal{L}_{task}
$$

may be replaced by a justified proxy.

---

# 47. Representation Cost

Define:

$$
C_{representation}(B)
$$

as the cost associated with the temporary representation.

Possible measurements:

* number of vectors,
* dimensionality,
* rank,
* memory,
* parameter count,
* storage,
* computational operations.

---

# 48. Inference Compute

Define:

$$
C_{compute}
$$

as the additional computation introduced by SCBI.

Possible measures:

* forward passes,
* FLOPs,
* GPU time,
* wall-clock latency,
* candidate evaluations,
* optimization iterations,
* memory bandwidth.

The actual primary compute measure must be specified in experiments.

---

# 49. Inference Budget

Define an inference budget:

$$
\mathcal{B}_{inf}.
$$

It may constrain:

$$
K\leq K_{max}
$$

$$
T\leq T_{max}
$$

$$
F\leq F_{max}.
$$

A method must not receive unlimited additional computation unless the experiment explicitly studies scaling.

---

# 50. Compute-Matched Comparison

For a fair comparison:

$$
C(SCBI)
\approx
C(Baseline).
$$

If exact equality is impossible, report:

$$
\Delta C
=
C(SCBI)-C(Baseline).
$$

Performance improvements must be interpreted together with:

$$
\Delta C.
$$

---

# 51. Information-Matched Comparison

Define:

$$
I(M)
$$

as the information available to method \(M\).

For a controlled comparison:

$$
I(SCBI)\approx I(Baseline).
$$

Any additional information must be reported.

---

# 52. Candidate Selection

The selected candidate is:

$$
B_t^*
=
\operatorname{Select}(\mathcal{C}_t,S,C).
$$

For simple maximization:

$$
B_t^*
=
\arg\max_{B\in\mathcal{C}_t}S(B).
$$

For minimization:

$$
B_t^*
=
\arg\min_{B\in\mathcal{C}_t}\mathcal{L}(B).
$$

---

# 53. Candidate Search

Candidate search means exploring:

$$
\mathcal{C}_t.
$$

Search may be:

* exhaustive,
* stochastic,
* gradient-based,
* gradient-free,
* beam-based,
* evolutionary,
* Bayesian,
* heuristic.

SCBI does not automatically imply a specific search method.

---

# 54. SCBI Core Definition

For the purposes of the current research, **core SCBI** is provisionally defined as:

> **An inference-time mechanism coupled to a frozen foundation model that constructs or proposes temporary representation objects, evaluates candidate representations using a predefined objective and/or consistency criterion, and may iteratively select or modify the temporary representation and inference state without modifying the persistent foundation-model parameters.**

Mathematically:

$$
\boxed{
\theta_{t+1}=\theta_t
}
$$

while:

$$
\boxed{
(B_t,z_t)
\rightarrow
(B_{t+1},z_{t+1})
}
$$

may occur during inference.

---

# 55. Minimum SCBI Components

A system should not be called SCBI merely because it changes an activation.

The current minimum conceptual components are:

```text
1. Frozen foundation model
2. Temporary representation/state
3. Candidate construction or modification
4. Candidate evaluation
5. Selection, acceptance, or update
6. Inference-time operation
```

The exact role of "self-consistency" remains an open research question.

---

# 56. Optional Components

The following are optional unless theory establishes otherwise:

* multiple candidates,
* iterative optimization,
* explicit consistency score,
* gradient-based optimization,
* gradient-free optimization,
* external evaluator,
* retrieval,
* memory,
* learned candidate generator,
* stochastic sampling.

Optional components must not become hidden requirements.

---

# 57. Core SCBI vs Variants

## Core

$$
\Delta\theta=0
$$

and temporary representation/state adaptation occurs during inference.

## Variant A — Parameter Adaptation

$$
\Delta\theta\neq0.
$$

Not core SCBI.

## Variant B — Retrieval-Augmented SCBI

Uses external retrieval.

## Variant C — Learned Generator

Uses a trained model to generate \(B_t\).

## Variant D — Persistent SCBI

Retains representations across inference episodes.

## Variant E — Multimodal SCBI

Operates over multimodal representations.

Each variant must explicitly state what changed.

---

# 58. What Does Not Qualify as SCBI by Itself

The following alone are insufficient:

### Ordinary inference

$$
B_t=B_0
$$

with no adaptation.

### Fine-tuning

$$
\theta\rightarrow\theta'.
$$

### Prompt engineering

Changing only the textual prompt.

### RAG

Retrieving information without temporary representation construction.

### Self-consistency decoding

Sampling multiple outputs without representation adaptation.

### Activation steering

Applying a fixed steering vector without dynamic candidate construction/evaluation.

### Random noise injection

Changing representations without an explicit candidate/evaluation mechanism.

### Chain-of-thought

Generating reasoning text alone.

---

# 59. Important Non-Equivalence Rule

Two systems should be considered equivalent only after algorithmic or mathematical analysis.

The following are not sufficient distinctions:

```text
Different name
Different notation
Different implementation language
Different repository
Different model
Different benchmark
Different variable names
```

---

# 60. Representation Equivalence

Two representation objects:

$$
B
$$

and:

$$
\tilde{B}
$$

may be considered equivalent under transformation \(Q\) if they produce the same relevant computational behavior:

$$
f_\theta(x;B,z)
\approx
f_\theta(x;\tilde{B},\tilde{z})
$$

under the defined equivalence criterion.

The exact equivalence relation must be determined for each representation class.

---

# 61. Algorithmic Equivalence

Two algorithms are potentially algorithmically equivalent if they perform the same essential operations:

```text
construct
→ evaluate
→ select
→ update
```

even if the implementation details differ.

The literature agent and theory agent must investigate this explicitly.

---

# 62. Observed Improvement

Define observed improvement:

$$
\Delta P
=
P(SCBI)-P(Baseline).
$$

A positive:

$$
\Delta P>0
$$

is an empirical observation.

It is not automatically evidence of causality or novelty.

---

# 63. Causal Effect

A causal claim requires a controlled intervention.

Conceptually:

$$
Y(B=1)-Y(B=0).
$$

The experiment must isolate the effect of dynamic representation adaptation from:

* additional compute,
* additional information,
* evaluator effects,
* randomness,
* implementation differences.

---

# 64. Statistical Significance

A measured improvement must be accompanied by an appropriate statistical analysis.

Possible quantities include:

$$
p
$$

values,

confidence intervals:

$$
CI
$$

and effect sizes:

$$
d.
$$

The specific statistical methodology belongs in:

```text
evaluation/README.md
```

and must be selected before final evaluation where practical.

---

# 65. Practical Significance

Statistical significance is not sufficient.

A tiny improvement may be statistically significant but practically irrelevant.

Therefore report:

$$
\Delta P
$$

alongside:

$$
\Delta C.
$$

---

# 66. Stability

Define representation stability using a distance:

$$
D_B(B_t,B_{t+1}).
$$

Similarly:

$$
D_z(z_t,z_{t+1}).
$$

Potential instability occurs when small input changes produce disproportionately large state changes.

---

# 67. Robustness

Let:

$$
x'
=
\operatorname{Perturb}(x).
$$

Robustness studies:

$$
P(SCBI,x')
$$

relative to:

$$
P(SCBI,x).
$$

The perturbation family must be predefined.

---

# 68. Convergence

An SCBI process may be considered convergent under a chosen criterion if:

$$
D(B_{t+1},B_t)<\epsilon_B
$$

and/or:

$$
|J_{t+1}-J_t|<\epsilon_J.
$$

Convergence must not be assumed.

The algorithm may oscillate or terminate without convergence.

---

# 69. Representation Collapse

Representation collapse occurs when candidate representations become insufficiently distinguishable.

A potential measurement is:

$$
D(B_i,B_j)\rightarrow0
$$

for many candidate pairs.

Collapse must be experimentally defined for the representation being used.

---

# 70. Candidate Redundancy

Candidate redundancy occurs when:

$$
B_i\approx B_j
$$

for many candidates.

High redundancy can increase inference cost without increasing search coverage.

---

# 71. Search Efficiency

Define:

$$
E_{search}
=
\frac{\text{performance improvement}}
{\text{additional inference cost}}.
$$

This is only one possible efficiency measure.

A final efficiency metric must be chosen based on the experiment.

---

# 72. Generalization

SCBI generalization refers to whether the observed mechanism transfers beyond the conditions under which it was developed.

Possible dimensions:

* new examples,
* new datasets,
* new domains,
* new tasks,
* new models,
* new distributions.

---

# 73. Transfer

Transfer asks whether:

$$
B^*
$$

constructed for one task/example remains useful for another.

If:

$$
B^*(x_1)
$$

is applied to:

$$
x_2,
$$

this is no longer ordinary per-example temporary adaptation and must be explicitly studied.

---

# 74. Per-Example Adaptation

If:

$$
B^*=B^*(x)
$$

then each input may receive a distinct temporary representation.

This is the default interpretation for per-example SCBI.

---

# 75. Per-Task Adaptation

If:

$$
B^*=B^*(\mathcal{D}_{task}),
$$

then the representation is adapted to a task rather than a single example.

This must be labeled separately.

---

# 76. Per-Batch Adaptation

If:

$$
B^*=B^*(x_1,\ldots,x_n),
$$

then the representation depends on multiple examples.

This changes the information boundary and must be explicitly documented.

---

# 77. External Evaluator

An external evaluator is any model or process other than the frozen foundation model used to score candidates.

Represent:

$$
V(B,x)
$$

as an evaluator.

If used, it must be documented because the evaluator can introduce additional capabilities.

---

# 78. Learned Candidate Generator

A learned generator may be represented as:

$$
G_\phi.
$$

If:

$$
\phi
$$

is trained separately, its training procedure must be documented.

If \(G_\phi\) is sufficiently powerful to solve the task itself, experiments must determine whether observed gains are actually caused by the generator rather than SCBI.

---

# 79. Oracle

An oracle is any process that has access to information unavailable during legitimate inference.

Oracle access must never be hidden.

Examples:

$$
G(x,y)
$$

where \(y\) is unavailable at test time.

---

# 80. Leakage

Information leakage occurs when evaluation information enters:

* candidate generation,
* candidate selection,
* representation construction,
* state update,
* hyperparameter selection.

Leakage invalidates the intended evaluation.

---

# 81. Hyperparameter

A hyperparameter is a value selected outside the inference optimization itself.

Examples:

$$
\lambda,\tau,K,T,\eta.
$$

Hyperparameters must be selected using a predefined protocol.

---

# 82. Test Set

The test set must not be used to optimize:

* candidate-generation rules,
* thresholds,
* stopping criteria,
* representation dimension,
* number of iterations,
* model selection,
* prompt design.

Otherwise the reported test performance becomes biased.

---

# 83. Baseline

A baseline is a controlled method used to determine whether SCBI provides meaningful benefit.

A baseline must be:

* relevant,
* reproducible,
* fairly configured,
* computationally documented.

The strongest reasonable baselines should be preferred over convenient weak baselines.

---

# 84. Ablation

An ablation removes one component from SCBI.

For example:

```text
Full SCBI
↓
remove candidate search
↓
remove consistency
↓
remove state update
↓
remove representation update
```

Ablations determine which components actually matter.

---

# 85. Core Research Variables

The initial primary variables are:

$$
\theta,x,y,h_t,z_t,B_t,K,T,\tau.
$$

Additional variables may be introduced only when necessary.

---

# 86. Variable Naming Rules

Use:

```text
θ       frozen model parameters
x       input
y       target
ŷ       prediction
h       model representation
z       temporary inference state
B       temporary representation
C       candidate set or consistency, depending on context
S       score
L       loss
G       candidate generator
R       representation update
U       state update
T       iteration budget
K       candidate budget
τ       threshold
```

Do not reuse a symbol for unrelated concepts within the same mathematical document.

---

# 87. Notation Conflict Rule

If a symbol must be reused in a different context, explicitly define the new context.

Avoid ambiguous notation such as using:

$$
T
$$

simultaneously for:

* iterations,
* transformation,
* temperature.

Prefer:

$$
T_{max}
$$

for iteration count and:

$$
\mathcal{T}
$$

for a transformation.

---

# 88. Definition Change Protocol

A core definition may be changed only when supported by:

* literature evidence,
* mathematical necessity,
* experimental evidence,
* implementation necessity with scientific justification.

Every change must be recorded:

```text
Definition ID:
Previous definition:
New definition:
Reason:
Evidence:
Affected files:
Affected experiments:
Date:
Approved by:
```

---

# 89. Forbidden Silent Changes

The following must never occur silently:

```text
B_t changes from latent vector → matrix
z_t changes from state → memory
self-consistency changes from agreement → confidence
core SCBI begins updating θ
per-example adaptation becomes per-task adaptation
target information becomes available during inference
candidate generator gains an external model
```

Any such change requires a logged revision.

---

# 90. Definition Validation Checklist

Before implementing a major SCBI experiment:

```text
[ ] θ is explicitly defined
[ ] θ is frozen
[ ] x is defined
[ ] y availability is defined
[ ] h_t is defined
[ ] z_t is defined
[ ] B_t is defined
[ ] B_t's computational role is defined
[ ] Candidate generation is defined
[ ] Candidate evaluation is defined
[ ] Selection is defined
[ ] Acceptance/rejection is defined
[ ] Update rule is defined
[ ] Information boundary is defined
[ ] Inference budget is defined
[ ] Compute budget is defined
[ ] Leakage conditions are defined
[ ] Baseline is defined
[ ] Variant status is defined
```

---

# 91. Minimum Formal SCBI Tuple

A core SCBI experiment can be represented abstractly as:

$$
\boxed{
\mathcal{S}
=
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
\boxed{
\theta_t=\theta_0
\quad\forall t
}
$$

where:

* \(f_\theta\) = frozen foundation model
* \(x\) = input
* \(z_0\) = initial temporary state
* \(B_0\) = initial temporary representation
* \(G\) = candidate generator
* \(S\) = evaluation score
* \(C\) = consistency mechanism
* \(A\) = acceptance rule
* \(R\) = representation update
* \(U\) = state update
* \(T\) = iteration budget.

This tuple is a theoretical abstraction, not a claim that every component must be implemented independently.

---

# 92. Core SCBI Transition

The generic transition is:

$$
(B_t,z_t)
\xrightarrow{G}
\mathcal{C}_t
\xrightarrow{S,C}
B_t^*
\xrightarrow{A}
\xrightarrow{R,U}
(B_{t+1},z_{t+1}).
$$

The model parameters remain:

$$
\theta.
$$

---

# 93. Final SCBI Output

After \(T\) iterations:

$$
(B_T,z_T)
$$

produce:

$$
\boxed{
\hat{y}
=
f_\theta(x;B_T,z_T)
}
$$

The temporary objects may then be discarded:

$$
(B_T,z_T)
\rightarrow
\varnothing.
$$

---

# 94. Scientific Interpretation

If SCBI improves performance, the interpretation must be:

> The experiment provides evidence that the tested inference-time representation mechanism improves the measured task under the tested conditions.

It must **not** automatically be interpreted as:

> SCBI proves that frozen models can learn.

or:

> SCBI proves a new learning paradigm.

Those claims require substantially stronger evidence.

---

# 95. Novelty Is Not a Definition

Nothing in this document implies that SCBI is novel.

Novelty is determined separately through:

```text
research/README_LITERATURE.md
```

and:

```text
reports/novelty_report.md
```

A mathematically precise definition can still describe an existing method.

---

# 96. Scientific Status Labels

Use the following labels in theory documents:

```text
[FACT]
Supported by established evidence.

[DEFINITION]
Defined by this research.

[HYPOTHESIS]
Testable but unverified.

[CONJECTURE]
Theoretical claim without proof.

[PROPOSITION]
Mathematical statement supported by derivation.

[THEOREM]
Mathematical statement with a valid proof.

[OBSERVATION]
Direct experimental observation.

[INTERPRETATION]
Explanation inferred from evidence.

[OPEN]
Not yet resolved.
```

---

# 97. Current Definition Status

At the current stage:

```text
θ                       = FIXED
x                       = FIXED
y                       = FIXED
fθ                      = FIXED
h_t                     = WORKING
z_t                     = WORKING
B_t                     = WORKING / OPEN
candidate                = WORKING
candidate generation     = WORKING
candidate evaluation     = WORKING
self-consistency         = OPEN
acceptance               = WORKING
representation update    = WORKING
state update             = WORKING
inference budget         = WORKING
SCBI core definition     = PROVISIONAL
```

These statuses must be updated as the research progresses.

---

# 98. Final Definition Principle

The most important rule is:

> **Never allow the implementation to define the science after the fact.**

The research must first define what is being tested.

Then implementation should instantiate that definition.

Then experiments should test it.

Then results should determine whether the definition and hypothesis survive.

---

# 99. Final Scientific Standard

SCBI should eventually be expressible in one precise sentence:

> **SCBI is a formally specified inference-time procedure that operates with frozen foundation-model parameters and dynamically constructs, evaluates, and selects temporary representation/state configurations according to a predefined objective, with its scientific value determined by controlled comparison against existing inference-time methods.**

If this sentence cannot be made mathematically precise, the theory is not yet complete.

---

# 100. Source of Truth

When conflicts exist:

```text
theory/README_DEFINITIONS.md
```

is the authoritative source for terminology.

Any conflicting definition elsewhere must either:

1. be corrected, or
2. explicitly identify itself as a variant.

No implementation file, experiment notebook, prompt, or agent-generated note may silently override this document.

---

# 101. Non-Negotiable Rules

1. Never silently redefine \(B_t\).
2. Never silently redefine \(z_t\).
3. Never silently redefine self-consistency.
4. Never modify \(\theta\) in core SCBI.
5. Never use target information without declaring it.
6. Never hide external evaluators.
7. Never hide additional compute.
8. Never call an activation a basis without justification.
9. Never call an existing optimization procedure novel without prior-art analysis.
10. Never convert an empirical observation into a theorem.
11. Never convert a hypothesis into a fact.
12. Never remove failed definitions from research history.
13. Record all major definition changes.
14. Keep variants separate from core SCBI.
15. Preserve mathematical precision over implementation convenience.

---

# 102. Final Principle

> **Definitions must constrain the experiment, not be rewritten to fit the experiment.**

The purpose of this document is to ensure that when SCBI eventually produces a result—positive, negative, mixed, or equivalent to prior work—the result can be traced back to a clearly defined scientific object.

That is the standard required for the remainder of the research.

---

# 103. Formal Definition: Candidate Identifiability ($H_A$) vs. Candidate Usefulness ($H_B$)

### Status: Fixed (Post-EXP013 Consensus)

End-to-end SCBI decomposes into two independent formal propositions:

### 103.1 Hypothesis $H_A$ (Candidate Identifiability)
$$\boxed{\exists E \in \mathcal{E}: \quad \mathbb{E}_{x \sim \mathcal{D}} [M(f_\theta(x; P_E))] > \mathbb{E}_{x \sim \mathcal{D}, P \sim \text{Uniform}(\mathcal{G}(x))} [M(f_\theta(x; P))]}$$
*Interpretation:* A candidate representation evaluator possesses identifiability if and only if it selects interventions whose expected performance strictly exceeds uniform random selection within the admissible candidate set $\mathcal{G}(x)$.

### 103.2 Hypothesis $H_B$ (Candidate Usefulness / Headroom)
$$\boxed{\exists P \in \mathcal{G}(x): \quad \mathbb{E}_{x \sim \mathcal{D}} [M(f_\theta(x; P))] > \mathbb{E}_{x \sim \mathcal{D}} [M(f_\theta(x; I))]}$$
*Interpretation:* An intervention candidate generator produces useful candidates if and only if the Oracle upper bound across the candidate pool strictly exceeds the performance of the unmodified frozen foundation model ($M(I)$).

### 103.3 Conjunction for End-to-End SCBI
$$\boxed{H_{\mathrm{SCBI}} \iff H_A \land H_B}$$
End-to-end inference improvement requires both that useful representations exist in $\mathcal{G}(x)$ ($H_B$) and that the label-free evaluator $E$ successfully identifies them ($H_A$).

---

# 104. Formal Definition: Relative Selection Ability vs. Absolute Intervention Usefulness

### Status: Fixed

Let $\mathcal{G}(x) = \{P_1, \dots, P_K\}$ be the candidate pool for instance $x$.

### 104.1 Relative Selection Ability
An evaluator $E$ exhibits relative selection ability if:
$$M(E) - M(\mathrm{Random}) > 0$$
and recovers a strictly positive fraction of the candidate pool spread:
$$R_E = \frac{M(E) - M(\mathrm{Random})}{M(\mathrm{Oracle}) - M(\mathrm{Random})} > 0.$$
Relative selection ability evaluates the internal ranking quality of $E$ within the space of candidate representations $\mathcal{G}(x)$.

### 104.2 Absolute Intervention Usefulness
An intervention $P$ exhibits absolute usefulness if:
$$M(P) - M(\mathrm{Identity}) > 0.$$
Absolute usefulness evaluates whether the intervention produces a net improvement on the downstream foundation model relative to no intervention.

$$\boxed{\text{Relative Selection Ability } \nRightarrow \text{ Absolute Intervention Usefulness.}}$$
An evaluator may possess high relative selection ability within an intrinsically destructive candidate pool ($M(P_k) < M(I) \, \forall k$).

---

# 105. Formal Definition: Temporary Representation Transformation Operators

### Status: Working (Generalizing Basis Projections)

Let $H_l \in \mathbb{R}^{T \times d}$ denote residual hidden representations at layer $l$.

### 105.1 Orthogonal Basis Projection Operator
$$P_V = I - V V^\top, \quad V \in \mathbb{R}^{d \times r}, \quad V^\top V = I_r$$
Satisfies idempotency ($P^2 = P$) and symmetry ($P^\top = P$).

### 105.2 Continuous Gating / Contraction Operator
$$P_\alpha = I - \alpha V V^\top, \quad \alpha \in [0, 1]$$
For $\alpha \in (0, 1)$, $P_\alpha$ is non-idempotent ($P_\alpha^2 \neq P_\alpha$). It represents a symmetric linear contraction operator that scales down activation energy along subspace $V$ by factor $(1 - \alpha)$ while preserving orthogonal directions.

SCBI encompasses all temporary inference-time representation transformation operators $T \in \mathcal{T}$ acting on $H_l$, without requiring strict idempotency.

---

# 106. Formal Definition: Dual-Channel Evaluation Metrics ($M_{\mathrm{LM}}$ vs. $M_{\mathrm{contrast}}$)

### Status: Fixed

1. **Next-Token Accuracy ($M_{\mathrm{LM}}$):**
   $$M_{\mathrm{LM}} = \mathbb{I}\left[\arg\max_{w \in \mathcal{V}} P(w \mid x, T) = y_{\mathrm{target}}\right]$$
   Measures unconstrained greedy next-token prediction correctness, assessing general language modeling fluency and task completion.

2. **Contrastive Preference Margin ($M_{\mathrm{contrast}}$):**
   $$M_{\mathrm{contrast}} = \mathbb{I}\left[P(y_{\mathrm{target}} \mid x, T) > P(y_{\mathrm{distractor}} \mid x, T)\right]$$
   Measures targeted semantic discrimination against the explicit task distractor.

