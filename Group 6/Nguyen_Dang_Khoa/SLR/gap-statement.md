Tất cả 06 papers reviewed đều tập trung vào việc sử dụng các công cụ Mutation Testing truyền thống (như PITest) dựa trên các quy tắc toán tử cố định, hoặc áp dụng các mô hình ngôn ngữ lớn thương mại đóng (như GPT-4) để sinh phần tử đột biến trên các tập dữ liệu benchmark đóng.

Tuy nhiên, KHÔNG paper nào:

- (1) Khảo sát hay đánh giá hiệu quả của mô hình ngôn ngữ lớn mã nguồn mở chuyên biệt cho code thế hệ mới (như DeepSeek-Coder) trong quy trình kiểm thử đột biến;
- (2) Sử dụng chỉ số độ tương đồng ngữ nghĩa nâng cao (Semantic similarity) để sàng lọc và đánh giá chất lượng của các đột biến do AI tạo ra;
- (3) Đo lường tỷ lệ thực thi thành công thực tế (Executable rate) của các đoạn mã đột biến được tạo động bởi LLM trên các hệ thống phần mềm phức tạp.

Hiện nay chưa có nghiên cứu nào đánh giá toàn diện năng lực của các LLM mã nguồn mở chuyên dụng cho lập trình trong việc tối ưu hóa quy trình Mutation Testing, đồng thời thiếu hụt các độ đo chuẩn xác về mặt ngữ nghĩa và khả năng ứng dụng thực tế của mã đột biến, dẫn đến việc cộng đồng vẫn phải đối mặt với chi phí vận hành lớn và tỷ lệ code lỗi cao từ LLM.

Để giải quyết các hạn chế nêu trên, nghiên cứu này triển khai mô hình DeepSeek-Coder vào quy trình tự động sinh mã đột biến (Mutation Generation), đồng thời tích hợp bộ lọc kép sử dụng metric Semantic similarity và kiểm tra Executable rate nhằm loại bỏ các đột biến vô nghĩa. Đóng góp chính của nghiên cứu là cung cấp một khung đánh giá (framework) mới giúp nâng cao độ chính xác của các phần tử đột biến và giảm thiểu tối đa chi phí tính toán cho hệ thống kiểm thử trong môi trường thực tế.
