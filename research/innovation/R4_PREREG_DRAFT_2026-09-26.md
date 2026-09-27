# R4 (EOC) — Full Pre-registration DRAFT (UNSIGNED)

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. NOT reviewed.*
*Licensing chain: LOG-4353 (Friday cull, worth-it analysis + unsigned skeleton licensed) → LOG-4354 (Stage −1: citation verified with attribution correction, λ̂ proxy well-defined, CONTINUE to full pre-registration signaled).*
*Built from: `R4_PREREG_SKELETON_2026-09-25.md`, `R4_WORTHIT_ANALYSIS_2026-09-25.md`, `R4_STAGE_MINUS1_REPORT_2026-09-26.md`.*
*Requires before execution: independent Law #14 review + SIGN, CEO GPU clearance, sequencing behind K2→EXP083→EXP084→EXP086-B→EXP088→EXP087 queue. Does NOT mint an experiment number.*

---

## 0. Law #15 block (binding)

**Precise question.** Does per-item gain scheduling toward λ̂ ≈ 0 change 2-hop decisions beyond fixed-gain baselines — i.e., is **distance-to-criticality a usable per-item control signal** for a frozen model (Δθ = 0), using attention-softmax temperature τ and/or residual-stream scale as runtime scalar actuators? [HYPOTHESIS]

**Decision it changes.** **KILL** criticality-scheduling if scheduled-g ΔM ≤ best-fixed-g ΔM, or gain shows no |λ̂|-dose-response (Spearman p ≥ 0.1). **CONTINUE** to a pre-registered (diagnostic, gain-actuator) sweep **only** on the dose-response signature (ΔM > 0 AND Spearman one-sided p < 0.05). **Dead zone:** 0.05 ≤ Spearman one-sided p < 0.1 → **Underdetermined (hold)** per §7 — neither kill nor continue; no further spend. **Diagnostic-invalid branch:** λ̂ unmeasurable/unstable across seeds/ε → KILL the candidate (not the theory), at Stage 0 before any scheduling spend. **PIVOT branch:** Underdetermined and STOP outcomes route to re-design, never to the sweep (a design change becomes a new candidate, not a silent edit).

**Cheapest falsifying test.** Stage 0 diagnostic gate (**480 passes ≈ 0.0061 T4-h**): 2 passes/item × 60 items for λ̂_baseline (ε-direction seed pinned exactly once) **plus** the budgeted stability arm — 3 pre-registered ε-direction re-measurement seeds × 2 passes/item × 60 items (§2.4, D_stab). If λ̂ is unstable across seeds/ε, or the Var(|λ̂_baseline|) floor gate fires, the candidate dies or holds before any gain is ever scheduled. Total pilot cost ≈ 0.0098 T4-h (free-tier GPU), sixth in the sprint's cost order (behind R6, R1, R2, R5, R3).

---

## 1. Background and license

### 1.1 Citations (corrected per Stage −1 — see §4)

- [FACT] **Poole, Lahiri, Raghu, Sohl-Dickstein, Ganguli, "Exponential expressivity in deep neural networks through transient chaos", arXiv:1606.05340, NIPS 2016** — proves the order-to-chaos expressivity phase transition in random deep nets and derives the correlation-map slope χ₁ (Eq. 7), a multiplicative stretch factor partitioning ordered (χ₁ < 1) from chaotic (χ₁ > 1) regions. **Cited here for:** the χ₁/order-to-chaos framework only. χ₁ − 1 is the theoretical object the λ̂ diagnostic finite-differences across depth, licensing the λ̂ = 0 criticality criterion.
- [FACT] **Schoenholz, Gilmer, Ganguli, Sohl-Dickstein, "Deep Information Propagation", ICLR 2017, arXiv:1611.01232** — the "signal-propagation depth scales are maximal at criticality" theorem belongs to THIS paper, not Poole 2016 (verified by full-text search of Poole 2016: zero occurrences of "depth scale"; Schoenholz abstract: "in networks at the edge of chaos, one of these depth scales diverges. Thus arbitrarily deep networks may be trained only sufficiently close to criticality."). **Cited here for:** the depth-scale-maximality claim — the half of the license that says scheduling λ̂ → 0 maximizes the item's effective propagation depth, hence representational expressivity at decision time.

