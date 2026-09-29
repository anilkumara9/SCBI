# Independent exact-artifact verdict review — EXP121 (H19/PTTSC-SUFFIX)

**Lane:** independent verdict review, LOG-4645 pre-assigned · **Date:** 2026-09-29
**Scope:** recompute the EXP121 verdict from the exact raw artifacts, not the lane's report.
**Verdict: QUALIFY — RUN-INVALID stands, one documentation caveat.**

## 1. Protocol bars extracted (post-FIX-1 pre-reg, `EXP_PREREG_H19_PTTSCSUFFIX_2026-09-29.md`)

- G1 (per arm per item, §3.6): mean post-softmax mass on (t1, t2) ≥ 0.01 (H6 rule).
- Item valid (§3.8): planner-valid AND plan-arm G1 pass AND baseline-arm G1 pass.
- Elicitation-failure gate (§3.8): n_valid < 48/60 → RUN-INVALID. Not a verdict.
- Baseline variation gate: <2 distinct or minority <3 → RUN-INVALID.
- Baseline reproduction: 60/60 vs EXP112 archived readout, else RUN-INVALID.

## 2. Independent recompute from raw records

Recomputed from `experiments/runs/EXP121_pttscsuffix/out/exp121_per_item.json`
(60 records; lane flags cross-checked field-by-field — zero mismatches):

| Check | Lane claim | Independent recompute |
|---|---|---|
| n_valid (G1 rule) | 38/60 | **38/60** ✓ |
| planner-invalid items | 0 | 0 ✓ |
| plan-arm G1 failures | 22 | 22 ✓ (failing items {15,17,19,21,23,26,27,28,38,43,46,48,50,51,52,53,54,55,56,57,58,59}, mass 0.000142–0.008571) |
| baseline-arm G1 failures | 0 | 0 ✓ (mass range 0.068–0.568) |
| G1 invariance (stricter mean≥0.01 reading = mass≥0.02) | 30/60 | **30/60** ✓ — gate fires under both readings |
| Baseline variation | 2 distinct / minority 27 | 2 distinct / minority 27 (E2=33, E1=27) ✓ — gate passes |
| Baseline reproduction vs `EXP112_hdildr/out/exp112_per_item.json` archived `readout` | 0/60 mismatches | **0/60** ✓ |
| Phase-0b probe items valid in full run | 10/10 | 10/10 ✓ |
| Planner-valid | 60/60 | 60/60 ✓ |

Elicitation-failure gate: 38 < 48 → **RUN-INVALID fires.** Also fires under the
stricter phrasing (30 < 48). The verdict is invariant to the G1 mean-vs-sum phrasing.

## 3. Integrity pins

- Backbone Δθ=0: worksheet pins `backbone_pre == backbone_post == backbone_pin_expected`
  = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331) ✓
- Raw-artifact hash pins (result.json worksheet): `exp121_generations.json`,
  `exp121_forwards.json`, `exp121_precheck.json`, `exp121_per_item.json` —
  **all four recomputed SHA-256 match on disk** ✓
- `artifact_hashes.execute_script` (result.json) does NOT match the on-disk script.
  Cause disclosed in the report (§4 defect): `finalize()` truncated the script to
  0 bytes before hashing. The lane reconstructed the script and recorded the
  corrected hash `58f12ba52b93c34422c684b11d9c740025f48daebc95d3a90de55f3a48cc7113`.
  **Independently verified here:** (a) on-disk script SHA-256 equals the corrected
  hash ✓; (b) the script's code objects are **bytecode-identical** to
  `__pycache__/exp121_execute.cpython-312.pyc` compiled from the executed version
  (filename-agnostic recursive comparison, top-level bytecode equal) ✓.
  The reconstruction claim holds. Result JSON left append-only; correction recorded
  in the report. No impact on the verdict.
- Deterministic re-read ×2: `reparse_byte_identical: True` ✓
- Generations: 60; forwards: 120; exceptions: 0 ✓

## 4. Report p-value check (binding defect class, EXP120)

No McNemar table was computed — the falsification tree terminates at the n_valid
gate before any metric is read (Law #9). The report contains **no p-value**,
handwritten or otherwise. The defect class is moot here. ✓

## 5. LOG-4644 check

Exactly one `## LOG-4644` entry in `reports/research_log.md`, the next-free number
after LOG-4643. Substance matches the artifacts (n_valid=38, gates, defects,
pins, honesty fence). ✓

## 6. Documentation caveat (the QUALIFY)

The report and LOG-4644 both state: *"Two independent full runs reproduced
n_valid = 38 exactly."* This sentence is **not verifiable from retained
artifacts** — only the final run's records exist on disk; attempt 2's 60
generation records (written before the TypeError crash) were overwritten by the
final fresh run and not retained. The count's stability IS artifact-supported via
the deterministic re-read ×2 byte-identical check (`reparse_byte_identical:
True`, verified above), but the "two independent full runs" phrasing goes beyond
what the retained records can evidence. It should be corrected (append-only
erratum) to the verified claim, or the second run's records must be produced.
This caveat does not touch the verdict logic, any gate, or any number supporting
the verdict.

Secondary note (not a caveat): attempt 2's superseded generation records were not
retained (Law #8 spirit); the attempts are fully disclosed in the report and
LOG-4644, and no metric was ever read from them, so no Law #9 exposure.

## 7. Adjudication

- The lane's verdict **RUN-INVALID (elicitation-failure gate, n_valid=38/60 < 48)**
  is reproduced exactly from the raw artifacts under the pinned G1 rule, and is
  invariant to the licensed mean-vs-sum phrasing.
- All integrity pins hold (Δθ=0, raw records hash-pinned and matching,
  baseline reproduction 60/60, no metric read).
- **QUALIFY: the RUN-INVALID verdict stands**, with one documentation caveat
  (§6) requiring an append-only correction.
- Scientific consequence (unchanged): H11's planning question remains **untested
  on the logit channel** — third distinct apparatus failure mode
  (EXP117: generation channel; EXP119: tokenization identity; EXP121: plan-arm
  G1 mass collapse). Zero decision data.
