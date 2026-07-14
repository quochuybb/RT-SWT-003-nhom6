import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix, classification_report
import os
import warnings

warnings.filterwarnings('ignore')

def main():
    human_file = 'results/human_eval_sample.csv'
    ai_file = 'results/ai_judgements_pilot.csv'
    
    if not os.path.exists(human_file) or not os.path.exists(ai_file):
        print(f"Error: Required files not found.")
        return
        
    human_df = pd.read_csv(human_file)
    ai_df = pd.read_csv(ai_file)
    
    merged_df = pd.merge(human_df, ai_df, on='mut_id', how='inner')
    
    if len(merged_df) == 0:
        print("No matching records found.")
        return
        
    labels = ["Abstain", "Faithful", "Inconsistent", "Hallucination", "Error"]
    
    y_true = merged_df['human_label'].fillna('Unknown')
    y_pred = merged_df['ai_label'].fillna('Unknown')
    
    kappa = cohen_kappa_score(y_true, y_pred)
    
    print("\n===========================================")
    print(f"Total evaluated matches: {len(merged_df)}")
    print(f"Cohen's Kappa: {kappa:.4f}")
    if kappa >= 0.6:
        print("-> AI Reliability is Good (>= 0.6). We can trust the AI labels.")
    else:
        print("-> AI Reliability is Fair/Poor (< 0.6). Prompt engineering needed.")
    print("===========================================\n")
    
    print("Confusion Matrix:")
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=[f"Human_{l}" for l in labels], columns=[f"AI_{l}" for l in labels])
    print(cm_df)
    
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, labels=[l for l in labels if l != "Error"]))

if __name__ == "__main__":
    main()
