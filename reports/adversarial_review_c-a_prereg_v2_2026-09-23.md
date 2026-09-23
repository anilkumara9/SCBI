# Law #14 Adversarial Review — C-A Pre-Registration Draft v2 (LOG-181)

**Date:** 2026-09-23 · **Dispatch:** LOG-181 · **Reviewer role:** Law #14 Adversarial Reviewer
**Authority:** LOG-144 review line (same line as LOG-161 SIGN-WITH-CONDITION and the LOG-176
conversion ruling: REVISE — the five binding redesign requirements below).
**Target:** `experiments/protocols/C-A_DONOR_TRANSFER_PREREG_SPEC_V2.md` (741 lines, banner DRAFT,
no number minted), the v2 drafter's discharge of the LOG-176 REVISE.
**Mode:** analysis only; no GPU; no signed artifacts touched; no primary artifacts touched.
No research-log entry written (LOG-181 covers this dispatch).

## VERDICT: **SIGN-WITH-FIXES** (two fixes, F1–F2, enumerated in §7)

The v2 draft discharges four of the five LOG-176 requirements cleanly and the fifth
substantially — the tie-break-robustness battery is the ruling-licensed hardening and the
"keeps every computed value valid" rationale is legitimate, not convenience (§5). The
C5-deletion proof is sound, the reachability repair is genuine, the T4 cap sits in the
license language, the budget recomputes, and every re-attached audit value verifies against
the LOG-160/174 JSON twin (§1–§2). What blocks full SIGN is a defect the drafter's own
attached audit makes material: the S1–S6 sensitivity battery's agreement flag does not
account for duplicate-content twins of the C4′ winner, which agree with the winner's T3
reading **by construction** (identical centroid → identical decisions) and inflate the
agreement count, letting the pinned "tie-break-fragile" flag under-fire (F1). A secondary
phrasing ambiguity in the battery's enumeration rule needs one clarifying edit (F2). Both
fixes are pre-registration-compatible: neither changes the arm structure, the budget, or
any attached audit value. On application of F1–F2 the banner advances to PRE-REGISTERED;
the number mints at CEO signing from the then-next-free pool (§8).

---

## 1. The five LOG-176 requirements: discharge verification (none trusted)

