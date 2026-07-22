# Research Proposal: AI-Guided Semantic Mutation Testing for RAG
**Nhóm:** Nhóm 6
**Thành viên:** Nguyễn Quốc Huy, Bùi Lê Tấn Đạt, Nguyễn Đăng Khoa, Lê Đình Quý
**Topic code:** RT-SWT-003-nhom6
**Ngày nộp:** 2026-07-23
**Version:** 2.0 (Final)
**Trạng thái:** Đã hoàn thành (Cập nhật theo thực tế)

---

## 2. Research Problem Statement

### 2.1 Context & Significance
Sự phụ thuộc vào các hệ thống Generative AI (như RAG) trong các enterprise applications ngày càng cao, đòi hỏi các kỹ thuật automated testing khắt khe hơn để đảm bảo reliability. Tuy nhiên, các kỹ thuật đánh giá robustness của RAG hiện tại vẫn còn hạn chế, gây khó khăn cho việc quantify mức độ resilience của hệ thống trước adversarial data, đặc biệt là khi dữ liệu ngữ cảnh bị nhiễm độc (semantic poisoning).

### 2.2 State of the Art
Trong lĩnh vực RAG testing, Momtaz et al. (2026) là nghiên cứu tiên phong áp dụng Mutation Testing, nhưng mới chỉ giới hạn ở các mutation operators cơ bản (rule-based) trên văn bản. Song song đó, ở mảng đánh giá mô hình, việc sử dụng LLM-as-a-Judge đang ngày càng phổ biến nhưng khả năng của chúng trong việc phân định các hành vi vi tế như Inconsistent (tự sửa lỗi bằng tham số) và Faithful (bị đánh lừa hoàn toàn) chưa được kiểm chứng đầy đủ ở quy mô lớn.

### 2.3 GAP
Mặc dù mutation testing đã bắt đầu được áp dụng cho RAG (Momtaz 2026), **chưa có nghiên cứu thực nghiệm quy mô lớn nào đánh giá xem lỗ hổng đối với đột biến ngữ nghĩa thay đổi như thế nào khi mở rộng kích thước mô hình (Model Scale)** và **khi triển khai trên dữ liệu nội bộ (Private Data)**. Khoảng trống này thuộc loại **GAP-T (Technology Gap)** và tạo ra một niềm tin sai lệch (false sense of security) rằng mô hình càng lớn thì càng an toàn và System Prompt là lớp khiên bảo vệ vạn năng.

### 2.4 Motivation
Nếu không lấp đầy GAP này, các hệ thống RAG sẽ tiếp tục được đánh giá safety dựa trên những giả định sai lầm. Khi deploy vào production (đặc biệt là trên private data), RAG dễ bị vulnerable trước các data poisoning attacks tinh vi mà System Prompt không thể detect. Việc khám phá Định luật Tỷ lệ nghịch (Inverse Scaling Law) sẽ định hình lại phương pháp kiểm thử an ninh cho AI.

---

## 3. Related Work

### 3.1 Overview
| Paper | Tool/LLM | Dataset (size) | Metric | Best result | Hạn chế chính |
|---|---|---|---|---|---|
| Momtaz et al. (2026) | GPT-4, Llama-2 | QASper, Heritage (32 queries) | Hallucination Rate, Abstain Rate | Abstain rate đạt 66% khi xóa System Prompt | Chỉ dùng đột biến rule-based (cắt xén thủ công), quy mô nhỏ. |
| McKenzie et al. (2023) | Inverse Scaling Prize | Các task suy luận | Accuracy | Phát hiện nhiều task LLM càng lớn càng kém | Chưa áp dụng đánh giá trên kiến trúc RAG. |
| Chu et al. (2026) | SLR | 61 papers | N/A | Xác định 5 xu hướng GenAI trong SE | Là bài tổng quan (Review), không có thực nghiệm đánh giá cụ thể. |
| Moran et al. (2023) | LLM Fuzzer | Web UI Dataset | Coverage | Phát hiện 23 bug mới | Chỉ tập trung vào giao diện UI, không áp dụng cho cấu trúc RAG pipeline. |
| Chen et al. (2024) | RAGAS | Wikipedia (10k) | Faithfulness, Answer Relevance | 85% tương quan với chuyên gia (Human) | Chỉ là framework đo lường, không tích hợp cơ chế tiêm lỗi tự động. |

