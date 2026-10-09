# EXP150 Pre-registration — DRAFT: EXP149a bench-repair re-attempt — transitive-only hop dose-response with stratified dry-run gate and hardened-compositional pilot — 2026-10-09

**Status: DRAFT — NOT SIGNED. NOT EXECUTED.** This pre-registration drafts the licensed bench-repair re-attempt of EXP149a (LOG-4969) for the CEO-minted experiment number EXP150 (LOG-4971). It awaits independent Law #14 review and CEO sign + execution authorization. No forwards have been run under this number.

**Drafting lane:** EXP150 innovation-sprint design, 2026-10-09. **Experiment number EXP150 minted by the CEO** (LOG-4971) — new operationalization = new number per the single-lane fence; EXP149's HELD verdict stands untouched (a HELD scopes nothing and overturns nothing).

**Parent context [FACT]:** EXP148 (J7) CONTINUE ADOPTED (LOG-4958/4959; independent verdict review ADOPT, LOG-4960): frozen Pythia-410m, WRITE/READ prompting discipline beat budget-matched CoT by net +22.2pp (b=52, c=12, one-sided McNemar p=2.2833e-07, 95% Wald CI (0.1414, 0.3031)). Mandatory caveats: S vs B net −0.2500 (direct answering still beats WRITE/READ); discipline gain, not autonomous steering; single model, single bench. EXP149 (LOG-4969) HELD both follow-ups at Step-0 gates: (a) pooled dry-run gate tripped on subset composition (B=0.90 on a 12/20 compositional-2hop draw); the post-stop diagnostic found compositional strata at/near ceiling (B = 0.9895/0.9316) vs transitive at 0.3105/0.3316. LOG-4969 licensed exactly two repairs: (i) a stratified dry-run gate, (ii) a hardened compositional template or transitive-only dose-response.

**The narrowing [DEFINITION]:** EXP150 asks the dose-response question on the **transitive strata only**. The narrowing is registered here, in a new numbered experiment, for the stated reason (compositional strata at ceiling — no headroom to measure a gain; §1/§6). It does not reinterpret, re-draw, or re-litigate EXP149's HELD (Law #4 satisfied by construction).

**Governing laws:** Law #2 (every constant below is pinned, computed, or carried from a signed artifact — never improvised), Law #4 (no post-hoc hypothesis shifts), Law #6 (Δθ=0), Law #7 (bench golds never touch prompts), Law #9 (primaries registered here, before any new output is inspected — EXP149's descriptive stratum nets are prior observations and motivation, not test targets; hardened-compositional breakdowns descriptive only), Law #11 (labels throughout), Law #13 (determinism), Law #15 (worth-it gate §1).

**Epistemological labels** per `~/workspace/SCBI/AGENTS.md` §5 are load-bearing below. [NOTE] and [CAVEAT] mark operational clarifications.

---

## 0. The questions

**Primary — transitive-only hop dose-response [HYPOTHESIS]:** The WRITE/READ discipline advantage over budget-matched CoT grows with reasoning depth on the transitive strata: net(S−C) at transitive-3hop exceeds net(S−C) at transitive-2hop — δ̂_T3 − δ̂_T2 > 0, on frozen Pythia-410m, with a fresh bench.

