"""EXP106 (H3/LFH) execution — signed pre-registration
~/workspace/SCBI/research/prereg/EXP_PREREG_H3_LFH_2026-09-29.md
CEO launch: LOG-4533. Lane: LOG-4534.

Pinned spec (FIX-1/2/3):
- Head: sklearn LogisticRegression(penalty='l2', C=1.0), defaults otherwise.
- Embeddings: frozen Pythia-410m, program-standard read site = hidden_states[20]
  (the EXP091-bench site, verified by disassembly of the EXP091 extractor),
  final-token hidden state, float32, CPU, device_map='cpu',
  requires_grad_(False), model.eval(), torch.no_grad().
- Item encoding: premise-sentences substring, prompt[:prompt.index(' Question:')].
- Train: EXP092-B (60 items, bench pin verified), y = 1 iff phrasing=='A-first'.
- Test: archived EXP091 state embeddings (60 items), y = phrasing.
- Overlap tripwire: any train/test item-ID overlap -> RUN-INVALID.
- Backbone hash pre/post == WEIGHTS_PIN else RUN-INVALID (Law #6).
- Block-off: fresh backbone-only re-extraction of the full test bench,
  bit-compared against the embeddings used for scoring. Mismatch -> INVALID.
- Bars: >=40/60 CONTINUE / <=35/60 KILL / 36-39 HELD. One-sided binomial vs 0.5.
"""
import os, sys, json, math, hashlib, datetime
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.linear_model import LogisticRegression

OUT = os.path.expanduser('~/workspace/SCBI/experiments/runs/EXP106_lfh/out')
os.makedirs(OUT, exist_ok=True)
LOGF = open(os.path.join(OUT, 'exp106_execution_log.txt'), 'w')
def log(m):
    line = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {m}"
    print(line, flush=True); LOGF.write(line + '\n'); LOGF.flush()

SNAP = os.path.expanduser('~/workspace/.exp086_weights/pythia-410m')
WEIGHTS_PIN = 'ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed'
BENCH_PIN = '9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4'
SITE = 20  # hidden_states index: the EXP091 program-standard read site

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
    'date': '2026-09-29',
}
log('ENV: ' + json.dumps(manifest))

# ---------------- train bench: rebuild + pin ----------------
sys.path.insert(0, os.path.expanduser('~/workspace/SCBI/experiments/runs/EXP092_ibl'))
import reference_implementation as ref
bench92 = ref.build_bench()
pin = ref.bench_sha256(bench92)
assert pin == BENCH_PIN, f'BENCH PIN MISMATCH {pin}'
log(f'G0 bench pin OK: {pin[:16]}... (60 items)')
train_ids = [b['id'] for b in bench92]
y_train = np.array([1 if b['phrasing'] == 'A-first' else 0 for b in bench92], dtype=np.int64)
log(f'y_train: A-first(1)={int(y_train.sum())}, C-first(0)={int((1-y_train).sum())}')
train_texts = [state_text_of(b['prompt']) for b in bench92]
assert all('Question:' not in t for t in train_texts)

# ---------------- test bench: archived embeddings ----------------
tst = np.load(os.path.expanduser('~/workspace/SCBI/experiments/runs/EXP091_clm8b_falsifier_v3/out/exp091_embeddings.npz'), allow_pickle=True)
X_test = np.asarray(tst['state'], dtype=np.float32)
test_ids = [str(i) for i in tst['ids']]
y_test = np.array([1 if p == 'A-first' else 0 for p in tst['phrasing']], dtype=np.int64)
log(f'test archive: X_test {X_test.shape} {X_test.dtype}; A-first(1)={int(y_test.sum())}, C-first(0)={int((1-y_test).sum())}')

# ---------------- overlap tripwire (Law #7) ----------------
overlap = sorted(set(train_ids) & set(test_ids))
log(f'OVERLAP TRIPWIRE: {len(overlap)} shared item IDs')
if overlap:
    log('RUN-INVALID: train/test item-ID overlap: ' + str(overlap)); LOGF.close(); sys.exit(42)

# ---------------- backbone load + pre hash ----------------
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

