"""EXP091 embedding extraction — frozen Pythia-410m, layer 20, CPU, read-only.

Signed protocol: experiments/protocols/EXP091_CLM8B_ADAPTATION_V3_PREREG_SIGNED.md
(§6 repaired bench contract + provenance pin; guards G1'/G2/G3; Law #13
determinism pins).

Guards (all FATAL → RUN-INVALID, SystemExit):
  G1': every A/C occurrence in every constructed prompt must be covered by
      exactly one token, VERIFIED BY EXECUTING THE REAL TOKENIZER — never by
      word-commonness reasoning (§8 standing rule). Two enforcement points:
      (i) at extraction startup, the benchmark builder runs the real tokenizer
      over all 60 built prompts (offset-mapping cover check) and fails loud
      if any entity span is multi-token; (ii) the executor asserts
      encode(" "+A) and encode(" "+C) are each exactly one token (this is the
      embedded material, per the §0 action-text coupling). Any multi-token
      entity → RUN-INVALID; items are NOT silently dropped.
  G2: state_dict SHA-256 before AND after extraction must equal the LOG-331
      snapshot hash → Δθ=0 verified. Mismatch → RUN-INVALID.
  G3: phrasing-balance assert — exactly 30 A-first / 30 C-first (delegated to
      benchmark_exp091.assert_phrasing_balance).
  §6 provenance pin: SHA-256 of exp077_instance_records.json must equal
      47281cd3…0585 (mismatch → RUN-INVALID). The archive is pinned as the
      provenance record, NOT as the item source (caveat 6). The EXP089
      byte-for-value reproduction guard is STRUCK and does not exist here.

Action texts (§6, §0 coupling accepted by Law #14 at LOG-356): the entity in
its natural single-token BPE form, " "+A / " "+C. The bare form fragments
("Mars" → 2 tokens) and was never coherently embeddable.

torch / transformers are imported LAZILY (inside functions) so this module
imports on machines without them. --mock mode needs only numpy and never
touches weights; it re-verifies the build-time G1' artifact
(g1prime_verification.json) rather than executing the tokenizer.

Real execution requires --ceo-clearance (enforced by run_exp091.py); this
module exposes extract_real() / extract_mock() for the runner.
"""

import argparse
import hashlib
import json
import os
import sys

import numpy as np

