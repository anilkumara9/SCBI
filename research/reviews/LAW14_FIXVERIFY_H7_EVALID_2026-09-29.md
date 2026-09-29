# Law #14 Fix-Verification: H7/EVALID pre-registration repairs

**Verification lane:** LOG-4582 (pre-assigned). **Document verified:** `research/prereg/EXP_PREREG_H7_EVALID_2026-09-29.md`. **Review under verification:** `research/reviews/LAW14_REVIEW_H7_EVALID_2026-09-29.md` (LOG-4580, SIGN-WITH-FIXES, 2 fixes). **Repair lane:** LOG-4581. **Verifier posture:** independent of drafting and repair lanes; $0 CPU; read-only except this file and the log append.

**Verdict: ALL-FIXES-VERIFIED** — the LOG-4580 independent Law #14 review on `EXP_PREREG_H7_EVALID_2026-09-29.md` is explicitly **upgraded to SIGN**.

---

## F1 — Hypothesis/falsifier wording contradiction — PASS

The review found §1's hypothesis ("…at least one of five pinned elicitation protocols produces ≥80% … **on both** T1 and T2") contradicted §4's binding CONTINUE ("T1-CLEAR ≠ ∅ **and** T2-CLEAR ≠ ∅", possibly different protocols). The repaired §1 now reads (exact text found):

> **[HYPOTHESIS]** At least one of five pinned elicitation protocols clears the 80% mechanically-parseable structured-output bar on each task — the single-token answer task (T1, the H1 self-report shape) and the numbered-outline task (T2, the H4 planner shape) — from frozen base Pythia-410m under CPU greedy-decoding protocols. The clearing protocols need not be the same on T1 and T2.

> **Falsifiers:** per the §4 decision tree — CONTINUE if at least one protocol clears ≥80% on each task (not necessarily the same protocol); PIVOT if clearance occurs on exactly one task; HELD if the best protocol reaches 22–47/60 on at least one task with no clearance; KILL if every protocol scores ≤21/60 on both tasks.

Cross-check against the rest of the document: §2's exact question ("produce ≥80% parseable structured outputs … on each of the two downstream task shapes?") and §2's decision mapping ("at least one protocol clears ≥80% on T1 **and** at least one (possibly different) protocol clears ≥80% on T2") both agree with the §4 binding bars. No reading of §1 contradicts any branch of the §4 decision tree. The contradiction is gone.

## F2 — Joint-probability independence qualification — PASS

The review required the §4 joint-probability sentence to state the independence assumption, give the correlation-robust upper bound, and keep the Wilson-license sentence unchanged. The repaired sentence reads (exact text found):

> Moreover P(all five protocols ≤21/60 | every true rate ≥ 0.5) ≈ **5×10⁻¹⁰** — *under the independence approximation*: the five protocols share the same 60 items and the same frozen backbone, so outcomes are positively correlated, and the correlation-robust upper bound is the single-protocol value P(Bin(60,0.5) ≤ 21) ≈ **0.014**. The KILL's license rests on the per-protocol Wilson upper bound (0.4558), which requires no independence assumption.

All three required elements present verbatim: (1) the independence assumption stated explicitly ("*under the independence approximation*"); (2) the correlation-robust upper bound (≈0.014, the single-protocol value); (3) the note that the KILL's license rests on the per-protocol Wilson upper bound (0.4558), which requires no independence assumption. The Wilson-license sentence ("21/60: one-sided 95% Wilson upper bound = **0.4558 < 0.50**. A KILL therefore licenses the claim 'no tested protocol reaches 50% true parseability.'") is present and unchanged.

---

## Spot-check — PASS

Decision bars unchanged (CONTINUE: T1-CLEAR≠∅ and T2-CLEAR≠∅ with r≥48; PIVOT: exactly one; HELD: 22–47/60, no clearance; KILL: max ≤21/60 on both tasks). All five protocols per task present with pinned verbatim templates, greedy decoding, `max_new_tokens`, seeds, thread count, and item order. All statistical numbers unchanged (Wilson lower 0.7030, Wilson upper 0.4558, selection-bias disclosures 0.25 / 0.004, dossier-bar correction 0.5879). Anti-self-deception machinery unchanged (mechanical pinned parse rules, deterministic re-parse ×2 with byte-identical assertion, no pilot phase, no early abandonment, per-generation exceptions scored UNPARSEABLE, >10% → RUN-INVALID, 0/60 is a VALID measurement). Seven dossier deviations and the §7 overclaim fences unchanged. The repair touched exactly the two required sentences.

---

**Boundary:** this lane verified only — no draft edits, no execution approval, no experiment number minted, no follow-ups dispatched. The CEO launch decision is a separate lane.
