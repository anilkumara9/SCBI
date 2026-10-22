# EXP098 Verdict Review — Independent Law #14 Verdict Lane (2026-09-28)

**Verdict: PIVOT (premise) — NOT SUPPORTED for the composition claim. Binding.**

*Reviewer: Independent Scientific Mentor & Adversarial Reviewer (fresh lane — did not write the protocol, reviews, repair, or executor). All numbers below recomputed independently from the 300-row primary CSV (`per_item_records.csv`); zero discrepancies with the executor's mechanical read-out.*

## Decision-table walk (first-match-wins, §3 of the licensed v2 protocol)

- **Step 0 (foundation): PASS.** Constructor re-hash `5e03f206…917f361` matches the frozen pin exactly; per-item B-decision agreement **60/60** vs the archived EXP094 baseline (recomputed item-by-item from `experiments/runs/EXP094_peritem_l11/out/per_item_records.csv`); L11 degeneracy sanity recomputed 0.7923 vs archived 0.7923 (|diff| < 0.05). No HOLD.
- **Step 1 (delivery): PASS.** 360/360 cell-rows in band [0.285, 0.475] across exactly the six injected (layer, arm) cells; 0 out-of-band rows; 0 exclusions. (Delivery probe scope per F3: non-injected cells never probed.)
- **Step 2 (degeneracy): PASS.** {d_i^(20)} mean pairwise |cosine| = 0.6639 < 0.95 — gate not fired; {d_i^(11)} = 0.7923 < 0.95. The L20 direction set is a genuine per-item set, not degenerate.
- **Step 3 (regime routing): LIVE.** W-joint flips = 12 ≥ 1 (machine-written routing confirmed from the CSV).
- **Step 4 (premise PIVOT): FIRES.** L20-only flips = **6** ≥ 6 (b=0, c=6, all right→wrong, McNemar-exact doubling p=0.03125); L11-only = 3 < 6. The individual-inertness premise was wrong at this bench/strength — the composition question is **unasked**; re-derive before composing.
  - **Named observation does NOT fire:** it requires L20-only ≥ 6 **with p < 0.01**. p=0.03125 fails the bar. There is no licensed single-layer L20 positive. The p=0.03125 movement is reported as an observation only (in the pre-registered near-miss band, never a discovery).
- **Steps 5–8: not reached.**

**Robustness note:** the PIVOT is boundary-robust — had L20-only been 5, step 5 (fragility PIVOT: Joint 7 ≥ 6 AND W-joint 12 ≥ 6 jointly) would have fired instead. The verdict is PIVOT either way; only the sub-case differs.

## Decisive numbers (independently recomputed)

| Contrast vs B | Flips | b (0→1) | c (1→0) | McNemar p (doubling) | ΔM (logit-margin) |
|---|---|---|---|---|---|
| L11-only | 3 | 1 | 2 | 1.0000 | −0.0212 |
| L20-only | **6** | 0 | 6 | 0.03125 | −0.0089 |
| Joint | 7 | 0 | 7 | 0.015625 | −0.0425 |
| W-joint | 12 | 3 | 9 | 0.1460 | +0.0705 |
| Joint vs W-joint (diagnostic) | 13 | 6 | 7 | 1.0000 | — |

- B correct: 36/60 (matches the archived baseline exactly).
- Strata (A-first / C-first), ΔM: L11-only (+0.1565/−0.1990); L20-only (+0.3777/−0.3955); Joint (+0.4964/−0.5815); W-joint (−0.1175/+0.2585).
- Guards: Δθ=0 pre/post (LOG-331 pin); 120/120 per-layer norm-ties; ties 0; 368 passes ≤ 500 cap; single pinned CPU environment; $0; no GPU contact.
- Margin-shift ledger (§2.5, recomputed; shift-consistency verified 0 violations): 7 joint-flip items — **all 7 additive-explained**, 0 interaction-candidate, max |Δm_int| = 0.1763. The decomposition does not alter the verdict (it classifies only a CONTINUE); recorded for the record.

## What this verdict means (fenced)

- **PIVOT (premise)** maps to **Not supported for the composition claim** per the table's binding step→verdict mapping.
- The composition question cannot be cleanly asked: the L20-only premise arm moved at the bench/strength tested, so "two individually-inert interventions" is false at L20. Re-derivation is required before any composition test — a dedicated single-layer L20 design is new-design territory (the named observation's p<0.01 bar was not met, so no follow-up is licensed by this verdict).
- This verdict does **not** alter EXP094/095/096/097; does not license any claim about L20-only beyond the observation above; does not license three-layer compositions, other layer pairs, or any positive mechanism claim.
- The executor's pre-flight G5-probe repair (norm-0.38-absolute probe → constructed-d₀ probe at the operating ratio, per EXP094 precedent) was transparent and protocol-conformant; no deviation.

## Verdict record

Logged as **LOG-4423** (fresh highest-LOG check immediately before writing; was LOG-4422). Protocol reviewed: `research/innovation/S6-2_PREREG_DRAFT_v2_2026-09-28.md` (untouched). Records: `experiments/runs/EXP098_multilayer_composition/out/` (untouched).
