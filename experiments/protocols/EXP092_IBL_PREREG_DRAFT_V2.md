# EXP092 v2 — Information-Bottleneck Localization (IBL): Pre-registration DRAFT (UNSIGNED)

**Status:** DRAFT v2.1 — UNSIGNED. Not cleared for bundle build or execution.
**Supersedes:** `EXP092_IBL_PREREG_DRAFT.md` (v1), which was REJECTED at LOG-4319 (see §0); v2.0, which received SIGN-WITH-FIXES at LOG-4323 (see §0).
**Author (drafter):** Pre-registration agent, 2026-09-25.
**Review required:** Independent Law #14 review → (if ADOPT) bundle build → independent bundle review → CEO clearance → execution.

---

## §0. v1 → v2 lineage: why v1 was rejected and what changed

### v1 rejection (LOG-4319, binding)

The independent Law #14 review of EXP092 v1 returned **REJECT**. The binding reason:

> EXP091's 60-item bench contained only **10 unique 2-hop triples** and **5 unique 3-hop quads** per relevant construction. **50/60 items shared a triple/quad** with another item. The label was **deterministic from the tuple**, so an **entity-set oracle** (classify by which entities appear in the premise, ignoring order/relations) could achieve very high accuracy **without any relational information**. The v1 permutation null (permuting labels within strata) **broke the tuple→label relation** and therefore **could not calibrate the entity-set confound**. Consequence: the CONTINUE branch was biased upward and KILL was effectively unreachable — the decision tree was not a fair test.

Review file: `experiments/protocols/REVIEWS/EXP092_LAW14_REVIEW_2026-09-25.md`.

### v2 redesign (addresses the rejection point-by-point)

| # | v1 defect | v2 fix | Proof |
|---|-----------|--------|-------|
| 1 | Bench reused EXP091's (50/60 duplicate tuples; label deterministic from tuple) | **Fresh bench**: 60 items built from **60 unique ordered tuples** (15 triples + 15 quads per domain), deterministic seed-1022 assignment, registered in §6 | Uniqueness verified by execution: 60/60 unique under `(domain, tuple)` key |
| 2 | 5 entities/domain → entity-set overlap highly predictive | **10 entities/domain** (20 total), each target appears exactly 3× per domain; vocabularies verified single-token in-prompt | G1′ verified by execution: 240/240 A/C occurrences single-token, all 20 entities |
| 3 | Permutation null could not calibrate the entity-set confound | **Entity-set oracle explicitly constructed and tested**: leave-one-out 1-NN by max premise-entity overlap, analytic expected-accuracy tie-break, same stratified permutation scheme | Oracle acc = **0.0607** (6.07%), permutation p = **0.5312** (10,000 perms, seed 9207, reference implementation) — oracle is AT CHANCE and NOT significant under the null; the null **validly calibrates** the confound |
| 4 | K=10 labels, chance 10% | K=**20** labels (10/domain), chance **5%**; Fano license re-derived for K=20 (§1) | — |
| 5 | Weights path pointed at EXP086 bundle | **Weights relocated**: `experiments/runs/EXP086_amplifier/weights/pythia-410m/` → `/home/hatch/workspace/.exp086_weights/pythia-410m/` (moved to keep the repo committable; content presumed identical, **hash re-verification PENDING — see §6 G1 caveat**) | Relocation observed 2026-09-25; tokenizer loads from new path |

### What v2 preserves from v1 (with justification)

- **1-NN leave-one-out statistic.** The Law #14 review did not fault the statistic itself, only the bench/null calibration. 1-NN LOO is retained because (a) it is a finite-sample-robust lower bound on mutual information via Fano's inequality (license in §1), (b) it requires no trainable parameters (frozen-backbone law), and (c) it is directly comparable to EXP091's cosine-scoring instrument (same bench family, same n=60).
- **≥10pp effect bar** (`a_l − q95_l ≥ 0.10`). Retained: 10pp is the program's de facto meaningful-signal magnitude (bridge rescue was +10pp at EXP077, +16.67pp at EXP070). With K=20 (chance 5%), a 10pp margin above the null q95 is a *stronger* practical-significance gate than it was at K=10, not a weaker one.
- **Bonferroni null** (α = 0.05/24). Retained: 24 layers, family-wise error control unchanged. The review faulted the null's *calibration* (confound), not its *multiplicity correction*.
- **Full TOTAL decision tree** (CONTINUE / KILL / PIVOT). Retained with the KILL branch now genuinely reachable (the oracle proof in §8 shows the confound is calibrated, so a null result is interpretable as absence of signal, not as a broken instrument).

