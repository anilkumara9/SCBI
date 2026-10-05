## LOG-4922 — EXP145 verdict: KILL/PIVOT — S7-2b cross-family Decodability Gap replication (GPT-2-small, Triton→Neptune bench) (2026-10-05)

**Decode [OBSERVATION]:** D1 PASS (best layer 8 acc=0.2833, p=0.000999, effect=+0.1333; passing layers [8, 10]); D2 mean shared-direction cosine -0.4587 (bar 0.70) → FAIL.

**Verdict [INTERPRETATION]:** KILL/PIVOT (cell: decode− / steer− (intervention arm not licensed)). the generality claim is killed/bounded with the recorded caveat: the gap's precondition (decodability) is absent here; this outcome cannot separate an architecture effect from scale/bench-fit (the §1 steelman). The dissociation itself is untested in this family.

**Integrity [FACT]:** model revision `607a30d783dfa663…` (S0.2 resolved programmatically, character-identical to plan pin); bench pin `b9eac3893ddfbc67…` (pinned S7-2b JSON load, S0.1 pin assert + S0.1a procedural cross-check, G0/G2/G3 PASS, G1′ 240/240 under GPT-2 BPE before weight access); Δθ=0 pre/post state-dict hash in both phases; $0 CPU.

**Artifacts [FACT]:** `research/analysis_plans/EXP145_VERDICT_2026-10-05.md`, `research/analysis_plans/EXP145_RESULTS_2026-10-05.json`, run records `experiments/runs/EXP145/` (manifest, extraction + decision records JSONL, decode/direction/direction-verification JSON, logs).

**Next free: LOG-4923.
