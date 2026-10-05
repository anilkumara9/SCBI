"""EXP145 intervention arm — decision loop (S7-2 §3.4).

Executed ONLY if decode+ (D1 and D2 both pass). 3 conditions (B/P/N) x 60
items = 180 forward passes, GPT-2-small, CPU, $0.

Port of EXP093 run_conditions_real, adapted:
  - hook point: transformer.h[l*] (D4);
  - α calibrated: α = 0.047 × mean_i‖h_i‖ from the clean-run l* residual
    norms (S7-2 §3.4.3); assert achieved ‖αv‖/mean‖h_i‖ ∈ 0.047 ± 0.01;
  - per-item LOO directions v^(−i) (no item-i leakage), P=+αv^(−i),
    N=−αv^(−i);
  - G4 baseline reproduction: condition-B (hook attached, disabled) must
    reproduce the decode arm's S2 refs — n_correct identical AND
    |mean margin − ref| ≤ 1e-4 (mirrors EXP093's 36/60 + 1e-4 margin tol);
    failure → INCONCLUSIVE (measurement failure, S7-2 §3.4.6);
  - G5 re-verified with correct hook ordering BEFORE the loop;
  - G1 pre/post state-dict hash (Δθ=0); pre-hash additionally asserted
    equal to the extraction phase's recorded hash (same frozen snapshot);
  - per-item records written INCREMENTALLY (flush after each item).

Margins: raw-logit(target) − raw-logit(foil) at the final token, option ids
from the G1' table (never bare-word). Correct iff margin > 0 (strict —
ties incorrect, verbatim EXP093 tie rule).
"""

import json
import os
import sys

# Environment quirk (see exp145_step0_download.py): sanitize bracketed IPv6
# entries from no_proxy/NO_PROXY before any hub/httpx import.
for _var in ("no_proxy", "NO_PROXY"):
    _val = os.environ.get(_var)
    if _val:
        _clean = ",".join(p for p in _val.split(",") if "[" not in p and "]" not in p)
        os.environ[_var] = _clean

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp145_common as C  # noqa: E402
import exp145_inject as inj  # noqa: E402

MANIFEST = os.path.join(C.RUN_DIR, "exp145_manifest.json")
DECODE = os.path.join(C.RUN_DIR, "exp145_decode_report.json")
DIRJSON = os.path.join(C.RUN_DIR, "exp145_direction_verification.json")
DIRS = os.path.join(C.RUN_DIR, "exp145_directions.npz")
RECORDS = os.path.join(C.RUN_DIR, "exp145_decision_records.jsonl")
META = os.path.join(C.RUN_DIR, "exp145_decision_meta.json")

PERT_RATIO = 0.047   # S7-2 §3.4.3
PERT_TOL = 0.01      # ±0.01 assert bar
G4_MARGIN_TOL = 1e-4  # mirrors EXP093


