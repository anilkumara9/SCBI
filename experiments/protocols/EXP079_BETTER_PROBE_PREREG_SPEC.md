# EXP079 Protocol Specification: Oracle-Selection Ceiling with Out-of-Sample Probe — Verifier-First, Second Attempt

**Status:** PRE-REGISTERED (Law #14 adversarial review SIGN — 0 major, 5 minor findings all addressed, 2026-09-23)
**Date:** 2026-09-23
**Author role:** Preregistration Agent
**Predecessor experiments:** EXP070 (branch (c2) UNINFORMATIVE_PROBE, LOG-110 — the mandated
re-registration); EXP063–EXP068 (boundary series); EXP078 (closed, branch (a))
**Source idea:** EXP070 §8 branch (c2) required next step: "re-register with a better probe
(e.g., more probe items per vocabulary, per the review's recommendation) — takes the next free
number at pre-registration time; never a silent re-run under EXP070."
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `STATISTICAL_PROTOCOL_V02.md`,
`theory/LOOP_SPEC_DRAFT.md` (signed — the loop this pre-test gates),
`research/MATH_STANDARDS_CHARTER.md` (M1–M8), `research/literature/audit_2026-09-23.md` (N1 verdict)
**Execution rule:** Strictly confirmatory. No pool, probe, selection-rule, or threshold changes after
execution begins without a new pre-registration. **Changed design = the next free number at
pre-registration time.**

---

## 0. Re-registration note: why EXP070's probe failed, and what changes here

**[OBSERVATION] EXP070's result (LOG-110):** branch (c2) UNINFORMATIVE_PROBE. The oracle —
permitted label access on 5 template-matched support probe items per instance, selecting by
argmax mean correctness over 17 candidates (8 G1 bootstrap + 8 G2-ring + B_agg incumbent) —
gained ΔM = +0.00pp over static (b=0, c=0, p=1.0). The probe-signal gate failed on path (iii):
H_sel = 0.100 against the 0.25 floor; oracle-beats-B_agg on probe = 6.7% (reported only).

**[OBSERVATION] The 6.7% figure diagnoses degeneracy, not noise.** EXP070 §6 computed that under
pure selection noise, diagnostic (i) ≈ 86% ([FACT — computed]: P(B_agg not top-tied) over 17
i.i.d. 6-valued probe scores). The observed 6.7% is an order of magnitude below the noise
expectation: B_agg was top-tied on ~93% of instances. The probe scores were not noisy — they
were degenerate.

**[OBSERVATION] H_sel = 0.100 sits below the noise mean.** [FACT — computed, seed 7979, 100k
Monte Carlo draws]: under the null of direction-neutral selection uniform over 17 candidates,
H_sel at N=60 has mean 0.121, sd 0.020, 95th percentile 0.150; P(null H_sel ≥ 0.100) = 0.976.
EXP070's observed 0.100 is *below* the null mean — fully consistent with uniform tie-break
diffusion, and evidence against any systematic probe preference. (The old 0.25 floor was
≈6.5 sd above the null mean: [INTERPRETATION] arbitrary and, worse, uncalibrated — it could
not distinguish "noisy probe" from "degenerate probe".)
**[LIMITATION]** The Multinomial(1/17) null idealizes candidates as exchangeable; G1
span-sharing may correlate selections, pushing the (iii)-path false-pass rate slightly above
nominal 5%. The primary (ii) transfer gate is unaffected.

**[INTERPRETATION] Root cause: in-sample probing.** All 17 candidates were constructed from the
same 150 support contrast pairs the oracle then probed on. On in-sample items every candidate
scores at or near ceiling → near-total ties → the direction-neutral tie-break (seed 7005)
diffuses picks uniformly → H_sel at the noise floor → no transferable signal by construction.
Two aggravating factors: (1) granularity — 5 probe items admit only 6 score levels for 17
candidates, so ties are structurally inevitable even absent (1)... [CORRECTION: this factor is
secondary — with out-of-sample items, 5 items still tie often; the fix addresses both];
(2) pool span-homogeneity — the 8 G1 candidates are bootstrap reweightings of the same five
v̂_k and hence lie in the same 5-dimensional span as B_agg; on probe items they are
near-indistinguishable even out-of-sample, leaving the G2-ring sprays (70° cones) as the only
real diversity.

**[INTERPRETATION] What the better probe must do:** break the in-sample degeneracy (probe items
must be out-of-sample relative to candidate construction), increase score granularity (more
items per instance), and face a gate whose bar is calibrated against the selection null rather
than set by fiat. If the improved probe *still* shows no transfer signal, the licensed reading
is no longer "the probe was degenerate" but "the pool is causally homogeneous on this
benchmark" — a pool-quality finding, not a probe failure (branch (c2*) below).

**Design delta vs EXP070 (the only licensed changes):**
1. **Split-half support:** the 150 support contrast pairs are split deterministically
   (even/odd pair indices within each vocabulary) into BUILD (75 pairs: 15/vocab, even indices)
   used for *all* candidate construction, and HELDOUT (75 pairs: 15/vocab, odd indices) used
   *only* for probing. Candidates are thereby out-of-sample on every probe item. This changes
   B_agg's construction inputs (documented, intended); C2 uses the same BUILD-derived B_agg, so
   C3-vs-C2 remains apples-to-apples.
2. **Probe size:** up to 15 held-out probe items per instance (template/slot-signature matched,
   lowest global indices first, deterministic), minimum 8 (up from 3) — finer granularity
   (16 score levels vs 6).
3. **Calibrated gate:** the H_sel floor is replaced by the 95th percentile of the null
   max-fraction distribution (Monte Carlo, 100k draws, seed 7979, K=17, N=N_final) —
   [FACT — computed] 0.150 at N=60, 0.160 at N=50 — instead of the arbitrary 0.25.

Everything else — hypotheses, model/layer/α, the 17-family pool construction, the selection
rule (argmax + direction-neutral seeded tie-break), conditions C1–C7, benchmark, endpoints,
the +12pp worth-chasing bar with +16/+20pp bands, anti-cheat discipline, Δθ=0 — is carried
over from EXP070 unchanged. The probe is the changed variable; the pool's *inputs* change to
the BUILD half as the mechanical consequence (same 17-family construction, §7). Per pre-test
discipline, one mechanism changes.

---

## 1. Research question and hypotheses

$$\boxed{\textbf{Can \textit{any} per-instance selection over the loop's candidate pool —
even with an oracle's label access on out-of-sample probes — beat static CAA-equivalent injection?}}$$

**[HYPOTHESIS] H_ceiling:** Label-informed per-instance selection (the oracle) over the candidate
pool the EXP068 loop would search yields $\Delta M_{\mathrm{oracle}} > \Delta M_{\mathrm{static}}$
(McNemar exact $p < 0.05$ on the paired oracle-vs-static decisions) on the headroom-calibrated
benchmark — i.e., there exists a per-instance selection prize worth chasing.

**Null $H_0$:** $\Delta M_{\mathrm{oracle}} \le \Delta M_{\mathrm{static}}$ ($p \ge 0.05$) — even the
oracle cannot beat static injection; the loop's build-justification is withdrawn without building
it (see §1.2 — justification-withdrawal, not falsification of the adaptive loop hypothesis, which
EXP079 never tests).

### 1.1 Scope of this experiment (methodology pre-test, not a method)

[INTERPRETATION] EXP079 is the EXP070-mandated second attempt at the **kill-the-loop pre-test**:
**verifier-first, generator-second.** Before spending ~116k forward passes building the EXP068
$\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop, measure the maximum achievable gain of
*any* selection procedure over the loop's candidate pool — this time with a probe capable of
resolving candidates. The ceiling logic is unchanged from EXP070 §1.1:

- If **even oracle selection cannot beat static injection** (and the calibrated probe-signal
  gate of §8 confirms the ceiling was measured rather than merely unmeasured), no realizable
  target-free evaluator selecting over the same pool can justify the loop's cost → the
  build-justification for the loop is withdrawn; EXP068 is cancelled in its current form
  (justification-withdrawal, not falsification of $H_{\mathrm{loop}}$).
- If **oracle selection wins decisively**, the oracle–static gap quantifies the verifier's
  worth; EXP068 is justified (not validated).

The oracle's label access is **permitted**: this is a ceiling *measurement*, not a proposed
method. Law #7's test-time information boundary applies to the EXP068 loop, not to this
diagnostic. The anti-cheat clause (§3.5) is what keeps the ceiling honest — strengthened here
by the split-half construction (§3.2).

### 1.2 Logical structure: what each outcome licenses and does NOT license

| Outcome | LICENSES | DOES NOT LICENSE |
|---|---|---|
| **No significant oracle gain with probe signal** (branch (c1*)): no statistically significant C3-vs-C2 gain ($p \ge 0.05$), calibrated probe-signal gate passes (§8) | "No label-informed selection over this pool beats static injection here — the ceiling was measured with an out-of-sample, resolving probe, not merely unmeasured. The cost-benefit justification for building EXP068 is withdrawn; **EXP068 is cancelled in its current form**." | "Falsification of $H_{\mathrm{loop}}$" (never tested); "representation-level adaptation is impossible in general" (family-, model-, benchmark-restricted); "the loop's evaluator would fail" (never built); "steering is impossible" (the output bridge still rescues); any claim about directions outside the pool (A-pool, §7). Re-motivation path: a future loop protocol motivated by a *different* candidate family is a new pre-registration, not a resurrection. |
| **No significant oracle gain without probe signal** (branch (c2*)): no gain as in (c1*), calibrated gate fails (§8) | "The ceiling remains **unmeasured** — but the probe was already de-degenerated once. The licensed reading is now pool-homogeneity, not probe failure: the pool's candidates are causally near-indistinguishable on this benchmark. **EXP068 is explicitly NOT cancelled.**" Required next step: a pool-diversity diagnostic (measure pairwise causal disagreement among pool candidates directly) — **not** a third probe iteration under the same candidate family. | "EXP068 cancellation"; any statement about the pool's ceiling; "the probe needs more items" (that hypothesis was tested and exhausted here). |
| **Oracle significantly worse than static** (branch (c3*)): $p < 0.05$, $\Delta M_{\mathrm{oracle}} - \Delta M_{\mathrm{static}} < 0$ | "Per-instance selection over this pool actively hurts vs static. Justification withdrawn; **EXP068 is cancelled in its current form** — stronger than (c1*)." (Ungated: a significant negative is itself a measured effect.) | Same exclusions as (c1*). |
| **Oracle wins big** (branch (e)): margin $\ge +12$pp [ARBITRARY] and $p < 0.05$ | "A per-instance selection prize exists over this pool; the oracle–static gap quantifies the verifier's worth. **EXP068 is justified** — proceed to build the loop." | "The loop will work" (target-free recovery unmeasured); any novelty-tier movement (N1 stands); "invention" beyond selection among support-derived candidates. |
| **Oracle wins small** (branch (d)): C3 beats C2, $p < 0.05$, margin $< +12$pp [ARBITRARY] | "A selection signal exists but is below the worth-chasing bar." | EXP068 justification; $H_{\mathrm{loop}}$ confirmation. |

**[NOTE] on the asymmetry** (inherited from EXP070 §1.2, unchanged): an oracle loss (with probe
signal) withdraws the loop's justification; an oracle win merely *justifies building it*. A
realizable target-free selector over the same pool does no better in expectation than the
label-informed oracle. This asymmetry is the entire methodological point.

## 2. Frozen model and SHA-256 guard

- **Model / tokenizer (in-scope):** `EleutherAI/pythia-160m` (identical to EXP065/EXP070; the
  loop's primary development model). [DEFINITION] In this document, "the model" denotes this
  checkpoint at layer $l^*=10$; $d=768$ denotes its residual-stream width.
- **Architecture [FACT]:** GPT-NeoX; 162,322,944 params; $d = 768$; 12 layers; 12 attention
  heads; head dim $d_h = 64$; rotary embeddings; parallel attention/MLP; untied output embeddings.
- **Target layer:** $l^* = 10$ (83% depth, matching EXP065/EXP070). Intervention
  $h \leftarrow h + \alpha u$ via forward hook at $l^*$, last-token position; every $u$ is a
  unit vector in $\mathbb{R}^{768}$ (M4.4).
- **Intervention strength:** $\alpha = 0.50$ **fixed** for all conditions (program continuity;
  no tuning — the probe is the changed variable, and tuning $\alpha$ would spend the budget
  this pre-test exists to save).
- **Expected SHA-256:** `[TO BE REGISTERED at first execution — computed in the execution
  environment]` (EXP070 convention).
- **Guard procedure [FACT-level requirement]:** SHA-256 over the concatenation of `state_dict()`
  tensors (sorted keys, CPU, float32 bytes) before the oracle-probe phase and after the test
  phase. The **binding** guard is the runtime pre/post match. $\boxed{\Delta\theta \equiv 0}$
  non-negotiable (Law #6). No backward pass exists anywhere in this protocol.

## 3. Formal mechanism

### 3.1 Candidate pool $\mathcal{P}$ [DEFINITION]

Identical 17-family construction to EXP070 §3.1 (G1 ×8 bootstrap, seeds 7001/7002; G2-ring ×8,
$\sigma=0.1$, seed 7003; B_agg incumbent), with one change: all constructions use the **BUILD**
half of the support set only (75 contrast pairs: 15 per vocabulary, even pair-indices within
each vocabulary, deterministic). The G2-ring's $E[\cos]\approx0.34$ computation (EXP070 §3.1,
[FACT — computed]) is unaffected — it depends on $\sigma$ and $d$ only. $|\mathcal{P}|=17$ unit
directions in $\mathbb{R}^{768}$ (M4.1/M4.2/M4.4), archived per Law #13 with resample indices
and seeds. The pool remains a strict superset selector: the oracle can always fall back to the
incumbent, so any oracle–static gap is pure *selection* gain.

### 3.2 Split-half support and out-of-sample oracle probe $\pi(x)$ [DEFINITION]

**Split [DEFINITION]:** within each of the 5 vocabularies, the 30 support contrast pairs (indexed
0–29 in the loop spec's construction order) are split into BUILD = even indices (15 pairs) and
HELDOUT = odd indices (15 pairs). Deterministic; no seed; no human judgment. BUILD feeds §3.1
exclusively; HELDOUT feeds probing exclusively. Neither half is touched by the other phase.

For each test instance $x$ with template/slot signature $(\tau(x), \{(e_i,\sigma_i)\})$:

$$\pi(x) := \text{held-out support pairs with matching } (\tau, \text{slot-signature}),
\text{ lowest global pair-indices first (deterministic), capped at 15},$$

each pair contributing its labeled items as probe items (support labels by construction, loop
spec §2.2). Probe labels are used — permitted ceiling measurement, §1.1; Law #7 applies to the
EXP068 loop, not to this diagnostic.

- **Probe-construction precondition:** signatures must exist (holds by construction); a test
  item whose signature is unavailable is **excluded** and logged (Law #8); signatures are never
  improvised. If the precondition fails benchmark-wide, **HALT** before GPU spend — reportable.
- **Minimum probe size:** if fewer than **8** signature-matched held-out items exist for $x$,
  $x$ is excluded and logged. $N_{\mathrm{final}} \ge 50$ required (pre-registered power floor);
  if $N_{\mathrm{final}} < 50$, **HALT** — reportable.
- **Disjointness assertions (runtime):** probe item ids $\cap$ test item ids $= \varnothing$,
  support item ids $\cap$ test item ids $= \varnothing$, **and** probe item ids $\cap$ BUILD item
  ids $= \varnothing$ (the new assertion — candidates are built from BUILD, so this closes the
  in-sample path that degenerated EXP070's probe); violation of any aborts as a protocol
  violation. All id lists archived (§10).

**[INTERPRETATION] why this fixes the degeneracy:** probe items are now out-of-sample relative
to every candidate's construction data. Candidates can no longer score at ceiling by
memorization; their probe scores must reflect genuine directional differences. With up to 15
items (16 score levels), ties among 17 candidates become the exception rather than the rule,
so the direction-neutral tie-break stops being the de-facto selector.

### 3.3 Oracle selection rule [DEFINITION]

Unchanged from EXP070 §3.3: for test instance $x$, for each $B \in \mathcal{P}$, run $f_\theta$
on each probe item in $\pi(x)$ with $h \leftarrow h + \alpha B$ at $l^*$, record
$r(B; q) = \mathbf{1}[\text{correct on } q]$;

$$B^*(x) = \arg\max_{B \in \mathcal{P}} \bar{r}(B; \pi(x)),$$

ties broken by seeded-random uniform draw over top-tied candidates (seed 7005, archived per
instance) — direction-neutral in expectation. No human judgment. (The M3-reviewed rationale
stands: conservatism lives in the significance + magnitude bar, §8, not in the selection rule.)

### 3.4 Intervention

- **C3 (oracle-selected):** $h \leftarrow h + \alpha B^*(x)$, per-instance, $\alpha = 0.50$.
- **C2 (static $B_{\mathrm{agg}}$):** $h \leftarrow h + \alpha B_{\mathrm{agg}}$ with $B_{\mathrm{agg}}$
  built from BUILD pairs only (§3.1) — the CAA-equivalent benchmark on the same data the pool
  sees. [NOTE] This B_agg differs from EXP070's (full-support) B_agg by construction; the
  branch-(g) replication check interprets accordingly.
- All other conditions per §4. Injection-vector norms asserted $> 0$ at build time and
  persisted (F1 lesson).

### 3.5 Anti-cheat clause [DEFINITION]

1. The oracle touches **only** probe items $\pi(x)$ (HELDOUT half). Test items and test labels
   are never used in candidate construction, probe evaluation, or selection. BUILD items are
   never probed on. Selection indices logged per instance; post-run audit asserts no test id
   in any probe record and no BUILD id in any probe record.
2. Probe labels are support labels — licensed **solely** as a ceiling measurement (§1.1). No
   relaxation of Law #7 for EXP068 or any future loop experiment.
3. **Winner's-curse [LIMITATION]:** selection over 17 candidates on ~15 noisy probe items still
   induces winner's curse on test — attenuated vs EXP070 (out-of-sample probing removes the
   in-sample inflation; [INTERPRETATION] the remaining curse is ordinary selection noise, not
   structural degeneracy). Direction of risk unchanged: the kill is *easier* to trigger, not
   more damning. Mitigations: the calibrated probe-signal gate (§8) blocks noise-kills; the
   significance + magnitude bar (§8) carries justification conservatism.
4. **Any leakage** (test label in selection; probe/test, support/test, or probe/BUILD id
   overlap; post-hoc pool expansion) = **invalid run**, protocol violation per Law #8, never
   silently corrected under the EXP079 label.

## 4. Conditions (7)

| # | Condition | Intervention / procedure |
|---|---|---|
| C1 | Unintervened baseline | none |
| C2 | Static $B_{\mathrm{agg}}$ (BUILD-half; CAA-equivalent benchmark) | $h \leftarrow h + \alpha B_{\mathrm{agg}}$, $\alpha = 0.50$ |
| C3 | **Oracle-selected per-instance direction (EXP079 mechanism)** | $h \leftarrow h + \alpha B^*(x)$ per §3.3 |
| C4 | Random-selected candidate ("any candidate works" killer) | uniform-random $B \in \mathcal{P}$ per instance, seed 7004 |
| C5 | Static $B_\perp$ | specificity control (seed 9876, inherited) |
| C6 | Static $B_{\mathrm{wrong}}$ | wrong-task control (Paris-capital contrast, as EXP066) |
| C7 | Same-layer output bridge (positive control) | identical to EXP066 `make_bridge_vec` |

## 5. Benchmark, headroom gate, and readiness

- **Benchmark:** the identical N=60 Planetary/Elemental 2-hop/3-hop suite from EXP065/EXP070
  (same items, same premise permutations). No new benchmark construction (Law #9).
- **Probe-construction gate:** §3.2 precondition must hold and $N_{\mathrm{final}} \ge 50$, else
  **HALT** (reportable).
- **Headroom gate:** run C1; require baseline accuracy $\in [40\%, 70\%]$ (program continuity,
  EXP067 §5). If outside: **HALT**; recalibration requires a new pre-registration.

## 6. Endpoints

- **Primary (confirmatory):** $\Delta M$ (percentage points) on paired decisions, C3 vs C1;
  McNemar exact two-sided test on $(b, c)$. Null $H_0$: the paired (oracle, static) decisions
  are exchangeable (M5.3).
- **Key comparison (the kill):** C3 vs C2 — paired McNemar exact two-sided over the same items.
  Kill criteria on this comparison (§8 branches (c1*)/(c2*)/(c3*), gated on the calibrated
  probe signal).
- **Secondary (pre-registered):** C3 vs C4 (attribution); C2 vs C1 (static-null check on the
  BUILD-half B_agg); rescues $b$ / corruptions $c$; $\mathrm{KL}_{\mathrm{div}} < 0.50$ guardrail
  (exploratory, inherited); **probe-signal diagnostics** (these GATE the branch-(c*) ruling,
  §8) — (i) fraction of instances where the oracle's pick strictly beat $B_{\mathrm{agg}}$ on
  the probe (**reported only** — EXP070 showed it is degenerate under ties and uninformative
  under noise; it does not gate); (ii) point-biserial $r_{pb}$ between per-instance probe
  margin (winner's $\bar{r}$ minus $B_{\mathrm{agg}}$'s $\bar{r}$) and the test beats-static
  indicator $Y_x = \mathbf{1}[\text{C3 correct and C2 incorrect on } x]$; one-sided $p < 0.05$
  via $t = r_{pb}\sqrt{(n-2)/(1-r_{pb}^2)}$, $n = N_{\mathrm{final}}$ (conventional $\alpha$);
  (iii) **selection concentration** $H_{\mathrm{sel}} = \max_{j \in \mathcal{P}}
  \frac{1}{N}\sum_x \mathbf{1}[B^*(x) = j]$ against the **calibrated null bar** (§8). Per-instance
  $B^*(x)$ index trace archived (feeds (iii)).
- **Margin shifts:** recorded but **exploratory only** — audit Finding 3 / O5 stands.

## 7. Assumptions (named, not smuggled)

- **[ASSUMPTION] A-pool (the false-kill route):** as EXP070 §7 — the kill is licensed only
  within the pre-registered search family, on this benchmark/model/layer. **Amendment for
  EXP079:** the pool is built from the BUILD half (75 pairs) rather than the full support.
  [INTERPRETATION] This makes the pool slightly *weaker* (less data per v̂_k), biasing toward
  the kill, not away from it — the calibrated gate (§8) is the protection, as before. The
  family (G1+G2-ring+incumbent) is unchanged, so the ceiling remains a ceiling for the loop's
  Generate family.
- **[ASSUMPTION] A-probe-v2:** held-out support pairs with matching template/slot signature
  are valid labeled analogs of the test instance — i.e., a direction that rescues the probe
  analogs tends to rescue the instance. Tested by diagnostics (ii)/(iii), which **gate** the
  branch-(c*) ruling (§8): no transfer signal → (c2*), the caveat blocks the kill.
- **[ASSUMPTION] A-selection-noise:** ordinary winner's-curse from selecting among 17 on
  ~15 noisy items (attenuated vs EXP070; §3.5(3)). Direction of risk: kill-easier.
  Mitigations: calibrated gate + significance/magnitude bar.
- **[ASSUMPTION] A-split-representativeness:** even/odd pair indices are exchangeable within
  each vocabulary (no index-correlated difficulty gradient in the loop spec's construction
  order). [NOTE] If the loop spec's pair ordering carries a difficulty trend, BUILD and
  HELDOUT differ systematically — flagged here as a stated debt; the direction-neutral
  selection rule and the C2-apples-to-apples comparison contain the damage, and any
  BUILD/HELDOUT accuracy asymmetry is reported (Law #8).

## 8. Pre-registered decision tree

**Calibrated probe-signal gate** [DEFINITION] (M5.2/M5.3 — evaluated on entering branch (c*),
*before* any (c1*)/(c2*) ruling; the diagnostics gate the kill, they are not a logged caveat):
- **Null for (iii)** [DEFINITION]: under no probe signal, per-instance selection is uniform
  over $\mathcal{P}$ ($K=17$), so $H_{\mathrm{sel}}$ follows the max-fraction distribution of
  $\mathrm{Multinomial}(N_{\mathrm{final}}, (1/17,\dots,1/17))$. **Bar:** the 95th percentile
  of this distribution, computed by 100k Monte Carlo draws (seed 7979, pre-registered) at
  analysis time with the realized $N_{\mathrm{final}}$ — [FACT — computed] 0.150 at N=60,
  0.160 at N=50. This replaces EXP070's arbitrary 0.25 floor: the bar is now a property of
  the selection null, not of the drafter's caution.
- If the test beats-static outcomes $Y_x$ (§6) have nonzero variance: compute diagnostic (ii).
  **Gate passes** iff $r_{pb} > 0$ with one-sided $p < 0.05$ (probe signal transfers to test).
- Else (the oracle never beat static on any instance — (ii) undefined): **gate passes** iff
  diagnostic (iii) $H_{\mathrm{sel}} \ge \bar{H}$ (calibrated bar) — the probe drove selection
  decisively yet nothing transferred: a measured zero.
- Otherwise the gate fails → branch (c2*).

**Branch precedence** [DEFINITION] (inherited): (f) is evaluated before the selection-grounded
rulings (c1*)/(c3*)/(d)/(e); a fired (f) suspends their selection licenses (not (c2*)'s probe
logic, not (b)'s invalid-run discipline).

| # | Branch | Pre-registered ruling — LICENSES / DOES NOT LICENSE |
|---|---|---|
| (a) | **Readiness/headroom halt** (§5 gates fail) | **Reportable halt**, not a result about selection. LICENSES: "the benchmark/probe preconditions are not met." DOES NOT LICENSE: anything about $H_{\mathrm{loop}}$. |
| (b) | **C7 positive control fails** ($\Delta M \le 0$ or $p \ge 0.05$) | **Invalid run** — setup broken or benchmark drifted. **No conclusion about $H_{\mathrm{loop}}$**; do not interpret C3. |
| (c1*) | **Canonical kill (calibrated-probe-gated):** C3 vs C2 no significant gain ($p \ge 0.05$), **and** the calibrated probe-signal gate passes | **Justification withdrawn — EXP068 cancelled in its current form.** LICENSES: "No label-informed selection over this BUILD-half pool beats static injection here; the ceiling was measured with an out-of-sample, resolving probe. No target-free evaluator over the same pool can justify the loop's cost." DOES NOT LICENSE: anything in §1.2's (c1*) column. |
| (c2*) | **Still-uninformative probe:** C3 vs C2 shows no gain as in (c1*), **but** the calibrated gate fails | **Ceiling still unmeasured — EXP068 NOT cancelled.** LICENSES: "Even the de-degenerated probe carried no transferable signal: the pool's candidates are causally near-indistinguishable on this benchmark (pool-homogeneity finding)." Required next step: a pool-diversity diagnostic (direct pairwise causal-disagreement measurement among pool candidates) — **not** a third probe iteration under this candidate family. DOES NOT LICENSE: EXP068 cancellation; any statement about the pool's ceiling; "the probe needs more items." |
| (c3*) | **Oracle significantly worse than static:** C3 vs C2, McNemar $p < 0.05$, $\Delta M_{\mathrm{oracle}} - \Delta M_{\mathrm{static}} < 0$ | **Justification withdrawn — EXP068 cancelled in its current form (stronger than (c1*)).** Ungated: a significant negative is itself a measured effect. DOES NOT LICENSE: anything in §1.2's (c1*) column. |
| (d) | **Oracle wins small:** C3 beats C2, $p < 0.05$, margin $< +12$pp [ARBITRARY] | **Ambiguous — EXP068 NOT justified.** LICENSES: "a selection signal exists but is below the worth-chasing bar." Sensitivity bands at $+16$pp/$+20$pp reported. |
| (e) | **Oracle wins big:** C3 beats C2 by $\ge +12$pp [ARBITRARY] **and** $p < 0.05$ | **EXP068 JUSTIFIED — explicitly NOT validated.** LICENSES: "a per-instance selection prize exists; the oracle–static gap quantifies the verifier's worth; proceed to build the loop." DOES NOT LICENSE: anything in §1.2's oracle-win column. |
| (f) | **No selection signal:** C4 (random) $\ge$ C3 ($\Delta M_{C4} \ge \Delta M_{C3}$), or C3 $\approx$ C4 while both beat C2 | **Do not kill or justify on selection grounds.** LICENSES: "the pool helps but *selection* doesn't — or the oracle methodology is uninformative." Diagnose via §6 diagnostics before any next step. (Precedence: (f) before (c1*)/(c2*)/(c3*)/(d)/(e) — if (f) fires, its no-signal reading dominates; (c2*)'s pool-homogeneity reading is subsumed and no kill/justify branch fires, keeping the M5.2 partition unique.) |
| (g) | **C2 static check** ($\Delta M = 0$, $b = c = 0$) while C7 rescues | Consistency check on the BUILD-half B_agg. If C2 shows $\Delta M \ne 0$ here, flag vs EXP065/EXP070 (expected: possible small deviation — the B_agg construction inputs changed by design; the flag is a drift diagnostic, not a failure). |

**The $+12$pp worth-chasing bar** [INTERPRETATION — inherited from EXP070 §8, re-verified; the bar value itself is [ARBITRARY], justification and sensitivity bands below]:
under exact two-sided McNemar at $\alpha=0.05$, $(b=6,c=0) \to p=0.03125$ (significant) while
$(b=5,c=0) \to p=0.0625$ (not significant) — [FACT — computed]. Any significant oracle–static
gap on N=60 implies $\ge 6$ net pure rescues ($\ge 10$pp); the $+12$pp bar is the lowest round
bar strictly above the significance floor at which p-value and magnitude bind independently
($(b=6,c=0)$: 10.0pp significant but below bar → (d); $(b=8,c=0)$: 13.3pp, $p=0.0078$ → (e)).
The oracle is an unachievable upper bound; a target-free evaluator recovers only a fraction —
$+12$pp is lenient (halving-honest level $\sim+20$pp reported as upper sensitivity band).
Branches (d)/(e) reported at $+12$/$+16$/$+20$pp.

**[NOTE] on the false-kill route:** as EXP070 §8 — the dangerous false kill is **A-pool**; the
kill is licensed only within the pre-registered search family. The 2-step-ring objection is
rejected as before (security theater). A reviewer should attack the family restriction or the
gate calibration — not the pool width.

## 9. Budget and compute plan (free-tier feasibility)

[DEFINITION] Worst-case, no caching (probe evaluations cached across instances sharing a
template signature would only reduce passes; caching is a permitted optimization changing no
ruling).

| Phase | Forward passes (worst case) | Basis |
|---|---|---|
| Oracle probe evaluation | $\le 15{,}300$ | 17 candidates $\times$ 15 probe items $\times$ 60 instances |
| Test conditions C1–C7 | $420$ | $7 \times 60$ single forwards |
| **Total** | **$\le 15{,}720$** | |
| Wall-clock, conservative | $\approx 2$ h | $15{,}720 \times 0.49$ s/pass (program's measured-rate basis) |
| Wall-clock, expected | $15$–$30$ min | T4 realistic $0.1$–$0.2$ s/pass for pythia-160m short sequences [CONJECTURE] |

Fits in a single Kaggle GPU session with margin. **Order of operations:** (1) split-half +
probe-construction/$N_{\mathrm{final}}$ gate (metadata, no GPU) → (2) 5-instance pilot (GPU:
wall-clock **and** a probe-yield smoke check — report diagnostics (i)/(iii) on the 5 instances
as a sanity signal, not a ruling; EXPECT (i) materially above EXP070's 6.7% and (iii) ties rare
— if the pilot reproduces EXP070's degeneracy, HALT and diagnose before the full spend) →
(3) full launch. Splittable across sessions (probe phase → test phase are natural checkpoints,
all state archived).

## 10. Reproducibility and hygiene (Law #13)

- **Seeds (pre-registered):** master `torch.manual_seed(20260923)`, NumPy `20260923`;
  $\mathcal{G}_1$ bootstrap 7001; Dirichlet weights 7002; $\mathcal{G}_2$-ring 7003;
  C4 random selection 7004; tie-break draw 7005; $B_\perp$ 9876 (inherited);
  **7979** (H_sel null Monte Carlo — the only new seed; the even/odd split is deterministic
  and needs none).
- **Archive (all persisted):** BUILD/HELDOUT split indices; the 17 pool vectors +
  resample/perturbation indices and seeds; per-instance probe scores $\bar{r}(B; \pi(x))$ for
  all $B \in \mathcal{P}$; the selected $B^*(x)$ index and its tie-break draw; injection-vector
  norms (asserted $> 0$); per-instance condition records in the EXP066 JSON schema;
  probe/BUILD/test id lists (for the three disjointness audits, M5); the H_sel null Monte
  Carlo draws summary (seed, N_final, K, bar); environment manifest.
- **Hook isolation:** forward hook registered per instance, removed after; no inter-instance
  state. Determinism: `torch.use_deterministic_algorithms(True)` where supported.
- **No silent retuning:** any change to pool, probe, split, selection rule, or thresholds after
  execution begins is a protocol violation — the changed design takes the next free number.

## 11. Non-goals (explicit)

- This protocol does not test any target-free evaluator — none is built here.
- It does not test the loop's $\mathcal{S}/\mathcal{T}$ dynamics, multi-iteration compounding,
  or the $\rho$-gate — those belong to EXP068.
- It does not claim the oracle is achievable, deployable, or interesting as a method — it is
  a measuring instrument, discarded after use.
- It does not move the novelty tier in any direction (N1 stands; §1.1).
- It does not re-litigate EXP070's (c2) ruling — that ruling stands; this is its mandated
  successor.

## 12. What EXP079 does NOT test

- Directions outside the pre-registered pool $\mathcal{P}$ (A-pool bounds the license).
- Whether a *different* candidate family (matrix-valued bases, per-instance $\alpha$, layer
  sweeps) would change the ceiling — each is a separate future protocol.
- Cross-model or cross-scale ceilings (160m only; a 410m replication takes the next free
  number at pre-registration time).
- The origin of the raw $\approx 0.7$ cosine or the causal-break location (EXP067's territory).
- Whether the BUILD/HELDOUT split itself is optimal — the even/odd split is a stated,
  deterministic choice (A-split-representativeness), not a tuned one.

---

**Pre-registration checklist:** ☐ pool $\mathcal{P}$ fixed (17 vectors, seeds 7001–7003,
BUILD-half construction) ☐ even/odd split fixed (BUILD even / HELDOUT odd indices, no seed) ☐
probe construction fixed (§3.2: up to 15 held-out items, min 8, three disjointness assertions
incl. probe∩BUILD) ☐ oracle selection rule fixed (§3.3, direction-neutral seeded tie-break,
seed 7005) ☐ anti-cheat clause armed (§3.5) ☐ $\alpha = 0.50$ fixed ☐ headroom gate armed ☐
$N_{\mathrm{final}} \ge 50$ gate armed ☐ $+12$pp bar with $+16$/$+20$pp sensitivity bands ☐
calibrated probe-signal gate armed (§8: (ii) transfer test; (iii) H_sel vs 95th-pct null bar,
seed 7979; (i) reported-only) ☐ full decision tree recorded (§8, every branch has LICENSES /
DOES NOT LICENSE, unique/exhaustive partition per M5.2) ☐ A-pool named as the false-kill
route ☐ A-split-representativeness stated as debt ☐ SHA-256 guard armed ☐ budget $\le 15{,}720$
passes (single-session feasible) ☐ pilot probe-yield smoke check specified (degeneracy → HALT
before full spend)
*No results exist under this protocol. Any deviation is a protocol violation, not a discovery.*
