"""
BENCH-004-TRANSFER: Cross-Task & Unseen Domain Generalization Benchmark for SCBI.

Evaluates whether autonomous SCBI transfers zero-shot to 5 completely new relational domains
with unseen entity types, relational predicates, and vocabulary tokens:
1. Corporate Ownership & Subsidiaries
2. Historical Imperial Capitols & Seats of Rule
3. Biochemical Enzymes & Specific Substrates
4. Material Craft & Artisan Media
5. Athletic Tournaments & Championship Awards

Features:
- Paired Counterfactual Construction (Base x, Positive x+, Negative x-)
- Explicit Character Spans for Target Evidence and Distractor Evidence
- 50/50 Surface Order Permutation (Target-First vs. Distractor-First)
- Diverse Natural Framing (Fact/Note, Context/Meanwhile, Natural Prose)
"""

import random

def generate_bench_004_transfer(n_instances=100, seed=350):
    rng = random.Random(seed)

    domains = [
        # Domain 1: Corporate Ownership / Parent Company
        {
            "name": "corporate_ownership",
            "premise_templates": [
                "Acme Corp operates as a major subsidiary of {target}.",
                "Vortex Systems is fully owned and directed by {target}.",
                "Nexus Technologies was formally acquired by {target}.",
                "Summit Media operates under the corporate umbrella of {target}."
            ],
            "pos_templates": [
                "Acme Corp is a recognized business unit of {target}.",
                "Vortex Systems is controlled and managed by {target}.",
                "Nexus Technologies belongs directly to {target}.",
                "Summit Media is owned and operated by {target}."
            ],
            "neg_templates": [
                "Acme Corp operates as a major subsidiary of {counter}.",
                "Vortex Systems is fully owned and directed by {counter}.",
                "Nexus Technologies was formally acquired by {counter}.",
                "Summit Media operates under the corporate umbrella of {counter}."
            ],
            "distractor_templates": [
                "Beta LLC was recently purchased by {distractor}.",
                "Delta Labs formed an investment alliance with {distractor}.",
                "Apex Capital merged operations with {distractor}.",
                "Pinnacle Group established a joint venture with {distractor}."
            ],
            "query_templates": [
                "Which company owns Acme Corp? Acme Corp is owned by",
                "Who directs Vortex Systems? Vortex Systems is directed by",
                "Who acquired Nexus Technologies? Nexus Technologies was acquired by",
                "Who operates Summit Media? Summit Media is operated by"
            ],
            "targets": ["Apple", "Google", "Microsoft", "Amazon", "Sony", "Oracle", "Intel", "Adobe"],
            "distractors": ["Meta", "Nvidia", "Samsung", "Cisco", "IBM", "Tesla", "Qualcomm", "Spotify"],
            "counters": ["Baidu", "Tencent", "Alibaba", "Yahoo", "Dell", "HP", "Ebay", "Uber"]
        },
        # Domain 2: Historical Imperial Capital / Seat of Rule
        {
            "name": "imperial_seat",
            "premise_templates": [
                "Emperor Marcus ruled the ancient empire from {target}.",
                "Queen Isabella reigned over the kingdom from {target}.",
                "King Philip commanded the royal forces from {target}.",
                "Sultan Mehmed governed the vast territories from {target}."
            ],
            "pos_templates": [
                "Emperor Marcus maintained his imperial throne in {target}.",
                "Queen Isabella directed sovereign affairs from {target}.",
                "King Philip oversaw the crown council from {target}.",
                "Sultan Mehmed presided over the imperial palace in {target}."
            ],
            "neg_templates": [
                "Emperor Marcus ruled the ancient empire from {counter}.",
                "Queen Isabella reigned over the kingdom from {counter}.",
                "King Philip commanded the royal forces from {counter}.",
                "Sultan Mehmed governed the vast territories from {counter}."
            ],
            "distractor_templates": [
                "General Claudius established a frontier outpost in {distractor}.",
                "Duke Raymond constructed a military garrison in {distractor}.",
                "Baron Walter fought a provincial skirmish in {distractor}.",
                "Countess Beatrice inspected a trading port in {distractor}."
            ],
            "query_templates": [
                "Where did Emperor Marcus rule from? Emperor Marcus ruled from",
                "Where did Queen Isabella reign from? Queen Isabella reigned from",
                "Where did King Philip command from? King Philip commanded from",
                "Where did Sultan Mehmed govern from? Sultan Mehmed governed from"
            ],
            "targets": ["Rome", "Ravenna", "Constantinople", "Milan", "Venice", "Florence", "Naples", "Toledo"],
            "distractors": ["Carthage", "Alexandria", "Antioch", "Corinth", "Syracuse", "Palermo", "Verona", "Genoa"],
            "counters": ["Granada", "Cordoba", "Seville", "Valencia", "Burgos", "Leon", "Salamanca", "Cadiz"]
        },
        # Domain 3: Biochemical Enzyme / Specific Substrate
        {
            "name": "biochemical_substrate",
            "premise_templates": [
                "The digestive enzyme amylase specifically hydrolyzes {target}.",
                "The metabolic enzyme lactase specifically degrades {target}.",
                "The pancreatic enzyme lipase breaks down dietary {target}.",
                "The cellular enzyme catalase rapidly decomposes {target}."
            ],
            "pos_templates": [
                "The digestive enzyme amylase catalyzes the digestion of {target}.",
                "The metabolic enzyme lactase breaks the chemical bonds of {target}.",
                "The pancreatic enzyme lipase digests molecules of {target}.",
                "The cellular enzyme catalase neutralizes molecules of {target}."
            ],
            "neg_templates": [
                "The digestive enzyme amylase specifically hydrolyzes {counter}.",
                "The metabolic enzyme lactase specifically degrades {counter}.",
                "The pancreatic enzyme lipase breaks down dietary {counter}.",
                "The cellular enzyme catalase rapidly decomposes {counter}."
            ],
            "distractor_templates": [
                "The stomach protease pepsin actively degrades {distractor}.",
                "The alkaline reagent reacts vigorously with {distractor}.",
                "The chemical buffer stabilizes particles of {distractor}.",
                "The synthetic solvent dissolves residues of {distractor}."
            ],
            "query_templates": [
                "What does amylase hydrolyze? Amylase hydrolyzes",
                "What does lactase degrade? Lactase degrades",
                "What does lipase break down? Lipase breaks down",
                "What does catalase decompose? Catalase decomposes"
            ],
            "targets": ["starch", "lactose", "lipids", "peroxide", "sucrose", "maltose", "proteins", "cellulose"],
            "distractors": ["protein", "glucose", "fructose", "peptides", "albumin", "gelatin", "casein", "keratin"],
            "counters": ["glycogen", "dextrin", "collagen", "elastin", "chitin", "fibrin", "myosin", "insulin"]
        },
        # Domain 4: Material Craft / Artisan Medium
        {
            "name": "artisan_craft",
            "premise_templates": [
                "Fine porcelain sculpture is handcrafted from pure {target}.",
                "Ancient terracotta pottery is molded from red {target}.",
                "Traditional Damascus blades are forged from high-carbon {target}.",
                "Classical mosaic flooring is assembled from polished {target}."
            ],
            "pos_templates": [
                "Fine porcelain sculpture is shaped using white {target}.",
                "Ancient terracotta pottery is formed using baked {target}.",
                "Traditional Damascus blades are crafted using folded {target}.",
                "Classical mosaic flooring is created using cut {target}."
            ],
            "neg_templates": [
                "Fine porcelain sculpture is handcrafted from pure {counter}.",
                "Ancient terracotta pottery is molded from red {counter}.",
                "Traditional Damascus blades are forged from high-carbon {counter}.",
                "Classical mosaic flooring is assembled from polished {counter}."
            ],
            "distractor_templates": [
                "Modern industrial packaging is manufactured from corrugated {distractor}.",
                "Cheap novelty souvenirs are cast in synthetic {distractor}.",
                "Reinforced structural panels are molded from composite {distractor}.",
                "Disposable dining cutlery is stamped out of rigid {distractor}."
            ],
            "query_templates": [
                "What is porcelain handcrafted from? Porcelain is handcrafted from",
                "What is terracotta molded from? Terracotta is molded from",
                "What are Damascus blades forged from? Damascus blades are forged from",
                "What is mosaic flooring assembled from? Mosaic flooring is assembled from"
            ],
            "targets": ["clay", "earth", "steel", "marble", "bronze", "copper", "silver", "glass"],
            "distractors": ["plastic", "paper", "cardboard", "resin", "rubber", "foam", "vinyl", "nylon"],
            "counters": ["stone", "wood", "iron", "gold", "granite", "quartz", "plaster", "lead"]
        },
        # Domain 5: Athletic Tournament / Championship Award
        {
            "name": "championship_award",
            "premise_templates": [
                "The championship soccer team celebrated and hoisted the golden {target}.",
                "The victorious marathon runner proudly displayed the winner's {target}.",
                "The tournament tennis champion walked off court carrying the coveted {target}.",
                "The regatta winner was officially awarded the ceremonial {target}."
            ],
            "pos_templates": [
                "The championship soccer team celebrated and lifted the winner's {target}.",
                "The victorious marathon runner accepted the gold {target}.",
                "The tournament tennis champion received the victor's {target}.",
                "The regatta winner brought home the official {target}."
            ],
            "neg_templates": [
                "The championship soccer team celebrated and hoisted the golden {counter}.",
                "The victorious marathon runner proudly displayed the winner's {counter}.",
                "The tournament tennis champion walked off court carrying the coveted {counter}.",
                "The regatta winner was officially awarded the ceremonial {counter}."
            ],
            "distractor_templates": [
                "The runner-up athletic club received a participation {distractor}.",
                "The third-place competitor was handed a consolation {distractor}.",
                "The tournament referee wore an honorary {distractor}.",
                "The organizing committee distributed a promotional {distractor}."
            ],
            "query_templates": [
                "What did the championship team hoist? The championship team hoisted the",
                "What did the marathon runner display? The marathon runner displayed the",
                "What did the tennis champion carry? The tennis champion carried the",
                "What was the regatta winner awarded? The regatta winner was awarded the"
            ],
            "targets": ["trophy", "cup", "medal", "shield", "plate", "plaque", "bowl", "crown"],
            "distractors": ["ribbon", "certificate", "badge", "banner", "pennant", "pin", "card", "towel"],
            "counters": ["sash", "belt", "ring", "rosette", "wreath", "scroll", "flag", "medallion"]
        }
    ]

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
        # Style 3: Pure Natural Prose
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

        order = "target_first" if (i % 2 == 0) else "distractor_first"
        style = framing_styles[(i // 2) % len(framing_styles)]

        if order == "target_first":
            base_text = style["target_first"].format(prem=prem_base, dist=dist, query=query)
            pos_text = style["pos_tf"].format(pos=prem_pos, dist=dist, query=query)
            neg_text = style["neg_tf"].format(neg=prem_neg, dist=dist, query=query)
        else:
            base_text = style["distractor_first"].format(prem=prem_base, dist=dist, query=query)
            pos_text = style["pos_df"].format(pos=prem_pos, dist=dist, query=query)
            neg_text = style["neg_df"].format(neg=prem_neg, dist=dist, query=query)

        dataset.append({
            "id": i,
            "domain_name": dom["name"],
            "domain": d_idx,
            "order": order,
            "style": style["type"],
            "base": base_text,
            "pos": pos_text,
            "neg": neg_text,
            "target_evidence_text": prem_base,
            "distractor_evidence_text": dist,
            "target": target,
            "target_token": " " + target,
            "distractor": distractor,
            "distractor_token": " " + distractor,
            "counter": counter
        })

    return dataset

if __name__ == "__main__":
    data = generate_bench_004_transfer(100, seed=350)
    print(f"Generated {len(data)} instances for BENCH-004-TRANSFER.")
    print("\nSample Instance 0 (Corporate Ownership, Target-First):")
    print("Base:", data[0]["base"])
    print("Target Evidence:", data[0]["target_evidence_text"])
    print("Distractor Evidence:", data[0]["distractor_evidence_text"])
    print("Target Token:", repr(data[0]["target_token"]))

    print("\nSample Instance 1 (Imperial Capital, Distractor-First):")
    print("Base:", data[1]["base"])
    print("Target Evidence:", data[1]["target_evidence_text"])
    print("Distractor Evidence:", data[1]["distractor_evidence_text"])
    print("Target Token:", repr(data[1]["target_token"]))
