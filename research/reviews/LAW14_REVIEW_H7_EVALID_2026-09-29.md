# Independent Law #14 Review: H7/EVALID pre-registration

**Review lane:** LOG-4580 (pre-assigned). **Document under exact-version review:** `research/prereg/EXP_PREREG_H7_EVALID_2026-09-29.md` (the H7 pre-registration as it stands at review time; this review names that exact filename).
**Reviewer posture:** independent of the drafting lane (LOG-4579). $0 CPU. Read-only except this file and the log append.
**Verdict: SIGN-WITH-FIXES** (2 fixes, both verifiable, non-structural). Nothing structural is wrong; the decision bars, guards, and licensing are sound.

---

## 1. Scope of verification

I verified against: the round-2 dossier `research/innovation/SPRINT_2026-09-29_SUMMIT_ROUND2.md` (§H7, §4 ranking), the EXP108 execution report `research/experiments/EXP108_HDI_REPORT_2026-09-29.md`, the EXP109 execution report `research/experiments/EXP109_PTTSC_REPORT_2026-09-29.md`, and the original pre-registrations `research/prereg/EXP_PREREG_H1_HDI_2026-09-29.md` (§3, lines 57–60) and `research/prereg/EXP_PREREG_H4_PTTSC_2026-09-29.md` (§3.3, lines 48–56). All statistical claims below were independently recomputed in Python (exact binomial sums; Wilson score interval, one-sided 95%, z=1.645).

---

## 2. What passed (verified)

**Anchor fidelity.** Both P1 anchors are truly verbatim as the draft's [FACT] labels claim:
- T1-P1 template + greedy + `max_new_tokens=4` matches the EXP108 pre-reg's pinned generation spec exactly (line 57: the same "Reply with a single letter and nothing else." sentence).
- T2-P1 template + greedy + `max_new_tokens=160` matches the EXP109 pre-reg's pinned planner spec exactly (line 50).
- The T2 extraction rule (first-occurrence positions of literal `1.`–`4.` markers, spans between consecutive markers in position order, stripped, drop empties/exact duplicates, ≥2 distinct non-empty) yields the identical parseability verdict as EXP109's pinned planner-valid rule on every input (EXP109's extra clauses — preamble discarded, missing marker → empty outline — change no verdict under the ≥2 rule). The [FACT] "identical to EXP109's planner-valid rule" holds at the verdict level.
- The T1 first-alpha rule (strip, first alphabetic, uppercase, ∈ {A,C}) matches the EXP108 pre-reg's pinned parse rule exactly.

