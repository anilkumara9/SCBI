# Independent exact-artifact verdict review: EXP113 (H7/EVALID)

**Lane:** LOG-4585 (pre-assigned). **Date:** 2026-09-29.
**Document under review:** `research/experiments/EXP113_EVALID_REPORT_2026-09-29.md`
**Pre-registration:** `research/prereg/EXP_PREREG_H7_EVALID_2026-09-29.md` (Law #14 SIGN, LOG-4582)
**Raw artifacts:** `experiments/runs/EXP113_evalid/out/exp113_raw.json` (600 records), `exp113_console.log`, `exp113_console_crash1.log`, `exp113_execution_log_crash1.txt`, `exp113_run.py`
**Method:** every binding number recomputed independently from raw records with my own parse implementation; pre-reg decision bars checked verbatim; script code inspected for honesty-note claims. No report modified, $0 CPU.

---

## Verdict: BIND

The registered CONTINUE stands on the artifacts. No caveat required for the verdict to bind.

## Independent verification

### 1. Parse counts recomputed from raw records (my own implementation)

Using the pre-reg's pinned parse rules (T1: first alphabetic char, uppercase, ∈ {A, C}; T2: literal markers `1.`–`4.`, ≥2 distinct non-empty outlines), applied to all 600 raw generations:

| Protocol | T1 (mine / report) | T2 (mine / report) |
|---|---|---|
| P1 | 0 / 0 | 24 / 24 |
| P2 | 60 / 60 | 60 / 60 |
| P3 | 0 / 0 | 0 / 0 |
| P4 | 58 / 58 | 0 / 0 |
| P5 | 60 / 60 | 60 / 60 |

**All 10 counts match exactly.** Coverage verified: 5 protocols × 2 tasks × 60 items = 600 records, 60 unique item IDs, no early abandonment (P1/P3/P4-on-T2 all ran to completion despite 0/60 scores — a valid measurement, never RUN-INVALID, per §3.6).

### 2. Decision bars applied verbatim

- T1-CLEAR = {P2, P4, P5} (≥48/60), T2-CLEAR = {P2, P5} (≥48/60). Both non-empty → **CONTINUE** per pre-reg §4.
- No PIVOT/HELD/KILL branch applies (P1/P3 are 0/60 but clearance exists; max counts far exceed 21/60).
- The per-task licensing form holds correctly: P4 clears T1 but fails T2 (derailed text), and is counted in T1-CLEAR only — consistent with the §1 fix (protocols need not be the same across tasks).

### 3. Infrastructure incident

- `exp113_console_crash1.log` exists; it ends at `progress: 180/600` with no traceback — a silent VM-reboot death. No metric was read before the crash: the crash logs contain no parse table, no counts, no verdict line (compare the successful run's console, which logs counts only after generation 600 + backbone re-hash + re-parse).
- The relaunched run completed all 600 from scratch with identical code/seeds/pins; the write-only `exp113_raw_partial.json` checkpoint was diagnostic only and never read back into the numbers (the final 600 records are the clean relaunch's).

### 4. Preconditions and apparatus gates

- Backbone SHA-256 (sorted state_dict keys) = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` **before and after** all 600 generations — matches the LOG-331 pin; Δθ=0.
- Bench provenance SHA-256 = `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` — matches pin; 60 items.
- Exceptions: 0/600 (no traceback anywhere in raw records). Empty generations: 2/600, both T1-P4 at bench indices 45/50 (verified against bench build order) — scored UNPARSEABLE per the registered rule, consistent with T1-P4 = 58. Far below the 10% RUN-INVALID threshold. No RUN-INVALID branch fired.
- Deterministic re-parse ×2: byte-identical (asserted in the successful console log, line `deterministic re-parse: byte-identical (2 runs)`).
- Environment: torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, threads set=2/read=2, seeds 0, greedy, float32 — matches the pinned manifest.

### 5. Honesty notes verified

- **accelerate==1.15.0**: confirmed importable in the execution venv (`~/workspace/.venv-exp111/bin/python` → `1.15.0`). The script's load call (`exp113_run.py:201`) passes `device_map="cpu"` verbatim — the pinned spec is honored exactly, not dropped as in EXP111. Spec-honoring, not spec-changing.
- **T1-P2 exemplars**: script asserts `it["ent"] == it["A"]` (`exp113_run.py:101`) and appends `"\nA: A"` — all three exemplar answers are the letter A, deterministic, exactly as the report discloses. Per pre-reg §3.1 this cannot inflate the parseability metric.
- Block formats documented; the blocklist diagnostic is descriptive-only (frac_block_a=1.0 on T1-P1 reproducing the EXP108 echo; block_b≈0.167 on T2-P1).

### 6. Overclaim fences

Report §7 present and complete: parseable output ≠ reasoning, ≠ honesty, ≠ capability; CONTINUE validates the *elicitation methods only* and does **not** revive H1/H4 (revival lanes are new hypotheses with their own pre-registrations and gates); backbone-specific (base Pythia-410m, CPU, greedy); novelty N1. No post-hoc re-interpretation of the signature, thresholds, or protocols.

## Boundary

Review only. No artifact modified, no experiment number minted, no follow-ups dispatched. Scoreboard sync and commit-prep are separate later lanes.
