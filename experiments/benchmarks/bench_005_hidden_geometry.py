"""
BENCH-005-HIDDEN-GEOMETRY: Synthetic Multi-Geometry Benchmark for SCPM.
Implements 6 distinct hidden computational structures:
1. Hierarchy: Taxonomic tree inheritance (category depth reasoning)
2. Temporal: Sequential event ordering (before/after chronologies)
3. Causal: Directed causal chains (mechanistic cause-effect reasoning)
4. Interaction: Non-linear feature conjunctions (XOR / condition pairing)
5. Exclusion: Negation and set difference (mutual exclusivity)
6. Distractor: Lexical distractor interference (canonical competition)

When evaluated by SCPM, NO structural labels, spans, or geometry annotations
are exposed. The model receives only the raw text prompt 'base'.
"""

import random

def generate_bench_005_hidden_geometry(n_per_geometry=20, seed=500):
    rng = random.Random(seed)
    dataset = []
    global_id = 0

    # 1. HIERARCHY (Taxonomic Category Depth)
    hierarchy_trees = [
        {"root": "animal", "branches": [
            {"mid": "mammal", "leaves": ["canine", "feline", "bovine", "equine"], "targets": ["fur", "milk", "warmth", "lungs"]},
            {"mid": "reptile", "leaves": ["lizard", "snake", "turtle", "gecko"], "targets": ["scales", "claws", "eggs", "cold"]},
            {"mid": "avian", "leaves": ["eagle", "sparrow", "falcon", "parrot"], "targets": ["feathers", "beak", "wings", "nest"]}
        ]},
        {"root": "vehicle", "branches": [
            {"mid": "aircraft", "leaves": ["jet", "glider", "biplane", "helicopter"], "targets": ["wings", "altitude", "rotor", "cockpit"]},
            {"mid": "watercraft", "leaves": ["submarine", "frigate", "sailboat", "kayak"], "targets": ["hull", "rudder", "anchor", "buoyancy"]},
            {"mid": "landcraft", "leaves": ["truck", "sedan", "tractor", "scooter"], "targets": ["wheels", "tires", "engine", "axle"]}
        ]}
    ]
    for i in range(n_per_geometry):
        tree = hierarchy_trees[i % len(hierarchy_trees)]
        branch = rng.choice(tree["branches"])
        other_branch = rng.choice([b for b in tree["branches"] if b != branch])
        leaf = rng.choice(branch["leaves"])
        other_leaf = rng.choice(other_branch["leaves"])
        target = rng.choice(branch["targets"])
        distractor = rng.choice(other_branch["targets"])
        
        prompt = f"Premise: A {leaf} has {target}. Distractor: A {other_leaf} has {distractor}. Question: What does a {leaf} have? Answer: A {leaf} has"
        dataset.append({
            "id": global_id,
            "geometry": "hierarchy",
            "base": prompt,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor
        })
        global_id += 1

    # 2. TEMPORAL (Sequential Event Ordering)
    temporal_events = [
        ("dawn", "noon", "dusk", "midnight"),
        ("Monday", "Wednesday", "Friday", "Sunday"),
        ("spring", "summer", "autumn", "winter"),
        ("January", "April", "August", "December")
    ]
    for i in range(n_per_geometry):
        seq = temporal_events[i % len(temporal_events)]
        t1, t2, t3, t4 = seq
        target = t3
        distractor = t1
        prompt = f"Chronology: First event was {t1}. Second event was {t2}. Third scheduled event was {target}. Earlier event was {distractor}. Question: What was the third event? Answer: The third event was"
        dataset.append({
            "id": global_id,
            "geometry": "temporal",
            "base": prompt,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor
        })
        global_id += 1

    # 3. CAUSAL (Directed Cause-Effect Chains)
    causal_chains = [
        {"cause": "spark", "intermediate": "flame", "effect": "smoke", "confound": "water"},
        {"cause": "frost", "intermediate": "ice", "effect": "slip", "confound": "sun"},
        {"cause": "virus", "intermediate": "fever", "effect": "sweat", "confound": "cure"},
        {"cause": "leak", "intermediate": "puddle", "effect": "rust", "confound": "seal"}
    ]
    for i in range(n_per_geometry):
        chain = causal_chains[i % len(causal_chains)]
        target = chain["effect"]
        distractor = chain["confound"]
        prompt = f"Process log: The primary reaction produced {target}. A secondary side-effect caused {distractor}. Question: What did the primary reaction produce? Answer: The primary reaction produced"
        dataset.append({
            "id": global_id,
            "geometry": "causal",
            "base": prompt,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor
        })
        global_id += 1

    # 4. INTERACTION (Non-linear conjunction / XOR Logic)
    interaction_cases = [
        {"cond_a": "acid", "cond_b": "base", "result": "salt", "single": "fumes"},
        {"cond_a": "north", "cond_b": "south", "result": "attract", "single": "repel"},
        {"cond_a": "heat", "cond_b": "oxygen", "result": "combustion", "single": "smoke"},
        {"cond_a": "charge", "cond_b": "mass", "result": "plasma", "single": "light"}
    ]
    for i in range(n_per_geometry):
        case = interaction_cases[i % len(interaction_cases)]
        target = case["result"]
        distractor = case["single"]
        prompt = f"Reaction log: Single chemicals remain inert. Combining {case['cond_a']} and {case['cond_b']} produces {target}. Heating produces {distractor}. Question: What does combining {case['cond_a']} and {case['cond_b']} produce? Answer: Combining {case['cond_a']} and {case['cond_b']} produces"
        dataset.append({
            "id": global_id,
            "geometry": "interaction",
            "base": prompt,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor
        })
        global_id += 1

    # 5. EXCLUSION (Negation & Set Difference)
    exclusion_cases = [
        {"all": ["gold", "silver", "bronze"], "excluded": "gold", "target": "silver", "distractor": "gold"},
        {"all": ["circle", "triangle", "square"], "excluded": "circle", "target": "triangle", "distractor": "circle"},
        {"all": ["north", "east", "west"], "excluded": "north", "target": "east", "distractor": "north"},
        {"all": ["alpha", "beta", "gamma"], "excluded": "alpha", "target": "beta", "distractor": "alpha"}
    ]
    for i in range(n_per_geometry):
        case = exclusion_cases[i % len(exclusion_cases)]
        target = case["target"]
        distractor = case["distractor"]
        prompt = f"Selection rule: Options are {distractor} and {target}. The rule strictly forbids {case['excluded']}. Question: Which option is accepted? Answer: The accepted option is"
        dataset.append({
            "id": global_id,
            "geometry": "exclusion",
            "base": prompt,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor
        })
        global_id += 1

    # 6. DISTRACTOR INTERFERENCE (Canonical Interference)
    distractor_cases = [
        {"box": "blue", "dist_box": "red", "target": "blue", "distractor": "red"},
        {"box": "green", "dist_box": "yellow", "target": "green", "distractor": "yellow"},
        {"box": "wooden", "dist_box": "metal", "target": "wooden", "distractor": "metal"},
        {"box": "glass", "dist_box": "plastic", "target": "glass", "distractor": "plastic"}
    ]
    for i in range(n_per_geometry):
        case = distractor_cases[i % len(distractor_cases)]
        target = case["target"]
        distractor = case["distractor"]
        prompt = f"Fact: The key is inside the {case['box']} box. Note: The {case['dist_box']} box contains coins. Question: Where is the key? Answer: The key is in the"
        dataset.append({
            "id": global_id,
            "geometry": "distractor",
            "base": prompt,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor
        })
        global_id += 1

    return dataset

if __name__ == "__main__":
    bench = generate_bench_005_hidden_geometry(n_per_geometry=5, seed=500)
    print(f"Generated {len(bench)} instances across 6 geometries.")
    for inst in bench[::5]:
        print(f"\n[Geometry: {inst['geometry']}]")
        print(f"Base: {inst['base']}")
        print(f"Target: {inst['target']} | Distractor: {inst['distractor']}")
