# Law #14 Review of the LOG-191 Patch (LOG-192) — Independent Adversarial Review, 2026-09-23

**Reviewer:** Independent Law #14 reviewer. No prior involvement in the synthesis,
the LOG-158/187 reviews, or the LOG-191 patch. The drafter's claims about the
patch were treated as untrusted; every item below was checked against the
document itself, `research/synthesis/SYNTHESIS_A_J_REV2_2026-09-23.md`.

**Target:** `research/synthesis/SYNTHESIS_A_J_REV2_2026-09-23.md` (LOG-191 patch draft)
**Reference:** `reports/adversarial_review_synthesis_rev2_mentor_2026-09-23.md` (the
mentor's second review; the five defects), LOG-190/LOG-193 (CEO orders + final
adoption gate criteria), `research/CHATGPT_MENTORSHIP_DIRECTIVE.md` (standing laws).

**Final disposition: SIGN.** All five defects are closed as *eliminations from the
protocol's logic*, not as prose acknowledgments. The fresh-object regression sweep
found no regression in previously cleared sections. Two non-blocking observations
are recorded at the end (historiography and venue-provenance — neither drives a
verdict). No fixes are required before the mentor's final adoption gate.

---

## Acceptance-gate audit — per defect

### Defect 1 — M15 genuinely load-bearing: **CLOSED**

The D2/G3/G4 contradiction is eliminated by conjunction, not by rhetoric:

