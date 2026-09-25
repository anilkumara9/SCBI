# E1 Resolution — EXP083 smoke-test source retrieval (2026-09-25)

Escalation E1 (LOG-258, BUILD_NOTES.md §3) claimed the §A.2.5/§A.2.6
smoke-test text was "unretrievable in this workspace
(STATISTICAL_PROTOCOL_V02.md absent)". Re-examined 2026-09-25 under the
30-day campaign's GPU-queue readiness lane. Findings:

## 1. STATISTICAL_PROTOCOL_V02.md is NOT missing

The file exists at `experiments/protocols/STATISTICAL_PROTOCOL_V02.md`
(Protocol ID STAT-V0.2, dated 2026-09-11 — predates EXP083). The "absent"
claim was incorrect; the builder evidently searched the wrong location.
Content: seed separation, selection-regret tolerance, Wilcoxon/Cliff's-δ
equivalence standard, best-of-N baseline rule. It is a program-level
standard; EXP083's operative statistics (Tango CIs, one-sided McNemar,
canonical table) are pinned self-contained in the signed protocol §8 —
no missing statistical doc blocks this bundle. Retraction of the
"missing" claim is on record here.

## 2. §A.2.5/§A.2.6 do not exist — the binding smoke spec is §A.2 item 5

No subsections §A.2.5/§A.2.6 exist in
`research/proposals/AMBITION_SPRINT_EXPDESIGN_2026-09-24.md`. The
mandatory startup smoke test is specified at **§A.2 item 5**, retrieved
verbatim:

> **Startup smoke test (mandatory):** ≤12 passes on 3 items covering every
> arm once, asserting (i) the runner reaches the verdict code path, (ii) the
> identity arm reproduces the archived baseline bit-for-bit, (iii) throughput
> ≥80% of the booked model. Three Kaggle startup crashes burned quota — the
> smoke gate is a Law, not a suggestion. Smoke passes count toward the 150
> ceiling.

## 3. Coverage mapping — all three assertions implemented and passing

| §A.2 item 5 assertion | smoke_test.py implementation | Status |
|---|---|---|
| (i) runner reaches the verdict code path | `test_verdict_path_reachability` — synthetic 3-item fixture through positions → guards → flip contrast → `adjudicate_verdict`; asserts a complete verdict record | PASS (19/19, re-run 2026-09-25) |
| (ii) identity arm reproduces archived baseline bit-for-bit | `test_identity_vs_archive` — match → ok; mismatch → INVALID(ii), never a flip verdict; adjudication preemption asserted | PASS |
| (iii) throughput ≥80% of booked model | `test_throughput_gate` — 85% → pass, 79% → fail, non-positive projection → fail (no silent pass); the gate function is encoded, evaluated live on the GPU node at startup | PASS |

Plus (protocol §6): 9-pass smoke inventory within the ≤12 cap
(`test_smoke_pass_inventory`), SHA pre-run check before any pass
(`test_sha_prerun_check_present`), INVALID precedence (i)→(ii)→(iii)
(`test_invalid_precedence_order`), pass-193 hard stop
(`test_pass_193_hard_stop`).

## Disposition

E1 discharged: no unretrievable text; the binding spec was found at §A.2
item 5 and every assertion is implemented, tested, and green. No smoke-test
revision pass required. This document changes nothing in the signed
protocol or the bundle — it is a retrieval/coverage record only.

*— GPU-queue readiness lane, 30-day campaign, 2026-09-25.*
