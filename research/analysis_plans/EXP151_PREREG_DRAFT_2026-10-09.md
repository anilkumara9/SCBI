# EXP151 Pre-registration — DRAFT: re-priced transitive-only hop dose-response at n=380/hop level (LOG-219 debt closure) — 2026-10-09

**Status: DRAFT — NOT SIGNED. NOT EXECUTED. NO EXPERIMENT NUMBER MINTED.** This pre-registration drafts the Law #15 packet licensed by the CEO's LOG-4977 ruling (option (a)) closing the LOG-219 OPEN debt from the LOG-4976 Friday cull. It awaits independent Law #14 review and CEO Law #15 sign + number-mint. No forwards have been run under this packet.

**Drafting lane:** EXP151 Law #15 packet lane (design only), 2026-10-09. **This lane does not mint experiment numbers** — the number (expected: EXP151) is minted by the CEO at the Law #15 SIGN-and-mint, per LOG-4977 constraint (7).

**Parent context [FACT]:** EXP148 (J7) CONTINUE ADOPTED (LOG-4958/4959; independent verdict review ADOPT, LOG-4960): frozen Pythia-410m, WRITE/READ prompting discipline beat budget-matched CoT by net +22.2pp (b=52, c=12, one-sided McNemar p=2.2833e-07, 95% Wald CI (0.1414, 0.3031)). Mandatory caveats: S vs B net −0.2500 (direct answering still beats WRITE/READ); discipline gain, not autonomous steering; single model, single bench. EXP149 (LOG-4969) HELD the hop dose-response at Step-0 (pooled gate tripped on a compositional-heavy draw; diagnostic: compositional at ceiling 0.9895/0.9316, transitive with headroom 0.3105/0.3316). EXP150 (LOG-4971/4972/4973) executed the transitive-only repair: stratified gate PASS, pilot licensed the full run (d_pilot = 0.30 → 0.566 ≥ 0.53), first full-run block d_block1 = 0.40 → registered power 0.466 < 0.53 → STOP/HELD per the bench-size rule. The hardened-compositional secondary was never built — (v2)/(v4) jointly unsatisfiable (design-record finding, LOG-4973). LOG-4976 escalated the unanswered transitive dose-response question (LOG-219); LOG-4977 ruled option (a): re-price the question at the n the d_block1 = 0.40 datum implies.

**The re-pricing [DEFINITION]:** this packet asks the transitive-scoped dose-response question on a bench that can supply the design's own power bar at the priced discordant rate: n_T2 = n_T3 = 380 per hop level (2 transitive strata × 380 = 760 items). It does not reinterpret, re-draw, or re-litigate EXP149's or EXP150's HELDs (Law #4 satisfied by construction — each HELD scopes nothing and overturns nothing).

**Governing laws:** Law #2 (every constant below is pinned, computed, or carried from a signed artifact — never improvised), Law #4 (no post-hoc hypothesis shifts), Law #6 (Δθ=0), Law #7 (bench golds never touch prompts), Law #9 (primaries registered here, before any new output is inspected — EXP150's block datum is prior data and prices the design's d-range, not a test target), Law #11 (labels throughout), Law #13 (determinism), Law #15 (worth-it gate §1).

**Epistemological labels** per `~/workspace/SCBI/AGENTS.md` §5 are load-bearing below. [NOTE] and [CAVEAT] mark operational clarifications.

---

## 0. The questions

**Primary — transitive-only hop dose-response [HYPOTHESIS]:** The WRITE/READ discipline advantage over budget-matched CoT grows with reasoning depth on the transitive strata: net(S−C) at transitive-3hop exceeds net(S−C) at transitive-2hop — δ̂_T3 − δ̂_T2 > 0, on frozen Pythia-410m, with a fresh bench at the registered n.

