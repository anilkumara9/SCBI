# Law #14 Fix-Verification — EXP135 B2/EVAL Pre-registration Repairs

**Artifact:** `research/prereg/EXP135_PREREG_EVAL_2026-09-30.md` (repaired draft)
**Against:** `research/reviews/LAW14_REVIEW_EXP135_EVAL_PREREG_2026-09-30.md` (LOG-4840 review, fixes F1–F6, advisories A1–A2)
**Repair record:** LOG-4841
**Verifier:** independent fix-verification lane (LOG-4842 pre-assigned, CEO). No prior involvement in drafting or repair.
**Verdict:** **PASS-WITH-AMENDMENT** — all 8 required items correctly applied; one pre-existing ambiguity (§3.7(e) denominator) needs a one-line clarification before launch.
**Date:** 2026-09-30

---

## Per-fix verification

### F1 — Tie-break bias → PASS
- §3.5 now reads: "ties in score are broken by a pre-registered random permutation drawn from the dedicated `np.random.default_rng(135033)` stream (F1 fix)." The deterministic lowest-index-wins rule is gone from the ranking statistic.
- The spec's tie-break is correctly scoped: "the spec's tie-break (LOOP_SPEC_DRAFT §2.3 — higher C_cons, then lower candidate index) governs the loop's *selection* step; the ranking test pre-registers its own tie-break for the ranking statistic."
- Seed 135033 appears in exactly two places (the §3.1 seed table and the §3.5 specification) — both correct uses, distinct from all other seeds (135031, 135008, 20260930).
- The uniform-null exactness claim is stated and correct: under H0 with the seeded-random tie-break, k_i is uniform on {1..9} regardless of degeneracy, so E[ρ\*_i] = (5−5)/4 = 0. A blind-tap total failure now reads as ρ̄\* ≈ 0 (plus the (e) guard trips), not ρ̄\* = 1.0. The statistical defect is closed.

### F2 — Exclusions parameterized → PASS
- "n = 60 − e parameterizes the §3.5 endpoint/null and the §3.7(f) budget (F2 fix)" — stated in §3.1.
- Endpoint: "ρ̄\* = (1/n)Σ_{included i}ρ\*_i, n = 60 − e." No residual (1/60).
- Null: "B = 200,000 draws of n uniforms per replicate." No residual 60-uniform draws.
- Budget: "9·n·5 + 5·n + 750 + N_g = 50n + 750 + N_g ± 0 (3,751 at n = 60, N_g = 1)." No hardcoded "3,750". The "3,751 at n = 60" is a descriptive worked example, not a protocol assumption.
- Remaining "60" references are legitimate: the 60-item bench description, `len(bench) == 60` pin, and the LOG-213 historical "(a) 0/60" fact.

