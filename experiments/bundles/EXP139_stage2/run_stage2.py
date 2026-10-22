#!/usr/bin/env python3
"""EXP139 Stage-2: full attractor test (T=8, GPU, founder-gated).

Executes EXACTLY per research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md
(SIGNED, LOG-4885), §5, reusing the Stage-1 implementation precedent
(experiments/runs/EXP139_stage1/run_stage1.py).

Documented execution choices (NOT protocol changes; see BUNDLE_NOTES.md):
  AMBIGUITY-1: 60 fresh baseline passes (540 total), not the pre-reg's 520.
      Stage-1 archived only h_i norms, not the 20 h_i vectors, so items 0-19
      cannot be reused on the founder's machine; recomputation is
      deterministic per machine (cross-machine equivalence is anchored by
      validity gates (a)–(c), not by a bitwise claim).
  AMBIGUITY-2: readout is the two-way candidate comparison (Stage-1 and the
      committed EXP135 records' convention), not the pre-reg §2 text's
      full-vocab argmax. The paired table is only well-defined under the
      two-way convention (baseline correctness is derived from committed yhat).
  Gate (c) is extended to all 60 items (60/60) as the direct analog of §3(c);
      the paired table itself uses the COMMITTED baseline yhat (pre-reg §4/§5:
      "no new baseline passes" for the comparison).
  AMBIGUITY-4 (adjudicated, binding Law #14 apparatus review LOG-4896): for
      κ̂<1 and ΔM_attractor ≤ 0 the governing branch is HELD(f) ("converges to
      nothing useful — dynamics exist, no capability; licenses nothing, kills
      nothing"). The §0 breaking-points line and §5 bar assigning KILL are
      superseded as drafting defects. This is a pre-execution disambiguation,
      not a post-hoc bar shift (Law #4).

Exit codes: 0 = clean completion; 44 = RUN-INVALID (validity gate trip or
venue failure). No training, no weight updates, Δθ=0 throughout.
"""
import hashlib
import json
import os
import sys
import time

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)
import exp139_stage2_lib as L  # noqa: E402

import torch  # noqa: E402
from transformers import AutoTokenizer, AutoModelForCausalLM  # noqa: E402

OUT_DIR = os.path.join(BUNDLE_DIR, "out")
os.makedirs(OUT_DIR, exist_ok=True)
LOGF = open(os.path.join(OUT_DIR, "stage2_run_log.txt"), "w")


def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOGF.write(line + "\n")
    LOGF.flush()


FWD_COUNT = [0]


def count_fwd(n=1):
    FWD_COUNT[0] += n


def sha256_state_dict(model):
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu()
        if t.dtype != torch.float32:
            t = t.float()
        h.update(t.numpy().tobytes())
    return h.hexdigest()


def run_invalid(reason):
    log("RUN-INVALID: %s" % reason)
    json.dump({"verdict": "RUN-INVALID", "reason": reason, "forwards": FWD_COUNT[0]},
              open(os.path.join(OUT_DIR, "stage2_verdict.json"), "w"), indent=1)
    LOGF.close()
    sys.exit(44)


# ============ venue ============
if not torch.cuda.is_available():
    run_invalid("no CUDA device visible — Stage-2 is GPU-gated (founder's Kaggle T4)")
DEVICE = torch.device("cuda:0")
log("device=%s (%s)" % (DEVICE, torch.cuda.get_device_name(0)))
# execution hygiene only (not protocol): reduce nondeterminism sources
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# ============ model (pre-reg §2 verbatim, venue moved to cuda:0) ============
log("loading model %s rev %s (float32, local_files_only)" % (L.MODEL_ID, L.HF_REVISION))
try:
    tokenizer = AutoTokenizer.from_pretrained(
        L.MODEL_ID, revision=L.HF_REVISION, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        L.MODEL_ID, revision=L.HF_REVISION, local_files_only=True,
        torch_dtype=torch.float32, device_map="cpu")
