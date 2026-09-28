# GAP ANALYSIS: What Made the Legendary Papers Explode — and Where the SCBI Boundary Paper (v82) Stands

**Lane:** GAP-ANALYSIS (founder commission 2026-09-27, acknowledged, never executed)
**LOG:** LOG-4496 | **Date:** 2026-09-28 | **Compute:** $0 CPU, analysis only
**Constraint honored:** no modification to v82 paper sources; no v83 build.
**Inputs:** `~/workspace/scbi-paper/v82/paper.tex` (754 lines, 18 pages, read in full), `~/workspace/your_files/SCBI_Boundary_Paper_v82.pdf` (reference), `~/workspace/SCBI/research/benchmarks/FRONTIER_SCOREBOARD.md` (v1.4), `PROGRESS_ANALYSIS.md`.
**Factual discipline:** every legendary-paper claim below is a real, verifiable fact about a real paper. No invented citations. Key numbers spot-verified against primary sources on 2026-09-28 (arXiv:2201.11903 Table 1; LoRA Tables 5–6; AlexNet abstract/ILSVRC-2012 results; InstructGPT §4.1).

---

## PART 1 — Per-paper explosion factors

Eleven canonical papers. For each: what actually made it explode — title, framing device, figure strategy, simplicity of the core claim, timing, open artifacts, narrative arc. Specifics, not generics.

### 1. AlexNet — Krizhevsky, Sutskever, Hinton, "ImageNet Classification with Deep Convolutional Neural Networks," NeurIPS 2012

- **Title:** utterly plain, descriptive, unsexy. The paper exploded *despite* the title, which proves a title is not load-bearing when the number is a phase change.
- **The number:** ILSVRC-2012 top-5 error **15.3% vs 26.2%** for the second-best entry — an absolute 10.9-point drop, ~41% relative. The margin was unprecedented in ImageNet history; the 10-year retrospective devoted a full paragraph to the gap alone.
- **Framing device:** "everything you were told doesn't work, works — if you scale it." It invented zero new components (CNNs were LeCun 1998; ReLU, dropout, augmentation all existed). The claim was compositional: ReLU + dropout + data augmentation + two GTX 580s = a different kind of system.
- **Figure strategy:** the architecture diagram (Figure 2, the split-GPU network) became the visual template for a decade of CNN papers; feature-visualization figures made the learned representations *visible*.
- **Simplicity:** "Deep CNNs trained on GPUs crush ImageNet." One sentence.
- **Timing:** arrived the exact year data (1.2M labeled images) and consumer GPUs (GTX 580) made the previously-untrainable trainable. The bottleneck had just moved; AlexNet was standing on it.
- **Open artifacts:** custom CUDA kernels, released code, trained weights — the community could reproduce and extend within weeks.
- **Narrative arc:** underdog method (neural nets were out of fashion; SVMs ruled) beats the entire field by a margin so large the room went quiet (standing-room-only NIPS session). Defeat-of-incumbent stories are the most viral narrative in science.
- **Lesson for SCBI:** explosions come from a *margin over the incumbent*, not from a title. v82 has no incumbent to beat — its headline is a self-kill (ΔM = 0). A null cannot use the AlexNet playbook directly.

### 2. Attention Is All You Need — Vaswani et al., NIPS 2017

- **Title:** a provocation and a slogan. It became the vocabulary of the field ("attention," "transformer"). Short, declarative, slightly arrogant — maximally quotable.
- **The number:** 28.4 BLEU EN→DE, 41.8 EN→FR — new state of the art, trained in **3.5 days on 8 P100 GPUs** (vs. weeks for the LSTM incumbents). The number was "better AND cheaper AND faster," a triple threat.
- **Framing device:** subtraction as innovation — "we propose a new simple network architecture… based *solely* on attention mechanisms, dispensing with recurrence and convolution entirely." Deleting the incumbent's core component is a power move.
- **Figure strategy:** Figure 1, the Transformer block diagram (encoder/decoder stacks with multi-head attention), is the most reproduced diagram in ML history. Every subsequent paper redrew it. An iconic figure is a free citation engine: people copy your visual language and cite you for it.
- **Simplicity:** "You don't need recurrence. Attention is all you need." Eight words.
- **Timing:** RNN/LSTM translation had plateaued; the field was hungry for parallelizable architectures. Published June 2017, right as GPU-rich labs needed something to spend compute on.
- **Open artifacts:** the Tensor2Tensor release and the diagram itself; within a year, OpenNMT, fairseq, and every lab had a Transformer.
- **Narrative arc:** eight Google authors quietly delete the two pillars of sequence modeling and win anyway. Elegance + dominance.
- **Lesson for SCBI:** v82's nearest shot at an iconic figure is the hero dissociation figure (decode bar high, injection arrow flat) — but it currently needs a long caption to be understood. The Transformer diagram needs no caption.

