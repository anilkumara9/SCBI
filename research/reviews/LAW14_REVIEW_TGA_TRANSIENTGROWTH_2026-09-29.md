# Independent Law #14 Review — TGA Pre-registration (Transient-Growth Amplification)

**Lane:** LOG-4696 (pre-assigned). **Artifact reviewed:**
`research/prereg/EXP_PREREG_TGA_TRANSIENTGROWTH_2026-09-29.md`
(TGA draft, LOG-4695; Family A of the paradigm-break sprint).
**$0 CPU.** Read-only on all signed artifacts; nothing pushed, spent, or
credential-touched. Fresh eyes — this lane did not draft the protocol.

**Verdict: SIGN-WITH-FIXES** — one launch-gating fix, four
verdict-immaterial fixes. The design is licensed and launchable once
FIX-1 is applied and byte-verified.

---

## The ten assigned checks

### 1. Bar partition: coherent, disjoint, exhaustive — PASS

Let (R, S) = (median R, median σ₁/σ₂), R ≥ 0 always
(R = σ_max/σ̄, σ̄ > 0 for nonzero M):

| Region | Verdict |
|---|---|
| R ≥ 3, S ≥ 1.5 | CONTINUE |
| R ≥ 3, S < 1.5 | KILL |
| 2 ≤ R < 3, any S | HELD |
| R < 2, any S | KILL |

R ≥ 3 is covered by the first two rows for all S > 0; 2 ≤ R < 3 by the
third; R < 2 by the fourth. Boundaries: R = 3 → the R ≥ 3 rows
("≥ 3"); R = 2 → HELD ("2 ≤ R"); S = 1.5 with R ≥ 3 → CONTINUE
("≥ 1.5"). Every (R, S) pair falls into exactly one cell. The
partition is complete and disjoint. (The median-convention ambiguity
at even decision-set sizes is a separate, launch-gating defect —
FIX-1 below — not a partition defect.)

### 2. Mathematical license chain — PASS with a precision fix

- **[THEOREM] variational SVD characterization** (max_{‖δ‖=1} ‖Mδ‖ =
  σ_max): correct, and it is the actual load-bearing theorem — the
  pilot measures the largest possible linear gain of the frozen span
  directly. ✓
