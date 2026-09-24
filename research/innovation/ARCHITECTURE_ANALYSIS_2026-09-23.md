# Architecture Analysis — LOG-201 (2026-09-23)

**Role:** Track-2 mechanistic-interpretability analyst (with theory support)
**Commission:** LOG-201 — architecture analysis track (CPU / $0, docs only)
**Inputs read before writing (knowledge protocol discharged):**
`research/innovation/PARADIGM_AUDIT_2026-09-23.md` (full),
`research/innovation/SPRINT3_CANDIDATES_2026-09-23.md` (full),
`research/innovation/DIRECTION_DECISION_2026-09-23.md` (full),
`research/analysis_plans/G1_REPORT_2026-09-23.md` (full),
`~/workspace/SCBI/AGENTS.md` (§2 laws, §5 labeling standard).
**Cost:** $0 GPU. No code written, no weights touched, no forward passes run.
One read-only `config.json` inspection of the locally cached checkpoint (CPU).
No signed artifact modified. Δθ=0 throughout.
**Epistemic standard (binding):** every load-bearing claim carries
FACT / INFERENCE / HYPOTHESIS / SPECULATION (mentor canonical layer) +
the repo 10-label standard (AGENTS.md §5) + evidentiary level L1/L2/L3.
Verdicts use ONLY: Supported / Not supported / Inconclusive / Underdetermined / Refuted.
**Grading key for architectural arguments (Law #15 Q4):**
`[STRUCTURAL]` = follows from the architecture's mathematics (residual paths,
linear readout, dimensional arithmetic) modulo stated caveats;
`[ANALOGY]` = borrowed from interpretability literature or mechanistic intuition,
not derived — honest about it;
`[THEOREM]` = none claimed in this document (stated explicitly where the
temptation arises).
Law #3: no fabricated citations. Claims about external literature not in the
program's verified corpus are tagged UNVERIFIED and never load-bearing.

---

## 0. Grounded architecture facts (the substrate under analysis)

[FACT]/[OBSERVATION] — read 2026-09-23 from the locally cached checkpoint
config (`~/.cache/huggingface/hub/models--EleutherAI--pythia-410m/.../config.json`;
read-only, no weights loaded):

| Property | Value |
|---|---|
| Architecture | GPTNeoXForCausalLM (GPT-NeoX) |
| Layers | 24 (indices 0–23) |
| Hidden size d | 1024 |
| Attention heads | 16 → head dim 64 |
| MLP intermediate | 4096 |
| Vocabulary | 50304 |
| Rotary | 25% of head dims (16 of 64 dims carry position) |
| Block structure | **parallel** attention + MLP branches summed into the residual stream |

[FACT] (GPT-NeoX block math): x_{l+1} = x_l + Attn(LN₁(x_l)) + MLP(LN₂(x_l)).
[FACT] (G1 §2, verified against installed transformers 5.17.0 source): the fused
QKV weight is per-head interleaved at stride 192 (rows [192h,192h+64) = Qʰ,
[192h+64,192h+128) = Kʰ, [192h+128,192h+192) = Vʰ); the dense output projection
is blocked-column per head (W_Oʰ = cols [64h,64h+64)).
[FACT] (G1 §1): injection at L20 leaves exactly 3 downstream blocks
(layers 21–23) = **48 downstream attention heads** before the final LayerNorm
and the unembedding readout.
[FACT] (G1 §4): the MLP up-projection (4096×1024) is full row-rank (rank 1024);
Ē_MLP ≈ 1.000000 for every tested vector — the MLP filters nothing.
[FACT] (math): for d=1024, the chance cosine band for random unit vectors is
σ = 1/√d ≈ 0.031 (≈ ±0.061 at 95%).

These are the load-bearing structural facts. Everything in §1–§2 is argued
from them, not from the program's history.

