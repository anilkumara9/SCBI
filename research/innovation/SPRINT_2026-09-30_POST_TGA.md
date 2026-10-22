# Innovation Sprint — POST-TGA mechanism candidates (2026-09-30)

**Sprint lane:** LOG-4837 (pre-assigned). $0 CPU, proposals only — no execution, no experiment numbers minted, no signed protocol touched, no GPU contact.
**Summit question:** *What discovery would have to be true for a frozen model (Δθ=0) to become far more cognitively capable through inference-time computation?*
**Status:** PROPOSAL DOSSIER — licenses nothing. Every candidate below requires its own signed pre-registration + independent Law #14 review before any execution (launch chain). This dossier is differentiated against SPRINT_2026-09-29_SUMMIT.md (H1–H4, all executed), SPRINT_2026-09-29_SUMMIT_ROUND2.md (H5–H8, all executed), and all verdicts through LOG-4836.

---

## 1. Evidence base (ground truth these candidates are built on)

[OBSERVATION] — all numbers from primary artifacts / the research log:

- **Seven binding KILLs:** EXP107, EXP114, EXP125, EXP126, EXP129, EXP131, EXP133 — all with independent Law #14 SIGN.
- **Both steering branches closed with delivery-verified nulls:** EXP131 — one-shot injection along the dynamics' leading singular direction v̂₁ steers zero decisions (ĉ = 0.03742 < 0.1, ΔM_v1 = 0 over 110 arm-pairs, median ratio 0.5592, McNemar p = 1.0) with (h) r = 1.0000001 and (d2) drift-detector PASS (LOG-4832, binding). EXP133 — geodesic multistep steering along v̂₁ steers zero decisions (ΔM_geo = 0, ĉ_geo = 0.0374, McNemar p = 1.0) with verified delivery (LOG-4818, binding). GEOSTEER retired as a license.
- **The blind-tap lesson:** the program voided its own binding GPU verdict (LOG-4810) when independent review proved the injection hook never reached the readout — then rehabilitated it honestly on CPU (LOG-4832). Delivery verification ((h) positive control) is now a standing breaking-point class.
- **What survives:** EXP127's TGA CONTINUE — the frozen L20→L24 propagator HAS a distinguished leading singular direction (median amplification R = 8.24×) [OBSERVATION] — a dynamics measurement, not steering. EXP111/120/122: trained heads decode domain-set identity at 24–27/30 on three benches — reclassified as domain-set-detector correlations (Law #11, EXP126; observations stand, Law #8). EXP112: 41/60 honesty-decoding HELD, bench-1-specific.
- **The loop's untested link:** E-validity (label-free evaluation of candidate bases) remains conjecture — never tested. EXP129 killed closed-loop adaptive pursuit (median r = 1.000005); EXP070's oracle ceiling is GPU-gated.
- **The program has never seen a positive steering result.** Zero positive autonomous-steering signals (scoreboard v3.11).

## 2. Design constraints (what is dead, what is occupied)

**Do not propose:** single-site residual-stream injection in any variant (static, cone, offset, gated, dose-response, threshold, one-shot TGA, multistep-geodesic TGA — EXP077/093/094/095/096/097/131/133 + S6 wave closed it); closed-loop adaptive pursuit (EXP129); trained-head transfer reading (EXP107) and its identity-readout interpretation (EXP126); logit-level masking operators (EXP105); honesty-instrument third benches / new layers / new carriers (barred per H22 §4); planner/executor generation pilots (EXP109/115/116/117/119 — H11 untested, not killed, but the elicitation apparatus is dead); true-INT8/bitsandbytes-exact (GPU-gated, gate-killed Round 2).
**Occupied by executed sprints (do not duplicate):** H1 (honesty line), H2 (EXP110 precision cert), H3 (EXP106/107), H4 (EXP109), H5 (EXP111), H6 (EXP112), H7 (EXP113), H8 (EXP114 KILL).

---

## 3. The five candidates

Each carries the full worth-it gate: (1) exact question, (2) KILL/CONTINUE/PIVOT decision changed, (3) cheapest test + cost, (4) mathematical license, (5) quantitative prediction, (6) breaking point — plus (7) non-resurrection audit.

---