- **§G4 Branch S condition (vii)** (lines ~1536–1544): Branch S requires the
  candidate-specific M15 comparator (§G3) be cleared **at the Level-2 standard**
  — "C\* beats M15 at matched (a) online inference FLOPs with lower 99.286% CI
  (1−α₂) > δ_min = 0.05, OR the pre-registered structural-comparison path below
  is licensed. M15 is not optional: a Branch-S license that skips the
  newer-prior-art comparator is invalid." Level-2 conditions (i), (ii), (vii)
  are gated jointly (§G1b, lines ~1350–1358: "the gate passes only if ALL clear
  δ_min at α₂").
- **§G3 M15 protocol-pinning rule** (binding, lines 1419–1440): each M15 is an
  executable protocol — frozen model, exact configuration, task construction,
  two-number FLOP accounting, all fixed before NTDP data contact. Four pinned
  protocols: M15-LTPO (T=8, η=0.1, intrinsic-confidence reward, [PINNED-CHOICE]
  marked), M15-MetaReasoner (dormant until ASR activates), M15-LatentMAS
  (R=3, D=2, shared latent working memory), M15-NoisyCoconut (K=5, σ=0.1, no
  abstention, [PINNED-CHOICE] marked where beyond the abstract). Zero
  "LTPO-style"-type hand-waving survives in live sections (the only generic
  "-style" occurrences are lines 2111–2135, inside the R(h) LOG-187 historical
  record — see observation 1).
- **[INCOMPLETE] M15 blocks, never clears** (§G3 + §G4 line 1542): "If the M15
  protocol is marked [INCOMPLETE]... condition (vii) cannot be evaluated and
  Branch S is BLOCKED for that candidate (verdict Inconclusive) — incompleteness
  is never read as clearance." The structural path requires M15 to be run as a
  control arm (condition (c)), so it cannot evade an [INCOMPLETE] M15 either.
- **Structural-comparison rule** (lines 1573–1588, "pre-registered; not an escape
  hatch"): the superiority test is waived ONLY IF all three trigger conditions
  hold — (a) a pre-registered observable mechanism property *independent of the
  measured gain* with a pre-registered operational check ("'different
  architecture' as a redescription of the mechanism, without an independent
  operational check, never qualifies"); (b) established on the NTDP; (c) M15
  still run as a Level-3 control with a pre-registered failure-mode prediction —
  AND conditions (i)–(vi) hold, AND M15 does not beat C\* at the Level-2
  standard ("if M15 clears δ_min over C\* at α₂, the structural claim is Not
  supported"). This matches the mentor's explicit allowance ("or otherwise
  demonstrating a pre-registered structural distinction") with trigger conditions
  precise enough to bite.
- **Branch HOLD** (line 1552): program-level hold with explicit entry conditions
  (Inconclusive primary comparison incl. the MDE > 2·δ_min power rule,
  uninformative licensing control, [INCOMPLETE] comparator, [INCOMPLETE]
  candidate). Release requires a fresh pre-registration — fresh task-family
  construction, re-consumed Level-2 budget, blocking defect repaired; "a held
  candidate never re-enters on the same data or by re-analysis." A candidate that
  exhausts its re-test path exits HOLD to the applicable F-branch verdict,
  "never to Branch S by attrition."
- **H3 interaction is sound** (§H3 condition 1): HOLD with an active
  pre-registered re-test path suspends the family kill verdict to Inconclusive
  (a candidate with no verdict cannot satisfy a condition about verdicts —
  counting it as a failure would manufacture a kill from underpower); HOLD with
  no remaining re-test path does not block the kill. The kill license remains
  executable without a discretionary rescue path (line 1685–1695: "executes
  without re-approval").

### Defect 2 — ASR internally consistent: **CLOSED**

- Zero occurrences of "8/8" in the document (verified by grep).
- Every counting site reads **"7 complete candidates + 1 pending candidate
  (ASR), not eligible for experimental triage until policy scope is frozen"**:
  §E summary table (C4 row: "pending — boxes answered but [INCOMPLETE]: not
  eligible for §F/§G until policy scope is frozen"), §E paragraph (line 1129),
  §F1 (C4 excluded, ablation specified prospectively only), §G1b Level-2 budget
  (α₂=0.05/7=0.00714, 99.286% CIs — "C4/ASR is [INCOMPLETE] and excluded from
  the NTDP and from this budget"), §§H1/H3/H4, §J Stage 1, checklist line 2250.
- §C4 (lines 917–975): policy-scope declaration explicitly [INCOMPLETE]; "C4/ASR
  may not enter §F culling or §G NTDP runs — and no Box-1/Box-2 verdict for ASR
  is licensable — until the policy-scope declaration is pre-registered."
- The checklist (line 2250) lists the seven complete as "C1, E7, C2, C3, C5,
  C6, E8-conditional" + "1 pending candidate (C4/ASR, [INCOMPLETE])". E8's
  conditionality is flagged at every count and the Level-2 budget does not get
  re-divided if E8 never activates (conservative, §G1b). No statement counts
  ASR as complete.

### Defect 3 — LCMIC bandwidth isolation: **CLOSED**

- §F3 (lines 1207–1252) is a five-arm design: (a) C5 full latent, (b) C5-text,
  (c) debate/MoA, (d) M15-LatentMAS, (e) **bandwidth control** — latent channel
  compressed to text-equivalent payload (pre-registered top-k PC compression,
  payload_bits(e) ≤ payload_bits(b), frozen before data contact). Arm (e) is a
  real arm, not an appendix note.
- **Bandwidth-isolation rule, binding licensing condition** (line 1230): "If
  L_(a−e) > δ_min... the channel-representation claim is **Not supported** and
  C5's Branch S is BLOCKED (§G4 condition (v)). If U_(a−e) < δ_min... the
  raw-capacity account is ruled out. If the (a−e) CI overlaps δ_min ⇒
  Inconclusive for the isolation question — C5 is held (Branch S blocked)."
- §G4 condition (v) (lines ~1530–1536) incorporates the rule verbatim; C5's
  Box 1 carries the (e) condition as a conjunct of unique support ("the
  bandwidth-isolation arm (e) matches full latent (a) at the practical margin
  (U_(a−e) < δ_min)"), with the explicit withdrawal clause if L_(a−e) > δ_min.
  The protocol forbids attributing raw channel capacity to the mechanism.

### Defect 4 — Fresh-object literature audit: **CLOSED**

- **Appendix V** (lines 2286–2459): 17 records (V1–V17), each with source URL,
  fetch date (2026-09-23), verdict (VERIFIED / PARTIALLY VERIFIED / UNVERIFIED),
  exact supported claim, and textual consequence. Covers B1 (CAA, Activation
  Addition), B4 (PPLM, Self-Refine), B5 (DEER, STARS, ∇-Reasoner, Activation-LQR),
  D1/M15 (Meta-Reasoner, LTPO, LatentMAS, NoisyCoconut), A8 (EXP048/049/056/057/058
  primary JSONs). The Self-Refine "2–3 iteration plateau / blind spots" claims
  are honestly withdrawn as factual and restated as [HYPOTHESIS] (V4; B4 text
  repeats the withdrawal in-body). Non-load-bearing inherited references (RISER,
  ToT, venue-only claims) are explicitly listed as not re-verified with the rule
  that any that becomes load-bearing must earn a V-record first.
- **Independent spot checks by this reviewer (own fetches, not inherited):**
  (1) live TMLR index (https://www.jmlr.org/tmlr/papers/, fetched 2026-09-23)
  lists "NoisyCoconut: Counterfactual Consensus via Latent Space Reasoning —
  Michael M. Jerge, David Evans — June 2026" as a published paper — matches V12
  and every body citation; (2) arXiv:2604.19018 abstract confirms the A-LQR
  mechanism claims (layer-wise Jacobians, LTV system, LQR feedback, setpoint
  tracking-error bounds, no offline training, no parameter updates) and the
  corrected title — matches V8; (3) arXiv:2510.04182 abstract confirms the LTPO
  mechanism (parameter-free, test-time, latent thought vectors as dynamic
  parameters, online policy gradient, intrinsic confidence reward from the
  frozen LLM's own output distributions) — matches V10; (4) repo-local
  `experiments/runs/EXP056_autonomous_lifecycle/exp056_autonomous_results.json`
  read directly: base 0.6, unsup_selected 0.64, scpm_oracle 0.74, verdict
  SELECTION_BOTTLENECK_ACTIVE — matches V15.
- **Publication status current at patch time:** "under review at TMLR" appears
  zero times outside the historical R(h) record; all live NoisyCoconut citations
  read "TMLR June 2026 — published". Venue-only claims for ∇-Reasoner/A-LQR/
  Meta-Reasoner rest on the same-day LOG-185 record with the provenance split
  declared in-text and in V7/V8/V9 ("rests on the LOG-185 ... record"); venues
  drive no synthesis verdict (the mechanism characterizations, which do, are
  abstract-verified today). The LOG-185 NoisyCoconut staleness is explicitly
  superseded (LOG-191 log + V12), not silently overwritten.

### Defect 5 — CLLC corrected: **CLOSED**

- C1 Box 1 (lines 731–741): the old sentence "No competitor predicts
  bound-holding feedback beating its own open-loop ablation" is explicitly
  **withdrawn**, with the parenthetical "(A-LQR occupies exactly that
  comparison)". Activation-LQR is named as the direct prior for
  feedback-vs-open-loop control in both the Novelty section (line 711) and Box 1.
- The surviving distinction is explicitly narrower: "the observer/controller/
  plant separation with cached gains, the pre-registered setpoint construction
  on the relational task, and a measured bound-holding result that A-LQR's
  formulation (setpoints on toxicity/truthfulness-style steering) does not
  predict — the mechanism-level differentiation from A-LQR."
- Companion corrections verified: C2 Box 1 now reads "Among the reviewed
  comparators, no identified method uses ELM's specific fixed-slot, externally
  addressable runtime scratch-buffer protocol" (no more "no competitor has
  cross-pass accumulating state"); C6 Box 1's duplicate merge-vs-select line is
  gone (the phrase appears once as a test condition; the closing sentence is a
  distinct discriminator statement) and the absolute claim is scoped to
  reviewed literature.

---

## Fresh-object regression sweep (whole document read as a fresh object)

| Section | Result |
|---|---|
| A1 narrowed dissociation | Preserved: raw cosine observed, semantic reading suspended pending anisotropy-controlled nulls; licensed dissociation = geometric similarity without causal transfer; verdict Supported on the dissociation as a boundary proposition. |
| A3 bridge downgrade | Preserved and strengthened: per-demonstration CIs with margin-clearing adjudication (EXP077 official is directional-only, not margin-clearing); one option-informed construction, not independent confirmations; Law #7 caveat binding on §C/§H. |
| A5 pooled equivalence | Preserved: pooled 300-item CI [−0.0126, +0.0126], U < δ_min, Not supported via equivalence-to-null within the licensed narrow bounds. |
| A6 no-oracle-ceiling | Preserved: "an oracle ceiling exists for the loop" → Inconclusive; EXP079 probe-infeasibility retained as standing gate. |
| A9 decision-flip endpoint | Preserved: margins inadmissible, McNemar decision-change only. |
| D2 five novelty conditions | Preserved; condition 3 strengthened to reference the pinned §G3 M15 protocols (same requirement, executable form). Changed-burden box updated to "seven complete mechanisms". |
| F1 conditionality | Preserved: ASR excluded from triage; adaptive-ablation with four-cell mapping; demote-not-cull on underpower. |
| H3 kill license | Preserved: pre-registered, executes without re-approval, theory preservation named forbidden; HOLD-suspension clause is statistically honest (no verdict → Inconclusive, not killed; exhausted re-test → F-branch), not a rescue path. |
| §I L1/L2/L3 | Preserved: three grades bound to the three evidentiary levels; definition rules out the entire current corpus (working as intended). |
| δ_min | Re-justified on treatment-independent decision-theoretic grounds (5pp = smallest effect changing the program's resource decision given the standing ≥2F/item cost structure; no observed effect enters); one value frozen; 2/5/10pp sensitivity table reported but never used for verdicts (§G1b). |
| Power honesty (LOG-189 consequence) | Preserved: MDE > 2·δ_min → held Inconclusive; no N increase pre-registered; Branch HOLD entry condition (a) encodes it. |
| Novelty tiers | Conservative: every candidate "Honest tier: N1 until..." — N1 — Known Combination stands unless the protocol honestly earns better; B1 explicitly N0 for the tested static mechanism. |
| Banned verdict phrases | None of "interesting/promising/elegant/worth another experiment" appear as verdicts; the string "p ≥ 0.05" appears only in the standing ban itself. |

---

## Non-blocking observations (not adoption defects)

1. **R(h) historiography.** Line 2124 retains "α₂=0.00625 Bonferroni over 8
   candidates" — inside the explicitly labeled LOG-187 historical record, which
   the patch policy retains verbatim ("not back-edited into R(h)"), with the
   change to 7 documented in R(i) (lines 2163–2239). All live sections use
   99.286%/α₂=0.00714 consistently (6 occurrences). This is legitimate
   historiography, not a live prescription — no fix required.
2. **Venue provenance.** V7/V8/V9 rest venue-only claims on the same-day LOG-185
   record with the split declared; no verdict depends on a venue. Acceptable —
   but the mentor may wish to note that the "current at patch time" bar was met
   for the one status that had actually changed (NoisyCoconut).

---

## What this review did NOT do

No GPU was used; no signed protocol, primary artifact, mentor review file, or
REV/LOG-158 file was touched. The REV2 draft is a text-and-citation patch only,
as ordered. The patch drafter's claims were not trusted; all line references
above are this reviewer's own checks.

**Disposition: SIGN** — the patched synthesis may proceed to the mentor's final
adoption gate.
