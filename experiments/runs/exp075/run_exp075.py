"""
EXP075: Subspace-Restricted Bridge -- Is the Subspace Right and the Direction Wrong?
Pre-registered confirmatory protocol:
    experiments/protocols/EXP075_SUBSPACE_BRIDGE_PREREG_SPEC.md

Core scientific question (protocol §1):
    Does the per-vocabulary contrast subspace S = span{v1..v5} contain a
    causally efficacious direction -- i.e., was the EXP065/066 null a
    *direction-choice* failure inside S, rather than a subspace failure?

Mechanism (protocol §3):
    S from the 5 per-vocabulary residual-stream contrast directions (EXP066
    support procedure, 5 x 30 support contrast pairs), thin-QR -> Q_S.
    bridge(x) = normalize(E[target] - E[foil]) (EXP066-identical).
    C4: h <- h + alpha * normalize(P_S bridge(x))     (the test)
    C5: h <- h + alpha * normalize(P_S^perp bridge(x)) (the discriminant)
    C3: full bridge (positive control); C2: B_agg (static basis, expected null).

This is BOUNDARY science, not novelty science (protocol §1.1): the N1 verdict
stands regardless of outcome. Branch (e) licenses only a label-informed,
per-item existential direction inside S (review M1/M2); mechanism
(relational vs logit-steering) is unidentified by this experiment; the energy
gate guards null-interpretability only (protocol §3.4, review m2).

Pipeline (protocol order of operations):
    (1) support set + v_hat_k + S construction + rank guard (§3.1)
    (2) benchmark N=60 (EXP065/066-identical construction) (§5)
    (3) bridges + projections + energy gate (§3.2-§3.4)   [precedence (a)]
    (4) C1 baseline + headroom gate (§5)                  [precedence (b)]
    (5) conditions C1..C7 + endpoints (§4, §6)
Output directory: experiments/runs/EXP075_subspace_bridge/

Conservative readings of protocol ambiguities (all logged here, not improvised):
    - Branch (f) is terminal (protocol §7.0 canonical criterion, "single
      source of truth"): the exact-kill cell (C4 b=c=0, C3 valid, C2 null)
      rules H_sub FALSIFIED. (h)/(i) are supplementary localization NOTES in
      the evaluator's report() for the (f) region, not branch replacements.
      For the (g) conditional sub-case the partition stands: C5 significant
      positive -> (h) ("upgrades it toward (f)"); otherwise -> (i)
      ("neither (e) nor (f) fires" -- literally true there). The exact (b,c)
      cells are reported regardless.
    - Zero-norm projection hygiene: a zero ||P_S bridge(x)|| (or S^perp) would
      make normalize() undefined. The spec is silent; aborting loudly (FATAL)
      is the non-silent option (EXP067 F1 lesson: impossible, not just absent).
      This is a measure-zero hygiene event, not a branch.
    - Rank-guard halt (§3.1) is not lettered in §7.1's tree (it fires before any
      condition runs). Reported as branch (a') with the §3.1/§7.2 halt text;
      it is NOT the energy-gate branch (a).
    - Energy gate is evaluated on the full N=60 benchmark before the headroom
      gate, per the (a)->(b) precedence.
    - (e) + C5-also-rescues: branch stays (e) ((h) is conditional on (f)/(g)
      only); the C5 rescue is reported as an informational note, no branch change.
    - u_S and u_S^perp are both unit-norm at alpha=0.50 like every condition
      (§3.3: renormalization is load-bearing; the test is about direction, not
      energy).
    - Historical baselines for the (d) comparability rider: EXP065 68.33%,
      EXP066 56.67% (research_log.md artifact spot-check; the numbers live in
      the results artifact, not only in the evaluator).
    - No-peeking discipline (m1): S is constructed strictly BEFORE the
      benchmark exists, and build_subspace_S() receives ONLY the support
      contrast deltas (signature-enforced; it cannot reference test items,
      which do not exist yet at call time). The runner is self-contained (no
      support artifact files), so the whitelist is realized as ordering +
      signature discipline, not file-path filtering -- documented in
      UNTESTED_ASSUMPTIONS.md.

Governing standards:
    - AGENTS.md 14 Inviolable Laws (Law 6: Delta theta = 0; Law 7: zero
      leakage; Law 8: halts are reportable outcomes; Law 13: archiving)
    - STATISTICAL_PROTOCOL_V02.md
    - reports/adversarial_review_exp075_prereg_2026-09-23.md (SIGNED)

Mechanically adapted from experiments/runs/exp070/run_exp070.py (harness:
SHA-256 guard, hook lifecycle, eval_test_condition, F1 injection-norm guards,
CUDA FATAL, halt payloads).
"""

