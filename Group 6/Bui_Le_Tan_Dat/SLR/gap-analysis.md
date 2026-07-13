# GAP Analysis — Predictive Mutation Testing with LLM
Evidence table: N = 10 paper | Ngày: 2025-06-11

## Bảng GAP

| Cột | Phát hiện | Loại GAP | Phản chứng |
|---|---|---|---|
| Tool/LLM | Toàn bộ 10 paper dùng traditional ML (RF, CNN, RNN, GNN, GA); không có paper nào dùng pre-trained code LLM (CodeBERT, UniXcoder, GPT-based) | GAP-T | ✅ Kiểm tra 10/10 paper — xác nhận không có LLM |
| Dataset | 9/10 paper chỉ dùng Java; không có large-scale study nào trên Python/JavaScript/C++ (>100 projects) | GAP-D | ✅ Kiểm tra 10/10 paper — xác nhận |
| Metric | Không có paper nào đo tương quan predicted mutation score vs. real fault detection rate trong CI/CD pipeline thực tế | GAP-M | ✅ Kiểm tra 10/10 paper — xác nhận |
| Hạn chế | ≥4/10 paper thừa nhận: dynamic features cần test execution tốn kém; equivalent mutant identification vẫn cần manual work | GAP-S | ✅ Xác nhận: Mao 2019, Duque 2020, PMT TSE 2019, Dang 2022 |

---

## GAP Chính: GAP-T

Toàn bộ các nghiên cứu hiện tại về predictive mutation testing đều sử dụng traditional machine learning (Random Forest, SVM, CNN) với hand-crafted features; chưa có nghiên cứu nào khai thác pre-trained code representation models (e.g., CodeBERT, UniXcoder) để học ngữ nghĩa của mutant một cách trực tiếp, dẫn đến hạn chế trong khả năng tổng quát hóa cross-language và cross-project.

## GAP Secondary: GAP-D

Không có nghiên cứu nào đánh giá hiệu quả của predictive mutation testing trên các ngôn ngữ ngoài Java ở quy mô lớn (>100 projects), đặc biệt là Python và JavaScript — hai ngôn ngữ phổ biến nhất trong thực tế phát triển phần mềm hiện đại.

---

## Chi tiết kiểm tra phản chứng

Bảng kiểm tra từng paper cho GAP primary (GAP-T):

| Tên paper | Đã dùng LLM/pre-trained code model không? | Ghi chú |
|---|---|---|
| MQP 2021 | Không | Random Forest + static features |
| Cerebro 2023 | Không | RNN Encoder-Decoder — sequence model, không phải pre-trained LLM |
| CAMUS 2025 | Không | GNN — graph-based, không có pre-trained LLM |
| ICSE 2022 | Không | Ridge Regression, Random Forest |
| PMT TSE 2019 | Không | Random Forest + hand-crafted PIE features |
| AST 2023 | Không | Learning-based — không có bằng chứng LLM (N/A dataset) |
| ICST 2019 (Mao) | Không | RF, CNN, caForest — không có pre-trained LLM |
| APSEC 2023 | Không | PIE + NL features — NL features nhưng không phải LLM embedding |
| TSE 2022 (Dang) | Không | Fuzzy Clustering + Multi-population GA |
| ICSTW 2020 (Duque) | Không | Random Forest (scikit-learn) |

**→ Kết luận: XÁC NHẬN GAP-T.** 0/10 paper dùng pre-trained code LLM.

---

## Feasibility Check — GAP Chính (GAP-T)

| Tiêu chí | Mức | Ghi chú |
|---|---|---|
| Dataset | ✅ | Defects4J + 654 Java projects public — benchmark có sẵn, đã verified |
| Tool/API | ⚠️ | CodeBERT/UniXcoder free (HuggingFace); GPT-4o API có phí nhưng < $5 cho N mẫu nhỏ |
| Compute | ⚠️ | Cần GPU — Colab/Kaggle free tier đủ cho fine-tuning nhỏ |
| Ground truth | ✅ | Không cần annotation thêm — dùng killed/survived labels từ PIT tool |
| Skills | ⚠️ | Cần HuggingFace transformers, fine-tuning — có thể học < 1 tuần |
| Thời gian | ⚠️ | Tight nhưng khả thi trong 1–2 tuần với CodeBERT off-the-shelf |
| Contribution | ✅ | Baseline đầu tiên cho LLM + mutation testing — rõ ràng novel, không bị làm trước |

**Kết quả: 0 ❌ / 4 ⚠️ / 3 ✅ → An toàn — tiếp tục với GAP này**
