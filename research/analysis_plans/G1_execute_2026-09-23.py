#!/usr/bin/env python3
"""G1 Phase-2 execution (LOG-134) — weight-only QK/OV projection-energy audit.

Frozen plan: research/analysis_plans/G1_PLAN.md (re-frozen after LOG-137 review).
Binding: CPU-only, torch.float32 explicit, local_files_only, read-only weights,
ZERO forward passes, hash verified before any computation.

Head-row layout (verified 2026-09-23 against the INSTALLED transformers 5.x
GPTNeoXAttention source: view(batch,seq,-1,3*dh).transpose(1,2).chunk(3,-1)):
  qkv_w rows [192h:192h+64]   = W_Q^h
  qkv_w rows [192h+64:192h+128] = W_K^h
  qkv_w rows [192h+128:192h+192] = W_V^h
  dense_w cols [64h:64h+64]    = W_O^h   (attn_output.reshape(batch,seq,-1) -> dense)
NOTE: this is the per-head INTERLEAVED layout (stride 192), not the blocked
[Q|K|V] layout. The plan delegated layout verification to the executor (§2);
this is that verification, executed against modeling source, documented here.
"""
import importlib.util
import json
import subprocess
import textwrap
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# ---------------- pinned configuration (Law #13) ----------------
SEED_RHO = 20260923
SEED_S = 20260924
MODEL_ID = "EleutherAI/pythia-410m"
SNAP = "/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
ARCHIVE = "experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt"
LAYERS = [21, 22, 23]
N_HEADS = 16
D = 1024
DH = 64
T0 = time.time()

torch.manual_seed(0)  # global default only; all stochastic draws use dedicated generators

# ---------------- 1. archived vectors (read-only) ----------------
arc = torch.load(ARCHIVE, map_location="cpu", weights_only=False)
ARCH_PRE = arc["pre_hash"]
assert ARCH_PRE == arc["post_hash"], "archived pre/post hash mismatch (Delta theta != 0 at archive)"

# ---------------- 2. model + tokenizer: read-only, float32, local ----------------
tok = AutoTokenizer.from_pretrained(SNAP, local_files_only=True, trust_remote_code=False)
model = AutoModelForCausalLM.from_pretrained(
    SNAP, local_files_only=True, trust_remote_code=False, torch_dtype=torch.float32)
model.eval()  # no forwards are run below; belt-and-braces
sd = model.state_dict()
assert sd["gpt_neox.embed_in.weight"].shape[1] == D

# ---------------- 3. Delta theta = 0: recompute runner's get_hash ----------------
spec = importlib.util.spec_from_file_location("run_exp077", "experiments/runs/exp077/run_exp077.py")
r77 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r77)  # module level is constants-only; main() guarded
live_hash = r77.get_hash(model)
assert live_hash == ARCH_PRE, f"HASH MISMATCH: live {live_hash[:16]} vs archived {ARCH_PRE[:16]}"
print(f"[hash] OK pre==post==live ({live_hash[:16]}...); Delta theta = 0", flush=True)

# ---------------- 4. per-head weight extraction (layout verified, see header) ----------------
def head_mats(l):
    qkv = sd[f"gpt_neox.layers.{l}.attention.query_key_value.weight"].to(torch.float32)
    den = sd[f"gpt_neox.layers.{l}.attention.dense.weight"].to(torch.float32)
    assert qkv.shape == (3072, 1024), qkv.shape
    assert den.shape == (1024, 1024), den.shape
    out = []
    for h in range(N_HEADS):
        b = 3 * h * DH
        Wq = qkv[b:b + DH, :]
        Wk = qkv[b + DH:b + 2 * DH, :]
        Wv = qkv[b + 2 * DH:b + 3 * DH, :]
        Wo = den[:, h * DH:(h + 1) * DH]
        out.append((Wq, Wk, Wv, Wo))
    return out

def rowspace_basis(M):
    """Orthonormal row-space basis (k x d) of M (m x d) via thin SVD; returns (basis, rank)."""
    _, s, Vh = torch.linalg.svd(M, full_matrices=False)  # M = U S Vh
    tol = max(M.shape) * torch.finfo(torch.float32).eps * float(s[0])
    k = int((s > tol).sum().item())
    return Vh[:k, :], k

