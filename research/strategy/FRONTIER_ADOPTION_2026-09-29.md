# Frontier Technique-Adoption Memo — 2026-09-29

**Lane:** LOG-4528 (pre-assigned). $0 CPU only; read-only on repo; no protocol, paper, weight, GPU, push, or spend actions taken.
**Source:** `~/workspace/goals/scbi-research-program/hidden_files/frontier_sweep_log.md`, 2026-09-29 block (arXiv:2609.06473, verified via arxiv.org; AutoTrust JEV-27B, PRNewswire via CNA/Morningstar — benchmark numbers vendor-claimed, UNVERIFIED).
**Method:** adoption analysis only. Nothing below modifies any existing file; all "changes" are recommendations for named future artifacts.

---

## Finding 1 — arXiv:2609.06473, "Steering Under Compression" (Bhandari & Wade)

**What exactly we steal (three concrete procedures, not vibes):**
1. **Matched-geometry collinearity gate.** For any claim of the form "steering survives X transformation," require: extract the steering direction under the transformation (e.g., INT8 replica), compute cosine against the reference-model (FP16) direction, and gate on a pre-registered threshold (their measured band: 0.989–0.998 INT8, 0.945–0.990 NF4). A claimed effect without a collinearity gate is unpublishable in our pipeline.
2. **Censored iso-effect dose ladder.** Fit the dose–response curve (effect vs steering coefficient) with censoring, and pre-register tests for *discontinuous* failure modes: their reasoning-length result shows lengthening is graded-then-cap-runaway while shortening is a 12–30% step-function collapse. Our steering arms currently record ΔM at fixed α; we must record the curve shape, not the point.
3. **Baseline-shift attribution.** Compression can dominate the intervention (their Mistral-NF4 GSM8K baseline 0.545→0.365 at α=0). Any future quantized-replica claim must report the α=0 baseline shift separately from the steering delta — we do not currently separate these two numbers in one check.

**What would change (named files/sections — NOT changed by this lane):**
- `falsification_kit/core/` + `falsification_kit/tier0.py`: add a quantization-collinearity gate to the degeneracy/control battery (fails the battery if a transformation claim lacks the cosine gate).
- `falsification_kit/battery.py`: add the iso-effect ladder shape test (graded vs step-function vs cap-runaway classification) alongside the existing ΔM battery.
- Future EXP steering pre-registrations (e.g., successors to S4-9 `research/innovation/S4-9_PREREG_DRAFT_2026-09-27.md`, which already carries matched-geometry random-direction controls): extend the control section with the collinearity gate and dose-ladder; adopt their pre-registered-equivalence framing (pooled contrast −0.010, 90% CI [−0.026, +0.007] on sentiment/INT8).
- `experiments/protocols/EXP083_RCPA_PREREG_SPEC.md`: its control section is the template — future lanes should mirror its matched-geometry discipline plus the new ladder.

**New falsification this enables (impossible today):** today we cannot distinguish "quantization broke the direction" from "quantization broke the economics." With the gate + ladder, a future claim "steering X survives INT8" becomes killable in two new ways: (a) collinearity gate failure (geometry changed — direction is not preserved), (b) baseline-shift dominance (α=0 moves more than any α>0 — the intervention is epiphenomenal). Neither check exists in our kit.

**Cost and license:** the discipline itself is $0 CPU (kit/battery code + pre-reg text). Actually *running* quantized-replica verification is GPU-gated (INT8 replicas of Pythia-410m on CPU are out of budget; NF4 needs accelerator). License: adopt the protocol language now; execution gates on founder GPU unlock.

**Verdict: ADOPT-WITH-CONDITIONS.** Adopt the collinearity gate + iso-effect ladder + baseline-shift separation as mandatory pre-registration and kit language for all future steering-under-transformation claims. Condition: no re-verification of our closed steering lines is licensed — S4/S5/S6/I2′ verdicts stand on FP32 arms; applying this retroactively would be busywork, and their verdicts (zero flips) are transformation-invariant anyway.

---

## Finding 2 — AutoTrust JEV-27B (frozen Qwen3.8-27B + 108.9M-param decision head)

