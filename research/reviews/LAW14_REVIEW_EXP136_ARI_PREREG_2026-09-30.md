# Law #14 Independent Review: B4/ARI Pre-registration Draft

**Artifact under review:** `research/prereg/EXP136_PREREG_ARI_2026-09-30.md` (exact file, DRAFT state)
**Review lane:** LOG-4849 (pre-assigned by the CEO). **Reviewer independence:** this lane neither drafted (LOG-4848) nor repaired the artifact.
**Verdict:** **SIGN-WITH-FIXES** — two required fixes (F1, F2), two advisories (A1, A2). The hypothesis, decision-table structure, worth-it gate, and non-resurrection audit are sound; the statistical specification has one direction defect and the delivery control has one coverage gap.

---

## 1. Decision table — PASS with F1

The four branches (CONTINUE / KILL / HELD / RUN-INVALID) with precedence RUN-INVALID > HELD > KILL > CONTINUE are exact, exhaustive, and mechanically applicable — **conditional on F1**. Every data configuration resolves to exactly one branch:

- T1 or T2 significant (p ≤ 0.05) with C flat → CONTINUE (routing-specific).
- ΔM_T1 = ΔM_T2 = 0 with (h) PASS → KILL.
- T1/T2 significant with C significant → HELD (unattributable); T1/T2 ΔM > 0 sub-significant → HELD.
- Any §3.6 guard trips → RUN-INVALID (precedence voids all else).

