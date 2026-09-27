# S4-9 — Law #15 Worth-It Gate Analysis

*Innovation agent, 2026-09-27. **ON PAPER ONLY** — no compute, no model runs,
no weights touched, no signed protocols/artifacts modified, no experiment number
minted. **No pilot is authorized here:** a full fresh pre-registration chain plus
Law #14 review is required before any run (see §8).*

**Candidate:** S4-9 — per-item (not shared) layer-11 task-direction causal test
(EXP094+ material).

**Lineage:** born at the Friday cull 2026-09-25 (LOG-4353) from EXP093's death-debt
(LOG-219 rule: every null or kill produces ≥1 new falsifiable candidate — logged
before the workstream closes). The deaths table records the debt as
**PAID** (S4-9 drafted LOG-4353); this packet is the Law-#15 material that the
backlog row requires before any pre-registration draft is commissioned.

**Backlog source row:** `research/innovation/CANDIDATE_BACKLOG.md`, S4-9:
"EXP093 killed the *shared* layer-11 direction; does a *per-item*
(item-specific) task direction move decisions?" — status PROPOSAL.

---

## 1. The precise question [HYPOTHESIS]

EXP093 (binding KILL UPHELD, LOG-4352) showed that static injection of the
**shared** layer-11 task direction on EXP092-B moves zero decisions:
aggregate/A-first/C-first accuracy identical across B/P/N arms (0.6000/0.9667/0.2333),
Δ = 0.0000, McNemar b = c = 0 → p = 1.0 in all six tests (P-vs-B and N-vs-B × 3
strata), with the perturbation verified real (perturbation_ratio = 0.0474, ~4.7%
of residual norm, reached the logits — mean margins shifted +0.0059 P / −0.0076 N —
yet flipped nothing: causal inertness, not measurement failure). The licensed claim
is scoped: it falsifies *"≥10pp causal transfer via a shared static direction at
layer 11"* only.

**The question:** does an *item-specific* (per-item) task direction move
decisions on the same bench, where the shared direction moved none?

Per item *i*, construct a task direction d_i(x_i) from that item's own geometry
(contrast direction local to the item, e.g. a within-item task contrast at L11),
and inject it at matched norm to the EXP093 perturbation (4.7% of residual norm).
Then:

**Primary contrast:** ΔM_task-per-item vs ΔM_shared (EXP093 baseline ≈ 0.0000).
**Specificity contrast:** ΔM_task-per-item vs ΔM_random-per-item (a norm-matched
per-item *random* direction control — the Law-#13-style specificity arm that
EXP093 lacked).

---

## 2. The decision it changes

All three outcomes pre-registered; exactly one row of this table will be earned.

| Outcome | Condition | Effect |
|---|---|---|
| **KILL** (directional family at L11) | Shared-vs-per-item contrast: ΔM_task-per-item ≤ ΔM_shared (both ≈ 0) | The causal inertness is **not** a sharedness artifact. The licensed claim expands: static L11 task directions — shared *or* per-item — do not move decisions. The L11 directional family is dead; hunt moves to gated/dynamic or multi-layer mechanisms (EXP094+ material in those families). |
| **KILL** (specificity) | Random-per-item matches task-per-item: ΔM_random-per-item ≈ ΔM_task-per-item | A per-item "rescue" that a random per-item nudge reproduces is a **nonspecific perturbation effect**, not task-geometry steering. KILL — no causal license for per-item task geometry. |
| **CONTINUE** (licensed positive only) | ΔM_task-per-item > random-per-item control **and** clears the pre-registered causal bar (see §4), with pre-registered N-vs-B routing and stratum breakdown in the CONTINUE claim | Per-item geometry carries causal content the shared direction lacked. Earns a full experiment license (EXP094+): the first causal-steering license at a non-readout layer. |
| **PIVOT** | Per-item directions show item-heterogeneous movement that is direction-specific but sign-inconsistent (flips in both directions, stratum-dependent) | PIVOT to a **conditional** design: per-item steering is conditional on a pre-registered per-item covariate (e.g. baseline margin, coherence, layer-specific norm). A global per-item-direction claim is dead; a conditional one is EXP095 material. |

**What rides on it:** whether the EXP093 kill was a *sharedness* artifact or a
*location* verdict. The belief it tests (named at the Friday cull, LOG-4353):
**"the EXP093 kill was about sharedness, not location."** [INTERPRETATION]