**Giải thích thuật ngữ đo lường (Metrics):**
- **Hallucination Rate:** Tỷ lệ hệ thống sinh ra thông tin hoàn toàn bịa đặt, không có trong ngữ cảnh và không có thật trong kiến thức tham số.
- **Abstain Rate:** Tỷ lệ hệ thống phòng vệ thành công bằng cách chủ động từ chối trả lời do phát hiện mâu thuẫn trong ngữ cảnh.
- **Faithful Rate:** Tỷ lệ hệ thống tin tưởng và sinh ra câu trả lời tuân thủ hoàn toàn theo ngữ cảnh đã bị nhiễm độc (Bị đánh lừa).
- **Inconsistent Rate:** Tỷ lệ hệ thống lén lút sửa lỗi trong ngữ cảnh bằng cách sử dụng kiến thức tham số nội tại (Vi phạm nguyên tắc RAG).
- **Answer Relevance (Độ liên quan):** Thước đo đánh giá câu trả lời có đi đúng vào trọng tâm câu hỏi gốc hay không (chống lạc đề).
- **Coverage:** Độ bao phủ kiểm thử, thể hiện tỷ lệ không gian dữ liệu hoặc mã nguồn đã được quét qua bởi hệ thống fuzzing/testing.

**Giải thích công cụ & phương pháp (Tool/LLM):**
- **GPT-4, Llama-2:** Các mô hình ngôn ngữ lớn (LLM) hiện đại, đại diện cho AI tạo sinh, thường được dùng để sinh lỗi hoặc đóng vai trò giám khảo (LLM-as-a-Judge).
- **SMART (Semantic Mutation Testing):** Phương pháp/công cụ sử dụng LLM để tự động phân tích và sinh ra các lỗi ngữ nghĩa (semantic mutants) tinh vi trên mã nguồn.
- **SLR (Systematic Literature Review):** Đánh giá tài liệu có hệ thống. Đây là một phương pháp luận nghiên cứu (methodology) thay vì một công cụ phần mềm.
- **LLM Fuzzer:** Khung kiểm thử tự động (Fuzzing framework) ứng dụng LLM để sinh các dữ liệu đầu vào đột biến liên tục nhằm tìm kiếm lỗ hổng hoặc bug trong ứng dụng.
- **RAGAS:** Một framework chuyên biệt mã nguồn mở dùng để đo lường và đánh giá chất lượng (evaluation) của các luồng RAG (Retrieval-Augmented Generation).
### 3.2 Pattern Analysis
- **Sự chuyển dịch của công cụ Mutation Testing từ Rule-based sang Generative AI** - thể hiện qua [Wang et al. (2026), Chu et al. (2026), Moran et al. (2023)]. Các LLM được chứng minh có khả năng sinh các đột biến ngữ nghĩa tinh vi và bám sát bối cảnh thực tế hơn nhiều so với thao tác chuỗi (string manipulation) truyền thống.
- **Việc kiểm thử hệ thống RAG vẫn đang trong giai đoạn sơ khai và phụ thuộc vào dữ liệu giả lập thủ công** - thể hiện qua [Momtaz et al. (2026), Chen et al. (2024)]. Việc phát hiện ra các định luật (Scaling Laws) trong RAG chưa thực sự được chú trọng.

### 3.3 GAP Mapping
| GAP-T/M/D/S | Evidence (số paper support) | Status |
|---|---|---|
| **GAP-T:** Thiếu thực nghiệm quy mô lớn đánh giá The Inverse Scaling Law của RAG trước đột biến ngữ nghĩa. | 30 papers (Chưa có bài nào phân tích sâu về tỷ lệ thuận/nghịch của quy mô mô hình trong RAG). | Confirmed |
| **GAP-D:** Chưa đánh giá độ tin cậy của RAG trên Private Data (Enterprise docs) so với Public Data. | 1 paper (Momtaz 2026 chỉ kiểm thử trên tài liệu công khai có trong pretraining). | Confirmed |

---

## 4. Research Questions

> **RQ1 (Model Scale vs Vulnerability):** [P: Hệ thống RAG không sử dụng System Prompt] + [I: Khi tiếp nhận các đột biến ngữ nghĩa] có bộc lộ [O: Tỷ lệ Abstain (An toàn) suy giảm khi tăng kích thước mô hình (8B vs 17B)] không?

**Classification:** Comparative study giữa hai kích thước mô hình (Model Scale).
**H0:** Tỷ lệ Abstain của mô hình 17B $\ge$ mô hình 8B.
**H1:** Tỷ lệ Abstain của mô hình 17B $<$ mô hình 8B (Inverse Scaling Law).

**Metric:** Abstain Rate (Được đánh giá tự động bởi `Llama 4 Scout 17B`).
**Significance Threshold:** $p < 0.05$ - So sánh hiệu năng phòng thủ giữa hai mô hình có kích thước tham số khác biệt trên cùng một tập dữ liệu.
**Statistical Test:** Two-Proportion Z-test ($\alpha = 0.05$). Rationale: Cần so sánh 2 tỷ lệ độc lập trên 2 nhóm (17B và 8B).

---

