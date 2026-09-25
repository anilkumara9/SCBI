# Paper Figure/Table Descriptions + Revised Abstract (PROPOSAL — 2026-09-24, LOG-280)

**Status:** Working draft for CEO review. NOT applied to `reports/paper_draft.md` — the
paper is awaiting Law #14 re-review of the LOG-276 diff; applying these would be a
silent edit, which Law #3/Law #12 forbid. Every number below is already
artifact-grounded in the LOG-279 proofread pass; no new numbers are introduced.

---

## Figure 1 — EXP077: the geometric-variant sweep (proposed)

**Panel A — Radial sweep (α ∈ {0.25, 0.50, 1.0, 2.0}).** Bar chart of ΔM (pp)
per α at Pythia-410M, layer 20, N=60. All four bars at exactly 0.00 pp
(McNemar p=1.000000, Holm-adjusted; significant-set S_H=∅). Baseline
0.5667 shown as a dashed reference line.
**Panel B — Angular / control / offset / replication.** Four point markers,
all b=0, c=0, p=1.0: cone-vs-line (ρ=30°, K=8), cone-vs-control,
α=1.0 offset, C3-vs-C1 replication.
**Panel C — The output bridge gate.** Single contrasting bar at +10 pp
(b=6, c=0, p=0.03125) on the same axes — the rescue control firing while
every geometric variant of the concept direction is flat zero.
**Caption note (licensed scope, verbatim from the evaluator ruling):** branch
(c) NEITHER kills *only* the tested unconditional ρ=30° cone and α=1.0
offset hypotheses at pythia-410m/layer-20; other radii, gated, and
conditional (concept-projection) variants survive and are untested.

## Figure 2 — EXP067: the Stage A halt (proposed)

**Panel A — Anchor rank vs. the full-rank bar.** Two bars: observed anchor
rank 33 (head 0, pair V1→V2_Biblical) against the pre-registered bar of 64,
with the spectral-gap readout (GPU 1.59e-08 vs. CPU-smoke 1.44e-08 — within
10%, device-independent as predicted) against the >1e-6 guard.
**Panel B — The decision tree that fired.** Branch (a) STAGE_A_HALT
highlighted; the canonical falsification criterion (branches (b)–(e))
shown greyed-out, never exercised. Label: "H1 untestable under this
operationalization — neither falsified nor confirmed; I1 stands
unchallenged."
**Panel C — Why the sound operationalization was underdetermined.** Schematic:
80 anchors spanning only ~33 of the 64 head-subspace dimensions —
the rank-deficiency defect (§6) was never fixable under this anchor design.

## Table 1 — EXP065/066 confirmatory conditions (proposed consolidated table)

One table replacing the §5.3/§5.4 split: per run (EXP065 = Pythia-160M/L10;
EXP066 = Pythia-410M/L20), conditions Static B_agg, "Aligned" dynamic basis,
Same-Layer Output Bridge (RESCUE CONTROL — known-answer direction, not a
mechanism control, LOG-204 §H7), Random-Rotation Control (5 seeds), B_⊥,
B_wrong; columns: ΔM (pp), b, c, McNemar exact p, KL div. All basis cells:
ΔM=0.0, b=c=0, p=1.0. Bridge cells: +16.67pp (10/19, p=0.0020, KL 0.0118)
and +13.33pp (8/26, p=0.0078, KL 0.0283). Footnote: Wilcoxon-on-margins
demoted to exploratory (§5.5 — the B_wrong control reaches p=1.2×10⁻⁸ with
b=c=0).

---

## Revised abstract (PROPOSAL — replaces the current abstract on CEO sign-off)

> We report a boundary result for inference-time steering of frozen language
> models (Δθ = 0). Relational contrast directions Δh = h(rel) − h(neu)
> extracted across five disjoint entity vocabularies exhibit high *raw*
> pairwise cosine similarity (mean +0.72 on Pythia-160M, +0.69 on
> Pythia-410M) with no alignment applied — yet static injection of the
> aggregated basis B_agg into the residual stream produces **zero** decision
> changes (ΔM = 0.0 pp, b = 0, c = 0, McNemar p = 1.0) on an N = 60
> relational-reasoning benchmark with verified headroom (19 and 26
> rescuable errors), while a same-layer output-space bridge — carried as a
> **rescue control** (known-answer direction), not a mechanism control —
> rescues 10/19 (+16.7 pp, p = 0.0020) and 8/26 (+13.3 pp, p = 0.0078)
> errors with zero corruptions. **Raw geometric similarity of internal
> contrast directions does not imply causal interchangeability under static
> injection.**
>
> The boundary survives two further falsification attempts. EXP077, a
> GPU-executed sweep of static geometric variants of the concept direction
> (cone at four angles, cone-vs-line, cone-vs-control, offset, radial grid),
> returned branch (c) NEITHER: no variant moved a single decision (ΔM = 0,
> p = 1.0 throughout) while the bridge rescued again (+10 pp, p = 0.03125) —
> killing only the tested unconditional 30° cone and α = 1 offset hypotheses
> at Pythia-410M/layer-20. EXP067, the same-space full-rank alignment
> experiment pre-registered with a falsification criterion binding on every
> outcome, halted at its own Stage A guard (branch (a): 80 anchors span
> only ~33 of 64 head-subspace dimensions), leaving its hypothesis
> untestable and the boundary unchallenged.
>
> We further document, inside this paper, two forensic corrections to our
> own program's records. First, the retracted Procrustes claim: summary
> documents had stated a rotation *improved* cross-vocabulary alignment
> (Δcos ≈ +0.13 to +0.79); recomputation from primary artifacts shows it
> **destroyed** similarity (Δcos = −0.72 / −0.70) — a rank-≤2 Procrustes fit
> on unembedding-space anchors applied to full-rank residual-stream
> directions, which we prove can only scramble (Lemma). Second, the
> program's null-space downstream-filtering explanation: a weight-only
> QK/OV projection-energy audit (G1, verdict KILL) showed the failed
> direction is *more* QK-visible (Ē_QK = 0.390, above the random-unit-vector
> null 95th percentile) than the rescuing bridge (Ē_QK = 0.356, mid-null) —
> the exact inversion of the theorem's central sentence. The boundary claim
> rests on its endpoints and survives; the mechanism position is now
> **readout-misalignment-or-unknown**, and the bridge's rescue is licensed
> only as label-assisted readout steering at evidentiary level L1
> (option-informed by construction, per the Law #7 bridge-leakage audit).
>
> Prior-art position (Law #10): the tested mechanism is algorithmically
> equivalent to Contrastive Activation Addition (Rimsky et al., ACL 2024);
> assessed novelty N1 — Known Combination, adversarially signed. This paper
> claims no method, no mechanism for the bridge's rescue, and no capability
> — the program holds zero positive signals for autonomous steering. Its
> contribution is a carefully controlled negative result with the confounds
> surgically removed: *here is what static steering cannot do, here is the
> proof that our earlier attempt to say otherwise was wrong, and here is
> the list of explanations we have now ruled out.*

**End of proposal.**
