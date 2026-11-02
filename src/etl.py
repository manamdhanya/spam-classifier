"""Extract, transform and load SMS messages into a simple feature store."""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from src.preprocess import clean_text

RAW_PATH = Path("datasets/spam.csv")
FEATURE_DIR = Path("feature_store")

def extract(path: Path = RAW_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            "Dataset missing. Run: python -m src.download_data"
        )

    df = pd.read_csv(
        path,
        header=None,
        names=["label", "text"],
        encoding="latin-1"
    )

    # Remove header if the dataset already contains one
    if str(df.iloc[0]["label"]).lower() in ["label", "v1"]:
        df = df.iloc[1:].reset_index(drop=True)

    df["label"] = df["label"].astype(str).str.lower().str.strip()
    return df

def validate(df: pd.DataFrame) -> None:
    if not {"label", "text"}.issubset(df.columns):
        raise ValueError("Input must contain label and text columns")
    labels = set(df["label"].dropna().astype(str).str.lower().unique())
    if not labels.issubset({"ham", "spam"}) or not labels:
        raise ValueError(f"Unexpected labels: {labels}")
    if df["text"].isna().any():
        raise ValueError("Null messages found")

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates().reset_index(drop=True)
    out = pd.DataFrame()
    out["text_clean"] = df["text"].apply(clean_text)
    out["char_len"] = df["text"].astype(str).str.len()
    out["word_count"] = df["text"].astype(str).str.split().str.len()
    out["digit_count"] = df["text"].astype(str).str.count(r"\d")
    out["exclaim_count"] = df["text"].astype(str).str.count("!")
    out["target"] = (df["label"].astype(str).str.lower() == "spam").astype(int)
    return out[out["text_clean"].str.len() > 0].reset_index(drop=True)

def load(features: pd.DataFrame, out_dir: Path = FEATURE_DIR):
    out_dir.mkdir(parents=True, exist_ok=True)
    train, test = train_test_split(
        features, test_size=0.2, random_state=42, stratify=features["target"]
    )
    train.to_csv(out_dir / "train_features.csv", index=False)
    test.to_csv(out_dir / "test_features.csv", index=False)
    return train, test

def run_etl():
    raw = extract()
    print("Raw data shape:", raw.shape)
    validate(raw)
    features = transform(raw)
    print("After cleaning:", features.shape)
    train, test = load(features)
    print("Train rows:", len(train), "| Test rows:", len(test))
    print("Features stored in:", FEATURE_DIR.resolve())
    return train, test

if __name__ == "__main__":
    run_etl()
