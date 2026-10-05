"""EXP144 shared utilities — bench import, hashes, incremental records.

S7-2 plan: procedural bench rebuild via the COMMITTED EXP092 bench-builder
procedure (imported, not copied — zero transcription drift). All forwards on
GPT-2-small, CPU, $0. Frozen backbone Δθ=0 (Law #6).
"""

import hashlib
import json
import os
import sys

import numpy as np

# Committed EXP092 procedure (read-only reference). The bench is
# tokenizer-independent, so this builder is the S7-2 bench builder.
EXP092_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "EXP092_ibl"))
sys.path.insert(0, EXP092_DIR)
import reference_implementation as ref  # noqa: E402  (committed, read-only)

N_ITEMS = 60
N_LAYERS = 12          # GPT-2-small
THREAD_PIN = 2         # S7-2 §3.1: per EXP093 precedent
PERM_SEED = 20261007   # S7-2 §3.1: pre-registered stratified-permutation seed
ALPHA_B = 0.05 / 12    # Bonferroni, D2 deviation
EFFECT_BAR = 0.10      # 10pp effect bar
PERM_B = 1000
R_MIN_ASSERT = 1e-9    # S0.4: ||r_i|| > 1e-9

RUN_DIR = os.path.dirname(os.path.abspath(__file__))


class RunInvalid(Exception):
    """Guard failure -> RUN-INVALID (withheld, never a verdict)."""


class Inconclusive(Exception):
    """Pre-registered INCONCLUSIVE termination (never a verdict)."""


def build_bench():
    """Procedural bench via the committed EXP092 builder (verbatim procedure)."""
    return ref.build_bench()


def canonical_pin(bench=None):
    """Full 64-hex bench sha256 over the registered canonical serialization."""
    bench = bench if bench is not None else build_bench()
    return ref.bench_sha256(bench)


def guard_g0_bench(bench=None):
    """G0: bench provenance — uniqueness, balance, strata (pin recorded)."""
    bench = bench if bench is not None else build_bench()
    g0 = ref.verify_g0(bench)   # asserts structure/strata; returns dict w/ pin
    return bench, g0


def guard_g2_oracle(pin):
    """G2: re-verify the committed oracle-diagnostic artifact bound to pin.

    The diagnostic is a pure function of the bench items (no tokenizer, no
    weights); the EXP092 build-time artifact therefore applies verbatim to
    the procedurally identical rebuilt bench.
    """
    path = os.path.join(EXP092_DIR, "g2_verification.json")
    if not os.path.isfile(path):
        raise RunInvalid(f"G2 FAIL: artifact not found at {path} — RUN-INVALID.")
    with open(path) as f:
        art = json.load(f)
    if art.get("bench_pin") != pin:
        raise RunInvalid(
            f"G2 FAIL: artifact bench pin {art.get('bench_pin')} != rebuilt "
            f"bench pin {pin} — stale artifact — RUN-INVALID.")
    if art.get("gate") != "PASS" or not (art.get("permutation_p", 0) >= 0.05):
        raise RunInvalid(
            f"G2 FAIL: oracle diagnostic gate={art.get('gate')}, "
            f"p={art.get('permutation_p')} — bench confounded — RUN-INVALID.")
    return art


def compute_state_dict_hash(state_dict):
    """Byte-identical replica of EXP077/EXP091/EXP092 get_hash: sorted keys,
    CPU, float32 bytes."""
    sha = hashlib.sha256()
    for key in sorted(state_dict.keys()):
        arr = np.asarray(state_dict[key], dtype=np.float32)
        sha.update(arr.tobytes())
    return sha.hexdigest()


class JsonlWriter:
    """Append-only per-item record writer (flush after every item)."""

    def __init__(self, path):
        self.path = path
        self._seen = set()
        if os.path.isfile(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            rec = json.loads(line)
                            if "item" in rec:
                                self._seen.add(int(rec["item"]))
                        except ValueError:
                            pass

    def done(self, item):
        return int(item) in self._seen

    def write(self, record):
        with open(self.path, "a") as f:
            f.write(json.dumps(record) + "\n")
            f.flush()
            os.fsync(f.fileno())
        self._seen.add(int(record["item"]))

    def count(self):
        return len(self._seen)
