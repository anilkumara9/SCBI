# SCBI RESEARCH — TECHNICAL STACK & COMPUTE SETUP

This document defines the technical tools, GPU environments, ML frameworks,
research libraries, experiment infrastructure, and reproducibility requirements
for the SCBI research project.

The stack must support rigorous experimentation with frozen foundation models
and inference-time temporary representation optimization.

==================================================
1. PRIMARY DEVELOPMENT ENVIRONMENT
==================================================

Primary development environment:

- Windows workstation for development
- Python 3.11+ recommended
- VS Code / Google Antigravity
- Git + GitHub
- virtual environment / uv / conda
- Linux-based GPU environment for serious experiments

The local Windows machine is primarily for:

- coding
- debugging
- unit tests
- small experiments
- documentation
- experiment configuration
- data preparation
- visualization

Do NOT assume the local machine has sufficient GPU memory for large-model
experiments.

==================================================
2. GPU COMPUTE STRATEGY
==================================================

GPU compute should be treated as a separate research resource.

Preferred environments, depending on availability and budget:

Tier 1 — Free / low-cost prototyping

- Google Colab
- Kaggle Notebooks
- Lightning AI or equivalent free/limited GPU environments

Tier 2 — Paid / scalable experimentation

- RunPod
- Lambda
- Vast.ai
- cloud GPU instances
- university/research lab GPU servers

Tier 3 — Large-scale research

- dedicated NVIDIA GPU server
- multi-GPU cloud instances
- institutional HPC

The project must NOT depend on one specific provider.

All experiments must be portable.

==================================================
3. GPU TYPES
==================================================

For early SCBI experiments, prioritize GPUs with sufficient VRAM rather
than raw compute alone.

Approximate preference:

8–16 GB VRAM:
    small models / proof-of-concept experiments

16–24 GB VRAM:
    stronger medium-model experiments

24–48 GB VRAM:
    serious single-GPU experiments

48 GB+:
    larger models / larger hidden-state experiments

80 GB:
    large-model research and high-memory experimentation

Multi-GPU:
    only when scientifically necessary.

Do not use multi-GPU simply because it is available.

==================================================
4. CUDA STACK
==================================================

GPU experiments should record:

- NVIDIA GPU model
- VRAM
- CUDA version
- cuDNN version when relevant
- PyTorch version
- Python version
- operating system
- driver version

Every experiment must be reproducible from recorded environment metadata.

Recommended baseline:

Python
PyTorch
CUDA
Hugging Face Transformers
Hugging Face Datasets
Accelerate

Use the CUDA/PyTorch combination appropriate for the selected GPU
environment rather than hard-coding an incompatible version.

==================================================
5. CORE ML FRAMEWORK
==================================================

Primary framework:

PyTorch

Use PyTorch for:

- model inference
- hidden-state extraction
- tensor operations
- representation transformations
- optimization experiments
- gradient-based SCBI variants
- GPU execution
- profiling

SCBI must not modify model parameters unless the experiment is explicitly
testing a non-SCBI baseline.

==================================================
6. FOUNDATION MODEL LIBRARIES
==================================================

Primary model ecosystem:

Hugging Face Transformers

Use it for:

- loading open-weight foundation models
- tokenizer management
- hidden-state extraction
- model configuration
- model generation
- reproducible model versions

Possible research models:

- small language models
- encoder models
- decoder-only language models
- vision models where appropriate

Start with SMALL models.

Do not begin SCBI research with a huge model.

The purpose of the first experiment is to test the mechanism, not maximize
model size.

==================================================
7. MODEL VERSION CONTROL
==================================================

Every experiment must record:

- model name
- model version / revision
- parameter count
- architecture
- tokenizer
- precision
- quantization
- model source
- exact Hugging Face revision when available

Never silently switch models between experiments.

A model change requires a new experiment configuration.

==================================================
8. MODEL PRECISION
==================================================

Supported modes may include:

- FP32
- FP16
- BF16
- INT8
- 4-bit quantization

Default research preference:

FP32 or BF16 where practical.

Quantization may be used to reduce memory, but it must be recorded.

Do not compare:

FP32 baseline

against

4-bit SCBI

and attribute the difference to SCBI.

