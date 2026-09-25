# Geometric Similarity without Causal Transfer: A Boundary Study of Static Steering on Frozen Language Models

**Authors:** SCBI Research Consortium
**Document status:** Working draft — 2026-09-23 (Phase 1 sign-off complete; adversarial review SIGNED; **LOG-145 mechanism rewrite + EXP067/077 absorption — re-review required before external use, Law #14**)
**Governing protocol:** `reports/README.md`, `AGENTS.md` (14 laws), `.agents/rules/00-core-research.md`
**Epistemological labels** follow `AGENTS.md` §5. Every quantitative claim cites its primary artifact.

---

## Abstract

We report a boundary result for inference-time steering of frozen language models
($\Delta\theta = 0$). Relational contrast directions
$\Delta h = h(\text{rel}) - h(\text{neu})$ extracted across five disjoint entity
vocabularies exhibit high *raw* pairwise cosine similarity (mean $+0.72$ on Pythia-160M,
$+0.69$ on Pythia-410M) with no alignment applied — yet static injection of the
aggregated basis $B_{\mathrm{agg}}$ into the residual stream produces **zero**
decision changes ($\Delta M = 0.0$ pp, $b=0$, $c=0$, McNemar $p=1.0$) on an $N=60$
relational-reasoning benchmark with verified headroom (19 and 26 rescuable errors),
while a same-layer output-space bridge direction rescues 10/19 ($+16.7$ pp,
$p=0.0020$) and 8/26 ($+13.3$ pp, $p=0.0078$) errors with zero corruptions.
**[INTERPRETATION]** Raw geometric similarity of internal contrast directions does
not imply causal interchangeability under static injection.

We state our prior-art position up front, as required by our research constitution
(Law #10): the tested mechanism, $h \leftarrow h + \alpha B_{\mathrm{agg}}$, is
**algorithmically equivalent** to Contrastive Activation Addition
(Rimsky et al., ACL 2024) and Activation Addition (Turner et al., 2023). Our assessed
novelty tier is **N1 — Known Combination** (tested mechanism N0), signed off after
independent adversarial review of 24 verified citations. This paper therefore makes
no methods claim; its contribution is a carefully controlled **negative result**
that the steering literature predicts (Tan et al., NeurIPS 2024; Braun et al., 2025)
but had not shown in this exact form: geometric alignability without causal transfer,
with the confound of operator unsoundness surgically removed.

We further document, inside this paper, a forensic correction to our own program's
records: summary documents had claimed that a Procrustes rotation *improved*
cross-vocabulary alignment ($\Delta\cos \approx +0.13$ to $+0.79$); recomputation
from primary artifacts shows the rotation **destroyed** similarity
($\Delta\cos = -0.72$ / $-0.70$). We prove why — a rank-$\le 2$ Procrustes fit on
unembedding-space anchors, applied to full-rank residual-stream directions,
provably scrambles its input (Lemma, [THEOREM]) — and we executed EXP067, the
same-space, full-rank alignment experiment pre-registered with a falsification
criterion binding on every outcome branch: it **halted at its own Stage A
guard** (branch (a); 80 anchors span only ~33 of the 64 head-subspace
dimensions), leaving its hypothesis untestable and the boundary claim
unchallenged. A weight-only audit of downstream QK/OV projection energy (G1,
**verdict KILL**) falsified the program's prior null-space
downstream-filtering explanation for this boundary — the failed direction is
*more* QK-visible ($\bar{E}_{\mathrm{QK}} = 0.389985$) than the rescuing
bridge ($0.356185$, mid-null) — so §7 restates the mechanism position as
**readout-misalignment-or-unknown**: the boundary stands on its endpoints,
the bridge's mechanism is recorded as unknown (none of the live hypotheses
promoted), and the QK-subspace operator program is stood down. A paper that
hides its own retraction is fraud; we publish ours — three of them.

---

## 1. Introduction

**Research question.** *Can a frozen foundation model ($\Delta\theta = 0$) improve its
inference behavior through the construction and application of temporary
representation bases at inference time?* This is the Self-Consistent Basis Invention
(SCBI) question. The full SCBI hypothesis posits a per-instance
Generate–Evaluate–Select–Transfer ($\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$)
loop over representation bases. **[OBSERVATION]** What has actually been tested to
date (EXP064–EXP066) is far narrower: a **static** aggregated contrast-direction
basis injected into the residual stream. The dynamic loop has never been executed —
not once, on any model, in this program. Every claim in this paper is scoped to the
tested static mechanism; the loop is discussed only as explicitly unvalidated future
work (§12). Collapsing the two would repeat the hypothesis-shifting error our own
adversarial audit flagged (Laws #4, #11).

**Why a boundary paper.** The most informative outcome of this program is not a new
method — our literature audit (§2) establishes that the tested mechanism already
exists — but a clean, confound-free characterization of *where it stops working*.
Steering vectors are known to be brittle: Tan et al. (2024) document unsteerable
behaviors and out-of-distribution fragility for CAA itself, and Braun et al. (2025)
show steering is unreliable precisely when the target behavior is not a coherent
direction. Our contribution is to exhibit this failure in a controlled,
headroom-verified, positive-controlled setting — and to separate it, by forensic
analysis, from a methods failure (an unsound alignment operator) that had been
misreported as a scientific result.

**Contributions.**

1. **A defensible negative result (O1–O5, §5):** high raw cross-vocabulary cosine
   ($\approx 0.7$) with zero causal transfer under static injection at full
   headroom, replicated across two model scales, with a same-layer positive
   control that rescues a substantial fraction of errors. Geometric similarity
   does not imply causal interchangeability — under static injection, at these
   scales, on this benchmark family.
2. **A forensic correction (§4):** we retract our program's own prior summary
   claim about Procrustes alignment, show exactly what the artifacts say, and
   record the correction in our canonical documents. Negative results include
   results about ourselves.
3. **A theorem about a failure mode (Lemma, §6):** rank-deficient Procrustes
   alignment is provably non-unique on the orthogonal complement of its fit
   subspace; applied to generic full-rank directions it scrambles them. The
   EXP065/066 "alignment" step is a case study.
4. **An executed boundary experiment (§8):** EXP067 re-tests the causal
   question with a sound, same-space, full-rank operator and a falsification
   criterion that binds on every branch — including halts, which are
   pre-registered as reportable outcomes, not off-ramps. (It halted at Stage A;
   see §8.)
5. **An honest novelty position (§2, §10):** N1 — Known Combination, adversarially
   signed. We name the exact priors and the precise sense in which our tested
   mechanism is equivalent to them.

**What this paper is not.** It is not a methods paper; it claims no novel
mechanism. It is not a claim about "superhuman" capabilities — our formalization
document lists that as an explicit non-claim. It is not evidence that frozen
models cannot be steered (our own positive control steers them, via output
space). It is a boundary stone: *here, and no further, under these conditions.*

---

## 2. Related Work and Prior-Art Position

Our research constitution (Law #10) forbids novelty claims without an exhaustive
prior-art audit with equivalence analysis. The full audit — 24 citation records,
every one verified against the live public web on 2026-09-22/23, with a search
log, taxonomy, and ranked closest works — is published as
`research/literature/audit_2026-09-23.md`; the novelty assessment
(`reports/novelty_report.md`) was adversarially reviewed, corrected, and
**SIGNED 2026-09-23** at tier **N1 — Known Combination** (tested mechanism: N0).
We summarize the load-bearing results.

### 2.1 The tested mechanism lives in Family A: diff-in-means steering

The applied operator in EXP064–066 is $h \leftarrow h + \alpha u$ with
$\alpha = 0.50$, where $u$ is a normalized mean contrast direction. This is the
same linear operator as **Activation Addition** (Turner et al., 2023:
$v = \bar{h}(p_+) - \bar{h}(p_-)$, $h \leftarrow h + c\cdot v$) and
**Contrastive Activation Addition** (Rimsky et al., ACL 2024: layer-swept mean
contrast vectors added during inference). Our adversarial reviewer verified the
[EQUIVALENT] rating at the operator level: per-instance normalization,
five-vocabulary aggregation, a fixed coefficient, and single-layer application
are preprocessing and hyperparameter choices — they do not change the
inference-time operator. The same family includes Representation Engineering's
control phase (Zou et al., 2023), Inference-Time Intervention (Li et al.,
NeurIPS 2023), latent steering vectors (Subramani et al., ACL 2022 Findings),
and the refusal direction (Arditi et al., 2024). **[INTERPRETATION]** SCBI Stage A
is an instance of contrastive activation addition, not a variant of it.

### 2.2 The alignment step lives in Family B: linear cross-space alignment

Orthogonal Procrustes alignment of vector spaces is Smith et al. (ICLR 2017);
the unconstrained least-squares variant is Mikolov et al. (2013). Our Stage A
"alignment" was a defective instantiation of this 2013/2017 recipe — rank-2,
cross-space — and no novelty can attach to a broken instance of a known
operator (§6). The stitching literature (Bansal et al., NeurIPS 2021) already
contains our negative result as a known phenomenon: geometric alignability does
not imply causal interchangeability — and stitching validates alignment
*causally*, which our Stage A never did. Distributed Alignment Search
(Geiger et al., CLeaR 2024) optimizes its rotation against intervention
objectives; ours was constructed heuristically and never intervention-validated.

### 2.3 The claimed (untested) loop lives in Family C: inference-time search

The $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop, had it been built,
would compose three verified priors: **Tree of Thoughts** (Yao et al.,
NeurIPS 2023 — generate → self-evaluate → select/backtrack;
[INTERPRETATION] algorithmically isomorphic, differing only in search object:
thoughts vs. bases),
**Self-Consistency** (Wang et al., ICLR 2023 — agreement-as-evidence selection
over sampled outputs), and **Self-Refine** (Madaan et al., NeurIPS 2023 —
generate → self-critique → refine with a single frozen LLM). The closest
*dynamic-intervention* prior is **PPLM** (Dathathri et al., ICLR 2020):
per-instance, inference-time gradient updates to the hidden states of a frozen
LM, guided by an evaluator — but an *external* attribute classifier, not
internal self-consistency, and over hidden-state trajectories, not bases.
**[INTERPRETATION]** The loop is a domain-shifted composition of known
mechanisms; domain shift alone does not clear N1. The remaining distinction —
internal self-consistency evaluator over basis-valued search objects — is a
[CONJECTURE] with zero empirical support, and per our protocol it is
**unscored pending demonstration**, not "N2-aspirational."

### 2.4 The brittleness literature predicts our result

**Tan et al. (NeurIPS 2024)** audit steering vectors in- and out-of-distribution,
including CAA: steerability is highly variable, spurious biases contribute, and
many behaviors are simply unsteerable. **Braun et al. (ICLR 2025 Workshop)**
find steering unreliable exactly when the target behavior is not a coherent
direction — which is one reading of our zero-transfer result. Two methodological
warnings bear directly on our measurements: **Ethayarajh (EMNLP 2019)**
establishes that contextualized representations are strongly anisotropic, so a
raw cosine of $\approx 0.7$ is weak evidence of shared structure; and
**Jorgensen et al. (2023)** show that mean-centring is required to remove the
non-informative global offset from steering vectors — a control our pipeline
omitted. Our O1 observation (§5) is therefore reported with an explicit
anisotropy pointer, not as "shared relational geometry."

### 2.5 What the audit did not find

[FACT] No verified paper demonstrates the complete loop with a *self-consistency*
evaluator over *bases* — per-instance basis generation, internal evaluation,
selection, and application with $\Delta\theta = 0$. [INTERPRETATION] Absence of
an exact prior is weak evidence: every component and the loop structure itself
have verified priors, and the loop has never been shown to work. The honest
research gap is narrow: *whether a per-instance, self-evaluated basis (not
direction, not thought) can be constructed at inference time on a frozen
backbone and improve decisions* — with the evaluator-reliability ceiling
(Brown et al., 2024: without a trustworthy verifier, selection plateaus) and
anisotropy controls as explicit falsifiers.

---

## 3. Method

### 3.1 Contrast-direction construction

For each support vocabulary $V_k$ ($k = 1..5$: Anglo, Biblical, Greek, Roman,
Modern — disjoint entity lexicons), a per-vocabulary contrast direction was
constructed at target layer $l^*$ ($l^* = 10$ for Pythia-160M, $l^* = 20$ for
Pythia-410M, both at 83% model depth):

$$\hat{v}_k = \operatorname{normalize}\!\left(\frac{1}{30}\sum_{i=1}^{30}
\frac{\Delta h_i^{(k)}}{\|\Delta h_i^{(k)}\|}\right),
\qquad \Delta h_i^{(k)} = h_{l^*}(x_i^{\mathrm{rel}}) - h_{l^*}(x_i^{\mathrm{neu}}),$$

where $h_{l^*}(\cdot)$ is the residual-stream hidden state at the last token
position. The aggregated basis is
$B_{\mathrm{agg}} = \operatorname{normalize}(\sum_k \hat{v}_k)$.
Intervention is $h \leftarrow h + \alpha u$ with $\alpha = 0.50$, applied via a
forward hook at layer $l^*$; parameters are frozen ($\Delta\theta \equiv 0$,
SHA-256 verified pre/post in every run).

### 3.2 Benchmark and endpoints

The confirmatory benchmark is $N = 60$ novel-entity 2-hop/3-hop relational
items (Planetary + Elemental domains), disjoint from all support vocabularies.
Baselines were calibrated into the pre-registered 40–70% headroom window:
EXP065 (Pythia-160M) baseline $68.33\%$ (19 rescuable errors); EXP066
(Pythia-410M) baseline $56.67\%$ (26 rescuable errors) — full headroom, so a
null result cannot be attributed to ceiling effects.

The **primary endpoint** is $\Delta M = M_{\mathrm{mod}} - M_{\mathrm{base}}$
(accuracy, percentage points) with paired decisions, tested by the McNemar
exact test on discordant counts $(b, c) = {}$(rescues, corruptions). The six
mandated conditions per run: unintervened baseline, static $B_{\mathrm{agg}}$,
"aligned" dynamic basis, same-layer output bridge
($u \propto W_U[t_{\mathrm{target}}] - W_U[t_{\mathrm{foil}}]$, a normalized
unembedding-space direction), random-rotation control (5 seeds), $B_\perp$, and
$B_{\mathrm{wrong}}$ (wrong-task contrast). Per-instance logit-margin shifts
were recorded but are **demoted to exploratory**: our own $B_{\mathrm{wrong}}$
negative control reaches Wilcoxon $p = 1.2\times10^{-8}$ with $b = c = 0$,
which invalidates margin-shift significance as evidence of task-relevant
causal effect (§5.4). Any residual-stream injection perturbs margins; only
decision flips count.

### 3.3 The Stage A alignment operator (as implemented)

EXP065/066 Stage A fit, per vocabulary pair, an orthogonal Procrustes rotation
from two unembedding-space anchor vectors and applied it to the hidden-state
contrast direction:

```python
U, S, Vh = torch.linalg.svd(E_k.T @ E_0)   # E_*: [2, d] stacks of unembedding rows
R_k = U @ Vh                                # [d, d], the "rotation"
v_aligned = R_k @ v_hat                     # v_hat: residual-stream contrast direction
```

[FACT] $M := E_k^T E_0$ is $d \times d$ but $\operatorname{rank}(M) \le 2$.
The rotation is therefore constrained on at most a 2-dimensional subspace and
implementation-defined on the remaining $d - 2$ dimensions (§6). It was fit on
**unembedding** token-identity vectors and applied to **residual-stream**
relational-reasoning directions — a cross-space transfer that was never
validated, pre-registered, or tested independently.

---

## 4. Forensic Correction: Retraction of the Procrustes Alignment Claim

Our program's summary documents — the experiment ledger
(`.muse by meta/COMPREHENSIVE_EXPERIMENT_LEDGER.md` §2.3), the handover README
(§3), and `manifest.json` — stated that "Procrustes rotation **increased**
cross-vocabulary alignment by **+0.1290** cosine similarity over raw
directions," generalized in the README to "robust geometric alignment under
closed-form Procrustes rotation ($\Delta\cos \approx +0.13$ to $+0.79$)."
On 2026-09-23, an adversarial audit recomputed every Stage A statistic
directly from the primary artifacts. The claim is **retracted**. What the
artifacts actually say:

**[OBSERVATION]** From `experiments/runs/EXP065_coordinate_alignment/exp065_results.json`
(`stage_A_alignment_discovery`), corroborated by `exp065_run_log.txt`:

| Vocabulary | raw cosine | aligned cosine | $\Delta\cos$ |
|---|---|---|---|
| V2_Biblical | $+0.7379$ | $-0.0640$ | $-0.8019$ |
| V3_Greek | $+0.7144$ | $+0.0217$ | $-0.6927$ |
| V4_Roman | $+0.6996$ | $+0.0023$ | $-0.6973$ |
| V5_Modern | $+0.7224$ | $+0.0527$ | $-0.6697$ |
| **mean** | **$+0.7186$** | **$+0.0032$** | **$-0.7154$** |

**[OBSERVATION]** From `experiments/runs/EXP066_pythia410m_replication/exp066_replication_results.json`
(`stage_A_alignment`): mean raw $+0.6852 \to$ mean aligned $-0.0118$,
**$\Delta\cos = -0.6971$**, corroborated by `exp066_run_log.txt`.

[INTERPRETATION] The claimed $+0.1290$ is irreconcilable with the primary
artifacts — sign flipped, magnitude off by $\sim$5.5×. Both flagship runs show
the Procrustes step **destroying** cross-vocabulary similarity ($\to \sim 0$),
not improving it. The "$+0.79$" figure is misattributed from EXP064's Level A
(`pre_intervention_alignment.mean_off_diagonal = 0.7927` in
`exp064_results.json`) — a *raw* aggregated-basis alignment with no rotation,
a different quantity entirely. The provenance of $+0.1290$ itself is unresolved;
no artifact in the repository produces it. We record that honestly rather than
inventing a source.

Corrections have been applied to the ledger, the handover README, and
`manifest.json` (verified: no surviving unqualified occurrence of the false
figures outside explicit retraction text), and the correction is logged in
`reports/research_log.md` under Law #12. **No primary artifact was modified.**
The consequence for the science: the "aligned dynamic basis" Stage B condition
injected a *scrambled* basis, so its $\Delta M = 0$ cannot bear on whether
*alignment* enables causal transfer — it is a methods failure, not a result
about alignment. The valid boundary evidence is the **static-basis** condition
(§5), which needed no rotation at all.

---

## 5. Results: The Boundary

### 5.1 [OBSERVATION] O1 — Raw cross-vocabulary similarity is high without any alignment

Mean pairwise cosine $\cos(\hat{v}_1, \hat{v}_k)$ over $k = 2..5$: **$+0.7186$**
(EXP065, Pythia-160M, $d = 768$), **$+0.6852$** (EXP066, Pythia-410M,
$d = 1024$); EXP064's aggregated-basis Level A gives $0.7927$ mean
off-diagonal. No rotation was applied to obtain these numbers. [NOTE] Per §2.4,
this must not be lifted out of context as "shared relational geometry":
Ethayarajh (2019) establishes strong anisotropy in contextualized
representations, and our vectors received no Jorgensen-style (2023)
mean-centring — the global-offset control the literature requires was omitted.
What O1 establishes is narrow and sufficient for the boundary argument: the
similarity was already present *before* any alignment step, so the alignment
step was never needed to produce it.

### 5.2 [OBSERVATION] O2 — The Procrustes step destroyed this similarity

Post-rotation mean cosine: $+0.0032$ (EXP065), $-0.0118$ (EXP066);
$\Delta\cos = -0.7154$ / $-0.6971$ (§4 table). §6 proves this is the
mathematically expected output of the operator as implemented, not a scale
effect or a mystery.

### 5.3 [OBSERVATION] O3 — Static injection yields zero causal transfer at full headroom

Condition "Static $B_{\mathrm{agg}}$" ($h \leftarrow h + 0.5\,B_{\mathrm{agg}}$):

| Run | $\Delta M$ | $b$ (rescues) | $c$ (corruptions) | McNemar $p$ | KL div. |
|---|---|---|---|---|---|
| EXP065 (160M) | $0.0$ pp | 0 | 0 | $1.0000$ | $0.00028$ |
| EXP066 (410M) | $0.0$ pp | 0 | 0 | $1.0000$ | $0.00017$ |

Baselines $68.33\%$ / $56.67\%$ with 19 / 26 rescuable errors — both inside the
pre-registered 40–70% window. The null is not a ceiling artifact. The EXP064
basis sweep (7 basis constructions: single-SVD, single-centroid, pool,
$B_{\mathrm{agg}}$, random, $B_\perp$, wrong-task) likewise yields $\Delta M =
0.0$, $b = c = 0$, $p = 1.0$ in every cell
(`exp064_results.json` → `condition_results`) — **but at 95% baseline, i.e.
only 3 rescuable errors**: a null there is weak, ceiling-adjacent evidence,
not headroom-verified. [CORRECTION M1, 2026-09-23] The "eleven basis
conditions" headline therefore mixes two evidential grades and must be read
with the annotation: **7 ceiling-adjacent** (EXP064) + **4 headroom-verified**
(EXP065/066: Static $B_{\mathrm{agg}}$ and "aligned" dynamic basis per run,
all $\Delta M = 0.0$, $b = c = 0$, $p = 1.0$). The strong form of the boundary
claim rests on the 4 headroom-verified conditions; the 7 EXP064 nulls are
directionally consistent but cannot carry weight on their own. EXP064's three
reversal/specificity probe conditions are **excluded** from the count — they
test specificity (whether any basis effect survives premise/polarity
reversal), not the primary static-transfer hypothesis — and two of them
registered a single non-significant rescue each ($b = 1$, $c = 0$, $p = 1.0$),
which is why the "zero decision changes" statement is scoped to the eleven.

### 5.4 [OBSERVATION] O4 — Output-space intervention at the same layer steers behavior

"Same-Layer Output Bridge" ($u \propto W_U[t] - W_U[f]$):

| Run | $\Delta M$ | rescues | corruptions | McNemar $p$ | KL div. |
|---|---|---|---|---|---|
| EXP065 (160M) | $+16.67$ pp | 10/19 | 0 | $0.0020$ | $0.0118$ |
| EXP066 (410M) | $+13.33$ pp | 8/26 | 0 | $0.0078$ | $0.0283$ |

KL divergence confirms only this condition meaningfully moves the output
distribution ($0.028$ vs $\approx 0.0002$ for all basis conditions). This is
an [OBSERVATION] of output-side steerability at layer 20 — behavior *is*
movable via output-space directions — but it is near-direct answer-logit
steering, and whether it constitutes "causal access" rather than logit
pushing is exactly what the three standing reviews are testing (LOG-149's
REVISE landing; the synthesis Cluster A Law #7 option-leakage challenge; the
synthesis Cluster C readout-tilt falsification). It must not be framed as a
control validating any representation-synthesis mechanism. (EXP064's bridge:
$+5.0$ pp, 3 rescues, $p = 0.25$, n.s. — directionally consistent,
underpowered on its own.)

### 5.5 [OBSERVATION] O5 — Margin-shift significance is not a causal endpoint

EXP066 Wilcoxon tests on per-instance logit-margin shifts:

| Condition | $\Delta M$ | McNemar $p$ | Wilcoxon $p$ | mean $\Delta$margin |
|---|---|---|---|---|
| Static $B_{\mathrm{agg}}$ | $0.0$ | $1.0$ | $0.041$ | $+0.009$ |
| "Aligned" basis | $0.0$ | $1.0$ | $1.6\times10^{-11}$ | $-0.041$ |
| Output bridge | $+0.133$ | $0.0078$ | $1.6\times10^{-11}$ | $+0.749$ |
| $B_\perp$ | $0.0$ | $1.0$ | $0.21$ | $+0.003$ |
| **$B_{\mathrm{wrong}}$ (control)** | $0.0$ | $1.0$ | **$1.2\times10^{-8}$** | $-0.021$ |

[INTERPRETATION] A "highly significant" Wilcoxon $p$ with $b = c = 0$ means
only that the intervention systematically shifted logit margins without
flipping any decision — a distributional nudge, not a causal effect. The
wrong-task negative control is significant at $p = 1.2\times10^{-8}$:
margin-shift significance is therefore not task-relevant evidence, since *any*
residual-stream injection perturbs margins. Notably, the scrambled-basis
condition shifted margins *negatively* ($-0.041$, $p = 1.6\times10^{-11}$) —
consistent with §6: a scrambled basis acts as structured noise slightly
suppressing the target logit. The raw `wilcoxon_p` fields remain in the JSONs;
we relabel them exploratory and warn against their misreading.

### 5.6 The corrected central claim

**[INTERPRETATION] I1 — the defensible boundary.** Raw geometric similarity of
relational contrast directions across disjoint vocabularies ($\approx 0.7$
cosine, no rotation) coexists with strictly zero causal transfer under static
residual-stream injection at full headroom, while output-space directions at
the same layer rescue a substantial fraction of errors. *Geometric similarity
of internal contrast directions does not imply causal interchangeability under
static injection.*

**[INTERPRETATION] I2.** The rotated-basis null is uninterpretable as an
alignment test (O2: the basis was scrambled). It contributes no evidence for
or against the boundary.

**[INTERPRETATION] I3 — scope.** I1 is established for Pythia-160M/410M,
layers at 83% depth, the $N=60$ Planetary/Elemental benchmark family, and
$\alpha = 0.50$ single-vector additive injection. Generalization beyond these
conditions is [OPEN], not implied.

---

## 6. Theoretical Analysis: Why the Alignment Operator Scrambles

The full proof is published as `theory/proofs/procrustes_failure_analysis.md`
(the first proof document in the repository; adversarially verified line by
line and SIGNED 2026-09-23). We state the load-bearing results.

### 6.1 Lemma (rank-deficient Procrustes non-uniqueness) [THEOREM]

**Lemma.** Let $M \in \mathbb{R}^{d \times d}$ with $\operatorname{rank}(M) =
r < d$ and thin SVD $M = U_r \Sigma_r V_r^T$. The minimizers of
$\|RX - Y\|_F$ over $R \in O(d)$, where $M = YX^T$, are exactly the matrices
$R = U_r V_r^T + U_0 Q_0 V_0^T$ with $Q_0 \in O(d-r)$ arbitrary.

*Proof sketch.* Minimizing $\|RX - Y\|_F^2$ is equivalent to maximizing
$\mathrm{tr}(R^T M) = \mathrm{tr}(Z\Sigma)$ with $Z = V^T R^T U \in O(d)$;
$\mathrm{tr}(Z\Sigma) = \sum_i \sigma_i z_{ii} \le \sum_i \sigma_i$ with
equality iff $z_{ii} = 1$ for all $i \le r$. An orthogonal $Z$ with
$z_{ii} = 1$ ($i \le r$) must satisfy $Z = \mathrm{diag}(I_r, Z_0)$,
$Z_0 \in O(d-r)$ — a unit-norm row with a $+1$ entry is exactly $e_i^T$.
∎

[INTERPRETATION] For EXP065/066, $r \le 2$ while $d \in \{768, 1024\}$. The
"rotation" is determined on at most a 2-dimensional subspace; on the remaining
$\ge 766$ dimensions it is an arbitrary choice of the SVD implementation
(LAPACK's null-space completion), carrying zero task information.

### 6.2 Proposition (scramble bound) [PROPOSITION]

**[ASSUMPTION] A-comp** (random-completion model): the arbitrary completion
$Q_0$ is modeled as Haar-distributed on $O(d-r)$. The Lemma shows $Q_0$ is
unconstrained by the task; the expectation below quantifies behavior over
this arbitrary degree of freedom. (Our adversarial review hardened this
wording: `torch.linalg.svd` is deterministic, so the observed cosine is one
draw from an unknown deterministic completion rule — the expectation is over
the *design space* of completions, and it is the **Lemma**, not the
Proposition, that makes the observed draw task-arbitrary.)

**Proposition.** For fixed unit vectors $v, w$:
$$\mathbb{E}_{Q_0}\big[(w^T R v)^2\big] \;=\; (w^T U_r V_r^T v)^2 \;+\;
\frac{\|P_{S^\perp} v\|^2 \,\|P_{T^\perp} w\|^2}{\,d - r\,},$$
hence deterministically
$\mathbb{E}[(w^T R v)^2] \le \|P_S v\|^2 + 1/(d-r)$, and for typical $v$
($\mathbb{E}\|P_S v\|^2 = r/d$):
$\mathbb{E}|\cos(Rv, w)| \lesssim \sqrt{(r+1)/d}$.

For EXP065/066 ($r = 2$): the bound predicts $|\cos| \lesssim 0.0625$
($d = 768$) and $\lesssim 0.0541$ ($d = 1024$); the observed values are
$+0.0032$ and $-0.0118$ — inside the predicted scramble band. **Caveat
(T-1):** the $\sqrt{(r+1)/d}$ numerics assume genericity of the empirical
directions w.r.t. the anchor subspace; $\|P_S \hat{v}_k\|$ is not computable
from the stored artifacts (the JSONs hold scalar summaries only; no vector
dumps exist — a reproducibility gap our Law #13 now requires future runs to
close). The deterministic bound holds regardless; the numerics are
illustrative scale, honestly labeled.

### 6.3 The unstated cross-space assumption

**[ASSUMPTION] A-cross (reconstructed; was unstated):** a rotation aligning
token-identity geometry in *unembedding* space transfers to
relational-reasoning directions in the *residual stream*. It was never
validated; Stage A ($\Delta\cos \approx -0.72/-0.70$) contradicts it in this
operationalization. Its salvageable core — a *uniformity* claim that a
vocabulary-renaming rotation estimated from same-space correspondences acts
uniformly on relational directions — is exactly what EXP067 tests, via a
Stage A gate computed on held-out relational directions (named
[ASSUMPTION] A-uniform in the protocol). Note the two defects are
independent: even full-rank anchors would leave A-cross unvalidated, and even
same-space fitting would leave a rank-2 fit scrambling. EXP067 fixes both.

---

## 7. Mechanism: The Null-Space Explanation Is Dead — Readout-Misalignment-or-Unknown

The boundary (I1) survives; the mechanism the program used to *explain* it
does not. This section records the retraction, states what the evidence now
supports, and names — with epistemic labels — what remains unknown.

### 7.1 The retracted explanation

The program's handover records stated, as the "Core Causal Null-Space
Theorem"
(`.muse by meta/THEORY_AND_MATHEMATICAL_FOUNDATIONS.md` §3.3), the following
explanation for the boundary (quoted verbatim; **RETRACTED 2026-09-23 by G1,
see below**):

> Rotating $B_{\mathrm{agg}}$ via $R(x)$ aligns the vector in the ambient
> embedding space $\mathbb{R}^d$, but **fails to align with the specific
> query/key projection matrices $W_Q^{(l+1)}, W_K^{(l+1)}$ of downstream
> attention heads**. The downstream heads project $b_{\mathrm{dynamic}}$ into
> their null space or treat it as off-manifold noise, resulting in zero
> behavioral rescue.

**[OBSERVATION]** (FACT) G1 (`research/analysis_plans/G1_REPORT_2026-09-23.md`,
LOG-134) tested this as a weight-only QK/OV projection-energy audit on
pythia-410m (injection at L20; all 48 heads in layers 21–23;
torch.float32; CPU; $\Delta\theta = 0$ SHA-256-confirmed). Pre-registered
decision rule: $\bar{E}_{\mathrm{QK}}(B_{\mathrm{agg}}) \ge
\bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}})$ → KILL. The rule fired:

| Quantity | Value |
|---|---|
| $\bar{E}_{\mathrm{QK}}(B_{\mathrm{agg}})$ | $0.389985$ |
| $\bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}})$ | $0.356185$ |
| Null (100 draws, seed 20260923): $q_{0.05}$ / $q_{0.95}$ / mean | $0.341099$ / $0.361730$ / $0.352333$ |
| $p_{\mathrm{low}}(B_{\mathrm{agg}})$ / $p_{\mathrm{high}}(b_{\mathrm{mean}})$ | $1.0000$ / $0.2277$ |
| Verdict | **KILL** |

