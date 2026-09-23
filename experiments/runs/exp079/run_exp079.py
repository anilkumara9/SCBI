"""
EXP079 runner: Oracle-Selection Ceiling with Out-of-Sample Probe (pre-registered).

Protocol (DO NOT MODIFY): experiments/protocols/EXP079_BETTER_PROBE_PREREG_SPEC.md
(prereg draft LOG-119, Law #14 review LOG-120, PRE-REGISTERED LOG-121).

Design delta vs EXP070 (the mandated better-probe re-registration, LOG-110):
  (1) Split-half support: the 150 support contrast pairs (5 vocabularies x 30,
      indexed 0-29 in the loop spec's construction order, identical to EXP070's
      support construction) are split deterministically by even/odd
      index_in_vocab into BUILD (75 pairs: 15/vocab, even) for ALL candidate
      construction and HELDOUT (75 pairs: 15/vocab, odd) for probing only.
  (2) Out-of-sample oracle probe: per test instance, HELDOUT support pairs
      matching (hop, index-pattern) -- the same (hop, index-pattern) key
      EXP070's probe used (reversal flag not part of the key) -- sorted by
      lowest global pair-index first (vocab_order*30 + index_in_vocab),
      capped at 15 items, minimum 8; each pair contributes its labeled
      (p_rel, target, foil) item. Probe labels are SUPPORT labels (permitted
      ceiling measurement, §1.1).
  (3) Calibrated probe-signal gate: H_sel against the 95th-pct
      Multinomial(N_final, 1/17) null bar computed at RUNTIME with the realized
      N_final (seed 7979), replacing EXP070's fixed 0.25 floor.
  (4) BUILD-half B_agg for C2 (CAA-equivalent benchmark on the same data the
      pool sees).
  (5) Third disjointness assertion: probe item ids cap BUILD item ids = empty
      (closes the in-sample path that degenerated EXP070's probe).

Scope: IN-SCOPE only -- EleutherAI/pythia-160m, layer 10, alpha=0.50.
Frozen backbone: Delta theta = 0 (binding pre/post SHA-256 parameter guard).

Conservative readings adopted (documented, not improvised):
  R1. Oracle selection score = mean BINARY CORRECTNESS over probe items
      (spec §3.3: r(B;q) = 1[correct on q]; unchanged from EXP070 §3.3, whose
      code implements correctness-rate argmax). The "probe margin" in
      diagnostic (ii) is winner_rate - B_agg_rate (correctness rates), per §6.
  R2. G1 bootstrap: 15-with-replacement draws per vocabulary over that
      vocab's 15 BUILD (even-indexed) Delta_h (EXP070's 30-from-30 analog);
      Dirichlet(1x5) over the 5 vocabularies (seeds 7001/7002).
  R3. Pilot degeneracy HALT (§9: "if the pilot reproduces EXP070's degeneracy,
      HALT"): tie_rate = fraction of the 5 pilot instances whose oracle
      argmax was tied (n_tied > 1); HALT_DEGENERACY if tie_rate >= 4/5.
      (EXP070's degeneracy was near-ceiling ties making the seeded tie-break
      the effective selector; §9 EXPECTS "ties rare".) Diagnostics (i)/(iii)
      are reported on the pilot as sanity signals, not rulings.
  R4. B_star (Law #13 "best BUILD-only candidate direction") excludes the
      B_agg incumbent from the argmax -- B_agg is an aggregate, not a single
      candidate direction.

Mechanical requirements: torch_dtype=torch.float32, no constant shadowing,
device-consistent tensors, get_output_embeddings().weight, real-tokenizer
F2-style single-token guard on test entities (hard halt) + logged token audit
on the inherited support entities (11/25 are 2-token; first-token probe
matching is EXP070's method, disclosed not silent), Deltaθ=0 pre/post
hash, complete Law #13 archives.
"""

import os
import sys
import json
import math
import hashlib

import numpy as np
import torch
from scipy import stats
from transformers import AutoTokenizer, AutoModelForCausalLM

# ----------------------------------------------------------------------------
# Pre-registered constants (protocol §2/§3/§5/§9/§10)
# ----------------------------------------------------------------------------
MODEL_NAME = "EleutherAI/pythia-160m"
TARGET_LAYER = 10          # l* = 10 (83% depth)
ALPHA = 0.50               # fixed intervention strength
D = 768                    # residual-stream width

SEED_TORCH = 20260923      # master seed
SEED_G1_BOOT = 7001        # G1 bootstrap resample
SEED_G1_DIR = 7002         # G1 Dirichlet weights
SEED_G2_RING = 7003        # G2-ring perturbations
SEED_TIEBREAK = 7005       # oracle tie-break draw (archived per instance)
SEED_HSEL_NULL = 7979      # H_sel null Monte Carlo (runtime, §8)

N_G1 = 8                   # G1 draws
N_RING = 8                 # one G2-ring draw per G1 candidate
N_POOL = N_G1 + N_RING + 1 # 17 = 8 + 8 + B_agg incumbent
SIGMA_RING = 0.1           # perturbation scale (loop spec default)

N_PROBE_CAP = 15           # protocol §3.2: up to 15 held-out probe items
N_PROBE_MIN = 8            # protocol §3.2: minimum probe size
N_FINAL_MIN = 50           # protocol §5 power floor
HEADROOM_LO, HEADROOM_HI = 0.40, 0.70  # protocol §5
PILOT_N = 5                # protocol §9: 5-instance pilot
PILOT_TIE_RATE_HALT = 0.8  # R3: degeneracy = ties ubiquitous (>=4/5 tied)
KL_GUARD = 0.50            # KL_div guardrail (exploratory, inherited)

