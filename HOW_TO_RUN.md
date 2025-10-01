# How to Run the Application

This guide shows you how to run the Customer Insight Platform in different modes.

---

## 🚀 Quick Start (Demo Mode - Recommended)

**Demo Mode** uses mock data and doesn't require Redis or Celery. Perfect for testing and demos!

### Windows - One Command to Start Everything:
```cmd
start-demo.bat
```

### What it does automatically:
1. ✅ Sets `DEMO_MODE=True` in `backend/.env`
2. ✅ Opens frontend in a new window (http://localhost:3000)
3. ✅ Starts backend server in the current window (http://127.0.0.1:8000)
4. ✅ Activates Python virtual environment

**That's it!** The frontend will automatically open in your browser, and both servers will be running!

---

## 🔧 Full Mode (Real Web Scraping)

**Full Mode** uses real web scraping with Celery background workers.

### Prerequisites:
1. **Redis** must be installed and running
   - Not installed? See **REDIS_SETUP.md** for installation guide
   - Quick install: `choco install redis-64`
   - Or use **Demo Mode** instead (no Redis needed)

### Windows - Mostly Automatic:

**Terminal 1 - Redis (start manually):**
```cmd
redis-server
```

**Terminal 2 - Everything Else (automatic):**
```cmd
start-full.bat
```

### What start-full.bat does automatically:
1. ✅ Checks if Redis is installed (stops if not)
2. ✅ Checks if Redis is running (stops if not)
3. ✅ Sets `DEMO_MODE=False` in `backend/.env`
4. ✅ Starts Celery worker in a new window
5. ✅ Opens frontend in a new window (http://localhost:3000)
6. ✅ Starts backend server in the current window (http://127.0.0.1:8000)

**Just run Redis first, then run start-full.bat - everything else is automatic!**

---

## 📝 What's the Difference?

| Feature | Demo Mode | Full Mode |
|---------|-----------|-----------|
| **Command** | `start-demo.bat` | `start-full.bat` |
| **Windows Opened** | 2 (backend + frontend) | 3 (backend + frontend + celery) |
| **Manual Steps** | 0 - Fully automatic! | 1 - Start Redis first |
| **Speed** | ~5 seconds | 30-60 seconds |
| **Data Source** | Mock data | Real web scraping |
| **Redis Required** | ❌ No | ✅ Yes (manual) |
| **Celery Worker** | ❌ No | ✅ Yes (automatic) |
| **Frontend** | ✅ Automatic | ✅ Automatic |
| **Setup Complexity** | Simple | Medium |
| **Use Case** | Testing, demos, development | Production |

## 🛑 How to Stop Everything

### Quick Stop:
```cmd
stop-all.bat
```

This stops all processes: backend, frontend, and Celery worker.

### Manual Stop:
- Close each terminal window
- Or press `Ctrl+C` in each window

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
- ❌ You had to start frontend in a separate terminal
- ❌ You had to start Celery in another terminal
- ❌ Easy to forget steps or make mistakes
- ❌ Required 3-4 terminals for full mode

### After (New Batch Files):
- ✅ `start-demo.bat` → One command, everything starts automatically (2 windows)
- ✅ `start-full.bat` → One command + Redis, everything else automatic (3 windows)
- ✅ `stop-all.bat` → Stop all processes instantly
- ✅ Automatic `DEMO_MODE` configuration
- ✅ Automatic Celery worker startup (full mode)
- ✅ Automatic frontend startup
- ✅ Clear status messages and checks

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

**"Error 10061 connecting to localhost:6379" or "Redis connection refused":**

This means Redis is not running! Here's what to do:

1. **Check if Redis is installed:**
   ```cmd
   where redis-server
   ```

2. **If not installed, install Redis:**
   - See **REDIS_SETUP.md** for detailed instructions
   - Quick install with Chocolatey: `choco install redis-64`
   - Or download from: https://github.com/microsoftarchive/redis/releases

3. **Start Redis:**
   ```cmd
   redis-server
   ```

4. **Test Redis connection:**
   ```cmd
   redis-cli ping
   ```
   Should respond with: `PONG`

5. **Alternative: Use Demo Mode** (no Redis needed):
   ```cmd
   start-demo.bat
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

### For Development & Testing:
```cmd
start-demo.bat
```
**One command** - Opens 2 windows, fully automatic, ready in seconds!

### For Testing Real Scraping:
```cmd
# Terminal 1:
redis-server

# Terminal 2:
start-full.bat
```
**Two commands** - Opens 3 windows, Celery & frontend automatic!

### When You're Done:
```cmd
stop-all.bat
```
**Stops everything** - Clean shutdown of all processes.

---

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

Now you can start **EVERYTHING** with just one command!

```cmd
# Demo Mode - Fully automatic (0 manual steps):
start-demo.bat

# Full Mode - Almost automatic (just start Redis first):
redis-server    # Terminal 1
start-full.bat  # Terminal 2

# Stop Everything:
stop-all.bat
```

**Windows will open automatically:**
- 💻 Backend (main window) - http://127.0.0.1:8000
- 🌐 Frontend (new window) - http://localhost:3000
- ⚙️ Celery Worker (new window, full mode only)

Happy coding! 🚀
