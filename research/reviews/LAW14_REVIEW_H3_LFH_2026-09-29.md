# Law #14 Independent Review — EXP_PREREG_H3_LFH_2026-09-29.md

**Review lane:** LOG-4530 (pre-assigned). **Independent** of the LOG-4529 drafting lane — this reviewer did not write the document under review.
**Date:** 2026-09-29
**Artifact under exact-version review:** `research/prereg/EXP_PREREG_H3_LFH_2026-09-29.md` (H3 — LFH: Label-Free Head pre-registration, drafted under LOG-4529 from `research/innovation/SPRINT_2026-09-29_SUMMIT.md` §H3)
**Scope:** $0 CPU. Read-only everywhere except this file and the LOG-4530 log append. No execution approved, no experiment number minted, no follow-up dispatched.

## Verdict: SIGN-WITH-FIXES

The pre-registration is falsifiable, statistically sound, Law-compliant, and honestly scoped — but it leaves **two method degrees of freedom unpinned** (regularization strength, embedding layer/source) that an executor could tune post-hoc. Three fixes are required before execution; each is verifiable by inspection of the revised draft. No fix changes the decision bars, the hypothesis, or the verdict logic.

---

## 1. Falsifiability — PASS (with observation)

- Decision bars are decisive in both directions and pre-committed: **≥ 40/60 → CONTINUE**, **≤ 35/60 → KILL**, **36–39 → HELD** (licenses nothing, retires nothing, no re-runs, no larger-n rescue — the rescue is explicitly barred as a gate tweak).
- The HELD zone is **honest, not a hedge**: it is pre-committed, it licenses NOTHING, and it cannot be revisited. The falsifier (≤ 35/60) is a genuine kill — it retires the output-side room and deepens LOG-204.
- **OBS-2:** the CONTINUE bar (one-sided p = 0.0067) is ~7× stricter than α = 0.05 — outcomes 37–39/60 (P(X≥37) = 0.046, P(X≥38) = 0.026, P(X≥39) = 0.014, verified independently) would be "significant" at the looser standard but are HELD here. This is a conservative, pre-committed choice that errs toward inconclusive rather than false-positive. Acceptable; noted for the record.

## 2. Statistical correctness — PASS (independently verified)

Computed independently (scipy, n = 60, p = 0.5):
- P(X ≥ 40) = **0.006745** — draft's "≈ 0.0067" correct. The dossier's loose "≈ 0.003" (which is P(X ≥ 41) = 0.0031) was honestly corrected in the draft and the deviation documented. ✓
- P(X ≥ 36) = **0.077501** — draft's "0.078" correct. ✓
- P(X ≤ 35) = **0.922499** — draft's "0.92" correct; the KILL bar "deliberately fails to distinguish from chance" is an accurate reading. ✓
- One test, one bench, one primary metric — no multiplicity problem.
- **OBS-6:** the binomial p-values assume item independence; this is the program's established bench convention (consistent with EXP091/EXP105). Noted, not a defect.

## 3. Law compliance — PASS (with required fixes)

- **Law #6 (frozen backbone):** hash recorded before and after; any mismatch → RUN-INVALID, quarantine, no metric read (Law #13). Adequate. The backbone pin (`ec276abe…`, LOG-331) is cited via the dossier rather than restated — acceptable.
- **Law #7 (zero data leakage):** the overlap tripwire is airtight procedurally — item-ID intersection computed **before any training**, overlap > 0 → RUN-INVALID, abort, provenance repair. "No test labels, targets, or EXP091 embeddings beyond the frozen features may touch the training objective" is correctly stated. **OBS-1:** exact item-ID match will not catch near-duplicate paraphrases; acceptable given independently constructed benches, but see FIX-3 which closes the adjacent model-selection loophole.
- **Law #4 (no post-hoc shifts):** bars pre-committed; "any hypothesis rewording after seeing the metric" is recorded as BARRED scientific misconduct. Compliant — **except** the two unpinned method choices below, which are post-hoc tuning vectors the draft does not close. Hence the fixes.

## 4. JEV-27B block-off discipline as CONTINUE precondition — PASS (with observation)

- Correctly specified as a **precondition on admissibility**: byte-identity check on head-attached vs head-detached outputs over the full test bench; any mismatch → apparatus INVALID; "a CONTINUE verdict with a failed block-off is void." The gate order (block-off before any capability claim) is right.
- **OBS-3:** under the stated method — an external, detachable readout on archived frozen embeddings — the head cannot perturb the backbone by construction, so the check passes vacuously; Law #6's parameter-hash check already covers backbone perturbation. The check is harmless as specified and its CONTINUE-precondition logic is correct, but it tests almost nothing in this design. Considered, not a required fix.

