"""EXP145 decode-arm extraction — 60 forward passes, GPT-2-small, CPU, $0.

Mirrors EXP092 extract_real: weight-free guards first, G1' cover BEFORE
weight access, threads pinned, model.eval() + requires_grad_(False) +
no_grad, G1 pre/post state-dict hash (Δθ=0), per-item records written
INCREMENTALLY (flush after each item; resumed runs skip recorded items).

S0.2: asserts the loaded snapshot's revision character-by-character against
the pin recorded at download time (S7-3 lesson: never trust a transcription).
"""

import json
import os
import sys

# Environment quirk (see exp145_step0_download.py): sanitize bracketed IPv6
# entries from no_proxy/NO_PROXY before any hub/httpx import.
for _var in ("no_proxy", "NO_PROXY"):
    _val = os.environ.get(_var)
    if _val:
        _clean = ",".join(p for p in _val.split(",") if "[" not in p and "]" not in p)
        os.environ[_var] = _clean

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp145_common as C  # noqa: E402

MANIFEST = os.path.join(C.RUN_DIR, "exp145_manifest.json")
RECORDS = os.path.join(C.RUN_DIR, "exp145_extract_records.jsonl")


def main():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from huggingface_hub import snapshot_download

    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print(msg, flush=True)

    with open(MANIFEST) as f:
        manifest = json.load(f)
    if manifest.get("g1prime") != "PASS (240/240, GPT-2 BPE, offset-mapping)":
        raise C.RunInvalid("G1' did not pass in step 0 — RUN-INVALID.")
    rev = manifest["model_revision_40hex"]

    torch.set_num_threads(C.THREAD_PIN)
    assert torch.get_num_threads() == C.THREAD_PIN
    log(f"[extract] torch intra-op threads pinned: {C.THREAD_PIN}")

    bench, g0 = C.guard_g0_bench()
    assert g0["pin"] == manifest["bench_pin"], "bench pin drifted"
    log(f"[extract] G0 pass: bench pin {g0['pin'][:16]}…")
    g2 = C.guard_g2_oracle(g0["pin"])
    log(f"[extract] G2 pass (bound to pin): oracle={g2['oracle_accuracy']:.4f}")
    n_a = sum(1 for b in bench if b["phrasing"] == "A-first")
    assert n_a == 30 and len(bench) == 60, "G3 phrasing balance"
    log("[extract] G3 pass: 30/30 A-first/C-first.")

    # S0.2: download weights at the PINNED revision, then assert the local
    # snapshot directory's revision character-by-character vs the record.
    snap = snapshot_download(
        manifest["repo_id"], revision=rev,
        cache_dir=os.path.join(C.RUN_DIR, "hf_cache"))
    snap_base = os.path.basename(os.path.normpath(snap))
    if snap_base != rev:
        raise C.RunInvalid(
            f"S0.2 FAIL: local snapshot revision dir {snap_base!r} != "
            f"recorded pin {rev!r} — RUN-INVALID.")
    log(f"[extract] S0.2 pass: local revision {snap_base[:16]}… == recorded "
        f"pin (character-identical).")

    log(f"[extract] loading tokenizer: {snap}")
    tokenizer = AutoTokenizer.from_pretrained(snap, local_files_only=True)

    # G1' re-fires under the real tokenizer BEFORE any weight access.
    sys.path.insert(0, C.EXP092_DIR)
    import g1prime
    table = g1prime.verify_g1_prime(tokenizer, bench)
    n_occ = sum(v["occurrences"] for v in table.values())
    assert n_occ == 240
    log("[extract] G1' re-pass: 240/240 single-token (real GPT-2 BPE) "
        "BEFORE weight access.")
    opt_ids = [(table[b["A"]]["token_id"], table[b["C"]]["token_id"])
               for b in bench]

    log("[extract] loading frozen model (weights accessed NOW, first time)")
    model = AutoModelForCausalLM.from_pretrained(
        snap, local_files_only=True, torch_dtype=torch.float32,
        device_map="cpu")
    model.eval()
    model.requires_grad_(False)
    n_layers = model.config.n_layer
    hidden = model.config.hidden_size
    assert n_layers == C.N_LAYERS, f"n_layer={n_layers} != 12"
    log(f"[extract] model: {n_layers} layers, hidden={hidden}, eval(), "
        f"requires_grad_(False).")

    # G1 (pre): frozen-backbone hash recorded.
    pre_hash = C.compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    log(f"[extract] G1 pre-extraction state-dict hash: {pre_hash[:16]}… "
        f"(recorded; post-hash must match, Δθ=0).")

    def encode_ids(text):
        return tokenizer.encode(text, add_special_tokens=False)

    writer = C.JsonlWriter(RECORDS)
    pending = [i for i in range(C.N_ITEMS) if not writer.done(i)]
    log(f"[extract] {C.N_ITEMS - len(pending)}/60 items already recorded; "
        f"{len(pending)} pending.")

    with torch.no_grad():
        for i in pending:
            b = bench[i]
            ids = torch.tensor([encode_ids(b["prompt"])], dtype=torch.long)
            out = model(ids, output_hidden_states=True)
            # hidden_states[0] = embeddings -> [1..12] = layers 0..11.
            hs = [out.hidden_states[l + 1][0, -1, :].detach().cpu()
                  .to(torch.float32).numpy().astype(np.float64).tolist()
                  for l in range(C.N_LAYERS)]
            a_id, c_id = opt_ids[i]
            logits = out.logits[0, -1, :].detach().cpu().to(torch.float32)
            writer.write({
                "item": i,
                "id": b["id"],
                "layers": hs,                       # 12 x 768
                "logit_target": float(logits[a_id]),
                "logit_foil": float(logits[c_id]),
                "a_id": int(a_id), "c_id": int(c_id),
                "n_tokens": int(ids.shape[1]),
            })
    log(f"[extract] {writer.count()}/60 records complete.")

    # Assemble the bundle.
    recs = {}
    with open(RECORDS) as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                recs[int(r["item"])] = r
    if len(recs) != C.N_ITEMS:
        raise C.Inconclusive(f"S0.5: {C.N_ITEMS - len(recs)}/60 missing "
                             "records — INCONCLUSIVE.")
    # layers assembled as (12 layers, 60 items, 768 dims)
    layers = np.stack([[np.array(recs[i]["layers"][l], dtype=np.float32)
                        for i in range(C.N_ITEMS)]
                       for l in range(C.N_LAYERS)])
    assert layers.shape == (C.N_LAYERS, C.N_ITEMS, 768), layers.shape
    opt_logits = np.array([[recs[i]["logit_target"], recs[i]["logit_foil"]]
                           for i in range(C.N_ITEMS)], dtype=np.float32)

    # S0.3: per-layer std > 0; no NaN/Inf.
    for l in range(C.N_LAYERS):
        std = float(layers[l].std())
        assert std > 0, f"S0.3 FAIL: layer {l} std={std} — RUN-INVALID."
        assert np.isfinite(layers[l]).all(), f"layer {l} NaN/Inf"
    log("[extract] S0.3 pass: per-layer std > 0 for all 12 layers; no "
        "NaN/Inf.")

    # G1 (post): Δθ=0 verified.
    post_hash = C.compute_state_dict_hash(
        {k: v.detach().cpu() for k, v in model.state_dict().items()})
    if post_hash != pre_hash:
        raise C.RunInvalid(
            f"G1 FAIL (post): state-dict hash changed during extraction — "
            f"Δθ=0 VIOLATED — RUN-INVALID.")
    log(f"[extract] G1 post-extraction hash OK: {post_hash[:16]}… "
        f"(Δθ=0 verified)")

    emb_path = os.path.join(C.RUN_DIR, "exp145_embeddings.npz")
    np.savez(emb_path, layers=layers.astype(np.float32), opt_logits=opt_logits,
             ids=np.array([b["id"] for b in bench]),
             labels=np.array([b["ent"] for b in bench]),
             phrasing=np.array([b["phrasing"] for b in bench]),
             domain=np.array([b["domain"] for b in bench]))
    meta = {
        "mode": "real", "experiment": "EXP145", "n": C.N_ITEMS,
        "n_layers": C.N_LAYERS, "dim": int(layers.shape[2]),
        "model_revision_40hex": rev,
        "bench_pin": manifest["bench_pin"],
        "G0": f"pass (pin {manifest['bench_pin'][:16]}…)",
        "G1": f"pass (pre/post hash {pre_hash[:16]}…, Δθ=0 verified)",
        "G1_pre_hash": pre_hash,
        "G1'": "pass (240/240, real GPT-2 BPE, before weight access)",
        "G2": f"pass (oracle={g2['oracle_accuracy']:.4f}, "
               f"p={g2['permutation_p']:.4f}, bound to pin)",
        "G3": "pass (30/30)",
        "S0.2": f"pass (revision {rev[:16]}… character-identical)",
        "S0.3": "pass (per-layer std > 0, no NaN/Inf)",
        "embeddings": os.path.basename(emb_path),
    }
    with open(os.path.join(C.RUN_DIR, "exp145_extraction_meta.json"), "w") as f:
        json.dump(meta, f, indent=1)
    with open(os.path.join(C.RUN_DIR, "exp145_extraction_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print(f"[extract] wrote {emb_path}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except C.RunInvalid as e:
        print(f"RUN-INVALID: {e}", flush=True)
        sys.exit(3)
    except C.Inconclusive as e:
        print(f"INCONCLUSIVE: {e}", flush=True)
        sys.exit(4)
