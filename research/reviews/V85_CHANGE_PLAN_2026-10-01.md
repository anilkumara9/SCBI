# v84 → v85 Change Plan — Frontier-Sweep Related-Work Addition (2026-10-01)

**Lane:** LOG-4871 (pre-assigned). **Status: DRAFT — licenses nothing.**
**Applies to:** v84 release candidate (`~/workspace/scbi-paper/v84/`, main edition) and
`~/workspace/scbi-paper/v84-ieee/` (IEEE edition). **v82 and v83 stay frozen.**
**Trigger:** LOG-4870 daily frontier sweep (`reports/research_log.md`).

**Scope (hard boundary):** related-work *sentences only*. No figure changes, no claim
changes, no result changes, no rewording of any signed result (C1–C6), no new numbered
claims. Bibliography: one new entry, sweep-verified (LOG-4870) and abstract-re-verified
by this lane (2026-10-01, arXiv abs page); no other field invented. **F1: the entry
goes into BOTH `v84/refs.bib` AND `v84-ieee/refs.bib` — the IEEE edition's clause
cites `\cite{varshney2026cosine}`, so a single entry would leave the IEEE build
with an undefined citation.**

One item is admitted. The sweep's second item ("Less Sycophancy, Stronger Refusal?",
arXiv:2609.35544v1) is **not** admitted to this plan: the sweep marked it tangential
("one line in related work at most") and the CEO's brief licensed only the Varshney
item for this lane. The plan records why the admitted item earns its place.

---

## 1. Admitted item — Varshney, "Cosine Similarity Is Not Evidence" (quantization-transfer noise floor)

**Citation (sweep-verified LOG-4870; abstract-re-verified by this lane 2026-10-01 via
the arXiv abs page, https://arxiv.org/abs/2609.30275v1):** Pranav Varshney (University
of Michigan), "Cosine Similarity Is Not Evidence: Measuring the Noise Floor of
Interpretability Transfer Under Quantization," arXiv:2609.30275v1 (announced
2026-09-29). Core abstract-verified claims: interpretability artifacts are calibrated
on full-precision weights, deployed on quantized ones, and certified as surviving the
change by scale-invariant statistics (cosine similarity, correlation, AUROC) reported
without the estimator's noise floor. For the difference-in-means direction estimator
the split-half floor is governed by κ = nρ²/d with E[cos] ≈ (1 + 4/κ)⁻¹; measured
ρ = 33–61 on Qwen2.5-1.5B-Instruct, so two independent estimator runs agree to
0.978–0.994 by sampling alone — a published 0.996 cosine between full-precision and
quantized directions is unevaluable without the n it was computed at. Against the
split-half null measured *within the quantized model*: the INT4 direction rotated
beyond estimator noise; the INT8 null result is explicitly *not* an equivalence claim.
A scale-invariant statistic cannot distinguish translation from attenuation of a
transferred decision variable.

**Why admitted:** it is the external methodology audit that EXP138's design
preempted. EXP138 (binding CERTIFIED, LOG-4865) certified the TGA injection nulls
under weight-only INT8 fake-quantization through six *behavioral* tiers — decision
flips, the ĉ VJP gate, McNemar — and never through a cosine-similarity
preservation claim. Varshney supplies the independent argument for exactly that
discipline: without the estimator's noise floor, a cosine is not evidence, and an
INT8 "no movement" null is not an equivalence claim. The admission is *methodology
convergence*, not result corroboration: Varshney validates the program's
"no cosine-as-evidence" discipline; it threatens nothing, corroborates no boundary
number, and changes no verdict.

**Placement note:** v84's main text contains zero quantization/precision discussion
(verified: no "quantiz" hit in `v84/paper.tex`), so the citation belongs in the
methodology discussion, not in a results section. The natural home is the
"measurement traps" paragraph in Related work — the trap theme is exactly what
Varshney audits. The proposed text deliberately names no experiment numbers and
asserts no new results: it cites the paper as validation of a discipline the paper
already embodies ("only McNemar decision flips count as causal evidence").

**Insertion point — main edition** (`v84/paper.tex`, line 188,
`\paragraph{Two measurement traps we close.}`): insert a *new* paragraph immediately
after that paragraph (the existing paragraph's "Two" stays accurate — it still
describes two traps). Proposed text:

