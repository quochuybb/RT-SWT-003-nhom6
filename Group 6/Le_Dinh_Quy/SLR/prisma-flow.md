# PRISMA Flow Diagram - AI-guided Mutant Selection

Dưới đây là thống kê quy trình lọc bài báo (SLR) theo đúng chuẩn PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses), phản ánh chính xác dữ liệu của nhóm:

## 1. Dữ liệu tổng quan
- **Identification (Thu thập dữ liệu):** 750 bài
- **Duplicates removed (Loại bỏ trùng lặp):** 62 bài
- **Screening V1 (Lọc Tiêu đề & Tóm tắt):** 688 bài
- **Excluded V1 (Bị loại ở V1):** 502 bài
- **Eligibility V2 (Lọc Toàn văn - Full-text):** 186 bài
- **Excluded V2 (Bị loại ở V2):** 171 bài
- **Included (Cuối cùng được chọn):** 15 bài

---

## 2. Sơ đồ PRISMA (Mermaid)
Bạn có thể copy đoạn code dưới đây vào các trình vẽ Markdown/Mermaid (như Obsidian, GitHub, hoặc Notion) để tự động tạo sơ đồ:

```mermaid
graph TD
    %% Identification Phase
    A1[Search String A: 250] --> ID_Total
    A2[Search String B: 250] --> ID_Total
    A3[Search String C: 250] --> ID_Total
    
    ID_Total[Records identified from databases <br> n = 750]
    
    %% Duplication Phase
    ID_Total --> Dedup[Records after duplicates removed <br> n = 688]
    ID_Total -.-> Dup[Duplicate records removed <br> n = 62]
    
    %% Screening Phase (V1)
    Dedup --> Screen_V1[Records screened Title/Abstract <br> n = 688]
    Screen_V1 --> Exclude_V1[Records excluded <br> n = 502 <br> Fail automated IC/EC]
    
    %% Eligibility Phase (V2)
    Screen_V1 --> Assess_V2[Full-text articles assessed for eligibility <br> n = 186]
    Assess_V2 --> Exclude_V2[Full-text articles excluded <br> n = 171 <br> Reasons: <br> EC-O Biology/Off-topic, <br> EC-N Surveys, <br> Missing IC-P/IC-I, <br> EC-A No PDF]
    
    %% Included Phase
    Assess_V2 --> Included[Studies included in review <br> n = 15]
    
    %% Styling
    classDef includeBox fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef excludeBox fill:#f8d7da,stroke:#dc3545,stroke-width:2px;
    classDef processBox fill:#e2e3e5,stroke:#6c757d,stroke-width:2px;
    classDef startBox fill:#cce5ff,stroke:#004085,stroke-width:2px;
    
    class Included includeBox;
    class Dup,Exclude_V1,Exclude_V2 excludeBox;
    class Dedup,Screen_V1,Assess_V2 processBox;
    class A1,A2,A3,ID_Total startBox;
```

---

## 3. Chi tiết nguyên nhân loại trừ ở Vòng 2 (171 bài bị loại)
- **EC-O**: Sai chủ đề (chủ yếu là bài viết Sinh học/Y khoa về gen, protein hoặc Tối ưu hóa trình biên dịch).
- **EC-N**: Là các bài Survey, Systematic Literature Review, hoặc không có thực nghiệm đánh giá.
- **Fail IC-P / IC-I**: Không có đủ keyword hoặc phương pháp về Kiểm thử đột biến (Mutation Testing) và Học máy/AI.
- **EC-A**: Không thể tải hoặc trích xuất được PDF toàn văn (chỉ có Abstract).
