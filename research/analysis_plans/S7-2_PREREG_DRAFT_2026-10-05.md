# S7-2 Pre-registration — Cross-family replication of the Decodability Gap (GPT-2-small)

**Status:** DRAFT for independent Law #14 review. Born at the Monday idea session, LOG-4911 (2026-10-05).
**No experiment number minted** (the CEO assigns numbers; this plan mints none).
**Cost:** $0. This document is planning only — **zero new model forward passes**. The validation run it specifies is a CPU pilot (≈240–1,000 forwards); its execution needs its own lane authorization and will mint its experiment number then.
**Read-only** on all archives, signed protocols, and prior run artifacts.

---

## §1. Worth-it gate (Law #15)

1. **Exact question [HYPOTHESIS]:** Does the Decodability Gap — high-cosine decodability with zero causal transfer — replicate in a non-Pythia architecture (GPT-2-small), or is it a Pythia/GPT-NeoX artifact?
2. **Decision it changes:** KILL / CONTINUE / PIVOT the **generality** of the paper's headline boundary claim (C2: raw cosine ≈0.70 with zero detectable causal transfer). Downstream: the paper's generality language — "transformer-general boundary law" vs "Pythia/GPT-NeoX observation."
3. **Cheapest test:** $0 CPU — copy the licensed EXP092 decode protocol + EXP093 injection protocol onto GPT-2-small (≈240–1,000 forwards; decode scan 60, intervention 180, guards/spot-checks the remainder).
4. **Mathematical license:** the readout-misalignment account (G1's death [OBSERVATION]) predicts architecture-independence **only if** misalignment is transformer-general [CONJECTURE]. The LOO maximum-average-cosine construction is non-degenerate by the registered v0.2 proof: per-item normalization breaks the zero-sum that made v0.1 identically zero [FACT — `direction_builder.py` docstring, EXP093 bundle].
5. **Quantitative prediction:** if the gap is transformer-general, GPT-2-small shows ≥1 layer with Bonferroni-significant 1-NN decode **and** shared-direction mean cosine ≥ 0.70, **and** injection of that direction moves <6 decisions (McNemar n.s.).
6. **Breaking point:** GPT-2's sequential blocks vs GPT-NeoX parallel residuals, 3× smaller scale (124M vs 410M), and different tokenization may break either the decode or the dissociation — ΔM > 0 or decode ≈ chance. Any of these falsifies-or-bounds the generality claim per the §4 table.

**Steelman (argued at full strength):** GPT-2-small is 3× smaller with different tokenization — a decodability difference may reflect scale/bench-fit, not architecture; and one model doesn't make a law either way. Conceded in advance: decode− outcomes carry the bench-fit caveat explicitly (§4, §5); a single cross-family point upgrades "one family" to "two families," not to a law.

---

## §2. Background and licensed scope

**[FACT]** EXP092 (Pythia-410m, 24 layers, d=1024): per-layer LOO 1-NN (K=20, chance=0.05, B=1,000 stratified perms, Bonferroni α=0.05/24) found 10 layers significant {0,1,2,11,12,13,14,15,17,18}; l*=11 at 20/60=33.33%, p=0.000999, effect +20pp. Verdict: CONTINUE.

**[FACT]** EXP093 re-run (Pythia-410m): injection of the LOO maximum-average-cosine shared correction at layer 11 (α=1.0, perturbation 4.7% of residual norm, 3 conditions × 60 items) moved **zero** decisions: ΔM=0, McNemar b=c=0, p=1.0, 0 flips across all strata. Verdict: KILL (the shared-direction causal-transfer hypothesis at layer 11).

**[FACT]** The paper's C2 boundary claim: contrast directions with raw cosine +0.7186/+0.6852 produced zero decision flips under static injection at both tested scales.

**[DEFINITION]** The *Decodability Gap* for this plan: a decodable direction (mean cosine ≥ 0.70 with per-item LOO corrections, **and** Bonferroni-significant 1-NN layer decode) that is causally inert under matched injection (<6 decision flips, McNemar n.s.).

**Licensed scope [FACT]:** LOG-4911 / backlog S7-2 row — "copy the licensed EXP092 decode protocol + EXP093 injection protocol exactly onto GPT-2-small"; kill criterion: "GPT-2-small fails the 0.7-cosine decode bar, OR its decodable direction moves decisions (≥6 flips, McNemar p<0.05) → KILL/PIVOT the generality claim"; ≈1k forwards CPU, $0.

---

## §3. Protocol

### 3.1 Model and environment pins

- **Model:** HuggingFace `gpt2` (GPT-2-small, 124M parameters, 12 layers, d=768) [FACT — public model card].
- **Revision pin:** the executor records the full 40-hex commit hash of the `gpt2` revision at download time (one-time ≈548MB fetch, $0); **Step 0 asserts the local hash character-by-character against the recorded value** (S7-3 lesson: never trust a transcribed pin).
- **Weights:** read-only throughout; `model.eval()` + `requires_grad_(False)`; all forwards under `torch.no_grad()`; Δθ=0 asserted by pre/post state-dict hash (G1).
- **Determinism:** threads pinned (2, per EXP093 precedent); seeds pinned and recorded. Pre-registered: stratified-permutation seed `20261007` for the decode-arm nulls; direction-build and decision loop are seed-free given fixed inputs (seeds recorded in the run manifest).; numpy/torch/scipy/transformers versions recorded in the run manifest.

### 3.2 Bench construction (port of the EXP092 bench-builder procedure)

The bench is defined **procedurally**, not by byte-identical items: re-execute the committed EXP092 bench-builder procedure with GPT-2's tokenizer.

- **Structure [ASSUMPTION]:** 60 items, 60/60 unique (domain, tuple), 20 target entities, 30/30 A-first/C-first phrasing balance, same domains as the EXP092 bench.
- **G0 (bench provenance):** new bench pin (full 64-hex sha256) recorded; 60/60 uniqueness; strata match; phrasing 30/30 — else RUN-INVALID.
- **G1′ (tokenizer cover — the EXP090 lesson):** all 240 in-prompt A/C entity occurrences must be single-token under GPT-2's BPE tokenizer (offset-mapping check, never bare-word), **before any weight access** — else RUN-INVALID. No silent entity substitution: if the ported builder cannot satisfy G1′, the run is INCONCLUSIVE (bench non-portable), with the tokenization mismatch documented.
- **G2 (oracle diagnostic):** entity-set oracle at chance on the rebuilt bench (bench-pin-bound) — else RUN-INVALID.
- **Deviations from the Pythia bench** (entity substitutions forced by BPE tokenization, if any) are listed per-item in the run report with the G1′ evidence.

### 3.3 Decode arm (EXP092 protocol, adapted)

1. **Embedding extraction:** one forward pass per item (60 total); capture final-token residual states at all 12 layers → array (12, 60, 768). Assert per-layer std > 0 (degeneracy pre-check — S7-3 lesson) and no NaN/Inf.
2. **1-NN scan:** per-layer LOO 1-NN (K=20), chance = 0.05, B=1,000 **stratified** permutations (stratify on phrasing — the O1 caveat), Bonferroni α = 0.05/12 ≈ 0.004167, effect bar (acc − q95) ≥ 0.10.
3. **G4 (null-spread):** every layer's permutation null must have non-zero spread — else the instrument is deaf at that layer (RUN-INVALID for that layer's reading).
4. **l\*** = argmax (acc − q95) over layers passing both bars; if none pass, decode = − (skip to §4 table).
5. **Shared direction:** verbatim port of the committed EXP093 `direction_builder.py` (numpy-only, read-only on the embeddings): LOO maximum-average-cosine construction at l\* — r_i = c^(−i)(i) − h(i) with ‖r_i‖ > 1e-9 asserted (else RUN-INVALID), u_i = r_i/‖r_i‖, v^(−i) = normalize(mean_{j≠i} u_j). Record **mean_i cos(v^(−i), u_i)** — the achieved average cosine.
6. **Decode gates (both pre-registered, both required for decode+):**
   - (D1) ≥1 layer with p < 0.05/12 **and** (acc − q95) ≥ 0.10;
   - (D2) mean_i cos(v^(−i), u_i) ≥ **0.70** (the paper's C2 bar).

### 3.4 Intervention arm (EXP093 protocol, adapted)

Executed **only if decode+** (else the §4 table short-circuits; no injection without a decodable direction).

1. **Hook point:** output of GPT-2 block `transformer.h[l*]` at the final token position (the sequential-block analogue of the NeoX `gpt_neox.layers[11]` tap — see §7 deviation D4).
2. **Direction:** the shared LOO maximum-average-cosine direction (full-sample v = normalize(mean_i u_i); LOO variants v^(−i) used per-item exactly as the ported `inject.py` specifies — no item-i leakage).
3. **Scale calibration (pre-registered):** α chosen so the perturbation ratio ‖αv‖/‖residual‖ = **0.047 ± 0.01**, computed from clean-run residual norms at l\* **before** the decision loop (matches EXP093's delivered 4.7%; absolute α is meaningless across d=768 vs d=1024). Aggregation pinned: α = 0.047 × mean_i‖h_i‖, where ‖h_i‖ are the 60 clean-run final-token residual norms at l\*; assert the achieved ‖αv‖/mean_i‖h_i‖ ∈ 0.047 ± 0.01, else recalibrate once or declare INCONCLUSIVE.
4. **G5 (injection-site verification — the EXP093 RUN-INVALID lesson):** re-verify on the real model with correct hook ordering (capture registered **after** the injection hook): (i) hooked final-position residual == clean + αv within rel ≤ 1e-6; (ii) hook-disabled logits bit-match hook-free reference; (iii) max-abs deviation sane. **Any G5 failure → RUN-INVALID** (withheld, never a verdict).
5. **Decision loop:** 3 conditions (B/P/N) × 60 items = **180 forward passes**; record per-item decisions, margins, and the flip ledger.
6. **G4 delivery:** injection reaches the logits (margin movement on a pre-registered fraction of items at tol 1e-4, mirroring EXP093's 36/60) — perturbation real, else the null is a measurement failure (INCONCLUSIVE).

### 3.5 Forward budget

60 (decode scan) + 180 (intervention) + guards/spot-checks ≤ **1,000 CPU forwards total**. $0.

### 3.6 Step-0 abort conditions (all pre-registered; any failure → RUN-INVALID/INCONCLUSIVE, never a verdict)

- S0.1: bench 64-hex pin recomputes character-identical; G1′ 240/240 single-token cover under GPT-2 BPE.
- S0.2: model 40-hex revision hash matches the recorded pin; G1 pre-hash recorded.
- S0.3: per-layer embedding std > 0 for all 12 layers (degeneracy pre-check).
- S0.4: G4 null-spread non-zero at every layer; r_i norms > 1e-9 in the direction build.
- S0.5: >10% missing/NaN in any arm → INCONCLUSIVE.

---

## §4. Decision table (frozen before any forward pass)

**decode+** ≡ (D1) ≥1 layer p < 0.05/12 with (acc−q95) ≥ 0.10 **and** (D2) mean shared-direction cosine ≥ 0.70.
**steer+** ≡ ≥6 decision flips **and** McNemar p < 0.05 (the licensed backlog bar).
**steer−** ≡ <6 flips and McNemar n.s.; **ΔM ≥ 10pp** is a registered secondary (EXP093's delta_bar).

|  | steer− | steer+ |
|---|---|---|
| **decode+** | **CONTINUE** — the Decodability Gap replicates cross-family. Generality supported; licenses "two-family" generality language for the paper. | **KILL** — generality falsified as a boundary law: the decodable direction is causal in GPT-2-small. **PIVOT** the paper's claim to Pythia/GPT-NeoX scope. |
| **decode−** | **KILL/PIVOT** the generality claim (licensed kill criterion) — **with the recorded caveat:** the gap's precondition (decodability) is absent here; this outcome cannot separate an architecture effect from scale/bench-fit (the §1 steelman). | **PIVOT (anomalous)** — steering without decodability is outside the licensed verdicts; triggers a fresh Law-#15 packet for mechanism investigation. Not a verdict on the gap. |

No other reading is licensed. Post-hoc re-barring (e.g., "cosine 0.65 is close enough") is forbidden by Law #9.

---

## §5. Falsification self-check

- **What refutes the Gap as a general phenomenon:** decode+ with steer+ — a decodable direction (≥0.7 cosine) that moves decisions in GPT-2-small. The dissociation fails where its precondition holds; the boundary law does not generalize.
- **What merely bounds it to Pythia:** decode− (either cell) — the precondition fails, so the experiment tests nothing about the dissociation itself; consistent with a Pythia/GPT-NeoX-scoped claim, a scale effect, or a bench-port failure. The KILL/PIVOT verdict fires on the *generality* claim either way, but the mechanism is unresolved.
- **What would embarrass this plan:** a decode+ / steer− outcome driven entirely by the A-first phrasing stratum (the O1 caveat) — mitigated by stratified permutations and a pre-registered stratum breakdown in the report (not a verdict input).

---

## §6. Anti-fabrication guardrails (paper presentation fences)

1. **No shared numeric axis** between Pythia-410m results and GPT-2-small results in any future figure or table — separate panels, separate scales.
2. Pythia numbers (33.33%, ΔM=0, +0.7186/+0.6852) appear only as **prior [OBSERVATION]s**, never as a comparison baseline; no "replicates/beats/underperforms" language across models.
3. Tasks, models, and metrics are described as **incommensurable where they are**: different tokenizers, depths, widths, scales — the verdict is about the *dissociation pattern*, not a numeric horse race.
4. Banned across all new content: `SOTA`, `outperforms`, `competitive`, `validates`, `ranked`, `roadmap` (standing fence).

---

## §7. Deviations from the Pythia protocol (per-deviation justification)

- **D1 — Tokenizer (NeoX → GPT-2 BPE):** unavoidable; the bench is rebuilt procedurally and G1′ re-fires under the real tokenizer (EXP090 lesson). Justification: G1′ is a validity gate, not a cosmetic choice.
- **D2 — Layer count (24 → 12):** Bonferroni denominator becomes 12 (α≈0.004167). Justification: the correction must match the actual number of tests; using 24 would be anti-conservative.
- **D3 — Residual width (1024 → 768):** injection scale matched by **perturbation ratio** (0.047 ± 0.01), not absolute α. Justification: causal comparability requires matched relative perturbation; absolute α is meaningless across widths.
- **D4 — Block structure (parallel → sequential):** hook point moved to `transformer.h[l*]` output; G5 re-verified on the real model with correct hook ordering (EXP093 RUN-INVALID lesson). Justification: the tap must sit on the residual stream; the module path is architecture-specific.
- **D5 — Scale (410M → 124M):** recorded as a confound, not controlled. Justification: no smaller Pythia with the same bench exists in the program's $0 lane; the steelman caveat (§1, §5) carries it.

---

## §8. LOG-218 belief-change statement

**Belief [CONJECTURE]:** "The Decodability Gap is a transformer-general boundary law."
**Overturning observation:** in GPT-2-small, either nothing is decodable at the 0.7-cosine bar (generality KILL/PIVOT with bench-fit caveat), or the decodable direction moves decisions (generality KILL outright).
**Confirming observation:** decode+ with steer− — the dissociation holds in a second family.

---

## §9. Epistemological labeling note

Per `AGENTS.md` §5: all [FACT]/[DEFINITION]/[HYPOTHESIS]/[CONJECTURE]/[ASSUMPTION]/[OBSERVATION]/[INTERPRETATION] tags above are load-bearing. Future measured numbers (per-layer accuracies, cosine, flips, McNemar p) are [OBSERVATION]s; the §4 table's readings are [INTERPRETATION]s licensed only by the frozen bars. The S7-3 lessons are applied: §3.6 degeneracy pre-checks ("can this vary across items in principle?") and character-by-character pin verification (S0.1, S0.2).