> \paragraph{A quantization trap our discipline closes.}  Varshney \citep{varshney2026cosine}
> audits a practice this paper's discipline already refuses: certifying
> interpretability artifacts as surviving quantization by scale-invariant statistics
> (cosine similarity, correlation, AUROC) reported without the estimator's noise
> floor.  For the difference-in-means direction estimator, two independent runs
> already agree to $0.978$--$0.994$ by sampling alone on Qwen2.5-1.5B-Instruct, so a
> published cosine of $0.996$ between full-precision and quantized refusal directions is
> unevaluable without the $n$ it was computed at; against the split-half null measured
> within the quantized model, the INT4 direction rotated beyond estimator noise, while
> the INT8 null result is explicitly not an equivalence claim.  Our transfer claims
> rest on decision flips, never on cosine; we cite Varshney as convergent validation
> of that discipline, not as corroboration of any boundary number.

**Insertion point — IEEE edition** (`v84-ieee/sections/sec-intro.tex`, line 42,
`\paragraph{Two measurement traps we close}`): the traps are one flowing paragraph
ending "...margin shifts are reported, never counted." Append a third trap clause:

> Third, interpretability-transfer claims under quantization certified by
> scale-invariant statistics without the estimator's noise floor are unevaluable
> \cite{varshney2026cosine}: the split-half null alone agrees to $0.978$--$0.994$
> by sampling, and an INT8 null result is not an equivalence claim — our
> decision-flip discipline converges with this audit.

**Bibliography** (added to **both** `v84/refs.bib` **and** `v84-ieee/refs.bib` **
(F1 — the IEEE clause cites `\cite{varshney2026cosine}`, so one entry would leave
the IEEE build with an undefined citation); follows the `@misc` arXiv pattern of
`nadaf2026`/`jia2026`):

```bibtex
@misc{varshney2026cosine,
  author = {Varshney, Pranav},
  title = {Cosine Similarity Is Not Evidence: Measuring the Noise Floor of Interpretability Transfer Under Quantization},
  year = {2026},
  eprint = {2609.30275},
  archivePrefix = {arXiv}
}
```

---

## 2. Fencing (what this plan does NOT do)

1. No claim changes: C1–C6, the capability headline ("zero positive autonomous-steering
   signals"), and all signed numbers are untouched.
2. No result changes: EXP138's CERTIFIED verdict is not introduced into the paper —
   the proposed text cites Varshney as methodology validation only, and deliberately
   avoids naming EXP110/EXP138 or any new experiment numbers (the v84 text has no
   precision-certification discussion to attach them to).
3. No figure changes; no new numbered claims; the boxed "THREE BETS, ONE HORIZON"
   summary is untouched.
4. The citation is not presented as corroboration of any boundary number — the
   "Converging evidence" paragraph's closing fence ("None threatens the boundary
   claim") is not modified.
5. Novelty stays N1 — no new mechanism is claimed.

---

## 4. Implementation checklist (post-review, F1)

1. Add the `@misc{varshney2026cosine}` entry to **`v84/refs.bib`**.
2. Add the same entry to **`v84-ieee/refs.bib`** (required — the IEEE clause cites
   `\cite{varshney2026cosine}`; a single entry leaves the IEEE build with an
   undefined citation).
3. Insert the main-edition paragraph into `v84/paper.tex` after the
   `\paragraph{Two measurement traps we close.}` paragraph (line 188).
4. Append the IEEE clause to `v84-ieee/sections/sec-intro.tex` after
   "...margin shifts are reported, never counted." (line 42 paragraph).
5. Rebuild **both** editions and confirm zero undefined citations/warnings on
   `varshney2026cosine`.

No experiment numbers, no signed results, and no v82/v83 files are touched at any
step.

---

## 5. Uncertainties (for the independent Law #14 reviewer)

1. **Abstract-only verification.** This lane verified the citation against the arXiv
   abstract page (2026-10-01), not the full paper body. Every claim in the proposed
   text is abstract-verified; body-level details (e.g., the exact INT4/INT8
   experimental protocol) were not checked. If the reviewer requires body-level
   verification, that is a gap in this plan, not a defect in the citation.
2. **Restraint vs. grounding.** The proposed text deliberately avoids naming
   EXP110/EXP138 because v84 has no precision-certification discussion. The reviewer
   should judge whether this restraint is correct, or whether citing a methodology
   audit without naming the program's own precision-certification work leaves the
   paragraph ungrounded.
3. **Bib key** `varshney2026cosine` follows the short-key pattern (`nadaf2026`,
   `jia2026`); the reviewer may prefer a different key.
