from pathlib import Path

import pandas as pd


base_dir = Path(__file__).resolve().parent
file_path = base_dir / "archive" / "DataCoSupplyChainDataset.csv"

print(f"Loading dataset from: {file_path}")

df = pd.read_csv(file_path, encoding="latin1")

print("\nDataset loaded successfully!")
print("Dataset shape:", df.shape)
print("\nColumns:")
print(list(df.columns))

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

print("\nDuplicate rows:", df.duplicated().sum())

print("\nSummary statistics:")
print(df.describe(include="all").T)

print("\nNumeric columns:")
print(df.select_dtypes(include="number").columns.tolist())

print("\nCategorical columns:")
print(df.select_dtypes(exclude="number").columns.tolist())

print("\nQuick insights:")
print(f"- Rows: {df.shape[0]}")
print(f"- Columns: {df.shape[1]}")
print(f"- Missing cells: {df.isnull().sum().sum()}")
print(f"- Duplicates: {df.duplicated().sum()}")