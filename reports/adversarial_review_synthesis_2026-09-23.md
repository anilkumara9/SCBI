# Law #14 Adversarial Review — A–J Synthesis (LOG-158)

**Reviewer:** Law #14 adversarial reviewer (LOG-164 dispatch) · **Date:** 2026-09-23
**Reviewed:** `research/synthesis/SYNTHESIS_A_J_2026-09-23.md` (1486 lines)
**Spec:** `research/synthesis/SYNTHESIS_SPEC.md` · **Audit:** `CLUSTER_B_2026-09-23.md`
**Cluster reports:** `CLUSTER_A/B/C_2026-09-23.md`
**Authority:** the reviewer answers to the CEO; no one may instruct a finding to be
softened. **Analysis only.** No GPU used; no experiments run; no signed protocol or
primary artifact modified. No research-log entry written (LOG-164 covers this dispatch).

## VERDICT: SIGN-WITH-FIXES

The synthesis clears for the mentor's adversarial review and program adoption once
the six enumerated fixes below are applied. Nothing found is blocking (no verdict
needs revision, no candidate fails the boxed standard, no reconciliation item was
silently dropped). **G/H pre-registration is authorized only AFTER the mentor's
review**, per the dispatch terms.

---

## 1. Verdict integrity (§A) — HELD

- **A1 (I1):** Supported, explicitly below L1 (a boundary constraint, not a capability).
  No creep.
- **A2 (dynamic alignment):** the two-way Inconclusive split is preserved exactly as
  Cluster A demanded — "aligned-basis injection fails to rescue": Inconclusive (never
  tested); "sound dynamic alignment rescues": Inconclusive. Not collapsed into
  Not supported; EXP067's scope is correctly protected.
- **A3 (bridge rescues):** Supported-at-L1, with the full validity carry: Bonferroni
  fragility of EXP077's +10pp stated, borderline EXP066 p=0.0078 vs 0.0083 stated,
  smoke-vs-official magnitude gap flagged as a reproducibility red flag on magnitude,
  "no pp number is cited as a stable quantity." The Law #7 caveat is binding and
  unsoftened: "the readout is causally accessible to an option-informed direction."
  This is the honest L1 picture; no level-crossing detected.
- **A4 (handover §3.3):** Refuted (the specific QK-subspace sentence), scoped to the
  claim — Cluster B's constraint (5) honored: the kill does not touch the bridges or I1.
- **A5 (EXP077):** Not supported, explicitly inside the licensed bounds; gated and
  conditional variants survive. Kill is narrow by design.
- **A6 (loop ceiling):** Inconclusive — EXP070 UNINFORMATIVE_PROBE + EXP079 infeasible
  probe rule both recorded as process failures, not loop failures. No ceiling measured;
  nothing in the corpus licenses L2.
- **A7 (EXP078 localization):** Underdetermined — correctly, since "the
  subspace/projection metric is wrong" remains compatible with the observation.
- **A10 (EXP023/024 selection-bias):** recorded as **Supported (L1, selection-bias
  audit pending)** — never as confirmed; "The outcome is NOT asserted here." This
  matches Cluster B's instruction verbatim ("cite R1 as Supported (L1, challenge
  pending)"). **Numerical cross-check against the primary artifact:**
  `reports/experiment_report.md` shows Seed-84 CI [+0.0300,+0.1200] and pooled CI
  [+0.0400,+0.0950]; the synthesis quotes the seed-84 CI next to Seed 84 and Cluster B
  quotes the pooled CI next to the pooled result — consistent attribution, no
  inconsistency. (My initial alarm on a CI mismatch was wrong; the primary source
  resolves it.)

## 2. Prior-art honesty (§B/§D) — HELD, with one fix (Fix 1)

