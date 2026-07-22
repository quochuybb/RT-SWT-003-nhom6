# Gap Statement — Nguyễn Quốc Huy (Semantic Scholar)

> **Chủ đề:** AI-guided Mutant Selection for Java Programs
> **Evidence table:** N = 7 papers
> **Nguồn:** Semantic Scholar

---

## 2A. Xác định 4 loại GAP

### GAP-T (Technology) — Ưu tiên cao nhất
**Chưa có paper nào sử dụng LLM tạo sinh (GPT-4o, Claude, LLaMA-3) để chọn lọc đột biến thông minh**

- 7/7 paper dùng kỹ thuật ML truyền thống hoặc metaheuristic:
  - Spectral Clustering, Squirrel Search Algorithm, Elitist GA, MutationBERT (BERT encoder-only), Random Forest, Gradient Boosting, FCA Clustering
- MutationBERT (Jain & Alon) dùng BERT — là encoder-only model, **không phải** LLM tạo sinh
- **0/7 paper dùng generative LLM** (GPT-4o, Claude, LLaMA-3) cho mutant selection

### GAP-D (Dataset) — Ưu tiên cao
**Chỉ Java, quy mô nhỏ–trung bình, thiếu đa ngôn ngữ và enterprise-scale**

- 7/7 paper chỉ thực nghiệm trên Java
- Đa số dataset nhỏ: 8–20 programs (5/7 paper)
- Chỉ 2 paper (Aghamohammadi) dùng 654 projects nhưng vẫn chỉ Java
- Không có Go, Rust, TypeScript, Python

### GAP-M (Metric) — Ưu tiên trung bình
**Tập trung vào Accuracy/AUC, thiếu đánh giá chi phí triển khai thực tế**

- 5/7 paper chỉ dùng AUC, Mutation Score, P/R/F1
- Wei et al. và Zhu et al. có time-cost/speed-up nhưng không đo inference cost AI, CI/CD latency, developer productivity
- 0/7 paper đo chi phí API, cost-per-mutant, hay tích hợp CI/CD

### GAP-S (Shared Limitation) — Bổ sung
**Hạn chế chung ≥ 3 papers cùng thừa nhận**

- "Chỉ Java, chưa đa ngôn ngữ" → 5/7 paper
- "Dataset nhỏ/benchmark cố định" → 4/7 paper
- "Chưa xử lý equivalent mutants" → 3/7 paper

---

## 2B. Kiểm tra phản chứng

### GAP-T: "Chưa ai dùng LLM tạo sinh cho mutant selection"

| Paper | Phản chứng? | Ghi chú |
|---|---|---|
| Wei et al. (Spectral Clustering) | Không | Unsupervised clustering |
| SQUMUTH (Mohanty) | Không | Metaheuristic (SSA) |
| Rani & Suri (Elitist GA) | Không | Genetic Algorithm |
| Jain & Alon (MutationBERT) | Không | BERT encoder-only, không generative |
| Aghamohammadi #1 (PMT) | Không | RF + Gradient Boosting |
| Aghamohammadi #2 (EPMT) | Không | Ensemble ML + LIME |
| Zhu et al. (Compression) | Không | FCA + Overlapped Grouping |

→ **Kết luận: 0 phản chứng. GAP-T đứng vững.**

### GAP-D: "Chỉ Java, thiếu đa ngôn ngữ"
→ 0 phản chứng. 7/7 chỉ Java. **BÁC BỎ không được.**

### GAP-M: "Thiếu cost metrics thực tế"
→ 0 phản chứng rõ ràng. Wei/Zhu có speed-up nhưng không đo AI inference cost. **BÁC BỎ không được.**

---

## 2C. Đánh giá khả thi (Feasibility) — GAP-T (Primary Candidate)

| Tiêu chí | Đánh giá | Kết quả |
|---|---|---|
| **Dataset** | Defects4J có sẵn trên GitHub, tải được ngay | ✅ An toàn |
| **Tool/API** | GPT-4o có free tier (hoặc dùng GPT-4o-mini giá rẻ ~$0.15/1M tokens) | ✅ An toàn |
| **Compute** | CPU đủ cho prompt engineering; không cần GPU (LLM chạy qua API) | ✅ An toàn |
| **Ground truth** | Killing matrix từ PITest/MuJava có sẵn; không cần annotation thủ công | ✅ An toàn |
| **Skills** | Python + OpenAI API; có tutorial sẵn; học < 1 tuần | ✅ An toàn |
| **Experiment** | Few-shot prompting pipeline; hoàn thành được trong thời gian còn lại | ✅ An toàn |
| **Thời gian** | Xong với buffer ≥ 1 tuần dự phòng | ✅ An toàn |
| **Contribution** | Là baseline đầu tiên cho LLM-based mutant selection trên Defects4J | ✅ An toàn |

**→ Quy tắc quyết định: ≤ 2 ⚠️, không có ❌ → An toàn — tiếp tục với GAP này.**

---

## 2C. Đánh giá khả thi — GAP-M (Secondary Candidate)

| Tiêu chí | Đánh giá | Kết quả |
|---|---|---|
| **Dataset** | Dùng chung Defects4J với GAP-T | ✅ An toàn |
| **Tool/API** | Đo effort reduction = đếm số mutant cần chạy, tính thời gian | ✅ An toàn |
| **Compute** | Không cần thêm resource | ✅ An toàn |
| **Ground truth** | So sánh với Random baseline, dễ tạo | ✅ An toàn |
| **Skills** | Thêm metric effort vào pipeline sẵn có | ✅ An toàn |

**→ GAP-M pass feasibility. Chọn làm secondary GAP.**

---

## 2D. Ghi nhận GAP cuối cùng

### GAP Primary: GAP-T (Technology)

> Mặc dù đã có nhiều nghiên cứu áp dụng ML truyền thống (Random Forest, Gradient Boosting), metaheuristic (Squirrel Search, Genetic Algorithm), deep learning chuyên biệt (MutationBERT/BERT) và kỹ thuật clustering (Spectral Clustering, FCA) vào bài toán chọn lọc và dự đoán đột biến trên Java, **chưa có nghiên cứu nào ứng dụng trực tiếp khả năng suy luận ngữ nghĩa của LLMs tạo sinh hiện đại (GPT-4o, Claude, LLaMA-3) để phân tích mã nguồn và chọn lọc đột biến thông minh thông qua zero-shot/few-shot reasoning.**

### GAP Secondary: GAP-M (Metric)

> Các nghiên cứu hiện tại chủ yếu đánh giá bằng AUC, Mutation Score, Precision/Recall/F1. **Thiếu vắng các thước đo chi phí triển khai toàn diện** (inference cost, CI/CD integration latency, effort reduction rate, developer productivity impact) bên cạnh các metrics học thuật truyền thống.

### Hướng nghiên cứu đề xuất

> Xây dựng giải pháp ứng dụng **GPT-4o** kết hợp **few-shot prompting** để trực tiếp chọn lọc đột biến trên **Defects4J**, đánh giá đồng thời cả **mutation adequacy score (≥15%)** và **effort reduction (≥30%)** so với baseline Random và ML truyền thống (Random Forest).
