# EXP144 — Execution Report (Step-0 INCONCLUSIVE, 2026-10-05)

**Outcome: INCONCLUSIVE (bench non-portable)** — S7-2 §3.2 G1′ (tokenizer
cover) fired at Step 0, before any weight access. **No verdict was produced.
No forward passes were executed. No weights were downloaded.** The
Decodability Gap itself is untested in GPT-2-small, not falsified.

**Mode:** real (Step-0 only). **Clearance:** CEO dispatch on LOG-4918 SIGN
(minted EXP144). **Compute:** $0 CPU; 0 model forward passes.

---

## 1. Step-0 guard sequence (from `exp144_step0_log.txt`)

| Step | Result |
|---|---|
| Model revision resolve (`gpt2` → `openai-community/gpt2`) | `607a30d783dfa663caf39e06633721c8d4cfcd7e` (40-hex, recorded programmatically — S0.2) |
| G0 bench provenance (committed EXP092 builder, re-executed) | pass — pin `9be8162633fe19aa…` (identical to EXP092's committed pin, confirming procedural identity), 60/60 unique tuples, strata match §2 |
| G2 oracle diagnostic (artifact re-verified, bound to pin) | pass — oracle=0.0607, p=0.5312 ≥ 0.05 |
| Tokenizer files downloaded (weights NOT downloaded) | 13 files, revision-pinned |
| S0.2 pin recorded | `607a30d783dfa663caf39e06633721c8d4cfcd7e` in `exp144_manifest.json` |
| **G1′ real-tokenizer cover (GPT-2 BPE, offset mapping)** | **FAIL — 232/240 single-token** |

G1′ failure line:

```text
INCONCLUSIVE: G1' FAIL: 8 A/C occurrence(s) not covered by exactly one token
(e.g. exp092_planetary_2hop_3/target/Triton@(59, 65)→['ĠT', 'rit', 'on']; ...)
```

Runner exit code 1 (INCONCLUSIVE). The model weights were never downloaded;
the extraction, decode, and intervention arms never started.

## 2. Diagnosis: one entity is intrinsically multi-token under GPT-2 BPE

The full per-entity cover table (`exp144_g1prime_mismatch.json`, diagnostic
using the same offset-mapping logic as the committed `g1prime` module):

- **Failing entities: ['Triton'] only.** 0/8 in-prompt occurrences
  single-token; GPT-2's BPE segments it as `ĠT` + `rit` + `on` (3 tokens).
- **All other 19 entities pass 232/232** (planetary: Mars, Venus, Jupiter,
  Saturn, Mercury, Europa, Titan, Io, Miranda; elemental: all 10).

The 8 failing occurrences are the 4 bench items where Triton is the target
or foil (2 in-prompt occurrences each: premise + question). Triton is
intrinsically unsplittable-as-one-token under this BPE vocabulary — no
prompt rephrasing can fix it without changing the entity itself.

## 3. Why the execution lane did not substitute the entity

The signed plan's G1′ clause is explicit: "No silent entity substitution: if
the ported builder cannot satisfy G1′, the run is INCONCLUSIVE
(bench non-portable), with the tokenization mismatch documented."

Substituting Triton (e.g. for another planet) would change the committed
bench-builder procedure — a different bench, a different 64-hex pin, a
different 20-target/3× balance — i.e. a **protocol modification**, which this
lane is not licensed to make ("no modification of signed artifacts"; a
design change becomes a new experiment number, never a silent edit to a
signed protocol). The single-lane fence applies: the executor stops at its
lane and reports back; self-repair is the EXP093 lesson's forbidden move.
The mismatch is documented above instead.

## 4. Weight integrity

- No weights were downloaded or accessed at any point. The only network
  fetch was the 13 tokenizer/config files at the pinned revision.
- **Δθ = 0 stands trivially** — there is nothing to mutate.

## 5. Environment manifest (Step-0 phase)

| Component | Version |
|---|---|
| Python | 3.12.3 |
| transformers | 5.17.0 (tokenizer only; torch absent in this venv) |
| huggingface_hub | 1.33.0 |
| numpy | 2.5.3 |
| torch | not installed in the Step-0 venv (by design — G1′ must precede weight access) |
| Model revision (pinned, S0.2) | `607a30d783dfa663caf39e06633721c8d4cfcd7e` |
| Bench pin | `9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4` |
| Threads | nproc=2 (pin 2 planned for the unreached phases) |

Execution venv staged (unused): `~/.exp_venvs/exp142` (torch 2.14.1+cpu,
transformers 5.17.0, hub 1.33.0, numpy 1.26.4).

## 6. Registered implication

**None on the science.** An INCONCLUSIVE is withheld, never a verdict (§3.6).
The cross-family question — whether the Decodability Gap replicates outside
Pythia/GPT-NeoX — is still open; S7-2 tested nothing about the dissociation
itself. The only licensed claim from this run: *the EXP092-B bench is not
portable to GPT-2's BPE as designed (Triton is 3 tokens); a cross-family
replication on GPT-2-small needs a re-registered bench* (documented entity
substitution, or a multi-token-tolerant variant) *under a new experiment
number.*

## 7. Artifacts (preserved, Law #8)

- `exp144_manifest.json` — revision pin, bench pin, G0/G2 evidence, G1′ FAIL disposition
- `exp144_step0_log.txt` — full Step-0 stdout
- `exp144_g1prime_mismatch.json` — per-entity cover table (232/240; Triton 0/8)
- `exp144_g1prime_diagnostic.py` — the diagnostic script
- `exp144_step0_download.py`, `exp144_extract.py`, `exp144_decode.py`,
  `exp144_directions.py`, `exp144_inject.py`, `exp144_decision.py`,
  `exp144_verdict.py`, `exp144_common.py` — the full execution bundle,
  staged but unexecuted past Step 0 (kept for the re-registered follow-up)
- `hf_cache/` — tokenizer/config files at the pinned revision only (no weights)

**Forward budget consumed: 0 / 1,000. Cost: $0.**
