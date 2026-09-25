# Independent Law #14 Verdict Review — EXP092 (IBL) Real Execution

**Reviewer:** Independent Scientific Mentor / Law #14 Reviewer (reports directly to the founder; binding)
**Date:** 2026-09-25
**Target:** EXP092 (Information-Bottleneck Localization) real-execution verdict — **CONTINUE** — reported at LOG-4336
**Run report:** `experiments/runs/EXP092_ibl/EXP092_RUN_REPORT_2026-09-25.md`
**Signed protocol:** `experiments/protocols/EXP092_IBL_PREREG_SIGNED.md` (SHA-256 `75e744ad9bae98cc86c0443823bd27b197a9c17fc106ba984e5870cf1bdb347c` — recomputed by reviewer, matches)
**CEO clearance:** LOG-4332 (Nova) — verified present, names the exact executed command, CPU-only scope
**Launch chain verified:** signed (LOG-4325) → bundle build (LOG-4328) → bundle SIGN (LOG-4331) → CEO clearance (LOG-4332) → execution (LOG-4336). Complete, in order.

---

## BINDING VERDICT: ADOPT-WITH-CORRECTIONS

The reported **CONTINUE** is **ADOPTED** as a licensed program result. Every number in the verdict chain was independently recomputed from the primary artifacts (`.npz` embeddings, extraction log/meta, scorer report) using reviewer-written code that does not import the bundle — agreement is **exact** (max |Δ| = 0.00e+00 on accuracies and p-values across all 24 layers). The §5 TOTAL decision tree was applied correctly. All guards fired-and-passed in the registered order. Δθ=0 holds.

Two corrections are binding (C1, C2) and one interpretive caveat is recorded (O1). None alters the verdict, the S set, l*, or the licensed claim — they constrain documentation, future methodology, and the scope of the "redirect to l*=11" consequence.

**Licensed claim (adopted, per §5):** "Frozen Pythia-410m layer 11 carries significant task information (1-NN LOO, Bonferroni-significant, ≥10pp above null q95) on the EXP092-B bench." Novelty remains N1. No capability, superhuman, conscious, or autonomous claim is licensed.

---

## 1. Independent recomputation of per-layer statistics — CONFIRMED EXACT

Reviewer wrote `verify.py` from scratch (own LOO 1-NN, own stratified permutation with the registered `random.Random(9207+b)` within-strata scheme, B=1,000; no bundle imports). Results vs `out/exp092_report.json`:

| Check | Result |
|---|---|
| Layer-11 accuracy | 0.3333 (20/60) — confirmed |
| S set | {1, 11, 12, 13, 14, 15, 17, 18} — confirmed, all 8 meet both bars |
| p_11 | 0.000999 = 1/1001 < α_B = 0.0020833 — confirmed |
| Effect (acc − q95) at l=11 | +0.2000 ≥ 0.10 — confirmed |
| Max \|Δ accuracy\| vs reported | 0.00e+00 (all 24 layers) |
| Max \|Δ p\| vs reported | 0.00e+00 (all 24 layers) |
| Layer 20 | acc 0.15, p = 0.0659 — not significant, correctly excluded |
| Embeddings integrity | (24, 60, 1024) float32, no NaN/Inf; 20 labels × 3 each; 4 strata (16/16/14/14); no exact distance ties (tie rule armed, never triggered) |
| S2 baseline | acc 0.60, margin −0.001819 — recomputed, matches |

Sharp-boundary audit: layer 2 (effect +0.0992 < 0.10) and layer 0 (+0.0833) are correctly EXCLUDED from S; layer 15 (effect exactly +0.1000 ≥ 0.10) is correctly INCLUDED. The ≥10pp bar was applied as registered, with no rounding leniency in either direction.

**Decision-tree application (§5):** S = {l ≠ 20 : p_l < α_B ∧ (a_l − q95_l) ≥ 0.10} = {1, 11, 12, 13, 14, 15, 17, 18} ≠ ∅ → **CONTINUE**, l* = argmax effect = layer 11. KILL and PIVOT branches correctly not taken. The verdict follows mechanically from the recomputed numbers.

## 2. Guard audit from the extraction log — ALL FIRED IN ORDER

