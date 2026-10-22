# Pre-registration DRAFT: Geodesic Multistep Steering along the TGA v₁ Direction (CPU Pilot, Matched Norm Budget)

**Lane:** LOG-4790 (pre-assigned). **Status: DRAFT — licenses nothing.** This file is a design document only. No experiment number is minted; no Law #14 review has been performed; no SIGN is claimed or implied; no execution is licensed (CPU or GPU). Any GPU-resident stage is fenced as founder-gated in §9 — NOT licensed by this lane, not by this file.

**$0 CPU scope:** when (if ever) executed, this pilot is CPU-only on frozen Pythia-410m (Δθ=0, LOG-331 pin). No GPU contact, no spend, no credentials.

**Chain:** EXP131 (one-shot TGA v₁ injection) → binding KILL (LOG-4766, independent Law #14 SIGN): ĉ = 0.03741576759203537 < 0.1, ΔM_v1 = 0, zero flips on all 11 arms, McNemar p = 1.0, budget B = 0.50578119, norm audit 110/110 PASS. Licensed escalation instrument class (LOG-4751 sweep): GEOSTEER (Ngo/Vo/Le, arXiv:2609.10658) — Riemannian/geodesic multistep steering. Worth-it gate: `research/strategy/GEOSTEER_MULTISTEP_WORTHIT_2026-09-30.md` (LOG-4790).

---

## 0. The breaking point (read first)

Conjunctive. Any miss → **apparatus-void or RUN-INVALID as stated, hypothesis UNTESTED** (Law #9 ordering: guards → backbone pin → artifact re-pins → budget computation and record → endpoint-ĉ gate → forward batches (injection paths) → validity-check evaluation → raw-record hash-pin → metric → decision):

(a) **Δθ=0** — backbone LOG-331 parameter hash `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (sorted `state_dict` keys, float32, tensor bytes — the EXP077/EXP084/EXP108/EXP131 canonical convention) pinned before the first CPU forward and re-pinned after the last; any mismatch → apparatus-void.
(b) **Direction re-pins** — `exp127_vectors.npz` SHA-256 matches the EXP131-pinned value AND all 10 per-prompt ids align as `v1__<prompt_id>` / `v2__<prompt_id>` / `bagg__<prompt_id>`; miss → apparatus-void (the steered direction is not the EXP127 direction). No re-derivation of v̂₂ (EXP131's deflated power iteration is NOT re-run — re-pin only).
(c) **No finite differences** — the executor asserts no finite-difference term (‖Δ‖/‖δ‖ or any δ-perturbation sensing) exists anywhere in the path pipeline; the geodesic steps are exact-vector addition + exact sphere retraction at x_{20,last}. Any finite-difference sensing input → apparatus-void (EXP128 constraint, §8).
(d) **Norm-budget matching (the dose fence, mechanical)** — every arm spends exactly the EXP131 budget B = 0.50578119 (copied verbatim from LOG-4766; NOT recomputed as a new number — Law #2; the executor independently recomputes B = 0.01 × median ‖y_{20,last}‖ per the EXP129 FIX-2 rule and asserts equality with 0.50578119 within 1e-6 relative, recorded before the first injection forward; mismatch → apparatus-void, bench/backbone drift). Per-step: tangent injection ‖t_k‖ = B/5 ± 1e-6 relative on every geodesic step (exact by construction — §3.4); one-shot arm ‖δ‖ = B ± 1e-6 relative; total tangent injection ∑‖t_k‖ = B ± 1e-6 relative on every arm. The retracted displacement δ_k := x_{k+1} − x_k is recorded per step with ‖x_0‖ pinned per prompt, and the retracted total satisfies the one-sided retraction bound B·(1 − α²/(2‖x_0‖²)) − 1e-6·B ≤ ∑‖δ_k‖ ≤ B + 1e-6·B (retraction shortens, never escalates — §3.4, F1 repair). Any miss → apparatus-void (the verdict would measure the budget, not the path — EXP129 FIX-4 discipline; the norm audit is EXP131's 110/110 PASS discipline extended to paths).
(e) **B_agg-path null-control holds** — the dead-control geodesic path along B̂_agg must replicate ΔM = 0; if it moves any decision → **RUN-INVALID (apparatus drift)** — the bench or backbone is not what EXP077/EXP131 measured, and no verdict may be read.
(f) **No training, no weight mutation** — pure forwards through a frozen model in eval mode; the executor contains no optimizer, no loss, no backward pass into weights. The ĉ computation uses exact autograd VJPs (EXP127's Law-#14-licensed apparatus) — a backward *through the frozen graph*, never into weights.
(g) **Decision-readout only** — the readout is the registered H1/H6 §3.3 cosine decision statistic, verbatim. No logit channel, no generation, no decode probe, no trained head, no learned objective fitted on task labels. Any generation-channel touch → **RUN-INVALID** (EXP130's Law #14 REJECT, LOG-4721; the line-7637 cull of the label-assisted capability claim stands). [GUARD] (A1: design constraint, not an assumption)

[DEFINITION] ĉ_geo (decision-orthogonality, path form): for prompt i, let x_K,i be the geodesic endpoint (K = 5 steps along Π(v̂₁,i)) and M_i the margin statistic. Let g_i = ∇_{x_K,i} margin_i be the exact-autograd VJP of the registered cosine margin at the endpoint. ĉ_geo,i = |⟨Π_K(v̂₁,i), ĝ_i⟩| with ĝ_i = g_i/‖g_i‖. The gate statistic is the mean over the 10 prompts. If ‖g_i‖ < 1e-12 on a prompt, that prompt is excluded with the exclusion recorded; ≥ 3 exclusions → apparatus-void. **ΔM_geo = 0 AND ĉ_geo < 0.1 → KILL at the decision-orthogonality gate** (F3: conditional on the endpoint null, per the EXP131 precedent where the (flips + low ĉ) corner never arose; if ΔM_geo > 0 the §2 table governs and ĉ_geo is diagnostic only — EXP127 §8).

## 1. Hypothesis (one falsifiable sentence)

[HYPOTHESIS] A norm-preserving geodesic multistep path (K = 5, total budget B = 0.50578119, sphere retraction + parallel transport) along the TGA leading singular direction v̂₁ moves decisions on frozen Pythia-410m where the one-shot Euclidean injection δ = B·v̂₁ moved none.

## 2. Exact question and the decision it changes

**Question:** At fixed total injected norm B, does the *path class* (geodesic multistep vs Euclidean one-shot) change the decision outcome along v̂₁?

| Measured condition | Verdict |
|---|---|
| ΔM_geo = 0 (zero decision flips on the geodesic v̂₁ endpoint arm; McNemar n.s. automatic) **AND** the PIVOT trigger below does not fire | **KILL** — the dynamical intervention story closes at the instrument level. TGA remains a dynamics-characterization quantity only (EXP127's CONTINUE stands as measurement); no targeting claim over TGA dynamics is ever licensed — not one-shot (LOG-4766), not multistep-geodesic (this verdict), not any budget escalation (fenced by EXP095, LOG-4400). The GEOSTEER escalation branch retires; GeoSteer returns to cull status. If additionally mean ĉ_geo < 0.1, the kill is characterized as decision-orthogonal (the §4 gate); if ĉ_geo ≥ 0.1 with ΔM_geo = 0, the kill stands on the decision question without the orthogonality characterization (F3 harmonization). |
| ΔM_geo > 0 with McNemar(geodesic v̂₁ vs base) one-sided p ≤ 0.05 **AND** rank-trend holds (margin-displacement(v̂₁ geodesic) ≥ margin-displacement(v̂₂ geodesic) on ≥ 8/10 prompts — the §3.7 definition, used identically here; F4) **AND** best-random-path null holds (geodesic v̂₁ out-moves the best random path) **AND** B_agg-path ΔM = 0 | **CONTINUE** — the first bound positive steering signal in program history: multistep-geodesic is a licensed instrument class on Pythia-410m L20, the 10 pinned prompts, matched budget. A GPU follow-up pre-reg may then be *drafted* (founder-gated; not licensed here). |
| ΔM_geo = 0 **BUT** ≥ 2 prompts show midpoint ĉ (k ∈ {2,3}) ≥ 0.1 on the v̂₁ geodesic | **PIVOT** — path-midpoint targeting: curvature exists mid-path but washes out at the endpoint; a new matched-budget design is drafted (never a dose increase). N1: ≥ 2 prompts (not 1) for multiplicity control across the 20 midpoint ĉ values; the trigger licenses only a draft. |
| B_agg-path arm moves any decision | **RUN-INVALID** — apparatus drift (breaking point (e)); hypothesis UNTESTED. |
| Any breaking-point miss | **apparatus-void / RUN-INVALID as stated** — hypothesis UNTESTED. |
| Geodesic v̂₁ moves decisions **only** where a matched random path also does | **KILL** — the effect is path-noise, not the amplifier's. |
| ΔM_geo > 0, McNemar(geodesic v̂₁ vs base, one-sided) n.s., random-null holding (the flips are not matched by either random path) | **INCONCLUSIVE** — hypothesis UNTESTED (insufficient power at N = 10 pinned prompts). No verdict is read; the pilot is neither KILL nor CONTINUE, and this row licenses no follow-up. (F2 repair) |
| ΔM_geo > 0, McNemar(geodesic v̂₁ vs base, one-sided) p ≤ 0.05, random-null holding, rank-trend flat or inverted | **KILL** — the effect is not the amplifier's (§3.7 rank-trend gate). (F2 repair) |
| Any measured outcome matching no row above (no CONTINUE/PIVOT/RUN-INVALID/apparatus-void conjunct fires) | **INCONCLUSIVE** — hypothesis UNTESTED; licenses nothing. (a) No CONTINUE/PIVOT claim may be read from an unmatched corner (Law #4). (b) The corner must be added to this table explicitly before any retest. (c) Repeated INCONCLUSIVE on the same corner across pilots escalates to KILL. (B2 repair; CEO decision LOG-4795: KILL overclaims on ambiguous data — INCONCLUSIVE denies the Law-#4 escape hatch without post-hoc closure.) |

The KILL branches are evaluated first (EXP129 FIX-1 precedence discipline); the CONTINUE bars apply only if no KILL branch fires. Precedence within nulls: the midpoint-PIVOT check fires before the endpoint-null KILL — an "endpoints null BUT ≥ 2 prompts with midpoint ĉ ≥ 0.1" outcome routes to PIVOT, not KILL (see §4 evaluation order; A3). The kill is the named-first and the valuable product.

## 3. Method

### 3.1 Prompts (pinned)

The same 10 pinned prompts as EXP131 (reused bench artifact — no new prompts, no new labels, no label touch). Bench re-verified at startup (prompt ids, tokenization, single-token entity encoding per the H1/H6 §3.3 recipe); bench mismatch → apparatus-void.

### 3.2 Frozen backbone (CPU)

Pythia-410m weights loaded read-only on CPU; LOG-331 hash pinned pre AND post (breaking point (a)). torch deterministic-algorithms flag set; pinned seed stream = EXP131's recorded seed (CPU generation, recorded); environment manifest recorded (torch/transformers/numpy versions; EXP131's GPU run pinned transformers 5.17.0, torch 2.10.0+cu128, numpy 2.0.2 — the pilot records its CPU equivalents).

### 3.3 Direction re-pins (breaking point (b))

v̂₁,i, v̂₂,i, B̂_agg re-pinned from `exp127_vectors.npz` (EXP131's re-pin discipline). No re-derivation.

### 3.4 Geodesic path definition (deterministic, exact)

For direction unit vector u (per-prompt), step count K = 5, α = B/5, x_0 = x_{20,last} (EXP131's injection site — apples-to-apples):
- Tangent injection: t_k = α · Π_k(u), where Π_k is parallel transport of u to the tangent space at x_k on the sphere ‖x‖ = ‖x_0‖ (rotation in the plane span{x_k, Π_k(u)}; exact, deterministic, closed form). N4: the stepwise retraction procedure below governs — the executor must NOT substitute a single exact great-circle arc for the K specified steps. [FACT] ‖t_k‖ = α exactly by construction (the executor asserts per breaking point (d)).
- Retraction: x_{k+1} = (x_k + t_k) · (‖x_0‖/‖x_k + t_k‖) — norm-preserving by construction, so ‖x_k‖ = ‖x_0‖ for all k; t_k ⊥ x_k gives ‖x_k + t_k‖ = √(‖x_0‖² + α²) exactly.
- Retracted displacement (F1 repair): δ_k := x_{k+1} − x_k is the actual state move the model experiences. [FACT] The retraction shortens it: with c = ‖x_0‖/√(‖x_0‖² + α²) = 1/√(1 + α²/‖x_0‖²), ‖δ_k‖² = c²α² + (c−1)²‖x_0‖², i.e. ‖δ_k‖ = α·(1 − ε_k) with 0 < ε_k ≤ α²/(2‖x_0‖²) per step (leading order 3α²/8‖x_0‖²). The shortfall is pure retraction geometry — it can only shorten, never inject more than the tangent step. Dose accounting: the §0(d) audit binds the tangent injections (‖t_k‖, ∑‖t_k‖ — exact, hence satisfiable); the retracted total ∑‖δ_k‖ is recorded per prompt (‖x_0‖ pinned per prompt) against the one-sided bound in §0(d).
- N3 contingency: the one-shot arm is re-measured on CPU. If it does not replicate EXP131's GPU null, the McNemar(geodesic, one-shot) reference stays within-run (CPU-to-CPU — the GPU record is never imported); the divergence is logged as a bench-drift note and the B_agg-path null-control becomes the binding validity check.
- Endpoint x_K; optional midpoint states x_2, x_3 (PIVOT diagnostic only — registered, not decision-gated).
- One-shot arm: x_1 = x_0 + B·v̂₁ (CPU re-measure of the EXP131 baseline — the McNemar reference is CPU-to-CPU, never GPU-imported).

### 3.5 Arms (per prompt)

- **Base:** no injection — reference decisions.
- **One-shot v̂₁:** δ = B·v̂₁ (EXP131 baseline, re-measured on CPU).
- **Geodesic v̂₁ endpoint:** K = 5 steps along Π(v̂₁).
- **Geodesic v̂₂ endpoint:** K = 5 steps along Π(v̂₂) (rank-trend gate).
- **Random-path geodesics (2):** K = 5 steps along Π(u_j), u_j drawn as matched-norm random unit vectors from the pinned seed stream (matched-norm path null; best-random-path pinned before outputs are inspected).
- **B_agg-path:** K = 5 steps along Π(B̂_agg) (the dead control — ΔM = 0 expected; breaking point (e)).
- Total: 7 arms × 10 prompts = **70 forwards** + 20 endpoint ĉ VJPs (geodesic v̂₁ + one-shot v̂₁, 10 prompts each) + ≤ 20 optional midpoint forwards (v̂₁ path, k = 2,3 — PIVOT diagnostic only). CPU, $0.

### 3.6 Readout — the registered decision statistic

The H1/H6 §3.3 recipe, verbatim: candidate entities E1 = `tuple[0]`, E2 = `tuple[-1]`; option texts `" " + E`; executor asserts `encode(" "+E)` is exactly one token on the real Pythia tokenizer for every item (failure → RUN-INVALID, items NOT silently dropped); option embeddings = frozen layer-20 final-token hidden state of the single-token option text; `score(E) = cosine(state_emb, option_emb)`; decision = argmax(score(E1), score(E2)); ties → E2; **margin** = `|cos(E1) − cos(E2)|`. The path is injected at x_{20,last} during the item's forward; everything else is identical to EXP131. **No logit channel, no generation, no decode probe, no trained head** (breaking point (g)).

Per (item, arm): decision, margin. **ΔM** = decision flip vs the base arm. Margin displacement = |margin_arm − margin_base|.

### 3.7 Decision bars with statistical license

- **Primary:** McNemar(geodesic v̂₁ arm vs base arm), one-sided, **p ≤ 0.05** with ΔM_geo > 0 — a registered positive bar, fixed before any output is inspected (Law #9).
- **Reference:** McNemar(geodesic v̂₁ vs one-shot v̂₁), one-sided — separates the pilot from the EXP131 baseline on the same CPU forwards.
- **Decision-orthogonality gate:** mean ĉ_geo over 10 prompts; **ΔM_geo = 0 AND ĉ_geo < 0.1 → KILL** (conditional gate per F3, §0 definition; EXP127 §8).
- **Rank-trend gate:** margin-displacement(v̂₁ geodesic) ≥ margin-displacement(v̂₂ geodesic) on ≥ 8/10 prompts (the single quantified definition — used identically in §2, F4); flat or inverted → **KILL** (the effect is not the amplifier's).
- **Random-null gate:** best-random-path pinned before inspection; if geodesic v̂₁'s effect does not exceed it → **KILL** (path-noise).
- Per-step ĉ profile: diagnostic only (not registered, not decision-gated) — feeds the PIVOT branch via midpoint ĉ.

### 3.8 Raw-record hash-pin specification

Per (item, arm, step): tangent-injection norm ‖t_k‖, retracted-displacement norm ‖δ_k‖, ‖x_0‖ (pinned per prompt — feeds the §0(d) retraction bound), state checksum post-retraction, decision, margin — written to the records JSON; SHA-256 hash-pin recorded before the verdict lane reads them; any verdict computed from unpinned records → the verdict is void (EXP131's defect-class-(b) discipline).

### 3.9 Guards and what is NOT measured here

- No generation-channel measurement exists in this pilot (EXP130 REJECT is terminal on the program).
- No learned objective, no label-fitted anything (line-7637 cull is respected).
- No dose axis (EXP095 kills it; budget is a constant, B).
- No GPU stage (fenced, §9).

## 4. Falsification decision tree

Evaluated in Law-#9 order after hash-pin: breaking-point conjuncts → B_agg-path null-control → midpoint-PIVOT check (ΔM_geo = 0 AND ≥ 2 prompts with midpoint ĉ ≥ 0.1 → PIVOT) → decision-orthogonality gate (ΔM_geo = 0 AND ĉ_geo < 0.1 → KILL; ΔM_geo = 0 with ĉ_geo ≥ 0.1 → KILL on the decision question, §2) → primary McNemar bar → rank-trend (flat/inverted → KILL) → random-null (geodesic effect ⊆ random-path effect → KILL) → INCONCLUSIVE check (ΔM_geo > 0, McNemar n.s., random-null holding → INCONCLUSIVE). First firing verdict wins; KILL branches precede CONTINUE bars (EXP129 FIX-1). F3: the PIVOT check precedes the endpoint-null KILL so the table's 'endpoints null BUT…' exception is live.

## 5. Law #9 ordering

guards → backbone pin → artifact re-pins (v̂₁/v̂₂/B̂_agg) → budget computation and record (B = 0.50578119, α = B/5) → endpoint-ĉ gate → forward batches (injection paths, any batch order) → validity-check evaluation (per-step norm audit + B_agg-path null-control + re-pin) → raw-record hash-pin → metric (ĉ_geo, ΔM, McNemar, rank trend, midpoint ĉ) → decision.

## 6. Cost and honesty

- ~70 forwards + ~20 ĉ VJPs + ≤ 20 optional midpoint forwards, CPU-only, $0; Pythia-410m ≈ 1.6 GB weights — fits the lab VM. (F5: the worth-it gate's '5 arms / 50 forwards' cost figure is superseded — the registered design is 7 arms × 10 prompts = 70 forwards. The two added arms, geodesic v̂₂ (rank-trend gate) and B_agg-path (null-control), are required by the §2 decision table and cannot be cut. The gate strategy file was reconciled in repair round 2, LOG-4795: 7-arm/70-forward/20-VJP/≤20-midpoint counts, B1 tangent-injection tolerance language, and the B3 UNVERIFIED relabel.)
- A KILL is the named-first product: the terminal, instrument-level closure of the dynamical-intervention hypothesis class — TGA targeting stands down on every licensed instrument and every fenced budget. That is a publishable boundary fact (v84 future-work line can cite the closure).
- A CONTINUE is tagged exactly as it is: a bound positive steering signal on Pythia-410m L20, the 10 pinned prompts, matched budget — never "steering works," never consciousness, never generality.
- This draft licenses nothing; the pilot may only ever be *built* after Law-#14 review of a signed pre-reg and CEO clearance — none of which this file provides.

## 7. What constrains this protocol (the seventh item, restated for the executor)

1. EXP131's KILL (LOG-4766) binds the one-shot v₁ hypothesis — this pilot is the named LOG-4751 escalation instrument class only.
2. EXP095's dose kill (LOG-4400) fences all budget increases — B is a constant; any lane that raises it is barred.
3. EXP130's Law #14 REJECT (LOG-4721) fences all generation-channel designs — decision-readout only.
4. The line-7637 cull fences all label-assisted capability claims — no labels, no trained head, no learned objective.

## 8. What this protocol does NOT claim

- No targeting claim on TGA beyond this pilot's bars; a CONTINUE licenses an instrument class on this bench, not a mechanism.
- A KILL closes the question *at matched budget on this bench* — it does not prove "no multistep steering anywhere on any model" (that would be an unlicensed universal; the claim is the bounded closure, stated as such).
- Nothing about consciousness, generality, or capability. No v82/v83/v84 claim is altered by this draft (signed paper sources are read-only to this lane).

## 9. GPU-resident stage — FENCED, NOT LICENSED

Any GPU stage (e.g., a K-sweep, a larger bench, a per-step ĉ profile on GPU) is **founder-gated**: it requires a fresh Law-#15 worth-it gate on the measured CPU result, a Law-#14 pre-reg review with SIGN, a minted experiment number, and CEO/founder clearance. **This lane provides none of those.** This draft does not license, schedule, or authorize any GPU contact.

---

## Scope erratum (appended 2026-09-30, CEO, per LOG-4817 finding F1 — signed text above untouched)

The KILL-row narrative's clause "not one-shot (LOG-4766)" is **suspended** per LOG-4810: EXP131's binding KILL (LOG-4766) was re-categorized as RUN-INVALID (apparatus defect — blind readout tap) after LOG-4808/4809, and the one-shot TGA-v₁ injection hypothesis is UNTESTED. The EXP133 attempt-4 KILL (LOG-4814, independently reviewed LOG-4817) therefore closes the **multistep-geodesic** branch only: geometry-aware multistep steering along the TGA leading direction steers zero decisions at matched budget with verified delivery. It does not imply one-shot closure; one-shot remains an open hypothesis on the EXP131 track.
