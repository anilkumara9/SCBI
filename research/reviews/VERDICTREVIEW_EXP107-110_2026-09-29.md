# Independent exact-artifact verdict review — EXP107, EXP108, EXP109, EXP110

**Lane:** LOG-4559 (pre-assigned). **Status:** independent of every drafting, repair, and execution lane.
**Scope:** read-only verification of the four newest execution reports against their raw artifacts and their pre-registration decision bars.
**Method:** recomputed every checkable quantity from the raw run artifacts; compared against the pre-regs in `research/prereg/`; read-only everywhere except this file and the log append. $0 CPU. No reports modified, no follow-ups dispatched.
**Epistemology:** per `~/workspace/SCBI/AGENTS.md` — `[FACT]`, `[OBSERVATION]`, `[INTERPRETATION]` labeled.

---

## EXP107 — template-control kill-test (H3) — **BIND**

- **Verdict on artifacts:** KILL (the EXP106 transfer reading). Report: `research/experiments/EXP107_TEMPLATECTRL_REPORT_2026-09-29.md`. Pre-reg: `research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md`.
- `[OBSERVATION]` Recomputed from `experiments/runs/EXP107_templatectrl/out/exp107_per_item.json` (60 items, fields `id/phrasing/flipped/derived_from/y/pred/correct`): **34/60 correct**; per-cell (phrasing × flipped) = A-first/original **15/15**, A-first/flipped **4/15**, C-first/original **15/15**, C-first/flipped **0/15**. Original-word cells 30/30, flipped-word cells 4/30. The report's numbers match the raw item records exactly.
- `[FACT]` One-sided binomial P(X ≥ 34 | 60, 0.5) recomputed = **0.18314700335164552**, matching the report's 0.1831.
- `[FACT]` Pre-reg §4 bars: **≤ 35/60 → KILL**; "±5 of embedding-shift noise absorbed by the ≤35/60 KILL bar" is registered verbatim (§28/§71), so the 4/15-vs-0/15 flipped-cell asymmetry the report notes moves nothing. 34/60 ≤ 35/60 → KILL applied exactly as written. The GPU proposal licensed by EXP106's CONTINUE is voided in the pre-reg's exact language.
- `[FACT]` The report's registered limitation — the test cannot distinguish a word-template cue from a subject-position cue (pre-reg §3.6/§7, limitation §118) — is honored; no stronger claim is made.
- `[INTERPRETATION]` **BIND.** The verdict follows from the artifacts through the registered bars. No post-hoc re-interpretation detected.

## EXP108 — HDI honesty instrument (H1) — **QUALIFY**

- **Verdict on artifacts:** RUN-INVALID (elicitation failure). Report: `research/experiments/EXP108_HDI_REPORT_2026-09-29.md`. Pre-reg: `research/prereg/EXP_PREREG_H1_HDI_2026-09-29.md`.
- `[FACT]` The elicitation-failure gate was registered before the run (pre-reg §3.4: `n_unparseable ≥ 7 → RUN-INVALID (elicitation failure), NOT a verdict`), not invented after the fact.
- `[OBSERVATION]` The raw artifact `experiments/runs/EXP108_hdi/out/exp108_console.log` records `elicitation complete: n_unparseable = 60/60` and `RUN-INVALID (elicitation failure): n_unparseable=60 >= 7. Not a verdict.` The runner (`run_exp108.py`) writes only this summary line; **no per-item generation records were retained**, so the parse step (strip → first alphabetic char → {A, C} else UNPARSEABLE) cannot be independently re-computed from the artifacts. The "60/60 echo path" claim rests on the run script's in-memory computation as summarized in the log.
- `[FACT]` The pre-reg's falsification tree requires no metric be read when the gate fires; the report correctly reads none (no fidelity, no balanced accuracy, no probe). The degenerate-channel gate was never reached and is correctly not claimed to have fired. The report's licensed observation (60/60 echo-path unparseable, token sequence `[187, 187, 23433, 27] = "\n\nQuestion:"` from the 3-item diagnostic) is an apparatus finding, not evidence about honesty — correctly fenced.
- `[INTERPRETATION]` **QUALIFY.** The verdict stands — the registered gate fired on the artifact as documented, and the bars were applied exactly. Caveat (required footnote): the evidence chain for `n_unparseable = 60/60` is a single console-log summary line; no per-item generation records exist, so an independent reviewer cannot re-run the parse rule from raw artifacts. Future RUN-INVALID verdicts of this class should retain per-item generation logs.

## EXP109 — PTTSC planner/executor pilot (H4) — **BIND**

