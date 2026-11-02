"""Model loading and SMS prediction helpers."""
import json
import joblib
from src.preprocess import clean_text
from src.train import MODEL_PATH, METRICS_PATH, train_all

def load_model():
    if not MODEL_PATH.exists():
        train_all(log_to_mlflow=False)
    return joblib.load(MODEL_PATH)

def load_metrics():
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text())
    return {}

def predict_message(model, text: str) -> dict:
    cleaned = clean_text(text)
    probability = float(model.predict_proba([cleaned])[0][1])
    return {
        "label": "Spam" if probability >= 0.5 else "Not Spam",
        "spam_probability": probability,
        "cleaned": cleaned,
    }
