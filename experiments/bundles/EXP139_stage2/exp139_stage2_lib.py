#!/usr/bin/env python3
"""EXP139 Stage-2 pure-Python library — NO torch dependency.

Pinned constants, bench reconstruction, Newcombe paired inference, trajectory
diagnostic, and the §6 verdict-tree reporter.

Protocol source (binding): research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md
(SIGNED, LOG-4885). Stage-1 implementation precedent:
experiments/runs/EXP139_stage1/run_stage1.py (LOG-4885→4886).

This module is importable on CPU with stdlib only so the bundle's structural
tests run without GPU contact and without model/weight downloads.
"""

import hashlib
import json
import math

# ============ pre-reg §2 pinned constants ============
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df"
HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
MODEL_ID = "EleutherAI/pythia-410m"
D_HID = 1024

# ============ pre-reg §5 Stage-2 protocol constants ============
N_ITEMS = 60          # all 60 bench items, view 0
T_STEPS = 8           # fixed re-entrant iterations
BASELINE_PASSES = 60  # see AMBIGUITY-1: pre-reg states 40 additional passes
R_PASSES = 480        # 60 items x 8 R-evaluations
EXPECTED_FORWARDS = 540  # 60 baseline + 480 R (pre-reg cost line says 520)

# ============ pre-reg §7 inference bars ============
BAR_DELTA_PP = 0.08   # ΔM_attractor ≥ +8pp
BAR_LCI = 0.05        # Newcombe paired 95% LCI > 0.05
WILSON_Z = 1.96       # 95%, no continuity correction

# ============ Stage-1 context [OBSERVATION, LOG-4886] ============
KAPPA_HAT_STAGE1 = 0.955971  # < 1: contraction license SURVIVES; Stage-2 gate open

# ============ bench reconstruction (verbatim port of run_stage1.py) ============
SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Joel", "Gideon", "Ruth", "Abel"],
    "V3_Greek": ["Ajax", "Jason", "Apollo", "Paris", "Atlas"],
    "V4_Roman": ["Marcus", "Julius", "Augustus", "Felix", "Diana"],
    "V5_Modern": ["Liam", "Noah", "Eli", "Maya", "Finn"],
}
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())
NOVEL_VOCAB_PLANET = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
NOVEL_VOCAB_ELEMENT = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
TRIPLES_INDICES = [
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
]
QUADS_INDICES = [
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
]


