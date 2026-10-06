# EXP148 — Independent Verdict Review (2026-10-06)

**Reviewer:** independent (did not execute EXP148). **Verdict on the verdict: ADOPT.**

## 1. Mandate

Review the EXP148 CONTINUE verdict (`EXP148_VERDICT_2026-10-06.md`) against the signed
pre-registration (`EXP148_PREREG_2026-10-06.md` §4), the results JSON
(`EXP148_RESULTS_2026-10-06.json`), and the per-item records
(`experiments/runs/EXP148/exp148_per_item.jsonl`, 540 records). Binding: ADOPT or OVERTURN.

## 2. Independent recomputation [FACT]

Recomputed from the per-item records (not from the report's arithmetic):

- S vs C discordant pairs: **b=52, c=12** — reconstructed exactly from per-item correctness.
- S vs B discordant pairs: **b=14, c=59** — reconstructed exactly.
- Arm accuracies: B=119/180=0.6611, C=34/180=0.1889, S=74/180=0.4111 — match the report.
- Exact one-sided McNemar p (H1: S>C): **2.2833e-07** (Bin(64, 0.5), P(X≥52)).
  Reported 2.283e-07 ✓.
- Two-sided p: 4.5666e-07 (reported 4.567e-07 ✓).
- Net δ̂ = 40/180 = 0.22222 (reported 0.2222 ✓).
- 95% Wald CI (S7-1 §2.2 convention): **(0.14139, 0.30306)** (reported (0.1414, 0.3031) ✓).
- S vs B one-sided p (H1: S>B) ≈ 1.0, net −0.25 ✓.

## 3. Verdict-table fidelity [FACT]

Pre-reg §4, precedence RUN-INVALID > HELD > KILL > CONTINUE:

- **RUN-INVALID:** requires guard (a)/(c)/(e)/(f)/(g)/(h) trip. None tripped
  (WRITE rate 180/180, tokens B=15/C=120/S=120, 45,900 ≤ 50k, Δθ=0 match). Not RUN-INVALID.
- **HELD:** requires guard (d) or (f′) trip. (d): 0.6611 ∈ [0.2, 0.8] PASS.
  (f′): S/C = 1.0 ∈ [2/3, 3/2] PASS. Not HELD.
- **KILL:** requires (i) one-sided p ≥ 0.1 AND (ii) two-sided p ≥ 0.1 AND
  (iii) CI upper < +0.10. Observed p = 2.3e-07, CI upper = 0.3031.
  All three prongs fail → KILL does **not** fire. PIVOT attaches to KILL → no PIVOT.
- **CONTINUE:** requires one-sided p < 0.05 ✓ (2.3e-07) AND net δ̂ ≥ +0.10 ✓ (0.2222)
  → **CONTINUE fires.**

The verdict report applies the table exactly. No misapplication.

## 4. Guard integrity [FACT]

Spot-checked from per-item records:

- (e) discipline delivered: WRITE-span regex `WRITE\(fact\d+,` matches in **180/180**
  S generations (rate 1.0000 ≥ 0.5) ✓.
- (f) compute delivered: mean new tokens B=15.0, C=120.0, S=120.0 —
  C, S > 2×B ✓.
- (f′) budget matched: S/C = 1.0000 ∈ [0.667, 1.5] ✓.
- (d) calibration: B = 0.6611 ∈ [0.2, 0.8] ✓.
- Strata balanced 45/45/45/45; 540 records = 180 items × 3 arms ✓.
- Pins/hashes: carried from the LOG-4956 verification (scripted character-identical
  comparison); the verdict report's values match the results JSON exactly.

No guard that should have tripped was missed.

## 5. Scoring fidelity [FACT]

Verified `correct == (first_token == normalized gold)` on all **540/540 records —
zero mismatches**. The stored `first_token` field matches the deterministic rule;
no post-hoc re-scoring. All 180 C and 180 S generations contain `ANSWER:`
(zero missing), so the pre-registered "no ANSWER: → 0" fallback never triggered —
no hidden rescues. Scoring applied exactly as pre-registered in §5.3.

## 6. The C-arm caveat [INTERPRETATION]

The verdict report is honest: §5 states C = 0.1889 absolute, S (0.4111) does not
beat B (0.6611), and the licensed claim is "discipline beats budget-matched CoT"
— not "scratchpad beats the best baseline." The §4 CONTINUE bar is defined on
S vs C only, and the verdict follows the table; the caveat scopes the claim
without undermining it. The report does not overclaim. The stratum table is
labeled descriptive; no stratum is promoted to a decision (Law #9 clean).

## 7. In-principle variability [FACT]

Scored signals vary across items in principle: first-token correctness differs by
stratum (B: 0.98 → 0.27), and S−C net spans +0.0444 → +0.4667 across strata.
Not degenerate-by-construction (2026-10-05 lesson applied).

## 8. Verdict

**ADOPT.** The CONTINUE verdict stands as reported: the arithmetic is exact,
the decision table is applied faithfully, the guards hold, the scoring matches
the pre-registration, and the report's caveats are honest. EXP148 is the
program's first capability entry — WRITE/READ discipline beats budget-matched
CoT by +22.2pp (p = 2.3e-07) at Δθ=0 on Pythia-410m, scoped to the S-vs-C
comparison as the pre-reg licenses.

*Review completed 2026-10-06. Reviewer independent of the EXP148 execution lane.
No forwards run; $0.*