# Support vocabularies: identical to EXP070's support construction (5 x 30).
SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Caleb", "Gideon", "Miriam", "Reuben"],
    "V3_Greek": ["Hector", "Jason", "Nestor", "Paris", "Priam"],
    "V4_Roman": ["Marcus", "Lucius", "Titus", "Felix", "Silas"],
    "V5_Modern": ["Liam", "Noah", "Sora", "Maya", "Leila"],
}
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())

# Loop-spec index patterns (identical to EXP065/EXP070).
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

# Benchmark: identical N=60 Planetary/Elemental 2-hop/3-hop suite (protocol §5).
NOVEL_PLANET = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
NOVEL_ELEMENT = ["Iron", "Gold", "Silver", "Bronze", "Steel"]


# ----------------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------------
def log(msg, log_file=None):
    print(msg, flush=True)
    if log_file is not None:
        log_file.write(msg + "\n")
        log_file.flush()


def param_hash(model):
    """Binding Deltaθ=0 guard: SHA-256 over sorted state_dict tensors (CPU, f32)."""
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu().to(torch.float32).contiguous()
        h.update(k.encode())
        h.update(t.numpy().tobytes())
    return h.hexdigest()


def guard_single_token(tok, entities, who):
    """F2-style real-tokenizer guard: every entity must be exactly one token.

    Raises SystemExit (loud halt) on the first multi-token entity -- a silent
    [0]-index truncation (the EXP066 lesson) must be impossible, not absent.
    """
    bad = []
    for e in entities:
        ids = tok.encode(" " + e, add_special_tokens=False)
        if len(ids) != 1:
            bad.append((e, len(ids)))
    if bad:
        print(f"FATAL (F2-style tokenizer guard) in {who}: multi-token entities "
              f"(would silently truncate): {bad}", flush=True)
        sys.exit(1)


def paired_stats(a_correct, b_correct):
    """McNemar exact two-sided test on paired binary decisions (M5.3).

    b = a rescues, c = a corrupts; exact_p = 2*P(Bin(b+c,0.5) <= min(b,c)).
    """
    a = np.asarray(a_correct, dtype=bool)
    b_ = np.asarray(b_correct, dtype=bool)
    n = len(a)
    b = int(np.sum(a & ~b_))
    c = int(np.sum(~a & b_))
    dm = float(np.mean(a.astype(float) - b_.astype(float)))
    if b + c == 0:
        p = 1.0
    else:
        p = float(2.0 * stats.binom.cdf(min(b, c), b + c, 0.5))
        p = min(p, 1.0)
    return {"delta_m": dm, "b": b, "c": c, "exact_p": p, "n": n}


def compute_hsel_null_bar(N_final, n_draws=100000, seed=SEED_HSEL_NULL):
    """Calibrated H_sel null bar (protocol §8): 95th percentile of
    max_j Multinomial(N_final, 1/17)/N_final, seed 7979, computed at runtime
    with the REALIZED N_final. Verified: N=60 -> 0.150, N=50 -> 0.160."""
    rng = np.random.default_rng(seed)
    draws = rng.multinomial(N_final, [1.0 / N_POOL] * N_POOL, size=n_draws)
    hsel_null = draws.max(axis=1) / N_final
    return float(np.quantile(hsel_null, 0.95))


# ----------------------------------------------------------------------------
# Benchmark + support construction (identical items to EXP065/EXP070)
# ----------------------------------------------------------------------------
def build_test_items():
    """N=60 Planetary/Elemental 2-hop/3-hop suite (EXP070's exact items)."""
    test_items = []

    def _add(inst_id, hop, domain, prompt, target, foil, pattern, reversed_flag):
        test_items.append({
            "id": inst_id, "hop": hop, "domain": domain, "prompt": prompt,
            "target": target, "foil": foil,
            "target_token": " " + target, "foil_token": " " + foil,
            "sig": {"hop": hop, "reversed": reversed_flag, "pattern": list(pattern)},
        })

    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_PLANET[iA], NOVEL_PLANET[iB], NOVEL_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp079_planet_2hop_{i}", 2, "Planetary", p, A, C, (iA, iB, iC), is_rev)
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = NOVEL_PLANET[iA], NOVEL_PLANET[iB], NOVEL_PLANET[iC], NOVEL_PLANET[iD]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp079_planet_3hop_{i}", 3, "Planetary", p, A, D_ent, (iA, iB, iC, iD), is_rev)
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_ELEMENT[iA], NOVEL_ELEMENT[iB], NOVEL_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp079_element_2hop_{i}", 2, "Elemental", p, A, C, (iA, iB, iC), is_rev)
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = NOVEL_ELEMENT[iA], NOVEL_ELEMENT[iB], NOVEL_ELEMENT[iC], NOVEL_ELEMENT[iD]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp079_element_3hop_{i}", 3, "Elemental", p, A, D_ent, (iA, iB, iC, iD), is_rev)
    assert len(test_items) == 60, f"Expected 60 test instances, got {len(test_items)}"
    return test_items


def build_support_metadata():
    """Support metadata (no model needed): 5 vocabs x 30 pairs.

    Identical to EXP070's support construction: per vocabulary, 15 triples
    (index_in_vocab 0..14) + 15 quads (15..29); each pair = (p_rel, p_neu)
    contrast plus its LABELED probe item (p_rel, target, foil).
    """
    meta = {}  # vk -> list of 30 pair dicts
    for vi, (vk, ents) in enumerate(SUPPORT_VOCABULARIES.items()):
        pairs = []
        for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
            A, B, C = ents[iA], ents[iB], ents[iC]
            q_opts = f"{A} or {C}" if (i % 2 == 0) else f"{C} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            pairs.append({
                "id": f"sup_{vk}_triple_{i}", "vocab": vk, "vocab_order": vi,
                "hop": 2, "pattern": (iA, iB, iC), "index_in_vocab": i,
                "global_index": vi * 30 + i,
                "p_rel": p_rel, "p_neu": p_neu,
                "target": A, "foil": C,
                "target_token": " " + A, "foil_token": " " + C,
            })
        for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
            A, B, C, D_ent = ents[iA], ents[iB], ents[iC], ents[iD]
            q_opts = f"{A} or {D_ent}" if (i % 2 == 0) else f"{D_ent} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
            pairs.append({
                "id": f"sup_{vk}_quad_{i}", "vocab": vk, "vocab_order": vi,
                "hop": 3, "pattern": (iA, iB, iC, iD), "index_in_vocab": 15 + i,
                "global_index": vi * 30 + 15 + i,
                "p_rel": p_rel, "p_neu": p_neu,
                "target": A, "foil": D_ent,
                "target_token": " " + A, "foil_token": " " + D_ent,
            })
        assert len(pairs) == 30
        meta[vk] = pairs
    return meta


