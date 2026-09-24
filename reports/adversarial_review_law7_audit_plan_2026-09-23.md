# Law #14 Adversarial Review — Law #7 Bridge Audit Plan (LOG-197)

**Reviewer:** Track-7 independent Law #14 reviewer · **no prior involvement** in the Law #7 bridge audit or its plan
**Target:** `research/analysis_plans/LAW7_BRIDGE_AUDIT_PLAN_LOG197_2026-09-23.md` (frozen plan, 420 lines)
**Date:** 2026-09-23
**Disposition: SIGN-WITH-FIXES** (1 major fix required before execution; 2 minor)
**Compute used:** none — read-only file inspection, no weights loaded, no forward passes, no signed artifacts modified.

**Rule of this review:** the plan-writer's claims are untrusted. Every code-trace line range, every artifact claim, and every (b,c) number was re-verified against the repo files independently.

---

## Method

Read in full: the plan; `research/synthesis/SYNTHESIS_A_J_REV2_2026-09-23.md` §G1b (lines 1269–1343), §H6 (K1/K2/K3 ordering), §H7 (open CEO decision); `research/synthesis/CLUSTER_A_2026-09-23.md` §6 CHALLENGE (lines 470–558); `research/analysis_plans/G1_REPORT_2026-09-23.md`; the 14 Laws (`~/workspace/SCBI/AGENTS.md` §2); the five permitted verdict categories and FACT/INFERENCE/HYPOTHESIS/SPECULATION layer (`research/MENTORSHIP_DIRECTIVE.md`, lines 373–391 and 43–46).

Spot-checked against source (no execution):
- All four §3 code-trace line ranges against the actual runner scripts via `sed`/`grep`.
- Artifact claims against primary JSONs/logs: `experiments/runs/EXP065_coordinate_alignment/exp065_results.json`, `EXP066_pythia410m_replication/exp066_instance_evaluations.json` + `exp066_replication_results.json`, `EXP077_cone_vs_line/exp077_results.json` + `exp077_run_log.txt`, and `research/reports/research_log.md` (LOG-110, LOG-128).
- Environment pin: ran `/home/hatch/workspace/.venv_smoke/bin/python -c` version check; verified HF snapshot path and the SHA-256 guard hash against `research/analysis_plans/G1_RESULTS_2026-09-23.json`.
- Grep for banned verdict language across the plan.

---

## Checklist results

### 1. COMPLETENESS — PASS

All eight required sections are present and substantive:
- (a) §1 — Q1/Q2 stated formally with own-words H0/H1 (plus per-endpoint H0/H1 in §2).
- (b) §2 — E1–E4 each have an own-words question, an executor procedure, exact tolerances (ε=1e-6; norm rel. err ≤ 1e-5; δ_min=0.05; exact two-sided 95% CI).
- (c) §4 — kill criteria mapped to the five verdict categories for Q1 and Q2 separately.
- (d) §5 — operational Law #7 compliance rule (static symbol-provenance audit).
- (e) §7 — scoping against K1/K2/K3 with the binding interpretation order.
- (f) §6 — CPU-impossibility justification, proof-by-endpoint.
- (g) §8 — deterministic verdict→recommendation mapping, explicitly recommendation-only.
- (h) §9 — frozen execution protocol (env pin, Δθ=0 guard, step order, deviation discipline).
Bonus: §10 reviewer checklist is itself a completeness guard.

### 2. ENDPOINT SOUNDNESS — PASS (with a ruled disclosure and one fix-forcing caveat)

**E1 tolerance (ε=1e-6).** Justified in-plan as arbitrary-but-reasoned: float32 linear algebra on 1024-dim unit-ish vectors, tolerance ~10³× float32 unit roundoff, and tight enough that any materially different direction (cos ≤ 0.999999 ↔ angle ≳ 0.08°) fails. Independent judgment: probative AND safe. The executor computes both sides with identical tensor ops, so the comparison is dominated by exact reproducibility, not accumulation noise; 1e-6 is generous slack on a bit-reproducible computation and strict against any genuinely different operator. Norm tolerance (rel. err ≤ 1e-5) is consistent with the recorded scales (1.0 / 1.0 / 0.5 / 0.5). **PASS.**

