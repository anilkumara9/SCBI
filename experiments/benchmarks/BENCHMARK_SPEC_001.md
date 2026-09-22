# Benchmark Specification 001: Synthetic Linear Disentanglement & Distractor Interference (SLD-DI)

**Benchmark ID:** BENCH-001  
**Target:** Mechanism evaluation for Instance-Adaptive Subspace Projection (IASP / SCBI Formulation D+C)  
**Governing Protocol:** Reviewer V0.2 Section 10  
**Date:** 2026-09-11  

---

## 1. Task Generation Process

The task is designed to test representation-level interference in a controlled setting where ground truth is known, features are algebraically tractable, and causal attribution is unambiguous.

### Latent Structure
- Feature Space: $\mathbb{R}^d$ ($d=32$ for minimal verification; scalable to $d=896$ for Qwen2.5-0.5B).
- Let $u_{\text{query}} \in \mathbb{R}^d$ be the unit vector representing the primary relational query.
- Let $u_{\text{target}} \in \mathbb{R}^d$ be the true target signal with class label $y \in \{0, 1, 2, 3\}$.
- Let $u_{\text{distractor}} \in \mathbb{R}^d$ be an orthogonal planted distractor subspace ($r=2$) designed to corrupt downstream linear readout.

### Instance Construction
Each instance $x_i$ consists of a sequence of $S=8$ token vectors:
1. Tokens $1 \dots 4$: Context / premise tokens encoding the true relation $y_i$.
2. Tokens $5 \dots 6$: Planted distractor tokens projecting strongly onto $u_{\text{distractor}}$.
3. Tokens $7 \dots 8$: Query tokens triggering the downstream prediction head.

### In-Distribution (ID) vs. Out-of-Distribution (OOD)
- **ID Split ($N=100$):** Distractor amplitude $\alpha_{\text{distractor}} = 0.5$.
- **OOD Split ($N=100$):** Strong distractor interference $\alpha_{\text{distractor}} = 1.8$, where distractor energy overwhelms the baseline linear attention readout.

---

## 2. Benchmark Parameters

```yaml
benchmark:
  name: "synthetic_linear_disentanglement"
  id: "BENCH-001"
  hidden_dim: 32
  seq_len: 8
  num_classes: 4
  distractor_rank: 2
  sample_count:
    val: 50
    test_id: 100
    test_ood: 100
  metric: "exact_match_accuracy"
```
