# S4-8 — I2′ Multi-Option Runner-Up Suppression — Pre-registration DRAFT v3 (UNSIGNED)

*Status: DRAFT v3 — UNSIGNED. NOT a protocol. NOT executable. NOT signed. No experiment number minted (S4-8 is fresh-proposal material; numbering happens after Law #14 SIGN + CEO license).*
*This v3 is v2 (`S4-8_PREREG_DRAFT_v2_2026-09-28.md`, LOG-4477) with ONE binding amendment: the N1 fix (LOG-4478) gating step 8 on the foil–top-1 overlap stratum (O ≤ 0.5). v1 and v2 are preserved untouched. Awaiting the second delta check of the amended step-8 text (separate lane) before SIGN.*
*Licensing chain: LOG-323 (EXP085 KILLED as designed, binding — k=2 collapse) → LOG-4353 (Friday cull: S4-8 born from EXP085's death-debt, LOG-219 rule; debt recorded PAID; S4-8 is a FRESH proposal, NOT a revival — per LOG-323's explicit routing) → LOG-4475 (v1 draft) → LOG-4476 (independent Law #14 review, SIGN-WITH-FIXES) → lane-keeper queue 2026-09-28 (this repair lane commissioned, pre-assigned LOG-4477).*
*All values below are from `research/innovation/CANDIDATE_BACKLOG.md` (S4-8 row) and LOG-323 unless otherwise cited. No number is invented.*
***No pilot is authorized by this draft.** Before any run: independent delta re-verification of this v2 + SIGN (separate lane), then CEO execution clearance. $0 CPU for this document; the designed battery is <0.01 T4-h and CEO clearance gates any run regardless of venue.*

---

## 0. Law #15 block (binding)

**Precise question [HYPOTHESIS].** EXP085 was KILLED as designed (LOG-323) because at k=2 binary forced-choice, rank-suppression is untestable by construction: ΔM_C2 ≡ 2·(N_f/60)−1 (a deterministic relabeling of baseline accuracy), Tier-0 Type-I = 1.00 with kill-bar power 0.00, C3 undefined, C7 ≡ N_f/60. That kill is scoped to the binary construct — it says nothing about the mechanism. **On a genuinely multi-option bench (k=8) where correct-rank is a real measurement, are 2-hop failures selection failures — the correct answer sitting at low latent rank, suppressed by a wrong top-1 — repairable by target-free top-1 masking?** [HYPOTHESIS]

**Decision it changes.** **KILL** (premise) if the Tier-0 screen finds median correct-rank > 5 on failed items — dead at $0, no selection-failure population exists. **KILL** (nonspecific) if random-masking matches top-1-masking — any mask perturbs rescues; the mechanism claim dies. **KILL** (null) if no arm moves — no suppression effect anywhere on the bench. **CONTINUE** (licensed positive only) if top-1 masking rescues (ΔM_T > 0.10) with random-mask flat (|ΔM_R| < 0.05) and T-vs-R significant at p < 0.05 — the first licensed target-free selection-repair on a multi-option bench. (D2: the v1 foil-flat conjunct is removed — the structural-foil arm is handled by the pre-registered foil–top-1 overlap stratum, §3.) **PIVOT** if top-1 masking is flat (ΔM_T ≤ 0) while the structural-foil mask rescues — interference confirmed but not autonomously exploitable; or if a significant foil rescue co-occurs with a non-CONTINUE top-1 pattern (§3 step 8, D1 — requires overlap O ≤ 0.5; at O > 0.5 the F pattern is non-diagnostic per the stratum). All outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** Tier-0 correct-rank screen first: ≤120-pass logit rebuild (program archives carry decisions only — LOG-284), $0 CPU. Median correct-rank > 5 on failed items → dead at $0, battery never runs. Then the suppression battery: 60 items × 4 arms (B, T, F, R) = 240 decision passes + probes ≈ 360 passes, <0.01 T4-h, $0. **Probes [DEFINITION, m1]:** non-decision readout passes used to extract the full 8-option logit vector and the correct-rank at the pinned readout position (as opposed to arm decision passes, which record only the masked-argmax decision). Budgeted ≤2 per item (≈120 total); any probe beyond the 360-pass planning figure counts against the 500 hard cap.

**Quantitative prediction (pre-registered, bars).** On the Tier-0 population (baseline-wrong AND correct-rank ≤ 5): ΔM_T > DELTA_BAR = 0.10 **and** T-vs-R McNemar-exact p < 0.05 (primary, α = 0.05, the single binding test) **and** |ΔM_R| < 0.05. (D2: the v1 |ΔM_F| < 0.05 conjunct is removed — F is non-diagnostic at foil–top-1 overlap > 0.5; see the pre-registered overlap stratum, §3.) The rescue is predicted to concentrate on correct-rank-2 items (the literal runner-up).

**Breaking point (sharp).** ΔM_T ≤ 0.05 on the Tier-0 population → the autonomous top-1-mask procedure has no effect (routes to PIVOT-or-KILL per §3). ΔM_R within sampling noise of ΔM_T (T-vs-R p ≥ 0.05) with ΔM_T > 0 → **KILL** (nonspecific) — masking is a generic perturbation, not a selection repair. Tier-0 population n_pop < 12 → **Underdetermined** — never KILL on a powerless test (R4 rule).

**The belief it tests (named, LOG-4353):** "EXP085's kill was about the construct, not the mechanism — selection failures may be real on multi-option benches." [INTERPRETATION]

---

## 1. Background and license

- **EXP085 binding facts [OBSERVATION, LOG-323]:** k=2 pin holds on all seven in-repo sources (no k≥3 source exists); at k=2 the I2 design collapses algebraically — ΔM_C2 ≡ 2·(N_f/60)−1, Tier-0 Type-I = 1.00 / kill-bar power 0.00, C3 undefined (masks {m₁,m₂} = O(x)), C7 ≡ N_f/60, §7 sequencing fires on an empty set. The formal treatment is sound — what it proves is the vacuity. Banked boundary: binary forced-choice makes rank-suppression untestable by construction.
- **Death-debt [FACT, LOG-4353]:** S4-8 pays EXP085's LOG-219 death-debt; deaths table records PAID. This draft is the "full fresh pre-registration chain" the backlog row requires — **not a revival, not an edit of EXP085's killed draft** (LOG-323: draft retained, bannered KILLED, body untouched; no signed file modified — this document is a new unsigned file).
- **Mathematical license [PROPOSITION — elementary combinatorial fact, m2]:** on a k-option bench with k ≥ 3, the correct-rank r_i ∈ {1,…,k} is NOT a deterministic function of correctness — it carries independent content (at k=2, r_i = 2 ⟺ wrong, which is the entire collapse). Proof sketch: at k ≥ 3, on a wrong item the correct option's logit can sit at any rank 2,…,k while a different option holds top-1, so correctness ↛ rank. Masking the top-1 token's logit (−1e9 before argmax) is a well-defined operator for any k; the masked argmax over the remaining k−1 options is a genuine counterfactual decision. **License verdict: HOLDS for a test, not a conclusion** — the license licenses the experiment, not the positive. Honest audits carried: (Gap 1) masking perturbs the whole softmax → random-mask control prices out generic perturbation (specificity is the binding contrast); (Gap 2) one new bench → CONTINUE claim bench-scoped; (Gap 3) power at n_pop: McNemar needs ≥6 unidirectional flips → Tier-0 population gate n_pop ≥ 12 before the battery.
- **EXP090 lesson — G1 contract [FACT, LOG-362]:** "benchmark entities are G1-satisfiable single words" was asserted by two independent reviews WITHOUT running the real tokenizer; 7/10 entities were multi-token → RUN-INVALID. This design's G1 contract (§2.1, §4) requires real-tokenizer verification of every option string against the pinned tokenizer artifact (EleutherAI/gpt-neox-20b — D4), or the run is void — asserted satisfiability is worth nothing.
- **Summit filter:** a licensed positive would be the program's first target-free selection-repair license — a repair primitive the summit (autonomous self-steering) must build on. Caveat preserved: masking is externally applied by the executor, never self-computed by the model — must never be described as an autonomy result.

---

## 2. Design (frozen model, Δθ = 0)

### 2.1 The scored multi-option construct (new — the heart of the fresh proposal)

**Bench:** new 60-item 2-hop bench, **k = 8 options per item**, built fresh for S4-8 (not EXP092-B, which is binary/A-first/C-first). Each item: a 2-hop question, exactly one correct option, seven distractors. At bench-build time (before any model pass) the builder designates exactly one **structural foil** per item — the distractor judged most confusable — documented in the bench manifest with rationale (§5 item 2). Post-hoc foil-picking from baseline errors is forbidden (Law #7 — that would be label-leakage by another name).

**Bench-build procedure (pre-registered, D4):**
- **(a) Item-generation procedure:** 60 2-hop questions written by the bench-builder: each question must require two reasoning hops (entity → bridge entity → answer), must have exactly one correct answer, and seven distractors of the same entity type as the correct answer. The structural foil is the distractor judged most confusable "by a strong student," designated under the D3 blindness criterion below.
- **(b) Correct-answer verification:** each item's designated correct option is verified by an independent checker lane (different from the item writer) against the question's reference source **before any model contact**; items failing verification are dropped and replaced during bench construction (pre-run construction, never post-hoc).
- **(c) Correct-position shuffle:** within each item, the 8 option positions are assigned by a uniform random permutation (seed pinned, recorded in the manifest); no fixed correct-position pattern is permitted (A-first/C-first avoided — EXP092-B lesson).
- **(d) Prompt template + readout-position pin:** the exact prompt template is pre-registered here and frozen:
  ```
  Q: <question>
  A) <option 1>
  B) <option 2>
  C) <option 3>
  D) <option 4>
  E) <option 5>
  F) <option 6>
  G) <option 7>
  H) <option 8>
  Answer:
  ```
  The **readout position [PINNED]** is the token position immediately following the terminal `Answer:` — the scored logits are the next-token logits at that position. Template hash and readout-position index are recorded in §5 item 2.
- **(e) Tokenizer artifact (named, D4):** the production tokenizer of the frozen model is **EleutherAI/gpt-neox-20b** (the Pythia-410m production tokenizer); the exact revision hash must be recorded in the tokenizer-verification attestation (§5 item 2) before any model pass. A gate whose instrument is unnamed is not auditable — this pins it.

**Option→token mapping (G1 contract, EXP090 lesson):** each option string must tokenize to **exactly one token** under the REAL pinned tokenizer (run — not asserted), and the 8 tokens within an item must be pairwise distinct. Verification is a pre-registered gate (§4): any multi-token option or intra-item token collision → **RUN-INVALID** (procedure void, not a verdict). The scored decision is argmax over the 8 option-token logits at the readout position; correct-rank r_i is the rank of the correct option's logit (1 = top).

**Why k = 8 [FACT]:** the Tier-0 threshold (median correct-rank > 5) needs k > 5 to have content; k = 8 gives rank resolution 1–8 while keeping the 480 option-string tokenizer verifications tractable. At k = 8 none of EXP085's degeneracies occur: ΔM is not a function of N_f, the mask set is well-defined (mask 1 of 8, score 7), and Tier-0's Type-I is a genuine statistical property.

**Foil-build blindness (operationalized, D3 — Law #7):**
- **Builder identity [pre-registered]:** structural foils are designated by the named bench-builder (role + lane identifier recorded in the bench manifest, §5 item 2) — a lane that has had no access to model outputs on S4-8 bench items.
- **Blindness criterion [DEFINITION]:** at the time of foil designation, the builder has observed **zero** model outputs on any S4-8 bench item — no logits, decisions, ranks, or margins. Designation uses only the question text and the distractor texts, under the criterion "the distractor a strong student would most plausibly pick."
- **Verification step [pre-registered]:** before any model pass, an independent verification lane (different from the builder) confirms (a) every foil-designation timestamp precedes the first model-pass timestamp, (b) the bench manifest records per-item foil rationale + hashes, and (c) no model-output artifact exists with a timestamp earlier than the first model pass. The verification result is persisted in the bench manifest. **Any post-hoc foil re-designation is a disqualification, not a finding.**

### 2.2 Tier-0 correct-rank screen (the $0 gate — runs first, battery gated on it)

- **Passes:** ≤120-pass logit rebuild on the 60 bench items (archives carry decisions only — LOG-284), $0 CPU. Records per-item: top-1 decision, full 8-option logit vector, correct-rank r_i (ties broken by option-index order — pre-registered; §3 step 5 tie-guard).
- **Population:** failed items (baseline top-1 ≠ correct) with r_i ≤ 5 → the Tier-0 population (size n_pop).
- **Kill rule:** median r_i over failed items > 5 → **KILL** (premise) — dead at $0, battery never runs; no selection-failure population exists to repair.
- **Power rule:** n_pop < 12 → **Underdetermined** — the battery cannot reach McNemar significance by construction (R4: never KILL on a powerless test).
- **Sanity rule:** baseline accuracy outside [0.25, 0.75] → **HOLD** — bench miscalibrated, not a verdict on the mechanism. Bench must not overlap EXP092-B items (fresh construct).

### 2.3 Suppression battery arms (pre-registered; full within-item pairing)

| Arm | Operation at readout | Role |
|---|---|---|
| B | none (Δθ = 0) | baseline — anchors bench + Tier-0 |
| T | mask baseline top-1 token (logit → −1e9), re-argmax over 7 | test — the autonomous, target-free procedure (rank-chosen, label-free) |
| F | mask the structural foil's token (bench-manifest designation), re-argmax | diagnostic — is the designated foil the suppressor? (label-informed at build time, NOT autonomous) |
| R | mask a uniformly random option token among the k−2 options excluding baseline top-1 AND the correct option, re-argmax; seed pinned | specificity control — generic masking effect, priced out |

**R-arm exclusion rationale [DEFINITION]:** on Tier-0 items the top-1 is wrong by construction, so T never masks the correct option; R excluding the correct option keeps the control symmetric (masking the correct option would be a strawman that can only suppress rescues). The exclusion is documented, not hidden.

**Masking semantics [DEFINITION]:** masking sets the option token's logit to −1e9 before the argmax; all other logits untouched; the decision is the argmax over the surviving options. ΔM_X = (1/n_pop)Σ[correct_X(i) − correct_B(i)] on the Tier-0 population (primary); full-bench ΔM reported as secondary.

### 2.4 Budget (pre-registered)

- **Tier-0: ≤120 passes, $0 CPU.** **Battery: 60 × 4 = 240 decision passes + probes ≈ 360 passes, <0.01 T4-h, $0** (probes defined in §0). Hard cap 500 total; spend beyond 360 needs a logged, pre-cleared exception. CEO clearance gates any run regardless of venue (CPU $0 or the founder's free GPU lane — CPU agents never launch GPU work).

### 2.5 Statistics (pre-registered)

- **McNemar exact** on paired decisions within the Tier-0 population: T-vs-B, F-vs-B, R-vs-B, T-vs-R, T-vs-F (all within-item paired; no between-items allocation; no post-hoc re-routing).
- **Primary contrast (binding):** T-vs-R McNemar at **ALPHA = 0.05** — the single binding test. All other contrasts at Bonferroni **α = 0.0125**, descriptive (Law #9 — no post-hoc promotion).
- **DELTA_BAR = 0.10** (program-licensed bar); **flat band |ΔM| < 0.05 for R under CONTINUE** (D2: the v1 F conjunct is removed; F is handled by the pre-registered overlap stratum, §3).
- **Tango 95% CIs** on the paired differences.

---

## 3. Decision table (pre-registered)

**Binding evaluation order (first match wins).** The executor evaluates in this exact order; exactly one step is earned:

**Foil–top-1 overlap stratum (pre-registered, D2).** Overlap O [DEFINITION] = (# Tier-0 items where the structural-foil token equals the baseline top-1 token) / n_pop. If O > 0.5, the F arm is **non-diagnostic** — it duplicates the T arm on a majority of Tier-0 items: F results are reported descriptively by stratum with no binding consequence, and CONTINUE carries no F conjunct. If O ≤ 0.5, the F arm is diagnostic and a significant F rescue routes per steps 6/8 below. (This stratum replaces v1 step 10's parenthetical "mechanism note" — the overlap check is now pre-registered and adjudicating, not a contradiction.)

1. **G1 contract:** real-tokenizer verification fails (any multi-token option or intra-item token collision, against the pinned EleutherAI/gpt-neox-20b artifact) → **RUN-INVALID** — procedure void (EXP090 lesson); no verdict licensable. *(Maps to: Inconclusive.)*
2. **Tier-0 premise:** median correct-rank over failed items > 5 → **KILL** (premise): dead at $0 — no selection-failure population. *(Maps to: Refuted.)*
3. **Tier-0 power:** n_pop < 12 → **Underdetermined** — powerless test; battery does not run. *(Maps to: Underdetermined.)*
4. **Bench sanity:** baseline accuracy outside [0.25, 0.75] → **HOLD** — miscalibrated bench. *(Maps to: Inconclusive.)*
5. **Tie-guard:** correct-option top-1 tie rate > 25% in Tier-0 → **HOLD** — rank instrument degraded. Tie rate [PINNED, D5] = (# Tier-0 items where the correct option's logit is exactly tied — float32 exact equality — for the highest logit among the 8 options) / n_pop. *(Maps to: Inconclusive.)*
6. **PIVOT (diagnostic):** ΔM_T ≤ 0 AND ΔM_F > 0 with F-vs-B p < 0.0125 → **PIVOT**: interference confirmed (the structural foil suppresses the answer) but not autonomously exploitable by target-free top-1 masking. *(Maps to: Not supported for the autonomous claim.)*
7. **CONTINUE:** ΔM_T > 0.10 AND T-vs-R p < 0.05 AND |ΔM_R| < 0.05 → **CONTINUE**, bench-scoped: target-free top-1 masking rescues decisions; first selection-repair license. (D2: the v1 |ΔM_F| < 0.05 conjunct is removed — unreachable by construction in the expected foil–top-1 overlap world; F is handled by the pre-registered overlap stratum above.) *(Maps to: Supported.)*
8. **PIVOT (foil interference, D1):** not CONTINUE, AND ΔM_F > 0 with F-vs-B McNemar p < 0.0125, AND overlap O ≤ 0.5 (F diagnostic per the pre-registered stratum) → **PIVOT**: the structural-foil mask rescued decisions — interference confirmed (the designated foil suppresses the answer) — but the pattern is not attributable to the autonomous target-free top-1 procedure (T flat, sub-bar, or matched by the random arm). The verdict rationale must name the foil arm; it must never read "random masking matches — generic perturbation" in this corner. If O > 0.5, the F-significant pattern carries no binding consequence per the stratum — the evaluation falls through to step 9/11. *(Maps to: Not supported for the autonomous claim.)*
9. **KILL (nonspecific):** ΔM_T > 0 AND T-vs-R p ≥ 0.05 → **KILL**: random masking matches — generic perturbation, not selection repair. (D1/N1: this step now fires only when the F-significant pattern did not route to step 8 — including the O > 0.5 corner, where the F pattern is non-diagnostic per the stratum, so the rationale is accurate.) *(Maps to: Refuted.)*
10. **KILL (null):** |ΔM_T|, |ΔM_F|, |ΔM_R| all < 0.05 → **KILL**: no suppression effect anywhere on this bench. *(Maps to: Refuted.)*
11. **Otherwise → PIVOT** *(maps to: Not supported for the global claim)* — unclassified pattern recorded by name (e.g., T rescues but F also rescues with T-vs-R significant → CONTINUE per step 7 stands; F's rescue is then a mechanism note per the overlap stratum, reported descriptively).

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted). No banned language. A design change is a new proposal, never a silent edit (Law #4).

**Scope fence:** EXP085's kill is untouched (binary construct stays dead); this is a different experiment per LOG-323's routing. No autonomy claim — masking is executor-applied. No generality beyond the k=8 2-hop bench, Pythia-410m, frozen. A CONTINUE licenses the operationalized claim only ("target-free top-1 masking rescues decisions on this bench"), never a cognitive "the model knew the answer" gloss. The S6 L11 stand-down is a different lane; no L11 direction is involved here.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post; mismatch voids the run (Law #13).
- **G1 real-tokenizer gate (EXP090 lesson):** all 480 option strings verified single-token and intra-item-distinct with the REAL pinned tokenizer (EleutherAI/gpt-neox-20b; exact revision hash recorded in the attestation) before any model pass; attestation persisted (§5 item 2). Failure → RUN-INVALID (§3 step 1), never a verdict.
- **Foil-build blindness (Law #7, operationalized D3):** structural foils designated at bench-build time under the D3 blindness criterion (§2.1) by the named builder; independent verification lane confirms designation-precedes-first-model-pass, manifest rationale + hashes, and zero pre-pass model-output artifacts (§5 item 2). Any post-hoc foil re-designation is a disqualification, not a finding.
- **N_pop feasibility computation (EXP079 lesson — recorded on paper):** before the battery, compute from Tier-0: n_pop and the minimum flips for McNemar p < 0.05 (b=6, c=0 → p = 2/64 = 0.03125; b=5, c=0 → p = 0.0625, n.s.). The n_pop ≥ 12 gate IS this computation's enforcement — unlike EXP079's split-limited probe there is no hidden structural cap (max achievable ΔM = 1.0 ≥ DELTA_BAR = 0.10; rank threshold contentful at k=8). If the computation shows the bar unreachable, the battery does not run (HOLD, not a silent edit).
- **Degeneracy analysis + constant-data unit tests (LOG-4338 lesson):** pre-registered before any run — (a) constant-logit input → rank function returns the option-index tie-break (unit test asserts); (b) masking a non-top-1 token never changes argmax on fixed logits (unit test asserts); (c) masking top-1 promotes the previous runner-up on fixed logits (unit test asserts); (d) b=c=0 → McNemar p=1.0 is a valid null, not an error; (e) empty failed set → Tier-0 vacuous → KILL (premise); (f) **McNemar-exact implementation cross-checked against a reference (hand recurrence or scipy.stats) on the full (b,c) grid before any bench contact; mismatches void the statistics machinery (m3).** The rank/mask/McNemar machinery must pass all six on synthetic data before touching the bench.
- **Per-item records (Law #13):** every pass persists (item id, arm, top-1 decision, correct-rank, 8 option logits, masked token, margin vs B). Non-negotiable — LOG-284/LOG-4352 aggregate-only gaps are not repeated.
- **Verdict discipline:** §3 order, five permitted verdicts, no post-hoc table edits.
- **$0 compute for this draft:** on-paper only. No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, arm ∈ {B,T,F,R}, top-1 decision, correct-rank r_i, 8 option-token logits, masked token id or none, ΔM components vs B).
2. Bench manifest: 60 items × 8 option strings, option→token-id mapping, REAL-tokenizer verification attestation (per-string token counts + intra-item distinctness **+ tokenizer artifact name EleutherAI/gpt-neox-20b and exact revision hash — D4**), structural-foil designations + build-time rationale, bench-build code hash, **bench-builder identity + D3 blindness-verification result, correct-position shuffle seed, frozen prompt-template hash + pinned readout-position index (D3/D4)**.
3. Tier-0 worksheet: failed-item list, r_i values, median, n_pop, tie rate (D5-pinned numerator/denominator), the §3 step-2/3/4/5 evaluations.
4. Δθ = 0 hash pre/post; environment + seed manifest (Law #13; R-arm seed pinned).
5. Masking unit-test log: the six §4 degeneracy tests, PASS/FAIL each.
6. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition; **foil–top-1 overlap O and the D2 stratum report**; stratum-style table of all five contrasts (ΔM, b/c/p, Tango CI) on Tier-0 pop + full bench.

---

## 6. Six ranked design risks (for the Law #14 reviewer)

1. **Option→token mapping validity (EXP090 lesson).** A single multi-token option voids the logit-scored construct the way EXP090's bench voided its run. Mitigation: G1 real-tokenizer gate as RUN-INVALID (§4) — but the reviewer should confirm the gate's attestation format is auditable (per-string evidence, not a summary boolean).
2. **Foil-designation circularity (Law #7).** The structural foil is the load-bearing diagnostic for PIVOT; if its designation smuggles model-output knowledge, step 6 is circular. Mitigation: build-time blindness + manifest rationale — reviewer should stress-test whether the "most confusable distractor" judgment is really model-blind.
3. **Mask-specificity power.** R is the only specificity control; at n_pop ~12–20 a partial R rescue (0 < ΔM_R < ΔM_T) may leave T-vs-R non-significant while a real specific effect exists. Pre-registered routing sends this to KILL (nonspecific) — never "trending" (Law #9). Reviewer: confirm this conservatism is acceptable, or demand a larger n_pop gate.
4. **Multiplicity.** Five contrasts; exactly one binding test (T-vs-R, α=0.05), rest Bonferroni 0.0125/descriptive. Reviewer: confirm the primary is the right binding choice (vs T-vs-B), and that the flat-band |ΔM|<0.05 for R under CONTINUE is not post-hoc (it is pre-registered here).
5. **Tier-0 population size.** n_pop < 12 → Underdetermined by fiat; a bench where the model fails little (or ranks well) yields no test. Reviewer: confirm the 12-item gate isn't itself a selection bias that conditions on the phenomenon (it is pre-registered and mechanical — but flag if the bench's difficulty profile makes n_pop systematically small).
6. **Bench miscalibration / novelty.** A brand-new k=8 bench has no calibration history; accuracy outside [0.25,0.75] → HOLD. Reviewer: confirm the bench-build spec (§2.1) is tight enough that HOLD is a bench problem, not a backdoor to re-running until the bench "works" (re-running a rebuilt bench is a new proposal, not a repair).

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not revive EXP085 (LOG-323's killed draft stays bannered and untouched); does not alter any signed protocol; does not touch weights.
- Does not invent numbers — every value cites the CANDIDATE_BACKLOG S4-8 row or LOG-323, except the new construct (§2.1–§2.3), which is the fresh design this draft exists to specify.

---

## 8. Next steps

Independent **Law #14 review** of v1 complete (LOG-4476, SIGN-WITH-FIXES, 8 fixes D1–D5/m1–m3); this v2 is the repair wave. **Independent delta re-verification** of this v2 (separate lane — NOT commissioned here) must confirm each fix is present verbatim → SIGN → CEO execution clearance → Tier-0 screen → (gate) → battery. **Pilot NOT authorized until all complete.**

*v3 note (LOG-4479): this v3 applies the N1 binding amendment (LOG-4478) gating step 8 on O ≤ 0.5. A second delta check of the amended step-8 text (separate lane) must pass before SIGN.*

---

*Draft v3 prepared 2026-09-28 by the S4-8 N1-amendment lane (pre-assigned LOG-4479), applying the binding N1 fix (LOG-4478) to step 8 as exact pre-registered text + direct cross-references. v1 and v2 preserved untouched. DRAFT, UNSIGNED. On paper only, $0 compute. No signed protocol file was edited; this is a new unsigned file. Awaiting the second delta check of the amended step-8 text.*
