# Research Proposal: AI-Guided Semantic Mutation Testing for RAG
**Nhóm:** Nhóm 6
**Thành viên:** Nguyễn Quốc Huy, Bùi Lê Tấn Đạt, Nguyễn Đăng Khoa, Lê Đình Quý
**Topic code:** RT-SWT-003-nhom6
**Ngày cập nhật:** 2026-07-23
**Version:** 2.0 (Final)
**Trạng thái:** Đã hoàn thành (Cập nhật theo kết quả nghiên cứu thực tế)

---

## 2. Research Problem Statement

### 2.1 Context & Significance
Sự phụ thuộc vào các hệ thống Generative AI (như RAG) trong các enterprise applications ngày càng cao, đòi hỏi các kỹ thuật automated testing khắt khe hơn để đảm bảo reliability. Tuy nhiên, các kỹ thuật đánh giá robustness của RAG hiện tại vẫn còn hạn chế, gây khó khăn cho việc quantify mức độ resilience của hệ thống trước adversarial data, đặc biệt là lỗi nhiễm độc dữ liệu.

### 2.2 State of the Art
Trong lĩnh vực RAG testing, Momtaz et al. (2026) là nghiên cứu tiên phong áp dụng Mutation Testing, nhưng mới chỉ giới hạn ở các mutation operators cơ bản (rule-based) trên văn bản. Song song đó, việc ứng dụng LLM làm giám khảo (LLM-as-a-Judge) đang trở nên phổ biến, nhưng độ tin cậy của chúng khi phân biệt giữa việc tuân thủ dữ liệu sai (Faithful) và tự sửa lỗi bằng tham số (Inconsistent) chưa được đánh giá ở quy mô lớn.

### 2.3 GAP
Mặc dù mutation testing đã bắt đầu được áp dụng cho RAG (Momtaz 2026), **chưa có nghiên cứu thực nghiệm quy mô lớn nào đánh giá xem lỗ hổng đối với đột biến ngữ nghĩa (semantic poisoning) thay đổi như thế nào khi mở rộng kích thước mô hình (Model Scale)** và **khi triển khai trên dữ liệu nội bộ (Private Data)**. Khoảng trống này tạo ra sự lầm tưởng rằng mô hình càng lớn thì càng an toàn, và System Prompt là giải pháp bảo vệ tuyệt đối.

### 2.4 Motivation
Nếu không lấp đầy GAP này, các hệ thống RAG enterprise sẽ được triển khai với false sense of security. Khi đối mặt với adversarial context tinh vi (đặc biệt là dữ liệu nội bộ không có trong pretraining), RAG có nguy cơ nhiễm độc cao mà System Prompt thông thường không thể chống đỡ. Việc làm rõ The Inverse Scaling Law (Định luật tỷ lệ nghịch) sẽ giúp định hình lại chiến lược bảo mật cho các hệ thống AI.

---

## 3. Related Work

### 3.1 Overview
| Paper | Tiêu điểm | Best result / Finding | Hạn chế chính đối với RAG Testing |
|---|---|---|---|
| Momtaz et al. (2026) | Mutation Testing cho RAG | Abstain rate đạt 66% khi xóa Prompt | Chỉ dùng rule-based mutations, quy mô nhỏ. |
| McKenzie et al. (2023) | Inverse Scaling Prize | Phát hiện nhiều task LLM càng lớn càng kém | Chưa áp dụng đánh giá trên cấu trúc RAG pipeline. |
| Y. Zhang et al. (2023) | LLM-as-a-Judge | Đạt thỏa thuận cao với con người | Đánh giá chung, chưa đi sâu vào phân tích mâu thuẫn context-parametric. |

### 3.2 Khái niệm Đo lường (Metrics / Labels)
Trong thực nghiệm cuối cùng, mọi phản hồi được LLM-as-a-Judge phân loại vào 1 trong 4 nhãn (Labels) triệt để:
- **Abstain (An toàn):** Hệ thống phát hiện mâu thuẫn và từ chối trả lời.
- **Faithful (Bị đánh lừa):** Hệ thống tin tưởng mù quáng vào context bị nhiễm độc.
- **Inconsistent (Vi phạm RAG):** Hệ thống lén lút sửa lỗi trong context dựa trên kiến thức tham số (Parametric Knowledge).
- **Hallucination (Ảo giác):** Sinh ra thông tin hoàn toàn không liên quan đến cả context và sự thật.

---

## 4. Research Questions

> **RQ1 (Model Scale):** Kích thước mô hình (8B vs. 17B) ảnh hưởng như thế nào đến mức độ dễ bị tổn thương trước nhiễm độc ngữ nghĩa khi không được bảo vệ bởi System Prompts?
- **Hypothesis:** Trái với trực giác (Inverse Scaling Law), mô hình lớn hơn (17B) sẽ dễ bị tổn thương hơn mô hình nhỏ (8B) do khả năng hợp lý hóa logic sai lệch tốt hơn.