def colspace_basis(M):
    """Orthonormal column-space basis (d x k) of M (d x m) via thin SVD; returns (basis, rank)."""
    U, s, _ = torch.linalg.svd(M, full_matrices=False)  # M = U S Vh
    tol = max(M.shape) * torch.finfo(torch.float32).eps * float(s[0])
    k = int((s > tol).sum().item())
    return U[:, :k], k

# projectors per head: store the orthonormal bases (energy = ||B^T v|| / ||v||)
QK_B, QK_RANK, OV_B, OV_RANK, HEAD_IDX = [], [], [], [], []
for l in LAYERS:
    for h, (Wq, Wk, Wv, Wo) in enumerate(head_mats(l)):
        Bq, kq = rowspace_basis(torch.cat([Wq, Wk], dim=0))      # (k,1024)
        Bo, ko = colspace_basis(torch.cat([Wo, Wv.t()], dim=1))  # (1024,k)
        QK_B.append(Bq); QK_RANK.append(kq)
        OV_B.append(Bo); OV_RANK.append(ko)
        HEAD_IDX.append((l, h))
N48 = len(HEAD_IDX)
assert N48 == 48
print(f"[heads] 48 projectors built; QK ranks: min={min(QK_RANK)} max={max(QK_RANK)}; "
      f"OV ranks: min={min(OV_RANK)} max={max(OV_RANK)}", flush=True)

def energies(v):
    """e_QK and e_OV per head for a vector v (1024,)."""
    v = v.to(torch.float32)
    n = float(torch.norm(v).item())
    assert n > 0
    eq = [float(torch.norm(B @ v).item()) / n for B in QK_B]
    eo = [float(torch.norm(B.t() @ v).item()) / n for B in OV_B]
    return eq, eo

# ---------------- 5. vector set ----------------
V = {
    "B_agg": arc["v_hat"].to(torch.float32),
    "B_perp": arc["B_perp_basis"].to(torch.float32),
    "B_wrong": arc["B_wrong"].to(torch.float32),
}
for k in range(5):
    V[f"vhat_{k+1}"] = arc["v_hats"][k].to(torch.float32)
DIAG = {
    "v_hat_c": arc["v_hat_c"].to(torch.float32),
    "mu": arc["mu"].to(torch.float32),
    "r_vec": arc["r_vec"].to(torch.float32),
}
for j in range(8):
    DIAG[f"u_{j+1}"] = arc["u_list"][j].to(torch.float32)
    DIAG[f"q_{j+1}"] = arc["q_list"][j].to(torch.float32)

# ---------------- 6. bench rebuild: VERBATIM code path (run_exp077.py ll. 591-638) ----------------
src_lines = open("experiments/runs/exp077/run_exp077.py").read().splitlines()
seg = textwrap.dedent("\n".join(src_lines[590:638]))  # 1-based 591..638: bench=[] .. assert
ns = dict(vars(r77))
ns["log"] = lambda *a, **k: None
ns["log_file"] = None
exec(compile(seg, "bench_block_ll591_638", "exec"), ns)
bench = ns["bench"]
assert len(bench) == 60 and bench[0]["id"] == "exp077_planet_2hop_0"
print("[bench] rebuilt verbatim: 60 items, first id:", bench[0]["id"], flush=True)

# ---------------- 7. bridge mean (make_bridge_vec, run_exp077.py ll. 725-729, verbatim formula) ----------------
E = model.get_output_embeddings().weight.detach().cpu().to(torch.float32)
VSZ = E.shape[0]
t_ids, f_ids, b_list = [], [], []
for it in bench:
    t = tok.encode(" " + it["A"])[0]
    f = tok.encode(" " + it["C"])[0]
    t_ids.append(t); f_ids.append(f)
    w = E[t, :] - E[f, :]
    n = float(torch.norm(w).item())
    assert n > 0, "F1 guard: zero-norm bridge direction"
    b_list.append(w / n)
b_mean = sum(b_list) / torch.norm(sum(b_list))
V["b_mean"] = b_mean
excluded_ids = set(t_ids) | set(f_ids)
print(f"[bridge] 60 per-item bridges; b_mean norm=1; excluded token ids: {len(excluded_ids)}", flush=True)

