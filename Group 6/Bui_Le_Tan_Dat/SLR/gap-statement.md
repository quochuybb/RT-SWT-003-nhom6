# Gap Statement – AI-guided Mutant Selection

Evidence table: N = 10 papers

## Các khoảng trống phát hiện

### GAP-T (Technology): Thiếu nghiên cứu sử dụng LLM

**Bằng chứng:** Wang_2021_MQP, Zhang_2019_PMT, Chen_2025_CAMUS, Dang_2022_GeneticAlgorithmMutationTesting sử dụng Random Forest, GNN hoặc Genetic Algorithm; không có nghiên cứu nào sử dụng LLM.

### GAP-M (Metric): Thiếu đánh giá chi phí thực tế

**Bằng chứng:** Hầu hết các paper sử dụng Precision, Recall, F1, AUC và Mutation Score; ít nghiên cứu đánh giá runtime reduction hoặc cost-effectiveness.

### GAP-D (Dataset): Dataset tập trung vào Java

**Bằng chứng:** Chen_2025_CAMUS, Kaufman_2022_PrioritizingMutants và Zhang_2019_PMT thực nghiệm trên Defects4J hoặc các dự án Java.

## Phát biểu GAP tổng hợp

Các nghiên cứu hiện tại chủ yếu áp dụng Machine Learning, GNN và Genetic Algorithm cho mutant selection trên dataset Java. Chưa có nghiên cứu sử dụng LLM, đánh giá đầy đủ chi phí thực tế và mở rộng thực nghiệm sang các hệ sinh thái ngoài Java.
