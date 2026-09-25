"""EXP093 protocol pin.

The pre-registration is SIGNED (LOG-4343, 2026-09-25): the signing ceremony
verified SHA-256(signed file with the 64-char digest value blanked) ==
3e0f269b... (self-referential digest convention, signature-block rule) and
SHA-256(reviewed draft content) == 33434fe3... (cross-check). Both digests
were re-verified independently by the bundle build before stamping.
Real execution additionally requires independent bundle review + CEO
clearance (the runner refuses without --ceo-clearance).
"""

import os

# Signed protocol digest (LOG-4343 signing ceremony).
SIGNED_PROTOCOL_DIGEST = (
    "3e0f269b9f2c5170d2b6ed37b2bd03f39f8eeb344914e8bb1f904709ad13db93")

# Bench pin (EXP092-B), registered in the draft §2 / §6 G0 (byte-identical).
BENCH_PIN = (
    "9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4")

# Weights pin (LOG-331; relocated snapshot integrity confirmed at LOG-4321).
WEIGHTS_PIN = (
    "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed")

# Relocated LOG-331 snapshot (integrity confirmed at LOG-4321).
SNAPSHOT_DIR = "/home/hatch/workspace/.exp086_weights/pythia-410m"

# Archived EXP092 embeddings (read-only direction source, draft §3.1).
NPZ_PATH = os.path.join("experiments", "runs", "EXP092_ibl", "out",
                         "exp092_embeddings.npz")

# torch intra-op thread pin (draft F8). EXP092 did not pin explicitly, so its
# extraction ran at the machine default (nproc=2 on this host); the bundle
# pins 2 explicitly, records it in run meta, and asserts it before condition B.
THREAD_PIN = 2


def _repo_root():
    # Bundle lives at experiments/runs/EXP093_l11_causal/; repo root is 3 up.
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "..", "..", ".."))


def signed_protocol_path():
    return os.path.join(_repo_root(), "experiments", "protocols",
                        "EXP093_L11_CAUSAL_PREREG_SIGNED.md")


def draft_protocol_path():
    return os.path.join(_repo_root(), "experiments", "protocols",
                        "EXP093_L11_CAUSAL_PREREG_DRAFT.md")


def npz_path():
    return os.path.join(_repo_root(), *NPZ_PATH.split(os.sep))
