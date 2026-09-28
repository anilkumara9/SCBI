# The Decodability Gap — Falsification Kit

A runnable, model-agnostic bundle that lets anyone test steering claims on
their own language model. It operationalizes one question:

> **When a model "knows" the answer (the correct token is decodable in its
> logits), can an intervention at the decision point steer it there?**

The kit runs a two-phase protocol on a frozen model ($\Delta\theta = 0$):

1. **Tier-0** — a 60-item cloze bench ("*\<question\>* The answer is")
   scored by correct-token rank among 8 candidate logits. Binding bars decide
   whether the bench is even a valid instrument on your model:
   `LINE-CLOSED` / `KILL` / `UNDERDETERMINED` / `HOLD` / `TIER-0 PASSED`.
2. **Battery** — logit-level masking operators (arms B/T/F/R) on the Tier-0
   population, with McNemar-exact tests, Tango 95% CIs, and a binding
   decision table: `CONTINUE` / `PIVOT` / `KILL`.

## Quick start

```bash
pip install -r requirements.txt
# 1. sanity: the seven degeneracy unit tests (must all pass)
python tests/test_degeneracy.py
# 2. Tier-0 on your model (any HuggingFace causal LM)
python tier0.py --model-id EleutherAI/pythia-410m --out results/tier0.json
# 3. battery on the recorded logits (no model contact, $0)
python battery.py --records results/tier0.json --out results/battery.json
```

Reproduce the published EXP105 numbers without any model:

```bash
bash reproduce_exp105.sh
# expect: REPRODUCTION EXACT ✔  (KILL at step 9, dM_T=+0.2381, p=0.0625)
```

## Layout

| Path | What |
|---|---|
| `bench/cloze_bench.json` | 60 cloze items, 8 candidate pools, correct/foil indices, prompts |
| `core/scoring.py` | rank / top-1 / masking / McNemar / Tango / bar orders / decision table |
| `tests/test_degeneracy.py` | the seven §5 degeneracy unit tests (a)–(g), standalone |
| `tier0.py` | model-agnostic Tier-0 runner (`--model-id`, G1 gate, Δθ=0 guard) |
| `battery.py` | masking arms B/T/F/R + decision table on recorded logits |
| `reference/` | published EXP105 worksheets + the record adapter |
| `reproduce_exp105.sh` | one-command reproduction check |

## Reading the verdict

- **TIER-0 PASSED** — the bench is a valid instrument on your model; the
  battery is licensed.
- **LINE-CLOSED** — baseline < 0.25: the bench cannot measure two-hop recall
  on this model at all. Stop. (This is a finding about the instrument, not
  a failure of the run.)
- **KILL (battery)** — the licensed test could not certify a steering
  effect. On EXP105: truth-masking rescued 5/21 vs 0/21 for random masking —
  a clean direction, but the binding bar (p < 0.05) was missed by one flip.
- **What a Refuted verdict does NOT mean** — it is not evidence that masking
  is generic, and not evidence that no steering mechanism exists. It is
  evidence that *this licensed test, on this bench, at this power* could not
  certify specificity. The discipline is: exactly the test that was
  pre-registered, no re-runs, no larger populations, no post-hoc bars.

## Design notes (why the bench looks like this)

- **Cloze, not multiple-choice.** The lettered A)–H) format was measured to
  carry a position-A prior (30/60 top-1 at position 0, p = 2.02e-12) on the
  reference model — the format measured a readout artifact, not recall.
  Removing the letters (0.1833 → 0.5333 baseline) restored the instrument.
- **Tie-break by ascending token id**, applied only on exact float32 ties.
- **Structural foils** were designated before any model contact (D3
  blindness); the F arm is non-diagnostic when foil–top-1 overlap O > 0.5.
- **Frozen backbone**: weight SHA-256 is asserted identical pre/post run.

## Provenance

Built from the SCBI research program (research log LOG-4475…LOG-4491):
EXP104 Tier-0, the bench autopsy, S4-8/S4-8′ pre-registrations (signed), and
EXP105 Tier-0 + battery. No model weights are included in this kit.
Dependencies: `torch`, `transformers`, `numpy`, `scipy` (scipy only needed
for the exact Tango CI and test (f); a Newcombe-Wilson fallback is built in).
