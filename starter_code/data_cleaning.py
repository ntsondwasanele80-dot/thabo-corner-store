"""
data_cleaning.py
-----------------
Task 2: Load the raw CSV files and clean them.

Cleaning decisions (also documented in README.md):
  * products.csv
      - Drop rows where unit_price or product_name is missing.
      - Normalise the "category" column to Title Case (e.g. "beverages"
        -> "Beverages").
      - Drop exact duplicate rows.
  * sales.csv
      - The raw file mixes four date formats:
          YYYY-MM-DD  (ISO, unambiguous)
          DD/MM/YYYY  (day-first)
          YYYY/MM/DD  (ISO with slashes)
          DD-MM-YYYY  (day-first)
        We standardise every date to ISO YYYY-MM-DD (sorts correctly,
        cannot be misread). Day-first is used for slash/dash formats
        because this is a South African store using dd/mm/yyyy.
      - Drop rows where sale_date, quantity or product_id is missing.
      - Fill missing payment_method with "Unknown" (do NOT drop the
        row — the sale still happened).
      - Drop rows whose product_id does not exist in products
        (referential integrity).
      - Drop exact duplicate rows.
"""

import pandas as pd


def load_raw_data(products_path: str, sales_path: str):
    """
    Load the two raw CSV files into pandas DataFrames.
    """
    products_df = pd.read_csv(products_path)
    sales_df = pd.read_csv(sales_path)

    return products_df, sales_df


def clean_products(products_df: "pd.DataFrame") -> "pd.DataFrame":
    """
    Clean the products DataFrame.
    """
    df = products_df.copy()

    # 1. Drop rows missing the fields we cannot invent.
    df = df.dropna(subset=["unit_price", "product_name"])

    # 2. Normalise inconsistent category capitalisation.
    df["category"] = df["category"].str.title()

    # 3. Drop exact duplicate rows (e.g. P003 appears twice).
    df = df.drop_duplicates()

    return df


def clean_sales(sales_df: "pd.DataFrame", valid_product_ids) -> "pd.DataFrame":
    """
    Clean the sales DataFrame.
    """
    df = sales_df.copy()

    # ---- 1. Parse dates by trying each known format in turn ---------
    def parse_date(value):
        if pd.isna(value):
            return pd.NaT
        value = str(value).strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                return pd.to_datetime(value, format=fmt)
            except (ValueError, TypeError):
                continue
        return pd.NaT  # genuinely unparseable

    df["sale_date"] = df["sale_date"].apply(parse_date)

    # ---- 2. Drop rows missing critical fields -----------------------
    df = df.dropna(subset=["sale_date", "quantity", "product_id"])

    # ---- 3. Standardise every date to ISO YYYY-MM-DD ----------------
    df["sale_date"] = df["sale_date"].dt.strftime("%Y-%m-%d")

    # ---- 4. Fill missing payment_method with "Unknown" --------------
    df["payment_method"] = df["payment_method"].fillna("Unknown")

    # ---- 5. Drop rows pointing at non-existent products -------------
    df = df[df["product_id"].isin(valid_product_ids)]

    # ---- 6. Drop exact duplicate rows -------------------------------
    df = df.drop_duplicates()

    return df


def cleaning_summary(
    raw_df: "pd.DataFrame",
    clean_df: "pd.DataFrame",
    name: str
) -> str:
    """
    Build a short summary of the cleaning.
    """
    removed = len(raw_df) - len(clean_df)

    return f"{name}: {len(raw_df)} raw rows -> {len(clean_df)} clean rows ({removed} removed)"