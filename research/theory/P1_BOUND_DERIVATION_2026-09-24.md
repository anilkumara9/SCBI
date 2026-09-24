# P1 Bound Derivation — Theorem-Backed Quantitative Bound for the Feedback-vs-Open-Loop Gap

*Theory note, 2026-09-24 (LOG-248). CPU only, $0. Not a signed protocol.
Requested by the reviewer in the LOG-247 corrections: "If you want a theorem-backed
quantitative bound, derive it from explicit approximation/Lipschitz/curvature
assumptions."*

## 0. Verdict up front

**Partial success — the valuable kind.** The bound's *form* is now theorem-backed
with explicit assumptions: for the practical feedback-vs-open-loop gap
$\delta$, we prove $0 \le \delta \le 2\varepsilon$ where $\varepsilon$ is the
sup-norm affine-approximation error of the downstream map over the joint budget
set, and $\delta \le \kappa R^2$ under a $\kappa$-bounded Hessian. **But the
numerical instantiation of this bound from S3-9 alone is impossible, for a proven
reason:** S3-9's 1-D $\alpha$-grid cannot identify $\varepsilon$ or $\kappa$ off
the measured ray (explicit counterexample in §5). P1 is therefore upgraded from
"heuristic prediction" to **"theorem-backed conditional bound with a specified
missing measurement"** — and the missing measurement (a curvature diagnostic,
~150 passes, §6) is now priced. A clean impossibility of identification is
recorded instead of a hand-waved number.

## 1. Setup and notation

Fix an instance $x$. Let the joint injection vector be
$\vec u = (u_0,\dots,u_{L-1})$, $u_\ell \in \mathbb{R}^d$, and let
$D(\vec u) = \varphi(s_L(\vec u))$ be the downstream objective (negative margin)
under the frozen deterministic plant. [DEFINITION]

- **Joint budget set** [ASSUMPTION A2]: $U = \times_\ell \mathcal{U}_\ell$,
  $\mathcal{U}_\ell = \{u : \|u\|_{\Sigma_\ell} \le R_\ell\}$ (Mahalanobis balls),
  with joint radius $R^2 = \sum_\ell R_\ell^2$ in the whitened norm $\|\cdot\|_\Sigma$.
- **Affine model** $\bar D(\vec u) = a + \langle b, \vec u\rangle$; approximation
  error [DEFINITION]: $\varepsilon = \sup_{\vec u \in U} |D(\vec u) - \bar D(\vec u)|$.
- **Affine-based open-loop** [DEFINITION]: $\bar u = \arg\min_{\vec u \in U}
  [\bar D(\vec u) + \lambda\|\vec u\|_\Sigma^2]$, cost
  $J_{\mathrm{ob}} = D(\bar u) + \lambda\|\bar u\|_\Sigma^2$.
  (This is what a planner that believes the S3-9 affine fit would actually do.)
- **Feedback optimum** [DEFINITION]: $J^*_{\mathrm{fb}} = \min_\pi J_{\mathrm{true}}(\pi)$
  over all feedback policies $\pi$ under the true plant.
- **Practical gap** [DEFINITION]: $\delta = J_{\mathrm{ob}} - J^*_{\mathrm{fb}}$.
  This is the quantity P1 must bound: how much the best feedback can beat the
  open-loop injection designed from the affine premise.

Regularity [ASSUMPTION A1]: $D$ is $C^2$ on $U$ (transformer blocks compose smooth
maps — GELU/SiLU, softmax — and LayerNorm is smooth away from the degenerate
zero-variance set, which real LM activations avoid; the degenerate case is
excluded), with $\kappa := \sup_{\vec u \in U} \|\nabla^2 D(\vec u)\|_{\Sigma,\mathrm{op}} < \infty$.

Determinism [ASSUMPTION A3 = LOG-246 F2]: the frozen plant is deterministic, so
for a fixed instance every policy $\pi$ realizes to a fixed injection vector
$\vec u(\pi) \in U$. (Consequence: with *known* $D$, feedback $\equiv$ open-loop
exactly — the only licit feedback benefit is against *model error*, i.e. channels
(A)/(C) of LOG-246 §3.)