**What it does NOT change (scope fence):** the EXP093 KILL itself is untouched
(shared direction stays dead); gated/dynamic mechanisms and multi-layer
compositions remain separate EXP094+ material regardless of outcome.

---

## 3. Cheapest falsifying test and cost

**Design (3 arms × 60 items ≈ 180–240 passes, CPU):**

- **Arm B (baseline):** no injection, Δθ = 0 — anchors the EXP092-B bench.
- **Arm T (per-item task direction):** item-specific direction d_i injected at the
  EXP093 norm (4.7% of residual norm), exact-delivery probe (G5-style) retained.
- **Arm R (random per-item control):** norm-matched random per-item direction —
  the specificity arm. Task-free by construction.

**Pre-registered guards (hardened before any pilot — the EXP090 lesson):**
- **G7 (Law #7):** per-item directions must be constructed **label-free** — from
  within-item contrasts that expose no test labels, targets, or future instances
  to the direction generator. A label-informed per-item direction is a
  disqualification, not a positive.
- **Per-item margin CSV (Law #13 repair):** LOG-4352's non-blocking observation
  recorded the Law-#13 gap — per-item margins were not persisted in EXP093
  (aggregates only). This bundle writes per-item, per-arm margins to disk.
  Non-negotiable.
- **N-vs-B routing:** the primary licensed contrast (per-item-task vs baseline)
  carries a pre-registered arm-routing rule — which items enter the contrast and
  under what allocation rule — fixed before inspection. No post-hoc re-routing.
- **Stratum breakdown in the CONTINUE claim:** a CONTINUE verdict requires the
  stratum-level table (aggregate / A-first / C-first, as in EXP093's six tests);
  a claim that survives only in aggregate is underlicensed and routes to PIVOT.
- **N_final feasibility computation** as a standing pre-reg gate (EXP079 lesson).

**Cost:** ≈180–240 passes, **CPU, <0.005 T4-h** — $0 cost (from the backlog row).
No GPU. This is the cheapest decision-changeable test in the current queue for the
shared-vs-per-item question.

---

## 4. Mathematical license

**License:** [THEOREM-adjacent linear-algebra fact] In the 512-dimensional
residual space at L11, the shared direction d̄ is one fixed vector. A per-item
decision function f_i(v) depends on the full injected vector, not just its
projection on d̄. EXP093 falsified E_i[f_i(d̄)] > bar — a one-dimensional
statement. The per-item test asks a strictly broader question: does there exist
a *family* of item-indexed directions {d_i} with E_i[f_i(d_i)] > bar beyond a
random-direction control?

**Quantitative prediction (pre-registered, bars):**
- ΔM_task-per-item > 0.10 (DELTA_BAR = 0.10, the EXP093-licensed bar) **and**
  ΔM_task-per-item > ΔM_random-per-item with McNemar p < 0.05 on the T-vs-R
  flip table (b_T-vs-R vs c_T-vs-R).
- The **specificity gap is non-negotiable**: it is the signature no alternative
  predicts — a nonspecific perturbation effect predicts ΔM_T ≈ ΔM_R; only
  task-geometry steering predicts ΔM_T > ΔM_R.

**Breaking point (sharp):**
- ΔM_task-per-item ≤ 0.10 with ΔM_R within sampling noise of ΔM_T → the
  per-item family is dead **KILL** — the inertness is about location, not
  sharedness; EXP093's licensed claim expands to all static L11 task directions.
- If per-item norm variance across items is degenerate (all d_i ≈ collinear),
  the test is powerless → **Underdetermined** (never KILL on a powerless test —
  the R4-licensed rule).

**Honest audit of the license (adversarial pass):**
- *Gap 1 — construction degrees of freedom.* A "per-item task direction" is a
  design choice, not a God-given object; the constructor could smuggle
  label information or engineer the positive (Law #7 hazard). Mitigation is
  structural: the G7 label-free guard is a **disqualification bar**, and the
  random-direction control prices out construction cleverness — any constructor
  clever enough to help the task arm helps the random arm equally. [CONJECTURE]
  Mitigation noted: the control carries the audit, not the constructor.
- *Gap 2 — one bench.* EXP092-B is a single relational bench; a per-item
  positive licenses steering on *this* bench, not a general steering primitive.
  Mitigation: the CONTINUE claim is bench-scoped by pre-registration; a
  general claim is EXP095+ material.
- *Gap 3 — power.* n = 60 with Δ̄ = 0.10 detects ≈6 flips; the specificity
  contrast T-vs-R needs enough per-item movement on *either* arm. Hardening:
  the pre-reg gates on observed movement (b+c) before interpreting the
  specificity table; movement ≈ 0 → the contrast is KILL-not-Underdetermined
  only if T and R both sit at zero with the perturbation proven delivered
  (EXP093 proved delivery is provable — perturbation_ratio, G5).

**License verdict:** HOLDS for a *test*, not a conclusion. The mathematics is a
straight dimensionality argument (one shared vector vs an item-indexed family),
the prediction is quantitative with a sharp breaking point, and both nearest
alternatives (sharedness-irrelevant inertness; nonspecific perturbation) are
priced into the decision table. The license licenses the experiment, not the
positive.

---

## 5. Death-debt linkage

This candidate **pays EXP093's death-debt**. LOG-4353 (Friday cull, 2026-09-25):
EXP093's kill produced S4-9 under the LOG-219 rule ("every null or kill produces
≥1 new falsifiable candidate — logged before the workstream closes"); the deaths
table records the debt as **PAID** (S4-9 drafted). This packet is the Law-#15
material the backlog row requires ("requires ... full fresh pre-reg chain +
Law #14 review before any run"); the debt is *fully discharged* when the
pre-registration is drafted, Law-#14-reviewed, and signed — this packet is the
licensed step before it.

---

## 6. Summit filter

Does it move a frozen model toward **causal steering**? **Yes — as mechanism
science, and summit-directly relevant.**

A licensed positive would be the program's first causal-steering license at a
non-readout layer: item-specific frozen geometry that *moves decisions* beyond a
random control is a usable per-item steering channel. That is precisely the
primitive an autonomous steering loop (the summit: frozen models that steer
themselves) must build on — you cannot have autonomous per-item steering without
first knowing that per-item geometry is a causal channel at all. EXP093 proved
the shared channel is dead; S4-9 asks whether the per-item channel exists.

Honest caveat: the test as specified is *externally* applied injection — the
per-item direction is computed by us, not by the model. It is not itself the
autonomy result and must never be described as such. The summit-directional
extension is explicit and named: the model *self-computes* its per-item steering
direction (closed self-steering loop — summit-phase material). Verdict: GO as
Phase-3 mechanism science with a named autonomous extension.

---

## 7. Graveyard filter

- **Static cones/geometry (EXP077, killed (a)):** a per-item direction is still a
  static injection — but EXP093's *licensed claim explicitly reserves* per-item
  directions as EXP094+ material. Not pre-killed. CLEAR.
- **EXP091 zero-shot scoring:** no readout/scoring claim. CLEAR.
- **QK null-space (G1):** no weight-subspace energy story; injection-side,
  runtime-only. CLEAR.
- **Label-informed "wins" (bridge demotion, LOG-204):** the G7 label-free
  constructor guard is a disqualification bar — a label-informed per-item
  positive earns nothing. Law #7 clean by construction. CLEAR.
- **SAH (S3-4) / S3-8 downstream amplification:** distinct objects (intervention
  α-control; L1-vs-downstream decomposition). No overlap. CLEAR.
- **EXP085 k=2 collapse:** not a rank/suppression construct. CLEAR.

---

## 8. Pilot authorization — EXPLICIT

**No pilot is authorized by this packet.** The backlog row already requires, and
this packet re-affirms: before any run, S4-9 needs (1) a **full fresh
pre-registration chain** — new construct, arm-routing rule, N-vs-B contrast,
stratum-breakdown requirement, per-item margin CSV (Law #13), G7 label-free
constructor guard, N_final feasibility computation (EXP079 lesson) —
**not a revival or an edit of EXP093's signed protocol**; and (2) **Law #14
review + SIGN** of that pre-registration; and (3) CEO execution clearance.
This packet is the Law-#15 worth-it material only.

---

## Verdict: GO as EXP094+ material (gate passed; pilot NOT authorized)

S4-9 passes the Law-#15 gate: a precise question born from a recorded death-debt,
a decision table with teeth (two distinct KILL paths, a PIVOT branch, and a
licensed CONTINUE with stratum discipline), the cheapest falsifier in the queue
for this question (≈180–240 passes, CPU, <0.005 T4-h, $0), a dimensionality-anchored
license with a quantitative prediction and a sharp breaking point, summit relevance
as the per-item steering primitive, and clearance of the entire graveyard.

Open item carried to the Law #14 lane: the per-item direction constructor's
label-free audit (G7) and the arm-routing rule are the two highest-risk pre-reg
components — Law #14 should stress-test both before signing anything.