### 3. BERT — Devlin et al., "Pre-training of Deep Bidirectional Transformers," Oct 2018

- **Title:** descriptive; the acronym did the work. "BERT" is short, anthropomorphic, meme-able.
- **The number:** not one number but a *sweep table*: GLUE 80.5 (vs 72.8 GPT), SQuAD, MNLI — 11 NLP tasks, nearly all beaten with the same recipe. The table was the argument: fine-tune the same checkpoint on everything.
- **Framing device:** two pre-training tasks everyone can picture — masked-word prediction ("fill in the blank") and next-sentence prediction. The method is explainable to a non-expert in 30 seconds.
- **Figure strategy:** the pre-training/fine-tuning diagram (same architecture, different heads) — visually communicates "one model, many tasks."
- **Simplicity:** "Pre-train once on unlabeled text, fine-tune cheaply on anything." 
- **Timing:** post-Transformer, pre-GPT-3 — the exact window when the field had the architecture but not the recipe.
- **Open artifacts:** THE reason BERT exploded — open-sourced code AND weights AND a Colab fine-tuning tutorial. A grad student could beat SOTA on their task in an afternoon. Democratization is the highest-octane virality fuel there is.
- **Narrative arc:** the open, reproducible workhorse vs. the closed frontier. BERT won by being *usable*.
- **Lesson for SCBI:** v82's NeurIPS checklist answers **\answerNo** on open data/code. This is the single biggest virality gap: BERT proved openness beats eloquence.

### 4. GPT-3 — Brown et al., "Language Models are Few-Shot Learners," May 2020

- **Title:** the title IS the claim, and the claim is a magic trick: "few-shot learners." It names a capability nobody thought existed.
- **The number:** 175B parameters — but the viral number was qualitative: the model does translation, QA, and arithmetic *from a prompt*, with no gradient updates. The famous Figure 1 (aggregate few-shot performance vs. scale) showed smooth, predictable scaling curves.
- **Framing device:** in-context learning as a new paradigm — "the model learns the task from the prompt." Every demo was a party trick (write a poem, generate code).
- **Figure strategy:** scaling curves (performance vs. model size, log-linear) — the visual promise that *bigger will keep working*. Plus few-shot example boxes that readers could try themselves.
- **Simplicity:** "Make it 100× bigger and it learns from examples in the prompt."
- **Timing:** the scaling-laws paper (Kaplan, Jan 2020) had just told the field that scale is predictable; GPT-3 was the proof, four months later.
- **Open artifacts:** none — API only. GPT-3 proves closed can go viral IF the capability is shocking enough and demos are abundant. (The API playground was the artifact.)
- **Narrative arc:** emergence — capabilities nobody trained for, appearing at scale. The "sparks" narrative.
- **Lesson for SCBI:** GPT-3 is the exception that proves the rule — closed works only with a shocking positive capability. v82 has no positive capability to demo.

### 5. Kaplan et al. — "Scaling Laws for Neural Language Models," Jan 2020

- **Title:** plain. The paper exploded on the strength of a *law*.
- **The number:** power-law relationships between loss and (parameters, data, compute) with clean exponents. Predictability itself was the product.
- **Framing device:** physics envy — the messy field of deep learning gets *laws*. Log-log plots that are straight lines.
- **Figure strategy:** log-log scaling plots — the straight line on a log-log plot is the most persuasive figure in science. It says "this is not noise; this is nature."
- **Simplicity:** "Loss falls as a power law in scale. You can predict the future."
- **Timing:** told every lab exactly how to spend its compute budget, right before the billion-dollar training runs.
- **Open artifacts:** the empirical fits, immediately usable for planning.
- **Narrative arc:** from alchemy to science — the field's maturation story.
- **Lesson for SCBI:** the closest SCBI analogue is Eq. (3), the 1/(d−r) dilution law — a genuine quantitative law ("the transfer is not a map; it is a draw"). It is currently buried in §3. A legendary paper would put the law in the title or abstract's first line.

