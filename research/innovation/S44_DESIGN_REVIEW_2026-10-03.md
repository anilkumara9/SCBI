# Law #14 Review — S4-4 (J1) Sprint Design (S44_DESIGN_2026-10-03.md)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design)
**Date:** 2026-10-03
**Document reviewed:** `~/workspace/SCBI/research/innovation/S44_DESIGN_2026-10-03.md` (exact file)
**Design-lane verdict under review:** CONDITIONAL RUN
**Review verdict:** **APPROVE-WITH-CONDITIONS** (conditions §9; execution additionally needs CEO venue approval per LOG-4408)

This review is of the design document only. It licenses nothing to run.

---

## 1. The operator — VERIFIED CORRECT (and the design caught a real error)

**Finding: the dimensional correction is right, and I verified it independently.**
- S4 doc line 159 writes "Π = W_E W_Uᵀ". With W_E, W_U ∈ ℝ^{50304×1024} (verified from the local HF cache: `gpt_neox.embed_in.weight [50304,1024]`, `embed_out.weight [50304,1024]`, `tie_word_embeddings: false`), W_E W_Uᵀ ∈ ℝ^{50304×50304} = V×V — dimensionally wrong for the claimed ℝᵈ→ℝᵈ map. The design's claim about the S4 doc is accurate.
- Π = W_EᵀW_U ∈ ℝ^{1024×1024}: [1024,50304]@[50304,1024] = [1024,1024]. ✓ Dimensionally valid.
- Sensible: Πh = W_Eᵀ(W_U h) = Σ_v logit_v · e_v, a fixed linear feedback map (decode-to-logits then re-encode). No training, Δθ=0 preserved. The design's admission that Π is not a projection and ‖Π‖₂ may exceed 1 (§4.2) is honest.
- Minor terminological note (not a condition): "soft re-embedding" is slightly loose — the construction uses raw logits, no softmax, so it is sharper than a true expectation under the output distribution. The math is pinned exactly as Π = W_EᵀW_U, which is what matters; the pre-reg should state "raw-logit weighting, no softmax" so the executing lane implements it verbatim (folded into condition C1).

## 2. The Banach license — SANE AS A FALSIFICATION TARGET, NOT AS A PREDICTION

**Finding: the steelman fails, and the design already knows it — which is why the screen is worth running.**
- Steelman of divergence: each GPTNeoX block is x ↦ x + Attn(LN(x)) + MLP(LN(x)) with parallel residual structure; the identity path alone forces per-block Lipschitz ≥ 1, and 24 composed blocks are generically expansive. Π is not contractive by construction. There is no mechanism in the design by which R = F_{0..24}∘Π becomes a contraction — §4.2 admits exactly this ("the contraction, if it exists, would have to come from the composition... and can only be established empirically").
- Is the screen worth running despite the honest prior κ̂≥1? **Yes**, for three reasons the design states plainly: (a) Stage 1 costs 40 CPU passes (~minutes, $0, zero founder GPU goodwill burned — Stage 2 is strictly gated on κ̂<1); (b) a κ̂<1 outcome would be genuinely surprising and informative precisely because the prior is against it; (c) the likely κ̂≥1 outcome buys the cheap kill of J1's Banach claim *plus* the bounded-T pilot, which has independent value and prior-art precedent (2602.14759 reports modest gains from looping).
- The expected value of this sprint is the kill + the bounded pilot, not the attractor. The design is honest about this (§9.1). CONTINUE is a long shot; that is priced, not hidden.

## 3. One-sided screen — ADEQUATE, WITH THE BACKSTOP SPECIFIED

**Finding:** κ̂ = max over a finite sample ≤ sup = true Lipschitz, so κ̂≥1 refutes contraction while κ̂<1 never proves it. The design states this explicitly (§4.4) — no one-sidedness laundering. The trajectory diagnostic backstop (‖h^{(t+1)}−h^{(t)}‖ strictly decreasing over t=0..7; non-decreasing trajectory voids the Banach reading even if ΔM>0, re-scoped to PIVOT) is an adequate empirical complement for a screen. For a 40-pass gate this is the right level of rigor; a certificate was never on offer.

## 4. The bars — HONEST, WITH TWO VERDICT GAPS TO CLOSE

