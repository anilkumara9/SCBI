# K3 Phase-0 R1 — Construction Audit + Rescue Screen Gate: EXECUTOR REPORT

**LOG-241 · Implementation track (Executor) · 2026-09-23**
**Plan:** `research/analysis_plans/K3_PHASE0_R1_PLAN_LOG239_2026-09-23.md` (Phase-0 §10 steps 1–6, worked verbatim)
**License:** Law #14 SIGN = LOG-240 (R1 Phase-0 released; Phase 1 NOT released — the §8 G9 chain is unsatisfied)
**Cost:** $0 CPU. Forward passes: 0. GPU: dark. RNG consumed: none.
**Evidentiary level:** L0 (instrument provenance) / L1 (weight-algebra geometry). No L2/L3 crossing.

---

## Headline

[FACT] Both pinned Law-#7-compliant bridge constructions are well-defined, statically compliant, and non-degenerate: **candidate (i) premise-rank bank direction — Supported** (E-K3-1 PASS, g = 1.922505 ≥ 0.25, identity pass); **candidate (ii) donor centroid C3 — Supported** (E-K3-1 PASS, g = 1.061783 ≥ 0.25, audit-value match 7.45e-9 ≤ 1e-6, |g − 1.061783| = 9.56e-8 ≤ 1e-4). [FACT] Guards G1–G7 all passed: G4 recomputed 60/60 index-aligned byte-exact (id, t, f) against the signed pre-audit JSON (Law #3 — nothing inherited from LOG-238); Δθ=0 pre == post == archived `ec276abe…e0ed`; zero forward invocations. [FACT] No 0.9-bar firing on either candidate (k = 0/60 both; CP95 [0.0000, 0.0596]) — no Phase-1 caveat attaches; candidate (ii)'s signed |cos| < 0.1 fact re-verified (max 0.0918 / 0.0817). **Program aggregation (pre-registered §7.1): PROCEED** — both candidates advance to the §8 G9 release chain. No verdict on H_compliant; Phase 1 does not exist until G9 releases it.

---

## 1. §10 execution record (steps 1–6)

