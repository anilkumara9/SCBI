"""EXP107 (template-control kill-test of EXP106) — execution lane LOG-4540.
CEO launch: LOG-4539. Pre-reg: research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md
(SIGN via LOG-4536/4537/4538). Read-only on signed protocols and paper sources.

Pinned spec (verbatim from pre-reg + EXP106 executor):
- Bench: build_exp107_bench.py; registered pin e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5
- Train artifacts reused from EXP106: exp106_train_embeddings.npz
  embeddings-array sha256 4e6229bea083570f17e3368326d9848c9a8db5dc25c7efc75f0e1a2960b5683c
  ids-array sha256 4668fc45716d46b408c778c93d2d844ad9b2c5bafb33458ec30a4b673ed44474
- Head: sklearn LogisticRegression(penalty='l2', C=1.0), defaults otherwise.
- Backbone: frozen Pythia-410m, hidden_states[20], final-token hidden state,
  float32, CPU, device_map='cpu', requires_grad_(False), model.eval(), torch.no_grad().
  Weights pin ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed
- Extraction input: premise == prompt[:prompt.index(' Question:')], prompt starts 'Premise:'.
- Sanity gate FIRST: retrained head must score 60/60 on the original EXP091 bench
  (rebuilt via EXP106 executor's build_test_premises VERBATIM), else RUN-INVALID.
- Overlap tripwire: train/test item-ID intersection must be 0, else RUN-INVALID.
- Block-off: two fresh backbone-only passes of the decorrelated bench bit-identical,
  and scored embeddings byte-identical to a fresh backbone-only pass, else INVALID.
- Bars: >=40/60 CONTINUE / <=35/60 KILL / 36-39 HELD. One-sided binomial vs 0.5.

Exit codes: 0 = valid verdict reached; 42 = overlap RUN-INVALID; 43/44/45 = hash RUN-INVALID;
46 = reuse-integrity RUN-INVALID; 47 = bench pin RUN-INVALID; 48 = sanity-gate RUN-INVALID;
49 = block-off INVALID (verdict void).
"""
import os, sys, json, math, hashlib, datetime
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.linear_model import LogisticRegression

OUT = os.path.expanduser('~/workspace/SCBI/experiments/runs/EXP107_templatectrl/out')
os.makedirs(OUT, exist_ok=True)
LOGF = open(os.path.join(OUT, 'exp107_execution_log.txt'), 'w')
def log(m):
    line = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {m}"
    print(line, flush=True); LOGF.write(line + '\n'); LOGF.flush()

SNAP = os.path.expanduser('~/workspace/.exp086_weights/pythia-410m')
WEIGHTS_PIN = 'ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed'
BENCH107_PIN = 'e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5'
EMB_ARR_PIN = '4e6229bea083570f17e3368326d9848c9a8db5dc25c7efc75f0e1a2960b5683c'
IDS_ARR_PIN = '4668fc45716d46b408c778c93d2d844ad9b2c5bafb33458ec30a4b673ed44474'
SITE = 20