Source: `research/analysis_plans/G1_RESULTS_2026-09-23.json`. The ordering is
the exact reverse of the theorem's prediction: the failed direction is
unusually QK-*visible* — every one of the 100 null draws had lower energy
($p_{\mathrm{low}} = 1.0$) — while the rescuing bridge is QK-*unremarkable*
($p_{\mathrm{high}} = 0.23$, mid-null). $B_{\mathrm{agg}}$ beats the bridge in
35 of 48 heads with weak cross-head correlation ($r = 0.27$, i.e. the two
directions are visible to *different* heads). The OV secondary corroborates
($\bar{E}_{\mathrm{OV}}(B_{\mathrm{agg}}) = 0.406759$ vs
$\bar{E}_{\mathrm{OV}}(b_{\mathrm{mean}}) = 0.353308$, null band
$0.3466$–$0.3590$). The $s_j$ companion rejects "maximize QK-projection
energy" as a sufficient-condition design objective
(median$_j \bar{E}_{\mathrm{QK}}(s_j) = 0.356201$ vs $0.356185$;
$\bar{E}_{\mathrm{QK}}(\bar{s}) = 0.367099$). And $B_{\mathrm{wrong}}$ carries
QK energy $0.488475$ with $\Delta M = 0$ — the cleanest single-vector proof
that "visible to attention" $\neq$ "causal."

