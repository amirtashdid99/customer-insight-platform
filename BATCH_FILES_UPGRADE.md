# ✅ Batch Files Now Handle DEMO_MODE Automatically!

## 🎉 What's New?

Your batch files are now **SMART** - they automatically set the correct `DEMO_MODE` for you!

---

## 📍 Where is the .env file?

**Location:** `backend/.env`

You can view it:
```cmd
type backend\.env
```

---

## 🚀 How to Use (It's Now Automatic!)

### Demo Mode (Quick & Easy):
```cmd
start-demo.bat
```

**What it does automatically:**
1. ✅ Sets `DEMO_MODE=True` in `backend/.env`
2. ✅ Starts backend server
3. ✅ No Redis needed!

### Full Mode (Real Scraping):
```cmd
start-full.bat
```

**What it does automatically:**
1. ✅ Sets `DEMO_MODE=False` in `backend/.env`
2. ✅ Checks if Redis is running
3. ✅ Starts backend server
4. ⚠️ You still need to run Redis + Celery separately

---

## 🔄 What Changed?

### ❌ Before (Old Way):
1. Edit `backend/.env` manually
2. Change `DEMO_MODE=True` or `False`
3. Save the file
4. Run the batch file
5. Easy to forget or make mistakes!

### ✅ After (New Way):
1. Just run `start-demo.bat` or `start-full.bat`
2. **That's it!** 🎉

---

## 📝 Technical Details

### Demo Batch File (`start-demo.bat`):
```bat
# Automatically runs this command:
powershell -Command "(Get-Content .env) -replace 'DEMO_MODE=False', 'DEMO_MODE=True' | Set-Content .env"
```

### Full Batch File (`start-full.bat`):
```bat
# Automatically runs this command:
powershell -Command "(Get-Content .env) -replace 'DEMO_MODE=True', 'DEMO_MODE=False' | Set-Content .env"

# Also checks Redis:
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient('localhost', 6379); ... }"
```

---

## 🧪 Test It Out!

### Check Current Mode:
```cmd
type backend\.env | findstr DEMO_MODE
```

### Switch to Demo Mode:
```cmd
start-demo.bat
# Then check: type backend\.env | findstr DEMO_MODE
# Should show: DEMO_MODE=True
```

### Switch to Full Mode:
```cmd
start-full.bat
# Then check: type backend\.env | findstr DEMO_MODE
# Should show: DEMO_MODE=False
```

---

## 📚 Documentation

Read **HOW_TO_RUN.md** for complete instructions and troubleshooting!

---

## ✨ Summary

**Question:** "Can't it do that automatically?"  
**Answer:** ✅ **YES! Now it does!**

- `start-demo.bat` → Sets `DEMO_MODE=True`
- `start-full.bat` → Sets `DEMO_MODE=False`

No more manual editing required! 🎊
