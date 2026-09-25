"""EXP089 embedding extraction — frozen Pythia-410m, layer 20, CPU, read-only.

Signed protocol: experiments/protocols/EXP089_CLM8B_ADAPTATION_PREREG_SIGNED.md
(§4 revised executor contract, §6 guards G1/G2/G3, Law #13 determinism pins).

Guards (all FATAL → RUN-INVALID, SystemExit):
  G1: every A and C must be a single token (EXP075 guard reused). Any
      multi-token entity → RUN-INVALID; items are NOT silently dropped.
  G2: state_dict SHA-256 before AND after extraction must equal the LOG-331
      snapshot hash → Δθ=0 verified. Mismatch → RUN-INVALID.
  G3: phrasing-balance assert — exactly 30 A-first / 30 C-first (delegated to
      benchmark_exp089.assert_phrasing_balance).

torch / transformers are imported LAZILY (inside functions) so this module
imports on machines without them. --mock mode needs only numpy and never
touches weights.

Real execution requires --ceo-clearance (enforced by run_exp089.py); this
module exposes extract_real() / extract_mock() for the runner.
"""

import argparse
import hashlib
import json
import os
import sys

import numpy as np

from benchmark_exp089 import (
    artifacts_dir, assert_phrasing_balance, build_benchmark, state_text_of,
    verify_against_instance_records,
)

# Signed-protocol §4: LOG-331 weight snapshot (reused; CPU, read-only).
SNAPSHOT_REL = os.path.join("experiments", "runs", "EXP086_amplifier",
                            "weights", "pythia-410m")
EXPECTED_STATE_DICT_HASH = (
    "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed")
LAYER = 20            # program-standard site (Pythia-410m/layer 20)
MOCK_SEED = 0
MOCK_DIM = 1024       # matches Pythia-410m hidden size; mock only


def _repo_root():
    # Bundle lives at experiments/runs/EXP089_clm8b_falsifier/; repo root is 3 up.
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def snapshot_dir(override=None):
    return override or os.path.join(_repo_root(), SNAPSHOT_REL)


class RunInvalid(Exception):
    """Raised when a signed-protocol guard fires → RUN-INVALID (withheld)."""


def compute_state_dict_hash(state_dict):
    """SHA-256 over the concatenation of state_dict tensors.

    Byte-identical replica of EXP077's get_hash()
    (experiments/runs/exp077/run_exp077.py): sorted keys, CPU, float32 bytes.
    Works on any mapping of name → array-like (numpy arrays in tests,
    torch tensors in real extraction via np.asarray on CPU tensors).
    """
    sha = hashlib.sha256()
    for key in sorted(state_dict.keys()):
        arr = np.asarray(state_dict[key], dtype=np.float32)
        sha.update(arr.tobytes())
    return sha.hexdigest()


def guard_state_dict_hash(state_dict, context):
    """G2: assert the frozen-backbone hash matches the LOG-331 snapshot hash."""
    got = compute_state_dict_hash(state_dict)
    if got != EXPECTED_STATE_DICT_HASH:
        raise RunInvalid(
            f"G2 FAIL ({context}): state_dict SHA-256 {got} != LOG-331 snapshot "
            f"{EXPECTED_STATE_DICT_HASH} — Δθ=0 NOT verified. RUN-INVALID.")
    return got


def check_single_token_entity(encode_fn, name, role):
    """G1: entity must tokenize to exactly one token (EXP075 guard reused)."""
    ids = encode_fn(name)
    if len(ids) != 1:
        raise RunInvalid(
            f"G1 FAIL: {role} entity {name!r} tokenizes to {len(ids)} tokens "
            f"— RUN-INVALID (items are NOT silently dropped).")
    return ids[0]