**Breaking point (primary):** 95% CI for (δ̂_T3 − δ̂_T2) entirely ≤ 0, with per-level guards (d_s),(e),(f),(f′) PASS → **KILL** the transitive-scoped dose-response claim (the gain does not grow with hops on the transitive strata; EXP148's CONTINUE stands as a pooled effect, not a depth effect). **Terminal registration:** a second HELD here is a design-debt finding, not a license for another re-attempt — the apparatus stands down at that point (LOG-4977).

**Scope fence [DEFINITION]:** EXP151 tests depth-dependence on transitive strata **only**, at Δθ=0, no fine-tuning. It licenses no Gap claim, no steering claim, no claim about the compositional strata, other families, or scales. Whatever fires here *scopes* EXP148's CONTINUE; nothing overturns it. Hardened-compositional is excluded by design-record (§5.1); its reconciliation is a deferred, unlicensed lane.

**What this pre-registration does not do:** it does not re-litigate EXP148 (CONTINUE stands), EXP149, or EXP150 (HELDs stand — no gate outcome is re-drawn or reinterpreted); it does not change the models, the arms, the prompts, or the scoring; it does not touch the paper or any killed lane; it does not license execution (independent review SIGN + CEO authorization still required); it does not mint an experiment number.

---

## 1. Worth-it gate (Law #15, 7 points)

1. **Exact question [HYPOTHESIS]:** §0 — is the discipline gain depth-driven on transitive strata, asked on a bench whose registered power clears the design's own bar at the priced discordant rate (δ̂_T3 > δ̂_T2)?
2. **Decisions changed:**
   - **Primary:** CONTINUE (§4): 95% CI for (δ̂_T3 − δ̂_T2) entirely above 0 AND transitive-3hop S−C one-sided p < 0.05 → dose-response supported on transitive strata; the capability entry gains a depth axis (transitive-scoped). KILL (§4): CI entirely ≤ 0 with per-level guards (d_s),(e),(f),(f′) PASS → the gain is not depth-driven on transitive strata. HELD (§4): anything else — **terminal for this line** (no further re-attempt licensed). RUN-INVALID (§4): apparatus guard trip — never a verdict.
3. **Cheapest tests:** the EXP148 three-arm design (B: T_B=15; C, S: T=120 budget-matched) on a fresh transitive-only bench, 2 strata × 380 items = 760 items, frozen Pythia-410m, greedy, Δθ=0. Preceded by the binding stratified Step-0 gate and the registered bench-size STOP rule (pilot AND first-block keying).
4. **Cost:** $0 CPU. **193,800 (generation) + 600 (stratified dry run) + 4,800 (C+S pilot) = 199,200 ≤ guard (g) 200k.** Wall ≈ 9h at EXP148 rates — re-gated at Step 0 (guard (h) ≤ 72h). [NOTE]: design cost sits at 99.6% of the 200k cap (800 forwards of headroom) — razor-thin by construction; the bench-size STOP rule and Step-0 re-assertion cover overruns (a computation, not a choice).
5. **Mathematical license:** EXP148/EXP149/EXP150 pre-reg §§2–3 inherited unchanged — (a) first-token scoring [DEFINITION]; (b) WRITE/READ discipline definition [DEFINITION]; (c) budget-matched CoT control [DEFINITION] with guard (f′) earning the "budget-matched" label; (d) the McNemar decision machinery [DEFINITION] with the S7-1 §2.2 Wald convention (SE = √[(b+c) − (b−c)²/n]/n).
6. **Quantitative predictions:** if depth-driven on transitive: δ̂_T3 − δ̂_T2 ≥ +0.10. If the breaking point holds: δ̂_T3 − δ̂_T2 ≤ 0. **Power licenses:** §2 — the registered true-power band is [0.74, 0.88] over the design d-range [0.30, 0.40]; the bench-size STOP floor is the band floor **0.74**; whether to run at the §2 zero-margin is the CEO's Law #15 call (registered honestly here; the call is not this document's).
7. **Breaking points:** §0 — plus the binding stratified Step-0 gate (§5.4): a (d-T*) trip STOPS the study at design cost (no full run, no verdict); a Step-0 registered power < 0.74 (pilot keying) STOPS at design cost; a first-full-run-block registered power < 0.74 (block keying) STOPS at that point — all logged HELD (computations, not choices).

