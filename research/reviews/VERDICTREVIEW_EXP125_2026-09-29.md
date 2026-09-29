# VERDICTREVIEW EXP125 — Independent exact-artifact review — 2026-09-29

**Lane:** LOG-4681 (pre-assigned). **Report:** `research/experiments/EXP125_HONESTYGEN4_REPORT_2026-09-29.md`.
**Protocol:** `research/prereg/EXP_PREREG_H22_HONESTYGEN4_2026-09-29.md`
(signed sha256 `276b4db84e8c3442dc2859ab68ad5312223b91ebc6c28b237fafccf7ecf92820`
— verified before any verification step below).
**Raw artifacts:** `experiments/runs/EXP125_honestygen4/out/`.
**Scope:** $0 CPU, read-only (this review made no model contact beyond tokenizer-only
decoding of public bench text; transformers 5.17.0 installed user-locally for the
tokenizer check). I did not execute this run; every number below was reimplemented from
the protocol text, never by reusing the executor's functions.
**Verdict: BIND — with one minor observation (non-verdict-bearing).**

---

## 1. Hash pins (all recomputed)

| Artifact | Expected | Observed | Match |
|---|---|---|---|
| `exp125_bench4.json` | `4995545cae3b662567166d1549952e304d19ced014431bb48637f4b5e27c6cf7` | same | YES |
| protocol post-fix | `276b4db84e8c3442dc2859ab68ad5312223b91ebc6c28b237fafccf7ecf92820` | same | YES |
| `exp125_per_item.json` | `27a3744d147ebde390f458a3a3d3d01ae2578433566807417c1eba4225ba367b` | same | YES |
| `exp125_embeddings.npz` | `c12defa52589154df25a5365c69b8566ed4a1b44a5e29c9f2fef7be40e421082` | same | YES |
| worksheet pins `backbone_pre` / `backbone_post` | `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` | same/same | YES |

Δθ=0: pre and post pins identical and equal to the LOG-331 pin. Worksheet prereg pin
matches the signed value — the protocol executed was the protocol signed.

---

## 2. Fidelity re-derived independently: 28/60 ✓

Rule (from protocol text): fidelity_i = 1 iff `decision_i == readout_i`.
From `exp125_per_item.json` (60 records): **28/60 = 0.4667**. Cells balanced 15/15/15/15.
Per-cell: A-first/original 11/15, A-first/flipped 9/15, C-first/original 5/15,
C-first/flipped 3/15 — matches the report §5. Ties: 0 readout, 0 decision.

Cosine recheck from raw embeddings (`state` 60×1024, `option` 120×1024 float32):
recomputed decision (argmax of float32 cosines) agrees with the stored `decision`
**60/60**. The stored cosine floats reproduce to ~7 significant figures (item-0:
0.2038810683 vs my 0.2038810700, ~1.6e-9 ULP-level difference from reduction order —
see observation below). What the verdict reads — the argmax — agrees everywhere.

**Bars bind verbatim (H6's signed bars, Law #4):** 28/60 ∈ ≤33/60 → KILL. The count
regions are disjoint and exhaustive per the Law-#14 review; no ambiguity.

---

## 3. Guards re-verified from raw artifacts

| Guard | Bar | Independent value | Holds |
|---|---|---|---|
| G4 instrument-health (cosine spread, 120 values) | ≥ 1e-4 | 0.1381252199… | YES |
| G1 mass guard (mean) | ≥ 0.01 | 0.2323426825… (min 0.0441552606…, max 0.6369767237…, frac ≥0.01 = 1.0) | YES |
| G2 variation guard | distinct ≥ 2, minority ≥ 3 | readouts E1=21, E2=39, minority 21 | YES |
| `[-3:]` identity (real Pythia-410m tokenizer, tokenizer-only) | 60/60 = `[32, 37741, 27]` | **60/60** (decode: `? Answer:`) | YES |
| byte-exact decomposition `prompt == premise + QUESTION_SUFFIX` | 60/60 | 60/60 | YES |
| single-token option texts (t1/t2 scalar ints, 120/120) | 120/120 | 120/120 | YES |

All guards passed → this is a verdict (KILL), not an apparatus failure. Law #9 honored:
no metric number existed in the report before the guard walk completes.

---

## 4. P-values re-derived (exact binomial, scipy, ≥10 decimals)

| Quantity | Executor | Independent | Match |
|---|---|---|---|
| P(X ≥ 42 \| 60, 0.5) | 0.0013352181 | 0.0013352181… | YES |
| P(X ≤ 57 \| 60, 0.99) | 0.0224201648 | 0.0224201647… | YES |
| P(X ≥ 41 \| 60, 0.5) | 0.0031088013 | 0.0031088013… | YES |
| P(X ≥ 33 \| 60, 0.5) | 0.2594790016 | 0.2594790015… | YES |
| P(X ≤ 23 \| 60, 0.5) | 0.0462304905 | 0.0462304905… | YES |
| P(X ≥ 28 \| 60, 0.5) observed one-sided | 0.7405209984 | 0.7405209984… | YES |

Defect class 1 clean: all p-values executor-computed and printed, and my independent
recomputation agrees to the printed precision. The systematic-misreporting diagnostic
(≤ 23/60) was correctly NOT triggered at 28/60 — verified.

---

## 5. Honest-frame check

- Report §1/§6 state: EXP112's bench-1 HELD stands per Law #8, reclassified
  bench-specific (Law #11 two-layer tagging); the honesty readout is a one-bench
  phenomenon. §6 states no cross-bench fidelity comparison is licensed, and the
  report makes none beyond the tagging statement. ✓
- The bench-2 line stays dead — explicitly restated in §1. No rescue, no rerun. ✓
- No hypothesis rewording (Law #4): the report §6 declares none occurred. ✓
- §4 protocol: KILL never followed by larger-n re-test, different layer, different
  carrier, third bench, or re-read. The report honors it. ✓
- Descriptive per-cell asymmetry (A-first 20/30 vs C-first 8/30) is correctly tagged
  [OBSERVATION], recorded for future separately pre-registered work, and changes no
  verdict. ✓

---

## 6. Observation (non-verdict-bearing)

The report §4 claims the execution lane's own post-hoc check recomputed the item-0
cosine pair "bit-exact". My independent float32 recomputation from the raw embeddings
agrees to ~7 significant figures but differs at the ULP level (~1.6e-9; reduction-order
artifact of torch vs numpy float32 cosine). This does not affect the verdict in any way:
the metric reads only the argmax (decision), which agrees 60/60, and fidelity is
re-derived directly from the stored decision/readout fields (28/60). The claim is a
documentation precision overreach in a post-hoc sentence, not a defect in the verdict
path. No erratum required.

---

## 7. Binding determination

The KILL follows mechanically from the signed, verbatim-carried H6 bars:
28/60 ∈ ≤33/60, all guards pass, Δθ=0, hashes pinned before verdict, p-values
executor-computed. H22's honesty-generality hypothesis at logit level is dead;
EXP112's bench-1 HELD stands, reclassified bench-specific. **Verdict: BIND.**
