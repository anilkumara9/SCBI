# S7-4 Pre-registration — DRAFT: EXP136 HELD powered follow-up (attention-routing)

**Status:** SIGNED. Independent Law #14 review returned SIGN-WITH-FIXES (re-review required); all three required fixes + both advisories applied by the repair lane; independent fix-verification re-review returned binding PASS (all fixes verified from independent recomputation; no further review needed). The CEO signs on the re-review's authority.
**Drafting lane:** S7-4 (J10), licensed HELD follow-up of EXP136; born at the Monday session 2026-10-05 (LOG-4911); backlog row `research/innovation/CANDIDATE_BACKLOG.md:35`.
**Experiment number:** EXP146 (minted by the CEO at execution authorization, 2026-10-05 — new protocol = new number per the single-lane fence).
**Parent outcome [FACT]:** EXP136 (B4/ARI) returned a binding HELD verdict (LOG-4853, independent verdict review): T1 (span-boost, one-sided b>c) b=0/c=1, p=1.0; T2 (span-ablate, one-sided c>b) b=3/c=4, p=0.5; C (uniform, two-sided) b=1/c=4, p=0.375. All guards PASS, (h) hook-delivery PASS on both hooks, Δθ=0, 242 forwards. The verdict review's honest observation [INTERPRETATION]: "the flip pattern is symmetric noise, not a lurking signal — T2's 7 flips split b=3/c=4 (net movement ≈ 0), and T1's single flip is a *worsening* (c=1, b=0), opposite to its predicted direction."

**Governing laws:** Law #2 (no invented numbers — every constant below is pinned or computed from the EXP136 records, never improvised), Law #4 (no post-hoc shifts — the bars below are binding; the EXP136 bars are inherited, not re-read), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — bench labels never touch the intervention), Law #9 (metrics registered before any output is inspected), Law #11 (observation vs interpretation separated throughout), Law #13 (deterministic reproducibility), Law #15 (worth-it gate §1).

**Epistemological labels** per `AGENTS.md` §5 ([HYPOTHESIS], [FACT], [OBSERVATION], [ASSUMPTION], [CONJECTURE], [DEFINITION], [INTERPRETATION]) are used throughout and are load-bearing.

---

## 0. The question (read first)

**[HYPOTHESIS]** EXP136's HELD verdict reflects underpowering, not absence: a small real directional attention-routing effect exists but n=60 could not separate it from symmetric noise.

**Breaking point:** On pooled n=120, both routing arms show McNemar directional p ≥ 0.1 with the 95% CI for the directional net rate lying entirely below +10pp, and (h) PASS on both hooks → **KILL** the routing-around hypothesis (scoped: as a ≥10pp steering path — §4). The routing-around account of the nulls is dead; the nulls are not routable-around.

**What this draft does not do:** it does not re-read EXP136's bars (Law #4 — EXP136's HELD stands as registered); it does not change the intervention, the model, or the arms; it does not license any new bench family (Bench 2 is the same family, §5.3).

---

## 1. Worth-it gate (Law #15, 7 points)