> **RQ2 (Data Domain & Parametric Shield):** [P: Hệ thống RAG sử dụng Llama 3.1 17B] + [I: Khi chạy trên dữ liệu Private (không có trong pretraining)] có duy trì được [O: Tỷ lệ tự sửa lỗi (Inconsistent Rate)] so với khi chạy trên Public Data không?

**Classification:** Comparative study giữa hai miền dữ liệu.
**H0:** Tỷ lệ Inconsistent trên Private Data $\ge$ trên Public Data.
**H1:** Tỷ lệ Inconsistent trên Private Data $<$ trên Public Data (Mất đi khiên tham số).

**Metric:** Inconsistent Rate (Tỷ lệ hệ thống lén sửa lỗi dựa vào kiến thức học trước đó).
**Significance Threshold:** $p < 0.05$ - Đánh giá rủi ro khi triển khai RAG trên môi trường Enterprise nội bộ.
**Statistical Test:** Two-Proportion Z-test ($\alpha = 0.05$). Rationale: Phân tích sự thay đổi hành vi giữa tập Public và Private.

---

## 5. Experiment Protocol

### 5.1 Experiment Pipeline
*(Trình tự thực thi dựa trên Execution Runbook của nhóm)*

#### Giai đoạn 1: Chuẩn bị Dữ liệu (Tuần 5-6)
**Trách nhiệm chính:** Bùi Lê Tấn Đạt (DG) | **Hỗ trợ:** Nguyễn Quốc Huy (PL)

1. **Thu thập tập dữ liệu gốc:** Tải toàn bộ tài liệu kỹ thuật từ kho lưu trữ GitHub của FastAPI (Public) và tài liệu API nội bộ (Private).
2. **Tiền xử lý dữ liệu (Data Preprocessing):** Sử dụng mã lệnh Python để loại bỏ các thẻ HTML/CSS không cần thiết, trích xuất cấu trúc văn bản thuần túy theo định dạng Markdown.
3. **Trích xuất ngữ cảnh:** Lấy ngẫu nhiên **32 đoạn văn bản** (tương đương 1 tài liệu hoặc 1 section hoàn chỉnh). Lưu trữ kết quả tại `data/raw/contexts.json`.
4. **Xây dựng tập truy vấn (Ground Truth):** Dựa trên 32 ngữ cảnh tham chiếu, tiến hành soạn thảo thủ công **32 câu truy vấn**.
   - *Lưu ý:* Phân bổ đa dạng các cấp độ câu hỏi: Trích xuất thông tin (Factoid), Tổng hợp, Suy luận (Reasoning), và Ứng dụng mã nguồn.
5. **Lưu trữ:** Tạo tập dữ liệu `data/raw/test_cases.csv` bao gồm 3 trường thông tin: `id`, `context_text`, `query`.

#### Giai đoạn 2: Thiết lập Baseline - Đo lường Điểm chuẩn (Tuần 6)
**Trách nhiệm chính:** Nguyễn Đăng Khoa (LR)

1. **Khởi tạo Cơ sở dữ liệu Vector (VectorDB):** Nạp 32 tài liệu tham chiếu (văn bản sạch) vào Workspace của AnythingLLM.
2. **Thực thi truy vấn:** Triển khai mã lệnh Python để tương tác với API AnythingLLM, gửi tuần tự 32 câu truy vấn vào hệ thống.
3. **Thu thập Log:** Lưu lại toàn bộ phản hồi từ AnythingLLM vào tệp `results/baseline_responses.csv` (Cấu trúc: `id`, `query`, `baseline_answer`).

#### Giai đoạn 3: Tiêm Đột Biến Ngữ Nghĩa (Tuần 7)
**Trách nhiệm chính:** Nguyễn Đăng Khoa (LR) | **Review:** Nguyễn Quốc Huy (PL)

1. **Tương tác API Qwen 3 / Llama 70B:** Phát triển mã lệnh truyền các đoạn `context_text` vào cấu hình mô hình (`temperature=0.7`).
   - *Mục tiêu:* Yêu cầu LLM tinh chỉnh cấu trúc ngữ nghĩa nhằm tạo ra sai lệch về logic hoặc thông số kỹ thuật (Semantic Mutations).
2. **Xác thực dữ liệu (Validation):** Triển khai các biểu thức chính quy (Regex) để kiểm tra tính toàn vẹn định dạng Markdown và nội dung trả về. Nếu văn bản trả về rỗng, tiến hành gọi lại API tự động.
3. **Lưu trữ:** Đảm bảo sinh 13 phiên bản đột biến cho mỗi ngữ cảnh gốc. Lưu trữ tổng cộng $416$ mẫu dữ liệu vào tệp `data/mutated/semantic_mutants.csv`.

