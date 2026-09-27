# R4 (EOC) — Law #15 Worth-It Gate Analysis

*Innovation agent, 2026-09-25. ON PAPER ONLY — no compute, no model runs, no commits.
Source: `research/proposals/AMBITION_SPRINT_SYNTHESIS_2026-09-24.md` §R4; rank order confirmed (R1→EXP083, R2→EXP084, R3→EXP086 done/queued; R4 next). No R4 guards closed; no pre-registration drafted. PWAR is HELD (piggyback-only).*

**Candidate:** R4 — EOC: Edge-of-chaos per-item gain scheduling.

---

## 1. The precise question [HYPOTHESIS]

Does per-item gain scheduling toward λ̂ ≈ 0 change 2-hop decisions beyond fixed-gain baselines — i.e., is **distance-to-criticality a usable per-item control signal** for a frozen model?

Construction: per item x, estimate a finite-time Lyapunov proxy λ̂(x) = log(‖Δh_L‖/‖Δh_0‖)/L from two nearby forward passes (x, x+ε). Schedule the model's intrinsic global gain g(x) — attention softmax temperature τ and/or residual-stream scale, both runtime scalars, Δθ = 0 — to push λ̂ toward 0.

## 2. The decision it changes

**KILL** criticality-scheduling if scheduler ≤ best fixed gain **or** gain shows no |λ̂| dose-response.
**CONTINUE** to a pre-registered (diagnostic, gain-actuator) sweep **only** on the dose-response signature.
**Diagnostic-invalid branch:** λ̂ unmeasurable/unstable across seeds → KILL the candidate (not the theory).

**What rides on it:** whether *intrinsic-dynamics control* — modulating how the model computes rather than what direction is injected — is a live mechanism family. This is a genuinely new family (gain scheduling vs vector injection). A KILL closes the sharpest candidate in that family and takes the PWAR piggyback down with it; a CONTINUE opens the program's first non-injection control mechanism.

## 3. Cheapest falsifying test and cost

Sequenced kill-first (each gate must pass before the next spend):

- **Stage −1 ($0 CPU):** verify the Poole et al. 2016 citation (currently UNVERIFIED-WEB) and sanity-check the λ̂ finite-difference proxy on a toy random net (CPU, no real weights) — proves the diagnostic machinery is well-defined.
- **Stage 0 — diagnostic gate (120 passes ≈ 0.0015 T4-h, free-tier GPU):** 2 passes/item × 60 items. KILL the candidate here if λ̂ is unstable across seeds/ε (diagnostic-invalid) — no gain scheduling attempted.
- **Stage 1 — pilot (180 more passes; total 300 ≈ 0.0038 T4-h):** 3 gain settings/item. Manipulation check inside: if λ̂ doesn't move under scheduling → stop, no further spend.

Total pilot cost: **≈ 0.0038 T4-h (free-tier GPU)** — fourth in the sprint's cost order, behind R7/R5/R3.

## 4. Mathematical license

**License:** [THEOREM-level in random nets] Poole et al. 2016 — signal-propagation depth scales are maximal at criticality (ordered/chaotic phase boundary). The EOC translation: λ̂(x) measures per-item distance from criticality across depth; scheduling gain to push λ̂ → 0 maximizes the item's effective propagation depth, hence representational expressivity at decision time.

**Quantitative prediction:** gain concentrates on items with |λ̂_baseline| ≫ 0 (far-from-critical); items already near λ̂ ≈ 0 gain ~0. Formally: Spearman(gain, |λ̂_baseline|) > 0, one-sided p < 0.05, AND scheduled-g ΔM > best-fixed-g ΔM. **The |λ̂|-dose-response is non-negotiable** — it is the signature no alternative predicts:
- fixed-temperature predicts *uniform* effects (no dose-response);
- PWAR predicts *entropy-dispersion* response (different diagnostic) — mutually discriminating on the same 60 items, which is why PWAR piggybacks.

**Breaking point (sharpest in the sprint):** scheduled-g ΔM ≤ best-fixed-g ΔM, **or** gain uncorrelated with |λ̂_baseline| (Spearman p ≥ 0.1) → the criticality story is decorative → **KILL**.

