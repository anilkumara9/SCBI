"""
EXP013 Phase A Pilot: GPT-2 Response Channel Dynamic Range Validation
Measures D_JS and Delta_NLL for semantic-preserving (+) vs. semantic-changing (-) counterfactuals.
Strictly verifies H13-A: D(q(x), q(x+)) < D(q(x), q(x-)) and Delta_NLL(+) < Delta_NLL(-).
"""
import torch
import torch.nn.functional as F
import numpy as np
import hashlib
from transformers import AutoTokenizer, AutoModelForCausalLM

def main():
    print("=" * 70)
    print("EXP013 PHASE A PILOT: PRETRAINED TRANSFORMER RESPONSE CHANNEL")
    print("=" * 70)
    
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    
    # SHA-256 Checksum
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    param_hash = h.hexdigest()
    print(f"[REPRODUCIBILITY] GPT-2 Parameter Hash (SHA-256): {param_hash}")
    
    # Construct 10 controlled natural language premise-distractor triplets
    # Each triplet has:
    # - base: Premise fact + Irrelevant distractor + Query + Target continuation
    # - pos: Semantic-preserving paraphrase of Premise + same distractor + same query
    # - neg: Semantic-changing counterfactual of Premise + same distractor + same query
    triplets = [
        {
            "id": 1,
            "base": "Premise: The key is inside the blue box. Distractor: The red box contains a watch. Question: Where is the key? Answer: The key is in the blue",
            "pos": "Premise: The key is kept in the blue box. Distractor: The red box contains a watch. Question: Where is the key? Answer: The key is in the blue",
            "neg": "Premise: The key is inside the green box. Distractor: The red box contains a watch. Question: Where is the key? Answer: The key is in the blue",
            "target": " box"
        },
        {
            "id": 2,
            "base": "Premise: Alice traveled to Paris. Distractor: Bob stayed in London. Question: Who traveled to Paris? Answer: Alice",
            "pos": "Premise: Alice took a trip to Paris. Distractor: Bob stayed in London. Question: Who traveled to Paris? Answer: Alice",
            "neg": "Premise: Charlie traveled to Paris. Distractor: Bob stayed in London. Question: Who traveled to Paris? Answer: Alice",
            "target": " traveled"
        },
        {
            "id": 3,
            "base": "Premise: The capital of France is Paris. Distractor: Berlin is a city in Germany. Question: What is the capital of France? Answer: The capital is Paris",
            "pos": "Premise: France has its capital in Paris. Distractor: Berlin is a city in Germany. Question: What is the capital of France? Answer: The capital is Paris",
            "neg": "Premise: The capital of France is Lyon. Distractor: Berlin is a city in Germany. Question: What is the capital of France? Answer: The capital is Paris",
            "target": " city"
        },
        {
            "id": 4,
            "base": "Premise: The flight departs on Monday. Distractor: The hotel opens on Wednesday. Question: What day does the flight depart? Answer: Monday",
            "pos": "Premise: The airplane leaves on Monday. Distractor: The hotel opens on Wednesday. Question: What day does the flight depart? Answer: Monday",
            "neg": "Premise: The flight departs on Friday. Distractor: The hotel opens on Wednesday. Question: What day does the flight depart? Answer: Monday",
            "target": " morning"
        },
        {
            "id": 5,
            "base": "Premise: Dr. Smith specializes in cardiology. Distractor: Dr. Brown loves playing chess. Question: What is Dr. Smith's field? Answer: cardiology",
            "pos": "Premise: Dr. Smith is an expert in cardiology. Distractor: Dr. Brown loves playing chess. Question: What is Dr. Smith's field? Answer: cardiology",
            "neg": "Premise: Dr. Smith specializes in dermatology. Distractor: Dr. Brown loves playing chess. Question: What is Dr. Smith's field? Answer: cardiology",
            "target": " and"
        },
        {
            "id": 6,
            "base": "Premise: The code repository is hosted on GitHub. Distractor: The server runs on Ubuntu. Question: Where is the repository hosted? Answer: GitHub",
            "pos": "Premise: The software repo resides on GitHub. Distractor: The server runs on Ubuntu. Question: Where is the repository hosted? Answer: GitHub",
            "neg": "Premise: The code repository is hosted on Bitbucket. Distractor: The server runs on Ubuntu. Question: Where is the repository hosted? Answer: GitHub",
            "target": " platform"
        },
        {
            "id": 7,
            "base": "Premise: Sarah drank orange juice with breakfast. Distractor: Mark prefers black coffee. Question: What beverage did Sarah drink? Answer: orange juice",
            "pos": "Premise: Sarah had orange juice for breakfast. Distractor: Mark prefers black coffee. Question: What beverage did Sarah drink? Answer: orange juice",
            "neg": "Premise: Sarah drank apple cider with breakfast. Distractor: Mark prefers black coffee. Question: What beverage did Sarah drink? Answer: orange juice",
            "target": " today"
        },
        {
            "id": 8,
            "base": "Premise: The package weighs five kilograms. Distractor: The envelope is made of brown paper. Question: How heavy is the package? Answer: five kilograms",
            "pos": "Premise: The parcel has a weight of five kilograms. Distractor: The envelope is made of brown paper. Question: How heavy is the package? Answer: five kilograms",
            "neg": "Premise: The package weighs twenty kilograms. Distractor: The envelope is made of brown paper. Question: How heavy is the package? Answer: five kilograms",
            "target": " exactly"
        },
        {
            "id": 9,
            "base": "Premise: The library opens at nine in the morning. Distractor: The bakery opens at six. Question: When does the library open? Answer: nine",
            "pos": "Premise: The public library begins service at nine in the morning. Distractor: The bakery opens at six. Question: When does the library open? Answer: nine",
            "neg": "Premise: The library opens at noon. Distractor: The bakery opens at six. Question: When does the library open? Answer: nine",
            "target": " am"
        },
        {
            "id": 10,
            "base": "Premise: The museum exhibits ancient Egyptian artifacts. Distractor: The park has a rose garden. Question: What artifacts are in the museum? Answer: Egyptian",
            "pos": "Premise: The museum displays relics from ancient Egypt. Distractor: The park has a rose garden. Question: What artifacts are in the museum? Answer: Egyptian",
            "neg": "Premise: The museum exhibits medieval Japanese armor. Distractor: The park has a rose garden. Question: What artifacts are in the museum? Answer: Egyptian",
            "target": " relics"
        }
    ]

    def compute_metrics(text_base, text_pos, text_neg, target_continuation):
        # 1. Output distribution at final token
        inputs_0 = tokenizer(text_base, return_tensors="pt")
        inputs_p = tokenizer(text_pos, return_tensors="pt")
        inputs_n = tokenizer(text_neg, return_tensors="pt")
        
        with torch.no_grad():
            out_0 = model(**inputs_0)
            out_p = model(**inputs_p)
            out_n = model(**inputs_n)
            
            logits_0 = out_0.logits[0, -1, :]
            logits_p = out_p.logits[0, -1, :]
            logits_n = out_n.logits[0, -1, :]
            
            p0 = F.softmax(logits_0, dim=-1)
            pp = F.softmax(logits_p, dim=-1)
            pn = F.softmax(logits_n, dim=-1)
            
            # Proper Mathematical JS Divergence (summed over vocabulary in nats)
            def js(p, q):
                m = 0.5 * (p + q)
                # In PyTorch F.kl_div, input is log-probs, target is probs: sum(target * (log(target) - input))
                kl_pm = F.kl_div(m.log(), p, reduction="sum")
                kl_qm = F.kl_div(m.log(), q, reduction="sum")
                return (0.5 * (kl_pm + kl_qm)).item()
            
            d_pos_js = js(p0, pp)
            d_neg_js = js(p0, pn)
            
            # 2. Sequence NLL on target continuation
            target_ids = tokenizer(target_continuation, return_tensors="pt")["input_ids"]
            
            def get_seq_nll(prefix_text, target_ids):
                full_ids = tokenizer(prefix_text + target_continuation, return_tensors="pt")["input_ids"]
                prefix_len = tokenizer(prefix_text, return_tensors="pt")["input_ids"].shape[1]
                labels = full_ids.clone()
                labels[0, :prefix_len] = -100 # Mask out prefix
                loss = model(input_ids=full_ids, labels=labels).loss
                return loss.item()
            
            nll_0 = get_seq_nll(text_base, target_ids)
            nll_p = get_seq_nll(text_pos, target_ids)
            nll_n = get_seq_nll(text_neg, target_ids)
            
            delta_nll_pos = abs(nll_p - nll_0)
            delta_nll_neg = abs(nll_n - nll_0)
            
            return {
                "d_pos_js": d_pos_js,
                "d_neg_js": d_neg_js,
                "ratio_js": d_neg_js / max(d_pos_js, 1e-9),
                "delta_nll_pos": delta_nll_pos,
                "delta_nll_neg": delta_nll_neg,
                "ratio_nll": delta_nll_neg / max(delta_nll_pos, 1e-9),
                "nll_0": nll_0,
                "nll_p": nll_p,
                "nll_n": nll_n
            }

    results = []
    print(f"\nEvaluating {len(triplets)} triplets across output JS divergence and Target Sequence NLL...")
    print("-" * 80)
    print(f"{'ID':<4} | {'D_pos (JS)':<12} | {'D_neg (JS)':<12} | {'Ratio JS':<10} | {'dNLL_pos':<10} | {'dNLL_neg':<10} | {'Ratio NLL':<10}")
    print("-" * 80)
    
    for t in triplets:
        res = compute_metrics(t["base"], t["pos"], t["neg"], t["target"])
        results.append(res)
        print(f"{t['id']:<4} | {res['d_pos_js']:<12.6f} | {res['d_neg_js']:<12.6f} | {res['ratio_js']:<10.2f} | {res['delta_nll_pos']:<10.4f} | {res['delta_nll_neg']:<10.4f} | {res['ratio_nll']:<10.2f}")

    print("-" * 80)
    mean_d_pos_js = np.mean([r["d_pos_js"] for r in results])
    mean_d_neg_js = np.mean([r["d_neg_js"] for r in results])
    mean_ratio_js = mean_d_neg_js / max(mean_d_pos_js, 1e-9)
    
    mean_dnll_pos = np.mean([r["delta_nll_pos"] for r in results])
    mean_dnll_neg = np.mean([r["delta_nll_neg"] for r in results])
    mean_ratio_nll = mean_dnll_neg / max(mean_dnll_pos, 1e-9)
    
    print("\nSUMMARY OF PHASE A PILOT FINDINGS:")
    print(f"Mean D_pos (JS):        {mean_d_pos_js:.6f}")
    print(f"Mean D_neg (JS):        {mean_d_neg_js:.6f}")
    print(f"Aggregate Ratio (JS):   {mean_ratio_js:.2f}x (neg vs pos)")
    print(f"Mean Delta_NLL (pos):   {mean_dnll_pos:.4f}")
    print(f"Mean Delta_NLL (neg):   {mean_dnll_neg:.4f}")
    print(f"Aggregate Ratio (NLL):  {mean_ratio_nll:.2f}x (neg vs pos)")
    
    # Statistical test: Wilcoxon signed-rank on D_neg > D_pos
    from scipy.stats import wilcoxon
    stat_js, p_js = wilcoxon([r["d_neg_js"] for r in results], [r["d_pos_js"] for r in results], alternative="greater")
    stat_nll, p_nll = wilcoxon([r["delta_nll_neg"] for r in results], [r["delta_nll_pos"] for r in results], alternative="greater")
    
    print(f"Wilcoxon p-value (JS divergence D_neg > D_pos):  p = {p_js:.6f}")
    print(f"Wilcoxon p-value (Delta NLL dNLL_neg > dNLL_pos): p = {p_nll:.6f}")
    
    if p_js < 0.05 and p_nll < 0.05 and mean_ratio_js > 2.0:
        print("\n>>> PILOT GATEWAY CLEARED: H13-A is CONFIRMED on GPT-2. The response channel is active and measurable.")
    else:
        print("\n>>> PILOT GATEWAY FAILED: Response channel insufficient.")

if __name__ == "__main__":
    main()