One honest caveat I note but do not fail: E1's first link (reconstruction vs code-formula) is executor self-consistency, not an independent measurement — the probative weight rides on E2 (the traced path is what executed) + E3 (norm records). The plan discloses this two-link structure explicitly ("neither link alone suffices"). Not oversold. No fix needed.

**E4 / δ_min = 0.05 "inherited-not-derived" — RULED ACCEPTABLE, not a defect.** The §G1b text (REV2 synthesis, lines 1269–1300) deliberately freezes δ_min as treatment-independent ("frozen before NTDP data contact and held constant across all comparisons — margin-shopping after data contact is forbidden"; the LOG-191 correction removed the bridge-anchored wording). §H6 binds the battery to the §G1b decision protocol ("All verdicts per the §G1b decision protocol"), and K2 applies the same rule to retrospective-style comparisons. This audit sits inside §H6's battery preparation; adopting the identical ruler is the commensurable choice, and the writer disclosed the adoption explicitly ("by adoption, not by fresh derivation", tagged [DEFINITION — binding protocol]). Re-deriving a margin inside the audit would itself be margin-shopping risk. The mentor's finding #2 (effect + CI + pre-registered margin in place of p-value reasoning) is satisfied in full. **The inheritance is licensed; the disclosure is the correct handling.**

**Exact two-sided 95% CI.** Matches the §G1b universal primary-comparison rule verbatim ("exact two-sided 95% confidence interval [L, U] for the paired difference"). The plan names the interval family (McNemar-compatible exact interval) and leaves computation to the executor — the same delegation pattern the G1/C-A precedents used. **PASS.**

**Inconclusive reachability.** Verified reachable at every level: Q1 (provenance ambiguity), E4 cell (4) (CI overlaps δ_min or covers 0 too widely → Inconclusive, "never converted to a negative"), Q2 (cell (4)), E3 (EXP070 vector-consistency cell explicitly Underdetermined, never filled by assumption). **PASS.**

**Caveat (feeds the MAJOR fix below):** E4's record source is NOT pinned. The synthesis's own §G1b sensitivity table gives the EXP077 **official** bridge CI [+0.0338, +0.2015] ("directional only" — does NOT clear δ_min=0.05 → cell (4) → Inconclusive) and the EXP077 **smoke** bridge CI [+0.1444, +0.3544] (clears → cell (1) → meaningful). The record choice is verdict-determinative for EXP077 and must be frozen in the plan. Currently E4 says only "the archived (b, c) counts". See Fix F1.

### 3. VERDICT HYGIENE — PASS

- All verdicts in §4 use exactly the five permitted categories (Supported / Not supported / Inconclusive / Underdetermined / Refuted), matching `MENTORSHIP_DIRECTIVE.md` lines 373–391.
- Grep for "promising", "interesting", "worth another experiment", "mechanistically elegant", "novel" (as verdict): **zero hits**. The plan's language ("rescue-capability control", "positive-control status") is about instrument status, never a verdict substitute.
- EXP070's vector cell is honestly marked Underdetermined ("no byte-identical repo mirror has been retrieved (LOG-110)"); I verified independently via `find` that no `exp070_vectors*` file exists anywhere in the repo. The downgrade is correct, not a gap: E1's weight-only rebuild uses in-repo item definitions (test_instances at `run_exp070.py` l. 376, probe_map built in-script at ll. 463–481, zero external loads), so the missing mirror does not block the provenance question.
- Missing-artifact handling is sound: impossibility is stated as principled (vectors never archived for EXP065/066/077), not as a compute limitation, and E3 is correctly scoped as records-consistency, not vector-identity.

### 4. BATTERY SCOPE — PASS

- §7 contains an explicit executor ban: "This audit does NOT compute K1(a), does not verdict it, and the executor is forbidden from drawing any K1-style conclusion from the reconstructed vectors." §9 step 8: "No K1/K2/K3 verdicts." §8's table draws no K3 kill verdict — Q2's attribution is explicitly "the *narrow* reading and stops short of the K3 kill."
- The question the plan answers that K1(a) does not is stated precisely: "construction **provenance** — WHERE in the code the option rows enter (file:line, §3), whether the archived rescues were produced *with* those rows (E2/E3), and whether the construction is Law-#7-compliant (Q1/§5). K1(a) can tell you the direction *is* a target boost; only this audit can tell you the program *built it from the answer key*." No leakage across the battery boundary. The interpretation order (no K2/K3 verdict before K1 rules) is preserved, while parallel preparation is exercised — exactly what §H6 permits. **PASS.**