### 1.2 Mathematical license

[THEOREM-level in random nets; translated as [HYPOTHESIS] for frozen inference] Per-item finite-time stretch λ̂(x) measures distance from criticality across depth. Scheduling the model's intrinsic global gain to push λ̂ → 0 maximizes the item's effective propagation depth.

**Quantitative prediction (pre-registered):** gain concentrates on items with |λ̂_baseline| ≫ 0 (far-from-critical); items already near λ̂ ≈ 0 gain ~0. Formally: Spearman(gain_i, |λ̂_baseline,i|) > 0, one-sided p < 0.05, AND scheduled-g ΔM > best-fixed-g ΔM (gain_i defined in §6).

**The |λ̂|-dose-response is non-negotiable.** It is the signature no alternative predicts:
- fixed-temperature predicts *uniform* effects (no dose-response);
- PWAR predicts *entropy-dispersion* response (different diagnostic) — mutually discriminating on the same 60 items, which is why PWAR piggybacks.

**Sharpest breaking point in the sprint:** scheduled-g ΔM ≤ best-fixed-g ΔM, **or** gain uncorrelated with |λ̂_baseline| (Spearman p ≥ 0.1) → the criticality story is decorative → **KILL**.

### 1.3 Honest audit of the license (adversarial pass — carried forward, not softened)

- **Gap 1 — trainability → decisions.** The theorems are about signal propagation at initialization (trainability/expressivity), not decision accuracy under inference-time gain modulation. The link is analogical — one inferential step beyond the theorem. [CONJECTURE] *The license licenses the test, not the conclusion.* If the analogy is false, the signature won't appear, and the breaking point fires. Stated honestly in any downstream write-up.
- **Gap 2 — temperature confound.** Modulating τ directly sharpens/softens attention; any gain could be a plain temperature effect. Mitigation is structural, not rhetorical: uniform gain across |λ̂_baseline| = the temperature story = **KILL by the breaking point**. The design anticipates its own confound via the dose-response.

---

## 2. Design (frozen model, Δθ = 0)

### 2.1 Diagnostic

Per item x: λ̂(x) = log(‖Δh_L‖/‖Δh_0‖)/L from two nearby forward passes (x, x+ε), where the ε-direction is a pinned random unit direction with its seed pinned **exactly once** (LOG-4354 hardening (b)). L = depth in layers (last hidden state Δh_L relative to input-layer Δh_0).

**Stage −1 result (carried):** on a numpy toy random MLP (widths [64, 128×10, 64], tanh, 20 items, 860 measurements, all computed not invented): 0 NaN/0 Inf; ε-robust over 5 decades (1e-6…1e-2, cross-decade Pearson r = 1.0000); regime discrimination gain 0.5 → λ̂ = −0.683 (ordered), 1.0 → λ̂ = −0.004 (critical), 1.5 → λ̂ = +0.210 (chaotic), regime separation 30–60× the within-item seed noise; seed stability: within-item std 0.013 vs cross-item std 0.003 on the random net. **Honest reading carried forward:** the proxy is mechanically sound, but on random nets the per-item λ̂(x) signal is seed noise, not item structure — hence the seed pin and the load-bearing variance floor (§5).

### 2.2 Actuator

