# EXP084 Independent Law #14 Bundle Review — 2026-09-25 (LOG-4317)

**Reviewer:** Independent Law #14 reviewer (reports to the founder; binding, cannot be overridden).
**Target:** implementation bundle at `experiments/runs/EXP084_newton_duel/` (R2 Newton-vs-gradient duel).
**Signed protocol:** `experiments/protocols/EXP084_R2_NEWTON_DUEL_PREREG_SIGNED.md` (immutable; not edited by this review).
**VERDICT: SIGN.** No load-bearing defects. The bundle faithfully implements the signed protocol and is eligible for the CEO's GPU-clearance decision chain (see §7).

$0 CPU, weights read-only, no GPU execution, no signed-artifact edits, no bundle edits.

---

## 1. Signed-protocol digest

Recomputed independently before anything else:

`811a390cf248922837ee6ee36f315ef29ecba40df63f38b60e51b14ebd8ef003` — **MATCH** (expected digest).

## 2. Test suites re-run by this reviewer (independent of the gate-closure record)

| Suite | Result (my re-run) |
|---|---|
| `python3 test_exp084.py` (script-style `check()` harness, not unittest) | **74/74 passed, 0 failed** |
| `python3 smoke_test.py` | **SMOKE RESULT: PASS** (40 SMOKE-OK checks incl. 17-check mock section) |
| `python3 mock_harness.py` | **17/17 mock scenarios pass** (8 scenario runs) |

All three match the gate-closure record's claims; I did not reuse its numbers on trust.

## 3. `adjudicate` vs §7 verdict-table precedence (independent adversarial probes)

