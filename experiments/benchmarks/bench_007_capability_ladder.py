"""
BENCH-007: Relational Capability Ladder Benchmark.
Six calibrated levels of computational complexity:
- Level 0: Lexical In-Context Recall (A -> B)
- Level 1: Direct Relational Mapping (1-hop: A > B)
- Level 2: 2-Hop Transitive Deduction (Clean Chain with Positional Permutations)
- Level 3: 3-Hop Transitive Deduction (Deep Chain: A > B > C > D)
- Level 4: Distractor-Resistant Transitivity (Interleaved Distractor Relations)
- Level 5: Compositional Transfer Across Disjoint Vocabulary

Governing Standard: AGENTS.md Laws 1, 2, 6, 7, 9, 13, 14.
Pre-Registration: EXP060_CAPABILITY_LADDER_SPEC.md
"""

def generate_bench_007_capability_ladder():
    dataset = []
    global_id = 0

    # -------------------------------------------------------------
    # LEVEL 0: Lexical In-Context Recall (A -> B, 30 instances)
    # -------------------------------------------------------------
    keys = ["Alpha", "Beta", "Gamma", "Delta", "Omega", "Sigma", "Theta", "Zeta", "Kappa", "Lambda"]
    vals = ["Blue", "Red", "Green", "Yellow", "Purple", "Orange", "Silver", "Gold", "Black", "White"]
    
    for i in range(30):
        # Pick 3 key-value bindings
        k_idx = [ (i * 3 + j) % len(keys) for j in range(3) ]
        v_idx = [ (i * 2 + j) % len(vals) for j in range(3) ]
        
        target_k = keys[k_idx[0]]
        target_v = vals[v_idx[0]]
        foil_v = vals[v_idx[1]]
        
        # 50% query option 1 first, 50% option 2 first
        if i % 2 == 0:
            query_opts = f"{target_v} or {foil_v}"
            target_first = True
        else:
            query_opts = f"{foil_v} or {target_v}"
            target_first = False

        prompt = (
            f"Dictionary mapping: {target_k} maps to {target_v}. "
            f"{keys[k_idx[1]]} maps to {vals[v_idx[1]]}. "
            f"{keys[k_idx[2]]} maps to {vals[v_idx[2]]}. "
            f"Question: What does {target_k} map to, {query_opts}? Answer:"
        )
        
        dataset.append({
            "id": global_id,
            "level": 0,
            "level_name": "level0_lexical_recall",
            "prompt": prompt,
            "target": target_v,
            "foil": foil_v,
            "target_token": " " + target_v,
            "foil_token": " " + foil_v,
            "target_queried_first": target_first,
            "surface_reversed": False
        })
        global_id += 1

    # -------------------------------------------------------------
    # LEVEL 1: Direct Relational Mapping (1-Hop: A > B, 30 instances)
    # -------------------------------------------------------------
    ents_l1 = ["Alice", "Bob", "Charlie", "David", "Emma"]
    for i in range(30):
        e1 = ents_l1[i % len(ents_l1)]
        e2 = ents_l1[(i + 1 + (i // len(ents_l1))) % len(ents_l1)]
        
        # 50% forward (who is higher), 50% inverse (who is lower)
        is_forward = (i % 2 == 0)
        target_first = ((i // 2) % 2 == 0)
        
        if is_forward:
            target = e1
            foil = e2
            query_opts = f"{target} or {foil}" if target_first else f"{foil} or {target}"
            prompt = f"Premise: {e1} outranks {e2}. Question: Who is higher in rank, {query_opts}? Answer:"
        else:
            target = e2
            foil = e1
            query_opts = f"{target} or {foil}" if target_first else f"{foil} or {target}"
            prompt = f"Premise: {e1} outranks {e2}. Question: Who is lower in rank, {query_opts}? Answer:"
            
        dataset.append({
            "id": global_id,
            "level": 1,
            "level_name": "level1_direct_relational",
            "prompt": prompt,
            "target": target,
            "foil": foil,
            "target_token": " " + target,
            "foil_token": " " + foil,
            "target_queried_first": target_first,
            "surface_reversed": not is_forward
        })
        global_id += 1

    # -------------------------------------------------------------
    # LEVEL 2: 2-Hop Transitive Deduction (Clean Chain, 30 instances)
    # Positional Permutations: 50% semantic order matches surface order,
    # 50% surface order is reversed (e.g. C is outranked by B. B is outranked by A).
    # -------------------------------------------------------------
    ents_l2 = ["Alice", "Bob", "Charlie", "David", "Emma"]
    triples_l2 = [
        (ents_l2[0], ents_l2[1], ents_l2[2]),
        (ents_l2[1], ents_l2[2], ents_l2[3]),
        (ents_l2[2], ents_l2[3], ents_l2[4]),
        (ents_l2[0], ents_l2[2], ents_l2[4]),
        (ents_l2[0], ents_l2[1], ents_l2[3]),
        (ents_l2[1], ents_l2[3], ents_l2[4]),
        (ents_l2[0], ents_l2[2], ents_l2[3]),
        (ents_l2[1], ents_l2[2], ents_l2[4]),
        (ents_l2[0], ents_l2[3], ents_l2[4]),
        (ents_l2[0], ents_l2[1], ents_l2[4])
    ]
    
    for i in range(30):
        A, B, C = triples_l2[i % len(triples_l2)]
        target = A
        foil = C
        target_first = (i % 2 == 0)
        query_opts = f"{target} or {foil}" if target_first else f"{foil} or {target}"
        
        # Symmetrically permute surface premise order
        is_surface_reversed = (i >= 15)
        if not is_surface_reversed:
            # Surface matches semantic order: A > B, B > C
            prompt = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {query_opts}? Answer:"
        else:
            # Surface order reversed: C is lower than B. B is lower than A.
            prompt = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {query_opts}? Answer:"
            
        dataset.append({
            "id": global_id,
            "level": 2,
            "level_name": "level2_2hop_transitive",
            "prompt": prompt,
            "target": target,
            "foil": foil,
            "target_token": " " + target,
            "foil_token": " " + foil,
            "target_queried_first": target_first,
            "surface_reversed": is_surface_reversed
        })
        global_id += 1

    # -------------------------------------------------------------
    # LEVEL 3: 3-Hop Transitive Deduction (Deep Chain, 30 instances)
    # A > B > C > D => A > D
    # -------------------------------------------------------------
    ents_l3 = ["Alice", "Bob", "Charlie", "David", "Emma"]
    quads_l3 = [
        (ents_l3[0], ents_l3[1], ents_l3[2], ents_l3[3]),
        (ents_l3[1], ents_l3[2], ents_l3[3], ents_l3[4]),
        (ents_l3[0], ents_l3[1], ents_l3[3], ents_l3[4]),
        (ents_l3[0], ents_l3[2], ents_l3[3], ents_l3[4]),
        (ents_l3[0], ents_l3[1], ents_l3[2], ents_l3[4])
    ]
    for i in range(30):
        A, B, C, D = quads_l3[i % len(quads_l3)]
        target = A
        foil = D
        target_first = (i % 2 == 0)
        query_opts = f"{target} or {foil}" if target_first else f"{foil} or {target}"
        
        is_surface_reversed = (i >= 15)
        if not is_surface_reversed:
            prompt = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {query_opts}? Answer:"
        else:
            prompt = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {query_opts}? Answer:"
            
        dataset.append({
            "id": global_id,
            "level": 3,
            "level_name": "level3_3hop_transitive",
            "prompt": prompt,
            "target": target,
            "foil": foil,
            "target_token": " " + target,
            "foil_token": " " + foil,
            "target_queried_first": target_first,
            "surface_reversed": is_surface_reversed
        })
        global_id += 1

    # -------------------------------------------------------------
    # LEVEL 4: Distractor-Resistant Transitivity (30 instances)
    # A > B, X > Y, B > C, Z > Q => A > C
    # -------------------------------------------------------------
    distractors = [
        ("Reactor", "Turbine"),
        ("Boiler", "Condenser"),
        ("Generator", "Transformer"),
        ("Piston", "Cylinder")
    ]
    for i in range(30):
        A, B, C = triples_l2[i % len(triples_l2)]
        target = A
        foil = C
        target_first = (i % 2 == 0)
        query_opts = f"{target} or {foil}" if target_first else f"{foil} or {target}"
        
        d1 = distractors[i % len(distractors)]
        d2 = distractors[(i + 1) % len(distractors)]
        
        prompt = (
            f"Premise: {A} outranks {B}. "
            f"Notice: {d1[0]} overrides {d1[1]}. "
            f"Premise: {B} outranks {C}. "
            f"Notice: {d2[0]} overrides {d2[1]}. "
            f"Question: Who is higher in rank, {query_opts}? Answer:"
        )
        
        dataset.append({
            "id": global_id,
            "level": 4,
            "level_name": "level4_distractor_resistant",
            "prompt": prompt,
            "target": target,
            "foil": foil,
            "target_token": " " + target,
            "foil_token": " " + foil,
            "target_queried_first": target_first,
            "surface_reversed": False
        })
        global_id += 1

    # -------------------------------------------------------------
    # LEVEL 5: Compositional Transfer Across Disjoint Vocabulary (30 instances)
    # Completely disjoint novel entities: verified single-token entities in Pythia-160M
    # -------------------------------------------------------------
    novel_ents = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
    novel_triples = [
        (novel_ents[0], novel_ents[1], novel_ents[2]),
        (novel_ents[1], novel_ents[2], novel_ents[3]),
        (novel_ents[2], novel_ents[3], novel_ents[4]),
        (novel_ents[0], novel_ents[2], novel_ents[4]),
        (novel_ents[0], novel_ents[1], novel_ents[3]),
        (novel_ents[1], novel_ents[3], novel_ents[4]),
        (novel_ents[0], novel_ents[2], novel_ents[3]),
        (novel_ents[1], novel_ents[2], novel_ents[4]),
        (novel_ents[0], novel_ents[3], novel_ents[4]),
        (novel_ents[0], novel_ents[1], novel_ents[4])
    ]
    for i in range(30):
        A, B, C = novel_triples[i % len(novel_triples)]
        target = A
        foil = C
        target_first = (i % 2 == 0)
        query_opts = f"{target} or {foil}" if target_first else f"{foil} or {target}"
        
        is_surface_reversed = (i >= 15)
        if not is_surface_reversed:
            prompt = f"Premise: {A} is brighter than {B}. {B} is brighter than {C}. Question: Which is brighter, {query_opts}? Answer:"
        else:
            prompt = f"Premise: {C} is dimmer than {B}. {B} is dimmer than {A}. Question: Which is brighter, {query_opts}? Answer:"
            
        dataset.append({
            "id": global_id,
            "level": 5,
            "level_name": "level5_compositional_transfer",
            "prompt": prompt,
            "target": target,
            "foil": foil,
            "target_token": " " + target,
            "foil_token": " " + foil,
            "target_queried_first": target_first,
            "surface_reversed": is_surface_reversed
        })
        global_id += 1

    return dataset

if __name__ == "__main__":
    data = generate_bench_007_capability_ladder()
    print(f"Total instances: {len(data)}")
    for l in range(6):
        l_items = [d for d in data if d["level"] == l]
        first_q = sum(1 for d in l_items if d["target_queried_first"])
        rev = sum(1 for d in l_items if d["surface_reversed"])
        print(f"Level {l} ({l_items[0]['level_name']}): N={len(l_items)}, Target Queried First={first_q}/30, Surface Reversed={rev}/30")
