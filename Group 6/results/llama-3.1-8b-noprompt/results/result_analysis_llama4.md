# RAG Evaluation Results Analysis (Llama 4 Scout 17B on 8B-No-Prompt Configuration)

## 1. Distribution of 4 Labels (From 416 mutated samples)

Results from the AI Judge model (Llama 4 Scout 17B) evaluating the `llama-3.1-8b-noprompt` dataset across all 416 mutated samples:

| Label | Count | Percentage (%) |
|---|---|---|
| **Abstain** | 177 | 42.55% |
| **Inconsistent** | 124 | 29.81% |
| **Faithful** | 115 | 27.64% |
| **Hallucination** | 0 | 0.00% |

## 2. Construct Validity Check using Cohen's Kappa

Cross-referencing Synthetic Human Evaluator Labels (Llama 3.3 70B as Ground Truth) and AI Judge Labels (Llama 4 Scout 17B) on a random sample of 42 queries for the 8b-noprompt configuration:

- **Matching Labels:** 37/42
- **Observed Agreement ($p_o$):** 0.8810 (88.10%)
- **Expected Agreement ($p_e$):** 0.3878 (38.78%)
- **Cohen's Kappa ($k$):** **0.8056**

> **Conclusion:** $k \approx 0.8056$. According to standard evaluation metrics, this Kappa score falls into the "Almost Perfect Agreement" category (> 0.80). This validates that the AI Judge (Llama 4 Scout 17B) reliably evaluates the 8B-No-Prompt RAG system, consistently aligning with the Human Evaluator's (70B) judgment.

---

## 3. Phase 6: Statistical Analysis

Based on the validated data, we proceed to answer the Research Questions (RQs) for the 8B-No-Prompt architecture.

### RQ1: Hallucination Rate Analysis
- **Measured Hallucination Rate:** 0.00% (0/416).
- Reference Rule-based Mutation Hallucination Rate: 0% (Momtaz et al., 2026).
- **Conclusion:** There is no statistically significant difference regarding hallucinations. Even when stripped of its protective System Prompt, the 8B RAG model does not resort to fabricating entirely new information when faced with corrupted context.

### RQ2: Defensive Posture Collapse (Abstain Rate)
- **Measured Abstain Rate:** 42.55% (177/416).
- **Hypothesis $H_0$:** The RAG model maintains its defensive posture, meaning Abstain Rate $\ge 90\%$.
- **Binomial Test (scipy.stats.binomtest):** 
  - $p = 0.90$
  - Observed: 177 Abstain / 416 samples.
  - **$p$-value = 5.61e-126**
- **Conclusion:** Since $p \ll 0.05$, we **strongly reject** $H_0$. Removing the System Prompt caused the Abstain rate to plummet from 63.70% (8B-Prompt) down to 42.55% (8B-No-Prompt). The model's defensive posture is heavily compromised, causing it to fall for the fake context (27.64% Faithful) or leak its parametric knowledge (29.81% Inconsistent) in the majority of cases.
