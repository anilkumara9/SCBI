# Innovation Sprint — SUMMIT-aimed mechanism candidates (2026-09-25)

**Sprint agent:** Innovation Sprint (reporting to CEO Nova), under the 30-Day Autonomous Campaign Charter (`research/CAMPAIGN_30DAY.md`).
**Summit question:** *What discovery would have to be true for a frozen model to become far more cognitively capable through inference-time computation?*
**Status:** PROPOSAL DOSSIER — licenses nothing. Every candidate below requires its own signed pre-registration + independent Law #14 review before any execution (launch chain).

---

## 1. Evidence base (the ground truth these candidates are built on)

[OBSERVATION] — all numbers from primary artifacts, not summaries:

- **The boundary (EXP065/066):** raw cross-vocabulary cosine +0.7186 / +0.6852 collapses to +0.0032 / −0.0118 after Procrustes (Δcos −0.7154 / −0.6971). Raw geometric similarity ≈0.7 carries **zero causal transfer** under static injection. Former positive Procrustes claims retracted.
- **The output-side signal (EXP070/077):** every static geometric variant decision-flat (ΔM=0, p=1.0 across cone/cone-vs-line/offset/radial-grid); the option-informed bridge rescues +16.67pp (p=0.001953, EXP070) and +10pp (p=0.03125, EXP077). Bridge power localizes **outside** the tested concept subspace (EXP078). Bridge is option-informed → Law #7 violation → rescue artifact, not autonomous mechanism (LOG-204 demotion stands).
- **The EXP091 null (LOG-361/362, ADOPTED):** zero-shot cosine scoring of frozen Pythia-410m/layer-20 embeddings on 60 novel relational items: **31/60 (51.67%), p=0.4487**; margins noise-scale (mean 6.8e-4, max 1.38e-3); cosA_mean≈cosC_mean≈0.19; **instrument responsive** (G4 spread 0.0803 ≫ 1e-4 deaf bar); guards all pass; Δθ=0 verified. A genuine null from a working instrument — the free-lunch version is dead.
- **Non-normal dynamics (EXP086 Stage A):** Henrici He 0.7332–0.8343 (mean 0.7689) across all 48 attention blocks — strongly non-normal layer dynamics (advisory, non-binding).
- **Kills on record:** G1 killed the QK-null-space mechanism sentence; K1 found no persistent readout tilt (0/180 at the 0.9 bar); EXP082/EXP085 KILLed as designed.
- **Frontier (CLM8B_ADAPTATION_2026-09-25):** frozen Qwen3-8B + two ~20M *trained* projection heads + bidirectional InfoNCE scores candidates at the output boundary (vendor-reported capability; 9× claim UNVERIFIED). Zero-shot over frozen geometry is at chance (our EXP091) — the trained-vs-zero-shot gap is the open question. Any trainable-heads proposal below is flagged SCOPE-CHANGE.

## 2. Design constraints (what is dead, what is occupied)

**Do not propose:** static/unconditional geometric injection (Family A — five rooms dead under narrow license); zero-shot cosine/direction scoring of frozen embeddings (killed by EXP091 — candidates must not be the falsified thing); QK-subspace operators (G1); unsound cross-space fits (Procrustes — retracted); bare-word tokenization guards (EXP090 lesson).

**Occupied by prior art (novelty ceiling N1 unless differentiated):** Family C inference-time search+self-eval (LTPO, NoisyCoconut, Meta-Reasoner, Self-Refine); Family D logit optimization (∇-Reasoner); Family E feedback control (Activation-LQR); per-instance latent optimization (LTPO).

**Occupied by this program's own candidates:** C1 CLLC (closed-loop control), E7 DPRS (readout-space search), C2 ELM, C3 TTPS, C4 ASR, C5 LCMIC, C6 CLB, E8 donor-bridge, S3-1 ARP, S3-2 LOM, S3-3 DUG, S3-4 SAH, R1–R7 pipeline, K2/EXP083/084/086/087/088 queue. New candidates below are differentiated against each.

---

## 3. The seven candidates

Each carries a full Law #15 block: (1) precise question, (2) the KILL/CONTINUE/PIVOT decision it affects, (3) cheapest falsifying test + cost, (4) mathematical license + quantitative prediction + breaking point.

