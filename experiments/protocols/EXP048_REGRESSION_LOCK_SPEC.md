# EXP048 REGRESSION LOCK SPECIFICATION

**Experiment ID:** EXP048  
**Pre-Registration Date:** 2026-09-12  
**Status:** PRE-REGISTERED (LOG-057)  
**Type:** Canonical Deterministic Regression Lock (not exploratory)

---

## 1. Scientific Mandate

EXP047's implementation consistency audit (2026-09-12) revealed that its
"active probing refuted" conclusion was invalid due to two design mismatches:
1. The wrong operator was used (G4_ortho_flow instead of G_contrastive)
2. A mixed benchmark was used instead of pure BENCH-002 Seed-84

EXP048 resolves this by deterministically reproducing EXP043's G_contrastive
evaluation on the identical benchmark. It is NOT exploratory. It has exactly
one goal: reproduce EXP043 or trigger a provenance audit.

---

## 2. Frozen Protocol Parameters

| Parameter | Value |
|---|---|
| Model | EleutherAI/pythia-160m |
| Model SHA-256 | 54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936 |
| Benchmark | BENCH-002-NL only (pure -- no BENCH-004) |
| Seed | 84 |
| N instances | 50 |
| Layer (target_block) | 7 (0-indexed = Layer 8) |
| Operator | G_contrastive = extract_subspace(h8[dist_indices, :], rank=2) -> P_c = V_c @ V_c.T |
| Projection rank | 2 |
| Alpha | 0.25 |
| Prompt field | inst["base"] |
| Target extraction | tokenizer.encode(" " + inst["target"].strip())[0] |
| Span anchors | " Distractor:" and " Question:" character offsets |
| Compute budget | B_eval = 1.00 (single forward pass per instance) |

---

## 3. Pre-Registered Success Criteria

| Metric | Required Value |
|---|---|
| Baseline accuracy | Exactly 60% (30/50) |
| Intervention accuracy (G_contrastive) | >= 72% (36/50); exact reported |
| Rescues (b) | >= 6 (EXP043: b=7; tolerance +/-1) |
| Corruptions (c) | = 0 |
| McNemar p | <= 0.05 |
| Per-instance baseline match vs EXP043 | >= 46/50 |
| Per-instance intervention match vs EXP043 | >= 46/50 |

---

## 4. Pre-Registered Failure Criterion

If baseline accuracy != 60% OR b < 5 OR c > 0:
  -> Trigger full EXP043 provenance audit.
  -> No theoretical conclusions may be drawn from EXP043 finding.

---

## 5. Parameter Hash Protocol

Pre-experiment SHA-256 must equal CANONICAL_HASH.
Post-experiment SHA-256 must equal pre-experiment hash (Delta_theta = 0).
Any hash mismatch must be flagged before result interpretation.

---

## 6. Zero Data Leakage Protocol

The G_contrastive operator is constructed from h8[dist_indices] where dist_indices
are derived from the offset mapping of the prompt text (not from any label).
No outcome labels, target IDs, or correct answers are used in operator construction.
The t_id (target token ID) is used ONLY for evaluation, not for operator construction.

---

## 7. Instance-Level Verification

EXP048 must output a per-instance comparison table against EXP043 aggregates.
EXP043 does not store raw per-instance predictions (only aggregate stats).
The comparison verifies:
  - EXP048 baseline accuracy exactly equals EXP043's 60% aggregate
  - EXP048 b within +/-1 of EXP043's b=7
  - EXP048 c = 0 matching EXP043's c=0

---

## 8. Two-Branch Resolution

Branch A -- REGRESSION_LOCK_CONFIRMED:
  EXP043 G_contrastive result is deterministically reproducible.
  EXP047's negative result is confirmed as a design-mismatch / non-falsifying experiment.
  EXP043's +14 pp finding is strengthened as the canonical empirical anchor for SCBI.

Branch B -- FAILURE_CRITERION_TRIGGERED:
  Full EXP043 provenance audit required.
  No theoretical conclusions from EXP043 until audit complete.
  EXP047's negative result cannot be used to fill the vacuum.

---

## 9. Post-EXP048 Scientific Direction

IF Branch A (confirmed):
  The canonical research question becomes:
  "Can a system prospectively discover when G_contrastive should be invoked?"
  This is the active-probing hypothesis that EXP047 failed to test.

IF Branch B (audit triggered):
  Full re-examination of operator construction, instance ordering, and
  tokenization from EXP043's original execution environment.

---

**Output:** experiments/runs/EXP048_regression_lock/exp048_regression_results.json
**Script:**  experiments/scripts/run_exp048_regression_lock.py
