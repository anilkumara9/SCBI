# Law #14 Independent Execution Review — EXP133 Attempt 4 (2026-09-30)

**Reviewer:** independent lane (no involvement in the Amendment D diagnosis, the executor repair, or the attempt-4 run).
**Verdict under review:** EXP133 attempt 4 — **KILL** (LOG-4814): ΔM_geo = 0, ĉ_geo = 0.0374 < 0.1, McNemar(geo vs base) one-sided p = 1.0, 0 exclusions, pivot_prompts = 0.
**Review verdict: SIGN-WITH-FIXES** — one narrow documentation fix (F1). The KILL stands on its evidence; the fix closes a stale premise in the pre-reg's KILL-row narrative. The KILL becomes binding once the CEO appends the erratum (a 2-minute edit; no re-execution).

## 1. Delivery verification (the crux) — PASS

This is what the attempt-3 KILL lacked, and it is now present three ways:

- **(h) positive control:** the run logs record `r = 1.0000001 ∈ [0.99, 1.01]` — PASS, in both the smoke and full-run logs. The control ran before the first injection forward per Amendment D §3.
- **Records-level delivery:** all 60 (prompt, injection-arm) margin displacements are **nonzero** (spot: geo_v1 on prompt 0 = 9.78e-06; geo_v2 = 1.78e-07; random arms 4.6e-06 / 6.3e-07). The attempt-3 blind-tap signature (max|Δcos| = 0.000e+00 on every arm) is gone. The blind-readout 0/0 → 1.0 median_r signature is absent.
- **Hash pin:** `out/exp133_records.json` sha256 = `6174f6d3029aae1b7a8c60c195d03c0bf1f3fdb3ef949426e1693b0836f092f3`, matching the LOG-4814 pin exactly. The report's `records_pin` agrees.

The honest signature is now visible: the tap moves on every injection (delivery ✓) while decisions never move (ΔM = 0) — exactly what a decision-orthogonal direction should produce.

## 2. Repair confinement — PASS

`git diff 0efc6e3 8d764d1 -- run_exp133.py`: **28 insertions, 1 deletion.** The insertions are exactly the §5b (h) positive-control block; the single modified line is `register_forward_hook(hook_fn)` → `register_forward_hook(hook_fn, prepend=True)`. No other executor change. Clearance (LOG-4813) held.

## 3. Breaking points — all PASS

| BP | Evidence |
|---|---|
| (a) backbone | weights pre+post `ec276abe…` = LOG-331 pin, bit-identical |
| (b1) v1 re-pin | `9b527c02…` = Amendment B registered pin |
| (b2) v2 run-twice | `d633b897…` both runs, bit-identical |
| (b3) B_agg | `d3556d83…` = EXP131 ground-truth pin |
| (d) budget | recomputed B matches 0.50578119 within 1e-4 (Amendment C); tangent steps worst rel dev 1.4e-16 (bar 1e-6); retraction bound held on all 50 path-arms (worst shortfall 1.5e-6); one-shot arms at B ± 1e-6 |
| (h) positive control | r = 1.0000001, PASS |

Rank-trend 7/10 vs bar 8: not a conjunct of the firing KILL row, so the miss does not block the verdict; KILL-first precedence was correctly applied (the §0-gate KILL fires before any CONTINUE consideration). LOG-4814's phrasing ("the rank-trend … KILL branches would independently fire") is sloppy — the rank-trend KILL row requires ΔM_geo > 0 and does not fire here — but the verdict does not depend on it. Noted, non-blocking.

## 4. Decision-table application — PASS

- ΔM_geo = 0: verified independently — zero nonzero `dm` entries across all 70 (prompt, arm) pairs; spot-checked decisions identical across arms (E2/E2/…, E1/E1/…).
- PIVOT trigger: 0 prompts with midpoint ĉ ≥ 0.1 at k ∈ {2,3} (verified from `midpoint_c_per_prompt`; max observed ≈ 0.064). PIVOT check correctly precedes the endpoint KILL per the precedence note.
- First KILL row fires: ΔM_geo = 0 AND PIVOT trigger negative. KILL-first precedence honored.
- Characterization: ĉ_geo mean = 0.03736427 (verified from `c_geo_per_prompt`; range 0.0643…0.0089, 0 exclusions) < 0.1 → "decision-orthogonal" characterization per the §4/F3 gate. Correct.
- McNemar: 0 discordant pairs → one-sided p = 1.0. Correct.
- B_agg-path arm: zero decision moves → the RUN-INVALID row does not fire. Correct.
- No CONTINUE/INCONCLUSIVE/PIVOT corner arguably applies.

## 5. Scope honesty — FINDING F1 (the fix)

The pre-reg's KILL-row narrative states: "no targeting claim over TGA dynamics is ever licensed — **not one-shot (LOG-4766)**, not multistep-geodesic (this verdict), not any budget escalation (fenced by EXP095, LOG-4400)."

LOG-4766 (EXP131's KILL) is **suspended** (LOG-4810, RUN-INVALID apparatus defect). The "not one-shot" clause therefore rests on a suspended premise. The verdict as *reported* (LOG-4814) is honestly fenced — it claims only the multistep-geodesic closure and logs an explicit scope caveat — but the signed pre-reg's narrative retains the stale clause, and a future reader applying the table could mis-cite one-shot as closed.

**Fix F1:** the CEO appends a dated scope-erratum note to `research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md` (appended, not altering signed text): the KILL row's "not one-shot (LOG-4766)" clause is suspended per LOG-4810; the binding closure from this verdict is the **multistep-geodesic branch only**; one-shot remains UNTESTED. The verdict's validity does not depend on the stale clause (the §0 gate fired on measured numbers), so no re-execution is required.

## 6. Record preservation — PASS

Attempt-3 void records preserved as `exp133_records_attempt3.json` (sha256 `5078f518…` = LOG-4807 pin, verified). Attempt-4 records distinct and pinned (verified §1). Prior void reports retained.

## Disposition

**SIGN-WITH-FIXES.** Apply F1 (CEO, ~2 minutes, no re-execution); the EXP133 attempt-4 KILL is then **binding**: the geodesic-multistep TGA-v₁ steering branch is dead at matched budget with verified delivery, and TGA survives only as a dynamics-characterization quantity (EXP127's CONTINUE). The one-shot branch stays UNTESTED — that disposition belongs to the EXP131 track, not this verdict.
