# Law #14 Independent Review — GEOSTEER Multistep Pre-reg DRAFT (LOG-4792)

**Reviewer lane:** LOG-4792 (CEO pre-assigned). **Independent:** the reviewer did not write the gate or the pre-reg.
**Artifact reviewed (exact version):** `~/workspace/SCBI/research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md`
**Supporting context read:** `~/workspace/SCBI/research/strategy/GEOSTEER_MULTISTEP_WORTHIT_2026-09-30.md`; LOG-4790 and LOG-4791 entries in `reports/research_log.md`; `~/workspace/SCBI/AGENTS.md` (14 Laws).
**Scope:** paper only, $0 CPU. Review only — no redesign, no fixes applied, no experiment number, no execution licensed.

## Verdict: SIGN-WITH-FIXES

The design is scientifically licensed and its falsification discipline is genuine. Five specification-level defects must be repaired by the author lane before this draft can advance to a signed pre-reg. None requires redesigning the science; all are internal-consistency or mechanical-specification fixes.

---

## What passes

**License chain (Q4 / §7).** The escalation is the LOG-4751-named instrument class, conditional on EXP131's null; LOG-4766 delivered the null. The seventh-item fences are each honored with a named mechanism: EXP095 dose kill → B constant (§0(d), §7.2); EXP130 REJECT → decision-readout only (§0(g), §7.3); line-7637 cull → no labels, no trained head, no learned objective (§0(g), §7.4); EXP131's KILL → the licensed question is bounded to this instrument (§7.1, §7.4). "New instrument class, not a dose tweak" is honestly sustained: total injected norm is identical to the dead one-shot arm; the licensed variation is path geometry at fixed norm. The GEOSTEER paper's learned objective is explicitly excluded, which narrows rather than stretches the license — acceptable.

