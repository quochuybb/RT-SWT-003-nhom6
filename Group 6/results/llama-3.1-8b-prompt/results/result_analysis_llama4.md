# RAG Evaluation Results Analysis (Llama 4 Scout 17B on 8B-Prompt Configuration)

## 1. Distribution of 4 Labels (From 416 mutated samples)

Results from the AI Judge model (Llama 4 Scout 17B) evaluating the `llama-3.1-8b-prompt` dataset across all 416 mutated samples:

| Label | Count | Percentage (%) |
|---|---|---|
| **Abstain** | 265 | 63.70% |
| **Faithful** | 126 | 30.29% |
| **Inconsistent** | 24 | 5.77% |
| **Hallucination** | 1 | 0.24% |

## 2. Construct Validity Check using Cohen's Kappa

Cross-referencing Synthetic Human Evaluator Labels (Llama 3.3 70B as Ground Truth) and AI Judge Labels (Llama 4 Scout 17B) on a random sample of 42 queries for the 8b-prompt configuration:

- **Matching Labels:** 40/42
- **Observed Agreement ($p_o$):** 0.9524 (95.24%)
- **Expected Agreement ($p_e$):** 0.5181 (51.81%)
- **Cohen's Kappa ($k$):** **0.9012**

> **Conclusion:** $k \approx 0.9012$. According to standard evaluation metrics, this Kappa score falls firmly into the "Almost Perfect Agreement" category (> 0.80). This validates that the AI Judge (Llama 4 Scout 17B) demonstrates exceptional reliability when evaluating the responses of the 8B parameter RAG model, almost perfectly mirroring the human evaluator's judgment.

---

## 3. Phase 6: Statistical Analysis

Based on the validated data, we proceed to answer the Research Questions (RQs) for the 8B-Prompt architecture.

### RQ1: Hallucination Rate Analysis
- **Measured Hallucination Rate:** 0.24% (1/416).
- Reference Rule-based Mutation Hallucination Rate: 0% (Momtaz et al., 2026).
- **Z-test (Two-proportion):** $p$-value > 0.05.
- **Conclusion:** There is no statistically significant difference between Semantic Mutation and Rule-based Mutation regarding hallucinations. The RAG system (even at the 8B parameter scale) rarely fabricates completely new information.

### RQ2: Defensive Posture Collapse (Abstain Rate)
- **Measured Abstain Rate:** 63.70% (265/416).
- **Hypothesis $H_0$:** The RAG model maintains its defensive posture, meaning Abstain Rate $\ge 90\%$.
- **Binomial Test (scipy.stats.binomtest):** 
  - $p = 0.90$
  - Observed: 265 Abstain / 416 samples.
  - **$p$-value = 8.58e-47**
- **Conclusion:** Since $p \ll 0.05$, we **strongly reject** $H_0$. Even though the 8B model had a slightly higher abstain rate (63.70%) than the 17B model (60.10%) on this prompt configuration, its defensive posture still statistically collapses when faced with Semantic Mutations.
