# Celery + Redis Deployment Guide

## Architecture

This application now uses **production-ready background task processing**:

- **FastAPI Web Service**: Handles HTTP requests, returns immediately with job ID
- **Celery Worker**: Processes long-running analysis tasks in the background
- **Redis**: Message queue/broker between web service and workers
- **PostgreSQL/SQLite**: Stores analysis results

## Local Development

### 1. Install Redis

**Windows:**
```powershell
# Using Chocolatey
choco install redis-64

# Or download from: https://github.com/microsoftarchive/redis/releases
```

**Mac:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

### 2. Start Services

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - FastAPI Web:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

**Terminal 3 - Celery Worker:**
```bash
cd backend
source venv/bin/activate
celery -A worker.celery_app worker --loglevel=info
```

**Terminal 4 - Frontend:**
```bash
cd frontend
npm start
```

## Render Deployment

### Option A: Using render.yaml (Recommended)

1. **Push to GitHub:**
```bash
git add .
git commit -m "Add Celery + Redis background processing"
git push origin main
```

2. **Create Blueprint on Render:**
   - Go to https://dashboard.render.com/
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and create:
     - Web Service (FastAPI)
     - Background Worker (Celery)
     - Redis instance

3. **Set Environment Variables:**
   - `DATABASE_URL`: `sqlite:///./customer_insight.db` (or your PostgreSQL URL)
   - `SECRET_KEY`: (auto-generated or use your own)
   - `ALLOWED_ORIGINS`: Your Vercel frontend URL
   - `REDIS_URL`: (auto-linked from Redis service)

### Option B: Manual Setup

#### 1. Create Redis Instance
- Dashboard → New → Redis
- Name: `customer-insight-redis`
- Plan: Free
- Click "Create Redis"
- **Copy the Internal Redis URL**

#### 2. Create Web Service
- Dashboard → New → Web Service
- Connect repository
- Name: `customer-insight-api`
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  - `DATABASE_URL` = `sqlite:///./customer_insight.db`
  - `SECRET_KEY` = (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
  - `ALLOWED_ORIGINS` = Your Vercel URL
  - `REDIS_URL` = (paste Internal Redis URL from step 1)

#### 3. Create Background Worker
- Dashboard → New → Background Worker
- Connect same repository
- Name: `customer-insight-worker`
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `celery -A worker.celery_app worker --loglevel=info --concurrency=2`
- Environment Variables: (same as Web Service)
  - `DATABASE_URL` = (same)
  - `SECRET_KEY` = (same)
  - `REDIS_URL` = (same Internal Redis URL)

## Verifying Deployment

### Check Web Service
```bash
curl https://your-api.onrender.com/health
# Should return: {"status": "healthy", "database": "connected"}
```

### Check Celery Worker Logs
- Go to Render Dashboard → Background Worker → Logs
- You should see:
```
[INFO/MainProcess] Connected to redis://...
[INFO/MainProcess] celery@hostname ready
```

### Test Analysis Flow
1. Visit your Vercel frontend
2. Search for "iPhone 17"
3. Backend should:
   - Return immediately with job ID (< 1 second)
   - Worker processes in background (30-90 seconds)
   - Frontend polls for status updates
   - Results display when complete

## Troubleshooting

### Worker not processing tasks
```bash
# Check Redis connection
redis-cli ping
# Should return: PONG

# Check Celery can connect
celery -A worker.celery_app inspect ping
```

### Tasks failing
- Check worker logs on Render
- Verify `REDIS_URL` is set correctly on both web and worker
- Ensure database is accessible from worker

### Frontend timeout
- Increase `maxAttempts` in `App.tsx` (currently 60 = 2 minutes)
- Check worker logs for actual task duration

## Architecture Benefits

✅ **No Timeouts**: Workers run independently, not tied to HTTP request lifecycle  
✅ **Scalable**: Can run multiple workers to process tasks in parallel  
✅ **Reliable**: Tasks persist in Redis queue even if worker restarts  
✅ **Monitorable**: Celery Flower dashboard available for monitoring  
✅ **Production-Ready**: Standard architecture used by companies worldwide  

## Cost

- Render Free Tier:
  - ✅ Web Service: Free (750 hours/month)
  - ✅ Background Worker: Free (750 hours/month)
  - ✅ Redis: Free (25MB storage, enough for queue)
- Total: **$0/month** for portfolio project

## Future Enhancements

- Add Celery Beat for scheduled tasks (e.g., daily analysis updates)
- Implement task result caching
- Add Flower dashboard for monitoring: `celery -A worker.celery_app flower`
- Use PostgreSQL instead of SQLite for better concurrency
- Add task retries with exponential backoff