except Exception as e:
    run_invalid(
        "model cache missing or unreadable (%s). The founder must first run: "
        "huggingface-cli download %s --revision %s" % (e, L.MODEL_ID, L.HF_REVISION))
model.to(DEVICE)
model.eval()
pre_hash = sha256_state_dict(model)
log("backbone pre-hash: %s" % pre_hash)
if pre_hash != L.BACKBONE_PIN:
    run_invalid("(b) backbone pre-hash mismatch: got %s" % pre_hash)
log("(b) backbone pin PASS")

# ============ bench (verbatim port of run_stage1.py via lib) ============
bench = L.build_bench()
assert len(bench) == L.N_ITEMS, "bench len %d != %d" % (len(bench), L.N_ITEMS)
bench_hash = L.bench_sha256(bench)
log("(a) bench len=60; bench sha256=%s" % bench_hash)
if bench_hash != L.BENCH_PIN:
    run_invalid("(a) bench sha256 mismatch: got %s" % bench_hash)
log("(a) bench pin PASS")

views0 = [L.make_views(it, L.novel_src(it))[0] for it in bench]  # view 0

# committed baseline (view 0) — copied values, never recomputed for the table
committed = json.load(open(os.path.join(BUNDLE_DIR, "data",
                                        "committed_baseline_view0.json")))
assert committed["n_items"] == L.N_ITEMS
committed_yhat = [it["committed_yhat"] for it in committed["items"]]
assert [it["id"] for it in committed["items"]] == [b["id"] for b in bench], \
    "committed item ids do not match reconstructed bench"

# ============ operator + forward machinery (pre-reg §2) ============
W_E = model.gpt_neox.embed_in.weight.detach()
W_U = model.get_output_embeddings().weight.detach()
final_ln = model.gpt_neox.final_layer_norm


def tok1(s):
    ids = tokenizer.encode(" " + s)
    assert len(ids) == 1, "multi-token: %s -> %s" % (s, ids)
    return ids[0]


def R_of_h(h):
    """One re-entrant step. h: (1024,) float32 pre-LN residual state."""
    z = W_E.t() @ (W_U @ h)                      # Pi h, raw-logit weighting, no softmax
    inputs_embeds = z.view(1, 1, L.D_HID)
    with torch.no_grad():
        out = model(inputs_embeds=inputs_embeds,
                    position_ids=torch.tensor([[0]], device=DEVICE),
                    attention_mask=torch.tensor([[1]], device=DEVICE),
                    output_hidden_states=True)
    count_fwd(1)
    return out.hidden_states[-1][0, 0, :].detach()


