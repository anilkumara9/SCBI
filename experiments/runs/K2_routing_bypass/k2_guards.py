"""K2 routing-vs-bypass — guard predicates (REV2 §4).

Pure standard library. CPU. Deterministic. Every guard in REV2 §4 is
represented here as a testable predicate; run_k2.py wires them to the
live execution. Guard numbering follows REV2 exactly (G1..G10).

Mapping to the dispatch shorthand: the dispatch's "G5 no-unlicensed-
forward-pass" is REV2 G4; the dispatch's "(c)-gate b_c >= 6 FATAL" is
REV2 G5. REV2 numbering is binding in this bundle.
"""

# Pre-registered constants (REV2 §3.4/§3.5/§4).
N_ITEMS = 60
N_ARMS = 3
PASSES_PER_PIN = N_ITEMS * N_ARMS      # 180; G4 binds to 3 * N_actual
C_GATE_MDE_B = 6                      # REV2 §3.5: L1 MDE at c=0
G1_INVALID_FAILURES = 3               # REV2 G1: >=3 item failures -> INVALID
G10_EXCLUSION_FLOOR = 6               # REV2 F2: >6 exclusions -> Underdetermined
NORM_REL_TOL = 1e-5                   # REV2 G1(b)
DELTA_MIN = 0.05


def g1_norm_check(rebuilt_norms, logged_norms, tol=NORM_REL_TOL):
    """REV2 G1(b): per-item ||b_K2|| vs run-logged C8 norms, rel err <= tol.

    Returns (ok, per_item) with per-item (rel_err, passed). The plan's
    honesty caveat stands: this is a WEAK identity check (any unit*alpha
    vector passes); the honest license is deterministic-reconstruction +
    the live (c)-gate (G5).
    """
    if len(rebuilt_norms) != len(logged_norms):
        return False, []
    per_item = []
    ok = True
    for rn, ln in zip(rebuilt_norms, logged_norms):
        if ln == 0:
            rel = float("inf") if rn != 0 else 0.0
        else:
            rel = abs(rn - ln) / abs(ln)
        passed = rel <= tol
        per_item.append({"rel_err": rel, "passed": bool(passed)})
        ok = ok and passed
    return ok, per_item


def g1_invalid_check(n_item_failures, threshold=G1_INVALID_FAILURES):
    """REV2 G1: >=3 item failures -> run INVALID."""
    return n_item_failures >= threshold


def g4_pass_count_check(n_passes, n_actual_items, n_arms=N_ARMS):
    """REV2 G4: exactly 3 * N_actual forward passes (180 at full N).

    N_actual = 60 - exclusions per the G10 floor; the binding requirement
    is exact equality with the licensed count — no unlicensed passes,
    no missing passes.
    """
    expected = n_arms * n_actual_items
    return n_passes == expected, expected


def g5_c_gate_check(b_c, mde_b=C_GATE_MDE_B):
    """REV2 G5: b_c >= 6 (L1 MDE) else INVALID -> Underdetermined.

    Non-vacuous: the gate checks the K2 runner's LIVE (c) arm against the
    L1 MDE floor (deliberately below the b=14 smoke anchor) — it tests
    implementation integrity (hook site, vector identity G1, position
    masks) and current benchmark headroom, not anchor reproduction.
    """
    return b_c >= mde_b


def g10_exclusion_floor_check(exclusions, floor=G10_EXCLUSION_FLOOR):
    """REV2 G10/F2: >6 exclusions (>10%) -> run is Underdetermined.

    At <=6 exclusions the run proceeds at the actual N; every exclusion
    is recorded with cause, never silently dropped.
    """
    n = len(exclusions)
    if n > floor:
        return ("Underdetermined",
                "exclusion floor breached: %d exclusions (>%d); run is "
                "Underdetermined with cause; fix cause, re-run under a new LOG." % (n, floor))
    return ("proceed", "exclusions=%d (<=%d); bars apply at actual N=%d."
            % (n, floor, N_ITEMS - n))


