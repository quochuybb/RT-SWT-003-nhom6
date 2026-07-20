import os
import csv
import json
import time
import requests
import shutil

GROQ_API_KEY = "YOUR_API_KEY_HERE"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
MODEL = "llama-3.1-8b-instant"

def translate_to_english(text):
    prompt = f"Translate the following Vietnamese technical question about FastAPI to English. Only return the translated English string, nothing else.\n\nVietnamese: {text}\nEnglish:"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
    }
    for attempt in range(3):
        try:
            res = requests.post(GROQ_API_URL, headers=HEADERS, json=payload, timeout=15)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"].strip().strip('"')
            elif res.status_code == 429:
                time.sleep(10)
            else:
                time.sleep(2)
        except:
            time.sleep(2)
    return text # Fallback

def main():
    input_file = "data/raw/test_cases.csv"
    backup_file = "data/raw/test_cases_vn.csv"
    
    if not os.path.exists(backup_file):
        shutil.copy2(input_file, backup_file)
        
    rows = []
    with open(backup_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            
    print(f"Translating {len(rows)} queries to English...")
    for i, row in enumerate(rows):
        en_query = translate_to_english(row["query"])
        print(f"[{i+1}/32] Translated to EN: {en_query.encode('ascii', 'ignore').decode()}")
        row["query"] = en_query
        time.sleep(0.5)
        
    with open(input_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            
    print("Translation complete! Overwritten test_cases.csv")
    
if __name__ == '__main__':
    main()