def build_bench():
    bench = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = "%s or %s" % (A, C) if target_first else "%s or %s" % (C, A)
        if i < 8:
            p = "Premise: %s outranks %s. %s outranks %s. Question: Who is higher in rank, %s? Answer:" % (A, B, B, C, q_opts)
        else:
            p = "Premise: %s is lower than %s. %s is lower than %s. Question: Who is higher in rank, %s? Answer:" % (C, B, B, A, q_opts)
        bench.append({"id": "exp077_planet_2hop_%d" % i, "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "planet", "hop": 2, "domain": "Planetary",
                      "idx": (iA, iB, iC), "tfirst": target_first, "variant": "outranks" if i < 8 else "lower"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                          NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        target_first = (i % 2 == 1)
        q_opts = "%s or %s" % (A, D_ent) if target_first else "%s or %s" % (D_ent, A)
        if i < 8:
            p = ("Premise: %s outranks %s. %s outranks %s. %s outranks %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (A, B, B, C, C, D_ent, q_opts)
        else:
            p = ("Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (D_ent, C, C, B, B, A, q_opts)
        bench.append({"id": "exp077_planet_3hop_%d" % i, "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "planet", "hop": 3, "domain": "Planetary",
                      "idx": (iA, iB, iC, iD), "tfirst": target_first, "variant": "outranks" if i < 8 else "lower"})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = "%s or %s" % (A, C) if target_first else "%s or %s" % (C, A)
        if i < 7:
            p = "Premise: %s outranks %s. %s outranks %s. Question: Who is higher in rank, %s? Answer:" % (A, B, B, C, q_opts)
        else:
            p = "Premise: %s is lower than %s. %s is lower than %s. Question: Who is higher in rank, %s? Answer:" % (C, B, B, A, q_opts)
        bench.append({"id": "exp077_element_2hop_%d" % i, "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "element", "hop": 2, "domain": "Elemental",
                      "idx": (iA, iB, iC), "tfirst": target_first, "variant": "outranks" if i < 7 else "lower"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                          NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        target_first = (i % 2 == 0)
        q_opts = "%s or %s" % (A, D_ent) if target_first else "%s or %s" % (D_ent, A)
        if i < 7:
            p = ("Premise: %s outranks %s. %s outranks %s. %s outranks %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (A, B, B, C, C, D_ent, q_opts)
        else:
            p = ("Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (D_ent, C, C, B, B, A, q_opts)
        bench.append({"id": "exp077_element_3hop_%d" % i, "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "element", "hop": 3, "domain": "Elemental",
                      "idx": (iA, iB, iC, iD), "tfirst": target_first, "variant": "outranks" if i < 7 else "lower"})
    return bench


def make_views(it, src_ents):
    views = []
    for vk in VOCAB_KEYS:
        sub = dict(zip(src_ents, [SUPPORT_VOCABULARIES[vk][k] for k in it["idx"]]))
        prompt = it["prompt"]
        for old, new in sub.items():
            assert old in prompt, "substitution source missing: %s" % old
            prompt = prompt.replace(old, new)
        views.append({"prompt": prompt, "vk": vk,
                      "A": sub[it["A"]], "C": sub[it["C"]]})
    return views


def novel_src(it):
    base = NOVEL_VOCAB_PLANET if it["typ"] == "planet" else NOVEL_VOCAB_ELEMENT
    return [base[k] for k in it["idx"]]


def bench_sha256(bench):
    return hashlib.sha256(json.dumps(
        [{k: bench[i][k] for k in ("id", "prompt", "A", "C")} for i in range(len(bench))],
        sort_keys=True).encode()).hexdigest()


# ============ pre-reg §7 Newcombe paired interval (verbatim construction) ============
def wilson_interval(phat, n, z=WILSON_Z):
    """Wilson 95% interval, no continuity correction, clipped to [0,1]."""
    den = 1.0 + z * z / n
    center = (phat + z * z / (2 * n)) / den
    half = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / den
    return (max(0.0, center - half), min(1.0, center + half))


def newcombe_paired(b, c, n):
    """b = #{baseline wrong, attractor right}; c = #{baseline right, attractor wrong}."""
    dhat = (b - c) / n
    pb, pc = b / n, c / n
    lb, ub = wilson_interval(pb, n)
    lc, uc = wilson_interval(pc, n)
    L = dhat - math.sqrt((pb - lb) ** 2 + (uc - pc) ** 2)
    U = dhat + math.sqrt((ub - pb) ** 2 + (pc - lc) ** 2)
    return {"dhat": dhat, "L": L, "U": U, "b": b, "c": c, "n": n,
            "wilson_b": [lb, ub], "wilson_c": [lc, uc]}


def mcnemar_exact_twosided(b, c):
    """Secondary only (reported, not binding). Exact two-sided McNemar p via the
    doubling method on Binomial(b+c, 0.5). Convention flagged for the reviewer
    (AMBIGUITY-3); the pre-reg does not name a two-sided convention."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p_le = sum(math.comb(n, i) for i in range(k + 1)) / 2.0 ** n
    return min(1.0, 2.0 * p_le)


# ============ pre-reg §5 trajectory diagnostic (binding backstop) ============
def trajectory_strictly_decreasing(diff_norms):
    """diff_norms = [||h^(t+1)-h^(t)||_2 for t=0..7]; must be strictly decreasing."""
    return all(a > b for a, b in zip(diff_norms, diff_norms[1:]))


# ============ pre-reg §6 verdict-tree reporter (κ̂<1 path) ============
def stage2_branch_report(dhat, L, U, traj_ok):
    """Reports which §6 branches trip (κ̂<1 path).

    AMBIGUITY-4 (binding adjudication, Law #14 apparatus review LOG-4896):
    for κ̂<1 and ΔM_attractor ≤ 0 the governing branch is HELD(f) — the §6
    falsification table governs; the §0 breaking-points line and the §5 bar
    assigning KILL are superseded as drafting defects. HELD(f): "converges to
    nothing useful — dynamics exist, no capability; licenses nothing, kills
    nothing". This is a pre-execution disambiguation of a drafting defect, not
    a post-hoc bar shift (Law #4)."""
    licensed = (dhat >= BAR_DELTA_PP) and (L > BAR_LCI)
    rep = {"dhat": dhat, "L": L, "U": U,
           "trajectory_strictly_decreasing": traj_ok,
           "delta_licensed": licensed,
           "branches": [], "conflicts": []}
    if traj_ok and licensed:
        rep["branches"].append(
            ("CONTINUE", "κ̂<1, trajectory strictly decreasing, "
             "ΔM_attractor ≥ +8pp with LCI > 0.05 — licenses a follow-on (new number) "
             "on the attractor mechanism, not an integration claim"))
    if (not traj_ok) and licensed:
        rep["branches"].append(
            ("PIVOT", "κ̂<1, trajectory non-decreasing, ΔM licensed — Banach reading void; "
             "re-scope to fixed-T refinement (no Banach claim)"))
    if traj_ok and (not licensed) and dhat > 0:
        rep["branches"].append(
            ("HELD(c)", "κ̂<1, trajectory passes, 0 < ΔM < +8pp or LCI straddles the "
             "licensing threshold — movement without a licensed capability claim"))
    if (not traj_ok) and (not licensed) and dhat > 0:
        rep["branches"].append(
            ("HELD(d)", "κ̂<1, trajectory non-decreasing, ΔM not licensed — "
             "Banach reading void; nothing else established"))
    if dhat <= 0:
        # Binding adjudication (LOG-4896): HELD(f) governs. No conflict is
        # reported and no KILL reading is emitted in this case.
        rep["branches"].append(
            ("HELD(f)", "κ̂<1, ΔM_attractor ≤ 0 — converges to nothing useful: "
             "dynamics exist, no capability; licenses nothing, kills nothing "
             "(binding adjudication LOG-4896; §0/§5 KILL lines superseded as "
             "drafting defects)"))
    return rep
