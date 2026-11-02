"""Shared text normalization for training and inference."""
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

URL_RE = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
NON_ALNUM_RE = re.compile(r"[^a-z0-9\s]")

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = URL_RE.sub(" urltoken ", text)
    text = NON_ALNUM_RE.sub(" ", text)
    tokens = [token for token in text.split() if token not in ENGLISH_STOP_WORDS]
    return " ".join(tokens)
