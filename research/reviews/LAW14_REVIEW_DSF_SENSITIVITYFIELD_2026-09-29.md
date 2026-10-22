# Independent Law #14 Review — DSF Pre-registration (EXP_PREREG_DSF_SENSITIVITYFIELD_2026-09-29.md)

**Lane:** LOG-4704 (pre-assigned). **$0 CPU.** Read-only on all signed
artifacts; this review and the LOG-4704 entry are the only writes.
Fresh eyes — the reviewer did not draft the protocol.

**Verdict: SIGN-WITH-FIXES** — the design is mathematically sound and
the hypothesis is falsifiable, but two specification defects are
launch-gating (an unexecutable Law #9 ordering and a dangling
section reference). Five further fixes are verdict-immaterial
precision/completeness items.

**Sources read before ruling:** the draft; the DSF gate memo
(LOG-4702, `research/strategy/DSF_GATE_2026-09-29.md`); the TGA
pre-registration (`EXP_PREREG_TGA_TRANSIENTGROWTH_2026-09-29.md`,
§3.3/§10); the research log (LOG-4698 EXP127 CONTINUE, LOG-4699
BIND-WITH-CAVEAT, LOG-4702/4703); EXP086 Stage-A record (LOG-331,
Henrici numbers); `~/workspace/SCBI/AGENTS.md` house rules.

---

## 1. Bars — coherent, disjoint, exhaustive ✓

The decision partition is complete over all attainable Gini values
(Gini ∈ [0, 1−1/24] for 24 nonnegative S_l):

| Gini | Top-3 | Decision |
|---|---|---|
| ≥ 0.4 | not all in {L21,L22,L23} | CONTINUE |
| ≥ 0.4 | all in {L21,L22,L23} | KILL as independent family |
| [0.2, 0.4) | — | HELD |
| < 0.2 | — | KILL |

The ≥0.4 region is split by the top-3 condition into two disjoint
sub-cases; the top-3 tie-break (lowest layer index first, §0) makes
the set deterministic. The structure matches the gate (LOG-4702 §2)
under Law #4 — the notation change {x_21,x_22,x_23} → {L21,L22,L23}
is disambiguated by the pre-reg's explicit §3.1 site definition
(see FIX-4). No recalibration, no cross-field comparison. ✓

## 2. Gini statistic ✓ (with FIX-6)

§0 pins the standard mean-absolute-difference form
G = Σ_iΣ_j|S_i − S_j| / (2·n²·S̄), n = 24 — the correct formula,
executor-computed (defect class (a) honored). A concentration
coefficient over the 24-element field is the right statistic for
the "soft spots vs uniform" question, and the no-p-value stance is
coherent: the bars are pre-registered concentration properties,
not hypothesis tests. One precision point (FIX-6): S_l as defined
(ratio averaged over isotropic u) estimates the
mean-random-direction gain — Frobenius-norm-related, a lower bound
on the spectral norm — not the spectral norm σ_1 that EXP127's
power iteration measured. The Gini concentration question is
unaffected, but the "same object EXP127 measured via JVPs"
phrasing (gate §4, echoed in §1.1) overstates the identity.

## 3. ε design ✓ — no fix