## 2. Theorem 1 — feedback benefit bounded by affine-model error

**[THEOREM].** Under A1–A3, let $\bar D$ be any affine model with sup-error
$\varepsilon$ on $U$. Then $0 \le \delta \le 2\varepsilon$.

*Proof sketch.* For any policy $\pi$,
$|J_{\mathrm{true}}(\pi) - J_{\mathrm{affine}}(\pi)|
 = |D(\vec u(\pi)) - \bar D(\vec u(\pi))| \le \varepsilon$,
since the $\lambda\|\cdot\|^2$ regularizer is known exactly. Hence:
(i) $J_{\mathrm{ob}} = J_{\mathrm{true}}(\mathrm{const}_{\bar u})
   \le J_{\mathrm{affine}}(\mathrm{const}_{\bar u}) + \varepsilon
   = J^*_{\mathrm{open}}(\mathrm{affine}) + \varepsilon$;
(ii) $J^*_{\mathrm{fb}}(\mathrm{true}) = J_{\mathrm{true}}(\pi^*)
   \ge J_{\mathrm{affine}}(\pi^*) - \varepsilon
   \ge J^*_{\mathrm{fb}}(\mathrm{affine}) - \varepsilon
   = J^*_{\mathrm{open}}(\mathrm{affine}) - \varepsilon$,
   where the last equality is the LOG-246 §3 ray-linearity theorem (exact-affine
   case: optimal feedback cost equals optimal open-loop cost under deterministic
   affine dynamics — certainty equivalence at zero noise).
Subtracting: $\delta \le 2\varepsilon$. The lower bound $\delta \ge 0$ holds
because feedback policies include constants:
$J^*_{\mathrm{fb}}(\mathrm{true}) \le J_{\mathrm{true}}(\mathrm{const}_{\bar u}) = J_{\mathrm{ob}}$. ∎

## 3. Corollary — curvature form

**[COROLLARY].** Under A1–A3 with Hessian bound $\kappa$ on $U$,
$0 \le \delta \le \kappa R^2$.

*Proof sketch.* Taylor with integral remainder:
$D(\vec u) = D(0) + \langle \nabla D(0), \vec u\rangle
 + \int_0^1 (1-t)\,\langle \vec u, \nabla^2 D(t\vec u)\,\vec u\rangle\,dt$,
so $|\mathrm{remainder}| \le \tfrac{\kappa}{2}\|\vec u\|_\Sigma^2 \le \kappa R^2/2$.
The first-order Taylor polynomial is an affine model with
$\varepsilon \le \kappa R^2/2$ (the best affine fit does at least as well);
Theorem 1 gives $\delta \le 2\varepsilon \le \kappa R^2$. ∎

**Reading:** the bound tightens *quadratically* as the budget shrinks — for small
$R$ it is a strong certificate that feedback cannot beat open-loop by much; for
large $R$ it loosens and eventually goes vacuous (§7).

## 4. What S3-9 actually measures

S3-9 measures $g(\alpha) = \Delta M(\alpha)/\Delta M_{L1}(\alpha)$ on an $\alpha$-grid
(single layer L20, fixed direction $\hat v$). Define the effective injection
$t = \Delta M_{L1}(\alpha)$ and $\tilde d(t) = \Delta M(t) = D(t\hat v)$ in margin
units. [ASSUMPTION A4]: $t$ is monotone in $\alpha$ on the grid (directly checkable
from the data when it lands).

[OBSERVATION-to-be]: if $\mathrm{CV}_\alpha[g] \le 20\%$, then
$|\tilde d(t) - \bar c t| \lesssim 0.2\,|\bar c t|$, i.e. the affine-fit error
**on the ray** satisfies $\varepsilon_{\mathrm{ray}} \lesssim 0.2 \cdot \max_t |\tilde d(t)|$.

**The gap:** $\varepsilon_{\mathrm{ray}}$ bounds the fit error on the 1-D set
$\{\alpha\hat v\}$; Theorem 1 needs $\varepsilon = \sup_U |D - \bar D|$ over the
full joint budget set (all layers, all directions). The step from ray to volume
is where identification dies (§5).

