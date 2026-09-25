# EXP083 Protocol Specification: R1 RCPA — Relational Cross-Position Amplification

**PRE-REGISTRATION SIGNED — Law #14 final SIGN recorded LOG-257. Runners may be built from this document only within the licensed scope (§13: implementation-bundle stage — evaluator test suite + startup smoke test; NO GPU execution).**

**Status:** SIGNED (pre-registration; Law #14 review LOG-251 verdict SIGN-WITH-FIXES — all 12 findings discharged, §12; re-review LOG-253 verdict SIGN-WITH-FIXES — all 5 fixes R1–R5 discharged, §14; final sign-off LOG-255 verdict SIGN-WITH-FIXES — M1–M3 clarifications applied, §15; **final Law #14 SIGN recorded LOG-257**)
**Date:** 2026-09-24
**Author role:** Research Lead (standing), drafting under CEO mandate
**Experiment number:** EXP083 (next free; EXP082 minted LOG-182, executed LOG-217 — verified unminted at drafting)
**Predecessor experiments:** EXP065/066 (boundary series), EXP077 (cone-vs-line — the null under differential test), K1 (readout-tilt falsification), EXP070 (oracle ceiling), G1 (QK-null-space kill)
**Source idea:** `research/proposals/AMBITION_SPRINT_SYNTHESIS_2026-09-24.md` §R1 (ambition sprint LOG-250; promotion recommendation: R1 → QUEUED)
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `experiments/protocols/STATISTICAL_PROTOCOL_V02.md`, `research/proposals/AMBITION_SPRINT_EXPDESIGN_2026-09-24.md` (§A.2 kill-pilot template, §A.3 negative-control battery, §A.4 pre-registration skeleton — the governing design law), `research/MATH_STANDARDS_CHARTER.md` (binding M1–M8), Law #7 audit (LOG-197) and bridge demotion (LOG-204)
**Execution rule:** Strictly confirmatory. No direction, α, seed, gate, threshold, position rule, or verdict-table change after execution begins without a new pre-registration. **Changed design = the next free number at pre-registration time.**
**Queue position:** behind K2 on the user's Kaggle node — GPU-sequencing only (F11, §10). R1 may be pre-registered before K2 executes.

---

## 0. Law #15 packet

**Q1 (precise question):** EXP077 killed *within-position* static injection at layer 20 (ΔM=0, p=1.0 everywhere). Is the transferable signal **relational across positions** — does a per-instance cross-position vector r = h_L(ans_pos) − h_L(q_pos), injected at the final layer's answer position, move decisions where every within-position direction failed? Construction uses positions only, zero labels (F4).

**Q2 (decision it changes):** **KILL** the relational-readout family if r̂ moves decisions no more than a matched-norm random direction (verdict table §8); **CONTINUE** to a powered pilot only if r̂ flips wrong→right at ≥ δ_min = 0.05 above control with one-sided McNemar p ≤ 0.05. **HELD** (never CONTINUE) on straddle or sub-claim signal. A RE-SKIN KILL fires before the flip test if r̂ is near-static across items (F5; on a validated apparatus — verdict-precedence order, §8).

**Q3 (cheapest test and pass count):** 3 forward passes/item (clean read for r + inject r̂ + inject random) × 60 items = 180 + ≤12 startup smoke + $0 identity arm (archive-validated) = **≤192 passes ≈ 0.0024 T4-h**. The 150-pass kill-pilot ceiling is exceeded; the CEO tier exception is pre-committed in this protocol (F3-TIER-EXCEPTION, §6). Verified on CPU 2026-09-24: the EXP077 archive contains no per-position h_L states (137 KB vector file cannot hold 60 items × 2 positions × 1024 dims; instance records carry no positional data), so the clean-read pass cannot be $0'd. No cheaper test exists: r must be read before it can be injected.

**Q4 (mathematical license):** [CONJECTURE] If the decision-relevant feature is relational — the readout depends on cross-position comparisons with relational gradient ∇_rel — then a per-instance relational vector r̂ at the output side carries decision-moving content that within-position static directions lack. **Quantitative prediction:** Δ = flip-rate(r̂) − flip-rate(random) ≥ δ_min = 0.05, one-sided McNemar p ≤ 0.05 in the r̂ direction. **Breaking point:** the §8 verdict table — two-sided 95% Tango CI for Δ entirely below +0.05 (KILL_gross), or the b=c=0 flat outcome at observed N_final (KILL_flat functional bar — canonical N_final=57 → one-sided 95% Tango upper 0.045315 < 0.05, R1), or mean pairwise cos(r̂_i, r̂_j) > 0.5 (RE-SKIN KILL — on a validated apparatus; verdict-precedence order, §8). The EXP077-null "theorem" sketch is demoted to [CONJECTURE] with its missing premise stated (F8, §1.1).

---

## 1. Research question and hypotheses

$$\boxed{\textbf{Does a per-instance cross-position vector at the output side move decisions where within-position static injection cannot?}}$$

**[HYPOTHESIS] H_rel:** The transferable signal is relational across positions. r = h_L(ans_pos) − h_L(q_pos) carries decision-moving content; injecting α·r̂ at h_L(ans_pos) flips wrong→right strictly more than a matched-norm random direction.

**[HYPOTHESIS] H_null (standing boundary):** No injected direction at the output side moves decisions beyond norm-matched noise. r̂ ≤ random on flips; the boundary verdict (raw geometric similarity without causal transfer) extends to relational constructions.

### 1.1 The EXP077 differential — [CONJECTURE], not [THEOREM] (F8)

The sprint packet claimed R1 "predicts EXP077's null as a theorem." That claim is **demoted**. The sketch argued: if the readout depends on cross-position comparisons with relational gradient ∇_rel, then any within-position static direction v satisfies ⟨v, ∇_rel⟩ ≈ 0 *to first order*. This is false as stated — a within-position injection v at the answer position changes the relational feature d = h_a − h_q by +v, with first-order effect ⟨∇_rel, v⟩, which vanishes only under the **additional premise** that the static v is orthogonal to the instance's relational gradient (or the statistical premise that instance-varying ∇_rel is isotropic around fixed v). That premise is precisely what is at issue; the sketch assumed its conclusion.

**[CONJECTURE] C_rel (explicit premises):** *If* (P1) the decision-relevant feature is the cross-position difference d = h_a − h_q, *and* (P2) instance relational gradients ∇_rel are isotropic around any fixed within-position direction v (or orthogonal to it), *then* within-position static injection has zero first-order decision effect — EXP077's ΔM=0/p=1.0 follows as a structural consequence. The candidate does not need this conjecture: the differential prediction (r̂ moves / random must not) is testable as stated.

**Layer confound (pre-registered, F8):** EXP077 injected at **layer 20**; R1 injects at **h_L (final layer, index 23)**. Two axes change at once (relational structure × layer). A positive R1 result does **not** isolate which axis mattered. On CONTINUE, the powered pilot **must** carry a static-direction-at-h_L arm (the EXP077-style arm transplanted to the final layer) to disentangle layer from relationality. Not required in the kill pilot — kill pilots kill; interpretation is priced into CONTINUE (F10).

---

## 2. Frozen model and SHA-256 guard

- **Model / tokenizer (in-scope):** `EleutherAI/pythia-410m` (the model on which the boundary null's 410m leg was established, EXP066/077).
- **Architecture [FACT]:** GPT-NeoX; d = 1024; 24 layers.
- **Intervention site:** final-layer residual stream h_L (layer index 23, 0-indexed), at ans_pos. Intervention h_L(ans_pos) ← h_L(ans_pos) + α·u via forward hook; u unit-norm; α carries all scale.
- **α: pinned at 1.0** (F2). Anchored to EXP077's α=1 offset precedent on the same probe family (r̂ is unit-norm, so α is directly the injection norm). **A null at α=1.0 is a KILL, not a license to scan α.** Any α variation is a new Law #15 packet.
- **Expected SHA-256** (pre and post, over all parameters):
  `4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd`
  (carried from EXP067 §2 — same model `EleutherAI/pythia-410m`; sanity check only).
  **Guard procedure:** SHA-256 over `state_dict()` tensors (sorted keys, CPU, float32 bytes) pre/post run; binding guard is the runtime pre/post match. The pre-run SHA-256 is additionally compared against the expected pinned hash above; mismatch → INVALID (§8, R3) — the binding pre/post match alone would let a wrong-model download slip through. $\boxed{\Delta\theta \equiv 0}$ non-negotiable (Law #6). No backward pass exists anywhere.

---

## 3. Probe set, baseline license, and position rule

### 3.1 Probe set
The pinned 60-item EXP077-derived suite (Planetary/Elemental 2-hop/3-hop, EXP065/066-identical construction, ported verbatim — Law #9: no new benchmark construction). Prompt template (structural, pinned verbatim from the EXP077 runner):
`Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:`
(and the three sibling templates: "is lower than" / 3-hop variants — all share the `...? Answer:` terminal structure).

### 3.2 Baseline license (F7)
Baseline correctness = the archived `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` C1 (no-intervention) decisions. Archived C1 accuracy = **60.00%** (headroom gate [40%, 70%]: PASS, verified on CPU 2026-09-24). The **identity arm** (α=0, no hook) must reproduce the archived C1 decisions **bit-for-bit at $0** — this is the apparatus check. Identity/arm-archive mismatch → **INVALID session** (apparatus failure), no verdict about R1.

### 3.3 Position-identification rule (F4) — structural, label-free
- **ans_pos** = T−1, the final prompt token (the `:` of the terminal `Answer:`).
- **q_pos** = the token index of the `?` terminating the question span: search the prompt **string** for `? Answer:` (M3 — substring search operates on text, not token IDs), take the character offset of the `?`, and map it to its token index (no labels, no metadata).
- **Law #7 prohibition (pre-registered):** no position-selection rule may inspect correctness labels, target/foil strings, or benchmark metadata. Positions are template structure — known a priori. The construction touches only positions; the bridge (label-informed) is disqualified as a mechanism arm (LOG-204) and appears nowhere in this protocol.

---

## 4. Formal construction

**Notation (M1.1):** In *this* document, h_L(x, p) ∈ ℝ¹⁰²⁴ is the final-layer residual-stream hidden state for item x at position p, from a clean forward pass (no intervention).

**[DEFINITION] Relational vector:** for item i,
$$r_i = h_L(x_i, \mathrm{ans\_pos}_i) - h_L(x_i, \mathrm{q\_pos}_i), \qquad \hat{r}_i = r_i / \|r_i\|_2.$$
[M4.1 shape check:] h_L, r_i, r̂_i ∈ ℝ¹⁰²⁴; r̂_i unit-norm. [M4.2 space check:] construction space = final-layer residual stream; application space = final-layer residual stream at ans_pos. **Same space — no transfer assumption needed.** [M4.4:] α=1.0 carries all scale.

**Arms (kill pilot):**
- **A_r (candidate):** h_L(ans_pos) ← h_L(ans_pos) + 1.0·r̂_i.
- **A_g (null control):** h_L(ans_pos) ← h_L(ans_pos) + 1.0·ĝ_i, where ĝ_i is a unit-norm isotropic Gaussian direction drawn per item from a dedicated **torch.Generator** (`torch.randn(1024, generator=g_i)` with `g_i.manual_seed(20260924 + i)`; master seed S0 = 20260924). **torch is the sole ĝ_i generator library (R5)** — numpy is not used for ĝ_i. Greedy decoding. Matched norm by construction (‖ĝ_i‖₂ = 1 = ‖r̂_i‖₂).
- **A_0 (identity, $0):** no intervention — archive-validation arm (§3.2). **$0 mechanism (R4):** A_0 is not a separate pass — the greedy-decoded decisions from the clean-read pass (§6) **constitute** the A_0 identity arm ($0 by reuse); the §3.2 archive bit-for-bit comparison is computed on those decisions. No additional passes.

**Endpoint (F7):** outcome(i, arm) = 1 iff item i was **wrong at baseline** (archived C1) **and right under the arm**, else 0. Items right at baseline are structural zeros — handled, not subsetted. McNemar's b/c count discordant (A_r-only vs A_g-only) wrong→right flips. Δ = flip-rate(A_r) − flip-rate(A_g).

---

## 5. Guards (F5, F6)

**G-norm (F6):** norm-floor guard. Floor = the **5th percentile of ‖r_i‖ over the 60 items**, computed $0 on CPU from the clean-read states, by **linear interpolation (numpy.percentile default, type 7; position (n−1)·p = 59·0.05 = 2.95 between sorted ‖r‖ values)** — this method is pinned (R2); nearest-rank interpolation would give N_final=58 and is rejected. Items with ‖r_i‖ **strictly below** the floor (<, not ≤) are **excluded before the flip test**; the exclusion count and N_final are reported. **N_final is deterministic: exactly 3 items fall strictly below the interpolated floor → N_final = 57** (verified arithmetically 2026-09-24). Tie edge case: if sorted ‖r‖ values tie at the interpolation point, N_final = 58 — the KILL_flat functional bar (§8) applies at the observed N_final either way, and still fires (0.044568 < 0.05). Rationale: near-zero r normalizes noise into the "relational" arm, biasing toward a mushy null. Exclusion floors are §A.4 guards, not post-hoc trimming.

**G-static (F5):** static-ness check, computed $0 on CPU **after** G-norm exclusion and **before** the flip arms run. Statistic: mean pairwise cos(r̂_i, r̂_j) over included items (n(n−1)/2 pairs). **Chance anchor:** for random unit vectors in d=1024, pairwise cos ∼ N(0, 1/1024) — |cos| ≳ 0.1 is already far above chance. **Bar: mean pairwise cos > 0.5 → RE-SKIN KILL** (dominant common component — e.g., a systematic position-embedding difference between q_pos and ans_pos — making r̂ a static direction in disguise; the killed static family (a) already covers it). If G-static fires (on a validated apparatus — verdict-precedence order, §8), the injection arms are **not run** (GPU saved); the session ends at 60 clean-read + 9 smoke passes with verdict RE-SKIN KILL.

**G-curve (F9, report-only in kill pilot):** $0 diagnostic **mean⟨r̂_i, ĥ_a,i⟩** over included items (the rescaling fraction — r contains +h_a, so injection partially rescales h_a). Reported with the pilot. **Interpretation rule (pre-registered):** if the verdict is CONTINUE *and* the rescaling fraction > 0.5, the powered pilot must include B.4's scalar-rescale arm (×1.1 of the final residual at matched norm) as a competing explanation — a CONTINUE without it is misattribution. The random-direction control does not cover rescaling (random vectors are orthogonal to ĥ_a in expectation), so this diagnostic is the guard.

---

## 6. Pass budget (F3)

| Block | Passes |
|---|---|
| Startup smoke (3 items × {clean read, A_r, A_g} = 9; asserts verdict-path reachability, identity-vs-archive, throughput ≥80%) | ≤12 |
| Clean-read pass × 60 (r computation; G-norm, G-static, G-curve on CPU) | 60 |
| A_r injection arm × 60 (skipped if G-static fires) | 60 |
| A_g random-direction arm × 60 (skipped if G-static fires) | 60 |
| A_0 identity arm | $0 (clean-read pass's greedy-decoded decisions reused — R4; no additional passes) |
| **Total** | **≤192** |

**F3-TIER-EXCEPTION (CEO, pre-committed in this protocol):** 192 > the 150-pass kill-pilot ceiling (§A.2). The exception is licensed because the r̂-computation pass is irreducible — CPU-verified 2026-09-24 that no archived per-position h_L states exist — and every pass is inventoried above; no hidden passes. Cost ≈ **0.0024 T4-h**. The runner **refuses pass 193** (hard stop, §A.4 guard).

---

## 7. Negative-control battery mapping (§A.3)

| §A.3 control | Served by (kill pilot) |
|---|---|
| Label-free arms (Law #7) | All arms: positions only; bridge disqualified and absent |
| Information-destroyed: isotropic Gaussian at matched norm | A_g (destroys direction, keeps norm) |
| Sign-flip (−r̂) | **Deferred** — mandatory powered-stage arm on CONTINUE (F10) |
| Permuted/shuffled (item j's vector on item i) | **Deferred** — mandatory powered-stage arm on CONTINUE (F10) |
| Identity arm ($0) | A_0, archive bit-for-bit validation |
| Wrong-answer quarantine | No rescue arms exist in this protocol |

**F10 exemption (granted, conditional):** the kill question — "does r̂ carry decision-moving content beyond norm?" — is answered by A_r vs A_g; a norm/energy artifact dies to the random arm. Sign-flip and permuted-r̂ discriminate *among positive explanations* and are interpretation instruments. **Deferral is licensed iff this protocol pre-commits them as mandatory powered-stage arms on CONTINUE** (named in §9). Deferral without this pre-commitment is denied.

## 8. Verdict table (F1) — pre-registered, CI-exclusion form

Primary statistic: Δ = flip-rate(A_r) − flip-rate(A_g), McNemar paired structure, Tango CIs (program standard). One- vs two-sided use is pinned per row; the point estimate Δ̂ is a **screen only, never the verdict**.

**Verdict precedence (M1, pre-registered — stated once here, referenced everywhere):** INVALID conditions are evaluated first and **preempt all verdict rows**, in this order: (i) pre-run SHA-256 vs the expected pinned hash; (ii) identity arm vs archived C1, bit-for-bit; (iii) guard computation faults (G-norm / G-static); **then** (iv) the flip-test verdict rows (RE-SKIN, KILL_gross, KILL_flat, HELD, CONTINUE). A session failing any of (i)–(iii) records INVALID — a broken apparatus can never record RE-SKIN KILL or any other row. **RE-SKIN KILL fires only on a validated apparatus.**

| Row | Firing condition | Verdict |
|---|---|---|
| **RE-SKIN** | G-static fires on a **validated apparatus** (verdict precedence, §8 header): mean pairwise cos(r̂_i, r̂_j) > 0.5 (§5) | **RE-SKIN KILL.** r̂ is a static direction in disguise; killed family (a) covers it. Flip arms not run. |
| **KILL_gross** | Two-sided 95% Tango CI for Δ — **computed at observed N_final (post-G-norm-exclusion), on the included items, consistent with b/c counting** (M2) — lies **entirely below +0.05** | **KILL.** Excludes the packet's own claimed effect (δ_claim = 0.05, Q4). |
| **KILL_flat** | b = c = 0 **and** one-sided 95% Tango upper at observed N_final **< 0.05** | **KILL.** Gross miss — the flat world fires only if it clears this functional bar. Canonical: N_final = 57 deterministic (R2) → one-sided 95% upper = **0.045315** < 0.05 (independently verified 2026-09-24 from the Tango 1998 profile likelihood; evaluator encodes the canonical one-sided table; firing boundary N_final ≥ 52). The N=60 canonical 0.043147 is retained as the §A.4 reference value. |
| **HELD** | CI straddles +0.05; **or** b = c = 0 with one-sided 95% Tango upper ≥ 0.05 at observed N_final (flat but underpowered — reachable only at N_final ≤ 51, e.g. guard-fault edge cases); **or** sub-claim directional signal (Δ̂ > 0 with one-sided p in (0.05, 0.20]) | **HELD (Inconclusive).** Priced powered follow-up (§9), **never CONTINUE**. |
| **CONTINUE** | Δ̂ ≥ +0.05 **and** exact one-sided McNemar (binomial) p ≤ 0.05 in the A_r direction **and** G-static passed **and** G-norm exclusions reported | **CONTINUE to a powered pilot** — never a capability claim. MDE anchor: b=6, c=0 → one-sided p = 0.015625 (two-sided 0.03125). |
| **INVALID** | Identity arm ≠ archived C1 bit-for-bit; or SHA-256 pre/post mismatch; **or pre-run SHA-256 ≠ expected pinned hash `4c242d…dd` (R3 — wrong model downloaded; the binding pre/post guard alone would not catch it)**; or G-static/G-norm computation fault | **No verdict.** Apparatus failure; re-scope under a new pre-registration. **Preempts all rows** — evaluated in precedence order (i)–(iii) before any flip-test row (§8 header). |

**F1 correction recorded (evaluator-verified 2026-09-24):** the review's remedy states the b=c=0 flat outcome "fires cleanly" under the two-sided CI-exclusion form. Computed exactly (Tango score interval, boundary MLE ũ=|δ| at b=c=0): the two-sided 95% CI at b=c=0, N=60 is **[−0.0602, +0.0602]** — it does **not** lie entirely below +0.05. The review's remark is corrected here, not deleted: the flat world is killed by **KILL_flat** (one-sided bar — re-anchored per R1/R2: b=c=0 at N_final=57 → **0.045315** < 0.05, independently verified 2026-09-24 from the Tango 1998 profile likelihood; the N=60 canonical 0.043147 is retained as the §A.4 reference), not by KILL_gross. KILL_gross remains the primary kill for non-flat data. (Two-sided 95% canonical at N_final=57: **[−0.0631, +0.0631]**, verified — the evaluator's KILL_gross reference at the canonical N_final.) (The reviewer's one-sided MDE anchor "b=6,c=0 → p=0.03125" is likewise corrected: 0.03125 is the **two-sided** value; the pinned **one-sided** value is 0.015625 — exact binomial, verified. The evaluator test suite encodes both canonical numbers.)

**Power-gate clause (standing):** this ≤192-pass pilot is an asymmetric instrument — it can KILL or HOLD; only a powered, pre-registered stage can CONTINUE toward a claim. HELD never upgrades to CONTINUE.

---

## 9. Powered-stage pre-commitment (on CONTINUE only)

A CONTINUE verdict licenses **only** a powered pilot, which requires its own Law #15 packet, its own Law #14 review, and its own pre-registration. That pilot **must** carry all four of the following arms (F8, F9, F10 pre-commitment — deferral in the kill pilot is licensed by this list):

1. **Sign-flip arm** (−r̂ at α=1.0): directionality — if r̂ and −r̂ move decisions equally, the effect is magnitude-at-position, not relational content (F10).
2. **Permuted-r̂ arm** (item j's r̂_i applied to item i≠j, fixed seed-pinned derangement): item-specificity — if permuted ≡ matched, the vector carries no item-specific relational information (F10).
3. **Static-at-h_L arm** (EXP077-style static direction, e.g. B_agg, transplanted to final-layer h_L at ans_pos, α=1.0): disentangles the layer axis from the relationality axis (F8).
4. **Conditional scalar-rescale arm** (B.4's ×1.1 final-residual rescale at matched norm): required **iff** the kill pilot's G-curve rescaling fraction > 0.5 (F9).

**Priced follow-up rule (for HELD):** the powered N is solved from the kill pilot's observed discordant rate ψ̂ via the paired-proportion formula N = (z_{1−α}√ψ̂ + z_{1−β}√(ψ̂−δ²))²/δ² with δ = 0.05, one-sided α = 0.05, 1−β = 0.80; the verdict report carries the solved N and the pass price. No powered N is pre-committed here.

---

## 10. K2-fork independence (F11) and queue position

R1 never asks the routing question — it is a whole-trajectory/output-side instrument, exactly the class the LOG-250 G1 guard re-scopes toward. The §8 verdict table is **invariant under all three K2 fork outcomes**:
- K2 supports routing contrast → R1 proceeds (relational readout is a different question).
- K2 supports final-position-local → R1's output-side premise is strengthened; verdict table unchanged.
- K2 row-4 strands → R1 proceeds **unaffected**; it is the licensed exit class.

**Queue position behind K2 is GPU-sequencing on the user's Kaggle node, not logical dependency.** R1 is pre-registered before K2 executes.

## 11. No curvature-diagnostic dependency (F12)

R1's endpoint (discrete flip-rate), construction (r̂ from hidden states), and math license (relational-gradient conjecture) require **no κ̂, no ε, no Hessian, no off-ray quantities of any kind**. The LOG-248 identifiability result is irrelevant to R1 — its bound lives on the S3-9 ray; R1 never leaves the measured positions. Required inputs: clean-read h_L states (F3), α = 1.0 (F2), positions (F4). Nothing else. The G2 guard does not touch R1.

---

## 12. Finding-discharge index (LOG-251 F1–F12)

| Finding | Discharged in | How |
|---|---|---|
| F1 kill in CI-exclusion form | §8 | KILL_gross: two-sided 95% Tango CI entirely below +0.05; KILL_flat: b=c=0 with one-sided 95% upper at observed N_final < 0.05 (**R1** functional bar; canonical N_final=57 → 0.045315; N=60 reference 0.043147 retained); one-/two-sided use pinned per row; point estimate is screen-only. Includes a recorded correction: the flat outcome does not fire the two-sided CI form ([−0.0602, +0.0602] computed); MDE anchor corrected to one-sided 0.015625. |
| F2 α pinned | §2 | α = 1.0 pinned, EXP077-anchored; null at α=1.0 is a KILL; α variation = new Law #15 packet. |
| F3 pass inventory complete | §6 | 180 + ≤12 smoke + $0 identity = ≤192; archive audit CPU-verified (no per-position h_L states); F3-TIER-EXCEPTION pre-committed; runner refuses pass 193. |
| F4 position rule pinned | §3.3 | ans_pos = T−1; q_pos = `?` of `? Answer:` by template-substring search; Law #7 prohibition pre-registered. |
| F5 static-ness threshold | §5 G-static | mean pairwise cos > 0.5 → RE-SKIN KILL, with chance anchor (N(0,1/1024)); fires before flip arms run. |
| F6 norm-floor guard | §5 G-norm | floor = 5th percentile of ‖r‖ (**R2:** linear interpolation pinned → N_final=57 deterministic); exclusions pre-flip-test, count reported; KILL_flat governed by the R1 functional bar at observed N_final. |
| F7 flip outcome defined | §3.2, §4 | outcome = wrong-at-baseline AND right-under-arm; baseline = archived C1, identity-validated; structural zeros handled. |
| F8 conjecture demotion + layer confound | §1.1 | EXP077-null "theorem" → [CONJECTURE] with missing premise stated; layer confound pre-registered; static-at-h_L arm mandatory in powered pilot (§9). |
| F9 rescaling confound | §5 G-curve, §9 | $0 diagnostic mean⟨r̂,ĥ_a⟩ reported; > 0.5 + CONTINUE → scalar-rescale arm mandatory in powered pilot. |
| F10 battery deferral | §7, §9 | Exemption granted conditionally; sign-flip + permuted-r̂ pre-committed as mandatory powered-stage arms. |
| F11 K2-fork independence | §10 | Verdict table invariant under all three fork outcomes; queue position is sequencing only. |
| F12 no curvature dependency | §11 | Explicit: no κ̂/ε/Hessian/off-ray quantities; G2 does not touch R1. |

---

## 13. Law #14 re-review slot and promotion path

1. **This draft → Law #14 re-review of the skeleton (§A.4.6).** The reviewer adjudicates: (a) the F1 correction (two-sided CI vs KILL_flat split); (b) the F3-TIER-EXCEPTION (192 > 150 ceiling); (c) the pinned thresholds (0.5 static-ness, 5th-percentile floor, 0.5 rescaling fraction); (d) the seed scheme; (e) the F10 conditional exemption.
2. On SIGN: CEO GPU clearance; implementation agent builds the bundle (evaluator test suite per §A.2.6 — must reproduce the canonical Tango table: 0.043147 (N=60 reference), [−0.0602, +0.0602] (two-sided, N=60), **0.045315 (N_final=57 — the KILL_flat firing canonical, R1)**, [−0.0631, +0.0631] (two-sided, N_final=57), 0.056902 (b=c=1 boundary check); startup smoke per §A.2.5).
3. Queue: behind K2 on the user's Kaggle node (sequencing only).
4. Execution → §8 verdict table → logged verdict. On CONTINUE: powered pilot per §9 (new Law #15 packet, new pre-registration).

## 14. LOG-253 R1–R5 discharge index (re-review fixes)

| Fix | Discharged in | How (recomputed numbers verified independently 2026-09-24) |
|---|---|---|
| R1 dead KILL_flat row | §8 KILL_flat row; §0 Q4; §5 G-norm | Replaced the N_final=60 pin with the functional bar: b=c=0 AND one-sided 95% Tango upper at observed N_final < 0.05. Canonical N_final=57 (R2) → **0.045315 < 0.05** — the row can fire. Verified from the Tango 1998 profile likelihood (constrained-MLE score, no library values trusted): reproduces 0.043147 (N=60), [−0.0602,+0.0602] (two-sided, N=60), 0.056902 (b=c=1), and the exact one-sided McNemar p=0.015625 at b=6,c=0. Firing boundary N_final ≥ 52. The N=60 canonical 0.043147 is retained as the §A.4 reference value, not deleted. |
| R2 G-norm percentile method | §5 G-norm; §12 F6 | Pinned **linear interpolation** (numpy.percentile default, type 7; position 59·0.05=2.95); exclusion = strictly-below (<). Nearest-rank rejected (would give N_final=58). Arithmetic verified: exactly 3 of 60 items fall strictly below the interpolated floor → **N_final=57 deterministic**. Tie edge case noted (N_final=58 — functional bar still fires, 0.044568 < 0.05). |
| R3 pre-run SHA-256 INVALID row | §8 INVALID row; §2 guard procedure | Added: pre-run SHA-256 ≠ expected pinned hash `4c242d…dd` → INVALID (wrong model downloaded). §2 now states the pre-run comparison explicitly; the binding pre/post match is unchanged. |
| R4 identity-arm $0 mechanism | §4 A_0; §6 budget | Stated explicitly: the clean-read pass's greedy-decoded decisions **constitute** the A_0 identity arm ($0 by reuse); no separate identity pass exists. Budget unchanged: 9 + 60 + 60 + 60 = 189 ≤ 192; runner refuses pass 193. |
| R5 ĝ_i generator library | §4 A_g | **torch** named as the sole generator: dedicated `torch.Generator`, `torch.randn(1024, generator=g_i)`, `g_i.manual_seed(20260924 + i)`, S0 = 20260924. numpy excluded for ĝ_i (Law #13). |

**What this draft licenses:** nothing beyond re-review. **Does not license:** GPU execution; any runner construction; any efficacy, capability, or H-level claim; any α ≠ 1.0; any change to signed artifacts; any use of the bridge as a mechanism arm.

## 15. LOG-255 M1–M3 discharge index (final sign-off fixes)

| Fix | Discharged in | How |
|---|---|---|
| M1 verdict precedence | §8 header (pinned once); §5 G-static; §8 RE-SKIN row; §8 INVALID row; §0 Q2 | INVALID conditions preempt all verdict rows. Pre-registered evaluation order: (i) pre-run SHA-256, (ii) identity-vs-archive bit-for-bit, (iii) guard computation faults, then (iv) the flip-test verdict rows (RE-SKIN, KILL_gross, KILL_flat, HELD, CONTINUE). A broken apparatus can never record RE-SKIN KILL — it fires only on a validated apparatus. No design change. |
| M2 KILL_gross CI denominator | §8 KILL_gross row | Pinned explicitly: the two-sided 95% Tango CI for Δ is computed at observed N_final (post-G-norm-exclusion), on the included items — consistent with b/c counting. No design change. |
| M3 §3.3 q_pos phrasing | §3.3 | "search … in the tokenized prompt" → search the prompt **string** for `? Answer:`, take the character offset of the `?`, map it to its token index. Substring search operates on text, not token IDs. No design change. |

**Final SIGN readiness (M1–M3 discharged):** this draft has applied all three LOG-255 required clarifications as one-sentence pins with no design change. **It is ready for the final Law #14 SIGN** — on SIGN, the protocol is SIGNED and the implementation-bundle stage is licensed per LOG-255 (evaluator test suite reproducing the canonical table + startup smoke test). It licenses nothing until that SIGN is recorded.

*— Research Lead (standing), pre-registration draft, LOG-256, 2026-09-24.*
