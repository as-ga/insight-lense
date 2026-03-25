# API Documentation

## Analytics Dashboard API

Base URL: `http://localhost:8000`

All endpoints return JSON responses.

### Health Check

**GET `/health`**
- Health check endpoint
- Response: `{"status": "ok"}`

### Revenue Endpoints

**GET `/api/revenue`**
- Returns monthly revenue trend data
- Response: Array of objects with `order_year_month` and `total_revenue`

### Customers Endpoints

**GET `/api/top-customers`**
- Returns top customers by spending
- Response: Array of customer objects with `name`, `region`, `total_spend`, `churned`

### Categories Endpoints

**GET `/api/categories`**
- Returns category performance data
- Response: Array of objects with `category` and `total_revenue`

### Regions Endpoints

**GET `/api/regions`**
- Returns regional analysis data
- Response: Array of objects with `region`, `num_customers`, `num_orders`, `total_revenue`, `avg_revenue_per_customer`

## Error Handling

- `400`: Bad Request
- `404`: Not Found (data file not found)
- `500`: Server Error

## Environment Variables

Configured in `backend/.env`:
- `API_HOST`: Server host (default: 0.0.0.0)
- `API_PORT`: Server port (default: 8000)
- `FLASK_ENV`: Development/Production (default: development)
- `FLASK_DEBUG`: Enable debug mode (default: True)
- `CORS_ORIGIN`: Frontend URL for CORS (default: http://localhost:5173)
