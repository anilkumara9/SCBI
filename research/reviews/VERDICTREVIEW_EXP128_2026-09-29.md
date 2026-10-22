# Independent Verdict Review — EXP128 (DSF/SENSITIVITY-FIELD) — 2026-09-29

**Lane:** LOG-4707 (pre-assigned). **Verdict: BIND-WITH-CAVEAT** — EXP128's RUN-INVALID (apparatus-void) is correct from the exact artifacts. The caveat is a non-verdict-bearing protocol-arithmetic observation (§6); no erratum to the verdict is needed.

**Reviewer:** independent lane; no involvement in EXP128's gate, pre-registration, Law #14 review, or execution. Read-only on all signed artifacts and the GPU queue; wrote only this review and the LOG-4707 research-log entry. $0 CPU.

---

## 1. Materials

- Execution report: `research/experiments/EXP128_DSF_SENSITIVITYFIELD_REPORT_2026-09-29.md` (LOG-4706)
- Signed protocol: `research/prereg/EXP_PREREG_DSF_SENSITIVITYFIELD_2026-09-29.md`
- Raw artifacts: `experiments/runs/EXP128_dsf/out/` — `exp128_console.log` (3,266 bytes), `exp128_stdout.log` (6,541 bytes). No field/check/ratios/worksheet JSON exists (the tree halted before the §3.9 hash-pin node); the executor `exp128_execute.py` was read for logic audit only, never reused for recomputation.

## 2. Independent verification (reimplemented from the protocol text)

**Protocol hash.** `sha256sum` on the protocol file returns `c1f5212651fc8d2ca2eefd6e4bebfc9580dc7a85f958bd19f48f8b73263f683b` — matches the signed post-fix value, the report's claim, and the console log's pre-forward pin line. ✓

**Linearity check (breaking point (b), protocol §3.6).** Reimplemented independently: for each of the 12 pinned check points (items {0,4,9} × layers {L5,L11,L17,L23}), `rel = |S(ε/2)−S(ε)|/S(ε)`, pass iff `rel ≤ 0.25` (and `S(ε) ≠ 0`), using the check-point table values from the console log:

| item | layer | S(ε) | S(ε/2) | rel (recomputed) | table rel | verdict |
|---|---|---|---|---|---|---|
| 0 | L5 | 9.4964 | 21.1816 | 1.2305 | 1.23 | FAIL |
| 0 | L11 | 10.8147 | 18.9249 | 0.7499 | 0.7499 | FAIL |
| 0 | L17 | 10.8375 | 21.3019 | 0.9656 | 0.9656 | FAIL |
| 0 | L23 | 7.38359 | 9.11771 | 0.2349 | 0.2349 | **PASS** |
| 4 | L5 | 8.44262 | 15.7927 | 0.8706 | 0.8706 | FAIL |
| 4 | L11 | 8.93842 | 17.7076 | 0.9811 | 0.9811 | FAIL |
| 4 | L17 | 7.77752 | 18.3736 | 1.3624 | 1.362 | FAIL |
| 4 | L23 | 3.91339 | 7.16379 | 0.8306 | 0.8306 | FAIL |
| 9 | L5 | 8.3498 | 15.5471 | 0.8620 | 0.862 | FAIL |
| 9 | L11 | 7.83391 | 15.5642 | 0.9868 | 0.9868 | FAIL |
| 9 | L17 | 7.96442 | 16.2509 | 1.0404 | 1.04 | FAIL |
| 9 | L23 | 3.04035 | 4.65474 | 0.5310 | 0.531 | FAIL |

**Count: 1/12 within 25%** — matches the report exactly. The logged table `rel` values match the recomputation to printed precision on all 12 points. The only PASS is item 0 / L23 (rel = 0.2349 ≤ 0.25); the other 11 have rel ∈ [0.531, 1.362], matching the report's "0.53–1.36" band.

