#!/usr/bin/env python3
"""EXP105 intervention battery (S4-8' cloze) — LOG-4491.

Applies the pre-registered battery arms B/T/F/R (S4-8 v3 §2.3 carried over
verbatim, instantiated for cloze) to the recorded Tier-0 8-candidate logit
vectors. Masking is a logit-level operator (-1e9 before argmax); no model
contact is needed or performed. $0 CPU. Deterministic.

Pre-registered facts used (from S4-8 v3, SIGNED at LOG-4480, carried over in
S4-8' v2, SIGNED at LOG-4488):
- Arms: B none; T mask baseline top-1 token; F mask structural foil token;
  R mask uniformly random candidate among k-2 excluding baseline top-1 AND
  the correct option, seed pinned.
- Primary population: Tier-0 population = failed items with correct-rank <= 5.
- Primary contrasts on Tier-0 pop; full-bench secondary.
- Primary binding test: T-vs-R McNemar-exact at ALPHA=0.05.
  Other contrasts at Bonferroni alpha=0.0125, descriptive.
- DELTA_BAR = 0.10; flat band |dM| < 0.05.
- Tango 95% CIs on paired differences.
- Overlap O = (# Tier-0-pop items where foil token == baseline top-1 token)/n_pop.
- Tie-break: float32 exact-equality ties broken by ascending token id.
"""
import json, math, random, hashlib, os, sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
T0_DIR = os.path.abspath(os.path.join(HERE, '..', 'EXP105_cloze_Tier0'))
R_SEED = 20260928  # pinned BEFORE any battery computation (2026-09-28)

MASK = -1e9


def load_json(path):
    with open(path) as f:
        return json.load(f)


def argmax_tiebreak(logits, token_ids, masked=None):
    """Argmax over candidates with ascending-token-id tie-break on exact ties."""
    best = None
    for i, (lg, tid) in enumerate(zip(logits, token_ids)):
        if masked is not None and i == masked:
            continue
        key = (-lg, tid)
        if best is None or key < best[0]:
            best = (key, i)
    return best[1]


def mcnemar_exact(b, c):
    """Two-sided exact McNemar p-value (binomial). b/c grid cross-checked in unit test (f)."""
    n = b + c
    if n == 0:
        return 1.0
    m = min(b, c)
    s = sum(math.comb(n, k) for k in range(m + 1))
    return min(1.0, 2.0 * s / 2.0 ** n)


def tango_ci(b, c, d, alpha=0.05):
    """Tango (1998) score CI for paired difference delta=(b-c)/n, 95%."""
    from scipy.stats import chi2
    z2 = chi2.ppf(1 - alpha, 1)
    try:
        return _tango_interval(float(b), float(c), float(d), z2)
    except Exception:
        return _newcombe_interval(b, c, d, alpha)


def _tango_interval(b, c, d, z2):
    """Tango (1998) score CI for paired difference delta=(b-c)/n.

    Constrained MLE of theta=(p12+p21)/2 under H0: p12-p21=delta is found by
    direct bounded maximization of the (concave) log-likelihood, which handles
    boundary cases (b=0 or c=0) correctly via the 0*log0:=0 convention.
    The score statistic X^2(delta) is U-shaped; CI = {delta: X^2 <= z2}.
    """
    from scipy.optimize import brentq, minimize_scalar
    n = b + c + d
    if n == 0:
        return (0.0, 0.0)

    def term(k, p):
        if k == 0:
            return 0.0  # 0*log0 := 0; boundary p=0 allowed
        if p <= 0:
            return float('inf')
        return k * math.log(p)

    def constrained_theta(delta):
        lo = abs(delta) / 2.0
        hi = min(0.5, 1.0 - abs(delta) / 2.0)
        if hi <= lo:
            return None

        def nll(theta):
            p12 = theta + delta / 2.0
            p21 = theta - delta / 2.0
            prem = 1.0 - 2.0 * theta
            if p12 < 0 or p21 < 0 or prem < 0:
                return 1e18
            return -(term(b, p12) + term(c, p21) + term(d, prem))

        r = minimize_scalar(nll, bounds=(lo, hi), method='bounded',
                            options={'xatol': 1e-14})
        return r.x

    def t_stat(delta):
        th = constrained_theta(delta)
        if th is None:
            return 1e12
        p12 = th + delta / 2.0
        p21 = th - delta / 2.0
        prem = 1.0 - 2.0 * th
        xs = 0.0
        for k, p in ((b, p12), (c, p21), (d, prem)):
            e = n * p
            xs += (k - e) ** 2 / e if e > 0 else (0.0 if k == 0 else 1e12)
        return xs

    delta_hat = (b - c) / n

    def f(x):
        return t_stat(x) - z2

    flo, fhat, fhi = f(-1.0), f(delta_hat), f(1.0)
    if fhat >= 0:
        # degenerate: statistic non-negative even at the MLE (shouldn't happen)
        return (max(-1.0, delta_hat), min(1.0, delta_hat))
    lo = brentq(f, -1.0, delta_hat) if flo * fhat < 0 else -1.0
    hi = brentq(f, delta_hat, 1.0) if fhat * fhi < 0 else 1.0
    return (max(-1.0, lo), min(1.0, hi))