Global gain g — **runtime scalars only**: attention softmax temperature τ and/or residual-stream scale. No vectors added, no directions injected. Δθ = 0 throughout (pre/post weight hash per Law #13).

### 2.3 Scheduler (pre-registered mapping — no scheduler λ̂-evaluations; LOG-4356 F3 repair)

Per item: g(x) = M(λ̂_baseline(x)) — a **pre-registered deterministic mapping** from the pinned baseline diagnostic to a gain setting on the frozen §3 grid (grid positions only; numeric multipliers remain [OPEN] to the manifest). No λ̂(x; g) is measured to choose the setting — the argmin-over-measurements design is replaced, so the scheduler consumes **zero diagnostic passes**:

- **Direction:** sign(λ̂_baseline,i) — ordered side (λ̂ < 0) → the sharpening-direction step; chaotic side (λ̂ > 0) → the softening-direction step.
- **Dose:** |λ̂_baseline,i| above/below the **pre-registered median split** of the pooled Stage 0 baseline distribution (computed before any scheduling, label-free) — above median → the full step in the sign direction; at/below median (near-critical) → neutral. This encodes the pre-registered prediction "items already near λ̂ ≈ 0 gain ~0" structurally.

The grid size is pre-registered at **3 settings** (neutral + one sharpening step + one softening step); the scheduled setting is therefore always a grid setting, so scheduled-gain decisions are covered by the 3 decision passes/item (§2.4). The mapping fixes the *assigned setting*, not the *outcome* — gain_i (§6) remains an observed margin difference, so the Spearman dose-response prediction is empirical, not tautological. λ̂ is computed from two nearby forward passes — **label-free by construction; Law #7 clean** (no test labels in the diagnostic or the scheduler).

### 2.4 Arms and budget (60 items)

| Arm | Passes/item | Purpose | Spend |
|---|---|---|---|
| D_base (diagnostic) | 2 | λ̂_baseline; ε-direction seed pinned exactly once | 120 passes |
| D_stab (diagnostic) | 6 (3 seeds × 2) | λ̂ seed-stability re-measurement (Stage 0 gate, §5) | 360 passes |
| G_sched | 3 (one per grid setting) | scheduled-gain decisions + best-fixed-gain grid decisions (scheduled setting is always a grid setting per §2.3) | 180 passes |
| G_manip | 2 | manipulation check: λ̂ measured at the scheduled gain (§5) | 120 passes |

**Stage 0 (diagnostic gate): 480 passes ≈ 0.0061 T4-h. Stage 1 (pilot): 300 passes ≈ 0.0038 T4-h. Total pilot: 60 × 13 = 780 passes ≈ 0.0098 T4-h (free-tier GPU).** PWAR piggyback: entropy-dispersion diagnostic recorded on the same 60 items at $0 marginal (PWAR is HELD — piggyback-only, no PWAR claim licensed by this experiment).

---

## 3. Fixed-gain grid (pre-registered as a real grid — Gap-4 hardening)

The fixed-gain baseline is the **same candidate gain set used in G_sched, held constant per item** — so "best fixed gain" is a real grid search over explicitly named settings, not a single arbitrary τ. Grid structure is fixed before execution:

- **Structure (frozen pre-execution):** multiplicative gain factors on the default temperature τ₀ (τ = τ₀ × m) and/or residual-stream scale factors s, symmetric about the neutral setting (m = 1 / s = 1), the neutral setting included as one arm, spanning both the ordered-sharpening and chaotic-softening directions. The *exact numeric multipliers are not invented here* and are finalized in the pre-registered execution manifest at Law #14 review — recorded before execution, never during. ([OPEN] until manifest sign.)
- The grid is **frozen before execution**; adding a setting after seeing results is a protocol violation (Law #3 / Law #9).

---

## 4. Citation erratum (append-only)

The worth-it analysis stated "signal-propagation depth scales are maximal at criticality" as a Poole 2016 theorem. **Correction (Stage −1, LOG-4354):** that claim is Schoenholz et al. 2017 (arXiv:1611.01232); Poole et al. 2016 (arXiv:1606.05340) is cited for the χ₁/order-to-chaos framework. This draft attributes correctly everywhere (§1.1). The worth-it file now carries its own append-only erratum (appended 2026-09-26; the original §4 text there is unedited — correction by append-only erratum only); signed artifacts were not touched.

---

## 5. Stage 0 diagnostic gate (before any scheduling — sequence is kill-first)

| Gate | Test | Fail action |
|---|---|---|
| Seed/ε stability | λ̂ re-measured across K = 3 pre-registered ε-direction seeds (D_stab arm, §2.4: 3 × 2 passes/item — budgeted, LOG-4356 F2 repair); unstable → | **KILL candidate** (diagnostic-invalid — not a KILL of the theory) |
| Manipulation check | λ̂ measured at the scheduled gain (G_manip arm, §2.4: 2 passes/item — budgeted); λ̂ doesn't move under scheduling → | **STOP** — no further spend |
| **Variance floor (LOG-4354 hardening (b))** | Var(\|λ̂_baseline\|) must exceed the pre-registered floor; floor defined relative to Stage 0's own seed-noise measurement: **Var_cross(\|λ̂_baseline\|) must exceed the pooled within-item seed variance Var_within from the stability arm** (discriminability > 1). The Stage −1 toy showed within-item seed std 0.013 vs cross-item std 0.003 — if a frozen model's items show no more λ̂ variance than seed noise, the Spearman test is powerless. | **Underdetermined** — never KILL on a powerless test |

No variance → **Underdetermined (not KILL)** — never kill on a powerless test.

---

## 6. Endpoints

- **Primary:** ΔM = accuracy(scheduled-g) − accuracy(best fixed-g), paired per item.
- **Signature (non-negotiable):** Spearman(gain_i, |λ̂_baseline,i|), one-sided, where **[DEFINITION] gain_i := margin_scheduled,i − margin_best-fixed,i** — margin is the logit (log-odds) difference between the correct choice and the highest-logit incorrect choice on item i, computed from the same frozen forward passes that produce the decision (evaluation labels used at the endpoint only; Law #7 clean — no labels in the diagnostic or scheduler). gain_i is continuous by construction (not a {−1, 0, +1} accuracy-difference variable). **Ties treatment (pre-registered):** exact ties in the rank inputs are measure-zero; if one occurs (e.g., a degenerate 0.0 margin), use midrank averaging and report the count of tied ranks — this is the conservative standard and cannot make the one-sided p < 0.05 gate easier to fire. Both the ΔM edge and the dose-response must fire.
- **Manipulation check:** λ̂ moves under scheduling (else STOP per §5).
- **Power gate:** §5 variance floor.

---

## 7. Decision table (pre-registered — verdicts, not procedures)

| Condition | Verdict |
|---|---|
| λ̂ unstable across seeds/ε (Stage 0) | **KILL** candidate (diagnostic-invalid) |
| Manipulation check fails (λ̂ doesn't move under scheduling) | **STOP** — no further spend |
| Var(\|λ̂_baseline\|) below floor (Stage 0) | **Underdetermined** — powerless test; never KILL |
| scheduled-g ΔM ≤ best-fixed-g ΔM | **KILL** — criticality story decorative |
| Spearman p ≥ 0.1 (no \|λ̂\| dose-response) | **KILL** — criticality story decorative |
| Spearman one-sided 0.05 ≤ p < 0.1 | **Underdetermined (hold)** — weak evidence: too ambiguous to kill, too weak to license the sweep; no further spend authorized; candidate held (not killed, not continued) pending a pre-registered powered follow-up |
| ΔM > 0 AND Spearman one-sided p < 0.05 | **CONTINUE** → pre-registered (diagnostic, gain-actuator) sweep |

---

## 8. Guards (pre-registered)

- **Δθ = 0:** weight hash before and after every stage (Law #13). Any hash mismatch voids the run.
- **Bench pin / thread pin:** hardware and thread configuration pinned for the full run.
- **Law #7:** no test labels in the diagnostic or the scheduler — λ̂ is label-free by construction; PWAR piggyback records only the diagnostic value.
- **Seed pin:** the ε-direction seed is pinned exactly once (LOG-4354 (b)); the pin is logged.
- **Grid freeze:** the fixed-gain grid (§3) is frozen before execution; no mid-run edits.
- **$0 compute for this draft:** this document is on-paper only. No model runs, no weights touched, no GPU contact.

---

## 9. What this draft does NOT do

- Does not sign anything; does not authorize GPU; does not mint an experiment number (reserved for the signing lane).
- Does not finalize numeric grid multipliers (structural grid only; values finalized in the execution manifest at Law #14 review — recorded as [OPEN] in §3).
- Does not claim novelty beyond the program's adopted N1 position (no fresh prior-art claim made here).
- Does not touch PWAR beyond the $0-marginal piggyback diagnostic (PWAR remains HELD).

---

## 10. Next step

Independent **Law #14 adversarial review** of this draft → SIGN (or fix-list) → CEO GPU clearance → sequenced behind K2→EXP083→EXP084→EXP086-B→EXP088→EXP087. **Do NOT claim review happened.**

---

*Draft prepared 2026-09-26, on paper only, $0 compute, CPU only. No signed protocol file was edited; this is a new unsigned file.*