**Requirement 1 — "Resolve C5 honestly: drop the arm or prove a distinct prior-control."**
**DISCHARGED.** The draft chose deletion with proof (§R0.1, §5.2, §4.1 [THEOREM]).
Independent verification of the proof, from the pinned construction alone:
b̂_D = normalize(Σ_d (W_U[t_d] − W_U[f_d])) regroups to normalize(Σ_y W_U[y]·(n_t(y) −
n_f(y))) — regrouping terms is exact, and identical per-token coefficients give identical
unnormalized sums, hence identical normalized vectors. The three-desiderata
unsatisfiability follows: (i) prior preserved ⟺ identical (n_t−n_f) ⟹ centroid identical
⟹ (iii) geometrically distinct fails; (ii) relation-destroyed-with-prior-preserved is, in
this family, exactly a multiset-preserving re-pairing ⟹ centroid identical ⟹ (iii) fails;
a different (n_t−n_f) ⟹ (i) fails. The JSON twin corroborates: cos(b̂_C5,b̂_C3) =
0.9999999999999998, g(C5) = 1.0617830595495654 = g(C3) to all digits. The v1 §5.2
[PROPOSITION] ("C5's centroid differs from C3's") is **struck, not patched** — §5.2 quotes
it, declares it FALSE as pinned, and records why (donor premises never enter b̂_D). v1-T5
deleted; `SEED_C5_PERM=20261067` RETIRED (four mentions, all as retired); grep over the
full spec confirms **zero live C5-referencing clauses** — every remaining "C5" mention is a
retirement record, the deletion proof, or the §12 checklist's [C5-RETIREMENT] item. The v1
file itself is untouched (23 C5 mentions still present — the unsigned-draft discipline
holds). §13's rebuilt follow-up does **not** smuggle the vacuous idea back: it explicitly
drops the permuted-bank null as a point mass under the identity and rebuilds it under a
*different* centroid construction (per-donor-normalize-then-average), where permuting
target–premise pairings genuinely changes per-donor unit vectors and hence the centroid —
algebraically non-vacuous, and fenced out of this design (new number, Law #4).

**Requirement 2 — "Decide the T3/T4/T6-without-prior-control battery explicitly."**
**DISCHARGED.** §8 carries the theory-role [AFFIRMATION]: with no prior-control
constructible in this family (§R0.1), discrimination rests on T3 (donor-relation-template
channel, C4′ similarity-matched within δ), T4 (within-bank similarity-gradient channel,
low-similarity stratum), T5 (per-item similarity-covariate channel, β1 with arm-specific
s_t/s_f covaried) — the three observable implications of relation-mediated steering. The
bank-prior channel's non-lesionability is recorded as a **known limitation of the Level-1
license**, with the identity theorem cited as the reason — not as a hole in the battery.
Reachability of every terminal is proved, not asserted (§4 below).

**Requirement 3 — "Carry the T4 entity-group caveat into the license language."**
**DISCHARGED.** The "~30/30" aside survives only as historical record ("was an expectation
under a continuous-feature assumption; it does not obtain and does not survive in v2" —
§4.4, §6, §12); it appears nowhere as a live expectation. The binding cap — "transfer
across **at most 3 independent low-similarity target entities** ({Mars, Venus, Iron})" —
appears in §6's license caveat **and** in the outcome-(a) license line in §8, i.e., in the
license language itself, not just an audit appendix. The stratifying feature's zero
within-entity variation is stated at both sites.

**Requirement 4 — "Harden C4′ selection against the singleton fragility."**
**DISCHARGED with one gap (F1).** The drafter chose the ruling-licensed tie-break-robustness
option: the pinned greedy rule stands (winner `ca_C4cand_V5_Modern_triple_1`, D=0.046564 ≤
δ=0.05, g(B)=0.860981 — all verified against the JSON twin), the fragility is disclosed in
the T3 reading (7 δ-satisfying singletons, lowest-index tie-break, D within 7% of δ:
0.046564/0.05 = 0.9313), and the S1–S6 battery reports the tie-break spread descriptively
with a pinned agreement flag that can mark the T3 reading "tie-break-fragile" but can
never promote or demote the verdict. The already-resolved demotion fallback is deleted
rather than retained as an unreachable branch. The gap: the battery's agreement flag does
not handle duplicate-content twins (F1, §5/§7). The 7%-of-δ disclosure prong is satisfied.

**Requirement 5 — "Recompute the budget; re-pin seeds; re-run the audit against the revised
construction."** **DISCHARGED.** Budget from the final arm structure: 5 deciding arms
(C1, C2, C3, C4′, C6) × 60 = **300**; 6 exploratory arms (S1–S6) × 60 = **360**;
**total 660**. Stage 0 remains 0 GPU. Seeds re-pinned (`SEED_TORCH=SEED_NUMPY=20260923`,
`SEED_C6=20260989`, `SEED_PERMNULL=20261123`; `SEED_C5_PERM` retired); α=0.50, l*=20,
hook pinned (§10). On the audit: the revised construction's bank set is {C3 20-donor
list, C4′ selected singleton} — **unchanged from v1** — so the LOG-160/174 weight-only
values still apply without re-running; §4.5 pins the recomputation rule for any future
bank-set change. C5's values are retired as license values and retained only as identity
evidence (§2.7 below). Requirement 5's re-run clause is satisfied by the no-change
justification plus the §4.5 forward rule.

---

## 2. The drafter's seven claims: verified, not trusted

1. **C5 dropped with proof** — verified (§1, Req. 1; proof independently re-derived in §3).
2. **Budget recomputed: 300 + 360 = 660** — verified by arm count (§1, Req. 5). The S1–S6
   battery is genuinely exploratory: its T3-analog McNemar statistics are pinned
   "descriptive only," the agreement flag is a pinned descriptive caveat, and the spec
   states twice that it never promotes or demotes the verdict. It is not a deciding arm
   in disguise — with the F1 caveat on the flag's denominator.
