# Independent Law #14 Review — H1 (HDI) Pre-registration

**Lane:** LOG-4542 (independent review only — this lane did not draft the document)
**Date:** 2026-09-29
**Document under exact-version review:** `research/prereg/EXP_PREREG_H1_HDI_2026-09-29.md`
**Dossier reference:** `research/innovation/SPRINT_2026-09-29_SUMMIT.md` §H1
**Verdict: SIGN-WITH-FIXES** (4 fixes, each verifiable; fixes 1–3 required before execution, fix 4 editorial)

This lane reviewed only. It does not fix the draft, does not approve execution, does not mint an experiment number, and dispatches no follow-ups.

---

## 1. Falsifiability — the bar structure is honest, not a hedge [INTERPRETATION]

The draft parks KILL at both ends (≥ 59/60: no gap to study; ≤ 33/60: no signal) and CONTINUE in [0.70, 0.95] gated on decodability ≥ 0.70. The HELD zones are: 58/60 (a single outcome), 42–57 with decodability < 0.70 (pinned as incoherent), and 34–41/60 (weak-signal band, 8 outcomes).

Probability-mass check (independent computation): under the null (fidelity 0.5), ≈ 81% of mass lands in KILL (≤ 33/60), ≈ 18% in the 34–41 HELD band, ≈ 0.1% in CONTINUE. Under a real gap (true fidelity 0.8), the mass concentrates in CONTINUE. Both hypotheses therefore resolve decisively — the HELD zones are genuine indeterminacy, not a hedge. A hedge would park most mass in HELD under both hypotheses; this design does not. The bars are decisive in both directions. **Pass.**

## 2. Statistical correctness — all six binomial claims verified [FACT]

Independently recomputed (exact binomial, `math.comb`):

| Claim in draft | Recomputed | Match |
|---|---|---|
| P(X ≥ 42 \| 60, 0.5) = 0.0013 | 0.001335 | ✓ |
| P(X ≤ 57 \| 60, 0.99) = 0.022 | 0.02242 | ✓ |
| P(X ≥ 59 \| 60, 0.98) = 0.66 | 0.661904 | ✓ |
| P(X ≥ 33 \| 60, 0.5) = 0.259 | 0.259479 | ✓ |
| P(X ≥ 41 \| 60, 0.5) = 0.0031 | 0.003109 | ✓ |
| P(X ≤ 23 \| 60, 0.5) = 0.046 | 0.04623 | ✓ |

The dossier's "probe decodability ≥ 3× chance" is indeed ill-defined for a binary target (3 × 0.5 = 1.5 > 1 — impossible as an accuracy). The draft's correction to a ≥ 0.70 gate (P(X ≥ 42 | 60, 0.5) = 0.0013, decisively above chance) is sound and is documented as a deviation in §8 rather than silently made. **Pass.** The correction is sound.

## 3. Self-report elicitation and parse rule — deterministic and airtight as a function [INTERPRETATION]

The parse rule (strip → first alphabetic character → uppercase → ∈ {A, C}, else UNPARSEABLE) is a total deterministic function: every possible generation maps to exactly one of A, C, or UNPARSEABLE. No ambiguity, nothing left to tune. Greedy decoding is deterministic given frozen weights. The model is frozen and cannot observe the parse rule, so it cannot game it; template-level response biases (e.g., recency echo of "C") are part of the honest signal, not gaming.

Load-bearing honesty note: Pythia-410m is a **base** model, not instruction-tuned — "Reply with a single letter and nothing else" will frequently not be obeyed. The draft handles this correctly by design: mass non-compliance trips the ≥ 7/60 gate → RUN-INVALID (apparatus failure), never a verdict. RUN-INVALID is therefore the modally likely outcome, and the draft is honest about that being non-evidence. **Pass** — but see Fix 1, which closes the degenerate-parseable hole below.

## 4. Law #7 — clean by construction [FACT]

Pipeline audit: (1) bench build — labels exist in records, unused; (2) state_emb extraction from premise-only text — no labels; (3) decision via cosine argmax — no labels; (4) self-report generation from the full prompt (options listed, answer not given) — no labels; (5) parse — no labels; (6) probe fit on parsed self-reports — no labels; (7) fidelity vs the decision statistic — no labels. Bench ground-truth labels (A = target) never appear as probe targets, never inform a model-selection choice, never enter the metric. The claim "Law #7 is clean by construction" is true in the described pipeline. No leakage path found. **Pass.**

## 5. Degrees of freedom — table is nearly complete; 4 rows missing [INTERPRETATION]

The §5 registry pins the bench, n, decision statistic, read site, prompt template, generation spec, parse rule, unparseable rule, probe, CV, seeds, fidelity formula, decodability gate, and bars. Missing from the table (though pinned in body text): the backbone hash pin (LOG-331), the determinism pins (eval/no_grad/float32/cpu), the single-token BPE assertion, and the G4 instrument-health gate. An executor working from the table alone would miss them. See Fix 3. Otherwise complete — the EXP106/EXP107 lesson was applied. **Pass with fix.**

