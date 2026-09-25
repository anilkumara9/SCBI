# EXP087 — Independent Re-Verification of the LOG-341 Repair Wave (2026-09-25)

**Re-verifier:** Independent Scientific Mentor & Adversarial Reviewer —
reports DIRECTLY to the founder. This verdict is binding; the CEO cannot
override, suppress, or recall it.

**Target:** `experiments/runs/EXP087_translation_signature/` after the
LOG-341 repair wave, which applied the binding LOG-340 bundle-review fixes
F1–F3. Every item below was verified by fresh inspection or fresh
execution — nothing was taken on the repair agent's attestation.

## Verdict: SIGN

The repair wave is confirmed complete. The bundle is clear for the CEO's
GPU-clearance decision. GPU execution remains NOT licensed until that
clearance is granted. Queue position on clearance: behind K2 → EXP083 →
EXP084 → EXP086 Stage B → EXP088; no pre-emption.

## Fix-by-fix verification

**F1 (apparatus integrity) — CONFIRMED.** `exp087_guards.py:31` defines
`MODEL_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"` (the LOG-331
pinned snapshot). Both `--execute` `from_pretrained` calls in
`run_exp087.py` (model, line 159; tokenizer, line 162) pass
`revision=G.MODEL_REVISION`. The silent wrong-revision failure mode is
closed.

**F2 (precision) — CONFIRMED.** `run_exp087.py` lines 247–251 inject
`model_id`, `model_revision`, full `state_dict_hash_pre`,
`state_dict_hash_post`, and `delta_theta_zero` into the report dict
written by `write_report`. A revision/pin failure is now detectable
post-hoc.

**F3 (precision) — CONFIRMED.** The false "must be called" claim is gone
from `BUILD_NOTES.md`; the note now documents that
`exp087_rng.require_single_seed(1)` never existed and that enforcement is
de-facto (the single `torch.manual_seed(G.MASTER_SEED)` call in
`run_exp087.py:151` — verified exactly one occurrence in the bundle).
Repo-wide grep finds no code referencing the nonexistent function
(remaining mentions are in this review file, the corrected BUILD_NOTES,
and the research log — documentation of the correction, not calls).

## Independent test reruns (this re-verification, 2026-09-25)

- `test_exp087.py`: **59/59 pass** (re-verifier's execution)
- `smoke_test.py`: **8/8 pass** (re-verifier's execution; includes
  `--execute` refusal without flags)
- `mock_harness.py`: **8/8 scenarios pass** — S1 KILL; S2–S5 CONTINUE by
  the correct row; S6 R5 RUN-INVALID; S7 JoinError→RUN-INVALID;
  S8 archived reproduction r_pinned=0.49708, p=2.67e-05,
  r_sorted=−0.21388, μ̂_arch=0.74921 in envelope (re-verifier's execution)

## Signed-protocol integrity

`experiments/protocols/EXP087_TRANSLATION_SIGNATURE_PREREG_SIGNED.md`
SHA-256 recomputed this re-verification:
`32c27415b20fa0d07adb4fffb61127859c5e726fbfecff642a89e91fc1358d23` —
byte-identical to the LOG-330/erratum record and the LOG-340 review record.

## Binding record

A1 (GROSS_CORRUPTION_BAR=4), A2 (join failure → RUN-INVALID), A3
(headroom [0.40, 0.70] + violation → RUN-INVALID) were recorded binding
in BUILD_NOTES.md at LOG-341; the re-verifier takes no exception to
their transcription. No endpoint, verdict, cost, or mapping was altered —
no new experiment number is triggered. $0 CPU; no weights touched.
