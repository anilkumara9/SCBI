# Independent Law #14 Review — EXP131 (TGA v₁ injection test) execution bundle

**Lane:** LOG-4730 (pre-assigned). **Verdict: SIGN-WITH-FIXES.**
**Bundle:** `experiments/bundles/exp131_v1inj/` (`run_exp131.py`,
`build_exp107_bench.py`, `exp077_support.py`, `test_decision_tree.py`,
`RUNBOOK.md`, `requirements.txt`, vendored signed protocol copy).
**Signed protocol under implementation:**
`research/prereg/EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md`,
post-fix SHA-256 `d85205f4ce2b1aadd2b2bda64397f7523e15958cf4fd8d903acccf0fd7f8bf52`
(hash re-verified by this review before reading the bundle — match).
**Scope:** bundle fidelity to the signed protocol. This review does not
re-litigate the signed design (that was LOG-4725); it verifies the
executor implements it.

## What was verified (fresh read of every bundle file + independent re-execution of the pure logic)

1. **Protocol hash-lock — PASS.** `PROTOCOL_PIN` is a string literal at the
   top of `run_exp131.py` (not loaded from config). Step 0 hashes the first
   existing protocol candidate and `sys.exit(42)` on mismatch — before model
   load, before any forward. The check is on the live execution path, not a
   dead branch. The vendored protocol copy in the bundle dir hashes to
   `d85205f4…f8bf52` (byte-identical to the signed file).
2. **Backbone pin — PASS.** `WEIGHTS_PIN` literal (`ec276abe…e0ed`,
   LOG-331); pinned before the first forward (mismatch → exit 42,
   quarantine) and re-pinned after the last forward (mismatch → exit 44,
   apparatus-void). `state_dict_hash` uses the canonical sorted-key float32
   method.
3. **Artifact re-pins — PASS.** `V1_NPZ_PIN` literal (`9b527c…13dc`);
   independently re-verified by this review: the file at
   `experiments/runs/EXP127_tga/out/exp127_vectors.npz` hashes exactly to
   the pin and carries 10 `v1__<prompt_id>` keys. Id alignment asserted per
   prompt id (miss → exit 44). v̂₂: K=40 fixed iterations (FIX-4),
   seed pinned (`20260929_4714`), `|v̂₂ᵀv̂₁| < 1e-6` asserted (fail →
   exit 44). B_agg: deterministic reconstruction from the EXP077 archived
   support set — this review confirmed the support reads use
   `hidden_states[21]`, byte-for-byte the index of EXP077's
   `TARGET_LAYER + 1` construction (code comments carry an off-by-one
   "output of block 20" label; the INDEX is what matters and it matches).
   Reconstruction SHA-256 recorded in the worksheet. **Zero
   finite-difference terms:** the only sensing ops are
   `torch.autograd.functional.jvp/vjp` (exact), mechanically asserted by
   `sensing_discipline_assert` (whitelist: exact JVP/VJP; blacklist:
   finite-difference gain ratios) — EXP128's death does not transfer.
4. **Budget B — PASS.** `B = 0.01 × median ‖y_{20,last}‖` computed from base
   forwards and logged BEFORE the first injection forward. Per-arm norm
   audit: every injection arm's `‖δ‖` checked against B within 1e-6
   relative (fail → exit 44, apparatus-void). The audit measures the same
   float32 quantity that is injected — no precision slip between audit and
   act.
5. **ĉ gate — PASS.** Exact-VJP margin-gradient alignment computed on the
   base (no-injection) forward, before any injection forward — no
   circularity. `ĉ < 0.1 → KILL`; ≥3 degenerate `‖g‖` exclusions →
   apparatus-void. Matches protocol §3.7.
6. **One-shot only — PASS.** `inject_forward` is a single forward hook per
   arm; no loop, no adaptation, no dose escalation anywhere in the script —
   EXP129's KILL does not transfer.
