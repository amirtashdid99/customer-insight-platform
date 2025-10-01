# Free Demo Deployment Guide (Render)

This guide shows how to deploy the **demo version** to Render for free (uses mock data, no Redis needed).

## Why Demo Mode?

- **Free**: No Redis costs, single web service
- **Fast**: Analysis completes in ~5 seconds
- **Reliable**: No timeout issues
- **Perfect for Portfolio**: Shows off your project professionally

The GitHub version has full functionality (real scraping) when run locally.

---

## Step 1: Update Render Web Service

Since DigitalOcean payment isn't working, let's use Render:

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your repository: `customer-insight-platform`
4. Configure:
   - **Name**: `customer-insight-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   ```
   DATABASE_URL=sqlite:///./customer_insight.db
   SECRET_KEY=(generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
   ALLOWED_ORIGINS=https://customer-insight-platform.vercel.app
   DEMO_MODE=True
   REDIS_URL=redis://localhost:6379/0
   ```
   
   **Note**: Even in demo mode, set `REDIS_URL` (it won't be used but config expects it)

6. **Instance Type**: Free
7. Click **"Create Web Service"**

---

## Step 2: Wait for Deployment

Build takes ~5-10 minutes (PyTorch is large).

Check logs for:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

---

## Step 3: Update Vercel Frontend

1. Go to https://vercel.com/dashboard
2. Click your project → **Settings** → **Environment Variables**
3. Edit `REACT_APP_API_URL`:
   - Set to your Render URL (e.g., `https://customer-insight-backend.onrender.com`)
4. **Save**
5. Go to **Deployments** → Latest → **"..."** → **"Redeploy"**

---

## Step 4: Test Your Demo

1. Visit: https://customer-insight-platform.vercel.app/
2. Search for "iPhone 15" or any product
3. Analysis should complete in ~5-10 seconds
4. See results with sentiment analysis and charts

---

## Demo vs Full Version

### Demo Version (Online):
- ✅ Free hosting (Render + Vercel)
- ✅ Fast (~5 seconds)
- ✅ No Redis/Celery needed
- ✅ Perfect for portfolio
- ❌ Uses sample data (not real scraping)

### Full Version (Local):
- ✅ Real web scraping
- ✅ Actual customer reviews
- ✅ Complete ML pipeline
- ✅ Production-ready architecture
- ⚠️ Requires Redis + Celery
- ⚠️ Takes 30-90 seconds

---

## Switching Between Modes

### For Online Demo (Render):
```bash
# In Render environment variables:
DEMO_MODE=True
```

### For Local Development:
```bash
# In backend/.env:
DEMO_MODE=False

# Start Redis
redis-server

# Start Celery worker
celery -A worker.celery_app worker --loglevel=info

# Start API
uvicorn app.main:app --reload
```

---

## Troubleshooting

### Render Build Fails
- Check Python version is 3.9+
- Verify all packages in `requirements.txt` are compatible
- Check build logs for specific errors

### Frontend Can't Connect
- Verify `REACT_APP_API_URL` in Vercel matches your Render URL
- Check CORS: `ALLOWED_ORIGINS` in Render must include Vercel URL
- Test backend directly: `https://your-backend.onrender.com/health`

### Demo Mode Not Working
- Verify `DEMO_MODE=True` in Render environment variables
- Check application logs for errors
- Test API docs: `https://your-backend.onrender.com/docs`

---

## Cost

**Total: $0/month** (100% free tier)
- Render Web Service: Free (750 hours/month)
- Vercel Frontend: Free (100GB bandwidth/month)
- SQLite Database: Free (included)

**No credit card required!**

---

## Resume/Portfolio Tips

On your resume, you can describe this as:

> **Customer Insight Platform** | React, FastAPI, PyTorch, Celery  
> Full-stack ML application for customer sentiment analysis with async task processing  
> • Built production-ready REST API with FastAPI and background job queue (Celery)  
> • Implemented NLP sentiment analysis using transformer models (DistilBERT)  
> • Deployed scalable architecture with Redis message broker and worker services  
> • Live Demo: [customerinsight.vercel.app](https://customer-insight-platform.vercel.app)

**In interviews**, mention:
- Demo version uses mock data for reliability
- Full version (on GitHub) includes real web scraping with BeautifulSoup
- Chose Celery architecture to avoid timeout issues in production
- Could scale to handle 1000s of concurrent analyses with more workers

---

**Your GitHub shows the complete implementation. Your demo shows it works. Perfect combination! 🎉**
