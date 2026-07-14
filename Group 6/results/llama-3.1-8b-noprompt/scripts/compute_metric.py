import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix, classification_report
import os

def main():
    human_file = 'results/human_eval_sample.csv'
    ai_file = 'results/ai_judgements.csv'
    
    if not os.path.exists(human_file) or not os.path.exists(ai_file):
        print(f"Error: Required files not found. Need both {human_file} and {ai_file}")
        return

    human_df = pd.read_csv(human_file)
    ai_df = pd.read_csv(ai_file)

    # Merge on mut_id
    merged = pd.merge(human_df, ai_df[['mut_id', 'ai_label']], on='mut_id', how='inner')

    if 'human_label' in merged.columns and 'ai_label' in merged.columns:
        df_clean = merged.dropna(subset=['human_label', 'ai_label']).copy()
        df_clean['human_label'] = df_clean['human_label'].astype(str).str.strip().str.replace('\xa0', '')
        df_clean['ai_label'] = df_clean['ai_label'].astype(str).str.strip().str.replace('\xa0', '')
        df_clean = df_clean[df_clean['human_label'] != '']
        
        if len(df_clean) > 0:
            kappa = cohen_kappa_score(df_clean['human_label'], df_clean['ai_label'])
            print(f'\n===========================================')
            print(f'Total evaluated matches: {len(df_clean)}')
            print(f'Cohen\'s Kappa: {kappa:.4f}')
            if kappa >= 0.6:
                print(f'-> AI Reliability is Good (>= 0.6). We can trust the AI labels.')
            else:
                print(f'-> AI Reliability is Fair/Poor (< 0.6). Prompt engineering needed.')
            print(f'===========================================\n')
            
            print('Confusion Matrix:')
            labels = sorted(list(set(df_clean['human_label'].unique().tolist() + df_clean['ai_label'].unique().tolist())))
            cm = pd.DataFrame(confusion_matrix(df_clean['human_label'], df_clean['ai_label'], labels=labels), index=[f"Human_{l}" for l in labels], columns=[f"AI_{l}" for l in labels])
            print(cm)
            
            print('\nClassification Report:')
            print(classification_report(df_clean['human_label'], df_clean['ai_label'], labels=labels))
        else:
            print('No valid overlapping data to calculate Kappa.')
    else:
        print('Columns not found in merged df.')

if __name__ == "__main__":
    main()
