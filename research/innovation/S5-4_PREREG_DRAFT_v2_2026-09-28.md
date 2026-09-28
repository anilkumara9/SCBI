# S5-4 — Headroom-Gated Injection of the Killed Per-Item L11 Direction — Pre-registration DRAFT v2 (UNSIGNED)

---

## Errata — v2 (2026-09-28; repair of the binding Law #14 fix list F1–F3, LOG-4402)

*This version applies the binding Law #14 fix list (LOG-4402) in full. v1 (`S5-4_PREREG_DRAFT_2026-09-28.md`, LOG-4401) is preserved unedited. Nothing else changed.*

- **F1 (§6 item 3 + §2.1.1 flatness; re-verifiable by inspection):** restated the fragility-PIVOT risk with the joint requirement — step-4 PIVOT fires only on gated T(8.0) movement ≥ 6 **and** gated B_wrong movement ≥ 6; B_wrong ≥ 6 with T < 6 fires step-3 KILL (first-match-wins) and strengthens it (flippable-by-large-nudge items not moved by the task direction). The previous text implied B_wrong ≥ 6 alone → PIVOT, contradicting the binding decision table.
- **F2 (§2.4; needs delta re-verification):** added the symmetric over-coverage rule — if realized max|shift(8.0)| < 0.5 × τ_8 = 0.45, the step-3 KILL verdict carries the "low-margin-items form" fence inline (strict-reach form softened), with the realized reach reported. Mirrors the existing under-coverage tripwire (> 1.125 = 1.25 × τ_8).
- **F3 (§0; inspection):** "(the program's first mechanism family fully closed)" → "(the program's first mechanism family closed, conditionally — within the linear license up to ratio 0.38)", matching the binding step-3 language ("the static per-item family is closed conditionally too"). Grep-verified: no other "family closed" occurrence needed the qualifier.

---