import os
import sys
import json
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
# Configuration (protocol §2, §3.1, §8)
# ----------------------------------------------------------------------------
MODEL_NAME = "EleutherAI/pythia-410m"
D = 1024
N_LAYERS = 24
TARGET_LAYER = 20          # l* = 20 (83% depth, matching EXP066/EXP067)
ALPHA = 0.50               # fixed for all conditions (protocol §2)

EXPECTED_SHA256 = "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd"
# Registered value from EXP067 §2; sanity check only. The BINDING guard is the
# runtime pre/post match (EXP067 §2, E-4).

SEED_TORCH = 20260923
SEED_NUMPY = 20260923
SEED_B_PERP = 9876         # inherited

N_SUPPORT_PAIRS = 30       # 5 x 30 support contrast pairs (§3.1)
N_BENCH = 60
HEADROOM_LO, HEADROOM_HI = 0.40, 0.70   # protocol §5
RANK_GUARD_RATIO = 1e-6                # sigma_min/sigma_max > 1e-6 (§3.1)
ENERGY_BAR = 0.10          # [ARBITRARY, anchored at chance E[e]~0.07] (§3.4)
ENERGY_SENSITIVITY = [0.05, 0.10, 0.15]
KL_GUARDRAIL = 0.50        # secondary guardrail, exploratory (EXP067 precedent)

# Historical baselines for the branch-(d) comparability rider (M3):
# research_log.md artifact spot-check (EXP065/066 Static_B_agg runs).
HISTORICAL_BASELINES = {"EXP065": 0.6833, "EXP066": 0.5667}

SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Caleb", "Gideon", "Miriam", "Reuben"],
    "V3_Greek": ["Hector", "Jason", "Nestor", "Paris", "Priam"],
    "V4_Roman": ["Marcus", "Lucius", "Titus", "Felix", "Silas"],
    "V5_Modern": ["Liam", "Noah", "Sora", "Maya", "Leila"],
}
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())

# Test-entity vocabularies: hoisted to module level (were local to main()) so
# the F2 single-token guard can check test entities before any forward pass
# runs. The benchmark builder below references these module constants.
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
# Utilities (identical to EXP066/067/070 harness)
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
    McNemar exact two-sided via binomtest.
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


def log(msg, log_file=None):
    print(msg, flush=True)
    if log_file:
        log_file.write(msg + "\n")
        log_file.flush()


def build_subspace_S(delta_h_by_vocab):
    """Construct S = span{v_hat_1..v_hat_5} and its thin-QR basis.

    No-peeking discipline (mechanical, protocol §3.1 m1): this function
    receives ONLY the support contrast deltas. It has no access to benchmark
    items, labels, or outcomes -- they do not exist yet at call time (the
    benchmark is constructed after this returns). Signature-enforced, not
    asserted.

    Returns (Q_S [d,5], v_hat_stack [d,5], sigma_min_over_max).
    """
    v_hats = []
    for vk in VOCAB_KEYS:
        dH = delta_h_by_vocab[vk]                       # [30, d]
        norms = torch.norm(dH, dim=1, keepdim=True) + 1e-12
        mean_v = (dH / norms).mean(dim=0)
        v_hats.append(mean_v / (torch.norm(mean_v) + 1e-12))
    V = torch.stack(v_hats, dim=1)                     # [d, 5]
    svals = torch.linalg.svdvals(V)
    ratio = float((svals.min() / (svals.max() + 1e-30)).item())
    Q_S, _R = torch.linalg.qr(V, mode="reduced")       # deterministic thin-QR
    return Q_S, V, ratio, [float(s) for s in svals]