### v2.0 → v2.1 changelog (LOG-4323 SIGN-WITH-FIXES — both fixes applied, verified by execution)

The independent Law #14 review of v2.0 returned **SIGN-WITH-FIXES** (binding, LOG-4323; review: `experiments/protocols/REVIEWS/EXP092_LAW14_REVIEW_V2_2026-09-25.md`). The v1 confound fix was verified sound (oracle 0.0607 reproduced exactly by the reviewer; G1′ 240/240; Appendix C 20/20). Two load-bearing fixes were required, both textual/registrational — no redesign, no new data:

| # | Review finding | v2.1 fix | Execution proof |
|---|---------------|----------|-----------------|
| FIX 1 | Appendix-A parity sentence ("planetary A-first iff i odd") contradicted §4's strata table and the parenthetical (both: 8 A-first/block planetary) | Sentence corrected: **planetary A-first iff i even; elemental A-first iff i odd** (quads: same rule) | Bench rebuilt from corrected spec: strata = (P,A-first)=16, (P,C-first)=14, (E,A-first)=14, (E,C-first)=16 — matches §4 exactly; 60/60 prompts byte-identical to the reviewer's verified parity-B reconstruction |
| FIX 2 | Bench SHA-256 pin `2996ac8b…3ac3e` not reproducible from the registered spec (8 serializations tried; item schema and option-order rule unregistered) | **Registered the exact canonical serialization** — item-dict schema (`id,prompt,A,C,ent,typ,hop,domain,phrasing,tuple`), `json.dumps(bench, sort_keys=True, separators=(",",":"), ensure_ascii=True).encode("utf-8")` → SHA-256; **registered the option-order rule** (target first iff A-first); pin **recomputed from the reference implementation**: `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4`. Reference implementation cited: `experiments/runs/EXP092_ibl/reference_implementation.py` (also pins the G2 oracle/permutation code: analytic expected-accuracy tie-break, `random.Random(9207+b)` per permutation b) | `verify_g0()` passes: 60/60 unique `(domain,tuple)`, 20/20 targets ×3/domain, 30/30 phrasing, pin recomputes. G2 diagnostic: oracle = 0.0607, p = 0.5312 (10,000 perms, seed 9207) — NOT significant, gate PASS |

**Informational (non-design) update:** the §6 G1 weights-integrity caveat is recorded **RESOLVED**. The parallel investigation (LOG-4321, committed `f8014fd`) found the relocated snapshot byte-intact — the mismatch was a procedural artifact (the v2.0 drafter hashed the raw safetensors file, 364 tensors, instead of the loaded `state_dict`, 292 tensors); the LOG-331 pin `ec276abe…` was reproduced exactly from the relocated snapshot. The Law #14 v2 review (§4) ruled the draft's fail-safe posture correct and the caveat resolved; the normal launch chain is no longer gated on weights integrity. No design change; the G1 guard text now states the resolution.

The old pin `2996ac8b…3ac3e` is **retired**: it could not be derived from any registered spec and is struck from the draft. The v2.1 pin above is the binding one.

---

## §1. Exact question (Law #15)

**Q.** For frozen Pythia-410m, does the residual stream at *any* layer carry mutual information about the correct relational answer — i.e., is EXP091's layer-20 null a *localization* failure (information present elsewhere) or an *absence* failure (information not present at any layer)?

**Affected decision.** If a non-layer-20 layer carries significant task information, the program's readout/injection target moves from layer 20 to that layer (CONTINUE with re-targeting). If no layer does, the "output-side room" as an autonomous-mechanism program loses its last refuge: the bridge's +10pp must come from its label-informed construction (strengthening the LOG-204 artifact interpretation), and the honest next step is artifact forensics or retirement of the room (KILL).

**Cheapest falsifier / cost.** 60 forward passes (final-token hidden states, all 24 layers) on CPU + 1-NN LOO per layer + stratified permutation null. $0 GPU, ~1.5 CPU-hours. (The forward passes are the dominant cost; the statistics are trivial.)

