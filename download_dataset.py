# Kaggle Dataset Download Script
# Dataset: https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset

import os
from pathlib import Path

try:
    import kagglehub
except ImportError:
    print("Installing kagglehub...")
    os.system("pip install kagglehub")
    import kagglehub

# Download dataset
print("Downloading phishing email dataset from Kaggle...")
path = kagglehub.dataset_download("naserabdullahalam/phishing-email-dataset")
print(f"Dataset downloaded to: {path}")

# Find CSV file and copy to backend/data
import shutil

data_dir = Path("backend/data")
data_dir.mkdir(parents=True, exist_ok=True)

source_path = Path(path)
csv_files = list(source_path.glob("*.csv"))

if csv_files:
    source_file = csv_files[0]
    dest_file = data_dir / "phishing_emails.csv"
    shutil.copy(source_file, dest_file)
    print(f"Copied {source_file.name} to {dest_file}")
    print(f"\nDataset ready at: {dest_file}")
else:
    print("No CSV file found in downloaded dataset")
    print(f"Please manually copy CSV from: {path}")
