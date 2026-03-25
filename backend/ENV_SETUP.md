# 🚀 Backend Environment Setup Guide

## 📝 Environment Variables

All configuration is done through environment variables in `.env` file.

### Available Variables

```bash
# Backend Configuration
FLASK_ENV=development          # development | production
FLASK_DEBUG=True              # True | False

# API Configuration
API_HOST=0.0.0.0              # Server host
API_PORT=8000                 # Server port

# CORS Configuration
CORS_ORIGIN=http://localhost:5173  # Frontend URL
```

## 🔧 Setup Steps

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `pandas` - Data processing
- `numpy` - Numerical computing
- `faker` - Sample data generation
- `python-dotenv` - Environment variable loading

### 2. Create `.env` File

```bash
# Copy from example
cp .env.example .env

# Edit if needed
nano .env
```

Default `.env`:
```bash
FLASK_ENV=development
FLASK_DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGIN=http://localhost:5173
```

### 3. Generate Sample Data

```bash
cd ../scripts
python generate_sample_data.py
```

## 🚀 Running the Backend

### Option 1: Direct Script (Recommended)

```bash
./backend/run.sh
```

This script:
- Loads `.env` file
- Reads `API_HOST` and `API_PORT` from environment
- Starts FastAPI with uvicorn

### Option 2: Manual Command

```bash
cd backend
export $(cat .env | grep -v '#' | xargs)
python -m uvicorn app.main:app --host $API_HOST --port $API_PORT --reload
```

### Option 3: Full Stack (Backend + Frontend)

```bash
./run-full-stack.sh
```

This starts both services:
- 🔌 Backend: http://localhost:8000
- 🎨 Frontend: http://localhost:5173

## 📊 Verify It's Running

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

### API Endpoints

- `GET /health` - Health check
- `GET /api/revenue` - Monthly revenue
- `GET /api/top-customers` - Top customers
- `GET /api/categories` - Category performance
- `GET /api/regions` - Regional analysis

## 🔌 Connection from Frontend

Update `frontend/.env`:

```bash
VITE_SERVER_URL=http://localhost:8000
```

## 🛠️ Configuration in Code

The `app/config.py` file reads all environment variables:

```python
from app.config import settings

print(settings.API_HOST)     # 0.0.0.0
print(settings.API_PORT)    # 8000
print(settings.ENVIRONMENT) # development
print(settings.DEBUG)       # True
```

## 🌍 Production Setup

For production, create `.env`:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGIN=https://yourdomain.com
```

Run with Gunicorn:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 📋 Troubleshooting

### Port Already in Use

Change `API_PORT` in `.env`:

```bash
API_PORT=9000
```

Then restart with `./backend/run.sh`

### Environment Variables Not Loading

Make sure `.env` exists in backend directory:

```bash
ls -la backend/.env
```

### Module Import Errors

Reinstall dependencies:

```bash
pip install -r requirements.txt --force-reinstall
```

## ✅ Summary

1. ✅ Install: `pip install -r requirements.txt`
2. ✅ Setup: `cp .env.example .env`
3. ✅ Run: `./backend/run.sh`
4. ✅ Test: `curl http://localhost:8000/health`

Done! 🎉
