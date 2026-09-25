# EXP088 — Recirculation directional-leak discrimination: pre-registration skeleton (DRAFT)

**Status:** DRAFT, unsigned, pre-Law-#14. A fresh Law #14 review by a different reviewer is required before any runner is built.
**Lane:** Lane 6 frontier intelligence, steal #1 (LOG-293 §H), deep-dive LOG-294.
**Mandate:** discriminate *belief-state feedback* from *generic perturbation / extra compute* as the mechanism behind Recirculation's inference-time gains.
**Primary source:** Mozer, Siddiqui, Sawyer, Sanyal, Liu, "Recirculation," arXiv:2608.17981v1 [cs.LG], 18 Aug 2026. All paper facts below were read from the primary PDF this turn (LOG-294); line references are to the fetched PDF text.
**Laws:** Δθ=0 (Law #6; param hash pre/post); Law #7 (labels at evaluation only); Law #15 (card in §1); no silent level-crossing (L1 endpoint declared in §2).

---

## 1. Law #15 card

1. **Precise question:** Does recirculation's gain on a frozen model come from *deep→shallow belief-state feedback* (the paper's mechanism: a deep layer's contextualized representation enriches a shallow layer's impoverished one), or from *generic perturbation / extra serial compute* (any small activation kick plus a second forward pass)?
2. **Decision:** KILL the belief-state account if deep→shallow leakage does not beat shallow→deep leakage (or matched-norm random-direction leakage) on the primary contrast; CONTINUE to conditional/adaptive variants only if deep→shallow wins with LCI > 0.05; PIVOT to perturbation/compute characterization if recirculation helps but direction doesn't matter.
3. **Cheapest test:** Stage A: (s,d) perplexity screen, 9 pairs × 2 passes on ~50k held-out tokens ≈ 450 block-passes. Stage B: directional discrimination on the fixed N=60 2-hop MCQ probe: 3 α values × 3 leak directions × 2 passes × 60 items = 1080 leak passes + 60 no-recirculation baseline passes = 1,140 passes. Total ≈ 1,590 passes ≈ **0.02 T4-h (~1–2 min)** on the free-T4 lane. (Estimate; GPU-node actuals logged per precedent — CONJECTURE until measured.)
4. **Mathematical license:** §3 (small-α perturbation bound [PROPOSITION], depth-causality information advantage [HYPOTHESIS], ∩-shaped α signature [PREDICTION]). **Quantitative prediction:** ΔM(D→S) − ΔM(S→D) > 0.05 (LCI), one-sided McNemar p ≤ 0.05; per-α gain ∩-shaped (0.15 ≤ 0.10). **Breaking point:** D→S ≤ S→D (no information advantage); or monotone gain in α (perturbation-magnitude account, not belief-state); or α too large → OOD amplification (the paper's own stated risk).

---

## 2. Level and classification (no silent crossing)

- **Endpoint:** decision accuracy on a fixed 2-hop MCQ probe set = **L1 (improves inference)**.
- **Mechanism class:** inference-time architectural modification (externally specified leak + second forward pass) — "inference-time activation control" per LOG-247, never autonomous cognition.
- **Out of scope:** the paper's *adaptive* recirculation (trains an MLP mapping token embeddings → vector-valued α,β). That trains auxiliary parameters; whether an auxiliary mixing module counts as Δθ=0-legal inference apparatus is a **boundary question for the CEO**, default NO — this protocol tests the training-free variant only.

---

## 3. Formalization (Founder's mathematical order)

**Definitions.** Fix frozen model M (Δθ=0) with L layers. D1: h_l(x) ∈ ℝ^d = residual-stream state after layer l. D2: leak operator with source s > destination d and coefficient α ∈ (0,1):
h_d ← α · (‖h_d‖₂/‖h_s‖₂) · h_s + (1−α) · h_d  (paper Eq. 1–2; convex mixture, norm-matched source).
D3: one recirculation iteration = apply D2 at layer d, then run layers d+1..L a second time (two stacks in parallel; readout after the first iteration of a stack — paper Fig. 3c). D4: leak *directions*: D→S (s deep, d shallow — the paper's operator: apply D2 at destination d, then rerun layers d+1..L), S→D (D2 with s↔d swapped: a shallow source's activation leaked upward into the deep destination, rerun span s+1..L), RAND (source vector replaced by a fixed random unit vector drawn once per run with pinned seed, scaled to destination norm ‖h_d‖; destination = d*, rerun span layers d+1..L — *the same rerun span as D→S*, making RAND the compute-matched perturbation control). All three arms use the convex norm-matched mixture (D2) with the fixed ramping schedule pinned below; no trained parameters anywhere (Δθ=0 held).

**P1 (small-α perturbation bound) [PROPOSITION].** The leak perturbs the destination residual stream by at most 2α in relative norm.
*Proof sketch:* ‖h_d^new − h_d‖₂ = α‖(‖h_d‖/‖h_s‖)h_s − h_d‖₂ ≤ α(‖h_d‖ + ‖h_d‖) = 2α‖h_d‖₂ by triangle inequality. ∎
*Scope:* at α=0.15 the relative perturbation ≤ 30%. If the downstream map Φ_{d+1..L} is K-Lipschitz on the data manifold, output perturbation ≤ 2αK‖h_d‖. This is the mathematical content of the paper's "small leakage avoids OOD feedback amplification" — the OOD risk is *controlled by α*, and the control is quantitative. The paper's empirical α range {0.04,…,0.16} sits inside the small-perturbation regime.

**P2 (depth-causality information advantage) [HYPOTHESIS — the discriminating claim].** In a feedforward net, h_d(x) is a function of layers < d only; h_s (s > d) contains context processed through s layers of contextualization (Lepori et al.: ambiguity resolved in deep layers; shallow layers hold the ambiguous mixture). The leak injects I(h_s; y | h_d) bits of *new* information at layer d — information no feedforward computation can provide to layer d. Hence D→S should beat S→D (which injects *less*-contextualized information upward into the deep layer) and RAND (which injects zero information, pure perturbation).
*Falsifier:* D→S ≤ S→D or D→S ≤ RAND ⇒ the gain is not information-advantage; the belief-state account is dead.

**P3 (dynamical-system license) [PROPOSITION].** Define the recirculated map G: h_d ↦ Φ_{d+1..L}(mix(h_d, h_s(h_d))). One full iteration is a discrete-time dynamical system h_d^{(k+1)} = G(h_d^{(k)}; x) in iteration index k, decoupled from depth — the same layer holds z(t) and z(t+1) for z(t+1) = f(z(t), x(t)) (paper §2, Fig. 4). A looped transformer, by contrast, only unrolls in depth (a deeper feedforward net with weight sharing). *Scope:* we test k=1 (one additional iteration), as in all paper experiments; unbounded k → a true RNN (paper §2).

**P4 (∩-shaped α signature) [PREDICTION].** The belief-state account predicts gain(α) rises then falls: too small α → signal below the noise floor of Φ; too large α → P1's bound loosens and representations leave the data manifold (paper: "increasing α amplifies the effect but results in more source-destination pairs that harm perplexity," Fig. 5). A generic-extra-compute account predicts no α-dependence of this shape (compute is constant in α); a pure-perturbation account predicts monotone gain in α. The ∩-shape is therefore a *discriminating signature*, pre-registered as: gain(0.15) ≤ gain(0.10) on the primary contrast. **Pinned adjudication rule (F6 — no unmapped cells):** monotone-increasing gain in α → PIVOT (B2, perturbation account); flat curve → neutral (the primary contrast rules); ∩-shaped or α=0.15-harms/α=0.10-helps → supports (B3).

**External license [THEOREM, cited not proved]:** Merrill & Sabharwal (2025), *A little depth goes a long way: the expressive power of log-depth transformers*, arXiv:2503.03961 — Θ(log n) layers necessary and sufficient for regular-language recognition up to length n (constructability; the Recirculation paper's depth-boundedness discussion cites it for this, and itself notes the proof addresses constructability, not learnability — not our claim to prove). Recirculation's iteration index k is not bounded by L, which is the formal sense in which it escapes the depth bound. [Citation re-verified against the primary PDF (arXiv:2608.17981v1) at repair time, LOG-309 — Law #3.]

---

## 4. Primary-source extraction (verified from arXiv:2608.17981v1 this turn)

- **Leak equation:** z_{t+1,t,d} = α f(z_{t,t,s}|d,t) + β z_{t,t,d}, β = 1−α (convex, 1B model); f rescales source to destination L2 norm (Eq. 2). 4B/12B models *critically require* non-convex β = 1 (paper §4.3).
- **α values:** swept {0.04, 0.07, 0.10, 0.16}; evaluations at α = 0.15 (β = 0.85).
- **Optimal (s,d) on tuning set:** 1B {11,4}; 4B {18,9}; 12B {35,16}. Pairs examined ≤ 12 layers apart. Destination ≈ layer 4 (1B); source 5–7 layers above. Recirculation *to layer-0 output* fails (representations not yet contextualized enough to be interpretable).
- **Ramping:** 1B needs α attenuated for the first ~10 tokens (early-token recirculation harmful: little state to propagate, OOD cost dominates); 4B/12B show no early-token harm.
- **Cross-family:** Ministral3, Pythia, Qwen3, Phi2 all show a robust region (middle of architecture) — but magnitude ≈ 5% (Gemma3) vs < 0.5% (others) *without* normalization/α tuning. **Pythia implication:** we must sweep (s,d), not copy Gemma's pair. Gemma gen-2/gen-4 also strong (Peri-LN architecture hypothesis — paper §5.2).
- **Controls that rule out artifacts:** (i) temperature tuning: T=1.2 alone gives 8.48% ppl reduction; recirculation alone 14.21%; combined 19.55% — nearly additive ⇒ not reducible to softmax sharpening. (ii) training-free looping: qualitatively different heatmaps; helps only at larger scales ⇒ different principle.
- **Token/lag analysis:** benefit is a power function of lag k (large at short lags, residual tail to lag 256); positions 20–200 most persistent; PoS: adverbs/adjectives/verbs biggest, numerals/determiners/pronouns smallest; single-token benefits additive in log-likelihood ⇒ supports the persistent-state story, rules out undifferentiated artifacts.
- **Downstream:** instruction-following error −25% (4B), −75% (12B) with preselected hyperparams; contextualization (Lepori Racing Thoughts): 1B/4B win on 2/3 question types, 12B disappointing (2/3 at disadvantage — honest null, keep).
- **Single-token benchmarks (Table 2, Gemma3 4B PT):** recirculation improves 6/8 modestly (MMLU 57.90→58.28; ARC-E 81.78→82.07; ARC-C 54.44→54.86; PiQA 79.98→80.52; BoolQ 79.08→79.11; Lambada 70.02→70.27; WinoGrande 69.46→69.38; HellaSwag 75.89→75.86).
- **GSM8K (4B PT, zero-shot CoT):** improves both pass@1 and pass@128 ⇒ both capability *sharpening* and *expansion* (Yue et al. framing). **Adaptive** recirculation: 8.8% / 20.9% error-rate reductions at pass@1/pass@128. (Abstract's "21% accuracy increase" = the 20.9% pass@128 error-rate reduction — report the precise form.)
- **Adaptive variant (out of scope, recorded):** learns α,β (scalar/vector × static/token-conditional); best = token-conditional vector via MLP (Hadamard, Eq. 3), trained on 250 docs each from arXiv/C4/PG19; mean 23.0% ppl reduction vs 8.5% basic; ≥ full fine-tuning (21.6%) with the base model untouched.
- **Latency:** no added generation latency (two stacks parallelize on modern hardware); serial prefill cost (cannot parallelize — the price of recurrence).

---

## 5. Design

**Model:** Pythia-410m (24 layers), frozen. Param hash logged pre/post (Law #13).

**Queue (F9):** GPU-dark until signed + CEO GPU clearance; queued behind K2 → EXP083 → EXP084; no pre-emption. (Nothing has executed — this line records the standing position, not a claim on the queue.)

**Stage A — (s,d) perplexity screen (GPU pilot).** Grid: d ∈ {4, 6, 8}, s = d + {4, 6, 8} (9 pairs; mirrors the paper's "source 5–7 above destination, middle of architecture" and the Pythia-family robust region). α = 0.10, convex mixture, norm-matched (paper Eq. 2). Corpus: ~50k held-out tokens (exact slice pinned at build; no test-set overlap with Stage B). Metric: perplexity reduction vs no-recirculation baseline. **Feasibility gate (pinned, F7):** compute mean perplexity-reduction Δppl for each of the 9 pairs on the pinned ~50k-token corpus. If no pair shows strictly-positive Δppl beyond the corpus noise floor (pinned at build — two no-recirculation repeat runs; default ε = 0 if unmeasurable) → INVALID (Pythia-410m may be unreceptive; do not proceed — the paper's <0.5% untuned Pythia result makes this a live outcome). Otherwise (s*, d*) = argmax Δppl, margin over the runner-up logged.

**Stage B — directional discrimination (GPU).** Fixed N=60 2-hop MCQ probe set (pin, F11: reuse the EXP077 60-record archive verbatim — `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`, sha256 `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585`, 60 records, established LOG-306/LOG-307 — with fixed indices; any deviation loudly logged per the EXP084-D1 convention; or the program's standard probe — decided at build, registered before running). At (s*, d*), α ∈ {0.07, 0.10, 0.15}, conditions {D→S, S→D, RAND matched-norm} + no-recirculation baseline. Ramping (pinned schedule, F8): α·(t/10) linear ramp over token positions t = 1..10, full α from t = 11 onward (paper §4.3: 1B needs attenuation for the first ~10 tokens; the schedule is fixed for all runs) — recorded at build, never tuned.
- **Primary contrast (pinned, F4):** Δ = ΔM(D→S) − ΔM(S→D) at leak coefficient α_leak = 0.10, N=60. Endpoint: accuracy. With a common baseline and common items, the paired D→S-vs-S→D correctness comparison IS the contrast. Primary test: single paired McNemar exact one-sided (p ≤ 0.05) + two-sided 95% Tango CI (the §G1b/EXP077 convention) on the paired difference. Pooled-across-α and per-α readings are secondary/discriminant with no Supported-licensing power (EXP085-F5 precedent).
- **Secondary:** D→S vs RAND (rules out generic perturbation); per-α curve with the ∩-shape prediction gain(0.15) ≤ gain(0.10).
- **Verdicts:** KILL the belief-state account if Δ ≤ 0 (LCI ≤ 0) or D→S ≤ RAND → the gain, if any, is perturbation/compute, not feedback. CONTINUE (to conditional/adaptive variants, pending the CEO boundary ruling) iff Δ > 0 with LCI > 0.05 and D→S > RAND. PIVOT iff recirculation beats baseline but Δ ≈ 0 → characterize as perturbation/compute effect (measure vs 2×-compute baseline: two independent forward passes + vote). HELD if CIs straddle (underpowered — no N increase pre-registered; report as inconclusive per the program's power-gate precedent). **Sub-threshold mapping (binding §G1b, F5):** L > δ_min → Supported; U < δ_min → Not supported (contrast dead); otherwise Inconclusive (held, never culled) — so 0 < LCI ≤ 0.05 is held, not killed. **Honest MDE note:** N=60 → L1 MDE 10pp = 2·δ_min (§B2, PARADIGM_AUDIT_2026-09-23); CONTINUE's LCI > 0.05 bar on a difference-of-gains needs a large net effect — HELD is the likely outcome and must be reported as inconclusive per the power gate, not narrated upward.
- **Breaking points (pre-registered):** (B1) Stage-A screen flat → INVALID, stop. (B2) monotone gain in α → perturbation account favored over belief-state (PIVOT). (B3) α=0.15 harms vs baseline while 0.10 helps → consistent with P1's OOD bound (supports, with the ∩-shape). (B4) S→D ≥ D→S → KILL belief-state (information flows the wrong way or nowhere).

**Cost (honest fwd-equiv):** Stage A: 9 pairs × 2 × ~25 blocks ≈ 450 block-passes. Stage B: 60 × 3 × 3 × 2 = 1080 leak passes + 60 no-recirculation baseline passes = 1,140 passes. Total ≈ 1,590 passes ≈ **0.02 T4-h (~1–2 min)**. Estimate only; GPU-node actuals logged.

---

## 6. Pre-registered contingencies

- If the EXP077 archive is unavailable → fall back to the program's standard 2-hop MCQ probe; the substitution is logged as a deviation per the EXP084-D1 convention, never silent.
- Interaction with CLLC/S3-9: if S3-9 returns nonlinear CV_α[g], the P1 Lipschitz reading weakens but P2's directional prediction stands (direction, not linearity, is the discriminator) — recorded, not resolved here.
