"""EXP145 Step 0 — model revision pin + tokenizer download + G1' gate.

S7-2b §4 order: S0.1 (bench pin recompute over the loaded pinned JSON +
G1' live re-fire, 240/240) BEFORE any weight access; S0.1a (procedural
cross-check); S0.2 (model revision assert). If G1' fails, the run is
INCONCLUSIVE (bench non-portable) — no silent entity substitution, no
weight download.

Exit codes: 0 = G1' PASS, tokenizer ready; 1 = INCONCLUSIVE (G1' fail);
2 = RUN-INVALID.
"""

import json
import os
import sys

# Environment quirk: httpx (huggingface_hub's HTTP layer) chokes on the
# bracketed IPv6 entries in no_proxy/NO_PROXY ("Invalid port: ':1]'").
# Sanitize before any hub/httpx import. Proxy egress itself is unaffected.
for _var in ("no_proxy", "NO_PROXY"):
    _val = os.environ.get(_var)
    if _val:
        _clean = ",".join(p for p in _val.split(",") if "[" not in p and "]" not in p)
        os.environ[_var] = _clean

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp145_common as C  # noqa: E402

REPO_ID = "gpt2"
MANIFEST = os.path.join(C.RUN_DIR, "exp145_manifest.json")


def main():
    from huggingface_hub import HfApi, snapshot_download

    # S0.2: resolve the revision programmatically (never transcribed) and
    # assert it character-identical to the plan's pinned revision.
    api = HfApi()
    info = api.model_info(REPO_ID)
    rev = info.sha
    if not (isinstance(rev, str) and len(rev) == 40
            and all(c in "0123456789abcdef" for c in rev)):
        raise C.RunInvalid(f"S0.2 FAIL: resolved revision is not a 40-hex "
                           f"sha: {rev!r} — RUN-INVALID.")
    if rev != C.S72B_MODEL_REV:
        raise C.RunInvalid(
            f"S0.2 FAIL: resolved revision {rev!r} != plan pin "
            f"{C.S72B_MODEL_REV!r} — revision drift — RUN-INVALID.")
    print(f"[step0] S0.2 pass: resolved {REPO_ID} -> revision {rev} "
          f"(character-identical to plan pin)", flush=True)

    # S0.1 (pin part): load the pinned bench JSON and recompute the pin.
    bench = C.build_bench()
    pin = C.canonical_pin(bench)
    if pin != C.S72B_PIN:
        raise C.RunInvalid(
            f"S0.1 FAIL: recomputed pin {pin} != plan pin {C.S72B_PIN} — "
            f"RUN-INVALID.")
    print(f"[step0] S0.1 pin pass: {pin[:16]}… character-identical to plan "
          f"pin (recomputed over the loaded pinned bench JSON)", flush=True)

    # S0.1a: procedural cross-check (Law #14 fix 3, required hardening).
    proc_pin = C.guard_s01a_procedural_crosscheck(pin)
    print(f"[step0] S0.1a pass: procedural pin {proc_pin[:16]}… == loaded "
          f"JSON pin", flush=True)

    # G0 + G2 (weight-free).
    bench, g0 = C.guard_g0_bench(bench)
    if g0["pin"] != pin:
        raise C.RunInvalid(
            f"G0 FAIL: verify_g0 pin {g0['pin']} != S0.1 pin {pin} — "
            f"RUN-INVALID.")
    print(f"[step0] G0 pass: bench pin {pin[:16]}…, 60/60 unique, "
          f"strata {g0['strata']}", flush=True)
    g2 = C.guard_g2_oracle(pin)
    print(f"[step0] G2 pass: oracle={g2['oracle_accuracy']:.4f}, "
          f"p={g2['permutation_p']:.4f} (derivation diagnostic re-bound to "
          f"the new pin)", flush=True)

    # Tokenizer files ONLY — no weights touched on this path.
    tok_dir = snapshot_download(
        REPO_ID, revision=rev,
        allow_patterns=["*.json", "*.txt", "*.model"],
        cache_dir=os.path.join(C.RUN_DIR, "hf_cache"))
    print(f"[step0] tokenizer files downloaded (weights NOT downloaded)",
          flush=True)

    # Record the pin BEFORE any weight access (S0.2 recorded value).
    manifest = {
        "experiment": "EXP145",
        "repo_id": REPO_ID,
        "resolved_repo_id": info.id,
        "model_revision_40hex": rev,
        "bench_pin": pin,
        "bench_g0": {"n": g0["n"], "unique_tuples": g0["unique_tuples"],
                   "strata": {f"{d}/{p}": v for (d, p), v in
                              g0["strata"].items()}},
        "g2": {"oracle_accuracy": g2["oracle_accuracy"],
               "permutation_p": g2["permutation_p"], "gate": g2["gate"]},
        "g1prime": "pending",
    }
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"[step0] S0.2 pin recorded: {rev}", flush=True)

    # G1': verbatim committed g1prime cover check under GPT-2's BPE.
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(tok_dir, local_files_only=True)
    sys.path.insert(0, C.EXP092_DIR)
    import g1prime
    try:
        table = g1prime.verify_g1_prime(tokenizer, bench)
    except g1prime.RunInvalid as e:
        manifest["tokenizer_files_dir"] = tok_dir
        manifest["g1prime"] = "FAIL (bench non-portable)"
        manifest["g1prime_failure"] = str(e)[:500]
        manifest["disposition"] = ("INCONCLUSIVE (bench non-portable) per "
                                   "S7-2b §4 S0.1 G1' — no weights downloaded")
        with open(MANIFEST, "w") as f:
            json.dump(manifest, f, indent=1)
        print(f"INCONCLUSIVE: {e}", flush=True)
        print(f"[step0] G1' FAIL — bench non-portable to GPT-2 BPE; the run "
              f"is INCONCLUSIVE per S7-2b §4 S0.1 G1'. Weights never downloaded.",
              flush=True)
        return 1
    n_occ = sum(v["occurrences"] for v in table.values())
    n_single = sum(v["single_token"] for v in table.values())
    if n_occ != 240 or n_single != 240:
        manifest["tokenizer_files_dir"] = tok_dir
        manifest["g1prime"] = (f"FAIL ({n_single}/{n_occ} single-token, "
                               "bench non-portable)")
        manifest["disposition"] = ("INCONCLUSIVE (bench non-portable) per "
                                   "S7-2b §4 S0.1 G1' — no weights downloaded")
        with open(MANIFEST, "w") as f:
            json.dump(manifest, f, indent=1)
        print(f"INCONCLUSIVE: G1' {n_single}/{n_occ} single-token, expected "
              f"240/240 — bench non-portable (INCONCLUSIVE).", flush=True)
        return 1
    print(f"[step0] G1' PASS: {n_single}/{n_occ} A/C occurrences single-token "
          f"under GPT-2 BPE (real tokenizer, offset-mapping cover).",
          flush=True)

    manifest["g1prime"] = "PASS (240/240, GPT-2 BPE, offset-mapping)"
    manifest["tokenizer_files_dir"] = tok_dir
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=1)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except C.RunInvalid as e:
        print(f"RUN-INVALID: {e}", flush=True)
        sys.exit(2)