### 6. Chain-of-Thought — Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," Jan 2022

- **Title:** names the technique; "chain-of-thought" became field vocabulary overnight.
- **The number:** PaLM 540B on GSM8K: **17.9% → 58.1%** (8-shot CoT; Table 1, arXiv:2201.11903) — beating fine-tuned GPT-3 175B + verifier (55%) with *no parameter updates*. A 3× jump from a prompt change.
- **Framing device:** "show your work" — the technique is something every schoolchild understands. Worked examples in the prompt.
- **Figure strategy:** side-by-side prompt boxes (standard vs. CoT) with the model writing out reasoning steps. The figure IS the method; anyone can copy it in 10 seconds.
- **Simplicity:** "Give the model worked examples with reasoning steps and it reasons." Zero-shot variant (Kojima et al.): append "Let's think step by step."
- **Timing:** the exact moment 100B+ models existed but couldn't do math. The pain was universal; the fix was free.
- **Open artifacts:** the method is the artifact — eight hand-written exemplars, copy-pasteable. Zero cost to adopt. This is democratization at the absolute limit: the "code" is a sentence.
- **Narrative arc:** emergence again — reasoning appears at scale, unlocked by a trick so simple it feels like cheating.
- **Lesson for SCBI:** the most viral technique papers minimize adoption cost to zero. v82's adoption cost is high (read a theorem, accept a null).

### 7. LoRA — Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models," 2021

- **Title:** the acronym became the product name. Four letters, pronounceable, searchable.
- **The number:** **10,000× fewer trainable parameters** (175B → 4.7M on GPT-3) with quality matching or beating full fine-tuning (WikiSQL 73.4% vs 73.8%; MultiNLI 91.7% vs 89.5% — LoRA Tables 5–6). Plus: VRAM 3× smaller, checkpoint 35 MB vs 350 GB.
- **Framing device:** "freeze the giant, train two tiny matrices." The intrinsic-rank hypothesis — updates live in a low-dimensional subspace — is elegant and surprising.
- **Figure strategy:** the low-rank decomposition diagram (W + BA) — one picture explains the whole paper; the log-scale parameter bar chart (175B vs 4.7M) is viscerally shocking.
- **Simplicity:** "Fine-tune a 175B model on one GPU by training 0.0027% of the parameters."
- **Timing:** the exact moment everyone had access to giant open models (LLaMA era was coming; GPT-3-scale fine-tuning was impossible for mortals). Maximum pain, maximum relief.
- **Open artifacts:** code released, merged into HuggingFace PEFT within months; QLoRA, LoRA+ followed. The ecosystem did the marketing.
- **Narrative arc:** David vs. Goliath — the tiny adapter beats full fine-tuning. Democratization story.
- **Lesson for SCBI:** LoRA won by *removing a barrier*. Papers that remove barriers go viral; papers that erect them (new falsification requirements) go cited-but-not-viral. v82 is in the second category by construction.

### 8. InstructGPT — Ouyang et al., "Training Language Models to Follow Instructions with Human Feedback," Jan 2022

