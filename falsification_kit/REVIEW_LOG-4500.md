# Independent Law #14 Review — Decodability Gap Falsification Kit (LOG-4500)

**Verdict: ADOPT-WITH-FIXES** — one required fix (F1), two observations (F2, F3).
Review-only lane: no kit file modified. All scripts read end-to-end; all
31 unit tests and the full reproduction re-run independently by the reviewer.

## Scope verified

- `tier0.py` (183 lines), `battery.py` (108), `core/scoring.py` (254),
  `core/__init__.py`, `tests/test_degeneracy.py` (126),
  `reference/adapt_exp105.py`, `reproduce_exp105.sh`, `requirements.txt`,
  `bench/cloze_bench.json` (60 items), `reference/battery_worksheet.json`.

## Task 1 — mechanism checks: all PASS

1. **G1 gate actually rejects** (`tier0.py` ll.80–106): candidates failing
   single-token attestation (`len(ids) != 1`) or intra-item distinctness are
   excluded from `item_pools`, listed in `gate_failures`, and never scored.
   Zero passing items → `SystemExit` HALT (ll.105–106). No bypass path.
2. **Δθ=0 guard actually compares** (`tier0.py` ll.37–44, 78, 146–148):
   streaming SHA-256 over all parameters (fp32 view) before and after the
   run; `assert hash_before == hash_after` raises on drift — not a log line.
3. **Decision-table bar order** (`core/scoring.py` `battery_decision`,
   ll.198–254): step-for-step identical to the committed
   `experiments/runs/EXP105_battery/run_battery_exp105.py` (ev6→ev11,
   same thresholds, same first-match order). Primary binding step 9
   (`ev9`, l.238: `dM_T > 0` and T-vs-R McNemar `p ≥ 0.05` → KILL) precedes
   everything except the pre-registered PIVOT/CONTINUE steps. ✓
4. **Arms** (`core/scoring.py` `battery_arms`): B none; T masks baseline
   top-1; F masks structural foil; R masks uniformly among k−2 excluding
   baseline top-1 AND correct, seed pinned `R_SEED = 20260928` before any
   battery computation — matches the original. ✓
5. **Population**: Tier-0 pop = failed items with correct_rank ≤ 5. ✓
6. **Tie-break**: ascending token id on float32-exact ties, identical to the
   original `argmax_tiebreak`. ✓
7. **McNemar-exact**: formula identical to the original; unit test (f)
   cross-checks against `scipy.stats.binomtest` on the full (b,c)∈[0,10]²
   grid (worst |diff| < 1e-12). ✓

## Task 2 — independent re-run: REPRODUCTION EXACT ✔

- All **31 unit tests PASS** (re-run by reviewer, `python3
  tests/test_degeneracy.py`).
- `bash reproduce_exp105.sh` → **REPRODUCTION EXACT ✔** on all 7 checked
  fields vs the committed `battery_worksheet_exp105.json`:
  verdict=KILL, step=9, n_pop=21, dM_T=0.23809523809523808 (exact),
  dM_R=0.0 (exact), T-vs-R p=0.0625 (exact), O=0.5714285714285714 (exact).
  b/c/p exact on all five contrasts.
- **Bench fidelity**: 60/60 items content-identical to the committed
  `cloze_bench_manifest.json` (prompt, options, correct/foil indices);
  `foil_idx`/`correct_idx` self-consistent 60/60.
- **Token-ID fidelity**: the kit's `reference_token_ids_gpt_neox_20b` are
  byte-identical to the manifest's Pythia-410m `option_token_ids` 60/60
  (same GPT-NeoX vocab); adapter top-1 token ids match the original
  per-item records' `top1_token_id` 60/60. The reproduction runs on the
  identical token-ID pools as the original experiment.
- Kit `reference/battery_worksheet.json` faithful to the committed
  worksheet on every checked field.

## Task 3 — adversarial check: no false-PASSED path; one false-KILL path (F1)

No path found by which the kit could emit a false **TIER-0 PASSED** or
false **CONTINUE**: both verdicts are pure functions of measured logits
with no bypass — the G1 gate runs unconditionally, the weight-hash guard
asserts (not logs), the CONTINUE step requires the conjunction
`dM_T > 0.10 ∧ p_TR < 0.05 ∧ |dM_R| < 0.05` from real computation, and the
R-seed is pinned and recorded in the worksheet.

### F1 (REQUIRED FIX) — silent population collapse → verdict on n_pop=0
`battery.py` ll.9–12 (docstring "Input") lists the minimal record fields as
`item_id, candidate_logits[8], candidate_token_ids[8], correct_idx,
foil_idx, top1_idx` — **without `correct_rank`**. But population
membership (`battery.py` ll.59–62) requires `rec.get("correct_rank")`; a
record set following the docstring gets `n_pop = 0` and the battery
**silently emits `KILL (step 10)`** with no warning. Verified empirically
by the reviewer: 60 well-formed bare records → `n_pop: 0, verdict: KILL,
step: 10`. A verdict must never be emitted from an empty population.
Inherited from the original script (which also lacks an n_pop==0 guard),
but the kit is built for third-party use where `tier0.py` may not be the
producer. **Fix: HALT/raise when n_pop == 0 (or when any record lacks
`correct_rank`), and correct the docstring's Input field list.**
Conservative direction (false KILL, not false PASSED), severity medium.

### F2 (observation, no action) — Tango CI numerical noise
The kit's Tango 95% CIs differ from the original worksheet at ~1e-6
(optimizer convergence across scipy versions); e.g. T-vs-R
(0.04663740431495465, 0.45091172624432585) vs
(0.04663939627990292, 0.4509140303516862). Both round to the published
(0.047, 0.451). Binding McNemar p-values are bit-exact; CIs are
descriptive. Not a defect.

### F3 (observation, no action) — field-name note
`reference_token_ids_gpt_neox_20b` are in fact the Pythia-410m token IDs
(verified 60/60 identical to the manifest; same NeoX vocab). Values are
correct; the name is mildly misleading. Cosmetic only.

## Required fix list

1. **F1**: `battery.py` must refuse to emit a verdict on an empty
   population (raise/HALT on `n_pop == 0`), and the docstring Input
   section must list `correct_rank` as required. Until fixed, the kit is
   ADOPTED for internal/kit-pipeline use only (tier0.py → battery.py,
   where `correct_rank` is always present); third-party bare-record use
   is not cleared.

## Verdict

**ADOPT-WITH-FIXES.** The kit faithfully ports the EXP105 machinery:
bar order, arms, population, tie-break, and statistics verified identical
to the committed artifacts; the EXP105 reproduction is exact on every
binding number. The single required fix (F1) blocks only the
third-party bare-record path and is a small, well-scoped change.