## 5. Overclaim guards — PASS

- §7 holds under adversarial reading: a CONTINUE is "a first positive signal, not superhuman cognition, not consciousness, not generality beyond the EXP091 bench, and not evidence about internal mechanisms of cognition." No sentence promises superhuman cognition, generality, consciousness, or capability beyond the bench.
- The draft explicitly disclaims JEV-27B replication ("its honest CPU shadow"), holds novelty at **N1 — Known Combination** (N2-adjacent only on independently verified CONTINUE), and states that a KILL retires the room, not the summit program. Clean.

## 6. Feasibility honesty — PASS

- "$0 CPU, ~30 min, no GPU contact" is credible: a ~2k-parameter logistic fit on 60 training items is seconds of CPU; a single 60-item forward extraction on frozen Pythia-410m fits the ~30-minute envelope; the "zero new forwards if archived" branch is stated conditionally and honestly.
- Nothing in the method requires GPU contact, weight access beyond frozen reads, or new training data. The lane-scope statement (drafting only; no signed protocol, weights, GPU queue, push, or PR touched) is accurate.

## 7. Assertions vs cited sources — PASS (with observation)

- The dossier's worth-it gate, the LOG-204 artifact interpretation, the Decodability Gap numbers, and the backbone pin are all cited from program records and used within their licensed scope.
- **OBS-5:** §3.4 tags the JEV-27B discipline adoption as [FACT]. The *adoption* is a fact; the underlying JEV-27B byte-identity claim is vendor-claimed and UNVERIFIED per the 2026-09-29 sweep itself. The draft does not assert the vendor claim as fact (§7 disclaims replication), so no misrepresentation — but a future reader should not read the [FACT] tag as endorsing JEV-27B's claim.
- §3.5 (linear-probe theory) is tagged [THEOREM — stated, reviewed separately]; the statement (a linear head cannot manufacture information absent from the embedding — data-processing inequality) is a legitimate mathematical license, and the "reviewed separately" caveat is honest.

---

## Required fixes (each verifiable by inspection of the revised draft)

**FIX-1 — Pin the L2 regularization strength (Law #4 / Law #9).**
The draft says "L2-regularized logistic regression" but never pins λ (or C), nor the selection rule. An executor could tune λ against the EXP091 test bench to push a 38 into a 40 — a post-hoc shift the current text does not bar.
*Fix:* state the exact value (e.g., C = 1.0) **or** the exact selection rule using train data only (e.g., k-fold CV on EXP092-B). No EXP091 label may inform λ.
*Verification:* the revised draft names the value or the rule; absent either, the fix is not done.

**FIX-2 — Pin the embedding source (Law #4 / Law #9).**
The draft says "frozen backbone embeddings" without naming the layer (or multi-layer combination rule), and "archived embeddings if … on disk" without citing which archive. An executor could fish across layers and report the best.
*Fix:* name the single backbone layer (or an explicit multi-layer combination rule), and either cite the archive path with its layer provenance or state the full extraction spec (layer, pooling, item encoding).
*Verification:* the revised draft names the layer/source; absent, the fix is not done.

**FIX-3 — Extend the Law #7 bar to model selection (Law #7).**
§3.2 bars test labels from "the training objective" but not from model-selection decisions (λ, layer, decision threshold).
*Fix:* add one sentence — "No EXP091 test label, target, or metric may inform any model-selection choice (regularization strength, embedding layer/source, decision threshold); all such choices are pinned above or derived from train data only."
*Verification:* the sentence (or equivalent) is present.

**No fix changes the hypothesis, the decision bars, the verdict logic, or the scope.** After the three fixes are verified in the draft, this review's verdict upgrades to SIGN and the artifact is cleared for the CEO launch-decision lane. Execution remains gated on a minted experiment number and founder-authorized lanes — this review approves nothing beyond the document.

---

## Reviewer independence statement

This reviewer did not draft, edit, or contribute to `EXP_PREREG_H3_LFH_2026-09-29.md` or the SPRINT_2026-09-29_SUMMIT.md H3 section. All statistics above were recomputed independently. $0 compute spent; no repo state modified except this review file and the LOG-4530 append. Lane stops here.
