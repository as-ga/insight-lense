# Project Setup Guide

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)
- pnpm or npm
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/as-ga/insight-lense.git
cd insight-lense
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
pnpm install
```

### 4. Generate Sample Data

```bash
cd ../scripts
python generate_sample_data.py
```

## Running the Project

### Option 1: Full Stack (Recommended)

```bash
./run-full-stack.sh
```

This starts both services:
- 🔌 Backend: http://localhost:8000
- 🎨 Frontend: http://localhost:5173

### Option 2: Separate Terminals

**Terminal 1 - Backend:**
```bash
./backend/run.sh
```
Backend runs on `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm dev
```
Frontend runs on `http://localhost:5173`

### Option 3: Manual Backend Start

```bash
cd backend
export $(cat .env | grep -v '#' | xargs)
python -m uvicorn app.main:app --host $API_HOST --port $API_PORT --reload
```

## Environment Configuration

### Backend (.env)

The `backend/.env` file is automatically created with defaults:

```bash
FLASK_ENV=development
FLASK_DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGIN=http://localhost:5173
```

### Frontend (.env)

Create `frontend/.env`:

```bash
VITE_SERVER_URL=http://localhost:8000
```

## Data Processing Scripts

Located in `scripts/` directory:

- `generate_sample_data.py`: Generate 1000+ customers and orders
- `clean_data.py`: Data cleaning and validation
- `analyze.py`: Data analysis and insights

Run any script:
```bash
python scripts/<script_name>.py
```

## Building for Production

### Frontend Build

```bash
cd frontend
pnpm build
```

Output: `frontend/dist/`

### Backend Production

Use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app.main:app
```
