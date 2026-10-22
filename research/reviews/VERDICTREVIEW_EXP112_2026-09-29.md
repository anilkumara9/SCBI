# Independent Exact-Artifact Verdict Review — EXP112 (H6/HDI-LR)

**Lane:** LOG-4576 (pre-assigned). **Date:** 2026-09-29.
**Artifacts reviewed:** `research/prereg/EXP_PREREG_H6_HDILR_2026-09-29.md` (signed, LOG-4573 CLEAN SIGN), `research/experiments/EXP112_HDILR_REPORT_2026-09-29.md`, raw artifacts in `experiments/runs/EXP112_hdildr/out/` (`exp112_per_item.json`, `exp112_worksheet.json`, `exp112_stdout.log`, `exp112_execute.py`).
**Method:** independent recomputation from the raw per-item records, the execution script's own code path, and independently recomputed hashes — not the report's summaries.
**Discipline:** $0 CPU. Read-only; no report modified, no follow-ups dispatched, no push, no GPU contact.

## Verdict: BIND

The registered **HELD** verdict stands on the artifacts. Every binding number was recomputed from the raw per-item records and matches the report exactly. The decision bars were applied verbatim from the pre-registration. The guard ordering and all preconditions verify.

### 1. Fidelity and the registered bars — PASS
- Independently recomputed from `exp112_per_item.json` (60 records, 60 unique ids): agreement(readout, decision) = **41/60 = 0.6833** — matches the report to the item.
- Pre-reg §4 decision table: 34–41/60 → HELD. 41/60 falls inside the registered HELD band — not in CONTINUE (42–57), not in KILL (≥59, ≤33).
- The execution script (`exp112_execute.py` lines 198–216) encodes the bars verbatim: `>=59 → KILL; ==58 → HELD; 42–57 → CONTINUE; 34–41 → HELD; else → KILL`. 41 → HELD. No post-hoc reinterpretation.
- P(X ≥ 41 | 60, 0.5) = 0.0031088… — the report's 0.0031 checks out.
- ≤23/60 systematic-misreporting diagnostic: not triggered (41/60); correctly absent.

### 2. Degeneracy guards — PASS (both the values and the ordering)
- G1 mean mass recomputed from raw records: **0.3010748148880897** (min 0.0684922355868045, max 0.5677453841090856; 100% of items ≥ 0.01) — matches the report's 0.301075. Bar: ≥ 0.01 → PASSED.
- G2 readout balance: **E1 = 27/60, E2 = 33/60**, 2 distinct values, minority = 27 — matches. Bar: ≥2 distinct and minority ≥ 3 → PASSED.
- **Guard ordering verified in the code, not just the report's word:** `exp112_execute.py` line 181 reads `# ---------------- 9. degeneracy guards BEFORE any metric is read ----------------`; guards run in section 9 with RUN-INVALID exits; line 196 logs "G1 and G2 passed: channel non-degenerate. Metric may now be read."; fidelity is computed only afterward in section 10. A degenerate channel could not have produced a metric.

### 3. Preconditions — PASS
- **Archive hashes independently recomputed** from `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz`: npz file sha256 `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76` — exact match to the pin; embeddings-array bytes sha256 and ids-array bytes sha256 — both exact matches. Array (60,1024) float32; ids (60,).
- **Bench pin:** stdout log shows canonical-JSON sha256 matching `e91b302f…4f5` exactly; npz ids == bench ids 60/60.
- **QUESTION_SUFFIX byte-exactness:** `build_exp107_bench.py` line 53: `QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"` — matches the report's claim (no trailing space).
- **Backbone Δθ=0:** stdout log shows the LOG-331 hash `ec276abe…38e0ed` matched **before** all fresh forwards (06:28:30) and **after** all 180 forwards (06:29:30). The report's claim is corroborated by the timestamped log.
- **Single-token BPE assertion:** 120/120 — in the log. Ties: 0 decision ties, 0 readout ties (recomputed).

### 4. Descriptive per-cell diagnostic — PASS (licenses nothing, as registered)
- Recomputed from raw records: A-first/original 8/15, A-first/flipped 12/15, C-first/original 9/15, C-first/flipped 12/15 — match the report's §9 table exactly.
- The flipped-word (24/30) vs original-word (17/30) concentration is recorded as an [OBSERVATION] with "it changes no verdict" and "Per §3.8, this licenses nothing." It is not presented as a verdict and does not smuggle a claim.

### 5. Overclaim fences — PASS
- Report §10: HELD licenses nothing and retires nothing; honesty-decoding correlation on one bench at one read site — "not consciousness, not deceptive intent, not generality beyond the 60-item bench, not capability of any kind"; the readout is "a two-way argmax over first-token logits — nothing more"; novelty N1. All fences present verbatim.

## Footnote
No caveat required for the verdict to bind. Descriptive note only: the descriptive per-cell labels ("original"/"flipped words") map to the raw `flipped` False/True field; the mapping was checked against the bench structure and is consistent.

**Single most important finding:** fidelity 41/60 was recomputed independently from the raw per-item records — it matches the report exactly, falls inside the pre-registered 34–41/60 HELD band, and the guards that protect it (G1, G2) were provably checked before any metric was read, with all three archive hashes and both backbone pins independently re-verified. The HELD verdict is exactly what the pre-registered decision table prescribes for these numbers.
