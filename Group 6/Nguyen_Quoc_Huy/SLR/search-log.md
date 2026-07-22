# Search Log - AI-guided Mutant Selection for Java Programs
**Thành viên:** Huy
**Ngày thực hiện:** 2026-06-01

---

## Chuỗi tìm kiếm (Query Strings)

### String A — Lựa chọn/giảm thiểu đột biến bằng AI (Kết hợp P & I)
**Mục tiêu:** Tập trung vào việc tìm các nghiên cứu sử dụng AI/Machine Learning để tối ưu hóa tập đột biến.
**Query nguyên văn:**
```text
(mutation testing OR mutation analysis) AND (artificial intelligence OR machine learning OR predictive OR AI) AND (mutant selection OR mutant reduction OR smart selection)
```
**Database:** Semantic Scholar
**Bộ lọc:** Không có bộ lọc (Lấy theo độ liên quan từ API/Scraping)
**Ngày search:** 2026-06-01
**Số kết quả:** 252 papers

### String B — Đánh giá chi phí, nỗ lực và chất lượng trên Java (Kết hợp P, O & ngữ cảnh)
**Mục tiêu:** Tập trung vào các thước đo (metrics) đánh giá kết quả của mutation testing cụ thể trên ngôn ngữ Java.
**Query nguyên văn:**
```text
(mutation testing OR mutation analysis) AND (Java) AND (mutation score OR mutation adequacy OR quality) AND (effort OR computational cost OR efficiency)
```
**Database:** Semantic Scholar
**Bộ lọc:** Không có bộ lọc
**Ngày search:** 2026-06-01
**Số kết quả:** 147 papers

### String C — So sánh trực tiếp giữa AI và ngẫu nhiên (Kết hợp P, I, C)
**Mục tiêu:** Chuỗi này hẹp hơn một chút, nhắm thẳng vào các bài báo có sự so sánh giữa phương pháp học máy/dự đoán và phương pháp ngẫu nhiên truyền thống.
**Query nguyên văn:**
```text
(mutation testing) AND (predictive OR machine learning) AND (random mutant OR random selection) AND (comparison OR evaluation)
```
**Database:** Semantic Scholar
**Bộ lọc:** Giới hạn lấy top 243 bài báo đầu tiên có độ liên quan cao nhất (Relevance) do truy vấn trả về quá nhiều kết quả (~4000 bài).
**Ngày search:** 2026-06-01
**Số kết quả thu thập:** 243 papers

---

## Tổng hợp trước dedup

| Database | String | Kết quả |
|----------|--------|---------|
| Semantic Scholar | String A | 252 |
| Semantic Scholar | String B | 147 |
| Semantic Scholar | String C | 243 |
| **Tổng trước dedup** | | **642** |
| **Sau dedup** | | **641** |
| Số bị loại (trùng lặp) | | 1 |

---

## Ghi chú

- Thực hiện dedup bằng: Lập trình Python (Sử dụng thư viện `pandas` trong file `merge_outputs.py`, loại bỏ trùng lặp dựa trên việc chuẩn hóa cột `title` về in thường và xóa khoảng trắng).
- Số lượng trùng lặp bằng 1: Một bài báo bị trùng lặp đã được xóa.

---

### Tổng kết thực tế quy trình SLR

**SV: Huy**
- Chuỗi String A, B, C -> Semantic Scholar = 642 kết quả
- Sau dedup: 641 papers -> file `merged_output/merged_papers.csv` (và `01_all_records.csv`) có 641 dòng
- Screening V1: 612 bị loại -> 29 pass -> file `SLR/02_after_screening_v1.csv` có cột v1_decision = 612 EXCLUDE + 29 INCLUDE
- Full-text V2: 22 bị loại -> 7 final -> file `SLR/03_final_included.csv` có cột v2_decision = 7 INCLUDE (POTENTIAL)
