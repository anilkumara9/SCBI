# Mentor's Final Adoption Gate on REV2 (LOG-195) — Independent Scientific Mentor & Adversarial Reviewer, 2026-09-23

**Reviewer:** In-house Independent Scientific Mentor & Adversarial Reviewer
(Muse Spark subagent, standing appointment by the user 2026-09-23), succeeding
ChatGPT. First assignment. This gate is mine — I re-derived the verdict; nothing
is inherited from ChatGPT's notes or from LOG-192's SIGN (treated as a claim to
verify, not a result).

**Target:** `research/synthesis/SYNTHESIS_A_J_REV2_2026-09-23.md` (LOG-191 patch,
2,459 lines), judged as a fresh adversarial object.

**Structure of this gate:** (A) the five LOG-193 defects, each CLOSED only if
eliminated from the protocol's logic; (B) the 9 re-review acceptance criteria
from the directive; (C) a fresh-object regression sweep over every previously
cleared section; (D) my own Law #3 spot-checks (own fetches, not inherited).

**Verdict: ADOPT.**

---

## A. The five LOG-193 defects

### 1. M15 genuinely load-bearing: CLOSED

- §G4 Branch S condition (vii): the candidate-specific pinned M15 must be
  cleared at the Level-2 standard (lower 99.286% CI > δ_min=0.05), "or the
  pre-registered structural-comparison path below is licensed. M15 is not
  optional: a Branch-S license that skips the newer-prior-art comparator is
  invalid." The D2/G3/G4 contradiction is closed by conjunction.
- [INCOMPLETE] M15 blocks Branch S (Inconclusive) and is never read as
  clearance. The structural path requires M15 to be run as a control arm
  (trigger condition (c)), so it cannot evade an [INCOMPLETE] M15 either.
- The structural-comparison rule has three trigger conditions precise enough
  to bite: (a) pre-registered observable mechanism property independent of the
  measured gain, with a pre-registered operational check — "'different
  architecture' as a redescription of the mechanism, without an independent
  operational check, never qualifies"; (b) the distinction is experimentally
  established on the NTDP; (c) M15 is still run as a Level-3 control with a
  pre-registered failure-mode prediction. And crucially: if M15 beats C* at
  the Level-2 standard, the structural claim is **Not supported** — the
  structural difference must do work the prior method cannot do.
- §G3 pins four executable protocols (M15-LTPO T=8/η=0.1; M15-MetaReasoner
  with frozen bandit scope; M15-LatentMAS R=3/D=2; M15-NoisyCoconut K=5/σ=0.1)
  with frozen model, exact configuration, task construction, and two-number
  FLOP accounting, all fixed before NTDP data contact; paper-free choices
  marked [PINNED-CHOICE].
- Program-level Branch HOLD exists (neither kill nor license): explicit entry
  conditions, release only via fresh pre-registration (fresh task family,
  re-consumed Level-2 budget, blocking defect repaired), a held candidate
  never re-enters on the same data or by re-analysis, exhaustion goes to the
  F-branch — never to Branch S by attrition.

### 2. ASR internally consistent: CLOSED

- Zero occurrences of "8/8" (grep-verified). Five "7 complete" sites,
  including the §E summary table and the standing-law checklist (line ~2250).
- Every counting site reads "7 complete candidates + 1 pending candidate
  (C4/ASR), not eligible for experimental triage until policy scope is frozen":
  §E table/paragraph, §F1, §G1b (Level-2 budget re-divided over 7:
  α₂=0.05/7=0.00714, 99.286% CIs), §§H1/H3/H4, §J, checklist.
- §C4's policy-scope declaration is explicitly [INCOMPLETE]: "C4/ASR may not
  enter §F culling or §G NTDP runs — and no Box-1/Box-2 verdict for ASR is
  licensable — until the policy-scope declaration is pre-registered."

### 3. LCMIC bandwidth isolation: CLOSED

- §F3 is a five-arm design; arm (e) is the bandwidth control — the exchanged
  latent tensor is projected/quantized so its total payload in bits ≤ the
  text channel's token budget in arm (b) (pre-registered top-k PC compression,
  k fixed on the pilot, frozen before data contact). A real arm, not an
  appendix note.
