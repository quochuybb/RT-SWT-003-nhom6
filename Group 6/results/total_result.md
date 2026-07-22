# Tổng hợp và So sánh Kết quả Đánh giá RAG trên 4 Kịch bản

Tài liệu này tổng hợp số liệu phân tích của 4 kịch bản thực nghiệm Semantic Mutation Testing trên 2 mô hình (Llama 3.1 8B và Llama 3.1 17B), có và không có bọc System Prompt Guardrails. 

## 1. Bảng Tổng hợp Số liệu (416 mẫu / Kịch bản)

| Mô hình & Cấu hình | Abstain (%) | Faithful (%) | Inconsistent (%) | Hallucination (%) | Cohen's Kappa ($k$) |
|------------------|------------|-------------|-----------------|-------------------|---------------|
| **17B (No Prompt)** | 6.25%      | 37.74%      | 56.01%          | 0.0%              | 0.7137 (Good)      |
| **17B (Prompt)**    | 61.06%     | 24.52%      | 14.42%          | 0.0%              | 0.8199 (Excellent) |
| **8B (No Prompt)**  | 43.75%     | 22.84%      | 33.41%          | 0.0%              | 0.6818 (Good)      |
| **8B (Prompt)**     | 66.11%     | 25.24%      | 8.65%           | 0.0%              | 0.8531 (Excellent) |

---

## 2. Các Phát hiện Khoa học Thú vị (Key Findings)

Dựa trên bảng số liệu, nhóm nghiên cứu rút ra những nhận định đột phá sau:

### 2.1. System Prompt Guardrails là tấm khiên cực kỳ hiệu quả
- Khi được nạp câu lệnh bảo vệ ("Use strictly only the provided Context..."), tỷ lệ từ chối trả lời (Abstain) của cả 2 mô hình đều **tăng vọt một cách ấn tượng**. 
- Cụ thể: 17B tăng từ 6.25% lên 61.06%; 8B tăng từ 43.75% lên 66.11%. Điều này chứng minh rằng Prompt là công cụ kiểm soát rẻ và nhanh nhất để gia cố tuyến phòng thủ của RAG.

### 2.2. Sự bướng bỉnh của "Parametric Knowledge" ở Mô hình lớn
- Ở trạng thái **No Prompt**, con 17B có tỷ lệ **Inconsistent khổng lồ (56.01%)**, trong khi 8B chỉ là 33.41%.
- **Giải thích:** Mô hình càng lớn (17B) thì dung lượng kiến thức nội tại (Parametric Knowledge) càng sâu rộng và "tự tin". Khi thấy tài liệu RAG cung cấp thông tin sai trái/mâu thuẫn, con 17B có xu hướng "coi thường" tài liệu và tự động trả lời bằng kiến thức thật của nó. Trong khi đó, con 8B ngây thơ hơn, ít kiến thức hơn nên không dám tự tin phản kháng mạnh như vậy.

### 2.3. "Tử huyệt" chung: Sự cả tin (Faithful) không bị dập tắt
- Mặc dù System Prompt giúp dập tắt tỷ lệ Inconsistent (rớt xuống còn 14% và 8%), nhưng nó lại **gần như bất lực** trong việc hạ thấp tỷ lệ **Faithful**.
- Cả 17B và 8B (có Prompt) vẫn tin sái cổ vào tài liệu đột biến ở mức **~25%**. 
- **Giải thích:** Prompt ép mô hình phải "bám sát vào tài liệu". Vì vậy, nếu bản thân tài liệu RAG chứa thông tin sai lệch (mutated), mô hình tuân lệnh Prompt nên nhắm mắt trích xuất luôn thông tin sai đó. Mô hình LLM không có khả năng nhận thức "sự thật" bên ngoài để bác bỏ logic sai trong chính văn bản RAG.

### 2.4. Khả năng gây "Ảo giác" (Hallucination) của Semantic Mutation là 0%
- Trong toàn bộ 4 kịch bản x 416 câu = 1664 mẫu, **KHÔNG CÓ MỘT CA HALLUCINATION NÀO XẢY RA**.
- **Kết luận:** Tấn công ngữ nghĩa (Semantic Mutation) phá hủy RAG không phải bằng cách làm nó bịa chuyện (Hallucination), mà bằng cách bắt nó hấp thụ kiến thức độc hại (Faithful) hoặc ép nó rò rỉ kiến thức nội tại (Inconsistent).

### 2.5. AI Judge (70B) cực kỳ đáng tin cậy
- Hệ số Cohen's Kappa trên các cấu hình đều duy trì mức Tốt đến Rất tốt ($k > 0.68$), đặc biệt các phiên bản có Prompt đều đạt mức xuất sắc ($k > 0.8$).
- Cụ thể: 8B No Prompt ($k \approx 0.68$) và 17B No Prompt ($k \approx 0.71$). Lý do các bản No Prompt có Kappa thấp hơn là do mô hình trả lời lan man, lấp lửng, khiến cả người và AI Judge (Llama 3.3 70B) đều gặp khó khăn khi chốt nhãn. Khi được ép vào khuôn khổ Prompt, câu trả lời rõ ràng, đẩy Kappa lên mức cao nhất (0.81 - 0.85).