**[INTERPRETATION]** (INFERENCE) The theorem's central sentence — downstream
heads project the failed direction into their null space while granting the
bridge large energy — is **Refuted** as a QK-subspace claim. Scope of the
refutation: G1 measures QK/OV projection energy, not the full downstream
Jacobian (disclosed [ASSUMPTION] A-G1-linear); what is dead is the specific
null-space downstream-filtering mechanism, not the proposition that
downstream processing matters at all.

### 7.2 The boundary survives on its endpoints

G1 touches mechanism, not measurement. I1 — raw similarity $\approx 0.7$
coexists with zero causal transfer under static injection while the output
bridge rescues — rests on endpoints, and every endpoint has since been
re-tested:

- **EXP065/066** (§5.3–§5.4): static $B_{\mathrm{agg}}$ $\Delta M = 0.0$ pp
  ($b = c = 0$, McNemar $p = 1.0$) at 68.33%/56.67% baselines with 19/26
  rescuable errors; output bridge $+16.67$ pp (10/19, $p = 0.0020$) and
  $+13.33$ pp (8/26, $p = 0.0078$).
- **EXP077** (2×Tesla T4, executed 2026-09-23; **evaluator ruling (verbatim):
  branch (c) NEITHER**, flat-zero trigger): no static geometric variant of
  the concept direction moved decisions — radial sweep
  $\alpha \in \{0.25, 0.5, 1.0, 2.0\}$ all $\Delta M = 0.00$ pp, $p = 1.0$
  (Holm-adjusted, $S_H = \varnothing$); angular (cone vs line,
  $\rho = 30^\circ$, $K = 8$) $b = c = 0$, $p = 1.0$; control (cone vs
  control) $b = c = 0$, $p = 1.0$; offset $b = c = 0$, $p = 1.0$;
  replication $b = c = 0$, $p = 1.0$; baseline 0.5667. The output-bridge
  gate PASSED: $+10$ pp ($b = 6$, $c = 0$, $p = 0.03125$). Source: verbatim
  evaluator ruling recorded in `reports/research_log.md` (LOG-128); the
  in-repo archive `experiments/runs/EXP077_cone_vs_line/` (the CPU-smoke run)
  shows a statistically-flat null (angular b=2, c=1, p=1.0) with a stronger
  bridge rescue
  ($+23.33$ pp, $b = 14$, $c = 0$, $p = 0.000122$, baseline 0.60 —
  `exp077_results.json`).

  [NOTE] Branch (c) kills *only* the tested $\rho = 30^\circ$ unconditional
  cone and $\alpha = 1.0$ offset hypotheses, at pythia-410m/layer-20 on this
  benchmark; other radii and gated/conditional variants survive (protocol
  §8/§11).

