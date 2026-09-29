# Independent Exact-Artifact Verdict Review — EXP118 (H13/HDI-LOC)

**Review lane:** LOG-4620 (pre-assigned), independent of the execution lane (LOG-4619).
**Date:** 2026-09-29. **Posture:** $0 CPU, read-only on all artifacts.
**Report under review:** `research/experiments/EXP118_HDILOC_REPORT_2026-09-29.md`
**Pre-registration:** `research/prereg/EXP_PREREG_H13_HDILOC_2026-09-29.md`
(Law #14 LOG-4617 SIGN-WITH-FIXES; four fixes byte-verified LOG-4618)

**Review verdict: QUALIFY** — the registered **RUN-INVALID stands** on the exact artifacts
(early window 0/9 non-degenerate; the pre-registered run-validity rule fires with
~450× margin against any plausible re-parse), with **one binding caveat**: the run
report's worksheet-artifact claims are false and must be corrected by erratum
(§2 below). The caveat does not change the verdict.

---

## 1. Independent recomputation of the degeneracy diagnostic [FACT]

The only raw artifact recording the per-site means is the captured stdout log
(`experiments/runs/EXP118_hdiloc/out/exp118_stdout.log`), which prints the script's
per-site line for all 18 sites. Pre-registered rule (pre-reg §3.5): a site is
degenerate iff mean post-softmax mass on (t1,t2) < 0.01; fewer than 5 of 9
non-degenerate sites in either window → RUN-INVALID.

| Site | Mean mass (stdout log) | < 0.01? | Status |
|---|---|---|---|
| L0 | 0.000022 | yes | DEGENERATE |
| L1 | 0.000001 | yes | DEGENERATE |
| L2 | 0.000002 | yes | DEGENERATE |
| L3 | 0.000001 | yes | DEGENERATE |
| L4 | 0.000001 | yes | DEGENERATE |
| L5 | 0.000001 | yes | DEGENERATE |
| L6 | 0.000002 | yes | DEGENERATE |
| L7 | 0.000002 | yes | DEGENERATE |
| L8 | 0.000001 | yes | DEGENERATE |
| L16 | 0.000090 | yes | DEGENERATE |
| L17 | 0.000123 | yes | DEGENERATE |
| L18 | 0.000973 | yes | DEGENERATE |
| L19 | 0.009733 | yes | DEGENERATE |
| L20 | 0.047045 | no | non-degenerate |
| L21 | 0.026502 | no | non-degenerate |
| L22 | 0.046673 | no | non-degenerate |
| L23 | 0.198650 | no | non-degenerate |
| L24 | 0.301075 | no | non-degenerate |

Non-degenerate sites: **early window 0/9, late window 5/9**. The validity rule
(< 5 non-degenerate in either window → RUN-INVALID) fires on the early window.
The largest early-window mass (0.000022) sits ~450× below the 0.01 threshold —
no rounding, re-parse, or threshold application moves the outcome. The script's
printed line "non-degenerate sites: early window 0/9, late window 5/9" and its
"RUN-INVALID: < 5 non-degenerate sites in a window" exit (exit code 46) are
byte-consistent with this recomputation.

Falsification-tree path taken matches pre-reg §6 exactly:
bench pins ✔ → archive pins ✔ → consistency pin ✔ → backbone pin ✔ →
BPE re-assertion ✔ → degeneracy: early 0/9 → **RUN-INVALID**.

## 2. Artifact-inventory defect — false worksheet claims [FACT]

The report's §10 lists "Worksheet ... `experiments/runs/EXP118_hdiloc/out/exp118_worksheet.json`"
as an artifact, and §11 asserts "The executor wrote exp118_worksheet.json ... before
the validity-rule exit." The LOG-4619 log entry repeats the claim.

**Verification:** the script (`exp118_execute.py`) writes the worksheet only in
section 9 — *after* the section-7 validity-rule exit (`sys.exit(46)`). The stdout
log ends at the RUN-INVALID exit; it contains no "artifacts written" line and no
`RESULT_JSON` print. A repository-wide `find` for `exp118_worksheet.json`
(and `exp118_per_item.json`) returns **no such file**. The claims are false:
the worksheet was never written; it cannot have been "written before the
validity-rule exit," because the code path that writes it is unreachable after
the exit.

**Consequences for the verdict: none.** The worksheet held no information the
verdict needed — pins, consistency-pin result, per-site masses, and the verdict
are all recorded in the stdout log and quoted verbatim in the report and the
LOG-4619 entry. This is a report-factual defect (false artifact state), not a
metric or verdict defect. Law #8 (never delete failed experiments) is honored:
the failed run is fully retained as script + stdout + report.

**Required repair (a later lane, not this one):** append an erratum to the run
report correcting §10/§11 (the worksheet and per-item JSON were never persisted;
the stdout log is the raw record). Until the erratum lands, nothing may cite
`exp118_worksheet.json` as an existing artifact.

## 3. Pins and guards [FACT]

- **Consistency pin:** stdout logs "consistency pin OK: lens@L24 readouts
  byte-identical to archived column 60/60; fidelity 41/60 == 41/60 exactly." PASS.
- **Backbone (Law #6):** hash before and after all forwards identical:
  `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`,
  matching the LOG-331 pin in pre-reg §3.6. Δθ=0.
- **Provenance:** npz / embeddings-bytes / ids-bytes / bench canonical-JSON
  pins all logged MATCH; EXP112 archive 60 records id-order-aligned. The npz
  embeddings shape (60, 1024) float32 is logged.
- **BPE:** "single-token BPE re-assertion: 120/120 option texts exactly one
  token, match archived t1/t2."
- **Environment:** torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3,
  sklearn 1.9.1, seeds 0/0, threads 2 — matches the registered envelope.

## 4. Law #9 fence — no fidelity and no contrast C was read [FACT]

The script computes per-site fidelity and the contrast C only in section 8,
which is unreachable after the section-7 `sys.exit(46)`. The stdout log contains
no per-site fidelity line, no `CONTRAST C` line, and no `RESULT_JSON` print.
No result JSON files exist. **The metric branch was never reached.** The only
"41/60" in the run is the §3.2 consistency pin — an archived pin, not a metric.

## 5. Double-normalization mechanics — the pin arbitrated [OBSERVATION]

The report states the first attempt double-applied `final_layer_norm` at L24
(transformers 5.17.0 captures `hidden_states[-1]` already final-normed), that
the consistency pin HALTed it (5/60 argmax flips), and that the corrected lens
(`lm_head(h_24)` at L24; `lm_head(final_layer_norm(h_L))` for L≤23) passed the
pin. The only directly verifiable fact is the corrected run: the lens@L24
readouts are byte-identical 60/60 to the archived column, and the script's
docstring documents the correction mechanism. The failed first attempt left no
separate log in `out/` — I cannot independently verify the "5/60 flips" number,
but it is a mechanics note, not a verdict input, and the corrected run's
passing pin independently confirms lens correctness. No protocol text changed;
the registered pin arbitrated, exactly as pre-registered.

## 6. Fences [FACT]

- No verdict on the late-locality hypothesis was or could be smuggled: the metric
  was never computed (§4).
- EXP112's HELD (41/60) stands unchanged; the report's §9 fence honors the
  pre-registered untouchability.
- The §10-item-12 citation nit ("(H6 §8.6 equivalent)" should read "H6 §8 item 6")
  was already recorded in the CEO launch entry (LOG-4619) and is carried here.

## 7. Review verdict

**QUALIFY.** The registered RUN-INVALID binds — apparatus failure
(logit-lens channel cannot speak at early layers on this bench; entity-name
tokens acquire unembedding mass only in the final ~5 layers), not a verdict on
the locality hypothesis, and not a failure of the apparatus's honesty: the
pre-registered run-validity rule fired exactly as designed at the exact
breaking point named in the pre-reg §0(6). **Caveat:** the report's worksheet
claims (§10/§11) are false — the file was never written; an erratum must
correct them and `exp118_worksheet.json` must not be cited as existing.

**Files:** this review at
`~/workspace/SCBI/research/reviews/VERDICTREVIEW_EXP118_2026-09-29.md`;
report at `research/experiments/EXP118_HDILOC_REPORT_2026-09-29.md`;
raw: `experiments/runs/EXP118_hdiloc/out/exp118_execute.py`,
`experiments/runs/EXP118_hdiloc/out/exp118_stdout.log`.

**Next (lane-discipline):** an erratum-append lane for the report's §10/§11
worksheet claims; then scoreboard records EXP118 as the sixth RUN-INVALID
(EXP108/109/115/116/117).
