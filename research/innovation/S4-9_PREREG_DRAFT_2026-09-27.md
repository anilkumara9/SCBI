# S4-9 — Per-Item Layer-11 Task-Direction Causal Test — Pre-registration DRAFT (UNSIGNED)

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. NOT reviewed. No experiment number minted (S4-9 is EXP094+ material; numbering happens after Law #14 review + CEO license).*
*Licensing chain: LOG-4352 (EXP093 real re-execution, KILL UPHELD, binding) → LOG-4353 (Friday cull: S4-9 born from EXP093's death-debt, LOG-219 rule; debt recorded PAID) → LOG-4365 (Law-#15 worth-it analysis delivered, GO as EXP094+ material) → LOG-4366 (reconciled; S4-9 pre-reg draft commissioned as a $0 CPU writer lane) → LOG-4368 (this draft) → LOG-4369 (independent Law #14 review, SIGN-WITH-FIXES: F1–F4 blocking, A1–A7 advisory) → LOG-4370 (this repair).*
*All values below are from `research/innovation/S4-9_WORTHIT_ANALYSIS_2026-09-27.md` (LOG-4365) and LOG-4352 unless otherwise cited. No number is invented.*
***No pilot is authorized by this draft.** Before any run: independent Law #14 review + SIGN (pre-assigned LOG-4369, separate lane), then CEO execution clearance. No GPU contact is needed for the design (CPU <0.005 T4-h), but CEO clearance gates any run regardless of venue.*

---

## 0. Law #15 block (binding, carried from LOG-4365)

**Precise question [HYPOTHESIS].** EXP093 (binding KILL UPHELD, LOG-4352) showed that static injection of the **shared** layer-11 task direction on EXP092-B moves zero decisions: aggregate/A-first/C-first accuracy identical across B/P/N arms (0.6000/0.9667/0.2333), Δ = 0.0000, McNemar b = c = 0 → p = 1.0 in all six tests (P-vs-B and N-vs-B × 3 strata), with the perturbation verified real (perturbation_ratio = 0.0474, ~4.7% of residual norm, reached the logits — mean margins shifted +0.0059 P / −0.0076 N — yet flipped nothing: causal inertness, not measurement failure). The licensed claim is scoped: it falsifies *"≥10pp causal transfer via a shared static direction at layer 11"* only. **Does an item-specific (per-item) task direction move decisions on the same bench, where the shared direction moved none?** [HYPOTHESIS]

**Decision it changes.** **KILL** the L11 directional family if per-item ΔM ≤ shared (≈ 0 both) — the inertness is not a sharedness artifact; licensed claim expands to all static L11 task directions, hunt moves to gated/dynamic or multi-layer mechanisms. **KILL** (specificity) if random-per-item matches task-per-item — nonspecific perturbation, no causal license. **CONTINUE** (licensed positive only) if ΔM_task-per-item > random-per-item AND clears the pre-registered causal bar (§3), with pre-registered routing and stratum breakdown — the first causal-steering license at a non-readout layer. **PIVOT** if movement is item-heterogeneous and sign-inconsistent — global per-item claim dead, conditional design becomes EXP095 material. All four outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** 3 arms × 60 items ≈ 180–240 passes, CPU, <0.005 T4-h, $0 (from the backlog row). Arms: B baseline (Δθ = 0), T per-item task direction at the EXP093 norm, R norm-matched per-item *random* direction (specificity arm EXP093 lacked). No cheaper decision exists for the shared-vs-per-item question.

**Quantitative prediction (pre-registered, bars).** ΔM_task-per-item > DELTA_BAR = 0.10 (the EXP093-licensed bar) **and** ΔM_task-per-item > ΔM_random-per-item with McNemar p < 0.05 on the T-vs-R flip table (b_T-vs-R vs c_T-vs-R). The specificity gap is non-negotiable: a nonspecific perturbation effect predicts ΔM_T ≈ ΔM_R; only task-geometry steering predicts ΔM_T > ΔM_R.

**Breaking point (sharp).** ΔM_task-per-item ≤ 0.10 with ΔM_R within sampling noise of ΔM_T → per-item family dead **KILL** — inertness is about location, not sharedness. If {d_i} degenerate (collinear; §4), the test is powerless → **Underdetermined** (never KILL on a powerless test — R4-licensed rule).

**The belief it tests (named, LOG-4353):** "the EXP093 kill was about sharedness, not location." [INTERPRETATION]

---

## 1. Background and license

- **EXP093 binding facts [OBSERVATION, LOG-4352]:** static injection of the shared L11 task direction on EXP092-B: Δ = 0.0000; McNemar b = c = 0 → p = 1.0 all six tests; perturbation_ratio = 0.0474 (real nudge); margins +0.0059 P / −0.0076 N (reached logits); zero flips. Licensed claim: shared static L11 directions do not move decisions; per-item directions reserved as EXP094+ material.
- **Death-debt [FACT, LOG-4353/4366]:** S4-9 pays EXP093's LOG-219 death-debt; deaths table records PAID. This draft is the "full fresh pre-registration chain" the backlog row requires — **not a revival or an edit of EXP093's signed protocol** (LOG-4352 §4: protocol digest `3e0f269b…` intact; no signed file modified — this document is a new unsigned file).
- **Mathematical license [THEOREM-adjacent linear-algebra fact, LOG-4365 §4]:** in the 512-dimensional residual space at L11, the shared direction d̄ is one fixed vector; EXP093 falsified E_i[f_i(d̄)] > bar — a one-dimensional statement. The per-item test asks strictly broader: does a family {d_i} exist with E_i[f_i(d_i)] > bar beyond a random-direction control? **License verdict: HOLDS for a test, not a conclusion** — the license licenses the experiment, not the positive. Honest audits carried: (Gap 1) constructor degrees of freedom → G7 disqualification bar + random control prices out cleverness; (Gap 2) one bench → CONTINUE claim bench-scoped to EXP092-B; (Gap 3) power n=60/Δ̄=0.10 detects ≈6 flips → movement gate before interpreting specificity.
- **Summit filter [LOG-4365 §6]:** a licensed positive would be the program's first causal-steering license at a non-readout layer — the per-item steering primitive the summit (autonomous self-steering) must build on. Caveat preserved: injection is externally applied by us, not self-computed by the model — must never be described as an autonomy result.

---

## 2. Design (frozen model, Δθ = 0)

### 2.1 Arms (pre-registered)

| Arm | Injection at L11 | Role |
|---|---|---|
| B | none (Δθ = 0) | baseline — anchors the EXP092-B bench |
| T | per-item task direction d_i at matched norm (target perturbation_ratio ≈ 0.0474 of residual norm per item) | test arm — item-indexed family |
| R | norm-matched random per-item direction, task-free by construction | specificity control — the arm EXP093 lacked |

#### 2.1.1 T-arm constructor (frozen specification C-1 — the intervention under test)

d_i is the item-indexed **within-item task-framing contrast** at L11, computed by this exact algorithm (no executor discretion; the constructor code is frozen per G7.1 before any run):

- **Input tensors (label-free by construction):** for item i, the item's input-token IDs exactly as presented in the B-arm pass (prompt/question text, byte-identical tokenization to the baseline pass). Token span: the **last prompt token** (the readout-anchor position — the last input token before generation begins; the same position at which the constructor reads L11 and at which injection occurs). Explicitly NOT read: the bench label field, answer keys, target tokens, correct-option indices, any other item's data, any aggregate computed with label knowledge. [DEFINITION]
- **Contrast operation (per item i):**
  1. Pass A (task): forward item i under the bench's task framing, exactly as in the B-arm pass. Record the L11 residual-stream activation at the readout-anchor position: a_i = h_i^task ∈ ℝ^512 (the 512-dimensional L11 residual space, LOG-4365 §4).
  2. Pass B (reference): forward the *same* item text under a fixed label-free neutral prefix P₀ (a constant task-free string, frozen with the constructor — never the bench prompt, never label-bearing text). Record the L11 residual-stream activation at the same position: b_i = h_i^ref ∈ ℝ^512.
  3. Raw direction: r_i = a_i − b_i — the within-item task-framing contrast: the vector by which the task framing displaces item i's L11 representation. If ‖r_i‖₂ = 0 exactly, the item yields no direction and is flagged in the constructor manifest; the G5 delivery probe's per-item band (§4) catches it downstream (perturbation_ratio = 0 sits outside 0.0355–0.0593).
- **Normalization:** u_i = r_i / ‖r_i‖₂ (unit vector).
- **Per-item norm matching:** ‖h_i^B‖₂ = the L11 residual norm at the readout-anchor position on item i's B-arm pass. d_i = u_i × (0.0474 × ‖h_i^B‖₂) — so the construction target is perturbation_ratio = ‖d_i‖₂ / ‖h_i^B‖₂ = 0.0474 exactly per item, the EXP093-licensed norm (LOG-4352); the G5 probe's ±25% band (0.0355–0.0593) tolerates injection drift.
- **Injection:** d_i is added to the L11 residual stream at the readout-anchor position of item i's T-arm pass, before the next block; nothing else changes.

Rationale: the contrast reads only the item's own input activations under two presentations; no label, answer key, or target enters any input tensor, so the constructor is mechanically label-swap invariant (G7.3). Uniform per-item norms are *intended* by this construction — see §4 (F4 repair): norm uniformity never triggers Underdetermined.

#### 2.1.2 R-arm direction specification (A6)

- **Norm tie:** for item i, the R-arm direction norm equals the T-arm item norm: ‖g_i‖₂ = ‖d_i‖₂ (the norm computed in §2.1.1 before injection). [DEFINITION]
- **Sampling distribution:** g_i_raw drawn from an isotropic Gaussian in the 512-dimensional L11 residual space, then normalized to unit norm before scaling to ‖d_i‖₂. The sampling seed is pinned in the environment + seed manifest (§5 item 3). Task-free by construction.

#### 2.1.3 G7 label-free audit (disqualification bar — LOG-4369 §6-answer-1, binding)

The frozen constructor hash (G7.1) is audited **before any run**; attestation is persisted in the constructor manifest (§5 item 2):

- **G7.1 — Freeze:** constructor code + config + neutral-prefix string P₀ + dependency pins hashed (SHA-256) and committed before any run; the audit applies to that hash.
- **G7.2 — Input attestation:** an independent lane (no authorship of the constructor) enumerates every input the constructor reads. Allowed: the item's own input-token activations at L11 (prompt/question tokens only, §2.1.1). Forbidden: item labels, answer keys, target tokens, correct-option indices, any other item's data, any aggregate computed with label knowledge. The audit first documents *where EXP092-B's label lives* in the bench files so the auditor can verify the constructor cannot reach it.
- **G7.3 — Label-swap invariance test (the auditable disqualification bar):** run the frozen constructor on the bench with labels randomly permuted (equivalently, replaced with constants); the produced {d_i} must be identical to the production run (bit-for-bit, or max abs diff ≤ 1e-9). Any label path fails this test mechanically — no judgment involved.
- **G7.4 — Cross-item isolation:** verify d_i uses only item i's data (no leakage from other items' labels or answers).
- **G7.5 — Verdict:** PASS → attestation + hashes persisted in the constructor manifest. FAIL (any label contact) → **DISQUALIFICATION**: not a negative result; the run is voided; only a fresh constructor with a fresh audit may proceed. A label-informed per-item direction is a disqualification, never a positive.

**Bench:** EXP092-B, n = 60 items, strata aggregate / A-first / C-first (the six-test structure of EXP093 preserved for comparability).

### 2.2 Budget (pre-registered)

- **180–240 passes expected; hard cap 400.** Decomposition (self-verifying): 3 injection conditions (B, T, R) × 60 items = 180 passes; 60 reserved for exact-delivery re-probes and margin-verification repeats. Spend beyond 240 requires a logged, pre-cleared exception; the 400 hard cap is not waivable within this pre-registration (a change is a new design, not an edit). CPU only, <0.005 T4-h, $0.

### 2.3 Statistics (pre-registered)

- **McNemar exact** on paired decisions: T-vs-B and R-vs-B pair each arm against the item's own baseline decision; T-vs-R pairs the T(i) and R(i) decisions directly (not vs baseline).
- **ΔM definition (EXP093's Δ convention):** ΔM_T = (1/n)Σ[correct_T(i) − correct_B(i)], the paired accuracy difference; analogously ΔM_R for R-vs-B. correct_X(i) is the top-1 correctness on item i under arm X. [DEFINITION]
- **Tango 95% CIs** on the paired differences.
- **DELTA_BAR = 0.10** (the EXP093-licensed bar), **ALPHA = 0.05** — verbatim bars, no post-hoc movement.
- **Movement gate:** the specificity contrast T-vs-R is interpreted only if observed movement (b + c on T-vs-B or R-vs-B) clears a pre-registered minimum (≥ 6 total flips across T and R vs B — the ≈Δ̄=0.10 detectable count at n=60). Movement ≈ 0 on both T and R with delivery proven → **KILL** (§3 step 3), not Underdetermined. If the delivery probe FAILS under the pre-registered aggregation rule (§4), the run routes to **Inconclusive/HOLD** per §3 step 1 — a procedure problem; never KILL and never Underdetermined.

---

## 3. Decision table (pre-registered)

**Arm-routing rule (binding, F3 repair):** every one of the 60 EXP092-B bench items receives all three arms (B, T, R); all contrasts (T-vs-B, R-vs-B, T-vs-R) are within-item paired; no item is excluded from any contrast; stratum membership (aggregate / A-first / C-first) is the EXP092-B bench pin, fixed before inspection. There is no between-items allocation and no post-hoc re-routing — re-routing is structurally impossible under full pairing. (The backlog row's "N-vs-B" label referred to the per-item test arm; S4-9's arms are B/T/R and the N label does not appear anywhere in this design's binding rules. §0's description of EXP093's own P/N arms is historical fact and is not renamed.)

**Binding evaluation order (first match wins — F1 repair).** The executor evaluates the steps in this exact order; exactly one step is earned:

1. **Delivery:** G5-style probe FAILS (§4 aggregation rule) → **Inconclusive/HOLD** — procedure invalid; no verdict licensable. Single routing for delivery failure. *(Maps to: Inconclusive.)*
2. **Degeneracy:** {d_i} degenerate — mean pairwise |cosine| ≥ 0.95 (F4: norm-CV clause removed) — → **Underdetermined** — never KILL on a powerless test (R4 rule). *(Maps to: Underdetermined.)*
3. **Movement:** (b + c on T-vs-B) + (b + c on R-vs-B) < 6 → **KILL** (family): inertness is not a sharedness artifact; licensed claim expands to all static L11 task directions; hunt moves to gated/dynamic or multi-layer mechanisms. *(Maps to: Refuted.)*
4. **Specificity:** T-vs-R McNemar p ≥ 0.05 with overlapping Tango CIs → **KILL** (specificity): nonspecific perturbation effect; no causal license for per-item task geometry. *(Maps to: Refuted.)*
5. **Licensed positive:** ΔM_T > 0.10 AND T-vs-R p < 0.05 AND stratum-consistent — defined as ΔM_T > 0 in **all three** strata (aggregate, A-first, C-first; strict — a zero or negative stratum fails consistency) — → **CONTINUE**, bench-scoped to EXP092-B. *(Maps to: Supported.)* The CONTINUE claim carries the full stratum table (aggregate / A-first / C-first × (T-vs-B, R-vs-B, T-vs-R) = **nine** cells, §5 item 5): a claim surviving only in aggregate is underlicensed and routes to step 6 sub-case (c).
6. **Otherwise → PIVOT** *(maps to: Not supported for the global claim)*, with named sub-cases:
   - (a) sign-heterogeneous movement across items/strata with null T-vs-R specificity — global per-item claim dead; conditional design (pre-registered covariate: baseline margin / coherence / per-item norm) is EXP095 material;
   - (b) **consistent wrong-direction steering** (ΔM_T < −0.10 with T-vs-R p < 0.05) — a causal channel exists (the constructor is mis-signed); the sign story is EXP095 material, never KILL;
   - (c) T-vs-R significant but stratum-inconsistent (e.g., aggregate-only positive) — underlicensed per LOG-4365 §3, conditional design is EXP095 material.

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted); the parenthetical mappings above bind each step to its permitted verdict. No banned language. No EXP093 claim is altered: the shared direction stays dead in all steps. The Law-#15 §0 "four outcomes" (KILL, KILL-specificity, CONTINUE, PIVOT) map to steps 3–6; steps 1–2 are procedure/power guards (Inconclusive/HOLD, Underdetermined), not outcomes of the question.

**Scope fence:** the EXP093 KILL is untouched; gated/dynamic mechanisms and multi-layer compositions remain separate EXP094+ material regardless of outcome.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post; any mismatch voids the run (Law #13).
- **G7 label-free constructor (Law #7):** the frozen constructor spec C-1 (§2.1.1) is audited per the G7.1–G7.5 procedure (§2.1.3) before any run; a label-informed per-item direction is a **disqualification**, not a positive. Constructor code hash, inputs, and label-contact attestation are persisted (§5 item 2).
- **G5-style exact-delivery probe:** per-item perturbation_ratio target ≈ 0.0474 (EXP093's measured ratio), tolerance band ±25% (0.0355–0.0593), verified to have reached the logits (margin-shift sign/magnitude recorded per item). **Aggregation rule (A4, pre-registered):** probe PASS iff ≥ 58/60 items sit within the band with margin shift recorded; otherwise probe FAIL → Inconclusive/HOLD (§3 step 1). Without this rule the probe→verdict trigger would be executor judgment.
- **Per-item margin CSV (Law #13 repair):** LOG-4352's non-blocking observation — EXP093 persisted aggregates only. This design writes per-item, per-arm (B/T/R) margins, top-1 decisions, perturbation_ratio, and margin shifts to disk. **Non-negotiable.** (Margin convention: EXP093's logit-margin, cited by reference — §5 item 1.)
- **Arm-routing rule:** the binding full-pairing rule (§3, F3 repair); no post-hoc re-routing — re-routing is structurally impossible under full pairing.
- **N_final feasibility computation (EXP079 lesson, A5 — recorded on paper):** a standing pre-reg gate — before the run, compute the minimum flips needed for McNemar p < 0.05 at n=60 and verify the design can reach DELTA_BAR. On paper: McNemar-exact significance at any n requires ≥ 6 unidirectional discordant pairs (b=6, c=0 → p = 2/64 = 0.03125 < 0.05; b=5, c=0 → p = 0.0625, n.s.), which is exactly the registered ≥6-flip movement gate; unlike EXP079's split-limited probe there is no structural cap (max achievable ΔM = 1.0 ≥ DELTA_BAR = 0.10). If the feasibility computation shows the bar is unreachable by construction, the run does not proceed (HALT_PROBE-style stop, not a silent edit).
- **Degeneracy gate (F4 repair):** single check — mean pairwise |cosine| over {d_i} ≥ 0.95 → Underdetermined (§3 step 2), computed before interpreting any verdict. Directional degeneracy is the powerless per-item test (the shared-direction case already killed → R4 Underdetermined). Norm uniformity does NOT trigger Underdetermined — norms are deliberately matched per item (§2.1.1), and a family with diverse directions and uniform norms is the ideal matched case; the genuine degenerate-norm case (all-zero d_i) is caught by the G5 delivery probe's per-item band.
- **Verdict discipline:** the §3 evaluation order above, five permitted verdicts with the step→verdict mappings, no post-hoc table edits; a design change is a new experiment number, never a silent edit.
- **$0 compute for this draft:** this document is on-paper only. No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, stratum, arm ∈ {B,T,R}, top-1 decision, margin, perturbation_ratio, margin shift vs B). Margin convention: EXP093's logit-margin m(h) = logit(target) − logit(foil), cited by reference (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md` §3, "the correct-margin") — not redefined at execution time.
2. Constructor manifest: frozen constructor code hash (SHA-256, G7.1), neutral-prefix string P₀, inputs, sampling seed (R arm), label-contact attestation (G7.1–G7.5 audit), per-item d_i norms and pairwise |cosine| summary (degeneracy gate inputs).
3. Δθ = 0 hash pre/post; environment + seed manifest (Law #13 reproducibility).
4. Delivery probe log: G5-style exact-delivery per-item results plus the PASS/FAIL aggregation decision (§4, ≥58/60 rule).
5. Stratum table: aggregate / A-first / C-first × (T-vs-B, R-vs-B, T-vs-R): ΔM, McNemar b/c/p, Tango 95% CI.
6. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition.

---

## 6. Reviewer open items (LOG-4365 §8) — CLOSED by LOG-4369 review; closures recorded here

1. **Constructor label-free audit (G7)** — CLOSED. The reviewer supplied the G7.1–G7.5 audit procedure and it is now embedded in the binding design: frozen constructor spec C-1 (§2.1.1) + G7 audit as disqualification bar (§2.1.3). The run does not start without a PASS attestation persisted in the constructor manifest (§5 item 2).
2. **Arm-routing rule wording** — CLOSED. The placeholder is replaced by the binding full-within-item-pairing rule (§3, F3 repair); the "N" label is retired from S4-9's design (S4-9's arms are B/T/R). There is no residual degree of freedom to stress.
3. **Norm-vs-collinearity tightening** — REJECTED, per the review (F4). The split's direction (separating the two concepts) was right; the OR was wrong. Norm CV < 0.05 must not trigger Underdetermined — it does not indicate a powerless test, it added a void condition the packet never licensed, and the genuine degenerate-norm case (all-zero d_i) is caught by the G5 delivery probe. Kept: the collinearity check only (§4 degeneracy gate, §3 step 2).

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not alter EXP093's signed protocol or any signed artifact; does not touch weights.
- Does not invent numbers — every value cites LOG-4365 or LOG-4352, except the constructor spec (§2.1.1–§2.1.3) which is a new frozen design licensed by the LOG-4369 review ("the science belongs to the repair lane") and the review-supplied aggregation example (A4, §4) adopted verbatim.

---

## 8. Next steps

Independent **Law #14 review** of this draft **has happened** (LOG-4369, verdict SIGN-WITH-FIXES; report: `research/innovation/REVIEWS/S4-9_PREREG_LAW14_REVIEW_2026-09-27.md`). Repair of findings F1–F4 + advisories A1–A7 applied in this lane (LOG-4370). Next: **independent delta re-verification** (separate lane, not commissioned here) → SIGN → CEO execution clearance → run (CPU, <0.005 T4-h). **Pilot NOT authorized until all three complete.**

---

*Draft prepared 2026-09-27 by the S4-9 pre-registration writer lane (LOG-4368), licensed by LOG-4366 commission. Repair of LOG-4369 findings F1–F4 + advisories A1–A7 applied 2026-09-27 by the LOG-4370 repair lane (still DRAFT, UNSIGNED — repair does not sign). On paper only, $0 compute, CPU-only design. No signed protocol file was edited; this is a new unsigned file.*
