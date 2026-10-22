# Independent Law #14 Review — H13 (HDI-LOC) Pre-registration
**File under review:** `research/prereg/EXP_PREREG_H13_HDILOC_2026-09-29.md`
**Review lane:** LOG-4617 (pre-assigned). $0 CPU. Independent of the LOG-4616 drafting lane.
**Date:** 2026-09-29.

## VERDICT: SIGN-WITH-FIXES

The science is sound: every binding number survived independent recomputation, the bar tiling is gapless, and the design is genuinely new data under a pinned apparatus. But the draft is **structurally incomplete and carries two factual inaccuracies** — it cannot be signed until fixed. Four fixes (FIX-1 through FIX-4 below) with exact prescribed wording/location. Fix-verification by a separate lane before any CEO launch.

---

## 1. What survived independent recomputation

**Statistical license (§0d / §4) — all numbers EXACT:**
- Per-layer SE under no-locality null (flat 0.6833): √(0.6833×0.3167/60) = 0.0601 ✓
- Window-mean SE (independence): 0.0601/3 = 0.0200 ✓
- SE(C) = 0.0283 ✓; C ≥ 0.10 → 0.10/0.0283 = 3.53σ, two-sided p = 2(1−Φ(3.53)) = 4.2×10⁻⁴ ≈ 4×10⁻⁴ ✓
- Attenuated df (~3 effective layers/window): SE(C) = 0.0601/√3×√2 = 0.0490 ✓; 0.10/0.0490 = 2.04σ, p ≈ 0.041 ✓
- KILL-bar miss rate under true C = 0.10: P(C<0.05) = Φ(−0.05/0.0283) = Φ(−1.77) = 0.038 ≈ 0.04 (independence); Φ(−1.02) = 0.154 ≈ 0.15 (attenuated) ✓
- §0 item 5 arithmetic: (0.6833 + 8x)/9 ≥ 0.65 → x ≥ 0.64583 → 0.6458 ✓
- P(X ≥ 41 | 60, 0.5) = 0.0031 carried verbatim from the signed EXP112 report ✓

**Bar tiling (§4) — gapless:** C ≥ 0.10 ∧ late ≥ 0.65 → CONTINUE; |C| < 0.05 → KILL; C ≤ −0.10 → KILL; 0.05 ≤ C < 0.10 (any late) → HELD; C ≥ 0.10 ∧ late < 0.65 → HELD; −0.10 < C < −0.05 → HELD. Full coverage of the real line; no razor-thin CONTINUE (dual bar, 2–3.5σ from the no-locality null, plus the independent late ≥ 0.65 demand); reverse-concentration KILL present. No other reading licensed.

