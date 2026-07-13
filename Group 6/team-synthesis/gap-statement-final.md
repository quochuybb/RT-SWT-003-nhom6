# Gap Statement — Final (Group 6)

> **Chủ đề:** AI-guided Mutant Selection for Java Programs
> **Evidence table merged:** N = 35 papers
> **Thành viên tổng hợp:** 5 (Huy, Đạt, Long, Quý, Khoa)

---

## Các khoảng trống phát hiện (Đối chiếu từ 5 thành viên)

### GAP-T (Technology) — *Ưu tiên cao nhất*
**Sự thiếu vắng ứng dụng trực tiếp LLMs thế hệ mới trong chọn lọc và phân loại đột biến**

| Thành viên | Bằng chứng |
|---|---|
| **Huy** | Đa số nghiên cứu dùng ML truyền thống (RF, Gradient Boosting) hoặc DL chuyên biệt (BERT). Chưa có paper nào áp dụng LLM tạo sinh (GPT-4, LLaMA-3) để chọn mutant dựa trên zero-shot/few-shot reasoning. |
| **Đạt** | Wang_2021_MQP, Zhang_2019_PMT, Chen_2025_CAMUS, Dang_2022 sử dụng RF, GNN hoặc GA; không có nghiên cứu nào sử dụng LLM. |
| **Long** | Các công cụ MT truyền thống (PITest) dùng quy tắc toán tử cố định. Wang 2026 mới bắt đầu dùng GPT-4/Claude 3 nhưng chỉ để sinh mutant, chưa để chọn lọc thông minh. |
| **Quý** | S1–S15: Chưa có nghiên cứu nào dùng trực tiếp LLM để phân loại equivalent mutants hoặc chọn subsuming mutants từ source code. Ngoài aSTRA (Google, đóng), chưa có công cụ chọn lọc mutant tích hợp CI/CD mở cho cộng đồng. |
| **Khoa** | Các paper dùng RF, XGBoost, SVM, LSTM; thiếu khai thác mô hình biểu diễn ngữ cảnh chuyên sâu dạng đồ thị (GNN) kết hợp luồng dữ liệu Java lớn. |

**Kết luận GAP-T:** 5/5 thành viên đều xác nhận khoảng trống này. Đây là GAP có bằng chứng mạnh nhất (primary gap).

---

### GAP-M (Metric) — *Ưu tiên cao*
**Tập trung quá nhiều vào Accuracy/AUC, thiếu đánh giá chi phí triển khai thực tế và năng suất lập trình viên**

| Thành viên | Bằng chứng |
|---|---|
| **Huy** | Hầu hết dùng AUC/Accuracy. Chỉ bài Compression Techniques đề cập speed-up. Rất ít paper đo "Execution Time Overhead" thực tế hoặc cân bằng "Mutation Adequacy" vs "Computational Cost" chuẩn hóa trên dự án lớn. |
| **Đạt** | Hầu hết dùng Precision, Recall, F1, AUC, Mutation Score; ít đánh giá runtime reduction hoặc cost-effectiveness. |
| **Quý** | 13/15 bài (ngoại trừ S1, S2 của Google) hoàn toàn bỏ qua: chi phí inference AI, tác động lên năng suất lập trình viên, và out-of-distribution robustness. |
| **Khoa** | Đánh đổi chưa tối ưu giữa Mutation Score và Effort Reduction; chưa chứng minh tính ổn định cross-project trên Java thế hệ mới. |

**Kết luận GAP-M:** 4/5 thành viên xác nhận (Long không đề cập trực tiếp nhưng gián tiếp qua chi phí CI/CD). Đây là secondary gap.

---

### GAP-D (Dataset) — *Ưu tiên cao*
**Phụ thuộc dataset cũ (Defects4J), bó hẹp ở Java, thiếu dữ liệu quy mô công nghiệp**

| Thành viên | Bằng chứng |
|---|---|
| **Huy** | Dùng chung dataset cố định (654 Java projects, 8–14 benchmark programs). Chưa có đánh giá trên dự án Microservices/Enterprise level. |
| **Đạt** | CAMUS, Kaufman, Zhang thực nghiệm trên Defects4J hoặc Java projects. |
| **Long** | Chỉ Java; thư viện đơn luồng; chưa đánh giá trên hệ thống phức tạp. |
| **Quý** | S7 chỉ 4 Java projects; S9 dùng HumanEval/MBPP ngắn; S12 chỉ C. Dữ liệu đa ngôn ngữ duy nhất (Google monorepo) là mã nguồn đóng. Thiếu dataset đa ngôn ngữ (Go, Rust, TypeScript) cho cộng đồng. |
| **Khoa** | Dataset huấn luyện cục bộ, có thể overfitting khi chuyển sang dự án Java mới. |

**Kết luận GAP-D:** 5/5 thành viên đều xác nhận. Đây là secondary gap.

---

### GAP-S (Scope/Application) — *Bổ sung từ Long*
**Thiếu đánh giá LLM mã nguồn mở chuyên biệt cho code và các metric ngữ nghĩa nâng cao**

| Thành viên | Bằng chứng |
|---|---|
| **Long** | Không paper nào đánh giá LLM mã nguồn mở chuyên biệt (DeepSeek-Coder); thiếu metric Semantic similarity để sàng lọc chất lượng đột biến AI; thiếu đo Executable rate thực tế của mã đột biến do LLM tạo. |

**Kết luận GAP-S:** 1/5 thành viên đề cập trực tiếp, nhưng liên quan mật thiết tới GAP-T.

---

## Phát biểu GAP tổng hợp nhóm (Group Gap Statement)

Mặc dù đã có nhiều tiến bộ trong việc áp dụng Machine Learning truyền thống (Random Forest, SVM, Gradient Boosting), Deep Learning chuyên biệt (LSTM, CodeBERT, GNN) và thuật toán tìm kiếm (Genetic Algorithm, Squirrel Search) vào chọn lọc đột biến trên Java, **khoảng trống nghiên cứu lớn nhất hiện nay bao gồm:**

1. **GAP-T (Primary):** Chưa có nghiên cứu nào ứng dụng trực tiếp khả năng suy luận ngữ nghĩa của các LLMs tạo sinh hiện đại (GPT-4o, Claude, LLaMA-3) để phân tích mã nguồn và chọn lọc đột biến thông minh thông qua zero-shot/few-shot reasoning.

2. **GAP-M (Secondary):** Thiếu vắng các thước đo đánh giá chi phí triển khai toàn diện (inference cost, CI/CD integration latency, developer productivity impact) bên cạnh các metrics học thuật truyền thống (AUC, F1).

3. **GAP-D (Secondary):** Các bộ dataset benchmark hiện tại bị bó hẹp ở ngôn ngữ Java/C với quy mô nhỏ–trung bình, chưa có dataset mã nguồn mở đa ngôn ngữ quy mô công nghiệp phục vụ huấn luyện và kiểm chứng chéo mô hình AI.

**→ Hướng nghiên cứu đề xuất:** Xây dựng giải pháp ứng dụng LLM (GPT-4o) kết hợp few-shot prompting để trực tiếp chọn lọc đột biến trên Defects4J, đánh giá đồng thời cả mutation adequacy score (≥15%) và effort reduction (≥30%) so với baseline Random và ML truyền thống.
