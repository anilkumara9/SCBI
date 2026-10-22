# Law #14 Fix-Verification: B5/TGA-INT8 Pre-registration Repairs

**Artifact verified (exact filename):** `research/prereg/EXP138_PREREG_TGAINT8_2026-09-30.md` (repaired draft)
**Review under verification:** `research/reviews/LAW14_REVIEW_EXP138_TGAINT8_PREREG_2026-09-30.md` (LOG-4861, SIGN-WITH-FIXES)
**Repair record:** LOG-4862
**Verification lane:** LOG-4863 (pre-assigned, independent of the LOG-4860 drafting and LOG-4862 repair lanes).
**Date:** 2026-09-30. **$0 CPU, paper only. Verification only — no edits made.**

## Verdict: PASS

All required fixes (F1) and both advisories (A1–A2) are correctly and completely applied — verified byte-by-byte against the LOG-4861 review and the primary EXP131 artifacts. Decision table, tiers Q1–Q6, hypothesis, §3.5-equivalent derivations, and worth-it gate are untouched, as briefed. No amendments required. The pre-registration is launch-ready pending the CEO launch decision.

---

## Per-fix verification

### F1 (required) — 8 matched-norm randoms' provenance pinned: PASS

§3.3 step 5 now pins the randoms' provenance via re-derivation (the review's option (b)):

> "The 8 matched-norm randoms are re-derived verbatim from EXP131's pinned generation scheme — `torch.Generator()` (CPU), per-prompt `manual_seed(20260929_4724 + pi*100)` (pi = prompt index 0–9), drawing rand0–rand7 in order via `torch.randn(H)` and unit-normalizing, then scaling to norm budget B — so the quantized run uses the identical random directions as EXP131's records (records SHA-256 `867b123f0afadf335af5c2e2bcec3c274993b70157067aa1c88989e525ef581f`); no new randomness is introduced."

Byte-verified against `experiments/bundles/exp131_v1inj/run_exp131.py`:

| Draft claim | Primary source | Match |
|---|---|---|
| `torch.Generator()` (CPU) | line 499: `gen_r = torch.Generator()` (CPU is the default device) | ✓ |
| per-prompt `manual_seed(20260929_4724 + pi*100)` | line 502: `gen_r.manual_seed(20260929_4724 + pi * 100)` | ✓ exact |
| rand0–rand7 drawn in order via `torch.randn(H)` | lines 504–506: `for j in range(K_RAND): u = torch.randn(H, generator=gen_r)` | ✓ |
| unit-normalizing, scaled to B | line 507: `rand_dirs.append(u / u.norm())`; line 511: `delta = (B * arms[an]...)` | ✓ |
| 8 randoms | line 147: `K_RAND = 1 if SMOKE else 8` | ✓ |
| records SHA-256 `867b123f…f581f` | `sha256sum out/exp131_records.json` → `867b123f0afadf335af5c2e2bcec3c274993b70157067aa1c88989e525ef581f`; independently confirmed by the `exp131_records.json.sha256` sidecar file | ✓ triple-confirmed |

The Law #13 reproducibility gap is closed: the execution lane can reproduce the random set deterministically with zero ambiguity. The repair's choice of re-derivation over record-reuse is sound (maximizes comparability; the records hold labels + outcomes, not the vectors, per LOG-4862).

### A1 (advisory) — baseline-shift magnitude bound into the CERTIFIED paper statement: PASS

§4 now carries the licensed template verbatim:

> *"The TGA injection nulls (EXP131 ĉ < 0.1, ΔM_v1 = 0; EXP133 ΔM_geo = 0) reproduce under weight-only INT8 fake-quantization; X/10 quantized-baseline decisions shifted vs FP32 at α = 0, and the injection nulls reproduce against the quantized baseline."*

Followed by the explicit fence: *"The baseline-shift magnitude X/10 is bound into the statement — a large α = 0 shift with CERTIFIED cannot be stated as over-general precision-robustness without it."* The over-general reading the advisory warned about is fenced.

### A2 (advisory) — quantized-copy presentation mechanism: PASS

§3.3 step 2 now requires: *"The execution worksheet records the quantized-copy presentation mechanism (in-memory `state_dict` swap vs saved-to-local-directory as a model-id), per EXP110's pre-reg precedent (Law #13)."* Matches EXP110's pre-reg requirement.

---

## Scope check

- Decision table (CERTIFIED ⟺ Q1∧Q2∧Q3∧Q4; PIVOT ⟺ any fail; RUN-INVALID ⟺ Q5/Q6 fail): untouched.
- Tiers Q1–Q6, hypothesis (§1), §1.1 LOG-4528 argument, falsification tree (§5), breaking points (a)–(h) (§6), §7 fences, worth-it gate (§8): untouched.
- No TBD/TODO/FIXME/placeholder remnants in the draft (swept, zero hits).

## Boundary

Verification only. No edits to the draft, no execution, no number minted (EXP138 still provisional). Next: CEO launch decision.
