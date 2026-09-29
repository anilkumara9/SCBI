# Law #14 Independent Review — v84 Change Plan (Frontier-Sweep Related Work)

**Lane:** LOG-4754 (pre-assigned). **Verdict: SIGN-WITH-FIXES.**
**Artifact reviewed (exact version):** `research/paper/V84_CHANGE_PLAN_SWEEP_2026-09-30.md`,
SHA-256 `191cb6b37149f359d22450a40e96bfbd7a3b0b99265d92a478392c6fbd3b372b`.
**Date:** 2026-09-30. **$0 CPU, paper only.** v82/v83/v84 sources read-only;
nothing in them modified by this review.

---

## 1. Pre-review verification

- Plan SHA-256 hashed by the reviewer before reading:
  `191cb6b37149f359d22450a40e96bfbd7a3b0b99265d92a478392c6fbd3b372b` — the
  reviewed bytes are the drafted bytes (LOG-4753).
- House rules (`~/workspace/SCBI/AGENTS.md`) read per the runtime note.
- This is an exact-version review under the 2026-09-28 lesson: the verdict below
  names the exact artifact filename and hash. A review of a different version
  would not satisfy Law #14.

## 2. Citation verification (independent arXiv re-hit)

### 2a. arXiv:2604.02608 — "Steerable but Not Decodable"

Re-fetched 2026-09-30. **Verified:**
- Title: "Steerable but Not Decodable: Function Vectors Operate Beyond the Logit Lens" ✓
- Author: Mohammed Suhail B Nadaf ✓ (plan's "Mohammed Suhail B. Nadaf" is standard
  BibTeX punctuation — acceptable, not a finding)
- Submitted 3 Apr 2026 (v1); **last revised 8 May 2026 (v2)** — plan says "v2 Aug
  2026" → **WRONG (FIX-1)**
- 12 tasks, 6 models from 3 families, 4,032 directed cross-template pairs ✓
- Converse cell: decodable-without-steerable nearly empty (3 of 72) ✓
- "FVs encode computational instructions, not answer directions" ✓ (abstract:
  "FVs encode computational instructions, not answer directions")

**Not verified — the "−0.91" number:** the plan's §1 citation header and its
proposed main-edition insertion both carry "gaps to −0.91". Full paper text
extracted via `pdftotext` and searched: the string "0.91" appears only as
steering-accuracy figures (0.918, real 0.91 vs control 0.35); no "−0.91" gap
metric exists in the text, and the abstract carries no such number. The number
originates in the LOG-4751 sweep report, not in the paper. **→ FIX-2.**

Abstract-verified replacement language exists: "Even at > 0.90 steering accuracy,
projecting the FV through the unembedding yields incoherent token distributions."

### 2b. arXiv:2609.10658 — GEOSTEER

Re-fetched 2026-09-30. **Verified:**
- Authors: Xuan Cuong Ngo, Hao Vo, Ngan Le ✓
- Submitted 9 Sep 2026 ✓
- Steering formulated as Riemannian optimization; sequence of small geodesic
  steps on the representation manifold ✓; learned nonlinear activation-space
  objective guiding each step ✓; norm-preserving ✓