**Honest audit of the license (adversarial pass):**
- *Gap 1 — trainability → decisions.* Poole's theorem is about signal propagation at initialization (trainability/expressivity), not decision accuracy under inference-time gain modulation. The link is analogical — one inferential step beyond the theorem. [CONJECTURE] Mitigation: the dose-response signature is exactly the empirical bridge; if the analogy is false, the signature won't appear, and the breaking point fires. The license licenses the *test*, not the conclusion.
- *Gap 2 — temperature confound.* Modulating τ directly sharpens/softens attention; any gain could be plain temperature effect. Mitigation is structural: uniform gain across |λ̂_baseline| = temperature story = KILL by the breaking point. The design anticipates its own confound.
- *Gap 3 — power.* If |λ̂_baseline| has no variance across the 60 items, the Spearman test is powerless. **Hardening (new):** the pre-reg must gate on Var(|λ̂_baseline|) > 0 (pre-registered floor) before the dose-response test; no variance → **Underdetermined** (not KILL — never kill on a powerless test).
- *Gap 4 — strawman baseline.* "Best fixed gain" must be a real grid, explicitly pre-registered, not a single arbitrary τ. **Hardening (new):** fixed-gain grid specified in the skeleton.

**License verdict:** HOLDS. Theorem-anchored, quantitative, mutually discriminating against the two nearest alternatives, with the sharpest breaking point in the sprint and both gaps converted into pre-registered gates.

---

## Erratum (append-only — appended 2026-09-26; correction claimed but never written at LOG-4354, repaired per LOG-4356 F9)

**Correction to §4 (Mathematical license) above:** §4 states "Poole et al. 2016 — signal-propagation depth scales are maximal at criticality (ordered/chaotic phase boundary)." That attribution is wrong. The "signal-propagation depth scales are maximal at criticality" theorem belongs to **Schoenholz et al. 2017 (arXiv:1611.01232)**; **Poole et al. 2016 (arXiv:1606.05340)** is cited only for the χ₁/order-to-chaos framework (verified at Stage −1 by full-text search of Poole 2016: zero occurrences of "depth scale"). The original §4 text above is left unedited — this erratum carries the correction by append-only amendment. The R4 full pre-registration draft attributes correctly in its §1.1. No signed artifact was touched.

## 5. Summit filter

Does it move a frozen model toward autonomous inference-time cognition? **Partially — passes as mechanism science.** As specified, EOC is externally scheduled (we compute λ̂, we set τ) — not autonomous. But it is *inference-time control of the model's own dynamics*, and the summit-directional extension is explicit: the model self-estimates λ̂ and self-schedules gain (a closed self-regulation loop — Phase 4 material). It also attacks the verifier bottleneck obliquely: λ̂ is a *label-free, per-item diagnostic* — exactly the class of signal the program's E-step needs. Verdict: GO as Phase-3 mechanism with a named autonomous extension; it is not itself the autonomy result and must never be described as such.

## 6. Graveyard filter

- **Static cones/geometry (EXP077, killed (a)):** no vector added, no direction, no candidate pool — global gain scheduling is untouched by any killed experiment. CLEAR.
- **Layer-20 readouts (EXP091):** no readout claim. CLEAR.
- **QK null-space (G1):** G1 killed a *weight-subspace energy* story; EOC modulates *runtime dynamics* (τ scalars), a different object. CLEAR.
- **Label-informed "wins" (bridge demotion, LOG-204):** λ̂ is computed from two nearby forward passes — label-free by construction. Law #7 clean. CLEAR.
- **SAH (S3-4):** distinct — SAH controls *intervention* α with hysteresis; EOC controls *intrinsic* gain. Different object, no overlap. CLEAR.

## Verdict: GO

R4 EOC passes the Law #15 gate: precise question, decision with teeth, cheapest falsifier costed at 0.0038 T4-h, theorem-anchored license with a quantitative prediction and the sprint's sharpest breaking point, summit-relevant as mechanism science, and clear of the entire graveyard. Two hardenings required in pre-registration: (a) |λ̂_baseline| variance gate → Underdetermined (not KILL) if absent; (b) explicit best-fixed-gain grid. Pre-registration skeleton drafted as companion file — DRAFT, UNSIGNED; signing is a separate lane (needs Law #14 + CEO GPU clearance, sequenced behind the K2→EXP083→EXP084→EXP086-B→EXP088→EXP087 queue).