The "C moves but T1/T2 flat" configuration resolves to KILL under the stated precedence (neither HELD branch fires; KILL's ΔM = 0 condition holds). This is correct for the routing-specific hypothesis — if the undirected control moves decisions but the directed arms do not, routing is not the lever — but the draft does not state it; see A2.

## 2. The (h) control — PASS with F2

The (h) control (§3.4) directly observes the intervention's effect on the causal variable itself: post-softmax L20 attention weights with the span ablated (max_h Σ_span < 1e-6), renormalization (|Σw − 1| < 1e-5), finiteness, and a non-no-op assert (L1 > 0.01 vs base). This is genuinely stronger than the residual-stream (h) precedent (EXP131/EXP133), which inferred delivery through a downstream tap. The control cannot pass while the T2 hook fails to reach the attention computation.

**However — F2:** the control registers and verifies **only the T2 (ablate) hook**. T1's 3× span-boost is never verified. If base span attention mass is ~0, T1 computes 3×0 = 0 — a no-op — and a KILL resting on ΔM_T1 = 0 would be invalid (the hypothesis "T1 doesn't steer" was never tested; only "our T1 implementation changed nothing" was observed). The KILL bar requires both arms delivered; only one is proven.

## 3. The n = 60 correction — PASS (numbers independently recomputed)

The drafter's §0.1 correction is mathematically sound; every number recomputed exact in this review:

- n = 10: one-sided McNemar p ≤ 0.05 requires b ≥ 5, c = 0 (P(Bin(5,½) ≥ 5) = 1/32 = 0.03125); b = 4, c = 0 gives 1/16 = 0.0625 > 0.05. The sprint's "≥ 2/10" prediction cannot reach its own bar. Confirmed.
- False-KILL risk at 20% true rate, n = 10: 0.8^10 ≈ 0.107 ≈ 11%. Confirmed.
- n = 60, b = 10, c = 2: P(Bin(12,½) ≥ 10) = 79/4096 ≈ 0.0193 ≤ 0.05. The CONTINUE bar is reachable at realistic effect sizes. Confirmed.
- KILL stringency: 0.9^120 ≈ 3.23×10^{-6} under a 10% true flip rate — the bar bites, not vacuous. Confirmed.

## 4. Scope fence — PASS

§1.2 correctly fences B4 as an **operator-efficacy** probe, not a label-free or autonomous-steering test. The span annotations are prompt-structure metadata (entity location), not answer labels; the endpoint is argmax over the vocabulary with labels used nowhere (§3.1, Law #7). A CONTINUE licenses "attention reweighting moves frozen decisions" and motivates routing-*discovery* work; the draft explicitly withholds any autonomous-steering reading. The fence is correctly drawn and a CONTINUE cannot be honestly misread as autonomous steering under it.

## 5. Breaking points — PASS with F2

Guards (a)–(g) cover: Δθ=0 weight integrity (a), eager-backend non-perturbation via 60/60 B-decision agreement against the archived EXP094 vector (b), bench/span pins with the >6-exclusion trip (c), hook delivery (d), per-forward renormalization and finiteness (e), the forward-budget audit 4n + 1 = 241 (f), and clean completion (g). Law #7 is covered by construction (labels touch neither intervention nor endpoint). The n = 60 − e parameterization is present. The one gap is F2 (T1 delivery); no other trip is missing.

## 6. Worth-it gate and non-resurrection — PASS

All 7 Law #15 points are present and substantive. The non-resurrection audit (§6) was independently re-verified by this lane via full-log grep:

- No execution has ever intervened on attention weights. The log's attention hits are: read-only measurement hooks (S6-3b/3c/EXP102, "read-only" verbatim), an unexecuted Layer-8 mechanistic hypothesis, R5/EAR (different question — circuit-addressed scratch memory, killed), and the sprint dossier's own §7.5(e) listing attention temperature scaling as unexplored. Law #4 clean.
- S6's breaking point (iv) — "no fifth externally-computed attention-gate variant" (LOG-890/920/968) — fences attention-as-a-*gate* (a measurement conditioning residual injection), not attention-as-the-*intervention-target*. The draft's distinction is accurate; the fence does not cover B4.
- G1 killed a QK-subspace theorem (a claim about past failures' geometry), not an intervention. EXP131/133 killed residual injection at L20 — B4 holds the site constant and varies the operator, the licensed comparison the program has never run. EXP105 masked logits (readout-side), not attention. All differentiations hold.

## 7. Required fixes

### F1 — McNemar direction mismatch (statistical defect)

The draft specifies McNemar one-sided with H1: b > c (arm *improves* over base) uniformly across arms (§3.3). But:

- **T2 (span-ablate)** is predicted to *worsen* accuracy — §0.2: "probed bidirectionally." A T2 effect in its predicted direction (e.g., b = 2, c = 10) yields p = 0.9968 under H1: b > c (independently recomputed) — the CONTINUE bar **cannot fire on T2's own prediction**.
- **C (uniform control)** has no directional prediction; it guards against "any perturbation" effects. A systematic C *worsening* (c >> b) would not trip the HELD bar's "C: p ≤ 0.05" conjunct under the one-sided improvement test, allowing a CONTINUE on an unattributable effect.
- Correlated: systematic T1 *worsening* (c >> b) resolves to HELD (sub-significant) rather than CONTINUE, though systematic worsening proves steerability as surely as improvement.

**Fix:** specify direction-appropriate tests — T1: one-sided b > c; T2: one-sided c > b (or two-sided); C: two-sided for the attribution conjunct — with the choice justified in §3.3, and update the §5.6 quantitative prediction to cover both directions. (Two-sided at the b = 10, c = 2 example gives p ≈ 0.0386, still ≤ 0.05 — the bar remains reachable.)

### F2 — T1 delivery unverified (coverage gap in (h))

As §2 above: extend the (h) control to register the T1 hook and assert non-trivial boost delivery (e.g., post-boost span mass or L1 distance from base above a pre-registered threshold), or add a guard requiring base span attention mass above a threshold for T1's KILL contribution to be licensed. The KILL bar's "both arms" condition is currently half-proven.

## 8. Advisories (non-blocking)

- **A1:** The (h) control observes modified *weights* but not that they propagate to the module *output* (a hook modifying a detached copy would pass (h) yet leave decisions at base — a false-KILL path). Low risk under the standard forward-hook pattern, and guard (e) provides per-forward sanity; consider asserting L20 output differs from base on the probe forward. Cheap insurance, not required.
- **A2:** State explicitly that "C significant, T1/T2 flat" resolves to KILL (per precedence), to prevent future misreading of the decision table.

## Disposition

**SIGN-WITH-FIXES.** Apply F1 and F2, then independent fix-verification against this review, then the CEO launch decision. The program's first attention-intervention axis is well-posed; the two fixes are mechanical, not architectural.

---

*Review: independent Law #14 lane, LOG-4849. $0 CPU, paper only. No repairs, no execution.*
