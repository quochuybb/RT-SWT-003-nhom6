import os
import csv
import json
import time
import requests
from datetime import datetime

API_KEY = "YOUR_ANYTHINGLLM_API_KEY"
BASE_URL = "http://localhost:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

CLEAN_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "baseline_docs")
MUTATED_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "mutated_md_files")
STATE_FILE = "results/upload_state.json"
RESULTS_FILE = "results/full_mutated_responses.csv"

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
    payload = {"name": slug}
    res = requests.post(f"{BASE_URL}/workspace/new", headers=HEADERS, json=payload)
    if res.status_code == 200:
        return res.json().get("workspace", {}).get("slug")
    return None

def delete_workspace(slug):
    res = requests.delete(f"{BASE_URL}/workspace/{slug}", headers=HEADERS)
    return res.status_code == 200

def update_embeddings(workspace_slug, document_locations):
    payload = {"adds": document_locations, "deletes": []}
    res = requests.post(f"{BASE_URL}/workspace/{workspace_slug}/update-embeddings", headers=HEADERS, json=payload)
    return res.status_code == 200

def attack_workspace(workspace_slug, query):
    payload = {"message": query, "mode": "query"}
    try:
        res = requests.post(f"{BASE_URL}/workspace/{workspace_slug}/chat", headers=HEADERS, json=payload, timeout=90)
        if res.status_code == 200:
            data = res.json()
            return data.get("textResponse", "Abstain")
    except Exception as e:
        print(f"Lỗi kết nối / Timeout khi hỏi {workspace_slug}: {e}")
    return "Abstain"

def load_queries():
    queries = {}
    with open("data/raw/test_cases.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            queries[row["id"]] = row["query"]
    return queries

def main():
    print("--- BAT DAU CHAY BATCHED ATTACK (GIAI DOAN 4) ---")
    os.makedirs("results", exist_ok=True)
    
    # 1. Tải và map queries
    queries_map = load_queries()
    
    # 2. Upload state
    upload_state = {"clean": {}, "mutated": {}}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            upload_state = json.load(f)
            
    print("\n--- BƯỚC 1: KIỂM TRA UPLOAD TÀI LIỆU ---")
    clean_files = sorted([f for f in os.listdir(CLEAN_DOCS_DIR) if f.endswith(".md")])
    for i, f in enumerate(clean_files):
        ctx_id = f.replace(".md", "")
        if ctx_id not in upload_state["clean"]:
            print(f"  Uploading clean [{i+1}/{len(clean_files)}]: {f}")
            loc = upload_file(os.path.join(CLEAN_DOCS_DIR, f))
            if loc: upload_state["clean"][ctx_id] = loc
            time.sleep(0.2)
        else:
            print(f"  Skip clean [{i+1}/{len(clean_files)}]: {f} (da upload)")
            
    mutated_files = sorted([f for f in os.listdir(MUTATED_DOCS_DIR) if f.endswith(".md")])
    print(f"\n  Tong so file mutated can upload: {len(mutated_files)}")
    for i, f in enumerate(mutated_files):
        mut_id = f.replace(".md", "")
        if mut_id not in upload_state["mutated"]:
            print(f"  Uploading mutated [{i+1}/{len(mutated_files)}]: {f}")
            loc = upload_file(os.path.join(MUTATED_DOCS_DIR, f))
            if loc: upload_state["mutated"][mut_id] = loc
            time.sleep(0.2)
        else:
            print(f"  Skip mutated [{i+1}/{len(mutated_files)}]: {f} (da upload)")
            
    with open(STATE_FILE, 'w') as sf:
        json.dump(upload_state, sf)

    # 3. Khởi tạo file kết quả
    fieldnames = ["mut_id", "query", "mutated_response"]
    existing_results = set()
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
    else:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_results.add(row["mut_id"])

    # 4. Chia mẻ (Batches of 20)
    print("\n--- BƯỚC 2: TIẾN HÀNH BATCHED ATTACK ---")
    all_mutations = sorted(list(upload_state["mutated"].items()))
    
    # Lọc bỏ những mut_id đã có kết quả
    pending_mutations = [(mut_id, loc) for mut_id, loc in all_mutations if mut_id not in existing_results]
    
    BATCH_SIZE = 20
    for i in range(0, len(pending_mutations), BATCH_SIZE):
        batch = pending_mutations[i:i+BATCH_SIZE]
        print(f"\n🔄 Bắt đầu cụm mới (tiến độ: {len(existing_results)+i}/{len(all_mutations)})")
        
        batch_slugs = []
        
        # 4a. Khởi tạo & Embed
        for mut_id, mut_loc in batch:
            target_ctx_id = mut_id.split("_MUT_")[0]
            mut_num = mut_id.split("_MUT_")[1]
            slug = f"ctx-{target_ctx_id.split('_')[1]}-mut-{mut_num}"
            
            created_slug = create_workspace(slug)
            if not created_slug:
                created_slug = slug # Fallback nếu đã tồn tại
                
            doc_locations = [loc for cid, loc in upload_state["clean"].items() if cid != target_ctx_id]
            doc_locations.append(mut_loc)
            
            success = update_embeddings(created_slug, doc_locations)
            if success:
                batch_slugs.append((mut_id, created_slug, target_ctx_id))
            else:
                print(f"❌ Nhúng lỗi cho {created_slug}")
            time.sleep(0.5)
            
        # Nghỉ để tránh Rate Limit của Groq/AnythingLLM
        time.sleep(12)
        
        # 4b. Attack
        batch_results = []
        for mut_id, slug, target_ctx_id in batch_slugs:
            query = queries_map.get(target_ctx_id, "")
            print(f"⚔️ Đang hỏi {slug}...")
            response = attack_workspace(slug, query)
            batch_results.append({
                "mut_id": mut_id,
                "query": query,
                "mutated_response": response
            })
            
        # 4c. Lưu kết quả
        with open(RESULTS_FILE, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for res in batch_results:
                writer.writerow(res)
                
        # 4d. Cleanup
        print("🧹 Đang dọn dẹp (xóa) workspaces trong cụm...")
        for _, slug, _ in batch_slugs:
            delete_workspace(slug)
            
    print("\n🎉 HOÀN TẤT GIAI ĐOẠN 4 (TẤN CÔNG 416 WORKSPACE) 🎉")

if __name__ == '__main__':
    main()
