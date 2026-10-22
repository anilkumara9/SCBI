# Independent Exact-Artifact Verdict Review — EXP114 (H8/POE)

**Lane:** LOG-4592 (pre-assigned), independent of the drafting, repair, and execution lanes.
**Documents reviewed:** `research/experiments/EXP114_POE_REPORT_2026-09-29.md` (execution report) against
`research/prereg/EXP_PREREG_H8_POE_2026-09-29.md` (pre-registration; clean Law #14 SIGN, zero fixes — LOG-4589; CEO launch LOG-4590).
**Raw artifacts:** `experiments/runs/EXP114_poe/out/` — `exp114_result.json` (60 per-item records), `exp114_worksheet.json` (order patterns, pins), `exp114_stdout.log` (timestamped gate transcript), `exp114_execute.py` (execution script).

**Verdict: BIND** — the registered KILL stands on the artifacts. No caveat required.

## 1. Binding numbers independently recomputed from raw per-item records

Recomputed from the 60 per-item records in `exp114_result.json` (fields `correct_ens`, `correct_base`, `pred_ens_y`, `pred_base_y`, `y`), not from the report's summaries:

| Metric | Report | Recomputed | Match |
|---|---|---|---|
| acc_ensemble | 38/60 = 0.6333 | 38/60 | ✔ |
| acc_baseline | 41/60 = 0.6833 | 41/60 | ✔ |
| b (base wrong, ens right) | 2 | 2 | ✔ |
| c (base right, ens wrong) | 5 | 5 | ✔ |
| n (discordant) | 7 | 7 | ✔ |
| One-sided exact McNemar p = P(X ≥ 2 \| 7, 0.5) | 0.9375 | 0.9375 | ✔ |
| net (b − c) | −3 | −3 | ✔ |

- `correct_ens`/`correct_base` fields verified internally consistent with `pred_*_y == y` on all 60 records (0 inconsistencies).
- Label balance: Σy = 30 (registered 30/30). ✔
- Applied bars (pre-reg §4 verbatim): CONTINUE required p ≤ 0.05 with b > c — not met; HELD required net > 0 — not met; **net ≤ 0 → KILL — met (−3)**. The `b = c = 0` degenerate branch was registered but not needed (n = 7 > 0). No post-hoc re-interpretation of any bar.

## 2. Order-generation claim verified

- Pre-reg §3.3 pins: 5 i.i.d. order bits per item from `random.Random(20260929)`, sequential draws in canonical bench order, per-item patterns logged.
- Replicated with a fresh `random.Random(20260929)` using the execution script's draw method (`rng.randint(0, 1)`, `exp114_execute.py:131–132`): **0/60 order-pattern mismatches** against the worksheet-logged patterns.
- Degenerate 5–0 compositions: **3/60** — matches the report and worksheet exactly (expected ≈ 6% under i.i.d. draws).
- Per-cell descriptives recomputed from raw records match the report exactly: A-first/flipped ens 0.400/base 0.600; A-first/original 0.533/0.667; C-first/original 1.000/0.933; C-first/flipped 0.600/0.533. (Descriptive only — no decision branch reads them.)
- **Reviewer note (non-binding):** the pre-reg pins the RNG, seed, and "i.i.d. bit draws" but not the exact draw method; in this Python version `randint(0,1)` and `getrandbits(1)` produce different sequences (verified empirically). The script's `randint(0,1)` is a legitimate i.i.d. bit draw, was fixed in the signed execution script before any output was inspected, and the per-item patterns are worksheet-logged — the scheme is exactly reproducible. This affects neither the verdict nor reproducibility; no footnote required.

## 3. Precondition claims verified

- **Archive hashes — independently recomputed from the npz artifact** (not from the lane's transcript): npz file `6cf4a8a7…af6a76`, embeddings-array bytes `9b6e8afb…99123`, ids-array bytes `3669e102…5075cb9` — all three match the pre-reg pins exactly.
- **Bench pin:** stdout log `[09:19:47]` — canonical-JSON sha256 matches `e91b302f…4f5`, 60 items, bench ids == npz ids 60/60. ✔
- **Backbone LOG-331 pin:** stdout log — `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` matched **before the first forward** (09:19:57) and **after the last of 360 forwards** (09:24:56) — Δθ=0. ✔
- **Single-token BPE assertion:** stdout log — 120/120 entity texts exactly one token, zero failures. ✔
- **Prompt rule byte-exact with no letters:** verified in `exp114_execute.py:136–138` (`build_prompt` inserts entity names only; `QUESTION_SUFFIX` byte-exact per log `[09:19:47]`). No option-letter construct-validity path. ✔
- **Tie-break E2 applied identically to both arms:** code lines 160–168 (ensemble) and 170–174 (baseline) — exact float-equality ties → E2 in both. ✔
- **Environment manifest (Law #13):** stdout log — torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, threads 2 set / 2 read back, torch/numpy seeds 0, CPU float32, order seed 20260929, K=5. ✔ Zero generation (360/360 forwards, no autoregressive decoding). ✔

## 4. Falsification branch and fences

- **Branch taken:** `b − c = −3 ≤ 0 → KILL` — matches the registered decision tree exactly. The stdout log itself records `VERDICT: KILL — net (b-c)=-3 <= 0 -> KILL` before any report was written. ✔
- **Fences honored:** report §5.1/§7.3 retire *only* the positional-order-ensembling axis for this task class — test-time scaling in general and the adaptive-loop program are explicitly not retired. The report claims no reasoning, consciousness, or capability consequence (§5.2). ✔
- **No post-hoc softening:** the report states KILL plainly; the "5pp below baseline" reading is labeled `[OBSERVATION]`; no unregistered K-increased rescue is proposed or implied (the pre-reg's HELD branch reserves K-increased follow-up to a *separate* pre-registration, which the report does not invoke). "No data invented. No follow-ups dispatched." ✔
- The report's HALT-vs-RUN-INVALID label note (bench-pin mismatch labeling) is moot — no mismatch occurred. Honestly disclosed, not a defect.

## 5. Most important finding

Every binding number — accuracies, the McNemar table, the one-sided p-value, the net, the order patterns, the three archive hashes, and both backbone pins — was independently recomputed from the raw artifacts and matched exactly. The KILL branch (`net ≤ 0`) is the registered tree's prescribed outcome for these numbers, and the report frames the kill with its fences intact: the positional-order-ensembling axis is dead for this task class, and nothing else is. This is the round-2 wave's first clean negative, and it is clean.