#### Giai đoạn 4: Đánh giá Lỗ hổng RAG (Tuần 7 - 8)
**Trách nhiệm chính:** Nguyễn Đăng Khoa (LR)

1. **Khởi tạo 416 Workspace độc lập:** Khởi tạo 416 Workspace trên hệ thống AnythingLLM. Thiết lập cho 5 cấu hình: 17B (có/không prompt), 8B (có/không prompt), và 17B Private Data.
2. **Triển khai truy vấn tự động (Cross-querying):** Vận hành mã lệnh để duyệt qua toàn bộ 416 Workspace. Tại mỗi Workspace, hệ thống sẽ tự động trích xuất và gửi truy vấn (`query`) tương ứng với tài liệu đột biến đang được nhúng tại đó.
3. **Thu thập kết quả (Full Batch):** Ghi nhận lại toàn bộ 416 luồng phản hồi từ hệ thống RAG cho mỗi cấu hình.
4. **Thu thập kết quả:** Ghi nhận lại toàn bộ luồng phản hồi vào tệp `results/mutated_responses.csv`.
   - *Nguyên tắc toàn vẹn dữ liệu:* Trong trường hợp timeout hoặc hệ thống bị sập, gán nhãn kết quả là `Abstain` (Từ chối). Tuyệt đối không can thiệp thủ công vào dữ liệu.

#### Giai đoạn 5: Đánh giá Tự động bằng LLM (LLM-as-a-Judge)
**Trách nhiệm chính:** Lê Đình Quý (MS) | **Human Eval:** Bùi Lê Tấn Đạt (DG) | **Oversight:** Nguyễn Quốc Huy (PL)

1. **Chấm điểm bằng AI:** Phát triển mã lệnh chuyển giao bộ dữ liệu làm đầu vào cho LLM (`Llama 4 Scout 17B`), yêu cầu phân loại đầu ra thành 1 trong 4 nhãn (kèm Chain-of-Thought qua trường `reason`). 
   - `Faithful`: Phản hồi tuân thủ hoàn toàn ngữ cảnh bị đột biến (Bị đánh lừa).
   - `Abstain`: Hệ thống chủ động từ chối trả lời (An toàn).
   - `Inconsistent`: Phản hồi khớp sự thật nhưng mâu thuẫn ngữ cảnh (Vi phạm RAG).
   - `Hallucination`: Sinh thông tin sai lệch không liên quan (Ảo giác).
2. **Kiểm định độ tin cậy (Construct Validity):** Lấy mẫu ngẫu nhiên 110 câu phản hồi để tiến hành đánh giá mù (blind evaluation) thủ công độc lập.
3. **Xác minh chỉ số Kappa:** Tính toán chỉ số Cohen's Kappa giữa kết quả chuyên gia và Llama 4 Scout. Xác thực mức độ tin cậy đạt $k > 0.73$.

#### Giai đoạn 6: Phân Tích Thống Kê (Tuần 8)
**Trách nhiệm chính:** Lê Đình Quý (MS) | **Final Review:** Nguyễn Quốc Huy (PL)

