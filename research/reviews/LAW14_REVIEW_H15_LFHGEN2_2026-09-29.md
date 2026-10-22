# Law #14 Review — H15 pre-registration (LFH-GEN2)

**Lane:** LOG-4632 (pre-assigned, independent). $0 CPU. No model runs, no signed
artifact modified, no GPU contact, no commits, no pushes.
**Target:** `research/prereg/EXP_PREREG_H15_LFHGEN2_2026-09-29.md` (23 KB, §§0–10
+ boundary, drafted LOG-4631).
**Ground sources verified against:**
`research/strategy/H15_GATE_2026-09-29.md` (binding gate memo, LOG-4630),
`research/strategy/INNOVATION_SPRINT_2026-09-29_H1315.md` (H15 brief),
`research/prereg/EXP_PREREG_H5_LFHTD_2026-09-29.md` (H5 signed — pinned protocol
transcription check), `experiments/runs/EXP107_templatectrl/build_exp107_bench.py`
(bench-1 construction facts: verb families, QUESTION_SUFFIX, ID namespace, flip
discipline, docstring wording), LOG-331 backbone pin (cross-artifact).

## Verdict: SIGN

The draft is launch-eligible. Zero fixes required. The 20-discrepancy-class sweep
found no binding defect. Findings class by class:

### 1. Completeness (no truncation placeholders; §§0–10 present)
PASS. §§0, 1, 1.1, 2, 3, 3.1–3.8, 4, 5, 6, 7, 8, 9, 10 all present; no
`[...]`/`TODO`/`TBD` truncation markers anywhere in the 23 KB file.

### 2. Construction gates (§3.1/§3.2) — operational, self-arbitrating
PASS.
- **G-C1 (pure-template detector ≤ 36/60):** the α=0.05 one-sided justification
  is stated as P(X ≥ 37 | 60, 0.5) ≈ 0.047. Independently recomputed: 0.0462.
  "≈0.047" is fair; the bar (≤36/60) is the correct consequence — 37/60 is
  above chance, so the bar correctly fails a template-decodable bench.
- **G-C2 (|Pearson(r1,r2)| ≤ 0.10):** quantitative, with the Law-#13 fence
  explicit — the correlation compares bench-2's construction against bench-1's
  *builder records* as a design check only; it feeds no bench-1 labels or
  embeddings into the analysis (§8 item 5 repeats the fence). The fence is real,
  not decorative.
- **G-C3 (independent decomposition pin):** defined as the EXP107 equivalent
  of QUESTION_SUFFIX byte-exact + canonical-order construction — independently
  auditable from the builder code.
- **Design-time assertions** (cells, families, extraction contract, ID
  namespace, label check) are each mechanically checkable; bench-1 IDs are
  asserted to start with `exp107_` (builder line 172 — verified), so the
  "assert no id starts with 'exp107_'" disjointness gate is well-formed.

### 3. Binding bars — internally consistent, consistent with the gate memo
PASS. ≥20/30 & G<0.30 → CONTINUE; ≤18/30 or G≥0.30 → H15-KILL of the
*generality hypothesis only*; 19/30 & G<0.30 → HELD, no rescue; cross-bench
effect-size comparisons unlicensed (§2, §6, §9 item 7); Law-#8/#11 two-layer
tagging (bench-1 observation stands, reclassified as bench-specific, never
erased). All bar values independently recomputed:
P(X≥20|30,0.5)=0.0494 ✓, P(X≥19)=0.1002 ✓, P(X≥18)=0.1808 ✓.
The G≥0.30 bar with N_F=N_T=15 denominators corresponds to a ≥5-item gap
(5/15=0.333) — matches the gate memo's "(≥5-item gap)" gloss.
Pre-installed kill-test sentence present (§4, final paragraph).

### 4. Breaking-point text (§0)
PASS. "Bench construction is the breaking point" licenses no
contaminated-bench run: any gate failure → lane dies at construction, no head
trained, no metric read, no experiment number consumed beyond what the CEO
assigns; construction failure logged as construction-fate RUN-INVALID. The
falsification tree (§5) mirrors this at its first branch. No escape hatch
anywhere in the file.

