# EXP081 Mathematical License Addendum — LOG-209

**Status:** ADDENDUM to the signed protocol
`experiments/protocols/C-A_DONOR_TRANSFER_PREREG_SPEC_V2.md`
(PRE-REGISTERED, CEO-signed LOG-182, 2026-09-23, on the LOG-181 Law #14
re-review SIGN-WITH-FIXES with F1–F2 applied and verified).
**The signed protocol text is not modified by this file** (corrections
discipline; §A.6 transition rule, CEO-RATIFIED per LOG-204 ruling 3).
**Dispatch:** LOG-209 · **Date:** 2026-09-23 · **Cost:** $0, CPU, docs only.
**Author role:** Track-1 (theory) protocol specialist.

**Law #15 (on record, LOG-209):**
1. Q: the recovered license (graded) for EXP081's prior-channel design, plus
   the control story under the §H7 demotion.
2. Decision: CONTINUE — this signed addendum is a precondition for GPU
   clearance of EXP081; without it clearance cannot be sought.
3. Cheapest: $0 paperwork vs re-drafting and re-reviewing a signed protocol
   through full Law #14 cycles (weeks, zero scientific gain).
4. License: this addendum IS the Q4 instrument — its L1–L4, reviewer-verified.

---

## Mathematical License (binding — Law #15 Q4; see research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md)

**License grade:** IN-HOUSE-PROOF (promotion-ready). Per §A.3: may authorize a
pilot or scale-gated run only; full-run authorization requires promotion via
Law #14 review of the proof attacking each step per Charter M2.2.
(INTUITION is disqualifying — not cited here.)

### L1. Authorizing result
- **Statement (exact):** **[THEOREM] — the prior-channel / vector identity**
  (§4.1 of the signed spec, verbatim): *"For any two donor banks D, D′ over
  the same vocabulary, if n_t(y) − n_f(y) = n_t′(y) − n_f′(y) for every token
  y, then b̂_D ≡ b̂_D′ exactly."*
  *Proof.* Σ_{d∈D}(W_U[t_d]−W_U[f_d]) = Σ_y W_U[y]·(n_t(y)−n_f(y)) by
  regrouping terms; identical per-token coefficients give identical
  unnormalized sums, hence identical vectors after normalization. ∎
  **Corollary** (§R0.1): the three desiderata — (i) prior preserved,
  (ii) relation destroyed, (iii) geometrically distinct — are jointly
  **unsatisfiable** under sum-of-differences-then-normalize. This is the
  license for the C5 deletion (§5.2): a prior-preserving control is
  geometrically vacuous, and a bank with a different (n_t−n_f) cannot
  attribute a rescue gap to relational content.
- **Source:** in-house proof, signed spec §4.1/§R0.1. The LOG-181 Law #14
  reviewer **independently re-derived the regrouping from the pinned
  formula** (`reports/adversarial_review_c-a_prereg_v2_2026-09-23.md` §3).
  Weight-only corroboration: cos = 0.9999999999999998 (JSON-verified:
  `experiments/protocols/C-A_PREAUDIT_2026-09-23.json`
  `/part2_log174/c5_bank/cos_centroid_c5_c3`, [FACT — computed]);
  ‖S_C5−S_C3‖ = 0.000e+00 (signed spec §5.2/§R0.1 [FACT]; C5's values retained
  only as identity evidence).
  No standalone per-step M2.2 proof attack is on record — hence
  IN-HOUSE-PROOF, not PROVEN-LEMMA.
- **Epistemic label:** [THEOREM].

### L2. Quantitative prediction for the primary endpoint
- **Endpoint:** this license authorizes a *design element*, not an accuracy
  endpoint: the prior-channel analysis — i.e., the claim that no
  prior-preserving control is geometrically distinct in this family (the C5
  deletion, §5.2/§R0.1), and that the T3–T5 discrimination battery is the
  complete observable-implication set for relation-mediated steering.
- **Prediction:** any bank with the identical per-token (n_t−n_f) as C3 has a
  centroid identical to C3's — cosine to C3 = 1 up to float rounding
  (measured: **0.9999999999999998**; norm difference **0.000e+00**). A bank
  with a different (n_t−n_f) has a different prior channel and cannot
  attribute a C3-vs-bank rescue gap to relational content (v1 §5's own
  rejection logic for the naive C4). The corroboration is a [FACT —
  computed] about the pinned bank, not a prediction about GPU outcomes.
- **Derivation:** the §4.1 proof — one regrouping step; the prediction *is*
  the identity restated as a measurement (cosine and norm of the
  two constructions).

### L3. Breaking point
- **Falsifying observation (the identity itself):** a bank with the exact
  per-token (n_t−n_f) of C3 whose centroid is *not* identical to C3's
  (cosine materially < 1, norm difference materially > 0) ⇒ the regrouping
  identity is refuted and the C5-deletion proof collapses. **Decision:** KILL
  the v2 design's prior analysis; the design returns to DRAFT (any
  re-registration takes a new number, Law #4).
