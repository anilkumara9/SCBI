# Independent Law #14 Review: DGF (Directional-Gain Field) Pre-registration

**Lane:** LOG-4739 (pre-assigned). **Review standard:** binding — SIGN / SIGN-WITH-FIXES / REJECT.
**Protocol under review:** `research/prereg/EXP_PREREG_DGF_GAINFIELD_2026-09-29.md`
**Protocol SHA-256 (verified before reading):** `370185a94619dfcd09773da0487b178c3ded54cde539dfcde19ddc93f1890dfe` — MATCH.
**Gate:** LOG-4737 (PASS-conditional; `research/strategy/DGF_GATE_2026-09-29.md`).
**Design-study basis:** LOG-4736 (`research/analysis_plans/DSF_APPARATUS_REDESIGN_STUDY_2026-09-29.md`).

**$0 CPU. No model contact. Read-only review.**

---

## Verdict

**SIGN-WITH-FIXES.** The protocol is launchable after the numbered fixes below.
No REJECT-level defect. The design is sound: the apparatus is genuinely disjoint
from EXP128's killed finite-difference primitive, the characterization-only
framing is load-bearing and enforced in the text, the bars are quantitative and
executable, and the seventh item proves non-resurrection. Four fixes are
launch-gating; five are verdict-immaterial.

---

## What was verified (fresh read of the full protocol)

1. **Protocol hash confirmed** `370185a9…1890dfe` before reading; the reviewed
   bytes are the drafted bytes.
2. **Five gate conditions carried** (header list + §1.2/§4/§0(b)/§3.3/§3.1/§7):
   characterization-only framing; null-contrast ΔGini with margin 0.2 and no
   raw-Gini bar; multi-ε float64 convergence diagnostic as the breaking point;
   probe provenance pinned pre-JVP; novelty N1. All present.
3. **Diagnostic/sensing separation is structural, not cosmetic.** The sensing
   primitive is forward-mode AD exclusively; the diagnostic's F(ε) values never
   enter ΔGini, the tree, or any bar — they gate the decision set only
   (pass/fail per prompt, ≥8/10 required, else apparatus-void). The distinction
   is airtight at the protocol level. (One honesty correction required — FIX-2.)
4. **Decision bars are quantitative and executable:** median ΔGini ≥ 0.2 (with
   median Gini_iso < 0.4) → CONTINUE; ≤ 0 → KILL; median Gini_iso ≥ 0.4 →
   KILL-as-premise; margin zone → HELD with "no re-run without a new gate"
   (no "more layers needed" escape); convergence failure → apparatus-void.
   A flat field genuinely kills.
5. **Non-resurrection proven** (§8): EXP128's RUN-INVALID named; zero finite
   differences in any sensing/verdict-bearing quantity; different bars
   (null-contrasted ΔGini vs raw Gini ≥ 0.4); different license
   (characterization vs targeting map). EXP129 (no loop), static-family kills
   (no decision read — probes are diagnostic in a gain measurement), EXP130
   (no generation channel), EXP131 (complementary, not re-asked) all addressed.
   No ε retuning anywhere: ε exists only in the verdict-immaterial diagnostic.
