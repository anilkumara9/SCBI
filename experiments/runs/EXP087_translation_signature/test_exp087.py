#!/usr/bin/env python3
"""EXP087 evaluator tests — every number from an actual run, nothing invented.

Covers: benchmark construction + G2 byte-identity, guards (refusal gates,
Δθ=0), pinned join (all failure modes + archived r reproduction), statistics
(estimators, envelope, t p-value, 4σ flag), verdict precedence (R5 dominates;
R1–R4 → CONTINUE; all-hold → KILL), support-set aggregation, and the
archived-data reproduction (r = 0.49708 under O pairing; r = −0.21388 under
sorted pairing).
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import exp087_benchmark as B
import exp087_guards as G
import exp087_join as J
import exp087_statistics as S
import exp087_support as SUP
import exp087_verdicts as V

HERE = os.path.dirname(os.path.abspath(__file__))
SCBI = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ARCHIVE = os.path.join(SCBI, "experiments", "runs",
                       "EXP066_pythia410m_replication",
                       "exp066_instance_evaluations.json")
K1_JSON = os.path.join(SCBI, "research", "analysis_plans",
                       "K1_RESULTS_LOG213_2026-09-23.json")

PASS = []
FAIL = []


def check(name, cond, detail=""):
    if cond:
        PASS.append(name)
    else:
        FAIL.append((name, detail))
        print(f"FAIL: {name} {detail}")


def load_archive():
    with open(ARCHIVE, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- benchmark
def test_benchmark():
    items = B.build_items()
    check("bench_n60", len(items) == 60, f"got {len(items)}")
    O = B.order_O()
    check("O_n60_unique", len(O) == 60 and len(set(O)) == 60)
    check("O_blocks", O[0] == "pythia410m_planet_2hop_0"
          and O[15] == "pythia410m_planet_3hop_0"
          and O[30] == "pythia410m_element_2hop_0"
          and O[45] == "pythia410m_element_3hop_0"
          and O[59] == "pythia410m_element_3hop_14")
    check("leading_space", all(it["target_token"].startswith(" ")
                                and it["foil_token"].startswith(" ") for it in items))
    check("g2_byte_identity", B.g2_byte_identity_check(ARCHIVE) is True)
    h1 = B.prompt_sha256(items[0]["prompt"])
    h2 = B.prompt_sha256(items[0]["prompt"] + " ")
    check("sha256_sensitive", h1 != h2 and len(h1) == 64)


# ---------------------------------------------------------------- guards
def test_guards():
    check("pins", G.MODEL_ID == "EleutherAI/pythia-410m" and G.LAYER_INDEX == 20
          and G.N_ITEMS == 60 and abs(G.ALPHA - 0.5) < 1e-12
          and abs(G.ENVELOPE_LO - 0.649) < 1e-12
          and abs(G.ENVELOPE_HI - 0.849) < 1e-12
          and abs(G.HEADROOM_LO - 0.40) < 1e-12
          and abs(G.HEADROOM_HI - 0.70) < 1e-12)
    check("crash_guard_ok", G.crash_guard(SCBI) is True)
    try:
        G.crash_guard("/nonexistent")
        check("crash_guard_missing", False, "should have raised")
    except G.BundleError:
        check("crash_guard_missing", True)

    class FakeArgs:
        bundle_review_signoff = False
        ceo_gpu_clearance = False
    try:
        G.require_execution_license(FakeArgs(), log_fn=lambda m: None)
        check("refuse_no_flags", False, "should have refused")
    except G.RefusalError:
        check("refuse_no_flags", True)
    FakeArgs.bundle_review_signoff = True
    try:
        G.require_execution_license(FakeArgs(), log_fn=lambda m: None)
        check("refuse_one_flag", False, "should have refused")
    except G.RefusalError:
        check("refuse_one_flag", True)
    FakeArgs.ceo_gpu_clearance = True
    check("license_both_flags",
          G.require_execution_license(FakeArgs(), log_fn=lambda m: None) is True)

    # Δθ=0 guard on a fake state dict
    gb = G.FrozenBackboneGuard()
    sd = {"b": [[1.0, 2.0], [3.0, 4.0]], "a": [0.5]}
    gb.capture_pre(sd)
    gb.capture_post(sd)
    check("dtheta0_pass", gb.verify() is True)
    sd2 = {"b": [[1.0, 2.0], [3.0, 4.001]], "a": [0.5]}
    gb.capture_post(sd2)
    try:
        gb.verify()
        check("dtheta0_catch", False, "should have raised")
    except G.BundleError:
        check("dtheta0_catch", True)
    fp = G.determinism_fingerprint()
    check("fingerprint", fp["master_seed"] == G.MASTER_SEED
          and fp["second_seed_used"] is False)


# ---------------------------------------------------------------- join
def test_join():
    archive = load_archive()
    c = J.load_c_vector(K1_JSON)
    check("c_len60", len(c) == 60)
    O = B.order_O()
    fresh = [{"instance_key": k, "prompt": archive[k]["prompt"]} for k in O]
    joined = J.pinned_join(c, fresh, archive)
    check("join_ok", len(joined) == 60 and all(
        abs(r["c_i"] - c[j]) < 1e-18 for j, r in enumerate(joined)))
    # failure modes
    try:
        J.pinned_join(c[:59], fresh, archive)
        check("join_bad_len", False, "should raise")
    except G.JoinError:
        check("join_bad_len", True)
    dup = fresh + [fresh[0]]
    try:
        J.pinned_join(c, dup, archive)
        check("join_dup", False, "should raise")
    except G.JoinError:
        check("join_dup", True)
    wrong = [{"instance_key": k, "prompt": archive[k]["prompt"]} for k in O]
    wrong[5] = dict(wrong[5]); wrong[5]["prompt"] += "x"
    try:
        J.pinned_join(c, wrong, archive)
        check("join_hash", False, "should raise")
    except G.JoinError:
        check("join_hash", True)
    missing = [r for r in fresh if r["instance_key"] != O[3]]
    try:
        J.pinned_join(c, missing, archive)
        check("join_missing", False, "should raise")
    except G.JoinError:
        check("join_missing", True)


# ---------------------------------------------------------------- statistics
def test_statistics():
    check("mean", abs(S.mean([1.0, 2.0, 3.0]) - 2.0) < 1e-12)
    check("std", abs(S.sample_std([1.0, 2.0, 3.0]) - 1.0) < 1e-12)
    check("envelope_in", S.envelope_check(0.74921) is True)
    check("envelope_lo_edge", S.envelope_check(0.649) is True)
    check("envelope_hi_edge", S.envelope_check(0.849) is True)
    check("envelope_out_lo", S.envelope_check(0.648) is False)
    check("envelope_out_hi", S.envelope_check(0.850) is False)
    check("positivity", S.strict_positivity([0.01, 0.5]) is True
          and S.strict_positivity([0.01, 0.0]) is False)
    # rescue-set identity on a tiny hand case
    recs = [{"m0": -0.5, "dm_c2": 0.7}, {"m0": 0.3, "dm_c2": 0.7},
            {"m0": -0.9, "dm_c2": 0.7}]
    check("predicted_set", S.predicted_rescue_set(recs) == {0})
    check("hamming", S.hamming_distance({0, 1}, {0, 2}) == 2)
    ok, viol = S.subset_check({1}, {1, 2})
    check("subset_ok", ok and viol == [])
    ok, viol = S.subset_check({1, 5}, {1, 2})
    check("subset_viol", (not ok) and viol == [5])
    b, c = S.mcnemar_cells([True, True, False, False], [True, False, True, False])
    check("mcnemar", (b, c) == (1, 1), f"got {(b, c)}")
    # t p-value: strong positive correlation -> tiny p
    r = S.pearson_r([1, 2, 3, 4, 5], [1.1, 1.9, 3.2, 3.8, 5.1])
    p = S.corr_one_sided_pvalue(r, 5)
    check("t_pvalue_small", 0 < p < 0.01, f"r={r:.4f} p={p:.2e}")
    # null correlation -> large p
    r0 = S.pearson_r([1, 2, 3, 4, 5, 6], [3, 1, 4, 1, 5, 9][:6])
    p0 = S.corr_one_sided_pvalue(r0, 6)
    check("t_pvalue_null", p0 > 0.05, f"r={r0:.4f} p={p0:.3f}")
    # 4σ flag: one extreme outlier among tight data
    dm = [0.749] * 59 + [0.749 + 5 * 0.001]
    flagged, mu, sig = S.layernorm_saturation_flag(dm)
    check("sigma_flag", flagged == [59], f"got {flagged}")
    dm2 = [0.749 + 0.001 * ((i % 3) - 1) for i in range(60)]
    flagged2, _, _ = S.layernorm_saturation_flag(dm2)
    check("sigma_noflag", flagged2 == [], f"got {flagged2}")


def test_archived_reproduction():
    """The strongest grounded test: real archive + real K1 c."""
    archive = load_archive()
    c = J.load_c_vector(K1_JSON)
    O = B.order_O()
    dm = [archive[k]["Same_Layer_Output_Bridge_margin_shift"] for k in O]
    mu = S.mu_hat(dm)
    check("arch_mu", abs(mu - G.MU_CENTER) < 1e-4, f"mu={mu}")
    check("arch_mu_in_envelope", S.envelope_check(mu) is True)
    check("arch_min", abs(min(dm) - G.MIN_DM_ARCH) < 1e-4, f"min={min(dm)}")
    r, p, ok = S.corr_replication_test(dm, c)
    check("arch_r", abs(r - G.R_ARCH) < 1e-4, f"r={r:.5f}")
    check("arch_r_passes", ok and p < 0.05, f"p={p:.2e}")
    dm_sorted = [archive[k]["Same_Layer_Output_Bridge_margin_shift"]
                 for k in sorted(archive.keys())]
    r_sorted = S.pearson_r(dm_sorted, c)
    check("arch_r_sorted", abs(r_sorted - G.R_SORTED_NEG) < 1e-4,
          f"r_sorted={r_sorted:.5f}")


# ---------------------------------------------------------------- verdicts
def _base_records():
    """60 records where everything holds (KILL shape). dm_c2 has realistic
    spread (never zero-variance) while keeping every row in the KILL shape."""
    recs = []
    for i in range(60):
        m0 = 0.25 if i % 2 == 0 else -0.35   # 30 correct / 30 wrong
        dm2 = 0.749 + 0.02 * math.sin(i)     # variance for R4; all > 0
        dm3 = 0.009
        recs.append({"instance_key": f"k{i}", "m0": m0, "dm_c2": dm2,
                      "dm_c3": dm3,
                      "base_correct": m0 > 0,
                      "c2_correct": (m0 + dm2) > 0,
                      "c3_correct": (m0 + dm3) > 0})
    return recs


def _c_corr(dm):
    # c correlated with dm at r ≈ 0.9 -> R4 passes
    return [0.9 * (d - 0.749) / 0.05 + 0.1 * ((i % 5) - 2) / 2
            for i, d in enumerate(dm)]


def test_verdicts():
    recs = _base_records()
    dm = [r["dm_c2"] for r in recs]
    rep = V.adjudicate(recs, _c_corr(dm))
    check("verdict_kill", rep["verdict"] == "KILL",
          f"got {rep['verdict']} row={rep.get('verdict_row')}")

    # R5 dominates: envelope breach -> RUN-INVALID even with a corruption too
    recs2 = _base_records()
    for r in recs2:
        r["dm_c2"] = 0.50
    recs2[0]["dm_c2"] = -0.1  # also an R1 break
    recs2[0]["c2_correct"] = False
    rep = V.adjudicate(recs2, _c_corr([r["dm_c2"] for r in recs2]))
    check("r5_dominates", rep["verdict"] == "RUN-INVALID"
          and rep["verdict_row"] == "R5_envelope",
          f"got {rep['verdict']}/{rep.get('verdict_row')}")

    # R1: dm <= 0 -> CONTINUE
    recs3 = _base_records()
    recs3[7]["dm_c2"] = -0.02
    recs3[7]["c2_correct"] = False
    rep = V.adjudicate(recs3, _c_corr([r["dm_c2"] for r in recs3]))
    check("r1_dm", rep["verdict"] == "CONTINUE"
          and rep["verdict_row"] == "R1_positivity",
          f"got {rep['verdict']}/{rep.get('verdict_row')}")

    # R1: corruption -> CONTINUE
    recs4 = _base_records()
    i = next(i for i, r in enumerate(recs4) if r["base_correct"])
    recs4[i]["c2_correct"] = False
    rep = V.adjudicate(recs4, _c_corr([r["dm_c2"] for r in recs4]))
    check("r1_corr", rep["verdict"] == "CONTINUE"
          and rep["verdict_row"] == "R1_corruption",
          f"got {rep['verdict']}/{rep.get('verdict_row')}")

    # R2: Hamming != 0 -> CONTINUE (predicted rescue not observed)
    recs5 = _base_records()
    i = next(i for i, r in enumerate(recs5) if not r["base_correct"])
    recs5[i]["c2_correct"] = False  # P contains i, observed does not
    rep = V.adjudicate(recs5, _c_corr([r["dm_c2"] for r in recs5]))
    check("r2_ham", rep["verdict"] == "CONTINUE"
          and rep["verdict_row"] == "R2_identity",
          f"got {rep['verdict']}/{rep.get('verdict_row')}")

    # R3: C3 rescue of C2-resistant -> CONTINUE
    recs6 = _base_records()
    i = 1  # force C2-resistant: base-wrong, m0 + dm_c2 < 0
    recs6[i]["m0"] = -1.2
    recs6[i]["dm_c2"] = 0.749
    recs6[i]["base_correct"] = False
    recs6[i]["c2_correct"] = False
    recs6[i]["dm_c3"] = 1.2
    recs6[i]["c3_correct"] = True   # ...but C3 rescues
    rep = V.adjudicate(recs6, _c_corr([r["dm_c2"] for r in recs6]))
    check("r3_subset", rep["verdict"] == "CONTINUE"
          and rep["verdict_row"] == "R3_subset",
          f"got {rep['verdict']}/{rep.get('verdict_row')}")

    # R4: non-significant corr -> CONTINUE
    recs7 = _base_records()
    c_null = [float((i * 37) % 11 - 5) for i in range(60)]  # deterministic noise
    rep = V.adjudicate(recs7, c_null)
    check("r4_corr", rep["verdict"] == "CONTINUE"
          and rep["verdict_row"] == "R4_corr",
          f"got {rep['verdict']}/{rep.get('verdict_row')}")

    # headroom violation -> RUN-INVALID
    recs8 = _base_records()
    for r in recs8[:45]:
        r["base_correct"] = True  # 75% base accuracy
    rep = V.adjudicate(recs8, _c_corr([r["dm_c2"] for r in recs8]))
    check("headroom", rep["verdict"] == "RUN-INVALID"
          and rep["verdict_row"] == "headroom_gate",
          f"got {rep['verdict']}/{rep.get('verdict_row')}")

    # gross corruptions -> RUN-INVALID (build-lane resolution)
    recs9 = _base_records()
    n = 0
    for r in recs9:
        if r["base_correct"] and n < G.GROSS_CORRUPTION_BAR:
            r["c2_correct"] = False
            n += 1
    rep = V.adjudicate(recs9, _c_corr([r["dm_c2"] for r in recs9]))
    check("gross", rep["verdict"] == "RUN-INVALID"
          and rep["verdict_row"] == "guard_iii_gross",
          f"got {rep['verdict']}/{rep.get('verdict_row')}")

    # wrong n -> BundleError
    try:
        V.adjudicate(recs[:59], _c_corr(dm[:59]))
        check("verdict_n", False, "should raise")
    except G.BundleError:
        check("verdict_n", True)


# ---------------------------------------------------------------- support
def test_support():
    pairs = SUP.build_support_prompts()
    check("support_150", len(pairs) == 150, f"got {len(pairs)}")
    check("support_vocabs", len({p[0] for p in pairs}) == 5)
    # pure-math aggregation on synthetic deltas
    import random
    rng = random.Random(42)
    d = 16
    dh = {k: [[rng.gauss(0, 1) for _ in range(d)] for _ in range(30)]
          for k in SUP.SUPPORT_VOCABULARIES}
    b = SUP.aggregate_b_agg(dh)
    n = math.sqrt(sum(x * x for x in b))
    check("bagg_unit", abs(n - 1.0) < 1e-9, f"norm={n}")
    check("bagg_dim", len(b) == d)
    # bridge vec verbatim form
    E = [[float(i + j) for j in range(8)] for i in range(10)]
    w = SUP.make_bridge_vec_embed(E, 3, 7)
    nw = math.sqrt(sum(x * x for x in w))
    check("bridge_unit", abs(nw - 1.0) < 1e-9, f"norm={nw}")


def main():
    test_benchmark()
    test_guards()
    test_join()
    test_statistics()
    test_archived_reproduction()
    test_verdicts()
    test_support()
    print(f"\nEVALUATOR: {len(PASS)}/{len(PASS) + len(FAIL)} pass")
    if FAIL:
        print(f"{len(FAIL)} FAILURES:")
        for n, d in FAIL:
            print(f"  - {n}: {d}")
        sys.exit(1)
    print("ALL GREEN")


if __name__ == "__main__":
    main()
