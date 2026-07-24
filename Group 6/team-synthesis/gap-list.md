# Danh sách GAP

*(Tài liệu này dùng để tổng hợp các GAP từ các thành viên trong nhóm, bao gồm cả những ý tưởng được đề xuất ban đầu nhưng bị loại bỏ qua các vòng đánh giá tính khả thi G1/G2)*

| STT | Tên thành viên | Đề xuất GAP | Trạng thái |
|---|---|---|---|
| 1 | Nguyễn Quốc Huy | **Technology GAP:** Chưa có nghiên cứu dùng LLM sinh đột biến ngữ nghĩa (Semantic Mutation) để kiểm thử hệ thống RAG thay cho Rule-based (như nghiên cứu của Momtaz). | **Được chọn (GAP Chính)** |
| 2 | Lê Đình Quý | **Methodology GAP (Source Code):** Ứng dụng khả năng của LLM để tự động sinh đột biến ngữ nghĩa trên mã nguồn truyền thống (Java/C++). | **Loại bỏ** (Không khả thi: Gặp rào cản lớn về lỗi biên dịch và tốn kém tài nguyên phần cứng Fine-tuning trong thời gian 4-5 tuần của môn học). |
| 3 | Bùi Lê Tấn Đạt | **Domain/Dataset GAP:** Chưa có đánh giá mức độ tin cậy của RAG trên miền dữ liệu Kỹ thuật phần mềm (API Docs) để đối chiếu với kiến thức tham số (Parametric Knowledge) của mô hình. | **Được chọn (GAP Phụ 1)** |
| 4 | Bùi Lê Tấn Đạt | **Application GAP:** Ứng dụng mô hình ngôn ngữ (LLM Fuzzer) để tự động sinh dữ liệu kiểm thử lỗ hổng trên giao diện Web UI. | **Loại bỏ** (Chỉ tập trung vào bề mặt giao diện, không đánh giá được khả năng suy luận logic bên trong của AI). |
| 5 | Nguyễn Đăng Khoa | **Defense GAP:** Chưa có nghiên cứu đo lường định lượng sự xuyên thủng của màng bảo vệ "System Prompt" trước các cuộc tấn công bằng dữ liệu đột biến tinh vi. | **Được chọn (GAP Phụ 2 / RQ3)** |
| 6 | Nguyễn Đăng Khoa | **Measurement GAP:** Xây dựng framework đánh giá chất lượng RAG một cách thụ động dựa trên các Metrics (như dự án RAGAS). | **Loại bỏ** (Chỉ mang tính đo lường thụ động, không có cơ chế tiêm lỗi tự động để đo lường tính chống chịu trước Adversarial Attacks). |
