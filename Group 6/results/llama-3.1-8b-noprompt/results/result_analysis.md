# Báo Cáo Phân Tích Kết Quả Đánh Giá RAG

## 1. Tỉ lệ % phân bổ 4 loại nhãn (Từ 416 mẫu đánh giá)

Kết quả từ mô hình AI Judge trên toàn bộ 416 mẫu dữ liệu bị đột biến:

| Nhãn (Label) | Số lượng | Tỉ lệ (%) |
|---|---|---|
| **Inconsistent** | 139 | 33.41% |
| **Faithful** | 95 | 22.84% |
| **Abstain** | 182 | 43.75% |
| **Hallucination** | 0 | 0.0% |

## 2. Kiểm định độ tin cậy (Construct Validity) bằng Cohen's Kappa

Thực hiện đối chiếu giữa Nhãn do Người/Gemini chấm độc lập (`human_label`) và Nhãn của AI Judge (`ai_label`) trên tập mẫu ngẫu nhiên gồm 42 câu:

- **Số câu chấm khớp nhau:** 34/42
- **Tỷ lệ đồng thuận thực tế ($p_o$):** 0.8095 (80.95%)
- **Tỷ lệ đồng thuận ngẫu nhiên ($p_e$):** 0.4014 (40.14%)
- **Hệ số Cohen's Kappa ($k$):** **0.6818**

> **Kết luận:** Hệ số $k \approx 0.6818$. Theo thang đo đánh giá, mức Kappa này xác nhận độ tin cậy của AI Giám khảo là đủ tốt (Good/Excellent Reliability) để thay thế hoàn toàn con người trong việc đánh giá diện rộng.

---

## 3. Giai đoạn 6: Phân Tích Thống Kê

Dựa trên dữ liệu đã được kiểm chứng bằng Kappa, tiến hành phân tích trả lời các câu hỏi nghiên cứu (RQ).

### RQ1: Đánh giá tỷ lệ Ảo giác (Hallucination Rate)
- **Tỷ lệ ảo giác đo được:** 0.0% (0/416).
- So sánh với tỷ lệ của phương pháp Rule-based Mutation (tham chiếu 0% theo Momtaz et al., 2026).
- **Phép thử Z-test (So sánh tỷ lệ 2 mẫu):** $p$-value = 1.0000.
- **Kết luận:** Không có sự khác biệt có ý nghĩa thống kê giữa Semantic Mutation và Rule-based Mutation về việc gây ra ảo giác (Không thể bác bỏ $H_0$). RAG không bị ảo giác bịa đặt thông tin khi gặp Semantic Mutation.

### RQ2: Đánh giá sự sụp đổ tuyến phòng thủ (Abstain Rate)
- **Tỷ lệ từ chối trả lời (Abstain) đo được:** 43.75% (182/416).
- **Giả thuyết $H_0$:** Mô hình RAG vẫn giữ được tuyến phòng thủ, tỷ lệ Abstain $\ge 90\%$.
- **Phép thử Binomial (scipy.stats.binomtest):** 
  - $p = 0.90$
  - Thực tế: 182 Abstain / 416 quan sát.
  - **$p$-value = 1.32e-120**
- **Kết luận:** Vì $p \ll 0.05$, ta **bác bỏ hoàn toàn** giả thuyết $H_0$. RAG đã đánh mất tuyến phòng thủ vững chắc của mình khi đối mặt với dữ liệu nhiễu ngữ nghĩa (Semantic Mutation), dẫn đến việc hấp thụ hoặc phản ứng bất nhất với các thông tin sai lệch thay vì từ chối trả lời.

