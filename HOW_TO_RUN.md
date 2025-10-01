# How to Run the Application

This guide shows you how to run the Customer Insight Platform in different modes.

---

## 🚀 Quick Start (Demo Mode - Recommended)

**Demo Mode** uses mock data and doesn't require Redis or Celery. Perfect for testing and demos!

### Windows:
```cmd
start-demo.bat
```

### What it does automatically:
1. ✅ Sets `DEMO_MODE=True` in `backend/.env`
2. ✅ Activates Python virtual environment
3. ✅ Starts backend server on http://127.0.0.1:8000

### Then start the frontend:
```cmd
cd frontend
npm start
```

Frontend will open at http://localhost:3000

---

## 🔧 Full Mode (Real Web Scraping)

**Full Mode** uses real web scraping with Celery background workers.

### Prerequisites:
1. **Redis** must be installed and running
2. **Celery worker** must be running

### Windows:

**Terminal 1 - Redis:**
```cmd
redis-server
```

**Terminal 2 - Backend:**
```cmd
start-full.bat
```
This automatically sets `DEMO_MODE=False` in `backend/.env`

**Terminal 3 - Celery Worker:**
```cmd
cd backend
venv\Scripts\activate
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

**Terminal 4 - Frontend:**
```cmd
cd frontend
npm start
```

---

## 📝 What's the Difference?

| Feature | Demo Mode | Full Mode |
|---------|-----------|-----------|
| **Speed** | ~5 seconds | 30-60 seconds |
| **Data Source** | Mock data | Real web scraping |
| **Redis Required** | ❌ No | ✅ Yes |
| **Celery Worker** | ❌ No | ✅ Yes |
| **Setup Complexity** | Simple | Complex |
| **Use Case** | Testing, demos, development | Production |

---

## 🔍 Where is the .env File?

The `.env` file is located at:
```
backend/.env
```

You can edit it manually, but the batch files now do this automatically! 🎉

### .env Configuration:

**For Demo Mode:**
```env
DEMO_MODE=True
```

**For Full Mode:**
```env
DEMO_MODE=False
REDIS_URL=redis://localhost:6379/0
```

---

## ✨ What Changed?

### Before (Old Batch Files):
- ❌ You had to manually edit `.env` file
- ❌ Easy to forget to change `DEMO_MODE`
- ❌ Confusing error messages

### After (New Batch Files):
- ✅ `start-demo.bat` automatically sets `DEMO_MODE=True`
- ✅ `start-full.bat` automatically sets `DEMO_MODE=False`
- ✅ `start-full.bat` checks if Redis is running
- ✅ Clear instructions and status messages

---

## 🐛 Troubleshooting

### Demo Mode Issues:

**"Module not found" errors:**
```cmd
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Port 8000 already in use:**
- Stop the other backend process
- Or change the port: `uvicorn app.main:app --reload --port 8001`

### Full Mode Issues:

**"Redis connection refused":**
```cmd
# Install Redis (if not installed):
# Download from: https://github.com/microsoftarchive/redis/releases

# Start Redis:
redis-server
```

**Celery worker not starting:**
```cmd
cd backend
venv\Scripts\activate
pip install celery redis
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

**"DEMO_MODE is still True":**
- The batch file automatically changes it, but you can verify:
```cmd
type backend\.env | findstr DEMO_MODE
```

---

## 🎯 Recommended Workflow

### For Development:
```cmd
start-demo.bat
```
Fast, simple, no Redis needed.

### For Testing Real Scraping:
```cmd
start-full.bat
```
Use when you need to test actual web scraping functionality.

### For Deployment:
- Use **Demo Mode** for free hosting (Render/Vercel)
- Use **Full Mode** for paid hosting with Redis

---

## 📚 More Documentation

- **DEPLOYMENT.md** - How to deploy to Render + Vercel
- **QUICK_START.md** - Complete setup from scratch
- **DEVELOPER_GUIDE.md** - Code structure and API docs

---

## 🎉 That's It!

Now you can easily switch between modes without manually editing files!

```cmd
start-demo.bat   # For quick testing (no Redis)
start-full.bat   # For real scraping (needs Redis)
```

Happy coding! 🚀
