# EXP139 — S4-4 (J1) Re-entrant Attractor Dynamics — Pre-registration DRAFT (UNSIGNED)

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. Licenses nothing. No run is authorized by this document.*
*Before any execution: independent Law #14 review of this exact draft + CEO clearance (including the LOG-4408 CPU-venue approval). Stage 2 additionally requires the founder's Kaggle GPU.*
*Experiment number EXP139 minted by the CEO 2026-10-03 (verified free: no hits in the research log or backlog).*
*Licensing chain: LOG-288 (S4-4/J1 born, QUEUED, 2026-09-24) → LOG-4408 (watchlist: J1 κ̂-screen CPU re-scope needs Law #14 + CEO venue re-licensing, NOT unilateral) → LOG-4879 (Friday cull option (b): redirect to surviving J-tier lines) → LOG-4883 (G/E/S loop family stood down) → `research/innovation/S44_DESIGN_2026-10-03.md` (worth-it gate, verdict CONDITIONAL RUN) → `research/innovation/S44_DESIGN_REVIEW_2026-10-03.md` (independent Law #14 review, APPROVE-WITH-CONDITIONS C1–C5).*
*Governing laws: Law #2 (no invented numbers), Law #4 (bars binding, no post-hoc shifts), Law #6 (Δθ=0), Law #7 (labels touch bench evaluation only — §8), Law #9 (metrics before inspection), Law #11 (observation vs interpretation), Law #13 (deterministic reproducibility), Law #15 (this document is the binding gate).*
*Epistemological labels per `AGENTS.md` §5 used throughout. $0 compute for this document.*

---

## 0. Law #15 block (binding)

**Precise question [HYPOTHESIS].** Does re-entrant iteration h^{(t+1)} = R(h^{(t)}), R(h) := F_{0..24}(Πh), h^{(0)} = h_L(x), of the frozen Pythia-410m backbone converge (empirical contraction κ̂ < 1), and does the attractor's decoded answer outperform the single-pass answer (ΔM_attractor ≥ +8pp with paired 95% LCI > 0.05) on the 60-item decision bench?

**Decision it changes.** **KILL** (family) if κ̂ ≥ 1 and the bounded-T pilot shows ΔM_bounded ≤ 0 — no contraction and no gain from re-entrance. **PIVOT** if κ̂ ≥ 1 but the bounded-T pilot shows ΔM_bounded > 0 with LCI > 0.05 — bounded re-entrance helps without a convergence license (re-scope to fixed-T refinement, no Banach claim); or if κ̂ < 1 but the trajectory diagnostic fails while ΔM is licensed — same re-scope. **CONTINUE** (licensed positive only) if κ̂ < 1, the trajectory diagnostic passes, and ΔM_attractor ≥ +8pp with LCI > 0.05 — licenses a follow-on (new number) on the attractor mechanism, not an integration claim. **HELD** in the six pre-registered intermediate/unrun cases (§6) — licenses nothing, kills nothing. Exactly one branch will be earned; precedence KILL > PIVOT > CONTINUE > HELD.

**Cheapest falsifying test.** Stage-1 κ̂ screen: 60 forward passes, $0 CPU, minutes — measures the load-bearing contraction license before any GPU. κ̂ ≥ 1 kills the Banach claim outright; the screen exists to kill, not to confirm (§4.4 one-sidedness admitted).

**Quantitative predictions (pre-registered bars).** Stage-1: κ̂ < 1 (the candidate's prediction; honest prior is κ̂ ≥ 1 — §10). Stage-2: ΔM_attractor ≥ +8pp with Newcombe paired 95% LCI > 0.05 (explicit construction §7; no software name invented). Stage-1b: ΔM_bounded > 0 with LCI > 0.05 for the PIVOT branch.

**Breaking points (sharp).** Stage-1 κ̂ ≥ 1 → contraction license LOST (Stage 2 does not run). Stage-1b ΔM_bounded ≤ 0 → **KILL**. Stage-2 ΔM_attractor ≤ 0 → **KILL**. Any validity gate in §3 fails → screen VOID (HELD with reason, never a verdict on the hypothesis).

**The belief it tests (named).** "A feedforward LLM can only compute feedforward functions" → "a frozen feedforward net can implement recurrent attractor computation at inference time." [INTERPRETATION]

---

## 1. Background, license, and condition-closure checklist

- **S4-4/J1** (backlog row 22, QUEUED since LOG-288): formal treatment in `research/innovation/S4_I1_FORMALIZATION_AND_J_TIER_2026-09-24.md`, Part B (J1 ranked #1 of the J-tier).
- **Design** (`S44_DESIGN_2026-10-03.md`): worth-it gate, verdict CONDITIONAL RUN. **Independent Law #14 review** (`S44_DESIGN_REVIEW_2026-10-03.md`): APPROVE-WITH-CONDITIONS C1–C5. This draft closes each condition; the closure is itemized here so the next reviewer can check it mechanically:
  - **C1** — re-entrant input construction pinned → §2 (sequence layout, position IDs, attention mask, readout, raw-logit weighting; no improvisation surface remains).
  - **C2** — verdict gaps closed → §6 (κ̂≥1 with Stage-1b unrun → HELD(a); Stage-1b intermediate zone → HELD(b); Stage-2 intermediate zone → HELD(c)).
  - **C3** — Stage-1b venue rule pinned → §4 (5-item pilot criterion: mean <30 s/pass and peak RSS < 8 GB → CPU, else GPU).
  - **C4** — Blayney et al. 2026 verified at draft stage → §9 (exists: arXiv:2604.11791; characterization confirmed; abstract-only, full-text follow-up flagged).
  - **C5** — expectation calibration stated → §10 (modal outcome κ̂≥1 → bounded-T pilot; pilot is boundary science).
- **Non-resurrection [FACT].** J1 injects no direction (vs killed static-geometry lanes), contains no selection step (vs dead E-step, LOG-4883), makes no layer-11 claim (vs S6), iterates residual states not output space (vs R7), uses no confidence signal (vs S4-5/TESTA). Every kill stands; nothing killed is re-tested.
- **Cost correction to the design [FACT].** The design's "40 passes" counts R-evaluations only. The committed EXP135 records store yhat/margin per (item, view) — no residual vectors (verified 2026-10-03 from `experiments/runs/EXP135_eval/out/exp135_records.json`). Obtaining the 20 h_i states requires 20 baseline forward passes. **True Stage-1 cost: 60 forward passes** (20 baseline + 40 R-evaluation). Still $0 CPU, still minutes by the H-wave precedent (108 generations in 20.9 min CPU, LOG-4553; a forward pass is far cheaper than a generation).

---

## 2. Re-entrant construction (C1 — fully pinned)

**Model [FACT].** EleutherAI/pythia-410m, local HF cache revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` (the LOG-331 pin), 24 layers, d=1024, 16 heads, vocab 50304, `tie_word_embeddings: false`, GPTNeoX parallel-residual blocks (all verified from the cached `config.json` 2026-10-03). Load via `AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=HF_REVISION, local_files_only=True, torch_dtype=torch.float32, device_map="cpu")` — float32 to match the EXP135 committed records. **Backbone pin:** sha256 of the state dict must equal `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (BACKBONE_PIN from `run_exp135.py`); mismatch → run VOID. Δθ=0 throughout: `model.eval()`, `torch.no_grad()`.

**Bench [FACT].** The 60-item decision bench reconstructed deterministically from `experiments/runs/EXP135_eval/run_exp135.py` (`build_bench`, `make_views`, `tok1`); `bench_sha256` must equal `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` (verified in TESTA_CALIBRATION_2026-10-03.md). Reconstruction mismatch → run VOID. Correctness: predicted token id == `tok1("A")`, where `tok1(s) = tokenizer.encode(" " + s)[0]` (single-token assertion, same tokenizer as the model).

**The operator.** Πh := W_Eᵀ(W_U h), with W_E = `gpt_neox.embed_in.weight`, W_U = `embed_out.weight` ([50304,1024] each, verified). **Raw-logit weighting, no softmax** — computed in float32 as written (no explicit 1024×1024 materialization required; the map is exactly Π = W_EᵀW_U ∈ ℝ^{1024×1024}). This corrects the S4 doc's dimensionally-wrong "W_E W_Uᵀ" (V×V) notation — the Law #14 review verified the correction independently.

**Single re-entrant step R(h) — exact procedure.**
1. Compute z = Πh ∈ ℝ^{1024}.
2. Form a **single-token input sequence**: `inputs_embeds = z.view(1, 1, 1024)`, `position_ids = [[0]]`, `attention_mask = [[1]]`. The re-entrant input carries no prompt context by construction — the state alone is iterated (this IS the re-entrant claim under test; rotary embeddings at position 0 apply no rotation).
3. Run the full 24-layer forward with `output_hidden_states=True`.
4. R(h) := `hidden_states[-1][0, 0, :]` — the final-block output at the sole position, pre-final-LayerNorm (consistent with h^{(0)} below).

**Initial state.** h^{(0)} = h_L(x) := `hidden_states[-1]` at the **last prompt position** from the single-pass forward on the item's prompt (view 0, §3), pre-final-LayerNorm — the same representation space R outputs.

**Readout (identical for baseline and attractor).** logits = `embed_out(final_layer_norm(h))`; prediction = argmax over the full vocab; correct iff == `tok1("A")`. Baseline readout position: last prompt position. Re-entrant readout position: position 0 (the sole position). If argmax ∉ {tok1("A"), tok1("C")}, record the raw token id as a diagnostic; it counts as incorrect.

**What is NOT pinned by choice (declared, not hidden).** View 0 (canonical first view) is used for all re-entrant measurements — arbitrary but deterministic and pre-registered; the 5-view structure characterizes the baseline only. T values are fixed per stage (§3–§5); no adaptive stopping.

---

## 3. Stage-1: κ̂ contraction screen (CPU)

**Items.** Items 0–19 in canonical bench order, view 0 (20 states; deterministic, no selection).

**Procedure.**
1. Validity gates (all must pass, else the screen is VOID → HELD with reason, never a verdict): (a) bench sha256 matches; (b) backbone pre-hash matches BACKBONE_PIN; (c) recomputed baseline yhat for the 20 screen items (view 0) matches the committed yhat exactly (20/20).
2. For each i: run the prompt forward (1 pass) → h_i; record baseline yhat_i.
3. δ_i: u_i uniform on the unit sphere via `torch.Generator().manual_seed(0)` (`torch.randn(1024, generator=g)`, normalized); δ_i = 0.01·‖h_i‖₂·u_i.
4. Evaluate R(h_i) and R(h_i + δ_i) (2 passes each).
5. κ̂ = max over (a) the 20 local ratios ‖R(h_i+δ_i) − R(h_i)‖₂/‖δ_i‖₂ and (b) all 190 cross-item ratios ‖R(h_i) − R(h_j)‖₂/‖h_i − h_j‖₂ (i<j), reusing the R(h_i) from step 4 — no extra passes. Report max (the estimator) plus median and IQR (diagnostics).
6. **Cost: 60 forward passes** (20 baseline + 40 R-evaluation) — the §1 cost correction. $0 CPU.

**One-sidedness (admitted, binding).** κ̂ is a lower bound on the true Lipschitz constant (max over finite sample ≤ sup). κ̂ ≥ 1 **refutes** contraction; κ̂ < 1 never proves it. The trajectory diagnostic (§5) is the backstop, not a certificate.

**Stage-1 verdicts.** κ̂ < 1 → contraction license SURVIVES → Stage-2 gate opens (still needs CEO venue approval + founder GPU). κ̂ ≥ 1 → contraction license LOST → Stage 2 does NOT run → Stage-1b (§4).

---

## 4. Stage-1b: bounded-T pilot (only if κ̂ ≥ 1)

**Venue rule (C3 — pinned).** Run the first 5 items (15 passes) as a pilot. **CPU iff** mean wall-clock per forward pass < 30 s **and** peak process RSS < 8 GB on the pilot; otherwise GPU (founder-gated, not assumed). The criterion is evaluated once, recorded, and not revisited at runtime.

**Procedure.** All 60 items, view 0, **T = 3 fixed** (180 R-evaluations + 40 additional baseline passes for items 20–59 [items 0–19 reuse Stage-1 h_i] = 220 passes): iterate h^{(1)}, h^{(2)}, h^{(3)} per item; decode at each t ∈ {1,2,3} via §2 readout. **Primary endpoint:** ΔM_bounded at t=3 vs the committed single-pass baseline (view 0 yhat from records — no new baseline passes). Secondary: t=1,2 trajectories (diagnostics, no extra passes).

**Inference.** Same Newcombe paired construction as §7 on the 60 pairs. PIVOT bar: ΔM_bounded > 0 with LCI > 0.05. KILL bar: ΔM_bounded ≤ 0.

---

## 5. Stage-2: full attractor test (only if κ̂ < 1; GPU, founder-gated)

**Procedure.** All 60 items, view 0, **T = 8 fixed** (480 R-evaluations + 40 additional baseline passes = 520 passes, <0.01 T4-h per backlog row 22). Decode at t=8 → ΔM_attractor vs committed baseline (view 0). **Trajectory diagnostic (binding backstop):** ‖h^{(t+1)} − h^{(t)}‖₂ for t=0..7 must be strictly decreasing; a non-decreasing trajectory voids the Banach reading even if ΔM is licensed (re-scoped per §6).

**Bars.** CONTINUE: ΔM_attractor ≥ +8pp with Newcombe paired 95% LCI > 0.05 (§7). KILL: ΔM_attractor ≤ 0.

---

## 6. Falsification tree (C2 — gaps closed; precedence KILL > PIVOT > CONTINUE > HELD)

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | κ̂ < 1 **and** trajectory strictly decreasing **and** ΔM_attractor ≥ +8pp with LCI > 0.05 | Attractor computation exists and helps. Licenses a follow-on (new number) on the mechanism. |
| KILL | κ̂ ≥ 1 **and** Stage-1b ΔM_bounded ≤ 0 | No contraction and no gain. Family closed. |
| PIVOT | (κ̂ ≥ 1 **and** Stage-1b ΔM_bounded > 0 with LCI > 0.05) **or** (κ̂ < 1 **and** trajectory non-decreasing **and** Stage-2 ΔM ≥ +8pp with LCI > 0.05) | Bounded re-entrance helps without a convergence license → re-scope to fixed-T refinement (no Banach claim). |
| HELD (a) | κ̂ ≥ 1 **and** Stage-1b unrun or infeasible | Contraction license lost; bounded pilot untested. Licenses nothing, kills nothing. |
| HELD (b) | Stage-1b 0 < ΔM_bounded with LCI ≤ 0.05 | Suggestive but unlicensed; a powered follow-up needs its own gate. |
| HELD (c) | κ̂ < 1, trajectory passes, Stage-2 0 < ΔM_attractor < +8pp, or Δ̂ ≥ +8pp with L ≤ 0.05 (LCI straddles the licensing threshold) | Movement without a licensed capability claim. |
| HELD (d) | κ̂ < 1, trajectory non-decreasing, ΔM not licensed | Banach reading void; nothing else established. |
| HELD (e) | κ̂ < 1 and Stage-2 unrun or infeasible | Contraction license survives; attractor untested. Licenses nothing, kills nothing. |
| HELD (f) | κ̂ < 1 and Stage-2 ΔM_attractor ≤ 0 | Converges to nothing useful — dynamics exist, no capability. Licenses nothing, kills nothing. |

Any validity gate failure (§3) → screen VOID (HELD with the stated reason).

---

## 7. Inference: Newcombe paired interval (explicit construction — no software invented)

For n=60 paired items: b = #{baseline wrong, attractor right}, c = #{baseline right, attractor wrong}, Δ̂ = (b−c)/n.
- Wilson 95% interval (z=1.96, **no continuity correction**) for p̂_b = b/n → (l_b, u_b), and for p̂_c = c/n → (l_c, u_c), each clipped to [0,1]:
  center = (p̂ + z²/2n)/(1 + z²/n); half = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n).
- L = Δ̂ − √((p̂_b − l_b)² + (u_c − p̂_c)²); U = Δ̂ + √((u_b − p̂_b)² + (p̂_c − l_c)²).
- **Binding bar:** Δ̂ ≥ 0.08 **and** L > 0.05.
- Secondary (reported, not binding): McNemar-exact two-sided p on the 2×2 table.
The executing lane implements these equations verbatim and archives the code; any deviation voids the inference.

---

## 8. Law #7 boundary

Labels (correct answers) are used **only** for bench evaluation — computing accuracy, ΔM, and the paired table. No label touches any selection, ranking, scoring, stopping, or venue decision anywhere in EXP139 (there is no selection step; the screen items are bench-ordered, not label-selected). The κ̂ estimator never sees labels. The Law #7 firewall is structural, not procedural.

---

## 9. Citation verification (C4) and prior art

- **Blayney et al. 2026 — VERIFIED at draft stage (2026-10-03).** "A Mechanistic Analysis of Looped Reasoning Language Models," arXiv:2604.11791 (April 2026). Abstract confirms: for many studied models each recurrent-block layer converges to a distinct fixed point, yielding a consistent cyclic trajectory. Relevance exactly as the design characterized: plausibility support for fixed-point dynamics in **trained** looped models — not frozen pretrained ones, which is J1's question. **Abstract-only verification**; full-text follow-up is flagged for any future paper use (per the design's §8 note).
- **arXiv:2602.14759** ("Inner Loop Inference") and **arXiv:2605.12466** ("Solve the Loop") — verified real with accurate characterizations by the independent Law #14 design review (2026-10-03); not re-verified here. Novelty read **N1 (known combination)** stands; J1's differentiators (Π-feedback construction, contraction-licensed attractor claim, falsification-first bars on this bench/backbone) are construction differences, honestly claimed.