### 5. LAW #7 CRITERIA — PASS

- The operational rule (§5) is checkable by construction audit: "list every input symbol of `make_bridge_vec`-equivalents and trace each to its source; compliance requires every source to be one of: frozen model weights, item-unspecific constants, or support/premise material provably carrying no per-item target information." No test labels, no target answers, no candidate-option tokens — verifiable statically from the §3 trace. **PASS.**
- The compliant-reconstruction sketch is genuinely a sketch: "(NOT built — building is execution)". It describes the shape a compliant construction would have to take; it does not design, name hyperparameters for, or pre-commit to any build. Not a smuggled design. **PASS.**

### 6. CPU-FIRST HONESTY — PASS

- §6 is proof-by-endpoint, not assertion: E1 = read-only tensor indexing + cosine (G1 precedent: 48-head audit CPU in 41 s); E2 = static inspection; E3 = JSON/log parsing; E4 = exact interval arithmetic on archived integers. Each endpoint's sufficiency argument names the specific artifact or code property that makes forward passes unnecessary.
- The honest out-of-scope boundary is stated: re-execution replication and the compliant-bridge falsifier both require forward passes and are explicitly out of scope here (the latter is the gated K3 falsifier). "A forward pass cannot distinguish 'label-assisted' from 'steerable' — that discrimination is K1/K2's geometric/interventional job." Correct scoping.
- §9 authorizes no GPU and no forward pass at any step; the model load is read-only (`local_files_only`, `trust_remote_code=False`, `model.eval()`, "No forward pass at any point"). Δθ=0 guard included with the archived hash `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`, which I verified appears in `G1_RESULTS_2026-09-23.json`. **PASS.**

### 7. DECISION SCOPE — PASS

- §8 is framed strictly as recommendation: "The auditor recommends; the CEO decides." All four rows are labeled "(recommended)". The DEMOTE row correctly conditions on K1 ("if K1 confirms readout bias, demotion is mandatory; if K1 surprisingly exonerates, the CEO may revisit") — the §H7 open decision is respected, not preempted.
- "Signed protocols EXP065/066/070/077 are immutable — this plan proposes no edits to them." No design change, no silent edit. **PASS.**

### 8. EXECUTION RIGOR — PASS with qualification

