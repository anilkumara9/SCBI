"""EXP149a diagnostic — B-arm accuracy on the FULL 760-item bench.

DIAGNOSTIC ONLY (not a verdict input): study (a) already STOPPED at the
registered dry-run gate (B=0.90 on the 20-item subset -> HELD). This measures
whether the bench itself is systematically too easy or the subset was
unrepresentative. B arm only, T_B=15, greedy, §5.3 scoring. ~11k forwards.
"""
import json
import os
import re
import string
import sys
import time

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.expanduser("~/workspace/.exp149-venv/lib/python3.12/site-packages"))

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

SNAPSHOT = ("/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m"
            "/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f")
BENCH_PATH = os.path.join(RUN_DIR, "EXP149A_BENCH_2026-10-09.json")
PROMPTS_PATH = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP147/S7-1_PROMPTS_2026-10-05.json")
OUT = os.path.join(RUN_DIR, "exp149a_b_diagnostic.jsonl")

torch.manual_seed(149004)


def normalize(s):
    s = s.lower()
    s = s.translate(str.maketrans("", "", string.punctuation))
    return " ".join(s.split())


def main():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    tokenizer = AutoTokenizer.from_pretrained(SNAPSHOT, local_files_only=True,
                                              trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        SNAPSHOT, local_files_only=True, torch_dtype=torch.float32,
        device_map="cpu", attn_implementation="eager", trust_remote_code=False)
    model.eval()
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    with open(PROMPTS_PATH) as f:
        prompts = json.load(f)
    with open(BENCH_PATH) as f:
        bench = json.load(f)
    t = prompts["arms"]["B"]["template"]
    shots = "".join(prompts["shots"]["B"])
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            if line.strip():
                done.add(json.loads(line)["item_id"])
    print(f"resuming: {len(done)}/760 done", flush=True)
    from collections import Counter
    strat_acc = Counter()
    strat_n = Counter()
    for it in bench:
        if it["id"] in done:
            continue
        prompt = t.replace("{shots}", shots).replace(
            "{facts}", " ".join(it["facts"])).replace(
            "{question}", it["question"])
        inp = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            out = model.generate(inp["input_ids"], max_new_tokens=15,
                                 do_sample=False,
                                 pad_token_id=tokenizer.eos_token_id)
        gen = tokenizer.decode(out[0][inp["input_ids"].shape[1]:],
                               skip_special_tokens=True)
        toks = normalize(gen).split()
        first = toks[0] if toks else ""
        correct = 1 if first == normalize(it["gold"]) else 0
        with open(OUT, "a") as f:
            f.write(json.dumps({"item_id": it["id"], "stratum": it["stratum"],
                                "correct": correct}) + "\n")
        done.add(it["id"])
    for line in open(OUT):
        r = json.loads(line)
        strat_n[r["stratum"]] += 1
        strat_acc[r["stratum"]] += r["correct"]
    total = sum(strat_n.values())
    acc = sum(strat_acc.values()) / total
    print(f"FULL BENCH B accuracy: {acc:.4f} ({total} items)")
    for s in sorted(strat_n):
        print(f"  {s}: {strat_acc[s]/strat_n[s]:.4f} ({strat_n[s]})")


if __name__ == "__main__":
    main()
