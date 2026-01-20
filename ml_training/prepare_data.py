import pandas as pd
import os
import requests
import re
import numpy as np

# Configuration
DATASET_DIR = "."
OUTPUT_DIR = "data"
INDONLU_URL = "https://raw.githubusercontent.com/indonlu/indonlu/master/dataset/smsa_doc-sentiment-prosa"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download {url}")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()

def prepare_sentiment_data():
    print("--- Preparing Sentiment Data ---")
    
    # 1. Download IndoNLU SmSA (Sentinel Analysis)
    train_url = f"{INDONLU_URL}/train_preprocess.tsv"
    valid_url = f"{INDONLU_URL}/valid_preprocess.tsv"
    
    download_file(train_url, f"{OUTPUT_DIR}/indonlu_train.tsv")
    download_file(valid_url, f"{OUTPUT_DIR}/indonlu_valid.tsv")
    
    # 2. Load IndoNLU
    cols = ['text', 'label']
    try:
        df_indonlu_train = pd.read_csv(f"{OUTPUT_DIR}/indonlu_train.tsv", sep='\t', names=cols)
        df_indonlu_valid = pd.read_csv(f"{OUTPUT_DIR}/indonlu_valid.tsv", sep='\t', names=cols)
        df_indonlu = pd.concat([df_indonlu_train, df_indonlu_valid])
        print(f"Loaded IndoNLU: {len(df_indonlu)} rows")
    except Exception as e:
        print(f"Error loading IndoNLU: {e}")
        df_indonlu = pd.DataFrame(columns=cols)

    # 3. Load Internal Dataset
    try:
        df_internal = pd.read_csv(os.path.join(DATASET_DIR, "dataset.csv"))
        # Combine title and description for text
        df_internal['text'] = df_internal['title'] + " " + df_internal['description']
        # Map labels if necessary (internal: 'positive', 'neutral', 'negative')
        # IndoNLU: 'positive', 'neutral', 'negative' (usually matches, but let's ensure)
        df_internal = df_internal[['text', 'label']]
        print(f"Loaded Internal Data: {len(df_internal)} rows")
    except Exception as e:
        print(f"Error loading internal dataset: {e}")
        df_internal = pd.DataFrame(columns=cols)

    # 4. Merge
    df_final = pd.concat([df_indonlu, df_internal], ignore_index=True)
    df_final['text'] = df_final['text'].apply(clean_text)
    
    # Check distribution
    print("Sentiment Distribution:")
    print(df_final['label'].value_counts())
    
    output_path = f"{OUTPUT_DIR}/final_sentiment_data.csv"
    df_final.to_csv(output_path, index=False)
    print(f"Saved merged sentiment data to {output_path}")

def prepare_category_data():
    print("\n--- Preparing Category Data ---")
    
    # Currently relying on Internal Data + Augmentation (since Kaggle requires API for News Title)
    # Ideally user manually downloads Kaggle dataset, but for now we use what we have
    
    try:
        df_internal = pd.read_csv(os.path.join(DATASET_DIR, "dataset.csv"))
        df_internal['text'] = df_internal['title'] + " " + df_internal['description']
        df_internal = df_internal[['text', 'category']]
        
        # Clean
        df_internal['text'] = df_internal['text'].apply(clean_text)
        
        print("Category Distribution:")
        print(df_internal['category'].value_counts())
        
        output_path = f"{OUTPUT_DIR}/final_category_data.csv"
        df_internal.to_csv(output_path, index=False)
        print(f"Saved category data to {output_path}")
        
    except Exception as e:
        print(f"Error preparing category data: {e}")

if __name__ == "__main__":
    prepare_sentiment_data()
    prepare_category_data()
