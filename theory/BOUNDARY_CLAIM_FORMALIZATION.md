# Formalization of the Corrected Representational–Causal Boundary Claim

**Author role:** Theory Agent
**Date:** 2026-09-23
**Status:** Working formalization; precedes any manuscript use
**Governing docs:** `theory/README_DEFINITIONS.md` (source of truth for symbols), `AGENTS.md` §5 (labels),
`reports/adversarial_audit_exp065_exp066.md` (evidence base)

**Notation context:** All SCBI symbols ($\theta, x, y, h, z, B, \Delta M$) follow
`theory/README_DEFINITIONS.md` §86. Experiment-specific quantities are defined in §4 below.

---

## 1. The retracted claim (for the record)

**[INTERPRETATION — RETRACTED 2026-09-23]:** *"Internal relational contrast directions across disjoint
entity vocabularies exhibit robust geometric alignment under closed-form Procrustes rotation
($\Delta\cos \approx +0.13$ to $+0.79$), yet this aligned basis yields zero causal transfer —
hence representational alignment is not sufficient for causal interchangeability."*

**[FACT]:** This claim contradicts the primary artifacts. Recomputed Stage A values
(`exp065_results.json`, `exp066_replication_results.json`, both run logs):
EXP065 raw $+0.7186 \to$ aligned $+0.0032$ ($\Delta\cos = -0.7154$);
EXP066 raw $+0.6852 \to$ aligned $-0.0118$ ($\Delta\cos = -0.6971$).
The rotation destroyed similarity; the $+0.1290$ figure is unsourced. The claim is withdrawn
and replaced by §3 below. (Corrections applied to summary docs; see `reports/research_log.md` 2026-09-23.)

---

## 2. What the experiments actually measured

For each support vocabulary $V_k$ ($k=1..5$; Anglo, Biblical, Greek, Roman, Modern), a per-vocabulary
contrast direction was constructed at target layer $l^*$ ($l^*=10$ for pythia-160m, $l^*=20$ for pythia-410m):

$$\hat{v}_k = \operatorname{normalize}\!\left(\frac{1}{30}\sum_{i=1}^{30}
\frac{\Delta h_i^{(k)}}{\|\Delta h_i^{(k)}\|}\right),
\qquad \Delta h_i^{(k)} = h_{l^*}(x_i^{\mathrm{rel}}) - h_{l^*}(x_i^{\mathrm{neu}})$$

where $h_{l^*}(\cdot)$ is the residual-stream hidden state at layer $l^*$ (last token position).
The aggregated basis is $B_{\mathrm{agg}} = \operatorname{normalize}(\sum_k \hat{v}_k)$.
Intervention: $h \leftarrow h + \alpha \, u$ with $u$ the condition direction, $\alpha = 0.50$,
via forward hook at layer $l^*$; $\theta$ frozen ($\Delta\theta \equiv 0$, SHA-256 verified pre/post).

Benchmark: $N=60$ novel-entity 2-hop/3-hop relational items (Planetary + Elemental domains),
disjoint from support vocabularies. Primary endpoint: $\Delta M = M_{\mathrm{mod}} - M_{\mathrm{base}}$
(accuracy, percentage points) with paired decisions; McNemar exact test on discordant counts $(b, c)$
= (rescues, corruptions).

---

## 3. The corrected claim, decomposed

### 3.1 Observations

**[OBSERVATION] O1 — Raw cross-vocabulary geometric similarity is high without any alignment.**
Mean pairwise cosine $\cos(\hat{v}_1, \hat{v}_k)$ over $k=2..5$: $+0.7186$ (EXP065, pythia-160m, $d=768$),
$+0.6852$ (EXP066, pythia-410m, $d=1024$). Sources: `stage_A_alignment_discovery` /
`stage_A_alignment` in the result JSONs; corroborated by run logs.
[NOTE — B-1] O1 must not be lifted out of context as "shared relational geometry": Ethayarajh (2019)
establishes strong anisotropy in contextualized representations (high raw cosine is expected), and
SCBI's vectors received no Jorgensen-style (2023) mean-centring — the global-offset control the
literature requires was omitted. See Q2.

**[OBSERVATION] O2 — The Procrustes rotation step destroyed this similarity.**
Post-rotation mean cosine: $+0.0032$ (EXP065), $-0.0118$ (EXP066); $\Delta\cos = -0.7154$ / $-0.6971$.
The operator is characterized in `theory/proofs/procrustes_failure_analysis.md` (rank-2 fit,
cross-space application); the near-zero outcome is the mathematically expected output of the
operator as implemented, not a scale effect.

**[OBSERVATION] O3 — Static injection of the geometrically similar basis yields zero causal transfer.**
Condition "Static $B_{\mathrm{agg}}$": $\Delta M = 0.0$ pp, $b=0$, $c=0$, McNemar $p=1.0000$,
on benchmarks with verified headroom (EXP065: baseline $68.33\%$, 19 rescuable errors;
EXP066: baseline $56.67\%$, 26 rescuable errors; both inside the pre-registered 40–70% window).

**[OBSERVATION] O4 — Output-space intervention at the same layer does steer behavior.**
"Same-Layer Output Bridge" ($u \propto W_U[t_{\mathrm{target}}] - W_U[t_{\mathrm{foil}}]$, unembedding-space
direction): EXP065 $\Delta M = +16.67$ pp ($p=0.0020$, 10/19 rescues); EXP066 $\Delta M = +13.33$ pp
($p=0.0078$, 8/26 rescues); $c=0$ in both. KL divergence confirms only this condition meaningfully
moves the output distribution (0.028 vs $\approx$ 0.0002).

