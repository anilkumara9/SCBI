# S5-1 — α-Sweep Dose-Response on the Killed Per-Item L11 Direction — Pre-registration DRAFT v2 (UNSIGNED)

*Status: DRAFT v2 — UNSIGNED. NOT a protocol. NOT executable. NOT reviewed (delta re-verification pending). No experiment number minted (S5-1 is EXP094+ material; numbering happens after Law #14 SIGN + CEO license).*
*Licensing chain: LOG-4373–4377 (EXP094 executed; Refuted/KILL, pure inertness; Law #14 SIGN) → LOG-4390 (founder gap review ranks the α-sweep the single highest-value missing experiment) → LOG-4391 (Monday idea session: S5-1 born as PROPOSAL; Law-#15 packet on record — linear-perturbation license, threshold-account breaking point ‖δ‖/‖r‖>1) → LOG-4394 (v1 draft) → LOG-4395 (Law #14 ACCEPT-WITH-FIXES, binding fix list F1–F13) → this v2 (repair lane).*
*All values below are from LOG-4391, LOG-4375/4376/4377, LOG-4395, the EXP094 verdict review (`experiments/protocols/REVIEWS/EXP094_VERDICT_REVIEW_2026-09-27.md`), and EXP093's signed pre-reg (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`) unless otherwise cited. No number is invented. Every changed statistic in this version was recomputed from primaries by the repair lane (see errata).*
***No pilot is authorized by this draft.** Before any run: independent Law #14 delta re-verification of F1, F2, F4, F6 + SIGN (separate lane), then CEO execution clearance. CPU-only design ($0); no GPU contact under any circumstance.*

---

## ERRATA — v1 → v2 (2026-09-28, binding; Law #14 fix list F1–F13, LOG-4395)

*Append-only repair record. v1 (`S5-1_PREREG_DRAFT_2026-09-28.md`) is preserved unedited; every change below is listed with its exact location. Fixes F1, F2, F4, F6 require independent delta re-verification before SIGN.*

- **F1 — Discovery bar → Bonferroni p < 0.01.** The T(α)-vs-B(α) discovery McNemar is now p < 0.01 (Bonferroni over the 5 grid α); minimum significant table b=8, c=0 (p = 2·2⁻⁸ = 0.0078125 < 0.01, independently recomputed; b=7, c=0 → 0.015625, n.s.). Changed in: §0 bars and decision paragraph; §2.4 (ALPHA split into ALPHA_disc = 0.01 / ALPHA_guard = 0.05); §3 steps 4b (p ≥ 0.01), 5 (p < 0.01), 6 (new sub-case 6c: p ∈ [0.01,0.05) → PIVOT, never CONTINUE-with-caveat); §4.2 algebra; §6 item 1 (ruling recorded). The ≥6-flip gate is retained — dominated by p<0.01 for discovery, still gates B_wrong-flatness and step 4a. Discriminant/guard contrasts (B_wrong-vs-B, T-vs-B_wrong) stay at 0.05: guards, not discovery claims. Family-wise false-positive under the global null is now ≈ 1−0.99⁵ ≈ 0.049 (recomputed), with the conjunction as additional mitigation.
- **F2 — B-arm determinism resolved: single B run (option (a), recommended).** Justification: under the draft's own determinism premise (§3 step 0: deterministic CPU + byte-identical prompts + thread pinning *must reproduce*), five B runs are byte-identical — 240 passes of pure redundancy, not five independent replications. The single B run doubles as the determinism self-check via the strengthened step-0 gate (F6). Changed in: §2.3 (660 injection + 150 reserve = 810 expected; 1300 hard cap unchanged); §3 step 0; §5 items 1, 5 (B recorded once per item; pairing is B(i) vs T(α,i) vs B_wrong(α,i)); §0 cheapest-test arithmetic.
- **F3 — Manifest filename.** `constructor_manifest_run.json` → `constructor_manifest.json` (2 occurrences: §2 frozen-spec paragraph, §4 guards). Pre-run checklist names the real file. Law #14 verified the G7 fields (`g72_attestation`, `g7_verdict`) exist in the real file.
- **F4 — Step-3 KILL names its object.** "Refuted (KILL family)" → "Refuted: the magic-strength rescue of the per-item static family is refuted *on the licensed five-point grid*" — never bare "KILL family" (no double-counting EXP094's already-killed family, no scope creep in retelling). Sub-grid-peak fence carried inline. New B_wrong-moved sub-case: B_wrong(α) ≥ 6 flips at any α while all T(α) < 6 → the KILL stands, but the report must state that nonspecific fragility was observed.
- **F5 — Step-4a α-index.** B_wrong movement is evaluated at the *same* α as the T(α) movement (co-movement is the strength-artifact evidence).
- **F6 — Step-0 gate rebuilt.** (i) Per-item B-decision agreement with EXP094's archived B vector when archived (pre-run checklist: locate it; absent → 36/60 aggregate gate with disclosed compensating-flip weakness). (ii) Worksheet records the exact T(1.0)-vs-B flip count; any nonzero count < 6 → foundation-wobble flag (sweep proceeds per the <6 standard; wobble disclosed). (iii) A step-0 HOLD triggers a pre-registered diagnosis lane (re-hash weights vs LOG-331 pin, verify thread pinning, byte-compare prompts) — never a silent re-run. Changed in §3 step 0 and §5 item 6.
- **F7 — Delivery-failure routing.** Zero-norm d_i or any common-cause-across-α delivery failure → HOLD + diagnose; isolated per-α delivery failures → exclude that α only. Changed in §3 step 1; §4.1 item 4 aligned (already HOLD).
- **F8 — Orders of magnitude.** §0 "two orders of magnitude" → "16× (1.2 orders of magnitude)" (log₁₀(16) = 1.204, recomputed).
- **F9 — §6 item 2 corrected.** α=8.0 → ratio 0.3792 < 1 stays *inside* the ≲1 linear license; the "exits the linear license" phrase is struck.
- **F10 — B_wrong norm precision.** "Exactly T(α)'s per-item norm" → "targets T(α)'s per-item norm (exact iff regenerated ‖d_i‖₂ matches EXP094's 0.0474·‖h_i^B‖₂); the §3-step-1 delivery probe is the enforcer." Changed in §2.1 arms table and §2.1.1.
- **F11 — Doubling arithmetic.** §4.1: b=60, c=0 → p ≈ 1.73×10⁻¹⁸ under doubling (2·2⁻⁶⁰ = 1.7347×10⁻¹⁸, recomputed).
- **F12 — CONTINUE interpretive fence; 4th arm declined.** Step-5/§0/§1 CONTINUE language now licenses only "a task-direction-shaped causal signal at the winning α on EXP092-B" — NOT per-item specificity (this-item's-d_i vs any-task-derived-direction requires the d_{π(i)} control, EXP095+ material). The optional d_{π(i)} 4th arm is **declined in this version**: the isotropic random arm is the correct control for the live strength-artifact alternative, and a 4th arm would add a new decision row requiring full delta re-verification — it stays EXP095+ material. Flagged in §2.1.1 and §6 item 3.
- **F13 — T-vs-B_wrong labeled diagnostic-only.** §2.4 states explicitly: the T(α)-vs-B_wrong(α) contrast is computed for the 135-cell table but has no decision role in §3; no post-hoc role may be invented (Law #9).

---

## 0. Law #15 block (binding, carried from LOG-4391; bars per F1)

**Precise question [HYPOTHESIS].** EXP094 (binding Refuted/KILL, LOG-4375/4376/4377) showed that static injection of the **per-item** layer-11 task direction at α=1.0 (perturbation_ratio = 0.0474) on EXP092-B moves zero decisions: B = T = R = 36/60, ΔM_T = +0.0000, McNemar b = c = 0 → p = 1.0000 on all nine contrasts, zero flips across 120 injection item-arms despite nonzero margin shifts on every item and genuinely established G5 delivery (rel_err 4.26e-07) — pure inertness. The licensed claim is scoped: it falsifies causal influence of the per-item static direction **at α = 1.0** only. **Is that kill a point or a curve?** Map ΔM(α) and flip-rate(α) over α ∈ {0.25, 0.5, 1.0, 2.0, 4.0} — a 16× strength range — on the same EXP092-B 60 items, with a norm-matched discriminant arm at every α. [HYPOTHESIS]

**Decision it changes.** **KILL** the "magic strength" hope if all-α ΔM = 0 and flips = 0 — the inertness is not a strength artifact; the family license becomes strength-invariant over the licensed grid (boundary-law graduation, scoped — §3 step 3). **CONTINUE** (licensed positive only) if ∃α ∈ {0.25, 0.5, 2.0, 4.0} with T-vs-B flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 (Bonferroni over 5 α — F1) AND B_wrong(α) flat AND stratum-consistent — the EXP094 kill narrows to its α=1 band and a task-direction-shaped causal signal at the winning α on EXP092-B is earned (F12 fence: NOT per-item specificity). **PIVOT** if movement appears but the discriminant arm moves with it (strength artifact, not geometry), if movement lacks directional significance at the discovery bar, or if a near-miss (flips ≥ 6, p ∈ [0.01, 0.05)) fails the Bonferroni bar (→ step 6c, never CONTINUE-with-caveat) — the rescue is nonspecific or unlicensed; conditional/artifact designs become EXP095+ material. All outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** No single-α pilot falsifies the ∃α claim: a peaked dose-response (works at α=0.5, dead at α=4.0) survives any one-point null, and a high-α-only effect survives any low-α null. The 5-point sweep — 660 injection passes (60 B + 300 T + 300 B_wrong), CPU, $0 (F2) — **is** the cheapest test of the dose-response shape. The cheapest internal falsifier of the foundation is the replication gate (§3 step 0): if EXP094's exact condition does not reproduce, nothing downstream is licensable.

**Quantitative prediction (pre-registered, bars).** Per-α, on T-vs-B paired decisions: flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 (discovery contrast — F1) AND B_wrong(α) flat (flips < 6 AND |ΔM| < 0.10, guard bars) AND ΔM_T(α) > 0 in all three strata (aggregate / A-first / C-first, strict). The B_wrong-flatness conjunct is non-negotiable: a strength-mediated nonspecific effect predicts T(α) and B_wrong(α) moving together; only task-geometry steering predicts T(α) moving while B_wrong(α) stays flat.

**Breaking point (sharp, two levels).** (i) In-band: all-α T-vs-B movement < 6 → the magic-strength hope is dead on the licensed grid; KILL. (ii) License boundary: the linear-perturbation license is licensed only while ‖δ‖/‖r‖ ≲ 1 (threshold account, LOG-4391). This design's maximum is α=4.0 → ratio 0.1896 < 1 — the design stays inside its license, and the >1 breaking point ("push too weak" exhausted) is **untested by this design**. A flat zero through α=4.0 must never be phrased as killing the threshold account itself — only the in-band magic-strength hope. [INTERPRETATION of scope]

**The belief it tests (named, LOG-4391):** "the EXP094 kill is about geometry" — overturned-by "it was about strength" (a positive band at some α) or deepened-by "inert as a function of strength" (flat zero over 16×, 1.2 orders of magnitude — F8 — a paper-worthy law). [INTERPRETATION]

---

## 1. Background and license

- **EXP094 binding facts [OBSERVATION, LOG-4375/4376/4377; verdict review §2]:** per-item L11 task-direction injection at α=1.0 on EXP092-B: B=T=R=36/60; ΔM_T=+0.0000, ΔM_R=+0.0000; McNemar b=c=0 → p=1.0000 all nine contrasts; movement 0 < 6; 0 ties/180; G5 band [0.0355, 0.0593] with 0/120 violations; execution rel_err 4.26e-07; Δθ=0 hash pin `ec276abe…` (LOG-331); degeneracy statistic mean pairwise |cosine| = 0.7923 < 0.95. Licensed claim: per-item static L11 directions do not move decisions **at α=1.0**; gated/dynamic and multi-layer compositions untouched.
- **Death-debt [FACT, LOG-4391]:** S5-1 pays EXP094's LOG-219 death-debt jointly with S5-4; deaths table records debt PAID on proposal (execution outstanding). This draft is the "pre-registered plan" the backlog row requires — **not a revival or an edit of EXP094's design** (EXP094 has no signed protocol file to edit; its run is a closed record). This document is a new unsigned file (v2 of the draft; v1 preserved).
- **Mathematical license [THEOREM-adjacent linear-algebra fact, EXP093 signed pre-reg §License, cited by reference]:** let m(h) = logit(target) − logit(foil) be the correct-margin [DEFINITION, EXP093 §License]. The intervention sets h′ = h + α·d_i at L11; to first order, Δm_i ≈ α·⟨∇ₕm_i, d_i⟩. **License verdict: HOLDS for a test, not a conclusion** — the license licenses the sweep, not a positive. Under the magic-strength hope, ⟨∇m_i, d_i⟩ ≠ 0 for a substantial item subset, so |Δm_i| grows linearly in α and items with baseline |m_i| < α·|⟨∇m_i,d_i⟩| flip: flip-rate(α) is then non-decreasing in α (within the linear regime) and some grid α clears the §0 bars. EXP094's datum — nonzero margin shifts on every item at α=1 yet zero flips — is compatible with |⟨∇m,d⟩| small-but-nonzero (predicts flips emerging by α=4, i.e. 4× the shift) **or** with pure jitter (predicts no α helps: the KILL branch). The sweep separates exactly these two readings. Honest audits carried: (Gap 1) α-grid resolution — a "magic" peak narrower than the grid spacing is invisible; the KILL is scoped to the licensed grid, never to "all strengths" (see §4); (Gap 2) one bench — any CONTINUE is bench-scoped to EXP092-B; (Gap 3) multiplicity — five α at ALPHA_disc=0.01 each carry family-wise false-positive ≈ 1−0.99⁵ ≈ 0.049 (F1, recomputed); the ≥6-flip + B_wrong-flat + stratum-consistency conjunction is the pre-registered additional mitigation, NOT a substitute correction — disclosed, not hidden (§4, §6 item 1).
- **Summit filter:** a licensed positive would be the program's first task-direction-shaped causal signal at a non-readout layer — the dose-response primitive the summit (autonomous self-steering) must build on (F12 fence: scoped to the winning α on EXP092-B; not a per-item-specificity claim, not an autonomy result). Caveat preserved: injection is externally applied, not self-computed — never described as an autonomy result.

---

## 2. Design (frozen model, Δθ = 0; frozen EXP094 bundle path)

### 2.1 Arms (pre-registered)

| Arm | Injection at L11 (readout-anchor position, per item i) | Role |
|---|---|---|
| B | none (Δθ = 0) — single run per item (F2) | baseline — anchors EXP092-B; replication anchor |
| T(α) | per-item task direction d_i scaled to norm α·0.0474·‖h_i^B‖₂ | test arm — the dose |
| B_wrong(α) | per-item **random** direction g_i (EXP094's frozen R-arm constructor, pinned seed → identical {g_i}) scaled to norm α·‖d_i‖₂ (targets — F10 — T(α)'s per-item norm) | discriminant — the arm that must stay flat |

**{d_i} regeneration (frozen specification).** The {d_i} vectors were not persisted by EXP094 (verdict review O1 — only norms). The executor regenerates them from the frozen EXP094 constructor `experiments/runs/EXP094_peritem_l11/constructor.py`, hash-pinned `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361` [FACT, constructor manifest]. Pre-run: re-hash the constructor; mismatch vs the pin → HOLD (do not proceed). The G7 label-free attestation (label-swap max abs diff 0.0, cross-item isolation) carries from EXP094's `constructor_manifest.json` (F3 — filename corrected; Law #14 verified the `g72_attestation` and `g7_verdict` fields exist in the real file) — same frozen code + same P₀ (`e7e81496…f2601e11`) + same bench, so the attestation is code-identical, not re-audited per α. The {g_i} are regenerated from the same frozen R-arm constructor with the pinned seed (§5 item 2 of EXP094's manifest).

#### 2.1.1 B_wrong(α) — exact specification (what it rules out)

- **Construction [DEFINITION]:** for item i and strength α, g_i drawn from the isotropic Gaussian in the 1024-dimensional L11 residual space (Pythia-410m hidden_size = 1024; the "512" in EXP094's draft docstring was a ruled-zero-content erratum — verdict review §7), normalized to unit norm, then scaled: B_wrong(α,i) = α·‖d_i‖₂·(g_i/‖g_i‖₂). Task-free by construction (seed-pinned, label-free inputs only). The norm **targets** T(α)'s per-item norm (F10 — exact iff regenerated ‖d_i‖₂ matches EXP094's 0.0474·‖h_i^B‖₂; the §3-step-1 delivery probe is the enforcer).
- **"Flat" (pre-registered):** B_wrong(α) is flat iff flips(B_wrong(α) vs B) < 6 AND |ΔM_Bwrong(α)| < 0.10, where ΔM uses EXP093's paired convention ΔM = (1/n)Σ[correct_X(i) − correct_B(i)].
- **What it rules out:** the live alternative at high α is the **perturbation-strength artifact** — EXP093's signed pre-reg states it explicitly: "Any intervention perturbs the residual stream; a perturbation alone can flip near-zero-margin decisions (S2's mean margin was −0.0018 — decisions are fragile)." At α=4.0 the injected norm is 0.1896 of the residual norm; a nonspecific large-nudge effect (fragile margins, OOD activations) predicts B_wrong(α) flipping alongside T(α). The B_wrong arm targets T(α)'s per-item norms at every α — the **only** difference between the arms is direction content (task-derived vs isotropic random). If T(α) moves while B_wrong(α) stays flat, the strength artifact is priced out; if both move, the effect is nonspecific → PIVOT (§3 step 4a), never CONTINUE.
- **Why not −d_i:** the wrong-sign arm tests sign-symmetry, a question EXP093's ±v design already probed; the dangerous confound for a *strength* sweep is strength-mediated nonspecific flips, which the norm-matched random arm controls directly. (A shuffled-item variant d_{π(i)} — "any task-derived direction" vs "this item's direction" — would be strictly stronger for per-item-specificity claims; **declined in this version** (F12) — adding it would create a new decision row requiring full delta re-verification; it stays EXP095+ material. The 3-arm design stands with the §3-step-5 interpretive fence.)

### 2.2 Strength grid (pre-registered)

α ∈ {0.25, 0.5, 1.0, 2.0, 4.0}; per-item perturbation_ratio targets α·0.0474 = {0.01185, 0.0237, 0.0474, 0.0948, 0.1896}. G5-style per-α bands (±25%): [0.00889, 0.01481], [0.01778, 0.02963], [0.0355, 0.0593], [0.0711, 0.1185], [0.1422, 0.2370]. **No interpolation between grid points is licensed** — each α is an independent pre-registered test; the "curve" is five measured points, not a fitted function.

### 2.3 Budget (pre-registered — F2)

- **660 injection passes** (60 B single-run + 5 α × 60 T + 5 α × 60 B_wrong); **+150 reserved** for delivery/margin-verification repeats → **810 expected; hard cap 1300.** Spend beyond 810 requires a logged, pre-cleared exception; the 1300 hard cap is not waivable within this pre-registration (a change is a new design, not an edit). CPU only, $0. (Single B run per item — F2: under the §3-step-0 determinism premise, five B runs would be byte-identical, so 240 passes of redundancy are removed; the pairing structure is B(i) vs T(α,i) vs B_wrong(α,i).)

### 2.4 Statistics (pre-registered)

- **McNemar exact, doubling convention** (EXP094's convention, verdict review §1) on paired decisions, per α: T(α)-vs-B, B_wrong(α)-vs-B, T(α)-vs-B_wrong(α).
- **ΔM** per EXP093's paired convention; **Tango 95% CIs** on the paired differences.
- **DELTA_BAR = 0.10** (all contrasts); **ALPHA_disc = 0.01** for the T(α)-vs-B(α) discovery contrast (Bonferroni over 5 α — F1); **ALPHA_guard = 0.05** for the discriminant/guard contrasts (B_wrong-vs-B, T-vs-B_wrong) — guards, not discovery claims. **Movement gate: ≥ 6 flips** (retained — dominated by p<0.01 for discovery, still gates B_wrong-flatness and step 4a).
- **T(α)-vs-B_wrong(α) is diagnostic-only (F13):** computed for the 135-cell table but has no decision role in §3. No post-hoc role may be invented (Law #9).
- **Correctness:** margin > 0 (strict), EXP094's convention. **Tie gate:** ties/180 > 5% at any α → that α RUN-INVALID (excluded, no verdict licensed there). (Per α: 60 B + 60 T(α) + 60 B_wrong(α) = 180 rows; the single B vector is reused across α.)
- **Multiplicity disclosure (F1 ruling recorded):** five α each at ALPHA_disc=0.01 → family-wise ≈ 1−0.99⁵ ≈ 0.049 under the global null (recomputed). The CONTINUE bar's conjunction (flips ≥ 6 AND p < 0.01 AND B_wrong flat AND stratum-consistent) is the pre-registered additional mitigation. A near-miss with p ∈ [0.01, 0.05) is **not** a CONTINUE-with-caveat — it falls to step 6c PIVOT. Adjacent-α replication is accepted only if pre-registered as a substitute design (it is not, in this version).

---

## 3. Decision table (pre-registered)

**Arm-routing rule (binding):** every one of the 60 EXP092-B items receives the B arm once and all of T(α), B_wrong(α) at all five α (full within-(item,α) pairing against the single B vector); all contrasts are paired; no item excluded from any contrast; stratum membership (aggregate / A-first / C-first, 30/30) is the bench pin, fixed before inspection. No post-hoc re-routing — structurally impossible under full pairing.

**Binding evaluation order (first match wins).** Exactly one step is earned:

0. **Replication anchor (the EXP094 point — F6).** Pre-run checklist: locate EXP094's archived per-item B decisions. (i) If archived: per-item B-decision agreement is required — any disagreement → **HOLD**. (ii) Aggregate fallback (archived vector absent): B ≠ 36/60 correct → **HOLD** (disclosed weakness: compensating per-item flips could pass the aggregate gate). T(1.0)-vs-B movement ≥ 6 → **HOLD** (EXP094 non-replication — the kill's foundation is unstable; no sweep verdict licensable). The worksheet records the exact T(1.0)-vs-B flip count; any nonzero count < 6 → **foundation-wobble flag** (the sweep proceeds per the <6 standard; the wobble is disclosed in the report). A step-0 HOLD triggers the pre-registered diagnosis lane — re-hash weights vs the LOG-331 pin, verify thread pinning, byte-compare prompts against EXP094's — **never a silent re-run**. *Neither outcome is a verdict on the sweep; both are foundation guards.* (A positive can therefore only be earned at α ∈ {0.25, 0.5, 2.0, 4.0}.)
1. **Delivery (F7).** Per-α G5 aggregation rule: probe PASS(α) iff ≥ 58/60 items sit within the §2.2 band for that α with margin shift recorded vs B. Zero-norm d_i or any common-cause-across-α delivery failure → **HOLD + diagnose** (the whole run — the foundation is broken). Isolated per-α delivery failures → that α excluded (no verdict licensed there); remaining α proceed. *(Maps to: Inconclusive.)*
2. **Degeneracy.** Mean pairwise |cosine| over regenerated {d_i} ≥ 0.95 → **Underdetermined** — never KILL on a powerless test (R4 rule). Sanity companion (pre-registered): |recomputed value − 0.7923| > 0.05 → **HOLD** (constructor regeneration broken — the {d_i} are not EXP094's). *(Maps to: Underdetermined.)*
3. **All-α KILL (the in-band kill — F4).** T(α)-vs-B movement < 6 at **every** α ∈ {0.25, 0.5, 1.0, 2.0, 4.0} → **Refuted: the magic-strength rescue of the per-item static family is refuted *on the licensed five-point grid*** — inertness is not a strength artifact; the family license becomes strength-invariant over a 16× strength range — boundary-law graduation **scoped to the licensed grid** (a narrower magic peak between grid points is not ruled out — §4 Gap 1; the >1 threshold-account breaking point is not tested — §0). B_wrong-moved sub-case: B_wrong(α) ≥ 6 flips at any α while all T(α) < 6 → the KILL stands, but the report must state that nonspecific fragility was observed (the bench moves under large nudges regardless of direction). *(Maps to: Refuted.)*
4. **Specificity PIVOT.** At any α with T(α) movement ≥ 6: (a) B_wrong evaluated at the **same α** (F5) moves ≥ 6 → **PIVOT** (strength artifact — the effect is nonspecific perturbation, not task geometry; EXP095+ artifact designs); (b) T(α)-vs-B McNemar p ≥ 0.01 (F1) → **PIVOT** (movement without directional evidence at the discovery bar — e.g. b≈c splits). *(Maps to: Not supported for the directional claim.)*
5. **Licensed positive (F1, F12).** ∃α ∈ {0.25, 0.5, 2.0, 4.0} with T(α)-vs-B flips ≥ 6 AND McNemar p < 0.01 AND B_wrong(α) flat AND ΔM_T(α) > 0 in **all three** strata (strict — a zero or negative stratum fails consistency, carried from S4-9) → **CONTINUE (Supported), fenced:** the EXP094 kill narrows to its α=1 band; what is licensed is **a task-direction-shaped causal signal at the winning α on EXP092-B** — NOT per-item specificity (this-item's-d_i vs any-task-derived-direction requires the d_{π(i)} control, EXP095+ material). The full per-α stratum table is published (§5 item 5). Multiple qualifying α → all reported; the scope is the qualifying set, never interpolated. *(Maps to: Supported.)*
6. **Otherwise → PIVOT** *(maps to: Not supported for the global claim)*, with named sub-cases: (a) sign-heterogeneous movement across α or items with null T-vs-B_wrong specificity — global dose claim dead, conditional design EXP095 material; (b) **consistent wrong-direction steering** (ΔM_T(α) < −0.10 with p < 0.01 (F1) and B_wrong(α) flat) — a causal channel exists, the constructor is mis-signed; sign story is EXP095 material, never KILL; (c) **near-miss discovery** (flips ≥ 6, p ∈ [0.01, 0.05), B_wrong flat, stratum-consistent) — the Bonferroni bar is not cleared; not a licensed positive; may motivate an EXP095+ design with pre-registered adjacent-α replication, never a CONTINUE-with-caveat.

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted); the parenthetical mappings bind each step to its verdict. No banned language. No EXP094 claim is altered: the α=1.0 kill stands in all steps. **Scope fence:** gated/dynamic mechanisms and multi-layer compositions remain separate EXP095+ material regardless of outcome; the threshold-account breaking point (‖δ‖/‖r‖>1) remains untested regardless of outcome.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post == LOG-331 pin `ec276abe…`; any mismatch voids the run (Law #13).
- **Frozen constructor:** re-hash `experiments/runs/EXP094_peritem_l11/constructor.py` before any run; mismatch vs `5e03f206…917f361` → HOLD. G7 attestation carries from EXP094's `constructor_manifest.json` (F3; Law #14 verified `g72_attestation` and `g7_verdict` present) — code-identical.
- **G5-style exact-delivery probe:** per-(α,i) perturbation_ratio target α·0.0474, band ±25% (§2.2); aggregation rule ≥58/60 per α (§3 step 1, F7 routing). Margin shift vs B recorded per item (reached-the-logits check, carried from EXP094).
- **Per-item records (Law #13):** every (item, α, arm) persists: top-1 decision, margin (EXP093's logit-margin m(h)=logit(target)−logit(foil), cited by reference — §5 item 1), perturbation_ratio, margin shift vs B. **Non-negotiable.**
- **Arm-routing rule:** binding full pairing (§3); no post-hoc re-routing.
- **Tie gate:** per α, ties/180 > 5% → that α RUN-INVALID (180 = 60 B + 60 T(α) + 60 B_wrong(α); single B vector reused).
- **Thread pinning:** torch intra-op thread count pinned to the EXP092/EXP094 extraction value and asserted before condition B, per EXP093 G4 (thread-count differences can flip near-zero margins; S2's mean margin was −0.0018).

### 4.1 Degeneracy analysis of every diagnostic (LOG-4338 lesson — constant-data unit tests, pre-registered)

Each diagnostic states what it returns on degenerate input. A diagnostic that can manufacture a positive from degenerate input is disqualified; all below fail safe:

1. **McNemar exact (doubling).** Constant input (b = c = 0 — the EXP094 datum): p = 1.0000 exactly, never significant → fails safe toward KILL, **cannot** manufacture CONTINUE. Adversarial input (b=60, c=0): p ≈ 1.73×10⁻¹⁸ under doubling (F11 — 2·2⁻⁶⁰ = 1.7347×10⁻¹⁸, recomputed). Discovery minimum (F1): b=8, c=0 → p = 0.0078125 < 0.01 ✓; b=7, c=0 → 0.015625, n.s. Unit test (executor runs pre-registration): all-identical decision vectors → p = 1.0 asserted.
2. **ΔM paired difference.** Zero-variance input → ΔM = 0 exactly, Tango CI = [0, 0] → cannot clear DELTA_BAR = 0.10 → fails safe.
3. **Flip-rate(α).** No flips → 0. Safe.
4. **Degeneracy gate (mean pairwise |cosine| over {d_i}).** 60 identical vectors → 1.0 ≥ 0.95 → Underdetermined (correct: the powerless test is caught, never KILLed). **Zero-vector edge:** if any ‖d_i‖ = 0, cosine is 0/0 undefined — pre-registered handling: a zero-norm item is a common-cause delivery failure → **HOLD + diagnose (§3 step 1, F7)** before the gate is ever computed. The gate is never asked to divide by zero. Unit test: 60 copies of one vector → gate returns 1.0 → fires.
5. **B_wrong flatness — the dangerous direction.** A dead instrument returns B_wrong flat (p = 1.0) — and flatness is the CONTINUE-*enabling* conjunct. The two-part bar neutralizes this: a dead instrument simultaneously returns T(α) p = 1.0, failing the T-significance conjunct. **CONTINUE requires the conjunction** (T significant at p<0.01 AND B_wrong flat); neither conjunct alone licenses anything. A diagnostic that rewarded flatness alone would be disqualified — this design does not.
6. **The "curve" itself.** No curve-shape statistic is pre-registered; the dose-response is five independent per-α tests. There is no fitted function to degenerate. Grid-resolution limit (Gap 1): a magic peak narrower than the grid spacing (e.g. centered at α = 0.7) is invisible to this design — the step-3 KILL is therefore scoped to "no magic strength **on the licensed grid**," never "no magic strength at any strength." Stated here so the verdict language cannot drift.

### 4.2 Probe-feasibility algebra (EXP079 lesson — proved, not asserted; F1-updated)

- **McNemar minimum (discovery contrast, Bonferroni):** exact doubling convention — b=8, c=0 → p = 2·2⁻⁸ = 0.0078125 < 0.01 ✓ (minimum significant table, recomputed); b=7, c=0 → p = 0.015625, n.s. Feasible (needs 8 of 60 items; maximum achievable = 60). Guard-contrast minimum (unchanged): b=6, c=0 → p = 0.03125 < 0.05 ✓; b=5, c=0 → 0.0625, n.s.
- **No structural cap (the EXP079 contrast):** unlike EXP079's split-limited probe (max N_final = 46 < 50 — infeasible by construction), every item's decision can flip under some α in principle; max flips per α = 60 ≥ 8; max ΔM = 1.0 ≥ DELTA_BAR = 0.10. **No HALT_PROBE-style infeasibility exists in this design.**
- **B_wrong flat bar** (<6 flips, |ΔM| < 0.10): the complement region — feasible by the same arithmetic.
- **Replication gate** (per-item B agreement when archived; 36/60 aggregate fallback): feasible — deterministic CPU forward passes, byte-identical prompts, thread pinning; EXP094 demonstrated exact reproduction of S2's 36/60.
- **License-regime check:** max ‖δ‖/‖r‖ = 0.1896 < 1 → the design stays inside the linear-perturbation license; no extrapolation beyond the licensed regime is attempted.
- **Conclusion:** every pre-registered bar is reachable by construction. If Law #14's independent delta re-computation of this algebra disagrees, the run does not proceed.

### 4.3 Verdict discipline

The §3 evaluation order, five permitted verdicts with step→verdict mappings, no post-hoc table edits; a design change is a new experiment number, never a silent edit. **$0 compute for this draft:** on-paper only. No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, stratum, α ∈ {0.25,0.5,1.0,2.0,4.0} for T/B_wrong; B recorded once per item, α-index n/a — F2, arm ∈ {B,T,B_wrong}, top-1 decision, margin, perturbation_ratio, margin shift vs B). Margin convention: EXP093's logit-margin m(h) = logit(target) − logit(foil), cited by reference (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md` §License, "the correct-margin") — not redefined at execution time.
2. Constructor manifest: re-verified constructor SHA-256 (must equal `5e03f206…917f361`), P₀ hash, R-arm seed, G7 carry-over attestation reference (`constructor_manifest.json` — F3), per-item d_i/g_i norms, pairwise |cosine| summary (degeneracy gate inputs + §3-step-2 sanity value).
3. Δθ = 0 hash pre/post; environment + seed + thread-count manifest (Law #13 reproducibility).
4. Delivery probe log: per-(α,i) perturbation_ratio vs the §2.2 bands; per-α PASS/FAIL aggregation decisions (≥58/60 rule, F7 routing); zero-norm / common-cause events logged with HOLD routing.
5. Stratum table: 3 strata × 5 α × 3 contrasts (T-vs-B, B_wrong-vs-B, T-vs-B_wrong [diagnostic-only — F13]): ΔM, McNemar b/c/p, Tango 95% CI — 135 cells, machine-written. (T(α) and B_wrong(α) pair per-item against the single B vector.)
6. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition — including the step-0 replication values (per-item agreement vector or aggregate count; exact T(1.0)-vs-B flip count; foundation-wobble flag if nonzero <6 — F6).

---

## 6. Known design risks — what Law #14 should try to break (falsification-first), with v2 dispositions

Ranked by how badly each would wound the licensed verdicts:

1. **Multiplicity across five α.** *v2 disposition (F1):* **ADOPTED as a binding fix** — the discovery contrast is Bonferroni-corrected (ALPHA_disc = 0.01; family-wise ≈ 0.049, recomputed); the conjunction (≥6 flips + p<0.01 + B_wrong flat + stratum-consistent) is retained as additional mitigation; near-misses (p ∈ [0.01,0.05)) fall to step-6c PIVOT, never CONTINUE-with-caveat. Remaining for delta re-verification: the F1 algebra and the step-4b/5/6c threshold updates.
2. **Grid resolution vs the KILL's scope.** A narrow magic peak between grid points (α≈0.7, or α>4) is invisible; the step-3 KILL is scoped to the licensed grid (F4 names the killed object: the magic-strength rescue *on the licensed five-point grid*). *v2 disposition (F9):* the item-2 parenthetical is corrected — α=8.0 → ratio 0.3792 stays *inside* the ≲1 linear license, so a grid extension to α=8.0 would not exit the license; it is nevertheless NOT covered by this pre-registration's in-band KILL and would need its own licensed extension. The headline risk (unqualified "strength-invariant" in retelling) is fenced by F4's verdict language.
3. **B_wrong's discriminant strength.** Isotropic random at matched norm controls "any large nudge," but its OOD profile at α=4.0 may differ from d_i's (structured vs unstructured large perturbations could fail asymmetrically). *v2 disposition (F12):* 3-arm design stands with the §3-step-5 interpretive fence (no per-item-specificity claim); the d_{π(i)} 4th arm is declined in this version and stays EXP095+ material. **Attack (delta re-verification):** confirm the fence language cannot be read as licensing per-item specificity.
4. **Replication-gate brittleness.** *v2 disposition (F6):* **ADOPTED** — per-item B-decision agreement when archived (aggregate 36/60 fallback with disclosed compensating-flip weakness); exact T(1.0)-vs-B flip count on the worksheet with foundation-wobble flag; HOLD triggers a pre-registered diagnosis lane, never a silent re-run. Remaining for delta re-verification: the new step-0 text and the §5-item-6 worksheet spec.
5. **Linearity to ratio 0.19 assumed, not probed.** The license predicts |Δm| linear in α; the design never checks it. If the response is strongly nonlinear, the "curve" reading needs care. **Attack:** add a pre-registered linearity diagnostic (per-item margin-shift vs α slope sign-consistency) as a non-binding instrument check — it cannot change the verdict but would qualify the interpretation. *(Unchanged from v1; still open for Law #14.)*
6. **The untested >1 breaking point.** The draft is explicit (§0, §3 scope fence) that ratio >1 is untested; a future reader may still cite S5-1's KILL against the threshold account. **Attack:** nothing to fix in the design — Law #14 should confirm the scope fence is airtight in the verdict language. *(Unchanged from v1; held.)*

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not alter EXP094's closed run record, v1 of this draft, or any signed artifact; does not touch weights.
- Does not invent numbers — every value cites LOG-4391, LOG-4375/4376/4377, LOG-4395, the EXP094 verdict review, or EXP093's signed pre-reg, except the B_wrong construction (§2.1.1), the replication-gate/step-0 design (§3 step 0), and the v2 repair choices (F2 option (a), F12 4th-arm decline), which are frozen design choices by this lane, flagged for Law #14 delta re-verification.
- Does not license interpolation between α points, the >1 breaking point, α > 4.0, gated/dynamic mechanisms, or multi-layer compositions.

---

## 8. Next steps

Independent **Law #14 delta re-verification** of F1, F2, F4, F6 (dispatched separately — binding per LOG-4395) → SIGN or further fixes → **CEO execution clearance** → run (CPU, ≤810 passes expected, 1300 hard cap — F2). **Pilot NOT authorized until all complete. No GPU contact under any circumstance.**

---

*Draft v2 prepared 2026-09-28 by the S5-1 pre-registration repair lane (licensed by LOG-4395 ACCEPT-WITH-FIXES). DRAFT, UNSIGNED — delta re-verification requested but not performed; no finding is closed. On paper only, $0 compute, CPU-only design. v1 preserved unedited at `research/innovation/S5-1_PREREG_DRAFT_2026-09-28.md`; no signed protocol file was edited; this is a new unsigned file.*
