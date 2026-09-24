# S3-4 Cone-Arm-Only Flip-Stability Characterization — LOG-216 (2026-09-23)

**Role:** Track-6 data analyst. **Log:** LOG-216 (pre-assigned by the CEO).
**Scope:** REDUCED characterization of the S3-4 (SAH) candidate — the cone arm
only, on the archived EXP077 α grid. $0 CPU; archived JSONs only; no weights,
no forward passes, no GPU. No signed artifact modified.
**Deliverable twin:** `research/analysis_plans/S34_CONEARM_ANALYSIS_LOG216_2026-09-23.json`
(executor script: `research/analysis_plans/s34_log216_executor.py` — deterministic, no RNG).

**Standup headline:** The cone arm's α-grid profile is overwhelmingly no-flip
(57/60 items), but it is NOT zero-stable-flip: 3 items flip and every observed
flip persists (zero unstable flips). On headroom items the stable-flip rate is
2/24 = 8.3% (95% Wilson CI [2.3%, 25.8%]) — the cone-arm-only killer sub-check
(≈ 0 stable-flip rate → no operating range) does **not** fire. The Stage-0 gate
(bridge-vs-B_wrong stable-flip separation, p < 0.1) remains **uncomputable** —
the per-α records for those arms do not exist — so nothing here licenses the
GPU pilot.

---

## Law #15 answers (on record, pre-work)

1. **Q1:** Characterize the cone arm's flip-stability profile on the archived
   EXP077 α grid {0.25, 0.5, 1.0, 2.0} vs baseline C1, using the SAH candidate's
   pre-registered stable/unstable classifications.
2. **Q2:** CONTINUE/HOLD — informs whether SAH has an operating range on the
   cone arm. Does **not** license the GPU pilot (the Stage-0 gate needs the
   bridge-vs-B_wrong separation, which is uncomputable).
3. **Q3:** $0 — archived `exp077_instance_records.json` only; zero forward passes.
4. **Q4:** n/a — characterization, not an experiment; classifications are
   pre-registered from the candidate's definitions.

---

## Method (pre-registered definitions, applied as written)

Source [OBSERVATION]/[FACT]: `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`
(60 items; arms `C1` baseline, `C2_a025`…`C5_a200` cone at α = 0.25/0.5/1.0/2.0).

Classifications (from S3-4 §(a) of `SPRINT3_CANDIDATES_2026-09-23.md`):

- **flip** at α_k: `correct(α_k) ≠ correct(C1)` [DEFINITION].
- **STABLE flip** at α_k ∈ {0.25, 0.5, 1.0}: flip(α_k) AND `correct(α_{k+1}) = correct(α_k)` [DEFINITION].
- **UNSTABLE flip** at α_k ∈ {0.25, 0.5, 1.0}: flip(α_k) but not persisting [DEFINITION].
- **indeterminate-persistence** at α = 2.0: flip with no α_{k+1} to check; reported,
  not classified as stable [DEFINITION].
- **α\***: smallest α_k with a stable flip; 0 (abstain) if none [DEFINITION].
- **headroom item**: baseline C1 = wrong (room for a rescue flip) [DEFINITION].

**Measurement caveat** [OBSERVATION]/[FACT] (stated plainly, not worked around):
the archive records per-arm **correctness**, not the decision function
D(α) = argmax f(x; α·v̂) that SAH's definitions quantify. A correctness flip
implies a decision flip (sound), but wrong→wrong decision flips are invisible.
All counts below are therefore **lower bounds** on true decision-flip activity —
the operating range, if anything, is underestimated, never overestimated.

**Data-quality check** [OBSERVATION]/[FACT]: the archived `A_alpha_*` rescue
flags agree with the computed rescue cells (flip AND baseline-wrong AND
now-correct) on all 240 cells (60 items × 4 α). 0 mismatches — the binary
ledger is internally consistent on the cone arm.

