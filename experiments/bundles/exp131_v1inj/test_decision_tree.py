#!/usr/bin/env python3
"""Unit tests for the EXP131 decision tree (protocol §2 + §4, KILL branches first per FIX-1).

Pure logic tests — no model, no GPU. Verifies every tree branch is
reachable in code: CONTINUE, KILL (c-hat / inert / flat-trend /
bar-unmet), HELD, RUN-INVALID (B_agg drift), APPARATUS-VOID.

Run:  python3 test_decision_tree.py
"""
import importlib.util
import math
import os
import sys

_spec = importlib.util.spec_from_file_location(
    "run_exp131", os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_exp131.py"))
_mod = importlib.util.module_from_spec(_spec)
# Prevent main() from running on import: it is under __main__ guard already.
_spec.loader.exec_module(_mod)
decision_tree = _mod.decision_tree
binom_sf_ge = _mod.binom_sf_ge

PASS = 0
FAIL = 0


def check(name, got, want_verdict):
    global PASS, FAIL
    v, reason = got
    if v == want_verdict:
        PASS += 1
        print("PASS %s -> %s (%s)" % (name, v, reason))
    else:
        FAIL += 1
        print("FAIL %s: got %s (%s), want %s" % (name, v, reason, want_verdict))


def base(**kw):
    vi = {"c_hat": 0.5, "dm_v1": 5, "mcnemar_p": 0.01, "rank_trend": True,
          "median_r": 3.0, "dm_bagg": 0, "apparatus_void": None}
    vi.update(kw)
    return vi


# 1. CONTINUE — all conjunctive bars met.
check("CONTINUE", decision_tree(base()), "CONTINUE")

# 2. KILL — c-hat gate (decision-orthogonal amplifier).
check("KILL:c_hat", decision_tree(base(c_hat=0.05)), "KILL")

# 3. KILL — v1 inert.
check("KILL:inert", decision_tree(base(dm_v1=0, median_r=1.0)), "KILL")

# 4. KILL — flat rank trend.
check("KILL:flat-trend", decision_tree(base(rank_trend=False)), "KILL")

# 5. KILL — bar unmet: median r < 2 but DM_v1 > 0 (hypothesis's >=2x core falsified).
check("KILL:r-bar-unmet", decision_tree(base(median_r=1.5)), "KILL")

# 6. KILL — bar unmet: McNemar p not significant.
check("KILL:p-unmet", decision_tree(base(mcnemar_p=0.2)), "KILL")

# 7. HELD — margin gain without flips.
check("HELD", decision_tree(base(median_r=2.5, dm_v1=0, mcnemar_p=1.0)), "HELD")

# 8. RUN-INVALID — B_agg null-control fired (takes precedence over KILL).
check("RUN-INVALID", decision_tree(base(dm_bagg=2)), "RUN-INVALID")

# 9. APPARATUS-VOID — takes precedence over everything.
check("APPARATUS-VOID", decision_tree(base(dm_bagg=2, apparatus_void="pin miss")), "APPARATUS-VOID")

# 10. KILL precedence: c-hat fires before inertness when both hold.
check("KILL:precedence", decision_tree(base(c_hat=0.05, dm_v1=0)), "KILL")

# McNemar exact table spot-checks against the protocol's §3.7 a-priori table.
assert abs(binom_sf_ge(5, 5) - 0.0312) < 1e-4, binom_sf_ge(5, 5)
assert abs(binom_sf_ge(6, 6) - 0.0156) < 1e-4, binom_sf_ge(6, 6)
assert abs(binom_sf_ge(7, 8) - 0.0352) < 1e-4, binom_sf_ge(7, 8)
assert abs(binom_sf_ge(8, 9) - 0.0195) < 1e-4, binom_sf_ge(8, 9)
assert abs(binom_sf_ge(9, 10) - 0.0107) < 1e-4, binom_sf_ge(9, 10)
assert math.isclose(binom_sf_ge(0, 5), 1.0)
print("PASS McNemar exact table matches the protocol's §3.7 a-priori table (5/5, 6/6, 7/8, 8/9, 9/10)")
PASS += 1

print("\n%d passed, %d failed" % (PASS, FAIL))
sys.exit(1 if FAIL else 0)
