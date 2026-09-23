# Law #14 Adversarial Review — C-A Pre-Registration Draft (LOG-150)

**Date:** 2026-09-23 · **Dispatch:** LOG-161 · **Reviewer role:** Law #14 Adversarial Reviewer
**Authority:** same review line as LOG-144 (REVISE verdict with nine binding (c) items).
**Target:** `experiments/protocols/C-A_DONOR_TRANSFER_PREREG_SPEC.md` (LOG-150 draft, DRAFT status)
**Mandate:** SIGN iff all nine (c) items are present and pinned; REJECT (enumerating the missing) otherwise.
**Mode:** analysis only; no GPU, no experiments, no signed artifacts touched. No research-log entry written (LOG-161 covers this dispatch).

## VERDICT: **SIGN-WITH-CONDITION**

All nine (c) items are **present and pinned** in the draft (§1). The draft is structurally complete —
the drafter's "all nine present" report is **confirmed, not trusted**. But the LOG-144 §(c) SIGN
criterion and the draft's own §12 require the LOG-160 weight-only pre-audit values to be **computed
and attached** before signature. `experiments/protocols/C-A_PREAUDIT_2026-09-23.md` does **not
exist yet** (verified by `ls` — file absent). Per the dispatch's SIGN CONDITION, this is
SIGN-WITH-CONDITION, not full SIGN: the exact attachment requirements are enumerated in §7. If the
audit reports DO-NOT-RUN, the verdict becomes REVISE with the redesign requirement (new number,
Law #4), never a patch.

---

## 1. The nine (c) items: verified present AND pinned

| # | Item | Draft location | Pin check | Verdict |
|---|---|---|---|---|
| (c).1 | [DONORS] Exact 20-donor list, relation template, premise-disjointness proof, $(t_d,f_d)$ histogram, Law #7 statement | §3.1–3.3 | 20 table rows (verified by count); ids `ca_C3_donor_{vk}_triple_{i}`; "outranks" template pinned; §3.2 disjointness [PROPOSITION] + build assert (FATAL on violation); histogram over 25-entity support pool with per-vocab $n_t-n_f$ identity (see §2 ruling); §3.3 Law #7 statement explicit | **PASS** |
| (c).2 | [CENTROID] Pinned formula, degeneracy floor, weight-only audit, stratum feasibility gate | §4.1–4.4 | Sum-of-differences-then-normalize pinned; per-donor-normalize-then-average explicitly REJECTED; $g(D)=\\|\sum(W_U[t_d]-W_U[f_d])\\|/\sqrt{\|D\|}$; floor **0.25**; below floor → redesign, never run; §4.3 permutation null (200 banks, `SEED_PERMNULL=20261123`); §4.4 low stratum non-empty **AND ≥5 C1-wrong headroom items**, else DO-NOT-RUN as transfer test | **PASS** |
| (c).3 | [C4′] Similarity-matched different-relation arm, matching algorithm, $\delta$, achieved-match report, demotion fallback | §5.1 | Greedy algorithm fully pinned (discrepancy $D(B)$ formula exact, tie-break lowest candidate index, 30-donor cap); **$\delta=0.05$**; achieved-match report pre-GPU; fallback: $\min D>\delta$ → contrast demoted to exploratory, stratum becomes primary, T3 exploratory-not-deciding, "no post-hoc promotion" stated twice (§5.1, §8(d)) | **PASS** |
| (c).4 | [C5] Permuted-label (prior-preserving, relation-destroying) control | §5.2 | `numpy.random.default_rng(SEED_C5_PERM=20261067)`; deterministic fixed-point re-draw rule (`seed+1`); multiset-preservation [PROPOSITION]; sketch's "random-target donor" explicitly REJECTED in §5 | **PASS** |
| (c).5 | [STRATA] Split rule frozen pre-forward-pass; within-stratum McNemar | §6 | Median split on $s_t^{C3}(j)$ over 60 items, Stage 0 weights-only; ties → low; ~30/30; "no tertiles, no post-hoc re-cutting (Law #9)"; decision endpoint = within-stratum McNemar exact C3-vs-C1; T4: $p<0.05$, $\Delta M>0$ | **PASS** |
| (c).6 | [MODEL] Item-level model, link, significance on relation-match | §7 | 120 rows (arms C3, C4′); $\mathrm{logit}\,P(\mathrm{rescue})= \beta_0+\beta_1\mathrm{relmatch}+\beta_2 s_t^{(a)}+\beta_3 s_f^{(a)}$; arm-specific $(s_t,s_f)$; `statsmodels` logistic; item-clustered sandwich SEs (60 clusters); two-sided Wald; T6: $\beta_1>0$ **and** $p<0.05$ with $(s_t,s_f)$ covaried | **PASS** |
| (c).7 | [DECISION TREE] All outcomes, permitted verdicts only, T1–T6 conjunctive, verbatim anti-creep sentence | §8 | Outcomes (a)–(f): Supported / Not supported (kill, family-scoped) / Not supported-or-Refuted (leakage) / Underdetermined / Inconclusive / DO-NOT-RUN — all from the LOG-148 permitted set; "Partial transfer" explicitly not a verdict; T1–T6 conjunctive for (a); anti-creep sentence **byte-verbatim** on one line in LICENSES (verified against LOG-144 §b.6.16, §4 below) | **PASS** |
| (c).8 | [ENDPOINTS] McNemar exact only; C2-headroom gate; Level-1 cap | §9 | "McNemar exact only... No margins, no Wilcoxon, no KL, no cosine-deltas as decision endpoints — anywhere (Law #9)"; KL = exploratory guardrail only (mean KL < 0.50, EXP077 precedent); C2-headroom gate; Level-1 cap; all Level 2/3 mentions are prohibitive (verified by grep — §5 below) | **PASS** |
| (c).9 | [HYGIENE] Budget, seeds/$\alpha$/$l^*$/hook, SHA-256, EXP058+EXP078(a) distinguished, N1, no balancing | §10 | **360-pass budget** recomputed from first principles (§3 below); `SEED_TORCH=SEED_NUMPY=20260923`, `SEED_C5_PERM=20261067`, `SEED_C6=20260989`, `SEED_PERMNULL=20261123`; $\alpha=0.50$, $l^*=20$, hook pinned; SHA-256 `get_hash` pre/post (Law #6/#13); EXP058 + EXP078(a) cited-and-distinguished; **N1 retained**; bank balancing explicitly prohibited (§10, §3.1, §4.2) | **PASS** |

**Nine of nine present and pinned. Zero items vague or unpinned. Nothing to enumerate for REJECT.**

---

## 2. Reviewer ruling: the histogram reading (review order #2)

**Ruling: the drafter's reading is CORRECT, and it is sanctioned as the faithful operationalization
of (c).1. It does not violate §(c).1; it is the only reading under which §(c).1 is non-degenerate.**

The chain of reasoning:

1. LOG-144 §b.1.2 required the $(t_d,f_d)$ histogram **"over the 10-entity pool"** — but that
   phrasing was written under the assumption visible in LOG-144's own §"one challenge" (donors
   "drawn from the same item distribution" as tests, hence sharing the 10-token answer pool).
2. The final design, following the sketch's own "entity-disjoint" mandate and LOG-144 §b.1.1
   ("no shared premise triples"), uses **name-entity donors from the 25-entity support pool** —
   literally zero tokens shared with the 10-token answer pool *by construction*. This eliminates
   L1 (target-identity leakage) entirely and is the stricter design.
3. A histogram of the donor $(t_d,f_d)$ pairs "over the 10-entity pool" would therefore be
   **identically zero** — pure box-ticking with zero audit value.
4. The *purpose* of the histogram requirement is stated in LOG-144 §b.1.2 itself: **"L4 made
   auditable"** — i.e., to expose the bank token-prior $(n_t-n_f)$ that drives the bypass model.
   That object lives over the **25-entity support pool** (the donors' actual answer-token support),
   which the draft reports in full: per-vocab $n_t-n_f$ identity ($e_0$:+2, $e_1$:+1, $e_2$:0,
   $e_3$:−1, $e_4$:−2; verified internally consistent against the V1 donor rows), the deliberate
   skew disclosed, balancing prohibited.
5. The draft separately states the structural 10-token answer-pool overlap as **[FACT]** (§1) and
   documents that literal token-identity overlap is zero *by construction* while L2/L3/L4 channels
   remain and are measured by $s_t, s_f$.

A reviewer who demanded the literal 10-entity-pool form would be demanding a less informative
artifact. **(c).1 PASSES with the 25-entity-pool histogram.** This ruling is final for this
pre-registration; it may not be re-litigated at bundle time.

---

## 3. Budget recomputation (review order #3)

Independent arithmetic, from the arm structure:

- Arms: C1, C2, C3, C4′, C5, C6 = **6 arms** (§5 table).
- Each arm makes decisions on the **60 test items**, one forward pass per item-arm (the decision
  rule is argmax over two single-token encodings at the final position — one pass).
- Vector construction costs **zero** forward passes: C2 bridges from $W_U$, C3/C4′/C5 centroids
  from $W_U$, C6 from a seeded RNG; C1 has no vector.
- $6 \times 60 \times 1 = \mathbf{360}$ forward passes. Stage 0 (weight-only audit, §4.3) costs 0 GPU passes.

**The 360 figure follows from the arm structure. The sprint's "2,700" does not** (2,700/(6×60) =
7.5 — no clean decomposition into passes-per-item-arm) and is correctly **superseded** (§10).
The ~25 s estimate on 2×T4 is labeled [ESTIMATE] and is not load-bearing. **Budget item confirmed.**

---

## 4. Conjunctive license + anti-creep sentence (review order #4)

- **One line, verbatim:** LICENSES contains (line 361) —
  > "A C3 win that fails any of T3–T6 is not transfer; it is similarity/prior steering consistent with audit Finding 4."
  Byte-identical to the LOG-144 §b.6.16 required sentence (verified by diff of the quoted text).
- **No license-side softening vs §b.5:** the draft's outcome (a) license reads "Supported — transfer
  license, capped at evidentiary Level 1: 'a same-relation donor-centroid bridge can improve
  inference on headroom items via relation-mediated steering at pythia-410m/$l^*$=20/$\alpha$=0.50
  on this benchmark.'" The scope qualifiers (model / $l^*$ / $\alpha$ / benchmark) make it
  *stricter* than §b.5's form, not softer. The sketch's one-sided kill is replaced by the
  conjunctive license with equal force on both sides, as required. Outcome (b)'s kill is
  family-scoped exactly as §b.5 demands ("ONLY for unembedding-difference donor bridges at
  $l^*$=20 on this benchmark"), and outcome (c)'s leakage→Refuted conditions match §d's
  falsification battery verbatim (C5 ≈ C3; rescue fully accounted for by $s_t-s_f$ with
  $\beta_1$ null).

---

## 5. Level-1 cap and verdict vocabulary (review order #5)

- **Level 2/3 language:** every occurrence of "Level 2"/"Level 3" in the spec is prohibitive
  ("It cannot reach Level 2... or Level 3"; "No Level 2/3 language appears anywhere"; "No Level 2
  ... or Level 3 ... language (P1)"). Verified by grep: **zero affirmative** Level 2/3 claims.
- **Verdict vocabulary:** only Supported / Not supported / Inconclusive / Underdetermined / Refuted
  are used as verdicts (all double-bolded at decision points). The two out-of-set strings found —
  `"Partial transfer" is not a verdict` (the prohibition itself) and `TRANSFER_WEAK_OR_SPECIFIC`
  (a quoted historical EXP058 verdict, not a verdict of this design) — are correct usages.
- Double-labeling (FACT/DEFINITION/HYPOTHESIS/PROPOSITION/INFERENCE/ASSUMPTION/OBSERVATION/
  INTERPRETATION/CONJECTURE/ESTIMATE) is maintained throughout, per the mentorship directive.

---

## 6. C4′ demotion fallback and Law #4 (review order #6)

The fallback is **correctly pre-registered with no post-hoc promotion path**:

- Trigger: $\min D > \delta=0.05$ at the 30-donor cap → "matching has **failed**" (§5.1).
- Consequence: C3-vs-C4′ contrast demoted to exploratory; stratum analysis becomes the primary
  discrimination; T3 marked exploratory-not-deciding; outcome (d) → Underdetermined if readings
  conflict, else verdict from T1,T2,T4,T5,T6.
- "No post-hoc promotion: a failed match can never be re-argued as support for transfer" (§5.1);
  outcome (d) repeats the bar: "A failed match is never re-argued as transfer support (Law #4)."
- Law #4 is honored structurally elsewhere: redesigned donor bank = new pre-registration (§4.2);
  leakage-demonstration runs = separate pre-registration, never the capability bet (§4.4, §8(f));
  §14 change protocol.

---

## 7. The condition: what must attach before full SIGN

The draft is complete; the **SIGN is withheld only pending attachment**. Full SIGN requires ALL of:

1. **`experiments/protocols/C-A_PREAUDIT_2026-09-23.md` attached** (the LOG-160 weight-only
   computation, CPU, $0 GPU), reporting at minimum:
   - (a) $g(D)$ for the **C3 bank** against the **0.25 floor** (§4.2); and for the selected C4′
     bank and the C5 bank once constructed — floor must be met for all three (below floor →
     redesign the bank, never run);
   - (b) $s_t(j), s_f(j)$ full distributions over the 60 test items (min/median/max, histogram)
     plus the permutation null (`SEED_PERMNULL=20261123`, 200 banks) with the observed C3 bank's
     percentile (§4.3);
   - (c) the **C4′ achieved-match report**: final $|B|$, achieved $D$ (must be $\le 0.05$ or the
     §5.1 demotion fallback fires by design), selected donor ids, $g(B)$ vs the 0.25 floor, and
     per-item $|s_t^B-s_t^{C3}|$, $|s_f^B-s_f^{C3}|$ distributions;
   - (d) **stratum feasibility**: low-similarity stratum non-empty **with ≥ 5 C1-wrong headroom
     items** (§4.4/§6) — else DO-NOT-RUN as a transfer test.
2. **All nine §12 checklist boxes marked checked** in the spec.
3. **No design change** between now and signing (any change = new number per §14/Law #4).

**Consequence rule (binding):** if the audit reports DO-NOT-RUN — degeneracy below floor, or
low stratum empty/headroom-free — this verdict **converts to REVISE** with the redesign
requirement (redesigned donor bank = a new pre-registration, per §4.2/§4.4 and Law #4), per the
LOG-161 dispatch instruction. A passing audit converts this verdict to full **SIGN**.

**Banner change authorized on full SIGN:** the spec header block

> **Status: DRAFT — NOT signed, NOT pre-registered. Law #14 adversarial review (same reviewer, under LOG-144 authority) required before PRE-REGISTERED.**

is authorized to be replaced with:

> **Status: PRE-REGISTERED — signed by the Law #14 adversarial reviewer under LOG-144 authority (dispatch LOG-161), 2026-09-23. Experiment number minted at signing per LOG-149/150.**

(No edit is made by this review; the banner edit is the drafter's/CEO's action at signing, gated
on §7 items 1–3 above.)

---

## 8. Non-blocking observations (not (c) items; no action required)

- **O1.** §4.2 applies the degeneracy floor to C3, C4′, *and* C5 banks; note that C5's $g(D)$ is
  algebraically identical to C3's (multiset preservation), so C3 and C5 pass/fail together —
  harmless redundancy, recorded for the audit's convenience.
- **O2.** The evaluation order lists T1 before T2 but tags T2 "(headroom gate, first)"; outcome
  (e) makes T2's failure override any T1 reading (Inconclusive, no kill). Precedence is
  unambiguous in the decision table; no change needed.
- **O3.** C4′'s 150-item candidate pool ("is next to" × 5 vocabs × 30 triples+quads) and the
  permutation-null 150-item pool ("outranks" triples+quads × 5 vocabs) are numerically consistent
  (5 × 30 = 150 each); the builder has no discretion on pool definition.
- **O4.** If C4′ matching fails and the fallback fires, the item-level model (§7) still runs with
  arms {C3, C4′} and T6 still decides — consistent with outcome (d) ("verdict follows
  T1,T2,T4,T5,T6 with T3 marked exploratory-not-deciding").

---

## 9. Adversarial independence note

This verdict answers to the CEO alone. The drafter's self-report ("all nine present and pinned")
was **re-verified item by item against the pinned text** — it happened to be accurate; the one
structural surprise (the histogram reading) was ruled in the drafter's favor on substantive
grounds (§2), because demanding the literal form would have produced a less informative artifact.
The SIGN is nevertheless withheld pending the audit attachment: a pre-registration that can be
signed before its own pre-registered gates are computed is not a pre-registration. No instruction
to soften this verdict was received; none would have been honored.

*End of LOG-161 review. Report: `reports/adversarial_review_c-a_prereg_2026-09-23.md`.*

---

# LOG-176 — Conversion Ruling on the C-A Pre-Registration Draft (Law #14 Adversarial Reviewer, LOG-144 review line)

**Date:** 2026-09-23 · **Dispatch:** LOG-176 · **Reviewer role:** Law #14 Adversarial Reviewer
**Authority:** LOG-144 review line (same line as LOG-161 SIGN-WITH-CONDITION).
**Target:** `experiments/protocols/C-A_DONOR_TRANSFER_PREREG_SPEC.md` (DRAFT, LOG-150) with the
complete weight-only pre-audit attached: `experiments/protocols/C-A_PREAUDIT_2026-09-23.md`
Part 1 (LOG-160) + Part 2 §§8–13 (LOG-174) and the JSON twin.
**Mode:** analysis only; no GPU; no signed artifacts touched. No research-log entry (LOG-176 covers this dispatch).

## VERDICT: **REVISE** (blocking)

The LOG-161 condition's attachments are complete — every §12 item now has its computed values
(§1 below). But the audit, which the condition required, surfaced a **design-level falsity** the
condition did not anticipate: the C5 control is **geometrically identical to C3 by construction**
under the pinned §4.1 identity, which makes §5.2's pinned [PROPOSITION] false, T1/T5 mutually
exclusive, outcome (a) logically unreachable, and the §8 C5 refutation clause a tautology that
fires by construction. A pre-registration whose capability-license branch is unreachable and
whose refutation evidence is a tautology cannot be signed. The defect is in the licensed decision
tree itself — not a minor attachment — so this is REVISE, not SIGN-WITH-FIXES. No banner advance;
no experiment number minted. The failed draft consumes no number.

**On the LOG-161 conversion rule.** LOG-161 §7 stated "a passing audit converts this verdict to
full SIGN." That rule was premised on the audit being a mechanical attachment of gate values.
The audit instead **falsified a pinned design proposition**. The conversion rule is overridden:
signing a design known to contain a false pinned proposition and an unreachable license branch
would violate Law #14's challenge duty and Law #2's honesty duty. The mechanical gates all pass;
the design does not.

## 1. Independent verification of the load-bearing facts (none trusted)

Recomputed/read from the JSON twin and markdown, not from the task's summary:

- **Degeneracy:** g(C3)=1.0617830595495654, g(C4′)=0.8609809349756752, g(C5)=1.0617830595495654
  (= C3's to all reported digits) — all ≥ 0.25 floor. **PASS ×3** [FACT — verified].
- **C4′ selection:** n_selected=1, D=0.04656406188177837 ≤ δ=0.05 → STOP-D≤δ branch fired;
  demotion fallback did NOT fire. Selected: `ca_C4cand_V5_Modern_triple_1` (Noah−Maya, "is next to"
  triple). singletons_with_D_le_delta=7; tie-break = lowest candidate index (deterministic, no RNG);
  a duplicate-content twin of the winner exists in the pool. **As reported** [FACT — verified].
- **C5 construction:** seed_final=20261069 (2 fixed-point redraws from 20261067/20261068, pinned
  rule); multiset_preserved=True; prior (n_t−n_f) identical to C3's for all 25 support entities;
  cos(b̂_C5,b̂_C3)=0.9999999999999998 (≈1 to float precision; markdown rounds to 1.000000000000000).
  **Identity confirmed** [FACT — verified].
- **C3 stratum:** low=49 / high=11; low headroom=23 (≥5). **PASS** [FACT — verified].
- **C4′ stratum analog:** low=35 / high=25; low headroom=16 (≥5). **PASS as analog** [FACT — verified].
- **s_t coarseness:** 6 distinct values (one per target entity) under both centroids — the median
  split is necessarily an entity-group split. **Confirmed** [FACT — verified].
- **EXP081:** verified unminted — the only repository mentions are "next free: EXP081" (research log,
  post-LOG-172 G2 signing); no `exp081` run directory; no protocol references. Next free at any
  future signing must be re-verified at that time.

**Review-line self-correction:** LOG-161 O1 noted that g(C5) is algebraically identical to g(C3)'s
but did not catch that the *vectors* are identical. The identity was derivable from the pinned
text at LOG-161 time (§4.1 identity + §5.2 multiset preservation). The review line missed it;
the audit caught it. Recorded, not hidden.

## 2. Ruling on Flag 1 — C5 ≡ C3: STRUCTURALLY VACUOUS → REVISE (blocking)

**(a) Identity verification — CONFIRMED, by the spec's own pinned text.** §4.1 pins
b̂_D = normalize(Σ_d (W_U[t_d] − W_U[f_d])) = normalize(Σ_y W_U[y]·(n_t(y) − n_f(y))).
§5.2 pins C5's donor pairs as (t_{π(i)}, f_i) with the target multiset and foil multiset preserved
exactly. Summing: Σ_i W_U[t_{π(i)}] = Σ_i W_U[t_i] (permutation reorders terms) and
Σ_i W_U[f_i] is unchanged — so the unnormalized sums are identical, hence b̂_C5 ≡ b̂_C3 exactly.
The JSON's cos=0.9999999999999998 and the markdown's ‖S_C5−S_C3‖=0.000e+00 are the numerical
shadow of this algebraic identity [THEOREM — from pinned definitions; FACT — computed].

**(b) The ruling: the C5 arm is structurally vacuous, and the conjunctive license does NOT absorb it.
The genuine-test reading of T5's intent is the correct one — and it is the one that fails.**

Two readings were on the table:

- *Reading A (genuine mutual-exclusion test):* T5 was meant to discriminate — C5 geometrically
  distinct but prior-matched, so C5-rescuing ⟺ prior/similarity steering and C5-silent-while-C3-rescues
  ⟹ relation-mediated structure. This is what the pinned text says: §5.2's [PROPOSITION] claims
  "C5's centroid **differs** from C3's only in which target tokens are paired with which donor
  premises" and that "any C3-vs-C5 rescue gap is attributable to per-donor relational content."
- *Reading B (intended to fire):* the §8 clause was designed to fire exactly here, making T5 a
  genuine mutual-exclusion test by construction.

**Reading A is the correct reading of the spec's intent** — it is the only reading consistent with
the pinned §5.2 [PROPOSITION], which asserts a geometric difference that does not exist. Reading B
is contradicted by that same proposition: had the drafter intended identity, the spec would state
"C5 ≡ C3 by the §4.1 identity; T5 vacuous by construction." It states the opposite. The drafter
believed the permuted pairing would move the centroid; under sum-of-differences-then-normalize it
cannot, because donor premises never enter b̂_D (unembedding-space construction — the "relational
content" was never in the vector to begin with; this is the spec's own §4.1 confound proposition).

**Consequences (all by construction, not by data):**

1. **T1 and T5 are mutually exclusive.** Identical vectors → identical per-item decisions →
   identical discordant pairs → (ΔM_C5, p_C5) = (ΔM_C3, p_C3) exactly. T1∧T5 demands the same
   McNemar test yield p<0.05 and p≥0.05 — impossible.
2. **Outcome (a) "Supported — transfer license" is logically unreachable.** It requires T1–T6
   conjunctively, hence T1∧T5. A confirmatory pre-registration whose positive-license branch cannot
   fire is a broken instrument — and note the symmetry with what LOG-144 struck down: the sketch's
   one-sided kill (null kills, win auto-licenses) was replaced by the conjunctive license precisely
   to avoid one-sidedness. As pinned, the design is a **kill-only machine** — the same sin reversed.
3. **The §8 refutation clause fires by construction whenever T1 fires.** Paired C3-vs-C5 compares
   an arm with itself: b=c=0, p=1.0 (harness rule, spec §8) ≥ 0.05 — so "paired C3-vs-C5 p≥0.05 with
   C3 vs C1 significant → Refuted" is a tautology dressed as an exact test. Reporting b=c=0, p=1.0
   from identical arms as discriminating refutation evidence misrepresents the evidence's information
   content (zero) — a Law #2/Law #11 violation in the verdict machinery itself.
4. **§12 item 4 [C5] is not substantively satisfied.** The construction and seed are pinned, but the
   required "prior-preservation argument" — "any C3-vs-C5 rescue gap is attributable to per-donor
   relational content, and C5 ≈ C3 shows the rescue is prior/similarity steering" — is **false as
   pinned**. C5 ≡ C3 cannot "show" anything about the rescue; it is the same observation counted twice.
5. **§13's "one idea" (permuted-bank null family) is likewise vacuous.** Under the §4.1 identity,
   every prior-preserving permuted bank has the identical centroid → identical ΔM → the permutation
   null is a point mass at C3's own ΔM. The "exact permutation test on ΔM" has zero variance by
   construction. The idea is dead as written.

**The deeper point for the redesign:** in the sum-of-differences unembedding family, the "prior
channel" and the intervention vector are the same object — any bank with the same (n_t−n_f) has the
same centroid. There may be **no** label-informed, prior-preserving, relation-destroying,
geometrically-distinct control in this family. The discrimination battery must rest on T3 (C4′),
T4 (stratum), T6 (model) — or the centroid construction must change (which changes the whole design).

## 3. Ruling on Flag 2 — singleton C4′ bank: LICENSED AS WRITTEN; NOT VACUOUS; NOT a §12-box failure

The pinned greedy rule (§5.1) specifies the stop condition (D ≤ δ), the cap (30), and the tie-break
(lowest index) — and **pins no minimum bank size**. The audit applied it verbatim. D=0.046564 ≤ 0.05
met the tolerance; g(B)=0.860981 passes the floor; the STOP-D≤δ branch fired, so the demotion
fallback correctly did not fire.

- **Does it operationalize T3's intended discrimination? Yes.** The C4′ vector (Noah−Maya
  "is next to" direction) is geometrically distinct from C3's; the achieved profile match is within
  the pre-registered δ envelope (per-item deviations: |s_t|-median 0.0267, max 0.0435; |s_f|-median
  0.0220, max 0.0694). The paired C3-vs-C4′ McNemar can come out either way — unlike C5, this test
  carries information. T3 is not vacuous or degenerate in the logical sense.
- **Is it a §12-box failure? No.** Item 3 requires the achieved-match report attached with
  D ≤ δ or the fallback fired — the report is attached, D ≤ δ holds, the fallback correctly stayed
  unfired. The box is satisfied.
- **Recorded fragility (for the redesign, not a REVISE trigger by itself):** D=0.046564 sits
  within 7% of the δ boundary; 7 singletons already met δ and the lowest-index tie-break selected
  among them (a duplicate-content twin of the winner exists in the pool). The T3 outcome is hostage
  to a near-boundary tie-break among near-identical singletons. The redesign should pin either a
  minimum bank size or a tie-break-robustness rule (e.g., report the T3-relevant spread across tied
  winners as a sensitivity analysis — descriptive, not deciding).

## 4. Ruling on Flag 3 — the 49/11 and 35/25 entity-group splits: ACCEPTABLE AS PINNED; NO RE-REGISTRATION

Spec §6 pins the **rule** — median split on s_t^{C3}(j), ties → low, computed Stage 0 from weights
alone. The "~30/30" is an aside (an expectation under a continuous-feature assumption), not a pin.
The audit applied the pinned rule verbatim; the 49/11 outcome follows necessarily from s_t taking 6
distinct values with the median equal to Iron's s_t (21 tied items). The T4 inference language
("leakage predicts rescue concentrates in the high stratum; transfer predicts rescue in the low
stratum") is stratum-level throughout — **the spec never promises a per-item gradient**, so no
promise is broken.

- **No re-registration required.** The split is the pinned rule's output, not a post-hoc re-cut
  (Law #9 is satisfied — the rule was frozen before any forward pass).
- **Binding interpretive caveat (carries into any signed version):** T4 tests rescue on
  low-similarity **target entities** with exactly **3 independent entity-level observations**
  ({Mars, Venus, Iron} for C3; {Venus, Iron, Gold} for the C4′ analog) — not a 49-observation
  per-item gradient. A T4 license can at most mean transfer across 3 low-similarity target entities.
  This limitation (LOG-174 §12) must appear in the T4 license language, not just in an audit appendix.
- The feasibility gate (§4.4, binding, pinned to the C3 stratum) passes with margin: 49 low items,
  23 headroom ≥ 5. The C4′-analog (35/25, 16 headroom) is descriptive support for the reviewer's
  T3/T4 reading only.

## 5. What REVISE requires (redesign requirements, binding on the next draft)

The redesign is a **new draft revision of the C-A pre-registration** (C-A v2), not a new experiment
line: the draft is unsigned and unnumbered, so Law #4's "changed design = next free number" binds
**at signing**, not at revision. No number is consumed by this ruling. On re-review SIGN, the number
mints from the then-next-free pool (currently EXP081 — **re-verify unminted at signing time**).

Minimum redesign requirements (the re-review will check each):

1. **Resolve C5 honestly.** Either (i) drop the C5 arm (budget recomputed: 360 → 300 passes) and
   remove T5 plus all C5-referencing §8 clauses, rewriting outcomes (a)/(c) without it; or
   (ii) replace it with a genuinely geometrically-distinct prior-controlled design — with a proof
   that the control is distinct under the pinned centroid construction. The false §5.2 [PROPOSITION]
   must be corrected or deleted; the identity theorem (any (n_t−n_f)-preserving bank ⇒ identical
   centroid) should be stated explicitly, since it is itself a publishable lemma about this
   intervention family.
2. **Decide the discrimination battery without a prior-control.** If C5 is dropped, the leakage
   discrimination rests on T3/T4/T6 alone — the theory role must affirm in the draft that this
   battery suffices, or supply the replacement control. The §13 permuted-bank idea must be dropped
   or rebuilt (it is vacuous under the §4.1 identity — §2.5 above).
3. **Carry the T4 entity-group caveat into the license language** (§4 above): a T4 license means
   transfer across 3 low-similarity target entities, at most.
4. **Harden C4′ selection** against the singleton fragility (§3): pin a minimum bank size or a
   tie-break-robustness sensitivity rule. The achieved D's 7%-of-δ margin must be disclosed in the
   T3 reading.
5. **Recompute the budget from the final arm structure** (300 if C5 is dropped) and re-pin all
   seeds; re-run the weight-only audit against the revised construction before the next review.

Non-requirements (explicitly not demanded): no change to C3's donor list, the §4.1 formula, the
degeneracy floor, the C2/C6 arms, the McNemar-only endpoint rule, or the Level-1 cap — all verified
sound at LOG-161 and unaffected by this ruling.

## 6. Adversarial independence note

This verdict overrides the LOG-161 conversion rule on substantive grounds stated in §0 — the audit
did not merely attach values, it falsified a pinned proposition. The singleton and stratum flags
were ruled in the design's favor where the pinned text supported them (§3, §4); the C5 flag was
ruled against it where the pinned text contradicted itself (§2). No instruction to soften was
received; none would have been honored. The verdict answers to the CEO.

*End of LOG-176 conversion ruling. This section appends to, and does not rewrite, the LOG-161
review above.*
