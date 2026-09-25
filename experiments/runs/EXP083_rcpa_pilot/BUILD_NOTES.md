# EXP083 BUILD NOTES — LOG-258 assumptions inventory

Every interpretive choice made while building this bundle, and every defect
escalated rather than silently resolved. Nothing here changes the signed
LOG-257 protocol; where the protocol could not be implemented literally on
the CPU build machine, the bundle implements it exactly as written and the
gap is flagged for the CEO.

## 1. Resolved readings (adopted; documented, not silent)

**R1. One-sided McNemar form.** §8 pins "exact one-sided McNemar (binomial)
p ≤ 0.05 in the A_r direction" with the anchor b=6, c=0 → 0.015625. Adopted
reading: the binomial upper tail P(Bin(b+c, 0.5) ≥ b). At b+c=0 this returns
1.0 (no discordant evidence); the b=c=0 worlds are decided by the
KILL_flat/HELD rows, never by this p-value. Integer-exact via
math.comb sums against 2**s — no float pmf.

**R2. Row-vs-row precedence among flip rows.** §8 lists RE-SKIN, KILL_gross,
KILL_flat, HELD, CONTINUE but does not pin evaluation order among the flip
rows. Adopted reading: KILL_gross → KILL_flat → CONTINUE → HELD. This is
forced by the MDE anchor: b=6, c=0 at N_final=57 must adjudicate CONTINUE
(§8's own pin), and a listing-order reading (HELD-straddle before CONTINUE)
could demote a significant directional result to HELD whenever the two-sided
CI straddles. CONTINUE's conjuncts are therefore sufficient for CONTINUE.
The evaluator asserts the anchor case adjudicates CONTINUE.

**R3. Canonical flat tables.** The §8/§13.2 canonical values are reproduced
from cell tables (n11, n12, n21, n22): (60,0,0,0) → 0.043147 / ±0.0602;
(57,0,0,0) → 0.045315 / ±0.0631; (58,1,1,0) → 0.056902. At b=c=0 the
constrained-MLE score depends only on (n, m=n), so any concordant split
gives identical values — verified in-code, not assumed.

**R4. Evidentiary mapping.** §8's row labels are operational verdicts; the
bundle additionally records the program-standard evidentiary verdict:
KILL / RE-SKIN KILL → Not supported; HELD → Inconclusive; CONTINUE →
Inconclusive (licenses a powered pilot only — never a capability claim);
INVALID → Underdetermined. CONTINUE is deliberately NOT "Supported": the
§8 power-gate clause makes this pilot an asymmetric kill/hold instrument.

**R5. G-static on the CPU build machine.** G-static consumes real r̂ vectors
from the clean-read pass (GPU node). Here it is a pure function over unit
vectors, fixture-tested (identical → fires at 1.0; orthogonal → 0.0;
non-unit/wrong-dim/<2 items → ValueError → INVALID(iii) at the call site).

**R6. Throughput gate.** §6's "throughput ≥ 80%" is a live GPU-node
assertion. The bundle encodes the gate function
(measured/projected ≥ 0.80, non-positive projection fails) and
fixture-tests it; the runner evaluates it at startup on the GPU node.

**R7. torch ĝ_i generation.** torch is absent on the CPU build machine.
exp083_random.py separates the testable seed-scheme contract
(20260924+i, distinct, deterministic) from the torch-dependent generation,
which raises a clear RuntimeError off-node instead of silently falling back
(R5 exclusivity is asserted by an import-statement check in the evaluator).

## 2. Verified canonical reproductions (from the bundle's own computation)

| Value | Protocol | Bundle |
|---|---|---|
| one-sided 95% upper, N=60 flat | 0.043147 | 0.043147 (6dp) |
| two-sided 95% CI, N=60 flat | [−0.0602, +0.0602] | matches (4dp) |
| one-sided 95% upper, N_final=57 flat | 0.045315 | 0.045315 (6dp) |
| two-sided 95% CI, N_final=57 flat | [−0.0631, +0.0631] | matches (4dp) |
| one-sided 95% upper, b=c=1 | 0.056902 | 0.056902 (6dp) |
| one-sided McNemar p, b=6,c=0 | 0.015625 | 0.015625 (exact) |
| flat tie edge case, N_final=58 | 0.044568 | 0.044568 (6dp) |
| KILL_flat firing boundary | N_final ≥ 52 | verified (52 fires, 51 holds) |

## 3. Escalated (not silently resolved)

**E1. §A.2.5/§A.2.6 text unretrievable.** The task's smoke-test citation
(§A.2.5/§A.2.6) does not resolve to retrievable text in this workspace
(STATISTICAL_PROTOCOL_V02.md absent; the ambition-sprint §A.2 covers only
§A.2.1). The smoke test is implemented from the protocol's own §6 spec
(9 passes; verdict-path reachability; identity-vs-archive; throughput ≥80%),
which is the binding source. If §A.2.5/§A.2.6 imposes additional smoke
requirements, the smoke test needs a revision pass — flagged, not assumed.

**E2. GPU-node-only paths untested live.** generate_g_hat, the forward-hook
injection, and the tokenizer offset table execute only on the user's Kaggle
node. The bundle's contracts for them are encoded and fixture-tested; a
startup smoke failure on the node blocks execution per §6.

**E3. No weights touched.** The bundle was built and tested with synthetic
fixtures only. The expected model SHA-256
(4c242d9a…48dd) is pinned and asserted; the pre-run comparison is
INVALID(i)-gated.

## 4. Test summary

- test_exp083.py: **92/92 pass** (stdlib only; numpy cross-check conditional).
- smoke_test.py: **19/19 pass** (CPU, synthetic fixtures).
- run_exp083.py --smoke → SMOKE OK; --run without --gpu-clearance → REFUSED.

## 5. Clearance status

Bundle construction complete per the LOG-257 license (evaluator test suite +
startup smoke test). **CEO GPU clearance: NOT granted, NOT requested here.**
Execution remains unlicensed until Law #14 bundle review + CEO clearance.
Queue: behind K2 on the user's Kaggle node (GPU-sequencing only).
