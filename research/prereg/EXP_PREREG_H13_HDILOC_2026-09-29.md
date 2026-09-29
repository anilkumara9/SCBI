# Pre-registration: H13 — HDI-LOC (Mechanistic Locality of the Logit-Level Self-Report Signal)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4616 (pre-assigned). **Source:** `research/strategy/INNOVATION_SPRINT_2026-09-29_H1315.md` §H13 (worth-it gate passed).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — no bench labels touch the apparatus), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

**Epistemological labels** per `SCBI/AGENTS.md` §5: [OBSERVATION], [HYPOTHESIS], [INTERPRETATION], [PROPOSITION], [ASSUMPTION], [FACT].

---

## 0. Worth-it gate (§0 — the six elements, binding on this draft)

1. **Exact question:** Does EXP112's logit-level self-report fidelity (41/60, HELD) concentrate in late layers of base Pythia-410m when read via a zero-training logit lens at each layer's residual stream, on the same EXP107 decorrelated bench? Formally: is the pre-registered contrast **C = mean(fidelity over L16–L24) − mean(fidelity over L0–L8)** (hidden_states indices; 9 layers each) large and positive?
2. **Decision changed:** C ≥ 0.10 with late-window fidelity ≥ 0.65 → CONTINUE the honesty-instrument program with a localization story; |C| < 0.05 → KILL the locality question (signal diffuse; EXP112's HELD stands but loses its mechanistic foothold); C ≤ −0.10 → KILL the late-locality hypothesis (reverse concentration); everything else → HELD.
3. **Cheapest test:** 60 items × 18 layers of cached forwards, logit-lens readout = argmax over the two pinned entity first-token ids at each layer. $0 CPU, zero training, zero generation, same bench/pins as EXP112.
4. **Mathematical license:** EXP112 HELD 41/60 with P(X ≥ 41 | 60, 0.5) = 0.0031 — a real signal exists at the final-output logits read site; the logit lens (final LayerNorm + unembedding) is a standard zero-training per-layer readout; the layer contrast is a single pre-registered statistic (no multiplicity). The per-layer readouts are NEW data — never computed — not Law-#9 theater.
5. **Quantitative prediction:** fidelity monotone non-decreasing over L12–L24; late window ≥ 0.65 (the other 8 late layers must average ≥ 0.6458 given the archived final-output fidelity 41/60 = 0.6833 (the logit lens applied at hidden_states[24])); early window ≤ 0.55; C ≥ 0.10.
6. **Breaking point:** per-layer logit-lens degeneracy collapses either window (< 5 non-degenerate layers per window → RUN-INVALID), or the profile is flat (|C| < 0.05) → locality KILLED; no rescue, no re-run.

**Key challenges adjudicated:**

(a) **Is the late-layer question new data?** [FACT] Yes. EXP111's per-layer L4–L16 analysis trained L2-logistic heads on activations — a different instrument (trained, not zero-training). No logit-lens self-report profile was ever computed for H6/EXP111/EXP112. The contrast statistic, the windows, and the bars are registered before any per-layer forward.

(b) **Is a new experiment number licensed?** [FACT] Yes. The per-layer readouts require 1080 new forward passes. The only re-read data is the decision-target column (EXP112's archived per-item decisions), which is the *fixed measurement target* pinned by H6's protocol, verified by a pre-run consistency pin (§3.2) — not a metric being re-tested.

(c) **H6's "no different layer" fence.** [INTERPRETATION] H6 §4's 'No rescue runs' clause bars a HELD/KILL being 'followed by ... a different layer' as an unlicensed gate tweak — that bar was about re-running H6's *existence* question at another layer to chase a better verdict. H13 asks a *different question* (where the signal lives) that no registered bar ever addressed, and H13 **cannot upgrade EXP112's HELD** — no H13 outcome changes EXP112's verdict (fenced in §7.1).

(d) **Statistical license (honestly computed, verified at drafting):** Under a no-locality null where per-layer fidelity is flat at EXP112's 0.6833, per-layer SE ≤ √(0.6833×0.3167/60) = 0.0601; window-mean SE ≤ 0.0200 under independence; SE(C) ≤ 0.0283. C ≥ 0.10 is ≥ 3.5σ from the no-locality null (two-sided p ≈ 4×10⁻⁴). Inter-layer logit-lens correlation attenuates the effective df — at ~3 effective layers per window, SE(C) ≈ 0.0490, C ≥ 0.10 is 2.0σ (p ≈ 0.041). The CONTINUE bar is therefore 2–3.5σ from no-locality: **not razor-thin**, and the dual bar (late ≥ 0.65) adds an independent demand. The HELD zone 0.05–0.10 is the honest indeterminate band. KILL-bar miss rate under a true C = 0.10: ≈ 0.04 (independence) to ≈ 0.15 (attenuated) — disclosed, and the HELD zone absorbs the ambiguous region.

**Summit filter:** a localizable self-report signal is a mechanistic foothold toward self-consistent representation — the summit needs honest internal readouts; a diffuse signal is far harder to build on. **GATE: PASS.**

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** On the 60-item EXP107 template-decorrelated bench, the fidelity between the frozen backbone's logit-lens self-report (two-way argmax over the pinned entity-name token ids at each layer's residual stream, zero generation) and the H6-registered decision statistic concentrates in late layers: **C = mean(fidelity L16–L24) − mean(fidelity L0–L8) ≥ 0.10 with late-window fidelity ≥ 0.65.**

**Falsifiers:** |C| < 0.05 (diffuse) or C ≤ −0.10 (reverse concentration).

### 1.1 Why H13 exists — H6 is NOT re-run

[OBSERVATION] EXP112 (H6/HDI-LR) ended **HELD**: fidelity 41/60 = 0.6833 at the single final-output read site, P(X ≥ 41 | 60, 0.5) = 0.0031. The signal's layer profile is unknown.

H13 asks **where the signal lives**, not whether it exists. The apparatus is H6's instrument extended per-layer via the logit lens — the same two-way argmax readout, the same pinned token ids, the same decision target. No H6 measurement is re-run as a measurement of H6's question: the final-output fidelity value is an archived constant (a consistency pin, §3.2), and H13's verdict bars are defined on the contrast, which no registered bar ever addressed. This is a **new hypothesis**, not a rescue of H6's HELD (and H13 cannot upgrade it — §7.1).

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** At fixed logit-lens readout, does the H6 self-report fidelity concentrate in late layers (L16–L24) relative to early layers (L0–L8)?

**Decision changed:**
- **CONTINUE** the honesty-instrument program *with a localization story*: the self-report signal is late-layer-localizable — a mechanistic foothold for later, separately-licensed lanes.
- **KILL** the locality question: the signal is diffuse (|C| < 0.05) or concentrates early (C ≤ −0.10) — EXP112's HELD stands but has no layer foothold; no further layer-profile work is licensed.
- **HELD** (registered): borderline contrast 0.05–0.10, contrast ≥ 0.10 without late ≥ 0.65, or reverse-borderline −0.10 < C < −0.05 — indeterminate; licenses nothing, retires nothing, no re-runs.

**Primary statistic (registered before any run):** per-layer fidelity f_L = (1/60) Σᵢ 1[readout_i,L == decision_i], where readout_i,L is the §3.4 logit-lens readout at hidden_states index L and decision_i is the H6-registered decision (archived, §3.2). Contrast **C = mean(f_L : L ∈ {16..24}) − mean(f_L : L ∈ {0..8})**, computed over non-degenerate layers only (§3.5).

---

## 3. Method

### 3.1 No-generation protocol [ASSUMPTION]

Zero generation, identical to H6: one forward pass per (item, layer) for the readout; only the final (answer) position is read. If any execution step required generation, the run would HALT rather than substitute an elicitation.

### 3.2 Bench, decision target, provenance [PROPOSITION]

- **Bench:** the 60-item EXP107 template-decorrelated bench — identical provenance pin as H6 §3.2: canonical bench-JSON SHA-256 `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`; npz `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76`; embeddings-bytes `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123`; ids-bytes `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9`. `len(bench) == 60`. Any mismatch → HALT.
- **Decision target (fixed, not re-measured):** EXP112's archived per-item decision column (`experiments/runs/EXP112_hdildr/out/exp112_per_item.json`). **Pre-run consistency pin:** the executor loads the archived per-item readout and decision columns and recomputes fidelity — it must equal **41/60 exactly**; otherwise HALT (archive drift). This is a pin, not a metric re-test: the final-output fidelity value is an archived constant for H13.
- **Candidate entities / token ids:** E1 = tuple[0], E2 = tuple[-1], t1/t2 = the pinned single-token ids from EXP112's worksheet (re-asserted: `encode(" "+E)` is exactly one token on the real Pythia tokenizer; any failure → RUN-INVALID, items NOT dropped).

### 3.3 Layer sites and the logit lens [PROPOSITION]

- **Sites:** hidden_states indices L ∈ {0..8} ∪ {16..24} of frozen Pythia-410m (24 transformer layers; index 24 = final layer output). 18 sites, 60 items each.
- **Logit lens (pinned):** logits_L = LayerNorm_f(h_L) @ W_U, where LayerNorm_f is the model's final layer norm and W_U its unembedding matrix (Pythia-410m's lm_head has no bias). Readout: **readout_i,L = argmax(logit_L[t1], logit_L[t2])**; ties (exact float equality) → E2 (mirrors H6).
- **No training, no tuning of the lens.** The lens is the standard zero-training per-layer readout; its early-layer limitations are handled by the per-layer degeneracy diagnostic (§3.5), not by post-hoc exclusion.

