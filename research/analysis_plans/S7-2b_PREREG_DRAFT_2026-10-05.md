# S7-2b Pre-registration — DELTA of the signed S7-2 plan (Triton→Neptune bench swap for GPT-2 BPE portability)

**Status:** SIGNED. Independent Law #14 review returned SIGN-WITH-FIXES (LOG-4921); all three required fixes applied verbatim (documentation/mechanical only — no threshold, bar, decision-logic, or verdict-cell change); re-review not required per the reviewer's binding terms.
**Parent outcome [FACT]:** EXP144 aborted at Step 0 — INCONCLUSIVE (bench non-portable), LOG-4919. G1′ fired: 232/240 in-prompt A/C occurrences single-token under GPT-2 BPE (bar 240/240); the mismatch is confined to ONE entity, Triton (0/8; BPE segments it as `ĠT`+`rit`+`on` — an intrinsic vocabulary fact [OBSERVATION], `exp144_g1prime_mismatch.json`). Zero forwards executed; weights never downloaded. The cross-family question is OPEN — the Gap was untested, not falsified.
**Experiment number:** EXP145 (minted by the CEO at execution authorization, 2026-10-05 — protocol modification = new number per the single-lane fence).
**Cost:** $0. This document is planning only — **zero model forward passes**. The bench derivation it records used string ops + tokenizer encode only.
**Read-only** on all archives, the signed S7-2 plan, and prior run artifacts. The staged EXP144 execution bundle (`experiments/runs/EXP144/`: extract/decode/directions/inject/decision/verdict scripts) is referenced, not rewritten.

---

## §0. The single delta (the only change vs the signed S7-2 plan)

**Change [DEFINITION of this delta]:** in the Planetary vocabulary, replace the entity **"Triton"** with **"Neptune"** (vocab index 8, 1:1 swap). All tuple arrays, the phrasing rule (FIX 1), the option-order rule (FIX 2), and the prompt templates are byte-identical to the committed EXP092 procedure.

**Verification [OBSERVATION]** (derivation script `S7-2b_build_bench_2026-10-05.py`, CPU-only, tokenizer files only — no weights):
- "Neptune" is single-token under GPT-2 BPE: token id **26461** (`ĠNeptune`), via the exact offset-mapping cover logic G1′ used.
- Screened alternatives: single-token — Pluto, Ceres, Ariel (rejected on thematic grounds); multi-token, rejected — Uranus (`ĠUran`+`us`), Eris (`ĠE`+`ris`), Haumea, Makemake, Callisto, Ganymede, Enceladus, Rhea, Dione, Iapetus, Oberon, Umbriel, Charon, Phobos, Deimos, Nereid, Proteus.
- **Why Neptune:** Triton is Neptune's moon — the swap preserves the Planetary domain's astronomical character (Neptune is a major planet alongside Mars/Venus/Jupiter/Saturn/Mercury); no substring collisions with any other entity (word-boundary safe).

**New bench pin [FACT]:** `b9eac3893ddfbc67400a5d2b5cbb694ba81308471caf4a150476227065e56545` (64-hex sha256, registered canonical serialization; character-verified by recompute). Derived from committed pin `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4`. Pinned bench: `research/analysis_plans/S7-2b_BENCH_2026-10-05.json` (60 items); derivation manifest: `S7-2b_BENCH_MANIFEST_2026-10-05.json`.

**Surface-diff audit [OBSERVATION]:** every delta-bench prompt equals the committed-bench prompt with `"Triton"`→`"Neptune"` (asserted item-by-item in the derivation script); 5 of 60 items change surface strings (10 "Triton" occurrences total: 8 as A/C decision slots — the G1′ count — plus 2 as the middle entity B); item ids, tuples, phrasing, and domains are identical. Zero "Triton" occurrences remain.

**Nothing else changes.** §2 gives the section-by-section inheritance audit.

---

## §1. Worth-it gate (Law #15) — delta version