- **"Adjacent possible already shipped":** present and unsoftened. §B5 states at full
  strength that ∇-Reasoner occupies the output-side dynamic room (with the burden
  placed on SCBI: "why gradient-free self-consistency would beat gradient-based
  optimization with a reward model at matched compute") and that Activation-LQR
  occupies H1's slot "with stronger validation than anything in SCBI" — SCBI's H1
  candidacy named as "strictly weaker than the art until proven otherwise." DEER is
  stated as demonstrated L2 evidence from the field. R(f) correctly refuses to soften
  this into "SCBI was early."
- **N1/N0 lines held:** §B1 — N1 overall, **N0 for the tested mechanism**. The exact
  operator-equivalence claim (v = h̄₊ − h̄₋, h ← h + c·v) is carried, with break-points
  marked where equivalence fails. The anisotropy-correction deficit (Jorgensen/
  Ethayarajh) is admitted as a methodological *deficit* vs prior art — admirably hostile.
- **Cluster B's seven non-softenable constraints:** all seven enforced and traceable
  (R(g) maps each to a section). Verified each in text.
- **FIX 1 — SVF content cited despite Cluster B's explicit do-not-cite instruction.**
  Cluster B §2.2: "cluster C / the literature program must verify and place it
  before the synthesis finalizes; **do not cite its content**." Synthesis §B6 says:
  "*Steering Vector Fields (Feb 2026) and Activation-LQR (Apr 2026) move steering to
  vector fields and closed-loop feedback control with tracking-error bounds*" — the
  sentence then carries the UNVERIFIED tag, but the tag does not cure the violation:
  it cites SVF's *content* (vector-fields steering) as a load-bearing premise of "the
  field has moved past open-loop additive steering." Worse, the parenthetical says
  "the literature program must verify **before the synthesis is cited on it**" —
  while the sentence it sits in cites it. This also misattributes jointly: the
  tracking-error bounds belong to A-LQR alone. Fix: strip SVF's content claim from
  §B6; keep SVF *named* as reported by the internal Sept-2026 sweep, UNVERIFIED, with
  no content claim; let Activation-LQR alone carry the closed-loop/bounds clause
  (which it fully supports). The argument loses nothing — A-LQR is sufficient.

## 3. The boxed standard (§E) — HELD for all 8; C5/C6 rationale verified

- All eight candidates (C1, E7/DPRS, C2, C3, C4, C5, C6, E8) carry **both** Box 1
  (unique-support observation) and Box 2 (kill observation), each pre-registrable as
  written. None is marked [Supported]; the §E preamble states "none is assumed
  correct — all await falsification attempts." No candidate is kept on elegance.
- **C5/C6 double-H5 (R(b)):** the non-overlap rationale holds on inspection. C5's
  Box 1 (latent-channel > text at matched budget, text-only ≈ debate/MoA, critic
  doubt AUC>0.55) concerns *inter-instance* communication; nothing in C6's
  intra-pass branching mechanism predicts it. C6's Box 1 (branch diversity,
  merge-vs-select, ~2F beating Best-of-4 at 4F) concerns *intra-pass* arbitration;
  nothing in C5's multi-instance mechanism predicts it. Mechanism-distinct, no shared
  Box-1 observation — the merge/cut ledger (E2→H5c conditional, E3 folded as
  pruning operator, E4 absorbed, E1/E5/E6 superseded) is consistent with Cluster A's
  "E-input is scaffolding" instruction.
- **E8 conditional gating:** explicit — "This candidate is gated: it becomes a live
  mechanism program only if the §H bridge battery leaves an output-side room… a
  pre-registered conditional design, not an active bet." Fix 6 (minor citation hygiene):
  E8's Box 1 cites "(pre-registered; LOG-144 review scope)" — LOG-144 is defined only
  in Cluster A's report, not in this document. Add a parenthetical naming it (the
  entity-similarity-leak adversarial review per Cluster A).

## 4. Theory preservation — NO FINDING, with one phrasing fix (Fix 5)