## 5. Proposition — S3-9 cannot identify $\varepsilon$ or $\kappa$ (impossibility)

**[PROPOSITION].** For *any* S3-9 outcome (any grid, any resolution), there exist
downstream maps $D_1, D_2$ agreeing *exactly* on the measured ray with
$\delta(D_1) = 0$ and $\delta(D_2) \ge M$ for arbitrary $M > 0$.

*Proof sketch (adversarial bump construction).* Take $D_1(\vec u) = \langle b, \vec u\rangle$
with $b = \beta\hat v$ (affine; $\varepsilon = 0$, $\delta = 0$ by Theorem 1).
Let $w \perp \hat v$, $\|w\|_\Sigma = 1$, and
$D_2(\vec u) = \langle b, \vec u\rangle + M\,\sigma(\langle w, \vec u\rangle)$,
where $\sigma$ is a smooth bump with $\sigma(0) = \sigma'(0) = 0$, $\sup\sigma = 1$,
supported inside the budget set. On the S3-9 ray $\{\alpha\hat v\}$,
$\langle w, \alpha\hat v\rangle = 0$, so $D_2 \equiv D_1$ there **to all orders** —
no finite (indeed, no infinite) $\alpha$-grid distinguishes them.
With $b = \beta\hat v$, the affine optimum $\bar u$ lies on the ray; place the
bump centered at $\langle w,\cdot\rangle = \langle w, \bar u\rangle$... in fact
place it at $t^* = \langle w, \bar u\rangle$ (adversarial placement after seeing
$\bar u$ — the diagnostic cannot rule this out). Then
$J_{\mathrm{ob}}(D_2) = \bar D(\bar u) + \lambda\|\bar u\|^2 + M$, while
$J^*_{\mathrm{fb}}(D_2) \le \min_{\text{ray}}[D_2 + \lambda\|\cdot\|^2]
 = \min_{\text{ray}}[\bar D + \lambda\|\cdot\|^2] = \bar D(\bar u) + \lambda\|\bar u\|^2$
(a constant ray policy avoids the bump entirely, and feedback can do at least
this well). Hence $\delta(D_2) \ge M$, with $M$ arbitrary. ∎

**Consequence:** no finite bound on $\delta$ is derivable from S3-9 observables
alone. Any numerical P1 bound must import a *global* curvature/approximation
assumption over $U$ from outside S3-9. The conjecture
"[CONJECTURE] ray-representative error: $\sup_U|D-\bar D| \le C\,\varepsilon_{\mathrm{ray}}$"
would license $\delta \le 2C\varepsilon_{\mathrm{ray}}$, but it is untestable from
S3-9 and **must not ground a verdict**.

## 6. The missing measurement (now priced)

What would instantiate the bound: an upper bound on $\kappa$ over the injection
* schedule space* (the §7 controller injects only along $\hat v$ per layer, so
$\kappa$ is needed over the $L$-dimensional schedule space, $\approx 24$-D for
Pythia-410m — not full activation space).

**Proposed curvature diagnostic:** randomized power iteration on $\nabla^2 D$ via
central finite differences,
$v^\top H v \approx [D(hv) - 2D(0) + D(-hv)]/h^2$ (3 forward passes per matvec),
$\sim$15–25 iterations $\approx$ 45–75 passes, plus $\sim$60 calibration passes
for the Mahalanobis whiteners $\Sigma_\ell$ (no activation archives exist per
LOG-243, so these must be measured live). **Total $\approx$ 150 passes
$\approx$ 0.002 T4-h**, GPU-gated, queued behind K2 per §H6.

**Honesty caveats** [ASSUMPTION]: power iteration estimates the top eigenvalue
*at the nominal point*; a sup-bound over $U$ needs a covering argument or the
stated assumption that curvature does not spike off-nominal. Finite-difference
error and iteration truncation make $\hat\kappa$ [CONJECTURE]-grade until
cross-validated. The operational bound $\delta \le \hat\kappa R^2$ inherits these
caveats — it is a *working* breaking point, not a theorem-grade certificate.

