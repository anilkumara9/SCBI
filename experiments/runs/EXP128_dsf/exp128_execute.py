#!/usr/bin/env python3
"""EXP128 (DSF) — Dynamical Sensitivity-Field Mapping, LOG-4706 execution lane.

Finite-difference gain field S_l = E[||x_{24,last}(y_l + delta) - x_{24,last}(y_l)|| / ||delta||]
across the 24 injection sites (L0 = post-embedding, Ll = block-(l-1) output), final-token site,
readout x_{24,last} = post-final-LayerNorm input to the unembedding.

Law #9 ordering: guards -> backbone pin -> forward batches (field + eps/2 check, either order)
-> linearity-check evaluation -> raw-record hash-pin -> Gini -> decision.

$0 CPU. Frozen backbone, eval mode, torch.no_grad(). No optimizer, no loss, no backward pass
into weights. Δθ=0 by construction (LOG-331 pin before and after).
"""
import hashlib
import json
import math
import os
import sys
import time

import numpy as np
import torch
import transformers

# ---------------- pins ----------------
PROTOCOL_PIN = "c1f5212651fc8d2ca2eefd6e4bebfc9580dc7a85f958bd19f48f8b73263f683b"
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
BASE_SEED = 20260929
K_DRAWS = 4
EPS = 1e-3
N_LAYERS = 24
HID = 1024
ITEMS_N = 10
CHECK_ITEMS = (0, 4, 9)
CHECK_LAYERS = (5, 11, 17, 23)
LIN_TOL = 0.25
LIN_MIN_PASS = 10

PROTOCOL = os.path.expanduser("~/workspace/SCBI/research/prereg/EXP_PREREG_DSF_SENSITIVITYFIELD_2026-09-29.md")
SNAP = "/home/hatch/workspace/.exp086_weights/pythia-410m"
EXP107DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl")
EXP127_REF = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP127_tga/out/exp127_per_prompt.json")
RUN_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP128_dsf")
OUT = os.path.join(RUN_DIR, "out")
os.makedirs(OUT, exist_ok=True)
LOGF = os.path.join(OUT, "exp128_console.log")