# ---------------- 8. companion steering controls s_j (token-id-level exclusion) ----------------
gen_s = torch.Generator().manual_seed(SEED_S)
pairs = []
while len(pairs) < 20:
    a = int(torch.randint(0, VSZ, (1,), generator=gen_s).item())
    b = int(torch.randint(0, VSZ, (1,), generator=gen_s).item())
    if a != b and a not in excluded_ids and b not in excluded_ids:
        pairs.append((a, b))
for j, (a, b) in enumerate(pairs):
    w = E[a, :] - E[b, :]
    V[f"s_{j+1}"] = w / torch.norm(w)
V["s_bar"] = sum(V[f"s_{j+1}"] for j in range(20))
V["s_bar"] = V["s_bar"] / torch.norm(V["s_bar"])

# ---------------- 9. random-rho null ----------------
gen_r = torch.Generator().manual_seed(SEED_RHO)
G = torch.randn(100, D, generator=gen_r)
RHOS = [G[j] / torch.norm(G[j]) for j in range(100)]

# ---------------- 10. energies for everything ----------------
E_QK, E_OV = {}, {}
for name, v in list(V.items()) + list(DIAG.items()):
    eq, eo = energies(v)
    E_QK[name], E_OV[name] = eq, eo
RHO_QK = [energies(r)[0] for r in RHOS]
RHO_OV = [energies(r)[1] for r in RHOS]

def agg(per_head):
    return float(sum(per_head) / len(per_head))

A_QK, A_OV = {}, {}
for name in E_QK:
    A_QK[name] = agg(E_QK[name])
    A_OV[name] = agg(E_OV[name])
S_QK = sorted(agg(rq) for rq in RHO_QK)
S_OV = sorted(agg(ro) for ro in RHO_OV)
q05_qk, q95_qk = S_QK[4], S_QK[94]
q05_ov, q95_ov = S_OV[4], S_OV[94]

def p_low(S, x):
    return (1 + sum(1 for s in S if s <= x)) / 101.0

def p_high(S, x):
    return (1 + sum(1 for s in S if s >= x)) / 101.0

A = A_QK["B_agg"]; B = A_QK["b_mean"]
# ---------------- 11. decision (exhaustive partition, plan §7) ----------------
if A >= B:
    verdict = "KILL"
elif A < q05_qk and B > q95_qk:
    verdict = "CONSISTENT"
else:
    verdict = "INCONCLUSIVE"
s_med = float(np_median := __import__("numpy").median([A_QK[f"s_{j+1}"] for j in range(20)]))
s_bar_e = A_QK["s_bar"]
design_obj_rejected = bool(s_med >= B or s_bar_e >= B)

# ---------------- 12. sensitivity diagnostics (non-decision) ----------------
# (b) include layer-20 heads
QK20, OV20 = [], []
for h, (Wq, Wk, Wv, Wo) in enumerate(head_mats(20)):
    Bq, _ = rowspace_basis(torch.cat([Wq, Wk], dim=0))
    Bo, _ = colspace_basis(torch.cat([Wo, Wv.t()], dim=1))
    QK20.append(Bq); OV20.append(Bo)
def agg64(name):
    v = V[name].to(torch.float32); n = float(torch.norm(v).item())
    eq = [float(torch.norm(Bb @ v).item()) / n for Bb in QK_B + QK20]
    return float(sum(eq) / len(eq))
sens_layer20 = {name: agg64(name) for name in ["B_agg", "b_mean"]}
# (c) max-head energies
maxhead = {name: (max(E_QK[name]), max(E_OV[name])) for name in V}
# MLP exploratory: rowspace of dense_h_to_4h for layers 21-23
MLP = {}
for name in ["B_agg", "b_mean", "B_perp", "B_wrong", "s_bar"]:
    v = V[name].to(torch.float32); n = float(torch.norm(v).item()); es = []
    for l in LAYERS:
        Wup = sd[f"gpt_neox.layers.{l}.mlp.dense_h_to_4h.weight"].to(torch.float32)
        assert Wup.shape == (4096, 1024)
        Bu, _ = rowspace_basis(Wup)
        es.append(float(torch.norm(Bu @ v).item()) / n)
    MLP[name] = float(sum(es) / len(es))

