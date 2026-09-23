# EXP080 Protocol Specification: Oracle-Selection Ceiling over the Output-Side Candidate Pool (Phase A only)

**Status:** PRE-REGISTERED — signed by the CEO (Research Lead) under LOG-172, 2026-09-23,
on the LOG-171 Law #14 re-review SIGN (`reports/adversarial_review_g2_prereg_r2_2026-09-23.md`).
**Revision record:** LOG-167 revision (2026-09-23) — addresses the LOG-152 REVISE
verdict (blockers B1–B4, minors m1–m7); LOG-171 re-review returned **SIGN**.
**Date:** 2026-09-23
**Author role:** Pre-registration Drafter (LOG-143 dispatch)
**Numbering:** **EXP080**, minted at CEO signing (next free number; Law #4). Any changed
design after signing takes the next free number at pre-registration time (Law #4).
**Phase:** A only. Phase B (target-free evaluator build) is NOT pre-registered here.
**Predecessors:** EXP065/066 (boundary series), EXP070 (hidden-state oracle ceiling —
returned UNINFORMATIVE_PROBE, ceiling unmeasured not zero), EXP077 (cone-vs-line;
output bridge rescues +10pp GPU / +23.33pp smoke), EXP078 (subspace localization;
HALT_ENERGY — bridge power mostly outside the tested concept subspace), G1 (QK-subspace
audit — KILL, LOG-134).
**Source idea:** `research/innovation/SPRINT2_2026-09-23.md` §G2 (Experiment agent,
Class 3 Phase A; [CONJECTURE] awaiting this pre-registration).
**Governing standards:** `AGENTS.md` (14 Inviolable Laws; §5 10-label standard),
`research/MATH_STANDARDS_CHARTER.md` (M5.2/M5.3/M5.4 binding on this tree),
`experiments/protocols/STATISTICAL_PROTOCOL_V02.md`,
`research/CHATGPT_MENTORSHIP_DIRECTIVE.md` (evidentiary levels; verdict standard),
`research/literature/audit_2026-09-23.md` (N1 verdict stands; this spec moves no tier).

---

## 0. Reading record (knowledge-protocol compliance)

Per `research/TEAM_KNOWLEDGE_PROTOCOL.md` §1, the drafter read before writing:
`AGENTS.md` (14 laws, §5 10-label standard); `research/innovation/SPRINT2_2026-09-23.md`
(§G2, the kill list, sequencing); `research/analysis_plans/G1_REPORT_2026-09-23.md`
(full); `experiments/protocols/EXP070_ORACLE_CEILING_PREREG_SPEC.md` (full — the
methodological template); `research/MATH_STANDARDS_CHARTER.md` (M5.2/M5.3/M5.4);
`reports/research_log.md` (LOG-134 G1 kill, LOG-138 EXP079 closure and the
probe-feasibility-algebra discipline, EXP070 history, EXP077/078 outcomes);
`experiments/runs/exp078/run_exp078.py` (`make_bridge_vec` code path — the bridge
definition is grounded in the verbatim archived implementation, not in prose).

**Epistemic convention used throughout:** every load-bearing claim carries BOTH layers —
the canonical layer (**FACT / INFERENCE / HYPOTHESIS / SPECULATION**, mentorship
directive) and the repo 10-label (`AGENTS.md` §5) — e.g. **[FACT]/[OBSERVATION]**.
Unlabeled assertions are to be read as [CONJECTURE]/SPECULATION.

**Revision compliance (LOG-167):** the reviser independently verified B1 against
`experiments/runs/exp078/run_exp078.py` (the halt path at L330–349/L555 precedes
the `torch.save` at L750; no `exp078_vectors.pt` exists in `~/workspace`) and
implemented the full LOG-152 fix list (B1–B4, m1–m7) in this draft. Banner
advanced to **PRE-REGISTERED** at CEO signing (LOG-172) on the LOG-171 re-review
SIGN; experiment number **EXP080** minted.

**Evidentiary level of this experiment:** level 1 — *"can improve inference"*
(decision accuracy on a fixed benchmark). Nothing in this protocol licenses claims at
level 2 (*"changes computational strategy"*) or level 3 (*"creates qualitatively new
capability"*). All conclusions state this level explicitly.

---

## 1. Research question and hypotheses

$$\boxed{\textbf{Over the output-side candidate pool } \mathcal{P} \textbf{ — where G1 and
EXP077/078 locate the causal channel — does \textit{any} label-informed per-instance
selection beat static injection?}}$$

**[HYPOTHESIS]/[HYPOTHESIS] H_ceiling-G2:** Label-informed per-instance oracle selection
over the output-side pool $\mathcal{P}$ (§3) yields $\Delta M_{\mathrm{oracle}} >
\Delta M_{\mathrm{static}}$ with McNemar exact two-sided $p < 0.05$ on the paired
(oracle, static) decisions over the same items — i.e., a per-instance selection prize
exists in the output room.

**[HYPOTHESIS]/[HYPOTHESIS] Null $H_0$:** $\Delta M_{\mathrm{oracle}} \le
\Delta M_{\mathrm{static}}$ or $p \ge 0.05$ — even the generous oracle (§4.3) cannot
beat static injection over this pool.

**The kill criterion is the falsifier.** The pre-registered falsification criterion for
$H_{\mathrm{ceiling\text{-}G2}}$ is: **C3-vs-C2 McNemar $p \ge 0.05$** (branch (c), §9).
If it fires, the verdict is **Not supported** — and per §11 the output-side evaluator
program is stood down. Under Lemma L1 (§4.5: $c = 0$ by construction), the
falsification criterion reduces to $b \le 5$; §9(c) carries the
bridge-replication contingency. No silent hypothesis shift is permitted afterward (Law #4):
a non-significant positive (e.g. $(b=5,c=0)$: $+8.3$pp, $p=0.0625$) does not become
"a trend worth chasing" — the m7 precedent (EXP070 re-review) is adopted verbatim:
the kill trigger is widened to $p \ge 0.05$ precisely so the
positive-but-nonsignificant cell has a branch.

### 1.1 Scope (methodology pre-test, not a method)

**[INFERENCE]/[INTERPRETATION]** G2 is a **kill-the-evaluator-program pre-test**, not a
proposed method and not a novelty experiment. It applies EXP070's verifier-first
methodology where the causal channel actually lives: G1 killed the QK-subspace
mechanism (LOG-134); EXP077 showed no static geometric variant of the concept
direction moves accuracy while the output bridge rescues; EXP078 localized the
bridge's power mostly outside the tested concept subspace. Every evaluator-shaped
idea (any $\mathcal{E}$ in output space) is worthless if the oracle ceiling over the
output room is zero. G2 is the gate for ALL evaluator-shaped work (sprint §G2).

The oracle's label access is **permitted**: this is a ceiling *measurement*, not a
proposed method. Law #7's test-time information boundary applies to any future
evaluator, not to this diagnostic. The anti-cheat clause (§4.4) keeps the ceiling honest.

### 1.2 Asymmetry (inherited from EXP070, restated)

An oracle **loss** (branch (c)) stands the program down; an oracle **win** merely
licenses Phase B *behind a new pre-registration and EXP068 reconciliation* — it does
not validate any evaluator. The ceiling is an upper bound on selection gain: a
realizable target-free selector over the same pool cannot *systematically* beat the
label-informed oracle in expectation (a lucky single realization may match it).
This asymmetry is the entire methodological point.

---

## 2. Frozen model and SHA-256 guard

- **Model / tokenizer (in-scope):** `EleutherAI/pythia-410m` — the model on which the
  output-side effects were measured (EXP066 bridge, EXP077, EXP078).
- **Architecture [FACT]:** GPT-NeoX; 160,326,400 params (410m class); $d = 1024$;
  24 layers; 16 attention heads; head dim $d_h = 64$; rotary embeddings; parallel
  attention/MLP; untied output embeddings.
- **Target layer:** $l^* = 20$ (83% depth, matching EXP077/078). Intervention
  $h \leftarrow h + \alpha u$ via forward hook at $l^*$, last-token position.
- **Intervention strength:** $\alpha = 0.50$ **fixed** for all conditions (program
  continuity with EXP065–078; no tuning — this is a cheap pre-test, and tuning
  $\alpha$ would spend the budget this experiment exists to save).
- **Expected SHA-256:** `[TO BE REGISTERED at first execution — computed in the
  execution environment]` (same convention as EXP067/070 §2; no GPU/torch on the
  drafting machine).
- **Guard procedure [FACT-level requirement]:** SHA-256 over the concatenation of
  `state_dict()` tensors (sorted keys, CPU, float32 bytes) computed before the
  oracle-selection phase and after the test phase. The **binding** guard is the
  runtime pre/post match; a registered value, once recorded, is a sanity check only.
  $\boxed{\Delta\theta \equiv 0}$ is non-negotiable (Law #6). No backward pass exists
  anywhere in this protocol.
- **Sanity-value caution [FACT]/[OBSERVATION]** (m6): the registered EXP067 sanity
  value `4c242d9a…` was computed over **unsorted** state-dict keys (LOG-123
  root-cause), despite "sorted keys" text in EXP067 §2. This protocol pins sorted
  keys (verbatim `get_hash` from the EXP078 runner, which sorts). The EXP067
  sanity value **must not be compared** against this protocol's sorted-keys
  computation at execution — a mismatch is expected and non-binding. The binding
  guard is the runtime pre/post match.

---

## 3. Candidate pool $\mathcal{P}$ [DEFINITION]

The pool is the **static, pre-computable union of the output-side candidate family**,
fixed before any test item is touched. $|\mathcal{P}| = 10$ unit directions per item.

**[FACT]/[OBSERVATION]** — the arithmetic this pool size grounds: 10 candidates
$\times$ 60 items $=$ 600 oracle-evaluation forward passes (§10).

### 3.1 Pool members (exact construction, pinned seeds)

For each test item $x$ with target token id $t_x$ and foil token id $f_x$ (the
benchmark exposes both; §6):

1. **Self-bridge $b(x)$ — oracle, label-informed.** The verbatim EXP066/078 code path:
   $$b(x) = \mathrm{normalize}(W_U[t_x] - W_U[f_x]), \qquad
     W_U = \texttt{model.get\_output\_embeddings().weight}$$
   (the LOG-114 mechanical fix — `get_output_embeddings()` — is the registered
   accessor; the historical `embed_out` attribute name is stale under
   transformers 5.x). Weight-only; 0 forward passes. This is the EXP077 positive
   control direction, now also pool member #1.
2.–8. **Top1−topk pseudo-bridges $u_k(x)$, $k = 2..8$ — target-free (7 candidates).**
   From the C1 (unintervened) logits on $x$ at the last-token position, take the
   top-$k$ argmax token ids $y_{(1)}, \dots, y_{(k)}$ (deterministic; no seed needed):
   $$u_k(x) = \mathrm{normalize}\!\left(W_U[y_{(1)}] -
     \frac{1}{k-1}\sum_{j=2}^{k} W_U[y_{(j)}]\right).$$
   **[INFERENCE]/[INTERPRETATION]:** these are the label-free output-side analog of
   "what the model itself almost said" — per-item, constructed from C1's own
   distribution, requiring no extra forward passes beyond C1 (whose logits are
   reused). They are the only pool members a future target-free evaluator could
   plausibly construct; their presence is what makes the ceiling informative about
   the evaluator program rather than about the bridge alone.
9. **$P_S$-residue $p(x)$ — oracle-sense, label-informed.**
   $$p(x) = \mathrm{normalize}(P_S\, b(x)), \qquad P_S = Q_S Q_S^\top,$$
   where $Q_S$ is **rebuilt in-protocol in Phase 0** (§3.1a) — there is no
   archived EXP078 artifact to load. **[FACT]/[OBSERVATION]** (B1, verified by
   LOG-167 inspection of `run_exp078.py`): the EXP078 runner exits at
   `sys.exit(0)` on `HALT_ENERGY` (L555) *before* the `torch.save` at L750;
   `save_halt` (L330–349) persists only `exp078_results.json`; no
   `exp078_vectors.pt` exists anywhere in `~/workspace`. The earlier draft's
   provenance claim ("the smoke run built and persisted $Q_S$; LOG-114") was
   **false** and is deleted here.
   Sourcing rule: $Q_S$ is built by the pinned §3.1a procedure at G2 build time;
   its SHA-256 is recorded in the run manifest; a rebuild failure (rank or
   orthonormality guard) is a **readiness halt (a)** — genuine, not guaranteed.
   Degeneracy guard (CPU-computable, after the rebuild, before selection): assert
   $\|P_S b(x)\| > 10^{-3}$ for all 60 items; EXP078 measured
   $e_{\mathrm{median}} = 0.0544$ on this quantity, so the guard is far from the
   empirical value — a firing means the rebuild is wrong, not that the guard is
   tight.
10. **Static $B_{\mathrm{agg}}$ — the incumbent.** The static aggregated contrast
    basis, verbatim EXP066/077 construction. Including it makes the oracle a
    strict superset selector: the oracle can always fall back to the static
    direction, so any measured oracle–static gap is pure *selection* gain, never
    pool luck.

**Removed from the selection pool (B3):** static $B_\perp$ (seed 9876) and static
$B_{\mathrm{wrong}}$ (Paris-capital contrast) are **not** pool members — the source
idea (SPRINT2 §G2) enumerates the pool as 10 without them; their inclusion was
arithmetic-fitting (LOG-143), and a dead control in an argmax-correctness pool can
only inflate $b$ by chance, dilutes the (f)-branch instrument, and pollutes the
audit. They stay as forced-baseline test conditions C5/C6 (§5).

**Norm assertions (the F1 lesson):** every pool member is asserted unit-norm
($|\,\|u\| - 1| < 10^{-5}$) at build time; any violation aborts as a protocol
violation. A silent-zero control must be impossible, not just absent.

### 3.1a Phase-0 $Q_S$ rebuild [DEFINITION] (B1 — Path A, chosen)

**[FACT]/[OBSERVATION]** The rebuild reconstructs, verbatim, the EXP078 support
procedure (`run_exp078.py` `build_subspace_S` L204–220 + support loop L359–387) —
the archived code is the pin, not a prose description. 300 forward passes
(5 vocabs × 30 pairs × 2); forwards on GPU, all algebra on CPU (the LOG-116
discipline: support deltas `.detach().cpu()`).

Pinned constants (copied verbatim from the archived runner):
- `SUPPORT_VOCABULARIES`: V1_Anglo = [Alice, Bob, Charlie, David, Emma];
  V2_Biblical = [Aaron, Joel, Gideon, Ruth, Abel]; V3_Greek = [Ajax, Jason,
  Apollo, Paris, Atlas]; V4_Roman = [Marcus, Julius, Augustus, Felix, Diana];
  V5_Modern = [Liam, Noah, Eli, Maya, Finn].
- `TRIPLES_INDICES` (15): (0,1,2), (1,2,3), (2,3,4), (0,2,4), (0,1,3), (1,3,4),
  (0,2,3), (1,2,4), (0,3,4), (0,1,4), (0,1,2), (1,2,3), (2,3,4), (0,2,4), (0,1,3).
- `QUADS_INDICES` (15): (0,1,2,3), (1,2,3,4), (0,1,3,4), (0,2,3,4), (0,1,2,4)
  repeated 3×.

Procedure per vocab $v_k$, index $i$:
- triple $(i_A, i_B, i_C)$: $q_{\text{opts}} =$ "`$A$ or $C$`" if $i$ even else
  "`$C$ or $A$`"; $p_{\text{rel}} =$ "Premise: $A$ outranks $B$. $B$ outranks $C$.
  Question: Who is higher in rank, $q_{\text{opts}}$? Answer:"; $p_{\text{neu}} =$
  the same template with "is next to" replacing "outranks". Quad analog with 4
  entities and "`$A$ or $D$`"/"`$D$ or $A$`" parity.
- $\delta h = h_{\text{rel}} - h_{\text{neu}}$: hidden state at
  `hidden_states[TARGET_LAYER + 1]` (post-layer-20), last-token position,
  `.detach().cpu()`.
- Per vocab: stack $[30, d]$ → row-normalize → mean over the 30 rows →
  renormalize → $\hat v_k$; $V = [\hat v_1 \dots \hat v_5]$ $[d, 5]$;
  `torch.linalg.qr(V, mode="reduced")` **on CPU** → $Q_S$ $[1024, 5]$.
- Determinism pin (inherited from EXP078): `torch.manual_seed(20260923)`,
  `np.random.seed(20260923)`, `torch.use_deterministic_algorithms(True)` where
  supported.

Build asserts (failure = readiness halt (a) — genuine, not guaranteed):
- rank guard: $\sigma_{\min}/\sigma_{\max} > 10^{-6}$ (`RANK_GUARD_RATIO`,
  inherited from EXP078 §3.1);
- orthonormality: $\|Q_S^\top Q_S - I_5\|_F < 10^{-5}$;
- SHA-256 of $Q_S$ (float32 CPU bytes) recorded in the run manifest at build time.

No-peeking (EXP078 §3.1 m1, inherited): the rebuild sees only the pinned constants
above + model weights; benchmark items and labels are never touched by the rebuild
function — signature-isolated, not asserted. The EXP078 energy/headroom gates are
**not** re-run here — they belonged to EXP078's halted hypothesis, not to $Q_S$
construction (which passed its own rank guard).

**[INFERENCE]/[INTERPRETATION] Why Path A over Path B (reviser's rationale,
Law #8):** (1) source-idea fidelity — SPRINT2 §G2 enumerates the pool as
{self-bridge, 7 pseudo-bridges, $P_S$-residue, $B_{\mathrm{agg}}$} = 10; with B3
removing the two budget-fitted controls, keeping $P_S$-residue via rebuild means
the pool matches the source idea exactly, no deviation rationale needed.
(2) Scientific content — the $P_S$-residue member is the EXP078 localization
question as an intervention, and with $e_{\mathrm{median}} = 0.0544$ (bridge power
~95% outside $S$) it is expected near-orthogonal to the bridge, so it can only
*enrich* the §7 marginal-rescue decomposition (a non-bridge rescue source),
never confound it. (3) Cost — 300 passes (~15s GPU); total 1,320 passes remains
free-tier trivial. (4) Pre-registerability — the procedure is verbatim-pinned from
archived code, not a prose pointer.
**Provenance honesty (Law #8):** the built $Q_S$ is a *reconstruction* from the
archived procedure, not "the archived EXP078 artifact" — no such artifact ever
existed (B1). It is numerically a fresh instance of the same construction, pinned
and hash-recorded here.

### 3.2 Why this pool (and what bounds the license)

**[INFERENCE]/[INTERPRETATION]** The pool is family-honest for the output-side
evaluator program: it contains the strongest known output-side intervention (the
self-bridge), the target-free directions an evaluator could construct (the
pseudo-bridges), the in-subspace residue (the EXP078 localization question, now as
an intervention), and the incumbent plus specificity controls. The kill in
branch (c) is licensed **only within this pre-registered family**, on this
benchmark/model/layer — the A-pool discipline (EXP070 §7) applies here with the
family named as *output-side per-item directions at layer 20*.

**[INFERENCE]/[INTERPRETATION]** Known limitation, stated not smuggled: the
self-bridge dominates the pool — on items where the bridge rescues, the oracle
will select it, making C3 $\approx$ C7 on those items. The "oracle selection" is
therefore close to a single-candidate test wherever the bridge works. The
protection against learning nothing beyond "the bridge works" (already known) is
the pre-registered exploratory **marginal-rescue decomposition** (§7): per rescued
item, the full correct set, split into bridge-driven rescues vs rescues where a
non-bridge member was correct with the bridge wrong. If the oracle never rescues
an item without the bridge, the ceiling is a bridge
ceiling — reported as such (Law #8), not as an output-room ceiling.

---

## 4. Oracle selection rule and anti-cheat

### 4.1 Selection rule [DEFINITION]

For test instance $x$, for each $B \in \mathcal{P}$: run $f_\theta$ on $x$ with
intervention $h \leftarrow h + \alpha B$ at $l^*$, and record
$r(B; x) = \mathbf{1}[\text{decision correct on } x]$ (the item's true label used —
permitted ceiling measurement, §1.1; decision rule identical to the EXP066/EXP077
bench verbatim code path, not redefined here).

$$B^*(x) = \arg\max_{B \in \mathcal{P}} r(B; x),$$

ties broken by a seeded-random draw uniform over the top-tied candidates (seed
7201, pre-registered; the draw is archived per instance) — **direction-neutral in
expectation**: neither the incumbent, the bridge, nor any challenger is favored
(direction-neutral is retained for audit cleanliness, not as an M3 correction:
the EXP070 M3 citation is misapplied here — under correctness-argmax the tie-break
**cannot** affect $b$ (any draw among correct candidates is correct; any draw
among all-wrong is wrong), so no tie-break rule could bias the instrument toward
the kill branch).

### 4.2 Random-selection condition (the (f)-branch instrument)

C4 selects $B \sim \mathrm{Uniform}(\mathcal{P})$ per instance (uniform over the
**10** members, seed 7202, pre-registered, archived). This separates "selection works" from "the pool is
good" — the f2-analog of EXP068 §11.

### 4.3 Winner's-curse direction [LIMITATION — stated, not smuggled]

**[INFERENCE]/[INTERPRETATION]** Unlike EXP070 (which selected on support analogs),
G2 selects on the test item itself with its label — the most generous oracle the
program has fielded. Best-of-10 selection on the item's own label **inflates**
the measured ceiling; it cannot deflate it. Consequence for the licenses:
- A **kill** under this generous instrument is *strong* evidence of a zero
  ceiling — the program could not beat static even when handed the answers.
- A **win** is an *upper bound*, not an achievable gain — a target-free evaluator
  will recover only a fraction of it. This is why the worth-chasing bar (§9,
  $+12$pp) sits where it does, and why a win licenses only Phase B *behind a new
  pre-registration*, never a claim that the gap is recoverable.
- EXP070's uninformative-probe failure mode (branch (c2) there) **cannot occur
  here by construction**: there is no probe, so there is no probe-noise gate to
  fail. The residual failure mode is benchmark/setup drift, caught by branches
  (a)/(b).

### 4.4 Anti-cheat clause [DEFINITION]

1. Test labels are used **solely** for (i) the per-item argmax correctness
   evaluation in §4.1 — the ceiling instrument — and (ii) the degeneracy guard
   $\|P_S b(x)\| > 10^{-3}$ (§3.1 item 9), a norm inequality that exports
   nothing. They are never used in candidate
   construction (except the self-bridge and $P_S$-residue, whose label use is the
   licensed oracle-sense construction), never exported, never inform any
   condition except through $B^*(x)$.
2. Per sprint kill-list #4 and Law #7: a label-informed bridge presented as a
   *method* is a killed proposal class. The oracle selection here is a
   **measuring instrument, discarded after use**. Any downstream use of
   $B^*(x)$ directions as a proposed technique is a protocol violation.
3. **Any leakage** (post-hoc pool expansion; candidate construction touching
   items outside §3.1; $Q_S$ rebuild substitution of any constant or template
   from §3.1a without re-pinning) =
   **invalid run**, reported as a protocol violation per Law #8, never silently
   corrected under the G2 label.

### 4.5 Lemma L1 — the superset lemma ($c = 0$ by construction) [FACT]/[THEOREM] (B2a)

**Lemma.** Under the §11 determinism pin (seeds 7201/7202/20260923 fixed,
deterministic algorithms where supported), on C3-vs-C2:
$c = \#\{x : \text{C2 correct} \wedge \text{C3 wrong}\} = 0$ exactly.

*Proof.* $B_{\mathrm{agg}} \in \mathcal{P}$ (§3.1 item 10). If
$r(B_{\mathrm{agg}}; x) = 1$ then $\max_{B \in \mathcal{P}} r(B; x) = 1$, and the
§4.1 tie-break draws only among the correct candidates — so C3 is correct whenever
C2 is. Hence $\{\text{C2 correct}\} \subseteq \{\text{C3 correct}\}$ exactly, and
$c = 0$. ∎

**Consequences [FACT]/[INTERPRETATION]:**
- The C3-vs-C2 McNemar collapses to a one-sided binomial test on $b$ (rescues).
  The §9 branch mapping in $b$-terms: (c) ⟺ $b \le 5$; (d) ⟺ $b \in \{6, 7\}$;
  (e) ⟺ $b \ge 8$.
- $b \ge b_{\text{bridge}} := \#\{x : \text{bridge correct} \wedge B_{\mathrm{agg}}
  \text{ wrong}\}$ (the self-bridge is pool member #1). Historical
  $b_{\text{bridge}} = 6$ (GPU) — exactly the (d) floor.
- The §9 tree's general form still assigns every $(b, c)$ cell including $c > 0$
  (M5.2 — no unassigned cell); all reachability and power claims below are
  **conditional on $c = 0$**, i.e. on the determinism pin holding.

---

## 5. Conditions (7)

| # | Condition | Intervention / procedure |
|---|---|---|
| C1 | Unintervened baseline | none |
| C2 | Static $B_{\mathrm{agg}}$ (benchmark) | $h \leftarrow h + \alpha B_{\mathrm{agg}}$, $\alpha = 0.50$ |
| C3 | **Oracle-selected per-instance direction (G2 mechanism)** | $h \leftarrow h + \alpha B^*(x)$ per §4.1 |
| C4 | Random-selected candidate ("selection works" killer) | uniform-random $B \in \mathcal{P}$ per instance, seed 7202 |
| C5 | Static $B_\perp$ | specificity control (seed 9876, inherited) |
| C6 | Static $B_{\mathrm{wrong}}$ | wrong-task control (as EXP066) |
| C7 | Self-bridge (positive control) | identical to EXP066/078 `make_bridge_vec`, per item |

---

## 6. Benchmark, readiness, and the feasibility computation

- **Benchmark:** the identical N=60 Planetary/Elemental 2-hop/3-hop suite from
  EXP065 (same items, same premise permutations). No new benchmark construction
  (Law #9).
- **Readiness halt (a) triggers:** $Q_S$ Phase-0 rebuild failure (rank or
  orthonormality guard, §3.1a — evaluated on GPU in Phase 0, before any
  *selection* spend); any benchmark entity multi-token under the real 410m
  tokenizer (F2-guard discipline, LOG-111; CPU-computable, before any GPU
  spend); any $\|P_S b(x)\| \le 10^{-3}$ (after the rebuild); any pool-member
  norm assertion failure.

### 6.1 Probe-feasibility algebra (LOG-138 discipline — computed BEFORE the gate)

**[FACT — computed]** The maximum achievable $N$ in closed form:

$$N_{\mathrm{final}} = 60 - n_{\mathrm{excluded}},$$

where $n_{\mathrm{excluded}}$ counts items for which some pool member is
uncomputable. By §3.1: (i) the self-bridge needs single-token target/foil —
**[FACT]/[OBSERVATION]** all 10 benchmark novel entities are single-token under
the 410m tokenizer (LOG-113 independent verification), and foils are drawn from
the same verified entity set; (ii) pseudo-bridges need only C1 logits — always
available; (iii) $P_S$-residue needs $Q_S$ — built in-protocol in Phase 0 (§3.1a) before any
selection pass; a build failure fires readiness halt (a) as a genuine halt,
never a guaranteed one (B1); (iv) static members are global. Hence
$n_{\mathrm{excluded}} = 0$ **by construction**, and

$$\boxed{\min N_{\mathrm{final}} = \max N_{\mathrm{final}} = 60 \ge 50}$$

— the $N_{\mathrm{final}} \ge 50$ power floor is reachable by construction. No
EXP079-style structural shortfall is possible here: there is no split, no probe
map, no attrition mechanism. The only non-determinism (Phase-0 build outcome) is evaluated before
GPU selection spend, as a readiness halt — never as a mid-run
surprise. **Never sign an infeasible gate again: the gate is feasible by
construction, shown above.**

**[FACT — computed]** Gate reachability on the McNemar grid ($N = 60$,
exact two-sided, $\alpha = 0.05$):

| Cell $(b, c)$ | $\Delta M$ | $p$ | Branch it fires |
|---|---|---|---|
| $(0, 0)$ | $0.0$pp | $1.0000$ | (c) — the measured-zero cell; inhabited by this program's boundary series (EXP070 hidden-state pool: $\Delta M = +0.00$pp) |
| $(5, 0)$ | $+8.3$pp | $0.0625$ | (c) — positive-but-nonsignificant; the m7 cell; assigned, not silent |
| $(6, 0)$ | $+10.0$pp | $0.03125$ | (d) — minimum significant win; the (d) floor |
| $(8, 0)$ | $+13.3$pp | $0.0078$ | (e) — minimum (e) cell |

**[FACT — computed]** (B4) Cells with $c > 0$ are unreachable under the determinism
pin: e.g. the former §6.1 row $(11, 3)$ ($+13.3$pp, $p = 0.0574$) would require
three C2-correct/C3-wrong items, impossible under Lemma L1 ($\{\text{C2
correct}\} \subseteq \{\text{C3 correct}\}$ exactly). It is moved to the §7
impossible-cells list with proof — it is **not** the "≥+12pp-but-nonsignificant
cell closing the partition gap" (no such gap exists under $c = 0$).

**[INFERENCE]/[INTERPRETATION]** Reachability restated in $b$-terms under Lemma L1
($c = 0$): (c) via $b \le 5$ (the null region the program has repeatedly inhabited,
including the boundary null); (d) via $b \in \{6, 7\}$; (e) via $b \ge 8$. Every
branch is reachable by construction; no branch is a dead letter. Cells with
$c > 0$ are unreachable under the determinism pin — listed in §7 with proof
(M5.4); the tree's general form still assigns them (M5.2).

**Positive-control *detectability* [FACT]/[OBSERVATION]** (m4 — this is a
detectability characterization, not a validity requirement; branch (b) contains
no C7 conjunct by design): C7 (self-bridge) has minimum detectable cell $(6,0)$
on $N = 60$. Archived bridge effects: smoke $+23.33$pp ($(b,c) = (14,0)$,
$p = 0.000122$); GPU $+10$pp ($(b,c) = (6,0)$, $p = 0.03125$) (EXP077).
**[INFERENCE]/[INTERPRETATION]:** the smoke effect exceeds the floor with wide
margin; the GPU effect sits exactly at the floor. C7 non-replication is the
measured ceiling, never invalidity (see §9(c) note).

---

## 7. Endpoints

- **Primary (confirmatory):** $\Delta M$ (percentage points) on paired decisions,
  C3 vs C1; McNemar exact two-sided on $(b, c)$.
- **Key comparison (the kill):** C3 vs C2 — paired McNemar exact two-sided on the
  (oracle, static) decision pairs over the same items. $b$ = oracle-rescues
  (C3 correct, C2 wrong); $c$ = oracle-corruptions (C3 wrong, C2 correct).
- **Secondary (pre-registered):** C3 vs C4 (attribution: does *selection* beat
  random? — feeds branch (f)); C2 vs C1 (static-null replication check — feeds
  branch (g)); **C3 vs C7 McNemar** (the direct bridge-superiority measure —
  zero extra passes, data already collected; feeds the audit; no new branch,
  M5.2 intact — it is measurement, not a ruling); rescues $b$ / corruptions $c$;
  $\mathrm{KL}_{\mathrm{div}} < 0.50$
  guardrail (exploratory, inherited); **marginal-rescue decomposition**
  (exploratory, B2b): for each rescued item $x$ (C3 correct, C2 wrong), record
  the full correct set $\mathrm{Corr}(x) = \{B \in \mathcal{P} : r(B; x) = 1\}$
  and report (i) rescued with the bridge correct, (ii) rescued with the bridge
  wrong but $\ge 1$ non-bridge member correct — **the true selection prize**
  (this count gates the §9(d)/(e) "output room" licenses), (iii) rescued with
  *only* non-bridge members correct. **[FACT]/[INTERPRETATION]** Under Lemma L1,
  (iii) coincides with (ii) on rescued items ($B_{\mathrm{agg}}$ is wrong on
  every rescued item by definition) — reported as a single bin, the identity
  noted.
- **Margin shifts:** recorded but **exploratory only** — audit Finding 3 / O5
  stands: the C6 control invalidates margin-shift significance as a causal endpoint.

**Degenerate-input handling (M5.3):** under Lemma L1 ($c = 0$ by construction),
$b = c = 0$ is the only $b = c$ case under the determinism pin; the exact
two-sided McNemar $p = 1.0$ by convention for the degenerate test — this is the
measured-zero cell, assigned to branch (c), not an undefined statistic. If C3
$\equiv$ C2 decisions on all items but C1 differs,
$\Delta M_{\mathrm{oracle}} - \Delta M_{\mathrm{static}} = 0$ is still reported
exactly. No undefined statistic has an unassigned branch (M5.2).

**Impossible cells carry their proof (M5.4):**
- $(\Delta M_{\mathrm{oracle}} - \Delta M_{\mathrm{static}} = 0,\ p < 0.05)$:
  vacuous — $b = c \Rightarrow p = 1.0$ under exact McNemar.
- $(p < 0.05,\ \text{margin} \ge +12\text{pp})$ not firing (e): impossible by the
  §9 partition — all such cells are (e).
- **Any $(b, c)$ with $c > 0$ on C3-vs-C2** — including the former §6.1 row
  $(11, 3)$ ($+13.3$pp, $p = 0.0574$): *unreachable under the §11 determinism
  pin*. **Proof** (Lemma L1, §4.5): $B_{\mathrm{agg}} \in \mathcal{P}$ and
  correctness-argmax selection ⇒ $\{\text{C2 correct}\} \subseteq \{\text{C3
  correct}\}$ exactly ⇒ $c = 0$; $(11, 3)$ would require three
  C2-correct/C3-wrong items, which cannot exist. (The tree's general form still
  assigns these cells — M5.2 — but no execution path under the pinned seeds
  reaches them.)
- A non-unit pool member entering selection: impossible by the §3.1 norm
  assertions (build-time abort).

---

## 8. Assumptions (named, not smuggled)

- **[ASSUMPTION]/[ASSUMPTION] A-family (the false-kill route):** the output-side
  evaluator program's search space is fairly represented by the 10-member pool
  $\mathcal{P}$ at layer 20. The kill in branch (c) is licensed **only within
  this pre-registered family**, on this benchmark/model/layer. A future evaluator
  over a *different* output-side family (per-instance $\alpha$, layer sweeps,
  matrix-valued directions) is a new pre-registration, not a resurrection.
- **[ASSUMPTION]/[ASSUMPTION] A-generous:** selecting on the test item's own
  label inflates the measured ceiling (§4.3). Direction of risk: the kill is
  *easier to trust*, the win is *harder to trust as achievable*. The
  significance + magnitude bar (§9) carries the conservatism for the
  justification decision.
- **[ASSUMPTION]/[ASSUMPTION] A-bridge-dominance:** acknowledged in §3.2 — the
  self-bridge is expected to dominate selection where it rescues. The
  marginal-rescue decomposition (§7) is the pre-registered check on whether the
  ceiling is a bridge ceiling or an output-room ceiling.

---

## 9. Pre-registered decision tree

**Branch precedence [DEFINITION]** (m8 precedent): (a) is evaluated first
(readiness); then (b) (validity); then (f) (selection attribution); then exactly
one of (c)/(d)/(e) fires — the three form an exhaustive partition of the
(C3-vs-C2) outcome space ($\{p \ge 0.05\} \cup \{p < 0.05,\ \mathrm{margin} <
+12\mathrm{pp}\} \cup \{p < 0.05,\ \mathrm{margin} \ge +12\mathrm{pp}\}$ = every
cell; M5.2). A fired (f) suspends the selection licenses of (c)/(d)/(e) but not
their pool-quality reporting (Law #8). (g) is informational and fires alongside
any branch.

The $+12$pp worth-chasing bar is inherited from EXP070's re-derived justification
(LOG-083): the lowest round bar strictly above the significance floor at which
the p-value and magnitude conditions bind independently on $N = 60$ — $(6,0)$ is
significant at $+10.0$pp but below the bar → (d); $(8,0)$ clears it at $+13.3$pp,
$p = 0.0078$ → (e). [ARBITRARY — sensitivity bands at $+16$pp and $+20$pp
reported alongside the ruling.] Rationale (unchanged): the oracle is an
unachievable upper bound; a target-free evaluator recovers only a fraction of
its gap; $+12$pp is a *lenient* bar and the halving-honest $\sim$+20pp is the
upper sensitivity band.

| # | Branch | Pre-registered ruling — LICENSES / DOES NOT LICENSE |
|---|---|---|
| (a) | **Readiness halt** (§6 gates fail: rebuild/tokenizer/norm pre-checks) | **Reportable halt**, not a result about selection. LICENSES: "the preconditions for the ceiling measurement are not met." DOES NOT LICENSE: anything about $H_{\mathrm{ceiling\text{-}G2}}$; any evaluator-program verdict. Evidentiary verdict: **Inconclusive**. Evidentiary level: none (readiness halt). |
| (b) | **Validity failure** (post-run): $\Delta\theta \ne 0$, any injection norm $= 0$, C1 baseline outside $[40\%, 70\%]$ (headroom-gate provenance: EXP067 headroom gate, LOG-129; EXP077 smoke C1 $= 0.60$), or C5/C6 show McNemar $p < 0.05$ each vs C1 (a specificity control firing = setup drift) | **Invalid run.** **No conclusion about $H_{\mathrm{ceiling\text{-}G2}}$ may be drawn**; do not interpret C3 (EXP067 §7.1(b) discipline). Note: C7 failing to replicate is NOT a (b) — it is the measured ceiling; see (c). Evidentiary verdict: **Inconclusive**. Evidentiary level: none (invalid run). |
| (c) | **KILL:** C3 vs C2: **no statistically significant gain ($p \ge 0.05$)** — includes $\Delta M_{\mathrm{oracle}} \le 0$, the $(0,0)$ measured-zero cell, and the $(5,0)$ positive-but-nonsignificant cell. Cells with $c > 0$ are unreachable under Lemma L1 (§4.5) — see §7. | **The output-side evaluator program is stood down.** LICENSES: "Even the generous label-informed oracle over the output-side pool does not beat static injection here — the ceiling is zero as measured; no target-free evaluator over this family can justify its cost." The verdict on $H_{\mathrm{ceiling\text{-}G2}}$ is **Not supported** (pre-registered falsification criterion fired; evidentiary level: improve-inference). If C7 failed to replicate, that non-replication is logged as a boundary-relevant observation (Law #8) and the kill stands on the pool as measured. **Bridge-replication contingency (Law #8):** given C2-null replication, (c) ⟺ the bridge rescues $\le 5$ items — the stand-down is on the pool as measured, but the report distinguishes *bridge-degradation* (the bridge failed to replicate its historical 6 rescues) from *evaluator-failure* (the target-free pseudo-bridges added nothing where the bridge rescued). The kill itself stays simple per the m7 discipline. DOES NOT LICENSE: "representation-level adaptation is impossible in general" (family-, model-, benchmark-restricted); "the adaptive loop hypothesis is falsified" (never tested); any claim about directions outside $\mathcal{P}$ (A-family); "the bridge never works" (historical rescues stand). Re-motivation path: a future program over a *different* output-side family is a new pre-registration, not a resurrection. |
| (d) | **Oracle wins small:** C3 beats C2, McNemar $p < 0.05$, but margin $< +12$pp | **Program survives; Phase B NOT licensed.** LICENSES (B2c — gated on the §7 marginal-rescue decomposition): **if** non-bridge marginal rescues (bin (ii)) $> 0$ — "a selection signal exists in the output room but is below the worth-chasing bar." **If** bin (ii) $= 0$ — no "output room" license issues; the ruling reports "**bridge ceiling, not pool ceiling**" (Law #8), and the program's survival is qualified as resting on the bridge alone. Verdict on $H_{\mathrm{ceiling\text{-}G2}}$: **Supported** (the statistical leg), with the magnitude leg failed — the bar is the bar. Reported at $+12$/$+16$/$+20$pp sensitivity bands. DOES NOT LICENSE: Phase B; any evaluator build; "the gap is recoverable target-free" (A-generous: the win is an upper bound). Evidentiary level: improve-inference. |
| (e) | **Oracle wins big:** C3 beats C2 by $\ge +12$pp **and** McNemar $p < 0.05$ | **Phase B licensable — explicitly NOT licensed.** LICENSES (B2c): the "per-instance selection prize exists in the output room" license — and with it the Phase-B-licensable judgment — issues **only if** §7 bin (ii) (non-bridge marginal rescues) $> 0$; the oracle–static gap then quantifies the most any evaluator could be worth. **If** bin (ii) $= 0$, the ruling reports "**bridge ceiling, not pool ceiling**" (Law #8): a bridge-dominated gap is not evidence any target-free evaluator could recover anything, so Phase B is **not licensable** on this result — the license conditions are unmet. Verdict on $H_{\mathrm{ceiling\text{-}G2}}$: **Supported** (evidentiary level: improve-inference). DOES NOT LICENSE: building Phase B (requires ALL of: a new pre-registration, AND EXP068 reconciliation — EXP068's unlicensed status is unchanged by this result — AND the Law #14 review of that pre-registration); "a target-free evaluator can recover the gap" (unmeasured; A-generous); any novelty-tier movement (N1 stands); any level-2/level-3 claim. |
| (f) | **No selection signal:** C4 (random) $\ge$ C3 ($\Delta M_{C4} \ge \Delta M_{C3}$) | **Do not kill or justify on selection grounds.** LICENSES: "the pool helps but *selection* doesn't — or the oracle methodology is uninformative." Verdict on $H_{\mathrm{ceiling\text{-}G2}}$: **Underdetermined** (selection attribution unresolved). A C4 $>$ C2 finding alone is a pool-quality result, reported as such (Law #8), not an evaluator justification. Diagnose via the §7 marginal-rescue decomposition before any re-registration. Precedence: (f) is evaluated before (c)/(d)/(e); a fired (f) suspends their selection licenses, not their pool reporting. Evidentiary level: improve-inference. |
| (g) | **C2 static replicates the boundary null** ($\Delta M = 0$, $b = c = 0$) while C7 rescues | Informational consistency check — fires alongside any branch. The boundary result reproduces on this run; the ceiling was measured under the same conditions as the program's headline null. If C2 shows $\Delta M \ne 0$ here, flag the discrepancy vs EXP065/066 before interpreting any branch (benchmark/drift diagnostic). Evidentiary verdict: none — informational overlay by design. Evidentiary level: none. |

---

## 10. Budget and compute plan (free-tier feasibility)

**[DEFINITION]** Primary compute metric: forward passes. All accounting is
**worst-case, no caching**.

| Phase | Forward passes (worst case) | Basis |
|---|---|---|
| Phase-0 $Q_S$ rebuild (§3.1a) | $300$ | 5 vocabs $\times$ 30 pairs $\times$ 2 (rel/neu) |
| Oracle selection (§4.1) | $600$ | 10 candidates $\times$ 60 items |
| Test conditions C1–C7 | $420$ | $7 \times 60$ single forwards |
| **Total** | **$\boxed{1{,}320}$** | **[FACT — computed]** |
| Wall-clock | $\approx 60$s | sprint estimate on 2$\times$T4 **[ESTIMATE]** (batched short-sequence 410m) |

**[FACT — computed]:** $300 + 10 \times 60 + 7 \times 60 = 300 + 600 + 420 = 1{,}320$.
Pseudo-bridge construction needs no extra passes (C1 logits reused); the
self-bridge and static members are weight-only; $Q_S$ is built in-protocol in
Phase 0 (300 support passes, §3.1a — no archived artifact exists, B1), not
loaded. **Order of operations:** (1) CPU readiness checks (tokenizer
single-token, static norm assertions; no GPU) → (2) Phase-0 $Q_S$ rebuild (GPU;
rank/orthonormality asserts; SHA-256 recorded in the manifest) → (3) degeneracy
guard $\|P_S b(x)\| > 10^{-3}$ (CPU, weight-only) → (4) 5-instance pilot (GPU:
wall-clock measurement + selection-yield smoke — diagnostics, not a ruling) →
(5) full launch. The run is splittable across Kaggle sessions (rebuild →
selection phase → test phase are natural checkpoints with all state archived).

---

## 11. Reproducibility and hygiene (Law #13)

- **Seeds (pre-registered):** master `torch.manual_seed(20260923)`, NumPy
  `20260923` (also the Phase-0 rebuild seeds, inherited from EXP078); oracle
  tie-break 7201; C4 random selection 7202 (uniform over the 10 members).
  Pseudo-bridges are deterministic (no seed).
- **Archive (all persisted):** the 10 pool vectors per item (or the deterministic
  recipe + C1 logits for the pseudo-bridges); per-instance candidate correctness
  $r(B; x)$ for all $B \in \mathcal{P}$; the selected $B^*(x)$ index and its
  tie-break draw; the per-item correct set $\mathrm{Corr}(x)$ (for the §7
  decomposition); injection-vector norms (asserted $> 0$); per-instance condition
  records in the EXP066 JSON schema; the rebuilt $Q_S$ + its SHA-256 + build
  diagnostics (rank ratio, singular values, support-procedure constants);
  environment manifest.
- **Hook isolation:** forward hook registered per instance, removed after; no
  inter-instance state. Determinism: `torch.use_deterministic_algorithms(True)`
  where supported.
- **No silent retuning:** any change to pool, selection rule, or thresholds after
  execution begins is a protocol violation — the changed design takes the next
  free number at pre-registration time (Law #4).

---

## 12. Non-goals (explicit)

- This protocol does not test any target-free evaluator — none is built here
  (Phase B is deferred; §9(e)).
- It does not test the loop's $\mathcal{S}/\mathcal{T}$ dynamics, multi-iteration
  compounding, or the $\rho$-gate — those belong to EXP068 (unlicensed).
- It does not claim the oracle is achievable, deployable, or interesting as a
  method — it is a measuring instrument, discarded after use (§4.4).
- It does not move the novelty tier in any direction (N1 stands).
- It does not test directions outside $\mathcal{P}$ (A-family bounds the
  license), other layers, other $\alpha$, or other models.

---

**Pre-registration checklist:** ☐ pool $\mathcal{P}$ fixed (10 members, §3.1
constructions + §3.1a Phase-0 rebuild, seeds 7201/7202/20260923) ☐ $Q_S$ sourcing
fixed (Phase-0 rebuild, SHA-256 recorded at build time; rebuild failure =
readiness halt (a)) ☐ oracle selection rule fixed (§4.1, direction-neutral
seeded tie-break) ☐ Lemma L1 stated (§4.5) ☐ marginal-rescue decomposition +
C3-vs-C7 secondary pre-registered (§7); (d)/(e) "output room" licenses gated on
non-bridge marginal rescues ☐ winner's-curse direction documented (§4.3)
☐ anti-cheat clause armed (§4.4) ☐ $\alpha = 0.50$, layer 20, 410m fixed
☐ headroom gate armed ☐ $N_{\mathrm{final}} = 60$ feasibility shown in closed
form (§6.1) ☐ every McNemar cell assigned a branch, $c > 0$ cells proven
unreachable (§6.1 table + §7; M5.2/M5.3/M5.4) ☐ $+12$pp bar
recorded [ARBITRARY] with $+16$/$+20$pp sensitivity bands ☐ full decision tree
recorded (§9, every branch has LICENSES / DOES NOT LICENSE + permitted verdict
+ evidentiary level) ☐ A-family named as the false-kill route (§8) ☐ SHA-256
guard armed ($\Delta\theta \equiv 0$) ☐ budget $1{,}320$ passes with exact
arithmetic (§10)
*No results exist under this protocol. Any deviation is a protocol violation, not a discovery.*
