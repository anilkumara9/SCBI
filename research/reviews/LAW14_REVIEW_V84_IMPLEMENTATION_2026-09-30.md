# Law #14 Exact-Version Review — v84 Implementation (Built Sources)

**Lane:** LOG-4760 (pre-assigned). **Verdict: SIGN.**
**Review date:** 2026-09-30. **Standard:** binding, exact-version.
**Implementation under review:** `~/workspace/scbi-paper`, branch `arxiv-prep`,
commit **`baa044d`** (`baa044d41d75b96b9203511a0c9b080336d0413e`),
message "feat(v84): sweep related-work additions — Nadaf converse dissociation, GEOSTEER future-work watch item".
Verified HEAD = `baa044d` before review; exact-version requirement satisfied.

**Change plan reviewed against:** `research/paper/V84_CHANGE_PLAN_SWEEP_2026-09-30.md`,
post-fix SHA-256 `af0f0d12e819e96e8744eae6e5d0305ad4577de30cb8f0728b8b09372fe4a9a6`
(recomputed locally — match).

**Scope:** read-only review. No paper sources modified, no commits, no pushes, no
credentials touched. Prior reviews LOG-4754 (plan) and LOG-4516 (pre-wave draft) do
not cover this build; this lane reviews the built implementation.

## 1. Insertion completeness — every plan item present, verbatim

Diffed `baa044d` against its parent `36d154e`. The source diff touches exactly five
text files (plus the two rebuilt PDFs), all at the licensed insertion points:

| # | Plan item | Found | Verdict |
|---|-----------|-------|---------|
| 1 | Main: "Two" → "Three contemporaneous results" + Nadaf converse sentences (`\citep{nadaf2026}`), closing sentence "None threatens the boundary claim; all three corroborate its shape from independent angles — one theoretical, one peer-reviewed behavioral, one converse-directional" | `v84/paper.tex`, converging-evidence paragraph, byte-match to plan text | PASS |
| 2 | Main: new future-work paragraph with `\citet{ngo2026}` (GEOSTEER watch item), after section opening, before bets figure | `v84/paper.tex`, byte-match to plan text | PASS |
| 3 | IEEE: converging-evidence sentence extended with "and a converse-direction result in which function-vector steering succeeds where the logit lens cannot decode at any layer \cite{nadaf2026}" | `v84-ieee/sections/sec-discussion.tex`, byte-match | PASS |
| 4 | IEEE: one sentence before "The program advances only through gates" — "One named watch item: \cite{ngo2026} reformulate steering as Riemannian optimization — geodesic multistep updates beating one-step baselines — the instrument class the program would escalate to if one-shot injection fails." | `v84-ieee/sections/sec-conclusion.tex`, byte-match | PASS |
| 5 | `nadaf2026` bibtex entry appended to both `v84/refs.bib` and `v84-ieee/refs.bib` (title "Steerable but Not Decodable: Function Vectors Operate Beyond the Logit Lens", eprint 2604.02608, no unsupported `−0.91` figure — only `> 0.90`) | both bib files, byte-match | PASS |
| 6 | `ngo2026` bibtex entry appended to both bib files (title "GEOSTEER: Geodesic Optimization for Activation Steering in Large Language Models", eprint 2609.10658) | both bib files, byte-match | PASS |

Every changed line belongs to the plan. No other source line changed.

## 2. Rebuild verification — independent, this lane

Fresh `tectonic` rebuilds from the committed sources, run by this review lane:
- `v84/paper.tex` → `paper.pdf`: EXIT 0, no `??` in output, zero "undefined" citation warnings.
- `v84-ieee/ieee-paper.tex` → `ieee-paper.pdf`: EXIT 0, no `??` in output, zero "undefined" citation warnings.
- Rendered references verified in the rebuilt PDFs: [17]/[18] Nadaf and Ngo entries
  appear in the IEEE bibliography; Nadaf converse sentences and GEOSTEER watch-item
  paragraphs appear in the main-edition body. (Title case is downcased by the
  bibliography style — expected, style-normalized, not a defect.)

## 3. Regression checklist

1. **No new numbered claims:** zero `C7` occurrences in the diff; `\textbf{C1}`–`\textbf{C6}`
   each still present exactly twice in `v84/paper.tex`; no removed line touches any
   C-tag sentence.
2. **Touched pages confined:** only the licensed insertion points; no `.tikz` figure
   file changed; no claim text edited.
3. **Banned language absent:** no "release candidate" string, no `+0.010`/`−0.004`
   numbers, no steering-success claim, no new superhuman claim. The single
   "Superhuman" diff hit is the pre-existing unchanged horizon sentence
   ("names the horizon, never an achievement").
4. **College email:** `1nh22cd066@newhorizonindia.edu` present in `v84/paper.tex`
   (main) and `v84-ieee/ieee-paper.tex` (IEEE). Old personal address absent from the
   diff.
5. **Tags:** (C5) in §conclusion untouched at its location; all six tags in place.
6. **NeurIPS checklist / IEEE compliance:** untouched (no checklist-file changes in
   the diff).
7. **New-claim grounding:** the converse-dissociation numbers (4,032 pairs, 12
   tasks, 6 models, `> 0.90`) and GEOSTEER benchmark wins (TruthfulQA,
   RealToxicityPrompts, UltraFeedback) are stated as the cited papers' own
   statements, matching the LOG-4751 sweep-verified abstracts. No license or
   verdict implication is attached to either.
8. **v82/v83:** untouched — zero files outside `v84/` and `v84-ieee/` in the diff.

## 4. Plan deviation — `\citet` → `\cite` in IEEE

The plan proposed `\citet{ngo2026}` in the IEEE conclusion sentence; the build uses
`\cite{ngo2026}` because the IEEE template does not load natbib. Verified:
renders as "[18]" — grammatically correct in the sentence
("One named watch item: [18] reformulate steering as Riemannian optimization").
Intent-preserving, conformance-mandated. Correctly recorded by the implementation
lane. Accepted.

## Verdict

**SIGN.** The committed v84 implementation at `baa044d` carries exactly the
CEO-cleared, Law #14-reviewed change plan, builds byte-clean in both editions with
no undefined references, and passes every regression check. Cleared for the
paper-side push chain (fresh token, fast-forward verification, no force-push —
founder-reserved, not licensed here).
