# EXP133 — APPARATUS-VOID report (pilot stopped at breaking points, no forwards executed)

**Experiment:** EXP133 (GEOSTEER geodesic multistep CPU pilot, minted LOG-4798).
**Lane:** LOG-4799 (CEO pre-assigned). **Date:** 2026-09-30. **$0 CPU.**
**Verdict: APPARATUS-VOID** (breaking point (b) tripped). Hypothesis UNTESTED. Zero forwards executed. No records exist; no records hash.

## Breaking-point results

**(a) Backbone LOG-331 pin — PASS.** Loaded `/home/hatch/workspace/.exp086_weights/pythia-410m`
with transformers 5.17.0 / torch 2.14.0+cpu / float32 (canonical sorted-state_dict float32-bytes
convention). Measured: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
— matches the LOG-331 pin exactly. Δθ=0 apparatus intact. No forward was run after pinning.

**(b) Direction re-pins — TRIPPED → APPARATUS-VOID.**
- `exp127_vectors.npz` SHA-256: `9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`
  — matches the EXP131-pinned V1_NPZ_PIN. Artifact intact.
- Key inventory (20 keys total): `v1__<prompt_id>` × 10 — PRESENT, all 10 prompt ids align.
  `v2__<prompt_id>` × 0 — ABSENT. `bagg__<prompt_id>` × 0 — ABSENT.
  (Remaining 10 keys are `urand__<prompt_id>` 64×1024 random-direction sets, not v2/B_agg.)
- The pre-reg's breaking point (b) requires all three id families and orders
  apparatus-void on miss. The conjunction fails. **No v2 or B_agg direction can be
  obtained as specified.** The pre-reg further forbids re-running EXP131's deflated
  power iteration ("re-pin only"), so deterministic reproduction is barred by the spec.

**Root cause (pre-reg factual defect, not an apparatus defect):** the signed pre-reg
assumed `exp127_vectors.npz` contains `v2__` and `bagg__` keys. It never did — EXP131
derived v2 via seeded deflated power iteration (K=40, seed 20260929_4714) and B_agg via
deterministic EXP077 support-set reconstruction; neither was archived as npz keys.
Two independent Law #14 reviews (LOG-4792, LOG-4793) and the fix-verification lane
(LOG-4797) checked the breaking points' logic but never inventoried the artifact's
actual keys. The backbone (a) and the v1 re-pin are both fine; only the v2/B_agg
sourcing clause is unsatisfiable.

## What was NOT done (per the single-lane fence)

- No executor built. No smoke test. No forwards. No metrics. No decision-table evaluation.
- No workaround attempted: v2/B_agg were NOT re-derived, the spec was NOT reinterpreted.
- Environment that would have been used (recorded, not run): transformers 5.17.0,
  torch 2.14.0+cpu, numpy 2.5.3 (`~/workspace/.venv-exp077`).

## Recommended CEO dispositions (not this lane's mandate)

1. Amend the pre-reg's breaking point (b) and §3.3: either (i) archive v2/B_agg as
   pinned artifacts and re-pin, or (ii) explicitly license deterministic reproduction
   (v2: seed 20260929_4714, K=40 deflated power iteration; B_agg: EXP077 support-set
   reconstruction) with hash-verification against EXP131's records — then re-clear.
2. Add an artifact-inventory check to the Law #14 review checklist: breaking points
   that reference artifact contents must be verified against the actual artifact,
   not just the spec text. This defect class survived two reviews and a verification.
