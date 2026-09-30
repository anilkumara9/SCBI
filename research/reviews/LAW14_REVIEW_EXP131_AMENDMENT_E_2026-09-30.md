# Law #14 Independent Review — EXP131 Amendment E (venue GPU→CPU)

**Artifact:** `experiments/bundles/exp131_v1inj/AMENDMENT_VENUE_CPU_2026-09-30.md` (DRAFT)
**Reviewer:** independent Law #14 lane (LOG-4825, CEO pre-assigned). No prior
involvement in the amendment's drafting.
**Date:** 2026-09-30
**Verdict:** **SIGN** — no blocking findings; one non-blocking advisory (A1).
The amendment is approved as drafted: a venue-only change. It licenses
nothing by itself; execution still requires fresh CEO clearance.

**Scope of this review:** the draft note only. No executor edits, no
execution, no re-verdict. Read in full: the draft; the signed pre-reg
`EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md` (§§0, 2, 3.1–3.5); LOG-4810,
LOG-4822, LOG-4823, LOG-4824; `run_exp131.py` (spot-checked for the
drift-detector question); `~/workspace/SCBI/AGENTS.md`.

---

## 1. Venue-change narrowness — PASS

The draft changes exactly one thing: the execution device (GPU→CPU). The
everything-else-unchanged clause was verified against the signed pre-reg:

- Hypothesis (§2 exact question), bench (verbatim EXP107, canonical first
  10, §3.1), arms (base / v̂₁ / v̂₂ / 8 randoms / B_agg, §3.5), budget rule
  (B = 1% of median ‖y_{20,last}‖, runtime-computed, §3.4), ĉ gate and
  decision table (§2), random-control seeds, B_agg dead control (§0(e)),
  and the (h) positive control (hook-fix amendment, LOG-4822) are all
  untouched by the draft. The draft is paper-only: it effects the venue
  change by *where* the executor runs, not by any code or protocol edit.
- "The executor is CPU-capable [FACT]" is grounded: the RUNBOOK documents
  CPU build and unit-testing (11/11 decision-tree tests), `--smoke` runs
  end-to-end locally, and LOG-4820's (h) smoke ran on CPU
  (torch 2.14.0+cpu / transformers 5.17.0) with (h) PASS (r = 1.0000001).
- No hypothesis shift (Law #4), no definition shift (Law #5).

## 2. Drift license — PASS, honestly fenced

- The 4.832e-06 CPU-vs-GPU figure is LOG-4803's measured value
  (0.50578363 vs 0.50578119), cited accurately; the >20× margin
  arithmetic checks (1e-4 / 4.832e-6 ≈ 20.7×).
- **No conflation:** the draft's "Correction to the brief" explicitly
  separates EXP133's Amendment-C 1e-4 tolerance ("lives in EXP133's
  Amendment C — a different pre-registration") from EXP131's §0(d), which
  I verified is the **same-device per-arm norm audit** (‖δ‖ = B within
  1e-6 relative; pre-reg §0(d), §3.4) — unaffected by venue, since all
  forwards on a run share one device. The 1e-4 band is cited only as a
  demonstrated-safe *detector* band (LOG-4805 independent SIGN), not
  imported as an EXP131 breaking point.
- The decision statistics' scale-invariance claim holds: ĉ (cosine),
  margin-displacement ratio (paired ratio), ΔM (counts), McNemar p, and
  rank trend are dimensionless or dose-matched on-device; §2's table
  references no absolute B. A ~5e-6 relative dose shift cannot move any
  registered gate.

## 3. The drift-detector recommendation — (b) SEPARATE, at CEO discretion

The drafter (correctly, Law #2) found the brief's assumed detector does
not exist — I verified from `run_exp131.py`: the literal `0.50578119`
appears nowhere; B is runtime-computed and never compared cross-device —
and states this honestly (Law #11) instead of inventing it.

The recommended detector (CPU-B vs GPU-registered 0.50578119 within
1e-4 relative; miss → apparatus-void, exit 44) is sound, narrow, and
mechanical, and exit 44 matches the executor's existing apparatus-void
convention. **Recommendation:**

- **(a) Fold into Amendment E — NO.** It is an executor change; folding
  it in would break the amendment's "venue only" narrowness claim and
  smuggle an unreviewed code modification inside a paper-only note. The
  draft itself correctly refuses this ("it is not part of this draft").
- **(b) Separate mini-amendment — YES, at CEO discretion.** Sound and
  narrow, but it needs its own Law #14 review + clearance before
  execution, like any executor change.
- **(c) Unnecessary — defensible but not recommended.** (a) pins the
  weights, (d) audits per-arm dose on-device, (e) guards bench/backbone
  via B_agg, (h) guards delivery; the residual risk the detector covers
  (a >1e-4 systematic scale shift with pins intact) is small. But this
  program was just burned by an unguarded apparatus assumption
  (LOG-4808/4809); a cheap, pre-registered, dedicated falsifier for the
  venue change is the safer posture. Not required for this SIGN.

## 4. Worth-it gate honesty — PASS

All seven points in LOG-4824 survive the correction; the correction
itself is Law #2/#11 compliance, not a gate failure. Point (6) is now
accurately stated (existing guards + *recommended* detector, not an
assumed one). The quantitative prediction is labeled [INTERPRETATION].

## 5. Non-resurrection — PASS

Same hypothesis, same protocol, same decision table — only the device
changes. The one-shot TGA-v₁ injection hypothesis remains UNTESTED
(LOG-4810); no killed family is revived, no §7 constraining kill is
re-opened, no science is smuggled.

## Law #11 labeling — PASS

[FACT]/[INTERPRETATION] used correctly throughout; the quantitative
prediction is labeled [INTERPRETATION]; no unverifiable
version-attribution claims (the LOG-4812/4821 lesson was applied —
the draft makes no ≤5.0-type assertions).

## Advisory (non-blocking)

- **A1:** Pre-reg §3.2 records the device in the worksheet ("device
  pinned in the worksheet"). The execution lane should ensure the
  worksheet records the actual CPU device rather than inheriting any
  GPU-template value. Operational note only; not a draft defect.

## Disposition

Amendment E approved as drafted — venue-only, licenses nothing.
Execution of EXP131 attempt 2 on CPU still requires fresh CEO clearance
(LOG-4823's clearance was GPU-scoped and cannot execute). If the CEO
wants the drift-detector, commission it as a separate mini-amendment
with its own review; it is not part of this SIGN.