**Run-validity rule (§3.5) — genuine:** < 5 non-degenerate sites in either window → RUN-INVALID, with window means computed over non-degenerate sites only. This blocks the false-CONTINUE path: a degenerate window can never enter the contrast — the run invalidates first. The §6 tree registers it before any metric (Law #9).

**New-data license — confirmed:** EXP111's per-layer analysis (EXP111 report §6–§7) trains L2-logistic heads on activations — a trained instrument, not a zero-training logit lens. No logit-lens self-report profile was ever computed for H6/EXP111/EXP112. The 1080 forwards are new data; the only re-read datum is EXP112's archived decision column as a fixed measurement target with a 41/60-exact HALT-on-drift consistency pin — a pin, not a metric re-test. Not Law-#9 theater.

**Laws #4/#6/#7/#13:** bars binding; backbone hash before/after all fresh forwards vs the LOG-331 pin; seeds/threads pinned; Law #7 clean by construction (no labels touch the apparatus); environment manifest matches the EXP107/EXP108/EXP112 registry.

**Compute envelope:** 1080 forwards, zero generation, frozen backbone — EXP112 did 180 forwards in ~86 s on CPU, so the run is comfortably inside the licensed $0 CPU envelope. No GPU contact.

**H12 kill honored:** the per-cell diagnostic is dropped (§3.8, §5 table); no decision branch and no diagnostic reads the cells. Verified by body sweep.

**H6 fence (§7.1 concept) — airtight in substance:** the draft fences that no H13 outcome changes EXP112's HELD. H13 asks where the signal lives; H6's existence question is not re-verdicted. The fence language is correct — but see FIX-2 (it lives nowhere in the document).

---

## 2. Defects found

### DEFECT A (structural, blocking): the document is incomplete
The file ends at §6, and §6's falsification-decision-tree table is a **literal truncation placeholder** (`...[truncated 4156 chars]` — line 152, verified in raw bytes). §§7–10 do not exist — yet the body repeatedly references them:
- §0(c): "fenced in §7.1"
- §1.1: "cannot upgrade it — §7.1"
- §2: "§7.1"
- The drafting-lane handoff claimed "the honesty fence (§7.1)" and "§10 deviation list is exhaustive (12 items)" — neither exists in the file.

A pre-registration whose falsification tree is a placeholder and whose referenced honesty fence and deviation list are absent is not launch-eligible.

### DEFECT B (factual, fixable): wrong read-site identity
The draft repeatedly calls EXP112's archived 41/60 "the L20 read site" / "L20's known 41/60" (§0 items 4–5, §1.1, §3.2). Per H6 §3.4 (pinned) and EXP112 report §6, the readout was **the logits at the final (answer) position** — the model's output logits, which is exactly the logit lens (LayerNorm_f + unembedding) applied at hidden_states[24], not L20. (The "hidden_states[20]" in EXP112's environment manifest is the decision arm's archived state-embedding site, §3.3.) The consequence is benign but real: the late window {16..24} *contains* the archived site, so the §3.2 consistency pin is a true byte-level identity check — the draft should say so.

### DEFECT C (citation, fixable): "H6 §8.5" does not exist
§0(c) cites "H6 §8.5 barred a KILL/HELD being 'followed by a different layer'". H6's pre-registration has no §8.5 and no such clause under that name. The actual bar is H6 §4's "No rescue runs" clause (verbatim): "A HELD or KILL is never followed by a larger-n re-test, a different layer, a different carrier, or a re-read — each would be an unlicensed gate tweak (barred)." The substantive interpretation (the bar addressed re-running H6's *existence* question as a rescue; H13 asks a *different question*) is defensible, but the citation is wrong and must be corrected.

### Deviation-list sweep (the H9-review lesson)
§5's "Contrast C" row and §3.5/§3.8 deviations were checked against the body. No undocumented twelfth-or-thirteenth adaptation was found in the *existing* sections — but the exhaustive §10 list claimed by the drafting lane does not exist (Defect A). The fix-verification lane must confirm the new §10 is complete against the body.

---

## 3. Required fixes (exact wording/location)

### FIX-1 — complete §6's falsification decision tree
Replace the placeholder row (`| Bench/np ...[truncated 4156 chars]`) with this complete table body (verbatim):

```
| Bench canonical-JSON or npz/embeddings/ids pins ≠ pinned | HALT | Apparatus drift. Licenses nothing. |
| Consistency pin: recomputed fidelity ≠ 41/60 exactly | HALT | Archive drift in the archived decision column. Licenses nothing. |
| Backbone hash before/after fresh forwards ≠ LOG-331 pin | RUN-INVALID | Law #6. Quarantine. No metric may be read. |
| BPE single-token re-assertion fails on any item | RUN-INVALID | Tokenization contract broken; items NOT dropped. Not a verdict. |
| < 5 non-degenerate sites in either window | RUN-INVALID | Logit-lens apparatus failure — the channel cannot speak. Not a verdict. |
| C ≥ 0.10 and late-window fidelity ≥ 0.65 | CONTINUE | Late-layer localization is real. |
| \|C\| < 0.05 | KILL | Signal diffuse — locality question retired; EXP112's HELD stands unchanged. |
| C ≤ −0.10 | KILL | Reverse concentration — late-locality hypothesis falsified. |
| 0.05 ≤ C < 0.10 (any late), C ≥ 0.10 with late < 0.65, −0.10 < C < −0.05 | HELD | Indeterminate. Licenses nothing, retires nothing, no re-runs. |
| Any hypothesis rewording after seeing the metric | BARRED | Law #4. Scientific misconduct, not a verdict. |
```

### FIX-2 — add the missing §§7–10 (verbatim content below)

**§7. Honesty fence**
### 7.1 EXP112's HELD is untouchable
No H13 outcome — CONTINUE, HELD, KILL, or RUN-INVALID — changes EXP112's registered HELD verdict (41/60). H13 asks where the signal lives, not whether H6's existence question re-verdicts. A CONTINUE licenses layer-window localization of the self-report signal as a mechanistic foothold for later, separately-licensed lanes only; it does not upgrade, re-open, or re-measure EXP112.
Fidelity between two readouts of the same frozen backbone is a decoding correlation, not honesty in any introspective sense; a localized signal is a layer window, not a mechanism.

**§8. Cost / honesty statement [FACT]**
- $0 compute. No GPU contact. No training. Backbone frozen, Δθ=0.
- ~1080 forward passes (60 items × 18 layer sites), CPU, float32, zero generation — comparable to EXP112's 180 forwards in ~86 s; inside the licensed $0 CPU envelope.
- This lane drafts only: no execution, no experiment number minted, no signed protocol touched, no push, no PR.

**§9. What H13 does NOT claim**
1. A CONTINUE does not claim the model "knows" its decision in any introspective sense — only that the two-way logit-lens readout's agreement with the registered decision statistic concentrates in late layers.
2. Not consciousness, not deceptive intent, not generality beyond the 60-item bench, not capability of any kind.
3. A KILL retires the locality question only — EXP112's HELD stands unchanged; the summit program is unaffected.
4. A HELD licenses nothing and retires nothing — no larger-N rescue, no different window, no different lens, no re-read (all barred).
5. Novelty: N1 — Known Combination (logit lens is a known instrument applied to a new question — Law #10).
6. Unsigned and unreviewed until the independent Law #14 lane signs or rejects.

**§10. Deviations from H6's pre-registered spec (complete list)**
1. **New question:** H6 measured the self-report signal's existence at one read site; H13 measures where it lives across 18 sites. The contrast C, windows, and bars are registered before any per-layer forward; H6's "No rescue runs" clause (H6 §4) bars re-running the *existence* question, which H13 does not do (see §0c).
2. **18 layer sites vs one:** hidden_states indices {0..8} ∪ {16..24} (final logits = lens at L24) vs H6's single final-logits site.
3. **Logit-lens readout:** LayerNorm_f(h_L) @ W_U per site vs H6's output logits — identical at L24 by construction; no lens tuning.
4. **Per-site degeneracy diagnostic + run-validity rule (§3.5):** new — the H6 G1 rule applied per site, with < 5 non-degenerate sites/window → RUN-INVALID.
5. **Contrast statistic C** replaces the fidelity metric as the primary statistic; fidelity becomes a per-site component.
6. **New decision bars:** CONTINUE/HELD/KILL on C and late-window fidelity (§4), replacing H6's fidelity bands.
7. **Consistency pin** on EXP112's archived decision column (41/60-exact HALT-on-drift): new.
8. **G1/G2 guards** carried as archived pins, not re-checked (decision column is archived, §3.2).
9. **Per-cell diagnostic dropped** — cell stratification was killed at the H12 worth-it gate (p = 0.0946 noise).
10. **Option-embedding forwards dropped** — decision column is archived; no 120 fresh single-token forwards.
11. **Compute:** ~1080 forwards (60 × 18 sites) vs H6's 180; still $0 CPU.
12. **Novelty unchanged:** N1 — Known Combination (H6 §8.6 equivalent).

The fix-verification lane must byte-confirm §10 against the body: every adaptation in §§3–5 appears here, and no row here introduces an undocumented design choice.

### FIX-3 — correct the read-site identity (Defect B)
Replace:
- §0 item 4: "at the L20 read site" → "at the final-output logits read site"
- §0 item 5: "given L20's known 41/60 = 0.6833" → "given the archived final-output fidelity 41/60 = 0.6833 (the logit lens applied at hidden_states[24])"
- §1.1: "at the single L20 read site" → "at the single final-output read site"
- §3.2: "the L20 fidelity value is treated as an archived constant" → "the final-output fidelity value is an archived constant"
Add one sentence to §3.3 (verbatim): "The late window {16..24} contains the archived site (lens at L24 is the model's output logits), so the §3.2 consistency pin is a true byte-level identity check on the lens implementation."
The §0 item 5 arithmetic (other 8 late sites ≥ 0.6458) is unchanged — verified.

### FIX-4 — correct the H6 fence citation (Defect C)
§0(c): replace "H6 §8.5 barred a KILL/HELD being 'followed by a different layer'" with "H6 §4's 'No rescue runs' clause bars a HELD/KILL being 'followed by ... a different layer' as an unlicensed gate tweak". Keep the remainder of the paragraph unchanged.

---

## 4. Fix-verification checklist for the next lane
1. §6 table == FIX-1 verbatim; placeholder text gone.
2. §§7–10 exist == FIX-2 verbatim (epistemological labels preserved).
3. FIX-3 replacements complete (grep for remaining "L20" — the only permitted L20 mentions are in §3.3's option-embedding history reference and the new §3.3 sentence; none may describe EXP112's readout).
4. FIX-4 citation corrected; no remaining "§8.5".
5. §10 complete vs body (§§3–5) — no undocumented adaptation, no extra design choice.
6. No other line changed (byte-diff against this review's snapshot).

Lane boundaries held: no protocol edited, no execution, no self-review. Review complete.