- SHA-256 Δθ=0 guards: present, pre and post, with the archived value independently verified in the G1 results JSON. Mismatch = FATAL, no report (Law #6). **PASS.**
- Artifact paths: named exactly (`exp065_results.json`, `exp066_replication_results.json`, `exp077_results.json`; EXP070 via LOG-110 record with mirror-pending disclosed). **PASS.**
- Frozen-plan deviation discipline: "any deviation from this protocol ... is a logged bundle deviation and INVALIDATES the frozen plan; execution may not proceed past the deviation without a fresh Law #14 sign-off (Law #4)." **PASS.**
- venv/pinning: `/home/hatch/workspace/.venv_smoke` with torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3 — I executed the version check; all three match exactly. HF snapshot path exists on disk. **PASS.**
- Qualification: the E3/E4 record-pinning gap (Fix F1) is an execution-rigor defect — it is the one item that could make the executor trip or misfire.

---

## Code-trace spot-check (independent re-verification of the §3 table)

| Run | Claim | Verified |
|---|---|---|
| EXP065 | ll. 485–487 `make_bridge_vec` = normalize(E[tt]−E[ft]) | **CONFIRMED** — l. 485 `def`, l. 486 `w = model.embed_out.weight[tt,:] - model.embed_out.weight[ft,:]`, l. 487 `return w / (torch.norm(w) + 1e-12)` |
| EXP065 | ll. 406–407 encoding `item["target_token"]`/`item["foil_token"]` | **CONFIRMED** |
| EXP065 | label fields ll. 258–259, 286–287, 315–316, 343–344 (`" " + true_target/foil`) | **CONFIRMED** (all four) |
| EXP065 | l. 420 vector-fn wiring; ll. 483–491 Condition 3 arm | **CONFIRMED** |
| EXP066 | ll. 391–393 identical formula | **CONFIRMED** |
| EXP066 | ll. 408–409 encoding; l. 421 wiring | **CONFIRMED** |
| EXP070 | ll. 659–661 `make_bridge_vec` (`.detach()` variant) | **CONFIRMED** |
| EXP070 | ll. 754–755 encoding inside `_c7_fn` (def at 753) | **CONFIRMED** |
| EXP070 | l. 697 `v = vec_fn(t)` via `eval_condition` l. 693; ll. 752–757 C7 arm; ALPHA=0.50 l. 87 | **CONFIRMED** |
| EXP070 | probe_map/item construction in-script, no external loads | **CONFIRMED** (ll. 463–481; zero `json.load`/`torch.load`/`pickle` in the runner) |
| EXP077 | ll. 725–729 `make_bridge_vec(item, i)`: `tt`/`ft` from `" " + item["A"]`/`" " + item["C"]`, `_E[tt,:]−_E[ft,:]`, `ALPHA_BRIDGE * normalize(w)` | **CONFIRMED** (`_E = model.get_output_embeddings().weight` at l. 724; ALPHA_BRIDGE=0.50 at l. 118) |
| EXP077 | ll. 731–739 F1 guard (norms asserted > 0, recorded) | **CONFIRMED** |
| EXP077 | ll. 765–773 C8 arm | **APPROXIMATE** — the run-arm code is at ll. 768–772 with the Gate-2 comment header at 765–767; the range is close but not exact (non-blocking; §9 step 4's verbatim re-verification self-corrects — see Minor F3) |
| EXP077 | ll. 993–999 archive dict lacks C8 bridge vectors | **CONFIRMED** — keys are v_hat, v_hat_c, mu, v_hats, v_hat_c_ks, u_list, w_list, q_list, r_vec, B_wrong, B_perp_basis, pre_hash, post_hash; no bridge vectors |

## Artifact-number spot-check

- EXP065 `exp065_results.json`: aggregates-only (no vector-ish keys at any depth); Same_Layer_Output_Bridge: b=10, c=0, ΔM=+16.67pp, p=0.001953125. **Matches the plan.**
- EXP066 `exp066_instance_evaluations.json`: per-item correctness + margin shifts, no vectors. `exp066_replication_results.json` Same_Layer_Output_Bridge: b=8, c=0, ΔM=+13.33pp, p=0.0078125. **Matches the plan.**
- EXP070: C7 b=10, c=0, +16.67pp, p=0.001953 per LOG-110 (research_log.md line ~3339); mirror-pending and "no unverified transcription kept as a primary" both disclosed. **Matches the plan.**
- EXP077 run log line 70: "C8 bridge vectors: 60 per-item unembedding directions, min norm=0.5000 (all > 0)." **Matches the plan.** But see the MAJOR defect: this is the **smoke** run's log.

---

## Defect register

### MAJOR F1 — E3 check 2 / §9 step 6 conflate the EXP077 smoke archive with the official GPU record

**The plan's text (§2 E3 check 2):** "the archived summary (b,c, ΔM) per run (EXP065: b=10,c=0,+16.67pp,p=0.001953; EXP066: b=8,c=0,+13.33pp,p=0.0078125; EXP070: b=10,c=0,+16.67pp,p=0.001953 per LOG-110; **EXP077 official GPU: b=6,c=0,+10.00pp,p=0.03125) must match the primary JSONs exactly** — already forensically recomputed (LOG-097-lineage); **the executor re-verifies against the repo JSONs** as a guard against artifact drift."

**What the repo actually contains (verified by direct read):**
- `experiments/runs/EXP077_cone_vs_line/exp077_results.json` → C8_bridge: **b=14, c=0, ΔM=+23.33pp, p=0.000122** (`/stage_B_conditions/C8_bridge`, `/bridge_gate` agree; run log line 78 agrees: "C8 output bridge: accuracy 0.8333 (50/60), delta_m=+23.33pp (b=14, c=0), p=0.000122").
- This is the **CPU smoke** archive (LOG-118/LOG-123: full CPU launch, EXIT 0, artifacts written to `EXP077_cone_vs_line/`).
- The official GPU numbers (b=6, c=0, +10pp, p=0.03125) exist **only** in `reports/research_log.md` LOG-128 (line ~3387) and in the un-retrieved Kaggle notebook outputs (sha256 recorded in LOG-128: `50a326a6…`, `de0b9c4a…`, `0c2e3552…`, `6918efcf…`). A filesystem-wide search confirms **no official EXP077 results JSON exists in the repo**.

**Consequence:** an executor following the plan verbatim compares (6, 0, +10pp, 0.03125) against the repo JSON (14, 0, +23.33pp, 0.000122), finds a mismatch, and — per the plan's own E3 null/alternative ("H0: an archived record contradicts the construction") — must log a record contradiction. Worse, the plan makes "Refuted reachable for Q2 only if the recorded rescues are shown to be recording errors against the primary artifacts (E3 check)" — a false E3 contradiction could therefore launder into a spurious Q2=Refuted. The defect is execution-blocking: the executor will either misfire or halt.

This also regresses on a standing Law #14 finding: the paper-rewrite re-review (LOG-156, recorded in research_log.md) **required** the GPU-vs-smoke provenance distinction (official +10pp/b=6 vs smoke +23.33pp/b=14) to never be conflated. The plan conflates them in its fidelity check.

**Related:** E4 says "take the archived (b, c) counts" without pinning which record. The synthesis's §G1b sensitivity table assigns the two records different verdict cells — official CI [+0.0338, +0.2015] is "directional only" (does NOT clear δ_min → E4 cell (4) → Inconclusive); smoke CI [+0.1444, +0.3544] clears → E4 cell (1). The record choice is verdict-determinative for EXP077's Q2 contribution and must be frozen pre-execution.

### MINOR F2 — §10 disposition line omits INCONCLUSIVE

The plan's final line reads "Disposition (reviewer): SIGN / SIGN-WITH-FIXES / REJECT." The standing disposition set used by Law #14 reviews in this program (and in this task's own instructions) is SIGN / SIGN-WITH-FIXES / INCONCLUSIVE / REJECT. A reviewer who finds the plan unjudgeable should not be boxed into SIGN or REJECT. Mechanical fix: add INCONCLUSIVE.

### MINOR F3 — §3 EXP077 bridge-arm line range is approximate (non-blocking)

"ll. 765–773 (C8 'Output_Bridge' ...)" — the actual run-arm statements are at ll. 768–772 (comment header at 765–767). §9 step 4 requires the executor to re-verify every file:line verbatim and log mismatches as deviations, so this self-corrects at execution; no verdict rides on it. Tighten the range or leave it — the executor's verbatim check governs.

---

## Required fixes (mechanical — the writer executes, the reviewer does not rewrite)

**F1 (MAJOR — execution may not proceed until applied).** In §2 E3 check 2 and §9 step 6(b), replace the single EXP077 fidelity check with two pinned records:
1. **Smoke record (in-repo):** `experiments/runs/EXP077_cone_vs_line/exp077_results.json` + `exp077_run_log.txt` — verify **b=14, c=0, ΔM=+23.33pp, p=0.000122** and the log's "C8 bridge vectors: 60 per-item unembedding directions, min norm=0.5000 (all > 0)." (log line 70).
2. **Official GPU record:** **b=6, c=0, ΔM=+10.00pp, p=0.03125** per `reports/research_log.md` LOG-128 (2026-09-23); notebook-output artifacts recorded by sha256 in LOG-128 (`50a326a6…` / `de0b9c4a…` / `0c2e3552…` / `6918efcf…`) — official byte-identical mirror pending retrieval; LOG-128 is the cited record, mirror-pending disclosed (same disclosure pattern the plan already uses for EXP070).
3. Add the prohibition sentence: "The smoke archive and the official record are two different runs and must never be cross-compared; a difference between them is EXPECTED and is not a record contradiction under E3."
4. In §2 E4, pin the primary record: "E4 uses the **official GPU** (b=6, c=0) as the primary input for commensurability with the §G1b retrospective table; the smoke (b=14, c=0) CI is reported as a labeled secondary [OBSERVATION] only, never verdict-bearing." Include the one-line rationale: the §G1b table places the two records in different cells (official → cell (4) Inconclusive; smoke → cell (1)), so the source must be frozen.
5. In §2 E3 check 1, qualify: the quoted norm record is from the smoke run log; the scale (0.5000 = ALPHA_BRIDGE) is construction-generic from code (`run_exp077.py` l. 118).

**F2 (MINOR).** §10 final line → "Disposition (reviewer): SIGN / SIGN-WITH-FIXES / INCONCLUSIVE / REJECT."

**F3 (MINOR, optional).** §3 EXP077 row: tighten "ll. 765–773" to "ll. 765–772 (comment header 765–767; run-arm statements 768–772)".

**After F1–F3 are applied:** the plan returns for a targeted Law #14 re-verification of the fixed lines only (per the plan's own §9 Law #4 discipline, any deviation — including a fix — needs fresh sign-off before execution). No GPU, no weights, no signed artifacts are touched by the fixes.

---

## Disposition: SIGN-WITH-FIXES

The plan is structurally sound — complete, endpoint-rigorous, verdict-hygienic, battery-scoped, Law-#7-operational, CPU-honest, decision-scoped, and execution-disciplined — with one blocking defect: the EXP077 record-fidelity check conflates the smoke archive with the official GPU record and would make the executor misfire, with a possible spurious path to Q2=Refuted. That is exactly the class of assumption-laundering this gate exists to catch. Fix F1 mechanically per the instructions above; F2/F3 are editorial. Execution is not released until the fixes are re-verified.

---

## Standup for the Research Lead

**What I did.** Independently re-verified the entire LOG-197 plan against primary sources: read all four runner scripts at the claimed line ranges (every construction formula, encoding line, label-field definition, and arm wiring), read all four experiments' primary JSONs/logs, checked the (b,c,ΔM,p) numbers, confirmed the venv pin and snapshot path on disk, confirmed the Δθ=0 hash in the G1 results JSON, and grepped the plan for banned verdict language. No weights loaded, no code executed, nothing signed touched.

**What surprised me.** Two things. First, the plan is unusually well-built for a first draft — the writer anticipated most of my attacks (the EXP070 Underdetermined downgrade, the two-link E1/E2 honesty, the "inherited-not-derived" disclosure on δ_min, the explicit K1/K2/K3 ban). Second, the one real defect is a provenance conflation the program already learned once: the LOG-156 paper-rewrite review forced the GPU-vs-smoke distinction (+10pp/b=6 vs +23.33pp/b=14) into the paper, and this plan regressed on it in E3/E4. Institutional memory worked in review but not in drafting — worth noting for the Lead's process notes.

**What remains uncertain.** Whether the plan-writer intended E4's primary record to be the official GPU numbers (my recommended pin) or something else — the plan as written doesn't say, and the choice flips EXP077 between E4 cell (4)/Inconclusive and cell (1)/meaningful, which feeds Q2. This is precisely why F1 must freeze it pre-execution rather than leave it to executor judgment.

**What I need.** Nothing from the Lead beyond the standard loop: the writer applies F1–F3 mechanically, and the fixed lines come back for a targeted re-verification before any execution. I also flag for the CEO's awareness (not a plan defect): the official EXP077 notebook-output mirror (sha256 `50a326a6…` etc., per LOG-128) is still un-retrieved; until it is, the official record rests on the LOG-128 log entry alone.

**Verdict:** **SIGN-WITH-FIXES** — release execution only after F1 is applied and re-verified.


---

## Addendum — Targeted Re-verification of Fixed Lines (2026-09-23)

**Reviewer:** same track-7 Law #14 reviewer (independent; no prior involvement in the Law #7 audit or plan)
**Scope:** the fixed lines only — §2 E3 check 1, §2 E3 check 2, §2 E4 primary pin, §9 step 6(b), §10 disposition line, §3 EXP077 row — against the fix specification ("Required fixes (mechanical)" F1–F3 in this file's Defect register), plus a scope-discipline spot-check for out-of-spec alterations and an internal-consistency pass. Read-only; no weights, no code execution, no GPU, no signed artifacts touched.

### Per-item re-verification

| Fix | Check | Result |
|---|---|---|
| F1.5 (§2 E3 check 1) | Norm record explicitly sourced to the smoke run log (`experiments/runs/EXP077_cone_vs_line/exp077_run_log.txt`, log line 70); 0.5000 scale qualified as construction-generic from code (`run_exp077.py` l. 118) | **PASS** — both elements present verbatim as specified |
| F1.1 (§2 E3 check 2) | Pinned smoke record: in-repo JSON + run log, b=14, c=0, ΔM=+23.33pp, p=0.000122, log line 70 norm quote | **PASS** — numbers and citations match the review's independently verified ground truth |
| F1.2 (§2 E3 check 2) | Pinned official GPU record: b=6, c=0, ΔM=+10.00pp, p=0.03125 per `reports/research_log.md` LOG-128 (2026-09-23); notebook sha256 hashes cited (`50a326a6…` / `de0b9c4a…` / `0c2e3552…` / `6918efcf…`); mirror-pending disclosed | **PASS** — all elements present; disclosure pattern matches the plan's existing EXP070 treatment |
| F1.3 (§2 E3 check 2) | Never-cross-compare prohibition sentence | **PASS** — present verbatim ("The smoke archive and the official record are two different runs and must never be cross-compared; a difference between them is EXPECTED and is not a record contradiction under E3") |
| F1.4 (§2 E4) | Primary record pinned to official GPU (b=6, c=0) for §G1b commensurability; smoke CI as labeled secondary [OBSERVATION] only, never verdict-bearing; one-line rationale (two records land in different §G1b cells, so the source must be frozen) | **PASS** — all elements present verbatim |
| F1 (§9 step 6(b)) | Same two-record replacement with the prohibition sentence; EXP065/066/070 checks unchanged (`exp065_results.json`, `exp066_replication_results.json`, EXP070 from LOG-110 record, mirror-pending disclosed) | **PASS** — EXP065/066/070 clauses byte-identical to the pre-fix plan; old conflated sentence fully removed |
| F2 (§10 final line) | Disposition line reads "SIGN / SIGN-WITH-FIXES / INCONCLUSIVE / REJECT" | **PASS** |
| F3 (§3 EXP077 row) | Bridge-arm range tightened to "ll. 765–772 (comment header 765–767; run-arm statements 768–772)" | **PASS** — matches the review's independent line verification |

### Scope discipline

Spot-checked the surrounding sections for unintended alterations: §2 E1 (tolerance, scale check, null/alternative), §2 E2 (procedure, null/alternative), §2 E4 procedure paragraph + decision parameters + four-cell mapping + attribution step, §4 verdict mapping, §5 Law #7 criteria, §6 CPU-impossibility, §7 battery scoping, §8 recommendation table, §9 steps 1–5 / 7–9 (env pin, Δθ=0 guard, step order, frozen-plan discipline), §10 checklist items, and the §2 E3 "Honest boundary" artifact facts. All are unchanged from the version this review originally passed. **No substantive change outside the F1–F3 fix spec was found.**

**Ruling on the prohibition-sentence duplication (§2 + §9):** ACCEPTABLE. Both instances state the same rule with the same scope ("under E3"); neither creates ambiguity, and the redundancy is harmless because the prohibition is a standing invariant the executor must not violate at either step.

### Consistency

E3's two-record structure flows correctly into E4's pinned primary record (the pin paragraph sits immediately after the procedure paragraph and disambiguates EXP077 before any decision parameter is applied). No remaining sentence conflates the smoke archive with the official record or invites the executor to cross-compare them. §9 step 7's "archived (b,c)" for EXP077 resolves through the §2 E4 pin to the official record; step 6(b) establishes both records with their distinct provenance. The F1.5 qualification (norm record = smoke-run; scale = construction-generic) is consistent with §9 step 5's per-run norm-scale rule, since the scale is code-generic (ALPHA_BRIDGE, `run_exp077.py` l. 118) rather than record-specific.

**Disposition: SIGN — execution released.** The fixed plan resolves the blocking defect (the false E3 contradiction path and the spurious route to Q2=Refuted are eliminated) and freezes the verdict-determinative record choice pre-execution. No further fixes required.
