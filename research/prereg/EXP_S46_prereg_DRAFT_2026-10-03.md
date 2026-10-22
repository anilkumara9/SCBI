# S4-6 (J2) Metacognitive Self-Modeling — Pre-registration DRAFT (UNSIGNED)

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. Licenses nothing. No run is authorized by this document.*
*Before any execution: independent Law #14 review of this exact draft + CEO approval. Stage 2 additionally requires the founder's Kaggle GPU.*
*No experiment number is minted in this draft. The number is minted by the CEO only at pre-registration SIGN (after independent Law #14 review + CEO approval), and must be verified free in the research log and backlog before minting.*
*Licensing chain: LOG-288 (S4-6/J2 born, QUEUED as backlog row 24, 2026-09-24) → LOG-4879 (Friday cull option (b): redirect to surviving J-tier lines) → LOG-4883 (G/E/S loop family stood down) → LOG-4888 (S4-5/EXP140 stood down at Stage-1 with G3 calibration NULL; J-tier queue continues) → `research/innovation/S46_DESIGN_2026-10-03.md` (worth-it gate, verdict CONDITIONAL RUN) → `research/innovation/S46_DESIGN_REVIEW_2026-10-03.md` (independent Law #14 review, APPROVE-WITH-CONDITIONS C1–C3) → this draft.*
*Governing laws: Law #2 (no invented numbers), Law #3 (no fabricated citations), Law #4 (bars binding, no post-hoc shifts), Law #6 (Δθ=0), Law #7 (labels touch bench evaluation and the calibration instrument only — §7), Law #9 (metrics before inspection), Law #11 (observation vs interpretation), Law #13 (deterministic reproducibility), Law #15 (this document is the binding gate).*
*Epistemological labels per `AGENTS.md` §5 used throughout. $0 compute for this document.*

---

## 0. Law #15 block (binding)

**Precise question [HYPOTHESIS].** On the 60-item decision bench, does the frozen Pythia-410m model's P(True) self-evaluation â_self of its own baseline answers carry correctness information (I(â_self; correctness) > 0), and does revising only the answers the self-model flags as likely-wrong (â_self_i < 0.5) rescue decisions beyond the baseline and beyond random revision?

**Decision it changes.** **KILL (self-model)** if the Stage-1 I-screen is null (permutation p ≥ 0.05) — the self-modeling family is dead before any revision spend. **KILL (calibration)** if the Stage-1 calibration gate is significantly inverted — â_self is an anti-signal. **KILL (revision)** if Stage-2 ΔM_trig ≤ ΔM_rand — the discrepancy trigger carries no signal beyond resampling. **PIVOT** if I > 0 (I-screen passes) but ΔM_trig ≤ 0 — the signal is real but useless for revision → re-scope to diagnostic use only (never a revision trigger). **CONTINUE** (licensed positive only) if G1–G3 pass and ΔM_trig ≥ +8pp with Newcombe paired 95% LCI > 0.05 **and** ΔM_trig > ΔM_rand (paired one-sided p < 0.05) — licenses a follow-on (new number) on the self-model mechanism, not an integration claim. **HELD** in the pre-registered intermediate/unrun cases (§5) — licenses nothing, kills nothing. Exactly one branch will be earned; precedence **KILL (any) > PIVOT > CONTINUE > HELD** (PIVOT is reachable — see §5; it is not demoted).

**Cheapest falsifying test.** Stage-1 CPU pilot: 60 self-eval forward passes (baseline answers reused from committed EXP140 B0 records), $0 CPU, ~15–30 min (EXP139 60/60 CPU precedent) — carries three binding gates (G1 signal variance, G2 I-screen, G3 calibration). The pilot exists to kill, not to confirm: the honest prior is against the signal (§9).

**Quantitative predictions (pre-registered bars).** G1: std(â_self) > 0.01, non-constant. G2: I(â_self; c) > 0, 4-bin equal-frequency MI + Miller-Madow, permutation p < 0.05 (100,000 permutations, seed 20261007). G3: C1 Spearman(â_self, per-item accuracy) positive, one-sided p < 0.05 **and** C2 TESTA-style partition mean(â_self|baseline-wrong) < mean(â_self|baseline-right), one-sided permutation p < 0.05 (100,000 permutations, seed 20261008). Stage-2: ΔM_trig ≥ +8pp with Newcombe paired 95% LCI > 0.05 **and** ΔM_trig > ΔM_rand (paired one-sided McNemar-exact p < 0.05).

**Breaking points (sharp).** G2 null (p ≥ 0.05) → **KILL the self-modeling family before revision** (the backlog's bar). G3 either-null → no GPU (HELD, family stands down — the signal may be absent rather than anti-informative). G3 either-inverted (wrong-direction one-sided p < 0.05) → **KILL the self-modeling family outright**. Stage-2 ΔM_trig ≤ ΔM_rand → **KILL revision**. ΔM_trig ≤ 0 despite I > 0 → **PIVOT to diagnostic**. Trigger fires on <15 items → revision test VOID (HELD with reason). Any validity gate in §3 fails → screen VOID (HELD with reason, never a verdict on the hypothesis).

**The belief it tests (named).** "Self-modeling (a consciousness prerequisite) is absent in frozen models at inference time" → "the frozen model's P(True) self-evaluation carries correctness information usable for discrepancy-driven revision, with no labels and no training." [INTERPRETATION]

---

## 1. Background, license, and condition-closure checklist

- **S4-6/J2** (backlog row 24, QUEUED since LOG-288): "Does the frozen model model itself usefully (I > 0), and does discrepancy-driven revision rescue?" — L2-aimed summit tier, the most summit-direct question in the queue.
- **Design** (`S46_DESIGN_2026-10-03.md`): worth-it gate, verdict CONDITIONAL RUN. **Independent Law #14 review** (`S46_DESIGN_REVIEW_2026-10-03.md`): APPROVE-WITH-CONDITIONS C1–C3. This draft closes each condition; the closure is itemized here so the next reviewer can check it mechanically:
  - **C1** — EXP125 characterization corrected → this section and §6(v): EXP125 (LOG-4680, H22/HONESTY-GEN4) killed a **first-token logit-readout honesty self-report** (fidelity 28/60 vs the registered cosine-argmax decision statistic), bench-specific per LOG-4680/Law #8 — **not** "verbalized" self-report. The "verbalized vs distributional" framing appears nowhere in this draft. The non-resurrection rests on the reviewer's four correct grounds: (a) different property (honesty-fidelity vs correctness-informativeness), (b) different ground truth (decision statistic vs bench labels), (c) EXP125's kill was bench-specific, (d) Kadavath et al. 2022 provides an independent empirical anchor EXP125 never had. The corrected distinction is sufficient per the review (§1 ruling).
  - **C2** — revision mechanics pinned → §2: revision decoding is **GREEDY** (matching the baseline ŷ_i); minimum triggered-item count **15** (25% of the bench, pre-registered design parameter); if the trigger fires on <15 items, the revision test is **VOID** → HELD with reason ("trigger-rate floor not met"), never a verdict.
  - **C3** — full-text verification → §8: Kamoi et al. (TACL 2024, 2024.tacl-1.78) **VERIFIED real** via ACL Anthology (full abstract + metadata checked; characterization accurate: no prior work demonstrates successful self-correction with feedback from prompted LLMs except exceptionally suited tasks; works with reliable external feedback; large-scale fine-tuning enables it); Xu et al. ("Pride and Prejudice," ACL 2024, 2024.acl-long.826, arXiv:2402.11436) **VERIFIED real** at full-text level (PDF fetched and read 2026-10-03: self-bias formally defined as the tendency to favor own generation, prevalent across six LLMs, amplified by the self-refine pipeline; matches the design's self-bias-confound characterization). Nothing is marked verified that is not.
- **[MECHANICAL CLARIFICATION — for the Law #14 reviewer]** The design's §5 C2 carries TESTA's "majority-wrong/right" language, which presupposes per-item multiple views. S4-6 contributes **one baseline answer per item** (binary correctness). This draft resolves C2 to the faithful adaptation: mean(â_self | baseline-wrong items) < mean(â_self | baseline-right items), one-sided permutation. The licensed direction (higher â_self ↔ higher accuracy) is unchanged; this is a transcription-level clarification, not a bar change. The reviewer should confirm.
- **Non-resurrection [FACT].** S4-6 injects no direction (vs killed static-geometry lanes), makes no loop claim (vs stood-down G/E/S, LOG-4883), uses no vote (vs EXP114 POE — the order-swap is a revision framing, never a vote), revives no culled probe set, and (per C1) tests correctness-informativeness against bench labels, not honesty-fidelity against a decision statistic (vs EXP125, LOG-4680). Vs S4-5/EXP140: different signal family (metacognitive judgment about a fixed answer vs trajectory-integrated surprise density); EXP140's G3-null does not transfer — the informativeness question is re-tested from scratch. Every kill stands; nothing killed is re-tested.
- **Baseline-source decision [FACT].** This draft **REUSES** the committed EXP140 B0 records (`experiments/runs/EXP140_stage1/stage1_records.json`) as ŷ_i — legitimate per the review (§7): committed, deterministic, byte-identical on re-run per EXP140's gate (c). Stage-1 = **60 self-eval passes** (no baseline regeneration). Budget held constant either way (≤120 passes); the reuse-vs-regenerate choice is pinned here, not left to the executing lane.

---

## 2. Self-eval construction + revision mechanics (C1–C2 — fully pinned)

**Model [FACT].** EleutherAI/pythia-410m, local HF cache revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` (the LOG-331 pin), 24 layers, d=1024, vocab 50304, `tie_word_embeddings: false` (verified from the cached `config.json` in the EXP139 pre-reg, 2026-10-03). Load via `AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=HF_REVISION, local_files_only=True, torch_dtype=torch.float32, device_map="cpu")` — float32 to match the committed records. **Backbone pin:** sha256 of the state dict must equal `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (verified against the committed EXP140 Stage-1 records `experiments/runs/EXP140_stage1/stage1_records.json`, 2026-10-03); mismatch → run VOID. Δθ=0 throughout: `model.eval()`, `torch.no_grad()`; post-run backbone hash must match the pin.

**Bench [FACT].** The 60-item decision bench reconstructed deterministically from `experiments/runs/EXP135_eval/run_exp135.py` (`build_bench`, `make_views`, `tok1`); `bench_sha256` must equal `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` (verified against the committed EXP140 Stage-1 records, 2026-10-03). Reconstruction mismatch → run VOID. All 60 items in canonical bench order, **view 0** (deterministic, pre-registered; no label-based item selection).

**Self-evaluation instrument [DEFINITION].** For item i with baseline answer ŷ_i (from the committed EXP140 B0 records, greedy decode on the view-0 prompt):
- Self-eval prompt (fixed, identical for all items):
  `<view-0 item prompt> Proposed answer: ŷ_i. Is the proposed answer correct? (A) True (B) False`
  where ŷ_i is rendered as the decoded answer text ("A" or "C" as presented in the view-0 prompt).
- **â_self_i := P_θ(token "A" | self-eval prompt)** — the model's assigned probability to the single "True" token, computed in one teacher-forced forward pass. A single scalar per item; 60 values.
- **No self-eval sampling seed is needed** (teacher-forced, deterministic). Law #13: nothing chosen at runtime.

**I-screen instrument [DEFINITION].**
- Discretize â_self into **4 equal-frequency bins** over the 60 items (~15 items/bin, pre-registered).
- **Î := I_naive(â_bin; c) + (4−1)(2−1)/(2·60) = I_naive + 0.025 nats** (Miller-Madow bias correction; c ∈ {0,1} is baseline-answer correctness per bench labels — **labels touch only this instrument and the G3 instrument**).
- **Permutation test:** 100,000 permutations of c (seed **S_PERM_G2 = 20261007**, pinned); p = fraction of permuted Î_MM ≥ observed Î_MM. One-sided in the licensed direction (I > 0).
- **Bar:** p < 0.05 → G2 passes. p ≥ 0.05 → **KILL the self-modeling family before revision** (the backlog's bar, binding).
- **Secondary instruments (reported, not binding):** AUC of â_self as a correctness classifier (DeLong 95% CI); Spearman(â_self, per-item accuracy) one-sided positive.

**Discrepancy trigger [DEFINITION].**
- **Trigger:** revise item i iff **â_self_i < τ_rev**, τ_rev = **0.5** (pre-registered design parameter — the self-model predicts its own answer is wrong; threshold fixed, never tuned on labels).
- **Trigger-rate floor (C2b):** the revision test is valid only if **≥15 items** trigger. Fewer than 15 → revision test **VOID** → HELD with reason ("trigger-rate floor not met"). The floor is a pre-registered design parameter, not derived from data.
- **Revision (C2a — pinned):** on trigger, regenerate the answer under the **order-swapped framing** (the two option texts exchanged in place in the view-0 prompt; semantic label mapping preserved: A = correct, readout unchanged), **GREEDY decoding** (matching the baseline ŷ_i). The revised answer replaces the baseline for triggered items only.
- **Degenerate handling:** if the self-eval forward for an item produces â_self_i ∈ {0, 1} exactly, it is kept (a value, not an error); if a forward fails (0 items expected), the item is excluded from G2/G3 with a diagnostic count; ≥3 failed self-evals → pilot VOID.

**Revision controls (pre-registered; the EXP140 resampling lesson).**
- **Revise-all:** regenerate every item under order-swap, greedy, ignoring the trigger. Isolates the *trigger* from reframing.
- **Random-trigger:** revise a random subset of the same size as the triggered set (seed **S_RANDTRIG = 20261009**, pinned; if the triggered set size is 0 — impossible, since <15 is VOID — skip). Isolates the trigger's *information* from resampling.
- **Endpoints (pre-registered):** ΔM_trig = acc(trigger-revised) − acc(baseline); ΔM_all; ΔM_rand — accuracies over all 60 items (revised answers replace baseline for revised items only). ΔM_trig > ΔM_rand is tested by a paired one-sided McNemar-exact test on the (trigger-revised, random-revised) 2×2 table (b' = #{trigger right, random wrong}, c' = #{trigger wrong, random right}), p < 0.05.
- **Stage-2 cost:** 60 items × (trigger-thresholded revision + revise-all + random-trigger) ≤ **180 passes** (backlog row 24), <0.01 T4-h, founder-gated.

---

## 3. Stage-1: CPU pilot — I-screen + calibration gates (binding)

**Items.** All 60 items, canonical bench order, view 0. **60 self-eval forward passes** (baseline answers reused from the committed EXP140 B0 records, §1 decision), CPU, $0, ~15–30 min (EXP139 60/60 CPU precedent).

**Validity gates** (all must pass, else the pilot is VOID → HELD with reason, never a verdict): (a) bench sha256 matches; (b) backbone pre-hash matches BACKBONE_PIN; (c) baseline-answer reuse fidelity: committed B0 answers byte-identical to the executing lane's re-read (no regeneration — read, don't recompute); (d) post-run backbone hash matches the pin (Δθ=0).

**Binding gates** (all three must pass in the licensed direction or Stage 2 does not run):
- **G1 signal-variance:** std(â_self) > **0.01** (design parameter) and the 60 values are not all identical. Catches the Xu et al. self-bias confound (model rates everything highly → constant signal → vacuous self-model).
- **G2 I-screen:** I(â_self; c) > 0 with permutation p < 0.05 (seed 20261007). Null → **KILL the self-modeling family before revision** (the backlog's bar — no revision stage runs).
- **G3 calibration** (the TESTA burden): â_self must predict correctness in the licensed direction. Instrument: per-item â_self (the *signal*; the trigger threshold τ_rev is fixed, never tuned); per-item correctness from bench labels (**labels touch only this instrument**). Pre-registered tests, one-sided in the licensed direction (higher â_self ↔ higher accuracy):
  - **C1:** Spearman(â_self, per-item accuracy), one-sided p < 0.05, **positive** direction. (Mirrors TESTA's R3 with the sign in the licensed direction.)
  - **C2:** TESTA-style partition — mean(â_self | baseline-wrong items) **<** mean(â_self | baseline-right items), one-sided permutation test (100,000 permutations, **seed 20261008** pinned), p < 0.05. (Adapts TESTA's R2/C2 to the single-answer-per-item bench; see the §1 mechanical clarification.)
- **G3 gate logic (binding):** C1 and C2 **both** pass in the licensed direction → G3 passes → Stage-2 gate opens (still needs CEO venue approval + founder GPU + signed pre-reg). **Either null → G3 fails → no GPU** (family stands down, not killed — the signal may be absent rather than anti-informative → HELD with reason). **Either significantly inverted (wrong-direction one-sided p < 0.05) → KILL the self-modeling family outright** — â_self carries the TESTA pathology in metacognitive form.
- **Gate/verdict linkage (explicit per the review §5):** PIVOT and every Stage-2 branch require Stage 2 to have run, which requires G1–G3 all passing. G2-null kills before revision; G3-null stands the family down (no verdict on revision).

---

## 4. Stage-2: GPU revision test (only if G1–G3 pass; founder-gated)

**Procedure.** §2 mechanics on the founder's Kaggle queue: trigger-thresholded revision + revise-all control + random-trigger control, greedy decoding, ≤180 passes, ≈ **<0.01 T4-h** (backlog row 24). Endpoints ΔM_trig, ΔM_all, ΔM_rand as §2. Inference per §6.

**Bars.** CONTINUE: ΔM_trig ≥ **+8pp** with Newcombe paired 95% LCI > 0.05 **and** ΔM_trig > ΔM_rand (paired one-sided McNemar-exact p < 0.05). KILL (revision): ΔM_trig ≤ ΔM_rand. PIVOT: I-screen passes but ΔM_trig ≤ 0 (signal real, revision useless → diagnostic re-scope).

**Licensing.** Stage 2 runs **only** if: (i) G1–G3 all pass in the licensed direction on the signed Stage-1 record; (ii) this pre-registration is Law #14-signed; (iii) CEO issues GPU venue clearance; (iv) the founder provides the Kaggle queue slot. This draft assumes nothing about venue availability.

---

## 5. Falsification tree (precedence KILL (any) > PIVOT > CONTINUE > HELD)

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | G1–G3 pass **and** ΔM_trig ≥ +8pp with Newcombe LCI > 0.05 **and** ΔM_trig > ΔM_rand (p < 0.05) | Discrepancy-driven revision carries signal beyond reframing and beyond resampling. Licenses a follow-on (new number) on the self-model mechanism. |
| KILL (self-model) | G2 null (permutation p ≥ 0.05) | No correctness information in the self-model → the family is dead before revision. (Binding bar from backlog row 24.) |
| KILL (calibration) | G3 either-inverted (wrong-direction p < 0.05) | â_self is an anti-signal — the TESTA pathology in metacognitive form → the family is dead. |
| KILL (revision) | Stage-2 ΔM_trig ≤ ΔM_rand | The discrepancy trigger carries no signal beyond resampling → discrepancy-driven revision is dead. |
| PIVOT | I-screen passes **and** ΔM_trig ≤ 0 | The signal is real but useless for revision — re-scope to diagnostic use only (never a revision trigger). **Reachable:** when ΔM_rand < ΔM_trig ≤ 0 (random revision hurts more than triggered revision, but triggered revision still doesn't help), PIVOT fires without KILL (revision) tripping first. Non-empty region — the branch is live. |
| HELD (a) | G1 fails | Signal degenerate — apparatus/screen finding, not a verdict on the hypothesis. |
| HELD (b) | G2–G3 either-null | Signal absent, not anti-informative. Family stands down; licenses nothing, kills nothing. |
| HELD (c) | Stage-2 0 < ΔM_trig < +8pp, or Δ̂ ≥ +8pp with LCI straddling 0.05, or ΔM_trig > ΔM_rand numerically with paired p ≥ 0.05 | Positive ΔM_trig failing either the Newcombe magnitude bar or the paired-significance bar — licenses nothing, kills nothing. |
| HELD (d) | ΔM_trig ≥ +8pp but ΔM_trig ≤ ΔM_rand | A gain that doesn't beat resampling is not the candidate's claim (precedence: KILL revision). |
| HELD (e) | Stage-1 unrun, infeasible, trigger-rate floor not met (<15 triggered), or any validity gate fails | Screen VOID. Licenses nothing, kills nothing. |

Every region of (I, ΔM_trig, ΔM_rand, LCI) space maps to exactly one verdict under the stated precedence — PIVOT is reachable (per the review's §5 case-table walk), and the HELD coverage includes the numerical-superiority-with-p≥0.05 case (the S4-5 F2 lesson).

---

## 6. Inference: Newcombe paired interval (explicit construction — no software invented)

For n=60 paired items (revision test): b = #{baseline wrong, revised right}, c = #{baseline right, revised wrong}, Δ̂ = (b−c)/n.
- Wilson 95% interval (z=1.96, **no continuity correction**) for p̂_b = b/n → (l_b, u_b), and for p̂_c = c/n → (l_c, u_c), each clipped to [0,1]:
  center = (p̂ + z²/2n)/(1 + z²/n); half = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n).
- L = Δ̂ − √((p̂_b − l_b)² + (u_c − p̂_c)²); U = Δ̂ + √((u_b − p̂_b)² + (p̂_c − l_c)²).
- **Binding bar:** Δ̂ ≥ 0.08 **and** L > 0.05.
- Secondary (reported, not binding): McNemar-exact two-sided p on the 2×2 table.
The executing lane implements these equations verbatim and archives the code; any deviation voids the inference.

---

## 7. Law #7 boundary

Labels (correct answers) are used **only** for bench evaluation — computing accuracy, ΔM, the paired tables — and for the G2 I-screen instrument (correctness c for mutual information) and the G3 calibration instrument (per-item correctness for Spearman/partition validation). **No self-eval score, no trigger, no revision, no gate threshold sees labels.** G1 uses no labels; G2/G3 thresholds (p < 0.05, licensed direction) are fixed here, never tuned on labels. The trigger threshold τ_rev = 0.5 is a design parameter, fixed before any label contact. The κ̂-style structural firewall holds: â_self is computable with labels absent. The permutation seeds are fixed, not chosen at runtime.

---

## 8. Citation verification (C3) and prior art

All verifications below were performed 2026-10-03 at the pre-reg drafting stage. The three primary citations are verified at full-text or API level; nothing is marked verified that is not.

- **Kadavath et al. 2022, "Language Models (Mostly) Know What They Know," arXiv:2207.05221 — VERIFIED real** (independently verified by the Law #14 design review via arXiv API, 2026-10-03). P(True) self-evaluation of own samples; a partially distinct skill from answering (one-shot "is this true?" performs worse); calibration format-dependent and scale-sensitive; RLHF policies miscalibrated; P(IK) head required training. **Closest prior art for the I-screen.** Distinctions: (a) their models run to 52B — S4-6 tests whether any of the signature survives at 410M frozen; (b) their P(IK) head required training — S4-6 is training-free; (c) they did not test discrepancy-driven revision — the second stage is S4-6's novel element.
- **Madaan et al. 2023, "Self-Refine: Iterative Refinement with Self-Feedback," NeurIPS 2023, arXiv:2303.17651 — VERIFIED real** (independently verified by the Law #14 design review via arXiv API, 2026-10-03). Generate → self-feedback → refine loop with one frozen model; ~20% average improvement across 7 tasks. **Closest prior art for the revision stage.** Distinctions: (a) their feedback is free-form natural-language critique; S4-6's revision is *discrepancy-triggered* (revise only where the self-model disagrees) with matched resampling controls; (b) their tasks are generative — S4-6 tests decision rescue on a fixed bench with binding bars.
- **Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet," ICLR 2024, arXiv:2310.01798 — VERIFIED real** (independently verified by the Law #14 design review via six independent secondary sources, 2026-10-03; arXiv API rate-limited at review time). Intrinsic self-correction fails and often degrades reasoning without external feedback; part of Self-Refine's gains traced to prompt-design artifacts. **The boundary this design must respect.** S4-6's answer: the discrepancy trigger is *not* free-form self-correction — it is a gated revision licensed only if the I-screen first establishes that the self-model carries information. If the I-screen is null, no revision runs — the design concedes Huang's point by construction.
- **Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs," TACL vol. 12, 2024, pp. 1417–1440 — VERIFIED real** (ACL Anthology ID 2024.tacl-1.78, DOI 10.1162/tacl_a_00713; abstract and metadata checked 2026-10-03). Findings: (1) no prior work demonstrates successful self-correction with feedback from prompted LLMs, except tasks exceptionally suited; (2) self-correction works well with reliable external feedback; (3) large-scale fine-tuning enables self-correction. Consistent with the design's characterization ("prompt-only self-correction does not work in fair settings; works with reliable external feedback") and its gating structure.
- **Xu et al., "Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement," ACL 2024, 2024.acl-long.826, arXiv:2402.11436 — VERIFIED real** at full-text level (PDF fetched and read 2026-10-03). Formally defines LLM self-bias — the tendency to favor its own generation — via two statistics; finds self-bias prevalent across six LLMs (GPT-4, GPT-3.5, Gemini, LLaMA2, Mixtral, DeepSeek) on translation, constrained generation, and math; the self-refine pipeline amplifies self-bias while improving fluency. Matches the design's characterization ("self-bias confound: models rate their own output higher"). The G1 variance gate and the trigger-rate diagnostic observe this confound; the bars self-correct.

**Novelty read: N1 (known combination)** — P(True)-style self-evaluation and self-refinement loops both have prior art. The differentiators are the discrepancy-triggered (rather than blanket) revision with matched resampling controls, the falsification-first I-screen that kills before revision, and the pre-registered calibration gate on this bench/backbone. The draft claims none of the prior art's territory and cites it.

---

## 9. Expectation calibration

**Modal outcome: G2-null or a clean kill.** The honest prior is against the signal: TESTA (anti-calibrated margin), EXP140 (null free energy), EXP125 (dead honesty self-report on its bench), Huang et al. (intrinsic self-correction fails at frontier scale), Kamoi (no successful prompt-only self-correction in fair settings) — and Kadavath's existence proof is at 52B, two orders of magnitude above 410M. The pilot's expected value is the cheap falsification of the metacognitive family at $0 — **boundary science on this bench/backbone, not a novelty claim and not a revision claim**. A G2 pass would be genuinely surprising precisely because the prior is against it; CONTINUE remains a long shot, priced not hidden. The program's most summit-direct question gets answered either way.

---

## 10. Risks and honest limitations

1. **Honest prior against the signal** (§9): the inversion/absence risk is the point of G2/G3, not an afterthought.
2. **Self-bias confound (Xu et al.):** the model may rate its own answers highly across the board → â_self has no variance → G1 catches it, trigger never fires, I-screen is vacuous. The gates observe this; they do not patch it.
3. **The EXP125-distinction is now correctly stated (C1)** — the residual risk is empirical (â_self may simply fail the I-screen), not categorical.
4. **Elicitation shift:** the self-eval prompt changes the decision context; â_self is comparable across items but absolute values are prompt-dependent. The bars use only relative informativeness (I, AUC, rank correlation), never absolute thresholds — except τ_rev = 0.5, a design parameter.
5. **Bench specificity:** all bars are on the 60-item decision bench at Pythia-410m, view 0. No claim about other benches/backbones is licensed under any branch.
6. **â_self is sign-less until G2/G3** — EXP135's lesson is respected by making the sign channel a gate, not an assumption.
7. **Trigger-rate floor (15) is a design parameter** — chosen for inference validity on the revision test, not derived from data; a floor that is never met makes Stage 2 untestable, which the VOID rule handles honestly.

---

## Appendix A. Condition-closure checklist (for the next Law #14 reviewer)

- [ ] C1: §1 and §6(v) characterize EXP125 correctly (first-token logit-readout honesty self-report, fidelity 28/60 vs cosine-argmax decision statistic, LOG-4680, bench-specific); no "verbalized vs distributional" framing; non-resurrection rests on the four correct grounds (a–d).
- [ ] C2: §2 pins revision decoding GREEDY (matching baseline ŷ_i) and the trigger-rate floor 15/60 with the VOID rule.
- [ ] C3: §8 verifies Kamoi (TACL 2024, 2024.tacl-1.78) and Xu (ACL 2024, 2024.acl-long.826, arXiv:2402.11436) at full-text level; nothing marked verified that is not.
- [ ] Seeds pinned: S_PERM_G2 = 20261007 (I-screen permutation), S_PERM_C2 = 20261008 (G3 C2 partition), S_RANDTRIG = 20261009 (random-trigger subset). No seed chosen at runtime. (Self-eval is teacher-forced; no sampling seed needed.)
- [ ] Pins: §2 backbone pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` and bench pin `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`, both verified against the committed EXP140 Stage-1 records.
- [ ] Baseline-source decision pinned: REUSE of committed EXP140 B0 records (§1).
- [ ] Mechanical clarification: §1 documents the C2 partition adaptation (single-answer-per-item bench; "majority-wrong/right" → baseline-wrong/right), for reviewer confirmation.
- [ ] Precedence KILL (any) > PIVOT > CONTINUE > HELD; PIVOT reachable; HELD coverage complete (incl. the numerical-superiority-with-p≥0.05 case).
- [ ] No experiment number minted in this draft (minted only at pre-reg SIGN).