- **[THEOREM] Kreiss Matrix Theorem**: the lower-bound form
  sup_k ‖A^k‖ ≥ ρ_ε(A)/ε is stated correctly. Its role is explicitly
  fenced in §8 ("gives an *existence condition*, not a predicted
  number; the R ≥ 3 bar comes from the program's own ×1.8 precedent,
  not from the theorem") — the draft does not derive any quantitative
  prediction from it. Strictly, Kreiss concerns powers of a fixed
  operator while TGA measures one finite-horizon product; the draft's
  fencing makes this decorative-but-honest, not load-bearing. No
  defect — but see FIX-2 for the adjacent He-description precision.
- **EXP086 Stage A He as license**: verified against the log —
  He: min 0.7332, max 0.8343, mean 0.7689 (LOG-331, CPU, read-only,
  Δθ=0). The numbers are quoted exactly. Stage A was signed
  "advisory only — verdict is None by construction" (it cannot
  KILL/CONTINUE/HOLD/PIVOT a family); the draft uses He only to
  motivate the pilot question, never as a guard or verdict input —
  within bounds. However, the draft writes "48 attention blocks";
  the measured object was 48 attention O/V projection components
  (24 O direct + 24 V fused-interleaved) across 24 layers — FIX-2.

### 3. Power-iteration design vs the ≥8/10 rule — REAL DEFECT, launch-gating (FIX-1)

Breaking point (b) permits 8/10 or 9/10 σ₁-converged prompts and
forbids reading from unconverged iterates, but the §0 [DEFINITION]
defines the decision statistic as "the median R over the 10 prompts"
and nothing pins (i) whether the median is computed over the
converged subset, (ii) the median convention for an even count
(n_d = 8), or (iii) whether the median σ₁/σ₂ is computed over the
same prompts as median R (the §5 tree requires σ₂ convergence on
≥ 8/10 independently — the two converged sets need not coincide, and
by pigeonhole their intersection can be as small as 6). The executor
cannot compute the verdict without these rules. **FIX-1
(launch-gating):** pin that the median R and median σ₁/σ₂ are both
computed over the decision set = prompts on which *both* σ₁ and σ₂
converged (n_d ≥ 8 required; fewer → apparatus-void), with an explicit
executor-computed median convention for even n_d (recommend: average
of the two middle order statistics); update the §0 [DEFINITION] and
the §2 table header ("Median R (10 prompts)") to name the decision
set. No bar changes.

### 4. Hutchinson estimator arm — PASS with an auditability fix

- σ̄ = sqrt(Tr(MᵀM)/1024) is the correct normalization: for isotropic
  u, E[‖Mu‖²] = Tr(MᵀM)/1024 = σ̄², so R = σ_max/σ̄ measures the
  leading-vector gain against the RMS random-direction gain — exactly
  the "dwarfs the gain along random directions" claim. ✓
- "Same M, same budget" is verifiable in principle: both null arms
  are K=64 on the same M, and §3.6 pins the product-counting rule —
  but §3.7's hash-pinned record list does not include per-arm product
  counts, so breaking point (c) is not auditable from the pinned
  records. **FIX-4 (verdict-immaterial):** add per-arm autograd
  product counts to the §3.7 pinned record list.
- Observation (not a fix): Hutchinson Tr(MᵀM) needs only JVPs
  (E[‖Mz‖²]); the draft's "1 JVP + 1 VJP per draw" is a conservative
  costing, safe under the hard cap.

### 5. Budget cap vs gate estimate — PASS

Gate: ~300–500 JVPs, ~1h. Draft: hard cap 700 products/prompt, ≤7000
total, ~1–2 CPU-hours. §9 item 1 discloses this fully with the reason
(the σ₂ deflation arm postdates the gate estimate) and states the
kill bars are unchanged. The deviation list (§9, seven items) was
checked against the gate memo item by item — complete, no unlisted
deviations. The bars are identical. ✓

### 6. Jacobian definition and clamping discipline — PASS

§3.3 pins the object exactly: all keys and values at all positions
clamped to base-pass values; only the block-20 input residual at the
last token varies; M = ∂x_{24,last}/∂x_{20,last} via autograd JVP/VJP.
The map is differentiable in the single 1024-vector (queries vary
against clamped KVs; the residual path is differentiable). The
cross-position (unfrozen-KV) Jacobian is correctly flagged out of
scope ([OPEN] in §3.3, §6 item 2, §10) — a design decision, not a
verdict factor. ✓

### 7. Span placement — PASS, coherent with no-rescue

L20→L24 primary; **no fallback span licensed**; L12→L16 named only as
a future gate's target. R < 2 kills the dynamics-matched program
outright (both §2 and §4 tables); HELD requires a new gate for any
re-test. A fallback measurement after an R < 2 would be a rescue —
the pre-reg correctly refuses to license one. ✓

### 8. Seventh-item record — one factual correction (FIX-3)

Verified against the log: EXP077 cone kills at L20 (ΔM=0, p=1.0) ✓;
EXP094 L11 inertness (120 arms, zero flips) ✓; S5-2 4.87% per-arm 95%
upper bound ✓; S5-3 PIVOT — never-decodable for all eight EXP077
variants ✓; G1 QK-subspace KILL ✓; the 2026-09-25 TGA proposal ranked
#2 with "$0 CPU; no experiments executed" — the "unfollowed, not
killed" claim checks out ✓. **Defect:** EXP086 Stage B is listed
among the "constraining kills" as "(task-informed decision-normal
amplification)" — but Stage B was licensed and GPU-gated and **never
executed** (no GPU spent); it is not a kill. **FIX-3
(verdict-immaterial):** reclassify EXP086 Stage B as "licensed,
GPU-gated, never executed" and remove it from the kills list. The
substantive claim — no *executed* experiment measured or injected
along v_1 — stands.

### 9. Downstream ĉ gate deferral — PASS

The ĉ < 0.1 and rank-trend KILL gates are named in §2 explicitly for
the GPU pre-reg a CONTINUE would license; §6.1 states no injection is
licensed; §10 states a CONTINUE licenses the GPU *pre-registration*,
not GPU execution. Correctly deferred; no injection is licensed by
this pre-reg. ✓

