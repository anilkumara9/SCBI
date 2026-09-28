# S6-3 v1 → v2 Delta Re-verification (2026-09-28)

**Lane:** independent delta re-verification (fresh; did not draft v1, did not review it, did not repair it).
**Target files:**
- v1: `research/innovation/S6-3_PREREG_DRAFT_v1_2026-09-28.md`
- v2: `research/innovation/S6-3_PREREG_DRAFT_v2_2026-09-28.md`
- Fix spec: `experiments/protocols/REVIEWS/S6-3_DRAFT_v1_LAW14_REVIEW_2026-09-28.md` (F1–F7, LOG-4436)

## Check 1 — v1 immutability
`sha256sum` of v1 = `4b26874a1a787b2dbd2b295a1ee0911bbed97824edb056fa27803d416a50a595` — **matches** the pre-repair hash exactly. v1 untouched. PASS.

## Check 2 — F1–F7 applied exactly as specified

- **F1** (CONTINUE-reachability window; KILL evidential weight; 8/F reporting): v2 §4.2 states the positive requires ≥8 directional flips on fired items only, hence unreachable at coverage < 8/60 (13.3%); names the **[10%, 8/60)** window with routings KILL (gated-T < 6, gated-R sub-threshold, LIVE) / PIVOT (gated-R ≥ 6) / Underdetermined (FROZEN). §0 decision block and §4.1 item 4 now read "flatness across the *fired* items" with the 0/6 → 95% upper bound 39.3% accounting. §4.2 and §5 item 8 require the verdict lane to report **8/F** alongside 8/N_realized. Exact per spec. PASS.
- **F2** (τ_i > 1 edge): step 0iii now asserts **E_i/N_i ≤ 0.5** for all 60 items (violation → HOLD — "the bench annotation is outside the gate's operating range"); §0.2 carries the one-sentence τ_i ≤ 1 operating condition. PASS.
- **F3** ("readout query" → mid-stack L11 + frozen rationale): hypothesis and mass_i definition reworded to "mid-stack (L11) attention from the final prompt token to the entity span"; §2.2 adds the frozen rationale (local-to-injection-layer self-consistency; mean-over-heads as the conservative frozen choice) and the one-sentence entity-span derivation (union of G1′-verified entity-occurrence token positions via the tokenizer offset map). PASS.
- **F4** (citation): "EXP096's differently-gated T moved **3/21** at this ratio." PASS.
- **F5** (τ wording + binding adjudication): "the conventional twice-uniform heuristic for concentration above chance"; §0.2 records the LOG-4436 binding adjudication verbatim (licensable as fail-safe pre-registered heuristic; the three license conditions; load-bearing for testability not validity); §6 risk 1 updated with the ruling. PASS.
- **F6** (step-4 scoping): disjunct (b) keeps "the directional claim's refutation is reported as an observation"; new sentence: "In disjunct (a), no refutation is reported — a directional signal, if any, is uninterpretable under matched-control fragility." Verbatim per spec. PASS.
- **F7** (vacuous-gate prose): step 2c pre-registers the exact weakened prose **"CONTINUE (directional signal at ratio 0.38; gating unattributed — the gate was vacuous)."** and requires the verdict lane to use it verbatim when the caveat attaches. Exact per spec. PASS.

## Check 3 — no unauthorized changes
Full `diff` reviewed hunk-by-hunk (86 diff lines). Every change traces to F1–F7 or to standard repair bookkeeping (v1→v2 header labels, status line, licensing chain +LOG-4435/4436, sources +LOG-4435/4436, v2 footer recording v1's hash). No new design, no bar change, no invented numbers, no rewording outside the fix scope. The apparent "���" in one diff line is a terminal rendering artifact of a pre-existing U+2192 (→) arrow — verified byte-identical (`342 206 222`) in v1 and v2 via `od -c`. PASS.

## Check 4 — v2 header discipline
v2 header: "DRAFT v2 — UNSIGNED... awaiting independent delta re-verification (separate lane), then CEO clearance"; v1's SHA-256 recorded in the header and footer. No pilot authorized. PASS.

## Verdict: SIGN

All four checks pass. The repair lane's claims are verified: F1–F7 applied exactly, v1 byte-identical, nothing else changed. v2 is authorized to proceed to CEO execution clearance. This lane takes no further action.
