"""
BENCH-006: Transitive Relational Reasoning Across Disjoint Surface Domains.
Evaluates 2-hop transitive deduction: A > B and B > C => A > C
across 5 completely disjoint vocabulary domains and matched non-transitive controls.
Pre-Registration: EXP059_TRANSITIVE_RELATION_TRANSFER_SPEC.md
Governing Standard: AGENTS.md Laws 1, 2, 6, 7, 9, 13, 14.
"""

def generate_bench_006_transitive():
    domains = {
        "domain0_discovery_social": {
            "entities": ["Alice", "Bob", "Charlie", "David", "Emma"],
            "verb": "outranks",
            "relation_name": "higher in rank"
        },
        "domain1_heldout_names": {
            "entities": ["Mira", "Kael", "Nova", "Orion", "Lyra"],
            "verb": "outranks",
            "relation_name": "higher in rank"
        },
        "domain2_biochemical": {
            "entities": ["Kinase", "Phosphatase", "Enzyme", "Receptor", "Substrate"],
            "verb": "activates",
            "relation_name": "upstream activator"
        },
        "domain3_industrial": {
            "entities": ["Reactor", "Turbine", "Generator", "Boiler", "Condenser"],
            "verb": "overrides",
            "relation_name": "higher priority"
        },
        "domain4_symbolic": {
            "entities": ["Alpha", "Beta", "Gamma", "Omega", "Sigma"],
            "verb": "precedes",
            "relation_name": "earlier in sequence"
        }
    }

    dataset = []
    global_id = 0

    for dom_key, dom_cfg in domains.items():
        ents = dom_cfg["entities"]
        verb = dom_cfg["verb"]
        rel = dom_cfg["relation_name"]

        # Form 10 unique ordered triples (A, B, C)
        triples = [
            (ents[0], ents[1], ents[2]),
            (ents[1], ents[2], ents[3]),
            (ents[2], ents[3], ents[4]),
            (ents[0], ents[2], ents[4]),
            (ents[0], ents[1], ents[3]),
            (ents[1], ents[3], ents[4]),
            (ents[0], ents[2], ents[3]),
            (ents[1], ents[2], ents[4]),
            (ents[0], ents[3], ents[4]),
            (ents[2], ents[1], ents[0]) # cyclic test
        ][:8]

        # 1. Forward Transitive (Valid: A > B, B > C => A > C)
        for A, B, C in triples:
            prompt = f"Premise: {A} {verb} {B}. {B} {verb} {C}. Question: Who is {rel}, {A} or {C}? Answer:"
            dataset.append({
                "id": global_id,
                "domain": dom_key,
                "task_type": "transitive_forward",
                "is_valid_transitive": True,
                "prompt": prompt,
                "target": A,
                "foil": C,
                "target_token": " " + A,
                "foil_token": " " + C
            })
            global_id += 1

        # 2. Reverse Transitive (Valid: B > A, C > B => C > A)
        for A, B, C in triples:
            prompt = f"Premise: {B} {verb} {A}. {C} {verb} {B}. Question: Who is {rel}, {A} or {C}? Answer:"
            dataset.append({
                "id": global_id,
                "domain": dom_key,
                "task_type": "transitive_reverse",
                "is_valid_transitive": True,
                "prompt": prompt,
                "target": C,
                "foil": A,
                "target_token": " " + C,
                "foil_token": " " + A
            })
            global_id += 1

        # 3. Matched Non-Transitive Control (Invalid: A > B, C > B => common target)
        for A, B, C in triples:
            prompt = f"Premise: {A} {verb} {B}. {C} {verb} {B}. Question: Who is {rel}, {A} or {C}? Answer:"
            dataset.append({
                "id": global_id,
                "domain": dom_key,
                "task_type": "common_target_control",
                "is_valid_transitive": False,
                "prompt": prompt,
                "target": A,
                "foil": C,
                "target_token": " " + A,
                "foil_token": " " + C
            })
            global_id += 1

    return dataset

if __name__ == "__main__":
    data = generate_bench_006_transitive()
    print(f"Generated {len(data)} total instances across 5 disjoint domains.")
    for d in data[:6]:
        print(f"[{d['domain']} | {d['task_type']}] Target: {d['target']} | Foil: {d['foil']}")
        print(f"Prompt: {d['prompt']}\n")
