# Independent Law #14 Review — EXP107 template-control pre-registration

**Lane:** LOG-4536 (independent review; pre-assigned)
**Date:** 2026-09-29
**Document under exact-version review:** `research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md`
**Independence [FACT]:** this lane did not write the draft. The draft was produced by the LOG-4535 design lane; this review was conducted independently, with no shared authorship and no edits to the draft.
**Cost:** $0 CPU. Read-only everywhere except this review file and the LOG-4536 log append. No execution licensed, no push, no weights touched, no GPU contact.

**Review method [FACT]:** adversarial re-verification, not re-reading. This lane independently:
1. Executed `experiments/runs/EXP107_templatectrl/build_exp107_bench.py` and checked the registered bench pin, cell balance, and all design-time assertions from scratch.
2. Ran an independent residual-cue sweep over the built bench (word family × phrasing, grammatical role × phrasing, target sentence position, first-entity distribution, closed vocabulary).
3. Recomputed the binomial bars from first principles.
4. Verified the train-embeddings and id-array SHA-256 pins against `experiments/runs/EXP106_lfh/out/exp106_train_embeddings.npz` directly.
5. Compared the builder's `_base_items()` constants and templates against the EXP106 executor's `build_test_premises()` in `experiments/runs/EXP106_lfh/run_exp106.py`.
6. Checked the backbone hash pin against the EXP106 report's verified pin.

---

## Findings per review test

### Test 1 — Does the decorrelation design break template↔label determinism? [PASS]

**[OBSERVATION]** Independent execution confirms: word family × phrasing = exactly 15/15/15/15 across the four cells. Vocabulary is closed (only "outranks" / "is lower than" appear). A pure word-family detector ("outranks"→A-first) scores exactly 30/60 on the built bench: original cells 30/30, flipped cells 0/30 — matching the draft's registered rival prediction.