**Finding:** the bars are jointly non-vacuous and pre-registered (Law #4 satisfied):
- ΔM ≥ +8pp with paired Newcombe LCI > 0.05 on n=60 is stringent (≈5 net items, CI entirely above +5pp) — a real capability bar, not a reach, not a gimme. The +8pp is a design-lane judgment call, but it is *pre-registered*, which is what the law requires.
- KILL = κ̂≥1 ∧ ΔM_bounded ≤ 0 is a clean joint kill.
- **Gap 1:** κ̂ ≥ 1 with Stage-1b unrun or infeasible → no verdict specified (defaults to nothing). → Condition C2.
- **Gap 2:** Stage-1b intermediate zone (0 < ΔM_bounded but LCI straddling, or ΔM>0 without LCI>0.05) → no branch specified. → Condition C2.

## 5. Non-resurrection audit — CLEAN

**Finding:** the distinctions are real, not rhetorical.
- (i) Killed static-geometry lanes injected *directions* and made causal claims about geometry; J1 injects no direction, iterates full residual states. Different object. ✓
- (ii) Dead E-step: J1 has no selection step — no candidates, no ranker; the sign-less-score failure mode is inapplicable. ✓
- (iii) S6 was layer-11 static geometry; J1 makes no layer-11 or static-direction claim. ✓
- (iv) R6/R7: R7 iterates in *output* space; J1 iterates *residual states* through the model's own layers with the Π map. The S4 doc's distinction (also vs Sprint2 C-B unembedding-difference space) is substantive. ✓
- (v) S4-5 uses confidence signals; J1 uses none — TESTA's anti-calibration finding is correctly judged irrelevant. ✓
- Nothing killed is re-tested; every kill stands.

## 6. Prior art — VERIFIED REAL, CHARACTERIZATION ACCURATE, N1 HONEST

**Finding (independently verified 2026-10-03):**
- arXiv:2602.14759 "Inner Loop Inference for Pretrained Transformers" is real. Abstract: inference-time inner looping by "repeatedly re-applying a selected block range" in frozen off-the-shelf LMs, "modest but consistent accuracy improvements"; v2 notes naive looping is unstable without regularizers. The design's characterization (same family, different construction; PIVOT branch overlaps its territory; no novelty claimed there) is accurate.
- arXiv:2605.12466 "Solve the Loop: Attractor Models" is real (Fein-Ashley & Rashidinejad, USC, May 2026). It trains a separate attractor module with implicit differentiation — the design's distinction (J1 trains nothing, Δθ=0) is correct.
- N1 (known combination) is the honest novelty read. The differentiators claimed (Π-feedback construction, contraction-licensed attractor claim, falsification-first bars on this bench/backbone) are real differences in construction, not denied prior art.
- **UNCHECKED:** the Blayney et al. 2026 citation (looped LMs converging to fixed points for most tokens) was not independently verified. → Condition C4.

## 7. LOG-4408 watchlist routing — CORRECT

**Finding:** the watchlist required Law #14 + CEO re-licensing for the CPU re-scope, explicitly "NOT proposed unilaterally." The design makes itself the re-licensing vehicle, routes through this review + CEO venue approval, and names the founder-gated items. This is exactly the required handling. The H-wave CPU-forward-pass precedent (LOG-4553) is a legitimate venue analogy.

## 8. Verdict check — CONDITIONAL RUN IS RIGHT, SHARPENED

**Finding:** DO NOT RUN would be wrong — the screen is ~free, falsification-first, and honest about its priors. But the design has genuine underspecifications that the pre-reg must close (below). The design-lane verdict stands, sharpened into conditions.

---

## 9. Verdict: APPROVE-WITH-CONDITIONS

Stage-1 CPU screen may run after (a) these conditions are closed in the pre-registration draft, and (b) CEO venue approval per LOG-4408:

- **C1 — Re-entrant input construction.** The pre-reg must pin exactly how Πh is fed as model input: sequence layout (single-token sequence vs appended to context), position IDs, attention mask, and the answer-position readout convention. This is currently an improvisation surface; the "no improvisation" claim (§3b) does not hold until it is pinned. State the raw-logit (no softmax) computation explicitly.
- **C2 — Verdict-gap closure.** The pre-reg must specify: (a) the verdict if κ̂ ≥ 1 and Stage-1b cannot run (recommend HELD with stated reason); (b) the branch for the Stage-1b intermediate zone (0 < ΔM_bounded without LCI > 0.05).
- **C3 — Stage-1b venue rule.** "CPU if tractable, else GPU" needs a tractability criterion (e.g., wall-clock or memory threshold) pinned in the pre-reg, not decided at runtime.
- **C4 — Citation verification.** Verify Blayney et al. 2026 at pre-reg stage, alongside the full-text follow-ups the design already flags (§8).
- **C5 — Expectation calibration (for the record, not the pre-reg).** The pre-reg should state plainly that the modal outcome is κ̂ ≥ 1 → bounded-T pilot, and that the pilot's value is boundary-science confirmation on this bench/backbone, not novelty. The design already says this; keep it in the pre-reg so a later reader cannot mistake the pilot for the attractor claim.

**What this review does NOT do:** it does not license execution (CEO venue approval still required), mint an experiment number, or approve Stage 2 (strictly gated on κ̂ < 1 by the design's own bars).

---

## 10. Summary

The S4-4 design is sound, honest, and worth executing conditionally. Its load-bearing claims check out: the Π dimensional correction is right (verified against the HF cache: embed_in/embed_out [50304,1024], tie_word_embeddings=false), the Banach framing is presented as conjecture with the honest prior against it, the screen is one-sided by explicit admission, the bars are pre-registered and non-vacuous, the non-resurrection audit is substantive, and the prior art is real and accurately characterized with an honest N1 read. The expected value is the cheap kill plus the bounded-T pilot — the design prices this correctly. Five conditions (C1–C5) must be closed in the pre-registration draft before Stage 1 runs; none is a reason to reject. The LOG-4408 routing is handled correctly.
