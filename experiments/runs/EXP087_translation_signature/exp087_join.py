#!/usr/bin/env python3
"""EXP087 pinned c_i item-alignment join (§8 item 2, resolved LOG-314).

The K1 JSON (research/analysis_plans/K1_RESULTS_LOG213_2026-09-23.json,
endpoint_a.EXP066.c, 60 floats) carries no per-item key material, so the
constructible join is an ORDER PIN licensed by K1's archive-verified G2
guard, with SHA-256 prompt-hash byte-identity verification on the
fresh-run side.

Pinned join rule:
  (inputs)    the K1 JSON, the EXP066 archive, the verbatim O list, and the
              EXP087 fresh-run per-item logs;
  (hash)      SHA-256 over the UTF-8 bytes of the prompt string,
              byte-verbatim, no normalization;
  (join)      for j = 0..59, pair c[j] with the fresh-run record whose
              instance_key == O[j], and REQUIRE
              SHA-256(fresh prompt) == SHA-256(archive prompt at O[j]);
  (tie-break) none required — keys are unique on both sides;
  (failures)  c length != 60 → fail; fresh key set != O set → fail;
              any prompt-hash mismatch → fail; duplicate keys → fail.

On ANY join failure the join is unlicensed for R4 (JoinError, FATAL — it
never silently mis-pairs). The verdict layer maps a join failure at
execution time to RUN-INVALID (apparatus) — a build-lane resolution
flagged for independent review (see BUILD_NOTES.md).
"""

import json

import exp087_benchmark as B
import exp087_guards as G


def load_c_vector(k1_json_path):
    """Load the 60 K1 c values (endpoint_a.EXP066.c)."""
    with open(k1_json_path, "r", encoding="utf-8") as f:
        d = json.load(f)
    try:
        c = d["endpoint_a"]["EXP066"]["c"]
    except KeyError as e:
        raise G.JoinError(f"join FATAL: K1 JSON missing endpoint_a.EXP066.c ({e})")
    if len(c) != 60:
        raise G.JoinError(f"join FATAL: c has length {len(c)}, expected 60")
    return [float(v) for v in c]


def pinned_join(c_list, fresh_records, archive):
    """Pair c[j] with the fresh-run record whose instance_key == O[j].

    fresh_records: iterable of dicts with 'instance_key' and 'prompt'.
    archive: dict mapping instance key -> {'prompt': ...} (EXP066 archive).

    Returns a list of 60 dicts, in O order, each the fresh record with an
    added 'c_i' field. Raises G.JoinError (FATAL) on any failure mode.
    """
    O = B.order_O()
    if len(c_list) != 60:
        raise G.JoinError(f"join FATAL: c length {len(c_list)} != 60")
    by_key = {}
    for rec in fresh_records:
        k = rec.get("instance_key")
        if k in by_key:
            raise G.JoinError(f"join FATAL: duplicate fresh-run key '{k}'")
        by_key[k] = rec
    if set(by_key.keys()) != set(O):
        missing = sorted(set(O) - set(by_key.keys()))
        extra = sorted(set(by_key.keys()) - set(O))
        raise G.JoinError(
            f"join FATAL: fresh key set != O set "
            f"(missing={missing[:5]}, extra={extra[:5]})")
    joined = []
    for j, key in enumerate(O):
        rec = by_key[key]
        if key not in archive:
            raise G.JoinError(f"join FATAL: archive missing key '{key}'")
        h_fresh = B.prompt_sha256(rec["prompt"])
        h_arch = B.prompt_sha256(archive[key]["prompt"])
        if h_fresh != h_arch:
            raise G.JoinError(
                f"join FATAL: prompt-hash mismatch at O[{j}] = '{key}' "
                f"(fresh={h_fresh[:12]}... != archive={h_arch[:12]}...) — "
                f"a changed prompt invalidates the join; never silently mis-paired")
        out = dict(rec)
        out["c_i"] = float(c_list[j])
        out["join_index"] = j
        joined.append(out)
    return joined


def default_k1_path():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    scbi = os.path.abspath(os.path.join(here, "..", "..", ".."))
    return os.path.join(scbi, "research", "analysis_plans",
                        "K1_RESULTS_LOG213_2026-09-23.json")
