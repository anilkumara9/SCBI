# EXP096 Verdict Review — Headroom-Gated Injection at α=8.0 (2026-09-28)

*Independent verdict lane. The reviewer did not write the S5-4 protocol, the Law #14 reviews, the v2 repair, or the executor. Every statistic below was recomputed from the raw 102-row `per_item_records.csv` by this lane — zero numbers were trusted from the executor. Verdict is binding.*

**Verdict: REFUTED.** The headroom-gated rescue of the per-item static family is refuted on the licensed reach-calibrated set at α=8.0 — inertness is structural, not a headroom artifact; the threshold account ("the push is real but too weak except near the boundary") is falsified within the linear license up to ratio 0.38 at the rescue's best shot; the static per-item family is closed conditionally too.

## 1. Recomputed numbers (independent; zero discrepancies with the executor's arithmetic)

| Contrast (gated set G, |G|=21) | Correct | Flips vs B | McNemar b/c/p (exact, doubling) | ΔM |
|---|---|---|---|---|
| B (baseline) | 16/21 | — | — | — |
| T(8.0) vs B | 15/21 | **3** (< 6) | b=1, c=2 → **p=1.0** | −0.0476 (−1/21) |
| B_wrong(8.0) vs B | 17/21 | **3** (< 6) | b=2, c=1 → **p=1.0** | +0.0476 (+1/21) |
| T(8.0) vs B_wrong(8.0) [diagnostic-only] | — | 4 | b=1, c=3 → p=0.625 | −0.0952 |

Flip ledgers (verified row-by-row):
- T: `exp092_planetary_2hop_2` wrong→right; `exp092_planetary_3hop_7` right→wrong; `exp092_elemental_2hop_0` right→wrong. **Sign-heterogeneous; ΔM_T < 0.**
- B_wrong: `exp092_planetary_2hop_0` right→wrong; `exp092_planetary_2hop_2` wrong→right; `exp092_planetary_2hop_9` wrong→right.

Strata (verified): A-first (n=13) ΔM_T = +0.0769 (b=1, c=0, p=1.0); C-first (n=8) ΔM_T = −0.25 (b=0, c=2, p=0.5). Ties: 0/42 gated injection rows → tie gate not triggered.

McNemar spot-verification of the executor's stratum table: agg__TW b=1,c=3 → 2·(1+4)/16 = 0.625 ✓; C__TB b=0,c=2 → 2·1/4 = 0.5 ✓; C__TW b=0,c=3 → 2·1/8 = 0.25 ✓. All 9 cells consistent.

## 2. §3 decision-table walk (binding order, first match wins)

**Step 0 — Foundation gates: no HOLD.**
- Constructor re-hash: `5e03f206…917f361` — verified independently byte-for-byte against the live file. PASS.
- B decisions: **60/60 exact match** vs the pinned EXP094 archive (archive SHA-256 `9ada6ef9…b366d149` verified independently byte-for-byte). PASS.
- Gate manifest: recomputed G from the pinned archive = Appendix A **21/21 member-for-member**; gate consistent with |m_B| ≤ 0.90 across all 60 items (min outside-gate |m_B| = 1.0442, max inside-gate = 0.8904). PASS.
- Degeneracy sanity: 0.7923 vs the 0.7923 reference — within tolerance. PASS.
- Baseline composition: 5 wrong / 16 right; 13 A-first / 8 C-first — matches the protocol's frozen values. PASS.

**Step 1 — Delivery: no HOLD.** 42/42 gated rows in [0.2844, 0.4740]; 0 out of band; no exclusions. (Attempt-1 HOLD audited separately in §4 — resolved under the diagnosis lane.)

**Step 2 — Degeneracy: no Underdetermined.** Mean pairwise |cosine| = 0.7922606323 < 0.95.

**Step 3 — Gated KILL: FIRES.** Gated T(8.0)-vs-B movement = 3 < 6 → **Refuted**. Steps 4–6 are not reached (first-match-wins).

For the record, the later steps' conditions were independently evaluated and none would have fired anyway:
- Step 4 (fragility PIVOT): requires T ≥ 6 AND B_wrong ≥ 6 jointly — T=3, B_wrong=3. Not met.
- Step 5 (suggestive PIVOT): requires flips ∈ [2,5] ALL wrong→right — T's 3 flips are 1 wrong→right + 2 right→wrong, and ΔM_T < 0. Not met.
- Step 6a (heterogeneity): noted as an observation — A-first ΔM_T = +0.077 while C-first ΔM_T = −0.25 < −0.05 — but step 3 fired first, so no step-6 routing applies.

