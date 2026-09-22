---
name: reproducibility
description: Operational checklist and technical standards for ensuring 100% deterministic reproducibility, hardware/environment auditing, artifact tracking, and weight immutability verification.
---

# Reproducibility Skill

This skill provides technical recipes and verification checklists to ensure that every mathematical derivation, software implementation, and empirical run within the **Self-Consistent Basis Invention (SCBI)** project is 100% deterministically reproducible.

**Foundational Documents:**
- [`documentation/researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) §8 (Independent reproduction standards)
- [`documentation/theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §6, §7 (Frozen parameter enforcement)
- **Governing Rule:** [`.agents/rules/04-code.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/04-code.md)

---

## When to Use This Skill

Activate this skill whenever:
- Setting up a new code repository or execution pipeline.
- Running benchmark suites or saving experimental artifacts.
- Packaging an experimental release, checkpoint, or paper supplementary material.
- Verifying whether an experiment can be recreated bit-for-bit on an independent machine.

---

## 1. Deterministic Seeding Protocol

All executable scripts must use the standard deterministic seeding block:

```python
import os
import random
import numpy as np
import torch

def set_deterministic_seed(seed: int = 42) -> None:
    """Sets deterministic seeds across all random number generators and backends."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    
    # Deterministic PyTorch backend operations
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    
    # Set Python hash seed
    os.environ["PYTHONHASHSEED"] = str(seed)
```

---

## 2. Parameter Immutability Audit ($\Delta\theta=0$)

To guarantee that the foundation backbone was not silently fine-tuned during inference:

```python
import hashlib
import torch

def compute_model_parameter_hash(model: torch.nn.Module) -> str:
    """Computes a SHA-256 hash over all model parameters and buffer states."""
    hasher = hashlib.sha256()
    for name, param in sorted(model.named_parameters()):
        hasher.update(name.encode("utf-8"))
        hasher.update(param.detach().cpu().numpy().tobytes())
    for name, buf in sorted(model.named_buffers()):
        hasher.update(name.encode("utf-8"))
        hasher.update(buf.detach().cpu().numpy().tobytes())
    return hasher.hexdigest()
```

Every experiment runner must:
1. Compute `hash_before = compute_model_parameter_hash(model)`.
2. Run full evaluation across test set.
3. Compute `hash_after = compute_model_parameter_hash(model)`.
4. Assert: `assert hash_before == hash_after, "REPRODUCIBILITY VIOLATION: Model weights mutated!"`

---

## 3. Environment & Hardware Manifest

Every experiment output directory must automatically dump an `environment.json` file capturing:
- Python version (`sys.version`)
- PyTorch and CUDA versions (`torch.__version__`, `torch.version.cuda`)
- GPU hardware name (`torch.cuda.get_device_name(0)`)
- Installed package versions (`pip freeze`)
- Git commit hash (`git rev-parse HEAD`)
- Git status / diff (`git diff HEAD`) to catch uncommitted changes

---

## 4. Artifact Logging Hierarchy

Experimental outputs must be saved using the standard directory structure:

```text
runs/
└── [experiment_id]/
    ├── config.yaml            # Complete, unedited hyperparameter config
    ├── environment.json       # System, GPU, pip versions, commit hash
    ├── seeds.json             # List of seeds used and per-seed status
    ├── metrics.json           # Aggregated statistics (mean, std, 95% CI, p-values)
    ├── raw_predictions.jsonl   # Per-instance input, ground truth, baseline & SCBI outputs
    └── weight_checksum.log    # Verified parameter hashes before and after run
```

---

## 5. Pre-Release Reproducibility Checklist

- [ ] All source files are version-controlled with a clean working tree.
- [ ] Dependencies are pinned in `pyproject.toml` / `requirements.txt`.
- [ ] Seed parameter `--seed` is exposed in CLI and logged.
- [ ] Weight checksum validation passed with 100% match.
- [ ] Raw instance-level outputs are preserved for independent re-analysis.