3. **Every decision-tree terminal provably reachable** — verified under adversarial attack
   (§4). The v1 kill-only defect is repaired: outcome (a) is reachable, and no
   tautological refutation clause survives.
4. **T4 capped at 3 entities; "~30/30" deleted; caveat in the license** — verified (§1,
   Req. 3).
5. **C4′ hardening via tie-break-robustness battery** — substantially verified; ruling in
   §5 (choice legitimate; battery answers the licensed fragility modulo F1).
6. **The nine (c) items adapted** — verified: §12 checklist carries all nine, with item 4
   correctly adapted to [C5-RETIREMENT]. Spot-verified: McNemar-only endpoints (§9, with
   KL as exploratory guardrail only); Level-1 cap with zero affirmative Level 2/3 claims
   (all "Level 2"/"Level 3" mentions prohibitive); five permitted verdicts only
   (Supported / Not supported / Inconclusive / Underdetermined / Refuted); double-labeling
   maintained; evidentiary levels capped; the verbatim anti-creep sentence —
   "A C3 win that fails any of T3–T5 is not transfer; it is similarity/prior steering
   consistent with audit Finding 4." — byte-identical to LOG-144 §b.6.16 except the
   renumbered range, and the T3–T5 renumbering is consistent everywhere (every "T6" in the
   spec is a historical v1 reference: "v1's T6," "ex-T6," "old-T6 → new-T5," "v1-T3–T6");
   seeds/α/l*/hook pinned; SHA-256 Δθ=0 guards with attached tri-match; EXP058 and
   EXP078(a) cited-and-distinguished; N1 retained; bank balancing prohibited.
7. **Re-attached audit values** — verified value-by-value against the JSON twin:
   g(C3)=1.0617830595495654 → 1.061783 ✓; g(C4′)=0.8609809349756752 → 0.860981 ✓;
   C4′ D=0.04656406188177837 → 0.046564 ✓ (n_selected=1, branch STOP-D≤δ, demotion
   correctly unfired); per-item |s_t| deviations 0.006682/0.026718/0.043542/0.024645 ✓;
   per-item |s_f| deviations 0.005491/0.021975/0.069394/0.021919 ✓; strata 49/11 ✓;
   low-stratum headroom 23 ≥ 5 ✓ (C1-wrong 26/60 from the EXP066 prior artifact);
   permutation null 38.0th percentile ✓ (null −0.034053 ± 0.013496);
   s_t min/median/max −0.091793/−0.035416/0.081702 ✓; 9/60 with s_t > s_f ✓;
   SHA-256 pre=post=archived=`ec276abe3902fab0…` ✓. All are the LOG-160/174 computed
   values and all remain valid under the v2 bank set, which is unchanged. C5's values
   (seed 20261069, cos=0.9999999999999998) appear only as evidence for the §R0.1 identity
   finding — no v2 license value depends on them (confirmed by full-text grep: zero live
   C5 clauses).

---

## 3. The C5 identity theorem: independent verification

The §4.1 [THEOREM] as pinned: for banks D, D′ over the same vocabulary, identical
per-token (n_t−n_f) ⟹ b̂_D ≡ b̂_D′. Proof re-derived from the pinned formula, not from
the drafter's summary: Σ_d (W_U[t_d] − W_U[f_d]) = Σ_y W_U[y]·(n_t(y) − n_f(y)) by term
regrouping (exact); identical coefficient vectors give identical unnormalized sums;
normalization is deterministic — identity follows. The corollary (three desiderata
jointly unsatisfiable) is proved in §R0.1 and re-verified in §1 above. **The theorem is
sound; the deletion is the honest resolution.** Note for the record: the proof's force
comes from the pinned algebra (sum-of-differences-then-normalize); it does not claim
anything about other construction families — which is exactly why §13's rebuilt
different-algebra idea is non-vacuous and correctly fenced out of this design.

