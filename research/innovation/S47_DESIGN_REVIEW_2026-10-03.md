# Law #14 Review — S4-7 (J3) Spectral Phase Transition Design (S47_DESIGN_2026-10-03.md)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design)
**Date:** 2026-10-03
**Document reviewed:** `~/workspace/SCBI/research/innovation/S47_DESIGN_2026-10-03.md` (exact file)
**Design-lane verdict under review:** CONDITIONAL RUN
**Review verdict:** **APPROVE-WITH-CONDITIONS** (conditions §9; execution additionally needs CEO approval per the design's own launch chain)

This review is of the design document only. It licenses nothing to run, mints no experiment number, and touches no signed artifact.

---

## 0. Reading note

I read the full design, plus: `TESTA_CALIBRATION_2026-10-03.md` (full), LOG-4888 (EXP140 Stage-1 record), LOG-4890 (EXP141 Stage-1 record), LOG-4680 (EXP125 kill record, relevant to the audit), backlog row 25, and the J3 formal sketch in `research/innovation/S4_I1_FORMALIZATION_AND_J_TIER_2026-09-24.md` §§J3/J4 (lines 208–270). The three prior-art items were not independently verified this lane (arXiv API was rate-limited at design time and remains so); they are assessed as REPORTED, consistent with the design's labeling.

---

## 1. The MP null — SOUND AS A COUNTING RULE, PERMUTATION TEST IS THE REAL INSTRUMENT

**Finding:** The design's framing is correct and I find no MP-theatre. The Marchenko–Pastur construction serves exactly one function: a *pre-registered, fixed counting rule* that converts each layer's spectrum into an integer s_{i,l}. The falsification instrument is the label permutation test on Δ_s, which makes no assumption about MP exactness — it tests whether the *grouping* (correct vs failed) explains the counts. Under the permutation null, any systematic bias in the counting rule (bulk misfit, σ̂² error, anisotropy) applies equally to both groups and cancels. This is the right division of labor, and the design states it explicitly (§4.1: "the falsification does not come from 'is MP exactly right' but from the label permutation test").

- **Is σ̂² estimation adequately pinned?** It is *deferred*, not pinned: §1 says "estimation method pinned in pre-reg — e.g., σ̂² fit from the bulk median against the theoretical MP median at γ_i." Deferral is acceptable at the design stage (this document is the worth-it gate, not the protocol), and §9.2 already flags the bulk-fit diagnostic requirement. Condition C1 makes the pinning mandatory in the pre-reg: the estimator, the bulk-fit diagnostic, and the diagnostic's reporting (not binding) must be fixed before any data is seen.

---

## 2. The max-over-layers statistic — PRE-REGISTERED, PERMUTATION TEST VALID

**Finding:** s_i := max_l s_{i,l} is defined as the per-item statistic in §1, *before* the test is specified in §2. The permutation test shuffles only the correct/failed labels; the max-over-layers transformation is applied identically to every item in every permutation (it is a fixed per-item function of the data, computed once). Therefore there is no multiple-comparisons inflation: the max cannot "find" a favorable layer after seeing labels, because the labels are what get permuted and the max is label-blind. The permutation test is valid for this statistic.

- The residual concern is *sensitivity*, not validity: max over 24 layers can be driven by a noisy outlier layer, which costs power. That is a design choice with a stated cost (the V2 per-layer diagnostic, reported not binding, gives the layer localization), not a defect. No condition needed, but the pre-reg should keep the max-inside-permutation construction explicit (one sentence).

---

## 3. The one-sided construction — KILLS ON WRONG DIRECTION, AS CLAIMED

**Finding:** I verified the logic. Licensed direction Δ_s > 0; one-sided p = P(perm Δ_s ≥ obs Δ_s); KILL iff p ≥ 0.05. If the true effect is wrong-direction and large (obs Δ_s very negative), then P(perm Δ_s ≥ obs Δ_s) ≈ 1 ≥ 0.05 → KILL. If the effect is null, p is uniform and KILL fires with probability 0.95 — which is the design's intent (the backlog's bar is "permutation p ≥ 0.05 → KILL the observational claim"). The construction does not merely fail to CONTINUE on wrong-direction; it actively KILLs. The design's claim (§1, §4.2) holds exactly as stated. The bias-coherence counter-argument (§1, §9.3) is therefore genuinely collected by the instrument, not rhetorically absorbed.