**Step 1 — environment + model load + G3 pre-hash.** [FACT] Environment asserted exact: `/home/hatch/workspace/.venv_smoke`, python 3.12.3, torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, scipy 1.18.1, Linux-7.0.0-38-generic-x86_64. [FACT] `EleutherAI/pythia-410m` @ `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` loaded read-only (`local_files_only=True`, `trust_remote_code=False`, `torch_dtype=torch.float32`, `model.eval()`); pinned snapshot present in the local HF cache — nothing downloaded, nothing substituted. [FACT] G3 pre-hash via the verbatim `run_exp077.py` ll.166–172 formulation = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`, byte-equal to the archived hash (64-hex, verified against the LOG-197/G1 corpus records).

**Step 2 — bench port + G4 + G6.** [FACT] Bench rebuilt from verbatim ports of the runner's construction code (`run_exp077.py` ll.149–162 constants, ll.586–636 four quad loops); quad-loop sub-ranges recorded: planet_2hop 0–14, planet_3hop 15–29, element_2hop 30–44, element_3hop 45–59 (60 items). [FACT] **G4:** the executor recomputed the full 60/60 index-aligned byte-exact comparison of rebuilt `(id, t, f)` against `experiments/protocols/C-A_PREAUDIT_2026-09-23.json` `similarity_audit.per_item` itself (Law #3) — **60/60 matches, 0 mismatches**; nothing inherited from LOG-238's claim. The pre-repair smoke archive `exp077_instance_records.json` was not touched (§2 D1-lesson note, binding). [FACT] **G6:** all 35 unique donor + test entity strings single-token as `" "+entity` (60 premise-non-option instances covered); zero violations.

**Step 3 — E-K3-1 static Law #7 compliance audit.** [FACT] Candidate (i): per-item `{tok(B_i), tok(C_i)} ∩ {tok(target_i), tok(foil_i)} = ∅` on all 30 3-hop items — **PASS, no violating ids**. (C-c): the ported construction references only the `B`/`Cprem` fields — input multiset is exactly the 60 premise-non-option strings; no label-derived ids by construction. (C-d): present-instance bench material only (the fixed N=60 bench contains no held-out/future instances). (C-e): licensed. [FACT] Candidate (ii): donor token-id set ∩ all 60 test `{target, foil}` token ids = ∅ — **PASS, empty intersection**; donor-label flow cited from the signed EXP081 v2 §3.3 Law #7 statement (support-side construction material; labels never enter the evaluation objective). [OBSERVATION] Cross-item collision count (descriptive, non-gating, per the LOG-235 F-235-1 rationale): 60/60 bank premise instances coincide with *some other* item's target/foil token id — expected on the shared 10-entity pool; carries no compliance weight.

**Step 4 — constructions + E-K3-2 + E-K3-3 + E-K3-4.** [FACT] b̂_P built from the 30 3-hop `(B_i, C_i)` pairs (higher-minus-lower by prompt rank); b̂_D built from the 20 verbatim v2 §3.1 `(t_d, f_d)` donor pairs via sum-of-differences-then-normalize. [FACT] **G7:** all 50 bank-pair norms > 0 (P: min 0.688273; D: min 0.742775); both candidate norms > 0 (‖b̂_P‖ = 1.0, ‖b̂_D‖ = 1.0 to float32). [FACT] **E-K3-2:** g_P = **1.922505** ≥ 0.25 → PASS; g_D = **1.061783** ≥ 0.25 → PASS. Per-pair norms — (i): min 0.688273 / mean 0.753911 / max 0.867831; (ii): min 0.742775 / mean 0.857066 / max 0.964313. [FACT] **E-K3-3(a):** self-consistency |cos(path-A, independent float64 path-B)| = **1.0** for both candidates (≥ 1−1e-6). [FACT] **E-K3-3(b):** candidate (ii) recomputed s_t/s_f match the signed per-item records with max abs deviation **7.45e-9** (≤ 1e-6); summary-stat deviation 7.45e-9; |g_rebuilt − 1.061783| = **9.56e-8** (≤ 1e-4) — the rebuild IS the signed v2 C3 construction. [FACT] **E-K3-4:** cosine profiles vs the per-item option-informed bridge (see §3 table); 0.9-bar: k = **0/60** on both candidates, exact Clopper–Pearson 95% CI **[0.0000, 0.0596]** — no firing, no Phase-1 caveat attaches to candidate (i); candidate (ii) shows no firing against the signed audit (|cos| < 0.1 re-verified: max |s_t| = 0.0918, max |s_f| = 0.0817).

**Step 5 — G5 + G3 post-hash.** [FACT] **G5:** source scan of the executor script finds zero direct forward-invocation patterns (`model(` occurrences: 0; all weight access via `model.state_dict()`, `model.eval()`, `model.get_output_embeddings()` attribute reads; tokenizer only for ids) — **no forward pass at any step**. [FACT] **G3:** post-hash = pre-hash = archived `ec276abe…e0ed` → **Δθ=0**.

**Step 6 — twin JSON + this report.** [FACT] `K3_CONSTRUCTION_AUDIT_RESULTS_LOG239_LOG241_2026-09-23.json` written: unrounded g values, all 50 per-pair norms, per-item cosine arrays (60 × 5), token-id audit sets, hashes, env manifest, guard outcomes, verdicts. RNG: none consumed (recorded).

---

## 2. Guards G1–G11 (FATAL on failure)

| Guard | Outcome |
|---|---|
| G1 static audit executability | PASS — E-K3-1 completed as specified on both candidates; no silent skips |
| G2 identity | PASS — E-K3-3(a) 1.0/1.0 (≥ 1−1e-6); E-K3-3(b) 7.45e-9 ≤ 1e-6, 9.56e-8 ≤ 1e-4 |
| G3 Δθ=0 | PASS — pre == post == archived `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (verbatim ll.166–172 formulation) |
| G4 label/premise cross-check | PASS — **60/60** index-aligned byte-exact (id, t, f) vs the signed pre-audit JSON, recomputed by this executor (Law #3); smoke archive never consulted |
| G5 no forward pass | PASS — source scan: 0 direct forward-invocation occurrences |
| G6 single-token | PASS — 35/35 unique entities single-token; 60/60 premise instances covered |
| G7 norm floors | PASS — all pair norms > 0; both candidate norms > 0 |
| G8 Phase-1 pins | N/A — Phase 1 not released |
| G9 Phase-1 release chain | NOT SATISFIED (by design) — plan SIGN ✓, Phase-0 report (this) filed ✓; Law #14 re-verification SIGN, CEO GPU clearance, BK-04 booking outstanding → **no GPU** |
| G10 budget cap | N/A — Phase 1 not released |
| G11 Tango method identity | N/A — Phase 1 not released |

---

## 3. Endpoint results

### E-K3-1 — compliance (primary gate)

| Candidate | Per-item disjointness | Violating ids | Verdict |
|---|---|---|---|
| (i) premise-rank bank | {B_i,C_i} ∩ {t_i,f_i} = ∅, 30/30 items | — (none) | **PASS** |
| (ii) donor centroid C3 | donor ids ∩ test {t,f} ids = ∅ | — (none) | **PASS** |

[OBSERVATION] Cross-item collision count: 60/60 premise instances share a token id with some *other* item's target/foil — descriptive, non-gating (LOG-235 F-235-1).

### E-K3-2 — non-degeneracy (gate)

| Candidate | g (6dp) | floor | Per-pair norms min / mean / max | Gate |
|---|---|---|---|---|
| (i) premise-rank bank | **1.922505** | 0.25 | 0.688273 / 0.753911 / 0.867831 | PASS |
| (ii) donor centroid C3 | **1.061783** | 0.25 | 0.742775 / 0.857066 / 0.964313 | PASS |

### E-K3-3 — construction identity (guard)

| Check | (i) | (ii) | Tolerance | Result |
|---|---|---|---|---|
| (a) self-consistency |cos| | 1.0 | 1.0 | ≥ 1−1e-6 | pass / pass |
| (b) s_t/s_f max abs dev vs signed | — | 7.45e-9 | ≤ 1e-6 | pass |
| (b) \|g − 1.061783\| | — | 9.56e-8 | ≤ 1e-4 | pass |
| (c) single-token entities | pass | pass | G6 | pass |

### E-K3-4 — geometric profile vs the option-informed bridge (descriptive)

| Candidate | cos vs b̂_i^opt mean / median / min / max | cos vs ŵ_t mean / max | cos vs ŵ_f mean / max | 0.9-bar k/60 | CP95 |
|---|---|---|---|---|---|
| (i) premise-rank bank | 0.204543 / 0.091276 / −0.058034 / 0.741783 | 0.034494 / 0.379488 | −0.201613 / −0.030145 | 0 | [0.0000, 0.0596] |
| (ii) donor centroid C3 | −0.028046 / −0.039888 / −0.112130 / 0.059757 | −0.038264 / 0.081702 | −0.003907 / 0.081702 | 0 | [0.0000, 0.0596] |

[FACT] No 0.9-bar firing on either candidate → the pre-registered caveat for a Phase-1 CONTINUE on candidate (i) does not attach. [FACT] Candidate (ii)'s signed |cos| < 0.1 fact re-verified (max |s_t| = 0.0918, max |s_f| = 0.0817) — no [OBSERVATION] against the signed audit. [INFERENCE] Candidate (i) is weakly aligned with the option-informed bridge on average (mean cos ≈ 0.20, max 0.74) while remaining label-free by construction — the §12 "label-free headroom" asset: a descriptive bound on how much of the option-informed direction is recoverable from premise-rank geometry.

---

## 4. §7.1 verdict table (filled verbatim from the plan)

| E-K3-1 compliance | E-K3-2 (g ≥ 0.25) | E-K3-3 identity | Guards | Per-candidate verdict |
|---|---|---|---|---|
| **PASS** | **≥ 0.25 (1.922505)** | **pass** | **pass** | **Candidate (i): Supported** — viable compliant candidate; Phase-1-eligible |
| **PASS** | **≥ 0.25 (1.061783)** | **pass** | **pass** | **Candidate (ii): Supported** — viable compliant candidate; Phase-1-eligible |
| PASS | < 0.25 | pass | pass | Not supported — degenerate; cannot bear the rescue test (defect named; no repair in place) — *not landed* |
| FAIL (ids named) | any | any | pass | Not supported — not Law-#7-compliant as specified (defect named; Law #4: repair = new plan) — *not landed* |
| cannot complete (items named) | — | — | pass | Inconclusive — audit uncompletable as specified — *not landed* |
| — | — | — | fail | Refuted (integrity failure; halt; no claim licensed) — *not landed* |

**Program-level Phase-0 aggregation (pre-registered): ≥1 candidate Supported → PROCEED.**

Per §9 (quoted, not extended): "Phase-0 PROCEED (≥1 Supported): the supported candidate(s) advance to the §8 G9 release chain. Nothing else changes; no verdict on H_compliant yet." The LOG-238 halt converts to a superseded halt per the R1-specific consequence (the halt report is preserved in place, untouched — Law #8). The UNDERDETERMINED/GPU-INFEASIBLE branch did not fire. No §H7 decision is touched; no novelty claim is made (N1); K3's donor reading remains an [OBSERVATION] for EXP081, never a verdict on H_transfer (Law #4).

---

## 5. L1 mathematical license — the readout-shift lemma reproduced (promotion record)

**Lemma (readout-shift).** [THEOREM] Let W_U ∈ ℝ^{V×d} be the frozen unembedding matrix, x ∈ ℝ^d the final-token residual, ℓ = W_U x (+ constant bias, immaterial: Δℓ is bias-independent). For unit v̂ ∈ ℝ^d, scalar α, token y: the perturbation x ← x + αv̂ shifts the y-logit by **Δℓ_y = α·(W_U[y,:]·v̂) = α‖W_U[y,:]‖₂·cos(v̂, ŵ_y)**, ŵ_y = W_U[y,:]/‖W_U[y,:]‖₂. *Proof:* Δℓ = W_U(αv̂); take the y-th row. ∎ (K1 §6 L1; EXP082 §6 L1 — same lemma, cited not re-proved.)

**Assumption inventory (L4, Phase-0-relevant):** A1 (item/premise labels — discharged via G4, 60/60 recomputed); A2 (mid-network propagation — UNDISCHARGED [CONJECTURE]; the Phase-0 geometric/compliance endpoints do not need it); A3 (run pins — discharged via G3, pre == post == archived); A4 (EXP070 excluded — honored; no EXP070 vector endpoint anywhere); A5 (binary scoring — verified by code read, EXP077 ll.669–682); A6 (α/l\*/hook/dtype pinned — Phase-1 scope, not exercised); A7 (premise-bank orientation higher-minus-lower — honored; the sign-flip variant is not constructed); A8 (diagnostics as [OBSERVATION] — honored); A9 (donor-identity anchor — discharged via E-K3-3(b)); A10 (item-independence for CIs — the CP CIs are nominal; disclosed, not hidden); A11 (K3-(ii) vs EXP081 jurisdiction — honored); A12 (data contact — (ii) values re-verified as guards; (i) geometry has no data contact). Weakest load-bearing grade for the Phase-1 causal upshot remains CONJECTURE-UNDER-TEST; the Phase-0 algebra and static compliance checks are IN-HOUSE-PROOF, promoted toward PROVEN-LEMMA by this report's reproduction of the L1 proofs and the Law #14 re-verification SIGN.

---

## 6. Deliverables

1. Executor script: [K3_construction_audit_execute_LOG239_LOG241_2026-09-23.py](sandbox://workspace/SCBI/research/analysis_plans/K3_construction_audit_execute_LOG239_LOG241_2026-09-23.py) — G5 asserted (zero direct forward-invocation occurrences; §2 table).
2. This report: [K3_PHASE0_REPORT_LOG241_2026-09-23.md](sandbox://workspace/SCBI/research/analysis_plans/K3_PHASE0_REPORT_LOG241_2026-09-23.md)
3. Machine-readable twin: [K3_CONSTRUCTION_AUDIT_RESULTS_LOG239_LOG241_2026-09-23.json](sandbox://workspace/SCBI/research/analysis_plans/K3_CONSTRUCTION_AUDIT_RESULTS_LOG239_LOG241_2026-09-23.json) — unrounded g values, 50 per-pair norms, per-item cosine arrays (60 × 5), token-id audit sets, hashes, env manifest, guard outcomes, verdicts.

## 7. Caveats and open questions

- [OPEN] Phase 1 does not exist until the §8 G9 release chain completes (Law #14 re-verification SIGN of this report + CEO GPU clearance + BK-04 booking). No GPU was spent; nothing downstream moves on this report alone.
- [OBSERVATION] transformers 5.17 emits a `torch_dtype`-is-deprecated warning on `from_pretrained`; the pinned kwarg still takes effect (weights loaded float32; the Δθ=0 hash confirms the snapshot). Cosmetic; recorded for the record.
- [OBSERVATION] The LOG-238 halt report stands preserved in place (Law #8); under the R1-specific §9 consequence it is now a *superseded* halt. No signed artifact was edited.
- No banned-verdict language appears in this report. `reports/research_log.md` was not written (the Lead owns the log).

*Executor: LOG-241 · 2026-09-23 · Standup: verdict in hand — both candidates **Supported**; program **PROCEED** to the §8 G9 release chain. Two Law-#7-compliant constructions exist, are non-degenerate, and match their pinned identities; the rescue question is now a GPU question.*
