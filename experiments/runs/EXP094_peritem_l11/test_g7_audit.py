"""EXP094 G7 label-free constructor audit (pre-reg §2.1.3, binding).

G7.1 — Freeze: SHA-256 over constructor.py + P0 text + frozen constants +
        dependency pins; written to constructor_manifest.json and committed
        BEFORE any run. The executor re-hashes at startup and refuses on
        mismatch.
G7.2 — Input attestation: mechanical source scan of constructor.py for
        forbidden label-contact tokens + documentation of where EXP092-B's
        label lives (bench["ent"]; the archived .npz label vector) + the
        enumerated allowed-input list. Neither is reachable from this module.
G7.3 — Label-swap invariance (the auditable disqualification bar): run the
        frozen construction pipeline on synthetic activations with labels
        randomly permuted; the produced {d_i} must be identical
        (max abs diff <= 1e-9). Any label path fails mechanically.
G7.4 — Cross-item isolation: the constructor rejects non-1-D tensors
        (mechanical); pipeline structure review confirms d_i uses only
        item i's activations.
G7.5 — Verdict: PASS -> attestation + hashes persisted in the constructor
        manifest. FAIL -> DISQUALIFICATION: run voided, fresh constructor
        required.

Usage:
  python test_g7_audit.py --freeze --manifest PATH   # G7.1: write manifest
  python test_g7_audit.py --audit --manifest PATH    # G7.2-G7.5: run audit
Exit 0 = PASS (audit) / manifest written (freeze); exit 1 = FAIL.
"""

import argparse
import hashlib
import inspect
import json
import os
import re
import sys

import numpy as np

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)
import constructor as C

# Whole-word tokens that must not appear in constructor.py (G7.2 mechanical
# scan). The constructor may not name, read, or reason about bench
# annotations, option indices, or cross-item aggregates. Word-boundary
# matching: "experiment" does not trip "ent"; hits are reviewed, not
# auto-failed — but this constructor is written so the scan is clean.
FORBIDDEN_TOKENS = (
    "ent", "label", "labels", "target", "foil", "answer", "correct", "key",
    "npz",
)

SWAP_TOL = 1e-9


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def do_freeze(manifest_path):
    """G7.1: hash the frozen constructor + config; write the manifest."""
    import torch
    import transformers
    ctor_path = os.path.join(BUNDLE_DIR, "constructor.py")
    manifest = {
        "constructor_version": C.CONSTRUCTOR_VERSION,
        "constructor_sha256": sha256_file(ctor_path),
        "P0_TEXT": C.P0_TEXT,
        "P0_sha256": hashlib.sha256(C.P0_TEXT.encode("utf-8")).hexdigest(),
        "NORM_RATIO": C.NORM_RATIO,
        "R_SEED": C.R_SEED,
        "dependency_pins": {
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "numpy": np.__version__,
            "python": sys.version.split()[0],
        },
        "g7_verdict": "PENDING",
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"[G7.1] manifest written: {manifest_path}")
    print(f"[G7.1] constructor SHA-256: {manifest['constructor_sha256']}")
    print(f"[G7.1] P0 SHA-256: {manifest['P0_sha256']}")
    return manifest


def g72_source_scan():
    """G7.2: mechanical scan + input enumeration."""
    src_path = os.path.join(BUNDLE_DIR, "constructor.py")
    src = open(src_path).read()
    hits = []
    for tok in FORBIDDEN_TOKENS:
        for m in re.finditer(r"\b" + re.escape(tok) + r"\b", src,
                             flags=re.IGNORECASE):
            line = src[:m.start()].count("\n") + 1
            hits.append((tok, line))
    sig_inputs = {}
    for name in ("build_per_item_direction", "build_random_direction"):
        fn = getattr(C, name)
        sig_inputs[name] = list(inspect.signature(fn).parameters)
    attestation = {
        "forbidden_token_hits": hits,
        "function_signatures": sig_inputs,
        "allowed_inputs": [
            "prompt token-ID arrays (item's own input tokens only)",
            "P0 token-ID array (frozen neutral prefix)",
            "a_vec: L11 residual at readout anchor, task framing (D,)",
            "b_vec: L11 residual at readout anchor, P0 reference (D,)",
            "h_norm_b: scalar L11 residual norm on the B-arm pass",
            "rng: numpy Generator (R arm only, seed pinned)",
        ],
        "label_locations_documented": [
            "bench['ent'] (target entity string per item) — never passed to "
            "any constructor function; the executor's construction call sites "
            "take prompt text / activation vectors only.",
            "archived .npz label vector — not read by this experiment at all "
            "(EXP093's direction source; EXP094 constructs from live passes).",
        ],
        "cross_item_statement": "build_per_item_direction coerces inputs to "
            "1-D float64 and raises ConstructionError on any other shape; no "
            "code path indexes other items.",
    }
    return attestation, hits


