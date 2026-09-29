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
evidence delta for v84 — current release candidate, superseding v83 per
LOG-4519; v84 = v83 + converging-evidence related work + O1/O2 polish).
It is not a capability and does not compete with
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

---

## The I2′ line (opened and CLOSED 2026-09-28) — selection-failure instrumentation

**Terminal state.** I2′ answered EXP085's death-debt question — are
selection failures measurable and repairable? — with a complete
falsification-terminal arc in one day. Chain: S4-8 pre-registration
SIGNED (LOG-4480) → EXP104 Tier-0 executed (LOG-4481/4482) → HOLD →
Inconclusive (0.1833 < 0.25 bench sanity; premise bars met, battery NOT
run) → bench autopsy (LOG-4483): the HOLD was a position-A prior —
30/60 top-1 at position 0, p=2.02e-12 — format-driven, an instrument
confound not a premise kill → S4-8′ cloze recalibration SIGNED
(LOG-4488) → **EXP105 Tier-0 PASSED (LOG-4489)**: baseline 32/60 =
0.5333 inside [0.25, 0.75] (NOT line-closed), median correct-rank on
failed items 4.0 ≤ 5, n_pop 21 ≥ 12, tie-guard 0.0 — the cloze format
rescued measurability (0.1833 → 0.5333) and confirmed the A-prior
diagnosis: the prior was a readout-format artifact, not a knowledge
absence → **EXP105 battery Refuted at step 9 (LOG-4491)**: ΔM_T =
+0.2381 (5/21 rescues) vs ΔM_R = 0.0000 (0/21, perfectly flat) — clean
direction — but the primary T-vs-R McNemar-exact p=0.0625 ≥ 0.05,
missed CONTINUE by exactly one flip; foil–top-1 overlap O = 0.571 > 0.5
→ F arm non-diagnostic, exactly as the pre-registered N1 amendment's
O ≤ 0.5 gate anticipated (validated design lesson). Pre-registered stop
rules closed the line: no re-run, no larger population, no third
readout.

**The instrument lesson, banked.** The MC bench in lettered format is not
a knowledge instrument on this base LM (position-A prior + shuffle-seed
sensitivity); cloze scoring restores it. This reconciles with EXP092:
the supervised 1-NN (33.33% vs 5%, p=0.000999) measures information
*presence*; EXP104 measured the untuned head's *routability*. Presence ≠
routability — another dissociation, not a contradiction.

**The verdict's honest reading.** Refuted is not evidence that masking
is generic — it is evidence the licensed test could not certify
specificity. The observed rescue direction was clean (random masking
rescued 0/21); the binding significance bar was missed by one flip at
n_pop=21. This is a falsification-terminal entry on the boundary map,
not a capability entry and not a premise kill.

**What changed, what didn't.** The honest headline is unchanged: zero
positive signals for autonomous steering; the label-free race stays tied
at zero. What changed is that the program's first selection-failure line
ran its entire licensed arc — instrument built, confound diagnosed and
removed, premise certified-not-specific by its own pre-registered bar —
in one day, $0, Δθ=0, with the terminal condition written *before* the
run, not after.
