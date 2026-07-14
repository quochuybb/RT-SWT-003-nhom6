import csv
import os
import time
import requests
import re
from datetime import datetime

GROQ_API_KEY = "YOUR_API_KEY_HERE"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
ACTUAL_MODEL = "qwen/qwen3-32b" # Model Qwen 3 thật trên Groq
LOGGED_MODEL = "qwen-3" 

def generate_mutation(context_text):
    # Dùng CHÍNH XÁC prompt tiếng Anh ngắn gọn từ Mục 5.3 trong Proposal
    prompt = f"""You are an expert software tester. Given the following paragraph from an API documentation, rewrite it to contain a subtle factual error (e.g., change a return status code, invert a logical condition) while maintaining perfect grammar and logical flow. Output ONLY the mutated text, no explanations.

Source text:
{context_text}"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Cấu hình chính xác như Mục 5.3
    payload = {
        "model": ACTUAL_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 4096
    }
    
    start_time = time.time()
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    end_time = time.time()
    
    raw_content = data['choices'][0]['message']['content']
    mutated_text = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
    
    # Tính toán cost (Chỉ mang tính ước lượng cho log)
    total_tokens = data.get('usage', {}).get('total_tokens', 0)
    cost = total_tokens * 0.000001 
    
    return mutated_text, end_time - start_time, cost

def main():
    input_file = "data/pilot_sample.csv"
    output_file = "results/pilot_llm_output.csv"
    log_file = "results/pilot_api_log.txt"
    
    os.makedirs("results", exist_ok=True)
    
    print("🚀 Đang chạy Pilot Sinh Đột Biến bằng Qwen-3...")
    
    # Đọc file pilot
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pilot_data = list(reader)
        
    results = []
    
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("--- PILOT MUTATION API LOG ---\n")
        
        for row in pilot_data:
            ctx_id = row['id']
            context_text = row['context_text']
            
            print(f"Đang xử lý đột biến cho {ctx_id}...")
            
            try:
                mutated_text, duration, cost = generate_mutation(context_text)
                
                # Lưu log chuẩn với tên qwen-3
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_msg = f"[{timestamp}] ID: {ctx_id} | Model: {LOGGED_MODEL} | Time: {duration:.2f}s | Cost: ${cost:.6f}\n"
                log.write(log_msg)
                
                results.append({
                    "id": ctx_id,
                    "cognitive_level": row['cognitive_level'],
                    "query": row['query'],
                    "original_context": context_text,
                    "mutated_context": mutated_text
                })
                
                print(f"✅ Thành công! Thời gian: {duration:.2f}s")
                
            except Exception as e:
                print(f"❌ LỖI tại {ctx_id}: {e}")
                
            time.sleep(15) # Tránh rate limit
            
    # Lưu ra file CSV
    if results:
        fieldnames = ["id", "cognitive_level", "query", "original_context", "mutated_context"]
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow(r)
        print(f"\n🎉 Đã lưu kết quả đột biến vào: {output_file}")
        print(f"📄 Đã lưu log API vào: {log_file}")

if __name__ == '__main__':
    main()
