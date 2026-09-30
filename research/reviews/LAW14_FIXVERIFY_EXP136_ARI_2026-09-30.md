# Law #14 Fix-Verification: B4/ARI Pre-registration Repairs

**Artifact verified:** `research/prereg/EXP136_PREREG_ARI_2026-09-30.md` (repaired draft)
**Against:** `research/reviews/LAW14_REVIEW_EXP136_ARI_PREREG_2026-09-30.md` (LOG-4849 review, F1–F2 required, A1–A2 advisory)
**Repair record:** LOG-4850 (4 judgment calls)
**Verification lane:** LOG-4851 (pre-assigned by the CEO). **Independence:** this lane neither drafted (LOG-4848), reviewed (LOG-4849), nor repaired (LOG-4850) the artifact.
**Verdict: PASS.** All required fixes correctly and completely applied. No amendments.

---

## Per-fix verification (all PASS)

### F1 — Direction-appropriate McNemar alternatives: PASS
- **T1:** one-sided H1: b > c (§3.3 line 79; §1 line 29; §2 line 46; §4 table line 88; §5.6 line 152). ✓
- **T2:** one-sided H1: c > b (same lines). ✓
- **C:** two-sided, as the attribution guard (same lines). ✓
- **Precedence** RUN-INVALID > HELD > KILL > CONTINUE intact (§4 line 139). ✓
- **Stale-reference sweep:** the single remaining directionless "one-sided" (line 20, §0.1) is the historical description of the superseded sprint bet — correctly untouched. The only "uniform one-sided H1" hit is the F1-fix annotation itself describing what was replaced. Zero live stale references. ✓
- **Statistical license:** T2 reachability example added (b=2, c=10 → p=79/4096≈0.019 by symmetry). ✓

### F2 — (h) extended to T1 (Phase 2): PASS
- **Phase 2 registered** (§3.4, "in two probe forwards (N_h = 2)") with asserts 7–13:
  - Assert 8: L1 activity (1/H)Σ_h‖w−w_base‖_1 > 0.01 ✓
  - Assert 9: boost direction — post-renormalization span mass strictly increases (valid for any base mass in (0,1)) ✓
  - Assert 10: absolute floor mean_h Σ_span w > 1e-3 (catches the ~0-base no-op) ✓
  - Asserts 11–12: renormalization |Σw−1|<1e-5, finiteness ✓
  - Assert 13: output propagation ‖o−o_base‖_2 > 1e-6 ✓
- **~0-base disposition:** the §3.4 NOTE explicitly routes Phase-2 assert failures to RUN-INVALID exit 44, not KILL — "the apparatus cannot test T1, so no verdict on the hypothesis is licensed." ✓
- **Budget guard (f):** 4·n + N_h = 242 at n=60 (one T2 probe + one T1 probe). Zero stale 241 / N_h=1 references. ✓

### A1 — Output-propagation asserts: PASS
Asserts 6 (Phase 1) and 13 (Phase 2) both assert ‖o−o_base‖_2 > 1e-6 on the L20 attention-submodule output, closing the detached-copy false-KILL path. ✓

### A2 — "C significant, T1/T2 flat" resolution: PASS
§4 explicitly resolves the configuration to KILL per precedence, with the [INTERPRETATION] that an effective undirected control with flat directed arms means routing is not the lever. ✓

---

## Ruling on the 4 judgment calls (LOG-4850)

1. **(h)-extension vs mass-gate — SOUND, no amendment.** The extension routes the degenerate ~0-base-mass case through the existing RUN-INVALID path; a mass-gate would have complicated the decision table without epistemic gain. The KILL bar's "both arms delivered" condition is now fully proven or the run voids. The cleaner option was correctly chosen.

2. **Strict-increase + absolute floor vs relative-ratio — SOUND, no amendment.** A relative-ratio boost test is undefined at ~0 base mass (3×0=0 — ratio meaningless). The strict-increase (3s/(1+2s)>s ⟺ s<1, true for all s∈(0,1)) verifies boost direction; the 1e-3 absolute floor catches the no-op. The combination is the correct specification.

3. **One-sided b>c for T1; systematic worsening → HELD — SOUND, no amendment.** Per Law #4, an effect in the unpredicted direction cannot license CONTINUE. HELD is the honest bin: it neither kills the axis (wrong if steering is real) nor continues it (a post-hoc shift). Minor note (non-blocking): the HELD branch's "sub-significant" label is slightly imprecise for a significant-wrong-direction effect, but the §3.3 NOTE documents the resolution explicitly and pre-registered, so the executor faces no ambiguity.

4. **1e-6 output-propagation threshold — SOUND, no amendment.** Under deterministic computation a detached-copy hook yields o=o_base bit-exactly, so any positive threshold trips it; 1e-6 sits far above float32 noise for typical activation magnitudes and far below any genuine intervention effect (an L1 weight change >0.01 propagates to output deltas orders of magnitude larger). Correctly sized.

---

## Overall verdict: PASS

All six required/advisory items (F1, F2, A1, A2) are correctly and completely applied, verified byte-by-byte against the LOG-4849 review. The decision-table bars, hypothesis, worth-it gate, and non-resurrection audit are untouched, as briefed. The four repair-lane judgment calls are sound; none require amendment.

**The B4/ARI pre-registration is launch-ready pending the CEO launch decision.** Single-lane fence held: verification only, no edits to the draft.

---

*Fix-verification: independent Law #14 lane, LOG-4851. $0 CPU, paper only.*