- The bandwidth-isolation rule is a binding licensing condition: L_(a−e) >
  δ_min → the channel-representation claim is **Not supported** and C5's
  Branch S is **BLOCKED** (§G4 condition (v)); U_(a−e) < δ_min → the
  raw-capacity account is ruled out; CI overlap → Inconclusive, C5 held.
- C5's Box 1 carries the (e) condition as a conjunct of unique support. The
  protocol forbids attributing raw channel capacity to the mechanism.

### 4. Fresh-object audit complete with current publication status: CLOSED

- Appendix V (17 records, V1–V17): each with source URL, fetch date
  (2026-09-23), verdict, exact supported claim, and textual consequence.
  Covers B1 (CAA, Activation Addition), B4 (PPLM, Self-Refine), B5 (DEER,
  STARS, ∇-Reasoner, Activation-LQR), D1/M15 (Meta-Reasoner, LTPO, LatentMAS,
  NoisyCoconut), A8 (EXP048/049/056/057/058 primary JSONs).
- Self-Refine's unverified "2–3 iteration plateau / blind spots" claims are
  honestly withdrawn as factual and restated as [HYPOTHESIS].
- Non-load-bearing inherited references (RISER, ToT, venue-only claims) are
  explicitly listed as not re-verified, with the rule that any that becomes
  load-bearing must earn a V-record first.
- Zero occurrences of "under review at TMLR" outside the historical R(h)
  record. NoisyCoconut's status is current: I fetched the live TMLR index
  myself on 2026-09-23 — "NoisyCoconut: Counterfactual Consensus via Latent
  Space Reasoning, Michael M. Jerge, David Evans, June 2026" is listed as a
  published paper with OpenReview/PDF/code links. The LOG-185 staleness is
  explicitly superseded (LOG-191 log + V12), not silently overwritten.

### 5. CLLC corrected with A-LQR as direct prior: CLOSED

- C1 Box 1 explicitly withdraws the false sentence ("no competitor predicts
  bound-holding feedback beating its own open-loop ablation") with the
  parenthetical "(A-LQR occupies exactly that comparison)."
- Activation-LQR is named as the direct prior for feedback-vs-open-loop
  control in the Novelty section and in Box 1.
- The surviving distinction is explicitly narrower: observer/controller/plant
  separation with cached gains, the pre-registered setpoint construction on
  the relational task, and a measured bound-holding result that A-LQR's
  formulation (setpoints on toxicity/truthfulness-style steering) does not
  predict.
- Companion corrections: C2 Box 1 now reads the auditable reviewed-literature
  claim (fixed-slot, externally addressable runtime scratch-buffer protocol);
  C6's duplicate merge-vs-select line is gone (phrase appears once as a test
  condition) and the absolute claim is scoped to reviewed literature.

---

## B. The 9 re-review acceptance criteria

1. **Law #3 verification of new prior-art claims:** PASS — Appendix V with
   17 records; my own fetches confirmed the three most load-bearing
   (NoisyCoconut/TMLR index, A-LQR/2604.19018 abstract, LTPO/2510.04182
   abstract) plus repo-local EXP048 JSON. The abstract-verified claims match
   the patch's characterizations exactly.
2. **Novelty boundary narrower than the invoked literature:** PASS — D2
   condition 3 (changed-burden box, "seven complete mechanisms"), honest
   tiers N1 throughout (B1 N0 for the tested static mechanism).
3. **p≥0.05 ban:** PASS — 4 occurrences, all in the standing-ban statements;
   never used as evidence against a candidate.
4. **MDE/power/multiplicity/selection-hierarchy fixed before NTDP data
   contact:** PASS — G1b: α₂=0.00714 over 7 candidates, 99.286% CIs,
   MDE≈7.5pp (95%) / 11.25pp (Level-2) stated, the power rule (MDE > 2·δ_min
   → held Inconclusive, no N increase pre-registered) encoded in Branch HOLD
   entry condition (a).