1. **Exact question [HYPOTHESIS]:** Does the Triton→Neptune swap repair bench portability, so the licensed S7-2 cross-family question (does the Decodability Gap replicate in GPT-2-small?) can actually be tested?
2. **Decision it changes:** CONTINUE the GPT-2-small cross-family replication (dispatch execution under a new experiment number) vs ABANDON the cross-family lane as bench-non-portable.
3. **Cheapest test:** $0 CPU — rebuild the bench with the swapped entity and re-fire G1′ (done in this draft's derivation: 240/240, zero forwards). The eventual execution is ≈1k CPU forwards, reusing the staged EXP144 bundle verbatim.
4. **Mathematical license:** the swap is a pure label permutation at fixed vocab indices — all set-overlap structure the oracle depends on is preserved, so the G2 diagnostic reproduces the committed values bit-for-bit (0.0607, p=0.5312) [FACT — verified in derivation]. No re-licensing of the decode/injection math is needed; those arms are entity-agnostic.
5. **Quantitative prediction:** G1′ on the swapped bench reads 240/240 (confirmed); the execution's Step-0 sequence then proceeds past the point where EXP144 stopped.
6. **Breaking point:** had G1′ still read <240/240 on the swapped bench, this delta would be dead and the cross-family lane would stand down. It reads 240/240 — the breaking point moves to the decode arm's frozen bars (D1/D2, §4).

**Steelman (argued at full strength):** swapping an entity changes the bench, so this is strictly a weaker test of "the same bench" than a clean port — and one could argue the port was doomed by construction (BPE vocabularies differ). Conceded in advance: the verdict is about the *dissociation pattern* in a second family (§6 anti-fabrication fences), never about numeric comparability with Pythia; the swap is documented per-item and the bench is re-pinned, so nothing is silent.

---

## §2. Section-by-section inheritance audit vs the signed S7-2 plan

Every section of the signed S7-2 plan is either inherited verbatim or carries the documented delta. No silent changes.

| S7-2 § | S7-2b status | Notes |
|---|---|---|
| §1 Worth-it gate | **Replaced** by §1 above (delta-scoped) | The parent gate's question/decision/bars are unchanged and re-enter at execution |
| §2 Background & licensed scope | **Inherited verbatim**, plus: EXP144 INCONCLUSIVE (LOG-4919) is now a licensed [FACT] in the background; licensed scope extends to the single documented entity swap | Backlog row S7-2 unchanged; the swap is the minimal port repair |
| §3.1 Model & environment pins | **Inherited verbatim** | `gpt2` @ `607a30d783dfa663caf39e06633721c8d4cfcd7e`; Δθ=0; seeds; thread pin |
| §3.2 Bench construction | **Delta** (§0 + §3 below) | Committed EXP092 builder + Neptune swap; new pin `b9eac389…e56545`; G1′ re-fires at Step 0 |
| §3.3 Decode arm | **Inherited verbatim** | 60-forward scan, LOO 1-NN K=20, B=1,000 stratified perms (seed `20261007`), Bonferroni 0.05/12, effect bar 0.10, D1/D2 gates, shared-direction construction |
| §3.4 Intervention arm | **Inherited verbatim** | `transformer.h[l*]` tap, α = 0.047 × mean‖h‖ with 0.047±0.01 assert, G5 hook verification, 3×60 decision loop, G4 delivery |
| §3.5 Forward budget | **Inherited verbatim** | ≤1,000 CPU forwards, $0 |
| §3.6 Step-0 aborts | **Pin updated** to `b9eac389…e56545`; bench source changed from procedural rebuild to pinned-JSON load (S5-INV precedent) — see §7; G1′ still re-fires live at Step 0 | S0.1 now pins `b9eac389…e56545` + G1′ 240/240 (re-verified live at execution) |
| §4 Decision table | **Inherited verbatim** | decode+/steer− → CONTINUE; decode+/steer+ → KILL (+PIVOT paper scope); decode− → KILL/PIVOT with bench-fit caveat; anomalous cell → fresh Law-#15 packet |
| §5 Falsification self-check | **Inherited verbatim** | |
| §6 Anti-fabrication guardrails | **Inherited verbatim** | No shared numeric axes; Pythia numbers as prior [OBSERVATION]s only; incommensurability; banned terms |
| §7 Deviations | **Inherited verbatim** + D6 | D6 (new): Triton→Neptune entity swap — forced by GPT-2 BPE tokenization (intrinsic vocabulary fact); documented per-item, bench re-pinned; no silent substitution |
| §8 LOG-218 belief-change | **Inherited verbatim** | "The Decodability Gap is a transformer-general boundary law" [CONJECTURE] |
| §9 Epistemological labeling | **Inherited verbatim** + §6 below | |

---

## §3. New-bench construction & verification record (CPU-only; already executed as planning work)

1. **Procedure [FACT]:** `S7-2b_build_bench_2026-10-05.py` replicates the committed EXP092 `build_bench()` verbatim (read-only import of `reference_implementation`; tuple arrays, FIX 1/FIX 2, templates unchanged) with the single documented vocab delta (PLANET_VOCAB[8]: "Triton"→"Neptune"). No model weights were touched; only the cached GPT-2 tokenizer files were read (revision `607a30d783dfa663caf39e06633721c8d4cfcd7e`).
2. **New bench pin [FACT]:** `b9eac3893ddfbc67400a5d2b5cbb694ba81308471caf4a150476227065e56545` — character-verified by independent recompute from the written JSON.
3. **G0 (bench provenance) [OBSERVATION]:** PASS via the committed `verify_g0` (reads bench items only): 60 items, 60/60 unique (domain, tuple), strata {(Planetary,A-first):16, (Planetary,C-first):14, (Elemental,A-first):14, (Elemental,C-first):16}.
4. **G1′ re-fire (derivation-time) [OBSERVATION]:** 240/240 in-prompt A/C occurrences single-token under GPT-2 BPE (bar 240/240) — the gate that killed EXP144 now passes. Neptune: token id 26461 in all occurrences. Failing entities: none.
5. **Balance check [OBSERVATION]:** 60 items; 20 entities × 3 as target (Neptune appears exactly 3× where Triton did — the swap preserves target balance by construction); phrasing 30/30 A-first/C-first. Documented in the derivation manifest.
6. **G2 (oracle diagnostic) [OBSERVATION]:** accuracy=0.060715, p=0.531247 — bit-identical to the committed EXP092 diagnostic, as predicted (pure label swap at fixed indices preserves all set-overlap structure). Gate PASS (p ≥ 0.05).

---

## §4. Execution Step-0 (what the eventual execution lane will assert — inherited from S7-2 §3.6, pin updated)

- S0.1: bench 64-hex pin recomputes character-identical to `b9eac3893ddfbc67400a5d2b5cbb694ba81308471caf4a150476227065e56545` **recomputed over the loaded pinned bench JSON** (`S7-2b_BENCH_2026-10-05.json`); **G1′ re-fires live on the new bench and must read 240/240** before any weight access — else INCONCLUSIVE (bench non-portable), never a verdict.
- S0.1a: at execution Step 0, re-run the committed derivation procedure (`build_bench_s72b()` + `ref.bench_sha256` from `S7-2b_build_bench_2026-10-05.py`, not the artifact-writing `main()`) and require its pin to equal the loaded JSON's pin; any mismatch → RUN-INVALID.
- S0.2: model 40-hex revision hash matches `607a30d783dfa663caf39e06633721c8d4cfcd7e` (resolved programmatically, never transcribed); G1 pre-hash recorded.
- S0.3: per-layer embedding std > 0 for all 12 layers (degeneracy pre-check).
- S0.4: G4 null-spread non-zero at every layer; r_i norms > 1e-9 in the direction build.
- S0.5: >10% missing/NaN in any arm → INCONCLUSIVE.

Any failure → RUN-INVALID/INCONCLUSIVE, never a verdict (single-lane fence: no self-repair).

---

## §5. Frozen bars (restated for review self-containment; inherited verbatim from S7-2 §3.3/§3.4/§4)

- **decode+** ≡ (D1) ≥1 layer p < 0.05/12 with (acc−q95) ≥ 0.10 **and** (D2) mean shared-direction cosine ≥ 0.70.
- **steer+** ≡ ≥6 decision flips **and** McNemar p < 0.05; **steer−** ≡ <6 flips and McNemar n.s.; ΔM ≥ 10pp registered secondary.
- Four-cell table: decode+/steer− → **CONTINUE** (gap replicates cross-family); decode+/steer+ → **KILL** generality (+**PIVOT** paper to Pythia/GPT-NeoX scope); decode− → **KILL/PIVOT** with the bench-fit caveat (§1 steelman); steer+ without decode+ → **anomalous**, fresh Law-#15 packet, not a verdict on the gap.
- Post-hoc re-barring is forbidden by Law #9.

---

## §6. Epistemological labeling note

Per `AGENTS.md` §5: all [FACT]/[DEFINITION]/[HYPOTHESIS]/[CONJECTURE]/[ASSUMPTION]/[OBSERVATION]/[INTERPRETATION] tags above are load-bearing. The swap's portability claim ("Neptune is single-token under GPT-2 BPE") is an [OBSERVATION] (tokenizer measurement, derivation-time and re-verified live at Step 0); "the swap preserves bench validity" is an [INTERPRETATION] licensed by G0/G1′/G2 passing; the cross-family generality claim remains a [CONJECTURE] until the §5 table fires. Future measured numbers (per-layer accuracies, cosine, flips, McNemar p) will be [OBSERVATION]s; the §5 table's readings are [INTERPRETATION]s licensed only by the frozen bars.

---

## §7. Execution licensing note

- The eventual execution mints a **NEW experiment number** (protocol modification = new number, per the single-lane fence) — not minted in this draft.
- The staged EXP144 bundle (`experiments/runs/EXP144/exp144_{extract,decode,directions,inject,decision,verdict,common}.py`) is reused **verbatim**; the only execution-side change is loading the S7-2b pinned bench (`S7-2b_BENCH_2026-10-05.json`) with the S0.1 pin assert, instead of the committed EXP092 builder output. No script rewrites.
- G2 at execution: the derivation-time diagnostic (bit-identical to committed) is recorded; the execution lane re-binds the artifact to the new pin per S0.1.
