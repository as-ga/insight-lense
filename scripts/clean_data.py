import argparse
import logging
from pathlib import Path
from typing import Tuple, Dict

import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "raw_data_dir": Path(__file__).parent / "data" / "raw",
    "processed_data_dir": Path(__file__).parent / "data" / "processed",
}


def load_csv_safe(filepath: Path) -> pd.DataFrame:
    """Load CSV with error handling."""
    try:
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        df = pd.read_csv(filepath)
        if df.empty:
            raise pd.errors.EmptyDataError(f"Empty CSV: {filepath}")
        logger.info(f"✓ Loaded {filepath.name}: {len(df)} rows")
        return df
    except FileNotFoundError as e:
        logger.error(f"✗ {e}")
        raise
    except pd.errors.EmptyDataError as e:
        logger.error(f"✗ {e}")
        raise


def clean_customers(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """Clean customers.csv."""
    logger.info("\n=== CLEANING CUSTOMERS ===")
    report = {
        "rows_before": len(df),
        "duplicates_removed": 0,
    }

    # Before stats
    before_stats = df.isna().sum()
    logger.info(f"Before: {len(df)} rows")
    logger.info(f"Null counts (before): {dict(before_stats)}")

    # 1. Remove duplicates by customer_id, keep most recent signup_date
    df["signup_date"] = pd.to_datetime(
        df["signup_date"], format="%Y-%m-%d", errors="coerce"
    )
    df_sorted = df.sort_values("signup_date", ascending=False, na_position="last")
    duplicates = len(df) - len(df_sorted)
    df = df_sorted.drop_duplicates(subset=["customer_id"], keep="first")
    report["duplicates_removed"] = duplicates
    logger.info(f"Removed {duplicates} duplicate rows")

    # 2. Standardize emails to lowercase
    df["email"] = df["email"].str.lower().str.strip()

    # 3. Flag invalid emails
    def is_valid_email(email):
        if pd.isna(email) or email == "":
            return False
        return "@" in email and "." in email

    df["is_valid_email"] = df["email"].apply(is_valid_email)
    invalid_count = (~df["is_valid_email"]).sum()
    logger.info(f"Flagged {invalid_count} invalid emails")

    # 4. Parse signup_date (already done above)
    unparseable = df["signup_date"].isna().sum()
    if unparseable > 0:
        logger.warning(f"⚠ {unparseable} unparseable signup_dates -> NaT")

    # 5. Strip whitespace from name and region
    df["name"] = df["name"].str.strip()
    df["region"] = df["region"].str.strip()

    # 6. Fill missing region with 'Unknown'
    df["region"] = df["region"].replace("", "Unknown")
    df["region"] = df["region"].fillna("Unknown")

    # After stats
    report["rows_after"] = len(df)
    after_stats = df.isna().sum()
    logger.info(f"After: {len(df)} rows")
    logger.info(f"Null counts (after): {dict(after_stats)}")

    return df, report


def clean_orders(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """Clean orders.csv."""
    logger.info("\n=== CLEANING ORDERS ===")
    report = {
        "rows_before": len(df),
        "rows_dropped": 0,
    }

    # Before stats
    before_stats = df.isna().sum()
    logger.info(f"Before: {len(df)} rows")
    logger.info(f"Null counts (before): {dict(before_stats)}")

    # 1. Parse order_date with multiple formats
    def parse_date(val):
        if pd.isna(val):
            return pd.NaT
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
            try:
                return pd.to_datetime(val, format=fmt)
            except (ValueError, TypeError):
                pass
        return pd.NaT

    df["order_date"] = df["order_date"].apply(parse_date)
    unparseable = df["order_date"].isna().sum()
    if unparseable > 0:
        logger.warning(f"⚠ {unparseable} unparseable order_dates -> NaT")

    # 2. Drop rows where both customer_id and order_id are null
    before_drop = len(df)
    df = df.dropna(subset=["customer_id", "order_id"], how="all")
    dropped = before_drop - len(df)
    report["rows_dropped"] = dropped
    if dropped > 0:
        logger.info(f"Dropped {dropped} rows with both customer_id and order_id null")

    # 3. Fill missing amount with median grouped by product
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    missing_before = df["amount"].isna().sum()
    df["amount"] = df.groupby("product")["amount"].transform(
        lambda x: x.fillna(x.median())
    )
    filled = missing_before - df["amount"].isna().sum()
    logger.info(f"Filled {filled} missing amounts with product median")

    # 4. Normalize status column
    status_map = {
        "done": "completed",
        "canceled": "cancelled",
        "pending": "pending",
        "completed": "completed",
        "refunded": "refunded",
        "cancelled": "cancelled",
    }
    df["status"] = df["status"].str.lower().str.strip().map(status_map)
    unmapped = df["status"].isna().sum()
    if unmapped > 0:
        logger.warning(f"⚠ {unmapped} status values could not be normalized")

    # 5. Add derived column order_year_month
    df["order_year_month"] = df["order_date"].dt.strftime("%Y-%m")

    # After stats
    report["rows_after"] = len(df)
    after_stats = df.isna().sum()
    logger.info(f"After: {len(df)} rows")
    logger.info(f"Null counts (after): {dict(after_stats)}")

    return df, report


def clean_products(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """Clean products.csv (minimal cleaning)."""
    logger.info("\n=== CLEANING PRODUCTS ===")
    report = {
        "rows_before": len(df),
        "rows_after": len(df),
    }

    before_stats = df.isna().sum()
    logger.info(f"Before: {len(df)} rows")
    logger.info(f"Null counts (before): {dict(before_stats)}")

    # Minimal cleaning - strip whitespace
    df["product_name"] = df["product_name"].str.strip()
    df["category"] = df["category"].str.strip()

    after_stats = df.isna().sum()
    logger.info(f"After: {len(df)} rows")
    logger.info(f"Null counts (after): {dict(after_stats)}")

    return df, report


def main(raw_dir: Path = None, processed_dir: Path = None):
    """Main cleaning pipeline."""
    raw_dir = raw_dir or CONFIG["raw_data_dir"]
    processed_dir = processed_dir or CONFIG["processed_data_dir"]

    processed_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 50)
    logger.info("DATA CLEANING PIPELINE")
    logger.info("=" * 50)

    # Load raw data
    customers_raw = load_csv_safe(raw_dir / "customers.csv")
    orders_raw = load_csv_safe(raw_dir / "orders.csv")
    products_raw = load_csv_safe(raw_dir / "products.csv")

    # Clean data
    customers_clean, customers_report = clean_customers(customers_raw)
    orders_clean, orders_report = clean_orders(orders_raw)
    products_clean, products_report = clean_products(products_raw)

    # Save cleaned data
    customers_clean.to_csv(processed_dir / "customers_clean.csv", index=False)
    orders_clean.to_csv(processed_dir / "orders_clean.csv", index=False)
    products_clean.to_csv(processed_dir / "products_clean.csv", index=False)
    logger.info(f"\n✓ Cleaned files saved to {processed_dir}")

    # Print summary report
    logger.info("\n" + "=" * 50)
    logger.info("CLEANING SUMMARY REPORT")
    logger.info("=" * 50)
    logger.info(
        f"Customers: {customers_report['rows_before']} → {customers_report['rows_after']} rows"
    )
    logger.info(f"  - Duplicates removed: {customers_report['duplicates_removed']}")
    logger.info(
        f"Orders: {orders_report['rows_before']} → {orders_report['rows_after']} rows"
    )
    logger.info(f"  - Rows dropped: {orders_report['rows_dropped']}")
    logger.info(
        f"Products: {products_report['rows_before']} → {products_report['rows_after']} rows"
    )
    logger.info("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean raw CSV data")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=CONFIG["raw_data_dir"],
        help="Path to raw data directory",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=CONFIG["processed_data_dir"],
        help="Path to processed data directory",
    )
    args = parser.parse_args()

    main(args.raw_dir, args.processed_dir)
