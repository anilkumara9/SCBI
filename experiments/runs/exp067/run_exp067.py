"""
EXP067: Attention-Head QK/OV Subspace Procrustes Projection.
Pre-registered confirmatory protocol:
    experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md

Core scientific question:
    Does a SOUND Procrustes alignment operator enable causal transfer of
    cross-vocabulary relational bases where the unsound EXP065/066 operator
    could not? (H1 vs H0; falsification decision tree in protocol §7.)

SCOPE NOTE (honest labeling; cf. protocol §1.1, §2):
    The signed protocol pre-registers EleutherAI/pythia-410m (24 layers,
    d=1024, 16 heads, target layer 20) -- this is the script's DEFAULT.
    EleutherAI/pythia-160m (12 layers, d=768, 12 heads, target layer 10 =
    83% proportional depth, same convention as EXP066's layer comment) is
    available via `--model pythia-160m` as an OUT-OF-PROTOCOL-SCOPE pilot
    only: it prints an explicit OUT-OF-SCOPE PILOT banner, its results.json
    carries "protocol_scope": "OUT-OF-SCOPE ...", and evaluate_exp067.py
    prints NO PROTOCOL RULING for such runs (scope-gated). No mechanism,
    hyperparameter, seed, gate, or endpoint differs between configs except
    the model-dependent geometry (d, n_heads, target layer).

Conservative readings of protocol ambiguities (all logged):
    - Support frame for (supp -> V_test) fits: V1_Anglo (matches EXP065/066
      E_0 convention). Two rotations: V1->Planetary, V1->Elemental.
    - Anchor pairing: index-aligned (i-th entity <-> i-th entity), same
      template j <-> j; 5 entities x 16 templates = 80 pairs.
    - Rank/spectral guard violation on ANY head fit: abort whole run
      (protocol: "abort on violation") -> HALT_STAGE_A branch (a).
    - Fewer than K=4 heads with g_h > 0: H* = all passing heads; zero ->
      Stage A halt.
    - Stage C (EXP066's specificity probes) is NOT in the EXP067 protocol
      and is therefore NOT run (Law #9: no unregistered conditions).

Governing standards:
    - AGENTS.md 14 Inviolable Laws (Law 6: Delta theta = 0; Law 7: zero
      leakage; Law 8: halts are reportable outcomes; Law 13: reproducibility
      + Law #13 vector archiving)
    - STATISTICAL_PROTOCOL_V02.md
    - theory/proofs/procrustes_failure_analysis.md

Mechanically adapted from experiments/scripts/run_exp066_pythia410m_replication.py.
Output directory per protocol §7.2: experiments/runs/EXP067_qkov_subspace_procrustes/
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
# Configuration
# ----------------------------------------------------------------------------
MODEL_CONFIGS = {
    "pythia-160m": {
        "hf_name": "EleutherAI/pythia-160m",
        "d": 768,
        "n_layers": 12,
        "n_heads": 12,
        "head_dim": 64,
        "target_layer": 10,  # 83% proportional depth (EXP066 convention)
        "expected_sha256": None,  # not registered; recorded at runtime
        "protocol_scope": "OUT-OF-SCOPE (pre-registration fixes pythia-410m)",
    },
    "pythia-410m": {
        "hf_name": "EleutherAI/pythia-410m",
        "d": 1024,
        "n_layers": 24,
        "n_heads": 16,
        "head_dim": 64,
        "target_layer": 20,  # 83% depth, protocol §2
        "expected_sha256": "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd",
        "protocol_scope": "IN-SCOPE (pythia-410m, layer 20)",
    },
}

SEED_TORCH = 20260923
SEED_NUMPY = 20260923
C5_SEEDS = [11, 22, 33, 44, 55]   # protocol §8
B_PERP_SEED = 9876                # inherited from EXP066
ALPHA = 0.50                      # protocol §3.4 (inherited)
K_HEADS = 4                       # protocol §3.5
N_ANCHOR_TEMPLATES = 16
N_ANCHOR_ENTITIES = 5             # 5 entities x 16 templates = 80 pairs
RANK_TOL_GAP = 1e-6               # spectral-gap guard, protocol §3.3
HEADROOM_LO, HEADROOM_HI = 0.40, 0.70  # protocol §5

# 16 pre-registered anchor prompt templates (entity-frame; disjoint from all
# test benchmark prompts: no "outranks", no "Question:", no "Answer:").
ANCHOR_TEMPLATES = [
    "{e} kept a detailed journal of the northern expedition.",
    "The council appointed {e} as keeper of the archives.",
    "{e} was celebrated for extraordinary bravery.",
    "Travelers spoke of {e} with great respect.",
    "{e} built a small cabin near the river.",
    "The old map was drawn by {e} many years ago.",
    "{e} shared stories around the evening fire.",
    "Everyone in the village knew {e} by name.",
    "{e} planted an orchard on the hillside.",
    "The merchant traded rare spices with {e}.",
    "{e} wrote letters that were never sent.",
    "A statue of {e} stands in the town square.",
    "{e} studied the stars from the rooftop.",
    "The sailors trusted {e} to navigate the strait.",
    "{e} repaired the bridge after the storm.",
    "Children gathered to hear {e} tell tales.",
]
assert len(ANCHOR_TEMPLATES) == N_ANCHOR_TEMPLATES

# ----------------------------------------------------------------------------
# Utilities (identical to EXP066 harness)
# ----------------------------------------------------------------------------
def get_hash(model):
    sha = hashlib.sha256()
    for p in model.parameters():
        sha.update(p.detach().cpu().numpy().tobytes())
    return sha.hexdigest()


def compute_kl(p_base, p_mod):
    p_base = torch.clamp(p_base, min=1e-12)
    p_mod = torch.clamp(p_mod, min=1e-12)
    return float(torch.sum(p_base * (torch.log(p_base) - torch.log(p_mod))).item())


def compute_paired_stats(base_correct, mod_correct):
    b = 0  # base wrong, mod correct (rescues)
    c = 0  # base correct, mod wrong (corruptions)
    for bc, mc in zip(base_correct, mod_correct):
        if not bc and mc:
            b += 1
        elif bc and not mc:
            c += 1
    if b + c == 0:
        p_val = 1.0
    else:
        res = stats.binomtest(min(b, c), b + c, 0.5, alternative="two-sided")
        p_val = float(res.pvalue)
    delta_m = (b - c) / len(base_correct)
    return b, c, delta_m, p_val


def log(msg, log_file=None):
    print(msg, flush=True)
    if log_file:
        log_file.write(msg + "\n")
        log_file.flush()


def collect_head_outputs(model, tokenizer, layer_attn, prompts, n_heads, head_dim, device, log_file):
    """Capture per-head output vectors o_h = W_O^{(h)} z_h at the last token.

    Hooks the attention `dense` submodule input (merged heads), slices per-head
    z_h, and multiplies by the head's W_O block. Returns [n_prompts, n_heads, d].

    Runtime self-check (guards the head-slicing assumption): for every prompt,
    sum_h o_h + bias must equal dense(merged_input) to 1e-3. If HF's internal
    layout ever changes, this fails loudly instead of silently corrupting fits.
    """
    captured = {}

    def hook_fn(module, inp, outp):
        captured["merged"] = inp[0].detach()

    handle = layer_attn.dense.register_forward_hook(hook_fn)
    W = layer_attn.dense.weight.detach().cpu()          # [d, d]
    b = layer_attn.dense.bias.detach().cpu() if layer_attn.dense.bias is not None else None
    d = W.shape[0]
    assert W.shape == (d, d), f"dense weight shape {tuple(W.shape)} != ({d}, {d})"
    assert d == n_heads * head_dim

    all_o = []
    with torch.no_grad():
        for p in prompts:
            ids = tokenizer.encode(p, return_tensors="pt").to(device)
            captured.clear()
            model(input_ids=ids)
            merged = captured["merged"][0, -1, :].cpu()          # [d]
            o_heads = []
            for h in range(n_heads):
                z_h = merged[h * head_dim:(h + 1) * head_dim]    # [64]
                Wb = W[:, h * head_dim:(h + 1) * head_dim]       # [d, 64]
                o_heads.append(Wb @ z_h)                        # [d]
            o_stack = torch.stack(o_heads)                      # [H, d]
            recon = o_stack.sum(dim=0) + (b if b is not None else 0.0)
            dense_out = merged @ W.T + (b if b is not None else 0.0)
            assert torch.allclose(recon, dense_out, atol=1e-3), \
                "head decomposition self-check FAILED: sum_h o_h != dense(x)-bias"
            all_o.append(o_stack)
    handle.remove()
    log(f"  hook lifecycle ok: dense-input hook registered and removed ({len(prompts)} prompts).", log_file)
    return torch.stack(all_o)  # [n_prompts, H, d]


def fit_subspace_procrustes(A_sub, B_sub):
    """Full-rank subspace Procrustes with pre-registered runtime guards.

    A_sub, B_sub: [m, 64] subspace-coordinate anchor stacks (m=80).
    Returns (R_tilde [64,64], rank, spectral_gap). Guards (protocol §3.3):
      rank(M_tilde) == 64 and sigma_64/sigma_1 > 1e-6, else the fit is
      REJECTED (caller must abort -> HALT_STAGE_A, branch (a)).
    """
    M = B_sub.T @ A_sub                       # [64, 64]
    U, S, Vh = torch.linalg.svd(M)
    rank = int(torch.linalg.matrix_rank(M).item())
    gap = float((S[-1] / (S[0] + 1e-30)).item())
    R_tilde = U @ Vh                          # [64, 64] orthogonal
    return R_tilde, rank, gap, S


def main():
    parser = argparse.ArgumentParser(description="EXP067: QK/OV subspace Procrustes (pre-registered)")
    parser.add_argument("--model", default="pythia-410m", choices=list(MODEL_CONFIGS.keys()),
                        help="pythia-410m (default, IN-SCOPE) or pythia-160m (OUT-OF-SCOPE pilot)")
    parser.add_argument("--allow-cpu", action="store_true",
                        help="override the CUDA-required guard on CPU-only machines "
                             "(strongly discouraged: ~2,100 forward passes on CPU takes "
                             "many hours and may hit session limits)")
    args = parser.parse_args()
    cfg = MODEL_CONFIGS[args.model]
    d, n_heads, head_dim = cfg["d"], cfg["n_heads"], cfg["head_dim"]
    target_layer = cfg["target_layer"]
    assert d == n_heads * head_dim == 64 * n_heads

    out_dir = os.path.join("experiments", "runs", "EXP067_qkov_subspace_procrustes")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp067_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    torch.manual_seed(SEED_TORCH)
    np.random.seed(SEED_NUMPY)
    try:
        torch.use_deterministic_algorithms(True)
        log("torch.use_deterministic_algorithms(True) enabled.", log_file)
    except Exception as e:
        log(f"WARNING: deterministic algorithms unavailable ({e}); continuing.", log_file)

    log("=" * 80, log_file)
    log("EXP067: Attention-Head QK/OV Subspace Procrustes Projection", log_file)
    log("Pre-registered protocol: experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md", log_file)
    log(f"Model config: {args.model} | d={d} | heads={n_heads} | target_layer={target_layer}", log_file)
    log(f"Protocol scope: {cfg['protocol_scope']}", log_file)
    if args.model == "pythia-160m":
        # M2: out-of-scope pilot must be unmissable at runtime, not just in the JSON.
        log("=" * 80, log_file)
        log("OUT-OF-SCOPE PILOT -- NO PROTOCOL RULING", log_file)
        log("This run uses pythia-160m; the signed protocol pre-registers pythia-410m",
            log_file)
        log("ONLY. Statistics are reported raw; evaluate_exp067.py will print", log_file)
        log("'NO PROTOCOL RULING -- OUT-OF-SCOPE PILOT' instead of a branch ruling.", log_file)
        log("=" * 80, log_file)
    log("=" * 80, log_file)

    # M3: fail LOUDLY without CUDA -- a silent CPU fallback would burn ~2,100
    # forward passes over many hours (likely hitting session limits) with no error.
    if not torch.cuda.is_available():
        if not args.allow_cpu:
            msg = ("FATAL: no CUDA GPU detected. EXP067 requires a GPU "
                   "(~2,100 forward passes; a CPU run takes many hours and will "
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

    model_name = cfg["hf_name"]
    log(f"Loading model & tokenizer: {model_name} ...", log_file)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # Mechanical pin (LOG-109 class): transformers 5.x defaults from_pretrained
    # to float16; the runner's CPU-side statistics (torch.randn, QR, SVD) are
    # float32 and torch.dot/matmul do not promote (Half vs Float crashes at
    # B_perp construction). Pinning float32 is values-neutral vs the registered
    # protocol (which assumes float32: §2 guard hashes "float32 bytes") and
    # matches EXP070/075/077/078. `torch_dtype` is deprecation-warned but
    # functional in transformers 5.x (cf. EXP077 m4).
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)
    model.eval()
    model.to(device)

    # ---- SHA-256 guard: PRE (binding guard = pre/post match; registered value = sanity check per E-4)
    pre_hash = get_hash(model)
    log(f"Pre-experiment parameter SHA-256: {pre_hash}", log_file)
    if cfg["expected_sha256"] is not None:
        if pre_hash == cfg["expected_sha256"]:
            log("Model hash matches registered manifest value (sanity check).", log_file)
        else:
            log("WARNING (E-4): pre-hash differs from registered manifest value; "
                "registered value is a sanity check only, NOT an abort trigger. "
                "Binding guard remains the runtime pre/post match.", log_file)
    else:
        log("No registered hash for this config; computed pre-hash is recorded as the run manifest.", log_file)

    layer_module = model.gpt_neox.layers[target_layer]
    layer_attn = layer_module.attention

    env_manifest = {
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": str(device),
        "model": model_name,
        "protocol_scope": cfg["protocol_scope"],
    }
    log(f"Environment manifest: {json.dumps(env_manifest)}", log_file)

    # -------------------------------------------------------------
    # 1. Multi-Vocabulary Support Set & B_agg (identical to EXP066)
    # -------------------------------------------------------------
    log(f"\n[1] Support set & B_agg at layer {target_layer} (d={d}) ...", log_file)
    support_vocabularies = {
        "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
        "V2_Biblical": ["Aaron", "Caleb", "Gideon", "Miriam", "Reuben"],
        "V3_Greek": ["Hector", "Jason", "Nestor", "Paris", "Priam"],
        "V4_Roman": ["Marcus", "Lucius", "Titus", "Felix", "Silas"],
        "V5_Modern": ["Liam", "Noah", "Sora", "Maya", "Leila"],
    }
    triples_indices = [
        (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
        (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
        (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    ]
    quads_indices = [
        (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
        (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
        (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    ]

    delta_h_by_vocab = {vk: [] for vk in support_vocabularies}
    for vk, ents in support_vocabularies.items():
        for i, (iA, iB, iC) in enumerate(triples_indices):
            A, B, C = ents[iA], ents[iB], ents[iC]
            q_opts = f"{A} or {C}" if (i % 2 == 0) else f"{C} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            with torch.no_grad():
                o_rel = model(input_ids=tokenizer.encode(p_rel, return_tensors="pt").to(device), output_hidden_states=True)
                o_neu = model(input_ids=tokenizer.encode(p_neu, return_tensors="pt").to(device), output_hidden_states=True)
            dh = o_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu() - o_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
            delta_h_by_vocab[vk].append(dh)
        for i, (iA, iB, iC, iD) in enumerate(quads_indices):
            A, B, C, D = ents[iA], ents[iB], ents[iC], ents[iD]
            q_opts = f"{A} or {D}" if (i % 2 == 0) else f"{D} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            with torch.no_grad():
                o_rel = model(input_ids=tokenizer.encode(p_rel, return_tensors="pt").to(device), output_hidden_states=True)
                o_neu = model(input_ids=tokenizer.encode(p_neu, return_tensors="pt").to(device), output_hidden_states=True)
            dh = o_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu() - o_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
            delta_h_by_vocab[vk].append(dh)
        delta_h_by_vocab[vk] = torch.stack(delta_h_by_vocab[vk])  # [30, d]

    v_hat_by_vocab = {}
    for vk, dH in delta_h_by_vocab.items():
        norms = torch.norm(dH, dim=1, keepdim=True) + 1e-12
        mean_v = (dH / norms).mean(dim=0)
        v_hat_by_vocab[vk] = mean_v / (torch.norm(mean_v) + 1e-12)
    sum_v = torch.stack(list(v_hat_by_vocab.values())).sum(dim=0)
    B_agg = sum_v / (torch.norm(sum_v) + 1e-12)
    log(f"B_agg constructed across K=5 support vocabularies (dim={B_agg.shape[0]}, norm={torch.norm(B_agg):.4f}).", log_file)

    torch.manual_seed(B_PERP_SEED)
    r_orth = torch.randn(d)
    r_orth -= B_agg * torch.dot(B_agg, r_orth)
    r_orth /= torch.norm(r_orth)
    B_perp = r_orth
    torch.manual_seed(SEED_TORCH)  # restore protocol seed

    p_wrong_rel = "Fact: Paris is the capital of France. Question: What is the capital of France, Paris or London? Answer:"
    p_wrong_neu = "Fact: Paris is near London. Question: What is the capital of France, Paris or London? Answer:"
    with torch.no_grad():
        out_wr_rel = model(input_ids=tokenizer.encode(p_wrong_rel, return_tensors="pt").to(device), output_hidden_states=True)
        out_wr_neu = model(input_ids=tokenizer.encode(p_wrong_neu, return_tensors="pt").to(device), output_hidden_states=True)
    dH_wrong = out_wr_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu() - out_wr_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
    B_wrong = dH_wrong / (torch.norm(dH_wrong) + 1e-12)
    log("B_perp (seed 9876) and B_wrong (Paris-capital contrast) constructed.", log_file)

    # -------------------------------------------------------------
    # 2. Stage A: per-head OV-subspace Procrustes (protocol §3)
    # -------------------------------------------------------------
    log("\n" + "=" * 80, log_file)
    log("[2] STAGE A: PER-HEAD OV-SUBSPACE PROCRUSTES (protocol §3)", log_file)
    log("=" * 80, log_file)

    # --- 2a. Orthonormal head-subspace bases Q_h (thin QR of W_O blocks; deterministic)
    W_dense = layer_attn.dense.weight.detach().cpu()  # [d, d]
    Q_heads = {}
    for h in range(n_heads):
        Wb = W_dense[:, h * head_dim:(h + 1) * head_dim]  # [d, 64] = W_O^{(h)}
        Qh, _ = torch.linalg.qr(Wb, mode="reduced")       # [d, 64]
        Q_heads[h] = Qh
    log(f"Q_h bases built for {n_heads} heads via thin QR (each [d,64], orthonormal).", log_file)

    # --- 2b. Anchor collection: 5 support vocabs x 5 entities x 16 templates = 400 prompts
    log("[2b] Collecting anchor head-outputs (400 support prompts) ...", log_file)
    anchor_prompts, anchor_meta = [], []
    for vk, ents in support_vocabularies.items():
        for e in ents:
            for tj, tmpl in enumerate(ANCHOR_TEMPLATES):
                anchor_prompts.append(tmpl.format(e=e))
                anchor_meta.append((vk, e, tj))
    anchor_o = collect_head_outputs(model, tokenizer, layer_attn, anchor_prompts,
                                    n_heads, head_dim, device, log_file)  # [400, H, d]
    # subspace coordinates: A_sub[vk] -> [80, H, 64]
    A_sub = {}
    for vk in support_vocabularies:
        idx = [i for i, m in enumerate(anchor_meta) if m[0] == vk]
        assert len(idx) == N_ANCHOR_ENTITIES * N_ANCHOR_TEMPLATES == 80, f"{vk}: {len(idx)} anchors != 80"
        per_head = []
        for h in range(n_heads):
            per_head.append(anchor_o[idx][:, h, :] @ Q_heads[h])  # [80, 64]
        A_sub[vk] = torch.stack(per_head, dim=1)  # [80, H, 64]
    log("Anchor subspace coordinates stacked: 80 pairs/vocab, m=80 >= d_h=64 (D1 fix).", log_file)

    # --- 2c. Relational directions in head subspaces: v_tilde_k^{(h)} = Q_h^T v_hat_k
    v_tilde = {}
    for vk, vhat in v_hat_by_vocab.items():
        v_tilde[vk] = torch.stack([Q_heads[h].T @ vhat for h in range(n_heads)], dim=0)  # [H, 64]

    # --- 2d. Fit R_tilde_h^{(1->k)} for k=2..5, guards, alignment gain g_h
    log("[2d] Fitting per-head subspace Procrustes (V1 -> Vk, k=2..5) with runtime guards ...", log_file)
    vocab_keys = list(support_vocabularies.keys())  # [V1..V5]
    stage_A_heads = []
    guard_abort = None
    for h in range(n_heads):
        gains = []
        fits_ok = True
        gap_min = float("inf")
        for k in range(1, 5):
            vk = vocab_keys[k]
            R_t, rank, gap, S = fit_subspace_procrustes(A_sub["V1_Anglo"][:, h, :], A_sub[vk][:, h, :])
            if rank != head_dim or gap <= RANK_TOL_GAP:
                fits_ok = False
                guard_abort = (h, vk, rank, gap)
                break
            gap_min = min(gap_min, gap)
            v1, vkh = v_tilde["V1_Anglo"][h], v_tilde[vk][h]
            # m1 fix (protocol §3.5 specifies TRUE cosines): v_tilde are NOT unit
            # vectors (||P_{S_h} v_hat|| <= 1), so raw dot products mislabel the
            # quantity. Normalizing cannot flip the halt/no-halt sign (||R_t v1||
            # == ||v1||, so sign(cos_al - cos_raw) == sign(dot_al - dot_raw)),
            # but it fixes the top-K ranking and the diagnostics table.
            n1 = torch.norm(v1) + 1e-12
            nkh = torch.norm(vkh) + 1e-12
            cos_al = float((torch.dot(R_t @ v1, vkh) / (n1 * nkh)).item())
            cos_raw = float((torch.dot(v1, vkh) / (n1 * nkh)).item())
            gains.append(cos_al - cos_raw)
        if not fits_ok:
            break
        g_h = float(np.mean(gains))
        stage_A_heads.append({"head": h, "g_h": g_h,
                              "per_pair_gains": gains,
                              "rank": head_dim, "spectral_gap_min": gap_min})
        log(f"  head {h:>2}: g_h = {g_h:+.4f}", log_file)

    def save_halt(outcome, reason, extra):
        payload = {
            "experiment": "EXP067",
            "model": model_name,
            "protocol_scope": cfg["protocol_scope"],
            "outcome": outcome,
            "halt_reason": reason,
            "pre_hash": pre_hash,
            "post_hash": get_hash(model),
            "target_layer": target_layer,
            "hidden_dim": d,
            "num_heads": n_heads,
            "alpha": ALPHA,
            "stage_A_heads": stage_A_heads,
            "env_manifest": env_manifest,
        }
        payload.update(extra)
        with open(os.path.join(out_dir, "exp067_results.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        log("=" * 80, log_file)
        log(f"{outcome}: {reason}", log_file)
        log("THIS HALT IS THE REPORTABLE OUTCOME OF EXP067 (protocol §7.2).", log_file)
        log(f"Diagnostics written to {out_dir}/exp067_results.json", log_file)
        log("=" * 80, log_file)
        log_file.close()

    if guard_abort is not None:
        h, vk, rank, gap = guard_abort
        save_halt("HALT_STAGE_A",
                  f"rank/spectral guard violated: head {h}, pair V1->{vk}: rank={rank}, gap={gap:.2e} (protocol §3.3, §7.1 branch a)",
                  {"guard_violation": {"head": h, "pair": f"V1->{vk}", "rank": rank, "spectral_gap": gap}})
        print("STAGE A GATE HALTED (guard) — THIS IS THE RESULT. Download exp067_results.json and report it.")
        sys.exit(0)

    # --- 2e. Head selection H* = top K=4 heads with g_h > 0; Stage A gate
    passing = sorted([r for r in stage_A_heads if r["g_h"] > 0], key=lambda r: -r["g_h"])
    H_star = [r["head"] for r in passing[:K_HEADS]]
    log(f"[2e] Heads with g_h > 0: {len(passing)}/{n_heads}; H* = {H_star}", log_file)
    if len(H_star) == 0:
        save_halt("HALT_STAGE_A",
                  "no head satisfies g_h > 0 on held-out support pairs: A-anchor/A-uniform rejected on support data; "
                  "H1 untestable under this operationalization (protocol §3.5, §7.1 branch a)",
                  {})
        print("STAGE A GATE HALTED (no head with g_h > 0) — THIS IS THE RESULT. Download exp067_results.json and report it.")
        sys.exit(0)
    log(f"Stage A gate PASSED: |H*| = {len(H_star)}.", log_file)

    # --- 2f. Test-vocabulary anchors + per-domain rotations for h in H*
    test_vocabs = {
        "Planetary": ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"],
        "Elemental": ["Iron", "Gold", "Silver", "Bronze", "Steel"],
    }
    log("[2f] Collecting test-vocabulary anchors (160 prompts) ...", log_file)
    t_prompts, t_meta = [], []
    for dom, ents in test_vocabs.items():
        for e in ents:
            for tj, tmpl in enumerate(ANCHOR_TEMPLATES):
                t_prompts.append(tmpl.format(e=e))
                t_meta.append((dom, e, tj))
    t_o = collect_head_outputs(model, tokenizer, layer_attn, t_prompts,
                               n_heads, head_dim, device, log_file)  # [160, H, d]
    T_sub = {}
    for dom in test_vocabs:
        idx = [i for i, m in enumerate(t_meta) if m[0] == dom]
        assert len(idx) == 80, f"{dom}: {len(idx)} anchors != 80"
        per_head = [t_o[idx][:, h, :] @ Q_heads[h] for h in range(n_heads)]
        T_sub[dom] = torch.stack(per_head, dim=1)  # [80, H, 64]

    R_domain = {}  # R_domain[dom][h] = R_tilde_h^{(V1->dom)}
    for dom in test_vocabs:
        R_domain[dom] = {}
        for h in H_star:
            R_t, rank, gap, S = fit_subspace_procrustes(A_sub["V1_Anglo"][:, h, :], T_sub[dom][:, h, :])
            if rank != head_dim or gap <= RANK_TOL_GAP:
                save_halt("HALT_STAGE_A",
                          f"rank/spectral guard violated on test-vocab fit: head {h}, V1->{dom}: "
                          f"rank={rank}, gap={gap:.2e} (protocol §3.3, §7.1 branch a)",
                          {"guard_violation": {"head": h, "pair": f"V1->{dom}", "rank": rank, "spectral_gap": gap},
                           "H_star": H_star})
                print("STAGE A GATE HALTED (guard) — THIS IS THE RESULT. Download exp067_results.json and report it.")
                sys.exit(0)
            R_domain[dom][h] = R_t
            log(f"  V1->{dom} head {h}: rank={rank}, spectral_gap={gap:.2e}", log_file)

    # --- 2g. Law #13 vector archiving (T-1 lesson: persist everything needed to
    #        recompute ||P_S v_hat_k|| and re-derive any Stage A quantity)
    archive = {
        "Q_heads": {h: Q_heads[h] for h in range(n_heads)},
        "A_sub": A_sub,                       # [80, H, 64] per support vocab
        "T_sub": T_sub,                       # [80, H, 64] per test vocab
        "v_hat_by_vocab": v_hat_by_vocab,     # [d] per support vocab
        "v_tilde": v_tilde,                   # [H, 64] per support vocab
        "B_agg": B_agg, "B_perp": B_perp, "B_wrong": B_wrong,
        "R_domain": R_domain,                 # fitted rotations, h in H*
        "H_star": H_star,
        "stage_A_heads": stage_A_heads,
        "anchor_meta": anchor_meta,
        "test_anchor_meta": t_meta,
    }
    torch.save(archive, os.path.join(out_dir, "exp067_vectors.pt"))
    log("Vector archive written: exp067_vectors.pt (Law #13).", log_file)

    # -------------------------------------------------------------
    # 3. Benchmark Construction (N=60, identical items to EXP065/066)
    # -------------------------------------------------------------
    log("\n" + "=" * 80, log_file)
    log("[3] BENCHMARK SPECIFICATION (N=60, ported verbatim from EXP066)", log_file)
    log("=" * 80, log_file)

    novel_vocab_planet = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
    novel_vocab_element = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
    test_instances = []

    for i, (iA, iB, iC) in enumerate(triples_indices):
        A, B, C = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        test_instances.append({"id": f"exp067_planet_2hop_{i}", "hop": 2, "domain": "Planetary",
                               "prompt": p, "target": A, "foil": C,
                               "target_token": " " + A, "foil_token": " " + C})
    for i, (iA, iB, iC, iD) in enumerate(quads_indices):
        A, B, C, D = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC], novel_vocab_planet[iD]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        test_instances.append({"id": f"exp067_planet_3hop_{i}", "hop": 3, "domain": "Planetary",
                               "prompt": p, "target": A, "foil": D,
                               "target_token": " " + A, "foil_token": " " + D})
    for i, (iA, iB, iC) in enumerate(triples_indices):
        A, B, C = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        test_instances.append({"id": f"exp067_element_2hop_{i}", "hop": 2, "domain": "Elemental",
                               "prompt": p, "target": A, "foil": C,
                               "target_token": " " + A, "foil_token": " " + C})
    for i, (iA, iB, iC, iD) in enumerate(quads_indices):
        A, B, C, D = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC], novel_vocab_element[iD]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        test_instances.append({"id": f"exp067_element_3hop_{i}", "hop": 3, "domain": "Elemental",
                               "prompt": p, "target": A, "foil": D,
                               "target_token": " " + A, "foil_token": " " + D})
    assert len(test_instances) == 60, f"Expected 60 test instances, got {len(test_instances)}"
    log(f"Benchmark: {len(test_instances)} instances (Planetary/Elemental x 2-hop/3-hop).", log_file)

    # -------------------------------------------------------------
    # 4. Baseline Evaluation & Headroom Gate (protocol §5)
    # -------------------------------------------------------------
    log("\n" + "=" * 80, log_file)
    log("[4] BASELINE EVALUATION & HEADROOM GATE", log_file)
    log("=" * 80, log_file)

    base_correct_list, base_logits_diff = [], []
    for item in test_instances:
        inp_ids = tokenizer.encode(item["prompt"], return_tensors="pt").to(device)
        t_tok = tokenizer.encode(item["target_token"])[0]
        f_tok = tokenizer.encode(item["foil_token"])[0]
        with torch.no_grad():
            out = model(input_ids=inp_ids)
        t_l = float(out.logits[0, -1, t_tok].item())
        f_l = float(out.logits[0, -1, f_tok].item())
        base_correct_list.append(bool(t_l > f_l))
        base_logits_diff.append(t_l - f_l)

    base_acc = float(np.mean(base_correct_list))
    num_correct = sum(base_correct_list)
    num_errors = len(test_instances) - num_correct
    log(f"Baseline Accuracy: {base_acc*100:.2f}% ({num_correct}/60 correct, {num_errors} errors available).", log_file)
    if not (HEADROOM_LO <= base_acc <= HEADROOM_HI):
        save_halt("HALT_HEADROOM",
                  f"baseline accuracy {base_acc*100:.2f}% outside pre-registered 40%-70% window: "
                  f"benchmark miscalibrated; recalibration requires a new pre-registration (protocol §5, §7.2)",
                  {"baseline_accuracy": base_acc, "H_star": H_star})
        print("HEADROOM GATE HALTED — THIS IS THE RESULT (benchmark miscalibrated). Download exp067_results.json and report it.")
        sys.exit(0)
    log("HEADROOM GATE PASSED: baseline within pre-registered [40%, 70%] window.", log_file)

    # -------------------------------------------------------------
    # 5. Stage B: 7 mandated conditions (protocol §4)
    # -------------------------------------------------------------
    log("\n" + "=" * 80, log_file)
    log("[5] STAGE B: 7 MANDATED CONDITIONS", log_file)
    log("=" * 80, log_file)

    I64 = torch.eye(head_dim)

    def head_projected_sum(basis_vec, R_by_head):
        """alpha * sum_{h in H*} Q_h (R_h - I) Q_h^T basis ; delta form.

        Valid ONLY for rotated conditions (C3/C5/C6/C7). The static C2 control
        is computed DIRECTLY below as alpha*sum Q_h Q_h^T b (protocol §3.4);
        it must NOT go through this delta form (with R=None it would compute
        alpha*sum Q_h (I-I) Q_h^T b = 0 -- the F1 silent-zero bug)."""
        total = torch.zeros(d)
        qb = {h: Q_heads[h].T @ basis_vec for h in H_star}  # [64] each
        for h in H_star:
            Rh = R_by_head[h]
            total += Q_heads[h] @ ((Rh - I64) @ qb[h])
        return ALPHA * total

    # Precompute intervention vectors. C2 is the DIRECT head-projection of the
    # static basis (protocol §3.4: C2 = alpha * sum_{h in H*} Q_h Q_h^T B_agg) --
    # NOT the delta form (F1 fix: the delta form with R=None is identically 0).
    C2_vec = ALPHA * sum(Q_heads[h] @ (Q_heads[h].T @ B_agg) for h in H_star)
    C3_vec = {dom: head_projected_sum(B_agg, R_domain[dom]) for dom in test_vocabs}
    C6_vec = {dom: head_projected_sum(B_perp, R_domain[dom]) for dom in test_vocabs}
    C7_vec = {dom: head_projected_sum(B_wrong, R_domain[dom]) for dom in test_vocabs}

    # ---- F1 GUARD (Law #14): a silent-zero control must be IMPOSSIBLE, not
    #      merely fixed. Before this fix, C2 was computed through the delta
    #      form with R=None -> alpha*sum Q_h (I64-I64) Q_h^T B_agg = 0, a
    #      silent no-op that would have corrupted the E-5 C2-vs-C3 contrast.
    #      Every condition's injection vector is asserted non-degenerate here,
    #      and the norms are persisted to results.json for audit.
    injection_norms = {"C2_Static_HeadProjected": float(torch.norm(C2_vec).item())}
    for dom, _v in C3_vec.items():
        injection_norms[f"C3_Aligned_Dynamic_Basis[{dom}]"] = float(torch.norm(_v).item())
    for dom, _v in C6_vec.items():
        injection_norms[f"C6_Dynamic_B_perp[{dom}]"] = float(torch.norm(_v).item())
    for dom, _v in C7_vec.items():
        injection_norms[f"C7_Dynamic_B_wrong[{dom}]"] = float(torch.norm(_v).item())
    for _k, _n in injection_norms.items():
        assert _n > 0, (f"FATAL (F1 guard): injection vector {_k} has zero norm -- "
                        f"the control would be a silent no-op. Aborting.")
    log(f"C2/C3/C6/C7 vectors precomputed over H*={H_star} (alpha={ALPHA}).", log_file)
    log(f"Injection-vector norms (F1 guard, all > 0): {json.dumps(injection_norms)}", log_file)

    def make_bridge_vec(tt, ft):
        # Mechanical fix (LOG-114 class): transformers 5.x renamed
        # GPTNeoXForCausalLM.embed_out to lm_head; get_output_embeddings() is
        # version-agnostic (4.44+ and 5.x) and returns the same matrix
        # (verified: identical to lm_head.weight). Zero scientific change.
        out_emb = model.get_output_embeddings().weight
        w = out_emb[tt, :].detach() - out_emb[ft, :].detach()
        return w / (torch.norm(w) + 1e-12)

    instance_records = {item["id"]: {"prompt": item["prompt"], "domain": item["domain"],
                                     "base_correct": base_correct_list[i]}
                        for i, item in enumerate(test_instances)}

    def eval_test_condition(cond_name, vector_fn):
        mod_correct, d_logits_t, d_logits_f, d_H_list = [], [], [], []
        kl_list, top10_overlaps, margin_shifts = [], [], []
        for idx, item in enumerate(test_instances):
            p_text = item["prompt"]
            t_tok = tokenizer.encode(item["target_token"])[0]
            f_tok = tokenizer.encode(item["foil_token"])[0]
            inp_ids = tokenizer.encode(p_text, return_tensors="pt").to(device)
            with torch.no_grad():
                out_b = model(input_ids=inp_ids, output_hidden_states=True)
            l_b = out_b.logits[0, -1, :]
            probs_b = F.softmax(l_b, dim=-1)
            t_l_b = float(l_b[t_tok].item()); f_l_b = float(l_b[f_tok].item())
            top10_b = set(torch.topk(l_b, k=10).indices.tolist())
            h_b = out_b.hidden_states[target_layer + 1][0, -1, :].detach().cpu()

            v_vec = vector_fn(item, t_tok, f_tok).to(device).view(1, 1, -1)

            if idx == 0:
                # F1 guard, per-instance arm: no condition may inject a zero
                # vector silently (covers C4's per-instance bridge vectors).
                _vn = float(torch.norm(v_vec).item())
                assert _vn > 0, (f"FATAL (F1 guard): {cond_name} injection vector is "
                                 f"zero on instance {item['id']} -- silent no-op. Aborting.")
                log(f"  {cond_name}: first-instance injection norm = {_vn:.6f} (non-degenerate).", log_file)

            # All intervention vectors are pre-scaled by ALPHA (C2 via direct head
            # projection, C3/C5/C6/C7 via head_projected_sum delta form, C4 via
            # _c4_fn below), so the hook adds v_vec as-is.
            def hook_fn(module, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                h_mod = h + v_vec
                if isinstance(outp, tuple):
                    return (h_mod,) + outp[1:]
                return h_mod

            handle = layer_module.register_forward_hook(hook_fn)
            with torch.no_grad():
                out_m = model(input_ids=inp_ids, output_hidden_states=True)
            handle.remove()

            l_m = out_m.logits[0, -1, :]
            probs_m = F.softmax(l_m, dim=-1)
            t_l_m = float(l_m[t_tok].item()); f_l_m = float(l_m[f_tok].item())
            top10_m = set(torch.topk(l_m, k=10).indices.tolist())
            h_m = out_m.hidden_states[target_layer + 1][0, -1, :].detach().cpu()

            is_mod_corr = bool(t_l_m > f_l_m)
            mod_correct.append(is_mod_corr)
            d_logits_t.append(t_l_m - t_l_b); d_logits_f.append(f_l_m - f_l_b)
            margin_shift = (t_l_m - f_l_m) - (t_l_b - f_l_b)
            margin_shifts.append(margin_shift)
            d_H_list.append(float(torch.norm(h_m - h_b).item()))
            kl_i = compute_kl(probs_b, probs_m)  # m2: per-instance KL (protocol §8)
            kl_list.append(kl_i)
            top10_overlaps.append(len(top10_b.intersection(top10_m)) / 10.0)
            instance_records[item["id"]][f"{cond_name}_correct"] = is_mod_corr
            instance_records[item["id"]][f"{cond_name}_margin_shift"] = margin_shift
            instance_records[item["id"]][f"{cond_name}_kl_div"] = float(kl_i)

        b, c, delta_m, p_val = compute_paired_stats(base_correct_list, mod_correct)
        wilc_p = float(stats.wilcoxon(margin_shifts).pvalue) if any(m != 0 for m in margin_shifts) else 1.0
        return {
            "name": cond_name,
            "acc_base": base_acc,
            "acc_mod": float(np.mean(mod_correct)),
            "delta_m": float(delta_m),
            "rescues_b": b, "corruptions_c": c,
            "exact_p": float(p_val),
            "wilcoxon_p": wilc_p,  # exploratory only (audit Finding 3)
            "delta_logit_target": float(np.mean(d_logits_t)),
            "delta_logit_foil": float(np.mean(d_logits_f)),
            "delta_margin": float(np.mean(margin_shifts)),
            "delta_H": float(np.mean(d_H_list)),
            "kl_div": float(np.mean(kl_list)),
            "top10_overlap": float(np.mean(top10_overlaps)),
        }

    stage_B_results = {}
    # C1: unintervened baseline (defined statistics; no forward passes needed)
    stage_B_results["C1_Unintervened_Baseline"] = {
        "name": "C1_Unintervened_Baseline", "acc_base": base_acc, "acc_mod": base_acc,
        "delta_m": 0.0, "rescues_b": 0, "corruptions_c": 0, "exact_p": 1.0,
        "wilcoxon_p": 1.0, "delta_logit_target": 0.0, "delta_logit_foil": 0.0,
        "delta_margin": 0.0, "delta_H": 0.0, "kl_div": 0.0, "top10_overlap": 1.0,
    }
    log("C1 recorded (unintervened baseline).", log_file)

    log("Evaluating C2: Static Basis (head-projected, protocol §3.4) ...", log_file)
    stage_B_results["C2_Static_HeadProjected"] = eval_test_condition(
        "C2_Static_HeadProjected", lambda item, tt, ft: C2_vec)

    log("Evaluating C3: Aligned Dynamic Basis (PRIMARY TEST CONDITION) ...", log_file)
    stage_B_results["C3_Aligned_Dynamic_Basis"] = eval_test_condition(
        "C3_Aligned_Dynamic_Basis", lambda item, tt, ft: C3_vec[item["domain"]])

    log("Evaluating C4: Same-Layer Output Bridge (positive control) ...", log_file)
    # C4 follows the EXP066 convention: the bridge vector is pre-scaled by ALPHA
    # here so the hook (which adds v_vec as-is) stays uniform across conditions.
    def _c4_fn(item, tt, ft):
        return ALPHA * make_bridge_vec(tt, ft)
    stage_B_results["C4_Output_Bridge"] = eval_test_condition("C4_Output_Bridge", _c4_fn)

    log("Evaluating C5: Random Rotations x5 seeds (Haar O(64)) ...", log_file)
    rand_rot_runs = []
    for s_idx, seed_val in enumerate(C5_SEEDS):
        torch.manual_seed(seed_val)
        R_rand = {}
        for h in H_star:
            M_r = torch.randn(head_dim, head_dim)
            U_r, _, Vh_r = torch.linalg.svd(M_r)
            R_rand[h] = U_r @ Vh_r  # Haar(O(64)) via QR/SVD of Gaussian
        v_rand = head_projected_sum(B_agg, R_rand)
        _rn = float(torch.norm(v_rand).item())
        assert _rn > 0, (f"FATAL (F1 guard): C5 seed {s_idx} vector is zero -- silent no-op. Aborting.")
        injection_norms[f"C5_Random_Rotation_Seed_{s_idx}"] = _rn
        run_res = eval_test_condition(f"C5_Random_Rotation_Seed_{s_idx}",
                                      lambda item, tt, ft, _v=v_rand: _v)
        rand_rot_runs.append(run_res)
    torch.manual_seed(SEED_TORCH)
    stage_B_results["C5_Random_Rotation_Control"] = {
        "name": "C5_Random_Rotation_Control (5-Seed Mean)",
        "acc_base": base_acc,
        "acc_mod": float(np.mean([r["acc_mod"] for r in rand_rot_runs])),
        "delta_m": float(np.mean([r["delta_m"] for r in rand_rot_runs])),
        "rescues_b": float(np.mean([r["rescues_b"] for r in rand_rot_runs])),
        "corruptions_c": float(np.mean([r["corruptions_c"] for r in rand_rot_runs])),
        "exact_p": 1.0,
        "delta_logit_target": float(np.mean([r["delta_logit_target"] for r in rand_rot_runs])),
        "delta_logit_foil": float(np.mean([r["delta_logit_foil"] for r in rand_rot_runs])),
        "delta_margin": float(np.mean([r["delta_margin"] for r in rand_rot_runs])),
        "delta_H": float(np.mean([r["delta_H"] for r in rand_rot_runs])),
        "kl_div": float(np.mean([r["kl_div"] for r in rand_rot_runs])),
        "top10_overlap": float(np.mean([r["top10_overlap"] for r in rand_rot_runs])),
    }

    log("Evaluating C6: Dynamic B_perp ...", log_file)
    stage_B_results["C6_Dynamic_B_perp"] = eval_test_condition(
        "C6_Dynamic_B_perp", lambda item, tt, ft: C6_vec[item["domain"]])

    log("Evaluating C7: Dynamic B_wrong ...", log_file)
    stage_B_results["C7_Dynamic_B_wrong"] = eval_test_condition(
        "C7_Dynamic_B_wrong", lambda item, tt, ft: C7_vec[item["domain"]])

    # -------------------------------------------------------------
    # 6. Results ledger, SHA-256 post guard, artifacts
    # -------------------------------------------------------------
    log("\n" + "=" * 80, log_file)
    log("[6] STAGE B RESULTS LEDGER (EXP067)", log_file)
    log("=" * 80, log_file)
    log(f"{'Condition':<32} | {'Acc(Mod)':<8} | {'Delta_M':<9} | {'b (Res)':<7} | {'c (Cor)':<7} | {'p-value':<8} | {'KL':<7}", log_file)
    log("-" * 100, log_file)
    for c_key, res in stage_B_results.items():
        log(f"{res['name']:<32} | {res['acc_mod']*100:>6.2f}% | {res['delta_m']*100:>+7.2f}% | "
            f"{res['rescues_b']:>7} | {res['corruptions_c']:>7} | {res['exact_p']:>8.4f} | {res['kl_div']:>7.4f}", log_file)

    post_hash = get_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}", log_file)
    assert pre_hash == post_hash, "CRITICAL: Backbone parameter drift detected! Delta theta != 0."
    log("CONSTITUTIONAL COMPLIANCE CONFIRMED: Delta theta == 0 (binding pre/post match).", log_file)

    results_payload = {
        "experiment": "EXP067",
        "model": model_name,
        "protocol_scope": cfg["protocol_scope"],
        "outcome": "COMPLETED",
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "target_layer": target_layer,
        "hidden_dim": d,
        "num_heads": n_heads,
        "alpha": ALPHA,
        "seeds": {"torch": SEED_TORCH, "numpy": SEED_NUMPY, "C5": C5_SEEDS, "B_perp": B_PERP_SEED},
        "baseline_accuracy": base_acc,
        "errors_available": num_errors,
        "H_star": H_star,
        "stage_A_heads": stage_A_heads,
        "injection_vector_norms": injection_norms,  # F1 guard: all asserted > 0
        "stage_B_conditions": stage_B_results,
        "env_manifest": env_manifest,
    }
    res_json_path = os.path.join(out_dir, "exp067_results.json")
    with open(res_json_path, "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)
    inst_json_path = os.path.join(out_dir, "exp067_instance_records.json")
    with open(inst_json_path, "w", encoding="utf-8") as f:
        json.dump(instance_records, f, indent=2)

    log(f"\nArtifacts saved to:\n  {res_json_path}\n  {inst_json_path}\n"
        f"  {os.path.join(out_dir, 'exp067_vectors.pt')} (Law #13 archive)\n  {log_path}", log_file)
    log("Run evaluate_exp067.py on exp067_results.json for the pre-registered decision-tree ruling.", log_file)
    log_file.close()
    print("EXP067 COMPLETED. Now run: python experiments/runs/exp067/evaluate_exp067.py")


if __name__ == "__main__":
    main()
