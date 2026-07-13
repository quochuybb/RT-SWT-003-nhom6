# GAP Analysis - AI-guided Mutant Selection
Evidence table: N = 15 paper | Ngày: 2026-06-09

## BƯỚC 1: Kiểm tra Evidence Table (Gates Validation)
- **P1 (Số paper):** 15 paper ($\ge$ 5) $\rightarrow$ **Pass**
- **P2 (Cột Tool/LLM):** 100% điền (PIT, ChatGPT, CodeBERT, SQUMUTH...) $\rightarrow$ **Pass**
- **P3 (Cột Kết quả):** $\ge$ 50% hàng có số liệu cụ thể (MS 97.27%, 89% Productivity) $\rightarrow$ **Pass**
- **P4 (Cột Hạn chế):** $\ge$ 50% hàng có điền hạn chế (Google monorepo đóng, dataset đơn ngôn ngữ) $\rightarrow$ **Pass**
- **P5 (Cột Metric):** Tên metric cụ thể (Mutation Score, Precision, Cost Reduction) $\rightarrow$ **Pass**

## Bảng GAP (BƯỚC 2A)

| Cột | Phát hiện | Loại GAP | Phản chứng |
|-----|-----------|----------|------------|
| Tool/LLM | Thiếu vắng Generative LLM trực tiếp suy luận và chọn lọc mutant. | GAP-T | ✅ Kiểm tra 15 paper |
| Dataset | Các benchmark bị thiên lệch ngôn ngữ (C/Java), quy mô nhỏ. | GAP-D | ✅ Kiểm tra 15 paper |
| Metric | Thiếu đánh giá thực tế về AI inference cost và năng suất lập trình viên. | GAP-M | ✅ Kiểm tra 15 paper |
| Hạn chế | Chưa có giải pháp cân bằng giữa chất lượng chọn lọc và chi phí AI/thời gian. | GAP-S | ✅ Kiểm tra 15 paper |

## GAP Chính: GAP-T
Mặc dù AI/ML đã được ứng dụng trong mutation testing, việc sử dụng các Mô hình Ngôn ngữ Lớn sinh tạo (Generative LLMs như GPT-4, Llama) để trực tiếp suy luận và phân loại đột biến tương đương (equivalent mutants) hoặc chọn lọc đột biến bao hàm (subsuming mutants) từ source code vẫn chưa được khai phá.

## GAP Secondary: GAP-M & GAP-D
Các nghiên cứu hiện tại thiếu hụt bộ dữ liệu benchmark đa ngôn ngữ quy mô lớn mã nguồn mở (GAP-D) và hoàn toàn bỏ qua việc đo lường chi phí thực thi thực tế của AI (AI inference cost) so với năng suất của lập trình viên (GAP-M).

## Đánh giá khả thi (Feasibility) trước khi chốt GAP (BƯỚC 2C)

| Tiêu chí | Trạng thái | Lý do đánh giá |
|---|---|---|
| **Dataset** | ✅ An toàn | Khởi đầu với Defects4J (public, tải được ngay). Việc mở rộng ngôn ngữ sẽ crawl thêm từ GitHub có sẵn. |
| **Tool/API** | ✅ An toàn | GPT-4o / Llama-3 API đều có mức phí rất rẻ cho sinh viên (< $5) hoặc Colab free. |
| **Compute** | ✅ An toàn | Sinh mutant bằng CPU máy cá nhân, LLM chạy qua API không đòi hỏi GPU cục bộ mạnh. |
| **Ground truth** | ✅ An toàn | Mutant thô được sinh bởi PIT/Major có sẵn, không cần tạo nhãn thủ công (0 giờ annotation). |
| **Skills** | ✅ An toàn | Đã có kỹ năng API/prompting và chạy tool PIT. |
| **Thời gian** | ✅ An toàn | Pipeline prompt đơn giản, xong với buffer $\ge$ 1 tuần. |
| **Contribution**| ✅ Có thể | Baseline đầu tiên cho việc dùng trực tiếp Generative LLM chọn lọc mutant. |

## Chi tiết kiểm tra phản chứng (BƯỚC 2B)