- **Verdict on artifacts:** RUN-INVALID (elicitation failure; global degeneracy tripwire also fires). Report: `research/experiments/EXP109_PTTSC_REPORT_2026-09-29.md`. Pre-reg: `research/prereg/EXP_PREREG_H4_PTTSC_2026-09-29.md`.
- `[OBSERVATION]` Recomputed from `experiments/runs/EXP109_pttsc/out/exp109_raw.json` (20 items): n_valid (executor- or baseline-parseable) = **0/20**; planner_valid on 2/20 items (mechanical answer-enumerations, executor still 0/4 parseable); executor generations 8 total, 0 parseable; baseline 80/80 unparseable; total generations 108 ≈ 20.86 CPU-min. Matches the report.
- `[FACT]` Registered gates (pre-reg §3.8): elicitation-failure gate `20 − n_valid ≥ 3` → fires at 20 ≥ 3; global degeneracy tripwire (≥50% of executor+baseline generations unparseable) → fires at 88/88. Both fired; the verdict's language matches the falsification tree ("The generation apparatus failed; this is not evidence about planning").
- `[FACT]` Pilot-scope fencing honored: the report contains **no planning-capability verdict**; it explicitly states the coordinator axis is **not** retired for the piloted scope (a KILL would require net ≤ 0 on valid paired items — never reached), and that any future planner-executor test is a separate pre-registered lane. No re-run, larger-n rescue, or gate tweak claimed.
- `[INTERPRETATION]` **BIND.** The verdict follows from the artifacts through the registered gates. The pilot-scope fencing is exactly as the pre-reg requires.

## EXP110 — QBR quantization-boundary robustness (H2) — **BIND**

- **Verdict on artifacts:** CERTIFIED-WITH-NOTE (6/7 tiers, structural tiers T1–T3 intact). Report: `research/experiments/EXP110_QBR_REPORT_2026-09-29.md`. Pre-reg: `research/prereg/EXP_PREREG_H2_QBR_2026-09-29.md`.
- `[OBSERVATION]` All seven per-tier Booleans recomputed from `experiments/runs/EXP110_qbr/out/` raw artifacts (`tier0_quantized.json`, `battery_quantized.json`) against the FP32 reference in `falsification_kit/reference/`:
  - T1: quantized TIER-0 PASSED @ 0.5333 vs ref TIER-0 PASSED @ 0.5333 → TRUE.
  - T2: quantized KILL vs ref KILL → TRUE.
  - T3: quantized step 9 vs ref step 9 → TRUE.
  - T4: quantized dM_T=+0.2000>0, dM_F=+0.1500>0, |dM_R|=0<0.05 vs ref +0.2381/+0.1429/flat → TRUE.
  - T5: quantized T-vs-R b=4,c=0,p=0.1250 ≥ 0.05 vs ref b=5,c=0,p=0.0625 → TRUE.
  - T6: quantized O=0.5000, strict criterion O > 0.5 → **FALSE** (ref O=0.5714).
  - T7: quantized n_pop=20 (within ±5 of ref 21, >0), median failed rank 4.0 = ref 4.0 → TRUE.
  - Result: **6/7 with T1∧T2∧T3 true → CERTIFIED-WITH-NOTE**, exactly the pre-reg §4 branch. The T6 flip (10/20 vs 12/21, population 21→20 at the rank-5 margin) is documented as the bounded precision effect the pre-reg anticipated; the PIVOT branch is correctly not triggered.
- `[FACT]` Reference values above were read from the kit's reference worksheets (`tier0_worksheet.json`: baseline 0.5333, n_pop 21, median rank 4.0, torch 2.14.0+cpu, transformers 5.17.0; `battery_worksheet.json`: KILL, step 9, dM +0.2381/+0.1429/0.0, T-vs-R b=5/c=0/p=0.0625, O=0.5714). All match the pre-reg's pinned reference.
- `[FACT]` `fakequant_manifest.json`: 97 Linear layers transformed; `fp32_pin_match_log331: true`; presentation mechanism `saved-to-local-directory used as --model-id` (the F2 fix). Environment: torch 2.14.0+cpu, transformers 5.17.0 (match reference pins), threads 2 set / 2 read back, seed 20260928, CPU float32.
- `[FACT]` The backbone pin-check-then-derive procedure is documented and coherent: the FP32 backbone verified against the LOG-331 pin via the verbatim LOG-331 procedure (SHA-256 over sorted state_dict keys); the first-pass tier0-style parameter-order hash mismatch was root-caused as a hash-method difference (documented in the report so it is not re-discovered); the quantized copy SHA-256 differs (expected) and the copy is disposable.
- `[FACT]` §7 fences are present in the report (lines 7, 73–74): certification scoped to the INT8 simulation (not true INT8 hardware, not activation quantization, not NF4); no strengthening, re-opening, or re-licensing of the I2′/EXP105 KILL — it stands regardless; no closed line re-run; no capability claim; novelty N1.
- `[INTERPRETATION]` **BIND.** The verdict follows from the artifacts through the registered decision bars. The license question (LOG-4554) was already adjudicated in H2's favor by the independent review; this lane verifies only the execution-verdict binding, which holds.

---

## Summary

| Experiment | Registered verdict | Review | Note |
|---|---|---|---|
| EXP107 | KILL (transfer reading) | **BIND** | Raw items, p-value, and registered ≤35/60 bar all match |
| EXP108 | RUN-INVALID (elicitation) | **QUALIFY** | Verdict logic stands; required footnote: per-item generations not retained — parse step not independently re-computable |
| EXP109 | RUN-INVALID (elicitation) | **BIND** | Both registered gates fire on the raw; no planning verdict; pilot fencing honored |
| EXP110 | CERTIFIED-WITH-NOTE | **BIND** | All 7 per-tier Booleans recomputed from raw match; reference pins, environment manifest, fake-quant manifest, and §7 fences all verified |

**[INTERPRETATION]** All four verdicts bind to their registered bars. The one required footnote is EXP108's thin evidence chain. No verdict was modified; no report was edited; no follow-ups dispatched. This lane stops here.
