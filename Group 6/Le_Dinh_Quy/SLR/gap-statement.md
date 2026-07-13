# Gap Statement - AI-guided Mutant Selection
Evidence table: N = 15 paper

## Các khoảng trống phát hiện

### GAP-T (Technology): Sự thiếu vắng các mô hình ngôn ngữ lớn (LLM) trong việc trực tiếp chọn lọc và phân loại đột biến
**Bằng chứng:** Cột Tool/LLM.
- *Nghiên cứu gần nhất:* S5 (Garg et al., 2022) sử dụng CodeBERT + LSTM và S12 (Chekam et al., 2019) sử dụng LSTM kết hợp Decision Tree để tự động chọn lọc mutants. S9 (Liu et al., 2023) và S13 (Alagarsamy et al., 2024) đã bắt đầu áp dụng LLMs/Code models (GPT-4, ChatGPT, CodeT5) để sinh test cases hoặc assertions nhằm cải thiện mutation score.
- *Thiếu sót:* Chưa có bất kỳ nghiên cứu nào (S1 - S15) sử dụng trực tiếp khả năng suy luận ngữ nghĩa của các Mô hình Ngôn ngữ Lớn (LLMs) thế hệ mới để trực tiếp phân loại đột biến tương đương (equivalent mutants) hoặc chọn lọc đột biến bao hàm (subsuming mutants) từ source code. Ngoài ra, ngoại trừ hệ thống đóng aSTRA của Google (S1, S2), chưa có công cụ chọn lọc đột biến tự động tích hợp CI/CD nào được mở rộng cho cộng đồng.

### GAP-M (Metric): Thiếu các chỉ số đánh giá thực tế về chi phí vận hành AI và năng suất của lập trình viên (Human-in-the-loop)
**Bằng chứng:** Cột Metric và Kết quả.
- *Nghiên cứu gần nhất:* S1 và S2 (Petrović et al., 2021) là các bài nghiên cứu hiếm hoi trong thực tế công nghiệp đo lường "Productivity Rate" (tỉ lệ lập trình viên thực sự tương tác và sửa mutants). S7 (Mohanty et al., 2025) và S12 (Chekam et al., 2019) có đo lường mức độ giảm thiểu chi phí (Cost Reduction) gián tiếp thông qua phần trăm mutant bị cắt giảm.
- *Thiếu sót:* 13/15 nghiên cứu còn lại (ngoại trừ S1, S2) hoàn toàn bỏ qua việc đo lường các chỉ số thực tế như: chi phí tính toán thực tế của việc chạy mô hình AI (inference overhead/cost), tác động lên năng suất và tải nhận thức của lập trình viên ngoài môi trường đóng của Google, và độ tin cậy của mô hình khi phân phối dữ liệu bị lệch pha (out-of-distribution robustness).

### GAP-D (Dataset): Sự thiên lệch lớn về ngôn ngữ lập trình và sự hạn chế của các bộ dữ liệu mã nguồn mở quy mô công nghiệp
**Bằng chứng:** Cột Dataset.
- *Nghiên cứu gần nhất:* S1, S2 (Petrović et al., 2021) đã sử dụng tập dữ liệu Google monorepo quy mô cực lớn (~2 tỷ dòng code) hỗ trợ đa ngôn ngữ (C++, Java, Python, Go, TypeScript). S5 (Garg et al., 2022) và S12 (Chekam et al., 2019) đã kết hợp các dự án Java (Apache Commons, Joda-Time) và C (Codeflaws, CoREBench) để tăng tính đa dạng.
- *Thiếu sót:* Các nghiên cứu mã nguồn mở hiện tại vẫn bị bó hẹp trong các bộ benchmark đơn ngôn ngữ hoặc kích thước nhỏ (S7 chỉ dùng 4 Java projects; S9 dùng các hàm Python ngắn đơn lẻ của HumanEval/MBPP; S12 chỉ dùng C). Dữ liệu quy mô lớn, đa ngôn ngữ duy nhất trong S1, S2 lại là mã nguồn đóng của Google, khiến cộng đồng học thuật thiếu đi nguồn dữ liệu chuẩn hóa, đa ngôn ngữ (như Go, Rust, TypeScript) để huấn luyện và kiểm chứng chéo các mô hình AI.

## Phát biểu GAP tổng hợp
Mặc dù các kỹ thuật AI/ML đã được nghiên cứu để tối ưu hóa việc chọn lọc đột biến trong kiểm thử phần mềm, các giải pháp hiện tại vẫn bị giới hạn trong việc sử dụng mô hình học máy truyền thống hoặc học sâu quy mô nhỏ trên các ngôn ngữ đơn lẻ (chủ yếu là C/Java) với tập dữ liệu học thuật hạn chế, đồng thời thiếu các đánh giá thực tế về chi phí vận hành AI và ảnh hưởng đến năng suất của lập trình viên. Do đó, việc xây dựng một giải pháp ứng dụng Mô hình Ngôn ngữ Lớn (LLM) để trực tiếp chọn lọc đột biến thông minh trên môi trường đa ngôn ngữ quy mô lớn, kết hợp đánh giá toàn diện cả về chi phí suy luận và tính khả dụng đối với con người, là một khoảng trống nghiên cứu cấp thiết cần được giải quyết.