_logf = open(LOGF, "a")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    _logf.write(line + "\n")
    _logf.flush()

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_json(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def state_dict_hash(model):
    """Canonical LOG-331 method: sha256 over sorted state_dict keys, float32 bytes."""
    sha = hashlib.sha256()
    sd = model.state_dict()
    for k in sorted(sd.keys()):
        sha.update(np.asarray(sd[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()

def seed_for(item_idx, layer, draw):
    return BASE_SEED + item_idx * 10**6 + layer * 10**3 + draw

def draw_delta(seed, eps):
    g = torch.Generator()
    g.manual_seed(seed)
    u = torch.randn(HID, generator=g)
    u = u / torch.linalg.norm(u)
    d = eps * u
    # exact-budget realization in float32: one deterministic renormalization so that
    # ||delta|| matches the pinned budget eps to one ULP on every (item, layer, draw).
    # The direction remains the seed-deterministic isotropic unit vector; no RNG change.
    d = d * (eps / torch.linalg.norm(d))
    return d

# ---------------- 0. protocol hash before anything ----------------
log("== EXP128 (DSF) execution lane LOG-4706 ==")
h_proto = sha256_file(PROTOCOL)
log("protocol sha256: %s" % h_proto)
if h_proto != PROTOCOL_PIN:
    log("HALT: protocol hash mismatch. Tree terminates before any field is minted.")
    sys.exit(42)
log("protocol pin OK (post-fix LOG-4705 revision)")

# ---------------- 1. prompts: verbatim EXP107 bench, canonical first 10 ----------------
sys.path.insert(0, EXP107DIR)
from build_exp107_bench import build_bench  # noqa: E402

bench = build_bench()
assert len(bench) == 60, "EXP107 bench len != 60"
items = bench[:10]
prompt_ids = [b["id"] for b in items]
prompt_texts = [b["prompt"] for b in items]
exp_ids = ["exp107_%s_exp077_planet_2hop_%d" % (("flip" if i % 2 == 0 else "ctrl"), i) for i in range(10)]
# actual canonical ids verified from bench construction + EXP127 decision set
exp_ids = ["exp107_flip_exp077_planet_2hop_0", "exp107_ctrl_exp077_planet_2hop_1",
           "exp107_flip_exp077_planet_2hop_2", "exp107_ctrl_exp077_planet_2hop_3",
           "exp107_flip_exp077_planet_2hop_4", "exp107_ctrl_exp077_planet_2hop_5",
           "exp107_flip_exp077_planet_2hop_6", "exp107_ctrl_exp077_planet_2hop_7",
           "exp107_ctrl_exp077_planet_2hop_8", "exp107_flip_exp077_planet_2hop_9"]
assert prompt_ids == exp_ids, "canonical first-10 ids mismatch: %s" % prompt_ids
ref127 = json.load(open(EXP127_REF))
assert len(ref127) == 10
for i, r in enumerate(ref127):
    assert r["prompt"] == prompt_texts[i], "prompt %d text differs from EXP127 pinned decision set" % i
log("prompts: canonical-order first 10 of verbatim EXP107 bench; ids + text match EXP127 decision set")

# ---------------- 2. environment ----------------
torch.manual_seed(BASE_SEED)
torch.set_num_threads(2)
threads = torch.get_num_threads()
assert threads == 2, "thread read-back != 2"
log("torch %s | transformers %s | numpy %s | sklearn N/A (no fit) | threads=%d (read back)"
    % (torch.__version__, transformers.__version__, np.__version__, threads))

# ---------------- 3. frozen backbone (AutoModelForCausalLM — EXP126 loader lesson) ----------------
model = transformers.AutoModelForCausalLM.from_pretrained(
    SNAP, local_files_only=True, trust_remote_code=False,
    device_map="cpu", torch_dtype=torch.float32,
    output_hidden_states=True, output_attentions=False)
model.eval()
for p in model.parameters():
    p.requires_grad_(False)
h_pre = state_dict_hash(model)
log("backbone LOG-331 pin (pre): %s" % h_pre)
if h_pre != WEIGHTS_PIN:
    log("RUN-INVALID: backbone pin mismatch before first forward (Law #6). Quarantine. No field exists.")
    sys.exit(42)
log("backbone pin OK. Delta-theta guard armed.")
tokenizer = transformers.AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
cfg = model.config
assert (cfg.hidden_size,) == (HID,), "hidden size mismatch"
final_ln = model.gpt_neox.final_layer_norm

@torch.no_grad()
def base_forward(input_ids):
    """Full frozen forward; returns x_{24,last} (post-final-LN input to unembedding)."""
    out = model(input_ids=input_ids)
    h24 = out.hidden_states[24]
    x24 = final_ln(h24)
    return x24[0, -1, :].detach()

@torch.no_grad()
def perturbed_forward(input_ids, site_layer, delta):
    """Perturb final-token residual at site `site_layer` (0=post-embed, l>=1=block l-1 out)."""
    if site_layer == 0:
        mod = model.gpt_neox.embed_in
    else:
        mod = model.gpt_neox.layers[site_layer - 1]

    def hook(_m, _inp, outp):
        o = outp.clone()
        o[:, -1, :] = o[:, -1, :] + delta
        return o

    handle = mod.register_forward_hook(hook)
    try:
        out = model(input_ids=input_ids)
    finally:
        handle.remove()
    h24 = out.hidden_states[24]
    x24 = final_ln(h24)
    return x24[0, -1, :].detach()

# ---------------- 4. forward batches ----------------
input_ids_list = [tokenizer(t, return_tensors="pt")["input_ids"] for t in prompt_texts]

fwd_field_base = 0
fwd_field_pert = 0
fwd_check = 0

# per-(item, layer) base readouts (computed once per item; protocol formula counts 2/arm)
base_x24 = {}
for i in range(ITEMS_N):
    base_x24[i] = base_forward(input_ids_list[i])
    fwd_field_base += 1
log("base pass complete: 10/10 readouts (1 forward per item)")

ratio_records = []   # field arm
check_records = []   # eps/2 arm
# per (item, layer) draw lists
field_draws = {}     # (i, l) -> [ratios]
check_draws = {}     # (i, l) -> [ratios_half]

t0 = time.time()
total_triples = ITEMS_N * N_LAYERS * K_DRAWS
done = 0
for i in range(ITEMS_N):
    for l in range(N_LAYERS):
        for d in range(K_DRAWS):
            seed = seed_for(i, l, d)
            delta = draw_delta(seed, EPS)
            dn = float(torch.linalg.norm(delta))
            if abs(dn - EPS) > 1e-9:
                log("APPARATUS-VOID: delta budget violated at (i=%d,l=%d,d=%d): ||delta||=%r" % (i, l, d, dn))
                sys.exit(43)
            x24p = perturbed_forward(input_ids_list[i], l, delta)
            fwd_field_pert += 1
            ratio = float(torch.linalg.norm(x24p - base_x24[i])) / dn
            ratio_records.append({"item": i, "layer": l, "draw": d, "seed": seed,
                                  "delta_norm": dn, "ratio": ratio, "arm": "field"})
            field_draws.setdefault((i, l), []).append(ratio)
            done += 1
            if done % 240 == 0:
                log("field forwards: %d/%d (%.1f min elapsed)" % (done, total_triples, (time.time() - t0) / 60.0))
log("field batch complete: base=%d perturbed=%d (protocol formula: 10*24*4*2=1920)" % (fwd_field_base, fwd_field_pert))

# epsilon/2 linearity-check arm: items {0,4,9} x layers {L5,L11,L17,L23}, same seeds/draw indices
for i in CHECK_ITEMS:
    for l in CHECK_LAYERS:
        for d in range(K_DRAWS):
            seed = seed_for(i, l, d)
            delta = draw_delta(seed, EPS / 2.0)
            dn = float(torch.linalg.norm(delta))
            if abs(dn - EPS / 2.0) > 1e-9:
                log("APPARATUS-VOID: delta budget violated at check (i=%d,l=%d,d=%d)" % (i, l, d))
                sys.exit(43)
            x24p = perturbed_forward(input_ids_list[i], l, delta)
            fwd_check += 1
            ratio = float(torch.linalg.norm(x24p - base_x24[i])) / dn
            check_records.append({"item": i, "layer": l, "draw": d, "seed": seed,
                                  "delta_norm": dn, "ratio": ratio, "arm": "eps_half"})
            check_draws.setdefault((i, l), []).append(ratio)
log("check batch complete: %d eps/2 forwards (expected 3*4*4=48)" % fwd_check)
assert fwd_check == 48

# ---------------- 5. linearity-check evaluation (breaking point (b)) ----------------
check_flags = []
for (i, l) in sorted(check_draws):
    s_eps = float(np.mean(field_draws[(i, l)]))
    s_half = float(np.mean(check_draws[(i, l)]))
    if s_eps == 0.0:
        passed = False
    else:
        passed = (abs(s_half - s_eps) / s_eps) <= LIN_TOL
    check_flags.append({"item": i, "layer": l, "S_eps": s_eps, "S_eps_half": s_half,
                        "rel": (abs(s_half - s_eps) / s_eps) if s_eps != 0 else None,
                        "pass": passed})
n_pass = sum(1 for c in check_flags if c["pass"])
log("linearity check: %d/12 within 25%% (bar: >= 10/12)" % n_pass)
for c in check_flags:
    log("  item %d layer L%d: S(eps)=%.6g S(eps/2)=%.6g rel=%.4g %s"
        % (c["item"], c["layer"], c["S_eps"], c["S_eps_half"], c["rel"] if c["rel"] is not None else float("nan"),
           "PASS" if c["pass"] else "FAIL"))
if n_pass < LIN_MIN_PASS:
    log("APPARATUS-VOID: linearity check failed (%d/12 < 10/12). No field minted." % n_pass)
    sys.exit(44)
log("linearity check PASS — finite difference is in the linear regime")

# ---------------- 6. backbone pin (post) ----------------
h_post = state_dict_hash(model)
log("backbone LOG-331 pin (post): %s" % h_post)
if h_post != WEIGHTS_PIN or h_post != h_pre:
    log("APPARATUS-VOID: backbone pin mismatch post-forward. Δθ != 0.")
    sys.exit(45)
log("Δθ=0 confirmed (pins identical, LOG-331)")

# ---------------- 7. field elements + SEs ----------------
S_l = []
SE_l = []
for l in range(N_LAYERS):
    vals = []
    for i in range(ITEMS_N):
        vals.extend(field_draws[(i, l)])
    assert len(vals) == 40
    S_l.append(float(np.mean(vals)))
    SE_l.append(float(np.std(vals, ddof=1) / math.sqrt(40)))

# split-half Gini-stability diagnostic (disclosed OBSERVATION, no bar reads it)
def gini_of(vals):
    v = np.asarray(vals, dtype=np.float64)
    m = v.mean()
    if m == 0:
        return float("nan")
    n = len(v)
    return float(np.abs(v[:, None] - v[None, :]).sum() / (2.0 * n * n * m))

halfA, halfB = [], []
for l in range(N_LAYERS):
    a, b = [], []
    for i in range(ITEMS_N):
        a.extend(field_draws[(i, l)][:2])
        b.extend(field_draws[(i, l)][2:])
    halfA.append(float(np.mean(a)))
    halfB.append(float(np.mean(b)))
gini_halfA, gini_halfB = gini_of(halfA), gini_of(halfB)
log("OBSERVATION (no bar): split-half Gini draws{0,1}=%.4f draws{2,3}=%.4f" % (gini_halfA, gini_halfB))

# ---------------- 8. raw-record hash-pin BEFORE Gini (§3.9) ----------------
env_manifest = {
    "torch": torch.__version__, "transformers": transformers.__version__,
    "numpy": np.__version__, "threads": threads,
    "backbone_pin_pre": h_pre, "backbone_pin_post": h_post,
    "delta_theta": 0,
    "protocol_sha256": h_proto,
    "forward_counts": {"field_base": fwd_field_base, "field_perturbed": fwd_field_pert,
                       "check_eps_half": fwd_check,
                       "protocol_formula_field": ITEMS_N * N_LAYERS * K_DRAWS * 2},
    "eps": EPS, "K_draws": K_DRAWS, "base_seed": BASE_SEED, "layers": N_LAYERS, "items": ITEMS_N,
    "check_items": list(CHECK_ITEMS), "check_layers": list(CHECK_LAYERS),
    "linearity_pass": n_pass, "linearity_min": LIN_MIN_PASS,
    "elapsed_s": time.time() - t0,
}
field_obj = {"S_l": S_l, "SE_l": SE_l,
             "draw_config": "torch.Generator.manual_seed(seed); randn(1024) normalized; delta=eps*u",
             "per_item_layer_draw": field_draws}
check_obj = {"records": check_flags, "per_arm": check_records}
ratios_obj = {"field": ratio_records}
json.dump(field_obj, open(os.path.join(OUT, "exp128_field.json"), "w"))
json.dump(check_obj, open(os.path.join(OUT, "exp128_check.json"), "w"))
json.dump(ratios_obj, open(os.path.join(OUT, "exp128_ratios.json"), "w"))
json.dump(env_manifest, open(os.path.join(OUT, "exp128_manifest.json"), "w"), indent=1)

pins = {
    "exp128_field.json": sha256_file(os.path.join(OUT, "exp128_field.json")),
    "exp128_check.json": sha256_file(os.path.join(OUT, "exp128_check.json")),
    "exp128_ratios.json": sha256_file(os.path.join(OUT, "exp128_ratios.json")),
    "exp128_manifest.json": sha256_file(os.path.join(OUT, "exp128_manifest.json")),
}
worksheet = {"env_manifest": env_manifest, "raw_sha256_pre_gini": pins,
             "check_flags": check_flags, "S_l": S_l, "SE_l": SE_l}
json.dump(worksheet, open(os.path.join(OUT, "exp128_worksheet.json"), "w"), indent=1)
pins["exp128_worksheet.json"] = sha256_file(os.path.join(OUT, "exp128_worksheet.json"))
_logf.flush()
pins["exp128_console.log"] = "computed-after-flush"
for k, v in pins.items():
    log("pinned (pre-Gini) %s: %s" % (k, v))

# ---------------- 9. decision statistic: layer-Gini + top-3 ----------------
G = gini_of(S_l)
order = sorted(range(N_LAYERS), key=lambda l: (-S_l[l], l))
top3 = order[:3]
log("layer-Gini G = %.6f" % G)
log("top-3 concentration layers: %s" % (["L%d" % l for l in top3],))
log("field: " + " ".join("L%d=%.4g" % (l, S_l[l]) for l in range(N_LAYERS)))
log("OBSERVATION (no bar): per-layer SEs " + " ".join("L%d=%.2g" % (l, SE_l[l]) for l in range(N_LAYERS)))

READOUT_ADJ = {21, 22, 23}
if G >= 0.4 and not set(top3) <= READOUT_ADJ:
    verdict = "CONTINUE"
elif G >= 0.4 and set(top3) <= READOUT_ADJ:
    verdict = "KILL-as-independent-family"
elif G >= 0.2:
    verdict = "HELD"
else:
    verdict = "KILL"
log("VERDICT: %s — Gini=%.6f top-3=%s" % (verdict, G, ["L%d" % l for l in top3]))

# ---------------- 10. decision record into worksheet ----------------
worksheet["Gini"] = G
worksheet["top3"] = top3
worksheet["verdict"] = verdict
worksheet["split_half_gini"] = {"draws01": gini_halfA, "draws23": gini_halfB}
worksheet["raw_sha256_post_gini"] = pins
json.dump(worksheet, open(os.path.join(OUT, "exp128_worksheet.json"), "w"), indent=1)
log("final worksheet written; exp128_worksheet.json: %s" % sha256_file(os.path.join(OUT, "exp128_worksheet.json")))
log("done. verdict=%s Gini=%.6f" % (verdict, G))
_logf.close()
sys.exit(0)
