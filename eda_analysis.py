from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "processed" / "cleaned_supply_chain.csv"
PLOT_PATH = ROOT / "eda_summary.png"


def main() -> None:
    df = pd.read_csv(CSV_PATH)

    print("Dataset shape:", df.shape)
    print(df.head())

    sales_by_category = df.groupby("Category Name")["Sales"].sum().sort_values(ascending=False)
    print("\nTop sales by category:")
    print(sales_by_category.head(10))

    profit_by_category = df.groupby("Category Name")["Benefit per order"].sum().sort_values(ascending=False)
    print("\nTop profit by category:")
    print(profit_by_category.head(10))

    shipping_mode = df["Shipping Mode"].value_counts()
    print("\nShipping mode counts:")
    print(shipping_mode)

    delivery_status = df["Delivery Status"].value_counts()
    print("\nDelivery status counts:")
    print(delivery_status)

    if "late_delivery" not in df.columns:
        df["late_delivery"] = df["Delivery Status"].str.contains("Late", case=False, na=False).astype(int)

    print("\nLate delivery rate:", df["late_delivery"].mean())

    plt.figure(figsize=(10, 5))
    sales_by_category.head(10).plot(kind="bar", title="Top 10 Sales by Category")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150, bbox_inches="tight")
    print(f"\nSaved summary chart to: {PLOT_PATH}")


if __name__ == "__main__":
    main()
