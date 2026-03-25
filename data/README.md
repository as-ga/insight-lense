# Data README

## Directory Structure

### raw/
Original CSV files imported into the system:
- `customers.csv` - Customer data (1000+ records)
- `orders.csv` - Transaction data (5000+ records)
- `products.csv` - Product catalog (10+ items)

### processed/
Cleaned and aggregated data for frontend consumption:
- `customers_clean.csv` - Cleaned customer records
- `orders_clean.csv` - Cleaned transaction records
- `products_clean.csv` - Cleaned product data
- `monthly_revenue.csv` - Aggregated monthly revenue
- `top_customers.csv` - Top 10 customers by spend
- `category_performance.csv` - Revenue by category
- `regional_analysis.csv` - Regional metrics

## Data Generation

To generate fresh sample data:

```bash
python scripts/generate_sample_data.py
```

This will create realistic data using the Faker library with:
- Random customer names and emails
- Random product selections
- Random order dates within last 12 months
- ~5% realistic data quality issues

## Data Processing

To clean and process raw data:

```bash
python scripts/clean_data.py
python scripts/analyze.py
```

## Data Schema

### customers.csv
```
customer_id, name, email, region
```

### orders.csv
```
order_id, customer_id, product_id, order_date, amount
```

### products.csv
```
product_id, product_name, category, price
```
