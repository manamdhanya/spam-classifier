"""Download the UCI SMS Spam Collection dataset."""
from pathlib import Path
import urllib.request
import zipfile

DATA_DIR = Path("datasets")
ZIP_PATH = DATA_DIR / "sms-spam-collection.zip"
CSV_PATH = DATA_DIR / "spam.csv"
DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if CSV_PATH.exists():
        print(f"Dataset already exists: {CSV_PATH}")
        return
    print("Downloading UCI SMS Spam Collection...")
    urllib.request.urlretrieve(DATA_URL, ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH) as archive:
        member = next((n for n in archive.namelist() if n.endswith("SMSSpamCollection")), None)
        if member is None:
            raise FileNotFoundError("SMSSpamCollection not found in downloaded archive")
        with archive.open(member) as source, CSV_PATH.open("w", encoding="utf-8") as target:
            for raw in source:
                decoded = raw.decode("utf-8", errors="replace").rstrip("\n")
                label, _, message = decoded.partition("\t")
                target.write(f'"{label}","{message.replace(chr(34), chr(34)*2)}"\n')
    ZIP_PATH.unlink(missing_ok=True)
    print(f"Saved dataset to {CSV_PATH}")

if __name__ == "__main__":
    main()
