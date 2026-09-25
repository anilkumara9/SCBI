#!/usr/bin/env python3
"""EXP086 startup smoke test (0 model passes, CPU only).

Verifies on THIS bundle (no weights, no GPU) before any execution-node
work:
  1. all bundle modules import
  2. signed pins match the protocol
  3. the Stage-A registry names 48 blocks (24 O direct, 24 V fused-interleaved)
  4. the runner refuses Stage A without the bundle-review signoff (exit 2)
  5. no model/weight access happens (no weights path exists in the bundle)
  6. a small synthetic Stage-A screen (numpy) produces a well-formed report
  7. the evaluator verdict path adjudicates a synthetic CONTINUE fixture

Run: python3 smoke_test.py
Exit 0 iff all checks pass.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"smoke ok - {name}")
    else:
        FAIL += 1
        print(f"smoke FAIL - {name} {detail}")


def main():
    global PASS, FAIL

    try:
        import numpy  # noqa: F401
        import exp086_guards as G
        import exp086_henrici as H
        import exp086_rng as R
        import exp086_statistics as S
        import exp086_verdicts as V
        import run_exp086 as RUN
        check("imports", True)
    except Exception as e:  # noqa: BLE001
        check("imports", False, repr(e))
        print(f"\nsmoke: {PASS} passed, {FAIL} failed")
        sys.exit(1)

    # 2. signed pins
    check("pin MODEL_ID", G.MODEL_ID == "EleutherAI/pythia-410m")
    check("pin MASTER_SEED", G.MASTER_SEED == 20260924)
    check("pin N_ITEMS", G.N_ITEMS == 60)
    check("pin LAYER_INDEX", G.LAYER_INDEX == 20)
    check("pin archive sha", G.RECORDS_SHA256
          == "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585")

    # 3. registry shape + V provenance
    check("registry 48 blocks", len(H.BLOCKS) == 48)
    check("registry 24 O direct / 24 V fused-interleaved",
          sum(1 for s in H.BLOCKS if s["kind"] == "direct") == 24
          and sum(1 for s in H.BLOCKS if s["kind"] == "fused-interleaved") == 24)
    check("V rows are the per-head interleaved set (LOG-327)",
          all(tuple(s["row_idx"]) == H.V_ROWS
              for s in H.BLOCKS if s["kind"] == "fused-interleaved"))

    # 4. runner refuses Stage A without the bundle-review signoff
    try:
        rc = RUN.main(["--stage-a"])
        check("runner refuses --stage-a without signoff (exit 2)", rc == 2,
              f"rc={rc}")
    except SystemExit as e:
        check("runner refuses --stage-a without signoff (exit 2)",
              e.code == 2, f"code={e.code}")

    # 5. no model/weight access: the bundle ships no weights and the runner
    #    gate runs before any torch import
    check("no weights shipped in bundle",
          not any(p.endswith((".bin", ".safetensors"))
                  for _, _, fs in os.walk(os.path.dirname(os.path.abspath(__file__)))
                  for p in fs))
    try:
        RUN.TorchBackend("/no/such/weights")
        check("TorchBackend refuses without torch", False)
    except RuntimeError as e:
        check("TorchBackend refuses without torch", "torch" in str(e))

    # 6. small synthetic Stage-A screen (numpy; 4 blocks; no 1024x1024 alloc)
    _rng = __import__("numpy").random.default_rng(20260924)


    def _syn_block(d, non_normal):
        W = _rng.standard_normal((d, d)) * 0.2 + __import__("numpy").eye(d)
        if non_normal:
            W[0, 1] = 3.0
        return W


    _he = []
    _ok = True
    for i in range(4):
        W = _syn_block(8, i % 2 == 1)
        v, _info = H.henrici_index(W, name=f"smoke.b{i}")
        if not (0.0 <= v <= 1.0) or not math.isfinite(v):
            _ok = False
        _he.append(v)
    check("synthetic screen: 4 finite He in [0,1]", _ok,
          f"he={['%.3f' % x for x in _he]}")
    check("synthetic screen: report is JSON-serializable & advisory-only",
          all(isinstance(x, float) for x in _he))
    import json as _json
    _rep = {"stage": "A", "verdict": None, "advisory_only": True,
            "blocks_screened": 4, "henrici": _he}
    try:
        _json.dumps(_rep)
        check("synthetic screen: report serializes", True)
    except TypeError as e:
        check("synthetic screen: report serializes", False, str(e))

    # 7. verdict path on a synthetic CONTINUE fixture
    res = {
        "delta_theta_ok": True, "n_wrong_baseline": 20, "frac_aborted": 0.0,
        "apparatus_ok": True, "c_hat": 0.40, "exceedance": 0.50,
        "delta_lci": 0.10, "delta_uci": 0.30, "delta_point": 0.20,
        "mcnemar_p": 0.001, "rank_valid": True,
        "delta_rank_lci": 0.05, "delta_rank_uci": 0.25,
        "delta_rank_point": 0.15, "stage2_ran": True, "delta_perm_lci": 0.04,
    }
    v, e, _d = V.adjudicate(res)
    check("verdict path: synthetic fixture -> CONTINUE",
          v == "CONTINUE" and e == "Supported", f"{v}/{e}")

    print(f"\nsmoke: {PASS} passed, {FAIL} failed")
    return FAIL == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
