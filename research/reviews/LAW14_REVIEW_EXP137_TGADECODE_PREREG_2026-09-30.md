# Law #14 Independent Review — B3/TGA-DECODE Pre-registration Draft

**Artifact under review:** `research/prereg/EXP137_PREREG_TGADECODE_2026-09-30.md` (exact file, DRAFT status)
**Reviewer lane:** LOG-4856 (pre-assigned by the CEO). **Date:** 2026-09-30.
**Reviewer independence:** this lane did not draft the pre-registration (LOG-4855 was a separate lane).
**Verdict: SIGN** — the draft is launch-ready pending the CEO launch decision. Three non-blocking advisories (A1–A3) below; no required fixes.

---

## 1. The layers[19] derivation — independently verified CORRECT

This is the highest-stakes detail in the draft, and it holds. The reviewer re-derived it from the primary sources, not from the draft's account:

1. **v̂₁'s native space (EXP127).** `experiments/runs/EXP127_tga/exp127_execute.py:220-244` — `power_iteration` computes `w = jvp(f, z, v)` then `t = vjp(f, z, w)`, i.e., power iteration on M^T M. The returned vector is the leading **right (input) singular vector** of M = ∂x_{24,last}/∂x_{20,last}. The perturbation is applied at `h20_in = hs[20][0]` (line 278), commented in-code as "input of block 20, all positions." Therefore v̂₁ lives in the `hidden_states[20]` space = input of transformer block 20. The draft's "leading input singular vector" characterization is exact.

2. **EXP092's archive indexing.** `experiments/runs/EXP092_ibl/extract_layer_embeddings.py:263-265` — `layers[l, i, :] = out.hidden_states[l + 1][0, -1, :]` with the in-code comment "hidden_states[0] = embedding output -> indices 1..24 = layers 0..23." In standard HF indexing, `hidden_states[i]` = output of block (i−1) for i ≥ 1. Therefore archived `layers[l]` = output of 0-indexed block l.

3. **The index.** Input of block 20 = output of block 19 = `hidden_states[20]` = archived `layers[19]`. The draft's conclusion — project onto archived `layers[19]`, not `layers[20]` — is correct. Projecting onto `layers[20]` (= output of block 20) would indeed test an unlicensed subspace one block downstream of v̂₁'s native space.

4. **Transformers 5.x caveat checked.** EXP127's executor notes (lines 279-283) that `hs[24]` is the final-layer-norm output, not block 23's output, in transformers 5.x. This quirk affects only `hs[24]`; `hs[20]` = output of block 19 is unaffected in both transformers 4.x and 5.x. The derivation does not depend on the quirk.

**Ruling:** the derivation is correct. No other archived index is licensed.

## 2. Decision table — exact, exhaustive, mechanically applicable

Let a = 1-NN LOO accuracy (n=60, K=20, chance 0.05), p = stratified permutation p-value (B=10,000):

- **CONTINUE:** a ≥ 0.15 AND p < 0.00208
- **KILL:** a ≤ 0.08
- **HELD:** 0.08 < a < 0.15, OR (a ≥ 0.15 AND p ≥ 0.00208)
- **RUN-INVALID:** any §3.5 breaking point trips

Verified disjoint and exhaustive over (a, p) space with no apparatus trip. Note a is always a multiple of 1/60 ≈ 0.0167, so a ≤ 0.08 ⟺ ≤4/60 and a ≥ 0.15 ⟺ ≥9/60 — the draft's parentheticals are exact. No post-hoc re-binning is possible (Law #4).

### The p < 0.00208 bar — challenged and upheld

The draft explicitly flags this choice for review (§4 NOTE, §7). The reviewer's ruling:

