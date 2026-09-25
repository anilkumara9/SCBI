# R4 EOC — Pre-registration SKELETON (DRAFT, UNSIGNED)

*Companion to `R4_WORTHIT_ANALYSIS_2026-09-25.md`. This is a skeleton only — structure and decision logic for the future pre-registration agent. NOT a protocol. NOT signed. NOT executable. Requires: citation verification (Poole et al. 2016), full Law #15 four-answers, Law #14 review + SIGN, CEO GPU clearance, and sequencing behind the K2→EXP083→EXP084→EXP086-B→EXP088→EXP087 queue.*

---

## 1. Question

Does per-item gain scheduling toward λ̂ ≈ 0 change 2-hop decisions beyond fixed-gain baselines?

## 2. Construction (frozen model, Δθ = 0)

- **Diagnostic:** per item x, λ̂(x) = log(‖Δh_L‖/‖Δh_0‖)/L from passes (x, x+ε). ε and seed pinned; stability across seeds pre-registered.
- **Actuator:** global gain g(x) ∈ {attention softmax temperature τ} ∪ {residual-stream scale} — runtime scalars only. No vectors added, no directions injected.
- **Scheduler:** g(x) = argmin_g |λ̂(x; g)| per item (toward criticality), vs fixed-gain grid baseline.

## 3. Arms (60 items)

| Arm | Passes/item | Purpose |
|---|---|---|
| D (diagnostic) | 2 | λ̂_baseline, λ̂ stability |
| G_sched | 3 (gain settings incl. scheduled) | scheduled-gain decisions |
| G_fixed grid | folded into G_sched settings | best-fixed-gain baseline (explicit grid, pre-registered) |

Total: 60 × 5 = 300 passes ≈ 0.0038 T4-h. PWAR piggyback: entropy-dispersion diagnostic recorded on the same 60 items ($0 marginal).

## 4. Endpoints

- **Primary:** ΔM = accuracy(scheduled-g) − accuracy(best fixed-g), paired per item.
- **Signature:** Spearman(gain_i, |λ̂_baseline,i|), one-sided.
- **Manipulation check:** λ̂ moves under scheduling (else stop — no further spend).
- **Variance gate:** Var(|λ̂_baseline|) above pre-registered floor (else Underdetermined).

## 5. Decision table (pre-registered)

| Condition | Verdict |
|---|---|
| λ̂ unstable across seeds/ε | KILL candidate (diagnostic-invalid) |
| Manipulation check fails | STOP (no further spend) |
| Var(\|λ̂_baseline\|) below floor | Underdetermined (powerless test — never KILL) |
| scheduled-g ΔM ≤ best-fixed-g ΔM | KILL |
| Spearman p ≥ 0.1 (no dose-response) | KILL |
| ΔM > 0 AND Spearman one-sided p < 0.05 | CONTINUE → (diagnostic, gain-actuator) sweep |

## 6. Guards

Δθ = 0 (pre/post hash); bench pin; thread pin; no test labels in diagnostic or scheduler (Law #7); ε/seed pinned; fixed-gain grid frozen before execution.

## 7. What this skeleton does NOT do

No citation (Poole 2016 unverified — Stage −1). No final numbers for ε, gain grid, variance floor. No signing. The pre-registration agent owns all of it.