Scope note (Law #9 transparency): the S(ε)/S(ε/2) entries are means over 4 draws reported by the executor; per-draw ratios were not retained (the tree halts before the §3.9 hash-pin node — the report discloses this). The verification recomputes the §3.6 check rule on the pinned console-table values, which are the only records the tree produced before the halt.

**Descriptive-numerics cross-check (unlicensed observation, verified as arithmetic only):** S(ε/2)/S(ε) ratios recomputed: item-0 {2.230, 1.750, 1.966, 1.235}; item-4 {1.871, 1.981, 2.362, 1.831}; item-9 {1.862, 1.987, 2.040, 1.531}. On the 11 failing points the ratios span 1.531–2.362, matching the report's descriptive "≈ 1.5–2.4×" band. This verifies the arithmetic of the report's [OBSERVATION], not its interpretation.

**δ-budget audit (breaking point (c)).** The executor (logic-audited, not reused) implements a per-draw halting guard: after the deterministic renormalization `d ← d·(ε/‖d‖)` (seed-deterministic direction, no RNG change), `|‖δ‖ − ε| > 1e-9` → APPARATUS-VOID + immediate exit before the perturbed forward for that draw. The second attempt's log shows 960/960 field forwards and 48/48 check forwards completing with no budget-halt line and an `assert fwd_check == 48` — so all 1008 draws passed the 1e-9 audit. The renormalization and tolerance are executor-internal: `grep` on the signed protocol file finds no "renorm", "1e-9", or "1e-12" — no protocol edit occurred. Constants audited against the protocol: `EPS=1e-3` (§3.3), `BASE_SEED=20260929`, `K_DRAWS=4`, `N_LAYERS=24`, `ITEMS_N=10`, `CHECK_ITEMS=(0,4,9)`, `CHECK_LAYERS=(5,11,17,23)`, `LIN_TOL=0.25` (§3.6) — all match. ✓

**Δθ=0 (breaking point (a)).** The console log records the backbone pre-pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331) on both attempts. The post-pin node is correctly unreached: the executor's linearity-failure branch calls `sys.exit(44)` immediately after logging APPARATUS-VOID, and the post-pin node sits after it — the log ends at the APPARATUS-VOID line, confirming tree order (linearity gate → post-pin → hash-pin). ✓

**Lane-defect disclosure.** Complete and honest. Attempt 1 (16:30:22→16:30:47): used a 1e-12 audit tolerance and halted apparatus-void at the very first draw `(i=0,l=0,d=0)` with `‖δ‖=0.0010000000474974513` — before any perturbed forward. Attempt 2 (16:31:16→16:42:24): re-ran the full tree from the top (protocol pin → prompt verification → backbone pre-pin → base pass → 960 field forwards → 48 check forwards → linearity evaluation → apparatus-void at the gate). Both attempts are on the append-only console log; the cause (float32 non-representability of 1e-3) is documented in the executor's comments and the report's §5. No extraction or metric existed before the corrected tree ran. ✓

**Nothing beyond the gate was read (Law #9).** `grep` for `gini|top-3|top_3` over both logs: zero hits. No p-value, no McNemar, no decision statistic anywhere. The `out/` directory contains only the two logs — no field, check, ratios, or worksheet JSON was written, exactly as the report states. The metric is genuinely unminted: 1/12 < 10/12 → `sys.exit(44)` before the §3.9 hash-pin node, the Gini node, and all four §4 bars. ✓

**Honest frame.** The report §6 records the soft-spot hypothesis as UNTESTED, not killed; the saturating-response observation is tagged `[OBSERVATION]`/`[INTERPRETATION]` (unlicensed, no verdict); no ε retuning was attempted (§0(b)/§10 boundary honored); EXP127's CONTINUE and the TGA program are stated untouched; the capability scoreboard stays at zero. Law #11/Law #8 handling is not triggered here (no KILL minted, nothing reclassified). ✓

## 3. Ruling

The RUN-INVALID follows mechanically from the artifacts: the conjunctive breaking point (b) required ≥ 10/12 check points within 25%, the independent recomputation yields 1/12, and the §5 tree mandates apparatus-void before the hash-pin node. All pre-forward guards passed honestly; the halt is at the registered gate, not a guard failure.

## 4. Deliverables

- This review: `research/reviews/VERDICTREVIEW_EXP128_2026-09-29.md`
- Research log: exactly one LOG-4707 entry appended (continuity 4706→4707 verified; LOG-4707 confirmed next-free before append).

## 5. Notes for the CEO lane (not verdict-bearing)

1. **Scope of the S-values.** The linearity count is verified from the executor's logged table values; per-draw ratio records were not retained (tree halts before §3.9). This matches the report's own disclosure.
2. **Caveat — protocol §3.7 cost formula.** The protocol's cost estimate "10×24×4×2 = 1920 forwards" overcounts what the §3.4 estimator requires (960 one-sided perturbed forwards + 10 base forwards; the ×2 has no estimator basis — §3.4 defines a one-sided difference). The executor ran exactly the estimator-required counts (960 perturbed + 10 base + 48 check = 1018), and the report discloses actual counts alongside the formula. Non-verdict-bearing (the tree's forward-count node passed on actuals); flagged so future DSF-family gates write the cost formula from the estimator, not the reverse.

**Final: BIND-WITH-CAVEAT** — the verdict is correct from the exact artifacts; the caveat is the §3.7 arithmetic observation above.
