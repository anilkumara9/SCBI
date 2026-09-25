#!/usr/bin/env python3
"""EXP087 guards: signed pins, startup crash-guard, frozen-backbone guard,
execution refusal gates.

Implements the signed protocol
experiments/protocols/EXP087_TRANSLATION_SIGNATURE_PREREG_SIGNED.md (LOG-324)
as read through the binding erratum
experiments/protocols/ERRATUM_EXP087_STALE_WATERMARK_2026-09-24.md (LOG-329/330):
the at-signing R5 re-mapping (RUN-INVALID, NOT CONTINUE) is binding; the
retained draft body is superseded wherever it conflicts.

All pins below are copied from the protocol (§1 Law #15 card, §2, §3, §8).
Changing any pin is a design change -> new experiment number (Law #4).
"""

import hashlib
import json
import os
import sys

# ---------------------------------------------------------------------------
# Signed pins
# ---------------------------------------------------------------------------

MODEL_ID = "EleutherAI/pythia-410m"
LAYER_INDEX = 20              # 0-indexed residual stream (program-standard site)
D_MODEL = 1024                # Pythia-410m hidden size
N_ITEMS = 60                  # fixed benchmark size (§3)
ALPHA = 0.5                   # C2 bridge + C3 static scale (§3)
MASTER_SEED = 20260925        # deterministic RNG seed (bundle pin)

# R5 apparatus envelope (§2, §8 item 1 resolved LOG-314; at-signing remap
# LOG-324): between-configuration envelope 0.74921 ± 0.10 — NOT a
# statistical bar.
MU_CENTER = 0.74921
ENVELOPE_HALF = 0.10
ENVELOPE_LO = 0.649
ENVELOPE_HI = 0.849

# Archived reference values (protocol §2, recomputed from
# exp066_instance_evaluations.json at build time and verified):
MU_HAT_ARCH = 0.74921         # archived mean margin shift (C2)
MIN_DM_ARCH = 0.64815         # archived min_i Δm_i
SUP_EPS_ARCH = 0.10106        # archived sup|ε|
R_ARCH = 0.49708              # archived corr(Δm_i, c_i)
R_SORTED_NEG = -0.21388       # sorted-key pairing gives r = -0.21388 (pairing
                              # is load-bearing; §8 item 2)
ARCH_B = 8                    # archived McNemar rescue cell (C2)
ARCH_C = 0                    # archived McNemar corruption cell (C2)

# Headroom gate, carried over from EXP066 (§3): base accuracy in [40%, 70%].
HEADROOM_LO = 0.40
HEADROOM_HI = 0.70

# R4 corr decision rule (§2): PASS = one-sided p < 0.05 for corr > 0.
CORR_P_BAR = 0.05

# §3 guard (iii) gross-apparatus rule — BUILD-LANE RESOLUTION (flagged for
# independent review, see BUILD_NOTES.md): c >= 4 corruptions (half the
# archived rescue signal) means the C2 arm cannot be the registered
# α=0.5 bridge under any translation-compatible noise → RUN-INVALID
# (apparatus). c in {1,2,3} follows the registered R1 row → CONTINUE.
# This quantification is NOT in the signed protocol; the reviewer may re-map.
GROSS_CORRUPTION_BAR = 4


class BundleError(Exception):
    """Loud bundle failure — never silent."""


class RefusalError(Exception):
    """Execution-refusal signal (exit 2)."""


class JoinError(BundleError):
    """Pinned-join failure — FATAL, never silently mis-paired."""


# ---------------------------------------------------------------------------
# Startup crash-guard: runs BEFORE any weight access in every mode.
# ---------------------------------------------------------------------------

REQUIRED_PROTOCOL_FILES = [
    "experiments/protocols/EXP087_TRANSLATION_SIGNATURE_PREREG_SIGNED.md",
    "experiments/protocols/ERRATUM_EXP087_STALE_WATERMARK_2026-09-24.md",
]


