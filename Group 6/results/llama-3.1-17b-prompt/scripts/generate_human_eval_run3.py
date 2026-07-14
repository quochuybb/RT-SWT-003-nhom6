"""
Tạo file human_eval_sample cho Run 3 (Không có System Prompt).
Sử dụng đúng 42 mut_id từ Run 2 để đảm bảo so sánh công bằng,
nhưng cập nhật mutated_response từ file mới (không có System Prompt).
"""
import csv
import os

def main():
    print("=== Tao Human Eval Sample cho Run 3 (Khong co System Prompt) ===")
    
    # 1. Đọc danh sách 42 mut_id từ file human_eval cũ
    old_sample_ids = []
    with open("results/human_eval_sample.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            old_sample_ids.append(row["mut_id"])
    print(f"Doc duoc {len(old_sample_ids)} mut_id tu file cu")
    
    # 2. Đọc mutated_context từ semantic_mutants.csv
    context_map = {}
    with open("data/mutated/semantic_mutants.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            context_map[row["mut_id"]] = row["mutated_context"]
    
    # 3. Đọc mutated_response MỚI từ full_mutated_responses.csv (Run 3)
    response_map = {}
    with open("results/full_mutated_responses.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            response_map[row["mut_id"]] = row
    
    # 4. Đọc ai_judgements để lấy nhãn AI cho từng mẫu
    ai_label_map = {}
    with open("results/ai_judgements.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ai_label_map[row["mut_id"]] = row["ai_label"]
    
    # 5. Tạo file human_eval mới
    output_file = "results/human_eval_sample_run3.csv"
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "mut_id", "query", "mutated_context", "mutated_response", 
            "ai_label", "human_label"
        ])
        writer.writeheader()
        
        found = 0
        for mut_id in old_sample_ids:
            resp_data = response_map.get(mut_id, {})
            if resp_data:
                writer.writerow({
                    "mut_id": mut_id,
                    "query": resp_data.get("query", ""),
                    "mutated_context": context_map.get(mut_id, ""),
                    "mutated_response": resp_data.get("mutated_response", ""),
                    "ai_label": ai_label_map.get(mut_id, ""),
                    "human_label": ""  # Để trống cho anh Đạt chấm tay
                })
                found += 1
            else:
                print(f"  CANH BAO: Khong tim thay {mut_id} trong file moi!")
    
    print(f"\nXuat thanh cong {found}/42 mau ra: {output_file}")
    print("Cot 'human_label' de trong cho anh cham tay.")
    print("Cot 'ai_label' la nhan AI da cham de doi chieu.")

if __name__ == "__main__":
    main()
