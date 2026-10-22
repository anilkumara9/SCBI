# Law #14 Independent Review — EXP133 Execution (GEOSTEER Geodesic Multistep CPU Pilot)

**Lane:** independent Law #14 execution reviewer. **LOG-4808** (CEO pre-assigned).
**Date:** 2026-09-30. **$0 CPU, paper only.** Read-only on the repo; no model forwards run by this lane (two minimal hook-probe forwards were run against the local weights to test the injection mechanism — no experimental data collected).
**Verdict: REJECT.**

**Artifacts reviewed in full:**
1. `reports/research_log.md` LOG-4807 (verdict entry).
2. `experiments/runs/EXP133_geosteer_multistep/out/exp133_records.json` (+ `.sha256`).
3. `experiments/runs/EXP133_geosteer_multistep/out/exp133_report.json`.
4. `experiments/runs/EXP133_geosteer_multistep/run_exp133.py` (executor).
5. Signed pre-reg + Amendments B/C; both void reports (attempts 1–2).
6. `~/workspace/SCBI/AGENTS.md` (house rules, read per runtime note).

**Independence:** I did not design, build, or run EXP133. I authored none of the reviewed artifacts.

---

## §0 — Headline finding

**The KILL verdict cannot stand. The injection never reached the readout.** The executor's forward hook (`layers[19].register_forward_hook`, adding the geodesic delta) does not modify `hidden_states[20]` (SITE) under the installed transformers 5.17.0. The decision readout therefore measured an un-injected state on every arm: cosine scores are **bit-identical** (0.000e+00 difference) across all 7 arms × 10 prompts. ΔM_geo = 0 and median margin behavior are vacuous — they reflect a blind tap, not an inert intervention. The correct category is **RUN-INVALID (apparatus defect)**; the hypothesis is **UNTESTED**.

This is not a close call. Evidence:

- **E1 (mechanism, reproduced twice):** Minimal probe — Pythia-410m, transformers 5.17.0 (confirmed), eval, no_grad, hook byte-identical to the executor's (`o[:, -1, :] += delta`, |delta| = 16.08). Result: `hidden_states[20]` diff norm = **0.0**, bit-identical = True. Meanwhile `hidden_states[21]` diff = 16.40, `hidden_states[24]` diff = 35.67, logits max-abs-diff = 4.02. The hook fires and the intervention propagates downstream — it simply does not touch the tapped index. (The `@capture_outputs` decorator in transformers 5.x shifted the captured-output indexing relative to the 4.x/5.0 convention the bundle was built against.)
- **E2 (records):** all 10 prompts × 6 injection arms show `max|Δcos| = 0.000e+00` vs base; `margin_disp` exactly 0.0 everywhere; `dm` all 0. A 0.5-norm injection producing bit-identical readouts to 1e-16 is impossible unless the tap is upstream of (or otherwise disconnected from) the injection.
- **E3 (records hash):** `exp133_records.json` SHA-256 = `5078f518bf21cd82c4e194711f35b212e1d64946c7013381e648461b0388442e` — matches the LOG-4807 pin exactly. The records are intact; the defect is in what was measured, not in record-keeping.

**What survives:** the ĉ_geo values (mean 0.03736427, verified from records; zero exclusions) are a *valid* measurement of local gradient geometry — `chat_at` computes the margin gradient via autograd through the cosine formula on the walk endpoints, independent of the hook. But ĉ measures "how the margin would change if the state moved," not "the intervention moved nothing." It cannot rescue the decision verdict.

---

## §1 — Checklist

1. **Records integrity — PASS (with the E3 caveat above).** Hash matches the LOG-4807 pin bit-for-bit. Spot-check: mean ĉ_geo recomputed = 0.03736427 ✓; exclusions [] ✓; budget_B = 0.50578119 verbatim ✓; pins present (protocol, amendment, weights_pre/post, v1_npz, v2_run1, v2_run2, bagg_reconstruction, bench) ✓. The arithmetic is correct; the numbers are vacuous for the reasons in §0.

2. **Breaking points — PASS as executed, but (d)'s audit and the norm audits do not detect this defect class.** (a) backbone pre+post exact ✓. (b1) v1 pin + 10/10 ids ✓. (b2) v2 run-twice bit-identical (`d633b897…` both) ✓. (b3) B_agg bit-identical to EXP131's pin ✓. (d) within amended 1e-4 ✓. Norm-budget audit all-pass ✓. None of these guards observes whether the hook's delta reaches the readout tap — the defect class "intervention delivered to the wrong site" is unguarded. New checklist item for the program (see §3).

