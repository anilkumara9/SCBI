#!/usr/bin/env python3
"""EXP087 C3 support set: B_agg construction, verbatim from EXP066
(experiments/scripts/run_exp066_pythia410m_replication.py ll. 97-154).

Five support vocabularies x 30 contrast pairs (15 2-hop + 15 3-hop):
  p_rel = "Premise: {A} outranks {B}. {B} outranks {C}. ..." (relational)
  p_neu = "Premise: {A} is next to {B}. {B} is next to {C}. ..." (neutral)
  dh = h_rel(final token, layer L+1) - h_neu(final token, layer L+1)
Per-vocab direction: v_hat_k = mean(dh / ||dh||), normalized.
B_agg = normalize(sum_k v_hat_k).

The pure-math aggregation (aggregate_b_agg) is torch-free and unit-tested.
build_b_agg() requires torch + the model and runs ONLY on the licensed
execution path (--execute with both flags).
"""

import math

SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Caleb", "Gideon", "Miriam", "Reuben"],
    "V3_Greek": ["Hector", "Jason", "Nestor", "Paris", "Priam"],
    "V4_Roman": ["Marcus", "Lucius", "Titus", "Felix", "Silas"],
    "V5_Modern": ["Liam", "Noah", "Sora", "Maya", "Leila"],
}

TRIPLES_INDICES = [
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
]
QUADS_INDICES = [
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
]


def build_support_prompts():
    """The 150 (p_rel, p_neu) contrast pairs, verbatim construction.
    Returns list of (vocab_key, p_rel, p_neu)."""
    pairs = []
    for v_key, ents in SUPPORT_VOCABULARIES.items():
        for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
            A, B, C = ents[iA], ents[iB], ents[iC]
            q_opts = f"{A} or {C}" if (i % 2 == 0) else f"{C} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            pairs.append((v_key, p_rel, p_neu))
        for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
            A, B, C, D = ents[iA], ents[iB], ents[iC], ents[iD]
            q_opts = f"{A} or {D}" if (i % 2 == 0) else f"{D} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            pairs.append((v_key, p_rel, p_neu))
    assert len(pairs) == 150
    return pairs


def _norm(v):
    return math.sqrt(sum(x * x for x in v))


def aggregate_b_agg(delta_h_by_vocab):
    """Pure-math B_agg aggregation (torch-free, unit-tested).

    delta_h_by_vocab: dict vocab_key -> list of 30 vectors (lists of floats).
    Returns the unit-norm B_agg vector (list of floats).
    """
    v_hats = []
    for v_key, vecs in delta_h_by_vocab.items():
        if len(vecs) != 30:
            raise ValueError(f"B_agg: vocab {v_key} has {len(vecs)} vectors, expected 30")
        d = len(vecs[0])
        mean_v = [0.0] * d
        for v in vecs:
            n = _norm(v) + 1e-12
            for j in range(d):
                mean_v[j] += v[j] / n
        mean_v = [x / len(vecs) for x in mean_v]
        n = _norm(mean_v) + 1e-12
        v_hats.append([x / n for x in mean_v])
    d = len(v_hats[0])
    total = [0.0] * d
    for v in v_hats:
        for j in range(d):
            total[j] += v[j]
    n = _norm(total) + 1e-12
    b_agg = [x / n for x in total]
    if _norm(b_agg) <= 0:
        raise ValueError("B_agg: zero norm — silent no-op refused")
    return b_agg


def make_bridge_vec_embed(embed_weight, t_id, f_id):
    """EXP066 make_bridge_vec VERBATIM (pure-math form):
    w = E[t] − E[f]; return w / (||w|| + 1e-12)."""
    w = [a - b for a, b in zip(embed_weight[t_id], embed_weight[f_id])]
    n = _norm(w) + 1e-12
    return [x / n for x in w]


def build_b_agg(model, tokenizer, device, target_layer, log_fn=print):
    """EXECUTION-ONLY: full B_agg construction on the model (150 support
    pairs × 2 forward passes = 300 passes, plus the 180 registered passes).

    NOTE: the 300 support passes are part of the C3 arm's construction cost;
    the registered 180-pass budget (§4) covers the C1/C2/C3 measurement arms
    — the support construction is the pre-registered B_agg definition
    (EXP065/066/067-identical), not an unregistered extra.
    """
    import torch
    log_fn(f"[C3] constructing B_agg: 150 support pairs x 2 passes at layer {target_layer}")
    pairs = build_support_prompts()
    delta_h_by_vocab = {k: [] for k in SUPPORT_VOCABULARIES}
    with torch.no_grad():
        for v_key, p_rel, p_neu in pairs:
            o_rel = model(input_ids=tokenizer.encode(p_rel, return_tensors="pt").to(device),
                          output_hidden_states=True)
            o_neu = model(input_ids=tokenizer.encode(p_neu, return_tensors="pt").to(device),
                          output_hidden_states=True)
            dh = (o_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
                  - o_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu())
            delta_h_by_vocab[v_key].append(dh.tolist())
    b_agg = aggregate_b_agg(delta_h_by_vocab)
    log_fn(f"[C3] B_agg constructed (dim={len(b_agg)}, norm={_norm(b_agg):.4f})")
    return torch.tensor(b_agg, dtype=torch.float32)
