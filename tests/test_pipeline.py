import pandas as pd
from src.preprocess import clean_text
from src.etl import validate, transform
from src.train import build_pipeline, evaluate
from sklearn.naive_bayes import MultinomialNB

def test_clean_text_removes_punctuation_and_stopwords():
    assert clean_text("WIN a FREE Prize!!!") == "win free prize"

def test_clean_text_masks_urls():
    assert "urltoken" in clean_text("Visit https://example.com now")

def test_validate_accepts_ham_and_spam():
    validate(pd.DataFrame({"label": ["ham", "spam"], "text": ["hello", "win prize"]}))

def test_transform_creates_features():
    raw = pd.DataFrame({"label": ["ham", "spam"], "text": ["hello friend", "win free prize now"]})
    features = transform(raw)
    assert {"text_clean", "char_len", "target"} <= set(features.columns)
    assert features["target"].tolist() == [0, 1]

def test_model_pipeline_can_predict():
    texts = ["hello friend", "see you tomorrow", "win cash prize", "claim free offer"]
    labels = [0, 0, 1, 1]
    model = build_pipeline(MultinomialNB()).fit(texts, labels)
    assert model.predict(["claim free cash"]) [0] == 1
    metrics, _ = evaluate(model, pd.DataFrame({"text_clean": texts, "target": labels}))
    assert 0 <= metrics["accuracy"] <= 1