---

### Candidate 1 — IBL: Information-Bottleneck Localization

**Mechanism sketch.** EXP091 asked whether frozen geometry aligns with labels (answer: no, at layer 20). IBL asks the prior question: *where, if anywhere, does the frozen residual stream carry mutual information about the correct answer?* For each layer l, estimate task-relevant information via 1-nearest-neighbor leave-one-out classification accuracy on the layer's embeddings (a finite-sample-robust lower bound on MI via Fano's inequality; KSG kNN-MI as a secondary statistic after PCA to ≤20 dims, with the n=60 sample-size limitation declared). If no layer carries signal, the information is not "misplaced" — it is absent, and the bridge's +10pp must come from its label-informed construction (strengthening the LOG-204 artifact interpretation). If a layer lights up, the program's readout target moves there.

**Law #15 block.**
1. *Precise question:* Is max_l Î(h_l; y) > 0 at any layer of frozen Pythia-410m on the 60-item relational bench, where Î is 1-NN LOO accuracy vs a stratified permutation null?
2. *Decision affected:* CONTINUE the "misplaced information" program (redirect readout to l*) vs KILL it (information absent everywhere → bridge-as-artifact interpretation strengthened; PIVOT the output-side program toward construction-artifact forensics).
3. *Cheapest falsifying test + cost:* one per-layer extraction run (60 forward passes, CPU ~40 min — same as EXP091) + 1-NN LOO per layer (24) against 1,000 stratified permutations per layer. **$0 CPU, ~1.5h total.** No GPU, no weights touched (read-only extraction).
4. *Mathematical license:* Fano's inequality — classification error lower-bounds conditional entropy, so above-chance 1-NN accuracy certifies I(h_l; y) > 0 without density estimation; the permutation null controls finite-sample bias exactly. *Quantitative prediction:* under "misplaced information," some layer exceeds the permutation 95th percentile by ≥10pp; under "absent," all 24 layers sit inside the null band. *Breaking point:* no layer exceeds the Bonferroni-corrected permutation threshold → KILL the misplaced-information hypothesis (licensed kill, not inconclusive — the test has a calibrated null).

**Novelty audit.** No program experiment has scanned layers for task information; EXP091 read only layer 20. Prior art: linear probing across layers is old (probing literature), but the *use* here is diagnostic-adjudicative (artifact forensics on the bridge), not capability-claiming. N1.

---

### Candidate 2 — TGA: Transient-Growth-matched Amplifier

**Mechanism sketch.** EXP086 measured strong non-normality (He≈0.77) but stopped at the advisory scalar. Non-normal dynamics permit large **transient** growth: over a finite layer span, perturbations along specific directions can be amplified by σ_max(M) ≫ 1 even when all eigenvalues are stable (pseudospectra / Kreiss Matrix Theorem). TGA computes the leading right singular vector v_1 of the layer-to-layer propagator M = Π_{t=l}^{L} J_t (Jacobians via autograd on frozen weights) and injects the task signal along v_1 — the direction the network's *own dynamics* maximally amplifies — vs matched-norm random directions. This is dynamics-matched injection, not geometry-matched: it exploits the amplifier the model already contains.

