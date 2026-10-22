# Independent Law #14 Review — EXP129 (CLP) Pre-registration Draft

**Lane:** LOG-4712 (pre-assigned). **$0 CPU.** Review only — no execution
licensed, no signed artifact modified, no GPU contact, nothing pushed,
spent, or credential-touched.

**Verdict: SIGN-WITH-FIXES.** The pre-registration is launchable after the
numbered fixes below. The dossier's channel-vs-dose tripwire does **not**
fire: the protocol's feedback construct genuinely discriminates adaptation
from dose (ruling in §2). Two fixes are launch-gating (verdict-material in
corner cases); five are verdict-immaterial protocol hygiene. No REJECT.

**Artifact under review:**
`research/prereg/EXP_PREREG_CLP_ADAPTIVEPURSUIT_2026-09-29.md`
— sha256 verified before review:
`f03804d2879cfd8b4d2393fbb986e3f0fe90ae4188658b6b88cbb644a47919eb`
(matches the lane brief; no lane defect).

**Read:** the protocol (full), `research/strategy/CLP_GATE_2026-09-29.md`
(LOG-4710, PASS conditional), `research/experiments/EXP127_TGA_TRANSIENTGROWTH_REPORT_2026-09-29.md`
(cited numbers re-verified: median R = 8.240640, σ₁/σ₂ = 1.557689 —
match the protocol's citations), `research/experiments/EXP128_DSF_SENSITIVITYFIELD_REPORT_2026-09-29.md`
(1/12 within 25% at ε=1e-3 — the killed apparatus).

---

## 1. The four launch conditions — protocol-level status

| # | Gate condition | Protocol spec | Status |
|---|---|---|---|
| 1 | Norm-matched controls + adaptation≠dose proof | §3.4 three arms (closed-loop 2-step / open-loop 2-step sum with pinned v̂₂ / single shot), all at component-norm budget B; norm audit per (item, arm); breaking point (b) → apparatus-void on any budget miss | **PASS**, with FIX-4 (audit granularity) |
| 2 | EXP128 constraint — killed finite-difference sensing absent | §3.5 + breaking point (c): exact-JVP/adjoint sensing via autograd (EXP127's Law-#14-licensed instrument); executor asserts *absence* of any finite-difference sensing term; grep confirms no `‖g(y+δ)−g(y)‖/‖δ‖`-as-sensing-input anywhere in the protocol text | **PASS**, with FIX-3 (whitelist/blacklist the assert) |
| 3 | Dynamics-sensed directions only | §3.3: v̂₁/v̂₂ re-pinned from EXP127's run dir; "No semantic, task, or concept direction enters this protocol" | **PASS**, with FIX-5 (record expected artifact hashes + per-prompt id alignment) |
| 4 | Correction rule frozen, no per-item tuning | §3.5 closed form ŵ = Mᵀd̂₁/‖Mᵀd̂₁‖, identical for all items; breaking point (d) → apparatus-void on any per-item modification | **PASS** |

All four conditions are protocol-level specs, not informal assertions.
The dose-fence is mechanical: the closed-loop arm injects δ₂ = δ₁ + c
with ‖δ₂‖ ≤ B by triangle inequality while the single-shot arm injects
exactly B — the loop can never win on dose, so a ≥2 ratio cannot be
read as "a bigger push." The open-loop sum arm (pinned v̂₂, the
strongest dynamics-licensed "second push") is the honest control the
gate demanded.

---

## 2. The channel-vs-dose tripwire — RULING: does not fire

This is the review's core adversarial test, and I steel-manned the
REJECT case before ruling.

**Steel-man for REJECT (adaptation = dose):** In a deterministic model,
the closed-loop arm is a deterministic function of (item, pre-registered
rule): M is measurable without feedback (it is EXP127's apparatus),
δ₁ is pre-registered, and d₁ = g(y+δ₁) − g(y) is a deterministic
function of (item, δ₁). The "feedback" ŵ = Mᵀd̂₁/‖Mᵀd̂₁‖ is therefore
pre-computable in the linear limit (ŵ ≈ MᵀMδ₁/‖MᵀMδ₁‖) — a notational
re-description of a 2-step open-loop sequence with a clever second
direction. The experiment would then compare two 2-step open-loop
sequences (adjoint second direction vs v̂₂ second direction): a
*geometry* comparison wearing feedback's name. The "feedback gain"
would really be "adjoint-direction gain," and the construct "feedback
has causal value" would be unsupported — the design cannot isolate
feedback from direction choice, because the feedback direction is
confounded with "a better second direction." Rule adaptation = dose
(or rather, adaptation = geometry), never launch.

**Why the steel-man fails here:**

(a) The feedback signal is the *measured nonlinear* response direction
d̂₁, not its linear prediction. EXP128 established that at the
relevant scale the map is *not* locally linear (1/12 within 25%) —
so d₁ carries information about the nonlinear response that Mδ₁
does not contain. The deviation from linearity IS the feedback
signal. In the linear limit the steel-man would be correct; the
protocol operates outside that limit by EXP128's own finding.

(b) The norm-matching makes the dose reading mechanically impossible:
all arms spend the same component-norm budget, and the loop arm
injects ≤ the single-shot arm's norm. A ≥2 ratio is an efficiency
statement, not a dose statement.

(c) The protocol contains its own tripwire as a registered KILL
branch: median ‖d₂‖/‖d_sum‖ ≤ 1.2 → "dose in disguise" KILL, which
fires exactly when the feedback reduces to a second pre-computed
push. The design tests the reduction rather than assuming it away.
(Verified: this branch is mutually exclusive with the CONTINUE bar
by construction — ‖d₂‖ ≥ 2·max(‖d_sum‖,‖d_single‖) implies
‖d₂‖/‖d_sum‖ ≥ 2 > 1.2 — so no precedence ambiguity there.)

(d) The counterfactual structure differs in the only sense that
matters operationally: the executor *cannot compute ŵ without
running the measurement forward*. An open-loop executor skips the
sense step; this one cannot.

**Ruling:** adaptation ≠ dose as a construct. The norm-matched
per-norm ratio discriminates feedback gain from dose, and the
dose-in-disguise branch polices the boundary. The family may launch
(subject to fixes). Law #14's pre-launch tripwire is satisfied, not
triggered.

---

## 3. Law #9 ordering — executable

§5 tree: guards → backbone pin → forward batches → validity-check
evaluation (norm-budget audit + sensing-discipline assert +
correction-rule pin) → raw-record hash-pin → displacement metric →
decision. Checked against the LOG-4704 defect class (a check
reusing a quantity it claimed to precede):

- The norm-budget audit reads ‖δ‖ values produced by the forwards —
audit-after-forwards is executable, no circularity.
- The correction-rule check recomputes ŵ from the raw-record d₁
vectors and the adjoint diagnostics (§3.8 requires both pinned) —
a post-hoc code-vs-formula audit, executable.
- The hash-pin precedes the metric; the metric reads only pinned
records. Nothing in the checks depends on the decision statistic.
- The loop arm's internal sense→act sequence is fixed by §3.4 text
("forward again with δ₂ … fresh forward from the unperturbed
base"); FIX-7 asks the §5 parenthetical to say so explicitly.

**PASS** with FIX-7 (wording).

---

## 4. Non-resurrection audit

Constraining kills named and checked: EXP077 (semantic cone kills at
L20, ΔM=0), EXP093 (shared-direction inertness), EXP094 (120 L11
semantic arms, zero flips), S5-2 (4.87% per-arm bound — *decision
effects along semantic/static directions*; CLP's metric is residual
*displacement* along *dynamics-sensed* directions, with flips held
as [OBSERVATION] only, so the bound is unengaged), EXP095 (dose —
fenced mechanically by (b)), EXP096/097 (saturation — a registered
KILL branch here, not a confound), G1 (QK-subspace mechanism
account, not a feedback channel), EXP115/116/123 (generation
channel — CLP never generates, decodes, or reads content), EXP125
(H22), EXP126 (H23), the LOG-4693 static-snapshot paradigm death.

The directions (v̂₁/v̂₂ from EXP127, CONTINUE'd and bound) are a new
direction class under Law #4 — the model's own maximally-amplified
directions, never semantic — and the feedback-gain discriminant was
measured by no dead lane. This is not EXP077/EXP094 with a bolt-on:
those lanes had semantic directions + no norm control; this protocol
has dynamics-sensed directions + mechanical norm control + the
dose-in-disguise KILL branch. **PASS** — no resurrection.

---

## 5. EXP128 non-transfer — verified

EXP128 killed a *sensing instrument*: the finite-difference gain
ratio ‖Δx‖/‖δ‖ as an estimator of the propagator norm at ε=1e-3
(1/12 within 25%, bar ≥10/12). CLP uses no such estimator:

- Sensing is exact-JVP/adjoint via autograd (EXP127's licensed
apparatus). Grep of the protocol confirms: no finite-difference
gain ratio appears as a sensing input; §3.5 and §3.7 and breaking
point (c) bar it explicitly, with apparatus-void on violation.
- The measured displacement d₁ is used as a *direction* (d̂₁),
never as a linearity claim or a norm estimate. The "maximally
amplifies" reading of ŵ = Mᵀd̂₁/‖Mᵀd̂₁‖ is exact linear algebra
*on M* (it maximizes ⟨d̂₁, Mw⟩ over unit w by Cauchy–Schwarz) —
a claim about the Jacobian, not about g. No linear-regime
assumption about the residual map is invoked, consistent with
EXP128's finding.
- The protocol does not need DSF's field: the loop senses its own
response. DSF stays UNTESTED; CLP assumes nothing about it.

**PASS** — EXP128's failure does not transfer, because its
apparatus is absent from this protocol. FIX-3 sharpens the
executor assert so this stays true at execution.

---

## 6. Honest frame — verified

§7 honest frame verbatim (control-efficiency, not capability;
scoreboard stays at zero; KILL as adverse evidence against the GPU
closed-loop line without unlicensing signed bundles; no injection
here is autonomous steering). §8 "does NOT claim" list is complete
and correct (not a capability, not generality, not a mechanism
account, not a resurrection; novelty N1 — Known Combination).
Flips are [OBSERVATION] only with the EXP094 zero-flip-floor
justification. No steering/consciousness claim anywhere.
**PASS.**

---

## Fixes

### Launch-gating (fix before launch — verdict-material)

**FIX-1 — Pin the verdict-branch precedence (§4/§5).** The
saturation KILL branch (median ‖d₂−d₁‖/‖d₁‖ ≤ 0.1) and the
CONTINUE bar (median r ≥ 2) can co-fire in the corner where the
first push alone dominates: if ‖d₁‖ ≥ 2× the best open-loop arm
while the correction buys nothing (d₂ ≈ d₁), both the ≥2 ratio
and the ≤0.1 saturation statistic hold — opposite verdicts, no
stated precedence. Required: state the evaluation precedence
explicitly in §4 and the §5 tree. Recommended: the saturation and
dose-in-disguise KILL branches are evaluated first (they test the
family premise — "feedback bought displacement" — directly; a
procedure that wins on the first push alone does not license the
feedback premise); the ratio bars apply only if neither fires.
Any explicit precedence with justification is acceptable; silence
is not.

**FIX-2 — Pin the budget magnitude B (§3.3).** "Budget B —
pinned absolute norm … (executor-pinned; identical across all
arms, items, and draws)" gives B no numerical value or scale.
The bars are scale-free, but the *saturation branch is
scale-sensitive* and the executor's choice of B is a degree of
freedom that moves the outcome (B ≫ residual norm forces the
saturation KILL; B → 0 forces noise) — a Law #4 design
under-specification the gate's "pinned, §3.3" did not license.
Required: state B's numerical value (or a narrow range tied to
the L20 residual-norm scale / EXP127's perturbation scale) in
the pre-reg, with the executor asserting the chosen B *before*
the first forward and breaking point (b) auditing it.

### Verdict-immaterial (protocol hygiene — checkable)

**FIX-3 — Sharpen the sensing-discipline assert (§3.5, breaking
point (c), §5 tree).** The assert bars "any finite-difference
sensing term" but the feedback signal d₁ *is* a finite
displacement. Required: enumerate allowed vs barred uses —
WHITELIST the finite-displacement *direction* d̂₁ as the feedback
input; BLACKLIST any finite-difference *gain ratio* ‖Δ‖/‖δ‖ used
as an amplification estimate. This makes the executor assert
mechanically checkable (grep-able) and prevents executor drift.

**FIX-4 — Norm-audit granularity (§3.4, breaking point (b)).**
§0(b) says "the executor audits ‖δ‖ per arm per item," but the
loop arm's injected perturbation is δ₂ = δ₁ + c with
‖δ₂‖ ≤ B by triangle inequality while the budget is pinned on
the *components* (‖δ₁‖ = ‖c‖ = B/2). Required: audit both the
injected norm per arm (‖δ₂‖, ‖δ₁+δ_open‖, ‖δ_single‖) *and* the
component structure, and key breaking point (b) explicitly to
the component structure (‖δ₁‖=‖c‖=‖δ_open‖=B/2, ‖δ_single‖=B,
within float32 tolerance). "Every arm spends exactly B" is
ambiguous for the loop arm as written.

**FIX-5 — v̂ artifact re-pin (§3.3, §5 tree).** "Hash re-pinned
by the executor before the first forward" does not record the
*expected* hashes. Required: record the expected SHA-256 of the
EXP127 v̂₁/v̂₂ artifact files in the pre-reg (they are fixed
post-hoc artifacts), and require the re-pin step to verify
per-prompt id alignment between the artifact and the 10-item
decision set — matching a directory hash is not alignment.

**FIX-6 — Forward-count arithmetic (§3.6).** "10 items × 3 arms
× 2 forwards = 60 forwards" overcounts the estimator-required
forwards: per item the arms need 1 base + 2 loop + 1 sum + 1
single = 5 forwards → 50 forwards, plus ~10 VJPs for the adjoint
sensing. Required: correct the count (or state 60 as an explicit
upper bound). Documentation-only; same defect class as the DSF
review's cost-formula caveat.

**FIX-7 — Loop-arm sequentiality in the tree (§5).** "Forward
batches (all arms, any batch order)" could be misread as
licensing intra-arm reordering. Required: state that batch order
is free across items/arms but the loop arm's sense→act sequence
(forward-1 → measure d₁ → compute c → forward-2 from the
unperturbed base) is fixed.

### Caveats (review record — no fix required)

- **C1.** The §3.5 fallback (‖Mᵀd̂₁‖ = 0 → ŵ = v̂₁, item flagged
not dropped) biases that item's ratio toward KILL by construction
(the loop arm then equals the single-shot arm). Conservative and
disclosed; no change required — but the execution report must
tabulate fallback flags per item.
- **C2.** d₁'s *direction* is the feedback signal; if EXP128's
threshold intuition holds strongly (response direction dominated
by saturation structure rather than by δ₁), the loop may find
ŵ ≈ constant across items — that outcome is measurable inside
the protocol (it would surface in the saturation branch and the
per-item r_i spread), not a design flaw.

---

## Ruling summary

- Channel-vs-dose: **adaptation ≠ dose** — the tripwire does not
fire; the family may launch.
- Law #9 ordering: executable; no LOG-4704-class defect.
- Non-resurrection: clean — dynamics-sensed directions, new
discriminant, no killed lane touched.
- EXP128 non-transfer: verified — the killed apparatus is absent.
- Honest frame: verified verbatim.
- **SIGN-WITH-FIXES**: FIX-1 and FIX-2 before launch; FIX-3
through FIX-7 checkable at fix-verification. Then: fix-verification
→ CEO launch decision → execution under EXP129.

*Reviewer: independent Law #14 lane, LOG-4712. Fresh eyes; no role
in the gate, draft, or any execution lane.*
