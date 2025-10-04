# 🚀 Deployment Guide

## Quick Deployment Options

### Option 1: Local Development (Recommended for Testing)

**What this means:** Run the application on your own computer for development and testing.

#### Steps:

1. **Install Prerequisites**
   ```bash
   # Check Python version (need 3.9+)
   python --version
   
   # Check Node.js version (need 16+)
   node --version
   ```

2. **Run Demo Mode (Easiest)**
   ```bash
   # Double-click this file:
   start-demo.bat
   
   # Or in terminal:
   cd backend
   python -m uvicorn app.main:app --reload
   
   # In another terminal:
   cd frontend
   npm start
   ```

3. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

**What happens locally:**
- Backend runs on your computer (port 8000)
- Frontend runs on your computer (port 3000)
- Database is SQLite file (no PostgreSQL needed)
- ML models load on first use
- No cloud services needed
- Free and fast for development

---

### Option 2: Cloud Deployment (Render + Vercel) - Current Setup

**What this means:** Your app runs on internet servers, accessible from anywhere.

#### Backend on Render (Already Deployed)

**What Render does:**
- Hosts the Python FastAPI backend
- Provides a public URL (https://customer-insight-platform-4rgb.onrender.com)
- Auto-deploys when you push to GitHub
- Free tier: 512MB RAM, sleeps after 15min inactivity

**How it works:**
1. You push code to GitHub
2. Render detects the push
3. Render automatically builds and deploys
4. App is live in 5-10 minutes

**Manual deployment (if needed):**
1. Go to https://dashboard.render.com
2. Click your service "customer-insight-platform-4rgb"
3. Click "Manual Deploy" → "Deploy latest commit"
4. Wait 5-10 minutes

**Environment variables (already set):**
```
DATABASE_URL=sqlite:///./customer_insight.db
DEMO_MODE=True
SECRET_KEY=<your-secret>
ALLOWED_ORIGINS=https://customer-insight-platform.vercel.app,http://localhost:3000
```

#### Frontend on Vercel (Already Deployed)

**What Vercel does:**
- Hosts the React frontend
- Provides a public URL (https://customer-insight-platform.vercel.app)
- Auto-deploys when you push to GitHub
- Free tier: unlimited bandwidth

**How it works:**
1. You push code to GitHub
2. Vercel detects the push
3. Vercel builds and deploys
4. App is live in 2-3 minutes

**Manual deployment (if needed):**
1. Go to https://vercel.com/dashboard
2. Click your project "customer-insight-platform"
3. Go to "Deployments" tab
4. Click "..." → "Redeploy"

**Environment variables (already set):**
```
REACT_APP_API_URL=https://customer-insight-platform-4rgb.onrender.com
```

---

### Option 3: AWS Cloud (Advanced - For Production Scale)

**What this means:** Deploy to Amazon Web Services for enterprise-grade hosting.

**Why use AWS:**
- Better performance (no sleep on free tier)
- More scalable (handles thousands of users)
- More services (Lambda, S3, RDS, SES)
- Professional setup for resume

**Not needed unless:**
- You expect high traffic (1000+ daily users)
- You want to learn AWS for job interviews
- You need 99.99% uptime
- You're building a real business

#### AWS Services Setup

**1. AWS RDS (Database) - Do This on AWS Console**

What: PostgreSQL database in the cloud
Why: Better than SQLite for production

Steps on aws.amazon.com:
1. Log in to AWS Console
2. Go to RDS service
3. Click "Create database"
4. Choose:
   - Engine: PostgreSQL 15
   - Template: Free tier
   - DB instance: db.t3.micro
   - Storage: 20 GB
   - Username: postgres
   - Password: (create strong password)
   - Public access: Yes
5. Click "Create database"
6. Wait 10 minutes
7. Copy connection string:
   ```
   postgresql://postgres:PASSWORD@xxx.rds.amazonaws.com:5432/postgres
   ```

**2. AWS Lambda (Backend) - Do This on AWS Console**

What: Serverless backend (no server management)
Why: Only pay for actual usage, auto-scales

Steps on aws.amazon.com:
1. Go to Lambda service
2. Click "Create function"
3. Choose:
   - Name: customer-insight-api
   - Runtime: Python 3.11
   - Memory: 1024 MB
   - Timeout: 30 seconds
4. Upload code (see CLOUD_DEPLOYMENT.md)
5. Add environment variables:
   ```
   DATABASE_URL=<RDS connection string>
   SECRET_KEY=<your-secret>
   DEMO_MODE=False
   ```

**3. API Gateway - Do This on AWS Console**

What: Creates public URL for Lambda function
Why: Makes Lambda accessible from internet

Steps on aws.amazon.com:
1. Go to API Gateway service
2. Create REST API
3. Create resource: `/{proxy+}`
4. Create method: ANY
5. Link to Lambda function
6. Deploy to stage: prod
7. Get URL: https://xxx.execute-api.us-east-1.amazonaws.com/prod

**4. AWS S3 (Storage) - Do This on AWS Console**

What: File storage for scraped data
Why: Reliable, cheap storage

Steps on aws.amazon.com:
1. Go to S3 service
2. Create bucket: customer-insight-data
3. Create folders:
   - raw-data/
   - processed-data/

**5. AWS SES (Email) - Do This on AWS Console**

What: Email sending service
Why: Reliable email delivery for alerts

Steps on aws.amazon.com:
1. Go to SES service
2. Verify email identity (your email)
3. Get SMTP credentials
4. Add to environment variables:
   ```
   EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
   EMAIL_PORT=587
   EMAIL_USERNAME=<SMTP username>
   EMAIL_PASSWORD=<SMTP password>
   ```

---

## Comparison: Local vs Render vs AWS

| Feature | Local | Render (Current) | AWS |
|---------|-------|------------------|-----|
| **Cost** | Free | Free ($0) | ~$15-30/month |
| **Setup Time** | 5 minutes | 10 minutes | 2-3 hours |
| **Public Access** | No | Yes | Yes |
| **Performance** | Fast | Sleeps after 15min | Always on |
| **Scalability** | 1 user | 10-50 users | 1000+ users |
| **Learning Curve** | Easy | Easy | Advanced |
| **Best For** | Development | Demos, Portfolio | Production, Jobs |

---

## What You Should Do

### For Portfolio/Demo (Current Setup is Perfect)
✅ Keep Render + Vercel
- Free
- Easy to maintain
- Looks professional
- Works for demos

**No action needed!** Everything is deployed and working.

### For Learning AWS (Optional)
📚 Follow CLOUD_DEPLOYMENT.md
- Good for resume
- Learn cloud skills
- Interview talking point
- Not needed for current project

### For Real Business (Future)
💼 Upgrade Render to paid tier ($7/month)
- Easier than AWS
- No sleep issues
- More RAM for ML models
- Keep everything else the same

---

## Current Deployment Status

✅ **Backend:** https://customer-insight-platform-4rgb.onrender.com
- Auto-deploys from GitHub main branch
- Demo mode (memory optimized)
- Free tier (sleeps after 15min)

✅ **Frontend:** https://customer-insight-platform.vercel.app
- Auto-deploys from GitHub main branch
- Fully responsive
- Free tier (unlimited bandwidth)

✅ **Repository:** https://github.com/amirtashdid99/customer-insight-platform
- All code pushed
- Auto-deployment configured
- Ready for sharing

---

## Quick Commands Reference

### Local Development
```bash
# Start demo mode (easy)
./start-demo.bat

# Start full mode (needs Redis)
./start-full.bat

# Stop everything
./stop-all.bat
```

### Git Deployment (Auto-deploys to Render + Vercel)
```bash
git add .
git commit -m "Update features"
git push
# Wait 5-10 minutes for deployment
```

### Manual Render Deployment
1. Go to https://dashboard.render.com
2. Click service → "Manual Deploy"

### Manual Vercel Deployment
1. Go to https://vercel.com/dashboard
2. Click project → "Deployments" → "Redeploy"

---

## Troubleshooting

### "Backend not responding"
- **Cause:** Render free tier sleeping
- **Solution:** Wait 30-60 seconds for wake-up
- **Prevention:** Use UptimeRobot to ping every 5 minutes

### "502 Bad Gateway"
- **Cause:** Backend crashed (out of memory)
- **Solution:** Already fixed with DEMO_MODE optimization
- **Check:** View Render logs for errors

### "CORS errors"
- **Cause:** Wrong ALLOWED_ORIGINS
- **Solution:** Check Render environment variables include Vercel URL

### "Database not found"
- **Cause:** SQLite file not created
- **Solution:** Backend auto-creates on first run
- **Check:** See backend/customer_insight.db file

---

## Summary

**You don't need to do anything right now!**

- ✅ Your app is already deployed and working
- ✅ Render auto-deploys when you push to GitHub
- ✅ Vercel auto-deploys when you push to GitHub
- ✅ Everything is free and functional

**Only explore AWS if:**
- You want to learn it for job interviews
- You need better performance
- You're building a real business

**For your portfolio, the current setup is perfect!** 🎉
