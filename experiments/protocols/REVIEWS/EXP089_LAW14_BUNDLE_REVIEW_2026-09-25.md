# EXP089 — Independent Law #14 Bundle Review: SIGN-WITH-FIXES

**Reviewer:** Independent Law #14 Bundle Reviewer (reports DIRECTLY to the founder; verdict binding, not overridable by the CEO).
**Date:** 2026-09-25. **Logged:** LOG-345.
**Target:** `experiments/runs/EXP089_clm8b_falsifier/` (built LOG-344, CPU, $0 GPU).
**Signed protocol:** `experiments/protocols/EXP089_CLM8B_ADAPTATION_PREREG_SIGNED.md`
— SHA-256 recomputed by the reviewer: `87f2c47b7cbcec3db98cd88d7240b95ce7f49af9039aa0ae4ec251a2714c24cb`,
byte-identical to the LOG-338 record. **Signed file untouched; immutable.**

---

## Verdict: SIGN-WITH-FIXES

The bundle faithfully implements the signed protocol. Two precision fixes are
required before it is clear for CEO execution-clearance consideration. Neither
changes any registered endpoint, verdict, cost, or mapping — **no new
experiment number is triggered by the bundle fixes**. Real execution remains
NOT licensed (and is additionally blocked at the protocol level — see §6
ruling below).

---

## 1. Faithfulness verification (all independently executed, nothing on trust)

