# CLLC Pre-Registration Requirements Checklist — Draft v1

**Status:** DRAFT for Law #14 review. Not a signed pre-registration.
**Date:** 2026-09-24. **Author:** prior-art verification agent (per founder 24/7 order — second wave, no idle gap).
**Cost:** $0, CPU only.
**Purpose:** the five mandatory items that must ALL be satisfied before CLLC (EXP-CLLC-01
per `research/theory/CLLC_FORMALIZATION_2026-09-23.md` §8) may be registered as a
novelty-bearing pivot. Each item names its gate status, its evidence, and the exact
action that unblocks it. Registration additionally requires K2's P2 gate firing
(the §8 trigger).

---

## Item 1 — Steering Vector Fields identity (VERIFIED — gate CLEAR)

**Requirement:** a retrieved, citable primary-source identity for the mandatory novelty gate.

**Status:** CLEAR (LOG-277).
- Title: *Steering Vector Fields for Context-Aware Inference-Time Control in Large Language Models*
- Authors: Jiaqian Li, Yanshu Li, Kuan-Hao Huang
- arXiv:2602.01654 (cs.CL); submitted 2 Feb 2026, revised 19 Sep 2026 (v2)
- URL (from tool result): https://arxiv.org/abs/2602.01654
- Mechanism: learned differentiable concept scoring function; steering direction = its local gradient at each activation; context-dependent; coordinated multi-layer; multi-attribute.
- **No-kill ruling:** SVF is a learned state-dependent steering law (no setpoint, no error signal, no observer, no tracking bounds) — it does NOT implement closed-loop feedback control and does not occupy CLLC's narrowed slot (Jacobian-free ∧ partially-observed ∧ low-rank feedback). It becomes a **forced comparator candidate** at registration.
- Code repo: none listed on arXiv page — UNVERIFIED/absent, not invented.

**Unblock action:** none remaining. (G4 record-correction proposal in LOG-250 is a separate user-sign-off item; it does not block registration.)

---

## Item 2 — Activation-LQR verification (VERIFIED — gate CLEAR)

**Requirement:** primary-source confirmation of the direct prior art's mechanism class, for the (C)-vs-(D) contrast.

**Status:** CLEAR (LOG-277; re-fetched 2026-09-24).
- Title: *Local Linearity of LLMs Enables Activation Steering via Model-Based Linear Optimal Control*
- Authors: Julian Skifstad, Xinyue Annie Yang, Glen Chou
- arXiv:2604.19018; submitted 21 Apr 2026 (cs.LG/cs.AI/cs.SY); ICML 2026 proceedings listing records-verified (not re-fetched today)
- Closed-loop: YES (explicit). Jacobian-based: YES (layer-wise Jacobians, LTV model, LQR). Actuates: activations (not weights, not text). Tracking-error bounds: derived. Tasks: toxicity/truthfulness/refusal/arbitrary concepts — behavior steering, not relational cognitive tasks.
- Code URL from abstract: https://github.com/trustworthyrobotics/lqr-activation-steering — liveness UNVERIFIED (not fetched).

**Unblock action:** none remaining for the mechanism facts. (Repo fetch, if needed for (D)'s Jacobian cost, is a Law #14 open item in the accounting draft.)

---

## Item 3 — Matched compute/information accounting (DRAFT — Law #14 review pending)

**Requirement:** an operational definition of "matched compute" and "matched information" such that the (C)-vs-(B2) and (C)-vs-(D) contrasts cannot be decided by reviewer discretion.

**Status:** DRAFT DELIVERED, awaiting Law #14 review (`research/analysis_plans/CLLC_ACCOUNTING_DRAFT_2026-09-24.md`, LOG-277).
- Compute unit: FPE (forward-pass-equivalent) per instance, online vs amortized kept separate.
- Per-arm FPE ledger (formulas): (A)=1, (B)=1, (B2)=2, (C)/(C8)=2, (D)=1+Jacobian ledger+Riccati solve, (E)=2.
- Compute-matched: FPE ratio within pre-registered τ (draft: 0.25); beyond τ → asymmetric comparison with the efficiency ratio as primary instrument. (D) expected asymmetric: publish ρ = FPE_D/FPE_C.
- Information ledger: observation rank (scalar/rank-8/full-state), Jacobian access (none < full, strict for C-vs-D by construction), dynamics model, shared reference construction (isolates the controller from the setpoint), controller form. "Strictly less information/compute" formally defined.

**Unblock action:** Law #14 review to ratify or replace τ and η*, confirm harness FPE calibration, confirm (D)'s Jacobian cost, confirm probe label-hygiene.

---

## Item 4 — Operationalized "competitive" criteria (DRAFT — Law #14 review pending)

**Requirement:** a statistical definition of "competitive" / "beats" / "dominated" with no words doing the work of numbers.

**Status:** DRAFT DELIVERED, awaiting Law #14 review (same file, §3–§3.1, LOG-277).
- Primary endpoint: decision-flip rescue rate vs (A); McNemar exact; Tango 95% CI; δ_min = 0.05 (binding stats revision).
- (C) beats (B2) ⟺ L(Δ̂(C,B2)) > δ_min. Indistinguishable / dominated / underpowered cells defined; underpowered = Inconclusive (hold, never license).
- Efficiency ratio η = (ΔM_C/FPE_C)/(ΔM_D/FPE_D); pre-registered η* = 1.0 (draft).
- Full between-the-arms KILL/CONTINUE/PIVOT/HALT decision table pre-registers every cell — this is the G3 resolution.

**Unblock action:** Law #14 review (same as item 3).

---

## Item 5 — Fresh Law #14 review slot (NOT YET SCHEDULED)

**Requirement:** the complete registration package (items 1–4 plus the §8 EXP-CLLC-01 skeleton) passes adversarial review as a fresh object before signing.

**Status:** PENDING.
**Unblock action:** schedule Law #14 review once (a) K2's P2 gate fires (the §8 trigger — registration is conditional and cannot precede it), and (b) items 3–4's draft parameters (τ, η*, FPE calibration) are finalized. The review must treat the package as a fresh object per the LOG-193/V-record rule: the SVF and A-LQR verifications above are fresh (2026-09-24 primary-source fetches). **Freshness rule** [FIX-LOG-285, draft proposal for the review to ratify]: primary-source records are re-fetched at review time if ≥90 days have elapsed since the last fetch, or sooner if the record's publication status is known to have changed (new version, venue change, retraction). Until the review ratifies this, the working assumption is the 2026-09-24 fetches stand for a review held before 2026-12-24.

---

## Registration readiness summary

| # | Item | Status |
|---|---|---|
| 1 | SVF identity | CLEAR (primary source) |
| 2 | Activation-LQR verification | CLEAR (primary source) |
| 3 | Matched compute/information accounting | DRAFT — Law #14 pending |
| 4 | Operationalized "competitive" criteria | DRAFT — Law #14 pending |
| 5 | Fresh Law #14 review slot | PENDING (blocked on P2 gate) |

**External blockers (not CPU-workable):** K2's P2 gate must fire; user sign-off on the LOG-250 G4 record correction (does not block registration itself).
