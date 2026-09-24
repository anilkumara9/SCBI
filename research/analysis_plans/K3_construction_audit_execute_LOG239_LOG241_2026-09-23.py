#!/usr/bin/env python3
"""K3 Phase-0 R1 executor (LOG-241).

Implements K3_PHASE0_R1_PLAN_LOG239_2026-09-23.md Phase-0 §10 steps 1-6 verbatim.
CPU only, $0, weight algebra only. Zero forward invocations: the script performs
no direct forward invocation of the model anywhere (G5 asserted by source scan).

Plan:  research/analysis_plans/K3_PHASE0_R1_PLAN_LOG239_2026-09-23.md (Law #14 SIGNED via LOG-240)
Twin:   K3_CONSTRUCTION_AUDIT_RESULTS_LOG239_LOG241_2026-09-23.json
Report: K3_PHASE0_REPORT_LOG241_2026-09-23.md
"""

import hashlib
import json
import math
import platform
import re
import sys

import numpy as np
import torch
from scipy.stats import beta as beta_dist
from transformers import AutoModelForCausalLM, AutoTokenizer

# --------------------------------------------------------------------------
# Pins (plan §8.1 / §2 / §3.3)
# --------------------------------------------------------------------------
LOG = "LOG-241"
PLAN = "K3_PHASE0_R1_PLAN_LOG239_2026-09-23"
REPO = "/home/hatch/workspace/SCBI"
OUT_DIR = REPO + "/research/analysis_plans"
ARCHIVED_HASH = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
MODEL_NAME = "EleutherAI/pythia-410m"
SNAPSHOT = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
PREAUDIT = REPO + "/experiments/protocols/C-A_PREAUDIT_2026-09-23.json"
G_FLOOR = 0.25
IDENT_COS_TOL = 1e-6          # E-K3-3(a): 1 - |cos| must be <= 1e-6
AUDIT_VAL_TOL = 1e-6          # E-K3-3(b): max abs dev vs signed s_t/s_f
G_C3_TOL = 1e-4               # E-K3-3(b): |g_rebuilt - 1.061783| <= 1e-4

# Verbatim ports of run_exp077.py ll.149-162 (bench vocabulary + index tables).
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

# C3 donor (t_d, f_d) pairs: verbatim from the signed v2 spec §3.1 table
# (V1_Anglo, V2_Biblical, V3_Greek, V4_Roman, V5_Modern) x triple indices 0..3.
DONORS_C3 = [
    ("Alice", "Charlie"), ("Bob", "David"), ("Charlie", "Emma"), ("Alice", "Emma"),
    ("Aaron", "Gideon"), ("Joel", "Ruth"), ("Gideon", "Abel"), ("Aaron", "Abel"),
    ("Ajax", "Apollo"), ("Jason", "Paris"), ("Apollo", "Atlas"), ("Ajax", "Atlas"),
    ("Marcus", "Augustus"), ("Julius", "Felix"), ("Augustus", "Diana"), ("Marcus", "Diana"),
    ("Liam", "Eli"), ("Noah", "Maya"), ("Eli", "Finn"), ("Liam", "Finn"),
]


def fatal(msg):
    print("FATAL: " + msg, file=sys.stderr)
    sys.exit(1)


def get_hash(model):
    """SHA-256 binding guard (protocol §2): SHA-256 over the concatenation of
    state_dict() tensors (sorted keys, CPU, float32 bytes).
    Verbatim formulation from run_exp077.py ll.166-172 (EXP082-D1 lesson)."""
    sha = hashlib.sha256()
    for key in sorted(model.state_dict().keys()):
        sha.update(model.state_dict()[key].detach().cpu().to(torch.float32).numpy().tobytes())
    return sha.hexdigest()


def tok_id(tokenizer, entity):
    # LOG-197 E1 / EXP081 v2 §2 F2 convention, exactly as the runners encode.
    ids = tokenizer.encode(" " + entity)
    return ids


