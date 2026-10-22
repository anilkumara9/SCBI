# Law #14 Independent Review — EXP131 hook-fix amendment note (LOG-4821)

**Artifact under review:** `experiments/bundles/exp131_v1inj/AMENDMENT_HOOKFIX_2026-09-30.md` (DRAFT)
**Repair diff:** commit `eadbb17` (`experiments/bundles/exp131_v1inj/run_exp131.py`)
**Verdict: SIGN-WITH-FIXES** — one mechanical documentation fix (F1); the repair itself is approved.

## Independence
This reviewer did not repair the bundle, draft the note, or participate in LOG-4820. Review is paper-only, $0 CPU.

## Q1 — Mechanism: PASS
The note's Background states the Amendment-D mechanism as applied to EXP131: under transformers 5.17.0 the `@capture_outputs` snapshot hooks install in append order, so the chain on `layers[19]` was `[capture_hook, injection_hook]` — `hidden_states[20]` recorded the pre-injection block-19 output while the injection propagated downstream. This matches LOG-4809's findings exactly (Q1: hook byte-identity confirmed; Q2: hs[20] bit-identical with/without injection, downstream moved; Q3: `median_r = 1.0` is the 0/0 → 1.0 blind-tap signature). No misstatement. The "capture hook returns `None`, so downstream is byte-identical under either ordering" claim repeats what the LOG-4812 reviewer verified from the installed 5.17.0 source — correctly reused, not re-asserted on authority.

## Q2 — Narrowness: PASS
`git show eadbb17 -- experiments/bundles/exp131_v1inj/run_exp131.py` contains exactly two hunks: (i) the 28-line insertion of the §5b breaking-point (h) block; (ii) the 1-line change `register_forward_hook(hook_fn)` → `register_forward_hook(hook_fn, prepend=True)` (plus its comment). 28 insertions / 1 deletion, nothing else. The note's "verified by `git diff`: 28 insertions, 1 deletion, nothing else" is accurate. Site (`layers[19]`), readout line, dose B, arms, and decision table are untouched. The rejected `layers[18]` alternative is correctly identified as a science change and was not taken. Law #4 (no hypothesis shift) and Law #5 (no definition shift) hold.

## Q3 — (h) spec fidelity: PASS
Every Amendment D §3 parameter is faithfully implemented: seed `20260930` ✓; `‖δ_probe‖ = 16.0` (float32, run device) ✓; band `r ∈ [0.99, 1.01]` ✓; miss → apparatus-void message + `sys.exit(44)` ✓; placement after the base pass and before the first injection forward (§5b, ahead of step 6 and the injection arms) ✓; first bench prompt (`input_ids_list[0]`, i.e. "prompt 1") ✓; `tap_base` from the already-recorded `base_states[0]` (no extra forward) ✓; probe discarded from all records (`del` + comment) ✓.
One structural nuance, verified equivalent: the implementation registers a separate `probe_hook_fn` rather than reusing the injection `hook_fn`. Both use the same layer (`layers[19]`), the same `prepend=True` ordering, and the same clone-and-add pattern (`o = outp.clone(); o[:, -1, :] = o[:, -1, :] + δ`) at the last token — the delivery path tested is functionally identical to the injection path. This is a faithful implementation, not drift.

## Q4 — Re-clearance discipline: PASS
The note is explicit in two independent places: the Status line ("Does NOT re-clear EXP131 for execution — re-clearance requires an independent Law #14 review of this amendment plus a fresh CEO clearance, which are not granted by this document") and the final paragraph ("it does not re-clear the experiment. The repaired bundle awaits independent review and CEO clearance before any GPU execution."). Nothing in the note implicitly licenses a run. The Scope paragraph's ĉ = 0.0374 discussion is correctly fenced ("licenses no KILL") and the EXP133 CPU one-shot corroboration is explicitly denied rehabilitative force ("does not rehabilitate EXP131's GPU verdict"). Law #14 (challenge rather than defend) is satisfied — the note withholds every claim it has not earned.

## Q5 — Smoke evidence: PASS
LOG-4820 records the (h) PASS (`r = 1.0000001 ∈ [0.99, 1.01]`) as delivery evidence only — the deliverable the repair review needs. The appended LOG-4820 CORRECTION honestly discloses the kill-race (the smoke ran to completion; the kill was a no-op) and fences the smoke's KILL verdict as the RUNBOOK-documented 1-prompt/K=1 branch-exercising artifact ("it is NOT a result and is not presented as one"). The note itself correctly makes no claim about the smoke. Law #11 labeling in LOG-4820/its correction is clean ([FACT] vs [OBSERVATION] separated; the apology note documents the misreport rather than hiding it).

## Fix F1 (mechanical, required before CEO signature)
The note's Repair §1 says the fix restores "the ≤5.0 tap semantics the signed pre-registration assumed." The ≤5.0 attribution is unverifiable in this environment (5.0 not installed) — this is the same Law #11 point the LOG-4812 review raised as a non-blocking advisory on Amendment D, which the CEO then applied pre-signature (LOG-4813). For consistency: soften to "the post-hook tap semantics the signed pre-registration assumed [INTERPRETATION — the ≤5.0 attribution is unverified here]" or drop the version attribution. Narrative color, not load-bearing (validity rests on the verified 5.17.0 mechanism + probe), ~30-second edit.

## Disposition
**SIGN-WITH-FIXES.** Upon the CEO applying F1, the amendment note is approved as a narrow apparatus repair. It does not re-clear EXP131 — GPU re-execution still requires a fresh CEO clearance decision. The one-shot TGA-v₁ hypothesis remains UNTESTED.
