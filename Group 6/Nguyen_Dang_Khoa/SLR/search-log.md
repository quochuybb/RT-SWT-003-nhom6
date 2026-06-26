\# Search Log – Mutation Testing using LLM and AI Techniques

\*\*Thành viên:\*\* Nguyễn Đăng Khoa

\*\*Ngày thực hiện:\*\* 2026-06-03

\---

\## Chuỗi tìm kiếm (Query Strings)

String A: (“mutation testing” OR “mutation analysis”) AND (“artificial intelligence” OR “machine learning” OR “predictive” OR “AI”) AND (“mutant selection” OR “mutant reduction” OR “smart selection”)

\*\*Database:\*\* Google Sholar

\*\*Bộ lọc:\*\*

\- English only  
- Peer-reviewed  
- Publication year ≥ 2022

\*\*Ngày search:\*\* 2026-06-03

\*\*Số kết quả:\*\* 216 papers

\---

String B: (“mutation testing” OR “mutation analysis”) AND (“Java”) AND (“mutation score” OR “mutation adequacy” OR “quality”) AND (“effort” OR “computational cost” OR “efficiency”)

\*\*Database:\*\* Google Sholar

\*\*Bộ lọc:\*\*

\- English only  
- Conference + Journal  
- Publication year ≥ 2018

\*\*Ngày search:\*\* 2026-06-03

\*\*Số kết quả:\*\* 2240 papers

\---

String C: (“mutation testing”) AND (“predictive” OR “machine learning”) AND (“random mutant” OR “random selection”) AND (“comparison” OR “evaluation”)

\*\*Database:\*\* Google Sholar

\*\*Bộ lọc:\*\*

\- English only  
- Manual screening

\*\*Ngày search:\*\* 2026-06-03

\*\*Số kết quả:\*\* 284 papers

\---

\# Tổng hợp trước dedup

|Database|String|Kết quả|
|-|-|-|
|Scopus|String A|216|
|IEEE Xplore|String B|2240|
|Semantic Scholar|String C|284|

|||
|-|-|
|\*\*Tổng trước dedup\*\*|\*\*2740 papers\*\*|

\## Ghi chú

\- Kết quả được xuất thành file `01\_all\_records.csv`.  
- Thực hiện sàng lọc theo tiêu chí IC/EC trong bảng evidence.  
- Bao gồm các trường:  
- IC1: English  
- IC2: Publication year ≥ 2022  
- IC3: Peer-reviewed  
- IC4: Relevant topic  
- IC5: Empirical study  
- Loại bỏ các bài không phù hợp theo tiêu chí EC (nếu có).  
- Sau quá trình screening, các bài được sử dụng để xây dựng Evidence Table và phân tích Research Gap.

\---

\## Thống kê quá trình tìm kiếm

|Thuộc tính|Giá trị|
|-|-:|
|Tổng kết quả truy xuất từ các cơ sở dữ liệu|2740|
|Paper được export để screening|30|
|Paper được Include|24|
|Paper bị Exclude|5|
|Duplicate phát hiện trong tập export|6|

\---

\## Kết nối với SLR

File này là nhật ký tìm kiếm phục vụ cho quy trình Systematic Literature Review (SLR).

Các paper được giữ lại sau screening tiếp tục được sử dụng để:

1\. Xây dựng Evidence Table.  
2. Phân tích GAP (GAP-T, GAP-D, GAP-M, GAP-S).  
3. Thiết kế Experiment Design Rationale.  
4. Xây dựng Research Question và Hypothesis.

