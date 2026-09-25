# Independent Law #14 Bundle Review — EXP083 (R1 RCPA kill pilot)

**Verdict: SIGN** (with three non-blocking documentation errata recorded below; none load-bearing)
**Reviewer:** Independent Law #14 reviewer, reporting directly to the founder. Binding; not appealable by the CEO.
**Date:** 2026-09-25
**Review target:** `experiments/runs/EXP083_rcpa_pilot/` — built 2026-09-24 under the LOG-257 implementation-bundle license (evaluator test suite + startup smoke test; NO GPU execution).
**Authority read in full:** the signed protocol `experiments/protocols/EXP083_RCPA_PREREG_SPEC.md` (read verbatim); the bundle files `exp083_endpoints.py`, `exp083_guards.py`, `exp083_position.py`, `exp083_random.py`, `run_exp083.py`, `smoke_test.py`, `test_exp083.py`, `manifest.json`, `requirements.txt`, `BUILD_NOTES.md`; the two readiness-lane records `E1_RESOLUTION_2026-09-25.md` and `GATE_CLOSURE_PRECEDENCE_CLI_2026-09-25.md` (treated as read-only context, re-verified independently — nothing in them trusted on authority).

## 1. Signed-protocol digest — CONFIRMED

SHA-256 of the signed protocol recomputed by the reviewer: `8a76834b42d9ef2058198f9a1925b192279d6a4e4fbab45da0b8d82c0527e9f8` — begins `8a76834b42d9ef20` as required. Matches `manifest.json` `protocol_sha256_prefix`. `git status` shows no modifications to the protocol vs the committed tree; the bundle build did not touch the signed artifact. **Gate 1 passes.**

## 2. Endpoint arithmetic — CONFIRMED (independently recomputed, not trusted)

- Re-ran `test_exp083.py` myself on the CPU build machine: **92/92 pass**. Re-ran `smoke_test.py`: **19/19 pass**. Both green on an independent execution by this reviewer.
- Wrote a separate analytic cross-check from the Tango 1998 constrained-MLE score (closed-form boundary-MLE at the flat table, independent bisection on a separately derived Z(δ) elsewhere). Results, matched against the protocol's canonical table and the bundle's output:
  - N=60 flat one-sided 95% upper: **0.043147** ✓
  - N=57 flat one-sided 95% upper: **0.045315** ✓ (bundle emits 0.04531478)
  - N=60 two-sided 95% half-width: **0.060172 → ±0.0602** ✓
  - N=57 two-sided 95% half-width: **0.063139 → ±0.0631** ✓
  - b=c=1 boundary one-sided upper: **0.056902** ✓
  - McNemar one-sided p at b=6,c=0: **0.015625** (exact integer arithmetic, 1/64) ✓
  - b=6,c=0,N=57 two-sided CI: **(0.0355, 0.2112)** ✓
- Every canonical value is computed by the bundle's code (the test suite asserts 6dp/4dp from the code path); the analytic cross-check reproduces them independently. The two-sided CI never decides the flat world (F1 correction honored in code: `KILL_gross` checks only `U < 0.05`; the flat world falls through to `KILL_flat`). **Gate 2 passes.**

## 3. Verdict precedence — CONFIRMED, with an explicit ruling on the sharpest judgment call

Re-ran all six flip-row probes through the bundle's own `adjudicate_verdict`:
- **MDE anchor** b=6,c=0,N=57 → **CONTINUE** (Δ̂=0.1053 ≥ 0.05, one-sided p=0.015625 ≤ 0.05), even though the independently computed two-sided CI (0.0355, 0.2112) straddles +0.05. **R2 reading confirmed in code.**
- b=c=0 + G-static fired on a validated apparatus → **RE-SKIN KILL** (preempts the flat kill). ✓
- SHA-256 failure + static fired + MDE flip data → **INVALID**, detail `INVALID(i)` (preempts everything). ✓
- b=c=0, N=57, no static → **KILL** via KILL_flat, U_1s=0.04531478 < 0.05. ✓
- b=0,c=8 → **KILL** via KILL_gross (CI upper −0.0355 < 0.05). ✓
- b=2,c=1 straddle → **HELD**. ✓
- Mutual exclusion holds by construction: KILL_gross (U<0.05) implies Δ̂<0.05 so CONTINUE is disjoint; KILL_flat (b=c=0) gives Δ̂=0, disjoint. INVALID order (i)→(ii)→(iii) asserted and green.

