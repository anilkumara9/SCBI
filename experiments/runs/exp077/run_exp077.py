"""
EXP077: Cone-vs-Line Geometry -- Is the Relational Concept Conical?
Pre-registered confirmatory protocol (SIGNED 2026-09-23):
    experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md

Core scientific question (protocol §1):
    Is the relational concept in the two-hop task conical (a cone of
    directions rescues) rather than a single line (one direction rescues)?

Mechanism (protocol §3):
    v_hat := B_agg reconstructed from the archived support set (5 vocabs x 30
    contrast pairs), exactly per theory/BOUNDARY_CLAIM_FORMALIZATION.md §2.
    v_hat^c: offset-removed direction (global centring, renormalized).
    Cone arm: K=8 directions u_j = normalize(v_hat cos φ_j + w_j sin φ_j),
    φ_j in {3.75°, ..., 30°}, w_j ⊥ v_hat from pinned seed 7701.
    Control arm: identical construction around pinned random r (seed 7702),
    assert |cos(r, v_hat)| < 0.5 at build.
    10 conditions: C1 baseline; C2-C5 v_hat at α in {0.25, 0.5, 1.0, 2.0};
    C6 offset-removed at α=1.0; C7 B_wrong (reported only); C8 output bridge
    (positive control / validity gate); C9 cone best-of-8 at α=1.0; C10
    control best-of-8 at α=1.0.

This is BOUNDARY science, not novelty science (protocol §1.1, N1 stands).
Two-way falsification: flat-zero kills the cone/affine hypothesis and
strengthens I1; a peaked α-curve or angular cone-wins withdraws the blanket
null in favor of a geometry-conditional claim.

Pipeline (protocol §9 order of operations):
    (1) support build + v_hat/mu/v_hat^c + continuity assertion (§5)
    (2) cone/control construction (CPU, pinned seeds) + build asserts
    (3) benchmark N=60 (EXP065-identical) + anti-cheat assert
    (4) C1 baseline + headroom gate (§5)            [branch (d) if fail]
    (5) C8 bridge gate (§5)                         [branch (d) if fail]
    (6) full launch: C2-C7, C9, C10 + endpoints (§4, §6)
Output directory: experiments/runs/EXP077_cone_vs_line/

Conservative readings of protocol ambiguities (all logged here, not improvised):
    - Support entity lists: the spec says "the archived support set" without
      enumerating entities. We use the F2-corrected EXP078 entity set (all 25
      support + 10 benchmark entities verified single-token under the real
      pythia-410m tokenizer) with the EXP066-identical construction procedure.
      The F2 guard re-verifies at runtime. (LOG-111 lesson.)
    - C8 (output bridge): protocol §4 names EXP066 `make_bridge_vec` verbatim
      and §5 calibrates the gate against EXP066 (+13.33pp, p=0.0078 at
      alpha=0.5). We implement v_output(x) = normalize(E[target] - E[foil])
      at α=0.50, injected into the layer-20 residual stream (ASSUMPTION
      A-bridge-space: cross-space by design, not a mechanism claim).
    - μ is the mean over all 300 support presentations (150 rel + 150 neu),
      layer 20, last token (protocol §3.2). v_hat^c_k = normalize(v_hat_k - μ);
      v_hat^c = normalize(sum_k v_hat^c_k). The renormalization amplification
      (1/||v_hat_k - μ||) is logged, not hidden (protocol §3.2).
    - The |cos(r, v_hat)| < 0.5 build assert is a deterministic function of
      pinned seed 7702 and the archived support data (reviewer's note): it is
      verified at bundle construction (CPU, pre-runtime) and re-asserted at
      execution. Seeds 7701/7702 are consumed via dedicated torch.Generators,
      so no intervening RNG use can desynchronize them (MAJOR-4 fix pattern).
    - Margin shifts are recorded but exploratory only (audit O5: the C7
      control invalidates margin-shift significance as a causal endpoint).
    - KL divergence per condition is exploratory (guardrail 0.50, EXP067
      precedent), never a branch trigger.
    - C7 (B_wrong) is a specificity diagnostic: reported, never a branch
      trigger (protocol §4).

Standing mechanical lessons applied (LOG-108/109/114/116):
    - No variable shadowing of module constants (D_ent, never D).
    - torch_dtype=torch.float32 pinned (script assumes float32 throughout).
    - get_output_embeddings() for version-agnostic unembedding access.
    - Device-consistent placement: cone/control vectors are CPU-built;
      run_with_intervention moves them via vec.to(device).
    - F2 single-token guard against the REAL tokenizer before any forward.

Governing standards:
    - AGENTS.md 14 Inviolable Laws (Law 6: Delta theta = 0; Law 7: zero
      leakage; Law 8: halts are reportable outcomes; Law 13: archiving)
    - STATISTICAL_PROTOCOL_V02.md
    - reports/adversarial_review_exp077_prereg_2026-09-23.md (SIGN)
"""

import os
import sys
import json
import math
import argparse
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats
from transformers import AutoModelForCausalLM, AutoTokenizer

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ----------------------------------------------------------------------------
# Configuration (protocol §2, §3.3, §3.4, §8, §10)
# ----------------------------------------------------------------------------
MODEL_NAME = "EleutherAI/pythia-410m"
D = 1024
N_LAYERS = 24
TARGET_LAYER = 20          # l* = 20 (83% depth, matching EXP066/067)

EXPECTED_SHA256 = "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd"
# Registered value from EXP067 §2; sanity check only. The BINDING guard is the
# runtime pre/post match.

SEED_TORCH = 20260923
SEED_NUMPY = 20260923
SEED_CONE_AXES = 7701      # cone orthogonal axes w_j (protocol §3.3, §10)
SEED_CONTROL = 7702        # control direction r + control axes (protocol §3.4, §10)
SEED_B_PERP = 9876         # inherited (B_wrong pipeline)

ALPHA_GRID = [0.25, 0.50, 1.00, 2.00]   # protocol §2 (radial sweep)
ALPHA_GEOM = 1.00          # cone/control/offset arms (protocol §2, §3.3)
ALPHA_BRIDGE = 0.50        # C8 positive control (EXP066's configuration that
                           # the §5 gate is calibrated against: alpha=0.5)

RHO_DEG = 30.0             # cone angular radius (protocol §3.3, A-cone-radius)
K_CONE = 8                 # cone/control directions (protocol §3.3)
CONTROL_COS_CAP = 0.5      # |cos(r, v_hat)| < 0.5 build assert (protocol §3.4)

N_SUPPORT_PAIRS = 30       # 5 x 30 support contrast pairs (§3.1)
N_BENCH = 60
HEADROOM_LO, HEADROOM_HI = 0.40, 0.70   # protocol §5
CONTINUITY_FLOOR = 0.50    # mean cos(v_hat_1, v_hat_k) >= 0.50 (protocol §5)
KL_GUARDRAIL = 0.50        # secondary guardrail, exploratory (EXP067 precedent)

