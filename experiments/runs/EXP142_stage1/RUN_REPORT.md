# EXP142 Stage-1 RUN REPORT — S4-7 spectral phase transition (RMT lens)

**Protocol:** `research/prereg/EXP_S47_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4891).

## Validity gates

- bench sha256 `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` — PASS
- backbone pre/post hash `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — PASS (Delta theta = 0)
- 60/60 passes complete — PASS (+3 determinism re-runs)
- determinism spot-check 3/3 byte-identical — PASS

## C2 guard

- n_i: median 32.0, IQR [29.0, 35.0], range [29, 35], below-floor(40): 60
- items kept: 0/60; guard fired: True

## Primary test

**VOID — not run.** The C2 guard fired (0/60 items with n_i ≥ 40), so the primary
permutation test was not run per the pre-registered guard. The NaN/p=0.0 values
from the empty-set computation are void artifacts, not results.

- bulk-fit diagnostic: median KS = 0.4108 (flag 0.15) — FLAGGED (poor MP fit at
  n_i ≈ 30; consistent with the guard firing — the MP asymptotics are not
  trustworthy at these sequence lengths)

## Secondary diagnostics (not binding)

**VOID — computed on the empty kept set; not interpretable.** (The per-layer
"significant" flags and l_c counts below are artifacts of empty-array
computation, recorded for transparency, not as findings.)

- l_c present on 0/0 items
- per-layer test: VOID (empty input)
- mean-difference version: VOID (empty input)

## Design note (for the parent, not a verdict)

The design's C2 section priced "n_i ≈ 100 typical" — the measured n_i is
median 32 (range 29–35). The guard worked as designed (HELD, never a spurious
KILL), but the S4-7 observational question cannot be answered on this bench as
specified: the prompts are too short for stable per-item spectra. A future
re-scoping would need longer sequences or a different n_i construction — that
is a new design, not licensed here.

## Verdict

**HELD** — C2 guard fired: 0 items with n_i>=40 (<30) - insufficient positions for stable spectra