- 0.05/24 = 0.0020833…; the draft's 0.00208 matches EXP092 §4's Bonferroni bar (verified in `experiments/protocols/EXP092_IBL_PREREG_SIGNED.md:113`).
- For a single pre-registered test, no multiple-comparison correction is statistically required; 0.05 would be the conventional bar. The draft's adoption of the stricter bar is therefore a **deliberate conservatism**, not a statistical necessity — and the draft says so openly.
- **It cannot manufacture a KILL:** the KILL bar (a ≤ 0.08) involves no p-value. The stricter bar only moves mass between CONTINUE and HELD, never into KILL.
- **CONTINUE remains reachable:** for a genuine signal at a ≥ 15% (≥9/60 vs 3/60 expected), the permutation p-value over B=10,000 would sit far below 0.001. The bar is demanding, not prohibitive. Drafting correction 3 (B=10,000 for headroom below the bar) is correctly reasoned: minimum resolvable p ≈ 0.0001 < 0.00208.
- **Effect-size conjunct is good practice:** requiring both significance (p) and a meaningful effect (a ≥ 15% = 3× chance) guards against "significant but trivial" findings at n=60.

**Ruling:** the bar choice is sound, disclosed, and conservative in the anti-hype direction appropriate to a falsification-first program. Not a defect.

## 3. Canonical v̂₁ — verified sound

- **Coherence re-measured independently:** the reviewer computed mutual |cosine| over all 45 pairs from the hash-verified archive: **min 0.9956, max 0.9996, mean 0.9973 — exactly matching the draft's [OBSERVATION]**. All 45 pairs ≥ 0.99; breaking point (b)'s 0.99 gate has genuine headroom below the measured minimum.
- **Sign-aligned mean well-defined:** after sign-alignment (s_i = sign(V_i·V_0)), the mean has norm 0.9988 — the canonical direction is not a cancellation artifact.
- **Sign-alignment decision-irrelevant:** 1-NN on 1-D uses |s_i − s_j| with s_i = H_i·v̂₁. Under v̂₁ → −v̂₁, all scalars negate and all pairwise absolute differences are preserved, so nearest-neighbor assignments are identical. Verified empirically (dummy 60×1024 data: assignments identical under sign flip). The draft's claim is exact, and the §3.2 step-3 rule (+1 on exact-zero dot product) is a reproducible tie-break for a measure-zero event.

## 4. Breaking points — all sound; no missing trip, no over-strict trip

| ID | Assessment |
|---|---|
| (a) Direction-archive integrity | SHA-256 independently recomputed: `9b527c…13dc` **exact match**; 10 `v1__` keys confirmed. Sound. |
| (b) v̂₁ coherence ≥ 0.99 | Independently re-measured 0.9973 (see §3). Sound; failure correctly routes to RUN-INVALID (premise failure, not a verdict). |
| (c) Embedding-archive integrity | SHA-256 independently recomputed: `9219bd…95fae` **exact match**; shape (24, 60, 1024) float32 confirmed. Sound. |
| (d) Bench alignment | Strata independently counted from the archive: (P,A-first)=16, (P,C-first)=14, (E,A-first)=14, (E,C-first)=16 — **matches EXP092 §4's table** (`EXP092_IBL_PREREG_SIGNED.md:110`) and the draft's "16/14/14/16". Bench pin `9be816…` confirmed registered in the signed EXP092 pre-reg. Sound. |
| (e) Degeneracy | Zero variance of the 60 scalars → RUN-INVALID. Sound — a degenerate instrument cannot discriminate. |
| (f) Ties | Any exact 1-NN distance tie → RUN-INVALID. Sound: exact float ties on 1-D projections of distinct 1024-d vectors are measure-zero (EXP092 §3 precedent); a tie indicates archive corruption. Not over-strict. |
| (g) Label count | 20 unique labels independently confirmed; the K=20 / 5%-chance baseline is therefore correct. Sound. |

**Missing-trip sweep:** NaN/Inf in the scalars is not explicitly covered (see A1). Sign-cancellation of the mean is covered by (b). Archive-bitrot is covered by (a)/(c). Bench substitution is covered by (d). No other trip is missing.

## 5. S2 random-direction controls — adequately specified

8 seeded random unit vectors (`np.random.default_rng(137002)`, normalized), same 1-D 1-NN procedure as primary. The draft's §7 question — whether matched-norm specification is needed — is answered: **unit-norm vs unit-norm is apples-to-apples**; v̂₁ is a unit vector and the randoms are normalized to unit norm, so no further norm matching is required. In 1024 dimensions, accidental alignment of a random unit vector with v̂₁ is negligible (|cosine| concentrates near 0, σ ≈ 1/32). The control is non-binding and reported for interpretation only; the specification is sufficient for that role.

