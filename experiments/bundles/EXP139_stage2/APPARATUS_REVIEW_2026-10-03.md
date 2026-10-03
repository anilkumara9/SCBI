# Law #14 Apparatus Review — EXP139 Stage-2 Kaggle Execution Bundle

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (binding verdict; the CEO cannot override).
**Date:** 2026-10-03.
**Artifact under review:** `experiments/bundles/EXP139_stage2/` — `exp139_stage2_lib.py`, `run_stage2.py`, `tests/test_bundle_cpu.py`, `requirements.txt`, `README.md`, `BUNDLE_NOTES.md`, `data/committed_baseline_view0.json`.
**Protocol (binding, immutable):** `research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md` (SIGNED per LOG-4885; the file's "DRAFT (UNSIGNED)" header is stale text — the LOG-4885 entry promotes it, same pattern as the EXP142 pre-reg; signed status is established by LOG-4885 and `research/prereg/EXP139_S44_prereg_REVIEW_2026-10-03.md`. This review edits nothing signed.)
**Stage-1 context [OBSERVATION, LOG-4886]:** κ̂ = 0.955971 < 1 — contraction license survives; Stage-2 gate scientifically open, founder-GPU-gated.
**Compute:** $0; zero GPU contact; no weight downloads (torch not installed in the review environment). CPU structural tests re-run by this reviewer: **60/60 PASS**.

## Binding verdict: SIGN-WITH-FIXES

Four required fixes (F1–F4), three minor (m1–m3). **F1 is critical: as written, the executor crashes on the first item's attractor decode — the bundle is non-functional.** Nothing may be asked of the founder until a repair lane applies F1–F4 (+m1–m3) and a follow-up Law #14 verification review signs the repaired bundle. No re-review of substance is needed after mechanical repair unless the repair changes protocol behavior.

---

## 1. Line-by-line verification against the signed pre-registration

### §2 pins — PASS
- `BACKBONE_PIN ec276abe…38e0ed`, `BENCH_PIN eb304fa6…45589df`, `HF_REVISION 9879c9b5…d4f`, `MODEL_ID EleutherAI/pythia-410m` — all four present verbatim in the lib and verified present in the pre-registration text by test (`pin_in_prereg_*`, `model_id_in_prereg`). ✓
- Load call matches §2 verbatim (`from_pretrained(..., revision=HF_REVISION, local_files_only=True, torch_dtype=torch.float32, device_map="cpu")`); venue moved to `cuda:0` via `model.to(DEVICE)` — a documented venue move, not a protocol change. `model.eval()`, `torch.no_grad()` throughout. ✓
- Operator: `z = W_E.t() @ (W_U @ h)` with `W_E = gpt_neox.embed_in.weight`, `W_U = get_output_embeddings().weight` — exactly Π = W_EᵀW_U, raw-logit weighting, no softmax, float32. ✓
- Re-entrant step: single-token `inputs_embeds = z.view(1,1,1024)`, `position_ids=[[0]]`, `attention_mask=[[1]]` (both on device), `output_hidden_states=True`, `R(h) := hidden_states[-1][0,0,:]`. ✓
- Initial state: `hidden_states[-1][0,-1,:]` (last prompt position, pre-final-LN). ✓
- Readout: `embed_out(final_layer_norm(h))`; baseline at last prompt position, re-entrant at position 0. ✓ (Two-way candidate convention — see AMBIGUITY-2 adjudication below.)
- `tok1(s) = tokenizer.encode(" " + s)[0]` with single-token assertion. ✓

### §5 executor protocol
- 60 baselines + 480 R-evaluations (T=8 from `lib.T_STEPS`, no hardcoded 8) with an in-script forward-budget assert → exit 44 on mismatch. ✓ (540 vs the pre-reg's 520 — see AMBIGUITY-1.)
- Decode at t=8; paired table (b, c) vs the COMMITTED baseline yhat (recomputed yhat used only for gate (c)); §7 Newcombe construction implemented verbatim — independently re-verified by this reviewer from scratch (n=60,b=10,c=2 → L=0.024445, U=0.249521; lib matches to 1e-12; the test's hand-derived constants match to 1e-4). Minimal bar-met case (b=9,c=0 → dhat=0.15, L=0.0584) confirms the bar is attainable but demanding. ✓
- Trajectory backstop: 8 diff-norms (t=0..7), strict decrease required; tie rejected (tested). Aggregation choice (all-60-items strict) is the conservative reading of the pre-reg's unaggregated "must be strictly decreasing" — acceptable, documented in logs; noted as m3. ✓
- Validity gates (a) bench sha256, (b) backbone pre-hash, (c) yhat fidelity — all trip to RUN-INVALID (exit 44), never to a verdict. ✓ Gate (c) extended 20/20 → 60/60: strictly stronger than §3(c), an acceptable analog (the paired table's baseline arm is the committed yhat, so verifying all 60 recomputed yhats against it is the correct fidelity check for the 540-pass execution). ✓
- **F1 (CRITICAL):** the attractor decode is broken. `readout_yhat(h)` returns the full `(50304,)` logit vector, but both call sites index `[0]` (`lv_attr = readout_yhat(traj[L.T_STEPS])[0]`, `lv_t = readout_yhat(traj[t])[0]`), reducing it to a 0-dim scalar; `yhat_of` then evaluates `float(lv1d[t_target])` → `IndexError: too many indices for tensor of dimension 0`. The executor crashes on item 0's attractor decode. (A refactor slip: Stage-1's `yhat_of` needed `[0,-1,:]` because it received full `(batch, seq, vocab)` logits; here the reduction already happened inside `readout_yhat`.) The static test suite cannot catch torch-path defects — this is the gap F1's regression test must close.
- **F2:** post-hash is computed and logged but not enforced: a backbone post-hash mismatch logs "MISMATCH" and still exits 0. Law #6 (Δθ=0) is inviolable — a verdict emitted from a mutated-weights run would be void. Harden to RUN-INVALID (exit 44) on post-hash mismatch, and persist `backbone_post` in `stage2_records.json` and `stage2_verdict.json` (currently only the pre-hash is recorded).

### §7 / §6 reporting
- Branch reporter covers CONTINUE / PIVOT / HELD(c) / HELD(d) correctly (tested). The ΔM≤0 path dual-reports pending adjudication — resolved by F4 below.

### Exit-44 RUN-INVALID semantics — PASS
- Gates, venue failure (no CUDA), missing model cache (with the exact recovery command), and budget mismatch all write a `RUN-INVALID` verdict artifact and `sys.exit(44)`. No gate failure can produce a hypothesis verdict. ✓

---

## 2. Binding adjudication of the four ambiguities

**AMBIGUITY-1 (540 vs 520 passes) — ACCEPT 540.** The pre-reg's "520" is a resource estimate, not a bar; the measurement set (60 baselines + 480 R-evaluations) is identical. Stage-1 archived only h_i norms, not the 20 h_i vectors, so items 0–19 cannot be reused on the founder's machine — recomputation is required. The in-script 540 assert is the correct enforcement. Wording correction in m2.

**AMBIGUITY-2 (two-way readout vs §2's full-vocab argmax) — ACCEPT the two-way convention for BOTH arms (binding).** (1) The signed Stage-1 implementation (`run_stage1.py`, LOG-4886) uses the two-way comparison — verified by this reviewer (`yhat_of`: `t_target if lv[t_target] >= lv[t_foil] else t_foil`); Stage-2 must use the same correctness predicate as the stage whose license it inherits. (2) The paired table's baseline arm is derived from the committed EXP135 records, which use the two-way convention — a mixed convention would make the paired comparison ill-defined. (3) The deviation from the §2 text materializes only in the third-token-argmax corner. (4) It is documented in the executor docstring, README, and run report. This is a documented deviation from the §2 text, not a protocol change.

**AMBIGUITY-3 (McNemar two-sided convention) — ACCEPT the doubling method.** The statistic is secondary (reported, not binding) and the convention is documented. No change required.

**AMBIGUITY-4 (Stage-2 ΔM_attractor ≤ 0 → KILL vs HELD(f)) — HELD(f) GOVERNS (binding).**
The document contradicts itself: §0 breaking points and §5 bars assign ΔM≤0 → KILL; the §6 falsification table assigns κ̂<1 with ΔM≤0 → HELD(f) ("converges to nothing useful — dynamics exist, no capability; licenses nothing, kills nothing"). Adjudication:
1. The §6 table is the operative branch assignment — it is the C2 gap-closure the design review demanded, and it carries the document's only explicit conflict-resolution rule ("precedence KILL > PIVOT > CONTINUE > HELD", adjudicating conflicts *between table rows*). Within the table, the KILL row's trip condition ("κ̂ ≥ 1 and Stage-1b ΔM_bounded ≤ 0") does not trip in the κ̂<1 path; HELD(f)'s does. "Exactly one branch will be earned" → HELD(f).
2. The §0 Law #15 block — the document's binding gate — itself incorporates "the six pre-registered intermediate/unrun cases (§6)", i.e. HELD(a)–(f) including (f). The breaking-points summary line contradicts the block's own enumeration; the block wins.
3. The §0 decision-text family-KILL condition ("κ̂ ≥ 1 and the bounded-T pilot shows ΔM_bounded ≤ 0") agrees with the §6 KILL row, not with the breaking-points line. The program's own log summary (LOG-4885) records the binding KILL bar the same narrow way. The two most deliberate statements agree; the two summary lines are the outliers — overcompressions that conflate the Stage-1b KILL bar (correct there, where no contraction license exists) with Stage-2.
4. Substance: Stage-2's two-part license (trajectory backstop + ΔM) separates dynamics from capability. Killing the family on a capability miss when the dynamics finding survived would conflate them and contradict the §10 calibration (the dynamics/boundary-science is the experiment's value).
**Ruling:** for κ̂<1 and Stage-2 ΔM_attractor ≤ 0, the governing branch is **HELD(f)**. The §0 breaking-points line "Stage-2 ΔM_attractor ≤ 0 → KILL" and the §5 bar "KILL: ΔM_attractor ≤ 0" are superseded as drafting defects. This is a pre-execution disambiguation of a drafting defect, not a post-hoc bar shift (Law #4): HELD(f) licenses nothing and kills nothing.

---

## 3. Test-suite assessment

60/60 PASS on independent re-run by this reviewer. Coverage is good with one structural gap:
- Pin fidelity (bench hash, all three pins + model id + T=8 in the pre-reg text): covered. ✓
- No-training static scan (5 negative patterns absent, 7 positive tokens present): covered. ✓
- Verdict-tree branches (CONTINUE/PIVOT/HELD(c)/HELD(d)/conflict): covered. After F4, the conflict-path test must assert HELD(f) emission instead of dual-report. ✓ (with F4)
- Data integrity vs EXP135 source (60 ids + 60 yhat values match `cache_unintervened[i][0].yhat`): covered on the build machine. ✓
- Newcombe/Wilson/McNemar vs independent references: covered; Newcombe additionally verified from scratch by this reviewer. ✓
- **Gap:** the torch execution path is untestable in the build environment (torch not installed) — F1 slipped through exactly here. **F3:** the two checks reading `~/workspace/...` absolute paths (pre-reg text, EXP135 source) raise `FileNotFoundError` on the founder's Kaggle machine — the founder cannot complete README step 5 ("all must pass") on a clean machine. Both checks must SKIP gracefully when the files are absent (provenance was verified at build time, by this review); README step 5 must read "zero FAILs required; SKIP lines are expected on Kaggle (build-machine provenance checks)".

## 4. Founder-facing README assessment

Steps are exact, complete, and safe: Kaggle notebook → GPU (T4) → Internet ON → upload bundle (structure preserved) → `huggingface-cli download EleutherAI/pythia-410m --revision 9879c9b5…d4f` (public repo, no login) → `pip install -r requirements.txt` → CPU tests → `run_stage2.py` → send back the four `out/` files. No credential or token handling anywhere. No weight-exfiltration risk: weights remain in the Kaggle HF cache; outputs are JSON/log/Markdown. Model pin is correct. Expected console markers and exit-44 semantics are accurate. Two corrections required: F3 (step 5 achievability) and F4 (the "both readings" paragraph must state the adjudicated HELD(f) reading with a transparency note).

## 5. Awareness note — LOG-4895 chat-template finding

Per instructions this finding is not applied here; conditional exposure only. The bundle's measurement chain uses direct `tokenizer.encode(prompt)` on prompt strings — **no chat template appears anywhere** (verified in the Stage-1 precedent and this executor). Tokenizer is pinned (`transformers==5.17.0`, the LOG-331 pin basis), and validity gate (c) (60/60 yhat fidelity vs committed records) anchors tokenization bitwise at runtime. **The bundle would not be affected if the LOG-4895 finding signs.** Optional follow-up hardening (vendoring exact token-id buffers per prompt) is available but not required. (Note: since this review was commissioned, LOG-4895 has landed in the research log as SIGN-WITH-FIXES; its F2 softens the token-exactness claim to position-dependent, which reinforces the posture taken here.)

## Required fixes (for a separate repair lane — this review modifies nothing)

- **F1 (critical):** remove the erroneous `[0]` at the two attractor-decode call sites in `run_stage2.py` (`readout_yhat` already returns the `(50304,)` vector). Add a CPU regression test that would have caught this (stubbed 50304-length readout through the exact `yhat_of` call path).
- **F2:** trip RUN-INVALID (exit 44) on backbone post-hash mismatch; persist `backbone_post` in `stage2_records.json` and `stage2_verdict.json`.
- **F3:** make the two `~/workspace/...`-dependent test checks SKIP (not crash) when the files are absent; reword README step 5 to "zero FAILs required; SKIPs expected on Kaggle".
- **F4:** implement the AMBIGUITY-4 adjudication — emit HELD(f) as the governing branch for κ̂<1 & ΔM≤0 (cite this review, LOG-4896), keep a transparency note on the superseded §0/§5 lines; update README's "both readings" paragraph and the conflict-path test.
- **m1:** `BUNDLE_NOTES.md` §(b): "40 structural tests" → 60.
- **m2:** soften "bitwise-deterministic" → per-machine determinism; cross-machine equivalence is anchored by gates (a)–(c), not by a bitwise claim.
- **m3:** document the trajectory aggregation choice (all-60-items strict) in `BUNDLE_NOTES.md` as the conservative reading of the pre-reg's unaggregated "must be strictly decreasing".

**Founder contact is not licensed** until the repair lane applies F1–F4 (+m1–m3) and a follow-up Law #14 verification review signs the repaired bundle.