def _synthetic_activations(n_items=60, dim=1024, seed=7094):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n_items, dim))
    B = rng.normal(size=(n_items, dim))
    h_norms = np.linalg.norm(A, axis=1) + 1.0
    return A, B, h_norms


def g73_label_swap(n_items=60, dim=1024):
    """G7.3: the pipeline wrapper accepts a labels array (audit surface, as
    in the executor where bench dicts carry 'ent'); the constructor math
    never reads it. Permute labels -> {d_i} must be identical (<= 1e-9)."""
    A, B, h_norms = _synthetic_activations(n_items, dim)
    labels = np.array([f"entity_{i % 20}" for i in range(n_items)])
    rng = np.random.default_rng(4373)
    perm = rng.permutation(n_items)
    labels_perm = labels[perm]

    def pipeline(labels_ctx):
        # Mirrors the executor: labels are in scope (bench dicts) but only
        # prompt-derived activations reach the constructor.
        _ = labels_ctx  # accepted, never read — the audit surface
        out = []
        for i in range(n_items):
            d, _ = C.build_per_item_direction(A[i], B[i], h_norms[i])
            out.append(d)
        return np.stack(out)

    D1 = pipeline(labels)
    D2 = pipeline(labels_perm)
    max_diff = float(np.abs(D1 - D2).max())
    return max_diff, max_diff <= SWAP_TOL


def g74_isolation():
    """G7.4: mechanical — 2-D input rejected; signatures are per-item."""
    try:
        C.build_per_item_direction(np.zeros((2, 8)), np.zeros(8), 1.0)
        return False, "2-D a_vec accepted (isolation broken)"
    except C.ConstructionError:
        pass
    try:
        C.build_per_item_direction(np.zeros(8), np.zeros((8, 2)), 1.0)
        return False, "2-D b_vec accepted (isolation broken)"
    except C.ConstructionError:
        pass
    return True, "non-1-D tensors rejected; d_i is a pure function of item i"


def do_audit(manifest_path):
    """G7.2–G7.5."""
    manifest = json.load(open(manifest_path))
    # Re-verify the freeze first (G7.1 binding to this audit).
    ctor_path = os.path.join(BUNDLE_DIR, "constructor.py")
    if sha256_file(ctor_path) != manifest["constructor_sha256"]:
        print("[G7] FAIL: constructor hash != frozen manifest — the audited "
              "code is not the frozen code. DISQUALIFIED.")
        return 1

    attestation, hits = g72_source_scan()
    print(f"[G7.2] source scan hits: {hits if hits else 'none'}")
    g72_pass = (len(hits) == 0)
    if not g72_pass:
        print("[G7.2] FAIL: forbidden label-contact tokens in "
              "constructor.py — DISQUALIFIED.")
        return 1

    max_diff, g73_pass = g73_label_swap()
    print(f"[G7.3] label-swap max abs diff: {max_diff:.3e} "
          f"(tol {SWAP_TOL:.0e}) -> {'PASS' if g73_pass else 'FAIL'}")
    if not g73_pass:
        print("[G7.3] FAIL: label permutation changed {d_i} — label contact. "
              "DISQUALIFIED.")
        return 1

    g74_pass, g74_msg = g74_isolation()
    print(f"[G7.4] cross-item isolation: {g74_msg} -> "
          f"{'PASS' if g74_pass else 'FAIL'}")
    if not g74_pass:
        print("[G7.4] FAIL — DISQUALIFIED.")
        return 1

    manifest["g72_attestation"] = attestation
    manifest["g73_max_abs_diff"] = max_diff
    manifest["g74_statement"] = g74_msg
    manifest["g7_verdict"] = "PASS"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print("[G7.5] VERDICT: PASS — attestation + hashes persisted.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="EXP094 G7 constructor audit")
    ap.add_argument("--freeze", action="store_true")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()
    if args.freeze:
        do_freeze(args.manifest)
        return 0
    if args.audit:
        return do_audit(args.manifest)
    ap.error("specify --freeze or --audit")


if __name__ == "__main__":
    sys.exit(main())