**[INTERPRETATION]** (INFERENCE) I1: **Supported** — the boundary is now five
experiments deep (EXP064 null, EXP065/066 headroom-verified nulls, EXP067
halt, EXP077 flat-zero across cone/line/offset/radial) with the output bridge
rescuing in every run where it appears.

### 7.3 The bridge's rescue: mechanism unknown

**[OBSERVATION]** (FACT) The bridge $u \propto W_U[t_{\mathrm{target}}] -
W_U[t_{\mathrm{foil}}]$ moves decisions in every run it appears (EXP065
$+16.67$ pp, EXP066 $+13.33$ pp, EXP077 GPU $+10$ pp), and it is
QK-unremarkable: it never needed privileged QK access, and it doesn't have
any (G1 Finding 4, unchallenged by this audit). No intervention has measured
*why*.

The competing live possibilities, honestly labeled — none promoted to
[INTERPRETATION] of a fact:

1. **[HYPOTHESIS] Readout bypass / near-direct logit steering.** The bridge
   works because it is constructed in unembedding space and the residual
   stream preserves a near-direct linear bypass to the unembedding layer —
   it directly tilts answer logits. (The program's audit Finding 4; G1 does
   not challenge it. Untested by intervention.)
2. **[HYPOTHESIS] Different direction family.** The causal object is not a
   residual-geometry contrast direction at all: relational contrast
   directions live in a different direction family than answer-logit
   differences, and only the latter engage the decision — the transferable
   direction lives output-side, not in the concept geometry.
