# EXP084 Protocol Specification (SIGNED): R2 Newton-vs-gradient duel

> **PRE-REGISTRATION SIGNED — Law #14 final SIGN recorded LOG-264.**
> This is the final signed skeleton: the LOG-263 repaired draft plus the two
> LOG-264 fixes applied verbatim (Fix 1 [REQUIRED] §7 INVALID(iii); Fix 2 [MINOR]
> §10 F7). The DRAFT file is superseded and retained as history; it was never
> edited into signed status. Signed protocols are immutable — any design change
> requires a new experiment number (Law #4). Runners may be built from this
> document only within the licensed scope (§12: implementation-bundle stage —
> evaluator test suite + startup smoke test; NO GPU execution, NO efficacy or
> capability claims).

**Experiment:** EXP084 — R2 repaired duel: scalar-curvature (finite-difference,
undamped, single-step) Newton vs gradient descent on the label-free top-2
margin proxy.
**Date:** 2026-09-24. **Status:** SIGNED (pre-registration; Law #14 review LOG-260 verdict SIGN-WITH-FIXES — all 10 findings discharged, §10; re-review LOG-262 verdict SIGN-WITH-FIXES — R1–R5 discharged (LOG-263), §10; final re-review LOG-264 verdict SIGN-WITH-FIXES — 2 fixes applied verbatim to this file; **final Law #14 SIGN recorded LOG-264**). **Cost:** $0 to draft (CPU only, no weights touched, no signed artifacts edited).
**Parent review:** `reports/adversarial_review_r2_newton_law14_2026-09-24.md`
(LOG-260, SIGN-WITH-FIXES, 10 findings). **Source packet:**
`research/proposals/AMBITION_SPRINT_SYNTHESIS_2026-09-24.md` (R2) and
`research/proposals/AMBITION_SPRINT_EXPDESIGN_2026-09-24.md` (X2 + §A.3/§A.4).

---

## 0. Law #15 packet (rewritten per F1, F4, F5)

**Q1 (precise question):** At a fixed injection site, does a single
curvature-derived Newton correction (scalar-curvature step
s_N = −g/κ̂_dir, keeping its **natural** step length — F1 repair (a)) beat a
fixed-norm gradient step on per-item gains of the label-free top-2 margin
proxy? Two contrasts, both pre-registered: (i) **cost-fair**: Newton (2 probes
+ 1 step-eval = 3 forward passes) vs re-linearized 3-step GD (3 forward
passes) — the primary duel (F5); (ii) **per-step quality**: Newton vs 1-step GD
at norm ρ — secondary screen. **R5c forward-equivalent disclosure:** Newton =
3 fwd-equiv (2 probes + 1 step-eval; g₀ sunk/shared); GD-costfair marginal ≈
7 fwd-equiv (3 fwd + 2 re-linearization bwd at 2× each; g₀ sunk/shared). The
asymmetry favors Newton and is **fail-safe for the KILL direction** — a
Newton win despite the handicap is stronger; a Newton loss at inflated
cost-fairness is a decisive kill.

**Q2 (decision):** **KILL** the tested flagship — *cheap finite-difference
undamped single-step scalar-curvature Newton along the gradient direction* —
if it ≡ or < cost-fair GD on margin gains (F3 scope; escape hatches named in
§7). **CONTINUE** to a curvature-spectrum study (≤660 passes) only if Newton
wins the cost-fair duel **and** beats random-direction and permuted-step
controls **and** satisfies the dose-response conjunct (e) (§7) — i.e. a
curvature-specific, item-specific win, not a generic-lucky-length one (R2).

**Q3 (cheapest-why):** 384 forward-equivalents — per item (N=24): 10 forward
passes + 3 backward passes (≈6 fwd-equiv) = 16 fwd-equiv; 24 × 16 = **384
fwd-equiv ≈ 0.0048 T4-h** @410m. *(The sprint's "120 passes ≈ 0.0015 T4-h"
omitted the random arm and all backward passes; the honest pilot cost is
≈3.2× the sprint claim — see §6.)*

**Q4 (math license):** [CONJECTURE] (F4 — the cited one-step-convergence theorem
does **not** license the prediction as a theorem). Partial license (re-derived
per R1, LOG-262 — the objective is margin **maximization**): on the local
quadratic model M(α) ≈ M₀ + ‖g‖α + ½κ̂_dirα² along ĝ, the scalar Newton step
α* = −‖g‖/κ̂_dir (s_N = α*ĝ, natural length ‖s_N‖ = ‖g‖/|κ̂_dir|) is the exact
1-D **maximizer** — valid iff κ̂_dir < 0 (concave along ĝ; α* > 0 uphill;
M(α*) = M₀ + ‖g‖²/(2|κ̂_dir|)). For κ̂_dir > 0 the same formula targets the
1-D **minimum** (α* < 0 downhill; M(α*) = M₀ − ‖g‖²/(2κ̂_dir) < M₀) — hence the
§3 definedness guard restricts arm (b) to the concave regime. The true Newton
step −H⁻¹g coincides with s_N only if ĝ is an H-eigenvector, which is not
established. **Prediction:** median(ΔM_Newton − ΔM_GD-costfair) > 0, larger
where |κ̂_dir| is large (where |κ̂_dir| is large, GD-1 at ρ = 1.0 overshoots the
concave max badly while Newton's small precise step lands near it; where
|κ̂_dir| is small, Newton's huge step overshoots). **Breaking point:** §7 KILL
row (CI-exclusion form, F10); CONTINUE additionally gated on the
dose-response conjunct (e) (§7).

---

## 1. Frozen model, SHA-256 guard, and site pins (F8)

- **Model / tokenizer (in-scope):** `EleutherAI/pythia-410m` (the model on
  which the boundary null's 410m leg was established, EXP066/EXP077).
- **Architecture [FACT]:** GPT-NeoX; d = 1024; 24 layers.
- **Intervention site (F8 pin):** layer-20 residual stream (index 20,
  0-indexed), at the answer position, via forward hook:
  h₂₀(ans_pos) ← h₂₀(ans_pos) + s. **Rationale:** EXP077's boundary-null site —
  a positive Newton result is directly comparable to the static family that
  died at this site; a null inherits the same comparability.
- **Guard procedure (Law #6/Law #13):** SHA-256 over `state_dict()` tensors
  (sorted keys, CPU, float32 bytes) pre/post run; binding guard is the runtime
  pre/post match. Pre-run SHA-256 additionally compared against the expected
  pinned hash
  `4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd`
  (carried from EXP083 §2 — same model `EleutherAI/pythia-410m`); mismatch →
  INVALID (§7, INVALID row (i)). $\boxed{\Delta\theta \equiv 0}$ non-negotiable (Law #6).
  Backward passes are gradient readouts w.r.t. activations only; no optimizer
  step exists anywhere.

## 2. Probe set, margin proxy, and Law #7 posture

- **Probe set:** EXP077 binary-decision probe set (N=60 records archived), items
  0–23 in archived order. **R5d archive pin:** `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`, sha256 `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` (verified 2026-09-24; file unmodified in git). "Archived order" = array order of that file — no outcome conditioning is possible (EXP077 was a null; margins were never its endpoint). [LICENSE CARRYOVER — LOG-262 adjudicated CONFIRM; for the re-review to verify; if the carryover is denied, the powered-stage protocol pins its own set.]
- **[DEFINITION] Margin proxy:** M(h) := z₁ − z₂, where z₁ ≥ z₂ are the two
  largest logits at the answer position from a forward pass with activation h
  at the site. Constructed from the model's own logits only — **no labels,
  targets, or benchmark metadata touch construction, selection, or scoring**
  (Law #7; §A.3 item 1). The LOG-204-demoted bridge appears nowhere.
- **License note L1 (LOG-262 adjudication: CONFIRM; R4 citation fix):** EXPDESIGN
  §A.4 registers margins as SECONDARY endpoints "ONLY where licensed by
  precedent (S3-8, K1)" and bans them as decision endpoints where the program
  has banned them. R2's primary endpoint is continuous ΔM margins. **The
  license cites the K1 precedent** (continuous margin-based decision endpoint,
  0.9 tilt bar, falsification verdict stands) — NOT "LOG-260's acceptance":
  LOG-260 accepted margins without discussion and never adjudicated §A.4.
  LOG-262 adjudication: **CONFIRM margin-primary** — (i) §A.4's discrete-ΔM
  default is written for binary-decision probe designs; no discrete decision
  event exists in this design — discretizing to top-1 flips discards the
  preregistered signal; (ii) at N=24 a flip endpoint makes KILL structurally
  unfirable (rule-of-three floor ≈ 0.125) → HOLD-by-design; (iii) the HL
  CI-exclusion KILL (§7) preserves §A.4's spirit. The verdict table (§7) stays
  on margins; a flip-endpoint swap would require re-derivation, not silent
  substitution (Law #4). The +0.01 bar's lack of decision-calibration is
  recorded as **fail-safe for a kill pilot**: an arbitrary small bar can only
  under-fire KILL (→ HELD), never over-fire it.

## 3. Formal construction (F1 repair (a))

Notation: for item i, h = h₂₀(xᵢ, ans_pos) ∈ ℝ¹⁰²⁴ from the clean baseline
pass; M₀ = M(h).

1. **Gradient:** g = ∇ₕM(h) via one backward pass through the logit readout
   w.r.t. the site activation (readout only; no weight update). ĝ = g/‖g‖₂.
2. **Directional curvature (F7 — κ̂_dir, NOT κ):** two central-difference
   probes M₊ = M(h + δĝ), M₋ = M(h − δĝ) with **pinned spacing δ = 0.1**
   (F8; δ = ρ/10, ρ pinned below). κ̂_dir := (M₊ − 2M₀ + M₋)/δ² — a
   **directional** curvature (Rayleigh-quotient estimate), not the condition
   number κ = λmax/λmin (F7). **Limitation recorded:** with a single spacing
   δ, "curvature ≈ 0" and "curvature drowned in noise" are indistinguishable;
   the second-δ replication probe is explicitly declined (keeps the pilot
   cheap) and too-noisy is marked UNDETERMINED in the §7 attribution rule.
3. **Newton arm (b) — natural length (F1):** s_N = −g/κ̂_dir (scalar-curvature
   Newton step). **No norm rescaling** — the arm keeps its curvature-derived
   natural step length; the honest duel is "does curvature-derived step-length
   selection beat a fixed-norm gradient step?" (F1 repair (a)). Under the
   corrected §3 guard (κ̂_dir < −κ_floor), s_N = α*ĝ with α* = ‖g‖/|κ̂_dir| >
   0 — an **uphill** step, the exact 1-D maximizer of the local quadratic
   model along ĝ (§0 Q4 re-derivation); ‖s_N‖ = ‖g‖/|κ̂_dir|.
4. **Newton-definedness guard, corrected (pre-registered; R1, LOG-262):**
   scalar Newton for a **maximization** objective is defined only where the
   local quadratic model is concave along ĝ. Arm (b) is **defined** iff
   κ̂_dir < −κ_floor := −1e-6, and **excluded** iff κ̂_dir ≥ −κ_floor. The
   old draft's "wrong-signed" descriptor belonged to the **positive** regime
   under maximization: for κ̂_dir > 0 the formula targets the 1-D minimum
   (α* < 0 downhill, M(α*) < M₀), so convex-uphill exclusions (κ̂_dir ≥
   +κ_floor: Newton-for-maximization undefined; model unbounded above along
   +ĝ) are reported **separately** from too-flat exclusions (−κ_floor ≤ κ̂_dir
   < +κ_floor, i.e. the excluded items not in the convex class: LOG-248 κR²
   regime, second order provably negligible at this scale) — R3a. Excluded items leave all Newton contrasts; they are counted
   with the split and reported. No cap, no rescaling, no rescue — capping
   would reintroduce F1-style scale manipulation. If arm (b) is defined on
   **< 12 of 24** items → INVALID/UNDEFINED-LANDSCAPE (§7). Median ‖s_N‖/ρ
   (over defined items) reported as context.

## 4. Arms and pins (F5, F8)

- **ρ (F8 pin):** ρ = 1.0. **Rationale:** matches EXP083's injected-norm scale
  (unit-norm direction at α = 1.0), keeping the R2 perturbation scale
  comparable to the RCPA family's.
- **Seeds (F8 pin):** master 20260924; per-item torch Generator seeded
  20260924+i; torch-exclusive random generator (EXP083 precedent); greedy
  decoding; fixed derangement for arm (e) from the master seed.

| Arm | Construction | Fwd passes/item |
|---|---|---|
| P0 baseline / identity | M₀ = M(h); doubles as §A.3-item-4 identity arm (bit-for-bit vs archived baseline) | 1 |
| (probe) curvature | M₊, M₋ at h ± δĝ, δ = 0.1 | 2 |
| (a) GD-1 | s = ρĝ; ΔM_a = M(h+s) − M₀ | 1 |
| (d) GD-costfair | 3 sequential steps, **re-linearized**: step k uses fresh gₖ = ∇M at the current point, step norm ρ/3 each; ΔM_d from the 3rd readout | 3 fwd + 2 bwd |
| (b) Newton | s_N = −g/κ̂_dir (natural length, uphill; defined iff κ̂_dir < −κ_floor per §3 guard, R1); ΔM_b = M(h+s_N) − M₀ | 1 |
| (c) random | s = ρr̂, r̂ isotropic unit (torch); ΔM_c — §A.3 item 2(a), information-destroyed | 1 |
| (e) permuted-Newton | item der(i)'s s_N applied to item i (fixed derangement, seed-pinned); ΔM_e — §A.3 item 3 | 1 |

Backward passes/item: g₀ (1) + g₁, g₂ for arm (d) re-linearization (2) = 3
backward ≈ 6 forward-equivalents.

**R5c fwd-equiv disclosure:** arm (d) GD-costfair costs 3 forward passes but
its re-linearization marginal is ≈7 fwd-equiv (3 fwd + 2 bwd at 2×; g₀
sunk/shared), vs arm (b) Newton at 3 fwd-equiv (2 probes + 1 step-eval; g₀
sunk/shared). The asymmetry favors Newton and is fail-safe for the KILL
direction.

**§A.3 battery mapping:** item 1 (Law #7) — clean, margin from model's own
logits; item 2(a) — arm (c); item 2(b) sign-flip / 2(c) position-shuffle —
**specific exemption argued** (for re-review): the verdicts turn on
*relative* contrasts (Newton vs GD), and the random arm plus the F2
sensitivity precondition carry the directionality/apparatus load; the
injection is single-position by design, so position-shuffle is a site change,
not a control; item 3 — arm (e); item 4 — P0 identity arm ($0); item 5 —
N/A (no labels anywhere).

## 5. Statistics (pre-registered)

- Primary contrasts are paired per-item differences of margin gains:
  ΔM_b − ΔM_d (cost-fair), ΔM_b − ΔM_a (per-step), ΔM_b − ΔM_c,
  ΔM_b − ΔM_e, ΔM_a − ΔM_c (F2 precondition).
- Tests: Wilcoxon signed-rank (paired), one-sided for directional claims. The
  KILL row carries **no** two-sided Wilcoxon: its non-difference verdict rests
  on the median(ΔM_b − ΔM_d) ≤ 0 direction prong plus the HL 95% CI-exclusion
  effect-size prong (§7) (R5b — the old "two-sided for KILL non-difference"
  phrase was vestigial and is removed). **CI (F10):** two-sided 95%
  Hodges–Lehmann interval for the median difference — the KILL's effect-size
  prong is CI-exclusion, not a point estimate.
- **Dose-response conjunct (e, R2):** Spearman rank correlation between
  |κ̂_dir| and (ΔM_b − ΔM_d), computed over the **defined item set**
  (κ̂_dir < −κ_floor), one-sided > 0 at pilot bar p ≤ 0.10 (F2 precedent);
  p by exact permutation. Tests Q4's "larger where |κ̂_dir| is large"
  prediction — curvature-specificity of the win. Failure → HELD(win not
  curvature-explained) (§7), never KILL.
- **Sensitivity precondition (F2, binding):** one-sided Wilcoxon
  (ΔM_a − ΔM_c) > 0 at p ≤ 0.10. Fail → INVALID/UNINFORMATIVE-PROXY —
  the margin proxy is unresponsive to gradient steps at this site; the
  apparatus is dead and **no family kill is licensed**.
- **F10 calibration:** the +0.01 margin-units bar is reported as a percentage
  of the session clean-margin IQR (context); no decision-calibration of the
  bar is claimed — recorded limitation. The uncalibrated status is **fail-safe
  for a kill pilot**: an arbitrary small bar can only under-fire KILL
  (→ HELD), never over-fire it (R4). The underpowered-HELD rule is
  structural: KILL requires the HL 95% CI upper < +0.01, which low power
  alone cannot satisfy (wide CIs straddle → HELD).

## 6. Pass budget (F6 — honest inventory)

| Item | Forward | Backward (≈2 fwd-equiv each) |
|---|---|---|
| P0 baseline/identity | 1 | — |
| g₀ gradient | — | 1 |
| curvature probes | 2 | — |
| arm (a) GD-1 | 1 | — |
| arm (d) GD-costfair (re-linearized) | 3 | 2 |
| arm (b) Newton | 1 | — |
| arm (c) random | 1 | — |
| arm (e) permuted-Newton | 1 | — |
| **Per item** | **10** | **3 (≈6 fwd-equiv)** |

**Totals (N=24):** 240 forward passes + 72 backward passes (≈144 fwd-equiv at
2× each) = **384 forward-equivalents ≈ 0.0048 T4-h** @410m (22 fwd/s measured
→ ≈17 s). **Correction recorded (F6):** the sprint's "120 passes ≈ 0.0015
T4-h" omitted the random arm (120 → 144 forward even before the F5 arm) and
all backward passes (≈5 fwd-equiv/item in the reviewed packet's own
accounting; 6 here with the re-linearized cost-fair arm); the true pilot cost
is ≈3.2× the sprint claim. Startup smoke budget (Law #14 gate at bundle
stage): ≤12 passes by precedent, priced at bundle build, not here.

## 7. Verdict table (F9 — complete; precedence order fixed)

INVALID rows preempt all scientific rows. Order: (i)→(iv) apparatus, then
sensitivity, then CONTINUE, then HELD(win-not-curvature-explained), then
HELD(step-noise), then KILL, then HELD(straddle).

| Row | Condition (all pre-registered) | Verdict |
|---|---|---|
| INVALID (i) | SHA-256 pre/post mismatch; or pre-run SHA-256 ≠ pinned `4c242d…dd` | **No verdict.** Apparatus failure; re-scope under a new number. |
| INVALID (ii) | P0 identity arm ≠ archived baseline bit-for-bit | **No verdict.** Session invalid (EXP083 precedent). |
| INVALID (iii) | Arm (b) defined (κ̂_dir < −κ_floor) on < 12 of 24 items | **UNDEFINED-LANDSCAPE.** The duel cannot run; not a family kill. |
| INVALID (iv) | F2 sensitivity precondition fails: one-sided Wilcoxon (ΔM_a − ΔM_c) p > 0.10 | **UNINFORMATIVE-PROXY.** Apparatus dead; never KILL. |
| CONTINUE | (a) Newton > GD-costfair one-sided p ≤ 0.05 **and** (b) Newton > random one-sided p ≤ 0.05 **and** (c) Newton > GD-1 one-sided p ≤ 0.05 **and** (d) Newton > permuted one-sided p ≤ 0.05 **and** (e) dose-response: Spearman(\|κ̂_dir\|, ΔM_b − ΔM_d) > 0 one-sided p ≤ 0.10 over the defined item set (§5) | License curvature-spectrum study (≤660 passes). Evidentiary: **Inconclusive** (pilot license only — EXP083 precedent). |
| HELD (win not curvature-explained) | (a)–(d) hold but (e) fails | Win is not curvature-explained (e.g. generic-lucky-length effect, §0 Q4): the win cannot license a curvature study → **Inconclusive**. Curvature-spectrum study NOT licensed. Explicitly not KILL. |
| HELD (step-noise) | (a) holds but (b) or (d) fails | Win is step-noise or non-item-specific curvature → **Inconclusive**. Neither kill nor continue licensed. |
| KILL (flagship, cost-fair) | CONTINUE not met **and** median(ΔM_b − ΔM_d) ≤ 0 **and** two-sided 95% HL CI upper < +0.01 margin units | **KILL the tested flagship** (F3 scope below). Evidentiary: **Not supported**. |
| KILL (directional, narrow) | Same criteria on ΔM_b − ΔM_a | Kills only the per-step-quality claim; reported secondary. |
| HELD (straddle) | None of the above — incl. HL CI straddling +0.01 (F10 underpowered rule) | **Inconclusive.** Pilot KILL-or-HOLD; no powered claims. |

**F3 kill scope (binding verdict language):** the KILL applies **only** to
"cheap finite-difference undamped single-step scalar-curvature Newton along
the gradient direction" — **on items where the scalar-curvature step is
defined (κ̂_dir < −κ_floor)** (R3b population qualifier; exclusions split
per §3). Explicitly **NOT killed** — each an [OPEN] escape
hatch needing its own Law #15 packet: (a) damped Newton / Levenberg-Marquardt
/ trust-region methods (raw Newton failing on non-convex landscapes is
textbook); (b) exact Hessian-vector products via autodiff/double-backprop
(no finite-difference noise); (c) quasi-Newton / multi-step curvature
accumulation; (d) Krylov/Lanczos subspace Newton directions distinct from g.

**F7 attribution rule (on KILL; [INTERPRETATION] only):** report median κ̂_dir
(defined set), IQR, and the **exclusion split** (R3a): (i) convex-uphill rate
(κ̂_dir ≥ +κ_floor — Newton-for-maximization undefined; model unbounded above
along +ĝ); (ii) too-flat rate (−κ_floor ≤ κ̂_dir < +κ_floor, i.e. the
excluded items not in the convex class — LOG-248 κR²
regime: second order provably negligible at this scale). Pre-registered
reading: flat-dominated exclusions at rate ≥ 50% → "consistent with too-flat";
convex-dominated exclusions reported as such — a convex-dominated pattern is
itself informative and must **not** be folded into "too-flat"; else if
sign(κ̂_dir) mixed across items with span > 10² → "curvature unstable at
spacing δ = 0.1 — too-noisy **UNDETERMINED** (single spacing; replication
declined, limitation recorded)." Attribution never changes the verdict.

## 8. Powered-stage pre-commitment (on CONTINUE only)

The licensed follow-up (≤660 passes) must: (1) carry a Krylov/Lanczos arm to
close F3 hatch (d) by design; (2) carry a damped-Newton arm to close hatch
(a); (3) stratify by κ̂_dir tertiles with a pre-registered dose-response rule
carrying the pilot's §7 conjunct (e) — Spearman(|κ̂_dir|, ΔM_b − ΔM_d) > 0 —
as the powered dose-response hypothesis;
(4) re-derive the endpoint license if the re-review replaces margins with
flips (L1). No powered claim is licensed by EXP084 itself under any row.

## 9. Queue position

Behind EXP083: **K2 → EXP083 → EXP084** on the user's Kaggle node
(GPU-sequencing only). No GPU clearance is requested or granted by this
draft. Execution remains unlicensed until: Law #14 re-review SIGN of the
final skeleton → implementation bundle + bundle review → CEO GPU clearance.

## 10. Finding-discharge index (LOG-260 F1–F10)

| Finding | Discharge | Section |
|---|---|---|
| F1 [structural] vacuous Newton arm | Repair (a): Newton keeps natural length ‖s_N‖ = ‖g‖/‖κ̂_dir‖; no rescaling; Q1 rewritten as "curvature-derived step-length selection vs fixed-norm gradient step". **R1 re-derivation (LOG-262):** under the corrected guard (defined iff κ̂_dir < −κ_floor) the step is the exact 1-D **maximizer** of the local quadratic model along ĝ (α* = −‖g‖/κ̂_dir > 0 uphill) — the old draft's guard kept the downhill regime | §0, §3–§4 |
| F2 dead-apparatus KILL | GD > random one-sided p ≤ 0.10 sensitivity precondition; fail → INVALID/UNINFORMATIVE-PROXY, never KILL | §5, §7 |
| F3 family-kill overreach | KILL scoped to the tested flagship; 4 escape hatches named [OPEN] in verdict language; **R3b:** scope names the defined population (κ̂_dir < −κ_floor) | §7 |
| F4 unlicensed theorem | One-step theorem demoted; prediction marked [CONJECTURE] with the 1-D quadratic-model partial license stated honestly — **R1 re-derivation (LOG-262):** the step is the exact 1-D **maximizer**, valid iff κ̂_dir < 0; coincides with −H⁻¹g only if ĝ is an H-eigenvector | §0 |
| F5 circular cost argument | Arm (d): re-linearized 3-step GD, 3 forward passes = Newton's 3; primary duel is cost-fair | §4, §7 |
| F6 short inventory | 240 fwd + 72 bwd (≈144 fwd-equiv) = 384 fwd-equiv ≈ 0.0048 T4-h; sprint's 0.0015 corrected (≈3.2×); R5c fwd-equiv asymmetry disclosed | §6, §0 |
| F7 "measured κ" misnomer | κ̂_dir = directional curvature; too-flat rule pre-registered; too-noisy UNDETERMINED (single δ, replication declined, limitation recorded). **R1/R3 re-derivation (LOG-262):** definedness guard corrected — defined iff κ̂_dir < −κ_floor (concave/maximization regime); attribution splits convex-uphill (κ̂_dir ≥ +κ_floor) vs too-flat (−κ_floor ≤ κ̂_dir < +κ_floor) exclusions | §3, §7 |
| F8 unpinned ρ/site/seeds | ρ = 1.0 (EXP083 scale); site = L20 residual stream, answer position (EXP077 site); seeds 20260924 / 20260924+i, torch-exclusive; δ = 0.1 | §1, §4 |
| F9 incomplete verdict table | HELD(step-noise), INVALID(iii–iv), HELD(straddle) rows added; **R2:** CONTINUE conjunct (e) (Spearman dose-response, p ≤ 0.10) added with new HELD(win-not-curvature-explained) row; permuted arm stays as §A.3-item-3 conjunct (d); precedence fixed and partition verified | §7 |
| F10 N=24 asymmetry, uncalibrated bar | KILL's effect-size prong is HL 95% CI-exclusion (upper < +0.01) — low power cannot fire it; bar reported vs clean-margin IQR as context, no decision-calibration claimed; **R4:** uncalibrated status recorded as fail-safe for a kill pilot (can only under-fire KILL → HELD, never over-fire) | §5, §7 |

## 11. Items for the Law #14 re-review (LOG-262 adjudications recorded, not silently resolved)

LOG-262 adjudicated all five drafter-flagged items (four CONFIRM, one CONFIRM-with-citation-fix); the re-review is asked to **verify** each adjudication against the repaired text.

- **L1 (margin-primary endpoint):** LOG-262 adjudicated **CONFIRM** — license
  cites the **K1 precedent** (continuous margin-based decision endpoint; R4
  citation fix applied in §2; "LOG-260's acceptance" citation removed).
  Re-review: verify the adjudication, or replace with the flip endpoint per §2.
- **Probe-set carryover:** LOG-262 adjudicated **CONFIRM** (EXP077 set archived
  and fixed; "items 0–23 in archived order" admits no outcome conditioning).
  R5d archive pin applied: `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`, sha256 `47281cd3…0585` (§2). Re-review: verify.
- **§A.3 exemptions:** LOG-262 adjudicated **CONFIRM** the 2(b)/2(c) exemption
  argument (§4) — the length-isolation concern it leaves open is carried by
  the R2 dose-response conjunct (e). Re-review: verify.
- **κ_floor = 1e-6 and the <12/24 INVALID bar:** LOG-262 adjudicated
  **CONFIRM, sign-corrected** — both are pinned pre-registered guards, not
  verdicts; both fail safe (INVALID preempts KILL); exclusion is on a
  pre-treatment covariate (κ̂_dir), not on outcomes — not gameable.
  Re-review: verify.
- **Arm (d) re-linearization:** LOG-262 adjudicated **CONFIRM** — fixed-direction
  3-hop is endpoint-identical to arm (a); re-linearized 3-step GD is the right
  cost-fair competitor. R5c fwd-equiv disclosure applied (§0, §4).
  Re-review: verify.

## 12. Promotion path (signed)

**SIGNED** — Law #14 final SIGN recorded LOG-264 (the gated re-review; no
further protocol review required). The two LOG-264 fixes are applied verbatim
in this file (§7 INVALID(iii), §10 F7); the DRAFT is superseded, never edited.
Next gates: implementation bundle → **bundle review** → CEO GPU clearance →
queue K2 → EXP083 → EXP084 (GPU-sequencing only). Licensed by this protocol:
implementation-bundle stage ONLY — evaluator test suite + startup smoke test.
NOT licensed: GPU execution, model weights, efficacy/capability/H-level claims,
α other than the pinned construction, bridge-as-mechanism arms, signed-artifact
edits. $0 spent to this point; CPU only; no weights touched.

*End of draft skeleton. Next step per program law: Law #14 re-review of this
document as a design object.*
