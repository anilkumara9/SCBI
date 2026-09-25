# Self-Consistent Basis Invention (SCBI)

**A falsification-first research program asking whether a frozen language model can become more cognitively capable through inference-time computation alone.**

- **Status:** active research program · 70+ experiment runs · 249 research-log entries (as of 2026-09-25)
- **License:** Apache-2.0
- **Paper:** in preparation — boundary/negative-result workshop draft in `reports/paper_draft.md`

---

## The canonical question

> **What discovery would have to be true for a frozen model to become far more cognitively capable through inference-time computation?**

Every experiment in this repository is an attempt to answer that question — or to kill a candidate answer as cheaply as possible.

## The frozen backbone

$$\boxed{\theta_t = \theta_0 \qquad \Delta\theta \equiv 0}$$

Core SCBI experiments never update weights, biases, adapters, or normalization parameters. Every run verifies this with pre/post parameter hashes. If the weights moved, the run is invalid — no exceptions.

---

## What we have established

These are the program's *licensed* findings — each survived independent adversarial review (see [How the lab works](#how-the-lab-works)). Numbers are quoted exactly as logged; the primary artifacts are in `experiments/runs/`.

### 1. The representational–causal dissociation (EXP065 / EXP066)

Raw cross-vocabulary geometric similarity of **~0.7 cosine** does **not** yield causal transfer under static injection. The similarity is real and measurable; it does not move decisions. This replicated across Pythia scale (160M → 410M) with Δθ ≡ 0 strictly verified. It is the program's central boundary result: **decodability is not influence**.

### 2. The concept geometry is not where the leverage is (EXP077)

Four static geometric variants of a concept direction (cone at multiple angles, cone-vs-line, cone-vs-control, offset, radial grid) moved decision accuracy by exactly **Δ = 0 (p = 1.0)** — branch (c) NEITHER. The output-side bridge positive control rescued **+10pp (56.67% → 66.67%, p = 0.03125)**. Licensed reading: the transferable direction lives output-side, not in the concept geometry. The tested unconditional 30° cone and α = 1 offset hypotheses are dead at Pythia-410m/layer 20; gated and conditional variants survive.

### 3. Layer-20 readouts carry no exploitable signal (EXP091) — KILL

Zero-shot cosine-similarity scoring of frozen Pythia-410m layer-20 final-token embeddings on a registered novel relational benchmark: **31/60 = 51.67%, p = 0.449**. Verdict: KILL, independently adopted. There is no decision signal here to exploit.

### 4. Task information localizes to mid-network layers (EXP092) — CONTINUE

Information-bottleneck localization across all 24 layers of frozen Pythia-410m (60 prompts, 60 forward passes, $0 CPU):

- **Layer 11:** leave-one-out 1-NN accuracy **20/60 = 33.3%** vs 5% chance (20 labels), raw permutation **p = 0.000999**, Bonferroni-significant (threshold 0.0020833), **+20pp above the null 95th percentile**
- **8 layers** met both registered bars: {1, 11, 12, 13, 14, 15, 17, 18}
- **Layer 20** (the previously inspected layer): 15%, p ≈ 0.066 — not significant, correctly excluded

Licensed claim: *frozen Pythia-410m layer 11 carries significant task information on the EXP092-B bench.* The independent reviewer recomputed every statistic from the primary embeddings and agreed exactly. Recorded caveat: the signal is phrasing-sensitive (A-first 53.3% vs C-first 13.3%) — any "redirect to layer 11" claim carries that caveat.

### 5. Falsified mechanism candidates

- **G1 (QK/OV projection-energy audit)** — KILL. The "Core Causal Null-Space Theorem" is false as a QK-subspace claim: the failed direction is unusually QK-visible while the working bridge is QK-unremarkable — the exact inversion of the theorem's central sentence.
- **K1 (readout-tilt falsification)** — the tilt charge did not hold (0 of 180 reached the 0.9 bar).

### 6. In flight

- **EXP093 (layer-11 causal transfer)** — the causal counterpart to EXP092's correlational result: inject the layer-11 task direction back into the frozen model during decisions (±v with sign-flip placebo, 180 forward passes, ~15 CPU-min, $0). Pre-registration signed; bundle built and under independent review. Registered prior: the shared-direction hypothesis is *a priori* weak (per-item correction directions ~3% coherent) — KILL is the expected outcome, CONTINUE would be surprising and informative.

