"""EXP145 shared utilities — bench import, hashes, incremental records.

S7-2b plan (SIGNED, LOG-4921): the bench is loaded from the PINNED S7-2b
JSON (S5-INV precedent — the single licensed execution-side change vs the
EXP144 bundle; §7). The pin is asserted character-identical at S0.1, and
S0.1a re-runs the committed derivation procedure as a cross-check
(Law #14 fix 3). All forwards on GPT-2-small, CPU, $0. Frozen backbone
Δθ=0 (Law #6).
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

# --- S7-2b pins (signed plan §0/§4; Law #14 character-verified) ----------------
S72B_BENCH_PATH = os.path.expanduser(
    "~/workspace/SCBI/research/analysis_plans/S7-2b_BENCH_2026-10-05.json")
S72B_PIN = ("b9eac3893ddfbc67400a5d2b5cbb694ba81308471caf4a150476227065e56545")
S72B_DERIVATION_SCRIPT = os.path.expanduser(
    "~/workspace/SCBI/research/analysis_plans/S7-2b_build_bench_2026-10-05.py")
S72B_MANIFEST_PATH = os.path.expanduser(
    "~/workspace/SCBI/research/analysis_plans/"
    "S7-2b_BENCH_MANIFEST_2026-10-05.json")
S72B_MODEL_REV = "607a30d783dfa663caf39e06633721c8d4cfcd7e"  # S0.2 expected


class RunInvalid(Exception):
    """Guard failure -> RUN-INVALID (withheld, never a verdict)."""


class Inconclusive(Exception):
    """Pre-registered INCONCLUSIVE termination (never a verdict)."""


def build_bench():
    """S7-2b bench: load the PINNED bench JSON (S5-INV precedent).

    This is the single licensed execution-side change vs the EXP144 bundle
    (S7-2b §7): the committed EXP092 builder output is replaced by the
    pinned S7-2b JSON. The pin is asserted character-identical at S0.1;
    S0.1a cross-checks the committed derivation procedure.
    """
    with open(S72B_BENCH_PATH) as f:
        bench = json.load(f)
    if not isinstance(bench, list) or len(bench) != N_ITEMS:
        raise RunInvalid(
            f"bench JSON malformed: expected list of {N_ITEMS} items — "
            f"RUN-INVALID.")
    return bench


def canonical_pin(bench=None):
    """Full 64-hex bench sha256 over the registered canonical serialization."""
    bench = bench if bench is not None else build_bench()
    return ref.bench_sha256(bench)


def guard_g0_bench(bench=None):
    """G0: bench provenance — uniqueness, balance, strata (pin recorded)."""
    bench = bench if bench is not None else build_bench()
    g0 = ref.verify_g0(bench)   # asserts structure/strata; returns dict w/ pin
    return bench, g0


def guard_s01a_procedural_crosscheck(pin):
    """S0.1a (Law #14 fix 3, required hardening): re-run the committed
    derivation procedure (build_bench_s72b + ref.bench_sha256 — NOT the
    artifact-writing main()) and require its pin to equal the loaded JSON's
    pin. Any mismatch → RUN-INVALID."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "s72b_derivation", S72B_DERIVATION_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # module-level asserts run; main() guarded
    proc_pin = ref.bench_sha256(mod.build_bench_s72b())
    if proc_pin != pin:
        raise RunInvalid(
            f"S0.1a FAIL: procedural pin {proc_pin} != loaded JSON pin "
            f"{pin} — RUN-INVALID.")
    return proc_pin


def guard_g2_oracle(pin):
    """G2 for S7-2b: re-bind the derivation-time diagnostic to the new pin.

    The committed EXP092 g2_verification.json is bound to the committed pin
    (9be816…); S7-2b's derivation diagnostic is bit-identical to it (pure
    label swap preserves set-overlap structure — verified in derivation and
    independently by the Law #14 reviewer) and is bound here to the new pin
    per S7-2b §7.
    """
    with open(S72B_MANIFEST_PATH) as f:
        man = json.load(f)
    if man.get("bench_sha256") != pin:
        raise RunInvalid(
            f"G2 FAIL: derivation manifest pin {man.get('bench_sha256')} != "
            f"S0.1 pin {pin} — RUN-INVALID.")
    art_path = os.path.join(EXP092_DIR, "g2_verification.json")
    if not os.path.isfile(art_path):
        raise RunInvalid(
            f"G2 FAIL: committed artifact not found at {art_path} — "
            f"RUN-INVALID.")
    with open(art_path) as f:
        art = json.load(f)
    if not (man["g2_oracle_accuracy"] == art["oracle_accuracy"]
            and man["g2_permutation_p"] == art["permutation_p"]):
        raise RunInvalid(
            "G2 FAIL: derivation diagnostic not bit-identical to the "
            "committed EXP092 diagnostic — RUN-INVALID.")
    if art.get("gate") != "PASS" or not (man["g2_permutation_p"] >= 0.05):
        raise RunInvalid(
            f"G2 FAIL: oracle diagnostic gate={art.get('gate')}, "
            f"p={man['g2_permutation_p']} — bench confounded — RUN-INVALID.")
    return {"oracle_accuracy": man["g2_oracle_accuracy"],
            "permutation_p": man["g2_permutation_p"], "gate": "PASS"}


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