def arr_sha(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()

def state_dict_hash(model):
    sha = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        sha.update(np.asarray(model.state_dict()[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()

def state_text_of(prompt):
    assert prompt.startswith('Premise:'), "prompt does not start with 'Premise:'"
    return prompt[:prompt.index(' Question:')]

# ---------------- environment manifest ----------------
import sklearn, transformers
manifest = {
    'torch': torch.__version__, 'transformers': transformers.__version__,
    'numpy': np.__version__, 'sklearn': sklearn.__version__,
    'snapshot': SNAP, 'site_hidden_states_index': SITE,
    'head': "LogisticRegression(penalty='l2', C=1.0) [all other params default]",
    'date': '2026-09-29', 'lane': 'LOG-4540',
}
log('ENV: ' + json.dumps(manifest))

# ---------------- reuse-integrity check (no new train extraction) ----------------
tr = np.load(os.path.expanduser('~/workspace/SCBI/experiments/runs/EXP106_lfh/out/exp106_train_embeddings.npz'))
X_train = np.ascontiguousarray(tr['embeddings'], dtype=np.float32)
train_ids = [str(i) for i in tr['ids']]
train_phrasing = [str(p) for p in tr['phrasing']]
assert X_train.shape == (60, 1024), X_train.shape
emb_h, ids_h = arr_sha(X_train), arr_sha(tr['ids'])
log(f'reuse-integrity: embeddings-array sha={emb_h[:16]}... match={emb_h == EMB_ARR_PIN}')
log(f'reuse-integrity: ids-array sha={ids_h[:16]}... match={ids_h == IDS_ARR_PIN}')
if emb_h != EMB_ARR_PIN or ids_h != IDS_ARR_PIN:
    log('RUN-INVALID: train-embeddings reuse integrity broken'); LOGF.close(); sys.exit(46)
y_train = np.array([1 if p == 'A-first' else 0 for p in train_phrasing], dtype=np.int64)
log(f'y_train: A-first(1)={int(y_train.sum())}, C-first(0)={int((1-y_train).sum())}')

# ---------------- decorrelated bench build + pin ----------------
sys.path.insert(0, os.path.expanduser('~/workspace/SCBI/experiments/runs/EXP107_templatectrl'))
import build_exp107_bench as b107
bench = b107.build_bench()
v = b107.verify_cells(bench)
log(f'bench cells: {v["cells"]}')
log(f'bench pin: {v["pin"][:16]}... match={v["pin"] == BENCH107_PIN}')
if v['pin'] != BENCH107_PIN:
    log('RUN-INVALID: decorrelated-bench pin mismatch'); LOGF.close(); sys.exit(47)
test_ids = [b['id'] for b in bench]
y_test = np.array([1 if b['phrasing'] == 'A-first' else 0 for b in bench], dtype=np.int64)
test_texts = [state_text_of(b['prompt']) for b in bench]
assert all('Question:' not in t for t in test_texts)
log(f'y_test: A-first(1)={int(y_test.sum())}, C-first(0)={int((1-y_test).sum())}')

# ---------------- overlap tripwire (Law #7) ----------------
overlap = sorted(set(train_ids) & set(test_ids))
log(f'OVERLAP TRIPWIRE: {len(overlap)} shared item IDs')
if overlap:
    log('RUN-INVALID: train/test item-ID overlap: ' + str(overlap)); LOGF.close(); sys.exit(42)

# ---------------- backbone load + pre hash (Law #6) ----------------
log('loading tokenizer + frozen model...')
tokenizer = AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(SNAP, local_files_only=True, torch_dtype=torch.float32, device_map='cpu')
model.eval(); model.requires_grad_(False)
pre = state_dict_hash(model)
log(f'G1 pre hash: {pre[:16]}... match={pre == WEIGHTS_PIN}')
if pre != WEIGHTS_PIN:
    log('RUN-INVALID: backbone hash mismatch (Law #6)'); LOGF.close(); sys.exit(43)

def extract(texts):
    embs = np.zeros((len(texts), model.config.hidden_size), dtype=np.float32)
    with torch.no_grad():
        for i, t in enumerate(texts):
            ids = torch.tensor([tokenizer.encode(t, add_special_tokens=False)], dtype=torch.long)
            out = model(ids, output_hidden_states=True)
            h = out.hidden_states[SITE][0, -1, :].detach().cpu().to(torch.float32).numpy()
            embs[i, :] = h
    return embs

# ---------------- train head (EXP106 spec verbatim; no tuning) ----------------
clf = LogisticRegression(penalty='l2', C=1.0)
clf.fit(X_train, y_train)
log(f'head fit: n_iter={clf.n_iter_}, coef shape={clf.coef_.shape}')

# ---------------- sanity gate: retrained head on ORIGINAL EXP091 bench ----------------
# EXP106 executor's build_test_premises, verbatim.
NOVEL_VOCAB_PLANET = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
NOVEL_VOCAB_ELEMENT = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
TRIPLES = [(0,1,2),(1,2,3),(2,3,4),(0,2,4),(0,1,3),(1,3,4),(0,2,3),(1,2,4),(0,3,4),(0,1,4),
           (0,1,2),(1,2,3),(2,3,4),(0,2,4),(0,1,3)]
QUADS = [(0,1,2,3),(1,2,3,4),(0,1,3,4),(0,2,3,4),(0,1,2,4),
         (0,1,2,3),(1,2,3,4),(0,1,3,4),(0,2,3,4),(0,1,2,4),
         (0,1,2,3),(1,2,3,4),(0,1,3,4),(0,2,3,4),(0,1,2,4)]
def build_test_premises():
    items = []
    for vocab, triples, quads, dom, thr in ((NOVEL_VOCAB_PLANET, TRIPLES, QUADS, 'planet', 8),
                                            (NOVEL_VOCAB_ELEMENT, TRIPLES, QUADS, 'element', 7)):
        for i, (iA, iB, iC) in enumerate(triples):
            A, B, C = vocab[iA], vocab[iB], vocab[iC]
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}." if i < thr
                 else f"Premise: {C} is lower than {B}. {B} is lower than {A}.")
            items.append((f'exp077_{dom}_2hop_{i}', p, 'A-first' if i < thr else 'C-first'))
        for i, (iA, iB, iC, iD) in enumerate(quads):
            A, B, C, D = vocab[iA], vocab[iB], vocab[iC], vocab[iD]
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}." if i < thr
                 else f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}.")
            items.append((f'exp077_{dom}_3hop_{i}', p, 'A-first' if i < thr else 'C-first'))
    return items