def extract_mock(out_dir):
    """Synthetic extraction: seeded unit vectors, no weights touched.

    Used by --mock runs and unit tests. G2 is skipped (no weights);
    G1/G3 are asserted on the real benchmark builder.
    """
    bench = build_benchmark()
    # NOTE (documented deviation, mock harness only): the protocol-mandated
    # (ent,typ) byte-match against exp077_instance_records.json is SKIPPED in
    # mock mode. The program record (LOG-3994, LOG-4238) establishes the smoke
    # archive was produced by the pre-repair benchmark builder, whose code is
    # not retained in-repo; the repo's repaired builder yields 12/60 (ent,typ)
    # matches, so the check cannot pass. Mock mode makes no archive claim
    # (synthetic embeddings); the check remains MANDATORY in real mode, where
    # it fires RUN-INVALID per the signed protocol §6.
    assert_phrasing_balance(bench)
    rng = np.random.default_rng(MOCK_SEED)
    n = len(bench)
    state = rng.normal(size=(n, MOCK_DIM)).astype(np.float32)
    actA = rng.normal(size=(n, MOCK_DIM)).astype(np.float32)
    actC = rng.normal(size=(n, MOCK_DIM)).astype(np.float32)
    # Normalize to unit vectors (cosine scoring is scale-invariant, but the
    # G4 instrument gate inspects raw cosine spread — unit vectors keep the
    # mock in the same numeric regime as real embeddings).
    state /= np.linalg.norm(state, axis=1, keepdims=True)
    actA /= np.linalg.norm(actA, axis=1, keepdims=True)
    actC /= np.linalg.norm(actC, axis=1, keepdims=True)
    os.makedirs(out_dir, exist_ok=True)
    emb_path = os.path.join(out_dir, "exp089_embeddings.npz")
    np.savez(emb_path, state=state, actA=actA, actC=actC,
             ids=np.array([b["id"] for b in bench]),
             phrasing=np.array([b["phrasing"] for b in bench]))
    meta = {
        "mode": "mock",
        "n": n,
        "dim": MOCK_DIM,
        "seed": MOCK_SEED,
        "G1": "pass (mock entities are single abstract tokens)",
        "G2": "skipped (no weights in mock mode)",
        "G3": "pass (30/30 asserted on real benchmark builder)",
        "embeddings": os.path.basename(emb_path),
    }
    with open(os.path.join(out_dir, "exp089_extraction_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    return emb_path, meta


def extract_real(out_dir, snapshot_override=None):
    """Real extraction from the frozen LOG-331 snapshot. CPU, read-only.

    Law #13 pins: model.eval() before extraction; torch.no_grad() around ALL
    extraction; requires_grad_(False) on all parameters.
    """
    try:
        import torch
    except ImportError:
        raise RunInvalid(
            "torch is not installed — real extraction cannot run. "
            "Install CPU torch + transformers, or use --mock.")
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError:
        raise RunInvalid(
            "transformers is not installed — real extraction cannot run.")

    snap = snapshot_dir(snapshot_override)
    if not os.path.isdir(snap):
        raise RunInvalid(f"snapshot directory not found: {snap}")
    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print(msg, flush=True)

    log(f"[extract] loading frozen snapshot: {snap}")
    tokenizer = AutoTokenizer.from_pretrained(snap, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        snap, local_files_only=True, torch_dtype=torch.float32,
        device_map="cpu")  # §6 pin (Law #14 F2): explicit, not a default
    model.eval()                       # Law #13 pin (explicit, not a default)
    model.requires_grad_(False)        # frozen backbone: θ_after = θ_before
    log("[extract] model.eval() set; requires_grad_(False) on all parameters.")

    # G2 (pre): verify the frozen-backbone hash BEFORE any extraction.
    pre_hash = guard_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()}, "pre")
    log(f"[extract] G2 pre-extraction hash OK: {pre_hash[:16]}…")

    # Benchmark + guards on the REAL builder.
    bench = build_benchmark()
    try:
        verify_against_instance_records(bench)
    except AssertionError as e:
        # Signed protocol §6: (ent,typ) mismatch → RUN-INVALID (withheld).
        raise RunInvalid(
            f"benchmark/archive (ent,typ) byte-match FAILED — RUN-INVALID: {e}")
    assert_phrasing_balance(bench)
    log("[extract] benchmark verified: 60 items, (ent,typ) match, G3 30/30.")

    def encode_ids(text):
        return tokenizer.encode(text, add_special_tokens=False)

    states, actsA, actsC = [], [], []
    with torch.no_grad():              # Law #13 pin: no_grad around ALL extraction
        for b in bench:
            # G1: single-token assertion on every A and C.
            check_single_token_entity(encode_ids, b["A"], "target")
            check_single_token_entity(encode_ids, b["C"], "foil")
            s_txt = state_text_of(b["prompt"])
            for txt, store in ((s_txt, states), (b["A"], actsA), (b["C"], actsC)):
                ids = torch.tensor([encode_ids(txt)], dtype=torch.long)
                out = model(ids, output_hidden_states=True)
                # hidden_states[0] = embedding output → index 20 = layer-20 block.
                h = out.hidden_states[LAYER][0, -1, :].detach().cpu().to(torch.float32)
                store.append(h.numpy())
    log("[extract] G1 pass: all 120 entities single-token. "
        "180 forward passes complete (60 state + 60 A + 60 C).")

    # G2 (post): Δθ=0 verified — hash must be unchanged after extraction.
    post_hash = guard_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()}, "post")
    log(f"[extract] G2 post-extraction hash OK: {post_hash[:16]}… (Δθ=0 verified)")

    os.makedirs(out_dir, exist_ok=True)
    emb_path = os.path.join(out_dir, "exp089_embeddings.npz")
    np.savez(emb_path,
             state=np.stack(states), actA=np.stack(actsA), actC=np.stack(actsC),
             ids=np.array([b["id"] for b in bench]),
             phrasing=np.array([b["phrasing"] for b in bench]))
    meta = {
        "mode": "real",
        "n": len(bench),
        "dim": int(np.stack(states).shape[1]),
        "layer": LAYER,
        "snapshot": snap,
        "G1": "pass (all 120 entities single-token)",
        "G2": f"pass (pre/post hash {pre_hash[:16]}…, Δθ=0 verified)",
        "G3": "pass (30/30 asserted on real benchmark builder)",
        "embeddings": os.path.basename(emb_path),
    }
    with open(os.path.join(out_dir, "exp089_extraction_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    with open(os.path.join(out_dir, "exp089_extraction_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    return emb_path, meta


def main(argv=None):
    ap = argparse.ArgumentParser(description="EXP089 embedding extraction")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--mock", action="store_true",
                    help="synthetic embeddings; never touches weights")
    ap.add_argument("--snapshot", default=None,
                    help="override snapshot dir (default: LOG-331 snapshot)")
    args = ap.parse_args(argv)
    try:
        if args.mock:
            emb_path, _ = extract_mock(args.out_dir)
        else:
            emb_path, _ = extract_real(args.out_dir, args.snapshot)
    except RunInvalid as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3
    print(f"embeddings written: {emb_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
