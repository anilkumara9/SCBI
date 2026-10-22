# S4-5 (J4) Free-Energy Branch Selection — Pre-registration DRAFT (UNSIGNED)

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. Licenses nothing. No run is authorized by this document.*
*Before any execution: independent Law #14 review of this exact draft + CEO approval. Stage 2 additionally requires the founder's Kaggle GPU.*
*No experiment number is minted in this draft. The number is minted by the CEO only at pre-registration SIGN (after independent Law #14 review + CEO approval), and must be verified free in the research log and backlog before minting.*
*Licensing chain: LOG-288 (S4-5/J4 born, QUEUED as backlog row 23, 2026-09-24) → LOG-4879 (Friday cull option (b): redirect to surviving J-tier lines) → LOG-4883 (G/E/S loop family stood down) → `research/innovation/S45_DESIGN_2026-10-03.md` (worth-it gate, verdict CONDITIONAL RUN) → `research/innovation/S45_DESIGN_REVIEW_2026-10-03.md` (independent Law #14 review, APPROVE-WITH-CONDITIONS C1–C5) → this draft.*
*Governing laws: Law #2 (no invented numbers), Law #3 (no fabricated citations), Law #4 (bars binding, no post-hoc shifts), Law #6 (Δθ=0), Law #7 (labels touch bench evaluation and the calibration instrument only — §7), Law #9 (metrics before inspection), Law #11 (observation vs interpretation), Law #13 (deterministic reproducibility), Law #15 (this document is the binding gate).*
*Epistemological labels per `AGENTS.md` §5 used throughout. $0 compute for this document.*

---

## 0. Law #15 block (binding)

**Precise question [HYPOTHESIS].** On the 60-item decision bench, does selecting the branch minimizing the frozen Pythia-410m model's per-token trajectory surprise (free energy) over K=4 branched rationale trajectories rescue decisions beyond the single-pass baseline (ΔM_FE) and beyond random-branch selection (ΔM_random)?

**Decision it changes.** **KILL (selector)** if the free-energy signal is significantly *inverted* at the Stage-1 calibration gate (G3) — the selector family is dead before any GPU spend — or if Stage-2 ΔM_FE ≤ ΔM_random — the selector carries no signal beyond branching diversity. **Calibrated-signal sub-reading of KILL (selector):** when G3 passed but ΔM_FE ≤ ΔM_random — the signal is real (calibrated) but useless for selection → re-scope to diagnostic use only (never a selector). **KILL (branching)** if Stage-2 ΔM_FE ≤ 0 — the branches contain nothing worth selecting. **CONTINUE** (licensed positive only) if G1–G3 pass and ΔM_FE ≥ +8pp with Newcombe paired 95% LCI > 0.05 **and** ΔM_FE > ΔM_random (paired one-sided p < 0.05) — licenses a follow-on (new number) on the selector mechanism, not an integration claim. **HELD** in the pre-registered intermediate/unrun cases (§5) — licenses nothing, kills nothing. Exactly one branch will be earned; precedence **KILL > PIVOT > CONTINUE > HELD** (PIVOT is an annotated sub-reading of KILL (selector), never earned independently — see line 16).

**Cheapest falsifying test.** Stage-1 CPU pilot: 240 generations + 240 combined scoring passes, $0 CPU, ~1h (LOG-4552 precedent) — carries three binding gates (G1 diversity, G2 F-variance, G3 calibration). The pilot exists to kill, not to confirm: the honest prior is against the signal (§9).

**Quantitative predictions (pre-registered bars).** G1: ≥2 distinct decoded answers across the 4 branches on ≥15/60 items. G2: median over items of (max_k F_k − min_k F_k) ≥ 0.05 nats/token. G3: C1 Spearman(F̄, per-item accuracy) negative, one-sided p < 0.05 **and** C2 TESTA-style partition mean(F̄|majority-wrong) > mean(F̄|majority-right), one-sided permutation p < 0.05 (100,000 permutations, seed 20261006). Stage-2: ΔM_FE ≥ +8pp with Newcombe paired 95% LCI > 0.05 **and** ΔM_FE > ΔM_random (paired one-sided McNemar-exact p < 0.05).

**Breaking points (sharp).** G3 either-null → no GPU (HELD, family stands down — the signal may be absent rather than anti-informative). G3 either-inverted (wrong-direction p < 0.05) → **KILL the free-energy-selector family outright**. Stage-2 ΔM_FE ≤ ΔM_random → **KILL selector**. Stage-2 ΔM_FE ≤ 0 → **KILL branching**. Any validity gate in §3 fails → screen VOID (HELD with reason, never a verdict on the hypothesis).

**The belief it tests (named).** "Target-free, training-free evaluation is impossible without a trained judge" → "the frozen model's own trajectory surprise density can select better than voting, with no labels and no training." [INTERPRETATION]

---

## 1. Background, license, and condition-closure checklist

- **S4-5/J4** (backlog row 23, QUEUED since LOG-288): "Does free-energy selection over branched trajectories rescue decisions?" — L2-aimed summit tier; the program's only remaining candidate for a training-free, target-free evaluator.
- **Design** (`S45_DESIGN_2026-10-03.md`): worth-it gate, verdict CONDITIONAL RUN. **Independent Law #14 review** (`S45_DESIGN_REVIEW_2026-10-03.md`): APPROVE-WITH-CONDITIONS C1–C5. This draft closes each condition; the closure is itemized here so the next reviewer can check it mechanically:
  - **C1** — all seeds pinned → §2 (S_B2 = 20261004, S_B3 = 20261005, S_PERM_C2 = 20261006, S_RANDOM = 20261003). Law #13: no seed chosen at runtime.
  - **C2** — citation correction → this section: the H-wave "108 generations in 20.9 min" precedent is the EXP109 execution report at **LOG-4552** (verified 2026-10-03 by grep of `reports/research_log.md`: the figure appears in the LOG-4552 entry; LOG-4553 is the H2 QBR pre-registration draft). The design's LOG-4553 citation is corrected here.
  - **C3** — prior-art verification → §8: Jinnai et al. arXiv:2311.05263, Freitag et al. arXiv:2111.09388, CycleVLA arXiv:2601.02295 — all three VERIFIED real at abstract level (arXiv API, 2026-10-03); FREIA distinction restated. Full-text verification flagged as follow-up for any paper use.
  - **C4** — degenerate-branch handling + dual reporting → §2: R_max = 48 pinned; empty rationale → F undefined → branch excluded from selection and all F-statistics (diagnostic count; ≥3 fully-degenerate items → pilot VOID); identical branches → F-spread 0, ties to lowest branch index (no special handling needed). Primary F (answer token excluded) and secondary full-trajectory F (answer token included) reported side by side.
  - **C5** — min-F consequence stated → §3: if the secondary min_k-F calibration diagnostic inverts while mean-F passes G3, the binding consequence is Stage-2's KILL-selector bar (ΔM_FE ≤ ΔM_random) — mean-calibration is not a selection license.
- **[FLAGGED DEVIATION — resolved, for the Law #14 reviewer]** The design's §5 C2 literal text reads "mean F̄ on majority-wrong items **<** mean F̄ on majority-right items," which tests the *inverted* hypothesis against the design's own stated licensed direction ("lower F ↔ higher accuracy"; C1 negative ρ; Law #15 prediction). This draft resolves the C2 trip condition to the licensed direction (wrong **>** right, one-sided) and flags the discrepancy here. Rationale: the licensed direction is stated twice in the design and is the candidate's Law #15 prediction; the `<` is a transcription slip, not a design choice. **Law #14 ruling: CONFIRMED** — the independent reviewer confirms the draft's resolution (EXP_S45_prereg_REVIEW_2026-10-03.md §0, C2-direction ruling).
- **Non-resurrection [FACT].** S4-5 injects no direction (vs killed static-geometry lanes), makes no loop claim (vs stood-down G/E/S, LOG-4883), uses no vote (vs EXP114 POE), uses no verbalized confidence (vs EXP125), revives no culled probe set (S3-5 culled LOG-4353; branch generators re-specified at prompt/decoding level). Every kill stands; nothing killed is re-tested.
- **Cost correction to the design [FACT].** The design's "240 generations + 300 forward passes" double-counts: the answer readout is folded into the teacher-forced scoring pass (§2), so the true Stage-1 cost is **240 generations + 240 combined scoring passes**. Still $0 CPU, still ~1h by the LOG-4552 precedent.

---

## 2. Branch construction (C1 — fully pinned)

**Model [FACT].** EleutherAI/pythia-410m, local HF cache revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` (the LOG-331 pin), 24 layers, d=1024, vocab 50304, `tie_word_embeddings: false` (verified from the cached `config.json` in the EXP139 pre-reg, 2026-10-03). Load via `AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=HF_REVISION, local_files_only=True, torch_dtype=torch.float32, device_map="cpu")` — float32 to match the committed records. **Backbone pin:** sha256 of the state dict must equal `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (verified against the committed EXP139 Stage-1 records `experiments/runs/EXP139_stage1/stage1_records.json`, 2026-10-03); mismatch → run VOID. Δθ=0 throughout: `model.eval()`, `torch.no_grad()`; post-run backbone hash must match the pin.

**Bench [FACT].** The 60-item decision bench reconstructed deterministically from `experiments/runs/EXP135_eval/run_exp135.py` (`build_bench`, `make_views`, `tok1`); `bench_sha256` must equal `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` (verified against the committed EXP139 Stage-1 records, 2026-10-03). Reconstruction mismatch → run VOID. All 60 items in canonical bench order, **view 0** (deterministic, pre-registered; no label-based item selection).

**Free-energy estimator [DEFINITION].** For branch k with rationale tokens r_k = (r_{k,1}, …, r_{k,|r_k|}) generated under branch prompt P_k:
- **F_k := −(1/|r_k|) · Σ_{i=1}^{|r_k|} log p_θ(r_{k,i} | P_k, r_{k,<i})** — per-token mean NLL (surprise density) of the rationale under the frozen model, teacher-forced. **Primary**: rationale tokens only (prompt excluded — branch prompts differ in option order; answer token excluded — keeps F a pure trajectory signal outside the margin's decision-local territory).
- **Secondary (C4)**: **F^full_k** := mean NLL over the rationale tokens **plus** the decoded answer token a_k — reported side by side with F_k; the design's answer-token exclusion is the weakest judgment and this is the hedge.
- λ-free: per-token normalization removes the invented complexity weight (the S4 sketch's `λ|r_k|` is dropped for an operational reason).
- Selection: **k* = argmin_k F_k** over non-degenerate branches; ties broken toward the lowest branch index. The decision is branch k*'s forced-choice answer a_{k*}.

**Branch generators (K=4, prompt/decoding level).**
- **B0** — anchor: greedy rationale (do_sample=False, ≤R_max tokens), view-0 prompt.
- **B1** — framing counterfactual: view-0 prompt with the two option texts exchanged in place (A-text ↔ C-text); greedy rationale. The label mapping is semantic, not positional: A = correct answer, so correctness remains (a_k == tok1("A")) and the readout is unchanged. This turns the known position bias into an exploitable branch.
- **B2, B3** — stochastic counterfactuals: view-0 prompt, sampling τ=0.7, fixed seeds **S_B2 = 20261004**, **S_B3 = 20261005** (design parameters, pinned — C1).
- Rationale template (fixed, identical for all branches): `<view-0 item prompt> Reason step by step, then answer:` — B0 shares this template, so ΔM isolates *selection*, not elicitation.
- **R_max = 48** tokens (C4). Generation stops at EOS or 48 tokens; a rationale truncated at 48 tokens is a valid trajectory (NLL over the 48 produced tokens).

**Answer elicitation and readout (pinned).** After rationale generation, append the literal suffix `"\nAnswer:"` and take the argmax over **{tok1("A"), tok1("C")}** at the final position — the same 2-token forced-choice readout as the EXP135 baseline, where `tok1(s) = tokenizer.encode(" " + s)[0]` (single-token assertion, same tokenizer as the model). Correct iff the argmax == tok1("A") (A = correct answer, semantic). **The readout is folded into the teacher-forced scoring pass**: one forward over (P_k + r_k + "\nAnswer:") yields (i) rationale log-probs → F_k, (ii) answer-position logits → a_k, (iii) −log p(a_k | context) → F^full_k. Causal-LM log-probs of rationale tokens are unaffected by the appended suffix — the fold is exact, not approximate.

**Degenerate-branch handling (C4 — pinned, no improvisation surface).**
- Empty rationale (0 tokens, immediate EOS): F_k undefined → the branch is **excluded** from selection, from F̄/F-spread computations, from the SC vote, and from per-item accuracy; the item-branch pair is counted in a degeneracy diagnostic. If all 4 branches of an item are degenerate, the item is excluded from G3 with a diagnostic count; **≥3 fully-degenerate items → pilot VOID** (HELD with reason).
- Identical rationales across branches: F_k computed normally; F-spread contribution 0; selection ties → lowest branch index. No special handling.
- Any other generation pathology (repetition attractor, non-EOS runaway) is *not* degenerate — its F_k is computed as defined; pathological trajectories are data, not errors (the EXP109 repetition attractor is the precedent for treating them as findings).

**Comparators (pre-registered).**
- **Random-branch:** uniform selection over the 4 branches per item via `torch.Generator().manual_seed(20261003)` (S_RANDOM = 20261003, pinned — C1), computed analytically on the branch answers — no extra passes. Expected ΔM_random ≈ mean-branch ΔM.
- **Self-consistency (forced, matched tokens):** majority vote over the 4 branch answers at the same K and token budget; ties broken toward B0's answer. Reported as ΔM_SC (secondary, not binding — the design's CONTINUE bar does not condition on SC; the comparator exists per SPRINT2_2026-09-23 §TIER-0 to check S4-5 against the voting it disavows).

**Endpoints (pre-registered).** ΔM_FE = acc(min-F selection) − acc(B0); ΔM_random = acc(random-branch) − acc(B0); ΔM_SC = acc(majority vote) − acc(B0). Accuracies over the 60 items. ΔM_FE > ΔM_random is tested by a paired one-sided McNemar-exact test on the (FE, random-branch) 2×2 table (b' = #{FE right, random wrong}, c' = #{FE wrong, random right}), p < 0.05.

---

## 3. Stage-1: CPU pilot — feasibility + calibration gates (binding)

**Items.** All 60 items, canonical bench order, view 0. 240 generations + 240 combined scoring passes, CPU, $0, ~1h (LOG-4552 precedent: 108 generations in 20.9 min; forward passes are far cheaper per the EXP139 Stage-1 60/60 CPU precedent).

**Validity gates** (all must pass, else the pilot is VOID → HELD with reason, never a verdict): (a) bench sha256 matches; (b) backbone pre-hash matches BACKBONE_PIN; (c) determinism spot-check: re-run B0 generation on 3 items (bench order 0, 30, 59) → byte-identical rationales; (d) post-run backbone hash matches the pin (Δθ=0).

**Binding gates** (all three must pass in the licensed direction or Stage 2 does not run):
- **G1 diversity:** ≥2 distinct decoded answers across the 4 branches on **≥15/60 items** (design parameter). If branches never diverge, branching is vacuous.
- **G2 variance:** median over items of (max_k F_k − min_k F_k) ≥ **0.05 nats/token** (design parameter; degenerate-excluded). If F_k is flat, the selector has nothing to select on.
- **G3 calibration** (the TESTA burden): the free-energy signal must predict correctness in the licensed direction. Instrument: per item, **F̄ = mean_k F_k** over non-degenerate branches (the *signal*; mean, not min — min is selection-adjacent); per-item accuracy = fraction correct over non-degenerate branch answers (**labels touch only this instrument**). Pre-registered tests, one-sided in the licensed direction (lower F ↔ higher accuracy):
  - **C1:** Spearman(F̄, per-item accuracy), one-sided p < 0.05, **negative** direction. (Mirrors TESTA's R3, which found ρ=−0.3958 for the margin — the sign must go the *other* way here.)
  - **C2:** TESTA-style partition — mean F̄ on majority-wrong items (per-item accuracy ≤ 0.5) **>** mean F̄ on majority-right items (≥ 0.75), one-sided permutation test (100,000 permutations, **seed 20261006** pinned — C1), p < 0.05. (Mirrors TESTA's R2/C2 procedure with the sign flipped to the licensed direction; see the §1 flagged deviation.)
- **G3 gate logic (binding):** C1 and C2 **both** pass in the licensed direction → G3 passes → Stage-2 gate opens (still needs CEO venue approval + founder GPU + signed pre-reg). **Either null → G3 fails → no GPU** (family stands down, not killed — the signal may be absent rather than anti-informative → HELD with reason). **Either significantly inverted (wrong-direction one-sided p < 0.05) → KILL the free-energy-selector family outright** — the signal carries the TESTA pathology and selection on it would be worse than random.
- **Secondary diagnostic (C5):** the same C1/C2 pair computed with **min_k F_k**. If the secondary inverts while mean-F passes G3, Stage 2 may still run, but the **binding consequence is Stage-2's KILL-selector bar (ΔM_FE ≤ ΔM_random)** — mean-calibration is not a selection license. This closes the instrument/selector gap (the instrument is deliberately not selection-adjacent).
- **Dual reporting (C4):** primary F_k and secondary F^full_k reported side by side for every endpoint; G1–G3 are computed on the primary F.

---

## 4. Stage-2: GPU selection test (only if G1–G3 pass; founder-gated)

**Procedure.** Same machinery as §2–§3 at the pinned R_max = 48, on the founder's Kaggle queue: 240 generations + 240 combined scoring passes + the SC comparator (rides free on the same branches) ≈ **<0.01 T4-h** (backlog row 23). Endpoints ΔM_FE, ΔM_random, ΔM_SC as §2. Inference per §6.

**Bars.** CONTINUE: ΔM_FE ≥ **+8pp** with Newcombe paired 95% LCI > 0.05 **and** ΔM_FE > ΔM_random (paired one-sided McNemar-exact p < 0.05). KILL (selector): ΔM_FE ≤ ΔM_random. KILL (branching): ΔM_FE ≤ 0.

**Licensing.** Stage 2 runs **only** if: (i) G1–G3 all pass in the licensed direction on the signed Stage-1 record; (ii) this pre-registration is Law #14-signed; (iii) CEO issues GPU venue clearance; (iv) the founder provides the Kaggle queue slot. This draft assumes nothing about venue availability.

---

## 5. Falsification tree (precedence KILL > PIVOT > CONTINUE > HELD)

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | G1–G3 pass **and** ΔM_FE ≥ +8pp with Newcombe LCI > 0.05 **and** ΔM_FE > ΔM_random (p < 0.05) | Free-energy selection carries signal beyond branching and beyond voting. Licenses a follow-on (new number) on the selector mechanism. |
| KILL (selector) | G3 either-inverted **or** Stage-2 ΔM_FE ≤ ΔM_random | The selector carries no signal (or is an anti-signal) → the free-energy-selector family is dead. **Calibrated-signal sub-reading:** when G3 passed, the verdict is annotated — the signal is real (calibrated) but useless for selection → re-scope to diagnostic use only (never a selector). |
| KILL (branching) | Stage-2 ΔM_FE ≤ 0 | The branches contain nothing worth selecting → the branching family is dead too. (Binding bars from backlog row 23.) |
| HELD (a) | G1 or G2 fails | Branching vacuous or selector vacuous — apparatus/screen finding, not a verdict on the hypothesis. |
| HELD (b) | G3 either-null | Signal absent, not anti-informative. Family stands down; licenses nothing, kills nothing. |
| HELD (c) | Stage-2 0 < ΔM_FE < +8pp, or Δ̂ ≥ +8pp with LCI straddling 0.05, or ΔM_FE > ΔM_random numerically with paired p ≥ 0.05 | Positive ΔM_FE failing either the Newcombe magnitude bar or the paired-significance bar — licenses nothing, kills nothing. |
| HELD (d) | ΔM_FE ≥ +8pp but ΔM_FE ≤ ΔM_random | A gain that doesn't beat branching diversity is not the candidate's claim (precedence: KILL selector). |
| HELD (e) | Stage-1 unrun, infeasible, or any validity gate fails | Screen VOID. Licenses nothing, kills nothing. |

Every region of (ΔM_FE, ΔM_random, LCI) space maps to exactly one verdict under the stated precedence — the review's case-table walk found no gap, and this draft preserves the mapping.

---

## 6. Inference: Newcombe paired interval (explicit construction — no software invented)

For n=60 paired items: b = #{baseline wrong, FE right}, c = #{baseline right, FE wrong}, Δ̂ = (b−c)/n.
- Wilson 95% interval (z=1.96, **no continuity correction**) for p̂_b = b/n → (l_b, u_b), and for p̂_c = c/n → (l_c, u_c), each clipped to [0,1]:
  center = (p̂ + z²/2n)/(1 + z²/n); half = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n).
- L = Δ̂ − √((p̂_b − l_b)² + (u_c − p̂_c)²); U = Δ̂ + √((u_b − p̂_b)² + (p̂_c − l_c)²).
- **Binding bar:** Δ̂ ≥ 0.08 **and** L > 0.05.
- Secondary (reported, not binding): McNemar-exact two-sided p on the 2×2 table.
The executing lane implements these equations verbatim and archives the code; any deviation voids the inference.

---

## 7. Law #7 boundary

Labels (correct answers) are used **only** for bench evaluation — computing accuracy, ΔM, the paired tables — and for the G3 calibration instrument (per-item correctness for Spearman/partition validation). **No branch score, no selection, no ranking, no gate threshold sees labels.** G1/G2 use no labels; G3's thresholds (p < 0.05, licensed direction) are fixed here, never tuned on labels. The κ̂-style structural firewall holds: the selector (argmin_k F_k) is computable with labels absent. Using mean-F rather than min-F as the instrument is a genuine firewall refinement, not a loophole (the Law #14 review, §3).

---

## 8. Citation verification (C3) and prior art

All verifications below are **abstract-level** (arXiv API, 2026-10-03); full-text verification is flagged as follow-up for any paper use (per the design's §8 and the S4-4 pre-reg's C4 precedent). The independent Law #14 reviewer's re-verification of the three non-FREIA citations was rate-limited at review time — the abstract-level verifications above stand; full-text verification remains the flagged follow-up.

- **Jinnai et al., "Model-Based Minimum Bayes Risk Decoding for Text Generation," arXiv:2311.05263 — VERIFIED real.** Abstract confirms: MBR decoding selects a hypothesis from a pool minimizing expected risk under a probability model per a utility function; approximates over a sampled hypothesis set; the proposed MBMBR variant uses the model probability itself as the distribution estimate instead of the Monte Carlo estimate, outperforming MBR on text-generation tasks with encoder-decoders and LLMs. Distinction: MBR needs a utility/risk function; S4-5's selector is judge-free — the model's own surprise density, no trained judge, no risk metric. (MBMBR's use of model probability is the closest neighbor; it remains utility-framed, S4-5 is not.)
- **Freitag et al., "High Quality Rather than High Model Probability: Minimum Bayes Risk Decoding with Neural Metrics," arXiv:2111.09388 (TACL, presented at NAACL 2022) — VERIFIED real.** Abstract confirms the exact warning the design cites: "model estimates and translation quality only vaguely correlate"; MBR over unbiased samples optimizing diverse metrics (BLEURT) beats beam search on human evaluation. Distinction: needs a neural metric (a trained judge); S4-5 is judge-free. Freitag's warning is the exact skepticism G3 operationalizes.
- **CycleVLA, "Proactive Self-Correcting Vision-Language-Action Models via Subtask Backtracking and Minimum Bayes Risk Decoding," arXiv:2601.02295 — VERIFIED real.** Abstract confirms: MBR decoding as a zero-shot test-time scaling strategy for VLAs after subtask backtracking; proactive self-correction on LIBERO/LIBERO-Plus and a real robot. Distinction: needs a failure predictor + backtracking apparatus + MBR over retries under a distance/risk metric; S4-5 needs only the frozen model's surprise density over branched rationale trajectories — no failure detector, no metric.
- **FREIA, "Free Energy-Driven RL with Adaptive Advantage Shaping," arXiv:2605.04065 — VERIFIED real by the independent Law #14 design review (2026-10-03).** Distinction restated: FREIA *trains* (free-energy principle as an RL reward under policy optimization); S4-5 trains nothing (Δθ=0) — pure inference-time selection. Same principle, opposite sides of the training/inference line.

**Novelty read: N1 (known combination)** — test-time trajectory selection has MBR prior art. The differentiators are the judge-free free-energy selector, falsification-first bars, and the pre-registered calibration gate on this bench/backbone. The draft claims none of the prior art's territory and cites it.

---

## 9. Expectation calibration

**Modal outcome: G3-null or a clean kill.** The honest prior is against the signal: TESTA showed internal signals on this bench family track the biased policy — possibly *inverted* — and free energy is computed from the same frozen model's logits on the same bench. The pilot's expected value is the cheap falsification of the free-energy-selector family at $0 — **boundary science on this bench/backbone, not a novelty claim and not a selection claim**. A G3 pass would be genuinely surprising precisely because the prior is against it; CONTINUE remains a long shot, priced not hidden.

---

## 10. Risks and honest limitations

1. **Honest prior against the signal** (§9): the inversion risk is the point of G3, not an afterthought.
2. **Temperature vacuity:** min-F may collapse to the deterministic anchor (B2/B3 have higher F by construction); the bars self-correct (collapse → ΔM_FE ≈ 0 → KILL branching), but the modal Stage-2 outcome may be KILL-branching, not CONTINUE.
3. **Elicitation shift:** the rationale template changes the decision context vs direct-decode baselines; ΔM is clean (B0 shares the template) but absolute accuracies are not comparable to EXP135's 43.67%.
4. **Bench specificity:** all bars are on the 60-item decision bench at Pythia-410m, view 0. No claim about other benches/backbones is licensed under any branch.
5. **The S4 sketch deviation** (l*-branching → prompt-level branching) is documented in the design's §2/§6.i; mid-layer branching is a separate design, not a fallback.
6. **F is sign-less until G3** — EXP135's lesson is respected by making the sign channel a gate, not an assumption.
7. **B1's order-swap construction** is mechanical (option-text exchange in the view-0 prompt, semantic label mapping preserved); the executing lane derives it from `run_exp135.py`'s `make_views` — the Law #14 reviewer should check the implementation against this pin.

---

## Appendix A. Condition-closure checklist (for the next Law #14 reviewer)

- [ ] C1: §2 pins S_B2 = 20261004, S_B3 = 20261005, S_PERM_C2 = 20261006, S_RANDOM = 20261003. No seed chosen at runtime.
- [ ] C2: §1 corrects the H-wave precedent to LOG-4552 (grep-verified; LOG-4553 is the H2 QBR draft).
- [ ] C3: §8 verifies Jinnai (2311.05263), Freitag (2111.09388), CycleVLA (2601.02295) at abstract level; FREIA distinction restated; full-text follow-up flagged.
- [ ] C4: §2 pins R_max = 48, degenerate-branch rules (empty → excluded, diagnostic count; ≥3 fully-degenerate items → VOID), and dual reporting of F_k and F^full_k side by side.
- [ ] C5: §3 states the min_k-F inversion consequence — Stage-2's KILL-selector bar is binding; mean-calibration is not a selection license.
- [x] Flagged deviation: §1 documents the C2 inequality-direction resolution (design's literal `<` → licensed direction `>`); **CONFIRMED** by the independent Law #14 reviewer (review §0).
- [ ] Cost correction: §1 states the true 240-gen + 240-pass Stage-1 cost (design said 300 passes).
- [ ] Pins: §2 backbone pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` and bench pin `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`, both verified against the committed EXP139 Stage-1 records.
- [ ] No experiment number minted in this draft (minted only at pre-reg SIGN).
