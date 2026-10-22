# Law #14 Fix-Verification — H2 (QBR) Pre-registration

**Verification lane:** LOG-4556 (pre-assigned). **Date:** 2026-09-29.
**Artifact under verification:** `research/prereg/EXP_PREREG_H2_QBR_2026-09-29.md`
**Review requiring fixes:** `research/reviews/LAW14_REVIEW_H2_QBR_2026-09-29.md` (independent Law #14, LOG-4554, verdict SIGN-WITH-FIXES, fixes F1 + F2).
**Repair lane:** LOG-4555 (claims both fixes applied). This verifier is independent of both the drafting and repair lanes.
**Scope:** the two fixes only, plus a spot-check that nothing else changed. This verification approves no execution, mints no experiment number, launches nothing.
**Method:** read-only. $0 CPU. No weights touched.

---

## Verdict: ALL-FIXES-VERIFIED

**The review is upgraded to SIGN on the exact filename** `EXP_PREREG_H2_QBR_2026-09-29.md`.

---

## Fix F1 — PASS

Required: one sentence requiring the execution worksheet to record the Law #13 environment manifest — exact torch and transformers versions and the CPU thread count the executor sets and reads back via `torch.get_num_threads()`.

Found (§3.3 step 1, line 58):

> "The execution worksheet must also record the Law #13 environment manifest: exact torch and transformers versions (reference worksheet pins `torch=2.14.0+cpu`, `transformers=5.17.0`) and the CPU thread count the executor sets and reads back via `torch.get_num_threads()` — compliance verifiable against the reference worksheet's existing `torch`/`transformers` keys by worksheet diff."

Reference values confirmed against the checked-in reference worksheet: `falsification_kit/reference/tier0_worksheet.json` carries `"torch": "2.14.0+cpu"` and `"transformers": "5.17.0"` — the cited reference values are accurate. The sentence is present, exact, and placed where the review required.

## Fix F2 — PASS

Required: one sentence requiring the execution worksheet to state the quantized-copy presentation mechanism (in-memory `state_dict` swap vs saved-to-local-directory used as `--model-id`).

Found (§3.3 step 2, line 59):

> "The execution worksheet must state the quantized-copy presentation mechanism — in-memory `state_dict` swap after model load, or saved-to-local-directory used as `--model-id` — since tier0.py loads by model-id from cache and §3.2's "disposable in-memory copy" pins the quantization target, not how the copy is presented to the runner."

Present, exact, and placed where the review required. It correctly preserves the execution lane's discretion over the mechanism itself while requiring the disclosure.

## Spot-check: structural elements unchanged — PASS

- Hypothesis (§1, line 13): present — "The EXP105 falsification-kit battery's binding verdict (KILL at step 9) reproduces under weight-only INT8 fake-quantization of the frozen backbone — i.e., the Decodability Gap boundary is precision-regime-robust at the binding-bar level."
- Exact question (§2, line 31): present and unchanged.
- Seven tiers T1–T7 (§3.3, lines 66–72): all present with per-tier Boolean reproduce criteria — TIER-0 PASSED / 0.5333, KILL, step 9, dM contrasts, b=5/c=0/p=0.0625, O=0.5714, n_pop=21 / median rank 4.0.
- Decision bars (§4, lines 83–84, 101–103): CERTIFIED / CERTIFIED-WITH-NOTE (6/7 with T1–T3 intact) / PIVOT (any structural flip or ≤5/7) — present, unchanged.
- PIVOT operational definition (§2, line 38): present — statement template, one bounded characterization lane, hard fences.
- Fences (§7.1, lines 117–125): present — simulation-scope certification, no closed-line re-opens, no capability claims.
- Fake-quant spec (§3.2, line 51): present — per-output-channel symmetric INT8, FP32 storage/compute, embeddings/biases/LayerNorm/activations FP32, no INT8 kernels.
- §1.1 license argument (lines 15–25): present — adversarial kill-invitation intact.
- Δθ=0 procedure (§3.2, line 53): present — LOG-331 pin `ec276abe...` verified before quantization, disposable in-memory copy, copy SHA recorded, tier0 pre/post hash assertion, copy discarded.

Per the LOG-4555 repair entry, only the two fix sentences were added; no other sections were reformatted or reworded. No additions, deletions, or shifts beyond F1 and F2 were observed.

## Boundary

This lane stops here. Execution under a minted experiment number and the CEO launch decision are separate later lanes — not this one.