def gate_a_evaluate(byte_identity_ok, norm_match_ok, tokenizer_logged):
    """LOG-224c Ruling 7 — pre-execution gate A (CPU identity dry run).

    (i) two independent CPU rebuilds of per-item b_K2 byte-identical;
    (ii) norms match run-logged C8 norms <= 1e-5;
    (iii) tokenizer checksum + HF revision logged.
    Failure blocks GPU clearance WITH CAUSE. Honest form: rebuild-vs-
    rebuild byte-identity + norm-compare vs run-logged norms — never
    "byte-compare vs archive" (no per-item archive exists).
    """
    causes = []
    if not byte_identity_ok:
        causes.append("byte-identity FAILED: the two independent CPU rebuilds "
                      "of per-item b_K2 are not byte-identical")
    if not norm_match_ok:
        causes.append("norm-compare FAILED: rebuilt per-item norms do not match "
                      "the run-logged C8 norms within 1e-5 relative error")
    if not tokenizer_logged:
        causes.append("tokenizer pin FAILED: checksum + HF revision not logged "
                      "at vector-build time")
    if causes:
        return ("FAIL", "pre-execution gate A FAILED — GPU clearance BLOCKED with cause: "
                + " | ".join(causes))
    return ("PASS", "pre-execution gate A PASSED: byte-identical rebuilds, norms match, "
            "tokenizer pin logged")


def checklist_b_record(tokenizer_checksum, hf_revision):
    """LOG-224c Ruling 6 — pre-execution checklist B (tokenizer pin).

    Log sha256 of the resolved tokenizer payload as loaded + the exact HF
    commit SHA at vector-build time. A missing log is a RECORDED DEVIATION
    on the pre-execution checklist, NOT an INVALID.
    """
    if tokenizer_checksum and hf_revision:
        return {"status": "complete",
                "tokenizer_sha256": tokenizer_checksum,
                "hf_revision": hf_revision,
                "note": "Ruling 6 satisfied: checksum + revision logged at vector-build time."}
    return {"status": "deviation_recorded",
            "tokenizer_sha256": tokenizer_checksum,
            "hf_revision": hf_revision,
            "note": ("Ruling 6 DEVIATION (recorded, NOT an INVALID): tokenizer checksum and/or "
                     "HF revision missing at vector-build time. Construction-identity's weakest "
                     "pin is unverified for this run; the deviation is disclosed, not hidden.")}


def g3_delta_theta_check(pre_hash, post_hash):
    """REV2 G3: sha256(state_dict) pre-run == post-run; mismatch -> FATAL."""
    match = (pre_hash == post_hash) and bool(pre_hash)
    return match, ("Δθ=0 holds (pre==post)" if match
                   else "FATAL: pre/post parameter hash mismatch — frozen-backbone "
                        "violation (AGENTS.md Law #6); results are NOT reported.")


def guards_evaluate(record):
    """Row-5 pre-adjudication: any FATAL guard failed / records missing.

    `record` carries the guard outcomes from the run. Returns
    (underdetermined: bool, cause: str). Called BEFORE adjudicate_verdict.
    """
    fatal = []
    if not record.get("g3_pre_post_match", False):
        fatal.append("G3 Δθ=0 violated (pre/post hash mismatch)")
    if not record.get("g4_pass_count_ok", False):
        fatal.append("G4 pass-count violated (expected %s, got %s)"
                     % (record.get("g4_expected"), record.get("g4_got")))
    if record.get("g1_invalid", False):
        fatal.append("G1 INVALID (>=3 per-item identity failures)")
    if not record.get("g5_c_gate_passed", True):
        fatal.append("G5 (c)-gate failed (b_c=%s < %s)"
                     % (record.get("b_c"), C_GATE_MDE_B))
    if record.get("records_missing", False):
        fatal.append("records missing")
    floor_status, floor_msg = g10_exclusion_floor_check(record.get("exclusions", []))
    if floor_status == "Underdetermined":
        fatal.append("G10: " + floor_msg)
    if fatal:
        return True, "Underdetermined — FATAL guard(s): " + " | ".join(fatal)
    return False, "no FATAL guard failures; " + floor_msg
