"""
SCBI GPU Environment Verification & Health Check.

Governing Specification: TECHNICAL_STACK.md Section 29
"""

import sys
import torch
import torch.nn as nn


def verify_gpu_stack() -> bool:
    """
    Executes the 7-step GPU environment check from Section 29.
    """
    print("\n--- 29. GPU ENVIRONMENT CHECK ---")

    # 1. CUDA available
    cuda_available = torch.cuda.is_available()
    print(f"1. CUDA Available: {cuda_available}")
    if not cuda_available:
        print("   [INFO] Running on CPU development environment.")
        print("   [INFO] Serious GPU experiments must be dispatched to Tier 1/2 Linux GPU cluster.")
        return False

    # 2. Correct GPU visible
    device_count = torch.cuda.device_count()
    device_name = torch.cuda.get_device_name(0)
    print(f"2. Visible GPU(s): {device_count} -> {device_name}")

    # 3. VRAM available
    total_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    free_mem = torch.cuda.mem_get_info()[0] / (1024**3)
    print(f"3. VRAM: {free_mem:.2f} GB free / {total_mem:.2f} GB total")

    # 4. PyTorch CUDA tensor allocation works
    try:
        x = torch.ones((100, 100), device="cuda")
        y = x @ x
        print("4. PyTorch CUDA tensor execution: PASS")
    except Exception as e:
        print(f"4. PyTorch CUDA tensor execution: FAIL ({e})")
        return False

    # 5. Model load test
    try:
        toy_model = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 10)).to("cuda")
        print("5. GPU model load: PASS")
    except Exception as e:
        print(f"5. GPU model load: FAIL ({e})")
        return False

    # 6. Inference test
    try:
        toy_input = torch.randn(2, 64, device="cuda")
        out = toy_model(toy_input)
        assert out.shape == (2, 10)
        print("6. GPU model inference: PASS")
    except Exception as e:
        print(f"6. GPU model inference: FAIL ({e})")
        return False

    # 7. Hidden-state extraction hook test
    try:
        activations = []
        def hook_fn(module, inp, output):
            activations.append(output)
        
        handle = toy_model[1].register_forward_hook(hook_fn)
        _ = toy_model(toy_input)
        handle.remove()
        assert len(activations) == 1
        print("7. GPU hidden-state extraction hook: PASS")
    except Exception as e:
        print(f"7. GPU hidden-state extraction hook: FAIL ({e})")
        return False

    print("\n--- ALL 7 GPU ENVIRONMENT CHECKS PASSED ---\n")
    return True


if __name__ == "__main__":
    is_gpu_ready = verify_gpu_stack()
    if not is_gpu_ready and "--strict" in sys.argv:
        print("[ERROR] Strict GPU requirement failed. Halting.")
        sys.exit(1)
