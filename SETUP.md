# 🚀 QUICK START GUIDE

## Your First 30 Minutes with This Project

### Step 1: Run the Setup Script (5 minutes)

Open PowerShell in the project directory and run:

```powershell
.\setup.ps1
```

This will:
- Check if Python and PostgreSQL are installed
- Create a virtual environment
- Install all Python dependencies
- Create a .env file

### Step 2: Configure Database (5 minutes)

1. **Create the database:**
   ```powershell
   psql -U postgres -c "CREATE DATABASE customer_insight_db;"
   ```

2. **Edit `backend\.env`:**
   - Open the file in a text editor
   - Change this line:
     ```
     DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/customer_insight_db
     ```
   - Replace `yourpassword` with your PostgreSQL password

3. **Generate a secret key:**
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   - Copy the output
   - Replace the SECRET_KEY in `.env`

### Step 3: Download Dataset (5 minutes)

1. Go to: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
2. Download `WA_Fn-UseC_-Telco-Customer-Churn.csv`
3. Place it in: `ml_training\datasets\`

### Step 4: Train the Models (10 minutes)

```powershell
cd ml_training\scripts
python train_churn_model.py
```

**Expected output:**
```
Loading data...
Training XGBoost model...
ROC-AUC Score: 0.84XX
Model saved successfully!
```

### Step 5: Initialize Database Schema (2 minutes)

```powershell
cd ..\..\backend
alembic upgrade head
```

**You should see:**
```
INFO  [alembic.runtime.migration] Running upgrade -> ..., Initial schema
```

### Step 6: Start the Backend (1 minute)

```powershell
cd app
python main.py
```

**Success looks like:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 7: Test the API (2 minutes)

1. Open browser: http://localhost:8000/docs
2. You should see the interactive API documentation
3. Try the `/health` endpoint - click "Try it out" → "Execute"
4. You should get: `{"status": "healthy", "database": "connected"}`

---

## Your First Analysis

### Test the Complete Pipeline:

1. **In the Swagger UI** (http://localhost:8000/docs):

2. **Find `POST /api/analysis/analyze`**
   - Click "Try it out"
   - Enter:
     ```json
     {
       "product_name": "iPhone 15"
     }
     ```
   - Click "Execute"

3. **Copy the `analysis_id`** from the response

4. **Check Status:**
   - Use `GET /api/analysis/status/{analysis_id}`
   - Paste your analysis_id
   - Execute
   - Watch the status change to "completed"

5. **View Results:**
   - Use `GET /api/analysis/dashboard/iPhone 15`
   - Execute
   - See all the analysis results!

---

## Project Structure at a Glance

```
project1/
│
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py            # ← Start here: Main API application
│   │   ├── api/               # API endpoints
│   │   │   └── analysis.py    # ← Core analysis logic
│   │   ├── ml/                # Machine Learning
│   │   │   ├── sentiment_analyzer.py
│   │   │   └── churn_predictor.py
│   │   ├── scrapers/          # Web scraping
│   │   │   └── web_scraper.py
│   │   ├── models/            # Database & schemas
│   │   │   ├── database_models.py
│   │   │   └── schemas.py
│   │   └── core/              # Configuration
│   │       ├── config.py
│   │       └── database.py
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Configuration (create from .env.example)
│
├── ml_training/               # Model Training
│   ├── scripts/
│   │   └── train_churn_model.py  # ← Run this to train models
│   └── datasets/              # Put Kaggle dataset here
│
├── trained_models/            # Saved ML models (created after training)
│
├── frontend/                  # React Frontend (create next)
│
├── IMPLEMENTATION_GUIDE.md    # ← Detailed step-by-step guide
├── CHECKLIST.md              # Track your progress
├── WHY_THIS_IS_UNIQUE.md     # For portfolio presentation
└── README.md                 # Project overview
```

---

## Common Issues & Solutions

### Issue: "psql: command not found"
**Solution:** Add PostgreSQL to your PATH
- Windows: Add `C:\Program Files\PostgreSQL\15\bin` to PATH

### Issue: "Import error: No module named 'fastapi'"
**Solution:** Make sure virtual environment is activated
```powershell
cd backend
.\venv\Scripts\Activate.ps1
```

### Issue: "Database connection failed"
**Solution:** 
1. Check PostgreSQL is running
2. Verify password in `.env` is correct
3. Ensure database exists: `psql -U postgres -l`

### Issue: "Model file not found"
**Solution:** You need to train the models first
```powershell
cd ml_training\scripts
python train_churn_model.py
```

### Issue: Sentiment model downloading is slow
**Solution:** The first time you run sentiment analysis, it downloads ~250MB model from Hugging Face. This is normal. Subsequent runs will be fast.

---

## Next Steps After Quick Start

### Immediate (Today):
1. ✅ Get backend running
2. ✅ Complete one analysis
3. ✅ Verify data in PostgreSQL
   ```powershell
   psql -U postgres -d customer_insight_db
   SELECT * FROM products;
   SELECT * FROM analyses;
   \q
   ```

### This Week:
1. Read `IMPLEMENTATION_GUIDE.md` in detail
2. Understand each component
3. Customize the web scraper
4. Start the React frontend (Phase 3)

### This Month:
1. Complete the full stack
2. Add custom features
3. Deploy to cloud
4. Write blog post
5. Update LinkedIn

---

## Learning Resources

### FastAPI:
- Official Docs: https://fastapi.tiangolo.com/
- Focus on: Background Tasks, Dependency Injection, Pydantic

### SQLAlchemy:
- Official Tutorial: https://docs.sqlalchemy.org/en/20/tutorial/
- Focus on: ORM, Relationships, Queries

### Transformers (Hugging Face):
- Docs: https://huggingface.co/docs/transformers/
- Focus on: Pipelines, Sentiment Analysis

### XGBoost:
- Docs: https://xgboost.readthedocs.io/
- Focus on: Classification, Hyperparameters

### React + TypeScript:
- React Docs: https://react.dev/
- TypeScript Handbook: https://www.typescriptlang.org/docs/

---

## Getting Help

### Check These First:
1. Error messages - they're usually helpful!
2. `IMPLEMENTATION_GUIDE.md` - detailed explanations
3. Code comments - everything is documented
4. API docs at http://localhost:8000/docs

### Debug Mode:
Backend logs show everything:
- SQL queries
- ML model loading
- Scraping progress
- Error stack traces

### Test Individual Components:
```python
# Test sentiment analyzer
from app.ml.sentiment_analyzer import get_sentiment_analyzer
analyzer = get_sentiment_analyzer()
print(analyzer.analyze("This is great!"))

# Test database connection
from app.core.database import SessionLocal
db = SessionLocal()
print("Database connected!" if db else "Failed")
```

---

## Setup Complete! 🎉

Current status:
- ✅ Working backend API
- ✅ Trained ML models  
- ✅ Database configured
- ✅ Full architecture implemented

**Next:** Follow the `IMPLEMENTATION_GUIDE.md` for detailed explanations of each component.

**Note:** This project demonstrates full-stack ML engineering. Understanding each component is key for interviews.

---

## Quick Command Reference

```powershell
# Activate virtual environment
cd backend
.\venv\Scripts\Activate.ps1

# Start backend server
cd app
python main.py

# Train models
cd ml_training\scripts
python train_churn_model.py

# Database operations
psql -U postgres -d customer_insight_db
\dt                    # List tables
\d products           # Describe table
SELECT * FROM analyses;

# Run migrations
cd backend
alembic upgrade head
```

Good luck! 🚀
