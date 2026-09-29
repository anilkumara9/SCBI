# S6-1 — Threshold-Account Breaking Point: Injection Beyond the Linear License — Pre-registration DRAFT v2 (UNSIGNED)

## ERRATA — v2 repair (2026-09-28)

v1 (`S6-1_PREREG_DRAFT_2026-09-28.md`, logged LOG-4410) is preserved byte-identical. Law #14 adversarial review (LOG-4411) returned **ACCEPT-WITH-FIXES**: no structural defect; the five fixes below repair justification language and fence precision only. No decision-table number, bar, movement gate, routing rule, or verdict mapping was altered by this repair.

- **F1 — §4.1 item 7 rewritten (false neutralization claim).** v1 claimed a dead B_wrong instrument "simultaneously returns T p = 1.0," contradicting §2.4's own asymmetric liveness rule (B_wrong=0/T≥1 → LIVE). Replaced with the true analysis: (a) a truly frozen regime yields T=0 too, so the T-significance conjunct fails — the actual neutralization path; (b) B_wrong=0 with significant directional T routes LIVE and a CONTINUE there is valid (the strongest task-direction-specific evidence).
- **F2 — ratio attribution corrected.** "Ratio 0.01185 (EXP094)" was wrong: 0.01185 = 0.0474×0.25 is EXP095's α=0.25 point; EXP094 ran α=1.0 → 0.0474. Corrected in §3 step 4 and the §3 scope fence. Citation error, not an invented number.
- **F3 — weakened-form KILL extended to 3.0-FROZEN.** v1's weakened form covered only 3.0-RUN-INVALID. It now covers any non-live 3.0 (RUN-INVALID or FROZEN), with the principle stated inline: no verdict is earned on an instrument that never went live; the full-strength KILL requires both ratios live.
- **F4 — range notation replaced with point enumeration.** The "0.01185–3.0" notation is retired in §3 step 4 and the scope fence (it read as a continuous claim, tensioning §2.2's no-interpolation rule). Replaced with the enumerated tested battery, with "no interpolation" restated.
- **F5 — single-environment execution pre-registered.** New rule in §2.3: all 300 passes in one pinned environment; no mid-run rebuilds; violation voids the run (Law #13).

*Status: DRAFT v2 — UNSIGNED. NOT a protocol. NOT executable. Law #14 review performed (LOG-4411, ACCEPT-WITH-FIXES); the five binding fixes are applied in this version (errata above). No experiment number minted (S6-1 is EXP096+ material; numbering happens after independent delta re-verification + CEO execution clearance).*
*Licensing chain: LOG-4391 (Monday idea session — the program's license named the ‖δ‖/‖r‖>1 breaking point) → LOG-4400 (EXP095 verdict: REFUTED — magic-strength rescue dead on the licensed grid) → LOG-4407 (EXP096 verdict: REFUTED — headroom-gated rescue dead at α=8.0; "the >0.4740-ratio regime (threshold account above ratio 0.4740) untested"; no further static per-item L11 experiments licensed) → LOG-4408 (innovation sprint: S6-1 ranked #1 of 5 — "the cheapest falsifying test of the last coherent static rescue") → v1 draft (LOG-4410) → LOG-4411 (Law #14 review: ACCEPT-WITH-FIXES — five binding fixes F1–F5) → this v2 draft (LOG-4412).*
*All values below are from LOG-4391, LOG-4400, LOG-4407, LOG-4408, the EXP094/EXP095/EXP096 verdict reviews (`experiments/protocols/REVIEWS/`), the frozen EXP094/EXP095/EXP096 execution archives, and EXP093's signed pre-reg (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`) unless otherwise cited. No number is invented. Every statistic in §4.2 was recomputed by this lane from first principles ($0; no model executed, no weights touched).*
***No pilot is authorized by this draft.** Before any run: independent Law #14 review + SIGN (separate lane), then CEO execution clearance. CPU-only design ($0); no GPU contact under any circumstance.*

---

## 0. Law #15 block (binding, carried from LOG-4408)

**Precise question [HYPOTHESIS].** EXP095 mapped the dose-response inside the linear license (max ratio 0.1896 — flat); EXP096 pushed to ratio 0.38 at the rescue's best shot (headroom-gated, α=8.0 — flat, 3 flips, p=1.0). The licensed carve-out that survived both kills is the **threshold account**: "the push is real but needs to dominate the residual." Does the killed per-item L11 task direction move decisions when the injection **exceeds** the linear license — at ‖δ‖/‖r‖ ∈ {1.5, 3.0}, where the push dominates the residual stream? [HYPOTHESIS]

**Decision it changes.** **KILL** the threshold account entirely if T-vs-B movement < 6 flips at both ratios with the regime verified live — inertness is deeper than strength at *every coherent strength*; the wall gains its far side; the static per-item family's inertness becomes the ultimate boundary statement (fenced — §3). **CONTINUE** (licensed positive) if ∃ ratio ∈ {1.5, 3.0} with T-vs-B flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND B_wrong flat (< 6 flips AND |ΔM| < 0.10) AND ΔM_T > 0 in all three strata (strict) — the threshold account is vindicated; the license boundary was the whole story; the static family reopens above ratio 1 and the >1 regime becomes the program. **PIVOT** if both arms move together (OOD fragility, nonspecific — the >1 regime is decision-noise, not a mechanism), if movement lacks directional significance, or if a ratio's regime is decision-frozen or degenerate (pre-mapped below — the weirdest outcomes are not left unmapped). All outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** The threshold account's prediction is existential over strength: it survives any sub-license null (EXP095, EXP096) by construction. The only falsifier is a super-license null — and the cheapest one is two ratios, not a sweep: 60 EXP092-B items × 3 arms (B, T(ratio), B_wrong(ratio)) × 2 ratios {1.5, 3.0} = 300 injection passes (+ 90 reserve → 390 expected, 600 hard cap), CPU, $0. Ratio 1.5 is the first coherent super-license point (clearly above 1, still a perturbation in the weak sense); ratio 3.0 is the maximum coherent strength (beyond it the intervention replaces the representation — §0.1). No new machinery: the executor pattern is EXP095's, with α = ratio/0.0474 (ratio 1.5 → α ≈ 31.65; ratio 3.0 → α ≈ 63.29).

**Quantitative prediction (pre-registered, bars).** Per ratio, on T-vs-B paired decisions over the 60 items: flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND B_wrong(ratio) flat (flips < 6 AND |ΔM| < 0.10) AND ΔM_T(ratio) > 0 in all three strata (aggregate / A-first / C-first, strict) → CONTINUE, scoped to the winning ratio. T-vs-B flips < 6 at every live ratio → KILL. Near-miss p ∈ [0.01, 0.05) → PIVOT (S5-1 v2 F1 precedent — never CONTINUE-with-caveat).

**Breaking point (sharp, two levels).** (i) In-band: T-vs-B movement < 6 at both ratios with the regime verified live → the threshold account is dead at every coherent strength; KILL. (ii) Coherence boundary: ratio 3.0 is the maximum coherent static-injection strength — beyond it (‖δ‖ > 3‖r‖) the intervention replaces the representation rather than perturbing it, by the packet's own definition (§0.1). A null at 3.0 with a live regime therefore **exhausts** the "stronger push" rescue: no coherent "try ratio 5.0" remains. [INTERPRETATION of scope]

**The belief it tests (named, LOG-4408):** "the push is real but too weak" — overturned-by directional movement above ratio 1 (threshold vindicated; the >1 regime becomes the program) or deepened-by a clean KILL at 1.5 and 3.0 (inertness is structural, not a strength artifact at any strength). [INTERPRETATION]

### 0.1 The >1 license treatment (the central honesty section — what Law #14 must attack first)

[FACT] The linear-perturbation license (EXP093 signed pre-reg §License, cited by reference) is the first-order expansion Δm_i ≈ α·⟨∇ₕm_i, d_i⟩, valid while ‖δ‖ ≪ ‖r‖ (remainder O(‖δ‖²)). At ‖δ‖/‖r‖ ∈ {1.5, 3.0} the remainder dominates the first-order term. **The linear license does not cover this design, and this draft does not smuggle it in.** No quantitative prediction about margin-shift magnitude is licensed at these ratios; the reach-scaling law (§0.1 of S5-4 v2) is not extrapolated here.

[INTERPRETATION] What licenses the test is the threshold account's **own terms of engagement**: the account predicts that once ‖δ‖ dominates ‖r‖, a real directional push must register as decisions move — the response is set by the model's off-manifold behavior, and off-manifold behavior driven by task geometry is exactly what the account asserts. This is not a mathematical license; it is a pure empirical probe of the breaking point the program itself named in LOG-4391. The test is fair because the account cannot simultaneously claim "the push needs to dominate" and be unfalsifiable at the ratios where the push dominates.

[DEFINITION — coherence boundary] A static injection at ratio ρ is **coherent** iff the injection arm's decisions retain item-level variance (the intervention perturbs the decision substrate rather than replacing it). Operationalized in §2.4: zero-variance decisions on any injection arm at a ratio → that ratio is RUN-INVALID (representation-replacement regime — evidence for neither side). Ratio 3.0 is the maximum ratio this draft tests; beyond 3.0 the intervention is >3× the residual norm, which is replacement by this definition. [ASSUMPTION made testable]

[INTERPRETATION] What a KILL means: the task direction does not move decisions at any coherent static-injection strength — the wall's far side. What it does NOT mean: anything about dynamic, gated, multi-layer, or other-layer mechanisms (fenced — §3); anything about the direction's decodability (S5-3 territory); anything about non-static interventions.

---

## 1. Background and license

- **EXP094 binding facts [OBSERVATION, LOG-4375/4376/4377; verdict review §2]:** per-item L11 task-direction injection at α=1.0 on EXP092-B: B=T=R=36/60; ΔM_T=+0.0000; McNemar b=c=0 → p=1.0000 all nine contrasts; 0 flips across 120 injection item-arms despite nonzero margin shifts on every item (max |shift| = 0.090155); Δθ=0 hash pin `ec276abe…` (LOG-331); degeneracy mean pairwise |cosine| = 0.7923 < 0.95. Licensed claim: per-item static L11 directions do not move decisions **at α=1.0**.
- **EXP095 binding facts [OBSERVATION, LOG-4400; verdict review §2]:** α-sweep {0.25, 0.5, 1.0, 2.0, 4.0}: T-vs-B flips = {0, 0, 0, 1, 1}; every McNemar p = 1.0 across all 5 α × 3 contrasts × 3 strata; foundation reproduced 60/60 per-item B agreement. Verdict: **REFUTED — the magic-strength rescue is dead on the licensed five-point grid**; inertness is strength-invariant over 16× (boundary-law graduation, scoped to the grid).
- **EXP096 binding facts [OBSERVATION, LOG-4407; verdict review §2]:** headroom-gated injection at α=8.0 (ratio 0.3792, max band 0.4740 < 1) on the frozen 21-item reach-calibrated set: gated T-vs-B 3 flips (< 6), b=1, c=2 → p=1.0, ΔM_T = −0.0476, sign-heterogeneous; B_wrong 3 flips, p=1.0; in-run reach 0.8621 (neither tripwire fired). Verdict: **REFUTED — the headroom-gated rescue is dead**; the threshold account falsified within the linear license up to ratio 0.38; the static per-item family closed **conditionally** (first in program history). The α=16 variant explicitly NOT licensed (both follow-up conditions failed).
- **Death-debt [FACT, LOG-4408]:** this sprint's proposal wave is the LOG-219 death-debt payment for EXP095 and EXP096; S6-1 is the green-lit first proposal. This draft is the "pre-registered plan" the proposal requires — **not a revival or an edit of EXP094/095/096** (all three runs are closed records). This document is a new unsigned file.
- **Mathematical license [see §0.1]:** the linear license does not cover this regime; the test is licensed by the threshold account's own prediction (empirical probe of a named breaking point), not by perturbation theory. **License verdict: HOLDS for a test, not a conclusion** — the probe is fair on the account's own terms; a positive would reopen the family above ratio 1, a null exhausts the coherent "stronger push" rescue.
- **Summit filter:** a CONTINUE would be the program's first causal-steering signal at a non-readout layer — the >1 regime would become the program and the summit's dose-response primitive would live there. A KILL completes the static-family map the paper needs (the wall's far side) — citable boundary infrastructure. Caveat preserved: injection is externally applied, not self-computed — never described as an autonomy result.

---

## 2. Design (frozen model, Δθ = 0; frozen EXP094 bundle path; two super-license ratios)

### 2.1 Arms (pre-registered)

| Arm | Injection at L11 (readout-anchor position, per item i) | Role |
|---|---|---|
| B | none (Δθ = 0) — single run per item | baseline — anchors EXP092-B; paired baseline for both ratios |
| T(1.5) | per-item task direction d_i scaled to norm 1.5·‖h_i^B‖₂ (α ≈ 31.65) | test arm — first coherent super-license point |
| T(3.0) | per-item task direction d_i scaled to norm 3.0·‖h_i^B‖₂ (α ≈ 63.29) | test arm — maximum coherent strength |
| B_wrong(1.5) | per-item **random** direction g_i (EXP094's frozen R-arm constructor, pinned seed → identical {g_i}) scaled to norm targeting T(1.5)'s per-item norm | discriminant + liveness instrument at 1.5 |
| B_wrong(3.0) | per-item **random** direction g_i (same frozen constructor, pinned seed) scaled to norm targeting T(3.0)'s per-item norm | discriminant + liveness instrument at 3.0 |

**Single-B design (frozen choice, S5-1 v2 F2 precedent):** under the draft's determinism premise the B arm is byte-identical across ratios (no injection) — re-running it per ratio would be 120 redundant passes. Budget: 60 B + 120 T + 120 B_wrong = **300 passes**. The strengthened step-0 gate (§3 step 0) doubles as the determinism self-check. (Deviation from the LOG-4408 packet's 360 noted here — the packet assumed per-ratio B; the F2 precedent rules it redundant.)

**{d_i}, {g_i} regeneration (frozen specification).** Identical to S5-1 v2 §2.1 / S5-4 v2 §2.1: regenerated from the frozen EXP094 constructor `experiments/runs/EXP094_peritem_l11/constructor.py`, hash-pinned `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361` [FACT, constructor manifest]; pre-run re-hash, mismatch → HOLD. G7 label-free attestation carries from EXP094's `constructor_manifest.json` (same frozen code + same P₀ (`e7e81496…f2601e11`) + same bench — code-identical, not re-audited). The {g_i} use the pinned R-arm seed.

#### 2.1.1 B_wrong's dual role at super-license ratios (what it rules out)

- **Role 1 — liveness instrument [DEFINITION]:** at each ratio, B_wrong flips ≥ 1 → the regime is **decision-live** (something can move decisions at this ratio). B_wrong flips = 0 AND T flips = 0 → **decision-frozen** → that ratio is Underdetermined (never KILL on a frozen regime — §3). The instrument cannot manufacture a KILL: it only unlocks evaluation; the KILL is earned by T's flatness across 60 items, measured independently.
- **Role 2 — discriminant [DEFINITION]:** where the regime is live, B_wrong at matched norm controls "δ-driven but content-free" decision changes — the exact confound of the >1 regime (decisions vary with δ but carry no task geometry). If T moves ≥ 6 with p < 0.01 while B_wrong stays flat, the δ-artifact is priced out; if both move ≥ 6, the effect is nonspecific → PIVOT (fragility), never CONTINUE. **Joint-requirement rule (S5-4 v2 F1 precedent):** fragility-PIVOT fires only on T ≥ 6 **and** B_wrong ≥ 6 jointly — B_wrong ≥ 6 with T < 6 fires step-3 KILL (first-match-wins) and strengthens it (the regime is live and flippable, yet the task direction does not move it).
- **"Flat" (pre-registered):** B_wrong(ratio) is flat iff flips(B_wrong vs B) < 6 AND |ΔM_Bwrong| < 0.10, ΔM per EXP093's paired convention.

### 2.2 Ratios (pre-registered, two points)

‖δ‖/‖r‖ ∈ {**1.5**, **3.0**}; executor α = ratio/0.0474 ≈ {31.65, 63.29}. G5-style delivery bands (±25%): **[1.125, 1.875]** and **[2.25, 3.75]**. **No interpolation between ratios is licensed** — each ratio is an independent pre-registered test. **No other ratio is licensed** — this is not a dose-response (strength is EXP095's closed territory); the question is the threshold account's breaking point, tested at its first coherent point and its maximum coherent strength.

**Items:** all 60 EXP092-B items (30 A-first / 30 C-first strata, bench pin). **Not gated** — justified: the threshold account is about the push dominating the residual, not about headroom; gating would conflate two rescues (EXP096's conditionality with S6-1's strength). The full set is the rescue's own terms.

### 2.3 Budget (pre-registered)

- **300 injection passes** (60 B + 120 T + 120 B_wrong); **+90 reserved** for delivery/margin-verification repeats → **390 expected; hard cap 600.** Spend beyond 390 requires a logged, pre-cleared exception; the 600 hard cap is not waivable within this pre-registration (a change is a new design, not an edit). CPU only, $0.
- **Single-environment rule (pre-registered, Law #14 F5):** all 300 passes run in one pinned environment — no mid-run rebuilds, library upgrades, or environment changes between the B run and the injection arms. The §5.3 manifest attests the environment; changing it mid-run voids the run (Law #13). (The single-B design's determinism premise requires this guard.)

### 2.4 Statistics (pre-registered)

- **McNemar exact, doubling convention** (EXP094's convention, verdict reviews §1) on paired decisions, per ratio: T-vs-B, B_wrong-vs-B, T-vs-B_wrong [diagnostic-only — Law #9 hygiene, cf. S5-1 v2 F13].
- **ΔM** per EXP093's paired convention; **Tango 95% CIs** on the paired differences.
- **DELTA_BAR = 0.10; ALPHA_disc = 0.01** — single discovery bar per ratio. **Family-wise disclosure:** 2 ratios at 0.01 → ≈ 1 − 0.99² ≈ 0.020 under the global null — disclosed, not hidden; the CONTINUE conjunction (flips ≥ 6 AND p < 0.01 AND B_wrong flat AND all-strata ΔM_T > 0) is the pre-registered mitigation. **Movement gate: ≥ 6 flips** (program standard; necessary but not sufficient — the discovery bar needs b ≥ 8 effectively, §4.2).
- **Correctness:** margin > 0 (strict), EXP094's convention.
- **Liveness instrument rule (per ratio):** B_wrong flips ≥ 1 → ratio is LIVE → evaluate. B_wrong flips = 0 AND T flips = 0 (delivery confirmed) → ratio is FROZEN → Underdetermined at that ratio (no verdict licensed there). B_wrong = 0 with T ≥ 1 → ratio is LIVE (T moved where random didn't — evaluate normally; the asymmetry is disclosed in §4.1 item 4).
- **Coherence gate (per ratio):** zero-variance decisions (all 60 identical top-1) on any injection arm → that ratio is **RUN-INVALID** — representation-replacement regime, evidence for neither side, no verdict licensed there. (B-arm zero-variance → foundation HOLD, not RUN-INVALID — the bench itself broke.)
- **Tie gate:** ties/180 > 5% at any ratio → that ratio RUN-INVALID (excluded, no verdict licensed there).

---

## 3. Decision table (pre-registered)

**Arm-routing rule (binding):** every one of the 60 EXP092-B items receives B once and all four injection arms (full within-(ratio,item) pairing); all contrasts are paired; no item excluded from any contrast; stratum membership (aggregate / A-first / C-first, 30/30) is the bench pin, fixed before inspection. No post-hoc re-routing — structurally impossible under full pairing.

**Per-ratio regime routing (binding, evaluated before the global table):** at each ratio r ∈ {1.5, 3.0}: RUN-INVALID_r if the coherence gate or tie gate fires (§2.4); else FROZEN_r if B_wrong flips = 0 AND T flips = 0 (delivery confirmed); else LIVE_r. A ratio that is RUN-INVALID or FROZEN contributes no verdict — it is reported with its routing and excluded from the global steps.

**Binding evaluation order (first match wins).** Exactly one step is earned:

0. **Foundation gates.** (i) Constructor re-hash vs `5e03f206…917f361` → mismatch: **HOLD**. (ii) Per-item B-decision agreement vs the archived EXP094 B vector: 60/60 required → any disagreement: **HOLD**. (iii) Degeneracy sanity: |recomputed mean|cos| − 0.7923| > 0.05 → **HOLD** (constructor regeneration broken). A HOLD triggers the pre-registered diagnosis lane (re-hash weights vs LOG-331 pin, verify thread pinning, byte-compare prompts, re-verify archive SHA-256) — **never a silent re-run**. *Foundation guards only; no verdict on the hypothesis.*
1. **Delivery.** G5 probe on the 240 injection rows: per-row perturbation_ratio within the §2.2 band for its ratio, margin shift recorded vs B. Per (ratio, arm): ≤2 rows out of band → those items excluded from that arm's contrasts (no verdict licensed on them). >2 rows out of band on any (ratio, arm), or any zero-norm d_i → **HOLD + diagnose** (common-cause suspected). *(Maps to: Inconclusive.)*
2. **Degeneracy.** Mean pairwise |cosine| over regenerated {d_i} ≥ 0.95 → **Underdetermined** — never KILL on a powerless test (R4 rule). *(Maps to: Underdetermined.)*
3. **Powerless test.** No LIVE ratio (both ratios FROZEN, or one FROZEN and the other RUN-INVALID, or both RUN-INVALID) → **Underdetermined** — the test could not move decisions at all; a KILL is never manufactured from a frozen or replaced regime. *(Maps to: Underdetermined.)*
4. **Threshold KILL (the wall's far side).** At every LIVE ratio, T-vs-B movement < 6 → **Refuted: the threshold account is dead at every coherent static-injection strength** — inertness is deeper than strength; the static per-item family's inertness is structural from the tested battery's minimum ratio 0.01185 (EXP095's α=0.25 point — F2 correction; v1 misattributed it to EXP094) through ratio 3.0 (enumerated battery — §3 scope fence; no interpolation). **Weakened-form fence (pre-registered, extended per Law #14 F3):** if ratio 3.0 is non-live — RUN-INVALID *or* FROZEN — while ratio 1.5 is LIVE with T < 6, the KILL fires in weakened form — "dead at every coherent strength tested (ratio 1.5); ratio 3.0 is non-live [state which: RUN-INVALID = crosses into representation-replacement; FROZEN = the instrument never went live] and is untestable by static injection" — with the fence inline in the verdict language, never dropped in retelling. **Principle (F3):** no verdict is earned on an instrument that never went live; the full-strength KILL requires both ratios live. *(Maps to: Refuted.)*
5. **Specificity PIVOT.** At any LIVE ratio with T movement ≥ 6: (a) B_wrong movement ≥ 6 → **PIVOT** (fragility — the >1 regime is decision-noise under large nudges, nonspecific perturbation, not task geometry); (b) T-vs-B McNemar p ≥ 0.01 → **PIVOT** (movement without directional significance at the discovery bar — e.g. b≈c splits, or near-miss p ∈ [0.01, 0.05)). *(Maps to: Not supported for the directional claim.)*
6. **Licensed positive.** ∃ LIVE ratio with T-vs-B flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND B_wrong flat (< 6 flips AND |ΔM| < 0.10) AND ΔM_T > 0 in **all three** strata (strict — a zero or negative stratum fails consistency, carried from S4-9) → **CONTINUE (Supported), scoped:** the threshold account is vindicated; the license boundary was the whole story; the static family reopens above ratio 1 on EXP092-B at the winning ratio; the >1 regime becomes the program. Multiple qualifying ratios → all reported; the scope is the qualifying set, never interpolated. *(Maps to: Supported.)*
7. **Otherwise → PIVOT** *(maps to: Not supported for the global claim)*, with named sub-cases: (a) sign-heterogeneous movement across ratios or strata with null T-vs-B_wrong specificity — global threshold claim dead, conditional design EXP097+ material; (b) **consistent wrong-direction steering** (ΔM_T < −0.10 with p < 0.01 and B_wrong flat at a LIVE ratio) — a causal channel exists, the constructor is mis-signed; sign story is EXP097+ material, never KILL.

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted); the parenthetical mappings bind each step to its verdict. No banned language. No EXP094/095/096 claim is altered. **Scope fence:** dynamic/gated mechanisms, multi-layer compositions, other layers/benches/models remain EXP097+ material regardless of outcome; the KILL is fenced to static per-item L11 injection at the coherent *tested* strengths — enumerated battery (Law #14 F2/F4): 0.01185 (EXP095 α=0.25), 0.0237 (EXP095 α=0.5), 0.0474 (EXP094 α=1.0; also EXP095 α=1.0), 0.0948 (EXP095 α=2.0), 0.1896 (EXP095 α=4.0), 0.3792 (EXP096 α=8.0; delivery max band 0.4740), 1.5 and 3.0 (S6-1) — never to "all mechanisms" or "all strengths"; **no interpolation between tested points is licensed** (v1's "0.01185–3.0" range notation is retired — it read as a continuous claim). The >3.0 regime is replacement by definition, not tested strength.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post == LOG-331 pin `ec276abe…`; any mismatch voids the run (Law #13).
- **Frozen constructor:** re-hash `experiments/runs/EXP094_peritem_l11/constructor.py` before any run; mismatch vs `5e03f206…917f361` → HOLD. G7 attestation carries from EXP094's `constructor_manifest.json` (code-identical).
- **G5-style exact-delivery probe:** per-(ratio,i,arm) perturbation_ratio targets {1.5, 3.0}, bands ±25% (§2.2); aggregation rule per (ratio, arm) (§3 step 1). Margin shift vs B recorded per item (reached-the-logits check, carried from EXP094).
- **Per-item records (Law #13):** every (item, ratio, arm) persists: top-1 decision, margin (EXP093's logit-margin m(h)=logit(target)−logit(foil), cited by reference — §5 item 1), perturbation_ratio, margin shift vs B. **Non-negotiable.**
- **Arm-routing rule:** binding full pairing (§3); no post-hoc re-routing.
- **Coherence + tie gates:** per ratio, zero-variance injection-arm decisions → RUN-INVALID; ties/180 > 5% → RUN-INVALID (§2.4).
- **Thread pinning:** torch intra-op thread count pinned to the EXP092/EXP094 extraction value and asserted before condition B, per EXP093 G4 (thread-count differences can flip near-zero margins; S2's mean margin was −0.0018).

### 4.1 Degeneracy analysis of every diagnostic (LOG-4338 lesson — constant-data unit tests, pre-registered)

Each diagnostic states what it returns on degenerate input. A diagnostic that can manufacture a positive from degenerate input is disqualified; all below fail safe:

1. **McNemar exact (doubling).** Constant input (b = c = 0 — the EXP094 datum): p = 1.0000 exactly, never significant → fails safe toward KILL, **cannot** manufacture CONTINUE. Adversarial input (b=60, c=0): p ≈ 1.73×10⁻¹⁸ (S5-1 v2 F11). Unit test (executor runs pre-registration): all-identical decision vectors → p = 1.0 asserted.
2. **ΔM paired difference.** Zero-variance input → ΔM = 0 exactly, Tango CI = [0, 0] → cannot clear DELTA_BAR = 0.10 → fails safe.
3. **Flip-rate(ratio).** No flips → 0. Safe.
4. **The liveness instrument (B_wrong ≥ 1) — the dangerous direction.** Two degenerate cases: (a) Truly-frozen regime (nothing can move): B_wrong = 0, T = 0 → FROZEN → Underdetermined — correct, never KILL. (b) Noise-unlocked regime: a single B_wrong noise flip with T = 0 → LIVE → step-4 KILL fires. **Disclosed asymmetry:** the ≥1 bar is deliberately weak to avoid manufacturing Underdetermined from freeze-ambiguity; the KILL's evidential weight comes from T's flatness across 60 items at two ratios (120 independent chances to move), not from the bar's height. A critic demanding a higher bar (≥3) must argue it pre-registration — either ruling is honest, but the bar cannot move after the run.
5. **The coherence gate (zero-variance → RUN-INVALID).** Could it dodge a KILL? It fires only when an injection arm's decisions are constant across all 60 items — i.e., the intervention destroyed the decision substrate (replacement regime). On a live regime with an inert T, decisions retain variance (B itself is 36/60). The gate therefore cannot fire on the KILL's evidence — it fires only where no verdict is licensable. Fails safe. Unit test: constant decision vector → RUN-INVALID asserted.
6. **Degeneracy gate (mean pairwise |cosine| over {d_i}).** 60 identical vectors → 1.0 ≥ 0.95 → Underdetermined (correct: the powerless test is caught, never KILLed). **Zero-vector edge:** a zero-norm d_i sits at perturbation_ratio = 0, outside every §2.2 band → delivery HOLD (§3 step 1) **before** the gate is ever computed. The gate is never asked to divide by zero. (S5-1 v2 §4.1 precedent.)
7. **B_wrong flatness — the second dangerous direction (corrected per Law #14 F1).** A dead instrument returns B_wrong flat — and flatness is a CONTINUE-*enabling* conjunct. The true neutralization analysis: (a) a truly frozen regime yields T = 0 as well, so the T-significance conjunct fails — *that* is the actual neutralization path, and it is automatic; (b) B_wrong = 0 with significant directional T routes LIVE per the §2.4 asymmetric rule, and a CONTINUE there fires correctly — task-direction-specific movement where matched-norm random injection moves nothing is the *strongest* evidence for the threshold account, not a confound. (v1's claim that "a dead instrument simultaneously returns T p = 1.0" was false and contradicted §2.4.) **CONTINUE requires the conjunction** (T significant AND B_wrong flat AND all-strata ΔM_T > 0); no conjunct alone licenses anything.

### 4.2 Probe-feasibility algebra (EXP079 lesson — proved, not asserted)

- **McNemar minimum at ALPHA_disc = 0.01:** exact doubling convention — b=8, c=0 → p = 2·(1/2)⁸ = 0.0078125 < 0.01 ✓; b=7, c=0 → p = 0.015625, n.s. The discovery bar needs ≥8 directional flips; the ≥6-flip movement gate is necessary-but-insufficient (6–7 flips with p ≥ 0.01 → step-5 PIVOT, never CONTINUE). Maximum achievable = 60 ≥ 8. **No structural infeasibility** (the EXP079 contrast): every item's decision can flip in principle; max ΔM = 1.0 ≥ DELTA_BAR.
- **KILL feasibility:** needs T-vs-B < 6 at every LIVE ratio — satisfiable (the null predicts ~0–2).
- **Liveness feasibility:** B_wrong ≥ 1 flip per ratio — satisfiable by the same arithmetic; at ratios 1.5/3.0 large random nudges are expected to flip fragile items (S5-4: B_wrong moved 3/21 at ratio 0.38). If it fails, the regime is genuinely frozen → step 3 fires honestly.
- **Family-wise:** 2 ratios at 0.01 → 1 − 0.99² ≈ 0.0199 ≈ 2% — disclosed in §2.4, not hidden.
- **Delivery bands** [1.125, 1.875] and [2.25, 3.75]: the executor's ratio targeting is identical machinery to EXP095's (ratio = α·0.0474); bands are ±25% by the G5 convention. Feasible by construction.
- **Coherence gate feasibility:** zero-variance detection is a deterministic property of the 60-vector — always computable, never infeasible.
- **Budget:** 300 + 90 = 390 expected ≤ 600 hard cap. **Replication gate** (B = 36/60 per-item agreement): feasible — deterministic CPU forward passes demonstrated across EXP094/095/096, including a rebuilt environment (EXP095 step-0: 60/60).
- **Conclusion:** every pre-registered bar is reachable by construction. If Law #14's independent recomputation of this algebra disagrees, the run does not proceed.

### 4.3 Verdict discipline

The §3 evaluation order, five permitted verdicts with step→verdict mappings, no post-hoc table edits; a design change is a new experiment number, never a silent edit. The per-ratio routing (RUN-INVALID / FROZEN / LIVE) is computed before the global table and cannot be re-routed after inspection. **$0 compute for this draft:** on-paper only. No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, stratum, ratio ∈ {1.5, 3.0}, arm ∈ {B, T, B_wrong}, top-1 decision, margin, perturbation_ratio, margin shift vs B). Margin convention: EXP093's logit-margin m(h) = logit(target) − logit(foil), cited by reference (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md` §License, "the correct-margin") — not redefined at execution time.
2. Constructor manifest: re-verified constructor SHA-256 (must equal `5e03f206…917f361`), P₀ hash, R-arm seed, G7 carry-over attestation reference, per-item d_i/g_i norms, pairwise |cosine| summary (degeneracy gate inputs + §3-step-0 sanity value).
3. Δθ = 0 hash pre/post; environment + seed + thread-count manifest (Law #13 reproducibility).
4. Delivery probe log: per-(ratio,i,arm) perturbation_ratio vs the §2.2 bands; per-(ratio,arm) PASS/FAIL aggregation decisions (§3 step 1 rule).
5. Regime-routing log: per ratio, the computed routing (LIVE / FROZEN / RUN-INVALID) with its evidence (B_wrong flip count, T flip count, decision-variance check, tie rate) — machine-written, before the global table is walked.
6. Stratum table: 3 strata × 2 ratios × 3 contrasts (T-vs-B, B_wrong-vs-B, T-vs-B_wrong [diagnostic-only]): ΔM, McNemar b/c/p, Tango 95% CI — 54 cells, machine-written.
7. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition (including the step-0 foundation values and the per-ratio routing).

---

## 6. Known design risks — what Law #14 should try to break (falsification-first)

Ranked by how badly each would wound the licensed verdicts:

1. **Is ratio 3.0 "replacing the representation"?** The packet's own breaking-point argument (§0.1) — if Law #14 rules 3.0 is already replacement rather than perturbation, the design's top ratio is untestable and the KILL weakens to the ratio-1.5 form (pre-registered weakened fence, §3 step 4). The zero-variance RUN-INVALID rule is the tripwire, but a critic may argue replacement can be subtler — decisions vary, yet are driven by δ-artifacts rather than content. **Counter offered:** the norm-matched B_wrong arm is exactly the control for "δ-driven but content-free" changes — if decisions vary with δ while T never beats B_wrong directionally, that is inertness of the *task direction*, not replacement of the substrate. Attack the counter, not just the tripwire.
2. **The liveness bar (≥1 flip) is weak.** A single B_wrong noise flip unlocks the KILL (§4.1 item 4 — disclosed). **Attack:** demand ≥3 flips or a sign-consistent liveness bar, or argue the asymmetry lets a lucky noise flip launder a KILL. **Counter:** the KILL's weight is T's 120-item flatness, not the bar's height; raising the bar manufactures Underdetermined from freeze-ambiguity. Either ruling must be pre-registered before the run — not debated after.
3. **OOD-collapse confound.** At ratios 1.5/3.0 the regime is off-manifold by construction — a critic may argue the whole design tests a strawman (the threshold account's "dominance" regime is definitionally OOD, so a KILL kills nothing real). **Counter:** the account is a claim *about* this regime; testing it on its own terms is not a strawman — but the verdict language must never generalize the KILL beyond static injection (fenced in §3). The instrument check + coherence gate are the anti-gaming machinery; Law #14 must confirm the Underdetermined routing can't be gamed into a KILL or vice versa.
4. **The gap between ratio 0.4740 (EXP096's max band) and 1.5.** A narrow magic band (e.g., ratio 0.8–1.2) is invisible to this design — the KILL is scoped to the tested ratios {1.5, 3.0} plus the archived battery (0.01185–0.4740), never to "all strengths." Same Gap-1 discipline as S5-1 v2. **Attack:** demand an intermediate ratio (1.0)? Counter: ratio 1.0 at full-set was EXP094's kill (0 flips); re-testing it is deterministic archive re-reading (EXP095 demonstrated 60/60 bit-reproduction) — not an experiment.
5. **One bench.** Any CONTINUE is bench-scoped to EXP092-B; a critic may note the >1 regime's OOD character makes bench-generality even less licensable than usual. Disclosed; the scope fence (§3) holds regardless.
6. **Stratum consistency at OOD ratios.** The strict all-strata ΔM_T > 0 bar for CONTINUE may be unearnable where strata behave asymmetrically under large nudges — a critic may call the positive-detection machinery decorative. Disclosed; kept strict anyway — a CONTINUE that reopens the family must earn it (S5-1 v2 precedent).
7. **The "coherent strength" boundary is definitional.** The draft asserts 3.0 as the maximum coherent strength via the replacement definition (§0.1); a skeptic could still demand ratio 5.0 after a 3.0 null. **The draft's pre-registered answer:** beyond 3.0 the intervention exceeds 3× the residual norm — replacement by the packet's own definition, which the skeptic accepted by engaging the threshold account at all. No "stronger push" rescue remains coherent. This is a definitional fence, disclosed here — Law #14 should rule whether it holds.
8. **Single-B design deviation from the packet.** The LOG-4408 packet costed 360 passes (per-ratio B); this draft runs B once (300 passes, S5-1 v2 F2 precedent). **Attack:** argue per-ratio B is needed because the >1 regime might interact with the baseline runs (e.g., environment drift between ratio batches). Counter: the step-0 gate re-verifies B agreement against the archive before any injection; batch effects are an executor-scheduling matter, not a design matter — but Law #14 may demand per-ratio B re-verification as a cheap guard.

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not alter EXP094's/EXP095's/EXP096's closed run records, any prior draft, or any signed artifact; does not touch weights.
- Does not invent numbers — every value cites LOG-4391, LOG-4400, LOG-4407, LOG-4408, the EXP094/095/096 verdict reviews, the frozen execution archives, or EXP093's signed pre-reg, except the two-ratio selection, the single-B design (§2.1), the liveness/coherence routing (§2.4/§3), and the weakened-form KILL fence — which are frozen design choices by this lane, flagged for Law #14 above.
- Does not license a sub-license dose-response, interpolation between ratios, ratios beyond 3.0, dynamic/gated mechanisms, multi-layer compositions, other layers/benches/models, or any claim about the direction's decodability.

---

## 8. Next steps

Independent **Law #14 review** of this draft (separate lane — pre-assigned LOG number by the dispatcher) → SIGN or SIGN-WITH-FIXES → repair lane if needed → independent delta re-verification → **CEO execution clearance** → run (CPU, ≤390 passes expected, 600 hard cap). **Pilot NOT authorized until all complete. No GPU contact under any circumstance.**

---

*v2 prepared 2026-09-28 by the S6-1 pre-registration repair lead (LOG-4412), applying Law #14's five binding fixes (LOG-4411) to the v1 draft (LOG-4410 — preserved byte-identical). v2 is DRAFT, UNSIGNED — independent delta re-verification + CEO execution clearance still required before any run; no finding is closed. On paper only, $0 compute, CPU-only design. No signed protocol file was edited; no decision-table number, bar, movement gate, routing rule, or verdict mapping was altered — justification language and fence precision only.*