- Benchmarks: TruthfulQA, RealToxicityPrompts, UltraFeedback ✓; "consistently
  improves over state-of-the-art activation steering baselines" ✓
  (plan's "beating SOTA one-step baselines" is a faithful paraphrase)

**Title defect:** the actual arXiv title is "GEOSTEER: Geodesic Optimization for
Activation Steering in **Large Language Models**". The plan's §2 header and its
`@misc{ngo2026}` bibtex title say "…in **LLMs**". **→ FIX-3.**

## 3. Insertion points (v84 sources, read-only)

- **Main, converging-evidence paragraph:** `\paragraph{Converging evidence: the
  gap is not ours alone.}` exists in `v84/paper.tex`; its current text matches
  the plan's quoted basis verbatim ("Two contemporaneous results independently
  reproduce the decode-without-control shape…", closing "Neither threatens the
  boundary claim; both corroborate its shape from independent angles, one
  theoretical and one peer-reviewed behavioral."). The plan's "Two → Three"
  edit and closing-sentence rewrite are consistent with the actual text. (The
  plan's "line 173" is approximate — the paragraph sits in that neighborhood;
  acceptable, not a finding.)
- **IEEE, Novelty-and-position paragraph:** exists in
  `v84-ieee/sections/sec-discussion.tex`; the converging-evidence sentence ends
  at the `\cite{jia2026}` clause exactly as the plan quotes. The proposed append
  is consistent.
- **Main, future-work section:** `\section{Future work: three bets, one
  horizon}` + `\label{sec:future}` exist (`v84/paper.tex`, l.522–523); the
  opening line matches the plan's quoted text verbatim; the bets figure follows.
  The proposed new paragraph slots between the opening line and the figure
  without touching the boxed summary, figure, or bets. ✓
- **IEEE, conclusion:** `v84-ieee/sections/sec-conclusion.tex` l.20 future-work
  paragraph matches the plan's quoted text verbatim; the proposed sentence
  inserts before the final "Superhuman" sentence as described. ✓

## 4. Claim-scope check

- No new numbered claims: the proposed text adds no `\item[\textbf{C7}]`, does
  not reword C1–C6, O1/O2, or any tag. ✓
- GEOSTEER is framed strictly as a named watch item / escalation candidate
  ("recorded here as a watch item, untested on our benches") — never as a result
  or a license. The plan's §5 explicitly excludes "any license for GEOSTEER as
  an experiment". ✓
- The converse-dissociation framing ("decodability does not imply steerability,
  and steerability does not imply decodability") is grounded in the verified
  abstract. ✓
- No figure changes; no banned language in the proposed text (no "release
  candidate" string, no fabricated numbers beyond FIX-2, no steering-success
  claim on SCBI's benches, no superhuman claim beyond the existing horizon
  sentence). ✓

## 5. Bibliography keys

`nadaf2026` and `ngo2026`: **no hits in either** `v84/refs.bib` or
`v84-ieee/refs.bib` — no collisions. (`jia2026` exists as `@article`, untouched.)

## 6. Regression checklist

The plan's 8-item checklist is complete and honest. Item 8 ("the independent
review must verify the arXiv abstracts before SIGN") is discharged by §2 above.
One gap, verdict-immaterial: the checklist does not separately itemize
citation-field accuracy (version dates, exact titles) — but item 8's "grounded
in the cited papers' own statements" covers it, and the three field defects are
caught as numbered fixes below.

## 7. Scope

Held. This review read v84 sources only; v82/v83/v84 untouched. The review
itself modifies nothing.

## 8. Verdict: SIGN-WITH-FIXES

The plan is sound and signable after the three launch-gating citation fixes
(Law #3 — never fabricate citations or their fields).

**FIX-1 (launch-gating):** Correct the Nadaf version history everywhere it
appears in the plan (§1 citation header; the proposed main-edition insertion
if it repeats the date): "v1 Apr 2026; **v2 May 2026**" (last revised 8 May
2026 per arXiv), not "v2 Aug 2026".

**FIX-2 (launch-gating):** Remove the unverified "−0.91" gap number from the
plan (§1 citation header: "gaps to −0.91"; proposed main-edition insertion:
"(gaps to $-0.91$)"). Replace with abstract-verified language, e.g.: "even at
> 0.90 steering accuracy, projecting the FV through the unembedding yields
incoherent token distributions." Do not reintroduce any gap number not present
in the cited paper.

**FIX-3 (launch-gating):** Correct the GEOSTEER title to the exact arXiv title
in both places it appears (§2 header and the `@misc{ngo2026}` bibtex entry):
"GEOSTEER: Geodesic Optimization for Activation Steering in **Large Language
Models**" (not "…in LLMs").

## 9. Observation (not a fix — for the parent's attention)

The same two field errors (v2 "Aug 2026"; "−0.91") originate in the LOG-4751
sweep report (`research/benchmarks/FRONTIER_SWEEP_2026-09-30.md`, lines 59–60).
That report is a signed artifact; correcting it needs a dedicated erratum lane,
which is outside this review's scope. Recommended, not required for this plan's
SIGN.

---

*Independent review only — implements nothing. Next in the chain: fix-verification
of FIX-1…FIX-3 → CEO clearance → implementation lane → rebuild verification.*
