"""
BENCH-002-NL: Controlled Natural-Language Distractor Benchmark for SCBI.
Implements 100 controlled instances across 5 relational categories:
- Spatial Location (boxes, rooms, containers)
- Biographical Origin / Residence (cities, countries)
- Temporal Events (days of week, months)
- Professional Specialization (academic / medical fields)
- Entity Attributes (colors, materials, sizes)

Each instance has strictly pre-registered:
- base (x): Premise + Distractor + Question + Prompt
- pos (x+): Meaning-preserving predicate paraphrase of Premise
- neg (x-): Semantic counterfactual entity replacement in Premise
- target_token: Expected next-token continuation
- distractor_token: Competing distractor continuation
"""

def generate_bench_002_nl(n_instances=100, seed=42):
    import random
    rng = random.Random(seed)
    
    # 5 relational domain templates:
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
                "Question: Where is the key? Answer: The key is in the",
                "Question: Where are the documents? Answer: The documents are in the",
                "Question: Where is the treasure? Answer: The treasure is in the",
                "Question: Where is the passport? Answer: The passport is in the"
            ],
            "targets": ["blue", "wooden", "iron", "metal", "black", "leather", "golden", "stone"],
            "distractors": ["red", "plastic", "bronze", "glass", "white", "cloth", "silver", "brick"],
            "counters": ["green", "steel", "copper", "clay", "yellow", "paper", "diamond", "marble"]
        },
        # Domain 2: Biographical Origin / Travel
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
                "Question: Where did Alice travel? Answer: Alice traveled to",
                "Question: Where did David relocate? Answer: David relocated to",
                "Question: Where did Elena book a ticket to? Answer: Elena booked to",
                "Question: Where does Arthur reside? Answer: Arthur resides in"
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
                "Question: When is the conference? Answer: The conference is on",
                "Question: When is the experiment? Answer: The experiment is on",
                "Question: When is the championship? Answer: The championship is on",
                "Question: When is the product announcement? Answer: The announcement is on"
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
                "Question: What is Dr. Smith's research field? Answer: Dr. Smith specializes in",
                "Question: What does Professor Evans teach? Answer: Professor Evans teaches",
                "Question: What is Dr. Miller's field? Answer: Dr. Miller specializes in",
                "Question: What was Laura's doctoral field? Answer: Laura completed her dissertation in"
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
                "Question: What color is the sports car? Answer: The sports car is",
                "Question: What color is the silk gown? Answer: The silk gown is",
                "Question: What color is the ceramic vase? Answer: The ceramic vase is",
                "Question: What color is the leather sofa? Answer: The leather sofa is"
            ],
            "targets": ["blue", "yellow", "purple", "orange", "silver", "gold"],
            "distractors": ["black", "white", "brown", "gray", "beige", "navy"],
            "counters": ["green", "pink", "crimson", "cyan", "bronze", "violet"]
        }
    ]
    
    dataset = []
    for i in range(n_instances):
        d_idx = i % len(domains)
        dom = domains[d_idx]
        t_idx = (i // len(domains)) % len(dom["premise_templates"])
        
        target = rng.choice(dom["targets"])
        # Ensure distractor != target
        avail_dist = [d for d in dom["distractors"] if d != target]
        distractor = rng.choice(avail_dist)
        # Ensure counter != target and counter != distractor
        avail_counter = [c for c in dom["counters"] if c != target and c != distractor]
        counter = rng.choice(avail_counter)
        
        prem_base = dom["premise_templates"][t_idx].format(target=target)
        prem_pos = dom["pos_templates"][t_idx].format(target=target)
        prem_neg = dom["neg_templates"][t_idx].format(counter=counter)
        
        dist = dom["distractor_templates"][t_idx].format(distractor=distractor)
        query = dom["query_templates"][t_idx]
        
        base_text = f"Premise: {prem_base} Distractor: {dist} {query}"
        pos_text = f"Premise: {prem_pos} Distractor: {dist} {query}"
        neg_text = f"Premise: {prem_neg} Distractor: {dist} {query}"
        
        dataset.append({
            "id": i,
            "domain": d_idx,
            "base": base_text,
            "pos": pos_text,
            "neg": neg_text,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor,
            "counter": counter
        })
        
    return dataset

if __name__ == "__main__":
    data = generate_bench_002_nl(100, seed=42)
    print(f"Generated {len(data)} instances for BENCH-002-NL.")
    print("\nSample Instance 0:")
    print("Base:", data[0]["base"])
    print("Pos: ", data[0]["pos"])
    print("Neg: ", data[0]["neg"])
    print("Target token:", repr(data[0]["target_token"]))