**GAP tuyên bố:** Chưa có công trình nào sử dụng Generative LLM để trực tiếp phân tích ngữ nghĩa và chọn lọc/phân loại mutant trên source code.

| Paper | Đã làm không? | Ghi chú |
|-------|---------------|---------|
| Petrović'21 (S1, S2)| Không | Dùng aSTRA (context-based heuristics), không phải LLM. |
| Chen'25 (S3) | Không | CAMUS là Neural Network dự đoán, không phải Generative LLM. |
| Guilherme'23 (S4) | Không | Dùng ChatGPT (GPT-3.5) để sinh unit test, không phải chọn lọc mutant. |
| Garg'22 (S5) | Không | Dùng CodeBERT làm encoder (ML representation), không phải Generative reasoning. |
| Naeem'19 (S6) | Không | Dùng Machine Learning truyền thống (SVM, Decision Tree). |
| Mohanty'25 (S7) | Không | Dùng thuật toán tìm kiếm Squirrel Search (SQUMUTH). |
| Shobana'23 (S8) | Không | Dùng thuật toán tiến hóa (SBMEA). |
| Liu'23 (S9) | Không | Dùng LLMs đánh giá code, không chọn mutant cho software project. |
| Papadakis'18 (S10)| Không | Nghiên cứu thực nghiệm (Empirical study), không dùng AI. |
| Sun'18 (S11) | Không | DeepConcolic dùng cho testing DNN, không liên quan source code mutation. |
| Chekam'19 (S12) | Không | Dùng Machine Learning truyền thống (Decision Tree, LSTM). |
| Alagarsamy'24 (S13)| Không | Dùng CodeT5 để sinh test case (A3Test), không chọn mutant. |
| Li'22 (S14) | Không | Dùng thuật toán Multi-Armed Bandit (MMOS). |
| Wang'23 (S15) | Không | Dùng thuật toán PSO (SM-EOLPSO). |

$\rightarrow$ **Kết luận:** Xác nhận (GAP-T hoàn toàn tồn tại).

**GAP tuyên bố:** Không có bài báo nào (ngoại trừ Google nội bộ) đánh giá sự đánh đổi giữa hiệu quả chọn lọc (Mutation Score) và chi phí vận hành AI / năng suất lập trình viên (Effort/Cost).

| Paper | Đã làm không? | Ghi chú |
|-------|---------------|---------|
| Petrović'21 (S1, S2)| Có (một phần) | Đo Productivity Rate (89%) nhưng ở Google, không đo trực tiếp AI Inference Cost. |
| S3, S4, S6, S8-S11, S13-S15 | Không | Không nhắc đến Productivity/Cost Reduction, chỉ đo lường metrics học thuật. |
| Garg'22 (S5) | Không | Đo F-measure, MCC, không đo chi phí vận hành CodeBERT. |
| Mohanty'25 (S7) | Có (một phần) | Nhắc đến Cost Reduction gián tiếp, không tính chi phí chạy thuật toán. |
| Chekam'19 (S12) | Có (một phần) | Đo Cost Reduction gián tiếp qua tỷ lệ "killed mutants", không đo inference effort. |

$\rightarrow$ **Kết luận:** Xác nhận (GAP-M tồn tại).

## Chốt GAP cuối cùng (BƯỚC 2D)

**Kết quả đánh giá theo Quy tắc quyết định:**
- Số lượng điểm nghẽn (Blocker/❌): **0**
- Số lượng cảnh báo (Cần xử lý/⚠️): **0**
- $\rightarrow$ **Quyết định:** Mức độ đánh giá khả thi $\le$ 2 ⚠️ và không có ❌ $\rightarrow$ **An toàn — chốt tiếp tục với các GAP này.**

**Tuyên bố chốt GAP:**
Thực nghiệm sẽ tập trung giải quyết **GAP-T** (sử dụng Generative LLM trực tiếp suy luận và chọn lọc mutant) làm trọng tâm đổi mới công nghệ (Technology). Đồng thời, thiết lập framework đo lường nhằm giải quyết **GAP-M** (cân bằng giữa tỷ lệ chi phí vận hành AI và hiệu quả cắt giảm Effort) trên nền tảng **GAP-D** (dữ liệu benchmark đa ngôn ngữ mã nguồn mở).
