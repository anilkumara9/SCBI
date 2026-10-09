# EXP149 Pre-registration — DRAFT: EXP148 follow-ups — hop dose-response (Pythia-410m) and cross-family prompting-discipline generality (GPT-2-small) at Δθ=0

**Status: DRAFT — NOT SIGNED. NOT EXECUTED.** This pre-registration drafts the two death-debt candidates from the Friday cull (`EXP149_DESIGN_DRAFT_2026-10-09.md`, LOG-4965) for the CEO-minted experiment number EXP149 (LOG-4967). It awaits independent Law #14 review and CEO sign + execution authorization. No forwards have been run under this number.

**Drafting lane:** EXP149 innovation-sprint design, 2026-10-09. **Experiment number EXP149 minted by the CEO** (LOG-4967) — new operationalization = new number per the single-lane fence; EXP148's CONTINUE verdict stands untouched.

**Parent context [FACT]:** EXP148 (J7) CONTINUE ADOPTED (LOG-4958/4959; independent verdict review ADOPT, LOG-4960): frozen Pythia-410m, WRITE/READ prompting discipline beat budget-matched CoT by net +22.2pp (b=52, c=12, one-sided McNemar p=2.2833e-07, 95% Wald CI (0.1414, 0.3031)). Mandatory caveats: S vs B net −0.2500 (direct answering still beats WRITE/READ); discipline gain, not autonomous steering; single model, single bench. LOG-4965 licensed exactly two follow-ups: (a) hop dose-response; (b) cross-family generality within the EXP145 bound.

**The EXP145 bound [FACT — scope fence]:** EXP145's KILL/PIVOT (LOG-4925/4926) bounded the Decodability Gap's *shared-direction instrument* to Pythia-scale (GPT-2-small: D1 PASS, D2 mean shared-direction cosine −0.4587 vs 0.70 bar; decode+ precondition absent; architecture vs scale/bench-fit unseparated). EXP149 tests a **different object** — an inference-time prompting-discipline *capability gain* — and re-opens nothing: candidate (b)'s generality claim is scoped to the WRITE/READ discipline effect on its own pre-registered bars, with EXP144's bench-portability lesson enforced by the binding Step-0 portability gate (§5.4(b)). No Gap-generality claim is licensed by anything in EXP149.

**Governing laws:** Law #2 (every constant below is pinned, computed, or carried from a signed artifact — never improvised), Law #4 (no post-hoc hypothesis shifts), Law #6 (Δθ=0), Law #7 (bench golds never touch prompts), Law #9 (primaries registered here, before any new output is inspected — EXP148's descriptive stratum nets are prior observations and motivation, not test targets; stratum breakdowns descriptive only), Law #11 (labels throughout), Law #13 (determinism), Law #15 (worth-it gate §1).

**Epistemological labels** per `~/workspace/SCBI/AGENTS.md` §5 are load-bearing below. [NOTE] and [CAVEAT] mark operational clarifications.

---

## 0. The questions

**Study (a) — hop dose-response [HYPOTHESIS]:** The WRITE/READ discipline advantage over budget-matched CoT scales with reasoning depth: net(S−C) at 3-hop exceeds net(S−C) at 2-hop — δ̂_3 − δ̂_2 > 0, on frozen Pythia-410m, with a fresh bench.

