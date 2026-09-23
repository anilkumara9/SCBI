# Adversarial Review — EXP077 Cone-vs-Line Pre-registration (DRAFT)

**Reviewer role:** Adversarial Reviewer, Law #14
**Date:** 2026-09-23
**Document under review:** `experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md`
(DRAFT — PENDING ADVERSARIAL REVIEW — NOT SIGNED; drafted LOG-095 from sprint New Idea 6 / P6)
**Verdict:** **SIGN-WITH-FIXES** — 4 MAJOR, 6 MINOR. The draft is not signed until every
MAJOR is applied and re-verified. No REJECT: no fabrication, no fatal mathematical error,
every branch falsifiable, N1 intact.

**Reviewed against:** `AGENTS.md` (14 laws), `research/MATH_STANDARDS_CHARTER.md` (M1–M8),
`research/innovation/SPRINT_2026-09-23.md` New Idea 6 (the ACCEPTED proposal — P6 passed
clean, no fixes), `reports/adversarial_audit_exp065_exp066.md` (boundary facts),
`theory/BOUNDARY_CLAIM_FORMALIZATION.md` (I1, B_agg construction), EXP075 §7.1 (multiplicity
precedent), EXP075 branch (d) (boundary-revision precedent).

---

## 1. Rulings on the drafter's two self-flagged weaknesses

### 1.1 Radius misspecification — RULING: the drafter's worry is upheld; the current license bound is INSUFFICIENT

The drafter asks whether the "at ρ=30°" bound (A-cone-radius, §7; §1.2(c) DOES-NOT column)
suffices for the kill branch (c). **It does not, as currently written** — and the problem is
narrower and more mechanical than "add a second radius":

- §1.2(c) LICENSES reads: *"The cone/affine geometry hypothesis **dies for this task**."*
  The ρ=30° condition appears only in the DOES-NOT column ("other radii"). A license sentence
  is the citation-ready unit; per charter **M2.4** (conditional results must name their
  condition in every citation — dropping the condition when citing is a MAJOR finding), the
  kill license as written launders the radius condition. A reader quoting "the cone hypothesis
  dies for this task" will not carry "at ρ=30°".
- The asymmetry is one-sided and dangerous: a positive at ρ=30° licenses "the rescuing region
  extends beyond the single line" (generalizing, (a)), while a negative at the same single
  radius licenses the *death* of the whole cone hypothesis (c). Killing on one radius while
  generalizing on one radius is not symmetric science.