def split_support(meta):
    """Deterministic even/odd split within each vocabulary (protocol §3.2).

    BUILD = even index_in_vocab (15/vocab -> 75 pairs), candidate construction.
    HELDOUT = odd index_in_vocab (15/vocab -> 75 pairs), probing only.
    """
    build_idx, heldout_idx = {}, {}
    for vk in VOCAB_KEYS:
        b = [i for i, s in enumerate(meta[vk]) if s["index_in_vocab"] % 2 == 0]
        h = [i for i, s in enumerate(meta[vk]) if s["index_in_vocab"] % 2 == 1]
        assert len(b) == 15 and len(h) == 15, f"{vk}: BUILD={len(b)}, HELDOUT={len(h)}"
        assert set(b).isdisjoint(set(h))
        build_idx[vk], heldout_idx[vk] = b, h
    n_build = sum(len(v) for v in build_idx.values())
    n_held = sum(len(v) for v in heldout_idx.values())
    assert n_build == 75 and n_held == 75, f"BUILD={n_build}, HELDOUT={n_held}"
    return build_idx, heldout_idx


def build_probe_map(test_items, meta, heldout_idx):
    """Out-of-sample oracle probe π(x) (protocol §3.2).

    Per test instance: HELDOUT support pairs matching (hop, index-pattern)
    -- the same key EXP070's probe used (reversal flag not part of the key) --
    sorted by lowest global pair-index first, capped at 15 items, minimum 8.
    Each pair contributes its LABELED (p_rel, target, foil) item.
    """
    probe_map, probe_ids, excluded = {}, [], []
    n_probe_dist = []
    for t in test_items:
        sig = t["sig"]
        cands = []
        for vk in VOCAB_KEYS:
            for i in heldout_idx[vk]:
                s = meta[vk][i]
                if s["hop"] == sig["hop"] and tuple(s["pattern"]) == tuple(sig["pattern"]):
                    cands.append(s)
        cands.sort(key=lambda s: s["global_index"])
        chosen = cands[:N_PROBE_CAP]
        n_probe_dist.append(len(chosen))
        if len(chosen) < N_PROBE_MIN:
            excluded.append(t["id"])
        else:
            probe_map[t["id"]] = chosen
            probe_ids.extend([s["id"] for s in chosen])
    return probe_map, probe_ids, excluded, n_probe_dist


def compute_delta_h(model, tok_fn, device, meta):
    """Contrast vectors: Delta_h = h(p_rel) - h(p_neu) at layer l*, last token.

    Identical to EXP070's support construction. tok_fn(prompt) -> input_ids
    tensor on device. Returns {vk: [30, d] tensor (CPU)}.
    """
    delta_h_by_vocab = {}
    for vk in VOCAB_KEYS:
        vecs = []
        with torch.no_grad():
            for s in meta[vk]:
                o_rel = model(input_ids=tok_fn(s["p_rel"]),
                              output_hidden_states=True)
                o_neu = model(input_ids=tok_fn(s["p_neu"]),
                              output_hidden_states=True)
                dh = (o_rel.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
                      - o_neu.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu())
                vecs.append(dh)
        delta_h_by_vocab[vk] = torch.stack(vecs)
    return delta_h_by_vocab