5. **A3/A7 as readout-path steerability:** PASS — sensitivity table with the
   EXP077 official bridge now directional-only (not margin-clearing), Law #7
   caveat binding on §C/§H, bridge cited as "one option-informed
   construction."
6. **K1/K2/K3 logically ordered and capable of collapsing the output-side
   interpretation:** PASS — §H6: K1 ($0, archived artifacts, logically prior,
   kill criterion cos≥0.9 or label-shuffle rescue-persistence), K2
   (bypass-vs-routing, 180 passes), K3 (Law #7 audit, ordered last because it
   bites only on a mechanism surviving K1). Ordering binding on
   interpretation; parallel preparation permitted — sound.
7. **Mechanism-testing baselines:** PASS — TTPS interpreter-only control
   with the L3 decision rule (interpreter alone succeeds → Not supported for
   L3); §F3 five arms; pinned M15 protocols; Box-1 fingerprints per
   candidate.
8. **Online + amortized compute matching:** PASS — the two-number FLOP rule
   is applied in §G3, §G5, M15 pinning ("matched (a) online inference FLOPs,
   (b) amortized reported separately"), and the candidate arm's pass budget
   is set to the measured comparator cost on the pilot (no free FLOPs).
9. **H3 kill license executable without discretionary rescue path:** PASS —
   pre-registered, "executes without re-approval"; HOLD-suspension is
   statistically honest (a candidate with no verdict cannot satisfy a
   condition about verdicts — counting un-verdicted candidates as failures
   would manufacture a kill from underpower); HOLD with no remaining re-test
   path does not block the kill. Theory preservation is the named forbidden
   move.

---

## C. Fresh-object regression sweep

Read the whole document as a new adversarial object. Previously cleared
sections are preserved without weakening: A1's narrowed dissociation; A3's
bridge downgrade (strengthened by the margin-clearing adjudication);
A5's pooled equivalence ([−0.0126, +0.0126], U < δ_min); A6's refusal to
manufacture an oracle ceiling (EXP079 probe-infeasibility retained as a
standing gate); A9's decision-flip endpoint rule; D2's five conditions
(condition 3 strengthened, same requirement); F1's conditionality; H3's kill
license; §I's L1/L2/L3 grades; the power-honesty consequence; N1 novelty
tiers; the five permitted verdicts with the banned phrases nowhere as
verdicts. The changed-burden box now reads "seven complete mechanisms" —
consistent with the ASR fix. R(h) retains "α₂=0.00625 over 8 candidates"
verbatim inside the explicitly labeled LOG-187 historical record (legitimate
historiography, not a live prescription; all live sections use
99.286%/0.00714 consistently); R(i) logs every LOG-191 correction.

Non-blocking observations: (1) the historiography point above; (2) venue-only
claims for ∇-Reasoner/A-LQR/Meta-Reasoner rest on the same-day LOG-185
record with the provenance split declared in-text — no verdict depends on a
venue, and the one status that actually changed (NoisyCoconut) was re-checked
live; (3) §H7 honestly marks [OPEN] the CEO decision on whether a K1
readout-bias verdict demotes the bridge's positive-control status across
signed protocols — reserved for the CEO, not decided silently. The bridge's
interim status is "Supported (L1, mechanism [CONJECTURE], readout-bias audit
pending)" — honest.

---

## D. What this verdict licenses (and does not)

**ADOPT** means: the patched synthesis is the program's binding map and
protocol. It licenses G/H pre-registration and the queued experiments
(EXP080, EXP081 — still gated on the Law #7 bridge-leakage audit and CEO GPU
clearance; EXP068 only via a registered gate). It does **not** mean: any
capability claim — the document itself is a falsification protocol whose
honest consequence is that Branch S is likely unreachable at N=80. Adoption
is of the protocol and the novelty boundary, not of a result. The novelty
verdict remains N1 — Known Combination.

**Final verdict: ADOPT.**

*No GPU used; no signed protocols, primary artifacts, or prior review files
touched. LOG-194 succession recorded; LOG-195 logged. This gate was run by
the in-house mentor on 2026-09-23; ChatGPT's pending gate is superseded.*
