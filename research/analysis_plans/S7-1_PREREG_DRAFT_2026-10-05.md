# S7-1 Pre-registration — DRAFT: J7 In-context writable memory (scratchpad-as-memory at Δθ=0)

**Status:** SIGNED. Independent Law #14 review returned SIGN-WITH-FIXES (re-review required); repair lane applied required Fixes 1–3 + advisories (i)–(ii) + label nit (2026-10-05); independent fix-verification re-review returned binding PASS (all fixes verified; no further review needed). The CEO signs on the re-review's authority.
**Drafting lane:** S7-1 (J7), licensed proposal; born at the Monday session 2026-10-05 (LOG-4911); backlog row `research/innovation/CANDIDATE_BACKLOG.md:32`.
**CEO ruling on the budget delta (§2.4):** the backlog's n=60 is underpowered for the registered +10pp scale (MDE80 ≈ +17pp; KILL fires <40% under null — most true nulls would land HELD, licensing nothing and killing nothing). Per the S7-4 precedent (do not run an underpowered experiment), the CEO approves the draft's recommended n=180 (≈46k forwards, $0 CPU, wall-time gated by guard (h)). The n=60 verdict run is not licensed.
**Experiment number:** EXP147 (minted by the CEO at execution authorization, 2026-10-05 — new protocol = new number per the single-lane fence).
**Parent context [FACT]:** The 2026-10-03 Spotlight briefing (Percepta blog, Oct 2 — UNVERIFIED vendor source) is the first published existence proof of Δθ=0 capability growth via writable memory — but through a *custom writable-memory architecture* (tiny fixed intelligence module + unbounded writable sparse memory). The briefing explicitly preserves all killed-lane verdicts and authorizes no experiment from the blog alone. The program's kills say static geometric injection does not steer standard frozen transformers (EXP077/093/094/096/105/131, EXP146); the open question is whether the missing ingredient for Δθ=0 capability growth is *architectural* (Spotlight's claim) or *disciplinary* (prompting discipline on a standard frozen transformer).

**Governing laws:** Law #2 (no invented numbers — every constant below is pinned or computed, never improvised), Law #4 (no post-hoc shifts — the bars below are binding; the backlog row's verdict column is inherited, not re-read), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — bench gold answers never touch the prompts; few-shot exemplars are fixed and disjoint from the bench), Law #9 (metrics registered before any output is inspected), Law #11 (observation vs interpretation separated throughout), Law #13 (deterministic reproducibility), Law #15 (worth-it gate §1).

**Epistemological labels** per `~/workspace/SCBI/AGENTS.md` §5 ([FACT], [DEFINITION], [HYPOTHESIS], [CONJECTURE], [ASSUMPTION], [PROPOSITION], [THEOREM], [OBSERVATION], [INTERPRETATION], [OPEN]) are used throughout and are load-bearing. [NOTE] and [CAVEAT] mark operational clarifications.

---

## 0. The question (read first)

**[HYPOTHESIS]** A standard frozen transformer can simulate writable key–value memory in context: explicit WRITE/READ prompting discipline lets it externalize intermediate deductions as discrete tokens and re-attend to them, growing multi-hop capability without new architecture — beating budget-matched chain-of-thought.

**Breaking point:** On the powered design (n=180, §2), the scratchpad arm shows no advantage over budget-matched CoT (one-sided McNemar p ≥ 0.1, 95% CI for the net rate excluding +10pp) with the discipline verified delivered (guard (e)) and the budget-match comparability verified (guard (f′)) → **KILL** the J7 hypothesis (§4). The missing ingredient is architectural, not disciplinary — Spotlight's architectural claim sharpens into a testable boundary.

**What this draft does not do:** it does not test "memory" in the architectural sense (no new modules, no weight updates); it tests whether *prompting discipline* can simulate it. It does not license any model other than frozen Pythia-410m. It does not touch the v102 paper. It does not re-read any killed lane's bars.

---

## 1. Worth-it gate (Law #15, 7 points)