## 3. In-run reach verification (§2.4)

Realized max|shift(8.0)| = **0.8621**. Neither tripwire fired (not > 1.125, not < 0.45) → reach as calibrated; no fence modification to the step-3 KILL required. The KILL stands in its strict-reach form.

## 4. Attempt-1 HOLD audit

- HOLD.txt records a STEP-1 HOLD: 21/42 gated rows out of band (>2) — common-cause suspected.
- DIAGNOSIS.md identifies an **executor bug, not a protocol defect**: the executor built g_i at norm d_norm_alpha8 (already T(8.0)'s per-item norm) then injected 8·g_i, double-scaling B_wrong to ratio ~3.03 — outside the band on all 21 B_wrong rows.
- Confirmed: **no injection passes executed before the HOLD** (only B/foundation passes); the re-run proceeded under the protocol's diagnosis lane (HOLD → diagnose → fix → re-verify all guards) — never a silent re-run; attempt-1 artifacts preserved at `out/attempt1_hold_diagnosed/` (HOLD.txt, DIAGNOSIS.md, run log). The final delivery manifest shows 42/42 in band with an explicit norm-tie assertion added. Process discipline held.

## 5. What died, what graduated

- **What died:** the threshold account as a rescue of the per-item static family — "the push is real but too weak except near the boundary." At the rescue's best shot (α=8.0, the maximum interpretable strength inside the linear license, aimed at exactly the 21 items within calibrated reach), the task direction moved 3 items with p=1.0, net negative, sign-heterogeneous — while the random arm moved 3 items with equal ease. The items are flippable by large nudges; the task direction does not move them.
- **What graduated:** the static per-item family is closed **conditionally** — within the linear license up to ratio 0.38. This is the program's first mechanism family closed conditionally (with the F3 "conditionally" qualifier kept everywhere, as required).
- **Boundary-law pair:** EXP095 (strength-invariant inertness, 16×) + EXP096 (headroom-conditional inertness at 8× strength) now form a citable two-experiment closure of the static per-item L11 family within its license.

## 6. Scope fences (binding)

This verdict does NOT touch: the >0.4740-ratio regime (threshold account above ratio 0.4740 untested); non-static conditional mechanisms (attention-state-gated, dynamic, multi-layer); other layers, benches, or models. A gated zero here must never be cited against the threshold account above ratio 0.4740 — per §6 item 10 of the protocol.

## 7. What it licenses next

- The declined **α=16 variant is NOT licensed** by this verdict: the protocol licensed it as follow-up ONLY if this design PIVOTed on fragility (moot — B_wrong=3 < 6) or yielded a suggestive signal (failed — flips not all wrong→right). Both conditions failed; the α=16 variant stays unlicensed EXP097+ material.
- **No further static per-item L11 experiments are licensed** (LOG-4400's bar stands, extended by this verdict to conditional static variants within the license).
- Live lanes: gated/dynamic mechanisms, multi-layer compositions, >0.4740-ratio regimes, other layers/benches — each requires its own pre-registration and Law #14 review. Nothing is pre-licensed.

## 8. Records

- `experiments/runs/EXP096_headroom_gated/out/`: `per_item_records.csv` (102 rows), `stratum_table_27.json`, `mechanical_readout.json`, `gate_manifest.json`, `constructor_manifest.json`, `env_manifest.json`, `delivery_probe_log.json`, `exp096_report.json`, `exp096_run_log.txt`, `artifact_hashes.txt` (SHA-256 per artifact), `attempt1_hold_diagnosed/` (HOLD.txt, DIAGNOSIS.md, run log).
- Runners: `run_exp096.py`, `score_exp096.py`; `test_prechecks.py` 18/18 PASS.
- Licensing chain: LOG-4391 (PROPOSAL) → LOG-4401 (v1 draft) → LOG-4402 (Law #14 ACCEPT-WITH-FIXES) → LOG-4403 (v2 repair) → LOG-4404 (delta re-verification SIGN) → LOG-4405 (CEO clearance, minted EXP096) → LOG-4406 (execution) → this verdict (LOG-4407).

*Verdict rendered 2026-09-28 by the independent EXP096 verdict reviewer. $0 compute beyond reading records; no execution; no signed artifact edited.*
