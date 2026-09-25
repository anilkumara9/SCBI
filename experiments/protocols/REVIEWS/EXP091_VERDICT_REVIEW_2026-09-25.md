# EXP091 Independent Verdict Review — ADOPT (2026-09-25)

**Reviewer:** Independent Verdict Reviewer (reports directly to the founder; binding).
**Target:** `experiments/runs/EXP091_clm8b_falsifier_v3/out/` — real execution of the signed
EXP091 protocol (digest `747bb6a5722e8478f57b645cad93b9fd54902271bd3f8a64da9a4e24236f417b`).
**Runner's verdict under review:** KILL (31/60, p=0.4487), logged LOG-361.
**Verdict on the verdict: ADOPT.**

---

## 1. Chain of custody

- Signed protocol: `experiments/protocols/EXP091_CLM8B_ADAPTATION_V3_PREREG_SIGNED.md`
  (LOG-357; Law #14 draft review SIGN LOG-356; bundle review SIGN LOG-359;
  CEO execution clearance LOG-360, CPU-only $0).
- Execution artifacts reviewed read-only: `exp091_report.json`, `exp091_embeddings.npz`,
  `exp091_extraction_meta.json`, `exp091_extraction_log.txt`. No weights, artifacts, or
  signed files modified by this review.

## 2. Independent recomputation from per-item data (all 60 items)

Recomputed by this reviewer from `report.per_item` (not trusted from summary fields):

| Quantity | Runner-reported | Independently recomputed | Match |
|---|---|---|---|
| n_correct | 31 | 31 | yes |
| n_total | 60 | 60 | yes |
| accuracy | 0.5166666666666667 | 31/60 = 0.5166666666666667 | yes |
| acc_Afirst (30 items) | 0.5 | 15/30 = 0.5 | yes |
| acc_Cfirst (30 items) | 0.5333333333333333 | 16/30 = 0.5333333333333333 | yes |
| binomial upper-tail P(X≥31\|60,0.5) | 0.44871091349571524 | exact via math.comb = 0.44871091349571524 | yes (bit-identical) |
| G4 spread (max−min over 120 cosines) | 0.0802726149559021 | 0.0802726149559021 | yes |
| ties_broken_toward_foil | 0 | 0 exact cosA==cosC equalities | yes |
| margin mean / median | 0.0006809572378794353 / 0.0007813870906829834 | identical | yes |
| margin min / max | 4.565715789794922e-05 / 0.0013840794563293457 | identical | yes |
| mode | "real" | "real" | yes |

Scoring-rule consistency (§5: `A`=target invariant across phrasings; decision =
argmax(score(A), score(C)); ties → C deterministically): `correct ⟺ cosA > cosC`
held for all 60 items; 0 ties; no inconsistency.

## 3. §7.1 TOTAL decision-tree mapping

- Aggregate 31/60 ≤ 37/60 → **KILL**, "regardless of the split". CONTINUE requires
  ≥38/60 (not met); PIVOT applies only to aggregate-≥38 outcomes with failed/tied
  splits (not met). No other branch is reachable.
- No RUN-INVALID condition fired: G2 hash match (Δθ=0), §6 archive-hash pin pass,
  G1' pass at build time and extraction time (240/240 in-prompt single-token, real
  tokenizer), G3 30/30 phrasing balance, N=60, and G4 spread 0.0803 ≫ 1e-4 bar
  (instrument responsive, not deaf — G4 explicitly does not convert this into
  RUN-INVALID).

## 4. Guard/pin/artifact verification

- `mode`: "real" (execution-log and meta agree; not a mock verdict).
- G1': pass, 240/240 in-prompt occurrences single-token (extraction log +
  `g1prime_verification.json` binding).
- G2: pre/post hash `ec276abe3902fab0…` matches the LOG-331 frozen-state hash prefix;
  Δθ=0 verified; `model.eval()`, `requires_grad_(False)` recorded in the extraction log.
- G3: 30/30 asserted on the real benchmark builder (independently confirmed 30 A-first /
  30 C-first in per-item data).
- Provenance: §6 archive hash pin asserted OK at extraction (build-time record
  `47281cd3…0585` verified at LOG-359).
- Embeddings: `exp091_embeddings.npz` contains `state` (60,1024), `actA` (60,1024),
  `actC` (60,1024) float32 — 60 items × 1024 dims as registered; zero NaN, zero inf,
  zero all-zero rows in all three arrays. 180 forward passes (60 state + 60 A + 60 C)
  recorded in the extraction log, consistent with the §9 budget.

## 5. Pathology screen (beyond the tree)

- No NaNs or infs in any cosine or embedding array.
- Cosines not degenerate: 50 unique cosA values, 50 unique cosC values over 60 items
  (repeats expected — the same action-text embeddings recur across items sharing an
  entity; e.g. Mars appears 42 times).
- cosA mean 0.1902, cosC mean 0.1905 — means separated by ~3e-4, consistent with the
  observed near-chance accuracy; no hidden structure contradicting the KILL.
- Decision margins are noise-scale (max |Δcos| = 1.38e-3): exactly the profile of a
  signal-free instrument, not a measurement defect. G4 (0.0803) shows the instrument
  is responsive; the verdict is a genuine null, not deafness.
- Nothing found that the tree fails to cover; no problems invented.

## 6. Licensed interpretation boundary

The KILL licenses exactly what the protocol's §7 table states: the free-lunch version
dies — frozen Pythia-410m/layer-20 geometry carries no exploitable zero-shot decision
signal under this cosine-scoring instrument; the adaptation is shelved pending training
resources. Per the protocol's own [INTERPRETATION, not licensed inference] note, this
instrument cannot attribute CLM-8B's reported capability to its head training vs any
other cause. No capability, mechanism, or superhuman-intelligence claim is licensed by
this outcome; the experiment tested the falsifier question and answered it.

## 7. Verdict

**ADOPT.** The runner's KILL verdict is what the signed protocol's §7.1 tree licenses:
31/60 ≤ 37/60, all summary numbers independently recomputed bit-identical from per-item
data, every guard and pin verified, no RUN-INVALID condition, no measurement pathology.
No defect blocks adoption. The CLM-8B free-lunch hypothesis (zero-shot) is killed on
the record as designed.

*Independent reviewer, 2026-09-25. All reads read-only; only this review file and the
LOG-362 entry were written.*