- **Title:** descriptive; "RLHF" and "InstructGPT" became the vocabulary.
- **The number:** outputs from the **1.3B InstructGPT preferred over 175B GPT-3** — a 100×-smaller model beating the giant; 175B InstructGPT preferred **85±3%** over 175B GPT-3 (§4.1). TruthfulQA roughly doubled; hallucinations halved (41% → 21%).
- **Framing device:** the three-step diagram (SFT → reward model → PPO) — Figure 2 is the most copied alignment diagram ever. "Helpful, honest, harmless."
- **Figure strategy:** the pipeline diagram + human-preference win-rate bars. Preference bars are intuitively readable by non-experts.
- **Simplicity:** "Train the model on what humans prefer, not just next-token prediction."
- **Timing:** GPT-3 was powerful but unusable as a product (it didn't follow instructions). InstructGPT was the paper behind ChatGPT — it bridged the last mile to the product that changed the world.
- **Open artifacts:** no weights, but the *recipe* was fully specified and immediately replicated (the entire open-source RLHF wave).
- **Narrative arc:** alignment made practical — the paper that turned a research demo into something your grandmother could use.
- **Lesson for SCBI:** the "last mile to usability" paper beats the "deep truth" paper on virality. v82 is a deep-truth paper.

### 9. ResNet — He et al., "Deep Residual Learning for Image Recognition," Dec 2015

- **Title:** plain; "residual" became vocabulary.
- **The number:** 152 layers (8× deeper than VGG), **3.57% top-5 error** on ImageNet (ensemble) — winning ILSVRC 2015. But the viral number was the *depth*: 152 layers where everyone else was stuck at ~20.
- **Framing device:** reformulate the learning problem — "instead of learning H(x), learn F(x) = H(x) − x." The skip connection is a one-line idea.
- **Figure strategy:** the residual block diagram (the little curved skip arrow) — perhaps the most drawn-on-whiteboards diagram in deep learning. One curved arrow changed the field.
- **Simplicity:** "Add the input back. Now you can train 152 layers." The fix is literally one arrow.
- **Timing:** post-AlexNet/VGG, the field was stuck — deeper networks performed *worse* (degradation problem). Maximum pain point.
- **Open artifacts:** code released; every framework shipped ResNet within months.
- **Narrative arc:** the degradation mystery → the embarrassingly simple fix → depth unlocked.
- **Lesson for SCBI:** the one-arrow fix is the gold standard of "simple core claim." v82's core claim (decodability ⇏ steerability under static injection) is simple to *state* but the evidence chain (decode at L11, inject at L11, McNemar, headroom verification) is not one arrow.

### 10. Word2Vec — Mikolov et al., "Efficient Estimation of Word Representations in Vector Space," 2013

- **Title:** plain. The *meme* did the marketing.
- **The number:** not a benchmark — the analogy task: **king − man + woman ≈ queen**. Vector arithmetic on words.
- **Framing device:** word algebra. The party trick that launched a thousand keynotes.
- **Figure strategy:** 2-D projections of word vectors (countries/capitals forming parallelograms). Visual, instantly graspable.
- **Simplicity:** "Words are vectors; analogies are arithmetic." Plus: training is fast (the paper's real contribution was efficiency — CBOW/skip-gram on billions of words).
- **Timing:** NLP was drowning in one-hot sparsity; distributed representations were the bottleneck.
- **Open artifacts:** the C toolkit (word2vec.c) — blazing fast, runnable by anyone. Embeddings for everyone.
- **Narrative arc:** the demo, not the theorem — "look what the vectors can do."
- **Lesson for SCBI:** the single most viral unit in ML history is a *demo you can picture*. v82's nearest demo is Item-33 (decodes with 2nd-largest margin, yet injection moves nothing) — currently buried as numbers in the Discussion. It needs the king-queen treatment: a picture, not a paragraph.

### 11. GANs — Goodfellow et al., "Generative Adversarial Nets," 2014

- **Title:** the acronym became a field ("GANs," then the zoo: DCGAN, CycleGAN, StyleGAN).
- **The number:** early results were modest; the virality came from the *samples* — generated faces getting sharper every year. The product was visual progress.
- **Framing device:** the two-player game — generator vs. discriminator, "adversarial." A story with characters. Counterfeiter vs. police is explainable at a dinner party.
- **Figure strategy:** the GAN schematic (two boxes fighting) + generated image grids. The image grids did 90% of the marketing.
- **Simplicity:** "Two networks fight; both get better."
- **Timing:** generative modeling was stuck on blurry VAEs; the field wanted sharp samples.
- **Open artifacts:** the formulation was simple enough that anyone could implement it in an evening — the GAN zoo exploded because the barrier was ~50 lines of code.
- **Narrative arc:** conflict as engine — the most narratively satisfying frame in the set.
- **Lesson for SCBI:** v82 actually HAS a two-character drama — the decode probe vs. the injection (the informant vs. the lever), and the retraction (the authors vs. their own past claim). The paper under-plays both as theater.

---

## PART 2 — The 8 patterns (synthesis)

Across all eleven, virality factors in descending order of observed importance:

1. **A shocking number that moves in the right direction.** AlexNet 15.3 vs 26.2; CoT 17.9→58.1; LoRA 10,000×; InstructGPT 1.3B > 175B. Every explosion has one. (v82's numbers move toward zero — structurally anti-viral.)
2. **An iconic figure that becomes visual shorthand.** Transformer diagram; residual skip arrow; GAN two-box fight; LoRA W+BA; scaling-law log-log lines. People redraw your figure → they cite you.
3. **A sticky name that becomes vocabulary.** Attention, BERT, LoRA, chain-of-thought, GAN, ResNet. The title or acronym enters the language.
4. **A one-sentence core claim.** "Show your work." "Freeze the model, train two tiny matrices." "Add the input back." If it needs a paragraph, it won't spread.
5. **Timing: arrive at the bottleneck.** Every paper above landed the year its pain point peaked.
6. **Open artifacts / zero adoption cost.** BERT's weights, LoRA's code, CoT's sentence. The easier to try, the faster the spread.
7. **A narrative arc.** Defeat of the incumbent (AlexNet), emergence (GPT-3, CoT), David vs. Goliath (LoRA), conflict (GAN), maturation (scaling laws), last-mile-to-product (InstructGPT).
8. **Democratization.** The technique works for the reader, not just the authors' cluster.

Secondary pattern: **the retraction/confession.** None of the eleven retracted anything — but in the broader attention economy, public self-correction is disproportionately shared ("authors retract own claim, prove why with a theorem" is a *story*). v82's C3 retraction is its most distinctive narrative asset and is currently framed as duty, not drama.

---

## PART 3 — v82 audit: already world-class

Credit where due. Against the legendary set, v82 already has:

1. **The falsification pipeline as method.** Pre-registered kill criteria, Law #14 independent sign-off, binding verdicts — this is genuinely rare. Most papers (including several above) report positive sweeps; almost none pre-commit to the observation that would kill them. As *procedure*, this is the paper's most defensible claim to importance.
2. **The retraction with a theorem.** C3 is extraordinary: the authors recomputed from primary artifacts, found their own prior claim reversed sign (Δcos −0.72/−0.70 vs claimed +0.13/+0.79), retracted it in-paper, AND proved the dilution law (Prop. 1, the 1/(d−r) expectation) that predicts the reversal. "The transfer is not a map; it is a draw" is the paper's best line — quotable, visual, true.
3. **The honest-position block (C5).** Stating novelty N1 (known combination), disclaiming autonomous-steering signals, fencing "superhuman" as horizon — this level of self-fencing is world-class scientific citizenship, even if it is anti-viral.
4. **The phase diagram's discipline.** Refusing to fake coordinates for experiments that didn't earn them ("decode not probed" ledger, OPEN—UNTESTED badge) is a genuine integrity innovation in figure design.
5. **The master results table.** Every empirical claim traced to a primary artifact (Table 1, App. A). Most papers — including famous ones — cannot say this.
6. **The limitations section.** Eight numbered, checkable fences. Stronger than the median NeurIPS paper.
7. **The hero-figure instinct.** "Fig. 1 is the paper in one figure" is exactly the right instinct; the execution needs work (see Fix #3).
8. **The checklist honesty.** Answering \answerNo on open data/code rather than fudging it. (The fix is to change the answer, not the honesty.)

---

## PART 4 — v82 audit: the gaps (brutally honest)

Ranked by how much each gap costs against the #1-ever ambition:

**G1. No number goes up.** Every legendary paper's viral number is a capability gain. v82's headline numbers: ΔM = 0, p = 1.0, zero flips, kills, a halt. The honest headline (scoreboard v1.4) is "zero positive autonomous-steering signals." A null-result paper can be important (this one is), but no null-result paper in ML history has gone #1-viral on presentation polish. Virality rewards new powers, not mapped walls.

**G2. No iconic figure.** The figures are dense, multi-panel, caption-dependent schematics. None can be redrawn on a whiteboard in 10 seconds. The Transformer diagram test: can a reader sketch v82's core idea from memory after one viewing? Currently no.

**G3. The core claim needs a paragraph.** "Decodability without causal steerability under static injection at the tested protocol" vs. "show your work." The paper has the vocabulary seed ("The Decodability Gap") but buries it under fencing.

**G4. \answerNo on open data/code.** BERT proved openness beats eloquence. The kill pipeline, the decode-then-inject rig, the recomputation recipes — none are released. A reader cannot run the falsification procedure on their own model. This single checkbox is the largest *fixable* virality gap.

**G5. Toy scale.** Pythia-160m/410m, N=60. The legendary papers either used the biggest available system (GPT-3 175B, PaLM 540B) or democratized to everyone (LoRA, BERT-Colab). Small-model N=60 nulls invite the (fair) objection "try it at scale" — which the paper fences (Limitation 2, 6) but cannot refute.

**G6. The future is untested thesis, not results.** §6–§7 plus Appendix D are ~40% of the paper's intellectual weight and 0% of its evidence. Legendary papers' vision sections are short because the results carry the vision. Here the arrow ("three bets") is longer than the bow. (The founder has a pending cut-depth decision on exactly this.)

**G7. No demo moment.** Word2vec had king−man+woman; CoT had worked examples. v82's Item-33 (decodes with 2nd-largest 1-NN margin 1.013, yet injection moves nothing) is the demo — currently a numbers clause in the Discussion. Nobody will keynote a McNemar p-value.

**G8. Timing: a capstone, not a launchpad.** The paper maps where static steering dies just as the field's 2026 wave (SVF, Activation-LQR — both cited) has already moved to adaptive methods. It positions itself as "the instrument the adaptive wave needs," which is the right frame, but instruments get cited, not celebrated.

**G9. Title is accurate but not sticky.** "The Decodability Gap: Decodability Without Causality in Static Steering of Frozen Language Models" — 16 words. Compare: "Attention Is All You Need" (5), "LoRA" (1). The sticky part ("The Decodability Gap") is there; it's wearing a 12-word overcoat.

**G10. Single-author, undergraduate affiliation, no institutional amplifier.** Unfair but real: 9 of the 11 legendary papers rode Google/OpenAI/DeepMind distribution. The routing-around is open artifacts + a killer demo (BERT's Colab strategy), not polish.

**G11. The retraction is framed as duty, not drama.** C3 is the most *shareable* event in the paper (authors kill their own claim with a theorem they proved) and it's written in the flattest register in the document.

**G12. The "three explanations" framing arrives late.** The intro's best device — "when steering fails, three explanations compete: absent concept, wrong direction, wrong intervention class" — is genuinely good framing (it's the paper's "three ancestors" mirror), but the payoff (A1 ruled out, A2/A3/A4 survive narrowed) lands in the Discussion as a list. The detective story is under-staged.

---

## PART 5 — Top-10 fixes, ranked by expected impact

| Rank | Fix | What changes | Why it matters (pattern #) |
|---|---|---|---|
| 1 | **Open-source the kill pipeline + artifact bundle.** Release the decode-then-inject rig, the pre-registration templates, the Law #14 checklist, and recomputation recipes as a runnable repo (CPU-only, Pythia via HF). Flip checklist item 5 to \answerYes. | \answerNo → \answerYes | #6, #8 — BERT's lesson. This is the highest-leverage fix: it turns readers into users, and users cite. A "falsification kit" others run on their own models is the only path to citation-scale impact for a null paper. |
| 2 | **Promote "The Decodability Gap" to the whole identity.** Shorten the title to *The Decodability Gap* (+ subtitle). Use the term in every section header where the phenomenon appears. Make it the vocabulary entry. | Title + terminology | #3, #4 — sticky names become search terms. "Decodability Gap" is already good; it needs promotion, not replacement. |
| 3 | **Rebuild Fig. 1 as an iconic one-glance visual.** One panel: a tall "DECODE" bar (33% vs 5% chance) beside a flat "STEER" arrow (ΔM = 0) — the dissociation as a visual meme, sketchable from memory. Cut the caption by 60%; move statistics to the legend/table. | Hero figure | #2 — the whiteboard test. Current Fig. 1 fails it. |
| 4 | **Item-33 as the king-queen demo.** Give the dissociation a face: one item, its nearest-neighbor margin visualized, the injection arrow bouncing off. A boxed vignette ("Item 33: the model *knows* it, and cannot *use* it") early in Results — picture, not paragraph. | Demo moment | #7 (word2vec lesson), #2 — keynotes need a slide, not a p-value. (Note: Item-33 vignette variant is a pending founder decision in the v83 plan; this fix is gated on it.) |
| 5 | **Compress the core claim to one sentence, front-loaded.** Abstract's first line becomes something like: "Task information that decodes at 6× chance cannot steer the model it came from." Everything else is fencing — keep the fencing, but lead with the shock. | Abstract/intro lead | #4 — one-sentence claims spread; paragraphs don't. |
| 6 | **Cut the untested thesis to its fighting weight.** §6–§7 + App. D currently outweigh the evidence. Options per the pending founder cut-depth decision: (a) compress to one "horizon" page with the three bets as a table, or (b) move the G/E/S/T + scheduler specifications to a companion tech report. The paper's ratio of evidence to promise must match its honesty brand. | Length/proportion | Legendary papers let results carry vision. A 40%-thesis paper reads as a proposal, and proposals don't go viral. |
| 7 | **Promote the kill ledger to a main-text table.** A BERT-GLUE-style sweep table: every killed hypothesis, its kill criterion, the verdict number — one page, scannable. Currently the kills are prose in §5.2 and a master table in the appendix. Tables are cited; prose is skimmed. | Results presentation | #1-adjacent — the "sweep table" is how BERT made 11 tasks feel like one argument. |
| 8 | **Stage the three-explanations detective story.** Open §5 (Results) with the lineup — A1 (absent concept), A2 (wrong direction), A3 (too small), A4 (wrong magnitude) — as suspects, and close each subsection with the verdict. The intro already sets this up; the results should pay it off structurally, not as a Discussion list. | Narrative arc | #7 — detective stories are the most readable structure in science writing. |
| 9 | **A 5-minute Colab: "reproduce the Gap."** CPU-only notebook: load Pythia-160m, run decode-then-inject on a toy split, print the dissociation. This is the BERT-Colab play at zero cost and directly attacks G10 (no institutional amplifier) by making distribution peer-to-peer. | Artifact/demo | #6, #8, #10 — democratization routes around institutional disadvantage. |
| 10 | **Write the retraction as the story it is.** C3 deserves a narrative box: what was claimed, what the recomputation found, what the theorem predicted — "our own theorem convicted our own claim." Currently the flattest passage in the paper; it's the most human and most shareable. | Narrative | #7 — public self-correction is disproportionately shared; underplayed here. |

---

## PART 6 — What no presentation polish can fix

The honest list, as commissioned. These are structural, not cosmetic:

1. **Zero positive autonomous-steering signals.** The scoreboard's binding headline (v1.4, LOG-4495) is that the label-free capability race is tied at zero and SCBI holds no licensed capability result at any scale. No framing, figure, or title changes the fact that every legendary paper in Part 1 offered a *new power* and this paper offers a *mapped wall*. Polish can maximize citations; it cannot manufacture the capability demo that drives #1-ever virality.
2. **Small models, N=60.** Pythia-160m/410m with 60 items cannot license generality claims, and the field's attention is on frontier-scale systems. Limitation 2/6 fence this correctly, but the fence is also a ceiling: the objection "show me at 70B" has no $0-CPU answer.
3. **The adaptive thesis is untested.** The paper's forward arrow — G/E/S/T, gain scheduling, the five-stage path — is 0% evidenced. Until EXP068 (or a successor) produces a positive number, the vision section is a bet slip. No viral paper in Part 1 led with an untested promise as its second half.
4. **Static steering is a dying paradigm.** The paper is a capstone on the class the field is leaving (the 2026 adaptive wave: SVF, Activation-LQR). Capstones get cited by the next wave's related-work sections; they don't become the wave.
5. **Novelty N1 (known combination).** The paper honestly states the tested mechanism is algorithmically CAA-equivalent. That honesty forecloses the "new method" virality channel (LoRA, ResNet, GAN) permanently.
6. **No institutional amplifier.** Single author, undergraduate affiliation. The legendary set's distribution ran through Google, OpenAI, DeepMind. Open artifacts (Fix #1) and a Colab (Fix #9) are partial mitigations, not replacements.
7. **The #1-ever ambition vs. the null-result genre.** The founder's stated ambition is for this paper to become the #1 research paper ever published. The realistic ceiling for a null-result, small-model, single-author boundary paper — even a world-class one — is "most-cited paper *of its kind*" (the standard falsification reference for steering claims), not #1 overall. The gap between those two is not a presentation problem; it is a results problem, and only a future positive result (the adaptive program paying off) can close it.

**The honest strategic summary:** v82's maximum achievable outcome is to become *the* cited reference for "decodability ≠ steerability" and the standard falsification kit for steering claims — the paper everyone cites when a steering result needs a control. That is a genuinely important, durable position (cf. Belinkov-style probing cautions, which are cited thousands of times without ever going "viral"). The path there is Fix #1 (open kit) + Fix #3 (iconic figure) + Fix #2 (sticky term). Everything else is optimization.

---

*End of GAP-ANALYSIS deliverable. Pre-assigned LOG: LOG-4496. No v82 sources modified. No v83 built.*
