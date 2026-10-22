# Independent exact-artifact verdict review — EXP127 (TGA/TRANSIENT-GROWTH)

**Lane:** LOG-4699 (pre-assigned). **Verdict: BIND-WITH-CAVEAT** — EXP127's CONTINUE is correct from the exact artifacts; four documentation-precision observations below, all non-verdict-bearing.

**Reviewed:** `research/experiments/EXP127_TGA_TRANSIENTGROWTH_REPORT_2026-09-29.md` (execution lane LOG-4698) against the signed protocol `research/prereg/EXP_PREREG_TGA_TRANSIENTGROWTH_2026-09-29.md` and the raw artifacts in `experiments/runs/EXP127_tga/out/`. All recomputation was reimplemented from the protocol text; the executor's functions were not reused. $0 CPU. Read-only on all signed artifacts; this review and the LOG-4699 entry are the only writes.

---

## 1. Protocol hash (item 1)

`sha256(EXP_PREREG_TGA_TRANSIENTGROWTH_2026-09-29.md)` = `5dea0d419794fe6aa1fce056b9225625aa6ec3b55c57fab39bb7cb9e7d6e2882` — matches the signed post-fix value exactly. The console log shows the protocol hash verified (line 2) before any JVP (first prompt measurement at line 223).

## 2. Decision statistics independently re-derived (item 2)

- **Decision set:** prompts with both σ₁ and σ₂ converged = **n_d = 10 ≥ 8** (breaking point (b) satisfied).
- **Median R (even-n_d convention: average of the two middle order statistics):** sorted R = [8.0019, 8.0123, 8.0170, 8.0735, 8.1858, 8.2954, 8.3299, 8.3359, 8.4328, 8.5294] → **median R = 8.240640** — exact match to the report (6 decimals).
- **Median σ₁/σ₂ (same decision set, same convention):** **1.557689** — exact match.
- Internal consistency: R == σ₁/σ̄ per prompt (1e-9), σ₁/σ₂ consistent (1e-9); reported ranges R ∈ [8.0019, 8.5294], σ₁/σ₂ ∈ [1.5302, 1.5881] match the raw records.
- Bars: median R = 8.240640 ≥ 3 AND median σ₁/σ₂ = 1.557689 ≥ 1.5 → **CONTINUE** per §4, correctly read. R ≥ 3 is a registered ratio bar; no p-value needed (defect class 1 honored — none computed or quoted).

## 3. Convergence claims verified from traces (item 3)

Re-verified from the raw Rayleigh-quotient traces (not just the flags):

- **σ₁:** 10/10 converged — rel change in ρ_k below 1e-6 over the last 5 iterates, iters 20–27 (criterion: 1e-6/5 iters/≥20 minimum). σ₁ == sqrt(ρ_final) to 1e-6 on all prompts.
- **σ₂ (deflated):** 10/10 converged — rel change below 1e-4 over the last 5 iterates, iters 12–36 (criterion: 1e-4/5 iters/≥10 minimum). Every iterate is projected orthogonal to v₁ in the executor code (deflation per protocol §3.4); convergence flags match trace-verified values on all 10 prompts.
- The power-iteration implementation is correct: v ← MᵀMv/‖MᵀMv‖ via 1 JVP + 1 VJP per iterate, randomized isotropic start (no semantic content).

## 4. Hutchinson σ̄ arm (item 4)

- **K=64 Rademacher draws per prompt** on the same M, seeded (20260929 + prompt index); direct arm K=64 isotropic unit vectors, same M.
- Independent recomputation: σ̄ = sqrt(Tr_est/1024) matches reported σ̄ to 1e-9 (e.g., prompt 0: 1.1764099); direct median independently recomputed via even-n median = 1.156906, exact match; agreement |med − σ̄|/σ̄ ∈ [0.0022, 0.0263] ≤ 0.15 on all 10 prompts (diagnostic-only, not verdict-bearing).
- Stored vectors: v₁ per prompt (1024,) float32 and 64 direct uⱼ per prompt (64, 1024) in `exp127_vectors.npz` — shapes correct.

## 5. Budget cap (item 5)

- Per-prompt autograd product totals 264–318 ≤ 700 (breaking point / §3.6). Per-arm product counts present for all prompts (FIX-4): σ₁ = 2×iters, σ₂ = 2×iters, Hutchinson = 128 (64×2), direct = 64; sums reconcile to products_total exactly on all 10 prompts.

## 6. Δθ=0 (item 6)