### B1 — MCI: Multi-site Composition Injection

**Mechanism sketch.** Every killed injection was single-site. Decisions in a transformer are computed distributively across layers — no single site may be sufficient, which is exactly what seven single-site nulls would look like. MCI tests coordinated simultaneous injection at two sites (L11 + L20): if composition is the missing ingredient, the composed arm moves decisions where matched-budget single-site arms move nothing.

**Worth-it gate.**
1. *Exact question:* Does coordinated simultaneous injection at L11+L20 move frozen decisions where matched-total-budget single-site injections at each site move nothing?
2. *Decision changed:* **CONTINUE** the composition axis (→ the program's first positive steering signal; licenses the G/E/S loop's composition premise and GPU-scale multi-site designs) vs **KILL** it (the distributed-computation defense dies; steering is dead at two sites too).
3. *Cheapest test + cost:* 10 prompts × 4 arms (L11-only, L20-only, L11+L20 simultaneous at half-dose each = matched total budget, random-pair control) ≈ 40 injection forwards + (h) delivery check per site, using the repaired executor machinery (prepend=True hook, (h) control). **$0 CPU, ~30 min.**
4. *Mathematical license:* the program's own fencing — EXP094's verdict explicitly left "multi-layer compositions" alive as unlicensed-but-open; distributed-computation theory (no single layer sufficient for the decision); dose-matching makes the composition arm a strict generalization of the killed single-site arms. *Quantitative prediction:* ΔM_composition > 0 with paired McNemar one-sided p ≤ 0.05 vs the best single-site arm; predicted ≥ 2 flips/10 prompts if composition is the missing ingredient.
5. *Breaking point:* ΔM = 0 on the composition arm with (h) PASS at both sites → **KILL** "multi-site composition rescues steering."
6. *Non-resurrection audit:* all killed families are single-site in space (EXP077/093/094 static; EXP131 one-shot TGA; EXP133 multistep TGA). EXP129's kill doesn't transfer — temporal 2-step feedback at one site ≠ simultaneous spatial composition. Law #4 clean.

**Novelty audit.** No multi-site injection in the corpus. N1; N2-adjacent if it continues (first positive steering result in-program).

---

### B2 — EVAL: Label-free E-step Validity (bridge-ranking)

**Mechanism sketch.** The G/E/S loop's E-step — label-free evaluation of candidate bases — has never been tested; it stands as conjecture. The bridge is a measured positive control (+10pp, p = 0.03125, EXP077). If no label-free score can rank the bridge above matched randoms, the loop cannot select — E is dead as designed. If one can, the loop has a live evaluation component.