ε = 1e-3 absolute is a gate pin (Law #4 binds it). The protocol
does not assert linear-regime validity a priori; it *tests* it via
the pre-registered ε/2 check with a no-retune rule (failed check →
apparatus-void, never a smaller ε). That is internally consistent
and methodologically honest — the check, not the constant, is the
arbiter. Tolerance/ quorum are consistent everywhere: §0(b),
§3.6, and the §5 tree all require |S(ε/2)−S(ε)|/S(ε) ≤ 0.25 on
≥ 10 of 12 points; 10/12 = 83.3% ≥ 80%, and 10 = ceil(9.6) as
stated. ✓

## 4. δ discipline ✓ (with FIX-3, FIX-5)

The stream-seed formula `20260929 + item_idx·10^6 + layer·10^3 +
draw` is collision-free (max layer·10³+draw = 23,003 < 10⁶; max
draw = 3 < 10³) and deterministic. Two under-specifications
(FIX-3, verdict-immaterial): the RNG algorithm is unnamed
(torch.Generator vs numpy Generator matters for Law #13 exact
reproducibility), the draw-index origin (0- vs 1-based) is
unpinned, and the S(ε) = 0 division edge has no rule (count such
a point as failed). On draw-count adequacy: K = 4 is a gate pin
(Law #4 binds it) and each S_l aggregates 40 samples against wide
bars (0.2/0.4); the protocol carries no analytic adequacy
argument, so the honest mitigation is FIX-5 (verdict-immaterial):
the executor records per-layer standard errors and a split-half
(draws {0,1} vs {2,3}) Gini-stability diagnostic as a disclosed
[OBSERVATION] that no bar reads.

## 5. Forward count ✓ — arithmetic verified

10 × 24 × 4 × 2 = 1920 field forwards; 3 × 4 × 4 = 48 ε/2-check
forwards (S(ε) reused from the main field per §3.6); total 1968 —
consistent across §3.6, §3.7, and §7. Note for the executor: the
pinned 1920 count implies the base forward g_l(y_l) is computed
per (item, layer, draw), **not** reused across the 4 draws; the
count is arithmetically consistent as written, so the executor
must match it (any base-reuse optimization would need a protocol
amendment, not a silent change).

## 6. Generation-channel distinction — RULED SOUND

The terminal rule (EXP115/116/123) covers *elicitation-as-readout*.
DSF's metric (§3.4) is purely ‖g_l(y_l+δ) − g_l(y_l)‖₂ at
x_{24,last} — the residual stream before the unembedding. Output
logits are a forward-pass byproduct that is never read; no token
is decoded, no text is read, no content-dependent statistic is
computed; §6 states "No generation" explicitly and §3.5 gives the
Law-#7 content-cleanliness argument (isotropic δ, no labels
anywhere). **Ruling: the distinction holds; the terminal rule is
unengaged.** No fix.

## 7. Loader and pin ✓

§3.7 explicitly adopts `AutoModelForCausalLM` with the EXP126
loader lesson stated (LOG-331 computed on the causal-LM state
dict); the pin value
`ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
matches the program record. ✓

## 8. Breaking point — complete, EXCEPT the ordering (FIX-1) and
## the missing §3.9 (FIX-2)

The disjunction (a)–(d) plus the §5 tree covers every failure
mode (pin mismatch, linearity failure, δ-budget mismatch,
training, forward-batch failure via exit code) → apparatus-void,
hypothesis UNTESTED, no field minted. **But two defects:**

- **FIX-1 (launch-gating):** the stated Law #9 ordering (§0 and
  §5: "guards → backbone pin → linearity check → field → …") is
  unexecutable — the linearity check's *evaluation* requires S(ε),
  which §3.6 reuses from the main field. The check cannot be
  evaluated before the field forwards exist. Correct to:
  "guards → backbone pin → forward batches (field + ε/2 arm, either
  batch order) → linearity-check evaluation → raw-record hash-pin
  → Gini → decision", with check failure → apparatus-void before
  hash-pin. This preserves Law #9's intent (no metric before
  guards) while being executable.
- **FIX-2 (launch-gating):** the §5 tree's "Raw records hash-pinned
  before verdict (§3.9)" references a section that does not exist
  (the only "§3.9" hit in the document is that reference). Add
  §3.9 specifying the raw artifact set (per-triple ratios, per-layer
  S_l, δ seeds/vectors, S(ε/2) check values, environment manifest,
  console log), SHA-256, pinned before the Gini computation.

With those two fixes, no path to a Gini exists after any partial
failure.

## 9. Seventh-item record and never-resurrect audit ✓

§10's constraining-kill record (EXP077, EXP094, S5-2, S5-3, G1,
EXP115/116/123 — each a snapshot-instrument, semantic-direction,
or content-readout result; none measured layer-wise dynamical
sensitivity) is accurate and consistent with gate §7. The
never-resurrect list (H17, S5, H12, bench re-reading,
EXP117/118/119/121/123/124 reruns, entity-name generation, H22's
generality, H23's identity interpretation, TGA untouched) is
complete. ✓

## 10. Boundary ✓ (with FIX-7b)

No injection licensed ✓; final-token site only ✓ — consistent
with TGA §3.3, which named the cross-position Jacobian a design
decision (not measured), not a verdict factor. The draft's §10
parenthetical "(the cross-position Jacobian was barred in TGA
§3.3)" slightly overstates it → reword to "named as a design
decision (not measured) in TGA §3.3" (FIX-7b). Causality note
(for the record, no fix needed): perturbing the final-token
residual at layer l affects only the final-token trajectory
downstream, so the final-token-only map is clean.

---

## Fixes

### Launch-gating (must be applied and byte-verified before CEO launch)

- **FIX-1 — Law #9 ordering (§0, §5):** the linearity-check
  evaluation requires S(ε) from the field and cannot precede the
  forward batches. Reword both ordering strings to: "guards →
  backbone pin → forward batches (field forwards + ε/2-check
  forwards, either batch order) → linearity-check evaluation →
  raw-record hash-pin → Gini → decision", with check failure →
  apparatus-void before hash-pin. Reorder the §5 tree rows to
  match (linearity-evaluation node after the forwards node).
- **FIX-2 — missing §3.9:** write the raw-record hash-pin
  specification the §5 tree references: the artifact list, SHA-256,
  and the pre-Gini timing (defect class (b)).

### Verdict-immaterial (apply before launch; no bar or gate changes)

- **FIX-3 — §3.3 seed discipline:** name the RNG algorithm,
  pin the draw-index origin, and add the rule "S(ε) = 0 at a check
  point counts that point as failed."
- **FIX-4 — §2/§3.1 span notation:** one sentence clarifying that
  {L21, L22, L23} denotes the three sites nearest the readout
  under §3.1's block-input indexing (disambiguating the gate's
  x-notation; no bar change).
- **FIX-5 — estimator health:** executor records per-layer
  standard errors (40 samples) and a split-half Gini-stability
  diagnostic as a disclosed [OBSERVATION]; no bar reads it.
- **FIX-6 — norm identity:** clarify that S_l estimates the
  mean-random-direction gain (Frobenius-related), and soften "the
  same object EXP127 measured via JVPs" to the same
  layer-to-readout gain family.
- **FIX-7 — citation precision:** (a) the Henrici license
  (He = 0.7332–0.8343, mean 0.7689, 48 O/V components) is EXP086
  Stage A (LOG-331), not `G1_REPORT_2026-09-23.md` — correct the
  header citation (§1.1 already attributes it correctly to
  EXP086); (b) TGA §3.3 cross-position wording per §10 above.

**Law #14 verdict: SIGN-WITH-FIXES.** After FIX-1 and FIX-2 are
applied and byte-verified (plus the five immaterial fixes), the
protocol is launchable under the CEO launch decision. No
structural defect; the hypothesis is falsifiable, the bars bind,
and the measurement is new (Law #4: unfollowed, never killed).
