# K3 Phase-0 — Construction Audit: EXECUTOR HALT REPORT

**LOG-238 · Implementation track (Executor) · 2026-09-23**
**Plan:** `research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md` (§10 Phase-0 steps, worked verbatim in order)
**License:** Law #14 SIGN of the plan (released for Phase-0 execution ONLY; Phase 1 NOT released — the §8 G9 chain is not satisfied)
**Cost:** $0 CPU. Forward passes: 0. GPU: dark. RNG consumed: none.
**Evidentiary level:** L0 (instrument provenance) — the Phase-0 geometric/compliance endpoints (L1) were never reached.

---

## Headline

[FACT] K3 Phase-0 **halted at §10 step 2 on a FATAL G4** (label/premise cross-check):
the verbatim-ported bench's per-item `(ent, typ)` matched the archived
`exp077_instance_records.json` `(ent, typ)` on only **12/60** index-aligned items
(**48 mismatches**; first mismatch at index 1 — rebuilt `Venus/planet` vs archived
`Mars/planet`). Per §8 G4 ("any item mismatch vs archived per-item records =
FATAL"), execution stopped: **no verdict, reported**. Per the §7.1 table's
guard-fail row, both candidates land **Refuted (integrity failure; halt; no claim
licensed)**; per §9, REFUTED means **no verdict is licensed — the CEO decides**.
The construction question ("does a Law-#7-compliant bridge construction exist
that is well-defined, statically compliant, and non-degenerate?") is **not
answered** — this is a halt, not an Underdetermined verdict. Phase-0 endpoints
E-K3-1 through E-K3-4 were **not executed**. The GPU phase was not reached; the
§8 G9 release chain is untouched.

[INFERENCE] The halt is a plan-premise defect, not a construction defect: the
executor's port is independently verified byte-faithful to the pinned
construction (60/60 agreement with the signed pre-audit per-item records —
§3 D1, [OBSERVATION], non-gating). The outlier is the archive, not the port.

---

## 1. §10 execution record (steps 1–2; steps 3–7 not reached)

**Step 1 — environment + model load + G3 pre-hash.** [FACT] Environment asserted
exact: `/home/hatch/workspace/.venv_smoke`, torch 2.14.0+cpu, transformers
5.17.0, numpy 2.5.3, scipy 1.18.1 (script hard-asserts all four; any deviation
would have aborted before the model load). [FACT] Model loaded read-only:
`EleutherAI/pythia-410m` @ `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`
(`local_files_only=True`, `trust_remote_code=False`, `torch_dtype=torch.float32`,
`model.eval()`; pinned snapshot resolved from the local HF cache — nothing
downloaded, nothing substituted). [FACT] G3 pre-hash via the verbatim
`run_exp077.py` ll.166–172 formulation (SHA-256 over concatenation of
`state_dict()` tensors, sorted keys, CPU, float32 bytes):
`ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` ==
archived hash — **PASS**. (Note: transformers 5.17 emits a `torch_dtype`
deprecation warning; the LOG-109 pin stands per LOG-3381 m4 — behavior
unchanged, dtype float32 confirmed.)

**Step 2 — bench port + G6 + G4.** [FACT] The four bench-construction loops were
ported verbatim from `run_exp077.py` ll.586–636 (constants `TRIPLES_INDICES`,
`QUADS_INDICES`, `NOVEL_VOCAB_PLANET/ELEMENT` copied exactly; loop bodies
byte-identical modulo the runner's `log()` calls). Quad-loop sub-ranges
(recorded per plan §1): planet_2hop items 0–14, planet_3hop 15–29,
element_2hop 30–44, element_3hop 45–59; 60 items total; per-item `(B_i, C_i,
target_i=A, foil_i=C)` rebuilt. Ported target distribution: planet
{Mars: 21, Venus: 7, Jupiter: 2}, element {Iron: 21, Gold: 7, Silver: 2}.
[FACT] G6 (F2 single-token guard): all 35 entities (25 pinned donor entities
per EXP081 v2 §3.1 + 10 test entities) encode as exactly 1 token under
`" "+entity` — **PASS**. [FACT] G4: index-aligned byte comparison of rebuilt
`(ent, typ)` vs the archived per-item records → **12/60 matches, 48
mismatches → FATAL**. [OBSERVATION, non-gating] Descriptive port
self-consistency vs the signed `C-A_PREAUDIT_2026-09-23.json`
`similarity_audit.per_item` (id → (t, f)): **60/60 byte-agreement** — the port
is faithful to the pinned construction; see §3 D1. [FACT] G5: runtime
self-scan of the executor's own source found **0** forward-pass call sites
outside the allowlist (`from_pretrained`, `state_dict()`,
`get_output_embeddings()`, `model.eval()`, `get_hash`) — **PASS**; 0 forward
passes executed. [FACT] G3 post-hash:
`ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` —
pre == post == archived → **Δθ=0 confirmed across the halted run**.

**Steps 3–7 — NOT EXECUTED** (halted at step 2 per §8). E-K3-1 (compliance
audit), E-K3-2 (non-degeneracy g), E-K3-3 (identity), E-K3-4 (geometric
profile) have no values; no candidate vector was constructed.

---

## 2. Guards G1–G11 (FATAL as specified)

| Guard | Outcome |
|---|---|
| G1 static-audit executability | NOT REACHED (halted at step 2) |
| G2 identity tolerances | NOT REACHED (E-K3-3 not attempted) |
| G3 Δθ=0 | **PASS** — pre == post == archived `ec276abe…e0ed` (verbatim ll.166–172 formulation) |
| G4 label/premise cross-check | **FATAL** — 12/60 index-aligned (ent,typ) byte-matches; 48 mismatches (§3) |
| G5 no forward pass | **PASS** — code self-scan: 0 call sites; 0 forward passes executed |
| G6 single-token | **PASS** — 35/35 entities single-token as `" "+entity` |
| G7 pair-norm floors | NOT REACHED |
| G8 Phase-1 pins | N/A (Phase 1 not released) |
| G9 release chain | NOT SATISFIED — not invoked; Phase 1 does not exist |
| G10 budget cap | N/A — 0 forward passes |
| G11 Tango method identity | N/A (Phase-1 guard) |

---

## 3. Plan-premise defect found in execution (asset, not failure)

**D1 — G4's archive premise is false as written.** [FACT] The plan's §2 premises
the G4 cross-check on "EXP077 smoke `exp077_instance_records.json` ent/typ
fields" with the justification "LOG-197 established the runners' item
definitions are byte-identical 60/60." Both halves of the justification fail
on the evidence:

1. The in-repo archive is the **pre-MAJOR-3-repair smoke**: its records carry
   `(b,c) = (14,0)` for C8_bridge vs C1 (recomputed from the records —
   the plan's "in-repo JSON: b=14,c=0" smoke), and its per-item ents are
   **entity-grouped** (planet: Mars×6, Venus×6, Jupiter×6, Saturn×6, Mercury×6;
   element: Iron×6, Gold×6, Silver×6, Bronze×6, Steel×6). [FACT — counted from
   the archive]
2. The pinned bench construction (post-repair `run_exp077.py` ll.586–636)
   yields planet targets {Mars: 21, Venus: 7, Jupiter: 2} — Saturn and Mercury
   are never targets. [FACT — counted from the verbatim port]
3. No index alignment, reordering, or multiset comparison can reconcile the
   two: Saturn×6/Mercury×6 as archived *targets* vs zero as ported targets is a
   structural bench difference, not a transcription slip. First mismatch at
   index 1 (`exp077_planet_2hop_1`: rebuilt Venus/planet vs archived
   Mars/planet); 48/60 mismatched in total.
4. Provenance: LOG-3378 MAJOR-3 found the smoke-run bench was "a novel
   construction (Anglo subjects, 'visited/forged' templates), not the
   EXP065-identical 2-hop/3-hop suite"; LOG-3381 replaced the benchmark builder
   with the EXP065/066-identical suite ported from EXP078 — the construction
   the K3 plan pins. The repair smoke wrote to `/tmp` (ephemeral); the in-repo
   archive was never refreshed. EXP082's D2 independently established the same
   entity-grouped vs 21/7/2/0/0 divergence [FACT, re-verified here].
5. LOG-197's byte-identity sentence (research_log.md line 39) covers "the
   rebuilt per-item label strings … across all four runners' item definitions"
   — i.e., the runners' *current* (post-repair) definitions — not the smoke
   archive. The K3 plan mis-scoped that claim onto the archive.

[INFERENCE] G4 as specified is unsatisfiable: no correct executor can make the
pinned (post-repair) construction byte-match the pre-repair smoke archive.
The failure is in the plan's cross-check source selection, not in the
construction, the port, or the archive (the archive is a faithful record of
the bench its run actually used — Law #8 preserved it correctly).

**D1 corollary (the repair direction).** [OBSERVATION] The signed
`C-A_PREAUDIT_2026-09-23.json` `similarity_audit.per_item` records (id, t, f)
for all 60 items — attached to the signed EXP081 v2 spec — agree byte-for-byte
with the ported bench (60/60). A G4 repointed at that signed per-item record
would discharge A1. Per Law #4, repointing the guard is a new plan (or a Law
#14 ruling amending this one) — not an executor improvisation; the executor
did not substitute it.

---

## 4. §7.1 verdict table (filled verbatim from the plan)

| E-K3-1 compliance | E-K3-2 (g ≥ 0.25) | E-K3-3 identity | Guards | Per-candidate verdict |
|---|---|---|---|---|
| — (not executed) | — (not executed) | — (not executed) | **FAIL (G4 FATAL)** | **(i) premise-rank bank: Refuted (integrity failure; halt; no claim licensed)** |
| — (not executed) | — (not executed) | — (not executed) | **FAIL (G4 FATAL)** | **(ii) donor centroid: Refuted (integrity failure; halt; no claim licensed)** |

"Refuted" here carries exactly the plan's §7.1 row-5 meaning — *integrity
failure; halt; no claim licensed* — and §9's consequence: **no verdict**.
Nothing about either candidate's compliance, degeneracy, or identity was
measured; no negative on the construction question is licensed.

---

## 5. §9 pre-registered consequences (quoted; the executor does not interpret past them)

- **REFUTED (either phase):** "no verdict; executor reports the integrity failure; CEO decides. Nothing downstream moves on a refuted measurement."
- The construction question is **not answered** (this is a halt, not the
  Underdetermined cell — Underdetermined requires the Phase-0 endpoints to have
  been measured with no Supported candidate).
- The GPU phase was **not reached**; the §8 G9 chain (plan SIGN ∧ Phase-0
  report ∧ re-verification SIGN ∧ CEO GPU clearance ∧ BK-04 booking) is
  untouched. No GPU spend is authorized or needed by this outcome.
- The §H7 narrowed demotion, EXP081's queue position, and all Sprint-3 pilots
  are **unchanged** — nothing downstream moves on a refuted measurement.

---

## 6. L1 mathematical license — readout-shift lemma (stated; no promotion claimed)

[THEOREM] (plan §6 L1; K1 §6 L1; EXP082 §6 L1 — cited, not re-proved) Let
W_U ∈ ℝ^{V×d} be the frozen unembedding matrix, x ∈ ℝ^d the final-token
residual, ℓ = W_U x (+ constant bias, immaterial: Δℓ is bias-independent).
For unit v̂ ∈ ℝ^d, scalar α, token y: the perturbation x ← x + αv̂ shifts the
y-logit by **Δℓ_y = α·(W_U[y,:]·v̂) = α‖W_U[y,:]‖₂·cos(v̂, ŵ_y)**,
ŵ_y = W_U[y,:]/‖W_U[y,:]‖₂. *Proof:* Δℓ = W_U(αv̂); take the y-th row. ∎

No measurement in this halted run promotes or demotes any license grade. The
Phase-0 algebra+compliance checks remain IN-HOUSE-PROOF-eligible only upon a
successful re-execution under a repaired plan; the Phase-1 causal upshot
remains CONJECTURE-UNDER-TEST (A2 undischarged).

**Assumption inventory (L4) status:** A1 (item/premise labels) — port
verified verbatim, but its plan-specified discharge (G4) failed on the
archive premise; the descriptive 60/60 pre-audit agreement is recorded as
[OBSERVATION], not as a discharge. A3 (run pins incl. Δθ=0) — discharged via
G3 tri-match. A4 (EXP070 excluded) — honored (nothing from EXP070 touched).
A5/A6 (binary scoring, α/l\*/hook/dtype pins) — Phase-1-scoped, untouched.
A2 (mid-network propagation) — undischarged, carried as [CONJECTURE].

---

## 7. Deliverables

1. Executor script:
   [K3_construction_audit_execute_LOG234_2026-09-23.py](sandbox://workspace/SCBI/research/analysis_plans/K3_construction_audit_execute_LOG234_2026-09-23.py)
   — G5 asserted by runtime self-scan (0 forward-pass call sites; §2 table).
   Exits 42 on the G4 FATAL path.
2. This report:
   [K3_PHASE0_HALT_REPORT_LOG238_2026-09-23.md](sandbox://workspace/SCBI/research/analysis_plans/K3_PHASE0_HALT_REPORT_LOG238_2026-09-23.md)
3. Machine-readable twin:
   [K3_CONSTRUCTION_AUDIT_RESULTS_LOG234_2026-09-23.json](sandbox://workspace/SCBI/research/analysis_plans/K3_CONSTRUCTION_AUDIT_RESULTS_LOG234_2026-09-23.json)
   — env manifest, pre/post/archived hashes, bench port (ids/targets/foils),
   guard outcomes, full 48-mismatch G4 evidence, descriptive pre-audit
   agreement, endpoint sections marked NOT_EXECUTED.

No signed artifact was modified. No `reports/research_log.md` entry was
written (the Lead owns the log). No GPU was spent.

---

## 8. Recommended repair (for the CEO / Law #14 reviewer — not executed)

1. **Re-register K3 Phase-0 under a new plan number** (Law #4) with G4's
   cross-check source repointed from the pre-repair smoke archive to the
   signed `C-A_PREAUDIT_2026-09-23.json` `similarity_audit.per_item`
   (id, t, f) records — 60/60 byte-agreement with the pinned construction
   demonstrated in this run's twin JSON. Everything else in the frozen plan
   (endpoints, tolerances, guards G1–G3/G5–G11, §7 tables) can carry over
   verbatim.
2. Alternatively, a Law #14 ruling may amend G4's source in place — the
   executor takes no position on which vehicle the CEO prefers.
3. Do **not** repair by editing the smoke archive (Law #8 — it faithfully
   records its run's bench) or by weakening G4 to a non-fatal check (the
   cross-check is load-bearing for A1).

*Executor: LOG-238 · 2026-09-23 · Standup: no verdict in hand — the plan's own
guard caught a false premise before any measurement. The bench port is
verified faithful (60/60 vs the signed pre-audit); the archive it was told to
match predates the repair that created the bench. Recommend the re-registered
Phase-0 with G4 repointed; the $0 CPU gate can then run to completion.*