def crash_guard(scbi_root):
    """Fail fast and loud if the bundle's preconditions are not met."""
    if sys.version_info < (3, 9):
        raise BundleError(
            f"crash-guard: python >= 3.9 required, found {sys.version}")
    for rel in REQUIRED_PROTOCOL_FILES:
        p = os.path.join(scbi_root, rel)
        if not os.path.isfile(p):
            raise BundleError(f"crash-guard: required file missing: {rel}")
    return True


# ---------------------------------------------------------------------------
# Frozen-backbone guard (Law #6 / Law #13): Δθ = 0.
# ---------------------------------------------------------------------------

def state_dict_sha256(state_dict):
    """SHA-256 over parameters in a fixed (sorted-key) order. Works on
    torch tensors or any object exposing .detach()/.cpu()/.numpy()."""
    h = hashlib.sha256()
    for key in sorted(state_dict.keys()):
        t = state_dict[key]
        try:
            arr = t.detach().cpu().numpy()
        except Exception:
            arr = t
        h.update(key.encode("utf-8"))
        h.update(bytes(str(getattr(arr, "shape", None)).encode("utf-8")))
        try:
            h.update(arr.tobytes())
        except Exception:
            h.update(repr(arr).encode("utf-8"))
    return h.hexdigest()


class FrozenBackboneGuard:
    """Hash the model before and after the run; FATAL on any change."""

    def __init__(self):
        self.pre_hash = None
        self.post_hash = None

    def capture_pre(self, state_dict):
        self.pre_hash = state_dict_sha256(state_dict)
        return self.pre_hash

    def capture_post(self, state_dict):
        self.post_hash = state_dict_sha256(state_dict)
        return self.post_hash

    def verify(self):
        if self.pre_hash is None or self.post_hash is None:
            raise BundleError("Δθ=0 guard: pre/post hash missing — "
                              "cannot verify frozen backbone")
        if self.pre_hash != self.post_hash:
            raise BundleError(
                f"Δθ=0 guard FATAL: backbone changed during run\n"
                f"  pre : {self.pre_hash}\n  post: {self.post_hash}")
        return True


# ---------------------------------------------------------------------------
# Execution refusal gates.
# ---------------------------------------------------------------------------

def require_execution_license(args, log_fn=print):
    """The --execute path (GPU model loop) is licensed ONLY with BOTH
    --bundle-review-signoff AND --ceo-gpu-clearance. Otherwise REFUSE
    with exit 2 — no weights touched, no partial run.

    Presenting these flags without the actual independent Law #14 bundle
    review SIGN and the CEO GPU clearance is a Law #4 violation by the
    operator; the flags are attestations, and the run log records them.
    """
    missing = []
    if not getattr(args, "bundle_review_signoff", False):
        missing.append("--bundle-review-signoff")
    if not getattr(args, "ceo_gpu_clearance", False):
        missing.append("--ceo-gpu-clearance")
    if missing:
        log_fn("REFUSAL: --execute requires " + " and ".join(missing) +
               " — GPU execution NOT licensed (protocol: bundle review + "
               "CEO GPU clearance required). Refusing with exit 2; no "
               "weights touched.")
        raise RefusalError("unlicensed execution refused: "
                           + ", ".join(missing) + " missing")
    log_fn("LICENSE ATTESTED: --bundle-review-signoff and --ceo-gpu-clearance "
           "present. Proceeding to the licensed execution path.")
    return True


def determinism_fingerprint():
    """Record the determinism configuration (§8 item 3 resolution: no second
    seed — the pin is enforced and fingerprinted instead)."""
    fp = {
        "master_seed": MASTER_SEED,
        "second_seed_used": False,
        "rationale": ("determinism pin: C1 is a deterministic forward pass; "
                      "a second seed adds no information and would exceed "
                      "the registered 180-pass budget"),
    }
    try:
        import torch
        fp["torch_version"] = torch.__version__
        fp["cudnn_deterministic"] = torch.backends.cudnn.deterministic
        fp["cudnn_benchmark"] = torch.backends.cudnn.benchmark
    except ImportError:
        fp["torch_version"] = None
    return fp