- **Falsifying observation (the F1 fragility rule — recovered verbatim from
  §5.1 as signed with the LOG-182 fix):** among the n_d distinct-content
  S1–S6 alternates, if fewer than ⌈5n_d/6⌉ agree with the winner's T3
  reading, the T3 license line carries the pinned caveat **"T3 reading is
  tie-break-fragile (m/n_d distinct-content alternates agree)"**.
  **Decision: CONTINUE with the caveat reported** — the battery is
  descriptive, NEVER deciding; it can never promote or demote the verdict
  (§5.1; confirmed by the LOG-181 reviewer).
  **Correction to the §A.6 sketch:** the ratified sketch's "⇒ the C-A
  transfer claim is dead" over-reads the signed rule. The signed rule kills
  no claim. The transfer claim dies **only via the §8 decision tree**:
  outcome (b) (T1 null ⇒ **Not supported**; family-level kill licensed ONLY
  for unembedding-difference donor bridges at l*=20 on this benchmark) or
  outcome (c) (any of T3–T5 fails ⇒ **Not supported**; **Refuted** under the
  pinned conditions — C4′ rescues vs C1 while T3 fails, or rescue fully
  accounted for by s_t(j)−s_f(j) with β1 null). The addendum reports the
  signed text, not the sketch — that is the transition's finding-generator
  function at work.
- **Outcome partition:** §8 proves every terminal (a)–(d) reachable; no
  tautological refutation clause survives (v1's paired C3-vs-C5 clause,
  b=c=0 by construction, was deleted with the arm).

### L4. Assumption inventory
- **A4 (§5.1):** "is next to" carries no rank-order relational content (its
  program role is the neutral contrast template, EXP078 §1). [ASSUMPTION] —
  open declared debt (M2.1). If false, the T3 contrast (C4′ as
  different-relation donor) is mislabeled. Not dischargeable inside this
  protocol.
- **L5 (§3.1):** template wording enters h, not b̂_D, so it cannot produce
  arm differences — design constant. [ASSUMPTION].
- **The bypass model (§4.1 [PROPOSITION]/INFERENCE):**
  Δℓ_j(y) ≈ α⟨W_U[y], b̂_D⟩ + attention-mediated terms (not privileged per
  the G1 [OBSERVATION]) — the H_leak frame. A model, not a proven lemma; it
  is the null the discrimination battery is built to catch, not a license.
- **Bank-set pin (§4.5):** the §4.2–4.4 audit values are computed against the
  pinned bank set {C3 20-donor list, C4′ selected singleton}; any bank-set
  change requires recomputation from weights alone before signing — a
  forward rule, recorded.
- **Promotion path:** PROVEN-LEMMA via a Law #14 review of the identity as a
  standalone lemma attacking each step per Charter M2.2 (LOG-181 re-derived
  it in the design-review context, not as a standalone proof attack);
  promotion logged in `reports/research_log.md`.

---

## §H7 control relabeling (LOG-204 ruling 1 — DEMOTE)

C2 ("per-item oracle self-bridge … positive control **and headroom gate
(T2)**", §5) is hereby relabeled **"rescue control (known-answer direction),
NOT a mechanism control"** per the LOG-204 ruling. Its positive-control
status for autonomous-mechanism questions is REVOKED. Its surviving role is
strictly T2 (headroom gate, evaluated first): it verifies the apparatus can
still rescue via known-answer injection on this run — a **procedure-validity
function, not a mechanism claim**. If T2 fails (C2 p ≥ 0.05), the procedure
is invalid → **Inconclusive** (outcome (d)), overriding (b)/(c).

**What serves as the control for EXP081's autonomous-mechanism question:**
H_transfer asks whether a **label-free-at-test-time** donor bridge transfers
relation structure (§1; §3.3 — donor labels are support-side construction
material only; the vector applied to each test item is the fixed bank-level
centroid, carrying no per-item test label). C2 was label-informed *per
item*, so it could never control that question — the demotion removes a
label it never honestly held. The controls that remain are label-free at
test time like C3 itself: **C4′** (similarity-matched, different-relation
donor — the discrimination control) and **C6** (random unit direction —
the procedure control), plus the S1–S6 sensitivity battery (descriptive).
There is **no label-free positive control for transfer in this design** —
the transfer license is earned conjunctively (T1–T5), and a clean outcome
(a) would be the program's first positive signal for it. The bank-prior
channel cannot be independently lesioned in this family (identity theorem);
this is recorded as a **known limitation of the Level-1 license** (§8
[AFFIRMATION]), not as a hole in the battery. The addendum reports; it
does not rescue.

---

## Honest-reporting note (§A.6 point 5)

Best honest grade for the recovered license: **IN-HOUSE-PROOF** — matches
the §A.6 sketch; no downgrade required, one correction issued (the L3
sketch over-read, above). Multi-license note per §A.3: H_transfer is a
[HYPOTHESIS]/[CONJECTURE] — the protocol is its falsification attempt, so
the hypothesis-side license is CONJECTURE-UNDER-TEST; the weakest
load-bearing grade authorizes the cheapest discriminating experiment only —
which this is (660 passes, ≈45s on 2×T4, free-tier trivial). Open
assumptions A4/L5 are the inventory's declared debts; the identity theorem
discharges the prior-channel design question but licenses no transfer win.

---

**Signed:** Track-1 (theory) protocol specialist · LOG-209 · 2026-09-23 ·
**Law #14 review:** SIGN-WITH-FIXES — LOG-210 (independent Track-7 adversarial reviewer, no prior involvement in §A.6 addenda or EXP080/081 protocols), 2026-09-23. Two mechanical fixes applied by the reviewer (McNemar convention phrasing; norm-difference citation). Report: `reports/adversarial_review_addenda_law14_2026-09-23.md`.
