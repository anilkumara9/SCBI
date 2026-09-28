# EXP105 cloze-format Tier-0 — Execution Report (2026-09-28)

## Verdict: **TIER-0 PASSED**

**Experiment:** EXP105 — cloze-format Tier-0 screen of S4-8′ (re-prompted EXP104 multi-option bench)
**Pre-registration:** `S4-8_PRIME_PREREG_DRAFT_v2_2026-09-28.md`, SIGNED at LOG-4488 (approval chain LOG-4484→4488, CEO execution clearance)
**Execution LOG:** LOG-4489
**Bundle:** `~/workspace/SCBI/experiments/runs/EXP105_cloze_Tier0/`

## Tier-0 numbers (frozen Pythia-410m, $0 CPU, Δθ=0)

| Bar | Result | Gate |
|---|---|---|
| Baseline accuracy | **0.5333 (32/60)** | 0.25 ≤ acc ≤ 0.75 — not LINE-CLOSED, not HOLD |
| Median failed-item correct rank | **4.0** (n_failed=28) | ≤ 5 — not KILLED |
| n_pop (diagnostic subpopulation) | **21** | ≥ 12 — not UNDERDETERMINED |
| Tie guard | **0.0** (0/21) | ≤ 0.25 — not HOLD |

All four bars evaluated in binding order → **TIER-0 PASSED**.

**Pre-registered descriptive sensitivity:** alternative cue `Answer:` + completion → baseline **0.5**. Recorded in the worksheet as `alt_cue_sensitivity`; descriptive only — not a gate, not a result.

## Integrity

- **G1 gate:** PASS — 480/480 candidate strings single-token, token IDs match the EXP104 manifest, intra-item distinct. Tokenizer: `EleutherAI/gpt-neox-20b` main, fetched at run time, byte-identical to the pythia-410m snapshot's own tokenizer JSON (SHA-256 `c24618a1…5f25624`). Leading-space operationalization `tok(" " + option)` carried over from EXP104's G1 probe.
- **Δθ=0:** weight SHA-256 pre = post = `3e09001631bb…27511b` (match: True). 405.334M params, torch 2.14.0+cpu, transformers 5.17.0, seed 20260928.
- **Unit tests (pre-run):** all seven §5 degeneracy classes (a)–(g) passed, 31 assertions; McNemar exact matched SciPy to 1.11e-16 over the full (b,c)∈[0,10]² grid.
- **D3 blindness:** structural-foil designations carried over from EXP104 bench-build time unchanged; no re-designation for cloze re-prompting.
- **Run script SHA-256:** `530539c4812801aa…` (recorded in worksheet; G1-corrected version).

## Execution notes

- The run crossed a VM/runtime restart (12:23–12:25 UTC): 13 of 60 records were persisted pre-restart. Before resuming, `verify_resume.py` recomputed item `exp104_t0_00` and confirmed **bit-exact** match of all 8 candidate logits vs the stored record — resume declared valid; remaining 47 records then executed.
- Post-restart, `torch` had vanished from the environment; it was reinstalled into `~/workspace/venvs/exp-cpu/` (2.14.0+cpu) from the local pip cache at $0, plus transformers 5.17.0, safetensors, scipy.
- 60/60 baseline passes + the pre-registered descriptive alt-cue run are in the bundle. Artifacts: `tier0_worksheet_exp105.json`, `tier0_results_exp105.json`, `per_item_records.json/.csv`, `cloze_bench_manifest.json`, `tier0_exp105_stdout.log`.

## Battery status

**NOT RUN.** The battery is licensed only on a TIER-0 PASSED verdict; the verdict now exists, but the battery requires separate CEO dispatch. This lane stops at the Tier-0 report per the single-lane fence.
