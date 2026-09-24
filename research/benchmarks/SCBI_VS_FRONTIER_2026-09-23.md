# SCBI vs the Frontier — v1 (2026-09-23)

*Standing Benchmark Analyst. Companion to FRONTIER_SCOREBOARD_v1. Every SCBI number below is from a primary artifact or signed log; bridge numbers carry the LOG-197/LOG-204 reclassification.*

## SCBI's rows on the same axes

| SCBI result | Axis | Number (primary source) | N / model | Verdict | Frontier comparison |
|---|---|---|---|---|---|
| Static steering, EXP063–066/070/077 (B_agg, lines, cones, offsets, radial) | A (accuracy Δ) | **ΔM = 0.0pp, exact p = 1.0** throughout | N=60, pythia-160m/L10 & 410m/L20 | Not supported — no steerability | CAA (the operator-equivalent baseline) demonstrates behavioral steering on Llama 2; SCBI's own operator-equivalent program scores exactly zero on its tasks |
| Output bridge rescues (EXP064/065/066/070/077) | A | **+5.0 to +16.67pp**, p = 0.0020–0.0313 | N=60 | **Reclassified LOG-197/204: label-assisted readout artifact — NOT capability evidence** | Excluded from the capability column by our own audit. It does not compete with any frontier row |
| EXP067 (QK/OV subspace) | — | STAGE_A_HALT (rank 33 < 64) | 410m | Untestable under operationalization | No comparison possible |
| EXP078 (energy gate) | — | HALT (e_median = 0.0544 < 0.10) | 410m | Informative localization only | No comparison possible |
| EXP079 (probe) | — | Infeasible by construction (max N_final = 46 < 50) | — | Design void | No comparison possible |
| G1 (QK-null-space) | — | **KILL** of the handover's §3.3 sentence | Weight-only, $0 | Mechanism refuted | Negative result; no frontier equivalent needed |
| K1 | A | **Executing** (verdict pending) | $0 CPU | — | Will be plotted on arrival |

## The gap, in plain language

**On axis A (accuracy gain at matched compute):** the frontier's floor is DEER at +0.3–5.0% *while saving compute*, and its representative band is Meta-Reasoner +9–12%, ∇-Reasoner 71.2→80.4% on MATH-500, Self-Refine ~+20% absolute. **SCBI's capability entry is empty: 0.0pp across every static family, and the only positive numbers are disqualified as artifacts by our own audit.** We do not trail by a margin; we have no entry.

**On axis B (compute saved at non-inferior accuracy):** DEER owns this axis (−19–80% CoT, accuracy up). SCBI has no efficiency result at all.

**Where SCBI leads:** boundary science. No frontier system publishes a pre-registered, adversarially-reviewed demonstration that raw geometric similarity (~0.7 cosine) yields zero causal transfer under static injection, replicated across scale with the Procrustes failure mode retracted on record. That is a genuine, if negative, contribution — it is not a capability, and the board does not let it masquerade as one.

## What beating the frontier would require

A future SCBI result counts as beating the frontier **iff** all of the following hold (synthesis §D2, binding):

1. **Per-instance construction** — the intervention varies non-trivially across instances (else it is Family A steering with extra steps).
2. **Transfer-validated internal evaluator** — E's scores track rescue on a held-out distribution, not the gate distribution.
3. **Matched-compute superiority** — beats ToT-style search, best-of-N, ∇-Reasoner, Activation-LQR-style closed loop, DEER, and debate/MoA **at equal forward-pass budget**, plus the pinned M15 comparators (LTPO, Meta-Reasoner, LatentMAS, NoisyCoconut).
4. **Conditional computation** — randomizing E's measurements kills the gain (the P1 mechanism bar).
5. **Specificity** — Δ_valid − Δ_control > 0, pre-registered.
6. **Powered** — at N≤80 no run can license L2 (MDE 11.25–20pp > 2·δ_min); a powered re-registration at **N≈100+ (~1,000 passes, minutes on a T4)** with lower CI > δ_min = 0.05 is the minimum quantitative bar.

Numerically: a claim of "SCBI beats Meta-Reasoner" needs ≥+12pp over the matched baseline at N≥100 with the full comparator battery — i.e., roughly an order of magnitude more evidence than anything the program has produced to date. The board will show that row the day it exists, and not before.