# ---------------- train extraction (60 passes) ----------------
log('extracting train embeddings (60 passes, premise-only, hidden_states[20])...')
X_train = extract(train_texts)
assert X_train.shape == (60, 1024) and X_train.dtype == np.float32
assert np.isfinite(X_train).all()
log(f'X_train {X_train.shape}, std per-dim mean={X_train.std():.4f}')

post = state_dict_hash(model)
log(f'G1 post hash: {post[:16]}... match={post == WEIGHTS_PIN} (Δθ=0)')
if post != WEIGHTS_PIN:
    log('RUN-INVALID: backbone hash changed during extraction (Law #6)'); LOGF.close(); sys.exit(44)

np.savez(os.path.join(OUT, 'exp106_train_embeddings.npz'),
         embeddings=X_train, ids=np.array(train_ids),
         phrasing=np.array([b['phrasing'] for b in bench92]))

# ---------------- train head (FIX-1: C=1.0, no tuning) ----------------
clf = LogisticRegression(penalty='l2', C=1.0)
clf.fit(X_train, y_train)
log(f'head fit: n_iter={clf.n_iter_}, coef shape={clf.coef_.shape}')
train_acc = float(clf.score(X_train, y_train))
log(f'train accuracy (secondary, non-binding): {train_acc:.4f} ({int(train_acc*60)}/60)')

# ---------------- score on test bench ----------------
pred = clf.predict(X_test)
x = int((pred == y_test).sum())
log(f'TEST SCORE: {x}/60 = {x/60:.4f}')
per_item = [{'id': test_ids[i], 'y': int(y_test[i]), 'pred': int(pred[i]),
             'correct': bool(pred[i] == y_test[i])} for i in range(60)]
json.dump(per_item, open(os.path.join(OUT, 'exp106_per_item.json'), 'w'), indent=1)

# one-sided binomial p vs chance: P(X >= x | n=60, p=0.5)
p_val = sum(math.comb(60, k) for k in range(x, 61)) / 2**60
log(f'one-sided binomial p (vs 0.5): {p_val:.6f}')

# ---------------- block-off byte-identity check ----------------
# Rebuild EXP091 test premises from the repaired EXP077 builder (verbatim logic).
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
titems = build_test_premises()
assert [t[0] for t in titems] == test_ids, 'test ID order mismatch vs archive'
assert [t[2] for t in titems] == [str(p) for p in tst['phrasing']], 'phrasing pattern mismatch vs archive'
log('test-bench reconstruction verified: 60/60 ids + phrasing match archive')
test_texts = [t[1] for t in titems]

log('block-off: fresh backbone-only extraction, pass 1...')
E1 = extract(test_texts)
log('block-off: fresh backbone-only extraction, pass 2...')
E2 = extract(test_texts)
det = bool(np.array_equal(E1, E2))
log(f'determinism pass1==pass2: {det}')
arch = X_test
b1 = bool(np.array_equal(E1, arch))
log(f'byte-identity fresh==archive: {b1}')
sha = lambda a: hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
log(f'sha archive={sha(arch)[:16]} fresh1={sha(E1)[:16]} fresh2={sha(E2)[:16]}')
blockoff_pass = det and b1
log(f'BLOCK-OFF: {"PASS" if blockoff_pass else "FAIL"}')
if not blockoff_pass:
    log('APPARATUS INVALID: block-off byte-identity failed; any CONTINUE void.')

post2 = state_dict_hash(model)
log(f'G1 final hash: {post2[:16]}... match={post2 == WEIGHTS_PIN}')

result = {
    'x': x, 'n': 60, 'acc': x/60, 'p_one_sided_vs_chance': p_val,
    'train_acc': train_acc, 'overlap': overlap,
    'blockoff_pass': blockoff_pass, 'determinism_pass1_eq_pass2': det,
    'final_hash_ok': post2 == WEIGHTS_PIN,
}
json.dump(result, open(os.path.join(OUT, 'exp106_result.json'), 'w'), indent=1)
log('RESULT: ' + json.dumps(result))
LOGF.close()
