"""EXP083 (R1 RCPA kill pilot) — runner.

Modes:
  --smoke   CPU startup smoke test on synthetic fixtures (the §6 startup
            smoke; §A.2.5/§A.2.6). No model, no weights, no GPU.
  --run     Full GPU execution on the user's Kaggle node. Requires
            --gpu-clearance (CEO clearance, post Law #14 bundle review).
            Refuses to run without it, and refuses on any machine without
            torch + the model weights.

The full-run wiring (GPU node):
  1. pre-run SHA-256 over state_dict() vs pinned expected (R3) -> INVALID(i)
     BEFORE any pass is allocated;
  2. startup smoke (<=12 passes): verdict-path reachability, identity-vs-
     archive on the clean-read decisions, throughput >= 80%;
  3. clean-read pass x60 -> r_i, G-norm (floor, exclusions), G-static,
     G-curve ($0 CPU);
  4. if G-static fires on the validated apparatus -> RE-SKIN KILL, stop
     (flip arms not run — GPU saved);
  5. A_r x60, A_g x60 (torch ĝ_i, seeds 20260924+i, greedy decoding);
  6. post-run SHA-256 (Delta theta = 0); adjudicate (§8 verdict table,
     M1 precedence); write the run manifest.

Budget: the PassCounter refuses pass 193 (§6 hard stop). The A_0 identity
arm is $0 by reuse of the clean-read greedy decisions (R4).
"""

import os
import sys
import json
import argparse
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp083_guards import PassCounter, PassBudgetExceeded, MAX_PASSES, HARD_STOP

HERE = os.path.dirname(os.path.abspath(__file__))
PROTOCOL = os.path.normpath(os.path.join(
    HERE, "..", "..", "protocols", "EXP083_RCPA_PREREG_SPEC.md"))


def cmd_smoke(_args):
    from smoke_test import main as smoke_main
    return smoke_main()


def cmd_run(args):
    if not args.gpu_clearance:
        print("REFUSED: --run requires --gpu-clearance (CEO clearance, post "
              "Law #14 bundle review). Nothing was executed.")
        return 2
    try:
        import torch  # noqa: F401
    except ImportError:
        print("REFUSED: torch is not installed on this machine. The full run "
              "executes on the user's Kaggle GPU node only.")
        return 2
    # The live execution path is implemented here on the GPU node; the CPU
    # build machine never reaches this point (no weights, no torch).
    print("GPU execution path: licensed scope is bundle construction only "
          "(LOG-257). Execution is NOT licensed in this build.")
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser(description="EXP083 R1 RCPA kill-pilot runner")
    ap.add_argument("--smoke", action="store_true",
                    help="CPU startup smoke test on synthetic fixtures")
    ap.add_argument("--run", action="store_true",
                    help="full GPU execution (requires --gpu-clearance)")
    ap.add_argument("--gpu-clearance", action="store_true",
                    help="CEO GPU clearance flag")
    args = ap.parse_args(argv)
    if args.smoke:
        return cmd_smoke(args)
    if args.run:
        return cmd_run(args)
    ap.print_help()
    print("\nNo mode selected. Use --smoke (CPU) or --run --gpu-clearance (GPU node).")
    return 2


if __name__ == "__main__":
    sys.exit(main())
