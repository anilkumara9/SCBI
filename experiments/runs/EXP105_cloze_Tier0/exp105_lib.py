# exp105_lib.py — EXP105 cloze Tier-0 shared machinery.
# The rank / top-1 / masking / McNemar / bar-order code exercised by
# unit_tests_exp105.py is the SAME code imported by run_tier0_exp105.py,
# so the tested machinery is the run machinery (no drift).
import math
import statistics

MASK_LOGIT = -1e9
K = 8


def correct_rank(logits8, correct_idx, token_ids8):
    """Rank (1..8) of the correct candidate by logit desc; float32-exact
    equality ties broken by ASCENDING token id (S4-8' v2 sec 3).
    logits8 are Python floats converted from float32 model logits;
    exact float32 equality is preserved by the widening conversion."""
    assert len(logits8) == K and len(token_ids8) == K
    order = sorted(range(K), key=lambda j: (-logits8[j], token_ids8[j]))
    return order.index(correct_idx) + 1


def top1_decision(logits8, token_ids8):
    """Argmax over the 8 candidate logits with ascending-token-id tie-break."""
    assert len(logits8) == K and len(token_ids8) == K
    return max(range(K), key=lambda j: (logits8[j], -token_ids8[j]))


def masked_argmax(logits8, mask_idx, token_ids8):
    """Mask one candidate (-1e9) and re-argmax (battery machinery)."""
    masked = list(logits8)
    masked[mask_idx] = MASK_LOGIT
    return top1_decision(masked, token_ids8)


def mcnemar_exact(b, c):
    """Two-sided exact McNemar p = 2 * P(Bin(b+c, 0.5) <= min(b,c)), capped at 1.0.
    Pre-reg feasibility anchors: b=6,c=0 -> 2/64 = 0.03125; b=5,c=0 -> 2/32 = 0.0625.
    b=c=0 -> 1.0 (valid null, not an error)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2.0 * tail)


def token_id_rank_of_correct(correct_idx, token_ids8):
    """Descriptive diagnostic (v2 sec 9 item 3): rank of the correct candidate's
    token id among the 8 candidate token ids, ascending. Expect ~uniform 1..8."""
    ordered = sorted(range(K), key=lambda j: token_ids8[j])
    return ordered.index(correct_idx) + 1


def tier0_verdict(baseline_acc, failed_ranks, tie_rate):
    """Binding bar order (S4-8' v2 sec 4 + lane brief):
    1. baseline < 0.25        -> LINE-CLOSED
    2. empty failed set       -> KILL (premise vacuous, sec 5(e))
    3. median failed rank > 5 -> KILL (premise)
    4. n_pop < 12             -> UNDERDETERMINED
    5. baseline > 0.75 or tie-guard > 0.25 -> HOLD
    6. else                   -> TIER-0 PASSED
    n_pop = #{failed items with correct_rank <= 5} (suppressible population,
    carried over from EXP104's tier0pop definition)."""
    if baseline_acc < 0.25:
        return "LINE-CLOSED"
    if len(failed_ranks) == 0:
        return "KILL"
    med = statistics.median(failed_ranks)
    if med > 5:
        return "KILL"
    n_pop = sum(1 for r in failed_ranks if r <= 5)
    if n_pop < 12:
        return "UNDERDETERMINED"
    if baseline_acc > 0.75 or tie_rate > 0.25:
        return "HOLD"
    return "TIER-0 PASSED"