**Dose fence (§0(d), §3.4, §7.2, §9).** B = 0.50578119 is copied verbatim from LOG-4766 with an independent recompute-and-assert (not recompute-as-new — the Law #2 handling is correct). K-sweeps, larger benches, and GPU stages are fenced in §9 as founder-gated, not licensed. No plausible executor reading of this draft authorizes a budget increase.

**Status honesty (§6, §8, §9, header).** DRAFT / licenses-nothing / no-experiment-number is stated in the header, §2, §6, and §9 with no hidden licensing language. §8's bounded-claim discipline ("closes the question at matched budget on this bench") is exemplary.

**Statistical bars (§3.7).** McNemar one-sided p ≤ 0.05, ĉ_geo < 0.1 → KILL, rank-trend, best-random-path pinned before inspection, B_agg null-control — all registered before any execution (none has occurred). Law #9 satisfied.

**Breaking-point coverage (§0(a)–(g), §3.1, §3.2).** Δθ=0 pre+post pin, direction re-pins (no re-derivation), no-finite-differences (EXP128 constraint), norm-budget audit, B_agg null-control, no-training, decision-readout-only, plus bench re-verification (§3.1) and ĉ-exclusion cap (≥3 → void). Conjunctive ordering per Law #9 (§5).

**Laws check.** No Law #2 violation: B, ĉ = 0.0374, and the LOG-331 hash are in-log values; "70 forwards" = 7×10 arithmetic. No Law #4 shift: one falsifiable hypothesis sentence (§1). No Law #9 cherry-picking: metrics fixed pre-execution. Citation (GEOSTEER arXiv:2609.10658) is anchored to the in-log LOG-4751 record per program convention.

---

## Required fixes (author lane applies; re-review not required if applied verbatim)

**F1 — Retraction shortens each step; the norm audit as written can void every run (§3.4, §0(d)).**
§3.4 asserts "[FACT] Each step has exact norm ‖δ_k‖ = α by construction." Under the natural reading δ_k = x_{k+1} − x_k, this is false: the sphere retraction x_{k+1} = (x_k + t_k)·(‖x_0‖/‖x_k + t_k‖) shortens the step, since t_k ⊥ x_k gives ‖x_k + t_k‖ = √(‖x_0‖² + α²) > ‖x_0‖. The relative shortfall is ≈ α²/2‖x_0‖² per step, and the total ∑‖δ_k‖ < B strictly. Against the 1e-6 relative tolerance in §0(d), the per-step and total audits may therefore fail deterministically (whether they do depends on ‖x_0‖, which is not pinned). Fix: define δ_k unambiguously (tangent injection t_k vs retracted state difference x_{k+1} − x_k), state which quantity the §0(d) audit applies to, and bound the retraction shortfall explicitly (or set the tolerance to cover it). As written, the apparatus-void condition is live ammunition pointed at the pilot itself.

**F2 — Decision table (§2) is not exhaustive.** Two corners fire no branch: (a) ΔM_geo > 0 with McNemar n.s. and the random-null holding (e.g., a single flip the random paths don't match) — branch 1 needs ΔM_geo = 0, branch 2 needs p ≤ 0.05, branch 6 needs the flips to be a subset of random-path flips; (b) ΔM_geo > 0, p ≤ 0.05, random-null holding, but rank-trend flat/inverted — §3.7 says this → KILL ("the effect is not the amplifier's") but §2 has no such row. Fix: add both rows to the §2 table (suggested: (a) → a defined INCONCLUSIVE / hypothesis-UNTESTED insufficient-power verdict, never a silent pass; (b) → KILL per §3.7).

**F3 — ĉ-gate precedence contradicts the table (§0, §4 vs §2).** §0 and §4 state ĉ_geo < 0.1 → KILL unconditionally (before the McNemar bar); the §2 KILL row conjoins it with ΔM_geo = 0. In the (ΔM_geo > 0, ĉ_geo < 0.1) corner, §4 yields KILL while §2 yields CONTINUE (bars permitting). Fix: harmonize explicitly — either condition the gate on ΔM_geo = 0 (matching the table and the EXP131 precedent, where the corner never arose) or promote the unconditional gate into the table with its precedence stated.

**F4 — Rank-trend defined twice, differently (§2 vs §3.7).** §2: "v̂₂-geodesic effect ≤ v̂₁-geodesic effect"; §3.7: "margin-displacement(v̂₁) ≥ margin-displacement(v̂₂) on ≥ 8/10 prompts." Fix: use one quantified definition in both places.

**F5 — Arm count mismatch (gate Q3 vs pre-reg §3.5).** The worth-it gate costs "5 arms / 50 forwards"; the pre-reg specifies 7 arms (base, one-shot v̂₁, geodesic v̂₁, geodesic v̂₂, 2 random-paths, B_agg-path) = 70 forwards + VJPs. Fix: harmonize the gate's cost paragraph with the pre-reg's arm list (or vice versa).

---

## Advisory notes (not verdict-blocking)

- **N1 — PIVOT multiplicity.** The PIVOT trigger (≥1 of 20 midpoint ĉ values ≥ 0.1) has no multiplicity control. Stakes are low (it licenses only a draft), but consider ≥2 prompts or a mean-midpoint bar.
- **N2 — K = 5 unmotivated.** Acceptable as a pilot choice; the O(B²/K) mechanism argues larger K is better, cost argues smaller. Not a defect.
- **N3 — CPU baseline contingency.** The one-shot arm is re-measured on CPU (correct — no GPU import), but the pre-reg doesn't state the contingency if the CPU one-shot diverges from EXP131's GPU null. The within-run controls cover it; a one-line pre-registration of the contingency would close the loop.
- **N4 — "Great-circle" parenthetical (§3.4).** Loose relative to the stepwise retraction definition; the stepwise procedure governs and is deterministic. Ensure no executor substitutes the exact great circle for the specified retraction steps.

---

## Bottom line

SIGN-WITH-FIXES. Apply F1–F5; the draft then merits a signed pre-reg and CEO clearance consideration for the CPU pilot. The kill-first structure, the dose fence, the seventh-item constraints, and the bounded-claim discipline are all sound. F1 is the only defect that could kill a real run on its own — fix it first.
