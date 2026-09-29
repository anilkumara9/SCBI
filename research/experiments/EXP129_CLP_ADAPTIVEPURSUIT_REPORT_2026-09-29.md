# EXP129 — Closed-Loop Adaptive Pursuit (CLP): Execution Report

**Lane:** LOG-4715 (pre-assigned). **Family:** C of the paradigm-break sprint
(LOG-4693). **Gate:** LOG-4710 (PASS, conditional). **Pre-reg:**
`research/prereg/EXP_PREREG_CLP_ADAPTIVEPURSUIT_2026-09-29.md`
(post-erratum sha256 `8eea9f0d659501885cbe7e30657824a372495fda9ecc130c8cc4a0cabeee5ba7`,
verified before the first forward). **Law #14:** SIGN-WITH-FIXES (LOG-4712),
seven fixes byte-verified (LOG-4713), v̂₂-provenance erratum (LOG-4714).

**$0 CPU. Δθ=0 by construction** — pure forwards through the frozen
Pythia-410m in eval mode plus exact autograd JVP/VJP sensing at frozen
weights (EXP127's Law-#14-licensed apparatus); no optimizer, no loss, no
backward pass into parameters.

## Verdict

**KILL** — median per-item feedback-gain ratio **r = 1.000005 ≤ 1.2**.
The loop adds nothing the push didn't already do; the adaptive-pursuit
premise on $0 is dead. Recorded as adverse evidence against the GPU
closed-loop line's (CLLC/EXP086-B) premise; it does **not** unlicense
already-signed GPU bundles (licenses are per-experiment; evidence updates
priors).

This is a real null, not an apparatus failure: every breaking-point guard
passed, all 10 items agree (r ∈ [0.9998, 1.0002]), and the falsification
tree ran to the decision node.

## What the numbers say

| Quantity (median over 10 items) | Value | Bar | Branch |
|---|---|---|---|
| r = ‖d₂‖/max(‖d_sum‖,‖d_single‖) | **1.000005** | ≤ 1.2 → KILL | **fires** |
| saturation ‖d₂−d₁‖/‖d₁‖ | 1.013390 | ≤ 0.1 → KILL | no fire |
| dose ‖d₂‖/‖d_sum‖ | 1.652381 | ≤ 1.2 (+beats single) → KILL | no fire |
| loop/single ‖d₂‖/‖d_single‖ | 1.000005 | — | — |

Per-item r: [0.9998, 1.0001, 0.9999, 1.0000, 1.0001, 0.9998, 1.0001, 1.0002,
0.9999, 1.0000] — the loop arm's displacement equals the single-shot arm's
to four decimal places on every item.

[INTERPRETATION] The adjoint correction re-derived the direction it started
from: ŵ = Mᵀd̂₁/‖Mᵀd̂₁‖ points back along v̂₁ (the measured displacement d₁
is dominated by the σ₁ component, so the exact local adjoint of its
direction is v̂₁ again), making δ₂ = δ₁ + c ≈ B·v̂₁ = δ_single. The
"feedback" is a complicated way to do a single push — the loop's second act
is the open-loop single shot wearing a sense-act costume. The dose reading
is mechanically excluded (every arm spent exactly B; the injected loop norm
‖δ₂‖ ≤ B by the triangle inequality, audited), so this is not "a bigger
push": it is the same push, arrived at via feedback. The premise KILL
branches were evaluated first per FIX-1 and did not fire; the median-r bar
then fired KILL.

## Tree-node record (all PASS unless noted)

| Tree node | Result |
|---|---|
| Protocol hash pin (pre) | `8eea9f0d…` PASS |
| Bench provenance: 10 verbatim EXP107 prompts, ids `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}` | PASS |
| v̂₁ re-pin: npz sha256 `9b527c…13dc` + all 10 `v1__<prompt_id>` keys aligned | PASS |
| v̂₂ derivation (LOG-4714 erratum): seed `20260929_4714`, K=40 deflated power iteration, exact JVP/VJP | PASS — all 10 \|v̂₂ᵀv̂₁\| < 1.1e-08 (bar 1e-6) |
| Budget B = 0.01 × median‖y₂₀‖ = **0.50578363**, recorded before first perturbed forward | PASS |
| 50 forwards (10 base + 40 arm) + adjoint VJPs | DONE, exit 0 |
| Norm-budget audit: ‖δ₁‖=‖c‖=‖δ_open‖=B/2, ‖δ_single‖=B (rel tol 1e-5) | PASS all 40 components |
| Sensing-discipline assert (FIX-3): ops = {exact-jvp, exact-vjp}; no finite-difference term anywhere | PASS |
| Correction-rule pin (FIX-4): single frozen §3.5 rule, all 10 items | PASS |
| Backbone LOG-331 pin pre/post | `ec276abe…` / identical — Δθ=0 |
| Raw records hash-pinned before verdict (§3.8) | PASS (pins below) |
| Falsification precedence: saturation, dose-in-disguise first | neither fired |
| **Median r** | **1.000005 → KILL** |

## Raw artifacts (hash-pinned before the decision statistic existed)

- `experiments/runs/EXP129_clp/out/exp129_per_item.json` →
  `14a566ced435e4fbab1b9190bf4380d34c90db7a9bb65771374fc67845083fee`
- `experiments/runs/EXP129_clp/out/exp129_vectors.npz` →
  `e3d869aff941cb2d499c504a5e27b804d51019b5aef70bf8f48377b43813773e`
- `experiments/runs/EXP129_clp/out/exp129_worksheet.json` →
  `ec3b68d23cb84547eb0251ba1e87b6ccffd45bd1618c53a63daddf3506673c0a`
- `experiments/runs/EXP129_clp/out/exp129_console.log` →
  `7022273b38d5985a9482154fc97a1b35893871ff82814f580d471ed05d7d5470`
- Executor: `experiments/runs/EXP129_clp/exp129_execute.py`; stdout log retained.

## Disclosed protocol-ambiguity notes (for the independent review)

1. **Readout site (§3.1).** The protocol defines x_{24,last} with a
   "(post-final-LayerNorm)" parenthetical, but its entire design — v̂₁
   re-pinned from EXP127's artifact, M as "the exact L20→L24 Jacobian",
   the deflated iteration on MᵀM, the adjoint correction — references
   EXP127's propagator (block-23 output, pre-final-LayerNorm, final token).
   The executor used EXP127's map: the only internally consistent
   executable reading (a post-norm readout would put d̂₁ outside M's
   codomain, breaking the adjoint). The parenthetical is treated as a
   drafting slip; the review may adjudicate.
2. **Flips [OBSERVATION].** Recorded as **not measured**: the registered
   apparatus provides no licensed decision-readout channel — the logit
   channel is barred (§6), generation/probe/head are barred (§3.7), and no
   residual decision channel is licensed by this protocol. No bar reads
   flips; the verdict is unaffected.

## Honest frame

Control-efficiency question, not a capability claim — **the capability
scoreboard stays at zero positive autonomous-steering signals**. One
model (frozen Pythia-410m), one decision set (10 pinned prompts), one
span (L20 → x_{24,last}). The KILL retires the adaptive-pursuit premise
on $0 as a publishable boundary fact: at this scale, exact-adjoint
feedback re-targeting buys no displacement per unit norm that the
open-loop push didn't already buy — the feedback gain is 1.000 to four
places.