---

## Results

### FACT layer — the stability profile (all counts from the archive)

| Quantity | Value |
|---|---|
| n items | 60 |
| Items with ≥1 **stable** flip | 3 (rate 5.0%, 95% Wilson CI [1.7%, 13.7%]) |
| Items with ≥1 **unstable** flip | 0 (rate 0.0%) |
| Items with flip only at α=2.0 (indeterminate-only) | 0 |
| Items with **no flip at all** | 57 (95.0%) |
| α = 0.25: flips | 0 |
| α = 0.5: flips 2, stable 2 | — |
| α = 1.0: flips 3, stable 3 | — |
| α = 2.0: flips 3 (indeterminate-persistence) | — |
| α\* distribution: 0.25 → 0, 0.5 → 2, 1.0 → 1, 2.0 → 0 | — |
| Abstentions (no stable flip anywhere) | 57 (95.0%) |

The three stable-flip items [OBSERVATION]/[FACT]:

- **Item 25** (Mercury, planet, headroom): wrong→correct at α=0.5, persists
  through 1.0 and 2.0. Stable at 0.5 and 1.0. α\* = 0.5. Direction: **rescue**.
- **Item 30** (Iron, element, headroom): flips to correct at α=1.0, persists at
  2.0. Stable at 1.0. α\* = 1.0. Direction: **rescue**.
- **Item 46** (Silver, element, non-headroom): baseline correct, flips to wrong
  at α=0.5, persists through 1.0 and 2.0. Stable at 0.5 and 1.0. α\* = 0.5.
  Direction: **damage**.

Structural note [OBSERVATION]: every flip ever observed on the cone arm
persisted — a step-function trajectory (flip once, stay flipped). Zero
unstable flips, zero indeterminate-only items. The cone arm does not exhibit
the flip-flop pattern the candidate associates with the B_wrong "marginal
regime" signature.

Corroboration [OBSERVATION]/[FACT]: the aggregate in `exp077_results.json`
(radial arm, same grid) shows ΔM = 0 at α = 0.25/0.5 and +0.0167 (≈ +1 net
item of 60) at α = 1.0/2.0, p = 1.0 — consistent with the per-item profile
(near-total no-flip with a 3-item stable residue).

### Killer-box sub-check (the computable part)

The candidate's killer box: **stable-flip rate ≈ 0 on headroom items →
the control has no operating range → Not supported.**

Cone-arm-only result [OBSERVATION]/[FACT]:

- Headroom items: 24 of 60. Stable-flip rate = 2/24 = **8.3%**
  (95% Wilson CI [2.3%, 25.8%]). Both stable flips are rescues.
- Non-headroom items: 36 of 60. Stable-flip rate = 1/36 = 2.8%
  (the single item is the stable-damage case, item 46).

**Outcome of the sub-check** [INTERPRETATION]: the ≈ 0 kill condition is **not
met on the cone arm** — the point estimate is nonzero and the CI's lower bound
sits above zero. Two headroom items demonstrate exactly the SAH operating
behavior (flip to correct at a threshold α and persist). The cone arm has a
small but real operating range; the "no operating range" verdict does not
fire on this arm.

### INFERENCE layer

- The profile is sparse but structured: SAH's α\* rule would abstain on 57/60
  items and act on 3 — and its 2 headroom actions would both be stable rescues,
  its 1 non-headroom action a stable damage. [INTERPRETATION] On this arm the
  stability rule's selectivity is high (few triggers), and every trigger it did
  make persisted.
- The zero-unstable-flip count cuts both ways: it means no observed
  "marginal-regime" flip-flop on the cone arm (good for the control's
  selectivity), but it also means the candidate's claimed unstable-flip
  signature has **no positive example in this archive** on this arm — the
  signature's unstable half is empirically unexercised here. [INTERPRETATION]