# Historical baselines for the branch-(r) comparability rider (M3):
# research_log.md artifact spot-check (EXP065/066 Static_B_agg runs).
HISTORICAL_BASELINES = {"EXP065": 0.6833, "EXP066": 0.5667}

# Support vocabularies: the F2-corrected EXP078 set (all entities verified
# single-token under the pythia-410m tokenizer; conservative reading, see
# module docstring). Construction procedure identical to EXP066.
SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Joel", "Gideon", "Ruth", "Abel"],
    "V3_Greek": ["Ajax", "Jason", "Apollo", "Paris", "Atlas"],
    "V4_Roman": ["Marcus", "Julius", "Augustus", "Felix", "Diana"],
    "V5_Modern": ["Liam", "Noah", "Eli", "Maya", "Finn"],
}
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())

# Test-entity vocabularies (module level so the F2 guard checks them before
# any forward pass; benchmark builder references these constants).
NOVEL_VOCAB_PLANET = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
NOVEL_VOCAB_ELEMENT = ["Iron", "Gold", "Silver", "Bronze", "Steel"]

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

# ----------------------------------------------------------------------------
# Utilities (EXP066/067/070/078 harness)
# ----------------------------------------------------------------------------
def get_hash(model):
    """SHA-256 binding guard (protocol §2): SHA-256 over the concatenation of
    state_dict() tensors (sorted keys, CPU, float32 bytes)."""
    sha = hashlib.sha256()
    for key in sorted(model.state_dict().keys()):
        sha.update(model.state_dict()[key].detach().cpu().to(torch.float32).numpy().tobytes())
    return sha.hexdigest()


def compute_kl(p_base, p_mod):
    p_base = torch.clamp(p_base, min=1e-12)
    p_mod = torch.clamp(p_mod, min=1e-12)
    return float(torch.sum(p_base * (torch.log(p_base) - torch.log(p_mod))).item())


def compute_paired_stats(a_correct, b_correct):
    """Paired stats for the (A, B) decision pair lists.

    b = A wrong, B correct (B rescues over A); c = A correct, B wrong.
    delta_m = (b - c) / N  (B minus A, in fraction; x100 for pp).
    McNemar exact two-sided via binomtest. b=c=0 -> p=1.0 (M5.1).
    """
    b = 0
    c = 0
    for ac, bc in zip(a_correct, b_correct):
        if not ac and bc:
            b += 1
        elif ac and not bc:
            c += 1
    if b + c == 0:
        p_val = 1.0
    else:
        res = stats.binomtest(min(b, c), b + c, 0.5, alternative="two-sided")
        p_val = float(res.pvalue)
    delta_m = (b - c) / len(a_correct)
    return b, c, delta_m, p_val


def discordant_stats(K, M):
    """§3.6 discordant counts for the angular/control endpoints.

    (b, c) = (Σ K(1−M), Σ M(1−K)): b = K rescues where M does not;
    c = M rescues where K does not. For the angular endpoint K=cone/K_ind,
    M=line/L_ind (cone vs LINE); for the control endpoint K=cone/K_ind,
    M=control/R_ind (cone vs CONTROL). McNemar exact two-sided via
    binomtest; b=c=0 -> p=1.0 (M5.1). acc_base/acc_mod are the rescue
    rates of M and K (descriptive only). (MAJOR-2: these are the registered
    comparisons -- never cone-vs-baseline / control-vs-baseline.)
    """
    b = sum(1 for kk, mm in zip(K, M) if kk and not mm)
    c = sum(1 for kk, mm in zip(K, M) if mm and not kk)
    if b + c == 0:
        p_val = 1.0
    else:
        res = stats.binomtest(min(b, c), b + c, 0.5, alternative="two-sided")
        p_val = float(res.pvalue)
    n = len(K)
    return {"acc_base": float(np.mean(M)), "acc_mod": float(np.mean(K)),
            "delta_m": (b - c) / n, "b": b, "c": c, "p": p_val}


def holm_reject(p_values, alpha=0.05):
    """Holm step-down rejection set (strict p < alpha/(m-i+1)).

    Returns the set of indices rejected. Duplicated from evaluate_exp077.py
    for run-log display; the evaluator is authoritative for the ruling.
    """
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    rejected = set()
    for rank, i in enumerate(order):
        if p_values[i] < alpha / (m - rank):
            rejected.add(i)
        else:
            break
    return rejected


def log(msg, log_file=None):
    print(msg, flush=True)
    if log_file:
        log_file.write(msg + "\n")
        log_file.flush()


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

