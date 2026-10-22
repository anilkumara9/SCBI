# Law #14 Independent Review — EXP133 Amendment B (breaking point (b) + §3.3)

**Lane:** independent Law #14 reviewer. **LOG-4801** (CEO pre-assigned). **Date:** 2026-09-30.
**$0 CPU, paper-only.** Read-only on signed protocols, weights, and artifacts.
No model runs, no GPU contact, no commits, no pushes, no spend, no publish, no dispatch,
no experiment number minted, no execution licensed.

**Artifact reviewed (exact version):** `~/workspace/SCBI/research/prereg/EXP133_AMENDMENT_B_2026-09-30.md`
(DRAFT amendment to the CEO-signed GEOSTEER pre-reg, LOG-4798).

**Review-only fence:** I did not author the amendment. I edit nothing under review, apply no
repairs, license nothing, advance no pipeline. The only writes from this lane are this
review file and the single LOG-4801 research-log entry recording it.

**Independence confirmed.** The amendment was authored by the LOG-4800 recovery lane
(verified in the LOG-4800 entry). I am a different lane; I authored neither the pre-reg,
the gate, nor the amendment.

---

## Verdict: SIGN

The amendment is narrow, honest, and mechanically sound. All six checklist items pass.
No blocking findings. One advisory note (§7, non-blocking).

---

## §1 — Checklist

### 1. Narrowness — PASS
The amendment touches ONLY breaking point (b) and §3.3. §4 explicitly enumerates
everything unchanged: the decision table (including the B2 DEFAULT → INCONCLUSIVE row),
norm budget B = 0.50578119 and its §0(d) audit, breaking points (a) and (c)–(g), the
7-arm design, the H1/H6 §3.3 readout, the PIVOT/CONTINUE/KILL bars, and the founder-gated
GPU fence. I verified §4's list against the signed pre-reg's structure — no silent
alteration of definitions, metrics, or decision logic (Laws #4, #5, #9 clean).

### 2. v2 recovery honesty — PASS
- Parameters verified in-repo: seed `20260929_4714` (`run_exp131.py:386`), K=40 fixed
  iterations (`run_exp131.py:384`), §7 header citing the LOG-4714 erratum.
- LOG-4714 (research log line 13417) records the derivation as "Law #4 deterministic
  given seed + apparatus + frozen backbone" with the orthogonality assert
  |v̂₂,iᵀ v̂₁,i| < 1e-6. The amendment's citation is accurate.
- The original "re-pin only" prohibition is explicitly STRUCK and replaced with licensed
  deterministic reproduction — superseded openly, not silently violated (Law #4 clean).
- The no-ground-truth-hash caveat is labeled [CONJECTURE] and stated plainly: ulp-level
  GPU-vs-CPU differences cannot be excluded. This is the honest epistemic position —
  the amendment does not overclaim bit-identity with EXP131's v2.

### 3. B_agg hash gate — PASS
The pin `d3556d83751634a2fc5114d56c4ee246bb1b296293d2adcde40a369da1600ae1` was
verified verbatim in EXP131's records (`experiments/bundles/exp131_v1inj/out/exp131_records.json`
→ `pins.bagg_reconstruction`). The gate (reproduce → hash must equal pin, else
apparatus-void) is correctly specified and gives B_agg full ground-truth verifiability —
stronger than v2's position, as the amendment honestly notes by contrast.

### 4. Rank-trend robustness — PASS (sound)
The rank-trend gate compares v̂₁-effect vs v̂₂-effect magnitudes within the same pilot.
Ulp-level direction differences cannot invert a rank ordering unless the two effects are
themselves within ulp of each other — in which case the outcome is null-adjacent and the
decision table's other conjuncts (McNemar, random-path null) govern. The orthogonality +
unit-norm asserts bound the reproduction to the correct mathematical object (the K=40
deflated second singular direction). Sound.

### 5. §5 checklist addition — PASS (well-formed, correctly scoped)
The paragraph requires future reviews to inventory-verify artifact contents cited by
breaking points (key listing with shapes alongside the breaking-point text; missing
cited content = BLOCKING finding). This is the correct process fix for the defect class
that survived LOG-4792/4793/4797, and it is explicitly labeled as a process fix,
licenses nothing, and changes no science.

### 6. Status honesty — PASS
"DRAFT — licenses nothing" is stated in the header; "It licenses no execution; EXP133
re-execution requires independent review of this amendment + fresh CEO clearance" is
explicit. No hidden licensing language found.

---

## §2 — Factual verification performed

- `exp127_vectors.npz` exists at `experiments/runs/EXP127_tga/out/exp127_vectors.npz`
  (2,479,790 bytes); the void report's key inventory (10× v1__, 10× urand__, 0× v2__/bagg__)
  is consistent with the amendment's §1.
- B_agg pin verified verbatim against EXP131's records (see §1.3).
- Seed, K=40, §7 derivation, and LOG-4714 determinism assertion verified in-repo and
  in-log (see §1.2).
- No numbers invented by the amendment; every cited value traces to a pinned artifact
  or a log entry.

## §3 — Laws check

No Law #2 (no invented results), #3 (citations accurate; GEOSTEER claim properly
UNVERIFIED-tagged upstream), #4 (no hypothesis shift — the scientific question and
decision table are untouched), #5 (no definition changes), #9 (no metric changes),
#11 (epistemic labels correct, including the honest [CONJECTURE]) violations.

## §4 — Advisory (non-blocking)

**A1:** When the pilot re-executes under this amendment, the run-twice determinism check
(§3.1) should log both SHA-256 values even on pass, so a future auditor can confirm the
check ran rather than being asserted. Not required for SIGN — the gate is correctly
specified as apparatus-void on miss.

---

## §5 — Disposition

**SIGN.** Amendment B is approved as drafted. Upon CEO clearance, EXP133 may re-execute
under the signed pre-reg as amended by B, with breaking point (b) replaced by (b1)–(b3)
and §3.3 by the amendment's recovery + verification discipline. Nothing else in the
signed pre-reg is altered.
