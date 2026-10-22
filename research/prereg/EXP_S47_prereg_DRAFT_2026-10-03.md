# S4-7 (J3) Spectral Phase Transition — Pre-registration DRAFT (UNSIGNED)

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. Licenses nothing. No run is authorized by this document.*
*Before any execution: independent Law #14 review of this exact draft + CEO approval. Any intervention stage additionally requires its own worth-it gate, Law #14-signed pre-registration, CEO GPU clearance, and the founder's Kaggle GPU — nothing about intervention is licensed here.*
*No experiment number is minted in this draft. The number is minted by the CEO only at pre-registration SIGN (after independent Law #14 review + CEO approval), and must be verified free in the research log and backlog before minting.*
*Licensing chain: LOG-288 (S4-7/J3 born, QUEUED as backlog row 25, 2026-09-24) → LOG-4879 (Friday cull option (b): redirect to surviving J-tier lines) → LOG-4883 (G/E/S loop family stood down) → LOG-4890 (S4-6/EXP141 killed at Stage-1 — the frozen model's self-evaluation carries no correctness information; J-tier queue continues to S4-7, the last surviving line) → `research/innovation/S47_DESIGN_2026-10-03.md` (worth-it gate, verdict CONDITIONAL RUN) → `research/innovation/S47_DESIGN_REVIEW_2026-10-03.md` (independent Law #14 review, APPROVE-WITH-CONDITIONS C1–C5) → this draft.*
*Governing laws: Law #2 (no invented numbers), Law #3 (no fabricated citations), Law #4 (bars binding, no post-hoc shifts), Law #6 (Δθ=0), Law #7 (labels define the correct/failed groups in the primary test only — §5), Law #9 (metrics before inspection), Law #11 (observation vs interpretation), Law #13 (deterministic reproducibility), Law #15 (this document is the binding gate).*
*Epistemological labels per `AGENTS.md` §5 used throughout. $0 compute for this document.*

---

## 0. Law #15 block (binding)

**Precise question [HYPOTHESIS].** On the 60-item decision bench, does the signal-eigenvalue count of the frozen Pythia-410m model's residual-stream covariance — eigenvalues above the Marchenko–Pastur bulk edge — differ between correct and failed items, with correct items showing more signal eigenvalues?

**Decision it changes.** **KILL (observational)** if the one-sided permutation test on Δ_s = median(s_correct) − median(s_failed) gives p ≥ 0.05 — the RMT lens sees nothing; the spectral-lens family is dead and the intervention is never attempted (pre-registered sequencing, the backlog's bar). **CONTINUE** (licensed positive only) if p < 0.05 **and** Δ_s ≥ 2 — the RMT lens sees a correctness-signed spectral signal; this licenses a **new worth-it gate** for the spectral intervention (new number), not a capability claim, not integration. **HELD** if p < 0.05 but Δ_s < 2 — significant but below the candidate's magnitude bar; or if any measurement-validity guard fires (§2) — licenses nothing, kills nothing. Exactly one branch will be earned; precedence **KILL > CONTINUE > HELD**. No PIVOT branch is licensed by the backlog row; none is invented here.

**Cheapest falsifying test.** Stage-1 CPU observational pilot: 60 forward passes with `output_hidden_states=True` + 1440 small Gram eigendecompositions, CPU, $0, ~1h (EXP139 60/60 CPU precedent). The pilot **is** the full observational test — there is no separate feasibility gate; the binding KILL/CONTINUE/HELD bars are evaluated on the pilot. The pilot exists to kill, not to confirm: the honest prior is against the signal (§8).

**Quantitative predictions (pre-registered bars).** Primary: Δ_s = median(s_correct) − median(s_failed) ≥ **2** (the backlog's Law #15 prediction, verified verbatim in the J3 sketch) with one-sided permutation p < **0.05** (100,000 permutations, seed **S_PERM = 20261010**, pinned). Wrong-direction significance gives p ≈ 1 → KILL (the bias-coherence counter-argument is collected by the instrument, not rhetorically absorbed).

**Breaking points (sharp).** p ≥ 0.05 → **KILL the observational claim** (intervention never attempted). p < 0.05 ∧ Δ_s < 2 → **HELD** (licenses nothing, kills nothing). n_i guard fires (§2) or any validity gate (§3) fails → **HELD with reason** (measurement-invalid or screen VOID — never a verdict on the hypothesis).

**The belief it tests (named).** "Reasoning has no physics-level description in frozen models" → "correct reasoning is a phase transition in residual-stream coherence, visible as excess signal eigenvalues above the MP bulk on correct items." [INTERPRETATION]

---

## 1. Background, license, and condition-closure checklist

- **S4-7/J3** (backlog row 25, QUEUED since LOG-288): "Does the signal-eigenvalue count (MP null) differ between correct and failed items?" — L2-aimed summit tier; the program's only remaining candidate for a *physics-level description* of reasoning, and the last surviving J-tier line.
- **Design** (`S47_DESIGN_2026-10-03.md`): worth-it gate, verdict CONDITIONAL RUN. **Independent Law #14 review** (`S47_DESIGN_REVIEW_2026-10-03.md`): APPROVE-WITH-CONDITIONS C1–C5. This draft closes each condition; the closure is itemized here so the next reviewer can check it mechanically:
  - **C1** — σ̂² estimator pinned → §2: bulk-median fit against the theoretical MP median at γ_i (numerical integration of the MP density; procedure fixed below). Bulk-fit diagnostic (median KS distance between empirical and fitted MP CDFs, reported, not binding; flag threshold 0.15). Max-inside-permutation construction stated explicitly in §2 (one sentence).
  - **C2** — n_i measurement-validity guard → §2: N_MIN = **40** (design parameter); items with n_i < 40 excluded from the primary test with a diagnostic count; if <30 items remain → HELD with reason ("insufficient positions for stable spectra"), never KILL. The n_i distribution (median, IQR, range, count below floor) is reported in the run record.
  - **C3** — full-text verification → §6: Martin & Mahoney (JMLR 2021), neural collapse (PNAS 2020), intrinsic dimensionality (ACL 2021) all **VERIFIED real** at full-text/abstract level 2026-10-03; plus a **new prior-art finding** (Ettori 2026 UIC thesis, arXiv:2601.17357v1 — spectral hallucination detection via MP divergence) that updates the design's honest negative. Nothing is marked verified that is not.
  - **C4** — validity gates → §3: determinism check, backbone pre/post hash (Δθ=0), bench hash, 60/60 pass completion — the standard EXP139/140/141 gate kit.
  - **C5** — citation fix → this section: the Friday cull is **LOG-4879** (LOG-4889 is the S4-6 pre-reg sign). The design's "LOG-4889/LOG-4879" is corrected here.
- **Non-resurrection [FACT].** S4-7 injects nothing, steers nothing, makes no causal claim at Stage 1 — it *observes* the spectrum (vs killed static-geometry lanes, which died on causal claims about pre-chosen injected directions). The PCs are computed from each item's own activations, never pre-registered. Vs the REJECTED EXP135 sprint: different signal (spectral vs pair-flip statistics), live pilot (archives insufficient per LOG-243), no record-grounded predictions — the Law #2 exemption is vacuous here and stated as such. Vs EXP114 POE: no voting. Vs the stood-down G/E/S loop (LOG-4883): not a loop component. Vs EXP125 (LOG-4680): no self-report of any kind. Vs S4-5/EXP140 (LOG-4888): different object (spectral structure of the decision pass vs trajectory surprise density); EXP140's G3-null does not transfer — re-tested from scratch. Vs S4-6/EXP141 (LOG-4890): observational (does the spectrum differ?) vs metacognitive (does the model judge itself?); EXP141 never touched this question. **The sharp edge:** amplifying the top-signal-PC would be directional manipulation — the intervention is explicitly sequenced behind the observational license, gets its own worth-it gate and number, and nothing about it is pre-licensed here. Every kill stands; nothing killed is re-tested.
- **Baseline-source decision [FACT].** Correctness labels come from the committed EXP140 B0 records (`experiments/runs/EXP140_stage1/stage1_records.json`), reused exactly as in EXP141 (id-aligned, no regeneration) — legitimate per the S4-6 review §7. No new baseline passes are needed; Stage-1 = **60 forward passes with hidden states**.

---

## 2. Spectral construction (C1–C2 — fully pinned)

**Model [FACT].** EleutherAI/pythia-410m, local HF cache revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` (the LOG-331 pin), 24 layers, d=1024, vocab 50304, `tie_word_embeddings: false`. Load via `AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=HF_REVISION, local_files_only=True, torch_dtype=torch.float32, device_map="cpu")` — float32 to match the committed records. **Backbone pin:** sha256 of the state dict must equal `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (verified against the committed EXP141 Stage-1 records, 2026-10-03); mismatch → run VOID. Δθ=0 throughout: `model.eval()`, `torch.no_grad()`; post-run backbone hash must match the pin.

**Bench [FACT].** The 60-item decision bench reconstructed deterministically from `experiments/runs/EXP135_eval/run_exp135.py` (`build_bench`, `make_views`, `tok1`); `bench_sha256` must equal `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` (verified against the committed EXP141 Stage-1 records, 2026-10-03). Reconstruction mismatch → run VOID. All 60 items in canonical bench order, **view 0** (deterministic, pre-registered; no label-based item selection).

**Activation capture [DEFINITION].** For item i, one forward pass with `output_hidden_states=True` over the view-0 input tokens. For layer l = 1…24 (the 24 transformer-block outputs, i.e. `hidden_states[1]`…`hidden_states[24]`), let H_{i,l} ∈ ℝ^{n_i×1024} be the residual stream, where n_i = number of non-padding input token positions for item i. Center per dimension: X_{i,l} = H_{i,l} − mean over positions. Form the n_i×n_i Gram G_{i,l} = X_{i,l} X_{i,l}^T / n_i (same nonzero spectrum as the 1024×1024 covariance; the cheaper construction). Eigendecompose: λ_1 ≥ … ≥ λ_{n_i} ≥ 0. **Memory discipline (pinned):** accumulate the Gram per layer and discard the raw hidden-state tensor before the next layer — peak memory is one item's hidden states, not the full 590MB at once.

**σ̂² estimator (C1 — pinned) [DEFINITION].** The Marchenko–Pastur null is a *counting rule*, not a data-generating model; the label permutation test (§3) is the falsification instrument. The noise variance is fit per (item, layer) by the bulk median:
- Aspect ratio γ_i = 1024 / n_i (> 1, since n_i < 1024).
- Theoretical MP median for the nonzero spectrum: m_MP(γ_i) solves F_{γ_i}(m) = 1 − 1/(2γ_i), where F_{γ_i} is the MP CDF with parameter γ_i (the atom at 0 has mass 1 − 1/γ_i; the nonzero eigenvalues' CDF is the continuous part renormalized). Computed by numerical integration of the closed-form MP density f(x) = √((λ₊−x)(x−λ₋))/(2πγ_iσ²x) on [λ₋, λ₊] with σ²=1. The executing lane implements this equation verbatim; any deviation voids the inference.
- σ̂²_{i,l} = median(λ_1,…,λ_{n_i}) / m_MP(γ_i).
- MP bulk edge: λ₊(γ_i, σ̂²_{i,l}) = σ̂²_{i,l}·(1 + √(γ_i))².
- **Signal-eigenvalue count:** s_{i,l} := #{λ_j > λ₊(γ_i, σ̂²_{i,l})}.
- **Bulk-fit diagnostic (C1 — reported, not binding):** for each (item, layer), the Kolmogorov–Smirnov distance between the empirical eigenvalue CDF and the fitted MP CDF over the bulk; report the median across all pairs; flag "bulk-fit poor" if median KS > **0.15** (design parameter). A poor fit is visible in the record, never silent.

**Per-item statistic (C1 — max-inside-permutation, one sentence).** s_i := max_{l=1…24} s_{i,l}; the max-over-layers transformation is computed identically for every item inside every permutation — only the correct/failed labels are shuffled, so there is no multiple-comparisons inflation.

**n_i measurement-validity guard (C2 — pinned).** N_MIN = **40** (design parameter). Items with n_i < 40 are excluded from the primary test; the excluded count is a reported diagnostic. If fewer than **30** items remain, the pilot reports **HELD with reason** ("insufficient positions for stable spectra") — never KILL. The run record reports the n_i distribution (median, IQR, range, count below floor) regardless of outcome.

**Grouping.** Items are correct/failed per the baseline's answers from the committed EXP140 B0 records (correctness from bench labels — see §5 for the Law #7 statement).

**Secondary diagnostics (reported, not binding).** (a) The l_c transition rule from the J3 sketch (≥3 new outliers sustained 2 layers): distribution of l_c existence/position across groups. (b) Per-layer version of the primary test (which layers carry the difference, if any). (c) The same test on the mean difference (sensitive to tail items).

---

## 3. Stage-1: CPU observational pilot — procedure, validity gates, inference (C4)

**Items.** All 60 items, canonical bench order, view 0. **60 forward passes** with hidden-state capture (§2 construction), CPU, $0, ~1h (EXP139 60/60 CPU precedent for the forwards; the 1440 eigendecompositions are negligible next to them).

**Validity gates (C4 — all must pass, else the pilot is VOID → HELD with reason, never a verdict):** (a) bench sha256 matches; (b) backbone pre-hash matches BACKBONE_PIN; (c) post-run backbone hash matches the pin (Δθ=0); (d) 60/60 passes complete; (e) determinism spot-check: re-run 3 items, byte-identical s_{i,l} vectors.

**Primary inference (binding).**
- Statistic: Δ_s = median(s_correct) − median(s_failed), n_c + n_f = 60 (after the C2 guard; the guard's exclusions are reported).
- Test: one-sided permutation test, **100,000 permutations**, seed **S_PERM = 20261010** (pinned; Law #13 — no seed chosen at runtime). Shuffle only the correct/failed labels; recompute Δ_s identically each permutation (max-inside-permutation per §2). p = fraction of permuted Δ_s ≥ observed Δ_s.
- Licensed direction: Δ_s > 0 (correct items show more signal eigenvalues).
- **Wrong-direction behavior (verified by the design review §3):** if the true effect is wrong-direction and large, p ≈ 1 ≥ 0.05 → KILL. The bias-coherence counter-argument (failed items more spectral) is collected by the instrument.

**Falsification tree (binding; precedence KILL > CONTINUE > HELD).**

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | p < 0.05 **and** Δ_s ≥ 2 | The RMT lens sees a correctness-signed spectral signal. Licenses a NEW worth-it gate for the spectral intervention (new number) — not a capability claim, not integration. |
| KILL (observational) | p ≥ 0.05 | The RMT lens sees nothing → the spectral-lens family is dead. Intervention never attempted (pre-registered sequencing). (Binding bar from backlog row 25.) |
| HELD (a) | p < 0.05 but Δ_s < 2 | Significant but below the candidate's magnitude bar — licenses nothing, kills nothing. |
| HELD (b) | C2 guard fires (<30 items with n_i ≥ 40) | Measurement-invalid — licenses nothing, kills nothing. |
| HELD (c) | Stage-1 unrun, infeasible, or any validity gate fails | Screen VOID. Licenses nothing, kills nothing. |

Every (p, Δ_s) region maps to exactly one branch. No PIVOT is licensed by the backlog row; none is invented.

**Stage-1 cost:** 60 passes + 1440 Gram eigendecompositions ≈ **1h CPU, $0** (this machine). Storage: per-layer Grams accumulated on the fly (§2 memory discipline).

---

## 4. Intervention stage — NOT licensed here

If Stage-1 CONTINUEs, a **new** worth-it gate designs the spectral intervention (amplify the top-signal-PC at l_c; the J3 sketch's proposal), with its own Law #14 review, pre-registration, CEO GPU clearance, and founder Kaggle slot (costed <0.01 T4-h by analogy with the backlog row). The Law #14 reviewer of that gate is explicitly tasked with ruling whether data-driven spectral amplification is distinct from the killed directional program. **Nothing about intervention is pre-licensed by this document.**

---

## 5. Law #7 boundary

This is a purely observational test: there is no candidate score, no selection, no trigger, no revision, no ranking. Bench labels define the correct/failed groups in the primary permutation test — that *is* the validation. **No label sees anything beyond the pre-registered grouping**; the σ̂² estimator, the MP edge, the s_{i,l} counts, and the s_i statistic are all computed label-blind. The permutation seed is fixed, not chosen at runtime. The firewall is trivially intact because there is nothing labels could leak into beyond the grouping.

---

## 6. Citation verification (C3) and prior art

All verifications below were performed 2026-10-03 at the pre-reg drafting stage. Nothing is marked verified that is not.

- **Martin & Mahoney, "Implicit Self-Regularization in Deep Neural Networks: Evidence from Random Matrix Theory and Implications for Learning," JMLR 22(165):1−73, 2021 (arXiv:1810.01075) — VERIFIED real** (JMLR page and arXiv abstract checked 2026-10-03). RMT analysis of DNN weight matrices: the empirical spectral density shows an MP-conforming bulk with signal outliers; training exhibits 5+1 phases of increasing implicit self-regularization (bulk-MP → heavy-tailed). **Closest methodological prior art** (the MP-bulk-plus-outliers counting rule is inherited). Distinctions: (a) their object is *weight* matrices (static, post-training); S4-7's object is *activation* covariances at inference time; (b) they correlate spectra with generalization across models/training stages; S4-7 correlates per-item spectra with per-item correctness within one frozen model.
- **Papyan, Han & Donoho, "Prevalence of Neural Collapse during the terminal phase of deep learning training," PNAS 117(40):24652–24663, 2020 (arXiv:2008.08186) — VERIFIED real** (arXiv and PNAS/NSF records checked 2026-10-03). Terminal-phase training geometry: (NC1) within-class activation variability → 0, (NC2) class means → simplex ETF, (NC3) classifiers → class means, (NC4) nearest-class-center decision rule. **Conceptual prior art** for "coherence has a spectral signature." Distinctions: (a) a *training-time* phenomenon; S4-7 is inference-time; (b) about class structure, not per-item correctness.
- **Aghajanyan, Zettlemoyer & Gupta, "Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning," ACL 2021 (arXiv:2012.13255) — VERIFIED real** (arXiv and ACL Anthology checked 2026-10-03). Fine-tuning lives in a low-dimensional reparameterization (e.g., 200 trainable parameters → 90% of RoBERTa's MRPC performance); pre-training minimizes intrinsic dimension. **Adjacent** but distinct: parameter-space vs activation-space, fine-tuning vs inference.
- **NEW PRIOR ART (updates the design's honest negative): Ettori (2026), "Spectral Geometry for Deep Learning: Compression and Hallucination Detection via Random Matrix Theory," UIC master's thesis (arXiv:2601.17357v1) — VERIFIED real** (arXiv HTML read 2026-10-03). EigenTrack: real-time hallucination/OOD detection in LLMs/VLMs by converting streaming hidden activations into spectral signatures (entropy, eigenvalue gaps, divergence from the MP baseline) modeled with lightweight recurrent classifiers. The design's "no per-item inference-time MP prior art found" is therefore **superseded**: per-item inference-time MP spectral analysis for reliability now has prior art. Distinctions: (a) EigenTrack *trains* recurrent classifiers on spectral features — S4-7 is training-free MP counting + a label permutation test; (b) their target is hallucination/OOD detection; S4-7's is correctness-grouped signal-eigenvalue counts with binding KILL/CONTINUE/HELD bars on a fixed decision bench/backbone; (c) a master's thesis, not peer-reviewed. The specific construction here (MP-outlier counting + one-sided label permutation test on Δ_s with the backlog's bars) remains unclaimed as far as the search shows.
- **Result (iv) vs (viii) of the audit, restated:** the S4-7 question is observational and falsification-first; the intervention sharp edge is deferred to its own gate.

**Novelty read: N1 (known combination)** — MP spectral analysis is established (Martin & Mahoney; now also EigenTrack for inference-time reliability). The differentiators are the training-free counting rule, the correctness-grouped permutation test with binding bars, and the explicit sequencing (intervention never attempted on a null). The draft claims none of the prior art's territory and cites it.

---

## 7. Expectation calibration

**Modal outcome: KILL.** The honest prior is against the signal: four internal-signal failures on this bench family (TESTA anti-calibrated margin; EXP140 null free energy; EXP141 killed self-model; EXP125 killed honesty self-report) all point the same way, and the MP null is a counting rule over activations that were never trained to be spectrally informative about correctness. The pilot's expected value is the cheap falsification of the last J-tier line at $0 — **boundary science on this bench/backbone, not a novelty claim and not an intervention claim**. A CONTINUE would be genuinely surprising precisely because the prior is against it; it remains a long shot, priced not hidden. If the null lands, the program will have established that *no* internal correctness-signed signal exists on this bench family across five distinct families — margin, free energy, self-model, honesty-report, spectrum — which constrains where the missing ingredient can be (not in the frozen model's internals as probed; cf. the Percepta Spotlight architectural framing logged 2026-10-03).

---

## 8. Risks and honest limitations

1. **Honest prior against the signal** (§7): the measurement is built to kill cheaply.
2. **The MP null is a counting rule, not a true model** (§2): activations are not iid noise. The σ̂² bulk-median fit absorbs some misspecification, but a bad fit could systematically bias counts — the bulk-fit diagnostic (C1) makes fit failure visible, never silent.
3. **The bias-coherence counter-argument** (design §1, §9.3): the position bias may itself be the coherent low-rank component, making failed items *more* spectral. The licensed direction could be exactly backwards — the one-sided construction kills on this (p ≈ 1), by design.
4. **n_i vs d:** with short prompts the covariance estimate is noisy and the MP asymptotics shaky — the C2 guard pre-registers HELD-with-reason instead of a spurious KILL.
5. **The intervention sharp edge** (§1): amplifying the top-signal-PC is directional manipulation. The observational license does not launder it; the intervention gate must face the killed-lanes audit directly.
6. **Bench specificity:** all bars are on the 60-item decision bench at Pythia-410m, view 0. No claim about other benches/backbones is licensed under any branch.
7. **Prior-art movement:** the EigenTrack thesis (2026) shows the spectral-reliability territory is active; the pre-reg-stage search should be re-run before any paper use.

---

## Appendix A. Condition-closure checklist (for the next Law #14 reviewer)

- [ ] C1: §2 pins the σ̂² estimator (bulk-median fit against the theoretical MP median at γ_i, numerical integration of the closed-form MP density) + the bulk-fit diagnostic (median KS distance, reported not binding, flag threshold 0.15); the max-inside-permutation construction is stated explicitly (one sentence, §2).
- [ ] C2: §2 pins N_MIN = 40 with the exclusion diagnostic; <30 remaining items → HELD with reason, never KILL; the n_i distribution is reported in the run record.
- [ ] C3: §6 verifies Martin & Mahoney (JMLR 2021), neural collapse (PNAS 2020), intrinsic dimensionality (ACL 2021) at full-text/abstract level; the Ettori (2026) thesis is reported as new prior art updating the design's honest negative; nothing marked verified that is not.
- [ ] C4: §3 validity gates — determinism check, backbone pre/post hash (Δθ=0), bench hash, 60/60 pass completion.
- [ ] C5: §1 cites the Friday cull as LOG-4879 (not LOG-4889/LOG-4879).
- [ ] Seeds pinned: S_PERM = 20261010 (100,000-permutation primary test). No seed chosen at runtime. (No sampling anywhere — all forwards are deterministic.)
- [ ] Pins: §2 backbone pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` and bench pin `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`, both verified against the committed EXP141 Stage-1 records (2026-10-03).
- [ ] Baseline-source decision pinned: reuse of committed EXP140 B0 records (§1).
- [ ] Precedence KILL > CONTINUE > HELD; no PIVOT invented; HELD coverage complete (guards + VOID).
- [ ] No experiment number minted in this draft (minted only at pre-reg SIGN).
