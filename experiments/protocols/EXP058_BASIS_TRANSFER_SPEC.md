# EXP058 Protocol Specification: Basis Reconfiguration & Cross-Domain Transfer

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP050, EXP057  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Objectives

If temporary representations capture abstract computational coordinates rather than domain-specific lexical associations, **a representation discovered for a specific structural geometry in Domain A should successfully transfer to a structurally identical but lexically and domain-distinct Task B**.

$$\boxed{\text{Does a temporary basis discovered for Task A transfer to a lexically distinct Task B sharing the same geometry?}}$$

---

## 2. Experimental Conditions

| Condition | Basis Source | Target Task | Structural Match |
| :--- | :--- | :--- | :--- |
| **C0: Greedy Baseline** | None | Domain B | N/A |
| **C1: Matched Geometry Transfer** | Inferred on Domain A ($G_1$) | Domain B ($G_1$) | Matched Geometry |
| **C2: Mismatched Geometry Transfer** | Inferred on Domain A ($G_2$) | Domain B ($G_1$) | Mismatched Geometry |
| **C3: Native Inferred Basis** | Inferred directly on Domain B | Domain B ($G_1$) | Native Upper Bound |

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 Structural Transfer Specificity:
$$\Delta M(\text{Matched Transfer}) > \Delta M(\text{Mismatched Transfer}) \quad (p < 0.05)$$
Proving that basis transfer reflects geometric compatibility rather than generic activation perturbation.

### 3.2 Headroom Retention Ratio:
$$\tau_{\text{transfer}} = \frac{M(\text{Matched Transfer}) - M(\text{Base})}{M(\text{Native Basis}) - M(\text{Base})} \ge 0.50$$
Retaining at least $50\%$ of the native inferred basis headroom across disjoint domains.

---

## 4. Pre-Registered Falsification Criteria

Abstract structural transfer is **falsified** if:
1. Matched geometry transfer produces performance no better than mismatched geometry transfer ($p \ge 0.05$).
2. Cross-domain transfer causes net degradation ($\Delta M < 0$) on Domain B.