3. **[CONJECTURE] Downstream attenuation of static offsets.** LayerNorm-scale
   attenuation, attention-softmax saturation, or value-path misalignment.
   These survive G1 because they are linear-probe-invisible by construction
   (A-G1-linear), so the audit cannot discriminate them; they need
   interventional designs, not more projection-energy audits (G1 §6).

**[INTERPRETATION]** (INFERENCE) Evidentiary status of the bridge's mechanism:
**Underdetermined**; this paper claims no mechanism. [NOTE] The bridge's
positive-control status is under three standing attacks, and until they rule,
its rescue licenses only the empirical observation, not any of the three
hypotheses above: (1) the LOG-144 C-A entity-similarity review has LANDED as
REVISE (LOG-149) — the 10-token answer pool makes donor/test answer-token
overlap structural, with leakage as the null hypothesis; (2) the A–J
synthesis's Cluster A filed a Law #7 option-leakage challenge against the
bridge; (3) the synthesis's Cluster C proposed a readout-tilt label-shuffle
falsification of the rescue. The question is no longer only "genuine
output-side transfer or logit steering" but whether the bridge can serve as a
validity-bearing positive control at all. On the program's three evidentiary
levels ("can improve inference" ≠ "changes the computational strategy" ≠
"creates qualitatively new capability"), the paper establishes only the
first — for the bridge, empirically — and refuses the other two.