- Because correctness flips are a lower bound, the true decision-flip profile
  could only be richer (wrong→wrong flips invisible). The 8.3% headroom rate is
  a floor, not a ceiling. [INTERPRETATION]

### HYPOTHESIS layer

- [HYPOTHESIS] The step-function (flip-once-persist) pattern on the 3 flipping
  items is consistent with SAH's core claim that per-instance distance-to-boundary
  creates a threshold α per item — but n = 3 triggering items cannot support a
  mechanism claim; it only keeps the operating-range question alive.
- [HYPOTHESIS] The complete absence of flips at α = 0.25 (0/60) is consistent
  with undershoot at small α, but is equally consistent with the cone arm simply
  being weak at that strength; the archive cannot distinguish these.

### SPECULATION layer

- [SPECULATION] If the full α-grid (0.125…4.0, including persistence steps at
  both ends) were ever run, the currently indeterminate α=2.0 flips would become
  classifiable, and the 57 abstaining items might reveal threshold behavior at
  α > 2.0 — but that is a live-GPU question and is **not licensed by this
  analysis**.

---

## Evidentiary verdicts (the five permitted categories only)

- **Cone-arm killer sub-check** ("≈ 0 stable-flip rate on headroom items"):
  condition not met (8.3%, CI [2.3%, 25.8%]) → this arm alone does not trigger
  the SAH "no operating range" kill. [INTERPRETATION] Verdict on the sub-check:
  **Not supported** (for the kill claim on the cone arm).
- **SAH overall**: this analysis is a one-arm characterization, not the Stage-0
  gate → **Underdetermined**. The verdict on SAH stays exactly where the
  feasibility inventory left it: waiting on the bridge-vs-B_wrong separation,
  which requires per-α records that do not exist in the archive.
- **The unstable-flip signature on this arm**: zero observed unstable flips —
  **Inconclusive** (the signature's unstable half is unexercised here, neither
  confirmed nor refuted).

---

## Explicit limits (what this analysis CANNOT do — stated, not worked around)

1. **The Stage-0 gate is uncomputable.** `C7_Bwrong` and `C8_bridge` are
   single-arm per-instance booleans; per-α per-instance outcomes for these arms
   are **absent** (LOG-208 Check 3). The bridge-vs-B_wrong stable-flip
   separation (p < 0.1) cannot be computed from any archive.
2. **Binary outcomes only.** No margins, no logits, no per-item decision labels.
   What that forbids: true D(α) flip classification, any margin-regime analysis,
   and any claim about wrong→wrong decision flips.
3. **Reduced scope.** Cone arm (C2–C5) vs baseline C1 only. `C6_offset`,
   `C9_cone`, `C10_control` were excluded per the task.
4. **Characterization, not a verdict on SAH.** The classifications were
   pre-registered from the candidate's definitions; nothing here licenses the
   GPU pilot gate or any live experiment.

---

## Files

- Report (this file): `research/analysis_plans/S34_CONEARM_ANALYSIS_LOG216_2026-09-23.md`
- Machine-readable JSON twin (per-item classifications + aggregates + limits):
  `research/analysis_plans/S34_CONEARM_ANALYSIS_LOG216_2026-09-23.json`
- Executor: `research/analysis_plans/s34_log216_executor.py` (deterministic;
  $0 CPU; no weights, no forward passes; 0 mismatches on the rescue-flag
  consistency check).

## Recommended follow-ups (for the parent/CEO — none are licensed yet)

- The bridge/B_wrong per-α separation remains the binding Stage-0 gate and can
  only be produced by live GPU work (360 passes ≈ 0.005 T4-h per the candidate's
  own estimate) under a Law #14-signed plan. This analysis does not substitute
  for it.
- The full S3-4 Stage-0 gate as written needs all arms; the cone-arm sub-check
  clearing "≈ 0" is a necessary-but-insufficient condition and changes no
  licensing decision.

*End of LOG-216 analysis. Characterized, not judged.*
