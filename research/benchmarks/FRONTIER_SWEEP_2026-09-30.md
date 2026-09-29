# Daily Frontier Sweep — 2026-09-30

**Lane:** LOG-4751 (pre-assigned). **Scope:** work published or surfaced 2026-09-23 → 2026-09-30 relevant to the SCBI program. **$0 CPU, read-only on the repo; no model contact.**

Honest-date note: several high-relevance items below were submitted before the 7-day window but *surfaced* (crawled/discussed) within it; submission dates are given verbatim so nothing is mis-dated.

---

## A. Activation steering / representation geometry

### A1. GEOSTEER: Geodesic Optimization for Activation Steering in LLMs
- **Authors:** Xuan Cuong Ngo, Hao Vo, Ngan Le — **arXiv:2609.10658** (submitted 9 Sep 2026; surfaced ~28 Sep 2026)
- **One-line result:** norm-preserving steering reformulated as Riemannian optimization — a learned nonlinear objective guides a sequence of small geodesic steps on the representation manifold, beating SOTA one-step activation-steering baselines on TruthfulQA, RealToxicityPrompts, and UltraFeedback.
- **Relevance to SCBI:** **directly bears on EXP131** (licensed v₁ injection test). EXP131 licenses one-shot additive injection; GEOSTEER is the frontier's strongest case that one-step additive edits are the weak form and geometry-aware multistep steering is the strong form. If EXP131 returns a null, GEOSTEER's multistep-vs-one-shot distinction is the first licensed escalation candidate — it changes the *instrument class*, not the dose. If EXP131 returns positive, GEOSTEER's geodesic machinery is the natural generalization path. Recorded here as a *watch item*, not a license.
- https://arxiv.org/abs/2609.10658

### A2. Disentangling Steering Vectors (Steering Vector Dissection)
- **Authors:** Takeru Hiramatsu, Kyohei Atarashi, Koh Takeuchi, Hisashi Kashima — **arXiv:2609.07037** (submitted 7 Sep 2026)
- **One-line result:** trains a dedicated sparse autoencoder on instance-level steering vectors (positive−negative activation differences) to disentangle composite difference-in-means directions into semantically consistent basis vectors with mutually distinguishable steering effects.
- **Relevance to SCBI:** belongs to the retired static-snapshot instrument class (probes fixed semantic directions) — it does not fence the TGA/dynamics line. Noted for the related-work record; no license implication.

### A3. Steering Geometry: Validating Human Value Geometry in LLM Steering Space
- **Venue:** arXiv:2609.06289 (Sept 2026; related coverage surfaced ~16 Sep 2026)
- **One-line result:** distribution-driven steering vectors (CAA, SAE-feature, ODE-dynamics, spherical) recover the Schwartz value circumplex geometry (Spearman ρ up to 0.51), while behavior-centric methods (OPT, COLD-Steer, BiPO) show no significant geometric correlation despite comparable benchmark scores — shortcut steering hits targets without embedding intended value relationships.
- **Relevance to SCBI:** corroborates the program's lesson that benchmark scores underdetermine mechanism; a steering method's *geometric fidelity* is a separate axis. Mildly relevant to EXP131's decision-orthogonality gate (ĉ): the gate is the program's version of demanding the direction be task-relevant, not just score-moving.

### A4. Cylindrical Representation Hypothesis (CRH)
- **Authors:** Lang Gao et al. — ICML 2026 (posted ~Jul 2026; re-surfaced in sweep window)
- **One-line result:** steering unpredictability is structural, not noise — each input induces a local cylindrical geometry; a steering vector's effect depends on which sector it lands in, and the sector cannot be predicted from outside.
- **Relevance to SCBI:** if true, it predicts *input-conditional* steering effects — EXP131's per-prompt McNemar analysis (best-random comparator) is the kind of design that can detect exactly this. Watch item for the EXP131 verdict report.

### A5. UCSD "Steering AI" technique (Belkin group)
- **Coverage:** today.ucsd.edu (crawled 29 Sep 2026) — internal-feature identification + steering for hallucination/toxicity mitigation; code released.
- **Relevance to SCBI:** capability claim from a university lab; no numbers independently verified in this sweep. Recorded as a frontier capability entry to check against the scoreboard's "SCBI has zero capability entries" standing — the frontier lead is not narrowing on SCBI's side.

### A6. Confidence-steering causal study
- **Coverage:** scienmag.com (published ~13 Sep 2026; crawled 30 Sep 2026) — intervening on confidence-carrying internal states causally shifts model behavior (commit vs hedge) without changing knowledge or prompt.
- **Relevance to SCBI:** an honest positive steering result in the literature — it *does* move behavior via representation intervention, on a narrow axis (confidence expression). It does not contradict SCBI's zero-positive record on the program's decision benches (EXP107/EXP077/EXP094/EXP129), but it is the kind of result the program must cite in related work to avoid overclaiming "steering is impossible."

---

## B. Test-time scaling / reasoning / self-refinement

### B1. CoRefine: Confidence-Guided Self-Refinement for Adaptive Test-Time Compute
- **Venue:** arXiv:2602.08948 (Feb 2026; HTML surfaced in sweep)
- **One-line result:** a ~211K-parameter Conv1D controller learns HALT/RETHINK/ALTERNATIVE actions from confidence traces; ~190× efficiency gains over parallel sampling at competitive accuracy; high-confidence HALT achieves 92.6% precision.
- **Relevance to SCBI:** frontier test-time scaling state of the art; SCBI's Family D (TTS) was pre-launch killed (EXP130) for lack of a valid elicitation channel — CoRefine is *verifier/controller* machinery, not an elicitation channel, so it does not reopen EXP130. Recorded for the frontier scoreboard.

