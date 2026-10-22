# Law #14 Independent Review — EXP133 Amendment D (hook-delivery correction + readout-sensitivity positive control)

**Lane:** independent Law #14 reviewer. **LOG-4812** (CEO pre-assigned). **Date:** 2026-09-30.
**$0 CPU, paper only.** Read-only on signed protocols, weights, and artifacts. No model runs,
no GPU contact, no commits, no pushes, no spend, no publish, no dispatch, no experiment
number minted, no execution licensed.

**Artifact reviewed (exact version):**
`~/workspace/SCBI/research/prereg/EXP133_AMENDMENT_D_2026-09-30.md` — DRAFT amendment
covering ONLY (i) the `prepend=True` injection-hook registration correction and
(ii) ONE new breaking point (h): a readout-sensitivity positive control.

**Review-only fence:** I did not diagnose the hook or author the amendment. I edit nothing
under review, apply no repairs, license nothing, advance no pipeline. My only writes are
this review file and the single LOG-4812 research-log entry.

**Independence confirmed.** The amendment was authored by the LOG-4811 diagnosis lane; the
signed pre-reg by the LOG-4790 strategy worker; the REJECT (LOG-4808) and re-examination
(LOG-4809) by separate independent lanes. I authored none of them.

---

## §0 — Context verified

