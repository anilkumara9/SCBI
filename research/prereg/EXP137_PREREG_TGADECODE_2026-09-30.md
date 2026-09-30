# Pre-registration: B3 — TGA-DECODE: TGA Channel Decodability

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted (EXP137 provisional only), no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4855 (pre-assigned by the CEO). **Source:** `research/innovation/SPRINT_2026-09-30_POST_TGA.md` §B3 (worth-it gate passed, ranked #4).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #2 (no invented numbers — every constant below is pinned or executor-verified-from-record, never improvised), Law #4 (no post-hoc hypothesis shifts — the bars below are binding; non-resurrection audit §6), Law #6 (frozen backbone Δθ=0 — vacuous here: zero forwards are run), Law #7 (zero data leakage — the projection direction was derived without bench labels; §1.2), Law #9 (metrics registered before any output is inspected), Law #11 (observation vs interpretation separated throughout), Law #13 (deterministic reproducibility — seeds, hashes pinned below), Law #15 (worth-it gate §5).

**Epistemological labels** per `AGENTS.md` §5 ([HYPOTHESIS], [FACT], [OBSERVATION], [ASSUMPTION], [CONJECTURE], [DEFINITION], [INTERPRETATION]) are used throughout.

---

## 0. The breaking point (read first)

**[HYPOTHESIS]** The TGA leading direction v̂₁ — the dynamics' maximally-amplified channel (R = 8.24×, EXP127 CONTINUE) — carries task-decodable information, even though injecting along it moves zero decisions (EXP131/133 binding KILLs).

**Breaking point:** 1-NN leave-one-out decode on v̂₁-projected archived embeddings ≤ 8% (vs 5% chance, K=20) → **KILL** "the TGA channel carries task information." The TGA story closes completely: the direction exists (EXP127), carries nothing (this experiment), moves nothing (EXP131/133).

**Drafting corrections (caught here, not by review):**
1. **Projection space is `layers[19]`, not `layers[20]`.** EXP127's v̂₁ is the leading input singular vector of M = ∂x_{24,last}/∂x_{20,last}, where x_{20} = `hidden_states[20]` = input of transformer block 20 (`experiments/runs/EXP127_tga/exp127_execute.py:278`; the EXP131 bundle's program-standard `SITE = 20  # input of block 20 = hidden_states[20]`). The archived EXP092 embedding array indexes `layers[l]` = `hidden_states[l+1]` = output of 0-indexed block l (`experiments/runs/EXP092_ibl/extract_layer_embeddings.py:263-265`). Therefore v̂₁'s native space is archived index **19**, not 20. Projecting onto `layers[20]` would test a different (unlicensed) subspace. The executor asserts the index derivation; §3.5(a) pins it.
2. **Canonical v̂₁, not per-prompt v̂₁.** The archive holds 10 per-prompt v̂₁'s (one per EXP127 decision-set prompt), but the decode bench is the 60-item EXP092-B set — a different prompt set, so per-prompt matching is impossible and per-prompt v̂₁ computation would require new forwards (violating the zero-forwards design). The draft uses the sign-aligned mean direction, licensed by measurement: the 10 archived v̂₁'s have mutual |cosine| ∈ [0.9956, 0.9996], mean 0.9973 **[OBSERVATION]** (computed from the archive during drafting; sign ambiguity is intrinsic to SVD). 1-NN on 1-D projections is sign-invariant (|a·v̂ − b·v̂| = |a·(−v̂) − b·(−v̂)|), so the residual sign ambiguity is decision-irrelevant. Breaking point (b) re-verifies the coherence at runtime; if the archive does not cohere, the canonical-direction premise fails → RUN-INVALID, not a verdict.
3. **B = 10,000 permutations, not 1,000.** EXP092 used B=1,000 for its 24-layer scan. The CONTINUE bar here requires p < 0.00208; with B=1,000 the minimum resolvable p is ≈0.001, leaving almost no headroom below the bar (a true p ≈ 0.001 would be unresolvable). B=10,000 resolves to ≈0.0001. Cost is trivial (10,000 × 60 1-NN lookups on scalars). The seed stream is pinned §3.4.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** The scalar projection of frozen Pythia-410m's layer-20-input residual states onto the canonical TGA leading direction v̂₁ carries task-decodable information about the correct relational answer on the 60-item EXP092-B bench — i.e., the amplifier's channel is informative even though it is causally inert.

**Falsifiers:** per the §4 decision tree — CONTINUE iff 1-NN LOO accuracy ≥ 15% with stratified permutation p < 0.00208; KILL iff accuracy ≤ 8%; HELD iff 8% < accuracy < 15%, or ≥ 15% with p ≥ 0.00208; RUN-INVALID on apparatus failure (§3.5).

