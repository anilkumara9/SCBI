"""EXP092 embedding extraction — frozen Pythia-410m, all 24 layers, CPU, read-only.

Signed protocol: experiments/protocols/EXP092_IBL_PREREG_SIGNED.md
(§2 bench + provenance pin; guards G0/G1/G1'/G2/G3; Law #13 determinism pins).

Guards (all FATAL -> RUN-INVALID):
  G0: bench SHA-256 over the registered canonical serialization must equal
      the registered pin; 60/60 unique (domain,tuple); 20/20 targets at 3x;
      30/30 A-first/C-first; strata == §4 table. (reference_implementation.
      verify_g0 with the registered pin.)
  G1: state_dict SHA-256 (sorted keys, float32 bytes — the EXP077/EXP091
      compute_state_dict_hash procedure) must equal the LOG-331 pin
      ec276abe…f47fc4 — checked pre- AND post-extraction (Δθ=0).
  G1': real-tokenizer offset-mapping cover check over all 60 prompts BEFORE
      any weight access (240/240 single-token in-prompt); in mock mode the
      build-time artifact is re-verified (bound to the bench pin).
  G2: build-time oracle diagnostic artifact (oracle 0.0607, p >= 0.05)
      re-verified at extraction startup, bound to the bench pin. The
      diagnostic itself runs at build time per the signed protocol §6.
  G3: phrasing-balance assert — exactly 30 A-first / 30 C-first.

LAUNCH-CHAIN GATE (LOG-4329 FIX 1): the standalone module CLI enforces the
signed protocol's launch chain — non-mock extraction requires
--ceo-clearance and refuses with exit 2 otherwise (mirrors run_exp092.py).
run_exp092.py is the designated licensed entry point; this module CLI is a
second entry point and must not bypass clearance.

What is extracted per prompt: final-token hidden states at all 24 layers
(hidden_states[1..24]) + final-token logits over the vocabulary (for the S2
LM log-prob baseline; only the two option-token logits are stored).

torch / transformers are imported LAZILY (inside functions) so this module
imports on machines without them. --mock mode needs only numpy and never
touches weights.
"""

import argparse
import hashlib
import json
import os
import sys

import numpy as np

import reference_implementation as ref
from protocol_pin import BENCH_PIN, WEIGHTS_PIN
import g1prime

N_LAYERS = 24
N_ITEMS = 60
MOCK_SEED = 92092
MOCK_DIM = 1024          # matches Pythia-410m hidden size; mock only
G2_ARTIFACT = "g2_verification.json"

# Relocated LOG-331 snapshot (integrity confirmed at LOG-4321).
SNAPSHOT_DIR = "/home/hatch/workspace/.exp086_weights/pythia-410m"


class RunInvalid(Exception):
    """Raised when a signed-protocol guard fires -> RUN-INVALID (withheld)."""


def compute_state_dict_hash(state_dict):
    """SHA-256 over the concatenation of state_dict tensors.

    Byte-identical replica of EXP077's get_hash() / EXP091's
    compute_state_dict_hash: sorted keys, CPU, float32 bytes. Works on any
    mapping of name -> array-like.
    """
    sha = hashlib.sha256()
    for key in sorted(state_dict.keys()):
        arr = np.asarray(state_dict[key], dtype=np.float32)
        sha.update(arr.tobytes())
    return sha.hexdigest()


def guard_state_dict_hash(state_dict, context):
    """G1: assert the frozen-backbone hash matches the LOG-331 snapshot hash."""
    got = compute_state_dict_hash(state_dict)
    if got != WEIGHTS_PIN:
        raise RunInvalid(
            f"G1 FAIL ({context}): state_dict SHA-256 {got} != LOG-331 "
            f"snapshot {WEIGHTS_PIN} — Δθ=0 NOT verified. RUN-INVALID.")
    return got


def guard_g0_bench(bench=None):
    """G0: bench provenance. Raises RunInvalid (via BenchInvalid) on failure."""
    bench = bench if bench is not None else ref.build_bench()
    try:
        return ref.verify_g0(bench, BENCH_PIN)
    except ref.BenchInvalid as e:
        raise RunInvalid(str(e))


def guard_g2_artifact(bundle_dir=None):
    """G2: re-verify the build-time oracle-diagnostic artifact (bound to the
    bench pin). The diagnostic itself ran at build time per §6."""
    bundle_dir = bundle_dir or os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(bundle_dir, G2_ARTIFACT)
    if not os.path.isfile(path):
        raise RunInvalid(
            f"G2 FAIL: build-time diagnostic artifact not found at {path} "
            "— RUN-INVALID.")
    with open(path) as f:
        art = json.load(f)
    if art.get("bench_pin") != BENCH_PIN:
        raise RunInvalid(
            f"G2 FAIL: artifact bench pin {art.get('bench_pin')} != registered "
            f"{BENCH_PIN} — stale artifact; RUN-INVALID.")
    if art.get("gate") != "PASS" or not (art.get("permutation_p", 0) >= 0.05):
        raise RunInvalid(
            f"G2 FAIL: oracle diagnostic gate={art.get('gate')}, "
            f"p={art.get('permutation_p')} — bench confounded; RUN-INVALID.")
    return art


