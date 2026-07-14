import os
import requests
import json
import csv
import time

API_KEY = "YOUR_ANYTHINGLLM_API_KEY"
BASE_URL = "http://localhost:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

CLEAN_DOCS_DIR = "/home/huyico/Documents/Tool/CrawlSematic/Mutation_RAG/data/raw/baseline_docs"
STATE_FILE = "results/upload_state.json"
PILOT_BASELINE_WS = "pilot-baseline"

def upload_file(filepath):
    with open(filepath, 'rb') as f:
        files = {'file': f}
        res = requests.post(f"{BASE_URL}/document/upload", headers=HEADERS, files=files)
    if res.status_code == 200:
        data = res.json()
        if data.get("success") and len(data.get("documents", [])) > 0:
            return data["documents"][0]["location"]
    return None

def create_workspace(slug):
    res = requests.post(f"{BASE_URL}/workspace/new", headers=HEADERS, json={"name": slug})
    if res.status_code == 200:
        return res.json().get("workspace", {}).get("slug")
    return None

def update_embeddings(slug, locations):
    payload = {"adds": locations, "deletes": []}
    res = requests.post(f"{BASE_URL}/workspace/{slug}/update-embeddings", headers=HEADERS, json=payload)
    return res.status_code == 200

def chat_with_workspace(slug, query):
    payload = {"message": query, "mode": "chat"}
    res = requests.post(f"{BASE_URL}/workspace/{slug}/chat", headers=HEADERS, json=payload, timeout=120)
    if res.status_code == 200:
        return res.json().get("textResponse", "")
    return f"ERROR: {res.status_code}"

def main():
    print("🚀 BẮT ĐẦU CHẠY BASELINE PILOT 🚀")
    os.makedirs("results", exist_ok=True)
    
    upload_state = {"clean": {}, "mutated": {}}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            upload_state = json.load(f)
            
    # 1. Đảm bảo 32 file sạch đã được upload
    print("\n--- 1. Kiểm tra tài liệu sạch (Baseline) ---")
    clean_files = sorted([f for f in os.listdir(CLEAN_DOCS_DIR) if f.endswith(".md")])
    for f in clean_files:
        ctx_id = f.replace(".md", "")
        if ctx_id not in upload_state["clean"]:
            loc = upload_file(os.path.join(CLEAN_DOCS_DIR, f))
            if loc:
                upload_state["clean"][ctx_id] = loc
                with open(STATE_FILE, 'w') as sf:
                    json.dump(upload_state, sf)
            time.sleep(0.5)
            
    clean_locations = list(upload_state["clean"].values())
    
    # 2. Tạo Workspace 'pilot-baseline'
    print(f"\n--- 2. Khởi tạo Workspace: {PILOT_BASELINE_WS} ---")
    # Kiểm tra xem có chưa
    res_ws = requests.get(f"{BASE_URL}/workspaces", headers=HEADERS)
    existing = [w["slug"] for w in res_ws.json().get("workspaces", [])] if res_ws.status_code == 200 else []
    
    if PILOT_BASELINE_WS not in existing:
        create_workspace(PILOT_BASELINE_WS)
        print("Đã tạo mới Workspace. Đang nhúng (Embed) 32 file sạch vào VectorDB...")
        update_embeddings(PILOT_BASELINE_WS, clean_locations)
        time.sleep(5) # Chờ ChromaDB xử lý xong
    else:
        print(f"Workspace {PILOT_BASELINE_WS} đã tồn tại.")
        # Optional: Force update embeddings
        update_embeddings(PILOT_BASELINE_WS, clean_locations)
        
    # 3. Chạy Queries từ pilot_sample.csv
    print("\n--- 3. Bắn truy vấn (Queries) vào RAG ---")
    results = []
    log_file = "results/pilot_api_log.txt"
    
    with open('data/pilot_sample.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ctx_id = row['id']
            query = row['query']
            print(f"Đang hỏi câu: [{ctx_id}] {query}")
            
            start_time = time.time()
            answer = chat_with_workspace(PILOT_BASELINE_WS, query)
            duration = time.time() - start_time
            
            # Ghi log API
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write(f"[{timestamp}] ID: {ctx_id} | Model: AnythingLLM (Baseline) | Time: {duration:.2f}s | Cost: $0.00\n")
            
            results.append({
                "id": ctx_id,
                "query": query,
                "baseline_answer": answer
            })
            time.sleep(2) # Tránh rate limit của LLM
            
    # 4. Ghi file CSV
    out_file = "results/pilot_llm_output.csv"
    with open(out_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "query", "baseline_answer"])
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\n🎉 XONG! Kết quả lưu tại: {out_file}")
    print(f"📄 Đã ghi thêm log vào: {log_file}")

if __name__ == '__main__':
    main()
