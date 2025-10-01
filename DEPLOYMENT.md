# Deployment Guide - Render (Backend) + Vercel (Frontend)

This guide walks you through deploying the Customer Insight Platform with:
- **Backend (API)**: Render (Free tier with Demo Mode)
- **Frontend (React)**: Vercel (Free tier)

---

## Prerequisites

1. GitHub account with code pushed to repository
2. Render account (sign up at https://render.com)
3. Vercel account (sign up at https://vercel.com)

---

## Part 1: Deploy Backend to Render

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Connect your GitHub account

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `customer-insight-platform`
3. Configure the service:

**Basic Settings:**
- **Name**: `customer-insight-platform-api` (or your choice)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- Select **Free** (512 MB RAM, sleeps after inactivity)

### Step 3: Set Environment Variables
Click "Advanced" and add these environment variables:

```bash
# Required
DEMO_MODE=True
DATABASE_URL=sqlite:///./customer_insight.db
SECRET_KEY=your-super-secret-key-min-32-chars-random-string-here-change-this
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app

# Optional
APP_NAME=Customer Insight Platform
APP_VERSION=1.0.0
DEBUG=False
```

**Important Notes:**
- `DEMO_MODE=True` - Uses sample data, no Redis needed (perfect for free tier)
- `ALLOWED_ORIGINS` - Update after deploying frontend to Vercel
- Generate a strong `SECRET_KEY`: Use `python -c "import secrets; print(secrets.token_urlsafe(32))"`

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for build and deployment
3. Note your backend URL: `https://customer-insight-platform-api.onrender.com`

### Step 5: Test Backend
Visit: `https://your-backend-url.onrender.com/`

Should return:
```json
{
  "message": "Customer Insight Platform API",
  "version": "1.0.0",
  "status": "running",
  "demo_mode": true
}
```

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub
3. Connect your GitHub account

### Step 2: Import Project
1. Click "Add New..." → "Project"
2. Import your repository: `customer-insight-platform`
3. Configure project:

**Framework Preset:**
- Vercel will auto-detect: `Create React App`

**Root Directory:**
- Set to: `frontend`

**Build Settings:**
- Build Command: `npm run build` (auto-detected)
- Output Directory: `build` (auto-detected)
- Install Command: `npm install` (auto-detected)

### Step 3: Set Environment Variables
Add environment variable:

```
REACT_APP_API_URL=https://customer-insight-platform-api.onrender.com
```

Replace with your actual Render backend URL (no trailing slash).

### Step 4: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes for build
3. Note your frontend URL: `https://customer-insight-platform-abc123.vercel.app`

### Step 5: Update Backend CORS
1. Go back to Render dashboard
2. Open your backend service
3. Edit environment variable:
   ```
   ALLOWED_ORIGINS=https://customer-insight-platform-abc123.vercel.app,http://localhost:3000
   ```
4. Click "Save Changes" - service will redeploy

---

## Part 3: Test Your Deployed App

1. Visit your Vercel URL
2. Try the example queries (iPhone 15, Tesla Model 3, etc.)
3. Analysis should complete in ~5 seconds with sample data
4. Check browser console for any errors

---

## Troubleshooting

### Backend Issues

**"Service Unavailable" or 503 Error:**
- Render free tier sleeps after 15 min inactivity
- First request takes 30-60 seconds to wake up
- Subsequent requests are fast

**CORS Errors:**
- Verify `ALLOWED_ORIGINS` includes your Vercel URL
- Check for trailing slashes (don't use them)
- Redeploy backend after changing environment variables

**Database Errors:**
- SQLite is file-based and works on Render
- Data persists between deploys
- For production, consider PostgreSQL

### Frontend Issues

**"Failed to fetch" or Network Errors:**
- Check `REACT_APP_API_URL` is set correctly
- Ensure backend is deployed and running
- Check browser console for actual error

**Demo Notice Not Showing:**
- Backend must return `demo_mode: true` in root endpoint
- Check `/` endpoint response

**Example Buttons Not Working:**
- Clear browser cache
- Check browser console for JavaScript errors

---

## Monitoring & Limits

### Render Free Tier Limits:
- 512 MB RAM
- Sleeps after 15 min inactivity
- 750 hours/month (plenty for demo)
- Shared CPU

### Vercel Free Tier Limits:
- 100 GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS
- Global CDN

---

## Going to Production (Optional)

If you want real scraping with Celery + Redis:

1. **Upgrade Render**: Switch to paid plan ($7/month)
2. **Add Redis**: Add Render Redis instance
3. **Add Worker**: Create new "Background Worker" on Render
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `celery -A app.core.celery_app worker --loglevel=info`
4. **Update Environment**: Set `DEMO_MODE=False` and `REDIS_URL`

---

## Custom Domain (Optional)

### Vercel:
1. Go to Project Settings → Domains
2. Add your domain
3. Follow DNS configuration instructions

### Render:
1. Go to Service Settings → Custom Domain
2. Add your domain
3. Configure DNS records

---

## Automatic Deployments

Both platforms support automatic deployments:

- **Push to GitHub** → Automatic deployment
- **Pull Request** → Preview deployment (Vercel)
- **Merge to main** → Production deployment

---

## Success! 🎉

Your app is now live:
- **Frontend**: https://your-app.vercel.app
- **Backend API**: https://your-api.onrender.com
- **GitHub**: https://github.com/amirtashdid99/customer-insight-platform

---

## Next Steps

1. ✅ Share your app link on GitHub README
2. ✅ Add screenshots to README
3. ✅ Test from different devices
4. ✅ Monitor logs on Render/Vercel dashboards
5. ✅ Add app to your portfolio/resume
