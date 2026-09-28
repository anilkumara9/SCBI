# Gap Review: SCBI Papers vs. the Legendary-Paper Bar
**Date:** 2026-09-28 · **Reviewer:** one-shot analyst (LOG-4390) · **Scope:** paper only, $0 CPU
**Papers audited:** `~/workspace/scbi-paper/v39/paper.tex` (full NeurIPS manuscript, "v81", frozen 2026-09-27) and `~/workspace/scbi-paper/ieee/` (6-page IEEE build, QA PASS, LOG-4387/4388).

**Legendary-paper corpus studied (public web, arXiv/venue pages):** Attention Is All You Need (Vaswani et al., NeurIPS 2017) · GPT-3 / "Language Models are Few-Shot Learners" (Brown et al., NeurIPS 2020) · Chain-of-Thought (Wei et al., NeurIPS 2022) · LoRA (Hu et al., ICLR 2022; arXiv 2106.09685) · InstructGPT (Ouyang et al., arXiv 2203.02155, 2022) · Scaling Laws for Neural Language Models (Kaplan et al., 2020) · Training Compute-Optimal Large Language Models / Chinchilla (Hoffmann et al., 2022).

**Epistemology in this review:** every critical assertion carries a label — [FACT] (verifiable from a cited artifact or page), [OBSERVATION] (what the reviewer sees in the text), [INTERPRETATION] (reviewer's judgment). Nothing is invented: every number below traces to the v81 paper artifacts or the research log. EXP094 is outside v81 and is not cited as paper evidence (LOG-4388 scope note stands).

---

## What the legendary papers share (the bar)

[OBSERVATION] Across the seven papers, the same craft pattern recurs:

1. **A claim-as-title or a coined term.** "Attention Is All You Need" *is* the thesis. "Chain-of-thought" coined the field's vocabulary overnight; "LoRA" is a memorable acronym; GPT-3 named "few-shot learners"; Chinchilla gave "20 tokens per parameter" as a rule of thumb. The field can only talk about what the paper names.
2. **One killer figure.** CoT's Figure 1 (worked math example, reasoning steps highlighted, standard-prompt fail vs. CoT success side-by-side) is readable in ten seconds. InstructGPT's Figure 2 (SFT→RM→PPO three-step pipeline with blue arrows) is reproduced in nearly every alignment talk. LoRA's method diagram + the trainable-parameter comparison table (175B vs. 18M trainable). GPT-3's ladder of scaling curves. Kaplan's log-log straight lines. Chinchilla's isoFLOP curves. Attention's Transformer diagram. In each case the figure *is* the paper for 99% of readers.
3. **One viral number.** LoRA's "10,000× fewer parameters" and "no additional inference latency". InstructGPT's "1.3B preferred over 175B" and "85 ± 3%". CoT's "17.9% → 56.9% on GSM8K, surpassing fine-tuned GPT-3 with a verifier". GPT-3's "175 billion parameters, 10× more than any previous". Chinchilla's "70B beats 280B Gopher at equal compute". Each paper picked ONE number and repeated it verbatim everywhere.
4. **A named enemy (thesis vs. antithesis).** Attention vs. a decade of recurrence. GPT-3 vs. gradient fine-tuning ("applied without any gradient updates or fine-tuning"). InstructGPT vs. GPT-3 itself — same architecture, 100× fewer parameters, different training. CoT vs. answer-only prompting. Chinchilla vs. Kaplan's 0.73/0.27 prescription. Each abstract contains a sentence that gives the reader a stake in the argument.
5. **Calibrated honesty as a credibility engine.** GPT-3's abstract ends by naming datasets where it *struggles*. InstructGPT: "Even though InstructGPT still makes simple mistakes." Chinchilla's entire narrative is "the field's biggest bet was miscalibrated — we re-measured it." The retraction-adjacent honesty is what made the bold claims believable.
6. **A shipped artifact.** LoRA: GitHub package + checkpoints (became HF `peft`). Attention: the architecture anyone could implement. GPT-3: full hyperparameter tables per model size. Reproducibility discipline converts readers into builders, builders into citations.
7. **The legendary abstract arc (7–9 sentences):** problem → simple idea → the number → what it changes → honest boundary. GPT-3's and InstructGPT's abstracts are the canonical examples.

---

## (a) WHAT IS ALREADY WORLD-CLASS

Elements of the SCBI papers that already meet the legendary-paper bar, with evidence:

**1. The claim-as-title + coined term.** [FACT] The title is *"The Decodability Gap: Decodability Without Causality in Static Steering of Frozen Language Models"* — a claim-as-title in the Attention/CoT tradition, and "Decodability Gap" is a coined term: "We call this the *Decodability Gap*: decodability without causal steerability." [INTERPRETATION] This is the single strongest positioning asset the paper has; it is what a title should do.

**2. The in-paper retraction — stronger than Chinchilla's correction.** [FACT] §2.4 publishes: "Prior program summaries claimed Procrustes rotation improved cross-vocabulary alignment (Δcos ≈ +0.13 to +0.79). Recomputation from primary artifacts shows the opposite… The prior summary claim is retracted in full." Chinchilla went viral partly on "Kaplan was wrong about the ratio"; SCBI publishes the destruction of *its own* prior claim, with recomputed numbers (Δcos = −0.7154 / −0.6971), inside the paper. [INTERPRETATION] This is credibility craft at or above the legendary bar — no legendary paper in the corpus retracts its own number in the text.

**3. A real theorem with a slide equation and a one-liner.** [FACT] Lemma 1 (Procrustes non-uniqueness) + Proposition 1 (complement scrambling, Eq. (3)): a transferred direction keeps only a 1/(d−r) fraction of squared alignment in expectation; at d=1024, r=2, "a direction entirely in the complement keeps roughly one-thousandth (1/1022) of its squared alignment in expectation." The independently audited math (LOG-4388: "4 genuine corrections", all applied; "Theorem 1 used undefined… → inserted v39-verbatim definitions") is the Attention-style complexity-table move: legible math that survives adversarial review. Closing line [FACT]: "The transfer is not a map; it is a draw." [INTERPRETATION] This is quotable, slide-ready, and citable independent of the experiments.

**4. The killer figure exists (Fig. 1 hero).** [FACT] The hero figure is the CoT-Fig-1-style dissociation: panel A, EXP092 decodes at 20/60 = 33.33% against 5% chance (p = 0.000999, Bonferroni 0.0020833, 1000 permutations); panel B, EXP093 injects the same layer-11 direction and gets ΔM = 0, zero flips (McNemar b=c=0, p = 1.0), with the 4.7%-of-residual-norm delivery proof. IEEE captions are [FACT] "self-contained mini-stories" (LOG-4388). [INTERPRETATION] Two panels, one dissociation, one caption — structurally the right killer figure.

**5. The honesty discipline (InstructGPT-grade calibration).** [FACT] Eight numbered limitations "fenced… so they can be checked"; the phase diagram "refuses to invent coordinates: one measured point with both axes, a sideline of kills… No boundary curve is fitted; the open region above the finding is marked untested (OPEN — UNTESTED badge)"; "Zero flips on N=60 rules out flip rates above ~5% (95% bound), not smaller effects"; "'superhuman' names a motivating horizon, never an achievement"; "no methods claim is made, no autonomous-steering signal is licensed". [INTERPRETATION] This is the InstructGPT honesty craft — "still makes simple mistakes" — applied more rigorously than InstructGPT itself. It is the paper's second-strongest asset.

**6. The master-results-table discipline.** [FACT] Appendix caption: "Every empirical claim and its primary artifact. No number in §§4–5 lacks a row here." [INTERPRETATION] This is the reproducibility artifact none of the legendary papers shipped in-paper (GPT-3's hyperparameter tables are the closest analogue). It converts the paper from an argument into an auditable record.

**7. The Q1/Q2 framing + C1–C5 checkable claims.** [FACT] "Two questions organize everything that follows" and five checkable claims "each anchored to numbers we repeat verbatim throughout the paper" — the GPT-3/InstructGPT "main findings" structure. [INTERPRETATION] The skeleton is right; the meat placement is the fix (see §b, fix 6).

**8. The Item-33 micro-story.** [FACT] Discussion: "Item 33 decodes correctly with the second-largest 1-NN margin of all 60 items (1.013; same-class 2.106 vs. different-class 3.119), yet injection moves its decision margin by only +0.010 / −0.004 around a +2.07 baseline: decision unchanged." [INTERPRETATION] This is the paper's most quotable paragraph — a worked example with the dissociation inside a single item — and it is currently buried in the Discussion. CoT's Fig. 1 was exactly this kind of micro-story, promoted to the front.

**9. Hash-verified frozen backbone.** [FACT] "The frozen-model discipline is hash-verified on every run (Δθ ≡ 0 via SHA-256…)" [INTERPRETATION] Reproducibility theater done right — the kind of discipline that made LoRA's release trusted.

**10. "A null the rig is proven capable of breaking."** [FACT] Discussion: "That asymmetry, a null the rig is proven capable of breaking, is what makes the boundary a finding rather than an absence of evidence." [INTERPRETATION] This sentence is the paper's thesis in 20 words. It should appear verbatim in the abstract.

---

## (b) TOP-10 FIXES RANKED BY IMPACT

Concrete, implementable, presentation-only. Ranked by impact on virality/citation, not hype.

**Fix 1 — Pick THE viral number and repeat it verbatim everywhere.**
*What changes:* Elevate one one-liner — "decodes at 6.7× chance, steers zero decisions" (20/60 = 33.33% vs. 5% chance; ΔM = 0, p = 1.0 at full headroom) — and print it byte-identical in the abstract, the intro's second paragraph, Fig. 1's caption first sentence, the results lead, and the conclusion. Currently the number appears in at least four phrasings ("33.33%", "more than six times chance", "20/60", "6.7× chance" implied). [OBSERVATION] Every legendary paper repeated one number verbatim: 10,000×; 85 ± 3%; 17.9→56.9; 20 tokens/param. *Why it matters:* memorability is citation infrastructure — people cite what they can recite.

**Fix 2 — One name for the finding; demote the synonyms.**
*What changes:* "Decodability Gap" becomes the only proper name for the central finding. Demote "static null", "the boundary", "the dissociation", "licensed null" to mechanism-scoped labels (use them only with a qualifier: "the EXP065/066 static null"). [OBSERVATION] The intro alone uses "Decodability Gap", "decodability without causal steerability", "the static null", "the boundary", "the dissociation" interchangeably. CoT said "chain-of-thought" ~1000 times; it never said "the reasoning enhancement". *Why it matters:* the field cannot talk about what it cannot name. Term discipline is what turns a finding into vocabulary.

**Fix 3 — State the antithesis in the abstract: name the enemy.**
*What changes:* Add one sentence to the abstract's opening: the field's working assumption is that decodability is a proxy for steerability — that if a direction carries task information, adding it back should move decisions. This paper breaks that proxy. [OBSERVATION] The current abstract opens with the steering-vector fact, not the belief being overturned. GPT-3's abstract named fine-tuning as the thing it replaces; InstructGPT named "bigger ≠ better at following intent"; Chinchilla named Kaplan's ratio. *Why it matters:* a paper without a named antithesis is a report; a paper with one is an argument. Arguments get cited.

**Fix 4 — Promote Item 33 into the hero figure as a worked-example vignette.**
*What changes:* Add a top strip to Fig. 1 (or a boxed callout): "Item 33: decodes with margin 1.013 (2nd of 60) → injection moved its decision margin by +0.010/−0.004 → decision unchanged." [OBSERVATION] This is the CoT-Figure-1 move — a single worked example readable in ten seconds — and the material already exists verbatim in the Discussion. *Why it matters:* this is the screenshot that travels on social media; figures, not paragraphs, go viral.

**Fix 5 — One number per figure, first sentence of each caption.**
*What changes:* Audit all figures (v39: 7; IEEE: 4) so each caption's first sentence is the one-line quantitative takeaway, not scene-setting. The IEEE captions are already "self-contained mini-stories" (LOG-4388) — verify the first sentence carries the number. [OBSERVATION] Legendary figures lead with the claim (Chinchilla's contour captions lead with "70B beats 280B at equal compute"). *Why it matters:* skimmable figures are citable figures.

**Fix 6 — Restructure the abstract/intro to the legendary arc; move the C1–C5 ledger to Methods.**
*What changes:* Abstract becomes: problem (one sentence) → the adjudication procedure (one sentence) → the number (one sentence, Fix 1) → what it changes (one sentence) → the honest boundary (one sentence). Move the C1–C5 enumeration to a "Checkable claims" box in the falsification-pipeline section. [OBSERVATION] C1–C5 currently read as internal program machinery ("Law #14", "kill criteria") in the intro; GPT-3's abstract never mentioned OpenAI's internal process. *Why it matters:* the abstract is what 99% of readers read; machinery in the intro reads as niche.

**Fix 7 — Name the theorem's consequence: "The 1/(d−r) Dilution Law."**
*What changes:* Box Proposition 1's consequence as a named law: *the 1/(d−r) dilution law — a rank-deficient Procrustes transfer keeps only a 1/(d−r) fraction of squared alignment in expectation.* Reference it by name in the retraction, the discussion, and the conclusion. [OBSERVATION] Kaplan made exponents famous; Chinchilla made "20 tokens per parameter" famous. "1/1022" is currently buried in a paragraph. *Why it matters:* a named law is citable independently of the experiments — it gives the theorem a life of its own.

**Fix 8 — Convert the limitations' defensive posture into the thesis.**
*What changes:* Preface the numbered limitations with the sentence that already exists in Results: "Narrow by design; the narrowness is what makes it true." Add the Fix-10 sentence ("a null the rig is proven capable of breaking") to the limitations header. [OBSERVATION] The eight limitations are currently pure defense; InstructGPT turned "still makes simple mistakes" into a trust signal by owning it. *Why it matters:* preempts the #1 reviewer attack ("N=60, one layer, one α") by making it the contribution's definition.

**Fix 9 — Ship a "Reproduce the hero figure" box.**
*What changes:* One boxed paragraph: the primary artifacts, the entry-point commands/scripts, and the expected outputs that reproduce Fig. 1 (EXP092/EXP093) end-to-end. [OBSERVATION] The master results table maps claims→artifacts (world-class, §a.6), but there is no "run this, see that" path for a reader. LoRA shipped the package; GPT-3 shipped the tables. *Why it matters:* lowers the barrier from citation to replication; replicated figures become tutorial figures, tutorial figures become citations.

**Fix 10 — Compress the full paper's future section to falsifiable one-liners.**
*What changes:* In v39, cut the "industry thesis" and "path to superhuman, staged" prose to a three-bullet box: Bet 1 (G/E/S/T, EXP068 — dies if evaluator invalid or compute-matched static ties), Bet 2 (gain scheduler — dies if best fixed gain wins), Bet 3 (composition — dies if it underperforms its parts). Keep the "superhuman is the horizon, never the achievement" line. [OBSERVATION] The IEEE version already did this correctly (cut logs show the design-thesis material removed); the fix is to port that discipline back to v39. Attention's conclusion is ~150 words. *Why it matters:* a pitch deck in the future section dilutes the boundary-science credibility the paper earned everywhere else.

---

## (c) WHAT NO PRESENTATION POLISH CAN COVER

Evidence gaps requiring new experiments, not rewriting. Each names the missing experiment family.

**Gap 1 — The headline number is a point, not a curve (dose-response missing).**
[FACT] EXP093 tests exactly one (layer, α) point: layer 11, α = ±1.0. [INTERPRETATION] Legendary headline numbers came with the curve around them (GPT-3's 8-model ladder; Kaplan's 7 orders of magnitude; CoT's scale sweep showing the ~100B emergence threshold). The dissociation could narrow, widen, or invert at other magnitudes — EXP093's own margin data (perturbation moved margins but not decisions) *suggests* a threshold structure that is currently unmapped. **Missing experiment family:** an α-sweep dose-response on the layer-11 direction (paired decode-then-inject at ≥5 magnitudes), pre-registered with the flip-rate-vs-α curve as the primary endpoint. This is the single highest-value missing experiment: it converts the headline from a point into a law.

**Gap 2 — N=60 power: the 1–5% band is unmeasured.**
[FACT] "Zero flips on N=60 rules out flip rates above ~5% (95% bound), not smaller effects." [INTERPRETATION] The band where weak-but-real steering would live (1–5% flip rate) is exactly the band this design cannot see — and a skeptic's "there might be a small real effect" cannot be answered by prose. **Missing experiment family:** a powered replication at N≈100+ (the sixth frontier condition in Bet 3), pre-registered, on the same paired design.

**Gap 3 — No scale ladder: two small open models, one family.**
[FACT] Evidence rests on Pythia-160m (d=768, 12 layers) and Pythia-410m (d=1024, 24 layers). [INTERPRETATION] Every legendary paper showed the effect across a ladder (GPT-3: 125M→175B; Kaplan: orders of magnitude; Chinchilla: 70M→16B). The "boundary" is currently two points. Whether the Decodability Gap is scale-invariant, scale-shrinking, or scale-emergent is unknown. **Missing experiment family:** paired decode-then-inject across a model-size ladder (≥3 scales, ideally crossing an order of magnitude).

**Gap 4 — Nine of ten verdicts lack decode coordinates.**
[FACT] "Only EXP092×EXP093 has both coordinates measured… the eight EXP077 geometric variants (all ΔM = 0) and the remaining kills live in the 'decode not probed' ledger." [INTERPRETATION] The phase diagram's honesty is admirable, but it means the headline claim (decodable-yet-inert) is *fully measured at exactly one point*. The kills are steering-side only; we do not know which of them were decodable-yet-inert vs. never-decodable. **Missing experiment family:** paired decode probes for each killed variant (the EXP077 family first — it already has the injection side).

**Gap 5 — The positive side of the map is empty.**
[FACT] "CONTINUE (empty to date; none has cleared the gate)." [INTERPRETATION] Every legendary paper showed the thing *working*: GPT-3's few-shot wins, CoT's 56.9%, LoRA's on-par quality, InstructGPT's 85%, Chinchilla beating Gopher. SCBI's map has kills, a theorem, and rescue controls that are explicitly "not evidence about autonomy." A boundary with only one inhabited side reads as a obituary, not a map — and the adaptive thesis (§7) is currently all promise. **Missing experiment family:** at least one demonstrated positive — an adaptive intervention that moves decisions under the same falsification protocol. The licensed candidate is EXP068 (G/E/S/T loop, signed, GPU-gated). Until it runs, the paper's ceiling is "best negative-result paper", not "#1 paper ever."

**Gap 6 — Margin-shift invalidation rests on one wrong-task control.**
[FACT] Limitation 7: "Margin-shift invalidation rests on one wrong-task control, program policy, not a theorem." [INTERPRETATION] The "margins move, decisions don't" distinction is load-bearing for the headline (it's what makes 4.7% residual-norm delivery a non-result), and it leans on a single control. **Missing experiment family:** a control family — multiple wrong-task/wrong-layer/wrong-direction controls with pre-registered margin-vs-decision decision rules.

**Gap 7 — No human-judged endpoint.**
[OBSERVATION] InstructGPT's credibility came substantially from labeler preference with error bars (85 ± 3%). SCBI's endpoints are fully automatic (McNemar on decisions, 1-NN decode). [INTERPRETATION] Lower priority than Gaps 1–5, but a small human study (e.g., blinded rating of injected vs. baseline completions) would harden the "decisions unchanged" claim against the "your metric is too coarse" attack. **Missing experiment family:** blinded human evaluation on the injection arms.

---

## Bottom line for the founder

[INTERPRETATION] The papers are closer to the legendary bar than the program's self-assessment suggests: the coined term, the in-paper retraction, the audited theorem, the honest phase diagram, and the master-results-table discipline are all at or above the bar — several legendary papers lack any equivalent of the retraction or the artifact table. The gap to "#1 ever" is not more rigor; it is **memorability engineering** (Fixes 1–7: one number, one name, one enemy, one vignette, one law) plus **one curve and one positive** (Gaps 1 and 5). The highest-leverage single action: run the α-sweep dose-response (Gap 1) and promote Item 33 (Fix 4) — a curve behind the number and a face on the figure. Nothing in §b or §c requires touching signed protocols, weights, or the v81 number set; all numbers cited here are v81-licensed.
