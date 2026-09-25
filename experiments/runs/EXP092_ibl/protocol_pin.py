"""EXP092 signed-protocol pin.

The runner refuses to execute unless the SIGNED protocol exists at the
recorded path with the recorded SHA-256 digest (Law #4: signed protocols are
immutable; a digest mismatch means the protocol file differs from the signed
version and nothing is licensed).
"""

import os

# Signed at LOG-4325 on the binding independent Law #14 SIGN (re-verification
# addendum). Computed over experiments/protocols/EXP092_IBL_PREREG_SIGNED.md.
SIGNED_PROTOCOL_DIGEST = (
    "75e744ad9bae98cc86c0443823bd27b197a9c17fc106ba984e5870cf1bdb347c")

# Bench pin (EXP092-B), registered in the signed protocol §2/§6 G0.
BENCH_PIN = (
    "9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4")

# Weights pin (LOG-331; relocated snapshot integrity confirmed at LOG-4321).
WEIGHTS_PIN = (
    "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed")


def _repo_root():
    # Bundle lives at experiments/runs/EXP092_ibl/; repo root is 3 up.
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "..", "..", ".."))


def signed_protocol_path():
    return os.path.join(_repo_root(), "experiments", "protocols",
                        "EXP092_IBL_PREREG_SIGNED.md")