- Backbone LOG-331 pre-pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` in worksheet and console (pre, per prompt-block).
- Post-pin: identical value in `worksheet.final.backbone_pin_post` and console tail ("backbone pin identical after all JVPs: Delta theta = 0"). Executor contains no optimizer, no loss, no backward into weights; all parameter tensors `requires_grad=False`. **Δθ=0 confirmed.**

## 7. Method-integrity notes (item 7)

- **x_{24} construction is correct:** the executor computes `x24_base = layers[23](hs[23], …)[0, -1]` — the real layer-23 module applied to the block-23 input, i.e., the block-23 output / block-24 input, exactly the protocol's §3.3 definition. The transformers-5.x hs[24] indexing trap was handled correctly (not via hs[24]).
- **Manual-span sanity diagnostic on the console log:** the final run shows `sanity max|f(z0)-x24_base|` = 2.20e-04 … 8.20e-04 on all 10 prompts (≤ 1e-3), matching the pinned JSON records. The machinery is self-consistent.
- The report's §5 note-1 parenthetical ("verified fln(module(hs[23])) == hs[24] to 0.0") exists in the executor only as a comment — see observation O2 below. The measurement object is unaffected (built from the real module call + validated by the sanity diagnostic).

## 8. Honest frame (item 8)

The report's §6 is complete and correct: the CONTINUE licenses a **signed GPU injection-test pre-registration** (new number, new Law #14 review, ĉ gate, rank-trend gate) — **no injection is licensed by this run**; no steering claim is made; the capability scoreboard stays at zero; no generality beyond Pythia-410m L20→L24 and the 10 pinned prompts is claimed; the cross-position Jacobian is named as unmeasured by design (§3.3/§10). Novelty N1.

## 9. Falsification-tree ordering (item 9)

Verified on the append-only console log (Law #9): protocol hash verified (line 2) → backbone pre-pin per block → per-prompt measurements (lines 223–295) → **raw records hash-pinned (lines 303–306: per_prompt=66f028ba…, vectors=9b527c02…, worksheet=0c0df797…) BEFORE R was read (line 310: "median R = 8.240640")** → backbone post-pin (identical) → decision set 10/10 → VERDICT: CONTINUE (line 311) → worksheet finalized. All four artifact hashes in the report's §4 table match the on-disk files exactly (recomputed independently). Breaking point (a)–(d): all satisfied.

---

## Caveats (non-verdict-bearing documentation-precision observations)

- **O1 — Descriptive range slips in §2/§3.** The report's ranges differ slightly from the raw records: σ₁ iters are 20–27 (report says 20–26); σ₂ iters are 12–36 (report says 19–36); direct-vs-Hutchinson agreement min is 0.0022 (report says 0.0083); sanity min is 2.20e-04 (report says 2.4e-04). Every registered guard criterion is satisfied on the actual values (≥20/≥10 minimums, ≤0.15, ≤1e-3); the ranges are descriptive only.
- **O2 — fln verification is comment-only.** The "verified … to 0.0" parenthetical in §5 note 1 has no executed assert in the executor (lines 278–281 are a NOTE comment). The x_{24} construction itself is correct and functionally validated by the sanity diagnostic. Precision overreach in a method note only.
- **O3 — Worksheet hash in the §4 table.** The table shows the post-verdict finalized worksheet hash (`f045413a…`) with "Pinned before R? yes". Strictly, the pre-R pin was the pre-verdict worksheet (`0c0df797…`), recorded honestly in `worksheet.final.artifact_pins`; the table conflates the two. Law #9 ordering itself is intact (console lines 303–310).
- **O4 — Undisclosed smoke-mode machinery validation.** The console log shows five single-prompt SMOKE MODE attempts before the real run; one failed the manual-span sanity (15.85 ≫ 1e-3), the span bug was fixed, a clean smoke passed (8.2e-04), and only then did the full run proceed. The banners explicitly state "no numbers minted, no verdict" — pre-tree machinery validation, so no verdict impact — but the repair is not disclosed in the report. Flagged for transparency; no erratum to the verdict needed.

---

## Verdict

**BIND-WITH-CAVEAT.** EXP127's CONTINUE — median R = 8.240640 ≥ 3 and median σ₁/σ₂ = 1.557689 ≥ 1.5 over the n_d=10 decision set — is correct from the exact artifacts. The dynamics-matched injection program is licensed for its GPU injection-test pre-registration gate, and nothing more. The four caveats above are documentation precision issues; none bears on the verdict.

*LOG-4699 appended to `reports/research_log.md` (continuity 4698→4699 verified, next-free confirmed).*
