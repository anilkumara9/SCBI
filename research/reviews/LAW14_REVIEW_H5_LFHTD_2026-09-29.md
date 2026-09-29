# Law #14 independent review — H5/LFH-TD pre-registration

**Document under exact-version review:** `research/prereg/EXP_PREREG_H5_LFHTD_2026-09-29.md`
**Review lane:** LOG-4564 (pre-assigned). Independent of the LOG-4563 drafting lane.
**Date:** 2026-09-29. **$0 CPU.** Read-only except this file and the log append.
**Context read:** `research/innovation/SPRINT_2026-09-29_SUMMIT_ROUND2.md` (§H5),
`research/experiments/EXP107_TEMPLATECTRL_REPORT_2026-09-29.md`,
`SCBI/AGENTS.md` (house rules).

## Verdict: SIGN-WITH-FIXES

The core design is sound: falsifiable hypothesis, mathematically correct bars
(independently recomputed below), a well-calibrated kill-test, honest fences,
and five deviations that all read as genuine repairs. Five fixes are required,
all verifiable, none structural. The single most important finding is **F2**:
the draft's "15 vs 15" G-statistic premise is not licensed by its own split
specification.

## Independent verification (recomputed, not trusted)

**Binomial bars (exact, one-sided vs 0.5):**
- P(X ≥ 20 | n=30) = **0.049369** — draft says 0.0494 ✓
- P(X ≥ 19 | n=30) = **0.100244** — draft says 0.1002 ✓
- P(X ≥ 18 | n=30) = **0.180797** — draft says p ≥ 0.1808 ✓
- Dossier's "≥ 40/60, p ≈ 0.003": exact P(X ≥ 40 | n=60) = **0.006745**.
  The dossier's p-value is wrong by ~2.2× (observation only — the dossier is a
  proposal record; the bar itself is impossible regardless, see Q1).

**Kill-test calibration (G = acc(flipped=False) − acc(flipped=True), 15-vs-15):**
- EXP107's G = 30/30 − 4/30 = **0.8667** — draft says 0.867 ✓
- Null false-trigger P(G ≥ 0.30) = P(X−Y ≥ 5), X,Y iid Bin(15,½) = **0.0494**
- Genuine-signal false-trigger (true acc 0.75/cell): P(X−Y ≥ 5) ≈ **0.017**
- Realistic failure mode (template-dependent position: 15/15 original,
  ~7–8/15 flipped): G ≈ 0.47–0.53, comfortably above 0.30 ✓
- The 0.30 threshold sits well above null noise and well below the realistic
  failure signature. Well-calibrated.

