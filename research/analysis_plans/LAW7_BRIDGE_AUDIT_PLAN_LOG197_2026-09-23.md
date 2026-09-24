# Law #7 Bridge Construction Compliance Audit — FROZEN PLAN

**LOG-197 · Track-8 Experimental Statistician · 2026-09-23**
**Status: FROZEN — pending Law #14 review (SIGN / SIGN-WITH-FIXES releases execution).**
**No GPU. No forward passes. No weight writes (Δθ=0). Read-only weights. CPU/$0 only.**

**Dispatch:** Research Lead, on CEO order. STEP 1 of the no-blind-running chain
(plan → Law #14 review → execution → verdict). This file is the PLAN ONLY.

**Chain position:** §H6 battery preparation — K1 (readout-tilt) FIRST, K2 SECOND,
K3 THIRD on interpretation; parallel *preparation* is permitted. This audit is the
K3-adjacent **construction/code provenance audit**: it answers whether the bridge is
option-informed as built and as used (Q1), and — conditional on that — re-reads the
archived rescues under the §G1b decision rule (Q2). It does NOT draw the K3 kill
verdict ("output-side program re-scoped"); that belongs to the K3 falsifier
(compliant-bridge build + rescue test), which is gated on K1 survival per §H6.

**Scope (signed protocols are immutable):** EXP065 / EXP066 / EXP070 / EXP077, the
four runs whose output-bridge arms repeatedly rescued (+10.00pp to +16.67pp).
EXP078's bridge is a subspace-restricted variant on a different mechanism question
and is OUT of scope (its halt is already recorded). EXP075's licensed existence
proof uses a donor construction — also OUT of scope.

---

## 1. Audit questions (formal)

**Q1 — construction provenance.** *Is the bridge construction, as implemented in the
code and as executed in the archived EXP065/066/070/077 runs, built from
target/foil option-token unembedding rows — i.e., option-informed on the letter of
Law #7?*

- H0 (Q1): the executed bridge directions carry no per-item test-label information:
  no test item's target answer, foil, or candidate-option token row of the
  unembedding matrix enters the construction function.
- H1 (Q1): the executed bridge directions are option-informed: each item's own
  target and foil tokens are encoded and their unembedding rows enter
  normalize(E[target] − E[foil]).

**Q2 — rescue attribution (conditional on Q1 being Supported).** *Under the §G1b
effect+CI+δ_min decision protocol, are the recorded rescues best read as
label-assisted readout artifacts rather than evidence of steerability?*

- H0 (Q2): the archived rescue magnitudes are too small/uncertain to license even
  the narrow L1 reading ("the readout is causally accessible to an option-informed
  direction") — the rescues fail the §G1b meaningful-magnitude rule.
- H1 (Q2): the rescues clear the §G1b meaningful-magnitude rule, and the
  parsimonious licensed reading is the label-assisted readout artifact (L1-narrow),
  NOT evidence of autonomous steerability (which would require the K1/K2 battery to
  rule in its favor — a verdict this audit does not draw).

[NOTE on Q2's framing: "label-assisted readout artifact" is the *narrow* licensed
reading of a meaningful rescue; "steerability evidence" is a *stronger* reading that
demands more (K1 tilt-survival). This audit distinguishes artifact-compatible from
not-significant; it never certifies steerability.]

---

## 2. Endpoints (exact and computable)

### E1 — Construction-algebra identity (Q1, deterministic)

**Question (own words):** does the bridge direction the code constructs equal
normalize(E[target] − E[foil]) up to sign and normalization?

**Procedure (executor):** for each of the four runs, rebuild every per-item bridge
vector weight-only: encode the item's target/foil token strings exactly as the
run's code encodes them (see §3), fetch the two unembedding rows from the
read-only weight matrix, form `w = E[tt] − E[ft]`, normalize. Then verify the
documented code path's formula algebraically:

- **Algebraic tolerance:** |cos(b_reconstructed, b_codeform)| ≥ 1 − ε, with
  **ε = 1e-6** [ARBITRARY — the construction is float32 linear algebra; 1e-6 is
  three orders of magnitude above float32 unit roundoff (~1.2e-7 per op on unit
  vectors) and tight enough that no materially different direction can pass].
  All 60 items per run must pass. The code path's formula is read directly from
  source (E1 verifies the executor's reconstruction matches the *documented code
  path*, and E2 verifies that path is what actually executed — a two-link chain,
  neither link alone suffices).
- **Scale check:** ‖b‖ must equal the run's recorded injection norm: EXP065 unit
  (‖·‖=1); EXP066 unit; EXP070 0.50 (ALPHA=0.50); EXP077 0.50 (ALPHA_BRIDGE=0.50).
  Tolerance: relative error ≤ 1e-5.

**Null/alternative (E1):** H0: the code-constructed direction deviates from
normalize(E[target]−E[foil]) beyond tolerance (a different operator was used);
H1: it matches within tolerance.

**Power/feasibility:** deterministic (no sampling). Feasibility is guaranteed:
item token strings are in the run scripts' verbatim construction code (C-A
pre-audit precedent: items rebuilt verbatim, §0 of that audit); weight rows are
read-only reads.

### E2 — Code-trace provenance (Q1, deductive)

**Question (own words):** at which exact source lines do option-token rows enter the
bridge construction, and is there any alternative code path that could have built
the executed vectors label-free?

**Procedure (executor):** produce the evidence table (§3) with file:line for
(i) tokenization of the per-item target/foil label fields, (ii) unembedding-row
indexing by those token ids, (iii) the vector function call, (iv) the arm
evaluation wiring. Also grep for any second bridge-construction path (e.g., a
label-free fallback) in the four runner scripts and record its absence/presence.

**Null/alternative (E2):** H0: the executed call path never encodes a per-item
target/foil/option token (a label-free path executed); H1: the executed path
encodes the item's own target and foil labels at the pinned lines.

### E3 — Artifact consistency (Q1, records check)

**Question (own words):** do the archived run artifacts' records agree with the
construction the code documents?

**Honest boundary (stated now so the reviewer can judge):** no archived artifact
in the corpus records the per-item bridge vectors themselves —
[FACT — verified by inspection]:
- EXP065: `exp065_results.json` is aggregates-only (per the forensic-audit P3
  review, LOG-097 lineage: "EXP065's results_json is aggregates-only (no
  per-instance file written)").
- EXP066: `exp066_instance_evaluations.json` records per-item correctness and
  margin shifts per condition, not vectors; the script contains zero
  torch.save/np.save (same forensic finding).
- EXP077: `exp077_vectors.pt` archives v_hat, v_hat_c, mu, v_hats, u_list,
  w_list, q_list, r_vec, B_wrong, B_perp_basis, hashes — NOT the C8 bridge
  vectors (`run_exp077.py` ll. 993–999).
- EXP070: `exp070_vectors.pt` exists only in the Kaggle notebook outputs; no
  byte-identical repo mirror has been retrieved (LOG-110). Its contents
  (including whether C7 vectors are archived) are UNVERIFIED from the repo.

Therefore E3 is a *records-consistency* endpoint, not a vector-identity
endpoint, and a vector-vs-artifact identity claim is IMPOSSIBLE in principle for
EXP065/066/077 (not a compute limitation — see §6). The checks:

1. **EXP077 norm record:** the smoke run log
   (`experiments/runs/EXP077_cone_vs_line/exp077_run_log.txt`, log line 70)
   records "C8 bridge vectors: 60 per-item unembedding directions, min
   norm=0.5000 (all > 0)." [OBSERVATION]. The quoted norm record is from the
   smoke run log; the scale (0.5000 = ALPHA_BRIDGE) is construction-generic
   from code (`run_exp077.py` l. 118). Executor: the E1-rebuilt EXP077 vectors
   must have ‖b‖ = 0.5000 ± 1e-5 for all 60 items (matches the recorded
   record).
2. **(b,c) record fidelity:** the archived summary (b,c, ΔM) per run
   (EXP065: b=10,c=0,+16.67pp,p=0.001953; EXP066: b=8,c=0,+13.33pp,p=0.0078125;
   EXP070: b=10,c=0,+16.67pp,p=0.001953 per LOG-110) must match the primary
   JSONs exactly — already forensically recomputed (LOG-097-lineage); the
   executor re-verifies against the repo JSONs as a guard against artifact
   drift. For EXP077 the fidelity check is two pinned records, never one:
   (i) **Smoke record (in-repo):**
   `experiments/runs/EXP077_cone_vs_line/exp077_results.json` +
   `exp077_run_log.txt` — verify b=14, c=0, ΔM=+23.33pp, p=0.000122 and the
   log's "C8 bridge vectors: 60 per-item unembedding directions, min
   norm=0.5000 (all > 0)." (log line 70).
   (ii) **Official GPU record:** b=6, c=0, ΔM=+10.00pp, p=0.03125 per
   `reports/research_log.md` LOG-128 (2026-09-23); notebook-output artifacts
   recorded by sha256 in LOG-128 (`50a326a6…` / `de0b9c4a…` / `0c2e3552…` /
   `6918efcf…`) — official byte-identical mirror pending retrieval; LOG-128 is
   the cited record, mirror-pending disclosed (same disclosure pattern the plan
   already uses for EXP070).
   The smoke archive and the official record are two different runs and must
   never be cross-compared; a difference between them is EXPECTED and is not a
   record contradiction under E3.
3. **Item-definition identity:** the token strings used in the E1 rebuild must be
   the verbatim item label fields the executed code encoded (assert string
   equality, not just statistical plausibility).

**Null/alternative (E3):** H0: an archived record contradicts the construction
(e.g., recorded norms ≠ ALPHA-scale, or (b,c) ≠ JSON); H1: all available records
are consistent with the E1/E2 construction. Where no record exists (EXP070
vectors), the endpoint is **Underdetermined** for that run — never filled in by
assumption.

### E4 — Rescue attribution under §G1b (Q2, statistical re-analysis)

**Question (own words):** do the archived paired decision counts for each bridge
arm clear the binding practical-significance rule, and given Q1, what is the most
the rescues may license?

**Procedure (executor):** for each run's bridge arm vs its own baseline, take the
archived (b, c) counts (b = rescues wrong→correct, c = corruptions correct→wrong;
all four runs record c = 0). Compute Δ̂M = (b − c)/N and the **exact two-sided
95% confidence interval [L, U]** for the paired difference (McNemar-compatible
exact interval — the same interval family the §G1b protocol binds).

**Primary record pin (EXP077):** E4 uses the official GPU (b=6, c=0) as the
primary input for commensurability with the §G1b retrospective table; the smoke
(b=14, c=0) CI is reported as a labeled secondary [OBSERVATION] only, never
verdict-bearing. The §G1b table places the two records in different cells
(official → cell (4) Inconclusive; smoke → cell (1)), so the source must be
frozen.

**Decision parameters (inherited from the adopted §G1b protocol, not re-derived
here):** δ_min = 0.05 (5pp — the binding stats revision's practical-meaningfulness
margin, mentor finding #2); CI level = 95% exact two-sided.
**WHY these values:** the mentor's binding statistical revision requires
effect + CI + pre-registered margin in place of p-value reasoning, and §G1b binds
every primary comparison in the adopted synthesis to δ_min=0.05 with the exact
two-sided 95% CI. This audit must be commensurable with K1/K2/K3 verdicts — it
uses the same ruler by adoption, not by fresh derivation. [DEFINITION — binding
protocol]

**Per-run mapping (exhaustive, §G1b four-cell rule applied to the superiority
claim "the bridge rescues by a meaningful amount"):**
1. **L > δ_min → "meaningful rescue magnitude established"** (significance alone
   insufficient: p<0.05 with L ≤ δ_min is not meaningful).
2. **U < 0 → "genuinely negative"** (not expected; recorded for completeness).
3. **U < δ_min (U ≥ 0) → "meaningful rescue ruled out"** (equivalence-to-null at
   the practical margin; the only way a null becomes a negative finding).
4. **Otherwise (CI overlaps δ_min or covers 0 too widely) → Inconclusive** —
   the comparison is underpowered for the magnitude question; the rescue is
   HELD, never converted to a negative. Inconclusive is always reachable and is
   never re-labeled as evidence against the rescue.

**Attribution step (conditional on Q1 = Supported):** for any run in cell (1),
the licensed reading is the **narrow L1**: "the readout path is causally
accessible to an option-informed direction (label-assisted readout steering)."
[INFERENCE]/[INTERPRETATION]. The stronger "autonomous steerability" reading is
NOT licensed here — it requires the K1/K2 battery (which this audit neither
duplicates nor preempts). For runs in cell (3), the rescue magnitude is
practically ruled out. For runs in cell (4), attribution is suspended
(Inconclusive).

**Power/feasibility:** fully feasible — (b, c, N) are archived for all four runs
(EXP070's from the LOG-110 run record; primary mirror pending). The endpoint is
deterministic re-analysis; no sampling, no forward passes. The "power" question
is handled by the protocol itself: wide CIs map to Inconclusive, never to a
negative.

---

## 3. Code-trace evidence table (to be verified verbatim by the executor)

| Run | Construction lines | Token-encoding lines (target/foil label fields) | Vector-fn wiring | Bridge arm |
|---|---|---|---|---|
| EXP065 | `experiments/scripts/run_exp065_temporary_coordinate_alignment.py` ll. 485–487 (`make_bridge_vec`: `w = model.embed_out.weight[tt,:] − model.embed_out.weight[ft,:]`, unit-normalized) | ll. 406–407 (`t_tok`/`f_tok` ← `tokenizer.encode(item["target_token"])[0]`, `item["foil_token"]`; label fields set at ll. 258–259, 286–287, 315–316, 343–344 as `" " + true_target/foil`) | l. 420 (`v_vec = vector_fn(item, t_tok, f_tok)`) | ll. 483–491 (Condition 3 "Same-Layer Output Bridge (v_output at Layer 10)") |
| EXP066 | `experiments/scripts/run_exp066_pythia410m_replication.py` ll. 391–393 (identical formula) | ll. 408–409 (same encoding of `item["target_token"]`/`item["foil_token"]`) | l. 421 (`v_vec = vector_fn(item, t_tok, f_tok)`) | ll. 495–500 (Condition 3 "Same-Layer Output Bridge Control (Layer 20)") |
| EXP070 | `experiments/runs/exp070/run_exp070.py` ll. 659–661 (`make_bridge_vec`, `.detach()` variant, unit-normalized) | ll. 754–755 (`tt`/`ft` ← `tokenizer.encode(t["target_token"])[0]`, `t["foil_token"]`; inside `_c7_fn`, ll. 753–756) | l. 697 (`v = vec_fn(t)` via `eval_condition`, l. 693) | l. 752–757 (C7 "Same-layer output bridge (positive control)"; `ALPHA * make_bridge_vec(tt, ft)`, ALPHA=0.50 at l. 87) |
| EXP077 | `experiments/runs/exp077/run_exp077.py` ll. 725–729 (`make_bridge_vec`: `tt`/`ft` ← `tokenizer.encode(" " + item["A"])[0]`, `" " + item["C"]` — item A = correct answer, C = foil; `w = _E[tt,:] − _E[ft,:]`; returns `ALPHA_BRIDGE * normalize(w)`, ALPHA_BRIDGE=0.50 at l. 118) | ll. 726–727 (tokenization); `_E = model.get_output_embeddings().weight` at l. 724 | ll. 731–739 (F1 guard: per-item bridge norms asserted > 0, recorded) | ll. 765–772 (C8 "Output_Bridge", positive control, bridge-validity gate ΔM>0 AND p<0.05; comment header 765–767; run-arm statements 768–772) |

[All line references verified by direct read 2026-09-23. The executor re-verifies
each reference against the repo files (Law #2 guard against drift) and records any
mismatch as a deviation — see §8.]

**Critical provenance fact for the reviewer:** in all four runs the token ids are
derived from the item's OWN answer labels (`target_token`/`foil_token` set from
`true_target`/`true_foil` at construction; EXP077's `item["A"]` is documented in
the runner as "target = correct answer"). There is no support-bank, no
premise-only, and no donor intermediary in this code path — the bridge is
per-item and label-fed by construction. [FACT — code read]

---

## 4. Verdict mapping (five permitted categories only)

**Q1 verdict (from E1 ∧ E2 ∧ E3):**
- **Supported** iff E1 passes on all 60 items for all four runs AND E2's trace
  confirms the executed path encodes the per-item target/foil labels AND E3
  records are consistent (EXP070's E3 recorded as Underdetermined-conditional,
  which does not block Q1 — its code path and items are in-repo).
- **Refuted** iff E2 finds the executed path does not encode per-item labels, or
  E1's identity fails (a different operator executed). [This would overturn the
  §H6 [FACT] premise and must be reported as a correction to the synthesis.]
- **Inconclusive** iff E1/E2 are internally inconsistent in a way the tolerance
  cannot resolve (e.g., item definitions rebuilt ≠ items the run encoded —
  provenance ambiguity, not a negative).
- **Underdetermined** iff a load-bearing source is missing (e.g., a runner
  script absent from the repo). Multiple explanations remain compatible.

**Q2 verdict (conditional; only computed if Q1 = Supported):**
- **Supported** iff at least one run lands in E4 cell (1) (L > 0.05): the narrow
  L1 reading "label-assisted readout artifact" is the licensed attribution.
  [Evidentiary level: L1-narrow — "can improve inference" via a label-informed
  direction. NOT L2, NOT L3. No silent crossing.]
- **Not supported** iff every run lands in E4 cell (3) (U < 0.05): even the
  narrow artifact reading is ruled out at the practical margin.
- **Inconclusive** iff the discriminating runs land in E4 cell (4).
- **Underdetermined** iff archived (b,c) are unavailable for a run claimed in
  scope. **Refuted** is reachable for Q2 only if the recorded rescues are shown
  to be recording errors against the primary artifacts (E3 check) — otherwise
  Refuted is not an applicable cell for a re-analysis endpoint.

**Every load-bearing claim in the execution report carries:** verdict category
(one of the five above), evidentiary level (L0 = instrument provenance, L1 =
inference improvement, L2/L3 excluded by construction), and both label layers:
FACT/INFERENCE/HYPOTHESIS/SPECULATION atop the 10-label standard
([FACT]/[DEFINITION]/[HYPOTHESIS]/[CONJECTURE]/[ASSUMPTION]/[PROPOSITION]/
[THEOREM]/[OBSERVATION]/[INTERPRETATION]/[OPEN]).

---

## 5. Law #7 compliance criteria (operational definition)

**Law #7 (AGENTS.md):** "Never expose test set labels, targets, or future
instances to candidate representation generators or evaluation objectives."

**Operational compliance rule for a bridge construction (checkable, static):**
a construction is Law-#7-compliant iff a data-flow audit of the vector
construction function shows that NONE of its inputs is (a) a test item's target
answer, (b) a test item's foil / candidate-option tokens, (c) any test label, or
(d) any future instance. The audit is a symbol-provenance check: list every input
symbol of `make_bridge_vec`-equivalents and trace each to its source; compliance
requires every source to be one of: frozen model weights, item-unspecific
constants, or support/premise material provably carrying no per-item target
information (e.g., entity-disjoint donor banks with the disjointness proof
attached, C-A pattern).

**What a compliant reconstruction would have to look like (NOT built — building
is execution):** a per-item or bank-level direction constructed from
premise-entity tokens only (never the answer options), or from a donor item bank
with verified entity-disjointness from the test set and the entity-similarity-leak
control — i.e., the §H6-K3 falsifier's "premise-entity-tokens-only" construction.
Any reconstruction that encodes the item's own target/foil option tokens is
non-compliant by definition, regardless of downstream performance.

**Compliance verdict for the audited bridge:** if Q1 = Supported, the audited
construction is **non-compliant with Law #7 on the letter** (it encodes the
item's own target/foil option tokens per item). [INFERENCE]/[INTERPRETATION] over
E1/E2 [OBSERVATION]s. This licenses NO claim beyond §I condition 5: such a
construction cannot support an *autonomous* mechanism claim.

---

## 6. CPU-impossibility justification (§f)

**Claim:** every endpoint in this plan is answerable CPU-only with read-only
weight reads; nothing requires a forward pass or GPU.

**Proof by endpoint:**
- E1: pure linear algebra on unembedding rows (read-only tensor indexing +
  cosine). Precedent: G1 executed 48-head projection-energy audits CPU-only in
  41 s; the C-A pre-audit did full weight-only centroid/similarity/permutation
  analysis with zero forward passes.
- E2: static source inspection — no compute at all.
- E3: JSON/log record comparison — no compute beyond parsing.
- E4: exact binomial/McNemar interval arithmetic on archived integers — no
  model contact.

**What cannot be answered without forward passes — and why it is out of scope:**
(i) whether the archived decisions would replicate under re-execution
(causal replication ≠ construction provenance; re-running signed experiments is
prohibited and unnecessary for the provenance question); (ii) whether a
Law-#7-compliant reconstruction would rescue (that IS the §H6-K3 falsifier —
execution, gated on K1 survival, not this audit). A forward pass cannot
distinguish "label-assisted" from "steerable" — that discrimination is K1/K2's
geometric/interventional job. Therefore no GPU is requested, and no GPU is
authorized in this step regardless.

**Δθ=0 guard:** SHA-256 over the loaded parameters pre and post (verbatim
`get_hash` procedure, G1/C-A precedent); must equal the archived
`ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`.
Any mismatch = FATAL, results not reported (Law #6).

---

## 7. Relation to K1/K2 (scoping against the §H6 battery)

- **K1(a)** asks the *geometric* question: cos(bridge direction, unembedding row
  of t_target) ≥ 0.9 — is the direction, as a vector, a target boost
  (readout tilt)? **This audit does NOT compute K1(a), does not verdict it, and
  the executor is forbidden from drawing any K1-style conclusion from the
  reconstructed vectors.** If a cosine is computed incidentally as an E1 sanity
  check, it is reported as [OBSERVATION] flagged "K1-owned — no verdict drawn."
- **The question this audit answers that K1(a) does not:** construction
  **provenance** — WHERE in the code the option rows enter (file:line, §3),
  whether the archived rescues were produced *with* those rows (E2/E3), and
  whether the construction is Law-#7-compliant (Q1/§5). K1(a) can tell you the
  direction *is* a target boost; only this audit can tell you the program
  *built it from the answer key* — the fact that makes the §I-5 and Law #7
  consequences bite.
- **K2** (bypass-vs-routing, needs a pilot run) is untouched by this audit.
- **No K3 verdict is drawn here** (interpretation order: no K3 verdict before
  K1 rules). Q2's attribution is explicitly the *narrow* reading and stops
  short of the K3 kill ("output-side program re-scoped").

---

## 8. Positive-control status — RECOMMENDATION rule (auditor reports; CEO decides per §H7)

Deterministic mapping from audit verdicts to a recommendation on the bridge's
positive-control status for EXP080/081. The auditor recommends; the CEO decides.
Signed protocols EXP065/066/070/077 are immutable — this plan proposes no edits
to them (per the repo correction law, any correction proposal goes to the user
separately).

| Audit outcome | Recommendation to CEO |
|---|---|
| Q1 = **Supported** and any run in E4 cell (1) | **DEMOTE (recommended):** the bridge is a label-informed instrument. Retain at most as a *rescue-capability control* ("the apparatus can detect causal effects" — the EXP070 LOG-110 license), explicitly relabeled as "rescue control (known-answer direction), NOT a mechanism control." Its positive-control status for EXP080/081's autonomous-mechanism questions should be revoked or replaced with a label-free control, subject to K1's verdict (if K1 confirms readout bias, demotion is mandatory; if K1 surprisingly exonerates, the CEO may revisit). |
| Q1 = **Supported** and no run in E4 cell (1) | **RETAIN-WITH-RELABELING (recommended):** relabel as "bridge rescue control — magnitude below the practical margin; mechanism unproven; K1 pending." No EXP080/081 clearance may cite the bridge as positive evidence of steerability. |
| Q1 = **Refuted** | **RETAIN (recommended):** the option-informed premise is overturned; the bridge's positive-control status stands as written, K1/K2 proceed as scheduled, and the §H6 [FACT] premise is corrected in the synthesis. |
| Q1 = **Inconclusive** or **Underdetermined** | **HOLD (recommended):** provenance unresolved — no EXP080/081 GPU clearance may rest on the bridge's positive-control status until the provenance resolves or K1 rules. Escalate the blocker to the CEO with the K1-first interpretation order noted. |

---

## 9. Execution protocol (for the later step; the reviewer judges this now)

1. **Environment pin:** `/home/hatch/workspace/.venv_smoke` (torch 2.14.0+cpu,
   transformers 5.17.0, numpy 2.5.3) — the G1/C-A-pre-audit venv. No other
   interpreter.
2. **Model load (read-only, verbatim G1/C-A procedure):** local HF snapshot
   `/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`,
   `AutoModelForCausalLM`, `torch_dtype=torch.float32`, `local_files_only`,
   `trust_remote_code=False`, `model.eval()`. No forward pass at any point.
3. **Δθ=0 guard:** SHA-256 pre = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
   (archived G1/C-A value); post must match; mismatch = FATAL, no report.
4. **E2 first:** verify every file:line in §3 against the repo; record the
   evidence table; grep the four runner scripts for any second bridge path.
5. **E1:** rebuild per-item bridge vectors weight-only per run (verbatim token
   encodings from §3); assert |cos| ≥ 1−1e-6 vs the documented code formula and
   the per-run norm scale (1.0 / 1.0 / 0.5 / 0.5, rel. err ≤ 1e-5).
6. **E3:** (a) EXP077: all 60 rebuilt norms = 0.5000 ± 1e-5 vs the run-log
   record; (b) re-verify archived (b,c,ΔM) against the repo JSONs
   (EXP065 `exp065_results.json`, EXP066 `exp066_replication_results.json`;
   EXP070 from the LOG-110 run record with primary-mirror-pending disclosed);
   for EXP077, two pinned records never cross-compared: smoke (in-repo)
   `experiments/runs/EXP077_cone_vs_line/exp077_results.json` +
   `exp077_run_log.txt` (b=14, c=0, ΔM=+23.33pp, p=0.000122) and official GPU
   (b=6, c=0, ΔM=+10.00pp, p=0.03125 per `reports/research_log.md` LOG-128;
   notebook-output artifacts recorded by sha256 in LOG-128
   (`50a326a6…` / `de0b9c4a…` / `0c2e3552…` / `6918efcf…`), byte-identical
   mirror pending retrieval; LOG-128 is the cited record). The smoke archive
   and the official record are two different runs and must never be
   cross-compared; a difference between them is EXPECTED and is not a record
   contradiction under E3; (c) assert verbatim item-label string identity.
   Record EXP070's vector-consistency cell as Underdetermined.
7. **E4 (only if Q1 = Supported):** exact two-sided 95% CIs on ΔM from archived
   (b,c); classify per the §G1b four-cell rule with δ_min = 0.05; apply the
   attribution step. Report per-run (b, c, Δ̂M, [L, U], cell, attribution).
8. **Report:** machine-readable results JSON twin (unrounded values) +
   verdicts per §4 with L0/L1 levels and both label layers on every
   load-bearing claim. Recommendation per §8. **No K1/K2/K3 verdicts.**
9. **Frozen-plan discipline:** any deviation from this protocol (different
   tolerance, added endpoint, environment change, re-derived δ_min) is a
   logged bundle deviation and INVALIDATES the frozen plan; execution may not
   proceed past the deviation without a fresh Law #14 sign-off (Law #4 —
   never silently shift the audit).

---

## 10. Reviewer checklist (what Law #14 must confirm)

- [ ] Q1/Q2 and all four endpoint H0/H1 are stated in the auditor's own words
  (not inherited from a summary).
- [ ] E1's tolerance (ε=1e-6, norm rel. err ≤ 1e-5) is judged adequate.
- [ ] δ_min = 0.05 and the exact two-sided 95% CI are accepted as the inherited
  §G1b ruler (adoption, not derivation).
- [ ] Inconclusive is reachable in E4 and is never converted to a negative.
- [ ] The plan draws no K1(a) verdict, no K2 verdict, and no K3 kill verdict.
- [ ] The §8 mapping is a recommendation (CEO decides per §H7); no signed
  protocol is proposed for editing.
- [ ] The §6 CPU-impossibility justification holds; no GPU authorized.
- [ ] EXP070's vector-consistency cell is honestly marked Underdetermined
  (notebook mirror pending), not assumed.
- [ ] The compliant-reconstruction sketch (§5) is a description, not a build.

**Disposition (reviewer):** SIGN / SIGN-WITH-FIXES / INCONCLUSIVE / REJECT.