def baseline_forward(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        out = model(input_ids=input_ids, output_hidden_states=True)
    count_fwd(1)
    h_last = out.hidden_states[-1][0, -1, :].detach()
    return h_last, out.logits[0, -1, :].detach()


def yhat_of(lv1d, t_target, t_foil):
    """Two-way candidate comparison — Stage-1 / committed-records convention
    (AMBIGUITY-2; see module docstring)."""
    return int(t_target) if float(lv1d[t_target]) >= float(lv1d[t_foil]) else int(t_foil)


def readout_yhat(h):
    lv = model.get_output_embeddings()(final_ln(h)).detach()
    return lv


# ============ Stage-2: 60 baselines + 480 R-evaluations ============
log("Stage-2: 60 baseline + 480 R-evaluation passes (T=%d)" % L.T_STEPS)
base_correct, attr_correct = [], []
traj_all, yhat_traj = [], []
recomputed_yhat = []
for ii in range(L.N_ITEMS):
    v = views0[ii]
    tA, tC = tok1(v["A"]), tok1(v["C"])
    h0, lv_base = baseline_forward(v["prompt"])
    yh_base = yhat_of(lv_base, tA, tC)
    recomputed_yhat.append(yh_base)

    # re-entrant iteration h^(1)..h^(T)
    traj = [h0]
    for _ in range(L.T_STEPS):
        traj.append(R_of_h(traj[-1]))
    diffs = [float(torch.norm(traj[t + 1] - traj[t])) for t in range(L.T_STEPS)]

    # binding decode at t=T (position 0, the sole position)
    lv_attr = readout_yhat(traj[L.T_STEPS])
    yh_attr = yhat_of(lv_attr, tA, tC)

    # diagnostics only (non-binding): per-t decodes
    diag = []
    for t in range(1, L.T_STEPS):
        lv_t = readout_yhat(traj[t])
        diag.append(yhat_of(lv_t, tA, tC))

    base_correct.append(1 if yh_base == tA else 0)
    attr_correct.append(1 if yh_attr == tA else 0)
    traj_all.append([float(x) for x in diffs])
    yhat_traj.append(diag)
    # keep GPU memory lean
    del traj
    if (ii + 1) % 10 == 0:
        log("  item %d/60; forwards=%d" % (ii + 1, FWD_COUNT[0]))

log("forwards total=%d (expected %d)" % (FWD_COUNT[0], L.EXPECTED_FORWARDS))
if FWD_COUNT[0] != L.EXPECTED_FORWARDS:
    run_invalid("forward budget: %d != %d" % (FWD_COUNT[0], L.EXPECTED_FORWARDS))

# validity gate (c): recomputed baseline yhat matches committed yhat 60/60
match = sum(1 for a, b in zip(recomputed_yhat, committed_yhat) if a == b)
log("(c) baseline yhat match: %d/60" % match)
if match != L.N_ITEMS:
    run_invalid("(c) baseline yhat mismatch: %d/60" % match)
log("(c) yhat fidelity PASS")

# ============ inference (§7): paired table vs COMMITTED baseline ============
# baseline correctness is derived from committed yhat (labels touch evaluation only)
committed_correct = []
for ii in range(L.N_ITEMS):
    tA = tok1(views0[ii]["A"])
    committed_correct.append(1 if committed_yhat[ii] == tA else 0)
b = sum(1 for bc, ac in zip(committed_correct, attr_correct) if bc == 0 and ac == 1)
c = sum(1 for bc, ac in zip(committed_correct, attr_correct) if bc == 1 and ac == 0)
nc = L.newcombe_paired(b, c, L.N_ITEMS)
mcnemar_p = L.mcnemar_exact_twosided(b, c)
log("paired table: b=%d (baseline wrong, attractor right) c=%d (baseline right, attractor wrong) n=%d"
    % (b, c, L.N_ITEMS))
log("DeltaM_attractor=%.4f  Newcombe 95%% LCI: L=%.4f U=%.4f" % (nc["dhat"], nc["L"], nc["U"]))
log("McNemar-exact two-sided p (secondary) = %.4g" % mcnemar_p)

# ============ trajectory diagnostic (binding backstop) ============
traj_ok = all(L.trajectory_strictly_decreasing(d) for d in traj_all)
log("trajectory strictly decreasing on all 60 items: %s" % traj_ok)

# ============ verdict-tree report (§6, κ̂<1 path; AMBIGUITY-4 adjudicated LOG-4896) ============
report = L.stage2_branch_report(nc["dhat"], nc["L"], nc["U"], traj_ok)
for name, reading in report["branches"]:
    log("branch: %s — %s" % (name, reading))
for conflict in report["conflicts"]:
    # Post-LOG-4896 this list is expected empty (AMBIGUITY-4 adjudicated to
    # HELD(f)); retained as a defensive tripwire only.
    log("CONFLICT (unexpected — none should remain post-LOG-4896): %s" % conflict)

# ============ Law #6: backbone post-hash (Δθ=0) — mismatch is RUN-INVALID ============
post_hash = sha256_state_dict(model)
log("backbone post-hash: %s" % post_hash)
if post_hash != L.BACKBONE_PIN:
    run_invalid("(post) backbone post-hash mismatch: got %s" % post_hash)
log("Δθ=0 post PASS")

# ============ artifacts (Law #8) ============
rec = {
    "experiment": "EXP139", "stage": 2, "log": "LOG-4885(pre-reg)",
    "n_items": L.N_ITEMS, "view": 0, "T": L.T_STEPS,
    "backbone_pre": pre_hash, "backbone_post": post_hash, "bench_sha256": bench_hash,
    "yhat_fidelity": "%d/60" % match,
    "paired": {"b": b, "c": c, "n": L.N_ITEMS},
    "newcombe": nc, "mcnemar_exact_twosided_p": mcnemar_p,
    "trajectory_strictly_decreasing_all": traj_ok,
    "trajectory_diff_norms": traj_all,
    "baseline_correct_committed": committed_correct,
    "attractor_correct_t8": attr_correct,
    "attractor_yhat_diagnostics_t1_t7": yhat_traj,
    "branch_report": report,
    "forwards": FWD_COUNT[0],
    "ambiguities_documented": ["AMBIGUITY-1", "AMBIGUITY-2", "AMBIGUITY-3", "AMBIGUITY-4"],
    "env": {"torch": torch.__version__, "device": torch.cuda.get_device_name(0)},
}
json.dump(rec, open(os.path.join(OUT_DIR, "stage2_records.json"), "w"))
json.dump({"experiment": "EXP139", "stage": 2,
           "gates": {"bench_pin": "PASS", "backbone_pin": "PASS", "yhat_fidelity": "PASS"},
           "backbone_post": post_hash,
           "paired": {"b": b, "c": c}, "newcombe": nc,
           "trajectory_ok": traj_ok, "branch_report": report,
           "forwards": FWD_COUNT[0]},
          open(os.path.join(OUT_DIR, "stage2_verdict.json"), "w"), indent=1)

report_md = """# EXP139 Stage-2 Run Report (full attractor test, T=8)

**Pre-reg:** `research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4885).
Bundle: `experiments/bundles/EXP139_stage2/`. Founder GPU venue.

## Validity gates
- (a) bench sha256: `{bench}` — PASS
- (b) backbone pre-hash: `{pin}` — PASS
- (c) baseline yhat fidelity: {match}/60 — PASS

## Results
- Paired table (n=60): b={b} (baseline wrong, attractor right), c={c} (baseline right, attractor wrong)
- ΔM_attractor: {dhat:+.4f}; Newcombe paired 95% LCI: [{L:+.4f}, {U:+.4f}]
- McNemar-exact two-sided p (secondary): {mp:.4g}
- Trajectory strictly decreasing (all 60 items): {traj}
- forwards: {fwd} (budget {exp})

## Branch report (pre-reg §6)
{branches}
{conflicts}

## Documented ambiguities (see BUNDLE_NOTES.md)
- AMBIGUITY-1: 540 passes executed vs pre-reg's 520 (Stage-1 archived norms only).
- AMBIGUITY-2: two-way readout convention (Stage-1/committed), not full-vocab argmax.
- AMBIGUITY-3: McNemar two-sided convention (doubling method).
- AMBIGUITY-4: ΔM≤0 → HELD(f) per binding Law #14 adjudication (LOG-4896);
  the §0/§5 KILL lines are superseded as drafting defects (pre-execution
  disambiguation, not a post-hoc bar shift).
""".format(bench=bench_hash, pin=pre_hash, match=match, b=b, c=c,
           dhat=nc["dhat"], L=nc["L"], U=nc["U"], mp=mcnemar_p, traj=traj_ok,
           fwd=FWD_COUNT[0], exp=L.EXPECTED_FORWARDS,
           branches="\n".join("- **%s**: %s" % br for br in report["branches"]),
           conflicts="\n".join("> CONFLICT: %s" % cf for cf in report["conflicts"])
           or "> none")
open(os.path.join(OUT_DIR, "RUN_REPORT.md"), "w").write(report_md)

log("CLEAN COMPLETION exit 0")
LOGF.close()
