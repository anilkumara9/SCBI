"""
BENCH-003-TEMPLATES: Template Transfer & Surface Order Permutation Benchmark for SCBI.

Evaluates whether autonomous SCBI transfers across:
1. Surface Order Permutation:
   - 50% Target-First: [Target Evidence] -> [Distractor Evidence] -> [Query]
   - 50% Distractor-First: [Distractor Evidence] -> [Target Evidence] -> [Query]
2. Lexical & Structural Diversification:
   - Varied natural markers ("Fact/Note", "Context/Meanwhile", "Record/Incident")
   - Pure natural prose without artificial header tags ("Meanwhile...", "In contrast...")

Returns structured instances with explicit character substrings for target and distractor
evidence to enable position-independent subspace extraction.
"""

import random

def generate_bench_003_templates(n_instances=100, seed=250):
    rng = random.Random(seed)

    domains = [
        # Domain 1: Spatial Location
        {
            "premise_templates": [
                "The key is inside the {target} box.",
                "The documents are stored in the {target} cabinet.",
                "The treasure is hidden in the {target} chest.",
                "The passport is kept inside the {target} drawer."
            ],
            "pos_templates": [
                "The key is placed inside the {target} box.",
                "The documents are located in the {target} cabinet.",
                "The treasure is concealed in the {target} chest.",
                "The passport is stored inside the {target} drawer."
            ],
            "neg_templates": [
                "The key is inside the {counter} box.",
                "The documents are stored in the {counter} cabinet.",
                "The treasure is hidden in the {counter} chest.",
                "The passport is kept inside the {counter} drawer."
            ],
            "distractor_templates": [
                "The {distractor} box contains an old watch.",
                "The {distractor} cabinet holds empty folders.",
                "The {distractor} chest contains silver coins.",
                "The {distractor} drawer holds office stationery."
            ],
            "query_templates": [
                "Where is the key? The key is in the",
                "Where are the documents? The documents are in the",
                "Where is the treasure? The treasure is in the",
                "Where is the passport? The passport is in the"
            ],
            "targets": ["blue", "wooden", "iron", "metal", "black", "leather", "golden", "stone"],
            "distractors": ["red", "plastic", "bronze", "glass", "white", "cloth", "silver", "brick"],
            "counters": ["green", "steel", "copper", "clay", "yellow", "paper", "diamond", "marble"]
        },
        # Domain 2: Biographical Travel / Residence
        {
            "premise_templates": [
                "Alice traveled directly to {target}.",
                "David relocated his family to {target}.",
                "Elena booked an airline ticket to {target}.",
                "Arthur established his permanent residence in {target}."
            ],
            "pos_templates": [
                "Alice took a flight to {target}.",
                "David moved his family to {target}.",
                "Elena bought an air ticket to {target}.",
                "Arthur made his home in {target}."
            ],
            "neg_templates": [
                "Alice traveled directly to {counter}.",
                "David relocated his family to {counter}.",
                "Elena booked an airline ticket to {counter}.",
                "Arthur established his permanent residence in {counter}."
            ],
            "distractor_templates": [
                "Bob decided to stay in {distractor}.",
                "George spent his vacation in {distractor}.",
                "Fiona canceled her trip to {distractor}.",
                "Henry visited friends in {distractor}."
            ],
            "query_templates": [
                "Where did Alice travel? Alice traveled to",
                "Where did David relocate? David relocated to",
                "Where did Elena book a ticket to? Elena booked to",
                "Where does Arthur reside? Arthur resides in"
            ],
            "targets": ["Paris", "Tokyo", "Rome", "Berlin", "Madrid", "Cairo", "Vienna", "Dublin"],
            "distractors": ["London", "Boston", "Oslo", "Prague", "Lisbon", "Athens", "Geneva", "Warsaw"],
            "counters": ["Sydney", "Toronto", "Seoul", "Venice", "Moscow", "Zurich", "Bangkok", "Munich"]
        },
        # Domain 3: Temporal Events
        {
            "premise_templates": [
                "The annual conference is scheduled for {target}.",
                "The scientific experiment will take place on {target}.",
                "The final championship match occurs on {target}.",
                "The product announcement is slated for {target}."
            ],
            "pos_templates": [
                "The annual conference will occur on {target}.",
                "The scientific experiment is set for {target}.",
                "The final championship match will happen on {target}.",
                "The product announcement is planned for {target}."
            ],
            "neg_templates": [
                "The annual conference is scheduled for {counter}.",
                "The scientific experiment will take place on {counter}.",
                "The final championship match occurs on {counter}.",
                "The product announcement is slated for {counter}."
            ],
            "distractor_templates": [
                "The hotel ballroom was reserved on {distractor}.",
                "The preliminary workshop took place on {distractor}.",
                "The ticket sales concluded on {distractor}.",
                "The press briefing was held on {distractor}."
            ],
            "query_templates": [
                "When is the conference? The conference is on",
                "When is the experiment? The experiment is on",
                "When is the championship? The championship is on",
                "When is the product announcement? The announcement is on"
            ],
            "targets": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "distractors": ["Saturday", "Sunday", "Thursday", "Monday", "Wednesday"],
            "counters": ["Friday", "Monday", "Tuesday", "Saturday", "Sunday"]
        },
        # Domain 4: Professional Specialization
        {
            "premise_templates": [
                "Dr. Smith conducts research in {target}.",
                "Professor Evans teaches university courses in {target}.",
                "Dr. Miller is a world-renowned specialist in {target}.",
                "Laura completed her doctoral dissertation in {target}."
            ],
            "pos_templates": [
                "Dr. Smith carries out scientific studies in {target}.",
                "Professor Evans lectures students in {target}.",
                "Dr. Miller is an internationally recognized expert in {target}.",
                "Laura wrote her doctoral thesis in {target}."
            ],
            "neg_templates": [
                "Dr. Smith conducts research in {counter}.",
                "Professor Evans teaches university courses in {counter}.",
                "Dr. Miller is a world-renowned specialist in {counter}.",
                "Laura completed her doctoral dissertation in {counter}."
            ],
            "distractor_templates": [
                "Dr. Taylor enjoys practicing {distractor} in his free time.",
                "Professor Clark frequently reads articles about {distractor}.",
                "Dr. White has a personal interest in {distractor}.",
                "Laura occasionally volunteers at a clinic for {distractor}."
            ],
            "query_templates": [
                "What is Dr. Smith's research field? Dr. Smith specializes in",
                "What does Professor Evans teach? Professor Evans teaches",
                "What is Dr. Miller's field? Dr. Miller specializes in",
                "What was Laura's doctoral field? Laura completed her dissertation in"
            ],
            "targets": ["physics", "biology", "chemistry", "psychology", "economics", "astronomy"],
            "distractors": ["philosophy", "sociology", "history", "literature", "geology", "botany"],
            "counters": ["mathematics", "genetics", "neuroscience", "anthropology", "linguistics", "ecology"]
        },
        # Domain 5: Object Attributes & Colors
        {
            "premise_templates": [
                "The sports car in the garage is painted {target}.",
                "The silk gown on the mannequin is {target}.",
                "The ceramic vase on the mantelpiece is {target}.",
                "The leather sofa in the living room is {target}."
            ],
            "pos_templates": [
                "The sports car in the garage has a coat of {target} paint.",
                "The silk gown on the mannequin has a rich {target} shade.",
                "The ceramic vase on the mantelpiece features a {target} finish.",
                "The leather sofa in the living room has {target} upholstery."
            ],
            "neg_templates": [
                "The sports car in the garage is painted {counter}.",
                "The silk gown on the mannequin is {counter}.",
                "The ceramic vase on the mantelpiece is {counter}.",
                "The leather sofa in the living room is {counter}."
            ],
            "distractor_templates": [
                "The vintage motorcycle outside is {distractor}.",
                "The wool scarf nearby is {distractor}.",
                "The wooden coffee table next to it is {distractor}.",
                "The decorative curtains are {distractor}."
            ],
            "query_templates": [
                "What color is the sports car? The sports car is",
                "What color is the silk gown? The silk gown is",
                "What color is the ceramic vase? The ceramic vase is",
                "What color is the leather sofa? The leather sofa is"
            ],
            "targets": ["blue", "yellow", "purple", "orange", "silver", "gold"],
            "distractors": ["black", "white", "brown", "gray", "beige", "navy"],
            "counters": ["green", "pink", "crimson", "cyan", "bronze", "violet"]
        }
    ]

    # Framing formats
    # Formats provide both Target-First and Distractor-First variants with novel markers
    framing_styles = [
        # Style 0: Fact / Note
        {
            "type": "fact_note",
            "target_first": "Fact: {prem} Note: {dist} Q: {query}",
            "distractor_first": "Note: {dist} Fact: {prem} Q: {query}",
            "pos_tf": "Fact: {pos} Note: {dist} Q: {query}",
            "pos_df": "Note: {dist} Fact: {pos} Q: {query}",
            "neg_tf": "Fact: {neg} Note: {dist} Q: {query}",
            "neg_df": "Note: {dist} Fact: {neg} Q: {query}",
        },
        # Style 1: Context / Meanwhile
        {
            "type": "context_meanwhile",
            "target_first": "Context: {prem} Meanwhile, {dist} Query: {query}",
            "distractor_first": "Context: {dist} In addition, {prem} Query: {query}",
            "pos_tf": "Context: {pos} Meanwhile, {dist} Query: {query}",
            "pos_df": "Context: {dist} In addition, {pos} Query: {query}",
            "neg_tf": "Context: {neg} Meanwhile, {dist} Query: {query}",
            "neg_df": "Context: {dist} In addition, {neg} Query: {query}",
        },
        # Style 2: Record / Incident
        {
            "type": "record_incident",
            "target_first": "Record: {prem} Incident: {dist} Prompt: {query}",
            "distractor_first": "Incident: {dist} Record: {prem} Prompt: {query}",
            "pos_tf": "Record: {pos} Incident: {dist} Prompt: {query}",
            "pos_df": "Incident: {dist} Record: {pos} Prompt: {query}",
            "neg_tf": "Record: {neg} Incident: {dist} Prompt: {query}",
            "neg_df": "Incident: {dist} Record: {neg} Prompt: {query}",
        },
        # Style 3: Pure Natural Prose (No artificial headers)
        {
            "type": "natural_prose",
            "target_first": "{prem} Meanwhile, {dist} {query}",
            "distractor_first": "{dist} In contrast, {prem} {query}",
            "pos_tf": "{pos} Meanwhile, {dist} {query}",
            "pos_df": "{dist} In contrast, {pos} {query}",
            "neg_tf": "{neg} Meanwhile, {dist} {query}",
            "neg_df": "{dist} In contrast, {neg} {query}",
        }
    ]

    dataset = []
    for i in range(n_instances):
        d_idx = i % len(domains)
        dom = domains[d_idx]
        t_idx = (i // len(domains)) % len(dom["premise_templates"])

        target = rng.choice(dom["targets"])
        avail_dist = [d for d in dom["distractors"] if d != target]
        distractor = rng.choice(avail_dist)
        avail_counter = [c for c in dom["counters"] if c != target and c != distractor]
        counter = rng.choice(avail_counter)

        prem_base = dom["premise_templates"][t_idx].format(target=target)
        prem_pos = dom["pos_templates"][t_idx].format(target=target)
        prem_neg = dom["neg_templates"][t_idx].format(counter=counter)
        dist = dom["distractor_templates"][t_idx].format(distractor=distractor)
        query = dom["query_templates"][t_idx]

        # Determine surface order: 50% target-first, 50% distractor-first
        order = "target_first" if (i % 2 == 0) else "distractor_first"
        style = framing_styles[(i // 2) % len(framing_styles)]

        if order == "target_first":
            base_text = style["target_first"].format(prem=prem_base, dist=dist, query=query)
            pos_text = style["pos_tf"].format(pos=prem_pos, dist=dist, query=query)
            neg_text = style["neg_tf"].format(neg=prem_neg, dist=dist, query=query)
            target_evidence_text = prem_base
            distractor_evidence_text = dist
        else:
            base_text = style["distractor_first"].format(prem=prem_base, dist=dist, query=query)
            pos_text = style["pos_df"].format(pos=prem_pos, dist=dist, query=query)
            neg_text = style["neg_df"].format(neg=prem_neg, dist=dist, query=query)
            target_evidence_text = prem_base
            distractor_evidence_text = dist

        dataset.append({
            "id": i,
            "domain": d_idx,
            "order": order,
            "style": style["type"],
            "base": base_text,
            "pos": pos_text,
            "neg": neg_text,
            "target_evidence_text": target_evidence_text,
            "distractor_evidence_text": distractor_evidence_text,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor,
            "counter": counter
        })

    return dataset

if __name__ == "__main__":
    data = generate_bench_003_templates(100, seed=250)
    print(f"Generated {len(data)} instances for BENCH-003-TEMPLATES.")
    print("\nSample Instance 0 (Target-First):")
    print("Base:", data[0]["base"])
    print("Order:", data[0]["order"], "| Style:", data[0]["style"])
    print("Target Evidence:", data[0]["target_evidence_text"])
    print("Distractor Evidence:", data[0]["distractor_evidence_text"])
    print("Target Token:", repr(data[0]["target_token"]))

    print("\nSample Instance 1 (Distractor-First):")
    print("Base:", data[1]["base"])
    print("Order:", data[1]["order"], "| Style:", data[1]["style"])
    print("Target Evidence:", data[1]["target_evidence_text"])
    print("Distractor Evidence:", data[1]["distractor_evidence_text"])
    print("Target Token:", repr(data[1]["target_token"]))
