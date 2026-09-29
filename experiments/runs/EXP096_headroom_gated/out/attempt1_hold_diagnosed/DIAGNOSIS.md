# Attempt 1 — STEP-1 HOLD diagnosis (2026-09-28)

**HOLD:** 21/42 gated delivery rows out of band (>2) — common-cause suspected.

**Diagnosis (executor bug, not a protocol defect):** the executor built the
R-arm directions g_i at norm d_norm_alpha8 (= 0.3792·||h||, already T(8.0)'s
per-item norm) and then injected `8 * g_i`, double-scaling B_wrong to ratio
~3.03 — outside the [0.2844, 0.4740] band on all 21 B_wrong rows. The 21 T
rows were correctly in band (0.3792).

**Fix:** inject `g_i` as-is (its norm already targets T(8.0)'s per-item norm,
per protocol §2.1); fixed the delivery probe, the manifest, and the sweep;
added an explicit norm-tie assertion after construction.

**Impact:** no injection passes were executed before the HOLD (only B/Ref
foundation passes, all gates passing: G7.1, gate-manifest 21/21, G0,
thread-pin, Δθ=0 pre, B agreement 60/60, degeneracy sanity 0.7923). No
verdict-relevant data produced. Re-run authorized under the protocol's
diagnosis lane (HOLD → diagnose → fix → re-verify all guards), not a silent
re-run.