---

## 4. Reachability attacks on the four terminals

- **(a) Supported (T2 holds; T1∧T2∧T3∧T4∧T5).** Attacked for hidden mutual exclusion:
  none found. The identity theorem constrains only (n_t−n_f)-preserving banks — the
  deleted C5 family. C4′'s centroid is geometrically distinct from C3's (D=0.0466>0 on
  the similarity profile ⟹ centroids differ, since identical centroids would give
  identical profiles), so paired C3-vs-C4′ decisions can differ in either direction; the
  low stratum (49 items, 23 headroom) is a fixed non-empty set on which C3-vs-C1 McNemar
  can independently fire; β1 can be positive while (s_t,s_f) vary. Witness world
  (relation-mediated steering) is coherent. **Reachable — the kill-only defect is
  repaired.**
- **(b) Not supported, family-scoped kill (T2 holds; ΔM_C3 ≤ 0).** Witness: EXP077's
  static-variant world (ΔM=0, p=1.0) with the C2 positive control rescuing — an
  empirically observed configuration. **Reachable.**
- **(c) Not supported / Refuted (T1 holds; any of T3–T5 fails).** Witnesses: the H_leak
  world (C4′, different relation but similarity-matched, rescues the same items — T3
  fails); rescue concentrated in the high stratum (T4 fails); rescue fully explained by
  s_t−s_f with β1 null (T5 fails). Each is a coherent data-generating world; the two
  Refuted sub-conditions are non-tautological. **Reachable.**
- **(d) Inconclusive (T2 fails).** Witness: procedure-invalid world; T2-first precedence
  pinned and overriding. **Reachable.**
- **New one-sidedness sweep:** none found. The v1 paired C3-vs-C5 tautology is deleted;
  the resolved demotion fallback is deleted rather than left as an unreachable branch;
  the S1–S6 flag cannot move any verdict. The design licenses as well as kills.

---

## 5. Ruling on the C4′ hardening choice

**The drafter's choice is legitimate, and "keeps every computed value valid" is a valid
reason — but the battery has one honest-reporting gap (F1).**

