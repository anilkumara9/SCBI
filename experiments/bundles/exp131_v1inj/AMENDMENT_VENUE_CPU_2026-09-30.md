# EXP131 — Amendment E: execution venue GPU→CPU — DRAFT 2026-09-30

**Status:** DRAFT. Venue-change note only. **Licenses nothing** — requires
independent Law #14 review + fresh CEO clearance, which are not granted by
this document.

**Background [FACT]:** the founder has no laptop — the LOG-4823-cleared GPU
re-execution (attempt 2) cannot run on their Kaggle. The CEO directs
re-execution on the team's CPUs instead.

## The change (one item)

**Execution venue: GPU → CPU.** The executor is CPU-capable [FACT]: the
RUNBOOK documents CPU build and unit-testing (11/11 decision-tree tests);
`--smoke` runs end-to-end locally; LOG-4820's (h) smoke ran on CPU
(torch 2.14.0+cpu / transformers 5.17.0) with (h) PASS (r = 1.0000001).

## License — the drift evidence

[FACT] LOG-4803 measured the CPU-vs-GPU budget drift directly:
CPU-recomputed B = 0.50578363 vs verbatim GPU-measured B = 0.50578119
(LOG-4766, T4), relative difference **4.832e-06**.

[FACT] Diagnosis (LOG-4803): genuine cross-device floating-point
numerics (~20 blocks of differently-ordered reductions, GPU torch
2.10+cu128 vs CPU torch 2.14.0), **not** drift — backbone (LOG-331),
bench, and B_agg pins were all bit-exact; the diagnostic reproduced
identical B with and without deterministic algorithms.

[FACT] LOG-4805 (independent Law #14 SIGN on EXP133's Amendment C):
a 1e-4 relative tolerance sits **>20× above the measured 4.832e-06
noise floor**, while 1e-6 is demonstrated unsatisfiable across devices.

[FACT] The pre-reg's budget is scale-relative **by design**: B = 1% of
median ‖y_{20,last}‖, computed fresh from base forwards at runtime on
the executing device (§3.4; §9 deviation 3 — no absolute number is
invented, Law #2). The decision statistics — ĉ (cosine alignment),
median margin-displacement ratio r, ΔM, McNemar p, rank trend — are
dimensionless or scale-relative; none depends on the absolute B.

## Correction to the brief

[FACT] The drafting brief's worth-it gate assumed a (d) budget
drift-detector at 1e-4 relative ("already 1e-4"; "(d) trips on CPU
(>1e-4)"). **The EXP131 executor has no such detector** — verified
from `run_exp131.py`: B is computed fresh at runtime and never compared
against the GPU-registered 0.50578119. The protocol's §0(d) is the
**same-device per-arm norm audit** (‖δ‖ = B within 1e-6 relative),
which is unaffected by venue. The 1e-4 tolerance lives in EXP133's
Amendment C — a different pre-registration. This draft does not invent
the assumed detector (Law #2).

## Runtime falsifiability (recommendation, not mandate)

The existing runtime guards already falsify apparatus defects on CPU:
(a) LOG-331 backbone pin pre/post, (d) per-arm norm audit at 1e-6
(same-device), (h) readout-sensitivity positive control before the
first injection forward. This draft **recommends** — for the CEO and
the Law #14 reviewer to decide — a narrow executor addition as the
venue change's dedicated runtime falsifier: a budget drift-detector
comparing CPU-computed B against GPU-registered 0.50578119 within
1e-4 relative; miss → apparatus-void, exit 44, zero decision
forwards. That addition is an executor change requiring its own
review + clearance; it is **not** part of this draft.

**Quantitative prediction [INTERPRETATION]:** CPU-computed B will
match 0.50578119 within ~5e-6 (the LOG-4803 measurement) — 20×+
inside the 1e-4 Amendment-C tolerance.

## Everything else unchanged

Hypothesis, bench (verbatim EXP107, canonical first 10), arms
(base / v̂₁ / v̂₂ / 8 randoms / B_agg), budget rule, ĉ gate,
decision table (§2), metrics, random-control seeds, B_agg dead
control, and the (h) positive control are byte-identical in
effect. Venue change only — no hypothesis shift (Law #4), no
definition shift (Law #5).

## Non-resurrection audit

Same hypothesis, same protocol, same decision table — only the
device changes. No killed family is revived; no constraining
kill from §7 is re-opened. The one-shot TGA-v₁ injection
hypothesis remains UNTESTED (LOG-4810); this amendment changes
where the test runs, not what it asks.

## What this note does not do

It does not claim a verdict, does not re-open the decision
table, does not assert the CPU run will KILL or CONTINUE, does
not modify the signed pre-reg (byte-identical; its startup
SHA-256 check still passes), and does not license execution.
