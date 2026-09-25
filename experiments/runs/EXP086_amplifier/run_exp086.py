#!/usr/bin/env python3
"""EXP086 runner: R3 dynamical-amplifier / singular-vector-aligned injection.

Implements the signed protocol
experiments/protocols/EXP086_R3_AMPLIFIER_PREREG_SIGNED.md (LOG-311, CEO-signed).

TWO MODES (one bundle, two gates):
  --stage-a : Stage A ($0 CPU, weight-only, ADVISORY). Licensed on bundle
              build (LOG-311) but weight access happens ONLY after the
              independent Law #14 bundle review -> requires
              --bundle-review-signoff (refuses with exit 2 otherwise).
              NEVER emits a verdict (structural; see exp086_henrici).
  --run     : Stage B GPU pilot orchestration (backend-neutral run_full_loop;
              the TorchBackend sketch is execution-node code). NOT licensed:
              requires BOTH --ceo-gpu-clearance AND --stage2-review-signoff
              (refuses with exit 2 otherwise). Queue: behind K2 -> EXP083 ->
              EXP084; no pre-emption.

Frozen backbone (Law #6): read-only weight access; FrozenBackboneGuard hashes
state_dict before/after every weight-touching phase; mismatch -> INVALID V1.
Deterministic (Law #13): seeds pinned, env manifest logged, parameter hashes
recorded, raw per-item logs preserved.

Pass budget (§11, binding): 121 fwd-equiv/item x 60 = 7260; Stage-2 permuted
arm = 120; total hard ceiling 7380. The budget REFUSES the excess pass.

This file has never executed a model pass on the build machine: the
TorchBackend raises without torch, and both execution modes refuse without
their clearance flags (verified by the smoke test).
"""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp086_guards as G
import exp086_henrici as H
import exp086_rng as R
import exp086_statistics as S
import exp086_verdicts as V

HERE = os.path.dirname(os.path.abspath(__file__))
PROTOCOL_PATH = os.path.join(
    HERE, "..", "..", "protocols", "EXP086_R3_AMPLIFIER_PREREG_SIGNED.md")


# ---------------------------------------------------------------------------
# Environment manifest (Law #13)
# ---------------------------------------------------------------------------

