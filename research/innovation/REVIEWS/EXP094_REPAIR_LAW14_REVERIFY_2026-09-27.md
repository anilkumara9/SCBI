# EXP094 Verdict Repair — Law #14 Delta Re-verification (LOG-4376)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (binding; reports to the founder)
**Date:** 2026-09-27
**Target:** verdict-repair commit `dcc455a` on `lane/log4375-exp094-verdict-repair`,
diffed against overturned execution commit `2e35c8e` (`lane/log4373-exp094-execution`)
**Binding baseline:** LOG-4374 (commit `85e6dfa`) — OVERTURNED with redo items R1–R5
**Method:** detached worktree at `2e35c8e`; repaired script executed in an
isolated `/tmp` copy (shared tree untouched); statistics independently
recomputed with fresh code against the committed Law #13 CSV

---

## Verdict: SIGN

All five redo items are verified repaired. The re-issued verdict —
**Refuted at §3 step 3 (KILL family), via pure inertness** — is now supported
by its artifacts, its statistics match independent recomputation, its step
reasoning is coherent with the binding §3 table, and its provenance is
accurately stated. **Merge of the execution + repair branches is authorized.**
No push (no founder token; push remains founder-reserved).

---

## R1 — rescore repaired and executed — VERIFIED

- The claimed minimal fix is real: `i = int(row["item_id"])` →
  `i = row["item_id"]` (one functional line; item IDs are strings such as
  `exp092_planetary_2hop_0`; no renumbering). Accompanied by an honest
  provenance docstring and a `repair_history` block — both traced to R1/R4,
  no unrelated edits.
- Executed the repaired script in an isolated copy: **exit 0**,
  `AUTHORITATIVE VERDICT: Refuted (decision step 3)`, report written.
- The committed `out/exp094_report.json` (previously cited-but-absent in
  `2e35c8e`) now exists; its full content (verdict, decision_step,
  decision_worksheet, stratum_table, secondaries, bars, recovery inputs,
  repair_history) matches a fresh independent execution byte-for-content.
- The script reads only the committed CSV/manifest and calls the frozen
  bundle scorer; no pass recomputed, no margin regenerated. The "no pass was
  recomputed" phrasing in the docstring is now a true statement about what
  the repaired script does — the false LOG-4373 "zero recomputation" recovery
  claim is separately struck (see R4), not silently reused.

## R2 — false statistics struck — VERIFIED

- Independent recomputation from the committed 180-row CSV (fresh code, strict
  `margin > 0` correctness rule): **B = T = R = 36/60**; ΔM_T = **+0.0000**;
  all three McNemar pairs **b = 0, c = 0, p = 1.0000**; movement (TB+RB
  flips) = **0**; strata A-first and C-first ΔM_T = **+0.0000** (30/30 each);
  0 exact-zero ties / 180. Baseline B 36/60 reproduces S2.
- This matches the LOG-4375 entry's stated recomputed values exactly and
  matches LOG-4374's independent recomputation.
- The false numbers (ΔM_T=−0.0333, T 34/60, R 33/60, p=0.6250, 8 flips,
  strata +0.0333/−0.1000) survive **only** in strike/repair-history context
  (commit message describing the strike; `repair_history` documenting the
  overturn). The terminal `exp094_report.json` contains none of them.
  The LOG-4373 "Prediction vs outcome" paragraph, built on the false numbers,
  is struck with them.
- CSV, manifest, and stdout log are byte-untouched by the repair delta.

## R3 — step reasoning corrected — VERIFIED

- The report's `decision_worksheet`:
  - step 1: `delivery_pass=True` → no match (correct);
  - step 2: `mean_abs_cosine=0.7923 < 0.95` → no match (correct);
  - step 3: `movement=0 < 6` → **MATCH → Refuted (KILL family)** (correct).
- Coherent with the binding §3 table: step 3 fires iff movement < 6.
  The LOG-4373 "movement gate passed: 8 flips ≥ 6 … ΔM_T ≤ 0.10 bar" phrasing
  is struck; it contradicted the table (8 flips would have routed to step 4,
  and "ΔM_T ≤ 0.10" is no step's condition).
- The verdict's stated reason is now pure inertness (zero flips across 120
  injection item-arms despite nonzero margin shifts on every item and a
  genuinely established G5 delivery) — the opposite of the overturned claim,
  and the correct reading of the data.