From `out/exp092_extraction_log.txt` (primary source, not the report's summary):

1. **G0** — bench pin `9be8162633fe19aa…` recomputed; 60/60 unique tuples; strata match §4. Fired first. PASS.
2. **G2** — oracle 0.0607, p = 0.5312 (build-time artifact, pin-bound). Fired before weight access. PASS.
3. **G3** — 30/30 A-first/C-first. Fired before weight access. PASS. *(Labeling note — see C1.)*
4. **G1′** — 240/240 in-prompt A/C occurrences single-token, real tokenizer, offset-mapping check. Log order: tokenizer loaded → G1′ PASS → *then* model loaded. **Before any weight access.** PASS.
5. **Signed-protocol digest** — asserted by `run_exp092.py::assert_signed_protocol()` before extraction (code inspected; digest independently recomputed by reviewer: `75e744ad…` matches). PASS.
6. **G1 pre** — `ec276abe3902fab0…` matches LOG-331 pin. PASS.
7. 60 forward passes.
8. **G1 post** — `ec276abe3902fab0…` identical. **Δθ=0 verified.** PASS.
9. **G4** — null spread 0.20–0.25 per layer (recomputed: all > 0). Instrument responsive. PASS.

No guard fired a refusal; none was skipped or reordered. The `--ceo-clearance` gate (LOG-4329 FIX 1) was satisfied — the executed command carries the flag.

## 3. S1 degeneracy — DIAGNOSIS CONFIRMED, VERDICT UNAFFECTED

The reported bit-identical 4.082639989633465 at all 24 layers is **mathematically inevitable**, not an implementation bug. Reviewer proof:

- Ross mixed estimator: MI = ψ(n) − ⟨ψ(N_y)⟩ + ψ(k) − ⟨ψ(m_i)⟩.
- With k=3 and zero exact distance ties (verified on real data: all m_i = 4), every point's neighbor count m_i = k+1 = 4.
- Labels balanced (verified: all N_y = 3), so ⟨ψ(N_y)⟩ = ψ(3), and the ψ(3) terms cancel exactly.
- Hence MI = ψ(60) − ψ(4) = 4.082639989633465 bits **identically, for any embeddings**. Reviewer recomputed the analytic constant — matches to 15 decimals.

**Consequence:** S1 as specified is vacuous *by construction* in this regime — it cannot discriminate layers regardless of the data. This is stronger than "degenerate here": the degeneracy persists for **any** k whenever distances are all distinct and labels are balanced. S1 is registered non-binding and did not drive the verdict, so the verdict stands — but the estimator must not be reused as specified (see C2).

## 4. Interpretation check — NO OVERCLAIM; SHORTCUT ANALYSIS

**Overclaim audit:** The run report's licensed language is properly scoped — "target-entity identifiability from final-token embeddings," explicitly "not a capability claim," "Novelty remains N1," "No superhuman/conscious/autonomous claim is licensed." The execution agent's own [INTERPRETATION] section honestly flags the relational-vs-mention question as unsettled by this experiment. **No overclaim found.**

**Shortcut scrutiny (reviewer's own analysis, `shortcut_analysis.py`):** Could the layer-11 signal (0.3333) be an entity-mention artifact the G2 oracle missed?

- Neural 1-NN vs oracle predictions agree on only **6.67%** of items; **0 of the 20** neural-correct items are oracle-correct. The neural signal is orthogonal to mention-overlap matching.
- Neural-correct items have *lower* mean mention-overlap with their NN (1.65) than neural-wrong items (1.77) — the opposite of what mention-matching would produce.
- First-mentioned-entity hypothesis tested and rejected: on C-first items (where first-mentioned = foil), the model predicts the foil only 10% vs the target 13.3% — no foil-dominance.
- Correct predictions spread across 11/20 targets (max 3/3 on two targets) — no single-token artifact concentration.

**Finding:** The G2 oracle construction covers the mention-set shortcut space, and the neural signal is demonstrably not mention-set matching. The "misplaced information" reading — target information present at layer 11, absent at layer 20 — survives this scrutiny. What the experiment does *not* settle (and does not claim) is whether the information reflects relational computation vs. a subtler non-relational regularity.

## 5. Δθ=0 — CONFIRMED

Extraction log attests G1 pre = G1 post = `ec276abe3902fab0…`; the guard compares full hashes and RUN-INVALIDs on mismatch — the run completed, so pre = post exactly. The hash procedure (`compute_state_dict_hash`: sorted keys, float32 bytes) is the EXP077/EXP091 procedure verbatim, and LOG-4321 already reproduced the full LOG-331 pin from this snapshot. Frozen backbone holds: θ_after = θ_before.

---

## Binding corrections

**C1 — Guard-table labeling drift (documentation).** The run report's guard table lists "G3 phrasing balance," but signed protocol §6 defines **G3 as the mode stamp** and places the 30/30 phrasing assertion under **G0**. Substance is intact (phrasing checked pre-weights; `"mode": "real"` stamped in `exp092_report.json` and the extraction meta), but the labels disagree with the signed protocol. **Required:** append an erratum to the run report mapping the executed checks to the protocol's guard names (G0⊃phrasing, G3=mode stamp). Do not silently edit the signed protocol.

**C2 — S1 estimator vacuous as specified (methodology).** Per §3 above, the Ross kNN-MI as specified (k=3, m_i counting, balanced labels, tie-free continuous embeddings) is a mathematical constant and cannot serve its intended diagnostic role — for any k, not just k=3. **Required:** S1 in its current specification is retired from future pre-registrations. Any successor MI diagnostic must be specified with a degeneracy analysis (unbalanced-label or tie structure, or a different estimator family) and unit-tested against a constant-data null before it is allowed to be informative.

## Recorded observation (not a correction)

**O1 — Phrasing asymmetry of the layer-11 signal.** Reviewer's breakdown: A-first items 16/30 (53.3%), C-first items 4/30 (13.3%). The licensed CONTINUE fires on the registered global statistic and the stratified null already blocks on phrasing, so the verdict is unaffected — but the "redirect the readout program to l*=11" consequence **must carry this caveat**: the information is concentrated in A-first (forward-chaining) phrasing. A layer-11 readout will inherit this phrasing sensitivity. The asymmetry is consistent with answer-computation modulated by reasoning difficulty (cf. S2's 60% output-side lean), not with a positional confound (foil-prediction rejected above) — but that reading is interpretive, not licensed.

---

## Summary for the program record

EXP092's CONTINUE is **adopted**. Independently recomputed from primary artifacts: 8 layers satisfy both registered bars, l* = 11 (acc 0.3333, p = 0.000999, +20pp above null q95), layer 20 correctly excluded, all guards fired in order, Δθ=0, no overclaim. The v1 confound that killed the first design stays dead — the v2 bench's entity-set oracle is at chance and the neural signal is orthogonal to mention matching. Two binding corrections (guard-label erratum; S1 specification retired) and one caveat (phrasing asymmetry) are recorded above. The readout program is licensed to re-target to layer 11, carrying O1's caveat. Cost: $0.

*Reviewer: Independent Law #14 Review Office. This verdict is binding and cannot be overridden or suppressed.*