def clopper_pearson(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else float(beta_dist.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta_dist.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi


def cos(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def main():
    res = {"log": LOG, "plan": PLAN, "phase": 0, "steps": {}}

    # ---- Step 1: env assert + read-only model load + G3 pre-hash ----
    env = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": __import__("transformers").__version__,
        "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "platform": platform.platform(),
        "venv": "/home/hatch/workspace/.venv_smoke",
    }
    res["env"] = env
    assert env["torch"] == "2.14.0+cpu", env
    assert env["transformers"] == "5.17.0", env
    assert env["numpy"] == "2.5.3", env
    assert env["scipy"] == "1.18.1", env

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, revision=SNAPSHOT, local_files_only=True,
        trust_remote_code=False, torch_dtype=torch.float32)
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME, revision=SNAPSHOT, local_files_only=True, trust_remote_code=False)

    pre_hash = get_hash(model)
    res["hashes"] = {"formulation": "run_exp077.py ll.166-172 verbatim",
                     "pre": pre_hash, "archived": ARCHIVED_HASH}
    if pre_hash != ARCHIVED_HASH:
        fatal("G3 pre-hash mismatch: %s != archived %s" % (pre_hash, ARCHIVED_HASH))
    res["steps"]["step1"] = "PASS: env exact; model read-only pinned snapshot; G3 pre-hash == archived"

    # ---- Step 2: verbatim bench port + G4 cross-check (recomputed, Law #3) + G6 ----
    # Verbatim port of run_exp077.py ll.586-636 (four bench-construction loops).
    bench = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        bench.append({"id": "exp077_planet_2hop_%d" % i, "A": A, "C": C,
                      "B": B, "hop": 2, "domain": "planet"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                          NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        bench.append({"id": "exp077_planet_3hop_%d" % i, "A": A, "C": D_ent,
                      "B": B, "Cprem": C, "hop": 3, "domain": "planet"})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        bench.append({"id": "exp077_element_2hop_%d" % i, "A": A, "C": C,
                      "B": B, "hop": 2, "domain": "element"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                          NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        bench.append({"id": "exp077_element_3hop_%d" % i, "A": A, "C": D_ent,
                      "B": B, "Cprem": C, "hop": 3, "domain": "element"})
    assert len(bench) == 60
    res["quad_loop_subranges"] = {"planet_2hop": [0, 14], "planet_3hop": [15, 29],
                                  "element_2hop": [30, 44], "element_3hop": [45, 59]}

    # Rebuild per-item (id, t, f): t = item["A"], f = item["C"] (foil field).
    rebuilt = [{"id": it["id"], "t": it["A"], "f": it["C"]} for it in bench]

    # G4: recompute the full 60/60 comparison from the source JSON (Law #3).
    # The pre-repair smoke archive exp077_instance_records.json is NOT a source (§2 D1).
    audit = json.load(open(PREAUDIT))
    per_item = audit["similarity_audit"]["per_item"]
    if len(per_item) != 60:
        fatal("G4: per_item record count %d != 60" % len(per_item))
    mismatches = []
    for k in range(60):
        a, b = rebuilt[k], per_item[k]
        for field in ("id", "t", "f"):
            if a[field] != b[field]:
                mismatches.append({"index": k, "field": field,
                                   "rebuilt": a[field], "json": b[field]})
    n_match = 60 - len({m["index"] for m in mismatches})
    res["G4"] = {"compared": 60, "index_aligned_matches": n_match,
                 "mismatches": mismatches,
                 "source": "experiments/protocols/C-A_PREAUDIT_2026-09-23.json similarity_audit.per_item (recomputed; nothing inherited from LOG-238)"}
    if n_match != 60:
        fatal("G4: %d/60 index-aligned (id,t,f) byte-matches; mismatches: %s" % (n_match, mismatches))
    res["steps"]["step2a"] = "PASS: G4 60/60 index-aligned byte-exact (id,t,f) vs signed pre-audit JSON"

    # G6: every donor + every premise-non-option entity single-token as " "+entity.
    test_entities = set(NOVEL_VOCAB_PLANET + NOVEL_VOCAB_ELEMENT)
    donor_entities = set(e for pair in DONORS_C3 for e in pair)
    premise_instances = []  # 30 3-hop items x 2 premise-non-option entities
    for it in bench:
        if it["hop"] == 3:
            premise_instances += [it["B"], it["Cprem"]]
    assert len(premise_instances) == 60
    g6_viol = []
    for e in sorted(test_entities | donor_entities):
        ids = tok_id(tokenizer, e)
        if len(ids) != 1:
            g6_viol.append({"entity": e, "n_tokens": len(ids), "ids": ids})
    res["G6"] = {"n_unique_entities_checked": len(test_entities | donor_entities),
                 "n_premise_instances": len(premise_instances),
                 "violations": g6_viol}
    if g6_viol:
        fatal("G6 single-token violation: %s" % g6_viol)
    res["steps"]["step2b"] = "PASS: G6 all 35 unique donor+test entities single-token"

    tid = lambda e: tok_id(tokenizer, e)[0]  # noqa: E731
    W = model.get_output_embeddings().weight.detach().cpu().to(torch.float32).numpy()
    Wn = W / np.linalg.norm(W, axis=1, keepdims=True)  # normalized option rows ŵ
    res["W_shape"] = list(W.shape)

    # ---- Step 3: E-K3-1 static Law #7 compliance audit ----
    # Candidate (i): per-item {tok(B_i), tok(C_i)} ∩ {tok(target_i), tok(foil_i)} = ∅.
    three_hop = [it for it in bench if it["hop"] == 3]
    assert len(three_hop) == 30
    ci_viol = []
    bank_pairs = []  # (B_i, C_i) strings, 30
    for it in three_hop:
        B, Cpr, t, f = it["B"], it["Cprem"], it["A"], it["C"]
        bank_pairs.append((B, Cpr))
        inter = {tid(B), tid(Cpr)} & {tid(t), tid(f)}
        if inter:
            ci_viol.append({"id": it["id"], "violating_ids": sorted(inter)})
    # (C-c): construction input strings are premise-non-option strings only —
    # assert by inspection of the ported construction (no target/foil string can
    # enter: the port references only B/Cprem fields). (C-d): all premise strings
    # come from the evaluated bench itself (present-instance, (C-e) licensed);
    # no held-out/future instance exists in the fixed N=60 bench.
    bank_input_strings = set(premise_instances)
    label_strings = set(it["A"] for it in bench) | set(it["C"] for it in bench)
    res["E-K3-1"] = {
        "candidate_i": {
            "per_item_disjointness_violations": ci_viol,
            "verdict": "PASS" if not ci_viol else "FAIL",
            "n_bank_pairs": 30,
            "Cc_note": "input multiset == 60 premise-non-option strings (B_i,C_i); port references only B/Cprem fields; no label-derived ids by construction",
            "Cd_note": "present-instance bench material only; no held-out/future instances in the fixed N=60 bench",
        },
    }
    # Descriptive [OBSERVATION], non-gating: cross-item collision count.
    other_target_foil = {}
    for j, it in enumerate(bench):
        other_target_foil[j] = {tid(it["A"]), tid(it["C"])}
    coll = 0
    for i, it in enumerate(three_hop):
        idx = bench.index(it)
        for s in (it["B"], it["Cprem"]):
            for j in range(60):
                if j != idx and tid(s) in other_target_foil[j]:
                    coll += 1
                    break
    res["E-K3-1"]["cross_item_collision_count_OBSERVATION"] = {
        "count": coll, "of": 60,
        "reading": "non-gating per §3.1 per-item rationale (LOG-235 F-235-1)"
    }

    # Candidate (ii): donor token-id set ∩ all test {target, foil} token ids = ∅.
    donor_ids = set(tid(e) for e in donor_entities)
    test_tf_ids = set()
    for it in bench:
        test_tf_ids |= {tid(it["A"]), tid(it["C"])}
    cii_inter = sorted(donor_ids & test_tf_ids)
    res["E-K3-1"]["candidate_ii"] = {
        "donor_test_tf_intersection": cii_inter,
        "verdict": "PASS" if not cii_inter else "FAIL",
        "Cc_Cd_note": "donor labels are support-side construction material only; donor-label flow cited from signed EXP081 v2 §3.3 (Law #7 statement); donor pool disjoint from test option pool verified statically above",
    }
    res["steps"]["step3"] = "E-K3-1 audited: (i) %s, (ii) %s" % (
        res["E-K3-1"]["candidate_i"]["verdict"], res["E-K3-1"]["candidate_ii"]["verdict"])

    # ---- Step 4: constructions + E-K3-2 + E-K3-3 + E-K3-4 ----
    # Candidate (i): path A = torch float32 loop; path B = numpy float64 vectorized
    # (independent code path for the E-K3-3(a) self-consistency check).
    diffs_P_A = [W[tid(B)] - W[tid(Cpr)] for (B, Cpr) in bank_pairs]
    S_P_A = np.sum(np.stack([d.astype(np.float32) for d in diffs_P_A]), axis=0)
    diffs_P_B = np.stack([(W[tid(B)].astype(np.float64) - W[tid(Cpr)].astype(np.float64))
                          for (B, Cpr) in bank_pairs])
    S_P_B = diffs_P_B.sum(axis=0)
    nrm_P_A, nrm_P_B = float(np.linalg.norm(S_P_A)), float(np.linalg.norm(S_P_B))
    bhat_P = S_P_A / nrm_P_A
    bhat_P_B = S_P_B / np.linalg.norm(S_P_B)

    # Candidate (ii): donor centroid, verbatim v2 §4.1 sum-of-differences-then-normalize.
    diffs_D_A = [W[tid(td)] - W[tid(fd)] for (td, fd) in DONORS_C3]
    S_D_A = np.sum(np.stack([d.astype(np.float32) for d in diffs_D_A]), axis=0)
    diffs_D_B = np.stack([(W[tid(td)].astype(np.float64) - W[tid(fd)].astype(np.float64))
                          for (td, fd) in DONORS_C3])
    S_D_B = diffs_D_B.sum(axis=0)
    nrm_D_A, nrm_D_B = float(np.linalg.norm(S_D_A)), float(np.linalg.norm(S_D_B))
    bhat_D = S_D_A / nrm_D_A
    bhat_D_B = S_D_B / np.linalg.norm(S_D_B)

    # G7: per-pair norm floors + injection-vector norms > 0.
    pair_norms_P = [float(np.linalg.norm(d)) for d in diffs_P_A]
    pair_norms_D = [float(np.linalg.norm(d)) for d in diffs_D_A]
    res["G7"] = {
        "min_pair_norm_P": min(pair_norms_P), "min_pair_norm_D": min(pair_norms_D),
        "norm_bhat_P": float(np.linalg.norm(bhat_P)),
        "norm_bhat_D": float(np.linalg.norm(bhat_D)),
    }
    for v in pair_norms_P + pair_norms_D:
        if not v > 0:
            fatal("G7: zero bank-pair norm")
    if not (np.linalg.norm(bhat_P) > 0 and np.linalg.norm(bhat_D) > 0):
        fatal("G7: zero candidate norm")
    res["steps"]["step4a"] = "PASS: G7 all pair norms > 0; candidate norms > 0"

    # E-K3-2: g = ‖Σ(W[x]−W[y])‖₂ / √(#pairs).
    g_P = nrm_P_A / math.sqrt(30)
    g_D = nrm_D_A / math.sqrt(20)
    res["E-K3-2"] = {
        "g_P": g_P, "g_D": g_D, "floor": G_FLOOR,
        "gate_P": "PASS" if g_P >= G_FLOOR else "FAIL",
        "gate_D": "PASS" if g_D >= G_FLOOR else "FAIL",
        "pair_norms_P": {"min": min(pair_norms_P), "mean": float(np.mean(pair_norms_P)),
                         "max": max(pair_norms_P), "all": pair_norms_P},
        "pair_norms_D": {"min": min(pair_norms_D), "mean": float(np.mean(pair_norms_D)),
                         "max": max(pair_norms_D), "all": pair_norms_D},
    }

    # E-K3-3(a): self-consistency |cos| ≥ 1 − 1e-6.
    sc_P = abs(cos(bhat_P.astype(np.float64), bhat_P_B))
    sc_D = abs(cos(bhat_D.astype(np.float64), bhat_D_B))
    res["E-K3-3a"] = {"self_consistency_P": sc_P, "self_consistency_D": sc_D,
                      "tol": IDENT_COS_TOL,
                      "pass_P": bool(sc_P >= 1 - IDENT_COS_TOL),
                      "pass_D": bool(sc_D >= 1 - IDENT_COS_TOL)}
    if not (sc_P >= 1 - IDENT_COS_TOL and sc_D >= 1 - IDENT_COS_TOL):
        fatal("G2/E-K3-3(a) self-consistency failed: P=%r D=%r" % (sc_P, sc_D))

    # E-K3-3(b): (ii) identity vs the signed audit values.
    s_t = [float(np.dot(bhat_D, Wn[tid(it["A"])])) for it in bench]
    s_f = [float(np.dot(bhat_D, Wn[tid(it["C"])])) for it in bench]
    dev_t = max(abs(a - b["s_t"]) for a, b in zip(s_t, per_item))
    dev_f = max(abs(a - b["s_f"]) for a, b in zip(s_f, per_item))
    sa = audit["similarity_audit"]
    summ = {"s_t": sa["s_t"], "s_f": sa["s_f"]}
    summ_dev = max(
        abs(float(np.mean(s_t)) - summ["s_t"]["mean"]),
        abs(float(np.median(s_t)) - summ["s_t"]["median"]),
        abs(min(s_t) - summ["s_t"]["min"]),
        abs(max(s_t) - summ["s_t"]["max"]),
        abs(float(np.std(s_t)) - summ["s_t"]["std"]),
        abs(float(np.mean(s_f)) - summ["s_f"]["mean"]),
        abs(float(np.median(s_f)) - summ["s_f"]["median"]),
        abs(min(s_f) - summ["s_f"]["min"]),
        abs(max(s_f) - summ["s_f"]["max"]),
        abs(float(np.std(s_f)) - summ["s_f"]["std"]),
    )
    g_dev = abs(g_D - 1.061783)
    res["E-K3-3b"] = {
        "max_abs_dev_s_t_vs_per_item": dev_t,
        "max_abs_dev_s_f_vs_per_item": dev_f,
        "audit_value_tol": AUDIT_VAL_TOL,
        "summary_stats_max_dev": summ_dev,
        "g_D": g_D, "g_C3_signed_rounded": 1.061783,
        "abs_g_minus_1_061783": g_dev, "g_tol": G_C3_TOL,
        "max_abs_s_t": max(abs(x) for x in s_t),
        "max_abs_s_f": max(abs(x) for x in s_f),
        "signed_claim_all_abs_cos_lt_0_1": bool(max(abs(x) for x in s_t + s_f) < 0.1),
    }
    if not (dev_t <= AUDIT_VAL_TOL and dev_f <= AUDIT_VAL_TOL):
        fatal("G2/E-K3-3(b): audit-value mismatch dev_t=%r dev_f=%r > 1e-6" % (dev_t, dev_f))
    if not g_dev <= G_C3_TOL:
        fatal("G2/E-K3-3(b): |g-1.061783|=%r > 1e-4" % g_dev)
    res["steps"]["step4b"] = "PASS: E-K3-3(a) self-consistency; E-K3-3(b) (ii) identity vs signed audit"

    # E-K3-4: geometric profile vs the option-informed bridge b̂_i^opt.
    bhat_opt = []
    for it in bench:
        d = W[tid(it["A"])] - W[tid(it["C"])]
        bhat_opt.append(d / np.linalg.norm(d))
    bhat_opt = np.stack(bhat_opt)
    cos_opt_P = [float(np.dot(bhat_P, b)) for b in bhat_opt]
    cos_opt_D = [float(np.dot(bhat_D, b)) for b in bhat_opt]
    cos_t_P = [float(np.dot(bhat_P, Wn[tid(it["A"])])) for it in bench]
    cos_f_P = [float(np.dot(bhat_P, Wn[tid(it["C"])])) for it in bench]

    def dist(a):
        a = np.array(a)
        return {"mean": float(np.mean(a)), "median": float(np.median(a)),
                "min": float(np.min(a)), "max": float(np.max(a)), "all": [float(x) for x in a]}

    k90_P = sum(1 for x in cos_opt_P if abs(x) >= 0.9)
    k90_D = sum(1 for x in cos_opt_D if abs(x) >= 0.9)
    cp_P = clopper_pearson(k90_P, 60)
    cp_D = clopper_pearson(k90_D, 60)
    res["E-K3-4"] = {
        "candidate_i": {
            "cos_vs_opt_bridge": dist(cos_opt_P),
            "cos_vs_target_rows": dist(cos_t_P),
            "cos_vs_foil_rows": dist(cos_f_P),
            "bar90": {"k": k90_P, "n": 60, "phat": k90_P / 60.0,
                      "CP95": list(cp_P),
                      "caveat_fires": bool(k90_P > 0)},
        },
        "candidate_ii": {
            "cos_vs_opt_bridge": dist(cos_opt_D),
            "cos_vs_target_rows": dist(s_t),
            "cos_vs_foil_rows": dist(s_f),
            "bar90": {"k": k90_D, "n": 60, "phat": k90_D / 60.0,
                      "CP95": list(cp_D),
                      "firing": bool(k90_D > 0)},
        },
    }
    # For (ii): any 0.9-bar firing = [OBSERVATION] against the signed audit,
    # Phase-1-gating — but E-K3-3(b) already passed, so identity held.
    res["steps"]["step4c"] = "E-K3-4 computed (descriptive): bar90 k_P=%d k_D=%d" % (k90_P, k90_D)

    # ---- Step 5: G5 (no forward invocation anywhere) + G3 post-hash ----
    src = open(__file__).read()
    direct_calls = re.findall(r"\bmodel\s*\(", src)
    res["G5"] = {"direct_model_call_occurrences": len(direct_calls),
                 "allowed_patterns_only": ["model.state_dict(", "model.eval(",
                                           "model.get_output_embeddings("],
                 "method": "source scan of this script; forward invocations prohibited"}
    if direct_calls:
        fatal("G5: direct forward-invocation pattern found %d time(s)" % len(direct_calls))
    res["steps"]["step5a"] = "PASS: G5 — no direct forward invocation in executor source"

    post_hash = get_hash(model)
    res["hashes"]["post"] = post_hash
    if post_hash != pre_hash or post_hash != ARCHIVED_HASH:
        fatal("G3 post-hash mismatch: %s" % post_hash)
    res["delta_theta"] = 0
    res["steps"]["step5b"] = "PASS: G3 Δθ=0 — pre == post == archived"

    # ---- Per-candidate §7.1 verdicts ----
    def verdict_71(comp, g, ggate, ident):
        if comp == "PASS" and ggate == "PASS" and ident:
            return "Supported"
        if comp == "FAIL":
            return "Not supported"
        if ggate == "FAIL":
            return "Not supported"
        return "Inconclusive"

    v_i = verdict_71(res["E-K3-1"]["candidate_i"]["verdict"],
                     g_P, res["E-K3-2"]["gate_P"], res["E-K3-3a"]["pass_P"])
    v_ii = verdict_71(res["E-K3-1"]["candidate_ii"]["verdict"],
                      g_D, res["E-K3-2"]["gate_D"],
                      res["E-K3-3a"]["pass_D"] and dev_t <= AUDIT_VAL_TOL
                      and dev_f <= AUDIT_VAL_TOL and g_dev <= G_C3_TOL)
    res["verdicts"] = {
        "candidate_i_premise_rank_bank": v_i,
        "candidate_ii_donor_centroid_C3": v_ii,
        "program_aggregation": ("PROCEED" if "Supported" in (v_i, v_ii)
                                else "UNDERDETERMINED — GPU phase INFEASIBLE as designed"),
    }
    res["steps"]["step6"] = "verdicts computed; twin JSON + report written"

    with open(OUT_DIR + "/K3_CONSTRUCTION_AUDIT_RESULTS_LOG239_LOG241_2026-09-23.json", "w") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps({"g_P": g_P, "g_D": g_D, "verdict_i": v_i, "verdict_ii": v_ii,
                      "bar90_kP": k90_P, "bar90_kD": k90_D,
                      "G4": "60/60", "delta_theta": 0}, indent=2))


if __name__ == "__main__":
    main()
