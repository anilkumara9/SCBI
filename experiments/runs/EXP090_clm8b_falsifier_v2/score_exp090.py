"""EXP090 scoring — zero-shot cosine state-vs-option scoring + §7.1 verdict logic.

Signed protocol: experiments/protocols/EXP090_CLM8B_ADAPTATION_V2_PREREG_SIGNED.md
(§6 scoring rule + G4 instrument gate; §7 registered bar; §7.1 positional
diagnostic; §8 falsification/invalidity).

Pipeline:
  1. Load embeddings (state, actA, actC) from exp090_embeddings.npz.
  2. cosines: 120 values (60 state–A, 60 state–C).
  3. G4 instrument-health gate: max − min < 1e-4 → RUN-INVALID (never KILL).
  4. Per-item decision = argmax(cosA, cosC); exact float ties break toward C
     (the foil — conservative) and are counted.
  5. Verdict per the TOTAL §7.1 tree:
       - aggregate ≥ 38/60 AND acc_Afirst > 0.5 AND acc_Cfirst > 0.5 → CONTINUE
       - aggregate ≤ 37/60                                            → KILL
       - aggregate ≥ 38/60 but a split fails strict >0.5 (incl. exactly
         0.5 or opposite tilts)                                       → PIVOT

Pure numpy — no torch required.
"""

import argparse
import json
import math
import os
import sys

import numpy as np

BAR_CONTINUE = 38   # ≥ 38/60 → CONTINUE (subject to §7.1); P(X≥38)=0.0260
N = 60
G4_DEAF_EPS = 1e-4  # signed-protocol §6 G4


class RunInvalid(Exception):
    """G4 instrument deafness → RUN-INVALID (withheld, never a verdict)."""


def cosine(a, b):
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def score_all(state, actA, actC):
    """Return (cosA, cosC) arrays of length N."""
    cosA = np.array([cosine(s, a) for s, a in zip(state, actA)])
    cosC = np.array([cosine(s, c) for s, c in zip(state, actC)])
    return cosA, cosC


def exact_binomial_upper_tail(n_correct, n=N, p=0.5):
    """Exact P(X ≥ n_correct | n, p) via math.comb (no approximation)."""
    return sum(math.comb(n, k) for k in range(n_correct, n + 1)) * (p ** n)


def adjudicate(per_item_correct, phrasing, cosines):
    """Apply the §7.1 TOTAL decision tree. Pure function (fully testable).

    per_item_correct: list/array of N bools (True = argmax chose A).
    phrasing: list/array of N "A-first"/"C-first" strings.
    cosines: array of 2N cosine values (state–A then state–C, or interleaved —
             only the spread matters for G4).
    Returns a dict with verdict, counts, splits, and diagnostics.
    """
    per_item_correct = [bool(x) for x in per_item_correct]
    phrasing = list(phrasing)
    cosines = np.asarray(cosines, dtype=np.float64)
    assert len(per_item_correct) == N and len(phrasing) == N, "need exactly N=60"

    # G4 instrument-health gate FIRST: a deaf instrument yields RUN-INVALID,
    # never KILL (§6 F1).
    spread = float(np.max(cosines) - np.min(cosines))
    if spread < G4_DEAF_EPS:
        raise RunInvalid(
            f"G4: instrument deaf — max−min cosine = {spread:.3e} < {G4_DEAF_EPS} "
            f"over {len(cosines)} values. RUN-INVALID (withheld, not a verdict).")

    n_correct = int(sum(per_item_correct))
    idx_a = [i for i, ph in enumerate(phrasing) if ph == "A-first"]
    idx_c = [i for i, ph in enumerate(phrasing) if ph == "C-first"]
    assert len(idx_a) == 30 and len(idx_c) == 30, "G3 violated in scorer input"
    acc_a = sum(per_item_correct[i] for i in idx_a) / 30.0
    acc_c = sum(per_item_correct[i] for i in idx_c) / 30.0

    if n_correct < BAR_CONTINUE:  # ≤ 37 → KILL (§7)
        verdict = "KILL"
    elif n_correct >= BAR_CONTINUE and acc_a > 0.5 and acc_c > 0.5:
        verdict = "CONTINUE"                  # clean §7.1 pass
    else:
        # Aggregate ≥ 38 but a split fails strict >0.5 (incl. exactly 0.5 or
        # opposite tilts) → PIVOT; CONTINUE withheld (§7.1 boundary rule F2).
        verdict = "PIVOT"

    return {
        "verdict": verdict,
        "n_correct": n_correct,
        "n_total": N,
        "accuracy": n_correct / N,
        "acc_Afirst": acc_a,
        "acc_Cfirst": acc_c,
        "binomial_p_upper_tail": exact_binomial_upper_tail(n_correct),
        "g4_spread": spread,
    }


def decide_from_embeddings(emb_path):
    """Full scoring pass over an embeddings bundle. Returns the report dict."""
    z = np.load(emb_path, allow_pickle=True)
    state, actA, actC = z["state"], z["actA"], z["actC"]
    ids = [str(x) for x in z["ids"]]
    phrasing = [str(x) for x in z["phrasing"]]
    assert state.shape[0] == actA.shape[0] == actC.shape[0] == N, \
        f"embedding count != {N}"

    cosA, cosC = score_all(state, actA, actC)
    per_item_correct, ties = [], 0
    margins = []
    for ca, cc in zip(cosA, cosC):
        margins.append(abs(float(ca) - float(cc)))
        if ca == cc:            # exact float tie → C (foil), conservative
            ties += 1
            per_item_correct.append(False)
        else:
            per_item_correct.append(bool(ca > cc))

    cosines = np.concatenate([cosA, cosC])
    result = adjudicate(per_item_correct, phrasing, cosines)
    result.update({
        "ties_broken_toward_foil": ties,
        "margin_mean": float(np.mean(margins)),
        "margin_median": float(np.median(margins)),
        "margin_min": float(np.min(margins)),
        "margin_max": float(np.max(margins)),
        "cosA_mean": float(np.mean(cosA)),
        "cosC_mean": float(np.mean(cosC)),
        "per_item": [
            {"id": i_, "correct": c, "phrasing": ph,
             "cosA": float(ca), "cosC": float(cc)}
            for i_, c, ph, ca, cc in zip(ids, per_item_correct, phrasing, cosA, cosC)
        ],
    })
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="EXP090 zero-shot scoring")
    ap.add_argument("--embeddings", required=True,
                    help="path to exp090_embeddings.npz")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args(argv)
    try:
        report = decide_from_embeddings(args.embeddings)
    except RunInvalid as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3
    # F1 (Law #14 LOG-345, carried forward): stamp execution mode into the
    # report. The mode comes from the extraction meta colocated with the
    # embeddings bundle (written by extract_mock/extract_real);
    # absent meta → "unknown".
    meta_path = os.path.join(os.path.dirname(os.path.abspath(args.embeddings)),
                             "exp090_extraction_meta.json")
    mode = "unknown"
    if os.path.isfile(meta_path):
        try:
            with open(meta_path) as f:
                mode = json.load(f).get("mode", "unknown")
        except (OSError, ValueError):
            mode = "unknown"
    report["mode"] = mode
    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, "exp090_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    r = report
    print(f"n_correct={r['n_correct']}/60  acc={r['accuracy']:.4f}  "
          f"acc_Afirst={r['acc_Afirst']:.4f}  acc_Cfirst={r['acc_Cfirst']:.4f}  "
          f"p_upper={r['binomial_p_upper_tail']:.6f}  VERDICT={r['verdict']}")
    print(f"report written: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
