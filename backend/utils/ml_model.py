import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import re

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MAX_LEN = 100

class SentimentModel:
    def __init__(self):
        self.sentiment_model = None
        self.category_model = None
        self.tokenizer = None
        self.sentiment_label_encoder = None
        self.category_label_encoder = None
        
        self.load_models()

    def load_models(self):
        try:
            print("Loading Deep Learning models...")
            # Load Models
            self.sentiment_model = load_model(os.path.join(MODEL_DIR, "sentiment_dl_model.h5"))
            self.category_model = load_model(os.path.join(MODEL_DIR, "category_dl_model.h5"))
            
            # Load Tokenizer (Shared or specific? Script saves separate ones, let's load specifically)
            with open(os.path.join(MODEL_DIR, "sentiment_tokenizer.pickle"), 'rb') as handle:
                self.tokenizer = pickle.load(handle)
                
            # Load Label Encoders
            with open(os.path.join(MODEL_DIR, "sentiment_label_encoder.pickle"), 'rb') as handle:
                self.sentiment_label_encoder = pickle.load(handle)
                
            with open(os.path.join(MODEL_DIR, "category_label_encoder.pickle"), 'rb') as handle:
                self.category_label_encoder = pickle.load(handle)
                
            print("Models loaded successfully!")
        except Exception as e:
            print(f"Error loading models: {e}")
            print("Ensure train_dl_models.py has been run successfully.")

    def preprocess(self, text):
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        seq = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=MAX_LEN, padding='post', truncating='post')
        return padded

    def extract_keywords(self, text, top_n=5):
        # Fallback simple keyword extraction since DL doesn't give feature importance easily
        # We can implement a simple frequency based or just skip for now.
        # Let's return capitalized words as a heuristic or simple frequency
        words = re.findall(r'\w+', text.lower())
        unique_words = list(set(words))
        # Filter stop words (simple list)
        stopwords = ['dan', 'yang', 'di', 'ke', 'dari', 'ini', 'itu', 'untuk', 'pada', 'adalah']
        keywords = [w for w in unique_words if w not in stopwords and len(w) > 3]
        return keywords[:top_n]

    def predict(self, title, description):
        text = str(title) + " " + str(description)
        padded_text = self.preprocess(text)
        
        result = {
            "label": "Unknown",
            "confidence": "0%",
            "keywords": [],
            "category": "Umum"
        }
        
        if self.sentiment_model:
            # Predict Sentiment
            pred_probs = self.sentiment_model.predict(padded_text)[0]
            pred_idx = np.argmax(pred_probs)
            confidence = float(pred_probs[pred_idx] * 100)
            
            if self.sentiment_label_encoder:
                label = self.sentiment_label_encoder.inverse_transform([pred_idx])[0]
            else:
                label = str(pred_idx)
                
            result["label"] = label
            result["confidence"] = f"{confidence:.2f}%"

        if self.category_model:
            # Predict Category
            cat_probs = self.category_model.predict(padded_text)[0]
            cat_idx = np.argmax(cat_probs)
            
            if self.category_label_encoder:
                category = self.category_label_encoder.inverse_transform([cat_idx])[0]
            else:
                category = "Umum"
            
            result["category"] = category
            
        result["keywords"] = self.extract_keywords(text)
        
        return result

    # Dummy train method specifically to avoid breaking old calls if any, 
    # but strictly we rely on offline training now.
    def train(self):
        print("Training is now handled by ml_training/train_dl_models.py")

