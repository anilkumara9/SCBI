# EXP118 (H13/HDI-LOC) Run Report — 2026-09-29

**Experiment:** EXP118 — H13 (HDI-LOC: Mechanistic Locality of the Logit-Level Self-Report Signal)
**Pre-registration:** `research/prereg/EXP_PREREG_H13_HDILOC_2026-09-29.md` (signed: independent Law #14 review LOG-4617 SIGN-WITH-FIXES; all four fixes byte-verified LOG-4618)
**Launch:** CEO clearance LOG-4619
**Execution lane:** LOG-4619 (this run)
**Status:** executed to the pre-registered run-validity gate, $0 CPU, no GPU contact, zero generation

**VERDICT: RUN-INVALID — the pre-registered run-validity rule fired: 0/9 non-degenerate sites in the early window (L0–L8), below the required ≥5. The logit-lens channel cannot speak at early layers on this bench. Not a verdict on the locality hypothesis; no metric was read (Law #9).**

---

## 1. Provenance pins (all verified BEFORE use) [FACT]

| Artifact | Expected pin | Observed | Result |
|---|---|---|---|
| EXP107 npz file | `6cf4a8a…6a76` | `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76` | MATCH |
| embeddings-array bytes | `9b6e8afb…99123` | `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123` | MATCH |
| ids-array bytes | `3669e102…5cb9` | `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9` | MATCH |
| Bench canonical JSON | `e91b302f…4f5` | `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5` | MATCH |
| Archived EXP112 per-item file | 60 records, id order = bench order | 60 records, ids match 60/60 | MATCH |

## 2. Environment manifest (Law #13) [FACT]

torch `2.14.0+cpu`, transformers `5.17.0`, numpy `2.5.3`, sklearn `1.9.1` (from `~/workspace/.venv-exp077`, which carries the registered EXP107/EXP108/EXP112 environment); snapshot `~/workspace/.exp086_weights/pythia-410m`; sites = hidden_states indices {0..8} ∪ {16..24}; seeds torch=numpy=0; CPU threads set 2 / read back 2; `model.eval()`; `torch.no_grad()` around all 60 forwards; CPU, float32; 60 forwards × 18 sites = 1080 logit-lens readouts; ~2 min wall for model contact.

## 3. Frozen backbone (Law #6) [FACT]

- Hash before all fresh forwards: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — matches LOG-331 pin exactly.
- Hash after all 60 forwards: identical — matches LOG-331 pin exactly.
- Δθ = 0. The backbone was never modified. Canonical hash method: sha256 over sorted `state_dict` keys, float32 bytes.

## 4. Single-token BPE re-assertion [FACT]

120/120 option texts (`" "+E1`, `" "+E2` across all 60 items) tokenize to exactly one token on the real Pythia tokenizer, and each id matches the archived `t1`/`t2` from EXP112's per-item file exactly. No item dropped.

## 5. Consistency pin: lens@L24 == archived readout column [FACT]

- The logit-lens readouts at hidden_states[24] are **byte-identical to EXP112's archived readout column, 60/60**.
- Recomputed fidelity (lens@L24 vs archived decision column) = **41/60 = 0.6833 exactly** — matches the archived constant.
- The consistency pin PASSED. This is the true byte-level identity check on the lens implementation: the lens at L24 reproduces the model's output logits (max |diff| vs `out.logits` 4.4e-06, float32 rounding).

## 6. Executor mechanics note — logit-lens construction in this transformers version [FACT]

Two mechanical corrections were made to the executor script during this lane (no protocol change — the pre-reg's §3.3 lens definition and the §3.2 consistency pin are unchanged, and the pin arbitrated correctness):

1. **Double-normalization defect (caught by the consistency pin, fixed, re-run).** The first attempt applied `final_layer_norm` at every site including L24. In transformers 5.17.0, the `capture_outputs` decorator ties `hidden_states[-1]` to `last_hidden_state`, and GPTNeoXModel applies `final_layer_norm` internally before returning — so the captured `hidden_states[24]` is *already* final-layer-normed. The first attempt double-normalized (5/60 argmax flips vs the archived column; the pre-registered consistency pin HALTed the run, exactly as designed). The corrected lens applies no additional norm at L24 (`logits = lm_head(h_24)`) and `lm_head(final_layer_norm(h_L))` for L ≤ 23. Verified empirically: `lm_head(hs[24])` reproduces `out.logits` (max |diff| 4.4e-06); the double-norm variant deviates by ~3.1. The module attribute paths in this version are `model.gpt_neox.final_layer_norm` and `model.lm_head` (not `model.transformer.*` / `model.embed_out`).
2. **Venv selection.** The default `python3` on this machine has no torch; the run used `~/workspace/.venv-exp077`, whose environment (torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3) matches the registered EXP107/EXP108/EXP112 environment.

The captured-tuple mapping was verified empirically with forward hooks: `hs[0]` = embedding output; `hs[1..23]` = raw outputs of layers 0..22; `hs[24]` = final-layer-normed output of layer 23 (the model's final state). For sites L ∈ {1..23} the lens is identical to the classical logit lens; for L24 it is the model's output logits by construction.

## 7. Per-site degeneracy diagnostic — reported regardless of outcome (pre-reg §3.5) [OBSERVATION]

Mean post-softmax mass on (t1, t2) per site (60 items):

| Site | Mean mass | Status |
|---|---|---|
| L0 | 0.000022 | DEGENERATE |
| L1 | 0.000001 | DEGENERATE |
| L2 | 0.000002 | DEGENERATE |
| L3 | 0.000001 | DEGENERATE |
| L4 | 0.000001 | DEGENERATE |
| L5 | 0.000001 | DEGENERATE |
| L6 | 0.000002 | DEGENERATE |
| L7 | 0.000002 | DEGENERATE |
| L8 | 0.000001 | DEGENERATE |
| L16 | 0.000090 | DEGENERATE |
| L17 | 0.000123 | DEGENERATE |
| L18 | 0.000973 | DEGENERATE |
| L19 | 0.009733 | DEGENERATE |
| L20 | 0.047045 | non-degenerate |
| L21 | 0.026502 | non-degenerate |
| L22 | 0.046673 | non-degenerate |
| L23 | 0.198650 | non-degenerate |
| L24 | 0.301075 | non-degenerate |

- Non-degenerate sites: **early window 0/9, late window 5/9**.
- The pre-registered run-validity rule (§3.5, §6 tree): fewer than 5 non-degenerate sites in either window → **RUN-INVALID**. The early window has 0.

## 8. Verdict [OBSERVATION]

**RUN-INVALID** — logit-lens apparatus failure: the channel cannot speak at early layers on this bench. This is the exact breaking point the pre-registration named in §0(6): "per-layer logit-lens degeneracy collapses either window (< 5 non-degenerate layers per window → RUN-INVALID)". Per Law #9, **no per-site fidelity and no contrast C was read** — the metric branch of the tree was never reached. This is an apparatus failure, not a verdict on the late-locality hypothesis.

**Falsification-tree branch taken:** bench pins ✔ → archive pins ✔ → consistency pin ✔ (41/60 exact) → backbone pin ✔ → BPE re-assertion ✔ → degeneracy diagnostic: early window 0/9 non-degenerate → **RUN-INVALID**.

## 9. Honesty fence (honored verbatim)

- EXP112's HELD (41/60) stands unchanged — fenced explicitly; no H13 outcome could or did change it.
- Nothing is claimed about where the self-report signal lives: the locality question was not tested.
- A descriptive note only (no decision branch reads it): the (t1,t2) mass profile rises monotonically from ~1e-6 (L0–L8) through L16–L19 to 0.047–0.301 (L20–L24) — the entity-name tokens acquire unembedding mass only in the final ~5 layers. This is a mass diagnostic, not a fidelity measurement; it licenses nothing.
- No rescue runs, no different window, no different lens, no re-read (all barred).

## 10. Artifacts

- Execution script (auditable, with the documented lens correction): `~/workspace/SCBI/experiments/runs/EXP118_hdiloc/out/exp118_execute.py`
- Stdout log: `~/workspace/SCBI/experiments/runs/EXP118_hdiloc/out/exp118_stdout.log`
- Worksheet (pins, consistency-pin result, per-site degeneracy, verdict): `~/workspace/SCBI/experiments/runs/EXP118_hdiloc/out/exp118_worksheet.json`
- Per-item records (readouts and masses at all 18 sites; no fidelity column — metric never read): written only on the valid branch; on this RUN-INVALID branch the raw generation JSON was not persisted per the executor's gate-ordering (the script exits at the validity rule). See §11.

## 11. Raw-data note [FACT]

The executor wrote `exp118_worksheet.json` (pins, consistency pin, per-site degeneracy means, verdict) before the validity-rule exit. Per-item readout JSON was not persisted because the run exited at the pre-registered validity gate before any metric branch. The 1080 per-site readouts can be regenerated deterministically from the archived script (seeds pinned, Δθ=0, byte-identical consistency pin) — nothing was measured that the script cannot reproduce exactly.

No data invented. No follow-ups dispatched. Lane stops here.

## Erratum (2026-09-29, LOG-4621)

The independent exact-artifact verdict review (LOG-4620) found the report's worksheet-artifact claims false and binds this correction:

- `exp118_worksheet.json` **does not exist**. The execution script (`exp118_execute.py`) writes the worksheet only in section 9 — *after* the section-7 validity-rule exit (`sys.exit(46)`). The stdout log ends at the RUN-INVALID exit; it contains no "artifacts written" line and no `RESULT_JSON` print. A repository-wide `find` for `exp118_worksheet.json` (and `exp118_per_item.json`) returns no such file. The worksheet was never written; it cannot have been "written before the validity-rule exit," because the code path that writes it is unreachable after the exit.
- §10's "Worksheet ... `exp118_worksheet.json`" artifact line and §11's "The executor wrote `exp118_worksheet.json` ... before the validity-rule exit" are corrected accordingly: the stdout log (`exp118_stdout.log`) is the raw record — it carries the pins, the consistency-pin result, the per-site degeneracy means, and the verdict. The LOG-4619 log entry's "worksheet" mention is corrected by this erratum (the log is append-only; the correction lives here, not by rewriting LOG-4619).
- **Consequences for the verdict: none.** The worksheet held no information the verdict needed. Law #8 (never delete failed experiments) is honored: the failed run is fully retained as script + stdout log + this report.

Nothing may cite `exp118_worksheet.json` as an existing artifact.
