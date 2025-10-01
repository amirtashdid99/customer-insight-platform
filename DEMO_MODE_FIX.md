# Demo Mode Fix - No Redis Required

## Problem
The application was trying to connect to Redis even in Demo Mode, causing the error:
```
Error 10061 connecting to localhost:6379. No connection could be made because the target machine actively refused it.
```

## Root Cause
The `analysis.py` API endpoint was always calling `run_analysis_task.delay()` which uses Celery to queue tasks to Redis, regardless of the `DEMO_MODE` setting.

## Solution Applied

### 1. Modified `app/api/analysis.py`
**Added conditional logic** to check `settings.DEMO_MODE`:

- **If `DEMO_MODE=True`**: Runs analysis synchronously without Celery/Redis
  - Uses `asyncio.create_task()` to run in background
  - Calls new `run_analysis_sync()` function
  - Estimated time: 5 seconds
  
- **If `DEMO_MODE=False`**: Uses Celery worker (requires Redis)
  - Calls `run_analysis_task.delay()` as before
  - Estimated time: 90 seconds

### 2. Created `run_analysis_sync()` in `app/tasks/analysis_tasks.py`
**New synchronous function** that:
- Works without Celery infrastructure
- Generates realistic mock data (15-25 comments)
- Runs sentiment analysis with ML models
- Extracts topics and predicts churn
- Saves results to database
- Completes in ~5 seconds

### 3. Added `ScrapedComment` schema in `app/models/schemas.py`
**Missing schema** needed for demo data generation:
```python
class ScrapedComment(BaseModel):
    text: str
    source: str
    source_url: str
    author: str
    posted_at: datetime
```

## Current Configuration

### `.env` file (Demo Mode)
```bash
DEMO_MODE=True  # ✅ No Redis needed
DATABASE_URL=sqlite:///./customer_insight.db
SECRET_KEY=your-secret-key-min-32-chars-long-string
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## How It Works Now

### Demo Mode (DEMO_MODE=True)
1. User clicks "Analyze" button on frontend
2. Frontend sends POST request to `/api/analysis/analyze`
3. Backend creates analysis record in database
4. Backend runs `run_analysis_sync()` in background thread
5. Function generates 15-25 mock comments with realistic text
6. Runs actual ML models (sentiment analysis, churn prediction)
7. Saves results to database
8. Frontend polls `/api/analysis/status/{id}` every 2 seconds
9. When complete, frontend fetches results and displays dashboard
10. **Total time: ~5 seconds**

### Full Mode (DEMO_MODE=False)
1. Same steps 1-3
2. Backend calls `run_analysis_task.delay()` → queues to Redis
3. Celery worker picks up task from Redis queue
4. Worker scrapes real web data from multiple sources
5. Runs ML analysis on real data
6. Saves results to database
7. Frontend polls and displays results
8. **Total time: ~30-90 seconds**
9. **Requires**: Redis server + Celery worker running

## Testing

### Start Backend (Demo Mode)
```bash
# Option 1: Batch script
.\start-demo.bat

# Option 2: Manual
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

### Start Frontend
```bash
cd frontend
npm start
```

### Test on Browser
1. Visit `http://localhost:3000`
2. Try example queries (iPhone 15, Tesla Model 3, etc.)
3. Should complete in ~5 seconds with mock data
4. **No Redis errors!** ✅

## Benefits of This Fix

✅ **No Redis dependency** in Demo Mode  
✅ **Faster setup** - just backend + frontend (2 terminals)  
✅ **Same ML models** - still uses real sentiment analysis and churn prediction  
✅ **Realistic data** - mock comments look authentic  
✅ **Easy deployment** - can deploy demo to free hosting (Render, Railway, etc.)  
✅ **Backward compatible** - Full mode still works with Redis when needed  

## Commits Applied

1. `635d44a` - Fix demo mode to work without Redis - add synchronous analysis
2. `3be489e` - Add ScrapedComment schema for demo mode

## Files Modified

- `backend/app/api/analysis.py` - Added DEMO_MODE check and conditional execution
- `backend/app/tasks/analysis_tasks.py` - Added `run_analysis_sync()` function
- `backend/app/models/schemas.py` - Added `ScrapedComment` class
- `backend/.env` - Set `DEMO_MODE=True` and added Redis URL

## Next Steps

1. ✅ Backend running on `http://127.0.0.1:8000`
2. 🔄 Start frontend: `cd frontend && npm start`
3. 🎯 Test at `http://localhost:3000`
4. 🚀 Deploy demo to Render/Vercel (see `DEMO_DEPLOYMENT.md`)

---

**Status**: ✅ FIXED - Demo mode now works without Redis!
