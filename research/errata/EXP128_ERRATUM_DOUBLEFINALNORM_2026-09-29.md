# Erratum — EXP128: double-final-LayerNorm readout defect

**Experiment:** EXP128 (DSF sensitivity field). **Verdict category:** RUN-INVALID;
DSF soft-spot premise UNTESTED (bound LOG-4706, reviewed LOG-4707). **Verdict
impact of this erratum:** NONE — the category stands.

**Erratum lane:** LOG-4747 (pre-assigned). **Finding source:** independent
apparatus audit during the EXP132 execution review (LOG-4744); finding also
recorded there as FIX-5. **Status:** append-only; this document does not modify
the signed EXP128 report (`research/experiments/EXP128_DSF_SENSITIVITYFIELD_REPORT_2026-09-29.md`)
or the signed EXP128 protocol.

---

## 1. The defect

EXP128's executor (`run_exp128.py`, `base_forward` / `perturbed_forward`) applies
`model.gpt_neox.final_layer_norm` to `hidden_states[24]`.

In transformers 5.17.0, `hidden_states` has 25 entries: `hs[0]` = embeddings,
`hs[k]` = block-(k−1) output for 1 ≤ k ≤ 23, and **`hs[24]` is already
post-final-LayerNorm** (relative error 0.0 vs the model's `last_hidden_state`;
independently verified in the LOG-4744 audit). The raw block-23 output is absent
from the returned list.

The executor therefore normalizes an already-normalized tensor. The double
application deviates from the correct single-norm readout by **relative norm
0.165** (independently measured in the LOG-4744 audit). EXP128's linearity
diagnostic measured the **wrong construct** (a double-normalized readout), not
the registered object `x_{24,last}`.

## 2. How it was found

During the independent Law #14 review of the EXP132 execution (LOG-4744), the
reviewer performed a read-only apparatus audit with independent recomputation
on the pinned weights. The audit:

- reproduced the transformers 5.17.0 `hidden_states` layout (25 entries;
  `hs[24]` = post-final-LN) at relative error 0.0;
- measured the double-application deviation (rel norm 0.165);
- ruled the causal-mask concern a phantom (explicit mask+positions+rotary
  reproduces the default path at rel error 0.0);
- confirmed EXP132's own readout (`make_g`, exactly one final LayerNorm) is
  correct — EXP132's executor had already flagged the double-norm pattern as a
  latent bug.

(Rotary-embedding audit numbers: rel diff 0.98 at layer-0 attention, 0.062 at
readout — the pre-fix smoke numbers were void; this audit is the basis of the
layout finding.)

## 3. Verdict impact: none

EXP128's verdict category is **unchanged: RUN-INVALID; DSF UNTESTED.**

Law #9 stopped the run before the verdict-bar read: the linearity check
(1/12 within 25%, bar 10/12) failed first, and no metric was ever read from
any construct, wrong or right. The verdict is therefore unaffected.

However, the report's substantive linearity numbers — "1/12 within 25%" and the
"amplification-driven transition saturation" interpretation — are **void as
measurements of the registered object `x_{24,last}`**. They describe the
double-normalized construct. This erratum corrects the record of WHAT was
measured, not the verdict.

## 4. Implications for future work

- Any re-analysis of EXP128's linearity data must use the corrected
  single-norm readout; the committed numbers cannot be re-interpreted as
  evidence about `x_{24,last}`.
- The defect deepens the apparatus-void story: the linearity diagnostic
  failed even on a doubly-normalized construct — the failure was not an
  artifact of the correct readout being harder to measure.
- No future experiment may reuse EXP128's `base_forward`/`perturbed_forward`
  readout recipe without correcting the normalization; any DSF-family return
  must pass a fresh gate with the corrected readout registered.

## 5. Provenance

This erratum is append-only and was written in a dedicated lane (LOG-4747).
It does not edit the signed EXP128 report, the signed EXP128 pre-registration,
or the EXP128 protocol. The EXP128 verdict category (RUN-INVALID / DSF
UNTESTED) stands as bound.

*Erratum written 2026-09-29/30. Finding: LOG-4744 (independent EXP132
execution review). Lane: LOG-4747.*
