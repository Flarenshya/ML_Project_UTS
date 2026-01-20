import pandas as pd
import numpy as np
import pickle
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Conv1D, GlobalMaxPooling1D, Bidirectional, MaxPooling1D
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import logging
import traceback

# Configuration
DATA_DIR = "data"
MODEL_DIR = "backend/utils/models"
MAX_WORDS = 10000
MAX_LEN = 100
EMBEDDING_DIM = 100

os.makedirs(MODEL_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(filename='training.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_hybrid_model(input_dim, output_dim, loss_fn):
    # Hybrid CNN-LSTM Architecture
    model = Sequential([
        Embedding(input_dim=input_dim, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
        
        # CNN Layer (Feature Extraction)
        Conv1D(filters=64, kernel_size=3, padding='same', activation='relu'),
        MaxPooling1D(pool_size=2),
        
        # LSTM Layer (Sequence Modeling)
        Bidirectional(LSTM(64)),
        Dropout(0.3),
        
        # Dense Layers (Classification)
        Dense(32, activation='relu'),
        Dense(output_dim, activation='softmax')
    ])
    
    model.compile(loss=loss_fn, optimizer='adam', metrics=['accuracy'])
    return model

import logging
import traceback

# Setup logging
logging.basicConfig(filename='training.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

import matplotlib.pyplot as plt

def plot_history(history, model_name):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)
    
    plt.figure(figsize=(12, 5))
    
    # Accuracy Plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, 'bo-', label='Training Accuracy')
    plt.plot(epochs, val_acc, 'r*-', label='Validation Accuracy')
    plt.title(f'{model_name} Accuracy')
    plt.legend()
    
    # Loss Plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, 'bo-', label='Training Loss')
    plt.plot(epochs, val_loss, 'r*-', label='Validation Loss')
    plt.title(f'{model_name} Loss')
    plt.legend()
    
    # Save
    plot_path = f"{MODEL_DIR}/{model_name.lower().replace(' ', '_')}_history.png"
    plt.savefig(plot_path)
    plt.close()
    print(f"Graph saved to {plot_path}")
    logging.info(f"Graph saved to {plot_path}")

def train_sentiment_model():
    print("--- Training Sentiment Model ---")
    logging.info("Starting Sentiment Training")
    try:
        df = pd.read_csv(f"{DATA_DIR}/final_sentiment_data.csv")
        df['text'] = df['text'].astype(str)
        
        # Tokenizer
        tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
        tokenizer.fit_on_texts(df['text'])
        sequences = tokenizer.texts_to_sequences(df['text'])
        padded = pad_sequences(sequences, maxlen=MAX_LEN, padding='post', truncating='post')
        
        # Encode Labels
        label_encoder = LabelEncoder()
        labels = label_encoder.fit_transform(df['label'])
        print("Sentiment Labels:", list(label_encoder.classes_))
        logging.info(f"Sentiment Labels: {list(label_encoder.classes_)}")
        num_classes = len(label_encoder.classes_)
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(padded, labels, test_size=0.2, random_state=42)
        
        # Build Model
        model = create_hybrid_model(input_dim=MAX_WORDS, output_dim=num_classes, loss_fn='sparse_categorical_crossentropy')
        
        # Train
        history = model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test), batch_size=32)
        
        # Plot
        plot_history(history, "Sentiment Model")
        
        # Save
        model.save(f"{MODEL_DIR}/sentiment_dl_model.h5")
        with open(f"{MODEL_DIR}/sentiment_tokenizer.pickle", 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(f"{MODEL_DIR}/sentiment_label_encoder.pickle", 'wb') as handle:
            pickle.dump(label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        print("Sentiment Model Saved!")
        logging.info("Sentiment Model Saved Successfully")
        
    except Exception as e:
        print(f"Error training sentiment model: {e}")
        logging.error(f"Error training sentiment model: {e}")
        logging.error(traceback.format_exc())
        traceback.print_exc()

def train_category_model():
    print("\n--- Training Category Model ---")
    logging.info("Starting Category Training")
    try:
        df = pd.read_csv(f"{DATA_DIR}/final_category_data.csv")
        df['text'] = df['text'].astype(str)
        
        # Tokenizer
        tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
        tokenizer.fit_on_texts(df['text'])
        sequences = tokenizer.texts_to_sequences(df['text'])
        padded = pad_sequences(sequences, maxlen=MAX_LEN, padding='post', truncating='post')
        
        # Encode Labels
        label_encoder = LabelEncoder()
        labels = label_encoder.fit_transform(df['category'])
        print("Category Labels:", list(label_encoder.classes_))
        logging.info(f"Category Labels: {list(label_encoder.classes_)}")
        num_classes = len(label_encoder.classes_)
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(padded, labels, test_size=0.2, random_state=42)
        
        # Build Model
        model = create_hybrid_model(input_dim=MAX_WORDS, output_dim=num_classes, loss_fn='sparse_categorical_crossentropy')
        
        # Train
        history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), batch_size=32)
        
        # Plot
        plot_history(history, "Category Model")
        
        # Save
        model.save(f"{MODEL_DIR}/category_dl_model.h5")
        with open(f"{MODEL_DIR}/category_tokenizer.pickle", 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(f"{MODEL_DIR}/category_label_encoder.pickle", 'wb') as handle:
            pickle.dump(label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        print("Category Model Saved!")
        logging.info("Category Model Saved Successfully")
        
    except Exception as e:
        print(f"Error training category model: {e}")
        logging.error(f"Error training category model: {e}")
        logging.error(traceback.format_exc())
        traceback.print_exc()


if __name__ == "__main__":
    train_sentiment_model()
    train_category_model()
