# S3 Stage-0 Pilot Feasibility Inventory — LOG-208 (2026-09-23)

**Role:** Track-6 data specialist. **Log:** LOG-208 (pre-assigned by the CEO).
**Scope:** $0 read-only inventory of the program's archives. No weights touched,
no forward passes run, no GPU used, no signed artifact modified.
**Status-label standard:** every entry below is `[OBSERVATION]` (a file listing
or file read). This document contains no verdicts, no interpretation, no pilot
design, and no comment on K1 or the bridge.

**Law #15 answers (on record):**
1. Q: Do the archives contain the data the three Stage-0 pilots need? — See the
   three check sections below (contents manifest only).
2. Decision: CONTINUE — feasibility gates the $0 pilots; missing data ⇒ a pilot
   is re-scoped or dropped before design, not after.
3. Cheapest: $0 read-only inventory; no weights, no forward passes, no GPU.
4. License: n/a, stated honestly — this is an inventory, not an experiment; it
   makes no mathematical claim.

**Method:** file listings (`ls`/`find`) plus key-schema reads (Python `json`)
of the archived result artifacts; binary header/string inspection of the single
`.pt` artifact (torch not installed in this environment; contents cross-checked
against the archiving statement in the runner code that wrote it).
Directories scanned: `experiments/runs/` in full (all EXP065/066/077 archive
directories), plus repo-wide filename and content searches for
`attention`/`residual`/`snapshot`/`logit`-lens artifacts and for `"logits"`
keys in `experiments/` and `evaluation/`.

---

## Check 1 — S3-1 (ARP): per-layer attention snapshots in the archives

**Needed by the pilot gate:** per-layer attention-pattern snapshots (with and
without intervention) for the archived EXP065/066/077 interventions.

### Files found (EXP065 archive)

`experiments/runs/EXP065_coordinate_alignment/`
- `exp065_results.json` (4,843 bytes) — keys: `experiment`, `model`,
  `pre_hash`, `post_hash`, `layer`, `alpha`, `sample_size`, `baseline_accuracy`,
  `stage_A_alignment_discovery` (4 records: `vocab`, `raw_cosine`,
  `aligned_cosine`, `delta_cosine`), `stage_B_confirmatory_results`,
  `stage_C_specificity_results`, `criteria`. Contents: aggregate tables only.
  Per-layer attention snapshots: **absent**.
- `exp065_run_log.txt` — run log (not read in full for this inventory).
- Per-item records file: **absent**. Per-layer activation records: **absent**.

### Files found (EXP066 archive)

`experiments/runs/EXP066_pythia410m_replication/`
- `exp066_replication_results.json` (4,748 bytes) — aggregate summary tables
  (`stage_A_alignment` 4 records, `stage_A_summary`, `stage_B_conditions`,
  `stage_C_specificity`). Per-layer attention snapshots: **absent**.
- `exp066_instance_evaluations.json` (75,390 bytes) — 60 item records
  (`pythia410m_planet_2hop_0..14`, `pythia410m_planet_3hop_0..14`,
  `pythia410m_element_2hop_0..14`, `pythia410m_element_3hop_0..14`). Per-item
  keys: `prompt`, `base_correct`, plus per-condition `*_correct` (boolean) and
  `*_margin_shift` (float) for `Static_B_agg`, `Aligned_Dynamic_Basis`,
  `Same_Layer_Output_Bridge`, `Random_Rotation_Seed_0..4`, `Dynamic_B_perp`,
  `Dynamic_B_wrong`. Contents: booleans and scalars only; no logit vectors, no
  attention patterns, no per-layer activations.
- `exp066_run_log.txt` — run log.
- Per-layer attention snapshots: **absent**.

### Files found (EXP077 archive)

`experiments/runs/EXP077_cone_vs_line/`
- `exp077_results.json` (9,180 bytes) — aggregate tables and endpoint
  statistics (`alpha_grid`, `cone`, `angular`, `control`, `offset`,
  `replication`, `radial`, `stage_B_conditions`, `bridge_gate`,
  `rescue_indicator_counts`, `interpretation_notes`, `env_manifest`). Per-layer
  attention snapshots: **absent**.
- `exp077_instance_records.json` (31,348 bytes) — 60 item records; keys per
  item: `item`, `ent`, `typ`, `correct` (per-arm booleans — see Check 3),
  `rescue_indicators` (binary flags). No attention patterns, no per-layer
  activations.
- `exp077_vectors.pt` (137,237 bytes) — archived intervention **vectors only**:
  `v_hat`, `v_hat_c`, `mu`, `v_hats`, `v_hat_c_ks`, `u_list`, `w_list`,
  `q_list`, `r_vec`, `B_wrong`, `B_perp_basis`, `pre_hash`, `post_hash`
  (verified via pickle-string inspection and the archiving statement in the
  runner). No attention tensors, no activation tensors.
- `exp077_run_log.txt` — run log.

### Repo-wide search result
- No file named `*attention*`, `*residual*`, `*snapshot*`, or `*logit*lens*`
  exists anywhere in the repo (excluding `__pycache__`).
- The strings `attn_weights`/`attention_weights` do not appear in any archived
  JSON in `experiments/`. The string `"logits` appears only in runner *scripts*
  (`experiments/scripts/run_exp009_suffix_surface.py`,
  `experiments/scripts/run_exp031_adaptive_cascade.py`), not in archived
  results.

