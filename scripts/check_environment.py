"""
SCBI Environment Verification & Manifest Generator.

Governing Specification: TECHNICAL_STACK.md Section 28, Section 34
"""

import json
import platform
import subprocess
import sys
from typing import Any, Dict


def get_git_commit() -> str:
    """Returns current git commit hash, 'no_commits_yet', or 'not_a_git_repository'."""
    try:
        # Check if inside git repo
        is_git = subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        if is_git == "true":
            try:
                commit = subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
                ).decode("utf-8").strip()
                return commit
            except subprocess.CalledProcessError:
                return "git_initialized_no_commits_yet"
        return "not_a_git_repository"
    except Exception:
        return "not_a_git_repository"


def check_environment() -> Dict[str, Any]:
    """Generates the required Section 34 Environment Manifest."""
    manifest: Dict[str, Any] = {
        "os": platform.platform(),
        "python_version": sys.version.split()[0],
        "pytorch_version": "not_installed",
        "transformers_version": "not_installed",
        "cuda_version": "not_available",
        "gpu": "none",
        "gpu_memory": "0 MB",
        "git_commit": get_git_commit(),
    }

    # PyTorch & CUDA check
    try:
        import torch
        manifest["pytorch_version"] = torch.__version__
        if torch.cuda.is_available():
            manifest["cuda_version"] = torch.version.cuda
            manifest["gpu"] = torch.cuda.get_device_name(0)
            vram_bytes = torch.cuda.get_device_properties(0).total_memory
            manifest["gpu_memory"] = f"{vram_bytes // (1024**2)} MB"
        else:
            manifest["cuda_version"] = "cpu_only"
            manifest["gpu"] = "cpu"
    except ImportError:
        pass

    # Transformers check
    try:
        import transformers
        manifest["transformers_version"] = transformers.__version__
    except ImportError:
        pass

    return manifest


if __name__ == "__main__":
    report = check_environment()
    print("\n=== SCBI ENVIRONMENT REPORT (Section 34) ===")
    print(json.dumps(report, indent=4))
    print("============================================\n")
