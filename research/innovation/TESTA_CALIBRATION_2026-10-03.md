# Test A — Margin-Calibration Instrument Check (EXP135 Sprint Salvage)

**Status:** Micro-analysis lane, 2026-10-03. $0 compute, analysis only, zero new forwards.
**License:** Salvaged Test A from the REJECTED EXP135 sprint design
(`research/innovation/EXP135_SPRINT_DESIGN_2026-10-03.md` §3), per the Law #14
review's salvage recommendation (`EXP135_SPRINT_DESIGN_REVIEW_2026-10-03.md` §7).
**Question:** Is the frozen model's margin a calibrated confidence proxy on the
EXP135 bench — i.e., is P(baseline correct | m⁰) increasing in m⁰?

## Law #7 firewall

[FACT] This is a **labeled instrument check only**. Bench labels (correct answer A
vs foil C per view) are used solely to compute the correctness of the
*unintervened baseline's* decisions and validate the margin–correctness
relationship. **No candidate score, selection statistic, or ranking in any
sprint or experiment sees these labels.** The firewall is intact: labels touch
only the instrument validation, never selection.

## Item-ID source used (documented per the design's fallback clause)

[FACT] The design's primary path — recovering the 6 licensed McNemar-b item IDs
(baseline-wrong/bridge-right) from
`experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` — is
**provenance-invalid** and was NOT used:
- The in-repo JSON is the **CPU-smoke archive**: C1 (baseline) = 36/60,
  C8_bridge = 50/60, McNemar b=14, c=0 (verified by direct count).
- The official GPU record (LOG-128) is b=6, c=0, baseline 34/60, bridge 40/60,
  and exists **only in LOG-128** (notebook-output sha256 checksums); no
  in-repo official JSON exists. File sizes differ (in-repo 31,348 B vs official
  31,313 B), confirming distinct records.
- Per the program's standing GPU-vs-smoke non-conflation rule (LOG-156), the
  smoke record's 14 b-items cannot stand in for the official record's 6.
- **The 6 official item IDs are unrecoverable from any in-repo artifact.**

Per the design's pre-registered fallback, Test A ran as a labeled instrument
check on the unintervened cache using bench labels, explicitly flagged here.

## Method

[FACT] Bench + views reconstructed deterministically from
`experiments/runs/EXP135_eval/run_exp135.py` (`build_bench`, `make_views`,
`tok1`). Reconstruction verified two ways:
1. Rebuilt bench sha256 = `eb304fa6…45589df`, matching the committed run's
   `bench_sha256` exactly.
2. Every committed `yhat` (300/300) equals exactly one of {tok1(A), tok1(C)}
   for its (item, view) — 0 mismatches.

Per-view correctness = (yhat == tok1(A)); per-item mean margin m̄⁰ over 5 views
(60 values). **Pre-registered partition:** wrong = majority-wrong items
(≤2/5 views correct, n=33); right = the rest (n=27). One-sided permutation
test (100,000 permutations, seed 20261003): m̄⁰(wrong) < m̄⁰(right), bar p<0.05.

## Result: calibration FAILS — and inverts

| Group | n | mean m̄⁰ |
|---|---|---|
| Wrong items (≤2/5 correct) | 33 | **1.0578** |
| Right items (≥3/5 correct) | 27 | 0.8627 |
| Observed diff (wrong − right) | | +0.1951 |

**One-sided permutation p = 0.9906** (100,000 permutations). The bar (p < 0.05)
is not met — decisively. Moreover the effect runs the **wrong way**: margins
are *higher* on wrong items.

Robustness (all pre-specified direction, all fail):
- R1 strict partition (0–1 vs 4–5 correct, middle dropped): 1.1539 vs 0.9075,
  p = 0.9985.
- R2 per-view (300 pairs): wrong 1.0330 vs right 0.8888, p = 0.9678.
- R3 Spearman(m̄⁰, per-item accuracy): **ρ = −0.3958, p = 0.0017** —
  significantly *anti*-calibrated.

Overall unintervened accuracy on the reconstructed bench: 43.67% (131/300).

### Post-hoc diagnostic (exploratory, not pre-registered)

A position-bias mechanism explains the inversion:

| Condition | Accuracy | Mean margin |
|---|---|---|
| Correct answer listed first | 50.00% (n=150) | 0.9062 |
| Correct answer listed second | 37.33% (n=150) | 1.0338 |

[INTERPRETATION] The model leans toward the first-listed option and is *more
confident* (larger top-2 logit gap) when the correct answer is second — i.e.,
precisely when its bias points the wrong way. The margin is calibrated to the
model's own (biased) decision policy, not to correctness. On this bench,
confidence is an anti-signal.

## Verdict: **FAILS**

The calibration license — P(baseline correct | m⁰) increasing in m⁰ — does not
hold on the EXP135 bench; the measured relationship is significantly inverted.

## What this means for S4-5's premise

[INTERPRETATION] S4-5's free-energy branch selection, like the rejected sprint's
S(B), relies on the premise that the frozen model's internal signals carry
correctness information usable label-free. This result weakens that premise
*for confidence-like signals on this bench family*: the model's margin is not
merely uninformative — it is significantly anti-informative (ρ = −0.40), driven
by a position bias the margin faithfully tracks. Two consequences for S4-5:
1. If S4-5's free-energy signal correlates with the same decision-confidence
   machinery (top-logit gaps), it inherits the same inversion risk; S4-5's
   design should include a calibration pre-check of its own signal against
   labels *before* any selection claim, or it risks building on an anti-signal.
2. The inversion is bench-specific (position bias in 2-option ranking prompts),
   not a universal indictment of internal signals — free energy over
   trajectories is a different object from next-token margin and may behave
   differently. But the burden of proof is now on S4-5 to show its signal is
   not similarly inverted, rather than assuming informativeness.

Neither consequence kills S4-5; both raise its evidentiary bar. The honest
reading: on this bench, "the model's own uncertainty" points the wrong way,
and any label-free selector built on it needs independent validation of the
sign — which is exactly what the rejected sprint's Phase 2 foil was designed
to do, and exactly what S4-5 should pre-register.

## Records

- Analysis script: `/tmp/testa.py` (ephemeral); result JSON: `/tmp/testa_result.json`.
- Committed records read (not modified):
  `experiments/runs/EXP135_eval/out/exp135_records.json` (cache_unintervened),
  `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` (smoke
  provenance check), `experiments/runs/EXP135_eval/run_exp135.py`
  (bench/view/tokenizer reconstruction).
- No signed artifacts touched. No commits. No pushes.
