import os
import csv
import pandas as pd

def main():
    print("🚀 BẮT ĐẦU TẠO CÁC FILE CÒN THIẾU CHO PILOT 🚀")
    
    # 1. Đọc pilot_llm_output.csv (Pilot Mutations)
    pilot_file = "results/pilot_llm_output.csv"
    if not os.path.exists(pilot_file):
        print(f"❌ Không tìm thấy {pilot_file}")
        return
        
    df_pilot = pd.read_csv(pilot_file)
    print(f"✅ Đã đọc {len(df_pilot)} mẫu từ {pilot_file}")
    
    # 2. Đọc full_mutated_responses.csv để lấy câu trả lời của RAG cho các mẫu này
    full_file = "results/full_mutated_responses.csv"
    if not os.path.exists(full_file):
        print(f"❌ Không tìm thấy {full_file}")
        return
        
    df_full = pd.read_csv(full_file)
    
    # 3. Tạo human_eval_sample_pilot.csv
    # Nó phải chứa ["mut_id", "query", "mutated_context", "mutated_response", "human_label"]
    human_eval_records = []
    
    for _, row in df_pilot.iterrows():
        ctx_id = row['id']
        query = row['query']
        mutated_context = row['mutated_context']
        
        # Tìm response tương ứng trong full_mutated_responses (vd: CTX_030_MUT_1)
        matches = df_full[df_full['mut_id'].str.startswith(f"{ctx_id}_MUT_")]
        
        if not matches.empty:
            mut_id = matches.iloc[0]['mut_id']
            mutated_response = matches.iloc[0]['mutated_response']
        else:
            mut_id = f"{ctx_id}_MUT_PILOT"
            mutated_response = "Abstain"
            
        human_eval_records.append({
            "mut_id": mut_id,
            "query": query,
            "mutated_context": mutated_context,
            "mutated_response": mutated_response,
            "human_label": "" # Để trống
        })
        
    human_file = "results/human_eval_sample_pilot.csv"
    df_human = pd.DataFrame(human_eval_records)
    df_human.to_csv(human_file, index=False)
    print(f"✅ Đã tạo {human_file} chứa 100% ({len(df_human)}) mẫu pilot.")

    # 4. Sửa lại run_experiment.py để trỏ tới file human_eval_sample_pilot.csv
    exp_file = "scripts/run_experiment.py"
    if os.path.exists(exp_file):
        with open(exp_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        content = content.replace(
            'with open("results/human_eval_sample.csv"', 
            'with open("results/human_eval_sample_pilot.csv"'
        )
        content = content.replace(
            'Chạy 42 mẫu trong human_eval_sample',
            'Chạy 100% mẫu pilot trong human_eval_sample_pilot'
        )
        
        with open(exp_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Đã cập nhật scripts/run_experiment.py để đọc từ human_eval_sample_pilot.csv trong chế độ pilot.")
    
    print("\n🎉 HOÀN TẤT! 🎉")
    print("Anh có thể chạy lệnh sau để chấm điểm AI cho đợt Pilot:")
    print("python scripts/run_experiment.py --mode pilot")

if __name__ == "__main__":
    main()
