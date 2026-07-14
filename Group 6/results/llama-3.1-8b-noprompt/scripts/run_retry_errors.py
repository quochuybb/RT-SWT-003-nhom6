import os
import csv
import time
from run_experiment_full import evaluate_with_llama

def main():
    print("🚀 BẮT ĐẦU CHẠY LẠI 52 CÂU LỖI (GIAI ĐOẠN 5) 🚀")
    
    # 1. Load data
    baseline_map = {}
    with open("results/baseline_responses.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            baseline_map[row["id"]] = row["baseline_answer"]
            
    context_map = {}
    with open("data/mutated/semantic_mutants.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            context_map[row["mut_id"]] = row["mutated_context"]
            
    mutated_responses = {}
    with open("results/full_mutated_responses.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mutated_responses[row["mut_id"]] = row
            
    # 2. Đọc file kết quả hiện tại
    results_file = "results/ai_judgements.csv"
    judgements = []
    error_ids = []
    
    with open(results_file, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            judgements.append(row)
            if row["ai_label"] == "Error":
                error_ids.append(row["mut_id"])
                
    print(f"Tổng số câu cần chạy lại: {len(error_ids)}")
    
    if len(error_ids) == 0:
        print("Không có câu nào bị lỗi. Hoàn tất!")
        return

    # 3. Tiến hành chấm điểm lại
    print("\n--- BƯỚC 1: AI CHẤM ĐIỂM LẠI ---")
    fixed_count = 0
    for i, row in enumerate(judgements):
        if row["ai_label"] == "Error":
            mut_id = row["mut_id"]
            
            ctx_id = mut_id.split("_MUT_")[0]
            mut_data = mutated_responses.get(mut_id, {})
            query = mut_data.get("query", "")
            mutated_resp = mut_data.get("mutated_response", "")
            mutated_ctx = context_map.get(mut_id, "")
            baseline_resp = baseline_map.get(ctx_id, "")
            
            print(f"[{fixed_count+1}/{len(error_ids)}] Đang chạy lại {mut_id}...")
            judge_result = evaluate_with_llama(query, mutated_ctx, baseline_resp, mutated_resp)
            
            new_label = judge_result.get("label", "Error")
            if new_label != "Error":
                row["ai_label"] = new_label
                row["reason"] = judge_result.get("reason", "No reason provided")
                fixed_count += 1
                
            # Cập nhật file ngay lập tức để không bị mất dữ liệu nếu sập giữa chừng
            with open(results_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["mut_id", "ai_label", "reason"])
                writer.writeheader()
                writer.writerows(judgements)
                
            time.sleep(2)
            
    print(f"\n✅ Đã sửa thành công {fixed_count}/{len(error_ids)} lỗi.")
    print("🎉 HOÀN TẤT CHẠY LẠI CÁC CÂU LỖI 🎉")

if __name__ == "__main__":
    main()