**RULING ON R2 (explicit):** The protocol's CONTINUE row pins its own firing condition — "Δ̂ ≥ +0.05 and exact one-sided McNemar (binomial) p ≤ 0.05 in the A_r direction and G-static passed and G-norm exclusions reported" — and pins the MDE anchor (b=6,c=0 → one-sided p = 0.015625) **inside the CONTINUE row itself**. I independently confirmed the anchor's two-sided CI at canonical N_final=57 straddles +0.05 (0.0355, 0.2112). If a straddling two-sided CI demoted CONTINUE to HELD, the MDE anchor pinned under CONTINUE would be vacuous — no anchor case could ever adjudicate CONTINUE. The protocol's Q2 states the CONTINUE criterion purely in one-sided terms, and its "one- vs two-sided use is pinned per row" discipline assigns the two-sided CI to KILL_gross and to the HELD-straddle catch-all for non-significant data. **The R2 reading — CONTINUE's conjuncts are sufficient, not demoted by a straddling two-sided CI — is the unique reading consistent with the protocol's own pins. The bundle's evaluation order (INVALID → RE-SKIN → KILL_gross → KILL_flat → CONTINUE → HELD) is licensed.** The protocol's §8 header listing "(RE-SKIN, KILL_gross, KILL_flat, HELD, CONTINUE)" is a listing, not an evaluation order; harmless, as the readiness lane already noted. **Gate 3 passes.**

## 4. Guards — CONFIRMED

- **G-norm:** `percentile_type7` implements linear interpolation (numpy.percentile default, type 7; position (n−1)·p). Exclusion is strictly-below (`<`, not `≤`) — a value exactly at the floor is not excluded (fixture-tested). Requires exactly 60 norms; non-finite input raises (→ INVALID(iii) upstream). Nearest-rank is rejected by name, matching R2. The "N_final=57 deterministic" claim is correctly treated as a property of the real data (computed at runtime), with the KILL_flat functional bar applied at the observed N_final either way (N_final=58 tie edge → 0.044568 < 0.05, still fires — verified).
- **G-static:** mean pairwise cos(r̂_i, r̂_j), bar **> 0.5**, with the chance anchor encoded in tests (0.5 ≫ 10/√1024). Fires only post-VALIDATED-apparatus (precedence in the adjudicator). Fault modes (non-unit, wrong dim, <2 items) raise → INVALID(iii).
- **G-curve:** report-only mean⟨r̂_i, ĥ_a,i⟩; never verdict-bearing. ✓
- **Pass-193 hard stop:** encoded in `PassCounter.use` — any allocation past MAX_PASSES=192 raises `PassBudgetExceeded`. Fixture-tested (fill to 192, then pass 193 refused). **Gate 4 passes.**

## 5. Position rule (§3.3) and Law #7 — CONFIRMED

`q_char_offset` searches the prompt **string** for `? Answer:` (M3 honored — text, not token IDs); `char_offset_to_token` maps char offset → token index via the tokenizer's offset table; `ans_pos = T−1`; q_pos strictly before ans_pos enforced. Missing anchor raises (no silent label-derived fallback). `locate_positions(prompt, token_char_spans)` touches only the prompt text and token spans — **no correctness labels, target/foil strings, or benchmark metadata are reachable in this code path**. The bridge appears nowhere. **Gate 5 passes.**

## 6. Seed scheme — CONFIRMED

`g_hat_seed(i) = 20260924 + i` (S0=20260924), 60 pairwise-distinct, deterministic. `generate_g_hat` constructs `torch.Generator`, `manual_seed(20260924+i)`, `torch.randn(1024, generator=g)`, unit-normalized — matching §4 exactly. **torch is the sole generator library:** the only `import torch` in the bundle is deferred inside `generate_g_hat` (GPU-node only) and inside `cmd_run`; no numpy import exists in any bundle module (docstring mentions only). Off-node, `generate_g_hat` raises `RuntimeError` — never silently falls back. **Gate 6 passes.**

## 7. CLI refusal gates — CONFIRMED (re-run by the reviewer, genuine exit codes)

- `--run` (no clearance) → `REFUSED: --run requires --gpu-clearance …` exit **2** ✓
- `--run --gpu-clearance` (no torch on build machine) → `REFUSED: torch is not installed …` exit **2** ✓
- `--smoke` → `EXP083 SMOKE: OK` (19/19) exit **0** ✓
- No GPU path is reachable without clearance; the full-run wiring refuses off-node. **Gate 7 passes.**

