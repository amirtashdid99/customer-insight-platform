## Quick Start (Demo Mode)

The easiest way to get started:

### Option 1: Using Batch Scripts (Windows)

**Backend:**
```bash
# Double-click or run:
start-demo.bat
```

**Frontend** (in a new terminal):
```bash
cd frontend
npm start
```

### Option 2: Manual Commands

**Backend:**
```bash
cd backend
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac
python -m uvicorn app.main:app --reload
```

**Frontend** (new terminal):
```bash
cd frontend
npm install  # First time only
npm start
```

Visit: `http://localhost:3000`

---

## Full Mode Setup

For real web scraping with Celery workers:

1. **Edit `.env`**: Set `DEMO_MODE=False`
2. **Start Redis**: `redis-server` or `docker run -d -p 6379:6379 redis`
3. **Start Backend**: `cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload`
4. **Start Celery Worker**: `cd backend && venv\Scripts\activate && celery -A app.core.celery_app worker --loglevel=info --pool=solo`
5. **Start Frontend**: `cd frontend && npm start`

**See [RUNNING_MODES.md](./RUNNING_MODES.md) for detailed instructions**

---

## What's the Difference?

| Feature | Demo Mode | Full Mode |
|---------|-----------|-----------|
| Redis Required | ❌ No | ✅ Yes |
| Setup Complexity | Simple | Advanced |
| Data Source | Mock/Sample | Real Web Scraping |
| Response Time | ~5 seconds | ~30-90 seconds |
| Best For | Testing, Demos | Production Use |

---

## Troubleshooting

**Error: "Connection refused to localhost:6379"**
- You're trying to run Full Mode without Redis
- Solution: Either start Redis or switch to Demo Mode (set `DEMO_MODE=True` in `.env`)

**Backend won't start**
- Make sure you're in the `backend` directory
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

**Frontend can't connect**
- Make sure backend is running on `http://127.0.0.1:8000`
- Check browser console for errors
- Verify CORS settings in backend `.env`

For more help, see [RUNNING_MODES.md](./RUNNING_MODES.md)