### 1.1 Why this experiment exists

EXP127 measured a real distinguished direction: the frozen L20→L24 propagator's leading singular vector v̂₁, median amplification 8.24× over random directions (CONTINUE as measurement, LOG-4699). EXP131 and EXP133 then killed v̂₁ as a *steering* direction — one-shot injection (ĉ = 0.03742 < 0.1, ΔM = 0) and geodesic multistep (ΔM_geo = 0), both with verified delivery (binding KILLs, LOG-4832/4818). But causality's null does not predict decodability's null — that dissociation is the program's central Decodability Gap thesis, externally replicated (arXiv:2609.06951, LOG-4499). Nobody has tested whether v̂₁ *carries* task information. If it decodes at chance, the TGA story closes completely (exists / carries nothing / moves nothing). If it decodes, the distinguished direction is task-aligned and reading-from-TGA designs are licensed — a live direction the steering kills did not touch.

### 1.2 Scope fence: no label contact in the projection (Law #7, Law #11)

**[FACT]** The canonical v̂₁ was derived by EXP127 from the propagator's singular structure alone — no bench labels, no task signal, no EXP092-B contact entered its computation. **[FACT]** The archived embeddings were extracted by EXP092's bundle from frozen forward passes, also label-free as representations. **[INTERPRETATION]** The projection is therefore a label-free linear readout of a label-free direction; the labels enter only at the 1-NN scoring step, exactly as in EXP092's licensed protocol. This is a *decodability* probe, not an autonomous-steering test: a CONTINUE licenses "v̂₁ carries task information" and motivates reading-from-TGA designs; it does **not** license any steering or capability claim — EXP131/133's causal nulls stand untouched regardless of outcome.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Does 1-NN leave-one-out classification on the 1-D v̂₁-projection of archived frozen embeddings exceed chance on the EXP092-B bench (K=20, chance 5%)?

**Decision changed:**
- **CONTINUE** (§4): accuracy ≥ 15% AND stratified permutation p < 0.00208 → "the TGA channel carries task-decodable information"; the TGA-measurement program continues into reading-from-TGA designs (new experiment numbers).
- **KILL** (§4): accuracy ≤ 8% → "the TGA channel carries no task information above the null ceiling"; the TGA story closes completely — direction exists (EXP127), carries nothing (this), moves nothing (EXP131/133).
- **HELD** (§4): 8% < accuracy < 15%, or ≥ 15% with p ≥ 0.00208 → ambiguous; licenses nothing, kills nothing. (A powered follow-up would need a new experiment number, not a bar change.)
- **RUN-INVALID** (§4): apparatus failure — archive hash mismatches, v̂₁ incoherence, ID/label misalignment, degeneracy, ties, or bench-pin mismatch. Never a verdict on the hypothesis.

---

## 3. Method

### 3.1 Archives [FACT / pinned]

No forward passes are executed. All data are read from two committed archives:

