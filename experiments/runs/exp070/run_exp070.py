"""
EXP070: Oracle-Selection Ceiling -- Verifier-First, Generator-Second.
Pre-registered confirmatory protocol:
    experiments/protocols/EXP070_ORACLE_CEILING_PREREG_SPEC.md

Core scientific question:
    Can ANY per-instance selection over the loop's candidate pool -- even with
    an oracle's label access -- beat static CAA-equivalent injection?
    (H_ceiling vs H0; falsification decision tree in protocol §8.)

This is a kill-the-loop pre-test, not a method and not a novelty experiment
(protocol §1.1). The oracle's label access is a ceiling MEASUREMENT, not a
proposed method (protocol §1.1, §3.5). Law #7's test-time information boundary
applies to the EXP068 loop, not to this diagnostic.

SCOPE: EleutherAI/pythia-160m ONLY (in-scope; the loop's primary development
model per the EXP068 draft). No out-of-scope pilot config exists for EXP070.

Pipeline (protocol §9 order of operations):
    (1) support set + B_agg/B_perp/B_wrong + candidate pool P (17 directions)
    (2) probe-construction / N_final gate (metadata, no GPU)
    (3) headroom gate (C1 baseline)
    (4) 5-instance pilot (probe + smoke check) -> full probe + oracle selection
    (5) test conditions C1..C7, probe-signal diagnostics, decision inputs
Output directory: experiments/runs/EXP070_oracle_ceiling/

Conservative readings of protocol ambiguities (all logged):
    - Probe template-match (§3.2): a test item's signature is
      (hop, reversal, index-pattern). Support items expose (hop, index-pattern)
      by construction; they carry NO reversal phrasing. Matching therefore
      requires hop equality AND index-pattern equality; the reversal flag is
      recorded but does not block matching. Requiring phrasing match would
      exclude all 30 reversal test items -> N_final=30 < 50 -> stillborn
      protocol. This is the only executable reading and is stated as the
      conservative one (documented, not improvised: signatures are built from
      the shared benchmark-construction indices).
    - Probe items are the support p_rel prompts (labeled by construction:
      target = highest-ranked entity, foil = lowest) -- the labeled analogs of
      the loop's own per-instance views (protocol §3.2 NOTE).
    - (f) clause 2 "C3 ~= C4 while both beat C2" operationalized as:
      C3-vs-C2 significant positive AND C4-vs-C2 significant positive AND
      C3-vs-C4 McNemar p >= 0.05 (indistinguishable selection, both beat
      static). Documented here, not improvised at evaluation time.
    - Pilot (protocol §9 m4): implemented as an early diagnostic checkpoint
      after the first 5 instances' probe+oracle (not a separate run): prints
      diagnostics (i)/(iii) as a sanity signal plus wall-clock projection,
      then continues automatically. A pathological pilot (zero probe items)
      aborts loudly.

Governing standards:
    - AGENTS.md 14 Inviolable Laws (Law 6: Delta theta = 0; Law 7: zero
      leakage -- test labels never touch selection; Law 8: halts are
      reportable outcomes; Law 13: reproducibility + vector archiving)
    - STATISTICAL_PROTOCOL_V02.md
    - theory/LOOP_SPEC_DRAFT.md (signed -- the loop this pre-test gates)

Mechanically adapted from experiments/runs/exp067/run_exp067.py (harness:
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
# Configuration (protocol §2, §3.1, §10)
# ----------------------------------------------------------------------------
MODEL_NAME = "EleutherAI/pythia-160m"
D = 768
N_LAYERS = 12
TARGET_LAYER = 10          # l* = 10 (83% depth, matching EXP065)
ALPHA = 0.50               # fixed for all conditions (protocol §2)

SEED_TORCH = 20260923
SEED_NUMPY = 20260923
SEED_G1_BOOT = 7001        # G1 bootstrap resample indices
SEED_G1_DIR = 7002         # Dirichlet vocabulary weights
SEED_G2_RING = 7003        # G2-ring perturbations
SEED_C4_RAND = 7004        # C4 random selection
SEED_TIEBREAK = 7005       # oracle tie-break draw (archived per instance)
SEED_B_PERP = 9876         # inherited

N_G1 = 8                   # G1 draws
N_RING = 8                 # one G2-ring draw per G1 candidate
SIGMA_RING = 0.1           # perturbation scale (loop spec default)
N_POOL = N_G1 + N_RING + 1 # 17 = 8 + 8 + B_agg incumbent
N_PROBE_PER_VOCAB = 1      # one probe item per vocabulary -> 5 probe items
N_PROBE_MIN = 3            # protocol §3.2 minimum probe size
N_FINAL_MIN = 50           # protocol §5 power floor
HEADROOM_LO, HEADROOM_HI = 0.40, 0.70  # protocol §5
PILOT_N = 5                # protocol §9 m4: 5-instance pilot

SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Caleb", "Gideon", "Miriam", "Reuben"],
    "V3_Greek": ["Hector", "Jason", "Nestor", "Paris", "Priam"],
    "V4_Roman": ["Marcus", "Lucius", "Titus", "Felix", "Silas"],
    "V5_Modern": ["Liam", "Noah", "Sora", "Maya", "Leila"],
}
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())

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
# Utilities (identical to EXP066/067 harness)
# ----------------------------------------------------------------------------
def get_hash(model):
    """SHA-256 binding guard (protocol §2): SHA-256 over the concatenation of
    state_dict() tensors (sorted keys, CPU, float32 bytes). The guard is binding
    as a runtime pre/post match (E-4 distinction); no registered hash exists yet
    for EXP070 (first execution)."""
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


def main():
    parser = argparse.ArgumentParser(description="EXP070: oracle-selection ceiling (pre-registered)")
    parser.add_argument("--allow-cpu", action="store_true",
                        help="override the CUDA-required guard on CPU-only machines "
                             "(strongly discouraged: ~5,800 forward passes on CPU takes "
                             "many hours and may hit session limits)")
    args = parser.parse_args()

    out_dir = os.path.join("experiments", "runs", "EXP070_oracle_ceiling")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp070_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    torch.manual_seed(SEED_TORCH)
    np.random.seed(SEED_NUMPY)
    try:
        torch.use_deterministic_algorithms(True)
        log("torch.use_deterministic_algorithms(True) enabled.", log_file)
    except Exception as e:
        log(f"WARNING: deterministic algorithms unavailable ({e}); continuing.", log_file)

    log("=" * 80, log_file)
    log("EXP070: Oracle-Selection Ceiling (verifier-first, generator-second)", log_file)
    log("Pre-registered protocol: experiments/protocols/EXP070_ORACLE_CEILING_PREREG_SPEC.md", log_file)
    log(f"Model: {MODEL_NAME} | d={D} | target_layer={TARGET_LAYER} | alpha={ALPHA}", log_file)
    log("Protocol scope: IN-SCOPE (pythia-160m, layer 10) -- the ONLY registered config.", log_file)
    log("=" * 80, log_file)

    # CUDA FATAL (no silent CPU fallback; Law #8: a killed session is data).
    if not torch.cuda.is_available():
        if not args.allow_cpu:
            msg = ("FATAL: no CUDA GPU detected. EXP070 requires a GPU "
                   "(~5,800 forward passes; a CPU run takes many hours and will "
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

    # ---- SHA-256 guard: PRE (protocol §2; binding guard = pre/post match)
    pre_hash = get_hash(model)
    log(f"Pre-experiment parameter SHA-256: {pre_hash}", log_file)
    log("No registered hash for EXP070 (first execution); computed pre-hash is the run manifest.", log_file)

    layer_module = model.gpt_neox.layers[TARGET_LAYER]

    env_manifest = {
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": str(device),
        "model": MODEL_NAME,
        "protocol_scope": "IN-SCOPE (pythia-160m, layer 10)",
    }
    log(f"Environment manifest: {json.dumps(env_manifest)}", log_file)

    # -------------------------------------------------------------
    # 1. Support set: contrast pairs (delta_h) + labeled probe items
    # -------------------------------------------------------------
    log("\n[1] Support set: 5 vocabs x 30 contrast pairs + labeled probe items ...", log_file)
    delta_h_by_vocab = {vk: [] for vk in VOCAB_KEYS}
    # support_probe_items[vk] = list of labeled p_rel items (probe candidates)
    support_probe_items = {vk: [] for vk in VOCAB_KEYS}
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
            pid = f"sup_{vk}_triple_{i}"
            support_ids.append(pid)
            support_probe_items[vk].append({
                "id": pid, "vocab": vk, "hop": 2, "pattern": (iA, iB, iC),
                "index_in_vocab": i, "prompt": p_rel,
                "target": A, "foil": C,
                "target_token": " " + A, "foil_token": " " + C,
            })
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
            pid = f"sup_{vk}_quad_{i}"
            support_ids.append(pid)
            support_probe_items[vk].append({
                "id": pid, "vocab": vk, "hop": 3, "pattern": (iA, iB, iC, iD),
                "index_in_vocab": 15 + i, "prompt": p_rel,
                "target": A, "foil": D_ent,
                "target_token": " " + A, "foil_token": " " + D_ent,
            })
        delta_h_by_vocab[vk] = torch.stack(delta_h_by_vocab[vk])  # [30, d]
    log(f"Support contrast pairs: 5 x [30, {D}]. Labeled probe items: 5 x 30.", log_file)

    # v_hat_k per vocab + B_agg (identical construction to EXP065/066/067)
    v_hat_by_vocab = {}
    for vk, dH in delta_h_by_vocab.items():
        norms = torch.norm(dH, dim=1, keepdim=True) + 1e-12
        mean_v = (dH / norms).mean(dim=0)
        v_hat_by_vocab[vk] = mean_v / (torch.norm(mean_v) + 1e-12)
    sum_v = torch.stack([v_hat_by_vocab[vk] for vk in VOCAB_KEYS]).sum(dim=0)
    B_agg = sum_v / (torch.norm(sum_v) + 1e-12)
    log(f"B_agg constructed (norm={float(torch.norm(B_agg)):.4f}).", log_file)

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
    log("B_perp (seed 9876) and B_wrong (Paris-capital contrast) constructed.", log_file)

    # -------------------------------------------------------------
    # 2. Candidate pool P = 17 unit directions (protocol §3.1)
    # -------------------------------------------------------------
    log("\n[2] Candidate pool P: 8x G1 bootstrap + 8x G2-ring + B_agg incumbent ...", log_file)
    rng_boot = np.random.default_rng(SEED_G1_BOOT)
    rng_dir = np.random.default_rng(SEED_G1_DIR)
    rng_ring = np.random.default_rng(SEED_G2_RING)

    pool = []            # list of unit [d] tensors
    pool_meta = []       # provenance per candidate
    g1_draws = []        # the 8 G1 vectors (ring parents)
    for i in range(N_G1):
        per_vocab_means = []
        resample_idx = {}
        for vk in VOCAB_KEYS:
            idx = rng_boot.integers(0, 30, 30)          # bootstrap w/ replacement, stratified
            resample_idx[vk] = idx.tolist()
            dH_r = delta_h_by_vocab[vk][idx]
            nr = torch.norm(dH_r, dim=1, keepdim=True) + 1e-12
            mv = (dH_r / nr).mean(dim=0)
            per_vocab_means.append(mv / (torch.norm(mv) + 1e-12))
        w = rng_dir.dirichlet(np.ones(5))               # Dirichlet(1,...,1)
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
    pool_meta.append({"family": "incumbent", "draw": 0, "note": "B_agg static basis"})
    assert len(pool) == N_POOL == 17
    for j, v in enumerate(pool):
        assert abs(float(torch.norm(v).item()) - 1.0) < 1e-5, f"pool[{j}] not unit"
    log(f"Pool P built: {N_POOL} unit directions (8 G1 + 8 G2-ring + incumbent).", log_file)
    ring_cos = [m["cos_to_parent"] for m in pool_meta if m["family"] == "G2-ring"]
    log(f"G2-ring parent cosines: mean={float(np.mean(ring_cos)):.3f} "
        f"(spec §3.1: E[cos]≈0.34 at sigma=0.1, d=768).", log_file)

    # -------------------------------------------------------------
    # 3. Benchmark (N=60, identical items to EXP065/066) + signatures
    # -------------------------------------------------------------
    log("\n[3] Benchmark: N=60 Planetary/Elemental 2-hop/3-hop (EXP065 items) ...", log_file)
    novel_vocab_planet = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
    novel_vocab_element = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
    test_instances = []

    def _add(inst_id, hop, domain, prompt, target, foil, pattern, reversed_flag):
        test_instances.append({
            "id": inst_id, "hop": hop, "domain": domain, "prompt": prompt,
            "target": target, "foil": foil,
            "target_token": " " + target, "foil_token": " " + foil,
            # template/slot signature (protocol §3.2; loop spec §2.2):
            # tau = (hop, reversal); slot-signature = entity index pattern.
            "sig": {"hop": hop, "reversed": reversed_flag, "pattern": list(pattern)},
        })

    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp070_planet_2hop_{i}", 2, "Planetary", p, A, C, (iA, iB, iC), is_rev)
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC], novel_vocab_planet[iD]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp070_planet_3hop_{i}", 3, "Planetary", p, A, D_ent, (iA, iB, iC, iD), is_rev)
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp070_element_2hop_{i}", 2, "Elemental", p, A, C, (iA, iB, iC), is_rev)
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC], novel_vocab_element[iD]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        _add(f"exp070_element_3hop_{i}", 3, "Elemental", p, A, D_ent, (iA, iB, iC, iD), is_rev)
    assert len(test_instances) == 60, f"Expected 60 test instances, got {len(test_instances)}"
    test_ids = [t["id"] for t in test_instances]
    log(f"Benchmark: {len(test_instances)} instances with template/slot signatures.", log_file)

    # -------------------------------------------------------------
    # 4. Probe-construction gate (metadata, no GPU) + anti-cheat
    # -------------------------------------------------------------
    log("\n[4] Probe-construction gate (§3.2) + anti-cheat assertions (§3.5) ...", log_file)

    def save_halt(outcome, reason, extra):
        payload = {
            "experiment": "EXP070",
            "model": MODEL_NAME,
            "protocol_scope": "IN-SCOPE (pythia-160m, layer 10)",
            "outcome": outcome,
            "halt_reason": reason,
            "pre_hash": pre_hash,
            "post_hash": get_hash(model),
            "target_layer": TARGET_LAYER,
            "hidden_dim": D,
            "alpha": ALPHA,
            "env_manifest": env_manifest,
        }
        payload.update(extra)
        with open(os.path.join(out_dir, "exp070_results.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        log("=" * 80, log_file)
        log(f"{outcome}: {reason}", log_file)
        log("THIS HALT IS THE REPORTABLE OUTCOME OF EXP070 (protocol §8 branch (a)).", log_file)
        log(f"Diagnostics written to {out_dir}/exp070_results.json", log_file)
        log("=" * 80, log_file)
        log_file.close()

    # Template-matched probe map: for each test instance, one support item per
    # vocabulary with matching (hop, index-pattern), lowest support index first.
    probe_map = {}   # test_id -> list of 5 probe items
    probe_ids = []
    excluded = []
    for t in test_instances:
        sig = t["sig"]
        per_vocab = []
        for vk in VOCAB_KEYS:
            cands = [s for s in support_probe_items[vk]
                     if s["hop"] == sig["hop"] and tuple(s["pattern"]) == tuple(sig["pattern"])]
            cands.sort(key=lambda s: s["index_in_vocab"])
            if cands:
                per_vocab.append(cands[0])
        if len(per_vocab) < N_PROBE_MIN:
            excluded.append(t["id"])
            log(f"  EXCLUDED {t['id']}: only {len(per_vocab)} vocabulary-matched probe items (< {N_PROBE_MIN}).", log_file)
        else:
            probe_map[t["id"]] = per_vocab
            probe_ids.extend([p["id"] for p in per_vocab])
    N_final = len(probe_map)
    log(f"Probe map: {N_final}/60 test instances have >= {N_PROBE_MIN} probe items "
        f"({len(excluded)} excluded).", log_file)
    if N_final < N_FINAL_MIN:
        save_halt("HALT_PROBE",
                  f"probe-construction gate failed: N_final={N_final} < {N_FINAL_MIN} "
                  f"(protocol §3.2, §5; reportable, not adjustable under EXP070)",
                  {"N_final": N_final, "excluded": excluded})
        print("PROBE-CONSTRUCTION GATE HALTED — THIS IS THE RESULT. Download exp070_results.json and report it.")
        sys.exit(0)

    # ---- Anti-cheat as RUNTIME ASSERTIONS (the EXP067 F1 lesson applied to
    #      data hygiene): a leakage path must be IMPOSSIBLE, not just absent.
    #      Both assertions abort loudly as protocol violations (protocol §3.5(4)).
    _overlap_pt = set(probe_ids).intersection(set(test_ids))
    assert len(_overlap_pt) == 0, (
        f"FATAL (anti-cheat): probe_ids ∩ test_ids = {sorted(_overlap_pt)} -- "
        f"test items leaked into probe records. Protocol violation; aborting.")
    _overlap_st = set(support_ids).intersection(set(test_ids))
    assert len(_overlap_st) == 0, (
        f"FATAL (anti-cheat): support_ids ∩ test_ids = {sorted(_overlap_st)} -- "
        f"test items leaked into the support set (candidates are built from the "
        f"full support set). Protocol violation; aborting.")
    log("Anti-cheat assertions PASSED: probe∩test=∅ and support∩test=∅ (both archived).", log_file)

    final_instances = [t for t in test_instances if t["id"] in probe_map]
    log(f"N_final = {len(final_instances)} instances proceed to the pilot.", log_file)

    # -------------------------------------------------------------
    # 5. Intervention harness (hook at l*, last-token position)
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
    # 6. Baseline + headroom gate (protocol §5)
    # -------------------------------------------------------------
    log("\n[6] BASELINE EVALUATION & HEADROOM GATE", log_file)
    base_correct, base_margins = [], []
    for t in final_instances:
        c, m = run_baseline(t["prompt"], t["target_token"], t["foil_token"])
        base_correct.append(c); base_margins.append(m)
    base_acc = float(np.mean(base_correct))
    log(f"Baseline Accuracy: {base_acc*100:.2f}% "
        f"({sum(base_correct)}/{len(final_instances)} correct).", log_file)
    if not (HEADROOM_LO <= base_acc <= HEADROOM_HI):
        save_halt("HALT_HEADROOM",
                  f"baseline accuracy {base_acc*100:.2f}% outside pre-registered "
                  f"40%-70% window (protocol §5, §8 branch (a))",
                  {"baseline_accuracy": base_acc, "N_final": N_final})
        print("HEADROOM GATE HALTED — THIS IS THE RESULT. Download exp070_results.json and report it.")
        sys.exit(0)
    log("HEADROOM GATE PASSED.", log_file)

    # -------------------------------------------------------------
    # 7. Oracle probe evaluation + selection (protocol §3.2, §3.3)
    # -------------------------------------------------------------
    log("\n[7] ORACLE PROBE EVALUATION (17 candidates x 5 probe items/instance) ...", log_file)
    log("    Probe labels are SUPPORT labels -- ceiling measurement only (§1.1, §3.5).", log_file)

    gen_tie = torch.Generator().manual_seed(SEED_TIEBREAK)  # tie-break stream, instance order
    probe_records = {}   # test_id -> {probe_scores, selected_idx, tie_draw, ...}
    import time as _time
    t_probe_start = _time.time()

    for n_done, t in enumerate(final_instances):
        tid = t["id"]
        probes = probe_map[tid]
        scores = np.zeros(N_POOL)
        for j, B in enumerate(pool):
            vec = ALPHA * B
            r = 0
            for q in probes:
                corr, _, _, _, _ = run_with_intervention(
                    q["prompt"], q["target_token"], q["foil_token"], vec)
                r += int(corr)
            scores[j] = r / len(probes)
        best = float(scores.max())
        tied = [j for j in range(N_POOL) if scores[j] == best]
        if len(tied) == 1:
            sel, draw = tied[0], None
        else:
            # Direction-neutral seeded tie-break (protocol §3.3; M3 review):
            # uniform over top-tied candidates, seed 7005, archived.
            draw = int(torch.randint(len(tied), (1,), generator=gen_tie).item())
            sel = tied[draw]
        probe_records[tid] = {
            "probe_scores": [float(s) for s in scores],
            "selected_idx": int(sel),
            "tie_draw": draw,
            "n_tied": len(tied),
            "winner_rbar": float(best),
            "bagg_rbar": float(scores[N_POOL - 1]),  # incumbent is pool[16]
            "probe_item_ids": [q["id"] for q in probes],
        }
        # F1 guard (per-instance arm): the oracle must never select a zero vector.
        _sn = float(torch.norm(pool[sel]).item())
        assert _sn > 0, f"FATAL (F1 guard): oracle selected zero-norm pool[{sel}] on {tid}. Aborting."

        # ---- 5-instance pilot checkpoint (protocol §9 m4): diagnostics (i)/(iii)
        #      as a sanity signal (not a ruling) + wall-clock projection.
        if n_done + 1 == PILOT_N:
            el = _time.time() - t_probe_start
            _recs = [probe_records[tt["id"]] for tt in final_instances[:PILOT_N]]
            _di = float(np.mean([1.0 if r["winner_rbar"] > r["bagg_rbar"] else 0.0 for r in _recs]))
            _cnt = np.zeros(N_POOL, dtype=int)
            for r in _recs:
                _cnt[r["selected_idx"]] += 1
            _hsel = float(_cnt.max() / PILOT_N)
            proj = el / PILOT_N * len(final_instances)
            log("-" * 80, log_file)
            log(f"PILOT SMOKE CHECK ({PILOT_N} instances -- sanity signal, NOT a ruling):", log_file)
            log(f"  diagnostic (i): oracle-beats-B_agg on probe = {_di*100:.1f}%", log_file)
            log(f"  diagnostic (iii): selection concentration H_sel = {_hsel:.3f} (noise floor ~{1/N_POOL:.3f})", log_file)
            log(f"  wall-clock: {el:.1f}s for {PILOT_N} instances -> projected probe phase ~{proj/60:.1f} min", log_file)
            if _di == 0.0 and _hsel <= 1.0 / N_POOL + 1e-9:
                log("  WARNING: pilot probe shows no signal at all -- continuing per protocol,", log_file)
                log("  the probe-signal gate (§8) will rule on the full data.", log_file)
            log("-" * 80, log_file)

    t_probe = _time.time() - t_probe_start
    log(f"Oracle probe complete: {len(final_instances)} instances x {N_POOL} candidates x 5 probes "
        f"({t_probe/60:.1f} min).", log_file)

    # Injection-norm guard for the static vectors (F1 lesson: impossible, not just absent)
    injection_norms = {
        "C2_Static_B_agg": float(torch.norm(ALPHA * B_agg).item()),
        "C5_Static_B_perp": float(torch.norm(ALPHA * B_perp).item()),
        "C6_Static_B_wrong": float(torch.norm(ALPHA * B_wrong).item()),
    }
    for _k, _n in injection_norms.items():
        assert _n > 0, f"FATAL (F1 guard): {_k} has zero norm -- silent no-op. Aborting."
    log(f"Static injection-vector norms (F1 guard, all > 0): {json.dumps(injection_norms)}", log_file)

    def make_bridge_vec(tt, ft):
        w = model.embed_out.weight[tt, :].detach() - model.embed_out.weight[ft, :].detach()
        return w / (torch.norm(w) + 1e-12)

    # Per-instance selected vectors (oracle C3, random C4)
    gen_c4 = torch.Generator().manual_seed(SEED_C4_RAND)
    c3_vecs, c4_vecs = {}, {}
    for t in final_instances:
        tid = t["id"]
        c3_vecs[tid] = ALPHA * pool[probe_records[tid]["selected_idx"]]
        _j = int(torch.randint(N_POOL, (1,), generator=gen_c4).item())
        c4_vecs[tid] = (ALPHA * pool[_j], _j)
        probe_records[tid]["c4_idx"] = _j
        assert float(torch.norm(c3_vecs[tid]).item()) > 0, f"FATAL (F1 guard): C3 zero on {tid}."
        assert float(torch.norm(c4_vecs[tid][0]).item()) > 0, f"FATAL (F1 guard): C4 zero on {tid}."
        injection_norms[f"C3_Oracle[{tid}]"] = float(torch.norm(c3_vecs[tid]).item())
        injection_norms[f"C4_Random[{tid}]"] = float(torch.norm(c4_vecs[tid][0]).item())
    log("C3 (oracle-selected) and C4 (random-selected, seed 7004) vectors built per instance.", log_file)

    # -------------------------------------------------------------
    # 8. Test conditions C1..C7 (protocol §4)
    # -------------------------------------------------------------
    log("\n[8] TEST CONDITIONS C1..C7 ...", log_file)
    N = len(final_instances)
    instance_records = {}
    for n, t in enumerate(final_instances):
        instance_records[t["id"]] = {"prompt": t["prompt"], "domain": t["domain"],
                                     "hop": t["hop"], "sig": t["sig"],
                                     "base_correct": bool(base_correct[n]),
                                     "oracle_selected_idx": probe_records[t["id"]]["selected_idx"],
                                     "c4_selected_idx": probe_records[t["id"]]["c4_idx"]}

    cond_correct = {}   # cond_name -> [bool]*N

    def eval_condition(cond_name, vec_fn):
        """vec_fn(test_item) -> intervention vector (pre-scaled by ALPHA)."""
        mod_correct, kl_list, margin_shifts = [], [], []
        for n, t in enumerate(final_instances):
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
        return {
            "name": cond_name,
            "acc_base": base_acc,
            "acc_mod": float(np.mean(mod_correct)),
            "delta_m": float(delta_m),
            "rescues_b": b, "corruptions_c": c,
            "exact_p": float(p_val),
            "wilcoxon_p": wilc_p,  # exploratory only (audit Finding 3 / O5)
            "delta_margin": float(np.mean(margin_shifts)),
            "kl_div": float(np.mean(kl_list)),
        }

    results = {}
    # C1: unintervened baseline (statistics only; correctness already measured)
    results["C1_Unintervened_Baseline"] = {
        "name": "C1_Unintervened_Baseline", "acc_base": base_acc, "acc_mod": base_acc,
        "delta_m": 0.0, "rescues_b": 0, "corruptions_c": 0, "exact_p": 1.0,
        "wilcoxon_p": 1.0, "delta_margin": 0.0, "kl_div": 0.0,
    }
    cond_correct["C1_Unintervened_Baseline"] = [bool(x) for x in base_correct]
    log("C1 recorded (unintervened baseline).", log_file)

    log("Evaluating C2: Static B_agg (CAA-equivalent benchmark) ...", log_file)
    _c2v = ALPHA * B_agg
    results["C2_Static_B_agg"] = eval_condition("C2_Static_B_agg", lambda t: _c2v)

    log("Evaluating C3: Oracle-selected per-instance direction (PRIMARY) ...", log_file)
    results["C3_Oracle_Selected"] = eval_condition(
        "C3_Oracle_Selected", lambda t: c3_vecs[t["id"]])

    log("Evaluating C4: Random-selected candidate ...", log_file)
    results["C4_Random_Selected"] = eval_condition(
        "C4_Random_Selected", lambda t: c4_vecs[t["id"]][0])

    log("Evaluating C5: Static B_perp ...", log_file)
    _c5v = ALPHA * B_perp
    results["C5_Static_B_perp"] = eval_condition("C5_Static_B_perp", lambda t: _c5v)

    log("Evaluating C6: Static B_wrong ...", log_file)
    _c6v = ALPHA * B_wrong
    results["C6_Static_B_wrong"] = eval_condition("C6_Static_B_wrong", lambda t: _c6v)

    log("Evaluating C7: Same-layer output bridge (positive control) ...", log_file)
    def _c7_fn(t):
        tt = tokenizer.encode(t["target_token"])[0]
        ft = tokenizer.encode(t["foil_token"])[0]
        return ALPHA * make_bridge_vec(tt, ft)
    results["C7_Output_Bridge"] = eval_condition("C7_Output_Bridge", _c7_fn)

    log("\nStage B ledger:", log_file)
    log(f"{'Condition':<28} | {'Acc(Mod)':<8} | {'Delta_M':<9} | {'b':<4} | {'c':<4} | {'p-value':<8} | {'KL':<7}", log_file)
    for _k, _r in results.items():
        log(f"{_r['name']:<28} | {_r['acc_mod']*100:>6.2f}% | {_r['delta_m']*100:>+7.2f}% | "
            f"{_r['rescues_b']:>4} | {_r['corruptions_c']:>4} | {_r['exact_p']:>8.4f} | {_r['kl_div']:>7.4f}", log_file)

    # -------------------------------------------------------------
    # 9. Paired comparisons (decision inputs for the tree)
    # -------------------------------------------------------------
    def _cmp(a_name, b_name):
        b, c, dm, p = compute_paired_stats(cond_correct[a_name], cond_correct[b_name])
        return {"b": b, "c": c, "delta_m": float(dm), "exact_p": float(p)}

    comparisons = {
        "C3_vs_C2": _cmp("C2_Static_B_agg", "C3_Oracle_Selected"),   # THE kill comparison
        "C3_vs_C4": _cmp("C4_Random_Selected", "C3_Oracle_Selected"),
        "C4_vs_C2": _cmp("C2_Static_B_agg", "C4_Random_Selected"),
        "C3_vs_C1": _cmp("C1_Unintervened_Baseline", "C3_Oracle_Selected"),
        "C4_vs_C1": _cmp("C1_Unintervened_Baseline", "C4_Random_Selected"),
        "C2_vs_C1": _cmp("C1_Unintervened_Baseline", "C2_Static_B_agg"),
        "C7_vs_C1": _cmp("C1_Unintervened_Baseline", "C7_Output_Bridge"),
    }
    log("\nPaired comparisons (b = second rescues over first):", log_file)
    for _k, _v in comparisons.items():
        log(f"  {_k}: b={_v['b']} c={_v['c']} ΔM={_v['delta_m']*100:+.2f}pp p={_v['exact_p']:.6f}", log_file)

    # -------------------------------------------------------------
    # 10. Probe-signal gate diagnostics (protocol §6, §8)
    # -------------------------------------------------------------
    log("\n[10] PROBE-SIGNAL GATE DIAGNOSTICS (§6, §8) ...", log_file)
    c2c = cond_correct["C2_Static_B_agg"]
    c3c = cond_correct["C3_Oracle_Selected"]
    Y = np.array([1.0 if (not a and b) else 0.0 for a, b in zip(c2c, c3c)], dtype=float)
    # Y_x = 1[C3 correct and C2 incorrect on x] -- beats-static head-to-head.
    probe_margins = np.array([probe_records[t["id"]]["winner_rbar"]
                              - probe_records[t["id"]]["bagg_rbar"]
                              for t in final_instances], dtype=float)
    diag_i = float(np.mean([1.0 if probe_records[t["id"]]["winner_rbar"]
                            > probe_records[t["id"]]["bagg_rbar"] else 0.0
                            for t in final_instances]))
    sel_counts = np.zeros(N_POOL, dtype=int)
    for t in final_instances:
        sel_counts[probe_records[t["id"]]["selected_idx"]] += 1
    H_sel = float(sel_counts.max() / N)

    Y_var_nonzero = bool(np.var(Y) > 0)
    r_pb, r_pb_p = None, None
    gate_path, gate_passed = None, False
    if Y_var_nonzero:
        # Diagnostic (ii): point-biserial r_pb(probe margin, Y); one-sided p<0.05.
        pr = stats.pointbiserialr(probe_margins, Y)
        r_pb = float(pr.statistic)
        if np.isnan(r_pb):
            # Defensive: probe margins carry no variance -> probe did not
            # differentiate candidates at all -> uninformative -> gate fails.
            gate_path, gate_passed = "ii-undefined", False
            log("  (ii) undefined (probe margins zero-variance) -> gate FAILS (uninformative).", log_file)
        else:
            df = N - 2
            t_stat = r_pb * np.sqrt(df / max(1e-12, 1 - r_pb ** 2))
            r_pb_p = float(stats.t.sf(t_stat, df))  # one-sided, H1: r > 0
            gate_path = "ii"
            gate_passed = bool(r_pb > 0 and r_pb_p < 0.05)
            log(f"  (ii) r_pb = {r_pb:+.4f}, one-sided p = {r_pb_p:.6f} "
                f"-> gate {'PASSES' if gate_passed else 'FAILS'}.", log_file)
    else:
        # (ii) undefined (oracle never beat static on any instance): gate passes
        # iff (iii) H_sel >= 25% -- probe drove selection decisively yet nothing
        # transferred: a measured zero (protocol §8).
        gate_path = "iii"
        gate_passed = bool(H_sel >= 0.25)
        log(f"  Y zero-variance (oracle never beat static head-to-head); "
            f"(iii) H_sel = {H_sel:.3f} -> gate {'PASSES' if gate_passed else 'FAILS'}.", log_file)
    log(f"  (i) oracle-beats-B_agg on probe: {diag_i*100:.1f}% (reported only; does not gate).", log_file)
    log(f"  (iii) selection concentration H_sel = {H_sel:.3f} "
        f"(noise floor ~{1.0/N_POOL:.3f}; floor 0.25 [ARBITRARY]).", log_file)

    probe_gate = {
        "passed": bool(gate_passed),
        "path": gate_path,
        "r_pb": r_pb,
        "r_pb_one_sided_p": r_pb_p,
        "Y_variance_nonzero": bool(Y_var_nonzero),
        "H_sel": float(H_sel),
        "diag_i_oracle_beats_bagg_on_probe": float(diag_i),
        "n": int(N),
    }

    # (g) consistency check: C2 replicates the EXP065 null while C7 rescues
    c2v1 = comparisons["C2_vs_C1"]
    c7v1 = comparisons["C7_vs_C1"]
    c7_valid = bool(c7v1["delta_m"] > 0 and c7v1["exact_p"] < 0.05)
    consistency_g = {
        "C2_replicates_EXP065_null": bool(c2v1["b"] == 0 and c2v1["c"] == 0),
        "C7_rescues": c7_valid,
        "C2_discrepancy_flag": bool(c2v1["delta_m"] != 0.0),
        "note": ("C2 ΔM=0 with b=c=0 while C7 rescues: boundary null replicates under "
                 "this run's conditions." if (c2v1["b"] == 0 and c2v1["c"] == 0 and c7_valid)
                 else "See discrepancy flag; interpret branches with the benchmark/drift diagnostic in mind."),
    }
    log(f"  (g) C2 replicates EXP065 null: {consistency_g['C2_replicates_EXP065_null']}; "
        f"C7 rescues: {c7_valid}; C2 discrepancy flag: {consistency_g['C2_discrepancy_flag']}.", log_file)

    # -------------------------------------------------------------
    # 11. SHA-256 post guard, Law #13 archive, results.json
    # -------------------------------------------------------------
    post_hash = get_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}", log_file)
    assert pre_hash == post_hash, "CRITICAL: Backbone parameter drift detected! Delta theta != 0."
    log("CONSTITUTIONAL COMPLIANCE CONFIRMED: Delta theta == 0 (binding pre/post match).", log_file)

    # Post-run audit: no test id may appear in any probe record (protocol §3.5(1)).
    for tid, rec in probe_records.items():
        assert tid not in rec["probe_item_ids"], f"ANTI-CHEAT VIOLATION: test id {tid} in its own probe record."
    log("Post-run anti-cheat audit PASSED: no test id in any probe record.", log_file)

    archive = {
        "pool_vectors": torch.stack(pool),          # [17, d]
        "pool_meta": pool_meta,
        "B_agg": B_agg, "B_perp": B_perp, "B_wrong": B_wrong,
        "v_hat_by_vocab": v_hat_by_vocab,
        "delta_h_by_vocab": delta_h_by_vocab,
        "probe_records": probe_records,             # per-instance probe scores, selection, tie draw
        "probe_map_ids": {tid: [q["id"] for q in probe_map[tid]] for tid in probe_map},
        "support_ids": support_ids,
        "test_ids": test_ids,
        "excluded_ids": excluded,
        "seeds": {"torch": SEED_TORCH, "numpy": SEED_NUMPY, "G1_boot": SEED_G1_BOOT,
                  "G1_dir": SEED_G1_DIR, "G2_ring": SEED_G2_RING, "C4": SEED_C4_RAND,
                  "tiebreak": SEED_TIEBREAK, "B_perp": SEED_B_PERP},
    }
    torch.save(archive, os.path.join(out_dir, "exp070_vectors.pt"))
    log("Vector archive written: exp070_vectors.pt (Law #13).", log_file)

    results_payload = {
        "experiment": "EXP070",
        "model": MODEL_NAME,
        "protocol_scope": "IN-SCOPE (pythia-160m, layer 10)",
        "outcome": "COMPLETED",
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "target_layer": TARGET_LAYER,
        "hidden_dim": D,
        "alpha": ALPHA,
        "seeds": archive["seeds"],
        "baseline_accuracy": base_acc,
        "N_final": N,
        "N_excluded": len(excluded),
        "probe_gate": probe_gate,
        "stage_B_conditions": results,
        "comparisons": comparisons,
        "injection_vector_norms": injection_norms,
        "consistency_check_g": consistency_g,
        "pool_info": {"n_candidates": N_POOL, "n_G1": N_G1, "n_ring": N_RING,
                      "sigma_ring": SIGMA_RING},
        "env_manifest": env_manifest,
    }
    res_json_path = os.path.join(out_dir, "exp070_results.json")
    with open(res_json_path, "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)
    inst_json_path = os.path.join(out_dir, "exp070_instance_records.json")
    with open(inst_json_path, "w", encoding="utf-8") as f:
        json.dump(instance_records, f, indent=2)

    log(f"\nArtifacts saved to:\n  {res_json_path}\n  {inst_json_path}\n"
        f"  {os.path.join(out_dir, 'exp070_vectors.pt')} (Law #13 archive)\n  {log_path}", log_file)
    log("Run evaluate_exp070.py on exp070_results.json for the pre-registered decision-tree ruling.", log_file)
    log_file.close()
    print("EXP070 COMPLETED. Now run: python experiments/runs/exp070/evaluate_exp070.py")


if __name__ == "__main__":
    main()