Seeds 137001/137002 confirmed unused elsewhere in the research log (grep clean excluding the EXP137 draft itself).

## 6. Worth-it gate (Law #15) — holds, all 7 points

1. Exact question stated (§2). 2. Decision changed: CONTINUE into reading-from-TGA designs vs KILL closing the TGA story (exists/carries nothing/moves nothing). 3. Cheapest test: two npz loads + 10,001 × 60 scalar 1-NN lookups; $0 CPU, ~15 min, zero new forwards — accurate. 4. Mathematical license: Fano-based MI bound (see A3 for a precision note), EXP127's R=8.24× [OBSERVATION], coherence [OBSERVATION] independently re-verified; quantitative prediction (a ≥ 15% w/ p < 0.00208 vs a ≤ 8%) stated. 5. Breaking point: a ≤ 8% → KILL. 6. Non-resurrection audit §6 (see §7 below). 7. Summit filter honest — no capability claim made or licensed.

## 7. Non-resurrection (Law #4) — sound

The audit table correctly distinguishes **decodability** (B3's claim) from **causality** (EXP131/133's killed claims) under the program's Decodability Gap dissociation (externally replicated, arXiv:2609.06951, LOG-4499). EXP092 decoded full 1024-d layer embeddings, never a 1-D v̂₁ projection. S5-3 fenced semantic/static directions; v̂₁ is a dynamics-derived direction class (LOG-4693). The staleness re-diff (full-log grep for any decode on v̂₁/TGA-direction projections) was clean — independently plausible given EXP127 measured amplification only. A CONTINUE here does not revive any injection claim; a KILL closes the story without touching EXP127's measurement CONTINUE. **Adequate.**

## 8. Statistical mechanics — no defect

- 1-NN LOO on 1-D absolute differences: standard; leave-one-out correctly excludes self-match.
- Stratified permutation (domain × phrasing, within-stratum shuffle): matches EXP092 §4; B=10,000 with `random.Random(137001 + b)` per permutation — deterministic, reproducible, adequate resolution.
- p = (1 + #{a^(b) ≥ a})/(1+B): standard exact form.
- EXP137 is the correct next free number (EXP136 = ARI pre-reg exists in `research/prereg/`).

## Advisories (non-blocking; no response required before launch)

- **A1 — NaN/Inf guard.** No breaking point explicitly covers non-finite scalars (e.g., a corrupted archive entry surviving the SHA check is impossible by construction, but a defensive `assert np.all(np.isfinite(scalars))` costs one line). Given both archives are hash-pinned and EXP092 already ran 1-NN successfully on A2, the residual risk is negligible. Suggested, not required.
- **A2 — Spot-id selection.** Breaking point (d)'s "cross-checks 5 spot ids against the EXP092-B bench pin" does not specify which 5. Recommend deterministic selection (e.g., first 5 in archive order) so the check is reproducible. The stratum counts + 60 unique ids already strongly identify the bench; this is belt-and-suspenders.
- **A3 — Fano precision.** §5.4 states "1-NN LOO accuracy is a finite-sample lower bound on mutual information via Fano's inequality." Strictly, Fano's inequality converts the error rate into a lower bound on I(X;Y); the accuracy *yields* the bound rather than *being* the bound. Suggest rephrasing for precision. Does not affect any mechanics.

---

## Verdict

**SIGN.** The pre-registration is exact, the highest-stakes derivation (layers[19]) is independently verified correct against the primary executor sources, every pinned constant the reviewer re-measured (both SHA-256 hashes, coherence 0.9973, strata 16/14/14/16, 20 labels, seed freshness) matches the draft, the decision table is exhaustive, the breaking points are sound, and the Law #4 audit holds. The three advisories are non-blocking. **Launch-ready pending the CEO launch decision.**

*Reviewer: independent Law #14 lane, LOG-4856. No repairs made (review only, per the single-lane fence).*
