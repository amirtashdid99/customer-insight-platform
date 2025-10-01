# Running the Application - Demo vs Full Mode

This guide explains how to run the Customer Insight Platform in both modes.

---

## Quick Start (Demo Mode - Recommended for Testing)

Demo mode uses mock data and doesn't require Redis or Celery workers.

### 1. Backend Setup (Demo Mode)

```bash
cd backend

# Make sure .env has DEMO_MODE=True
# Open .env and verify: DEMO_MODE=True

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Start backend
python -m uvicorn app.main:app --reload
```

**Backend will run on**: `http://127.0.0.1:8000`

### 2. Frontend Setup

```bash
# Open a NEW terminal
cd frontend

# Start frontend
npm start
```

**Frontend will run on**: `http://localhost:3000`

### 3. Test It Out

Visit `http://localhost:3000` and try the example queries:
- iPhone 15
- Tesla Model 3
- Netflix
- PlayStation 5
- MacBook Pro

**Demo mode generates realistic mock data in ~5 seconds per query.**

---

## Full Mode (Real Web Scraping)

Full mode scrapes real web data using Celery background workers and Redis.

### Prerequisites

1. **Install Redis**:
   - **Windows**: Download from [https://github.com/tporadowski/redis/releases](https://github.com/tporadowski/redis/releases)
   - Extract and run `redis-server.exe`
   - Or use Docker: `docker run -d -p 6379:6379 redis`

2. **Verify Redis is running**:
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

### 1. Backend Setup (Full Mode)

#### Terminal 1: Start Redis
```bash
# If installed natively
redis-server

# Or with Docker
docker run -d -p 6379:6379 redis
```

#### Terminal 2: Start Backend API
```bash
cd backend

# Edit .env and set: DEMO_MODE=False
# Open .env and change: DEMO_MODE=False

# Activate virtual environment
.\venv\Scripts\activate

# Start backend
python -m uvicorn app.main:app --reload
```

**Backend API**: `http://127.0.0.1:8000`

#### Terminal 3: Start Celery Worker
```bash
cd backend

# Activate virtual environment
.\venv\Scripts\activate

# Start Celery worker
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

> **Note**: On Windows, use `--pool=solo`. On Linux/Mac, you can omit this flag.

### 2. Frontend Setup

#### Terminal 4: Start Frontend
```bash
cd frontend
npm start
```

**Frontend**: `http://localhost:3000`

---

## Comparison: Demo vs Full Mode

| Feature | Demo Mode | Full Mode |
|---------|-----------|-----------|
| **Redis Required** | ❌ No | ✅ Yes |
| **Celery Worker** | ❌ No | ✅ Yes |
| **Data Source** | Mock/Sample | Real Web Scraping |
| **Response Time** | ~5 seconds | ~30-90 seconds |
| **Setup Complexity** | Simple (1 terminal for backend) | Complex (3 terminals) |
| **Best For** | Quick demos, testing UI | Production, real insights |

---

## Troubleshooting

### Error: "Connection refused to localhost:6379"

**Problem**: Redis is not running.

**Solution**: 
- If in **Demo Mode**: Change `.env` to `DEMO_MODE=True`
- If in **Full Mode**: Start Redis server first

### Error: "No module named 'celery'"

**Problem**: Celery not installed.

**Solution**:
```bash
cd backend
.\venv\Scripts\activate
pip install celery redis
```

### Error: "No module named 'app'"

**Problem**: Running from wrong directory.

**Solution**: Make sure you're in the `backend` directory when starting the server.

### Frontend Can't Connect to Backend

**Problem**: Backend not running or wrong URL.

**Solution**:
1. Verify backend is running on `http://127.0.0.1:8000`
2. Check `frontend/src/services/api.ts` has correct base URL
3. Check CORS settings in `backend/.env`

---

## Development Workflow

### For Quick Testing (Demo Mode)
```bash
# Terminal 1: Backend
cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm start
```

### For Full Testing (Production-like)
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Backend API
cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload

# Terminal 3: Celery Worker
cd backend && .\venv\Scripts\activate && celery -A app.core.celery_app worker --loglevel=info --pool=solo

# Terminal 4: Frontend
cd frontend && npm start
```

---

## Environment Variables Quick Reference

**Backend `.env` file:**

```bash
# For Demo Mode (no Redis needed)
DEMO_MODE=True
REDIS_URL=redis://localhost:6379/0  # Not used in demo mode

# For Full Mode (Redis required)
DEMO_MODE=False
REDIS_URL=redis://localhost:6379/0  # Must be running

# Always required
DATABASE_URL=sqlite:///./customer_insight.db
SECRET_KEY=your-secret-key-min-32-chars
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## API Endpoints

- **Health Check**: `GET http://127.0.0.1:8000/`
- **API Docs**: `http://127.0.0.1:8000/docs`
- **Start Analysis**: `POST http://127.0.0.1:8000/api/analysis/analyze`
- **Check Status**: `GET http://127.0.0.1:8000/api/analysis/status/{job_id}`
- **Get Results**: `GET http://127.0.0.1:8000/api/analysis/results/{analysis_id}`

---

## Tips

1. **Always start with Demo Mode** to test if everything works
2. **Use Full Mode only** when you need real data for production
3. **Check logs** in terminals if something goes wrong
4. **Redis port 6379** must be free (no other services using it)
5. **Don't commit `.env` file** - it's in `.gitignore`

---

For deployment instructions, see:
- `DEMO_DEPLOYMENT.md` - Deploy demo mode to Render (free)
- `CELERY_DEPLOYMENT.md` - Deploy full mode with Redis + Celery workers
