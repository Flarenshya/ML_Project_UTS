import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

MODEL_FILE = "backend/sentiment_model.pkl"
DATASET_FILE = "dataset.csv"

class SentimentModel:
    def __init__(self):
        self.model = None
        if not os.path.exists(DATASET_FILE):
            raise FileNotFoundError(f"Dataset file not found: {DATASET_FILE}")
        if os.path.exists(MODEL_FILE):
            self.model = joblib.load(MODEL_FILE)
        else:
            self.train()

    def train(self):
        df = pd.read_csv(DATASET_FILE)
        # 🔹 Hapus baris yang ada NaN di kolom penting
        df = df.dropna(subset=['title', 'description', 'label'])

        # 🔹 Gabungkan teks
        df['text'] = df['title'].astype(str) + " " + df['description'].astype(str)

        X_train, X_test, y_train, y_test = train_test_split(
            df['text'], df['label'], test_size=0.2, random_state=42
        )

        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB())
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


    def predict(self, title, description):
        text = str(title) + " " + str(description)
        label = self.model.predict([text])[0]
        return label