I ran 10 fresh probes against the real `adjudicate` path (not the record's table):

| Probe | Result | Expected (§7) |
|---|---|---|
| n_defined=5 + all conjuncts fire | INVALID/UNDEFINED-LANDSCAPE | ✓ preempts |
| sens_p=0.5 + all conjuncts fire | INVALID/UNINFORMATIVE-PROXY | ✓ preempts |
| (a)∧(b)∧(c)∧(d)∧(e) | CONTINUE | ✓ |
| (a)∧(b)∧(c)∧(d)∧¬(e), kill criteria met | HELD(win-not-curvature-explained) | ✓ preempts KILL |
| (a)∧¬(b), (a)∧¬(d) | HELD(step-noise) | ✓ |
| med≤0, HL-upper<0.01, no conjuncts | KILL(flagship, cost-fair) | ✓ |
| narrow-KILL criteria met, flagship straddles | HELD(straddle) + secondary=`KILL(directional, narrow)` | ✓ (LOG-266 Fix 2 behavior) |
| narrow criteria fail | secondary=None (silent) | ✓ |
| INVALID(iii) + narrow criteria met | INVALID/UNDEFINED-LANDSCAPE, no secondary | ✓ (INVALID preempts) |
| hl_hi=0.01 exactly | HELD(straddle) — strict `<` | ✓ |

**Observation O1 ruling (binding): NOT A DEFECT — protocol-faithful.** The record's O1 notes the KILL row does not re-check conjunct (a). I verified the code implements §7 literally: the KILL condition is "CONTINUE not met AND median(ΔM_b−ΔM_d) ≤ 0 AND HL-upper < +0.01", and the protocol's own HELD rows only cover the sub-cases (a)∧(b)∧(c)∧(d)∧¬(e) and (a)∧(¬(b)∨¬(d)). So e.g. (a)∧(b)∧(d)∧(e)∧¬(c) with the kill prongs falls through to KILL **in the signed protocol itself** — the code faithfully reproduces it. The pathological corner (one-sided Wilcoxon (a) firing while sample median ≤ 0 and HL-upper < 0.01, e.g. small negatives swamped by large positive ranks) is mathematically constructible. This is a protocol-internal edge, not a bundle deviation. Under Law #4 the signed protocol is immutable — re-deriving the KILL row would require a new experiment number, which I cannot and do not order. **No bundle fix required; recorded here for the founder's awareness.**

Additional conformance points verified in `compute_statistics` ordering:
- INVALID(iii) short-circuits **before** `require_spearman_table(n_defined)` (LOG-266 Fix 3 binding order — no scientific machinery on the UNDEFINED-LANDSCAPE path). ✓
- `require_spearman_table(n_defined)` runs before all verdict machinery. ✓
- F2 short-circuit: on dead apparatus the duel contrasts are **not computed at all** (their tie-loud-halts cannot preempt INVALID(iv)); the None-valued results dict reaches `adjudicate` only via the already-fired INVALID(iv) row. ✓
- INVALID(i)/(ii) are run-halting exceptions raised before `adjudicate` — "no verdict", protocol-faithful. ✓

## 4. GPU-fatal surface

- **Lazy torch:** all imports function-local — `run_exp084.py:89` (`sha256_state_dict`), `:424` (`TorchBackend.__init__`), `:815` (CLI probe); `exp084_rng.py:44,64` (inside `generate_r_hat`/`derangement`, raising RuntimeError without torch). No top-level torch import anywhere; CPU build machine runs stdlib-only. ✓
- **Refusal posture (verified live, genuine `$?`):** `--run` alone → exit 2 ("requires --ceo-gpu-clearance"); `--run --ceo-gpu-clearance` → exit 2 ("requires --stage2-review-signoff"); both flags with no torch → exit 2 ("torch is not installed; the model loop needs the GPU node"). Nothing executes on any refusal path. ✓ (`--smoke` → PASS/exit 0; `--bogus` → argparse error, cosmetic difference from EXP083's help+exit-2, nothing executes.)
- **No hardcoded paths:** zero hits for `/home/`, `/Users/` in non-test bundle code. ✓
- **Spearman n=20–24:** verified live — `require_spearman_table(20)` raises `MissingSpearmanTableError` (a `FileNotFoundError` subclass), loud halt, no verdict; n=12 passes on the present tables (n=1..19 shipped). ✓
- **Budget:** `PassBudget` 240 fwd / 72 bwd, hard refusal at pass 241 / bwd 73, threaded through P0, probes, all five arms, and the permuted arm (covered in the 74/74 suite; the mock's exact pass accounting — fwd=228=24×8+18+18, bwd=72 — is under the ceiling). ✓

## 5. LOG-269 binding items — live in the bundle

- **D1 (probe-set deviation):** loudly logged at runtime (`PROBE-SET DEVIATION (stage-2 review): rebuilt (ent,typ) matches archived records at {a24}/24 ... adopted reading: verbatim EXP077 §3 rebuild, fixed indices 0..23`) and manifest-recorded (`probe_set{records_sha256, alignment_24, alignment_60}` in `finish_run`). The default `RECORDS_REL` resolves to the pinned archive; the R5d pin on the default path is SHA-verified on disk (`47281cd3…0585` matches the pinned file) and regression-tested. ✓
- **D5 (||g₀|| monitor):** per-item `log(f"[P0] item {i}: M0=… ||g0||=…")` live in the P0 arm (line 592). Zero gradient → `ApparatusError` loud; degenerate gradients → F2 fails → INVALID/UNINFORMATIVE-PROXY, never a verdict. ✓
- **F1 (first-run P0 archive-then-halt):** `check_identity` archives M0 then raises the dedicated `BaselinePrepassHalt` — verdict-clean pre-pass, not `InvalidRunError`; re-run replays the archive and enforces INVALID(ii) bit-for-bit (the self-certifying guard is gone). Covered by 6 evaluator tests. ✓
- **F2 (default RECORDS_REL):** one level up — `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`, confirmed correct on disk; the old two-levels-up GPU-blocking bug is gone and regression-tested. ✓

## 6. Scope drift and watermarks

- **No new endpoints, bars, or decision rules.** Decision thresholds are protocol-literal: (a)–(d) ≤ 0.05, (e)/sensitivity ≤ 0.10, `KILL_BAR = 0.01` strict `<`, INVALID(iii) at n_defined < 12, INVALID(iv) at sens_p > 0.10. One protocol-silent choice is explicitly documented in code, not silently slipped in: the F2 sensitivity contrast runs over all 24 items (arms (a)/(c) exist on all items; the duel subset applies only to arm (b) — this is a legitimate reading of §5, not a defect).
- **Watermarks honest:** manifest `bundle_stage` = "implementation-bundle ... GPU-dark"; `signoff_flag` explicitly NOT self-cleared; BUILD_NOTES retracted the stale "background generation" note (n=20..24 are GPU-node build artifacts with a binding pre-execution build command). No "GPU-ready" claim anywhere.
- **Queue line preserved:** K2 → EXP083 → EXP084 (GPU-sequencing only) in manifest and build notes.
- Signed protocol untouched (digest match §1). Bundle is git-tracked; working tree clean.

## 7. Clearance implication

LOG-269's pre-execution condition 1 — *"`--stage2-review-signoff` requires independent Law #14 re-verification of the fixes"* — is **satisfied by this SIGN verdict** (LOG-270 F1/F2/M1/M2 re-verified above). Conditions 2–4 remain open on the founder/CEO side: GPU-node Spearman tables n=20..24 built and integrity-checked, the two-invocation P0 pre-pass ordering executed on the node, and the D5 ||g₀|| log inspection before any verdict is treated as final. Granting the flag itself stays with the founder.

---

*— Independent Law #14 reviewer, 2026-09-25.*
