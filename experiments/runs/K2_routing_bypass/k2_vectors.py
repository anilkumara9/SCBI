"""K2 routing-vs-bypass — bridge-vector construction-identity (REV2 G1).

Implements REV2 §5's companion identity:
    b_K2 = alpha * normalize(E[t] - E[f])   per item
with E = the pinned model's OUTPUT embedding matrix
(model.get_output_embeddings().weight), t/f = first subtokens of
" "+target / " "+foil — EXP066 `make_bridge_vec` VERBATIM (the LOG-197
E1+E2 source link; see run_exp077.py §4 C8, experiments/runs/exp077/).

torch is imported LAZILY (inside functions) so this module imports on a
torch-free machine; tensor functions raise a clear error there. The pure
predicates (digest compare, norm compare) live in k2_guards and are
torch-free.

Epistemic grade: [INFERENCE] (deterministic reconstruction) — never
[FACT]. The norm fingerprint G1(b) is a WEAK identity check (any
unit*alpha vector passes); the honest license is deterministic
reconstruction + the live (c)-gate (REV2 G5).
"""

import hashlib

ALPHA_K2 = 0.50  # REV2 §3.1: alpha=0.5 (EXP066's calibrated configuration)


def _require_torch():
    try:
        import torch
        return torch
    except ImportError as e:
        raise RuntimeError(
            "k2_vectors tensor functions require torch (Kaggle runtime). "
            "Pure guard predicates live in k2_guards.") from e


def build_bridge_vectors_primary(model, tokenizer, items, alpha=ALPHA_K2):
    """Primary construction path — the runner's path (EXP077 C8 verbatim).

    items: list of dicts with "A" (target string) and "C" (foil string).
    Returns (vectors, E): per-item CPU float32 tensors + the E matrix used.
    """
    torch = _require_torch()
    E = model.get_output_embeddings().weight.detach().cpu().to(torch.float32)
    vecs = []
    token_map = []
    for it in items:
        tt = tokenizer.encode(" " + it["A"])[0]   # target = correct answer
        ft = tokenizer.encode(" " + it["C"])[0]   # foil
        w = E[tt, :] - E[ft, :]
        v = alpha * (w / (torch.norm(w) + 1e-12))
        vecs.append(v)
        token_map.append({"A": it["A"], "C": it["C"],
                          "t_id": int(tt), "f_id": int(ft),
                          "t_single": len(tokenizer.encode(" " + it["A"])) == 1,
                          "f_single": len(tokenizer.encode(" " + it["C"])) == 1})
    return vecs, E, token_map


def build_bridge_vectors_reference(model, tokenizer, items, alpha=ALPHA_K2):
    """Independent reference construction path — gate A(i)'s second rebuild.

    Deliberately written as a separate code path (separate embedding-matrix
    fetch + clone, separate tokenization calls, manual norm) so that
    byte-identity between the two rebuilds is a non-trivial determinism
    check, not a self-comparison. Same pinned inputs, same mathematics.
    """
    torch = _require_torch()
    emb = model.get_output_embeddings().weight.detach().cpu().to(torch.float32).clone()
    vecs = []
    for it in items:
        ids_t = tokenizer(" " + it["A"], add_special_tokens=False)["input_ids"]
        ids_f = tokenizer(" " + it["C"], add_special_tokens=False)["input_ids"]
        if len(ids_t) != 1 or len(ids_f) != 1:
            raise ValueError(
                "reference path requires single-token target/foil "
                "(got %r -> %d tokens, %r -> %d tokens); the primary path's "
                "verbatim-C8 [0]-subtoken rule would diverge — recorded, not silent."
                % (it["A"], len(ids_t), it["C"], len(ids_f)))
        d = emb[ids_t[0], :] - emb[ids_f[0], :]
        n = torch.sqrt(torch.sum(d * d))
        vecs.append(alpha * d / (n + 1e-12))
    return vecs


def vector_digest(vec):
    """sha256 over the float32 CPU bytes of one vector (byte-identity unit)."""
    torch = _require_torch()
    b = vec.detach().cpu().to(torch.float32).numpy().tobytes()
    return hashlib.sha256(b).hexdigest()


def gate_a_run(model, tokenizer, items, logged_norms, tol=1e-5,
               tokenizer_checksum=None, hf_revision=None):
    """LOG-224c Ruling 7 — pre-execution gate A (CPU identity dry run).

    (i) two independent CPU rebuilds byte-identical (per-item digests);
    (ii) per-item norms match run-logged C8 norms within tol (rel err);
    (iii) tokenizer checksum + HF revision logged (via k2_guards.checklist_b_record).
    Returns a record; verdict via k2_guards.gate_a_evaluate.
    """
    from k2_guards import g1_norm_check, gate_a_evaluate, checklist_b_record
    torch = _require_torch()

    vecs_p, _E, token_map = build_bridge_vectors_primary(model, tokenizer, items)
    vecs_r = build_bridge_vectors_reference(model, tokenizer, items)

    digests_p = [vector_digest(v) for v in vecs_p]
    digests_r = [vector_digest(v) for v in vecs_r]
    byte_identity_ok = (digests_p == digests_r)
    mismatched = [i for i, (a, b) in enumerate(zip(digests_p, digests_r)) if a != b]

    rebuilt_norms = [float(torch.norm(v).item()) for v in vecs_p]
    norm_match_ok, per_item_norms = g1_norm_check(rebuilt_norms, logged_norms, tol=tol)

    checklist_b = checklist_b_record(tokenizer_checksum, hf_revision)
    tokenizer_logged = (checklist_b["status"] == "complete")

    verdict, message = gate_a_evaluate(byte_identity_ok, norm_match_ok, tokenizer_logged)
    return {
        "gate": "A",
        "verdict": verdict,
        "message": message,
        "n_items": len(items),
        "byte_identity_ok": bool(byte_identity_ok),
        "mismatched_items": mismatched,
        "per_item_digests_primary": digests_p,
        "norm_match_ok": bool(norm_match_ok),
        "per_item_norms": per_item_norms,
        "rebuilt_norms": rebuilt_norms,
        "token_map": token_map,
        "checklist_b": checklist_b,
        "epistemic_grade": "[INFERENCE] (deterministic reconstruction) — never [FACT]",
    }


def get_hash(model):
    """SHA-256 binding guard (REV2 G3): over sorted state_dict keys, CPU float32 bytes."""
    torch = _require_torch()
    sha = hashlib.sha256()
    for key in sorted(model.state_dict().keys()):
        sha.update(model.state_dict()[key].detach().cpu().to(torch.float32).numpy().tobytes())
    return sha.hexdigest()
