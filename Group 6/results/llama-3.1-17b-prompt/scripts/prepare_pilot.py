import csv
import random

def main():
    # Set fixed random seed
    random.seed(42)

    # Read test cases
    with open('data/raw/test_cases.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Sample 10%
    sample_size = max(1, int(len(rows) * 0.1))
    sampled_rows = random.sample(rows, sample_size)

    # Write to pilot_sample.csv (without label)
    fieldnames_sample = ['id', 'cognitive_level', 'context_text', 'query']
    with open('data/pilot_sample.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_sample)
        writer.writeheader()
        for row in sampled_rows:
            writer.writerow({
                'id': row['id'],
                'cognitive_level': row['cognitive_level'],
                'context_text': row['context_text'],
                'query': row['query']
            })

    # Write to pilot_ground_truth.csv (with label)
    fieldnames_truth = ['id', 'cognitive_level', 'context_text', 'query', 'label']
    with open('data/pilot_ground_truth.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_truth)
        writer.writeheader()
        for row in sampled_rows:
            writer.writerow({
                'id': row['id'],
                'cognitive_level': row['cognitive_level'],
                'context_text': row['context_text'],
                'query': row['query'],
                'label': ''            # empty label for manual annotation
            })
    
    print(f"✅ Đã lấy ngẫu nhiên {sample_size} câu (10%) từ test_cases.csv với random seed=42.")
    print("✅ Đã lưu vào data/pilot_sample.csv và data/pilot_ground_truth.csv")

if __name__ == '__main__':
    main()
