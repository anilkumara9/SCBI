# EXP067 — UNTESTED ASSUMPTIONS (Implementation Agent, 2026-09-23)

Everything below could NOT be verified on the build machine (no GPU, no torch,
no model download). The Kaggle/Colab run will hit these first. Each item is
labeled with its mitigation status in the implementation.

## A. Model / scope assumptions

- **A1 — 160m default is OUT-OF-PROTOCOL-SCOPE.** The signed protocol
  pre-registers `EleutherAI/pythia-410m` (layer 20, d=1024, 16 heads). This
  bundle defaults to `pythia-160m` (layer 10, d=768, 12 heads) per the free-tier
  execution directive. A 160m run does NOT satisfy the pre-registration; the
  output labels it `"protocol_scope": "OUT-OF-PROTOCOL-SCOPE"` and the
  evaluator prints the scope. Use `--model pythia-410m` for the in-scope run.
  (Design decision, not a bug.)
- **A2 — pythia-160m geometry unverified.** Assumed: 12 layers, d=768,
  12 heads, head_dim=64, `model.gpt_neox.layers[i]` layout, `embed_out`
  attribute. Target layer 10 = 83% proportional depth (EXP066's own comment
  convention: "Layer 10 on 160M" ↔ layer 20 on 410m). If the 160m checkpoint
  differs, the script asserts will fire on shape mismatches.
- **A3 — SHA-256 registered value exists only for 410m**
  (`4c242d9a…de936`). For 160m there is no registered hash; the run records the
  computed pre-hash as its manifest. Per protocol E-4, the BINDING guard is the
  runtime pre/post match (abort on drift); the registered value is a sanity
  check only and never an abort trigger. The script implements exactly this.

## B. HuggingFace / checkpoint internals (the dangerous ones)

- **B1 — `attention.dense` hook point.** Assumed: each
  `model.gpt_neox.layers[l].attention` has a submodule `dense` (nn.Linear,
  [d, d]) whose FORWARD INPUT is the merged per-head tensor
  `[batch, seq, d]` = concat(head_0 … head_{H-1}), each 64 dims.
  **Mitigation:** `collect_head_outputs` asserts a runtime self-check on EVERY
  anchor prompt: `sum_h o_h + bias == dense(merged)` to 1e-3. If HF's internal
  layout ever changes, the run aborts loudly instead of silently corrupting
  fits. The check was designed so it cannot pass on a wrong decomposition.
- **B2 — Head ordering.** The slice `merged[h*64:(h+1)*64]` assumes heads are
  laid out in index order. If the true order is a permutation, head INDICES are
  permuted but the experiment stays valid: H* selection, fits, and
  interventions are all per-index consistent, and the B1 self-check is
  order-invariant. No external head-identity claim is made anywhere.