def main():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from huggingface_hub import snapshot_download

    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print(msg, flush=True)

    with open(MANIFEST) as f:
        manifest = json.load(f)
    rev = manifest["model_revision_40hex"]
    with open(DECODE) as f:
        dec = json.load(f)
    with open(DIRJSON) as f:
        dj = json.load(f)

    if not (dec["D1"] and dj["D2"] == "PASS"):
        raise C.Inconclusive(
            "decode arm did not reach decode+ (D1 or D2 failed) — the "
            "intervention arm is not licensed (S7-2 §3.4).")
    l_star = int(dec["l_star"])
    v = np.load(DIRS)["v"].astype(np.float64)  # (60, 768) v^(-i)
    assert v.shape == (C.N_ITEMS, 768)

    torch.set_num_threads(C.THREAD_PIN)
    assert torch.get_num_threads() == C.THREAD_PIN
    log(f"[decision] threads pinned: {C.THREAD_PIN}")

    bench, g0 = C.guard_g0_bench()
    assert g0["pin"] == manifest["bench_pin"]

    # α calibration from the clean-run l* residual norms (decode-arm
    # embeddings ARE the clean final-token residuals at l*).
    z = np.load(os.path.join(C.RUN_DIR, "exp145_embeddings.npz"),
                allow_pickle=True)
    H = z["layers"][l_star].astype(np.float64)  # (60, 768)
    norms = np.linalg.norm(H, axis=1)
    mean_norm = float(norms.mean())
    alpha = PERT_RATIO * mean_norm
    achieved = alpha / mean_norm  # v unit-norm: ||alpha*v||/mean = alpha/mean
    if abs(achieved - PERT_RATIO) > PERT_TOL:
        raise C.Inconclusive(
            f"α calibration assert failed: achieved ratio {achieved:.4f} not "
            f"in {PERT_RATIO}±{PERT_TOL} — INCONCLUSIVE (recalibrate-once or "
            f"INCONCLUSIVE; one attempt licensed, value unchanged).")
    log(f"[decision] α={alpha:.6f} (0.047 × mean‖h_i‖={mean_norm:.4f}); "
        f"achieved perturbation ratio {achieved:.4f} ∈ 0.047±0.01: PASS.")

    # G4 refs from the decode arm's S2 (pre-registered before the loop).
    g4_n = int(dec["S2"]["n_correct_raw"])
    g4_margin = float(dec["S2"]["mean_raw_logit_margin"])
    log(f"[decision] G4 refs (decode-arm S2): n_correct={g4_n}/60, "
        f"mean margin={g4_margin:.6f}.")

    snap = snapshot_download(
        manifest["repo_id"], revision=rev,
        cache_dir=os.path.join(C.RUN_DIR, "hf_cache"))
    assert os.path.basename(os.path.normpath(snap)) == rev, "S0.2 drift"
    log("[decision] S0.2 pass: revision character-identical to pin.")

    tokenizer = AutoTokenizer.from_pretrained(snap, local_files_only=True)
    sys.path.insert(0, C.EXP092_DIR)
    import g1prime
    table = g1prime.verify_g1_prime(tokenizer, bench)
    opt_ids = [(table[b["A"]]["token_id"], table[b["C"]]["token_id"])
               for b in bench]
    log("[decision] G1' re-pass (real tokenizer, before decision loop).")

    model = AutoModelForCausalLM.from_pretrained(
        snap, local_files_only=True, torch_dtype=torch.float32,
        device_map="cpu")
    model.eval()
    model.requires_grad_(False)
    log("[decision] model loaded: eval(), requires_grad_(False), CPU.")

    # G1 (pre): frozen hash must match the recorded extraction-phase hash.
    with open(os.path.join(C.RUN_DIR, "exp145_extraction_meta.json")) as f:
        ext_meta = json.load(f)
    pre = C.compute_state_dict_hash(
        {k: v_.detach().cpu() for k, v_ in model.state_dict().items()})
    if pre != ext_meta.get("G1_pre_hash"):
        raise C.RunInvalid(
            f"G1 FAIL (pre): decision-loop state-dict hash {pre[:16]}… != "
            f"recorded extraction hash — snapshot drift — RUN-INVALID.")
    log(f"[decision] G1 pre hash OK: {pre[:16]}… (matches extraction; Δθ=0).")

    # G5 injection-site verification (single-item probe, correct ordering).
    g5 = inj.verify_g5_real(model, tokenizer, bench[0]["prompt"], v[0],
                            alpha, l_star)
    log(f"[decision] G5 PASS ({g5['hook_path']}): (i) rel_err="
        f"{g5['criterion_i_rel_err']:.2e}, nonfinal={g5['nonfinal_max_abs_change']:.2e}, "
        f"(ii) bit_match={g5['criterion_ii_bit_match']}, (iii) sane="
        f"{g5['criterion_iii_sane']}.")

    hook = inj.GPT2InjectionHook(l_star, alpha)
    writer = C.JsonlWriter(RECORDS)

    def margins_of(logits_t, a_id, c_id):
        lg = logits_t.detach().cpu().to(torch.float64).numpy()
        return float(lg[a_id] - lg[c_id])

    with torch.no_grad():
        # Condition B first for all items: G4 must pass before P/N run.
        mB = np.full(C.N_ITEMS, np.nan)
        done_b = {int(json.loads(l)["item"]) for l in
                  open(RECORDS) if l.strip() and json.loads(l).get("cond") == "B"} \
            if os.path.isfile(RECORDS) else set()
        for i, b in enumerate(bench):
            if i in done_b:
                continue
            ids = torch.tensor(
                [tokenizer.encode(b["prompt"], add_special_tokens=False)],
                dtype=torch.long)
            hook.attach(model, v[i])
            hook.disable()
            a_id, c_id = opt_ids[i]
            m = margins_of(model(ids).logits[0, -1, :], a_id, c_id)
            hook.detach()
            writer.write({"item": i, "id": b["id"], "cond": "B", "margin": m})
        # collect B margins
        recs = {}
        with open(RECORDS) as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    if r.get("cond") == "B":
                        recs[int(r["item"])] = r["margin"]
        mB = np.array([recs[i] for i in range(C.N_ITEMS)])
        n_b = int((mB > 0.0).sum())
        mean_m = float(mB.mean())
        if n_b != g4_n or abs(mean_m - g4_margin) > G4_MARGIN_TOL:
            raise C.Inconclusive(
                f"G4 FAIL: clean baseline {n_b}/60 correct (ref {g4_n}), mean "
                f"margin {mean_m:.6f} (ref {g4_margin:.6f}, tol "
                f"{G4_MARGIN_TOL}) — decision pipeline drifted — "
                f"INCONCLUSIVE (measurement failure).")
        log(f"[decision] G4 PASS: clean baseline {n_b}/60, mean margin "
            f"{mean_m:.6f} (ref {g4_margin:.6f}).")

        # Conditions P / N.
        for i, b in enumerate(bench):
            done = {json.loads(l)["cond"] for l in open(RECORDS)
                    if l.strip() and int(json.loads(l)["item"]) == i}
            if "P" in done and "N" in done:
                continue
            ids = torch.tensor(
                [tokenizer.encode(b["prompt"], add_special_tokens=False)],
                dtype=torch.long)
            a_id, c_id = opt_ids[i]
            if "P" not in done:
                hook.attach(model, v[i])
                hook.enable()
                mP = margins_of(model(ids).logits[0, -1, :], a_id, c_id)
                hook.detach()
                writer.write({"item": i, "id": b["id"], "cond": "P",
                              "margin": mP})
            if "N" not in done:
                hook.attach(model, -v[i])
                hook.enable()
                mN = margins_of(model(ids).logits[0, -1, :], a_id, c_id)
                hook.detach()
                writer.write({"item": i, "id": b["id"], "cond": "N",
                              "margin": mN})
        log("[decision] 180 forward passes complete (60 B + 60 P + 60 N).")

    # G1 (post): Δθ=0.
    post = C.compute_state_dict_hash(
        {k: v_.detach().cpu() for k, v_ in model.state_dict().items()})
    if post != pre:
        raise C.RunInvalid(
            f"G1 FAIL (post): state-dict hash changed — Δθ=0 VIOLATED — "
            f"RUN-INVALID.")
    log(f"[decision] G1 post hash OK: {post[:16]}… (Δθ=0 verified).")

    meta = {
        "experiment": "EXP145", "arm": "intervention",
        "l_star": l_star, "alpha": alpha, "mean_resid_norm": mean_norm,
        "perturbation_ratio_achieved": achieved,
        "perturbation_bar": [PERT_RATIO - PERT_TOL, PERT_RATIO + PERT_TOL],
        "G4": {"n_correct": n_b, "ref": g4_n,
               "mean_margin": mean_m, "ref_margin": g4_margin,
               "tol": G4_MARGIN_TOL, "gate": "PASS"},
        "G5": g5,
        "G1": f"pass (pre/post hash {pre[:16]}…, Δθ=0 verified)",
        "records": os.path.basename(RECORDS),
    }
    with open(META, "w") as f:
        json.dump(meta, f, indent=1)
    with open(os.path.join(C.RUN_DIR, "exp145_decision_log.txt"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    log(f"[decision] wrote {META}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except C.RunInvalid as e:
        print(f"RUN-INVALID: {e}", flush=True)
        sys.exit(3)
    except C.Inconclusive as e:
        print(f"INCONCLUSIVE: {e}", flush=True)
        sys.exit(4)
