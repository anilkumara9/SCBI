# Law #14 Independent Execution Review — EXP131 (TGA v₁ injection)

**Lane:** LOG-4766 (pre-assigned). **Verdict: SIGN.** Binding.

**Reviewer role:** independent — I did not build, patch, or run the executor. Evidence is the browser operator's execution report (treated as reported evidence, checked for internal consistency against the signed protocol and the repo's git history). The raw records file (`exp131_records.json`) was not available to this reviewer at review time; the records_pin is checked for self-consistency only (see §3).

## 1. Decision-tree fidelity — PASS

Signed protocol `EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md`, §4 falsification decision tree, ĉ-gate node: "**ĉ ≥ 0.1** — miss → **KILL**". The gate statistic is the mean ĉ over the 10 prompts (≥3 exclusions → apparatus-void).

- Reported: ĉ = 0.03741576759203537, **0 exclusions**, 10/10 prompts.
- 0.0374 < 0.1 → the tree routes to **KILL** at the ĉ gate. The executor's verdict reason — "decision-orthogonal amplifier: c_hat=0.0374 < 0.1" — matches the tree's licensed KILL rationale verbatim ("the amplified direction is decision-orthogonal — an amplifier of nothing the task cares about", §[DEFINITION] ĉ).
- The tree also requires CONTINUE to be conjunctive (ĉ ≥ 0.1, median r ≥ 2, ΔM_v1 > 0 with McNemar p ≤ 0.05, rank-trend holds, ΔM_Bagg = 0). The forward metrics independently fail every conjunct: median r = 1.0 < 2, ΔM_v1 = 0, McNemar p = 1.0, rank-trend = false. The KILL is over-determined: both the gate and the metric branches agree. No branch ambiguity.

## 2. Metric consistency — PASS

All reported metrics cohere with a fully inert apparatus:

- All 10 items r = 1.0 → per the bundle review's FIX-2 (0/0 → 1, disclosed), no displacement on any arm. Consistent with ΔM_v1 = 0, ΔM_Bagg = 0, best_random_arm = j0 with 0 flips on all 8 random arms.
- McNemar b = 0, c = 0, n = 0 → p(one-sided) = 1.0. Zero discordant pairs: neither v₁ nor the best random arm flipped anything. Coherent with the inertness above.
- ĉ = 0.0374 with 0 exclusions: no degenerate-‖g‖ exclusions, so the gate is a clean read of the mean, not an artifact of exclusions.
- Budget B = 0.50578119 recorded before injection; norm-budget audit 110/110 arms within 1e-6 → the dose fence held; the verdict measures direction, not dose.
- v2 derivation: K=40 fixed, |v2·v1| ~1e-9 OK on all 10 prompts → the registered orthogonality assert held.

## 3. Guard integrity — PASS (with one evidence limitation)

- **Pin chain:** protocol pin OK at executor startup ("protocol pin OK"); bench pin OK; v₁ artifact pin OK (9b527c02…); backbone LOG-331 pin `ec276abe3902fab0…` OK pre AND post → Δθ=0 held. The transformers 5.17.0 environment match (the version the LOG-331 pin was recorded under) is a legitimate environment requirement, not a guard bypass — the executor refused to run under 5.0.0 rather than proceed with a mismatched pin.
- **Sensing discipline:** assert PASS — exact JVP/VJP only; no finite-difference terms. Matches the protocol's barred list.
- **B_agg null-control:** ΔM_Bagg = 0 → the dead control replicated EXP077; no apparatus-drift RUN-INVALID.
- **Raw-record hash-pin:** records_pin `e33a0eac4f492eb53c441e00899023a2ee6bdb69f11340f8767644466283b1d6` reported to match the content of `exp131_records.json.sha256` in `out/`. **Limitation:** I could not independently recompute the pin (records file not forwarded to this reviewer). The pin is self-consistent within the report; flagging as reported-evidence, not independently verified bytes.

## 4. Executor provenance — PASS, does not invalidate the pre-execution SIGN-WITH-FIXES

Two post-release patches, both verified in the repo's git history (`652d2d4`, `f386972`) as device-placement-only:

- **LOG-4762 (652d2d4):** K/V/pos allocated on `device` in `build_clamped_kv`; device-safe `as_tensor` in `rotate_vec`; loop-local `v1d = v1[pid].to(device)` in the v2 loop. Placement only — no bar, threshold, seed, norm, or decision-logic change. `.to(device)` on float32 tensors changes no values.
- **LOG-4764 (f386972):** one line — `torch.randn(H, generator=gen_v2, device=device)` → `torch.randn(H, generator=gen_v2).to(device)`. This *restores* the reviewed executor's exact random stream: generation on CPU with pinned seed `20260929_4714`, then placement move. CPU-smoke verification recorded byte-identical |v2·v1| = 5.588e-09 before and after, so the v2 derivation is numerically identical to what the reviewed executor specified. The intermediate form (LOG-4762's version) would have produced a *different* stream on CUDA had it run — it never ran successfully; the executed form is the byte-identical one.

Both patches were required by the GPU environment (the bundle was CPU-tested only) and touch nothing the SIGN-WITH-FIXES review certified: protocol bars, ĉ gate, decision tree, budget, seeds, sensing whitelist, and pin chain are all untouched.

## 5. Verdict

**SIGN.** The EXP131 execution is valid: guards held, the pin chain is intact, the decision tree was walked in Law #9 order, and the KILL verdict follows from the licensed ĉ gate (0.0374 < 0.1) with metric-branch corroboration. The verdict stands.

**Headline:** EXP131 KILL — the dynamics' own leading singular direction is decision-orthogonal at the injection scale (ĉ = 0.0374); zero flips across all 11 injection arms. The TGA injection program's licensed hypothesis is refuted; the transient-growth amplifier steers no decisions.

*Independent review — binds under Law #14. Review-only lane; licenses nothing downstream.*