**[OBSERVATION]** Residual-cue sweep (this lane's own computation): grammatical role × phrasing is also exactly 15/15/15/15 (the flip moves the target subject↔object, but originals within each phrasing carry the opposite role — role is decorrelated too). Target-in-first-sentence ⟺ A-first holds 60/60 (the intended position signal, preserved by construction). Entity identity was already ruled out as the head's driver by EXP106's 31-item adversarial analysis; the bench reuses EXP091's entities, so no new entity confound is introduced. Premise length and first-entity do not determine the label. The decorrelated bench differs from the original EXP091 bench in exactly one manipulated variable — premise phrasing. Clean single-variable manipulation.

### Test 2 — Is the subject/object caveat honestly handled? [PASS]

**[OBSERVATION]** The draft registers the limitation twice (§3.6 and §7): a collapsed score kills the transfer reading under *either* a word-template or a subject-position cue, and the test does not identify which surface cue the head used.

**[INTERPRETATION]** The caveat is mathematically correct, not merely honest: this lane verified that both a pure word-family detector and a pure subject-role detector predict exactly 30/60 on this bench, so a collapsed score genuinely cannot discriminate between them. No claim in the draft overreaches it — the hypothesis's "target-position readout" refers to sentence position (first vs last), which the flip preserves and which is the only perfectly label-correlated feature remaining. The CONTINUE reading is licensed; the KILL reading is correctly scoped to "the EXP106 transfer reading," not to any claim about which artifact cue was used.

### Test 3 — Pipeline-continuity sanity gate: correctly specified, not gameable? [PASS with FIX-2]

**[OBSERVATION]** The gate (retrained head must reproduce 60/60 on the original EXP091 bench rebuilt verbatim from the EXP106 executor's `build_test_premises`, else RUN-INVALID, pre-primary) is correctly specified. This lane confirmed the builder's base items use byte-identical constants, templates, thresholds, and id scheme as the EXP106 executor. The gate's failure direction is safe: it can only block (RUN-INVALID) a drifted pipeline, never manufacture a CONTINUE — the retrain is deterministic given pinned embeddings, pinned hashes, and a pinned head spec, leaving no tuning freedom to game.

**[INTERPRETATION]** The one residual freedom is the software environment: the draft pins the head spec ("EXP106 spec verbatim") but not the sklearn version (EXP106 used sklearn 1.9.1 in `~/.venv-exp077`). A cross-version lbfgs retrain is near-certain to agree on this separable 60-point problem, but the failure mode would be a spurious RUN-INVALID. FIX-2 below pins the environment.

### Test 4 — Decision bars: decisive, rival predictions sound? [PASS with FIX-1]

**[OBSERVATION]** Recomputed from first principles: P(X≥40 | n=60, p=0.5) = 0.00674 — the draft's "p ≈ 0.0067" is exact. The pure-artifact point prediction (30/60) was verified by simulation on the built bench. The bars (≥40 CONTINUE / ≤35 KILL / 36–39 HELD) split the 30-point gap between rival predictions with a 4-point indeterminate zone; the KILL bar absorbs ±5 of noise around the artifact point prediction. The HELD zone correctly licenses nothing and bars unlicensed larger-n re-tests (no gate tweak).

**[INTERPRETATION]** The bars are decisive and honestly framed. One precision softening is warranted (FIX-1): "exactly 30/60" idealizes a perfect transfer of the cue detector to flipped premises; embedding shift could move the realized artifact score by a few points, which the ≤35 bar already absorbs.

### Test 5 — Frozen-setup pins carried over? [PASS]

**[OBSERVATION]** All pins verified independently: backbone hash `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` matches the EXP106 report's verified pin; layer 20 / final token / float32 / CPU extraction spec matches EXP106's disassembly-verified spec; head `LogisticRegression(penalty='l2', C=1.0)` matches; train-embeddings SHA-256 `4e6229bea083570f17e3368326d9848c9a8db5dc25c7efc75f0e1a2960b5683c` and id-array SHA-256 `4668fc45716d46b408c778c93d2d844ad9b2c5bafb33458ec30a4b673ed44474` both recomputed from the npz file and match the draft; bench pin `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5` reproduced by running the builder; overlap tripwire (`exp092_*` vs `exp107_*`, 0 by construction) and byte-identical block-off discipline carried over verbatim.

### Test 6 — Overclaim guards on the EXP106 GPU proposal license? [PASS]

**[OBSERVATION]** §7 is thorough and correctly scoped: CONTINUE → the EXP106-licensed GPU *proposal* stands with template-control evidence, still founder-gated, proposal-only, must itself be template-controlled; KILL → the proposal license is VOID and any new proposal must re-license against a template-decorrelated design; neither verdict licenses GPU execution; the draft explicitly does not re-litigate EXP106's binding CONTINUE ("this experiment tests the *reading* of that verdict"). Novelty stays N1. No overreach found.

### Test 7 — Assertions vs cited sources [PASS]

**[OBSERVATION]** Every quantitative assertion checked held: the binomial p-value, the 31/60 template-following items (EXP106 §11), the 60/60 EXP106 score, the bench pin, both reuse-integrity hashes, the backbone pin. No assertion was found that its cited source does not support. The §2 "mathematical license" parenthetical (linear head extracts only what is in the embedding) is slightly loose as stated, but the design's actual guarantee rests on the bench construction, which this lane verified independently — noted as an observation, not a defect.

---

## Verdict

**SIGN-WITH-FIXES** for `research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md`.

The design is sound: the decorrelation instrument works as registered (independently verified by execution), the caveat is honest and mathematically correct, the bars are decisive, all pins carry over, and the overclaim guards are properly scoped. Two minor, verifiable fixes are required before CEO launch; neither changes any decision, bar, or interpretation.

**FIX-1 (precision):** In §2 (worth-it gate, quantitative prediction) and §3.6 (registered rival predictions), change "exactly 30/60" to "≈30/60" and append "(point prediction; ±5 of embedding-shift noise absorbed by the ≤35/60 KILL bar)". *Verification:* `grep -c "exactly 30/60" research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md` returns 0 after the fix.

**FIX-2 (reproducibility, Law #13):** In §3.2 (head spec), append the environment pin for the retrain: "Retrain executes in the EXP106 environment (sklearn 1.9.1, `~/.venv-exp077`, torch 2.14.0+cpu) so the sanity gate tests pipeline determinism, not cross-version optimizer drift." *Verification:* the string "1.9.1" appears in §3.2 after the fix.

**Boundary:** this lane reviews only. It does not fix the draft, does not approve execution, does not mint EXP107, and dispatches no follow-ups. Fixes are the design lane's or CEO's act; a fixes-verified check is a separate lane.

**Next free: LOG-4537.**
