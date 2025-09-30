# 🔧 Common Setup Issues - SOLVED!

## Issue 1: TypeScript Version Conflict ✅ FIXED

**Error:**
```
npm error ERESOLVE could not resolve
npm error peerOptional typescript@"^3.2.1 || ^4" from react-scripts@5.0.1
npm error Conflicting peer dependency: typescript@4.9.5
```

**Solution:**
Changed TypeScript version in `package.json` from `^5.3.3` to `^4.9.5`

**Why:** react-scripts 5.0.1 requires TypeScript 4.x, not 5.x

---

## Issue 2: PowerShell Script Execution Policy ✅ FIXED

**Error:**
```
npm : File C:\Program Files\nodejs\npm.ps1 cannot be loaded because 
running scripts is disabled on this system.
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Why:** Windows security blocks script execution by default. This allows npm scripts to run.

---

## Issue 3: Wrong Directory

**Error:**
```
ENOENT: no such file or directory, open '...\project1\package.json'
```

**Solution:**
Make sure you're in the `frontend` directory:
```powershell
cd c:\Users\R00T99\Desktop\GitHub\1\project1\frontend
npm install
```

---

## Current Status

✅ TypeScript version fixed
✅ PowerShell execution policy set
✅ npm install running...

**What's happening now:**
- npm is downloading ~200 packages
- Installing React, TypeScript, Recharts, Axios, etc.
- This takes 2-3 minutes (normal!)

**You'll see:**
- Spinner animation (⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏)
- Progress messages
- Eventually: "added XXX packages in XXs"

---

## After Installation Completes

### Run the Frontend:
```powershell
npm start
```

This will:
- Compile TypeScript to JavaScript
- Start development server
- Automatically open http://localhost:3000 in your browser

### If Port 3000 is Busy:
```powershell
# Use a different port
$env:PORT=3001
npm start
```

---

## Running the Complete App

**Terminal 1 - Backend:**
```powershell
cd c:\Users\R00T99\Desktop\GitHub\1\project1\backend\app
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd c:\Users\R00T99\Desktop\GitHub\1\project1\frontend
npm start
```

**Then:**
- Open http://localhost:3000
- Enter a product name
- Click "Analyze"
- Watch your full-stack app in action! 🎉

---

## Other Potential Issues

### "Module not found" errors
```powershell
# Clear cache and reinstall
rm -r node_modules
npm install
```

### "Cannot find module 'react'"
```powershell
# Make sure you're in frontend directory
cd frontend
npm install
```

### Backend connection errors
**Check:**
1. Backend is running on port 8000
2. No CORS errors in browser console
3. `.env` file exists in frontend with `REACT_APP_API_URL=http://localhost:8000`

### Slow initial load
**Normal!** First time:
- TypeScript compilation takes ~30 seconds
- BERT model downloads ~250MB (backend)
- Subsequent loads are much faster

---

## Success Indicators

✅ Frontend:
```
Compiled successfully!

You can now view customer-insight-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

✅ Backend:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ Working App:
- Beautiful purple gradient background
- Search box appears
- Can enter product name
- "Analyze" button works
- Dashboard shows results

---

## Need Help?

1. Check terminal output for specific errors
2. Read error messages carefully
3. Google the exact error message
4. Check browser console (F12) for frontend errors
5. Check backend terminal for API errors

---

**You're almost there! Just waiting for npm install to finish...** ⏳
