# Independent exact-artifact verdict review — EXP124 (H21/PLAN-INSTRUMENT)

**Review lane:** LOG-4671 (pre-assigned). **Report under review:** `research/experiments/EXP124_PLANINSTRUMENT_REPORT_2026-09-29.md` (execution lane LOG-4670). **Verdict: BIND** — no caveat.

---

## 1. What I recomputed (independent, fresh implementation)

I reimplemented the pinned §3.3 outline-extraction and §3.4 choice-extraction rules from the protocol text (not by importing the executor), rebuilt the bench deterministically via `build_exp107_bench.build_bench()`, and applied the rules to the raw generation texts in `exp124_generations.json` (last 60 records = the fresh full-run generations, item_idx 0..59 in order):

| Count | Mine | Runner (exp124_run.json) |
|---|---|---|
| A-FIRST | 48 | 48 |
| C-FIRST | 7 | 7 |
| choice-invalid | 5 | 5 |
| per-item agreement | — | **60/60** |
| outline-count agreement | — | **60/60** |

**C-FIRST=7 < 12.** The pre-registered choice-information gate (breaking point (a), §5 falsification tree: "choice-information gate: each phrasing chosen ≥ 12 → fails → RUN-INVALID (decision-inert control)") fires exactly as the lane claims. The lane's verdict follows mechanically from the artifacts. No other reading of the rule (leftmost-longest entity mention, case-sensitive, |L|≥2 requirement per §3.4 steps 2–6) changes any of the 60 items.

## 2. Phase-0 gates (verified from exp124_run.json)

- Phase-0pre: 120/120 `[-3:]` tails `== [32, 37741, 27]`, no model contact — PASS.
- Phase-0a: 10/10 choice-valid on probe {0,1,2,5,6,7,8,9,10,11} (≥8 required) — PASS.
- Phase-0b: 4/10 items with differing variant readouts (≥3 required); M_A=0.38102, M_C=0.46331 (both ≥0.01) — PASS.
- Planner prompts byte-identical to the EXP113 T2-P2 reference: 0/60 mismatches — PASS.

The Phase-0-pass/full-run-collapse contrast is the key structural fact, and the protocol handles it explicitly: the falsification tree terminates at the choice-information gate pre-metric, and §7.5 fence item 5 distinguishes *which* apparatus piece failed (choice informativeness) as a boundary finding. The hypothesis is UNTESTED, not killed.

## 3. Integrity pins

- Backbone Δθ=0: pre-contact hash `ec276abe3902fab0…` matched LOG-331 via a hard mismatch→RUN-INVALID gate. The post-contact pin branch sits after the 120 variant forwards in the registered tree — the lane halted at the gate before any forward phase, so no post pin exists. The report discloses this explicitly ("Δθ=0 note"); the executor contains no optimizer/backward pass — Δθ=0 by construction. Not a defect; matches the signed tree order.
- Raw-artifact hash pins: I recomputed SHA-256 of all five persisted artifacts — `exp124_console.log`, `exp124_generations.json`, `exp124_forwards.json`, `exp124_run.json`, `exp124_worksheet.json` — all match `exp124_artifact_pins.json`. Persisted before verdict (defect class 2 satisfied).
- Forwards: exactly 20 records, all `probe_A`/`probe_C` (Phase-0b). Zero full-run forwards ran — correct per tree order (Law #9).
- Baseline reproduction vs EXP112 archive: not reached (tree terminates at the gate) — correctly absent, not skipped.

## 4. Law #9 / defect class 1

No McNemar table, no b/c/d/p values, no p-value anywhere in the report. The report explicitly states "b, c, d, p do not exist" and "No p-value is quoted in this report (defect class 1: none was computed)". Law #9 honored — the metric stage was not reached.

## 5. Descriptive failure-mode analysis (unlicensed observation — spot-verified)

I independently verified the report's descriptive claims: 60/60 full-run generation texts contain a `Premise:` line in the final outline whose entities lie outside the bench vocabulary (e.g., Gold/Iron/Silver/Bronze regurgitations alongside exemplar-planet recitations like Venus/Mars). The "34 distinct hallucinated premises" reproduces exactly under truncation-variant normalization (38 raw, 34 collapsed). The report and LOG-4670 correctly flag this section as unlicensed observation, not part of the verdict. No caveat needed.

## 6. Terminal reading

The lane, the report, and LOG-4670 all state the correct terminal reading: **RUN-INVALID (apparatus-void); H21's instrument-selection channel is UNTESTED, not retired**; H11's planning question survives its fourth RUN-INVALID. No number was minted; the label-free race remains tied at zero; EXP111/EXP120 CONTINUEs and EXP112 HELD are untouched.

---

**Verdict: BIND — the execution lane's RUN-INVALID is correct from the exact artifacts, with no caveat.**
