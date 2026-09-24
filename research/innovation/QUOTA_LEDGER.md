# GPU QUOTA LEDGER — SCBI program

**Authority:** `research/innovation/COMPUTE_PLAYBOOK_2026-09-23.md` §3 (binding rules).
**Rule:** no run starts without a booked entry here + CEO GPU clearance. Only the Research Lead may book; only the CEO may clear or void.
**Statuses:** `booked` → `running` → `spent`; `void` / `refunded` for aborted runs.
**Reconciliation:** every Sunday, the Lead reconciles each lane against its source (Kaggle usage page, Lightning credit balance, ZeroGPU billing page, Colab observed behavior) and appends a dated note.

## Law #15 answers for this ledger (binding, on record — Law #14 LOG-203, fix F-202-1)

1. **Precise question:** which GPU bookings exist, in what state, against what quota — the booking-integrity record.
2. **Decision changed:** KILL/CONTINUE for any unbooked or uncleared GPU run — no run starts without a booked entry here + CEO GPU clearance (rule above). The ledger is the enforcement instrument.
3. **Cheapest:** a markdown table, $0. There is no cheaper enforcement mechanism than a written, reconciled record.
4. **Mathematical license:** n/a — operational instrument, stated honestly. (The playbook's §6 carries the landscape record this ledger draws on.)

## Opening balances — 2026-09-23

| lane | quota | notes |
|---|---|---|
| Kaggle GPU | 30 h/week, resets weekly (reset day UNVERIFIED) | T4×2 or P100 per notebook; 20 GB disk; phone-verified account |
| Kaggle TPU v3-8 | ~20 h/week, separate pool | Unevaluated for our stack; not booked |
| Colab free | unpublished dynamic quota, 12h session cap, ~90min idle | Lane locked until the user completes Action 1 |
| Lightning AI | 15 credits/mo (no card), T4-hours/mo UNVERIFIED (22 vs 75) | Lane locked until the user completes Action 2 |
| HF ZeroGPU | 5 GPU-min/day, max 2 Spaces (free, >30-day account) | Lane locked until the user completes Action 3 |
| CPU (local VM) | unlimited, $0 | All audits/proofs/K1 re-analysis |

## Bookings

| date | booking_id | platform | experiment | passes_planned | T4-h_booked | T4-h_actual | CEO_clearance_ref | status |
|---|---|---|---|---|---|---|---|---|
| 2026-09-23 | BK-2026-09-23-01 | Kaggle | EXP080 — G2 oracle ceiling, Phase A | 1,320 | 0.05 | — | pending LOG-197 verdict + CEO clearance | booked |
| 2026-09-23 | BK-2026-09-23-02 | Kaggle | EXP081 — C-A donor transfer v2 | 660 | 0.03 | — | pending LOG-197 verdict + CEO clearance | booked |
| 2026-09-23 | BK-2026-09-23-03 | Kaggle | Sprint-3 Stage-0 pilots (S3-1..S3-6) | ~0.05h-equivalent | 0.13 | — | pending K1 verdict + CEO clearance | booked |
| 2026-09-23 | BK-2026-09-23-04 | Kaggle | K3 — Law-#7-compliant bridge test | ~400 | 0.05 | — | pending K1 not-confirming-tilt + construction audit + CEO clearance | booked |
| 2026-09-23 | BK-2026-09-23-05 | Kaggle/Colab | CLLC 160m pilot | ~600–1,000 [ESTIMATE] | 2.00 | — | pending CLLC pilot gate (κ bound-check) + CEO clearance | booked |

**Total booked:** ~2.26 T4-h (BK-03 corrected 0.10 → 0.13 per Law #14 LOG-203 F-202-3, headroom rule 4). **Reserve (verdict-licensed only):** ~27.74 h — released only by battery verdicts, the CLLC pilot outcome, or an L2-licensed powered re-registration. Recorded as `reserved`, not available.

## Reconciliation log

*(Lead appends a dated note each Sunday.)*
