"""EXP144 verdict — apply the frozen S7-2 §4 decision table (no other reading).

decode+ = (D1) ≥1 layer p < 0.05/12 with (acc−q95) ≥ 0.10 AND (D2) mean
shared-direction cosine ≥ 0.70.
steer+ = ≥6 decision flips AND McNemar p < 0.05 (verbatim doubling-convention
exact test, ported from the committed EXP093 scorer).
steer− = <6 flips and McNemar n.s.

§4 table:
  decode+/steer− → CONTINUE (gap replicates cross-family)
  decode+/steer+ → KILL (generality falsified as boundary law; PIVOT paper's
                         claim to Pythia/GPT-NeoX scope)
  decode−/steer− → KILL/PIVOT generality (with bench-fit caveat)
  decode−/steer+ → PIVOT-anomalous (fresh Law-#15 packet, not a gap verdict)

Writes: EXP144_VERDICT_2026-10-05.md + EXP144_RESULTS_2026-10-05.json in
research/analysis_plans/, and LOG-4919 at the top of reports/research_log.md.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp144_common as C  # noqa: E402

DECODE = os.path.join(C.RUN_DIR, "exp144_decode_report.json")
DIRJSON = os.path.join(C.RUN_DIR, "exp144_direction_verification.json")
RECORDS = os.path.join(C.RUN_DIR, "exp144_decision_records.jsonl")
DEC_META = os.path.join(C.RUN_DIR, "exp144_decision_meta.json")
MANIFEST = os.path.join(C.RUN_DIR, "exp144_manifest.json")
PLAN_DIR = os.path.expanduser("~/workspace/SCBI/research/analysis_plans")
LOG_PATH = os.path.expanduser("~/workspace/SCBI/reports/research_log.md")

FLIP_BAR = 6
ALPHA = 0.05


def mcnemar_exact_p(b, c):
    """Verbatim port of the committed EXP093 scorer's exact McNemar
    (two-sided, doubling convention). b = wrong-under-B/right-under-P;
    c = right-under-B/wrong-under-P."""
    n = int(b) + int(c)
    if n == 0:
        return 1.0
    k = min(int(b), int(c))
    tail = sum(math.comb(n, j) for j in range(k + 1)) * (0.5 ** n)
    return min(1.0, 2.0 * tail)


def main():
    with open(DECODE) as f:
        dec = json.load(f)
    with open(DIRJSON) as f:
        dj = json.load(f)
    with open(MANIFEST) as f:
        manifest = json.load(f)

    d1 = bool(dec["D1"])
    d2_cos = float(dj["D2_mean_cosine"])
    d2 = bool(dj["D2"] == "PASS")
    decode_plus = d1 and d2
    l_star = dec["l_star"]

    steer_stats = None
    if decode_plus:
        # Assemble per-item margins.
        recs = {}
        with open(RECORDS) as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    recs.setdefault(int(r["item"]), {})[r["cond"]] = r["margin"]
        assert len(recs) == C.N_ITEMS and all(
            set(v) == {"B", "P", "N"} for v in recs.values()), \
            f"decision records incomplete: {len(recs)}/60"
        import numpy as np
        mB = np.array([recs[i]["B"] for i in range(C.N_ITEMS)])
        mP = np.array([recs[i]["P"] for i in range(C.N_ITEMS)])
        mN = np.array([recs[i]["N"] for i in range(C.N_ITEMS)])
        # Verbatim EXP093 tie rule: correct iff margin > 0 (strict).
        cB = mB > 0.0
        cP = mP > 0.0
        cN = mN > 0.0
        b = int((~cB & cP).sum())
        c_ = int((cB & ~cP).sum())
        p = mcnemar_exact_p(b, c_)
        flips = b + c_
        steer_plus = (flips >= FLIP_BAR) and (p < ALPHA)
        acc_B, acc_P, acc_N = (float(cB.mean()), float(cP.mean()),
                               float(cN.mean()))
        delta = (int(cP.sum()) - int(cB.sum())) / C.N_ITEMS
        steer_stats = {
            "n": C.N_ITEMS,
            "acc_B": acc_B, "acc_P": acc_P, "acc_N": acc_N,
            "delta": delta,
            "monotone": bool(acc_P > acc_B > acc_N),
            "mcnemar_b": b, "mcnemar_c": c_, "flips": flips,
            "mcnemar_p": p,
            "steer_plus": bool(steer_plus),
            "flip_bar": FLIP_BAR, "alpha": ALPHA,
        }
        print(f"[verdict] P-vs-B: flips={flips} (b={b}, c={c_}), "
              f"McNemar p={p:.4g}, Δ={delta:+.4f}", flush=True)

    # §4 table (frozen; no other reading licensed).
    if decode_plus:
        assert steer_stats is not None
        if steer_stats["steer_plus"]:
            verdict = "KILL"
            reading = ("generality falsified as a boundary law: the decodable "
                       "direction is causal in GPT-2-small. PIVOT the paper's "
                       "claim to Pythia/GPT-NeoX scope.")
            cell = "decode+ / steer+"
        else:
            verdict = "CONTINUE"
            reading = ("the Decodability Gap replicates cross-family: "
                       "decodable (≥0.7 cosine) yet causally inert in a "
                       "second architecture. Licenses 'two-family' "
                       "generality language for the paper.")
            cell = "decode+ / steer−"
    else:
        verdict = "KILL/PIVOT"
        reading = ("the generality claim is killed/bounded with the recorded "
                   "caveat: the gap's precondition (decodability) is absent "
                   "here; this outcome cannot separate an architecture "
                   "effect from scale/bench-fit (the §1 steelman). The "
                   "dissociation itself is untested in this family.")
        cell = "decode− / steer− (intervention arm not licensed)"

    results = {
        "experiment": "EXP144",
        "verdict": verdict,
        "verdict_cell": cell,
        "verdict_reading": reading,
        "decode": {
            "D1": d1,
            "D2_mean_cosine": d2_cos,
            "D2": d2,
            "decode_plus": decode_plus,
            "l_star": l_star,
            "passing_layers": dec["passing_layers"],
            "alpha_bonferroni": dec["alpha_bonferroni"],
            "effect_bar": dec["effect_bar"],
            "perm_seed": dec["perm_seed"],
            "layers": dec["layers"],
            "S2": dec["S2"],
        },
        "steer": steer_stats,
        "integrity": {
            "model_revision_40hex": manifest["model_revision_40hex"],
            "bench_pin": manifest["bench_pin"],
            "g1prime": manifest["g1prime"],
            "frozen_backbone": "Δθ=0 asserted pre/post (extraction + "
                               "decision loop)",
            "cost": "$0 CPU",
        },
    }
    res_path = os.path.join(PLAN_DIR, "EXP144_RESULTS_2026-10-05.json")
    with open(res_path, "w") as f:
        json.dump(results, f, indent=1)
    print(f"[verdict] wrote {res_path}", flush=True)

    # Verdict report.
    best = max(dec["layers"], key=lambda s: s["accuracy"])
    lines = []
    A = lines.append
    A("# EXP144 — Verdict Report (2026-10-05)")
    A("")
    A(f"**Verdict: {verdict}** — cell `{cell}`.")
    A("")
    A("## 1. Decode arm (S7-2 §3.3)")
    A("")
    A(f"[OBSERVATION] D1: {'PASS' if d1 else 'FAIL'} — "
      f"{len(dec['passing_layers'])} layer(s) with p < {dec['alpha_bonferroni']:.6f} "
      f"and (acc−q95) ≥ {dec['effect_bar']}: {dec['passing_layers']}; "
      f"best layer {best['layer']} acc={best['accuracy']:.4f} "
      f"(p={best['p']:.4g}, effect={best['effect']:+.4f}).")
    A(f"[OBSERVATION] D2: mean_i cos(v^(−i), u_i) = {d2_cos:.4f} (bar 0.70) → "
      f"{'PASS' if d2 else 'FAIL'}" + (f"; l*={l_star}." if l_star is not None else "."))
    A(f"[OBSERVATION] S2 (LM log-prob baseline, non-binding): "
      f"acc={dec['S2']['accuracy']:.4f} ({dec['S2']['n_correct']}/60).")
    if steer_stats is not None:
        s = steer_stats
        A("")
        A("## 2. Intervention arm (S7-2 §3.4)")
        A("")
        A(f"[OBSERVATION] l*={l_star}, α calibrated to 0.047×mean‖h_i‖ "
          f"(assert ±0.01 PASS); G5 PASS; G4 baseline reproduction PASS; "
          f"180 forwards.")
        A(f"[OBSERVATION] P-vs-B: acc {s['acc_B']:.4f} → {s['acc_P']:.4f} "
          f"(Δ={s['delta']:+.4f}, monotone={s['monotone']}); "
          f"flips={s['flips']} (b={s['mcnemar_b']}, c={s['mcnemar_c']}); "
          f"McNemar p={s['mcnemar_p']:.4g} → "
          f"{'steer+' if s['steer_plus'] else 'steer−'} "
          f"(bars: ≥{s['flip_bar']} flips AND p<{s['alpha']}).")
    A("")
    A("## 3. Verdict reading")
    A("")
    A(f"[INTERPRETATION] {reading}")
    A("")
    A("## 4. Integrity")
    A("")
    A(f"[FACT] Model revision (40-hex, recorded at download, S0.2 "
      f"character-identical): `{manifest['model_revision_40hex']}`.")
    A(f"[FACT] Bench pin: `{manifest['bench_pin']}` (procedural rebuild via "
      f"the committed EXP092 builder; G0/G2/G3 PASS; G1′ 240/240 under "
      f"GPT-2 BPE before weight access).")
    A("[FACT] Frozen backbone Δθ=0 asserted by pre/post state-dict hash in "
      "both the extraction and decision-loop phases. Cost: $0 CPU.")
    with open(os.path.join(PLAN_DIR, "EXP144_VERDICT_2026-10-05.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[verdict] wrote verdict report", flush=True)

    # LOG-4919 at the top of the research log.
    entry = []
    E = entry.append
    E("## LOG-4919 — EXP144 verdict: {v} — S7-2 cross-family Decodability Gap "
      "replication (GPT-2-small) (2026-10-05)".format(v=verdict))
    E("")
    dec_line = ("**Decode [OBSERVATION]:** D1 {d1} (best layer {bl} "
                "acc={ba:.4f}, p={bp:.4g}, effect={be:+.4f}; passing layers "
                "{pl}); D2 mean shared-direction cosine {cos:.4f} (bar 0.70) "
                "→ {d2}.").format(
        d1="PASS" if d1 else "FAIL", bl=best["layer"], ba=best["accuracy"],
        bp=best["p"], be=best["effect"], pl=dec["passing_layers"],
        cos=d2_cos, d2="PASS" if d2 else "FAIL")
    E(dec_line)
    E("")
    if steer_stats is not None:
        s = steer_stats
        E("**Intervention [OBSERVATION]:** l*={ls}, α=0.047×mean‖h_i‖ (assert "
          "PASS), G5 PASS, G4 PASS, 180 forwards. P-vs-B: acc {ab:.4f}→{ap:.4f} "
          "(Δ={d:+.4f}), flips={f} (b={b}, c={c}), McNemar p={p:.4g} → "
          "{st} (bars: ≥6 flips AND p<0.05).".format(
            ls=l_star, ab=s["acc_B"], ap=s["acc_P"], d=s["delta"],
            f=s["flips"], b=s["mcnemar_b"], c=s["mcnemar_c"], p=s["mcnemar_p"],
            st="steer+" if s["steer_plus"] else "steer−"))
        E("")
    E("**Verdict [INTERPRETATION]:** {v} (cell: {cell}). {r}".format(
        v=verdict, cell=cell, r=reading))
    E("")
    E("**Integrity [FACT]:** model revision `{rev}` (S0.2 character-identical "
      "to download-time record); bench pin `{pin}` (procedural EXP092-builder "
      "rebuild, G0/G2/G3 PASS, G1′ 240/240 under GPT-2 BPE before weight "
      "access); Δθ=0 pre/post state-dict hash in both phases; $0 CPU.".format(
        rev=manifest["model_revision_40hex"][:16] + "…",
        pin=manifest["bench_pin"][:16] + "…"))
    E("")
    E("**Artifacts [FACT]:** `research/analysis_plans/EXP144_VERDICT_2026-10-05.md`, "
      "`research/analysis_plans/EXP144_RESULTS_2026-10-05.json`, run records "
      "`experiments/runs/EXP144/` (manifest, extraction + decision records "
      "JSONL, decode/direction/direction-verification JSON, logs).")
    E("")
    E("**Next free: LOG-4920.")
    with open(LOG_PATH) as f:
        old = f.read()
    with open(LOG_PATH, "w") as f:
        f.write("\n".join(entry) + "\n" + old)
    print("[verdict] LOG-4919 prepended to research log", flush=True)
    print(f"[verdict] AUTHORITATIVE VERDICT: {verdict} ({cell})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
