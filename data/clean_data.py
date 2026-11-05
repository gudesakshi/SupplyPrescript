import json
from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent
SOURCE_PATH = DATA_DIR / "archive" / "DataCoSupplyChainDataset.csv"
OUTPUT_DIR = DATA_DIR / "processed"
CLEANED_PATH = OUTPUT_DIR / "cleaned_supply_chain.csv"
REPORT_PATH = OUTPUT_DIR / "cleaning_report.json"

DATE_COLUMNS = ["order date (DateOrders)", "shipping date (DateOrders)"]
NON_NEGATIVE_COLUMNS = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Order Item Quantity",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Sales per customer",
    "Sales",
    "Order Item Total",
    "Product Price",
]
DROP_REASONS = {
    "Product Description": "entirely empty in the source dataset",
    "Order Zipcode": "mostly missing and not needed for the planned analysis",
    "Customer Zipcode": "direct customer location identifier; use broader geography instead",
    "Customer Email": "personally identifying information not needed for analysis",
    "Customer Fname": "personally identifying information not needed for analysis",
    "Customer Lname": "personally identifying information not needed for analysis",
    "Customer Password": "sensitive information not needed for analysis",
    "Customer Street": "personally identifying information not needed for analysis",
    "Product Image": "image URL not needed for tabular analysis",
    "Product Status": "constant column with no variation in the source dataset",
}


def clean_dataset(source_path=SOURCE_PATH, cleaned_path=CLEANED_PATH, report_path=REPORT_PATH):
    """Clean the source data conservatively and save an analysis copy and report."""
    source_path = Path(source_path)
    cleaned_path = Path(cleaned_path)
    report_path = Path(report_path)

    if not source_path.is_file():
        raise FileNotFoundError(f"Source dataset not found: {source_path}")

    data = pd.read_csv(source_path, encoding="latin1")
    original_shape = data.shape
    original_missing = data.isna().sum()
    original_missing = {
        column: int(count)
        for column, count in original_missing.items()
        if count
    }

    required_columns = ["Order Item Id", *DATE_COLUMNS, *NON_NEGATIVE_COLUMNS]
    missing_required = [column for column in required_columns if column not in data]
    if missing_required:
        raise ValueError(f"Required columns are missing: {missing_required}")

    exact_duplicates = int(data.duplicated().sum())
    data = data.drop_duplicates().copy()

    if data["Order Item Id"].duplicated().any():
        raise ValueError("Order Item Id is not unique; inspect duplicate item records before cleaning.")

    removed_columns = {
        column: reason
        for column, reason in DROP_REASONS.items()
        if column in data.columns
    }
    if "Order Zipcode" in data.columns:
        missing_rate = data["Order Zipcode"].isna().mean() * 100
        removed_columns["Order Zipcode"] = (
            f"{missing_rate:.1f}% missing and not needed for the planned analysis"
        )
    data = data.drop(columns=list(removed_columns))

    trimmed_counts = {}
    text_columns = data.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        original_values = data[column]
        trimmed_values = original_values.str.strip()
        changed_count = int((original_values.notna() & original_values.ne(trimmed_values)).sum())
        if changed_count:
            trimmed_counts[column] = changed_count
        data[column] = trimmed_values.replace("", pd.NA)

    for column in DATE_COLUMNS:
        parsed_dates = pd.to_datetime(
            data[column],
            format="%m/%d/%Y %H:%M",
            errors="coerce",
        )
        invalid_count = int(parsed_dates.isna().sum())
        if invalid_count:
            raise ValueError(f"Could not parse {invalid_count} values in date column {column!r}.")
        data[column] = parsed_dates

    invalid_values = {}
    for column in NON_NEGATIVE_COLUMNS:
        invalid_count = int(data[column].lt(0).sum())
        if invalid_count:
            invalid_values[column] = invalid_count
    if invalid_values:
        raise ValueError(f"Negative values found in non-negative fields: {invalid_values}")

    remaining_missing = data.isna().sum()
    remaining_missing = {
        column: int(count)
        for column, count in remaining_missing.items()
        if count
    }
    if remaining_missing:
        raise ValueError(
            "Unexpected missing values remain after cleaning; review before imputing: "
            f"{remaining_missing}"
        )

    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(cleaned_path, index=False)

    report = {
        "source_file": str(source_path),
        "cleaned_file": str(cleaned_path),
        "source_shape": {"rows": int(original_shape[0]), "columns": int(original_shape[1])},
        "cleaned_shape": {"rows": int(data.shape[0]), "columns": int(data.shape[1])},
        "exact_duplicate_rows_removed": exact_duplicates,
        "duplicate_order_item_ids": 0,
        "missing_values_before": original_missing,
        "missing_values_after": 0,
        "removed_columns_and_reasons": removed_columns,
        "text_values_trimmed_by_column": trimmed_counts,
        "date_columns_converted": DATE_COLUMNS,
        "validation": "passed",
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Dataset cleaning completed.")
    print(f"Source shape: {original_shape[0]:,} rows x {original_shape[1]} columns")
    print(f"Cleaned shape: {data.shape[0]:,} rows x {data.shape[1]} columns")
    print(f"Exact duplicate rows removed: {exact_duplicates}")
    print(f"Columns removed: {len(removed_columns)}")
    print(f"Text columns trimmed: {len(trimmed_counts)}")
    print(f"Missing values after cleaning: {int(data.isna().sum().sum())}")
    print(f"Cleaned data: {cleaned_path}")
    print(f"Cleaning report: {report_path}")
    return data, report


if __name__ == "__main__":
    clean_dataset()