sg_items = build_test_premises()
sg_texts = [t[1] for t in sg_items]
sg_y = np.array([1 if t[2] == 'A-first' else 0 for t in sg_items], dtype=np.int64)
log('sanity gate: fresh extraction of original EXP091 bench (60 passes)...')
E_sg = extract(sg_texts)
sg_pred = clf.predict(E_sg)
sg_x = int((sg_pred == sg_y).sum())
log(f'SANITY GATE: {sg_x}/60 on original EXP091 bench (must be 60/60)')
if sg_x != 60:
    log('RUN-INVALID: sanity gate failed — pipeline drift, head is not the EXP106 head')
    LOGF.close(); sys.exit(48)
log('SANITY GATE: PASS')

mid = state_dict_hash(model)
log(f'G1 mid hash (post sanity-gate): {mid[:16]}... match={mid == WEIGHTS_PIN}')

# ---------------- decorrelated bench extraction (60 passes) ----------------
log('extracting decorrelated bench (60 passes, premise-only, hidden_states[20])...')
E = extract(test_texts)
assert E.shape == (60, 1024) and E.dtype == np.float32 and np.isfinite(E).all()
post = state_dict_hash(model)
log(f'G1 post hash: {post[:16]}... match={post == WEIGHTS_PIN} (Δθ=0)')
if post != WEIGHTS_PIN:
    log('RUN-INVALID: backbone hash changed during extraction (Law #6)'); LOGF.close(); sys.exit(44)
np.savez(os.path.join(OUT, 'exp107_test_embeddings.npz'), embeddings=E, ids=np.array(test_ids))
log(f'scored embeddings sha={arr_sha(E)[:16]}...')

# ---------------- score decorrelated bench ----------------
pred = clf.predict(E)
x = int((pred == y_test).sum())
log(f'DECORRELATED SCORE: {x}/60 = {x/60:.4f}')
cells = {}
for b, p_, y_ in zip(bench, pred, y_test):
    key = (b['phrasing'], 'flipped' if b['flipped'] else 'original')
    cells.setdefault(key, []).append(bool(p_ == y_))
cell_scores = {f'{p}/{w}': f'{int(sum(v))}/{len(v)}' for (p, w), v in sorted(cells.items())}
log('per-cell: ' + json.dumps(cell_scores))
per_item = [{'id': test_ids[i], 'phrasing': bench[i]['phrasing'],
             'flipped': bool(bench[i]['flipped']), 'derived_from': bench[i]['derived_from'],
             'y': int(y_test[i]), 'pred': int(pred[i]),
             'correct': bool(pred[i] == y_test[i])} for i in range(60)]
json.dump(per_item, open(os.path.join(OUT, 'exp107_per_item.json'), 'w'), indent=1)

p_val = sum(math.comb(60, k) for k in range(x, 61)) / 2**60
log(f'one-sided binomial p (vs 0.5): {p_val:.6e}')

# ---------------- block-off byte-identity ----------------
log('block-off: fresh backbone-only extraction, pass 1...')
E1 = extract(test_texts)
log('block-off: fresh backbone-only extraction, pass 2...')
E2 = extract(test_texts)
det = bool(np.array_equal(E1, E2))
byte_id = bool(np.array_equal(E, E1))
log(f'determinism pass1==pass2: {det}')
log(f'byte-identity scored==fresh: {byte_id}')
log(f'sha scored={arr_sha(E)[:16]} fresh1={arr_sha(E1)[:16]} fresh2={arr_sha(E2)[:16]}')
blockoff_pass = det and byte_id
log(f'BLOCK-OFF: {"PASS" if blockoff_pass else "FAIL"}')

final = state_dict_hash(model)
final_ok = final == WEIGHTS_PIN
log(f'G1 final hash: {final[:16]}... match={final_ok}')

result = {
    'x': x, 'n': 60, 'acc': x/60, 'p_one_sided_vs_chance': p_val,
    'cell_scores': cell_scores, 'sanity_gate': f'{sg_x}/60',
    'overlap': overlap, 'reuse_integrity_ok': True, 'bench_pin_ok': True,
    'blockoff_pass': blockoff_pass, 'determinism_pass1_eq_pass2': det,
    'byte_identity_scored_eq_fresh': byte_id, 'final_hash_ok': final_ok,
}
json.dump(result, open(os.path.join(OUT, 'exp107_result.json'), 'w'), indent=1)
log('RESULT: ' + json.dumps(result))
LOGF.close()

if not blockoff_pass:
    print('APPARATUS INVALID: block-off failed; verdict void.', flush=True)
    sys.exit(49)

# verdict
if x >= 40:
    print('VERDICT: CONTINUE')
elif x <= 35:
    print('VERDICT: KILL')
else:
    print('VERDICT: HELD')