**Law #15 block.**
1. *Precise question:* Is the transient-gain ratio σ_max(M)/σ̄(M) ≫ 1 over the injection-to-readout layer span, and does injection along v_1 produce ΔM > 0 where matched-norm random injection gives ΔM = 0?
2. *Decision affected:* two-stage. Stage-1 pilot: CONTINUE to a GPU injection pilot vs KILL the transient-amplifier program. Stage-2 (GPU, only if pilot passes): CONTINUE/KILL on causal decision gain.
3. *Cheapest falsifying test + cost:* **Stage-1 pilot ($0 CPU, ~1h):** randomized power iteration (≈30–50 JVPs per prompt, no full Jacobian) estimates σ_max(M); Hutchinson trace estimator gives σ̄(M); over ~10 bench prompts. **If median σ_max/σ̄ < 2 → KILL** — no exploitable transient amplifier exists, before any GPU spend. Stage-2 injection test only if the pilot passes (~0.1 T4-h, queued behind the founder's GPU).
4. *Mathematical license:* for the linearized propagator M, max_{||δ||=1} ||Mδ|| = σ_max(M) exactly (variational characterization of the leading singular value); non-normality (He≈0.77, measured) is the license for expecting σ_max/σ̄ > 1, since for normal M the ratio is ≈1. *Quantitative prediction:* pilot ratio ≥ 3 → injection along v_1 enjoys ≥3× the downstream gain of a random direction at matched norm, predicting ΔM_TGA > ΔM_random = 0. *Breaking point:* pilot ratio < 2 → KILL (the non-normality does not yield a usable directional gain; He was a red herring for control purposes).

**Novelty audit.** EXP086 Stage B amplifies along the *decision normal* (deflated power iteration on a task direction); TGA injects along the *dynamics'* maximally-amplified direction (task-agnostic propagator SVD) — complementary, explicitly differentiated. Prior art: transient-growth analysis is textbook in fluid dynamics / non-normal systems (Trefethen & Embree); its application to transformer residual-stream injection is unoccupied to our knowledge (no citation found in the program's literature corpus; Law #14 review must verify). CLLC (C1) uses Jacobians for *feedback control*; TGA uses them for *open-loop basis selection*. N1, N2-adjacent on formulation if the pilot ratio holds.

---

### Candidate 3 — CGD: Controllability-Gramian Diagnosis of the transfer boundary

**Mechanism sketch.** The program's central mystery: the option-informed bridge transfers (+10pp) while the geometrically-similar B_agg does not (Δcos −0.7154 post-Procrustes; ΔM=0). CGD explains it with linear control theory: for the linearized trajectory, the finite-horizon controllability Gramian W = Σ_k Φ_k B B^T Φ_k^T ranks output directions by minimum-energy reachability. Transferable ⟺ high controllability weight: directions outside the controllable subspace require enormous injection energy, i.e., they *cannot* transfer under bounded injection — which is exactly the observed boundary. The test: measure cosine overlap of (a) the EXP077 bridge direction and (b) the failed B_agg (both on disk in `exp077_vectors.pt`) with the top-k controllable subspace. If CGD holds, it *generates* new candidate directions (top controllable vectors) for follow-up injection tests — turning a diagnostic into a direction foundry.

**Law #15 block.**
1. *Precise question:* Does the bridge direction lie in the highly-controllable subspace of the frozen dynamics while B_agg does not (overlap_bridge ≫ overlap_Bagg ≈ random)?
2. *Decision affected:* CONTINUE the controllability program (→ foundry: inject top controllable vectors) vs KILL the controllability explanation of the boundary (the boundary needs a different theory).
3. *Cheapest falsifying test + cost:* randomized power iteration on W (matrix-free: Φ and Φ^T via JVPs/VJPs, no full Jacobians), top-10 subspace, overlap cosines for bridge vs B_agg vs 1,000 random directions as null. **$0 CPU, ~1–2h.** Vectors on disk; weights read-only.
4. *Mathematical license:* minimum control energy to reach direction d scales as 1/(d^T W d) (linear systems theory, [THEOREM]); random-direction overlap with a 10-dim subspace of R^1024 concentrates at √(10/1024) ≈ 0.099. *Quantitative prediction:* overlap_bridge > 0.5 while overlap_Bagg < 0.2. *Breaking point:* permutation test fails to separate bridge from B_agg (p > 0.05) → KILL the controllability explanation.

**Novelty audit.** Controllability Gramians are textbook control theory; applied to *explaining* a representation-transfer boundary in transformers, unoccupied in the program's corpus (Law #14 to verify). Differentiated from CLLC (control *design*) — CGD is control-theoretic *diagnosis*. N1.

---

### Candidate 4 — SCS: Stability-gated Consensus Scoring

**Mechanism sketch.** The synthesis (C5) states the bottleneck is the verifier, and none has been built. SCS builds the cheapest possible one: a decision is trusted only if it is **stable under meaning-preserving perturbation**. For each bench item, generate 2 paraphrases with the frozen model (CPU), score all three variants with the EXP091 instrument, and apply the stability gate: decide only when sign(margin) agrees across variants (confirmation-gated vote); abstain otherwise. Bias–variance logic: genuine signal survives paraphrase (sign-consistent); noise flips sign (inconsistent). The measurable claim: the sign-consistent subset has accuracy > chance while the inconsistent subset does not — i.e., stability *carries* decision signal the raw margin lacks.

**Law #15 block.**
1. *Precise question:* Does cross-paraphrase sign-consistency of the cosine margin predict correctness (consistent-subset accuracy > 0.5) on the 60-item bench?
2. *Decision affected:* CONTINUE the stability-verifier program (→ a verifier component for the G/E/S/T loop) vs KILL it (stability adds nothing; the verifier bottleneck stands).
3. *Cheapest falsifying test + cost:* 120 paraphrase generations (frozen Pythia-410m, CPU) + rescoring with the existing EXP091 pipeline. **$0 CPU, ~1–2h.** (No pairing exists on disk — verified: 60 unique ids, 0 cross-phrasing pairs — so generation is required; stated honestly.)
4. *Mathematical license:* under pure noise (the EXP091 null), P(sign agreement across 3 variants) concentrates at its binomial null and the consistent subset stays at chance — the test *cannot* manufacture signal from noise; under signal+noise, agreement probability rises with |signal|/|noise| (elementary). *Quantitative prediction:* consistent subset (expected ~25–35 items under weak signal) accuracy ≥ 65% vs inconsistent subset ≤ 55%. *Breaking point:* consistent-subset accuracy ≤ 55% (binomial vs 0.5, p > 0.05) → KILL the stability-gate claim.

**Novelty audit.** Self-consistency (Wang et al.) votes over *reasoning paths*; SCS gates a *geometric margin* on cross-perturbation sign stability — different object. NoisyCoconut uses latent-noise consensus for abstention (Family C, occupied slot) — SCS differs: deterministic paraphrase perturbations of the *input*, applied to the *scorer*, with a pre-registered falsification bar. N1.

---

### Candidate 5 — LTI: Layer-Trajectory Coherence readout

**Mechanism sketch.** Every killed experiment read a *single* layer. LTI reads the *trajectory*: for each option, c_l = cos(state_l, action_l) across layers 1..24. If the forward pass iteratively refines toward the correct answer (discrete-time convergence), the correct option's alignment trajectory should be more monotone/smooth — a convergence signature — while the foil's is an unconverged walk. Decision statistic: Spearman ρ(c_l, l) (refinement monotonicity), paired correct-vs-foil per item. This uses the layer axis as *time*, a genuinely dynamical readout no killed experiment employed.

**Law #15 block.**
1. *Precise question:* Is the cross-layer alignment trajectory of the correct option more monotone (higher Spearman ρ with layer index) than the foil's, paired per item?
2. *Decision affected:* CONTINUE the dynamical-readout program (→ trajectory-based decision rules) vs KILL it (layer dynamics carry no decision signal beyond single-layer geometry).
3. *Cheapest falsifying test + cost:* per-layer extraction (60 forward passes, CPU ~40 min — one run yields all layers) + paired Wilcoxon on Δρ. **$0 CPU, ~1h.**
4. *Mathematical license:* under the null (no iterative refinement), both trajectories are exchangeable random walks → E[Δρ]=0 with a symmetric null (permutation-calibrated); under convergence dynamics, the correct trajectory's ρ concentrates positive (analogous to Lyapunov-function monotonicity along trajectories). *Quantitative prediction:* mean Δρ > 0.15. *Breaking point:* Wilcoxon p > 0.05 or Δρ < 0.05 → KILL.

**Novelty audit.** S3-3 DUG uses layer *disagreement* for routing/escalation; LTI uses trajectory *coherence* for the decision itself — differentiated (routing vs deciding). Reading "all layers" for probing is old; the *monotone-convergence decision statistic* on option alignment is the new claim. N1.

---

### Candidate 6 — GNR: Gradient-Norm (Fisher-score) readout

**Mechanism sketch.** EXP091's null is *first-order*: cosine direction carries no signal. GNR goes *second-order*: the decision invariant is the local sensitivity s(o) = ||∇_h log p(o | premise)|| — the Fisher score norm of each option. License: the score is the sufficient statistic for local discriminability (Fisher information = Var(score)); if pretraining concentrated task distinctions in the loss landscape's *curvature* rather than embedding *direction*, first-order cosine is blind by construction while the score norm sees it. Two-sided paired test (direction of the effect registered as unknown — the claim is "curvature carries information," not its sign).

**Law #15 block.**
1. *Precise question:* Does ||∇_h log p(o|premise)|| differ systematically (two-sided) between the correct and foil options, paired per item?
2. *Decision affected:* CONTINUE the second-order readout program (→ curvature-based decision rules) vs KILL it (no second-order signal either; the null deepens to all local geometry).
3. *Cheapest falsifying test + cost:* 120 backward passes (2 options × 60 items, frozen Pythia-410m, CPU) + two-sided Wilcoxon on paired norms. **$0 CPU, ~3h.**
4. *Mathematical license:* Fisher information identity (E[ss^T] = −E[H]); under the null the paired norm differences are symmetric about 0. *Quantitative prediction:* two-sided Wilcoxon p < 0.05 with a consistent sign across ≥60% of items. *Breaking point:* p > 0.05 → KILL the curvature-readout hypothesis.

**Novelty audit.** Gradient-based *interpretation* (saliency) is old; gradient-norm-as-*decision-rule* on frozen representations for relational choice is unoccupied in the program's corpus. Differentiated from ∇-Reasoner (Family D: gradient *descent on logits* as the mechanism) — GNR *reads* the gradient norm, never descends. N1.

---

### Candidate 7 — SAR: Span-Averaged Readout (noise-model adjudication)

**Mechanism sketch.** EXP091 used final-token pooling (the CLM recipe). Each entity occurs *twice* in-prompt (premise + question; G1' verified single-token at both). If per-occurrence embeddings are signal + iid noise, averaging over occurrences improves SNR by √k — and the EXP091 margins (mean 6.8e-4, noise-scale) are exactly the profile where denoising matters. If the noise is *systematic* (no signal at all), averaging changes nothing. SAR adjudicates the noise model of the EXP091 null — which every follow-up interpretation depends on. Honest flag: this is an *ablation*, not a mechanism; ranked accordingly.

**Law #15 block.**
1. *Precise question:* Does span-averaged entity pooling (mean over in-prompt occurrences) lift margins out of the noise floor / move accuracy off chance vs final-token pooling?
2. *Decision affected:* KILL the iid-noise model (→ the EXP091 null is systematic absence of signal; do not chase denoising variants) vs CONTINUE denoising ablations (→ pooled readouts as the default instrument).
3. *Cheapest falsifying test + cost:* fresh extraction with span-averaged entity embeddings (60 forward passes, CPU ~40 min) + the registered EXP091 scorer unchanged. **$0 CPU, ~1h.**
4. *Mathematical license:* Var(mean of k iid) = Var/k (elementary); under iid noise, margin scale grows ~√2 with k=2 occurrences. *Quantitative prediction:* margin mean ≥ 9.6e-4 (√2 × 6.8e-4) with accuracy movement, OR no change. *Breaking point:* margins still noise-scale AND accuracy ≤ 37/60 → KILL the iid-noise model (systematic null confirmed).

**Novelty audit.** Pooling ablations are standard; the *use* is adjudicative (noise-model forensics on an adopted null). N0/N1 — included for falsifiability-per-dollar, not ambition.

---

## 4. Ranking by falsifiability-per-dollar

Score = (decision weight × kill-decisiveness) / cost. All $0; cost is CPU-hours + interpretive leverage.

| Rank | Candidate | Cost (CPU) | What a kill buys | What a continue buys |
|---|---|---|---|---|
| **1** | **IBL** | ~1.5h | Kills "misplaced information"; strengthens bridge-artifact case; closes the biggest interpretive fork | Redirects the entire readout program to l* |
| **2** | **TGA pilot** | ~1h | Kills the dynamics-matched program before any GPU spend | Opens a new injection basis from the model's own amplifier |
| **3** | **CGD** | ~1–2h | Kills the controllability explanation of the boundary | Explains the central mystery + foundry for new directions |
| 4 | SCS | ~1–2h | Kills the stability-verifier premise | First genuine verifier component for the loop |
| 5 | LTI | ~1h | Kills dynamical-readout | Trajectory-based decision rules |
| 6 | GNR | ~3h | Deepens the null to all local geometry | Second-order decision rules |
| 7 | SAR | ~1h | Confirms systematic null (kills denoising line) | Pooled readouts as default instrument |

## 5. Top 3 — expanded falsification paths

**#1 IBL.** The single highest-leverage question in the program right now is interpretive, not mechanical: *is the bridge's power misplaced information or construction artifact?* IBL answers it with a calibrated null in ~1.5 CPU-hours. If no layer exceeds the permutation threshold, the "output-side room" as an autonomous-mechanism program loses its last refuge — the honest next step is artifact forensics (E8 donor-transfer under full Law #7, or retirement of the room). If a layer lights up, every subsequent experiment re-targets. No other candidate re-orients the program as fast.

**#2 TGA pilot.** The non-normality measurement (He≈0.77) is currently decorative — advisory, non-binding, explaining nothing. The pilot converts it into a decision in ~1 CPU-hour: either the dynamics contain a usable directional amplifier (ratio ≥ 3 → GPU injection test with a real license) or they don't (ratio < 2 → the He number was a red herring and the dynamics program stands down). Randomized power iteration + Hutchinson keeps it honest and cheap; no full Jacobians, no GPU, no hand-waving.

**#3 CGD.** If it holds, it does something no program result has done: *explain* the 0.7-cosine-zero-transfer boundary mechanistically rather than merely mapping it. Minimum-energy reachability is the right language for "why does this direction transfer and that one doesn't" — similarity was always the wrong quantity; controllability may be the right one. And unlike pure diagnostics, it manufactures its successors (top controllable vectors → injection candidates).

## 6. Required controls (not candidates — mandated for the next pre-registrations)

- **LM log-prob baseline:** p(option | premise) from the frozen model's own next-token distribution, on the 60-item bench. The program has never run its most obvious baseline. If it is also at chance, the bench is genuinely hard; if above chance, the geometry program was looking in the wrong place and the logits were the instrument all along. $0 CPU, ~1h. Every future readout pre-registration must include this control.
- **Span-occurrence consistency check:** cos(occurrence_1, occurrence_2) per entity — if ≈1, SAR's premise (iid noise across occurrences) is already weakened before extraction.

## 7. Rejected darlings (kill-your-darlings log)

- **Min-entropy prefix search** (optimize a per-instance prefix to minimize answer entropy): crowded (OPRO et al.), weak novelty, expensive on CPU. Killed on novelty-per-dollar.
- **1-bit SimHash denoising** of cosine margins: the "discretization denoises" license did not survive scrutiny — under the EXP091 noise profile the majority-vote gain is unquantified without a noise model SAR would first have to establish. Killed on license; revisit only if SAR continues.
- **Test-time soft-prompt optimization:** occupies LTPO's "per-instance latent optimization" slot (N0/N1 at best), and per-instance gradient optimization on CPU is prohibitively slow. Killed on occupancy + cost.
- **Trained contrastive heads (CLM-style):** the honest adaptation of the frontier finding — but it is SCOPE-CHANGE (trainable apparatus; needs training data/compute the program does not have at $0). Flagged, not proposed: it requires its own experiment number, an explicit Law #7 training protocol, and founder licensing of the Δθ≠0 apparatus framing. Recorded here so the idea is not lost: *if* training becomes available, the head-training program starts from the EXP091 null as its zero-shot baseline.

---

## 8. Session notes

- Summit filter applied to all seven: each candidate names a discovery that would have to be true (layer-localized task information; a usable transient amplifier; controllability as the transfer quantity; stability as signal; convergent layer dynamics; curvature-carried distinctions; iid noise) for frozen inference-time computation to gain capability.
- No experiments executed in this sprint ($0 CPU, proposals only). Next step per candidate: signed pre-registration + independent Law #14 review (launch chain).
- Dossier: `research/innovation/SPRINT_2026-09-25_SUMMIT.md` (this file).