1. **Exact question [HYPOTHESIS]:** Does explicit in-context read/write discipline (WRITE/READ scratchpad) beat budget-matched chain-of-thought on multi-hop reasoning at Δθ=0 — i.e., can a standard frozen transformer simulate writable memory purely in context?
2. **Decision changed:**
   - **CONTINUE** (§4): scratchpad vs budget-matched CoT, one-sided McNemar p < 0.05 with net ≥ +10pp → "explicit read/write discipline beats budget-matched CoT" — the program's first capability entry; the writable-memory-in-context line lives and is licensed for follow-up (dose-response on hops, cross-family).
   - **KILL** (§4): no scratchpad advantage (one-sided p ≥ 0.1, 95% CI excludes +10pp), discipline verified delivered (guard (e) PASS) and budget-match comparability verified (guard (f′) PASS) → "discipline adds nothing over budget-matched CoT" — J7 dead; the Δθ=0 capability-growth question pivots to architecture (Spotlight's direction).
   - **PIVOT** (§4): KILL fires but scratchpad beats baseline (S vs B p < 0.05) → test-time compute helps, discipline doesn't — pivot the lane to test-time-compute scaling, not memory discipline.
   - **HELD** (§4): everything else — sub-significant signals, CIs too wide, unattributable effects. Licenses nothing, kills nothing.
   - **RUN-INVALID** (§4): apparatus failure (discipline not delivered, compute not delivered, bench degenerate, compute infeasible). Never a verdict.
3. **Cheapest test:** $0 CPU generation bench — n=180 multi-hop items × 3 arms (B: 2-shot direct-answer baseline; C: 2-shot budget-matched CoT; S: 2-shot structured WRITE/READ scratchpad), frozen Pythia-410m, greedy decoding, token budgets T_B=15 / T=120 (C and S share T — the compute-confound fence). ≤50k generation forwards, $0.
4. **Cost:** $0 CPU. Wall-time gated at Step 0 (guard (h)): proceed only if projected run ≤ 72h on measured throughput; else INCONCLUSIVE (compute-infeasible) — never self-escalate to GPU.
5. **Mathematical license:**
   - (a) [CONJECTURE] Attention implements content-addressable lookup over the context (induction-head circuits and their generalizations) — the mechanism for READ exists in principle in a standard transformer.
   - (b) [DEFINITION] WRITE/READ discipline: externalize each intermediate deduction as a discrete token span `WRITE(factK, ...)` and re-attend to it via `READ(factK)` — this converts the binding-maintenance problem (hold K bindings across hops in the residual stream) into a lookup problem (attend to discrete token spans).
   - (c) [CONJECTURE] If hop-degradation is driven by binding degradation (the S4-2 premise: composed-context entity-slot encodings degrade vs clean probes), externalization should reduce it — explicit addressing bypasses the degraded binding path. The S4-2 transplant question was about *repairing* bindings; S7-1 is about *routing around* them through externalization.
   - (d) [DEFINITION] The budget-matched CoT control (same token budget T=120, same 2-shot structure) is designed to isolate *discipline* from *test-time compute*. [CAVEAT — Fix 1]: T=120 is a cap, not a guarantee of equal usage — the "budget-matched" label is earned only if guard (f′) holds (mean_tokens(S)/mean_tokens(C) ∈ [2/3, 3/2], a registered [ASSUMPTION]); if (f′) trips, the S−C comparison is attribution-compromised → HELD. When (f′) holds, any S−C difference is attributable to the addressing discipline, not to generating more tokens. This is the steelman built into the design: "scratchpad is test-time compute with extra steps" predicts S ≈ C, which is the KILL pattern.
6. **Quantitative prediction:** If the [CONJECTURE] holds at decision-relevant scale: S − C ≥ +10pp net correctness (one-sided McNemar p < 0.05 at n=180, §2). If the breaking point holds (binding degradation dominates and is not addressable by externalization, or the model cannot follow the discipline): S − C ≈ 0 with the discipline verified delivered.
7. **Breaking point:** §0 — KILL on the powered null with guard (e) PASS. The bar bites: P(KILL fires) ≈ 0.65–0.88 under true null at n=180 (§2); false-KILL under a true +10pp effect < 3%.

---

## 2. Power analysis (the license for n=180) [FACT — exact binomial computation, no model runs]

Paired design: per item, b = S-correct/C-wrong, c = S-wrong/C-correct; q = P(b)/item, r = P(c)/item, net = q−r, d = q+r (discordant rate). All power figures are exact (binomial enumeration over discordant-pair counts, α=0.05 one-sided), computed from first principles in the drafting lane — same convention as S7-4 §2.1.

### 2.1 CONTINUE-bar power (one-sided McNemar p < 0.05)

| q | r | net | d | n=60 | n=120 | n=180 |
|---|---|---|---|---|---|---|
| 0.15 | 0.05 | 0.10 | 0.20 | 0.430 | 0.756 | 0.906 |
| 0.175 | 0.075 | 0.10 | 0.25 | — | — | 0.830 |
| 0.20 | 0.10 | 0.10 | 0.30 | 0.332 | 0.592 | 0.761 |
| 0.225 | 0.125 | 0.10 | 0.35 | — | — | 0.700 |
| 0.20 | 0.05 | 0.15 | 0.25 | 0.707 | — | — |
| 0.25 | 0.05 | 0.20 | 0.30 | 0.880 | — | — |

**Reading [INTERPRETATION]:** n=60 (the backlog's number) is underpowered for the registered +10pp scale — power 0.27–0.43, MDE80 ≈ +17pp. It is powered only for large effects (≥+20pp: power 0.76–0.88). n=180 clears 80% power at +10pp for discordant rates d ≤ 0.30 (MDE80 ≈ +10pp); at d=0.35 power is 0.70 (MDE80 ≈ +11pp).

### 2.2 KILL-bar operating characteristics

P(KILL fires) = P(one-sided p ≥ 0.1 AND two-sided p ≥ 0.1 AND 95% CI upper < +0.10), exact enumeration:

| Truth | n=60 | n=120 | n=180 |
|---|---|---|---|
| Null, d=0.20 | 0.389 | 0.670 | 0.812 |
| Null, d=0.25 | 0.321 | 0.569 | 0.728 |
| Null, d=0.30 | 0.277 | 0.485 | 0.650 |
| True +10pp (q=0.15, r=0.05) | 0.033 | — | 0.028 |
| True +15pp (q=0.20, r=0.05) | — | — | 0.0005 |
| True +20pp (q=0.25, r=0.05) | 0.0004 | — | — |

[NOTE]: the 95% Wald CI uses SE = √[(b+c) − (b−c)²/n]/n (same convention as S7-4 §3). [CAVEAT]: the KILL bar's firing probability under null depends on the discordant rate d, which is unknown pre-registration — the table spans the plausible range rather than assuming it.

**Reading [INTERPRETATION]:** at n=60 the KILL bar fires only 28–39% under true null — most true nulls land HELD (CI too wide), not KILL. At n=180 it fires 65–88% under null — a powered null. False-KILL under a true +10pp effect is <3% at n=180: the bar does not kill real effects.

### 2.3 False-CONTINUE under null

| n | d=0.20 | d=0.30 |
|---|---|---|
| 60 | 0.027 | 0.032 |
| 180 | — | — |

[NOTE]: false-CONTINUE at n=180 under null is ≤ 0.035 across d ∈ [0.15, 0.40] (same α=0.05 machinery; verified in the drafting computation).

### 2.4 Honest conclusion and recommendation

**The backlog's n=60 is underpowered for the registered +10pp scale and must not run as a verdict study** (S7-4 precedent: do not run an underpowered experiment). At n=60, MDE80 ≈ +17pp and the KILL bar fires <40% under null — the likely outcome is HELD regardless of the truth, which licenses nothing and kills nothing.

**This draft recommends n=180** — the cheapest discriminative design: MDE80 ≈ +10pp (d ≤ 0.30), KILL fires 65–88% under null, false-KILL <3% at +10pp. Cost ≈ 46k generation forwards (180 items × 255 tokens/item across the 3 arms ≈ 45.9k, + 540 prompt-encoding forwards), ~1.7× the backlog's ≈27k figure — **the budget delta is flagged for CEO approval**; if the CEO holds the backlog budget, this draft does not license the n=60 verdict run.

**What would change this assessment [FACT]:** the d-dependence is the residual uncertainty — if the true discordant rate exceeds 0.35, MDE80 rises to ~+11-12pp even at n=180. The draft states this rather than assuming d.

---

## 3. Frozen decision bars (restated from the backlog row)

Backlog row `research/innovation/CANDIDATE_BACKLOG.md:32` (S7-1, J7), verdict column, verbatim:

> ΔM_scratchpad ≤ ΔM_budget-matched-CoT → KILL (discipline adds nothing); scratchpad > baseline but ≤ matched CoT → PIVOT to test-time-compute account

**Operational definitions** (operationalization, not modification — the Law #14 reviewer rules on faithfulness):
- "ΔM_scratchpad ≤ ΔM_budget-matched-CoT": with gains measured over the same baseline B, gain_S − gain_C = acc_S − acc_C (paired per-item correctness). The KILL condition is the conjunction: (i) S vs C one-sided McNemar (H1: S>C) p ≥ 0.1, AND (ii) S vs C two-sided McNemar p ≥ 0.1 (no significant anti-discipline effect — else HELD), AND (iii) 95% Wald CI for the net rate δ̂=(b−c)/n lies entirely below +0.10 (upper < +0.10).
- "scratchpad > baseline but ≤ matched CoT → PIVOT": KILL fires (or S vs C p ≥ 0.1) AND S vs B one-sided McNemar (H1: S>B) p < 0.05 → the PIVOT reading attaches: test-time compute helps, discipline doesn't.
- The CONTINUE reading (the backlog's LOG-218 overturning observation): S vs C one-sided McNemar p < 0.05 AND net rate δ̂ ≥ +0.10 — "structured scratchpad discipline beats budget-matched CoT by ≥+10pp."
- The KILL reading is scoped: "discipline adds nothing *over budget-matched CoT*" — it does not rule out sub-10pp discipline effects, and it does not rule out architectural writable memory (Spotlight's direction).

---

## 4. Decision table (binding)

Precedence: RUN-INVALID > HELD > KILL > CONTINUE (a tripped guard voids everything; an inconclusive configuration is HELD, never KILL; KILL requires the full powered-null conjunction). PIVOT is a secondary reading that attaches to KILL when its condition holds.

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | S vs C one-sided (H1: S>C) p < 0.05 AND net δ̂ ≥ +0.10 | Explicit read/write discipline beats budget-matched CoT; writable-memory-in-context lives; the program's first capability entry — follow-ups licensed (hop dose-response, cross-family) |
| KILL | S vs C: (i) one-sided p ≥ 0.1, AND (ii) two-sided p ≥ 0.1, AND (iii) 95% CI upper < +0.10; guards (e) and (f′) PASS | Discipline adds nothing over budget-matched CoT; J7 dead. The Δθ=0 capability-growth question pivots to architecture |
| PIVOT | KILL fires AND S vs B one-sided (H1: S>B) p < 0.05 | (Reported alongside KILL) Test-time compute helps but discipline doesn't — pivot the lane to test-time-compute scaling, not memory discipline |
| HELD | Anything else (sub-significant signals, CI too wide, guard (d) trips, guard (f′) trips — attribution compromised) | Inconclusive — licenses nothing, kills nothing |
| RUN-INVALID | Any guard (a)/(c)/(e)/(f)/(g)/(h) trips (guard (d) trips → HELD, not RUN-INVALID — bench degeneracy is a finding about the bench, not apparatus failure; guard (f′) trips → HELD, not RUN-INVALID — attribution compromised is a finding about the control, not apparatus failure) | Apparatus failure — never a verdict |

---

## 5. Protocol

### 5.1 Bench construction [DEFINITION]

A **new** 180-item multi-hop bench family (no existing multi-hop machinery in the repo — verified 2026-10-05):
- **Item structure:** synthetic invented-entity contexts with all needed facts stated in-context (no parametric knowledge required — this tests in-context reasoning, not recall). Each item: 2–6 context sentences, one question, one gold answer from a closed entity vocabulary.
- **Strata** (4 × 45 items): {2-hop, 3-hop} × {transitive, compositional}. [DEFINITION — Fix 3] A *transitive* item presents a chain of comparisons under a total order and asks for the extremal entity (min/max): the answer requires composing two (2-hop) or three (3-hop) pairwise relations transitively. A *compositional* item presents a chain of entity→entity relations (e.g., friend-of, pet-of) and asks for the endpoint of the composed chain: the answer requires composing two (2-hop) or three (3-hop) relations by substitution — the question names the START of the chain, never an intermediate entity.
  - *Transitive (2-hop):* "Zorp is taller than Blip. Blip is taller than Fweep. Who is the shortest?" (gold: Fweep — requires composing Zorp>Blip and Blip>Fweep transitively)
  - *Compositional (2-hop):* "Blip's friend is Zorp. Zorp's pet is Fweep. Who is Blip's friend's pet?" (gold: Fweep — requires composing friend-of with pet-of by substitution; the question names the chain start "Blip", never the intermediate "Zorp")
  - *3-hop variants* chain three relations (transitive: four entities in a total order; compositional: three relation-links from the named start entity).
- **Construction procedure** (execution lane): committed script `S7-1_build_bench_2026-10-05.py`, seed `random.Random(7101)` [ASSUMPTION — registered]; entity pools fixed in the script; templates fixed; no LLM-generated items (fully templatic — deterministic by construction).
- **G0:** n=180, all items surface-distinct, strata exact (45/45/45/45), gold answers single entity tokens from the closed vocabulary, every gold entity appears ≥2× across the bench (no singleton answers — else the answer is guessable by elimination) [ASSUMPTION — registered threshold].
- **Pin:** sha256 of the canonical JSON serialization, character-verified at Step 0 (the S7-3/S7-4 lesson: never transcribe — recompute).
- **Law #7:** gold answers are used only at scoring; prompts contain context + question only. Few-shot exemplars (§5.2) use disjoint entity names and are fixed before any bench construction.

### 5.2 Arms and prompts

Model: frozen Pythia-410m, greedy decoding (do_sample=False), Δθ=0. All arms 2-shot (shot-count confound controlled); exemplars fixed, committed in a pinned prompt file at Step 0, entity-disjoint from the bench.

- **B (baseline):** 2-shot direct-answer. Template: `Context: {facts}\nQuestion: {question}\nAnswer with the name only.\nAnswer: {exemplar answers in shots}` — generation budget T_B=15 tokens [ASSUMPTION — registered].
- **C (budget-matched CoT):** 2-shot chain-of-thought. Template: `Context: {facts}\nQuestion: {question}\nThink step by step. Give the final answer after "ANSWER:".` — generation budget T=120 tokens.
- **S (structured scratchpad):** 2-shot WRITE/READ. Template: `Context: {facts}\nQuestion: {question}\nUse the scratchpad. WRITE each deduced fact as WRITE(fact1, ...), WRITE(fact2, ...). When you need a fact, READ it: READ(fact1). Give the final answer after "ANSWER:".` — generation budget T=120 tokens (same T as C — the compute-confound fence [DEFINITION]).
- **Exemplar content** (illustrative — exact text pinned at execution, Step 0): two worked 2-hop items per arm showing the arm's format (B: bare answers; C: step-by-step then ANSWER:; S: WRITE(fact1,...)/READ(fact1) then ANSWER:). [OPEN: exact exemplar wording — must be committed before any bench forward.]

### 5.3 Scoring (registered, deterministic)

1. For C/S: take text after the LAST occurrence of `ANSWER:`; for B: take the full generation.
2. Normalize: lowercase, strip punctuation, collapse whitespace.
3. Exact match vs normalized gold → 1, else 0. No `ANSWER:` in a C/S generation → 0 (registered; no post-hoc rescue).
4. Primary metric: per-item correctness per arm. All verdict statistics are paired McNemar on (S, C), (S, B) correctness pairs. No LLM judge (non-deterministic — excluded by Law #13).

### 5.4 Step-0 guards

- (a) **Δθ=0:** pre/post state-dict hash equality (pin recorded).
- (b) **Model revision:** 40-hex resolved programmatically at download (expected program pin `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`; Step 0 records the actual — never transcribed).
- (c) **Bench pin:** recomputed character-identical from the built JSON before any forward.
- (d) **Calibration:** B accuracy ∈ [0.2, 0.8] → else HELD (bench degenerate for this question: floor = too hard for Pythia-410m; ceiling = no headroom). B outputs are reused for the verdict (no wasted compute).
- (e) **Discipline delivered:** ≥50% of S generations contain ≥1 well-formed `WRITE(factK, ...)` span, where "well-formed" is defined character-exactly by the regex ``r'WRITE\(fact\d+,'`` — literal `WRITE(`, literal `fact`, one or more ASCII digits, literal comma. The closing paren is NOT required (truncated writes still count as delivery attempts); content after the comma is not inspected. The regex is applied to the raw generation text (pre-normalization). → else RUN-INVALID (the intervention didn't deliver — mirrors EXP136's (h) hook-delivery guard). [ASSUMPTION — 50% threshold registered.]
  - [NOTE — advisory (i)]: guard (e) checks WRITE spans only, not READ spans. This is deliberate: WRITE verifies the model followed the format (discipline *delivery*); whether READ is *used effectively* is part of "does the discipline work" — a missing or ineffective READ is a finding about the intervention's efficacy (feeds the KILL verdict), not a delivery failure. A READ check would conflate delivery with efficacy.
- (f) **Compute delivered:** mean_tokens(C) > 2 × mean_tokens(B) AND mean_tokens(S) > 2 × mean_tokens(B) → else RUN-INVALID (test-time compute not delivered — the control is compromised). [ASSUMPTION — 2× threshold registered.]
- (f′) **Budget matched (comparability) — Fix 1:** mean_tokens(S)/mean_tokens(C) ∈ [2/3, 3/2] → else HELD (attribution compromised — the compute-confound fence leaks; a finding about the control, not apparatus failure). [ASSUMPTION — the [2/3, 3/2] band is a registered threshold: the "budget-matched" label is earned by actual usage, not by the T=120 cap alone (see §1.5(d)).]
  - [NOTE — advisory (ii)]: B-arm format compliance is reported descriptively (fraction of B generations that are a single entity token after normalization, plus mean extra-token count). Verbose B generations depress B accuracy and could spuriously fire the PIVOT secondary reading; the compliance report lets the verdict review assess this. It is NOT a guard — B verbosity is a measurement property, not apparatus failure.
- (g) **Budget audit:** total generation forwards ≤ 50k (180 items × 255 tokens/item ≈ 45.9k + 540 prompt-encoding forwards).
- (h) **Compute gate:** throughput probe (50 generation steps on a fixed dummy prompt, excluded from the bench) at Step 0; projected full-run time = 47k / measured_tok_s. If > 72h → INCONCLUSIVE (compute-infeasible). Never self-escalate to GPU. [ASSUMPTION — 72h threshold registered.]

### 5.5 Cost

$0 CPU. ≈46k generation forwards + 540 prompt-encoding forwards (guard (g)). Wall-time unknown until guard (h) measures it — the draft does not assert a duration (Law #2).

### 5.6 Determinism (Law #13)

Seeds: bench 7101; generation seed fixed per arm (registered at execution); greedy decoding. Model revision 40-hex pinned. Environment manifest recorded. All per-item records flushed per write (the EXP143 lesson).

---

## 6. Material uncertainties for the Law #14 reviewer

1. **n=180 vs the backlog's n=60** (§2.4): the draft recommends deviating from the backlog on power grounds and flags the ~1.7× budget delta for CEO approval. If the CEO holds the backlog budget, the draft does not license the n=60 verdict run.
2. **Pythia-410m instruction-following:** a base (non-instruct) LM may not follow the WRITE/READ format even with 2-shot exemplars — guard (e) converts this into RUN-INVALID rather than a false KILL, but the 50% threshold is a registered assumption, and a RUN-INVALID burns the compute for no verdict.
3. **Bench difficulty calibration:** the [0.2, 0.8] B-accuracy gate is a registered assumption. If Pythia-410m sits at floor on 2-hop transitive items, the run ends HELD at guard (d) — the question would need a stronger model (not licensed; new proposal required).
4. **T=120 sufficiency for 3-hop scratchpads:** 3 WRITEs + READs + answer ≈ 100–120 tokens — tight. If S generations truncate mid-reasoning, guard (f) may still pass (tokens generated) while the discipline is degraded. The reviewer should judge whether T=150 is warranted (cost: +16k forwards).
5. **Stratum pooling:** the primary analysis pools all 4 strata. If the effect is hop-dependent (e.g., 3-hop only), pooling dilutes it — but stratum-conditional bars would be post-hoc fishing (Law #9). The draft pools; stratum breakdowns are descriptive only.
6. **The d-dependence (§2.2 CAVEAT):** the KILL bar's power under null ranges 0.65–0.88 across plausible discordant rates. The draft does not assume d.