---

## 4. Non-resurrection vs killed static-geometry — CLEAN, WITH THE SHARP EDGE HONESTLY FLAGGED

**Finding:** The killed static-geometry lanes (EXP077, EXP092/093/094, S5-1–S5-4, S6, EXP095/096) died on *causal* claims about *pre-chosen* directions that were injected. S4-7's Stage-1 claim is *observational* and *data-driven*: the PCs are computed from each item's own activations, never pre-registered; nothing is injected; no causal claim is made. The RMT observable is not "geometry in the killed sense" — it is a measurement, not a manipulation.

- **The sharp edge is handled correctly.** §6(i) states plainly that the *intervention* stage (amplify the top-signal-PC at l_c) is directional manipulation by another name, and refuses to launder it: the intervention is sequenced behind the observational license, gets its own worth-it gate and experiment number, and the Law #14 reviewer of that gate is explicitly tasked with ruling on whether "data-driven spectral amplification" is distinct from the killed directional program. Nothing about intervention is pre-licensed. This is the correct posture — the audit stays honest by deferring the hard question to the gate where it belongs, rather than answering it prematurely in either direction.
- Remaining lines (ii)–(viii): all substantive. (ii) EXP135's killer cannot transfer (live pilot, no records computation; the Law #2 exemption is vacuous here and stated as such). (vi) EXP140's G3-null does not transfer (different object; re-tested from scratch). (vii) EXP141's kill was about the absence of a *self-model*; S4-7 asks whether the *computation* has a spectral signature — a question EXP141 never touched. Clean.

---

## 5. The bars — JOINTLY NON-VACUOUS; Δ_s ≥ 2 IS HONEST; CONTINUE SCOPE IS RIGHT

**Finding:** KILL (p ≥ 0.05) / CONTINUE (p < 0.05 ∧ Δ_s ≥ 2) / HELD (p < 0.05 ∧ Δ_s < 2). Every (p, Δ_s) region maps to exactly one branch under KILL > CONTINUE > HELD. No PIVOT is licensed by the backlog row and none is invented — correct restraint (contrast S4-5, where PIVOT had to be demoted, and S4-6, where it was reachable; here the row simply has no PIVOT).

- **Δ_s ≥ 2 is the backlog row's Law #15 prediction** (J3 sketch: "signal-count(failed) < signal-count(correct) − 2 (medians)"), verified verbatim in the sketch (line ~222). It is pre-registered, not chosen post-hoc, and on integer counts with n=60 it is a real magnitude bar, not a gimme.
- **CONTINUE licenses only a new worth-it gate** — the right scope. An observational spectral difference is not a capability claim; the design refuses to let it become one. Correct.

---

## 6. The $0 screen — COSTING CREDIBLE; VALIDITY GATES TO PIN

**Finding:** 60 forward passes with `output_hidden_states=True` + 1440 Gram eigendecompositions (n_i × n_i, n_i ≈ 100) at ~1h CPU and ~590MB storage is credible arithmetic against the EXP139 (60/60 passes) and EXP140 (240+240 in ~1h) precedents. The eigendecomposition cost is genuinely negligible next to the forwards.

- **Validity gates to pin in pre-reg (condition C4):** determinism check, backbone pre/post hash (Δθ=0), bench hash, 60/60 pass completion — the standard EXP139/140/141 gate kit. The design cites the pins but does not enumerate the gates; the pre-reg must.
- **The n_i guard (§9.4) is well-conceived:** if prompts are too short for stable spectra, the pilot reports HELD with reason rather than a spurious KILL. This is a measurement-validity guard, pre-registered, and it must appear in the pre-reg (condition C2).

---

## 7. Prior art — ASSESSED AS REPORTED; HONEST NEGATIVE CREDITED