7. **Verdict arithmetic — PASS (independently re-executed).** This review
   extracted `decision_tree` and `binom_sf_ge` and ran all branches
   without torch: **11/11 pass** — CONTINUE, KILL (ĉ / inert / flat-trend /
   r-bar-unmet / p-unmet), HELD (margin gain without flips), RUN-INVALID
   (B_agg drift, precedence over KILL), APPARATUS-VOID (precedence over
   everything), KILL precedence (ĉ before inertness). McNemar one-sided
   exact table matches the protocol's §3.7 a-priori table on all 7 entries.
   FIX-1 (global-best random arm, lowest-j tie-break) and FIX-2 (0/0 → 1,
   x/0 → +∞, disclosed) implemented as pinned. B_agg flip → exit 43
   RUN-INVALID with records still written and pinned (honest invalid-run
   capture). CONTINUE is conjunctive as signed.
8. **Δθ=0 — PASS.** No optimizer, no loss; `requires_grad_(False)` on all
   parameters; `model.eval()`; the ĉ gate's `autograd.grad` is a backward
   through the frozen graph into an activation, never into weights
   (breaking point (f) as signed).
9. **Injection/readout site fidelity — PASS.** Injection hook on
   `layers[19]` (output of block 20 = `hidden_states[20]`) — the exact
   frame EXP127's v₁ artifact was measured in (`h20_in = hs[20]` in
   `exp127_execute.py`), and the exact hook site of EXP129's executor
   (the FIX-2 budget lineage). Readout is the H1/H6 §3.3 recipe verbatim
   at layer 20 (state and option embeddings both `hidden_states[20]`),
   as the signed protocol §3.6 licenses ("everything else in the H6
   pipeline is identical").
10. **Smoke interpretation — GAP (see FIX-1).** The reported smoke result
    (end-to-end pipeline OK; KILL via ĉ = 0.0634) is correctly a
    branch-exercising artifact of the 1-prompt/K=1 configuration, but the
    RUNBOOK does not say so.

## Fixes

**Founder-facing (launch-gating — fix before the bundle goes to the founder):**

1. **RUNBOOK must frame the smoke KILL.** Add, next to the `--smoke`
   pre-flight step: the smoke run is expected to print a KILL (the
   1-prompt/K=1 configuration degenerates the ĉ statistic by design —
   the build lane observed ĉ = 0.0634); this verdict is a
   branch-exercising artifact, NOT an experiment result; only the full
   run's verdict counts. Without this, the founder may read the smoke
   KILL as the experiment's answer and never run the real experiment.

**Verdict-immaterial:**

2. **RUNBOOK Step 1 is stale.** It instructs the founder to "copy the
   signed protocol file into this directory before uploading" — the
   bundle already vendors it (hash-verified identical,
   `d85205f4…f8bf52`). Replace with: "already included — verify its
   SHA-256 matches `d85205f4…f8bf52` before uploading."
3. **requirements.txt lists `scipy`, which nothing imports** (verified
   by grep across all four scripts). Remove the line to keep the
   founder's install lean. Harmless either way.

## Interpretation note (not a finding — for the execution report)

The readout sits at `hidden_states[20]`, the same tensor the injection
perturbs (the licensed H1/H6 §3.3 recipe). The injected δ is therefore
directly present in the readout state; the displacement statistics
measure v̂₁'s alignment with the margin gradient at the injection site
(the B cancels in the r ratio), not amplification through the L20→L24
propagator M. The ĉ gate and the singular-rank trend gate are the
load-bearing instruments under this readout — this is the signed design,
and the verdict bars are coherent as a test of v̂₁'s decision-relevance
at the injection site. The execution report must not describe a
CONTINUE as confirming transient-growth steering.

## Verdict

**SIGN-WITH-FIXES.** The bundle faithfully implements the signed
protocol on all ten checks. It is founder-ready after FIX-1 (smoke-KILL
framing) and FIX-2/FIX-3. No REJECT-level defect. Execution remains
founder-gated on user hardware; the executor's hash-lock refuses any
tampered protocol.

*Review-only lane — licenses nothing. Next in the launch chain:
fix-verification → bundle commit → founder GPU run.*
