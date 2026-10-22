# Pre-registration: B4 — ARI: Attention-Routing Intervention

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted (EXP136 provisional only), no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4848 (pre-assigned by the CEO). **Source:** `research/innovation/SPRINT_2026-09-30_POST_TGA.md` §B4 (worth-it gate passed, ranked #3).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #2 (no invented numbers — every constant below is pinned or executor-verified-from-record, never improvised), Law #4 (no post-hoc hypothesis shifts — the bars below are binding; non-resurrection audit §6), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — bench labels never touch the intervention; §1.2 scope fence), Law #9 (metrics registered before any output is inspected), Law #11 (observation vs interpretation separated throughout), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below), Law #15 (worth-it gate §5).

**Epistemological labels** per `AGENTS.md` §5 ([HYPOTHESIS], [FACT], [OBSERVATION], [ASSUMPTION], [CONJECTURE], [DEFINITION], [INTERPRETATION]) are used throughout.

---

## 0. The breaking point (read first)

**[HYPOTHESIS]** Directly reweighting attention — the model's information-routing substrate — moves frozen decisions where every residual-content intervention has moved nothing.

**Breaking point:** ΔM = 0 on both routing arms (T1 span-boost, T2 span-ablate) vs base, with the hook-delivery control (h) PASS on both hooks (§3.4 Phases 1–2) → **KILL** "attention-routing intervention steers decisions." The routing-around hypothesis is dead as a steering path; the verified-delivery nulls are not routable-around.

**Drafting corrections (caught here, not by review):**
1. **n = 60, not 10.** The sprint bet specified "10 prompts" with a CONTINUE bar of McNemar one-sided p ≤ 0.05. On n = 10, the exact one-sided McNemar needs b ≥ 5, c = 0 (p = 0.03125) — a 50% flip rate — while the sprint's own quantitative prediction is "≥ 2/10 decisions." The design is underpowered for its own prediction: at a true 20% flip rate, P(0/10 flips) ≈ 0.107, an 11% false-KILL risk. The draft uses the full 60-item bench (the program's standard), where the bars below are powered. Cost corrected §5.4.
2. **One annotated span, not target+foil.** The sprint's "boost target-token / ablate foil-token" assumes two annotated spans; the licensed bench carries ONE entity-span annotation per item (S6-3c §2, foundation gate iii). No span is invented (Law #2). T2 therefore ablates the annotated span (routing AWAY from the task-relevant entity) rather than a foil span. The routing hypothesis is probed bidirectionally regardless.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** Reweighting layer-20 attention at the answer position — boosting weight on the annotated entity span (T1) or ablating it (T2) — changes frozen Pythia-410m decisions on the 60-item EXP092-B bench, where residual-stream injection at the same layer moves nothing (EXP131 binding KILL, LOG-4832).

**Falsifiers:** per the §4 decision tree — CONTINUE if either routing arm moves decisions in its predicted direction (T1: McNemar one-sided b>c p ≤ 0.05; T2: one-sided c>b p ≤ 0.05) vs base while the uniform control does not (two-sided p > 0.05); KILL if ΔM = 0 on both routing arms with (h) PASS on both hooks; HELD if the uniform control also moves decisions (unattributable) or the effect is sub-significant; RUN-INVALID on apparatus failure (§3.6).

### 1.1 Why this experiment exists