3. **Decision-table application — the KILL branch fired on vacuous evidence.** Measured: ΔM_geo = 0, mean ĉ_geo = 0.03736 < 0.1, McNemar n.s. — the branch's conjuncts are literally satisfied. But ΔM_geo = 0 is entailed by the blind tap, not by the intervention. KILL-first precedence was honored; no PIVOT/INCONCLUSIVE corner applies (0 midpoint prompts ≥ 0.1). The table was applied correctly to numbers that do not mean what the table assumes. **The verdict is therefore REJECTED, re-categorized RUN-INVALID (apparatus defect).**

4. **Void history — both voids were genuine and properly handled; neither taints attempt 3.** Attempt 1 (b-trip: missing v2/bagg keys) and attempt 2 (d-trip: 1e-6 tolerance vs 4.83e-06 cross-device noise) both stopped per spec with hypothesis UNTESTED. Amendments B and C were narrow, independently signed, and correctly scoped. The void history is clean.

5. **Amendment discipline — PASS.** B and C touch only their stated breaking points; §4 everything-unchanged clauses verified against the signed pre-reg; no scope creep into the decision table or science. Laws #4/#5/#9 clean.

6. **Executor provenance — PASS with a note.** The (d) tolerance edit + docstring is the only functional change vs the smoke-passed executor (diff-verified per the lane report). The hook mechanism itself is byte-identical to EXP131's — which is precisely the problem (see §2).

---

## §2 — COROLLARY: EXP131's binding KILL is implicated

**This finding directly implicates EXP131 (LOG-4766, Law #14 SIGN, binding KILL).** Evidence chain:

- EXP131's executor (`experiments/bundles/exp131_v1inj/run_exp131.py:450`) uses the **byte-identical** hook mechanism: `layers[19].register_forward_hook`, `SITE = 20`, readout from `hidden_states[SITE]` (verified in code, lines 46/450/456).
- EXP131's full run executed on **transformers 5.17.0** (the version installed to restore the LOG-331 pin; listed in the run's full configuration).
- The hook blindness is a **transformers-version property**, not hardware: E1 was measured on CPU with 5.17.0; the Kaggle T4 ran the same 5.17.0. GPU vs CPU does not change `hidden_states` indexing.
- EXP131's reported `median_r = 1.0` is **exactly the blind-readout signature**: the ratio is `num/den` with `num = |margin_v1 − margin_base|`, `den = max_j |margin_randj − margin_base|`; the code's zero-denominator branch returns `1.0 if num == 0.0`. A blind tap gives 0/0 → 1.0 on every prompt → median exactly 1.0. A working tap with a truly inert v1 would give num ≈ 0 but den > 0 (random 0.5-norm injections move margins) → r ≈ 0, not 1.0.
- EXP131's "zero decision flips across all 11 injection arms" (80 random-direction injections) is likewise the blind signature — a working readout would show occasional random-arm flips.

**I do not overturn EXP131 here** — that is a CEO decision requiring its own lane (re-examination of EXP131's raw records for the bit-identical-cosine signature, which are hash-pinned but not all archived locally). But I record the implication plainly: **the program's headline GPU KILL rests on the same broken tap, and its binding status should be suspended pending re-examination.** The scoreboard's EXP131 KILL plot and any paper claims resting on it are affected.

**Causal story (new defect class):** the bundle was built/tested against transformers 5.0.0 (where the hook affected hs[20]); the 5.17.0 upgrade — required to restore the LOG-331 weights pin — silently shifted captured-output indexing (`@capture_outputs`), breaking the injection site without tripping any guard. Defect class: **library-version migration silently shifting activation indexing; breaking points must include a readout-sensitivity positive control** (e.g., assert the readout moves under a large random injection before the decision run).

---

## §3 — Required dispositions (for the CEO, not this lane)

1. **Re-categorize EXP133:** KILL → **RUN-INVALID (apparatus defect)**. Hypothesis UNTESTED. The GEOSTEER escalation branch is NOT retired — it was never actually tested.
2. **Suspend EXP131's binding KILL** pending a dedicated re-examination lane (check its raw records for the bit-identical signature; the records hash `e33a0eac…` is pinned).
3. **Fix the site:** future injection lanes must target the readout tap empirically verified on the installed transformers version (hook-effectiveness probe as a breaking point), not a hard-coded index carried across versions.
4. **Checklist addition:** Law #14 reviews of injection experiments must include a readout-sensitivity positive control (readout moves under a large random injection) — the defect class that survived two reviews, a fix-verification, and two amendments here.

**Fence held:** review only — no edits to reviewed artifacts, no repairs, no re-verdict, no execution. Lane writes: this review file + the LOG-4808 entry below.