## 8. E1 claim check — CONFIRMED

- `experiments/protocols/STATISTICAL_PROTOCOL_V02.md` exists (STAT-V0.2, 2026-09-11). ✓
- No §A.2.5/§A.2.6 exist anywhere in `AMBITION_SPRINT_EXPDESIGN_2026-09-24.md` (only §A.2.1 is referenced elsewhere). ✓
- The binding smoke spec is §A.2 item 5; I read it verbatim: "≤12 passes on 3 items covering every arm once, asserting (i) the runner reaches the verdict code path, (ii) the identity arm reproduces the archived baseline bit-for-bit, (iii) throughput ≥80% of the booked model." The E1 record's quotation is accurate.
- Coverage: (i) → `test_verdict_path_reachability`, (ii) → `test_identity_vs_archive`, (iii) → `test_throughput_gate`; plus 9-pass inventory within the ≤12 cap, SHA pre-run check, INVALID precedence, pass-193 hard stop. All green in my re-run. **Gate 8 passes.**

## 9. GPU-fatal scan — CLEAN (fail-safe posture confirmed)

- No unguarded torch imports at module top level: the only two `import torch` sites are function-deferred (`generate_g_hat`, `cmd_run`). `run_exp083.py` top-level imports only stdlib + `exp083_guards` (stdlib-only). ✓
- `requirements.txt` lists torch + numpy — appropriate for the Kaggle GPU node (both preinstalled; the listing is documentation, numpy used only in a conditional test cross-check).
- No hardcoded local paths (`/home/hatch`, `/root/`, `/tmp/`) in any bundle module; the `PROTOCOL` constant resolves relative to the bundle directory. ✓
- The runner's full-run path is an intentional stub: even with `--gpu-clearance` on a torch machine it prints "licensed scope is bundle construction only (LOG-257). Execution is NOT licensed in this build." and returns 2. This is fail-safe, not a defect — the licensed scope explicitly excludes GPU execution wiring, which is a post-clearance build. **The founder's Kaggle node will need the execution wiring built after CEO GPU clearance; this bundle cannot and does not attempt it.**
- No quota can be wasted by this bundle: everything executable is CPU-only on synthetic fixtures; weights untouched ($0 CPU confirmed). **Gate 9 passes.**

## 10. Protocol integrity and scope — CONFIRMED

- The signed protocol was not modified by the bundle build (digest + git status verified, §1).
- No scope expansion: the bundle contains no new arms (sign-flip and permuted-r̂ remain deferred per §7/§9 — absent from the bundle, correct), no new bars, no new verdict rows, no α variation (α=1.0 pinned in `exp083_guards.ALPHA` and the manifest), seed scheme and intervention site (final-layer h_L, layer 23, ans_pos) match §2/§4, pass inventory (192 + hard stop 193) matches §6, verdict precedence matches §8+M1, canonical table matches §8/§13. `manifest.json` is accurate in every field checked, including `ceo_gpu_clearance: false`.
- One stale citation **in the signed protocol itself** (not the bundle, and this reviewer cannot alter signed text): §13 item 2 cites "evaluator test suite per §A.2.6" — §A.2.6 does not exist; the E1 record establishes §A.2 item 5 as binding. Recommend the CEO/mentor record this as a signed-protocol erratum (it changes nothing: the operative requirements are fully pinned in §6/§8). **Gate 10 passes.**

## Non-blocking documentation errata (NOT load-bearing; for the builder, not conditions of this SIGN)

1. `smoke_test.py` line 1 docstring: "(§6; §A.2.5/§A.2.6)" → "(§6; §A.2 item 5)". §A.2.5/§A.2.6 do not exist (E1).
2. `run_exp083.py` line 5 docstring: same fix.
3. `BUILD_NOTES.md` §R3: "(§8/§13.2 canonical values)" → "(§8/§13 canonical values)". §13.2 does not exist in the signed protocol.

These are comment-only stale citations; none affect computation, verdict logic, or quota safety.

## Disposition

**SIGN.** The EXP083 execution bundle faithfully implements the signed LOG-257 protocol within its licensed scope (evaluator test suite + startup smoke test), is fail-safe on the founder's Kaggle GPU node (refuses rather than executes wastefully), and is cleared for the CEO GPU-clearance stage. The bundle licenses nothing beyond its construction scope; no GPU execution is licensed by this verdict.

*— Independent Law #14 reviewer, LOG-4313, 2026-09-25.*