def main():
    parser = argparse.ArgumentParser(description="EXP077: cone-vs-line geometry (pre-registered)")
    parser.add_argument("--allow-cpu", action="store_true",
                        help="override the CUDA-required guard on CPU-only machines "
                             "(strongly discouraged: ~1,740 forward passes on CPU "
                             "takes many hours and may hit session limits)")
    args = parser.parse_args()

    out_dir = os.path.join("experiments", "runs", "EXP077_cone_vs_line")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp077_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    torch.manual_seed(SEED_TORCH)
    np.random.seed(SEED_NUMPY)
    try:
        torch.use_deterministic_algorithms(True)
        log("torch.use_deterministic_algorithms(True) enabled.", log_file)
    except Exception as e:
        log(f"WARNING: deterministic algorithms unavailable ({e}); continuing.", log_file)

    log("=" * 80, log_file)
    log("EXP077: Cone-vs-Line Geometry -- Is the Relational Concept Conical?", log_file)
    log("Pre-registered protocol: experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md", log_file)
    log(f"Model: {MODEL_NAME} | d={D} | target_layer={TARGET_LAYER} | "
        f"alpha_grid={ALPHA_GRID} | rho={RHO_DEG}deg K={K_CONE}", log_file)
    log("Protocol scope: IN-SCOPE (pythia-410m, layer 20) -- the ONLY registered config.", log_file)
    log("=" * 80, log_file)

    # CUDA FATAL (no silent CPU fallback; Law #8: a killed session is data).
    if not torch.cuda.is_available():
        if not args.allow_cpu:
            msg = ("FATAL: no CUDA GPU detected. EXP077 requires a GPU "
                   "(~1,740 forward passes; a CPU run takes many hours and will "
                   "likely hit session limits). Enable a GPU runtime -- Kaggle: "
                   "right panel -> Accelerator: GPU T4 x2 (new accounts need phone "
                   "verification first, see RUNBOOK step 0); Colab: Runtime -> "
                   "Change runtime type -> T4 GPU -- then re-run. Override ONLY "
                   "with --allow-cpu (strongly discouraged).")
            log(msg, log_file)
            log_file.close()
            raise SystemExit(msg)
        log("WARNING: --allow-cpu override accepted on a CPU-only machine. Expect "
            "many hours of runtime; a killed session mid-run is data per Law #8 -- "
            "keep the log.", log_file)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    log(f"Device: {device}", log_file)

    log(f"Loading model & tokenizer: {MODEL_NAME} ...", log_file)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    # LOG-109: pin float32 (mechanical, zero scientific change). m4 note:
    # transformers 5.x deprecates torch_dtype= (warning only; still functional).
    # Kept deliberately: dtype= would break older 4.x environments, and the
    # pinned kwarg is a standing program lesson.
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)
    model.eval()
    model.to(device)

    # ---- F2: single-token entity guard. The spec/EXP066 procedure assumes
    # single-token entities. Abort LOUDLY (not silent first-subtoken
    # truncation) if ANY support or test entity encodes to more than one
    # token. Runs immediately after tokenizer load, before any forward pass.
    _f2_entities = (
        [(e, " " + e) for _ents in SUPPORT_VOCABULARIES.values() for e in _ents] +
        [(e, " " + e) for e in NOVEL_VOCAB_PLANET + NOVEL_VOCAB_ELEMENT]
    )
    for _label, _s in _f2_entities:
        _ids = tokenizer.encode(_s)
        _single = (len(_ids) == 1)
        log(f"F2 tokenization: entity '{_label}' -> ids={_ids} "
            f"single_token={_single}", log_file)
        if not _single:
            _msg = (f"FATAL (F2 guard): entity '{_label}' encodes to "
                    f"{len(_ids)} tokens (ids={_ids}) -- the spec/EXP066 "
                    f"procedure assumes single-token entities. Multi-token "
                    f"entities are never silently truncated to the first "
                    f"subtoken. Re-design (or a new pre-registration) is "
                    f"required; aborting.")
            log(_msg, log_file)
            log_file.close()
            raise SystemExit(_msg)
    log(f"F2 guard PASSED: all {len(_f2_entities)} support/test entities are "
        f"single-token.", log_file)

    # ---- SHA-256 guard: PRE (protocol §2; binding guard = pre/post match;
    #      registered value is a sanity check only).
    pre_hash = get_hash(model)
    log(f"Pre-experiment parameter SHA-256: {pre_hash}", log_file)
    if pre_hash == EXPECTED_SHA256:
        log("Registered-hash sanity check: MATCH (EXP067 §2 value).", log_file)
    else:
        log("WARNING: registered-hash sanity check MISMATCH (expected EXP067 §2 "
            "value). Continuing -- the BINDING guard is the runtime pre/post "
            "match; this warning is recorded, not fatal.", log_file)

    layer_module = model.gpt_neox.layers[TARGET_LAYER]

    env_manifest = {
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": str(device),
        "model": MODEL_NAME,
        "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
        "expected_sha256_sanity": EXPECTED_SHA256,
        "sha256_sanity_match": bool(pre_hash == EXPECTED_SHA256),
    }
    log(f"Environment manifest: {json.dumps(env_manifest)}", log_file)

    def save_halt(outcome, reason, extra):
        payload = {
            "experiment": "EXP077",
            "model": MODEL_NAME,
            "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
            "outcome": outcome,
            "halt_reason": reason,
            "pre_hash": pre_hash,
            "post_hash": get_hash(model),
            "target_layer": TARGET_LAYER,
            "hidden_dim": D,
            "alpha_grid": ALPHA_GRID,
            "historical_baselines": HISTORICAL_BASELINES,
            "env_manifest": env_manifest,
        }
        payload.update(extra)
        with open(os.path.join(out_dir, "exp077_results.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        log("=" * 80, log_file)
        log(f"{outcome}: {reason}", log_file)
        log("THIS HALT IS THE REPORTABLE OUTCOME OF EXP077 (protocol §8, branch (d)).", log_file)
        log(f"Diagnostics written to {out_dir}/exp077_results.json", log_file)
        log("=" * 80, log_file)
        log_file.close()

    # -------------------------------------------------------------
    # 1. Support set: 5 vocabs x 30 contrast pairs (delta_h) + raw
    #    hidden states for mu (protocol §3.1, §3.2).
    # -------------------------------------------------------------
    log("\n[1] Support set: 5 vocabs x 30 contrast pairs ...", log_file)
    delta_h_by_vocab = {vk: [] for vk in VOCAB_KEYS}
    h_all = []          # all 300 support presentations (for mu)
    support_ids = []
    for vk, ents in SUPPORT_VOCABULARIES.items():
        for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
            A, B, C = ents[iA], ents[iB], ents[iC]
            q_opts = f"{A} or {C}" if (i % 2 == 0) else f"{C} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            with torch.no_grad():
                o_rel = model(input_ids=tokenizer.encode(p_rel, return_tensors="pt").to(device), output_hidden_states=True)
                o_neu = model(input_ids=tokenizer.encode(p_neu, return_tensors="pt").to(device), output_hidden_states=True)
            h_rel = o_rel.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
            h_neu = o_neu.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
            delta_h_by_vocab[vk].append(h_rel - h_neu)
            h_all.extend([h_rel, h_neu])
            support_ids.append(f"sup_{vk}_triple_{i}")
        for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
            A, B, C, D_ent = ents[iA], ents[iB], ents[iC], ents[iD]
            q_opts = f"{A} or {D_ent}" if (i % 2 == 0) else f"{D_ent} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
            with torch.no_grad():
                o_rel = model(input_ids=tokenizer.encode(p_rel, return_tensors="pt").to(device), output_hidden_states=True)
                o_neu = model(input_ids=tokenizer.encode(p_neu, return_tensors="pt").to(device), output_hidden_states=True)
            h_rel = o_rel.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
            h_neu = o_neu.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
            delta_h_by_vocab[vk].append(h_rel - h_neu)
            h_all.extend([h_rel, h_neu])
            support_ids.append(f"sup_{vk}_quad_{i}")
        delta_h_by_vocab[vk] = torch.stack(delta_h_by_vocab[vk])  # [30, d]
    log(f"Support contrast deltas: 5 x [30, {D}]; raw presentations: {len(h_all)}.", log_file)
    assert len(h_all) == 300, f"expected 300 support presentations, got {len(h_all)}"

    # ---- Candidate directions (protocol §3.1, §3.2) ----
    cand = build_candidate_directions(delta_h_by_vocab, h_all)
    v_hat = cand["v_hat"]
    v_hat_c = cand["v_hat_c"]
    log(f"v_hat (=B_agg) constructed (norm={float(torch.norm(v_hat)):.4f}).", log_file)
    log(f"Continuity assertion input: cos(v_hat_1, v_hat_k) = "
        f"{[f'{c:.4f}' for c in cand['cos_v1']]}; mean = {cand['mean_cos_v1']:.4f} "
        f"(floor {CONTINUITY_FLOOR}).", log_file)
    if not (cand["mean_cos_v1"] >= CONTINUITY_FLOOR):
        save_halt("HALT_CONTINUITY",
                  f"continuity floor failed (§5): mean cos(v_hat_1, v_hat_k) = "
                  f"{cand['mean_cos_v1']:.4f} < {CONTINUITY_FLOOR} -- the support "
                  f"archive did not reproduce the O1 phenomenon; we are not "
                  f"testing the direction the null was established on. "
                  f"Reportable per §8 branch (d); re-design required, not a "
                  f"re-run under EXP077.",
                  {"continuity": {"mean_cos_v1_vk": cand["mean_cos_v1"],
                                  "cos_v1": cand["cos_v1"],
                                  "floor": CONTINUITY_FLOOR, "passed": False}})
        print("CONTINUITY GATE HALTED — THIS IS THE RESULT. Download exp077_results.json and report it.")
        sys.exit(0)
    log("CONTINUITY ASSERTION PASSED.", log_file)
    log(f"mu constructed over {len(h_all)} presentations (norm={float(torch.norm(cand['mu'])):.4f}).", log_file)
    log(f"v_hat^c constructed (norm={float(torch.norm(v_hat_c)):.4f}); "
        f"renormalization ||v_hat_k - mu|| per k = "
        f"{[f'{a:.4f}' for a in cand['amplifications']]} (amplification logged, §3.2).", log_file)

    # B_perp (seed 9876) and B_wrong (Paris-capital contrast, as EXP066) for C7.
    torch.manual_seed(SEED_B_PERP)
    r_orth = torch.randn(D)
    r_orth -= v_hat * torch.dot(v_hat, r_orth)
    r_orth /= torch.norm(r_orth)
    B_wrong_basis = r_orth
    torch.manual_seed(SEED_TORCH)
    p_wrong_rel = "Fact: Paris is the capital of France. Question: What is the capital of France, Paris or London? Answer:"
    p_wrong_neu = "Fact: Paris is near London. Question: What is the capital of France, Paris or London? Answer:"
    with torch.no_grad():
        out_wr_rel = model(input_ids=tokenizer.encode(p_wrong_rel, return_tensors="pt").to(device), output_hidden_states=True)
        out_wr_neu = model(input_ids=tokenizer.encode(p_wrong_neu, return_tensors="pt").to(device), output_hidden_states=True)
    dH_wrong = out_wr_rel.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu() - out_wr_neu.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
    B_wrong = dH_wrong / (torch.norm(dH_wrong) + 1e-12)
    log("B_perp (seed 9876) and B_wrong (Paris-capital contrast, as EXP066) constructed.", log_file)
    log("BUDGET NOTE (m3): the runner spends 2 additional forwards building the B_wrong "
        "direction above the §9 table's 1,740 (actual worst case 1,742; 0.1% over the "
        "registered bound — immaterial to the free-tier quota conclusion; disclosed "
        "rather than rounded into the bound).", log_file)

    # -------------------------------------------------------------
    # 2. Cone + control construction (protocol §3.3, §3.4) -- CPU,
    #    pinned seeds via dedicated generators (no intervening RNG use).
    # -------------------------------------------------------------
    log("\n[2] Cone (K=8, rho=30deg, seed 7701) + control cone (seed 7702) ...", log_file)
    phi_list = [math.radians(RHO_DEG * (j + 1) / K_CONE) for j in range(K_CONE)]
    log(f"phi_j (deg): {[f'{math.degrees(p):.2f}' for p in phi_list]}", log_file)

    gen_cone = torch.Generator().manual_seed(SEED_CONE_AXES)
    u_list, w_list = [], []   # w_list persisted for Law #13 (m2)
    for j, phi in enumerate(phi_list):
        g = torch.randn(D, generator=gen_cone)
        g = g - torch.dot(g, v_hat) * v_hat          # Gram-Schmidt vs v_hat
        w = g / (torch.norm(g) + 1e-12)               # unit, orthogonal to v_hat
        assert abs(float(torch.dot(w, v_hat))) < 1e-5, f"w_{j} not orthogonal to v_hat"
        u = math.cos(phi) * v_hat + math.sin(phi) * w
        u = u / (torch.norm(u) + 1e-12)
        # EXACT check: cos(u_j, v_hat) == cos(phi_j) by construction (M5.1).
        _cos = float(torch.dot(u, v_hat).item())
        assert abs(_cos - math.cos(phi)) < 1e-5, f"cone direction {j}: cos={_cos}, expected {math.cos(phi)}"
        assert float(torch.norm(u).item()) > 0
        u_list.append(u)
        w_list.append(w)
    log(f"Cone arm: {K_CONE} unit directions; min_j phi_j = {math.degrees(phi_list[0]):.2f}deg > 0 "
        f"(no direction coincides with v_hat).", log_file)

    gen_ctrl = torch.Generator().manual_seed(SEED_CONTROL)
    r_raw = torch.randn(D, generator=gen_ctrl)
    r_vec = r_raw / (torch.norm(r_raw) + 1e-12)
    cos_r_vhat = float(torch.dot(r_vec, v_hat).item())
    log(f"Control axis r: |cos(r, v_hat)| = {abs(cos_r_vhat):.4f} (cap {CONTROL_COS_CAP}).", log_file)
    if not (abs(cos_r_vhat) < CONTROL_COS_CAP):
        _msg = (f"FATAL (control build assert, §3.4): |cos(r, v_hat)| = {abs(cos_r_vhat):.4f} "
                f">= {CONTROL_COS_CAP} -- the pinned random draw is near-parallel to v_hat, "
                f"making the control a second cone arm. This is a deterministic function "
                f"of seed {SEED_CONTROL}; re-design (new seed) requires a new pre-registration.")
        log(_msg, log_file)
        log_file.close()
        raise SystemExit(_msg)
    q_list = []
    for j, phi in enumerate(phi_list):
        g = torch.randn(D, generator=gen_ctrl)
        g = g - torch.dot(g, r_vec) * r_vec
        w = g / (torch.norm(g) + 1e-12)
        q = math.cos(phi) * r_vec + math.sin(phi) * w
        q = q / (torch.norm(q) + 1e-12)
        assert float(torch.norm(q).item()) > 0
        q_list.append(q)
    log(f"Control arm: {K_CONE} unit directions around r (same rho, K, phi grid).", log_file)

    # F1 injection-norm guard: every static injection vector must have norm > 0.
    injection_norms = {
        "v_hat_a025": float(torch.norm(0.25 * v_hat).item()),
        "v_hat_a050": float(torch.norm(0.50 * v_hat).item()),
        "v_hat_a100": float(torch.norm(1.00 * v_hat).item()),
        "v_hat_a200": float(torch.norm(2.00 * v_hat).item()),
        "v_hat_c_a100": float(torch.norm(1.00 * v_hat_c).item()),
        "B_wrong_a100": float(torch.norm(1.00 * B_wrong).item()),
    }
    for j in range(K_CONE):
        injection_norms[f"cone_u{j}_a100"] = float(torch.norm(ALPHA_GEOM * u_list[j]).item())
        injection_norms[f"ctrl_q{j}_a100"] = float(torch.norm(ALPHA_GEOM * q_list[j]).item())
    for _k, _n in injection_norms.items():
        assert _n > 0, f"FATAL (F1 guard): {_k} has zero norm -- silent no-op. Aborting."
    log(f"Injection-norm guard PASSED ({len(injection_norms)} vectors, all > 0).", log_file)

    # -------------------------------------------------------------
    # 3. Benchmark N=60 + anti-cheat assert (protocol §3.5/§5).
    #    The identical N=60 Planetary/Elemental 2-hop/3-hop suite from EXP065
    #    (same items, same premise permutations) — ported VERBATIM from
    #    experiments/runs/exp078/run_exp078.py §2 (MAJOR-3 repair; Law #9: no
    #    new benchmark construction). Item dicts keep this runner's schema
    #    ("prompt"/"A"/"C" with A=target, C=foil) plus provenance fields.
    # -------------------------------------------------------------
    log("\n[3] Benchmark: N=60 Planetary/Elemental 2-hop/3-hop (EXP065/066-identical, ported from EXP078) ...", log_file)
    bench = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 8:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        bench.append({"id": f"exp077_planet_2hop_{i}", "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "planet", "hop": 2, "domain": "Planetary"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                          NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 8:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_planet_3hop_{i}", "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "planet", "hop": 3, "domain": "Planetary"})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 7:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        bench.append({"id": f"exp077_element_2hop_{i}", "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "element", "hop": 2, "domain": "Elemental"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                          NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 7:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_element_3hop_{i}", "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "element", "hop": 3, "domain": "Elemental"})
    assert len(bench) == N_BENCH, f"Expected {N_BENCH} benchmark items, got {len(bench)}"
    log(f"Benchmark: {len(bench)} items (EXP065/066-identical construction).", log_file)

    # ---- Anti-cheat assert (§3.5): no benchmark prompt may equal a support
    #      prompt. We keep the support prompt strings here to run the check.
    _support_prompts = set()
    for vk, ents in SUPPORT_VOCABULARIES.items():
        for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
            A, B, C = ents[iA], ents[iB], ents[iC]
            q_opts = f"{A} or {C}" if (i % 2 == 0) else f"{C} or {A}"
            _support_prompts.add(f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:")
            _support_prompts.add(f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:")
        for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
            A, B, C, D_ent = ents[iA], ents[iB], ents[iC], ents[iD]
            q_opts = f"{A} or {D_ent}" if (i % 2 == 0) else f"{D_ent} or {A}"
            _support_prompts.add(f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:")
            _support_prompts.add(f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:")
    _leak = [it["prompt"] for it in bench if it["prompt"] in _support_prompts]
    if _leak:
        save_halt("HALT_ANTICHEAT",
                  f"anti-cheat assert failed (§3.5): {_leak.__len__()} benchmark "
                  f"prompt(s) identical to a support prompt -- zero-leakage "
                  f"violation. Reportable per §8 branch (d).",
                  {"n_leaked": len(_leak)})
        print("ANTI-CHEAT ASSERT HALTED — THIS IS THE RESULT. Download exp077_results.json and report it.")
        sys.exit(0)
    log("Anti-cheat assert PASSED: no benchmark prompt coincides with a support prompt.", log_file)

    # -------------------------------------------------------------
    # 4. Evaluation harness (protocol §4).
    # -------------------------------------------------------------
    def eval_item(prompt, A, C, injection=None):
        """One item: argmax between 'A' and 'C' completions (protocol §4).
        injection = static vector (CPU tensor) added to the layer-20 residual
        stream of the last token, scaled already; None = baseline."""
        ids_A = tokenizer.encode(" " + A)
        ids_C = tokenizer.encode(" " + C)
        toks_A, toks_C = ids_A[0], ids_C[0]
        inp = tokenizer.encode(prompt, return_tensors="pt").to(device)
        if injection is None:
            with torch.no_grad():
                out = model(input_ids=inp)
            logits = out.logits[0, -1, :]
            chosen = A if logits[toks_A] > logits[toks_C] else C
            return chosen, logits.detach().cpu()
        vec = injection.to(device)
        hook_holder = {}
        def hook_fn(module, inputs, output):
            x = output[0] if isinstance(output, tuple) else output
            x = x.clone()
            x[:, -1, :] = x[:, -1, :] + vec
            hook_holder["hook"] = hook
            return (x,) + tuple(output[1:]) if isinstance(output, tuple) else x
        hook = layer_module.register_forward_hook(hook_fn)
        try:
            with torch.no_grad():
                out = model(input_ids=inp)
        finally:
            hook.remove()
        logits = out.logits[0, -1, :].detach().cpu()
        chosen = A if logits[toks_A] > logits[toks_C] else C
        return chosen, logits

    def run_arm(name, items, get_injection, log_file):
        """Run a condition arm over the benchmark (protocol §4, §9)."""
        log(f"\n[{name}] ...", log_file)
        correct, logits_list, records = [], [], []
        for i, it in enumerate(items):
            vec = get_injection(it, i)
            chosen, logits = eval_item(it["prompt"], it["A"], it["C"], injection=vec)
            correct.append(bool(chosen == it["A"]))
            logits_list.append(logits)
            records.append({"item": i, "chosen": chosen, "correct_A": it["A"], "correct": bool(chosen == it["A"])})
        return correct, logits_list, records

    def compute_accuracy(correct):
        return float(np.mean(correct))

    # C8: same-layer output bridge (positive control, EXP066 `make_bridge_vec`).
    # v_output(x) = normalize(E[target] - E[foil]) -- an UNEMBEDDING-space
    # direction applied to the layer-20 residual stream (cross-space by design;
    # protocol §4 C8 row and ASSUMPTION A-bridge-space). alpha=0.50 matches
    # EXP066's configuration (alpha=0.5, +13.33pp, p=0.0078) that the §5
    # bridge-validity gate is calibrated against. get_output_embeddings() is
    # the Transformers-5.x-safe accessor for the same matrix EXP066 called
    # model.embed_out.weight.
    _E = model.get_output_embeddings().weight.detach().cpu()
    def make_bridge_vec(item, i):
        tt = tokenizer.encode(" " + item["A"])[0]   # target = correct answer
        ft = tokenizer.encode(" " + item["C"])[0]   # foil
        w = _E[tt, :] - _E[ft, :]
        return ALPHA_BRIDGE * (w / (torch.norm(w) + 1e-12))

    # F1 guard extension: C8 bridge vectors (per-item unembedding directions).
    _c8_norms = []
    for _i, _it in enumerate(bench):
        _bv = make_bridge_vec(_it, _i)
        _n = float(torch.norm(_bv).item())
        assert _n > 0, f"FATAL (F1 guard): C8 bridge vector has zero norm on item {_i}."
        _c8_norms.append(_n)
        injection_norms[f"C8_bridge_item{_i}"] = _n
    log(f"C8 bridge vectors: 60 per-item unembedding directions, "
        f"min norm={min(_c8_norms):.4f} (all > 0).", log_file)

    base_correct, base_logits, base_records = run_arm("C1_Unintervened_Baseline", bench, lambda it, i: None, log_file)
    base_acc = compute_accuracy(base_correct)
    log(f"C1 baseline accuracy: {base_acc:.4f} ({sum(base_correct)}/{N_BENCH})", log_file)
    log(f"Historical baselines (branch-(r) comparability rider, M3): "
        f"{json.dumps(HISTORICAL_BASELINES)}", log_file)

    # -------------------------------------------------------------
    # 5. Gate 1: headroom (§5). Baseline outside [40%, 70%] -> branch (d).
    # -------------------------------------------------------------
    if not (HEADROOM_LO <= base_acc <= HEADROOM_HI):
        save_halt("HALT_HEADROOM",
                  f"headroom gate failed (§5): baseline accuracy {base_acc:.4f} "
                  f"outside [{HEADROOM_LO}, {HEADROOM_HI}]. Floor/ceiling effects "
                  f"would invalidate the paired comparison. Reportable per §8 "
                  f"branch (d); re-design required, not a re-run under EXP077.",
                  {"baseline_accuracy": base_acc,
                   "headroom_band": [HEADROOM_LO, HEADROOM_HI],
                   "historical_baselines": HISTORICAL_BASELINES})
        print("HEADROOM GATE HALTED — THIS IS THE RESULT. Download exp077_results.json and report it.")
        sys.exit(0)
    log("HEADROOM GATE PASSED.", log_file)

    # -------------------------------------------------------------
    # 6. Gate 2: bridge validity (§5). C8 = output bridge (per-item, V1),
    #    positive control; must have delta_m > 0 AND p < 0.05 vs C1.
    # -------------------------------------------------------------
    c8_correct, c8_logits, c8_records = run_arm("C8_Output_Bridge", bench, make_bridge_vec, log_file)
    c8_acc = compute_accuracy(c8_correct)
    b8, c8b, dm8, p8 = compute_paired_stats(base_correct, c8_correct)
    log(f"C8 output bridge: accuracy {c8_acc:.4f} ({sum(c8_correct)}/{N_BENCH}), "
        f"delta_m={dm8*100:+.2f}pp (b={b8}, c={c8b}), p={p8:.6f}", log_file)
    bridge_gate_pass = bool(dm8 > 0 and p8 < 0.05)
    if not bridge_gate_pass:
        save_halt("HALT_BRIDGE",
                  f"bridge gate failed (§5): output-bridge positive control did "
                  f"not show delta_m > 0 AND p < 0.05 vs baseline "
                  f"(delta_m={dm8*100:+.2f}pp, b={b8}, c={c8b}, p={p8:.6f}). "
                  f"Causal non-transfer may reflect the apparatus, not the "
                  f"geometry. Reportable per §8 branch (d); re-design required, "
                  f"not a re-run under EXP077.",
                  {"baseline_accuracy": base_acc,
                   "bridge": {"acc_base": base_acc, "acc_mod": c8_acc,
                              "delta_m": dm8, "b": b8, "c": c8b, "p": p8,
                              "passed": False}})
        print("BRIDGE GATE HALTED — THIS IS THE RESULT. Download exp077_results.json and report it.")
        sys.exit(0)
    log("BRIDGE GATE PASSED: positive control rescues.", log_file)

    # -------------------------------------------------------------
    # 7. Full launch: C2-C7 (§4), C9, C10 (protocol §9). C7 = B_wrong at
    #    alpha=1.0 (reported only, never a branch trigger).
    # -------------------------------------------------------------
    # Margin tokens (first subtoken of " A"/" C") for the registered
    # Wilcoxon-on-margins indicator (protocol §4; exploratory-only per audit
    # O5). Margins are computed inline per arm; no logits are retained beyond
    # what each arm already holds.
    _toks = [(tokenizer.encode(" " + it["A"])[0], tokenizer.encode(" " + it["C"])[0]) for it in bench]
    _m_base = [float((l[tA] - l[tC]).item()) for l, (tA, tC) in zip(base_logits, _toks)]

    radial_stats = {}
    arm_correct = {"C1": base_correct}
    for alpha in ALPHA_GRID:
        name = f"C_alpha_{alpha:g}"
        corr, lgs, recs = run_arm(name, bench, lambda it, i, a=alpha: a * v_hat, log_file)
        b, c, dm, p = compute_paired_stats(base_correct, corr)
        acc = compute_accuracy(corr)
        kl = float(np.mean([compute_kl(torch.softmax(bl, dim=0), torch.softmax(l, dim=0))
                            for bl, l in zip(base_logits, lgs)]))
        _m_mod = [float((l[tA] - l[tC]).item()) for l, (tA, tC) in zip(lgs, _toks)]
        _deltas = np.array(_m_mod) - np.array(_m_base)
        try:
            _wp = float(stats.wilcoxon(_deltas, alternative="two-sided").pvalue)
        except Exception:
            _wp = 1.0
        radial_stats[alpha] = {"acc_base": base_acc, "acc_mod": acc,
                               "delta_m": dm, "b": b, "c": c, "p": p,
                               "delta_margin": float(np.mean(_deltas)),
                               "wilcoxon_p": _wp,
                               "kl_div": kl,
                               "kl_guardrail_exceeded": bool(kl > KL_GUARDRAIL)}
        arm_correct[name] = corr
        log(f"{name}: acc={acc:.4f}, delta_m={dm*100:+.2f}pp (b={b}, c={c}), "
            f"p={p:.6f}, KL={kl:.4f}{' KL-EXCEEDED' if kl > KL_GUARDRAIL else ''}", log_file)

    off_correct, off_logits, off_records = run_arm("C6_OffsetRemoved", bench, lambda it, i: ALPHA_GEOM * v_hat_c, log_file)
    b_off, c_off, dm_off, p_off = compute_paired_stats(base_correct, off_correct)
    kl_off = float(np.mean([compute_kl(torch.softmax(bl, dim=0), torch.softmax(l, dim=0))
                            for bl, l in zip(base_logits, off_logits)]))
    log(f"C6 offset-removed (alpha=1.0): acc={compute_accuracy(off_correct):.4f}, "
        f"delta_m={dm_off*100:+.2f}pp (b={b_off}, c={c_off}), p={p_off:.6f}, KL={kl_off:.4f}", log_file)

    c7_correct, c7_logits, c7_records = run_arm("C7_B_wrong", bench, lambda it, i: ALPHA_GEOM * B_wrong, log_file)
    b_w, c_w, dm_w, p_w = compute_paired_stats(base_correct, c7_correct)
    log(f"C7 B_wrong (alpha=1.0, reported only): acc={compute_accuracy(c7_correct):.4f}, "
        f"delta_m={dm_w*100:+.2f}pp (b={b_w}, c={c_w}), p={p_w:.6f}", log_file)

    # -------------------------------------------------------------
    # 8. C9/C10 best-of-8 arms (protocol §3.3, §3.4, §4): per item, 8
    #    forwards with unit directions u_j (cone) / q_j (control) at
    #    alpha=1.0; per-item score = max_j correct. Worst case 960.
    # -------------------------------------------------------------
    def run_bestof8(name, directions, log_file):
        """directions: list of 8 unit CPU tensors (u_j or q_j)."""
        log(f"\n[{name}] best-of-8 x {len(bench)} items ...", log_file)
        item_ok, win_records = [], []
        for i, it in enumerate(bench):
            wins = 0
            for j, d in enumerate(directions):
                chosen, _ = eval_item(it["prompt"], it["A"], it["C"], injection=ALPHA_GEOM * d)
                if chosen == it["A"]:
                    wins += 1
                    break                     # first rescue suffices for the max
            item_ok.append(wins > 0)
            win_records.append({"item": i, "rescued": wins > 0})
            if (i + 1) % 15 == 0:
                log(f"  {name}: {i + 1}/{len(bench)} items", log_file)
        return item_ok, win_records

    cone_correct, cone_records = run_bestof8("C9_Cone", u_list, log_file)
    ctrl_correct, ctrl_records = run_bestof8("C10_Control", q_list, log_file)

    def paired_stats(a, b):
        bb, cc, dm, p = compute_paired_stats(a, b)
        return {"acc_base": float(np.mean(a)), "acc_mod": float(np.mean(b)),
                "delta_m": dm, "b": bb, "c": cc, "p": p}

    # ---- Rescue indicator lists (§3.6): L=line/C4, K=cone/C9, R=control/C10,
    #      O=offset/C6. Computed here because the angular/control ENDPOINTS
    #      are the §3.6 discordant counts (MAJOR-2 repair) — not
    #      cone-vs-baseline / control-vs-baseline.
    L_ind = [int((not a) and m) for a, m in zip(base_correct, arm_correct["C_alpha_1"])]
    K_ind = [int((not a) and m) for a, m in zip(base_correct, cone_correct)]
    R_ind = [int((not a) and m) for a, m in zip(base_correct, ctrl_correct)]
    O_ind = [int((not a) and m) for a, m in zip(base_correct, off_correct)]

    angular = discordant_stats(K_ind, L_ind)   # §3.6: cone vs LINE
    control = discordant_stats(K_ind, R_ind)  # §3.6: cone vs CONTROL
    log(f"\nAngular endpoint (cone vs line, §3.6): delta_m={angular['delta_m']*100:+.2f}pp "
        f"(b={angular['b']}, c={angular['c']}), p={angular['p']:.6f}", log_file)
    log(f"Control endpoint (cone vs control, §3.6): delta_m={control['delta_m']*100:+.2f}pp "
        f"(b={control['b']}, c={control['c']}), p={control['p']:.6f}", log_file)

    # ---- Rescue / margin / KL indicators (§4). MARGIN shifts are
    #      recorded but EXPLORATORY only (audit O5: the C7 negative control
    #      invalidates margin-shift significance as a causal endpoint).
    # ---- Wilcoxon signed-rank on margins: valid as an exploratory shift
    #      descriptor only if the C7 endpoint p-value does not invalidate it
    #      (protocol §4, boundary decision rule).
    def margin_shift(a_logits, b_logits, toks_A_C):
        """Per-item margins (logit[tA] - logit[tC]) under logits a and b."""
        m_a = [float((l[tA] - l[tC]).item()) for l, (tA, tC) in zip(a_logits, toks_A_C)]
        m_b = [float((l[tA] - l[tC]).item()) for l, (tA, tC) in zip(b_logits, toks_A_C)]
        return m_a, m_b

    # (_toks and _m_base were computed before the radial loop; reused here.)

    def arm_indicators(corr_logits, base_logits, name):
        m_base, m_mod = margin_shift(base_logits, corr_logits, _toks)
        deltas = np.array(m_mod) - np.array(m_base)
        try:
            wp = float(stats.wilcoxon(deltas, alternative="two-sided").pvalue) if len(deltas) else 1.0
        except Exception:
            wp = 1.0
        kl = float(np.mean([compute_kl(torch.softmax(bl, dim=0), torch.softmax(l, dim=0))
                            for bl, l in zip(base_logits, corr_logits)]))
        return {"delta_margin": float(np.mean(deltas)), "wilcoxon_p": wp, "kl_div": kl,
                "kl_guardrail_exceeded": bool(kl > KL_GUARDRAIL)}

    # Margins/Wilcoxon are computed only for arms with stored logits (C6, C7,
    # C8). C9/C10 (best-of-8) logits were not retained -- their indicator
    # endpoints are correctness-based (K/R lists), and no margin is fabricated
    # for them (AGENTS.md Law #2).
    cond_stats = {}
    for alpha, st in radial_stats.items():
        cond_stats[f"C_alpha_{alpha:g}"] = {**st}
    cond_stats["C1"] = {"acc_base": base_acc, "acc_mod": base_acc, "delta_m": 0.0,
                        "b": 0, "c": 0, "p": 1.0}
    cond_stats["C6_offset"] = {"acc_base": base_acc,
                               "acc_mod": float(np.mean(off_correct)),
                               "delta_m": dm_off, "b": b_off, "c": c_off,
                               "p": p_off, **arm_indicators(off_logits, base_logits, "C6")}
    cond_stats["C7_Bwrong"] = {"acc_base": base_acc,
                              "acc_mod": float(np.mean(c7_correct)),
                              "delta_m": dm_w, "b": b_w, "c": c_w, "p": p_w,
                              "reported_only": True,
                              **arm_indicators(c7_logits, base_logits, "C7")}
    cond_stats["C8_bridge"] = {"acc_base": base_acc, "acc_mod": c8_acc,
                               "delta_m": dm8, "b": b8, "c": c8b, "p": p8,
                               "positive_control": True,
                               **arm_indicators(c8_logits, base_logits, "C8")}

    # Rescue indicator lists (§4): per instance, A_alpha/C2-C5 (L/C4, K/C9,
    # R/C10, O/C6 were computed earlier at §3.6 for the endpoints).
    A_inds = {f"A_alpha_{alpha:g}": [int((not a) and m)
                                    for a, m in zip(base_correct, arm_correct[f"C_alpha_{alpha:g}"])]
              for alpha in ALPHA_GRID}

    # C3 (alpha=0.50) vs C1 replication pair -- feeds branch (r).
    rep = paired_stats(base_correct, arm_correct["C_alpha_0.5"])
    log(f"\nReplication endpoint C3 vs C1 (alpha=0.50): "
        f"delta_m={rep['delta_m']*100:+.2f}pp (b={rep['b']}, c={rep['c']}), p={rep['p']:.6f}", log_file)

    # ---- Holm display for the radial family (runner display only;
    #      the evaluator is authoritative).
    p_list = [radial_stats[a]["p"] for a in ALPHA_GRID]
    dm_list = [radial_stats[a]["delta_m"] for a in ALPHA_GRID]
    holm_set = holm_reject(p_list)
    S_H_disp = sorted([ALPHA_GRID[i] for i in holm_set if dm_list[i] > 0])
    log(f"Radial Holm display: p=[{[f'{p:.4f}' for p in p_list]}], "
        f"rejected idx={sorted(holm_set)}, S_H={S_H_disp}", log_file)

    # -------------------------------------------------------------
    # 9. Instance records + Law-13 archive (protocol §11; LOG-070
    #    pattern: raw instance records + direction vectors + support ids).
    # -------------------------------------------------------------
    instance_records = []
    for i, it in enumerate(bench):
        instance_records.append({
            "item": i, "ent": it["ent"], "typ": it["typ"],
            "correct": {
                "C1": bool(base_correct[i]),
                "C2_a025": bool(arm_correct["C_alpha_0.25"][i]),
                "C3_a050": bool(arm_correct["C_alpha_0.5"][i]),
                "C4_a100": bool(arm_correct["C_alpha_1"][i]),
                "C5_a200": bool(arm_correct["C_alpha_2"][i]),
                "C6_offset": bool(off_correct[i]),
                "C7_Bwrong": bool(c7_correct[i]),
                "C8_bridge": bool(c8_correct[i]),
                "C9_cone": bool(cone_correct[i]),
                "C10_control": bool(ctrl_correct[i]),
            },
            "rescue_indicators": {
                "L_C4": L_ind[i], "K_C9": K_ind[i], "R_C10": R_ind[i],
                "O_C6": O_ind[i],
                **{k: v[i] for k, v in A_inds.items()},
            },
        })

    post_hash = get_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}", log_file)
    if pre_hash != post_hash:
        _msg = (f"CRITICAL FATAL: pre/post parameter hash mismatch -- "
                f"frozen-backbone violation (AGENTS.md Law #6). pre={pre_hash} "
                f"post={post_hash}. Aborting; results are NOT reported.")
        log(_msg, log_file)
        log_file.close()
        raise SystemExit(_msg)
    log("Frozen-backbone guard PASSED: pre/post parameter hashes match.", log_file)

    # Archive (torch, in float32, CPU).
    archive = {
        "v_hat": v_hat, "v_hat_c": v_hat_c, "mu": cand["mu"],
        "v_hats": cand["v_hats"], "v_hat_c_ks": cand["v_hat_c_ks"],
        "u_list": torch.stack(u_list), "w_list": torch.stack(w_list),  # m2: w_j explicit (Law #13)
        "q_list": torch.stack(q_list),
        "r_vec": r_vec, "B_wrong": B_wrong, "B_perp_basis": B_wrong_basis,
        "pre_hash": pre_hash, "post_hash": post_hash,
    }
    torch.save(archive, os.path.join(out_dir, "exp077_vectors.pt"))
    log(f"Archive written: exp077_vectors.pt "
        f"({os.path.getsize(os.path.join(out_dir, 'exp077_vectors.pt'))} B)", log_file)
    with open(os.path.join(out_dir, "exp077_instance_records.json"), "w", encoding="utf-8") as f:
        json.dump(instance_records, f, indent=2)

    results_payload = {
        "experiment": "EXP077",
        "model": MODEL_NAME,
        "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
        "outcome": "COMPLETED",
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "expected_sha256_sanity": EXPECTED_SHA256,
        "sha256_sanity_match": bool(pre_hash == EXPECTED_SHA256),
        "target_layer": TARGET_LAYER,
        "hidden_dim": D,
        "seeds": {"torch": SEED_TORCH, "numpy": SEED_NUMPY,
                  "cone_axes": SEED_CONE_AXES, "control": SEED_CONTROL,
                  "B_perp": SEED_B_PERP},
        "alpha_grid": ALPHA_GRID,
        "cone": {"rho_deg": RHO_DEG, "K": K_CONE,
                 "phi_deg": [float(math.degrees(p)) for p in phi_list],
                 "cos_r_vhat": cos_r_vhat,
                 "control_cos_cap": CONTROL_COS_CAP},
        "continuity": {"mean_cos_v1_vk": cand["mean_cos_v1"],
                       "cos_v1": cand["cos_v1"],
                       "floor": CONTINUITY_FLOOR, "passed": True},
        "baseline_accuracy": base_acc,
        "historical_baselines": HISTORICAL_BASELINES,
        "bridge_gate": {"delta_m": dm8, "b": b8, "c": c8b, "p": p8, "passed": True},
        "stage_B_conditions": cond_stats,
        "angular": angular,
        "control": control,
        "offset": {"acc_base": base_acc, "acc_mod": float(np.mean(off_correct)),
                   "delta_m": dm_off, "b": b_off, "c": c_off, "p": p_off},
        "replication": rep,
        "radial": {"alphas": ALPHA_GRID, "p_values": p_list,
                   "delta_ms": dm_list,
                   "holm_rejected_display": sorted(holm_set),
                   "S_H_display": S_H_disp,
                   "note": "Runner display only; the evaluator (evaluate_exp077.py) "
                           "is authoritative for S_H and the ruling."},
        "offset_amplifications": cand["amplifications"],
        "injection_vector_norms": injection_norms,
        "env_manifest": env_manifest,
        "rescue_indicator_counts": {
            "L_C4": int(sum(L_ind)), "K_C9": int(sum(K_ind)),
            "R_C10": int(sum(R_ind)), "O_C6": int(sum(O_ind)),
            **{k: int(sum(v)) for k, v in A_inds.items()},
        },
        "instance_count": N_BENCH,
        "support_ids_count": len(support_ids),
        "kl_guardrail": KL_GUARDRAIL,
        "interpretation_notes": [
            "Margin shifts and Wilcoxon p-values are recorded but EXPLORATORY only; "
            "they cannot license causal claims (audit O5; protocol §4).",
            "C7 (B_wrong) is a specificity diagnostic: reported only, never a branch trigger.",
            "The (c) branch kills ONLY the tested rho=30deg unconditional cone and "
            "the alpha=1.0 offset hypotheses (spec §11 residual P5); gated/concept-projection variants survive.",
        ],
    }
    with open(os.path.join(out_dir, "exp077_results.json"), "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)
    log(f"Results written: exp077_results.json "
        f"({os.path.getsize(os.path.join(out_dir, 'exp077_results.json'))} B)", log_file)

    log("\n" + "=" * 80, log_file)
    log("EXP077 COMPLETED. Next: run evaluate_exp077.py on exp077_results.json "
        "for the pre-registered ruling (branch (d)/(r)/(a)/(b)/(c)).", log_file)
    log("=" * 80, log_file)
    log_file.close()


if __name__ == "__main__":
    main()
