# RAG Evaluation Results Analysis (Llama 4 Scout 17B on Legacy Prompt)

## 1. Distribution of 4 Labels (From 416 mutated samples)

Results from the AI Judge model (Llama 4 Scout 17B) evaluating the legacy `llama-3.1-17b-prompt` dataset across all 416 mutated samples:

| Label | Count | Percentage (%) |
|---|---|---|
| **Abstain** | 250 | 60.10% |
| **Faithful** | 127 | 30.53% |
| **Inconsistent** | 39 | 9.37% |
| **Hallucination** | 0 | 0.00% |

## 2. Construct Validity Check using Cohen's Kappa

Cross-referencing Synthetic Human Evaluator Labels (Llama 3.3 70B as Ground Truth) and AI Judge Labels (Llama 4 Scout 17B) on a random sample of 42 queries using the legacy prompt:

- **Matching Labels:** 36/42
- **Observed Agreement ($p_o$):** 0.8571 (85.71%)
- **Expected Agreement ($p_e$):** 0.4558 (45.58%)
- **Cohen's Kappa ($k$):** **0.7375**

> **Conclusion:** $k \approx 0.7375$. According to standard evaluation metrics, this Kappa score falls into the "Substantial Agreement" category (0.61 - 0.80). While acceptable, it is notably lower than the $k=0.9180$ ("Almost Perfect Agreement") achieved by the Upgraded System Prompt. This demonstrates that the legacy prompt structure struggled with edge cases, whereas the upgraded prompt successfully eliminated ambiguity in the AI Judge's reasoning.

---

## 3. Phase 6: Statistical Analysis

Based on the legacy data, we proceed to answer the Research Questions (RQs).

### RQ1: Hallucination Rate Analysis
- **Measured Hallucination Rate:** 0.0% (0/416).
- Reference Rule-based Mutation Hallucination Rate: 0% (Momtaz et al., 2026).
- **Conclusion:** RAG does not hallucinate fabricated information when facing Semantic Mutations, even with the legacy prompt.

### RQ2: Defensive Posture Collapse (Abstain Rate)
- **Measured Abstain Rate:** 60.10% (250/416).
- **Hypothesis $H_0$:** The RAG model maintains its defensive posture, meaning Abstain Rate $\ge 90\%$.
- **Binomial Test (scipy.stats.binomtest):** 
  - $p = 0.90$
  - Observed: 250 Abstain / 416 samples.
  - **$p$-value = 5.76e-58**
- **Conclusion:** Since $p \ll 0.05$, we **strongly reject** $H_0$. The RAG model still loses its defensive posture when faced with Semantic Mutations, despite having a higher abstain rate (60.10%) compared to the upgraded prompt (51.92%).