Baseline and SCBI must use matched precision whenever possible.

==================================================
9. MEMORY OPTIMIZATION
==================================================

For larger models use:

- mixed precision
- BF16
- FP16 where appropriate
- gradient checkpointing when applicable
- activation checkpointing when applicable
- 8-bit / 4-bit loading
- CPU offloading
- device mapping
- batch-size reduction
- sequence-length control

However:

Memory optimization must not alter the scientific definition of SCBI.

==================================================
10. ACCELERATE
==================================================

Hugging Face Accelerate may be used for:

- device placement
- multi-GPU experiments
- mixed precision
- distributed execution
- CPU/GPU offloading

Do not introduce distributed complexity until the single-GPU experiment
is validated.

==================================================
11. DATASETS
==================================================

Use:

Hugging Face Datasets

and/or:

- official dataset releases
- research benchmark repositories
- carefully versioned local datasets

Every experiment must record:

- dataset name
- version
- source
- split
- preprocessing
- filtering
- number of examples
- evaluation protocol

Never modify the test set based on results.

==================================================
12. INITIAL BENCHMARK STRATEGY
==================================================

The first experiments should use tasks that are:

- inexpensive
- reproducible
- objectively measurable
- easy to evaluate
- suitable for representation experiments

Possible categories:

1. classification
2. multiple-choice reasoning
3. language understanding
4. controlled synthetic tasks
5. representation probing tasks

Synthetic tasks are especially useful for mechanism testing because they
allow controlled ground truth and easier causal analysis.

Do not immediately use only large benchmark suites.

==================================================
13. EXPERIMENT TRACKING
==================================================

Use an experiment tracking system.

Possible tools:

- Weights & Biases
- MLflow
- TensorBoard
- local structured JSON/CSV logs

The project should remain functional even if an external tracking service
is unavailable.

Minimum local experiment record:

experiments/runs/<experiment_id>/

containing:

config.json
environment.json
metrics.json
results.json
stdout.log
stderr.log
README.md

==================================================
14. CONFIGURATION
==================================================

Never hard-code experiment parameters inside research code.

Use configuration files.

Recommended:

YAML or JSON

Example:

experiments/configs/EXP003_baseline_vs_scbi.yaml

Record:

model
dataset
seed
batch_size
sequence_length
representation_layer
candidate_count
iterations
objective
temperature
precision
GPU
compute_budget
evaluation_metric

==================================================
15. RANDOMNESS
==================================================

Record all relevant seeds.

At minimum:

Python random seed
NumPy seed
PyTorch seed

When applicable:

CUDA deterministic configuration
data-loader seed
sampling seed

Do not report one lucky run as definitive evidence.

Use multiple seeds when computationally feasible.

==================================================
16. STATISTICS
==================================================

Use:

- NumPy
- SciPy
- pandas
- statsmodels where appropriate

Possible analyses:

- mean
- standard deviation
- confidence intervals
- paired tests
- bootstrap confidence intervals
- effect sizes
- permutation tests
- multiple-comparison correction when necessary

Statistical significance must not be confused with scientific importance.

==================================================
17. VISUALIZATION
==================================================

Use:

- Matplotlib
- optionally Plotly for interactive analysis

Important plots:

- baseline vs SCBI
- performance vs compute
- performance vs candidate count
- performance vs iteration count
- performance vs representation dimension
- stability across seeds
- per-example improvements
- failure rates
- latency
- memory consumption

Every plot must be generated from saved experiment data.

Never manually edit a result to make the graph look better.

==================================================
18. PROFILING
==================================================

Measure actual computational cost.

Possible tools:

PyTorch Profiler
NVIDIA Nsight Systems
nvidia-smi
time/performance timers

Record:

- wall-clock latency
- GPU utilization
- GPU memory
- peak VRAM
- number of model evaluations
- candidate evaluations
- iterations
- FLOPs when measurable
- throughput

SCBI must be compared against compute-matched baselines.

==================================================
19. REPRESENTATION RESEARCH TOOLING
==================================================

SCBI is fundamentally a representation-level research problem.

Useful tooling includes:

PyTorch hooks

for:

- capturing hidden states
- inspecting activations
- injecting temporary transformations
- comparing representations

Potential tools:

