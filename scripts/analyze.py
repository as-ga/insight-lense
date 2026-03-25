import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
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
        return df
    except FileNotFoundError as e:
        logger.error(f"✗ {e}")
        raise
    except pd.errors.EmptyDataError as e:
        logger.error(f"✗ {e}")
        raise


def merge_data(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Merge cleaned datasets."""
    logger.info("\n=== MERGING DATA ===")

    # Left-join orders onto customers
    orders_with_customers = pd.merge(orders, customers, on="customer_id", how="left")
    logger.info(
        f"Orders without matching customer: {orders_with_customers['customer_id'].isna().sum()}"
    )

    # Left-join products onto merged data (match orders.product to products.product_name)
    full_data = pd.merge(
        orders_with_customers,
        products,
        left_on="product",
        right_on="product_name",
        how="left",
    )
    logger.info(
        f"Order rows without matching product: {full_data['category'].isna().sum()}"
    )

    return full_data


def analyze_monthly_revenue(full_data: pd.DataFrame, processed_dir: Path):
    """Compute total revenue by month (completed orders only)."""
    logger.info("\n=== ANALYZING: Monthly Revenue Trend ===")

    df = full_data[full_data["status"] == "completed"].copy()
    monthly_revenue = (
        df.groupby("order_year_month")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_revenue"})
        .sort_values("order_year_month")
    )

    monthly_revenue.to_csv(processed_dir / "monthly_revenue.csv", index=False)
    logger.info(f"✓ Saved: monthly_revenue.csv ({len(monthly_revenue)} months)")
    return monthly_revenue


def analyze_top_customers(full_data: pd.DataFrame, processed_dir: Path):
    """Identify top 10 customers by total spend (completed orders)."""
    logger.info("\n=== ANALYZING: Top Customers ===")

    df = full_data[full_data["status"] == "completed"].copy()
    top_customers = (
        df.groupby("customer_id")
        .agg(
            {
                "name": "first",
                "region": "first",
                "amount": "sum",
            }
        )
        .rename(columns={"amount": "total_spend"})
        .sort_values("total_spend", ascending=False)
        .head(10)
        .reset_index()
    )

    top_customers.to_csv(processed_dir / "top_customers.csv", index=False)
    logger.info(f"✓ Saved: top_customers.csv")
    return top_customers


def analyze_category_performance(full_data: pd.DataFrame, processed_dir: Path):
    """Compute category performance: revenue, avg order value, order count."""
    logger.info("\n=== ANALYZING: Category Performance ===")

    df = full_data[full_data["status"] == "completed"].copy()
    category_perf = (
        df.groupby("category")
        .agg(
            {
                "amount": ["sum", "mean", "count"],
            }
        )
        .reset_index()
    )
    category_perf.columns = [
        "category",
        "total_revenue",
        "avg_order_value",
        "number_of_orders",
    ]
    category_perf = category_perf.sort_values("total_revenue", ascending=False)

    category_perf.to_csv(processed_dir / "category_performance.csv", index=False)
    logger.info(f"✓ Saved: category_performance.csv ({len(category_perf)} categories)")
    return category_perf


def analyze_regional_performance(full_data: pd.DataFrame, processed_dir: Path):
    """Compute regional analysis: customer count, order count, revenue, avg revenue per customer."""
    logger.info("\n=== ANALYZING: Regional Performance ===")

    df = full_data[full_data["status"] == "completed"].copy()

    regional = (
        df.groupby("region")
        .agg(
            {
                "customer_id": "nunique",
                "order_id": "count",
                "amount": "sum",
            }
        )
        .reset_index()
    )
    regional.columns = ["region", "num_customers", "num_orders", "total_revenue"]
    regional["avg_revenue_per_customer"] = (
        regional["total_revenue"] / regional["num_customers"]
    )
    regional = regional.sort_values("total_revenue", ascending=False)

    regional.to_csv(processed_dir / "regional_analysis.csv", index=False)
    logger.info(f"✓ Saved: regional_analysis.csv ({len(regional)} regions)")
    return regional


def analyze_churn(
    full_data: pd.DataFrame,
    top_customers: pd.DataFrame,
    processed_dir: Path,
):
    """Flag customers with no completed orders in past 90 days as churned."""
    logger.info("\n=== ANALYZING: Customer Churn ===")

    # Find latest date in dataset
    latest_date = pd.to_datetime(full_data["order_date"]).max()
    cutoff_date = latest_date - timedelta(days=90)
    logger.info(
        f"Latest date: {latest_date.date()}, Cutoff (90 days): {cutoff_date.date()}"
    )

    # Find customers with completed orders in past 90 days
    recent_orders = full_data[
        (full_data["status"] == "completed")
        & (pd.to_datetime(full_data["order_date"]) >= cutoff_date)
    ]["customer_id"].unique()

    # Mark churned in top_customers
    top_customers["churned"] = ~top_customers["customer_id"].isin(recent_orders)
    churned_count = top_customers["churned"].sum()
    logger.info(f"Customers flagged as churned: {churned_count}")

    top_customers.to_csv(processed_dir / "top_customers.csv", index=False)
    return top_customers


def main(processed_dir: Path = None):
    """Main analysis pipeline."""
    processed_dir = processed_dir or CONFIG["processed_data_dir"]
    processed_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 50)
    logger.info("DATA ANALYSIS PIPELINE")
    logger.info("=" * 50)

    # Load cleaned data
    logger.info("\nLoading cleaned data...")
    customers = load_csv_safe(processed_dir / "customers_clean.csv")
    orders = load_csv_safe(processed_dir / "orders_clean.csv")
    products = load_csv_safe(processed_dir / "products_clean.csv")

    # Convert date columns
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    customers["signup_date"] = pd.to_datetime(customers["signup_date"])

    # Merge datasets
    full_data = merge_data(customers, orders, products)

    # Run all analyses
    monthly_revenue = analyze_monthly_revenue(full_data, processed_dir)
    top_customers = analyze_top_customers(full_data, processed_dir)
    category_perf = analyze_category_performance(full_data, processed_dir)
    regional_perf = analyze_regional_performance(full_data, processed_dir)

    # Add churn analysis to top_customers
    top_customers = analyze_churn(full_data, top_customers, processed_dir)

    # Print summary
    logger.info("\n" + "=" * 50)
    logger.info("ANALYSIS SUMMARY")
    logger.info("=" * 50)
    logger.info(f"✓ All analysis outputs saved to {processed_dir}")
    logger.info("  - monthly_revenue.csv")
    logger.info("  - top_customers.csv (with churn flag)")
    logger.info("  - category_performance.csv")
    logger.info("  - regional_analysis.csv")
    logger.info("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze cleaned data")
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=CONFIG["processed_data_dir"],
        help="Path to processed data directory",
    )
    args = parser.parse_args()

    main(args.processed_dir)