**Archived-embeddings ground truth (verified against the artifact, not the draft's word):**
- `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz` exists:
  `embeddings` (60, 1024) float32, `ids` (60,) str ✓
- All 60 IDs byte-match `exp107_per_item.json` ✓
- Cell structure: 4 × 15 exactly (A-first/C-first × flipped True/False) ✓
- Labels: y=1 iff A-first, exactly, in every cell ✓
- sha256 (file): `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76`
- sha256 (embeddings array bytes): `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123`
  — corroborated by the EXP107 report's block-off prefix `9b6e8afb…` ✓
- sha256 (ids array bytes): `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9`
  (no independent corroboration in the EXP107 report; repair lane must confirm)

**Stratified-split behavior (sklearn 1.9.1, seed 20260929, test_size=0.5):**
- Per-cell test counts are deterministically **8/8/7/7** (train 7/7/8/8);
  test n=30, train n=30 hold regardless ✓
- The two 8-count cells are the **1st and 4th classes in sorted key order**
  (verified across four key encodings and two array orders)
- Therefore the flipped-group totals (flipped=False vs flipped=True test items)
  depend on the **unpinned** stratify-key encoding. 15/15 occurs for some
  encodings; **16/14 is reachable** with a natural encoding
  (e.g. keys `a_orig,b_flip,c_flip,d_orig` → orig group 16, flip group 14).
  The draft's "(15 flipped=False / 15 flipped=True in test)" and
  "(15 vs 15 test items)" are unlicensed assertions → **F2**.

## Question-by-question findings

**Q1 — Dossier-error repair: VERIFIED CORRECT.** The dossier's worth-it gate
demands "≥ 40/60 on the held-out decorrelated split" while also requiring a
"disjoint split within the bench." The bench has 60 items total; a 60-item
held-out set leaves 0 train items, so no head can be trained — the bar is
mathematically incompatible with the design, exactly as the drafter claims.
(The dossier's breaking point "≤ 35/60 → KILL" has the same defect.) Genuine
repair, not a smuggled change. Side observation: the dossier's "p ≈ 0.003"
is itself numerically wrong (exact 0.0067) — a dossier error the draft
correctly did not need to rescue.

**Q2 — Bars at n=30: correct; the CONTINUE bar is the canonical critical
value.** 20/30 (p=0.0494) is the α=0.05 one-sided critical value — the
least-arbitrary replacement for the impossible 40/60, not a weakened bar.
It is razor-thin (one item flips CONTINUE↔HELD), but the draft is honest
about this: the HELD zone registers the razor case explicitly and the
honesty ledger admits the test is "powered for the pre-registered bar but
not for fine distinctions." Not too easy; correctly fenced.

**Q3 — G threshold: exactly defined and well-calibrated** (numbers above).
G ≥ 0.30 = a ≥5/15 gap under the draft's 15/15 premise. It catches the
realistic failure (template-dependent position readout, G≈0.47+) and the
EXP107-style detector (G=0.867), while a genuine robust signal sits at G≈0
with ~1.7% false-trigger. Conservative in the right direction. The
"takes precedence over any overall score" edge case (e.g. 25/30 with
15/15 + 10/15 → KILL) is consistent with the EXP107 discipline: 10/15 on
flipped words is at-chance (one-sided p≈0.15), i.e. the signature shape.
The defect is not the threshold but its denominator premise → **F2**.

**Q4 — Law #7 / model-selection freedoms: pinned except two.**
Pinned: C=1.0, solver=lbfgs, max_iter=1000, random_state=20260929, layer 20
(archived embeddings — no choice), split seed 20260929, test_size=0.5,
G threshold, decision bars. Residual freedoms: (a) sklearn/numpy versions
are delegated to "the execution worksheet" without stated values → **F1**;
(b) the stratify-key encoding is unspecified, which determines the
per-cell test counts → **F2**. With the version pinned, all remaining
defaults (tol, fit_intercept, shuffle) are pinned with it.

**Q5 — Leakage: no path found.** The split is disjoint at the ID level
(overlap → RUN-INVALID registered); train labels are the legitimate
supervised signal; the template cue has zero label correlation in train by
construction (verified in the JSON), so the head *cannot* learn template
detection from the training labels — the kill-test's realistic target is
template-dependent position readout, which G catches. Test labels touch
only the final registered evaluation. The archived embeddings are the
EXP107 bench items; reusing them is provenance-clean (hash verification
registered), not leakage. Using the same IDs as EXP107 is fine.

**Q6 — Split spec: seed-pinned, no re-rolls — but denominators unpinned**
→ **F2**. The spec determines test n=30 but not the flipped-group
denominators the G definition assumes.

**Q7 — Overclaim fences: adequate.** §8 fences a CONTINUE as "a correlation
at one layer on one bench," requires downstream causal tests before any
capability statement, and claims novelty N1. The consequences —
"first autonomous output-side result" and GPU-proposal re-licensing — are
consistent with EXP107's own registered terms ("any new GPU proposal must
be re-licensed against a template-decorrelated design"; H5 *is* that
design). "Autonomous" is program-consistent (EXP107 report: "autonomous
(non-artifact) instantiation"). Not grandiose given the fences.

**Q8 — HELD zone: principled, not a cop-out.** 19/30 (p=0.1002) is evidence
neither for nor against; forcing KILL or CONTINUE there would manufacture
a verdict. The no-rerun/no-rescue rule prevents HELD from becoming a
soft-CONTINUE. Correct design.

**Q9 — Five deviations: all genuine.** (1) n 60→30: forced by the
impossibility (Q1). (2) HELD zone: principled (Q8). (3) G ≥ 0.30
formalization: the dossier had no numeric criterion; the threshold is
calibrated (Q3). (4) Per-layer search folded as CONTINUE-contingent
secondary: matches the dossier's "folded as a secondary registered
analysis," now specified. (5) Block-off "no backbone contact" form:
genuine specification of the JEV-27B discipline for a no-forwards design.
None weakens the test; the 40/60→20/30 change replaces an impossible bar
with the canonical α=0.05 critical value.

## Required fixes (each verifiable; none structural)

**F1 — Pin the execution environment (Law #13).** §3.3 delegates the sklearn
version to "the execution worksheet" without stating it, and the secondary's
torch/transformers environment is unpinned. Fix: state sklearn==1.9.1 and
numpy==2.5.3 for the primary analysis (the EXP107 report's environment),
torch==2.14.0+cpu, transformers==5.17.0, and the CPU thread count
(set and read back) for the secondary's fresh extraction; require all of
them recorded in the execution worksheet. Verifiable by worksheet diff
against these values.

**F2 — Pin the split denominators (the most important fix).** Pin the exact
stratify-key construction in the pre-reg (state the key form, e.g. the
tuple or string and its mapping); state the exact per-cell test counts it
yields under sklearn 1.9.1 + seed 20260929 (independently re-runnable);
define G = acc(N_F flipped=False test items) − acc(N_T flipped=True test
items) with the actual observed N_F, N_T; require the worksheet to log
N_F and N_T; restate the 0.30 threshold against the actual denominators
and correct or remove the "≥5 of the 15 item-margin" and "(15 vs 15)"
glosses. Verifiable by re-running the split and recomputing G's
 attainable values.

**F3 — Pin the artifact reference hashes.** §3.2/§3.4 require the execution
lane to "verify byte-identity" of the input npz but state no reference
value. Fix: pin the embeddings-array sha256
`9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123`
(corroborated by the EXP107 report's block-off prefix `9b6e8afb…`),
the ids-array sha256
`3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9`,
and the npz-file sha256
`6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76`
— with the repair lane independently re-computing and confirming all three
before pinning (do not trust transcription). Verifiable by hash comparison.

**F4 — Secondary analysis: backbone-contact discipline and descriptive-only
status.** §6 incorporates §3.3–§3.6, but §3.4/§3.5 are written for the
no-backbone-contact primary ("the backbone is never loaded"). Fix: state
the secondary's backbone-contact checks (backbone hash verified against
the LOG-331 pin before and after the fresh layer 4/8/12/16 extraction,
Δθ=0), state the secondary extracts the same 60 bench items by ID, and
state explicitly that secondary per-layer bars are descriptive-only and
license no verdict (four layers at α=0.05 carry ~18.5% family-wise
false-positive rate — the reason for no multiplicity correction beyond
the SECONDARY label). Verifiable by presence of the sentences.

**F5 — Decision-tree completeness.** The tree claims "No other branches
exist" but omits two registered precondition-failure branches: the §3.4(c)
determinism-pass mismatch → RUN-INVALID and the §3.3 train/test ID-overlap
→ RUN-INVALID (the input-hash HALT is shown; these are not). Fix: add both
branches to the tree or explicitly scope "No other branches exist" to
post-precondition branches. Verifiable by inspection.

## Notes (not fixes)

- N1: the dossier's "p ≈ 0.003" for 40/60 is numerically wrong (exact
  0.006745). Dossier-only error; no draft change needed.
- N2: negative G (head better on flipped-word items) has no signature gate;
  acceptable — the EXP107 signature is directional, and no plausible
  mechanism produces large negative G under this design.
- N3: the "≤ 18/30 (p ≥ 0.1808)" gloss is loose (P(X≥18)=0.1808 is the
  upper-tail value); harmless as a "not significant" gloss.

## Boundary

This lane fixed nothing, approved no execution, and minted no experiment
number. Fix-verification, the CEO launch decision, and execution are
separate later lanes.