> **RQ2 (Data Domain / Parametric Shield):** Miền dữ liệu (Public vs. Private) ảnh hưởng ra sao đến khả năng mô hình tự sửa lỗi (Inconsistent) thay vì bị đánh lừa (Faithful)?
- **Hypothesis:** Trên dữ liệu Private, mô hình mất đi "Parametric Shield" (khiên tham số), dẫn đến tỷ lệ Inconsistent giảm mạnh và Faithful tăng đột biến.

> **RQ3 (Prompt Engineering):** Prompt Engineering có thể giảm thiểu tác động của nhiễm độc ngữ nghĩa đến mức độ nào trên các kích thước mô hình khác nhau?
- **Hypothesis:** System Prompt sẽ cải thiện đáng kể Abstain Rate (hoạt động như màng lọc phòng thủ), nhưng không thể đạt ngưỡng an toàn tuyệt đối ($\ge 90\%$).

---

## 5. Experiment Protocol (Actual Implementation)

### 5.1 Dataset (AI-Generated Semantic Mutations)
- **Quy mô:** $416$ đột biến ngữ nghĩa.
- **Miền dữ liệu:** Bao gồm **Public Data** (FastAPI documentation) và **Private Data** (Tài liệu nội bộ, không có trên internet).
- **Cách sinh đột biến:** Sử dụng Llama 3.1 70B/Qwen 3 để tinh chỉnh ngữ nghĩa (thay đổi giá trị, đảo ngược logic, sai lệch API param).

### 5.2 RAG Configurations Evaluated
Để cô lập tác động của quy mô mô hình, dữ liệu và prompt, thực nghiệm chạy 5 cấu hình:
1. Llama 3.1 17B (With Prompt)
2. Llama 3.1 17B (No Prompt)
3. Llama 3.1 8B (With Prompt)
4. Llama 3.1 8B (No Prompt)
5. Llama 3.1 17B (With Prompt, Private Data)

### 5.3 LLM-as-a-Judge Evaluation Pipeline
- **Mô hình giám khảo:** `Llama 4 Scout 17B`.
- **Phương pháp:** Prompting Few-Shot nâng cao với Chain-of-Thought (Yêu cầu mô hình giải thích lý do trước khi gán nhãn).
- **Validation:** Tiến hành Cross-validation thủ công bởi các thành viên trong nhóm trên 110 mẫu, đạt chỉ số **Cohen's Kappa $k > 0.73$**, chứng minh độ tin cậy cao của phương pháp tự động hóa.

### 5.4 Key Findings (Tổng kết thực tế)
- **Inverse Scaling Law:** Không có Prompt, 17B chỉ Abstain $3.61\%$, trong khi 8B Abstain $42.55\%$.
- **Parametric Shield:** Chuyển sang Private Data, 17B Inconsistent giảm xuống $2.88\%$, Faithful vọt lên $45.19\%$.
- **Prompt Defense:** Prompt giúp tăng Abstain từ $3.61\%$ lên $60.10\%$ (17B), nhưng vẫn không an toàn tuyệt đối.
- **Hallucination Myth:** Tỷ lệ Hallucination thực tế cực thấp ($\le 0.24\%$). Mối đe dọa lớn nhất là **Faithful**.

---

## 6. Threats to Validity (Đã được khắc phục)

### 6.1 Internal Validity
**Threat:** LLM-as-a-Judge có thể thiên vị hoặc đánh giá sai các câu trả lời vi tế (inconsistent).
**Mitigation:** Thay thế Llama 3.1 8B ban đầu bằng `Llama 4 Scout 17B` mạnh mẽ hơn, kết hợp Chain-of-Thought và kiểm chứng chéo bằng con người ($k > 0.73$).

### 6.2 External Validity
**Threat:** Kết quả có thể chỉ đúng với một loại dữ liệu (Public).
**Mitigation:** Đưa thêm **Private Data** vào thực nghiệm để mô phỏng chính xác môi trường Enterprise RAG, dẫn đến phát hiện về "Parametric Shield".

---

## 7. Timeline & Resources (Đã hoàn tất)

| Phân công | Thành viên | Trách nhiệm thực thi |
|---|---|---|
| **PL (Trưởng nhóm)** | Nguyễn Quốc Huy | Thiết kế phương pháp, Code LLM-as-a-Judge, Viết báo cáo khoa học. |
| **DG (Dữ liệu)** | Bùi Lê Tấn Đạt | Xây dựng 416 Mutations (FastAPI & Private), Cross-validation. |
| **LR (Thực thi)** | Nguyễn Đăng Khoa | Vận hành RAG pipeline, cấu hình System Prompts. |
| **MS (Thống kê)** | Lê Đình Quý | Phân tích Log, Trích xuất số liệu Abstain/Faithful/Inconsistent. |

**Chi phí thực tế:** Hoàn toàn miễn phí thông qua Groq API, HuggingFace và hạ tầng mã nguồn mở. Toàn bộ mã nguồn và dữ liệu đã được tổng hợp tại repository GitHub nhóm.