def env_manifest(extra=None):
    """Deterministic environment manifest for every run artifact."""
    try:
        import numpy as _np
        numpy_v = _np.__version__
    except ImportError:
        numpy_v = None
    try:
        import torch as _t
        torch_v = _t.__version__
    except ImportError:
        torch_v = None
    try:
        git = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                             text=True, cwd=HERE, timeout=10)
        commit = git.stdout.strip() if git.returncode == 0 else None
    except Exception:
        commit = None
    file_hashes = {}
    for fn in ("exp086_guards.py", "exp086_henrici.py", "exp086_rng.py",
               "exp086_statistics.py", "exp086_verdicts.py", "run_exp086.py"):
        p = os.path.join(HERE, fn)
        if os.path.exists(p):
            h = hashlib.sha256()
            with open(p, "rb") as f:
                h.update(f.read())
            file_hashes[fn] = h.hexdigest()
    try:
        hp = hashlib.sha256()
        with open(PROTOCOL_PATH, "rb") as f:
            hp.update(f.read())
        protocol_digest = hp.hexdigest()
    except OSError:
        protocol_digest = None
    m = {
        "experiment": "EXP086",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "numpy": numpy_v,
        "torch": torch_v,
        "git_commit": commit,
        "bundle_file_hashes": file_hashes,
        "protocol_sha256": protocol_digest,
        "master_seed": R.MASTER_SEED,
        "model": G.MODEL_ID,
        "layer_index": G.LAYER_INDEX,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if extra:
        m.update(extra)
    return m


def atomic_write_json(path, obj):
    """Atomic JSON write (tmp + rename); never leaves a half-written record."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
        f.write("\n")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Backend protocol (backend-neutral orchestration; EXP084 LOG-268 pattern)
# ---------------------------------------------------------------------------

class Backend:
    """Abstract execution backend. The runner never touches a model directly.

    Stage A: load_state_dict_readonly() -> {name: array-like}.
    Stage B: build_probe(record, i) -> probe; baseline_forward(probe);
             power_iteration(probe, h); decision_normal_vjp(probe, h);
             inject_and_eval(probe, h, direction, eps_frac).
    directions are tags: "v1","v2","v3","vrand_<k>","bagg","permuted".
    """

    # -- Stage A --
    def load_state_dict_readonly(self):
        raise NotImplementedError

    # -- Stage B --
    def build_probe(self, record, i):
        raise NotImplementedError

    def baseline_forward(self, probe):
        """-> (correct: bool, logits: list[float], h: vector). 1 fwd."""
        raise NotImplementedError

    def power_iteration(self, probe, h):
        """Deflated power iteration, ranks 1..3.

        -> dict(v=[v1,v2,v3] unit vectors, s=[s1,s2,s3] sigma hats,
                rayleigh=[traj1,traj2,traj3], n_iters=[..]).
        Costs 108 fwd-equiv (3 vec x 12 iter x (1 JVP + 1 VJP)); the runner
        charges the budget — the backend only reports n_iters for the log.
        """
        raise NotImplementedError

    def decision_normal_vjp(self, probe, h):
        """n̂ = grad_{h}(z_top1 - z_top2), unit vector. 1 VJP = 2 fwd-equiv."""
        raise NotImplementedError

    def inject_and_eval(self, probe, h, direction, eps_frac):
        """Inject eps_frac*||h|| * direction at the answer position; re-run.

        -> (correct: bool, logits: list[float]). 1 fwd.
        """
        raise NotImplementedError

    def stage2_derangement(self, n):
        """Fixed derangement der(i) != i for the Stage-2 permuted arm (§4 F10).

        Seeded (MASTER_SEED). The TorchBackend uses exp086_rng.derangement;
        test backends supply their own deterministic derangement.
        """
        raise NotImplementedError


class TorchBackend(Backend):
    """EXECUTION-NODE ONLY (torch + transformers + weights). UNTESTED on the
    CPU build machine (torch absent); must pass the Law #14 bundle review
    before any execution. Sketch of the signed §4/§6 construction:

    - Model loaded once, .eval(), all params requires_grad_(False); the
      state_dict is snapshotted by FrozenBackboneGuard (read-only by
      construction — no optimizer, no .backward() on params, no in-place
      weight ops anywhere in this file).
    - h_l(x): forward hook on gpt_neox.layers[20] capturing the residual
      stream at the answer position (final token; program-standard site).
    - J(x) = dz/dh_l never materialized: JVP via torch.autograd.functional.jvp
      (1 fwd), VJP via torch.autograd.functional.vjp (1 bwd ~= 2 fwd-equiv),
      on the hook-captured activation leaf under torch.enable_grad().
    - Deflated power iteration: w <- (I - Vhat Vhat^T) w projections between
      ranks; 12-iteration cap; Rayleigh-quotient stall tol 1e-3 (relative).
    - Sign rule: v_r <- sign(<v_r, n̂>) v_r (§4 F2).
    - n̂: single VJP of (z_top1 - z_top2) at h_l (label-free; Law #7 clean).
    - Injection: h_l <- h_l + eps*d̂ at the answer position via a second
      forward with a perturbation hook; eps = eps_frac * ||h_l||_2.
    - Correctness: greedy-decoded answer vs the probe's labeled correct
      option — labels touch ONLY the correctness endpoint (Law #7 standard).
    - Probe rebuild: verbatim EXP077 §3 rebuild, fixed indices 0..59; the
      deviation note (EXP084-D1 class) is loudly logged by load_probe_set.
    """

    def __init__(self, weights_path, device="cuda"):
        try:
            import torch  # noqa: F401
        except ImportError:
            raise RuntimeError(
                "TorchBackend requires torch (execution node). Refusing on "
                "the CPU build machine."
            )
        self.weights_path = weights_path
        self.device = device
        self._model = None

    def load_state_dict_readonly(self):
        import torch
        from transformers import AutoModelForCausalLM
        model = AutoModelForCausalLM.from_pretrained(
            self.weights_path, torch_dtype=torch.float32, device_map="cpu")
        model.eval()
        for p in model.parameters():
            p.requires_grad_(False)
        self._model = model
        return model.state_dict()

    # Stage-B methods: full implementations are execution-node code and are
    # intentionally NOT stubbed here beyond the interface — the bundle review
    # must verify them against §4/§6 before CEO clearance. Any call on the
    # build machine raises loudly.
    def stage2_derangement(self, n):
        return R.derangement(n, R.MASTER_SEED)

    def _no(self, name):
        raise RuntimeError(
            f"TorchBackend.{name}: execution-node only (no torch here).")

    def build_probe(self, record, i):
        self._no("build_probe")

    def baseline_forward(self, probe):
        self._no("baseline_forward")

    def power_iteration(self, probe, h):
        self._no("power_iteration")

    def decision_normal_vjp(self, probe, h):
        self._no("decision_normal_vjp")

    def inject_and_eval(self, probe, h, direction, eps_frac):
        self._no("inject_and_eval")


# ---------------------------------------------------------------------------
# Stage A — $0 CPU advisory screen
# ---------------------------------------------------------------------------

def run_stage_a(backend, out_dir, log=print):
    """Execute Stage A exactly as pinned in §5. Returns the advisory report.

    Flow: crash-guard -> frozen-backbone snapshot -> read-only weight load ->
    He per square block (O direct; V via fused-QKV per-head interleaved rows,
    loud provenance) -> frozen-backbone verify (Δθ=0) -> atomic report write.
    Emits NO verdict by construction (report["verdict"] is None).
    """
    G.crash_guard("stage-a", HERE)
    os.makedirs(out_dir, exist_ok=True)
    guard = G.FrozenBackboneGuard()

    log("[Stage A] loading weights (read-only) ...")
    t0 = time.time()
    state_dict = backend.load_state_dict_readonly()
    h0 = guard.snapshot_before(state_dict)
    log(f"[Stage A] state_dict sha256 (pre):  {h0}")

    report = H.stage_a_screen(state_dict)
    h1 = guard.verify_after(state_dict)  # INVALID V1 on mismatch (loud)
    log(f"[Stage A] state_dict sha256 (post): {h1}  (Δθ=0 verified)")

    report["param_hash_pre"] = h0
    report["param_hash_post"] = h1
    report["delta_theta_zero"] = (h0 == h1)
    report["env"] = env_manifest({"mode": "stage-a"})
    report["wall_seconds"] = time.time() - t0
    atomic_write_json(os.path.join(out_dir, "exp086_stage_a_report.json"), report)
    log(f"[Stage A] advisory report written: {len(report['blocks'])} blocks, "
        f"He in [{report['He_min']:.4f}, {report['He_max']:.4f}], "
        f"mean {report['He_mean']:.4f}")
    log("[Stage A] status: ADVISORY ONLY — no verdict emitted (by design).")
    return report


# ---------------------------------------------------------------------------
# Stage B — pilot orchestration (backend-neutral)
# ---------------------------------------------------------------------------

ARMS = ("v1", "v2", "v3", "vrand", "bagg")  # §4 (matched ||δ||₂ across arms)
NORM_TAGS = (0, 1)                          # index into G.EPS_NORMS


def load_probe_set(backend):
    """Load the pinned EXP077 archive; return (records, deviation_note).

    §6.1: verbatim rebuild, fixed indices 0..59. DEVIATION NOTE (EXP084-D1
    class, build-time): the pinned archive carries no prompt strings/options/
    token IDs/margins — only per-arm correctness records. The actual probe
    strings are rebuilt verbatim per EXP077 §3 by the backend's build_probe
    on the execution node; this deviation is loudly logged here and recorded
    in every run manifest. Any paper/scoreboard use must carry this note.
    """
    path = os.path.join(HERE, *G.RECORDS_REL)
    recs = json.load(open(path))
    assert len(recs) == G.N_ITEMS, "archive size drift (crash-guard covers this)"
    note = ("EXP084-D1 class: archive carries no prompt strings/options/token "
            "IDs/margins — probe inputs rebuilt verbatim per EXP077 §3, fixed "
            f"indices 0..{G.N_ITEMS - 1}, by the execution-node backend; "
            "outcome-independent (EXP077 was a null; margins were never its "
            "endpoint).")
    return recs, note


def _l2norm(vec):
    return sum(float(x) * float(x) for x in vec) ** 0.5


def _dot(a, b):
    return sum(float(x) * float(y) for x, y in zip(a, b))


def run_full_loop(backend, budget, out_dir, log=print):
    """Backend-neutral Stage-B orchestration. Returns (results, verdict_tuple).

    Ordering (§6/§9 binding): Δθ snapshot -> baseline forwards -> headroom
    gate V2 -> per-item power iteration + n̂ + arms -> abort-frac V3 ->
    apparatus V4 -> contrasts -> Stage-2 gate -> Δθ verify V1 -> adjudicate.
    Every forward/backward-equivalent is budget-charged; the ceiling refuses.
    """
    G.crash_guard("stage-b", HERE)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    guard = G.FrozenBackboneGuard()

    records, deviation_note = load_probe_set(backend)
    log(f"[Stage B] probe set: {len(records)} records (sha pin verified).")
    log(f"[Stage B] DEVIATION NOTE: {deviation_note}")

    # Δθ=0 snapshot BEFORE any weight-touching phase (§6.6)
    state_dict = backend.load_state_dict_readonly()
    h0 = guard.snapshot_before(state_dict)
    log(f"[Stage B] state_dict sha256 (pre): {h0}")

    probes = [backend.build_probe(rec, i) for i, rec in enumerate(records)]

    # ---- baseline forwards (1 fwd each; correctness endpoint only) ----
    base_correct, base_logits, hs = [], [], []
    for i, probe in enumerate(probes):
        correct, logits, h = backend.baseline_forward(probe)
        budget.charge(1, f"baseline item {i}")
        base_correct.append(bool(correct))
        base_logits.append(list(logits))
        hs.append(h)
    n_wrong = sum(1 for c in base_correct if not c)
    log(f"[Stage B] baseline: {n_wrong}/{G.N_ITEMS} wrong-at-baseline")
    G.check_headroom(n_wrong)  # V2 (loud INVALID)

    # ---- per-item: power iteration -> n̂ -> arms ----
    items = []
    n_aborted = 0
    alphas = []          # |<v̂_1, n̂>| per non-aborted item (ĉ components)
    for i, probe in enumerate(probes):
        h = hs[i]
        pi = backend.power_iteration(probe, h)
        budget.charge(108, f"power-iteration item {i}")  # §11: 3x12x(1+2)
        s = pi["s"]
        v = pi["v"]
        aborted = G.should_abort_item(s[0], s[1])
        rec = {"i": i, "sigma": list(s), "aborted": aborted,
               "rayleigh": pi.get("rayleigh"), "n_iters": pi.get("n_iters")}
        if aborted:
            n_aborted += 1
            rec["arms"] = {}
        else:
            n_hat = backend.decision_normal_vjp(probe, h)
            budget.charge(2, f"decision-normal VJP item {i}")
            # sign rule §4 F2: v̂_r <- sign(<v̂_r, n̂>) v̂_r
            vs = []
            for r in range(3):
                sgn = 1.0 if _dot(v[r], n_hat) >= 0 else -1.0
                vs.append([sgn * float(x) for x in v[r]])
            alpha = abs(_dot(vs[0], n_hat))
            alphas.append(alpha)
            rec["alpha"] = alpha
            rec["arms"] = {}
            for k, eps_frac in enumerate(G.EPS_NORMS):
                for a, arm in enumerate(ARMS):
                    if arm == "vrand":
                        direction = f"vrand_{k}"  # per-item per-norm seed
                    else:
                        direction = arm
                    correct, logits = backend.inject_and_eval(
                        probe, h, direction, eps_frac)
                    budget.charge(1, f"arm {arm} norm {eps_frac} item {i}")
                    rec["arms"][(arm, k)] = {
                        "correct": bool(correct), "logits": list(logits)}
        # random arm is KEPT on aborted items (apparatus + primary control)
        if aborted:
            rec["arms"] = {}
            for k, eps_frac in enumerate(G.EPS_NORMS):
                correct, logits = backend.inject_and_eval(
                    probe, h, f"vrand_{k}", eps_frac)
                budget.charge(1, f"arm vrand norm {eps_frac} item {i} (aborted)")
                rec["arms"][("vrand", k)] = {
                    "correct": bool(correct), "logits": list(logits)}
        items.append(rec)
    log(f"[Stage B] power iteration done: {n_aborted}/{G.N_ITEMS} aborted "
        f"(σ̂₁/σ̂₂ < {G.SIGMA_RATIO_ABORT})")
    G.check_abort_frac(n_aborted)  # V3 (loud INVALID)

    # ---- apparatus check §6.5: random δ at 0.45||h|| moves ||Δz||₂ ----
    moved = 0
    for i, rec in enumerate(items):
        dz = [b - a for a, b in
              zip(base_logits[i], rec["arms"][("vrand", 1)]["logits"])]
        if _l2norm(dz) > G.APPARATUS_NOISE_FLOOR:
            moved += 1
    frac_moved = moved / G.N_ITEMS
    log(f"[Stage B] apparatus: {moved}/{G.N_ITEMS} items moved margins "
        f"({frac_moved:.3f} >= {G.APPARATUS_MIN_FRAC} required)")
    G.check_apparatus(frac_moved)  # V4 (loud INVALID)

    return finish_run(backend, budget, out_dir, items, probes, hs, alphas,
                      base_correct, deviation_note, h0, guard, log)

# ---------------------------------------------------------------------------
# Contrasts, Stage-2 gate, adjudication (continued)
# ---------------------------------------------------------------------------

def _paired_table(items, arm_a, arm_b, norm_k=0):
    """Paired correctness table for arm-pair (A, B) at norm index norm_k.

    Returns (n10, n01, n00, n11) over items where BOTH arms are present
    (aborted items have no direction arms; pairwise deletion on the
    pre-treatment convergence covariate — non-gameable, EXP084-D3 class).
    n10 = #{A right, B wrong}; n01 = #{A wrong, B right}.
    """
    n10 = n01 = n00 = n11 = 0
    n_used = 0
    for rec in items:
        arms = rec["arms"]
        if (arm_a, norm_k) not in arms or (arm_b, norm_k) not in arms:
            continue
        a = arms[(arm_a, norm_k)]["correct"]
        b = arms[(arm_b, norm_k)]["correct"]
        n_used += 1
        if a and not b:
            n10 += 1
        elif b and not a:
            n01 += 1
        elif a and b:
            n11 += 1
        else:
            n00 += 1
    return (n10, n01, n00, n11), n_used


def finish_run(backend, budget, out_dir, items, probes, hs, alphas, base_correct,
               deviation_note, h0, guard, log=print):
    """Contrasts -> Stage-2 gate -> Δθ verify -> adjudicate -> artifacts."""
    t0 = time.time()

    # ---- primary contrast: v̂_1 vs v̂_rand at norm 0.15 (§7) ----
    (n10, n01, n00, n11), n_pri = _paired_table(items, "v1", "vrand", 0)
    delta_point = (n10 - n01) / (n10 + n01 + n00 + n11)
    mcnemar_p = S.mcnemar_exact_one_sided(n10, n01)
    delta_lci, delta_uci = S.tango_ci(n10, n01, n00, n11)
    log(f"[Stage B] primary Δ=v̂_1−v̂_rand @0.15: n=({n10},{n01},{n00},{n11}) "
        f"n_used={n_pri}, Δ̂={delta_point:+.4f}, "
        f"Tango95=({delta_lci:+.4f},{delta_uci:+.4f}), McNemar p={mcnemar_p:.4g}")

    # ---- rank contrast: v̂_1 vs v̂_3 at norm 0.15 (§7 discriminating) ----
    (r10, r01, r00, r11), n_rank = _paired_table(items, "v1", "v3", 0)
    rank_point = (r10 - r01) / (r10 + r01 + r00 + r11)
    rank_lci, rank_uci = S.tango_ci(r10, r01, r00, r11)
    log(f"[Stage B] rank Δ_rank=v̂_1−v̂_3 @0.15: Δ̂={rank_point:+.4f}, "
        f"Tango95=({rank_lci:+.4f},{rank_uci:+.4f})")

    # ---- rank-test validity: median_i(σ̂_1/σ̂_3) >= 1.2 (§6.4) ----
    ratios = [rec["sigma"][0] / rec["sigma"][2] for rec in items
              if not rec["aborted"] and rec["sigma"][2] > 0]
    ratios.sort()
    med_ratio = ratios[len(ratios) // 2] if ratios else 0.0
    rank_valid = med_ratio >= G.SIGMA_RATIO_RANK_VALID
    log(f"[Stage B] rank validity: median(σ̂_1/σ̂_3)={med_ratio:.3f} "
        f"(need ≥ {G.SIGMA_RATIO_RANK_VALID}) -> "
        f"{'DEFINED' if rank_valid else 'UNDEFINED → HELD (V11)'}")

    # ---- ĉ kill-first diagnostic (§2 D6, §7) ----
    chat = S.c_hat(alphas)
    exc = S.exceedance(alphas)
    log(f"[Stage B] ĉ={chat:.4f} (bar {G.CHAT_BAR}), "
        f"E={exc:.3f} (bar {G.EXCEEDANCE_BAR:.0%})")

    # ---- signed ledger (§7 P3): per-arm (b, c) vs baseline @0.15 ----
    ledgers = {}
    for arm in ARMS:
        arm_corr = [rec["arms"][(arm, 0)]["correct"] for rec in items
                    if (arm, 0) in rec["arms"]]
        base_sub = [c for rec, c in zip(items, base_correct)
                    if (arm, 0) in rec["arms"]]
        led = S.signed_ledger(base_sub, arm_corr)
        ledgers[arm] = led
        log(f"[Stage B] ledger {arm}@0.15: b={led['b_wrong_to_right']} "
            f"c={led['c_right_to_wrong']} anti-steerable="
            f"{led['anti_steerable_frac']}"
            f"{' FLAGGED' if led['flagged'] else ''}")

    # ---- Stage-2 gate (S4 F10, G3): runs IFF the primary win fires ----
    primary_win = (delta_lci > G.DELTA_MIN) and (mcnemar_p <= G.MCNEMAR_ALPHA)
    stage2_ran = False
    delta_perm_lci = delta_perm_uci = None
    n_perm_used = 0
    if primary_win:
        log("[Stage B] primary win fired -> running Stage-2 permuted arm")
        delta_perm_lci, delta_perm_uci, n_perm_used = run_stage2(
            backend, budget, items, probes, hs, log)
        stage2_ran = True

    # ---- Dtheta = 0 verification (S6.6) -> INVALID V1 on mismatch ----
    state_dict = backend.load_state_dict_readonly()
    h1 = guard.verify_after(state_dict)
    log("[Stage B] state_dict sha256 (post): %s  (Dtheta=0 verified)" % h1)

    results = {
        "delta_theta_ok": True,
        "n_wrong_baseline": sum(1 for c in base_correct if not c),
        "n_items": G.N_ITEMS,
        "frac_aborted": sum(1 for rec in items if rec["aborted"]) / G.N_ITEMS,
        "apparatus_ok": True,  # checked loudly mid-loop (V4); True = passed
        "c_hat": chat,
        "exceedance": exc,
        "delta_lci": delta_lci, "delta_uci": delta_uci,
        "delta_point": delta_point, "mcnemar_p": mcnemar_p,
        "rank_valid": rank_valid,
        "delta_rank_lci": rank_lci, "delta_rank_uci": rank_uci,
        "delta_rank_point": rank_point,
        "stage2_ran": stage2_ran,
        "delta_perm_lci": delta_perm_lci,
        "delta_perm_uci": delta_perm_uci,
        "n_primary_used": n_pri, "n_rank_used": n_rank,
        "n_perm_used": n_perm_used,
        "median_sigma1_sigma3": med_ratio,
        "ledgers": ledgers,
        "passes_used": budget.used,
        "passes_budget": budget.limit,
    }
    verdict, evidentiary, detail = V.adjudicate(results)
    log("[Stage B] VERDICT: %s (%s) -- %s" % (verdict, evidentiary, detail))

    record = {
        "experiment": "EXP086",
        "mode": "stage-b",
        "env": env_manifest({"probe_deviation_note": deviation_note}),
        "param_hash_pre": h0,
        "param_hash_post": h1,
        "delta_theta_zero": True,
        "results": results,
        "verdict": verdict,
        "evidentiary": evidentiary,
        "detail": detail,
        "wall_seconds": time.time() - t0,
        # raw per-item logs (Law #13); tuple arm keys -> "arm@norm" strings
        # because JSON object keys must be strings.
        "items": [
            {k: ({f"{a}@{n}": v for (a, n), v in rec["arms"].items()}
                 if k == "arms" else v)
             for k, v in rec.items()}
            for rec in items
        ],
    }
    atomic_write_json(os.path.join(out_dir, "exp086_stage_b_record.json"), record)
    return results, (verdict, evidentiary, detail)


def run_stage2(backend, budget, items, probes, hs, log=print):
    """Stage-2 conditional arm (§4 F10): permuted-v̂_1 at both norms.

    Item j's v̂_1 injected on item i (j = fixed derangement, seeded), both
    norms, paired per item vs v̂_1. Costs 120 fwd-equiv (§11).
    Returns (delta_perm_lci, delta_perm_uci, n_perm_used).
    """
    der = backend.stage2_derangement(len(items))
    p10 = p01 = p00 = p11 = 0
    n_perm_used = 0
    for k, eps_frac in enumerate(G.EPS_NORMS):
        for i, rec in enumerate(items):
            if rec["aborted"] or ("v1", k) not in rec["arms"]:
                continue
            j = der[i]
            # direction tag ("permuted", donor j, norm k):
            # the backend injects item j's v1 direction on item i
            correct, _ = backend.inject_and_eval(
                probes[i], hs[i], ("permuted", j, k), eps_frac)
            budget.charge(1, f"stage-2 permuted norm {eps_frac} item {i}")
            if k == 0:  # Δ_perm evaluated at the primary norm
                a = rec["arms"][("v1", 0)]["correct"]
                b = bool(correct)
                n_perm_used += 1
                if a and not b:
                    p10 += 1
                elif b and not a:
                    p01 += 1
                elif a and b:
                    p11 += 1
                else:
                    p00 += 1
    lci, uci = S.tango_ci(p10, p01, p00, p11)
    log(f"[Stage B] Stage-2 Δ_perm=v̂_1−permuted @0.15: n=({p10},{p01},{p00},"
        f"{p11}) Tango95=({lci:+.4f},{uci:+.4f})")
    return lci, uci, n_perm_used

# ---------------------------------------------------------------------------
# CLI: --smoke / --stage-a / --run (all gated; refusals exit 2)
# ---------------------------------------------------------------------------

def cmd_smoke():
    """0 model passes: import the smoke module and run it in-process."""
    sys.path.insert(0, HERE)
    import smoke_test
    ok = smoke_test.main()
    return 0 if ok else 1


def cmd_stage_a(args):
    if not args.bundle_review_signoff:
        print("REFUSED (exit 2): --stage-a requires --bundle-review-signoff "
              "(independent Law #14 bundle review). Weight access happens "
              "only after that review. No weights touched.", file=sys.stderr)
        return 2
    # The execution-node backend is chosen here; on the build machine there
    # is no weights path and no torch, so this raises loudly by design.
    if not args.weights:
        print("REFUSED (exit 2): --stage-a requires --weights <path> "
              "(read-only local snapshot).", file=sys.stderr)
        return 2
    backend = TorchBackend(args.weights)
    budget = G.PassBudget()  # Stage A is $0 CPU; budget unused but constructed
    report = run_stage_a(backend, args.out, log=print)
    print(f"Stage A complete: {args.out}/exp086_stage_a_report.json "
          f"(advisory only; verdict={report['verdict']})")
    return 0


def cmd_run(args):
    if not (args.ceo_gpu_clearance and args.stage2_review_signoff):
        print("REFUSED (exit 2): --run requires BOTH --ceo-gpu-clearance AND "
              "--stage2-review-signoff. GPU execution is NOT licensed "
              "(signed §15; queue behind K2 -> EXP083 -> EXP084).",
              file=sys.stderr)
        return 2
    backend = TorchBackend(args.weights or G.MODEL_ID)
    budget = G.PassBudget()
    results, (verdict, evidentiary, detail) = run_full_loop(
        backend, budget, args.out, log=print)
    print(f"Stage B complete: verdict={verdict} ({evidentiary})")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="EXP086 R3 dynamical-amplifier runner (gated; see --help)")
    ap.add_argument("--smoke", action="store_true",
                    help="startup smoke test (0 model passes)")
    ap.add_argument("--stage-a", action="store_true",
                    help="Stage A advisory weight-only screen")
    ap.add_argument("--run", action="store_true",
                    help="Stage B pilot (execution node; NOT licensed)")
    ap.add_argument("--out", default=os.path.join(HERE, "out"),
                    help="output directory for run artifacts")
    ap.add_argument("--weights", default=None,
                    help="read-only local weights snapshot path")
    ap.add_argument("--bundle-review-signoff", action="store_true",
                    help="independent Law #14 bundle review SIGN (Stage A gate)")
    ap.add_argument("--ceo-gpu-clearance", action="store_true",
                    help="CEO GPU clearance (Stage B gate)")
    ap.add_argument("--stage2-review-signoff", action="store_true",
                    help="Law #14 stage-2 review signoff (Stage B gate)")
    args = ap.parse_args(argv)
    if args.smoke:
        return cmd_smoke()
    if args.stage_a:
        return cmd_stage_a(args)
    if args.run:
        return cmd_run(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