**Program consequence** (licensed by the G1 plan §7 kill): the QK-subspace
operator program is **stood down** — no further compute on designing
QK/OV projection-energy objectives, including "maximize QK-projection
energy," which the $s_j$ companion independently rejected.

### 7.4 What EXP067's halt means for mechanism

§8 records the execution. The mechanism-relevant consequence: the program's
"sound full-rank Procrustes" operationalization — the last licensed attempt
to test whether *alignment quality* was the missing ingredient — proved
underdetermined by its own anchor design (80 anchors span only ~33 of the 64
head-subspace dimensions). The D1 rank-deficiency defect (§6) was never
fixable under this anchor design, and no mechanism test may now be run
under the EXP067 label. A redesigned sound-alignment test would take a new
experiment number; until one exists, the paper's mechanism claim stands at
readout-misalignment-or-unknown.

---

## 8. EXP067: Executed Boundary Experiment — Pre-registered Halt at Stage A

**Status: EXECUTED 2026-09-23** (2×Tesla T4, 70.79 s, notebook
exp067-qkov-subspace v1, verified bundle 1ff9606b…). Protocol authority
remains `experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md`
(adversarially SIGNED 2026-09-23). We summarize the design as pre-registered,
then record the outcome; the protocol is the authority.

**Research question.** Does a *sound* Procrustes alignment operator enable
causal transfer of cross-vocabulary relational bases where the unsound
EXP065/066 operator could not?

**[HYPOTHESIS] H1** (as pre-registered — quoted as a design statement, not
adopted as fact). A Procrustes rotation that is (a) fit in the *same* space
as the intervention — per-head attention OV output subspaces
$S_h = \mathrm{col}(W_O^{(h)})$, $\dim 64$, at layer 20 of Pythia-410M — and
(b) *full-rank-constrained* ($m = 80$ same-space anchors $\ge d_h = 64$,
runtime rank/spectral-gap guards, explicit identity on the orthogonal
complement) produces $\Delta M > 0$ with McNemar $p < 0.05$ on the same
$N=60$ headroom-calibrated benchmark.

**Scope (boundary science, not novelty science).** EXP067 determines whether
the I1 dissociation survives a fair, sound-operator test. Its outcome
**cannot move the novelty needle in either direction**: a positive result
would be a better-executed instance of an N0 mechanism (CAA-equivalent); a
null confirms the boundary. The per-instance
$\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop is explicitly out of
scope.

**Outcome — evaluator ruling (verbatim): BRANCH STAGE_A_HALT.** The
pre-registered rank/spectral guard fired before any baseline: head 0, pair
V1→V2_Biblical — rank = 33 (required ≥ 64), spectral gap = 1.59e-08,
reproducing the CPU smoke prediction (gap 1.44e-08) within 10%,
device-independent as predicted. Baseline n/a (halted before baseline).
Only two files were produced (halt before the archive stage):
`exp067_results.json` (4bef6dc6…, 924 B), `exp067_run_log.txt` (118c9c4f…,
2139 B); the result records live in `reports/research_log.md`. The GPU
sanity hash matched the registered manifest value exactly (4c242d9a…5ed48dd,
sanity PASSED) and $\Delta\theta = 0$ was confirmed (pre == post) — the
binding guard passed in its strongest form.

**Pre-registered ruling for branch (a):** H1 is *untestable under this
operationalization* — neither falsified nor confirmed. I1 stands
unchallenged.

**[OBSERVATION]** The "sound" operationalization is underdetermined: 80
anchors span only ~33 of the 64 head-subspace dimensions for head 0 — so the
D1 rank-deficiency defect (§6) was never actually fixable under this anchor
design. **[INTERPRETATION]** (INFERENCE) This closes the alignment-quality
path as operationalized. Tweak-and-rerun under the EXP067 label is
explicitly forbidden by the protocol (§7.2): an adjusted design is a new
experiment number, so the guard cannot become p-hacking-adjacent. A
redesigned sound-alignment test would need anchors that actually span the
head subspace — and, after G1 (§7.3), the program is no longer licensed to
pursue alignment quality as the lever in QK/OV subspace at all. The canonical
falsification criterion (protocol §7.0) and the full decision tree were never
exercised; branch (a) fired first, and the protocol binds us to report
exactly that.

---

## 9. Limitations

We enumerate what this paper does not establish, because a boundary paper that
hides its boundaries is not one.

1. **Statistical endpoints.** The Wilcoxon-on-logit-margins endpoint is
   invalidated as a causal measure by our own $B_{\mathrm{wrong}}$ control
   ($p = 1.2\times10^{-8}$, $b = c = 0$); it is reported as exploratory only.
   All causal claims rest on McNemar exact tests of paired decisions.
2. **Anisotropy and centring.** O1's raw cosine $\approx 0.7$ was measured
   without Jorgensen-style mean-centring; under Ethayarajh (2019) anisotropy,
   part of this similarity may be a global offset rather than relational
   structure. Template-ablation controls are [OPEN] (formalization Q2).
3. **T-1 data-grounding.** The scramble-bound numerics are illustrative until
   a future run archives raw anchor/contrast vectors; the deterministic bound
   is unaffected.
4. **Scope.** I1 covers Pythia-160M/410M, 83%-depth layers, one benchmark
   family, $\alpha = 0.50$ single-vector injection. No claim is made beyond
   these conditions — including any claim about "superhuman" capabilities.
5. **The loop is untested.** Nothing in this paper bears on whether a
   per-instance $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop would
   work; no such loop has been executed. The Self-Refine blind-spot finding
   (Madaan et al., 2023) is a standing falsifier-risk for any future internal
   evaluator $\mathcal{E}$.
