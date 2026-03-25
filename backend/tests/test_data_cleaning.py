import tempfile
from pathlib import Path

import pandas as pd
import pytest

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from clean_data import clean_customers, clean_orders, clean_products
from analyze import merge_data


class TestCustomersClean:
    """Test customer data cleaning."""

    def test_remove_duplicates(self):
        """Test that duplicates are removed based on customer_id."""
        data = {
            "customer_id": [1, 1, 2],
            "name": ["Alice", "Alice", "Bob"],
            "email": ["alice@example.com", "ALICE@EXAMPLE.COM", "bob@example.com"],
            "region": ["North", "North", "South"],
            "signup_date": ["2023-01-15", "2023-01-20", "2023-02-10"],
        }
        df = pd.DataFrame(data)
        cleaned, report = clean_customers(df)

        assert len(cleaned) == 2
        assert report["rows_before"] > report["rows_after"]

    def test_email_validation(self):
        """Test email validation."""
        data = {
            "customer_id": [1, 2, 3, 4],
            "name": ["Alice", "Bob", "Charlie", "Diana"],
            "email": ["alice@example.com", "bob@", "charlie", "diana@example.org"],
            "region": ["North", "South", "East", "West"],
            "signup_date": ["2023-01-15", "2023-02-10", "2023-03-05", "2023-04-01"],
        }
        df = pd.DataFrame(data)
        cleaned, _ = clean_customers(df)

        assert (
            bool(cleaned[cleaned["customer_id"] == 1]["is_valid_email"].values[0])
            is True
        )
        assert (
            bool(cleaned[cleaned["customer_id"] == 2]["is_valid_email"].values[0])
            is False
        )
        assert (
            bool(cleaned[cleaned["customer_id"] == 3]["is_valid_email"].values[0])
            is False
        )
        assert (
            bool(cleaned[cleaned["customer_id"] == 4]["is_valid_email"].values[0])
            is True
        )

    def test_region_fill_missing(self):
        """Test that missing regions are filled with 'Unknown'."""
        data = {
            "customer_id": [1, 2],
            "name": ["Alice", "Bob"],
            "email": ["alice@example.com", "bob@example.com"],
            "region": ["North", None],
            "signup_date": ["2023-01-15", "2023-02-10"],
        }
        df = pd.DataFrame(data)
        cleaned, _ = clean_customers(df)

        assert cleaned[cleaned["customer_id"] == 2]["region"].values[0] == "Unknown"

    def test_whitespace_stripped(self):
        """Test that whitespace is stripped from name and region."""
        data = {
            "customer_id": [1],
            "name": ["  Alice  "],
            "email": ["alice@example.com"],
            "region": ["  North  "],
            "signup_date": ["2023-01-15"],
        }
        df = pd.DataFrame(data)
        cleaned, _ = clean_customers(df)

        assert cleaned["name"].values[0] == "Alice"
        assert cleaned["region"].values[0] == "North"


class TestOrdersClean:
    """Test orders data cleaning."""

    def test_parse_multiple_date_formats(self):
        """Test date parsing with multiple formats."""
        data = {
            "order_id": [1, 2, 3, 4],
            "customer_id": [1, 2, 3, 4],
            "product": ["Laptop", "Mouse", "Keyboard", "Monitor"],
            "amount": [1200, 25, 75, 400],
            "order_date": ["2024-01-01", "01/01/2024", "01-02-2024", "invalid"],
            "status": ["completed", "pending", "completed", "completed"],
        }
        df = pd.DataFrame(data)
        cleaned, _ = clean_orders(df)

        assert pd.notna(cleaned.iloc[0]["order_date"])
        assert pd.notna(cleaned.iloc[1]["order_date"])
        assert pd.notna(cleaned.iloc[2]["order_date"])
        assert pd.isna(cleaned.iloc[3]["order_date"])

    def test_status_normalization(self):
        """Test that status values are normalized."""
        data = {
            "order_id": [1, 2, 3, 4],
            "customer_id": [1, 2, 3, 4],
            "product": ["Laptop", "Mouse", "Monitor", "Keyboard"],
            "amount": [1200, 25, 400, 75],
            "order_date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            "status": ["done", "canceled", "completed", "refunded"],
        }
        df = pd.DataFrame(data)
        cleaned, _ = clean_orders(df)

        assert cleaned[cleaned["order_id"] == 1]["status"].values[0] == "completed"
        assert cleaned[cleaned["order_id"] == 2]["status"].values[0] == "cancelled"
        assert cleaned[cleaned["order_id"] == 3]["status"].values[0] == "completed"
        assert cleaned[cleaned["order_id"] == 4]["status"].values[0] == "refunded"

    def test_derive_year_month(self):
        """Test that order_year_month is derived correctly."""
        data = {
            "order_id": [1, 2],
            "customer_id": [1, 2],
            "product": ["Laptop", "Mouse"],
            "amount": [1200, 25],
            "order_date": ["2024-01-15", "2024-03-20"],
            "status": ["completed", "pending"],
        }
        df = pd.DataFrame(data)
        cleaned, _ = clean_orders(df)

        assert cleaned.iloc[0]["order_year_month"] == "2024-01"
        assert cleaned.iloc[1]["order_year_month"] == "2024-03"

    def test_fill_missing_amount(self):
        """Test that missing amounts are filled with product median."""
        data = {
            "order_id": [1, 2, 3, 4],
            "customer_id": [1, 2, 1, 2],
            "product": ["Laptop", "Laptop", "Laptop", "Mouse"],
            "amount": [1200, None, 1200, 25],
            "order_date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            "status": ["completed", "completed", "completed", "pending"],
        }
        df = pd.DataFrame(data)
        cleaned, _ = clean_orders(df)

        assert cleaned.iloc[1]["amount"] == 1200  # Filled with Laptop median


class TestMerge:
    """Test data merging."""

    def test_left_join_customers_orders(self):
        """Test left join of orders and customers."""
        customers = pd.DataFrame(
            {
                "customer_id": [1, 2, 3],
                "name": ["Alice", "Bob", "Charlie"],
                "email": [
                    "alice@example.com",
                    "bob@example.com",
                    "charlie@example.com",
                ],
                "region": ["North", "South", "East"],
                "signup_date": ["2023-01-01", "2023-02-01", "2023-03-01"],
                "is_valid_email": [True, True, True],
            }
        )

        orders = pd.DataFrame(
            {
                "order_id": [1, 2, 3],
                "customer_id": [1, 2, 999],  # 999 doesn't exist in customers
                "product": ["Laptop", "Mouse", "Monitor"],
                "amount": [1200, 25, 400],
                "order_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "status": ["completed", "pending", "completed"],
                "order_year_month": ["2024-01", "2024-01", "2024-01"],
            }
        )

        products = pd.DataFrame(
            {
                "product_id": [1, 2, 3],
                "product_name": ["Laptop", "Mouse", "Monitor"],
                "category": ["Electronics", "Accessories", "Electronics"],
                "unit_price": [1200, 25, 400],
            }
        )

        merged = merge_data(customers, orders, products)

        assert len(merged) == 3
        assert merged[merged["customer_id"] == 999]["name"].isna().all()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