- **B3 — Intervention hook point.** The script hooks the whole
  `layer_module` (GPTNeoXLayer) output and adds the vector — IDENTICAL to the
  EXP066 harness (layer output ≡ residual stream post-layer, the point at
  which `hidden_states[target_layer+1]` is read). Assumed unchanged between
  160m/410m; the parallel attention/MLP structure means the hook sees
  attn_out + mlp_out (+ residual passthrough, per HF's layer forward).
- **B4 — `embed_out` for the C4 bridge.** `model.embed_out.weight[tok, :]`
  assumed present with shape [vocab, d] (EXP066 used it; untied embeddings per
  protocol §2).
- **B5 — transformers version drift.** `AutoModelForCausalLM` /
  `AutoTokenizer` API assumed stable; GPTNeoX needs no `trust_remote_code`.
  requirements.txt pins lower bounds (`transformers>=4.44`) because free-tier
  images change; the run log records the actual environment manifest.

## C. Protocol ambiguities — conservative readings taken (all logged in code)

- **C1 — Support frame for (supp → V_test) fits:** protocol does not name which
  support vocabulary anchors the test-vocab rotation. Implemented V1_Anglo
  (matches EXP065/066 E_0 convention). Two rotations: V1→Planetary, V1→Elemental.
- **C2 — Anchor pairing:** index-aligned (entity i ↔ entity i, template j ↔ j),
  role-matched by construction (5 entities × 16 templates = 80 pairs).
- **C3 — Guard violation scope:** rank/spectral violation on ANY head fit aborts
  the whole run → HALT_STAGE_A branch (a). (Protocol: "abort on violation".)
- **C4 — Fewer than K=4 passing heads:** H* = all heads with g_h > 0 (fewer than
  4); zero → Stage A halt. (Protocol fixes K=4 but cannot select 4 from fewer.)
- **C5 — The 16 anchor templates** are the implementer's construction, frozen as
  constants in the script (= the pre-registration). Template-choice sensitivity
  is unmeasured; templates are entity-frame and disjoint from test prompts.
- **C6 — Stage C dropped.** EXP066's specificity probes are NOT in the EXP067
  protocol; running them would add unregistered conditions (Law #9). Dropped.
- **C7 — C1 statistics** are defined (baseline vs itself: ΔM=0, b=c=0, p=1.0),
  not measured — mathematically exact, no forward passes needed.
- **C8 — C5 Haar sampling** via SVD of a Gaussian (matches EXP066's convention),
  seeds {11,22,33,44,55} per protocol; 5-seed mean reported like EXP066.

## D. Tokenizer / data assumptions (inherited from EXP066)

- **D1 — Single-token entities.** `tokenizer.encode(" "+name)[0]` assumes each
  entity/target/foil is a single token; multi-token names would silently use the
  first token. Same convention as EXP066 (Mars/Venus/…/Alice/… are single tokens
  in the GPT-NeoX tokenizer as far as is known — unverified here).
- **D2 — Anchor prompts use last-token head outputs**, consistent with the Δh
  last-token convention. Protocol says "when processing T_j(e)"; last-token is
  the documented reading.
- **D3 — No test-label leakage (Law #7).** Test-vocabulary anchors use
  test-vocab ENTITIES inside ANCHOR templates only — never test prompts,
  options, or answers. Protocol explicitly permits entity tokens.

## E. Free-tier environment assumptions

- **E1 — VRAM.** Estimated fp32: pythia-160m ≈ 0.7 GB, pythia-410m ≈ 1.7 GB.
  No optimizer state (no backward pass anywhere), short-prompt activations are
  small. Fits a T4 (16 GB) comfortably — estimated, not measured. If OOM,
  the honest fix is a smaller batch (already 1) — do NOT silently switch dtype
  without recording it (that would deviate from the EXP066 fp32 convention).
- **E2 — HuggingFace Hub access.** `EleutherAI/pythia-160m` / `pythia-410m`
  assumed public, no auth token. Requires **Internet: ON** in Kaggle.
- **E3 — Runtime estimate.** ~2,100 short forward passes total (560 anchors +
  300 support-contrast + ~1,260 Stage B). Estimated tens of minutes on a T4 for
  160m, 2–4× for 410m. NOT measured. Quota: Kaggle 30 h/week GPU — ample.
- **E4 — No checkpointing.** A crash/disconnect means re-running from scratch.
  Keep failed logs (Law #8: failed runs are data). Do not resume partial runs.
- **E5 — `torch.use_deterministic_algorithms(True)`** may warn or raise on CUDA
  for some ops; wrapped in try/except and logged. Determinism is best-effort on
  GPU; seeds are still fixed and the hash guard still binds Δθ=0.
- **E6 — Disk.** Model download ~0.6 GB (160m) / ~1.6 GB (410m); Kaggle disk is
  ample. `/tmp` is NOT used; outputs go to the run directory.

## F. Evaluator assumptions

- **F1 — Branch (b) vs (d) precedence.** If C4 fails, the run is INVALID even if
  C3 looks "falsifying" — the tree checks (b) before (d), per protocol table order.
- **F2 — Mixed-branch precedence** follows protocol table order c1 → c2 → c3.
- **F3 — Fail-safe `UNCLASSIFIED` branch** is honest engineering, not in the
  protocol; it fires only if no pre-registered branch matches (indicates a
  schema/logic error — investigate, do not interpret).
- **F4 — KL guardrail (< 0.50)** is reported, never branching (protocol lists it
  as secondary; §7 has no KL branch).
- **F5 — `--historical` dry-run mode** maps EXP065/066 schemas onto C3/C4 roles
  for evaluator self-testing only. Those runs used the UNSOUND operator, so the
  printed ruling is illustrative, never a protocol outcome.
