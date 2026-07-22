# RAG Evaluation Results Analysis (Llama 4 Scout 17B on No-Prompt Configuration)

## 1. Distribution of 4 Labels (From 416 mutated samples)

Results from the AI Judge model (Llama 4 Scout 17B) evaluating the `llama-3.1-17b-noprompt` dataset across all 416 mutated samples:

| Label | Count | Percentage (%) |
|---|---|---|
| **Faithful** | 214 | 51.44% |
| **Inconsistent** | 186 | 44.71% |
| **Abstain** | 15 | 3.61% |
| **Hallucination** | 1 | 0.24% |

## 2. Construct Validity Check using Cohen's Kappa

Cross-referencing Synthetic Human Evaluator Labels (Llama 3.3 70B as Ground Truth) and AI Judge Labels (Llama 4 Scout 17B) on a random sample of 42 queries for the no-prompt configuration:

- **Matching Labels:** 38/42
- **Observed Agreement ($p_o$):** 0.9048 (90.48%)
- **Expected Agreement ($p_e$):** 0.4569 (45.69%)
- **Cohen's Kappa ($k$):** **0.8246**

> **Conclusion:** $k \approx 0.8246$. According to standard evaluation metrics, this Kappa score falls into the "Almost Perfect Agreement" category (> 0.80). This validates that the AI Judge (Llama 4 Scout 17B) evaluates the No-Prompt RAG system with extremely high reliability, closely mirroring the Human Evaluator's (70B) judgment.

---

## 3. Phase 6: Statistical Analysis

Based on the validated data, we proceed to answer the Research Questions (RQs) for the No-Prompt architecture.

### RQ1: Hallucination Rate Analysis
- **Measured Hallucination Rate:** 0.24% (1/416).
- Reference Rule-based Mutation Hallucination Rate: 0% (Momtaz et al., 2026).
- **Z-test (Two-proportion):** $p$-value > 0.05.
- **Conclusion:** There is no statistically significant difference between Semantic Mutation and Rule-based Mutation regarding hallucinations (Failed to reject $H_0$). The RAG system rarely fabricates completely new information, even without a defensive system prompt.

### RQ2: Defensive Posture Collapse (Abstain Rate)
- **Measured Abstain Rate:** 3.61% (15/416).
- **Hypothesis $H_0$:** The RAG model maintains its defensive posture, meaning Abstain Rate $\ge 90\%$.
- **Binomial Test (scipy.stats.binomtest):** 
  - $p = 0.90$
  - Observed: 15 Abstain / 416 samples.
  - **$p$-value $\approx 0.0$**
- **Conclusion:** Since $p \ll 0.05$, we **strongly reject** $H_0$. Without a protective System Prompt, the RAG model's defensive posture is completely obliterated. The model blindly absorbs the mutated context (51.44% Faithful) or relies on its own parametric knowledge to contradict the context (44.71% Inconsistent), but it almost never correctly abstains (3.61%).