6. **Bookkeeping.** The experiment ledger claims EXP001–EXP066; the runs
   directory contains 61 directories (EXP001–EXP006 bundled; EXP051 and
   EXP055 absent). The inventory gap is annotated, not reconciled.
7. **Compute.** EXP067 executed 2026-09-23 (2×Tesla T4) and halted at its
   pre-registered Stage A guard (branch (a)); the sound-alignment
   operationalization proved underdetermined and H1 untestable (§8).
8. **G1 scope.** G1 measures QK/OV projection energy, not the full downstream
   Jacobian (disclosed [ASSUMPTION] A-G1-linear); what it refutes is the
   specific null-space downstream-filtering mechanism (§7.1), not the
   proposition that downstream processing matters.
9. **The bridge's mechanism is [OPEN].** This paper records no mechanism for
   the bridge's rescue (§7.3: **Underdetermined**); it claims only the
   empirical fact that it rescues.
10. **EXP077 kill scope.** Branch (c) kills only the tested
    $\rho = 30^\circ$ unconditional cone and $\alpha = 1.0$ offset hypotheses
    at pythia-410m/layer-20; other radii and gated/conditional variants
    survive and are untested.

---

## 10. Future Work

Three paths are open, in order of how much of the program's honesty they
preserve.

1. **EXP067 is executed (branch (a) halt).** The sound-alignment path as
   operationalized is closed: 80 anchors span only ~33 of the 64
   head-subspace dimensions (§8), and the QK-subspace operator program is
   stood down after G1 (§7.3). A sound-alignment test would need anchors that
   actually span the head subspace — under a new experiment number, with a
   new pre-registration. The next mechanistic questions
   (LayerNorm-scale attenuation, attention-softmax saturation, value-path
   misalignment) are linear-probe-invisible by construction (G1 §6); they
   need *interventional* designs, not more projection-energy audits.
2. **Locate the break.** With the QK-subspace account ruled out as the gate
   (§7.1), the next science is mechanistic, not methodological — but this
   paper licenses no leg of it: every candidate in §7.3 is
   [HYPOTHESIS]/[CONJECTURE], awaiting designs that can discriminate them.
3. **Specify, then test, the loop.** The only path to a novelty-relevant
   claim is an operational $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$
   specification — which does not currently exist in any form — followed by a
   demonstration that beats compute-matched baselines (self-consistency,
   Best-of-N, Tree of Thoughts) on reasoning tasks with $\Delta\theta = 0$.
   PPLM, ToT, and Self-Refine are the explicit design priors it must
   distinguish itself from; the Brown et al. verifier ceiling and the
   Self-Refine blind-spot finding are its standing falsifiers. Until the spec
   exists on paper, no loop experiment may be pre-registered — that is how
   the next forensic audit gets written.

What cannot make the program interesting: a positive EXP067 C3 presented as a
novel method (it would be well-executed CAA), or any manuscript containing
the words "invented," "novel mechanism," or "superhuman" adjacent to the
tested static mechanism.

**Submission posture.** Per our own adversarial review's standing
recommendation, this manuscript in its current form is workshop-suitable;
main-track submission awaits either a mechanism-resolving experiment (the
bridge's rescue is currently Underdetermined, §7.3) or a boundary result
that extends I1 beyond these conditions — and we bind the program to that
standard here, in print.

---

## 11. Conclusion

Raw geometric similarity ($\approx 0.7$ cosine) of relational contrast
directions across disjoint vocabularies does not yield causal transfer under
static residual-stream injection ($\Delta M = 0$, $b = c = 0$, two scales,
eleven basis conditions — 4 headroom-verified, 7 ceiling-adjacent; see §5.3
annotation; EXP077 adds a further eight geometric-variation conditions, all
flat zero — see §7.2), while output-space directions at the
same layer rescue up to 10/19 errors — and, in EXP077, no static geometric
variant of the concept direction moved a single decision (branch (c)
NEITHER, §7.2) while the bridge rescued again. The alignment step that was
supposed to bridge the two was provably unsound — a rank-$\le 2$ Procrustes
fit on unembedding anchors applied to full-rank residual-stream directions,
which our Lemma shows can only scramble — and our own summary documents
misreported its effect with the sign flipped. We retracted it, proved why it
failed, executed the sound-alignment test that was supposed to replace it
(it halted at its own guard, §8), and — in §7 — retracted the program's
null-space downstream-filtering explanation too: G1 showed the failed
direction is *more* QK-visible than the rescuing bridge, the exact inversion
of the old theorem. The tested
mechanism is algorithmically equivalent to Contrastive Activation Addition;
we claim no novelty for it, and we claim no mechanism for the bridge's
rescue (§7.3: **Underdetermined**). What we claim is the boundary, carefully
measured and honestly labeled: *here is what static steering cannot do, here
is the proof that our earlier attempt to say otherwise was wrong, and here
is the list of explanations we have now ruled out.*

---

## 12. Revision Note — 2026-09-23 (LOG-145, authorized rewrite)

Per the program's retraction culture (research/RESEARCH_OPERATING_SYSTEM.md
§3), this rewrite is recorded explicitly; superseded wording is preserved
below with its retraction, never silently edited.

**What changed in this revision.** (1) New §7 "Mechanism" replaces the
program's null-space downstream-filtering explanation with
**readout-misalignment-or-unknown**: the boundary claim I1 stands on its
endpoints; the bridge's mechanism is recorded as unknown (Underdetermined);
the QK-subspace operator program is stood down. (2) §8 records EXP067's
execution outcome (branch (a) Stage A halt). (3) Abstract, §1, §9, §10, §11,
and the Data statement updated to absorb EXP067/EXP077 and G1.

**Why.** G1 (LOG-134, `research/analysis_plans/G1_REPORT_2026-09-23.md`)
returned **KILL** — the failed direction is *more* QK-visible than the
rescuing bridge, the exact inversion of the handover's Core Causal Null-Space
Theorem (§3.3). EXP077 executed on GPU with **branch (c) NEITHER** (flat
zero across cone/line/offset/radial; bridge gate passed at +10 pp). EXP067
executed on GPU with **BRANCH STAGE_A_HALT** (rank 33 of 64, gap 1.59e-08).
This dispatch was explicitly sequenced by the CEO (LOG-135: absorb
EXP077/067, hold the mechanism rewrite until G1 lands); G1 has landed, and
this rewrite is its authorized execution.

**Retracted / superseded wording (preserved verbatim):**

1. The handover "Core Causal Null-Space Theorem"
   (`.muse by meta/THEORY_AND_MATHEMATICAL_FOUNDATIONS.md` §3.3): *"The
   downstream heads project $b_{\mathrm{dynamic}}$ into their null space or
   treat it as off-manifold noise, resulting in zero behavioral rescue."*
   **Status: Retracted as a QK-subspace claim by G1 (2026-09-23).** It is
   preserved in the handover corpus per signed-artifact immutability; this
   paper no longer endorses it.
2. The paper's prior §7 status line: *"Status: PRE-REGISTERED, not
   executed"* (of EXP067). **Status: Superseded — EXP067 executed
   2026-09-23; see §8.**
3. The paper's prior pivot sentence (§7): *"the program pivots to locating
   the break (QK routing vs OV transport vs MLP readout) rather than
   improving alignment."* **Status: Superseded — the QK leg of that pivot is
   closed by G1 (§7.1); the QK-subspace operator program is stood down
   (§7.3).** The remaining candidates (LayerNorm-scale attenuation,
   attention-softmax saturation, value-path misalignment) survive only as
   [CONJECTURE] (§7.3).
