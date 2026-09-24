# Standing Update Protocol — Benchmark Analyst re-hire spec (2026-09-23)

*How the next Benchmark Analyst instance updates the scoreboard. Binding on re-hire.*

## Trigger

Every new SCBI verdict (experiment completion, halt, kill, or demotion) AND every monthly frontier sweep, whichever comes first. The Research Lead re-hires this role with the verdict's primary artifacts attached.

## Inputs (read before writing)

1. The verdict's primary artifacts (results JSON, run log, signed protocol) — never summaries alone.
2. The current scoreboard files under `research/benchmarks/`.
3. The synthesis §D map and §H battery (for comparator obligations).
4. For frontier rows: the paper's own abstract at minimum; full text for any number that becomes load-bearing (Law #3).

## Update procedure

1. **Add the SCBI row first**, from primary artifacts: axis, effect with the paper's own uncertainty, exact N, model/layer, compute budget, pre-registered verdict category. If the verdict is a halt/kill/infeasible, the row says so — nulls are plotted, never omitted.
2. **Re-verify any frontier number the new row is compared against** (Law #3 — fresh fetch, current date). Rows not implicated keep their existing provenance; mark them "carried, not re-verified."
3. **Recompute the gap statement** in SCBI_VS_FRONTIER: if we still trail, say so in the same plain language. If a row now beats a frontier system, it must satisfy the six §D2 conditions — check each explicitly before writing the claim.
4. **Bump the version** (v1 → v2 …), date the files, append a changelog entry at the top of each file. Never edit a prior version in place: write new dated files.
5. **Extract-or-mark pass**: for any frontier row still showing "not extracted," either extract the number from the paper or mark it permanently absent with the reason.

## Report format

Standup format to the Research Lead: (a) what changed on the board, (b) the new gap reading in one paragraph, (c) any frontier paper whose status changed (preprint→published, retracted, superseded), (d) Law #3 verification log (what was fetched, when, what it confirmed).

## Anti-cherry-picking rules (binding)

- Every SCBI verdict gets a row, including halts, kills, and infeasible designs. Omitting an unfavorable row is a Law #2 violation (fabrication by omission).
- No axis-stretching: a result is plotted on the axis its protocol pre-registered. Post-hoc re-axising to look better is forbidden (Law #4).
- Frontier numbers are the papers' own headline claims with their own uncertainty — never our re-computation presented as theirs.
- The "what would beating require" bar (§D2 six conditions) does not move to accommodate a near-miss. Near-misses are reported as near-misses.
- $0 spend: literature arithmetic only. No GPU, no paid sources.
