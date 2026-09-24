# Law #7 Bridge Construction Compliance Audit — EXECUTION REPORT

**LOG-197 · Track-8 Experimental Statistician (Executor) · 2026-09-23**
**Plan:** `research/analysis_plans/LAW7_BRIDGE_AUDIT_PLAN_LOG197_2026-09-23.md` (FROZEN, Law #14 SIGN — initial SIGN-WITH-FIXES, fixes applied, targeted re-verification SIGN)
**Execution:** per §9 verbatim. CPU-only. Zero forward passes. Read-only weight tensor reads.
**Deliverables:** this report + machine-readable twin `research/analysis_plans/LAW7_BRIDGE_AUDIT_RESULTS_LOG197_2026-09-23.json` (unrounded values).

**Battery-scope banner:** this audit does NOT compute K1(a), does NOT verdict it, and draws NO K1/K2/K3-style conclusion from the reconstructed vectors. It answers construction provenance and Law #7 compliance only. [DEFINITION — binding scope]

---

## 0. Execution guards (pre/post)

| Guard | Value |
|---|---|
| Environment | `/home/hatch/workspace/.venv_smoke`: torch **2.14.0+cpu**, transformers **5.17.0**, numpy **2.5.3** — asserted in-script, all exact [OBSERVATION] |
| Model load | pinned snapshot `.../models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`, `local_files_only`, `trust_remote_code=False`, `torch_dtype=torch.float32`, `model.eval()`; **no forward pass executed at any step** [FACT] |
| Δθ=0 pre-hash | `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` == archived (`manifest.model_hash_live`, re-confirmed from `G1_RESULTS_2026-09-23.json` at runtime) [FACT] |
| Δθ=0 post-hash | `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — match; Law #6 satisfied [FACT] |
| Hash procedure | verbatim `get_hash` (SHA-256 over concatenation of `state_dict()` tensors, sorted keys, CPU, float32 bytes — `run_exp077.py` ll. 166–172) [DEFINITION] |

**Deviation log:** one entry, D1 (F3-class, non-blocking): the frozen plan's §3 table lists EXP070's encoding lines as ll. 754–755 / `_c7_fn` ll. 753–756 / C7 arm ll. 752–757; actual: `tt` l. 755, `ft` l. 756, `_c7_fn` def ll. 754–757, C7 arm ll. 753–758. Substantive claims confirmed verbatim; corrected lines recorded in the E2 table below. **Not a bundle deviation** — no tolerance, endpoint, environment, or margin changed; execution proceeded per §9 step 4's verbatim re-verification rule (the same self-correction the Law #14 reviewer licensed for F3). No other deviations. [FACT]

---

## 1. E1 — Construction-algebra identity (Q1, deterministic) — PASS

**Method [FACT]:** for each run, 60 items rebuilt from verbatim ports of the runners' item-construction code; token ids via `tokenizer.encode(" " + label)[0]` exactly as the runners call it; rows fetched from the read-only unembedding matrix (`model.get_output_embeddings().weight` — the identical matrix the runners' `model.embed_out.weight` names; `embed_out` does not exist under transformers 5.17, and LOG-114/115 established the accessor returns the identical matrix [FACT]). Side A = executor reconstruction; side B = literal transcription of each runner's `make_bridge_vec` lines. Scale per plan: EXP065 1.0, EXP066 1.0, EXP070 0.50 (`ALPHA`), EXP077 0.50 (`ALPHA_BRIDGE`).

| Run | Items | min \|cos(sideA, sideB)\| over 60 (tolerance ≥ 1−1e-6) | max norm rel. err (tolerance ≤ 1e-5) | norm range | Verdict |
|---|---|---|---|---|---|
| EXP065 | 60 | 1.0000000 | 1.192e-07 | [1.000000, 1.000000] | PASS |
| EXP066 | 60 | 1.0000000 | 1.192e-07 | [1.000000, 1.000000] | PASS |
| EXP070 | 60 | 1.0000000 | 1.192e-07 | [0.500000, 0.500000] | PASS |
| EXP077 | 60 | 1.0000000 | 1.192e-07 | [0.500000, 0.500000] | PASS |

All 240 per-item checks pass both the algebraic-identity tolerance and the scale check. [FACT — computed]

**Item-definition identity (§2 E3 check c) [FACT]:** the rebuilt per-item label strings are byte-identical across all four runners' item definitions (60/60 each: EXP066 == EXP065, EXP070 == EXP065, EXP077 (A, C) == EXP065 (target, foil)). All 10 benchmark entities verified single-token under the pinned snapshot tokenizer (no silent-truncation hazard of the LOG-111 class).

**Load-bearing provenance fact (E2-adjacent) [FACT — code read]:** the executed runners pin different models — EXP065 `model_name = "EleutherAI/pythia-160m"` (l. 77), EXP066 `"EleutherAI/pythia-410m"` (l. 78), EXP070 `MODEL_NAME = "EleutherAI/pythia-160m"` (l. 83), EXP077 `"EleutherAI/pythia-410m"` (l. 101). The frozen protocol's §9 step 2 loads pythia-410m only and was followed verbatim. Consequence, stated plainly: E1's first link is executor self-consistency against the documented formula (already disclosed in-plan: "neither link alone suffices"); the rebuilt vectors are numerically the 410m-matrix instantiations, not byte-copies of the executed EXP065/070 (160m) numerics. The as-executed claim rides on E2 (the traced path, including its model pin) + E3 (records). This is recorded as an observation, not a deviation — the protocol was executed exactly as frozen. [OBSERVATION]/[INTERPRETATION]

**E1 verdict: PASS** — the code-constructed direction is `normalize(E[target] − E[foil])` (scaled per run) on the letter of the traced formulas. [FACT]

---

## 2. E2 — Code-trace provenance (Q1, deductive) — CONFIRMED

37/37 line assertions pass against the repo files (direct read, §9 step 4). [FACT]

| Run | Construction | Token encoding (per-item target/foil label fields) | Label-field definitions | Vector-fn wiring | Bridge arm |
|---|---|---|---|---|---|
| EXP065 | ll. 485–487: `w = model.embed_out.weight[tt,:] − model.embed_out.weight[ft,:]`, unit-normalized | ll. 406–407: `t_tok`/`f_tok` ← `tokenizer.encode(item["target_token"])[0]`, `item["foil_token"]` | ll. 258–259, 286–287, 315–316, 343–344: `"target_token": " " + true_target`, `"foil_token": " " + true_foil` | l. 420: `v_vec = vector_fn(item, t_tok, f_tok)` | ll. 483–491: `lambda item, tt, ft: make_bridge_vec(tt, ft)` (Condition 3, Layer 10) |
| EXP066 | ll. 391–393: identical formula | ll. 408–409: same encoding of `item["target_token"]`/`item["foil_token"]` | ll. 251–252, 279–280, 308–309, 336–337: same `" " + true_target/foil` fields | l. 421: `v_vec = vector_fn(item, t_tok, f_tok)` | ll. 495–500: `lambda item, tt, ft: make_bridge_vec(tt, ft)` (Condition 3, Layer 20) |
| EXP070 | ll. 659–661: `.detach()` variant, unit-normalized | ll. 755–756: `tt`/`ft` ← `tokenizer.encode(t["target_token"])[0]`, `t["foil_token"]` (inside `_c7_fn`, def ll. 754–757) | l. 382 (`_add`): `"target_token": " " + target, "foil_token": " " + foil`; C7 iterates `final_instances` (l. 506; probe map 60/60 per LOG-110, so final == test) | l. 697: `v = vec_fn(t)` via `eval_condition` (l. 693) | ll. 753–758: `return ALPHA * make_bridge_vec(tt, ft)`, `results["C7_Output_Bridge"] = eval_condition("C7_Output_Bridge", _c7_fn)`; ALPHA=0.50 (l. 87) |
| EXP077 | ll. 725–729: `tt`/`ft` ← `tokenizer.encode(" " + item["A"])[0]`, `" " + item["C"]` (comments: "target = correct answer" / "foil"); `w = _E[tt,:] − _E[ft,:]`; `return ALPHA_BRIDGE * normalize(w)`; `_E = model.get_output_embeddings().weight` (l. 724); ALPHA_BRIDGE=0.50 (l. 118) | ll. 726–727 (same lines) | ll. 600/613/623/636: `"A": A, "C": C` (`"C": D_ent` for 3-hop); A=target, C=foil documented at l. 588; A/C are the evaluated answer options (`eval_item(it["prompt"], it["A"], it["C"])`, l. 707; correct ⟺ chosen == A, ll. 708–710) | ll. 731–739: F1 guard (per-item bridge norms asserted > 0, recorded) | ll. 765–772: comment header 765–767, `run_arm("C8_Output_Bridge", bench, make_bridge_vec, log_file)` at l. 768 |

**Second-path grep [FACT]:** exactly one `make_bridge_vec` definition exists in each runner (EXP065 l. 485; EXP066 l. 391; EXP070 l. 659; EXP077 l. 725). No label-free fallback bridge path exists. The other `embed_out.weight` reads in EXP065/066 (ll. 176–197, 384–390) belong to the Procrustes E_0/E_k/E_inst machinery feeding Conditions 1–2, not the bridge arm.

**E2 verdict: CONFIRMED** — the executed call path in all four runs encodes each item's OWN target and foil option tokens and indexes the unembedding rows by them; no support bank, no premise-only, no donor intermediary in this path. [FACT — code read, L0]

---

## 3. E3 — Artifact consistency (Q1, records check) — CONSISTENT

**(a) EXP077 norm record [OBSERVATION]:** smoke run log (`experiments/runs/EXP077_cone_vs_line/exp077_run_log.txt`, line 70) records "C8 bridge vectors: 60 per-item unembedding directions, min norm=0.5000 (all > 0)." — matches verbatim. The 60 rebuilt EXP077 norms are all 0.5000 ± 1e-5 [FACT — computed]. Stronger, at per-item resolution: the smoke archive records all 60 per-item C8 bridge norms (`injection_vector_norms.C8_bridge_item{i}`); max |rebuilt − archived| = **1.192e-07** ≤ 1e-5 [FACT — computed]. The scale (0.5000 = ALPHA_BRIDGE) is construction-generic from code (`run_exp077.py` l. 118); the log record is smoke-run-specific.

**(b) (b, c, ΔM, p) fidelity [FACT — records]:**

| Run | Archived record (primary JSON) | Plan-pinned expectation | Match |
|---|---|---|---|
| EXP065 | `exp065_results.json` → `stage_B_confirmatory_results.Same_Layer_Output_Bridge`: b=10, c=0, ΔM=0.1667, p=0.001953125 | 10/0/+16.67pp/0.001953 | YES |
| EXP066 | `exp066_replication_results.json` → `stage_B_conditions.Same_Layer_Output_Bridge`: b=8, c=0, ΔM=0.1333, p=0.0078125 | 8/0/+13.33pp/0.0078125 | YES |
| EXP077 smoke (in-repo) | `exp077_results.json` → `stage_B_conditions.C8_bridge`: b=14, c=0, ΔM=0.2333, p=0.0001220703125; `bridge_gate` agrees; run-log line 78 agrees | 14/0/+23.33pp/0.000122 | YES |
| EXP070 | cited from `reports/research_log.md` LOG-110: b=10, c=0, ΔM=+16.67pp, p=0.001953 (primary notebook mirror pending retrieval — disclosed) | 10/0/+16.67pp/0.001953 | YES (log-cited) |
| EXP077 official GPU | cited from `reports/research_log.md` LOG-128: b=6, c=0, ΔM=+10.00pp, p=0.03125 (notebook-output sha256 `50a326a6…`/`de0b9c4a…`/`0c2e3552…`/`6918efcf…`; byte-identical mirror pending — disclosed) | 6/0/+10.00pp/0.03125 | YES (log-cited) |

The smoke archive and the official record are two different runs and were never cross-compared; their difference is expected and is not a record contradiction. [DEFINITION — standing invariant]

**(c) Vector-consistency cells:** no archived artifact records per-item bridge vectors for EXP065/066/077 (aggregates-only / correctness-only / archive-dict-without-bridge-vectors — the plan's honest-boundary facts, re-confirmed) [FACT]. EXP070's vector-consistency cell is **Underdetermined** (no byte-identical repo mirror of `exp070_vectors.pt`; recorded, never filled by assumption).

**E3 verdict: CONSISTENT** — no archived record contradicts the E1/E2 construction. [FACT, L0]

---

## 4. E4 — Rescue attribution under §G1b (Q2, statistical re-analysis)

**Ruler [DEFINITION — binding protocol]:** exact two-sided 95% CI for the paired difference + δ_min = 0.05, adopted from §G1b (not re-derived). **Method identification [FACT — computed]:** the binding §G1b sensitivity table's CIs are Tango's (1998) score interval for the paired difference — verified by reproducing all five table rows to 4dp ([+0.0931,+0.2803], [+0.0651,+0.2417], [+0.0338,+0.2015], [+0.1444,+0.3544]) before use. (Clopper–Pearson, Wilson, Jeffreys, Agresti–Coull do not reproduce the table; Tango does exactly.)

**Primary pin:** EXP077 uses the official GPU record (b=6, c=0) per the frozen E4 pin; the smoke CI is a labeled secondary [OBSERVATION], never verdict-bearing.

| Run (primary) | (b, c, N) | Δ̂M | Tango 95% CI [L, U] | §G1b cell | Attribution |
|---|---|---|---|---|---|
| EXP065 | (10, 0, 60) | +0.1667 | [+0.0931, +0.2803] | **(1)** L > δ_min — meaningful rescue magnitude established | narrow L1 licensed |
| EXP066 | (8, 0, 60) | +0.1333 | [+0.0651, +0.2417] | **(1)** L > δ_min — meaningful rescue magnitude established | narrow L1 licensed |
| EXP070 | (10, 0, 60) | +0.1667 | [+0.0931, +0.2803] | **(1)** L > δ_min — meaningful rescue magnitude established | narrow L1 licensed |
| EXP077 official | (6, 0, 60) | +0.1000 | [+0.0338, +0.2015] | **(4)** — CI excludes 0 (directional) but does not clear δ_min; overlaps δ_min → **Inconclusive**, HELD, never converted to a negative | attribution suspended |
| EXP077 smoke (secondary) | (14, 0, 60) | +0.2333 | [+0.1444, +0.3544] | (1) — reported as [OBSERVATION] only | none (non-verdict-bearing) |

All numbers [FACT — computed]. Inconclusive is reachable and was reached (EXP077 official); it is not re-labeled as evidence against the rescue.

---

## 5. Verdicts

### Q1 — construction provenance: **Supported**

E1 passes on all 60 items for all four runs (min |cos| = 1.0000000 ≥ 1−1e-6; norm rel. err 1.192e-07 ≤ 1e-5) [FACT] ∧ E2's trace confirms the executed path encodes the per-item target/foil labels at the pinned lines with no alternative path [FACT] ∧ E3 records are consistent (EXP070's vector cell Underdetermined-conditional, which per the frozen mapping does not block Q1 — its code path and items are in-repo) [FACT]. Evidentiary level: **L0** (instrument provenance). Therefore: the bridge construction, as implemented and as executed in EXP065/066/070/077, is built from target/foil option-token unembedding rows — **option-informed on the letter of Law #7**. [INFERENCE over E1/E2 [OBSERVATION]s]

### Law #7 compliance: **non-compliant on the letter**

Under the §5 operational rule (a construction is compliant iff no input symbol is a test item's target answer, foil/candidate-option tokens, test label, or future instance), the audited construction fails: every input symbol of `make_bridge_vec` traces to the item's own target/foil option tokens. [INFERENCE]/[INTERPRETATION, L1-narrow]. This licenses NO claim beyond §I condition 5: such a construction cannot support an *autonomous* mechanism claim. [DEFINITION — binding]

### Q2 — rescue attribution (conditional on Q1 = Supported): **Supported**

Three runs land in E4 cell (1) (L > 0.05): EXP065, EXP066, EXP070 [FACT — computed]. Per the frozen mapping, the licensed reading is the **narrow L1**: "the readout path is causally accessible to an option-informed direction (label-assisted readout steering)." [INFERENCE]/[INTERPRETATION, L1-narrow — "can improve inference" via a label-informed direction; NOT L2, NOT L3; no silent crossing]. The stronger "autonomous steerability" reading is NOT licensed here — it requires the K1/K2 battery, which this audit neither duplicates nor preempts. EXP077 official sits in cell (4): Inconclusive — attribution suspended, held, never converted to a negative.

**Refuted is not applicable to Q2** (no recorded rescue was shown to be a recording error against the primary artifacts — E3 fidelity holds). [FACT]

---

## 6. §8 positive-control status — RECOMMENDATION (auditor reports; CEO decides per §H7)

**Outcome → mapping:** Q1 = **Supported** and three runs in E4 cell (1).

> **DEMOTE (recommended):** the bridge is a label-informed instrument. Retain at most as a *rescue-capability control* ("the apparatus can detect causal effects" — the EXP070 LOG-110 license), explicitly relabeled as "rescue control (known-answer direction), NOT a mechanism control." Its positive-control status for EXP080/081's autonomous-mechanism questions should be revoked or replaced with a label-free control, subject to K1's verdict: if K1 confirms readout bias, demotion is mandatory; if K1 surprisingly exonerates, the CEO may revisit. [INTERPRETATION — recommendation, not a verdict]

Signed protocols EXP065/066/070/077 are untouched by this audit; no correction is proposed to them here (any correction proposal goes to the user separately per the repo correction law). [FACT]

---

## 7. Notes for the record

1. **Model-pin observation (E2-adjacent) [FACT]:** EXP065 and EXP070 executed on `EleutherAI/pythia-160m`; EXP066 and EXP077 on `EleutherAI/pythia-410m` (runner-pinned, ll. cited in §2). The frozen §9 step 2 loads pythia-410m only — followed verbatim. E1 is therefore an algebraic-identity check of the documented formula (self-consistency link, disclosed in-plan), not an independent numeric measurement of the executed 160m vectors; the as-executed claim rides on E2 + E3. The formula itself is model-independent.
2. **CI-method identification [FACT — computed]:** the binding §G1b "exact" interval is Tango's (1998) score CI — established by reproducing the synthesis table to 4dp before use, not assumed.
3. **E3 strengthening [OBSERVATION]:** the smoke archive records all 60 per-item C8 bridge norms; rebuilt-vs-archived max |diff| = 1.192e-07.
4. **Open (not blocking):** EXP070 `exp070_vectors.pt` byte-identical mirror pending retrieval (vector-consistency Underdetermined); EXP077 official notebook-output mirror pending retrieval (LOG-128 is the cited record). [OPEN]
5. **What this audit does not touch:** K1(a) (not computed, not verdictable here), K2, K3 kill verdict, compliant-bridge reconstruction (the §H6-K3 falsifier — execution, gated on K1 survival). [DEFINITION — binding scope]

---

*Executor: Track-8 (LOG-197). No GPU. No forward passes. Δθ=0 pre/post verified. One F3-class table-precision correction logged (D1); no bundle deviations. Report ends; the CEO decides per §H7.*
