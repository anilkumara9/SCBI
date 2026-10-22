#!/usr/bin/env python3
"""EXP087 runner — translation-signature measurement and adjudication.

Modes:
  --analyze --per-item PATH --k1 PATH --archive PATH [--out PATH]
      CPU analysis path (the bundle's primary deliverable): load fresh-run
      per-item logs, apply the pinned c_i join, compute all endpoints,
      adjudicate the falsification table, write the report. No weights.
  --mock
      Synthetic end-to-end on CPU (used by mock_harness.py).
  --execute --bundle-review-signoff --ceo-gpu-clearance [other flags]
      LICENSED GPU EXECUTION PATH ONLY. Refuses (exit 2) without BOTH
      flags. Runs the C1/C2/C3 arms on pythia-410m/L20 (180 passes),
      then the analysis path. This build is NOT cleared for execution:
      independent Law #14 bundle review + CEO GPU clearance required.

Per-item log schema (fresh-run records, one per line or a JSON list):
  {instance_key, prompt, prompt_sha256, t_id, f_id,
   m0, argmax_c1, dm_c2, argmax_c2, dm_c3, argmax_c3}
Decisions are derived: base_correct = (argmax_c1 == t_id), etc.
"""

import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import exp087_benchmark as B
import exp087_guards as G
import exp087_join as J
import exp087_statistics as S
import exp087_verdicts as V

HERE = os.path.dirname(os.path.abspath(__file__))
SCBI = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def log(msg, fh=None):
    line = f"[EXP087] {msg}"
    print(line, flush=True)
    if fh is not None:
        fh.write(line + "\n")
        fh.flush()


# ---------------------------------------------------------------------------
# Analysis path (CPU, no weights)
# ---------------------------------------------------------------------------