def main():
    parser = argparse.ArgumentParser(description="EXP075: subspace-restricted bridge (pre-registered)")
    parser.add_argument("--allow-cpu", action="store_true",
                        help="override the CUDA-required guard on CPU-only machines "
                             "(strongly discouraged: ~1,080 forward passes on CPU "
                             "takes many hours and may hit session limits)")
    args = parser.parse_args()

    out_dir = os.path.join("experiments", "runs", "EXP075_subspace_bridge")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp075_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    torch.manual_seed(SEED_TORCH)
    np.random.seed(SEED_NUMPY)
    try:
        torch.use_deterministic_algorithms(True)
        log("torch.use_deterministic_algorithms(True) enabled.", log_file)
    except Exception as e:
        log(f"WARNING: deterministic algorithms unavailable ({e}); continuing.", log_file)

    log("=" * 80, log_file)
    log("EXP075: Subspace-Restricted Bridge (boundary science, not novelty science)", log_file)
    log("Pre-registered protocol: experiments/protocols/EXP075_SUBSPACE_BRIDGE_PREREG_SPEC.md", log_file)
    log(f"Model: {MODEL_NAME} | d={D} | target_layer={TARGET_LAYER} | alpha={ALPHA}", log_file)
    log("Protocol scope: IN-SCOPE (pythia-410m, layer 20) -- the ONLY registered config.", log_file)
    log("=" * 80, log_file)

    # CUDA FATAL (no silent CPU fallback; Law #8: a killed session is data).
    if not torch.cuda.is_available():
        if not args.allow_cpu:
            msg = ("FATAL: no CUDA GPU detected. EXP075 requires a GPU "
                   "(~1,080 forward passes; a CPU run takes many hours and will "
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
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)  # LOG-109: pin float32 -- script assumes float32 throughout (torch.randn defaults); matches historical EXP066 which ran this identical pattern without a dtype crash
    model.eval()
    model.to(device)

    # ---- F2: single-token entity guard (MAJOR). The spec / EXP066 procedure
    # assumes single-token entities. Abort LOUDLY (not silent first-subtoken
    # truncation) if ANY support or test entity encodes to more than one token.
    # Runs immediately after tokenizer load, before any forward pass and before
    # S construction. Checks the EXACT strings the code encodes: support
    # entities appear in prompts preceded by a space (" " + e); test entities
    # are encoded as " " + entity (target_token/foil_token).
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
            "experiment": "EXP075",
            "model": MODEL_NAME,
            "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
            "outcome": outcome,
            "halt_reason": reason,
            "pre_hash": pre_hash,
            "post_hash": get_hash(model),
            "target_layer": TARGET_LAYER,
            "hidden_dim": D,
            "alpha": ALPHA,
            "historical_baselines": HISTORICAL_BASELINES,
            "env_manifest": env_manifest,
        }
        payload.update(extra)
        with open(os.path.join(out_dir, "exp075_results.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        log("=" * 80, log_file)
        log(f"{outcome}: {reason}", log_file)
        log("THIS HALT IS THE REPORTABLE OUTCOME OF EXP075 (protocol §7.2).", log_file)
        log(f"Diagnostics written to {out_dir}/exp075_results.json", log_file)
        log("=" * 80, log_file)
        log_file.close()

    # -------------------------------------------------------------
    # 1. Support set: 5 vocabs x 30 contrast pairs (delta_h) -- the ONLY
    #    input the subspace construction ever sees (protocol §3.1, m1).
    # -------------------------------------------------------------
    log("\n[1] Support set: 5 vocabs x 30 contrast pairs (support-only input) ...", log_file)
    delta_h_by_vocab = {vk: [] for vk in VOCAB_KEYS}
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
            dh = o_rel.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu() - o_neu.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
            delta_h_by_vocab[vk].append(dh)
            support_ids.append(f"sup_{vk}_triple_{i}")
        for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
            A, B, C, D_ent = ents[iA], ents[iB], ents[iC], ents[iD]
            q_opts = f"{A} or {D_ent}" if (i % 2 == 0) else f"{D_ent} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
            with torch.no_grad():
                o_rel = model(input_ids=tokenizer.encode(p_rel, return_tensors="pt").to(device), output_hidden_states=True)
                o_neu = model(input_ids=tokenizer.encode(p_neu, return_tensors="pt").to(device), output_hidden_states=True)
            dh = o_rel.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu() - o_neu.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
            delta_h_by_vocab[vk].append(dh)
            support_ids.append(f"sup_{vk}_quad_{i}")
        delta_h_by_vocab[vk] = torch.stack(delta_h_by_vocab[vk])  # [30, d]
    log(f"Support contrast deltas: 5 x [30, {D}] (no test items exist yet).", log_file)

    # ---- Subspace S construction (BEFORE the benchmark exists; §3.1, m1) ----
    Q_S, V_hat, rank_ratio, svals = build_subspace_S(delta_h_by_vocab)
    log(f"S constructed: Q_S [1024, 5] via deterministic thin-QR; "
        f"sigma_min/sigma_max = {rank_ratio:.3e} (guard > {RANK_GUARD_RATIO:.0e}).", log_file)
    log(f"Singular values of the v_hat stack: {[f'{s:.4f}' for s in svals]}", log_file)
    if not (rank_ratio > RANK_GUARD_RATIO):
        save_halt("HALT_RANK",
                  f"rank guard failed (§3.1): sigma_min/sigma_max = {rank_ratio:.3e} "
                  f"<= {RANK_GUARD_RATIO:.0e}; S is degenerate -- the test would be "
                  f"uninformative. Reportable per §7.2; re-design required, not a "
                  f"re-run under EXP075.",
                  {"rank_ratio": rank_ratio, "singular_values": svals})
        print("RANK GUARD HALTED — THIS IS THE RESULT. Download exp075_results.json and report it.")
        sys.exit(0)
    log("RANK GUARD PASSED: numerical rank 5.", log_file)

    # v_hat_k archive + B_agg (identical construction to EXP065/066/067/070).
    v_hat_by_vocab = {vk: V_hat[:, k].clone() for k, vk in enumerate(VOCAB_KEYS)}
    sum_v = V_hat.sum(dim=1)
    B_agg = sum_v / (torch.norm(sum_v) + 1e-12)
    log(f"B_agg constructed (norm={float(torch.norm(B_agg)):.4f}); B_agg in S by construction.", log_file)

    torch.manual_seed(SEED_B_PERP)
    r_orth = torch.randn(D)
    r_orth -= B_agg * torch.dot(B_agg, r_orth)
    r_orth /= torch.norm(r_orth)
    B_perp = r_orth
    torch.manual_seed(SEED_TORCH)

    p_wrong_rel = "Fact: Paris is the capital of France. Question: What is the capital of France, Paris or London? Answer:"
    p_wrong_neu = "Fact: Paris is near London. Question: What is the capital of France, Paris or London? Answer:"
    with torch.no_grad():
        out_wr_rel = model(input_ids=tokenizer.encode(p_wrong_rel, return_tensors="pt").to(device), output_hidden_states=True)
        out_wr_neu = model(input_ids=tokenizer.encode(p_wrong_neu, return_tensors="pt").to(device), output_hidden_states=True)
    dH_wrong = out_wr_rel.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu() - out_wr_neu.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
    B_wrong = dH_wrong / (torch.norm(dH_wrong) + 1e-12)
    log("B_perp (seed 9876) and B_wrong (Paris-capital contrast, as EXP066) constructed.", log_file)

    # -------------------------------------------------------------
    # 2. Benchmark: N=60 Planetary/Elemental 2-hop/3-hop (EXP065/066
    #    construction; §5). Constructed AFTER S was frozen.
    # -------------------------------------------------------------
    log("\n[2] Benchmark: N=60 Planetary/Elemental 2-hop/3-hop (constructed after S froze) ...", log_file)
    novel_vocab_planet = NOVEL_VOCAB_PLANET    # module-level (F2 guard checked these)
    novel_vocab_element = NOVEL_VOCAB_ELEMENT  # module-level (F2 guard checked these)
    test_instances = []

    def _add(inst_id, hop, domain, prompt, target, foil):
        test_instances.append({
            "id": inst_id, "hop": hop, "domain": domain, "prompt": prompt,
            "target": target, "foil": foil,
            "target_token": " " + target, "foil_token": " " + foil,
        })

    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 8:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp075_planet_2hop_{i}", 2, "Planetary", p, A, C)
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC], novel_vocab_planet[iD]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 8:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp075_planet_3hop_{i}", 3, "Planetary", p, A, D_ent)
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 7:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp075_element_2hop_{i}", 2, "Elemental", p, A, C)
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC], novel_vocab_element[iD]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 7:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp075_element_3hop_{i}", 3, "Elemental", p, A, D_ent)
    assert len(test_instances) == 60, f"Expected 60 test instances, got {len(test_instances)}"
    test_ids = [t["id"] for t in test_instances]
    log(f"Benchmark: {len(test_instances)} instances (S already frozen; no-peeking preserved).", log_file)

    # -------------------------------------------------------------
    # 3. Bridges + projections + energy gate (§3.2-§3.4)  [precedence (a)]
    # -------------------------------------------------------------
    log("\n[3] Output bridges + subspace projections + ENERGY GATE ...", log_file)

    def make_bridge_vec(t_tok_idx, f_tok_idx):
        w = model.embed_out.weight[t_tok_idx, :].detach() - model.embed_out.weight[f_tok_idx, :].detach()
        return w / (torch.norm(w) + 1e-12)

    proj_S = Q_S @ Q_S.T                      # [d, d]
    bridge_records = {}                       # per-item projection archive
    e_list = []
    uS_vecs, uSperp_vecs = {}, {}
    for t in test_instances:
        tid = t["id"]
        tt = tokenizer.encode(t["target_token"])[0]
        ft = tokenizer.encode(t["foil_token"])[0]
        b_vec = make_bridge_vec(tt, ft)
        assert abs(float(torch.norm(b_vec).item()) - 1.0) < 1e-5, f"bridge not unit on {tid}"
        pS_pre = proj_S @ b_vec               # P_S(bridge), pre-norm
        pSp_pre = b_vec - pS_pre              # P_{S^perp}(bridge), pre-norm
        nS = float(torch.norm(pS_pre).item())
        nSp = float(torch.norm(pSp_pre).item())
        # F1 hygiene: normalize() of a zero vector is undefined. The spec is
        # silent; a loud abort is the non-silent option (measure-zero event).
        assert nS > 0, (f"FATAL (F1 guard): P_S(bridge) has zero norm on {tid} -- "
                        f"normalize() undefined. Aborting (measure-zero hygiene event).")
        assert nSp > 0, (f"FATAL (F1 guard): P_S^perp(bridge) has zero norm on {tid} -- "
                         f"normalize() undefined. Aborting (measure-zero hygiene event).")
        uS = pS_pre / nS
        uSp = pSp_pre / nSp
        e_i = nS / float(torch.norm(b_vec).item())   # = ||P_S bridge|| (bridge unit)
        e_list.append(e_i)
        uS_vecs[tid] = uS
        uSperp_vecs[tid] = uSp
        bridge_records[tid] = {
            "e": float(e_i),
            "proj_S_prenorm": pS_pre, "proj_S_unit": uS,
            "proj_Sperp_prenorm": pSp_pre, "proj_Sperp_unit": uSp,
            "bridge_norm": float(torch.norm(b_vec).item()),
        }
    e_arr = np.array(e_list)
    e_median = float(np.median(e_arr))
    e_sens = {f"{bar:.2f}": bool(e_median >= bar) for bar in ENERGY_SENSITIVITY}
    log(f"Energy ratio e = ||P_S bridge|| / ||bridge||: median = {e_median:.4f} "
        f"(gate: >= {ENERGY_BAR:.2f} [ARBITRARY, anchored at chance ~0.07]).", log_file)
    log(f"  per-item e: min={e_arr.min():.4f} max={e_arr.max():.4f} "
        f"q25={np.quantile(e_arr, 0.25):.4f} q75={np.quantile(e_arr, 0.75):.4f}", log_file)
    log(f"  sensitivity: " + ", ".join(f"bar {k}: {'PASS' if v else 'FAIL'}" for k, v in e_sens.items()), log_file)
    if not (e_median >= ENERGY_BAR):
        save_halt("HALT_ENERGY",
                  f"energy gate failed (§3.4): median e = {e_median:.4f} < {ENERGY_BAR:.2f} -- "
                  f"uninformative causal test, informative localization measurement: "
                  f"the bridge's causal power lies almost entirely outside S. "
                  f"Re-design required, not a re-run under EXP075 (reportable per §7.2).",
                  {"e_median": e_median, "e_distribution": {
                      "min": float(e_arr.min()), "q25": float(np.quantile(e_arr, 0.25)),
                      "median": e_median, "q75": float(np.quantile(e_arr, 0.75)),
                      "max": float(e_arr.max())},
                   "e_sensitivity": e_sens, "energy_bar": ENERGY_BAR,
                   "rank_ratio": rank_ratio, "singular_values": svals})
        print("ENERGY GATE HALTED — THIS IS THE RESULT. Download exp075_results.json and report it.")
        sys.exit(0)
    log("ENERGY GATE PASSED.", log_file)

    # -------------------------------------------------------------
    # 4. Intervention harness (hook at l*, last-token position)
    # -------------------------------------------------------------
    def run_with_intervention(prompt, t_tok_str, f_tok_str, vec):
        """Single forward with h <- h + alpha*vec at TARGET_LAYER (last token).

        Returns (correct_bool, t_logit, f_logit, kl_vs_base, h_delta_norm).
        vec is pre-scaled by ALPHA by the caller (uniform hook convention).
        """
        t_tok = tokenizer.encode(t_tok_str)[0]
        f_tok = tokenizer.encode(f_tok_str)[0]
        inp_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            out_b = model(input_ids=inp_ids, output_hidden_states=True)
        l_b = out_b.logits[0, -1, :]
        probs_b = F.softmax(l_b, dim=-1)
        h_b = out_b.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()

        v = vec.to(device).view(1, 1, -1)

        def hook_fn(module, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            h_mod = h + v
            if isinstance(outp, tuple):
                return (h_mod,) + outp[1:]
            return h_mod

        handle = layer_module.register_forward_hook(hook_fn)
        with torch.no_grad():
            out_m = model(input_ids=inp_ids, output_hidden_states=True)
        handle.remove()

        l_m = out_m.logits[0, -1, :]
        probs_m = F.softmax(l_m, dim=-1)
        t_l = float(l_m[t_tok].item()); f_l = float(l_m[f_tok].item())
        h_m = out_m.hidden_states[TARGET_LAYER + 1][0, -1, :].detach().cpu()
        return (bool(t_l > f_l), t_l, f_l,
                compute_kl(probs_b, probs_m),
                float(torch.norm(h_m - h_b).item()))

    def run_baseline(prompt, t_tok_str, f_tok_str):
        t_tok = tokenizer.encode(t_tok_str)[0]
        f_tok = tokenizer.encode(f_tok_str)[0]
        inp_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model(input_ids=inp_ids)
        t_l = float(out.logits[0, -1, t_tok].item())
        f_l = float(out.logits[0, -1, f_tok].item())
        return bool(t_l > f_l), (t_l - f_l)

    # -------------------------------------------------------------
    # 5. Baseline + headroom gate (protocol §5)  [precedence (b)]
    # -------------------------------------------------------------
    log("\n[5] BASELINE EVALUATION & HEADROOM GATE", log_file)
    base_correct, base_margins = [], []
    for t in test_instances:
        c, m = run_baseline(t["prompt"], t["target_token"], t["foil_token"])
        base_correct.append(c); base_margins.append(m)
    base_acc = float(np.mean(base_correct))
    log(f"Baseline Accuracy: {base_acc*100:.2f}% "
        f"({sum(base_correct)}/{len(test_instances)} correct).", log_file)
    if not (HEADROOM_LO <= base_acc <= HEADROOM_HI):
        save_halt("HALT_HEADROOM",
                  f"baseline accuracy {base_acc*100:.2f}% outside pre-registered "
                  f"40%-70% window (protocol §5, branch (b))",
                  {"baseline_accuracy": base_acc,
                   "e_median": e_median, "e_sensitivity": e_sens})
        print("HEADROOM GATE HALTED — THIS IS THE RESULT. Download exp075_results.json and report it.")
        sys.exit(0)
    log("HEADROOM GATE PASSED.", log_file)

    # Injection-norm guard for the static vectors (F1 lesson).
    injection_norms = {
        "C2_Static_B_agg": float(torch.norm(ALPHA * B_agg).item()),
        "C6_Static_B_perp": float(torch.norm(ALPHA * B_perp).item()),
        "C7_Static_B_wrong": float(torch.norm(ALPHA * B_wrong).item()),
    }
    for _k, _n in injection_norms.items():
        assert _n > 0, f"FATAL (F1 guard): {_k} has zero norm -- silent no-op. Aborting."
    log(f"Static injection-vector norms (F1 guard, all > 0): {json.dumps(injection_norms)}", log_file)

    # -------------------------------------------------------------
    # 6. Test conditions C1..C7 (protocol §4)
    # -------------------------------------------------------------
    log("\n[6] TEST CONDITIONS C1..C7 ...", log_file)
    N = len(test_instances)
    instance_records = {}
    for n, t in enumerate(test_instances):
        instance_records[t["id"]] = {"prompt": t["prompt"], "domain": t["domain"],
                                     "hop": t["hop"],
                                     "base_correct": bool(base_correct[n]),
                                     "e": bridge_records[t["id"]]["e"]}

    cond_correct = {}   # cond_name -> [bool]*N

    def eval_condition(cond_name, vec_fn):
        """vec_fn(test_item) -> intervention vector (pre-scaled by ALPHA)."""
        mod_correct, kl_list, margin_shifts = [], [], []
        for n, t in enumerate(test_instances):
            v = vec_fn(t)
            _vn = float(torch.norm(v).item())
            assert _vn > 0, (f"FATAL (F1 guard): {cond_name} zero vector on {t['id']} -- "
                             f"silent no-op. Aborting.")
            corr, t_l, f_l, kl, _dh = run_with_intervention(
                t["prompt"], t["target_token"], t["foil_token"], v)
            mod_correct.append(corr)
            kl_list.append(kl)
            margin_shifts.append((t_l - f_l) - base_margins[n])
            instance_records[t["id"]][f"{cond_name}_correct"] = bool(corr)
            instance_records[t["id"]][f"{cond_name}_kl_div"] = float(kl)
        b, c, delta_m, p_val = compute_paired_stats(base_correct, mod_correct)
        wilc_p = float(stats.wilcoxon(margin_shifts).pvalue) if any(m != 0 for m in margin_shifts) else 1.0
        cond_correct[cond_name] = mod_correct
        kl_mean = float(np.mean(kl_list))
        return {
            "name": cond_name,
            "acc_base": base_acc,
            "acc_mod": float(np.mean(mod_correct)),
            "delta_m": float(delta_m),
            "rescues_b": b, "corruptions_c": c,
            "exact_p": float(p_val),
            "wilcoxon_p": wilc_p,  # exploratory only (audit Finding 3 / O5)
            "delta_margin": float(np.mean(margin_shifts)),
            "kl_div": kl_mean,
            "kl_guardrail_exceeded": bool(kl_mean >= KL_GUARDRAIL),
        }

    results = {}
    # C1: unintervened baseline (statistics only; correctness already measured)
    results["C1_Unintervened_Baseline"] = {
        "name": "C1_Unintervened_Baseline", "acc_base": base_acc, "acc_mod": base_acc,
        "delta_m": 0.0, "rescues_b": 0, "corruptions_c": 0, "exact_p": 1.0,
        "wilcoxon_p": 1.0, "delta_margin": 0.0, "kl_div": 0.0,
        "kl_guardrail_exceeded": False,
    }
    cond_correct["C1_Unintervened_Baseline"] = [bool(x) for x in base_correct]
    log("C1 recorded (unintervened baseline).", log_file)

    log("Evaluating C2: Static B_agg (EXP066-identical; expected null per boundary result) ...", log_file)
    _c2v = ALPHA * B_agg
    results["C2_Static_B_agg"] = eval_condition("C2_Static_B_agg", lambda t: _c2v)

    log("Evaluating C3: Full output bridge (positive control; must replicate) ...", log_file)
    def _c3_fn(t):
        tt = tokenizer.encode(t["target_token"])[0]
        ft = tokenizer.encode(t["foil_token"])[0]
        return ALPHA * make_bridge_vec(tt, ft)
    results["C3_Full_Bridge"] = eval_condition("C3_Full_Bridge", _c3_fn)

    log("Evaluating C4: Subspace-restricted bridge (PRIMARY test condition) ...", log_file)
    results["C4_Subspace_Bridge"] = eval_condition(
        "C4_Subspace_Bridge", lambda t: ALPHA * uS_vecs[t["id"]])

    log("Evaluating C5: Complement-restricted bridge (discriminant) ...", log_file)
    results["C5_Complement_Bridge"] = eval_condition(
        "C5_Complement_Bridge", lambda t: ALPHA * uSperp_vecs[t["id"]])

    log("Evaluating C6: B_perp (C2 pipeline with orthogonalized basis) ...", log_file)
    _c6v = ALPHA * B_perp
    results["C6_Static_B_perp"] = eval_condition("C6_Static_B_perp", lambda t: _c6v)

    log("Evaluating C7: B_wrong (wrong-task basis, Paris-capital contrast) ...", log_file)
    _c7v = ALPHA * B_wrong
    results["C7_Static_B_wrong"] = eval_condition("C7_Static_B_wrong", lambda t: _c7v)

    log("\nStage B ledger:", log_file)
    log(f"{'Condition':<24} | {'Acc(Mod)':<8} | {'Delta_M':<9} | {'b':<4} | {'c':<4} | {'p-value':<8} | {'KL':<7} | {'KL>0.5':<6}", log_file)
    for _k, _r in results.items():
        log(f"{_r['name']:<24} | {_r['acc_mod']*100:>6.2f}% | {_r['delta_m']*100:>+7.2f}% | "
            f"{_r['rescues_b']:>4} | {_r['corruptions_c']:>4} | {_r['exact_p']:>8.4f} | "
            f"{_r['kl_div']:>7.4f} | {str(_r['kl_guardrail_exceeded']):<6}", log_file)

    # -------------------------------------------------------------
    # 7. SHA-256 post guard, Law #13 archive, results.json
    # -------------------------------------------------------------
    post_hash = get_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}", log_file)
    assert pre_hash == post_hash, "CRITICAL: Backbone parameter drift detected! Delta theta != 0."
    log("CONSTITUTIONAL COMPLIANCE CONFIRMED: Delta theta == 0 (binding pre/post match).", log_file)

    archive = {
        "Q_S": Q_S,                                   # [1024, 5] thin-QR basis
        "v_hat_stack": V_hat,                         # [1024, 5] the five v_hat_k
        "v_hat_by_vocab": v_hat_by_vocab,
        "B_agg": B_agg, "B_perp": B_perp, "B_wrong": B_wrong,
        "rank_ratio": rank_ratio, "singular_values": svals,
        "bridge_records": bridge_records,             # per item: pre/unit projections, e
        "uS_vecs": uS_vecs, "uSperp_vecs": uSperp_vecs,
        "support_ids": support_ids,
        "test_ids": test_ids,
        "seeds": {"torch": SEED_TORCH, "numpy": SEED_NUMPY, "B_perp": SEED_B_PERP},
    }
    torch.save(archive, os.path.join(out_dir, "exp075_vectors.pt"))
    log("Vector archive written: exp075_vectors.pt (Law #13).", log_file)

    results_payload = {
        "experiment": "EXP075",
        "model": MODEL_NAME,
        "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
        "outcome": "COMPLETED",
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "expected_sha256_sanity": EXPECTED_SHA256,
        "sha256_sanity_match": bool(pre_hash == EXPECTED_SHA256),
        "target_layer": TARGET_LAYER,
        "hidden_dim": D,
        "alpha": ALPHA,
        "seeds": archive["seeds"],
        "subspace": {
            "rank": 5,
            "rank_ratio_sigma_min_over_max": rank_ratio,
            "singular_values": svals,
        },
        "energy_gate": {
            "e_median": e_median,
            "energy_bar": ENERGY_BAR,
            "passed": True,
            "sensitivity": e_sens,
            "e_distribution": {
                "min": float(e_arr.min()), "q25": float(np.quantile(e_arr, 0.25)),
                "median": e_median, "q75": float(np.quantile(e_arr, 0.75)),
                "max": float(e_arr.max())},
        },
        "baseline_accuracy": base_acc,
        "historical_baselines": HISTORICAL_BASELINES,
        "stage_B_conditions": results,
        "injection_vector_norms": injection_norms,
        "env_manifest": env_manifest,
    }
    res_json_path = os.path.join(out_dir, "exp075_results.json")
    with open(res_json_path, "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)
    inst_json_path = os.path.join(out_dir, "exp075_instance_records.json")
    with open(inst_json_path, "w", encoding="utf-8") as f:
        json.dump(instance_records, f, indent=2)

    log(f"\nArtifacts saved to:\n  {res_json_path}\n  {inst_json_path}\n"
        f"  {os.path.join(out_dir, 'exp075_vectors.pt')} (Law #13 archive)\n  {log_path}", log_file)
    log("Run evaluate_exp075.py on exp075_results.json for the pre-registered decision-tree ruling.", log_file)
    log_file.close()
    print("EXP075 COMPLETED. Now run: python experiments/runs/exp075/evaluate_exp075.py")


if __name__ == "__main__":
    main()
