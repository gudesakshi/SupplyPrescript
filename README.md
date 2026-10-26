# Supply Prescript

## Overview
Supply Prescript is a supply chain analytics project focused on exploring order, shipping, product, and customer data to understand operational performance and identify patterns in delivery and fulfillment processes.

## Objective
The goal of this project is to inspect the dataset, clean and preprocess the data, analyze the key variables, and prepare the project for deeper business analysis and predictive modeling.

## Dataset
This project uses the DataCo Supply Chain Dataset stored in the `data/archive` folder.

The dataset includes information related to:
- orders and order status
- shipping modes and delivery timelines
- product categories and product attributes
- customer and regional information
- sales, profit, and order metrics

## Current Status
- Dataset has been loaded and inspected successfully
- Column types and schema have been reviewed
- Missing values and duplicate checks are in progress
- Data cleaning and preprocessing are the next steps

## Setup
Install the required Python libraries:

```bash
python -m pip install pandas numpy matplotlib seaborn
```

## Run the dataset inspection

```bash
python data/check_dataset.py
```

## Project Structure

```text
SupplyPrescript/
├── data/
│   ├── archive/
│   │   ├── DataCoSupplyChainDataset.csv
│   │   ├── DescriptionDataCoSupplyChain.csv
│   │   └── tokenized_access_logs.csv
│   └── check_dataset.py
├── .gitignore
├── README.md
└── .git/
```

## Workflow
1. Load and inspect the dataset
2. Clean missing values and duplicates
3. Convert and validate datatypes
4. Explore key trends and relationships
5. Perform feature engineering and analysis
6. Build predictive or decision-support models as needed

## Notes
This project is intended for exploratory analysis and may be extended with feature engineering, business insights, and predictive modeling based on the supply chain data.