---

## 10. Expectation calibration (C5)

**Modal outcome: κ̂ ≥ 1 → bounded-T pilot.** The honest prior is divergence (transformer blocks generically expansive; §4.2 of the design; the Law #14 review's steelman). The expected value of EXP139 is the cheap kill of the Banach claim plus the bounded-T pilot — **boundary science on this bench/backbone, not a novelty claim and not the attractor claim**. A κ̂ < 1 outcome would be genuinely surprising precisely because the prior is against it; CONTINUE remains a long shot, priced not hidden.

---

## 11. Risks and honest limitations

1. The single-token re-entrant input discards the question context by construction — the fixed point (if any) must carry question information through Π-feedback alone. That is the radical claim under test, stated plainly, not hidden.
2. View 0 is arbitrary but deterministic; results are view-0-scoped unless a follow-up generalizes.
3. κ̂ < 1 never proves contraction (one-sided screen, §3).
4. Π is a modeling choice; alternatives (e.g., pseudoinverse-style maps, identity) are deviations requiring their own gates.
5. All bars are bench- and backbone-scoped (60-item decision bench, Pythia-410m). No claim about other benches/backbones is licensed under any branch.
6. Stage-2's 520 GPU passes are founder-gated; this draft assumes nothing about venue availability.

---

## Appendix A. Condition-closure checklist (for the next Law #14 reviewer)

- [ ] C1: §2 pins sequence layout (single-token `inputs_embeds`), position_ids=[[0]], attention_mask=[[1]], readout (final-LN + unembed + argmax; baseline: last position; re-entrant: position 0), raw-logit Πh with no softmax. No improvisation surface remains.
- [ ] C2: §6 closes both gaps — HELD(a) for κ̂≥1 with Stage-1b unrun; HELD(b)/(c)/(d) for the intermediate zones.
- [ ] C3: §4 pins the venue rule (5-item pilot; <30 s/pass and <8 GB RSS → CPU, else GPU).
- [ ] C4: §9 records the Blayney verification (arXiv:2604.11791, abstract-only).
- [ ] C5: §10 states the modal outcome and the pilot's boundary-science status.
- [ ] Cost correction: §1/§3 state the true 60-pass Stage-1 cost (design said 40 R-evals only).
- [ ] Dtype correction: §2 pins torch.float32 to match the committed records (run_exp135.py), with BACKBONE_PIN `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`.