### B2. ReProbe: Efficient Test-Time Scaling of Multi-Step Reasoning by Probing Internal States
- **Venue:** ICLR/ACL 2026 paper-notes (notes updated ~19 Sep 2026)
- **One-line result:** a <10M-parameter transformer probe reads frozen-LLM hidden states/attention/logits to score per-step reliability; matches or beats PRMs 750–810× larger as a Best-of-N/beam-search step verifier.
- **Relevance to SCBI:** efficient verification machinery; orthogonal to the program's falsification-first lines. No license implication.

---

## C. Decodability ≠ steerability (the program's boundary claim)

### C1. Steerable but Not Decodable: Function Vectors Operate Beyond the Logit Lens
- **Authors:** Mohammed Suhail B. Nadaf — arXiv:2604.02608 (v1 Apr 2026; v2 Aug 2026; code README re-crawled 26 Sep 2026)
- **One-line result:** the *converse* dissociation of SCBI's headline — across 4,032 cross-template pairs, 12 tasks, 6 models, 3 families, function-vector steering succeeds even where the logit lens cannot decode the answer at any layer (gaps up to −0.91); only 3/72 task-model cells show decodable-without-steerable. FVs encode computational instructions, not answer directions; Mistral vs Llama/Gemma show two distinct mechanisms.
- **Relevance to SCBI:** **highest boundary-claim relevance.** SCBI's headline is "decodes at 6.7× chance; steers zero decisions"; this paper decomposes the linear representation hypothesis into linear decodability and linear steerability and shows they come apart in *both* directions. It is independent convergent evidence that the decodability↔steerability transfer is not a map. It strengthens the program's v82/v83 boundary narrative — cite in related work alongside arXiv:2609.06951. It does not change any verdict: SCBI's scoreboard stays at zero positive signals because neither paper produced a positive *on SCBI's own licensed benches*.

### C2. Beyond Decodability: Reconstructing LM Representations with an Encoding Probe
- **Authors:** Gaofei Shen et al. — arXiv:2605.00607 (v2, 3 Sep 2026; EMNLP camera-ready)
- **One-line result:** an encoding probe (features → representations) complements decoding probes; syntactic/lexical features contribute independently to reconstruction.
- **Relevance to SCBI:** methodological — a reminder that decode-probe results are estimator-relative, consistent with the program's Law #7 posture.

---

## D. Non-normality / transient growth (TGA/DGF line)

### D1. Nonlinear dynamics of random neural networks with second-order synaptic motifs
- **Authors:** Jun Yang, Hannah Choi — arXiv:2609.14251 (submitted 13 Sep 2026)
- **One-line result:** chain/reciprocal/convergent/divergent motifs jointly reshape the Jacobian eigenvalue bulk; Lyapunov spectrum and participation-ratio analyses show motif structure changes the geometry of chaotic activity even at fixed spectral edge.
- **Relevance to SCBI:** **bears on EXP127's dynamics measurement.** Independent theoretical machinery (Jacobian spectra, Lyapunov exponents, participation ratios) for the same object EXP127 measured empirically (σ₁/σ̄ = 8.24 on the frozen L20→L24 propagator). The participation-ratio dimension is a candidate diagnostic for future dynamics-characterization lanes — recorded as a watch item.

### D2. J-space / workspace hypothesis (blog summary)
- **Coverage:** github.com/storyteller-13/marina (updated 25 Sep 2026) — J-lens workspace: capacity-limited (tens of concepts), broadcast role along depth and sequence axes, present in pretrained base models.
- **Relevance to SCBI:** representation-geometry context; the "broadcast" finding (a single J-lens vector valid as input to many downstream operations) is conceptually adjacent to EXP127's distinguished-direction finding — but it is a blog summary of others' work, cited as context only.

---

## Headline for the program

No item in this sweep changes any verdict, license, or the capability headline (**zero positive autonomous-steering signals**). Two watch items:
1. **GEOSTEER (A1)** — the strongest fresh input to EXP131's design space: if the one-shot injection nulls, geometry-aware multistep steering is the licensed escalation candidate.
2. **Steerable-but-Not-Decodable (C1)** — independent converse-dissociation evidence strengthening the v82/v83 boundary narrative; cite in related work.

**Candidates found: 12** (A1–A6, B1–B2, C1–C2, D1–D2). **Single most relevant: A1 (GEOSTEER)** — freshest, and the only item that directly informs an active licensed lane (EXP131).

---

## Erratum (2026-09-30, LOG-4758; parallel lane used LOG-4757)

The independent Law #14 exact-version review of the v84 change plan (LOG-4754) found two field errors that originated in this signed report (the C1 entry, lines 59–60). The original lines are preserved above; this erratum corrects the record:

1. **Nadaf version date.** The C1 entry states "v2 Aug 2026". arXiv shows v2 last revised **8 May 2026**. The correct reading is "v2 May 2026".
2. **The "−0.91" gap number.** The C1 entry states "gaps up to −0.91". That number does not exist in the paper's full text or abstract — it originated in this sweep report. It is struck. The abstract-verified language is: function-vector steering succeeds with **>0.90 steering accuracy** even where the logit lens's **unembedding projection is incoherent** (the logit lens cannot decode the answer at any layer).
