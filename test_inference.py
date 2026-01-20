from backend.utils.ml_model import SentimentModel
import os

print("Initializing SentimentModel (Deep Learning)...")
try:
    model = SentimentModel()
    
    test_cases = [
        ("Tutorial Python yang sangat bagus", "Saya sangat suka video ini, penjelasannya jelas."),
        ("Makanan ini basi dan tidak enak", "Sangat mengecewakan, buang-buang uang."),
        ("Vlog jalan-jalan ke Bali", "Pemandangan indah tapi cuaca agak panas.")
    ]
    
    print("\n--- Testing Predictions ---")
    for title, desc in test_cases:
        result = model.predict(title, desc)
        print(f"\nInput: {title}")
        print(f"Prediction: {result}")
        
    print("\n✅ Inference Test Passed!")
except Exception as e:
    print(f"\n❌ Inference Test Failed: {e}")
    import traceback
    traceback.print_exc()