**All statistical claims recomputed exactly — six for six:**
- 48/60 one-sided 95% Wilson lower = **0.7030** ✓
- 21/60 one-sided 95% Wilson upper = **0.4558 < 0.50** ✓ (licenses the KILL's "no tested protocol reaches 50% true parseability" — each protocol individually satisfies it, so no independence assumption is needed for the Wilson license)
- Dossier's ≤29/60 one-sided 95% Wilson upper = **0.5879 ≥ 0.50** ✓ — deviation 1's claim is correct: the dossier's bar is mathematically unable to license "true rate < 50%". Genuine repair.
- P(any ≥48/60 | all five true rates = 0.70) = **0.2534 ≈ 0.25** ✓
- P(any ≥48/60 | all five true rates ≤ 0.60) = **0.0040** ✓
- P(all five ≤21/60 | all five true rates ≥ 0.5) = **4.77×10⁻¹⁰ ≈ 5×10⁻¹⁰** ✓ *under the independence approximation* — see F2.

**KILL license.** The KILL claim ("no tested protocol reaches 50% true parseability") is licensed by the per-protocol Wilson upper bound 0.4558: every protocol observes ≤21/60, so each protocol's upper bound applies to that protocol directly. Valid.

**No residual tuning freedom.** All five protocols per task pin prompt templates verbatim, greedy decoding (`do_sample=False`), `max_new_tokens`, and (P4) `repetition_penalty=1.2` / `no_repeat_ngram_size=3`; temperature is irrelevant under greedy; seeds (torch/numpy = 0), thread count, item order (bench build order), and exemplar item indices (T1-P2: items 0/1/2; T2-P2: items 3/4 with verbatim outlines) are all pinned. The execution lane cannot adjust anything after seeing results without violating Law #4, and the decision tree's "No other branches exist" closes the door.

**P1-anchor "environment is suspect" logic.** Registered as [OBSERVATION], read by no decision branch — a sanity signal, not a verdict lever. Sound and honest.

**HELD zone.** Principled, not a cop-out: the selection-bias disclosure shows the ~0.65–0.75 true-rate zone is where max-over-5 selection bias bites hardest (P(any ≥48/60 | true 0.70) ≈ 0.25); the 22–47/60 zone absorbs it, licenses nothing, retires nothing. Correct design.

**PIVOT.** Coherent per-axis licensing: H1 needs single-token answers, H4 needs numbered outlines — different elicitation shapes, so a cleared T1 with a failed T2 honestly licenses only the H1-revival lane. Not artificial.

**Anti-self-deception.** Airtight at the pre-reg level: mechanical pinned parse (pure function of raw logs), deterministic re-parse ×2 with byte-identical assertion (mismatch → RUN-INVALID), no pilot phase, no early abandonment (all 600 generations complete regardless of intermediate results), no mid-run protocol modification, per-generation exceptions logged and scored UNPARSEABLE (never silently dropped), >10% exceptions → RUN-INVALID, and a 0/60 protocol is a VALID measurement. No loophole for silent mid-run fixing that I can find.

**Law #7.** Bench labels appear only as the T1-P2 exemplar answers (disclosed in §3.1); the registered metric is parseability (format), never correctness — a constant "A" output scores 60/60 regardless of labels, so no label exposure can inflate any registered number. The parse rules never read labels. Sound.

**Deviations 2–7.** All genuine repairs, none smuggled weakenings: HELD absorbs the selection-bias zone (harder, not easier, than forcing a verdict); PIVOT covers the dossier's binary gap; the two new explicit-stop protocols (T1-P3, T2-P3) add families the dossier lacked — adding protocols makes KILL *harder* (all five must fail), so this cannot weaken the test; the full-60 T2 bench is required for the Wilson-licensed bars; the blocklist-as-diagnostic is correct (a protocol hitting the attractor *is the data* — gating on it would invalidate the measurement); the two-task structure is required for per-axis licensing.

**Cost.** ~2–4h $0 CPU is conservative-honest: calibrated against EXP109 (108 generations in 20.9 CPU-min ≈ 11.6s per ≤160-token generation); 600 generations ≈ 1.5–2.5h plus overhead. No $0-constraint issue. The generation-as-subject exception is explicitly fenced to this apparatus question.

---

## 3. Required fixes (2, verifiable, non-structural)

**F1 — Hypothesis/falsifier wording contradicts the binding decision bars.**
§1's hypothesis reads: "At least one of five pinned elicitation protocols produces ≥80% mechanically-parseable structured outputs ... **on both** T1 and T2," with falsifiers "no protocol clears ≥80% **on both** tasks (→ PIVOT / HELD / KILL per §4)." But §4's binding CONTINUE is "T1-CLEAR ≠ ∅ **and** T2-CLEAR ≠ ∅" with the explicit "(possibly different)" protocol allowance. CONTINUE can therefore fire when NO single protocol clears both tasks (e.g., T1-P3 clears T1 while T2-P5 clears T2) — in which case the §1 falsifier ("no protocol clears ≥80% on both tasks") is simultaneously true. The binding bars and the hypothesis sentence cannot both be literally true. The §2 exact question ("on each of the two downstream task shapes") agrees with §4. Fix: reword §1's hypothesis and falsifier sentences to the per-task licensing form — e.g., "at least one protocol clears the 80% bar on each task (not necessarily the same protocol)" — and restate the falsifiers as the §4 outcome mapping. Verify: after the edit, no reading of §1 contradicts any branch of the §4 decision tree.

**F2 — Joint-probability decisiveness claim needs its independence assumption stated.**
§4: "P(all five protocols ≤21/60 | every true rate ≥ 0.5) ≈ 5×10⁻¹⁰ — the KILL is decisive, not a matter of taste." My recomputation confirms 4.77×10⁻¹⁰ **under the independence approximation** — but the five protocols share the same 60 items and the same frozen backbone, so outcomes are positively correlated. Under arbitrary positive correlation the joint probability lies between the independent value (≈5×10⁻¹⁰) and the single-protocol value (P(Bin(60,0.5) ≤ 21) = **0.0137**, verified). Fix: qualify the sentence — state the independence assumption explicitly, give the correlation-robust upper bound (≈0.014, the single-protocol value), and note that the KILL's license rests on the per-protocol Wilson upper bound (0.4558), which requires no independence assumption. Verify: the edited sentence contains both the assumption and the bound, and the Wilson-license sentence is unchanged.

---

## 4. Verdict

**SIGN-WITH-FIXES** on the exact filename `EXP_PREREG_H7_EVALID_2026-09-29.md`. F1 and F2 are the only defects found; both are wording-level, verifiable by re-reading the edited sentences, and change no bar, guard, protocol, or number. The repair lane applies exactly F1 and F2; fix-verification re-reads the two sentences; no re-review of the whole document is needed.

**Boundary:** this lane reviewed only — no draft edits, no execution approval, no experiment number minted, no follow-ups dispatched.
