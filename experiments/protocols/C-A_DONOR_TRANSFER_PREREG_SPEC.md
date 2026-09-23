# C-A — Cross-Item Donor-Bridge Transfer: Pre-Registration Spec

**Status: DRAFT — NOT signed, NOT pre-registered. Law #14 adversarial review
(same reviewer, under LOG-144 authority) required before PRE-REGISTERED.**
No experiment number minted (assigned at signing per LOG-149/150).
No GPU executed; no primary artifacts touched; no signed protocols modified.

**Date:** 2026-09-23 · **Dispatch:** LOG-150 · **Author role:** Pre-registration drafter
**Source idea:** `research/innovation/SPRINT2_2026-09-23.md` §C-A (verbatim sketch verified
by LOG-144 reviewer); **binding constraints:** `reports/adversarial_review_c-a_confound_2026-09-23.md`
(LOG-144 verdict: REVISE — the draft is signed only if all nine (c) items are present and pinned).
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `research/TEAM_KNOWLEDGE_PROTOCOL.md`,
`research/MATH_STANDARDS_CHARTER.md` (binding M1–M8), `experiments/protocols/STATISTICAL_PROTOCOL_V02.md`,
`theory/BOUNDARY_CLAIM_FORMALIZATION.md` (boundary null I1), `research/README_LITERATURE.md` (novelty),
`research/CHATGPT_MENTORSHIP_DIRECTIVE.md` (P1–P4, three evidentiary levels, FACT/INFERENCE/HYPOTHESIS/SPECULATION
reporting layer atop the repo 10-label standard), LOG-148 verdict standard.
**Roadmap phase:** Phase 4 (transferable intervention = autonomous-capability primitive; sprint §C-A).
**Execution rule:** Strictly confirmatory. Changed design = the next free number at
pre-registration time (Law #4). No margins/Wilcoxon/KL as decision endpoints (Law #9).

**Corpus read (TEAM_KNOWLEDGE_PROTOCOL §1):** `research/TEAM_KNOWLEDGE_PROTOCOL.md`;
`reports/adversarial_review_c-a_confound_2026-09-23.md` (LOG-144, binding); `SCBI/AGENTS.md` (14 laws);
`research/innovation/SPRINT2_2026-09-23.md` §C-A (sketch, verified); `experiments/runs/exp077/run_exp077.py`
(benchmark construction, `make_bridge_vec`, McNemar harness, `get_hash`, F1/F2 guards);
`experiments/runs/exp078/run_exp078.py` (support vocabularies, "is next to" neutral template,
EXP078 branch-(a) provenance); `experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md` (format precedent);
`research/MATH_STANDARDS_CHARTER.md` (M1–M8); `theory/BOUNDARY_CLAIM_FORMALIZATION.md` (I1);
`reports/research_log.md` LOG-066 (EXP058), EXP078(a) ruling (LOG-116/120 entries), LOG-149/150 dispatch.

## 0. Notation context (M1.1 — scope: this document only)

In *this* document: $W_U \in \mathbb{R}^{V \times d}$ is the unembedding matrix
(`model.get_output_embeddings().weight`, $d=1024$, pythia-410m). $D$ is a donor bank;
$t_d, f_d$ are donor $d$'s target/foil tokens (correct answer $=$ target, $=$ item field `A`).
$\hat{b}_D$ is a donor-bank centroid (pinned §4). $s_t^{(a)}(j)=\cos(\hat{b}_a, W_U[t_j])$,
$s_f^{(a)}(j)=\cos(\hat{b}_a, W_U[f_j])$ are weight-only similarity features of arm $a$'s
intervention on test item $j$ (target $t_j$, foil $f_j$). $l^*=20$ is the injection layer.
$M$ = decision accuracy over the 60 test items; $\Delta M$ = arm minus C1 (fraction, ×100 for pp).
"Rescue" = an item C1 gets wrong and the arm gets right. Verdicts are only from the permitted set
(LOG-148): **Supported / Not supported / Inconclusive / Underdetermined / Refuted**.

## 1. Research question and hypotheses

**Question.** Is the output bridge's rescue relation-general or item-specific? Apply a bridge
direction built from *labeled donor items* (entity-disjoint, same relation template) to unlabeled
test items — the first test of whether the program's one working intervention family has
transferable structure, and the path to label-free-at-test-time gains (donor bank from labeled
support). [CONJECTURE] / SPECULATION (the capability bet).

**[HYPOTHESIS] H_transfer:** the same-relation donor-centroid bridge C3 rescues test items
*via relation-mediated structure* — i.e., its causal power survives controls that preserve
token-similarity/prior channels while destroying relational content (T1–T6 conjunctive, §8).

**[HYPOTHESIS] H_leak (the null for any C3 win):** the donor bridge rescues *via similarity/prior
steering* — near-direct answer-logit steering (audit Finding 4 [INTERPRETATION], G1 corroboration
[OBSERVATION]: bridge $\bar{E}_{QK}=0.356$, mid-null, QK-unremarkable), adding logit mass to
answers in proportion to unembedding similarity to the donor bank's target-minus-foil direction,
with no relational computation required.

**[FACT] — the structural 10-token answer-pool overlap (load-bearing).** The 60 test items draw
answers from a **10-token pool** {Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver,
Bronze, Steel} (`run_exp077.py:149-150`; per item, `A`=target, `C`=foil). Any donor bank drawn
from the same item distribution **necessarily shares answer tokens with test items**. With the
entity-disjoint name-entity donors used here (§3), literal token-identity overlap is zero *by
construction*, but unembedding-similarity channels (L2/L3) and bank-prior channels (L4) remain —
measured weight-only by $s_t, s_f$ (§4). **Leakage is therefore the null hypothesis for any C3
win, not a corner case.** A C3 win that fails any of T3–T6 is similarity/prior steering, not
transfer (§8, LICENSES).

**Evidentiary level (mentorship directive, standing law):** even a clean transfer license reaches
at most **Level 1** ("can improve inference" via an intervention at the tested configuration).
It cannot reach Level 2 ("changes computational strategy") or Level 3 ("creates qualitatively
new capability"), because under *both* H_transfer and H_leak the mechanism is readout steering
(P1: the canonical question stays mechanism-level). No Level 2/3 language appears anywhere in
this spec.

## 2. Benchmark and model configuration (frozen)

**[FACT]** The N=60 benchmark is the EXP065/066/077/078-identical Planetary/Elemental 2-hop/3-hop
suite (same items, same premise permutations; Law #9: no new benchmark construction).
Item ids: `exp077_planet_2hop_0..14`, `exp077_planet_3hop_0..14`,
`exp077_element_2hop_0..14`, `exp077_element_3hop_0..14`. Per item: `prompt`, `A` (target),
`C` (foil). Correct answer = `A`. Decision rule (pinned): argmax over the single-token
encodings `" A"` vs `" C"` at the final position; correct iff chosen == `A`.
([FACT] — construction in `run_exp077.py:588-638`; [DEFINITION] — anchored to the same schema.)

**[FACT]** Model: frozen pythia-410m ($\Delta\theta=0$; SHA-256 pre/post guard via the `get_hash`
harness verbatim from EXP077, §10). Tokenizer: pythia-410m. F2 guard (verbatim from EXP078):
all donor and test entities verified single-token as the exact encoded strings `" "+e` before
any forward pass; any multi-token entity → FATAL abort naming the entity.

**Pinned intervention site:** injection $h \leftarrow h + \alpha\hat{b}$ at the last-token residual
stream at the output of transformer layer $l^*=20$ (the same hook site as EXP066/EXP077/EXP078
`TARGET_LAYER=20`). **Pinned:** $\alpha=0.50$ (`ALPHA_BRIDGE`, EXP066's configuration:
$\alpha=0.5$, +13.33pp, $p=0.0078$; EXP077 C8 positive control rescued +10pp, 56.67%→66.67%,
$p=0.03125$ [OBSERVATION]). No $\alpha$ grid, no layer sweep in this design (Law #4: scope is
frozen; companion sweeps are separate pre-registrations).

## 3. Donor banks — (c).1 [DONORS]

### 3.1 C3 donor bank: same-relation, entity-disjoint (primary arm)

**[DEFINITION]** A *donor item* is a labeled support item (premise triple, relation template,
target $t_d$, foil $f_d$) used *only* to construct an intervention vector. Donor labels are
support-side construction material; they never enter the evaluation objective.

**Exact donor list (20 donors, pinned).** For each support vocabulary $vk \in$
{V1_Anglo, V2_Biblical, V3_Greek, V4_Roman, V5_Modern} (the F2-verified EXP078 set) and each
triple index $i \in \{0,1,2,3\}$ of `TRIPLES_INDICES`, with $(iA,iB,iC)=$ the $i$-th triple,
$A=ents[iA]$, $B=ents[iB]$, $C=ents[iC]$, `target_first=(i%2==1)`, `q_opts=f"{A} or {C}"` if
target_first else `f"{C} or {A}"`:

- id: `ca_C3_donor_{vk}_triple_{i}`
- prompt: `Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:`
- $t_d = A$ (correct answer), $f_d = C$.

The 20 $(t_d, f_d)$ pairs, verbatim:

| id suffix | $t_d$ | $f_d$ |
|---|---|---|
| V1_Anglo_triple_0 | Alice | Charlie |
| V1_Anglo_triple_1 | Bob | David |
| V1_Anglo_triple_2 | Charlie | Emma |
| V1_Anglo_triple_3 | Alice | Emma |
| V2_Biblical_triple_0 | Aaron | Gideon |
| V2_Biblical_triple_1 | Joel | Ruth |
| V2_Biblical_triple_2 | Gideon | Abel |
| V2_Biblical_triple_3 | Aaron | Abel |
| V3_Greek_triple_0 | Ajax | Apollo |
| V3_Greek_triple_1 | Jason | Paris |
| V3_Greek_triple_2 | Apollo | Atlas |
| V3_Greek_triple_3 | Ajax | Atlas |
| V4_Roman_triple_0 | Marcus | Augustus |
| V4_Roman_triple_1 | Julius | Felix |
| V4_Roman_triple_2 | Augustus | Diana |
| V4_Roman_triple_3 | Marcus | Diana |
| V5_Modern_triple_0 | Liam | Eli |
| V5_Modern_triple_1 | Noah | Maya |
| V5_Modern_triple_2 | Eli | Finn |
| V5_Modern_triple_3 | Liam | Finn |

**Relation template (pinned):** the "outranks" wording of the higher-in-rank relation — the same
*relation* as the test items (whose prompts use "outranks"/"is lower than" wordings). Template
wording is constant across arms; it enters $h$, not $\hat{b}_D$ (unembedding-space), so it cannot
produce arm differences — pre-registered as design constant L5 [ASSUMPTION].

**$(t_d,f_d)$ token histogram over the donor-entity pool (L4 made auditable) [FACT — counts by
construction].** Per vocabulary, with entities $(e_0..e_4)$:
$n_t$: $e_0\times2, e_1\times1, e_2\times1$; $n_f$: $e_2\times1, e_3\times1, e_4\times1, e_4$
a second time $\Rightarrow$ $n_f$: $e_2\times1, e_3\times1, e_4\times2$.
Concretely, $n_t - n_f$ per vocab: $e_0:+2,\; e_1:+1,\; e_2:0,\; e_3:-1,\; e_4:-2$.
Across the 5 vocabs (25 distinct entities), e.g. $n_t(\text{Alice})=2,\ n_f(\text{Emma})=2,\
n_t(\text{Emma})=0$. The bank is **naturally skewed and disclosed**; it is deliberately NOT
balanced — balancing would annihilate the centroid (degeneracy trap, §4; [PROPOSITION]/INFERENCE
per LOG-144 §a).

### 3.2 Premise-disjointness proof vs the 60 test items

**[PROPOSITION]/INFERENCE (set-disjointness; no experiment).** Test-item premises contain only
entities from the 10-token pool {Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver,
Bronze, Steel}. Every donor premise contains only entities from the 25-entity support pool
{Alice, Bob, Charlie, David, Emma, Aaron, Joel, Gideon, Ruth, Abel, Ajax, Jason, Apollo, Paris,
Atlas, Marcus, Julius, Augustus, Felix, Diana, Liam, Noah, Eli, Maya, Finn}. The two pools are
disjoint; therefore no donor premise triple (ordered entity 3-tuple) can equal any test premise
triple. Additionally, a pre-registered build assert requires: no donor prompt string equals any
of the 60 test prompt strings (FATAL abort on violation).

### 3.3 Law #7 statement (binding)

Donor labels $(t_d, f_d)$ are support-side construction material used **only** to build the
intervention vectors $\hat{b}_D$; they never enter the evaluation objective, the decision rule,
or any selection criterion. Test items are **unlabeled at intervention time**: the vector applied
to test item $j$ is the fixed bank-level centroid $\hat{b}_D$, identical for all 60 test items,
carrying no per-item test label information. The C-A design is label-free-at-test-time by
construction (the donor bank is the only labeled object in the design). [DEFINITION]/[ASSUMPTION]
— Law #7 compliance is structural, verified by the code's data-flow (donor labels flow only into
centroid construction; test labels flow only into scoring).

## 4. Centroid construction and weight-only gates — (c).2 [CENTROID]

### 4.1 Construction formula (pinned)

$$\hat{b}_D \;=\; \mathrm{normalize}\!\left(\sum_{d \in D} \bigl(W_U[t_d] - W_U[f_d]\bigr)\right)
\;=\; \mathrm{normalize}\!\left(\sum_{y} W_U[y]\,(n_t(y) - n_f(y))\right)$$

**sum-of-differences-then-normalize** (LOG-144 recommendation). The per-donor-normalize-then-average
variant is REJECTED for this design (it changes the bypass math: it would up-weight rare-pair
donors and alter the token-prior identity above). The builder has no discretion here.

**[PROPOSITION]/INFERENCE — the confound in one line** (algebra, LOG-144 §a): the centroid is the
donor bank's *token-prior direction* — "usually-right minus usually-wrong" in unembedding space.
The pre-registered bypass model: $\Delta \ell_j(y) \approx \alpha\langle W_U[y], \hat{b}_D\rangle$
+ (attention-mediated terms, not privileged per G1 [OBSERVATION]). No relational computation is
required for a decision flip under this model — only that the argmax over the two named options
moves. This is why H_leak is the null (§1).

### 4.2 Degeneracy gate (pre-registered floor)

**[DEFINITION]** Degeneracy statistic: $g(D) = \|\sum_{d\in D}(W_U[t_d]-W_U[f_d])\| / \sqrt{|D|}$
(pre-normalization norm on the $\sqrt{|D|}$ scale — the EXP078 energy-gate lesson applied at
design time). **Gate:** $g(D) \ge 0.25$ for the C3, C4′, and C5 banks. Below floor → **redesign
the donor bank, never run** (Law #4: a redesigned bank is a new pre-registration, not a patch).

### 4.3 Weight-only similarity audit ($0 GPU — the pre-signing gate)

Computed from weights alone (CPU; $W_U$ only — no forward passes), **before any GPU work and
before the Law #14 signature** (§12):

1. Build $\hat{b}_D$ for C3 (and, once selected, C4′ and C5 banks).
2. For all 60 test items compute $s_t(j)=\cos(\hat{b}_D, W_U[t_j])$, $s_f(j)=\cos(\hat{b}_D, W_U[f_j])$;
   report both full distributions (min/median/max, histogram).
3. **Permutation null:** 200 random donor banks of $|D|=20$ drawn without replacement (within bank)
   from the 150-item same-template support pool ("outranks" triples+quads across the 5 vocabs),
   seed `SEED_PERMNULL=20261123`; null = distribution of $\mathrm{mean}_j\, s_t(j)$ across banks;
   report the observed C3 bank's percentile (descriptive audit, not a decision endpoint).
4. Report $g(D)$ for each bank against the 0.25 floor.

### 4.4 Stratum feasibility gate

The low-similarity stratum (§6) must be **non-empty AND contain $\ge 5$ C1-wrong (headroom) items**.
If empty (or headroom-free) → the benchmark **cannot support the transfer claim in this
operationalization** → **DO-NOT-RUN as a transfer test**. It may still run as a *leakage
demonstration* (§8, outcome (e)) — labeled as such, never as a capability bet (LOG-144 §d.4).

## 5. Arms (all N=60, McNemar exact vs C1 unless noted)

| Arm | Intervention | Role |
|---|---|---|
| **C1** | none | baseline |
| **C2** | per-item oracle self-bridge $b(x_j)=\mathrm{normalize}(W_U[t_j]-W_U[f_j])$ | positive control **and headroom gate** (T2) |
| **C3** | donor-centroid bridge $\hat{b}_{D_{C3}}$ (§3.1, §4.1) | **primary** |
| **C4′** | similarity-matched different-relation donor-centroid bridge | discrimination control (§5.1) |
| **C5** | permuted-label donor bridge (prior preserved, relation destroyed) | content control (§5.2) |
| **C6** | random unit direction | procedure control |

**C2 [FACT]:** identical construction to EXP066/EXP077's positive control (`make_bridge_vec`:
$w=E[t]-E[f]$, normalized, $\alpha=0.50$); EXP077 observed +10pp rescue (56.67%→66.67%,
$p=0.03125$) [OBSERVATION]. If C2 fails to rescue on this run ($p\ge0.05$), the procedure is
invalid and any C3 null is **Inconclusive**, not a kill (T2, §8).

**C6:** $r \sim \mathcal{N}(0, I_d)$, $\hat{b}=r/\|r\|$, seed `SEED_C6=20260989`, $\alpha=0.50$.

The sketch's naive C4 (different-relation donor, unmatched) is **REJECTED** — it confounds
relation with similarity: different-relation donors have a different token-similarity profile, so
C3 > C4 proves nothing about relation (LOG-144 §b.3.8). It is replaced by C4′. The sketch's C5
("random-target donor") is **REJECTED** — it destroys both the relation channel and the prior
channel and therefore discriminates nothing; it is redefined as the permuted-label control
(LOG-144 §b.3.9).

### 5.1 C4′ — similarity-matched different-relation donor — (c).3 [C4′]

**Candidate pool (pinned):** 150 "is next to" support items — for each of the 5 support
vocabularies, the 15 `TRIPLES_INDICES` triples and 15 `QUADS_INDICES` quads with the neutral
template `Premise: {A} is next to {B}. {B} is next to {C}[. {C} is next to {D}.] Question: Who is
higher in rank, {q_opts}? Answer:` (the EXP078 `p_neu` construction, verbatim convention;
$(t_c, f_c) = (A, C)$ for triples, $(A, D)$ for quads). ids:
`ca_C4cand_{vk}_triple_{i}` / `ca_C4cand_{vk}_quad_{i}`.
[ASSUMPTION] A4: "is next to" carries no rank-order relational content (its program role is the
neutral contrast template, EXP078 §1). Different relation from C3's "outranks" by construction.

**Pre-registered greedy-matching algorithm (weights-only, $0 GPU):**

1. Compute C3's similarity profile $s_t^{C3}(j), s_f^{C3}(j)$ for $j=1..60$ (§4.3).
2. $B_0 = \emptyset$. At step $k \ge 1$: for each candidate $c \in P \setminus B_{k-1}$, form
   $B = B_{k-1} \cup \{c\}$, build its centroid by the §4.1 formula, compute its similarity
   profile $s_t^{B}(j), s_f^{B}(j)$, and the discrepancy
   $$D(B) = \tfrac{1}{60}\sum_{j=1}^{60}\Bigl(|s_t^{B}(j)-s_t^{C3}(j)| + |s_f^{B}(j)-s_f^{C3}(j)|\Bigr).$$
   Choose the $c$ minimizing $D$ (ties → lowest candidate index — deterministic, no seed needed).
3. Stop when $D(B_k) \le \delta$ or $|B_k| = 30$ (cap).
4. **Pinned tolerance:** $\delta = 0.05$ (mean absolute similarity-profile deviation).

**Achieved-match report (pre-GPU, attached to the audit):** final $|B|$, achieved $D$, the
selected donor ids, $g(B)$ against the 0.25 floor, and the per-item $|s_t^B - s_t^{C3}|$,
$|s_f^B - s_f^{C3}|$ distributions.

**Pre-registered fallback (Law #4):** if $\min D > \delta$ at the 30-donor cap, matching has
**failed**. The C3-vs-C4′ contrast is then **demoted to exploratory**; the stratum analysis (§6)
becomes the primary discrimination. The T3 conjunct is marked exploratory-not-deciding (§8,
outcome (d)). **No post-hoc promotion**: a failed match can never be re-argued as support for
transfer.

### 5.2 C5 — permuted-label donor (prior-preserving, relation-destroying) — (c).4 [C5]

Same 20 donor premises as C3 (§3.1). Let the donor pairs be ordered $(t_0,f_0)..(t_{19},f_{19})$.
Draw permutation $\pi$ of $\{0..19\}$ with `numpy.random.default_rng(SEED_C5_PERM=20261067)`;
if $\pi(i)=i$ for any $i$, re-draw with seed $+1$ (deterministic rule, pinned). Donor $d_i$'s
pair becomes $(t_{\pi(i)},\, f_i)$: the **target multiset and foil multiset are preserved
exactly**, so $(n_t - n_f)$ — the bank token prior — is **identical** to C3's, while per-donor
relational pairing is destroyed.

**[PROPOSITION]/INFERENCE** (multiset preservation by construction): C5's centroid differs from
C3's only in which target tokens are paired with which donor premises; the prior channel is
held fixed, so any C3-vs-C5 rescue gap is attributable to per-donor relational content, and
C5 ≈ C3 shows the rescue is prior/similarity steering. If C5 rescues indistinguishably from C3
(paired McNemar C3-vs-C5 $p\ge0.05$ with C3 vs C1 significant), H_transfer is **Refuted** under
this operationalization (LOG-144 §d).

## 6. Strata — (c).5 [STRATA]

**Split rule frozen before any forward pass (pinned):** median split on $s_t^{C3}(j)$ (C3's
target-similarity feature, §4.3) over the 60 test items, computed in Stage 0 from weights alone.
Low stratum: $s_t^{C3}(j) \le \mathrm{median}$ (ties → low); high stratum: $s_t^{C3}(j) >
\mathrm{median}$. ~30/30 items. No tertiles, no post-hoc re-cutting (Law #9).

**Decision endpoint:** within-stratum McNemar exact C3-vs-C1 (two-sided, $\alpha=0.05$).
Transfer requires the **low-similarity stratum to fire** (T4: $p<0.05$, $\Delta M>0$).
[INFERENCE]: leakage predicts rescue concentrates in the high stratum (rescue predicted by
$s_t(j)-s_f(j)$); transfer predicts rescue in the low stratum where similarity cannot explain it.
Feasibility gate §4.4 applies (low stratum non-empty with $\ge 5$ headroom items, else DO-NOT-RUN
as a transfer test).

## 7. Item-level model — (c).6 [MODEL]

**Pre-registered model.** Pooled item-level data over arms $a \in \{C3, C4'\}$ ($120$ rows):
$$\mathrm{rescue}_{j,a} = \mathbf{1}\{\text{C1 wrong on } j \;\&\; \text{arm } a \text{ correct on } j\},$$
$$\mathrm{logit}\,P(\mathrm{rescue}_{j,a}=1) \;=\; \beta_0 + \beta_1\cdot\mathrm{relmatch}_{j,a}
+ \beta_2\cdot s_t^{(a)}(j) + \beta_3\cdot s_f^{(a)}(j),$$
where $\mathrm{relmatch}_{j,a}=1$ iff $a=C3$ (same-relation donor) else $0$, and
$s_t^{(a)}(j), s_f^{(a)}(j)$ are the **arm-specific** similarity features (each arm's own
centroid). Fit: logistic regression (`statsmodels`), **item-clustered sandwich standard errors**
(60 clusters), two-sided Wald test. **T6:** $\beta_1 > 0$ **and** two-sided $p < 0.05$ with
$(s_t, s_f)$ covaried. [INFERENCE]: this is the precise "survives stratification" the sketch
gestured at — the relation-match indicator must carry weight *beyond* what token similarity
explains.

## 8. Decision tree — (c).7 [DECISION TREE]

All McNemar tests: exact two-sided via `scipy.stats.binomtest` on $(b,c)$ discordant pairs;
$b=c=0 \Rightarrow p=1.0$ (harness `compute_paired_stats`, EXP077 verbatim); $\alpha=0.05$.
$\Delta M = (b-c)/N$ (arm minus C1), reported in pp.

**Conjuncts (evaluated in order):**
- **T1:** C3 vs C1: $\Delta M > 0$, $p < 0.05$.
- **T2 (headroom gate, first):** C2 vs C1 rescues ($p < 0.05$). If $p \ge 0.05$ → procedure
  invalid → **Inconclusive** (any C3 null uninterpretable; no kill licensed).
- **T3:** C3 beats C4′ on paired decisions (McNemar on per-item C3-vs-C4′ outcomes, $b$ = C3
  correct & C4′ wrong): $p < 0.05$ with $b > c$.
- **T4:** low-similarity stratum fires: within-stratum McNemar C3-vs-C1 $p < 0.05$, $\Delta M > 0$.
- **T5:** C5 does **not** rescue: C5 vs C1 $p \ge 0.05$.
- **T6:** item-level model: $\beta_1 > 0$, two-sided Wald $p < 0.05$ with $(s_t, s_f)$ covaried.

| # | Outcome | Verdict on H_transfer |
|---|---|---|
| (a) | T2 holds; **T1–T6 ALL hold conjunctively** | **Supported** — transfer license, capped at evidentiary **Level 1**: "a same-relation donor-centroid bridge can improve inference on headroom items via relation-mediated steering at pythia-410m/$l^*$=20/$\alpha$=0.50 on this benchmark." No Level 2/3 language (P1). |
| (b) | T2 holds; $\Delta M_{C3} \le 0$ ($p \ge 0.05$) — the sketch's kill | **Not supported**; **family-level kill licensed ONLY for unembedding-difference donor bridges at $l^*$=20 on this benchmark** — donor bridge is item-specific; the transfer hope for *this intervention family* is dead. Does NOT kill the oracle self-bridge family (C2 stands), hidden-state transfer (different family; EXP058's kill already covers its static form), or any other pre-registration. |
| (c) | T1 holds but **any of T3–T6 fails** | **Not supported** (leakage verdict). **Refuted** under this operationalization if additionally: C4′ rescues vs C1 ($p<0.05$) while T3 fails (C4′ ≈ C3 — different relation, same similarity, same rescue); **or** C5 rescues vs C1 ($p<0.05$); **or** paired C3-vs-C5 $p \ge 0.05$ with C3 vs C1 significant; **or** rescue is fully accounted for by $s_t(j)-s_f(j)$ with $\beta_1$ null. Any of these shows the donor bridge's causal power is *entirely* token-identity/similarity/prior steering. |
| (d) | C4′ matching failed ($D > \delta$): T3 demoted to exploratory | **Underdetermined** if stratum/model readings conflict or strata underpowered; else verdict follows T1,T2,T4,T5,T6 with T3 marked exploratory-not-deciding. A failed match is never re-argued as transfer support (Law #4). |
| (e) | T2 fails (C2 $p \ge 0.05$) | **Inconclusive** — procedure invalid; no verdict on H_transfer, no kill. |
| (f) | Stratum feasibility gate failed (§4.4) | **DO-NOT-RUN as a transfer test.** May run as a *leakage demonstration* only, under a separate pre-registration labeled as such (Law #4) — never as a capability bet. |

"Partial transfer" is not a verdict (LOG-148 verdict standard). If outcome (c) fires with
quantitative C4′/C5 match to C3, the program's "best label-free capability candidate" slot
**vacates**: C-A is removed from Tier 1; C-B (self-bridge fixed point) becomes the lead
capability bet per the sprint's recommended sequence (LOG-144 §d). A leakage verdict is a
first-class **negative result** for the boundary paper's mechanism section (donor bridges rescue
via similarity/prior steering, not relational transfer — consistent with and strengthening audit
Finding 4 and G1), publishable as boundary science, not as a capability.

### LICENSES (binding; Law #4/#11)

> "A C3 win that fails any of T3–T6 is not transfer; it is similarity/prior steering consistent with audit Finding 4."

(verbatim, LOG-144 §b.6.16). The license side is written with equal force to the kill side:
the sketch's one-sided kill criterion (null kills, win auto-licenses) is replaced by the
conjunctive T1–T6 license above. A C3 win licenses **at most** Level 1; it never licenses claims
about hidden-state transfer, other models/layers/$\alpha$, or adaptive-loop efficacy.

## 9. Endpoints and guards — (c).8 [ENDPOINTS]

- **Decision endpoints: McNemar exact only** (per-arm vs C1; paired C3-vs-C4′; within-stratum
  C3-vs-C1; paired C3-vs-C5 for the refutation check). No margins, no Wilcoxon, no KL, no
  cosine-deltas as decision endpoints — anywhere (Law #9; audit Finding 3: the B_wrong
  $p=1.2\times10^{-8}$ with $b=c=0$ invalidated margins).
- **C2-headroom gate** (T2, §8): procedure validity precedes all verdicts.
- **Evidentiary level capped at Level 1** ("can improve inference"). No Level 2 ("changes
  computational strategy") or Level 3 ("creates qualitatively new capability") language (P1).
- KL divergence is an **exploratory guardrail only** (mean KL < 0.50, EXP077 precedent) —
  reported, never deciding.
- F1 injection-norm guard (all static injection vectors norm > 0, verbatim EXP077) and F2
  single-token guard (§2) are pre-registered build asserts, not endpoints.

## 10. Budget, seeds, guards, and provenance — (c).9 [HYGIENE]

**Forward-pass budget recomputed from first principles [FACT — arithmetic]:** 6 arms (C1, C2, C3,
C4′, C5, C6) × 60 items × 1 forward pass per item-arm = **360 forward passes**. All intervention
vectors are weight-computed (centroids from $W_U$; C2 per-item bridges from $W_U$; C6 from a
seeded RNG) — vector construction costs **zero** forward passes. The sprint's "2,700 passes"
does not follow from the arm structure and is **superseded** by this number (LOG-144 §b.6.15).
Stage 0 (weight-only audit, §4.3) costs 0 GPU passes. Estimated GPU time: ~20–30 s on 2×T4
(EXP077's comparable battery: 1,740 passes ≈ 2 min ⇒ 360 passes ≈ 25 s [ESTIMATE]).

**Pinned:** `SEED_TORCH=SEED_NUMPY=20260923` (EXP078 precedent); `SEED_C5_PERM=20261067`
(permuted-label control); `SEED_C6=20260989` (random direction); `SEED_PERMNULL=20261123`
(similarity-audit null); C4′ greedy matching deterministic (tie-break: lowest candidate index).
$\alpha=0.50$, $l^*=20$, hook = last-token residual stream at layer-20 output (§2).

**SHA-256 $\Delta\theta=0$ guards (Law #6/#13):** `get_hash` verbatim from the EXP077 harness
(SHA-256 over concatenated `state_dict()` tensors, sorted keys, CPU float32 bytes) computed
pre-run and post-run; mismatch → FATAL, run void. No weights, biases, adapters, or normalization
statistics are updated at any point.

**Cited and distinguished:**
- **EXP058** (LOG-066, `experiments/protocols/EXP058_BASIS_TRANSFER_SPEC.md`): a causal basis
  inferred on Domain A transferred zero-shot to Domain B (N=30, pythia-160m): Matched Transfer
  53.3% vs Base 60.0% ($\Delta M=-6.7$pp, McNemar $p=0.8906$), verdict TRANSFER_WEAK_OR_SPECIFIC
  [OBSERVATION]. **Distinguished:** EXP058 killed zero-shot transfer of *hidden-state inferred
  bases* across disjoint domains — a different mechanism family and granularity. C-A tests
  *output-side unembedding-difference donor bridges* at fixed $l^*$=20 — EXP058's kill does not
  extend to this family, and C-A is not a replication of EXP058.
- **EXP078 branch (a)** (LOG-116/120 entries): ENERGY_GATE_HALT — the bridge's causal power lies
  almost entirely outside the support-derived relational-contrast subspace $S$
  ($e_{\mathrm{median}}=0.0544 < 0.10$ bar) [OBSERVATION]. **Distinguished:** this is *why* a
  donor bridge cannot be a relational-contrast direction in disguise — if C-A's C3 works, it
  works as readout steering, and the only question is whether the steering is relation-mediated
  (hence the T3–T6 discrimination battery). EXP078's halt does not pre-empt C-A; it motivates it.
- **EXP077** (executed 2026-09-23): all static geometric variants null ($\Delta M=0$, $p=1.0$);
  the output-bridge positive control rescued +10pp (56.67%→66.67%, $p=0.03125$) [OBSERVATION] —
  provenance of the C2 configuration reused here.

**Novelty: N1 retained** (Known combination — `research/README_LITERATURE.md` §N1; Law #10). The
operator is equivalent to static steering-vector application (CAA, Rimsky et al.); the delta is
the *confound-aware transfer design* (similarity-matched C4′, permuted-label C5, conjunctive
T1–T6 license), which the September-2026 literature sweep found no prior art for as a combined
discrimination battery.

**Do NOT "fix" leakage by balancing the donor bank** (degeneracy trap, §3.1/§4.2): a balanced
bank ($n_t(y)\approx n_f(y)$) makes $\sum_d(W_U[t_d]-W_U[f_d])\approx0$ and $\hat{b}_D$ a
renormalized near-noise vector — C3 becomes C6 by construction, with zero power under *both*
hypotheses. Balancing does not de-confound; it annihilates. The bank stays natural and skewed;
discrimination comes from controls + stratification, never from bank surgery.

## 11. What a leakage verdict licenses and does NOT license

**Licenses (LOG-144 §d):** (1) H_transfer → **Refuted** under the tested operationalization
(unembedding-difference donor bridges, $l^*$=20, this benchmark); C-A vacates the Tier-1
capability slot. (2) A first-class negative result for the boundary paper's mechanism section.
(3) It does **NOT** license: killing the oracle self-bridge family (C2's rescue stands — the
mechanism question narrows to what lawful structure, if any, lives in $W_U$ differences beyond
token identity); any claim about hidden-state transfer; any weakening of other pre-registrations.

## 12. Pre-signing gate (Law #14 reviewer checklist)

The reviewer signs **iff** every item is present, pinned, and — for the weight-only audit —
**computed and attached** (Stage 0, CPU, before signature):

1. [DONORS] §3: exact 20-donor list, "outranks" template, premise-disjointness proof, $(t_d,f_d)$
   histogram, Law #7 statement. ☐
2. [CENTROID] §4.1–4.2: pinned sum-of-differences formula; degeneracy floor 0.25 with computed
   $g(D)$ for C3/C4′/C5 banks attached. ☐
3. [C4′] §5.1: greedy-matching algorithm, $\delta=0.05$, achieved-match report attached,
   demotion fallback. ☐
4. [C5] §5.2: permuted-label construction, seed pinned, prior-preservation argument. ☐
5. [STRATA] §6: median-split rule frozen pre-forward-pass; low-stratum feasibility ($\ge 5$
   headroom items) computed and attached. ☐
6. [MODEL] §7: logistic spec, arm-specific $(s_t,s_f)$, item-clustered SEs, T6 criterion. ☐
7. [DECISION TREE] §8: outcomes (a)–(f), T1–T6 conjunctive, verdicts from the permitted set only,
   anti-creep sentence verbatim in LICENSES. ☐
8. [ENDPOINTS] §9: McNemar exact only; C2-headroom gate; Level-1 cap. ☐
9. [HYGIENE] §10: 360-pass budget recomputed; seeds/$\alpha$/$l^*$/hook pinned; SHA-256 guards;
   EXP058 + EXP078(a) cited-and-distinguished; N1 retained; no bank balancing. ☐

A draft missing any item is **rejected** with the missing items enumerated (LOG-144 §c).
No partial signatures.

## 13. Assumptions, risks, challenge, and idea

**Open assumptions (declared debts, M2.1):** [ASSUMPTION] A4 ("is next to" is relation-neutral);
[ASSUMPTION] L5 (template wording cannot produce arm differences — enters $h$, not
$\hat{b}_D$); [ASSUMPTION] the bypass model $\Delta\ell_j(y)\approx\alpha\langle
W_U[y],\hat{b}_D\rangle$ holds to first order for QK-unremarkable directions (G1
[OBSERVATION] motivates; attention-mediated terms not privileged). **Risk (disclosed):**
similarity matching on the *same* 25-entity support pool pushes the C4′ centroid geometrically
toward C3's; the T3 contrast relies on the residual difference inside the $\delta=0.05$ envelope —
if matching only succeeds by near-identical banks, the fallback (§5.1) fires by design.

**One challenge (§2 obligation):** the strongest attack on this design is that T5 is asymmetric:
C5 preserves the prior *exactly* but also preserves C3's exact similarity profile up to pairing
permutation — so a C5 rescue does not distinguish "prior steering" from "similarity steering
with shuffled pairings." The spec's answer is pre-registered: either way H_transfer is refuted
(the relation template contributed nothing), and the C4′/stratum/model battery — not C5 alone —
carries the similarity-vs-prior split. If the reviewer wants the split sharper, the
permuted-bank family (idea below) is the next design, not a patch to this one.

**One idea (§2 obligation):** a *permuted-bank null family* as a follow-up design (new number,
Law #4): $k$ independent C5-style permuted banks (seeds $1..k$) run as full arms, testing
whether C3's $\Delta M$ is an outlier of the permuted-bank rescue distribution (exact
permutation test on $\Delta M$). Cheapest falsifier of "the bank's specific pairing matters";
kill = C3's $\Delta M$ inside the permuted null. Cost: $k \times 60$ passes. Not in this design.

## 14. Change protocol

Any change to donors, templates, formulas, gates, tolerances, seeds, $\alpha$, $l^*$, hook,
endpoints, strata, model, or decision tree after signing = a **new experiment number**
(Law #4). Corrections to this DRAFT are proposed to the reviewer, never applied silently.
