# Law #14 Review — EXP139 Pre-registration DRAFT (S4-4 / J1 Stage-1 Contraction Screen)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design or the draft)
**Date:** 2026-10-03
**Document reviewed:** `~/workspace/SCBI/research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md` (exact file)
**Prior records read:** `research/innovation/S44_DESIGN_2026-10-03.md` (worth-it gate, CONDITIONAL RUN); `research/innovation/S44_DESIGN_REVIEW_2026-10-03.md` (APPROVE-WITH-CONDITIONS C1–C5)
**Review verdict:** **SIGN-WITH-FIXES** (5 mechanical fixes, F1–F5 below). Not a REJECT: the draft is fundamentally sound; the issues are completions, not structural flaws. This review licenses nothing to run — execution additionally needs CEO venue approval per LOG-4408.

Independent verifications performed by this reviewer (not trusted from reports):
- Record structure: `experiments/runs/EXP135_eval/out/exp135_records.json` top-level keys are C1–C9 + `cache_unintervened`; per-record keys are exactly `yhat`, `margin` — **no residual vectors**. The draft's Stage-1 cost correction (40 → 60 passes) is valid.
- `run_exp135.py`: `torch_dtype=torch.float32` (line 70), dtype assertion (line 53), `BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"` (line 24) — matches the draft's pin verbatim.
- Full bench hash in research log line 15207: `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` — matches the draft's truncated `eb304fa6…45589df` (prefix/suffix).
- S4 doc writes "Π = W_E W_Uᵀ" (V×V, dimensionally wrong for the claimed ℝᵈ→ℝᵈ map) — the draft's correction to W_EᵀW_U ∈ ℝ^{1024×1024} is valid.
- Blayney et al. 2026: arXiv:2604.11791 exists ("A Mechanistic Analysis of Looped Reasoning Language Models", April 2026); abstract confirms fixed-point/cyclic-trajectory claims — the draft's characterization is accurate.
- Newcombe paired interval (§7): the Wilson score formulas and the Method-10 combination L = Δ̂ − √((p̂_b−l_b)² + (u_c−p̂_c)²), U = Δ̂ + √((u_b−p̂_b)² + (p̂_c−l_c)²) are the correct standard construction. "No continuity correction" is a legitimate pre-registered choice.

---

## Per-point findings

### 1. C1–C5 closure — genuinely closed, with two completions required (F1, F2)

- **C1 (input construction): CLOSED.** §2 pins: single-token `inputs_embeds` (z.view(1,1,1024)), position_ids=[[0]], attention_mask=[[1]], readout (final-LN + unembed + argmax; baseline at last prompt position, re-entrant at position 0), raw-logit Πh with explicit "no softmax". The review's terminological note ("soft re-embedding" vs raw logits) was addressed — the draft states the exact math. No improvisation surface remains.
- **C2 (verdict gaps): SUBSTANTIALLY CLOSED, two completions required.**
  - Gap (a) κ̂≥1 + Stage-1b unrun → HELD(a). ✓
  - Gap (b) Stage-1b intermediate zone → HELD(b). ✓
  - Stage-2 intermediate zone → HELD(c)/(d). ✓
  - **Missing: κ̂ < 1 with Stage-2 unrun or infeasible** (e.g., founder GPU never materializes — Stage 2 is explicitly founder-gated and "not assumed"). No branch covers this reachable outcome. → **F1.**
  - **Silent deviation: κ̂<1 + Stage-2 ΔM_attractor ≤ 0.** The approved design's falsification tree classifies this HELD ("Converges to nothing useful — dynamics exist, no capability. Licenses nothing, kills nothing."); the draft classifies it KILL ("Family closed") with no acknowledgment. Under Law #4 the design's bars were the reviewed baseline — deviations must be explicit, not silent. → **F2.**
- **C3 (venue rule): CLOSED.** §4: 5-item pilot (15 passes), CPU iff mean <30 s/pass AND peak RSS < 8 GB, else GPU; evaluated once, recorded, not revisited. Fully pinned.
- **C4 (Blayney): CLOSED and independently confirmed** (see verifications above).
- **C5 (expectation calibration): CLOSED.** §10 states the modal κ̂≥1 outcome and the pilot's boundary-science status.

### 2. The two self-reported corrections — both valid; same error pattern found twice more (F5)