# ---------------- 13. per-head foreground table ----------------
per_head = []
for i, (l, h) in enumerate(HEAD_IDX):
    per_head.append({
        "layer": l, "head": h,
        "qk_rank": QK_RANK[i], "ov_rank": OV_RANK[i],
        "e_qk_B_agg": E_QK["B_agg"][i], "e_qk_b_mean": E_QK["b_mean"][i],
        "e_ov_B_agg": E_OV["B_agg"][i], "e_ov_b_mean": E_OV["b_mean"][i],
    })
top8 = sorted(range(48), key=lambda i: E_QK["b_mean"][i], reverse=True)[:8]

# ---------------- 14. manifest + JSON ----------------
def pf(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception:
        return "n/a"

manifest = {
    "torch_version": torch.__version__,
    "transformers_version": __import__("transformers").__version__,
    "numpy_version": __import__("numpy").__version__,
    "python": pf(["python3", "--version"]) or sys.version.split()[0],
    "venv": "/home/hatch/workspace/.venv_smoke/bin/python",
    "model_snapshot": SNAP,
    "model_hash_live": live_hash,
    "model_hash_archived": ARCH_PRE,
    "hash_match": True,
    "torch_dtype": "torch.float32 (explicit)",
    "forward_passes": 0,
    "seeds": {"rho_null": SEED_RHO, "s_companion": SEED_S},
    "head_layout": "interleaved stride-192 (verified vs installed transformers 5.x GPTNeoXAttention source)",
    "elapsed_s": round(time.time() - T0, 1),
}
res = {
    "log": "LOG-134", "plan": "research/analysis_plans/G1_PLAN.md (re-frozen, LOG-137 CLEAR-WITH-FIXES)",
    "manifest": manifest,
    "endpoint": {"A_barE_QK_B_agg": A, "B_barE_QK_b_mean": B},
    "null_QK": {"q05": q05_qk, "q95": q95_qk, "mean": float(sum(S_QK) / 100),
                "sample": S_QK},
    "null_OV": {"q05": q05_ov, "q95": q95_ov, "mean": float(sum(S_OV) / 100),
                "sample": S_OV},
    "p_values": {
        "QK": {"p_low_B_agg": p_low(S_QK, A), "p_high_b_mean": p_high(S_QK, B)},
        "OV": {"p_low_B_agg": p_low(S_OV, A_OV["B_agg"]),
               "p_high_b_mean": p_high(S_OV, A_OV["b_mean"])},
    },
    "verdict": verdict,
    "near_null_space_conjuncts": {"B_agg_below_q05": bool(A < q05_qk),
                                  "bridge_above_q95": bool(B > q95_qk)},
    "kill_fired": bool(A >= B),
    "aggregates_QK": {k: A_QK[k] for k in sorted(A_QK)},
    "aggregates_OV": {k: A_OV[k] for k in sorted(A_OV)},
    "companion_s": {
        "median_QK": s_med, "s_bar_QK": s_bar_e,
        "design_objective_rejected": design_obj_rejected,
        "individual_QK": [A_QK[f"s_{j+1}"] for j in range(20)],
    },
    "per_head": per_head,
    "top8_heads_by_e_qk_b_mean": [{"layer": HEAD_IDX[i][0], "head": HEAD_IDX[i][1],
                                   "e_qk_b_mean": E_QK["b_mean"][i],
                                   "e_qk_B_agg": E_QK["B_agg"][i]} for i in top8],
    "sensitivity_layer20_included": sens_layer20,
    "max_head_energies": {k: {"QK": v[0], "OV": v[1]} for k, v in maxhead.items()},
    "MLP_exploratory": MLP,
    "qk_ranks": QK_RANK, "ov_ranks": OV_RANK,
    "bridge": {"n_items": 60, "excluded_token_ids": len(excluded_ids)},
}
with open("research/analysis_plans/G1_RESULTS_2026-09-23.json", "w") as f:
    json.dump(res, f, indent=1)
print(f"[done] verdict={verdict} A={A:.6f} B={B:.6f} q05={q05_qk:.6f} q95={q95_qk:.6f} "
      f"elapsed={time.time()-T0:.0f}s", flush=True)
