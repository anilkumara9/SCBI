"""CPU-only held-out bench construction for the S5-inverted pre-reg.
Replicates build_bench/make_views/novel_src from
experiments/runs/EXP140_stage1/run_stage1.py VERBATIM (string ops only;
no model, no tokenizer, no forward passes)."""
import json, hashlib, re

src = open('/home/hatch/workspace/SCBI/experiments/runs/EXP140_stage1/run_stage1.py').read()

def get_list(name):
    m = re.search(name + r'\s*=\s*(\[.*?\])', src, re.S)
    return eval(m.group(1))

def get_dict(name):
    # SUPPORT_VOCABULARIES = { ... }  (grab balanced braces)
    i = src.index(name)
    j = src.index('{', i)
    depth = 0
    for k in range(j, len(src)):
        if src[k] == '{': depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0:
                return eval(src[j:k+1])

NOVEL_VOCAB_PLANET = get_list('NOVEL_VOCAB_PLANET')
NOVEL_VOCAB_ELEMENT = get_list('NOVEL_VOCAB_ELEMENT')
TRIPLES_INDICES = get_list('TRIPLES_INDICES')
QUADS_INDICES = get_list('QUADS_INDICES')
SUPPORT_VOCABULARIES = get_dict('SUPPORT_VOCABULARIES')
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())
print('view keys:', VOCAB_KEYS)

def build_bench():
    bench = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = "%s or %s" % (A, C) if target_first else "%s or %s" % (C, A)
        if i < 8:
            p = "Premise: %s outranks %s. %s outranks %s. Question: Who is higher in rank, %s? Answer:" % (A, B, B, C, q_opts)
        else:
            p = "Premise: %s is lower than %s. %s is lower than %s. Question: Who is higher in rank, %s? Answer:" % (C, B, B, A, q_opts)
        bench.append({"id": "exp077_planet_2hop_%d" % i, "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "planet", "hop": 2, "domain": "Planetary",
                      "idx": (iA, iB, iC), "tfirst": target_first, "variant": "outranks" if i < 8 else "lower"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                          NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        target_first = (i % 2 == 1)
        q_opts = "%s or %s" % (A, D_ent) if target_first else "%s or %s" % (D_ent, A)
        if i < 8:
            p = ("Premise: %s outranks %s. %s outranks %s. %s outranks %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (A, B, B, C, C, D_ent, q_opts)
        else:
            p = ("Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (D_ent, C, C, B, B, A, q_opts)
        bench.append({"id": "exp077_planet_3hop_%d" % i, "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "planet", "hop": 3, "domain": "Planetary",
                      "idx": (iA, iB, iC, iD), "tfirst": target_first, "variant": "outranks" if i < 8 else "lower"})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = "%s or %s" % (A, C) if target_first else "%s or %s" % (C, A)
        if i < 7:
            p = "Premise: %s outranks %s. %s outranks %s. Question: Who is higher in rank, %s? Answer:" % (A, B, B, C, q_opts)
        else:
            p = "Premise: %s is lower than %s. %s is lower than %s. Question: Who is higher in rank, %s? Answer:" % (C, B, B, A, q_opts)
        bench.append({"id": "exp077_element_2hop_%d" % i, "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "element", "hop": 2, "domain": "Elemental",
                      "idx": (iA, iB, iC), "tfirst": target_first, "variant": "outranks" if i < 7 else "lower"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                          NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        target_first = (i % 2 == 0)
        q_opts = "%s or %s" % (A, D_ent) if target_first else "%s or %s" % (D_ent, A)
        if i < 7:
            p = ("Premise: %s outranks %s. %s outranks %s. %s outranks %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (A, B, B, C, C, D_ent, q_opts)
        else:
            p = ("Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (D_ent, C, C, B, B, A, q_opts)
        bench.append({"id": "exp077_element_3hop_%d" % i, "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "element", "hop": 3, "domain": "Elemental",
                      "idx": (iA, iB, iC, iD), "tfirst": target_first, "variant": "outranks" if i < 7 else "lower"})
    return bench

def make_views(it, src_ents):
    views = []
    for vk in VOCAB_KEYS:
        sub = dict(zip(src_ents, [SUPPORT_VOCABULARIES[vk][k] for k in it["idx"]]))
        prompt = it["prompt"]
        for old, new in sub.items():
            assert old in prompt, "substitution source missing: %s" % old
            prompt = prompt.replace(old, new)
        views.append({"prompt": prompt, "vk": vk, "A": sub[it["A"]], "C": sub[it["C"]]})
    return views

def novel_src(it):
    base = NOVEL_VOCAB_PLANET if it["typ"] == "planet" else NOVEL_VOCAB_ELEMENT
    return [base[k] for k in it["idx"]]

bench = build_bench()
assert len(bench) == 60
disc_sha = hashlib.sha256(json.dumps(
    [{k: bench[i][k] for k in ("id", "prompt", "A", "C")} for i in range(len(bench))],
    sort_keys=True).encode()).hexdigest()
print('discovery bench sha:', disc_sha)
print('matches committed pin:', disc_sha == 'eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df')

# view-0 sanity: replicate discovery items
items_v0 = [make_views(it, novel_src(it))[0] for it in bench]
# held-out: view 1 (V2_Biblical)
HELD_VIEW = 1
items_v1 = [make_views(it, novel_src(it))[HELD_VIEW] for it in bench]
assert all(v["vk"] == "V2_Biblical" for v in items_v1)
# zero prompt overlap with discovery view-0
v0_prompts = set(v["prompt"] for v in items_v0)
v1_prompts = [v["prompt"] for v in items_v1]
print('view-1 prompt overlap with view-0:', len(set(v1_prompts) & v0_prompts))
print('view-1 A/C names:', sorted(set(v["A"] for v in items_v1) | set(v["C"] for v in items_v1)))

held = [{"id": "s5inv_held_%02d" % n, "src_id": bench[n]["id"],
         "prompt": v["prompt"], "A": v["A"], "C": v["C"], "vk": v["vk"],
         "typ": bench[n]["typ"], "hop": bench[n]["hop"]}
        for n, v in enumerate(items_v1)]
held_sha = hashlib.sha256(json.dumps(
    [{k: h[k] for k in ("id", "prompt", "A", "C")} for h in held],
    sort_keys=True).encode()).hexdigest()
print('HELD-OUT bench sha256:', held_sha)
json.dump({"bench": held, "sha256": held_sha, "view": "V2_Biblical", "view_index": HELD_VIEW,
           "derived_from_bench_sha": disc_sha},
          open('/home/hatch/workspace/SCBI/research/analysis_plans/S5-INV_HELDBENCH_2026-10-05.json', 'w'),
          indent=1)
print('saved S5-INV_HELDBENCH_2026-10-05.json')

# single-token check for view-1 names (tokenizer load = no forward passes)
try:
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained('EleutherAI/pythia-410m', revision='9879c9b5f8bea9051dcb0e68dff21493d67e9d4f',
                                        local_files_only=True, trust_remote_code=False)
    names = sorted(set(v["A"] for v in items_v1) | set(v["C"] for v in items_v1))
    multi = [w for w in names if len(tok.encode(w, add_special_tokens=False)) != 1]
    print('tokenizer OK; multi-token view-1 names:', multi if multi else 'NONE — all single-token')
except Exception as e:
    print('tokenizer unavailable:', str(e)[:120])
