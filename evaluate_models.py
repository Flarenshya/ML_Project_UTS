import pandas as pd
import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Configuration
DATA_DIR = "data"
MODEL_DIR = "backend/utils/models"
MAX_LEN = 100

def evaluate_sentiment():
    print("\n" + "="*50)
    print("ANALISIS MODEL SENTIMEN")
    print("="*50)
    
    try:
        # Load Data
        df = pd.read_csv(f"{DATA_DIR}/final_sentiment_data.csv")
        df['text'] = df['text'].astype(str)
        
        # Load Tokenizer & Encoder
        with open(f"{MODEL_DIR}/sentiment_tokenizer.pickle", 'rb') as handle:
            tokenizer = pickle.load(handle)
        with open(f"{MODEL_DIR}/sentiment_label_encoder.pickle", 'rb') as handle:
            label_encoder = pickle.load(handle)
            
        # Load Model
        model = load_model(f"{MODEL_DIR}/sentiment_dl_model.h5")
        
        # Prepare Data
        sequences = tokenizer.texts_to_sequences(df['text'])
        X = pad_sequences(sequences, maxlen=MAX_LEN, padding='post', truncating='post')
        y_true = label_encoder.transform(df['label'])
        
        # Split (Same seed as training to evaluate on "Test" set)
        _, X_test, _, y_test = train_test_split(X, y_true, test_size=0.2, random_state=42)
        
        # Predict
        y_pred_probs = model.predict(X_test, verbose=0)
        y_pred = np.argmax(y_pred_probs, axis=1)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        print(f"\n✅ Akurasi Keseluruhan: {acc*100:.2f}%")
        
        print("\n📊 Laporan Klasifikasi:")
        print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
        
        print("\n📉 Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
    except Exception as e:
        print(f"Error validating sentiment: {e}")

def evaluate_category():
    print("\n" + "="*50)
    print("ANALISIS MODEL KATEGORI")
    print("="*50)
    
    try:
        # Load Data
        df = pd.read_csv(f"{DATA_DIR}/final_category_data.csv")
        df['text'] = df['text'].astype(str)
        
        # Load Tokenizer & Encoder
        with open(f"{MODEL_DIR}/category_tokenizer.pickle", 'rb') as handle:
            tokenizer = pickle.load(handle)
        with open(f"{MODEL_DIR}/category_label_encoder.pickle", 'rb') as handle:
            label_encoder = pickle.load(handle)
            
        # Load Model
        model = load_model(f"{MODEL_DIR}/category_dl_model.h5")
        
        # Prepare Data
        sequences = tokenizer.texts_to_sequences(df['text'])
        X = pad_sequences(sequences, maxlen=MAX_LEN, padding='post', truncating='post')
        y_true = label_encoder.transform(df['category'])
        
        # Split
        _, X_test, _, y_test = train_test_split(X, y_true, test_size=0.2, random_state=42)
        
        # Predict
        y_pred_probs = model.predict(X_test, verbose=0)
        y_pred = np.argmax(y_pred_probs, axis=1)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        print(f"\n✅ Akurasi Keseluruhan: {acc*100:.2f}%")
        
        print("\n📊 Laporan Klasifikasi:")
        print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
        
    except Exception as e:
        print(f"Error validating category: {e}")

if __name__ == "__main__":
    evaluate_sentiment()
    evaluate_category()
