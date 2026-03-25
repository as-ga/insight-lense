import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
from faker import Faker

PROJECT_ROOT = Path(__file__).parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"

# Seed for reproducibility
random.seed(42)
fake = Faker()
Faker.seed(42)


def generate_customers(num_customers=1000):
    """Generate customers.csv with realistic data using Faker."""
    regions = ["North", "South", "East", "West", "Central"]
    customers = []

    for i in range(1, num_customers + 1):
        name = fake.name()
        email = fake.email()
        region = random.choice(regions)
        signup_date = fake.date_between(start_date="-2y", end_date="today")

        # Add some realistic data quality issues (10% error rate)
        if random.random() < 0.05:  # 5% missing email
            email = None
        elif random.random() < 0.05:  # 5% malformed email
            email = fake.word() + "@" + fake.word()

        if random.random() < 0.02:  # 2% missing region
            region = None

        customers.append((i, name, email, region, signup_date))

    with open(DATA_RAW / "customers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "name", "email", "region", "signup_date"])
        writer.writerows(customers)


def generate_orders(num_orders=5000, num_customers=1000):
    """Generate orders.csv with realistic data using Faker."""
    statuses = ["completed", "pending", "canceled", "refunded"]
    products_list = [
        ("Laptop", 1200),
        ("Mouse", 25),
        ("Keyboard", 75),
        ("Monitor", 400),
        ("Headphones", 150),
        ("USB Cable", 10),
        ("Charger", 35),
        ("Webcam", 60),
        ("SSD", 120),
        ("RAM", 80),
    ]

    orders = []
    for i in range(1, num_orders + 1):
        customer_id = random.randint(1, num_customers)
        product, base_price = random.choice(products_list)
        amount = base_price + random.randint(-10, 50)  # Slight price variation
        order_date = fake.date_between(start_date="-1y", end_date="today")
        status = random.choice(statuses)

        # Add some realistic data quality issues (5% error rate)
        if random.random() < 0.02:  # 2% missing amount
            amount = None
        if random.random() < 0.03:  # 3% missing customer_id
            customer_id = None

        orders.append((i, customer_id, product, amount, order_date, status))

    with open(DATA_RAW / "orders.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["order_id", "customer_id", "product", "amount", "order_date", "status"]
        )
        writer.writerows(orders)


def generate_products():
    """Generate products.csv."""
    products = [
        (1, "Laptop", "Electronics", 1200),
        (2, "Mouse", "Accessories", 25),
        (3, "Keyboard", "Accessories", 75),
        (4, "Monitor", "Electronics", 400),
        (5, "Headphones", "Audio", 150),
        (6, "USB Cable", "Accessories", 10),
        (7, "Charger", "Accessories", 35),
        (8, "Webcam", "Electronics", 60),
        (9, "SSD", "Storage", 120),
        (10, "RAM", "Memory", 80),
    ]

    with open(DATA_RAW / "products.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "product_name", "category", "unit_price"])
        writer.writerows(products)


if __name__ == "__main__":
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    # Generate datasets with configurable sizes
    num_customers = 1000
    num_orders = 5000

    print("Generating sample data...")
    generate_customers(num_customers)
    print(f"✓ Generated {num_customers} customers")

    generate_orders(num_orders, num_customers)
    print(f"✓ Generated {num_orders} orders")

    generate_products()
    print(f"✓ Generated products")

    print(f"✓ All CSVs generated in {DATA_RAW}")
