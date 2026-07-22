# RAG Evaluation Results Analysis (Llama 4 Scout 17B)

## 1. Distribution of 4 Labels (From 416 mutated samples)

Results from the AI Judge model (Llama 4 Scout 17B) across all 416 mutated samples:

| Label | Count | Percentage (%) |
|---|---|---|
| **Inconsistent** | 12 | 2.88% |
| **Faithful** | 188 | 45.19% |
| **Abstain** | 216 | 51.92% |
| **Hallucination** | 0 | 0.00% |

## 2. Construct Validity Check using Cohen's Kappa

Cross-referencing Human Evaluator Labels (`human_label`) and AI Judge Labels (`ai_label` by Llama 4 Scout 17B) on a random sample of 42 queries:

- **Matching Labels:** 40/42
- **Observed Agreement ($p_o$):** 0.9524 (95.24%)
- **Expected Agreement ($p_e$):** 0.4195 (41.95%)
- **Cohen's Kappa ($k$):** **0.9180**

> **Conclusion:** $k \approx 0.9180$. According to standard evaluation metrics, this Kappa score falls into the "Almost Perfect Agreement" category. This confirms that the AI Judge (Llama 4 Scout 17B) is highly reliable and is suitable to fully replace human evaluators for large-scale assessment.

---

## 3. Phase 6: Statistical Analysis

Based on the Kappa-verified data from Llama 4 Scout 17B, we proceed to answer the Research Questions (RQs).

### RQ1: Hallucination Rate Analysis
- **Measured Hallucination Rate:** 0.0% (0/416).
- Reference Rule-based Mutation Hallucination Rate: 0% (Momtaz et al., 2026).
- **Z-test (Two-proportion):** $p$-value = 1.0000.
- **Conclusion:** There is no statistically significant difference between Semantic Mutation and Rule-based Mutation regarding hallucinations (Failed to reject $H_0$). RAG does not hallucinate fabricated information when facing Semantic Mutations.

### RQ2: Defensive Posture Collapse (Abstain Rate)
- **Measured Abstain Rate:** 51.92% (216/416).
- **Hypothesis $H_0$:** The RAG model maintains its defensive posture, meaning Abstain Rate $\ge 90\%$.
- **Binomial Test (scipy.stats.binomtest):** 
  - $p = 0.90$
  - Observed: 216 Abstain / 416 samples.
  - **$p$-value = 7.22e-87**
- **Conclusion:** Since $p \ll 0.05$, we **strongly reject** $H_0$. The RAG model completely loses its defensive posture when faced with Semantic Mutations, resulting in either absorbing the false information (Faithful) or reacting inconsistently (Inconsistent) instead of abstaining.
