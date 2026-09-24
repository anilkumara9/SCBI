# Frontier Scoreboard v1 — inference-time computation / steering / capability amplification

*Standing Benchmark Analyst, 2026-09-23. Law #3: headline rows re-verified today via arXiv abstracts; secondary rows carry the synthesis's LOG-185 verification record as provenance (stated per row). Law #15: Q: how far is SCBI from the frontier and what closes the gap? Decision changed: program prioritization. Cheapest path: $0 literature arithmetic. License: comparison bookkeeping (CIs, MDEs, matched-compute budgets) — no new theorem claimed.*

## Reading guide

- **Effect** = the paper's own headline number, with the uncertainty the paper reports. Where the abstract gives no number, the cell says so — never filled from memory.
- **Δθ=0?** = whether the method respects the frozen backbone (no weight updates, no trained components).
- **N** = evaluation sample size where reported; "n/r" = not reported in the source checked.
- Two honest axes exist: **(A)** accuracy gain at matched compute; **(B)** compute saved at non-inferior accuracy. Systems are plotted on the axis their paper claims. Forcing all rows onto one axis would be fabrication.

## The board

| # | System | Venue / status | Task | Model(s) | Effect (paper's own) | N | Compute budget | Δθ=0? | Provenance |
|---|--------|----------------|------|----------|----------------------|---|----------------|-------|------------|
| 1 | **CAA** (Rimsky et al.) | ACL 2024 | Behavioral steering (MCQ + open-ended) | Llama 2 Chat | Not quantified in abstract; "significantly alters behavior, minimally reduces capabilities" | n/r (abstract) | 1 fwd pass + vector add | Yes | Re-verified 2026-09-23 (arXiv:2312.06681 abstract) |
| 2 | **∇-Reasoner** (Wang et al.) | ICLR 2026 | Math reasoning (MATH-500) | Qwen-2.5-7B-Instruct | 71.2% → **80.4%** (LOG-185); abstract: ">20% accuracy improvement", **10–40% fewer model calls** vs strong baselines | n/r (abstract) | Iterative logit-gradient steps + reward model | Yes | Re-verified 2026-09-23 (arXiv:2603.04948 abstract) + LOG-185 |
| 3 | **Activation-LQR** (Skifstad et al.) | ICML 2026 | Toxicity / truthfulness / refusal / concept modulation | Multiple LLM archs/scales | Not quantified in abstract; "SOTA modulation … surpassing baseline steering"; formal tracking-error bounds | n/r (abstract) | Layer-wise Jacobians, "minimal overhead", no offline training | Yes | Re-verified 2026-09-23 (arXiv:2604.19018 abstract) + LOG-185 proceedings check |
| 4 | **Meta-Reasoner** (Sui et al.) | Findings ACL 2026 | Math (Game-of-24, TheoremQA), science (SciBench) | n/r (abstract) | **+9–12% accuracy** over prior SOTA; **−28–35% inference time**, same compute budget | n/r (abstract) | CMAB policy overhead only | Yes | Re-verified 2026-09-23 (arXiv:2502.19918 abstract) |
| 5 | **DEER** (Yang et al.) | arXiv 2025 | 10 reasoning benchmarks (GSM8K, MATH-500, AMC, GPQA, AIME, LiveCodeBench) | 11 cutting-edge LLMs | **−19.1–80.1% CoT length**, **+0.3–5.0% accuracy** | 10 benchmarks | Negative (saves compute) | Yes | Re-verified 2026-09-23 (arXiv:2504.15895 abstract) |
| 6 | **Self-Refine** (Madaan et al.) | NeurIPS 2023 | 7 diverse tasks (dialog → math reasoning) | GPT-3.5 / GPT-4 | **~+20% absolute** avg task improvement over one-step generation | 7 tasks | ~2–3× generation passes (generate→feedback→refine) | Yes | Re-verified 2026-09-23 (arXiv:2303.17651 abstract) |
| 7 | **NoisyCoconut** (Jerge & Evans) | TMLR Jun 2026 | Math reasoning | n/r (record) | Unanimous inter-path agreement → **error <15%** via selective abstention (K=5, σ=0.1) | n/r (record) | K=5 latent branches | Yes | Synthesis LOG-185 (status+mechanism verified 2026-09-23); abstention-gated, not pure accuracy |
| 8 | **RISER** (Ye et al.) | Findings ACL 2026 | Zero-shot reasoning | n/r (record) | **+3.4–6.5% avg** zero-shot accuracy | n/r (record) | Lightweight router (trained) | **No** — trained external router; excluded from Δθ=0 core | Synthesis record |
| 9 | **LTPO** (Ye, Liang & Shan) | arXiv:2510.04182 preprint | Latent thought optimization | Frozen LLM | Effect sizes not extracted in program record | — | Online policy gradient on latent vectors | Yes | Synthesis record; preprint, no venue |
| 10 | **LatentMAS** (Zou et al.) | ICML 2026 spotlight | Latent multi-agent collaboration | n/r (record) | Effect sizes not extracted in program record | — | Shared latent working memory | Yes | Synthesis record |
| 11 | **STARS** (Yang et al.) | arXiv:2605.26733 | Looped-LM stabilization | — | Training framework; no inference-time effect claimed | — | — | **No** — training required | Constraint only: predicts gain-then-collapse for frozen iterative loops |
| 12 | **PPLM** (Dathathri et al.) | ICML 2020 | Controlled generation | GPT-2 | Historical occupant of the dynamic-intervention slot; numbers not re-extracted | — | Gradient-guided hidden-state search | Yes | Prior art; slot occupancy only |

## What the board does NOT let you do

- Compare CAA's behavioral steering to ∇-Reasoner's MATH-500: different tasks, different axes. The board refuses the comparison explicitly.
- Treat NoisyCoconut's <15% error as an accuracy claim: it is abstention-gated (selective prediction), a different measurand.
- Treat RISER/STARS as Δθ=0 competitors: they are excluded by Law #6 / the frozen boundary; listed for honesty, not ranking.
- Quote LTPO/LatentMAS effect sizes: the program record does not contain them. Next re-hire should extract or mark permanently absent.
