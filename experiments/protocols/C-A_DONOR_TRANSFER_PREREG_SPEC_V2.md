# EXP081 — Cross-Item Donor-Bridge Transfer: Pre-Registration Spec (V2, PRE-REGISTERED)

**Status: PRE-REGISTERED — signed by the CEO (Research Lead) under LOG-182, 2026-09-23,
on the LOG-181 Law #14 re-review SIGN-WITH-FIXES
(`reports/adversarial_review_c-a_prereg_v2_2026-09-23.md`) with fixes F1–F2 applied
and verified in this file.** Experiment number **EXP081** minted at signing (next free;
re-verified unminted at signing time). No GPU executed; no primary
artifacts touched; no signed protocols modified. V1
(`C-A_DONOR_TRANSFER_PREREG_SPEC.md`, DRAFT LOG-150) is left untouched per
signed-draft discipline. **No GPU until CEO clearance at launch time.**

**Date:** 2026-09-23 · **Dispatch:** LOG-179 · **Author role:** C-A pre-registration v2 drafter
**Source idea:** `research/innovation/SPRINT2_2026-09-23.md` §C-A (verbatim sketch verified
by LOG-144 reviewer); **binding constraints:** `reports/adversarial_review_c-a_confound_2026-09-23.md`
(LOG-144); `reports/adversarial_review_c-a_prereg_2026-09-23.md` (LOG-161 SIGN-WITH-CONDITION
+ LOG-176 conversion ruling: REVISE — the five binding redesign requirements below).
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `research/TEAM_KNOWLEDGE_PROTOCOL.md`,
`research/MATH_STANDARDS_CHARTER.md` (binding M1–M8), `experiments/protocols/STATISTICAL_PROTOCOL_V02.md`,
`theory/BOUNDARY_CLAIM_FORMALIZATION.md` (boundary null I1), `research/README_LITERATURE.md` (novelty),
`research/CHATGPT_MENTORSHIP_DIRECTIVE.md` (P1–P4, three evidentiary levels, FACT/INFERENCE/HYPOTHESIS/SPECULATION
reporting layer atop the repo 10-label standard), LOG-148 verdict standard.
**Roadmap phase:** Phase 4 (transferable intervention = autonomous-capability primitive; sprint §C-A).
**Execution rule:** Strictly confirmatory. Changed design = the next free number at
pre-registration time (Law #4). No margins/Wilcoxon/KL as decision endpoints (Law #9).
**Attached weight-only audit:** `experiments/protocols/C-A_PREAUDIT_2026-09-23.md` + `.json`
(LOG-160 Part 1 + LOG-174 Part 2; CPU, $0 GPU, zero forward passes). V2 is consistent with
every computed value in it; values that do not survive the redesign are marked RETIRED, never
edited.

**Corpus read (TEAM_KNOWLEDGE_PROTOCOL §1):** `research/TEAM_KNOWLEDGE_PROTOCOL.md`;
`reports/adversarial_review_c-a_confound_2026-09-23.md` (LOG-144, binding);
`reports/adversarial_review_c-a_prereg_2026-09-23.md` (LOG-161 + LOG-176, binding);
`experiments/protocols/C-A_DONOR_TRANSFER_PREREG_SPEC.md` (v1 DRAFT, revised — not modified);
`experiments/protocols/C-A_PREAUDIT_2026-09-23.md` + `.json` (binding computed values);
`SCBI/AGENTS.md` (14 laws); `research/innovation/SPRINT2_2026-09-23.md` §C-A (sketch);
`experiments/runs/exp077/run_exp077.py` (benchmark construction, `make_bridge_vec`, McNemar
harness, `get_hash`, F1/F2 guards); `experiments/runs/exp078/run_exp078.py` (support
vocabularies, "is next to" neutral template, EXP078 branch-(a) provenance);
`experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md` (format precedent);
`research/MATH_STANDARDS_CHARTER.md` (M1–M8); `theory/BOUNDARY_CLAIM_FORMALIZATION.md` (I1);
`reports/research_log.md` LOG-066 (EXP058), EXP078(a) ruling (LOG-116/120 entries), LOG-149/150,
LOG-160/174 (audit), LOG-176 (conversion ruling) dispatch entries.

## R0. Revision record — LOG-176's five binding requirements and their discharge

V1 (LOG-150) received LOG-161 SIGN-WITH-CONDITION; the attached weight-only audit then
falsified a pinned v1 proposition (C5 ≡ C3 by construction), and the LOG-176 conversion ruling
returned **REVISE** with five binding redesign requirements. This v2 draft discharges each;
the re-review will check each item. (Law #4 binds at signing: no number is consumed by this
revision; v2 takes no number.)

**Requirement 1 — "Resolve C5 honestly: drop the arm or prove a distinct prior-control."**
**Discharged by DELETION with proof** (§5.2, §R0.1 below). C5 is dropped. The v1 §5.2
[PROPOSITION] ("C5's centroid differs from C3's") was false as pinned and is struck, not
patched. The identity theorem is stated explicitly (§4.1 [THEOREM]): any bank preserving the
exact per-token $(n_t-n_f)$ has a centroid identical to C3's — so no multiset-preserving
permutation, re-pairing, or same-entity relabeling can produce a geometrically distinct
prior-control under the pinned construction. A bank with a *different* $(n_t-n_f)$ does not
hold the prior channel fixed and therefore cannot attribute a rescue gap to relational content
(the same confound for which the sketch's naive C4 was rejected in v1 §5). The three
desiderata — preserve the prior, destroy the relation, differ geometrically — are jointly
unsatisfiable in the sum-of-differences family; no prior-control exists to be built, so none is
built. Budget recomputes to **300 deciding passes** (§10); `SEED_C5_PERM=20261067` is RETIRED.
The old T5 (C5 conjunct) is deleted; the item-level model is renumbered old-T6 → new-T5
(mapping pinned in §8).

**Requirement 2 — "Decide the T3/T4/T6-without-prior-control battery explicitly."**
**Discharged** (§8). With C5 dropped, discrimination rests on T3 (C4′ contrast), T4 (low-similarity
stratum), T5 (item-level model, ex-T6). The draft carries the theory-role affirmation that this
battery suffices (§8, [AFFIRMATION]): T3 closes the donor-relation-template channel with
similarity matched within δ; T4 closes the within-bank similarity-gradient channel; T5 closes
the per-item similarity-covariate channel — the three observable implications of
relation-mediated steering. The bank-prior channel cannot be independently lesioned in this
family (identity theorem); this is recorded as a *known limitation of the Level-1 license*,
not a hole in the battery. The §13 permuted-bank idea is dropped as vacuous under the identity
and rebuilt as a different-algebra follow-up (new number, Law #4). Every decision-tree terminal
is proved reachable (§8, reachability proofs): outcome (a) Supported is reachable — v2 is not a
kill-only machine — and no tautological refutation clause survives (the v1 paired C3-vs-C5
clause is deleted).

**Requirement 3 — "Carry the T4 entity-group caveat into the license language."**
**Discharged** (§6, §8). The "~30/30" aside does not survive in v2 — it is replaced by the
computed 49/11 split [FACT]. T4's license language states the binding caveat: T4 licenses at
most transfer across **3 independent low-similarity target entities** ({Mars, Venus, Iron}),
not a per-item gradient; the stratifying feature has zero within-entity variation.

**Requirement 4 — "Harden C4′ selection against the singleton fragility."**
**Discharged** (§5.1). The audit applied the pinned greedy rule verbatim and selected the
singleton `ca_C4cand_V5_Modern_triple_1` (D=0.046564, within 7% of δ) — the bank stands as
computed; the fragility is disclosed in the T3 reading, not hidden. Hardening takes the
tie-break-robustness form (the ruling's licensed option): a pre-registered **sensitivity
battery S1–S6** — the 6 non-winner singleton candidates with D ≤ δ, run as exploratory arms
(360 passes), reported descriptively with a pinned agreement flag that can mark the T3 reading
"tie-break-fragile" but can never promote or demote the verdict. The already-resolved
demotion fallback is deleted (the match succeeded; keeping it would be an unreachable branch).

**Requirement 5 — "Recompute the budget; re-attach the $0 pre-audit values that still apply."**
**Discharged** (§10, §4). Budget: 5 deciding arms × 60 items = **300 passes** (the ruling's
figure), plus the 360-pass exploratory sensitivity battery = **660 total**; Stage 0 remains
0 GPU passes. Re-attached [FACT — computed] values: g(C3)=1.061783, g(C4′)=0.860981 (floor
0.25, both PASS); C4′ achieved match (D=0.046564 ≤ δ=0.05, singleton, id pinned); strata 49/11
with 23 low-stratum headroom items (≥5, PASS); s_t/s_f distributions; permutation null
(observed bank at the 38.0th percentile); donor $(t_d,f_d)$ histogram (25-entity pool,
confirmed); Δθ=0 (SHA-256 tri-match `ec276abe3902fab0…`). C5's audit values (seed 20261069,
cos = 1.0) are RETIRED as license values and retained only as the evidence for the identity
finding. §4.5 pins the recomputation rule: if the bank set changes (donor list, C4′ selection),
g(D), s_t/s_f profiles, strata, headroom, achieved-match D, and the permutation-null
percentile must all be recomputed before signing.

### R0.1 The C5 deletion proof (recorded once, referenced by §5.2)

[THEOREM — from the pinned §4.1 construction; FACT — computed in the audit]:
under sum-of-differences-then-normalize, the centroid is a function of the per-token
$(n_t-n_f)$ alone. Hence: (a) any bank with the identical $(n_t-n_f)$ as C3 has a centroid
**identical** to C3's (audit: cos = 0.9999999999999998, ‖S_C5−S_C3‖ = 0.000e+00) — a
prior-preserving control is geometrically vacuous; (b) any bank with a different $(n_t-n_f)$
has a different prior channel — a rescue gap against C3 then confounds relational content
with prior difference and discriminates nothing (v1 §5's own rejection logic for the naive
C4). Desiderata (i) prior preserved, (ii) relation destroyed, (iii) geometrically distinct
are jointly unsatisfiable in this intervention family. **Therefore no honest C5 exists; the
arm is deleted.** The identity is itself a publishable lemma about the unembedding-difference
intervention family (per the ruling).

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
**Renumbering note (v1 → v2):** v1's T5 (C5 conjunct) is deleted; v1's T6 (item-level model) is
**T5** in v2. All other conjunct numbers are unchanged.

## 1. Research question and hypotheses

**Question.** Is the output bridge's rescue relation-general or item-specific? Apply a bridge
direction built from *labeled donor items* (entity-disjoint, same relation template) to unlabeled
test items — the first test of whether the program's one working intervention family has
transferable structure, and the path to label-free-at-test-time gains (donor bank from labeled
support). [CONJECTURE] / SPECULATION (the capability bet).

**[HYPOTHESIS] H_transfer:** the same-relation donor-centroid bridge C3 rescues test items
*via relation-mediated structure* — i.e., its causal power survives the discrimination battery
that holds token-similarity channels at bay (T1–T5 conjunctive, §8).

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
win, not a corner case.** A C3 win that fails any of T3–T5 is similarity/prior steering, not
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
construction; confirmed by the weight-only audit].** Per vocabulary, with entities $(e_0..e_4)$:
$n_t - n_f$ per vocab: $e_0:+2,\; e_1:+1,\; e_2:0,\; e_3:-1,\; e_4:-2$.
Across the 5 vocabs (25 distinct entities), e.g. $n_t(\text{Alice})=2,\ n_f(\text{Emma})=2,\
n_t(\text{Emma})=0$. The bank is **naturally skewed and disclosed**; it is deliberately NOT
balanced — balancing would annihilate the centroid (degeneracy trap, §4; [PROPOSITION]/INFERENCE
per LOG-144 §a). The audit verified the per-entity $(n_t-n_f)$ identity against the pinned donor
rows [FACT — computed].

### 3.2 Premise-disjointness proof vs the 60 test items

**[PROPOSITION]/INFERENCE (set-disjointness; no experiment).** Test-item premises contain only
entities from the 10-token pool {Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver,
Bronze, Steel}. Every donor premise contains only entities from the 25-entity support pool
{Alice, Bob, Charlie, David, Emma, Aaron, Joel, Gideon, Ruth, Abel, Ajax, Jason, Apollo, Paris,
Atlas, Marcus, Julius, Augustus, Felix, Diana, Liam, Noah, Eli, Maya, Finn}. The two pools are
disjoint; therefore no donor premise triple (ordered entity 3-tuple) can equal any test premise
triple. Additionally, a pre-registered build assert requires: no donor prompt string equals any
of the 60 test prompt strings (FATAL abort on violation) — the audit verified overlap = ∅
[FACT — computed].

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

**[THEOREM] — the prior-channel/vector identity (publishable lemma; proved from the pinned
construction).** For any two donor banks $D, D'$ over the same vocabulary, if
$n_t(y) - n_f(y) = n_t'(y) - n_f'(y)$ for every token $y$, then $\hat{b}_D \equiv \hat{b}_{D'}$
exactly. *Proof.* $\sum_{d\in D}(W_U[t_d]-W_U[f_d]) = \sum_y W_U[y]\,(n_t(y)-n_f(y))$ by
regrouping terms; identical per-token coefficients give identical unnormalized sums, hence
identical vectors after normalization. ∎
**Corollary (no prior-control in this family).** A label-informed bank that preserves the exact
bank token prior has a centroid identical to C3's — geometrically vacuous as a control. A bank
with a different $(n_t-n_f)$ has a different prior channel and cannot attribute a rescue gap to
relational content. The three desiderata (prior preserved / relation destroyed / geometrically
distinct) are jointly unsatisfiable under sum-of-differences-then-normalize. This is why §5.2
deletes C5 rather than repairing it (full proof recorded in §R0.1).

### 4.2 Degeneracy gate (pre-registered floor)

**[DEFINITION]** Degeneracy statistic: $g(D) = \|\sum_{d\in D}(W_U[t_d]-W_U[f_d])\| / \sqrt{|D|}$
(pre-normalization norm on the $\sqrt{|D|}$ scale — the EXP078 energy-gate lesson applied at
design time). **Gate:** $g(D) \ge 0.25$ for the C3 and C4′ banks. Below floor → **redesign
the donor bank, never run** (Law #4: a redesigned bank is a new pre-registration, not a patch).

**Attached [FACT — computed, LOG-160/174]:** $g(C3) = 1.061783 \ge 0.25$ (**PASS**, 4.25× floor);
$g(C4') = 0.860981 \ge 0.25$ (**PASS**, 3.44× floor). The C3 value was independently recomputed
via the per-entity $(n_t-n_f)$ identity — identical to 6 decimals. No redesign required.

### 4.3 Weight-only similarity audit ($0 GPU — attached pre-signing values)

Computed from weights alone (CPU; $W_U$ only — no forward passes). Values below are
[FACT — computed] from `C-A_PREAUDIT_2026-09-23.md` + `.json`:

1. $s_t(j)=\cos(\hat{b}_{C3}, W_U[t_j])$, $s_f(j)=\cos(\hat{b}_{C3}, W_U[f_j])$, $j=1..60$:
   $s_t$: min **−0.091793**, median **−0.035416**, max **0.081702**, mean −0.038264, std 0.032482;
   $s_f$: min **−0.039005**, median **0.010345**, max **0.081702**, mean −0.003907, std 0.028335.
   Count with $s_t(j) > s_f(j)$: **9/60**. All $|\cos| < 0.1$: the donor centroid is
   near-orthogonal to every test target's unembedding row — the token-similarity channel is
   **weak in absolute terms**.
2. **Structural [FACT]:** $s_t(j)$ depends only on the item's target entity — exactly **6 distinct
   values**: Venus −0.091793 (7 items), Mars −0.048545 (21), Iron −0.035416 (21),
   Gold −0.015161 (7), Silver 0.026304 (2), Jupiter 0.081702 (2).
3. **Permutation null** (`SEED_PERMNULL=20261123`, 200 banks, $|D|=20$, same-template support
   pool; null = $\mathrm{mean}_j\, s_t(j)$): null −0.034053 ± 0.013496; p5/p50/p95 =
   −0.057162/−0.033560/−0.012494; observed C3 bank at the **38.0th percentile** — squarely
   typical, not an outlier (descriptive audit, not a decision endpoint).

### 4.4 Stratum feasibility gate

The low-similarity stratum (§6) must be **non-empty AND contain $\ge 5$ C1-wrong (headroom) items**.

**Attached [FACT — computed, LOG-160]:** median $s_t^{C3} = -0.035416$ (= Iron's $s_t$ exactly;
ties → low). Low stratum = **49** items ({Mars 21, Venus 7, Iron 21}); high stratum = **11**
items ({Gold 7, Silver 2, Jupiter 2}). C1-wrong overall **26/60** (EXP066 executed pythia-410m
baseline, prompt-verified identical items, strict-$>$ rule — prior artifact, no new forward
pass). **Low-stratum headroom = 23 ≥ 5.** **Gate: PASS** with large margin.

**Binding interpretive caveat (LOG-176 requirement 3):** because $s_t$ takes only 6 distinct
values, the pinned median split is necessarily an **entity-group split**, not a per-item
gradient. T4 tests rescue on low-similarity *target entities* with exactly **3 independent
entity-level observations** in the low stratum. The v1 "~30/30" aside was an expectation under
a continuous-feature assumption; it does not obtain and **does not survive in v2**.

If the gate had failed (empty or headroom-free low stratum), the benchmark could not support
the transfer claim in this operationalization → **DO-NOT-RUN as a transfer test** (it may run
as a *leakage demonstration* under a separate pre-registration labeled as such — Law #4).
The gate **passed**; no DO-NOT-RUN branch remains in the decision tree (§8).

### 4.5 Audit-value dependency (pre-registered recomputation rule)

The §4.2–4.4 values are computed against the **bank set** {C3 20-donor list (§3.1), C4′
selected singleton (§5.1)}. **If the bank set changes** (donor list edit, different C4′
selection, any construction change), the following must be **recomputed from weights alone
before signing**: $g(D)$ for every bank; the $s_t/s_f$ profiles; the median split, strata,
and headroom; the C4′ achieved-match $D$; the permutation-null percentile. C5's audit values
(seed 20261069, cos = 1.0) are RETIRED as license values — retained only as the evidence for
the §R0.1 identity finding.

## 5. Arms (all N=60, McNemar exact vs C1 unless noted)

| Arm | Intervention | Role |
|---|---|---|
| **C1** | none | baseline |
| **C2** | per-item oracle self-bridge $b(x_j)=\mathrm{normalize}(W_U[t_j]-W_U[f_j])$ | positive control **and headroom gate** (T2) |
| **C3** | donor-centroid bridge $\hat{b}_{D_{C3}}$ (§3.1, §4.1) | **primary** |
| **C4′** | similarity-matched different-relation donor-centroid bridge | discrimination control (§5.1) |
| **C6** | random unit direction | procedure control |

**C2 [FACT]:** identical construction to EXP066/EXP077's positive control (`make_bridge_vec`:
$w=E[t]-E[f]$, normalized, $\alpha=0.50$); EXP077 observed +10pp rescue (56.67%→66.67%,
$p=0.03125$) [OBSERVATION]. If C2 fails to rescue on this run ($p\ge0.05$), the procedure is
invalid and any C3 null is **Inconclusive**, not a kill (T2, §8).

**C6:** $r \sim \mathcal{N}(0, I_d)$, $\hat{b}=r/\|r\|$, seed `SEED_C6=20260989`, $\alpha=0.50$.

**C5 (v1's permuted-label arm): DELETED** — see §5.2. The arm, its conjunct (v1-T5), and
`SEED_C5_PERM=20261067` are retired; no C5-referencing clause survives in this spec.

The sketch's naive C4 (different-relation donor, unmatched) is **REJECTED** — it confounds
relation with similarity: different-relation donors have a different token-similarity profile, so
C3 > C4 proves nothing about relation (LOG-144 §b.3.8). It is replaced by C4′. The sketch's C5
("random-target donor") was **REJECTED** in v1 — it destroyed both the relation channel and the
prior channel and therefore discriminated nothing; v1's permuted-label redefinition is now
deleted outright per §R0.1 (a prior-preserving control is vacuous, not merely weak).

### 5.1 C4′ — similarity-matched different-relation donor — (c).3 [C4′]

**Candidate pool (pinned):** 150 "is next to" support items — for each of the 5 support
vocabularies, the 15 `TRIPLES_INDICES` triples and 15 `QUADS_INDICES` quads with the neutral
template `Premise: {A} is next to {B}. {B} is next to {C}[. {C} is next to {D}.] Question: Who is
higher in rank, {q_opts}? Answer:` (the EXP078 `p_neu` construction, verbatim convention;
$(t_c, f_c) = (A, C)$ for triples, $(A, D)$ for quads). ids:
`ca_C4cand_{vk}_triple_{i}` / `ca_C4cand_{vk}_quad_{i}`.
[ASSUMPTION] A4: "is next to" carries no rank-order relational content (its program role is the
neutral contrast template, EXP078 §1). Different relation from C3's "outranks" by construction.

**Pinned greedy-matching algorithm (weights-only, $0 GPU):**

1. Compute C3's similarity profile $s_t^{C3}(j), s_f^{C3}(j)$ for $j=1..60$ (§4.3).
2. $B_0 = \emptyset$. At step $k \ge 1$: for each candidate $c \in P \setminus B_{k-1}$, form
   $B = B_{k-1} \cup \{c\}$, build its centroid by the §4.1 formula, compute its similarity
   profile $s_t^{B}(j), s_f^{B}(j)$, and the discrepancy
   $$D(B) = \tfrac{1}{60}\sum_{j=1}^{60}\Bigl(|s_t^{B}(j)-s_t^{C3}(j)| + |s_f^{B}(j)-s_f^{C3}(j)|\Bigr).$$
   Choose the $c$ minimizing $D$ (ties → lowest candidate index — deterministic, no seed needed).
3. Stop when $D(B_k) \le \delta$ or $|B_k| = 30$ (cap).
4. **Pinned tolerance:** $\delta = 0.05$ (mean absolute similarity-profile deviation).

**Achieved-match report [FACT — computed, LOG-174; attached]:** step 1 argmin over all 150
singletons = `ca_C4cand_V5_Modern_triple_1` ($(t,f)=$(Noah, Maya), "is next to" triple),
$D = 0.046564 \le 0.05$ ⇒ **stop at $|B|=1$**; the v1 §5.1 demotion fallback **did not fire**
and is **deleted** from v2 (the contingency is resolved; retaining it would be an unreachable
branch). $g(B) = 0.860981 \ge 0.25$ (**PASS**). Per-item deviations: $|s_t^B-s_t^{C3}|$
min/med/max/mean = 0.006682/0.026718/0.043542/0.024645; $|s_f^B-s_f^{C3}|$ =
0.005491/0.021975/0.069394/0.021919. The C4′ centroid is geometrically distinct from C3's —
unlike v1's C5, the paired C3-vs-C4′ McNemar carries information (T3 is not vacuous).

**Recorded fragility (binding disclosure, carried into the T3 reading):** the pinned rule
licenses a singleton bank (no minimum bank size was pinned). **7** of 150 singletons already
satisfied $D \le \delta$; the winner was decided by the lowest-candidate-index tie-break (a
duplicate-content twin of the winner exists in the pool). Achieved $D = 0.046564$ sits within
**7% of the δ boundary** ($0.046564/0.05 = 0.9313$). The T3 outcome is hostage to a
near-boundary tie-break among near-identical singletons — this is disclosed, not hidden.

**Pre-registered tie-break-robustness sensitivity battery (descriptive, NEVER deciding):**
the 6 non-winner singleton candidates with $D(\{c\}) \le \delta$ — a rule-defined set
(the executor enumerates the ids at build time by this rule, in ascending
candidate-index order; the spec pins the rule, not the ids; executor build
assert: exactly 6) — run as
**exploratory arms S1–S6** (60 items each; same $\alpha$, $l^*$, hook, decision rule; 360
forward passes, §10). For each Sk, report the T3-analog paired McNemar C3-vs-Sk
($b_k, c_k, p_k$) and *agreement* with the winner's T3 reading (agree iff
$(p_k<0.05 \land b_k>c_k)$ matches the winner's $(p<0.05 \land b>c)$ outcome).
**Pinned descriptive flag (not a verdict modifier):** de-duplicate the alternate set
by distinct $(t_d, f_d)$ content before counting (executor-computed; let $n_d$ = number
of distinct-content alternates) — duplicate-content twins agree with the winner's
T3 reading *by construction* and must not inflate the denominator. If fewer than a
$5/6$ fraction of the $n_d$ distinct-content alternates agree (agreement count
$< \lceil 5n_d/6 \rceil$), the T3 license line carries the pinned caveat "T3 reading is
tie-break-fragile (m/$n_d$ distinct-content alternates agree)" — reported, never
promoting or demoting the verdict.
The T3 conjunct decides on the pinned winner alone. No post-hoc promotion: a fragile T3 is
reported as fragile, never re-argued.

### 5.2 C5 — permuted-label donor: DELETED (the §R0.1 proof applied)

V1's §5.2 pinned a permuted-label bank (same 20 donor premises, targets permuted by a
fixed-point-free $\pi$, seed 20261067→20261069) and a [PROPOSITION] claiming "C5's centroid
**differs** from C3's only in which target tokens are paired with which donor premises" and
that "any C3-vs-C5 rescue gap is attributable to per-donor relational content."

**That proposition is FALSE as pinned and is struck.** By the §4.1 [THEOREM], the permuted
bank preserves the exact per-token $(n_t-n_f)$ and therefore has a centroid **identical** to
C3's — the audit computed cos = 0.9999999999999998, ‖S_C5−S_C3‖ = 0.000e+00 [FACT]. Donor
premises never enter $\hat{b}_D$ (unembedding-space construction); the "relational content"
the control was meant to destroy was never in the vector. V1's T5 (C5 does not rescue) was
therefore mutually exclusive with T1 by construction, v1's outcome (a) was logically
unreachable, and v1's §8 paired C3-vs-C5 refutation clause was a tautology (b=c=0, p=1.0 by
construction) — a kill-only machine, the same sin LOG-144 struck down, reversed.

**Resolution (LOG-176 requirement 1): deletion with proof.** No re-pairing, no different-entity
donor set, and no multiset-preserving permutation can produce a geometrically distinct
prior-preserving control under the pinned construction (§R0.1: the three desiderata are jointly
unsatisfiable in this family). The arm is deleted: v1's T5 conjunct is removed, all
C5-referencing §8 clauses are removed, and `SEED_C5_PERM=20261067` is **RETIRED**. C5's audit
values survive only as the evidence for the identity finding recorded here — never as license
values. The §13 permuted-bank follow-up idea is dropped as vacuous under the identity and
rebuilt as a different-algebra design (new number, Law #4).

## 6. Strata — (c).5 [STRATA]

**Split rule frozen before any forward pass (pinned):** median split on $s_t^{C3}(j)$ (C3's
target-similarity feature, §4.3) over the 60 test items, computed in Stage 0 from weights alone.
Low stratum: $s_t^{C3}(j) \le \mathrm{median}$ (ties → low); high stratum: $s_t^{C3}(j) >
\mathrm{median}$. **Computed outcome [FACT]: 49 low / 11 high** — an entity-group split
(low = {Mars, Venus, Iron}; high = {Gold, Silver, Jupiter}), not a per-item gradient. No
tertiles, no post-hoc re-cutting (Law #9).

**Decision endpoint:** within-stratum McNemar exact C3-vs-C1 (two-sided, $\alpha=0.05$).
Transfer requires the **low-similarity stratum to fire** (T4: $p<0.05$, $\Delta M>0$).
[INFERENCE]: leakage predicts rescue concentrates in the high stratum (rescue predicted by
$s_t(j)-s_f(j)$); transfer predicts rescue in the low stratum where similarity cannot explain it.
Feasibility gate §4.4 **passed** (49 low, 23 headroom ≥ 5).

**Binding license caveat (LOG-176 requirement 3):** a T4 license means transfer across **3
independent low-similarity target entities** ({Mars, Venus, Iron}) **at most** — the
stratifying feature has zero within-entity variation, so T4 is not a per-item gradient test.
This limitation appears in the T4 license language (§8), not just in an audit appendix.

## 7. Item-level model — (c).6 [MODEL]

**Pre-registered model.** Pooled item-level data over arms $a \in \{C3, C4'\}$ ($120$ rows):
$$\mathrm{rescue}_{j,a} = \mathbf{1}\{\text{C1 wrong on } j \;\&\; \text{arm } a \text{ correct on } j\},$$
$$\mathrm{logit}\,P(\mathrm{rescue}_{j,a}=1) \;=\; \beta_0 + \beta_1\cdot\mathrm{relmatch}_{j,a}
+ \beta_2\cdot s_t^{(a)}(j) + \beta_3\cdot s_f^{(a)}(j),$$
where $\mathrm{relmatch}_{j,a}=1$ iff $a=C3$ (same-relation donor) else $0$, and
$s_t^{(a)}(j), s_f^{(a)}(j)$ are the **arm-specific** similarity features (each arm's own
centroid). Fit: logistic regression (`statsmodels`), **item-clustered sandwich standard errors**
(60 clusters), two-sided Wald test. **T5:** $\beta_1 > 0$ **and** two-sided $p < 0.05$ with
$(s_t, s_f)$ covaried. [INFERENCE]: this is the precise "survives stratification" the sketch
gestured at — the relation-match indicator must carry weight *beyond* what token similarity
explains. (Renumbered: v1's T6.)

## 8. Decision tree — (c).7 [DECISION TREE]

All McNemar tests: exact two-sided via `scipy.stats.binomtest` on $(b,c)$ discordant pairs;
$b=c=0 \Rightarrow p=1.0$ (harness `compute_paired_stats`, EXP077 verbatim); $\alpha=0.05$.
$\Delta M = (b-c)/N$ (arm minus C1), reported in pp.

**Conjuncts (evaluated in order; T2 first — its failure overrides all other readings):**
- **T1:** C3 vs C1: $\Delta M > 0$, $p < 0.05$.
- **T2 (headroom gate, first):** C2 vs C1 rescues ($p < 0.05$). If $p \ge 0.05$ → procedure
  invalid → **Inconclusive** (any C3 null uninterpretable; no kill licensed).
- **T3:** C3 beats C4′ on paired decisions (McNemar on per-item C3-vs-C4′ outcomes, $b$ = C3
  correct & C4′ wrong): $p < 0.05$ with $b > c$. **T3 reading carries the pinned fragility
  (§5.1):** singleton C4′ bank, lowest-index tie-break among 7 δ-satisfying singletons,
  achieved $D$ within 7% of δ; the S1–S6 sensitivity battery reports the tie-break spread
  descriptively alongside.
- **T4:** low-similarity stratum fires: within-stratum McNemar C3-vs-C1 $p < 0.05$, $\Delta M > 0$.
  **License cap:** at most transfer across 3 low-similarity target entities (§6).
- **T5:** item-level model: $\beta_1 > 0$, two-sided Wald $p < 0.05$ with $(s_t, s_f)$ covaried
  (v1's T6, renumbered).

**[AFFIRMATION] — the theory role affirms the C5-less battery suffices (LOG-176 requirement 2).**
With no prior-control constructible in this family (§R0.1), discrimination rests on T3/T4/T5,
and each closes a distinct leakage channel: **T3** — the donor-relation-template channel
(C4′ differs from C3 in donor relation template with the similarity profile matched within
δ=0.05; a C3 win here says the donor *relation* matters); **T4** — the within-bank
similarity-gradient channel (rescue where the measured similarity channel is weakest);
**T5** — the per-item similarity-covariate channel (the relation-match indicator must carry
weight beyond arm-specific $s_t, s_f$). These are the three observable implications of
relation-mediated steering. The bank-prior channel cannot be independently lesioned in the
sum-of-differences family (identity theorem); this is recorded as a **known limitation of
the Level-1 license** — the license claims relation-mediated steering at the tested
configuration and cites the identity theorem as the reason no stronger prior-lesion exists
in this family — not as a hole in the battery.

| # | Outcome | Verdict on H_transfer |
|---|---|---|
| (a) | T2 holds; **T1–T5 ALL hold conjunctively** | **Supported** — transfer license, capped at evidentiary **Level 1**: "a same-relation donor-centroid bridge can improve inference on headroom items via relation-mediated steering at pythia-410m/$l^*$=20/$\alpha$=0.50 on this benchmark." T4's contribution is capped: transfer across at most 3 low-similarity target entities ({Mars, Venus, Iron}). T3's contribution carries the tie-break-fragility disclosure (§5.1). No Level 2/3 language (P1). |
| (b) | T2 holds; $\Delta M_{C3} \le 0$ ($p \ge 0.05$) — the sketch's kill | **Not supported**; **family-level kill licensed ONLY for unembedding-difference donor bridges at $l^*$=20 on this benchmark** — donor bridge is item-specific; the transfer hope for *this intervention family* is dead. Does NOT kill the oracle self-bridge family (C2 stands), hidden-state transfer (different family; EXP058's kill already covers its static form), or any other pre-registration. |
| (c) | T1 holds but **any of T3–T5 fails** | **Not supported** (leakage verdict). **Refuted** under this operationalization if additionally: C4′ rescues vs C1 ($p<0.05$) while T3 fails (C4′ ≈ C3 — different relation, same similarity, same rescue); **or** rescue is fully accounted for by $s_t(j)-s_f(j)$ with $\beta_1$ null. Any of these shows the donor bridge's causal power is *entirely* token-identity/similarity/prior steering. |
| (d) | T2 fails (C2 $p \ge 0.05$) | **Inconclusive** — procedure invalid; no verdict on H_transfer, no kill. Overrides (b) and (c). |

"Partial transfer" is not a verdict (LOG-148 verdict standard). If outcome (c) fires with
quantitative C4′ match to C3, the program's "best label-free capability candidate" slot
**vacates**: C-A is removed from Tier 1; C-B (self-bridge fixed point) becomes the lead
capability bet per the sprint's recommended sequence (LOG-144 §d). A leakage verdict is a
first-class **negative result** for the boundary paper's mechanism section (donor bridges rescue
via similarity/prior steering, not relational transfer — consistent with and strengthening audit
Finding 4 and G1), publishable as boundary science, not as a capability.

**Reachability of terminals (LOG-176 requirement 4 — proved, not asserted).** Every terminal
outcome below is logically reachable; no branch is vacuous, tautological, or mutually exclusive
by construction:
- **(a) Supported — reachable.** T1∧T2∧T3∧T4∧T5 are mutually compatible: no pinned identity
  constrains them jointly. C4′'s centroid is geometrically distinct from C3's (D=0.0466>0), so
  paired C3-vs-C4′ decisions can differ in either direction; the low stratum (49 items, 23
  headroom) is a fixed non-empty set on which C3-vs-C1 McNemar can independently fire; β1 can
  be positive while $(s_t,s_f)$ vary. Witness world: relation-mediated steering. — *Contrast
  with v1, where T1∧(v1-T5) was algebraically impossible and outcome (a) was unreachable.*
- **(b) Not supported (kill) — reachable.** T2 holds with C3 null: witness = EXP077's
  static-variant world (all static geometric variants ΔM=0, p=1.0) with the C2 positive control
  rescuing (+10pp, p=0.03125) — an empirically observed configuration.
- **(c) Not supported / Refuted — reachable.** T1 holds with T3 failing: witness = the H_leak
  world the design is built to catch (C4′, different relation but similarity-matched, rescues
  the same items). T1 holds with T4 failing: rescue concentrated in the high stratum. T1 holds
  with T5 failing: rescue fully explained by $s_t-s_f$, β1 null. Each is a coherent
  data-generating world.
- **(d) Inconclusive — reachable.** T2 fails: witness = a procedure-invalid world (C2 does not
  rescue on this run — empirically possible; precedence pinned: T2 is evaluated first and its
  failure overrides (b)/(c)).
- **No kill-only machine:** (a) can fire, so the design licenses as well as kills — the v1
  defect (unreachable positive branch) is repaired. **No tautological refutation clause
  survives:** v1's paired C3-vs-C5 clause (b=c=0, p=1.0 by construction) is deleted with the arm.

### LICENSES (binding; Law #4/#11)

> "A C3 win that fails any of T3–T5 is not transfer; it is similarity/prior steering consistent with audit Finding 4."

(verbatim LOG-144 §b.6.16 sentence, with the conjunct range renumbered v1-T3–T6 → v2-T3–T5 per
§R0; otherwise byte-identical.) The license side is written with equal force to the kill side:
the sketch's one-sided kill criterion (null kills, win auto-licenses) is replaced by the
conjunctive T1–T5 license above. A C3 win licenses **at most** Level 1; it never licenses claims
about hidden-state transfer, other models/layers/$\alpha$, or adaptive-loop efficacy.

## 9. Endpoints and guards — (c).8 [ENDPOINTS]

- **Decision endpoints: McNemar exact only** (per-arm vs C1; paired C3-vs-C4′; within-stratum
  C3-vs-C1; T3-analog paired C3-vs-Sk for the exploratory sensitivity battery, descriptive only).
  No margins, no Wilcoxon, no KL, no cosine-deltas as decision endpoints — anywhere (Law #9;
  audit Finding 3: the B_wrong $p=1.2\times10^{-8}$ with $b=c=0$ invalidated margins).
- **C2-headroom gate** (T2, §8): procedure validity precedes all verdicts.
- **Evidentiary level capped at Level 1** ("can improve inference"). No Level 2 ("changes
  computational strategy") or Level 3 ("creates qualitatively new capability") language (P1).
- KL divergence is an **exploratory guardrail only** (mean KL < 0.50, EXP077 precedent) —
  reported, never deciding.
- F1 injection-norm guard (all static injection vectors norm > 0, verbatim EXP077) and F2
  single-token guard (§2) are pre-registered build asserts, not endpoints.

## 10. Budget, seeds, guards, and provenance — (c).9 [HYGIENE]

**Forward-pass budget recomputed from first principles [FACT — arithmetic]:** 5 deciding arms
(C1, C2, C3, C4′, C6) × 60 items × 1 forward pass per item-arm = **300 forward passes** (the
LOG-176 ruling's recomputed figure). Pre-registered exploratory sensitivity battery: 6 arms
(S1–S6) × 60 = **360 passes**. **Total: 660 forward passes.** All intervention vectors are
weight-computed (centroids from $W_U$; C2 per-item bridges from $W_U$; C6 from a seeded RNG) —
vector construction costs **zero** forward passes. The sprint's "2,700 passes" does not follow
from the arm structure and is **superseded** by this number (LOG-144 §b.6.15). Stage 0
(weight-only audit, §4.3) costs 0 GPU passes. Estimated GPU time: ~40–60 s on 2×T4
(EXP077's comparable battery: 1,740 passes ≈ 2 min ⇒ 660 passes ≈ 45 s [ESTIMATE]).

**Pinned:** `SEED_TORCH=SEED_NUMPY=20260923` (EXP078 precedent); `SEED_C6=20260989` (random
direction); `SEED_PERMNULL=20261123` (similarity-audit null); C4′ greedy matching deterministic
(tie-break: lowest candidate index); S1–S6 set rule-defined (no RNG).
`SEED_C5_PERM=20261067` is **RETIRED** with the C5 arm (§5.2).
$\alpha=0.50$, $l^*=20$, hook = last-token residual stream at layer-20 output (§2).

**SHA-256 $\Delta\theta=0$ guards (Law #6/#13):** `get_hash` verbatim from the EXP077 harness
(SHA-256 over concatenated `state_dict()` tensors, sorted keys, CPU float32 bytes) computed
pre-run and post-run; mismatch → FATAL, run void. Attached audit tri-match [FACT — computed]:
pre = post = archived (G1) = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
⇒ $\Delta\theta=0$. No weights, biases, adapters, or normalization statistics are updated at
any point.

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
  (hence the T3–T5 discrimination battery). EXP078's halt does not pre-empt C-A; it motivates it.
- **EXP077** (executed 2026-09-23): all static geometric variants null ($\Delta M=0$, $p=1.0$);
  the output-bridge positive control rescued +10pp (56.67%→66.67%, $p=0.03125$) [OBSERVATION] —
  provenance of the C2 configuration reused here.

**Novelty: N1 retained** (Known combination — `research/README_LITERATURE.md` §N1; Law #10). The
operator is equivalent to static steering-vector application (CAA, Rimsky et al.); the delta is
the *confound-aware transfer design* (similarity-matched C4′, conjunctive T1–T5 license with the
identity-theorem prior analysis), which the September-2026 literature sweep found no prior art
for as a combined discrimination battery.

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
**computed and attached** (Stage 0, CPU, before signature). Adapted to the v2 arm structure
(LOG-176); every item re-verified present and pinned:

1. [DONORS] §3: exact 20-donor list, "outranks" template, premise-disjointness proof, $(t_d,f_d)$
   histogram, Law #7 statement. ☐
2. [CENTROID] §4.1–4.2: pinned sum-of-differences formula **plus the identity [THEOREM]**;
   degeneracy floor 0.25 with computed $g(D)$ for C3 (1.061783) and C4′ (0.860981) attached;
   §4.5 recomputation rule. ☐
3. [C4′] §5.1: greedy-matching algorithm, $\delta=0.05$, achieved-match report attached
   (D=0.046564, singleton `ca_C4cand_V5_Modern_triple_1`), **singleton fragility disclosed**,
   **tie-break-robustness sensitivity battery S1–S6 pinned** (6 exploratory arms, descriptive
   flag, never deciding). The v1 demotion fallback is deleted as resolved — no unreachable
   branch retained. ☐
4. [C5-RETIREMENT] §5.2 + §R0.1: C5 arm deleted with proof (identity theorem; the three
   desiderata jointly unsatisfiable); the false v1 §5.2 [PROPOSITION] struck; v1-T5 conjunct
   removed; `SEED_C5_PERM` retired; no C5-referencing clause survives anywhere in the spec. ☐
5. [STRATA] §6: median-split rule frozen pre-forward-pass; computed 49/11 entity-group split
   attached; low-stratum feasibility (23 headroom ≥ 5) computed and attached; the "~30/30"
   aside deleted; the 3-entity license caveat in the T4 language. ☐
6. [MODEL] §7: logistic spec, arm-specific $(s_t,s_f)$, item-clustered SEs, T5 criterion
   (renumbered from v1-T6). ☐
7. [DECISION TREE] §8: outcomes (a)–(d), T1–T5 conjunctive, verdicts from the permitted set
   only, anti-creep sentence verbatim in LICENSES (range renumbered per §R0), theory-role
   [AFFIRMATION] of the C5-less battery, **reachability proved for every terminal**. ☐
8. [ENDPOINTS] §9: McNemar exact only; C2-headroom gate; Level-1 cap. ☐
9. [HYGIENE] §10: **660-pass budget recomputed** (300 deciding + 360 exploratory);
   seeds/$\alpha$/$l^*$/hook pinned (C5 seed retired); SHA-256 guards with attached tri-match;
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
toward C3's; the T3 contrast relies on the residual difference inside the $\delta=0.05$ envelope,
and the achieved match is a singleton within 7% of δ — the S1–S6 sensitivity battery (§5.1) is
the pre-registered answer to exactly this risk.

**One challenge (§2 obligation):** the strongest attack on the C5-less design is that the
bank-level prior channel is never independently lesioned — T4/T5 hold *similarity* (the prior's
observable channel) at bay and T3 varies the donor relation template, but a skeptic can argue
the T1–T5 conjunction remains consistent with a prior-steering mechanism operating through an
unmeasured channel (e.g., foil-side or interaction effects the $s_t/s_f$ features miss). The
spec's pre-registered answer: T5's model includes arm-specific $s_t$ *and* $s_f$; T4 tests
rescue where the measured similarity channel is weakest; T3 shows the donor *relation template*
matters with similarity matched — and the identity theorem (§4.1) is cited as the reason no
stronger prior-lesion exists in this family, recorded as a known limitation of the Level-1
license rather than a hole in the battery. If the reviewer wants the prior channel lesioned
directly, that is a different construction algebra — the idea below — not a patch to this design.

**One idea (§2 obligation):** the v1 *permuted-bank null family* is **dropped as vacuous**
under the §4.1 identity — every permuted bank has the identical centroid, so the "exact
permutation test on ΔM" is a point mass at C3's own ΔM with zero variance by construction.
**Rebuilt version (new number, Law #4 — not in this design):** a permuted-bank null under a
*different centroid construction* (per-donor-normalize-then-average), where permuting
target–premise pairings changes the per-donor unit vectors and hence the centroid — there,
$k$ permuted banks as full arms give a genuine exact permutation test of whether C3's ΔM is an
outlier of the permuted-bank rescue distribution. Kill = C3's ΔM inside the permuted null.
Cost: $k \times 60$ passes. The identity theorem is what makes the construction change
necessary; the idea is recorded here so the program does not re-discover the vacuous version.

## 14. Change protocol

Any change to donors, templates, formulas, gates, tolerances, seeds, $\alpha$, $l^*$, hook,
endpoints, strata, model, sensitivity battery, or decision tree after signing = a **new
experiment number** (Law #4). Corrections to this DRAFT are proposed to the reviewer, never
applied silently. This v2 is a draft revision of the unsigned LOG-150 line: it consumes no
number, and Law #4 binds at signing — at which point the number mints from the then-next-free
pool (currently EXP081, to be re-verified unminted at signing time).
