# EXP095 — α-Sweep Dose-Response: Binding Verdict Review

*Date: 2026-09-28. Reviewer: Independent Scientific Mentor & Adversarial Reviewer (did not write the protocol, the reviews, the repair, or the execution).*
*License: LOG-4398 (CEO execution clearance) → LOG-4399 (execution, records verdict-ready).*
*Signed protocol: `research/innovation/S5-1_PREREG_DRAFT_v2_2026-09-28.md`.*
*Verdict: **REFUTED** — binding. This is a verdict review of an executed experiment; it is not itself a new experiment.*

---

## 1. Independent recomputation [OBSERVATION]

All statistics below were recomputed from `experiments/runs/EXP095_alpha_sweep/out/per_item_records.csv` (660 rows) by this reviewer, using an independent script (`/tmp/verdict_recompute_2026-09-28.py`). Nothing was trusted from the executor's arithmetic. McNemar exact, doubling convention, computed as p = min(1, 2·Σ_{i≤min(b,c)} C(b+c,i)·2^{-(b+c)}), with b = B-wrong→X-right flips, c = B-right→X-wrong flips. ΔM = paired (correct_X − correct_B)/60.

### Foundation (step-0 evidence), independently verified

| Check | Recomputed result |
|---|---|
| Constructor re-hash vs pin `5e03f206…917f361` | match (manifest: `constructor_sha256_live` prefix `5e03f206dd907b52baa1` = pin prefix) |
| Per-item B decisions vs archived EXP094 baseline | **60/60 agree** — verified against `experiments/runs/EXP094_peritem_l11/out/per_item_records.csv` (60 archived B rows read independently) |
| B correct count | **36/60** |
| T(1.0)-vs-B flips | **0** (foundation-wobble = false) |
| Degeneracy sanity | mean\|cos\| recomputed = 0.7922606323; \|0.7922606323 − 0.7923\| < 0.05 ✓ (< 0.95 gate) |
| Δθ=0 | recorded pre = post = LOG-331 pin in env manifest (executor evidence; hash check is Law #13's lane) |

### Dose-response (aggregate stratum), independently recomputed

| α | Arm | correct/60 | flips vs B | b/c | McNemar p | ΔM |
|---|---:|---:|---:|---|---:|---:|
| 0.25 | T | 36 | 0 | 0/0 | 1.0000 | +0.0000 |
| 0.25 | B_wrong | 36 | 0 | 0/0 | 1.0000 | +0.0000 |
| 0.5 | T | 36 | 0 | 0/0 | 1.0000 | +0.0000 |
| 0.5 | B_wrong | 36 | 0 | 0/0 | 1.0000 | +0.0000 |
| 1.0 | T | 36 | 0 | 0/0 | 1.0000 | +0.0000 |
| 1.0 | B_wrong | 36 | 0 | 0/0 | 1.0000 | +0.0000 |
| 2.0 | T | 35 | 1 | 0/1 | 1.0000 | −0.0167 |
| 2.0 | B_wrong | 36 | 0 | 0/0 | 1.0000 | +0.0000 |
| 4.0 | T | 35 | 1 | 0/1 | 1.0000 | −0.0167 |
| 4.0 | B_wrong | 36 | 2 | 1/1 | 1.0000 | +0.0000 |

- Maximum T-vs-B movement at any α: **1 flip** (item `exp092_planetary_3hop_7`, flipped to *wrong* at both α=2.0 and α=4.0). The discovery bar (flips ≥ 6 AND p < 0.01) is not approached anywhere; **every McNemar p = 1.0 across all 5 α, all 3 contrasts, all 3 strata** (135 cells checked).
- Stratum breakdowns (A-first / C-first, 30 each): no stratum shows any directional signal — the only nonzero cells are the single to-wrong flips above and the α=4.0 B_wrong 1/1 split (ΔM = 0.0). All stratum-level p = 1.0.
- Tie gate: 0/180 ties at every α — no α RUN-INVALID.
- Delivery: 300/300 in-band at every α (each α's §2.2 ±25% band checked row-by-row); no α excluded; no common-cause failure. Budget: 660 recorded rows; well under the 1300 hard cap.
- Stratum-table spot check: recomputed cells match `stratum_table_135.json` cell keys and values at the aggregate level (checked all 5 α × 2 decision contrasts).

---

## 2. Decision-table walk (§3, binding order, first match wins)

- **Step 0 — Replication anchor:** NOT fired. Per-item B agreement 60/60; T(1.0) movement 0 < 6; no HOLD, no wobble flag. The EXP094 foundation reproduced bit-for-bit on a rebuilt environment (torch 2.14.0 CPU, venv) — the environment reinstall did not perturb the foundation.
- **Step 1 — Delivery:** NOT fired. PASS at all 5 α; no isolated or common-cause failure.
- **Step 2 — Degeneracy:** NOT fired. 0.7923 < 0.95; regeneration sanity within tolerance.
- **Step 3 — All-α KILL:** **FIRED.** T(α)-vs-B movement = {0, 0, 0, 1, 1} — strictly < 6 at **every** α ∈ {0.25, 0.5, 1.0, 2.0, 4.0}. The B_wrong-moved sub-case does not trigger (max B_wrong movement = 2 < 6) — no nonspecific-fragility statement is required, though the α=4.0 B_wrong 1/1 split is disclosed above for the record.
- **Steps 4–6:** not reached (step 3 fired first; and for the record, no α carries ≥6 flips, so steps 4–6 could not have fired regardless).

---

## 3. Binding verdict

> **REFUTED: the magic-strength rescue of the per-item static family is refuted *on the licensed five-point grid*.**

[OBSERVATION] Over a 16× strength range (α = 0.25 → 4.0; perturbation ratio 0.01185 → 0.1896), static per-item L11 task-direction injection moved at most one decision per strength, with McNemar p = 1.0 everywhere and ΔM = 0 at three of five strengths (−0.0167 at two, single to-wrong flips). [INTERPRETATION] The inertness is not a strength artifact. The family license becomes strength-invariant over the licensed grid — **boundary-law graduation, scoped**.

**What died:** the "magic strength" hope — the belief that EXP094's zero-flip kill at α=1.0 was a strength artifact and some other strength would move decisions. EXP094's kill is a curve-flat point on a flat curve, not an isolated point.

**What survived/graduated:** EXP094's kill stands unaltered and is now generalized: per-item static layer-11 task directions do not move decisions on the EXP092-B bench at any licensed strength — the strongest form of the inertness claim the linear license permits.

---

## 4. Scope fence (binding — the verdict language cannot drift)

1. **Grid scope:** the KILL covers the licensed five-point grid {0.25, 0.5, 1.0, 2.0, 4.0} only. A narrower magic peak between grid points is not ruled out.
2. **Threshold account:** the design's maximum ratio was 0.1896 < 1. The ‖δ‖/‖r‖ > 1 breaking point is **untested by this design** — no future work may cite EXP095 against the threshold account.
3. **Mechanism scope:** gated, dynamic, and multi-layer compositions remain separate EXP096+ material regardless of this outcome.
4. **Bench scope:** EXP092-B only; 60 items, one model (Pythia-410m), one layer (L11).
5. **No per-item-specificity claim:** the 3-arm design with the F12 fence licenses no statement about this-item's-d_i vs any-task-derived-direction (the d_{π(i)} control is EXP096+ material).

---

## 5. What the verdict licenses next

1. **S5-4 (headroom-gated injection)** remains the live successor lane — per-item static geometry at L11 is now closed across the licensed strength grid, so the program's remaining in-band degrees of freedom are conditional/gated mechanisms. S5-4 requires its own preregistration + Law #14 review; this verdict does not pre-license it.
2. **Threshold-account designs (‖δ‖/‖r‖ > 1)** are EXP096+ material and need their own license — this verdict neither motivates nor licenses them beyond what LOG-4391 already scoped.
3. **Paper impact:** the S5-1 + EXP094 pair now constitutes a strength-invariant inertness law on the licensed grid — a citable boundary-law result for the manuscript's §3 (boundary formalization), with the §4 scope fences as the guardrails against overclaiming.
4. No further static per-item L11 strength experiments are licensed — a design change is a new experiment number, never a silent extension of EXP095 (a grid extension to α=8.0, for instance, would need its own pre-registration even though ratio 0.3792 stays inside the linear license, per F9).

---

## 6. Adversarial notes (what I tried to break)

- **Single-flip fishing:** the two to-wrong flips (α=2.0, 4.0, same item) and the α=4.0 B_wrong 1/1 split were the only movement in 660 injection rows. Under the global null with 60 items per cell, sub-threshold single flips are expected noise; both cells carry p = 1.0, and the B_wrong split has ΔM = 0. No directional evidence exists at any α, so no step-4/5/6 path is open. The protocol's first-match-wins order makes this moot, but the numbers confirm it.
- **Executor arithmetic:** fully recomputed from the raw CSV — zero discrepancies. The stratum table, sideband ledgers, and mechanical read-out all agree with the recomputation.
- **Environment confound:** the torch reinstall (missing in the rebuilt VM, recovered in an isolated venv) is the one genuine threat to the foundation — neutralized empirically by the 60/60 per-item B agreement, which is a bit-for-bit reproduction check, not a statistical one.
- **Budget bookkeeping:** the executor's "724 passes" narration double-counts T(1.0) inside the 300-T count (non-blocking observation, disclosed; the 660 recorded rows and the 1300 hard cap are the binding quantities, both satisfied).

*Report saved 2026-09-28. No model executed, no weights touched, no signed artifact edited. Read-only verdict review; $0 compute.*