**Why this is worth doing [INTERPRETATION]:** the primary is the cleanest remaining test of whether the program's first capability entry is depth-driven — asked on strata where a gain is in principle measurable, with the bench now priced to supply the design's own power bar at the observed discordant rate. A KILL is a sharp boundary (pooled/headroom-driven gain, not depth-driven); a CONTINUE genuinely extends the entry with a depth axis. A HELD closes the apparatus line honestly and finally.

---

## 2. Power analysis [FACT]

Per-level net δ̂_h = (b_h − c_h)/n_h; primary θ = δ̂_T3 − δ̂_T2; Wald SE(θ) = √[SE(δ̂_T3)² + SE(δ̂_T2)²], SE(δ̂_h) = √[(d_h − δ̂_h²)/n_h] (S7-1 §2.2 convention, carried). EXP148 realized per-level SE = 0.0412 at n=180 (b=52, c=12, d=0.3556).

**Design value [DEFINITION]:** n_T2 = n_T3 = 380 per hop level, fixed by the registered bench (2 transitive strata × 380 items, §5.1). EXP150's power table (n=190) does not transfer. Recomputed for the registered bench (this packet's independent recomputation): at d = 0.30–0.40, SE(θ) = 0.0370–0.0435, power **0.74–0.88** for δ = +0.10, one-sided α = 0.05 — the registered true-power band is **[0.74, 0.88]**. Power table (δ=+0.10, one-sided α=0.05): (d=0.30, net=0.20) → SE 0.0370, power 0.855; (d=0.32, net=0.20) → SE 0.0384, power 0.832; (d=0.36, net=0.20) → SE 0.0410, power 0.786; (d=0.40, net=0.20) → SE 0.0435, power 0.743; (d=0.30, net=0.25) → SE 0.0354, power 0.882. (Recomputation: SE √[(d−net²)(2/380)], power Φ(0.10/SE−1.645).) The design d-range [0.30, 0.40] extends EXP150's [0.30, 0.36] to include the EXP150 d_block1 = 0.40 datum — the effect is priced, not guessed (Law #9 satisfied: the datum is a design input, not a test target).

**Zero-margin flag [FACT]:** at the observed datum d = 0.40, registered power = 0.7429 — clears the band floor 0.74 by 0.003. The design is exactly powered at the observed discordant rate, with no headroom. Registered honestly here; the Law #15 call is the CEO's.

**Registered Step-0 power rule [DEFINITION] (carried from EXP150's Fix E3, re-keyed to the design n=380 per LOG-4977 constraint (4)):** at Step 0 the execution lane computes registered Wald-formula power — Φ(0.10/SE(θ) − 1.645) with SE(θ) = √[(d_src − 0.10²)(2/380)] — from the registered discordant-pair rate d_src, for δ = +0.10, one-sided α = 0.05, at the bench's fixed n_T2 = n_T3 = 380. **Registered d_src, in precedence order:** (1) the 20-item C+S pilot discordant-pair rate d_pilot = (b+c)/20 on the pilot's S−C correctness pairs, drawn from the **transitive** strata (§5.4) — the planning input; (2) the first 20-item C+S block of the full run, d_block1 — the operative re-keying. **Bench-size outcome [DEFINITION]:** if the registered power < 0.74 (the true-power band floor) at EITHER keying, the study STOPS — at design cost for the pilot keying, at that point for the block keying — logged HELD (the bench cannot supply even the design's own power bar; a computation, not a choice). The achieved power governs CONTINUE probability, not KILL validity: the CI-entirely-≤-0 KILL bar with false-KILL 0.025 under δ=0 is intact and fails safe to HELD.

**KILL-bar operating characteristics (carried):** under δ = 0, P(95% CI entirely ≤ 0) = 0.025 (remainder is HELD — the design fails safe); under true δ = +0.10, false-KILL < 1e-4; under true δ = −0.10 (reverse dose-response), P(KILL fires) ≈ **0.63–0.77** (recomputed at n=380: Φ(0.10/0.0370 − 1.96) ≈ 0.77 at d=0.30; Φ(0.10/0.0435 − 1.96) ≈ 0.63 at d=0.40).

---

## 3. Frozen decision bars (verbatim from EXP148 pre-reg §3, applied to the transitive primary)