### F3 — (g) control specified → PASS
- N_g = 1: "N_g = 1 forward, counted in the (f) budget (F3 fix)."
- Probe norm: ‖δ_probe‖ = 16.0 (float32, run device) — pinned, EXP133 (h) precedent.
- Position: "after the base pass and **before the first intervention forward**, on the first included bench item's first-view input_ids." The tap_base comes from the already-completed unintervened cache ("no extra forward") — ordering is consistent.
- Site: layer 20 (this protocol's injection site), answer position, `prepend=True`, r ∈ [0.99, 1.01], miss → exit 44.
- Budget: (f) includes "+ N_g (the (g) control)". The (g)-trips-(f) self-contradiction is closed.

### F4 — Seed hygiene → PASS
- Full seed-stream table in §3.1. Mechanism: `np.random.default_rng(SEED)` per stream — exactly one of the review's two suggested options, checkable by the executor.
- All new-style Generator seeds distinct: 135008 (C2–C9 randoms), 135033 (tie-break), 135031 (permutation null), 20260930 ((g) probe).
- The 135031 triple-use (torch.manual_seed / legacy np.random.seed / new-style default_rng) is provably safe: three independent RNG subsystems (torch global, numpy legacy RandomState, numpy new-style Generator) — seeding them with the same integer creates no correlation. The draft explicitly documents the permutation null's Generator as "independent of the legacy `np.random.seed(135031)` state." Slightly confusing on first read, but technically sound and explicitly documented. Not a defect.
- The (g) seed collision is fixed: 20260930, with the draft honestly noting the original "seed 135008, independent draw" was false as written.

### F5 — Exploratory score dropped → PASS
- Byte-search for "probe-decodability" and "decodability delta" across the draft: **zero matches**. The undefined quantity is fully removed, including from the §2 KILL clause's "DOES NOT LICENSE" list. The Law #7 risk is eliminated.

### F6 — Inertness gate → PASS
- New §3.7(h): per fresh random, count (item,view) pairs where ŷ_j(random) ≠ ŷ_j^cache over 5n pairs. Allowance ≤1% (⌈0.01·5n⌉; 3 of 300 at n=60). Trip: any random exceeds 1% → RUN-INVALID, exit 44.
- The (f) cache requirement now reads "full ŷ decisions AND margins per (item,view) — the decisions are required for the (h) inertness gate." The data the gate needs is guaranteed to exist.
- The false-KILL asymmetry (a secretly-efficacious random ranked correctly by S_E) is fenced: bridge-strength efficacy (≈30/300 pair-flips) exceeds the 3-flip trip by an order of magnitude.

### A1 — λ_c provenance → PASS
- §3.3: "λ_c = 0.7 (the spec's λ-grid midpoint from {0.5, 0.7, 0.9}, chosen as provisional primary — EXP068's tuning never ran, so no T3 order exists; A1 correction)." Honest and accurate.

### A2 — α transparency → PASS
- §3.2: "Expected α = 0.5 (the EXP077 C8 bridge-arm α, LOG-128 — A2 transparency); the executor asserts the LOG-128-read value equals 0.5 before proceeding." Quoted and fenced (mismatch → RUN-INVALID).

---

## The flagged judgment: §3.7(e) degeneracy-guard denominator

**Current text:** "if ANY score (primary or secondary) has zero variance across all 9 candidates on ≥30/60 items."

**The ambiguity:** with e > 0 view-precondition exclusions, n = 60 − e items are included. "≥30/60" then reads as an absolute 30 against a reduced denominator — 30/54 = 55.6% at max e, stricter than the evident 50% intent.

**Ruling:** the guard must be parameterized as **≥n/2 included items (≥30 at n = 60)**. Rationale: (1) the F2 fix established the program principle that item-count-dependent quantities use n; (2) the guard's purpose is a 50%-degeneracy apparatus check, and the threshold should preserve that fraction against the items actually measured; (3) excluded items are not part of the experiment and should not count toward either side of the fraction.

**Disposition:** this is a one-line clarification, not a scientific change. It was correctly left out of the F1–F6 repair scope (F2 covered only endpoint/null/budget). It needs a repair amendment before launch — hence PASS-WITH-AMENDMENT, not PASS.

---

## Overall verdict

**PASS-WITH-AMENDMENT.** All six required fixes and both advisories are correctly and completely applied — verified byte-by-byte against the LOG-4840 review. The decision-table bars, hypothesis, §3.5 derivation, and worth-it gate are untouched, as briefed. The single amendment: reword §3.7(e) to "≥n/2 included items (≥30 at n = 60)" to remove the denominator ambiguity under exclusions. Upon that one-line amendment, the pre-registration is launch-ready pending the CEO's launch decision.

**What was NOT changed by this lane:** the draft file itself (verification only, per the single-lane fence). The amendment must be applied by a repair lane and needs no re-verification beyond a byte-check against this report.

**Review file:** `research/reviews/LAW14_FIXVERIFY_EXP135_EVAL_2026-09-30.md` (this file)
**Log:** LOG-4842 (appended below)
