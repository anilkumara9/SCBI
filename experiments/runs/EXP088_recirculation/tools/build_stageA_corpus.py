#!/usr/bin/env python3
"""Build the pinned EXP088 Stage-A corpus artifact (build-time tool).

Signed protocol (Stage A): "~50k held-out tokens (exact slice pinned at
build; no test-set overlap with Stage B)".

This tool constructs the slice deterministically from a public source and
writes experiments/runs/EXP088_recirculation/stageA_corpus.json:

  source:      wikitext (wikitext-103-raw-v1), validation split
  file:        validation-00000-of-00001.parquet (HF datasets mirror)
  rows:        file order, "text" column concatenated with single newlines
  tokenizer:   EleutherAI/pythia-410m tokenizer.json (GPT-NeoX BPE)
  slice:       first 50,000 tokens of the tokenized stream

Provenance recorded in the artifact: dataset name/config/split, source file
URL + sha256, tokenizer URL + sha256, row count, join rule, token count,
and the sha256 of the token-ID array (the runner verifies this at startup).

Stage-B overlap: the Stage-B probe is 60 synthetic Planetary/Elemental
ranking prompts (EXP077); a natural-text Wikipedia slice cannot overlap it
by construction — recorded in the artifact notes.

Caveat (documented, not hidden): wikitext-103 derives from Wikipedia, which
is inside Pythia-410m's Pile pretraining mix — the slice is "held out" in
the protocol's sense (held out from the experiment: fixed before Stage A,
no overlap with the Stage-B probe), not held out from pretraining. The
Stage-A screen is comparative (recirculated vs baseline perplexity on the
same tokens) with a measured noise floor, so absolute perplexity levels do
not drive selection; the Law #14 bundle review adjudicates whether this
caveat needs a stronger held-out guarantee.

Usage (build machine; needs tokenizers + pyarrow):
    /tmp/exp088venv/bin/python tools/build_stageA_corpus.py

$0 (public data, CPU). Deterministic given the pinned source bytes.
"""

import hashlib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.dirname(HERE)
OUT_PATH = os.path.join(BUNDLE, "stageA_corpus.json")

PARQUET_URL = ("https://huggingface.co/datasets/wikitext/resolve/main/"
               "wikitext-103-raw-v1/validation-00000-of-00001.parquet")
TOKENIZER_URL = ("https://huggingface.co/EleutherAI/pythia-410m/resolve/main/"
                 "tokenizer.json")
N_TOKENS = 50000


def _fetch(url, label):
    print(f"fetching {label}: {url}", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "scbi-exp088/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    print(f"  {len(data)} bytes, sha256={hashlib.sha256(data).hexdigest()[:16]}...",
          flush=True)
    return data


def main():
    import pyarrow.parquet as pq  # noqa
    from tokenizers import Tokenizer  # noqa

    parquet_bytes = _fetch(PARQUET_URL, "wikitext-103-raw-v1 validation")
    tok_bytes = _fetch(TOKENIZER_URL, "pythia-410m tokenizer")

    tmp_parquet = os.path.join("/tmp", "exp088_wikitext_valid.parquet")
    with open(tmp_parquet, "wb") as f:
        f.write(parquet_bytes)
    table = pq.read_table(tmp_parquet)
    texts = table.column("text").to_pylist()
    print(f"parquet rows: {len(texts)}", flush=True)

    tmp_tok = os.path.join("/tmp", "exp088_tokenizer.json")
    with open(tmp_tok, "wb") as f:
        f.write(tok_bytes)
    tok = Tokenizer.from_file(tmp_tok)

    # Concatenate in file order; skip empty rows (wikitext-raw has "= ... ="
    # header rows — kept verbatim; the slice is defined by order, not content).
    stream = "\n".join(t for t in texts if t)
    ids = tok.encode(stream).ids
    print(f"tokenized stream: {len(ids)} tokens", flush=True)
    if len(ids) < N_TOKENS:
        raise RuntimeError(f"stream has {len(ids)} tokens < {N_TOKENS}")
    ids = ids[:N_TOKENS]

    id_bytes = b",".join(str(i).encode() for i in ids)
    ids_sha = hashlib.sha256(id_bytes).hexdigest()
    artifact = {
        "experiment": "EXP088",
        "stage": "A",
        "provenance": {
            "dataset": "wikitext",
            "config": "wikitext-103-raw-v1",
            "split": "validation",
            "source_url": PARQUET_URL,
            "source_sha256": hashlib.sha256(parquet_bytes).hexdigest(),
            "n_rows": len(texts),
            "join": "file order, 'text' column, single-newline join, empty rows dropped",
            "tokenizer_url": TOKENIZER_URL,
            "tokenizer_sha256": hashlib.sha256(tok_bytes).hexdigest(),
            "slice": f"first {N_TOKENS} tokens of the tokenized stream",
        },
        "n_tokens": N_TOKENS,
        "token_ids": ids,
        "token_ids_sha256": ids_sha,
        "notes": [
            "No overlap with the Stage-B probe set (60 synthetic EXP077 "
            "ranking prompts) by construction.",
            "CAVEAT: wikitext-103 derives from Wikipedia, inside "
            "Pythia-410m's Pile pretraining mix — held out from the "
            "experiment, not from pretraining. The Stage-A screen is "
            "comparative (recirculated vs baseline on identical tokens) "
            "with a measured noise floor; absolute perplexity does not "
            "drive selection.",
        ],
    }
    tmp = OUT_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(artifact, f)
    os.replace(tmp, OUT_PATH)
    print(f"wrote {OUT_PATH}: {N_TOKENS} tokens, ids sha256={ids_sha}",
          flush=True)


if __name__ == "__main__":
    sys.exit(main())
