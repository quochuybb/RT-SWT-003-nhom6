import pandas as pd
import numpy as np
import scipy.stats as stats
import os

def main():
    print("🚀 BẮT ĐẦU GIAI ĐOẠN 6: PHÂN TÍCH THỐNG KÊ (RQ1 & RQ2) 🚀\n")
    
    file_path = "results/ai_judgements.csv"
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file {file_path}")
        return
        
    df = pd.read_csv(file_path)
    total_cases = len(df)
    
    # Lọc bỏ các dòng Error (nếu còn sót)
    df = df[df['ai_label'] != 'Error']
    valid_cases = len(df)
    
    print(f"Tổng số mẫu được phân tích: {valid_cases}/{total_cases}\n")
    
    label_counts = df['ai_label'].value_counts()
    print("--- Phân bổ Nhãn ---")
    for label, count in label_counts.items():
        print(f"- {label}: {count} ({count/valid_cases*100:.2f}%)")
    print("---------------------\n")
    
    # ---------------------------------------------------------
    # RQ1: Hallucination Rate
    # ---------------------------------------------------------
    print("================ RQ1: Hallucination Rate ================")
    hallucination_count = df[df['ai_label'] == 'Hallucination'].shape[0]
    hallucination_rate = hallucination_count / valid_cases
    print(f"Số ca Hallucination: {hallucination_count}")
    print(f"Tỷ lệ Hallucination (Hallucination Rate): {hallucination_rate*100:.2f}%")
    
    # Giả lập Wilcoxon test vì chưa có data Rule-based
    print("\n*Ghi chú Wilcoxon Test:* Hiện tại dữ liệu chỉ có Semantic Mutations.")
    print("Để tính Wilcoxon (Semantic vs Rule-based), chúng ta cần dữ liệu Rule-based.")
    print("=========================================================\n")
    
    # ---------------------------------------------------------
    # RQ2: System Defense / Abstain Rate
    # ---------------------------------------------------------
    print("================ RQ2: Abstain Rate (System Defense) ================")
    abstain_count = df[df['ai_label'] == 'Abstain'].shape[0]
    abstain_rate = abstain_count / valid_cases
    print(f"Số ca Abstain: {abstain_count}")
    print(f"Tỷ lệ Abstain (Abstain Rate): {abstain_rate*100:.2f}%")
    
    print("\nKiểm định Binomial Test (H0: Abstain Rate >= 90%, H1: Abstain Rate < 90%)")
    # scipy.stats.binomtest(k, n, p, alternative='less')
    # k = số thành công (abstain), n = tổng số phép thử, p = xác suất kỳ vọng (0.90)
    result = stats.binomtest(k=abstain_count, n=valid_cases, p=0.90, alternative='less')
    p_value = result.pvalue
    
    print(f"p-value = {p_value:.5e}")
    if p_value < 0.05:
        print("=> Kết luận: p < 0.05. Bác bỏ H0.")
        print("Tỷ lệ phòng thủ của RAG đã RỚT XUỐNG DƯỚI mức 90% một cách có ý nghĩa thống kê.")
        print("Điều này chứng tỏ tấn công Semantic Mutation CÓ HIỆU QUẢ trong việc bẻ gãy hệ thống RAG.")
    else:
        print("=> Kết luận: p >= 0.05. Không thể bác bỏ H0.")
        print("Tỷ lệ phòng thủ của RAG vẫn duy trì ở mức an toàn >= 90%.")
    print("====================================================================\n")
    
    print("🎉 HOÀN TẤT PHÂN TÍCH THỐNG KÊ 🎉")

if __name__ == "__main__":
    main()
