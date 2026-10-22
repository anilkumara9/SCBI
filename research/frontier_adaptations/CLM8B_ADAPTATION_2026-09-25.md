# CLM-8B Frontier Adaptation Analysis — 2026-09-25

**Analyst:** Frontier-Adaptation (reporting to CEO Nova)
**Frontier verdict:** STEAL/ADAPT (highest-priority hard-thinking task per 2026-09-25 sweep)
**Status:** analysis only — no experiment licensed; the sketch in §5 is NOT a pre-registration.

---

## 1. Source record

**Primary sources (read directly):**
- Model card: `Contrastive-LM/CLM-v0.1-8B` on Hugging Face (https://huggingface.co/Contrastive-LM/CLM-v0.1-8B) — read 2026-09-25.
- HF org page: https://huggingface.co/Contrastive-LM — confirms artifacts: `CLM-v0.1-8B` (Text Ranking), `deepswe-clm-heads-8k`, datasets `CLM-v0.1-Pretrain-Nemotron` (62.5M rows), `deepswe-clm-train-embeddings-8k`.
- Release code referenced by model card: `github.com/Contrastive-LM/CLM` (not independently fetched).

**Secondary sources (cross-consistent, treated as reported claims):**
- MarkTechPost 2026-09-23, AIDailyPost 2026-09-24, Saipien, DigestAI, CryptoNWZ — all agree on mechanism and numbers below.

**Citation (from model card):** Kwok, Kang, Suresh, Saad-Falcon, Pavone, Ré, Mirhoseini (2026),
*Contrastive Language Models: A System One Model for Fast and Generalizable Decision-Making*, Notion Blog
(not arXiv — no peer-reviewed paper located as of 2026-09-25).

**UNVERIFIED:** every latency and accuracy number below is vendor-reported (model card / press). No
independent replication was found. The 9× figure's comparator (Jev) is proprietary and inaccessible.

---

## 2. Mechanism — what is frozen, what is computed

**Architecture (primary source):** two small projection heads — a *state head* and an *action head* —
on top of a **frozen Qwen3-8B encoder**, trained with a **bidirectional InfoNCE** contrastive loss.

**Inference pipeline:**
1. State text → frozen Qwen3-8B → **last-token pooling** → state embedding → state head.
2. Each candidate action text → frozen Qwen3-8B → last-token pooling → action embedding → action head.
3. Score = similarity between the two head outputs (dot product per secondary reports; model card
   says the contrastive objective "connects states and actions" — the dot-product+softmax detail is
   secondary-reported).
4. Softmax over candidate scores → answer distribution (typed outputs: Noul / Choice / Score).

**What is frozen:** the entire 8B backbone (Δθ=0 for the LLM — compatible with SCBI's frozen-backbone
law as far as the *model* is concerned).
**What is trained:** two ~20M-parameter projection heads (secondary-reported size; ~75 MB Apache-2.0
artifact per model card).
**What is computed at inference:** embeddings + one matrix multiply over candidates. States and actions
are encoded *separately*, so action embeddings are cached and reused across steps — the systems-level
source of the speedup.

**Training recipe (reported):** (1) pretrain on ~60M Nemotron Q&A pairs → 52.1% top-1 on ~100K held-out;
(2) mid-train on ~30M synthetic hard negatives (Gemini 2.5 Flash-Lite) → 69.2%; hard negatives *from the
start* overfit (62.4% peak then decline) — negative-mining timing matters; (3) post-train on ~1M agent
trajectories. Fine-tuned verifier heads: 81.6% DeepSWE, 87.6% Terminal-Bench 2.1 (held-out subsets,
**not** full leaderboard submissions — primary source is explicit that SOTA numbers need fine-tuning,
not zero-shot).

**Disambiguation:** secondary sources say "two separate encoders, each a frozen Qwen3-8B + head." The
primary model card shows ONE served encoder (`vllm serve Qwen/Qwen3-8B --runner pooling`) with the
`Engine.rank` client embedding both query and candidates through it. Binding reading: **single frozen
encoder run twice, two heads.** The "two encoders" phrasing is a functional description, not two backbones.

**Limitations (primary source, quoted in spirit):** encoder-locked (requires Qwen3-8B last-token-pooled
embeddings); **no generation** — scores only the candidates given, probabilities relative to that set;
CLM-35B (multimodal, more data/compute) coming early October 2026.

---

## 3. Mapping onto SCBI — threaten vs vindicate

**VINDICATES EXP077's output-side finding.** Five experiments converged on: the transferable direction
lives output-side, not in concept geometry (EXP077: all static geometric variants ΔM=0, p=1.0; bridge
+10pp output-side). CLM never touches the forward pass. It reads frozen output embeddings and scores.
The frontier just validated our boundary result as an *architecture*.

**Does NOT rescue the bridge (LOG-204 demotion stands).** The bridge was option-informed *injection into
the forward pass* — known-answer at inference. CLM's heads are label-informed *in training* but score
genuinely novel candidates at inference, and never inject. Different object, different license. The
demotion is unaffected.

**THREATENS the static-injection research direction, not the constitution.** The frozen backbone
(θ_after = θ_before for the LLM) survives — CLM's backbone is frozen too. What dies is the
"invent representations *inside* the forward pass" program: CAA-style steering, the EXP065/066/070/077/082
lineage. The evidence now says the winning move is not to steer the generator mid-flight but to let the
frozen model produce candidates and **score them at the output boundary**. This is a genuine PIVOT signal:
from synthesis-within to selection-over.

**The brutal honest point:** "contrastive head on frozen embeddings" is, at its core, a probe — a very
good, bidirectional-InfoNCE, systems-engineered probe. The stealable novelties are: (a) **state/action
disaggregation** — separate embedding of decision-context vs candidates, enabling caching; (b) scoring as
a *replacement for generation* in decision tasks (not a supplement); (c) the 3-stage recipe with
hard-negative timing.

**Summit relevance:** no claim of superhuman or conscious-level cognition (nothing in this window makes
one). But CLM-8B is the first concrete existence proof that **frozen-backbone + inference-time
computation beats a proprietary frontier system on real tasks** — the exact class of result SCBI has
zero of. It is the program's missing capability-entry archetype.

**The Δθ=0 adjudication (load-bearing for us):** the 20M heads ARE trained weights. Under a strict
reading, end-to-end Δθ≠0. The defensible SCBI reading: the *LLM backbone* stays frozen; the heads are
**inference-time scoring apparatus** — the same ontological category as our probes and the bridge
(apparatus, not model). Training them is training, so Law #7 (zero leakage) applies in full: held-out
evaluation, no test-label contamination. Any future pre-registration must state this license explicitly
and cannot claim "pure Δθ=0."

---

## 4. What would kill the adaptation idea (brutal list)

1. **It is just linear probing.** If the entire effect reduces to "a trained classifier on frozen
   embeddings beats chance," there is no new science for SCBI — that is decades old. The idea survives
   only if the *disaggregation + scoring-as-decision* architecture yields something probing does not.
2. **The magic is all in 60M+ training pairs.** If zero-shot scoring over frozen embeddings is at chance,
   then the capability comes from massive contrastive training we cannot afford ($0 budget, no GPU
   training) — the adaptation is unexecutable, not just unproven.
3. **The 9× is a systems artifact, not a cognitive one.** If the speedup is entirely "matmul vs
   autoregressive decode" (textbook), there is no intelligence claim — only engineering. True, but the
   *capability* numbers (81.6% / 87.6% verifier SOTA) are the part that matters, and those need
   fine-tuning.
4. **Candidate-set dependence.** Primary source admits: probabilities are relative to the given set; no
   generation. A scorer that cannot propose candidates cannot think — it can only judge. For the
   superhuman-cognition summit, scoring is a component, not a path.

---

## 5. Concrete adaptation sketch (Law #15 — NOT a pre-registration)

**Precise question:** Does output-side contrastive-style scoring over *frozen, untrained* Pythia
representations produce causal decision gains where static injection produced exactly zero?

**Decision it changes:** KILL vs CONTINUE/PIVOT on the "scoring-over-frozen-representations" adaptation
of the SCBI program. CONTINUE → toward trained heads (a funded training program). KILL → the CLM effect
is entirely in massive head training, unexecutable at $0; PIVOT → heads-as-trainable-apparatus only if
training becomes available.

**Cheapest falsifying test ($0, CPU-only, ~1 hour):** reuse EXP077's frozen artifacts
(`exp077_vectors.pt`, 60 items, Pythia-410m layer-20 final-token embeddings). For each item, treat the
premise embedding as the *state* and the two option embeddings as *actions*; score by cosine similarity
(the untrained analogue of the CLM dot-product head); decision = argmax. Measure accuracy vs 50% chance
and vs the static-injection null (ΔM=0, p=1.0) and the bridge positive control (+10pp, p=0.03125).

**Mathematical license:** InfoNCE maximizes a lower bound on mutual information I(state; action). The
zero-shot test asks whether the frozen pretrained geometry *already* aligns state–action MI with task
labels — i.e., whether the backbone's pretraining did the contrastive work for free.
**Quantitative prediction:** if frozen geometry carries task-relevant MI, zero-shot Choice accuracy
exceeds chance with binomial margin.
**Breaking point:** N=60, one-sided binomial vs p=0.5: **≥38/60 (63.3%) required** (P(X≥38)≈0.037).
**≤37/60 → KILL** the free-lunch version: frozen geometry carries no exploitable decision signal, and
the CLM capability must come from the 60M-pair head training we cannot run.

**Cost:** $0; CPU only; no weights touched (artifacts already on disk); no GPU.

---

## 6. Assessing the 9×-faster claim — what verification would take

The claim decomposes:
- **(a) vs Jev (proprietary, limited early access):** UNVERIFIABLE by us — no Jev access. The headline
  9× (T-Rex: 16.5ms vs 149.8ms) and 13×-at-1k-candidates figures are vendor-reported; mark UNVERIFIED.
- **(b) The architectural source (matmul-over-candidates vs N autoregressive decodes):** verifiable in
  principle and textbook. A $0 Kaggle-T4 test could time (i) N single-token forward passes vs (ii) one
  batched embedding pass + one N×d matmul on the same hardware — estimated ~0.05 T4-hours. This would
  verify the *mechanism* of the speedup, not the 9× number.
- **(c) The capability numbers (81.6% DeepSWE / 87.6% Terminal-Bench 2.1):** need the fine-tuned heads
  (`deepswe-clm-heads-8k`, Apache-2.0, on HF) + Qwen3-8B inference + the held-out task lists. The heads
  are downloadable; running them needs a GPU with ~16GB+ (Kaggle T4×2, free tier). The "held-out
  subsets, not full leaderboard" caveat (primary source) must be preserved in any reporting.

**Bottom line on verification:** the interesting scientific claim (scoring beats generating for decision
tasks) is testable by us at $0; the headline 9×-vs-Jev number is not independently checkable.

---

## 7. Watch items for the frontier sweep

- **CLM-35B** (multimodal, more data/compute) announced for early October 2026 — track release and
  whether the contrastive-scoring recipe scales.
- **Jev (TypeSafe AI)** — any public/benchmark access would unlock head-to-head verification.
- **Negative-mining timing** (hard negatives from start → overfit at 62.4%): a training-dynamics result
  worth stealing if we ever train heads.

---

## 8. Recommendation

**ADAPT (not wholesale steal).** Steal the architecture — state/action disaggregation and
scoring-as-decision at the output boundary — because it vindicates our own output-side boundary result
and threatens only the already-failing static-injection direction. Do NOT claim the 9× or the SOTA
numbers (UNVERIFIED, partially unverifiable). Run the §5 zero-shot test first: it costs one CPU-hour
and tells us whether the adaptation is executable at $0 or dies on the training-budget wall. If it
CONTINUES, the honest next step is a *funded* head-training program — which the founder must explicitly
license, since it crosses from Δθ=0 into trainable apparatus.
