import os
import requests
import json
import time

API_KEY = "YOUR_ANYTHINGLLM_API_KEY"
BASE_URL = "http://localhost:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

CLEAN_DOCS_DIR = "/home/huyico/Documents/Tool/CrawlSematic/Group6/data/baseline_docs"
MUTATED_DOCS_DIR = "/home/huyico/Documents/Tool/CrawlSematic/Group6/data/mutated_md_files"
STATE_FILE = "results/upload_state.json"

def upload_file(filepath):
    """Uploads a file to AnythingLLM and returns its location identifier."""
    with open(filepath, 'rb') as f:
        files = {'file': f}
        # Cần truyền headers không có Content-Type để requests tự set multipart/form-data
        res = requests.post(f"{BASE_URL}/document/upload", headers=HEADERS, files=files)
    
    if res.status_code == 200:
        data = res.json()
        if data.get("success") and len(data.get("documents", [])) > 0:
            return data["documents"][0]["location"]
    
    print(f"❌ Lỗi khi upload {filepath}: {res.status_code} - {res.text}")
    return None

def create_workspace(slug):
    """Creates a workspace and returns its slug."""
    payload = {"name": slug}
    res = requests.post(f"{BASE_URL}/workspace/new", headers=HEADERS, json=payload)
    if res.status_code == 200:
        data = res.json()
        return data.get("workspace", {}).get("slug")
    print(f"❌ Lỗi khi tạo workspace {slug}: {res.status_code} - {res.text}")
    return None

def update_embeddings(workspace_slug, document_locations):
    """Updates embeddings for a workspace with the given documents."""
    payload = {
        "adds": document_locations,
        "deletes": []
    }
    res = requests.post(f"{BASE_URL}/workspace/{workspace_slug}/update-embeddings", headers=HEADERS, json=payload)
    if res.status_code == 200:
        return True
    print(f"❌ Lỗi khi update embeddings cho {workspace_slug}: {res.status_code} - {res.text}")
    return False

def main():
    print("🚀 BẮT ĐẦU TỰ ĐỘNG HÓA TẠO 416 WORKSPACES 🚀")
    
    # 1. Quản lý Upload State để không phải upload lại nếu code bị gián đoạn
    upload_state = {"clean": {}, "mutated": {}}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            upload_state = json.load(f)
            print("Đã load trạng thái upload từ trước.")

    # 2. Upload Clean Docs (32 files)
    print("\n--- BƯỚC 1: UPLOAD TÀI LIỆU SẠCH (32 FILE) ---")
    clean_files = sorted([f for f in os.listdir(CLEAN_DOCS_DIR) if f.endswith(".md")])
    for f in clean_files:
        ctx_id = f.replace(".md", "") # Ví dụ: CTX_001
        if ctx_id not in upload_state["clean"]:
            filepath = os.path.join(CLEAN_DOCS_DIR, f)
            print(f"Đang upload {f}...")
            loc = upload_file(filepath)
            if loc:
                upload_state["clean"][ctx_id] = loc
                # Lưu state liên tục
                with open(STATE_FILE, 'w') as sf:
                    json.dump(upload_state, sf)
            time.sleep(0.5)

    # 3. Upload Mutated Docs (416 files)
    print("\n--- BƯỚC 2: UPLOAD TÀI LIỆU ĐỘT BIẾN (416 FILE) ---")
    mutated_files = sorted([f for f in os.listdir(MUTATED_DOCS_DIR) if f.endswith(".md")])
    for f in mutated_files:
        mut_id = f.replace(".md", "") # Ví dụ: CTX_001_MUT_01
        if mut_id not in upload_state["mutated"]:
            filepath = os.path.join(MUTATED_DOCS_DIR, f)
            print(f"Đang upload {f}...")
            loc = upload_file(filepath)
            if loc:
                upload_state["mutated"][mut_id] = loc
                with open(STATE_FILE, 'w') as sf:
                    json.dump(upload_state, sf)
            time.sleep(0.5)
            
    # 4. Tạo Workspaces
    print("\n--- BƯỚC 3: TẠO VÀ EMBED 416 WORKSPACES ---")
    # Lấy danh sách các workspace đã tạo để tránh tạo trùng (dùng API get workspaces)
    res_ws = requests.get(f"{BASE_URL}/workspaces", headers=HEADERS)
    existing_workspaces = []
    if res_ws.status_code == 200:
        existing_workspaces = [w["slug"] for w in res_ws.json().get("workspaces", [])]

    # Vòng lặp cho 416 đột biến
    for mut_id, mut_loc in upload_state["mutated"].items():
        # mut_id có dạng: CTX_001_MUT_01 -> Tách ra để lấy ctx_id (CTX_001)
        parts = mut_id.split("_MUT_")
        if len(parts) != 2:
            continue
            
        target_ctx_id = parts[0] # CTX_001
        mut_number = parts[1]    # 01
        
        # Format slug: ctx-001-mut-01
        slug = f"ctx-{target_ctx_id.split('_')[1]}-mut-{mut_number}"
        
        if slug in existing_workspaces:
            print(f"⚠️ Workspace {slug} đã tồn tại. Bỏ qua...")
            continue
            
        print(f"Đang xử lý Workspace: {slug} ...")
        
        # Chuẩn bị danh sách tài liệu: 31 file sạch + 1 file đột biến
        doc_locations = []
        for clean_id, clean_loc in upload_state["clean"].items():
            if clean_id != target_ctx_id:
                doc_locations.append(clean_loc)
        
        # Thêm file đột biến
        doc_locations.append(mut_loc)
        
        if len(doc_locations) != 32:
            print(f"❌ CẢNH BÁO: Workspace {slug} không đủ 32 files! (Có {len(doc_locations)} files)")
            
        # Tạo workspace
        created_slug = create_workspace(slug)
        if created_slug:
            # Nhúng embeddings
            success = update_embeddings(created_slug, doc_locations)
            if success:
                print(f"✅ Hoàn thành: {created_slug}")
            else:
                print(f"❌ Tạo được workspace nhưng nhúng thất bại: {created_slug}")
        
        time.sleep(1) # Chờ 1 giây để server không bị quá tải
        
    print("\n🎉 XONG! TẤT CẢ 416 WORKSPACES ĐÃ ĐƯỢC THIẾT LẬP THÀNH CÔNG 🎉")

if __name__ == '__main__':
    main()
