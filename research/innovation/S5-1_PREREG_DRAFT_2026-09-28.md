# S5-1 — α-Sweep Dose-Response on the Killed Per-Item L11 Direction — Pre-registration DRAFT (UNSIGNED)

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. NOT reviewed. No experiment number minted (S5-1 is EXP094+ material; numbering happens after Law #14 review + CEO license).*
*Licensing chain: LOG-4373–4377 (EXP094 executed; Refuted/KILL, pure inertness; Law #14 SIGN) → LOG-4390 (founder gap review ranks the α-sweep the single highest-value missing experiment) → LOG-4391 (Monday idea session: S5-1 born as PROPOSAL; Law-#15 packet on record — linear-perturbation license, threshold-account breaking point ‖δ‖/‖r‖>1) → LOG-4394 (this draft).*
*All values below are from LOG-4391, LOG-4375/4376/4377, the EXP094 verdict review (`experiments/protocols/REVIEWS/EXP094_VERDICT_REVIEW_2026-09-27.md`), and EXP093's signed pre-reg (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`) unless otherwise cited. No number is invented.*
***No pilot is authorized by this draft.** Before any run: independent Law #14 review + SIGN (separate lane), then CEO execution clearance. CPU-only design ($0); no GPU contact under any circumstance.*

---

## 0. Law #15 block (binding, carried from LOG-4391)

**Precise question [HYPOTHESIS].** EXP094 (binding Refuted/KILL, LOG-4375/4376/4377) showed that static injection of the **per-item** layer-11 task direction at α=1.0 (perturbation_ratio = 0.0474) on EXP092-B moves zero decisions: B = T = R = 36/60, ΔM_T = +0.0000, McNemar b = c = 0 → p = 1.0000 on all nine contrasts, zero flips across 120 injection item-arms despite nonzero margin shifts on every item and genuinely established G5 delivery (rel_err 4.26e-07) — pure inertness. The licensed claim is scoped: it falsifies causal influence of the per-item static direction **at α = 1.0** only. **Is that kill a point or a curve?** Map ΔM(α) and flip-rate(α) over α ∈ {0.25, 0.5, 1.0, 2.0, 4.0} — a 16× strength range — on the same EXP092-B 60 items, with a norm-matched discriminant arm at every α. [HYPOTHESIS]

**Decision it changes.** **KILL** the "magic strength" hope if all-α ΔM = 0 and flips = 0 — the inertness is not a strength artifact; the family license becomes strength-invariant over the licensed grid (boundary-law graduation, scoped — §3 step 3). **CONTINUE** (licensed positive only) if ∃α ∈ {0.25, 0.5, 2.0, 4.0} with T-vs-B flips ≥ 6 AND McNemar p < 0.05 AND B_wrong(α) flat AND stratum-consistent — the EXP094 kill narrows to its α=1 band and the first strength-licensed causal-steering signal at a non-readout layer is earned, scoped to the winning α on EXP092-B. **PIVOT** if movement appears but the discriminant arm moves with it (strength artifact, not geometry) or movement lacks directional significance — the rescue is nonspecific; conditional/artifact designs become EXP095+ material. All three outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** No single-α pilot falsifies the ∃α claim: a peaked dose-response (works at α=0.5, dead at α=4.0) survives any one-point null, and a high-α-only effect survives any low-α null. The 5-point sweep — 5 α × 60 items × 3 arms = 900 passes, CPU, $0 — **is** the cheapest test of the dose-response shape. The cheapest internal falsifier of the foundation is the α=1.0 replication gate (§3 step 0): if EXP094's exact condition does not reproduce, nothing downstream is licensable.

**Quantitative prediction (pre-registered, bars).** Per-α, on T-vs-B paired decisions: flips ≥ 6 AND McNemar-exact (doubling) p < 0.05 AND B_wrong(α) flat (flips < 6 AND |ΔM| < 0.10) AND ΔM_T(α) > 0 in all three strata (aggregate / A-first / C-first, strict). The B_wrong-flatness conjunct is non-negotiable: a strength-mediated nonspecific effect predicts T(α) and B_wrong(α) moving together; only task-geometry steering predicts T(α) moving while B_wrong(α) stays flat.

**Breaking point (sharp, two levels).** (i) In-band: all-α T-vs-B movement < 6 → the magic-strength hope is dead on the licensed grid; KILL. (ii) License boundary: the linear-perturbation license is licensed only while ‖δ‖/‖r‖ ≲ 1 (threshold account, LOG-4391). This design's maximum is α=4.0 → ratio 0.1896 < 1 — the design stays inside its license, and the >1 breaking point ("push too weak" exhausted) is **untested by this design**. A flat zero through α=4.0 must never be phrased as killing the threshold account itself — only the in-band magic-strength hope. [INTERPRETATION of scope]

**The belief it tests (named, LOG-4391):** "the EXP094 kill is about geometry" — overturned-by "it was about strength" (a positive band at some α) or deepened-by "inert as a function of strength" (flat zero over two orders of magnitude — a paper-worthy law). [INTERPRETATION]

---

## 1. Background and license

- **EXP094 binding facts [OBSERVATION, LOG-4375/4376/4377; verdict review §2]:** per-item L11 task-direction injection at α=1.0 on EXP092-B: B=T=R=36/60; ΔM_T=+0.0000, ΔM_R=+0.0000; McNemar b=c=0 → p=1.0000 all nine contrasts; movement 0 < 6; 0 ties/180; G5 band [0.0355, 0.0593] with 0/120 violations; execution rel_err 4.26e-07; Δθ=0 hash pin `ec276abe…` (LOG-331); degeneracy statistic mean pairwise |cosine| = 0.7923 < 0.95. Licensed claim: per-item static L11 directions do not move decisions **at α=1.0**; gated/dynamic and multi-layer compositions untouched.
- **Death-debt [FACT, LOG-4391]:** S5-1 pays EXP094's LOG-219 death-debt jointly with S5-4; deaths table records debt PAID on proposal (execution outstanding). This draft is the "pre-registered plan" the backlog row requires — **not a revival or an edit of EXP094's design** (EXP094 has no signed protocol file to edit; its run is a closed record). This document is a new unsigned file.
- **Mathematical license [THEOREM-adjacent linear-algebra fact, EXP093 signed pre-reg §License, cited by reference]:** let m(h) = logit(target) − logit(foil) be the correct-margin [DEFINITION, EXP093 §License]. The intervention sets h′ = h + α·d_i at L11; to first order, Δm_i ≈ α·⟨∇ₕm_i, d_i⟩. **License verdict: HOLDS for a test, not a conclusion** — the license licenses the sweep, not a positive. Under the magic-strength hope, ⟨∇m_i, d_i⟩ ≠ 0 for a substantial item subset, so |Δm_i| grows linearly in α and items with baseline |m_i| < α·|⟨∇m_i,d_i⟩| flip: flip-rate(α) is then non-decreasing in α (within the linear regime) and some grid α clears the §0 bars. EXP094's datum — nonzero margin shifts on every item at α=1 yet zero flips — is compatible with |⟨∇m,d⟩| small-but-nonzero (predicts flips emerging by α=4, i.e. 4× the shift) **or** with pure jitter (predicts no α helps: the KILL branch). The sweep separates exactly these two readings. Honest audits carried: (Gap 1) α-grid resolution — a "magic" peak narrower than the grid spacing is invisible; the KILL is scoped to the licensed grid, never to "all strengths" (see §4); (Gap 2) one bench — any CONTINUE is bench-scoped to EXP092-B; (Gap 3) multiplicity — five α at ALPHA=0.05 each carry family-wise false-positive ≈ 1−0.95⁵ ≈ 0.226; the ≥6-flip + B_wrong-flat conjunction is the pre-registered mitigation, NOT a correction — disclosed, not hidden (§4, reviewer item 1).
- **Summit filter:** a licensed positive would be the program's first strength-licensed causal-steering signal at a non-readout layer — the dose-response primitive the summit (autonomous self-steering) must build on. Caveat preserved: injection is externally applied, not self-computed — never described as an autonomy result.

---

## 2. Design (frozen model, Δθ = 0; frozen EXP094 bundle path)

### 2.1 Arms (pre-registered)

| Arm | Injection at L11 (readout-anchor position, per item i) | Role |
|---|---|---|
| B | none (Δθ = 0) | baseline — anchors EXP092-B; replication anchor at α=1.0 |
| T(α) | per-item task direction d_i scaled to norm α·0.0474·‖h_i^B‖₂ | test arm — the dose |
| B_wrong(α) | per-item **random** direction g_i (EXP094's frozen R-arm constructor, pinned seed → identical {g_i}) scaled to norm α·‖d_i‖₂ (exactly T(α)'s per-item norm) | discriminant — the arm that must stay flat |

**{d_i} regeneration (frozen specification).** The {d_i} vectors were not persisted by EXP094 (verdict review O1 — only norms). The executor regenerates them from the frozen EXP094 constructor `experiments/runs/EXP094_peritem_l11/constructor.py`, hash-pinned `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361` [FACT, constructor manifest]. Pre-run: re-hash the constructor; mismatch vs the pin → HOLD (do not proceed). The G7 label-free attestation (label-swap max abs diff 0.0, cross-item isolation) carries from EXP094's `constructor_manifest_run.json` — same frozen code + same P₀ (`e7e81496…f2601e11`) + same bench, so the attestation is code-identical, not re-audited per α. The {g_i} are regenerated from the same frozen R-arm constructor with the pinned seed (§5 item 2 of EXP094's manifest).

#### 2.1.1 B_wrong(α) — exact specification (what it rules out)

- **Construction [DEFINITION]:** for item i and strength α, g_i drawn from the isotropic Gaussian in the 1024-dimensional L11 residual space (Pythia-410m hidden_size = 1024; the "512" in EXP094's draft docstring was a ruled-zero-content erratum — verdict review §7), normalized to unit norm, then scaled: B_wrong(α,i) = α·‖d_i‖₂·(g_i/‖g_i‖₂). Task-free by construction (seed-pinned, label-free inputs only).
- **"Flat" (pre-registered):** B_wrong(α) is flat iff flips(B_wrong(α) vs B(α)) < 6 AND |ΔM_Bwrong(α)| < 0.10, where ΔM uses EXP093's paired convention ΔM = (1/n)Σ[correct_X(i) − correct_B(i)].
- **What it rules out:** the live alternative at high α is the **perturbation-strength artifact** — EXP093's signed pre-reg states it explicitly: "Any intervention perturbs the residual stream; a perturbation alone can flip near-zero-margin decisions (S2's mean margin was −0.0018 — decisions are fragile)." At α=4.0 the injected norm is 0.1896 of the residual norm; a nonspecific large-nudge effect (fragile margins, OOD activations) predicts B_wrong(α) flipping alongside T(α). The B_wrong arm has exactly T(α)'s per-item norms at every α — the **only** difference between the arms is direction content (task-derived vs isotropic random). If T(α) moves while B_wrong(α) stays flat, the strength artifact is priced out; if both move, the effect is nonspecific → PIVOT (§3 step 4a), never CONTINUE.
- **Why not −d_i:** the wrong-sign arm tests sign-symmetry, a question EXP093's ±v design already probed; the dangerous confound for a *strength* sweep is strength-mediated nonspecific flips, which the norm-matched random arm controls directly. (A shuffled-item variant d_{π(i)} — "any task-derived direction" vs "this item's direction" — would be strictly stronger; not in the licensed 3-arm design; flagged as reviewer item 3.)

### 2.2 Strength grid (pre-registered)

α ∈ {0.25, 0.5, 1.0, 2.0, 4.0}; per-item perturbation_ratio targets α·0.0474 = {0.01185, 0.0237, 0.0474, 0.0948, 0.1896}. G5-style per-α bands (±25%): [0.00889, 0.01481], [0.01778, 0.02963], [0.0355, 0.0593], [0.0711, 0.1185], [0.1422, 0.2370]. **No interpolation between grid points is licensed** — each α is an independent pre-registered test; the "curve" is five measured points, not a fitted function.

### 2.3 Budget (pre-registered)

- **900 injection passes** (5 α × 60 items × 3 arms); **+150 reserved** for delivery/margin-verification repeats → **1050 expected; hard cap 1300.** Spend beyond 1050 requires a logged, pre-cleared exception; the 1300 hard cap is not waivable within this pre-registration (a change is a new design, not an edit). CPU only, $0. (B is re-run per α — 300 B passes — giving five independent baseline replications and within-(α,item) pairing; the pairing structure is B(α,i) vs T(α,i) vs B_wrong(α,i).)

### 2.4 Statistics (pre-registered)

- **McNemar exact, doubling convention** (EXP094's convention, verdict review §1) on paired decisions, per α: T(α)-vs-B(α), B_wrong(α)-vs-B(α), T(α)-vs-B_wrong(α).
- **ΔM** per EXP093's paired convention; **Tango 95% CIs** on the paired differences.
- **DELTA_BAR = 0.10, ALPHA = 0.05** — verbatim bars, no post-hoc movement. **Movement gate: ≥ 6 flips** (the McNemar-feasible minimum — §4).
- **Correctness:** margin > 0 (strict), EXP094's convention. **Tie gate:** ties/180 > 5% at any α → that α RUN-INVALID (excluded, no verdict licensed there).
- **Multiplicity disclosure (not a correction):** five α each at ALPHA=0.05 → family-wise ≈ 0.226 under the global null. The CONTINUE bar's conjunction (flips ≥ 6 AND p < 0.05 AND B_wrong flat AND stratum-consistent) is the pre-registered false-positive mitigation. A CONTINUE earned at exactly one α with p ∈ [0.01, 0.05) is reported with the multiplicity caveat attached — Law #14 item 1.

---

## 3. Decision table (pre-registered)

**Arm-routing rule (binding):** every one of the 60 EXP092-B items receives all three arms at all five α (full within-(α,item) pairing); all contrasts are paired; no item excluded from any contrast; stratum membership (aggregate / A-first / C-first, 30/30) is the bench pin, fixed before inspection. No post-hoc re-routing — structurally impossible under full pairing.

**Binding evaluation order (first match wins).** Exactly one step is earned:

0. **Replication anchor (α = 1.0 — the EXP094 point).** B(1.0) ≠ 36/60 correct → **HOLD** (bench drift; deterministic CPU + byte-identical prompts + thread pinning per EXP093 G4 must reproduce — EXP094 demonstrated it). T(1.0)-vs-B(1.0) movement ≥ 6 → **HOLD** (EXP094 non-replication — the kill's foundation is unstable; no sweep verdict licensable). *Neither outcome is a verdict on the sweep; both are foundation guards.* (A positive can therefore only be earned at α ∈ {0.25, 0.5, 2.0, 4.0}.)
1. **Delivery.** Per-α G5 aggregation rule: probe PASS(α) iff ≥ 58/60 items sit within the §2.2 band for that α with margin shift recorded vs B(α). α=1.0 FAIL → **Inconclusive/HOLD** (whole run — the anchor is broken). Any other α FAIL → that α excluded (no verdict licensed there); remaining α proceed. *(Maps to: Inconclusive.)*
2. **Degeneracy.** Mean pairwise |cosine| over regenerated {d_i} ≥ 0.95 → **Underdetermined** — never KILL on a powerless test (R4 rule). Sanity companion (pre-registered): |recomputed value − 0.7923| > 0.05 → **HOLD** (constructor regeneration broken — the {d_i} are not EXP094's). *(Maps to: Underdetermined.)*
3. **All-α KILL (the in-band kill).** T(α)-vs-B(α) movement < 6 at **every** α ∈ {0.25, 0.5, 1.0, 2.0, 4.0} → **Refuted (KILL family):** the magic-strength hope is dead on the licensed grid; inertness is not a strength artifact; the family license becomes strength-invariant over a 16× strength range — boundary-law graduation **scoped to the licensed grid** (a narrower magic peak between grid points is not ruled out — §4 Gap 1; the >1 threshold-account breaking point is not tested — §0). *(Maps to: Refuted.)*
4. **Specificity PIVOT.** At any α with T(α) movement ≥ 6: (a) B_wrong(α) movement ≥ 6 → **PIVOT** (strength artifact — the effect is nonspecific perturbation, not task geometry; EXP095+ artifact designs); (b) T(α)-vs-B(α) McNemar p ≥ 0.05 → **PIVOT** (movement without directional evidence — e.g. b≈c splits). *(Maps to: Not supported for the directional claim.)*
5. **Licensed positive.** ∃α ∈ {0.25, 0.5, 2.0, 4.0} with T(α)-vs-B(α) flips ≥ 6 AND McNemar p < 0.05 AND B_wrong(α) flat AND ΔM_T(α) > 0 in **all three** strata (strict — a zero or negative stratum fails consistency, carried from S4-9) → **CONTINUE (Supported), scoped:** the EXP094 kill narrows to its α=1 band; the positive is licensed only at the winning α on EXP092-B, with the full per-α stratum table published (§5 item 5). Multiple qualifying α → all reported; the scope is the qualifying set, never interpolated. *(Maps to: Supported.)*
6. **Otherwise → PIVOT** *(maps to: Not supported for the global claim)*, with named sub-cases: (a) sign-heterogeneous movement across α or items with null T-vs-B_wrong specificity — global dose claim dead, conditional design EXP095 material; (b) **consistent wrong-direction steering** (ΔM_T(α) < −0.10 with p < 0.05 and B_wrong(α) flat) — a causal channel exists, the constructor is mis-signed; sign story is EXP095 material, never KILL.

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted); the parenthetical mappings bind each step to its verdict. No banned language. No EXP094 claim is altered: the α=1.0 kill stands in all steps. **Scope fence:** gated/dynamic mechanisms and multi-layer compositions remain separate EXP095+ material regardless of outcome; the threshold-account breaking point (‖δ‖/‖r‖>1) remains untested regardless of outcome.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post == LOG-331 pin `ec276abe…`; any mismatch voids the run (Law #13).
- **Frozen constructor:** re-hash `experiments/runs/EXP094_peritem_l11/constructor.py` before any run; mismatch vs `5e03f206…917f361` → HOLD. G7 attestation carries from EXP094's `constructor_manifest_run.json` (code-identical).
- **G5-style exact-delivery probe:** per-(α,i) perturbation_ratio target α·0.0474, band ±25% (§2.2); aggregation rule ≥58/60 per α (§3 step 1). Margin shift vs B(α) recorded per item (reached-the-logits check, carried from EXP094).
- **Per-item records (Law #13):** every (item, α, arm) persists: top-1 decision, margin (EXP093's logit-margin m(h)=logit(target)−logit(foil), cited by reference — §5 item 1), perturbation_ratio, margin shift vs B(α). **Non-negotiable.**
- **Arm-routing rule:** binding full pairing (§3); no post-hoc re-routing.
- **Tie gate:** per α, ties/180 > 5% → that α RUN-INVALID.
- **Thread pinning:** torch intra-op thread count pinned to the EXP092/EXP094 extraction value and asserted before condition B, per EXP093 G4 (thread-count differences can flip near-zero margins; S2's mean margin was −0.0018).

### 4.1 Degeneracy analysis of every diagnostic (LOG-4338 lesson — constant-data unit tests, pre-registered)

Each diagnostic states what it returns on degenerate input. A diagnostic that can manufacture a positive from degenerate input is disqualified; all below fail safe:

1. **McNemar exact (doubling).** Constant input (b = c = 0 — the EXP094 datum): p = 1.0000 exactly, never significant → fails safe toward KILL, **cannot** manufacture CONTINUE. Adversarial input (b=60, c=0): p ≈ 8.7e-19. Unit test (executor runs pre-registration): all-identical decision vectors → p = 1.0 asserted.
2. **ΔM paired difference.** Zero-variance input → ΔM = 0 exactly, Tango CI = [0, 0] → cannot clear DELTA_BAR = 0.10 → fails safe.
3. **Flip-rate(α).** No flips → 0. Safe.
4. **Degeneracy gate (mean pairwise |cosine| over {d_i}).** 60 identical vectors → 1.0 ≥ 0.95 → Underdetermined (correct: the powerless test is caught, never KILLed). **Zero-vector edge:** if any ‖d_i‖ = 0, cosine is 0/0 undefined — pre-registered handling: a zero-norm item sits at perturbation_ratio = 0, outside every §2.2 band → delivery FAIL → HOLD (§3 step 1) **before** the gate is ever computed. The gate is never asked to divide by zero. Unit test: 60 copies of one vector → gate returns 1.0 → fires.
5. **B_wrong flatness — the dangerous direction.** A dead instrument returns B_wrong flat (p = 1.0) — and flatness is the CONTINUE-*enabling* conjunct. The two-part bar neutralizes this: a dead instrument simultaneously returns T(α) p = 1.0, failing the T-significance conjunct. **CONTINUE requires the conjunction** (T significant AND B_wrong flat); neither conjunct alone licenses anything. A diagnostic that rewarded flatness alone would be disqualified — this design does not.
6. **The "curve" itself.** No curve-shape statistic is pre-registered; the dose-response is five independent per-α tests. There is no fitted function to degenerate. Grid-resolution limit (Gap 1): a magic peak narrower than the grid spacing (e.g. centered at α = 0.7) is invisible to this design — the step-3 KILL is therefore scoped to "no magic strength **on the licensed grid**," never "no magic strength at any strength." Stated here so the verdict language cannot drift.

### 4.2 Probe-feasibility algebra (EXP079 lesson — proved, not asserted)

- **McNemar minimum:** exact doubling convention — b=6, c=0 → p = 2·(1/2)⁶ = 0.03125 < 0.05 ✓; b=5, c=0 → p = 0.0625, n.s. The ≥6-flip bar is exactly the minimum significant discordant table — feasible (needs 6 of 60 items; maximum achievable = 60).
- **No structural cap (the EXP079 contrast):** unlike EXP079's split-limited probe (max N_final = 46 < 50 — infeasible by construction), every item's decision can flip under some α in principle; max flips per α = 60 ≥ 6; max ΔM = 1.0 ≥ DELTA_BAR = 0.10. **No HALT_PROBE-style infeasibility exists in this design.**
- **B_wrong flat bar** (<6 flips, |ΔM| < 0.10): the complement region — feasible by the same arithmetic.
- **Replication gate** (B(1.0) = 36/60 exactly): feasible — deterministic CPU forward passes, byte-identical prompts, thread pinning; EXP094 demonstrated exact reproduction of S2's 36/60.
- **License-regime check:** max ‖δ‖/‖r‖ = 0.1896 < 1 → the design stays inside the linear-perturbation license; no extrapolation beyond the licensed regime is attempted.
- **Conclusion:** every pre-registered bar is reachable by construction. If Law #14's independent recomputation of this algebra disagrees, the run does not proceed.

### 4.3 Verdict discipline

The §3 evaluation order, five permitted verdicts with step→verdict mappings, no post-hoc table edits; a design change is a new experiment number, never a silent edit. **$0 compute for this draft:** on-paper only. No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, stratum, α ∈ {0.25,0.5,1.0,2.0,4.0}, arm ∈ {B,T,B_wrong}, top-1 decision, margin, perturbation_ratio, margin shift vs B(α)). Margin convention: EXP093's logit-margin m(h) = logit(target) − logit(foil), cited by reference (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md` §License, "the correct-margin") — not redefined at execution time.
2. Constructor manifest: re-verified constructor SHA-256 (must equal `5e03f206…917f361`), P₀ hash, R-arm seed, G7 carry-over attestation reference, per-item d_i/g_i norms, pairwise |cosine| summary (degeneracy gate inputs + §3-step-2 sanity value).
3. Δθ = 0 hash pre/post; environment + seed + thread-count manifest (Law #13 reproducibility).
4. Delivery probe log: per-(α,i) perturbation_ratio vs the §2.2 bands; per-α PASS/FAIL aggregation decisions (≥58/60 rule).
5. Stratum table: 3 strata × 5 α × 3 contrasts (T-vs-B, B_wrong-vs-B, T-vs-B_wrong): ΔM, McNemar b/c/p, Tango 95% CI — 135 cells, machine-written.
6. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition (including the step-0 replication values).

---

## 6. Known design risks — what Law #14 should try to break (falsification-first)

Ranked by how badly each would wound the licensed verdicts:

1. **Multiplicity across five α.** Five independent tests at ALPHA=0.05 → family-wise false-positive ≈ 0.226 under the global null. The licensed CONTINUE bar has no multiplicity correction; the conjunction (≥6 flips + p<0.05 + B_wrong flat + stratum-consistent) is mitigation, not correction. **Attack:** demand Bonferroni (p < 0.01) or an adjacent-α replication requirement for CONTINUE, or accept the disclosed 22.6% with the caveat attached. Either ruling must be pre-registered before the run — not debated after.
2. **Grid resolution vs the KILL's scope.** A narrow magic peak between grid points (α≈0.7, or α>4) is invisible; §3 step 3 as drafted scopes the KILL to the licensed grid, but the *headline* risk is scope creep in later retelling ("strength-invariant" unqualified). **Attack:** tighten the step-3 verdict language further, or extend the grid (α=8.0? — exits the linear license at ratio 0.38, still <1; worth pricing).
3. **B_wrong's discriminant strength.** Isotropic random at matched norm controls "any large nudge," but its OOD profile at α=4.0 may differ from d_i's (structured vs unstructured large perturbations could fail asymmetrically). The strictly stronger control — shuffled-item direction d_{π(i)} ("any task-derived direction" vs "this item's direction") — is not in the licensed 3-arm design. **Attack:** argue for replacing or augmenting B_wrong with d_{π(i)}, or accept random as the pre-registered control with the asymmetry disclosed.
4. **Replication-gate brittleness.** B(1.0) = 36/60 *exactly* on a fresh CPU rerun: EXP094 demonstrated it, but thread-count pinning is asserted, not proven, across environments. **Attack:** replace exact-match with a tolerance band (e.g. 35–37/60), or keep exact with the HOLD routing (current draft) — but then a HOLD must trigger a real diagnosis lane, not a silent re-run.
5. **Linearity to ratio 0.19 assumed, not probed.** The license predicts |Δm| linear in α; the design never checks it. If the response is strongly nonlinear, the "curve" reading needs care. **Attack:** add a pre-registered linearity diagnostic (per-item margin-shift vs α slope sign-consistency) as a non-binding instrument check — it cannot change the verdict but would qualify the interpretation.
6. **The untested >1 breaking point.** The draft is explicit (§0, §3 scope fence) that ratio >1 is untested, but a future reader may still cite S5-1's KILL against the threshold account. **Attack:** nothing to fix in the design — but Law #14 should confirm the scope fence is airtight in the verdict language.

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not alter EXP094's closed run record or any signed artifact; does not touch weights.
- Does not invent numbers — every value cites LOG-4391, LOG-4375/4376/4377, the EXP094 verdict review, or EXP093's signed pre-reg, except the B_wrong construction (§2.1.1) and the replication-gate/step-0 design (§3 step 0), which are new frozen design choices by this lane, flagged for Law #14 in §6 items 3–4.
- Does not license interpolation between α points, the >1 breaking point, gated/dynamic mechanisms, or multi-layer compositions.

---

## 8. Next steps

Independent **Law #14 review** of this draft (separate lane, to be dispatched — pre-assigned LOG number by the dispatcher) → SIGN or SIGN-WITH-FIXES → repair lane if needed → independent delta re-verification → **CEO execution clearance** → run (CPU, ≤1050 passes expected, 1300 hard cap). **Pilot NOT authorized until all complete. No GPU contact under any circumstance.**

---

*Draft prepared 2026-09-28 by the S5-1 pre-registration lead lane (LOG-4394), licensed by LOG-4391 PROPOSAL. DRAFT, UNSIGNED — a Law #14 review has been requested but not performed; no finding is closed. On paper only, $0 compute, CPU-only design. No signed protocol file was edited; this is a new unsigned file.*
