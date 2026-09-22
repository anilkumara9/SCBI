import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-160m")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-160m")

tests = [
    ("Hierarchy", "Premise: An eagle is an avian creature having feathers. Distractor: A lizard is a reptile having scales. Question: What does an eagle have? Answer: An eagle has", "feathers"),
    ("Temporal", "Chronology: First event was Monday. Second event was Wednesday. Third scheduled event was Friday. Earlier event was Monday. Question: What was the third event? Answer: The third event was", "Friday"),
    ("Causal", "Process log: The primary reaction produced smoke. A secondary side-effect caused water. Question: What did the primary reaction produce? Answer: The primary reaction produced", "smoke"),
    ("Interaction", "Reaction log: Single chemicals remain inert. Combining acid and base produces salt. Heating produces fumes. Question: What does combining acid and base produce? Answer: Combining acid and base produces", "salt"),
    ("Exclusion", "Selection rule: Options are gold and silver. The rule forbids gold. Question: Which option is accepted? Answer: The accepted option is", "silver"),
    ("Distractor", "Fact: The key is inside the blue box. Note: The red box contains coins. Question: Where is the key? Answer: The key is in the", "blue")
]

for name, prompt, target in tests:
    t_id = tokenizer.encode(" " + target)[0]
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    with torch.no_grad():
        logits = model(input_ids=input_ids).logits[0, -1, :]
    top5 = torch.topk(logits, k=5).indices.tolist()
    top5_str = [tokenizer.decode([tok]) for tok in top5]
    pred_top = top5[0]
    print(f"[{name}]")
    print(f"Target: '{target}' (ID: {t_id}) | Top 1 Pred: '{tokenizer.decode([pred_top])}' (ID: {pred_top}) | Match: {pred_top == t_id}")
    print(f"Top 5: {top5_str}")
    print("-" * 50)
