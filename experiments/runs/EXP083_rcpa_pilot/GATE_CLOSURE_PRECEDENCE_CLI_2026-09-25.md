# Gate-closure record — EXP083 flip-row precedence + CLI verification (2026-09-25)

GPU-queue readiness lane, 30-day campaign. Both inspections executed on
the CPU build machine ($0, no weights touched). The signed protocol was
not modified.

## Gate 2 — flip-row precedence inspection: CLOSED (conforming)

Inspected `exp083_endpoints.py::adjudicate_verdict` against the signed
protocol §8 + M1 verdict-precedence order and the BUILD_NOTES R2 reading.
Adversarial probes executed (all from the bundle's own code path):

| Probe | Expected (protocol) | Observed |
|---|---|---|
| MDE anchor b=6,c=0,N=57 | CONTINUE (§8 pin) | CONTINUE — two-sided CI (0.0355, 0.2112) straddles +0.05 yet CONTINUE fires: R2 reading confirmed (CONTINUE's conjuncts sufficient, not demoted to HELD) |
| b=c=0 + G-static fired | RE-SKIN KILL (validated apparatus) | RE-SKIN KILL |
| b=c=0, N=57, no static | KILL_flat (one-sided upper 0.045315 < 0.05) | KILL, U_1s=0.04531478 ✓ canonical |
| b=0,c=8 | KILL_gross (CI entirely below +0.05) | KILL, CI upper −0.0684 ✓ |
| b=2,c=1 straddle | HELD | HELD |
| SHA fail + static + MDE data | INVALID(i) preempts all | INVALID, INVALID(i) recorded |

Mutual-exclusion verified by construction: KILL_gross (U<0.05) implies
d̂<0.05 so CONTINUE (d̂≥0.05) is disjoint; KILL_flat (b=c=0) gives
d̂=0, p=1.0, disjoint from CONTINUE. HELD is a true catch-all — fires
only when no kill row and no CONTINUE fired. Implementation order
INVALID(i)→(ii)→(iii) → RE-SKIN → KILL_gross → KILL_flat → CONTINUE →
HELD matches the manifest's `verdict_precedence` and the protocol's M1.

One nuance recorded (not a defect): the protocol §8 header lists the
flip rows as "(RE-SKIN, KILL_gross, KILL_flat, HELD, CONTINUE)" while the
adopted order is CONTINUE before HELD. Harmless: the rows are mutually
exclusive, so the listing order cannot change any adjudication.

## Gate 3 — CLI verification: CLOSED

`run_exp083.py` exit codes verified (no pipes, genuine `$?`):

| Invocation | Output | Exit |
|---|---|---|
| `--smoke` | `EXP083 SMOKE: OK` (19/19) | 0 |
| `--run` (no clearance) | `REFUSED: --run requires --gpu-clearance ... Nothing was executed.` | 2 |
| `--run --gpu-clearance` (no torch on build machine) | `REFUSED: torch is not installed ...` | 2 |
| (no args) | help + "No mode selected. Use --smoke ..." | 2 |
| `--bogus` | argparse error | 2 |

Refusal gates confirmed: no GPU execution path is reachable without
`--gpu-clearance`, and the GPU path additionally refuses off-node (no
torch). The `PROTOCOL` path constant resolves to the signed protocol
file. Manifest `protocol_sha256_prefix` (8a76834b42d9ef20) matches the
recomputed SHA-256 of the signed protocol.

## Remaining

Gate 4 (independent Law #14 bundle review) — commissioned separately;
its verdict is binding and outside this lane's authority.

*— GPU-queue readiness lane, 30-day campaign, 2026-09-25.*
