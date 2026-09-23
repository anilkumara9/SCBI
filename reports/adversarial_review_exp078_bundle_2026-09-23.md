# Law #14 Adversarial Review — EXP078 Execution Bundle

**Date:** 2026-09-23
**Reviewer role:** Adversarial Reviewer (Law #14)
**Target:** `experiments/runs/exp078/` (runner, evaluator, tests, RUNBOOK, UNTESTED_ASSUMPTIONS, requirements)
**Reference spec:** `experiments/protocols/EXP078_SUBSPACE_BRIDGE_REREG_PREREG_SPEC.md` (SIGNED, LOG-113)
**Predecessor bundle:** `experiments/runs/exp075/` (CLEARED, LOG-107; build record LOG-114)
**Verdict: CLEAR FOR EXECUTION** — 0 MAJOR, 0 MODERATE, 2 MINOR (both non-blocking, documented below)

---

## 1. Entity substitution fidelity (§3.1) — PASS

The bundle's `SUPPORT_VOCABULARIES` matches the spec §3.1 substitution table exactly:

| Vocab | Bundle contents | Spec table |
|---|---|---|
| V1_Anglo | Alice, Bob, Charlie, David, Emma | unchanged ✓ |
| V2_Biblical | Aaron, **Joel**, Gideon, **Ruth**, **Abel** | Caleb→Joel, Miriam→Ruth, Reuben→Abel ✓ |
| V3_Greek | **Ajax**, Jason, **Apollo**, Paris, **Atlas** | Hector→Ajax, Nestor→Apollo, Priam→Atlas ✓ |
| V4_Roman | Marcus, **Julius**, **Augustus**, Felix, **Diana** | Lucius→Julius, Titus→Augustus, Silas→Diana ✓ |
| V5_Modern | Liam, Noah, **Eli**, Maya, **Finn** | Sora→Eli, Leila→Finn ✓ |

Independent grep verification (not on the builder's word): zero occurrences of any of
the 11 replaced names (`Caleb|Miriam|Reuben|Hector|Nestor|Priam|Lucius|Titus|Silas|Sora|Leila`)
anywhere in the bundle (`.py` + `.md`); each of the 11 substitutes occurs exactly once
(in the vocab lists — no collisions, no duplicates). The benchmark novel vocabs
(planets/elements) are untouched, as the spec requires.

**F2 guard armed:** the single-token guard runs immediately after tokenizer load, before
any forward pass or support construction, checking the exact encoded strings
(`" " + e`) for all 25 support + 10 test entities, FATAL-aborting on any multi-token
entity. This is the failure mode that created EXP078; the guard that caught it is
present verbatim and still armed.

## 2. Bundle-vs-EXP075 diff classification — PASS

`diff experiments/runs/exp075/run_exp075.py experiments/runs/exp078/run_exp078.py`:
76 changed lines, exhaustively classified:

1. **Entity substitutions** (4 vocab-list lines) — the sole registered design delta.
2. **EXP075→EXP078 renames** (banners, docstrings, argparse description, output
   directory `EXP078_subspace_bridge`, artifact filenames, log strings, RUNBOOK/spec
   path references, `"experiment": "EXP078"` payload tags) — mechanical, complete,
   no stale references (grep for `exp075|EXP075` in RUNBOOK/UNTESTED_ASSUMPTIONS: empty).
3. **The LOG-114 mechanical fix** (1 hunk + comment): `model.embed_out.weight` →
   `model.get_output_embeddings().weight` in `make_bridge_vec`.

No mechanism, threshold, gate, seed, condition, endpoint, or decision-tree logic
drifted. The evaluator diff vs `evaluate_exp075.py` contains **zero non-rename
changes** (fully entity-agnostic); the test-file diff is renames only.

**Fix verification (version-agnostic, scientifically neutral):** in the installed
transformers 5.17.0, `GPTNeoXForCausalLM.get_output_embeddings()` returns
`self.lm_head`; in the 4.x line (requirements pin `transformers>=4.44`) it returned
`self.embed_out`. The 5.0 rename was nominal — same `nn.Linear(hidden_size,
vocab_size, bias=False)` weight matrix, same values. The accessor exists across the
entire pinned range. The fix changes which attribute name is read, not which numbers
are read. Scientifically neutral. (MINOR M2 below notes the spec's stale notation.)

**Independent validation run by reviewer:** `py_compile` clean on all three scripts;
`test_evaluate_exp078.py`: **25/25 PASS** (matches the builder's claim; includes the
HALT_ENERGY/HALT_RANK/halt-diagnostic-surfacing and malformed-payload tests).
Kaggle zip (`~/workspace/your_files/kaggle/exp078_bundle.zip`, sha256
`e6f80332…d92abd8dc0`, 7 files) unpacks byte-identical to the canonical bundle
(runner and evaluator hashes match LOG-114 exactly).

## 3. LOAD-BEARING: the energy-gate halt — DESIGN-INHERENT, not mechanical

The builder's CPU smoke halted at branch (a) `HALT_ENERGY` (builder-reported:
e_median=0.0544 < 0.10 bar; sensitivity 0.05 PASS / 0.10 FAIL / 0.15 FAIL), and a
counterfactual with the original 11 multi-token entities (F2 disabled) also halted
(0.0513). I traced the energy computation by hand, tensor by tensor, against spec §3.4:

- **Spec:** `e := ‖P_S bridge(x)‖ / ‖bridge(x)‖`, median over N=60.
- **Code:** `b_vec = normalize(E[t] − E[f])` with `E = model.get_output_embeddings().weight`
  (the unembedding matrix — §3.2's object; the `embed_out` spelling in the spec is a
  stale implementation hint, see M2). Unit norm asserted (`|‖b‖−1| < 1e-5`).
  `proj_S = Q_S @ Q_S.T`; `pS_pre = proj_S @ b_vec`; `e_i = ‖pS_pre‖ / ‖b_vec‖`.
  **Exact match to the spec formula.**
- **Q_S validity:** `build_subspace_S` stacks the five normalized `v̂_k` into
  `V [1024,5]`, applies the SVD rank guard (`σ_min/σ_max > 1e-6`, else HALT_RANK —
  passed in smoke), then deterministic thin-QR → `Q_S [1024,5]` with orthonormal
  columns. `Q_S Q_S^T` is therefore the true orthogonal projector onto
  `S = span{v̂_1..v̂_5}`. No defect.
- **Layer indexing:** support deltas and the intervention hook both use
  `hidden_states[TARGET_LAYER+1]` with `TARGET_LAYER=20` (output of 0-indexed layer
  20), hook registered on `model.gpt_neox.layers[20]` — internally consistent, and
  identical to the EXP066 procedure the spec registers ("constructed exactly per the
  EXP066 support procedure"; the EXP075 bundle's item-identity to that procedure was
  established in LOG-100 F4 and the diff confirms no change here).
- **No normalization or dtype defect:** model pinned float32 (LOG-109), all
  projections float32, `e_i` a ratio of norms (scale-free). F1 zero-norm hygiene
  asserts are present and did not fire.

**Chance-level analysis (reviewer's own):** for a uniform random unit vector
`u ∈ R^1024`, `E[‖P_S u‖²] = 5/1024`, so `E[‖P_S u‖] ≈ 0.066` (the spec's "≈0.07"
anchor overstates slightly by Jensen, but the bar is tagged [ARBITRARY] and
sensitivity bands are reported — no finding). The observed 0.054 sits **at/below
chance**: a random 5-dimensional subspace would capture as much of the bridge as
`S` does. Combined with the counterfactual (0.0513 with the original entities —
entity-independent), the halt is **design-inherent**: the entity-contrast subspace
(relational "outranks vs next-to" directions in residual stream) is essentially
orthogonal to the unembedding-space target-minus-foil directions. Renormalizing a
~5% residue to unit norm and injecting at α=0.50 would be, in the spec's own words,
a "renormalized-noise injection" — exactly what branch (a) exists to refuse.

**Sensitivity note (disclosed, not a finding):** at the 0.05 sensitivity bar the gate
would PASS (0.0544 ≥ 0.05). The registered bar is 0.10 and the ruling follows the
registered bar; moreover the scientific reading is bar-robust — at/below chance
capture, `S` carries no preferential share of the bridge under any bar. The bundle
reports the sensitivity bands as the spec requires.

**Ruling: DESIGN-INHERENT.** No mechanical error found in the energy computation.
The substitution is exonerated (counterfactual halts identically).

### What branch (a) licenses / does not license on GPU confirmation

Per spec §7.1(a), a GPU `HALT_ENERGY` rules: **HALT — uninformative causal test,
informative localization measurement.** LICENSES: "the bridge's causal power lies
almost entirely outside `S`" (the low-`e` distribution is evidentially non-empty and
must be reported); re-design required, never a re-run under EXP078. DOES NOT
LICENSE: any verdict on H_sub (neither support nor falsification — C4's test was
uninformative, not failed); the §7.1(f) "empty room" kill of the EXP068 loop's
search space (that license belongs to branch (f), which requires C4 `b=c=0` with C3
valid — unreachable from (a)); "no subspace works" (only this `S` tested).

## 4. Evaluator branch-(a) fidelity and halt-payload validity — PASS

- `evaluate()` checks `outcome` first: `HALT_RANK`→(a′), `HALT_ENERGY`→(a),
  `HALT_HEADROOM`→(b) — precedence (a)→(b) respected; the energy gate fires before
  the headroom gate in the runner, matching the spec's (a)→(b) order.
- `save_halt("HALT_ENERGY", …)` writes `exp078_results.json` with `outcome`,
  `halt_reason`, pre/post SHA-256 hashes, `e_median`/`e_distribution`/
  `e_sensitivity`/`energy_bar`, `rank_ratio`/`singular_values`, and the env
  manifest. `normalize_exp078` rebuilds the display dicts from these top-level
  fields (F8 fix inherited); `report()` prints e_median, bar, pass/fail, and the
  sensitivity bands — everything §7.1(a) requires reported. Covered by passing
  tests, re-run independently by this reviewer.
- The (a) ruling text matches spec §7.1(a) verbatim in substance.
- **GPU-run validity:** a Kaggle run halting at (a) yields a complete, official,
  pre-registered ruling artifact. The halt fires after ≈302 forwards (300 support +
  2 B_wrong) — i.e. **before** the 720 condition forwards — so GPU confirmation is
  cheap (≈10 min on T4 against ~26.8 h remaining quota) and worth doing to make the
  ruling official rather than resting on a CPU smoke.

## 5. Standard bundle checks — PASS

- **Seeds:** `torch 20260923`, `numpy 20260923`, `B_perp 9876` — identical to EXP075
  per spec §8. Thin-QR deterministic; `torch.use_deterministic_algorithms(True)` set.
- **Budget:** 300 support + 2 B_wrong + 60 baseline + 720 conditions (6 intervened
  conditions × 60 items × 2 forwards) = **1,082 ≈ 1,080** — matches the corrected
  §8 disclosure (LOG-100 F3). Quota-safe.
- **Anti-cheat / no-peeking:** `build_subspace_S` receives only support deltas
  (signature-enforced; benchmark does not exist at call time); support entities are
  person names, test entities planets/elements — structural separation. The bridge's
  use of each test item's own target/foil is the disclosed label-informed design
  ("the treasure was found with a map", §1.1), not leakage.
- **SHA-256 binding guard:** `get_hash` over sorted `state_dict()` keys as float32
  bytes, pre and post; the completed path asserts equality (Δθ=0); halt paths record
  both hashes for audit. Registered value `4c242d9a…5ed48dd` carried as sanity check
  only, per EXP067 §2 E-4.
- **KL exploratory-only:** `kl_guardrail_exceeded` recorded per condition, never
  gating. **Wilcoxon/margins:** computed and archived, never consulted by
  `evaluate()` (audit Finding 3 / O5 respected).
- **No invented results:** the bundle contains no results; the spec's "no results
  exist under this protocol" holds.

## Findings

**MINOR M1 — (g) branch unreachable in the evaluator (inherited, do not fix now).**
Spec §7.1 lists branch (g) "Mixed — neither support nor kill" with its own ruling,
but `evaluate()` can never return `"g"`: the non-(e)/non-(f) region with a quiet C5
falls through to `"i"`, whose ruling text asserts "C4 and C5 both null" — literally
inaccurate when C4 was partial (e.g. ΔM<0 with b,c>0). This collapse is the F1
conservative reading inherited verbatim from the cleared EXP075 bundle (LOG-105/
LOG-107), documented in the runner docstring, and the exact `(b,c,p,ΔM)` are still
printed in the report — so no decision-relevant information is lost. Changing it now
would itself be unlisted drift. Recommendation: a future evaluator revision should
make (g) reachable with its spec text; not blocking for execution (the predicted
outcome is branch (a), where this is moot).

**MINOR M2 — spec §3.2 notation stale (suggest touch-up, not blocking).** The spec
writes `E = model.embed_out.weight`; that attribute does not exist in transformers
5.x. The bundle's `model.get_output_embeddings().weight` returns the identical
matrix on both the 4.x and 5.x lines (verified in the installed 5.17.0:
`get_output_embeddings() → self.lm_head`, the nominal rename of `embed_out`).
Suggest a future spec touch-up to "E = the model's output-embedding matrix";
the code is strictly more correct than the notation. Not blocking.

## Recommendation to the parent

**CLEAR FOR EXECUTION.** Run the Kaggle GPU execution: the predicted branch-(a)
halt will produce the official pre-registered ruling at low quota cost, closing
EXP078 properly. On confirmation, the program's honest reading is that the
subspace-restricted bridge hypothesis dies at the energy gate for this
configuration — the EXP068 loop's search-within-S motivation is not supported by
this operationalization, and re-design (not re-run) is the licensed next step.
