# COMPUTE PLAYBOOK — SCBI free-tier stacking plan (LOG-202)

**Date:** 2026-09-23 | **Author:** Track 6 (systems/compute) | **Status:** operational playbook (not a signed protocol; amendable by the CEO)
**Epistemology:** every load-bearing claim carries [FACT]/[INFERENCE]/[HYPOTHESIS]/[CONJECTURE]/UNVERIFIED. Mapping to repo `AGENTS.md` §5: [INFERENCE] = [INTERPRETATION], [ESTIMATE] = [CONJECTURE]. Terms verified by web search today are [FACT — web-verified 2026-09-23]; single-source or contradictory items are tagged UNVERIFIED per Law #3 rather than guessed. (Counting method, Law #14 LOG-203 F-202-2: 20 UNVERIFIED tags counted; the §0 definitional line above is excluded from the count.)

**Law #15 coverage (Q4):** n/a — this is an operational document, not an experiment. No GPU was spent, no weights touched, no signed files edited. Stated honestly per the task.

---

## 1. Verified landscape (September 2026)

### 1a. Kaggle — PRIMARY LANE (current platform, keep)
| Attribute | Term |
|---|---|
| GPU quota | **30 GPU-hours/week, shared pool across T4×2 and P100** [FACT — web-verified 2026-09-23, multiple 2026 sources incl. Kaggle-efficient-GPU-usage docs] |
| Quota reset | Weekly; Monday vs Sunday UTC **conflicts across sources — UNVERIFIED** |
| Session length | **12h wall-clock for GPU sessions** (9h for TPU) per Kaggle docs [FACT]; one third-party skill doc says 9h — **conflict, UNVERIFIED, but 12h is the docs-backed figure** |
| Idle timeout | **UNVERIFIED** — two official Kaggle pages reportedly conflict (60min vs 20min) |
| GPU types | Auto-assigned: **T4×2 or P100** per notebook [FACT]. Third-party 2026 report: P100 (sm_60) cannot run Kaggle's Python 3.12 + current PyTorch — **UNVERIFIED from official docs; treat as a caution, not law** |
| Disk | 20 GB writable at `/kaggle/working` [FACT] |
| Gate | **Phone verification required** for GPU + internet in notebooks [FACT — web-verified 2026-09-23; the user's account is already verified since the lab runs here] |
| TPU pool | **TPU v3-8, ~20h/week, separate pool** [FACT] — CUDA/torch stack untested on it; evaluated-not-now |
| No card | No credit card required [FACT] |
| Billing nuance | A 1h T4×2 session burns **1 GPU-hour of the 30h pool** (wall-clock, not per-GPU) [INFERENCE from the shared-pool description — treat as working rule, UNVERIFIED at billing granularity] |

### 1b. Google Colab free tier — SECOND LANE (overflow)
| Attribute | Term |
|---|---|
| GPU | **T4, ~15 GB VRAM**, dynamically allocated [FACT — web-verified 2026-09-23] |
| Session cap | **12h hard cap** [FACT]; idle timeout **~90 min** [FACT, multiple sources] |
| Quota | **No published quota** — Google states usage limits are dynamic and unpublished [FACT — official Colab FAQ]. Third parties report ~100 compute units/month and ~4–5h effective before forced disconnect — **UNVERIFIED (single/third-party sources); plan on it being lumpy, not on the numbers** |
| Gate | **User's own Google account sign-in only; no card** [FACT]. Agents never touch it |
| Disk | ~78 GB ephemeral; Drive mounting required for persistence [FACT] |
| Verdict | Keep as lane 2 for overflow and parallel runs. Not a substitute for Kaggle's predictable 30h/week |

### 1c. Lightning AI free tier — BURST LANE (once-off big gates)
| Attribute | Term |
|---|---|
| Free credits | **15 credits/month, no credit card** [FACT — web-verified 2026-09-23; official pricing page says "No credit card. No commitments."] |
| Conversion | **Conflicting reports: ~22 T4-hours/month vs ~75 T4-hours/month (T4 row of official table)** — UNVERIFIED; the discrepancy is recorded, not resolved |
| GPU types | T4 typical; L4/L40S/RTX Pro 6000/A100/H100 at fewer hours [third-party, UNVERIFIED] |
| Session | Free Studio auto-restarts every ~4h [third-party, UNVERIFIED]; persistent storage + background execution are the lane's actual strengths [INFERENCE] |
| Verdict | Burst lane for single kill/pivot-deciding runs (e.g., powered N=100 re-registration, CLLC 410m). Do NOT burn on routine sweeps |

### 1d. Hugging Face ZeroGPU — INFERENCE-ONLY MICRO-PROBE LANE
| Attribute | Term (official docs, web-verified 2026-09-23) |
|---|---|
| Free quota | **5 GPU-min/day per account** (H200 dynamic allocation); quota resets 24h after first GPU use [FACT — huggingface.co/docs/hub/en/spaces-zerogpu] |
| Cap | **Max 2 ZeroGPU Spaces** for free accounts in good standing (verified email, account >30 days) [FACT — official docs] |
| Limits | Duration billed at 2× on some paths (a 45s task consumes 90s); no `torch.compile` (AOT only); possible **undocumented ~3 runs/day limit** per April 2026 HF forum — **UNVERIFIED, docs don't show it** |
| Verdict | Inference-only probes that fit Gradio-shaped apps and ≤5 min/day: architecture smoke probes, single-prompt checks, demo serving. NOT for batch experiments |

### 1e. Other avenues evaluated
| Avenue | Finding |
|---|---|
| **Paperspace Gradient** | Free tier reported (M4000, 6h auto-shutdown, 5GB) [third-party 2026-07 — UNVERIFIED from official docs]. Weaker GPU than T4; park as backup-only |
| **Modal Starter** | $30/mo recurring credit (~37–51 T4-equiv hours) BUT a payment method may be required on file — **excluded by the no-card constraint until independently verified otherwise** |
| **GCP $300 trial** | Officially **cannot attach GPUs during Free Trial status** (per docs via third-party — UNVERIFIED by direct fetch; treated as out until proven) — out |
| **AWS Educate / Azure for Students** | $100–$500 student credits [third-party — UNVERIFIED]; card-bearing cloud accounts — out under no-card constraint |
| **SageMaker Studio Lab** | **CLOSED to new customers effective 2026-07-30** [FACT — official AWS docs text]. Dead end; do not pursue |
| **NVIDIA Academic Hardware Grant** | Full-time faculty at PhD-granting institutions only — user is a student. **Not now** (revisit if a faculty collaborator joins) |
| **NSF ACCESS / NAIRR / NVIDIA Applied Research Accelerator** | US-institution PI or organization-deployment eligibility. **Not now** |
| **HF GPU community grants** | Possible later for a public demo Space; requires application + justification. **Not now** |

**Bottom line [INFERENCE]:** the $0 stack is Kaggle (primary, 30h/wk) + Colab (second lane, user-action) + Lightning (burst, user-action) + ZeroGPU (micro-probes, user-action) + local CPU (audits/proofs). Nothing else is usable without cards, applications, or faculty status.

---

## 2. Platform × experiment-class mapping

| Experiment class | Lane | Rationale |
|---|---|---|
| Weight-only audits (G1-style), K1 ($0 re-analysis), anisotropy/template-contamination analyses, CPU construction audits, analytical proofs, Law #14 reviews | **Local CPU** | $0, instant, Δθ=0, no quota burned. Everything that doesn't need a forward pass lives here |
| 410m-scale sweeps ≤ ~2,000 passes (EXP080: 1,320; EXP081: 660; K2: 180; K3 test: ~400; Sprint-3 Stage-0 pilots: ~0.05 T4-h total) | **Kaggle T4×2** | Each run is minutes; 30h/week covers the entire licensed falsification sequence (~1.6h worst-case) several times over |
| Second-lane overflow / parallel runs (re-runs, parallel pilot batches) | **Colab T4** (after user enables) | Absorbs overflow so Kaggle quota never blocks a gated run |
| Powered N=100 re-registrations (~1–2k passes), CLLC 410m pilot, DPRS build | **Kaggle week-2 quota or Lightning burst** | Licensed only by verdicts (row 9 of the paradigm-audit sequencing table); Lightning's burst lane is the escape valve if both Kaggle and Colab are drained |
| Single kill/pivot-deciding runs needing A100-class or >4h sessions | **Lightning AI** (after user signs up) | 4h Studio restart limit caps session length; spend only on runs whose verdict changes the program's direction |
| Gradio-shaped inference-only probes (≤5 min/day, no batch) | **HF ZeroGPU** (after user verifies account) | Architecture smoke probes, prompt-level checks, demo serving |
| Retired designs: EXP068 as-signed (~93k passes, dead-room pool, N=45 underpowered), static-geometry L20 variants (killed by EXP077 branch (c)) | **NO HOURS, any lane** | Shelving is per Law #8/#15; resurrection only by new evidence meeting the item's own pre-registered bar |

**Throughput basis for all costings [FACT]:** ~22 forward-passes/s on pythia-410m, 2×T4 (paradigm-audit sequencing table). 1,320 passes ≈ 60 s ≈ 0.02 T4-h.

---

## 3. Quota bookkeeping rules

**Ledger:** `research/innovation/QUOTA_LEDGER.md` (created alongside this playbook; append-only).
**Format per entry:** `| date | booking_id | platform | experiment | passes_planned | T4-h_booked | T4-h_actual | CEO_clearance_ref | status |`
Statuses: `booked` → `running` → `spent` (+`void`/`refunded` for aborted runs).

**Rules (binding):**
1. **No run starts without a booked quota entry** naming the experiment, the pass count, and the lane. Unbooked execution is a process violation (same class as the EXP079 probe-feasibility gap).
2. **No GPU run without CEO GPU clearance**, recorded as the clearance ref in the ledger. EXP080/081 remain gated on the LOG-197 verdict + CEO clearance (adopted gate).
3. **Only the Research Lead may book**; only executor agents run booked entries; only the CEO may clear or void. Agents never self-authorize.
4. **Book with headroom:** booked T4-h = ceil(2.5 × estimate) for sweeps (the smoke-test gate lesson: first-try failures burn quota); actuals are reconciled against bookings weekly, and systematic over/under-estimates feed back into the next booking.
5. **Weekly reconciliation:** every Sunday, the Lead reconciles all five lanes against their sources (Kaggle usage page, Lightning credit balance, ZeroGPU billing page, Colab observed behavior) and appends a dated reconciliation note.
6. **Reserve is not spend:** the ~27–28h held for verdict-licensed work is recorded as `reserved`, not available. Release requires a battery verdict or CEO order.

---

## 4. The next 30 GPU-hours — sequenced spend plan

**Precondition (already true):** LOG-197 executes on CPU, $0. Nothing below runs until its verdict lands + CEO clearance is booked in the ledger.

**Ordering note:** this sequence follows the CEO's LOG-202 instruction. LOG-198's DIRECTION_DECISION listed K3 before EXP080; the logical conditionality is preserved either way — K1 ($0, runs first) gates K3 (does not run if K1 confirms tilt) and gates the interpretation of Sprint-3 Stage-0 pilots. No GPU hour is booked before K1's verdict is on record except EXP080/081, whose gates are the LOG-197 verdict + CEO clearance.

| # | Run | Passes | T4-h (est → booked) | Lane | Status |
|---|---|---|---|---|---|
| 0 | K1 (readout-tilt falsification) + anisotropy analyses | 0 | 0 | CPU | **RUN NOW** — $0, logically prior to all GPU spend |
| 1 | **EXP080** — G2 oracle ceiling, Phase A (pre-registered LOG-172) | 1,320 | 0.02 → **0.05** | Kaggle | First GPU run after LOG-197 verdict + CEO clearance |
| 2 | **EXP081** — C-A donor transfer v2 (pre-registered LOG-182) | 660 | 0.01 → **0.03** | Kaggle | Second GPU run; same gate |
| 3 | **Sprint-3 Stage-0 pilots** (S3-1..S3-6, feasibility checks first — attention/residual snapshots, α-sweep ledger are $0) | ~0.05 T4-h total | 0.05 → **0.10** | Kaggle | Interpretation gated on K1 verdict (S3-1/S3-4 positive class) |
| 4 | **K3** — Law-#7-compliant bridge test | ~400 test + CPU build | 0.02 → **0.05** | Kaggle | **Conditional:** CPU construction audit passes AND K1 did not confirm tilt |
| 5 | CLLC 160m pilot (replacement big bet) | ~600–1,000 [ESTIMATE] | 1–2 → **2.00** | Kaggle/Colab | Pilot-licensed only (κ bound-check gate) |
| — | **Booked total** | — | **~2.25 h** | — | — |
| — | **Reserve (verdict-licensed only)** | — | **~27.75 h** | Kaggle/Colab/Lightning | Released only by battery verdicts (K1–K3, EXP080/081, CLLC pilot) or an L2-licensed powered re-registration (N=100, ~1–2k passes) |

**What does NOT get GPU hours:**
- **EXP068 as-signed** (~93k passes worst case; ~1.2h of pure forward-pass time at 22 fwd/s, but ~13h worst-case wall-clock once adaptive-loop overhead, session restarts, and re-run budget are folded in — Law #14 LOG-203 N-202-1): shelved per Law #15; dead-room pool; would not fit a 12h session worst-case anyway. Replacement bets (DPRS output-room loop gated on EXP080 bin(ii)>0; CLLC pilot) only.
- **Static-geometry variants at L20** (cone angles, offsets, radial grids): EXP077 branch (c) killed them — ΔM=0, p=1.0 throughout. Dead room.
- **Anything at N≤80 claiming a Level-2 verdict:** the MDE headline is binding — such spend buys nothing adjudicating. L2 requires a powered N≈100 re-registration licensed by verdicts.
- **Routine sweeps on the Lightning burst lane** or **batch jobs on ZeroGPU**: wrong lanes; burn rate mismatch.

---

## 5. Single clear user-action request

The user is asked to do exactly the following — and nothing else. **Agents never sign in, create accounts, or handle credentials; the user performs each action themselves and confirms back.**

**Action 1 — Colab second lane (highest value):** Sign in to your own Google account at colab.research.google.com, open the smoke-test notebook the Research Lead will prepare, set Runtime → Change runtime type → **T4 GPU**, run the smoke cell, and report back: (a) which GPU was assigned, (b) whether the session survived a short idle gap, (c) any quota/usage-limit message shown. Expected time: ~10 minutes.

**Action 2 — Lightning burst lane:** Sign up for the **free tier** at lightning.ai (no credit card required — the pricing page confirms this), then report back: (a) the visible monthly credit balance, (b) which GPU types are offered to you. Do not create studios or launch anything. Expected time: ~5 minutes.

**Action 3 — ZeroGPU micro-probe lane:** Create (or verify) a free Hugging Face account and confirm: (a) the email is verified, (b) whether your account is older than 30 days (2-ZeroGPU-Space cap applies to accounts >30 days in good standing). Nothing else needed now. Expected time: ~5 minutes.

**What the user must NOT do:** share passwords, tokens, or codes; add any card; upgrade to any paid tier; approve anything not listed here. If a platform demands a card to proceed, stop and report back — that lane is then excluded under the no-card constraint.

**Standing note:** when the user confirms each action, the Lead verifies the lane with a smoke test (a 60-second notebook for Colab; credit-balance read for Lightning; a 10-second Gradio probe for ZeroGPU) before any experiment is booked against it.

---

## 6. Law #15 — the four answers

- **Q1 (what's the verified landscape + playbook):** §1 verified September 2026 by web search — Kaggle 30h/wk primary; Colab free (T4, 12h sessions, dynamic unpublished quota) second lane; Lightning 15 credits/mo burst lane (exact T4-hour conversion UNVERIFIED); HF ZeroGPU 5 min/day free inference; CPU lane for all audits/proofs; everything else excluded (SageMaker Studio Lab dead 2026-07-30; cards/faculty/applications out). §2 maps every experiment class to a lane.
- **Q2 (CONTINUE — what gets the next GPU hour):** after the LOG-197 verdict lands + CEO clearance: EXP080 (1,320 passes, 0.05h booked), then EXP081 (660 passes, 0.03h), then Sprint-3 Stage-0 pilots (0.13h, headroom rule applied), then K3 (0.05h, conditional on K1 not confirming tilt), then the CLLC 160m pilot (2.00h, pilot-gated). Total booked ≈2.26h; ~27.74h held in reserve for verdict-licensed work only. EXP068 as-signed and static-geometry variants get nothing.
- **Q3 (cheapest possible):** this deliverable cost $0 — web verification only, docs-only, no compute, no sign-ins, no accounts touched.
- **Q4 (n/a):** stated honestly — this is an operational document, not an experiment; no GPU was spent and no weights were touched.

---

## 7. Open uncertainties (recorded, not resolved)

1. Kaggle quota reset day (Monday vs Sunday UTC) — UNVERIFIED.
2. Kaggle idle timeout (60min vs 20min conflict) and 9h-vs-12h session cap — UNVERIFIED.
3. Lightning 15 credits → T4-hours/month (22 vs 75) — UNVERIFIED; official table favors the higher figure but the lower is widely cited.
4. Colab free monthly compute units (~100) and effective per-session duration (~4–5h) — third-party only, UNVERIFIED; Google's stance is "dynamic and unpublished."
5. HF ZeroGPU undocumented ~3-runs/day limit (April 2026 forum) — UNVERIFIED; official docs show only the 5-min/day quota.
6. GCP Free Trial GPU exclusion not directly re-fetched from GCP docs — treated as out pending proof otherwise.
7. TPU v3-8 20h/week lane: untested for our torch/CUDA stack — evaluated-not-now, not booked.

---
*LOG-202 deliverable. Ledger: `research/innovation/QUOTA_LEDGER.md`. Amendments by the CEO only; this is operational (not a signed protocol) and does not require Law #14 to revise.*