**Breaking point (a):** 95% CI for (δ̂_3 − δ̂_2) entirely ≤ 0, with per-level guards (d),(e),(f),(f′) PASS → **KILL** the dose-response claim (the gain does not grow with hops; EXP148's CONTINUE stands as a pooled effect, not a depth effect).

**Study (b) — cross-family generality [HYPOTHESIS]:** The WRITE/READ discipline advantage over budget-matched CoT is not Pythia-specific: on frozen GPT-2-small, S vs C one-sided McNemar (H1: S>C) p < 0.05 AND net δ̂ ≥ +0.10 → CONTINUE (generality supported, scoped to these two families).

**Breaking point (b):** the EXP148 KILL conjunction mirrored on GPT-2-small — (i) one-sided p ≥ 0.1 AND (ii) two-sided p ≥ 0.1 AND (iii) 95% CI upper < +0.10, with guards (d),(e),(f′) PASS → **KILL** the generality claim (the discipline gain does not transfer to GPT-2-small; EXP148's capability entry stands as Pythia-scale). [CAVEAT]: a KILL here records scoped non-transfer only — it does not adjudicate architecture vs scale vs bench-fit (the EXP145 §1 steelman applies symmetrically).

**Scope fence [DEFINITION]:** EXP149 tests (a) depth-dependence and (b) prompting-discipline family-generality **only**, at Δθ=0, no fine-tuning. It licenses no Gap claim, no steering claim, no claim about other families or scales. Whatever fires here *scopes* EXP148's CONTINUE; nothing overturns it.

**What this pre-registration does not do:** it does not re-litigate EXP148 (CONTINUE stands); it does not reopen or re-read EXP145 (KILL/PIVOT stands); it does not change the models, the arms, the prompts, the budgets, or the scoring; it does not touch the paper or any killed lane; it does not license execution (independent review SIGN + CEO authorization still required).

---

## 1. Worth-it gate (Law #15, 7 points)

1. **Exact questions [HYPOTHESIS]:** §0 — (a) is the discipline gain depth-driven (δ̂_3 > δ̂_2)? (b) is it family-general (replicates on frozen GPT-2-small)?
2. **Decisions changed:**
   - **Study (a):** CONTINUE (§4a): 95% CI for (δ̂_3 − δ̂_2) entirely above 0 AND 3-hop S−C one-sided p < 0.05 → dose-response supported, the capability entry gains a depth axis. KILL (§4a): CI entirely ≤ 0 with per-level guards (d),(e),(f),(f′) PASS → gain is pooled/headroom-driven, not depth-driven. HELD (§4a): anything else. RUN-INVALID (§4a): apparatus guard trip — never a verdict.
   - **Study (b):** CONTINUE (§4b): S vs C one-sided p < 0.05 AND net δ̂ ≥ +0.10 → generality supported (two-family scope). KILL (§4b): the three-prong conjunction with guards (d),(e),(f′) PASS → generality dead; Pythia-scale entry. HELD (§4b): anything else, **including any Step-0 portability-gate trip (p1)/(p2)/(p3)** — a measurement boundary, not a verdict. RUN-INVALID (§4b): apparatus guard trip — never a verdict.
3. **Cheapest tests:** (a) the EXP148 three-arm design (B: T_B=15; C, S: T=120 budget-matched) on a fresh 2-hop/3-hop bench, n=380/level, frozen Pythia-410m, greedy, Δθ=0. (b) the EXP148 three-arm design byte-identical on the parent bench, n=180, frozen GPT-2-small, greedy, Δθ=0. Both preceded by binding Step-0 gates.
4. **Cost:** $0 CPU. (a) ≈ 193.8k generation forwards + ≈ 300 B dry-run forwards + 4,800 C+S pilot forwards = 198.9k ≤ guard (g) 200k [Fix D8]. (b) ≈ 45.9k forwards + ≈ 2.7k portability-pilot forwards = 48.6k ≤ guard (g) 50k [Fix D3]. Wall: (a) ≈ 8.8h, (b) ≈ 2.1h at EXP148 rates — re-gated at Step 0 (guard (h) ≤ 72h each).
5. **Mathematical license:** EXP148 pre-reg §§2–3 inherited unchanged — (a) first-token scoring [DEFINITION]; (b) WRITE/READ discipline definition [DEFINITION]; (c) budget-matched CoT control [DEFINITION] with guard (f′) earning the "budget-matched" label; (d) the McNemar decision machinery [DEFINITION] with the S7-1 §2.2 Wald convention (SE = √[(b+c) − (b−c)²/n]/n).
6. **Quantitative predictions:** (a) if depth-driven: δ̂_3 − δ̂_2 ≥ +0.10. If the breaking point holds: δ̂_3 − δ̂_2 ≤ 0. (b) if family-general: S−C net ≥ +0.10 on GPT-2-small (one-sided p < 0.05). If the breaking point holds: S−C ≈ 0 with discipline delivered. **Power licenses:** §2.
7. **Breaking points:** §0 — plus the binding Step-0 gates (§5.4): (a) the dry-run calibration gate; (b) the portability gate (p1)/(p2)/(p3). A gate trip STOPS the study at design cost — no full run, no verdict; the stop is logged.

**Why this is worth doing [INTERPRETATION]:** (a) decides whether the program's first capability entry is depth-driven or pooled — the highest-value structural question the CONTINUE verdict leaves open, and a risky directional bet the prior descriptive data leans against. (b) decides whether the entry is a Pythia-scale phenomenon or a family-general prompting principle — with the EXP145 bound keeping the claim honest. Clean KILLs on either are sharp boundaries; a CONTINUE on either genuinely extends the entry. HELDs cost only design compute.

---

## 2. Power analysis [FACT]

### 2.1 Study (a): difference of two independent S−C nets

Per-level net δ̂_h = (b_h − c_h)/n_h; primary θ = δ̂_3 − δ̂_2; Wald SE(θ) = √[SE(δ̂_3)² + SE(δ̂_2)²], SE(δ̂_h) = √[(d_h − δ̂_h²)/n_h] (S7-1 §2.2 convention). EXP148 realized per-level SE = 0.0412 at n=180 (b=52, c=12, d=0.3556).

| d per level | net per level | n/level | SE(θ) | Power (δ=+0.10, 1-sided α=0.05) |
|---|---|---|---|---|
| 0.30 | 0.20 | 380 | 0.0370 | 0.86 |
| 0.32 | 0.20 | 380 | 0.0384 | 0.83 |
| 0.36 | 0.20 | 380 | 0.0410 | 0.79 |
| 0.30 | 0.25 | 380 | 0.0354 | 0.88 |

**Registered power rule [DEFINITION]:** n = 380 per hop level is the design value. At Step 0 the execution lane computes registered Wald-formula power — Φ(0.10/SE(θ) − 1.645) with SE(θ) = √[(d_src − 0.10²)(1/n_3 + 1/n_2)] — from the registered discordant-pair rate d_src, for δ = +0.10, one-sided α = 0.05. If registered power < 0.80, n per level is raised to the smallest even integer with registered power ≥ 0.80 — a computation, not a choice (Law #2). **Registered d_src, in precedence order [Fix D8, Law #14 review 2026-10-09]:** (1) the 20-item C+S pilot discordant-pair rate d_pilot = (b+c)/20 on the pilot's S−C correctness pairs (§5.4); (2) EXP148's realized d = 0.3556 carried as the planning sanity-check value, keyed to the first 20-item C+S block of the full run: if the first-block rate d_block1 implies a higher n than the pilot-based n, the lane raises to the d_block1-implied n (smallest even integer by the same formula) before completing the block's remaining items — a computation, not a choice.

**Registered n-raise guard re-assertion [DEFINITION]:** after any n-raise computation, the execution lane re-projects total generation forwards and wall time at Step 0 at the raised n (per-arm costs §5.5, EXP148 rates). If the raised n would violate guard (g) (≤ 200k forwards, study (a)) or guard (h) (≤ 72h wall), study (a) STOPS at design cost — logged HELD. A computation, not a choice. [Fix D5, Law #14 review 2026-10-09.]

**KILL-bar operating characteristics:** under δ = 0, P(95% CI entirely ≤ 0) = 0.025 (remainder is HELD — the design fails safe); under true δ = +0.10, false-KILL < 1e-4; under true δ = −0.10 (reverse dose-response), P(KILL fires) ≈ 0.77. [Fix D2, Law #14 review 2026-10-09.]

### 2.2 Study (b): S vs C on GPT-2-small

Same scoring, same test, n = 180 — the S7-1/EXP148 license transfers unchanged:

- CONTINUE-bar power: n=180 clears 80% at +10pp for d ≤ 0.30 (MDE80 ≈ +10pp); at d=0.35 power 0.70.
- KILL-bar: fires 65–88% under true null (d ∈ [0.20, 0.35]); false-KILL < 3% at true +10pp; false-CONTINUE ≤ 0.035.

**[CAVEAT]:** the power license assumes the GPT-2-small discordant-pair rate d falls in [0.20, 0.35]. If the Step-0 pilot suggests d outside this band, the execution lane reports it and the CEO decides (no silent n change — Law #2).

---

## 3. Frozen decision bars (verbatim from EXP148 pre-reg §3, applied per study)

- Paired per-item correctness under §5.3 scoring. KILL = conjunction: (i) one-sided McNemar (H1: S>C) p ≥ 0.1, AND (ii) two-sided McNemar p ≥ 0.1, AND (iii) 95% Wald CI for net δ̂=(b−c)/n entirely below +0.10 (upper < +0.10).
- PIVOT: KILL fires AND S vs B one-sided McNemar (H1: S>B) p < 0.05 — test-time compute helps, discipline doesn't.
- CONTINUE: one-sided p < 0.05 AND net δ̂ ≥ +0.10.
- KILL is scoped: "discipline adds nothing *over budget-matched CoT*" (study (b)) / "the gain does not grow with hops" (study (a)) — neither rules out sub-10pp effects or architectural writable memory.

---

## 4. Decision tables (binding)

Precedence per study: RUN-INVALID > HELD > KILL > CONTINUE. PIVOT attaches to KILL when its condition holds. The Step-0 gates (§5.4) precede each study's full run: a gate trip STOPS the study — no full run, no verdict, the stop is logged.

### 4a. Study (a) — hop dose-response

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | 95% CI for (δ̂_3 − δ̂_2) entirely above 0 AND 3-hop S−C one-sided (H1: S>C) p < 0.05 | Dose-response supported: the discipline gain grows with reasoning depth; the capability entry gains a depth axis |
| KILL | 95% CI for (δ̂_3 − δ̂_2) entirely ≤ 0, with per-level guards (d),(e),(f),(f′) PASS | Dose-response dead: the gain does not grow with hops — it is pooled/headroom-driven. EXP148's CONTINUE stands as a pooled effect, not a depth effect |
| PIVOT | KILL fires AND (per-level) S vs B one-sided (H1: S>B) p < 0.05 on the 3-hop level | (Alongside KILL) Test-time compute helps at depth but discipline doesn't — pivot to test-time-compute scaling |
| HELD | Anything else (CI too wide, any per-level guard (d) or (f′) trips) | Inconclusive — licenses nothing, kills nothing |
| RUN-INVALID | Any per-level apparatus guard (a)/(c)/(e)/(f)/(g)/(h) trips | Apparatus failure — never a verdict |

### 4b. Study (b) — cross-family generality (GPT-2-small)

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | S vs C one-sided (H1: S>C) p < 0.05 AND net δ̂ ≥ +0.10 | Generality supported: the WRITE/READ discipline gain replicates on frozen GPT-2-small — a two-family prompting principle |
| KILL | S vs C: (i) one-sided p ≥ 0.1, AND (ii) two-sided p ≥ 0.1, AND (iii) 95% CI upper < +0.10; guards (d),(e),(f′) PASS | Generality dead: the gain does not transfer to GPT-2-small; EXP148's capability entry stands as Pythia-scale |
| PIVOT | KILL fires AND S vs B one-sided (H1: S>B) p < 0.05 | (Alongside KILL) Test-time compute transfers but discipline doesn't |
| HELD | Anything else, **including any Step-0 portability-gate trip (p1)/(p2)/(p3)** | Measurement boundary (EXP147 precedent) — licenses nothing, kills nothing; a portability failure is never a KILL |
| RUN-INVALID | Any apparatus guard (a)/(c)/(e)/(f)/(g)/(h) trips | Apparatus failure — never a verdict |

---

## 5. Protocol

### 5.1 Benches [DEFINITION]

**Study (a) — fresh bench, same procedure:** templatic construction per the EXP147/148 §5.1 recipe (closed entity pool, every gold a single entity token appearing ≥2×, entity-disjoint exemplars — Law #7), two hop levels (2-hop, 3-hop) × two strata (transitive, compositional) × 190 items = 760 items. Construction seed registered at execution (≠ 7101). Bench pin recomputed character-identical (64/64) at Step 0 before any forward (guard (c)). Never transcribed. Golds used only at scoring (§5.3).

**Study (b) — parent bench reused byte-identical:** the EXP148 bench (pin `2b055b53127a241b72338a82373c3efc7b666256e25d8c584d45989278c14dcf`) recomputed character-identical (64/64) at Step 0 **if** portability gate (p1) passes. **(p1)-fail branch (pre-registered):** rebuild the bench by the EXP147 §5.1 procedure with a GPT-2-BPE-safe entity pool (single-token golds under GPT-2 BPE *by construction*), new seed registered at execution, new pin recorded. Pre-registered branch, not a choice. The rebuilt bench is re-verified against (p1) at Step 0 (≥ 0.95 required) before any full-run forward; if the re-verification fails, study (b) STOPS at design cost, logged HELD. [Fix D9, Law #14 review 2026-10-09.]

### 5.2 Arms and prompts (carried verbatim from the EXP148 pre-reg §5.2 — both studies)

- **Models:** (a) frozen Pythia-410m; (b) frozen GPT-2-small. Greedy decoding (do_sample=False), Δθ=0. Model revisions resolved programmatically at Step 0 from the local caches (expectations: Pythia-410m `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`; GPT-2-small `607a30d783dfa663caf39e06633721c8d4cfcd7e` — carried, re-resolved not transcribed).
- All arms 2-shot (shot-count controlled). **B:** `Context: {facts}\nQuestion: {question}\nAnswer with the name only.\nAnswer: …` — T_B=15. **C:** `Context: {facts}\nQuestion: {question}\nThink step by step. Give the final answer after "ANSWER:".` — T=120. **S:** `Context: {facts}\nQuestion: {question}\nUse the scratchpad. WRITE each deduced fact as WRITE(fact1, ...), WRITE(fact2, ...). When you need a fact, READ it: READ(fact1). Give the final answer after "ANSWER:".` — T=120 (same T as C — the compute-confound fence).
- **Exemplars:** reuse the EXP148 Step-0-pinned exemplar file byte-identical. If unavailable at execution, rebuild by the S7-1 §5.2 construction procedure (two worked 2-hop items per arm, entity-disjoint from the bench) and record the new pin. Either way, exemplar text is committed before any bench forward.

### 5.3 Scoring (registered, deterministic — EXP148 pre-reg §5.3 verbatim, both studies)

1. **B arm:** full generation → normalize (lowercase, strip punctuation, collapse whitespace) → FIRST whitespace-delimited token → exact match vs normalized gold → 1, else 0.
2. **C/S arms:** text after the LAST `ANSWER:` → normalize → FIRST whitespace-delimited token → exact match vs gold → 1, else 0. No `ANSWER:` → 0 (no post-hoc rescue).
3. Primary metric: per-item correctness per arm. All verdict statistics are paired McNemar on (S, C) and (S, B) correctness pairs — study (a)'s primary additionally the difference of the two per-level S−C nets. No LLM judge (Law #13).

### 5.4 Step-0 guards and gates (binding — precede each study's full run)

**Shared (both studies):**
- **(u0) Scoring-pipeline unit test** (zero forwards): the C/S `ANSWER:`-parsing path asserted on synthetic strings (standard/lowercase/multiple-ANSWER:/trailing-rambling/missing→0) → else RUN-INVALID.
- **(a) Δθ=0:** pre/post state-dict hash equality.
- **(b) Model revision:** resolved programmatically; expectations carried (§5.2).
- **(c) Bench pin:** recomputed character-identical (64/64) before any forward.
- **(d) Calibration:** first-token B accuracy ∈ [0.2, 0.8] — **per hop level** for (a); pooled for (b) → else HELD (bench degenerate *for this measurement*).
- **(e) Discipline delivered:** ≥50% of S generations contain ≥1 well-formed `WRITE\(fact\d+,` span (regex on raw generation) → else RUN-INVALID. [NOTE]: WRITE-only by design; READ efficacy is efficacy, not delivery.
- **(f) Compute delivered:** mean_tokens(C) > 2 × mean_tokens(B) AND mean_tokens(S) > 2 × mean_tokens(B) → else RUN-INVALID. [ASSUMPTION — 2× registered.]
- **(f′) Budget matched:** mean_tokens(S)/mean_tokens(C) ∈ [2/3, 3/2] — per hop level for (a) → else HELD. [ASSUMPTION — band registered.]
- **(g) Budget audit:** total generation forwards ≤ 200k for (a); ≤ 50k for (b).
- **(h) Compute gate:** throughput probe (50 generation steps, fixed dummy prompt, excluded from benches) at Step 0; projected full-run ≤ 72h per study → else INCONCLUSIVE (compute-infeasible). Never self-escalate to GPU. [ASSUMPTION — 72h registered.]

**Study (a) dry-run gate (binding):** fresh 20-item subset of the NEW bench (subset seed registered at execution, ≠ construction seed), B arm only, T_B=15, greedy, §5.3 scoring. **Pass:** B accuracy ∈ [0.2, 0.8] → full run licensable (pending independent review SIGN + CEO execution authorization). **Fail:** study (a) STOPS at design cost (~300 forwards); no full run, no verdict; the stop is logged and licenses the bench-repair proposal.

**C+S pilot (registered [Fix D8, Law #14 review 2026-10-09]):** a separate fresh 20-item subset (pilot seed registered at execution, ≠ construction seed, ≠ B dry-run subset seed), C and S arms only (T=120, greedy, §5.3 scoring), cost 20×240 = 4,800 generation forwards — study (a) design cost 193,800 + 300 + 4,800 = 198,900 ≤ guard (g) 200k. Its S−C discordant-pair rate d_pilot = (b+c)/20 on the pilot's S−C correctness pairs is the registered Step-0 planning input for the §2.1 power rule.

**Study (b) portability gate (binding — EXP144 lesson):**
- **(p1) Tokenizer portability:** fraction of bench golds that are single tokens under GPT-2 BPE ≥ 0.95 [ASSUMPTION — registered] → else STOP (take the pre-registered (p1)-fail rebuild branch, §5.1).
- **(p2) Calibration portability:** B-arm first-token accuracy on a fresh 20-item subset ∈ [0.2, 0.8] [ASSUMPTION — registered] → else STOP.
- **(p3) Delivery portability:** WRITE-span regex rate on a 20-item S-arm pilot ≥ 0.50 [ASSUMPTION — registered] → else STOP.

Trip of (p2)/(p3), or the (p1)-fail rebuild still failing (p2)/(p3): study (b) **STOPS at design cost (~2,700 forwards: 20×15 B-pilot + 20×120 S-pilot [Fix D3]), logged HELD** — a measurement boundary (EXP147 precedent), which licenses nothing and kills nothing. A portability failure is never relabeled as a KILL (Law #4).

**4-hop exploratory trigger (study (a) only, pre-registered):** the third level is built and analyzed (Jonckheere–Terpstra trend test over {2,3,4}, one-sided for increasing trend) **iff** guard (h) at Step 0 projects the 2-level run at ≤ 48h wall [ASSUMPTION — registered] — i.e., genuine headroom exists. Otherwise 4-hop is neither built nor analyzed; the omission is logged. The trigger is an apparatus condition, not a data look (Law #9 clean). If the 4-hop level is admitted, its stratum breakdowns are descriptive only (Law #9 — no stratum promoted to a decision), same rule as §4. [Fix A5, Law #14 review 2026-10-09.]

**Descriptive reporting (not guards, both studies):** B-arm format compliance; mean extra-token counts; per-stratum S−C nets (descriptive — Law #9, no stratum promoted to a decision).

### 5.5 Cost

$0 CPU. (a): ≈193.8k generation + ≈300 B dry-run + 4,800 C+S pilot = 198.9k ≤ guard (g) 200k [Fix D8]. (b): ≈45.9k generation + ≈2.7k portability pilot = 48.6k ≤ guard (g) 50k [Fix D3]. Wall-time asserted at Step 0 per guard (h), never in advance (Law #2).

### 5.6 Determinism (Law #13)

Bench construction seeds registered at execution; dry-run/pilot subset seeds registered (≠ construction seeds); generation seeds fixed per arm, registered; greedy decoding; model revisions 40-hex pinned at Step 0 from cache; environment manifest recorded (same CPU stack family as EXP148: torch 2.14.x+cpu, transformers 5.17.0, numpy — re-recorded, not assumed). Per-item records flushed per write. Weights loaded from local caches only — no HF Hub contact at execution.

---

## 6. Material uncertainties

1. **The d-dependence (study (a)):** the registered power rule (§2.1) converts the n decision into a computation, not a choice — pinned Wald-formula method on the 20-item C+S pilot rate d_pilot, with EXP148's d = 0.3556 first-block keying [Fix D8]; any n-raise re-asserts guards (g)/(h), STOP/HELD at design cost if breached [Fix D5].
2. **Reverse dose-response:** if δ̂_3 − δ̂_2 < 0 with a tight CI, the (a) KILL fires — and a strong reverse pattern is itself a finding (headroom-driven gain), reported descriptively.
3. **GPT-2 BPE tokenization (study (b)):** the (p1) gate converts this into an apparatus check; the (p1)-fail rebuild branch is pre-registered.
4. **GPT-2-small format-following:** the (p3) gate converts WRITE non-delivery into HELD, never into a spurious KILL.
5. **Prior-data honesty (study (a)):** EXP148's descriptive stratum pattern motivated the dose-response question; the test runs on a fresh bench — Law #9 is satisfied by construction, and the §6 registration of this fact makes the motivation auditable.

---

*Pre-registration draft finalized 2026-10-09 (LOG-4967). Status: DRAFT — NOT SIGNED. NOT EXECUTED. No forwards run. Companions: `EXP149_DESIGN_DRAFT_2026-10-09.md`. Awaited: independent Law #14 review of the pre-reg draft → CEO sign → execution authorization (Step-0 gates first). Execution NOT licensed by this document.*

---

## Fixes applied — Law #14 review repair lane, 2026-10-09

**Status after repair: repaired per the independent review's exact prescriptions (`EXP149_LAW14_REVIEW_2026-10-09.md`). STILL NOT SIGNED — signing is the CEO's act after diff-level re-verification. NOT EXECUTED. No design, hypothesis, guard, or decision-bar change was made; all fixes are numeric/expositional.**

- **D1:** §2.1 power table recomputed from SE(θ) = √[(d−net²)(1/n_3+1/n_2)] — (0.30,0.20)→0.0370/0.86; (0.32,0.20)→0.0384/0.83; (0.36,0.20)→0.0410/0.79; (0.30,0.25)→0.0354/0.88. (Independently re-verified this lane.)
- **D2:** reverse dose-response P(KILL fires) ≈0.81 → **0.77**. (Independently re-verified this lane: Φ(0.7427) = 0.7713.)
- **D3:** study (b) portability-pilot cost ≈600 → **≈2,700** forwards (20×15 + 20×120); guard (g) margin re-asserted (45,900 + 2,700 = 48,600 ≤ 50k). (Independently re-verified this lane.)
- **D4:** 4-hop trigger reconciled to the registered wording (guard (h) at Step 0 projects the 2-level run at ≤ 48h wall); the pre-reg already carried it, so its wording is unchanged.
- **D5:** registered n-raise guard re-assertion added (§2.1) — STOP/HELD at design cost if the raised n would breach guard (g) ≤ 200k or guard (h) ≤ 72h.
- **D8:** registered discordant-pair-rate source added (20-item C+S pilot, d_pilot; EXP148's d = 0.3556 carried with first-block keying); Wald-formula power-computation method pinned; study (a) design cost updated (193,800 + 300 + 4,800 = 198,900 ≤ guard (g) 200k).
- **D9:** (p1) re-verification registered on any rebuilt bench (≥ 0.95 required; else STOP/HELD at design cost).
- **A2:** [ASSUMPTION — registered] tags added to the (p1)/(p2)/(p3) trip thresholds and the 48h guard.
- **A5:** 4-hop stratum descriptive-only rule carried explicitly (Law #9).
- **A1, A4:** advisory notes only — no changes made. A1's PIVOT reading is carried verbatim from EXP148's pre-reg §3 per the registered carry rule (changing it would violate the carry); A4's CONTINUE-bar asymmetry is registered and was noted, not objected. Both flagged for CEO discretion.
