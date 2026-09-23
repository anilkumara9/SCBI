# EXP070 Protocol Specification: Oracle-Selection Ceiling — Verifier-First, Generator-Second

**Status:** PRE-REGISTERED (protocol; not yet executed)
**Date:** 2026-09-23
**Author role:** Preregistration Agent
**Predecessor experiments:** EXP063–EXP068 (boundary series; EXP067/068 pre-registered, unexecuted)
**Source idea:** `research/innovation/SPRINT_2026-09-23.md` Idea 2 (CEO green-lit as the highest-leverage sequencing move)
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `STATISTICAL_PROTOCOL_V02.md`,
`theory/LOOP_SPEC_DRAFT.md` (signed — the loop this pre-test gates), `theory/BOUNDARY_CLAIM_FORMALIZATION.md`,
`research/literature/audit_2026-09-23.md` (N1 verdict)
**Execution rule:** Strictly confirmatory. No pool, probe, selection-rule, or threshold changes after
execution begins without a new pre-registration. **Changed design = the next free number at
pre-registration time.**
(Numbering note: the EXP068 draft's "changed design = EXP069" predates the innovation sprint's
numbering, which assigns EXP069 to Idea 1 (compositional factorization); this spec follows the
sprint: EXP070 = oracle ceiling. Consequence: the sprint's provisional EXP071 assignment (Idea 3,
target-free steerability diagnostic) is vacated — if Idea 3 advances, it takes the next free number
at pre-registration time, as does any changed design under EXP070 and the §9 410m replication.
No number is pre-claimed here.)

---

## 1. Research question and hypotheses