- LOG-4808 (independent Law #14 review): REJECT of EXP133's KILL — the `layers[19]`
  injection hook does not modify `hidden_states[20]` (SITE) under transformers 5.17.0;
  reproduced twice empirically (hook fires, |delta|=16.08; hs[20] diff = 0.0
  bit-identical; hs[21]/hs[24]/logits move). Correct category: RUN-INVALID (apparatus
  defect); hypothesis UNTESTED. Records hash
  `5078f518bf21cd82c4e194711f35b212e1d64946c7013381e648461b0388442e` verified.
- LOG-4809: EXP131 implicated and confirmed blind (byte-identical hook, blind-tap
  replication, `median_r = 1.0` = 0/0 → 1.0 signature).
- LOG-4810 (CEO decision): EXP131's binding KILL re-categorized RUN-INVALID; TGA
  injection hypothesis UNTESTED; path forward = fix the hook + positive control →
  independent review of Amendment D → re-execute EXP133 on CPU.
- LOG-4811: mechanism diagnosis + Amendment D draft (paper only, plus a one-prompt
  delivery probe: OLD append-order → tap diff 0.0 blind; NEW `prepend=True` →
  ‖tap_inj − tap_base‖ = 16.08 = ‖δ‖ exactly, max|tap_inj − tap_base − δ| = 3.58e-07).
- The signed pre-reg (`EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md`, LOG-4798, as
  amended by B/C) §0–§4, §3.6 (readout = `hidden_states[SITE]`, SITE = 20) and the
  decision table were read verbatim. Amendment D's §4 everything-unchanged list is
  complete and accurate against that document.

---

## §1 — Checklist findings

**1. Mechanism — PASS (independently verified against the installed source).**
I did not take the draft's account on authority; I read transformers 5.17.0's source
directly (the same installed version the executor runs):
- `GPTNeoXModel.forward` is decorated with `@capture_outputs`
  (`modeling_gpt_neox.py:321`) ✓ — the draft's claim.
- `_can_record_outputs = {"hidden_states": GPTNeoXLayer, "attentions": GPTNeoXAttention}`
  (`modeling_gpt_neox.py:297–300`) ✓ — one capture hook per `GPTNeoXLayer`.
- `install_output_capuring_hook` calls `module.register_forward_hook(output_capturing_hook)`
  with **default append order** (`utils/output_capturing.py`) ✓.
- `output_capturing_hook` snapshots the `output` argument and **returns None** — it
  never modifies the value passed downstream ✓.
- Hooks are installed **lazily on the first forward that requests `output_hidden_states`**
  (`maybe_install_capturing_hooks` inside the `capture_outputs` wrapper) ✓ — so the
  executor's base pass installs them before any injection hook is ever registered.
- PyTorch fires forward hooks in **registration order** (documented `register_forward_hook`
  semantics; `prepend=False` default) ✓.
- Hidden-state indexing: the first firing layer appends its input `args[0]`, then each
  layer appends its output — so `hidden_states[20]` = output of `layers[19]` ✓; the
  `tie_last_hidden_states` rewrite touches only `hidden_states[-1]`, not SITE=20 ✓.

Consequence, verified end-to-end: during injection forwards the chain on `layers[19]`
is `[capture_hook, injection_hook]`; the capture hook snapshots the **pre-injection**
block-19 output while the injection hook's modified return propagates downstream
unchanged (capture returns None). The tap is blind while `hidden_states[21]+` move —
exactly the LOG-4808/4809 observation. The draft's §1 mechanism account is correct and
sufficient; no alternative mechanism is needed, and the LOG-4811 probe (OLD blind /
NEW delivers) closes the loop empirically. **The mechanism is independently
corroborated, not merely plausible.**

**2. The fix is narrow and correct — PASS.** `prepend=True` (documented torch semantics:
"the hook will be fired before all existing forward hooks on this module") reorders
the chain to `[injection_hook, capture_hook]`, so the capture hook snapshots the
post-injection output. Two consequences follow and both are load-bearing:
- The ONLY thing that changes is the snapshot content. Because the capture hook
  returns None, downstream propagation is byte-identical under either ordering — the
  fix cannot alter any downstream state, any arm's model-visible behavior, or any
  record except what the tap snapshots. This is the narrowest possible repair.
- The hook site (`layers[19]`), the readout line (`out.hidden_states[SITE]`), the dose
  B, and the tap-space walk geometry are all textually/exactly preserved.

**3. Rejected-alternative analysis — PASS (sound).** Moving the hook to `layers[18]`
with `prepend=True` would make `hidden_states[20]` move, but the tap displacement
would be `f_19(x_18 + δ) − f_19(x_18)` — the block-19 nonlinear image of δ, not δ.
The signed protocol's geodesic walk, the norm budget B, and the ĉ_geo analysis are
all registered **in tap space**; the walk's δ_k are state-space displacements at
`x_{20,last}`. Injecting one block earlier breaks the correspondence between the
computed walk and the delivered intervention — a genuine science change, correctly
rejected as non-narrow.

**4. Breaking point (h) calibration — PASS.** The band `r ∈ [0.99, 1.01]` is genuinely
supported:
- The LOG-4811 probe measured `r = 1.0000000` under working delivery and `r = 0.0`
  (bit-identical) under blind delivery. The blind value is infinitely far from the
  band — the LOG-4808 defect trips it deterministically, not probabilistically.
- The band is ~100× wider than the measured working deviation (float32 rounding
  ~2e-8 relative), so a correct apparatus passes with wide margin. It cannot
  false-positive-void a working apparatus: the hook does pure addition
  (`o[:, -1, :] += δ`) and the snapshot follows the injection hook directly, so the
  ratio is 1.0 to float32 precision by construction.
- One prompt suffices: the defect is deterministic (hook order is global, not
  prompt-dependent) — blind on one prompt ⟹ blind on all (LOG-4808 showed 0.0 on all
  10 prompts × 6 arms).
- Conventions consistent: fixed seed (`20260930`, a new seed — no collision with the
  `20260929_4714` v2 seed or the bench seed stream), probe norm 16.0 (arbitrary; `r`
  normalizes it away — the draft correctly notes δ_probe is a control, not a dose,
  and it is discarded from all arms and records), exit 44 (the established
  apparatus-void exit), runs after the base pass and before the first injection
  forward with zero decision forwards executed (Law #9 ordering). No extra base
  forward is needed (`tap_base` = already-recorded `base_states[0]`) — $0 additional
  cost beyond the one control forward.

**5. Decision-table integrity — PASS.** Amendment D's §4 leaves the signed §2 table,
the KILL-first precedence, the PIVOT/INCONCLUSIVE corners, and the ĉ_geo gate
byte-identical in effect. Breaking point (h) gates run/no-run only. **Law #4 clean:**
the control uses a fixed-seed random vector on a frozen eval-mode model and is
discarded — it contains no hypothesis content and cannot bias KILL, CONTINUE, PIVOT,
or INCONCLUSIVE. A trip voids the run before any decision forward exists to bias.

**6. EXP131 spillover — PASS (fenced).** Amendment D §4 explicitly states it "covers
EXP133 only; EXP131's disposition (re-run vs subsume) is a separate CEO decision."
Nothing in the operative changes constrains EXP131. The §5 checklist addition is
forward-looking lane guidance ("injection lanes must prove delivery"), which is the
correct systemic fix and does not pre-judge EXP131's disposition. No implicit
re-opening, no constraint smuggled in.

**7. Status honesty — PASS.** "DRAFT — licenses nothing" at the top; the draft states
it licenses no execution and no executor edit, and that the executor repair and
re-execution require independent review of this amendment + fresh CEO clearance. No
hidden licensing language. The $0-CPU scope note correctly fences the one-prompt
probe as an observation, not experimental data.

**Laws #2/#3/#9 — CLEAN.** Every number is cited to LOG-4808/4809/4811 or the
installed source; no invented results; no metric changes; the control sits in the
breaking-point layer of the Law-#9 ordering. Law #11 labeling in the draft is honest
([FACT]/[OBSERVATION]/[INTERPRETATION] used correctly throughout).

---

## §2 — Verdict

**SIGN.** The mechanism is independently verified against the installed library source,
the fix is the provably-narrowest repair (one keyword; snapshot-only effect;
downstream byte-identical), the rejected alternative is correctly identified as a
science change, the positive control is calibrated against measured working/blind
values with margins that cannot false-void, the decision table and dose fence are
untouched, and EXP131's disposition is properly fenced off. No blocking findings.

**Advisory (non-blocking):** the draft's §1 labels "in transformers ≤5.0 the hidden
states were collected inline in the model forward after hook application" as [FACT].
I verified 5.17.0's behavior from the installed source but could not verify the ≤5.0
claim against a 5.0 installation (not present here). It is narrative color, not
load-bearing — the tap semantics that matter are established by the 5.17.0 source
plus the delivery probe — but under Law #11 it should be verified against 5.0
source or softened to [INTERPRETATION] before the amendment is signed.

**Disposition:** Amendment D approved as drafted (with the §1 advisory noted). EXP133
may re-execute under the signed pre-reg as amended by Amendments B, C, and D, upon
fresh CEO clearance. The executor repair is confined to the `prepend=True` keyword
plus the §3 positive control, exactly as drafted.
