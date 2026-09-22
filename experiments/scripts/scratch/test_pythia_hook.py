import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

m = AutoModelForCausalLM.from_pretrained('EleutherAI/pythia-160m')
t = AutoTokenizer.from_pretrained('EleutherAI/pythia-160m')
inp = t('Hello world', return_tensors='pt')

def hook(mod, inp, out):
    print('Hook output type:', type(out), 'len:', len(out) if isinstance(out, tuple) else 'tensor')
    h_out = out[0] if isinstance(out, tuple) else out
    print('Hidden states shape:', h_out.shape)

h = m.gpt_neox.layers[7].register_forward_hook(hook)
with torch.no_grad():
    out = m(**inp, output_hidden_states=True)
h.remove()
print('Pythia hook test passed!')
