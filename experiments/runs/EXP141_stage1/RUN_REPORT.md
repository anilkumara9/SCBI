# EXP141 Stage-1 Run Report (S4-6 metacognitive self-modeling CPU pilot)

**Pre-reg:** `research/prereg/EXP_S46_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4889). CEO venue approval: Stage-1 CPU pilot only (60 self-eval passes). $0 compute.

## Validity gates — all PASS
- (a) bench sha256: `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` — PASS
- (b) backbone pre-hash: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — PASS
- (c) EXP140 B0 record id alignment 60/60; B0 answers re-read from committed records (no regeneration) — PASS. B0 baseline accuracy 0.7000 (matches EXP140).
- (d) backbone post-hash matches pin (Δθ=0) — PASS
- Pass counts: 60 self-eval forwards (budget 60) — PASS; 0 failed self-evals
- Token "A" verified single (id=34)

**Baseline-answer reconstruction note (pre-reg interpretation, documented):** the committed EXP140 B0 records store per-branch `correct` (bool), not the answer text. B0 = argmax over {tok1(v["A"]), tok1(v["C"])} (EXP140 script notes; EXP139 precedent). The committed answer text is therefore exactly v["A"] if branch-0 correct else v["C"]. The bench label is used here solely as a decoding key for a committed experimental quantity — the answer B0 actually chose is fixed regardless; labels influence no self-eval score, trigger, revision, or gate threshold (Law #7 firewall intact; see §7 of pre-reg).

## Binding gates
- **G1 signal-variance:** std(â_self) = 0.000045 (bar > 0.01), non-constant=True — **FAIL**. The self-model signal is degenerate: the model assigns essentially the same P("True") to all 60 answers. This is the Xu et al. self-bias confound the design predicted — the model rates its own output uniformly, yielding a vacuous signal.
- **G2 I-screen:** Î_obs = 0.0716 nats (Miller-Madow corrected), 100k-permutation p = 0.18100 (bar < 0.05) — **NULL**.
- **G3 calibration:**
  - C1: Spearman(â_self, correctness) ρ = -0.1260, one-sided p (licensed, +) = 0.83134 — **null** (not inverted: wrong-direction p = 0.16866 > 0.05)
  - C2: n_wrong=18, n_right=42; D_obs = 0.000007, one-sided p (licensed) = 0.71532 — **null** (not inverted)
  - **G3: NULL** → no GPU (family stands down on this branch alone)

## Secondary diagnostic (reported, not binding)
- AUC(â_self → correctness) = 0.4206, DeLong 95% CI [0.2500, 0.5912] — below 0.5 but CI includes chance; not significantly inverted.

## Verdict: KILL (self-model)

**Reading per the binding falsification tree (pre-reg §5, precedence KILL (any) > PIVOT > CONTINUE > HELD):** G2-null (p = 0.181 ≥ 0.05) triggers **KILL (self-model)** — "no correctness information in the self-model → the family is dead before revision" (binding bar from backlog row 24).

**Precedence note:** the executing script initially emitted HELD (a) by checking G1 first. This was corrected per the pre-reg's explicit precedence: KILL outranks HELD. The G1 degeneracy is not an apparatus failure that voids the test — it is the *mechanism* of the kill. The Xu et al. self-bias confound is a real property of the elicited self-model (the model genuinely assigns near-constant P("True")), and a vacuous signal carries no information by construction. G2-null (p=0.181) confirms the absence of information even in the tiny residual variance. The HELD (a) "not a verdict on the hypothesis" reading applies to apparatus-level degeneracy; here the degeneracy is the empirical finding.

**What died:** the S4-6/J2 metacognitive self-modeling family at Stage 1. The frozen Pythia-410m's P(True) self-evaluation of its own answers carries no correctness information (I ≈ 0). The honest prior (LOW) is confirmed. No revision stage runs. No Stage-2 GPU.

**Boundary statement:** on the 60-item decision bench at Pythia-410m, the model's self-evaluation is a near-constant signal (std 4.5e-5) with no measurable mutual information with correctness. This is consistent with the TESTA/EXP140 pattern (internal signals track the model's policy, not correctness) and with Huang et al./Kamoi (no successful prompt-only self-correction in fair settings).

## Files
- `run_stage1.py` — execution script (verbatim pre-reg implementation + documented interpretation notes)
- `stage1_records.json` — per-item records (60 items: a_self, b0_correct, b0_answer, bin) + gates + pins + precedence note
- `stage1_verdict.json` — gate verdict
- `stage1_run_log.txt` — run log