**What exactly we steal (one concrete procedure):**
1. **Block-off byte-identical falsifiability discipline.** When a module is attached to a frozen backbone and then switched OFF, the outputs must be byte-identical to the base model (their bar: all 164 HumanEval completions byte-identical with the decision block off). Any future head-attach experiment of ours (output-side mechanisms, K3 Phase-1, bridge successors like EXP075-family) must include a disable switch and a byte-identical reproduction check against the backbone pin before any capability claim is made. This is a falsification gate, not a capability claim: fail the byte-identical check ⇒ the "frozen backbone" premise is dead and every downstream number is void.

**What would change (named files/sections — NOT changed by this lane):**
- `falsification_kit/tier0.py`: add a module-off invariance degeneracy test (attach → disable → byte-diff against the pinned backbone output; any difference = tier-0 kill of the "frozen" premise).
- Future head-attach pre-registrations (`research/CANDIDATE_BACKLOG.md` rows for K3 Phase-1 and any head-design candidates): add a "disable-switch clause" in the falsification decision tree — first branch is always the byte-identical check.
- `research/strategy/GPU_QUEUE_READINESS_2026-09-29.md` (future revisions): note that launch-licensed head experiments must carry the discipline in their pre-reg before execution.

**New falsification this enables (impossible today):** today we have no standard check separating "the head genuinely contributed" from "the backbone drifted during attachment." With the discipline, a future positive claim from a head experiment becomes killable at tier 0: if disabling the module does not restore byte-identical base behavior, the experiment dies before any benchmark is run. This closes the exact loophole class that killed our QK-subspace theorem (LOG-137-era: mechanism claims outrunning premise verification).

**Cost and license:** the discipline is $0 CPU (protocol language + kit test). Training or running a real decision head (their cost: ~9.2 B200-hours) is GPU-gated and founder-gated; no such lane is licensed. Additionally: the 84.07% mean benchmark number is UNVERIFIED (vendor-claimed) — we adopt the *discipline*, never the *number*. No claim about JEV-27B itself enters our ledger.

**Verdict: ADOPT-WITH-CONDITIONS.** Adopt the block-off byte-identical discipline as mandatory for all future frozen-backbone + attached-module experiments. Conditions: (a) withhold any verdict on JEV-27B itself until independent replication; (b) do not use JEV-27B as evidence for any of our claims — it is architecture-convergence context only (second Δθ=0 frozen-backbone + output-side head in 10 days after CLM-8B, which our EXP077 boundary finding predicts: the transferable direction lives output-side).

---

## Threat assessment against published v84 claims

**No threat from either finding — explicit statement.**

- arXiv:2609.06473 does not touch v84's claims. v84 claims: static activation directions decode at 6.7× chance with zero causal transfer (Decodability Gap), per-item L11 static geometry is inert, bridges are label-informed rescue controls, the QK-subspace theorem is retracted. All v84 steering evidence was collected on FP32 Pythia-410m; the compression paper studies whether steering *survives* quantization — a transformation our verdicts never cross. If anything, it strengthens v84: its falsificationist discipline (collinearity gates, censored dose ladders) is exactly the kind of control rigor v84's boundary science is built on.
- JEV-27B does not touch v84's claims. v84 makes no claim about trained decision heads; its boundary claims concern *static* steering of a frozen model. JEV-27B is a *trained* output-side head — precisely the "output side is where things live" architecture that EXP077 points at. Convergence with our boundary map, not contradiction. Its benchmark numbers are vendor-claimed and unverified; nothing in v84 leans on them.
- Note on related context (not a v84 threat): the Simula steering-grid paper (Sep 26 sweep) and SPS state-conditioned steering (Sep 27 sweep) study *conditional* steering. v84 never claimed conditional/adaptive steering fails — only static per-item geometry at L11. The K2/EXP083/084 line is our conditional-geometry bet and remains licensed, not threatened.

## Top adoption item

The single highest-value adoption: **add both disciplines to the falsification kit as tier-0 gates** — (1) the matched-geometry collinearity + censored iso-effect ladder for any steering-under-transformation claim, and (2) the block-off byte-identical invariance test for any frozen-backbone + attached-module claim. Both are $0 CPU to write as protocol language; both turn currently-unfalsifiable claim shapes into killable ones. This lane changes nothing; it proposes them for the kit's next repair/extension wave.

---

**Scope compliance:** no signed protocol modified; v82/v83/v84 sources untouched; no weights; no GPU contact; no push; no spend; no follow-up lanes dispatched. Boundary held.
