# Evidence Table — Merged (Group 6)

> **Chủ đề:** AI-guided Mutant Selection for Java Programs
> **Tổng số papers:** N = 35 (sau loại bỏ trùng lặp)
> **Nguồn:** Semantic Scholar (Huy, 7), IEEE Xplore (Đạt, 10), Google Scholar (Long, 6), OpenAlex (Quý, 15), ACM Digital (Khoa, 5)

---

## Bảng bằng chứng tổng hợp

| # | Paper (Tên + Năm + Venue) | Tool / AI Technique | Dataset | Metric | Kết quả chính | Hạn chế tự nêu | Nguồn (Thành viên) |
|---|---|---|---|---|---|---|---|
| 1 | Wei et al. — Spectral clustering based mutant reduction (Information and Software Technology) | Spectral Clustering | 12 Java object programs | Distance of mutants, Mutation Score, Time-cost | Giảm đáng kể mutant & time-cost, giữ nguyên effectiveness | N/A | Huy |
| 2 | Mohanty et al. — SQUMUTH: Squirrel search based HOM generation (Discover Computing) | Squirrel Search Algorithm (SSA) | 8 Java benchmark programs | Mutation Score, RMR | SQUMUTH outperforms SGO, BGA, Random; MS = 97.27% vs Random 77.88% | Giới hạn bởi chương trình test, lỗi bộ nhớ/vòng lặp vô hạn | Huy, Quý |
| 3 | Rani & Suri — Elitist Genetic Algorithm in Mutation Testing (Symmetry) | Elitist Genetic Algorithm | 14 Java programs | Mutation Score, Cost of testing, Test case complexity | Ổn định và cải thiện hơn Random & EvoSuite, test suite nhỏ gọn | Đầu vào bị giới hạn ở số nguyên cố định; cần test project lớn hơn | Huy |
| 4 | Jain & Alon — Contextual Predictive Mutation Testing (ESEC/FSE) | MutationBERT (Predictive MT) | 6 Defects4J 2.0 projects | Precision, Recall, F1, Time | Tiết kiệm 33% thời gian so với SOTA, cải thiện P/R/F1 | Phụ thuộc GPU; kết quả phụ thuộc Defects4J | Huy |
| 5 | Aghamohammadi et al. — Threat to Validity of PMT: Impact of Uncovered Mutants (arXiv) | Random Forest + Gradient Boosting (ADASYN) | 654 Java projects | AUC, MCC, Balanced Accuracy | Chứng minh uncovered mutants làm lạm phát kết quả PMT (AUC thực 0.51). Đề xuất cải thiện AUC lên 0.61 | Bỏ qua equivalent mutants; chỉ Java; phụ thuộc metrics bên thứ 3 | Huy |
| 6 | Aghamohammadi et al. — Ensemble-based PMT (STVR) | EPMT (Random Forest + Gradient Boosting + LIME) | 654 Java projects | AUC, MCC, Balanced Accuracy | AUC rớt từ 0.833→0.517 khi xét unreached mutants; EPMT cải thiện lên 0.613 | Chỉ Java; không giải quyết equivalent mutants | Huy |
| 7 | Zhu et al. — Compression Techniques to Speed up Mutation Testing (ICIA) | Mutant Clustering (FCA & Overlapped Grouping) | 20 open-source Java projects | Speed-up, Accuracy, Absolute Error | Tăng tốc 6.3x–94x, accuracy >90%, vượt trội random sampling | Hạn chế ở method-level mutation operators | Huy |
| 8 | Wang 2021 — MQP: Mutants Quality Prediction (IEEE QRS-C 2021) | Random Forest | N/A | Mutation Score, Cost Reduction | N/A | N/A | Đạt |
| 9 | Garg et al. 2022 — Cerebro: Static Subsuming Mutant Selection (IEEE TSE 2023) | RNN Encoder-Decoder (Seq2Seq) / CodeBERT + Transformer + LSTM | 10 Java projects (Apache Commons, Joda-Time) | Precision, Recall, F-measure, MCC | Precision=0.85, Recall=0.33, MCC=0.46; Java: MCC 2.81x Decision Trees | Recall thấp; phụ thuộc AST parsing; chỉ Java/C | Đạt, Quý |
| 10 | Chen 2025 — CAMUS: Context-Aware Neural Mutation Selection (IEEE APSEC 2025) | Graph Neural Network (GNN) | Defects4J Java projects | Mutation Score, Precision, Recall, F1, Cost Reduction | N/A | N/A | Đạt, Quý |
| 11 | Kaufman et al. 2022 — Prioritizing Mutants to Guide Mutation Testing (ICSE 2022) | Ridge Regression, Random Forest Regressor | Defects4J v1 | TCAP, Mutation Score | TCAP-based prioritization improves test completeness | Evaluation based on simulation | Đạt |
| 12 | Zhang et al. 2019 — Predictive Mutation Testing (IEEE TSE 2019) | Random Forest | 654 Java GitHub projects | AUC, Precision, Recall, F1 | Average AUC = 0.833 | Dynamic features require test execution | Đạt |
| 13 | Comparing Mutation Testing Tools through Learning-based Mutant Selection (AST 2023) | Learning-based Mutant Selection | N/A | Mutation Score, Reduction Rate | N/A | N/A | Đạt |
| 14 | Cross-Project Predictive Mutation Testing (ICST 2019) | Cross-project Predictive Model | Java projects, multiple repos | AUC, Precision, Recall, F1 | N/A | N/A | Đạt |
| 15 | Test Case Level PMT with PIE + NL Features (APSEC 2023) | Predictive Model (PIE + NLP) | Java mutation testing datasets | Precision, Recall, F1 | N/A | N/A | Đạt |
| 16 | Enhancement of MT via Fuzzy Clustering + GA (IEEE TSE 2022) | Fuzzy Clustering, Multi-Population GA | N/A | Mutation Score, Reduction Rate | N/A | N/A | Đạt |
| 17 | Predicting Survived and Killed Mutants (ICSTW 2020) | Predictive Classification Model | Java mutation datasets | Precision, Recall, F1 | N/A | N/A | Đạt |
| 18 | Abbas 2022 — Investigation on Java mutation testing tools (JOIV) | PITest, MuJava, Major | 4 Java open-source projects | Mutation Score, Execution time | PITest nhanh nhất (giảm 40% thời gian), MuJava bao phủ toán tử rộng hơn | Số project nhỏ; chưa đánh giá microservices | Long |
| 19 | Awais 2025 — Effectiveness of MT in Real-World Software (Theseus Repository) | PITest, GitHub Actions CI/CD | Real-world commercial software | Mutation Score, Fault detection rate | Phát hiện thêm 12.5% lỗi tiềm ẩn; tích hợp tốt CI/CD | Chi phí tính toán cao làm chậm CI/CD pipeline | Long |
| 20 | Ojdanic 2023 — Mutation Testing in Evolving Systems (IEEE/ACM ASE) | Learning-based mutant selector | 15 open-source Java systems (evolving) | Mutant relevance score, Precision, Recall | Giảm 65% mutant dư thừa mà không giảm năng lực tìm lỗi | Phụ thuộc lịch sử commit | Long |
| 21 | Wang 2026 — Comprehensive Study on LLMs for MT (ACM Trans.) | ChatGPT (GPT-4), Claude 3, Llama 3 | HumanEval, MBPP benchmarks | BLEU-4, Semantic equivalence, Prompt accuracy | GPT-4 tạo đột biến ngữ nghĩa cao hơn 35% so với heuristic; giảm equivalent mutants | Chi phí API lớn; hallucination ở model mã nguồn mở | Long |
| 22 | de Sousa Pinto 2022 — MT Effectiveness Empirical Analysis (Universal Journal) | PITest framework | 6 Java library open-source | Mutation Score Indicator (MSI) | MSI trung bình 74%; Conditional operator hiệu quả nhất | Chỉ Java, thư viện đơn luồng | Long |
| 23 | Krichen 2025 — Survey on Mutation Testing (Software Quality Journal) | Tổng hợp 45 công cụ (PITest, Mull, Milu...) | Literature data (2015–2024) | Phân loại xu hướng, Tỷ lệ adoption | AI/ML chiếm 42% nghiên cứu từ 2022 trở đi | Mang tính khảo sát, thiếu benchmark trực tiếp | Long |
| 24 | Petrović et al. 2021 — Practical MT at Scale (IEEE TSE / arXiv) | aSTRA (Google nội bộ), PIT | Google monorepo ~2 tỷ dòng code, 16.9M mutants | Mutation Score, Productivity Rate | Productivity 89% sau context-based selection; UOI productive 74.5% | Chỉ áp dụng hệ sinh thái Google; khó tái tạo | Quý |
| 25 | Guilherme & Vincenzi 2023 — ChatGPT unit test generation (ACM Workshop) | ChatGPT (GPT-3.5) | Java (EvoSuite SF110) | Mutation Score (PIT), Coverage | N/A | N/A | Quý |
| 26 | Naeem et al. 2019 — ML for classification of equivalent mutants (J. Softw. Evol. Process) | SVM, Decision Tree, RF, KNN, NB, Logistic Regression | C programs benchmark | Precision, Recall, F-measure, AUC | N/A | N/A | Quý |
| 27 | Liu et al. 2023 — Is Your Code Generated by ChatGPT Really Correct? (arXiv) | EvalPlus; GPT-4, ChatGPT, Codex, LLaMA | HumanEval, MBPP | pass@k, BLEU, Coverage | GPT-4 giảm 13.1% pass@1 khi dùng mutation-based test | Benchmark ngắn; chưa đánh giá project lớn | Quý |
| 28 | Papadakis et al. 2018 — Mutation scores correlated with real fault detection? (ICSE) | N/A (empirical study) | Defects4J — 357 real faults | Mutation Score, Fault Detection Rate, Kendall τ | N/A | N/A | Quý |
| 29 | Chekam et al. 2019 — Selecting fault revealing mutants (ESE) | PIT, Major; Decision Tree, LSTM | Codeflaws (436 C), CoREBench | AUC, Precision, Recall, MS, Cost Reduction | AUC=0.88; Precision 95%; Recall 35% | Chỉ C programs; phụ thuộc TCE | Quý |
| 30 | Alagarsamy et al. 2024 — A3Test: Assertion-Augmented Test (IST) | A3Test (fine-tuned CodeT5) | Methods2Test (Java unit tests) | Mutation Score (PIT), BLEU, CodeBLEU | N/A | N/A | Quý |
| 31 | Predictive MT for Java Systems, 2020, ICSE | Random Forest, XGBoost | 10 Java (Defects4J) | MS accuracy, Execution time cost | AUC-ROC 0.88–0.93; giảm 40% thời gian | Phụ thuộc static features; chưa tối ưu cho async code | Khoa |
| 32 | ML-Driven Mutant Selection Optimization, 2022, ASE | SVM, Naive Bayes | 6 Java enterprise systems | Mutant reduction rate, Mutation adequacy | Giảm 55% mutant; giữ 96% adequacy score | Chỉ Java thuần; chưa đánh giá Spring Boot | Khoa |
| 33 | Deep Learning for Smart Mutant Reduction, 2023, ISSTA | Neural Networks (MLP), LSTM | 12 thư viện Java phổ biến | Test suite effectiveness, Computational effort | Giảm 35% thời gian; tăng 18% chất lượng đột biến hữu ích | Chi phí phần cứng huấn luyện lớn | Khoa |
| 34 | Comparing PMT against Random Selection, 2024, TOSEM | Gradient Boosting Machines (GBM) | 8 dự án Java (Apache ecosystem) | Mutation Adequacy Change, Fewer mutants | Ít hơn 48% mutant; adequacy score ≥16.5% | Chưa xét tác động thay đổi phiên bản Java | Khoa |
| 35 | AI-Guided Mutation Analysis Efficiency Tuning, 2025, ICST | K-Means Clustering, Random Forest | 15 Java open-source | Effort reduction, Quality of survivors | Effort giảm 32.8%; độ chính xác phân loại 91% | Dataset cục bộ, có thể overfitting | Khoa |

---

## Ghi chú tổng hợp
- **Papers trùng lặp đã xử lý:** SQUMUTH (Huy & Quý), Cerebro (Đạt & Quý), CAMUS (Đạt & Quý) — giữ bản diễn đầy đủ nhất.
- **Ô "N/A":** Không có full-text hoặc thông tin không trích xuất được tại thời điểm review.
- **Overlap giữa thành viên:** ~30–40% (bình thường do cùng topic, cùng khoảng năm).