> **[CORRECTION ADDENDUM 2026-09-23 — Law #14 review LOG-203, fix F-201-1.]**
> The analysis as first written rests on a uniform "Pythia-410m / layer 20"
> substrate narrative. That narrative is **false for half the cited experimental
> record**. Verified against the runner sources (Law #14 LOG-203):
>
> | Experiment | Actual model (runner-pinned) | Injection layer | Downstream blocks | Runner source |
> |---|---|---|---|---|
> | EXP065 | `EleutherAI/pythia-160m` | **Layer 10** (concept extraction *and* bridge arm) | 1 of 12 | `run_exp065_temporary_coordinate_alignment.py` l. 77 (model), l. 95 (layer), ll. 483–491 (bridge at Layer 10) |
> | EXP070 | `EleutherAI/pythia-160m` | **Layer 10** ("l* = 10 (83% depth, matching EXP065)") | 1 of 12 | `experiments/runs/exp070/run_exp070.py` l. 83 (model), l. 86 (layer) |
> | EXP066 | `pythia-410m` | Layer 20 | 3 of 24 | as assumed |
> | EXP077 | `pythia-410m` | Layer 20 | 3 of 24 | as assumed |
>
> Consequences, applied through §§1–2: (a) EXP065's bridge rescue (ΔM=+16.67pp,
> p=0.001953125) happened at **L10 of a 12-layer model — one block from the
> readout**, where the residual-bypass channel is even more dominant than at
> 410m/L20 and the "48-head routing" discussion does not apply (160m has 12
> heads/layer, not 16); (b) §1.2's "At L10, by contrast, 14 downstream blocks
> (224 heads)" is about **410m**/L10 — the program's actual L10 injections were
> all on the 12-layer model; the two must not be conflated; (c) the convenience
> verdict is *strengthened*, not weakened: EXP066's runner pins the inheritance
> explicitly — `target_layer = 20  # Equivalent proportional depth (83.33%) to
> Layer 10 on 160M` — i.e., L20 was inherited via fractional-depth mapping from
> the original 160m/L10 experiment, never localized. The "inherited without any
> localization study" claim stands, now with the inheritance receipt attached.
> Where §§1.2/1.5 state channel arithmetic, read it as 410m-scoped unless the
> (model, layer) pair is named. Ground 1's "L8/L12/L16 at 410m" proposal is
> genuinely untested — the program's mid-layer injections were all on the
> 12-layer model. [FACT — corrections, runner-pinned]

---

## 1. Is Pythia-410m / layer 20 a principled choice or a convenience choice?

### 1.1 Where steering-relevant computation lives in a 24-layer decoder

"Steering-relevant" conflates three distinct loci. The program never separated
them, and the experimental record is exactly what that conflation predicts:

- **(i) Concept formation** [ANALOGY]: where relational content is computed —
  attention moves entity information to the scoring position and mid-network
  blocks compose it. By every mechanistic account of relational reasoning, this
  is a *mid-network* object (roughly layers 8–18 of 24): early layers are
  token/positional/syntactic, late layers sharpen toward the readout.
  (The logit-lens literature is the usual evidence for this depth profile;
  specific citations UNVERIFIED in-program — the claim is graded analogy, and
  the program's own $0 test for it is proposed in §3.1.)
- **(ii) Concept addressability** [INFERENCE from G1]/[OBSERVATION]: where an
  injected direction is *legible to downstream computation* — i.e., some
  attention head's QK/OV machinery or MLP gate actually routes it. G1 measured
  this directly at L20 and found the predicted ordering **inverted**: the
  failed B_agg is unusually QK-visible (Ē_QK = 0.390 > null q95 = 0.362),
  the rescuing bridge is QK-unremarkable (0.356, mid-null), and B_wrong is the
  most QK-visible of all (0.4885) with ΔM = 0. **Verdict on the addressability
  hypothesis at L20: Refuted** (as a QK-subspace claim; G1 §5). Visibility to
  attention ≠ causation — the cleanest single-vector proof in the corpus.
- **(iii) Decision legibility** [STRUCTURAL]: where an injected direction is
  legible to the *decision function itself*. The decision is
  argmax(LN(h₂₃)·Eᵀ) — a linear readout over the final residual. Any direction
  with high cosine to an unembedding row is decision-legible *regardless of
  what it means*. This is structural, modulo the final LayerNorm's
  (monotone, direction-preserving-up-to-centering) rescale.

The program measured concept-geometry objects (cross-vocabulary relational
contrast directions — locus (i) objects) at layer 20 (a locus-(iii)-adjacent
layer) and injected them there expecting locus-(ii) causal participation.
[INFERENCE]/[INTERPRETATION]: the five flat static-geometry families
(EXP064/065/066/077/078) plus the output-side bridge rescues are the signature
of that conflation — geometry without causation at the wrong depth, plus a
readout cheat at the right depth for cheating.

### 1.2 Depth: L20 is three blocks from the readout

[STRUCTURAL]: an additive intervention δ at L20's residual stream reaches the
logits through the identity branches of exactly 3 blocks plus the final
LayerNorm. Two channels exist and only two:

- **(a) Bypass:** δ rides the residual stream to the readout, attenuated only
  by LayerNorm rescaling and perturbed by 3 blocks' additive outputs. If δ
  aligns with unembedding rows, it tilts logits directly. This channel is
  *architecturally guaranteed to be legible* — it is the residual stream doing
  what residual streams do.
- **(b) Routing:** δ is *read* by downstream attention (48 heads) or MLP
  gates and transformed into computation. G1 closed the QK version of this
  channel (ordering inverted; B_wrong dissociation); the MLP version was never
  open (full-rank up-projection filters nothing — a direction cannot be
  selectively admitted or rejected by the MLP, it passes through).

[INFERENCE]/[INTERPRETATION] ([ANALOGY] graded, structural core): with 3
downstream blocks there is almost no room for channel (b) to do work *even if
the direction were legible* — relational computation needs attention-mediated
information movement across positions, and a static additive vector at one
position is a rank-1 perturbation to that position's query; the softmax is
dominated by learned positional/semantic compatibilities and saturates. At
L10, by contrast, 14 downstream blocks (224 heads) stand between the
injection and the readout — room for processing, and room for the direction
to be *ignored by the readout* if it is not causally integrated (which is
 precisely the falsifier the program wants: a mid-layer injection that does
*not* ride the bypass is a cleaner causal test than any L20 injection).

The honest depth statement: **L20 maximizes decision-legibility and minimizes
processing room.** That is the right layer for a readout probe and the wrong
layer for a concept-causation probe. The program used it as both.

### 1.3 Attention heads vs MLPs at L20

[OBSERVATION] (G1): QK-subspace routing of the failed direction is Refuted;
OV corroborates (B_agg 0.407 vs bridge 0.353, same ordering); MLP exploratory
is a null by construction (full-rank up-projection).
[INFERENCE]/[INTERPRETATION]: at L20, **neither** sub-block offers a foreign
static direction a useful channel — heads are causally deaf to it (visible ≠
causal), MLPs are transparent to it. The only remaining channel is the
residual bypass (channel (a) above). [STRUCTURAL core, INFERENCE conclusion]:
*this is the architectural explanation of the entire L20 experimental record*
— five flat families (nothing routes) + bridge rescues (bypass works) + G1
kill (the routing story was backwards). It is overdetermined, not accidental.

Caveat graded honestly [ANALOGY]: "heads are causally deaf to static additive
directions" is supported at L20 by G1's measurements; generalizing it to all
layers/depths is analogy until the per-layer profile (§3.1) is measured.

### 1.4 Residual-stream geometry and anisotropy

[OBSERVATION] (G1 §4): `mu` (the centering offset) is the most QK-visible
(0.5110) and OV-visible (0.6829) direction measured — data-conditioned
directions ride the anisotropic manifold (F2 disclosure).
[INFERENCE] ([ANALOGY] graded): the raw cross-vocabulary cosine ≈ 0.7
(EXP065/066) is far above the 1/√d chance band (±0.061), so it is *real
shared geometry* — but shared geometry along the anisotropic mean direction
is not evidence of shared *causal* content. The audit's B3.7 $0 analysis
(raw vs corpus-centred cosines) is the adjudicator: if the 0.7 collapses
under centring, the boundary paper's positive half is restated as
anisotropic bias and the "concept geometry" the program chased at L20 was
partly a hygiene artifact. Either way, **late-layer residuals are the most
readout-aligned and the most anisotropy-loaded in the network** — the worst
place to mistake geometry for causation, and the program mistook it there
five times.

### 1.5 Readout proximity: why everything working ended up output-side

[STRUCTURAL]: the bridge b̂ = normalize(E[t_target] − E[t_foil]) is *already in
the decision's native coordinates* — it is a difference of unembedding rows.
Injected at L20, it traverses 3 blocks of mostly-identity residual path to a
linear readout. Its rescue (+10 to +23pp, always c=0) is therefore close to
architecturally *expected*, not surprising — which is exactly why K1 (the
readout-tilt falsification: cos(bridge, unembedding row) ≥ 0.9 bar) is the
binding first gate. [INFERENCE]: the program discovered, expensively, that
the only decision-legible intervention at L20 is a readout tilt. The depth
(§1.2) and head/MLP (§1.3) analyses say this was derivable from the
architecture before the first GPU minute: **at 3 blocks from a linear
readout, "output-side" and "works" nearly coincide by construction.**

### 1.6 Verdict: PARTIALLY PRINCIPLED (split by function)

| Principled — as a *measurement convention* | Convenience — as a *causal locus* |
|---|---|
| Fixed layer ⇒ 5 experiments mutually comparable (real scientific value; the flat pattern is legible *because* the layer was held constant) | Inherited without any localization study — no depth sweep, no causal screen ever asked "where does the relational computation live?" before committing the program to L20 |
| Late-layer injection maximizes downstream *routing opportunity* in the head-count sense — G1's original motivation was principled, even though G1 refuted the QK version | L20 is 3 blocks from the readout: minimal processing room for a *concept* intervention, maximal bypass — the layer is structurally biased toward readout cheats and against concept causation |
| Logit-lens readability intuition (late residuals are interpretable) is legitimate for *measurement* | The steered object (relational contrast geometry) is a mid-network object by every mechanistic account; injecting it at 83% depth assumes what needed proving |
| Pythia-410m chosen for throughput (22 fwd/s, fits 2×T4 comfortably) — honest, stated compute discipline | 410m chosen for throughput, never for architectural suitability to the steering question; no suitability argument was ever made |

**Verdict: partially principled — weighted toward convenience.**
[INFERENCE]/[INTERPRETATION]: L20 was a principled choice of *where to look*
(readout-legible, comparable across experiments) and an unprincipled choice
of *where to intervene for concept causation* (no localization evidence; the
retrospective record — five flat families + G1 inversion — now argues the
causal locus is elsewhere or absent). The program's standing question "is the
substrate exhausted?" cannot be answered until the depth confound is removed:
the nulls may be *layer* nulls, not *substrate* nulls. No verdict above is a
[THEOREM]; the structural claims are marked [STRUCTURAL], the depth-profile
claims [ANALOGY], the measurements [OBSERVATION].

---

## 2. Alternative hunting grounds (ranked)

Each ground: architectural rationale (graded), cheapest probe with pass
counts, Law #15 Q3 honest cost assessment, and its trigger. **No ground is
pursued before its trigger fires** (§3).

### Ground 1 — Depth axis: early/mid-layer injection in Pythia-410m (FIRST)

**Architectural rationale.** [STRUCTURAL]: injection at L8/L12/L16 leaves
16/12/8 downstream blocks (256/192/128 reader heads) — room for channel (b)
routing to actually operate, and crucially, *distance from the linear
readout*: a mid-layer injection that rescues cannot be a pure bypass cheat,
because the direction must survive 8–16 blocks of attention/MLP processing
to reach the logits. A mid-layer rescue is therefore *harder to explain away*
than any L20 rescue — the depth axis is a cheat-resistant hunting ground by
construction. [ANALOGY]: relational concept formation is a mid-network object;
if the concept direction is causally real anywhere, it is addressable where
it is formed, not 3 blocks from the output. **This ground directly tests the
§1.6 verdict**: if static geometry rescues mid-network, L20 was the wrong
room; if it is flat at every depth, the null is substrate-deep and the
program may stop blaming the layer.

**Cheapest probe (two stages, $0 first).**
- Stage 0 ($0, CPU, no forward passes): extend G1's weight-only method to a
  **per-layer QK/OV projection-energy profile** — Ē_QK/Ē_OV of B_agg, b_mean,
  B_wrong at every injection layer 0–23 (384 heads total; G1 did 48 heads in
  41 s CPU — full profile is minutes). Discriminating question: does B_agg's
  addressability peak mid-network while the bridge's peaks late? A crossed
  profile is weight-only evidence for the wrong-room hypothesis before any
  GPU. (Feasibility: G1's executor already implements the per-head layout;
  the extension is mechanical — stated as a plan, not a result.)
- Stage 1 (GPU, only if Stage 0 is suggestive OR K1 confirms tilt): static
  B_agg injection at L8/L12/L16, α ∈ {0.5, 1.0}, N=60 headroom items,
  final-token position (matches the dead rooms' protocol, so a rescue is
  unambiguous news): 3 depths × 2 α × 60 = **360 passes ≈ 16 s ≈ 0.008 T4-h**
  at 22 fwd/s. L20/α-grid arms already archived (EXP077) — no re-runs.
  The *gated* (premise-position) variant survives EXP077's kill license and
  is the pre-registered follow-up, not the probe — the probe stays minimal.

**Law #15 Q3 (honest cost).** The $0 Stage 0 buys the localization hypothesis
for nothing and is the single cheapest discriminating analysis in this
document. Stage 1 costs 16 seconds of GPU. *Honest caveat*: Stage 1 repeats
the shelved operator family (unconditional static injection) — it is licensed
only as a *localization diagnostic*, never as a new discovery bid; a flat
Stage 1 closes the depth axis for the static family permanently (Law #8).

**Trigger.** **K1 confirms readout tilt** (primary): the output room is then
a confirmed cheat (P1 fires), the program has no positive evidence anywhere,
and "was it the layer?" is the cheapest remaining substrate question.
(Secondary, weaker: K1 survives but K2 shows bypass — the bridge is logit
steering, so the hunt for a *routing* mechanism moves upstream. If K1
survives AND K2 shows routing, the KEEP chain holds and this ground stands
down — the output room is then legitimately occupied.)

### Ground 2 — Family axis: a Qwen/Llama-class open-weight frozen model (SECOND)

**Architectural rationale.** [STRUCTURAL — the load-bearing contrast]:
Pythia is GPT-NeoX with **parallel** attention+MLP blocks; Llama/Qwen-class
models use **sequential** blocks (attention → residual → MLP → residual).
Consequences: (i) in a sequential block, an injected direction is re-processed
by the MLP *after* attention every block — the intervention cannot take the
pure-bypass path that NeoX's parallel layout leaves wide open, so a rescue in
a sequential model is stronger evidence of routing; (ii) SwiGLU MLPs are
*explicitly gated* — the gate is a multiplicative knob that can amplify or
suppress a direction conditionally, a routing mechanism NeoX's dense MLP lacks
(G1's "MLP filters nothing" was measured on NeoX's full-rank up-projection —
[ANALOGY] graded: whether SwiGLU's gate is effectively rank-deficient in
practice is unmeasured); (iii) full-dimension rotary (vs Pythia's 25%) changes
which subspaces carry position — relevant to whether a *global* static
direction can address position-specific computation. [INFERENCE]: the L20
null may be a **NeoX artifact** — parallel blocks + dense MLP + partial
rotary = an architecture where foreign static directions have exactly one
channel (bypass). The family axis tests that hypothesis, and it is the only
ground that changes the *block structure*, which is where G1's two findings
(full-rank MLP, QK inversion) both live.

**Cheapest probe ($0 first).** Port G1's weight-only QK/OV audit to the new
family's weights (downloaded free; CPU): the discriminating question is
whether *any* family shows the **predicted** ordering (bridge QK-visible ≫
failed direction) that NeoX inverted. A family passing that screen is where
the QK mechanism might actually live — decided for $0. (Load-bearing
family specs — exact RoPE coverage, gate behavior — verified from the
weights/configs at port time, not asserted here; current specifics tagged
UNVERIFIED.)
GPU probe only after the trigger: rebuild per-vocabulary contrast directions
under the new tokenizer + run the EXP065/066 static null-test with the bridge
positive control at matched relative depth (~83%): ≈ **240 passes (minutes)**.
*Honest caveat*: pass counts are cheap; **setup dominates** — new tokenizer,
new contrast-pair construction, new benchmark harness, new activation
archives. This is the highest-setup-cost ground.

**Law #15 Q3 (honest cost).** The $0 G1-port is the cheapest *family-level*
falsifier available: if every tested family inverts the QK ordering, the
QK-subspace program is dead across families, not just in NeoX. The GPU probe
is minutes; the engineering is days. Do not confuse the two costs.

**Trigger (conjunction — deliberately strict).** **K1 confirms tilt AND the
Ground-1 probe is flat at all depths** (Stage 0 profile shows no mid-network
addressability peak AND/OR Stage 1 sweep ΔM=0 everywhere): the null is then
substrate-deep in NeoX (output room = cheat, concept room = dead at every
depth), and only then is the family axis's setup cost justified. K2 showing
bypass corroborates (NeoX attention will not route static directions). $0
reconnaissance (weight download, config inspection, G1-port *code* prep) may
proceed anytime as CPU work, but its *interpretation as a hunting-ground
decision* waits on the trigger.

### Ground 3 — Scale axis: larger Pythia variants, 1B/2.8B (THIRD)

**Architectural rationale.** [ANALOGY] (superposition hypothesis — graded
honestly as analogy, not theorem): larger width (d=2048/2560 [UNVERIFIED —
not fetched in-program; the load-bearing claim is "wider than 1024"])
predicts less superposition interference ⇒ relational directions more
linearly separable ⇒ more likely causally addressable. Same family, same
tokenizer lineage, same training data (Pile) — the scale axis is the
*cleanest-controlled* axis: it varies capacity while holding block
structure, data, and tokenizer fixed. Note the interaction: Pythia-1B has
*16* layers [UNVERIFIED], so depth and scale interact — injection must be
matched at **fractional** depth (≈83%: L20/24), not absolute layer index.

**Cheapest probe ($0 first).** Verify tokenizer/vocab compatibility from
configs (CPU), download weights (free), run the G1 weight-only audit at
matched fractional depth (CPU). Discriminating $0 question: does the
QK-ordering inversion *persist* at larger width? If the inversion persists,
scale does not fix the mechanism story — decided for $0.
GPU probe only after the trigger: the matched static null-test + bridge
control, 60 items × 3 conditions = **180 passes** [ESTIMATE: throughput on
2×T4 unmeasured for 2.8B; fp16 ≈ 5.6 GB fits comfortably — budget "minutes,"
stated as unmeasured, not as 22 fwd/s].

**Law #15 Q3 (honest cost).** This axis tests the *weakest* hypothesis
(the null is capacity, not mechanism) at the *highest* GPU cost per pass.
The audit already shelved 7B+ scaling ("revisit only with a mechanism that
survives K1–K3 at 410m") — this analysis concurs and sharpens it: **scaling
a confirmed tilt buys nothing**; scaling is only informative when there is a
real mechanism to scale.

**Trigger (lives on the KEEP branch).** **K1–K3 all survive at 410m** (the
bridge is a real, routing, Law-#7-compliant mechanism) **AND** the audit's
§I condition 1 (forced-bigger-model baseline already run). EXP080 bin (ii) >
0 strengthens the case (a selection prize exists — test whether scale
enlarges it) but is not required. If K1 confirms tilt, this ground's trigger
* cannot fire* — it stands down permanently for the static family.

### Ground 4 — Feature/SAE-based substrates (LAST, conditional)

**Architectural rationale — and why it ranks last.** [ANALOGY]: SAEs
decompose superposition into putatively monosemantic features; the program's
core failure is *raw directions* that are geometrically similar but causally
inert — superposition interference is a candidate cause, and a feature basis
would be the causally right *unit* of intervention. **Honest counter**
[INFERENCE]: the program's null is *causal transfer*, not measurement noise —
cleaner features do not create transfer; nothing in the record suggests the
failure is "we measured the wrong direction" rather than "static injection
does not route." SAEs also add a trained component (Law #6 boundary) and
require a trained SAE for the exact checkpoint (availability UNVERIFIED).
The audit already owns this pivot (Gemma 3 + Gemma Scope 2, pivot (a), with
the invalid-run branch pre-registered) — this track defers to it rather than
duplicating it.

**Cheapest probe.** $0: this section's argument. There is no cheaper probe —
any empirical probe needs the SAE artifact itself.

**Law #15 Q3 (honest cost).** Highest cost, weakest architectural necessity.
Not recommended now.

**Trigger (the only signature that would justify it).** The Ground-1 probe
**finds a causally-effective locus** (some mid-layer rescues under gated
injection) **but raw-direction addressing fails there** (direction variants
flat at that locus) — the localization/addressing dissociation. That is the
signature that says "the *unit* of intervention is wrong, not the room."
Absent that signature, SAE cost is never justified.

---

## 3. Ranked recommendation and triggers (decision tree)

**Ranked order:** Ground 1 (depth) > Ground 2 (family) > Ground 3 (scale) >
Ground 4 (SAE). The ranking is cost-effectiveness × trigger-reachability, and
it induces a decision tree over the program's pending observations:

```
K1 ($0, runs first — DIRECTION_DECISION §1)
│
├─ K1 CONFIRMS TILT (P1 fires; output room = cheat)
│   ├─ EXP080 bin (ii) = 0 → output room fully closed as mechanism science
│   │   └─► GROUND 1 fires: $0 per-layer profile → 360-pass depth sweep
│   │       ├─ sweep rescues mid-layer → re-localize; DPRS/CLLC re-pointed
│   │       │   at the rescuing locus; Ground 4 trigger check
│   │       │   (locus found + addressing fails → SAE licensed)
│   │       └─ sweep flat at all depths → NeoX substrate-deep null
│   │           └─► GROUND 2 fires: $0 G1-port → family GPU probe
│   ├─ EXP080 bin (ii) > 0 → selection prize exists beyond the bridge
│       └─► DPRS re-pointed at output room (audit §B4(i)); Ground 1 as
│           diagnostic only (is the prize depth-specific?)
│
├─ K1 SURVIVES (tilt Not supported) → KEEP chain: K2 → K3 → EXP080 → EXP081
│   ├─ K2 shows BYPASS → bridge is logit steering; mechanism hunt moves up
│   │   └─► GROUND 1 fires (diagnostic): where is routing legible?
│   ├─ K2 shows ROUTING + K3 compliant bridge rescues
│   │   └─► STAY at 410m/L20-output-room; Ground 1 stands down
│   │       └─► GROUND 3 trigger armed: K1–K3 survive ⇒ scale axis licensed
│   │           (with forced-bigger-model baseline, audit §I cond. 1)
│   └─ K1 INCONCLUSIVE → battery holds; Ground 1's $0 Stage 0 may run
│       (pure CPU reconnaissance; interpretation marked [OPEN])
│
└─ Ground 4 (SAE) fires ONLY on the localization/addressing dissociation
  (Ground-1 sweep finds a locus + direction variants flat there).
```

**What must arrive before each move (the binding triggers):**

| Ground | Trigger (all must be observed, not assumed) |
|---|---|
| 1 — Depth | K1 confirms tilt (primary). Secondary: K1 survives + K2 bypass. Stage 0 ($0 profile) needs no trigger beyond K1's verdict existing; Stage 1 (360 passes) needs the tilt/bypass verdict. |
| 2 — Family | K1 confirms tilt **AND** Ground-1 probe flat at all depths. Conjunction — the setup cost is only justified on a substrate-deep NeoX null. |
| 3 — Scale | K1–K3 survive at 410m **AND** forced-bigger-model baseline run (audit §I-1). Cannot fire if K1 confirms tilt. |
| 4 — SAE | Ground-1 sweep finds a rescuing locus **AND** raw-direction variants are flat at that locus. |

---

## 4. Law #15's four answers (explicit)

- **Q1 — verdict + ranked hunting grounds:** §1.6 verdict (**partially
  principled, weighted toward convenience** — principled as measurement
  convention, convenience as causal locus) and §2–§3 ranking
  (depth > family > scale > SAE) with per-ground rationale, cheapest probes,
  and triggers. Above.
- **Q2 — PIVOT/CONTINUE: which decision this changes.** This analysis changes
  the **post-K1 (P1) pivot target**. The audit/decision named the P1 pivot as
  *mechanism-family → closed-loop control (CLLC pilot)*. This track refines
  it: the P1 pivot's **substrate half** is now ordered — Ground 1 (depth)
  fires first as the re-localization question, because the §1 analysis shows
  the nulls may be *layer* nulls, not substrate nulls, and the localization
  probe costs 16 seconds of GPU. CLLC (mechanism-family pivot) is unaffected
  and may parallelize — it is a different axis (mechanism, not substrate).
  On the KEEP branch, this analysis changes the **DPRS re-pointing decision**:
  if K1 survives, Ground 1's $0 profile becomes the diagnostic that tells
  DPRS *which readout-space region* to search. Net: PIVOT → depth-first
  re-localization before family/scale moves; CONTINUE → depth diagnostic
  informs the re-pointed loop.
- **Q3 — CPU/$0, cheapest possible.** The literature-and-architecture argument
  *is* this document ($0). Per ground, the cheapest discriminating next step:
  Ground 1 — the $0 per-layer QK/OV weight-energy profile (minutes of CPU,
  G1's method extended to 24 layers), then a 360-pass / ~16 s depth sweep;
  Ground 2 — the $0 G1-port weight audit on the new family's weights (the
  ordering-inversion test), GPU probe only post-trigger (~240 passes,
  setup-dominated); Ground 3 — $0 tokenizer/weight verification + G1 audit at
  matched fractional depth, 180-pass probe post-trigger (throughput
  unmeasured, bounded as "minutes"); Ground 4 — no probe cheaper than the
  argument exists; not recommended. Total $0-first sequence across grounds:
  two weight-only profiles and one port — all CPU, all pre-trigger-safe as
  reconnaissance, interpretation gated on triggers per §3.
- **Q4 — architectural argument, analogy vs theorem graded.** The argument is
  built in §1.1–§1.5 and §2 from transformer structure
  (depth/head-count/MLP-rank/readout-linearity), with every step graded
  [STRUCTURAL] / [ANALOGY] / [THEOREM]-none. Structural core: 24-layer
  GPT-NeoX with parallel blocks ⇒ L20 injection has exactly two channels
  (3-block residual bypass to a linear readout; 48-head routing), G1 closed
  the routing channel and measured the MLP channel as transparent by
  construction, leaving bypass as the only legible channel — which is why
  every working intervention ended up output-side. Analogy-graded: the
  mid-network concept-formation depth profile, the superposition/width
  argument for scale, the SwiGLU-gate routing story for the family axis.
  **No theorem is claimed**; the honest headline is that the L20 record was
  *derivable from the architecture* before the GPU was spent.

---

## 5. Open questions (what this analysis does not close)

1. [OPEN] Whether mid-layer static injection rescues — untested; Ground-1
   Stage 1 is the falsifier. The $0 Stage-0 profile sharpens but does not
   replace it.
2. [OPEN] Whether the 0.7 cross-vocabulary cosine survives corpus-centring
   (audit B3.7) — if it collapses, §1.4's "concept geometry" was partly
   anisotropic bias and the depth question gets *easier* (less worth chasing).
3. [OPEN] The exact load-bearing specs of candidate family checkpoints
   (RoPE coverage, gate rank-behavior) — UNVERIFIED; the $0 G1-port measures
   the behavior that matters (QK/OV ordering) without needing the specs.
4. [OPEN] SAE availability for the exact 410m checkpoint — UNVERIFIED;
   irrelevant until Ground 4's trigger fires.
5. [OPEN] Whether "heads are causally deaf to static directions" generalizes
   beyond L20 — the per-layer profile (§3.1/Stage 0) is the test; until then
   it is analogy with one measured point.

*End of LOG-201 deliverable. No GPU used. No code written. No weights touched.
No signed protocol, primary artifact, or LOG-197 chain material modified.
No citations fabricated; UNVERIFIED tags where the program has not verified.
Δθ=0 throughout.*
