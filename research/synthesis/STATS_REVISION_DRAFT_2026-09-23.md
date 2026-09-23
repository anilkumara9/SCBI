# Statistical Protocol Revision — Draft for the LOG-158 Revision (Lead-authored)

**Purpose:** binding replacement text for the revision drafter. Implements mentor
findings #2 (p≥0.05 inconsistency) and #3 (multiplicity). To be integrated into
the revised synthesis (new dated file); this draft is a working note, not a
signed artifact.

**Status:** draft for Law #14 review as part of the revision package.

---

## 1. Universal primary-comparison rule (replaces every "p≥0.05 ⇒ Not supported")

**Scope:** every primary comparison in §§E/F/G/H that licenses or kills a
mechanism claim. Endpoint is always the decision-change difference ΔM with the
exact McNemar paired test.

**Reporting requirement:** every primary comparison reports Δ̂M with an exact
two-sided 95% confidence interval [L, U] for the paired difference. A p-value
alone never licenses a verdict.

**Pre-registered practical margin:** δ_min = 0.05 (5pp).
*Rationale* [INFERENCE]: δ_min sits below the smallest bridge rescue ever
observed in the corpus (+10pp, EXP077 official) and above the noise floor;
with N=80 the one-sided exact McNemar MDE is ≈7.5pp at c=0, so δ_min lies just
below typical detectability — the Inconclusive cell (§1.1, case 4) honestly
absorbs that gap instead of converting underpower into a kill.

### 1.1 Verdict mapping (exhaustive)

For a superiority claim "X beats Y by a meaningful amount":

1. **L > δ_min → Supported.** Meaningful improvement established (significance
   is necessary but NOT sufficient — p<0.05 with L ≤ δ_min is not Supported).
2. **U < 0 → Not supported.** Genuinely negative effect with precision.
3. **U < δ_min (with U ≥ 0) → Not supported.** The CI rules out a meaningful
   improvement — equivalence-to-null at the practical margin (TOST logic).
   This is the only way a null result becomes "Not supported."
4. **Otherwise (CI overlaps δ_min, or covers 0 too widely to rule out δ_min)
   → Inconclusive.** The comparison is underpowered. The candidate is HELD
   for a powered re-test, never culled on this cell.

**Standing ban:** the string "p ≥ 0.05" never appears as evidence against a
candidate anywhere in the revised synthesis.

### 1.2 Negative-control rule

A negative control (B_perp, B_wrong, shuffled-label, random-perturbation) is
"null" iff its 95% CI rules out a meaningful rescue **in the rescue
direction** (U_ctrl < δ_min). If a control's CI cannot rule out δ_min, the
control is **uninformative** — any Branch-S licensing that depends on it is
BLOCKED (verdict Inconclusive), never licensed. An uninformative control is
a property of the experiment, not evidence for the candidate.

---

## 2. Hierarchical alpha-budget testing plan (new; implements finding #3)

Total program α = 0.05, partitioned across four levels. No level borrows from
another.

- **Level 1 — Program gate (H3 kill trigger / Survive).** α₁ = 0.05. A single
  family-level conjunction (kill requires ALL candidates to fail; Survive
  requires ≥1 Level-2-licensed Branch S). No multiplicity: it is one
  pre-registered conjunction.
- **Level 2 — Candidate gate (Branch-S licensing, per candidate).**
  α₂ = 0.05/8 = 0.00625 two-sided (Bonferroni over the 8 candidates), applied
  to the primary superiority gate (conditions i+ii jointly: vs M1 AND vs
  best of M2–M8 — the gate passes only if BOTH clear δ_min at α₂, using the
  CI rule of §1.1). Secondary Branch-S conditions (controls, fingerprint,
  harm) are reported at Level 3 and cannot license Branch S alone.
- **Level 3 — Mechanism fingerprint (Box-1 checks) and control validation.**
  α₃ = 0.05 per check, reported without cross-candidate adjustment. Gates
  *interpretation* of a Level-2 pass; cannot advance a candidate alone.
- **Level 4 — Secondary / exploratory.** Unadjusted p-values, labeled
  exploratory, cannot move any verdict.

**Anti-recycling rule (binding):** candidate selection cannot silently recycle
significance. A candidate failing Level 2 on NTDP data may not be re-tested
on the same data with a new analysis to manufacture a pass. Re-tests require
fresh task-family construction (track-9) and re-consume Level-2 budget.
"The winner" is selected only from Level-2-adjusted results.

