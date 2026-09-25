# Independent Law #14 Verdict Review — EXP093 real re-execution

**Binding verdict: UPHOLD KILL.** The real EXP093 re-execution's KILL is verified from primary artifacts. The run is valid; the statistics recompute exactly; the registered decision bars were applied as written; no signed file was modified; the apparatus demonstrably delivered the injection.

*Reviewer: Independent Law #14 (reports to the founder; binding, not overridable). Date: 2026-09-25. Target: real re-execution, repaired bundle commit `b5da3c5`, raw log `experiments/runs/EXP093_l11_causal/out/exp093_rerun_stdout_2026-09-25.log`, `out/exp093_report.json`.*

---

## Check 1 — Decision statistics recomputed independently: CONFIRMED

I reimplemented the statistics from scratch (own McNemar exact test, doubling convention; own decision-tree logic — no bundle imports) and applied them to the reported aggregates:

| Stratum | n | acc_B | acc_P | acc_N | Δ | McNemar b/c | p | monotone | bars |
|---|---|---|---|---|---|---|---|---|---|
| Aggregate | 60 | 0.6000 | 0.6000 | 0.6000 | 0.0000 | 0/0 | 1.0 | False | False |
| A-first | 30 | 0.9667 | 0.9667 | 0.9667 | 0.0000 | 0/0 | 1.0 | False | False |
| C-first | 30 | 0.2333 | 0.2333 | 0.2333 | 0.0000 | 0/0 | 1.0 | False | False |

Fractions are exact (36/60, 29/30, 7/30). My recomputation reproduces every number in `exp093_report.json` exactly. Decision tree per signed protocol §5 (CONTINUE → PIVOT(c) → PIVOT(a) → PIVOT(b) → KILL): all six McNemar p-values (P-vs-B and N-vs-B × 3 strata) = 1.0 ≥ 0.05 → no PIVOT branch reachable → **KILL**. The code's `decide()` routes identically; the printed `[run] AUTHORITATIVE VERDICT: KILL` is mechanical, not judgment.

**On raw per-item logs:** per-item margins are not persisted to disk (only aggregates in `report.json`; see non-blocking observation below). However, the zero-flip claim is *entailed*, not trusted: b = c = 0 means (~B&P).sum() = (B&~P).sum() = 0, i.e. per-item decisions are identical across B, P, and N — which is exactly what an empty flip ledger asserts. The ledger cannot be non-empty given these counts.

## Check 2 — Guards verified from the raw log: ALL PASS

From `out/exp093_rerun_stdout_2026-09-25.log` (raw, unedited):

- **G0:** bench pin `9be8162633fe19aa…` matches `report.json`'s full pin; 60/60 unique tuples; strata match §2.
- **G1′:** inherited via bench-pin byte-identity; real-tokenizer cover re-executed 240/240.
- **G2:** 60/60 ‖r_i‖ > 1e-9 (min 1.3352), 60/60 unit-norm, coherence mean_cos_u = −0.0160, prenorm [0.0246, 0.0444] — matches the registered prior exactly.
- **G1:** pre-run hash `ec276abe3902fab0…` = LOG-331 pin (the documented sorted-keys hash; procedure root-caused at LOG-123/126); post-run hash identical → **Δθ = 0**.
- **G5:** (i) rel_err = 4.30e-07 ≤ 1e-6 ✓; (ii) max_abs = 0.0 ✓; (iii) bit_match = True ✓ — the repaired probe.
- **G4:** clean baseline 36/60 exactly; mean margin −0.001819 vs registered ref −0.0018 (tolerance 1e-4) ✓. Threads pinned to 2 and asserted.

## Check 3 — Registered bars applied exactly as written: CONFIRMED

- `score_exp093.py`: `DELTA_BAR = 0.10`, `ALPHA = 0.05` — verbatim the registered §4.1 bars.
- Integer-count delta `(nP − nB)/n` (F1 fix) — no float-boundary misrouting possible; irrelevant here (Δ = 0.0 exactly).
- `decide()` evaluation order matches the signed §5 tree, including the N-vs-B secondary routing to PIVOT(b) per the registered forensics rule. No post-hoc movement of any bar.

## Check 4 — No signed file modified by the run: CONFIRMED

`git diff b5da3c5 -- experiments/runs/EXP093_l11_causal/ ':!.../out'` is **empty**. The only new files are the three expected run outputs in `out/` (`exp093_report.json`, `exp093_rerun_stdout_2026-09-25.log`, `exp093_run_log.txt`). `score_exp093.py`, `run_exp093.py`, `inject.py`, all signed protocols, and the protocol digest (`3e0f269b…` in `report.json`, matching the registered digest) are untouched.

## Check 5 — False-negative sanity: KILL STANDS, apparatus delivered

- **Injection magnitude:** perturbation_ratio = α / median‖h‖ = **0.0474** — the nudge was ~4.7% of the typical residual-stream norm: a real perturbation, not a whisper.
- **Delivery proven:** G5 criterion (i) rel_err = 4.30e-07 — the hook delivered exactly the registered +αv at the probe site; the decision loop uses the same single-hook injection mechanism.
- **Perturbation reached the logits:** mean margin shifted +0.0059 (P) and −0.0076 (N) — small, directionally-signed, but nonzero: the intervention demonstrably moved logits without flipping a single decision.
- Therefore this is **causal inertness**, not a measurement failure. The KILL is not a false negative.

---

## Licensed claim (scoped, per §8 of the signed protocol)

Static injection of the shared layer-11 task direction does not move decisions on EXP092-B (no significant transfer at any phrasing; Δ = 0.0, all McNemar p = 1.0). The EXP092 correlational signal is causally inert under static injection — **information ≠ influence at layer 11**. The layer-20 boundary generalizes. This falsifies "≥10pp causal transfer via a shared static direction at layer 11" — it does not license "layer 11 is useless" (the information is present, licensed by EXP092). Per-item (non-shared) directions, gated/dynamic mechanisms, and multi-layer compositions remain open as EXP094+ material.

## Non-blocking observation (process, not verdict)

Per-item margins (mB/mP/mN, 60×3 floats) are computed in memory and never persisted — only aggregates reach `report.json`. Law #13 ("preserve raw instance logs") is satisfied in letter for guards but not for the decision data itself. A future bundle should write the per-item margin CSV; it costs nothing and would let a reviewer recompute from raw records rather than entailed aggregates. This does not affect this verdict: b = c = 0 makes the aggregates fully determining.

---

**Files:** this review at `experiments/protocols/REVIEWS/EXP093_LAW14_VERDICT_REVIEW_2026-09-25.md`; LOG-4352 appended to `reports/research_log.md`. Committed locally; not pushed (founder push policy).