4. The prior §9 Future Work item 1: *"Execute EXP067"* — **superseded by
   execution (§8).** The prior §9 item 2 ("If EXP067 nulls…") —
   **superseded**: the ruling was a halt, not a null (H1 untestable, neither
   falsified nor confirmed).

No primary artifact was modified by this revision. Every number in §7–§8 was
re-verified against the artifacts named in the Data statement (Law #2); no
number without an artifact trace survives in the rewritten sections.

**Post re-review addendum (LOG-156 → LOG-162, 2026-09-23).** The Law #14
re-review of this rewrite (`reports/adversarial_review_paper_rewrite_2026-09-23.md`)
returned **SIGN-WITH-FIXES** — all re-verified numbers matched primary
artifacts, the retraction was complete, I1 endpoint-scoped, the bridge
Underdetermined, labels/verdicts compliant. Three wording fixes were applied
verbatim as directed: (F1) the §7.3 caveat no longer says "currently testing"
and now names all three standing attacks on the bridge's positive-control
status (the LOG-144 review's REVISE landing at LOG-149; the synthesis
Cluster A Law #7 option-leakage challenge; the synthesis Cluster C
readout-tilt falsification); (F2) §5.4's "legitimate 'causal access exists at
this layer'" was demoted to an [OBSERVATION] of output-side steerability,
pending those reviews; (F3) §7.2's "same flat-zero pattern" now reads
"statistically-flat null" (smoke angular b=2, c=1, p=1.0). With these fixes,
the draft is cleared for external use; submission or circulation remains the
user's decision. Process finding (adopted program-wide): the re-review noted
§12 items 2–4 above were unverifiable because the pre-rewrite draft was never
committed — future rewrites must snapshot the pre-rewrite draft first.

---

## Data and Reproducibility Statement

Primary artifacts (unmodified throughout this program; corrections touched
only summary documents):

- `experiments/runs/EXP064_lexical_invariant_basis/exp064_results.json` (+ run log)
- `experiments/runs/EXP065_coordinate_alignment/exp065_results.json` (+ run log)
- `experiments/runs/EXP066_pythia410m_replication/exp066_replication_results.json`,
  `exp066_instance_evaluations.json` (+ run log)
- Run scripts: `experiments/scripts/run_exp065_temporary_coordinate_alignment.py`,
  `experiments/scripts/run_exp066_pythia410m_replication.py`
- Forensic audit: `reports/adversarial_audit_exp065_exp066.md` (2026-09-23)
- Literature audit: `research/literature/audit_2026-09-23.md` (24 verified records)
- Novelty report: `reports/novelty_report.md` (N1, adversarially SIGNED)
- Formalization: `theory/BOUNDARY_CLAIM_FORMALIZATION.md`
- Proof: `theory/proofs/procrustes_failure_analysis.md` (Lemma [THEOREM], SIGNED)
- EXP067 protocol: `experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md`
  (PRE-REGISTERED, SIGNED) — **executed 2026-09-23, BRANCH STAGE_A_HALT**;
  result records in `reports/research_log.md` (verbatim evaluator ruling;
  run files `exp067_results.json` (4bef6dc6…), `exp067_run_log.txt`
  (118c9c4f…) produced at halt)
- G1 weight-only audit (2026-09-23, KILL): `research/analysis_plans/G1_REPORT_2026-09-23.md`,
  `research/analysis_plans/G1_RESULTS_2026-09-23.json` (unrounded numbers),
  `research/analysis_plans/G1_PLAN.md` (re-frozen), executor
  `research/analysis_plans/G1_execute_2026-09-23.py`
- EXP077 cone-vs-line (executed 2026-09-23, **branch (c) NEITHER**):
  `experiments/runs/EXP077_cone_vs_line/exp077_results.json` (+ instance
  records, run log, vectors.pt); GPU evaluator ruling recorded verbatim in
  `reports/research_log.md` (LOG-128); protocol
  `experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md`
- Review: `reports/adversarial_review_wave2_2026-09-23.md` (15/15 gates, SIGNED)

All models frozen ($\Delta\theta = 0$, SHA-256 pre/post per run). Seeds pinned
per run scripts. No new model execution was performed in this drafting phase;
every number above is recomputed from stored artifacts.

---

## References

- Arditi, A., et al. (2024). Refusal in Language Models Is Mediated by a Single Direction. arXiv:2406.11717.
- Bansal, Y., Nakkiran, P., & Barak, B. (2021). Revisiting Model Stitching to Compare Neural Representations. NeurIPS 2021.
- Belitsky, M., et al. (2025). KV Cache Steering for Controlling Frozen LLMs. arXiv:2507.08799.
- Braun, J., et al. (2025). Understanding (Un)Reliability of Steering Vectors in Language Models. ICLR 2025 Workshop on Foundation Models in the Wild. arXiv:2505.22637.
- Brown, B., et al. (2024). Large Language Monkeys: Scaling Inference Compute with Repeated Sampling. arXiv:2407.21787.
- Chuang, Y.-S., et al. (2024). DoLa: Decoding by Contrasting Layers Improves Factuality. ICLR 2024. arXiv:2309.03883.
- Dathathri, S., et al. (2020). Plug and Play Language Models. ICLR 2020. arXiv:1912.02164.
- Ethayarajh, K. (2019). How Contextual are Contextualized Word Representations? EMNLP 2019. arXiv:1909.00512.
- Geiger, A., et al. (2024). Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations. CLeaR 2024.
- Jorgensen, O., et al. (2023). Improving Activation Steering in Language Models with Mean-Centring. arXiv:2312.03813.
- Li, K., et al. (2023). Inference-Time Intervention: Eliciting Truthful Answers from a Language Model. NeurIPS 2023. arXiv:2306.03341.
- Madaan, A., et al. (2023). Self-Refine: Iterative Refinement with Self-Feedback. NeurIPS 2023. arXiv:2303.17651.
- Mikolov, T., Le, Q. V., & Sutskever, I. (2013). Exploiting Similarities among Languages for Machine Translation. arXiv:1309.4168.
- Rimsky, N., et al. (2024). Steering Llama 2 via Contrastive Activation Addition. ACL 2024. arXiv:2312.06681.
- Smith, S. L., et al. (2017). Offline Bilingual Word Vectors, Orthogonal Transformations and the Inverted Softmax. ICLR 2017. arXiv:1702.03859.
- Subramani, N., Suresh, N., & Peters, M. (2022). Extracting Latent Steering Vectors from Pretrained Language Models. Findings of ACL 2022. arXiv:2205.05124.
- Tan, D., et al. (2024). Analyzing the Generalization and Reliability of Steering Vectors. NeurIPS 2024. arXiv:2407.12404.
- Todd, E., et al. (2024). Function Vectors in Large Language Models. ICLR 2024. arXiv:2310.15213.
- Turner, A. M., et al. (2023). Steering Language Models With Activation Engineering. arXiv:2308.10248.
- Wang, X., et al. (2023). Self-Consistency Improves Chain of Thought Reasoning in Language Models. ICLR 2023. arXiv:2203.11171.
- Wu, Z., et al. (2024). ReFT: Representation Finetuning for Language Models. arXiv:2404.03592.
- Yao, S., et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023. arXiv:2305.10601.
- Zou, A., et al. (2023). Representation Engineering: A Top-Down Approach to AI Transparency. arXiv:2310.01405.

---

*End of draft. Status: manuscript draft for internal review — not submitted, not circulated.
Next gate: adversarial review of this draft before any external use (Law #14).*