def build_pool(delta_h_by_vocab, build_idx):
    """17-family candidate pool, BUILD half only (protocol §3.1; R2).

    v_hat per vocab = normalized mean of normalized BUILD Delta_h;
    B_agg = normalized sum of the 5 v_hat; G1 x8 = Dirichlet(1x5)-weighted
    aggregate of per-vocab bootstrap means (15-with-replacement over the
    vocab's 15 BUILD Delta_h); G2-ring x8 = G1[i] + N(0, 0.1, d).
    """
    rng_boot = np.random.default_rng(SEED_G1_BOOT)
    rng_dir = np.random.default_rng(SEED_G1_DIR)
    rng_ring = np.random.default_rng(SEED_G2_RING)

    v_hat_build = {}
    for vk in VOCAB_KEYS:
        dH = delta_h_by_vocab[vk][build_idx[vk]]          # [15, d]
        norms = torch.norm(dH, dim=1, keepdim=True) + 1e-12
        mv = (dH / norms).mean(dim=0)
        v_hat_build[vk] = mv / (torch.norm(mv) + 1e-12)
    sum_v = torch.stack([v_hat_build[vk] for vk in VOCAB_KEYS]).sum(dim=0)
    B_agg = sum_v / (torch.norm(sum_v) + 1e-12)

    pool, pool_meta, g1_draws = [], [], []
    for i in range(N_G1):
        per_vocab_means, resample_idx = [], {}
        for vk in VOCAB_KEYS:
            idx = rng_boot.integers(0, 15, 15)            # 15 w/ replacement, R2
            resample_idx[vk] = idx.tolist()
            dH_r = delta_h_by_vocab[vk][[build_idx[vk][k] for k in idx]]
            nr = torch.norm(dH_r, dim=1, keepdim=True) + 1e-12
            mv = (dH_r / nr).mean(dim=0)
            per_vocab_means.append(mv / (torch.norm(mv) + 1e-12))
        w = rng_dir.dirichlet(np.ones(5))
        agg = sum(float(w[k]) * per_vocab_means[k] for k in range(5))
        v_i = agg / (torch.norm(agg) + 1e-12)
        pool.append(v_i)
        g1_draws.append(v_i)
        pool_meta.append({"family": "G1", "draw": i,
                          "resample_indices": resample_idx,
                          "dirichlet_weights": [float(x) for x in w]})
    for i in range(N_RING):
        eps = torch.from_numpy(rng_ring.normal(0.0, SIGMA_RING, size=D).astype(np.float32))
        v_r = g1_draws[i] + eps
        v_r = v_r / (torch.norm(v_r) + 1e-12)
        pool.append(v_r)
        pool_meta.append({"family": "G2-ring", "draw": i, "parent_G1": i,
                          "sigma": SIGMA_RING,
                          "epsilon_norm": float(torch.norm(eps).item()),
                          "cos_to_parent": float(torch.dot(v_r, g1_draws[i]).item())})
    pool.append(B_agg)
    pool_meta.append({"family": "incumbent", "draw": 0,
                      "note": "B_agg static basis (BUILD half)"})
    assert len(pool) == N_POOL == 17
    for j, v in enumerate(pool):
        assert abs(float(torch.norm(v).item()) - 1.0) < 1e-5, f"pool[{j}] not unit"
        assert float(torch.norm(v).item()) > 0, f"FATAL (F1): pool[{j}] zero norm"
    return pool, pool_meta, B_agg, v_hat_build


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    torch.manual_seed(SEED_TORCH)
    np.random.seed(SEED_TORCH)
    try:
        torch.use_deterministic_algorithms(True)
    except Exception as e:
        print(f"WARNING: deterministic algorithms unavailable ({e}); continuing.", flush=True)

    out_dir = os.path.join("experiments", "runs", "EXP079_better_probe")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp079_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")
    state = {"pre_hash": None, "model": None}

    def save_halt(outcome, reason, extra):
        payload = {
            "experiment": "EXP079",
            "model": MODEL_NAME,
            "protocol_scope": "IN-SCOPE (pythia-160m, layer 10, alpha=0.50)",
            "outcome": outcome,
            "halt_reason": reason,
            "pre_hash": state["pre_hash"],
            "post_hash": param_hash(state["model"]) if state["model"] is not None else None,
            "target_layer": TARGET_LAYER,
            "hidden_dim": D,
            "alpha": ALPHA,
            "n_pool": N_POOL,
        }
        payload.update(extra)
        with open(os.path.join(out_dir, "exp079_results.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        log("=" * 80, log_file)
        log(f"{outcome}: {reason}", log_file)
        log("THIS HALT IS THE REPORTABLE OUTCOME OF EXP079 (protocol §8 branch (a)).", log_file)
        log(f"Diagnostics written to {out_dir}/exp079_results.json", log_file)
        log("=" * 80, log_file)
        log_file.close()
        print(f"{outcome} -- THIS IS THE RESULT. Download exp079_results.json and report it.",
              flush=True)
        sys.exit(0)

    # ---- CUDA gate: this experiment is GPU-only by design ----
    if not torch.cuda.is_available():
        print("FATAL: EXP079 requires a CUDA GPU (Kaggle T4 x2 / Colab T4). "
              "CPU execution is refused by design -- aborting.", flush=True)
        sys.exit(1)
    device = torch.device("cuda:0")
    log(f"Device: {torch.cuda.get_device_name(0)}; cuda={torch.cuda.is_available()}", log_file)

    # ---- Tokenizer + F2-style single-token guard (test AND support entities) ----
    tok = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=False)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    test_ents = list(dict.fromkeys(NOVEL_PLANET + NOVEL_ELEMENT))
    support_ents = list(dict.fromkeys(e for v in SUPPORT_VOCABULARIES.values() for e in v))
    # Hard F2-style guard on TEST entities: the benchmark's correctness claims
    # assume single-token targets/foils; a multi-token test entity would
    # silently truncate (the EXP066 lesson) -- impossible, not absent.
    guard_single_token(tok, test_ents, "test entities")
    log(f"Tokenizer guard PASSED: {len(test_ents)} test entities all single-token.",
        log_file)
    # Support entities: 11 of the 25 inherited EXP070 names are 2-token under
    # the pythia tokenizer. The signed protocol mandates EXP070's support
    # construction verbatim, so substitution would be a protocol change (new
    # experiment number, Law #4) -- NOT done here. Probe correctness therefore
    # uses first-token matching, exactly as EXP070's code did
    # (tokenizer.encode(...)[0]). This is a DISCLOSED property (logged below),
    # not a silent truncation: every candidate faces the same probe items, so
    # the oracle-vs-static comparison is unaffected by construction.
    _sup_tok_audit = {e: len(tok.encode(" " + e, add_special_tokens=False))
                      for e in support_ents}
    _multi = sorted(e for e, n in _sup_tok_audit.items() if n > 1)
    log(f"Support-entity token audit (Law #13): {_sup_tok_audit}", log_file)
    log(f"Support entities with >1 token (first-token probe matching, EXP070 "
        f"method, disclosed): {_multi}", log_file)

    def tok_fn(prompt):
        return tok(prompt, return_tensors="pt")["input_ids"].to(device)

    # ---- Model (float32; device-safe hook vectors, LOG-116 lesson) ----
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, torch_dtype=torch.float32, trust_remote_code=False).to(device)
    model.eval()
    state["model"] = model
    log("Model loaded (float32).", log_file)

    # ---- Support metadata + deterministic even/odd split (metadata, no GPU) ----
    meta = build_support_metadata()
    build_idx, heldout_idx = split_support(meta)
    log("Split-half support: BUILD=75 pairs (even indices), HELDOUT=75 pairs (odd).", log_file)

    # ---- Benchmark (identical N=60 items) ----
    test_items = build_test_items()
    test_ids = [t["id"] for t in test_items]

    # ---- Probe-construction / N_final gate (metadata, §9 step 1) ----
    probe_map, probe_ids, excluded, n_probe_dist = build_probe_map(test_items, meta, heldout_idx)
    N_final = len(probe_map)
    log(f"Probe map: {N_final}/60 instances have >= {N_PROBE_MIN} HELDOUT probe items "
        f"({len(excluded)} excluded).", log_file)
    if n_probe_dist:
        log(f"Probe-size distribution (all 60): min={min(n_probe_dist)}, "
            f"max={max(n_probe_dist)}.", log_file)
    support_ids = [s["id"] for vk in VOCAB_KEYS for s in meta[vk]]
    build_ids = [meta[vk][i]["id"] for vk in VOCAB_KEYS for i in build_idx[vk]]
    # Three disjointness assertions (protocol §3.2/§3.5) -- evaluated here on
    # metadata so the gate fires before GPU spend.
    _ov1 = set(probe_ids).intersection(set(test_ids))
    assert len(_ov1) == 0, f"FATAL (anti-cheat): probe ∩ test = {sorted(_ov1)}"
    _ov2 = set(support_ids).intersection(set(test_ids))
    assert len(_ov2) == 0, f"FATAL (anti-cheat): support ∩ test = {sorted(_ov2)}"
    _ov3 = set(probe_ids).intersection(set(build_ids))
    assert len(_ov3) == 0, f"FATAL (anti-cheat): probe ∩ BUILD = {sorted(_ov3)}"
    log("Anti-cheat assertions PASSED: probe∩test=∅, support∩test=∅, probe∩BUILD=∅.",
        log_file)
    if N_final < N_FINAL_MIN:
        save_halt("HALT_PROBE",
                  f"probe-construction gate failed: N_final={N_final} < {N_FINAL_MIN} "
                  f"(protocol §3.2, §5; reportable, not adjustable under EXP079)",
                  {"N_final": N_final, "excluded": excluded,
                   "n_probe_dist": n_probe_dist,
                   "probe_gate": None,
                   "build_n": 75, "heldout_n": 75})
    final_instances = [t for t in test_items if t["id"] in probe_map]
    log(f"N_final = {len(final_instances)} instances proceed.", log_file)

    # ---- Frozen-backbone binding guard (pre) ----
    pre_hash = param_hash(model)
    state["pre_hash"] = pre_hash
    log(f"Pre-run parameter hash: {pre_hash}", log_file)

    # ---- Support contrast vectors (GPU) ----
    log("Building support contrast vectors (150 pairs x 2 prompts) ...", log_file)
    delta_h_by_vocab = compute_delta_h(model, tok_fn, device, meta)
    for vk in VOCAB_KEYS:
        assert delta_h_by_vocab[vk].shape == (30, D)
    log("Support Delta_h: 5 x [30, 768].", log_file)

    # ---- Candidate pool (BUILD half only) ----
    pool, pool_meta, B_agg, v_hat_build = build_pool(delta_h_by_vocab, build_idx)
    ring_cos = [m["cos_to_parent"] for m in pool_meta if m["family"] == "G2-ring"]
    log(f"Pool P built: {N_POOL} unit directions (8 G1 + 8 G2-ring + BUILD B_agg).", log_file)
    log(f"G2-ring parent cosines: mean={float(np.mean(ring_cos)):.3f} "
        f"(spec §3.1: E[cos]≈0.34 at sigma=0.1, d=768).", log_file)

    # ---- Intervention harness (hook at l*, last-token position) ----
    def run_with_intervention(prompt, t_tok_str, f_tok_str, vec):
        """Single forward with h <- h + alpha*vec at TARGET_LAYER (last token).

        Returns (correct, prob_target, prob_foil, kl_div). vec is moved to the
        hook's device inside the hook (LOG-116 lesson: never assume vec lives
        on the model's device).
        """
        t_tok = tok.encode(t_tok_str, add_special_tokens=False)[0]
        f_tok = tok.encode(f_tok_str, add_special_tokens=False)[0]
        inp_ids = tok_fn(prompt)

        def hook_fn(module, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            h = h.clone()
            h[:, -1, :] = h[:, -1, :] + vec.to(h.device)
            return (h,) + tuple(outp[1:]) if isinstance(outp, tuple) else h

        target_layer_mod = model.gpt_neox.layers[TARGET_LAYER]
        handle = target_layer_mod.register_forward_hook(hook_fn)
        try:
            with torch.no_grad():
                out = model(input_ids=inp_ids, output_hidden_states=False)
                logits = out.logits[0, -1, :]
                probs = torch.softmax(logits, dim=-1)
                pt = float(probs[t_tok].item())
                pf = float(probs[f_tok].item())
        finally:
            handle.remove()
        with torch.no_grad():
            out_b = model(input_ids=inp_ids)
            probs_b = torch.softmax(out_b.logits[0, -1, :], dim=-1)
        kl = float((probs_b * (torch.log(probs_b + 1e-12)
                               - torch.log(probs + 1e-12))).sum().item())
        top1 = int(torch.argmax(logits).item())
        return (top1 == t_tok), pt, pf, kl

    def run_baseline(prompt, t_tok_str, f_tok_str):
        t_tok = tok.encode(t_tok_str, add_special_tokens=False)[0]
        f_tok = tok.encode(f_tok_str, add_special_tokens=False)[0]
        inp_ids = tok_fn(prompt)
        with torch.no_grad():
            out = model(input_ids=inp_ids)
            logits = out.logits[0, -1, :]
            probs = torch.softmax(logits, dim=-1)
        top1 = int(torch.argmax(logits).item())
        return (top1 == t_tok), float(probs[t_tok].item()), float(probs[f_tok].item())

    # ---- Baseline / headroom gate (§5) ----
    base_by_id = {}
    for t in test_items:
        corr, _, _ = run_baseline(t["prompt"], t["target_token"], t["foil_token"])
        base_by_id[t["id"]] = bool(corr)
    base_acc = float(np.mean(list(base_by_id.values())))
    log(f"Baseline C1 accuracy: {base_acc*100:.2f}% "
        f"({int(sum(base_by_id.values()))}/{len(test_items)}); "
        f"headroom gate [{HEADROOM_LO*100:.0f}%, {HEADROOM_HI*100:.0f}%].", log_file)
    if not (HEADROOM_LO <= base_acc <= HEADROOM_HI):
        save_halt("HALT_HEADROOM",
                  f"headroom gate failed: baseline={base_acc:.4f} outside "
                  f"[{HEADROOM_LO}, {HEADROOM_HI}] (protocol §5; reportable)",
                  {"baseline_accuracy": base_acc, "N_final": N_final})

    # ---- Oracle probe evaluation + selection (protocol §3.2, §3.3; R1) ----
    # r(B;q) = 1[correct on q]; B*(x) = argmax mean correctness; ties by
    # seeded uniform draw (seed 7005), direction-neutral in expectation.
    log(f"Oracle probe evaluation ({N_POOL} candidates x up to {N_PROBE_CAP} "
        f"probes x {N_final} instances) ...", log_file)
    gen_tie = torch.Generator().manual_seed(SEED_TIEBREAK)
    probe_records = {}
    import time as _time
    t_probe_start = _time.time()

    def evaluate_probes(t):
        """Probe phase for one instance; returns the probe record dict."""
        probes = probe_map[t["id"]]
        scores = np.zeros(N_POOL)  # mean correctness per candidate
        for j, B in enumerate(pool):
            vec = ALPHA * B
            r = 0
            for q in probes:
                corr, _, _, _ = run_with_intervention(
                    q["p_rel"], q["target_token"], q["foil_token"], vec)
                r += int(corr)
            scores[j] = r / len(probes)
        best = float(scores.max())
        tied = [j for j in range(N_POOL) if scores[j] == best]
        if len(tied) == 1:
            sel, draw = tied[0], None
        else:
            draw = int(torch.randint(len(tied), (1,), generator=gen_tie).item())
            sel = tied[draw]
        _sn = float(torch.norm(pool[sel]).item())
        assert _sn > 0, f"FATAL (F1 guard): oracle selected zero-norm pool[{sel}]."
        return {
            "probe_scores": [float(s) for s in scores],
            "selected_idx": int(sel),
            "tie_draw": draw,
            "n_tied": len(tied),
            "winner_rate": float(best),
            "bagg_rate": float(scores[N_POOL - 1]),  # incumbent is pool[16]
            "probe_item_ids": [q["id"] for q in probes],
        }

    # ---- Stage A: 5-instance pilot (§9; R3) ----
    pilot = final_instances[:PILOT_N]
    log(f"STAGE A: 5-instance pilot on {[t['id'] for t in pilot]} ...", log_file)
    for t in pilot:
        probe_records[t["id"]] = evaluate_probes(t)
    _recs = [probe_records[t["id"]] for t in pilot]
    _diag_i = float(np.mean([1.0 if r["winner_rate"] > r["bagg_rate"] else 0.0 for r in _recs]))
    _tie_rate = float(np.mean([1.0 if r["n_tied"] > 1 else 0.0 for r in _recs]))
    _cnt = np.zeros(N_POOL, dtype=int)
    for r in _recs:
        _cnt[r["selected_idx"]] += 1
    _hsel = float(_cnt.max() / PILOT_N)
    log(f"PILOT diagnostics (sanity signals, not a ruling): (i) oracle-beats-B_agg "
        f"on probe = {_diag_i*100:.1f}%; tie_rate = {_tie_rate:.2f} "
        f"(tied argmax on {_tie_rate*PILOT_N:.0f}/{PILOT_N}); "
        f"(iii) H_sel = {_hsel:.3f} (noise floor ~{1/N_POOL:.3f}).", log_file)
    if _tie_rate >= PILOT_TIE_RATE_HALT:
        save_halt("HALT_DEGENERACY",
                  f"5-instance pilot reproduces EXP070's degeneracy: tied oracle argmax "
                  f"on {_tie_rate*100:.0f}% of pilot instances (>= "
                  f"{PILOT_TIE_RATE_HALT*100:.0f}% bar, R3) -- the seeded tie-break "
                  f"would be the effective selector. Diagnose before the full spend "
                  f"(protocol §9; reportable).",
                  {"N_final": N_final, "baseline_accuracy": base_acc,
                   "pilot_diag_i": _diag_i, "pilot_tie_rate": _tie_rate,
                   "pilot_H_sel": _hsel,
                   "pilot_ids": [t["id"] for t in pilot]})
    log("PILOT PASSED: no degeneracy -- proceeding to the full probe evaluation.", log_file)

    # ---- Stage B: full probe evaluation ----
    for n_done, t in enumerate(final_instances):
        if t["id"] in probe_records:
            continue  # pilot instances already evaluated
        probe_records[t["id"]] = evaluate_probes(t)
        if (n_done + 1) % 10 == 0:
            el = _time.time() - t_probe_start
            log(f"  ... {n_done + 1}/{N_final} instances ({el:.0f}s elapsed)", log_file)
    t_probe = _time.time() - t_probe_start
    log(f"Oracle probe complete: {N_final} instances x {N_POOL} candidates "
        f"({t_probe/60:.1f} min).", log_file)

    # ---- Static injection-vector norm (F1 guard) ----
    _inorm = float(torch.norm(ALPHA * B_agg).item())
    assert _inorm > 0, "FATAL (F1 guard): C2 static vector has zero norm -- silent no-op."
    log(f"Static injection-vector norm (F1 guard): {_inorm:.6f} > 0.", log_file)

    # ---- Conditions C1..C7 (protocol §4) ----
    def make_bridge_vec(tt, ft):
        w = model.get_output_embeddings().weight[tt, :].detach() - \
            model.get_output_embeddings().weight[ft, :].detach()
        return w / (torch.norm(w) + 1e-12)

    def eval_condition(cond_name, vec_fn):
        correct, kls = [], []
        for t in final_instances:
            vec = vec_fn(t)
            corr, _, _, kl = run_with_intervention(
                t["prompt"], t["target_token"], t["foil_token"], vec)
            correct.append(corr)
            kls.append(kl)
        acc = float(np.mean(correct))
        kl_mean = float(np.mean(kls))
        kl_ok = bool(kl_mean < KL_GUARD)
        log(f"{cond_name}: acc={acc*100:.2f}% KL_div={kl_mean:.4f} "
            f"(guardrail < {KL_GUARD}: {'PASS' if kl_ok else 'FAIL-exploratory'})", log_file)
        return {"accuracy": acc, "correct": [bool(x) for x in correct],
                "kl_div": kl_mean, "kl_ok": kl_ok}

    cond_results = {}
    cond_results["C1_Baseline"] = {
        "accuracy": float(np.mean([base_by_id[t["id"]] for t in final_instances])),
        "correct": [bool(base_by_id[t["id"]]) for t in final_instances],
        "kl_div": 0.0, "kl_ok": True,
    }

    _bagg_vec = ALPHA * B_agg
    cond_results["C2_Static_B_agg"] = eval_condition("C2_Static_B_agg", lambda t: _bagg_vec)

    def _c3_fn(t):
        sel = probe_records[t["id"]]["selected_idx"]
        return ALPHA * pool[sel]
    cond_results["C3_Oracle_Selected"] = eval_condition("C3_Oracle_Selected", _c3_fn)

    rng_c4 = np.random.default_rng(4242)
    _c4_idx = {t["id"]: int(rng_c4.integers(0, N_POOL)) for t in final_instances}
    cond_results["C4_Random_Selected"] = eval_condition(
        "C4_Random_Selected", lambda t: ALPHA * pool[_c4_idx[t["id"]]])

    def _c7_fn(t):
        tt = tok.encode(t["target_token"], add_special_tokens=False)[0]
        ft = tok.encode(t["foil_token"], add_special_tokens=False)[0]
        return ALPHA * make_bridge_vec(tt, ft)
    cond_results["C7_Output_Bridge"] = eval_condition("C7_Output_Bridge", _c7_fn)

    # ---- Comparisons: McNemar exact two-sided (M5.3) ----
    def _cmp(a_name, b_name):
        return paired_stats(cond_results[a_name]["correct"], cond_results[b_name]["correct"])

    comparisons = {
        "C3_vs_C2": _cmp("C3_Oracle_Selected", "C2_Static_B_agg"),
        "C3_vs_C4": _cmp("C3_Oracle_Selected", "C4_Random_Selected"),
        "C4_vs_C2": _cmp("C4_Random_Selected", "C2_Static_B_agg"),
        "C2_vs_C1": _cmp("C2_Static_B_agg", "C1_Baseline"),
        "C7_vs_C1": _cmp("C7_Output_Bridge", "C1_Baseline"),
    }
    for k, v in comparisons.items():
        log(f"{k}: ΔM={v['delta_m']*100:+.2f}pp b={v['b']} c={v['c']} "
            f"exact_p={v['exact_p']:.6f}", log_file)

    # ---- Probe-signal diagnostics + calibrated gate (protocol §6, §8; R1) ----
    winner_minus_bagg = np.array([probe_records[t["id"]]["winner_rate"]
                                  - probe_records[t["id"]]["bagg_rate"]
                                  for t in final_instances])
    c3_c = np.array(cond_results["C3_Oracle_Selected"]["correct"], dtype=float)
    c2_c = np.array(cond_results["C2_Static_B_agg"]["correct"], dtype=float)
    Y = ((c3_c == 1) & (c2_c == 0)).astype(float)
    n = N_final
    if np.std(winner_minus_bagg) > 0 and np.std(Y) > 0 and n > 2:
        r_pb = float(np.corrcoef(winner_minus_bagg, Y)[0, 1])
        t_stat = r_pb * math.sqrt((n - 2) / max(1e-12, 1 - r_pb ** 2))
        r_pb_p = float(stats.t.sf(t_stat, n - 2))  # one-sided
    else:
        r_pb, r_pb_p = 0.0, 1.0
    sel_idx_all = [probe_records[t["id"]]["selected_idx"] for t in final_instances]
    counts = np.bincount(sel_idx_all, minlength=N_POOL)
    H_sel = float(counts.max() / N_final)
    null_bar = compute_hsel_null_bar(N_final)
    gate_passed = bool((r_pb_p < 0.05) and (H_sel > null_bar))
    gate_path = ("(ii)-AND-(iii)" if gate_passed
                 else ("(ii)-fail" if not (r_pb_p < 0.05) else "(iii)-fail"))
    log(f"Probe-signal gate: r_pb={r_pb:.4f} one-sided p={r_pb_p:.6f}; "
        f"H_sel={H_sel:.4f} vs calibrated null bar={null_bar:.4f} "
        f"(Multinomial({N_final},1/17) 95th pct, seed {SEED_HSEL_NULL}); "
        f"gate={gate_path} -> {'PASS' if gate_passed else 'FAIL'}.", log_file)

    # ---- (g) consistency check: C2 replicates EXP065 null while C7 rescues ----
    c2_null = comparisons["C2_vs_C1"]
    c7_pos = comparisons["C7_vs_C1"]
    consistency_g = {
        "C2_replicates_EXP065_null": bool(c2_null["exact_p"] >= 0.05),
        "C7_rescues": bool((c7_pos["delta_m"] > 0) and (c7_pos["exact_p"] < 0.05)),
        "C2_discrepancy_flag": bool(abs(c2_null["delta_m"]) > 0
                                    and c2_null["exact_p"] < 0.05),
    }
    log(f"(g) consistency: C2 replicates EXP065 null: "
        f"{consistency_g['C2_replicates_EXP065_null']}; C7 rescues: "
        f"{consistency_g['C7_rescues']}; C2 discrepancy flag: "
        f"{consistency_g['C2_discrepancy_flag']}.", log_file)

    # ---- Frozen-backbone binding guard (post) ----
    post_hash = param_hash(model)
    log(f"Post-run parameter hash: {post_hash}", log_file)
    assert pre_hash == post_hash, \
        f"FATAL (Law #6): parameter hash changed mid-run ({pre_hash} -> {post_hash})."
    log("Deltaθ=0 VERIFIED: pre/post parameter hashes match.", log_file)

    # ---- Law #13 archives ----
    torch.save({"pool": [v.detach().cpu() for v in pool],
                "pool_meta": pool_meta,
                "B_agg": B_agg.detach().cpu(),
                "v_hat_build": {k: v.detach().cpu() for k, v in v_hat_build.items()},
                "delta_h_by_vocab": {k: v for k, v in delta_h_by_vocab.items()}},
               os.path.join(out_dir, "exp079_vectors.pt"))
    idx_of = {t["id"]: k for k, t in enumerate(final_instances)}
    instance_records = {}
    for t in final_instances:
        r = probe_records[t["id"]]
        k = idx_of[t["id"]]
        instance_records[t["id"]] = {
            "prompt": t["prompt"], "domain": t["domain"], "hop": t["hop"],
            "pattern": t["sig"]["pattern"],
            "probe_item_ids": r["probe_item_ids"],
            "n_probe_items": len(r["probe_item_ids"]),
            "probe_scores": r["probe_scores"],
            "selected_idx": r["selected_idx"],
            "selected_family": pool_meta[r["selected_idx"]]["family"],
            "tie_draw": r["tie_draw"], "n_tied": r["n_tied"],
            "winner_rate": r["winner_rate"], "bagg_rate": r["bagg_rate"],
            "C1": cond_results["C1_Baseline"]["correct"][k],
            "C2": cond_results["C2_Static_B_agg"]["correct"][k],
            "C3": cond_results["C3_Oracle_Selected"]["correct"][k],
            "C4": cond_results["C4_Random_Selected"]["correct"][k],
            "C7": cond_results["C7_Output_Bridge"]["correct"][k],
        }
    with open(os.path.join(out_dir, "exp079_instance_records.json"), "w", encoding="utf-8") as f:
        json.dump(instance_records, f, indent=2)

    # B_star: best single BUILD-only candidate direction (R4: excludes B_agg).
    def _cand_acc(j):
        c = [bool(run_with_intervention(
            t["prompt"], t["target_token"], t["foil_token"], ALPHA * pool[j])[0])
            for t in final_instances]
        return float(np.mean(c))

    B_star_idx = max(range(N_POOL - 1), key=_cand_acc)

    payload = {
        "experiment": "EXP079",
        "model": MODEL_NAME,
        "protocol_scope": "IN-SCOPE (pythia-160m, layer 10, alpha=0.50)",
        "outcome": "COMPLETED",
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "target_layer": TARGET_LAYER,
        "hidden_dim": D,
        "alpha": ALPHA,
        "n_pool": N_POOL,
        "baseline_accuracy": base_acc,
        "N_final": N_final,
        "excluded": excluded,
        "n_probe_dist": n_probe_dist,
        "build_n": 75,
        "heldout_n": 75,
        "pilot": {"diag_i": _diag_i, "tie_rate": _tie_rate, "H_sel": _hsel,
                  "ids": [t["id"] for t in pilot]},
        "probe_gate": {
            "r_pb": r_pb,
            "r_pb_one_sided_p": r_pb_p,
            "H_sel": H_sel,
            "H_sel_null_bar": null_bar,
            "H_sel_null_seed": SEED_HSEL_NULL,
            "H_sel_null_draws": 100000,
            "passed": gate_passed,
            "path": gate_path,
        },
        "stage_B_conditions": {
            name: {
                "accuracy": r["accuracy"],
                "delta_m": paired_stats(r["correct"],
                                        cond_results["C1_Baseline"]["correct"])["delta_m"],
                "rescues_b": paired_stats(r["correct"],
                                          cond_results["C1_Baseline"]["correct"])["b"],
                "corruptions_c": paired_stats(r["correct"],
                                              cond_results["C1_Baseline"]["correct"])["c"],
                "exact_p": paired_stats(r["correct"],
                                        cond_results["C1_Baseline"]["correct"])["exact_p"],
                "kl_div": r["kl_div"],
                "kl_ok": r["kl_ok"],
            } for name, r in cond_results.items()
        },
        "comparisons": {
            k: {"delta_m": v["delta_m"], "b": v["b"], "c": v["c"],
                "exact_p": v["exact_p"], "n": v["n"]}
            for k, v in comparisons.items()
        },
        "consistency_check_g": consistency_g,
        "B_star_idx": int(B_star_idx),
        "B_star_family": pool_meta[int(B_star_idx)]["family"],
        "seeds": {"torch": SEED_TORCH, "g1_boot": SEED_G1_BOOT,
                  "g1_dir": SEED_G1_DIR, "g2_ring": SEED_G2_RING,
                  "tiebreak": SEED_TIEBREAK, "hsel_null": SEED_HSEL_NULL,
                  "c4": 4242},
        "probe_time_min": t_probe / 60.0,
    }
    with open(os.path.join(out_dir, "exp079_results.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    log("=" * 80, log_file)
    log("EXP079 RUN COMPLETE. Now run: python evaluate_exp079.py "
        f"{out_dir}/exp079_results.json", log_file)
    log("=" * 80, log_file)
    log_file.close()


if __name__ == "__main__":
    main()