**Mathematical license.** 1-NN leave-one-out accuracy is a finite-sample lower bound on mutual information I(H_l; Y) via Fano's inequality: for K=20 classes, P_e ≥ (H(Y) − I(H_l;Y) − h(P_e))/log(K−1). At chance (P_e = 0.95), Fano is tight: h(0.95) + 0.95·log₂(19) ≈ 4.322 = log₂(20). Any layer with 1-NN accuracy significantly above the permutation null therefore certifies I(H_l; Y) > 0 at that layer. The permutation null (labels permuted within domain × phrasing strata) destroys exactly the H_l→Y relation while preserving all marginal structure, so significance cannot be attributed to entity-frequency or phrasing artifacts — **and §8 proves it cannot be attributed to entity-set encoding either**.

**Quantitative prediction.** Under H₀ (no layer carries task information): all 24 layer accuracies lie within the stratified permutation null; max_l a_l ≤ q95_null + sampling noise; no p_l < 0.05/24. Under H₁ (localized information): ∃ l with p_l < 0.05/24 AND (a_l − q95_l) ≥ 0.10.

**Breaking point.** The license breaks if (a) the bench admits a non-relational shortcut the null doesn't calibrate (killed by §8's oracle proof), (b) the tokenizer check fails (G1′), (c) Δθ≠0 (G1), or (d) the null is miscalibrated (G2).

---

## §2. Bench: EXP092-B (fresh construction, registered)

**Design rationale.** The Law #14 review recommended *fresh construction with a no-duplicate invariant* over patching the old bench. v2 builds a new 60-item bench from scratch:

- **Vocabularies** (10/domain, all verified single-token in spaced/in-prompt form by real-tokenizer probe 2026-09-25):
  - *Planetary*: Mars, Venus, Jupiter, Saturn, Mercury, Europa, Titan, Io, Triton, Miranda
  - *Elemental*: Iron, Gold, Silver, Bronze, Steel, Tin, Lead, Silicon, Carbon, Crystal
  - Note: "Crystal" is a material, not an element. Domain coherence is **not** a registered requirement — the stratification (§4) requires only that the two entity sets be disjoint. The domain label is retained for lineage with EXP091.
- **Tuples**: 15 ordered triples + 15 ordered quads per domain, **all 60 unique** under the `(domain, tuple)` key. Deterministic assignment from RNG seed **1022** (rejection-sampled for uniqueness), registered verbatim in §6.
- **Balance**: each of the 20 target entities appears **exactly 3×** as the correct answer within its domain; 30 A-first / 30 C-first phrasing; prompt templates identical to EXP091 (2-hop and 3-hop forms).
- **Bench hash** (SHA-256 over the registered canonical serialization): `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4`
- **Canonical serialization (registered, FIX 2):** each item is the dict `{"id","prompt","A","C","ent","typ","hop","domain","phrasing","tuple"}` where `A`/`ent` = target entity name, `C` = foil entity name (2-hop: the C tuple element; 3-hop: the D tuple element), `typ` ∈ {planet, element}, `hop` ∈ {2,3}, `tuple` = ordered index list. Bench order: planetary 2-hop (15), planetary 3-hop (15), elemental 2-hop (15), elemental 3-hop (15); ids `exp092_{planetary|elemental}_{2hop|3hop}_{i}`. Serialization: `json.dumps(bench, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")`; pin = SHA-256 hexdigest of those bytes. Reference implementation: `experiments/runs/EXP092_ibl/reference_implementation.py` (`build_bench()`, `canonical_json()`, `bench_sha256()`).
- **Question-option-order rule (registered, FIX 2):** the options list the target first iff the item is A-first: `q_opts = "{A} or {F}"` if A-first else `"{F} or {A}"`, where F is the foil. (The v2.0 draft left this unregistered; the rule is now pinned.)
- **G1′** (real-tokenizer offset-mapping cover check, all 60 prompts): **240/240** A/C occurrences single-token in-prompt, 0 failures, all 20 entities. (Proven by execution 2026-9-25; the bundle re-verifies at runtime as a refusal gate.)

**Why 10 entities/domain instead of 5.** Over the old 5-entity vocabularies, unique tuples still left entity-set overlap predictive (with only 5 entities, any two triples sharing 2 entities give the oracle a strong signal). Expanding to 10 entities/domain with 3 occurrences each dilutes entity-set overlap to chance (proven in §8).

---

## §3. Statistic: 1-NN leave-one-out target-entity classification