- forward hooks
- forward pre-hooks
- activation caching
- tensor projections
- PCA
- SVD
- cosine similarity
- CKA
- representation similarity analysis

These tools are research instruments.

They do NOT automatically define what SCBI means.

==================================================
20. REPRESENTATION STORAGE
==================================================

Do not save enormous activation tensors blindly.

For each representation experiment, carefully decide:

- layer
- token positions
- batch subset
- dimensionality
- precision
- storage format

Possible formats:

- PyTorch tensors
- NumPy arrays
- safetensors

Record the representation metadata.

==================================================
21. SEARCH / OPTIMIZATION
==================================================

SCBI may require candidate search.

Possible methods:

Gradient-free:

- random search
- evolutionary search
- beam search
- coordinate search
- Bayesian optimization
- evolutionary strategies

Gradient-based:

- differentiable transformation optimization
- constrained optimization

Do NOT choose an optimization method because it produces better numbers.

Choose it based on the scientific formulation.

The optimization mechanism must be documented separately from the SCBI
scientific hypothesis.

==================================================
22. BASELINE LIBRARY
==================================================

Build a reusable baseline framework.

At minimum support:

Frozen model baseline

Random representation baseline

No-selection baseline

No-consistency baseline

Compute-matched search baseline

Relevant inference-time optimization baseline

Relevant test-time adaptation baseline

Potentially:

activation steering baseline

prompt optimization baseline

latent optimization baseline

The exact baselines depend on literature findings.

==================================================
23. REPRODUCIBLE ENVIRONMENT
==================================================

Use:

pyproject.toml

and/or:

requirements.txt

and preferably lock dependencies using an appropriate package manager.

Record:

Python version
PyTorch version
Transformers version
Datasets version
CUDA version
GPU
OS
Git commit
configuration hash
model revision
dataset revision

Every important experiment should be traceable to a Git commit.

==================================================
24. GIT
==================================================

Git is mandatory.

Use branches for major research changes.

Recommended:

main
research/*
experiment/*
feature/*

Do not commit:

- huge model weights
- raw datasets
- secrets
- API keys
- generated caches
- temporary GPU files

Use appropriate artifact/model storage when necessary.

==================================================
25. MODEL / DATA ARTIFACT STORAGE
==================================================

Possible tools:

Hugging Face Hub
Weights & Biases Artifacts
DVC
Git LFS
cloud/object storage

Do not put multi-GB model files directly into normal Git history.

==================================================
26. RESEARCH NOTEBOOKS
==================================================

Jupyter notebooks may be used for:

- exploration
- visualization
- debugging
- representation analysis

But notebooks are NOT the authoritative experiment implementation.

Important experiments must eventually have reproducible Python scripts.

Preferred:

experiments/scripts/EXP003_baseline_vs_scbi.py

rather than:

final_experiment.ipynb

==================================================
27. PAPER / RESEARCH WRITING
==================================================

Research writing should use:

Markdown initially

and later:

LaTeX

Possible tools:

Overleaf
local LaTeX
Pandoc

Citation management:

BibTeX

Do not manually invent citations.

Every important literature claim must trace to a real source.

==================================================
28. AUTOMATION
==================================================

Create scripts for:

- environment verification
- GPU verification
- model download
- dataset preparation
- experiment execution
- experiment comparison
- statistical analysis
- plotting
- report generation

Example:

scripts/
├── check_environment.py
├── check_gpu.py
├── run_experiment.py
├── compare_runs.py
├── analyze_results.py
└── generate_report.py

==================================================
29. GPU ENVIRONMENT CHECK
==================================================

Before GPU experiments, automatically verify:

1. CUDA available
2. correct GPU visible
3. VRAM available
4. PyTorch CUDA works
5. model can load
6. inference works
7. hidden-state extraction works

A failed environment check must stop the experiment.

==================================================
30. COLAB / CLOUD PORTABILITY
==================================================

Experiments must be runnable using:

Local GPU

or:

Google Colab

or:

another Linux GPU machine

without rewriting the research code.

The only environment-specific layer should handle:

- device
- paths
- credentials
- storage
- GPU configuration

==================================================
31. COST CONTROL
==================================================

Because GPU resources may be limited:

Stage 1:
CPU/small model correctness

Stage 2:
single-GPU tiny model

Stage 3:
single-GPU medium model

Stage 4:
larger model validation

Stage 5:
expensive scaling experiments

Never spend significant GPU money before the mechanism survives cheap
experiments.

==================================================
32. EXPERIMENT ESCALATION
==================================================

Use this progression:

              ┌───────────────────────┐
              │ Literature validation │
              └───────────┬───────────┘
                          ↓
              ┌───────────────────────┐
              │ Mathematical testing  │
              └───────────┬───────────┘
                          ↓
              ┌───────────────────────┐
              │ Synthetic experiment  │
              └───────────┬───────────┘
                          ↓
              ┌───────────────────────┐
              │ Small foundation model│
              └───────────┬───────────┘
                          ↓
              ┌───────────────────────┐
              │ Medium model          │
              └───────────┬───────────┘
                          ↓
              ┌───────────────────────┐
              │ Larger validation     │
              └───────────────────────┘

If SCBI fails at an earlier stage, investigate before scaling.

==================================================
33. SECURITY
==================================================

Never put credentials in:

- source code
- Git
- experiment configs
- notebooks
- README files

Use environment variables.

Examples:

HF_TOKEN
WANDB_API_KEY

Never expose API keys in experiment logs.

==================================================
34. REQUIRED ENVIRONMENT REPORT
==================================================

Every serious experiment must save:

{
    "python_version": "...",
    "pytorch_version": "...",
    "transformers_version": "...",
    "cuda_version": "...",
    "gpu": "...",
    "gpu_memory": "...",
    "model": "...",
    "model_revision": "...",
    "dataset": "...",
    "dataset_revision": "...",
    "git_commit": "...",
    "seed": "...",
    "config_hash": "..."
}

==================================================
35. RECOMMENDED INITIAL STACK
==================================================

Start with the smallest practical stack:

Python
PyTorch
Transformers
Datasets
Accelerate
NumPy
SciPy
pandas
Matplotlib
scikit-learn
Jupyter
pytest
Git

Optional:

Weights & Biases
MLflow
TensorBoard
PEFT
bitsandbytes
safetensors
PyTorch Profiler

Do NOT install dozens of libraries without a research reason.

==================================================
36. INITIAL HARDWARE TARGET
==================================================

The first SCBI prototype should target:

- 1 NVIDIA GPU
- approximately 16–24 GB VRAM if available
- small open-weight foundation model
- BF16/FP16 if supported
- batch size chosen according to memory
- short/moderate sequence length

The first objective is:

PROVE THE EXPERIMENT PIPELINE WORKS.

Not:

TRAIN THE LARGEST MODEL POSSIBLE.

==================================================
37. RESEARCH SOFTWARE ARCHITECTURE
==================================================

Recommended structure:

scbi/
├── core/
│   ├── episode.py
│   ├── state.py
│   ├── candidate.py
│   └── transition.py
│
├── models/
│   ├── frozen_model.py
│   ├── hooks.py
│   └── verification.py
│
├── representations/
│   ├── basis.py
│   ├── transforms.py
│   └── projections.py
│
├── optimization/
│   ├── generator.py
│   ├── evaluator.py
│   ├── selector.py
│   └── search.py
│
└── baselines/
    ├── frozen.py
    ├── random.py
    ├── no_selection.py
    └── compute_matched.py

This structure is implementation-oriented.

The theory remains authoritative.

==================================================
38. IMPORTANT SCIENTIFIC SEPARATION
==================================================

Separate:

RESEARCH HYPOTHESIS

from:

ALGORITHM

from:

IMPLEMENTATION

from:

INFRASTRUCTURE

from:

EXPERIMENT

from:

RESULT

from:

INTERPRETATION

A GPU library, optimization library, or model framework must never
silently become part of the scientific definition of SCBI.

==================================================
39. FINAL TECHNICAL RULE
==================================================

Use the cheapest, simplest, most reproducible technical stack capable of
testing the current scientific question.

Do not optimize infrastructure before validating the research.

Do not scale GPU usage before validating the mechanism.

Do not select a framework because it produces attractive results.

The purpose of the technical stack is:

REPRODUCIBLE SCIENCE.

Not:

MAXIMUM COMPUTE.