def guard_g3_phrasing(bench):
    n_a = sum(1 for b in bench if b["phrasing"] == "A-first")
    if n_a != 30 or len(bench) != 60:
        raise RunInvalid(
            f"G3 FAIL: A-first={n_a}/60, n={len(bench)} — RUN-INVALID.")


def option_token_ids(tokenizer, item):
    """The two option tokens for S2: target and foil (both single-token by G1')."""
    a_id = tokenizer.encode(" " + item["A"], add_special_tokens=False)
    c_id = tokenizer.encode(" " + item["C"], add_special_tokens=False)
    if len(a_id) != 1 or len(c_id) != 1:
        raise RunInvalid(
            f"G1' FAIL: option token for {item['A']!r}/{item['C']!r} not "
            f"single-token — RUN-INVALID.")
    return a_id[0], c_id[0]


def extract_mock(out_dir):
    """Synthetic extraction: seeded random embeddings, no weights touched.

    Runs the full guard chain that is weight-free: G0 (bench pin), G2
    (artifact re-verification), G3 (phrasing), G1' (build-time artifact
    re-verification). G1 is skipped (no weights in mock mode). Produces
    24-layer synthetic embeddings + synthetic option logits so the scorer
    exercises the full pipeline; mode is stamped "mock" (never a verdict).
    """
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    g0 = guard_g0_bench()
    g2 = guard_g2_artifact(bundle_dir)
    bench = ref.build_bench()
    guard_g3_phrasing(bench)
    g1p = g1prime.check_g1prime_artifact()

    rng = np.random.default_rng(MOCK_SEED)
    # 24 layers x 60 items x 1024 dims; layer-dependent scale so layers differ.
    layers = np.stack([
        rng.normal(loc=0.0, scale=1.0 + 0.05 * l,
                   size=(N_ITEMS, MOCK_DIM)).astype(np.float32)
        for l in range(N_LAYERS)
    ])
    # Synthetic option logits: pure noise (S2 at chance in mock).
    opt_logits = rng.normal(size=(N_ITEMS, 2)).astype(np.float32)

    os.makedirs(out_dir, exist_ok=True)
    emb_path = os.path.join(out_dir, "exp092_embeddings.npz")
    np.savez(emb_path, layers=layers, opt_logits=opt_logits,
             ids=np.array([b["id"] for b in bench]),
             labels=np.array([b["ent"] for b in bench]),
             phrasing=np.array([b["phrasing"] for b in bench]),
             domain=np.array([b["domain"] for b in bench]))
    meta = {
        "mode": "mock",
        "n": N_ITEMS,
        "n_layers": N_LAYERS,
        "dim": MOCK_DIM,
        "seed": MOCK_SEED,
        "G0": f"pass (bench pin {g0['pin'][:16]}…)",
        "G1": "skipped (no weights in mock mode)",
        "G1'": ("pass (build-time real-tokenizer verification artifact "
                "re-verified: 240/240 in-prompt occurrences single-token, "
                "bound to bench pin)"),
        "G2": (f"pass (oracle={g2['oracle_accuracy']:.4f}, "
               f"p={g2['permutation_p']:.4f}, gate PASS, bound to bench pin)"),
        "G3": "pass (30/30 asserted on real bench builder)",
        "embeddings": os.path.basename(emb_path),
    }
    with open(os.path.join(out_dir, "exp092_extraction_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    return emb_path, meta


def extract_real(out_dir, snapshot_override=None):
    """Real extraction from the frozen LOG-331 snapshot. CPU, read-only.

    Law #13 pins: model.eval() before extraction; torch.no_grad() around ALL
    extraction; requires_grad_(False) on all parameters; device_map="cpu"
    pinned explicitly (not a default).
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

    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    snap = snapshot_override or SNAPSHOT_DIR
    if not os.path.isdir(snap):
        raise RunInvalid(f"snapshot directory not found: {snap}")
    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print(msg, flush=True)

    # Weight-free guards FIRST (cheap, fail fast).
    g0 = guard_g0_bench()
    log(f"[extract] G0 pass: bench pin {g0['pin'][:16]}…, 60/60 unique "
        f"tuples, strata match §4.")
    g2 = guard_g2_artifact(bundle_dir)
    log(f"[extract] G2 pass: oracle={g2['oracle_accuracy']:.4f}, "
        f"p={g2['permutation_p']:.4f} (build-time diagnostic, bound to pin).")
    bench = ref.build_bench()
    guard_g3_phrasing(bench)
    log("[extract] G3 pass: 30/30 A-first/C-first.")

    log(f"[extract] loading tokenizer: {snap}")
    tokenizer = AutoTokenizer.from_pretrained(snap, local_files_only=True)

    # G1' enforcement: real-tokenizer offset-mapping cover check over all 60
    # prompts BEFORE any weight access.
    table = g1prime.verify_g1_prime(tokenizer, bench)
    n_occ = sum(v["occurrences"] for v in table.values())
    log(f"[extract] G1' pass: {n_occ}/240 A/C occurrences single-token "
        f"in-prompt (real tokenizer, offset-mapping cover check).")

    log(f"[extract] loading frozen model: {snap}")
    model = AutoModelForCausalLM.from_pretrained(
        snap, local_files_only=True, torch_dtype=torch.float32,
        device_map="cpu")  # §6 pin (Law #14 F2): explicit, not a default
    model.eval()                       # Law #13 pin (explicit, not a default)
    model.requires_grad_(False)        # frozen backbone: θ_after = θ_before
    log("[extract] model.eval() set; requires_grad_(False) on all parameters.")

    # G1 (pre): verify the frozen-backbone hash BEFORE any extraction.
    pre_hash = guard_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()}, "pre")
    log(f"[extract] G1 pre-extraction hash OK: {pre_hash[:16]}…")

    def encode_ids(text):
        return tokenizer.encode(text, add_special_tokens=False)

    layers = np.zeros((N_LAYERS, N_ITEMS, model.config.hidden_size),
                      dtype=np.float32)
    opt_logits = np.zeros((N_ITEMS, 2), dtype=np.float32)
    with torch.no_grad():              # Law #13 pin: no_grad around ALL extraction
        for i, b in enumerate(bench):
            ids = torch.tensor([encode_ids(b["prompt"])], dtype=torch.long)
            out = model(ids, output_hidden_states=True)
            # hidden_states[0] = embedding output -> indices 1..24 = layers 0..23.
            for l in range(N_LAYERS):
                h = out.hidden_states[l + 1][0, -1, :].detach().cpu()
                layers[l, i, :] = h.to(torch.float32).numpy()
            a_id, c_id = option_token_ids(tokenizer, b)
            logits = out.logits[0, -1, :].detach().cpu().to(torch.float32)
            opt_logits[i, 0] = float(logits[a_id])   # target option
            opt_logits[i, 1] = float(logits[c_id])   # foil option
    log(f"[extract] {N_ITEMS} forward passes complete ({N_LAYERS} layers, "
        f"final-token hidden states + option logits).")

    # G1 (post): Δθ=0 verified — hash must be unchanged after extraction.
    post_hash = guard_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()}, "post")
    log(f"[extract] G1 post-extraction hash OK: {post_hash[:16]}… "
        f"(Δθ=0 verified)")

    os.makedirs(out_dir, exist_ok=True)
    emb_path = os.path.join(out_dir, "exp092_embeddings.npz")
    np.savez(emb_path, layers=layers, opt_logits=opt_logits,
             ids=np.array([b["id"] for b in bench]),
             labels=np.array([b["ent"] for b in bench]),
             phrasing=np.array([b["phrasing"] for b in bench]),
             domain=np.array([b["domain"] for b in bench]))
    meta = {
        "mode": "real",
        "n": N_ITEMS,
        "n_layers": N_LAYERS,
        "dim": int(layers.shape[2]),
        "snapshot": snap,
        "G0": f"pass (bench pin {g0['pin'][:16]}…)",
        "G1": f"pass (pre/post hash {pre_hash[:16]}…, Δθ=0 verified)",
        "G1'": f"pass ({n_occ}/240 in-prompt occurrences single-token, "
                f"real tokenizer)",
        "G2": (f"pass (oracle={g2['oracle_accuracy']:.4f}, "
               f"p={g2['permutation_p']:.4f}, gate PASS, bound to bench pin)"),
        "G3": "pass (30/30 asserted on real bench builder)",
        "embeddings": os.path.basename(emb_path),
    }
    with open(os.path.join(out_dir, "exp092_extraction_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    with open(os.path.join(out_dir, "exp092_extraction_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    return emb_path, meta


def main(argv=None):
    ap = argparse.ArgumentParser(description="EXP092 layer-embedding extraction")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--mock", action="store_true",
                    help="synthetic embeddings; never touches weights")
    ap.add_argument("--ceo-clearance", action="store_true",
                    help="CEO execution clearance for REAL extraction "
                         "(LOG-4329 FIX 1: the standalone module CLI enforces "
                         "the signed protocol's launch chain)")
    ap.add_argument("--snapshot", default=None,
                    help="override snapshot dir (default: LOG-331 snapshot)")
    args = ap.parse_args(argv)
    # Launch-chain gate FIRST: no clearance, no real extraction — before any
    # guard, before any weight access (mirrors run_exp092.py).
    if not args.mock and not args.ceo_clearance:
        print("REFUSAL: real extraction requires --ceo-clearance (CEO). "
              "Use --mock for synthetic tests.", file=sys.stderr)
        return 2
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