**Finding:**
- **Martin & Mahoney (RMT weight spectra / WeightWatcher):** the characterization (MP bulk + signal outliers in trained weight matrices tracking training quality) matches the known program. REPORTED, not independently verified this lane.
- **Neural collapse (Papyan, Han & Donoho 2020):** the characterization (terminal-phase simplex ETF, within-class covariance → 0) matches the known result. REPORTED, not independently verified this lane.
- **Intrinsic dimensionality (Aghajanyan et al.):** the characterization (low intrinsic dimension of the fine-tuning parameter manifold) matches the known result. REPORTED, not independently verified this lane.
- **The honest negative** (no per-item inference-time MP prior art found) is stated as a search result with the update rule ("if the pre-reg-stage full-text search finds it, the novelty read updates"). I cannot exhaustively verify a negative; it is honestly labeled and the update rule is correct. Condition C3 requires the full-text verification at pre-reg stage, as the design already flags.

---

## 8. Verdict on CONDITIONAL RUN — CONFIRMED (NOT BUSYWORK)

**Finding:** DO NOT RUN would require a structural flaw or an uninformative test. Neither holds. The honest prior is LOW — four internal-signal failures point the same way — but the observable is a genuinely different family from all four dead signals (computation-global spectral structure vs decision-local sharpness vs trajectory surprise vs metacognitive judgment), the test costs ~1h of $0 CPU, and it closes the last J-tier line. A null result here is itself the deliverable: it would establish that *no* internal correctness-signed signal exists on this bench family across five distinct families — margin, free energy, self-model, honesty-report, spectrum — which is a boundary result with summit relevance (it constrains where the missing ingredient can be: not in the frozen model's internals as probed, pointing to architecture per the Percepta Spotlight framing). That is not busywork; it is the worth-it gate functioning as designed.

---

## 9. Verdict: APPROVE-WITH-CONDITIONS

Stage-1 CPU observational pilot may run after these conditions are closed in the pre-registration draft, plus CEO approval per the design's launch chain:

- **C1 — Pin the σ̂² estimator + bulk-fit diagnostic.** The pre-reg must fix the noise-variance estimation method (e.g., bulk-median fit against the theoretical MP median at γ_i) and a bulk-fit diagnostic (reported, not binding) before any data is seen. The max-inside-permutation construction must be stated explicitly (one sentence).
- **C2 — n_i measurement-validity guard.** The pre-reg must report the n_i distribution and state the rule: if n_i is too small for stable spectra, the pilot reports HELD with reason rather than a spurious KILL.
- **C3 — Prior-art full-text verification.** Martin & Mahoney, neural collapse, intrinsic dimensionality at full-text level, as the design already flags. Nothing is marked verified that is not.
- **C4 — Validity gates.** Determinism check, backbone pre/post hash (Δθ=0), bench hash, 60/60 pass completion — the standard kit.
- **C5 (minor) — Citation fix.** §0 cites "LOG-4889/LOG-4879" for the Friday cull; the Friday cull is LOG-4879 (LOG-4889 is the S4-6 pre-reg sign). Correct the citation.

**What this review does NOT do:** it does not license execution (CEO approval still required), mint an experiment number, or approve any intervention (the spectral intervention needs its own worth-it gate + Law #14-signed pre-registration + CEO GPU clearance + founder Kaggle slot — nothing is pre-licensed here).

---

## 10. Summary

The S4-7 design is honest, falsification-first, and worth executing conditionally. The MP construction is a principled pre-registered counting rule with the label permutation test as the real falsification instrument (no MP-theatre); the max-over-layers statistic is pre-registered and the permutation test is valid for it; the one-sided construction genuinely kills on wrong-direction effects; the non-resurrection audit is clean with the intervention sharp edge honestly deferred to its own gate; the bars are jointly non-vacuous with the backlog's Δ_s ≥ 2 magnitude bar; the $0 costing is credible; the prior art is honestly labeled with an update rule for the negative. Five conditions (C1–C5) must be closed in the pre-registration draft before Stage 1 runs; none is a reason to reject. The honest prior is LOW after four internal-signal failures, but a fifth $0 observational test of a genuinely different family is the worth-it gate working as designed, not busywork — and a null would close the last J-tier line with a boundary result of summit relevance.