### 5. Record-keeping gate (§3.7) and FIX-1 label-pin discipline (§3.4)
PASS. The EXP119 lesson is pinned as an artifact-existence gate: builder
script, canonical JSON, per-item records, embedding npz, train/test ID lists,
head parameters all hash-pinned *before any verdict is written*; missing
artifact → RUN-INVALID. The FIX-1 discipline is correctly applied
*prospectively*: since bench 2's builder does not yet exist, the draft pins
the procedure (builder's construction docstring + independent per-item
assertion, never a truncated inline comment) rather than citing a document
that does not exist — the only honest form this gate can take in a
pre-registration.

### 6. Laws #4/#7/#9/#13; no scope creep
PASS.
- **Law #4:** bars binding, "No re-runs, no re-seeds, no post-hoc bars" (§5),
  no-tuning/no-layer-choice/no-seed-re-rolls pinned (§3.5).
- **Law #7:** no test-informed model selection; bench-2 labels used only as
  pre-registered head targets + final registered evaluation; extended to every
  model-selection decision (§3.5 — the EXP106 lesson).
- **Law #9:** metrics registered before output inspection; falsification tree
  has no unregistered branches.
- **Law #13:** independent apparatus fence (§8 item 5, §3.5 block-off
  discipline, determinism re-fit pass byte-identical, seeds/environment
  pinned, backbone hash before AND after extraction vs LOG-331 pin
  `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` —
  cross-checked against the pin recorded across protocol artifacts).
- **Scope creep:** the per-layer secondary is barred (§6) — H15 runs one
  protocol at one read site (layer 20). The H5 §6 descriptive per-layer
  analysis is not re-licensed on bench 2.

### 7. Deviation from the gate memo
PASS. The 7-item deviations list (§9) is complete: (1) bench-construction
phase prepended, (2) fresh extraction instead of archived embeddings, (3)
record-keeping artifact-existence gate, (4) FIX-1 label-pin discipline,
(5) no secondary per-layer analysis, (6) H15-KILL semantics with Law-#8/#11
tagging, (7) cross-bench effect-size comparisons unlicensed. Each is an
explicitly declared design decision; no silent divergence from the gate
memo's six items.

### 8. Pinned-protocol transcription (H5 → H15, verbatim)
PASS. Split: `train_test_split` sklearn==1.9.1, numpy==2.5.3, test_size=0.5,
seed 20260929, 4-cell key `f"{phrasing}_{flipped}"`, 8/7/7/8 → train n=30,
test n=30, N_F=15 flipped=False, N_T=15 flipped=True — matches H5 §3.3 line
for line (including the "8/8/7/7 in sorted key order" wording, carried
verbatim — a transcription oddity inherited from the signed source, not a new
discrepancy; the explicit per-cell mapping 8/7/7/8 is self-consistent and
N_F/N_T-consistent, so the protocol is unambiguous). Head:
`LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000,
random_state=20260929)` — verbatim. No drift in C, solver, seed, or split.

### 9. Bench-builder facts cited correctly
PASS. Verb families `" outranks "` / `" is lower than "` (builder lines 14–21);
entity sets {Mars, Venus, Jupiter, Saturn, Mercury} ∪ {Iron, Gold, Silver,
Bronze, Steel} (lines 44–45); QUESTION_SUFFIX
`" Question: Who is higher in rank? Answer:"` byte-exact (line 53); flip
discipline "even sorted positions → 15 flipped + 15 original per phrasing"
(lines 25–27); the builder's meaning-preserving docstring wording
("ranking meaning (A > B > C [> D]) ... preserved", lines 11–12) is fairly
abridged, not truncated into a license — the FIX-1 class error does not
recur.

### 10. Honesty fences
PASS. §7 ledger: n=30 power caveat; bench-2 labels encode the
subject-position cue, so a CONTINUE means the head extracts *position* on a
second bench — narrow, disclosed; no generality beyond the two benches, the
layer, or the model (§8 item 1); §8 item 2 requires downstream causal tests
before any capability statement; N1 Known Combination (§8 item 6).

## Fixes
None. Zero truncation placeholders, zero section drift, zero arithmetic
errors, zero fence leakage, zero protocol drift.

## Sign
**SIGN.** The H15 pre-registration is launch-eligible as drafted. The CEO may
mint an experiment number and launch execution on the next lane.
