# EXP131 — Amendment F: budget drift-detector — DRAFT 2026-09-30

**Status:** DRAFT. Narrow mechanical addition to the repaired CPU bundle.
**Licenses nothing** — requires independent Law #14 review + fresh CEO
clearance, which are not granted by this document.

**Background [FACT]:** Amendment E moved EXP131's re-execution venue to
CPU (CEO-signed LOG-4826). LOG-4825 (independent Law #14 SIGN) recommended
the budget drift-detector as a separate mini-amendment; LOG-4826
commissioned this draft. The EXP131 executor currently computes B fresh
at runtime and never compares it against the GPU-registered value
(Amendment E "Correction to the brief" — verified: `0.50578119` occurs
0 times in `run_exp131.py`, so this detector is a genuine addition).

## The change (one item)

**Breaking point (d2): budget drift-detector.** Immediately after the
budget is computed at runtime on CPU — executor section 5, directly
after the `budget B = ...` log line and before section 5b (the (h)
positive control) and therefore before the first injection forward —
assert:

```
|B_cpu − 0.50578119| / 0.50578119 ≤ 1e-4
```

[FACT] The reference constant 0.50578119 is the verbatim GPU-registered
budget B from the original T4 run: 1% of median ‖y_{20,last}‖ recorded
before the first injection forward (Kaggle report hash `e33a0eac…`,
LOG-4766). It is a measured constant, not an invented number (Law #2).

[FACT] The 1e-4 band is the demonstrated-safe detector band:
LOG-4803 measured the actual CPU-vs-GPU drift at relative 4.832e-06
(backbone, bench, and B_agg pins bit-identical; diagnosis: cross-device
floating-point ordering, not drift), and LOG-4805 (independent Law #14
SIGN on EXP133's Amendment C) found 1e-4 sits >20× above that noise
floor while 1e-6 is demonstrated unsatisfiable across devices.

**Miss behavior [DEFINITION — executor convention]:** miss →
apparatus-void: log
`apparatus-void: budget drift-detector failed (|B_cpu-0.50578119|/0.50578119 = X not ≤ 1e-4) — cross-device budget drift.`,
then `sys.exit(44)` per the pre-reg's §0 breaking-point conventions
(exit 44 = apparatus-void, hypothesis UNTESTED). Zero decision forwards
have occurred at that point (section 5/5b precede all injections).

**Executor insertion point [FACT]:**
`experiments/bundles/exp131_v1inj/run_exp131.py`, section 5, between
line 266 (`log("budget B = ... (recorded BEFORE first injection forward)")`)
and the section-5b header (the (h) positive control). No other line moves.

## What this note does not do

It does not change the dose (B remains the runtime-computed CPU value —
the detector only observes it), the hypothesis, the bench, the arms,
the decision table (§2), the metrics, the seeds, the (d) same-device
per-arm norm audit (1e-6 relative, unaffected), or the (h) control.
It does not claim a verdict, does not assert the CPU run will KILL or
CONTINUE, and does not modify the signed pre-reg (byte-identical; its
startup SHA-256 check still passes).

## Everything else unchanged

Hypothesis, bench (verbatim EXP107, canonical first 10), arms
(base / v̂₁ / v̂₂ / 8 randoms / B_agg), budget rule (B = 1% of median
‖y_{20,last}‖ computed fresh at runtime), ĉ gate, decision table (§2),
metrics, random-control seeds, B_agg dead control, hook-fix repair
(`prepend=True`), and the (h) positive control are byte-identical in
effect. One detector added — no hypothesis shift (Law #4), no
definition shift (Law #5).

## Non-resurrection audit

Same hypothesis, same protocol, same decision table — one runtime
falsifier added. No killed family is revived; no constraining kill from
§7 is re-opened. The one-shot TGA-v₁ injection hypothesis remains
UNTESTED (LOG-4810); this amendment changes what the run checks, not
what it asks.