The late window {16..24} contains the archived site (lens at L24 is the model's output logits), so the §3.2 consistency pin is a true byte-level identity check on the lens implementation.

### 3.4 Self-report context [PROPOSITION]

Identical to H6 §3.4: the item's `prompt` field verbatim (premise + `" Question: Who is higher in rank? Answer:"`, no trailing space). Readout at the final (answer) position only. Zero new wording.

### 3.5 Degeneracy handling — per-layer diagnostic + run-level validity rule [PROPOSITION]

- **Per-layer diagnostic:** for each site L, compute mean post-softmax mass on (t1, t2) — the G1 quantity. A site is **degenerate** iff mean mass < 0.01 (the H6 G1 rule). Site degeneracy is reported per site regardless of outcome.
- **Run-level validity rule (pre-registered):** window means are computed over **non-degenerate sites only**. If **fewer than 5 of 9 sites in either window are non-degenerate → RUN-INVALID** (logit-lens apparatus failure at this read site — the channel cannot speak; not a verdict). This blocks the false-CONTINUE path where a degenerate early window (e.g., constant readout → fidelity exactly 0.5) manufactures contrast.
- H6's G4 (decision-statistic health, 0.085052) and G2 (final-output readout variation) were verified in EXP112 and are carried as archived pins — not re-checked, because the decision column is archived (§3.2).

### 3.6 Frozen backbone [ASSUMPTION / Law #6]

- Snapshot `~/workspace/.exp086_weights/pythia-410m`; environment the registered EXP107/EXP108/EXP112 environment (torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, sklearn 1.9.1).
- Backbone parameter hash recorded **before and after** all fresh forward passes and compared against the LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (sha256 over sorted state_dict keys, float32 bytes). Any mismatch → RUN-INVALID, quarantine, no metric may be read.
- `model.eval()`; `torch.no_grad()` around ALL forward passes; `device_map="cpu"`; float32; torch/numpy seeds = 0; CPU thread count set and read back via `torch.get_num_threads()`.

### 3.7 Law #7 posture [PROPOSITION]

Identical to H6 §3.7: bench labels, phrasing, and flipped flags are never used — not as targets (no training), not in the metric (fidelity compares readout against the archived decision, never labels), not in any selection. Law #7 clean by construction; no train/test split, no item-ID tripwire.

### 3.8 Template posture [PROPOSITION]

Identical to H6 §3.8 (template-free by construction: no training, no labels, byte-identical carrier, decorrelated bench). **Deviation:** H6's descriptive per-cell diagnostic is **dropped** — cell stratification was killed at the H12 worth-it gate (p = 0.0946 noise); no decision branch and no diagnostic reads the cells in H13.

---

## 4. Decision bars with statistical license

Single pre-registered statistic C (no multiplicity). All license numbers verified at drafting (§0d).

| Outcome | Verdict | Statistical license — what the region means |
|---|---|---|
| C ≥ 0.10 **and** late-window fidelity ≥ 0.65 | **CONTINUE** | Late-layer localization is real. C ≥ 0.10 is 2–3.5σ from the no-locality null (two-sided p ≈ 0.04–4×10⁻⁴ depending on inter-layer correlation); late ≥ 0.65 demands the signal be present across the late window (the other 8 late sites must average ≥ 0.6458), not a single-site spike. The honesty instrument has a layer foothold. |
| \|C\| < 0.05 | **KILL** | Signal diffuse across the measured profile — no layer foothold. EXP112's HELD stands unchanged; the locality question is retired. |
| C ≤ −0.10 | **KILL** | Reverse concentration — the signal, if any, concentrates early, falsifying the registered late-locality hypothesis. |
| 0.05 ≤ C < 0.10 (any late), or C ≥ 0.10 with late < 0.65, or −0.10 < C < −0.05 | **HELD** | Indeterminate. Licenses nothing, retires nothing, no re-runs. |
| Any hypothesis rewording after seeing the metric | **BARRED** | Law #4: scientific misconduct, not a verdict. |

**Run-invalid branch (before any metric):** < 5 non-degenerate sites in either window → RUN-INVALID. **HALT branches:** bench/archive pin mismatch; backbone hash mismatch; consistency-pin failure (≠ 41/60).

**No rescue runs.** A HELD or KILL is never followed by a different window choice, a different lens, a larger n, or a re-read — each would be an unlicensed gate tweak (barred).

---

## 5. Degrees of freedom — pinned in advance

| Degree of freedom | Pinned value | Section |
|---|---|---|
| Bench / archive pins | EXP107 bench + npz + embeddings/ids bytes (H6 §3.2 pins, verbatim) | §3.2 |
| Decision target | EXP112 archived per-item decision column; consistency pin = 41/60 exactly | §3.2 |
| n | 60 items exactly; no subsampling | §3.2 |
| Token ids | t1/t2 pinned from EXP112 worksheet; single-token re-assertion (failure → RUN-INVALID) | §3.2 |
| Layer sites | hidden_states indices {0..8} ∪ {16..24} (18 sites) | §3.3 |
| Logit lens | final LayerNorm + unembedding, no bias; argmax over (t1,t2); ties → E2 | §3.3 |
| Self-report context | item `prompt` verbatim; final position; zero generation | §3.4 |
| Degeneracy | per-site mass < 0.01 → degenerate; < 5 non-degenerate sites/window → RUN-INVALID | §3.5 |
| Seeds / threads | torch = numpy = 0; threads set and read back | §3.6 |
| Backbone hash pin | LOG-331 pin before and after all fresh forwards | §3.6 |
| Contrast C | mean(f over non-degenerate late sites) − mean(f over non-degenerate early sites) | §2 |
| Per-cell diagnostic | DROPPED (H12 kill) | §3.8 |
| Decision bars | §4 table — no other reading licensed | §4 |

No other variable may be adjusted after the metric is seen. Anything not in this table was not measured.

---

## 6. Falsification decision tree

| Outcome | Verdict | Meaning |
|---|---|---|
| Bench canonical-JSON or npz/embeddings/ids pins ≠ pinned | HALT | Apparatus drift. Licenses nothing. |
| Consistency pin: recomputed fidelity ≠ 41/60 exactly | HALT | Archive drift in the archived decision column. Licenses nothing. |
| Backbone hash before/after fresh forwards ≠ LOG-331 pin | RUN-INVALID | Law #6. Quarantine. No metric may be read. |
| BPE single-token re-assertion fails on any item | RUN-INVALID | Tokenization contract broken; items NOT dropped. Not a verdict. |
| < 5 non-degenerate sites in either window | RUN-INVALID | Logit-lens apparatus failure — the channel cannot speak. Not a verdict. |
| C ≥ 0.10 and late-window fidelity ≥ 0.65 | CONTINUE | Late-layer localization is real. |
| \|C\| < 0.05 | KILL | Signal diffuse — locality question retired; EXP112's HELD stands unchanged. |
| C ≤ −0.10 | KILL | Reverse concentration — late-locality hypothesis falsified. |
| 0.05 ≤ C < 0.10 (any late), C ≥ 0.10 with late < 0.65, −0.10 < C < −0.05 | HELD | Indeterminate. Licenses nothing, retires nothing, no re-runs. |
| Any hypothesis rewording after seeing the metric | BARRED | Law #4. Scientific misconduct, not a verdict. |

---

**§7. Honesty fence**
### 7.1 EXP112's HELD is untouchable
No H13 outcome — CONTINUE, HELD, KILL, or RUN-INVALID — changes EXP112's registered HELD verdict (41/60). H13 asks where the signal lives, not whether H6's existence question re-verdicts. A CONTINUE licenses layer-window localization of the self-report signal as a mechanistic foothold for later, separately-licensed lanes only; it does not upgrade, re-open, or re-measure EXP112.
Fidelity between two readouts of the same frozen backbone is a decoding correlation, not honesty in any introspective sense; a localized signal is a layer window, not a mechanism.

**§8. Cost / honesty statement [FACT]**
- $0 compute. No GPU contact. No training. Backbone frozen, Δθ=0.
- ~1080 forward passes (60 items × 18 layer sites), CPU, float32, zero generation — comparable to EXP112's 180 forwards in ~86 s; inside the licensed $0 CPU envelope.
- This lane drafts only: no execution, no experiment number minted, no signed protocol touched, no push, no PR.

**§9. What H13 does NOT claim**
1. A CONTINUE does not claim the model "knows" its decision in any introspective sense — only that the two-way logit-lens readout's agreement with the registered decision statistic concentrates in late layers.
2. Not consciousness, not deceptive intent, not generality beyond the 60-item bench, not capability of any kind.
3. A KILL retires the locality question only — EXP112's HELD stands unchanged; the summit program is unaffected.
4. A HELD licenses nothing and retires nothing — no larger-N rescue, no different window, no different lens, no re-read (all barred).
5. Novelty: N1 — Known Combination (logit lens is a known instrument applied to a new question — Law #10).
6. Unsigned and unreviewed until the independent Law #14 lane signs or rejects.

**§10. Deviations from H6's pre-registered spec (complete list)**
1. **New question:** H6 measured the self-report signal's existence at one read site; H13 measures where it lives across 18 sites. The contrast C, windows, and bars are registered before any per-layer forward; H6's "No rescue runs" clause (H6 §4) bars re-running the *existence* question, which H13 does not do (see §0c).
2. **18 layer sites vs one:** hidden_states indices {0..8} ∪ {16..24} (final logits = lens at L24) vs H6's single final-logits site.
3. **Logit-lens readout:** LayerNorm_f(h_L) @ W_U per site vs H6's output logits — identical at L24 by construction; no lens tuning.
4. **Per-site degeneracy diagnostic + run-validity rule (§3.5):** new — the H6 G1 rule applied per site, with < 5 non-degenerate sites/window → RUN-INVALID.
5. **Contrast statistic C** replaces the fidelity metric as the primary statistic; fidelity becomes a per-site component.
6. **New decision bars:** CONTINUE/HELD/KILL on C and late-window fidelity (§4), replacing H6's fidelity bands.
7. **Consistency pin** on EXP112's archived decision column (41/60-exact HALT-on-drift): new.
8. **G1/G2 guards** carried as archived pins, not re-checked (decision column is archived, §3.2).
9. **Per-cell diagnostic dropped** — cell stratification was killed at the H12 worth-it gate (p = 0.0946 noise).
10. **Option-embedding forwards dropped** — decision column is archived; no 120 fresh single-token forwards.
11. **Compute:** ~1080 forwards (60 × 18 sites) vs H6's 180; still $0 CPU.
12. **Novelty unchanged:** N1 — Known Combination (H6 §8.6 equivalent).