## R4 — provenance corrected — VERIFIED

- The LOG-4373 "Recovery note" ("verdict recovered via rescore_exp094.py …
  with zero recomputation") is explicitly declared FALSE and struck in the
  LOG-4375 entry; the false "zero recomputation" claim survives nowhere as a
  standing assertion.
- The `repair_history` block in the report's recovery section documents the
  full chain: LOG-4373 (script never ran — `int()` on string IDs →
  ValueError; claimed statistics had no auditable provenance) → LOG-4374
  (OVERTURNED: false statistics, false recovery story, missing report) →
  LOG-4375 (bug fixed, rescore executed, report produced and committed).
- The accurate record now stands: (a) the executor's crash-after-CSV-write
  is genuine (stdout log internal sequence; already verified by LOG-4374);
  (b) the committed recovery script never ran until the repair; (c) the
  repair applied only the pre-registered decision-table scoring to recorded
  data. Commit message `2e35c8e` is immutable; the LOG-4375 entry serves as
  its append-only erratum (the LOG-4373 entries are recorded retroactively
  in the same repair commit and struck there — disclosed, not concealed).

## R5 — timeline corrected — VERIFIED

- The LOG-4373 wall-clock claims (launch 14:25 IST / verdict ~15:10 IST) are
  struck: data commit `2e35c8e` is timestamped 2026-09-27 08:32:13 UTC =
  14:02:13 IST, which predates the claimed verdict time (verified from git).
  Review commit `85e6dfa` = 08:34:21 UTC, consistent with the entry.
- Artifact timestamps are stated as authoritative; run→CSV-write→crash
  ordering rests on the stdout log's internal sequence, stated as such (per
  LOG-4374 F5). No unrecoverable wall-clock is claimed.

---

## Scope discipline — VERIFIED

- The delta touches exactly three files, every hunk tracing to R1–R5 or a
  logged judgment call (the retroactive LOG-4373 record, disclosed in-lane):
  `rescore_exp094.py` (R1/R4), `out/exp094_report.json` (R1/R2, new),
  `reports/research_log.md` (R1–R5 record).
- Untouched: frozen scorer `score_exp094.py`, Law #13 CSV, constructor
  manifests, stdout log, S4-9 pre-registration, G7 chain, G5 delivery probe,
  baseline reproduction (36/60), Δθ=0. The LOG-4375 entry's "verified clean,
  untouched" statement is accurate.

## Licensed consequence — WITHIN LICENSE

- The corrected verdict's consequence claim — "the per-item static-geometry
  family is closed at L11 on this bench; gated/dynamic and multi-layer
  mechanisms untouched; no EXP093 claim altered" — is exactly what pre-reg
  §3 step 3 (KILL family) licenses and what LOG-4374 §4 reviewed as licensed,
  not an overclaim. Step-3 KILL is the verdict the binding table produces;
  no broader claim is made.

---

## Notes (non-blocking)

1. The LOG-4373 entries were committed retroactively inside the repair
   commit rather than on the execution branch. This is disclosed and
   struck-in-place per append-only erratum practice; it is a record-keeping
   wart, not a fidelity defect. Future lanes should commit execution log
   entries on the execution branch before the verdict review.
2. The `delivery_pass` flag is read from the run manifest, not the per-item
   CSV (the CSV carries margins/strata/item IDs). This matches the frozen
   bundle's design and the pre-reg; noted for audit clarity.
3. LOG-4374's advisory G5 band tautology note stands unaddressed, as
   expected for a verdict-layer repair — it is a design note for future
   per-item experiments, not a defect in this verdict.

---

## Review metadata

- **Findings:** none blocking; 3 non-blocking notes above.
- **Redo items:** R1 ✓, R2 ✓, R3 ✓, R4 ✓, R5 ✓ — all verified.
- **Artifacts examined:** detached worktree at `2e35c8e`; isolated execution
  at `/tmp/exp094_r1`; independent recomputation code (ephemeral).
- **Shared tree:** untouched by this review (read-only `git show`/diff plus
  isolated `/tmp` execution).
- **Commit:** this report + LOG-4376 log entry, on
  `lane/log4375-exp094-verdict-repair`. No push. No merge (merge is now
  authorized for the CEO/founder to execute).

**Reviewer signature:** Independent Scientific Mentor & Adversarial Reviewer —
LOG-4376, binding. Verdict: **SIGN** (merge authorized).