Triển khai thư viện `scipy.stats` để kiểm định phân phối kết quả ở Giai đoạn 5.
1. **Kiểm định RQ1:**
   - So sánh tỷ lệ Abstain Rate giữa mô hình 8B và 17B trong cấu hình No Prompt.
   - Áp dụng kiểm định thống kê nhằm xác nhận Inverse Scaling Law.
   - Phân tích Effect size (Cohen's $d$) và đánh giá ngưỡng bác bỏ ($p < 0.05$).
2. **Kiểm định RQ2:**
   - So sánh tỷ lệ Inconsistent Rate giữa Public và Private data.
   - Áp dụng kiểm định để khẳng định mô hình mất đi Parametric Shield khi không có pretraining data.
3. **Trình bày kết quả:** Biên soạn báo cáo trên Jupyter Notebook `full_analysis.ipynb` để hỗ trợ quá trình diễn giải khoa học.

#### 🚨 Yêu cầu Thử nghiệm Pilot (Tuần 7)
- Quy trình gồm 6 giai đoạn trên **bắt buộc phải được chạy thử nghiệm ở quy mô nhỏ (Pilot)** (khoảng 5 truy vấn) trong Tuần 7.
- Trong trường hợp phát sinh lỗi hệ thống, giới hạn API hoặc dữ liệu hỏng, Trưởng nhóm (PL) có trách nhiệm nộp đơn Amendment cho Giảng viên trong vòng 24 giờ.
- Chỉ khi thực nghiệm Pilot đạt kết quả ổn định, Tuần 8 mới tiến hành chạy toàn bộ lô dữ liệu (Full Batch) với 416 mẫu. Tuyệt đối không bỏ qua bước thử nghiệm.

### 5.2 Dataset
**Tên tập dữ liệu:** FastAPI Documentation & Internal Systems Docs | **Nguồn:** `github.com/fastapi/fastapi` và dữ liệu riêng | **Quy mô (N):** 32 đoạn văn bản + 32 truy vấn | **Miền dữ liệu (Domain):** Kỹ thuật phần mềm / API | **Tiền xử lý:** Lọc thẻ HTML/CSS, định dạng Markdown nguyên bản | **Chiến lược lấy mẫu:** Lấy mẫu ngẫu nhiên từ các tài liệu.
**Cơ sở lựa chọn:** Việc sử dụng kết hợp dữ liệu Public và Private giúp đánh giá chính xác tác động của Parametric Shield.

### 5.3 LLM/Tool Configuration
- **AI Models:** Llama 3.1 70B (Mutation Generator), Llama 3.1 8B/17B (SUT), `llama-4-scout-17b` (LLM-as-a-Judge).
- **Hyperparameters:** `temperature = 0.7`, `top_p = 0.95`.
- **Prompting Strategy (LLM Judge):** Thay vì Zero-Shot, áp dụng **Advanced Few-Shot Prompting** ($k=3$), tiêm trực tiếp các ví dụ hóc búa (đặc biệt là lỗi sửa code lén lút) vào Prompt để định hướng AI phân loại chuẩn xác.
- **Mẫu Prompt (Mutation Generator):** *"You are an expert software tester. Given the following paragraph from an API documentation, rewrite it to contain a subtle factual error (e.g., change a return status code, invert a logical condition) while maintaining perfect grammar and logical flow. Output ONLY the mutated text, no explanations."*
- **Rationale:** Chiến lược sử dụng LLM thay thế static rules (rule-based) tạo ra đột biến thực tế hơn. 

### 5.4 Measurement
**Metrics:** Abstain, Faithful, Inconsistent, Hallucination | **Evaluation Tool:** `Llama 4 Scout 17B` | **Ground Truth:** Cấu trúc API Docs nguyên bản | **Inter-Annotator Agreement (IAA):** Cohen's Kappa ($k > 0.73$) thực hiện chéo giữa các evaluators độc lập trên tập mẫu $N=110$ nhằm validate độ chính xác của LLM Judge.

### 5.5 Baseline (Áp dụng cho cấu trúc so sánh)
- **Tên kỹ thuật:** Cấu hình RAG nguyên bản không có System Prompt (No Prompt Config).
- **Cấu hình tái tạo (Reproducibility):** Triển khai Llama 3.1 với conversational fine-tuning mặc định, không tiêm bất kỳ bộ lọc phòng thủ nào để làm chuẩn đối chiếu (baseline) đánh giá sức mạnh của Prompt Engineering.

### 5.6 Statistical Analysis Plan
- **Kiểm định:** Two-Proportion Z-test - [one-tailed] được áp dụng cho cả RQ1 và RQ2 vì giả thuyết có định hướng rõ ràng (Inverse Scaling và Parametric Shield).
- **Lý luận thống kê:** Đáp ứng đầy đủ điều kiện so sánh 2 tỷ lệ độc lập, không yêu cầu giả định phân phối chuẩn trên dữ liệu liên tục.
- **Độ lớn tác động (Effect size):** Cohen's $d$ (Đo lường mức độ ảnh hưởng của các biến thể đột biến).
- **Cỡ mẫu và Năng lực kiểm định (Power):** Thiết lập $N = 416$ mẫu kiểm thử ($32 \text{ queries} \times 13 \text{ operators}$). Phân tích xác nhận Power $\ge 0.80$, thỏa mãn cỡ mẫu.

---

## 6. Evaluation Plan

### 6.1 Evaluation Criteria

| RQ | Metric | Significance Threshold | Statistical Test | Reject H0 when... | Negative Result Interpretation |
|---|---|---|---|---|---|
| **RQ1** | Abstain Rate (17B vs 8B) | Mức ý nghĩa $\alpha = 0.05$ | Z-test | $p < 0.05$ (17B Abstain thấp hơn hẳn 8B) | Có. Khẳng định quy mô mô hình lớn tỉ lệ thuận với an ninh hệ thống (Scale implies Safety). |
| **RQ2** | Inconsistent Rate (Private) | Mức ý nghĩa $\alpha = 0.05$ | Z-test | $p < 0.05$ (Private Inconsistent suy giảm đáng kể) | Có. Chứng minh mô hình không phụ thuộc vào pretraining data để tự sửa lỗi. |

### 6.2 Result Interpretation Matrix
- **Kịch bản 1: Double Positive (RQ1 và RQ2 cùng bác bỏ H0):** Mô hình lớn dễ dính độc hơn (Inverse Scaling Law), và RAG nội bộ dễ bị lừa hơn do mất khiên tham số (Parametric Shield). $\rightarrow$ **Kết luận khoa học:** Đặt ra cảnh báo đỏ cho các doanh nghiệp: Mô hình RAG càng lớn triển khai trên dữ liệu nội bộ càng rủi ro, cần biện pháp bảo vệ kiến trúc sâu hơn.
- **Kịch bản 2: Mixed (Một RQ bị bác bỏ):** Hiện tượng Inverse Scaling tồn tại nhưng dữ liệu Private không ảnh hưởng, hoặc ngược lại. $\rightarrow$ **Kết luận khoa học:** Rủi ro an ninh bị phụ thuộc mạnh vào một trong hai biến số, cần đào sâu tối ưu biến số còn lại.
- **Kịch bản 3: Double Negative (Cả RQ1 và RQ2 đều không thể bác bỏ H0):** Mô hình lớn an toàn hơn, Private data an toàn như Public data. $\rightarrow$ **Kết luận khoa học:** Kiến trúc RAG hiện tại đã đủ mạnh, chỉ cần scale up mô hình là giải quyết được bài toán Semantic Poisoning.

### 6.3 Sub-group Analysis
- **Tiêu chí phân cụm:** Tiến hành phân tách phản hồi dựa trên cấu hình Prompt Engineering (With vs Without Prompt).
- **Điều kiện thực thi:** Sự phân hoạch này được cố định hoàn toàn TRƯỚC thời điểm triển khai thực nghiệm. Mục tiêu chính là đánh giá xem System Prompt có thể đóng vai trò như một màng lọc đảo ngược (tạo ra lá chắn nhân tạo) cho mô hình lớn hay không.

---

## 7. Threats to Validity

### 7.1 Internal Validity
**Threat 1:** LLM-as-a-Judge có thể gặp khó khăn trong việc phân tách ranh giới mỏng manh giữa `Faithful` và `Inconsistent` trên các mutations cực kỳ tinh vi.
**Mitigation:** Ứng dụng mô hình `Llama 4 Scout 17B` với năng lực lý luận cao, buộc mô hình xuất ra chuỗi suy luận (Chain-of-Thought) vào biến `reason` trước khi ra quyết định gán nhãn cuối cùng.

**Threat 2:** Semantic mutations sinh ra có thể bị lỗi syntax.
**Mitigation:** Ứng dụng preprocessing script bằng Regex để validate Markdown syntax TRƯỚC KHI ingest data vào VectorDB.

### 7.2 External Validity
**Threat:** Việc giới hạn experiment trên một document structure (FastAPI Docs) có khả năng làm suy giảm generalizability đối với các hệ thống RAG nội bộ.
**Mitigation:** Triển khai thêm **Private Data** vào thực nghiệm để đối chiếu rủi ro thực tế trong Enterprise deployment (Parametric Shield).

### 7.3 Construct Validity
**Threat:** Việc triển khai LLM vào vai trò phân loại tự động (LLM-as-a-Judge) tiềm ẩn annotation bias và không phản ánh chính xác nhận định của con người.
**Mitigation:** Tiến hành random sampling $N=110$ test cases và tổ chức blind human evaluation độc lập. Sau đó, tính toán Inter-Rater Agreement (Cohen's Kappa). Kết quả từ LLM Judge đạt Kappa $> 0.73$, xác thực tính đúng đắn.

### 7.4 Conclusion Validity
**Threat:** Sample size hạn chế dẫn đến nguy cơ thiếu hụt Statistical Power.
**Mitigation:** Experimental framework được design để generate chính xác $N = 416$ paired test samples. Sample size này vượt trội so với yêu cầu, đảm bảo Power thực tế $\ge 0.80$.

---

## 8. Timeline & Resources

### 8.0 Phân công vai trò
| Role | Thành viên | Trách nhiệm thực thi |
|---|---|---|
| **PL** | Nguyễn Quốc Huy | Thiết kế mã nguồn (Coding), viết script tự động hóa LLM-as-a-Judge, viết báo cáo. |
| **DG** | Bùi Lê Tấn Đạt | Thiết kế 416 mutations, thu thập Private/Public data, Cross-validation. |
| **LR** | Nguyễn Đăng Khoa | Chạy code thực nghiệm RAG pipeline, cấu hình System Prompts. |
| **MS** | Lê Đình Quý | Chạy code phân tích Log và trích xuất số lượng nhãn từ JSON logs. |
| **RW** | Nguyễn Quốc Huy | Chịu trách nhiệm tổng hợp kết quả, soạn thảo văn bản báo cáo và vẽ biểu đồ. |

### 8.1 Resource Inventory
| Tài nguyên | Trạng thái | Owner | Ghi chú |
|---|---|---|---|
| Dataset | ✅ | DG | FastAPI Docs + Internal Enterprise Data |
| API key | ✅ | LR | Groq (Llama 3.1, Llama 4 Scout) |
| Máy chủ / Máy tính | ✅ | LR | Chạy cục bộ (AnythingLLM) |
| Ground truth | ✅ | DG | Hoàn tất Cross-validation (Kappa > 0.73) |

### 8.2 Chi phí ước tính
| Hạng mục | Số lượng | Đơn giá | Tổng chi phí |
|---|---|---|---|
| Llama 3.1 / 70B (Mutation) | 416 requests | Free | $0.00 |
| Llama 4 Scout 17B (Judge) | 416 requests | Free (Groq API) | $\sim \$0.00$ |
| AnythingLLM Desktop (SUT) | 1 software | Free | $0.00 |
| **Tổng cộng** | | | **$\sim \$0.00$** |

### 8.3 Timeline chi tiết (Tuần 5-10)
> **Tuần 5-6:** Song song hoàn thiện bản đề xuất (proposal) và cấu hình tài nguyên.
> **Tuần 7-8:** Khởi chạy thực nghiệm chuyên sâu (RBL-4).
> **Tuần 9-10:** Biên soạn báo cáo khoa học và trình bày (RBL-5).

| Tuần | Hoạt động | Owner | Checkpoint (Đầu ra dự kiến) |
|---|---|---|---|
| **5** | Soạn thảo proposal §2-§7 | DG + RW + PL | Bản thảo §2-§7 hoàn chỉnh |
| **5** | Xác minh và tải bộ dữ liệu | DG | Thư mục `data/raw/` + README |
| **5** | Khởi tạo API, xác thực kết nối | LR | Mã lệnh `test_api.py` hoạt động kèm log |
| **5** | Triển khai mã lệnh tính toán sơ bộ | MS | Bản nháp `compute_metric.py` |
| **6** | Hoàn tất cấu trúc tài nguyên, nộp bản hoàn chỉnh | PL | Tài liệu `proposal.md` v1.0 |
| **6** | $\star$ **Giảng viên phê duyệt** | GV | Trạng thái: Approved |
| **7** | Thiết lập ground truth giai đoạn Pilot | DG | Tập `data/pilot_ground_truth.csv` |
| **7** | Triển khai mô hình trên mẫu Pilot | LR | Log `results/pilot_llm_output.csv` |
| **7** | Đánh giá phân phối kết quả Pilot | MS | Báo cáo `results/pilot_analysis.ipynb` |
| **7** | **Đánh giá tổng thể Pilot** $\rightarrow$ Cập nhật Amendment (nếu cần) | PL | Biên bản cuộc họp. Tài liệu Amendment nộp Giảng viên |
| **8** | Định hình ground truth toàn diện | DG | Tập `data/full_ground_truth.csv` (IAA $\ge 0.60$) |
| **8** | Vận hành toàn bộ lô thực nghiệm (Full batch) | LR | Log kết quả và ngân sách `results/full_llm_output.csv` |
| **8** | Phân tích thống kê diện rộng | MS | Notebook `results/full_analysis.ipynb` kèm p-value |
| **8** | Kết xuất biểu đồ khoa học | RW | Thư mục `figures/` (boxplot + distribution plots) |
| **9-10**| Hoàn thiện tài liệu học thuật và thuyết trình | Tất cả | Slides & Báo cáo cuối kỳ |

### 8.4 Phương án dự phòng (Contingency Plan)
- **Nếu proposal chưa được thông qua vào cuối Tuần 6:** Giới hạn phạm vi ở RQ1, hủy bỏ RQ2 - thông báo Giảng viên lập tức.
- **Nếu gặp giới hạn về API Rate limit:** Phân rã tiến trình thành các batch nhỏ, áp dụng kỹ thuật chạy ngầm (background run) qua đêm với cơ chế `tenacity`.
- **Nếu dataset gặp lỗi truy cập:** Tích hợp bộ dữ liệu kỹ thuật dự phòng (VD: Flask Docs) - đưa ra quyết định xử lý trong 24 giờ.
- **Nếu giai đoạn Pilot bộc lộ điểm nghẽn kỹ thuật:** Tuân thủ mục §8.6 Amendment - đệ trình Giảng viên trong vòng 24 giờ.
- **Nếu quá hạn nộp từ thành viên:** Trưởng nhóm phân bổ lại trách nhiệm thực thi trong vòng 48 giờ.

### 8.5 Checkpoint per member (Tuần 5-10)
| Role | Tuần 5 | Tuần 6 | Tuần 7 | Tuần 8 | Tuần 9-10 |
|---|---|---|---|---|---|
| **PL** | Rà soát Draft §2-§7 | Đệ trình proposal + Cập nhật tiến độ | Pilot meeting note | Đối chiếu §4 $\leftrightarrow$ §6 | Báo cáo Slide |
| **DG** | `data/raw/` + README | Xác nhận tài nguyên §8.1 | `data/pilot_ground_truth.csv` | `full_ground_truth.csv` | Bản thảo §3 |
| **LR** | Thực thi `test_api.py` | Xác nhận API budget | `results/pilot_llm_output.csv`| `full_llm_output.csv` | Bản thảo §4 |
| **MS** | `compute_metric.py` | Triển khai Test plan | `results/pilot_analysis.ipynb`| `full_analysis.ipynb` | Bản thảo §5 |
| **RW** | Draft §7 Threats | Chỉnh lý cấu trúc §1-§7 | — | Khởi tạo `figures/` | Bản thảo §1, §7 |

### 8.6 Quy trình Amendment (Áp dụng khi Pilot phát sinh vấn đề kỹ thuật)
**Tiêu chí khởi tạo Amendment:**
| Phát hiện từ Pilot | Kích hoạt Amendment? | Cơ sở lý luận |
|---|---|---|
| Phân phối dữ liệu sai lệch giả định ban đầu (Bimodal, Heavy-tail) | ✅ Yêu cầu tinh chỉnh cấu trúc kiểm định | Vấn đề mang bản chất cấu trúc kỹ thuật, không tác động lên RQ |
| Sai lệch thông số Metric do lỗi tích hợp dữ liệu | ✅ Yêu cầu điều chỉnh công cụ xử lý | Phát sinh cản trở kỹ thuật trọng yếu |
| N thực tế không đạt kỳ vọng cấu trúc ban đầu | ✅ Yêu cầu rà soát Mục §5.2 và Power analysis | Giữ nguyên RQ, chỉ đảm bảo tính xác thực của biến số N |
| Khả năng phòng thủ thực nghiệm thấp hơn kỳ vọng đề xuất | ❌ KHÔNG Amendment | Dữ liệu phản ánh xu hướng thực tế của đối tượng nghiên cứu |
| Có nhu cầu bổ sung Metric do kết quả phụ phát sinh | ❌ KHÔNG Amendment | Hành vi HARKing - Vi phạm tiêu chuẩn học thuật toàn vẹn |

*(Thời hạn triển khai: Bắt buộc đệ trình bản sửa đổi `proposal-amendment-v1.1.md` trong vòng 24 giờ kể từ khi hoàn tất cuộc họp Pilot Tuần 7. Khuyến nghị Trưởng nhóm escalade tiến trình nếu Giảng viên không hồi đáp sau 48 giờ. NGHIÊM CẤM: Can thiệp cấu trúc cốt lõi của RQ hoặc thao túng cấu trúc Metric sau khi phát sinh kết quả).*

---

## Lời Cam Kết: 5 Nguyên Tắc Xuyên Suốt Thực Nghiệm
Nhằm khẳng định chuẩn mực toàn vẹn khoa học từ Tuần 3 đến Tuần 10, tập thể nhóm cam kết duy trì tuyệt đối 5 nguyên lý học thuật sau:

1. **Evidence-based:** Mọi quyết định tái cấu trúc hệ thống (như triển khai Llama 4 Scout làm Judge, thiết lập hyperparameters) phải được quy chiếu chặt chẽ trên Evidence Table. Nghiêm cấm hoàn toàn các kết luận mang tính chủ quan.
2. **No HARKing (Chống giả thuyết sau sự thật):** Toàn bộ nền tảng hệ thống Research Questions, Metrics và Thresholds được niêm phong trong Proposal. Tuyệt đối không tinh chỉnh câu hỏi nghiên cứu sau khi quan sát hiện trạng dữ liệu.
3. **Reproducibility (Đảm bảo khả năng tái tạo):** Báo cáo khoa học phải minh bạch toàn bộ nhật ký phiên bản mô hình (`llama-4-scout`), cơ sở Hyperparameters, và cấu trúc văn bản Prompt. Các khái niệm mô hồ về tham số cấu hình sẽ không được chấp nhận.
4. **Mandatory Pilot (Bắt buộc chạy mô phỏng):** Quy trình đường ống đánh giá (Pipeline) phải trải qua đợt kiểm thử độc lập ở mức độ Pilot vào Tuần 7 để xác thực độ ổn định mã lệnh trước khi tiến hành chu kỳ dữ liệu Full Experiment vào Tuần 8.
5. **Data Integrity (Toàn vẹn luồng dữ liệu):** Trong trường hợp mô hình LLM phát sinh đứt gãy kết nối hoặc trả về tín hiệu rỗng, dữ liệu này sẽ được tự động gán nhãn Invalid/Abstain. Dữ liệu thực nghiệm được khóa kín, loại trừ mọi yếu tố can thiệp thủ công từ kiểm thử viên.
