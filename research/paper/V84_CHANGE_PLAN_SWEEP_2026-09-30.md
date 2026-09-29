# v84 Change Plan — Frontier-Sweep Related-Work Additions (2026-09-30)

**Lane:** LOG-4753 (pre-assigned). **Status: DRAFT — licenses nothing.**
**Applies to:** v84 release candidate (`~/workspace/scbi-paper/v84/`, main edition) and
`~/workspace/scbi-paper/v84-ieee/` (IEEE edition). **v82 and v83 stay frozen.**
**Trigger:** LOG-4751 daily frontier sweep (`research/benchmarks/FRONTIER_SWEEP_2026-09-30.md`).

**Scope (hard boundary):** related-work and future-work *sentences only*. No figure
changes, no claim changes, no rewording of any signed result (C1–C6, the O1/O2 polish,
the tags), no new numbered claims. The boxed "THREE BETS, ONE HORIZON" summary and the
founder's v83/v84 decisions are preserved byte-for-byte. Bibliography: two new entries,
both sweep-verified (LOG-4751); no other field invented.

Two items are admitted. Everything else in the sweep (A2–A6, B1–B2, C2, D1–D2) is
*not* admitted to this plan: A2 belongs to the retired static class (already covered by
the brittleness citations), A3–A6/B1–B2/C2/D1–D2 carry no license or verdict implication
for v84's claims. The plan records why each admitted item earns its place.

---

## 1. Admitted item 1 — "Steerable but Not Decodable" (converse dissociation)

**Citation (sweep-verified, LOG-4751):** Mohammed Suhail B. Nadaf, "Steerable but Not
Decodable: Function Vectors Operate Beyond the Logit Lens," arXiv:2604.02608 (v1 Apr
2026; v2 Aug 2026). 4,032 cross-template pairs, 12 tasks, 6 models, 3 families;
function-vector steering succeeds where the logit lens cannot decode the answer at any
layer (gaps to −0.91); only 3/72 task-model cells show decodable-without-steerable.

**Why admitted:** it is the *converse* of v84's headline dissociation
("decodes at 6.7× chance; steers zero decisions"). Together with the two existing
converging items, it decomposes the linear representation hypothesis into *linear
decodability* and *linear steerability* and shows they come apart in **both**
directions — the transfer is not a map in either direction. Independent convergent
evidence for the boundary narrative; the paper already cites arXiv:2609.06951 in the
same spirit (v84 related-work addition, LOG-4516). No verdict, license, or the
capability headline ("zero positive autonomous-steering signals") is affected: neither
paper produced a positive on SCBI's own licensed benches.

**Insertion point — main edition** (`v84/paper.tex`, line 173,
`\paragraph{Converging evidence: the gap is not ours alone.}`):
Extend the paragraph. Current last sentence: "Neither threatens the boundary claim;
both corroborate its shape from independent angles, one theoretical and one
peer-reviewed behavioral." Proposed replacement text for the whole paragraph's tail —
change "Two contemporaneous results" → "Three contemporaneous results" and append
after the Jia sentence:

> Nadaf \citep{nadaf2026} supplies the converse: across 4,032 cross-template pairs,
> 12 tasks, and 6 models, function-vector steering succeeds even where the logit lens
> cannot decode the answer at any layer (gaps to $-0.91$). The dissociation holds in
> both directions: decodability does not imply steerability, and steerability does
> not imply decodability.

The closing sentence "Neither threatens the boundary claim; both corroborate its shape
from independent angles, one theoretical and one peer-reviewed behavioral." becomes:
"None threatens the boundary claim; all three corroborate its shape from independent
angles — one theoretical, one peer-reviewed behavioral, one converse-directional."

**Insertion point — IEEE edition** (`v84-ieee/sections/sec-discussion.tex`, line 29,
`\paragraph{Novelty and position}`): append to the existing converging-evidence
sentence (after the `\cite{jia2026}` clause):

> and a converse-direction result in which function-vector steering succeeds where
> the logit lens cannot decode at any layer \cite{nadaf2026}.

---

## 2. Admitted item 2 — GEOSTEER (next-instrument watch item)

**Citation (sweep-verified, LOG-4751):** Xuan Cuong Ngo, Hao Vo, Ngan Le,
"GEOSTEER: Geodesic Optimization for Activation Steering in LLMs," arXiv:2609.10658
(submitted 9 Sep 2026). Norm-preserving steering reformulated as Riemannian
optimization: a learned nonlinear objective guides a sequence of small geodesic steps
on the representation manifold, beating SOTA one-step activation-steering baselines
on TruthfulQA, RealToxicityPrompts, and UltraFeedback.

