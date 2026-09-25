# EXP093 — Layer-11 Causal Transfer: Pre-registration SIGNED

**Status:** SIGNED, 2026-09-25. Cleared for bundle build; execution requires independent bundle review + CEO clearance.

## Signature block (signing ceremony)

- **Experiment:** EXP093 — Layer-11 Causal Transfer. Causal test (static injection of the layer-11 task direction at layer 11) of the licensed EXP092 layer-11 CONTINUE.
- **Independent Law #14 review:** SIGN (binding) at LOG-4342 — narrow re-verification of the nine LOG-4340 upgrade conditions (LOG-4340 returned SIGN-WITH-FIXES; F1–F9 applied at LOG-4341; F1 re-verified by execution on the real `exp092_embeddings.npz` at LOG-4342). Review file: `experiments/protocols/REVIEWS/EXP093_LAW14_REVIEW_2026-09-25.md`.
- **Reviewed draft:** `experiments/protocols/EXP093_L11_CAUSAL_PREREG_DRAFT.md` v0.2 (UNSIGNED), commit `ca88c95`; verified byte-identical to the LOG-4342-reviewed version (git status clean; last touching commit `ca88c95`).
- **SHA-256 (reviewed draft content):** `33434fe34e8f56512dbbf5b9339509736e60462a94a1a96a10f0b90b5fae7378`
- **Signed by:** Nova (CEO), 2026-09-25, on the authority of the binding LOG-4342 SIGN.
- **Immutability:** this file is now IMMUTABLE. Corrections, if ever needed, go through append-only errata or a new experiment number (Law #4). The draft file is left untouched as the pre-signature record.
- **Body fidelity:** the protocol body below is byte-identical to the LOG-4342-reviewed draft. Its internal "DRAFT v0.2 / UNSIGNED" markers describe the pre-signature state and are superseded by this signature block.
- **SHA-256 (this signed file):** `3e0f269b9f2c5170d2b6ed37b2bd03f39f8eeb344914e8bb1f904709ad13db93`
  - Verification rule (self-referential digest convention — a digest cannot cover its own bytes): recompute SHA-256 over this file with the 64-character digest value after `**SHA-256 (this signed file):** ` replaced by the empty string. The result must equal the recorded value. Any other byte change breaks the match.

**Launch chain:** signed pre-registration (this file) → bundle build → independent bundle review → CEO execution clearance → execution.

---

# EXP093 — Layer-11 Causal Transfer: Pre-registration DRAFT (UNSIGNED)

**Status:** DRAFT v0.2 — **UNSIGNED**. Not cleared for bundle build. Independent Law #14 review of v0.1 returned **SIGN-WITH-FIXES** (binding, LOG-4340); v0.2 applies F1–F9 exactly as specified; re-verification of F1 by execution on the real `.npz` gates SIGN.

**Correction history (error-preservation standard):** v0.1 §3.1 defined an algebraically degenerate direction construction (the LOO mean of prototype residuals is identically the zero vector — residuals from class means sum to zero exactly, including under LOO; reviewer proved the identity and verified numerically at LOG-4340: pre-normalization norms 5.4e-17–6.9e-17 synthetic, max 7.178e-08 on the real `.npz`). v0.2 replaces §3.1 with the maximum-average-cosine shared correction direction (per-item normalization before averaging). The v0.1 formula is preserved on record in the §3.1 correction note; it is not silently erased.
**Author (drafter):** Pre-registration agent, reporting to CEO Nova, 2026-09-25.
**Lineage:** Direct successor of EXP092 (Information-Bottleneck Localization). EXP092 returned a licensed ADOPTED CONTINUE (LOG-4336 execution; LOG-4338 binding ADOPT-WITH-CORRECTIONS): "Frozen Pythia-410m layer 11 carries significant task information (1-NN LOO, Bonferroni-significant, ≥10pp above null q95) on the EXP092-B bench" (l* = 11, acc 0.3333, p = 0.000999, effect +0.2000; S = {1, 11, 12, 13, 14, 15, 17, 18}). This experiment is the licensed next step: the readout program was redirected to l* = 11, and EXP092's evidence is correlational. EXP093 is the causal test.

**Immutability note:** this is a draft. Once signed, it freezes; any design change becomes EXP094+.

---

## §0. Why this experiment exists (the gap it fills)

EXP092 proved *information presence*: the frozen model's layer-11 final-token embeddings carry target-entity information decodable at 33.3% against 5% chance. It did not prove *information potency*: whether that information can move the model's actual decisions. The program's boundary history is a warning — at layer 20, raw geometric similarity (~0.7 cosine) coexisted with **zero causal transfer** under static injection (EXP065/066/077 lineage; the licensed boundary). EXP093 asks whether layer 11 repeats that story (information without influence) or breaks it (information that transfers).

The candidate mechanism is **static injection of the layer-11 task direction at layer 11 during the decision forward pass**, measuring Δdecision-accuracy on the EXP092-B bench. This is the honest causal counterpart to EXP092's correlational 1-NN: same bench, same layer, same frozen weights — but an intervention, not an observation.

---

## §1. Law #15 (explicit)

**(1) Precise question.** Does static injection of the layer-11 task direction — the LOO maximum-average-cosine shared correction direction derived from the EXP092 layer-11 embeddings (§3) — at layer 11 causally move frozen Pythia-410m's binary decisions on the EXP092-B bench? I.e., is the licensed layer-11 information causally potent under static injection, or merely decodable?

**(2) KILL / CONTINUE / PIVOT decision it changes.**
- **CONTINUE** (all three §5 bars met on the phrasing-balanced aggregate): the layer-11 task geometry is causally steerable — static injection moves decisions by ≥10pp. The static-injection program is alive at layer 11 (it died at layer 20); the program builds on the direction (amplify, compose, transfer).
- **KILL** (no McNemar-significant effect in any stratum): the layer-11 information is causally inert under static injection. The EXP092 correlational signal does not transfer — *information ≠ influence* — generalizing the layer-20 boundary to layer 11. The *shared* static-injection family stands down at layer 11 (per-item static directions remain EXP094+ material per §7); the program must look to non-shared or non-static mechanisms (gated, dynamic, multi-layer) or retire the room.
- **PIVOT** (partial/ambiguous signal): (a) the effect is phrasing-gated (A-first only) — the O1 caveat confirmed causally, program pivots to phrasing-conditioned mechanisms; or (b) the effect is significant but sub-threshold or non-monotone (perturbation, not direction) — program pivots to mechanism forensics instead of building on the direction.

**(3) Cheapest falsifying test and its cost.** 60 bench items × 3 conditions (clean baseline, +v injection, −v sign-flip placebo) = **180 forward passes** on CPU, plus direction construction from the archived `.npz` (numpy, seconds — no new extraction). The −v arm is the falsifier-within-the-test: if −v helps as much as +v, the effect is perturbation, not direction, and the hypothesis dies even with a positive Δ. **Cost: ~10–15 CPU-minutes, $0 GPU.**

**(4) Mathematical license, quantitative prediction, breaking point.**
- *License.* EXP092 licensed I(H₁₁; Y) > 0 via Fano/1-NN (Y = target entity). The binary decision D is a deterministic function of the final logits, hence of the layer-11 final-token state h (composed with frozen downstream layers). Let m(h) = logit(target) − logit(foil) be the correct-margin. The intervention sets h′ = h + αv; to first order, Δm ≈ α⟨∇ₕm, v⟩. The registered v (§3) is the LOO maximum-average-cosine shared correction direction — the unit vector best aligned with the 60 per-item "toward correct class prototype" corrections. Under H1 (a shared decision-relevant component exists in the layer-11 geometry), ⟨∇ₕm, v⟩ > 0 on average, so Δm > 0 and decision accuracy rises; under the sign flip, Δm < 0 and accuracy falls.
- *Quantitative prediction.* On the phrasing-balanced aggregate (n = 60): acc(+v) − acc(baseline) **≥ 0.10** (10pp — the program's de facto meaningful magnitude, same bar as EXP092 §5 and the EXP077 bridge rescue), McNemar exact two-sided **p < 0.05** for +v vs baseline, and strict monotonicity **acc(+v) > acc(baseline) > acc(−v)**.
- *Breaking point.* The hypothesis dies if any of: (i) Δ < 0.10 — the effect is too small to build on; (ii) McNemar p ≥ 0.05 — not significant; (iii) acc(−v) ≥ acc(+v) — the effect is not direction-specific (perturbation alternative); (iv) the clean baseline fails to reproduce S2's 36/60 — the decision pipeline is not what was measured (RUN-INVALID, not a verdict).
- *Scope.* A KILL falsifies "**≥10pp causal transfer via a shared static direction at layer 11**," not "any causal role of layer-11 information." Per-item (non-shared) directions, dynamic/gated mechanisms, and multi-layer compositions are out of scope — they are EXP094+ material, named in §7.

---

## §2. Bench: EXP092-B reused verbatim (no new text)

- **The 60 prompts, option orders, and labels are byte-identical to the EXP092-B bench.** Bench pin (SHA-256 over the registered canonical serialization): `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4`.
- **Rationale for verbatim reuse:** the decision under test is the S2-style binary choice (target vs foil option token) on the exact items whose layer-11 geometry was licensed. Any prompt change would break comparability with EXP092 and require a new G1′; verbatim reuse inherits EXP092's G1′ (240/240 single-token in-prompt, real-tokenizer offset-mapping cover) via bench-pin byte-identity.
- **Strata** (unchanged): (planetary, A-first) = 16, (planetary, C-first) = 14, (elemental, A-first) = 14, (elemental, C-first) = 16. Phrasing-balanced 30/30 by construction.
- **Option token IDs:** the target and foil are single tokens in-prompt (G1′). Their token IDs are recovered from the real tokenizer's offset mapping over the actual prompt (the EXP092 G1′ procedure) — never by re-tokenizing entity strings in isolation (EXP090 lesson: bare-word tokenization is unsatisfied).

---

## §3. Intervention

### 3.1 The layer-11 task direction (registered construction, from the archived `.npz`, read-only)

Source: `experiments/runs/EXP092_ibl/out/exp092_embeddings.npz` — layer index 11, shape (24, 60, 1024), float32. Item order = bench order (asserted by the bundle against the `.npz`'s stored label vector; see G2).

> **v0.1 → v0.2 CORRECTION (dated 2026-09-25; binding LOG-4340; error-preservation standard).** v0.1 defined, for each j ≠ i, c^{−i}(j) = mean{ h(k) : k ≠ i, k ≠ j, target(k)=target(j) } and v^{−i} = normalize( mean_{j≠i} [c^{−i}(j) − h(j)] ). This construction is **algebraically degenerate**: mean_{j≠i}[c^{−i}(j) − h(j)] = **0 exactly** for every i — residuals from class means sum to zero exactly, class by class, including under LOO (the oldest identity in statistics). The reviewer proved the identity and verified numerically: pre-normalization norms 5.4e-17–6.9e-17 on synthetic data, max 7.178e-08 on the real archived `.npz` (float32 noise around analytic zero). `normalize()` of this vector divides by zero → NaN; G2's ‖v‖=1 assertion would have forced RUN-INVALID. The experiment was **unexecutable** as written, not merely weak. The drafter's intent ("the shared static direction that prototypicalizes any item") is preserved; the construction below replaces the v0.1 formula. The v0.1 formula is retained here on record and is NOT to be used.

For each item i ∈ {1…60}, define the **leave-one-out prototype residual**:

- h(i) = layer-11 final-token embedding of item i.
- c^{−i}(i) = mean{ h(k) : k ≠ i, target(k) = target(i) } — the class prototype of i's target, excluding i (mean of 2 items; always defined).
- r_i = c^{−i}(i) − h(i); the bundle asserts ‖r_i‖ > 1e-9 for all i (else RUN-INVALID — an item coinciding with its LOO prototype makes the direction undefined).
- u_i = r_i / ‖r_i‖ — the unit LOO correction direction.

The **shared direction for item i** is v^{−i} = normalize( (1/59) Σ_{j≠i} u_j ), computed **without item i's data** (zero leakage at test time), without model gradients, without new extraction.

**Mathematical note (registered):** the unnormalized mean Σ_j[c(j)−h(j)] is identically zero (residuals-from-class-means sum to zero, exactly, including under LOO — the v0.1 construction was degenerate by this identity). Per-item normalization before averaging breaks the zero-sum; v^{−i} is the unit vector maximizing average cosine with the 60 LOO correction directions.

**Why this direction.** It is the direct causal translation of the licensed 1-NN finding: if the layer-11 geometry clusters items by target entity, the maximum-average-cosine shared correction direction is the shared static direction that best "prototypicalizes" any item. Rejected alternatives are in Appendix A.

**Coherence diagnostic (registered, reported, non-binding):** the bundle reports the mean pairwise cosine among {u_i} and the pre-normalization ‖(1/59)Σ_{j≠i}u_j‖.

**Registered measurement (reviewer-verified on the archived `.npz`, 2026-09-25, LOG-4340):** min_i ‖r_i‖ = 1.3352 (no degeneracy — the ‖r_i‖ > 1e-9 assertion is satisfiable); mean pairwise cosine(u_i,u_j) = **−0.0160**; pre-normalization shared-direction norm ∈ [0.0246, 0.0444]; all 60 v^{−i} unit-norm, mutually near-identical (max pairwise cosine 0.9554, as expected for LOO variants).

**Registered implication:** the shared component is ~3% coherent — the "shared static direction" hypothesis is *a priori* weak (correction directions are nearly mutually orthogonal, slightly anti-aligned by the zero-sum constraint). This experiment is therefore a genuine falsification attempt: **KILL is the expected outcome**, and a CONTINUE would be surprising and informative.

**Interpretation boundary (registered):** the direction is label-informed in construction (it uses target groupings). Precedent: the LOG-204 bridge demotion — label-informed directions are *rescue controls (known-answer directions), NOT mechanism controls*. A CONTINUE therefore licenses **steerability** ("the layer-11 task geometry is causally steerable by a static direction"), not autonomous mechanism use, not a capability claim. This boundary is restated in §8.

### 3.2 Injection mechanics (registered)

- **Site:** post-block residual stream at **layer 11**, **final token position only** (the measurement site of EXP092 and the decision site of S2).
- **Operation:** h ← h + α·v^{−i}, with **α = 1.0** and v^{−i} unit-normalized. (Diagnostic, non-binding: the bundle reports ‖αv‖ / median(‖h₁₁‖) over the 60 items so the perturbation magnitude is on the record.)
- **Implementation:** forward hook on the layer-11 block output (Pythia/GPTNeoX: `gpt_neox.layers[11]`), adding the vector at the final position before layer 12's input. The bundle resolves the module path; G5 verifies placement by execution.
- **Conditions per item** (3 forward passes each, 180 total):
  - **B** (baseline): clean forward pass, no injection.
  - **P** (positive): inject +α·v^{−i}.
  - **N** (negative / sign-flip placebo): inject −α·v^{−i}.
- **Decision rule** (S2 procedure, per condition): correct iff logit(target-token) > logit(foil-token) at the final position. Ties (exact logit equality) → the item is scored as *incorrect* in that condition AND the tie is logged; if ties occur on >5% of item-conditions, RUN-INVALID (degenerate measurement). This is exactly S2's tie rule in the EXP092 scorer (`s2_lm_baseline` in `score_exp092.py`: `correct = logp[:,0] > logp[:,1]` — strict inequality; exact ties scored incorrect). EXP092 armed the rule but recorded zero ties, so the G4 36/60 baseline is well-defined under this rule.

### 3.3 Why the −v arm (the falsifier inside the test)

Any intervention perturbs the residual stream; a perturbation alone can flip near-zero-margin decisions (S2's mean margin was −0.0018 — decisions are fragile). The −v arm distinguishes **direction** from **perturbation**: under H1, +v helps and −v hurts (monotone in sign); under the perturbation alternative, +v and −v move accuracy symmetrically or not at all. The monotonicity bar (§4) is what kills the "any nudge works" reading.

---

## §4. Statistics

### 4.1 Primary (decision-driving)

- **Δ = acc(P) − acc(B)** on the phrasing-balanced aggregate (n = 60).
- **McNemar exact test** (two-sided) on the paired P-vs-B outcomes (correct/incorrect per item). α = 0.05, no multiplicity correction on the primary (single pre-registered comparison; cf. EXP092's Bonferroni which was for a 24-layer scan — there is no scan here).
- **Monotonicity:** strict acc(P) > acc(B) > acc(N) on observed accuracies.
- **Bars (all three required for CONTINUE):** Δ ≥ 0.10 **and** McNemar p < 0.05 **and** strict monotonicity.

### 4.2 Stratified (registered, phrasing — the O1 caveat)

Per stratum (A-first n = 30; C-first n = 30): Δ_s, McNemar nominal p_s, within-stratum monotonicity. Reported with nominal p-values (multiplicity noted, not corrected — the 10pp bar and monotonicity are the load-bearing gates, mirroring EXP092's structure). These drive the PIVOT(a) arm (§5).

### 4.3 Secondaries (reported, non-binding)

- McNemar (N-vs-B): expected Δ_N = acc(N) − acc(B) ≤ 0; reported for the record.
- Mean margin shift: mean[logit-margin(P) − logit-margin(B)] and the N counterpart — the continuous analog of Δ.
- Flip ledger: which items flip under P (B-wrong→P-right) and under N, cross-tabulated against EXP092's per-item 1-NN correctness (exploratory — does steerability concentrate where the geometry was already informative?).
- Anisotropy-alignment diagnostic (R1, non-binding): cosine between the mean v^{−i} and the H1 static-anisotropy bias direction (null re-mining, LOG-4316/4317) — constrains the "wrong direction" interpretation of a KILL.
- Correction-magnitude correlation (R3, non-binding): per-item Pearson correlation between P-condition margin shift and ‖r_i‖ — the correction mechanism predicts larger shifts for items farther from their prototype.

### 4.4 Power note (registered limitation)

With n = 60 paired binary outcomes, McNemar's exact test at α = 0.05 reaches significance at roughly ≥7 net flips (≈12pp) with few reversals. The design is powered for the registered ≥10pp effect; a true effect in the 3–8pp range will likely miss significance. **A KILL is therefore scoped**: it falsifies ≥10pp causal transfer, not sub-threshold influence. This is stated plainly so a null is not over-read.

---

## §5. Decision tree (TOTAL)

Let Δ, p, mono denote the aggregate statistics; Δ_A, p_A, mono_A and Δ_C, p_C, mono_C the strata.

- **CONTINUE** — Δ ≥ 0.10 **and** p < 0.05 **and** mono (strict P > B > N) on the aggregate. Licensed claim: "The LOO maximum-average-cosine shared correction direction at layer 11 causally steers frozen Pythia-410m's binary decisions on EXP092-B by ≥10pp (McNemar p < 0.05, sign-monotone). Stratum breakdown: Δ_A = __, Δ_C = __ (registered §4.2); the O1 phrasing-sensitivity caveat (§8.3) is part of this claim." Licensed consequence: the static-injection program is alive at layer 11 — build on the direction. Interpretation boundary per §8 (steerability, not autonomous mechanism; novelty N1; no capability claim).
- **KILL** — every McNemar p (aggregate, A-first, C-first; P-vs-B) ≥ 0.05. Licensed claim: "Static injection of the shared layer-11 task direction does not move decisions on EXP092-B (no significant transfer at any phrasing). The EXP092 correlational signal is causally inert under static injection — information ≠ influence at layer 11." Program consequence: the *shared* static-injection family stands down at layer 11 (per-item static directions remain EXP094+ material per §7); the layer-20 boundary generalizes.
- **PIVOT** — aggregate fails CONTINUE, but:
  - (a) **Phrasing-gated:** A-first meets all three bars (Δ_A ≥ 0.10, p_A < 0.05, mono_A) while C-first does not → the O1 caveat is confirmed causally; program pivots to phrasing-conditioned mechanisms.
  - (b) **Weak / non-directional:** some McNemar p < 0.05 (P-vs-B **or** N-vs-B) but the 10pp bar or monotonicity fails (significant-but-sub-threshold, or +v helps but −v doesn't hurt) → the signal is not direction-specific or not buildable; pivot to mechanism forensics, do not build on the direction. Significant N-vs-B with non-significant P-vs-B routes here (forensics), not to KILL.
  - (c) **Contrary-stratum significance:** C-first meets all three bars (Δ_C ≥ 0.10, p_C < 0.05, mono_C) while the aggregate fails CONTINUE → PIVOT to mechanism forensics. Rationale: contradicts the registered O1 directional prior; with nominal stratum p-values the false-positive risk is material, so no CONTINUE (no surprise-hunting reward) — but KILL's licensed claim would be false, so forensics with a new pre-registration before any build.
- **RUN-INVALID** — any guard failure (§6); tie rate > 5% of item-conditions; injection hook verified misplaced (G5); baseline reproduction failure (G4); or degenerate measurements (e.g., zero variance in any condition's outcomes). Never a verdict.

---

## §6. Guards and refusal gates (protocol-local definitions)

- **G0 (bench provenance):** bundle asserts bench SHA-256 = `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4` over the registered canonical serialization; prompts byte-identical to EXP092-B; strata match §2. Else RUN-INVALID.
- **G1 (Δθ=0):** state_dict SHA-256 (sorted keys, float32 bytes — EXP077/EXP091/EXP092 procedure) equals the LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`, checked pre- AND post-run. Snapshot: `/home/hatch/workspace/.exp086_weights/pythia-410m` (integrity confirmed LOG-4321). Mismatch → RUN-INVALID.
- **G1′ (tokenizer — inherited):** no new text is introduced (prompts byte-identical per G0); tokenizer satisfiability is inherited from EXP092's 240/240 real-tokenizer cover via bench-pin byte-identity. Option token IDs are recovered from the real tokenizer's offset mapping over the actual prompt (never by re-tokenizing entity strings in isolation — EXP090 lesson).
- **G2 (direction provenance):** the `.npz` exists, shape (24, 60, 1024), float32; its stored label vector matches the bench's target sequence (item-order assertion); the bundle recomputes {r_i}, {u_i}, {v^{−i}} from the `.npz` using the §3.1 LOO max-cosine procedure (no cached/precomputed direction files); asserts ‖r_i‖ > 1e-9 for all i (an item coinciding with its LOO prototype makes the direction undefined → RUN-INVALID); asserts ‖v^{−i}‖ = 1 for all i; α = 1.0; reports the coherence diagnostic (mean pairwise cosine among {u_i}; pre-normalization ‖(1/59)Σ_{j≠i}u_j‖). Any deviation → RUN-INVALID.
- **G3 (mode stamp):** `mode` ∈ {mock, real} on every artifact (EXP092 convention).
- **G4 (baseline reproduction):** the clean condition B must reproduce S2's registered baseline **exactly**: 36/60 correct, mean logit-margin within 1e-4 of the registered reference −0.0018 (full-precision −0.001819 per LOG-4338; the 1e-4 tolerance covers the recorded rounding precision). The model is deterministic and the prompts are byte-identical — any deviation means the decision pipeline drifted → RUN-INVALID, not a verdict. The bundle pins torch intra-op thread count to the EXP092 extraction value, records it in the run meta, and asserts it before condition B (thread-count differences can flip near-zero margins). S2's tie rule (§3.2) governs: the 36/60 baseline is well-defined under it.
- **G5 (injection-site verification):** before the real run, the bundle proves by execution (mock or single-item probe) that the hook adds exactly α·v at the layer-11 post-block residual, final position only, and that layer-12's input is unchanged at all other positions. Acceptance criteria (registered): (i) on a single-item probe, hooked final-position residual = unhooked value + α·v^{−i} within relative 1e-6; (ii) all other positions change by < 1e-9 absolute; (iii) condition B (hook disabled) logits bit-match a hook-free reference run. Misplacement → RUN-INVALID.
- **Signed-protocol digest:** the runner refuses unless the SIGNED file's SHA-256 matches the digest recorded at signing (computed when this draft is signed).

---

## §7. Secondaries and future-work notes (non-binding)

- S1–S3 as listed in §4.3 (including the R1 anisotropy-alignment and R3 correction-magnitude secondaries).
- **Deferred recommendations (LOG-4340, non-blocking):** R2 (α=0.5 dose-response secondary, 60 extra passes) — deferred to bundle-build discretion; not registered here. R4 (assert the 60 v^{−i} are not bit-identical) — a bundle-build checkpoint, not a protocol registration.
- **EXP094+ candidates (named, not designed):** per-item (non-shared) LOO directions — tests whether steerability exists without a shared direction (the hypothesis this experiment's KILL would leave open); gated/dynamic injection (condition the injection on the item's own layer-11 state); multi-layer composition (inject at 11, read the effect at 12–18).
- The S1 (Ross kNN-MI) specification stays retired per LOG-4338/C2 — no MI secondary is registered here.

---

## §8. Interpretation boundary (binding on any write-up)

1. The direction is **label-informed in construction** (uses target groupings from the `.npz` labels). By the LOG-204 precedent (bridge demoted to "rescue control, NOT a mechanism control"), a CONTINUE licenses **causal steerability of the layer-11 task geometry** — an existence proof that the information *can* be made to move decisions — and **does not** license: autonomous mechanism use by the model, a capability claim, or any superhuman/consciousness language. Novelty remains N1.
2. A KILL licenses **causal inertness under static injection**, scoped to ≥10pp transfer via a shared static direction (§4.4). It does not license "layer 11 is useless" — the information is present (EXP092, licensed); it is the *static-injection transfer* that fails.
3. The O1 phrasing caveat travels with every consequence: any layer-11 readout or steering inherits A-first/C-first asymmetry until proven otherwise.

---

## §9. Budget and venue

- **$0 GPU. CPU-only.** 180 forward passes (Pythia-410m, CPU) + 2 state-dict hashes + numpy direction construction. Estimated **~10–15 CPU-minutes** (EXP092's 60 passes took ~100s wall time).
- **Venue:** local CPU, venv `~/workspace/.venv-exp077` (torch CPU + transformers + safetensors + accelerate, per EXP092).
- **Read-only:** weights snapshot, the EXP092 `.npz`/logs/meta, the signed EXP092 protocol. No new extraction; no re-download.
- **Thread pinning (F8):** the bundle pins torch intra-op thread count to the EXP092 extraction value, records it in the run meta, and asserts it before condition B (see G4).

---

## Appendix A. Rejected direction alternatives (for the Law #14 review)

1. **Gradient-of-margin direction** (mean ∇ₕ[logit(target)−logit(foil)] over construction items): uses the model's own backward gradients *plus* labels — the most label-informed direction constructible. Nearly tautological (tests whether finite gradient steps work, not whether the EXP092 geometry transfers); closest to a rescue artifact. **Rejected.**
2. **Bare-entity direction** (target-minus-foil from bare-word embeddings): requires 20 new forward passes and a *new* G1′ — EXP090 proved bare-word tokenization is unsatisfied ("Mars" is two tokens bare). The licensed geometry is in-prompt, not bare-word. **Rejected.**
3. **Whole-residual amplification** (gain, not direction): confounds information with magnitude; not a task direction. **Rejected.**
4. **Per-item non-shared directions**: a different hypothesis ("each item has its own steerable direction") — legitimate, but it is EXP094 material, not this experiment. **Deferred, named in §7.**
5. **Top-PC of the residual matrix** (data-driven shared direction): rejected — less interpretable than the hypothesis-driven max-cosine correction direction; PC1 need not align with prototypicalization. **Rejected.**

## Appendix B. Registered constants

| Constant | Value | Source |
|---|---|---|
| Bench pin (EXP092-B) | `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4` | EXP092 signed §2 |
| Weights pin (LOG-331) | `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` | LOG-331 / LOG-4321 |
| Weights snapshot | `/home/hatch/workspace/.exp086_weights/pythia-410m` | LOG-4321 |
| Direction source | `experiments/runs/EXP092_ibl/out/exp092_embeddings.npz` (24,60,1024 float32) | EXP092 run report |
| S2 baseline | 36/60 = 0.60; mean margin −0.0018 | EXP092 run report |
| Shared-direction coherence | mean pairwise cosine(u_i,u_j) = −0.0160; pre-norm ‖(1/59)Σ_{j≠i}u_j‖ ∈ [0.0246, 0.0444]; min_i ‖r_i‖ = 1.3352 | Reviewer execution on archived `.npz` (LOG-4340) |
| O1 phrasing split | A-first 16/30 (53.3%), C-first 4/30 (13.3%) at layer 11 | LOG-4338 |
| Injection | layer 11 post-block residual, final position; α = 1.0; v unit norm | §3.2 (this draft) |
| Primary bars | Δ ≥ 0.10; McNemar exact p < 0.05; strict P > B > N | §4.1 (this draft) |
| Budget | ~10–15 CPU-min, $0 | §9 (this draft) |

---

*End of EXP093 draft v0.2 (UNSIGNED). Next: independent Law #14 re-verification of F1–F9 (F1 by execution on the real `.npz`) → SIGN → bundle build → bundle review → CEO clearance → execution.*