import benchmark_exp091
from benchmark_exp091 import (
    ALL_ENTITIES, action_text_of, assert_archive_hash,
    assert_phrasing_balance, build_benchmark, check_g1prime_artifact,
    state_text_of, verify_g1_prime,
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
    # Bundle lives at experiments/runs/EXP091_clm8b_falsifier_v3/; repo root is 3 up.
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


def guard_archive_provenance():
    """§6 provenance pin: the archive hash must match the §6-recorded hash."""
    try:
        return assert_archive_hash()
    except benchmark_exp091.RunInvalid as e:
        raise RunInvalid(str(e))


def check_single_token_entity(encode_fn, name, role):
    """G1 (legacy, EXP075/EXP090): entity must tokenize to exactly one token.

    Retained for unit-test coverage of the guard lineage; EXP091's registered
    guard is G1' (verify_g1_prime + the spaced-entity assert below).
    """
    ids = encode_fn(name)
    if len(ids) != 1:
        raise RunInvalid(
            f"G1 FAIL: {role} entity {name!r} tokenizes to {len(ids)} tokens "
            f"— RUN-INVALID (items are NOT silently dropped).")
    return ids[0]


def guard_g1_prime_action_texts(encode_fn):
    """G1' enforcement point (ii): the embedded material — " "+A / " "+C for
    every bench entity — must each encode to exactly one token.

    Enforcement point (i) (offset-mapping cover check over all 60 built
    prompts) is executed by verify_g1_prime() at extraction startup, before
    this. Any failure → RUN-INVALID.
    """
    token_ids = {}
    for name in ALL_ENTITIES:
        txt = action_text_of(name)
        ids = encode_fn(txt)
        if len(ids) != 1:
            raise RunInvalid(
                f"G1' FAIL: action text {txt!r} tokenizes to {len(ids)} tokens "
                f"— RUN-INVALID (items are NOT silently dropped).")
        token_ids[name] = ids[0]
    return token_ids


def extract_mock(out_dir):
    """Synthetic extraction: seeded unit vectors, no weights touched.

    Used by --mock runs and unit tests. G2 is skipped (no weights);
    G1'/G3 are asserted on the real benchmark builder. The §6 provenance pin
    is asserted (it is a file check — cheap and weight-free — so mock makes
    no weaker claim than real mode here). The build-time G1' verification
    artifact (real-tokenizer execution over all 60 prompts, recorded at build
    time) is re-verified for presence, internal consistency (240/240), and
    binding to the current builder output.
    """
    guard_archive_provenance()
    bench = build_benchmark()
    assert_phrasing_balance(bench)
    try:
        g1prime = check_g1prime_artifact()
    except benchmark_exp091.RunInvalid as e:
        raise RunInvalid(str(e))
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
    emb_path = os.path.join(out_dir, "exp091_embeddings.npz")
    np.savez(emb_path, state=state, actA=actA, actC=actC,
             ids=np.array([b["id"] for b in bench]),
             phrasing=np.array([b["phrasing"] for b in bench]))
    meta = {
        "mode": "mock",
        "n": n,
        "dim": MOCK_DIM,
        "seed": MOCK_SEED,
        "G1'": ("pass (build-time real-tokenizer verification artifact "
                "re-verified: 240/240 in-prompt occurrences single-token, "
                "bound to current bench hash; mock entities are single "
                "abstract tokens)"),
        "G2": "skipped (no weights in mock mode)",
        "G3": "pass (30/30 asserted on real benchmark builder)",
        "provenance_pin": "pass (§6 archive hash asserted)",
        "embeddings": os.path.basename(emb_path),
    }
    with open(os.path.join(out_dir, "exp091_extraction_meta.json"), "w") as f:
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

    # §6 provenance pin BEFORE any weight access (mismatch → RUN-INVALID).
    guard_archive_provenance()
    log("[extract] §6 provenance pin OK: exp077_instance_records.json hash "
        "matches the recorded archive.")

    log(f"[extract] loading frozen snapshot: {snap}")
    tokenizer = AutoTokenizer.from_pretrained(snap, local_files_only=True)

    # G1' enforcement point (i): execute the real tokenizer over all 60 built
    # prompts (offset-mapping cover check) BEFORE any weight access.
    g1prime_table = verify_g1_prime(tokenizer)
    n_occ = sum(v["occurrences"] for v in g1prime_table.values())
    log(f"[extract] G1'(i) pass: {n_occ}/240 A/C occurrences single-token "
        f"in-prompt (real tokenizer, offset-mapping cover check).")

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
    assert_phrasing_balance(bench)
    log("[extract] benchmark verified: 60 items, G3 30/30, provenance pinned.")

    def encode_ids(text):
        return tokenizer.encode(text, add_special_tokens=False)

    # G1' enforcement point (ii): the embedded material (" "+A / " "+C) must
    # each be exactly one token.
    action_token_ids = guard_g1_prime_action_texts(encode_ids)
    log("[extract] G1'(ii) pass: all 10 action texts (' '+entity) single-token: "
        + ", ".join(f"{n}={i}" for n, i in sorted(action_token_ids.items())) + ".")

    states, actsA, actsC = [], [], []
    with torch.no_grad():              # Law #13 pin: no_grad around ALL extraction
        for b in bench:
            s_txt = state_text_of(b["prompt"])
            # State text: premise sentences. Action texts: the entity's natural
            # single-token BPE form (" "+A / " "+C) — §0 coupling.
            for txt, store in ((s_txt, states),
                               (action_text_of(b["A"]), actsA),
                               (action_text_of(b["C"]), actsC)):
                ids = torch.tensor([encode_ids(txt)], dtype=torch.long)
                out = model(ids, output_hidden_states=True)
                # hidden_states[0] = embedding output → index 20 = layer-20 block.
                h = out.hidden_states[LAYER][0, -1, :].detach().cpu().to(torch.float32)
                store.append(h.numpy())
    log("[extract] 180 forward passes complete (60 state + 60 A + 60 C). "
        "Final-token hidden states; action texts in spaced single-token form.")

    # G2 (post): Δθ=0 verified — hash must be unchanged after extraction.
    post_hash = guard_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()}, "post")
    log(f"[extract] G2 post-extraction hash OK: {post_hash[:16]}… (Δθ=0 verified)")

    os.makedirs(out_dir, exist_ok=True)
    emb_path = os.path.join(out_dir, "exp091_embeddings.npz")
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
        "G1'": (f"pass (i: {n_occ}/240 in-prompt occurrences single-token, "
                f"real tokenizer; ii: all 10 action texts single-token)"),
        "G2": f"pass (pre/post hash {pre_hash[:16]}…, Δθ=0 verified)",
        "G3": "pass (30/30 asserted on real benchmark builder)",
        "provenance_pin": "pass (§6 archive hash asserted)",
        "embeddings": os.path.basename(emb_path),
    }
    with open(os.path.join(out_dir, "exp091_extraction_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    with open(os.path.join(out_dir, "exp091_extraction_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    return emb_path, meta


def main(argv=None):
    ap = argparse.ArgumentParser(description="EXP091 embedding extraction")
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