*DRAFT v2 continues below (v1 text + the three fixes above).*

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. NOT reviewed. No experiment number minted (S5-4 is EXP094+ material; numbering happens after Law #14 review + CEO license).*
*Licensing chain: LOG-4373–4377 (EXP094 executed; Refuted/KILL, pure inertness; Law #14 SIGN) → LOG-4390 (founder gap review) → LOG-4391 (Monday idea session: S5-4 born as PROPOSAL — "headroom-gated injection: the last licensed static variant"; Law-#15 packet on record — threshold-account license; breaking point = margin shifts without flips) → LOG-4398/4399/4400 (S5-1 executed as EXP095; binding verdict REFUTED — the magic-strength rescue is dead on the licensed grid; "S5-4 (headroom-gated injection) is the live successor lane — needs its own preregistration + Law #14 review; this verdict does not pre-license it") → this draft (LOG-4401).*
*All values below are from LOG-4391, LOG-4400, the EXP094 verdict review (`experiments/protocols/REVIEWS/EXP094_VERDICT_REVIEW_2026-09-27.md`), the EXP095 verdict review (`experiments/protocols/REVIEWS/EXP095_VERDICT_REVIEW_2026-09-28.md`), the frozen EXP094/EXP095 execution archives, and EXP093's signed pre-reg (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`) unless otherwise cited. No number is invented. Every statistic in §0.1/§4.2 was computed by this lane from the frozen archives (read-only CSV analysis, $0; no model executed, no weights touched).*
***No pilot is authorized by this draft.** Before any run: independent Law #14 review + SIGN (separate lane), then CEO execution clearance. CPU-only design ($0); no GPU contact under any circumstance.*

---

## 0. Law #15 block (binding, carried from LOG-4391; reshaped by the reach lemma §0.1)

**Precise question [HYPOTHESIS].** EXP094 killed the per-item static L11 direction at α=1.0 (0 flips, pure inertness) and EXP095 killed the "magic strength" rescue (≤1 flip at every α ∈ {0.25,…,4.0}, all p=1.0). The licensed carve-out that survived both kills is **conditionality**: the threshold account — "the push is real but too weak except where the baseline margin is within its reach." Does the killed per-item L11 direction move decisions when injected at the maximum interpretable strength inside the linear license (α=8.0, ratio 0.3792 < 1), restricted to the items whose baseline margin lies within the empirically-calibrated reach of the intervention? [HYPOTHESIS]

**Decision it changes.** **KILL** the headroom-gated rescue if the gated T-vs-B movement is < 6 flips with delivery confirmed — inertness is structural, not a headroom artifact; the threshold account is falsified within the linear license up to ratio 0.38; the static per-item family is closed conditionally too (the program's first mechanism family closed, conditionally — within the linear license up to ratio 0.38). **PIVOT (suggestive, unlicensed)** if the gated arm shows directional but sub-bar movement (≥2 flips, all wrong→right) — it motivates a powered follow-up design but licenses no positive, because the licensed positive is infeasible by construction (§4.2 — stated plainly, not hidden). **PIVOT (fragility)** if the gated B_wrong arm moves with T — the effect is nonspecific perturbation of fragile near-boundary items, not task geometry. All outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** The backlog's letter (gated injection at α=1.0) is infeasible — proven, not asserted (§0.1: the within-reach set at α=1.0 has exactly 1 member; the ≥6-flip discovery bar needs ≥6). A lower α gives a smaller reach and a weaker test; a higher α (16×) exits the interpretable regime (ratio 0.76, OOD/fragility risk dominates — declined in §6). The gated α=8.0 run — 102 injection passes (60 B + 21 T(8.0) + 21 B_wrong(8.0)), CPU, $0 — **is** the cheapest falsifier of the headroom rescue: the strongest push the linear license interpretably allows, restricted to exactly the items the threshold account says should flip.

**Quantitative prediction (pre-registered, bars).** On the frozen gated set G (|G|=21, §2.1.1): gated T-vs-B flips ≥ 6 AND McNemar-exact (doubling) p < 0.05 (single primary contrast — no Bonferroni) AND gated B_wrong flat (flips < 6 AND |ΔM| < 0.10) AND ΔM_T(G) > 0. **Declared infeasible by construction** (§4.2): at most 5 gated items are wrong at baseline, so max b = 5 → min p = 0.0625 — the directional positive cannot be earned. The pre-registered substitute for a directional signal is the step-5 suggestive PIVOT (≥2 flips, all wrong→right), which motivates follow-ups but licenses nothing.

**Breaking point (sharp, two levels).** (i) In-band: gated T-vs-B movement < 6 with delivery confirmed → the headroom-gated rescue is dead; KILL. (ii) License boundary: the design tests headroom-conditionality at α=8.0 (max band ratio 0.4740 < 1) only — the >0.4740-ratio regime (α=16 variant, declined §6) is untested, and non-static conditional mechanisms (attention-state-gated, dynamic, multi-layer) remain EXP096+ material. A gated zero must never be phrased as killing all conditional mechanisms — only the static headroom-gated variant. [INTERPRETATION of scope]

**The belief it tests (named, LOG-4391):** the licensed carve-out "gated and conditional variants survive" — overturned-by a directional gated signal (takes the PIVOT-suggestive form, since the licensed positive is infeasible) or deepened-by a gated zero at 8× strength (the carve-out dies with the family; inertness is structural). [INTERPRETATION]

### 0.1 The reach lemma (forcing result — why this draft deviates from the backlog's letter)

[OBSERVATION] Computed by this lane from the frozen EXP094 archive (`experiments/runs/EXP094_peritem_l11/out/per_item_records.csv`, SHA-256 `9ada6ef9d489aee959b56160053cbe7bdb7024e6c593cbf3a9ffbfd9b366d149`):

- Demonstrated reach at α=1.0: max over the 60 T-arm items of |margin_shift_vs_B| = **0.090155**.
- Within-reach set at α=1.0, G₁ = {i : |m_i^B| ≤ 0.090155}: **exactly 1 item** (`exp092_planetary_3hop_7`, m_B = +0.0645). That item did **not** flip in EXP094's T arm.
- The strict per-item directional gate {i : sign(s_i) = −sign(m_i^B) ∧ |s_i| ≥ |m_i^B|} is **empty** (proven — EXP094 had 0 flips, so no item's archived shift crossed its own margin).

[INTERPRETATION] The backlog's α=1.0 gated flip experiment is **infeasible by construction** (EXP079 lesson): the ≥6-flip discovery bar requires ≥6 flippable items; the within-reach set has 1. Any re-injection at an archived (item, α) would be deterministic archive re-reading (EXP095 demonstrated 60/60 bit-reproduction across a rebuilt environment), not an experiment. The concept is therefore preserved by gating at the maximum interpretable strength: the reach scaling law is **measured, not assumed** — max|shift|/α ∈ {0.0933, 0.0922, 0.0902, 0.0973, 0.1122} across the five archived α ∈ {0.25, 0.5, 1.0, 2.0, 4.0} (EXP095 archive) [OBSERVATION]. Nearest-anchor extrapolation: τ_8 = 2 × max|shift(α=4.0)| = 2 × 0.4488 = **0.8976 ≈ 0.90** → |G| = 21. The α=1.0→8.0 move is forced by the lemma, not chosen; the concept (inject only within-reach items) is unchanged.

---

## 1. Background and license

- **EXP094 binding facts [OBSERVATION, LOG-4375/4376/4377; verdict review §2]:** per-item L11 task-direction injection at α=1.0 on EXP092-B: B=T=R=36/60; ΔM_T=+0.0000; McNemar b=c=0 → p=1.0000 all nine contrasts; 0 flips across 120 injection item-arms despite nonzero margin shifts on every item (max |shift| = 0.090155) and G5 delivery rel_err 4.26e-07; Δθ=0 hash pin `ec276abe…` (LOG-331); degeneracy mean pairwise |cosine| = 0.7923 < 0.95. Licensed claim: per-item static L11 directions do not move decisions **at α=1.0**; gated/dynamic and multi-layer compositions untouched.
- **EXP095 binding facts [OBSERVATION, LOG-4400; verdict review §2]:** α-sweep {0.25, 0.5, 1.0, 2.0, 4.0}: T-vs-B flips = {0, 0, 0, 1, 1}; every McNemar p = 1.0 across all 5 α × 3 contrasts × 3 strata; foundation reproduced 60/60 per-item B agreement. Verdict: **REFUTED — the magic-strength rescue is dead on the licensed five-point grid**; inertness is strength-invariant over 16× (boundary-law graduation, scoped). No further static per-item L11 strength experiments are licensed.
- **Death-debt [FACT, LOG-4391]:** S5-4 pays EXP094's LOG-219 death-debt jointly with S5-1; deaths table records debt PAID on proposal (execution outstanding). This draft is the "pre-registered plan" the backlog row requires — **not a revival or an edit of EXP094/EXP095** (both runs are closed records). This document is a new unsigned file.
- **Mathematical license [THEOREM-adjacent linear-algebra fact, EXP093 signed pre-reg §License, cited by reference]:** let m(h) = logit(target) − logit(foil) be the correct-margin [DEFINITION, EXP093 §License]. The intervention sets h′ = h + α·d_i at L11; to first order, Δm_i ≈ α·⟨∇ₕm_i, d_i⟩. **License verdict: HOLDS for a test, not a conclusion.** Under the headroom rescue, items with |m_i^B| ≤ reach(α) flip when the push points toward the boundary; the gated set G (21 items within the calibrated reach at α=8.0) is where flips must concentrate — the rescue's best shot. Empirical calibration [OBSERVATION]: the reach scaling law above. Honest audits carried: (Gap 1) the τ extrapolation is 2× from the nearest measured anchor — disclosed, verified in-run (§4); (Gap 2) one bench — any verdict is bench-scoped to EXP092-B; (Gap 3) the gated set's baseline imbalance (5 wrong / 16 right; 13 A-first / 8 C-first) — stratum bars are relaxed to a heterogeneity veto, disclosed (§3 step 6).
- **Summit filter:** a directional gated signal would be the program's first conditional causal-steering signal at a non-readout layer — the conditional primitive the summit (autonomous self-steering) must build on. Caveat preserved: injection is externally applied, not self-computed — never described as an autonomy result. (The licensed positive is infeasible — §4.2 — so the summit upside takes the suggestive-PIVOT form.)

## 2. Design (frozen model, Δθ = 0; frozen EXP094 bundle path; single strength α=8.0)

### 2.1 Arms (pre-registered)

| Arm | Injection at L11 (readout-anchor position, per item i) | Coverage | Role |
|---|---|---|---|
| B | none (Δθ = 0) — single run per item | all 60 items | baseline — anchors EXP092-B; replication anchor; paired baseline for G |
| T(8.0) | per-item task direction d_i scaled to norm 8·0.0474·‖h_i^B‖₂ = 0.3792·‖h_i^B‖₂ | i ∈ G only (21 items) | test arm — the headroom-gated dose |
| B_wrong(8.0) | per-item **random** direction g_i (EXP094's frozen R-arm constructor, pinned seed → identical {g_i}) scaled to norm targeting T(8.0)'s per-item norm | i ∈ G only (21 items) | discriminant — must stay flat on the fragile gated set |

**{d_i}, {g_i} regeneration (frozen specification).** Identical to S5-1 v2 §2.1: regenerated from the frozen EXP094 constructor `experiments/runs/EXP094_peritem_l11/constructor.py`, hash-pinned `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361` [FACT, constructor manifest]; pre-run re-hash, mismatch → HOLD. G7 label-free attestation carries from EXP094's `constructor_manifest.json` (same frozen code + same P₀ (`e7e81496…f2601e11`) + same bench — code-identical, not re-audited). The {g_i} use the pinned R-arm seed.

#### 2.1.1 The gate G — exact specification (frozen, pre-computed, verified in-run)

- **Construction [DEFINITION]:** G = { i ∈ EXP092-B : |m_i^B| ≤ τ_8 }, where m_i^B is the archived EXP094 baseline logit-margin and τ_8 = 0.90 = 2 × max|shift(α=4.0)| (0.4488), the nearest-anchor extrapolation of the measured reach scaling law (§0.1). |G| = 21; frozen member list in Appendix A (13 A-first / 8 C-first; 5 wrong / 16 right at baseline).
- **Archive pin:** the gate is computed from `experiments/runs/EXP094_peritem_l11/out/per_item_records.csv`, SHA-256 `9ada6ef9d489aee959b56160053cbe7bdb7024e6c593cbf3a9ffbfd9b366d149` [FACT, computed by this lane]. The executor recomputes G from the pinned archive before any injection; the §3-step-0 gate-manifest check requires the recomputed member list to match Appendix A exactly — any divergence → HOLD (archive drift; never a silent re-gate).
- **Why a population band, not the strict per-item gate:** the strict gate {i : sign(s_i) = −sign(m_i^B) ∧ |s_i| ≥ |m_i^B|} is proven empty (§0.1) — a per-item headroom test is infeasible by construction (EXP079 lesson). The population band is the closest feasible realization of the licensed concept; the difference is disclosed here, not hidden.
- **"Flat" (pre-registered):** B_wrong(8.0) is flat on G iff flips(B_wrong vs B; G) < 6 AND |ΔM_Bwrong(G)| < 0.10, ΔM per EXP093's paired convention. **Disclosed asymmetry:** the gate selects near-boundary (fragile) items — B_wrong is *expected* to flip more here than on the full set (EXP094: 0 flips full-set). The unscaled <6 bar is therefore conservative: it makes the fragility-PIVOT (step 4) easier to hit and any directional T signal harder to mistake. **Joint-requirement correction (F1):** step-4 PIVOT (fragility) fires only on gated T(8.0) movement ≥ 6 **and** B_wrong ≥ 6 — if T < 6 while B_wrong moves, step-3 KILL fires first (first-match-wins), and B_wrong movement on fragile items strengthens that KILL (the items are flippable by large nudges, yet the task direction does not move them). B_wrong movement alone is never a discounted CONTINUE.

### 2.2 Strength (pre-registered, single point)

α = 8.0 fixed. Per-item perturbation_ratio target 8·0.0474 = **0.3792**; G5-style band (±25%): **[0.2844, 0.4740]**. Max band ratio 0.4740 < 1 → the design stays inside the linear-perturbation license (F9 precedent: α=8.0 → 0.3792 was already established as inside-license). **No other α is licensed** — this is not a dose-response; the question is conditionality, not strength (strength is EXP095's closed territory).

### 2.3 Budget (pre-registered)

- **102 injection passes** (60 B + 21 T(8.0) + 21 B_wrong(8.0)); **+60 reserved** for delivery/margin-verification repeats and gate-manifest recomputation → **162 expected; hard cap 400.** Spend beyond 162 requires a logged, pre-cleared exception; the 400 hard cap is not waivable within this pre-registration (a change is a new design, not an edit). CPU only, $0.

### 2.4 Statistics (pre-registered)

- **McNemar exact, doubling convention** (EXP094's convention) on paired decisions over G: T(8.0)-vs-B, B_wrong(8.0)-vs-B, T(8.0)-vs-B_wrong(8.0) [diagnostic-only — Law #9 hygiene, cf. S5-1 v2 F13].
- **ΔM** per EXP093's paired convention over G; **Tango 95% CIs** on the paired differences.
- **DELTA_BAR = 0.10**; **ALPHA_disc = 0.05** — single primary contrast, no Bonferroni (unlike S5-1's five α). **Movement gate: ≥ 6 flips** (program standard; the McNemar-feasible minimum at 0.05: b=6,c=0 → p=0.03125).
- **Correctness:** margin > 0 (strict), EXP094's convention. **Tie gate:** ties/42 > 5% on the gated injection rows → RUN-INVALID (no verdict licensed).
- **In-run reach verification (pre-registered):** after the run, compute realized max|shift(8.0)| over the gated T rows. If > 1.125 (= 1.25 × τ_8), the gate under-covered → any KILL is reported with the under-coverage disclosed, plus flips on the τ=1.125 superset as a non-decision diagnostic. If ≤ 1.125, coverage is confirmed. **Symmetric over-coverage rule (pre-registered, F2):** if realized max|shift(8.0)| < 0.5 × τ_8 = 0.45, the reach overshot — the step-3 KILL verdict must then carry the "low-margin-items form" fence inline (the strict-reach form softens to "even at maximum leverage on low-margin items, nothing moved"), with the realized reach reported.

---

## 3. Decision table (pre-registered)

**Arm-routing rule (binding):** B runs on all 60 items; T(8.0) and B_wrong(8.0) run exactly on the frozen Appendix-A member list — no additions, no substitutions. All contrasts are paired over G against the B vector; stratum membership is the bench pin, fixed before inspection. No post-hoc re-routing — structurally impossible under frozen routing.

**Binding evaluation order (first match wins).** Exactly one step is earned:

0. **Foundation gates.** (i) Constructor re-hash vs `5e03f206…917f361` → mismatch: **HOLD**. (ii) Per-item B-decision agreement vs the archived EXP094 B vector: 60/60 required → any disagreement: **HOLD**. (iii) Gate-manifest reproduction: recomputed G from the pinned archive must equal Appendix A exactly (k=21, member-for-member) → divergence: **HOLD**. (iv) Degeneracy sanity: |recomputed mean|cos| − 0.7923| > 0.05 → **HOLD** (constructor regeneration broken). A HOLD triggers the pre-registered diagnosis lane (re-hash weights vs LOG-331 pin, verify thread pinning, byte-compare prompts, re-verify archive SHA-256) — **never a silent re-run**. *Foundation guards only; no verdict on the hypothesis.*
1. **Delivery.** G5 probe on the 42 gated injection rows: per-row perturbation_ratio within [0.2844, 0.4740], margin shift recorded vs B. ≤2 rows out of band → those items excluded from all contrasts (no verdict licensed on them). >2 rows out of band, or any zero-norm d_i → **HOLD + diagnose** (common-cause suspected). *(Maps to: Inconclusive.)*
2. **Degeneracy.** Mean pairwise |cosine| over regenerated {d_i} ≥ 0.95 → **Underdetermined** — never KILL on a powerless test (R4 rule). *(Maps to: Underdetermined.)*
3. **Gated KILL (the conditional kill).** Gated T(8.0)-vs-B movement < 6 → **Refuted: the headroom-gated rescue of the per-item static family is refuted on the licensed reach-calibrated set at α=8.0** — inertness is structural, not a headroom artifact; the threshold account ("the push is real but too weak except near the boundary") is falsified within the linear license up to ratio 0.38 at the rescue's best shot; the static per-item family is closed conditionally too. *(Maps to: Refuted.)*
4. **Specificity PIVOT.** Gated T(8.0) movement ≥ 6 AND: (a) gated B_wrong moves ≥ 6 → **PIVOT** (fragility — near-boundary items flip under any large nudge; the effect is nonspecific perturbation, not task geometry); (b) T-vs-B McNemar p ≥ 0.05 → **PIVOT** (movement without directional evidence — e.g. b≈c splits). *(Maps to: Not supported for the directional claim.)*
5. **Suggestive-signal PIVOT (pre-registered substitute for the infeasible positive).** Gated T(8.0) flips ∈ [2,5], **all** wrong→right (c=0), ΔM_T(G) > 0, and gated B_wrong flat → **PIVOT: unlicensed directional signal** — motivates a powered follow-up (e.g. the declined α=16 variant, §6 item 7, or a larger bench) but licenses no positive and narrows no kill. *(Maps to: Not supported for the directional claim.)* Rationale, stated plainly: the licensed positive (flips ≥ 6 AND p < 0.05 AND B_wrong flat AND ΔM_T > 0) is **infeasible by construction** — max b = 5 (5 wrong-at-baseline gated items) → min p = 0.0625 (§4.2, proven). Had the archives shown ≥6 wrong-in-reach items, the CONTINUE branch would have been pre-registered with the standard bars (counterfactual pre-registration — the bars were not chosen to make CONTINUE impossible; the data made it impossible).
6. **Otherwise → PIVOT** *(maps to: Not supported for the global claim)*, with named sub-cases: (a) sign-heterogeneous movement across G or strata (one stratum ΔM_T < −0.05 while the other is positive) — global conditional claim dead; (b) **consistent wrong-direction steering** (ΔM_T(G) < −0.10 with p < 0.05 and B_wrong flat) — a causal channel exists, the constructor is mis-signed; sign story is EXP096+ material, never KILL.

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted); the parenthetical mappings bind each step to its verdict. No banned language. No EXP094/EXP095 claim is altered. **Scope fence:** the >0.4740-ratio regime, non-static conditional mechanisms (attention-state-gated, dynamic, multi-layer), other benches/models/layers remain EXP096+ material regardless of outcome.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post == LOG-331 pin `ec276abe…`; any mismatch voids the run (Law #13).
- **Frozen constructor + frozen gate archive:** re-hash `experiments/runs/EXP094_peritem_l11/constructor.py` (pin `5e03f206…917f361`) and the EXP094 records CSV (pin `9ada6ef9…b366d149`) before any run; mismatch on either → HOLD. G7 attestation carries from EXP094's `constructor_manifest.json` — code-identical.
- **G5-style exact-delivery probe:** per gated row, perturbation_ratio target 0.3792, band [0.2844, 0.4740] (§2.2); aggregation per §3 step 1. Margin shift vs B recorded per gated item (reached-the-logits check, carried from EXP094).
- **Per-item records (Law #13):** every (item, arm) persists: top-1 decision, margin (EXP093's logit-margin, cited by reference), perturbation_ratio, margin shift vs B, gate-membership flag. **Non-negotiable.**
- **Arm-routing rule:** binding frozen routing (§3); no post-hoc re-routing.
- **Tie gate:** ties/42 > 5% on gated injection rows → RUN-INVALID.
- **Thread pinning:** torch intra-op thread count pinned to the EXP092/EXP094 extraction value and asserted before condition B, per EXP093 G4.

### 4.1 Degeneracy analysis of every diagnostic (LOG-4338 lesson — constant-data unit tests, pre-registered)

Each diagnostic states what it returns on degenerate input. A diagnostic that can manufacture a positive from degenerate input is disqualified; all below fail safe:

1. **The gate G itself.** τ_8 = 0 on degenerate archives (all shifts zero) → G = {i : m_i^B = 0} — empty on real data → the §4.2 feasibility check fails → run not licensed (HOLD/Underdetermined), never a verdict. Archive-hash mismatch → §3-step-0 HOLD before any injection. Recomputed G ≠ Appendix A → HOLD. The gate cannot manufacture a positive: it only selects rows.
2. **McNemar exact (doubling) on G.** Constant input (b = c = 0): p = 1.0000 → step-3 KILL, cannot manufacture signal. Adversarial input (b=21, c=0): p ≈ 9.5×10⁻⁷ — the statistic is well-defined on the gated set. Unit test: all-identical decision vectors → p = 1.0 asserted.
3. **ΔM paired difference on G.** Zero-variance input → ΔM = 0, Tango CI = [0,0] → cannot clear DELTA_BAR → fails safe.
4. **Suggestive-PIVOT diagnostic (step 5).** 0 flips → step 3 fires first (first-match-wins); the suggestive branch cannot fire without actual directional flips. On 1 flip: neither step 3's complement nor step 5 fires → falls to step 6 PIVOT (correct: a single flip is noise, cf. EXP095's verdict review).
5. **B_wrong flatness on the fragile set — the dangerous direction.** Dead instrument → B_wrong flat AND T flat → step-3 KILL (correct). The asymmetry (fragile items selected) is conservative: it can only push toward step-4 PIVOT, never toward a false positive.
6. **Degeneracy gate (mean pairwise |cosine|).** 21 identical vectors → 1.0 ≥ 0.95 → Underdetermined (correct). Zero-norm d_i → §3-step-1 HOLD before the gate is computed (never divide by zero).

### 4.2 Probe-feasibility algebra (EXP079 lesson — proved, not asserted)

- **The reach lemma (§0.1) restated as algebra:** at α=1.0, |G₁| = 1 < 6 = minimum significant table → the α=1.0 gated flip experiment is infeasible by construction. The α=8.0 design exists because the lemma forces it.
- **Positive infeasibility (the honest core):** on the frozen G (|G|=21), exactly 5 items are wrong at baseline → max wrong→right flips b_max = 5 → min McNemar-exact p = 2·2⁻⁵ = 0.0625 > 0.05. **The licensed directional positive is unreachable by construction.** The design therefore pre-registers no CONTINUE branch; step 5 (suggestive PIVOT) is the honest substitute. Counterfactual: had b_max ≥ 6, the standard CONTINUE (flips ≥ 6, p < 0.05, B_wrong flat, ΔM_T > 0) would have been pre-registered.
- **KILL feasibility:** needs gated movement < 6 — satisfiable (the null predicts ~0–1). **PIVOT feasibility:** step 4 needs ≥6 flips (feasible: b+c ≥ 6 includes wrong-way flips); step 5 needs 2–5 all-right-way flips (feasible).
- **B_wrong flat bar** (<6 flips, |ΔM| < 0.10 on G): feasible by the same arithmetic; conservative on the fragile set (disclosed §2.1.1).
- **Delivery band** [0.2844, 0.4740]: max ratio 0.4740 < 1 → inside the linear license; no extrapolation beyond the licensed regime.
- **Budget:** 102 + 60 = 162 expected ≤ 400 hard cap. **Gate recomputation:** deterministic on the pinned archive — feasible by construction.
- **Conclusion:** every pre-registered bar except the (deliberately absent) CONTINUE is reachable by construction. If Law #14's independent recomputation of this algebra disagrees, the run does not proceed.

### 4.3 Verdict discipline

The §3 evaluation order, five permitted verdicts with step→verdict mappings, no post-hoc table edits; a design change is a new experiment number, never a silent edit. **$0 compute for this draft:** on-paper only (plus read-only CSV analysis of committed archives for the reach lemma). No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, stratum, arm ∈ {B, T(8.0), B_wrong(8.0)}, gate member y/n, top-1 decision, margin, perturbation_ratio, margin shift vs B). Margin convention: EXP093's logit-margin, cited by reference — not redefined at execution time.
2. Gate manifest: recomputed Appendix-A member list (must match exactly), archive SHA-256 (must equal `9ada6ef9…b366d149`), τ_8 derivation (2 × 0.4488), constructor SHA-256, P₀ hash, R-arm seed, G7 carry-over reference, per-item d_i/g_i norms, pairwise |cosine| summary.
3. Δθ = 0 hash pre/post; environment + seed + thread-count manifest (Law #13 reproducibility).
4. Delivery probe log: per gated row perturbation_ratio vs [0.2844, 0.4740]; PASS/FAIL aggregation per §3 step 1; in-run reach verification (realized max|shift(8.0)| vs the 1.125 under-coverage tripwire).
5. Stratum table: 3 strata (aggregate / A-first / C-first) × 3 contrasts (T-vs-B, B_wrong-vs-B, T-vs-B_wrong [diagnostic-only]): ΔM, McNemar b/c/p, Tango 95% CI — 27 cells, machine-written. (Stratum bars relaxed: report per-stratum ΔM; step-6a veto on sign-heterogeneity.)
6. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition — including the step-0 foundation values (B agreement vector, gate-manifest match, degeneracy sanity).

---

## 6. Known design risks — what Law #14 should try to break (falsification-first)

Ranked by how badly each would wound the licensed verdicts:

1. **The τ extrapolation.** "Within reach" at α=8.0 rests on the measured scaling law (max|shift|/α ∈ [0.0902, 0.1122], five archived α) holding to 8×. If Law #14 rules the 2×-from-nearest-anchor extrapolation unprincipled, the gate degrades to "low-margin items" and the KILL's bite softens to "even at maximum leverage, nothing moved" — still a kill of the general headroom form, but not of the strict reach form. **Attack:** demand the α=16 design (§6 item 7) instead, or accept the extrapolation with the in-run verification (§2.4) as the tripwire.
2. **No CONTINUE branch.** A critic may rule a KILL-only design unlicensable as a "test" — it cannot confirm the alternative it was built to give a chance. **Counter (for Law #14 to stress):** the infeasibility is proven from frozen archives (§4.2), not chosen for convenience; the existential rescue claim ("there exists a headroom regime where the direction works") IS falsifiable here — failing at its best shot kills it; the counterfactual CONTINUE is stated so the bars can't be accused of being rigged. Either ruling must be pre-registered before the run.
3. **B_wrong fragility PIVOT — risk framing corrected (F1).** The gate selects near-boundary items; at α=8.0 (ratio 0.38) a large random nudge may flip ≥6 of 21 fragile items. **Correction:** step-4 PIVOT (fragility) requires gated T(8.0) movement ≥ 6 **and** B_wrong ≥ 6 jointly — B_wrong ≥ 6 with T < 6 fires step-3 KILL (first-match-wins) and strengthens it (flippable-by-nudge items not moved by the task direction). The most probable outcome is therefore honest and productive: a flat T on flippable items is the KILL's best evidence. **Attack:** argue the α should drop to 4.0 (cleaner discriminant, cf. EXP095's 1/1 B_wrong split) — counter: α=4.0 outcomes are archived (deterministic re-read, not an experiment); the α is forced to be new.
4. **Deviation from the backlog's letter (α=1.0 → 8.0).** Law #14 must confirm the reach-lemma forcing is legitimate and not scope creep into S5-1's strength territory. Fence offered: single α, no curve, question is conditionality not dose-response; EXP095's verdict explicitly bars further strength experiments — this design is conditional-first, strength-second.
5. **Gated-set imbalance (5 wrong / 16 right; 13 A-first / 8 C-first).** Stratum consistency is relaxed to a heterogeneity veto (step 6a); a critic may call the positive-detection machinery weak. Disclosed; the KILL (the design's primary product) does not depend on strata.
6. **Population band vs the "true" per-item gate.** The strict per-item gate is proven empty — a critic could argue the TRUE headroom test is therefore impossible and S5-4 tests a strawman. **Counter:** the population band is the closest feasible realization; the strict form's death is itself reported (reach lemma) rather than hidden; the general form ("headroom helps") is what the band tests.
7. **The declined α=16 variant.** Feasible on paper (τ=1.44 → k=35, 9 wrong-at-baseline → positive feasible): gated T(16.0)/B_wrong(16.0) on 35 items. **Declined:** ratio 0.76 approaches the license boundary; OOD/fragility risk makes the B_wrong-PIVOT the likely outcome (no closure); the 16× reach extrapolation is speculative vs the 2× used here. Preserved as EXP096+ material — licensed as follow-up ONLY if this design PIVOTs on fragility (moot) or yields a suggestive signal (then α=16 is the powered follow-up).
8. **Sign-corrected variant considered and killed.** Per-item sign(-s_i^arch)·d_i would push every item's archived shift toward the boundary — but the reach lemma kills it: sign cannot create reach (|s_i| < |m_i^B| for 59/60 items regardless of sign). Reported so Law #14 need not re-derive it.
9. **Archive-dependence of the gate.** If EXP094's archive is ever revised, Appendix A changes — mitigated by the frozen SHA-256 pin and the §3-step-0 reproduction check (divergence → HOLD, never silent re-gating).
10. **The untested >0.4740-ratio regime.** Explicit: a gated zero here must never be cited against the threshold account above ratio 0.4740 — the fence is in the verdict language (§3 step 3), but retelling drift is the perennial risk.

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not alter EXP094's/EXP095's closed run records, the S5-1 drafts, or any signed artifact; does not touch weights.
- Does not invent numbers — every value cites LOG-4391, LOG-4400, the EXP094/EXP095 verdict reviews, the frozen execution archives (read-only analysis noted), or EXP093's signed pre-reg, except the gate construction (§2.1.1), the α=8.0 selection (forced by §0.1), the step-5 suggestive branch, and the declined α=16 variant — which are frozen design choices by this lane, flagged for Law #14 above.
- Does not license a directional positive (infeasible — §4.2), interpolation, the >0.4740-ratio regime, α=16, non-static conditional mechanisms, or multi-layer compositions.

---

## 8. Next steps

Independent **Law #14 review** of this draft (separate lane — pre-assigned LOG number by the dispatcher) → SIGN or SIGN-WITH-FIXES → repair lane if needed → independent delta re-verification → **CEO execution clearance** → run (CPU, ≤162 passes expected, 400 hard cap). **Pilot NOT authorized until all complete. No GPU contact under any circumstance.**

---

## Appendix A — Frozen gate member list (G, τ_8 = 0.90; |G| = 21)

*Computed 2026-09-28 from the pinned EXP094 archive (SHA-256 `9ada6ef9d489aee959b56160053cbe7bdb7024e6c593cbf3a9ffbfd9b366d149`). The executor must reproduce this list exactly (§3 step 0).*

| item_id | m_B (archived) | stratum |
|---|---|---|
| exp092_elemental_2hop_0 | +0.6628 | C-first |
| exp092_elemental_2hop_10 | +0.6960 | C-first |
| exp092_elemental_2hop_11 | +0.5983 | A-first |
| exp092_elemental_2hop_2 | −0.7389 | C-first |
| exp092_elemental_2hop_5 | +0.3917 | A-first |
| exp092_elemental_2hop_9 | +0.1469 | A-first |
| exp092_elemental_3hop_0 | +0.8106 | C-first |
| exp092_elemental_3hop_1 | +0.4430 | A-first |
| exp092_elemental_3hop_11 | +0.5651 | A-first |
| exp092_elemental_3hop_13 | +0.3956 | A-first |
| exp092_elemental_3hop_3 | +0.3274 | A-first |
| exp092_planetary_2hop_0 | +0.2375 | A-first |
| exp092_planetary_2hop_1 | −0.3727 | C-first |
| exp092_planetary_2hop_12 | +0.4389 | A-first |
| exp092_planetary_2hop_13 | −0.8483 | C-first |
| exp092_planetary_2hop_2 | −0.1281 | A-first |
| exp092_planetary_2hop_8 | +0.4902 | A-first |
| exp092_planetary_2hop_9 | −0.1558 | C-first |
| exp092_planetary_3hop_0 | +0.7376 | A-first |
| exp092_planetary_3hop_10 | +0.8904 | A-first |
| exp092_planetary_3hop_7 | +0.0645 | C-first |

*Baseline: 5 wrong / 16 right; 13 A-first / 8 C-first.*

---

*Draft prepared 2026-09-28 by the S5-4 pre-registration drafter (LOG-4401), licensed by LOG-4391 (PROPOSAL) and LOG-4400 (EXP095 verdict: S5-4 is the live successor lane). DRAFT, UNSIGNED — Law #14 review requested but not performed; no finding is closed. On paper only ($0; read-only archive analysis for the reach lemma), CPU-only design. No signed protocol file was edited; this is a new unsigned file.*