### S3-1 check summary
- Per-layer attention snapshots for EXP065/066/077 interventions: **absent**
  from all three archives. What exists instead: aggregate cosine tables
  (EXP065/066), per-item correctness/margin-shift scalars (EXP066), and
  intervention vectors (EXP077 `exp077_vectors.pt`).

---

## Check 2 — S3-3 (DUG): mid-layer residual snapshots in the archives

**Needed by the pilot gate:** mid-layer residual snapshots (for the logit lens)
and archived logits for the headroom items of the relevant runs.

### Files found
- The only files that could carry per-item activations are the ones listed in
  Check 1. Contents of each, with respect to residuals/logits:
  - `EXP065/exp065_results.json`: aggregate cosine scalars only — **absent**.
  - `EXP066/exp066_instance_evaluations.json`: per-item booleans and
    `*_margin_shift` scalars only — raw logit vectors **absent**, mid-layer
    residuals **absent**.
  - `EXP077/exp077_instance_records.json`: per-arm correctness booleans and
    binary rescue indicators only — raw logit vectors **absent**, mid-layer
    residuals **absent**.
  - `EXP077/exp077_vectors.pt`: static intervention vectors only — residuals
    **absent**.
- No `.npz`, `.safetensors`, or other tensor-archive files exist in the repo
  (only one `.pt` file, listed above).
- The EXP067/EXP070/EXP075/EXP079 runner scripts call `model(..., output_hidden_states=True)`,
  but those experiments have no local result artifacts (GPU-dark; nothing
  executed to archive), so they contribute no archived snapshots.

### S3-3 check summary
- Mid-layer residual snapshots: **absent** from all archives.
- Archived raw logits (per-item logit vectors): **absent** from all archives.
  Closest existing datum: EXP066 per-item `*_margin_shift` scalars and
  `base_correct`/per-condition `*_correct` booleans.

---

## Check 3 — S3-4 (SAH): EXP077 α-sweep ledger

**Needed by the pilot gate:** the α-sweep ledger — per-instance α values and
outcomes.

### Files found
`experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`
(60 items), per item:
- `correct` — per-arm binary outcomes with keys:
  `C1` (baseline), `C2_a025`, `C3_a050`, `C4_a100`, `C5_a200` (cone arm at
  α = 0.25 / 0.5 / 1.0 / 2.0), `C6_offset`, `C7_Bwrong`, `C8_bridge`,
  `C9_cone`, `C10_control`.
- `rescue_indicators` — binary flags with keys:
  `L_C4`, `K_C9`, `R_C10`, `O_C6`,
  `A_alpha_0.25`, `A_alpha_0.5`, `A_alpha_1`, `A_alpha_2`
  (per-α rescue flags for the radial/cone arm at α = 0.25 / 0.5 / 1.0 / 2.0).

`experiments/runs/EXP077_cone_vs_line/exp077_results.json` — corroborating
aggregate: `alpha_grid: [0.25, 0.5, 1.0, 2.0]`, `radial: {alphas, p_values,
delta_ms, ...}`, and `stage_B_conditions: {C_alpha_0.25, C_alpha_0.5,
C_alpha_1, C_alpha_2, C1, C6_offset, C7_Bwrong, C8_bridge}` (aggregate
statistics per arm).

### Coverage notes (from the archived records themselves)
- Per-instance α values recorded: {0.25, 0.5, 1.0, 2.0}.
- Per-instance outcomes at each α (binary correct/wrong plus binary rescue
  flag) are archived **for the cone arm (C2–C5 / A_alpha_*)** — 60 items ×
  4 α values.
- `C7_Bwrong` and `C8_bridge` are recorded as single-arm per-instance
  booleans (one value per item each); the archive holds no per-α records for
  these two arms.
- No raw per-instance logit values are archived; outcomes are binary.

### S3-4 check summary
- α-sweep ledger: **present** for the cone/radial arm (per-instance α values
  {0.25, 0.5, 1.0, 2.0} with per-instance binary outcomes and binary rescue
  flags; 60 items). Per-α per-instance outcomes for the bridge arm and the
  B_wrong arm: **absent** (single fixed-α records only).

---

## Overall manifest (no verdicts)

| Pilot gate datum | Location | Status |
|---|---|---|
| Per-layer attention snapshots (any intervention, any run) | — | absent |
| Per-layer activation snapshots (any intervention, any run) | — | absent |
| Mid-layer residual snapshots | — | absent |
| Raw per-item logit vectors | — | absent |
| Per-item correctness + margin-shift scalars (EXP066) | `experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json` (60 items) | present |
| Aggregate cosine/alignment tables (EXP065/066) | `experiments/runs/EXP065_coordinate_alignment/exp065_results.json`, `experiments/runs/EXP066_pythia410m_replication/exp066_replication_results.json` | present |
| Intervention vectors (EXP077) | `experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt` | present |
| α-sweep ledger: per-instance α {0.25,0.5,1.0,2.0} × binary outcomes (cone arm, 60 items) | `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` | present |
| Per-α per-instance outcomes for bridge / B_wrong arms | — | absent |
| EXP078/EXP067/EXP079/EXP070/EXP075 archived results | — | absent (bundle/package directories only; no result artifacts) |

**Gap list (files/values absent):** per-layer attention snapshots; mid-layer
residual snapshots; per-layer activation records; raw logit vectors;
per-item records for EXP065; archived results for EXP067/070/075/078/079;
per-α per-instance outcomes for the EXP077 bridge and B_wrong arms.

*End of LOG-208 inventory. Contents manifest only; no verdicts, no
interpretation, no pilot design, no comment on K1 or the bridge.*
