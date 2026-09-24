# CLLC Formalization — Closed-Loop Control of a Frozen Backbone

*Draft theory document, 2026-09-23 (LOG-246). Not a signed protocol. Pre-registration
skeleton in §8 is a draft for future Law #14 review — nothing here licenses GPU execution.*

*Revised 2026-09-23 per reviewer's corrections: (1) prior-art boundary — Activation-LQR
is closed-loop, CLLC's novelty narrowed to Jacobian-free low-information feedback;
(2) S3-9 renamed "linearity diagnostic", P1 demoted to heuristic; (3) out-of-distribution
language replaces "undefined"; (4) actuation language corrected; (5) autonomy
classification restricted to "inference-time activation control". This revision
supersedes the LOG-246 draft text; history preserved in git. Logged as LOG-247.*

## 0. Status and question

CLLC (closed-loop control over frozen activations) is the program's leading replacement
large bet if K2's P2 gate fires (final-position-local Supported). It is currently
unproven and unformalized. This document does the mathematical work now, on CPU, so the
pivot battery can launch the moment P2 fires instead of starting from scratch.

**Revised core question:** can a cheap, Jacobian-free, partially observed feedback
controller improve frozen-model inference over both optimized open-loop and adaptive
open-loop control, at matched compute, information, and intervention budget, and does
it offer any advantage over existing closed-loop activation control such as
Activation-LQR?

## 1. Setup: the frozen forward pass as a discrete-time dynamical system