- Paired per-item correctness under §5.3 scoring. KILL = conjunction: (i) one-sided McNemar (H1: S>C) p ≥ 0.1, AND (ii) two-sided McNemar p ≥ 0.1, AND (iii) 95% Wald CI for net δ̂=(b−c)/n entirely below +0.10 (upper < +0.10).
- PIVOT: KILL fires AND transitive-3hop S vs B one-sided McNemar (H1: S>B) p < 0.05 — test-time compute helps at depth but discipline doesn't (carried verbatim per the registered carry rule; CEO disposition A1/LOG-4968 applies).
- CONTINUE: one-sided p < 0.05 AND net δ̂ ≥ +0.10.
- KILL is scoped: "the discipline gain does not grow with hops on the transitive strata" — it neither rules out sub-10pp depth effects nor says anything about the compositional strata.

---

## 4. Decision tables (binding)

**Registered composition rule [DEFINITION] (carried from EXP150's Fix E4):** §4's decision table is the sole binding verdict machinery for this packet's primary; §3's per-level KILL/CONTINUE conjunctions are superseded for the primary verdict and retained only as the source definitions for the CONTINUE table's transitive-3hop S−C clause and the PIVOT condition, both restated in §4.

Precedence: RUN-INVALID > HELD > KILL > CONTINUE. The stratified Step-0 gate (§5.4) precedes the full run. There is no secondary — no compositional strata, no descriptive pilot, no secondary decision table (design-record §5.1).

### 4. Primary — transitive-only hop dose-response

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | 95% CI for (δ̂_T3 − δ̂_T2) entirely above 0 AND transitive-3hop S−C one-sided (H1: S>C) p < 0.05 | Dose-response supported on transitive strata: the discipline gain grows with reasoning depth; the capability entry gains a (transitive-scoped) depth axis |
| KILL | 95% CI for (δ̂_T3 − δ̂_T2) entirely ≤ 0, with per-level guards (d_s),(e),(f),(f′) PASS | Dose-response dead on transitive strata: the gain does not grow with hops there — it is pooled/headroom-driven. EXP148's CONTINUE stands as a pooled effect, not a depth effect |
| PIVOT | KILL fires AND (per-level) S vs B one-sided (H1: S>B) p < 0.05 on transitive-3hop | (Alongside KILL) Test-time compute helps at depth but discipline doesn't — pivot to test-time-compute scaling |
| HELD | Anything else (CI too wide, any per-level guard (d_s) or (f′) trips, either power keying < 0.74) | Inconclusive — **terminal for this line** (no further re-attempt licensed; a second HELD is a design-debt finding) |
| RUN-INVALID | Any per-level apparatus guard (a)/(c)/(e)/(f)/(g)/(h) trips | Apparatus failure — never a verdict |

---

## 5. Protocol

### 5.1 Bench [DEFINITION]

**Fresh bench, registered construction:** 2 transitive strata × 380 items = 760 items — transitive-2hop, transitive-3hop (transitive recipe carried from EXP147/148 §5.1, the measured instrument). Construction seed **151001** (≠ 149001, ≠ 150001). Closed 40-entity pool; entity-disjoint exemplars (Law #7); golds single entity names, ≥2× per the EXP148 recipe. Bench pin recomputed character-identical (64/64) at Step 0 before any forward (guard (c)). Never transcribed. Golds used only at scoring (§5.3).

**Design-record [FACT, LOG-4973]:** hardened-compositional is excluded — validity constraints (v2)/(v4) are jointly unsatisfiable on the registered model+pool. No hardened-compositional strata, gates, or statistics are registered. Its reconciliation is a deferred, unlicensed lane.

### 5.2 Arms and prompts (carried verbatim from the EXP150 pre-reg §5.2)

- **Model:** frozen Pythia-410m. Greedy decoding (do_sample=False), Δθ=0. Model revision resolved programmatically at Step 0 from the local cache (expectation `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` — carried, re-resolved not transcribed).
- All arms 2-shot (shot-count controlled). **B:** `Context: {facts}\nQuestion: {question}\nAnswer with the name only.\nAnswer: …` — T_B=15. **C:** `Context: {facts}\nQuestion: {question}\nThink step by step. Give the final answer after "ANSWER:".` — T=120. **S:** `Context: {facts}\nQuestion: {question}\nUse the scratchpad. WRITE each deduced fact as WRITE(fact1, ...), WRITE(fact2, ...). When you need a fact, READ it: READ(fact1). Give the final answer after "ANSWER:".` — T=120 (same T as C — the compute-confound fence).
- **Exemplars:** reuse the EXP148 Step-0-pinned exemplar file byte-identical. If unavailable at execution, rebuild by the S7-1 §5.2 construction procedure (two worked 2-hop items per arm, entity-disjoint from the bench) and record the new pin. Either way, exemplar text is committed before any bench forward.

### 5.3 Scoring (registered, deterministic — EXP150 pre-reg §5.3 verbatim)

1. **B arm:** full generation → normalize (lowercase, strip punctuation, collapse whitespace) → FIRST whitespace-delimited token → exact match vs normalized gold → 1, else 0.
2. **C/S arms:** text after the LAST `ANSWER:` → normalize → FIRST whitespace-delimited token → exact match vs gold → 1, else 0. No `ANSWER:` → 0 (no post-hoc rescue).
3. Primary metric: per-item correctness per arm. All verdict statistics are paired McNemar on (S, C) and (S, B) correctness pairs — the primary additionally the difference of the two per-level transitive S−C nets. No LLM judge (Law #13).

### 5.4 Step-0 guards and gates (binding — precede the full run)

**Shared:**
- **(u0) Scoring-pipeline unit test** (zero forwards): the C/S `ANSWER:`-parsing path asserted on synthetic strings (standard/lowercase/multiple-ANSWER:/trailing-rambling/missing→0) → else RUN-INVALID.
- **(a) Δθ=0:** pre/post state-dict hash equality.
- **(b) Model revision:** resolved programmatically; expectation carried (§5.2).
- **(c) Bench pin:** recomputed character-identical (64/64) before any forward.
- **(d_s) Stratified calibration gate (licensed repair (i)):** 20 fresh items per stratum × 2 transitive strata = 40 items (subset seed = construction_seed + 11 = **151012**, registered at design — the A2 seed-derivation rule: no execution-time choice), B arm only, T_B=15, greedy, §5.3 scoring.
  - **(d-T2)/(d-T3):** transitive-2hop / transitive-3hop B accuracy ∈ [0.2, 0.8] [ASSUMPTION — registered] → else the study STOPS at design cost (600 + 4,800 + build forwards), logged HELD — the primary is unmeasurable.
- **(e) Discipline delivered:** ≥50% of S generations contain ≥1 well-formed `WRITE\(fact\d+,` span (regex on raw generation) → else RUN-INVALID. [NOTE]: WRITE-only by design; READ efficacy is efficacy, not delivery.
- **(f) Compute delivered:** mean_tokens(C) > 2 × mean_tokens(B) AND mean_tokens(S) > 2 × mean_tokens(B) → else RUN-INVALID. [ASSUMPTION — 2× registered.]
- **(f′) Budget matched:** mean_tokens(S)/mean_tokens(C) ∈ [2/3, 3/2] — per hop level → else HELD. [ASSUMPTION — band registered.]
- **(g) Budget audit:** total generation forwards ≤ 200k.
- **(h) Compute gate:** throughput probe (50 generation steps, fixed dummy prompt, excluded from benches) at Step 0; projected full-run ≤ 72h → else INCONCLUSIVE (compute-infeasible). Never self-escalate to GPU. [ASSUMPTION — 72h registered.]

**C+S pilot (registered, carried — Fix D8):** a separate fresh 20-item subset drawn from the **transitive** strata (pilot seed = construction_seed + 23 = **151023**, registered at design), C and S arms only (T=120, greedy, §5.3 scoring), cost 20×240 = 4,800 generation forwards. Its S−C discordant-pair rate d_pilot = (b+c)/20 is the registered Step-0 planning input for the §2 power rule (pilot keying); the first 20-item C+S block of the full run supplies d_block1 (block keying). **Both keyings are registered** (LOG-4977 constraint (4)); either < 0.74 stops the study.

**4-hop:** not re-registered (out of scope; a new numbered experiment, not a quiet addition).

**Descriptive reporting (not guards):** B-arm format compliance; mean extra-token counts; per-level WRITE-span rates (descriptive — Law #9, no stratum promoted to a decision).

### 5.5 Cost

$0 CPU. 193,800 (generation: 760 items × 255) + 600 (stratified dry run) + 4,800 (C+S pilot) = **199,200 ≤ guard (g) 200k**. **Margin note [NOTE]:** design cost sits at 99.6% of the 200k cap (800 forwards of headroom) — razor-thin by construction; the bench-size STOP rule and Step-0 re-assertion cover overruns (a computation, not a choice). Wall-time asserted at Step 0 per guard (h), never in advance (Law #2).

### 5.6 Determinism (Law #13)

Bench construction seed **151001** registered at design. Dry-run subset seed 151012 (= 151001 + 11), pilot subset seed 151023 (= 151001 + 23) — the registered seed-derivation rule (A2 advisory implemented): every subset seed is a fixed registered offset from the construction seed; no execution-time seed choice exists. Generation seeds fixed per arm, registered; greedy decoding; model revision 40-hex pinned at Step 0 from cache; environment manifest recorded (same CPU stack family as EXP148/149/150 — re-recorded, not assumed). Per-item records flushed per write. Weights loaded from local caches only — no HF Hub contact at execution.

---

## 6. Material uncertainties

1. **Zero margin at the priced rate:** the registered bench-size rule keys to the band floor 0.74; at the EXP150 d_block1 = 0.40 datum the registered power is 0.7429 — a 0.003 margin. Any pilot/block rate above 0.40 stops the study. The design is exactly powered at the observed discordant rate. Whether this margin is acceptable is the CEO's Law #15 call.
2. **The literal-4×380 discrepancy:** the LOG-4977 prose "4 strata × 380" prices 393,000 > guard (g) (computed in the companion design draft §2). This draft carries the 2-strata × 380 configuration delivering the ruling's operative n=380/hop-level at 199.2k. CEO disposition LOG-4979: the 2-strata 760-item design is accepted; the LOG-4977 prose was a transcription error; guard (g) needs no amendment. [Fix E1, Law #14 review 2026-10-09.]
3. **Reverse dose-response:** if δ̂_T3 − δ̂_T2 < 0 with a tight CI, the KILL fires (operating characteristics §2) — and a strong reverse pattern is itself a finding (headroom-driven gain), reported descriptively.
4. **Second-HELD terminality:** a HELD here licenses no further re-attempt — the apparatus line stands down. This is a registered terminal condition, not a suggestion.
5. **Prior-data honesty:** the design d-range [0.30, 0.40] prices the EXP150 block datum; the test runs on a fresh bench — Law #9 is satisfied by construction, and this registration makes the pricing auditable.

**Mandatory EXP148 caveats travel with any report of results:** direct answering still beat WRITE/READ (S vs B −0.2500); this tests prompting discipline, not autonomous steering; single model, single bench family; no consciousness or superhuman-cognition claim.

---

## Fixes applied (Law #14 review repair lane, 2026-10-09)

- **E1:** operative-text "[For CEO disposition]" flag in pre-reg §6 item 2 (the literal-4×380 discrepancy) converted to the recorded disposition — CEO disposition LOG-4979: the 2-strata 760-item design is accepted; the LOG-4977 prose was a transcription error; guard (g) needs no amendment. Edited paragraph marked [Fix E1, Law #14 review 2026-10-09]. (Independently re-verified this lane: no "[For CEO disposition]" markers remain in operative text.)

---

*Pre-registration draft finalized 2026-10-09 (Law #15 packet lane; license LOG-4977). Status: DRAFT — NOT SIGNED. NOT EXECUTED. NO NUMBER MINTED. No forwards run. Companion: `EXP151_DESIGN_DRAFT_2026-10-09.md`. Awaited: independent Law #14 review of both drafts → CEO Law #15 SIGN-and-mint → execution authorization (Step-0 gates first). Execution NOT licensed by this document.*