**Power honesty (pre-registered):** Level-2 Bonferroni is conservative at
N=80. Before the NTDP, the protocol pre-registers N=80, δ_min=0.05,
α₂=0.00625 one-sided exact McNemar thinking (two-sided testing), the MDE
computed under the pilot-estimated discordant-pair count (N=20 pilot), and
the adaptation rule: if estimated MDE > 2·δ_min, N is increased per the
stated rule or the candidate is held — the Inconclusive cell is the honest
container for underpowered comparisons, never converted to Not supported.
McNemar exact is discrete at N=80: modest decision deltas may be
indistinguishable from zero, which §1.1 case 4 already handles.

---

## 3. Per-site replacements (exact)

**G4 Branch S (i),(ii):** append "with lower 95% CI > δ_min = 0.05" to both
superiority conditions. Significance alone does not license Supported.

**G4 Branch S (iv):** replace "(M12–M14 ΔM=0, p≥0.05; shuffled-label shows no
rescue)" with "each negative control's 95% CI rules out a δ_min rescue in
the rescue direction (U_ctrl < 0.05) — §1.2. A control that cannot rule out
δ_min blocks Branch S (Inconclusive)."

**G4 Branch F1:** replace "C\* ≤ best of M2–M8 at matched FLOPs (all p≥0.05
for the difference). → Not supported." with: "For the best forced baseline,
the 95% CI for (ΔM_C\* − ΔM_baseline) at matched FLOPs rules out a δ_min
advantage (U < 0.05) → **Not supported** (beaten-or-equivalent demonstrated).
If the CI overlaps δ_min → **Inconclusive** (underpowered comparison) — the
candidate is held for a powered re-test, never culled on this cell."

**F1 cull rule:** replace "any candidate with Δ ≤ 0 is demoted out of the
'new mechanism' race" with: "demote (Not supported for L2; may survive as L1
engineering) iff the adaptive-ablation difference CI rules out a δ_min
strategy contribution (U_abl < 0.05). CI overlapping δ_min → Inconclusive
(the ablation is underpowered) — candidate held, not demoted."

**DPRS Box 2 (line 594):** replace "DPRS ΔM ≤ 0 (p ≥ 0.05)" with "the 95% CI
for DPRS ΔM rules out δ_min (U < 0.05)".

**C4/ASR Box 2 (line 731):** replace "uniform-heavy at matched total FLOPs ≥
routed (p≥0.05 for the difference)" with "the CI for (ΔM_routed −
ΔM_uniform-heavy) rules out δ_min (U < 0.05) → allocation buys nothing,
withdrawn; CI overlapping δ_min → Inconclusive (underpowered), held."

**C5/LCMIC Box 2 (line 771):** replace "latent ≈ text at matched budget
(p≥0.05)" with "the CI for (ΔM_latent − ΔM_text) rules out δ_min (U < 0.05)
→ channel decorative, culled; overlaps → Inconclusive, held."

**F3 predictions (lines 933–934):** replace "(a)>(b) p<0.05 AND (b)≈(c)
p≥0.05" with "(a)>(b) with lower CI > δ_min, AND (b)≈(c) demonstrated by
equivalence (95% CI for (b−c) within ±δ_min) ⇒ the latent channel is the
mechanism; (a)≈(b) with CI ruling out δ_min ⇒ C5 reduces to debate (culled,
N1); equivalence not demonstrable (CI too wide) ⇒ Inconclusive."

**A10/EXP023 (lines 178–181, 1431):** replaced wholesale by the LOG-186
lineage ruling — no Bonferroni precommit; "Supported (L1,
selection-optimism caveat)" with the caveat precisely stated; pooled
p=0.000488 reported with the pre-specification caveat.

**Global:** no Supported verdict for any L2+ claim on significance alone —
Box-1 "p<0.05" gates (C1 line 553, DPRS line 589, C2 line 641, C4 line 724,
C5 line 765, C6 line 806, F1 line 888, K1 line 1145, K2 line 1176) are read
as "p<0.05 AND lower CI > δ_min"; where the original text asserts Supported
on p<0.05 alone, the revision adds the CI condition.

---

## 4. What is preserved

The falsification architecture is untouched: A4, A5, A6, A9, D2 (all five
boundary conditions), F1's structure, H3's license, §I's definition and
grades. This revision changes only the *decision rules* that map statistics
to verdicts — it makes kills harder to earn by accident (good: kills must be
demonstrated, not defaulted) and impossible to evade by underpower (the
Inconclusive cell forces powered re-tests).
