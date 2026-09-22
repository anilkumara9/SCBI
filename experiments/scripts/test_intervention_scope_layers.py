import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')
model.eval()

data = generate_bench_002_nl(5, seed=42)

for inst in data[:2]:
    prompt = inst['base']
    target = inst['target_token']
    inputs = tokenizer(prompt, return_tensors='pt')
    T = inputs['input_ids'].shape[1]
    
    with torch.no_grad():
        out0 = model(**inputs, output_hidden_states=True)
    base_pred = tokenizer.decode([torch.argmax(out0.logits[0, -1])])
    print(f"\nInstance {inst['id']}: target={repr(target)}, base_pred={repr(base_pred)}")
    
    for l in [2, 4, 6, 8, 10]:
        h_l = out0.hidden_states[l][0] # [T, 768]
        # Temporal quartile 1: [0, T//4]
        q1 = h_l[:T//4]
        v1 = torch.linalg.svd(q1, full_matrices=False).Vh[:2].T
        
        # Test 1: All-token intervention (non-materialized)
        def hook_all(module, input, output):
            h = output[0].clone()
            h_proj = h - torch.matmul(torch.matmul(h, v1), v1.T)
            return (h_proj, *output[1:])
            
        handle = model.transformer.h[l-1].register_forward_hook(hook_all)
        with torch.no_grad():
            out_all = model(**inputs)
        handle.remove()
        pred_all = tokenizer.decode([torch.argmax(out_all.logits[0, -1])])
        
        # Test 2: Final-token intervention (non-materialized)
        def hook_final(module, input, output):
            h = output[0].clone()
            h[:, -1, :] = h[:, -1, :] - torch.matmul(torch.matmul(h[:, -1, :], v1), v1.T)
            return (h, *output[1:])
            
        handle = model.transformer.h[l-1].register_forward_hook(hook_final)
        with torch.no_grad():
            out_final = model(**inputs)
        handle.remove()
        pred_final = tokenizer.decode([torch.argmax(out_final.logits[0, -1])])
        
        print(f"  L={l}: All-token pred={repr(pred_all):<12} | Final-token pred={repr(pred_final):<12}")
