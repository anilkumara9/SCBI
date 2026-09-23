# Law #14 Adversarial Review — G2 Oracle-Ceiling Pre-registration, Round 2 (LOG-171)

**Verdict: SIGN** — the DRAFT banner may advance to **PRE-REGISTERED**.
**Role:** Law #14 Adversarial Reviewer (LOG-171 dispatch; answers to the CEO; no instruction to soften was accepted or followed)
**Date:** 2026-09-23
**Target:** `experiments/protocols/G2_ORACLE_CEILING_PREREG_SPEC.md` (LOG-167 revision of the LOG-143 draft)
**Banner authorized:** **PRE-REGISTERED** on this SIGN. No experiment number is minted by this review (the spec reserves numbering to signing; next free EXP080 at time of drafting — the CEO's signing step mints it). **No GPU launch** — execution still requires explicit CEO clearance.
**Scope:** analysis only — no GPU, no experiments. Every load-bearing claim below was independently re-verified against the archived EXP078 runner source, not trusted from the reviser's summary.

---

## 0. Re-verification of the reviser's B1–B4 claims (each attacked independently)

### B1 — Path A rebuild: HELD ✓

**Runner-source verification (independent of the reviser's):**
- `run_exp078.py` L543: `save_halt("HALT_ENERGY", ...)` → L555: `sys.exit(0)`. The `save_halt` definition (L330–349) persists only `exp078_results.json` + the run log — no vectors.
- `torch.save(archive, ... "exp078_vectors.pt")` at L750 — strictly after the energy gate, unreachable on the halt path.
- Filesystem sweep of `~/workspace`: no `exp078_vectors.pt` exists (the search is functional — it finds `experiments/runs/EXP077_cone_vs_line/exp078…/exp077_vectors.pt`). RUNBOOK.md checklist item "`exp078_vectors.pt` exists" remains **unchecked** (L106).
- The false provenance claim is deleted everywhere: the exact string "smoke run built and persisted" appears **exactly once** in the revised spec (§3.1 item 9), as the quoted retracted claim. No other occurrence.

**Rebuild executability (§3.1a) — checked line-by-line against the archived code:**
- `SUPPORT_VOCABULARIES`: all five name lists match the runner L125–133 verbatim.
- `TRIPLES_INDICES` (15) and `QUADS_INDICES` (15), including the deliberate repetition patterns, match L140–148 verbatim.
- Prompt templates (outranks/next-to, "`$A$ or `$C`" parity, 4-entity quad analog), `hidden_states[TARGET_LAYER + 1]` last-token, `.detach().cpu()`: match the support loop (L359–387).
- Algebra: stack [30, d] → row-normalize → mean → renormalize → `[d,5]` stack → SVD rank ratio → `torch.linalg.qr(V, mode="reduced")`: matches `build_subspace_S` (L199–220). The 1e-12 normalization epsilon in the archived code is **not** pinned in the spec — noted as non-blocking nit n1 below (the SHA-256 is *recorded at build time*, not pre-registered, so no hash can mismatch by construction; the epsilon is numerically inert given the guard-anchored non-zero deltas).
- Seeds: `SEED_TORCH = SEED_NUMPY = 20260923` at runner L109–110, matching the spec's determinism pin; `RANK_GUARD_RATIO = 1e-6` (L116) matches the spec's rank guard; orthonormality guard `< 1e-5` is a new pre-registered guard, fine as specification.
- No-peeking: the rebuild function sees only pinned constants + model weights; the 300 forward passes are on pinned support prompts, never benchmark items. Executable as pre-registered.

**Attack-surface (1) — "weight-only or smuggled forward pass?"** The rebuild is **not** weight-only, and the spec does not pretend otherwise: the 300 forward passes (5×30×2) are counted honestly in the budget (§10) and the §3.1a rationale states "~15s GPU" cost. The weight-only property is correctly claimed only for the self-bridge $b(x)$ (§3.1 item 1) and the static members, where it is true. Nothing is smuggled; the arithmetic accounts for every pass. Attack resolved.

### B2 — Lemma L1 + audit + license gating: HELD ✓

**L1 statement and proof (§4.5):** stated as [FACT]/[THEOREM]. The proof is airtight *under the determinism pin*: $B_{\mathrm{agg}} \in \mathcal{P}$ (item 10), selection is max-correctness, and the §4.1 tie-break draws only among the top-tied (i.e., correct) candidates — hence $\{\text{C2 correct}\} \subseteq \{\text{C3 correct}\}$ exactly, $c = 0$. The determinism pin is the load-bearing condition (two separate forward passes of $B_{\mathrm{agg}}$ must agree), and the spec correctly marks all reachability/power claims conditional on the pin (§6.1). The b-term branch mapping recomputed independently: (c)⟺$b\le5$ ($p=0.0625$ at $b=5$), (d)⟺$b\in\{6,7\}$ ($(6,0)\to p=0.03125$, $+10.0$pp $< +12$pp), (e)⟺$b\ge8$ ($(8,0)\to p=0.007812$, $+13.3$pp). All match.

**M5.2:** the tree is stated in $(p,\text{margin})$ terms (§9 precedence), which assigns every $(b,c)$ cell including $c>0$; §6.1 and §7 explicitly mark $c>0$ reachability as conditional on the pin. No unassigned cell.

**§7 audit:** the confounded $B^*(x)$-distribution audit is gone; replaced by the pre-registered marginal-rescue decomposition over $\mathrm{Corr}(x)$ with bins (i)/(ii)/(iii), plus the zero-cost C3-vs-C7 McNemar secondary. Zero extra passes is true: C7 is a test condition (counted in the 7×60) and $r(B;x)$ comes from the 600 oracle-selection passes. The (ii)≡(iii) identity on rescued items is correctly noted ($B_{\mathrm{agg}}$ wrong by definition on rescues).

**(d)/(e) gating — airtight:** §9(d) issues the "output room" license **only if** bin (ii) $> 0$; if bin (ii) $= 0$ the ruling must read "**bridge ceiling, not pool ceiling**" and program survival is qualified as resting on the bridge alone. §9(e) withholds Phase-B licensability entirely when bin (ii) $= 0$ ("the license conditions are unmet"). Survival cannot ride the bridge's back into an unearned "output room" license — the gate is textual, pre-registered, and unconditional.

**The kill still measures the pool ceiling, and that is now honest:** the (c) license carries the bridge-replication contingency verbatim as B2c required — "given C2-null replication, (c) ⟺ bridge rescues ≤ 5", the stand-down is on *the pool as measured*, and the report must distinguish *bridge-degradation* (bridge failed its historical 6) from *evaluator-failure* (target-free pseudo-bridges added nothing where the bridge rescued). The data to make that distinction is pre-registered (per-item $\mathrm{Corr}(x)$ sets including the bridge as member #1 and the 7 target-free pseudo-bridges; C7 replication read off the test conditions). The kill trigger itself stays a simple $p \ge 0.05$ per the m7 discipline — Law #8 honesty is in the *reporting*, not in a new branch. The source idea priced "the evaluator's selection prize"; the spec now admits the instrument is a bridge-dominated pool ceiling and gates every program-level license on the non-bridge marginal rescue. That is the most honest version of this design.

### B3 — 10-member pool, B_⊥/B_wrong as C5/C6: HELD ✓

Pool = {self-bridge, 7 pseudo-bridges, $P_S$-residue, $B_{\mathrm{agg}}$} = 10 (§3.1 items 1–10). The removal paragraph names the arithmetic-fitting history (Law #8). Zero stale references: no "12-member"/"12 pool" text, no 1,140/960/1,020 budget figures remain; $B_\perp$/$B_{\mathrm{wrong}}$ appear only in the removal paragraph and as C5/C6 test conditions. C4 is uniform over **10** (seed 7202 unchanged). Budget basis 10×60 + 7×60 recomputed below.

### B4 — (11,3) in impossible cells with proof: HELD ✓

§7 lists (11,3) with the full proof (L1 + $B_{\mathrm{agg}} \in \mathcal{P}$ ⇒ $c = 0$; three C2-correct/C3-wrong items cannot exist). §6.1 reachability restated in b-terms: (c) via $b \le 5$, (d) via $b \in \{6,7\}$, (e) via $b \ge 8$. The (5,0) m7 cell retained as the canonical positive-but-nonsignificant assignment. No partition gap is claimed. The remaining impossible cells ((0 margin with $p<0.05$, +12pp-but-not-(e), non-unit pool member) each carry proofs — M5.4 satisfied.

---

## 1. Minors m1–m7 (the two load-bearing ones plus the rest)

- **m1 ✓:** §4.1 retains direction-neutral tie-breaking but corrects the rationale — the EXP070 M3 citation is called out as misapplied (the tie-break cannot affect $b$ under correctness-argmax), kept for audit cleanliness.
- **m2 ✓:** §9(b) pins "McNemar $p<0.05$ **each vs C1**" for the C5/C6 specificity controls.
- **m3 ✓:** the C1 [40%,70%] band carries provenance (EXP067 headroom gate, LOG-129; EXP077 smoke C1=0.60).
- **m4 ✓:** "positive-control *detectability*" framing; explicit that branch (b) contains no C7 conjunct by design. The m7-style widening of the kill trigger is correctly not conflated with a validity requirement.
- **m5 ✓:** (a)/(b) carry "Evidentiary level: none (readiness halt/invalid run)"; (f) carries level 1; (g) carries "verdict: none; informational overlay by design."
- **m6 ✓:** §2 documents that the EXP067 registered sanity value `4c242d9a…` was computed over **unsorted** keys (LOG-123 root cause) and **must not be compared** against this protocol's sorted-keys computation; the binding guard is the runtime pre/post match. The hash-comparison trap is closed.
- **m7 ✓:** the degenerate-input "proof" is restated via L1 ($b=c=0$ is the only $b=c$ case under determinism; $p=1.0$ by convention); the kill trigger stays widened to $p \ge 0.05$ with the m7 cell assigned, not silent.

---

## 2. Budget and feasibility — arithmetic independently recomputed

$300$ (Phase-0 rebuild: 5 vocabs × 30 pairs × 2) $+$ $10 \times 60 = 600$ (oracle selection) $+$ $7 \times 60 = 420$ (C1–C7) $=$ **1,320** forward passes. Matches §10. Pseudo-bridge construction costs nothing extra (C1 logits reused); self-bridge and static members are weight-only; the $Q_S$ 300 is GPU-forward, counted, not smuggled.

Feasibility: $N_{\mathrm{final}} = 60 - n_{\mathrm{excluded}} = 60$ in closed form before the gate (LOG-138 discipline). The one non-determinism — Phase-0 build outcome — is evaluated in Phase 0 as readiness halt (a), before any selection spend; it is a *genuine* halt because the procedure passed its rank guard on both EXP078 runs (GPU and CPU smoke reached the energy gate, which is downstream of the rank guard). No EXP079-style structural shortfall is possible (no splits, no probe map, no attrition).

---

## 3. New attack-surface rulings

1. **Phase-0 rebuild:** executable as pre-registered; constants verified verbatim against `run_exp078.py` L109–148, L199–220, L359–387; the 300 forward passes are honestly budgeted, not weight-only-pretended. No smuggling. **Attack fails.**
2. **(c)-branch bridge contingency:** the kill stays simple ($p \ge 0.05$, m7 discipline); the bridge-replication contingency is a *reporting* requirement, not a new branch — bridge-degradation vs evaluator-failure is distinguished in the report using pre-registered per-item $\mathrm{Corr}(x)$ data (bridge = member #1, pseudo-bridges target-free). Law #8 satisfied. **Attack fails.**
3. **Law #7 bridge audit (unresolved):** the revision never assumes a bridge verdict. Every bridge-dependent statement is conditional ("given C2-null replication", "historical $b_{\mathrm{bridge}} = 6$"), C7 non-replication is explicitly "the measured ceiling, never invalidity," and the (d)/(e) licenses gate on measured bin (ii), not on bridge success. No silent assumption found. **Attack finds nothing.**

---

## 4. Remaining nits (non-blocking; may be fixed at signing or execution)

- **n1:** §3.1a does not pin the 1e-12 normalization epsilon from `build_subspace_S`. Numerically inert here; the SHA-256 is recorded at build time, so no mismatch is possible. Fix by copying the epsilon verbatim at signing.
- **n2:** §9 cites the "m8 precedent" for branch precedence — real (research_log L3058, EXP070 re-review) but the citation could name the log line. Harmless.

Neither nit touches a falsifier, a license, or the budget.

---

## 5. Verdict

**SIGN.** All four blockers held under independent re-verification; all seven minors implemented (m6's hash-comparison warning and m2's C5/C6-vs-C1 pin verified as the load-bearing ones); budget arithmetic recomputed (1,320 passes); the feasibility proof re-derived under the Phase-0 rebuild; the new attack surface (rebuild executability, (c)-contingency simplicity, Law #7 audit) attacked and resolved.

The banner may advance to **PRE-REGISTERED**. The experiment number is minted at signing (next free at drafting: EXP080). **No GPU until CEO clearance.** A design change after signing still takes the next free number (Law #4).

*No results exist under this protocol; no primary artifacts were touched; no numbers were invented; no research-log entry was written (LOG-171 covers this dispatch).*