Every killed intervention in program history added content to the residual stream (h' = h + αv: EXP077 cones, EXP093/094/095/096 L11 injections, EXP131 TGA-v̂₁, EXP133 geodesic) or masked logits (EXP105). None touched the model's information *routing*. The routing-around hypothesis **[HYPOTHESIS]** — residual perturbations fail because downstream attention re-routes around them — predicts exactly the observed pattern: delivery verified (the (h) controls pass; margins move), decisions unmoved. B4 is the first test of the hypothesis's constructive half: if routing is the lever the nulls are hiding behind, then pulling the lever directly should move decisions. Same site as EXP131's kill (L20), different operator — the cleanest possible operator-class comparison: if B4 moves decisions where EXP131 didn't, it is the operator, not the site; if B4 also fails, the routing-around account is dead as a steering path.

### 1.2 Scope fence: this is NOT a label-free test (Law #7, Law #11)

**[FACT]** The T1/T2 arms use the bench's entity-span annotations to choose the routing target. **[INTERPRETATION]** B4 is an **operator-efficacy** probe, not an autonomous-steering test: it asks whether attention is a steerable substrate, not whether the model can discover the routing target without labels. A CONTINUE licenses "attention reweighting moves frozen decisions" and motivates label-free routing-*discovery* work; it does **not** license any autonomous-steering claim. The span annotations are prompt-structure metadata (the S6-licensed operating condition: 1 ≤ E_i < N_i, E_i/N_i ≤ 0.5), not answer labels; no ground-truth label touches the intervention or the endpoint. If the Law #14 review rules the span use label-adjacent, the draft — not the verdict — is what gets revised.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Does direct attention reweighting at L20 move frozen decisions on EXP092-B — specifically, does boosting attention to the annotated entity span (T1) or ablating it (T2) change the argmax answer, measured against base and against an undirected uniform-reweight control (C)?

**Decision changed:**
- **CONTINUE** (§4): T1 moves decisions (one-sided b>c p ≤ 0.05) **or** T2 moves decisions (one-sided c>b p ≤ 0.05) vs base, AND C does not (two-sided p > 0.05) → "attention is a steerable substrate" survives; routing-aware G/E/S designs licensed; the program's first operator-class positive.
- **KILL** (§4): ΔM = 0 on both T1 and T2 vs base with (h) PASS → "attention-routing intervention steers decisions" is dead; the routing-around hypothesis cannot rescue the nulls.
- **HELD** (§4): T1/T2 move decisions but p > 0.05 (underpowered/inconclusive), OR C also moves decisions (the effect is not routing-specific — unattributable). Licenses nothing, kills nothing.
- **RUN-INVALID** (§4): apparatus failure — Δθ=0 fails, bench/span pins fail, the (h) hook-delivery control fails, renormalization fails, or the budget audit fails. Never a verdict on the hypothesis.

---

## 3. Method

### 3.1 Backbone, bench, environment [FACT / pinned]

- **Backbone:** frozen Pythia-410m, `device_map="cpu"`, float32, `model.eval()`, `torch.no_grad()` around ALL forwards. CPU-only by design ($0).
- **Attention backend:** `attn_implementation="eager"` on ALL arms including base. **[FACT]** SDPA emits no attention weights and cannot be hooked (the EXP100/101 preflight, S6-3c §2). The eager backend is a compute-backend choice, not a model change: the B-decision agreement gate (§3.6(b)) proves it does not perturb decisions.
- **Δθ=0 procedure (pinned):** SHA-256 over tensor bytes with sorted `state_dict` keys, float32 (the EXP077/EXP084/EXP108 canonical convention). Hash asserted **before the first forward and after the last**; any mismatch → RUN-INVALID, exit 44. Expected pin: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331).
- **Bench:** the 60-item EXP092-B bench (30 A-first / 30 C-first strata — the S6/EXP094/EXP102 licensed bench). Expected bench pin: `9be8162633fe19aa…` (S6-3c §2); `len(bench) == 60` asserted; mismatch → RUN-INVALID, exit 44.
- **Span annotations (licensed):** each item carries one entity-span annotation with 1 ≤ E_i < N_i tokens, E_i/N_i ≤ 0.5, span excludes the final token (the S6-3c foundation gate iii operating condition, F2 re-proved). Any item violating the condition is **excluded** and logged (Law #8); **guard:** >6 exclusions → bench mismatch → RUN-INVALID, exit 44. n = 60 − e parameterizes the endpoint.
- **Environment (Law #13):** torch==2.14.0+cpu, transformers==5.17.0 (the registered EXP131-attempt-2 CPU environment); numpy version recorded in the worksheet; `torch.manual_seed(136013)` (model determinism only — the intervention itself is deterministic given weights; no protocol randomness beyond the seed).
- **Law #7:** bench ground-truth labels are used **nowhere** — not in the intervention (span annotations are prompt-structure metadata per §1.2), not in the endpoint (ŷ = argmax over the full vocabulary at the answer position), not in any selection.

### 3.2 The four arms (pinned)

Per included item i, at the final prompt (answer) position q_i:

- **B — base:** eager-attention forward, no hook. The reference for all contrasts.
- **T1 — span-boost (routing toward):** post-softmax L20 attention weights w^{(h)} at q_i (all heads h) are reweighted: w̃_t = 3·w_t for t ∈ span_i, w̃_t = w_t otherwise; renormalized w' = w̃/Σw̃. **[ASSUMPTION]** β = 3.0 is a single pre-registered boost factor (the S6 "single ratio, no grid" precedent) — the hypothesis is "does routing move decisions at all," not the dose-response.
- **T2 — span-ablate (routing away):** w̃_t = 0 for t ∈ span_i, w̃_t = w_t otherwise; renormalized. **[NOTE]** This is the executable form of the sprint's "ablate foil-token attention" under the one-span correction (§0.2): it removes routing to the task-relevant entity.
- **C — uniform-reweight (undirected control):** w'_t = 1/T_i for all positions t (T_i = prompt length). Tests "any attention perturbation" vs "directed routing."

The modified weights feed the value aggregation: out^{(h)} = Σ_t w'_t·v^{(h)}_t. The executor implements the reweighting via a forward hook on the L20 attention submodule intercepting post-softmax weights under the eager backend; the (h) control (§3.6(d)) verifies the interception reaches the computation.

### 3.3 Endpoint and statistics (Law #9)

**Primary endpoint:** per-arm decision-flip rate vs base, ΔM_arm = (1/n)Σ_i **1**[ŷ_i^{arm} ≠ ŷ_i^{B}], and the paired McNemar exact test per arm vs base with direction-appropriate alternatives (b = arm-correct & B-wrong, c = arm-wrong & B-correct) — **F1 fix:** the draft's uniform one-sided H1: b>c could not fire on T2's own predicted direction:
- **T1** (span-boost, predicted to improve-or-move): one-sided H1: b > c.
- **T2** (span-ablate, predicted to worsen): one-sided H1: c > b.
- **C** (uniform control, no directional prediction — attribution guard): two-sided.
**[NOTE]** The directional alternatives test the pre-registered predictions; a systematic effect in the unpredicted direction does not license CONTINUE (Law #4 — no post-hoc direction shifts). Correlated consequence: systematic T1 *worsening* (c >> b) resolves to HELD (sub-significant), not CONTINUE — the directional bars bind as written.

**Decision bars (§4, binding):**

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | (T1 vs B: one-sided b>c p ≤ 0.05 **or** T2 vs B: one-sided c>b p ≤ 0.05) **and** (C vs B: two-sided p > 0.05) | Routing-specific steering signal in the predicted direction; attention is a steerable substrate |
| KILL | ΔM_T1 = 0 **and** ΔM_T2 = 0 vs B, with (h) PASS on both hooks | Attention-routing intervention steers no decisions |
| HELD | (T1 or T2 significant in its directional test) **and** (C: two-sided p ≤ 0.05) — unattributable; **or** (T1/T2 ΔM > 0 but directional p > 0.05) — sub-significant | Inconclusive; licenses nothing, kills nothing |
| RUN-INVALID | any §3.6 guard fires | Apparatus failure; never a verdict on the hypothesis |

**Statistical license:** with n = 60 and base accuracy 36/60 (the archived EXP094 B vector): T1 at 44/60 with b = 10, c = 2 gives exact one-sided (b>c) p = 79/4096 ≈ 0.019 — the CONTINUE bar is reachable at realistic effect sizes. T2's predicted worsening is equally reachable: b = 2, c = 10 gives exact one-sided (c>b) p = 79/4096 ≈ 0.019 (by symmetry). Under the KILL world (true flip rate 10%), P(ΔM_T1 = ΔM_T2 = 0) = 0.9^{120} ≈ 3.2×10^{-6} — the KILL bar is stringent, not vacuous. The C-conjunct on CONTINUE prevents a generic "we touched attention" effect from licensing routing-specific claims (Law #9: the attribution control binds independently).

### 3.4 The (h) hook-delivery positive control (mandatory)

After hook registration and **before any decision forward**, on the first included bench item, in two probe forwards (N_h = 2):

**Phase 1 — T2 (span-ablate) hook:**
1. Register the T2 hook; run one forward with attention-weight and submodule-output capture at L20.
2. Read w^{(h)} at q_i for all heads. **Assert:** max_h Σ_{t ∈ span_i} w^{(h)}_t < 1e-6 (the span is ablated in every head).
3. **Assert:** |Σ_t w^{(h)}_t − 1| < 1e-5 for all h (renormalization held).
4. **Assert:** no NaN/Inf in any w^{(h)}.
5. **Assert:** (1/H)Σ_h ‖w^{(h)} − w^{(h)}_base‖_1 > 0.01 (the hook is active — not a no-op; w_base from the already-recorded B pass, no extra forward).
6. **Assert (A1):** ‖o − o_base‖_2 > 1e-6, where o is the L20 attention-submodule output on the probe forward and o_base the submodule output on the B pass — the reweighted weights propagate to the module output. **[INTERPRETATION]** This closes the detached-copy false-KILL path: a hook modifying a detached weight copy would pass asserts 2–5 yet leave o = o_base exactly (deterministic computation); assert 6 trips it.

**Phase 2 — T1 (span-boost) hook (F2 fix):** the draft's (h) verified only the T2 hook, leaving T1's 3× boost unproven — if base span attention mass is ~0, T1 computes 3×0 = 0 (a no-op) and a KILL resting on ΔM_T1 = 0 would be invalid. Phase 2 closes the gap:
7. Register the T1 hook; run one forward with attention-weight and submodule-output capture at L20.
8. **Assert:** (1/H)Σ_h ‖w^{(h)} − w^{(h)}_base‖_1 > 0.01 (the 3× boost is applied — not a no-op).
9. **Assert:** mean_h Σ_{t ∈ span_i} w^{(h)}_t > mean_h Σ_{t ∈ span_i} w^{(h)}_base_t (the change is a boost, not an arbitrary perturbation — post-renormalization span mass strictly increases for any base span mass in (0,1)).
10. **Assert:** mean_h Σ_{t ∈ span_i} w^{(h)}_t > 1e-3 (the boosted span commands non-trivial mass — if base span mass is ~0, the boost is a no-op and this assert fails).
11. **Assert:** |Σ_t w^{(h)}_t − 1| < 1e-5 for all h (renormalization held).
12. **Assert:** no NaN/Inf in any w^{(h)}.
13. **Assert (A1):** ‖o − o_base‖_2 > 1e-6 (output propagation, as in Phase 1).

Any assert fails → the hook does not reach the attention computation → apparatus-void → **RUN-INVALID, exit 44**, zero decision forwards. N_h = 2 probe forwards, counted in the (f) budget. **[INTERPRETATION]** This control is strictly stronger than the residual-stream (h): the intervention itself is directly observed, not inferred through a downstream tap. **[NOTE on the ~0-mass case]** If base span attention mass is ~0 on the probe item, Phase 2 asserts 8/10 fail → RUN-INVALID, not KILL — the apparatus cannot test T1, so no verdict on the hypothesis is licensed. This is the honest outcome; a KILL requires both hooks proven delivered.

### 3.5 What is NOT measured here

- No dose-response (single β = 3.0; T2 is binary). A CONTINUE motivates a dose study; it does not establish one.
- No other layers (L20 only — the EXP131 comparison site). A KILL fences L20 attention-routing, not "all attention intervention."
- No head subsets (all heads). Head-specific routing is a follow-up design.
- No label-free discovery (the §1.2 fence): the routing target is annotated.

### 3.6 Guards and breaking points (trip conditions + exit codes)

- **(a) Δθ=0:** SHA-256 pre/post mismatch → RUN-INVALID, **exit 44**.
- **(b) B-decision agreement (the eager-backend non-perturbation proof, S6-3c pattern):** per-item B decisions must match the archived EXP094 B vector 60/60 (36/60 accuracy) → any disagreement → RUN-INVALID, **exit 44**. (If eager attention perturbs decisions, the base is invalid and no contrast is licensed.)
- **(c) Bench + span pins:** bench SHA-256 mismatch, len ≠ 60, or >6 span-condition exclusions → RUN-INVALID, **exit 44**.
- **(d) Hook-delivery (h):** any §3.4 assert fails → RUN-INVALID, **exit 44**.
- **(e) Renormalization/NaN on decision forwards:** the executor asserts Σw' = 1 (±1e-5) and finiteness on every hooked forward; violation → RUN-INVALID, **exit 44**.
- **(f) Budget audit:** forward ledger must equal 4·n (B, T1, T2, C) + N_h (probe) ± 0 accounted passes (242 at n = 60, N_h = 2 — one T2 probe + one T1 probe); any unaccounted forward → RUN-INVALID, **exit 44**.
- **(g) Clean completion:** all guards pass → executor computes the endpoint, prints the verdict per §4, **exit 0**.

---

## 4. Decision table (binding)

§3.3. Precedence on exact-boundary data: RUN-INVALID > HELD > KILL > CONTINUE (a tripped guard voids everything; an unattributable significant effect is HELD, never CONTINUE; ΔM = 0 on both routing arms is KILL only with (h) PASS on both hooks).

**Explicit resolution (A2):** the configuration "C vs B significant (two-sided p ≤ 0.05) with ΔM_T1 = ΔM_T2 = 0" resolves to **KILL** — neither HELD branch fires (the unattributable-HELD requires T1/T2 significant in their directional tests; the sub-significant-HELD requires ΔM > 0), and KILL's ΔM = 0 condition holds with (h) PASS. **[INTERPRETATION]** If the undirected control moves decisions but the directed arms do not, routing is not the lever.

---

## 5. Worth-it gate (Law #15, 7 points)

1. **Exact question:** Does direct attention reweighting at L20 move frozen Pythia-410m decisions on EXP092-B, where residual-content injection at the same layer moves nothing?
2. **Decision changed:** CONTINUE → the routing-intervention axis lives (first operator-class positive; routing-aware G/E/S designs licensed). KILL → attention routing is dead as a steering path (the nulls are not routable-around). HELD → inconclusive. RUN-INVALID → apparatus failure.
3. **Cheapest test:** 60 items × 4 arms (B, T1 span-boost ×3, T2 span-ablate, C uniform) via eager-attention post-softmax hooks at L20; ΔM + paired McNemar vs base; the (h) hook-delivery control adapted for attention weights.
4. **Cost:** $0 CPU, ~4–6h (drafting correction §0.1: the sprint's ~0.75h at n = 10 cannot power its own bars; 240 decision forwards at the sprint's ~1–1.5 min/forward rate).
5. **Mathematical license:** attention as the transformer's routing mechanism **[DEFINITION]** — the post-softmax weights are the convex combination coefficients selecting which positions' values reach the residual stream; reweighting them IS re-routing by definition. The routing-around hypothesis **[HYPOTHESIS]** predicts the verified-delivery null pattern (delivery confirmed, decisions unmoved) as its signature.
6. **Quantitative prediction:** T1 flips ≥ 8/60 decisions with McNemar one-sided (b>c) p ≤ 0.05 vs B (e.g., b = 10, c = 2 → p ≈ 0.019), **or** T2 flips ≥ 8/60 with one-sided (c>b) p ≤ 0.05 (e.g., b = 2, c = 10 → p ≈ 0.019), while C stays flat (two-sided p > 0.05) — a routing-specific signal in the predicted direction.
7. **Breaking point:** ΔM_T1 = ΔM_T2 = 0 with (h) PASS → **KILL** "attention-routing intervention steers decisions" (P ≈ 3.2×10^{-6} under a 10% true flip rate — the bar bites).

## 6. Non-resurrection audit (Law #4)

- **No execution has ever intervened on attention weights.** Full-log grep (LOG-4848 re-diff): the attention hits are (i) S6-3b/3c/EXP102's **read-only** attention hooks — measurement instruments for gating, never intervened upon (the log says "read-only" verbatim, repeatedly); (ii) a Layer-8 "re-routing" mechanistic hypothesis **[INTERPRETATION]**, never executed; (iii) R5/EAR "ephemeral attention registers" (ablation-verified scratch memory — a different question, killed); (iv) the sprint dossier's own §7.5(e) listing inference-time attention temperature scaling as **unexplored** — the closest cousin, never executed. B4 is the first execution on the attention-intervention axis.
- **S6's breaking point (iv)** fenced "no fifth externally-computed attention-gate variant" — that fences attention-as-a-*gate* (a measurement used to condition residual injection), not attention-as-the-*intervention-target*. Different operator; the fence does not cover B4.
- **G1** killed a QK-subspace *theorem* (a claim about where failed directions live in weight space) — a statement about the geometry of past failures, not an intervention on attention. Different question class.
- **EXP131/133** killed residual injection at L20 — B4 intervenes at the **same site, different operator**. This is the licensed comparison the program has never run: site held constant, operator varied.
- **EXP105** masked logits (readout-side), not attention weights. Different substrate.
- The draft's two deviations from the sprint bet (n = 60, one-span T2) are documented in §0 as drafting corrections with mathematical justification, not post-hoc shifts — the bars were never licensed (this is the draft).

## 7. Launch chain and licensing

This draft licenses nothing. The Law #14 review of this exact file may demand fixes; fixes get an independent fix-verification; only then does the CEO decide on launch and mint EXP136. The executor will follow §3 exactly; any deviation trips a §3.6 guard.

---

*Draft: B4/ARI pre-registration lane, LOG-4848. $0 CPU, paper only. EXP136 provisional — not minted.*
