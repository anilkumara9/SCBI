"""EXP131 B_agg support machinery — vendored verbatim from EXP077.

Provenance: ~/workspace/SCBI/experiments/runs/exp077/run_exp077.py
(lines 138-161 constants; lines 251-294 build_candidate_directions).
Copied verbatim on 2026-09-29 for the EXP131 bundle; no scientific
change. The B_agg (v_hat) direction is the EXP077 dead bridge
direction, re-derived deterministically from the archived support
set per EXP077's §3.1–3.2 reconstruction — the provenance the
EXP131 pre-registration §3.3 licenses (Law #2: no B_agg artifact
hash exists in program records, so no hash is invented; the
deterministic reconstruction + its worksheet-recorded SHA-256 is
the pin).

Support prompt construction (p_rel / p_neu strings) is also verbatim
from run_exp077.py main() (lines ~440-466).
"""

import numpy as np
import torch

# ---- Verbatim from run_exp077.py (lines 138-145) ----
SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Joel", "Gideon", "Ruth", "Abel"],
    "V3_Greek": ["Ajax", "Jason", "Apollo", "Paris", "Atlas"],
    "V4_Roman": ["Marcus", "Julius", "Augustus", "Felix", "Diana"],
    "V5_Modern": ["Liam", "Noah", "Eli", "Maya", "Finn"],
}
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())

# ---- Verbatim from run_exp077.py (lines 152-156) ----
TRIPLES_INDICES = [
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
]

# ---- Verbatim from run_exp077.py (lines 157-161) ----
QUADS_INDICES = [
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
]


def support_prompts():
    """Yield (prompt_id, p_rel, p_neu) for the 300 support presentations.

    Verbatim string construction from run_exp077.py main() (§1 support set).
    5 vocabs x (15 triples + 15 quads) x (rel, neu) = 300 presentations.
    """
    for vk, ents in SUPPORT_VOCABULARIES.items():
        for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
            A, B, C = ents[iA], ents[iB], ents[iC]
            q_opts = f"{A} or {C}" if (i % 2 == 0) else f"{C} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            yield (f"sup_{vk}_triple_{i}", p_rel, p_neu)
        for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
            A, B, C, D_ent = ents[iA], ents[iB], ents[iC], ents[iD]
            q_opts = f"{A} or {D_ent}" if (i % 2 == 0) else f"{D_ent} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
            yield (f"sup_{vk}_quad_{i}", p_rel, p_neu)


# ---- Verbatim from run_exp077.py (lines 251-294) ----
def build_candidate_directions(delta_h_by_vocab, h_all):
    """Reconstruct v_hat_k, v_hat (=B_agg), mu, v_hat^c (protocol §3.1-3.2).

    v_hat_k = normalize(mean_i normalize(delta_h_i^(k)))
    v_hat   = normalize(sum_k v_hat_k)
    mu      = mean over all 300 support presentations (layer 20, last token)
    v_hat^c_k = normalize(v_hat_k - mu); v_hat^c = normalize(sum_k v_hat^c_k)

    Returns dict with all directions (CPU tensors) + diagnostics.
    """
    v_hats = []
    for vk in VOCAB_KEYS:
        dH = delta_h_by_vocab[vk]                       # [30, d]
        norms = torch.norm(dH, dim=1, keepdim=True) + 1e-12
        mean_v = (dH / norms).mean(dim=0)
        v_hats.append(mean_v / (torch.norm(mean_v) + 1e-12))
    V = torch.stack(v_hats, dim=1)                      # [d, 5]
    sum_v = V.sum(dim=1)
    v_hat = sum_v / (torch.norm(sum_v) + 1e-12)

    # Continuity assertion input (§5): mean cos(v_hat_1, v_hat_k) >= 0.50.
    cos_v1 = [float(torch.dot(v_hats[0], v_hats[k]).item()) for k in range(5)]
    mean_cos_v1 = float(np.mean(cos_v1))

    # Offset-removed direction (§3.2): global centring, then renormalize.
    # The spec registers v_hat^c_k = normalize(v_hat_k - mu) with the RAW
    # mean mu -- no unit-normalization of mu (MAJOR-1 repair: the builder's
    # "unit for stability" line changed the registered intervention).
    mu = torch.stack(h_all, dim=0).mean(dim=0)          # [d]
    vhatc_ks, amplifications = [], []
    for k in range(5):
        diff = v_hats[k] - mu
        amp = float(torch.norm(diff).item())            # 1/amp = amplification
        amplifications.append(amp)
        vhatc_ks.append(diff / (amp + 1e-12))
    Vc = torch.stack(vhatc_ks, dim=1)
    sum_vc = Vc.sum(dim=1)
    v_hat_c = sum_vc / (torch.norm(sum_vc) + 1e-12)
    return {
        "v_hats": v_hats, "v_hat": v_hat, "mu": mu,
        "v_hat_c": v_hat_c, "v_hat_c_ks": vhatc_ks,
        "amplifications": amplifications,
        "cos_v1": cos_v1, "mean_cos_v1": mean_cos_v1,
    }