## 7. Revised P1 statement and operational breaking point

**P1 (theorem-backed conditional bound).** *If* S3-9's diagnostic shows
near-ray-linearity **and** a curvature diagnostic supplies $\hat\kappa$ over the
schedule space, *then* same-layer/multi-layer feedback gain over best open-loop
satisfies $\delta \le \hat\kappa R^2$ (Corollary), respectively $\delta \le 2\hat\varepsilon$
under a measured sup-error. **Breaking point:** a pilot (C)-arm feedback gain
exceeding the instantiated bound kills the §3 channel analysis (the theory is
wrong; keep the empirical result, rewrite the theory). Until $\hat\kappa$ is
measured, P1 remains conditional — the heuristic
$\delta \lesssim \max_\alpha|g(\alpha)-\bar g|/\bar g$ is retained only as an
order-of-magnitude intuition, explicitly not verdict-bearing.

## 8. Law #15 four answers (this theory work)

1. **Precise question:** can P1's heuristic bound be replaced by a theorem-backed
   quantitative bound on the feedback-vs-open-loop gap, and what must be measured
   to instantiate it numerically?
2. **Decision changed:** CONTINUE — P1's *form* is upgraded to theorem-backed
   ($\delta \le 2\varepsilon$, $\delta \le \kappa R^2$) and the missing
   measurement is specified and priced (~150 passes); the alternative
   (KEEP-HEURISTIC) would have left the reviewer's challenge unanswered. Either
   branch was a result; the derivation succeeding conditionally is the better one.
3. **Cheapest test:** this $0 CPU derivation now; the curvature diagnostic
   (~0.002 T4-h) only after K2, GPU-gated. No weights touched, no signed artifacts
   edited.
4. **Mathematical license:** deterministic optimal-control perturbation theory —
   the $2\varepsilon$ sandwich is standard approximate-dynamic-programming
   reasoning; the curvature corollary is Taylor with integral remainder; the
   impossibility is an explicit adversarial construction. Breaking point: pilot
   gain $> \hat\kappa R^2$ kills the channel analysis.

## 9. Steelman — where the bound is vacuous or misleading

1. **Huge $\kappa$.** Attention softmax can have enormous curvature; if measured
   $\hat\kappa R^2$ dwarfs the effect size (the ×1.8 margin-gain scale), the bound
   is vacuous at operational budgets. It bites only when $\hat\kappa R^2$ is
   comparable to or smaller than the effect size — most plausibly at small $R$,
   where it tightens quadratically.
2. **Upper bound only.** $\delta \le 2\varepsilon$ says feedback *cannot win big*;
   it never says feedback *achieves* anything. A tiny $\varepsilon$ is a
   certificate of feedback-futility, not of open-loop success.
3. **Optimal-policy vs specific-law gap.** The theorem bounds the *optimal*
   feedback policy; EXP-CLLC-01's (C) arm is one scalar law. If (C) underperforms
   the bound, the law is weak — the bound is not falsified. Only a (C)-arm gain
   *above* the bound kills the channel analysis.
4. **Smoothness caveat.** A1 excludes the LayerNorm degenerate set; if the
   controlled trajectory approaches it, $\kappa$ is not defined there and the
   corollary fails silently — the diagnostic should monitor activation norms.
5. **Conservative domain.** $\varepsilon$/$\kappa$ range over all of $U$, but the
   §7 controller only explores $\hat v$-schedules; the bound is conservative for
   the actual controller. Tightening to schedule-space is recorded as future work,
   not claimed here.

## 10. What this licenses

Licenses: P1's upgraded statement (§7) as the program's quantitative feedback-futility
criterion; the curvature diagnostic as a priced, queued measurement (behind K2);
S3-9's continued role as the *ray* diagnostic (necessary, not sufficient).
Does not license: any numerical breaking point before $\hat\kappa$ is measured;
any verdict grounded in the ray-representative conjecture; any GPU execution;
any CLLC efficacy or capability claim.