1. **Exact question [HYPOTHESIS]:** Was EXP136 (n=60) underpowered for a small real directional attention-routing effect, or is the routing-around hypothesis dead? Concretely: on n=120 pooled across two benches, does direct L20 attention reweighting move frozen Pythia-410m decisions in the predicted direction (T1: b>c; T2: c>b)?
2. **Decision changed:**
   - **CONTINUE** (§4): pooled directional McNemar p < 0.05 with same-direction replication on both benches and a null uniform control → "attention is a steerable substrate" survives; the routing-around hypothesis lives; routing-aware G/E/S designs licensed (the program's first operator-class positive).
   - **KILL** (§4): no directional signal (p ≥ 0.1), 95% CI excludes ≥10pp, (h) PASS → the routing-around hypothesis is dead as a ≥10pp steering path; the verified-delivery nulls cannot be routed around.
   - **HELD** (§4): everything else — sub-significant signals, CIs too wide, unattributable effects, heterogeneity. Licenses nothing, kills nothing.
   - **RUN-INVALID** (§4): apparatus failure. Never a verdict.
3. **Cheapest test:** identical EXP136 protocol (same model, revision, β=3.0 boost, span-ablate, uniform control, eager backend, (h) two-phase hook-delivery control, all §5.7 guards) on n=120 = 60 (fresh Bench 1, seed 7401) + 60 (fresh Bench 2, seed 7402), both in the EXP092 family, mutually disjoint and disjoint from EXP092-B (§5.2–5.3). 4 arms × 120 items = 480 decision forwards + 2 probes = 482 total. $0 CPU.
4. **Cost:** $0 CPU, ~8–12h at the EXP136 rate (~1–1.5 min/forward; EXP136 ran 242 forwards).
5. **Mathematical license:** (a) Attention as the transformer's routing mechanism [DEFINITION] — post-softmax weights are the convex combination coefficients selecting which positions' values reach the residual stream; reweighting them IS re-routing by definition (inherited from EXP136 §5.5). (b) Power license [FACT — computed §2]: exact binomial McNemar power at n=120 gives 80% power at ~9pp net directional effect (pooled); the KILL bar fires with 73–92% joint probability under null-like symmetric noise (86–96% per arm; joint = square under cross-arm independence — §2.3); the KILL bar's 10pp exclusion threshold is aligned with the MDE80. (c) The routing-around hypothesis [HYPOTHESIS] predicts the verified-delivery null pattern as its signature — this follow-up is the powered test of its constructive half.
6. **Quantitative prediction:** If the routing-around hypothesis is real at a decision-relevant scale: T1 pooled b−c ≥ +10 (one-sided p < 0.05) with b>c on both benches, OR T2 pooled c−b ≥ +10 (one-sided p < 0.05) with c>b on both benches, while C stays null (two-sided p > 0.05). If it is dead: pooled directional p ≥ 0.1 on both arms with 95% CI upper bounds below +0.10.
7. **Breaking point:** §0 — KILL on powered null with (h) PASS; the bar bites (P ≈ 0.73–0.92 joint, 0.86–0.96 per arm, under symmetric noise at EXP136-like flip rates — §2).

---

## 2. Power analysis (the license for N=120) [FACT — exact binomial computation, no model runs]

All power figures below are exact (binomial enumeration over discordant-pair counts, α=0.05 one-sided), computed from first principles in the drafting lane. q = per-item flip probability in the predicted direction; r = per-item flip probability against; net = q−r.

### 2.1 Exact power: one-sided McNemar

| q (predicted) | r (against) | net | n=60 (EXP136) | n=120 (S7-4) |
|---|---|---|---|---|
| 0.06 | 0.02 | 0.04 | 0.118 | 0.331 |
| 0.08 | 0.02 | 0.06 | 0.249 | 0.582 |
| 0.10 | 0.02 | 0.08 | 0.401 | 0.781 |
| 0.10 | 0.04 | 0.06 | 0.211 | 0.466 |
| 0.12 | 0.03 | 0.09 | 0.430 | 0.791 |
| 0.15 | 0.03 | 0.12 | 0.627 | 0.930 |

**Reading [INTERPRETATION]:** EXP136 (n=60) had only ~40% power for an 8pp true effect — a ~60% chance of missing it. That is the "underpowered" the S7-4 question asks about, and it is real. At n=120, power for 8–9pp rises to ~78–79%.

### 2.2 Minimum detectable effect (MDE80)

At n=120 with r=0.03 background flip rate, exact power crosses 80% between net=0.09 (0.791) and net=0.10 (0.851). **MDE80 ≈ 9–10pp net directional effect** (pooled p<0.05 bar alone).

The full CONTINUE bar (§4) adds two guards — same-direction replication on both benches and the C-attribution null. Under the fresh+fresh design (Fix 1a) the two benches are i.i.d. 60-item draws, so the replication requirement is a genuine joint across two free benches (unlike the fixed-Bench-1 design, where T1's Bench-1 sign was predetermined as b=0,c=1 from EXP136). Monte Carlo over the binomial model (seed 20261005, 80k reps, exact McNemar per §2.1 convention) gives the bar-level operating characteristics [FACT — computed in the repair lane]:

| Truth (both routing arms) | P(CONTINUE fires) |
|---|---|
| True 9pp directional effect | 0.94 |
| True 3pp directional effect | 0.32 |
| Null, symmetric 3% flips | 0.031 (false-CONTINUE) |
| Null, symmetric 6% flips | 0.048 (false-CONTINUE) |

[INTERPRETATION]: the replication and attribution guards are the price of a credible CONTINUE; the draft states the cost plainly rather than hiding it. The 80% power threshold is cleared at 9pp for the full bar (per-arm: ~0.77–0.79) — a decisive improvement over EXP136's ~40% at 8pp. The false-CONTINUE rate under null-like noise is 3–5%, consistent with the bar's α=0.05 components.

### 2.3 KILL-bar operating characteristics (simulation, n=120 pooled per arm)

P(KILL fires) = P(the §4 KILL conjunction holds on **BOTH** routing arms T1 AND T2). Per-arm P(conjunction met) = P(directional one-sided p ≥ 0.1 AND two-sided p ≥ 0.1 AND 95% CI upper < 0.10). The joint is the product under cross-arm independence:

| Truth (both arms) | P(KILL fires, joint) | Per-arm marginal |
|---|---|---|
| Null, symmetric 2% flips | **0.92** | 0.959 |
| Null, symmetric 3% flips | **0.88** | 0.937 |
| Null, symmetric 6% flips | **0.73** | 0.855 |
| True 8pp directional effect (both arms) | **0.008** | 0.089 |
| True 3pp directional effect (both arms) | **0.41** | 0.642 |

[FACT — computed]: joint = per-arm² under cross-arm independence. The per-arm marginals are the drafting-lane simulation values (n=120 pooled per arm); the independence product is validated by direct joint Monte Carlo (repair lane, seed 20261005, 80k reps): 0.880 / 0.731 / 0.409 at null-3% / null-6% / true-3pp — matching the products to 3 decimals. [CAVEAT — cross-arm correlation]: the two routing arms share the same base (B) decisions, so their flip patterns may be positively correlated; positive correlation raises P(both fire) above the independence product. The product is therefore the **conservative (lower)** figure for the KILL bar's power under null-like noise. [NOTE — advisory (ii)]: the "True 3pp/8pp" rows put the directional effect on **both** arms; a mixed truth (effect on one arm only) gives a joint between the per-arm marginal and the square.

**Reading [INTERPRETATION]:** under null-like symmetric noise (the EXP136 pattern: T2 flipped 11.7% with zero directionality), the KILL bar fires with 73–92% joint probability (86–96% per arm) — it is well-powered, not vacuous. Under a true 8pp effect on both arms, false-KILL is <1% — the bar does not kill real effects. Under a true 3pp effect on both arms, KILL fires 41% of the time — which is CORRECT per the bar's definition (3pp < 10pp), but it means the KILL verdict must be scope-qualified (§4): it rules out ≥10pp directional routing effects, not all sub-10pp effects.

### 2.4 Honest conclusion on N=120

**N=120 is sufficient for the registered bars, and the draft states its blind spot plainly:**
- The KILL bar (exclude ≥10pp) is powered at 73–92% (joint two-arm; 86–96% per arm) under null-like noise. If the routing-around hypothesis is dead, S7-4 will very likely KILL it.
- The CONTINUE bar detects ≥9pp directional effects with ~94% power (full bar; ~77–79% per arm) — a decisive improvement over EXP136's ~40% at 8pp.
- **Blind spot [FACT]:** net directional effects of 3–6pp are not reliably separable at n=120 (power 30–55%). The draft does not pretend otherwise.
- **Why the blind spot is acceptable [INTERPRETATION]:** the registered bars define the decision-relevant effect sizes. A sub-6pp routing effect would not license routing-aware G/E/S designs (the entire point of CONTINUE) — it would sit below the noise floor EXP136 already measured (11.7% symmetric flips on T2). The KILL verdict is explicitly scoped to ≥10pp (§4); sub-10pp effects are declared out-of-scope, not ruled out.
- **What would change this assessment [FACT]:** reducing the MDE80 to ~6pp would require n≈270 (≈1080 forwards), 2.25× the licensed budget — a different proposal, not this one. The backlog licenses N≈120 / ≈480 passes; the power math confirms N=120 separates the hypotheses AS REGISTERED.

---

## 3. Frozen decision bars (restated exactly from the backlog row)

Backlog row `research/innovation/CANDIDATE_BACKLOG.md:35` (S7-4, J10), verdict column, verbatim:

> McNemar p ≥ 0.1 with CI excluding ≥10pp → KILL the routing-around hypothesis; directional flips replicating across two benches p < 0.05 → CONTINUE

**Operational definitions** (operationalization, not modification — the Law #14 reviewer rules on faithfulness):
- "McNemar p ≥ 0.1": the one-sided directional McNemar exact p-value (T1: H1 b>c; T2: H1 c>b, inherited from EXP136 §3.3) computed on pooled n=120, is ≥ 0.1 for the arm.
- "CI excluding ≥10pp": the 95% Wald CI for the directional net flip rate δ̂=(b−c)/n (T1) or δ̂=(c−b)/n (T2), SE=√[(b+c)−(b−c)²/n]/n, lies entirely below +0.10 (upper bound < 0.10).
- "directional flips replicating across two benches p < 0.05": pooled one-sided directional McNemar p < 0.05 AND the same directional sign on each bench separately (T1: b>c on Bench 1 and Bench 2; T2: c>b on Bench 1 and Bench 2). [NOTE]: this operationalizes "replicating" as directional agreement, not per-bench significance — requiring p<0.05 independently on each n=60 bench would give only ~16% joint power at 8pp (exact: per-bench power 0.398 at q=0.10, r=0.02, n=60 per §2.1 convention; joint = 0.398² = 0.158 under bench independence — exact binomial enumeration, same method as §2.1), defeating the follow-up's purpose. The choice and its cost are stated here for review, not hidden.
- The KILL reading is scoped: "KILL the routing-around hypothesis **as a ≥10pp steering path**" — sub-10pp effects are out of scope, not ruled out (§2.3).

---

## 4. Decision table (binding)

Precedence: RUN-INVALID > HELD > KILL > CONTINUE (a tripped guard voids everything; an inconclusive configuration is HELD, never KILL; KILL requires the full powered-null conjunction).

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | (T1 pooled one-sided b>c p < 0.05 OR T2 pooled one-sided c>b p < 0.05) AND (same directional sign on Bench 1 and Bench 2 for the significant arm) AND (C pooled two-sided p > 0.05) | Routing-specific steering signal replicating across benches; attention is a steerable substrate; routing-aware G/E/S designs licensed |
| KILL | For EACH routing arm (T1, T2): (i) pooled directional one-sided p ≥ 0.1, AND (ii) pooled two-sided p ≥ 0.1 (no significant anti-directional effect — else HELD), AND (iii) 95% CI upper bound < 0.10, AND (iv) (h) PASS on both hooks; AND (v) no qualitative heterogeneity (neither bench significant at p<0.05 in the opposite direction of the other) | The routing-around hypothesis is dead as a ≥10pp steering path; the verified-delivery nulls are not routable-around. Sub-10pp effects out of scope, not ruled out. |
| HELD | Any configuration meeting neither CONTINUE nor KILL: sub-significant directional signals; CIs too wide to exclude 10pp; significant anti-directional effects; unattributable signals (routing arm(s) AND C significant); qualitative bench heterogeneity; routing arms null but the powered-KILL conjunction incomplete | Inconclusive; licenses nothing, kills nothing, fences nothing |
| RUN-INVALID | Any §5.6 guard trips | Apparatus failure; never a verdict on the hypothesis |

**Replication-clause satisfiability [FACT — Fix 1a]:** both benches are fresh i.i.d. 60-item draws (§5.2–5.3), so the per-bench directional signs are free on both arms — the CONTINUE replication clause is satisfiable for T1 and for T2. This resolves the contradiction in the earlier draft, where Bench 1 was the fixed EXP092-B bench: under determinism T1's Bench-1 sign was predetermined as b=0,c=1 (EXP136's observed flips), making the replication clause unsatisfiable for T1 while satisfiable for T2.

**C-arm attribution note** (EXP136 §4 A2, inherited): if C is significant (two-sided p ≤ 0.05) while both routing arms meet the KILL conjunction, the verdict is **KILL** — "if the undirected control moves decisions but the directed arms do not, routing is not the lever" [INTERPRETATION]. If a routing arm is significant AND C is significant, the verdict is **HELD** (unattributable).

**Explicit non-firing:** "ΔM=0" alone is NOT a KILL condition in S7-4 (it was EXP136's strict bar and did not fire); the powered KILL conjunction above replaces it. Law #4: no re-reading EXP136's bar.

---

## 5. Protocol (identical EXP136, two benches)

### 5.1 Backbone, model, environment [FACT — pinned, identical to EXP136]

- **Backbone:** frozen Pythia-410m, `device_map="cpu"`, float32, `model.eval()`, `torch.no_grad()` around ALL forwards. CPU-only by design ($0).
- **Attention backend:** `attn_implementation="eager"` on ALL arms including base (SDPA emits no attention weights — the EXP100/101 preflight).
- **Δθ=0 procedure:** SHA-256 over tensor bytes with sorted `state_dict` keys, float32 (EXP077/EXP084/EXP108 canonical convention). Asserted before the first forward and after the last; mismatch → RUN-INVALID, exit 44. Expected pin: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331).
- **HF revision:** `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` (the EXP136-resolved revision; resolved programmatically at execution, never transcribed).
- **Environment (Law #13):** torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3; `torch.manual_seed(136013)` (identical seeds discipline — the intervention is deterministic given weights).
- **Law #7:** bench ground-truth labels used nowhere — not in the intervention (span annotations are prompt-structure metadata per EXP136 §1.2), not in the endpoint (ŷ = argmax over the full vocabulary at the answer position), not in any selection.

### 5.2 Bench 1: fresh 60, same family [FACT — built and pinned in the repair lane]

- **Construction:** 60 fresh items built with the committed EXP092 bench machinery (`reference_implementation`, read-only import — zero transcription drift, the S7-2b precedent) with exactly one documented delta: fresh tuple draws via `random.Random(7401)` (seed pinned). Unchanged from the committed procedure: PLANET_VOCAB / ELEMENT_VOCAB, the FIX 1 phrasing rule, the FIX 2 option-order rule, the prompt templates, the strata structure (15 triples + 15 quads per domain → 16/14/14/16 per domain×phrasing), within-tuple entity distinctness, and the G0 target-balance (each entity the target exactly 3× per domain). Derivation script: `research/analysis_plans/S7-4_build_benches_2026-10-05.py`; bench JSON: `research/analysis_plans/S7-4_BENCH1_2026-10-05.json`.
- **Freshness:** tuple sets disjoint from EXP092-B and from Bench 2 (per domain/kind); surface-diff audit: all 60 Bench-1 prompts pairwise distinct and distinct from all 60 EXP092-B prompts (asserted in the derivation script; recorded in `S7-4_BENCH_MANIFEST_2026-10-05.json`).
- **Pinning:** SHA-256 over the committed canonical serialization (`reference_implementation.bench_sha256`). Bench 1 pin: `83af7daa5596f351f0412ab4938ec4d3eb70477aad12915de6b7851b73a05eb5` — character-verified by independent recompute from the built bench JSON (all 64 hex chars identical); G0 PASS (n=60, unique tuples, strata 16/14/14/16). `len == 60` asserted at execution; pin mismatch → RUN-INVALID, exit 44.
- **Span annotations:** one entity-span per item, S6-3c protocol (1 ≤ E_i < N_i, E_i/N_i ≤ 0.5, span excludes the final token), derived at execution by the committed EXP136 span procedure (`run_exp136.py` `entity_span_token_idx`, read-only); >6 exclusions pooled across both benches → RUN-INVALID, exit 44. [NOTE]: span derivation is execution-time (as in EXP136, which had 0 exclusions on EXP092-B); the templates and vocabularies are unchanged from the committed bench, so span geometry is structurally identical.
- [NOTE — Fix 1a]: the "direct reproducibility of EXP136" framing is retired. Bench 1 is a fresh draw, not EXP136's bench; no EXP136 data are reused or pooled — all 120 items receive fresh forwards.

### 5.3 Bench 2: fresh 60, same family [FACT — built and pinned in the repair lane]

- **Construction:** 60 fresh items built by the same derivation as Bench 1 (§5.2; `research/analysis_plans/S7-4_build_benches_2026-10-05.py`) with tuple-draw seed `random.Random(7402)` (pinned); bench JSON: `research/analysis_plans/S7-4_BENCH2_2026-10-05.json`. Same committed machinery (vocabularies, FIX 1 / FIX 2, templates, strata, G0 target-balance); the only delta from the committed procedure is the fresh tuple draws.
- **Span annotations:** one entity-span per item per the S6-3c protocol (1 ≤ E_i < N_i, E_i/N_i ≤ 0.5, span excludes the final token), derived at execution by the committed EXP136 span procedure (as in §5.2).
- **Freshness:** tuple sets disjoint from EXP092-B and from Bench 1 (per domain/kind); item IDs (`s74_b2_*`) disjoint by construction; surface-diff audit: all 60 Bench-2 prompts pairwise distinct, distinct from all 60 EXP092-B prompts and all 60 Bench-1 prompts (asserted in the derivation script; recorded in the manifest).
- **Pinning:** SHA-256 over the committed canonical serialization (`reference_implementation.bench_sha256`); **pre-registered in the signed plan before execution** (the S7-2b precedent). Bench 2 pin: `c7d280ebc9a0eb6d6c761b91557570159671a842754792355b013ec0f695048b` — character-verified by independent recompute from the built bench JSON (all 64 hex chars identical); G0 PASS. The execution lane asserts the pin at Step 0 (S0.1); mismatch → RUN-INVALID, exit 44.
- **Strata/degeneracy pre-checks:** G0 bench-provenance (uniqueness, balance, strata) via the committed verifier — PASS on both benches; per-item B-decision variance > 0 checked at execution (no degenerate bench).

### 5.4 The four arms (pinned, identical to EXP136 §3.2)

Per included item i, at the final prompt (answer) position q_i, on each bench separately (n=60 per bench, pooled n=120 for the endpoint):

- **B — base:** eager-attention forward, no hook. Reference for all contrasts.
- **T1 — span-boost:** post-softmax L20 attention weights reweighted w̃_t = 3·w_t for t ∈ span_i, renormalized. β=3.0 single pre-registered factor (inherited).
- **T2 — span-ablate:** w̃_t = 0 for t ∈ span_i, renormalized.
- **C — uniform-reweight:** w'_t = 1/T_i (undirected control).

### 5.5 Endpoint and statistics (Law #9, inherited with pooling)

- **Primary endpoint:** per-arm decision-flip rate vs base on pooled n=120, ΔM_arm = (1/120)Σ_i **1**[ŷ_i^{arm} ≠ ŷ_i^{B}], and the paired McNemar exact test per arm vs base with the registered directional alternatives (T1: one-sided b>c; T2: one-sided c>b; C: two-sided). [NOTE]: the directional alternatives test the pre-registered predictions; systematic effects in the unpredicted direction do not license CONTINUE (Law #4).
- **Replication check:** directional sign per bench (b>c / c>b) recorded for each routing arm; required for CONTINUE (§4).
- **CI:** 95% Wald CI for the directional net rate per routing arm (pooled); required for KILL (§4).
- **Secondary (registered, non-binding):** per-bench McNemar p-values (diagnostic only — they do not trip any bar alone).

### 5.6 The (h) hook-delivery positive control (mandatory, identical to EXP136 §3.4)

Two-phase (h) on the first included Bench-1 item, N_h = 2 probes, all 13 asserts from EXP136 §3.4 (Phase 1 T2: span mass < 1e-6, renorm < 1e-5, L1 > 0.01, A1 output propagation; Phase 2 T1: L1 > 0.01, span mass boosted vs base and > 1e-3, renorm, A1). Any assert fails → RUN-INVALID, exit 44, zero decision forwards. [INTERPRETATION]: a KILL without proven delivery is invalid — the (h) is a validity condition on the KILL conjunction, not a nicety.

### 5.7 Guards and breaking points (trip conditions + exit codes; adapted to n=120)

- **(a) Δθ=0:** pre/post SHA-256 mismatch → RUN-INVALID, exit 44.
- **(b) B-decision archive and non-degeneracy:** per-item B decisions on both fresh benches recorded to the run manifest for the archive; base decisions non-degenerate (both answer options chosen across pooled n=120); any NaN → RUN-INVALID, exit 44. [NOTE — Fix 1a]: the EXP094-B 60/60 agreement check applied only to the fixed-Bench-1 design and is retired with it; apparatus validity is carried by guards (a), (d), and the §5.1 seed discipline.
- **(c) Bench + span pins:** either bench SHA-256 mismatch (Bench 1: `83af7daa5596f351f0412ab4938ec4d3eb70477aad12915de6b7851b73a05eb5`; Bench 2: `c7d280ebc9a0eb6d6c761b91557570159671a842754792355b013ec0f695048b`), len ≠ 60, or >6 span-condition exclusions pooled → RUN-INVALID, exit 44.
- **(d) Hook-delivery (h):** any §5.6 assert fails → RUN-INVALID, exit 44.
- **(e) Renormalization/NaN:** asserted per hooked forward; violation → RUN-INVALID, exit 44.
- **(f) Budget audit:** forward ledger must equal 4×120 (B, T1, T2, C) + N_h=2 probes = 482 ± 0 accounted passes; any unaccounted forward → RUN-INVALID, exit 44.
- **(g) Clean completion:** all guards pass → executor computes the endpoint, prints the verdict per §4, exit 0.

---

## 6. Non-resurrection audit (Law #4)

- EXP136's HELD verdict stands as registered; this draft does not re-read its bars (§4 explicit non-firing note).
- No execution has intervened on attention weights except EXP136 itself (this is its powered follow-up, not a resurrection — HELD licenses a powered retest by the backlog row).
- The S6 "no fifth externally-computed attention-gate variant" fence covers attention-as-gate, not attention-as-intervention-target (EXP136 §6, inherited).
- G1, EXP131/133, EXP105 distinctions inherited from EXP136 §6 — different question classes, unaffected.

---

## 7. Launch chain and licensing

This draft licenses nothing. The Law #14 review of this exact file may demand fixes; fixes get independent fix-verification; only then does the CEO decide on launch and mint a **NEW experiment number** (protocol extension to two benches = new number per the single-lane fence — not minted here). The executor follows §5 exactly; any deviation trips a §5.7 guard. $0 CPU only; frozen backbone Δθ=0.

---

*Draft: S7-4 pre-registration lane, 2026-10-05. $0 CPU, paper only. No experiment number minted.*