Hunted the full text for keep-alive-by-ambition/elegance/sunk-cost. The discipline is
real: §H3's license "executes without re-approval," F2 demotes to L1 engineering with
the L2/L3 claim withdrawn, E8 is conditional rather than protected, and §B's
track-7 verdict licenses the conclusion that "SCPM is a dead end as a mechanism
program." **One sentence needs repair:** §C6 — "a successor that avoids all five
rooms… starts from a constrained design space — which is what makes C1, C4, C5
**worth pursuing rather than random**." The underlying reasoning (negative map ⇒
constrained design space) is legitimate labeled [INFERENCE], but "worth pursuing
rather than random" is a paraphrase of the banned verdict "worth another experiment"
used as a verdict on three candidates' candidacy. Fix 5: rephrase as the
interpretation it is (e.g., "which is the evidentiary basis for keeping them in the
falsification funnel"), not a worthiness verdict.

## 5. G and H — discriminating, with two decision-tree gaps (Fixes 2, 3)

- **§G (NTDP) discriminates:** per-candidate M1–M14 battery, matched-FLOPs accounting,
  negative controls including a shuffled-label control, harm ledger, per-candidate
  Box-1 fingerprint, the §F1 adaptive-ablation arm (M11) as the P1-conditionality
  operationalization. Branch S / F1 / F2 / F3 / F4 + degenerate cells are individually
  well-reasoned.
- **§H license to kill:** explicit and pre-registered — "This license is pre-registered
  and executes without re-approval," with the forbidden move named ("Theory
  preservation… is the named forbidden move, and this paragraph is its antidote").
  Survive / Demote / Degenerate branches are real branches, not summaries.
- **FIX 2 — G4 has no branch for negative-control failure.** Branch S requires (iv)
  all negative controls null (M12–M14 ΔM=0; shuffled-label shows no rescue). But
  F1–F4 and the degenerate cells do not cover the cell where (i)–(iii), (v), (vi)
  hold and (iv) **fails** — i.e., the rescue is real but a negative control also
  fires (readout-bias artifact signature). Fix: add Branch F5 — *Contaminated*
  (Not supported as a mechanism; the artifact routes to the §H6 battery for
  adjudication rather than being scored as a mechanism failure).
- **FIX 3 — F3 (parameter substitution) leaves the family in limbo.** H3's kill
  trigger condition 1 lists only F1/F2/F4, so an all-F3 outcome fires neither the
  kill trigger nor H4's Survive (needs Branch S) nor H4's Demote (needs ≥1 F2).
  Track-11 says F3 "is not a failure of C* as engineering — a failure of the novelty
  claim," so the honest family-level reading of all-F3 is: the novelty claim failed
  everywhere. Fix: add F3 to H3 condition 1's branch list (with no Branch S), and add
  an H4 *Substitution branch* — novelty claim failed family-wide; surviving L1 value
  handled under the demote-to-engineering logic (track-11), no Stage 2/3.

## 6. The H7 CEO decision — UNRESOLVED, explicitly; no silent assumption

§H7 is marked **[OPEN]/[OPEN], UNRESOLVED — CEO decision required (not decided
here)**. I hunted for silent assumptions of the answer: §A3 cites the bridge as
"Supported (L1, mechanism [CONJECTURE], readout-bias audit pending)" — consistent
with awaiting the verdict, not assuming it. §H6's note that a K1 tilt-verdict
"removes the premise of the conditional E8 candidate" is a correct reading of E8's
explicit conditionality, not an assumption about H7's *protocol-status* question
(revoke vs retain-with-relabeling of positive-control status across EXP065/066/070/077).
C1's setpoint re-specification is phrased as a forward-looking conditional ("the
second option must be used if the §H battery confirms readout bias"), independent
of H7's retroactive decision. No silent position taken. **Held.**

## 7. §I/§J — one definition, gates are genuinely pre-registered — HELD

R(a) reconciles to one authoritative definition (track-5 five conditions + kill
criterion + L1/L2/L3 grades), with Cluster C's provisional elements folded in as
*measurement procedures* (F2, G-Branch S, D1–D4) — not as replacements — and the
differences flagged rather than smoothed. The §J gates name exact falsifiers:
Stage 1 — advance iff ≥1 G-Branch S (L2+); close iff H3 kill trigger fires; demote
iff H-Demote. Stage 2 — ≥2/3 families + Box-1 fingerprint on each winning family +
harm < 15%. Stage 3 — chance-bar + D1–D4 + scaling bar, all pre-registered, or "the
L3 claim is not made." Stage 3 is honestly labeled "ungated aspiration until an L2
mechanism exists." No decorative gates; no hype terms in any criterion.

## 8. K-ordering (K1 → K2 → K3) — RULING: sequence interpretation, parallelize preparation

R(c)'s logical-priority argument holds: K1 is $0 re-analysis of archived artifacts
(cheapest to a verdict); a confirmed tilt verdict *dissolves* the Law #7 question
(no autonomous mechanism left to audit), so only a survival verdict licenses K3 to
bite; K1 is "designed to lose cleanly" — a negative result strengthens the output-
side program. That is sound sequencing of *conclusions*.
The K1 ambiguity middle (cos < 1 but label-shuffle only partially diagnostic)
does not strand the program: K2 is informative under *either* K1 outcome (survival
→ does the surviving mechanism route through attention? tilt → is the tilt
bypass?; R(c) notes the joint tilt+bypass verdict closes the output-side room),
while only K3's *evaluation* is gated on K1 survival — "auditing the label
compliance of a confirmed readout tilt is wasted motion."
**Ruling:** keep the binding order for interpretation (no K3 conclusions before the
K1 verdict); but *preparation* is not gated — K2's ~180-pass pilot protocol and
K3's Law-#7-compliant constructions may be built in parallel while K1 runs. The
"Order is binding" sentence in §H6 should be scoped to interpretation, not
benchwork, so K1's timeline ($0 re-analysis, days-level) does not idle the program.
**Additionally (Fix 4):** K1 test (b), correct-item flip analysis, is listed as a
test but the kill criterion references only (a) and (c). Attach a pre-registered
decision rule to (b) or relabel it as a diagnostic readout — an unruled test in a
falsification battery is dead weight under Law #9.

## 9. Appendix R — reconciliation ledger verified

- **R(a):** one definition; Cluster C's provisional definition cut as standalone,
  its operational elements folded. Differences (1)–(5) flagged explicitly. Executed.
- **R(b):** C5/C6 both pass the boxed standard independently — kept as H5a/H5b with
  the non-overlap rationale (verified above in §3); E2→H5c conditional; E3 merged as
  pruning operator (restated around readout-coupled heads per G1's honest caveat);
  E4 absorbed into C1/DPRS; DPRS added from Cluster B's IDEA. Executed.
- **R(c):** twin bridge challenges ordered K1→K2→K3 with the rationale recorded;
  H7 explicitly reserved. Executed.
- **R(d):** conditionality probe merged as the named EXP068 instantiation of §F1's
  adaptive-ablation, with attribution to Cluster B §3.3 and track-3 §4.4, and the
  verbatim decision rule preserved. One assay, three uses — genuinely one
  experiment set, not three. Executed.
- **R(e):** EXP023 challenge recorded with its falsifier; outcome not asserted.
  Executed.
- **R(f):** "adjacent possible already shipped" at full strength — subject to Fix 1
  (SVF). The line itself is honest; only the SVF content-citation oversteps.
- **R(g):** all seven of Cluster B's non-softenable constraints traceable to text;
  Cluster A's "E-input is scaffolding" instruction honored (E1/E5/E6 superseded).
  Nothing with a live falsifier was dropped.

## 10. Standards — HELD

- **Epistemic double-labeling:** present on every load-bearing claim sampled across
  §§A–J, R (canonical pair + 10-label, e.g. [FACT]/[OBSERVATION],
  [INFERENCE]/[INTERPRETATION]).
- **Evidentiary levels:** L1/L2/L3 tagged per claim; the §F1 conditionality criterion
  and §D2 condition 4 operationalize the mechanism-level bar; Branch F2 exists
  precisely to prevent silent L1→L2 crossing.
- **Verdict categories:** only Supported / Not supported / Inconclusive /
  Underdetermined / Refuted used as verdicts. Banned phrases
  ("interesting," "promising," "elegant," "worth another experiment") appear nowhere
  as verdicts — the single occurrence is the meta-sentence asserting exactly that
  (subject to Fix 5's "worth pursuing rather than random" adjacency).
- **The F1 culls' "demoted" wording** is a consequence description, not a verdict;
  the binding verdict for the L2 claim is stated ("Not supported for L2") in the
  conditionality-probe paragraph. No fix required beyond Fix 5.

---

## Fixes required before mentor review (all minor, sentence-to-paragraph level)

1. **§B6 / R(f):** remove SVF's content claim ("move steering to vector fields");
   keep SVF named as sweep-reported, UNVERIFIED, no content claim; attribute
   tracking-error bounds to Activation-LQR alone. (Cluster B's "do not cite its
   content" constraint.)
2. **§G4:** add Branch F5 — *Contaminated* — for (i)–(iii),(v),(vi) holding while
   (iv) negative controls fail: verdict Not supported as a mechanism; artifact
   routed to the §H6 battery.
3. **§H3/H4:** add F3 to H3 condition 1's branch list and add an H4 Substitution
   branch (all-F3 ⇒ novelty claim failed family-wide; surviving L1 value demoted to
   engineering per track-11, no Stage 2/3).
4. **§H6 K1:** give test (b) (correct-item flip analysis) a pre-registered decision
   rule or relabel it as diagnostic readout; scope "Order is binding" to
   interpretation, explicitly permitting parallel preparation of K2/K3.
5. **§C6:** rephrase "worth pursuing rather than random" into a labeled
   interpretation of the negative-map constraint (banned-verdict adjacency).
6. **§E8 Box 1:** gloss "(LOG-144 review scope)" — name it as the
   entity-similarity-leak adversarial review per Cluster A.

**Non-blocking note for the mentor:** Fix 2 and Fix 3 close the only exhaustiveness
gaps in the NTDP/family decision trees; everything else reviewed is the synthesis
working as designed. The standing-law compliance checklist at the document's end is
left unchecked for the mentor — correct; I do not pre-tick it.

---

*End of LOG-164 review. Awaits the six fixes, then the mentor's adversarial review;
G/H pre-registration triggers only after the mentor's review, not before.*