**Why admitted:** it is the frontier's strongest case that one-step additive edits are
the *weak* form and geometry-aware multistep steering is the *strong* form. It directly
informs the active licensed lane EXP131 (one-shot v₁ injection): if EXP131 nulls,
GEOSTEER's multistep-vs-one-shot distinction is the first licensed escalation
candidate — it changes the *instrument class*, not the dose. If EXP131 returns
positive, GEOSTEER's geodesic machinery is the natural generalization path. Admitted
**as a named watch item in future work, never as a claim**: the paper asserts nothing
about GEOSTEER's results beyond what the citation states, and licenses nothing.

**Insertion point — main edition** (`v84/paper.tex`, `\section{Future work: three
bets, one horizon}`, `\label{sec:future}`): insert a new paragraph *after* the
section's opening line ("The boundary marks where the static class ends. The three
bets below say where to look next, and each dies cleanly if wrong. ...") and
*before* the bets figure. Proposed text:

> One frontier result names the instrument class the three bets do not cover.
> \citet{ngo2026} reformulate steering as Riemannian optimization: a learned
> nonlinear objective guides a sequence of small geodesic steps on the representation
> manifold, beating one-step activation-steering baselines on TruthfulQA,
> RealToxicityPrompts, and UltraFeedback. If one-shot injection at the
> dynamics-matched direction fails (the program's licensed EXP131 test), geometry-aware
> multistep steering — not a larger dose of the same push — is the first escalation
> the program's own falsification discipline would license. It is recorded here as a
> watch item, untested on our benches.

The boxed summary, figure, and all three bets are untouched.

**Insertion point — IEEE edition** (`v84-ieee/sections/sec-conclusion.tex`): the
future-work paragraph (2–3 sentences) gains one sentence. Current paragraph ends:
"The program advances only through gates, never around them. ``Superhuman'' names the
horizon, never an achievement." Proposed insertion before the final sentence:

> One named watch item: \citet{ngo2026} reformulate steering as Riemannian
> optimization — geodesic multistep updates beating one-step baselines — the
> instrument class the program would escalate to if one-shot injection fails.

---

## 3. Bibliography entries

Append to **both** `v84/refs.bib` and `v84-ieee/refs.bib` (no key collisions;
verified against both files):

```bibtex
@misc{nadaf2026,
  author = {Mohammed Suhail B. Nadaf},
  title = {Steerable but Not Decodable: Function Vectors Operate Beyond the Logit Lens},
  year = {2026},
  eprint = {2604.02608},
  archivePrefix = {arXiv}
}

@misc{ngo2026,
  author = {Xuan Cuong Ngo and Hao Vo and Ngan Le},
  title = {GEOSTEER: Geodesic Optimization for Activation Steering in LLMs},
  year = {2026},
  eprint = {2609.10658},
  archivePrefix = {arXiv}
}
```

Field provenance: all fields verbatim from the LOG-4751 sweep report (sweep-verified;
this lane did not re-hit arXiv). Keys `nadaf2026` / `ngo2026` chosen to avoid
collision with existing keys in both bib files.

---

## 4. Regression checklist (for the implementation + review lanes)

1. No new numbered claims: C1–C6 verbatim; O1/O2 polish verbatim; no new
   `\item[\textbf{C7}]`.
2. Touched pages confined to the insertion points: main `paper.tex` §related-work
   converging-evidence paragraph + §future-work new paragraph; IEEE
   `sec-discussion.tex` line-29 paragraph + `sec-conclusion.tex` future-work
   paragraph; both `refs.bib` (two appended entries).
3. Banned language absent: no "release candidate" string added to sources, no
   `+0.010/−0.004`-class numbers, no steering-success claim, no superhuman claim
   beyond the existing horizon sentence.
4. Author contact email unchanged (college address) in both editions.
5. Tag locations unchanged: (C5) in §conclusion, all six tags in place per LOG-4516.
6. NeurIPS checklist (main) and IEEE compliance untouched.
7. Both editions rebuild byte-clean (tectonic) with no `??` references and no
   duplicate labels; touched pages visually clean at reading scale.
8. The two new claims (converse dissociation; GEOSTEER benchmark wins) are grounded
   in the cited papers' own statements — the independent review must verify the
   arXiv abstracts before SIGN.

---

## 5. Explicitly out of scope

- v82 and v83 sources: frozen, untouched.
- The boxed "THREE BETS, ONE HORIZON" summary and its figure: verbatim.
- The Discussion's A1–A4 readings, the Limitations fences, the Conclusion's closing
  line ("The transfer is not a map; it is a draw."): verbatim.
- Any statement about EXP131's outcome (unmeasured) or EXP132 (apparatus-void):
  not cited, not implied.
- Any license for GEOSTEER as an experiment: this plan names it a watch item only.

---

*Draft only — licenses nothing. Next in the chain: independent Law #14 exact-version
review of this plan → CEO clearance → implementation lane → rebuild verification.*
