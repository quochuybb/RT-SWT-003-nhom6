# Search Log - AI-guided Mutant Selection for Java Programs
**Thành viên:** Bùi Lê Tấn Đạt
**Ngày thực hiện:** 2026-06-01

---

## Câu hỏi nghiên cứu & Định nghĩa PICO
> **RQ:** Đối với mutation testing trên Java projects (P), AI-guided mutant selection (I) so với random mutant generation (C) có tạo fewer but higher-quality mutants (mutation adequacy score cao hơn >=15%) với effort giảm >=30% không (O)?

---

## Chuỗi tìm kiếm (Query Strings) và Kết quả chi tiết

### String A
*   **Query nguyên văn:** 
    ```text
    (mutation testing OR mutation analysis) AND (artificial intelligence OR machine learning OR predictive OR AI) AND (mutant selection OR mutant reduction OR smart selection)
    ```
*   **Database:** OpenAlex
*   **Bộ lọc:** `publication_year:>=2018`
*   **Ngày search:** 2026-06-01
*   **Số kết quả:** 250 papers (giới hạn thu thập)

### String B
*   **Query nguyên văn:** 
    ```text
    (mutation testing OR mutation analysis) AND (Java) AND (mutation score OR mutation adequacy OR quality) AND (effort OR computational cost OR efficiency)
    ```
*   **Database:** OpenAlex
*   **Bộ lọc:** `publication_year:>=2018`
*   **Ngày search:** 2026-06-01
*   **Số kết quả:** 250 papers (giới hạn thu thập)

### String C
*   **Query nguyên văn:** 
    ```text
    (mutation testing) AND (predictive OR machine learning) AND (random mutant OR random selection) AND (comparison OR evaluation)
    ```
*   **Database:** OpenAlex
*   **Bộ lọc:** `publication_year:>=2018`
*   **Ngày search:** 2026-06-01
*   **Số kết quả:** 250 papers (giới hạn thu thập)

---

## Tổng hợp trước và sau Deduplication (Loại bỏ trùng lặp)

| Database | String | Kết quả |
| :--- | :--- | :--- |
| OpenAlex | String A | 250 papers |
| OpenAlex | String B | 250 papers |
| OpenAlex | String C | 250 papers |
| **Tổng trước khi loại trùng (Pre-deduplication)** | | **750 papers** |
| **Tổng sau khi loại trùng (Post-deduplication)** | | **688 papers** |
| **Số lượng bị loại do trùng lặp (Duplicates removed)** | | **62 papers** |

---

## Những bài báo cần tải thủ công (Không tự động tải được PDF)

Dưới đây là danh sách 8 bài báo thuộc danh sách 15 bài vòng 2 nhưng không thể tự động tải được file PDF (do không có link trực tiếp hoặc bị chặn bởi nhà xuất bản), yêu cầu phải tải thủ công:

**A. Các bài không có link trực tiếp (6 bài):**

1.  **Chen 2025 (CAMUS: Context-Aware Neural Mutation Selection)**
    *   **Link OpenAlex:** [OpenAlex W7131298928](https://openalex.org/W7131298928)
    *   **DOI:** `10.1109/APSEC66846.2025.00013`
2.  **Guilherme 2023 (An initial investigation of ChatGPT unit test generation capability)**
    *   **Link OpenAlex:** [OpenAlex W4387711873](https://openalex.org/W4387711873)
    *   **DOI:** `10.1145/3624032.3624035`
3.  **Naeem 2019 (A machine learning approach for classification of equivalent mutants)**
    *   **Link OpenAlex:** [OpenAlex W2993033744](https://openalex.org/W2993033744)
    *   **DOI:** `10.1002/smr.2238`
4.  **Papadakis 2018 (Are mutation scores correlated with real fault detection?)**
    *   **Link OpenAlex:** [OpenAlex W2788962378](https://openalex.org/W2788962378)
    *   **DOI:** `10.1145/3180155.3180183`
5.  **Li 2022 (MMOS: Multi-Staged Mutation Operator Scheduling for Deep Learning Library Testing)**
    *   **Link OpenAlex:** [OpenAlex W4315629811](https://openalex.org/W4315629811)
    *   **DOI:** `10.1109/globecom48099.2022.10001093`
6.  **Wang 2023 (Test case generation method based on particle swarm optimization algorithm)**
    *   **Link OpenAlex:** [OpenAlex W4382049351](https://openalex.org/W4382049351)
    *   **DOI:** `10.1117/12.2683538`

**B. Các bài bị chặn bởi tường lửa nhà xuất bản, tải về ra HTML (2 bài):**

7.  **Shobana 2023 (Mutation testing in test suite generation using separate bacterial memetic evolutionary algorithm in IoT)**
    *   **Link OpenAlex:** [OpenAlex W4323322517](https://openalex.org/W4323322517)
    *   **DOI:** `10.1016/j.measen.2023.100725`
8.  **Alagarsamy 2024 (A3Test: Assertion-Augmented Automated Test case generation)**
    *   **Link OpenAlex:** [OpenAlex W4402042086](https://openalex.org/W4402042086)
    *   **DOI:** `10.1016/j.infsof.2024.107565`

---

## Những bài báo đã tải thành công (7 bài)

Dưới đây là danh sách 7 bài báo đã tự động tải thành công bằng script (hiện đã nằm trong thư mục `final_15_pdfs`):

1.  **Petrović 2021 (Practical Mutation Testing at Scale: A view from Google)**
    *   **Link OpenAlex:** [OpenAlex W3196350964](https://openalex.org/W3196350964)
    *   **DOI:** `10.1109/tse.2021.3107634`
2.  **Petrović 2021 (Practical Mutation Testing at Scale)**
    *   **Link OpenAlex:** [OpenAlex W3129295186](https://openalex.org/W3129295186)
    *   **DOI:** `10.48550/arxiv.2102.11378`
3.  **Garg 2022 (Cerebro: Static Subsuming Mutant Selection)**
    *   **Link OpenAlex:** [OpenAlex W4206242116](https://openalex.org/W4206242116)
    *   **DOI:** `10.1109/tse.2022.3140510`
4.  **Mohanty 2025 (SQUMUTH squirrel search based algorithm for high order mutant generation in mutation testing)**
    *   **Link OpenAlex:** [OpenAlex W4410004423](https://openalex.org/W4410004423)
    *   **DOI:** `10.1007/s10791-025-09525-1`
5.  **Liu 2023 (Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation)**
    *   **Link OpenAlex:** [OpenAlex W4367860052](https://openalex.org/W4367860052)
    *   **DOI:** `10.48550/arxiv.2305.01210`
6.  **Sun 2018 (Concolic testing for deep neural networks)**
    *   **Link OpenAlex:** [OpenAlex W2963913218](https://openalex.org/W2963913218)
    *   **DOI:** `10.1145/3238147.3238172`
7.  **Chekam 2019 (Selecting fault revealing mutants)**
    *   **Link OpenAlex:** [OpenAlex W2995454814](https://openalex.org/W2995454814)
    *   **DOI:** `10.1007/s10664-019-09778-7`