- **A1 — direction archive:** `experiments/runs/EXP127_tga/out/exp127_vectors.npz`, SHA-256 `9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc` (pinned in EXP131's pre-reg §7 and re-verified at LOG-4799/4810). Contains 20 keys: 10 × `v1__<prompt_id>` (1024,) float32 — the per-prompt leading input singular vectors — and 10 × `urand__<prompt_id>` (64×1024). Only the `v1__` keys are used.
- **A2 — embedding archive:** `experiments/runs/EXP092_ibl/out/exp092_embeddings.npz`, SHA-256 `9219bd0dd961524e26a7bb570cbc1e67e7fb245f58271415c5cf174dceb95fae` (recorded in the S5_3 report, 2026-09-28; recomputed exact during drafting). Keys: `layers` (24, 60, 1024) float32 — final-token hidden states, `layers[l]` = output of 0-indexed block l; `ids` (60,); `labels` (60,) — 20 unique target entities; `phrasing` (60,) ∈ {A-first, C-first}; `domain` (60,) ∈ {Planetary, Elemental}.

**Δθ=0 [FACT]:** no model is loaded and no forward pass is executed; the backbone cannot change. The Δθ=0 guard is vacuous by construction — recorded here so the Law #14 review need not ask.

### 3.2 Canonical direction construction (deterministic, registered)

1. Load A1; assert SHA-256 and exactly 10 keys matching `v1__*` (breaking point (a)).
2. Stack the 10 vectors V (10, 1024); assert each has nonzero norm.
3. Sign-align: s_i = sign(V_i · V_0), with s_i = +1 if the dot product is exactly 0. (SVD sign ambiguity; 1-NN on 1-D projections is sign-invariant, so this choice cannot affect the verdict — recorded for reproducibility.)
4. v̂₁ = mean(s_i · V_i) / ‖mean(s_i · V_i)‖₂ — the canonical unit direction.
5. Assert the coherence gate: mean pairwise |cosine| over the 45 pairs ≥ 0.99 (breaking point (b); drafting-time measurement: 0.9973).

### 3.3 Projection and statistic (EXP092 protocol, single channel)

1. Load A2; assert SHA-256 (breaking point (c)); assert `layers` shape (24, 60, 1024).
2. Take H = `layers[19]` (60, 1024) — **the v̂₁-native space** (input of block 20; see drafting correction 1, §0). The executor asserts this index derivation in code comments; any other index is a protocol violation.
3. Scalars: s_i = H_i · v̂₁ for i = 1..60 (float64 accumulation; the projection is linear and label-free).
4. **1-NN leave-one-out** (EXP092 §3, single channel): for each i, find j≠i minimizing |s_i − s_j| (Euclidean on 1-D = absolute difference); predict label(j). Accuracy a = (# correct)/60. K=20, chance = 0.05.
5. **Ties:** assert zero exact distance ties across all 60 queries; any tie → RUN-INVALID (breaking point (f); EXP092 §3 precedent — exact float ties on distinct 1024-d projections are measure-zero, so a tie indicates archive corruption).

### 3.4 Null: stratified permutation, B=10,000

- **Strata** (EXP092 §4, reconstructed from A2's `domain` × `phrasing` keys): (Planetary, A-first), (Planetary, C-first), (Elemental, A-first), (Elemental, C-first). Labels permuted **within** strata only. Assert the stratum counts match EXP092 §4's table (16/14/14/16); mismatch → RUN-INVALID (breaking point (d) — the bench behind the archive must be EXP092-B).
- **B = 10,000** permutations (drafting correction 3, §0). RNG: `random.Random(137001 + b)` per permutation b (seed stream pinned; distinct from all program seeds by construction — 137001 is unused in the log).
- p = (1 + #{b : a^{(b)} ≥ a}) / (1 + B). q95 = 95th percentile of the permutation accuracies (reported, non-binding).
- **ID/label alignment:** assert A2's `ids` are 60 unique EXP092-B ids and `labels` are exactly the 20 registered target entities; the executor cross-checks 5 spot ids against the EXP092-B bench pin `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4` (breaking point (d)).

### 3.5 Breaking points (all → RUN-INVALID, exit 44; none is a verdict)

| ID | Trip condition |
|---|---|
| (a) Direction-archive integrity | A1 SHA-256 ≠ `9b527c…13dc`, or ≠10 `v1__` keys |
| (b) v̂₁ coherence | sign-aligned mean pairwise \|cosine\| < 0.99 (canonical-direction premise fails) |
| (c) Embedding-archive integrity | A2 SHA-256 ≠ `9219bd…95fae`, or `layers` shape ≠ (24, 60, 1024) |
| (d) Bench alignment | stratum counts ≠ 16/14/14/16, or ids/labels fail the EXP092-B spot check |
| (e) Degeneracy | the 60 scalars have zero variance (instrument cannot discriminate) |
| (f) Ties | any exact 1-NN distance tie on the 1-D scalars |
| (g) Label-count | ≠20 unique labels in A2 (the K=20 chance baseline would be wrong) |

### 3.6 Secondary statistics (pre-registered, non-binding)

- **S1 (full-vector 1-NN at layers[19]):** 1-NN LOO on the unprojected 1024-d `layers[19]` embeddings — asks whether the *space* (not the v̂₁ channel) carries information. Cannot override the primary verdict; reported for interpretation only.
- **S2 (random-direction controls):** the same 1-D 1-NN procedure along 8 seeded random unit vectors (`np.random.default_rng(137002)`, normalized) — calibrates what "1-D projection decode" looks like under the null geometry. If v̂₁'s accuracy is inside the random-direction spread, the CONTINUE interpretation weakens (recorded, non-binding).

---

## 4. Decision table (binding)

Let a = 1-NN LOO accuracy on the v̂₁-projected scalars (n=60, K=20, chance 5%), p = stratified permutation p-value (B=10,000).

- **CONTINUE:** a ≥ 0.15 (≥9/60) **AND** p < 0.00208 → "the TGA leading channel carries task-decodable information (1-NN, permutation-significant at the EXP092 family-wise bar)." Licenses reading-from-TGA designs (new experiment numbers). **[NOTE]** 0.00208 = 0.05/24 is EXP092's 24-layer Bonferroni bar, stricter than the single-test 0.05. It is adopted deliberately: B3 must clear the same evidential bar as the discovery experiment that produced the bench, so a CONTINUE cannot be manufactured by a weaker bar. The Law #14 review may challenge this choice; the draft does not hide it.
- **KILL:** a ≤ 0.08 (≤4/60) → "the TGA channel carries no task information above the null ceiling." The TGA story closes completely: exists (EXP127) / carries nothing (this) / moves nothing (EXP131/133).
- **HELD:** 0.08 < a < 0.15, **or** a ≥ 0.15 with p ≥ 0.00208 → ambiguous; licenses nothing, kills nothing.
- **RUN-INVALID:** any §3.5 breaking point trips. Never a verdict on the hypothesis.

The three bars are disjoint and exhaustive over (a, p) space. No post-hoc re-binning (Law #4).

---

## 5. Worth-it gate (Law #15, 7 points)

1. **Exact question:** Does the TGA leading direction v̂₁ carry task-decodable information (1-NN decode on v̂₁-projected archived embeddings vs 5% chance)?
2. **Decision changed:** CONTINUE the TGA-measurement program into reading-from-TGA designs vs KILL it — the TGA story closes completely (exists / carries nothing / moves nothing).
3. **Cheapest test + cost:** project archived frozen embeddings onto the canonical v̂₁ → 60 scalars; EXP092's licensed 1-NN + permutation protocol. **$0 CPU, ~15 min, zero new forwards** (two npz loads + 10,001 × 60 scalar 1-NN lookups).
4. **Mathematical license:** [THEOREM] 1-NN LOO accuracy is a finite-sample lower bound on mutual information via Fano's inequality (EXP092 §1, re-derived for K=20); [OBSERVATION] EXP127's v̂₁ (R = 8.24×, distinguished); [OBSERVATION] the 10 archived v̂₁'s cohere at |cosine| ≥ 0.9956 (canonical direction exists). **Quantitative prediction:** if task-aligned, a ≥ 15% with p < 0.00208; if task-orthogonal (as the injection nulls suggest), a ≤ 8%.
5. **Breaking point:** a ≤ 8% → KILL "the TGA channel carries task information" (§4).
6. **Non-resurrection audit:** §6 — decodability is a different claim class from the killed steering claims; no executed decode on v̂₁ exists.
7. **Summit filter:** B3 closes the program's flagship measurement story at $0. A CONTINUE would hand the program its first task-aligned distinguished direction — the raw material for reading-based (not steering-based) designs. No consciousness/superhuman/capability claim is made or licensed.

---

## 6. Non-resurrection audit (Law #4)

| Killed / fenced family | Why B3 is not a resurrection |
|---|---|
| EXP131 (one-shot v̂₁ injection KILL) / EXP133 (geodesic multistep KILL) | Killed claims are **causal** (pushing along v̂₁ moves decisions). B3 tests **decodability** (v̂₁-projection carries label information) — a different claim class under the program's Decodability Gap dissociation (decodability ≠ steerability; externally replicated arXiv:2609.06951, LOG-4499). A null here closes the story; a positive does not revive the injection claims. |
| EXP092's layer-wise decode results | EXP092 decoded **full-layer embeddings** (1024-d, all 24 layers). B3 decodes a **1-D v̂₁ projection** — a strictly narrower channel that no experiment has probed. |
| S5-3 "never-decodable" PIVOT | Fenced **semantic/static directions and decode rooms** (S5_3_REPORT_2026-09-28). v̂₁ is a dynamics-derived direction, a Law-#4-new direction class (LOG-4693 seventh-item record). |
| EXP094/095/096 (L11 injection kills) | Injection (causality) at a different site; B3 involves no injection at any site. |
| EXP098 (multi-site composition PIVOT) | Composition injection; B3 involves no injection. |

**Staleness re-diff (LOG-4834/4838 lesson, executed before drafting):** full-log grep for any executed 1-NN (or any) decode on v̂₁-projected or TGA-direction-projected embeddings — **clean**. EXP127 measured v̂₁ (amplification) but never decoded it; the log's 1-NN decodes (EXP092, S5-3) never touched v̂₁; the B3 bet's own dossier notes cross-layer TGA decode as subsumed, not executed. No EXP137/138 mentions exist. The bet is unexecuted.

---

## 7. Launch chain and licensing

**This draft licenses nothing.** Next: independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under minted EXP137 (provisional; next free number after EXP136).

**Reviewer attention requested:** (1) the p < 0.00208 bar choice (§4 NOTE — stricter than the single-test 0.05; deliberate, challengeable); (2) the sign-alignment rule §3.2 step 3 (decision-irrelevant by 1-NN sign-invariance, but confirm); (3) the `layers[19]` index derivation (drafting correction 1 — the highest-stakes detail in the draft); (4) whether S2's 8 random directions need a matched-norm or any-norm specification (they are unit-norm by construction; confirm sufficiency).

---

*End of B3/TGA-DECODE draft pre-registration. Stops here per the single-lane fence.*