### 7. Novelty position

Program synthesis adopted at **N1 — Known Combination**. The tested static mechanism is operator-equivalent to prior art (CAA family). No superhuman, conscious, revolutionary, or autonomous-capability claim is licensed. The summit — frozen models thinking at a human level — is an aspiration that organizes the research, not a result.

---

## What we do NOT claim

Honesty about negatives is the program's core asset. The following are explicitly **not** established and are policed by review:

- **No capability claim.** Nothing here shows a frozen model reasoning better, let alone approaching human-level or superhuman cognition.
- **Decodability ≠ causality.** A probe that reads information out of a layer (EXP092) does not show the model *uses* that information (that's what EXP093 tests).
- **Bridge positives are rescue artifacts.** The output-side bridge that rescues accuracy is a *known-answer direction* — a positive control, not evidence of an autonomous mechanism (standing CEO ruling, LOG-204).
- **Nulls are first-class citizens.** Every kill, halt, retraction, and RUN-INVALID is preserved, logged, and plotted on the frontier scoreboard. Retractions are documented in-paper, not buried.

---

## Repository map

```text
SCBI/
├── theory/                  # Definitions, assumptions, formulation, algorithm,
│                            # complexity, proofs — the mathematical specification
│   ├── README_DEFINITIONS.md # Canonical vocabulary (Law #5: changes need a changelog)
│   ├── README.md             # Mathematical specification
│   └── proofs/               # Procrustes-failure proof et al.
├── research/
│   ├── CAMPAIGN_30DAY.md     # Current autonomous campaign charter (lanes, cadence)
│   ├── GIT_WORKFLOW.md       # Lab git SOP: branches, PRs, review-before-merge
│   ├── CEO_DIARY.md          # Institutional memory of the research program
│   ├── benchmarks/           # Frontier scoreboard: SCBI vs 6 industry
│   │                         # inference-time systems (updated per verdict)
│   └── synthesis/            # A–J and REV2 program syntheses (adopted)
├── experiments/
│   ├── protocols/            # Pre-registrations: DRAFT → Law #14 review → SIGNED
│   │   ├── REVIEWS/          # Independent review verdicts (binding)
│   │   └── *_SIGNED.md       # Immutable once signed (corrections via errata only)
│   └── runs/                # 70+ run directories: bundle + report + artifacts
├── evaluation/              # Metrics, statistical tests, ablations, failure analysis
├── reports/
│   ├── research_log.md      # The chronological record: 249 LOG entries, every
│   │                        # verdict/kill/halt/retraction preserved
│   ├── paper_draft.md       # Boundary/negative-result workshop paper (~5k words)
│   └── mentor_adoption_gate_rev2_2026-09-23.md
├── scbi/                    # Implementation: frozen-backbone runtime, guards
├── scripts/                 # Tooling
├── evaluation/              # Metrics and statistical tests
├── documentation/           # Additional documentation
├── TECHNICAL_STACK.md       # Compute setup: free-tier GPU lanes (Kaggle/Colab),
│                            # CPU-first $0 execution, reproducibility requirements
├── MUSE_HANDOVER_PROMPT.md  # Machine-readable program handover
└── AGENTS.md                # Behavioral constitution: the 14 agent laws
```

### Source-of-truth hierarchy

When documents disagree: `theory/README_DEFINITIONS.md` → `theory/README.md` → `theory/README_ASSUMPTIONS.md` → `research/README_LITERATURE.md` → `theory/README_ALGORITHM.md` → `scbi/README.md` → `experiments/README.md` → `evaluation/README.md` → `reports/README.md`. Primary artifacts outrank summaries; the research log outranks this README.

---

## How the lab works

This repository is run as a continuous research program, not a collection of scripts.

**The launch chain.** No experiment runs without: signed pre-registration → independent Law #14 review → startup smoke test → CEO clearance → execution. Skipping a step invalidates the run.

**Independent review with teeth.** The Independent Scientific Mentor / Adversarial Reviewer reports to the founder, not to the lab's CEO. Its verdicts (SIGN / SIGN-WITH-FIXES / REJECT, and verdict reviews: ADOPT / KILL / CONTINUE / PIVOT / RUN-INVALID) are binding and cannot be overridden or suppressed. Reviews recompute statistics from primary artifacts — twice this program's reviewers have caught degenerate mathematics before a single flop was spent.

**The 14 agent laws** (full text in `AGENTS.md`): read before modifying; never invent results; never fabricate citations; never silently shift hypotheses or definitions; preserve the frozen backbone; zero data leakage; never delete failed experiments; no post-hoc metric cherry-picking; never claim premature novelty; distinguish observation from interpretation; document major decisions; preserve reproducibility; challenge rather than defend.

**Every cycle passes the worth-it gate** (Law #15): precise question → the KILL/CONTINUE/PIVOT decision it changes → the cheapest falsifying test and its cost → the mathematical license with a quantitative prediction and a breaking point. No license, no work.

**Signed protocols are immutable.** Corrections happen through append-only errata or a new experiment number — never silent edits, never force-pushes.

---

## Experiment registry (selected)

| Experiment | Question | Verdict |
|---|---|---|
| EXP065/066 | Does ~0.7 cross-vocab similarity transfer causally? | Boundary: similarity without transfer |
| EXP077 | Does any static geometric variant move decisions? | (c) NEITHER; bridge rescues +10pp |
| EXP079 | HALT probe for adaptive loop | HALT accepted via CPU readiness |
| EXP082 | Foil-suppression tilt | KILL upheld |
| EXP083/084 | Relational amplification; Newton-vs-gradient duel | Signed, queued for GPU |
| EXP086 | Dynamical amplifier (attention non-normality) | Stage A advisory (He ≈ 0.73–0.83, verdict None by construction); Stage B signed, queued for GPU |
| EXP087 | Translation signature | Bundle repaired, CEO-cleared for GPU |
| EXP088 | Recirculation | Queued for GPU |
| EXP089/090 | CLM-8B adaptation | Superseded / RUN-INVALID (tokenization) |
| EXP091 | Layer-20 cosine readout | KILL (31/60, p = 0.449) |
| EXP092 | Information-bottleneck localization | CONTINUE (layer 11, p = 0.000999) |
| EXP093 | Layer-11 causal transfer | In flight (bundle under review) |
| K2 | Routing-contrast bypass | First in GPU queue |
| G1 | QK null-space mechanism | KILL (theorem false as stated) |

The full record — every LOG entry, kill, halt, and retraction — is in `reports/research_log.md`.

---

## Reproducing results

**CPU-first, $0.** Most of the program's decisive results (EXP091, EXP092, G1, K1) ran on CPU with read-only weight access. Each run directory contains its bundle, build notes, and run report; guards (bench pins, weight hashes, thread pins) are asserted at execution time.

**GPU queue.** GPU experiments run on user-owned free-tier hardware (Kaggle/Colab), never on lab infrastructure. Current order: **K2 → EXP083 → EXP084 → EXP086 Stage B → EXP088**. Each has a tested execution bundle and an independent SIGN; execution notebooks live in the run directories (e.g. `experiments/runs/K2_routing_bypass/K2_kaggle_run.ipynb`).

**Reproducibility standard:** pinned seeds, environment manifests, pre/post parameter hashes (Δθ = 0 asserted), raw instance logs preserved. A run that cannot reproduce its guard values is RUN-INVALID, not a result.

---

## Frontier context

`research/benchmarks/` tracks SCBI against six quantitative industry inference-time systems. The honest scoreboard: the frontier holds real capability gains; SCBI holds zero capability entries and one genuine lead — **boundary science** (0.7 cosine with zero causal transfer, replicated, retraction on record). Beating the frontier needs powered N≈100+ evidence — roughly an order of magnitude more than anything produced to date. The scoreboard is updated automatically with every verdict, kills included.

---

## Contributing (lab workflow)

This repo follows lab discipline (`research/GIT_WORKFLOW.md`):

- **Topic branches** per workstream (`exp/093-…`, `review/…`, `docs/…`) — nobody commits to `main` directly
- **Pull requests for everything**, with LOG-linked descriptions and test evidence
- **Review before merge** — research artifacts need an independent Law #14 SIGN
- **Push constantly**; never force-push; never commit secrets, credentials, or model weights

---

## License

Apache-2.0 — see `LICENSE`.

## Citation

Paper in preparation. Until publication, cite the repository and the research log:

> SCBI Research Program, *Self-Consistent Basis Invention: boundary science for frozen-model inference-time computation*, GitHub repository, 2026. Experimental record: `reports/research_log.md`.
