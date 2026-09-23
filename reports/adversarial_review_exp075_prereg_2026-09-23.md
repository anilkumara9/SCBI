# Adversarial Review — EXP075 Pre-registration (Subspace-Restricted Bridge)

**Reviewer:** Adversarial Reviewer (Law #14)
**Date:** 2026-09-23
**Draft reviewed:** `experiments/protocols/EXP075_SUBSPACE_BRIDGE_PREREG_SPEC.md`
**Sources checked against:** `research/innovation/SPRINT_2026-09-23.md` (Idea 7),
`reports/adversarial_audit_exp065_exp066.md` (boundary facts, Findings 3–4),
`experiments/scripts/run_exp066_pythia410m_replication.py` (B_agg construction, support procedure, bridge),
`experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md` (template standard),
`AGENTS.md` (14 laws)

## VERDICT: SIGN-WITH-FIXES

3 MAJOR (M1–M3) + 4 MINOR (m1–m4), all fixable on paper. The core experiment —
project the known-working bridge into the contrast subspace and test for a causal
direction at matched injection scale — is sound. Every flaw is in the hypothesis
wording, the energy-gate description, or the decision-tree licenses. The draft was
**not edited**.

---

## M1 [MAJOR] — Branch (e)'s license over-licenses across three compounding gaps (the Finding-4 confound)

The drafter's §9 Finding-4 caveat is honest. The operative LICENSES text in branch
(e) is not. A C4 rescue (ΔM>0, p<0.05) is consistent with three readings the current
license collapses into one:

**(a) The energy gate does not screen the mechanism confound.** The bridge is
unit-norm, so $e = \|P_S(\mathrm{bridge})\|$. But $u_S$ is **renormalized** to unit
norm and injected at α=0.50 — identical scale to the working C3. At the gate floor
$e = 0.10$, the retained 10% is injected at **10× its natural scale** in the bridge.
Per audit Finding 4, the bridge is near-direct answer-logit steering (bridge KL
0.028 vs ~0.0002 for basis conditions — only the bridge meaningfully moves the
output distribution). If the retained 10% carries logit-steering residue, (e) fires
**for the wrong reason**: S contains a direction with decision-efficacy, but via
amplified logit-steering, not via anything the loop's relational search would
recognize as its target. The energy gate guards *null-interpretability*
("a null under near-zero projection is uninterpretable") — it does not, and
structurally cannot, screen the mechanism confound, because renormalization
decouples retained energy from injection strength. §3.4 as written invites the
misreading that passing the gate validates the test against this confound.

**(b) Per-item existential vs. global direction.** $\mathrm{bridge}(x)$ is built from
item $x$'s own target/foil tokens, so $u_S(x) = \mathrm{normalize}(P_S(\mathrm{bridge}(x)))$
is **item-specific**. The test therefore establishes the per-item existential
$\forall x\, \exists d_x \in S$ (rescuing), *not* the singular "a causally efficacious
direction" that H_sub (§1) and the §7.0 canonical criterion state. The loop is
per-instance ($B^*(x)$), so the per-item form is the right match for loop-motivation —
but the license must say so, and must not license the stronger global-direction
reading.

**(c) Label-informed existence vs. label-free search.** $\mathrm{bridge}(x)$ uses the
test item's target and foil — labels. The existence proof is **oracle-sense**: the
room is non-empty *as judged by a procedure that knows the answer*. The EXP068 loop
searches label-free (target-free cross-view agreement). "The loop's search-within-$S$
problem is well-posed" overstates by one logical step: well-posedness for a label-free
search is not established by a label-informed existence proof. The honest claim is
that the search problem is **non-vacuous in the oracle sense**. The "treasure is in
the room" metaphor does persuasive work here — the treasure was found *with a map*.

**Required:** (i) rewrite (e)'s LICENSES to the weakened form —
"for rescued items, $S$ contains an item-specific direction, constructible with
label information, that rescues at the decision endpoint; the EXP068 loop's
per-instance search-within-$S$ problem is non-vacuous in this oracle sense" —
plus explicit mechanism disclaimer ("relational vs. logit-steering mechanism
unidentified; the energy gate does not screen this"); (ii) add to (e)'s
DOES-NOT-LICENSE: "that a label-free search can find such directions (EXP068's
own question; contingent on EXP070's ceiling verdict and EXP068's ρ-gate)"; the
draft's §9 already notes the EXP070 contingency — it must live in the LICENSES,
not only in §9; (iii) qualify or drop the "treasure is in the room" metaphor;
(iv) add the §3.4 disclaimer that the energy gate guards null-interpretability
only.

**Why no new control is demanded:** no cheap control separates "relational" from
"logit-steering" at the decision endpoint — any decision change moves logits, so a
sign-flip or shuffled-bridge discriminant cannot identify mechanism either. The
confound is not screenable by an additional condition at this budget; license
weakening is the correct fix, not a new arm.

## M2 [MAJOR] — H_sub's singular-direction wording mismatches the per-item operationalization

H_sub (§1): "$S$ *contains a causally efficacious direction*." The §7.0 canonical
criterion repeats the singular. But C4 injects $u_S(x)$, a different direction per
item (M1(b)). If (e) fires, the licensed claim must be the per-item existential —
a reader is entitled to take "a causally efficacious direction" as global, which
the test does not establish (a global rescuing direction in $S$ would require a
different test: one fixed $d \in S$ injected across items).

**Required:** reword H_sub and the §7.0 canonical criterion to the per-item
existential form ("for each rescued item, $S$ contains an item-specific direction
that yields the rescue"); add to (e)'s DOES-NOT-LICENSE: "a single global
rescuing direction in $S$."

## M3 [MAJOR] — Branch (d)'s boundary-revision license needs a comparability rider

(d) carries the strongest license in the tree — "revision of the program's central
boundary claim" — and supersedes (e)–(i). The comparability discipline is strong
(same model, layer 20, α=0.50, identical N=60 suite, SHA-256 guard), but the
headroom band [40%, 70%] is wide: a C2 rescue at 42% baseline against the
historical null (ΔM=0 exactly, $b=c=0$) at a different baseline could be partly
headroom-driven rather than a genuine mechanism revision.

**Required:** (d)'s ruling must report the historical EXP065/066 baseline accuracy
alongside the current run's baseline, with a pre-registered comparability rider:
if the baselines differ substantially, the "boundary revision" reading is qualified
accordingly (the numbers, not the adjective, carry the claim). One sentence plus a
reporting requirement — the license is too strong to fire without it.

---

## m1 [MINOR] — State the support/test entity-domain separation in §3.1

Verified in `run_exp066_pythia410m_replication.py`: support entities are person
names (Alice/Bob/…, Aaron/Caleb/…, Hector/Jason/…, Marcus/Lucius/…, Liam/Noah/…;
script L103–109), test entities are planets (Mars/Venus/Jupiter/Saturn/Mercury)
and elements (Iron/Gold/Silver/Bronze/Steel; script L223–224). The no-peeking
discipline therefore rests on a **structural** domain separation, not only on
procedural path hygiene. **Required:** state this in §3.1, and make the
"runtime assertion fails if any test-benchmark path is opened" concrete (e.g.,
path whitelist) so the implementation has something to implement.

## m2 [MINOR] — Anchor the energy gate and reword the (a) halt

Two fixes: (i) the 0.10 bar is marked [ARBITRARY], but it need not be fully so —
under no alignment, $\mathbb{E}[\|P_S u\|^2] = 5/1024 \approx 0.0049$, i.e.
$\mathbb{E}[e] \approx 0.07$ for an arbitrary unit vector. State this chance-level
derivation in §3.4: the gate demands the subspace capture *more of the bridge
than chance*, which is the principled content of the bar (the 0.10 value itself
may keep its [ARBITRARY] tag, now anchored). (ii) Branch (a)'s "uninformative"
label is slightly misleading: in the low-$e$ world the halt report's $e$ **is**
the localization measurement — "the bridge's causal power lies almost entirely
outside $S$." That is evidentially non-empty; what is uninformative is
specifically C4's causal test (renormalized noise). Reword (a)'s ruling to say so,
so the halt is not mistaken for a discarded outcome. (Note: this resolves the
apparent "heads I win, tails we don't play" asymmetry — the gate does not screen
out disconfirming evidence, because $e$ itself *is* the disconfirming measurement
for the localization question; it only withholds the causal-direction verdict
that a renormalized-noise injection could not support.)

## m3 [MINOR] — Multiplicity disclosure

Branches (e), (f), and (h) each involve a McNemar test; the tree's precedence
(a)→(b)→(c)→(d)→(e)→(f)→(g), with (h)/(i) conditional, is the operative
multiplicity control. **Required:** one sentence stating that no family-wise error
correction is applied, with the justification (pre-registered precedence;
motivation-grade, not confirmatory-efficacy, claims). Do not add a correction —
disclose its absence.

## m4 [MINOR] — Numbering hygiene verified clean (no fix)

Reservations — EXP069 (Idea 1), EXP071 (Idea 3), EXP072/073/074 (Ideas 4/5/6),
EXP076 (wildest credible) — do not collide with EXP075; the next-free-number rule
(§7.2, citing the EXP070 LOG-077 precedent) is consistent. Recorded as checked.

---

## Verified clean (by independent reading/computation, not on trust)

- **$B_{\mathrm{agg}} \in S$ exactly** (script L145–153: `B_agg = normalize(Σ_k v̂_k)` over
  the same five vocabularies spanning $S$). The draft's "tightening observation" is
  therefore valid, and airtight within-run: in branch (e), precedence guarantees (d)
  did not fire, so C2 was non-significant on *this* run — "the causal direction in
  $S$ is not the mean direction" follows without leaning on history alone.
- **Renormalization is exactly matched**: C3, C4, C5 all inject unit-norm vectors at
  α=0.50 (script L391–393, L419–423 confirm the bridge/hook scale convention). "The
  test is about direction, not energy" is correct; no unfair-scale concern.
- **Rank guard halts on degeneracy** (σ_min/σ_max > 10⁻⁶); a near-degenerate $S$
  passing the guard is still a valid (lower-dimensional) subspace, not a vacuous test.
- **Budget**: 7 × 60 = 420 forward passes; <30 min on a Kaggle T4 is credible for
  pythia-410m.
- **N1 framing** (§1.1) holds: closest priors ReFT/LoReFT (Wu et al. 2024) and DAS
  (Geiger et al. 2024) with the constructed-vs-learned delta stated; "cannot move
  the novelty needle" explicit.
- **O5/Wilcoxon lesson honored**: margin shifts exploratory-only, with the
  $B_{\mathrm{wrong}}$ invalidation cited.
- **SHA-256 binding guard**, **Law #13 archiving** ($Q_S$, the five $\hat{v}_k$,
  pre-norm and unit-norm projections, per-item energy ratios, rank diagnostics,
  per-instance records — the T-1 lesson applied), **halt semantics** (halts are
  reportable; silent re-runs forbidden), **decision-tree precedence stated**.
- **Branch (h)** ("the bridge's causal power is not in the contrast subspace") is the
  most honestly worded branch in the tree — it claims about the *bridge*, where the
  evidence lives, and needs no weakening.

## Ruling on the Finding-4 confound (as tasked)

**Branch (e)'s license survives WEAKENED — not "not at all."** The weakening is
sufficient because the loop genuinely searches per-instance directions in or near
$S$: EXP068's $\mathcal{G}_1$ candidates are aggregates of the same $\hat{v}_k$,
hence elements of $S$ by construction. A label-informed, per-item existence proof
therefore non-vacuously constrains the loop's search space — the room is non-empty
*as judged by an oracle*, which is real (if weak) motivation. What does not survive
is any reading in which (e) establishes mechanism identity, a global direction, or
label-free findability. The required (e) license (M1) is: *"for rescued items, $S$
contains an item-specific direction, constructible with label information, that
rescues at the decision endpoint; the loop's per-instance search-within-$S$ problem
is non-vacuous in this oracle sense; mechanism (relational vs. logit-steering)
unidentified; label-free findability not established (EXP070-contingent,
EXP068's own question)."*

## Recommended next step

Corrections integrator applies M1–M3 + m1–m3 (m4 is verification-only), then a
focused diff verification before signing. No new conditions, no threshold changes,
no execution — all fixes are wording/license/reporting.

---

*Reviewer sign-off: pending — M1–M3 + m1–m3 applied and diff-verified.*
*Draft spec untouched. No primary artifacts touched. No results invented.*

---

## Final Verification — 2026-09-23: VERDICT: **SIGN**

**Verifier:** Adversarial Reviewer (Law #14, focused diff verification per the review's
own recommendation). Corrections applied by the Corrections Integrator (LOG-092).
Verified by full spec read + targeted grep, not on trust.

- **[M1] Branch (e)'s license is the weakened form.** LICENSES now reads: label-informed
  per-item existence proof; loop's per-instance search-within-$S$ non-vacuous in the
  oracle sense ($\mathcal{G}_1$ candidates are aggregates of the same $\hat{v}_k$, hence
  $\in S$ by construction); mechanism (relational vs. logit-steering) unidentified —
  "the energy gate guards null-interpretability only (§3.4)"; label-free findability not
  established, with the EXP070 contingency living **in the LICENSES text itself**
  (contingent on EXP070's ceiling verdict and EXP068's own $\rho$-gate), not only §9.
  DOES-NOT-LICENSE contains all three required exclusions, including "a single global
  rescuing direction in $S$" and "that a label-free search can find such directions."
  §3.4 carries the mechanism disclaimer verbatim as required: null-interpretability only;
  10× scale amplification at the $e = 0.10$ floor; Finding-4 KL numbers (0.028 vs
  ~0.0002); "a C4 rescue can fire for the wrong reason." **Zero stale remnants:**
  grep-verified — the unqualified "treasure" metaphor has 0 occurrences (the single
  occurrence is the qualified "(the treasure was found *with a map*)" in §1.1, the form
  this review prescribed); the singular-direction license has 0 operative occurrences
  ("global" appears only in the three per-item-existential disclaimers: H_sub text,
  §7.0 criterion, (e) DOES-NOT-LICENSE). **No new control arm added** — 7 conditions
  C1–C7 unchanged, thresholds unchanged.
- **[M2] Per-item existential throughout.** H_sub (§1): "for each rescued item, $S$
  contains an item-specific direction that yields the rescue — not a single global
  direction in $S$." §7.0 canonical criterion: identical per-item form. The boxed §1
  research *question* ("contain a causally efficacious direction") is the question, not
  the licensed reading, and is immediately followed by the per-item operationalization;
  non-blocking, noted for the record.
- **[M3] Branch (d) comparability rider.** (d)'s ruling requires reporting the historical
  EXP065/066 baseline accuracy alongside this run's baseline, with the pre-registered
  rider: if baselines differ substantially, the "boundary revision" reading is qualified
  accordingly — "the numbers, not the adjective, carry the claim."
- **[m1]** §3.1 states the structural entity-domain separation (person names vs
  planets/elements, verified in the EXP066 script) and makes the test-path assertion
  concrete: a path whitelist of support artifact directories; any out-of-whitelist open
  raises a runtime assertion and aborts before any vector is constructed.
- **[m2]** 0.10 gate anchored at chance $\mathbb{E}[e] \approx 0.07$ (5/1024) with the
  [ARBITRARY] tag kept; branch (a) halt reworded — "uninformative causal test,
  informative localization measurement"; low $e$ reported as evidentially non-empty.
- **[m3]** Multiplicity disclosure present: no family-wise correction; pre-registered
  precedence (a)→(b)→(c)→(d)→(e)→(f)→(g), (h)/(i) conditional, is the operative control;
  licensed claims are motivation-grade, not confirmatory-efficacy.
- **[Surgical-diff]** Changes map exactly to M1–M3/m1–m3 (H_sub, §1.1, §3.1, §3.4, §7.0,
  branches (a)/(d)/(e), multiplicity note). N1 framing (§1.1) intact; budget (420 passes),
  conditions, gates, thresholds untouched.

**VERDICT: SIGN.** The EXP075 pre-registration
(`experiments/protocols/EXP075_SUBSPACE_BRIDGE_PREREG_SPEC.md`) is hereby the **SIGNED
pre-registration** — execution-ready, strictly confirmatory. No mechanism, subspace-
construction, or threshold changes after the energy gate without a new pre-registration.

*Reviewer sign-off: SIGNED — Adversarial Reviewer, 2026-09-23. Draft untouched by
reviewer; no primary artifacts modified; no results invented.*
