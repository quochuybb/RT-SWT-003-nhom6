import requests
import json
import time

# Sử dụng Groq API như bạn đã dùng thành công ở Giai đoạn 3
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

def test_connection():
    print("Dang kiem tra ket noi den Groq API (Llama 3.1 8B)...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "Hello, are you ready to act as an LLM judge for my project?"}],
        "temperature": 0.0,
        "max_tokens": 50
    }
    
    start_time = time.time()
    try:
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        end_time = time.time()
        
        print("\n[OK] KET NOI THANH CONG! (Gate E3 Passed)")
        print(f"Phan hoi tu LLM: {data['choices'][0]['message']['content']}")
        print(f"Thoi gian phan hoi: {end_time - start_time:.2f}s")
        print(f"Token su dung: {data['usage']['total_tokens']}")
        
    except Exception as e:
        print("\n[FAILED] KET NOI THAT BAI!")
        print(f"Loi: {e}")

if __name__ == "__main__":
    test_connection()
