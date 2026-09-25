# EXP086 — R3 Dynamical-Amplifier / Singular-Vector-Aligned Injection: Pre-registration DRAFT

**Status:** DRAFT — unsigned, pre-Law-#14. **NOT licensed for execution.** No runner may be built from this draft until a fresh Law #14 re-review by a different reviewer returns SIGN or SIGN-WITH-FIXES with all fixes verified discharged.

**Parent review:** LOG-285 (Law #14 review of R3: SIGN-WITH-FIXES, 14 findings F1–F14). This draft discharges all 14 (discharge index §14).

**Number note:** dispatched as EXP085 in the review mandate; EXP085 was claimed by the I2 lane (LOG-283) during this review's flight. Per Law #13 (repo-wide grep before minting), R3 takes **EXP086** (verified free: zero mentions, no protocol file).

---

## 1. Law #15 four answers

1. **Exact question:** do per-instance perturbations aligned with the leading right singular vectors of the frozen model's downstream Jacobian product yield strictly larger decision-flip rates per unit norm than random or semantic-static directions — and does the per-instance maximum-gain direction carry decision-relevant content rather than merely amplifying noise? [HYPOTHESIS]
2. **Decision it changes:** KILL / CONTINUE / HELD / PIVOT on the **dynamical-amplifier mechanism family** (TNA+JPI). A CONTINUE licenses the family for full-scale follow-up; it does **not** license any capability claim above pilot-level L1 evidence.
3. **Cheapest test:** Stage A ($0 CPU, weight-only, advisory — §5) → Stage B live pilot: 60 items, per-item deflated power iteration (ranks {1,2,3}) + decision-normal VJP + flip arms at matched norms ≈ **7,260 forward-equivalents ≈ 0.09 T4-h (~5–6 min)** honestly counted (§11). No cheaper test discriminates the rank-ordering signature.
4. **Mathematical license + quantitative prediction + breaking point:** [THEOREM] T1 (SVD maximizer, §2) licenses the *construction* (v̂₁ maximizes linearized logit displacement); it does **not** license the flip prediction — that is [CONJECTURE] C2. Quantitative prediction: Δ := flip-rate(v̂₁) − flip-rate(v̂_rand) at matched norm satisfies **LCI(Δ) > δ_min = 0.05** (one-sided McNemar p ≤ 0.05), **and** the rank gradient Δ_rank := flip-rate(v̂₁) − flip-rate(v̂₃) satisfies **LCI(Δ_rank) > 0**. Breaking points: decision-orthogonal gain (ĉ < 0.1 with low exceedance → KILL); primary gain excluded (CI(Δ) entirely below +0.05 → KILL); rank gradient excluded with primary win (→ PIVOT, not CONTINUE); flat spectrum / non-convergence (→ INVALID/HELD, never a silent pass). Full verdict table §9.

## 2. Formalization

**Definitions.** Frozen model M, Δθ = 0. **D1:** h_ℓ(x) ∈ ℝ^d, d = 1024 (Pythia-410m), residual-stream state at the answer position of probe item x. **D2:** z: ℝ^d → ℝ^V, downstream map (blocks ℓ+1…L + unembedding) to logits, differentiable at h_ℓ(x) [ASSUMPTION: differentiability at the operating point; verified per-item by successful VJP — a failed VJP aborts the item]. **D3:** J(x) := Dz(h_ℓ(x)) ∈ ℝ^{V×d}, SVD J = UΣVᵀ, σ₁ ≥ σ₂ ≥ … ≥ 0. **D4:** v̂_r(x) := r-th right singular vector (defined up to sign; sign pinned §4). **D5:** n̂(x) := ∇_{h_ℓ}(z_top1 − z_top2)(h_ℓ(x)) — label-free decision normal from the model's own top-2 (one VJP; no test labels — Law #7 clean). **D6:** ĉ := (1/N)Σ_i |⟨v̂₁(x_i), n̂(x_i)⟩|, unit vectors.

**Licensed theorems (with scope — scope is part of the license).**
- **[THEOREM] T1 (SVD maximizer).** argmax_{‖u‖=1} ‖Ju‖₂ = ±v₁, value σ₁. *Proof sketch:* ‖Ju‖² = uᵀJᵀJu; JᵀJ = VΣ²Vᵀ symmetric PSD; Rayleigh quotient maximized at top eigenvector. ∎ *Scope:* licenses **linearized logit-displacement maximality at the operating point only** — nothing about decision flips, nothing about σ₁ being large, nothing about decision-subspace alignment. (Discharges F4: Kreiss demoted — see below.)
- **[THEOREM] T2 (power-iteration convergence).** w_{t+1} = JᵀJw_t/‖JᵀJw_t‖ contracts toward v₁ geometrically at rate (σ₂/σ₁)^{2t} when σ₁ > σ₂. *Proof sketch:* expand w_0 = Σ c_k v_k; component ratios decay as (c_k/c_1)(σ_k/σ₁)^{2t}. ∎ *Scope:* σ₁ ≈ σ₂ → no convergence; diagnosable from the Rayleigh-quotient trajectory → pinned stall criterion §6 (F8).
- **[THEOREM] T3 (ĉ chance anchor).** Independent uniform unit vectors in S^{d−1}: E|⟨a,b⟩| = √(2/(πd)) ≈ **0.0249** at d=1024. *Scope:* v̂₁, n̂ are not independent — anchor calibrates the 0.1 bar (≈4× random mean); the kill rule is a decision rule, not a significance test (F14).

**Demoted conjectures (not licensed; the experiment tests them).**
- **[CONJECTURE] C1 (Kreiss, motivational only).** The Kreiss Matrix Theorem bounds sup_k ‖A^k‖ for powers of a *single square* matrix; J(x) = Π_{l>ℓ} J_l is a product of *distinct* Jacobians. Kreiss licenses nothing here — retained as motivational context only. (F4)
- **[CONJECTURE] C2 (flip prediction).** T1 → ‖Jδ‖ maximality; the path to decision flips crosses the linearization gap, the margin geometry (ĉ gate), and the flip sign. No theorem connects them. The 1.5× ratio bar is [ARBITRARY] (secondary descriptor with 1.2×/2.0× sensitivity bands); the binding bar is the **difference** Δ with δ_min = 0.05 (F5).
- **[CONJECTURE] C3 (rank ordering).** σ₁ ≥ σ₂ ≥ … orders *logit displacement*; monotone *decision-flip* ordering in singular rank is the discriminating prediction under test — measured by the rank arms (F1), not assumed.

## 3. Framing (F9)

- **Evidentiary ceiling: L1** (improves inference). Endpoint = decision flips on a fixed 2-hop MCQ probe set. No L2/L3 claim is licensed by any outcome of this pilot; any such claim is a separate pre-registration.
- **Control classification:** the direction is externally specified (experimenter-computed power iteration on VJPs) → **inference-time activation control**, never autonomous cognition (LOG-247). The skeleton makes no autonomy claim.
- **Founder's-address note:** this experiment is inference polish (a better compass for the same additive-injection hand), not a cognition upgrade. A positive rank-ordering would map the frozen model's Jacobian sensitivity geometry — structural knowledge useful to the L3 climb — but the pilot itself yields L1 evidence only.

## 4. Construction (pinned)

- **Model/site:** Pythia-410m, layer ℓ = 20, answer-position residual stream (program-standard site; matches EXP077/EXP084).
- **Per-item direction computation:** J(x) = ∂z/∂h_ℓ via autograd; **deflated power iteration** for ranks {1,2,3}: 12-iteration cap per vector; each iteration = 1 JVP (≈1 fwd) + 1 VJP (≈2 fwd); deflation (I − V̂V̂ᵀ)JᵀJ(I − V̂V̂ᵀ) for subsequent ranks. Rayleigh-quotient stall tol = **1e-3** (relative change; diagnosable from the iteration itself, per the specialist).
- **Sign rule (F2):** v̂_r ← sign(⟨v̂_r, n̂⟩)·v̂_r — oriented to the +gap side of the label-free decision normal. Rationale: gives the family its best licensed shot; an arbitrary numerical sign must not decide the treatment. ĉ gate uses |·|, unaffected.
- **Norms (F11):** ε ∈ **{0.15, 0.45} × ‖h_ℓ(x_i)‖₂** per-item [ARBITRARY]. Rationale: relative (scale-free); 0.15 is the small-perturbation regime where T1's linearization is most defensible → **primary**; 0.45 is the robustness check. No norm-scanning (post-hoc tuning forbidden, Law #9).
- **Arms (matched ‖δ‖₂ across arms — non-negotiable):** {v̂₁, v̂₂, v̂₃, v̂_rand, B_agg} × 2 norms + unintervened baseline. B_agg = the killed static-semantic family direction (historical anchor: "the old family fails here"). v̂_rand = fresh uniform unit vector per item per norm (seeded).
- **Stage-2 conditional arm (F10):** permuted-v̂₁ (item j's v̂₁ injected on item i, j a fixed derangement, seeded) × 2 norms — runs **only if** the primary win criterion fires (G3 pin, LOG-297: "the primary win criterion" = V7's first two conjuncts — LCI(Δ) > 0.05 **and** one-sided McNemar p ≤ 0.05); CONTINUE requires **LCI(Δ_perm) > 0** where Δ_perm := flip-rate(v̂₁) − flip-rate(permuted-v̂₁), paired per item, Tango 95% CI (G2, LOG-297: no bare point inequality — a noise-level inequality must not satisfy a binding conjunct). Item-specificity rationale: §A.3 item-3; R2 arm-(e) precedent.

## 5. Stage A — $0 CPU advisory screen (F3)

[ASSUMPTION] A Henrici index of the true layer-transition Jacobian J_l = ∂F_l/∂h_l requires an operating point (attention is input-dependent); no per-layer activation archives exist (LOG-243). Therefore the "$0 weight-only" screen **cannot** be the true J_l screen as worded.
**Pinned object:** He_affine per layer-block computed from the **frozen weight matrices alone**, restricted to the square blocks only — the attention O/V projections (d×d); the rectangular MLP up/down projections (d×4d / 4d×d) are excluded because λ_i is undefined for rectangular matrices (G1, LOG-297). He = (‖W‖_F² − Σ|λ_i|²)^{1/2}/‖W‖_F via CPU eigendecomposition of each square block. **Status: explicitly approximate, advisory, non-binding.** It **cannot KILL** the family alone; it is a prior-strength modifier recorded before Stage B. Rationale for keeping it: Law #15 cheapest-first; G1 precedent licenses read-only weight access. If Stage A shows near-normal weights everywhere, the pilot still runs (the rank arms test the actual claim) — the screen's weakness is declared, not hidden.

## 6. Stage B — pilot protocol

1. **Probe set (F11, D1):** the EXP077 official 60-record archive — `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`, sha256 `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` (G4, LOG-297; recomputed by this repair wave — matches the EXP084 signed protocol's recorded pin, verified 2026-09-24, file unmodified in git), **verbatim rebuild, fixed indices**. Any deviation (index shift, item substitution) is loudly logged per EXP084-D1; the deviation note is a required artifact.
2. **Headroom gate (feasibility, EXP079 class):** require **≥15 wrong-at-baseline** items among the 60 (verified at build from archived correctness records). Fewer → **INVALID** (infeasible probe — do not run).
3. **Per-item computation:** baseline forward (correctness + logits) → power iteration (ranks 1–3, §4) → n̂ VJP → ĉ accumulation → flip arms.
4. **Convergence guards (F8):** per item, abort the item's direction arms (keep baseline + random arm) if σ̂₁/σ̂₂ < **1.1** (no distinguished max-gain direction — the arm would degenerate to random); if **>50%** of items abort → **INVALID (UNDEFINED-LANDSCAPE)**. Rank-test validity: require σ̂₁/σ̂₃ ≥ **1.2**, else the rank test is UNDEFINED → HELD (fail-safe, never KILL).
5. **Apparatus check:** matched-norm v̂_rand at 0.45‖h‖ must produce nonzero margin movement (‖Δz‖₂ above the 1e-4 noise floor) on ≥80% of items — else **INVALID** (proxy-unresponsive apparatus; R2-F2 class).
6. **Δθ = 0 verification:** model state_dict hash before/after (G3-style); mismatch → INVALID.

## 7. Endpoints & statistics

- **Primary:** Δ := flip-rate(v̂₁) − flip-rate(v̂_rand) at norm 0.15, paired per item. Test: one-sided McNemar exact on the discordant flip pairs + **Tango 95% CI** for the difference. Binding bar: **LCI(Δ) > 0.05** and p ≤ 0.05. (F5: difference form; the 1.5× ratio reported as [ARBITRARY] secondary with 1.2×/2.0× sensitivity bands.)
- **Discriminating (rank):** Δ_rank := flip-rate(v̂₁) − flip-rate(v̂₃) at norm 0.15, Tango 95% CI. CONTINUE needs **LCI(Δ_rank) > 0** (F1, F7).
- **Kill-first diagnostic:** ĉ (D6) + exceedance fraction E := P(|⟨v̂₁,n̂⟩| > 0.1). ĉ < 0.1 **and** E < 10% → KILL (decision-orthogonal gain). ĉ < 0.1 with E ≥ 10% → HELD (re-scope to conditional variant; the mean masked a decision-useful minority) (F14).
- **Signed ledger (P3 demand):** per arm-pair report (b, c) = (wrong→right, right→wrong); report the anti-steerable fraction c/(b+c). A v̂₁ win driven by c > 0 elsewhere is flagged in the ledger even if Δ > 0.
- **Secondary:** norm-0.45 robustness (same tests, reported; no separate verdict unless it contradicts the primary — contradiction → HELD).

## 8. S3-9 contingency (F12)

| S3-9 outcome | R3 reading |
|---|---|
| S3-9 linear (g α-invariant) | Supports the linear-amplifier interpretation of any R3 win; strengthens the "mathematical home" claim for the ×1.8. |
| S3-9 nonlinear (CV_α[g] > 20%) | The linear-amplifier *reading* weakens, but the rank-order test still discriminates: routing predicts α-dependence, **not** singular-rank dependence. A rank-ordered win under S3-9-nonlinear → PIVOT the interpretation (gain is direction-structured, not a fixed linear amplifier), not KILL. |
| S3-9 not yet returned | R3 runs as designed; the contingency row is evaluated at analysis time. No blocking. |
Three-way note: S3-9-linear also keeps CLLC's ray-linearity channel (B2-class open-loop adaptivity) alive — consistent with an R3 win; no contradiction either way.

## 9. Verdict table (exact, pre-registered; evaluated in order)

**INVALID (apparatus/probe failures — fail-safe, never a scientific verdict):**
- V1: Δθ ≠ 0 (state_dict hash mismatch) → INVALID.
- V2: <15 wrong-at-baseline (headroom gate) → INVALID.
- V3: >50% items power-iteration non-converged (Rayleigh stall) → INVALID (UNDEFINED-LANDSCAPE).
- V4: apparatus check fails (random δ moves neither flips nor margins) → INVALID.

**KILL (family dead):**
- V5 (kill-first): ĉ < 0.1 **and** exceedance E < 10% → **KILL** — gain without decision relevance is noise amplification.
- V6: 95% Tango CI for Δ entirely below +0.05 (primary gain excluded) → **KILL**.

**CONTINUE (all conjuncts; §A.3 battery):**
- V7: LCI(Δ) > 0.05 **and** one-sided McNemar p ≤ 0.05 **and** LCI(Δ_rank) > 0 **and** Stage-2 LCI(Δ_perm) > 0 (Δ_perm := flip-rate(v̂₁) − flip-rate(permuted-v̂₁), paired per item, Tango 95% CI; G2, LOG-297) → **CONTINUE** — licenses full-scale follow-up of the dynamical-amplifier family at L1.
- V7b (G3, LOG-297 — evaluated after V7, before V8): primary win (V7's first two conjuncts) **and** LCI(Δ_rank) > 0 **and** permuted fail (Stage-2 conjunct not met: LCI(Δ_perm) ≤ 0) → **HELD** — gain is not item-specific; the direction-noise reading (F10's repair) — do not CONTINUE.

**PIVOT (effect real, family signature failed):**
- V8: primary win (V7's first two conjuncts) **and** 95% CI for Δ_rank entirely below +0.05 with point estimate ≤ 0 (rank gradient excluded) → **PIVOT** — re-scope to the *max-displacement direction* reading (the model's most-amplified direction carries decision content, but not rank-ordered); the dynamical-amplifier family's discriminating signature failed. Deliberate deviation from the sprint's "flat rank → KILL": a real primary effect is not discarded; the *family claim* is what dies.

**HELD:**
- V9: primary win but rank straddles (CI(Δ_rank) crosses 0, not excluded) → **HELD** (R2-R2 precedent: win without the mechanism signature is not CONTINUE).
- V10: ĉ < 0.1 with E ≥ 10% → **HELD** (re-scope to conditional variant).
- V11: σ̂₁/σ̂₃ < 1.2 (rank test undefined) → **HELD**.
- V12: primary straddles (CI(Δ) crosses +0.05, not excluded by V6) → **HELD**.

## 10. Law #7 hygiene

Construction uses only the model's own logits and its own top-2 (VJPs) — **no test labels touch direction construction**. Labels are used solely at evaluation (correctness endpoints) — standard. n̂ = ∇(z_top1 − z_top2) is label-free. No bridge arm (no label-informed method as method or control). The permuted control is label-free. [FACT: Law #7 compliant by construction.]

## 11. Budget (honest forward-equivalents — F6)

Per item: deflated power iteration 3 vectors × 12 iters × (1 JVP ≈ 1 fwd + 1 VJP ≈ 2 fwd) = **108**; n̂ VJP = **2**; arms 5 × 2 norms + baseline = **11** fwd. **≈121 fwd-equiv/item → 60 items ≈ 7,260 fwd-equiv ≈ 0.09 T4-h (~5–6 min)** at the program rate (~80k passes/T4-h). Stage-2 permuted (conditional): 120 fwd-equiv ≈ 0.0015 T4-h. Stage A: $0 CPU. [CONJECTURE until GPU-node actuals are logged — R2 precedent; the runner logs wall-clock and pass counts.] The coordinator's "360 passes ≈ 0.0045 T4-h" is superseded — it omitted the VJP/JVP costs the specialist itself priced (LOG-285 F6).

## 12. Provenance corrections (F13)

The ×1.8 downstream gain (g mean 1.797, std 0.052, rescued n=8) is **S3-8/LOG-225 on EXP066 bridge-rescued items** — not "K3 Phase-0" (which proved premise-rank/donor construction values g = 1.9225/1.0618). Cited correctly here.

## 13. Reproducibility (Law #13)

Seeds pinned for v̂_rand draws and the Stage-2 derangement; environment manifest logged; model parameter hash pre/post (§6.6); raw per-item logs preserved (v̂_r, σ̂_r, Rayleigh trajectories, n̂, ĉ components, arm outcomes, signed ledgers). Epistemological labels (§2) used throughout; no post-hoc metric changes (Law #9); failed items/runs retained (Law #8).

## 14. Discharge index (LOG-285 F1–F14 → section)

F1 rank arms + Δ_rank → §4, §7, §9-V7/V8/V9. F2 sign rule → §4. F3 Stage-A object + non-binding status → §5. F4 Kreiss demoted, T1 operative → §2. F5 difference-form primary + [ARBITRARY] ratio → §1, §7. F6 honest inventory → §1, §11. F7 CI-exclusion rank rule → §7, §9. F8 convergence/flatness guards → §4, §6. F9 L1 ceiling + control classification → §3. F10 permuted Stage-2 → §4, §9-V7. F11 probe set + norms + headroom + D1 → §4, §6. F12 S3-9 contingency → §8. F13 provenance → §12. F14 ĉ anchor + exceedance → §2-T3, §7, §9-V5/V10.

LOG-297 re-review fixes G1–G4 → section: G1 He_affine square-block restriction → §5. G2 paired permuted bar (Δ_perm, Tango 95% LCI > 0) → §4, §9-V7. G3 new V7b HELD row + Stage-2 primary-win gate pin → §4, §9. G4 EXP077 archive digest → §6.1.

## 15. Queue & gates

GPU-dark until CEO clearance; queued behind K2 → EXP083 → EXP084. Stage A ($0) may run immediately on CPU (read-only weight access, G1 precedent). **No runner build until a fresh Law #14 re-review (different reviewer) signs this draft.**