Fix an input instance $x$. Let $F_\ell : \mathbb{R}^d \to \mathbb{R}^d$ be the frozen
$\ell$-th transformer block (attention + MLP + residual), $\ell = 0,\dots,L-1$, with
parameters $\theta$ fixed ($\Delta\theta \equiv 0$, Law #6).

- **Nominal trajectory:** $s_0 = E(x)$, $s_{\ell+1} = F_\ell(s_\ell)$.
- **Controlled trajectory:** inject $u_\ell \in \mathbb{R}^d$ at layer $\ell$:
  $\tilde{s}_\ell = s_\ell + u_\ell$, $s_{\ell+1} = F_\ell(\tilde{s}_\ell)$.
- **Objective:** $J = \varphi(s_L) + \lambda \sum_{\ell=0}^{L-1} \|u_\ell\|^2$,
  where $\varphi(s_L) = -\mathrm{margin}(s_L)$ (negative target-answer logit margin;
  minimizing $J$ maximizes the margin) or a 0/1 decision loss.
- **Observation:** $y_\ell = C s_\ell$, $C \in \mathbb{R}^{r \times d}$, $r \ll d$.
  In practice $C$ is a probe bank (logit-lens margin, trained linear probes).
  Partial observability is structural: we never observe "the answer" mid-pass.
- **Controller:** a policy $\pi_\ell : y_{0:\ell} \mapsto u_\ell$.
  Open-loop: $u_\ell$ are precomputed constants. Closed-loop: $u_\ell = \pi_\ell(y_\ell)$.

This is a finite-horizon discrete-time optimal control problem on a black-box nonlinear
plant. The plant is evaluable (forward passes) but not analytically known.

## 2. Four structural facts that decide what CLLC can and cannot do

- **(F1) Full actuation at the injection point.** Control enters additively in the
  full residual stream, so the linearized input matrix is $B_\ell = I_d$.
  *Direct actuation is not the injection-point bottleneck* — but this does not mean
  constrained useful reachability can never bind: the admissible set
  $\mathcal{U}_\ell$ (F4) and partial observability (F3) remain the operative
  constraints on what control can usefully achieve downstream.
- **(F2) Determinism.** The frozen forward pass has no process noise. The only
  "uncertainty" is model uncertainty ($F_\ell$ unknown analytically) and
  instance-to-instance variation.
- **(F3) Partial observability.** $\mathrm{rank}(C) = r \ll d$; the controller is
  blind to $d - r$ dimensions of the state.
- **(F4) Control authority is manifold-bounded.** Natural activations concentrate on
  a low-dimensional manifold $\mathcal{M}_\ell$. Define the Mahalanobis radius
  $\rho(u) = \sqrt{u^\top \Sigma_\ell^{-1} u}$ under a Gaussian fit to natural
  $s_\ell$. The admissible set is $\mathcal{U}_\ell = \{u : \rho(u) \le \rho_{\max}\}$;
  beyond it the model's behavior is out-of-distribution and empirically unsupported
  relative to the fitted natural-activation distribution — not mathematically
  undefined (the transformer remains defined everywhere), but unsupported by the
  calibration data, so budgeted control should not rely on it.

## 3. Theorem: no feedback benefit under ray-linearity

**Theorem.** Fix instance $x$ and injection layer $\ell_0$; set $u_\ell = 0$ for
$\ell \ne \ell_0$. Let $D(u) = \varphi(s_L(u))$ be the downstream objective as a
function of the single injection. Assume **ray-linearity**: $D$ is affine on the
budget set, $D(u) = a + \langle b, u\rangle$ for all $u \in \mathcal{U}_{\ell_0}$.
Then for any feedback policy $\pi$ respecting the same per-layer budget sets,
$\min_\pi J(\pi) = \min_{u \in \mathcal{U}_{\ell_0}} J_{\mathrm{open}}(u)$:
the optimal closed-loop cost equals the optimal open-loop cost.

*Proof sketch.* Under the affine assumption the terminal state is affine in the
injection, $s_L = p + Pu$. For the multi-layer affine case
$s_{\ell+1} = A_\ell s_\ell + u_\ell + c_\ell$ this is a deterministic LQ problem;
the optimal feedback law is $u_\ell = -K_\ell s_\ell + k_\ell$ (Riccati), and its
optimal cost coincides with the open-loop optimum: with zero noise the realized
trajectory under the optimal open-loop sequence equals the planned trajectory
exactly, so every feedback correction term evaluates to zero along the optimal path.
There is nothing to react to. ∎

**Corollary (the three licit benefit channels).** Feedback can beat open-loop only via:
- **(A) Nonlinearity correction** — reacting to realized nonlinear deviation of
  $F_\ell$ along the controlled path within a trajectory;
- **(B) Instance adaptivity** — scheduling gains per instance from early observations
  (the map $D_i$ varies across instances $i$; one open-loop $(v,\alpha)$ cannot be
  simultaneously optimal);
- **(C) Model-error replanning** — re-solving the open-loop problem from the measured
  state (MPC-style); observation helps even in deterministic systems because the
  internal model of $F_\ell$ is wrong.

**Excluded channel (D): layer distribution.** Spreading budget across layers is
achievable by a precomputed open-loop sequence. It is not a feedback benefit and must
be controlled for (arm (B) in §8), or any "CLLC win" may be misattributed.

## 4. Why S3-9 is CLLC's linearity diagnostic

S3-9 measures $g(\alpha) = \Delta M(\alpha)/\Delta M_{L1}(\alpha)$ over an $\alpha$
grid on the 8 rescued items — a **linearity diagnostic** for the ray-linearity
premise of the Theorem at L20. (Renamed from "premise verification": a finite
$\alpha$ grid cannot *prove* exact ray-linearity; it can only bound the observed
deviation from it.) Two branches:

- If $CV_\alpha[g] \le 20\%$ (near-linear): the Theorem approximately applies at
  L20, and same-layer feedback is predicted to add $\approx$ nothing over best
  open-loop. CLLC's remaining hope is channels (B)/(C)/(D) or a *different,
  nonlinear* layer (prediction P4).
- If $CV_\alpha[g] > 20\%$ (nonlinear): channel (A) is live, and feedback has
  room proportional to the measured curvature.

Either way S3-9 gates the quantitative use of the Theorem: P1's bound is only as
good as the diagnostic's grid.

## 5. Quantitative predictions with breaking points

- **P1 (linearity diagnostic, heuristic).** If S3-9 shows near-linearity, same-layer
  feedback gain over best open-loop is *heuristically* bounded by the measured
  nonlinearity: $\delta \lesssim \max_\alpha |g(\alpha) - \bar{g}|/\bar{g}$.
  This is a heuristic prediction, not a theorem-backed bound: a rigorous
  quantitative bound would require explicit approximation/Lipschitz/curvature
  assumptions on $D$, which are not derived here.
  *Breaking point:* a CLLC pilot showing $> 2\times$ that heuristic bound kills the
  channel analysis of §3 (the theory is wrong; keep the empirical result, rewrite
  the theory).
  *Update LOG-248:* derivation attempted — see
  `research/theory/P1_BOUND_DERIVATION_2026-09-24.md`. Verdict: theorem-backed
  conditional bound $0 \le \delta \le 2\varepsilon$ ($\delta \le \kappa R^2$)
  derived; numerical instantiation from S3-9 alone **proven impossible**
  (adversarial bump: exact ray-match to all orders, arbitrarily large $\delta$
  off-ray). P1 is now a theorem-backed conditional bound: operational breaking
  point is pilot (C)-arm gain $> \hat\kappa R^2$ **once** the priced curvature
  diagnostic (~150 passes ≈ 0.002 T4-h, queued behind K2) measures $\hat\kappa$.
  The heuristic above is retained only as order-of-magnitude intuition, not
  verdict-bearing.
- **P2 (authority collapse).** Performance vs. budget $\rho_{\max} \in \{0.5,1,2,4\}\times$
  natural Mahalanobis scale is $\cap$-shaped: rises to a peak at $1$–$2\times$, then
  collapses below the open-loop baseline at $4\times$ as injections move
  out-of-distribution relative to the fitted natural-activation distribution.
  *Breaking point:* monotone rise through $4\times$ falsifies the
  manifold-bounded-authority model (F4) — the constraint is softer than assumed,
  redesign the budget analysis.
- **P3 (observability saturation).** Feedback benefit saturates with probe rank $r$;
  predict saturation by $r \le 8$ on the 2-hop factual task (decision-relevant
  subspace is low-dimensional).
  *Breaking point:* $r = 1$ already saturates → drop the rank-$k$ machinery
  (simplify the design); no saturation by $r = 32$ → the task's decision subspace
  is higher-dimensional than assumed → revise (F3) analysis.
- **P4 (layer placement × nonlinearity).** Per-layer nonlinearity
  $\nu_\ell = |g_\ell(2\alpha) - g_\ell(\alpha)|/g_\ell(\alpha)$ (measurable in pilot
  calibration); CLLC benefit at layer $\ell$ is monotone in $\nu_\ell$.
  *Breaking point:* the best CLLC layer is the *most linear* one → the
  nonlinearity-benefit theory (channel A) is dead; only (B)/(C) survive.

## 6. Prior-art boundary (corrected)

The direct prior is **Activation-LQR** (Apr 2026). Correction to the previous draft,
which mischaracterized it as open-loop trajectory optimization: per our own
literature verification, Activation-LQR implements **closed-loop feedback control
of frozen activations using layer-wise Jacobians and online state feedback** —
model-based, per-step control under locally-linear dynamics.

Therefore **"feedback over activation steering" cannot be CLLC's novelty boundary**.
CLLC's possible contribution is narrower and testable: **a cheap, Jacobian-free,
partially observed, low-rank feedback controller that controls frozen-model
activations competitively with existing closed-loop controllers such as
Activation-LQR, while using less computational/model information** — no
Jacobian-vector products, no learned dynamics model, observation through a
low-rank probe bank.

The novelty-earning contrasts are (C)-vs-(B2) and (C)-vs-(D) in §8. If CLLC cannot
beat adaptive open-loop, or cannot match Activation-LQR at matched
information/compute, it contributes nothing beyond prior art and the pivot is
killed or re-scoped.

## 7. Controller design (cheapest instantiation)

Feedback law: $u_\ell = -k\,(m_\ell - m^*_\ell)\,\hat{v}$, where $m_\ell$ is the
scalar margin probe at layer $\ell$, $m^*_\ell$ a reference margin trajectory, and
$\hat{v}$ the S3-9/K2 direction. The scalar gain $k$ is tuned **on CPU from archived
$(\text{margin}, \text{injection})$ pairs** ($0, no GPU): line-search $k$ to maximize
predicted terminal margin under the ray-linear model, then verify in the pilot.
No Jacobian-vector products, no learned dynamics model — the cheapest controller
that can still test the feedback hypothesis. This Jacobian-free property is
precisely the narrowed novelty boundary of §6: it is the *entire* basis on which
CLLC can claim anything over Activation-LQR. (If it fails, upscale to MPC only with
a new Law #15 license.)

## 8. Pre-registration skeleton: EXP-CLLC-01 (DRAFT — for Law #14 review, not signed)

- **Trigger:** K2's P2 gate fires (final-position-local Supported) per
  DIRECTION_DECISION row 7. Number assigned at launch.
- **Arms** ($N = 60$ items each, Pythia-410m; layer from P4 calibration):
  - (A) best fixed open-loop single injection ($\hat{v}$, $\alpha^*$ from K2/S3-9);
  - (B) open-loop multi-layer precomputed sequence, budget-matched (isolates D);
  - (B2) adaptive open-loop: per-instance $\alpha_i$ from a pre-pass margin probe,
    two passes (cheap per-instance adaptivity — the hypothesis that must die first);
  - (C) CLLC Jacobian-free feedback (§7 law), scalar margin probe, budget-matched;
  - (C8) CLLC feedback, rank-8 probe (tests P3 observability saturation);
  - (D) actual Activation-LQR (layer-wise Jacobians, online state feedback),
    matched on budget as closely as its formulation permits — report any residual
    information/compute asymmetry explicitly rather than hiding it;
  - (E) **negative control:** feedback on *permuted* probe outputs (destroys
    observation information; must equal (A) at matched budget).
- **Budget matching:** $\sum_\ell \|u_\ell\|^2$ equalized across arms post-hoc by
  rescaling; report raw and matched. Information/compute asymmetry between (C)
  and (D) reported explicitly.
- **Endpoints:** primary — decision-flip rescue rate vs (A) (McNemar exact, Tango
  95% CI, program standard); secondary — $\Delta$ margin.
- **Critical comparisons:** (C) vs (B2) — does feedback add value beyond cheap
  per-instance adaptivity; (C) vs (D) — any advantage over existing closed-loop
  activation control. **(C) > (B) alone is insufficient** — (B) may simply be a
  weak baseline — and licenses no claim.
- **Pre-registered kill/continue criteria:**
  - (C) ≤ (A) at matched budget → **KILL** CLLC-as-feedback;
  - (C) > (B) but (C) ≤ (B2) → **KILL** feedback machinery — do not overclaim
    against weak open-loop baselines; CONTINUE adaptivity as open-loop;
  - (C) > (B2) but (C) < (D) → CONTINUE as an efficiency result *only* if (C)
    uses strictly less information/compute than (D); otherwise KILL the novelty
    claim (cheaper-but-weaker controller, not a contribution);
  - (C) ≥ (D) at matched information/compute → **meaningful control-method
    result**, CONTINUE to deeper investigation;
  - (B) > (A) with (C) = (B) → **PIVOT** to open-loop multi-layer;
  - (E) > (A) → **HALT**, budget-confound redesign, all feedback claims suspended.
- **Cost:** $7 \times 60 = 420$ passes $\approx 0.006$ T4-h; P4 calibration
  $\approx 800$ passes $\approx 0.005$ T4-h; **total $\approx 0.011$ T4-h**, $0.
- **Classification:** a successful CLLC result is classified as
  **"inference-time activation control"** — not evidence for autonomous cognitive
  discovery. Re-entry to the broader SCBI cognitive-control hypothesis requires a
  later experiment that removes the externally specified direction/reference
  (label-informed direction dependence is inherited, per the steelman).
- **Does not license:** any capability claim (forced baselines per Operating System
  §1 still required); any H-compliant verdict (K3's jurisdiction); any §H7 change;
  any autonomy/cognition claim.

## 9. Law #15 four answers (this formalization work)

1. **Precise question:** the revised core question of §0 — can a cheap,
   Jacobian-free, partially observed feedback controller beat optimized
   open-loop *and* adaptive open-loop at matched budget, and does it offer any
   advantage over existing closed-loop activation control such as
   Activation-LQR?
2. **Decision changed:** PIVOT — if the formalization holds, CLLC becomes a
   *registered* pivot battery deployable the instant P2 fires; if the Theorem's
   premises hold and no channel survives the steelman, CLLC-as-feedback is KILLED
   before one GPU pass is spent.
3. **Cheapest test:** this $0 CPU formalization now; empirical gates are S3-9
   (24–32 passes, already queued as K2 add-on) then EXP-CLLC-01 ($\approx 0.011$
   T4-h) only after P2 fires. No weights touched, no signed artifacts edited.
4. **Mathematical license:** deterministic optimal control — no-feedback-benefit
   theorem under ray-linearity (§3, proof sketch); full actuation $B_\ell = I_d$
   means direct actuation is not the injection-point bottleneck (not that
   reachability can never bind); binding constraints are (F3) partial
   observability and (F4) manifold-bounded authority; predictions P1–P4 each carry
   an explicit breaking point (P1 heuristic, pending Lipschitz/curvature
   assumptions for a theorem-backed bound).

## 10. Steelman: the strongest case against CLLC

1. **Determinism + adaptive open-loop.** The frozen pass is deterministic; the
   Theorem shows feedback's within-trajectory benefit needs nonlinearity. But
   per-instance adaptivity (channel B) needs no feedback law at all: a pre-pass
   probe plus per-instance gain is two forward passes and strictly simpler.
   If arm (B2) equals (C), the entire feedback apparatus is dead weight — this is
   the single most likely killer, and it is *cheaper* than CLLC.
2. **Compounding manifold risk.** Twenty layers of feedback is twenty chances to
   leave $\mathcal{M}_\ell$; the bridge's +10pp came from one careful injection.
   P2's $\cap$-shape may peak below the open-loop baseline everywhere.
3. **Budget dilution.** At matched total budget, spreading control across layers
   weakens per-layer authority; concentration at the best layer (open-loop) may
   dominate — in which case the "win" belongs to (A), not (C).
4. **Wrong missing ingredient.** Every static injection on the scoreboard is
   0.0pp; there is zero evidence that *adaptivity* — rather than direction quality
   or label-dependence — is what's missing. S3-8's ×1.8 amplifies a
   label-informed direction; CLLC does nothing to remove label-dependence, so even
   a CLLC "win" would inherit the Law #7 demotion.
5. **Novelty boundary corrected.** Activation-LQR is closed-loop feedback control
   with Jacobians, not open-loop optimization — so "feedback" was never available
   as CLLC's novelty. The honest claim is narrower: Jacobian-free,
   partially-observed, low-rank feedback at matched or lower information cost.
   Arm (D) exists to enforce exactly this comparison; if (C) < (D), CLLC is a
   cheaper-but-weaker controller, not a contribution.
6. **Complexity vs. the program's standard.** A closed-loop system is harder to
   make seeded, deterministic, and testable to the 84/84 bar; mid-pass misbehavior
   is strictly harder to debug than a static vector.

*Net of the steelman:* the honest ordering is (B2) before (C) — adaptive open-loop
is the cheaper hypothesis that must die first — and (D) alongside (C), because the
existing closed-loop controller is the bar, not open-loop. §8 is built in that
order.

## 11. What this licenses

Licenses: the CLLC pivot battery as a *designed, pre-registered-ready* instrument;
S3-9's status as the linearity diagnostic (not a proof of ray-linearity); the
(C)-vs-(B2) and (C)-vs-(D) contrasts as the novelty-earning experiments vs
adaptive open-loop and Activation-LQR respectively.
Does not license: any GPU execution, any claim that CLLC works, any capability or
H-level claim, any change to §H7 or the K2/K3 queues, any autonomy/cognition claim.
A successful CLLC result is "inference-time activation control" unless and until a
later experiment removes the externally specified direction. P2 has not fired;
CLLC remains a bet, now a priced and honestly bounded one.
