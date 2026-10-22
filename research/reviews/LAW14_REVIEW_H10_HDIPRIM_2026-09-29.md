# Independent Law #14 Review — H10 (HDI-PRIM) Pre-registration (2026-09-29)

**Artifact reviewed:** `research/prereg/EXP_PREREG_H10_HDIPRIM_2026-09-29.md` (drafting lane LOG-4600)
**Reviewer:** independent Law #14 lane (LOG-4601). Independent of the drafting lane. No protocol edited by this lane; no execution dispatched.
**Verdict: SIGN** — launch-eligible as drafted. No fixes required.

---

## 1. Bars/numbers — independently recomputed from first principles [FACT]

All six §4 binomial claims recomputed exactly (n=60):

| Claim | Draft | Independent recomputation | Match |
|---|---|---|---|
| P(X ≥ 59 \| 60, 0.98) | 0.6619 | 0.6619 | ✓ |
| P(X ≥ 42 \| 60, 0.5) | 0.0013 | 0.0013 | ✓ |
| P(X ≤ 57 \| 60, 0.99) | 0.0224 | 0.0224 | ✓ |
| P(X ≥ 41 \| 60, 0.5) | 0.0031 | 0.0031 | ✓ |
| P(X ≥ 33 \| 60, 0.5) | 0.2595 | 0.2595 | ✓ |
| P(X ≤ 22 \| 60, 0.5) | 0.0259 | 0.0259 | ✓ |

Fractions (34/60=0.5667, 41/60=0.6833, 42/60=0.70, 57/60=0.95, 58/60=0.9667, 59/60=0.9833, 33/60=0.55) all correct. Region tiling [0,33] ∪ [34,41] ∪ [42,57] ∪ {58} ∪ [59,60] = [0,60]: **no gaps, no overlaps**. §0's worth-it-gate summary matches the §4 table exactly. The statistical logic of each region is sound (e.g., ≥59/60 fails to reject near-perfection — correctly read as no-gap KILL; the ≤57-side check correctly establishes the gap below perfection).

## 2. Pathology blocking — holds by construction [FACT + interpretation]

EXP115's pathology (38/60 recitation) required three complete exemplar blocks ending `"Answer: <entity>"` — the model pattern-matched and continued the document macro-structure. The H10 §3.3 template contains exactly one block (target premise + question + unfinished copula sentence), zero exemplars, no `"Answer: <entity>"` blocks to recite. The only `"Premise:"` in the prompt is the target's own — the draft's §3.3 claim is accurate. The specific EXP115 pathology is **structurally impossible in this protocol** — not mitigated, eliminated. The draft's residual-risk disclosure (a *different* off-track mode, e.g. premise restart, absorbed by G1/G2 as RUN-INVALID) is the honest boundary of this claim. H7's documented rationale ("ending mid-sentence forces continuation instead of a fresh generation restart") is quoted verbatim and supports the design.

## 3. Deviation completeness — §9's 8 items are genuine and complete [FACT]

All 8 §9 items are real differences from H7's T1-P5 spec (tail `"The single-letter answer is:"` → `"The entity higher in rank is:"` verified against the H7 pre-reg; max_new_tokens 4 → 8 verified; archived decision arm; n 57 → 60; gates; constancy disclosure; pathology analysis; P2 → P5 family change). The completeness sweep (the lesson of the H9 review) finds **no ninth undocumented adaptation**: the parse rule, greedy decoding, seeds, re-parse ×2, exception handling, and backbone pins match their claimed sources exactly. The only unlisted difference — the EXP107 bench/question carrier vs H7's EXP089 bench — is the hypothesis's documented domain (stated in §0, §2, §3.1, and pinned in §5), not a hidden adaptation of the P5 mechanism. One documentation note (non-binding): §3.3's "only the tail noun phrase changes from the single-letter shape to the entity-name shape" refers to the priming tail, with the carrier documented separately — this is accurate as written.

## 4. Archived EXP112 decision arm — provenance sound [FACT]

- `experiments/runs/EXP112_hdildr/out/exp112_per_item.json` exists, 60 records.
- sha256 **independently recomputed by this lane**: `f8133f1f4dc6f302cb7fdbe4dee248f9eb5ab97afab00c7fbc7b331e1a804625` — byte-identical to the pre-reg's pin, which matches H9's independently computed pin and the EXP115 report's observed value.
- The bench was rebuilt by this lane (`build_bench()`, deterministic, no RNG): 60 items, sha256 `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5` — matches the pin.
- Ground-truth constancy verified from the bench builder: `tuple[0]` (A) is the outranker in every premise, and `flip_premise` is meaning-preserving — the correct answer is indeed always tuple[0]. The disclosure (§3.1, item 7) is correct.

## 5. Worth-it gate — PASS stands [INTERPRETATION]

H10 is a genuinely different experiment from H9: same generation-level question, but the *other* EXP113-cleared protocol — the exact pre-registered contingency (H7-CONTINUE's registered consequence, restated in H9 §4 and EXP115's report). It does not re-run P2, does not rescue H9's RUN-INVALID, and does not revive H1's unvalidated protocol. The recitation risk is structurally removed (item 2 above); the cheapest test (60 generations + archived decisions) is correct; both failure branches (gate fires → RUN-INVALID; signal absent → KILL) are informative.

## 6. Law compliance [FACT]

- **Law #4:** bars binding; post-hoc rewording explicitly BARRED in §4 ("scientific misconduct, not a verdict"). No rescue runs licensed.
- **Law #7:** priming shows no exemplars/labels; labels never used (not in metric — fidelity vs the archived decision statistic, not labels); no exemplar exclusion needed, and n=60 is correctly justified.
- **Law #9:** gates (G1/G2) fire before any metric; fidelity formula and bars registered before any run.
- **Law #13:** seeds (torch=numpy=0), environment manifest (torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, accelerate fallback), all three pins (bench, archive, LOG-331 backbone before/after), byte-exact template.
- Law #10 (N1 — Known Combination): stated; Law #6 (Δθ=0): backbone pin before/after, mismatch → RUN-INVALID, quarantine.

## 7. Falsification tree — complete [FACT]

Every branch terminates: HALT (bench/archive drift), RUN-INVALID (backbone mismatch, G1, G2, re-parse mismatch), KILL (≥59/60 no gap; ≤33/60 no signal), HELD (58/60, 34–41/60), CONTINUE (42–57/60). No dead ends, no unregistered re-runs, no post-hoc bars. "No rescue runs" (§4) correctly forbids gate tweaks after a HELD/KILL.

---

## Verdict: SIGN

The pre-registration is mathematically exact, honestly gated, law-compliant, and launch-eligible as drafted. This lane required no fixes. The CEO launch decision and execution are separate later lanes.