### 10. Defect-class N/A claims — genuinely inapplicable, PASS

- (e) [-3:] N/A — no logit channel, no decode, no token readout. ✓
- (f) single-token N/A — no bench, no entities, no options. ✓
- (g) per-item G1 N/A — no treatment arms, no screening. ✓
- Law #7: "No labels enter anywhere" — prompts are the verbatim
  EXP107 bench, canonical-order first 10, deterministic
  no-RNG selection with ids pinned; the decision statistic is pure
  linear algebra on the frozen propagator. The selection is
  label-blind by construction (position-based), and labels are never
  read. Posture sound. ✓

---

## Additional findings

- **Wrong cross-reference (verdict-immaterial, FIX-5):** breaking
  point (b) cites "the §3.6 power-iteration convergence criterion" —
  the criterion is defined in §3.4; §3.6 is the budget. Correct to
  "§3.4".
- **Power-iteration math verified:** v^{(k+1)} = MᵀMv/‖MᵀMv‖,
  ρ_k = ‖Mv^{(k)}‖² (Rayleigh quotient of MᵀM on the normalized
  iterate), σ = sqrt(ρ_final) — correct. Deflated σ₂ via
  v_1-orthogonal projection — standard. Seeded isotropic start —
  fine.
- **Null anchor math verified:** for normal M, σ_max/σ̄ =
  |λ|_max/RMS(|λ|) ≈ 1 on a flat spectrum — correct.
- **Budget/convergence interaction:** if the 700-product cap
  truncates before ≥8 prompts converge, breaking point (b) fires
  apparatus-void — the honest outcome; no rescue path exists. ✓
- **Defect-class 1:** the draft correctly frames R ≥ 3 as a ratio
  bar, not a p-value; no p-value is computed or quoted. ✓
- The direct-arm |median − σ̄|/σ̄ ≤ 0.15 trip is disclosed as
  diagnostic-only, non-verdict-bearing. ✓
- H17, S5, H12, bench re-reading, EXP117/118/119/121/123/124 reruns,
  entity-name generation, H22 generality, H23 identity interpretation
  stay dead and untouched. ✓

---

## Fixes

**FIX-1 — launch-gating (verdict computation undefined without it):**
Pin the decision set and median convention. In §0 [DEFINITION], §2
table header, §3.4, and §5: the median R and median σ₁/σ₂ are both
computed over the decision set = prompts on which *both* σ₁ and σ₂
converged (n_d ≥ 8 required; fewer → apparatus-void); pin the median
convention for even n_d (recommend: average of the two middle order
statistics), executor-computed. No bar changes.

**FIX-2 — verdict-immaterial (factual precision):** "across all 48
attention blocks" (header license line; §1.1) → "across 48 attention
O/V projection components (24 O direct + 24 V fused-interleaved) in
24 layers," matching the signed EXP086 Stage A report. Numbers
(0.7332–0.8343, mean 0.7689) are correct as quoted.

**FIX-3 — verdict-immaterial (historical accuracy):** seventh-item
record (§10): reclassify EXP086 Stage B as "licensed, GPU-gated,
never executed" — remove it from the constraining-kills list. The
"no executed experiment measured or injected along v_1" claim
stands.

**FIX-4 — verdict-immaterial (auditability):** add per-arm autograd
product counts to the §3.7 hash-pinned record list so breaking point
(c)'s "same budget" requirement is auditable at execution.

**FIX-5 — verdict-immaterial (cross-reference):** breaking point (b):
"the §3.6 power-iteration convergence criterion" → "the §3.4
power-iteration convergence criterion."

**Observations (no fix required):** Hutchinson Tr(MᵀM) needs only
JVPs — the draft's "1 JVP + 1 VJP per draw" is a conservative
costing, safe under the hard cap. The Kreiss theorem's stated form
(powers of a fixed operator) vs the single finite-horizon product M
is correctly fenced in §8 as an existence condition only.

---

*Next in the launch chain: fix-verification lane (byte-verify FIX-1
through FIX-5) → CEO launch decision → execution under a minted
experiment number.*
