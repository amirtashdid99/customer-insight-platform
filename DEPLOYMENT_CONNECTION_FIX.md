# 🔧 Fix: Frontend Can't Connect to Backend

## Current Status:

✅ **Backend (Render):** Working!
- URL: https://customer-insight-platform-4rgb.onrender.com
- Returns correct JSON with `demo_mode: true`

❌ **Frontend (Vercel):** Connection Error
- URL: https://customer-insight-platform.vercel.app
- Error: "Failed to start analysis. Make sure the backend is running."

---

## 🎯 The Problem:

The frontend can't reach the backend. This is caused by **one or both** of these issues:

1. **Missing Environment Variable** - `REACT_APP_API_URL` not set in Vercel
2. **CORS Blocking** - Backend doesn't allow requests from Vercel domain

---

## ✅ Solution: 2-Step Fix

### Step 1: Add Environment Variable in Vercel

1. Go to your Vercel project: https://vercel.com/dashboard
2. Click on your project: `customer-insight-platform`
3. Go to **Settings** → **Environment Variables**
4. Add a new variable:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** `https://customer-insight-platform-4rgb.onrender.com`
   - **Environments:** Select all (Production, Preview, Development)
5. Click **Save**

### Step 2: Update CORS in Render Backend

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your backend service: `customer-insight-platform-4rgb`
3. Go to **Environment** tab
4. Find the `ALLOWED_ORIGINS` variable
5. Update it to include your Vercel URL:
   ```
   https://customer-insight-platform.vercel.app,http://localhost:3000
   ```
   (Replace with your exact Vercel URL if different)
6. Click **Save Changes**
7. Wait for the service to redeploy (1-2 minutes)

---

## 🚀 Redeploy Frontend

After adding the environment variable:

**Option A: Automatic**
1. Go to your Vercel project
2. **Deployments** tab
3. Click ⋯ (three dots) on the latest deployment
4. Click **Redeploy**
5. Wait 2-3 minutes

**Option B: From GitHub**
```cmd
# Make a small change and push
git commit --allow-empty -m "Trigger redeploy"
git push origin main
```

---

## 🧪 How to Verify the Fix:

### Step 1: Check Backend CORS
Open your backend URL in browser:
```
https://customer-insight-platform-4rgb.onrender.com/
```
Should show JSON with `demo_mode: true` ✅ (Already working!)

### Step 2: Check Frontend Can Reach Backend
1. Open your Vercel app: https://customer-insight-platform.vercel.app
2. Open browser DevTools (F12)
3. Go to **Console** tab
4. Try clicking "iPhone 15" example
5. Check the console for errors

**If you see:**
- ❌ `CORS policy: No 'Access-Control-Allow-Origin'` → Update CORS in Render
- ❌ `undefined` in API URL → Environment variable not set in Vercel
- ✅ Analysis starts → It works!

---

## 🔍 Detailed Troubleshooting:

### Check Environment Variable in Vercel:

**In your deployed app, check the Network tab:**
1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Click "iPhone 15" button
4. Look for the request - what URL is it calling?
   - ✅ Should call: `https://customer-insight-platform-4rgb.onrender.com/api/analyze`
   - ❌ If calling: `http://localhost:8000/api/analyze` → Env var not set

### Check CORS in Render:

**Test CORS from browser console:**
```javascript
fetch('https://customer-insight-platform-4rgb.onrender.com/', {
  method: 'GET',
  headers: { 'Origin': 'https://customer-insight-platform.vercel.app' }
})
.then(res => res.json())
.then(data => console.log('CORS works!', data))
.catch(err => console.error('CORS blocked!', err));
```

---

## 📋 Expected Configuration:

### Vercel Environment Variables:
```
Name: REACT_APP_API_URL
Value: https://customer-insight-platform-4rgb.onrender.com
```

### Render Environment Variables:
```
DEMO_MODE=True
ALLOWED_ORIGINS=https://customer-insight-platform.vercel.app,http://localhost:3000
DATABASE_URL=sqlite:///./customer_insight.db
SECRET_KEY=<your-secret-key>
APP_NAME=Customer Insight Platform
APP_VERSION=1.0.0
DEBUG=False
```

---

## 🎯 Quick Checklist:

- [ ] Backend is running and returns JSON ✅ (Already done!)
- [ ] `REACT_APP_API_URL` added to Vercel environment variables
- [ ] `ALLOWED_ORIGINS` updated in Render to include Vercel URL
- [ ] Frontend redeployed after adding environment variable
- [ ] Backend redeployed after updating CORS
- [ ] Test the app - click example buttons
- [ ] Check browser console for errors

---

## 💡 Common Mistakes:

### ❌ Mistake 1: Trailing Slash
```
Wrong: https://customer-insight-platform-4rgb.onrender.com/
Right: https://customer-insight-platform-4rgb.onrender.com
```

### ❌ Mistake 2: HTTP vs HTTPS
```
Wrong: http://customer-insight-platform-4rgb.onrender.com
Right: https://customer-insight-platform-4rgb.onrender.com
```

### ❌ Mistake 3: Typo in Domain
```
Wrong: https://customer-insight-platform.vercel.app
Check:  https://customer-insight-platform-abc123.vercel.app
```

### ❌ Mistake 4: Not Redeploying
- After adding env vars, you MUST redeploy
- Changes don't apply to existing deployments

---

## 🎉 After the Fix:

Your app should work like this:

1. User visits: `https://customer-insight-platform.vercel.app`
2. Clicks "iPhone 15"
3. Frontend calls: `https://customer-insight-platform-4rgb.onrender.com/api/analyze`
4. Backend processes in ~5 seconds (demo mode)
5. Results display on the dashboard

---

## 🐛 Still Not Working?

### Check Render Logs:
1. Go to Render dashboard
2. Click your service
3. Go to **Logs** tab
4. Look for CORS or connection errors

### Check Vercel Logs:
1. Go to Vercel dashboard
2. Click your project
3. Go to **Deployments** tab
4. Click on the latest deployment
5. Check **Function Logs** and **Build Logs**

### Test Locally First:
```cmd
# In frontend folder, create .env:
echo REACT_APP_API_URL=https://customer-insight-platform-4rgb.onrender.com > .env

# Test locally:
npm start
```

If it works locally but not on Vercel, it's definitely the environment variable!

---

## 📞 Summary:

**Problem:** Frontend can't connect to backend  
**Cause:** Missing `REACT_APP_API_URL` in Vercel or CORS blocking  
**Solution:**  
1. Add `REACT_APP_API_URL` in Vercel settings
2. Add Vercel URL to `ALLOWED_ORIGINS` in Render
3. Redeploy both services

**Your URLs:**
- Backend: https://customer-insight-platform-4rgb.onrender.com
- Frontend: https://customer-insight-platform.vercel.app

Let me know if you need help with any of these steps! 🚀