- **(a) Stage-1 60 passes: VALID** (verified against record structure above).
- **(b) float32 + BACKBONE_PIN: VALID** (verified against run_exp135.py above).
- **However, the draft replicates the undercount pattern in Stages 1b and 2:** both need per-item baseline states h_i, but only items 0–19 have h_i from Stage-1.
  - Stage-1b (60 items, T=3): 180 R-evaluations + **40 additional baseline passes** (items 20–59; items 0–19 reuse Stage-1 h_i) = **220 passes, not 180**. → **F5.**
  - Stage-2 (60 items, T=8): 480 R-evaluations + **40 additional baseline passes** = **520 passes, not 480**. (Stage-1b does not run on the κ̂<1 path, so its h_i are unavailable.) → **F5.**
  - Cost claims survive (still trivial CPU / still <0.01 T4-h); this is Law #2 bookkeeping, not a license-breaker — but it is exactly the error class the draft itself corrected for Stage-1.

### 3. Falsification tree — complete except F1; precedence sound

Exhaustive case analysis: every (κ̂, trajectory, ΔM) combination routes to exactly one branch under KILL > PIVOT > CONTINUE > HELD, except the κ̂<1 + Stage-2-unrun case (F1). Validity-gate failures route to VOID→HELD correctly. Boundary cases check out: κ̂ exactly 1.0 → "κ̂ ≥ 1" branch; flat trajectory → "non-decreasing" (routes to PIVOT/HELD(d) by precedence); KILL precedence correctly overrides trajectory considerations when ΔM ≤ 0.

### 4. Inference spec — sound and fully specified

Newcombe Method 10 with explicit Wilson equations (z=1.96, no continuity correction, clipped to [0,1]); binding bar Δ̂ ≥ 0.08 with L > 0.05 (≈5 net items, CI entirely above +5pp — stringent, pre-registered); McNemar-exact as secondary only. The executing lane can implement verbatim; "any deviation voids the inference" is the correct strictness.

### 5. Law #7 firewall — structurally sound

Labels touch only bench evaluation (accuracy, ΔM, paired table). Screen items are bench-ordered (0–19), never label-selected. The κ̂ estimator (residual norms, R-evaluations) never sees labels. The validity gate (c) recomputes yhat (a prediction, not a label). The firewall is structural, not procedural — as required.

### 6. Residual risks — acceptable as pinned-and-declared

- Single-token position-0 construction: IS the radical claim under test (§11.1 states it plainly — the fixed point must carry question information through Π-feedback alone). Pinning is the pre-reg's job; optimality is not required for SIGN.
- View-0 arbitrariness: declared in §11.2, deterministic. Acceptable.

### 7. Other draft-vs-design comparisons — no further contradictions

- Stage-1b T: design "T ∈ {2,3} fixed" → draft pins T=3. Legitimate closure of an ambiguous phrase, within the stated range.
- The draft's staging of Stage-1b (a stage, not a verdict) is cleaner than the design's table and consistent with its intent.
- Licensing chain, governing laws, non-resurrection audit, and expectation calibration are all consistent with the design.

---

## Verdict: SIGN-WITH-FIXES

The draft becomes the binding EXP139 pre-registration once these 5 mechanical fixes are applied verbatim (a repair lane may apply them; no re-review of the full draft is needed — the CEO verifies the fixes by diff):

- **F1 — Add HELD(e) to §6** (and update §0's "four cases" count to five): `| HELD (e) | κ̂ < 1 and Stage-2 unrun or infeasible | Contraction license survives; attractor untested. Licenses nothing, kills nothing. |`
- **F2 — Reconcile the κ̂<1 + Stage-2 ΔM_attractor ≤ 0 classification.** The approved design classifies this HELD; the draft classifies it KILL, silently. Either (a) revert §0 and §6 to the design's HELD ("Converges to nothing useful — dynamics exist, no capability. Licenses nothing, kills nothing."), or (b) retain KILL and add an explicit deviation note in §0/§6 stating the departure from the design with its justification. The choice must be explicit in the document. (Reviewer's lean: the design's HELD is more precise — it preserves the convergence information — but either is defensible if explicit.)
- **F3 — Clarify HELD(c):** specify what "LCI straddles" straddles, i.e. `0 < ΔM_attractor < +8pp, or Δ̂ ≥ +8pp with L ≤ 0.05 (LCI straddles the licensing threshold)`.
- **F4 — Full bench hash:** in §2/§3 cite the complete `bench_sha256 = eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` (research log line 15207) instead of the truncated form, so the executing lane has the complete reference value.
- **F5 — Correct the Stage-1b and Stage-2 pass counts:** Stage-1b: "T = 3 fixed (180 R-evaluations + 40 additional baseline passes for items 20–59 [items 0–19 reuse Stage-1 h_i] = 220 passes)". Stage-2: "T = 8 fixed (480 R-evaluations + 40 additional baseline passes = 520 passes)". Update §4, §5, §6 cost references, and the §1/§10 cost statements accordingly.

This review does not license execution, mint anything further, or approve Stage 2. After the fixes: Law #14 SIGN is complete for the draft; Stage-1 execution still needs CEO venue approval per LOG-4408.