- A-cone-radius (§7) already states the correct bound ("branch (c)'s kill is licensed only at
  the tested radius") — the fix is to make the license sentence say what the assumption says.

**Required fix (MAJOR-2):** rewrite §1.2(c) LICENSES to carry the condition in the sentence,
e.g.: *"The ρ=30° cone hypothesis dies for this task (A-cone-radius); the affine-offset
hypothesis dies at the tested α=1.0; cones at other angular radii are untested and survive
this kill."* The gated (CAST-style) variant must be excluded in the license sentence as well
(it is currently only in DOES-NOT): *"…the unconditional cone/affine geometry hypothesis;
the conditional (gated) variant is untested (§11) and is not killed by (c)."*

A second radius arm (e.g. ρ=60° with a matching control cone, +960 passes, still free-tier
feasible at ≤2,700 total) remains a legitimate strengthening option at the CEO's discretion,
but it is **not required** for signing — the license rewrite is. If a second radius is added,
it needs its own attempts control; the existing control cone (built at ρ=30°) does not cover
a second radius arm.

### 1.2 Multiplicity on trigger (a)(ii) — RULING: Holm gate required; the "pre-registered curve" framing is not a multiplicity control

The drafter's arithmetic is correct: 1−0.95⁴ ≈ 0.1855 (~19%) family-wise across the four α
tests under independence. Two refinements:

1. Trigger (a)(ii) needs not just *any* significant α but a **non-upper** nonempty pattern,
   which trims the rate: P(non-upper nonempty) ≈ 0.1855 − P(upper nonempty) ≈ 0.1855 − 0.045
   ≈ **0.10–0.14** (positive dependence from the shared C1 pushes it below the independence
   value). Still roughly one-in-seven-to-ten false CONE-WINS under the global null.
2. The drafter's defense confuses two different things. Law #9 ("a single significant α is
   not cherry-picking if the grid was pre-registered") controls **researcher degrees of
   freedom** — which α gets reported. It does not control the **Type I error of the
   curve-shape test** — the chance that a null curve yields CONE-WINS. A pre-registered curve
   is still a multiple-testing procedure.

Trigger (a)(ii) can **withdraw the program's headline null in its blanket form**. A ~10–14%
false-positive rate on that trigger is too loose, and EXP075's "precedence-order as
multiplicity control" precedent does not transfer: EXP075 disclosed no FWER correction for
motivation-grade claims, but none of EXP075's branches withdrew a standing headline null.

**Required fix (MAJOR-3):** feed **Holm-adjusted** p-values into the radial shape
classification. Concretely, in §8: `S_H = {α : Holm-adjusted McNemar p < 0.05 vs C1 and
ΔM > 0}`; the empty / upper-set / non-upper classification runs on S_H. The curve remains
the endpoint (Law #9 intact — no α is cherry-picked); only the trigger's error rate is
controlled. Consequences that must be carried through:
- §7 A-headroom: minimum detectable pure-rescue signal becomes **8 net items** ((8,0) →
  p=0.0078 < 0.0125; (7,0) → p=0.0156 > 0.0125 — does not survive Holm), not 6.
- Checklist "kill criterion exact": flat-zero = all four **Holm-adjusted** p ≥ 0.05.
- The kill trigger is unaffected in practice (unadjusted all-null ⇒ Holm all-null).

The angular trigger (a)(i) needs no correction (conjunctive: both McNemar p<0.05 required —
FWER ≈ 0.0025 under the null). The offset trigger (a)(iii) is a single test. The fix is
surgical to the radial trigger only.

---

## 2. MAJOR findings (must fix before signing)

### MAJOR-1 — Missing C3-replication branch: the boundary null's own failure misfires into CONE-WINS

**Location:** §8 decision tree; §1.2 table; §6 ("C3 vs C1 as the boundary-null replication
check").

§6 registers C3 (v̂ at α=0.50) as the boundary-null replication check, but **no branch fires
on its failure**. Trace the cell: C3 significant (ΔM>0, p<0.05) with all other α null. Then
S = {0.5}, which is nonempty and not an upper set ({α ≥ α*} fails: 1.0, 2.0 ∉ S). Trigger
(a)(ii) fires → CONE-WINS, licensing *"the rescuing region extends beyond the single line…
zero transfer under single-direction static injection at the tested scales does not imply
zero transfer under geometrically richer injection."*

That license is **false for this cell**: the event is the *single line itself* rescuing at
the boundary null's own scale — I1 failed to replicate. The tree reads a replication failure
as cone evidence. Per M5.2 this is worse than a missing cell: the cell lands in a branch
whose license misdescribes it. EXP075 set the precedent for exactly this situation
(branch (d): "C2 rescues → Boundary revision — supersedes (e)–(i)").

**Required fix:** add a replication-failure branch, precedence immediately after (d) and
before (a):
> **(r) BOUNDARY-NULL REPLICATION FAILURE.** Trigger: C3 vs C1, two-sided McNemar p<0.05
> with ΔM≠0 (rescue *or* significant corruption — I1 asserts ΔM≡0). Ruling: report ΔM,
> (b,c), p, and this run's baseline accuracy alongside the historical EXP065/066 baselines
> (comparability rider per EXP075 branch (d)); **no geometry branch fires** — the geometry
> question is moot when the null itself did not replicate; re-scope under a new
> pre-registration. LICENSES: "I1 failed to replicate on pythia-410m/layer-20 at α=0.5 in
> this run." DOES NOT LICENSE: anything about H_cone/H_line.
- Update §8 precedence to (d) > (r) > (a) > (b) > (c); add the (r) row to the §8 table and
  the §1.2 LICENSES table; extend the M5.2 partition trace ("C3 sig → (r), regardless of
  other cells"); update the checklist (branch count, precedence string).
- Note: with (r) in place, (a)(ii) can still fire on S_H={0.25} alone (C2 significant, C3
  null) — a genuine peaked-at-low-α curve with the boundary null intact. That firing is
  legitimate and must be preserved.

### MAJOR-2 — Kill license drops the ρ=30° condition (M2.4)

Covered in §1.1 above. **Location:** §1.2(c) LICENSES sentence. Apply the rewrite there;
mirror the qualified wording in the §8 branch-(c) ruling cell.

### MAJOR-3 — Radial trigger needs a Holm gate

Covered in §1.2 above. **Locations:** §8 radial-shape definition, trigger (a)(ii), §7
A-headroom (6 → 8 net items), pre-registration checklist kill-criterion wording.

### MAJOR-4 — Proposal fidelity: the angular apparatus is new, the gated variant is deferred — reconcile with the accepted P6 record (Laws #4, #12)

The accepted P6 proposal (SPRINT_2026-09-23.md, New Idea 6 — ACCEPT clean, no fixes) specifies
three geometric tests: **(a)** α scale sweep, **(b)** offset test, **(c)** CAST-style
non-negativity gate. Its condition list (C1–C7) contains no angular cone sampling. The draft:
- **Adds** the entire angular cone/control-cone apparatus (§3.3, §3.4, §3.6 K/R indicators,
  C9/C10, the PRIMARY endpoint, +960 forward passes — the budget goes from the proposal's
  ~450 passes to ≤1,740, ~4×).
- **Defers** the gated variant (c) to P5's tournament (§11), while the proposal's kill
  criterion explicitly conjoined it ("the offset-removed and gated variants also yield
  ΔM = 0").

The angular arm is scientifically the most direct operationalization of the titular question,
and the deferral is honestly labeled (§11, §1.2 DOES-NOT columns) — this is not silent
hypothesis-shifting in the draft itself. But the proposal is a finalized, accepted record,
and proposal→draft changes of this magnitude (new primary endpoint, 4× budget, dropped kill
conjunct) must be **logged as an amendment, not left implicit** (Law #4: never silently shift
hypotheses; Law #12: document major decisions).

**Required fix (amendment path, recommended):** append a dated, clearly-marked
post-acceptance amendment note to the P6 section of `research/innovation/SPRINT_2026-09-23.md`
(do not rewrite the accepted text) recording: (i) the added angular cone/control apparatus
with rationale (direct test of the titular question; the α-sweep alone tests only radial
geometry); (ii) the gated variant's deferral to P5 with rationale (conditionality is a
separate mechanism class; the proposal's own condition list C1–C7 never operationalized it);
(iii) the narrowed kill (unconditional geometry only). The alternative — removing the
angular apparatus and restoring the gated arm — is acceptable but not recommended.

---

## 3. MINOR findings (fix within one review cycle; none blocks signing alone, all must be recorded)

- **MINOR-1 — "Grid midpoint" gloss (§2).** "Cone/control arms use α = 1.0 fixed [ARBITRARY
  — the grid midpoint; pinned]." 1.0 is not the midpoint of {0.25, 0.5, 1.0, 2.0} by any
  standard computation (median 0.75; geometric mean ≈ 0.707). Re-justify on substantive
  grounds (e.g. "one doubling above the null's α=0.5, giving the line arm headroom while
  staying in the tested regime") and drop the "midpoint" claim.
- **MINOR-2 — Wall-clock inconsistent with the proposal's rate (§9).** The proposal's
  ~450 passes ≈ <30 min implies ~15 passes/min → 1,740 passes ≈ ~2 h, not "≈ 30–45 min".
  Re-anchor the estimate to the proposal's rate or tag it [CONJECTURE].
- **MINOR-3 — RNG ordering for pinned seeds (§10).** "Cone orthogonal axes 7701; control
  direction + axes 7702" — require that each seed be set **immediately before its draws**
  (or via a dedicated `torch.Generator`), so no intervening RNG consumption can desynchronize
  the pinned constructions. One sentence in §10.
- **MINOR-4 — SHA-256 TBR (§2).** Same model as EXP067 (pythia-410m); carry EXP067's
  registered expected hash as the sanity-check value instead of TBR. The binding guard
  remains the runtime pre/post match.
- **MINOR-5 — Multiplicity disclosure (§8).** Add the EXP075-style disclosure paragraph:
  three sub-triggers feed branch (a) testing distinct sub-hypotheses (angular/radial/affine);
  the radial trigger is Holm-gated (§1.2 ruling); the licensed claims are motivation-grade
  (withdraw/replace the blanket null), not confirmatory-efficacy claims.
- **MINOR-6 — (b)(ii) license overstates singleton upper sets (§1.2(b), §8).** S_H = {2.0}
  alone is an upper set by the definition but a single point is *consistent with*
  monotonicity, not proof of it. Soften to "rescue is monotone-non-decreasing over the
  tested grid (singleton upper sets are consistent with, not proof of, monotonic scaling)."

**Note for the bundle's adversarial review (not this prereg):** §3.4's
`|cos(r,v̂)| < 0.5` build assert is deterministic given pinned seed 7702 — verify it passes
during bundle construction rather than discovering a stillborn protocol at runtime.

---

## 4. What survived the battery (passes — recorded so the next reviewer need not re-litigate)

- **Exhaustive partition (M5.2):** with MAJOR-1's (r) branch added, every cell of
  gates × C3-replication × angular × control × radial(Holm) × offset lands in exactly one
  branch; precedence (d)>(r)>(a)>(b)>(c) is unambiguous; the "attempts-alone" sub-case
  (angular b>c sig but control failed → (c), named) and the cone-ties-line-beats-control
  cell (→ (c), neither cone- nor line-wins) are assigned. Degenerate b=c=0 → p=1.0 handled
  (§3.6, M5.1); p=0.05-exactly → null stated (§8).
- **M4 space/shape checks:** M4.1 shapes stated (§3.1); M4.2 fit space = application space =
  residual stream at l*=20 for v̂, cone, control, and offset arms — no transfer assumption
  needed, stated in-text; the bridge's cross-space use is carried as labeled A-bridge-space
  with the EXP065/066 empirical-validity precedent (the program's accepted handling);
  M4.4 renormalization-before-injection stated with the amplification factor logged (§3.2).
  The cone is posited, not fit (§12) — M4.3 has no fitted operator to bite on.
- **Assumption labeling:** A-cone-radius, A-headroom, A-reconstruction, A-bridge-space all
  labeled [ASSUMPTION]; ρ, K, α grid, cone α, continuity floor tagged [ARBITRARY]; the
  sweep provenance carried unlaundered (algoverse Aug 2026 LOW-confidence secondary;
  QCRI/ACE practitioner-doc-only) — no laundering detected.
- **Falsifiability:** every branch has a crisp trigger; (c) is a genuine kill; (d) invalid
  is a valid outcome; no branch licenses novelty (N1 stands — §11, §1.2, checklist all
  consistent); margin shifts quarantined as exploratory (O5 respected); C7 diagnostic never
  a trigger.
- **Budget arithmetic:** 300 + 480 + 480 + 480 = 1,740 ✓; ≤1,740 claimed consistently
  (§1.1, §9, checklist).
- **Numbering:** EXP077 free at pre-registration time; EXP076/069/071–074 reservations
  respected.
- **Law #13 archive:** v̂_k, v̂, μ, v̂^c, w_j, φ_j, r, q_j, per-instance C1–C10 correctness,
  all rescue indicators, id-disjointness lists, injection norms, env manifest, SHA-256 —
  comprehensive.
- **Anti-cheat (Law #7/8):** support/benchmark id-disjointness asserted at runtime; no test
  label enters any construction; leakage = invalid, never silently corrected.
- **B_agg reconstruction formula** verified against `theory/BOUNDARY_CLAIM_FORMALIZATION.md`
  §2 (normalize-of-normalized-means, then normalize(sum)) ✓.
- **Metaphor audit (M7):** "rescue" operationally defined (§3.6, M7.2 cited); "kill" =
  hypothesis-rejected/I1-strengthened per the license text; no metaphor does definitional
  work.

---

## 5. Verdict

**SIGN-WITH-FIXES.** Apply MAJOR-1 through MAJOR-4 (exact locations above), record the six
MINORs, then re-verify: (i) the (r) branch in the §8 table, the §1.2 table, the precedence
string, the M5.2 trace, and the checklist; (ii) the Holm-gated S_H definition threading
through §8, §7 A-headroom, and the checklist; (iii) the radius-qualified kill license in
both §1.2 and §8; (iv) the dated P6 amendment note in the sprint document. The reviewer
re-checks the four MAJOR diffs before the DRAFT banner comes off. The bundle may be built
in parallel but **no GPU execution** until this review's fixes are signed off.

*No results exist under this protocol. This review changes no primary artifact.*

---

## 6. Re-verification of fixes (Law #14 signing gate) — 2026-09-23

**Re-verifier role:** Adversarial Re-verifier, Law #14
**Verdict: SIGN.** The protocol is now PRE-REGISTERED. Every MAJOR was applied exactly as
required; all six MINORs and the §3.4 determinism note are present; a stale-reference sweep
found no leftover contradicting the fixes.

### 6.1 MAJOR-by-MAJOR diff verification (checked against the reviewer's exact requirements)

- **MAJOR-1 — branch (r).** New row in the §1.2 LICENSES table ((r) REPLICATION FAILURE,
  two-sided, licenses only "I1 failed to replicate", licenses no geometry) and in the §8
  decision table. Precedence string updated to (d)>(r)>(a)>(b)>(c) in both the §8 header
  ("evaluated first; then (r); then (a); then (b); (c) is the residual") and the checklist
  (compact form, line 374). M5.2 partition trace extended: "C3 sig → (r), regardless of
  other cells"; the (a)(ii) entry explicitly states it is "suspended by (r) when C3 is
  significant" and preserves the legitimate firing "S_H={0.25} alone with C3 null" — the
  peaked-at-low-α cell the reviewer required not to lose. §6's C3 paragraph now points at
  branch (r): "a significant deviation in either direction fires branch (r), never a
  geometry branch." Two-sidedness (ΔM≠0 either direction) present in all three locations.
  PASS.
- **MAJOR-2 — kill license radius-bound.** §1.2(c) LICENSES sentence now reads: "The
  ρ=30° unconditional cone hypothesis and the α=1.0 offset hypothesis die for this task —
  cones at other angular radii are untested and survive this kill. The conditional (gated)
  variant is untested (§11) and is not killed by (c)." The condition is in the sentence
  itself (M2.4 satisfied — no citation-laundering path); the gated variant is excluded in
  the sentence. §8 branch-(c) ruling cell mirrors the qualified wording. No second radius
  arm was added (a permitted option, not required). PASS.
- **MAJOR-3 — Holm gate.** Radial shape [DEFINITION] now classifies S_H on Holm-adjusted
  McNemar p<0.05 over the four α tests; the empty/upper-set/non-upper classification runs
  on S_H; the p=0.05-exactly boundary stays null. A-headroom ( §7) recomputed: minimum
  detectable pure-rescue signal 6→8 net items with the arithmetic stated
  ((8,0)→p=0.0078<0.0125 survives; (7,0)→p=0.0156>0.0125 does not). Checklist kill wording:
  "flat-zero = all four Holm-adjusted McNemar p ≥ 0.05 vs C1 + offset null + angular
  null → (c); C3-significant → (r) first." PASS.
- **MAJOR-4 — proposal fidelity.** Dated (2026-09-23) post-acceptance amendment appended to
  the P6 section of `research/innovation/SPRINT_2026-09-23.md`, tagged MAJOR-4, Laws
  #4/#12; the accepted text above it is verbatim-preserved (verified: the original
  experiment sketch, kill criterion, cost, endpoints, and N1 framing are untouched above
  the amendment line); the amendment records (i) the added angular apparatus with rationale,
  (ii) the gated variant's deferral to P5 with rationale, (iii) the narrowed kill. PASS.

### 6.2 MINORs and determinism note

- MINOR-1: "midpoint" gloss gone; α=1.0 re-justified as "one doubling above the null's
  α=0.5" (ABSENT from file ✓). MINOR-2: wall-clock re-anchored to the proposal's rate
  ("≈1.5–2 h", [CONJECTURE]-tagged, proposal-anchored derivation shown). MINOR-3: seeds
  7701/7702 "set immediately before its draws (or via a dedicated torch.Generator)".
  MINOR-4: SHA-256 TBR resolved with EXP067's registered hash `4c242d9a…5ed48dd` (sanity
  check; binding guard remains runtime pre/post match). MINOR-5: EXP075-style multiplicity
  disclosure paragraph added to §8 (angular conjunctive FWER≈0.0025; radial Holm-gated;
  offset single test; motivation-grade claims). MINOR-6: singleton-upper-set softening
  present in both §1.2(b) LICENSES and §8 ("consistent with, not proof of, monotonic
  scaling"). §3.4 [DETERMINISM] note present: the |cos(r,v̂)|<0.5 assert is a deterministic
  function of pinned seed 7702, verified at bundle construction (CPU, pre-runtime), never
  discovered at execution time. All PASS.

### 6.3 Stale-reference sweep (re-verifier's own grep)

Absent from the spec: stale precedence `(d)>(a)>(b)>(c)` (compact and spaced forms),
"midpoint", "TBR", "30–45 min" / "30-45 min", "6 net items", unadjusted `S = {`
definitions, unadjusted "all four McNemar p ≥ 0.05" kill wording (the one match is
Holm-adjusted). The checklist retains the restored "sweep qualifiers carried unlaundered"
item. New precedence strings present in §8 and checklist. No stale reference survives.

### 6.4 Ruling on the fixer's flagged asymmetry (MAJOR-2 scope vs (a)'s generalizing license)

**The question:** (c)'s kill is now radius-bound "at ρ=30°" in the sentence, while (a)
CONE-WINS licenses "the rescuing region extends beyond the single line" from a positive
at the same ρ=30° — a positive generalizes while the kill does not. Is this legitimate,
or does (a) need the same qualifier for symmetry?

**RULING: the asymmetry is scientifically legitimate; no fix required.** Three reasons:

1. **Existential vs universal.** (a) makes an *existential* claim: there exists at least
   one direction off the line (within the tested ρ=30° cone / a tested scale / the
   offset direction) that rescues. "The rescuing region extends beyond the single line"
   IS the observed datum restated — a cone direction with 0<φ≤30° rescued where the line
   did not. Existential claims are supported by a single instance; they do not generalize
   beyond their own scope because their scope is the instance. (c)'s un-fixed sentence
   made a *universal* claim ("the cone hypothesis dies for this task" — all cones, all
   radii), which one radius cannot support. The standard logic of falsification —
   existentials are cheap to support and hard to kill; universals are easy to kill and
   hard to establish — is exactly what the two licenses now respect.
2. **(a) already disclaims other radii.** The §1.2(a) DOES-NOT column bars "other models,
   layers, radii, or α grids", and the ruling requires the firing sub-evidence
   (angular/radial/affine) to be named — the license sentence itself anchors "at the
   tested scales". There is no citation-laundering path analogous to the one MAJOR-2
   closed: quoting (a)'s sentence cannot produce a claim about untested radii.
3. **Symmetrizing would mislead.** Forcing "at ρ=30°" into (a)'s license sentence would
   imply the rescuing region is *confined* to ρ=30° — itself an untested universal
   claim. The current wording ("extends beyond the single line — angularly") is the
   honest description of what a positive datum shows.

### 6.5 Sign-off

**SIGN — 2026-09-23.** The draft's banner is updated to
**PRE-REGISTERED (protocol; not yet executed)**. No GPU execution may proceed under this
protocol except as it specifies; any changed design takes the next free number at
pre-registration time. The reviewer's earlier pass-survived battery (§4: partition, M4
checks, assumption labeling, falsifiability, budget, numbering, Law #13, anti-cheat,
B_agg formula, metaphor audit) stands unre-opened — the fixes added nothing it covered.

*This re-verification changes no primary artifact. Log: LOG-106.*
