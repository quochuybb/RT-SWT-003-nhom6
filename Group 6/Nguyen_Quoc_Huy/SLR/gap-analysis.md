# GAP Analysis — AI-guided Mutant Selection for Java Programs
Evidence table: N = 7 papers | Ngày: 2024-06-08

## Bảng GAP

| Cột | Phát hiện | Loại GAP | Phản chứng |
|---|---|---|---|
| Tool/LLM | 7/7 paper dùng ML truyền thống/Metaheuristic (RF, GA, Clustering, BERT). Chưa có paper nào dùng LLM tạo sinh (GPT-4o, Claude). | GAP-T | ✅ Kiểm tra 7 paper |
| Dataset | 7/7 paper chỉ đánh giá trên mã nguồn Java, đa số là dataset quy mô nhỏ-trung bình. Thiếu đa ngôn ngữ. | GAP-D | ✅ |
| Metric | 5/7 paper tập trung vào Accuracy/AUC, Mutation Score. Thiếu hoàn toàn thước đo chi phí triển khai thực tế (effort reduction, inference cost). | GAP-M | ✅ |
| Hạn chế | "Chỉ Java" (5/7 paper), "Dataset benchmark cố định nhỏ" (4/7 paper), "Chưa xử lý equivalent mutants" (3/7 paper). | GAP-S | ✅ |

## GAP Chính: GAP-T (Technology)
Mặc dù đã có nhiều nghiên cứu áp dụng ML và Metaheuristic vào chọn lọc đột biến trên Java, chưa có nghiên cứu nào ứng dụng khả năng suy luận ngữ nghĩa của LLMs tạo sinh (như GPT-4o) để chọn lọc đột biến thông qua zero-shot/few-shot reasoning.
**Lý do chọn:** Đây là công nghệ tiên tiến nhất hiện nay (LLM tạo sinh) nhưng hoàn toàn bị bỏ ngỏ trong mảng chọn lọc đột biến. Việc tiên phong lấp đầy khoảng trống này sẽ mang lại contribution và tính mới (novelty) cao nhất cho đồ án.

## GAP Secondary (nếu có): GAP-M (Metric)
Các nghiên cứu hiện tại thiếu vắng các thước đo chi phí triển khai toàn diện (inference cost, effort reduction rate) để đánh giá tính khả thi kinh tế khi đưa AI vào quy trình CI/CD thực tế.

## Chi tiết kiểm tra phản chứng
| Paper | Phản chứng cho GAP-T? | Ghi chú |
|---|---|---|
| Wei et al. (Spectral Clustering) | Không | Dùng Unsupervised clustering truyền thống |
| SQUMUTH (Mohanty) | Không | Dùng Metaheuristic (Squirrel Search Algorithm) |
| Rani & Suri (Elitist GA) | Không | Dùng Genetic Algorithm |
| Jain & Alon (MutationBERT) | Không | Dùng BERT encoder-only, không phải generative LLM |
| Aghamohammadi #1 (PMT) | Không | Dùng Random Forest + Gradient Boosting |
| Aghamohammadi #2 (EPMT) | Không | Dùng Ensemble ML + LIME |
| Zhu et al. (Compression) | Không | Dùng FCA + Overlapped Grouping |

## Feasibility Check - GAP Chính
| Tiêu chí | Mức | Ghi chú |
|---|---|---|
| Dataset | ✅ | Defects4J có sẵn trên GitHub, tải được ngay |
| Tool/API | ✅ | GPT-4o có free tier hoặc dùng GPT-4o-mini giá rẻ |
| Compute | ✅ | LLM chạy qua API, không cần GPU local |
| Ground truth | ✅ | Killing matrix từ PITest/MuJava có sẵn |
| Skills | ✅ | Python + OpenAI API, có tutorial sẵn |
| Thời gian | ✅ | Xong với buffer ≥ 1 tuần dự phòng |
| Contribution | ✅ | Là baseline đầu tiên cho LLM-based mutant selection trên Defects4J |
**Kết quả:** 0 ❌ / 0 ⚠️ -> An toàn
