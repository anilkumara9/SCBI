# Progress Analysis — where SCBI stands vs the frontier (standing; updated 2026-09-28)

*Standing Benchmark Analyst. One page. No softening. Supersedes the
2026-09-23 snapshot (`PROGRESS_ANALYSIS_2026-09-23.md`, preserved as
history). Full evidence: `FRONTIER_SCOREBOARD.md` §3.*

**The frontier, summarized.** In 2025–2026 the field shipped working
inference-time computation on frozen models: ∇-Reasoner (71.2→80.4%
MATH-500, 10–40% fewer calls), LatentMAS (up to +14.6% accuracy, 70–84%
token reduction), Meta-Reasoner (+9–12% accuracy at −28–35% inference time,
same budget), DEER (−19–80% chain-of-thought at +0.3–5.0% accuracy),
Self-Refine (~+20% absolute across 7 tasks), self-consistency (+17.9pp on
GSM8K), LLM-Monkeys (15.9%→56% SWE-bench Lite at 250 samples),
Activation-LQR (closed-loop LQR steering with tracking-error bounds),
NoisyCoconut (<15% error via selective abstention). The bar for
"inference-time compute does something" is high, published, and rising.

**SCBI, summarized.** Zero capability results. The EXP094–103 wave is now
complete and reads as the boundary map: per-item static L11 geometry
refuted by pure inertness (EXP094: 0 flips across 120 injection arms);
the α grid inert at every ratio (EXP095); movement that exists but is not
directionally attributable (EXP096/097/099 — fragility);
the composition premise not supported (EXP098 — random joint moved 12
vs 7 joint); and the {mean,max}×{L11,L20} externally-computed
attention-gate family closed 4/4 (EXP100 mean-at-L11: 0/60 coverage,
untestable; EXP101 max-at-L11: 16/60, 1 flip right→wrong, Refuted; EXP102
mean-at-L20: 1/60, untestable; EXP103 max-at-L20: 55/60, 3 flips p=1.0,
Refuted). The S6-5 pooled audit fixes the program ceiling at 5/381
directional flips (one-sided 95% UB 2.74%). The whole L11-rescue program
was then stood down (LOG-4463/4464): no self-computed-gate design clears
the worth-it gate — the rational update is "the direction is the problem,
not the gate." Ten experiments, ~2,000 CPU passes, $0. The only positive
numbers in the program's history remain the label-assisted bridge rescues,
demoted to rescue controls (LOG-197/204); its best autonomous number is
still +4pp, non-significant (EXP056).

**The gap.** Not a margin — an absence. On accuracy-at-matched-compute and
on compute-saved, SCBI has no entry while the frontier has six systems
plus the 2026 occupants (SVF, A-LQR, LTPO, LatentMAS). Our lead is
boundary science: the static + per-item + externally-gated rescue
program — every tested rescue dead, untestable, or uninterpretable — is
now a *map*, not a single null. That is real and publishable as a
boundary result (the gap analysis flags it as the largest no-new-compute
evidence delta for v83). It is not a capability and does not compete with
any frontier row. The one axis where the frontier is also at zero —
**label-free autonomous steering** — remains the only honest race.

**What closes it.** The §D2 six-condition bar: per-instance construction,
transfer-validated evaluator, matched-compute wins over ∇-Reasoner /
Activation-LQR / Meta-Reasoner / DEER / LatentMAS plus the pinned M15
comparators, conditional-computation proof, specificity gap — at powered
N≈100+. The live lanes toward that bar: the GPU queue (K2 → EXP083 →
EXP084 → EXP086 Stage B → EXP088 → EXP087, founder's Kaggle), and a new
direction family earning its own license (the S6 stand-down pre-registered
the re-opening conditions). The honest base rate, from the synthesis's
own power analysis: at current N the program is a falsification-and-
boundary program. The scoreboard will record a beaten frontier the day the
six conditions are met — and will say "not yet" every day until then.