**Worth-it gate.**
1. *Exact question:* Can any label-free score rank candidate injection directions by causal efficacy — specifically, does it rank the known-positive bridge above 8 matched randoms?
2. *Decision changed:* **CONTINUE** the G/E/S loop's E-step (→ licenses E-guided candidate-selection designs) vs **KILL** it (label-free evaluation is impossible on this bench; the G/E/S architecture needs rethinking).
3. *Cheapest test + cost:* compute 2–3 label-free scores (mean margin gain on the model's own greedy outputs; output consistency; probe-decodability delta) for the bridge + 8 matched randoms on the 60-item bench from archived embeddings/forwards; Spearman rank correlation between score-rank and causal-rank (bridge = 1). **$0 CPU, ~1h, zero new model forwards if embeddings archived.**
4. *Mathematical license:* the G/E/S LOOP_SPEC (E-validity explicitly "conjecture" — untested, not killed); the bridge as a measured positive control; rank statistics need no labels (Law #7 clean — scores from the model's own outputs). *Quantitative prediction:* Spearman ρ ≥ 0.7 between at least one score's ranking and the causal ranking.
5. *Breaking point:* all scores ρ ≤ 0.3 (no ranking signal) → **KILL** "label-free E-step is possible."
6. *Non-resurrection audit:* E-validity was never tested — recorded as conjecture, never as a killed claim. No verdict touches it. Law #4 clean.

**Novelty audit.** No E-validity test in the corpus. N1.

---

### B3 — TGA-DECODE: TGA Channel Decodability

**Mechanism sketch.** EXP131/133 killed *pushing into* the dynamics' maximally-amplified channel (causality). The Decodability Gap's whole point is that causality's null doesn't predict decodability's null. Untested: does v̂₁ (R = 8.24×) *carry* task information — is the amplifier's channel informative even though it's causally inert?

**Worth-it gate.**
1. *Exact question:* Does the TGA leading direction carry task-decodable information (1-NN decode on v̂₁-projected embeddings vs chance)?
2. *Decision changed:* **CONTINUE** the TGA-measurement program (→ the distinguished direction is task-aligned; licenses reading-from-TGA designs) vs **KILL** it (the amplifier is task-orthogonal; the TGA story closes completely — direction exists, carries nothing, moves nothing).
3. *Cheapest test + cost:* project archived frozen embeddings onto v̂₁ (exp127_vectors.npz — archived) → scalar per item; EXP092's licensed decode protocol (1-NN, permutation null, Bonferroni) on the 60-item bench. **$0 CPU, ~15 min, zero new forwards.**
4. *Mathematical license:* EXP127's CONTINUE (v̂₁ real, R = 8.24× [OBSERVATION]); EXP092's decode protocol (licensed, exact bars). *Quantitative prediction:* if task-aligned, 1-NN ≥ 15% vs 5% chance (permutation p < 0.00208); if task-orthogonal (as the injection nulls suggest), ≤ 8%.
5. *Breaking point:* decode ≤ 8% (no signal above the null ceiling) → **KILL** "the TGA channel carries task information."
6. *Non-resurrection audit:* killed claims are injection (causality) along v̂₁; this tests decodability (correlation) — different claim class under the program's central dissociation. Law #4 clean.

**Novelty audit.** No TGA-decode probe in the corpus. N1.

---

### B4 — ARI: Attention-Routing Intervention

**Mechanism sketch.** All killed interventions added content to the residual stream (h' = h + αv) or masked logits (EXP105). None touched the model's information *routing*. The "routing-around" hypothesis: residual perturbations fail because downstream attention re-routes around them — which predicts exactly the observed pattern (delivery verified, decisions unmoved). ARI intervenes on attention weights directly (boost target-token attention / ablate foil-token attention).

**Worth-it gate.**
1. *Exact question:* Does attention reweighting move frozen decisions where residual-content injection moves nothing?
2. *Decision changed:* **CONTINUE** the routing-intervention axis (→ first positive steering signal via a new operator; licenses routing-aware G/E/S designs) vs **KILL** it (routing intervention is dead too; the nulls aren't routable-around).
3. *Cheapest test + cost:* 10 prompts × 3 arms (target-boost, foil-ablate, uniform-reweight control) via attention-weight hooks on frozen Pythia-410m; ΔM + paired McNemar vs base. **$0 CPU, ~30–45 min.**
4. *Mathematical license:* attention as the model's routing mechanism [DEFINITION, transformer theory]; the routing-around hypothesis [HYPOTHESIS] predicts the verified-delivery null pattern. *Quantitative prediction:* target-boost moves ≥ 2/10 decisions (McNemar one-sided p ≤ 0.05 vs uniform control).
5. *Breaking point:* ΔM = 0 on both routing arms → **KILL** "attention-routing intervention steers decisions."
6. *Non-resurrection audit:* no experiment has intervened on attention weights. G1 killed a QK-subspace *theorem* (a claim about where failed directions live), not attention intervention. Different operator class. Law #4 clean.

**Novelty audit.** No attention-weight intervention in the corpus. N1; N2-adjacent if it continues.

---

### B5 — TGA-INT8: Precision Certification of the TGA Nulls

**Mechanism sketch.** EXP110 certified the I2′ battery verdicts under INT8 fake-quantization. The delivery-verified TGA nulls (EXP131/133) were measured at full precision; 2609.06473 shows causal structure can shift under quantization while geometry survives. Certify or precision-index the TGA boundary.

**Worth-it gate.**
1. *Exact question:* Do the TGA decision nulls reproduce under INT8 fake-quantization, or does precision open a transfer window?
2. *Decision changed:* **CERTIFY** the TGA boundary as precision-robust (→ paper generality claim) vs **PIVOT** (precision-indexed boundary; the nulls are regime-specific).
3. *Cheapest test + cost:* fake-quantize Pythia-410m (per-channel symmetric INT8, FP32 compute — the EXP110 certified pattern) + re-run the TGA decision arms (v̂₁ one-shot + geodesic multistep, 10 prompts). **$0 CPU, ~2–4h.**
4. *Mathematical license:* 2609.06473 [OBSERVATION] — causal structure can shift under quantization; EXP110's certified methodology. *Quantitative prediction:* ΔM = 0 on both arms under INT8 (nulls reproduce).
5. *Breaking point:* any decision flip on either arm → **PIVOT** (precision-indexed TGA boundary).
6. *Non-resurrection audit:* EXP110 certified the I2′ battery, not the TGA kills — different verdict family. Differentiated from the gate-killed true-INT8/bitsandbytes-exact (GPU-gated): this is fake-quant, CPU-feasible, the EXP110 pattern. Law #4 clean.

**Novelty audit.** No TGA precision variation in the corpus. N1. Summit filter: honest — boundary infrastructure, not capability.

---

## 4. Ranking (falsifiability-per-dollar × summit relevance)

| Rank | Candidate | Cost | Kill buys | Continue buys |
|---|---|---|---|---|
| **1** | **B1 MCI** | ~0.5h | Kills the distributed-computation defense; steering dead at two sites | **First positive steering signal**; licenses the loop's composition premise |
| **2** | **B2 EVAL** | ~1h | Kills the G/E/S loop's E-step as designed (architecture rethink) | Loop has a live evaluation component; licenses E-guided selection |
| **3** | **B4 ARI** | ~0.75h | Kills routing intervention; nulls aren't routable-around | First positive via a new operator; routing-aware loop designs |
| **4** | **B3 TGA-DECODE** | ~0.25h | Closes the TGA story completely (exists, carries nothing, moves nothing) | Distinguished direction is task-aligned; reading-from-TGA designs |
| **5** | **B5 TGA-INT8** | ~2–4h | — (certification, not a kill) | Precision-robust boundary (paper generality) |

## 5. Rejected darlings

- **Cross-layer TGA decode (multi-layer v̂₁ projection):** subsumed by B3's single-channel test — if the channel carries nothing, its cross-layer version adds no license. Not a standalone bet.
- **Larger-dose TGA injection:** dose escalation fenced by EXP095; the nulls were (h)-verified at matched budget — more dose is the dead escalation path, not a new mechanism.
- **Honesty-instrument third bench / new layer / new carrier:** explicitly barred per H22 §4 (Law #4).
- **G/E/S full-loop pilot:** EXP129 killed the closed-loop premise; a full-loop pilot without E-validity (B2) is unlicensed sequencing — B2 first.
- **Converse-gap search (high-causality, low-decodability directions):** fishing over randoms with no license; the 8-random nulls in EXP131 already price it. Fails the worth-it gate's "cheapest falsifying test" (no cheap distinguishing test exists).

## 6. Recommendation

**Run B1 first.** It is the only bet with first-positive upside at $0 — the program's missing "number that goes up" — and it tests the composition premise at the heart of the G/E/S loop. Both outcomes are decisive: CONTINUE gives the program its first steering signal and validates composition as a mechanism class; KILL retires the last spatial degree of freedom the program's own fencing left open. B2 follows as the architectural question (if E is dead, the loop needs redesign before any composition pilot matters at scale); B4 as the new-operator probe; B3 as the cheapest narrative closure; B5 as certification.

## 7. Session notes

- Summit filter applied: B1 and B4 are capability-positive bets (a frozen model gaining decision capability via inference-time apparatus); B2 is architecture-critical (the loop's untested link); B3 closes the program's flagship measurement story; B5 is boundary infrastructure. No candidate claims consciousness, superhuman achievement, or generality beyond its bench.
- Law #4 audits are explicit per candidate — the September-30 EXP134 refusal (LOG-4834) is the standing warning: sprint dossiers go stale as executions land; every future sprint must diff against the verdict record, not just prior dossiers.
- No experiments executed in this sprint ($0 CPU, proposals only). Next step per candidate: signed pre-registration + independent Law #14 review (launch chain). This dossier is a proposal record, not a license.
- Total proposed spend if all five run: ~5–7 CPU-hours, $0.