$$\boxed{\textbf{Can \textit{any} per-instance selection over the loop's candidate pool —
even with an oracle's label access — beat static CAA-equivalent injection?}}$$

**[HYPOTHESIS] H_ceiling:** Label-informed per-instance selection (the oracle) over the candidate
pool the EXP068 loop would search yields $\Delta M_{\mathrm{oracle}} > \Delta M_{\mathrm{static}}$
(McNemar exact $p < 0.05$ on the paired oracle-vs-static decisions) on the headroom-calibrated
benchmark — i.e., there exists a per-instance selection prize worth chasing.

**Null $H_0$:** $\Delta M_{\mathrm{oracle}} \le \Delta M_{\mathrm{static}}$ ($p \ge 0.05$) — even the
oracle cannot beat static injection; the loop's build-justification is withdrawn without building
it (see §1.2 for the exact license — justification-withdrawal, not falsification of the adaptive
loop hypothesis, which EXP070 never tests).

### 1.1 Scope of this experiment (methodology pre-test, not a method)

[INTERPRETATION] EXP070 is a **kill-the-loop pre-test**, not a proposed method and not a novelty
experiment. Its research question inverts the field's build order for test-time compute:
**verifier-first, generator-second.** Before spending ~116k forward passes building the EXP068
$\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop, measure the maximum achievable gain of
*any* selection procedure over the loop's candidate pool. The logic is a ceiling argument:

- If **even oracle selection cannot beat static injection** (and the probe-signal gate of §8
  confirms the ceiling was measured rather than merely unmeasured), no realizable target-free
  evaluator selecting over the same pool can justify the loop's cost → the build-justification
  for the loop is withdrawn; EXP068 is cancelled in its current form before it is built
  (see §1.2 — this withdraws justification; it does not falsify the adaptive loop hypothesis,
  which is never tested here).
- If **oracle selection wins decisively**, the gap between oracle and static quantifies exactly
  how much verifier quality is worth — turning "build a better evaluator" from a hope into a
  measured prize; EXP068 is justified (not validated).

The oracle's label access is **permitted** (sprint Idea 2): this is a ceiling *measurement*, not a
proposed method. Law #7's test-time information boundary applies to the EXP068 loop, not to this
diagnostic. The anti-cheat clause (§3.5) is what keeps the ceiling honest.

### 1.2 Logical structure: what each outcome licenses and does NOT license

| Outcome | LICENSES | DOES NOT LICENSE |
|---|---|---|
| **No significant oracle gain with probe signal** (branch (c1)): no statistically significant C3-vs-C2 gain ($p \ge 0.05$), probe-signal gate passed (§8) | "No label-informed selection over this pool beats static injection here — the ceiling was measured, not merely unmeasured. The cost-benefit justification for building EXP068 is withdrawn; **EXP068 is cancelled in its current form**." | "Falsification of the adaptive loop hypothesis $H_{\mathrm{loop}}$" (never tested — EXP070 tests label-informed selection over a static pool, not the adaptive target-free loop); "representation-level adaptation is impossible in general" (family-, model-, benchmark-restricted); "the loop's evaluator would fail" (the evaluator was never built — that is the point); "steering is impossible" (the output bridge still rescues); any claim about directions outside the pool (A-pool, §7). Re-motivation path: a future loop protocol motivated by a *different* candidate family (e.g., a positive EXP075 subspace result) is a new pre-registration, not a resurrection of the killed justification. |
| **No significant oracle gain without probe signal** (branch (c2)): no statistically significant C3-vs-C2 gain as in (c1), probe-signal gate failed (§8) | "The ceiling was **unmeasured** (probe uninformative) — not zero. No conclusion about the pool's ceiling may be drawn." | "EXP068 cancellation" — EXP068 is explicitly NOT cancelled. Required next step: re-register with a better probe (e.g., more probe items per vocabulary); never a silent re-run under EXP070. |
| **Oracle significantly worse than static** (branch (c3)): $p < 0.05$, $\Delta M_{\mathrm{oracle}} - \Delta M_{\mathrm{static}} < 0$ | "Per-instance selection over this pool actively hurts vs static. Justification withdrawn; **EXP068 is cancelled in its current form** — stronger than (c1)." (Ungated: a significant negative is itself a measured effect.) | Same exclusions as (c1). |
| **Oracle wins big** (branch (e)): margin $\ge +12$pp [ARBITRARY — sensitivity analysis required] and $p < 0.05$ | "A per-instance selection prize exists over this pool; the oracle–static gap quantifies the verifier's worth. **EXP068 is justified** — proceed to build the loop." | "The loop will work" (the loop must still find the direction **target-free**); "a target-free evaluator can recover the gap" (unmeasured); any novelty-tier movement (N1 stands); "invention" beyond selection among support-derived candidates. |
| **Oracle wins small** (branch (d)): C3 beats C2, $p < 0.05$, but margin $< +12$pp [ARBITRARY] | "A selection signal exists but is below the worth-chasing bar. Reachable: e.g., $(b=6,c=0)$ gives $10.0$pp at $p=0.03125$ on N=60." | EXP068 justification (the bar is the bar); $H_{\mathrm{loop}}$ confirmation. |

**[NOTE] on the asymmetry:** an oracle loss (with probe signal, §8) withdraws the loop's
justification; an oracle win merely *justifies building it*. The ceiling is an upper bound on
selection gain, not a lower bound on loop performance — a realizable loop cannot *systematically*
beat the oracle: in expectation, a target-free selector over the same pool does no better than
the label-informed oracle (a lucky single realization may match it). This asymmetry
is the entire methodological point, and it is why the false-kill route (A-pool, §7) is named
explicitly rather than assumed away.

---

## 2. Frozen model and SHA-256 guard

- **Model / tokenizer (in-scope):** `EleutherAI/pythia-160m` (identical to EXP065; the loop's primary
  development model per the EXP068 draft).
- **Architecture [FACT]:** GPT-NeoX; 162,322,944 params; $d = 768$; 12 layers; 12 attention heads;
  head dim $d_h = 64$; rotary embeddings; parallel attention/MLP; untied output embeddings.
- **Target layer:** $l^* = 10$ (83% depth, matching EXP065). Intervention $h \leftarrow h + \alpha u$
  via forward hook at $l^*$, last-token position.
- **Intervention strength:** $\alpha = 0.50$ **fixed** for all conditions (program continuity with
  EXP065/066; no tuning — this is a cheap pre-test, and tuning $\alpha$ would spend the budget
  this experiment exists to save).
- **Expected SHA-256:** `[TO BE REGISTERED at first execution — computed in the execution
  environment]` (same convention as the EXP068 draft §2; no GPU/torch on the drafting machine).
- **Guard procedure [FACT-level requirement]:** SHA-256 over the concatenation of `state_dict()`
  tensors (sorted keys, CPU, float32 bytes) computed before the oracle-probe phase and after the
  test phase. The **binding** guard is the runtime pre/post match; a registered value, once
  recorded, is a sanity check only (E-4 distinction, EXP067 §2). $\boxed{\Delta\theta \equiv 0}$
  is non-negotiable (Law #6). No backward pass exists anywhere in this protocol.

---

## 3. Formal mechanism

### 3.1 Candidate pool $\mathcal{P}$ [DEFINITION]

The pool is the **static, pre-computable union of the loop's Generate family**
(`theory/LOOP_SPEC_DRAFT.md` §2.1), fixed before any test item is touched:

1. **$\mathcal{G}_1$ family (8 draws):** bootstrap-resampled contrast aggregations exactly per the
   loop spec §2.1 — from the support contrast pairs $\{\Delta h_j^{(k)}\}$ ($k=1..5$ vocabularies),
   draw 8 bootstrap resamples (with replacement, stratified by vocabulary, seed 7001);
   per resample $i$: $\hat{v}^{(i)} = \mathrm{normalize}(\sum_k w_k^{(i)} \hat{v}_k^{(i)})$,
   $w^{(i)} \sim \mathrm{Dirichlet}(1,\dots,1)$ (seed 7002). Output: 8 unit directions.
2. **$\mathcal{G}_2$-ring family (8 draws):** one local-perturbation draw per $\mathcal{G}_1$
   candidate — $\mathrm{normalize}(\hat{v}^{(i)} + \varepsilon_i)$,
   $\varepsilon_i \sim \mathcal{N}(0, \sigma^2 I_d)$, $\sigma = 0.1$ (the loop spec's default;
   seed 7003). [FACT — computed]: $\sigma = 0.1$ in $d = 768$ gives
   $E[\cos(v, \mathrm{normalize}(v+\varepsilon))] \approx 1/\sqrt{1+d\sigma^2} \approx 0.34$ —
   a $\sim$70° cone, not a local neighborhood. The "1-step ring" is a wide spray; the loop's
   $\mathcal{G}_2$ is closer to repeated random search with selection than to fine
   hill-climbing, and the static pool (sprays around all 8 $\mathcal{G}_1$ draws) represents
   that search faithfully. A hypothetical 2-step ring would sit at $\cos \approx 0.12$
   ($\sim$83°) from its parent — nearly orthogonal, nearly random — and no static snapshot
   captures the loop's re-centering on accepted incumbents, so it is not added (see A-pool,
   §7). This is the minimal static representation of the refinement family the loop
   would explore at $t \ge 1$.
3. **Incumbent (1):** $B_{\mathrm{agg}} = \mathrm{normalize}(\sum_{k=1}^{5} \hat{v}_k)$ — the static
   aggregated contrast basis. Including it makes the oracle a strict superset selector: the
   oracle can always fall back to the static direction, so any measured oracle–static gap is
   pure *selection* gain, never pool luck.

$|\mathcal{P}| = 17$ unit directions, all built from **support data only** (no test labels, no
test items). The pool is archived in full per Law #13 (vectors, seeds, resample indices).

**[NOTE] on the sprint sketch:** the sketch named "$\mathcal{G}_1$ candidates, $K=8$" only. The
pool is deliberately widened to the loop's full Generate family (G1 + G2-ring + incumbent) so
the kill is family-honest: killing on G1-only would leave the "but refinement would find it"
objection open — which is exactly the false-kill route (§7). The widening makes the ceiling a
ceiling for the loop, not for an easier problem.

### 3.2 Oracle probe $\pi(x)$ [DEFINITION]

For each test instance $x$ with template/slot signature $(\tau(x), \{(e_i,\sigma_i)\})$:

$$\pi(x) := \text{one support item per vocabulary with matching } (\tau, \text{slot-signature}),
\text{ lowest support indices first (deterministic)},$$

yielding 5 labeled probe items (one per vocabulary: Anglo, Biblical, Greek, Roman, Modern).
Support items carry known correct/foil targets by construction (loop spec §2.2).

- **Probe-construction precondition:** every test item must expose $(\tau(x), \{(e_i,\sigma_i)\})$,
  and support items must expose theirs (holds by construction for the 150 support items per the
  loop spec §2.2). A test item whose signature is unavailable is **excluded** and logged (Law #8);
  signatures are never improvised. If the precondition cannot be satisfied for the benchmark as
  a whole, **HALT before any GPU spend** — reportable, not adjustable under EXP070.
- **Minimum probe size:** if fewer than 3 vocabulary-matched probe items exist for $x$, $x$ is
  excluded and logged. $N_{\mathrm{final}} \ge 50$ required (pre-registered power floor); if
  $N_{\mathrm{final}} < 50$, **HALT** — reportable.
- **Disjointness assertions (runtime):** probe item ids $\cap$ test item ids $= \varnothing$
  **and** support item ids $\cap$ test item ids $= \varnothing$ (candidates are built from the
  full support set — the second assertion closes the leakage path the first alone leaves open);
  violation of either aborts the run as a protocol violation. Both id lists are archived (§10).

**[INTERPRETATION] why template-matched support items:** the probe is the labeled analog of the
loop's own per-instance views (§2.2 of the loop spec: entity-frame substitutions of $x$). The
oracle selects on labeled *analogs* of $x$ — the closest mechanical realization of "what would
the best possible per-instance selector pick," without ever touching $x$ or its label.

### 3.3 Oracle selection rule [DEFINITION]

For test instance $x$, for each $B \in \mathcal{P}$: run $f_\theta$ on each probe item in
$\pi(x)$ with intervention $h \leftarrow h + \alpha B$ at $l^*$, and record
$r(B; q) = \mathbf{1}[\text{decision correct on probe item } q]$ (probe labels used —
permitted ceiling measurement, §1.1).

$$B^*(x) = \arg\max_{B \in \mathcal{P}} \bar{r}(B; \pi(x)),$$

ties broken by a seeded-random draw uniform over the top-tied candidates (seed 7005,
pre-registered; the draw is archived per instance) — **direction-neutral in expectation**:
neither the incumbent nor any challenger is favored. No human judgment enters anywhere.

[Rationale for the neutral tie-break — the draft's "conservative" framing was corrected
(M3 review)]: the $B_{\mathrm{agg}}$-preferring tie-break shrank the oracle–static gap,
biasing the instrument toward the kill branch — "conservative" for the justification claim
but anti-conservative for the kill, the wrong direction for a pre-test whose kill cancels a
research direction. The mean-probe-margin tie-break is dropped likewise: margin is an
O5-invalidated concept, and as a tie-break it would import margin noise into selection (m3).
Conservatism for the justification decision lives in the significance + magnitude bar
(§8: McNemar $p < 0.05$ AND $\ge +12$pp), where it belongs — not in the selection rule.

**[NOTE — documented deviation from the sprint sketch (Law #12)]:** the sprint's Idea 2 kill
criterion specifies "argmax-rescue per instance," readable as test-label argmax; this protocol
instead selects on labeled support analogs with test labels purely evaluative — a strictly
cleaner ceiling that avoids contaminating the measurement with test labels.

### 3.4 Intervention

- **C3 (oracle-selected):** $h \leftarrow h + \alpha B^*(x)$, per-instance, $\alpha = 0.50$.
- **C2 (static $B_{\mathrm{agg}}$):** $h \leftarrow h + \alpha B_{\mathrm{agg}}$ — the CAA-equivalent
  benchmark, identical construction to EXP065.
- All other conditions per §4. Injection-vector norms asserted $> 0$ at build time and persisted
  (the F1 lesson from the EXP067 bundle review — a silent-zero control must be impossible, not
  just absent).

### 3.5 Anti-cheat clause [DEFINITION]

1. The oracle touches **only** probe items $\pi(x)$ (support set). Test items and test labels are
   never used in candidate construction, probe evaluation, or selection. Selection indices are
   logged per instance; a post-run audit asserts no test id appears in any probe record.
2. Probe labels are support labels — their use is licensed **solely** as a ceiling measurement
   (§1.1). This does not relax Law #7 for EXP068 or any future loop experiment.
3. **Winner's-curse attenuation [LIMITATION — the draft's "deliberately generous" framing was
   backwards (M3 review)]:** candidates are built from the same support items the oracle probes
   on. The oracle selects the candidate that best fits 5 noisy probe items; the winner regresses
   on test. Probe-overfitting **attenuates** the measured test ceiling — it does not inflate it.
   [FACT — computed]: under pure selection noise, the expected best-of-17 probe score is
   $\approx 0.88$ against a true $0.50$ (and $P(\text{winner scores } 1.0) \approx 0.42$) — the
   oracle routinely "finds" illusory probe winners out of nothing. This makes the kill branch
   *easier* to trigger, not more damning. The protection against noise-kills is the probe-signal
   gate (§8); the conservatism for the justification decision is the significance + magnitude
   bar (§8) — neither lives in the selection rule.
4. **Any leakage** (test label used in selection; probe/test or support/test id overlap;
   post-hoc pool expansion) = **invalid run**, reported as a protocol violation per Law #8,
   never silently corrected under the EXP070 label.

---

## 4. Conditions (7)

| # | Condition | Intervention / procedure |
|---|---|---|
| C1 | Unintervened baseline | none |
| C2 | Static $B_{\mathrm{agg}}$ (CAA-equivalent benchmark) | $h \leftarrow h + \alpha B_{\mathrm{agg}}$, $\alpha = 0.50$ |
| C3 | **Oracle-selected per-instance direction (EXP070 mechanism)** | $h \leftarrow h + \alpha B^*(x)$ per §3.3 |
| C4 | Random-selected candidate ("any candidate works" killer) | uniform-random $B \in \mathcal{P}$ per instance, seed 7004 — separates "selection works" from "the pool is good" |
| C5 | Static $B_\perp$ | specificity control (seed 9876, inherited) |
| C6 | Static $B_{\mathrm{wrong}}$ | wrong-task control (Paris-capital contrast, as EXP066) |
| C7 | Same-layer output bridge (positive control) | identical to EXP066 `make_bridge_vec` |

---

## 5. Benchmark, headroom gate, and readiness

- **Benchmark:** the identical N=60 Planetary/Elemental 2-hop/3-hop suite from EXP065 (same items,
  same premise permutations). No new benchmark construction (Law #9).
- **Probe-construction gate:** run before anything else; §3.2 precondition must hold and
  $N_{\mathrm{final}} \ge 50$, else **HALT** (reportable).
- **Headroom gate:** run C1; require baseline accuracy $\in [40\%, 70\%]$ (program continuity,
  EXP067 §5). If outside: **HALT**; any recalibration requires a new pre-registration. A
  headroom halt is a reportable outcome, not adjustable under EXP070.

---

## 6. Endpoints

- **Primary (confirmatory):** $\Delta M$ (percentage points) on paired decisions, C3 vs C1;
  McNemar exact two-sided test on $(b, c)$.
- **Key comparison (the kill):** C3 vs C2 — paired McNemar exact two-sided on the
  (oracle, static) decision pairs over the same items. The kill criteria are stated on this
  comparison (§8 branches (c1)/(c2)/(c3), gated on probe signal).
- **Secondary (pre-registered):** C3 vs C4 (attribution: does *selection* beat random?);
  C2 vs C1 (static-null replication check on 160m); rescues $b$ / corruptions $c$;
  $\mathrm{KL}_{\mathrm{div}} < 0.50$ guardrail (exploratory, inherited);
  **probe-signal diagnostics** (these GATE the branch-(c) ruling, §8 — they are not mere
  caveats) — (i) fraction of instances where the oracle's pick strictly beat $B_{\mathrm{agg}}$
  on the probe (**reported only** — see note below; it does not gate); (ii) point-biserial
  correlation $r_{pb}$ between per-instance probe margin (winner's $\bar{r}$ minus
  $B_{\mathrm{agg}}$'s $\bar{r}$) and the test beats-static indicator
  $Y_x = \mathbf{1}[\text{C3 correct and C2 incorrect on } x]$ (the draft's loose "test rescue"
  is defined here as beating static head-to-head — the quantity branch (c) rules on);
  significance = one-sided $p < 0.05$ via $t = r_{pb}\sqrt{(n-2)/(1-r_{pb}^2)}$, $n = N_{\mathrm{final}}$
  (conventional $\alpha$, consistent with the program's McNemar $\alpha$); (iii) **selection
  concentration** $H_{\mathrm{sel}} = \max_{j \in \mathcal{P}} \frac{1}{N}\sum_x
  \mathbf{1}[B^*(x) = j]$ — under a noise probe, picks are approximately uniform over
  $\mathcal{P}$ (chance-level max $\approx 12\%$ on N=60, computed); under an informative
  probe, picks concentrate. Floor: $H_{\mathrm{sel}} \ge 25\%$ [ARBITRARY] ($\approx 2\times$
  the noise expectation, $\approx 6.5$ sd above it). Per-instance $B^*(x)$ index trace
  (archived; feeds (iii)).

  [NOTE on (i) — why it does not gate (M2 review)]: under pure selection noise, (i) $\approx$
  86% ([FACT — computed]: $P(B_{\mathrm{agg}} \text{ not top-tied})$ over 17 i.i.d. 6-valued
  probe scores) — it is high under both informative and noisy probes and therefore cannot
  distinguish them. The gate rests on (ii) (transfer: does probe signal predict test wins?)
  and (iii) (probe-side decisiveness for the zero-rescue edge).
- **Margin shifts:** recorded but **exploratory only** — audit Finding 3 / O5 stands: the C6
  control invalidates margin-shift significance as a causal endpoint.

---

## 7. Assumptions (named, not smuggled)

- **[ASSUMPTION] A-pool (the false-kill route — see §8 note):** the loop's adaptive multi-step
  $\mathcal{G}_2$ trajectory cannot reach rescuing directions outside the static pool
  $\mathcal{P}$ (G1 + 1-step ring + incumbent). The pool is a *snapshot*; the loop is a *path*.
  The kill in branches (c1)/(c3) is licensed **only** within the pre-registered search family,
  on this benchmark/model/layer. On the feared "2+ perturbation steps" scenario: $\sigma=0.1$
  in $d=768$ is a $\sim$70° cone ($E[\cos]\approx0.34$, §3.1) — the 1-step ring is already a wide
  spray, and a 2-step ring would sit at $\cos\approx0.12$ ($\sim$83°) from its parent: nearly
  orthogonal, nearly random. A static 2-step ring would not capture the loop's re-centering on
  accepted incumbents anyway — no static snapshot captures adaptivity — so adding it would be
  security theater (budget spent to look rigorous while leaving the real gap untouched), and it
  is not added. The wide step size actually strengthens the ceiling argument: with 70° steps
  there is little hill to climb — the loop's $\mathcal{G}_2$ is closer to repeated random search
  with selection than to fine hill-climbing, and the static pool (sprays around all 8
  $\mathcal{G}_1$ draws) represents that search faithfully. The static snapshot is a better
  proxy for the adaptive path than "local perturbation" suggests.
- **[ASSUMPTION] A-probe:** template-matched support items are valid labeled analogs of the
  test instance for selection purposes — i.e., a direction that rescues the probe analogs
  tends to rescue the instance. Tested by diagnostics (ii)/(iii), which **gate** the
  branch-(c) ruling (§8): if the probe shows no transfer signal, the ruling is (c2)
  uninformative — the caveat is not merely logged, it blocks the kill.
- **[ASSUMPTION] A-attenuation (renamed — the draft's "A-generous" framing was backwards,
  M3 review):** evaluating candidates on the support items they were built from induces
  winner's-curse attenuation of the measured ceiling (§3.5(3), quantified: expected best-of-17
  noise score $\approx 0.88$ vs true $0.50$). Direction of risk: the kill is *easier* to
  trigger, not more damning. Mitigations: the probe-signal gate (§8) blocks noise-kills; the
  significance + magnitude bar (§8) carries the conservatism for justification. Neither
  mitigation lives in the selection rule (§3.3 is direction-neutral).

---

## 8. Pre-registered decision tree

**Probe-signal gate** [DEFINITION] (M2 review — evaluated on entering branch (c), *before* any
(c1)/(c2) ruling; the diagnostics gate the kill, they are not a logged caveat):
- If the test beats-static outcomes $Y_x$ (§6) have nonzero variance: compute diagnostic (ii).
  **Gate passes** iff $r_{pb} > 0$ with one-sided $p < 0.05$ (probe signal transfers to test).
- Else (the oracle never beat static on any instance — (ii) is undefined): **gate passes** iff
  diagnostic (iii) $H_{\mathrm{sel}} \ge 25\%$ [ARBITRARY] — the probe drove selection decisively
  (systematic preferences) yet nothing transferred: a measured zero.
- Otherwise the gate fails → branch (c2).

**Branch precedence** [DEFINITION] (m8 review — resolves co-firing without executor improvisation):
(f) is evaluated before the selection-grounded rulings (c1)/(c3)/(d)/(e); a fired (f) suspends
their selection licenses (not (c2)'s probe logic, not (b)'s invalid-run discipline).

| # | Branch | Pre-registered ruling — LICENSES / DOES NOT LICENSE |
|---|---|---|
| (a) | **Readiness/headroom halt** (§5 gates fail) | **Reportable halt**, not a result about selection. LICENSES: "the benchmark/probe preconditions for the ceiling measurement are not met." DOES NOT LICENSE: anything about $H_{\mathrm{loop}}$. |
| (b) | **C7 positive control fails** (bridge: $\Delta M \le 0$ or $p \ge 0.05$) | **Invalid run** — setup broken or benchmark drifted. **No conclusion about $H_{\mathrm{loop}}$ may be drawn**; do not interpret C3 (EXP067 §7.1 branch (b) discipline). |
| (c1) | **Canonical kill (probe-gated):** C3 vs C2: **no statistically significant gain ($p \ge 0.05$), and** the probe-signal gate passes | **Justification withdrawn — EXP068 cancelled in its current form.** LICENSES: "No label-informed selection over this pool beats static injection here; the ceiling was measured, not merely unmeasured; therefore no target-free evaluator over the same pool can justify the loop's cost." DOES NOT LICENSE: anything in §1.2's (c1) column — read it before quoting this branch. |
| (c2) | **Uninformative probe:** C3 vs C2 shows no gain as in (c1), **but** the probe-signal gate fails | **Ceiling unmeasured — EXP068 NOT cancelled.** LICENSES: "The probe carried no transferable signal, so no ceiling was measured." Required next step: re-register with a better probe (e.g., more probe items per vocabulary, per the review's recommendation) — takes the next free number at pre-registration time; never a silent re-run under EXP070. DOES NOT LICENSE: any statement about the pool's ceiling; EXP068 cancellation. |
| (c3) | **Oracle significantly worse than static:** C3 vs C2 with McNemar $p < 0.05$ and $\Delta M_{\mathrm{oracle}} - \Delta M_{\mathrm{static}} < 0$ | **Justification withdrawn — EXP068 cancelled in its current form (stronger than (c1)).** LICENSES: "Per-instance selection over this pool actively hurts vs static." Ungated: a significant negative is itself a measured effect — with the direction-neutral tie-break, it means static systematically beats the pool's non-static candidates. DOES NOT LICENSE: anything in §1.2's (c1) column — read it before quoting this branch. |
| (d) | **Oracle wins small:** C3 beats C2, McNemar $p < 0.05$, but margin $< +12$pp [ARBITRARY] | **Ambiguous — EXP068 NOT justified.** LICENSES: "a selection signal exists but is below the worth-chasing bar." Reachable (unlike the draft's version): e.g., $(b=6,c=0)$ gives $10.0$pp at $p=0.03125$; $(b=8,c=1)$ gives $11.7$pp at $p=0.039$ (N=60). Sensitivity bands at $+16$pp and $+20$pp reported alongside the ruling. |
| (e) | **Oracle wins big:** C3 beats C2 by $\ge +12$pp [ARBITRARY — sensitivity analysis required] **and** McNemar $p < 0.05$ | **EXP068 JUSTIFIED — explicitly NOT validated.** LICENSES: "a per-instance selection prize exists; the oracle–static gap quantifies the verifier's worth; proceed to build the loop." DOES NOT LICENSE: anything in §1.2's oracle-win column — read it before quoting this branch. |
| (f) | **No selection signal:** C4 (random) $\ge$ C3 ($\Delta M_{C4} \ge \Delta M_{C3}$), or C3 $\approx$ C4 while both beat C2 | **Do not kill or justify on selection grounds.** LICENSES: "the pool helps but *selection* doesn't (f2-analog of EXP068 §11) — or the oracle methodology is uninformative." Diagnose probe leakage/noise via §6 diagnostics before any re-registration. A C4 $>$ C2 finding alone is a pool-quality result, reported as such (Law #8), not a loop justification. (Precedence: (f) is evaluated before (c1)/(c3)/(d)/(e); a fired (f) suspends their selection licenses — see the branch-precedence note above.) |
| (g) | **C2 static replicates the EXP065 null** ($\Delta M = 0$, $b = c = 0$) while C7 rescues | Consistency check passed — the boundary result reproduces on this run; the ceiling measurement was taken under the same conditions as the program's headline null. If C2 shows $\Delta M \ne 0$ here, flag the discrepancy vs EXP065 before interpreting any branch (benchmark/drift diagnostic). |

**Justification for the $+12$pp worth-chasing bar** [INTERPRETATION — re-derived after the M1
review]: a worth-chasing bar must bind *independently* of the significance test, or it is
decoration. [FACT — computed] under exact two-sided McNemar at $\alpha = 0.05$:
$(b=5,c=0) \to p=0.0625$ (not significant — the draft's "$+8$pp $\approx$ 5 net rescued items
with McNemar $p<0.05$" sentence was false and is retracted); $(b=6,c=0) \to p=0.03125$
(significant). So any significant oracle–static gap on the pre-registered $N$ range implies
$\ge 6$ net pure rescues ($\ge 10$pp at $N=60$; $\ge 12$pp at $N=50$) — a $+8$pp bar would never
bind, and branch (d) as originally defined could never fire. The bar is therefore set at
$+12$pp [ARBITRARY — sensitivity analysis required]: the lowest round bar strictly above the
significance floor at which the p-value and the magnitude conditions bind independently (at
$N=60$: $(b=6,c=0)$ is significant at $10.0$pp but below the bar → branch (d);
$(b=8,c=0)$ clears it at $13.3$pp, $p=0.0078$ → branch (e); at the $N_{\mathrm{final}}=50$
floor the two conditions coincide and the p-value remains binding). Rationale: the oracle is
an *unachievable* upper bound; a target-free evaluator will recover only a fraction of its
gap. Honest note on halving: a $+12$pp oracle gap halved is $6$pp — below the detection
floor — so $+12$pp is a *lenient* worth-chasing bar, and the halving-honest level ($\sim+20$pp)
is reported as the upper sensitivity band, not the primary bar. Branches (d)/(e) are reported
at $+12$/$+16$/$+20$pp so the ruling's threshold-dependence is visible, not hidden.

**[NOTE] on the false-kill route (for the adversarial reviewer):** the single most dangerous way
this pre-test kills the loop falsely is **A-pool (§7)**. The oracle pool is a *static snapshot*
of the loop's search space; the loop itself is an *adaptive path*. The kill is licensed **only
within the pre-registered search family**, and the "2-step ring" objection is answered in §7
(rejected as security theater — a static ring cannot capture re-centering on accepted incumbents,
and at $\cos\approx0.12$ it would be nearly random anyway). A reviewer who wants to attack this
pre-registration should attack the family restriction on the kill's license, or the probe-signal
gate's floors — not the pool width.

---

## 9. Budget and compute plan (free-tier feasibility)

[DEFINITION] Primary compute metric: forward passes. All accounting is **worst-case, no
caching** (probe evaluations cached across test instances sharing a template signature would
only reduce passes; caching is a permitted optimization that changes no ruling).

| Phase | Forward passes (worst case) | Basis |
|---|---|---|
| Oracle probe evaluation | $\le 5{,}100$ | 17 candidates $\times$ 5 probe items $\times$ 60 instances |
| Test conditions C1–C7 | $420$ | $7 \times 60$ single forwards |
| **Total** | **$\le 5{,}520$** | |
| Wall-clock, conservative | $\approx 45$ min | $5{,}520 \times 0.49$ s/pass (the loop spec's measured-rate basis) |
| Wall-clock, expected | $10$–$20$ min | T4 realistic $0.1$–$0.2$ s/pass for pythia-160m short sequences [CONJECTURE] |

**The budget fits under ~1 GPU-hour on the conservative estimate** — no fudging: the
conservative column uses the program's own measured-rate basis, and it still clears the bar
with margin. **Order of operations (m4):** (1) probe-construction/$N_{\mathrm{final}}$ gate (metadata, no GPU)
→ (2) 5-instance pilot (GPU: wall-clock measurement **and** a probe-yield smoke check — report
diagnostics (i)/(iii) on the 5 instances as a sanity signal, not a ruling) → (3) full launch.
The run is splittable across Kaggle sessions (probe phase →
test phase are natural checkpoints with all state archived). **410m replication** (if branch
(e) lands): takes the next free number at pre-registration time (m1 — not pre-claimed here);
not pre-registered here; requires its own pilot measurement.

---

## 10. Reproducibility and hygiene (Law #13; the T-1 lesson)

- **Seeds (pre-registered):** master `torch.manual_seed(20260923)`, NumPy `20260923`;
  $\mathcal{G}_1$ bootstrap 7001; Dirichlet weights 7002; $\mathcal{G}_2$-ring 7003;
  C4 random selection 7004; tie-break draw 7005; $B_\perp$ 9876 (inherited).
- **Archive (all persisted):** the 17 pool vectors + resample/perturbation indices and seeds;
  per-instance probe scores $\bar{r}(B; \pi(x))$ for all $B \in \mathcal{P}$; the selected
  $B^*(x)$ index and its tie-break draw; injection-vector norms (F1 lesson: asserted $>0$);
  per-instance condition records in the EXP066 JSON schema; probe/support/test id lists (for
  the disjointness audit, M5); environment manifest.
- **Hook isolation:** forward hook registered per instance, removed after; no inter-instance
  state. Determinism: `torch.use_deterministic_algorithms(True)` where supported.
- **No silent retuning:** any change to pool, probe, selection rule, or thresholds after
  execution begins is a protocol violation — the changed design takes the next free number
  at pre-registration time.

---

## 11. Non-goals (explicit)

- This protocol does not test any target-free evaluator — none is built here.
- It does not test the loop's $\mathcal{S}/\mathcal{T}$ dynamics, multi-iteration compounding,
  or the $\rho$-gate — those belong to EXP068.
- It does not claim the oracle is achievable, deployable, or interesting as a method — it is
  a measuring instrument, discarded after use.
- It does not move the novelty tier in any direction (N1 stands; §1.1).

---

## 12. What EXP070 does NOT test

- Directions outside the pre-registered pool $\mathcal{P}$ (A-pool bounds the license).
- Whether a *different* candidate family (matrix-valued bases, per-instance $\alpha$, layer
  sweeps) would change the ceiling — each is a separate future protocol.
- Cross-model or cross-scale ceilings (160m only; the 410m replication takes the next free number at pre-registration time).
- The origin of the raw $\approx 0.7$ cosine or the causal-break location (EXP067's territory).

---

**Pre-registration checklist:** ☐ pool $\mathcal{P}$ fixed (17 vectors, seeds 7001–7003) ☐ probe
construction fixed (§3.2, probe∩test and support∩test assertions) ☐ oracle selection rule fixed
(§3.3, direction-neutral seeded tie-break, seed 7005) ☐ anti-cheat clause armed (§3.5, M5
support∩test assertion) ☐ $\alpha = 0.50$ fixed ☐ headroom gate armed ☐ $N_{\mathrm{final}}
\ge 50$ gate armed ☐ $+12$pp bar recorded [ARBITRARY] with $+16$/$+20$pp sensitivity bands ☐
probe-signal gate armed (§8: diagnostics (ii)/(iii) gate branch (c)) ☐ full decision
tree recorded (§8, every branch has a LICENSES / DOES NOT LICENSE) ☐ A-pool named as the
false-kill route (2-step ring rejected, §7) ☐ SHA-256 guard armed ☐ budget $\le 5{,}520$ passes
($\approx 45$ min conservative)
*No results exist under this protocol. Any deviation is a protocol violation, not a discovery.*