def load_per_item_logs(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    recs = data["records"] if isinstance(data, dict) and "records" in data else data
    if len(recs) != G.N_ITEMS:
        raise G.BundleError(f"analyze: {len(recs)} records, expected {G.N_ITEMS}")
    required = {"instance_key", "prompt", "prompt_sha256", "t_id", "f_id",
                "m0", "argmax_c1", "dm_c2", "argmax_c2", "dm_c3", "argmax_c3"}
    for i, r in enumerate(recs):
        missing = required - set(r.keys())
        if missing:
            raise G.BundleError(f"analyze: record {i} missing fields {missing}")
        # prompt_sha256 self-consistency (cheap apparatus check)
        h = B.prompt_sha256(r["prompt"])
        if h != r["prompt_sha256"]:
            raise G.BundleError(
                f"analyze: record {i} ({r['instance_key']}) prompt_sha256 "
                f"mismatch — log tampering or corruption (apparatus)")
    return recs


def analyze(per_item_path, k1_path, archive_path, out_path=None):
    """Full analysis path: join -> endpoints -> verdicts -> report."""
    G.crash_guard(SCBI)
    log("analysis path: loading inputs")
    fresh = load_per_item_logs(per_item_path)
    c_list = J.load_c_vector(k1_path)
    with open(archive_path, "r", encoding="utf-8") as f:
        archive = json.load(f)

    log("applying the pinned c_i join (§8 item 2)")
    try:
        joined = J.pinned_join(c_list, fresh, archive)
    except G.JoinError as e:
        # Build-lane resolution (flagged for review): a join failure at
        # execution time is apparatus failure → RUN-INVALID, never a
        # silently mis-paired R4.
        log(f"JOIN FAILED: {e}")
        report = {
            "experiment": "EXP087",
            "verdict": "RUN-INVALID",
            "verdict_row": "pinned_join",
            "verdict_note": ("pinned c_i join failed at execution time "
                             "(apparatus); R4 unlicensed on mis-paired data; "
                             "mechanism verdict withheld, rerun required. "
                             "Build-lane resolution — flagged for review."),
            "join_error": str(e),
        }
        return write_report(report, out_path)

    # Build analysis records in O order; decisions derived from argmax ids.
    records = []
    for rec in joined:
        records.append({
            "instance_key": rec["instance_key"],
            "m0": float(rec["m0"]),
            "dm_c2": float(rec["dm_c2"]),
            "dm_c3": float(rec["dm_c3"]),
            "base_correct": int(rec["argmax_c1"]) == int(rec["t_id"]),
            "c2_correct": int(rec["argmax_c2"]) == int(rec["t_id"]),
            "c3_correct": int(rec["argmax_c3"]) == int(rec["t_id"]),
        })
    c_vals = [rec["c_i"] for rec in joined]

    log("adjudicating the falsification table")
    report = V.adjudicate(records, c_vals)
    report["experiment"] = "EXP087"
    report["determinism"] = G.determinism_fingerprint()
    report["license_note"] = ("analysis path is CPU-only; GPU execution "
                              "requires independent bundle review SIGN + "
                              "CEO GPU clearance")
    return write_report(report, out_path)


def write_report(report, out_path):
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        log(f"report written to {out_path}")
    log(f"VERDICT: {report['verdict']} (row: {report.get('verdict_row')})")
    return report


# ---------------------------------------------------------------------------
# Licensed execution path (GPU) — NOT cleared in this build
# ---------------------------------------------------------------------------

def execute(args):
    """The GPU model loop. Refuses without both license flags (exit 2)."""
    G.crash_guard(SCBI)
    try:
        G.require_execution_license(args, log_fn=lambda m: log(m))
    except G.RefusalError as e:
        log(f"FATAL: {e}")
        sys.exit(2)

    import torch
    log("licensed execution path: loading model (GPU)")
    torch.manual_seed(G.MASTER_SEED)
    if torch.cuda.is_available():
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    from transformers import AutoModelForCausalLM, AutoTokenizer
    device = "cuda"
    model = AutoModelForCausalLM.from_pretrained(
        G.MODEL_ID, revision=G.MODEL_REVISION,
        torch_dtype=torch.float32, trust_remote_code=False).to(device)
    tok = AutoTokenizer.from_pretrained(
        G.MODEL_ID, revision=G.MODEL_REVISION, trust_remote_code=False)
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)

    guard = G.FrozenBackboneGuard()
    pre = guard.capture_pre(model.state_dict())
    log(f"Δθ=0 guard pre-hash: {pre[:16]}...")

    # Benchmark items + G2 byte-identity against the archive.
    items = B.build_items()
    archive_path = args.archive or B.default_archive_path()
    B.g2_byte_identity_check(archive_path)
    log("G2 byte-identity check passed (60/60 prompts, O order)")

    # C3 support vector (EXP066-verbatim construction).
    import exp087_support as SUP
    b_agg = SUP.build_b_agg(model, tok, device, G.LAYER_INDEX,
                            log_fn=lambda m: log(m))

    layer_module = model.gpt_neox.layers[G.LAYER_INDEX]
    embed_out = model.embed_out.weight.detach()

    def make_bridge_vec(t_id, f_id):
        w = embed_out[t_id, :] - embed_out[f_id, :]
        return w / (torch.norm(w) + 1e-12)

    def run_arm(prompt, t_id, f_id, vec):
        """One item, one arm: returns (m, argmax_id). vec=None → C1."""
        inp = tok.encode(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            if vec is None:
                out = model(input_ids=inp)
            else:
                v = (G.ALPHA * vec).to(device).view(1, 1, -1)
                handle = layer_module.register_forward_hook(
                    lambda mod, i, o: (o[0] + v,) + o[1:]
                    if isinstance(o, tuple) else o + v)
                try:
                    out = model(input_ids=inp)
                finally:
                    handle.remove()
        logits = out.logits[0, -1, :]
        m = float(logits[t_id].item() - logits[f_id].item())
        argmax_id = int(torch.argmax(logits).item())
        return m, argmax_id

    log("C1/C2/C3 arms: 180 passes")
    records = []
    for j, (item, key) in enumerate(zip(items, B.order_O())):
        t_id = tok.encode(item["target_token"])[0]
        f_id = tok.encode(item["foil_token"])[0]
        m0, a1 = run_arm(item["prompt"], t_id, f_id, None)
        bv = make_bridge_vec(t_id, f_id)
        m2, a2 = run_arm(item["prompt"], t_id, f_id, bv)
        dm2 = m2 - m0
        m3, a3 = run_arm(item["prompt"], t_id, f_id, b_agg)
        dm3 = m3 - m0
        records.append({
            "instance_key": key,
            "prompt": item["prompt"],
            "prompt_sha256": B.prompt_sha256(item["prompt"]),
            "t_id": t_id, "f_id": f_id,
            "m0": m0, "argmax_c1": a1,
            "dm_c2": dm2, "argmax_c2": a2,
            "dm_c3": dm3, "argmax_c3": a3,
        })
        if (j + 1) % 20 == 0:
            log(f"  {j + 1}/60 items")

    post = guard.capture_post(model.state_dict())
    guard.verify()
    log(f"Δθ=0 guard verified (pre == post == {post[:16]}...)")

    per_item_path = os.path.join(HERE, "out", "exp087_per_item_logs.json")
    os.makedirs(os.path.dirname(per_item_path), exist_ok=True)
    with open(per_item_path, "w", encoding="utf-8") as f:
        json.dump({"records": records}, f)
    log(f"per-item logs written ({len(records)} records)")

    k1_path = args.k1 or J.default_k1_path()
    # F2 (LOG-340 repair): the full guard evidence goes into the report
    # JSON — a revision/pin failure must be detectable post-hoc, not just
    # as 16 hex chars on stdout.
    report = analyze(per_item_path, k1_path, archive_path, None)
    report["model_id"] = G.MODEL_ID
    report["model_revision"] = G.MODEL_REVISION
    report["state_dict_hash_pre"] = pre
    report["state_dict_hash_post"] = post
    report["delta_theta_zero"] = (pre == post)
    return write_report(report, args.out)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="EXP087 translation-signature runner")
    ap.add_argument("--analyze", action="store_true")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--per-item", default=None)
    ap.add_argument("--k1", default=None)
    ap.add_argument("--archive", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--bundle-review-signoff", action="store_true")
    ap.add_argument("--ceo-gpu-clearance", action="store_true")
    args = ap.parse_args(argv)

    modes = [args.analyze, args.mock, args.execute]
    if sum(modes) != 1:
        ap.error("exactly one of --analyze / --mock / --execute required")

    if args.mock:
        log("--mock: synthetic end-to-end (CPU, no weights)")
        sys.path.insert(0, HERE)
        import mock_harness
        return mock_harness.run_all()

    if args.analyze:
        if not args.per_item:
            ap.error("--analyze requires --per-item PATH")
        return analyze(args.per_item,
                       args.k1 or J.default_k1_path(),
                       args.archive or B.default_archive_path(),
                       args.out)

    if args.execute:
        return execute(args)


if __name__ == "__main__":
    main()