def _newcombe_interval(b, c, d, alpha=0.05):
    # Fallback (should rarely trigger): Wald interval with correct paired var.
    from scipy.stats import norm
    n = b + c + d
    if n == 0:
        return (0.0, 0.0)
    z = norm.ppf(1 - alpha / 2)
    phat = (b - c) / n
    var = ((b + c) - (b - c) ** 2 / n) / n ** 2
    se = math.sqrt(max(var, 0.0))
    return (max(-1.0, phat - z * se), min(1.0, phat + z * se))


def main():
    rng = random.Random(R_SEED)
    recs = load_json(os.path.join(T0_DIR, 'per_item_records.json'))
    manifest = load_json(os.path.join(T0_DIR, 'cloze_bench_manifest.json'))
    items = {m['item_id']: m for m in manifest['items']}
    assert len(recs) == 60, f"expected 60 Tier-0 records, got {len(recs)}"

    # --- Tier-0 population (pre-registered): failed AND correct_rank <= 5 ---
    pop, bench = [], []
    for r in recs:
        logits = r['candidate_logits']
        tids = items[r['item_id']]['option_token_ids']
        # sanity: recompute B arm from logits; must match recorded top1
        b_idx = argmax_tiebreak(logits, tids)
        assert b_idx == r['top1_idx'], f"B-arm recompute mismatch on {r['item_id']}"
        failed = not r['correct_is_top1']
        bench.append(r)
        if failed and r['correct_rank'] <= 5:
            pop.append(r)
    n_pop = len(pop)
    n_failed = sum(1 for r in recs if not r['correct_is_top1'])
    print(f"n_items=60 n_failed={n_failed} n_pop={n_pop}")

    # --- N_pop feasibility computation (EXP079 lesson, recorded on paper) ---
    # McNemar-exact minimum: b=6,c=0 -> p=2/64=0.03125 (<0.05); b=5,c=0 -> p=0.0625 (n.s.)
    feas = {'n_pop': n_pop, 'b6_c0_p': mcnemar_exact(6, 0),
            'b5_c0_p': mcnemar_exact(5, 0),
            'max_achievable_dM': 1.0, 'delta_bar': 0.10,
            'note': 'max achievable dM=1.0 >= DELTA_BAR=0.10; n_pop>=12 gate IS this computation.'}
    print('feasibility:', feas)

    batt = []  # per-item battery records
    overlap_hits = 0
    for r in recs:
        iid = r['item_id']
        logits = r['candidate_logits']
        tids = items[iid]['option_token_ids']
        opts = items[iid]['options']
        correct_opt = items[iid]['correct_option']
        correct_idx = opts.index(correct_opt)
        foil_opt = items[iid]['structural_foil']
        foil_idx = opts.index(foil_opt)
        top1_idx = r['top1_idx']

        arms = {}
        # B: none
        b_top = argmax_tiebreak(logits, tids)
        arms['B'] = b_top
        # T: mask baseline top-1
        arms['T'] = argmax_tiebreak(logits, tids, masked=top1_idx)
        # F: mask structural foil
        arms['F'] = argmax_tiebreak(logits, tids, masked=foil_idx)
        # R: uniform random among candidates excluding baseline top-1 AND correct
        eligible = [i for i in range(8) if i != top1_idx and i != correct_idx]
        r_mask = rng.choice(eligible)
        arms['R'] = argmax_tiebreak(logits, tids, masked=r_mask)

        dec = {a: (idx == correct_idx) for a, idx in arms.items()}
        batt.append({
            'item_id': iid, 'correct_idx': correct_idx,
            'top1_idx': top1_idx, 'foil_idx': foil_idx, 'r_mask_idx': r_mask,
            'masked_idx_per_arm': {'B': None, 'T': top1_idx, 'F': foil_idx, 'R': r_mask},
            'arms_top_idx': arms,
            'arms_correct': dec,
            'in_tier0_pop': r in pop,
            'foil_is_top1': (tids[foil_idx] == tids[top1_idx]),
        })
        if r in pop and tids[foil_idx] == tids[top1_idx]:
            overlap_hits += 1

    O = overlap_hits / n_pop if n_pop else float('nan')
    print(f"foil-top1 overlap O = {overlap_hits}/{n_pop} = {O:.4f}")

    pop_rec = [b for b in batt if b['in_tier0_pop']]

    def dM(arm, popset):
        return sum(b['arms_correct'][arm] - b['arms_correct']['B'] for b in popset) / len(popset)

    dM_T_pop, dM_F_pop, dM_R_pop = dM('T', pop_rec), dM('F', pop_rec), dM('R', pop_rec)
    dM_T_full, dM_F_full, dM_R_full = dM('T', batt), dM('F', batt), dM('R', batt)

    def mcnemar_pair(armX, armY, popset):
        b = sum(1 for r in popset if r['arms_correct'][armX] and not r['arms_correct'][armY])
        c = sum(1 for r in popset if not r['arms_correct'][armX] and r['arms_correct'][armY])
        dd = len(popset) - b - c
        return {'b': b, 'c': c, 'p': mcnemar_exact(b, c), 'tango95': tango_ci(b, c, dd)}

    contrasts = {
        'T-vs-B': mcnemar_pair('T', 'B', pop_rec),
        'F-vs-B': mcnemar_pair('F', 'B', pop_rec),
        'R-vs-B': mcnemar_pair('R', 'B', pop_rec),
        'T-vs-R': mcnemar_pair('T', 'R', pop_rec),  # PRIMARY BINDING at ALPHA=0.05
        'T-vs-F': mcnemar_pair('T', 'F', pop_rec),
    }

    # --- Decision table (v3 §3, first-match order; S4-8' sanity-split amendment) ---
    verdict, step = None, None
    evidence = {}
    # Steps 1-5 already adjudicated at Tier-0 (G1 PASS, median rank 4.0<=5,
    # n_pop=21>=12, baseline 0.5333 in band, tie rate 0.0<=0.25) — carried.
    p_TR = contrasts['T-vs-R']['p']
    p_FB = contrasts['F-vs-B']['p']
    ev6 = (dM_T_pop <= 0) and (dM_F_pop > 0) and (p_FB < 0.0125)
    ev7 = (dM_T_pop > 0.10) and (p_TR < 0.05) and (abs(dM_R_pop) < 0.05)
    ev8 = (not ev7) and (dM_F_pop > 0) and (p_FB < 0.0125) and (O <= 0.5)
    ev9 = (dM_T_pop > 0) and (p_TR >= 0.05)
    ev10 = all(abs(x) < 0.05 for x in (dM_T_pop, dM_F_pop, dM_R_pop))
    evidence = {'step6_cond': ev6, 'step7_cond': ev7, 'step8_cond': ev8,
                'step9_cond': ev9, 'step10_cond': ev10, 'O': O, 'O_le_0.5': O <= 0.5}
    if ev6:
        verdict, step = 'PIVOT', 6
    elif ev7:
        verdict, step = 'CONTINUE', 7
    elif ev8:
        verdict, step = 'PIVOT', 8
    elif ev9:
        verdict, step = 'KILL', 9
    elif ev10:
        verdict, step = 'KILL', 10
    else:
        verdict, step = 'PIVOT', 11

    n_rescued_T = sum(1 for r in pop_rec if r['arms_correct']['T'] and not r['arms_correct']['B'])
    n_rescued_F = sum(1 for r in pop_rec if r['arms_correct']['F'] and not r['arms_correct']['B'])
    n_rescued_R = sum(1 for r in pop_rec if r['arms_correct']['R'] and not r['arms_correct']['B'])

    worksheet = {
        'experiment': 'EXP105', 'phase': 'battery', 'format': 'cloze',
        'log': 'LOG-4491', 'r_seed': R_SEED,
        'n_items': 60, 'n_pop': n_pop, 'overlap_O': O,
        'dM_primary_tier0pop': {'T': dM_T_pop, 'F': dM_F_pop, 'R': dM_R_pop},
        'dM_secondary_fullbench': {'T': dM_T_full, 'F': dM_F_full, 'R': dM_R_full},
        'rescues_on_pop': {'T': n_rescued_T, 'F': n_rescued_F, 'R': n_rescued_R},
        'contrasts': contrasts,
        'feasibility': feas,
        'decision': {'verdict': verdict, 'step': step, 'evidence': evidence},
        'guards': {'model_contact': 'none — battery is a logit-level operator on recorded Tier-0 logits; delta_theta=0 by construction',
                   'bars': 'DELTA_BAR=0.10, flat band |dM|<0.05, primary T-vs-R alpha=0.05, others Bonferroni 0.0125'},
    }
    with open(os.path.join(HERE, 'battery_worksheet_exp105.json'), 'w') as f:
        json.dump(worksheet, f, indent=1)
    with open(os.path.join(HERE, 'per_item_records_battery.json'), 'w') as f:
        json.dump(batt, f, indent=1)

    import csv
    with open(os.path.join(HERE, 'per_item_records_battery.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['item_id', 'arm', 'top1_correct', 'masked_idx', 'in_tier0_pop'])
        for b in batt:
            for a in ('B', 'T', 'F', 'R'):
                mi = b['masked_idx_per_arm'][a]
                w.writerow([b['item_id'], a, int(b['arms_correct'][a]),
                            '' if mi is None else mi, int(b['in_tier0_pop'])])

    print(json.dumps({'dM_pop': worksheet['dM_primary_tier0pop'],
                      'contrasts_p': {k: v['p'] for k, v in contrasts.items()},
                      'rescues': worksheet['rescues_on_pop'],
                      'verdict': verdict, 'step': step}, indent=1))
    return worksheet


if __name__ == '__main__':
    ws = main()
    print('BATTERY VERDICT:', ws['decision']['verdict'], 'step', ws['decision']['step'])
