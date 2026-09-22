import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from experiments.benchmarks.bench_005_hidden_geometry import generate_bench_005_hidden_geometry

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-160m")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-160m")

bench = generate_bench_005_hidden_geometry(n_per_geometry=2, seed=500)
for inst in bench:
    prompt = inst["base"]
    t_str = inst["target"].strip()
    t_enc = tokenizer.encode(" " + t_str)
    t_id = t_enc[0]
    
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    with torch.no_grad():
        logits = model(input_ids=input_ids).logits[0, -1, :]
    top5 = torch.topk(logits, k=5).indices.tolist()
    top5_str = [tokenizer.decode([tok]) for tok in top5]
    print(f"Prompt: {prompt[-50:]}")
    print(f"Target: '{t_str}' (ID: {t_id}), Decoded ID: '{tokenizer.decode([t_id])}'")
    print(f"Top 5 preds: {top5_str}")
    print("-" * 50)