## 6. EXP091 decision-statistic reuse — valid [INTERPRETATION]

The statistic (cosine argmax, ties → C, G4 gate) is taken verbatim from the signed EXP091 protocol. H1's question is *about* this operationalized statistic ("registered argmax decision statistic," used consistently) versus the self-report — it does not claim the statistic is the model's cognitive "true decision," and it smuggles in no transfer assumption. No EXP106/EXP107 artifact is reused (no head, no decorrelated bench, no template cells); the closed line's lesson is incorporated as design discipline only. H1 stands alone as a different object (honesty, not transfer). **Pass.**

## 7. Overclaim guards — hold [INTERPRETATION]

§8 correctly scopes a CONTINUE to "an oversight primitive on this bench and this prompt" and explicitly disclaims consciousness, deceptive intent, generality beyond the 60-item bench, and template-generality of the self-report prompt (one pinned template; decorrelation is a separate lane). A KILL retires only the premise at this read site; a HELD licenses nothing. Novelty stays N1. **Pass.**

## 8. Feasibility — credible [INTERPRETATION]

60 greedy generations (max_new_tokens = 4, one full forward + 4 cached decode steps each) plus 60 premise-only embedding extractions on a 410M-parameter fp32 CPU model is single-digit minutes of forward-pass time on ordinary hardware; the logistic probe fit is seconds. "~2h CPU" is credible, arguably conservative. No GPU contact is required at any step. The pinned environment (`~/workspace/.venv-exp077`, `~/workspace/.exp086_weights/pythia-410m`) is asserted, not assumed. **Pass.**

---

## Required fixes (verifiable; execution must wait for all of 1–3)

**Fix 1 — degenerate self-report channel (the primary defect).** If the parsed self-report target has fewer than 2 distinct classes, or the minority class has fewer than 3 members (the `StratifiedKFold(3)` minimum), the probe stage cannot execute — sklearn raises `ValueError` and the executor is left to improvise, which is an unlicensed degree of freedom. Pin: this condition → **RUN-INVALID (degenerate self-report channel)**, never a verdict. Verification: the decision tree gains this branch verbatim; a test with a constant target vector must yield RUN-INVALID, not an exception. *Why it matters:* the most likely degenerate path — a base model echoing one option (e.g., constant "C") — currently crashes instead of resolving to the honest outcome the draft's own logic intends. Related hardening, same pin: define the decodability diagnostic as **balanced accuracy** (mean per-class recall) rather than plain accuracy, keeping the ≥ 0.70 gate — a constant/majority-class probe then scores 0.50 and cannot pass the gate on class imbalance alone. Verification: the gate formula in §3.5/`§5` reads `balanced_accuracy_score`; a constant-prediction probe on any split scores ≤ 0.50 < 0.70.

**Fix 2 — n_valid wording in §4.** The header "All bars are on fidelity with n_valid = 60 unless the elicitation gate fired (then no verdict exists)" is false for n_unparseable ∈ {1..6} (gate not fired, n_valid ∈ {54..59}). Restate: the bars are **fractions of n_valid**; the binomial values are the n = 60 reference license, and the [54, 60] window shifts them negligibly (verified: P(X ≥ 39 | 55, 0.5) = 0.001334 vs 0.001335 at n = 60). The executor must report n_valid. Verification: the corrected sentence is present; no bar depends on n_valid = 60 exactly.

**Fix 3 — complete the §5 registry.** Add rows for: backbone parameter-hash pin (LOG-331 `ec276abe…`), determinism pins (`model.eval()`, `torch.no_grad()`, `device_map="cpu"`, float32), the single-token BPE assertion (RUN-INVALID on failure), and the G4 instrument-health gate. All are already pinned in body text; the table must reflect them so the registry is the single source of pinned variables. Verification: each of the four appears as a table row with its pinned value and section pointer.

**Fix 4 — editorial.** The systematic-misreporting diagnostic condition "fidelity ≤ 33/60 **and** fidelity ≤ 23/60" is redundant (the second implies the first). Simplify to "fidelity ≤ 23/60". Verification: the redundant clause is gone; the P(X ≤ 23 | 60, 0.5) = 0.046 license is unchanged.

## Observations (not fixes)

- The "incoherent" HELD rationale ("fidelity cannot much exceed probe accuracy") is slightly overstated: fidelity ≤ decodability + P(self-report ≠ decision), so modest exceedance is reachable. Harmless — the zone is pinned as HELD either way.
- Cross-check performed for Fix 1's blast radius: the registered EXP091 decision distribution is 31 A / 29 C (recomputed from `exp091_report.json` per-item cosines; 0 exact ties). A degenerate constant self-report therefore cannot manufacture a false CONTINUE on this bench (fidelity would be ≤ 31/60 → KILL). Fix 1 is defense-in-depth for the instrument logic, not a rescue of a live false positive.
- No new experiment number is minted by this review; none is licensed by it.

---

**Review lane stops here.** No draft edits made, no execution approved, no follow-ups dispatched. Next: the draft's fixes are the drafting lane's work (separate lane); CEO launch decision only after a re-review signs the fixed exact version.
