import csv
import os
import time
import requests
import re
from datetime import datetime

GROQ_API_KEY = "YOUR_API_KEY_HERE"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
ACTUAL_MODEL = "qwen/qwen3-32b"
LOGGED_MODEL = "qwen-3" 

MUTATED_CSV_FILE = "data/mutated/semantic_mutants.csv"
MUTATED_MD_DIR = "data/mutated_md_files"
LOG_FILE = "results/full_api_log.txt"

def setup_directories():
    os.makedirs("data/mutated", exist_ok=True)
    os.makedirs(MUTATED_MD_DIR, exist_ok=True)
    os.makedirs("results", exist_ok=True)

def check_resume_status(ctx_id, mut_num):
    """Kiểm tra xem file markdown của đột biến này đã tồn tại chưa để resume."""
    filename = f"{ctx_id}_MUT_{mut_num:02d}.md"
    filepath = os.path.join(MUTATED_MD_DIR, filename)
    return os.path.exists(filepath), filepath

def validate_mutation(mutated_text):
    """Kiểm tra tính hợp lệ của văn bản đột biến (không rỗng, giữ format)."""
    if not mutated_text or len(mutated_text.strip()) < 10:
        return False
    # Có thể thêm check regex tuỳ chọn ở đây, ví dụ kiểm tra code block Markdown
    return True

def generate_single_mutation(context_text, retry_count=3):
    prompt = f"""You are an expert software tester. Given the following paragraph from an API documentation, rewrite it to contain a subtle factual error (e.g., change a return status code, invert a logical condition) while maintaining perfect grammar and logical flow. Output ONLY the mutated text, no explanations.

Source text:
{context_text}"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": ACTUAL_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 4096
    }
    
    for attempt in range(retry_count):
        try:
            start_time = time.time()
            res = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if res.status_code == 429:
                print(f"⚠️ Dính Rate Limit (429)! Đang chờ 65s rồi thử lại (Lần {attempt+1}/{retry_count})...")
                time.sleep(65)
                continue
                
            res.raise_for_status()
            data = res.json()
            end_time = time.time()
            
            raw_content = data['choices'][0]['message']['content']
            mutated_text = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
            
            # Tính toán cost ước lượng
            total_tokens = data.get('usage', {}).get('total_tokens', 0)
            cost = total_tokens * 0.000001 
            
            if validate_mutation(mutated_text):
                return mutated_text, end_time - start_time, cost
            else:
                print(f"⚠️ Văn bản trả về bị rỗng hoặc lỗi format. Thử lại (Lần {attempt+1})...")
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ Lỗi API (Lần {attempt+1}): {e}")
            time.sleep(5)
            
    return None, 0, 0

def main():
    print("🚀 BẮT ĐẦU CHẠY FULL-SCALE MUTATION (416 FILES) 🚀")
    setup_directories()
    
    # 1. Đọc 32 file gốc
    try:
        with open("data/raw/test_cases.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            test_cases = list(reader)
    except FileNotFoundError:
        print("❌ LỖI: Không tìm thấy data/raw/test_cases.csv")
        return

    # Khởi tạo CSV kết quả nếu chưa có
    fieldnames = ["id", "mut_id", "original_context", "mutated_context"]
    if not os.path.exists(MUTATED_CSV_FILE):
        with open(MUTATED_CSV_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    # 2. Lặp qua 32 dòng x 13 lần = 416
    for row in test_cases:
        ctx_id = row['id']
        context_text = row['context_text']
        
        for mut_num in range(1, 14): # 1 đến 13
            # Cơ chế Resume
            exists, filepath = check_resume_status(ctx_id, mut_num)
            mut_id = f"{ctx_id}_MUT_{mut_num:02d}"
            
            if exists:
                print(f"⏭️  Bỏ qua {mut_id} (Đã tồn tại)")
                continue
                
            print(f"Đang sinh đột biến cho {mut_id}...")
            mutated_text, duration, cost = generate_single_mutation(context_text)
            
            if mutated_text:
                # 3a. Lưu ra file .md
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(mutated_text)
                    
                # 3b. Lưu append vào CSV
                with open(MUTATED_CSV_FILE, "a", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerow({
                        "id": ctx_id,
                        "mut_id": mut_id,
                        "original_context": context_text,
                        "mutated_context": mutated_text
                    })
                    
                # 3c. Ghi Log
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"[{timestamp}] ID: {mut_id} | Model: {LOGGED_MODEL} | Time: {duration:.2f}s | Cost: ${cost:.6f}\n")
                    
                print(f"✅ Thành công {mut_id} ({duration:.2f}s)")
            else:
                print(f"❌ THẤT BẠI hoàn toàn sau 3 lần thử đối với {mut_id}!")
                
            # Sleep 15 giây giữa mỗi file để an toàn Rate Limit
            time.sleep(15)

    print("\n🎉 HOÀN TẤT TẤT CẢ 416 QUÁ TRÌNH SINH ĐỘT BIẾN 🎉")

if __name__ == "__main__":
    main()
