# Amendment DRAFT D: Hook-delivery correction + readout-sensitivity positive control (EXP133)

**Lane:** LOG-4811 (CEO pre-assigned). **Status: DRAFT — licenses nothing.** This is a narrow
amendment draft to the CEO-SIGNED pre-reg
`research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md` (signed LOG-4798, as amended
by Amendment B, Law #14 SIGN LOG-4801, and Amendment C, Law #14 SIGN LOG-4805). It amends
ONLY (i) the injection-hook registration in the executor (one keyword argument) and
(ii) adds ONE new breaking point — a readout-sensitivity positive control. It licenses no
execution and no executor edit; the executor repair and EXP133 re-execution require
independent review of this amendment + fresh CEO clearance.

**$0 CPU scope for this draft.** Paper only — except the one-prompt delivery probe cited
in §2 (no experimental data collected; probe script `/tmp/hookfix_probe.py`, ephemeral).

---

## §1 — What broke and why [FACT]

LOG-4808 (Law #14 REJECT) and LOG-4809 (independent replication) proved the injection
never reached the readout: with the executor's hook on `layers[19]`, `hidden_states[20]`
(the registered SITE/tap) is **bit-identical** with and without injection, while
`hidden_states[21]`, `hidden_states[24]` and the logits all move. EXP133's KILL and
EXP131's KILL are both RUN-INVALID (apparatus defect); both hypotheses are UNTESTED
(LOG-4810).

**Mechanism [FACT]** — verified by code reading against the installed transformers
5.17.0 (not by analogy):

1. In transformers 5.x, `GPTNeoXModel.forward` is decorated with `@capture_outputs`.
   Its `_can_record_outputs = {"hidden_states": GPTNeoXLayer, ...}` installs, on the
   **first** forward that requests `output_hidden_states=True`, one forward hook per
   `GPTNeoXLayer` that **snapshots the layer's return value** into the
   `hidden_states` tuple (`install_output_capuring_hook` in
   `transformers/utils/output_capturing.py`; `hidden_states[i]` = snapshot of
   `layers[i-1]`'s returned output, `hidden_states[0]` = input embeddings).
2. The executor's **base pass** (`run_exp133.py` line 305,
   `model(..., output_hidden_states=True)`, no injection hook) runs **before** the
   first injection forward (line 629). The capture hooks are therefore installed
   **before** any injection hook is ever registered.
3. PyTorch fires forward hooks in **registration order**
   (`register_forward_hook(hook, *, prepend=False)` default). During injection
   forwards the hook chain on `layers[19]` is
   `[capture_hook, injection_hook]`: the capture hook snapshots the **pre-injection**
   output of block 19, and only then does the injection hook's modified return value
   propagate downstream. Hence `hidden_states[20]` is blind while `hidden_states[21]+`
   move.
4. In transformers ≤5.0 the hidden states were collected **inline** in the model
   forward **after** hook application [INTERPRETATION — 5.0 source not installed
   here; narrative color, not load-bearing: tap semantics under 5.17.0 are
   established independently from the 5.17.0 source and the delivery probe],
   so the hook-modified value was captured and the tap saw the injection. The
   5.0.0 → 5.17.0 upgrade (done to restore the LOG-331 weights pin) changed
   capture from post-hook to pre-hook [FACT — verified from 5.17.0 source] —
   a library-version migration shifting activation-capture semantics with no
   guard observing it.

**Defect class [INTERPRETATION]:** intervention delivered to the wrong point in the
hook chain — the defect class LOG-4808 §2 named. No breaking point observed
intervention delivery to the readout tap; §3 below closes that gap.

## §2 — Corrected delivery: old vs new

**OLD** (`run_exp133.py` line 626, byte-identical in EXP131's executor):
```python
h_inj = layers[19].register_forward_hook(hook_fn)  # input of block 20
```
Hook site `layers[19]`, append order → fires **after** the `@capture_outputs`
snapshot hook → `hidden_states[20]` records the pre-injection block-19 output (blind).

**NEW:**
```python
h_inj = layers[19].register_forward_hook(hook_fn, prepend=True)  # input of block 20; prepend: fire before the @capture_outputs snapshot hook
```
Hook site **unchanged** (`layers[19]`); `prepend=True` (documented torch semantics:
"the provided hook will be fired before all existing forward hooks on this module")
puts the injection hook **first** in the chain. The capture hook then snapshots the
post-injection output, restoring exactly the ≤5.0 tap semantics the signed protocol
assumed: tap = block-19 output with δ applied = the state block 20 reads. The readout
line (`out.hidden_states[SITE]`) is textually unchanged.

**Rejected alternative [INTERPRETATION]:** moving the hook to `layers[18]` would make
`hidden_states[20]` move, but the delivered tap displacement would be
`f_19(x_18 + δ) − f_19(x_18)` — the block-19 image of δ — not δ. The geodesic walk,
the norm budget B, and the ĉ_geo analysis are all registered **in tap space**; injecting
one block earlier breaks the correspondence between the computed walk and the delivered
intervention. That is a science change, not a narrow repair. `prepend=True` keeps the
site, the tap, the dose, and the walk geometry exactly as licensed.

**Delivery probe [OBSERVATION]** — one prompt, CPU, transformers 5.17.0,
torch 2.14.0+cpu, Pythia-410m float32, executor byte-identical hook
(`o = outp.clone(); o[:, -1, :] = o[:, -1, :] + δ`), |δ| = 16.08:

| arm | hook fired | max\|tap_inj − tap_base\| | ‖tap_inj − tap_base‖ | max\|tap_inj − tap_base − δ\| |
|---|---|---|---|---|
| OLD (append) | yes | **0.0 (bit-identical)** | 0.0 | — |
| NEW (prepend=True) | yes | 1.8029 | **16.0800 = ‖δ‖** | 3.58e-07 (float32 rounding only) |

Downstream states (`hidden_states[21]`) move in both arms, confirming the hook fires
either way. The NEW arm delivers δ to the tap with displacement norm equal to ‖δ‖ to
float32 precision; the OLD arm reproduces the LOG-4808/4809 blind tap exactly.

## §3 — New breaking point (h): readout-sensitivity positive control

**Statement.** After the base pass and **before the first injection forward**, the
executor runs a delivery positive control on the first bench prompt's `input_ids`:

1. `tap_base` = the already-recorded base state `base_states[0]` (no extra forward).
2. Register the corrected hook (`prepend=True`) with a **fixed-seed** random probe
   vector δ_probe, seed `20260930`, scaled to **‖δ_probe‖ = 16.0** (float32, run device).
3. One forward with `output_hidden_states=True`; `tap_inj = hidden_states[SITE][0,-1,:]`.
4. Compute `r = ‖tap_inj − tap_base‖ / ‖δ_probe‖`. **Assert `r ∈ [0.99, 1.01]`**;
   miss → `apparatus-void: readout-sensitivity positive control failed`, exit 44,
   zero decision forwards executed.

**Calibration [OBSERVATION]:** the §2 probe measured `r = 1.0000000` under working
delivery and `r = 0.0` (bit-identical) under blind delivery. The `[0.99, 1.01]` band
is ~100× wider than the measured working deviation (float32 rounding ~2e-8 relative)
and infinitely far from the blind value — a correct apparatus passes with wide margin;
the LOG-4808 defect trips it deterministically. The 16.0 probe norm (~32× the dose B)
makes the movement unambiguous; δ_probe is a control, not a dose, and is discarded
(it appears in no arm and no record).

**Law #4 clean [INTERPRETATION]:** the control uses only the readout tap and a random
vector — it contains no hypothesis content and cannot bias any §2 verdict branch. It
gates run/no-run only.

## §4 — Everything else unchanged

The hypothesis (§1), the decision table (§2), the budget B and its verbatim Law #2
discipline, breaking points (a), (b) as amended by Amendment B, (c), (d) as amended by
Amendment C, (e), (f), (g), the arms (§3.5), the readout definition
(`hidden_states[SITE]`, §3.6 — textually unchanged; §2 restores its assumed semantics),
the geodesic-walk construction, the ĉ_geo definition, and the records discipline (§3.8)
are all untouched. The **only** executor change licensed by this amendment is the
`prepend=True` keyword in `inject_forward` (plus the §3 control). No science changes;
no new quantities; no re-interpretation of any prior verdict. This amendment covers
EXP133 only; EXP131's disposition (re-run vs subsume) is a separate CEO decision.

## §5 — Law #14 review-checklist addition

Append to the checklist:

> **Injection lanes must prove delivery to the readout tap on the installed library
> version.** Every injection experiment registers a readout-sensitivity positive
> control as a breaking point (large random injection → tap moves by the calibrated
> amount; miss → apparatus-void before any decision forward). Hook registration order
> relative to library-installed capture hooks must be verified by code reading on the
> installed version, not assumed from an older one. Any library-version migration
> (transformers or torch) re-opens activation-indexing and capture-order verification
> from scratch — the 5.0 → 5.17 `@capture_outputs` shift survived two reviews, a
> fix-verification, and two amendments because no guard observed the tap.
