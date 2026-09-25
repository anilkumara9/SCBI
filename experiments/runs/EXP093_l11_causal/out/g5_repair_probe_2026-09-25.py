"""LOG-4349 repair verification: run the REAL G5 probe (inject.verify_g5_real)
against the frozen LOG-331 Pythia-410m snapshot — the exact probe that failed
at LOG-4349 with rel_err = 1.0.

Read-only weights, torch.no_grad, G1 pre/post state-dict hash pinning (Δθ=0).
Does NOT run the decision loop or scoring — probe only. No writes to the repo.
"""
import os
import sys

BUNDLE = "/home/hatch/workspace/SCBI/experiments/runs/EXP093_l11_causal"
sys.path.insert(0, BUNDLE)
sys.path.append("/home/hatch/workspace/SCBI/experiments/runs/EXP092_ibl")

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import protocol_pin as pin
import run_exp093
from run_exp093 import compute_state_dict_hash
from inject import verify_g5_real, ALPHA, G5_REL_TOL, RunInvalid

torch.set_num_threads(pin.THREAD_PIN)
assert torch.get_num_threads() == pin.THREAD_PIN

# Bench + directions (read-only npz), same as the real runner
bench, _ = run_exp093.guard_g0_bench()
d = run_exp093.guard_g2_directions(
    pin.npz_path(), [b["ent"] for b in bench])
v = d["v"].astype(np.float64)
print(f"[probe] bench: {len(bench)} items; v[0] norm={np.linalg.norm(v[0]):.6f}",
      flush=True)

snapshot = pin.SNAPSHOT_DIR
tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    snapshot, local_files_only=True, torch_dtype=torch.float32,
    device_map="cpu")
model.eval()
model.requires_grad_(False)

pre = compute_state_dict_hash(
    {k: v_.detach().cpu() for k, v_ in model.state_dict().items()})
print(f"[probe] G1 pre-hash: {pre[:16]}… pin={pin.WEIGHTS_PIN[:16]}…", flush=True)
assert pre == pin.WEIGHTS_PIN, "G1 pre-hash mismatch — Δθ=0 NOT verified"

g5 = verify_g5_real(model, tokenizer, bench[0]["prompt"], v[0], ALPHA)
print(f"[probe] G5 gate={g5['gate']} "
      f"criterion_i_rel_err={g5['criterion_i_rel_err']:.3e} "
      f"criterion_ii_max_abs={g5['criterion_ii_max_abs_change']:.3e} "
      f"criterion_iii_bit_match={g5['criterion_iii_bit_match']}", flush=True)
assert g5["criterion_i_rel_err"] <= G5_REL_TOL, "criterion (i) FAILED"

post = compute_state_dict_hash(
    {k: v_.detach().cpu() for k, v_ in model.state_dict().items()})
print(f"[probe] G1 post-hash match: {post == pre} (Δθ=0)", flush=True)
assert post == pre, "weights changed during probe!"
print("[probe] REAL-PATH G5 PROBE: PASS", flush=True)