For each layer l ∈ {0,…,23}:
1. Extract final-token hidden state h_l(i) for each bench item i (60 forward passes, all layers in one pass each).
2. Leave-one-out 1-NN: for each i, find j≠i minimizing ‖h_l(i) − h_l(j)‖₂; predict target entity of j. (Euclidean on raw hidden states; no normalization — matches the "raw geometry" framing of the boundary claim.)
3. Accuracy a_l = fraction correct (K=20 labels; chance = 0.05).

**Ties**: Euclidean distances on float32 hidden states tie with probability ~0; the bundle asserts zero ties and RUN-INVALIDs otherwise (same rule as EXP091).

---

## §4. Null: stratified permutation, Bonferroni 0.05/24

- **Strata**: (domain × phrasing): (planetary, A-first)=16, (planetary, C-first)=14, (elemental, A-first)=14, (elemental, C-first)=16. Labels permuted **within** strata only.
- **B = 1,000** permutations per layer (matches v1; the oracle proof in §8 used 10,000 — the bundle uses 1,000 for the real statistic, 10,000 for the oracle diagnostic).
- Per layer: p_l = (1 + #{b: a_l^{(b)} ≥ a_l}) / (1 + B); q95_l = 95th percentile of the permutation distribution.
- **Family-wise**: Bonferroni α_B = 0.05/24 ≈ 0.002083.

---

## §5. Decision tree (TOTAL — all branches reachable)

Let S = {l ≠ 20 : p_l < α_B AND (a_l − q95_l) ≥ 0.10}.

- **CONTINUE** (re-target the program): S ≠ ∅. The readout/injection program moves to l* = argmax_{l∈S}(a_l − q95_l). Licensed claim: "frozen Pythia-410m layer l* carries significant task information (1-NN LOO, Bonferroni-significant, ≥10pp above null q95) on the EXP092-B bench."
- **KILL** (the information is absent, not misplaced): S = ∅ AND no layer has p_l < α_B. Licensed claim: "no Pythia-410m layer carries Bonferroni-significant task information on EXP092-B; EXP091's null generalizes across all 24 layers." Program consequence: the output-side room as an autonomous-mechanism program stands down; bridge positives revert to construction-artifact interpretation (LOG-204).
- **PIVOT** (ambiguous — neither clean signal nor clean null): S = ∅ BUT ∃ l with p_l < α_B and (a_l − q95_l) < 0.10 (significant but sub-threshold), OR only layer 20 is significant. Licensed claim: "weak/sub-threshold signal; insufficient for re-targeting." Program consequence: no re-targeting; the weak layer may be nominated for a powered follow-up (new experiment number, not a silent scope change).

**The 10pp bar is load-bearing**: it prevents Bonferroni-significant but practically meaningless deviations (e.g., 7% vs 5% chance with n=60) from re-targeting the program.

---

## §6. Guards and refusal gates

- **G0 (new-bench provenance)**: bundle asserts bench SHA-256 = `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4` computed over the registered canonical serialization (§2); 60/60 unique `(domain, tuple)` keys; 20/20 targets at exactly 3 occurrences/domain; 30/30 A-first/C-first; strata match the §4 table. Else RUN-INVALID. (The v2.0 pin `2996ac8b…3ac3e` is retired — it was not reproducible from the registered spec; see §0 v2.1 changelog.)
- **G1 (Δθ=0)**: state_dict SHA-256 (sorted keys, float32 bytes — the EXP077/EXP091 `compute_state_dict_hash` procedure) must equal the LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`, checked pre- AND post-extraction. **Weights-integrity note (RESOLVED 2026-09-25):** the weights were relocated from `experiments/runs/EXP086_amplifier/weights/pythia-410m/` to `/home/hatch/workspace/.exp086_weights/pythia-410m/` (repo hygiene). A same-day recomputation initially failed to reproduce the LOG-331 pin — the v2.0 drafter had hashed the raw safetensors file (364 tensors incl. non-persistent buffers) instead of the loaded model's `state_dict` (292 tensors). The parallel integrity investigation (LOG-4321) reproduced the pin **exactly** from the relocated snapshot using EXP091's hash procedure verbatim: the snapshot is byte-intact, no integrity incident. The Law #14 v2 review (§4) ruled the draft's fail-safe posture correct and the caveat resolved. G1 (hash of the loaded `state_dict`) will reproduce the pin at runtime; on mismatch the bundle MUST RUN-INVALID, not proceed.
- **G1′ (tokenizer)**: real-tokenizer offset-mapping cover check over all 60 prompts; all A/C occurrences must be single-token in-prompt. Else RUN-INVALID. (Pre-verified 240/240.)
- **G2 (null calibration)**: the bundle runs the §8 entity-set oracle diagnostic (10,000 stratified perms) on the registered bench at build time; asserts oracle p ≥ 0.05 (oracle NOT significant). If the oracle is significant, the bench is confounded → RUN-INVALID (do not silently "fix" the bench; re-register). Reference implementation pinned: `experiments/runs/EXP092_ibl/reference_implementation.py` (`oracle_expected_accuracy()` — analytic expected-accuracy tie-break, deterministic; `stratified_permutation_p()` — `random.Random(9207 + b)` per permutation b; `g2_diagnostic()`). Reference values: oracle = 0.0607, p = 0.5312 (B=10,000, seed 9207) → gate PASS.
- **G3 (mode stamp)**: `mode` ∈ {mock, real} stamped on every artifact; mock results are never verdicts.
- **G4 (instrument responsiveness)**: the bundle computes the G4 spread diagnostic (same as EXP091: spread of the statistic under the null); if the instrument is degenerate (zero spread), RUN-INVALID.

---

## §7. Secondary statistics (S1, S2 — pre-registered, non-binding)

- **S1 (KSG kNN-MI after PCA ≤20 dims)**: secondary mutual-information estimate, same bench. The n=60 sample-size limitation is declared; S1 cannot override the primary 1-NN verdict.
- **S2 (LM log-prob baseline)** [mandated by the 2026-09-25 summit, §6 "Required controls"]: p(option | premise) from the frozen model's own next-token distribution on the 60-item bench. If S2 is at chance, the bench is genuinely hard; if above chance, the geometry program was looking in the wrong place. $0 CPU. Pre-registered here so it cannot be added silently later.

---

## §8. Confound proof: the entity-set oracle is at chance (kills the v1 defect)

**Oracle definition** (the exact confound the Law #14 review named): leave-one-out 1-NN where similarity(i,j) = |premise-entities(i) ∩ premise-entities(j)| (max overlap); ties broken uniformly at random — computed as **analytic expected accuracy** (for each i, the fraction of max-overlap neighbors sharing i's label, averaged; deterministic, no RNG); label = target entity of the nearest neighbor. Pinned in `experiments/runs/EXP092_ibl/reference_implementation.py` (`oracle_expected_accuracy()`).

**Result on the registered EXP092-B bench** (reference implementation, deterministic):
- Oracle accuracy = **0.0607** (6.07%) — vs 5% chance for K=20.
- Stratified permutation null (10,000 perms, same strata as §4, `random.Random(9207 + b)` per permutation b): **p = 0.5312**. NOT significant. (The v2.0 draft reported p = 0.567 from an unpinned implementation; the reference value 0.5312 supersedes it. Both ≫ 0.05; the calibration conclusion is unchanged.)

**Interpretation.** The entity-set oracle — the strongest non-relational shortcut the review identified — is statistically indistinguishable from its permutation null on this bench. The v1 structural advantage (60/60 oracle accuracy under deterministic tie-break on the old bench, where 50/60 items shared entity sets) is gone. Therefore:
1. The §4 permutation null **validly calibrates** the entity-set confound: any Bonferroni-significant real-embedding result cannot be attributed to entity-set encoding.
2. The KILL branch is **genuinely reachable**: a null result means absence of signal, not a broken instrument.

**For comparison** (v1 bench, same oracle): 30/60 unique entity sets; 50/60 items with duplicated entity sets; oracle 60/60 under deterministic first-tie. The v1 bench was structurally confounded; the v2 bench is not.

---

## §9. Budget and venue

- **$0 GPU.** CPU-only: 60 forward passes (Pythia-410m, all 24 layers, final-token states) + 24×1,000 permutations + oracle diagnostic. Estimated ~1.5 CPU-hours (same envelope as the summit's IBL costing).
- **Venue**: local CPU (same as EXP091's extraction environment). No Kaggle/Colab needed.

---

## Appendix A. Registered tuple assignment (seed 1022)

Entity indices: Planetary = [Mars=0, Venus=1, Jupiter=2, Saturn=3, Mercury=4, Europa=5, Titan=6, Io=7, Triton=8, Miranda=9]; Elemental = [Iron=0, Gold=1, Silver=2, Bronze=3, Steel=4, Tin=5, Lead=6, Silicon=7, Carbon=8, Crystal=9].

```python
# Seed-1022 deterministic assignment, rejection-sampled for uniqueness.
# Verified: 60/60 unique under (domain, tuple) key; each target exactly 3x/domain.
TRIPLES_PLANET = [
    (1,6,7),(7,5,0),(0,9,6),(8,2,0),(3,7,0),
    (2,5,4),(3,5,4),(2,0,9),(6,0,5),(6,2,7),
    (0,2,1),(5,0,9),(9,7,4),(5,8,2),(4,1,9),
]
QUADS_PLANET = [
    (5,1,4,2),(0,7,5,6),(2,5,4,3),(3,2,9,4),(9,4,2,5),
    (6,2,9,0),(1,4,9,6),(8,7,3,4),(4,3,6,9),(4,1,5,0),
    (7,5,2,6),(7,9,4,8),(8,6,2,3),(9,3,1,6),(1,3,2,5),
]
TRIPLES_ELEMENT = [
    (5,0,2),(9,7,8),(1,8,7),(9,2,8),(3,0,6),
    (2,1,5),(1,3,5),(6,8,4),(8,4,2),(4,5,6),
    (5,7,4),(0,2,6),(8,9,2),(7,4,2),(4,5,1),
]
QUADS_ELEMENT = [
    (6,0,1,7),(4,1,9,2),(3,0,1,8),(0,2,9,5),(9,8,5,6),
    (5,1,2,8),(6,2,0,4),(3,5,1,4),(7,2,6,5),(2,0,3,4),
    (1,0,6,4),(0,6,4,5),(7,2,4,9),(2,5,3,6),(8,1,7,0),
]
```

Prompt construction (identical templates to EXP091): for triple index i in planetary, A-first iff i is even; in elemental, A-first iff i is odd. For quads the same parity rule applies. (FIX 1, v2.1: the v2.0 sentence had the planetary/elemental parity swapped, contradicting §4's strata table and the parenthetical below; corrected and re-verified against the §4 table.) A-first items use "outranks" phrasing, C-first items use "is lower than" phrasing (8 A-first per 15-block in planetary, 7 in elemental → 30/30 total).

## Appendix B. Oracle confound proof (execution record)

Computed 2026-09-25 on the registered bench (reference implementation `experiments/runs/EXP092_ibl/reference_implementation.py`, deterministic):

- Entity-set oracle: leave-one-out 1-NN, similarity = |premise-entities(i) ∩ premise-entities(j)|, analytic expected-accuracy tie-break (deterministic).
- Oracle accuracy: **0.0607** (6.07%).
- Stratified permutation null (10,000 permutations, same domain × phrasing strata as §4, `random.Random(9207 + b)`): **p = 0.5312**.
- Verdict on the diagnostic: oracle NOT significant → null calibrates the confound → G2 gate PASS.

Contrast with the v1 bench (same oracle, deterministic first-tie): 30/60 unique entity sets, 50/60 items with duplicated entity sets, oracle 60/60. The v1 bench was structurally confounded; v2 is not.

## Appendix C. G1′ pre-verification (execution record)

Real-tokenizer (Pythia-410m GPTNeoX) offset-mapping cover check over all 60 v2 prompts, 2026-09-25: **240/240** A/C occurrences single-token in-prompt, 0 failures. Per-entity occurrence counts and token IDs: Mars 16 (13648), Venus 8 (36210), Jupiter 10 (34434), Saturn 10 (38876), Mercury 16 (36091), Europa 12 (19930), Titan 16 (31916), Io 10 (26810), Triton 8 (39776), Miranda 14 (30140), Iron 8 (17826), Gold 8 (7284), Silver 16 (16309), Bronze 6 (49134), Steel 18 (19727), Tin 16 (46487), Lead 16 (12151), Silicon 10 (34413), Carbon 14 (32676), Crystal 8 (29509). The bundle re-verifies G1′ at runtime as a refusal gate.

## Appendix D. Standing-rule compliance (§8 of the campaign charter)

Per the campaign's standing tokenization rule (verify by execution, never assert): the single-token claims in §2/Appendix C were verified by executing the real tokenizer over the actual prompts (Appendix C), not by assertion. The uniqueness claim (§2) was verified by executing the builder (60/60 unique). The oracle claim (§8) was computed, not argued. The weights-integrity caveat (§6 G1) is reported as an unresolved observation, not papered over.

---

*End of EXP092 v2 draft (UNSIGNED). Next: independent Law #14 review.*

