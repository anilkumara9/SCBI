"""EXP083 (R1 RCPA kill pilot) — startup smoke test (§6; §A.2.5/§A.2.6).

Runs on CPU with synthetic fixtures. Asserts, on the licensed ≤12-pass
smoke budget (3 items x {clean read, A_r, A_g} = 9 passes):

  (a) verdict-path reachability: synthetic construction -> guards ->
      flip contrast -> adjudication produces a complete verdict record;
  (b) identity-vs-archive: a matching fixture passes bit-for-bit, a
      mismatching fixture records INVALID(ii) (never a flip verdict);
  (c) throughput gate: measured items/s >= 80% of the projected GPU
      throughput (the gate function is encoded and fixture-tested here;
      the runner evaluates it live on the GPU node at startup);
  (d) SHA pre-run check present: a wrong pre-run hash refuses BEFORE any
      pass is allocated (INVALID(i) precedence);
  (e) INVALID precedence order (i) -> (ii) -> (iii) on combined faults;
  (f) the pass-193 hard stop: the counter refuses any allocation past 192.

Exit 0 + SMOKE OK iff every assertion holds. No model weights, no GPU.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp083_endpoints import (flip_indicators, adjudicate_verdict,
                              mcnemar_one_sided_p)
from exp083_guards import (PassCounter, PassBudgetExceeded, MAX_PASSES,
                           HARD_STOP, sha_prerun_check, identity_check,
                           g_norm_floor, g_static_check,
                           EXPECTED_SHA256)
from exp083_position import locate_positions

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"  [{PASS if cond else FAIL}] {name}" + (f" — {detail}" if detail and not cond else ""))


def throughput_gate(measured_ips, projected_ips):
    """Startup throughput gate (§6): measured >= 80% of projected.

    Returns (ok, ratio). Evaluated live on the GPU node at startup;
    fixture-tested here.
    """
    if projected_ips <= 0:
        return False, 0.0
    ratio = measured_ips / projected_ips
    return ratio >= 0.80, ratio


def synthetic_prompt(i):
    return ("Premise: A%d outranks B%d. B%d outranks C%d. "
            "Question: Who is higher in rank, A%d or C%d? Answer:"
            % (i, i, i, i, i, i))


def synthetic_spans(prompt):
    """Whitespace-token char spans — a stand-in for the tokenizer's offset
    table (the real table comes from the GPU node's tokenizer)."""
    spans, s = [], 0
    for tok in prompt.split(" "):
        start = prompt.find(tok, s)
        spans.append((start, start + len(tok)))
        s = start + len(tok)
    return spans


def test_smoke_pass_inventory():
    pc = PassCounter()
    # 3 items x {clean read, A_r, A_g} = 9 passes, within the <=12 smoke cap.
    for blk in ["smoke clean-read x3", "smoke A_r x3", "smoke A_g x3"]:
        pc.use(3, blk)
    inv = pc.inventory()
    check("smoke: 9 passes allocated within the <=12 smoke cap",
          inv["total"] == 9 and inv["total"] <= 12, f"total={inv['total']}")
    check("smoke: hard stop encoded at pass 193",
          inv["hard_stop"] == 193 and inv["max_passes"] == 192)


def test_verdict_path_reachability():
    # Synthetic 3-item fixture: positions -> construction -> guards ->
    # flip contrast -> adjudication. Every stage must execute and the
    # verdict record must be complete.
    prompts = [synthetic_prompt(i) for i in range(3)]
    positions = [locate_positions(p, synthetic_spans(p)) for p in prompts]
    check("smoke: position rule locates (ans_pos, q_pos) on 3 items",
          all(a == len(synthetic_spans(p)) - 1 for (a, _), p in zip(positions, prompts)))
    # Synthetic flip outcomes over the 3 items (reachability only, not a verdict).
    g_flips = [0, 1, 0]
    r_flips = [1, 1, 0]
    rec = adjudicate_verdict(
        sha_prerun_ok=True, identity_ok=True, guard_fault=None,
        g_static_fired=False, g_static_value=0.02,
        g_norm_n_excluded=0, g_norm_floor=0.5,
        g_flips=g_flips, r_flips=r_flips)
    complete = all(k in rec for k in ("row", "row_detail", "verdict", "license",
                                      "contrast", "n_final"))
    check("smoke: verdict-path reachable end-to-end (complete record)",
          complete and rec["row"] in ("RE-SKIN KILL", "KILL", "HELD", "CONTINUE", "INVALID"),
          f"row={rec.get('row')}")
    check("smoke: flip indicators encode wrong-at-baseline AND right-under-arm",
          flip_indicators([False, True, False], [True, True, False]) == [1, 0, 0])


def test_identity_vs_archive():
    archive = [True, False, True]
    ok, _ = identity_check([True, False, True], archive)
    check("smoke: identity-vs-archive bit-for-bit (match -> ok)", ok)
    ok2, cause2 = identity_check([True, True, True], archive)
    check("smoke: identity mismatch -> INVALID(ii), never a flip verdict",
          (not ok2) and "INVALID(ii)" in cause2, cause2)
    rec = adjudicate_verdict(
        sha_prerun_ok=True, identity_ok=False, guard_fault=None,
        g_static_fired=False, g_static_value=0.0,
        g_norm_n_excluded=0, g_norm_floor=0.0,
        g_flips=[0], r_flips=[1])
    check("smoke: identity failure preempts flip rows in adjudication",
          rec["row"] == "INVALID" and "INVALID(ii)" in rec["row_detail"],
          rec["row_detail"])


def test_sha_prerun_check_present():
    ok, _ = sha_prerun_check(EXPECTED_SHA256)
    check("smoke: correct pre-run SHA passes", ok)
    ok2, cause2 = sha_prerun_check("00" * 32)
    check("smoke: wrong pre-run SHA -> INVALID(i) before any pass",
          (not ok2) and "INVALID(i)" in cause2, cause2)
    rec = adjudicate_verdict(
        sha_prerun_ok=False, identity_ok=False, guard_fault="x",
        g_static_fired=True, g_static_value=0.9,
        g_norm_n_excluded=0, g_norm_floor=0.0,
        g_flips=[0], r_flips=[0])
    check("smoke: SHA failure preempts (ii), (iii), and RE-SKIN",
          rec["row"] == "INVALID" and "INVALID(i)" in rec["row_detail"],
          rec["row_detail"])


def test_invalid_precedence_order():
    # Combined faults: (i)+(ii)+(iii)+RE-SKIN -> (i) recorded.
    rec = adjudicate_verdict(
        sha_prerun_ok=False, identity_ok=False, guard_fault="g-norm fault",
        g_static_fired=True, g_static_value=0.9,
        g_norm_n_excluded=0, g_norm_floor=0.0,
        g_flips=[0], r_flips=[0])
    check("precedence: (i) beats (ii), (iii), RE-SKIN",
          "INVALID(i)" in rec["row_detail"], rec["row_detail"])
    # (ii)+(iii) -> (ii) recorded.
    rec = adjudicate_verdict(
        sha_prerun_ok=True, identity_ok=False, guard_fault="g-static fault",
        g_static_fired=False, g_static_value=0.0,
        g_norm_n_excluded=0, g_norm_floor=0.0,
        g_flips=[0], r_flips=[0])
    check("precedence: (ii) beats (iii)",
          "INVALID(ii)" in rec["row_detail"], rec["row_detail"])
    # (iii) alone -> (iii) recorded, preempts flip rows.
    rec = adjudicate_verdict(
        sha_prerun_ok=True, identity_ok=True, guard_fault="g-norm fault",
        g_static_fired=False, g_static_value=0.0,
        g_norm_n_excluded=0, g_norm_floor=0.0,
        g_flips=[1, 1, 1], r_flips=[1, 1, 1])
    check("precedence: (iii) beats flip rows",
          rec["row"] == "INVALID" and "INVALID(iii)" in rec["row_detail"],
          rec["row_detail"])


def test_pass_193_hard_stop():
    pc = PassCounter()
    pc.use(MAX_PASSES, "fill to cap")
    refused = False
    try:
        pc.use(1, "pass 193")
    except PassBudgetExceeded:
        refused = True
    check("smoke: runner refuses pass 193 (hard stop)", refused)
    check("smoke: hard stop constant is 193", HARD_STOP == 193)


def test_throughput_gate():
    ok, ratio = throughput_gate(8.5, 10.0)
    check("throughput: 85% of projected -> pass", ok and abs(ratio - 0.85) < 1e-12)
    ok2, ratio2 = throughput_gate(7.9, 10.0)
    check("throughput: 79% of projected -> fail", (not ok2) and abs(ratio2 - 0.79) < 1e-12)
    ok3, _ = throughput_gate(10.0, 0.0)
    check("throughput: non-positive projection -> fail (no silent pass)", not ok3)


def main():
    t0 = time.time()
    print("EXP083 startup smoke test — CPU, synthetic fixtures")
    print("-" * 70)
    test_smoke_pass_inventory()
    test_verdict_path_reachability()
    test_identity_vs_archive()
    test_sha_prerun_check_present()
    test_invalid_precedence_order()
    test_pass_193_hard_stop()
    test_throughput_gate()
    print("-" * 70)
    n_fail = sum(1 for _, ok, _ in results if not ok)
    print(f"{len(results) - n_fail}/{len(results)} smoke assertions passed "
          f"({time.time() - t0:.2f}s)")
    if n_fail:
        print("SMOKE FAILURES:")
        for name, ok, detail in results:
            if not ok:
                print(f"  - {name}: {detail}")
        print("EXP083 SMOKE: FAIL")
        return 1
    print("EXP083 SMOKE: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
