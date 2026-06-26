\# GAP Analysis \- Mutation Testing on Microservices

Evidence table: N \= 6 papers  
Ngày: 2026-06-06

\---

\#\# Bảng GAP

| Cột | Phát hiện | Loại GAP | Phản chứng |  
|------|-----------|----------|------------|  
| Tool/LLM | Chưa có nghiên cứu đánh giá các LLM thế hệ mới (GPT-4o, GPT-5, Gemini...) cho mutation testing | GAP-T | ✅ Wang (2026) đã đánh giá GPT-4, Claude 3 và Llama 3 |  
| Dataset | Các nghiên cứu chủ yếu sử dụng benchmark Java hoặc hệ thống monolithic, chưa đánh giá trên microservices | GAP-D | ✅ Đã kiểm tra 6 paper, chưa có paper thực nghiệm trên microservices |  
| Metric | Mutation Score là metric được sử dụng phổ biến nhất | GAP-M | ✅ Không có metric nào vượt trội hơn |  
| Hạn chế | Chi phí tính toán cao và dataset nhỏ được nhiều paper cùng thừa nhận | GAP-S | ✅ Xuất hiện trong nhiều paper |

\---

\#\# GAP Chính: \[GAP-D\]

Các nghiên cứu hiện tại chủ yếu đánh giá mutation testing trên các dự án Java monolithic hoặc benchmark học thuật, trong khi chưa có đánh giá đầy đủ trên các hệ thống microservices có kiến trúc phân tán.

Nghiên cứu này đề xuất đánh giá hiệu quả của mutation testing trên hệ thống microservices công khai nhằm mở rộng phạm vi ứng dụng của phương pháp.

\---

\#\# GAP Secondary: \[GAP-T\]

Mặc dù đã có nghiên cứu sử dụng GPT-4, Claude 3 và Llama 3 trong mutation testing, chưa có nghiên cứu đánh giá các LLM thế hệ mới như GPT-4o hoặc GPT-5 trên cùng benchmark.

\---

\#\# Chi tiết kiểm tra phản chứng

| Paper | Đã làm GAP-D? | Ghi chú |  
|----------|--------------|----------------------------|  
| Abbas 2022 | Không | 4 Java open-source projects |  
| de Sousa Pinto 2022 | Không | 6 Java libraries |  
| Awais 2025 | Không | Commercial software |  
| Ojdanic 2023 | Không | 15 evolving Java systems |  
| Wang 2026 | Không | HumanEval, MBPP |  
| Krichen 2025 | Không | Survey paper |

\*\*Kết luận:\*\* Không tìm thấy paper nào đánh giá mutation testing trên hệ thống microservices.

\---

\#\# Feasibility Check – GAP Chính

| Tiêu chí | Mức | Ghi chú |  
|-----------|------|-------------------------------|  
| Dataset | ⚠️ | Cần lựa chọn benchmark microservices phù hợp |  
| Tool/API | ✅ | PITest và Maven miễn phí |  
| Compute | ⚠️ | Mutation testing tương đối tốn thời gian |  
| Ground truth | ⚠️ | Cần xác định baseline từ literature |  
| Skills | ✅ | Có tài liệu và công cụ hỗ trợ |  
| Thời gian | ⚠️ | Cần thời gian cấu hình benchmark |  
| Contribution | ✅ | Novelty rõ ràng |

\*\*Kết quả:\*\*

\- ✅ \= 3  
\- ⚠️ \= 4  
\- ❌ \= 0

\*\*Đánh giá:\*\* Rủi ro trung bình.

\*\*Quyết định:\*\* Tiếp tục với GAP này.  