- **Test reruns (reviewer's own executions):** `python3 -m unittest test_exp089` →
  **28/28 PASS** (0.061s, numpy-only). Mock end-to-end produces a full report.
- **G1 (single-token):** `check_single_token_entity` asserts every A and C
  tokenizes to exactly one id; multi-token → `RunInvalid`. Matches §6
  (EXP075 guard reused; items never silently dropped). Test-confirmed.
- **G2 (frozen backbone):** `compute_state_dict_hash` verified against
  EXP077's own `get_hash()` (`experiments/runs/exp077/run_exp077.py:166-172`):
  sorted keys → CPU → float32 → `.tobytes()` → SHA-256. **Byte-identical
  algorithm.** Pre- AND post-extraction hash asserted against the LOG-331
  snapshot hash `ec276abe…e0ed`; mismatch → RUN-INVALID. Matches §6/Law #6.
- **G3 (phrasing balance):** reviewer's own run of `build_benchmark()` →
  exactly **30 A-first / 30 C-first**; `assert_phrasing_balance` enforces it.
  Matches §6.
- **G4 (instrument-health gate):** `adjudicate()` checks `max − min < 1e-4`
  over all 120 cosines FIRST → `RunInvalid` (RUN-INVALID, exit 3), never KILL.
  Test-confirmed with a deaf instrument. Matches §6 [Law #14 F1].
- **§7.1 TOTAL decision tree:** code implements exactly —
  `n < 38 → KILL`; `n ≥ 38 AND acc_Afirst > 0.5 AND acc_Cfirst > 0.5 → CONTINUE`;
  else → PIVOT. Tree is total over integer n ∈ [0,60]. Boundary tests
  (38/60 clean, 37/60, split-at-0.5, opposite tilts) all pass. Matches §7.1
  [Law #14 F2].
- **Bar sharpness:** independently recomputed via `math.comb` —
  P(X≥38|n=60,p=0.5) = 0.0259469… (registers 0.0260 at 3dp, as §7 states);
  P(X≥37) = 0.0462. The bar is sharp: 37/60 would not reject.
- **Tie rule:** exact float equality → toward C (foil), counted. Matches §6.
- **State text:** `state_text_of` cuts `"Premise:"` → (excluding) `" Question:"`.
  Reviewer verified all 60 items: no question/option-list leakage; each
  premise contains A exactly once and C exactly once (1:1 balance). Law #7
  statement (§5) holds as implemented.
- **Law #13 pins:** `model.eval()` explicit before extraction;
  `torch.no_grad()` around ALL extraction; `requires_grad_(False)` on all
  parameters. Present in code, not relied on as HF defaults. Matches §6 [F4].
- **Refusal gates:** forbidden flags (`--train/--gpu/--cuda/--finetune/…`)
  refused pre-parse (exit 2); real run without `--ceo-clearance` refused
  (exit 2); signed-protocol digest guard (`87f2c47b…`) enforced at startup —
  unsigned/mismatched protocol → refusal. All test-confirmed. Matches §8.
- **Benchmark provenance:** vocab lists, index arrays, prompt templates
  ported from the repaired EXP077 builder; only addition is the `phrasing`
  provenance field required by §6 G3/§7.1 (documented; follows EXP077's own
  "plus provenance fields" practice). The EXP077 support-prompt anti-cheat
  assert is intentionally not ported (EXP089 uses no support prompts) —
  documented in BUILD_NOTES.md. Acceptable.

---

## 2. RULING on the §6 protocol-level blocker — CONFIRMED UNSATISFIABLE

The builder's finding is **independently reproduced and confirmed**:

- Reviewer's own execution: the repo's repaired builder yields **12/60**
  `(ent, typ)` matches against `exp077_instance_records.json`; first mismatch
  at index 1 (rebuilt `('Venus','planet')` vs archived `('Mars','planet')`).
- The archive's SHA-256 recomputes to
  `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` —
  **character-identical to the protocol §4 record.** The archive is authentic;
  it is the *builder* that cannot reproduce it.
- No pre-repair builder is retained anywhere: no `.zip` files on disk, a
  single `run_exp077.py` (the repaired one). The mismatch is systematic
  (archive groups `Mars×6, Venus×6, …`; the repaired builder interleaves by
  index) — consistent with a different prompt-ordering in the lost
  pre-repair builder. This is the already-adjudicated LOG-3994 / LOG-4238
  provenance break, reproduced a third time.

**Ruling:** the signed protocol's §6 executor contract — *"the (ent, typ)
sequence matches `exp077_instance_records.json` byte-for-value, else
RUN-INVALID"* — **is genuinely unsatisfiable with the current repo state.
The signed protocol, as written, cannot execute a real run.** The bundle is
NOT at fault: it implements the mandated guard faithfully, and real execution
correctly exits RUN-INVALID (exit 3) per the protocol's own §8. Mock mode's
documented archive-check skip is legitimate (mock makes no archive claim).

This does not impugn the bundle's faithfulness verdict above. It is a
protocol-level fact the CEO/Mentor must adjudicate: per the constitution,
any design change requires a **new experiment number**.

---

## 3. Required fixes (precision; no endpoint/verdict/cost/mapping change)

- **F1:** Stamp the execution mode into `exp089_report.json`. The authoritative
  verdict artifact currently carries no mode field — a mock-run KILL is
  indistinguishable on disk from a real-run KILL. Add `"mode": "mock"|"real"`
  (from the extraction meta) to the report dict in both `run_exp089.py` and
  `score_exp089.py:main`. One-line-class change; prevents misreading of the
  primary artifact.
- **F2:** Pin `device_map="cpu"` explicitly in the `from_pretrained` call in
  `extract_real()`. The signed protocol §6 registers `device_map="cpu"`; the
  bundle currently relies on the transformers CPU default. Substance is
  identical (the runner refuses all GPU flags), but the registered contract
  should be implemented literally.

## 4. Observations (not fixes; for the record)

- O1: `adjudicate()`'s G3 `assert len(idx_a)==30` raises bare `AssertionError`
  on a tampered `.npz` rather than `RunInvalid`. Fail-loud is acceptable;
  G3 is already enforced at extraction. No action required.
- O2: Mock mode skips G1/G2 (no real entities/weights exist in mock). The
  guard *logic* is unit-tested with monkeypatched inputs. Acceptable and
  documented.
- O3: `extract_state_embeddings.py:main` accepts `--snapshot` override. The
  override path still enforces the G2 hash check, so a wrong snapshot fails
  closed. Acceptable.

---

## 5. Advisory to the CEO (not binding): the cleanest §6 repair

If adjudication goes the new-experiment-number route (the constitution's
default), the cleanest repair is to **define the bench as the hash-pinned
archived records** (`exp077_instance_records.json`,
`47281cd3…0585`) rather than as a rebuilt sequence: the archive's byte-identity
already guarantees it is the data EXP077 ran on, and the §4 hash record makes
the bench fully reconstructible. The alternative — recovering the
smoke-bench prompts — appears impossible (never archived; no code reproduces
them). Do NOT edit the signed EXP089 protocol; draft the repair under a new
number.

---

**License state:** real execution NOT licensed. After F1–F2 are applied and
diff-verified, the bundle is clear for CEO execution-clearance consideration —
with the standing expectation that the first real run exits RUN-INVALID on
the §6 guard until the protocol-level blocker is adjudicated. $0 CPU;
no weights or EXP077 artifacts were modified by this review (all reads
read-only; hashes re-verified).
