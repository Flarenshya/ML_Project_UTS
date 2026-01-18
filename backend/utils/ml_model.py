import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import joblib
import os
import numpy as np

MODEL_FILE = "backend/sentiment_model.pkl"
DATASET_FILE = "dataset.csv"

class SentimentModel:
    def __init__(self):
        self.model = None
        self.category_model = None # Initialize attribute

        if not os.path.exists(DATASET_FILE):
            raise FileNotFoundError(f"Dataset file not found: {DATASET_FILE}")
        
        # Load Sentiment Model
        if os.path.exists(MODEL_FILE):
            try:
                self.model = joblib.load(MODEL_FILE)
            except:
                self.train()
        else:
            self.train()

        # Load Category Model
        CATEGORY_MODEL_FILE = "backend/category_model.pkl"
        if os.path.exists(CATEGORY_MODEL_FILE):
            try:
                self.category_model = joblib.load(CATEGORY_MODEL_FILE)
            except:
                self.train_category_model()
        else:
            self.train_category_model()

    def train_category_model(self):
        print("Training category model...")
        df = pd.read_csv(DATASET_FILE)
        # Ensure category column exists
        if 'category' not in df.columns:
            print("Category column missing, skipping category training.")
            return

        df = df.dropna(subset=['title', 'description', 'category'])
        df['text'] = df['title'].astype(str) + " " + df['description'].astype(str)

        X_train, X_test, y_train, y_test = train_test_split(
            df['text'], df['category'], test_size=0.2, random_state=42
        )

        # Deep Learning for Categorization (MLP)
        mlp_category = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, activation='relu', solver='adam', random_state=42)

        self.category_model = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('mlp', mlp_category)
        ])
        
        self.category_model.fit(X_train, y_train)
        joblib.dump(self.category_model, "backend/category_model.pkl") 
        print("Category model trained and saved.")

    def train(self):

        print("Training model...")
        df = pd.read_csv(DATASET_FILE)
        # 🔹 Hapus baris yang ada NaN di kolom penting
        df = df.dropna(subset=['title', 'description', 'label'])

        # 🔹 Gabungkan teks
        df['text'] = df['title'].astype(str) + " " + df['description'].astype(str)

        X_train, X_test, y_train, y_test = train_test_split(
            df['text'], df['label'], test_size=0.2, random_state=42
        )

        # Ensemble Model: NB + Logistic Regression + SVM + Neural Network (Deep Learning)
        clf1 = MultinomialNB()
        clf2 = LogisticRegression(random_state=42, max_iter=1000)
        clf3 = SVC(kernel='linear', probability=True, random_state=42)
        
        # Deep Learning Layer (Multi-Layer Perceptron)
        clf4 = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=500, activation='relu', solver='adam', random_state=42)

        voting_clf = VotingClassifier(
            estimators=[
                ('nb', clf1), 
                ('lr', clf2), 
                ('svc', clf3),
                ('mlp_neural_network', clf4)
            ],
            voting='soft'
        )

        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', voting_clf)
        ])
        self.model.fit(X_train, y_train)

        joblib.dump(self.model, MODEL_FILE)

        y_pred = self.model.predict(X_test)
        metrics = {
            "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
            "precision": round(precision_score(y_test, y_pred, average='weighted') * 100, 2),
            "recall": round(recall_score(y_test, y_pred, average='weighted') * 100, 2),
            "f1_score": round(f1_score(y_test, y_pred, average='weighted') * 100, 2)
        }

        print("Training completed!")
        print("Metrics:", metrics)
        return metrics

    def extract_keywords(self, text, top_n=5):
        try:
            vectorizer = self.model.named_steps['tfidf']
            feature_names = vectorizer.get_feature_names_out()
            tfidf_matrix = vectorizer.transform([text])
            sorted_items = sorted(
                zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0]),
                key=lambda x: -x[1]
            )
            # Filter only words with non-zero score
            keywords = [word for word, score in sorted_items if score > 0][:top_n]
            return keywords
        except Exception as e:
            print("Error extracting keywords:", e)
            return []

    def predict(self, title, description):
        text = str(title) + " " + str(description)
        
        # Predict Label
        label = self.model.predict([text])[0]
        
        # Predict Probability (Confidence)
        proba = self.model.predict_proba([text])[0]
        confidence = round(max(proba) * 100, 2)
        
        # Extract Keywords
        keywords = self.extract_keywords(text)

        # Predict Category
        category = "Umum" # Default category
        if self.category_model: # Check if category model is loaded
            category = self.category_model.predict([text])[0]

        return {
            "label": label,
            "confidence": f"{confidence}%",
            "keywords": keywords,
            "category": category
        }