6. **Law #9 ordering executable** (§0, §3.6, §5 tree): guards → backbone pin →
   probe/hash pins → convergence diagnostic → JVP batches → validity checks →
   raw-record hash-pin → metric → decision. (Validity checks need registration —
   FIX-3.) Δθ=0 pinned pre/post; no labels (Law #7 clean); honest frame held
   throughout (§1.2, §7: infinitesimal regime 3+ orders below injection budgets;
   capability scoreboard untouched).
7. **No targeting claim anywhere.** The protocol affirmatively disclaims
   targeting in §0, §1.2, §6(1), and §7. The §6(1) enforcement hook (targeting
   claim in a downstream report → pre-reg REJECT at that review) is correctly
   scoped.
8. **Convergence-diagnostic tolerance ruling (drafter-flagged):** the 0.25
   tolerance is ACCEPTED as-proposed. Rationale: the diagnostic's job is
   instrument-health (detect a wrong AD graph or catastrophic numerical
   pathology), not certification of perfect linearity. In float64 at
   ε ∈ {1e-6, 1e-7, 1e-8}, subtractive-cancellation error is ~1e-5 relative —
   far inside 0.25 when healthy; a knee between ε values produces factor-level
   disagreement — far outside 0.25 when pathological. The F(ε) traces are
   hash-pinned as instrument-health records (§3.6) and per-prompt exclusions
   require disclosure (§0(b)), so the tolerance is auditable, not a rubber
   stamp. Tightening would risk false exclusions in the safe (void) direction
   with no validity gain. **No change required.**
9. **Diagnostic strictness compounding noted:** "any failing diagnostic point
   excludes the prompt" over 27 points/prompt is strict, but it errs toward
   apparatus-void (the safe direction), is disclosed, and is the drafter's
   registered choice. No change required.

---

## Launch-gating fixes (verdict-material — protocol not launchable without these)

**FIX-1 (LAUNCH-GATING) — Make the isotropic null probe-symmetric.**
§3.4 defines Gini_iso over the per-layer *median-of-8* field while Gini_sem is
over a *single* probe's field. Under H0 the semantic probe is a generic
direction, but the median-of-8 field has probe noise suppressed, so
E[ΔGini | H0] > 0 — the test is biased toward CONTINUE by an unquantified
amount, and the 0.2 margin ("half EXP128's bar") was not calibrated to this
noise. Same JVPs, zero extra compute, strictly better test:
- §3.4: define Gini_iso_ij = Gini over the 24 values {S_l^*(u_j)}_l for each
  random probe j; per prompt Ḡini_iso_i = median_j(Gini_iso_ij);
  ΔGini_i = Gini_sem_i − Ḡini_iso_i. Under H0, E[ΔGini] = 0 by symmetry.
- Carry through §0 [DEFINITION], §2 table, §4 bars, §5 tree
  (KILL-as-premise bar reads "median Ḡini_iso (median over probes, then over
  prompts) ≥ 0.4").
- This preserves gate Condition 2 (null-contrast design, ΔGini = Gini_sem −
  Gini_iso, margin 0.2, no raw-Gini bar) — the *design* is verbatim; only the
  null's aggregation is refined to exact H0-symmetry. Record this rationale
  in §3.4 so the fix-verification lane does not flag a gate-condition drift.

**FIX-2 (LAUNCH-GATING) — Correct the §6(2) overclaim.**
"No finite differences anywhere in the executor (grep-verifiable)" is FALSE
as written: §3.3's convergence diagnostic computes F(ε) = ‖g_l(y_l+εu) −
g_l(y_l)‖/ε, which *is* a finite difference. Replace §6(2) with: "No finite
difference is used as a sensing primitive or enters any verdict-bearing
quantity. The sole ε-bearing computation is the verdict-immaterial convergence
diagnostic (§3.3); it is grep-auditable as diagnostic-only (its outputs gate
the decision set; they never enter ΔGini, the bars, or the tree)." Honesty of
the protocol's own claims is launch-gating (Law #2-adjacent).

**FIX-3 (LAUNCH-GATING) — Register the validity-check set.**
The Law #9 ordering (§0, §3.6) lists a "validity checks" step with no
definition — the executor would have to invent it, which breaks executability.
Register the set explicitly in §3.6 (all apparatus-void on failure, disclosed):
(a) probe unit-norm audit (|‖u‖ − 1| ≤ 1e-6 for the semantic probe and all 8
isotropic probes, pre-JVP); (b) JVP-output finiteness (no NaN/Inf in any
S_l^*(u); any occurrence → apparatus-void for that prompt, disclosed);
(c) seed/pin audit (isotropic seeds = 20260929 + prompt index; probe SHA-256
matches the manifest). No new quantities — these are checks on already-
registered objects.

**FIX-4 (LAUNCH-GATING) — Pin the exact 10 prompt ids.**
§3.1's `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}` brace-expands to 20
strings, but the decision set is 10 prompts ("canonical-order first 10").
Replace the pattern with the explicit 10-id list, sourced from EXP127's pinned
decision set (cited "for comparability" — the citation must resolve to bytes).
The fix-verification lane must confirm the 10 ids against EXP127's report /
environment manifest. An ambiguous decision set is not launchable.

---

## Verdict-immaterial fixes

**FIX-5** — Qualify the KILL license scope (§4 table, §7, §8): the protocol
tests ONE registered semantic probe direction per prompt. "The soft-spot
premise dies" overclaims — a KILL kills the premise *for the registered probe
direction*, not for all semantic directions. Restate as: "the soft-spot
premise dies for the registered probe class; fields identical up to the null."
(Pilot scope; the honest frame in §7 already limits generality — make the bar
licenses match it.)

**FIX-6** — Define g_l's codomain (§3.3): "the readout tensor" is never
defined. State explicitly which tensor the map targets (whichever EXP128 used —
final-layer last-token residual or logit vector), so the executor and any
future reviewer can reproduce the map exactly.

**FIX-7** — Relabel [THEOREM] (EXP127-class precedent) in §2: it is a
program-license rule ("a CONTINUE licenses further characterization only"),
not a mathematical theorem. Relabel [DEFINITION] (license scope) or drop the
label. Epistemological-label hygiene per AGENTS.md §5.

**FIX-8** — Budget arithmetic (§3.5): the parenthetical mixes per-prompt and
total counts ("diagnostic 10 prompts × 9 probes × 3 layers × 3 ε = 810
forward-sets" is a *total*, not per-prompt), and the 4000/prompt hard cap is
~9× the expected ~460 products/prompt. Restate cleanly (per-prompt expected
≈ 216 JVPs + 81 diagnostic forward-sets ≈ 460 product-equivalents; total ≤
40000), and tighten the per-prompt cap to 1000 (still >2× headroom; the exact
counts are deterministic, so the cap is a bug-catcher, not a target).

**FIX-9** — Degenerate-Gini branch (§3.4): register that an all-zero field
(Gini 0/0) → apparatus-void for that prompt, disclosed. Measure-zero in
practice (gains are O(1)), but a NaN must never reach the median.

---

## Interpretation note (for the execution report, not a finding)

The diagnostic's strictness (FIX-4's sibling concern in §0(b)) means a healthy
run may exclude 1–3 prompts; the report should show the exclusion pattern
(which prompts, which diagnostic points failed) so a systematic exclusion
(e.g., all deep-layer probes on all prompts) is visible as instrument signal
rather than silent attrition. The protocol already requires disclosure; the
report should make it prominent.

---

## Deliverable record

- Protocol SHA-256 verified pre-read: `370185a94619dfcd09773da0487b178c3ded54cde539dfcde19ddc93f1890dfe` — match.
- No model contact, no push, no spend, no credential touch. Read-only except
  this review file and the research-log append.
- Next in the launch chain: fix-verification (all nine fixes byte-verified) →
  CEO launch decision → execution under a minted number (EXP132-class).

*Independent Law #14 review — binding. LOG-4739.*