LOG-176 licensed two options: a minimum bank size **or** a tie-break-robustness
sensitivity rule, giving the sensitivity form explicitly ("report the T3-relevant spread
across tied winners as a sensitivity analysis — descriptive, not deciding"). The drafter
built exactly that: the 6 non-winner δ-satisfying singletons as exploratory arms, T3-analog
McNemar reported descriptively, a pinned agreement flag ("fewer than 5 of 6 alternates
agree" → "T3 reading is tie-break-fragile (m/6 alternates agree)") that never promotes or
demotes. Pinning a minimum bank size > 1 would have changed the bank and voided the
attached $0 audit — the very audit LOG-176 requirement 5 demands be re-run against the
revised construction. Choosing the option that preserves the audit while answering the
fragility is rigor (the ruling licensed it), not convenience dressed as rigor.

**The gap (F1):** the battery's agreement count does not account for duplicate-content
twins. The attached audit establishes the material facts: the 150-candidate pool carries
only 30 distinct (t,f) pairs (120 duplicate-content items), and "a duplicate-content twin
of the winner exists in the pool." A twin shares the winner's (t,f) pair exactly, hence
its centroid, its D, and all 60 per-item decisions are **identical** to the winner's —
it agrees with the winner's T3 reading **by construction**, contributing zero robustness
information while inflating m. The pinned <5/6 flag can therefore under-fire: with t
twins among the 6 alternates, the flag needs ≥2 of the 6−t distinct-content alternates to
disagree before firing. The spec discloses the twin in the T3 fragility paragraph but
never connects it to the battery's agreement denominator — a Law #2 gap in the
pre-registered reporting machinery. Fix F1 (§7) closes it without touching the arm
structure, the 360-pass exploratory budget, or any audit value.

---

## 6. New attack surface

**(1) No prior control — honestly disclosed.** With C5 deleted, no arm independently
lesions the bank-prior channel. The draft does not hide this: §8's [AFFIRMATION] states
it, §13's "one challenge" names it as the strongest attack on the design and gives the
pre-registered answer (T5 includes arm-specific s_t and s_f; T4 tests rescue where the
measured similarity channel is weakest; T3 varies the donor relation template with
similarity matched; the identity theorem is cited as the reason no stronger prior-lesion
exists in this family), and it is recorded as a known limitation of the Level-1 license.
The battery still discriminates — T3/T4/T5 close three distinct observable channels of
the leakage hypothesis — and the residual prior-channel gap is disclosed, not papered
over. This is the trade the LOG-176 requirement-2 affirmation licensed.

**(2) The 360-pass exploratory battery — pre-registered with exact procedures, not a
vague umbrella.** The set is rule-defined (the 6 non-winner singleton candidates with
D({c}) ≤ δ, executor build-asserts exactly 6); α, l*, hook, and decision rule are the
pinned ones; the reported statistics (T3-analog paired McNemar b_k, c_k, p_k) and the
agreement criterion are pinned; the flag's consequence (a caveat on the license line) and
its non-effect on the verdict are pinned. There is no discretionary "sensitivity"
umbrella for post-hoc analyses to hide under (Law #9). The two precision gaps are F1
(twin handling) and F2 (enumeration phrasing) in §7.

---

## 7. Fixes required before SIGN (F1–F2)

**F1 — De-duplicate (or separately report) duplicate-content twins in the S1–S6
agreement flag.** Pin that the agreement count is computed over **distinct (t,f)-content
alternates only**: (i) the executor enumerates the 6 non-winner D≤δ singletons in
ascending candidate-index order (S1–S6 labels; the 360-pass exploratory budget is
unchanged); (ii) alternates with (t,f) content identical to the winner's are reported as
"twin — agrees by construction" and **excluded from the agreement denominator**; (iii)
the fragile flag is re-pinned on the distinct-content denominator (e.g.,
'T3 reading is tie-break-fragile (m/n distinct-content alternates agree)' with a pinned
firing threshold the drafter chooses — it must be pinned pre-signing and must be
satisfiable, i.e., capable of firing); (iv) the executor build-assert is extended:
recompute D({c}) over all 150 candidates from W_U, assert the non-winner D≤δ set has
exactly 6 members and the winner is `ca_C4cand_V5_Modern_triple_1`, then apply the
de-duplication rule deterministically. No arm-structure, budget, or audit-value change.

**F2 — Clarify the enumeration phrasing.** §5.1's "ids enumerated in ascending
candidate-index order" is ambiguous (it reads as if the six ids are listed in the spec;
they are not — the set is rule-defined from the pinned audit). Rephrase to state
explicitly that the **executor** performs the enumeration in ascending candidate-index
order (after the F1 de-duplication) to assign the S1–S6 labels.

On application of F1–F2 (drafter's edit, no re-review of unaffected sections required
beyond a fix-verification pass), the banner advances to PRE-REGISTERED.

---

## 8. Number mint

The draft states "currently next free EXP081 — re-verify unminted at signing time."
**Verified today:** EXP080 was minted at the LOG-172 G2 signing (research log); no
`exp081` run directory exists; no protocol file or report references EXP081 as minted;
the highest numbered protocol/run in the repo is EXP079/exp079. **EXP081 is the next
free number as of this review** — the CEO must still re-verify unminted at signing time
per the draft's own rule, since another line could mint first.

---

## 9. Adversarial independence note

This verdict answers to the CEO alone. The drafter's seven claims were re-verified
item by item against the pinned text and the JSON twin — six verified clean, one
(C4′ hardening) verified with the F1 gap the drafter's own attached audit made visible.
The SIGN-WITH-FIXES verdict is not a softening: F1 is a genuine Law #2 defect in the
pre-registered reporting machinery (a fragility flag that can be padded by
construction-identical arms), and the fixes are enumerated precisely enough to verify
without re-litigating the design. No instruction to soften was received; none would
have been honored.

*End of LOG-181 review.*
