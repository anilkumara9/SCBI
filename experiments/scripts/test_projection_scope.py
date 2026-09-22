import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')
model.eval()

prompt = 'Premise: The key is inside the blue box. Distractor: The red box contains a watch. Question: Where is the key? Answer: The key is in the'
inputs = tokenizer(prompt, return_tensors='pt')
seq_len = inputs['input_ids'].shape[1]

with torch.no_grad():
    out = model(**inputs, output_hidden_states=True)
    h_layer4 = out.hidden_states[4][0]

# Candidate 1: Distractor token SVD
v_dist = torch.linalg.svd(h_layer4[10:20], full_matrices=False).Vh[:2].T
P_dist = torch.eye(768) - v_dist @ v_dist.T

# Candidate 2: Premise token SVD
v_prem = torch.linalg.svd(h_layer4[0:10], full_matrices=False).Vh[:2].T
P_prem = torch.eye(768) - v_prem @ v_prem.T

# Candidate 3: Random Orthogonal
q_rand, _ = torch.linalg.qr(torch.randn(768, 2))
P_rand = torch.eye(768) - q_rand @ q_rand.T

def hook_final_token(P):
    def hook_fn(module, input, output):
        h = output[0].clone()
        h[:, -1, :] = torch.matmul(h[:, -1, :], P.T)
        return (h, *output[1:])
    return hook_fn

print('--- FINAL TOKEN PROJECTION ---')
for name, P in [('Identity', torch.eye(768)), ('P_prem', P_prem), ('P_dist', P_dist), ('P_rand', P_rand)]:
    if name == 'Identity':
        pred = tokenizer.decode([torch.argmax(out.logits[0, -1])])
        p_blue = torch.softmax(out.logits[0, -1], dim=-1)[tokenizer(' blue')['input_ids'][0]].item()
    else:
        handle = model.transformer.h[3].register_forward_hook(hook_final_token(P))
        with torch.no_grad():
            out_p = model(**inputs)
        handle.remove()
        pred = tokenizer.decode([torch.argmax(out_p.logits[0, -1])])
        p_blue = torch.softmax(out_p.logits[0, -1], dim=-1)[tokenizer(' blue')['input_ids'][0]].item()
    print(f'{name:<10}: pred=\"{pred}\", P(blue)={p_blue:.4f}')

def hook_all_tokens(P):
    def hook_fn(module, input, output):
        h = output[0].clone()
        h = torch.matmul(h, P.T)
        return (h, *output[1:])
    return hook_fn

print('\n--- ALL TOKENS PROJECTION ---')
for name, P in [('Identity', torch.eye(768)), ('P_prem', P_prem), ('P_dist', P_dist), ('P_rand', P_rand)]:
    if name == 'Identity':
        pred = tokenizer.decode([torch.argmax(out.logits[0, -1])])
        p_blue = torch.softmax(out.logits[0, -1], dim=-1)[tokenizer(' blue')['input_ids'][0]].item()
    else:
        handle = model.transformer.h[3].register_forward_hook(hook_all_tokens(P))
        with torch.no_grad():
            out_p = model(**inputs)
        handle.remove()
        pred = tokenizer.decode([torch.argmax(out_p.logits[0, -1])])
        p_blue = torch.softmax(out_p.logits[0, -1], dim=-1)[tokenizer(' blue')['input_ids'][0]].item()
    print(f'{name:<10}: pred=\"{pred}\", P(blue)={p_blue:.4f}')
