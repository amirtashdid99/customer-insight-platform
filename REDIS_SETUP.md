# Redis Installation & Setup Guide for Windows

## ⚠️ Error: "Error 10061 connecting to localhost:6379"

This means **Redis is not running**. You need to install and start Redis before using Full Mode.

---

## 📥 Option 1: Install Redis (Recommended for Full Mode)

### Method A: Using Chocolatey (Easiest)

1. **Install Chocolatey** (if not already installed):
   - Open PowerShell as Administrator
   - Run:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install Redis**:
   ```powershell
   choco install redis-64 -y
   ```

3. **Start Redis**:
   ```cmd
   redis-server
   ```

### Method B: Manual Download

1. **Download Redis**:
   - Go to: https://github.com/microsoftarchive/redis/releases
   - Download: `Redis-x64-3.0.504.msi` (or latest version)

2. **Install**:
   - Run the MSI installer
   - Follow installation wizard
   - Add Redis to PATH when prompted

3. **Start Redis**:
   ```cmd
   redis-server
   ```

### Method C: Using Memurai (Redis Alternative for Windows)

1. **Download Memurai**:
   - Go to: https://www.memurai.com/get-memurai
   - Download free version

2. **Install**:
   - Run installer
   - Memurai runs as a Windows service automatically

3. **Check Status**:
   ```cmd
   sc query Memurai
   ```

---

## 🚀 Quick Test After Installation

```cmd
# Start Redis server (in a terminal):
redis-server

# In another terminal, test connection:
redis-cli ping
```

Should respond with: `PONG`

---

## 🔧 Using Full Mode After Redis Installation

Once Redis is installed and running:

```cmd
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start everything else
start-full.bat
```

---

## 🎯 Alternative: Use Demo Mode Instead

**Don't want to install Redis?** Use Demo Mode instead!

```cmd
start-demo.bat
```

Demo Mode:
- ✅ No Redis required
- ✅ Works instantly
- ✅ Uses mock data (~5 seconds)
- ✅ Perfect for testing and demos
- ❌ No real web scraping

Full Mode:
- ✅ Real web scraping
- ✅ Production-ready
- ❌ Requires Redis + Celery
- ❌ More complex setup

---

## 🐛 Troubleshooting

### Redis Won't Start

**Error: "Creating Server TCP listening socket *:6379: bind: No error"**
- Redis is already running
- Check: `tasklist | findstr redis-server`

**Error: "Can't open the log file"**
- Run as Administrator
- Or specify log file: `redis-server --logfile redis.log`

### Port 6379 Already in Use

```cmd
# Find what's using port 6379:
netstat -ano | findstr :6379

# Kill the process (replace PID with actual number):
taskkill /F /PID <PID>
```

### Redis Installed but Not in PATH

```cmd
# Find Redis installation:
dir C:\ /s /b | findstr redis-server.exe

# Run with full path:
"C:\Program Files\Redis\redis-server.exe"
```

---

## 📝 Configuration

### Redis Config File (Optional)

Create `redis.windows.conf`:

```conf
# Port
port 6379

# Bind to localhost only (secure)
bind 127.0.0.1

# Memory limit (256MB)
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence (save to disk)
save 900 1
save 300 10
save 60 10000

# Log file
logfile "redis.log"
```

Run with config:
```cmd
redis-server redis.windows.conf
```

---

## 🎯 Recommended Setup

### For Development:
```cmd
start-demo.bat
```
No Redis needed, instant start!

### For Production Testing:
1. Install Redis (one-time setup)
2. Start Redis: `redis-server`
3. Run: `start-full.bat`

---

## 💡 Pro Tips

### 1. Run Redis as Background Service

Using Memurai (automatic):
- Installs as Windows service
- Starts automatically on boot
- No terminal needed

Using Redis + NSSM:
```cmd
# Download NSSM from: https://nssm.cc/download
nssm install Redis "C:\Program Files\Redis\redis-server.exe"
nssm start Redis
```

### 2. Check Redis Status

```cmd
# Is Redis running?
tasklist | findstr redis

# Test connection:
redis-cli ping

# Get info:
redis-cli info
```

### 3. Quick Redis Commands

```cmd
# Connect to Redis:
redis-cli

# Inside redis-cli:
PING              # Test connection
SET mykey "test"  # Set a value
GET mykey         # Get a value
KEYS *            # List all keys
FLUSHALL          # Clear everything (careful!)
EXIT              # Quit redis-cli
```

---

## 🎉 Summary

**Got the Error 10061?**
1. Install Redis (one of the 3 methods above)
2. Start Redis: `redis-server`
3. Then run: `start-full.bat`

**Don't want to install Redis?**
- Use Demo Mode: `start-demo.bat`
- Perfect for testing and demos!

**Need Help?**
- Check if Redis is running: `tasklist | findstr redis`
- Test connection: `redis-cli ping`
- See this guide: https://redis.io/docs/getting-started/

---

## 📚 Next Steps

After installing Redis:
1. ✅ Start Redis: `redis-server`
2. ✅ Run full mode: `start-full.bat`
3. ✅ Test web scraping with real data
4. ✅ Monitor Celery worker logs

Or stick with Demo Mode:
1. ✅ Run: `start-demo.bat`
2. ✅ Everything works instantly
3. ✅ Perfect for development