**[OBSERVATION] O5 — Margin-shift significance is not a causal endpoint.**
Wilcoxon tests on per-instance logit-margin shifts yield $p = 1.6\times10^{-11}$ for the rotated-basis
condition and $p = 1.2\times10^{-8}$ for the wrong-task negative control $B_{\mathrm{wrong}}$, all with
$b=c=0$. The control invalidates margin-shift significance as evidence of task-relevant effect.

### 3.2 Interpretations (separated from observations per Law #11)

**[INTERPRETATION] I1 — The defensible boundary.**
Raw geometric similarity of relational contrast directions across disjoint vocabularies
($\approx 0.7$ cosine, no rotation) coexists with strictly zero causal transfer under static
residual-stream injection at full headroom, while output-space directions at the same layer
rescue a substantial fraction of errors. *Geometric similarity of internal contrast directions
does not imply causal interchangeability under static injection.* This is the corrected central claim.

**[INTERPRETATION] I2 — The rotated-basis null is uninterpretable as an alignment test.**
Because O2 shows the "aligned" basis was in fact scrambled ($\cos \approx 0$), Condition 2
("Aligned Dynamic Basis", $\Delta M = 0$) tests scrambled-basis injection, not aligned-basis
injection. It contributes no evidence for or against the boundary; it is a methods failure,
not a scientific result about alignment.

**[INTERPRETATION] I3 — Scope limits.**
I1 is established for: Pythia 160M/410M, layers at 83% depth, the N=60 Planetary/Elemental
benchmark family, $\alpha = 0.50$ single-vector additive injection. Generalization beyond these
conditions is **[OPEN]**, not implied.

### 3.3 Hypothesis for the next experiment

**[HYPOTHESIS] H1:** A Procrustes alignment operator that is (a) fit in the *same* space as the
intervention (per-head attention OV output subspaces, not unembedding$\to$residual) and
(b) full-rank-constrained (rank $\geq$ subspace dimension, explicit identity on the orthogonal
complement) will produce $\Delta M > 0$ with McNemar $p < 0.05$ on the same N=60
headroom-calibrated benchmark.

**Canonical falsification criterion (single source of truth; full decision tree in EXP067 §7,
quoted verbatim there):**
$$\boxed{\textbf{If C3 yields } \Delta M = 0 \textbf{ (McNemar } p \ge 0.05,\ b = 0\textbf{)}
\textbf{ while C4 yields } \Delta M > 0 \textbf{ (}p < 0.05\textbf{, } \ge 5 \textbf{ rescues),}
\textbf{ then H1 is FALSIFIED.}}$$
[INTERPRETATION] of that outcome: the dissociation is structural, not operator-quality; the
research program pivots to locating the break (QK vs OV vs MLP) rather than improving alignment.
(Test: EXP067, `experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md` §7 — the
pre-registered decision tree there elaborates this criterion for halt, invalid-run, and
mixed-outcome branches. Two sources of truth for one criterion would be a future inconsistency
bug; the EXP067 protocol's §7.0 restates this box verbatim.)

### 3.4 Open questions

**[OPEN] Q1:** Does a sound alignment operator (H1) change the Stage B verdict?
**[OPEN] Q2:** What explains the high *raw* similarity O1 ($\approx 0.7$)? Candidate explanations
include shared relational geometry across lexicons vs. residual prompt-template/positional artifacts
not removed by the $\Delta h$ contrast. Requires dedicated controls (template ablations).
**[OPEN] Q3:** At which downstream stage does the causal chain break — attention routing (QK),
value transport (OV), or MLP readout? EXP067 targets QK/OV; MLP remains open.

### 3.5 Explicit non-claims

- I1 is **not** a claim that frozen models cannot be steered (O4 shows they can, via output space).
- I1 is **not** a claim about SCBI's full mechanism (candidate generation/evaluation/selection were
  not exercised; only static injection was tested).
- I1 is **not** a novelty claim (prior-art audit complete 2026-09-23; verdict N1 — Known Combination, tested mechanism N0; cf. `reports/novelty_report.md`).
- No statement above asserts anything about "superhuman" capabilities.

---

## 4. Symbol–artifact map

| Symbol | Meaning | Primary artifact |
|---|---|---|
| $\hat{v}_k$ | per-vocab normalized contrast direction | `delta_h_by_vocab` → `v_hat_by_vocab` (scripts) |
| $B_{\mathrm{agg}}$ | normalized sum of $\hat{v}_k$ | run logs ("B_agg constructed") |
| $S_{\mathrm{raw}}$, $S_{\mathrm{aligned}}$ | mean $\cos(\hat{v}_1,\hat{v}_k)$, pre/post rotation | `stage_A_*` JSON fields, run logs |
| $\Delta M$, $(b,c)$, $p$ | accuracy delta (pp), rescues, corruptions, McNemar exact $p$ | `stage_B_conditions` JSON fields |
| $u_{\mathrm{bridge}}$ | $W_U[t]-W_U[f]$ normalized | `make_bridge_vec` (scripts) |

All labels in this document follow `AGENTS.md` §5 / `theory/README_DEFINITIONS.md` §96.