**Breaking point (primary):** 95% CI for (δ̂_T3 − δ̂_T2) entirely ≤ 0, with per-level guards (d_s),(e),(f),(f′) PASS → **KILL** the transitive-scoped dose-response claim (the gain does not grow with hops on the transitive strata; EXP148's CONTINUE stands as a pooled effect, not a depth effect).

**Secondary — hardened compositional pilot [OBSERVATION target]:** descriptive S−C nets and 95% CIs per hardened-compositional level, *if* the (d-HC*) gates pass. No decision table — descriptive only (Law #9).

**Scope fence [DEFINITION]:** EXP150 tests depth-dependence on transitive strata **only**, at Δθ=0, no fine-tuning. It licenses no Gap claim, no steering claim, no claim about the compositional strata, other families, or scales. Whatever fires here *scopes* EXP148's CONTINUE; nothing overturns it.

**What this pre-registration does not do:** it does not re-litigate EXP148 (CONTINUE stands) or EXP149 (HELD stands — the gate outcome is not re-drawn or reinterpreted); it does not change the models, the arms, the prompts, or the scoring; it does not touch the paper or any killed lane; it does not license execution (independent review SIGN + CEO authorization still required).

---

## 1. Worth-it gate (Law #15, 7 points)

1. **Exact questions [HYPOTHESIS]:** §0 — (primary) is the discipline gain depth-driven on strata with verified headroom (δ̂_T3 > δ̂_T2)? (secondary) does the hardened compositional instrument measure anything?
2. **Decisions changed:**
   - **Primary:** CONTINUE (§4): 95% CI for (δ̂_T3 − δ̂_T2) entirely above 0 AND transitive-3hop S−C one-sided p < 0.05 → dose-response supported on transitive strata; the capability entry gains a depth axis (transitive-scoped). KILL (§4): CI entirely ≤ 0 with per-level guards (d_s),(e),(f),(f′) PASS → the gain is not depth-driven on transitive strata. HELD (§4): anything else. RUN-INVALID (§4): apparatus guard trip — never a verdict.
   - **Secondary:** descriptive only — reported nets + CIs, no decision table, no verdict.
3. **Cheapest tests:** the EXP148 three-arm design (B: T_B=15; C, S: T=120 budget-matched) on a fresh bench with 4 strata (transitive-2hop, transitive-3hop — primary; hardened-compositional-2hop, hardened-compositional-3hop — secondary), 190 items/stratum, frozen Pythia-410m, greedy, Δθ=0. Preceded by the binding stratified Step-0 gate.
4. **Cost:** $0 CPU. ≈ 193.8k generation forwards + 1,200 stratified dry-run forwards + 4,800 C+S pilot forwards = **199.8k ≤ guard (g) 200k**. Wall ≈ 9h at EXP148 rates — re-gated at Step 0 (guard (h) ≤ 72h).
5. **Mathematical license:** EXP148/EXP149 pre-reg §§2–3 inherited unchanged — (a) first-token scoring [DEFINITION]; (b) WRITE/READ discipline definition [DEFINITION]; (c) budget-matched CoT control [DEFINITION] with guard (f′) earning the "budget-matched" label; (d) the McNemar decision machinery [DEFINITION] with the S7-1 §2.2 Wald convention (SE = √[(b+c) − (b−c)²/n]/n).
6. **Quantitative predictions:** if depth-driven on transitive: δ̂_T3 − δ̂_T2 ≥ +0.10. If the breaking point holds: δ̂_T3 − δ̂_T2 ≤ 0. **Power licenses:** §2 (registered Step-0 bench-size rule; the transitive d is not pre-known) — the registered true-power band is [0.53, 0.64] (Fix E1/E3); whether to run at this power is the CEO's Law #15 call (Advisory A5 — the band is registered honestly here; the call is not this document's).
7. **Breaking points:** §0 — plus the binding stratified Step-0 gate (§5.4): a (d-T*) trip STOPS the study at design cost (no full run, no verdict); a (d-HC*) trip drops that secondary stratum descriptively.

**Why this is worth doing [INTERPRETATION]:** the primary is the cleanest remaining test of whether the program's first capability entry is depth-driven — asked on strata where a gain is in principle measurable, with the pooled-gate defect of EXP149 repaired by construction. A KILL is a sharp boundary (pooled/headroom-driven gain, not depth-driven); a CONTINUE genuinely extends the entry with a depth axis. The secondary pilot tests whether the compositional instrument can be repaired at all — a finding about bench construction with value beyond this experiment. HELDs cost only design compute.

---

## 2. Power analysis [FACT]

Per-level net δ̂_h = (b_h − c_h)/n_h; primary θ = δ̂_T3 − δ̂_T2; Wald SE(θ) = √[SE(δ̂_T3)² + SE(δ̂_T2)²], SE(δ̂_h) = √[(d_h − δ̂_h²)/n_h] (S7-1 §2.2 convention, carried). EXP148 realized per-level SE = 0.0412 at n=180 (b=52, c=12, d=0.3556).

**Design value [DEFINITION]:** n_T2 = n_T3 = 190 per hop level, fixed by the registered bench (4 strata × 190 items, §5.1). EXP149's power table (n=380) does not transfer. Recomputed for the registered bench (independent Law #14 recomputation, this review): at d = 0.30–0.36, SE(θ) = 0.0523–0.0580, power **0.53–0.64** for δ = +0.10, one-sided α = 0.05 — the registered true-power band is **[0.53, 0.64]**. Power table (δ=+0.10, one-sided α=0.05): (d=0.30, net=0.20) → SE 0.0523, power 0.61; (d=0.32, net=0.20) → SE 0.0543, power 0.58; (d=0.36, net=0.20) → SE 0.0580, power 0.53; (d=0.30, net=0.25) → SE 0.0500, power 0.64. [Fix E1, Law #14 review 2026-10-09.]

**Registered Step-0 power rule [DEFINITION] (replaces the EXP149 n-raise rule per CEO disposition E3 — no n-raise is registered: the bench is fixed at 190/stratum (§5.1), so no larger n exists):** at Step 0 the execution lane computes registered Wald-formula power — Φ(0.10/SE(θ) − 1.645) with SE(θ) = √[(d_src − 0.10²)(2/190)] — from the registered discordant-pair rate d_src, for δ = +0.10, one-sided α = 0.05, at the bench's fixed n_T2 = n_T3 = 190. **Registered d_src, in precedence order:** (1) the 20-item C+S pilot discordant-pair rate d_pilot = (b+c)/20 on the pilot's S−C correctness pairs, drawn from the **transitive** strata (§5.4); (2) EXP148's realized d = 0.3556 carried as the planning sanity-check value, keyed to the first 20-item C+S block of the full run: if the first-block rate d_block1 implies required n above the bench size (registered power at n=190 < 0.53), the lane STOPS the full run at that point — logged HELD — a computation, not a choice. **Bench-size outcome [DEFINITION]:** if the Step-0 registered power < 0.53 (the true-power band floor), the study STOPS at design cost — logged HELD (the bench cannot supply even the design's own power bar; a computation, not a choice). The achieved power governs CONTINUE probability, not KILL validity: the CI-entirely-≤-0 KILL bar with false-KILL 0.025 under δ=0 is intact and fails safe to HELD. [Fix E3, Law #14 review 2026-10-09; CEO disposition E3.]

**n-raise guard re-assertion [SUPERSEDED]:** the EXP149 Fix-D5 n-raise guard re-assertion is superseded here — no n-raise is registered (the bench is fixed at 190/stratum, §5.1), so no raised-n re-projection exists. Guard (g) ≤ 200k and guard (h) ≤ 72h are asserted at design cost (199.8k forwards, ≈9h) and re-asserted at Step 0 on the bench's fixed n. The bench-size STOP rule (above) is the only registered power-driven stop. [Fix E3, Law #14 review 2026-10-09.]

**KILL-bar operating characteristics (carried):** under δ = 0, P(95% CI entirely ≤ 0) = 0.025 (remainder is HELD — the design fails safe); under true δ = +0.10, false-KILL < 1e-4; under true δ = −0.10 (reverse dose-response), P(KILL fires) ≈ **0.41–0.48** (recomputed at n=190: Φ(0.10/0.0523 − 1.96) ≈ 0.48 at d=0.30; Φ(0.10/0.0580 − 1.96) ≈ 0.41 at d=0.36) [Fix E2, Law #14 review 2026-10-09].

---

## 3. Frozen decision bars (verbatim from EXP148 pre-reg §3, applied to the transitive primary)

- Paired per-item correctness under §5.3 scoring. KILL = conjunction: (i) one-sided McNemar (H1: S>C) p ≥ 0.1, AND (ii) two-sided McNemar p ≥ 0.1, AND (iii) 95% Wald CI for net δ̂=(b−c)/n entirely below +0.10 (upper < +0.10).
- PIVOT: KILL fires AND transitive-3hop S vs B one-sided McNemar (H1: S>B) p < 0.05 — test-time compute helps at depth but discipline doesn't (carried verbatim per the registered carry rule; CEO disposition A1/LOG-4968 applies).
- CONTINUE: one-sided p < 0.05 AND net δ̂ ≥ +0.10.
- KILL is scoped: "the discipline gain does not grow with hops on the transitive strata" — it neither rules out sub-10pp depth effects nor says anything about the compositional strata.

---

## 4. Decision tables (binding)

**Registered composition rule [DEFINITION] (E4, Law #14 review 2026-10-09):** §4's decision table is the sole binding verdict machinery for the EXP150 primary; §3's per-level KILL/CONTINUE conjunctions are superseded for the primary verdict and retained only as the source definitions for the CONTINUE table's transitive-3hop S−C clause and the PIVOT condition, both restated in §4. [Fix E4.]

Precedence: RUN-INVALID > HELD > KILL > CONTINUE. The stratified Step-0 gate (§5.4) precedes the full run. The hardened-compositional secondary is descriptive-only — no decision table (Law #9).

### 4. Primary — transitive-only hop dose-response

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | 95% CI for (δ̂_T3 − δ̂_T2) entirely above 0 AND transitive-3hop S−C one-sided (H1: S>C) p < 0.05 | Dose-response supported on transitive strata: the discipline gain grows with reasoning depth; the capability entry gains a (transitive-scoped) depth axis |
| KILL | 95% CI for (δ̂_T3 − δ̂_T2) entirely ≤ 0, with per-level guards (d_s),(e),(f),(f′) PASS | Dose-response dead on transitive strata: the gain does not grow with hops there — it is pooled/headroom-driven. EXP148's CONTINUE stands as a pooled effect, not a depth effect |
| PIVOT | KILL fires AND (per-level) S vs B one-sided (H1: S>B) p < 0.05 on transitive-3hop | (Alongside KILL) Test-time compute helps at depth but discipline doesn't — pivot to test-time-compute scaling |
| HELD | Anything else (CI too wide, any per-level guard (d_s) or (f′) trips) | Inconclusive — licenses nothing, kills nothing |
| RUN-INVALID | Any per-level apparatus guard (a)/(c)/(e)/(f)/(g)/(h) trips | Apparatus failure — never a verdict |

---

## 5. Protocol

### 5.1 Bench [DEFINITION]

**Fresh bench, registered construction:** 4 strata × 190 items = 760 items — transitive-2hop, transitive-3hop (primary; transitive recipe carried from EXP147/148 §5.1), hardened-compositional-2hop, hardened-compositional-3hop (secondary; distractor-chain procedure, `EXP150_DESIGN_DRAFT_2026-10-09.md` §5, validity constraints (v1)–(v4) asserted at construction, zero forwards). Construction seed registered at execution (≠ 149001). Closed 40-entity pool; entity-disjoint exemplars (Law #7); golds single entity names, ≥2× per the EXP148 recipe. Bench pin recomputed character-identical (64/64) at Step 0 before any forward (guard (c)). Never transcribed. Golds used only at scoring (§5.3).

### 5.2 Arms and prompts (carried verbatim from the EXP149 pre-reg §5.2)

- **Model:** frozen Pythia-410m. Greedy decoding (do_sample=False), Δθ=0. Model revision resolved programmatically at Step 0 from the local cache (expectation `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` — carried, re-resolved not transcribed).
- All arms 2-shot (shot-count controlled). **B:** `Context: {facts}\nQuestion: {question}\nAnswer with the name only.\nAnswer: …` — T_B=15. **C:** `Context: {facts}\nQuestion: {question}\nThink step by step. Give the final answer after "ANSWER:".` — T=120. **S:** `Context: {facts}\nQuestion: {question}\nUse the scratchpad. WRITE each deduced fact as WRITE(fact1, ...), WRITE(fact2, ...). When you need a fact, READ it: READ(fact1). Give the final answer after "ANSWER:".` — T=120 (same T as C — the compute-confound fence).
- **Exemplars:** reuse the EXP148 Step-0-pinned exemplar file byte-identical. If unavailable at execution, rebuild by the S7-1 §5.2 construction procedure (two worked 2-hop items per arm, entity-disjoint from the bench) and record the new pin. Either way, exemplar text is committed before any bench forward.

### 5.3 Scoring (registered, deterministic — EXP149 pre-reg §5.3 verbatim)

1. **B arm:** full generation → normalize (lowercase, strip punctuation, collapse whitespace) → FIRST whitespace-delimited token → exact match vs normalized gold → 1, else 0.
2. **C/S arms:** text after the LAST `ANSWER:` → normalize → FIRST whitespace-delimited token → exact match vs gold → 1, else 0. No `ANSWER:` → 0 (no post-hoc rescue).
3. Primary metric: per-item correctness per arm. All verdict statistics are paired McNemar on (S, C) and (S, B) correctness pairs — the primary additionally the difference of the two per-level transitive S−C nets. No LLM judge (Law #13).

### 5.4 Step-0 guards and gates (binding — precede the full run)

**Shared:**
- **(u0) Scoring-pipeline unit test** (zero forwards): the C/S `ANSWER:`-parsing path asserted on synthetic strings (standard/lowercase/multiple-ANSWER:/trailing-rambling/missing→0) → else RUN-INVALID.
- **(a) Δθ=0:** pre/post state-dict hash equality.
- **(b) Model revision:** resolved programmatically; expectation carried (§5.2).
- **(c) Bench pin:** recomputed character-identical (64/64) before any forward.
- **(d_s) Stratified calibration gate (licensed repair (i)):** 20 fresh items per stratum × 4 strata = 80 items (subset seeds registered at execution, ≠ construction seed, ≠ each other), B arm only, T_B=15, greedy, §5.3 scoring.
  - **(d-T2)/(d-T3):** transitive-2hop / transitive-3hop B accuracy ∈ [0.2, 0.8] [ASSUMPTION — registered] → else the study STOPS at design cost (1,200 + 4,800 + build forwards), logged HELD — the primary is unmeasurable.
  - **(d-HC2)/(d-HC3):** hardened-compositional-2hop / hardened-compositional-3hop B accuracy ∈ [0.2, 0.8] [ASSUMPTION — registered] → else that stratum is excluded from the secondary (logged descriptively); the primary proceeds.
- **(e) Discipline delivered:** ≥50% of S generations contain ≥1 well-formed `WRITE\(fact\d+,` span (regex on raw generation) → else RUN-INVALID. [NOTE]: WRITE-only by design; READ efficacy is efficacy, not delivery.
- **(f) Compute delivered:** mean_tokens(C) > 2 × mean_tokens(B) AND mean_tokens(S) > 2 × mean_tokens(B) → else RUN-INVALID. [ASSUMPTION — 2× registered.]
- **(f′) Budget matched:** mean_tokens(S)/mean_tokens(C) ∈ [2/3, 3/2] — per hop level → else HELD. [ASSUMPTION — band registered.]
- **(g) Budget audit:** total generation forwards ≤ 200k.
- **(h) Compute gate:** throughput probe (50 generation steps, fixed dummy prompt, excluded from benches) at Step 0; projected full-run ≤ 72h → else INCONCLUSIVE (compute-infeasible). Never self-escalate to GPU. [ASSUMPTION — 72h registered.]

**C+S pilot (registered, carried — Fix D8):** a separate fresh 20-item subset drawn from the **transitive** strata (pilot seed registered at execution, ≠ construction seed, ≠ dry-run subset seeds), C and S arms only (T=120, greedy, §5.3 scoring), cost 20×240 = 4,800 generation forwards. Its S−C discordant-pair rate d_pilot = (b+c)/20 is the registered Step-0 planning input for the §2 power rule (with EXP148's d = 0.3556 first-block keying).

**4-hop:** not re-registered (design §6 — out of scope; a new numbered experiment, not a quiet addition).

**Descriptive reporting (not guards):** B-arm format compliance; mean extra-token counts; hardened-compositional per-level S−C nets + 95% CIs (descriptive — Law #9, no stratum promoted to a decision).

**Pooled-computation exclusion [DEFINITION] (Advisory A3, Law #14 review 2026-10-09):** items from any (d-HC*)-dropped stratum are excluded from all full-run pooled computations; the secondary is per-stratum descriptive only, so no pooled secondary statistic is registered.

### 5.5 Cost

$0 CPU. ≈ 193.8k generation + 1,200 stratified dry-run + 4,800 C+S pilot = **199.8k ≤ guard (g) 200k**. **Margin note [NOTE]:** design cost sits at 99.9% of the 200k cap (200 forwards of headroom) — razor-thin by construction; the bench-size STOP rule and Step-0 re-assertion cover overruns (a computation, not a choice). [Advisory A1 noted, Law #14 review 2026-10-09.] Wall-time asserted at Step 0 per guard (h), never in advance (Law #2).

### 5.6 Determinism (Law #13)

Bench construction seed registered at execution; dry-run/pilot subset seeds registered (≠ construction seed, ≠ each other); generation seeds fixed per arm, registered; greedy decoding; model revision 40-hex pinned at Step 0 from cache; environment manifest recorded (same CPU stack family as EXP148/149 — re-recorded, not assumed). Per-item records flushed per write. Weights loaded from local caches only — no HF Hub contact at execution.

---

## 6. Material uncertainties

1. **The transitive d (power):** the registered Step-0 bench-size rule (§2) computes power at the bench's fixed n=190 from the transitive C+S pilot rate (d_block1 keying carried); there is no n-raise — if the Step-0 registered power < 0.53 (true-power band floor) the study STOPS at design cost, logged HELD (a computation, not a choice) [Fix E3].
2. **Reverse dose-response:** if δ̂_T3 − δ̂_T2 < 0 with a tight CI, the KILL fires — and a strong reverse pattern is itself a finding (headroom-driven gain), reported descriptively.
3. **Hardened-compositional difficulty:** unverified until built — that is why the secondary is descriptive-only. If the hardening fails (gate trip), the secondary is dropped and the primary is unaffected; the instrument result is reported as a bench-construction finding.
4. **The narrowing:** the transitive-scoped hypothesis is a new registration in a new numbered experiment (EXP150), not a post-hoc shift — EXP149's unscoped question HELD, and its gate outcome is not re-drawn or reinterpreted here.
5. **Prior-data honesty:** EXP149's descriptive stratum pattern motivated both the narrowing and the hardening; the test runs on a fresh bench — Law #9 is satisfied by construction, and this registration makes the motivation auditable.

---

*Pre-registration draft finalized 2026-10-09 (LOG-4971). Status: DRAFT — NOT SIGNED. NOT EXECUTED. No forwards run. Companion: `EXP150_DESIGN_DRAFT_2026-10-09.md`. Awaited: independent Law #14 review of the pre-reg draft → CEO sign → execution authorization (Step-0 gates first). Execution NOT licensed by this document.*

---

## Fixes applied (Law #14 review repair lane, 2026-10-09)

- **E1:** §2 power table recomputed for the registered bench (n_T2 = n_T3 = 190): SE(θ) = 0.0523–0.0580, power 0.53–0.64 for δ=+0.10, one-sided α=0.05 — registered true-power band [0.53, 0.64]; all n=380-carried figures corrected. (Independently re-verified this lane: SE √[(d−0.04)(2/190)], power Φ(0.10/SE−1.645).)
- **E2:** reverse dose-response P(KILL fires) ≈0.77 (n=380 carry) → **≈0.41–0.48** at n=190 (Φ(0.10/0.0523−1.96) ≈ 0.48 at d=0.30; Φ(0.10/0.0580−1.96) ≈ 0.41 at d=0.36). (Independently re-verified this lane.)
- **E3:** the 0.80-bar n-raise rule is superseded — no n-raise is registered (bench fixed at 190/stratum; no larger n exists). Registered Step-0 bench-size rule: registered Wald-formula power at n=190 from d_src (pilot d_pilot, then d_block1 keying); if < 0.53 (band floor) the study STOPS at design cost, logged HELD (computation, not choice). Achieved power governs CONTINUE probability, not KILL validity (false-KILL 0.025 under δ=0 intact, fails safe). CEO disposition: the 0.80 bar is unsatisfiable; the true-power bar is accepted.
- **E4:** registered composition rule at the top of §4 — §4's decision table is the sole binding verdict machinery for the primary; §3's per-level KILL/CONTINUE conjunctions are superseded for the primary verdict and retained only as the source definitions for the CONTINUE table's transitive-3hop S−C clause and the PIVOT condition (both restated in §4).
- **A1:** razor-thin guard-(g) margin (199.8k/200k) registered explicitly in §5.5.
- **A2:** noted — registered seed-derivation rule for future pre-regs; no change in this draft.
- **A3:** (d-HC*)-dropped stratum items explicitly excluded from all full-run pooled computations (registered in §5.4).
- **A4:** PIVOT carry consistent with CEO disposition A1/LOG-4968; noted, not objected — no change.
- **A5:** Law #15 worth-it at ≈0.53–0.64 power flagged for the CEO's call — not a repair-lane decision; the band is registered honestly in §§1–2.

**Status after repair: repaired per the independent review's exact prescriptions (`EXP150_LAW14_REVIEW_2026-10-09.md`). STILL NOT SIGNED — signing is the CEO's act after diff-level re-verification. NOT EXECUTED. No hypothesis, guard, or decision-bar change was made; all fixes are numeric/expositional plus the registered E3/E4 rule registrations.**
