# Adversarial Review — EXP075 Execution Bundle (Law #14)

**Reviewer:** Adversarial Reviewer (Law #14)
**Date:** 2026-09-23
**Bundle reviewed:** `experiments/runs/exp075/` — `run_exp075.py` (752 lines),
`evaluate_exp075.py` (278 lines), `test_evaluate_exp075.py` (105 lines),
`requirements.txt`, `RUNBOOK.md`, `UNTESTED_ASSUMPTIONS.md`
**Reviewed against:** `experiments/protocols/EXP075_SUBSPACE_BRIDGE_PREREG_SPEC.md`
(SIGNED), `reports/adversarial_review_exp075_prereg_2026-09-23.md` (SIGN),
`experiments/scripts/run_exp066_pythia410m_replication.py` (historical support/
benchmark procedure), `reports/research_log.md` (historical baselines),
`AGENTS.md` (14 laws)
**Method:** full read of all six bundle files + independent grep/diff verification
of every load-bearing claim (not on trust). No code executed (no GPU/torch on
this machine); `py_compile`-cleanliness taken from the builder's LOG-096 record.
**Bundle untouched. No results invented. No primary artifacts modified.**

## VERDICT: **CLEAR-WITH-FIXES**

2 MAJOR + 2 MODERATE + 5 MINOR. All fixes are implementable without touching the
signed protocol, without new conditions, and without threshold changes. The core
harness — frozen backbone, gates, projections, archives, evaluator precedence —
is faithful. **The bundle is NOT cleared for execution until every MAJOR and
MODERATE fix is applied and a focused diff re-verification signs off.**

---

## 1. Rulings on the builder's five self-flagged uncertainties

### U1. Forward-budget mismatch — NOT load-bearing; acceptable IF disclosed with the corrected total
The spec's "420 forward passes" is itself an undercount: it budgets only the
condition phase and calls subspace construction "vector arithmetic (negligible),"
but §3.1's support procedure requires **300 model forwards** (150 pairs × rel/neu)
that the spec forgot. True total: 300 (support) + 2 (B_wrong) + 60 (baseline) +
720 (6 conditions × 60 items × base+modified for KL) = **≈1,082 forwards**.
The extra 360 KL-duplicate forwards do not change any estimand — the
unintervened comparator is the correct one for the KL — and ≈1,082 short
forwards on a T4 (≈10–20 min) is still far inside free-tier quota. The excess is
therefore **acceptable**, but the bundle currently states three different wrong
numbers (spec's 420; RUNBOOK's "420 + ~300"; `--allow-cpu` help's "~720").
**Required fix (F3, MODERATE):** correct all three to the honest ≈1,080 figure.
Caching the baseline forward is a permitted optimization, not a requirement.

### U2. `--allow-cpu` override — KEEP; the discouraged-hatch precedent is acceptable
Verified by grep: the signed spec contains **no** "must refuse to start without
CUDA" language (the only "CPU" occurrence is the SHA-256 "CPU, float32 bytes"
line). The refusal is therefore bundle policy + EXP070 precedent (which was
cleared), not a spec mandate — the task brief's premise is corrected for the
record. The hatch is loud (strong warning, Law #8 framing), discouraged, and any
CPU run is self-identifying via the `env_manifest.device` field archived in
`exp075_results.json`. Removing it gains nothing; keeping it mirrors the cleared
EXP070 bundle. **No fix required.** (Budget figure in the hatch text still needs
the F3 correction.)

### U3. Support-only path isolation — ACCEPTABLE as a reasoned, disclosed deviation
The spec's §3.1 whitelist presupposes support artifacts on disk ("support
artifact directories"). This runner reads **zero files** — support deltas are
generated in-script — so a filesystem whitelist is vacuous. The no-peeking
invariant is instead achieved more strongly: `build_subspace_S()` is called
**before the benchmark exists** (ordering), receives **only** the support deltas
(signature-enforced — test items are not in scope at call time), and the entity
domains are structurally disjoint (person names vs planets/elements, verified
against the historical script). **No fix to the mechanism required.** **Required
fix (F7, MINOR):** the runner's docstring claims this substitution is
"documented in UNTESTED_ASSUMPTIONS.md" — it is not there. Add the disclosure.

### U4. Benchmark identity — provenance is STRONGER than the builder claimed; the caveat is false
`UNTESTED_ASSUMPTIONS.md` B.3 claims "no historical EXP066 construction script
was available for comparison." **False.** `experiments/scripts/run_exp066_pythia410m_replication.py`
exists, was cited by the prereg review itself, and contains the full support and
benchmark constructions. I diffed both against the bundle:
- **Support:** entity lists, `triples_indices`/`quads_indices` (all 15+15),
  rel/neu prompt templates, `q_opts` parity (`i % 2 == 0`), `v_hat_k =
  normalize(mean(normalize(delta_h)))`, `B_agg = normalize(Σ v_hat_k)`,
  `B_perp` seed 9876, `B_wrong` Paris-capital prompts, `hidden_states[target_layer+1]`
  indexing — **all item-identical**.
- **Benchmark:** entity lists, index lists, templates, `target_first` parity
  (planets `i%2==1`, elements `i%2==0`), `is_rev` alternation (`i>=8` planets,
  `i>=7` elements — matching the runner's `i<8`/`i<7`), target/foil assignment —
  **item-identical prompts** (instance IDs and metadata fields differ only).
**Required fix (F4, MODERATE):** rewrite B.3 to record this verification instead
of the false caveat. This finding *upgrades* the bundle; it is not a blocker.

### U5. Multi-token entity handling — early-abort is the RIGHT choice, but it is NOT implemented
The spec is silent; EXP066's procedure assumed single-token entities. Of the two
candidate behaviors, early-abort matches the spec's intent better than silent
first-subtoken truncation (loud > silent, per the program's own F1 lesson).
**However:** grep over `run_exp075.py` for `multi.token|single.token|subtoken`
returns **zero hits**. The code silently takes `tokenizer.encode(...)[0]` at
lines 458 and 652. Meanwhile `UNTESTED_ASSUMPTIONS.md` A.1 claims "the runner
**aborts early if ANY support or test entity is multi-token**, before
constructing S," and LOG-096 repeats the claim. **A documented guard that does
not exist is a Law #2-adjacent falsehood.** **Required fix (F2, MAJOR):**
implement the early-abort in code (small, no protocol change — see fix list),
checking the exact strings the code encodes.

---

## 2. Findings (all must be fixed before execution clearance)

### F1 [MAJOR] — The (f) kill criterion can never fire: `evaluate()` deletes the pre-registered falsification branch
`evaluate_exp075.py` L158–162:
```python
if branch in ("f", "g"):
    c5 = norm["C5"]
    if sig_positive(c5):
        return "h"
    return "i"
```
Branch `"f"` is **unreachable as a return value** — `RULINGS["f"]` and
`BRANCH_NAMES["f"]` are dead text. For the exact-kill cell (C4 `b=c=0`, C3
valid, C5 null) the terminal ruling is `(i)` "non-localizable," whose text says
"**neither (e) nor (f) fires**." This **directly contradicts §7.0**, which the
spec designates the "**single source of truth**" / "Canonical criterion":
"If C4 yields ΔM ≡ 0 (b = c = 0) while C3 yields ΔM > 0 (p < 0.05), then H_sub
is FALSIFIED." Routing the kill into a ruling that denies the kill is a
post-hoc weakening of the falsification criterion — a **Law #4** violation,
even though it happens at bundle-build time rather than after seeing data.
The spec's own (h) text ("Strengthens (f)'s interpretation") presupposes (f)
fires; only (i)'s "neither (e) nor (f) fires" clause is inconsistent with (f),
and it is literally true only for the C4=(g) sub-case.
**Required fix — `evaluate_exp075.py`:**
- L158–162: when C4 is the exact-kill cell, return `"f"` as the terminal
  branch. `(h)`/`(i)` become **supplementary localization notes** for the (f)
  region, not replacements:
```python
if branch == "f":
    return "f"   # §7.0 canonical kill; (h)/(i) appended as notes in report()
if branch == "g":
    c5 = norm["C5"]
    if sig_positive(c5):
        return "h"   # "upgrades it toward (f)" — unchanged
    return "i"        # "neither (e) nor (f) fires" — literally true here
```
- `report()` (L212): for `bid == "f"`, after printing `RULINGS["f"]`, append
  the supplementary note: if C5 significant → append the (h) text ("wrong
  room — strengthens (f)'s interpretation"); else → append a localization
  note with the (i) content **minus** the "neither (e) nor (f) fires" clause
  (since (f) did fire), e.g. "neither S nor S⊥ alone rescued at unit-norm."
- Module docstring "Conservative readings" bullet and `run_exp075.py`'s
  docstring "Branch (i) operationalization" bullet: rewrite to describe (f)
  as terminal with (h)/(i) supplementary.
- `test_evaluate_exp075.py` L75: `"f: C4 b=c=0, C5 null"` must expect `"f"`
  (not `"i"`); L78: `"h: C4 b=c=0, C5 rescues"` must expect `"f"` (branch
  stays (f); the (h) note is report-level — add a `report()`-level assertion
  for the supplement). The (g)→(h)/(i) tests (L82–91) are correct as written.

### F2 [MAJOR] — Multi-token early-abort claimed but unimplemented (see U5)
**Required fix — `run_exp075.py`:** immediately after tokenizer load (L261),
before any forward pass and before S construction (L350), insert:
```python
# Single-token entity guard (F2): the spec/EXP066 procedure assumes
# single-token entities. Abort loudly rather than silently truncating to
# first subtoken. Check the exact strings the code encodes.
_single_tok_entities = (
    [(e, " " + e) for _ents in SUPPORT_VOCABULARIES.values() for e in _ents] +
    [(e, " " + e) for e in novel_vocab_planet + novel_vocab_element]
)
```
(placed after the benchmark entity lists are defined — or hoist the check to
cover both lists; support entities appear in prompts as `" " + ent` since the
template text precedes them with a space, test entities are encoded as
`" " + entity` at L458/L652). For each `(label, s)`: `ids =
tokenizer.encode(s)`; `assert len(ids) == 1`, else `SystemExit` with FATAL
message naming the entity. Log the per-entity id + single-token flag.
**Alternative (weaker, acceptable only if the abort is genuinely infeasible):**
correct `UNTESTED_ASSUMPTIONS.md` A.1 and LOG-096's claim to describe the
actual first-subtoken behavior. The reviewer requires the abort (F2 primary),
not the doc-downgrade.

### F3 [MODERATE] — Three wrong forward-budget figures (see U1)
True total ≈ **1,082** (300 support + 2 B_wrong + 60 baseline + 720 conditions).
**Required fixes (docs only):**
- `RUNBOOK.md` L28: "420 benchmark passes + ~300 support passes" →
  "≈1,080 total forward passes (≈720 condition + 300 support + 60 baseline)".
- `RUNBOOK.md` L60: same correction.
- `UNTESTED_ASSUMPTIONS.md` item 7 (L71–74): state the ≈1,082 true total and
  note the spec's 420 figure omitted the 300 support forwards.
- `run_exp075.py` L217 and L245 (`--allow-cpu` help / FATAL text): "~720
  forward passes" → "≈1,080 forward passes".

### F4 [MODERATE] — B.3's benchmark-provenance caveat is false (see U4)
**Required fix — `UNTESTED_ASSUMPTIONS.md` B.3:** replace with a dated record
of this review's verification: the runner's support and benchmark constructions
were diffed item-by-item against
`experiments/scripts/run_exp066_pythia410m_replication.py` (the historical
EXP066 procedure) and found identical (prompts, entities, indices, templates,
alternation, v_hat/B_agg/B_perp/B_wrong construction, layer indexing;
instance IDs differ only). Retain the honest residual: item-identity holds for
the construction procedure; the historical *results* comparison still rests on
the (d)-rider baselines.

### F5 [MINOR] — Exact p=0.05 boundary untested; LOG-096 falsely claims it is
`sig_positive` correctly implements the spec's strict `p < 0.05`, but no test
pins the boundary, and LOG-096 claims "exact p=0.05 boundary" tests exist.
**Required fix — `test_evaluate_exp075.py`:** add
`expect("boundary: C4 ΔM>0, p=0.05 -> (g), not (e)", base_norm(C4=_cond(0.10,
b=6, c=0, p=0.05)), "i")` and
`expect("boundary: C3 ΔM>0, p=0.05 -> (c) invalid", base_norm(C3=_cond(0.10,
b=6, c=0, p=0.05)), "c")`. Record LOG-096's inaccuracy in the LOG-100 entry
(the log is append-only; do not rewrite LOG-096).

### F6 [MINOR] — `UNTESTED_ASSUMPTIONS.md` D.9 doc drift
L76: "`PYTHIA_SEED=4100002`" — no such symbol exists in the code; the seeds are
`SEED_TORCH=SEED_NUMPY=20260923`, `SEED_B_PERP=9876`. L82: "EXP070-listed value"
— the code compares against the EXP067 §2 registered hash. L85: "per the
review's M2" — the prereg review's M2 concerns H_sub's wording, not hash
diagnostics (the diagnostic lead lives in branch (c)'s ruling). **Fix:** correct
all three references.

### F7 [MINOR] — Whitelist-substitution disclosure missing where claimed
`run_exp075.py`'s docstring says the ordering+signature substitution for the
spec's path whitelist is "documented in UNTESTED_ASSUMPTIONS.md" — it is not.
**Fix:** add the disclosure (per ruling U3) to `UNTESTED_ASSUMPTIONS.md`.

### F8 [MINOR] — Halt reports omit the diagnostics §7.1(a) requires to be reported
`normalize_exp075` (L173) reads `payload.get("energy_gate")`, which is `None`
for halt payloads — but `save_halt` for HALT_ENERGY writes `e_median`,
`e_distribution`, `e_sensitivity`, `energy_bar` at top level, and for HALT_RANK
writes `rank_ratio`/`singular_values`. `report()` therefore prints the (a)
ruling ("the e distribution is evidentially non-empty") without printing any e
value. **Fix:** in `normalize_exp075`, for halt payloads, build the display
dicts from the top-level halt fields so the report surfaces them.

### F9 [MINOR] — Malformed non-halt payload crashes instead of hitting the fail-safe
`normalize_exp075` raises `KeyError` (uncaught) on a non-halt payload missing
`stage_B_conditions`, bypassing `evaluate()`'s `"unclassified"` fail-safe.
Loud is better than silent, but the fail-safe exists for a reason. **Fix:** wrap
the `conds = payload["stage_B_conditions"]` access so a malformed payload
normalizes to `"unclassified"`.

---

## 3. Verified clean (by independent read/grep/diff, not on trust)

- **Precedence lattice:** (a)→(b)→(c)→(d)→(e)→(h)/(i) with (d) superseding
  (e)–(i) — implemented exactly (modulo F1).
- **Branch (e) weakening:** the ruling text is the signed spec's weakened
  LICENSES/DOES-NOT-LICENSE verbatim — per-item existential, label-informed,
  mechanism unidentified, no loop validation, N1 holds, EXP070/EXP068
  contingencies inside the license. The M1/M2 conditions are honored in the
  evaluator, not just the spec.
- **(e)+C5-rescues:** stays (e) with informational note; (h) correctly
  conditional on (f)/(g) only — tested (L70–72).
- **Energy gate:** median ≥ 0.10 with 0.05/0.15 sensitivity logged, archived,
  and evaluated on the full N=60 **before** the headroom gate — precedence
  (a)→(b) honored.
- **Rank guard:** halts on σ_min/σ_max ≤ 1e-6, reported as (a') with the
  §3.1/§7.2 halt text — the spec's unlettered gate handled explicitly.
- **Headroom gate:** [40%, 70%], halts to (b).
- **C3-validity gating:** (c) checked before any C4/C5 interpretation.
- **SHA-256:** binding pre/post match with hard abort on drift; the registered
  value correctly treated as warning-only sanity check.
- **Δθ = 0:** `torch.no_grad()` throughout, `model.eval()`, no optimizer, no
  weight writes — Law #6 holds by construction.
- **Seeds:** 20260923/20260923/9876 with post-B_perp restore; deterministic QR.
- **Law #13 archives:** `exp075_vectors.pt` (Q_S, v_hat stack, per-vocab
  v_hats, B_agg/B_perp/B_wrong, rank diagnostics, per-item pre-norm and
  unit-norm projections, energy ratios, support/test ids, seeds);
  `exp075_results.json`; per-instance records with per-condition correctness
  **and** KL (the T-1 lesson); run log; environment manifest.
- **KL exploratory-only:** recorded per condition, guardrail-flagged, never
  consulted by the evaluator — the O5/Wilcoxon lesson honored.
- **Historical baselines:** 0.6833/0.5667 verified in `research_log.md`
  (L2219: EXP065 68.33%; L2274: EXP066 56.67%, 34/60) — artifact-grounded, and
  the (d) comparability rider is printed by the evaluator (M3 honored).
- **McNemar:** exact two-sided `binomtest(min(b,c), b+c, 0.5)`; p=1.0 on
  b+c=0 — matches program convention.
- **Support/benchmark fidelity:** item-identical to the historical EXP066
  script (see U4) — the strongest provenance claim in any bundle to date.
- **Multiplicity disclosure:** present in the spec; evaluator adds no
  unregistered tests.
- **`requirements.txt`:** lower-bound pins mirroring EXP067 — appropriate for
  free-tier images.

## 4. Required re-verification

After the fixes are applied: a focused Law #14 diff re-verification of
`evaluate_exp075.py` (F1, F8, F9), `test_evaluate_exp075.py` (F1, F5),
`run_exp075.py` (F2, F3), `RUNBOOK.md` (F3), and `UNTESTED_ASSUMPTIONS.md`
(F3, F4, F6, F7) — then, and only then, execution clearance. No GPU run may
precede the sign-off.

---

*Reviewer sign-off: CLEAR-WITH-FIXES — Adversarial Reviewer, 2026-09-23.
Bundle not edited by reviewer. No primary artifacts modified. No results
invented. The single most load-bearing objection is F1: the evaluator as
written makes the pre-registered kill criterion (§7.0, "single source of
truth") unreachable, routing the exact-kill cell into a ruling that denies
the kill — a Law #4 violation that must be repaired before any execution.*

---

## 5. Law #14 Diff Re-verification (LOG-107, 2026-09-23)

**Re-verifier:** Adversarial Diff Re-verifier (Law #14)
**Method:** independent code-level diff check of each finding's fix against the
review's exact requirements; the test suite was run locally
(`python3 test_evaluate_exp075.py`); no GPU/torch needed. Bundle edited only
for the clearance banner. No primary artifacts modified. No results invented.

### VERDICT: **CLEAR FOR EXECUTION**

### Finding-by-finding verification

- **F1 [MAJOR] — PASS.** `evaluate()` L157–162 now returns `"f"` terminal for
  the exact-kill cell (C4 `b=c=0`, C3 valid); the old `("f","g")→(h)/(i)`
  routing is gone. `report()` L304–313 appends (h)/(i) as supplementary
  localization notes for the (f) region (branch unchanged), and the (i) note
  in the (f) region correctly omits the "neither (e) nor (f) fires" clause.
  `RULINGS["f"]`/`BRANCH_NAMES["f"]` are reachable. Docstrings rewritten.
  Tests updated and passing (exact-kill → `"f"`; (f)+C5-rescue → `"f"` with
  report-level supplement assertion).
- **F2 [MAJOR] — PASS.** The guard exists in code at `run_exp075.py` L276–303:
  immediately after tokenizer load, before any forward pass and before S
  construction; checks the exact encoded strings (`" " + e`) for all 35
  support+test entities; multi-token → FATAL `SystemExit` naming the entity.
  Test-entity lists hoisted to module level (`NOVEL_VOCAB_PLANET`,
  `NOVEL_VOCAB_ELEMENT`). The Law #2-adjacent docs falsehood is code-true.
- **F3 [MODERATE] — PASS.** ≈1,080 disclosed consistently: RUNBOOK L29/L62,
  runner `--allow-cpu` help + FATAL text (L227/L255), UNTESTED_ASSUMPTIONS
  item 7 (which records the spec's 420 omitted the 300 support forwards).
- **F4 [MODERATE] — PASS.** B.3 rewritten as a verification record: the
  item-identical diff against `experiments/scripts/run_exp066_pythia410m_replication.py`
  is recorded; the false "no historical script" caveat is gone.
- **F5 [MINOR] — PASS.** Exact p=0.05 boundary tests added and passing
  (C4 p=0.05→(g)→(i); C3 p=0.05→(c) invalid). LOG-096's claim remains
  corrected in LOG-100; the append-only log was not rewritten.
- **F6 [MINOR] — PASS.** D.8/D.9 drift corrected: `SEED_TORCH=SEED_NUMPY=
  20260923`/`SEED_B_PERP=9876`; EXP067 §2 registered hash; branch (c)
  ruling as the diagnostic lead.
- **F7 [MINOR] — PASS.** UNTESTED_ASSUMPTIONS §F item 13 adds the
  ordering+signature whitelist-substitution disclosure the runner's
  docstring claims (per ruling U3).
- **F8 [MINOR] — PASS.** `normalize_exp075` rebuilds energy/rank display
  dicts from top-level halt-payload fields; tests assert the e values and
  rank diagnostics surface in `report()` — both pass.
- **F9 [MINOR] — PASS, with ruling on the flagged uncertainty.** The fixer
  used an intermediate `"MALFORMED_PAYLOAD"` outcome string mapped to
  `"unclassified"` rather than a bare try/except. **Ruling: PASS.**
  The behavior is exactly what the review required — malformed non-halt
  payload → `evaluate()` returns `"unclassified"`, `report()` renders it
  with the schema-error explanation, no crash — i.e. "malformed →
  unclassified, loud-but-structured." The intermediate string is a labeled
  outcome the report renders, not a silent pass-through; the branch letter
  `evaluate()` emits is `"unclassified"` verbatim. Style alone is not a
  fail. Tests: malformed payload → `(unclassified)`; malformed report
  renders without crashing — both pass.

### Uncertainty rulings honored (verified)
- `--allow-cpu` hatch kept with loud warning + self-identifying
  `env_manifest.device` (EXP070 precedent); budget figure in hatch text
  corrected to ~1,080.
- Whitelist→ordering+signature stands as a disclosed deviation (§F item 13).

### Test suite (run by the re-verifier)
`python3 test_evaluate_exp075.py`: **25/25 PASS, 0 FAIL.** (16 updated
pre-existing + 9 new: 2 boundary, 2 (f)-supplement report assertions,
2 halt-diagnostic, 2 malformed-payload, 1 exact-kill terminal.)

### Scope of this clearance
This verdict clears the **bundle's fidelity to the signed protocol and the
review's required fixes only**. It does not re-litigate the protocol's
science (that was the preregistration review, SIGN) or pre-judge any
outcome. The evaluator's kill criterion (§7.0) is now reachable in code.
No GPU run preceded this sign-off. RUNBOOK banner updated to
CLEARED FOR EXECUTION.

*Re-verifier sign-off: CLEAR FOR EXECUTION — Diff Re-verifier (Law #14),
2026-09-23.*
