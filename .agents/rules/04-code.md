# Rule 04: Code Architecture & Implementation Invariants

**Applies to:** All source code, PyTorch/JAX implementations, inference pipelines, test scripts, and benchmark harnesses.  
**Foundational Documents:**
- [`documentation/theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §6, §7 (Frozen Foundation Model & Constraint)
- [`documentation/math.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/math.md) §3–§10 (State, Representation, Transitions)
- [`documentation/README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md) §1 (Definition enforcement in software)

---

## 1. Architectural Modularity

Codebases implementing SCBI must maintain strict modular boundaries separating the frozen backbone from the inference-time basis machinery:

```text
src/
├── backbone/          # Foundation model loaders, frozen wrappers, forward hooks
├── basis/             # Representation objects B_t (projectors, coordinate frames, tokens)
├── engine/            # SCBI loop: Candidate generation, evaluation, selection, state transition
├── evaluation/        # Metrics, compute budget trackers, statistical test harnesses
└── experiments/       # Reproducible execution scripts, CLI entrypoints, configuration configs
```

Cross-layer bleeding (e.g., an evaluation function directly mutating model weights) is strictly prohibited.

---

## 2. Mandatory Frozen-Backbone Runtime Guards

Every inference pipeline executing SCBI must implement automated runtime assertions verifying parameter immutability:

```python
def freeze_and_guard_backbone(model: torch.nn.Module) -> tuple[torch.nn.Module, dict[str, int]]:
    """Freezes all model parameters and computes baseline parameter checksums."""
    model.eval()
    checksums = {}
    for name, param in model.named_parameters():
        param.requires_grad = False
        checksums[name] = hash(param.data.cpu().numpy().tobytes())
    return model, checksums

def verify_backbone_unmodified(model: torch.nn.Module, baseline_checksums: dict[str, int]) -> None:
    """Verifies that no inference step has modified backbone weights."""
    for name, param in model.named_parameters():
        current_hash = hash(param.data.cpu().numpy().tobytes())
        assert current_hash == baseline_checksums[name], (
            f"VIOLATION: Backbone parameter '{name}' was modified during SCBI inference! "
            f"Core SCBI invariant Delta_theta = 0 violated."
        )
```

---

## 3. Transient State Isolation (No Episode Leakage)

1. **Episode Scoping:** State $z_t$ and candidate representations $B_t$ must be strictly encapsulated within the inference context of a single sample $x_i$.
2. **Mandatory State Purge:**
   - Between evaluations of different test instances, all temporary state variables, KV caches, or accumulated representations must be explicitly deleted or reset.
   - Carry-over of state across independent test instances turns the system into an online learning system, which violates the independent inference protocol.

---

## 4. Deterministic Reproducibility Standards

- **Seed Initialization:** Every entrypoint must expose an explicit `--seed` argument setting seeds for `random`, `numpy`, `torch`, and CUDA backends.
- **Config as Code:** All hyperparameter values (iteration count $T$, candidate count $K$, dimension $d$, selection thresholds) must be managed via version-controlled YAML/JSON configs, never hardcoded.
- **Hardware & Metric Logging:** Log wall-clock times (`time.perf_counter()`), peak VRAM (`torch.cuda.max_memory_allocated()`), and FLOP counts per instance.

---

## 5. Software Quality & Testing Requirements

- **Type Annotations:** Comprehensive Python 3.10+ type hints across all modules (`numpy.typing`, `torch.Tensor`, `typing.Protocol`).
- **Unit Testing Suite:**
  - Test that candidate generation $\mathcal{G}$ produces valid shapes in $\mathcal{B}$.
  - Test that candidate evaluation $\mathcal{E}$ handles edge cases (e.g., degenerate representations).
  - Test that candidate selection $\mathcal{S}$ is deterministic under fixed inputs.
  - Test that state transition $\mathcal{T}$ preserves invariant bounds.
